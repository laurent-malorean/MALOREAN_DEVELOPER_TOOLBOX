#!/usr/bin/env python3
"""Contrôles communs de la boîte à outils, indépendants de la stack du projet.

Implémente les contrôles décrits dans
developer/driven-development/development-workflow.md :

  vocabulary     aucun mot refusé de l'ontologie dans le dépôt
  traceability   identifiants des tests connus, chaque exigence a un critère,
                 critères et règles testables couverts par un test
                 (--strict : bloquant ; --write : génère les lignes « Test »)
  extract        génère l'extrait de spécification de chaque changement en cours
  commit         vocabulary + traceability + extraits à jour, puis commandes du projet
  release        contrôles avant archivage d'un changement (--archive : archive)

Python 3.9+, bibliothèque standard uniquement.
Configuration optionnelle : toolbox-checks.json à la racine du projet.
"""
import argparse
import datetime
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

CONFIG_NAME = "toolbox-checks.json"
DEFAULT_EXCLUDE_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "vendor", "dist", "build", "target",
    ".venv", "venv", "__pycache__", ".next", ".nuxt", "coverage", ".idea", ".vscode",
}
MAX_FILE_SIZE = 2_000_000

ID = r"[a-z0-9]+(?:-[a-z0-9]+)*(?:\.[a-z0-9]+(?:-[a-z0-9]+)*)+"
ID_RE = re.compile(rf"^{ID}$")
REQUIREMENT_HEADING = re.compile(rf"^###\s+({ID})\s*$")
CRITERION_HEADING = re.compile(rf"^#####\s+({ID})\s*$")
ANNOTATION = re.compile(rf"@(spec|rule)\s+({ID})")
CLARIFY = re.compile(r"À clarifier\s*:", re.IGNORECASE)
TEST_LINE = re.compile(r"^\s*-\s*Test\s*:")
UNCHECKED_TASK = re.compile(r"^\s*-\s*\[ \]")
RULE_CITATION = re.compile(rf"ontologie\s*›\s*({ID})")
VERDICT = re.compile(r"Verdict\s*:\s*(Accepté|À reprendre)", re.IGNORECASE)
EXTRACT_NAME = "spec-extract.md"
EXTRACT_HEADER = (
    "<!-- Généré par toolbox-checks à partir de doc/specs/ et doc/ontology/ — ne pas modifier.\n"
    "     Régénérer : python3 tools/toolbox-checks/toolbox_checks.py extract -->"
)
LETTERS = re.compile(r"[^\W\d_]+")
CAMEL_PART = re.compile(r"[A-ZÀ-Þ]?[a-zß-ÿ]+|[A-ZÀ-Þ]+(?![a-zß-ÿ])")


# --------------------------------------------------------------------------- config

@dataclass
class Config:
    root: Path
    doc: Path
    exclude_dirs: Set[str]
    exclude_globs: List[str]
    test_paths: List[Path]
    commit_commands: List[str] = field(default_factory=list)
    # Dossier de l'outil lui-même : jamais analysé (ses tests et sa doc contiennent des exemples).
    tool_dir: Path = field(default_factory=lambda: Path(__file__).resolve().parent)

    @property
    def ontology_dir(self) -> Path:
        return self.doc / "ontology"

    @property
    def specs_dir(self) -> Path:
        return self.doc / "specs"

    @property
    def archive_dir(self) -> Path:
        return self.doc / "changes" / "archive"


def load_config(root: Path) -> Config:
    root = Path(root).resolve()
    data = {}
    config_file = root / CONFIG_NAME
    if config_file.exists():
        data = json.loads(config_file.read_text(encoding="utf-8"))
    return Config(
        root=root,
        doc=root / data.get("doc_dir", "doc"),
        exclude_dirs=DEFAULT_EXCLUDE_DIRS | set(data.get("exclude_dirs", [])),
        exclude_globs=[CONFIG_NAME] + list(data.get("exclude_globs", [])),
        test_paths=[root / p for p in data.get("test_paths", [])],
        commit_commands=list(data.get("commit_commands", [])),
    )


# --------------------------------------------------------------------------- fichiers

def _is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _rel(cfg: Config, path: Path) -> str:
    try:
        return path.resolve().relative_to(cfg.root).as_posix()
    except ValueError:
        return path.as_posix()


def iter_text_files(cfg: Config, bases: List[Path]):
    """Fichiers texte sous `bases`, hors dossiers et motifs exclus."""
    for base in bases:
        if base.is_file():
            candidates = [base]
        elif base.is_dir():
            candidates = []
            for dirpath, dirnames, filenames in os.walk(base):
                dirnames[:] = sorted(
                    d for d in dirnames
                    if d not in cfg.exclude_dirs and not _is_under(Path(dirpath) / d, cfg.tool_dir)
                )
                candidates.extend(Path(dirpath) / f for f in sorted(filenames))
        else:
            continue
        for path in candidates:
            rel = _rel(cfg, path)
            if any(fnmatch.fnmatch(rel, g) for g in cfg.exclude_globs):
                continue
            try:
                if path.stat().st_size > MAX_FILE_SIZE:
                    continue
                raw = path.read_bytes()
            except OSError:
                continue
            if b"\0" in raw[:8192]:
                continue
            try:
                yield path, raw.decode("utf-8")
            except UnicodeDecodeError:
                continue


def _markdown_files(directory: Path) -> List[Path]:
    return sorted(directory.rglob("*.md")) if directory.is_dir() else []


def _lines_outside_fences(text: str):
    """(numéro, ligne) des lignes hors blocs de code Markdown."""
    in_fence = False
    for number, line in enumerate(text.split("\n"), start=1):
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield number, line


def _section(text: str, title: str) -> List[str]:
    """Lignes d'une section `## title` (jusqu'au titre de même niveau ou supérieur)."""
    out, inside = [], False
    for _, line in _lines_outside_fences(text):
        if re.match(r"^#{1,2}\s", line):
            inside = line.strip().lstrip("#").strip() == title
            continue
        if inside:
            out.append(line)
    return out


def _table_rows(lines: List[str]) -> List[List[str]]:
    """Lignes de données d'un tableau Markdown (sans en-tête ni séparateur)."""
    rows = [l.strip() for l in lines if l.strip().startswith("|")]
    data = []
    for row in rows[2:]:
        cells = [c.strip().strip("`").strip() for c in row.strip("|").split("|")]
        data.append(cells)
    return data


# --------------------------------------------------------------------------- ontologie

def refused_words(cfg: Config) -> List[str]:
    words = []
    for path in _markdown_files(cfg.ontology_dir):
        for cells in _table_rows(_section(path.read_text(encoding="utf-8"), "Mots refusés")):
            if cells and cells[0]:
                words.append(cells[0])
    return words


def ontology_rules(cfg: Config) -> Dict[str, dict]:
    rules = {}
    for path in _markdown_files(cfg.ontology_dir):
        for cells in _table_rows(_section(path.read_text(encoding="utf-8"), "Règles")):
            if cells and ID_RE.match(cells[0]):
                testable = not (len(cells) > 2 and cells[2].lower().startswith("non"))
                text = cells[1] if len(cells) > 1 else ""
                rules.setdefault(cells[0], {"file": path, "testable": testable, "count": 0, "text": text})
                rules[cells[0]]["count"] += 1
    return rules


# --------------------------------------------------------------------------- vocabulaire

def _tokens(line: str) -> Set[str]:
    tokens = set()
    for word in LETTERS.findall(line):
        tokens.add(word.lower())
        tokens.update(part.lower() for part in CAMEL_PART.findall(word))
    return tokens


def _contains(word: str, line: str, tokens: Set[str]) -> bool:
    if " " in word.strip():
        return re.search(rf"(?<!\w){re.escape(word)}(?!\w)", line, re.IGNORECASE) is not None
    return word.lower() in tokens


def check_vocabulary(cfg: Config) -> List[str]:
    """Occurrences de mots refusés, hors archives, table des mots refusés et mentions « Autrefois »."""
    words = refused_words(cfg)
    if not words:
        return []
    hits = []
    for path, text in iter_text_files(cfg, [cfg.root]):
        if _is_under(path, cfg.archive_dir) or path.name == EXTRACT_NAME:
            continue
        in_ontology = _is_under(path, cfg.ontology_dir)
        in_refused_table = False
        for number, line in enumerate(text.split("\n"), start=1):
            if in_ontology:
                if re.match(r"^#{1,2}\s", line):
                    in_refused_table = line.strip().lstrip("#").strip() == "Mots refusés"
                if in_refused_table or "Autrefois" in line:
                    continue
            tokens = _tokens(line)
            for word in words:
                if _contains(word, line, tokens):
                    hits.append(f"{_rel(cfg, path)}:{number} : mot refusé « {word} »")
    return hits


# --------------------------------------------------------------------------- spécifications

@dataclass
class Specs:
    requirements: Dict[str, dict]
    criteria: Dict[str, dict]
    errors: List[str]


def parse_specs(cfg: Config) -> Specs:
    requirements, criteria, errors = {}, {}, []
    seen: Dict[str, str] = {}

    def register(identifier, where):
        if identifier in seen:
            errors.append(f"{where} : identifiant en double « {identifier} » (déjà en {seen[identifier]})")
        else:
            seen[identifier] = where

    for path in _markdown_files(cfg.specs_dir):
        current = None
        for number, line in _lines_outside_fences(path.read_text(encoding="utf-8")):
            where = f"{_rel(cfg, path)}:{number}"
            m = REQUIREMENT_HEADING.match(line)
            if m:
                current = m.group(1)
                register(current, where)
                requirements[current] = {"where": where, "criteria": []}
                continue
            m = CRITERION_HEADING.match(line)
            if m:
                register(m.group(1), where)
                criteria[m.group(1)] = {"where": where, "file": path, "requirement": current}
                if current:
                    requirements[current]["criteria"].append(m.group(1))
                continue
            if re.match(r"^#{1,2}\s", line):
                current = None
    return Specs(requirements, criteria, errors)


def collect_annotations(cfg: Config) -> List[Tuple[str, str, str]]:
    """(type, identifiant, emplacement) pour chaque @spec / @rule hors documentation."""
    bases = cfg.test_paths or [cfg.root]
    found = []
    for path, text in iter_text_files(cfg, bases):
        if _is_under(path, cfg.doc):
            continue
        for number, line in enumerate(text.split("\n"), start=1):
            for kind, identifier in ANNOTATION.findall(line):
                found.append((kind, identifier, f"{_rel(cfg, path)}:{number}"))
    return found


def _tests_by_id(cfg: Config) -> Dict[str, List[str]]:
    by_id: Dict[str, List[str]] = {}
    for _, identifier, where in collect_annotations(cfg):
        by_id.setdefault(identifier, []).append(where)
    return by_id


def check_traceability(cfg: Config, strict: bool = False) -> Tuple[List[str], List[str]]:
    """(erreurs, avertissements). En mode strict, l'absence de test est une erreur."""
    specs = parse_specs(cfg)
    rules = ontology_rules(cfg)
    errors = list(specs.errors)
    warnings: List[str] = []

    for identifier, rule in rules.items():
        if rule["count"] > 1:
            errors.append(f"{_rel(cfg, rule['file'])} : règle en double « {identifier} »")
        if identifier in specs.criteria or identifier in specs.requirements:
            errors.append(f"identifiant en double « {identifier} » (règle et spécification)")

    for identifier, requirement in specs.requirements.items():
        if not requirement["criteria"]:
            errors.append(f"{requirement['where']} : l'exigence « {identifier} » n'a aucun critère d'acceptation")

    for kind, identifier, where in collect_annotations(cfg):
        if kind == "spec" and identifier not in specs.criteria:
            if identifier in specs.requirements:
                errors.append(f"{where} : @spec cite l'exigence « {identifier} » ; citer un de ses critères")
            else:
                errors.append(f"{where} : @spec cite un critère inconnu « {identifier} »")
        if kind == "rule" and identifier not in rules:
            errors.append(f"{where} : @rule cite une règle inconnue « {identifier} »")

    tested = _tests_by_id(cfg)
    missing = [f"{c['where']} : critère sans test « {i} »" for i, c in specs.criteria.items() if i not in tested]
    missing += [
        f"{_rel(cfg, r['file'])} : règle testable sans test « {i} »"
        for i, r in rules.items()
        if r["testable"] and i not in tested
    ]
    (errors if strict else warnings).extend(missing)
    return errors, warnings


def _test_line(identifier: str, tested: Dict[str, List[str]]) -> str:
    places = tested.get(identifier)
    return f"- Test : ✅ {', '.join(places)}" if places else "- Test : ❌ aucun"


def _rewrite_spec(text: str, tested: Dict[str, List[str]]) -> str:
    lines = text.split("\n")
    criteria_ids = [CRITERION_HEADING.match(l).group(1) for _, l in _lines_outside_fences(text) if CRITERION_HEADING.match(l)]
    covered = sum(1 for i in criteria_ids if i in tested)
    coverage = f"{len(criteria_ids)} critères, {covered} testés, {len(criteria_ids) - covered} sans test."

    out: List[str] = []
    state = {"criterion": None, "has_test": False, "in_coverage": False, "coverage_done": False}

    def close_block():
        if state["criterion"] and not state["has_test"]:
            i = len(out)
            while i > 0 and out[i - 1].strip() == "":
                i -= 1
            out.insert(i, _test_line(state["criterion"], tested))
        if state["in_coverage"] and not state["coverage_done"]:
            out.extend([coverage, ""])
        state.update(criterion=None, has_test=False, in_coverage=False, coverage_done=False)

    in_fence = False
    for line in lines:
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        if line.startswith("#"):
            close_block()
            m = CRITERION_HEADING.match(line)
            state["criterion"] = m.group(1) if m else None
            state["in_coverage"] = line.strip() == "## Couverture"
            out.append(line)
            continue
        if state["in_coverage"] and line.strip() and not state["coverage_done"]:
            out.append(coverage)
            state["coverage_done"] = True
            continue
        if state["criterion"] and TEST_LINE.match(line):
            if not state["has_test"]:
                out.append(_test_line(state["criterion"], tested))
                state["has_test"] = True
            continue
        out.append(line)
    close_block()
    return "\n".join(out)


def write_test_lines(cfg: Config) -> List[Path]:
    """Régénère les lignes « Test » et la section « Couverture » des spécifications."""
    tested = _tests_by_id(cfg)
    changed = []
    for path in _markdown_files(cfg.specs_dir):
        text = path.read_text(encoding="utf-8")
        new = _rewrite_spec(text, tested)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed.append(path)
    return changed


# --------------------------------------------------------------------------- extrait

def _requirement_blocks(cfg: Config) -> Dict[str, List[str]]:
    """Texte de chaque exigence (titre, énoncé, critères), tel qu'écrit dans la spécification."""
    blocks: Dict[str, List[str]] = {}
    for path in _markdown_files(cfg.specs_dir):
        current: Optional[str] = None
        in_fence = False
        for line in path.read_text(encoding="utf-8").split("\n"):
            if line.lstrip().startswith(("```", "~~~")):
                in_fence = not in_fence
            elif not in_fence:
                m = REQUIREMENT_HEADING.match(line)
                if m:
                    current = m.group(1)
                    blocks[current] = []
                elif re.match(r"^#{1,3}\s", line):
                    current = None
            if current:
                blocks[current].append(line)
    for lines in blocks.values():
        while lines and not lines[-1].strip():
            lines.pop()
    return blocks


def touched_ids(change: Path) -> Tuple[List[str], List[str]]:
    """Identifiants listés dans la rubrique « Exigences touchées » de la proposition."""
    proposal = change / "proposal.md"
    if not proposal.exists():
        return [], [f"{change.name} : proposal.md manquant"]
    text = proposal.read_text(encoding="utf-8")
    if not any(l.strip() == "## Exigences touchées" for _, l in _lines_outside_fences(text)):
        return [], [f"{change.name}/proposal.md : rubrique « ## Exigences touchées » manquante"]
    ids: List[str] = []
    for line in _section(text, "Exigences touchées"):
        for identifier in re.findall(rf"(?<![\w.-])({ID})(?![\w.-])", line):
            if identifier not in ids:
                ids.append(identifier)
    return ids, []


def build_extract(cfg: Config, change: Path) -> Tuple[str, List[str]]:
    """(texte de l'extrait, erreurs) pour un changement."""
    change = Path(change).resolve()
    ids, errors = touched_ids(change)
    if errors:
        return "", errors
    blocks = _requirement_blocks(cfg)
    criteria = parse_specs(cfg).criteria
    rules = ontology_rules(cfg)
    parts = [EXTRACT_HEADER, "", f"# Extrait de spécification — {change.name}", "", "## Exigences", ""]
    cited: List[str] = []
    for identifier in ids:
        if identifier in blocks:
            parts.extend(blocks[identifier] + [""])
            for line in blocks[identifier]:
                for rule in RULE_CITATION.findall(line):
                    if rule not in cited:
                        cited.append(rule)
        elif identifier in criteria:
            errors.append(f"{change.name}/proposal.md : « {identifier} » est un critère ; lister son exigence")
        else:
            errors.append(f"{change.name}/proposal.md : exigence inconnue « {identifier} »")
    if not ids:
        parts.extend(["Aucune exigence touchée.", ""])
    parts.extend(["## Règles de l'ontologie appliquées", ""])
    for rule in cited:
        if rule in rules:
            parts.append(f"- `{rule}` : {rules[rule]['text']}")
        else:
            errors.append(f"règle citée inconnue « {rule} »")
    if not cited:
        parts.append("Aucune.")
    return "\n".join(parts) + "\n", errors


def ongoing_changes(cfg: Config) -> List[Path]:
    changes = cfg.doc / "changes"
    if not changes.is_dir():
        return []
    return sorted(d for d in changes.iterdir() if d.is_dir() and d.name != "archive")


def sync_extracts(cfg: Config) -> List[str]:
    """Régénère les extraits périmés. Renvoie les messages : fichiers écrits et erreurs."""
    messages = []
    for change in ongoing_changes(cfg):
        text, errors = build_extract(cfg, change)
        if errors:
            messages.extend(f"✗ {e}" for e in errors)
            continue
        target = change / EXTRACT_NAME
        if not target.exists() or target.read_text(encoding="utf-8") != text:
            target.write_text(text, encoding="utf-8")
            messages.append(f"régénéré : {_rel(cfg, target)}")
    return messages


# --------------------------------------------------------------------------- livraison

def check_release(cfg: Config, change: Path) -> List[str]:
    """Contrôles avant archivage d'un changement."""
    change = Path(change).resolve()
    errors, _ = check_traceability(cfg, strict=True)

    if not (change / "proposal.md").exists():
        errors.append(f"{_rel(cfg, change)} : proposal.md manquant")

    tasks = change / "tasks.md"
    if not tasks.exists():
        errors.append(f"{_rel(cfg, change)} : tasks.md manquant")
    else:
        text = tasks.read_text(encoding="utf-8")
        for number, line in _lines_outside_fences(text):
            if UNCHECKED_TASK.match(line):
                errors.append(f"{_rel(cfg, tasks)}:{number} : tâche non cochée")
        rows = [r for r in _table_rows(_section(text, "Bilan")) if r and r[0] and not r[0].startswith("<")]
        if not rows:
            errors.append(f"{_rel(cfg, tasks)} : bilan vide")

    review = change / "review.md"
    if not review.exists():
        errors.append(f"{_rel(cfg, change)} : review.md manquant (verdict du juge)")
    else:
        verdicts = VERDICT.findall(review.read_text(encoding="utf-8"))
        if not verdicts or verdicts[-1].lower() != "accepté":
            errors.append(f"{_rel(cfg, review)} : dernier verdict du juge non « Accepté »")

    for path in _markdown_files(cfg.specs_dir) + _markdown_files(cfg.ontology_dir) + _markdown_files(change):
        for number, line in _lines_outside_fences(path.read_text(encoding="utf-8")):
            if CLARIFY.search(line):
                errors.append(f"{_rel(cfg, path)}:{number} : point « À clarifier » non tranché")

    for path in _markdown_files(cfg.specs_dir):
        for line in _section(path.read_text(encoding="utf-8"), "Hypothèses"):
            item = re.sub(r"^\s*[-*]\s*", "", line).strip()
            if line.strip().startswith(("-", "*")) and item:
                errors.append(f"{_rel(cfg, path)} : hypothèse non validée « {item} »")
    return errors


def archive_change(cfg: Config, change: Path, today: Optional[str] = None) -> Path:
    change = Path(change).resolve()
    today = today or datetime.date.today().isoformat()
    target = cfg.archive_dir / f"{today}-{change.name}"
    if target.exists():
        raise FileExistsError(f"{_rel(cfg, target)} existe déjà")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(change), str(target))
    return target


# --------------------------------------------------------------------------- CLI

def _report(title: str, errors: List[str], warnings: List[str] = ()) -> bool:
    for w in warnings:
        print(f"  ! {w}")
    for e in errors:
        print(f"  ✗ {e}")
    status = "OK" if not errors else f"{len(errors)} erreur(s)"
    extra = f", {len(warnings)} avertissement(s)" if warnings else ""
    print(f"[{title}] {status}{extra}")
    return not errors


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Contrôles communs de la boîte à outils.")
    parser.add_argument("--root", default=".", help="racine du projet (défaut : dossier courant)")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("vocabulary", help="aucun mot refusé dans le dépôt")
    t = sub.add_parser("traceability", help="lien critères / règles / tests")
    t.add_argument("--strict", action="store_true", help="un critère ou une règle sans test bloque")
    t.add_argument("--write", action="store_true", help="régénère les lignes « Test » et la couverture")
    sub.add_parser("extract", help="génère l'extrait de spécification des changements en cours")
    sub.add_parser("commit", help="contrôles avant commit")
    r = sub.add_parser("release", help="contrôles avant archivage d'un changement")
    r.add_argument("change", help="dossier du changement (doc/changes/<nom>)")
    r.add_argument("--archive", action="store_true", help="archive le changement si tout passe")
    args = parser.parse_args(argv)
    cfg = load_config(Path(args.root))

    if args.command == "vocabulary":
        return 0 if _report("Vocabulaire", check_vocabulary(cfg)) else 1

    if args.command == "traceability":
        if args.write:
            for path in write_test_lines(cfg):
                print(f"  mis à jour : {_rel(cfg, path)}")
        errors, warnings = check_traceability(cfg, strict=args.strict)
        return 0 if _report("Traçabilité", errors, warnings) else 1

    if args.command == "extract":
        messages = sync_extracts(cfg)
        for m in messages:
            print(f"  {m}")
        errors = [m for m in messages if m.startswith("✗")]
        print(f"[Extraits] {'OK' if not errors else f'{len(errors)} erreur(s)'}")
        return 0 if not errors else 1

    if args.command == "commit":
        ok = _report("Vocabulaire", check_vocabulary(cfg))
        errors, warnings = check_traceability(cfg)
        ok = _report("Traçabilité", errors, warnings) and ok
        messages = sync_extracts(cfg)
        extract_errors = [m[2:] for m in messages if m.startswith("✗")]
        extract_errors += [
            f"{m} — ajoutez-le au commit (git add) puis recommitez"
            for m in messages if not m.startswith("✗")
        ]
        ok = _report("Extraits", extract_errors) and ok
        for command in cfg.commit_commands:
            print(f"[Projet] {command}")
            if subprocess.run(command, shell=True, cwd=cfg.root).returncode != 0:
                print(f"  ✗ échec : {command}")
                ok = False
        return 0 if ok else 1

    if args.command == "release":
        change = Path(args.change)
        if not change.is_absolute():
            change = cfg.root / change
        if not change.is_dir():
            print(f"  ✗ dossier introuvable : {args.change}")
            return 1
        ok = _report("Livraison", check_release(cfg, change))
        if ok and args.archive:
            print(f"  archivé : {_rel(cfg, archive_change(cfg, change))}")
        return 0 if ok else 1
    return 1


if __name__ == "__main__":
    sys.exit(main())

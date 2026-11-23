"""Tests des contrôles communs. Lancer : python3 -m unittest discover tools/toolbox-checks/tests"""
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import toolbox_checks as tc  # noqa: E402

ONTOLOGY = """\
# Ontologie — Démo

## Concepts

| Mot | Code | Définition |
|---|---|---|
| Bidule | `Bidule` | Une chose. Autrefois « zorglub ». Règles : `bidule.jamais-vide`. |

## Règles

| Identifiant | Règle | Testable |
|---|---|---|
| `bidule.jamais-vide` | Un bidule n'est jamais vide. | Oui |
| `bidule.esthetique` | Un bidule est joli. | Non (subjectif) |

## Mots refusés

| Mot refusé | Mot retenu |
|---|---|
| Zorglub | Bidule |
| truc machin | Bidule |
"""

SPEC = """\
# Spécification — Bidules

## Couverture
à générer

## Exigences

### bidules.creer
Quand l'utilisateur crée un Bidule, le système doit l'enregistrer.

#### Critères d'acceptation

##### bidules.creer.nominal
- Étant donné rien
- Quand l'utilisateur crée un Bidule
- Alors il existe
- Test : ancien contenu

##### bidules.creer.erreur
- Étant donné un nom vide
- Quand l'utilisateur crée un Bidule
- Alors le système refuse

## Hypothèses
-

## Hors périmètre
-
"""


class Project:
    """Projet temporaire construit fichier par fichier."""

    def __init__(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve()

    def write(self, rel, content):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(content), encoding="utf-8")
        return path

    def config(self):
        return tc.load_config(self.root)

    def close(self):
        self._tmp.cleanup()


class Base(unittest.TestCase):
    def setUp(self):
        self.p = Project()
        self.p.write("doc/ontology/ontology.md", ONTOLOGY)
        self.p.write("doc/specs/bidules.md", SPEC)

    def tearDown(self):
        self.p.close()


class VocabularyTest(Base):
    def test_clean_project_passes(self):
        self.p.write("src/app.py", "def create_bidule():\n    pass\n")
        self.assertEqual(tc.check_vocabulary(self.p.config()), [])

    def test_refused_word_in_code_is_found(self):
        self.p.write("src/app.py", "x = 1\nlabel = 'Zorglub'\n")
        hits = tc.check_vocabulary(self.p.config())
        self.assertEqual(len(hits), 1)
        self.assertIn("src/app.py:2", hits[0])

    def test_refused_word_inside_identifier_is_found(self):
        self.p.write("src/app.ts", "class ZorglubService {}\nconst zorglub_id = 1\n")
        self.assertEqual(len(tc.check_vocabulary(self.p.config())), 2)

    def test_refused_phrase_is_found(self):
        self.p.write("README.md", "Le Truc Machin est obsolète.\n")
        self.assertEqual(len(tc.check_vocabulary(self.p.config())), 1)

    def test_word_containing_refused_word_is_not_found(self):
        self.p.write("src/app.py", "zorglubesque = 1\n")
        self.assertEqual(tc.check_vocabulary(self.p.config()), [])

    def test_ontology_refused_table_and_autrefois_are_exempt(self):
        self.assertEqual(tc.check_vocabulary(self.p.config()), [])

    def test_archive_is_exempt(self):
        self.p.write("doc/changes/archive/2026-01-01-x/proposal.md", "Zorglub devient Bidule.\n")
        self.assertEqual(tc.check_vocabulary(self.p.config()), [])

    def test_ongoing_change_is_checked(self):
        self.p.write("doc/changes/x/proposal.md", "Zorglub reste.\n")
        self.assertEqual(len(tc.check_vocabulary(self.p.config())), 1)

    def test_excluded_dirs_are_skipped(self):
        self.p.write("node_modules/lib/index.js", "Zorglub\n")
        self.assertEqual(tc.check_vocabulary(self.p.config()), [])


class TraceabilityTest(Base):
    def test_unknown_spec_id_in_test_is_error(self):
        self.p.write("tests/test_a.py", "# @spec bidules.inconnu.cas\n")
        errors, _ = tc.check_traceability(self.p.config())
        self.assertTrue(any("bidules.inconnu.cas" in e for e in errors))

    def test_requirement_id_cited_instead_of_criterion_is_error(self):
        self.p.write("tests/test_a.py", "# @spec bidules.creer\n")
        errors, _ = tc.check_traceability(self.p.config())
        self.assertTrue(any("exigence" in e for e in errors))

    def test_unknown_rule_id_is_error(self):
        self.p.write("tests/test_a.py", "# @rule bidule.inexistante\n")
        errors, _ = tc.check_traceability(self.p.config())
        self.assertTrue(any("bidule.inexistante" in e for e in errors))

    def test_requirement_without_criterion_is_error(self):
        self.p.write("doc/specs/autre.md", "# Spécification — Autre\n\n### autre.seule\nLe système doit exister.\n")
        errors, _ = tc.check_traceability(self.p.config())
        self.assertTrue(any("autre.seule" in e for e in errors))

    def test_duplicate_id_is_error(self):
        self.p.write("doc/specs/autre.md", "### bidules.creer\nX\n\n##### bidules.creer.autre\n- a\n")
        errors, _ = tc.check_traceability(self.p.config())
        self.assertTrue(any("en double" in e for e in errors))

    def test_untested_items_are_warnings_by_default(self):
        errors, warnings = tc.check_traceability(self.p.config())
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 3)  # 2 critères + 1 règle testable

    def test_untested_items_are_errors_when_strict(self):
        errors, _ = tc.check_traceability(self.p.config(), strict=True)
        self.assertEqual(len(errors), 3)

    def test_non_testable_rule_is_not_required(self):
        self.p.write(
            "tests/test_a.py",
            "# @spec bidules.creer.nominal\n# @spec bidules.creer.erreur\n# @rule bidule.jamais-vide\n",
        )
        errors, warnings = tc.check_traceability(self.p.config(), strict=True)
        self.assertEqual((errors, warnings), ([], []))

    def test_spec_examples_in_code_fences_are_ignored(self):
        self.p.write("doc/specs/guide.md", "```\n### faux.exemple\n```\n")
        errors, _ = tc.check_traceability(self.p.config())
        self.assertEqual(errors, [])


class WriteTest(Base):
    def test_write_generates_test_lines_and_coverage(self):
        self.p.write("tests/test_a.py", "x = 1\n# @spec bidules.creer.nominal\n")
        tc.write_test_lines(self.p.config())
        text = (self.p.root / "doc/specs/bidules.md").read_text(encoding="utf-8")
        self.assertIn("- Test : ✅ tests/test_a.py:2", text)
        self.assertIn("- Test : ❌ aucun", text)
        self.assertNotIn("ancien contenu", text)
        self.assertIn("2 critères, 1 testés, 1 sans test.", text)
        self.assertNotIn("à générer", text)

    def test_write_is_idempotent(self):
        self.p.write("tests/test_a.py", "# @spec bidules.creer.nominal\n")
        tc.write_test_lines(self.p.config())
        first = (self.p.root / "doc/specs/bidules.md").read_text(encoding="utf-8")
        tc.write_test_lines(self.p.config())
        second = (self.p.root / "doc/specs/bidules.md").read_text(encoding="utf-8")
        self.assertEqual(first, second)
        self.assertEqual(second.count("- Test :"), 2)


class ReleaseTest(Base):
    def _change(self, tasks):
        self.p.write("doc/changes/demo/proposal.md", "# Changement — demo\n")
        self.p.write("doc/changes/demo/tasks.md", tasks)
        self.p.write(
            "tests/test_a.py",
            "# @spec bidules.creer.nominal\n# @spec bidules.creer.erreur\n# @rule bidule.jamais-vide\n",
        )
        return self.p.root / "doc/changes/demo"

    DONE = (
        "# Tâches — demo\n\n## Tâches\n- [x] Fait\n\n## Bilan\n\n"
        "| Exigence / critère / règle | État | Prouvé par |\n|---|---|---|\n"
        "| bidules.creer.nominal | ✅ fait | tests/test_a.py |\n"
    )

    def test_complete_change_passes(self):
        change = self._change(self.DONE)
        self.assertEqual(tc.check_release(self.p.config(), change), [])

    def test_unchecked_task_blocks(self):
        change = self._change(self.DONE.replace("- [x] Fait", "- [ ] Pas fait"))
        self.assertTrue(any("non cochée" in e for e in tc.check_release(self.p.config(), change)))

    def test_empty_bilan_blocks(self):
        change = self._change("# Tâches\n\n## Tâches\n- [x] Fait\n\n## Bilan\n\n| A | B | C |\n|---|---|---|\n| | | |\n")
        self.assertTrue(any("bilan" in e.lower() for e in tc.check_release(self.p.config(), change)))

    def test_clarification_marker_blocks(self):
        change = self._change(self.DONE)
        spec = self.p.root / "doc/specs/bidules.md"
        spec.write_text(spec.read_text(encoding="utf-8") + "\n⚠ À clarifier : quelle couleur ?\n", encoding="utf-8")
        self.assertTrue(any("clarifier" in e for e in tc.check_release(self.p.config(), change)))

    def test_hypothesis_blocks(self):
        change = self._change(self.DONE)
        spec = self.p.root / "doc/specs/bidules.md"
        spec.write_text(spec.read_text(encoding="utf-8").replace("## Hypothèses\n-", "## Hypothèses\n- Les bidules sont bleus."), encoding="utf-8")
        self.assertTrue(any("ypothèse" in e for e in tc.check_release(self.p.config(), change)))

    def test_untested_criterion_blocks(self):
        change = self._change(self.DONE)
        self.p.write("tests/test_a.py", "# @spec bidules.creer.nominal\n")
        self.assertTrue(tc.check_release(self.p.config(), change))

    def test_missing_proposal_blocks(self):
        change = self._change(self.DONE)
        (change / "proposal.md").unlink()
        self.assertTrue(any("proposal.md" in e for e in tc.check_release(self.p.config(), change)))

    def test_archive_moves_change_with_date(self):
        change = self._change(self.DONE)
        target = tc.archive_change(self.p.config(), change, today="2026-11-23")
        self.assertFalse(change.exists())
        self.assertEqual(target.name, "2026-11-23-demo")
        self.assertTrue((target / "tasks.md").exists())


class SelfExclusionTest(Base):
    def test_tool_directory_is_never_scanned(self):
        tool = self.p.root / "tools" / "toolbox-checks"
        self.p.write("tools/toolbox-checks/README.md", "Zorglub\n# @spec bidules.inconnu.cas\n")
        cfg = self.p.config()
        cfg.tool_dir = tool
        self.assertEqual(tc.check_vocabulary(cfg), [])
        errors, _ = tc.check_traceability(cfg)
        self.assertEqual(errors, [])


class EdgeCaseTest(Base):
    def test_binary_and_excluded_glob_files_are_skipped(self):
        (self.p.root / "img.bin").write_bytes(b"Zorglub\0\0")
        self.p.write("toolbox-checks.json", '{"exclude_globs": ["generated/*"]}')
        self.p.write("generated/x.py", "Zorglub\n")
        self.assertEqual(tc.check_vocabulary(self.p.config()), [])

    def test_non_utf8_file_is_skipped(self):
        (self.p.root / "latin.txt").write_bytes("Zorglub é".encode("latin-1"))
        self.assertEqual(tc.check_vocabulary(self.p.config()), [])

    def test_no_refused_words_means_no_hit(self):
        self.p.write("doc/ontology/ontology.md", "# Ontologie\n")
        self.p.write("src/a.py", "Zorglub\n")
        self.assertEqual(tc.check_vocabulary(self.p.config()), [])

    def test_test_paths_limit_annotation_scan(self):
        self.p.write("toolbox-checks.json", '{"test_paths": ["tests", "missing", "one_test.py"]}')
        self.p.write("src/a.py", "# @spec bidules.inconnu.cas\n")
        self.p.write("one_test.py", "# @spec bidules.creer.nominal\n")
        errors, warnings = tc.check_traceability(self.p.config())
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 2)

    def test_duplicate_rule_and_rule_spec_collision_are_errors(self):
        self.p.write(
            "doc/ontology/autre.md",
            "## Règles\n\n| Identifiant | Règle | Testable |\n|---|---|---|\n"
            "| `bidule.jamais-vide` | doublon | Oui |\n| `bidules.creer` | collision | Oui |\n",
        )
        errors, _ = tc.check_traceability(self.p.config())
        self.assertTrue(any("règle en double" in e for e in errors))
        self.assertTrue(any("règle et spécification" in e for e in errors))

    def test_criterion_outside_requirement_is_tolerated(self):
        self.p.write("doc/specs/libre.md", "## Divers\n\n##### libre.seul.cas\n- a\n")
        errors, _ = tc.check_traceability(self.p.config())
        self.assertEqual(errors, [])

    def test_empty_coverage_section_is_filled(self):
        self.p.write("doc/specs/vide.md", "# S\n\n## Couverture\n\n## Exigences\n\n### vide.x\nX\n\n##### vide.x.cas\n- a\n```\n##### faux.cas\n```\n")
        tc.write_test_lines(self.p.config())
        text = (self.p.root / "doc/specs/vide.md").read_text(encoding="utf-8")
        self.assertIn("1 critères, 0 testés, 1 sans test.", text)
        self.assertEqual(text.count("- Test :"), 1)

    def test_archive_refuses_existing_target(self):
        change = self.p.root / "doc/changes/demo"
        change.mkdir(parents=True)
        (self.p.root / "doc/changes/archive/2026-11-23-demo").mkdir(parents=True)
        with self.assertRaises(FileExistsError):
            tc.archive_change(self.p.config(), change, today="2026-11-23")

    def test_missing_tasks_blocks_release(self):
        change = self.p.root / "doc/changes/demo"
        change.mkdir(parents=True)
        (change / "proposal.md").write_text("# P\n", encoding="utf-8")
        self.assertTrue(any("tasks.md manquant" in e for e in tc.check_release(self.p.config(), change)))


class CliTest(Base):
    def run_cli(self, *args):
        import contextlib
        import io

        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = tc.main(["--root", str(self.p.root), *args])
        return code, out.getvalue()

    def _complete_tests(self):
        self.p.write(
            "tests/test_a.py",
            "# @spec bidules.creer.nominal\n# @spec bidules.creer.erreur\n# @rule bidule.jamais-vide\n",
        )

    def test_vocabulary_command(self):
        self.assertEqual(self.run_cli("vocabulary")[0], 0)
        self.p.write("src/a.py", "Zorglub\n")
        code, out = self.run_cli("vocabulary")
        self.assertEqual(code, 1)
        self.assertIn("✗", out)

    def test_traceability_command_writes_and_reports(self):
        code, out = self.run_cli("traceability", "--write")
        self.assertEqual(code, 0)
        self.assertIn("mis à jour", out)
        self.assertIn("avertissement", out)
        self.assertEqual(self.run_cli("traceability", "--strict")[0], 1)

    def test_commit_command_runs_project_commands(self):
        self._complete_tests()
        self.p.write("toolbox-checks.json", '{"commit_commands": ["true"]}')
        self.assertEqual(self.run_cli("commit")[0], 0)
        self.p.write("toolbox-checks.json", '{"commit_commands": ["false"]}')
        code, out = self.run_cli("commit")
        self.assertEqual(code, 1)
        self.assertIn("échec", out)

    def test_release_command_archives(self):
        self._complete_tests()
        self.p.write("doc/changes/demo/proposal.md", "# P\n")
        self.p.write("doc/changes/demo/tasks.md", ReleaseTest.DONE)
        code, out = self.run_cli("release", "doc/changes/demo", "--archive")
        self.assertEqual(code, 0, out)
        self.assertIn("archivé", out)
        self.assertFalse((self.p.root / "doc/changes/demo").exists())

    def test_release_command_on_missing_dir(self):
        code, out = self.run_cli("release", "doc/changes/absent")
        self.assertEqual(code, 1)
        self.assertIn("introuvable", out)


class ConfigTest(unittest.TestCase):
    def test_config_file_overrides_defaults(self):
        p = Project()
        try:
            p.write("toolbox-checks.json", '{"doc_dir": "docs", "exclude_dirs": ["generated"], "test_paths": ["spec"]}')
            cfg = p.config()
            self.assertEqual(cfg.doc, p.root / "docs")
            self.assertIn("generated", cfg.exclude_dirs)
            self.assertEqual(cfg.test_paths, [p.root / "spec"])
        finally:
            p.close()


if __name__ == "__main__":
    unittest.main()

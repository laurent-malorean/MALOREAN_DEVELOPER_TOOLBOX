# toolbox-checks

Contrôles communs, **indépendants de la stack** du projet, qui implémentent ceux décrits dans [development-workflow.md](../../developer/driven-development/development-workflow.md). Ils ne lisent que du Markdown (`doc/`) et des annotations dans les fichiers de test.

Prérequis : Python 3.9 ou plus, aucune dépendance.

## Ce qui est contrôlé

| Commande | Contrôle | Bloque |
|---|---|---|
| `vocabulary` | Aucun mot refusé de l'ontologie dans le dépôt (y compris dans les noms : `ContactService`, `contact_id`). Exemptés : `doc/changes/archive/`, les `proposal.md` des changements (ils expliquent les renommages), les `spec-extract.md` générés, et dans l'ontologie la table « Mots refusés » et les lignes contenant « Autrefois ». | Oui |
| `traceability` | Identifiants en double ; exigence sans critère ; test qui cite un identifiant inconnu ou une exigence au lieu d'un critère. Critères et règles testables sans test : avertissement. | Oui (sauf avertissements) |
| `traceability --strict` | Idem, et tout critère ou règle testable sans test bloque. | Oui |
| `traceability --write` | Régénère la ligne « Test » sous chaque critère et la section « Couverture » des fiches. | — |
| `extract` | Génère `spec-extract.md` dans chaque changement en cours, à partir des « Exigences touchées » de sa proposition : exigences, critères, règles de l'ontologie citées. | Oui (identifiant inconnu, rubrique absente) |
| `commit` | `vocabulary` + `traceability` ; régénère les lignes « Test » des spécifications et les extraits (un fichier régénéré bloque : l'ajouter au commit) ; puis les `commit_commands` du projet. | Oui |
| `release <dossier>` | Limité aux exigences touchées du changement : chaque critère et chaque règle citée testable a un test ; chaque critère figure au bilan de `tasks.md` ; `proposal.md`, `tasks.md` et `review.md` présents ; dernier verdict du juge « Accepté » ; aucune tâche ni vérification manuelle de `test-plan.md` non cochée ; aucun « À clarifier : » dans les exigences touchées ni dans le dossier ; aucune hypothèse restante dans leurs fiches. Un autre changement en cours ne bloque pas. | Oui |
| `release <dossier> --archive` | Idem, puis déplace le dossier vers `doc/changes/archive/AAAA-MM-JJ-<nom>/`. | Oui |

Ce qui reste **au projet**, car dépendant de la stack : la commande de tests, la couverture (lignes, branches) et le test de mutation avec les seuils du flux commun. On les branche via `commit_commands` et la CI.

## Installer dans un projet

1. Copier ce dossier entier dans le projet, sous `tools/toolbox-checks/`. L'outil n'analyse jamais son propre dossier : ses exemples et ses tests ne déclenchent aucun contrôle dans le projet.
2. Activer le hook :
   ```sh
   chmod +x tools/toolbox-checks/pre-commit
   git config core.hooksPath tools/toolbox-checks
   ```
3. Optionnel : créer `toolbox-checks.json` à la racine du projet.
4. En CI : lancer `python3 tools/toolbox-checks/toolbox_checks.py commit`, et `release` avant l'intégration d'un changement.

## Configuration : `toolbox-checks.json`

Tout est optionnel.

```json
{
  "doc_dir": "doc",
  "test_paths": ["tests"],
  "exclude_dirs": ["generated"],
  "exclude_globs": ["*.min.js", "public/legacy/*"],
  "commit_commands": [
    "npm test -- --coverage"
  ]
}
```

| Clé | Rôle | Défaut |
|---|---|---|
| `doc_dir` | Dossier de documentation | `doc` |
| `test_paths` | Où chercher les annotations `@spec` / `@rule` | tout le dépôt hors `doc/` |
| `exclude_dirs` | Dossiers ignorés, en plus de `.git`, `node_modules`, `vendor`, `dist`, `build`, `target`, `.venv`, `venv`, `coverage`… | — |
| `exclude_globs` | Fichiers ignorés (chemin relatif à la racine) | — |
| `commit_commands` | Commandes du projet lancées par `commit` (tests, couverture, lint) | aucune |

## Annoter un test

Un commentaire, dans la syntaxe du langage, n'importe où dans le fichier de test — idéalement juste au-dessus du test :

```python
# @spec facturation.refuser-modification-validee.ligne
def test_validated_invoice_refuses_line_edit(): ...
```

```ts
// @rule facture.validee-non-modifiable
it("refuses any edit on a validated invoice", () => { ... });
```

```php
/** @spec facturation.creer-facture.nominal */
public function testCreatesDraftInvoice(): void { ... }
```

- `@spec` cite un **critère d'acceptation** (`##### <id>` dans `doc/specs/`).
- `@rule` cite une **règle** de l'ontologie (table « Règles »).
- Un test peut porter plusieurs annotations.

## Formats lus

- Ontologie (`doc/ontology/*.md`) : tables des sections `## Règles` (identifiant, règle, testable « Oui » / « Non… ») et `## Mots refusés` (mot refusé, mot retenu).
- Spécifications (`doc/specs/*.md`) : exigences en `### <id>`, critères en `##### <id>`, section `## Couverture`, section `## Hypothèses`. Les blocs de code sont ignorés.
- Changement (`doc/changes/<nom>/`, modèles dans `tools/templates/change/`) : `proposal.md` avec une rubrique `## Exigences touchées` (identifiants d'exigences), `tasks.md` avec cases `- [ ]` / `- [x]` et une section `## Bilan` en tableau, `review.md` avec des lignes `Verdict : Accepté` / `Verdict : À reprendre` seules sur leur ligne (la dernière compte), `test-plan.md` avec ses cases. Les dossiers dont le nom commence par `_` (comme `_templates`) ne sont pas des changements.

Formats détaillés : [spec-driven-development.md](../../developer/driven-development/spec-driven-development.md) et [ontology-driven-development.md](../../developer/driven-development/ontology-driven-development.md).

## Développer ces contrôles

```sh
python3 -m unittest discover tools/toolbox-checks/tests
```

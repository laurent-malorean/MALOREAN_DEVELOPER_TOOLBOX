# MALOREAN_DEVELOPER_TOOLBOX

Boîte à outils pour développer mes projets : architecture, bonnes pratiques (dev et design) et constantes réutilisables. Pas d'application ici, uniquement des fiches Markdown que les projets consultent et appliquent.

## Contenu

| Dossier | Contenu |
|---|---|
| `developer/driven-development/` | Flux de développement, méthodes par l'ontologie et par la spécification |
| `developer/security/` | Sécurité (gestion des dépendances) |
| `developer/ai-agent/` | Règles de travail de l'agent IA ; équipe d'agents séquentielle (architecte, QA, designer, développeur, juge) |
| `developer/archi/` | Architecture |
| `design/ux-ui/` | Lois et principes UX/UI |
| `tools/agents/` | Définitions des agents de l'équipe, prêtes à copier dans `.claude/agents/` |
| `tools/toolbox-checks/` | Contrôles communs prêts à copier dans un projet (vocabulaire, traçabilité, livraison), indépendants de la stack |

## Spécifications

Chaque projet décrit ce que le système doit faire dans une **spécification** écrite de façon à ce que rien ne reste implicite — ni pour un développeur, ni pour une IA. Méthode complète : [spec-driven-development.md](developer/driven-development/spec-driven-development.md).

### Où elles vivent dans un projet

```
doc/
  ontology/ontology.md                ce que SONT les choses (concepts, mots, règles)
  specs/<fonction>.md                 ce que FAIT le système, une fiche par grande fonction
  changes/<nom>/                      changement en cours : proposition, tâches, bilan
  changes/archive/AAAA-MM-JJ-<nom>/   changements livrés
```

La spécification décrit toujours l'état actuel du produit : on la met à jour directement à chaque changement, git garde l'historique.

### Comment une fiche est écrite

- **Exigences** : une seule obligation chacune, sous une forme fixe — « Quand …, le système doit … », « Si …, alors le système doit … », « Tant que … ».
- **Critères d'acceptation** : au moins un par exigence, en « Étant donné / Quand / Alors », couvrant cas nominal, cas limites et erreurs.
- **Identifiants** stables fondés sur un nom court (`facturation.refuser-modification-validee.ligne`), jamais réutilisés ; chaque test porte l'identifiant de ce qu'il prouve.
- **Ligne « Test »** sous chaque critère, générée automatiquement : on voit ce qui est prouvé et ce qui ne l'est pas.
- **Règles métier** : jamais recopiées — l'exigence cite la règle de l'ontologie et décrit seulement la réaction visible du système.
- **« ⚠ À clarifier »** : bloque le codage de l'élément concerné tant que la question n'est pas tranchée.
- **Hypothèses** (à valider avant livraison), **hors périmètre**, **critères de succès** mesurables.

### Exemple

```markdown
### facturation.refuser-modification-validee
Règle appliquée : ontologie › facture.validee-non-modifiable

Si l'utilisateur tente de modifier une facture validée, alors le système
doit refuser et proposer de créer un Avoir.

#### Critères d'acceptation

##### facturation.refuser-modification-validee.ligne
- Étant donné une facture validée
- Quand l'utilisateur modifie une ligne
- Alors la modification est refusée
- Et le système affiche « Facture validée : créez un avoir »
- Test : ✅ tests/invoice_test.py:31
```

### Comment elles servent au développement

Les critères d'acceptation sont la liste des tests à écrire en TDD, avant le code. Un changement n'est livré que si chaque critère a son test, que rien ne reste « à clarifier » et que la couverture atteint les seuils (90 % lignes et branches sur le code métier, 80 % de mutants détectés). Ordre de travail et contrôles : [development-workflow.md](developer/driven-development/development-workflow.md). Les contrôles sont fournis, prêts à copier : [tools/toolbox-checks](tools/toolbox-checks/README.md).

Inspirations : OpenSpec, Spec Kit, Kiro (notation EARS), et la critique de Birgitta Böckeler sur martinfowler.com.

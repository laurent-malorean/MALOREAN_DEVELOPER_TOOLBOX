# MALOREAN_DEVELOPER_TOOLBOX

Boîte à outils centrale pour développer mes projets. Ce repo ne contient pas d'application : c'est une base de connaissances (Markdown) que les autres projets consultent et réutilisent.

## Rôle de ce repo

Ce repo définit les bonnes pratiques ; les projets de développement les appliquent. Chaque projet a sa propre stack.

- **Ici** : le *quoi* et le *pourquoi* (méthodes, formats, règles, seuils), et les **contrôles communs** quand ils ne dépendent pas de la stack (`tools/toolbox-checks/` : ils ne lisent que du Markdown et des annotations de test). Ils sont écrits une seule fois, testés, et copiés tels quels dans les projets.
- **Dans chaque projet** : uniquement ce qui dépend de sa stack (commande de tests, couverture, test de mutation, CI), avec les seuils fixés ici.
- Avant de renvoyer une implémentation aux projets, vérifier si elle dépend vraiment de la stack ; sinon, elle appartient à ce repo.
- Rédiger chaque fiche pour qu'un projet puisse l'appliquer sans autre contexte : règles explicites, seuils chiffrés, modèles à copier.

## Utiliser ce repo dans un projet

- Le `CLAUDE.md` du projet renvoie vers les fiches à appliquer (au minimum `developer/driven-development/development-workflow.md` et `developer/ai-agent/agent-practices.md`) et décrit comment il implémente la partie propre à sa stack.
- Le projet copie `tools/toolbox-checks/` et active son hook (voir son README).

## Contenu

- **Architecture** — patterns, structures de projet, choix techniques de référence.
- **Bonnes pratiques**
  - **Dev** — conventions de code, tests, revue, outillage.
  - **Design** — lois UX/UI, principes d'interface, accessibilité.
- **Constantes** — valeurs réutilisables telles quelles d'un projet à l'autre (ex. palettes de couleurs, typographies, espacements, breakpoints).

## Organisation

```
developer/
  archi/              Architecture
  driven-development/ Flux de développement et méthodes « pilotées par » (ontologie, spécification)
  security/           Sécurité (ex. dependencies.md)
  ai-agent/           Comportement de l'agent IA sur un projet (agent-practices.md)
  ...                 Bonnes pratiques dev
design/
  ux-ui/          Bonnes pratiques design (ex. law-of-ui.md)
tools/
  toolbox-checks/ Contrôles communs indépendants de la stack (Python 3.9+, sans dépendance), avec leurs tests
constants/        Constantes (palettes, tokens…) — à créer au besoin
```

Ajouter un nouveau thème dans le dossier qui correspond à sa catégorie ; créer un sous-dossier quand un thème regroupe plusieurs fichiers.

## Conventions communes à mes projets

- `doc/` : documentation du produit développé.
  - `doc/ontology/ontology.md` : ontologie (ce que sont les choses) ; fichiers par domaine à côté.
  - `doc/specs/<fonction>.md` : spécification de référence (ce que fait le système).
  - `doc/changes/<nom>/` : changement en cours (proposition, tâches, bilan) ; `doc/changes/archive/` une fois livré.
- Les projets suivent un flux unique, en TDD, avec seuils de couverture et contrôles : `developer/driven-development/development-workflow.md`. Il s'appuie sur :
  - `developer/driven-development/ontology-driven-development.md` (contenu de l'ontologie, règles du vocabulaire) ;
  - `developer/driven-development/spec-driven-development.md` (format des spécifications, des changements et des identifiants).
- Toute bibliothèque ajoutée est vérifiée (maintenance, sécurité, licence, dépendances indirectes) avant l'ajout, puis surveillée en continu : voir `developer/security/dependencies.md`.

## Conventions de rédaction

- Documents en français, en Markdown.
- En-tête YAML en tête de fichier quand le document vient d'une source externe : `source`, `date_analyse`, `type`, puis les métadonnées utiles (catégories, nombre d'éléments…).
- Un fichier = un sujet. Titres hiérarchisés (`##`, `###`) pour rester lisible et indexable.
- Contenu actionnable : énoncé, principe, exemples, bonnes pratiques, erreurs à éviter.
- Constantes : stockées dans un format directement réutilisable (Markdown avec valeurs exactes, et si utile JSON/CSS à côté).

## Fichiers privés

- `CLAUDE.local.md` et `_SECRET/` sont ignorés par git : ne jamais en copier le contenu ailleurs ni le committer.

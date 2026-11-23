# MALOREAN_DEVELOPER_TOOLBOX

Boîte à outils centrale pour développer mes projets. Ce repo ne contient pas d'application : c'est une base de connaissances (Markdown) que les autres projets consultent et réutilisent.

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
  driven-development/ Méthodes « pilotées par » (ex. ontology-driven-development.md)
  security/           Sécurité (ex. dependencies.md)
  ...                 Bonnes pratiques dev
design/
  ux-ui/          Bonnes pratiques design (ex. law-of-ui.md)
constants/        Constantes (palettes, tokens…) — à créer au besoin
```

Ajouter un nouveau thème dans le dossier qui correspond à sa catégorie ; créer un sous-dossier quand un thème regroupe plusieurs fichiers.

## Conventions communes à mes projets

- `doc/` : documentation du produit développé.
- `doc/ontology/ontology.md` : point d'entrée de l'ontologie du projet ; les fichiers par domaine se rangent à côté dans `doc/ontology/`.
- Les projets suivent le développement guidé par l'ontologie : voir `developer/driven-development/ontology-driven-development.md`.
- Toute bibliothèque ajoutée est vérifiée (maintenance, sécurité, licence, dépendances indirectes) avant l'ajout, puis surveillée en continu : voir `developer/security/dependencies.md`.

## Conventions de rédaction

- Documents en français, en Markdown.
- En-tête YAML en tête de fichier quand le document vient d'une source externe : `source`, `date_analyse`, `type`, puis les métadonnées utiles (catégories, nombre d'éléments…).
- Un fichier = un sujet. Titres hiérarchisés (`##`, `###`) pour rester lisible et indexable.
- Contenu actionnable : énoncé, principe, exemples, bonnes pratiques, erreurs à éviter.
- Constantes : stockées dans un format directement réutilisable (Markdown avec valeurs exactes, et si utile JSON/CSS à côté).

## Fichiers privés

- `CLAUDE.local.md` et `_SECRET/` sont ignorés par git : ne jamais en copier le contenu ailleurs ni le committer.

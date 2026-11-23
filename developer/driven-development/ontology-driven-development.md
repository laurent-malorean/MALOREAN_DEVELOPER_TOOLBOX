---
type: bonne_pratique
sujet: developpement_guide_par_l_ontologie
sources:
  - https://malorean.net/articles/2026-10-29-ontology-driven-design-et-si-lontologie-devenait-le-filet-de-securite-du-code-genere-par-lia.html
date: 2026-11-23
voir_aussi:
  - development-workflow.md
  - spec-driven-development.md
---

# Développement guidé par l'ontologie

## L'idée

Chaque projet a un document de référence, **l'ontologie**, qui décrit le métier : ses mots, ses règles, ses états. Un mot = une chose, et ce mot est le même partout : spécifications, écrans, API, outils MCP, tests, code, documentation.

L'ontologie passe **avant** le code. Le code reprend les mots de l'ontologie ; si le code a besoin d'un autre mot, on change d'abord l'ontologie.

L'ontologie décrit le métier, pas l'architecture technique : une classe n'est pas forcément un concept métier.

L'ontologie est l'une des quatre références d'un projet (ontologie, spécification, code, proposition) ; leur rôle respectif, l'ordre de travail, le traitement des écarts et les contrôles sont décrits dans `development-workflow.md`. Ce fichier décrit ce qui est propre à l'ontologie : son contenu et les règles du vocabulaire.

## Où vit l'ontologie

- Point d'entrée unique : `doc/ontology/ontology.md`.
- Tant qu'elle se lit d'une traite, elle tient dans ce seul fichier.
- Quand elle grossit, on la découpe par domaine dans `doc/ontology/` (un fichier par domaine) ; `ontology.md` reste le sommaire qui renvoie vers chacun.

## Ce que contient l'ontologie

### 1. Les concepts, rangés par domaine

Une ligne par concept, et une seule :

| Mot | Code | Définition |
|---|---|---|
| Espace de travail | `Workspace` | Un nom et un dossier racine choisi par l'utilisateur, qui contient toutes ses notes. N'est pas un dossier quelconque du disque. Autrefois « bibliothèque ». Règles : `espace-de-travail.un-seul-ouvert`. |

- **Mot** : le terme métier, celui que voit l'utilisateur et qu'on emploie dans les documents.
- **Code** : le nom exact du type, de la classe, de la fonction, du module d'interface ou de la classe CSS qui porte la notion.
- **Définition** : ce que la notion **est** et ce qu'elle **n'est pas**. Les règles ne s'écrivent pas ici : la définition renvoie à leurs identifiants dans la section « Règles ».

### 2. Les relations

Comment les concepts se lient : « une commande est associée à un client », « un avoir référence la facture qu'il corrige ».

### 3. Les règles

Ce qui doit toujours être vrai, quel que soit l'écran ou le parcours. Chaque règle a un identifiant `<concept>.<nom-court>` (format détaillé dans `spec-driven-development.md`) :

| Identifiant | Règle | Testable |
|---|---|---|
| `facture.validee-non-modifiable` | Une facture validée ne peut plus être modifiée. | Oui |
| `facture.au-moins-une-ligne` | Une facture a au moins une ligne. | Oui |
| `action.une-seule-personne` | Une action concerne une seule personne. | Oui |

- Une règle testable a au moins un test qui cite son identifiant.
- Une règle non testable est marquée « Non » avec la raison ; elle relève de la relecture.
- La spécification cite ces règles ; elle ne les reformule jamais.

### 4. Les états et transitions

La vie d'un concept : « une commande peut être validée, annulée ou facturée » ; « une commande annulée ne peut pas être expédiée ». Une transition interdite est une règle : elle a son identifiant dans la section « Règles ».

### 5. Les mots à ne pas confondre

Chaque mot qui pourrait désigner deux choses, avec la façon de les distinguer (ex. une « action » du CRM n'est pas un geste de l'utilisateur, qui s'appelle « intention » ; une « étape » est une colonne du Kanban, un « passage » est un séjour d'une personne dans une entreprise).

### 6. Les mots refusés

Les synonymes interdits, avec le mot retenu à la place :

| Mot refusé | Mot retenu |
|---|---|
| Contact | Personne |
| Société | Entreprise |
| Tâche | Action |
| bibliothèque | Espace de travail |

Cette liste alimente le contrôle automatique du vocabulaire.

### 7. La traçabilité vers le code

Pour chaque concept, les éléments qui le réalisent : classes, fonctions, événements, opérations d'API, outils MCP. Ces liens ne définissent pas le concept. Chaque lien garde sa preuve (fichier, symbole) ; une relation supposée n'est pas une correspondance démontrée.

(Le lien entre une règle et ses tests passe, lui, par l'identifiant de la règle cité dans les tests.)

### 8. L'index des décisions

Un index daté qui pointe vers les propositions archivées (`doc/changes/archive/`). La raison d'une décision s'écrit **uniquement** dans la proposition du changement ; l'index ne la recopie pas.

| Date | Décision | Changement |
|---|---|---|
| 2026-10-12 | Le type de page Kanban disparaît au profit du CRM | `archive/2026-10-12-kanban-vers-crm` |

Les propositions archivées gardent les mots de leur époque : on ne les réécrit pas quand un mot change.

## Les règles du vocabulaire

1. **Ontologie d'abord.** Un mot nouveau entre dans l'ontologie avant d'apparaître dans le code, les tests, les écrans ou les documents.
2. **Un seul mot par notion, partout.** Écrans, documents, commentaires, types, fonctions, tests, classes CSS, messages d'erreur. Pas de synonyme, même « pour varier ».
3. **Un seul sens par mot.** Si deux notions se disputent un mot, l'une change de nom.
4. **Le mot vient de l'ontologie, pas de l'habitude.** On ne prend pas un terme parce qu'il est courant ailleurs (`sidebar`, `vault`, `item`…).
5. **Pas de nom temporaire.** Il deviendra permanent.

## Quand un mot est remplacé

Les deux mécanismes se complètent ; un mot remplacé apparaît aux deux endroits :

- **Dans la liste des mots refusés**, avec le mot retenu : c'est ce qui sert au contrôle et à la correction.
- **Dans la définition du mot retenu**, sous la forme « Autrefois … » : c'est ce qui garde l'historique pour le lecteur.

L'ancien mot ne s'emploie plus nulle part ailleurs. Renommer, c'est tout renommer d'un coup : ontologie d'abord, puis code, tests, identifiants, spécifications, écrans et documentation MCP, **dans le même commit**.

## Les réflexes

- Avant de nommer quoi que ce soit, chercher dans l'ontologie.
- Avant de toucher un concept, relire sa définition et ses règles : elles contraignent souvent le changement (« une action concerne une seule personne » → l'entreprise de l'action en découle).
- Un mot pour deux choses, ou deux mots pour une chose : c'est un défaut. Le noter dans « mots à ne pas confondre », puis le résoudre en renommant.
- Synonyme ou ancien mot repéré : le remplacer par le mot de l'ontologie.
- Une question métier se raisonne avec l'ontologie, pas avec le code ; le code sert à vérifier.
- Le commentaire d'un élément public dit ce qu'on obtient, dans les mots de l'ontologie. S'il est difficile à écrire, la notion est mal définie : revenir à l'ontologie.
- Extraire une fonction quand la partie extraite a un nom de l'ontologie et un sens seule, pas pour réduire la taille.

## Les contrôles propres à l'ontologie

(La liste complète des contrôles est dans `development-workflow.md`.)

- **Vocabulaire** : une étape de la CI locale, avant chaque commit, cherche les mots refusés dans tout le dépôt et refuse le commit s'il en reste — sauf dans les propositions archivées (`doc/changes/archive/`) et les mentions « Autrefois … » de l'ontologie.
- **Interface** : un test vérifie qu'aucun mot refusé n'apparaît à l'écran.
- **Relecture** : ce que l'outil ne peut pas trancher (un mot juste dans un autre sens, comme « page web »).

L'ontologie ne remplace ni les tests unitaires ni les tests d'intégration ; l'analyse par IA n'a pas la garantie d'une assertion déterministe.

## Pourquoi

- **Une seule langue** : un mot vu à l'écran se retrouve tel quel dans le code et les tests ; une demande métier se traduit directement dans le code.
- **Pas de faux doublons** : deux noms pour la même chose finissent en deux implémentations qui divergent.
- **Ambiguïtés tranchées une fois**, par écrit, au lieu d'être redécouvertes à chaque évolution.
- **Les tests décrivent le métier** : nommés avec l'ontologie, ils se lisent comme des règles fonctionnelles.
- **Un filet pour le code généré par l'IA** : un code qui compile et passe ses tests peut quand même trahir le métier. L'ontologie évite que chaque agent reconstruise sa propre interprétation du domaine.
- **Arrivée rapide** : une IA ou un développeur lit un seul document pour comprendre le domaine, avant la première ligne de code.

## Exemple réel de correction

Un audit a trouvé des notions à deux noms : le type de contenu des notes s'appelait « page » dans le code et « note » partout ailleurs ; l'interface était tantôt « l'interface », tantôt « la page » ; la liste des notes s'appelait `sidebar` dans le CSS ; « bibliothèque » traînait encore après avoir été remplacée par « espace de travail ».

Correction : un seul mot par notion, ontologie mise à jour (avec « Autrefois … »), renommage dans le code, les tests, les écrans et les documents, une proposition de changement qui explique le choix, et les anciens mots ajoutés aux mots refusés pour qu'ils ne reviennent pas.

## Modèle de `doc/ontology/ontology.md`

```markdown
# Ontologie — <projet>

## Concepts

### <Domaine>

| Mot | Code | Définition |
|---|---|---|
|  |  | <Ce que c'est, ce que ce n'est pas. Autrefois … Règles : <identifiants>.> |

## Relations

- 

## Règles

| Identifiant | Règle | Testable |
|---|---|---|
|  |  | Oui / Non (raison) |

## États et transitions

| Concept | États | Transitions autorisées |
|---|---|---|
|  |  |  |

## Mots à ne pas confondre

| Mot | Sens A | Sens B | Comment distinguer |
|---|---|---|---|
|  |  |  |  |

## Mots refusés

| Mot refusé | Mot retenu |
|---|---|
|  |  |

## Traçabilité vers le code

| Concept | Réalisé par | Preuve |
|---|---|---|
|  |  |  |

## Index des décisions

| Date | Décision | Changement |
|---|---|---|
|  |  |  |
```

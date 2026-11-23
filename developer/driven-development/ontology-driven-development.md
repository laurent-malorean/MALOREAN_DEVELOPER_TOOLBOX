---
type: bonne_pratique
sujet: developpement_guide_par_l_ontologie
sources:
  - https://malorean.net/articles/2026-10-29-ontology-driven-design-et-si-lontologie-devenait-le-filet-de-securite-du-code-genere-par-lia.html
date: 2026-11-20
---

# Développement guidé par l'ontologie

## L'idée

Chaque projet a un document de référence, **l'ontologie**, qui décrit le métier : ses mots, ses règles, ses états. Un mot = une chose, et ce mot est le même partout : spécifications, écrans, API, outils MCP, tests, code, documentation.

L'ontologie passe **avant** le code. Le code reprend les mots de l'ontologie ; si le code a besoin d'un autre mot, on change d'abord l'ontologie.

L'ontologie décrit le métier, pas l'architecture technique : une classe n'est pas forcément un concept métier.

Trois références, trois rôles :

- **Le code** est la vérité du comportement réellement implémenté.
- **L'ontologie** est la référence du sens métier.
- **L'intention** (la demande) explique pourquoi ce sens peut changer.

## Où vit l'ontologie

- Point d'entrée unique : `doc/ontology/ontology.md`.
- Tant qu'elle se lit d'une traite, elle tient dans ce seul fichier.
- Quand elle grossit, on la découpe par domaine dans `doc/ontology/` (un fichier par domaine) ; `ontology.md` reste le sommaire qui renvoie vers chacun.

## Ce que contient l'ontologie

### 1. Les concepts, rangés par domaine

Une ligne par concept, et une seule :

| Mot | Code | Définition |
|---|---|---|
| Espace de travail | `Workspace` | Un nom et un dossier racine choisi par l'utilisateur, qui contient toutes ses notes. Un seul est ouvert à la fois. Autrefois « bibliothèque ». |

- **Mot** : le terme métier, celui que voit l'utilisateur et qu'on emploie dans les documents.
- **Code** : le nom exact du type, de la classe, de la fonction, du module d'interface ou de la classe CSS qui porte la notion.
- **Définition** : ce que la notion veut dire, ses règles essentielles et ses limites — ce qu'elle est, ce qu'elle n'est pas, ce qui est interdit (ex. « une personne est rattachée à une entreprise à la fois »).

### 2. Les relations

Comment les concepts se lient : « une commande est associée à un client », « un avoir référence la facture qu'il corrige ».

### 3. Les règles et invariants

Ce qui doit toujours être vrai : « une facture validée ne peut plus être modifiée », « une facture a au moins une ligne », « une action concerne une seule personne ». Chaque invariant qui le peut devient un test exécutable.

### 4. Les états et transitions

La vie d'un concept : « une commande peut être validée, annulée ou facturée » ; « une commande annulée ne peut pas être expédiée ».

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

### 8. Les décisions

Pour chaque concept retiré, fusionné, renommé ou règle supprimée : la décision et sa raison (ex. pourquoi le type de page Kanban a disparu au profit du CRM). Les fiches de décision sont datées et gardent les mots de leur époque : on ne les réécrit pas quand un mot change.

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

L'ancien mot ne s'emploie plus nulle part ailleurs. Renommer, c'est tout renommer d'un coup : ontologie d'abord, puis code, tests, spécifications, écrans et documentation MCP, dans le même commit.

## L'ordre de travail

Toute évolution suit cet ordre, sans sauter d'étape :

1. **Confronter la demande à l'ontologie** (obligatoire, avant tout code). Identifier les concepts, règles et états touchés ; relever les contradictions. Seulement les concepts utiles, pas toute l'ontologie.
   - Évolution voulue du métier → on met l'ontologie à jour (étape 2), puis on cherche les autres endroits qui supposent encore l'ancienne règle.
   - Erreur de conception → on corrige la demande, pas l'ontologie.
   - Demande ambiguë → on pose la question ; on n'invente pas de règle.
2. **Ontologie.** Si l'évolution crée, renomme ou précise un concept : définition, règles, nom dans le code, mots refusés, décision.
3. **Test.** Écrire le test qui décrit le comportement attendu, nommé par ce qu'il garantit, avec les mots de l'ontologie.
4. **Échec.** Le lancer et le voir échouer, pour la bonne raison.
5. **Code.** Le code minimal qui fait passer le test, avec les noms de la colonne « Code ».
6. **Vérification.** Relancer le test, puis toute la suite ; contrôler la cohérence avec l'ontologie.
7. **Commit.** Ontologie, spécification, test, code et documentation ensemble.

## Quand le code et l'ontologie divergent

Un écart n'est pas toujours un bug : il peut signaler une transformation voulue du métier. On le classe :

- **Évolution voulue** (la demande l'explique) → l'ontologie évolue, avec une décision.
- **Dérive** (rien dans la demande ne l'explique : concept qui change de sens, vocabulaire qui diverge, notion abandonnée réintroduite) → on corrige le code.
- **Doute** → décision humaine.

Le code n'a pas automatiquement raison. On ne modifie jamais l'ontologie pour rendre acceptable une erreur du code.

## Les réflexes

- Avant de nommer quoi que ce soit, chercher dans l'ontologie.
- Avant de toucher un concept, relire sa définition : elle contient souvent la règle qui contraint le changement (« une action concerne une seule personne » → l'entreprise de l'action en découle).
- Un mot pour deux choses, ou deux mots pour une chose : c'est un défaut. Le noter dans « mots à ne pas confondre », puis le résoudre en renommant.
- Synonyme ou ancien mot repéré : le remplacer par le mot de l'ontologie.
- Une question métier se raisonne avec l'ontologie, pas avec le code ; le code sert à vérifier.
- Le commentaire d'un élément public dit ce qu'on obtient, dans les mots de l'ontologie. S'il est difficile à écrire, la notion est mal définie : revenir à l'ontologie.
- Extraire une fonction quand la partie extraite a un nom de l'ontologie et un sens seule, pas pour réduire la taille.

## Les contrôles

- **Vocabulaire** (déterministe) : une étape de la CI locale, avant chaque commit, cherche les mots refusés dans tout le dépôt et refuse le commit s'il en reste — sauf dans les fiches de décision et les mentions « Autrefois … ». Un test vérifie aussi qu'aucun mot refusé n'apparaît dans l'interface.
- **Invariants** (déterministe) : les règles de l'ontologie deviennent des tests ; on suit la part des invariants couverts.
- **Cohérence métier** (sémantique, par l'IA) : avant fusion, confronter les changements à l'ontologie et produire un rapport — concepts nouveaux ou modifiés, règles impactées, incohérences, modifications d'ontologie proposées, décisions à valider.
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

Correction : un seul mot par notion, ontologie mise à jour (avec « Autrefois … »), renommage dans le code, les tests, les écrans et les documents, une fiche de décision, et les anciens mots ajoutés aux mots refusés pour qu'ils ne reviennent pas.

## Modèle de `doc/ontology/ontology.md`

```markdown
# Ontologie — <projet>

## Concepts

### <Domaine>

| Mot | Code | Définition |
|---|---|---|
|  |  |  |

## Relations

- 

## Règles et invariants

- 

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

## Décisions

| Date | Décision | Raison |
|---|---|---|
|  |  |  |
```

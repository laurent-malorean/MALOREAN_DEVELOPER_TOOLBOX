---
type: bonne_pratique
sujet: flux_de_developpement
date: 2026-11-23
voir_aussi:
  - ontology-driven-development.md
  - spec-driven-development.md
  - ../security/dependencies.md
  - ../ai-agent/agent-team.md
---

# Flux de développement

Ce fichier est **le seul** à décrire l'ordre de travail, le traitement des écarts, la couverture de tests et la liste des contrôles. Les méthodes par l'ontologie et par la spécification y renvoient ; elles ne le recopient pas.

## Les quatre références

| Référence | Ce qu'elle dit | Où |
|---|---|---|
| **Ontologie** | Ce que **sont** les choses : concepts, mots, règles toujours vraies | `doc/ontology/` |
| **Spécification** | Ce que le système **doit faire** : exigences et critères d'acceptation | `doc/specs/` |
| **Code** | Ce que le système **fait réellement** | le code et ses tests |
| **Proposition** | **Pourquoi** on change : l'intention et la décision | `doc/changes/` |

Une information, un seul endroit : la règle dans l'ontologie, le comportement dans la spécification, la raison dans la proposition, l'historique des modifications dans git.

## Choisir la taille du changement

| Situation | Ce qu'on fait |
|---|---|
| Nouvelle fonctionnalité, nouvelle règle métier, renommage d'un concept | Dossier de changement complet |
| Bug qui révèle une exigence manquante | Dossier léger : proposition, exigence ajoutée à la spécification, tâches, revue du juge |
| Bug sur un comportement déjà spécifié | Pas de dossier : un test qui cite le critère concerné, puis le correctif |
| Remaniement sans changement de comportement, faute de frappe | Rien de plus que le cycle TDD habituel |

Dans tous les cas, le cycle TDD s'applique.

## L'ordre de travail

Toute évolution suit cet ordre, sans sauter d'étape. Quand le travail est mené par des agents, qui mène chaque étape et quel fichier il produit est décrit dans `../ai-agent/agent-team.md`.

### 1. Confronter la demande

Avant tout code, lire l'ontologie et la spécification de référence. Identifier les concepts, règles, exigences et états touchés (seulement ceux utiles) ; relever les contradictions. Trancher :

- **Évolution voulue du métier** → on continue, et on cherche tous les autres endroits qui supposent encore l'ancienne règle.
- **Erreur de conception dans la demande** → on corrige la demande, pas l'ontologie.
- **Demande ambiguë** → on pose la question. Si on avance malgré tout, le point est marqué « À clarifier » ; on n'invente jamais de règle.

### 2. Ouvrir le changement

Créer `doc/changes/<nom-du-changement>/` à partir des modèles (`doc/changes/_templates/`) : la proposition avec ses « Exigences touchées ». Les autres fichiers (plan de test, plan technique, plan d'interface, tâches, revue) sont écrits par les agents, selon la taille du changement (voir `../ai-agent/agent-team.md`).

### 3. Mettre à jour les références

Directement dans les références, sur la branche du changement :

1. **L'ontologie d'abord** : concept nouveau, renommé ou précisé ; règle ajoutée, modifiée ou retirée ; mots refusés.
2. **Puis la spécification** : exigences et critères d'acceptation, avec les mots de l'ontologie.
3. **Valider la préparation** (humain) : spécification, plans et plan de test relus avant tout code.

### 4. Développer en TDD, critère par critère

Les critères d'acceptation et les règles de l'ontologie forment la liste des tests à écrire. Pour chacun :

1. **Rouge** : écrire le test, qui porte l'identifiant du critère ou de la règle. Le lancer et le voir échouer, **pour la bonne raison**.
2. **Vert** : écrire le code **minimal** qui le fait passer, avec les noms de la colonne « Code » de l'ontologie.
3. **Nettoyage** : remanier sans changer le comportement, relancer **toute** la suite.

On ne passe au critère suivant qu'une fois le cycle bouclé. Aucun code de production n'est écrit sans un test rouge qui le réclame.

Niveau de test :
- règle de l'ontologie → test unitaire du domaine ;
- critère d'acceptation → test du cas d'usage (ou d'intégration) ;
- parcours critique → test de bout en bout, en nombre limité.

### 5. Vérifier

- Toute la suite passe.
- Couverture et test de mutation au-dessus des seuils (voir plus bas).
- Cohérence avec l'ontologie : pas de dérive (voir « Les écarts »).

### 6. Faire le bilan

Dans `tasks.md` du changement, exigence par exigence : faite et prouvée par tel test, non faite et pourquoi, bloquée par tel point « À clarifier ». Le bilan contient aussi le rapport de cohérence : concepts et règles touchés, écarts trouvés et leur classement, décisions à valider.

### 7. Relecture humaine

Le développeur relit le bilan, les modifications d'ontologie et de spécification, puis le code. Ce que l'outil ne peut pas trancher (un mot juste dans un autre sens) se décide ici.

### 8. Archiver et intégrer

- Déplacer le dossier vers `doc/changes/archive/AAAA-MM-JJ-<nom>/`.
- Ajouter la ligne correspondante dans l'index des décisions de l'ontologie.
- Intégrer la branche.

Les commits intermédiaires sont permis pendant le changement, à condition que chacun passe les contrôles « à chaque commit ». Un renommage de concept, lui, se fait dans un seul commit (voir la méthode par l'ontologie).

## Les écarts entre code et références

Un écart entre le code, l'ontologie et la spécification n'est pas toujours un bug : il peut signaler une évolution voulue du métier. On le classe :

- **Évolution voulue** (la proposition l'explique) → l'ontologie ou la spécification évolue, et la proposition le dit.
- **Dérive** (rien dans la proposition ne l'explique : concept qui change de sens, vocabulaire qui diverge, notion abandonnée réintroduite, comportement non spécifié) → on corrige le code.
- **Doute** → décision humaine, point marqué « À clarifier ».

Le code n'a pas automatiquement raison. On ne modifie jamais l'ontologie ou la spécification pour rendre acceptable une erreur du code.

## La couverture de tests

### Deux couvertures, qui se contrôlent l'une l'autre

1. **Couverture des exigences** : chaque critère d'acceptation et chaque règle testable de l'ontologie a au moins un test qui porte son identifiant.
2. **Couverture du code** : lignes **et** branches exécutées par les tests.

Du code non couvert par un test de critère ou de règle signale :
- soit un comportement non spécifié → il manque une exigence (dérive à traiter) ;
- soit du code mort → à supprimer.

### Le test de mutation

Un fort taux de couverture peut cacher des tests qui exécutent le code sans rien vérifier. Le test de mutation modifie volontairement le code (un `<` devient `<=`, une condition est inversée…) et vérifie qu'au moins un test échoue. Lancé sur le code métier, en CI ou avant archivage (il est lent).

### Les seuils

| Mesure | Code métier (domaine, cas d'usage) | Reste du code |
|---|---|---|
| Couverture des lignes | ≥ 90 % | ≥ 80 % |
| Couverture des branches | ≥ 90 % | ≥ 80 % |
| Mutants détectés | ≥ 80 % | — |
| Couverture des exigences | 100 % des critères et des règles testables | — |

**Sans recul** : un changement qui fait baisser une de ces mesures est refusé, même au-dessus du seuil. Les seuils sont un point de départ ; chaque projet peut les relever, jamais les baisser sans décision écrite.

Code exclu de la mesure : uniquement le code généré et la configuration, listés explicitement dans la configuration de l'outil de couverture.

## Les contrôles

| Contrôle | Quand | Bloque | Défini dans |
|---|---|---|---|
| Mots refusés absents (sauf archives, propositions, extraits générés, mentions « Autrefois … » de l'ontologie) | Chaque commit | Oui | Méthode par l'ontologie |
| Mots refusés absents de l'interface (test) | Chaque commit | Oui | Méthode par l'ontologie |
| Toute la suite de tests passe | Chaque commit | Oui | Ce fichier |
| Couverture lignes et branches : seuils et sans recul | Chaque commit | Oui | Ce fichier |
| Aucun test ne cite un identifiant inconnu | Chaque commit | Oui | Méthode par la spécification |
| Chaque exigence a au moins un critère d'acceptation | Chaque commit | Oui | Méthode par la spécification |
| Chaque critère touché et chaque règle citée testable a un test | Avant archivage | Oui | Ce fichier |
| Aucun « À clarifier » dans les exigences touchées ni le dossier, aucune hypothèse non validée dans leurs fiches | Avant archivage | Oui | Méthode par la spécification |
| Toutes les tâches cochées, bilan rempli | Avant archivage | Oui | Méthode par la spécification |
| Lignes « Test » et extrait de spécification de chaque PR à jour | Chaque commit | Oui | Méthode par la spécification |
| Dernier verdict du juge « Accepté » | Avant archivage | Oui | `../ai-agent/agent-team.md` |
| Chaque critère touché figure au bilan ; vérifications manuelles du plan de test cochées | Avant archivage | Oui | `../ai-agent/agent-team.md` |
| Test de mutation : seuil et sans recul | CI / avant archivage | Oui | Ce fichier |
| Cohérence métier (rapport par l'IA) | Avant archivage | Non, décision humaine | Ce fichier |
| Relecture humaine | Avant intégration | Oui | Ce fichier |
| Dépendances : failles connues, maintenance | Voir la fiche | Voir la fiche | `../security/dependencies.md` |

### Lancer les bons contrôles au bon moment

Les contrôles lancés dépendent de ce qu'on a touché. Un échec qui se voit en quelques secondes ne doit jamais coûter le temps d'une CI complète.

| Ce qu'on a touché | Ce qu'on lance, en local | Durée |
|---|---|---|
| Spécification ou ontologie seulement | Vocabulaire et traçabilité (`toolbox_checks.py commit`, déjà lancé par le hook) | Quelques secondes |
| Du code, y compris par un remplacement de texte | Mise en forme, analyse du code, tests de la partie touchée | Rapide |
| Prêt à intégrer | La CI complète, une seule fois | Longue |

- **Rapide avant long** : on ne lance la CI complète qu'une fois les contrôles rapides de la partie touchée au vert.
- **Un remplacement mécanique est une modification comme une autre.** Un renommage ou un remplacement de texte dans du code — même dans un libellé — peut casser la mise en forme, la longueur des lignes ou un test : il passe par les contrôles du code. Dans la documentation, il ne passe que par ceux de la documentation. Cas typique : un renommage dans l'ontologie, qui se propage dans tout le projet.
- **La CI échoue vite** : les contrôles les moins chers d'abord (mise en forme, analyse, tests unitaires), les plus longs ensuite ; arrêt au premier échec.
- **Un journal par exécution** : chaque exécution de la CI écrit son propre journal, horodaté, sans écraser le précédent ; sinon on ne peut plus dire après coup quand et pourquoi elle a échoué.

### Qui implémente quoi

- **Fourni par la boîte à outils**, identique pour tous les projets : [`tools/toolbox-checks/`](../../tools/toolbox-checks/README.md) — vocabulaire, traçabilité, génération des lignes « Test », contrôles avant archivage, hook git. Le projet le copie et l'active ; il ne le réécrit pas.
- **Implémenté par chaque projet**, car dépendant de sa stack : la commande de tests, la mesure de couverture (lignes, branches) avec les seuils ci-dessus et la règle sans recul, le test de mutation. Branchés dans `commit_commands` de `toolbox-checks.json` et dans la CI.

| Contrôle | Commande |
|---|---|
| Chaque commit | `toolbox_checks.py commit` (via le hook git) |
| Mise à jour des lignes « Test » | `toolbox_checks.py traceability --write` |
| Mise à jour des extraits de spécification | `toolbox_checks.py extract` |
| Avant archivage | `toolbox_checks.py release doc/changes/<nom> --archive` |

---
type: bonne_pratique
sujet: developpement_guide_par_la_specification
date: 2026-11-23
sources:
  - https://github.com/Fission-AI/OpenSpec
  - https://raw.githubusercontent.com/github/spec-kit/main/templates/spec-template.md
  - https://kiro.dev/docs/specs/
  - https://kiro.dev/blog/deep-spec-analysis/
  - https://www.martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
voir_aussi:
  - development-workflow.md
  - ontology-driven-development.md
---

# Développement guidé par la spécification

## L'idée

La spécification dit ce que le système **doit faire**, sous une forme qui ne laisse rien d'implicite : des exigences atomiques, chacune avec ses critères d'acceptation, chacun prouvé par un test. Une IA qui implémente une spécification ainsi écrite ne peut pas « oublier » une partie sans que le contrôle le voie.

L'ordre de travail, le TDD, la couverture et les contrôles sont dans `development-workflow.md`. Ce fichier ne décrit que le **format**.

Inspirations : OpenSpec (spécification de référence vivante, dossier de changement archivé), Spec Kit (marqueur de clarification, hypothèses, critères de succès), Kiro et la notation EARS (forme fixe des exigences). Limites retenues de la critique (Böckeler, martinfowler.com) : l'IA ne suit pas toujours la spécification, d'où les tests ; un même processus pour tout est contre-productif, d'où la taille proportionnée ; une spécification qui ne vit pas diverge, d'où la mise à jour directe de la référence.

## Spécification et ontologie : qui porte quoi

| | Ontologie | Spécification |
|---|---|---|
| Répond à | Ce que **sont** les choses | Ce que le système **fait** |
| Contient | Concepts, définitions, relations, règles toujours vraies, états et transitions autorisés | Exigences de comportement et leurs critères d'acceptation |
| Exemple | `facture.validee-non-modifiable` : une facture validée ne peut plus être modifiée | Si l'utilisateur tente de modifier une facture validée, le système refuse et propose un avoir |

- L'ontologie porte **la règle**. La spécification porte **la réaction observable** du système (refus, message, effet) et cite la règle par son identifiant.
- Aucune exigence ne reformule une règle de l'ontologie.
- La spécification emploie exclusivement les mots de l'ontologie.

## Où ranger

```
doc/
  ontology/ontology.md                  ontologie (voir la méthode par l'ontologie)
  specs/<fonction>.md                   spécification de référence, une fiche par grande fonction
  changes/<nom-du-changement>/          changement en cours = une PR
    proposal.md                         pourquoi, décision, exigences touchées
    spec-extract.md                     extrait généré de la spécification (lecture seule)
    technical-plan.md                   plan technique (architecte)
    ui-plan.md                          plan d'interface (designer), si le changement touche l'interface
    test-plan.md                        jeux de données et vérifications manuelles (QA)
    review.md                           verdicts du juge, un par passage
    tasks.md                            tâches puis bilan
  changes/archive/AAAA-MM-JJ-<nom>/     changements livrés
```

Qui écrit quel fichier, et dans quel ordre : [`../ai-agent/agent-team.md`](../ai-agent/agent-team.md).

- `spec-extract.md` contient les exigences listées dans « Exigences touchées » de la proposition, avec leurs critères et les règles de l'ontologie qu'elles citent. Il est **généré** (`toolbox_checks.py extract`, vérifié à chaque commit) : on ne l'écrit jamais à la main, on modifie la spécification de référence.

- La spécification de référence décrit **toujours l'état actuel** du produit. Pendant un changement, on la modifie directement sur la branche : git garde le diff et signale les conflits entre changements parallèles.
- Une fiche de spécification peut citer des concepts de plusieurs domaines de l'ontologie ; les deux découpages n'ont pas à correspondre.
- Une fiche dépasse une quinzaine d'exigences → on la découpe en plusieurs fonctions.

## Les identifiants

Tout repose sur eux : un test prouve un critère ou une règle en citant son identifiant.

| Élément | Format | Exemple |
|---|---|---|
| Exigence | `<fonction>.<nom-court>` | `facturation.refuser-modification-validee` |
| Critère d'acceptation | `<exigence>.<nom-court>` | `facturation.refuser-modification-validee.ligne` |
| Règle de l'ontologie | `<concept>.<nom-court>` | `facture.validee-non-modifiable` |

- En minuscules, mots séparés par des tirets, avec les mots de l'ontologie.
- Fondés sur un nom court, jamais sur un numéro : deux changements parallèles ne se disputent pas « 007 ».
- Un identifiant retiré n'est **jamais réutilisé** pour autre chose.
- Renommer une fonction ou un concept renomme ses identifiants et les références dans les tests, dans le même commit.
- Dans les tests : un commentaire `@spec <identifiant-du-critère>` ou `@rule <identifiant-de-la-règle>`, dans la syntaxe de commentaire du langage, juste au-dessus du test. Un test peut en porter plusieurs. `@spec` cite toujours un critère, jamais une exigence.

## Le format des exigences

Une exigence = **une seule obligation**. Formes autorisées (notation EARS, en français) :

| Forme | Usage | Exemple |
|---|---|---|
| Le système doit … | Toujours vrai | Le système doit afficher les montants en euros. |
| Quand …, le système doit … | Réaction à un événement normal | Quand l'utilisateur valide une facture, le système doit lui attribuer un numéro unique. |
| Tant que …, le système doit … | Comportement dans un état | Tant qu'une facture est en brouillon, le système doit permettre d'en modifier les lignes. |
| Si …, alors le système doit … | Erreur, refus, cas indésirable | Si l'utilisateur tente de modifier une facture validée, alors le système doit refuser et proposer de créer un avoir. |
| Là où …, le système doit … | Option ou fonctionnalité activable | Là où la facturation multi-devises est activée, le système doit afficher la devise de chaque ligne. |

- Une exigence qu'on n'arrive pas à écrire sous une de ces formes est floue : on la reprend.
- Pas de « et » qui cache deux obligations : on découpe.
- Pas de solution technique dans l'exigence (ni table, ni classe, ni bibliothèque) : elle va dans `technical-plan.md`.

Une bonne exigence est : **testable, sans solution imposée, non ambiguë, cohérente avec les autres, complète**.

## Les critères d'acceptation

Chaque exigence a **au moins un** critère d'acceptation, écrit en scénario :

```
##### <identifiant-du-critère>
- Étant donné <contexte>
- Quand <action>
- Alors <résultat observable>
- Et <autre résultat observable>
- Test : <généré>
```

- Couvrir le cas nominal, les cas limites et les erreurs.
- Un critère = un test (au moins).
- La ligne « Test » est **générée** à partir des annotations des tests (`toolbox_checks.py traceability --write`) ; elle n'est jamais écrite à la main : `✅ <fichier>:<ligne>` ou `❌ aucun`. La section « Couverture » est générée de la même façon.

## Les marqueurs et sections de contrôle

- **« ⚠ À clarifier : <question> »** dans une exigence ou un critère : on ne code pas cet élément tant que la question n'est pas tranchée ; le reste du travail continue. Interdit à l'archivage.
- **Hypothèses** : les choix par défaut faits quand la demande ne disait rien. Chacune doit être validée (elle devient alors une exigence ou une règle) ou passer « À clarifier » avant l'archivage. Une hypothèse non validée est une règle inventée.
- **Hors périmètre** : ce qu'on ne fait pas, pour que l'IA n'en rajoute pas.
- **Critères de succès** : ce qui se mesure sur l'ensemble de la fonction et n'est pas un comportement unitaire (performance, volume, objectif).

## Modèle de fiche : `doc/specs/<fonction>.md`

````markdown
# Spécification — <Fonction>

## Objet
<Ce que le système fait pour cette fonction, en deux lignes.>

## Concepts utilisés
<Concepts de l'ontologie cités.>

## Couverture
<Généré : N critères, N testés, N sans test.>

## Exigences

### <fonction>.<nom-court>
Règle appliquée : ontologie › <concept>.<nom-court>   (si applicable)

<Exigence sous une forme EARS.>

#### Critères d'acceptation

##### <fonction>.<nom-court>.<cas>
- Étant donné …
- Quand …
- Alors …
- Test : <généré>

## Critères de succès
- 

## Hypothèses
- 

## Hors périmètre
- 
````

### Exemple

````markdown
# Spécification — Facturation

## Objet
Créer, valider et corriger les factures.

## Concepts utilisés
Facture, Ligne, Avoir, Client.

## Couverture
5 critères, 4 testés, 1 sans test.

## Exigences

### facturation.creer-facture
Quand l'utilisateur crée une facture pour un Client, le système doit
l'enregistrer à l'état « brouillon ».

#### Critères d'acceptation

##### facturation.creer-facture.nominal
- Étant donné un Client existant
- Quand l'utilisateur crée une facture pour ce Client
- Alors la facture existe à l'état « brouillon », sans ligne
- Test : ✅ tests/invoice_test.py:12

##### facturation.creer-facture.client-inconnu
- Étant donné un Client qui n'existe pas
- Quand l'utilisateur crée une facture pour ce Client
- Alors le système refuse et affiche « Client introuvable »
- Test : ✅ tests/invoice_test.py:20

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

##### facturation.refuser-modification-validee.client
- Étant donné une facture validée
- Quand l'utilisateur change le Client
- Alors la modification est refusée
- Test : ❌ aucun

### facturation.numeroter-facture
Quand l'utilisateur valide une facture, le système doit lui attribuer
un numéro unique.
⚠ À clarifier : numérotation continue sur l'année ou par client ?

#### Critères d'acceptation

##### facturation.numeroter-facture.validation
- Étant donné une facture « brouillon » avec au moins une ligne
- Quand l'utilisateur la valide
- Alors elle reçoit un numéro unique
- Test : ✅ tests/invoice_test.py:45

## Critères de succès
- Une facture de 500 lignes se valide en moins de 2 secondes.
- Aucune facture validée ne peut être modifiée, quel que soit le canal
  (écran, API, outil MCP).

## Hypothèses
- Les montants sont en euros. (À valider avant archivage.)

## Hors périmètre
- L'envoi de la facture par e-mail.
- Le paiement.
````

## Modèle : `doc/changes/<nom>/proposal.md`

C'est l'**unique registre du pourquoi** : décisions métier, concepts retirés ou fusionnés, choix d'une bibliothèque.

````markdown
# Changement — <nom>

## Demande
<La demande telle que formulée.>

## Exigences touchées
- `<fonction>.<nom-court>`

(Identifiants d'exigences, jamais de critères. Sert à générer `spec-extract.md`.)

## Confrontation
- Concepts et règles touchés : <identifiants>
- Contradictions : <aucune | liste>
- Classement : évolution voulue | erreur corrigée dans la demande | ambiguïté (voir « À clarifier »)

## Décision
<Ce qu'on décide et pourquoi. Alternatives écartées.>

## Impacts
- Ontologie : <concepts, règles, mots refusés ajoutés / modifiés / retirés>
- Spécification : <exigences ajoutées / modifiées / retirées>
- Autres endroits qui supposaient l'ancienne règle : <liste>
- Dépendances ajoutées : <bibliothèque, version, raison, résultat de la vérification>

## Hors périmètre
- 
````

## Modèle : `doc/changes/<nom>/tasks.md`

````markdown
# Tâches — <nom>

## Tâches
- [ ] Ontologie mise à jour
- [ ] Spécification mise à jour
- [ ] <critère> : rouge → vert → nettoyage
- [ ] …
- [ ] Suite complète, couverture, mutation au-dessus des seuils

## Bilan

| Exigence / critère / règle | État | Prouvé par |
|---|---|---|
| <identifiant> | ✅ fait / ❌ non fait / ⚠ bloqué | <test> ou <raison> |

## Rapport de cohérence
- Écarts trouvés : <liste, chacun classé évolution voulue / dérive / doute>
- Décisions à valider : <liste>
````

## Modèle : `doc/changes/<nom>/technical-plan.md`

````markdown
# Plan technique — <nom>

## Couches et modules touchés
- 

## Découpage
<Étapes de développement, dans l'ordre, chacune rattachée aux critères qu'elle fait passer.>

## Données
<Modèles, migrations, volumes. « Aucune » si rien.>

## Risques
- 

## Contrôle de cohérence avec le plan d'interface
<Rempli par l'architecte lors de sa passe légère : compatible, ou points à reprendre.>
````

## Modèle : `doc/changes/<nom>/ui-plan.md`

````markdown
# Plan d'interface — <nom>

## Écrans et composants touchés
- 

## Pour chaque composant
- Contenu attendu : <une ligne, un paragraphe, une liste… et sa longueur typique>
- Taille et place : <dimensionnée pour le contenu attendu, pas pour le minimum>
- États : vide, rempli, erreur, chargement, désactivé
- Clavier et accessibilité : <ordre de tabulation, raccourcis, libellés>

## Règles appliquées
<Lois UI et constantes utilisées, par leur nom.>
````

## Modèle : `doc/changes/<nom>/test-plan.md`

Les cas de test sont les critères d'acceptation, dans la spécification ; ils n'apparaissent pas ici.

````markdown
# Plan de test — <nom>

## Critères ajoutés à la spécification
<Identifiants des cas limites et erreurs que le QA a ajoutés.>

## Jeux de données
- 

## Vérifications manuelles
<Ce que les tests automatiques ne couvrent pas : parcours réel, rendu, ressenti.>
- [ ] 
````

## Modèle : `doc/changes/<nom>/review.md`

Un passage par évaluation du juge ; le **dernier** verdict doit être « Accepté » pour archiver.

````markdown
# Revue — <nom>

## Passage 1
Verdict : À reprendre

### Points
- [bloquant] <fichier:ligne> — <problème> — <attendu>
- [mineur] …

## Passage 2
Verdict : Accepté
````

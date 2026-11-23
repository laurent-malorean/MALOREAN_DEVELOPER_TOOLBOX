---
type: bonne_pratique
sujet: equipe_d_agents
date: 2026-11-23
voir_aussi:
  - agent-practices.md
  - ../driven-development/development-workflow.md
  - ../driven-development/spec-driven-development.md
  - ../../design/ux-ui/law-of-ui.md
  - ../../tools/agents/README.md
sources:
  - https://www.anthropic.com/engineering/multi-agent-research-system
  - https://arxiv.org/html/2308.00352v7
  - https://arxiv.org/pdf/2510.14509
  - https://arxiv.org/html/2509.13942v1
  - https://arxiv.org/html/2404.04834v4
---

# Équipe d'agents

## L'idée

Le but de la boîte à outils est de **coder avec des agents** : c'est le mode de travail de tout projet. Un changement passe entre plusieurs agents spécialisés — QA, architecte, designer, développeur, juge — **l'un après l'autre**, jamais en même temps. Chacun démarre avec un **contexte neuf**, lit les fichiers de la PR, écrit son résultat dans **son** fichier, et s'arrête. Les agents ne se parlent pas : **les fichiers de la PR sont la seule mémoire commune**.

Pourquoi séquentiel, pas une équipe qui discute :

- Des agents qui échangent entre eux se coordonnent mal : mémoire limitée, vue partielle du projet, échanges inutiles (constat des évaluations de MetaGPT et ChatDev, et d'un banc d'essai indépendant où ces systèmes échouent sur des projets complets).
- Un système multi-agents consomme environ **15 fois** plus de jetons qu'une conversation, et convient mal aux tâches où tous doivent partager le même contexte — c'est le cas du code (Anthropic).
- Un seul agent écrit le code. Les autres préparent ou contrôlent, chacun avec un regard neuf.

Cette fiche dit **qui fait quoi et dans quel ordre**. Le format des fichiers est dans `spec-driven-development.md` ; l'ordre de travail général, le TDD, les seuils et les contrôles sont dans `development-workflow.md`.

## Le pipeline

### Préparation

1. **Confrontation** (session principale) : confronter la demande à l'ontologie et à la spécification, ouvrir le dossier de la PR, écrire `proposal.md` avec ses « Exigences touchées », mettre à jour l'ontologie et la spécification. Joue le rôle de chef de produit ; pas d'agent dédié.
2. **QA** → complète la spécification (cas limites, erreurs), ajoute si besoin des exigences à la rubrique « Exigences touchées », écrit `test-plan.md`. Il passe avant l'architecte pour que le plan technique s'appuie sur des critères complets.
3. **Architecte** → `technical-plan.md`.
4. **Designer** → `ui-plan.md`. Seulement si le changement touche l'interface.
5. **Architecte, passe légère** → section « Contrôle de cohérence avec le plan d'interface » de `technical-plan.md`. Seulement s'il y a eu un designer.
6. **Validation humaine de la préparation.** Aucun code avant.

### Développement

7. **Développeur** → crée `tasks.md` (une tâche par critère de l'extrait), puis le code et ses tests, en TDD, critère par critère ; remplit le bilan.

### Contrôle

8. **Juge** → ajoute un passage à `review.md`, avec un verdict « Accepté » ou « À reprendre ».
9. Si « À reprendre » : retour au **développeur**, puis au **juge**. **Au plus deux allers-retours** ; au-delà, décision humaine.
10. **QA, passe finale** → coche les vérifications manuelles de `test-plan.md`. Rien de ce que le TDD couvre déjà.
11. **Relecture humaine**, puis archivage et intégration (voir le flux de développement).

**L'extrait est régénéré avant chaque agent** : la session principale lance `python3 tools/toolbox-checks/toolbox_checks.py extract` avant de passer la main, et les contrôles le régénèrent aussi à chaque commit. Chaque agent y trouve les exigences de la PR, à jour, sans relire toute la spécification.

**Un verdict « Accepté » vaut pour le code jugé.** Tout commit de code après l'acceptation demande un nouveau passage du juge avant l'archivage.

## Les rôles

Le détail de chaque rôle — ce qu'il lit, écrit, vérifie, et ce qui lui est interdit — est dans sa définition d'agent, seul endroit où il est écrit (le projet la copie telle quelle) :

- **Architecte** ([`architect.md`](../../tools/agents/architect.md)) : plan technique ; métier indépendant de l'infrastructure, réutilisation de l'existant, noms de l'ontologie. N'écrit pas de code.
- **QA** ([`qa.md`](../../tools/agents/qa.md)) : en préparation, ajoute les critères manquants **dans la spécification** et écrit le plan de test (données, vérifications manuelles) ; en passe finale, exécute ces vérifications. N'écrit pas les tests automatiques.
- **Designer** ([`designer.md`](../../tools/agents/designer.md)) : plan d'interface ; chaque zone dimensionnée pour le contenu attendu, états, clavier, accessibilité. N'écrit pas de code.
- **Développeur** ([`developer.md`](../../tools/agents/developer.md)) : seul à écrire le code, en TDD ; tient les tâches et le bilan. Ne modifie ni la spécification ni les plans.
- **Juge** ([`judge.md`](../../tools/agents/judge.md)) : regard neuf, sans le raisonnement du développeur ; vérifie conformité, plans, qualité, **sécurité**, **performance** et seuils ; verdict « Accepté » ou « À reprendre ». Ne modifie pas le code.

> Incident à l'origine du designer en préparation : dans une application de notes, la fenêtre « Ajouter au cahier » sert à saisir une ligne ou un paragraphe ; sa zone de saisie n'affiche que quatre lignes et la fenêtre occupe environ un quart de l'écran. Personne ne s'est posé la question de la taille du contenu attendu.

## Proportionner

- **Nouvelle fonctionnalité avec interface** : pipeline complet.
- **Nouvelle fonctionnalité sans interface** : sans designer ni passe légère de l'architecte.
- **Bug qui révèle une exigence manquante** (dossier léger) : confrontation, QA (préparation), développeur, juge.
- **Bug sur un comportement déjà spécifié** (pas de dossier) : développeur, puis juge sur les modifications ; le juge rend son verdict dans la description de la PR, faute de dossier.
- **Remaniement, faute de frappe** : développeur seul ; contrôles habituels.

## Les règles de conduite

- **Séquentiel** : un agent à la fois. Seules des tâches réellement indépendantes peuvent tourner en parallèle (par exemple deux lectures de code sans lien).
- **Contexte neuf** : chaque agent est lancé sans l'historique de la session ; il ne connaît que ce que lui donnent les fichiers de la PR et son brief.
- **Un fichier par rôle** : un agent n'écrit que dans son fichier (et, pour le QA, dans la spécification ; pour le développeur, dans le code et `tasks.md`).
- **Résumé structuré** : chaque agent termine par un résumé court — ce qu'il a écrit, les points ouverts — que la session principale relaie.
- **Rien n'est cru sur parole** : un agent vérifie dans les fichiers et le code ce qu'un autre affirme.
- **Droits minimaux** : chaque agent n'a que les outils dont son rôle a besoin. Les outils d'écriture ne se limitent pas à un fichier : l'interdiction d'écrire du code, pour l'architecte, le designer, le QA et le juge, tient à leur définition, et le juge la vérifie.
- **Arrêt** : au plus deux allers-retours développeur ↔ juge ; un point qu'aucun agent ne peut trancher devient « À clarifier » et remonte à l'humain.

## Les définitions d'agents

Les définitions prêtes à copier sont dans [`tools/agents/`](../../tools/agents/README.md) : une par rôle, indépendantes de la stack. Le projet les copie dans `.claude/agents/`, avec les modèles de fichiers (`tools/templates/change/` → `doc/changes/_templates/`) et les contrôles communs. Son `CLAUDE.md` donne aux agents les commandes de tests, de couverture et de mutation, les seuils et l'emplacement des lois UI et des constantes.

Ces définitions sont autonomes, car les projets n'ont pas accès à la boîte à outils : c'est la seule exception assumée à la règle « une information, un seul endroit ».

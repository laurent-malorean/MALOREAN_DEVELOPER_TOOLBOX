---
type: bonne_pratique
sujet: travail_avec_un_agent_ia
date: 2026-11-23
voir_aussi:
  - ../driven-development/development-workflow.md
---

# Travailler avec un agent IA

Règles de comportement pour l'agent IA (Claude Code ou autre) qui travaille sur un projet. Elles complètent le flux de développement, qui dit **quoi** contrôler ; cette fiche dit **comment l'agent mène son travail**. Chaque projet y renvoie depuis son `CLAUDE.md`.

Chaque règle vient d'un incident réel ; l'incident est cité pour qu'on comprenne pourquoi elle existe.

## Surveiller une tâche longue par son propre signal

Quand l'agent lance une tâche longue (CI, build, déploiement, migration) :

- Il la surveille avec un signal qui dépend **réellement** d'elle : son code de sortie, ou les lignes d'échec et de fin de son journal.
- Il signale le **premier échec immédiatement**, sans attendre la fin ni qu'on lui demande.
- Il signale aussi la fin, avec le verdict.
- Une surveillance branchée sur autre chose que la tâche (une notification qui arrive tout de suite, un délai fixe) revient à ne pas surveiller du tout.

> Incident : une CI lancée de façon à ce que la notification de fin arrive aussitôt, sans rapport avec la CI. Elle a échoué tôt, personne ne l'a su avant que le développeur demande : environ 30 minutes perdues.

## Vérifier vite avant de lancer long

L'agent applique « Lancer les bons contrôles au bon moment » du flux de développement : contrôles rapides de la partie touchée d'abord, CI complète seulement quand ils sont au vert. Un remplacement de texte dans du code est une modification de code.

> Incident : un mot remplacé dans des fichiers de l'interface pour l'aligner sur l'ontologie, sans relancer la mise en forme. Le remplacement a raccourci des lignes ; la CI longue a échoué sur son tout premier contrôle.

## Garder la trace de chaque exécution

L'agent écrit le journal de chaque exécution dans un fichier distinct et horodaté, jamais en écrasant le précédent. Il peut ainsi dire quand et pourquoi une exécution a échoué.

> Incident : journal de la CI remplacé par celui de la relance ; impossible de dire à quelle minute l'échec était arrivé.

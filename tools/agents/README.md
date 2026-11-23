# Définitions d'agents

Les cinq rôles de l'équipe d'agents, au format des sous-agents de Claude Code, indépendants de la stack. Pipeline, ordre et allègement : [agent-team.md](../../developer/ai-agent/agent-team.md).

- `architect.md` : plan technique, puis passe légère de cohérence avec le plan d'interface.
- `qa.md` : critères manquants et plan de test en préparation ; vérifications manuelles en passe finale.
- `designer.md` : plan d'interface.
- `developer.md` : seul à écrire le code, en TDD.
- `judge.md` : verdict sur le code, avec un regard neuf.

## Installer dans un projet

1. Copier ces fichiers (sauf ce README) dans `.claude/agents/` du projet.
2. Dans le `CLAUDE.md` du projet, indiquer où se trouvent les lois UI et les constantes de design que le designer doit lire.
3. Lancer les agents dans l'ordre du pipeline, un à la fois, en donnant à chacun le nom du dossier de la PR (`doc/changes/<nom>/`).

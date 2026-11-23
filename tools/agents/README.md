# Définitions d'agents

Les cinq rôles de l'équipe d'agents, au format des sous-agents de Claude Code, indépendants de la stack. Pipeline, ordre et allègement : [agent-team.md](../../developer/ai-agent/agent-team.md).

- `qa.md` : critères manquants et plan de test en préparation (premier agent) ; vérifications manuelles en passe finale.
- `architect.md` : plan technique, puis passe légère de cohérence avec le plan d'interface.
- `designer.md` : plan d'interface.
- `developer.md` : seul à écrire le code, en TDD.
- `judge.md` : verdict sur le code, avec un regard neuf.

Ces définitions sont copiées telles quelles dans les projets, qui n'ont pas accès à la boîte à outils : elles contiennent donc tout ce dont l'agent a besoin. C'est la seule exception assumée à la règle « une information, un seul endroit ».

## Installer dans un projet

1. Copier ces fichiers (sauf ce README) dans `.claude/agents/` du projet.
2. Copier `tools/templates/change/` dans `doc/changes/_templates/` du projet.
3. Copier `tools/toolbox-checks/` dans `tools/toolbox-checks/` du projet et activer son hook.
4. Dans le `CLAUDE.md` du projet, indiquer :
   - les commandes de tests, de couverture et de mutation ;
   - les seuils (ceux du flux de développement, ou plus hauts) ;
   - l'emplacement des lois UI et des constantes de design.

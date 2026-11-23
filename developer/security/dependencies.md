---
type: bonne_pratique
sujet: gestion_des_dependances
date: 2026-11-23
---

# Dépendances : choisir et surveiller

## L'idée

Chaque bibliothèque ajoutée devient du code qu'on n'a pas écrit, qu'on ne relit pas, et qui tourne avec les mêmes droits que le nôtre. On la vérifie **avant de l'ajouter**, puis **en continu** : une faille peut être découverte des mois après l'ajout.

## Avant d'ajouter une bibliothèque

### 0. En a-t-on vraiment besoin ?

- Quelques lignes de code suffiraient-elles ?
- Une dépendance déjà présente, ou la bibliothèque standard, fait-elle déjà le travail ?

Si oui : ne pas l'ajouter.

### 1. Scanner tout l'arbre, pas seulement la bibliothèque

Une bibliothèque en amène souvent des dizaines d'autres (dépendances indirectes). C'est là que se cachent la plupart des failles et des paquets abandonnés. Chaque critère ci-dessous s'applique à **l'ensemble de l'arbre** ajouté.

### 2. Maintenance

| Critère | Signal d'alerte |
|---|---|
| Dernière version publiée | Plus d'un an sans version |
| Activité du dépôt | Pas de commit récent, dépôt archivé, paquet marqué « deprecated » |
| Mainteneurs | Un seul mainteneur actif |
| Tickets et demandes de modification | Nombreux, anciens, sans réponse |
| Failles passées | Corrigées lentement ou pas du tout |
| Compatibilité | Ne suit pas les versions récentes du langage ou du framework |

### 3. Sécurité

- **Failles connues** : aucune faille ouverte dans les bases publiques (GitHub Advisory, OSV, CVE) pour la version choisie et ses dépendances.
- **Script exécuté à l'installation** (`postinstall`, `setup.py`…) : à examiner ; refuser s'il n'est pas justifié.
- **Nom piégé** : vérifier que c'est bien le paquet attendu, pas un nom proche d'un paquet connu (`reqeusts`, `lodahs`…) ni un paquet qui imite un nom interne.
- **Provenance** : éditeur identifiable, lien entre le paquet publié et son dépôt source, signature ou attestation si disponible.
- **Droits demandés** : accès réseau, système de fichiers, variables d'environnement cohérents avec ce que fait la bibliothèque.

### 4. Licence

- Compatible avec l'usage prévu (projet privé, commercial, distribué).
- Attention aux licences contaminantes (GPL, AGPL) et aux paquets sans licence.
- Vérifier aussi les licences des dépendances indirectes.

### 5. Coût

- Poids ajouté (installation et, pour le front, taille livrée au navigateur).
- Nombre de dépendances indirectes amenées.
- Surface d'API utilisée réellement : si on en utilise 2 %, envisager plus léger.

### 6. Noter le choix

Pour chaque bibliothèque ajoutée, consigner dans les décisions du projet : la bibliothèque, sa version, pourquoi elle (et pas une autre, ou pas du code maison), et le résultat de la vérification.

## En continu

- **À chaque commit ou en CI** : contrôle automatique des failles connues ; le build échoue sur une faille critique ou haute.
- **Versions verrouillées** : fichier de verrouillage (`package-lock.json`, `pnpm-lock.yaml`, `poetry.lock`, `composer.lock`…) toujours commité ; installation en CI à partir de lui (`npm ci`, etc.).
- **Mises à jour automatiques proposées** (Dependabot, Renovate) : relues comme n'importe quel changement, jamais fusionnées à l'aveugle.
- **Revue périodique** (au moins trimestrielle) : repasser les critères de maintenance sur toutes les dépendances ; remplacer ou retirer celles qui sont abandonnées ; supprimer celles qui ne servent plus.

## Outils

| Besoin | Outils |
|---|---|
| Failles connues, multi-écosystème | `osv-scanner`, GitHub Dependabot alerts |
| Failles par écosystème | `npm audit` / `pnpm audit`, `pip-audit`, `composer audit`, `cargo audit`, `govulncheck` |
| Santé et maintenance d'un projet | OpenSSF Scorecard, deps.dev |
| Comportements suspects (scripts, réseau, noms piégés) | Socket |
| Licences | `license-checker` (npm), `pip-licenses`, deps.dev |
| Mises à jour proposées | Dependabot, Renovate |
| Dépendances inutilisées | `depcheck` / `knip` (JS), `deptry` (Python), `composer-unused` |

## Les réflexes

- Pas d'ajout de dépendance sans la vérification ci-dessus, même « pour tester ».
- Une faille signalée se traite tout de suite : mettre à jour, remplacer, ou documenter pourquoi elle n'est pas exploitable dans notre usage.
- Moins de dépendances = moins de surface d'attaque et moins de maintenance.

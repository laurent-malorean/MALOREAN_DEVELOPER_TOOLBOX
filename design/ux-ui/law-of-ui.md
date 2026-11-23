---
source: https://www.uilaws.com/
date_analyse: 2026-04-10
type: analyse_source
nombre_lois: 13
categories:
  - perception_visuelle
  - gestalt
  - comportement_utilisateur
  - design_visuel
---

## Source : Laws of UI (uilaws.com)

Site de référence listant 13 lois fondamentales du design d'interface. Analyse approfondie de chaque principe avec applications pratiques, bonnes pratiques et dark patterns associés.

---

## Lois de perception visuelle

### 1. Symétrie (Gestalt)

**Énoncé** : L'œil humain perçoit les éléments symétriques comme un tout unifié.

**Principe détaillé** : L'esprit humain perçoit naturellement les objets comme des formes symétriques se formant autour de leur centre. Ce principe crée équilibre, ordre et stabilité dans les layouts. Les designs symétriques sont perçus comme plus attractifs et harmonieux, ce qui améliore l'engagement et la satisfaction utilisateur.

**Exemples source** :
- Layouts web équilibrés avec poids égal de chaque côté d'un axe central
- Logos et éléments de branding symétriques créant un sentiment de stabilité
- Éléments d'interface (menus de navigation, groupes de boutons) arrangés symétriquement
- Formulaires avec champs et labels alignés symétriquement

**Application** : Dashboard — disposer les métriques clés ou widgets symétriquement de chaque côté d'un élément central. Cela crée un sentiment d'équilibre et aide les utilisateurs à scanner rapidement l'information.

**Bonnes pratiques** :
- Utiliser la symétrie pour les zones de contenu équivalent (comparaison, choix entre options)
- Casser volontairement la symétrie pour attirer l'attention sur un élément (CTA principal)
- Grilles paires (2, 4 colonnes) renforcent la perception de stabilité

**Dark patterns à éviter** :
- Symétrie trompeuse entre deux boutons d'importance inégale (ex : "Supprimer" et "Annuler" stylés identiquement pour piéger l'utilisateur)

---

### 2. Règle des tiers

**Énoncé** : Diviser un layout en grille 3×3 et placer les éléments clés sur les lignes crée des compositions plus équilibrées.

**Principe détaillé** : Principe de composition qui divise une image ou un layout en neuf parts égales via deux lignes horizontales et deux lignes verticales également espacées. Les éléments clés du design doivent être placés le long de ces lignes ou à leurs intersections. Cela produit une composition plus équilibrée, naturelle et engageante que le simple centrage.

**Exemples source** :
- Placer le contenu clé ou les CTA aux points d'intersection de la grille
- Aligner les blocs de texte le long des lignes verticales de la grille
- Positionner les images héro pour que le sujet principal tombe sur une ligne de la grille
- Concevoir les layouts de dashboard avec les widgets les plus importants positionnés selon la règle des tiers

**Application** : Landing page — placer le titre principal et le CTA aux intersections de la grille. Cela crée un layout plus dynamique et visuellement attractif qui attire naturellement l'attention sur ces éléments clés.

**Bonnes pratiques** :
- Ne pas centrer systématiquement — le décentrement crée du dynamisme
- Utiliser les 2/3 restants pour le contenu secondaire
- Fonctionne particulièrement bien pour les layouts asymétriques maîtrisés

**Dark patterns à éviter** :
- Placer un bouton de désabonnement ou d'annulation hors des points de focus pour le rendre difficile à trouver

---

### 3. Espace blanc (White Space)

**Énoncé** : L'utilisation correcte de l'espace blanc améliore la lisibilité, le focus et l'attrait visuel global.

**Principe détaillé** : L'espace blanc (ou espace négatif) désigne les zones vides entre les éléments d'un design. Ce n'est pas nécessairement blanc — c'est l'absence de contenu. Son utilisation efficace améliore dramatiquement la lisibilité, la clarté et l'attrait esthétique d'une interface. Il guide le regard vers les éléments importants et prévient la surcharge cognitive.

**Exemples source** :
- Marges et paddings généreux autour des blocs de texte pour améliorer la lisibilité
- Espacement entre les éléments d'UI pour créer des hiérarchies visuelles claires
- Designs minimalistes utilisant l'espace blanc abondant pour créer une impression de luxe ou de sophistication
- Utilisation du white space pour grouper les éléments liés et séparer les sections

**Application** : Menu de paramètres d'une app mobile — utiliser un ample espace blanc entre les catégories de réglages. Cela améliore la lisibilité et aide les utilisateurs à identifier et accéder rapidement aux réglages sans se sentir submergés par une information dense.

**Bonnes pratiques** :
- Minimum 8px de micro-espacement entre éléments liés, 24-32px entre groupes distincts
- Plus le contenu est dense (tableau, liste), plus le white space interne est critique
- Augmenter l'espace blanc sur mobile (cibles tactiles plus grandes)
- Deux types : **macro** (entre sections) et **micro** (entre lignes, paragraphes, éléments de formulaire)

**Dark patterns à éviter** :
- Comprimer volontairement l'espace autour d'un lien de désabonnement ou d'une option "non merci"
- Noyer une option indésirable dans un bloc dense sans respiration

---

### 4. Théorie des couleurs

**Énoncé** : Les couleurs évoquent des émotions et associations ; leurs combinaisons créent harmonie ou discordance.

**Principe détaillé** : Étude de la façon dont les couleurs interagissent et affectent la perception et les émotions humaines. En UI design, les choix de couleur impactent significativement le comportement utilisateur, la perception de marque et l'expérience globale. Comprendre les relations chromatiques (complémentaire, analogue, triadique) aide à créer des interfaces visuellement attractives et efficaces.

**Exemples source** :
- Utilisation cohérente des couleurs de marque à travers l'UI pour renforcer l'identité
- Couleurs contrastées pour les CTA afin de les faire ressortir
- Schéma de couleurs évoquant les bonnes émotions pour le produit (ex : bleus calmes pour une app de méditation)
- Couleur pour indiquer les différents états des éléments (actif, hover, disabled)

**Application** : App financière — schéma à dominante bleue pour évoquer confiance et professionnalisme. Vert pour les indicateurs financiers positifs, rouge pour les négatifs, en respectant les associations chromatiques communes du monde financier.

**Bonnes pratiques** :
- Limiter la palette à 3-5 couleurs fonctionnelles + nuances
- Ne jamais communiquer une information uniquement par la couleur (accessibilité — daltonisme)
- Tester les contrastes avec WCAG AA minimum (ratio 4.5:1 pour le texte)
- Utiliser la saturation pour hiérarchiser : vif = important, désaturé = secondaire

**Dark patterns à éviter** :
- Colorer le bouton "Accepter" en vert vif et le bouton "Refuser" en gris pâle quasi invisible (manipulation du consentement)
- Utiliser le rouge pour une action bénigne afin de créer de l'anxiété

---

### 5. Hiérarchie typographique

**Énoncé** : Une hiérarchie claire de tailles et styles de texte guide l'utilisateur à travers le contenu et améliore la lisibilité.

**Principe détaillé** : Arrangement des éléments textuels qui communique clairement leur importance relative. Obtenue par des variations de taille, graisse, couleur et espacement. Une hiérarchie typographique bien structurée aide les utilisateurs à scanner le contenu rapidement, comprendre les relations entre les informations, et naviguer plus efficacement.

**Exemples source** :
- Polices plus grandes et grasses pour les titres, plus petites et légères pour le corps
- Styles ou couleurs de polices différents pour distinguer les types d'information
- Utilisation cohérente des tailles de police à travers l'UI pour maintenir une hiérarchie claire
- White space et line-height pour améliorer la lisibilité et séparer les niveaux d'information

**Application** : App d'actualités — grande police bold pour les titres, police légèrement plus petite pour les sous-titres, taille confortable pour le corps. Cette hiérarchie claire aide les utilisateurs à scanner les articles rapidement et décider lesquels lire en détail.

**Bonnes pratiques** :
- Ratio de taille minimum 1.25× entre chaque niveau (ex : 14px, 18px, 22px, 28px)
- Maximum 2 familles de polices (1 pour les titres, 1 pour le corps)
- Graisse : Regular (400) pour le corps, Medium (500) pour les labels, Bold (700) pour les titres
- Line-height : 1.5 pour le corps, 1.2 pour les titres

**Dark patterns à éviter** :
- Réduire la taille du texte des conditions générales pour décourager la lecture
- Utiliser une hiérarchie inversée (texte important en petit, texte commercial en gros)

---

## Lois de Gestalt (perception de groupement)

### 6. Proximité (Gestalt)

**Énoncé** : Les éléments proches les uns des autres sont perçus comme liés ou groupés.

**Principe détaillé** : Les objets proches apparaissent groupés ensemble. Ce principe est crucial pour créer des groupements logiques d'information et d'éléments dans une interface. En utilisant stratégiquement la proximité, les designers créent des relations claires entre les éléments, rendant l'interface plus intuitive et facile à naviguer.

**Exemples source** :
- Regrouper les champs de formulaire liés et séparer les sections par du white space
- Placer les items de menu de navigation proches pour indiquer qu'ils font partie du même menu
- Positionner les labels proches de leurs champs de saisie correspondants
- Regrouper les boutons ou actions liés dans les barres d'outils ou barres d'action

**Application** : Page produit e-commerce — grouper le titre, le prix et le bouton "Ajouter au panier" en proximité serrée, tout en gardant la description et les spécifications dans une section séparée voisine. Aide les utilisateurs à trouver et traiter rapidement l'information liée.

**Bonnes pratiques** :
- L'espace entre groupes doit être au moins 2× l'espace intra-groupe
- Préférer l'espacement aux bordures pour grouper (plus léger visuellement)
- Tester en supprimant toutes les bordures : la structure reste-t-elle lisible ?

**Dark patterns à éviter** :
- Rapprocher visuellement un opt-in marketing du bouton de validation pour créer une association trompeuse
- Éloigner volontairement l'option de désinscription des autres options de compte

---

### 7. Clôture (Gestalt)

**Énoncé** : L'esprit humain perçoit des formes complètes même lorsque des parties sont manquantes.

**Principe détaillé** : Principe de la psychologie Gestalt — quand nous rencontrons des formes ou informations incomplètes, notre esprit comble les parties manquantes pour créer un pattern complet et reconnaissable. En UI design, ce principe peut être exploité pour créer des designs plus engageants et minimalistes qui communiquent efficacement l'information. Il sert aussi à guider l'attention ou créer des éléments visuellement intéressants.

**Exemples source** :
- Lignes pointillées ou tiretées pour impliquer des limites ou connexions
- Logos ou icônes où des parties de la forme manquent mais restent reconnaissables
- Images ou textes partiellement masqués que l'esprit de l'utilisateur complète
- Animations de chargement impliquant mouvement ou progression sans montrer chaque frame

**Application** : Logo ou jeu d'icônes — utiliser la clôture pour des designs minimalistes mais reconnaissables. Ex : icône "paramètres" avec des dents d'engrenage incomplètes — l'esprit complète la forme. Cela crée un look visuellement intéressant et moderne tout en restant reconnaissable.

**Bonnes pratiques** :
- Utiliser la troncature visuelle pour indiquer "il y a plus" (scroll horizontal, listes longues)
- Conteneurs semi-ouverts (bordure seulement en haut et en bas) pour alléger
- Les progress bars partiellement remplies exploitent la clôture pour montrer la progression

**Dark patterns à éviter** :
- Cacher du contenu important derrière une clôture qui semble complète (l'utilisateur croit avoir tout vu)

---

### 8. Continuité (Gestalt)

**Énoncé** : Les éléments arrangés sur une ligne ou courbe sont perçus comme plus liés que les éléments hors de cette ligne.

**Principe détaillé** : L'œil humain suit naturellement les lignes, courbes ou séquences de formes, même interrompues. En UI design, ce principe guide l'attention à travers un layout, crée un sens du flux, et établit des relations entre les éléments. Particulièrement utile pour les patterns de navigation intuitifs et les processus multi-étapes.

**Exemples source** :
- Lignes ou flèches guidant les utilisateurs à travers un processus étape par étape
- Alignement d'éléments sur un axe commun pour impliquer une relation
- Interfaces de scroll où le contenu s'enchaîne fluidement d'une section à l'autre
- Lignes courbes dans les infographies pour guider l'œil à travers les données

**Application** : Formulaire multi-étapes (checkout) — utiliser une barre de progression ou des étapes numérotées alignées en ligne en haut de page. Cette continuité visuelle aide les utilisateurs à comprendre où ils en sont et combien d'étapes restent, réduisant la friction et les abandons.

**Bonnes pratiques** :
- Aligner les éléments liés sur un même axe (vertical ou horizontal)
- Les lignes de connexion (timelines, steppers) renforcent la continuité
- Utiliser l'indentation pour montrer la hiérarchie dans la continuité

**Dark patterns à éviter** :
- Insérer un élément publicitaire dans un flux de continuité pour le faire passer pour du contenu natif

---

### 9. Contraste

**Énoncé** : Les éléments qui se démarquent de leur environnement attirent davantage l'attention et sont mieux mémorisés.

**Principe détaillé** : Arrangement d'éléments opposés (clair vs sombre, petit vs grand, etc.) pour créer de l'intérêt visuel et de l'emphase. Un contraste élevé fait ressortir les éléments importants et améliore la lisibilité. Crucial pour l'accessibilité — s'assurer que le texte est lisible et que les éléments interactifs sont identifiables pour tous, y compris les personnes avec des déficiences visuelles.

**Exemples source** :
- Texte clair sur fond sombre (ou inversement) pour assurer la lisibilité
- CTA en couleur contrastante pour les faire ressortir
- Contraste de taille pour emphaser les titres ou éléments importants
- Contraste typographique en combinant serif et sans-serif

**Application** : Page d'inscription — contraste élevé pour le bouton submit (couleur vive saturée sur fond neutre). Attire l'attention sur l'action principale et augmente la probabilité de complétion du formulaire.

**Bonnes pratiques** :
- Un seul niveau de contraste fort par écran (sinon tout est "prioritaire" = rien ne l'est)
- Ratio de contraste WCAG AA : 4.5:1 pour le texte, 3:1 pour les éléments graphiques
- Le contraste de taille amplifie le contraste de couleur
- Effet Von Restorff / isolation effect : un seul élément contrasté attire immédiatement le regard

**Dark patterns à éviter** :
- Réduire le contraste du bouton "Non merci" ou "Se désabonner" pour le rendre quasi invisible
- Utiliser un contraste élevé sur des options profitables et faible sur les options favorables à l'utilisateur

---

## Lois comportementales

### 10. Loi de Fitts

**Énoncé** : Le temps pour atteindre une cible est fonction de la distance à parcourir et de la taille de la cible.

**Principe détaillé** : Modèle prédictif du mouvement humain — le temps nécessaire pour se déplacer rapidement vers une zone cible est fonction de la distance à la cible et de sa taille. En UI design, crucial pour le placement et le dimensionnement des éléments interactifs (boutons, liens, contrôles de formulaire). Les éléments importants ou fréquemment utilisés doivent être plus grands et/ou plus proches de la zone de focus attendue.

**Formule** : T = a + b × log₂(2D/W), où D = distance et W = largeur de la cible.

**Exemples source** :
- Boutons importants ("Submit", "Buy Now") plus grands et facilement cliquables
- Contrôles fréquemment utilisés placés aux bords ou coins de l'écran pour un accès facile
- Zone cliquable agrandie pour les petites icônes ou liens
- Interfaces tactiles avec boutons de taille et d'espacement appropriés pour les doigts

**Application** : App de messagerie mobile — placer le bouton envoi dans le coin inférieur droit et le rendre plus grand que les autres éléments. Suit la loi de Fitts en rendant l'action la plus courante rapide et facile, surtout pour les droitiers tenant le téléphone d'une main.

**Bonnes pratiques** :
- Zone cliquable ≥ 44×44px sur mobile, ≥ 32×32px sur desktop
- Espacement entre cibles tactiles ≥ 8px (éviter les erreurs de tap)
- Les bords et coins de l'écran sont des "cibles infinies" (la souris ne peut pas les dépasser)
- Les actions destructrices peuvent être plus petites ET éloignées (protection par la difficulté)
- Regrouper les actions liées proches les unes des autres

**Dark patterns à éviter** :
- Bouton "Fermer la pub" minuscule et dans un coin
- Cible de fermeture intentionnellement petite sur une modale pour forcer l'interaction avec le contenu

---

### 11. Loi de Hick

**Énoncé** : Le temps de décision augmente avec le nombre et la complexité des choix.

**Principe détaillé** : La loi de Hick (ou Hick-Hyman) établit que le temps pour prendre une décision est proportionnel au nombre et à la complexité des choix disponibles. En UI design, ce principe souligne l'importance de la simplicité et de l'organisation. Réduire le nombre de choix ou les organiser efficacement aide les utilisateurs à décider plus vite et réduit la charge cognitive.

**Formule** : T = b × log₂(n + 1), où n = nombre de choix.

**Exemples source** :
- Décomposer les processus complexes en séries d'étapes plus simples
- Progressive disclosure : révéler les options supplémentaires uniquement quand nécessaire
- Organiser les items de menu en catégories logiques pour réduire les choix à chaque niveau
- Simplifier les formulaires en n'affichant que les champs pertinents selon les saisies précédentes

**Application** : App de streaming vidéo — au lieu de présenter tous les films et séries sur l'écran d'accueil, catégoriser le contenu et utiliser un système de recommandation. Réduit le nombre de choix immédiats, facilitant la décision.

**Bonnes pratiques** :
- Maximum 7±2 items au premier niveau de navigation
- Diviser les choix complexes en étapes (progressive disclosure)
- Mettre en avant l'option recommandée ou la plus fréquente
- Grouper les options en catégories logiques (réduit la charge perçue)
- Utiliser des valeurs par défaut intelligentes

**Dark patterns à éviter** :
- Multiplier volontairement les options de refus pour fatiguer l'utilisateur et le pousser à accepter (ex : paramètres de confidentialité avec 50 toggles)
- Confirmshaming : proposer des choix biaisés ("Oui je veux économiser" vs "Non, je préfère payer plus")

---

### 12. Consistance

**Énoncé** : Maintenir la consistance des éléments de design à travers une interface améliore l'utilisabilité et l'attrait esthétique.

**Principe détaillé** : Utilisation uniforme des éléments de design, patterns et comportements à travers une interface. Inclut la consistance visuelle (couleurs, polices, styles de boutons) et la consistance fonctionnelle (comportement identique des éléments similaires). Réduit la charge cognitive — pas besoin de réapprendre chaque section. Contribue aussi à un aspect plus professionnel et soigné.

**4 niveaux de consistance** :
- **Visuelle** : mêmes couleurs, typographies, espacements partout
- **Fonctionnelle** : un même pattern fait toujours la même chose
- **Interne** : cohérence au sein du produit
- **Externe** : cohérence avec les conventions du marché (→ Loi de Jakob)

**Exemples source** :
- Même schéma de couleurs et styles de boutons sur toutes les pages
- Patterns de navigation cohérents à travers l'interface
- Même style d'iconographie pour toutes les icônes
- Actions similaires ("Sauvegarder", "Annuler") toujours au même emplacement sur tous les écrans

**Application** : Suite de productivité avec plusieurs apps (éditeur texte, tableur, présentation) — maintenir les mêmes éléments d'UI à travers toutes les apps (icônes, styles de boutons, layouts de menu) pour que les utilisateurs basculent facilement sans réapprendre l'interface.

**Bonnes pratiques** :
- Documenter un design system (composants, tokens, patterns)
- Auditer régulièrement la consistance entre les écrans
- Une action = un verbe = un style (ex : "Créer" = bouton primary bleu partout)
- Respecter les conventions de la plateforme (iOS, Android, Web)

**Dark patterns à éviter** :
- Changer l'emplacement ou le style du bouton de fermeture selon les écrans
- Inverser l'ordre des boutons (Annuler/OK vs OK/Annuler) pour piéger l'utilisateur

---

### 13. Loi de Jakob

**Énoncé** : Les utilisateurs passent la majorité de leur temps sur d'autres sites ; ils préfèrent que votre site fonctionne comme ceux qu'ils connaissent déjà.

**Principe détaillé** : Nommée d'après l'expert en utilisabilité Jakob Nielsen. Les utilisateurs préfèrent les sites et applications qui fonctionnent de manière similaire à ceux qu'ils connaissent déjà. Ce principe souligne l'importance de suivre les patterns de design et conventions établis. En s'appuyant sur les modèles mentaux existants des utilisateurs, on crée des interfaces plus intuitives nécessitant moins d'apprentissage.

**Exemples source** :
- Menu de navigation principal en haut ou à gauche de la page, où les utilisateurs s'attendent à le trouver
- Icônes standard pour les actions communes (disquette pour "Sauvegarder", engrenage pour "Paramètres")
- Codes couleur conventionnels (rouge = erreur, vert = succès)
- Layouts familiers pour des types spécifiques de sites (pages produit e-commerce, layouts de blog)

**Application** : Site e-commerce — suivre les layouts et interactions conventionnels. Icône panier en haut à droite, sidebar gauche pour la navigation par catégorie, pages produit avec image à gauche et détails à droite. Cette familiarité aide les utilisateurs à naviguer et acheter facilement.

**Bonnes pratiques** :
- Étudier les conventions des outils de référence du secteur (Jira, Notion, Salesforce) avant de designer
- Si on doit dévier d'un standard : fournir un affordance explicite ou un onboarding
- Tester avec des utilisateurs — si > 30% cherchent une fonctionnalité au mauvais endroit, c'est un signal
- L'innovation doit porter sur la valeur, pas sur l'interaction

**Dark patterns à éviter** :
- Placer intentionnellement un pattern à un endroit inhabituel pour que l'utilisateur passe par un chemin commercial
- Cacher les paramètres de compte dans un endroit non standard pour réduire les résiliations

---

## Synthèse : règles opérationnelles

### À appliquer systématiquement

| Règle | Application CMMS |
|-------|-----------------|
| Proximité + White space | Grouper visuellement les champs liés dans les formulaires |
| Hiérarchie typo | Scan en 3 secondes : titre → sous-titre → corps |
| Contraste + Couleur | Un seul CTA primary par écran, statuts par couleur + icône |
| Fitts | Boutons ≥ 44px, actions fréquentes proches du contenu |
| Hick | Maximum 7 options visibles, progressive disclosure |
| Jakob | Respecter les conventions du marché (sidebar, tableaux, formulaires) |
| Consistance | Un composant = un comportement, partout |

### Checklist anti-dark-patterns

- [ ] Les boutons d'action et de refus ont un contraste équitable
- [ ] L'option favorable à l'utilisateur est aussi visible que celle favorable au business
- [ ] Le parcours de désabonnement/annulation est aussi simple que l'inscription
- [ ] Aucune pré-sélection de case à cocher marketing
- [ ] Les compteurs d'urgence ("Plus que 3 places !") reflètent la réalité
- [ ] Le contenu publicitaire est clairement distingué du contenu natif
- [ ] L'ordre des boutons est constant dans toute l'application

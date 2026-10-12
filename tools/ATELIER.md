# Design « Atelier » — landing épurée premium (réutilisable sur toutes les boutiques)

Fond blanc cassé, titres sans-serif gras (Plus Jakarta Sans ; option `"heading_font": "serif"`),
accent doux (`accent`, vert sauge par défaut) et bandes sombres (`accent_dark`, olive foncé par défaut), cartes arrondies.
Même mécanique que le design Salon Pro : un fichier de textes par produit, panneau de commande
COD `#commander` ouvert par tous les boutons `data-order`, barre fixe mobile
« Acheter maintenant · {prix promo} », pixel chargé par la boutique (`{{ content_for_header }}`).

## Sections (dans l'ordre)
Bandeau d'annonce · en-tête (logo, prix, Commander) · hero (titre sur plusieurs lignes, prix, réduction,
galerie à vignettes) · rangée de 4 chiffres clés · 4 cartes à icônes · bande sombre « point fort » avec
4 pictos · 3 avantages en situation (photo + texte) · « Ce que vous recevez » (4 photos) · caractéristiques
· avis clients (seulement s'il y en a de vrais) · 3 étapes de commande · carte offre · FAQ
· appel final sombre avec carte prix · pied de page.

## Nouveau produit
1. Copier `tools/products/_modele-atelier.json` → `tools/products/<produit>.json`.
2. `layout` = `landing-<produit>` (nom unique), `img` = préfixe unique des images (ex. `tens-`).
3. Remplir textes, prix (`price_new`, `price_old`, `price_new_num`, `save_pct`), `accent`.
4. Images dans `assets/` avec le préfixe : hero, 4 vues de galerie, point fort, 3 avantages, 4 « inclus », détails, offre.
   Format conseillé : 1000×1250 (portrait) ou 1200×1200, fonds clairs, sans texte.
5. `python3 tools/build.py <produit>` puis `python3 tools/preview.py landing-<produit>` (aperçu local).
6. Commit + push sur `main`, puis choisir le modèle `landing-<produit>` sur la fiche produit Shopify.

## Utiliser le design sur une autre boutique
Copier dans le dépôt du thème de l'autre boutique : le dossier `tools/` et `sections/mm-cod.liquid`.
Changer `brand`, `logo_file`, `accent`, `currency`, la zone de livraison dans les textes,
puis construire comme ci-dessus. Le reste du thème de la boutique n'est pas touché.

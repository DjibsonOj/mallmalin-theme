# Design « Atelier » — landing épurée premium (réutilisable sur toutes les boutiques)

Fond blanc, typographie serif élégante (Cormorant Garamond + Manrope), couleur d'accent sobre.
Même mécanique que le design Salon Pro : un fichier de textes par produit, panneau de commande
COD `#commander` ouvert par tous les boutons `data-order`, barre fixe mobile
« Acheter maintenant · {prix promo} », pixel chargé par la boutique (`{{ content_for_header }}`).

## Sections (dans l'ordre)
Bandeau d'annonce · en-tête (logo, prix, Commander) · hero (titre, prix, réduction, galerie à vignettes)
· 4 garanties · phrase d'accroche · 3 avantages (image + texte en alternance) · caractéristiques
· 3 étapes de commande · carte offre (contenu du colis + prix) · avis clients (seulement s'il y en a
de vrais) · FAQ · appel final · pied de page.

## Nouveau produit
1. Copier `tools/products/_modele-atelier.json` → `tools/products/<produit>.json`.
2. `layout` = `landing-<produit>` (nom unique), `img` = préfixe unique des images (ex. `tens-`).
3. Remplir textes, prix (`price_new`, `price_old`, `price_new_num`, `save_pct`), `accent`.
4. Images dans `assets/` avec le préfixe : hero, 4 vues de galerie, 3 avantages, détails, offre.
   Format conseillé : 1000×1250 (portrait) ou 1200×1200, fonds clairs, sans texte.
5. `python3 tools/build.py <produit>` puis `python3 tools/preview.py landing-<produit>` (aperçu local).
6. Commit + push sur `main`, puis choisir le modèle `landing-<produit>` sur la fiche produit Shopify.

## Utiliser le design sur une autre boutique
Copier dans le dépôt du thème de l'autre boutique : le dossier `tools/` et `sections/mm-cod.liquid`.
Changer `brand`, `logo_file`, `accent`, `currency`, la zone de livraison dans les textes,
puis construire comme ci-dessus. Le reste du thème de la boutique n'est pas touché.

# Design « Élan » — landing dynamique (réutilisable sur toutes les boutiques)

Même palette et mêmes cartes que le design Atelier, avec une couche de mouvement :
titre du hero qui monte ligne par ligne, photo dans une forme vivante qui ondule, pastilles
flottantes, compteurs animés, bandeau défilant, apparitions en cascade, parallaxe douce,
barre de progression de lecture et bouton final qui pulse. Si le téléphone du client demande
moins d'animations (réglage « mouvement réduit »), tout s'affiche sans bouger.

Mécanique identique : un fichier par produit, panneau COD `#commander` ouvert par tous les
boutons `data-order`, barre mobile « Acheter maintenant · {prix promo} », pixel de la boutique.

## Sections (dans l'ordre)
Bandeau d'annonce · en-tête · hero (titre animé, prix, bouton, vidéo facultative, photo dans
une forme vivante + 2 pastilles) · 4 chiffres clés animés · bandeau défilant · 4 cartes à icônes
· « Ce que vous recevez » (4 photos) · bande sombre « point fort » avec 4 pictos · avis clients
(seulement s'il y en a de vrais) · lifestyle (texte + 3 photos en parallaxe) · 3 étapes · FAQ
· appel final (texte + photo + carte prix) · pied de page.

## Nouveau produit
1. Copier `tools/products/_modele-elan.json` → `tools/products/<produit>.json`.
2. `layout` = `landing-<produit>` (nom unique), `img` = préfixe unique des images (ex. `tens-`).
3. Remplir textes, prix (`price_new`, `price_old`, `price_new_num`, `save_pct`), couleurs (`accent`, `accent_dark`).
4. Images dans `assets/` avec le préfixe : hero, 4 « inclus », point fort, 3 lifestyle, final. Sans texte incrusté.
5. Vidéo (facultatif) : `video_url` = lien YouTube « embed » ou fichier .mp4 déposé dans `assets/`. Vide = pas de bouton.
6. `python3 tools/build.py <produit>` puis `python3 tools/preview.py landing-<produit>` (aperçu local).
7. Commit + push sur `main`, puis choisir le modèle `landing-<produit>` sur la fiche produit Shopify.

Autre boutique : copier `tools/` et `sections/mm-cod.liquid` dans son thème (voir `tools/ATELIER.md`).

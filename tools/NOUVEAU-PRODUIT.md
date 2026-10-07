# Ajouter la landing d'un nouveau produit

Le design (style Salon Pro, animations, barre fixe, panneau de commande COD) ne change jamais :
il est dans `tools/landing.template.liquid`. Chaque produit = **un fichier de textes** + **ses images**.

1. Copier `tools/products/_modele.json` vers `tools/products/<produit>.json`.
2. Mettre dans `layout` un nom unique, ex. `landing-tensio` (jamais `landing`, réservé aux écouteurs).
3. Remplacer les textes (titre, 5 angles, étapes, prix `price_new` / `price_old` / `price_new_num`, `fig_val` = % de réduction).
4. Ajouter les images dans `assets/` avec un préfixe unique (`img`, ex. `tens-`) :
   `hero.jpg, hook.jpg, process.jpg, logo.jpg, f1..f10.jpg (flottantes), t1..t12.jpg (traînée)` + 5 visuels d'angles (champ `image` de chaque carte).
5. `python3 tools/build.py <produit>` → écrit `layout/<layout>.liquid` et `templates/product.<layout>.json`.
6. Commit + push sur `main` : Shopify se met à jour. Sur la fiche produit, choisir le modèle `landing-<produit>`.

Les prix sont écrits dans le fichier produit (pas lus depuis Shopify) : on les change à cet endroit, puis on relance le build.

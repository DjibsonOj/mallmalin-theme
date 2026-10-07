# Projet : landings produit MallMalin (Shopify, paiement à la livraison)

Ce dépôt est le thème Shopify de la boutique MallMalin (Conakry, Guinée, prix en GNF). Il sert **uniquement** à
créer et modifier les landings produit. Réponds toujours en français, simplement : le propriétaire (Jibrail) n'est pas développeur
et travaille surtout sur téléphone.

## Ce que tu fais quand il soumet un nouveau produit
1. Lis `tools/NOUVEAU-PRODUIT.md` et `tools/products/_modele.json`.
2. Demande en une seule fois ce qui manque : nom, prix promo et prix barré, public cible, bénéfices, photos, couleurs/variantes.
3. Écris le copywriting adapté au produit (pas une copie des écouteurs) : accroche, 5 angles marketing, 3 étapes, offre, objections, SEO (titre, description, JSON-LD).
4. Prépare les images avec un préfixe unique (hero, hook, process, logo, f1–f10, t1–t12, 5 visuels d'angles), visuels sans texte.
5. Crée `tools/products/<produit>.json`, lance `python3 tools/build.py <produit>`, vérifie le rendu (Playwright, bureau + mobile).
6. Commit + push sur `main` : Shopify se synchronise tout seul. Dis-lui de choisir le modèle `landing-<produit>` sur la fiche produit.
Pour changer un prix ou un texte : modifier le JSON du produit puis relancer le build. Ne jamais éditer à la main `layout/landing*.liquid` (généré).

## Règles à ne jamais enfreindre
- Ne pas toucher au reste du thème ni aux autres produits : seuls `layout/landing*.liquid`, `templates/product.landing*.json`, `assets/<préfixe>-*`, `tools/` changent.
- La landing des écouteurs (`layout: landing`, `tools/products/earbuds.json`) reste telle quelle sauf demande explicite.
- Aucun pixel Facebook ni Formspree dans les fichiers : le pixel vient de la boutique via `{{ content_for_header }}`.
- Le formulaire COD (app EasySell, bloc d'app) s'affiche dans le panneau `#commander` ouvert par tous les boutons `data-order` ; le panneau ne doit jamais avoir de `transform` ouvert (sinon les pop-ups de l'app disparaissent).
- Bouton flottant « Acheter maintenant · {prix promo} » = prix promo uniquement. Mobile d'abord. Textes en français.
- Personnages des visuels de famille/entreprise/école : personnes noires africaines.

## Contexte technique
- `tools/landing.template.liquid` = design Salon Pro (moteur d'animation, barre fixe avec prix, panneau COD). Ne le modifier que pour un changement de design valable pour tous les produits, puis régénérer **tous** les produits (`python3 tools/build.py`) et vérifier que chacun reste correct.
- Les prix sont écrits dans le JSON (`price_new`, `price_old`, `price_new_num`, `fig_val` = % de réduction).
- Taille limite d'un fichier Liquid Shopify : ~256 Ko.
- Tests : Python Playwright, chromium `/opt/pw-browsers/chromium`, `args=['--no-sandbox']` ; en local, retirer les balises Liquid et mapper `asset_url` vers `assets/`.

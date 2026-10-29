# Projet : landings produit AFRIBAZAAR (Shopify, paiement à la livraison) — branche `afribazaar`

Cette branche `afribazaar` est le thème Shopify de la boutique **Afribazaar** (la branche `main` = MallMalin : ne jamais y pousser de travail Afribazaar, et inversement). Il sert **uniquement** à
créer et modifier les landings produit. Réponds toujours en français, simplement : le propriétaire (Jibrail) n'est pas développeur
et travaille surtout sur téléphone.

## Ce que tu fais quand il soumet un nouveau produit
1. Lis `tools/ELAN.md` ou `tools/ATELIER.md` et le modèle correspondant (`tools/products/_modele-elan.json` / `_modele-atelier.json`).
2. Demande en une seule fois ce qui manque : nom, prix promo et prix barré, public cible, bénéfices, photos, couleurs/variantes.
3. Écris le copywriting adapté au produit (pas une copie des écouteurs) : accroche, 5 angles marketing, 3 étapes, offre, objections, SEO (titre, description, JSON-LD).
4. Prépare les images avec un préfixe unique (hero, hook, process, logo, f1–f10, t1–t12, 5 visuels d'angles), visuels sans texte.
5. Crée `tools/products/<produit>.json`, lance `python3 tools/build.py <produit>`, vérifie le rendu (Playwright, bureau + mobile).
6. Commit + push sur `afribazaar` : Shopify se synchronise tout seul. Dis-lui de choisir le modèle `landing-<produit>` sur la fiche produit.
Pour changer un prix ou un texte : modifier le JSON du produit puis relancer le build. Ne jamais éditer à la main `layout/landing*.liquid` (généré).

## Règles à ne jamais enfreindre
- Ne pas toucher au reste du thème ni aux autres produits : seuls `layout/landing*.liquid`, `templates/product.landing*.json`, `assets/<préfixe>-*`, `tools/` changent.
- Pour Afribazaar, utiliser les designs **Atelier** ou **Élan** (le design Salon Pro contient encore le nom MallMalin en dur).
- Marque `Afribazaar`, logo `assets/ab-logo.png`, préfixe d'images `ab-<produit>-`. Ville et devise : à confirmer avec Jibrail avant le premier produit.
- Logo : toujours adapté aux couleurs de la page produit (automatique dans Sur-Mesure avec un logo horizontal, voir `tools/SURMESURE.md`).
- Aucun pixel Facebook ni Formspree dans les fichiers : le pixel vient de la boutique via `{{ content_for_header }}`.
- Le formulaire COD (app EasySell, bloc d'app) s'affiche dans le panneau `#commander` ouvert par tous les boutons `data-order` ; le panneau ne doit jamais avoir de `transform` ouvert (sinon les pop-ups de l'app disparaissent).
- Bouton flottant « Acheter maintenant · {prix promo} » = prix promo uniquement. Mobile d'abord. Textes en français.
- Personnages des visuels de famille/entreprise/école : personnes noires africaines.

## Contexte technique
- Quatre designs : **Sur-Mesure** (adapté au produit, 7 styles, `"template": "surmesure"`, modèle `tools/products/_modele-surmesure.json`, doc `tools/SURMESURE.md` — à privilégier pour Afribazaar), Salon Pro, **Atelier** (épuré premium, `"template": "atelier"`, modèle `tools/products/_modele-atelier.json`, doc `tools/ATELIER.md`) et **Élan** (dynamique, `"template": "elan"`, modèle `tools/products/_modele-elan.json`, doc `tools/ELAN.md`). Sur-Mesure, Atelier et Élan sont des créations originales : ne pas les transformer en copie d'un design tiers.
- Ne jamais inventer : avis, caractéristiques, certifications, prix barré, stock limité ou compte à rebours. Sans donnée réelle, l'élément reste vide (il est alors masqué).
- Aperçu local : `python3 tools/preview.py <layout>` → `preview/` (ignoré par git).
- `tools/landing.template.liquid` = design Salon Pro (moteur d'animation, barre fixe avec prix, panneau COD). Ne le modifier que pour un changement de design valable pour tous les produits, puis régénérer **tous** les produits (`python3 tools/build.py`) et vérifier que chacun reste correct.
- Les prix sont écrits dans le JSON (`price_new`, `price_old`, `price_new_num`, `fig_val` = % de réduction).
- Taille limite d'un fichier Liquid Shopify : ~256 Ko.
- Tests : Python Playwright, chromium `/opt/pw-browsers/chromium`, `args=['--no-sandbox']` ; en local, retirer les balises Liquid et mapper `asset_url` vers `assets/`.

# Design « Sur-Mesure » — une landing adaptée à chaque produit

Un socle commun (formulaire COD `#commander`, barre mobile « Acheter maintenant · {prix promo} »,
pixel de la boutique) + **un style visuel** + **les sections utiles au produit, dans l'ordre voulu**.

## Les 7 styles (`"style"`)
| style | pour | ambiance |
|---|---|---|
| `tech` | électronique, gadgets | fond sombre, accent cyan, grille lumineuse |
| `beaute` | soins, cosmétiques | crème et rose, serif élégante, photo en arche |
| `sante` | santé, bien-être, tensiomètre | bleu et blanc, net et rassurant |
| `maison` | maison, cuisine | beige chaud, terracotta, serif douce |
| `mode` | mode, accessoires | noir et blanc éditorial, angles droits, photo plein écran |
| `sport` | sport, auto, outdoor | noir et vert fluo, titres capitales condensées |
| `enfants` | jouets, enfants | couleurs gaies, formes rondes |

Options : `hero_layout` (`split`, `centered`, `overlay`), `hero_fit` (`cover` ou `contain` pour un
produit détouré), `colors` pour changer n'importe quelle couleur (ex. `{"accent": "#1f6feb"}`).

## Les sections (`"sections"`, toutes facultatives, dans l'ordre de la liste)
`trust` réassurance · `stats` chiffres animés · `marquee` bandeau défilant · `problem` problème → solution
· `benefits` cartes à icônes · `showcase` photo/texte alternés · `demo` étapes d'utilisation
· `gallery` galerie · `beforeafter` avant/après à glisser · `specs` caractéristiques · `compare` tableau
de versions · `included` contenu du colis · `reviews` avis · `offer` offre · `faq` · `cta` appel final.
`"nav": "Libellé"` sur une section l'ajoute au menu (5 maximum).

## Règle : rien d'inventé
Une section ou un élément sans donnée réelle ne s'affiche pas :
- `reviews` vide → pas de section avis (uniquement de vrais avis clients) ;
- une ligne de `specs` sans valeur → ligne masquée ;
- `price_old` vide → pas de prix barré ni de % ;
- `ends_at` vide ou date passée → pas de compte à rebours (sinon vraie date de fin, ex. `2026-11-30T23:59:00Z`).

## Nouveau produit
1. Copier `tools/products/_modele-surmesure.json` → `tools/products/<produit>.json`.
2. Choisir le style, remplir textes et prix, garder seulement les sections utiles.
3. Images dans `assets/` avec le préfixe `img` (ex. `ab-tensio-hero.jpg`).
4. `python3 tools/build.py <produit>` puis `python3 tools/preview.py landing-<produit>`.
5. Commit + push sur `afribazaar`, puis choisir le modèle `landing-<produit>` sur la fiche produit.

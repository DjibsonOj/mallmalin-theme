# Installation — Landing MallMalin (Shopify)

Fichiers :
- layout/landing.liquid  (la page complète : design, animations, contenu)
- templates/product.landing.json  (template produit qui utilise ce layout)
- sections/mm-cod.liquid  (zone de commande : formulaire produit + blocs d'app COD)
- assets/ (30 images mm-*.jpg)

1. Boutique en ligne > Thèmes > ... > Dupliquer (sauvegarde) puis Modifier le code.
2. Assets > Ajouter un nouvel asset : importez les 30 images du dossier assets/.
3. Layout > Ajouter un layout « landing » : collez layout/landing.liquid.
4. Sections > Ajouter une section « mm-cod » : collez sections/mm-cod.liquid.
5. Templates > Ajouter un template produit, type JSON, nom « landing » : collez product.landing.json.
6. Produits > votre kit > Modèle de thème : « product.landing ». Prix produit = 250 000, prix comparé = 450 000.
7. Installez votre app COD : soit elle se greffe sur le bouton « Commander maintenant » du bas, soit
   Personnaliser le thème > page produit landing > section « Commande COD » > Ajouter un bloc > votre app.
8. Pixel : aucun code ici. Connectez le pixel via Facebook & Instagram (canal Shopify) ou Paramètres > Événements clients.
9. Prix affichés : 4 lignes assign en haut de layout/landing.liquid (mm_new, mm_old, mm_cur, mm_new_num).
10. Couleur d'accent : variable --lime (or #e0b04a) dans le CSS.

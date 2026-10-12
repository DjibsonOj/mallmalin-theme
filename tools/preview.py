#!/usr/bin/env python3
"""Aperçu local d'une landing générée (sans Shopify).

Usage :  python3 tools/preview.py landing-atelier-ecouteurs
Écrit :  preview/<layout>.html  (ouvrir dans un navigateur ; dossier ignoré par Shopify)
Les balises Liquid sont remplacées : asset_url → assets/, prix → valeurs du layout,
formulaire COD → faux formulaire de démonstration.
"""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def render(layout):
    src = open(os.path.join(ROOT, 'layout', layout + '.liquid'), encoding='utf-8').read()
    vars_ = dict(re.findall(r"\{%-? assign (\w+) = '([^']*)' -?%\}", src))
    src = re.sub(r'\{%-? comment -?%\}.*?\{%-? endcomment -?%\}', '', src, flags=re.S)
    src = re.sub(r"\{%-? assign [^%]*%\}", '', src)
    src = re.sub(r"\{\{ '([^']+)' \| asset_url \}\}", r'../assets/\1', src)
    src = src.replace('https:../assets/', '../assets/')
    src = src.replace('{{ content_for_header }}', '')
    src = src.replace('{{ canonical_url }}', '#')
    src = src.replace("{{ 'now' | date: '%Y' }}", '2026')
    fake = ('<div class="mm-native"><p class="mm-title">Formulaire de commande (aperçu)</p>'
            '<label>Nom complet</label><select><option>— zone de l’app COD —</option></select>'
            '<button class="btn-order" type="button">Commander maintenant</button></div>')
    src = src.replace('{{ content_for_layout }}', fake)
    for k, v in vars_.items():
        src = src.replace('{{ %s }}' % k, v)
    left = re.findall(r'\{\{.*?\}\}|\{%.*?%\}', src)
    if left: print('⚠ Liquid restant :', left[:5])
    os.makedirs(os.path.join(ROOT, 'preview'), exist_ok=True)
    out = os.path.join(ROOT, 'preview', layout + '.html')
    open(out, 'w', encoding='utf-8').write(src)
    print('OK ', out)
    return out

if __name__ == '__main__':
    for l in sys.argv[1:]: render(l)

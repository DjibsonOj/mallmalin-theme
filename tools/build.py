#!/usr/bin/env python3
"""Génère la landing d'un produit à partir de tools/products/<nom>.json

Usage :  python3 tools/build.py earbuds          (un produit)
         python3 tools/build.py                  (tous les produits)

Écrit :  layout/<layout>.liquid  et  templates/product.<layout>.json
"""
import json, os, re, sys, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = open(os.path.join(ROOT, 'tools', 'landing.template.liquid'), encoding='utf-8').read()

def asset(name): return "{{ '%s' | asset_url }}" % name
def esc_js(t): return t.replace('\\', '\\\\').replace("'", "\\'")

def card(c, pref):
    img = c['image'] if c['image'].endswith('.jpg') else c['image'] + '.jpg'
    return ('<figure class="card b-%s" style="--pos:%s"><div class="card-img"><img src="%s" alt="%s" loading="lazy"></div>'
            '<figcaption>%s<span class="mono">%s</span></figcaption><p class="card-desc">%s</p>'
            '<p class="card-cta"><a class="btn-order" href="#commander" data-order>Commander maintenant</a></p></figure>'
            % (c['size'], c['pos'], asset(pref + img), c['alt'], c['title'], c['meta'], c['desc']))

def build(name):
    cfg = json.load(open(os.path.join(ROOT, 'tools', 'products', name + '.json'), encoding='utf-8'))
    pref = cfg['img']
    out = TPL
    cfg = dict(cfg)
    cfg['cards'] = '\n'.join(card(c, pref) for c in cfg['cards'])
    cfg['spot_intro_html'] = ' '.join('<span>%s</span>' % w for w in cfg['spot_intro'].split())
    for i in (1, 2, 3):
        cfg['motto_h%d' % i] = esc_js(cfg['motto_h%d' % i])
    for k, v in cfg.items():
        if isinstance(v, str):
            out = out.replace('[[%s]]' % k, v)
    left = set(re.findall(r'\[\[(\w+)\]\]', out))
    if left: sys.exit('Clés manquantes dans %s.json : %s' % (name, sorted(left)))
    # images attendues
    missing = sorted({m for m in re.findall(r"'([^']+\.jpg)' \| asset_url", out)
                      if not os.path.exists(os.path.join(ROOT, 'assets', m))})
    if missing: print('⚠ images absentes de assets/ :', ', '.join(missing))
    lay = cfg['layout']
    open(os.path.join(ROOT, 'layout', lay + '.liquid'), 'w', encoding='utf-8').write(out)
    tp = {"layout": lay, "sections": {"cod": {"type": "mm-cod", "blocks": {}, "block_order": [], "settings": {}}}, "order": ["cod"]}
    open(os.path.join(ROOT, 'templates', 'product.%s.json' % lay), 'w', encoding='utf-8').write(json.dumps(tp, indent=2))
    print('OK  layout/%s.liquid  (%d Ko)  +  templates/product.%s.json' % (lay, len(out.encode()) // 1024, lay))

names = sys.argv[1:] or [os.path.basename(p)[:-5] for p in glob.glob(os.path.join(ROOT, 'tools', 'products', '*.json')) if not os.path.basename(p).startswith('_')]
for n in names: build(n)

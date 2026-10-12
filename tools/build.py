#!/usr/bin/env python3
"""Génère la landing d'un produit à partir de tools/products/<nom>.json

Usage :  python3 tools/build.py earbuds          (un produit)
         python3 tools/build.py                  (tous les produits)

Écrit :  layout/<layout>.liquid  et  templates/product.<layout>.json

Design : "template": "atelier" dans le JSON produit → design épuré premium
         (tools/landing-atelier.template.liquid) ; sinon design Salon Pro.
"""
import json, os, re, sys, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = open(os.path.join(ROOT, 'tools', 'landing.template.liquid'), encoding='utf-8').read()
TPL_ATELIER = open(os.path.join(ROOT, 'tools', 'landing-atelier.template.liquid'), encoding='utf-8').read()

def asset(name): return "{{ '%s' | asset_url }}" % name
def esc_js(t): return t.replace('\\', '\\\\').replace("'", "\\'")

def card(c, pref):
    img = c['image'] if c['image'].endswith('.jpg') else c['image'] + '.jpg'
    return ('<figure class="card b-%s" style="--pos:%s"><div class="card-img"><img src="%s" alt="%s" loading="lazy"></div>'
            '<figcaption>%s<span class="mono">%s</span></figcaption><p class="card-desc">%s</p>'
            '<p class="card-cta"><a class="btn-order" href="#commander" data-order>Commander maintenant</a></p></figure>'
            % (c['size'], c['pos'], asset(pref + img), c['alt'], c['title'], c['meta'], c['desc']))

# ─────────────── design « Atelier » (épuré premium) ───────────────
ICONS = {
 'truck': '<path d="M2 6h11v9H2zM13 9h4l3 3v3h-7z"/><circle cx="6" cy="17" r="1.8"/><circle cx="16.5" cy="17" r="1.8"/>',
 'cash': '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2.6"/><path d="M6 9.5v5M18 9.5v5"/>',
 'shield': '<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><path d="M8.8 12l2.2 2.2 4.2-4.4"/>',
 'phone': '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a1 1 0 01-1 1A16 16 0 014 5a1 1 0 011-1z"/>',
 'box': '<path d="M3 7.5L12 3l9 4.5v9L12 21l-9-4.5z"/><path d="M3 7.5l9 4.5 9-4.5M12 12v9"/>',
 'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'star': '<path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8-4.3-4.1 5.9-.9z"/>',
 'leaf': '<path d="M5 19c0-8 5-13 15-14-1 10-6 15-14 15"/><path d="M5 19l7-7"/>',
 'heart': '<path d="M12 20s-7-4.4-7-10a4 4 0 017-2.6A4 4 0 0119 10c0 5.6-7 10-7 10z"/>',
}
TICK = '<span class="tick"><svg viewBox="0 0 12 12" fill="none" stroke-width="2"><path d="M2.5 6.2l2.4 2.3 4.6-5"/></svg></span>'

def jpg(n): return n if n.endswith('.jpg') or n.endswith('.png') or n.endswith('.webp') else n + '.jpg'

def build_atelier(cfg):
    pref = cfg['img']
    c = dict(cfg)
    c.setdefault('accent', '#8c7b65')
    c.setdefault('currency_iso', 'GNF' if c.get('currency') == 'GNF' else c.get('currency', 'XOF'))
    c['hero_image'] = jpg(c['hero_image'])
    c['details_image'] = jpg(c['details_image'])
    c['offer_image'] = jpg(c['offer_image'])
    c['hero_points_html'] = '\n'.join('            <li>%s<span>%s</span></li>' % (TICK, p) for p in cfg['hero_points'])
    gal = [g for g in cfg['gallery']]
    c['thumbs_html'] = '\n'.join(
        '            <button type="button" aria-current="%s" data-src="%s" data-alt="%s" aria-label="Photo %d">'
        '<img src="%s" alt="" loading="lazy" width="200" height="200"></button>'
        % ('true' if i == 0 else 'false', asset(pref + jpg(g['image'])), g['alt'], i + 1, asset(pref + jpg(g['image'])))
        for i, g in enumerate(gal))
    c['trust_html'] = '\n'.join(
        '          <li><svg viewBox="0 0 24 24" aria-hidden="true">%s</svg><div><b>%s</b><span>%s</span></div></li>'
        % (ICONS.get(t['icon'], ICONS['star']), t['title'], t['text']) for t in cfg['trust'])
    c['benefits_html'] = '\n'.join(
        '        <article class="benefit">\n'
        '          <div class="b-media rv"><img src="%s" alt="%s" loading="lazy"></div>\n'
        '          <div class="b-copy rv"><span class="b-num">%02d — %s</span><h3 class="serif">%s</h3><p>%s</p>'
        '<a class="btn btn-line" href="#commander" data-order>Commander</a></div>\n'
        '        </article>'
        % (asset(pref + jpg(b['image'])), b['alt'], i + 1, b['kicker'], b['title'], b['text'])
        for i, b in enumerate(cfg['benefits']))
    c['specs_html'] = '\n'.join('            <li><span>%s</span><b>%s</b></li>' % (s['label'], s['value']) for s in cfg['specs'])
    c['steps_html'] = '\n'.join(
        '          <div class="step rv"><span class="step-n">%d</span><h3 class="serif">%s</h3><p>%s</p></div>'
        % (i + 1, s['title'], s['text']) for i, s in enumerate(cfg['steps']))
    c['included_html'] = '\n'.join('              <li>%s<span>%s</span></li>' % (TICK, x) for x in cfg['included'])
    c['faq_html'] = '\n'.join(
        '          <details><summary>%s<i aria-hidden="true"></i></summary><p class="a">%s</p></details>' % (q['q'], q['a'])
        for q in cfg['faq'])
    # avis : uniquement de vrais avis clients fournis par le marchand ; sinon la section disparaît
    revs = [r for r in cfg.get('reviews', []) if r.get('text')]
    if revs:
        c['reviews_section'] = (
            '    <section class="sec" id="avis" style="padding-top:0">\n      <div class="wrap">\n'
            '        <div class="sec-head rv"><p class="kicker">Avis clients</p><h2 class="serif h2">%s</h2></div>\n'
            '        <div class="reviews">\n%s\n        </div>\n      </div>\n    </section>'
            % (cfg.get('reviews_title', 'Ils l’ont reçu chez eux'),
               '\n'.join('          <figure class="review rv"><span class="stars" aria-label="%d sur 5">%s</span><p>%s</p><cite>%s</cite></figure>'
                         % (r.get('stars', 5), '★' * r.get('stars', 5), r['text'], r['name']) for r in revs)))
    else:
        c['reviews_section'] = ''
    out = TPL_ATELIER
    for k, v in c.items():
        if isinstance(v, str):
            out = out.replace('[[%s]]' % k, v)
    return out

def build(name):
    cfg = json.load(open(os.path.join(ROOT, 'tools', 'products', name + '.json'), encoding='utf-8'))
    if cfg.get('template') == 'atelier':
        return finish(name, cfg, build_atelier(cfg))
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
    finish(name, cfg, out)

def finish(name, cfg, out):
    left = set(re.findall(r'\[\[(\w+)\]\]', out))
    if left: sys.exit('Clés manquantes dans %s.json : %s' % (name, sorted(left)))
    # images attendues
    missing = sorted({m for m in re.findall(r"'([^']+\.(?:jpg|png|webp))' \| asset_url", out)
                      if not os.path.exists(os.path.join(ROOT, 'assets', m))})
    if missing: print('⚠ images absentes de assets/ :', ', '.join(missing))
    lay = cfg['layout']
    open(os.path.join(ROOT, 'layout', lay + '.liquid'), 'w', encoding='utf-8').write(out)
    tp = {"layout": lay, "sections": {"cod": {"type": "mm-cod", "blocks": {}, "block_order": [], "settings": {}}}, "order": ["cod"]}
    open(os.path.join(ROOT, 'templates', 'product.%s.json' % lay), 'w', encoding='utf-8').write(json.dumps(tp, indent=2))
    print('OK  layout/%s.liquid  (%d Ko)  +  templates/product.%s.json' % (lay, len(out.encode()) // 1024, lay))

names = sys.argv[1:] or [os.path.basename(p)[:-5] for p in glob.glob(os.path.join(ROOT, 'tools', 'products', '*.json')) if not os.path.basename(p).startswith('_')]
for n in names: build(n)

#!/usr/bin/env python3
"""Génère la landing d'un produit à partir de tools/products/<nom>.json

Usage :  python3 tools/build.py earbuds          (un produit)
         python3 tools/build.py                  (tous les produits)

Écrit :  layout/<layout>.liquid  et  templates/product.<layout>.json

Design : "template": "atelier" → épuré premium (tools/landing-atelier.template.liquid)
         "template": "elan"    → dynamique (tools/landing-elan.template.liquid)
         "template": "surmesure" → adapté au produit, 7 styles (tools/surmesure.py)
         sinon design Salon Pro.
"""
import json, os, re, sys, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = open(os.path.join(ROOT, 'tools', 'landing.template.liquid'), encoding='utf-8').read()
TPL_ATELIER = open(os.path.join(ROOT, 'tools', 'landing-atelier.template.liquid'), encoding='utf-8').read()
TPL_ELAN = open(os.path.join(ROOT, 'tools', 'landing-elan.template.liquid'), encoding='utf-8').read()
TPL_SURMESURE = open(os.path.join(ROOT, 'tools', 'landing-surmesure.template.liquid'), encoding='utf-8').read()
sys.path.insert(0, os.path.join(ROOT, 'tools'))

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
 'battery': '<rect x="2.5" y="7" width="17" height="10" rx="2"/><path d="M21.5 10.5v3M6 10v4M9.5 10v4M13 10v4"/>',
 'bolt': '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
 'bluetooth': '<path d="M7 7l10 10-5 4V3l5 4L7 17"/>',
 'music': '<path d="M9 18V5l11-2v13"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="17.5" cy="16" r="2.5"/>',
 'headphones': '<path d="M4 15v-3a8 8 0 0116 0v3"/><rect x="3" y="14" width="4" height="6" rx="1.5"/><rect x="17" y="14" width="4" height="6" rx="1.5"/>',
 'users': '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.2c2.8.3 5 2.6 5 5.8"/>',
 'gift': '<rect x="3" y="9" width="18" height="4" rx="1"/><path d="M5 13v8h14v-8M12 9v12M12 9c-2-4-6-4-6-1.5S10 9 12 9zm0 0c2-4 6-4 6-1.5S14 9 12 9z"/>',
 'building': '<path d="M4 21V5l8-2v18M12 8h8v13M2 21h20M7 8h2M7 12h2M7 16h2M15 12h2M15 16h2"/>',
 'school': '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2.5 9 2.5 12 0v-5"/>',
 'pin': '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0114 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
 'bag': '<path d="M5 8h14l-1 13H6z"/><path d="M9 8V6a3 3 0 016 0v2"/>',
 'sparkle': '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M18 6l-2.5 2.5M8.5 15.5L6 18"/>',
 'moon': '<path d="M20 14.5A8 8 0 019.5 4 8 8 0 1020 14.5z"/>',
 'feather': '<path d="M20 4c-8 0-14 6-14 14v2"/><path d="M6 14h7M9 10h7"/>',
}
TICK = '<span class="tick"><svg viewBox="0 0 12 12" fill="none" stroke-width="2"><path d="M2.5 6.2l2.4 2.3 4.6-5"/></svg></span>'

def svg(name): return '<svg viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % ICONS.get(name, ICONS['star'])
def jpg(n): return n if n.endswith(('.jpg', '.png', '.webp')) else n + '.jpg'

def build_atelier(cfg, tpl=None):
    pref = cfg['img']
    c = dict(cfg)
    c.setdefault('accent', '#c9d1b9')
    c.setdefault('accent_dark', '#2f362b')
    c.setdefault('currency_iso', c.get('currency', 'XOF'))
    serif = c.get('heading_font') == 'serif'
    c['font_class'] = 'f-serif' if serif else ''
    c['font_extra'] = '&family=Cormorant+Garamond:wght@500;600' if serif else ''
    c['cash_icon'] = svg('cash')
    for k in ('hero_image', 'details_image', 'offer_image', 'highlight_image'):
        if k in c: c[k] = jpg(c[k])
    # titre du hero : une ligne par élément, *mot* = mis en couleur
    c['hero_title_html'] = ''.join('<span>%s</span>' % re.sub(r'\*(.+?)\*', r'<em>\1</em>', l) for l in cfg['hero_title_lines'])
    c['thumbs_html'] = '\n'.join(
        '            <button type="button" aria-current="%s" data-src="%s" data-alt="%s" aria-label="Photo %d">'
        '<img src="%s" alt="" loading="lazy" width="200" height="200"></button>'
        % ('true' if i == 0 else 'false', asset(pref + jpg(g['image'])), g['alt'], i + 1, asset(pref + jpg(g['image'])))
        for i, g in enumerate(cfg.get('gallery', [])))
    def stat_val(v):
        m = re.match(r'^(\d+(?:[.,]\d+)?)(.*)$', v)
        if not m: return '<b>%s</b>' % v
        return '<b><span data-count="%s" data-suffix="%s">%s</span></b>' % (m.group(1), m.group(2).replace('"', '&quot;'), v)
    c['stats_html'] = '\n'.join(
        '          <li><span class="ico">%s</span><div>%s<span>%s</span></div></li>' % (svg(t['icon']), stat_val(t['value']), t['label'])
        for t in cfg['stats'])
    c['features_html'] = '\n'.join(
        '          <div class="feat rv"><span class="ico">%s</span><h3>%s</h3><p>%s</p></div>' % (svg(f['icon']), f['title'], f['text'])
        for f in cfg['features'])
    c['badges_html'] = '\n'.join(
        '            <li><span class="ico">%s</span>%s</li>' % (svg(b['icon']), b['label']) for b in cfg['highlight_badges'])
    c['benefits_html'] = '\n'.join(
        '        <article class="benefit">\n'
        '          <div class="b-media rv"><img src="%s" alt="%s" loading="lazy"></div>\n'
        '          <div class="b-copy rv"><span class="b-num">%02d · %s</span><h3 class="h">%s</h3><p>%s</p>'
        '<a class="btn btn-line" href="#commander" data-order>Commander</a></div>\n'
        '        </article>'
        % (asset(pref + jpg(b['image'])), b['alt'], i + 1, b['kicker'], b['title'], b['text'])
        for i, b in enumerate(cfg.get('benefits', [])))
    c['incl_html'] = '\n'.join(
        '          <figure class="rv"><div class="im"><img src="%s" alt="%s" loading="lazy"></div><figcaption>%s</figcaption></figure>'
        % (asset(pref + jpg(x['image'])), x['label'], x['label']) for x in cfg['incl_items'])
    c['specs_html'] = '\n'.join('            <li><span>%s</span><b>%s</b></li>' % (s['label'], s['value']) for s in cfg.get('specs', []))
    c['steps_html'] = '\n'.join(
        '          <div class="step rv"><span class="step-n">%d</span><h3 class="h">%s</h3><p>%s</p></div>'
        % (i + 1, s['title'], s['text']) for i, s in enumerate(cfg['steps']))
    c['included_html'] = '\n'.join('              <li>%s<span>%s</span></li>' % (TICK, x) for x in cfg.get('included', []))
    c['faq_html'] = '\n'.join(
        '          <details><summary>%s<i aria-hidden="true"></i></summary><p class="a">%s</p></details>' % (q['q'], q['a'])
        for q in cfg['faq'])
    # avis : uniquement de vrais avis clients fournis par le marchand ; sinon la section disparaît
    revs = [r for r in cfg.get('reviews', []) if r.get('text')]
    if revs:
        c['reviews_section'] = (
            '    <section class="sec" id="avis" style="padding-top:0">\n      <div class="wrap"><div class="reviews-wrap rv">\n'
            '        <div class="sec-head"><h2 class="h h2">%s</h2><span class="rule"></span></div>\n'
            '        <div class="reviews">\n%s\n        </div>\n      </div></div>\n    </section>'
            % (cfg.get('reviews_title', 'Ce que disent nos clients'),
               '\n'.join('          <figure class="review"><span class="stars" aria-label="%d sur 5">%s</span><p>%s</p><cite>%s</cite></figure>'
                         % (r.get('stars', 5), '★' * r.get('stars', 5), r['text'], r['name']) for r in revs)))
    else:
        c['reviews_section'] = ''
    if tpl is TPL_ELAN:
        for k in ('final_image',):
            c[k] = jpg(c[k])
        c.setdefault('hero_cta', 'Commander maintenant')
        c['hero_title_html'] = ''.join('<span class="ln"><span>%s</span></span>' % re.sub(r'\*(.+?)\*', r'<em>\1</em>', l) for l in cfg['hero_title_lines'])
        ch = cfg['hero_chip']
        c['chip1_icon'], c['chip1_title'], c['chip1_text'] = svg(ch['icon']), ch['title'], ch['text']
        c['marquee_html'] = ''.join('<li>%s</li>' % w for w in cfg['marquee'])
        c['life_html'] = '\n'.join(
            '          <figure class="rv"><img data-par="%s" src="%s" alt="%s" loading="lazy"></figure>'
            % (('-0.05', '0.04', '-0.03')[i % 3], asset(pref + jpg(x['image'])), x['alt']) for i, x in enumerate(cfg['life_images']))
        v = cfg.get('video_url', '').strip()
        if v:
            src = asset(v) if not v.startswith('http') else v
            c['video_button'] = '            <button type="button" class="play" data-video><i><svg viewBox="0 0 12 12"><path d="M2 1l9 5-9 5z"/></svg></i>%s</button>' % cfg.get('video_label', 'Voir la vidéo')
            c['video_modal'] = ('  <div class="vmodal" id="vmodal" data-src="%s" role="dialog" aria-label="Vidéo"><button type="button" class="vclose" aria-label="Fermer">&times;</button><div class="slot"></div></div>' % src)
        else:
            c['video_button'] = ''
            c['video_modal'] = ''
    out = tpl or TPL_ATELIER
    for k, v in c.items():
        if isinstance(v, str):
            out = out.replace('[[%s]]' % k, v)
    return out

def build(name):
    cfg = json.load(open(os.path.join(ROOT, 'tools', 'products', name + '.json'), encoding='utf-8'))
    if cfg.get('template') == 'atelier':
        return finish(name, cfg, build_atelier(cfg))
    if cfg.get('template') == 'elan':
        return finish(name, cfg, build_atelier(cfg, TPL_ELAN))
    if cfg.get('template') == 'surmesure':
        import surmesure
        return finish(name, cfg, surmesure.render(cfg, TPL_SURMESURE, asset, svg, jpg, TICK))
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

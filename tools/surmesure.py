"""Moteur du design « Sur-Mesure » : assemble une landing à partir du fichier produit.

Principe : un style visuel ("style") + une liste ordonnée de sections ("sections").
Une section sans données réelles n'est pas affichée (avis, caractéristiques,
compte à rebours…) : on n'invente jamais d'informations.
Appelé par tools/build.py quand "template": "surmesure".
"""
import os
import re

STYLES = {
    #  nom       polices Google Fonts                                                                       hero par défaut  couleur barre
    'tech':    ('Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700',                          'split',   '#0c0e12'),
    'beaute':  ('Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=DM+Sans:wght@400;500;600;700', 'split',   '#fbf6f2'),
    'sante':   ('Manrope:wght@400;500;600;700;800',                                                         'split',   '#f5f8fc'),
    'maison':  ('Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500&family=Inter:wght@400;500;600;700', 'split', '#f7f2ea'),
    'mode':    ('Bodoni+Moda:ital,opsz,wght@0,6..96,500;1,6..96,500&family=Jost:wght@400;500;600;700',      'overlay', '#ffffff'),
    'sport':   ('Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600;700',                     'overlay', '#0b0b0b'),
    'enfants': ('Baloo+2:wght@600;700;800&family=Nunito:wght@400;600;700;800',                              'split',   '#fffaf0'),
}
COLOR_KEYS = ('bg', 'surface', 'ink', 'muted', 'line', 'accent', 'accent-ink', 'accent2')
ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'


def announce(cfg):
    """Bandeau du haut. "announcement_scroll": true = texte défilant (bande passante)."""
    t = cfg.get('announcement')
    if not t: return ''
    if not cfg.get('announcement_scroll'):
        return '  <div class="announce">%s</div>' % t
    items = [x.strip() for x in t.split('·') if x.strip()]
    seq = ''.join('<span>%s</span><i aria-hidden="true">✦</i>' % x for x in items * 3)
    return ('  <div class="announce scroll" role="note" aria-label="%s"><div class="ann-track" aria-hidden="true">'
            '<div>%s</div><div>%s</div></div></div>' % (' · '.join(items), seq, seq))


def sticker(cfg, svg):
    """Badge rond flottant (ex. « 1+1 OFFERTE ») qui ouvre le formulaire de commande."""
    st = cfg.get('sticker') or {}
    if not st.get('big'): return ''
    return ('  <a class="sticker" id="sticker" href="#commander" data-order aria-label="%s">'
            '<span class="st-ico" aria-hidden="true">%s</span><b>%s</b><small>%s</small></a>\n'
            % (st.get('label', st['big']), svg(st.get('icon', 'gift')), st['big'], st.get('small', '')))


def render(cfg, tpl, asset, svg, jpg, tick):
    pref = cfg['img']
    style = cfg.get('style', 'sante')
    if style not in STYLES:
        raise SystemExit('Style inconnu « %s ». Choix : %s' % (style, ', '.join(STYLES)))
    fonts, hero_default, theme_color = STYLES[style]
    # police imposée pour toute la page, ex. "font": "Poppins" (Google Fonts)
    font = (cfg.get('font') or '').strip()
    if font:
        fonts = '%s:wght@400;500;600;700;800' % font.replace(' ', '+')
    # police du texte seulement (les titres gardent celle du style), ex. "font_body": "Poppins"
    font_body = (cfg.get('font_body') or '').strip()
    if font_body and not font:
        fonts += '&family=%s:wght@400;500;600;700' % font_body.replace(' ', '+')

    def img(name): return asset(pref + jpg(name))
    def em(t): return re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
    def has(x): return bool(x) and (not isinstance(x, list) or len(x) > 0)

    old = (cfg.get('price_old') or '').strip()
    save = (cfg.get('save_pct') or '').strip()
    cur_new = '{{ mm_new }}<small>{{ mm_cur }}</small>'

    def price_row(extra_badge=True):
        h = '<span class="price-new">%s</span>' % cur_new
        if old:
            h += '<span class="price-old">{{ mm_old }} {{ mm_cur }}</span>'
            if save and extra_badge:
                h += '<span class="badge">−%s %%</span>' % save
        return h

    dl = cfg.get('deal') or {}
    def deal(cls=''):
        """Offre spéciale bien visible (ex. 1 achetée = 1 offerte), affichée sous chaque prix."""
        if not dl.get('title'): return ''
        return ('<div class="deal%s"><span class="deal-ico" aria-hidden="true">%s</span><div><b>%s</b>%s</div></div>'
                % (cls, svg(dl.get('icon', 'gift')), dl['title'], ('<span>%s</span>' % dl['text']) if dl.get('text') else ''))

    c = {k: v for k, v in cfg.items() if isinstance(v, str)}
    c.update({
        'style': style,
        'hero_layout': cfg.get('hero_layout', hero_default),
        'hero_fit': cfg.get('hero_fit', 'cover'),
        'theme_color': cfg.get('colors', {}).get('bg', theme_color),
        'font_url': 'https://fonts.googleapis.com/css2?family=%s&display=swap' % fonts,
        'hero_image': jpg(cfg['hero']['image']),
        'currency_iso': cfg.get('currency_iso', cfg.get('currency', '')),
        'price_old': old,
        'bar_old': '<s>{{ mm_old }} {{ mm_cur }}</s>' if old else '',
        'order_old': '<span class="order-old">{{ mm_old }} {{ mm_cur }}</span>' if old else '',
        'order_note': cfg.get('order_note', 'Paiement à la livraison — nous vous appelons pour confirmer'),
        'html_class': ' '.join(x for x in (('no-scan' if cfg.get('fx_scan') is False else ''),) if x),
        'robots_meta': '  <meta name="robots" content="noindex, nofollow">\n' if cfg.get('noindex') else '',
        'announce_html': announce(cfg),
        'sticker_html': sticker(cfg, svg),
        'order_deal': ('<span class="order-deal">%s</span>' % dl['title']) if dl.get('title') else '',
    })
    # logo facultatif : affiché seulement s'il est présent dans assets/
    logo = cfg.get('logo_file', '')
    logo_ok = bool(logo) and os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', logo))
    wide = logo_ok and cfg.get('logo_wide')          # logo horizontal (icône + nom) : remplace le texte
    if wide:
        c['logo_img'] = '<img class="logo-wide" src="%s" alt="%s" height="40">' % (asset(logo), cfg['brand'])
    else:
        c['logo_img'] = ('<img src="%s" alt="" width="34" height="34">' % asset(logo)) if logo_ok else ''
    c['brand_text'] = '' if wide else cfg['brand']
    c['brand_cls'] = (' wide' + (' logo-pill' if cfg.get('logo_pill', style in ('tech', 'sport')) else '')) if wide else ''
    fav = cfg.get('favicon_file', logo)
    fav_ok = bool(fav) and os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', fav))
    c['favicon_link'] = ('  <link rel="icon" href="%s">\n' % asset(fav)) if fav_ok else ''
    # écran « réservé aux adultes » (produits 18+)
    ag = cfg.get('age_gate')
    if ag:
        ag = ag if isinstance(ag, dict) else {}
        c['age_gate_head'] = "  <script>try{if(sessionStorage.getItem('ag18')==='1')document.documentElement.classList.add('age-ok')}catch(e){}</script>\n"
        c['age_gate_html'] = ('  <div class="agegate" id="ageGate" role="dialog" aria-modal="true" aria-labelledby="agTitle"><div class="ag-box">'
            '<span class="ag-badge">18+</span><h2 id="agTitle">%s</h2><p>%s</p>'
            '<button type="button" class="btn btn-main" data-age-ok>%s</button><a class="ag-exit" href="%s">%s</a></div></div>\n'
            % (ag.get('title', 'Contenu réservé aux adultes'),
               ag.get('text', 'Cette page présente un produit destiné aux personnes majeures. Confirmez que vous avez 18 ans ou plus pour continuer.'),
               ag.get('confirm', "J'ai 18 ans ou plus"), ag.get('exit_url', '/'), ag.get('exit', 'Quitter')))
    else:
        c['age_gate_head'] = ''
        c['age_gate_html'] = ''
    ov = cfg.get('colors', {})
    c['color_overrides'] = ('html[data-style="%s"]{%s}' % (style, ';'.join('--%s:%s' % (k, v) for k, v in ov.items() if k in COLOR_KEYS))) if ov else ''
    if font_body and not font:
        c['color_overrides'] += 'html[data-style="%s"]{--fb:\'%s\',sans-serif}' % (style, font_body)
    if font:
        c['color_overrides'] += 'html[data-style="%s"]{--fh:\'%s\',sans-serif;--fb:\'%s\',sans-serif}' % (style, font, font)

    # ───────── HERO ─────────
    hr = cfg['hero']
    gallery = hr.get('gallery') or [{'image': hr['image'], 'alt': hr.get('alt', '')}]
    thumbs = ''
    if len(gallery) > 1:
        thumbs = '<div class="h-thumbs" role="group" aria-label="Photos du produit">%s</div>' % ''.join(
            '<button type="button" aria-current="%s" data-src="%s" data-alt="%s" aria-label="Photo %d"><img src="%s" alt="" loading="lazy" width="200" height="200"></button>'
            % ('true' if i == 0 else 'false', img(g['image']), g.get('alt', ''), i + 1, img(g['image'])) for i, g in enumerate(gallery))
    chips = ''.join('<div class="chip c%d"><span class="ico">%s</span><div><b>%s</b><span>%s</span></div></div>'
                    % (i + 1, svg(ch.get('icon', 'star')), ch['title'], ch.get('text', '')) for i, ch in enumerate(hr.get('chips', [])[:2]))
    note = hr.get('note', 'Paiement à la livraison')
    hero = (
        '    <section class="hero" id="hero">\n      <div class="wrap hero-grid">\n'
        '        <div class="hero-copy">\n'
        + ('          <span class="pill in-hero">%s</span>\n' % hr['kicker'] if hr.get('kicker') else '')
        + '          <h1 class="h in-hero">%s</h1>\n' % ''.join('<span class="ln">%s</span>' % em(l) for l in hr['title_lines'])
        + ('          <p class="hero-sub in-hero">%s</p>\n' % hr['sub'] if hr.get('sub') else '')
        + '          <div class="price-row in-hero">%s</div>\n' % price_row()
        + (('          %s\n' % deal(' in-hero')) if dl.get('title') else '')
        + '          <div class="hero-actions in-hero"><a class="btn btn-main" href="#commander" data-order id="heroOrder">%s%s</a>'
          '<span class="hero-note">%s%s</span></div>\n' % (hr.get('cta', 'Commander maintenant'), ARROW, tick, note)
        + '        </div>\n'
        '        <div class="hero-media in-hero"><div class="h-stage"><div class="h-main"><img id="hMain" src="%s" alt="%s" width="1000" height="1000" fetchpriority="high"></div>%s</div>%s</div>\n'
        % (img(hr['image']), hr.get('alt', ''), chips, thumbs)
        + '      </div>\n    </section>')

    # ───────── SECTIONS ─────────
    def head(s, center=True):
        h = ''
        if s.get('kicker'): h += '<span class="kicker">%s</span>' % s['kicker']
        if s.get('title'): h += '<h2 class="h h2">%s</h2>' % em(s['title'])
        if s.get('intro'): h += '<p class="lead">%s</p>' % s['intro']
        return ('<div class="sec-head rv">%s</div>' % h) if (h and center) else h

    def wrap(s, sid, inner, cls='sec'):
        if s.get('tint'): cls += ' tint'
        return '    <section class="%s" id="%s">\n      <div class="wrap">\n%s\n      </div>\n    </section>' % (cls, sid, inner)

    def stat_val(v):
        m = re.match(r'^(\d+(?:[.,]\d+)?)(.*)$', v)
        if not m: return v
        return '<span data-count="%s" data-suffix="%s">%s</span>' % (m.group(1), m.group(2).replace('"', '&quot;'), v)

    def s_trust(s, sid):
        it = s.get('items', [])
        if not it: return ''
        lis = ''.join('<li class="rv" data-icon="%s"><span class="ico">%s</span><div><b>%s</b><span>%s</span></div></li>' % (x.get('icon', 'shield'), svg(x.get('icon', 'shield')), x['title'], x.get('text', '')) for x in it)
        return '    <section class="trust" id="%s"><div class="wrap"><ul style="--n:%d">%s</ul></div></section>' % (sid, min(len(it), 4), lis)

    def s_stats(s, sid):
        it = s.get('items', [])
        if not it: return ''
        cards = ''.join('<div class="stat card rv"><b>%s</b><span>%s</span></div>' % (stat_val(x['value']), x['label']) for x in it)
        return wrap(s, sid, head(s) + '<div class="stats" style="--n:%d">%s</div>' % (min(len(it), 4), cards))

    def s_marquee(s, sid):
        it = s.get('items', [])
        if not it: return ''
        li = ''.join('<li>%s</li>' % x for x in it)
        return '    <div class="marquee" id="%s" aria-hidden="true"><div class="track"><ul>%s</ul><ul>%s</ul></div></div>' % (sid, li, li)

    def s_problem(s, sid):
        if not (s.get('pains') and (s.get('solution') or s.get('solution_text'))): return ''
        pr = s.get('image_ratio', '').strip()       # ex. "4/5" pour des photos verticales
        pst = (' style="aspect-ratio:%s"' % pr) if pr else ''
        bad = '<div class="ps-box bad card rv"><h3 class="h">%s</h3><ul>%s</ul>%s</div>' % (
            em(s.get('problem_title', 'Le problème')), ''.join('<li>%s</li>' % p for p in s['pains']),
            ('<div class="ps-img"%s><img src="%s" alt="%s" loading="lazy"></div>' % (pst, img(s['problem_image']), s.get('problem_alt', ''))) if s.get('problem_image') else '')
        good = '<div class="ps-box good card rv"><h3 class="h">%s</h3>%s%s%s</div>' % (
            em(s.get('solution_title', 'La solution')),
            ('<p>%s</p>' % s['solution_text']) if s.get('solution_text') else '',
            ('<ul>%s</ul>' % ''.join('<li>%s</li>' % p for p in s['solution'])) if s.get('solution') else '',
            ('<div class="ps-img"%s><img src="%s" alt="%s" loading="lazy"></div>' % (pst, img(s['image']), s.get('alt', ''))) if s.get('image') else '')
        return wrap(s, sid, head(s) + '<div class="ps">%s%s</div>' % (bad, good))

    def s_benefits(s, sid):
        it = s.get('items', [])
        if not it: return ''
        cols = s.get('columns', 4 if len(it) % 4 == 0 else 3)
        cards = ''.join('<div class="benefit card rv"><span class="ico">%s</span><h3>%s</h3><p>%s</p></div>' % (svg(x.get('icon', 'star')), x['title'], x.get('text', '')) for x in it)
        return wrap(s, sid, head(s) + '<div class="benefits" style="--cols:%d">%s</div>' % (cols, cards))

    def s_showcase(s, sid):
        it = s.get('items', [])
        if not it: return ''
        blocks = ''.join(
            '<article class="sc"><div class="sc-media rv"><img src="%s" alt="%s" loading="lazy"></div>'
            '<div class="sc-copy rv">%s<h3 class="h">%s</h3><p>%s</p><a class="btn btn-line" href="#commander" data-order>%s</a></div></article>'
            % (img(x['image']), x.get('alt', ''), ('<span class="kicker">%s</span>' % x['kicker']) if x.get('kicker') else '',
               em(x['title']), x.get('text', ''), s.get('cta', 'Commander'))
            for x in it)
        return wrap(s, sid, head(s) + '<div class="showcase">%s</div>' % blocks)

    def s_demo(s, sid):
        it = s.get('steps', [])
        if not it: return ''
        cards = ''.join(
            '<div class="step card rv">%s<div class="step-body"><span class="step-n">%d</span><h3 class="h">%s</h3><p>%s</p></div></div>'
            % (('<div class="step-img"><img src="%s" alt="%s" loading="lazy"></div>' % (img(x['image']), x.get('alt', x['title']))) if x.get('image') else '',
               i + 1, x['title'], x.get('text', '')) for i, x in enumerate(it))
        return wrap(s, sid, head(s) + '<div class="demo" style="--n:%d">%s</div>' % (min(len(it), 4), cards))

    def s_gallery(s, sid):
        it = s.get('images', [])
        if len(it) < 2: return ''
        figs = ''.join('<figure class="rv"><img src="%s" alt="%s" loading="lazy"></figure>' % (img(x['image']), x.get('alt', '')) for x in it)
        n = len(it)
        if n in (5, 9):   cls, cols = 'gal feature', 4          # 1 grande + 4 (ou 8) petites
        elif n % 4 == 0:  cls, cols = 'gal', 4
        elif n % 3 == 0:  cls, cols = 'gal', 3
        else:             cls, cols = 'gal', 2 if n == 2 else 3
        mob_odd = ' odd' if (n - (1 if 'feature' in cls else 0)) % 2 else ''
        return wrap(s, sid, head(s) + '<div class="%s%s" style="--cols:%d">%s</div>' % (cls, mob_odd, cols, figs))

    def s_beforeafter(s, sid):
        b, a = s.get('before'), s.get('after')
        if not (b and a and b.get('image') and a.get('image')): return ''
        inner = ('<div class="ba rv" style="--pos:50%%"><img src="%s" alt="%s" loading="lazy"><img class="after" src="%s" alt="%s" loading="lazy">'
                 '<span class="lbl l">%s</span><span class="lbl r">%s</span><span class="bar-h"></span><span class="knob">⇆</span>'
                 '<input type="range" min="0" max="100" value="50" aria-label="Comparer avant et après"></div>'
                 % (img(b['image']), b.get('label', 'Avant'), img(a['image']), a.get('label', 'Après'), b.get('label', 'Avant'), a.get('label', 'Après')))
        return wrap(s, sid, head(s) + inner)

    def s_video(s, sid):
        v = s.get('video', '').strip()
        if not v: return ''
        src = v if v.startswith(('http://', 'https://', '//')) else asset(pref + (v if v.endswith('.mp4') else v + '.mp4'))
        poster = (' poster="%s"' % img(s['poster'])) if s.get('poster') else ''
        ratio = s.get('ratio', '').strip()          # ex. "3/4" pour une vidéo verticale
        try:
            rw, rh = (float(x) for x in ratio.split('/'))
            vertical = rw < rh
        except ValueError:
            vertical = False
        vstyle = ' style="max-width:min(440px,100%)"' if vertical else ''
        inner = ('<figure class="vid rv"%s><video src="%s"%s muted loop playsinline preload="none" aria-label="%s"%s></video>'
                 '<button type="button" class="vid-btn" aria-label="Lecture / pause"><svg viewBox="0 0 12 12"><path d="M2 1l9 5-9 5z"/></svg></button>%s</figure>'
                 % (vstyle, src, poster, s.get('alt', 'Vidéo du produit'), (' style="aspect-ratio:%s"' % ratio) if ratio else '', ('<figcaption>%s</figcaption>' % s['caption']) if s.get('caption') else ''))
        if s.get('cta'): inner += '<div class="vid-cta rv"><a class="btn btn-main" href="#commander" data-order>%s</a></div>' % s['cta']
        return wrap(s, sid, head(s) + inner)

    def s_specs(s, sid):
        rows = [r for r in s.get('rows', []) if r.get('value')]
        if not rows: return ''
        ul = '<ul class="specs card">%s</ul>' % ''.join('<li><span>%s</span><b>%s</b></li>' % (r['label'], r['value']) for r in rows)
        if s.get('image'):
            inner = '<div class="specs-wrap"><div class="specs-media rv"><img src="%s" alt="%s" loading="lazy"></div><div class="rv">%s%s</div></div>' % (
                img(s['image']), s.get('alt', ''), head(s, center=False), ul)
        else:
            inner = head(s) + '<div class="specs-wrap solo rv">%s</div>' % ul
        return wrap(s, sid, inner)

    def s_compare(s, sid):
        cols, rows = s.get('columns', []), s.get('rows', [])
        if len(cols) < 2 or not rows: return ''
        hl = s.get('highlight', 1)
        def cell(v, j):
            cls = ' class="hl"' if j == hl else ''
            if str(v).lower() in ('oui', 'yes', 'true', '1'): v = '<span class="yes">✓</span>'
            elif str(v).lower() in ('non', 'no', 'false', '0', ''): v = '—'
            return '<td%s>%s</td>' % (cls, v)
        th = '<tr><th></th>%s</tr>' % ''.join('<th%s>%s</th>' % (' class="hl"' if j + 1 == hl else '', x) for j, x in enumerate(cols))
        trs = ''.join('<tr><td>%s</td>%s</tr>' % (r['label'], ''.join(cell(v, j + 1) for j, v in enumerate(r['values']))) for r in rows)
        return wrap(s, sid, head(s) + '<div class="cmp-wrap rv"><table class="cmp%s">%s%s</table></div>' % (' cmp-2' if len(cols) <= 2 else '', th, trs))

    def s_included(s, sid):
        it = s.get('items', [])
        if not it: return ''
        figs = ''.join(
            ('<figure class="card rv"><div class="im"><img src="%s" alt="%s" loading="lazy"></div><figcaption>%s</figcaption></figure>' % (img(x['image']), x['label'], x['label']))
            if x.get('image') else
            ('<figure class="card noimg rv"><figcaption><span class="ico">%s</span>%s</figcaption></figure>' % (svg(x.get('icon', 'box')), x['label']))
            for x in it)
        return wrap(s, sid, head(s) + '<div class="incl" style="--n:%d">%s</div>' % (min(len(it), 4), figs))

    def s_reviews(s, sid):
        it = [r for r in s.get('items', []) if r.get('text') and r.get('name')]
        if not it: return ''   # uniquement de vrais avis fournis par le marchand
        cards = ''.join('<figure class="review card rv"><span class="stars" aria-label="%d sur 5">%s</span><p>%s</p><cite>%s</cite></figure>'
                        % (r.get('stars', 5), '★' * r.get('stars', 5), r['text'], r['name']) for r in it)
        return wrap(s, sid, head(s) + '<div class="reviews">%s</div>' % cards)

    def s_offer(s, sid):
        terms = ''.join('<div><b>%s :</b> %s</div>' % (lbl, s[k]) for k, lbl in (('delivery', 'Livraison'), ('payment', 'Paiement'), ('returns', 'Retours'), ('guarantee', 'Garantie')) if s.get(k))
        cd = ''
        if s.get('ends_at'):
            cd = ('<div class="countdown" data-ends="%s">%s<div class="cd">%s</div></div>'
                  % (s['ends_at'], s.get('ends_label', 'L’offre se termine dans'),
                     ''.join('<span data-u>00<small>%s</small></span>' % u for u in ('jours', 'h', 'min', 's'))))
        body = ('<div class="offer-body">%s%s%s%s<div class="offer-price">%s</div>%s%s%s<a class="btn btn-main" href="#commander" data-order>%s</a></div>'
                % (('<span class="pill">%s</span>' % s['kicker']) if s.get('kicker') else '',
                   '<h2 class="h">%s</h2>' % em(s.get('title', 'Votre commande')),
                   ('<p>%s</p>' % s['text']) if s.get('text') else '',
                   ('<ul class="offer-list">%s</ul>' % ''.join('<li>%s<span>%s</span></li>' % (tick, x) for x in s['items'])) if s.get('items') else '',
                   price_row(), deal(), cd,
                   ('<div class="offer-terms">%s</div>' % terms) if terms else '',
                   s.get('cta', 'Commander — payer à la livraison')))
        media = ('<div class="offer-media"><img src="%s" alt="%s" loading="lazy"></div>' % (img(s['image']), s.get('alt', ''))) if s.get('image') else ''
        return wrap(s, sid, '<div class="offer card %s rv">%s%s</div>' % ('' if media else 'solo', media, body))

    def s_faq(s, sid):
        it = s.get('items', [])
        if not it: return ''
        det = ''.join('<details class="card"><summary>%s<i aria-hidden="true"></i></summary><p class="a">%s</p></details>' % (q['q'], q['a']) for q in it)
        s2 = dict(s); s2.setdefault('kicker', 'Questions fréquentes')
        return wrap(s2, sid, head(s2) + '<div class="faq rv">%s</div>' % det)

    def s_cta(s, sid):
        inner = ('<div class="cta rv"><div><h2 class="h">%s%s</h2>%s</div><div class="cta-card"><div class="price-row" style="justify-content:center">%s</div>%s'
                 '<span class="note">%s</span><a class="btn btn-main" href="#commander" data-order id="finalOrder">%s%s</a></div></div>'
                 % (em(s.get('title', 'Prêt à commander ?')), (' <em>%s</em>' % s['em']) if s.get('em') else '',
                    ('<p>%s</p>' % s['text']) if s.get('text') else '', price_row(False), deal(' center'),
                    s.get('note', 'Paiement à la livraison'), s.get('button', 'Commander maintenant'), ARROW))
        return '    <section style="padding:0 0 clamp(40px,6vw,72px)" id="%s"><div class="wrap">%s</div></section>' % (sid, inner)

    R = {'trust': s_trust, 'stats': s_stats, 'marquee': s_marquee, 'problem': s_problem, 'benefits': s_benefits,
         'showcase': s_showcase, 'video': s_video, 'demo': s_demo, 'gallery': s_gallery, 'beforeafter': s_beforeafter, 'specs': s_specs,
         'compare': s_compare, 'included': s_included, 'reviews': s_reviews, 'offer': s_offer, 'faq': s_faq, 'cta': s_cta}

    out_sections, nav, seen = [hero], [], {}
    for s in cfg.get('sections', []):
        t = s.get('type')
        if t not in R:
            raise SystemExit('Section inconnue « %s ». Choix : %s' % (t, ', '.join(R)))
        seen[t] = seen.get(t, 0) + 1
        sid = t if seen[t] == 1 else '%s-%d' % (t, seen[t])
        html = R[t](s, sid)
        if html:
            out_sections.append(html)
            if s.get('nav'): nav.append('<a href="#%s">%s</a>' % (sid, s['nav']))
    if not any(s.get('type') == 'cta' for s in cfg.get('sections', [])):
        out_sections.append(s_cta({}, 'final'))
    c['sections_html'] = '\n\n'.join(out_sections)
    c['nav_html'] = ''.join(nav[:5])

    out = tpl
    for k, v in c.items():
        if isinstance(v, str):
            out = out.replace('[[%s]]' % k, v)
    return out

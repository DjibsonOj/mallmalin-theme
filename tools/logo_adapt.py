"""Logo adapté aux couleurs de chaque page produit (design Sur-Mesure).

À partir du logo horizontal de la boutique (icône + nom), crée une seule fois dans assets/ :
  <logo>-icone.png  : l'icône, fond blanc retiré (couleurs d'origine)
  <logo>-texte.png  : le nom de la marque en masque (forme seule) ; la page le colorie
                      avec sa propre couleur (accent par défaut) → le logo « épouse » la page.
Les fichiers sont régénérés seulement si le logo source change.
"""
import os

def _no_white_bg(im):
    """Retire un fond blanc (ou presque) relié aux bords ; ne touche pas aux blancs intérieurs."""
    from PIL import Image, ImageDraw
    im = im.convert('RGBA')
    a = im.getchannel('A')
    if a.getextrema()[0] < 250:          # déjà transparent
        return im
    w, h = im.size
    rgb = im.convert('RGB')
    key = (255, 0, 255)
    for x, y in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)] + [(x, 0) for x in range(0, w, 8)] + [(x, h - 1) for x in range(0, w, 8)] + [(0, y) for y in range(0, h, 8)] + [(w - 1, y) for y in range(0, h, 8)]:
        r, g, b = rgb.getpixel((x, y))
        if min(r, g, b) >= 225:
            ImageDraw.floodfill(rgb, (x, y), key, thresh=40)
    px, out = rgb.load(), im.load()
    for y in range(h):
        for x in range(w):
            if px[x, y] == key:
                out[x, y] = (255, 255, 255, 0)
    return im

def _split_x(im):
    """Colonne qui sépare l'icône du texte : la plus grande bande vide dans les 60 % de gauche."""
    a = im.getchannel('A').point(lambda v: 255 if v > 40 else 0)
    w, h = im.size
    cols = [a.crop((x, 0, x + 1, h)).getbbox() is None for x in range(w)]
    best, start = (0, 0, 0), None
    for x in range(int(w * .6) + 1):
        if x < int(w * .6) and cols[x]:
            start = x if start is None else start
        elif start is not None:
            if start > 0 and x - start > best[0]:
                best = (x - start, start, x)
            start = None
    return (best[1], best[2]) if best[0] >= 3 else None

def adapt(assets_dir, logo):
    """Renvoie (icone, texte, largeur, hauteur du texte) ou None si le logo ne se découpe pas."""
    try:
        from PIL import Image
    except ImportError:
        return None
    src = os.path.join(assets_dir, logo)
    stem = os.path.splitext(logo)[0]
    ico_n, txt_n = stem + '-icone.png', stem + '-texte.png'
    ico_p, txt_p = os.path.join(assets_dir, ico_n), os.path.join(assets_dir, txt_n)
    if not (os.path.exists(ico_p) and os.path.exists(txt_p) and os.path.getmtime(ico_p) >= os.path.getmtime(src)):
        im = _no_white_bg(Image.open(src))
        cut = _split_x(im)
        if not cut:
            return None
        w, h = im.size
        ico = im.crop((0, 0, cut[0], h))
        txt = im.crop((cut[1], 0, w, h))
        bb = txt.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
        txt = txt.crop((bb[0], 0, bb[2], h))
        mask = Image.new('RGBA', txt.size, (255, 255, 255, 0))
        mask.putalpha(txt.getchannel('A'))
        ico.save(ico_p, optimize=True)
        mask.save(txt_p, optimize=True)
    t = Image.open(txt_p)
    return ico_n, txt_n, t.size[0], t.size[1]

def _lum(hx):
    hx = hx.lstrip('#')
    if len(hx) == 3: hx = ''.join(c * 2 for c in hx)
    r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)

def contrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + .05) / (lb + .05)

def page_colors(template_text, style, overrides):
    """Couleurs réelles de la page : celles du style, remplacées par "colors" du produit."""
    import re
    m = re.search(r'html\[data-style="%s"\]\{([^}]*)\}' % style, template_text)
    col = dict(re.findall(r'--([a-z0-9-]+):(#[0-9a-fA-F]{3,6})', m.group(1))) if m else {}
    col.update({k: v for k, v in (overrides or {}).items() if str(v).startswith('#')})
    return col

def pick_color(col, forced=None):
    """Couleur du nom de marque : imposée, sinon l'accent de la page s'il se lit bien sur le fond, sinon la couleur du texte."""
    if forced:
        return forced
    bg = col.get('bg', '#ffffff')
    for k in ('accent', 'ink'):
        if col.get(k) and contrast(col[k], bg) >= 3:
            return col[k]
    return '#ffffff' if _lum(bg) < .3 else '#111111'

def colorize(assets_dir, mask_name, color, out_name):
    from PIL import Image
    m = Image.open(os.path.join(assets_dir, mask_name))
    hx = color.lstrip('#')
    if len(hx) == 3: hx = ''.join(c * 2 for c in hx)
    out = Image.new('RGBA', m.size, tuple(int(hx[i:i + 2], 16) for i in (0, 2, 4)) + (0,))
    out.putalpha(m.getchannel('A'))
    out.save(os.path.join(assets_dir, out_name), optimize=True)
    return out_name

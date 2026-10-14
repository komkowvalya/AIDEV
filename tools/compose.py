import os, sys, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = os.path.dirname(os.path.abspath(__file__)); MK = os.path.join(S, 'mk')
OUT = sys.argv[1]; os.makedirs(OUT+'/instagram', exist_ok=True); os.makedirs(OUT+'/superhive', exist_ok=True)
F = lambda n, s: ImageFont.truetype(os.path.join(S, 'fonts', n), s)
HEAD, SUB, BODY = 'Oswald-Bold.ttf', 'BarlowCondensed-SemiBold.ttf', 'BarlowCondensed-Medium.ttf'
NAVY, NAVY2, RED, WHITE, MUTED = (13, 22, 38), (28, 44, 74), (214, 40, 57), (245, 247, 250), (160, 174, 196)

def bg(w, h):
    im = Image.new('RGB', (w, h), NAVY)
    g = Image.new('L', (w, h), 0); d = ImageDraw.Draw(g)
    d.ellipse((-w*0.3, h*0.15, w*1.3, h*1.1), fill=255)
    g = g.filter(ImageFilter.GaussianBlur(w*0.18))
    im.paste(Image.new('RGB', (w, h), NAVY2), (0, 0), g)
    # thin stripes motif top-right
    d = ImageDraw.Draw(im)
    for i in range(5):
        y = 36 + i*14
        d.rectangle((w-210, y, w-48, y+6), fill=RED if i % 2 == 0 else WHITE)
    return im

def shadow_paste(im, src, xy, blur=28, off=(0, 26), alpha=150):
    a = src.split()[-1]
    sh = Image.new('RGBA', src.size, (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: v*alpha//255))
    pad = blur*3
    big = Image.new('RGBA', (src.width+2*pad, src.height+2*pad), (0, 0, 0, 0)); big.paste(sh, (pad, pad))
    big = big.filter(ImageFilter.GaussianBlur(blur))
    im.paste(big, (xy[0]-pad+off[0], xy[1]-pad+off[1]), big)
    im.paste(src, xy, src)

def fit(img, w=None, h=None):
    img = img.crop(img.getbbox())
    s = min(w/img.width if w else 9e9, h/img.height if h else 9e9)
    return img.resize((int(img.width*s), int(img.height*s)), Image.LANCZOS)

def text_c(d, cx, y, s, font, fill):
    w = d.textlength(s, font=font); d.text((cx-w/2, y), s, font=font, fill=fill)

def header(im, kicker, title, sub, top=70, size=96):
    d = ImageDraw.Draw(im); W = im.width
    text_c(d, W/2, top, kicker, F(SUB, 34), RED)
    f = F(HEAD, size)
    while d.textlength(title, font=f) > W-120: size -= 4; f = F(HEAD, size)
    text_c(d, W/2, top+44, title, f, WHITE)
    yy = top+44+int(size*1.32)
    for line in sub.split('\n'):
        text_c(d, W/2, yy, line, F(BODY, 40), MUTED); yy += 48
    return yy

def footer(im, s='US LICENSE PLATE GENERATOR  ·  BLENDER GEOMETRY NODES'):
    d = ImageDraw.Draw(im); W, H = im.size
    d.rectangle((0, H-70, W, H), fill=(9, 15, 27))
    text_c(d, W/2, H-54, s, F(SUB, 30), MUTED)

def pill(d, x, y, s, font, fg=WHITE, bgc=RED):
    w = d.textlength(s, font=font); h = font.size
    d.rounded_rectangle((x, y, x+w+40, y+h+22), radius=(h+22)//2, fill=bgc)
    d.text((x+20, y+6), s, font=font, fill=fg); return x+w+40

R = lambda n: Image.open(os.path.join(MK, n+'.png')).convert('RGBA')
flat = lambda k: Image.open(os.path.join(MK, 'flat', k+'.png')).convert('RGBA')
STATES = sorted(json.load(open(os.path.join(MK, 'grid.png.json'))))

# ------------------------------------------------------------------ Instagram 1080x1350
IW, IH = 1080, 1350
def slide(name, kicker, title, sub, render, w=1000, h=760, cy=None, extra=None):
    im = bg(IW, IH).convert('RGBA')
    y = header(im, kicker, title, sub)
    img = fit(R(render), w, h)
    cy = cy or (y + (IH-70-y)//2)
    shadow_paste(im, img, ((IW-img.width)//2, cy-img.height//2))
    if extra: extra(im)
    footer(im); im.convert('RGB').save(f'{OUT}/instagram/{name}.png', optimize=True)

def badges(items, y=1180):
    def f(im):
        d = ImageDraw.Draw(im); font = F(SUB, 32)
        widths = [d.textlength(s, font=font)+40 for s in items]; gap = 16
        x = (IW - (sum(widths)+gap*(len(items)-1)))/2
        for s in items: x = pill(d, x, y, s, font, bgc=(38, 58, 96)) + gap
    return f

slide('01_cover', 'BLENDER 5.2  ·  GEOMETRY NODES', 'US LICENSE PLATES', 'All 50 states + DC in one modifier', 'hero',
      extra=badges(['51 PRESETS', 'EEVEE & CYCLES', 'BEGINNER FRIENDLY']))

# states wall
im = bg(IW, IH).convert('RGBA')
y = header(im, 'EVERY STATE INCLUDED', '50 STATES + DC', 'Real state names, slogans, colors and artwork')
cols, pw = 6, 162; ph = int(pw*0.5); gx, gy = 10, 12
rows = -(-len(STATES)//cols); x0 = (IW-(cols*pw+(cols-1)*gx))//2; y0 = y + ((IH-70-y) - (rows*ph+(rows-1)*gy))//2
for i, k in enumerate(STATES):
    r, c = divmod(i, cols)
    p = fit(flat(k), pw, ph)
    shadow_paste(im, p, (x0+c*(pw+gx), y0+r*(ph+gy)), blur=8, off=(0, 6), alpha=120)
footer(im); im.convert('RGB').save(f'{OUT}/instagram/02_all_states.png', optimize=True)

slide('03_bend', 'ONE SLIDER', 'EASY BEND', 'Wrap the plate around any bumper', 'bend')
slide('04_any_number', 'TYPE IT, DONE', 'ANY NUMBER', 'Real embossed letters · 6 fonts or your own', 'vanity',
      extra=badges(['EMBOSSED', 'FLAT PRINTED', 'CUSTOM FONT']))
slide('05_state_symbols', 'BUILT-IN SEPARATORS', 'STATE SYMBOLS', 'Florida orange · Georgia peach · PA keystone · NM Zia', 'sep')
slide('06_frame', 'DEALER STYLE', 'PLASTIC FRAME', 'Your own text on the frame, screws included', 'frame', w=1040, h=800)
slide('07_dirt', 'ONE CLICK', 'DIRT & FLIES', 'Road grime, mud speckles and squashed bugs', 'dirt', w=1040, h=800)

# simple panel graphic
def panel_img(w, h, scale=1.0):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w-1, h-1), radius=int(18*scale), fill=(40, 40, 44, 255), outline=(70, 70, 76, 255), width=2)
    ft, fi = F(SUB, int(30*scale)), F(BODY, int(27*scale))
    groups = [('Plate', ['Bend angle', 'Backplate', 'Mounting Holes', 'Screws']),
              ('Registration', ['WRITING', 'NUMBER', 'Font Index / Custom Font', 'Font Size', 'Letters Height']),
              ('State', ['STATE', 'SLOGAN', 'State / Slogan Size']),
              ('Border & Stickers', ['Embossed / Paint Border', 'Sticker', 'Sticker Position']),
              ('Colors', ['Letters · Plate · State · Slogan · Border']),
              ('Frame & Dirt', ['Plastic Frame', 'Flies', 'Frame writing #1-3'])]
    y = int(22*scale); lh = int(36*scale)
    for g, its in groups:
        tx, ty, ts = int(30*scale), y+int(13*scale), int(9*scale)
        d.polygon([(tx-ts, ty-ts//2), (tx+ts, ty-ts//2), (tx, ty+ts)], fill=(200, 200, 206))
        d.text((int(52*scale), y), g, font=ft, fill=(235, 235, 240)); y += lh+int(4*scale)
        for s in its:
            d.text((int(70*scale), y), s, font=fi, fill=(175, 178, 186))
            d.rounded_rectangle((w-int(230*scale), y+2, w-int(26*scale), y+lh-int(8*scale)), radius=int(6*scale), fill=(58, 58, 64))
            y += lh
        y += int(10*scale)
    return im
im = bg(IW, IH).convert('RGBA')
y = header(im, 'CLEAN MODIFIER PANEL', 'BEGINNER FRIENDLY', 'Only the inputs you need, grouped in panels\nUS plate specs (12" x 6", 7" hole spacing) built in')
p = panel_img(780, 860, 0.88); shadow_paste(im, p, ((IW-780)//2, y+24), blur=18, alpha=140)
footer(im); im.convert('RGB').save(f'{OUT}/instagram/08_simple_panel.png', optimize=True)

# ------------------------------------------------------------------ Superhive gallery 1920x1080
SW, SH = 1920, 1080
im = bg(SW, SH).convert('RGBA'); d = ImageDraw.Draw(im)
d.text((110, 170), 'BLENDER 5.2  ·  GEOMETRY NODES', font=F(SUB, 40), fill=RED)
d.text((104, 225), 'LICENSE PLATE', font=F(HEAD, 104), fill=WHITE)
d.text((104, 365), 'GENERATOR · USA', font=F(HEAD, 104), fill=WHITE)
d.text((110, 530), 'All 50 states + DC  ·  bend  ·  frame  ·  dirt', font=F(BODY, 46), fill=MUTED)
x = 110
for s in ['51 PRESETS', 'EEVEE & CYCLES', 'BEGINNER FRIENDLY']: x = pill(d, x, 620, s, F(SUB, 34)) + 16
h = fit(R('hero'), 900, 700); shadow_paste(im, h, (SW-h.width-50, (SH-h.height)//2+30))
im.convert('RGB').save(f'{OUT}/superhive/01_cover.png', optimize=True)

im = bg(SW, SH).convert('RGBA'); d = ImageDraw.Draw(im)
text_c(d, SW/2, 60, '50 STATES + DC INCLUDED', F(HEAD, 76), WHITE)
cols, pw = 9, 196; ph = int(pw*0.5); gx, gy = 12, 14
x0 = (SW-(cols*pw+(cols-1)*gx))//2; y0 = 200
for i, k in enumerate(STATES):
    r, c = divmod(i, cols)
    shadow_paste(im, fit(flat(k), pw, ph), (x0+c*(pw+gx), y0+r*(ph+gy)), blur=8, off=(0, 6), alpha=120)
im.convert('RGB').save(f'{OUT}/superhive/02_all_states.png', optimize=True)

im = bg(SW, SH).convert('RGBA'); d = ImageDraw.Draw(im)
cells = [('bend', 'EASY BEND'), ('frame', 'PLASTIC FRAME'), ('dirt', 'DIRT & FLIES'), ('vanity', 'ANY NUMBER')]
for i, (r, t) in enumerate(cells):
    cx, cy = 480 + (i % 2)*960, 290 + (i//2)*500
    img = fit(R(r), 820, 380); shadow_paste(im, img, (cx-img.width//2, cy-img.height//2+10), blur=18)
    text_c(d, cx, cy+210, t, F(HEAD, 44), WHITE)
im.convert('RGB').save(f'{OUT}/superhive/03_features.png', optimize=True)

im = bg(SW, SH).convert('RGBA'); d = ImageDraw.Draw(im)
d.text((110, 200), 'SIMPLE', font=F(HEAD, 120), fill=WHITE)
d.text((110, 340), 'MODIFIER PANEL', font=F(HEAD, 120), fill=WHITE)
yy = 530
for s in ['Type the number, pick the state — done', 'US plate specs built in (12" x 6", 7" holes)', 'Hidden layout values stay correct for every state', 'Separate colors for letters, state, slogan, border']:
    d.text((114, yy), '•  ' + s, font=F(BODY, 42), fill=MUTED); yy += 62
p = panel_img(700, 860, 0.83); shadow_paste(im, p, (SW-700-140, (SH-860)//2+20), blur=18, alpha=140)
im.convert('RGB').save(f'{OUT}/superhive/04_panel.png', optimize=True)

for n in ['sep', 'embossed']:
    im = bg(SW, SH).convert('RGBA'); d = ImageDraw.Draw(im)
    t = {'sep': 'STATE SYMBOLS AS SEPARATORS', 'embossed': 'EMBOSSED OR FLAT PRINTED'}[n]
    text_c(d, SW/2, 60, t, F(HEAD, 72), WHITE)
    img = fit(R(n), 1500, 860); shadow_paste(im, img, ((SW-img.width)//2, 180+(880-img.height)//2))
    im.convert('RGB').save(f'{OUT}/superhive/0{5 if n=="sep" else 6}_{n}.png', optimize=True)
print('done')

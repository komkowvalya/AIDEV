import os, sys
from PIL import Image, ImageDraw, ImageFont
C = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'callout'); OUT = sys.argv[1]
IF = '/usr/share/fonts/opentype/inter/'
F = lambda w, s: ImageFont.truetype(IF + f'Inter-{w}.otf', s)
W, H = 2600, 2000
NAVY, RED, INK, GREY = (22, 58, 120), (214, 40, 57), (25, 30, 40), (95, 102, 115)
im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)

panel = Image.open(os.path.join(C, 'panel.png')).convert('RGB')
PX = W - panel.width; im.paste(panel, (PX, 0))

d.text((70, 50), 'Main parameters', font=F('Medium', 64), fill=NAVY)
d.text((74, 135), 'One modifier drives the whole plate. Numbers on the plate match the panel.', font=F('Regular', 28), fill=GREY)

plate = Image.open(os.path.join(C, '0021_MD.png')).convert('RGB')
S = 0.78; X0, Y0 = 180, 290
pl = plate.resize((int(plate.width*S), int(plate.height*S)), Image.LANCZOS); im.paste(pl, (X0, Y0))
P = lambda x, y: (X0 + x*S, Y0 + y*S)

def badge(x, y, n, r=22):
    d.ellipse((x-r, y-r, x+r, y+r), fill=RED, outline='white', width=4)
    f = F('Bold', 24); t = str(n); tw = d.textlength(t, font=f)
    d.text((x-tw/2, y-15), t, font=f, fill='white')

def label(cx, top, n, title, desc, anchor_xy):
    ft, fd = F('SemiBold', 27), F('Regular', 22)
    tw = max(d.textlength(title, font=ft), d.textlength(desc, font=fd))
    x = cx - tw/2
    lx, ly = anchor_xy
    end = (cx, top + 72) if ly > top else (cx, top - 12)     # stop just outside the label
    d.line([(lx, ly), end], fill=RED, width=3)
    d.ellipse((end[0]-5, end[1]-5, end[0]+5, end[1]+5), fill=RED)
    d.text((x, top), title, font=ft, fill=INK); d.text((x, top + 36), desc, font=fd, fill=GREY)

# feature points on the plate (pixels of the 2000x1085 render)
feat = {1: (1640, 745), 2: (600, 762), 3: (985, 230), 4: (1000, 905), 5: (1610, 196),
        6: (478, 188), 7: (138, 560), 8: (300, 950)}
top_labels = {6: (520, 'Mounting Holes', 'slots on/off, + Screws'),
              3: (950, 'STATE', 'header text, font & size'),
              5: (1440, 'Sticker', 'object + Sticker Position')}
bot_labels = {7: (230, 'Border', 'embossed rim + paint line'),
              8: (545, 'Backplate', 'state artwork material'),
              2: (860, 'Letters Height', 'emboss depth, 0 = flat'),
              4: (1175, 'SLOGAN', 'bottom line text'),
              1: (1490, 'WRITING', 'number, font, size')}
for n, (cx, t, ds) in top_labels.items(): label(cx, 190, n, t, ds, P(*feat[n]))
for n, (cx, t, ds) in bot_labels.items(): label(cx, Y0 + plate.height*S + 55, n, t, ds, P(*feat[n]))
for n in feat: badge(*P(*feat[n]), n)

# parameters with no single spot on the plate
cards = [(9, 'RESOLUTION', 'Mesh density: 2 = 1 mm grid, 3 = 0.5 mm.', 'Lower it for plates far from camera.'),
         (10, 'Bend angle', 'Curves plate, frame and sticker together', 'to fit any bumper (5° here).'),
         (11, 'Colors', 'Letters, plate tint, state, slogan and', 'border each get their own color.'),
         (12, 'Plastic Frame · Flies', 'Dealer frame with 3 text lines and', 'one-click road dirt & bug splats.')]
cy0 = 1330
d.line([(70, cy0 - 40), (PX - 70, cy0 - 40)], fill=(225, 228, 234), width=2)
for k, (n, t, l1, l2) in enumerate(cards):
    x = 90 + (k % 2) * 950; y = cy0 + (k // 2) * 230
    d.rounded_rectangle((x, y, x + 860, y + 190), 18, fill=(244, 246, 250))
    badge(x + 60, y + 60, n, 28)
    d.text((x + 115, y + 34), t, font=F('SemiBold', 34), fill=INK)
    d.text((x + 115, y + 92), l1, font=F('Regular', 26), fill=GREY)
    d.text((x + 115, y + 128), l2, font=F('Regular', 26), fill=GREY)

# matching badges + row highlights on the real panel (y = row centre in the screenshot)
rows = {9: 160, 10: 194, 8: 229, 6: 264, 1: 380, 2: 803, 3: 1010, 4: 1148, 7: 1300, 5: 1439, 11: 1570, 12: 1832}
for n, y in rows.items():
    d.rounded_rectangle((PX + 64, y - 17, W - 14, y + 17), 7, outline=RED, width=3)
    badge(PX + 34, y, n, 20)
im.save(OUT, optimize=True); print(OUT, im.size)

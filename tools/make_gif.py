import os, sys
from PIL import Image, ImageDraw, ImageFont
G = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gif')
OUT = sys.argv[1]
W, H = 1280, 600
PW = 440                                         # panel width
IF = '/usr/share/fonts/opentype/inter/'
f_ui  = ImageFont.truetype(IF + 'Inter-Regular.otf', 17)
f_uib = ImageFont.truetype(IF + 'Inter-SemiBold.otf', 17)
f_hd  = ImageFont.truetype(IF + 'Inter-SemiBold.otf', 15)
f_cap = ImageFont.truetype(IF + 'Inter-SemiBold.otf', 26)
f_sub = ImageFont.truetype(IF + 'Inter-Regular.otf', 17)
BG, PANEL, ROWBG, FIELD, FIELD_HI, TXT, DIM, BLUE = (40,40,40), (48,48,48), (56,56,56), (29,29,29), (36,36,36), (230,230,230), (150,150,150), (71,114,179)

def lin2srgb(c): return tuple(int(255*((x*12.92) if x <= 0.0031308 else (1.055*x**(1/2.4)-0.055))) for x in c[:3])
FONTS = ['Barlow Condensed', 'Oswald', 'Overpass', 'Saira Condensed', 'Bebas Neue', 'Roboto Condensed']

state = {'WRITING': '8ABC123', 'FONT': 0, 'HEIGHT': 0.0012, 'SLOGAN': 'DMV.CA.GOV',
         'COLOR': (0.014, 0.023, 0.147), 'FRAME': False, 'FLIES': False}
ROWS = [('hdr', 'Registration'), ('WRITING', 'WRITING'), ('FONT', 'Font Index (6-Custom)'), ('HEIGHT', 'Letters Height'),
        ('hdr', 'State'), ('SLOGAN', 'SLOGAN'),
        ('hdr', 'Colors'), ('COLOR', 'Custom Letter Color'),
        ('hdr', 'Frame & Dirt'), ('FRAME', 'Plastic Frame'), ('FLIES', 'Flies')]

def fmt(k, v):
    if k == 'FONT': return str(v)
    if k == 'HEIGHT': return f'{v*1000:.1f} mm'
    return v

def draw_panel(d, active=None, cursor=False, pressed=False):
    d.rectangle((0, 0, PW, H), fill=BG)
    d.rectangle((0, 0, PW, 44), fill=(35, 35, 35))
    d.text((18, 12), 'Modifiers', font=f_uib, fill=TXT)
    d.rounded_rectangle((14, 58, PW-14, 96), 6, fill=PANEL)
    d.text((28, 67), 'GeometryNodes', font=f_uib, fill=TXT)
    d.text((PW-200, 68), 'LicensePlate_US_Base', font=f_hd, fill=DIM)
    y = 112; boxes = {}
    for key, label in ROWS:
        if key == 'hdr':
            d.polygon([(26, y+9), (38, y+9), (32, y+17)], fill=(200, 200, 200))
            d.text((46, y+2), label, font=f_uib, fill=TXT); y += 36; continue
        fx0, fx1 = 210, PW-22
        d.text((fx0-12-d.textlength(label, font=f_ui), y+5), label, font=f_ui, fill=TXT if key == active else (205, 205, 205))
        v = state[key]
        if key in ('FRAME', 'FLIES'):
            bx = (fx0, y+4, fx0+20, y+24)
            d.rounded_rectangle(bx, 4, fill=BLUE if v else FIELD, outline=(255,255,255) if key == active else None, width=2)
            if v: d.line([(fx0+4, y+14), (fx0+9, y+19), (fx0+17, y+8)], fill='white', width=3)
            boxes[key] = bx
        elif key == 'COLOR':
            bx = (fx0, y+2, fx1, y+27)
            d.rounded_rectangle(bx, 5, fill=lin2srgb(v), outline=(255,255,255) if key == active else None, width=2)
            boxes[key] = bx
        else:
            bx = (fx0, y+2, fx1, y+27)
            act = key == active
            d.rounded_rectangle(bx, 5, fill=FIELD_HI if act else FIELD, outline=BLUE if act else None, width=2)
            s = fmt(key, v)
            if key in ('FONT', 'HEIGHT'):
                tw = d.textlength(s, font=f_ui); d.text(((fx0+fx1)/2-tw/2, y+5), s, font=f_ui, fill=TXT)
                d.text((fx0+8, y+3), '‹', font=f_uib, fill=DIM); d.text((fx1-16, y+3), '›', font=f_uib, fill=DIM)
            else:
                d.text((fx0+10, y+5), s, font=f_ui, fill=TXT)
                if act and cursor:
                    cx = fx0+10+d.textlength(s, font=f_ui)+1; d.line([(cx, y+6), (cx, y+23)], fill=TXT, width=2)
            boxes[key] = bx
        y += 38
    if active == 'FONT':
        d.text((210, boxes['FONT'][3]+2), FONTS[state['FONT']], font=f_hd, fill=(120, 160, 220))
    return boxes

def arrow(d, x, y):
    pts = [(x, y), (x, y+22), (x+6, y+17), (x+10, y+26), (x+14, y+24), (x+10, y+16), (x+17, y+16)]
    d.polygon(pts, fill='white', outline='black')

plates = [Image.open(os.path.join(G, f'step_{i:02d}.png')).convert('RGB') for i in range(10)]
RW = W - PW - 90
plates = [p.resize((RW, int(p.height*RW/p.width)), Image.LANCZOS) for p in plates]
PY = 34

frames, durs = [], []
def frame(plate, caption, sub='', active=None, cursor=False, ms=80, blend_from=None, t=1.0, pointer=True):
    im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
    boxes = draw_panel(d, active, cursor)
    p = plate if blend_from is None else Image.blend(blend_from, plate, t)
    im.paste(p, (PW+45, PY))
    tw = d.textlength(caption, font=f_cap); cx = PW + (W-PW)/2
    d.text((cx-tw/2, H-92), caption, font=f_cap, fill=(25, 30, 45))
    if sub:
        sw = d.textlength(sub, font=f_sub); d.text((cx-sw/2, H-54), sub, font=f_sub, fill=(110, 115, 125))
    if active and pointer:
        b = boxes[active]; arrow(d, b[2]-40 if active not in ('FRAME', 'FLIES') else b[0]+12, b[1]+12)
    frames.append(im); durs.append(ms)

cur = plates[0]
frame(cur, 'US License Plate Generator', 'Blender Geometry Nodes · change a parameter, see the result', ms=1800)

def reveal(i, caption, sub, key):
    global cur
    new = plates[i]
    for t in (0.33, 0.66, 1.0):
        frame(new, caption, sub, active=key, blend_from=cur, t=t, ms=60)
    frame(new, caption, sub, active=key, ms=1700)
    cur = new

def typing(key, new, i, caption, sub):
    old = state[key]
    frame(cur, caption, sub, active=key, cursor=True, ms=500)
    for n in range(len(old)-1, -1, -1):
        state[key] = old[:n]; frame(cur, caption, sub, active=key, cursor=True, ms=45)
    for n in range(1, len(new)+1):
        state[key] = new[:n]; frame(cur, caption, sub, active=key, cursor=True, ms=110)
    frame(cur, caption, sub, active=key, cursor=False, ms=250)
    reveal(i, caption, sub, key)

def value(key, new, i, caption, sub, steps=6):
    old = state[key]
    frame(cur, caption, sub, active=key, ms=500)
    for s in range(1, steps+1):
        if isinstance(old, tuple): state[key] = tuple(o+(n-o)*s/steps for o, n in zip(old, new))
        elif isinstance(old, int) and isinstance(new, int): state[key] = round(old+(new-old)*s/steps)
        else: state[key] = old+(new-old)*s/steps
        frame(cur, caption, sub, active=key, ms=90)
    state[key] = new
    reveal(i, caption, sub, key)

def toggle(key, i, caption, sub):
    frame(cur, caption, sub, active=key, ms=600)
    state[key] = True
    frame(cur, caption, sub, active=key, ms=200)
    reveal(i, caption, sub, key)

typing('WRITING', 'BLENDER', 1, 'Type any registration', 'WRITING → BLENDER')
value('FONT', 2, 2, 'Six built-in fonts or your own', 'Font Index 0 → 2', steps=2)
value('FONT', 4, 3, 'Six built-in fonts or your own', 'Font Index 2 → 4', steps=2)
value('HEIGHT', 0.0, 4, 'Flat printed letters', 'Letters Height 1.2 mm → 0 mm')
value('HEIGHT', 0.003, 5, 'Deep embossed letters', 'Letters Height 0 mm → 3 mm')
value('COLOR', (0.55, 0.012, 0.02), 6, 'Separate colors for every part', 'Custom Letter Color → red')
typing('SLOGAN', 'GEOMETRY NODES', 7, 'Edit the state and slogan lines', 'SLOGAN → GEOMETRY NODES')
toggle('FRAME', 8, 'Plastic dealer frame in one click', 'Plastic Frame → on')
toggle('FLIES', 9, 'Road dirt & flies in one click', 'Flies → on')
durs[-1] = 3000

pal = [f.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG) for f in frames]
pal[0].save(OUT, save_all=True, append_images=pal[1:], duration=durs, loop=0, optimize=True, disposal=1)
print(len(frames), 'frames', sum(durs)/1000, 's')

# MP4 (H.264) with the same timing, for Instagram / Superhive video
import subprocess, tempfile
tmp = tempfile.mkdtemp(dir=G)
lst = []
for k, (f, ms) in enumerate(zip(frames, durs)):
    fp = os.path.join(tmp, f'{k:04d}.png'); f.save(fp); lst.append(f"file '{fp}'\nduration {ms/1000:.3f}")
lst.append(f"file '{fp}'")
open(os.path.join(tmp, 'list.txt'), 'w').write('\n'.join(lst))
mp4 = OUT[:-4] + '.mp4'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', os.path.join(tmp, 'list.txt'),
                '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264', '-crf', '18', '-movflags', '+faststart', mp4], check=True)
print('mp4', mp4)

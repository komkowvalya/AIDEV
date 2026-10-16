import bpy, sys, os, json, time
from PIL import Image
blend, outdir = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
STEPS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gif_steps.json')))
bpy.ops.wm.open_mainfile(filepath=blend)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 10
sc.cycles.use_adaptive_sampling = True; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1200, 700, 100
sc.render.film_transparent = True
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
o = bpy.data.objects['CA']
for p in bpy.data.objects:
    if p.modifiers.get('GeometryNodes'): p.hide_render = p is not o
ng = o.modifiers['GeometryNodes'].node_group
ident = {i.name: i.identifier for i in ng.interface.items_tree if i.item_type == 'SOCKET' and i.in_out == 'INPUT'}
def setv(k, v):
    getattr(o.modifiers['GeometryNodes'].properties.inputs, ident[k]).value = tuple(v) if isinstance(v, list) else v
LENS = 135.0
cd = bpy.data.cameras.new('GifCam'); cd.lens = LENS; cd.sensor_fit = 'HORIZONTAL'; cd.sensor_width = 36
cam = bpy.data.objects.new('GifCam', cd); sc.collection.objects.link(cam); sc.camera = cam
dist = (0.3188 / 0.86) * LENS / 36       # frame width fits too
cam.location = (o.location.x, o.location.y - 0.006, dist)
for i, step in enumerate(STEPS):
    for k, v in step['set'].items(): setv(k, v)
    out = os.path.join(outdir, f'step_{i:02d}.png')
    if os.path.exists(out): continue
    sc.render.filepath = out; t = time.time()
    bpy.ops.render.render(write_still=True)
    im = Image.open(out).convert('RGBA'); bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
    Image.alpha_composite(bg, im).convert('RGB').save(out)
    print(f'STEP {i} {time.time()-t:.0f}s', flush=True)

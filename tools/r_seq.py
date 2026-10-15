import bpy, sys, os, math, time
blend, outdir = sys.argv[1], sys.argv[2]
only = sys.argv[3].split(',') if len(sys.argv) > 3 and sys.argv[3] else None
samples = int(sys.argv[4]) if len(sys.argv) > 4 else 128
bpy.ops.wm.open_mainfile(filepath=blend)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.cycles.samples = samples; sc.cycles.use_adaptive_sampling = True; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 2000, 1085, 100
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGB'
# camera straight above the plate; 135 mm so the plate fills ~89 % of the width like the reference
LENS, WIDTH_FRAC, PLATE_W = 135.0, 0.895, 0.3048
cd = bpy.data.cameras.new('SeqCam'); cd.lens = LENS; cd.sensor_fit = 'HORIZONTAL'; cd.sensor_width = 36
cam = bpy.data.objects.new('SeqCam', cd); sc.collection.objects.link(cam); sc.camera = cam
dist = (PLATE_W / WIDTH_FRAC) * LENS / 36
plates = sorted([o for o in bpy.data.objects if o.modifiers.get('GeometryNodes') and o.name != '00_Start'],
                key=lambda o: o.name.split('.')[0])
for o in plates: o.hide_render = True
bpy.data.objects['00_Start'].hide_render = True
for i, o in enumerate(plates, 1):
    code = o.name.split('.')[0]
    if only and code not in only: continue
    if os.path.exists(os.path.join(outdir, f'{i:04d}_{code}.png')): continue
    o.hide_render = False
    cam.location = (o.location.x, o.location.y, o.location.z + dist); cam.rotation_euler = (0, 0, 0)
    sc.render.filepath = os.path.join(outdir, f'{i:04d}_{code}.png')
    t = time.time(); bpy.ops.render.render(write_still=True)
    print(f'FRAME {i:04d} {code} {time.time()-t:.0f}s', flush=True)
    o.hide_render = True

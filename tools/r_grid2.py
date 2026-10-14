import bpy, sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from rlib import *
blend, out = sys.argv[1], sys.argv[2]
bpy.ops.wm.open_mainfile(filepath=blend)
# unpack fonts for the 2D layouts
for f in bpy.data.fonts:
    if f.packed_file:
        open(os.path.join(os.path.dirname(__file__),'fonts',os.path.basename(f.filepath)),'wb').write(f.packed_file.data)
sc=setup_scene(res=(4320,4000), samples=16, world=(1,1,1), strength=1.0)
sc.view_settings.view_transform='Standard'
sc.render.film_transparent=True
pos={}
for o in bpy.data.objects:
    if o.modifiers.get('GeometryNodes'):
        setin(o,'Bend angle',0.0)
        if o.name=='00_Start': o.hide_render=True
        else: pos[o.name]=(o.location.x,o.location.y)
json.dump(pos, open(out+'.json','w'))
cam((0.9,-0.8,3),(0.9,-0.8,0),ortho=2.1)

sc.render.filepath=out
bpy.ops.render.render(write_still=True)

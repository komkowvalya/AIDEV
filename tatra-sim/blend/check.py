import bpy, mathutils
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath='/tmp/claude-0/-home-user-AIDEV/657386d6-1b83-5ae1-9bb0-e87210cc6e85/scratchpad/blend/tatra_parts.glb')
sc=bpy.context.scene
cols={'cast':(0.32,0.35,0.38,1),'dark':(0.12,0.13,0.14,1),'steel':(0.7,0.7,0.72,1),'rubber':(0.03,0.03,0.03,1),'tyre':(0.03,0.03,0.03,1),'rim':(0.75,0.76,0.77,1)}
for m in bpy.data.materials:
    if m.name in cols: m.use_nodes=True; m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=cols[m.name]; m.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value=0.5 if m.name in('cast','steel','rim') else 0
objs={o.name:o for o in bpy.data.objects if o.type=='MESH'}
# assemble steered axle at y=0 (blender), fixed at y=3: right side as exported, left mirrored; wheels at x=0.92
def place(prefix,dx,dy,mirror=False):
    for n,o in objs.items():
        if n.startswith(prefix+'__'):
            c=o.copy(); sc.collection.objects.link(c); c.location=(dx,dy,0); c.scale=(-1 if mirror else 1,1,1)
for ax,y in [('steer',0),('fixed',3.0)]:
    place(ax+'_body',0,y)
    for m in [False,True]:
        s=-1 if m else 1
        place(ax+'_arm',0,y,m)
        if ax=='steer': place('steer_knuckle',s*0.80,y,m)
        place('wheel',s*0.92,y,m)
place('transfer',0,1.5)
for o in objs.values(): o.hide_render=True
sc.render.engine='CYCLES'; sc.cycles.samples=12; sc.render.resolution_x=1000; sc.render.resolution_y=620
world=bpy.data.worlds.new('w'); sc.world=world; world.use_nodes=True; world.node_tree.nodes['Background'].inputs[0].default_value=(0.9,0.9,0.92,1)
sun=bpy.data.objects.new('sun',bpy.data.lights.new('sun','SUN')); sun.data.energy=3; sc.collection.objects.link(sun); sun.rotation_euler=(0.7,0.2,0.9)
cam=bpy.data.objects.new('cam',bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera=cam
def shot(name,loc,target,lens):
    cam.location=loc; d=mathutils.Vector(target)-mathutils.Vector(loc); cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler(); cam.data.lens=lens
    sc.render.filepath='/tmp/claude-0/-home-user-AIDEV/657386d6-1b83-5ae1-9bb0-e87210cc6e85/scratchpad/blend/'+name+'.png'; bpy.ops.render.render(write_still=True)
shot('chk_overview',(4.5,-3.5,3.2),(0,1.5,0),30)
shot('chk_close',(2.0,-1.6,0.9),(0.6,0,0),35)

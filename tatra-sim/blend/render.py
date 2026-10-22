import bpy, math, mathutils
bpy.ops.wm.open_mainfile(filepath='/root/.claude/uploads/657386d6-1b83-5ae1-9bb0-e87210cc6e85/9bfb785c-Tatra_geometry_02.blend')
sc=bpy.context.scene
# bounds of everything
mn=mathutils.Vector((1e9,)*3); mx=-mn
for o in bpy.data.objects:
    if o.type!='MESH': continue
    for c in o.bound_box:
        w=o.matrix_world@mathutils.Vector(c); mn=mathutils.Vector(map(min,mn,w)); mx=mathutils.Vector(map(max,mx,w))
print('BOUNDS',tuple(round(v,3) for v in mn),tuple(round(v,3) for v in mx))
for coll in bpy.data.collections:
    a=mathutils.Vector((1e9,)*3); b=-a
    for o in coll.objects:
        for c in o.bound_box:
            w=o.matrix_world@mathutils.Vector(c); a=mathutils.Vector(map(min,a,w)); b=mathutils.Vector(map(max,b,w))
    print('CB',coll.name,tuple(round(v,3) for v in a),tuple(round(v,3) for v in b))
sc.render.engine='CYCLES'; sc.cycles.samples=12; sc.cycles.device='CPU'
sc.render.resolution_x=900; sc.render.resolution_y=600
world=bpy.data.worlds.new('w'); sc.world=world; world.use_nodes=True; world.node_tree.nodes['Background'].inputs[0].default_value=(0.8,0.8,0.82,1); world.node_tree.nodes['Background'].inputs[1].default_value=1.2
cam=bpy.data.objects.new('cam',bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera=cam
sun=bpy.data.objects.new('sun',bpy.data.lights.new('sun','SUN')); sun.data.energy=3; sc.collection.objects.link(sun); sun.rotation_euler=(0.6,0.2,0.8)
def shot(name,loc,target,lens=35):
    cam.location=loc; d=mathutils.Vector(target)-mathutils.Vector(loc); cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler(); cam.data.lens=lens
    sc.render.filepath='/tmp/claude-0/-home-user-AIDEV/657386d6-1b83-5ae1-9bb0-e87210cc6e85/scratchpad/blend/'+name+'.png'; bpy.ops.render.render(write_still=True)
c=(mn+mx)/2
shot('all',(c.x+6,c.y-7,c.z+5),tuple(c),30)
shot('steer',(2.6,-2.8,1.6),(0.3,0.3,0),35)
shot('fixed',(2.6,1.8,1.6),(0.3,4.6,0),35)
shot('top',(c.x,c.y,c.z+12),tuple(c),35)

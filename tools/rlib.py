import bpy, math, sys, mathutils
def setup_scene(res=(1200,700), samples=48, world=(0.6,0.62,0.66), strength=0.6):
    sc=bpy.context.scene
    sc.render.engine='CYCLES'
    sc.cycles.device='CPU'
    sc.cycles.samples=samples
    sc.cycles.use_denoising=True
    sc.cycles.use_adaptive_sampling=True
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage=100
    sc.render.image_settings.file_format='PNG'
    sc.view_settings.view_transform='AgX'
    sc.view_settings.look='None'
    if not sc.world: sc.world=bpy.data.worlds.new('W')
    w=sc.world; w.use_nodes=True
    bg=w.node_tree.nodes.get('Background')
    bg.inputs[0].default_value=(*world,1); bg.inputs[1].default_value=strength
    return sc
def area(name, loc, rot, size, energy, color=(1,1,1)):
    l=bpy.data.lights.new(name,'AREA'); l.size=size; l.energy=energy; l.color=color
    o=bpy.data.objects.new(name,l); bpy.context.scene.collection.objects.link(o)
    o.location=loc; o.rotation_euler=rot; return o
def cam(loc, target, lens=85, ortho=None):
    c=bpy.data.cameras.new('Cam'); c.lens=lens
    if ortho: c.type='ORTHO'; c.ortho_scale=ortho
    o=bpy.data.objects.new('Cam',c); bpy.context.scene.collection.objects.link(o)
    o.location=loc
    d=mathutils.Vector(target)-mathutils.Vector(loc)
    o.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
    bpy.context.scene.camera=o; return o
def solo(names):
    for o in bpy.data.objects:
        if o.type=='MESH' and o.name not in names and o.modifiers.get('GeometryNodes'):
            o.hide_render=True
def setin(o, name, val):
    ng=o.modifiers['GeometryNodes'].node_group
    for it in ng.interface.items_tree:
        if it.item_type=='SOCKET' and it.in_out=='INPUT' and it.name==name:
            getattr(o.modifiers['GeometryNodes'].properties.inputs, it.identifier).value=val; return
    raise KeyError(name)

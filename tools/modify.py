import bpy, sys, mathutils
src, dst = sys.argv[1], sys.argv[2]
bpy.ops.wm.open_mainfile(filepath=src)
ng = bpy.data.node_groups['LicensePlate_US_Base']
N = ng.nodes; L = ng.links
V = mathutils.Vector

def item(name):
    for it in ng.interface.items_tree:
        if it.item_type=='SOCKET' and it.in_out=='INPUT' and it.name==name: return it
    raise KeyError(name)

# ---------------------------------------------------------------- 1. delete old plastic frame geometry
for nm in ['Quadrilateral.006','Quadrilateral.007','Fillet Curve.006','Fillet Curve.007','Curve to Mesh','Cube',
           'Transform Geometry.016','Transform Geometry.017','Join Geometry.009','Set Material.008',
           'Combine XYZ.016','Combine XYZ.017','Combine XYZ.018','Combine XYZ.019','Combine XYZ.020'] + \
          [f'Math.{i:03d}' for i in range(93,103)]:
    N.remove(N[nm])

# ---------------------------------------------------------------- 2. bake removed inputs into constants
spec = N.new('NodeFrame'); spec.label = 'FIXED US SPECS  (former modifier inputs, baked)'; spec.name='Frame.Fixed'
spec.location = N['Group Input'].location + V((0, 400)) if not N['Group Input'].parent else V((-2600, 900))
cy = [0]
def const(name, value):
    it = item(name)
    links = [l for l in L if l.from_node.type=='GROUP_INPUT' and l.from_socket.identifier==it.identifier]
    if isinstance(value, bool):
        n = N.new('FunctionNodeInputBool'); n.boolean = value
    elif isinstance(value, tuple):
        n = N.new('FunctionNodeInputVector'); n.vector = value
    else:
        n = N.new('ShaderNodeValue'); n.outputs[0].default_value = value
    n.label = name; n.name = 'Fixed ' + name
    n.parent = spec; n.location = V((0, -cy[0])); cy[0] += 110
    for l in links: L.new(n.outputs[0], l.to_socket)
    ng.interface.remove(it)
    return n

const('Size X', 0.3048); const('Size Y', 0.1524); const('Corner Radius', 0.00635)
const('Plate Thickness', 0.0008); const('Bottom Holes', True)
const('Hole Spacing', (0.1778, 0.1207, 0.0)); const('Slot Size', (0.0135, 0.0071, 0.0))
const('Registration Position', (0.0, -0.004, 0.0)); const('Middle Gap', 0.034)
const('Width Scale', 1.0); const('Max Width', 0.25)
const('Ring plates_ON', False); const('Signs Translation Tune', (0.0, 0.0, 0.0)); const('Sign1 Position', (-0.118, 0.052, 0.0))
ng.interface.remove(item('Sign1'))

# ---------------------------------------------------------------- 3. remove month sticker + sticker wells, single sticker position
for nm in ['Object Info','Vector Math.007','Vector Math.008','Transform Geometry.005','Domain Size','Compare.008',
           'Boolean Math.008','Switch.004','Quadrilateral.002','Quadrilateral.003','Fillet Curve.002','Fillet Curve.003',
           'Join Geometry.003','Fill Curve.002','Vector Math.009','Transform Geometry.006',
           'Quadrilateral.004','Quadrilateral.005','Fillet Curve.004','Fillet Curve.005','Join Geometry.004','Fill Curve.003',
           'Transform Geometry.008','Domain Size.001','Compare.009','Boolean Math.009','Switch.005','Vector Math.012','Vector Math.010']:
    N.remove(N[nm])
gi6 = N['Group Input.006']
sp = item('Sign2 Position')
L.new(gi6.outputs[sp.identifier], N['Vector Math.011'].inputs[0])
it = item('Sign2'); it.name = 'Sticker'; it.description = 'Registration sticker object (empty = no sticker)'
sp.name = 'Sticker Position'; sp.description = 'Sticker centre on the plate (X, Y in metres)'
N['Frame.006'].label = 'STICKER + SEPARATOR SIGN'

# ---------------------------------------------------------------- 4. hide fixed header layout inputs
for nm in ['State Position', 'Slogan Position', 'Header Max Width']:
    item(nm).hide_in_modifier = True

# ---------------------------------------------------------------- 5. new plastic frame
F = N['Frame.010']; F.label = 'PLASTIC FRAME  (fixed to the 12" x 6" plate)'
base = N['Group.005'].location.copy()
def add(t, loc, **kw):
    n = N.new(t); n.parent = F; n.location = base + V(loc)
    for k, v in kw.items(): setattr(n, k, v)
    return n
def rrect(w, h, r, cy, loc):
    q = add('GeometryNodeCurvePrimitiveQuadrilateral', loc); q.mode='RECTANGLE'
    q.inputs['Width'].default_value = w; q.inputs['Height'].default_value = h
    f = add('GeometryNodeFilletCurve', (loc[0]+200, loc[1]))
    f.inputs['Mode'].default_value = 'Poly'; f.inputs['Radius'].default_value = r; f.inputs['Count'].default_value = 10
    L.new(q.outputs[0], f.inputs['Curve'])
    t = add('GeometryNodeTransform', (loc[0]+400, loc[1]))
    t.inputs['Translation'].default_value = (0, cy, 0)
    L.new(f.outputs[0], t.inputs['Geometry'])
    return t.outputs[0]
def slab(curves, z0, z1, loc, name):
    """Filled region between curves (even-odd), extruded from z0 to z1, closed at the bottom."""
    j = add('GeometryNodeJoinGeometry', loc)
    for c in reversed(curves): L.new(c, j.inputs[0])
    fc = add('GeometryNodeFillCurve', (loc[0]+200, loc[1])); fc.inputs['Fill Rule'].default_value = 'Even-Odd'
    L.new(j.outputs[0], fc.inputs['Curve'])
    tr = add('GeometryNodeTransform', (loc[0]+400, loc[1])); tr.inputs['Translation'].default_value = (0,0,z0)
    L.new(fc.outputs[0], tr.inputs['Geometry'])
    ex = add('GeometryNodeExtrudeMesh', (loc[0]+600, loc[1])); ex.mode='FACES'
    ex.inputs['Offset'].default_value = (0,0,1); ex.inputs['Offset Scale'].default_value = z1 - z0
    ex.inputs['Individual'].default_value = False
    L.new(tr.outputs[0], ex.inputs['Mesh'])
    fl = add('GeometryNodeFlipFaces', (loc[0]+600, loc[1]-180))
    L.new(tr.outputs[0], fl.inputs['Mesh'])
    jj = add('GeometryNodeJoinGeometry', (loc[0]+800, loc[1]))
    L.new(fl.outputs[0], jj.inputs[0]); L.new(ex.outputs[0], jj.inputs[0])
    mg = add('GeometryNodeMergeByDistance', (loc[0]+1000, loc[1])); mg.inputs['Distance'].default_value = 1e-6
    L.new(jj.outputs[0], mg.inputs['Geometry'])
    mg.label = name
    return mg.outputs[0]

PW, PH = 0.3048, 0.1524
SIDE, TOP, BOT = 0.007, 0.0085, 0.022       # frame margins around the plate
LIP = 0.003                                  # how much the frame overlaps the plate edge
ZB, ZBACK, ZLIP, ZTOP = -0.0045, -0.003, 0.0018, 0.0042
ow, oh = PW + 2*SIDE, PH + TOP + BOT
ocy = (TOP - BOT) / 2
outer  = rrect(ow, oh, 0.009, ocy, (0, -300))
outer2 = rrect(ow, oh, 0.009, ocy, (0, -500))
pocket = rrect(PW + 0.001, PH + 0.001, 0.0068, 0, (0, -700))
pocket2= rrect(PW + 0.001, PH + 0.001, 0.0068, 0, (0, -900))
pocket3= rrect(PW + 0.001, PH + 0.001, 0.0068, 0, (0, -1100))
opening= rrect(PW - 2*LIP, PH - 2*LIP, 0.0045, 0, (0, -1300))
wall = slab([outer, pocket], ZB, ZTOP, (700, -300), 'Frame wall')
lip  = slab([pocket2, opening], ZLIP, ZTOP, (700, -800), 'Frame lip')
back = slab([pocket3], ZB, ZBACK, (700, -1300), 'Frame back')
jf = add('GeometryNodeJoinGeometry', (1900, -700))
for s in (back, lip, wall): L.new(s, jf.inputs[0])
smp = add('GeometryNodeSetMaterial', (2100, -700)); smp.inputs['Material'].default_value = bpy.data.materials['LP_US_Plastic']
L.new(jf.outputs[0], smp.inputs['Geometry'])
L.new(smp.outputs[0], N['Join Geometry.011'].inputs[0])

# frame writings: positions on the top / bottom bars, sized to fit inside them
top_vis = (PH/2 - LIP, PH/2 + TOP)
bot_vis = (-PH/2 - BOT, -PH/2 + LIP)
zt = ZTOP + 0.00005
cfg = {'Group.006': (0.0032, 0.24, (0, (top_vis[0]+top_vis[1])/2, zt)),
       'Group.007': (0.0050, 0.26, (0, -0.0848, zt)),
       'Group.008': (0.0026, 0.24, (0, -0.0925, zt))}
for nm, (size, mw, pos) in cfg.items():
    g = N[nm]
    g.inputs['Size'].default_value = size
    g.inputs['Max Width'].default_value = mw
    g.inputs['Position'].default_value = pos
ex = add('GeometryNodeExtrudeMesh', (N['Join Geometry.010'].location.x - base.x + 200, -200)); ex.mode='FACES'
ex.inputs['Offset'].default_value = (0,0,1); ex.inputs['Offset Scale'].default_value = 0.00012
L.new(N['Join Geometry.010'].outputs[0], ex.inputs['Mesh'])
L.new(ex.outputs[0], N['Set Material.009'].inputs['Geometry'])

# ---------------------------------------------------------------- 6. remove dead nodes
changed = True
while changed:
    changed = False
    for n in list(N):
        if n.type in ('FRAME', 'GROUP_OUTPUT', 'GROUP_INPUT'): continue
        if not any(o.is_linked for o in n.outputs):
            N.remove(n); changed = True
for n in list(N):   # group input nodes with nothing connected
    if n.type == 'GROUP_INPUT' and not any(o.is_linked for o in n.outputs): N.remove(n)

# ---------------------------------------------------------------- 7. per-state text fixes (current real plates)
def setv(o, name, v):
    getattr(o.modifiers['GeometryNodes'].properties.inputs, item(name).identifier).value = v
O = bpy.data.objects
setv(O['AL'], 'SLOGAN', 'WWW.ALABAMA.TRAVEL')
setv(O['DC'], 'STATE', 'WASHINGTON, DC'); setv(O['DC'], 'State Size', 0.016)
setv(O['KS'], 'SLOGAN', 'TO THE STARS')
setv(O['ND'], 'SLOGAN', 'PEACE GARDEN STATE')
setv(O['OK'], 'SLOGAN', 'EXPLORE OKLAHOMA')

bpy.ops.wm.save_as_mainfile(filepath=dst, compress=True)
print("SAVED", dst, len(N), "nodes")

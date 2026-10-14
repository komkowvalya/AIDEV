import bpy, sys, mathutils
src, dst = sys.argv[1], sys.argv[2]
bpy.ops.wm.open_mainfile(filepath=src)
V = mathutils.Vector
g = bpy.data.node_groups['LP_US_Flies']
N, L = g.nodes, g.links
for n in list(N):
    if n.type not in ('GROUP_INPUT', 'GROUP_OUTPUT'): N.remove(n)
gi = [n for n in N if n.type=='GROUP_INPUT'][0]; go = [n for n in N if n.type=='GROUP_OUTPUT'][0]
gi.location = (-1600, 0); go.location = (1400, 0)
def add(t, x, y, label=None, **inp):
    n = N.new(t); n.location = (x, y)
    if label: n.label = label
    for k, v in inp.items():
        if k.startswith('_'): setattr(n, k[1:], v)
        else: n.inputs[k.replace('__', ' ')].default_value = v
    return n
def frame(label, nodes):
    f = N.new('NodeFrame'); f.label = label
    for n in nodes: n.parent = f
    return f
def math(op, x, y, a=None, b=None, label=None, clamp=False):
    n = add('ShaderNodeMath', x, y, label, _operation=op); n.use_clamp = clamp
    for i, v in enumerate((a, b)):
        if v is None: continue
        if isinstance(v, (int, float)): n.inputs[i].default_value = v
        else: L.new(v, n.inputs[i])
    return n.outputs[0]
def mrange(val, fmin, fmax, tmin, tmax, x, y, smooth=True, label=None):
    n = add('ShaderNodeMapRange', x, y, label); n.interpolation_type = 'SMOOTHSTEP' if smooth else 'LINEAR'
    for sock, v in (('From Min', fmin), ('From Max', fmax), ('To Min', tmin), ('To Max', tmax)):
        if isinstance(v, (int, float)): n.inputs[sock].default_value = v
        else: L.new(v, n.inputs[sock])
    L.new(val, n.inputs['Value']); return n.outputs['Result']

# --- coordinates (object space, random offset per object so plates don't share the same dirt)
tc  = add('ShaderNodeTexCoord', -1400, 300)
oi  = add('ShaderNodeObjectInfo', -1400, 50)
rnd = add('ShaderNodeVectorMath', -1200, 50, _operation='SCALE'); L.new(oi.outputs['Random'], rnd.inputs[0]); rnd.inputs['Scale'].default_value = 37.0
off = add('ShaderNodeVectorMath', -1000, 200, _operation='ADD'); L.new(tc.outputs['Object'], off.inputs[0]); L.new(rnd.outputs[0], off.inputs[1])
P = off.outputs[0]
amt = add('ShaderNodeAttribute', -1400, -250, 'Flies on/off'); amt.attribute_name = 'Flies'; amt.attribute_type = 'GEOMETRY'
sep = add('ShaderNodeSeparateXYZ', -1200, 400); L.new(tc.outputs['Object'], sep.inputs[0])

# --- road grime: patchy, heavier towards the bottom and the side edges
nA = add('ShaderNodeTexNoise', -800, 500, 'grime noise', Scale=7.0, Detail=10.0, Roughness=0.62, Distortion=0.35); L.new(P, nA.inputs['Vector'])
bottom = mrange(sep.outputs['Y'], -0.085, 0.03, 1.0, 0.0, -800, 300, label='bottom build-up')
ax = math('ABSOLUTE', -950, 150, sep.outputs['X'])
edge = mrange(ax, 0.11, 0.165, 0.0, 1.0, -800, 150, label='edge build-up')
be = math('MAXIMUM', -600, 250, bottom, edge)
w  = math('MULTIPLY_ADD', -450, 250, be, 0.6)  # 0.6*be + 0.4
madd = w.node; madd.inputs[2].default_value = 0.4
gm = math('MULTIPLY', -300, 400, nA.outputs['Fac'], w)
grime = mrange(gm, 0.30, 0.62, 0.0, 0.45, -150, 400, label='grime mask')
nS = add('ShaderNodeTexNoise', -800, -50, 'mud speckles', Scale=260.0, Detail=1.5, Roughness=0.5); L.new(P, nS.inputs['Vector'])
spk = mrange(nS.outputs['Fac'], 0.66, 0.74, 0.0, 0.9, -600, -50, label='speckle mask')
spk = math('MULTIPLY', -450, -50, spk, be)
dirt = math('MAXIMUM', 0, 300, grime, spk)
dirt = math('MULTIPLY', 150, 300, dirt, amt.outputs['Fac'], label='DIRT')

# --- squashed bugs: irregular blobs with a lighter smeared halo
nD = add('ShaderNodeTexNoise', -800, -350, 'splat distortion', Scale=120.0, Detail=3.0, Roughness=0.6); L.new(P, nD.inputs['Vector'])
dv = add('ShaderNodeVectorMath', -600, -350, _operation='MULTIPLY_ADD'); L.new(nD.outputs['Color'], dv.inputs[0])
dv.inputs[1].default_value = (0.006, 0.006, 0.006); dv.inputs[2].default_value = (-0.003, -0.003, -0.003)
pd = add('ShaderNodeVectorMath', -450, -350, _operation='ADD'); L.new(P, pd.inputs[0]); L.new(dv.outputs[0], pd.inputs[1])
vor = add('ShaderNodeTexVoronoi', -300, -350, 'bug cells', Scale=26.0, Randomness=1.0); vor.voronoi_dimensions = '2D'; L.new(pd.outputs[0], vor.inputs['Vector'])
cs = add('ShaderNodeSeparateColor', -100, -550); L.new(vor.outputs['Color'], cs.inputs['Color'])
size = math('MULTIPLY_ADD', 50, -550, cs.outputs['Red'], 0.085); size.node.inputs[2].default_value = 0.03
present = math('GREATER_THAN', 50, -700, cs.outputs['Green'], 0.62)
s85 = math('MULTIPLY', 200, -450, size, 0.7)
body = mrange(vor.outputs['Distance'], s85, size, 1.0, 0.0, 350, -350, label='bug body')
s25 = math('MULTIPLY', 200, -600, size, 1.9)
halo = mrange(vor.outputs['Distance'], size, s25, 0.4, 0.0, 350, -550, label='bug smear')
pa = math('MULTIPLY', 500, -700, present, amt.outputs['Fac'])
body = math('MULTIPLY', 650, -350, body, pa, label='BUG BODY')
halo = math('MULTIPLY', 650, -550, halo, pa, label='BUG SMEAR')

bump = add('ShaderNodeBump', 800, -750, Strength=0.5, Distance=0.0004)
hb = math('MULTIPLY_ADD', 650, -750, halo, 0.3); L.new(body, hb.node.inputs[2])
L.new(hb, bump.inputs['Height'])

def bsdf(x, y, col, rough, label):
    b = add('ShaderNodeBsdfPrincipled', x, y, label); b.inputs['Base Color'].default_value = col
    b.inputs['Roughness'].default_value = rough; return b
dB = bsdf(500, 650, (0.11, 0.09, 0.065, 1), 0.85, 'Dirt')
hB = bsdf(950, -150, (0.27, 0.22, 0.09, 1), 0.3, 'Bug smear'); L.new(bump.outputs['Normal'], hB.inputs['Normal'])
bB = bsdf(950, -650, (0.03, 0.02, 0.012, 1), 0.22, 'Bug body'); L.new(bump.outputs['Normal'], bB.inputs['Normal'])
m1 = add('ShaderNodeMixShader', 800, 200); L.new(dirt, m1.inputs[0]); L.new(gi.outputs[0], m1.inputs[1]); L.new(dB.outputs[0], m1.inputs[2])
m2 = add('ShaderNodeMixShader', 1050, 150); L.new(halo, m2.inputs[0]); L.new(m1.outputs[0], m2.inputs[1]); L.new(hB.outputs[0], m2.inputs[2])
m3 = add('ShaderNodeMixShader', 1250, 100); L.new(body, m3.inputs[0]); L.new(m2.outputs[0], m3.inputs[1]); L.new(bB.outputs[0], m3.inputs[2])
L.new(m3.outputs[0], go.inputs[0])

# --- give the frame, sticker and signs the same dirt so the whole plate ages together
for mn in ['LP_US_Plastic','LP_US_Frame_Writing','LP_US_Chrome','LP_US_Sticker_Year','LP_US_Sticker_Month',
           'LP_US_Sign_FL_Orange','LP_US_Sign_GA_Peach','LP_US_Sign_NM_Zia','LP_US_Sign_PA_Keystone']:
    m = bpy.data.materials[mn]; nt = m.node_tree
    out = [n for n in nt.nodes if n.type=='OUTPUT_MATERIAL'][0]
    if any(n.type=='GROUP' and n.node_tree==g for n in nt.nodes): continue
    lk = out.inputs['Surface'].links[0]; src_sock = lk.from_socket
    gn = nt.nodes.new('ShaderNodeGroup'); gn.node_tree = g; gn.location = out.location + V((-200, -150))
    nt.links.new(src_sock, gn.inputs[0]); nt.links.new(gn.outputs[0], out.inputs['Surface'])

pl = bpy.data.materials['LP_US_Plastic'].node_tree.nodes['Principled BSDF']
pl.inputs['Roughness'].default_value = 0.45; pl.inputs['Coat Weight'].default_value = 0.08
pl.inputs['Base Color'].default_value = (0.012, 0.012, 0.012, 1)
bpy.ops.wm.save_as_mainfile(filepath=dst, compress=True)
print("SAVED")

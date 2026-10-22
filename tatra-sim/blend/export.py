import bpy, bmesh, mathutils, math
SRC='/root/.claude/uploads/657386d6-1b83-5ae1-9bb0-e87210cc6e85/9bfb785c-Tatra_geometry_02.blend'
OUT='/tmp/claude-0/-home-user-AIDEV/657386d6-1b83-5ae1-9bb0-e87210cc6e85/scratchpad/blend/tatra_parts.glb'
bpy.ops.wm.open_mainfile(filepath=SRC)
KP=0.80; WX=0.92; WHEEL_C=1.659
def cat(mname):
    n=(mname or '').lower()
    if 'rubber black' in n: return 'tyre'
    if 'metal - casted' in n: return 'rim'
    if 'rubber' in n: return 'rubber'
    if 'screw' in n: return 'steel'
    if 'cover' in n or 'engine' in n: return 'dark'
    return 'cast'
# group -> (origin in blender coords, target faces)
GROUPS={'steer_body':((0,0,0),14000),'steer_arm':((0,0,0),7000),'steer_knuckle':((KP,0,0),7000),
        'fixed_body':((0,4.636,0),7000),'fixed_arm':((0,4.636,0),8000),'transfer':((0,2.6,0),5000),'wheel':((WHEEL_C,0,0),12000)}
buckets={g:bmesh.new() for g in GROUPS}
def classify(coll,cx,cy,cz,obj):
    if coll=='wheel': return 'wheel'
    if coll=='Prevod' or obj=='Geometry.002': return 'transfer'
    if coll=='Rizena':
        if abs(cy)>1.3: return None
        if abs(cx)<0.22: return 'steer_body'
        if cx<0: return None                      # left side comes from mirroring the right
        return 'steer_knuckle' if cx>=0.84 else 'steer_arm'
    if coll=='Nerizena':
        if abs(cx)<0.22: return 'fixed_body'
        if cx<0: return None
        return 'fixed_arm'
for cname in ['Rizena','Nerizena','Prevod','wheel']:
    for o in bpy.data.collections[cname].objects:
        bm=bmesh.new(); bm.from_mesh(o.data); bm.transform(o.matrix_world); bm.verts.ensure_lookup_table(); bm.faces.ensure_lookup_table()
        mats=[m.name if m else '' for m in o.data.materials]
        seen=set()
        for v in bm.verts:
            if v.index in seen: continue
            stack=[v]; seen.add(v.index); comp=[]
            while stack:
                a=stack.pop(); comp.append(a)
                for e in a.link_edges:
                    b=e.other_vert(a)
                    if b.index not in seen: seen.add(b.index); stack.append(b)
            xs=[p.co.x for p in comp]; ys=[p.co.y for p in comp]; zs=[p.co.z for p in comp]
            diag=math.dist((min(xs),min(ys),min(zs)),(max(xs),max(ys),max(zs)))
            if diag<0.05 and cname!='wheel': continue        # bolts, washers, clips
            g=classify(cname,sum(xs)/len(xs),sum(ys)/len(ys),sum(zs)/len(zs),o.name)
            if not g: continue
            faces={f for p in comp for f in p.link_faces}
            dst=buckets[g]; vmap={}
            for f in faces:
                vs=[]
                for lv in f.verts:
                    if lv.index not in vmap: vmap[lv.index]=dst.verts.new(lv.co)
                    vs.append(vmap[lv.index])
                try:
                    nf=dst.faces.new(vs); nf.material_index=['cast','dark','steel','rubber','tyre','rim'].index(cat(mats[f.material_index] if f.material_index<len(mats) else ''))
                except ValueError: pass
        bm.free()
# build objects: one per (group, material category); decimate per group budget
for o in list(bpy.data.objects): bpy.data.objects.remove(o)
CATS=['cast','dark','steel','rubber','tyre','rim']
stats={}
for g,(org,target) in GROUPS.items():
    bm=buckets[g]; bmesh.ops.translate(bm,verts=bm.verts,vec=-mathutils.Vector(org))
    bmesh.ops.remove_doubles(bm,verts=bm.verts,dist=0.0002)
    bmesh.ops.dissolve_degenerate(bm,dist=0.0005,edges=bm.edges)
    bmesh.ops.triangulate(bm,faces=bm.faces); total=len(bm.faces); stats[g]=[total]
    for ci,cn in enumerate(CATS):
        sub=bm.copy(); bmesh.ops.delete(sub,geom=[f for f in sub.faces if f.material_index!=ci],context='FACES')
        bmesh.ops.delete(sub,geom=[v for v in sub.verts if not v.link_faces],context='VERTS')
        if not sub.faces: sub.free(); continue
        bmesh.ops.dissolve_limit(sub,angle_limit=math.radians(0.5),verts=sub.verts,edges=sub.edges,delimit={'MATERIAL'})
        bmesh.ops.triangulate(sub,faces=sub.faces)
        me=bpy.data.meshes.new(f'{g}__{cn}'); sub.to_mesh(me); sub.free()
        ob=bpy.data.objects.new(f'{g}__{cn}',me); bpy.context.scene.collection.objects.link(ob)
        mat=bpy.data.materials.get(cn) or bpy.data.materials.new(cn); me.materials.append(mat)
        bpy.context.view_layer.objects.active=ob; ob.select_set(True)
        share=target*len(me.polygons)/max(1,total)   # this material's share of the group budget
        n=len(me.polygons)
        if (g!='wheel' or cn=='rim') and n>share:
            m=ob.modifiers.new('dec','DECIMATE'); m.ratio=max(0.4,share/n); m.use_collapse_triangulate=True
            bpy.ops.object.modifier_apply(modifier=m.name)
        bpy.ops.object.shade_smooth_by_angle(angle=math.radians(40))
        ob.select_set(False)
        stats[g].append((cn,len(me.polygons)))
for g,s in stats.items(): print('STAT',g,s)
# compact binary: per mesh uint16 positions quantized to the bbox, int8 normals, uint16/uint32 indices; game frame = (x, z, -y)
import struct, json, gzip
heads=[]; blob=bytearray()
def pad4():
    while len(blob)%4: blob.append(0)
for ob in sorted([o for o in bpy.data.objects if o.type=='MESH'],key=lambda o:o.name):
    me=ob.data; me.calc_loop_triangles()
    try: me.calc_normals_split()
    except Exception: pass
    verts=[]; key={}; idx=[]
    for t in me.loop_triangles:
        tri=[]
        for li in t.loops:
            l=me.loops[li]; v=me.vertices[l.vertex_index].co; n=l.normal
            q=(l.vertex_index,round(n.x*60),round(n.y*60),round(n.z*60))
            k=key.get(q)
            if k is None: k=key[q]=len(verts); verts.append(((v.x,v.z,-v.y),(n.x,n.z,-n.y)))
            tri.append(k)
        idx+=tri if True else tri
    if not verts: continue
    mn=[min(v[0][a] for v in verts) for a in range(3)]; mx=[max(v[0][a] for v in verts) for a in range(3)]
    pad4(); po=len(blob)
    for (p,_) in verts:
        for a in range(3): blob+=struct.pack('<H',int(round((p[a]-mn[a])/max(1e-9,mx[a]-mn[a])*65535)))
    pad4(); no=len(blob)
    for (_,n) in verts:
        for a in range(3): blob+=struct.pack('<b',max(-127,min(127,int(round(n[a]*127)))))
    pad4(); io=len(blob); big=len(verts)>65535
    for i in idx: blob+=struct.pack('<I' if big else '<H',i)
    heads.append(dict(name=ob.name,nv=len(verts),ni=len(idx),mn=[round(x,5) for x in mn],mx=[round(x,5) for x in mx],po=po,no=no,io=io,big=big))
    print('MESH',ob.name,len(verts),len(idx)//3)
hj=json.dumps(heads).encode(); out=struct.pack('<I',len(hj))+hj
while len(out)%4: out+=b' '
out+=bytes(blob)
gz=gzip.compress(out,9)
open(OUT.replace('.glb','.bin.gz'),'wb').write(gz)
print('BIN',len(out),'GZ',len(gz),'tris',sum(h['ni'] for h in heads)//3)
bpy.ops.export_scene.gltf(filepath=OUT,export_format='GLB',export_yup=True,export_materials='PLACEHOLDER',export_normals=True,export_texcoords=False,export_apply=True)
print('DONE')

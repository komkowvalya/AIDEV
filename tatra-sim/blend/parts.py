import bpy, bmesh, mathutils, json
bpy.ops.wm.open_mainfile(filepath='/root/.claude/uploads/657386d6-1b83-5ae1-9bb0-e87210cc6e85/9bfb785c-Tatra_geometry_02.blend')
out={}
for cname in ['Rizena','Nerizena','Prevod','wheel']:
    comps=[]
    for o in bpy.data.collections[cname].objects:
        bm=bmesh.new(); bm.from_mesh(o.data); bm.transform(o.matrix_world); bm.verts.ensure_lookup_table()
        seen=set()
        for v in bm.verts:
            if v.index in seen: continue
            stack=[v]; seen.add(v.index); idx=[]
            while stack:
                a=stack.pop(); idx.append(a)
                for e in a.link_edges:
                    b=e.other_vert(a)
                    if b.index not in seen: seen.add(b.index); stack.append(b)
            xs=[p.co.x for p in idx]; ys=[p.co.y for p in idx]; zs=[p.co.z for p in idx]
            nf=len({f.index for p in idx for f in p.link_faces})
            comps.append(dict(o=o.name,n=len(idx),f=nf,c=[round(sum(xs)/len(xs),3),round(sum(ys)/len(ys),3),round(sum(zs)/len(zs),3)],mn=[round(min(xs),3),round(min(ys),3),round(min(zs),3)],mx=[round(max(xs),3),round(max(ys),3),round(max(zs),3)]))
        bm.free()
    out[cname]=comps
    print(cname,'components',len(comps),'faces',sum(c['f'] for c in comps))
json.dump(out,open('/tmp/claude-0/-home-user-AIDEV/657386d6-1b83-5ae1-9bb0-e87210cc6e85/scratchpad/blend/parts.json','w'))

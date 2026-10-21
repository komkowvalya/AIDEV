import json, math, base64
import numpy as np
from PIL import Image
D='/tmp/claude-0/-home-user-AIDEV/657386d6-1b83-5ae1-9bb0-e87210cc6e85/scratchpad/map/'
J=json.load(open(D+'snapped.json')); S=J['S']; W,H=J['size']
CX,CY=575,589
m=lambda p:[round((p[0]-CX)*S,1),round((p[1]-CY)*S,1)]
roads=[dict(n=r['name'],k=r['kind'],w=r['w'],c=r['closed'],p=[m(q) for q in r['pts']]) for r in J['roads']]
a=np.asarray(Image.open(D+'crop.png').convert('RGB')).astype(float)
mx=a.max(-1)
forest=(mx<112)&(a[...,1]>a[...,0]+14)&(a[...,2]>a[...,0]+20)
forest[:,:300]=False
forest[0:110,860:]=False; forest[390:445,950:]=False; forest[392:445,1060:]=True; forest[790:852,860:]=True
cell=8/S; cw=int(W/cell); ch=int(H/cell)
fm=np.zeros((ch,cw),bool)
for j in range(ch):
    for i in range(cw):
        blk=forest[int(j*cell):int((j+1)*cell), int(i*cell):int((i+1)*cell)]
        fm[j,i]=blk.mean()>0.5
bits=np.packbits(fm.flatten())
Image.fromarray((fm*255).astype(np.uint8)).resize((cw*4,ch*4)).save(D+'forest.png')
out=dict(S=round(S,4),size=[round(W*S),round(H*S)],roads=roads,
  pads=[dict(n=n,c=m((x,y)),r=round(r*S,1)) for n,x,y,r in J['pads']],
  lots=[dict(n=n,p=[m(q) for q in p]) for n,p in J['lots']],
  build=[[*m((x0,y0)),*m((x1,y1)),h] for x0,y0,x1,y1,h in J['build']],
  forest=dict(cell=8,w=cw,h=ch,x0=round(-CX*S,1),z0=round(-CY*S,1),bits=base64.b64encode(bits.tobytes()).decode()))
open(D+'polygon.json','w').write(json.dumps(out,separators=(',',':')))
print(len(json.dumps(out)), 'bytes; forest cells', int(fm.sum()), 'grid', cw, ch)

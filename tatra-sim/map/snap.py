import math, json, sys
import numpy as np
from PIL import Image, ImageDraw
D='/tmp/claude-0/-home-user-AIDEV/657386d6-1b83-5ae1-9bb0-e87210cc6e85/scratchpad/map/'
exec(open(D+'trace.py').read())
a=np.asarray(Image.open(D+'crop.png').convert('RGB')).astype(float)
mx=a.max(-1); mn=a.min(-1); sat=(mx-mn)/(mx+1e-3)
light=(mx>140)&(sat<0.2)
dark=(mx<95)&(sat<0.4)&(a[...,2]>=a[...,1]-6)
H,W=light.shape
def dens(p,closed,step=5):
    pts=p+[p[0]] if closed else p; out=[]
    for i in range(len(pts)-1):
        (x0,y0),(x1,y1)=pts[i],pts[i+1]; n=max(1,int(math.dist(pts[i],pts[i+1])/step))
        for k in range(n): t=k/n; out.append((x0+(x1-x0)*t,y0+(y1-y0)*t))
    if not closed: out.append(pts[-1])
    return out
def snap(p,closed,mask,wpx,R=9):
    q=[]; n=len(p)
    for i in range(n):
        a0=p[(i-1)%n] if closed or i>0 else p[i]; a1=p[(i+1)%n] if closed or i<n-1 else p[i]
        tx,ty=a1[0]-a0[0],a1[1]-a0[1]; L=math.hypot(tx,ty) or 1; nx,ny=-ty/L,tx/L
        ts=np.arange(-R,R+1); xs=np.clip((p[i][0]+nx*ts).round().astype(int),0,W-1); ys=np.clip((p[i][1]+ny*ts).round().astype(int),0,H-1)
        v=mask[ys,xs]; runs=[]; s=None
        for k,b in enumerate(v):
            if b and s is None: s=k
            if (not b or k==len(v)-1) and s is not None:
                e=k if not b else k+1; runs.append((s,e)); s=None
        best=None
        for s0,e0 in runs:
            w=e0-s0
            if w<max(2,wpx*0.35) or w>wpx*3: continue
            c=ts[s0]+(w-1)/2; sc=abs(c)
            if best is None or sc<best[0]: best=(sc,c)
        q.append((best[1] if best else 0.0,nx,ny))
    # median-filter the normal displacements so a road shifts as a smooth whole
    ds=[t[0] for t in q]; out=[]
    for i in range(n):
        win=[ds[(i+j)%n] if closed else ds[min(n-1,max(0,i+j))] for j in range(-6,7)]
        d=sorted(win)[len(win)//2]; out.append((p[i][0]+q[i][1]*d,p[i][1]+q[i][2]*d))
    return out
def smooth(p,closed,k=3):
    n=len(p); out=[]
    for i in range(n):
        xs=[];ys=[]
        for j in range(-k,k+1):
            jj=(i+j)%n if closed else min(n-1,max(0,i+j)); xs.append(p[jj][0]); ys.append(p[jj][1])
        out.append((sum(xs)/len(xs),sum(ys)/len(ys)))
    if not closed: out[0]=p[0]; out[-1]=p[-1]
    return out
oval_px=sum(math.dist(OVAL[i],OVAL[(i+1)%len(OVAL)]) for i in range(len(OVAL)))
res=[]
for name,kind,w,closed,p in ROADS:
    q=dens(p,closed); mask=dark if kind=='dark' else light
    S0=1.02; wpx=w/S0
    if name not in ('Measuring straights',):
        for it in range(2): q=smooth(snap(q,closed,mask,wpx),closed,4)
    res.append(dict(name=name,kind=kind,w=w,closed=closed,pts=q[::2] if len(q)>8 else q))
# scale from the snapped oval centreline = middle lane 1600 m
ov=res[0]['pts']; per=sum(math.dist(ov[i],ov[(i+1)%len(ov)]) for i in range(len(ov)))
S=1600/per; print('snapped oval px',round(per),'m/px',round(S,4))
json.dump(dict(S=S,roads=res,pads=PADS,lots=LOTS,build=BUILD,size=[W,H]),open(D+'snapped.json','w'))
im=Image.open(D+'crop.png').convert('RGB'); d=ImageDraw.Draw(im)
col={'asphalt':(255,40,40),'dark':(255,220,0),'gravel':(0,200,255)}
for r in res:
    pts=r['pts']+([r['pts'][0]] if r['closed'] else []); d.line(pts,fill=col[r['kind']],width=2)
im.save(D+'overlay2.png')

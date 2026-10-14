import bpy, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from rlib import *
blend, outdir, only = sys.argv[1], sys.argv[2], (sys.argv[3].split(',') if len(sys.argv)>3 else None)
import math
SHOTS = {
 'hero':   ('00_Start', {'Bend angle':0.07,'Screws':True,'Plastic Frame':True}, (0.30,-0.62,0.10),(0.0,0.0,-0.005),58,(1600,1100)),
 'bend':   ('NY', {'Bend angle':0.55}, (0.40,-0.55,0.16),(0,0.02,0),55,(1600,1100)),
 'vanity': ('TX', {'WRITING':'BLENDER','Bend angle':0.06}, (-0.26,-0.62,0.10),(0,0,-0.005),58,(1600,1100)),
 'sep':    ('FL', {'Bend angle':0.05}, (0.24,-0.64,0.08),(0,0,-0.005),58,(1600,1100)),
 'frame':  ('00_Start', {'Bend angle':0.0,'Screws':True,'Plastic Frame':True,'WRITING':'7GEO123','Frame writing #1':'CERTIFIED PRE-OWNED'}, (-0.24,-0.44,-0.03),(-0.02,0.0,-0.02),50,(1600,1100)),
 'dirt':   ('AZ', {'Bend angle':0.05,'Flies':True,'Plastic Frame':True,'Frame writing #2':'DESERT AUTO','Frame writing #3':'TUCSON  AZ'}, (0.22,-0.50,0.05),(0.0,0.0,-0.01),50,(1600,1100)),
 'embossed':('ID', {'Bend angle':0.0}, (0.10,-0.42,0.05),(0.02,0.0,0),50,(1600,1100)),
}
for name,(obj,vals,cl,tg,lens,res) in SHOTS.items():
    if only and name not in only: continue
    bpy.ops.wm.open_mainfile(filepath=blend)
    sc=setup_scene(res=res, samples=96, world=(0.85,0.88,0.95), strength=0.35)
    sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'
    sc.render.film_transparent=True
    solo([obj]); o=bpy.data.objects[obj]; o.location=(0,0,0); o.rotation_euler=(math.pi/2,0,0)
    for k,v in vals.items(): setin(o,k,v)
    cam(cl,tg,lens=lens)
    area('Key',(-0.6,-0.9,0.6),(1.1,0,-0.6),1.0,70)
    area('Fill',(0.8,-0.7,0.1),(1.5,0,0.85),1.2,25,(0.9,0.95,1.0))
    area('Rim',(0.0,0.4,0.6),(-0.6,0,3.14),0.6,30)
    sc.render.filepath=os.path.join(outdir,name+'.png')
    bpy.ops.render.render(write_still=True)

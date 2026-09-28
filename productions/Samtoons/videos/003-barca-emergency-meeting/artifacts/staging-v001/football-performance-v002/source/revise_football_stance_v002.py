"""Calibrate S06 rest poses; preserve every authored foot/ball contact.
Run apply(sys.modules['s06']) in the existing visible authoring session,
or after reconstructing v001 with its documented builder calls.
"""
import ast,math,json
from pathlib import Path
import bpy
from mathutils import Vector

def apply(m):
 assert not bpy.app.background
 old=m.body_pose
 before={(n,f,s):old(n,f)['legs'][s][2] for n in m.A for f in range(1,m.END+1) for s in ['L','R']}
 source=(m.V/'scripts/build_football_v001.py').read_text()
 node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='body_pose')
 code=ast.get_source_segment(source,node)
 correction='''
 # Rest proportions are calibrated to the planted stance. Active mechanics retain
 # their authored hip height; neither foot endpoints nor ball contacts move.
 idle_rows={
  'Pedri':[(1,1),(90,1),(108,0),(155,0),(175,1)],
  'Yamal':[(1,1),(114,1),(130,0),(260,0),(280,1)],
  'Raphinha':[(1,1),(218,1),(230,0)],
 }.get(name,[(1,0),(38,0),(48,1),(140,1),(153,0),(254,0),(280,1)])
 rest=at(f,idle_rows);center=(lf[0]+rf[0])*.5
 hip.x=hip.x*(1-rest)+center*rest
 height=min(pt[1]+.05+math.sqrt(.81**2-(pt[0]-(center+sgn*.095))**2) for sgn,pt in [(-1,lf),(1,rf)])-.002
 hip.y=hip.y*(1-rest)+height*rest
'''
 code=code.replace(' neck=hip+Vector',correction+' neck=hip+Vector',1)
 exec(compile(code,'<S06 calibrated rest>','exec'),m.__dict__)
 for n in m.A:
  for f in range(1,m.END+1):
   for side in ['L','R']:assert m.body_pose(n,f)['legs'][side][2]==before[n,f,side]
  for side in ['L','R']:
   h,k,a=map(Vector,m.body_pose(n,70)['legs'][side])
   assert math.degrees((k-h).angle(a-k))<10,(n,side)
 m.O=m.V/'artifacts/staging-v001/football-performance-v002';m.O.mkdir(exist_ok=True)
 bpy.context.window.scene=m.S;m.S.name='S003_S06_Football_v002';m.S.use_fake_user=True
 for n in m.A:m.clear_actor_keys(n);m.animate_actor(n);m.shorts_follow(n)
 report=m.check_save()
 report['stance_revision']={'rest_knee_bend_max_degrees':10,'all_foot_endpoints_match_v001':True,'scope':'Rest stance and transitions only; active kick/run mechanics preserved.'}
 (m.O/'construction-check.json').write_text(json.dumps(report,indent=2)+'\n')
 return report

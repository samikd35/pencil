import bpy,math
import numpy as np
from mathutils import Vector
q=bpy.app.driver_namespace['build19'];globals().update({k:q[k] for k in ['s','S','G','A','Y','R','K','opp','ball','key','pose','smooth','n','b','curves','surface','tube','mat','env']})
bpy.context.window.scene=s
# Saka's legs cross the hip centreline in the source: nearest anatomical segment, not x-side.
a=S;r=a['rest'];bones={side+lab:(side+aa,side+bb) for side in ['L','R'] for lab,aa,bb in [('thigh','hip','knee'),('calf','knee','ankle'),('foot','ankle','toe')]};skin=a['skin'];names=[v.name for v in skin.vertex_groups];ww=np.zeros((len(skin.data.vertices),len(names)))
for i,v in enumerate(skin.data.vertices):
 for g in v.groups:ww[i,g.group]=g.weight
 if v.co.y<r['hip'].y+.02:
  p=v.co;vals=[]
  for k,(aa,bb) in bones.items():
   d=r[bb]-r[aa];t=max(0,min(1,(p-r[aa]).dot(d)/d.length_squared));vals.append(((p-r[aa]-t*d).length,k))
  vals.sort();ww[i]=0;t=max(0,min(1,(p.y-r['hip'].y+.07)/.09));ww[i,names.index('torso')]=t;w=[math.exp(-(d*d-vals[0][0]**2)/.001) for d,k in vals[:2]]
  for (_,k),val in zip(vals[:2],w):ww[i,names.index(k)]=val/sum(w)*(1-t)
grid=ww.reshape(101,61,len(names))
for _ in range(10):grid[1:-1,1:-1]=.6*grid[1:-1,1:-1]+.1*(grid[:-2,1:-1]+grid[2:,1:-1]+grid[1:-1,:-2]+grid[1:-1,2:])
for vg in skin.vertex_groups:
 vg.remove(list(range(len(skin.data.vertices))))
 for i,w in enumerate(ww[:,vg.index]):
  if w>.0001:vg.add([i],float(w),'REPLACE')
# Fixed support foot; knee solves to the authored ankle path.
l1=(r['Rknee']-r['Rhip']).length;l2=(r['Rankle']-r['Rknee']).length
for f in range(1,198):
 s.frame_set(f);wind=smooth((f-148)/10);hit=smooth((f-158)/10);settle=smooth((f-178)/16)
 ank=Vector((.20,.19,0)).lerp(Vector((-.05,.42,0)),wind).lerp(Vector((.56,.20,0)),hit).lerp(Vector((.22,.19,0)),settle)
 hip=r['Rhip'];d=ank-hip
 if d.length>l1+l2-.002:ank=hip+d.normalized()*(l1+l2-.002)
 knee=b['ik'](hip,ank,l1,l2,hip+Vector((.3,-.2,0)));toe=ank+(r['Rtoe']-r['Rankle'])
 for name,p in [('Rknee',knee),('Rankle',ank),('Rtoe',toe)]:key(a['C'][name],'location',f,p)
# Ball is a 22 cm sphere; remove inherited scale from previous camera adaptation.
for f,v in [(1,(1,1,1)),(269,(1,1,1)),(270,(0,0,0))]:key(ball,'scale',f,v)
for fc in curves(ball):
 if fc.data_path=='scale':
  for k in fc.keyframe_points:k.interpolation='CONSTANT'
s.frame_set(168);bpy.context.view_layer.update();contact=S['root'].matrix_world@S['C']['Rtoe'].location;contact.z-=.07
head=q['head'];end=Vector((2.2,53.15,1.15))
for f in range(1,270):
 if f<168:p=contact.copy()
 elif f<=217:u=(f-168)/49;p=contact.lerp(head,u);p.z+=1.25*4*u*(1-u)
 elif f<=238:u=(f-217)/21;p=head.lerp(end,u);p.z+=.08*math.sin(math.pi*u)
 else:u=min(1,(f-238)/18);p=end.lerp(Vector((2.2,53.45,.11)),u)
 key(ball,'location',f,p)
q['contact']=contact
# Remove unmotivated foreground intrusions, keep the opponent visible only for the reaction.
q['show'](A['root'],270,1047)
# Current scale can be zero when looking up hidden actors: set before calling exposure helper.
opp['root'].scale=(1,1,1);q['show'](opp['root'],512,711)
for f in range(712,856):
 ask=smooth((f-716)/7)*(1-smooth((f-795)/10));b['pose_actor'](Y,f,ua=(-.38*ask,.38*ask),fa=(-.48*ask,.48*ask),hands=(-.18*ask,.18*ask),lean=.015*ask)
# A goalkeeper steps forward in depth: alternating raised boots and hip weight transfer.
r=R['rest']
for f in range(475,501):
 s.frame_set(f);p={k:v.copy() for k,v in r.items()};phase=(f-475)/25
 for side,offset in [('L',0),('R',12)]:
  u=max(0,min(1,(f-475-offset)/12));lift=.06*math.sin(math.pi*u);p[side+'ankle'].y+=lift;p[side+'toe'].y+=lift;p[side+'knee'].y+=lift*.5
 for k,v in p.items():key(R['C'][k],'location',f,v)
# Crowd silhouettes include bodies and seats, rather than isolated floating heads.
for ob in list(env.objects):
 if ob.name.startswith('v019 spectators'):
  verts=[];faces=[];inds=[]
  for po in ob.data.polygons:
   center=sum((ob.data.vertices[i].co for i in po.vertices),Vector())/len(po.vertices);x,y,z=center;ii=len(verts);verts.extend([(x-.17,y-.01,z-.18),(x+.17,y-.01,z-.18),(x+.13,y-.01,z-.06),(x-.13,y-.01,z-.06)]);faces.append(tuple(range(ii,ii+4)));inds.append(po.material_index)
  me=bpy.data.meshes.new('v019 crowd shoulders');me.from_pydata(verts,[],faces)
  for color in ['#d7c9b6','#303b46','#a73e47','#eee4d4']:me.materials.append(mat(color))
  for po,idx in zip(me.polygons,inds):po.material_index=idx
  oo=bpy.data.objects.new(me.name,me);env.objects.link(oo)
# Numeric account and native scene remain reviewable.
q['refined']=True;s.frame_set(168)
for f in [168,217,490,740,920]:
 s.frame_set(f);s.camera=max((m for m in s.timeline_markers if m.camera and m.frame<=f),key=lambda m:m.frame).camera;s.render.filepath=str(q['O']/'checks'/f'fixed-{f}.png');bpy.ops.render.render(write_still=True)
result={'contact':list(contact),'fixed_frames':[168,217,490,740,920]}

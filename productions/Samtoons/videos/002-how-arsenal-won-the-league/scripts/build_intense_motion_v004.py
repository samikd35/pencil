"""Eight-second jump stress test; reuse the current approved artwork and rig builder."""
from pathlib import Path
import ast
ROOT=Path('/Users/samikd/MyProjects/Pencil/productions/Samtoons/videos/002-how-arsenal-won-the-league')
rig_source=(ROOT/'scripts/build_unveiling_motion_v001.py').read_text()
# Reuse construction unchanged; stop before its mild performance and save step.
prefix=rig_source.split('actors={name:rig(name) for name in CONFIG}')[0]
prefix=prefix.replace("artifacts/unveiling-motion-v001", "artifacts/intense-motion-v004").replace("S002_TR02_motion_v001", "S002_intense_motion_v004")
# Trim invisible grid faces so folded transparent surfaces cannot occlude the art.
prefix=prefix.replace("mesh=bpy.data.meshes.new(person+' / continuous skin');", """import numpy as np
    image=next(n.image for n in material.node_tree.nodes if n.type=='TEX_IMAGE')
    rgba=np.empty(len(image.pixels),dtype=np.float32);image.pixels.foreach_get(rgba)
    alpha=rgba.reshape(image.size[1],image.size[0],4)[:,:,3]
    def opaque(index):
        px,py=pixels[index]
        return alpha[max(0,min(image.size[1]-1,int(1024-py))),max(0,min(image.size[0]-1,int(px)))]>.93
    faces=[face for face in faces if any(opaque(i) for i in face)]
    mesh=bpy.data.meshes.new(person+' / continuous skin');""")
prefix=prefix.replace("minimum=min(d*d for d,k in distances)", """# Feather the fitted artwork boundary; abrupt masks tear the continuous mesh.
        def clamp(value): return min(1,max(0,value))
        adjusted=[]
        for d,k in distances:
            mask=1.0
            if any(w in k for w in ['arm','hand']):
                left=290+max(0,py-330)*.12;right=485+max(0,py-330)*.12
                mask=clamp((left+18-px)/36) if k.startswith('L') else clamp((px-right+18)/36)
                mask*=clamp((435-py)/45)*clamp((py-195)/45)
            elif any(w in k for w in ['thigh','calf','foot']):mask=clamp((py-480)/65)
            if mask>0:adjusted.append((math.sqrt(d*d-.28**2*math.log(mask)),k))
        distances=adjusted
        minimum=min(d*d for d,k in distances)""")
exec(compile(prefix,'existing_rig_construction','exec'))
actors={'Gyokeres':rig('Gyokeres')}
a=actors['Gyokeres'];rest=a['rest'];controls=a['controls']
a['root'].location.x=2.8
camera=s.camera;camera.location=(-.8,.7,25);camera.data.ortho_scale=19
# Expand only the static set for this full-body stress-test framing.
for ob in copies.values():
 if ob.type=='MESH' and ob.name.find('TR02 / Gyokeres')<0 and ob.name.find('TR02 / Arteta')<0:
  ob.scale.x=1.3;ob.scale.y=1.3
 if 'arteta_contact_shadow' in ob.name:ob.hide_render=True
 if 'gyokeres_contact_shadow' in ob.name:
  ob.scale=(1,1,1);ob.location.x=2.8
# Each tuple: frame, pelvis elevation, ankle lift, outward ankle spread, arm rotation.
poses=[(1,0,0,0,0),(20,0,0,0,0),(36,-.65,0,0,-12),
       (43,-.85,0,0,-18),(49,.15,.30,.10,35),(61,1.35,1.65,.35,65),
       (72,.25,.30,.10,35),(77,0,0,0,15),(83,-.75,0,0,-8),
       (99,0,0,0,0),(108,0,0,0,0),(119,-.90,0,0,-18),
       (126,.2,.35,.10,40),(138,1.7,2.15,.55,70),(149,.35,.4,.15,40),
       (155,0,0,0,15),(162,-.85,0,0,-10),(180,0,0,0,0),(192,0,0,0,0)]
def rotate(v,angle):
 c=math.cos(angle);sn=math.sin(angle)
 return Vector((v.x*c-v.y*sn,v.x*sn+v.y*c,0))
def knee(hip,ankle,l1,l2,sign):
 d=(ankle-hip).length;assert 0<d<l1+l2+.03
 direction=(ankle-hip).normalized();along=(l1*l1-l2*l2+d*d)/(2*d)
 height=math.sqrt(max(0,l1*l1-along*along))
 normal=Vector((-direction.y,direction.x,0))*sign
 return hip+direction*along+normal*height
for f,body,feet,spread,arms in poses:
 p={k:v+Vector((0,body,0)) for k,v in rest.items()}
 for side,sign in [('L',-1),('R',1)]:
  h,k,ank,toe=[side+x for x in ['h','k','a','t']]
  p[ank]=rest[ank]+Vector((sign*spread,feet,0));p[toe]=rest[toe]+Vector((sign*spread,feet,0))
  p[k]=knee(p[h],p[ank],(rest[k]-rest[h]).length,(rest[ank]-rest[k]).length,sign)
  shoulder,elbow,wrist,finger=[side+x for x in ['s','e','w','f']]
  angle=math.radians(arms*sign)
  for joint in [elbow,wrist,finger]:p[joint]=p[shoulder]+rotate(rest[joint]-rest[shoulder],angle)
 for name,control in controls.items():
  control.location=p[name];control.keyframe_insert(data_path='location',frame=f)
for node in ast.parse(rig_source).body:
 if isinstance(node,ast.FunctionDef) and node.name=='curves':exec(compile(ast.Module(body=[node],type_ignores=[]),'curves','exec'))
for o in s.objects:
 for fc in curves(o):
  for key in fc.keyframe_points:
   key.interpolation='BEZIER';key.handle_left_type='AUTO_CLAMPED';key.handle_right_type='AUTO_CLAMPED'
s['Scope']='Eight-second high-movement construction test: two jumps, crouch, launch, airborne pose, landing and recovery. Silent diagnostic; not a new scripted shot or motion approval.'
s['Events']=json.dumps({'crouch':43,'jump_apex':61,'landing':77,'landing_compression':83,'deep_crouch':119,'high_jump_apex':138,'second_landing':155,'second_compression':162,'recovery':180})
s.frame_set(138);bpy.context.view_layer.update();OUT.mkdir(parents=True,exist_ok=True)
assert not (OUT/'intense-motion-v004.blend').exists()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'intense-motion-v004.blend'))
result={'file':bpy.data.filepath,'scene':s.name,'frames':192,'action':'two jumps with anticipation, contact and recovery'}

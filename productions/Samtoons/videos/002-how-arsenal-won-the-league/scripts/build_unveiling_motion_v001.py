"""Eight-second TR02 picture proof. Live Blender authoring; no full-film render.

Adapts episode 001's joint targets, COPY_LOCATION/STRETCH_TO bones and
continuous textured skin. Regions below are fitted to this approved drawing.
"""
import bpy, math, json
from pathlib import Path
from mathutils import Vector

ROOT=Path('/Users/samikd/MyProjects/Pencil/productions/Samtoons/videos/002-how-arsenal-won-the-league')
OUT=ROOT/'artifacts/unveiling-motion-v001'
NAME='S002_TR02_motion_v001'
assert NAME not in bpy.data.scenes, 'Preserve existing authored scene'
source=bpy.data.scenes['S002_TR02_treatment_v001']
s=bpy.data.scenes.new(NAME)
s.world=source.world
copies={}
for old in source.objects:
    ob=old.copy()
    if old.type=='CAMERA': ob.data=old.data.copy()
    s.collection.objects.link(ob); copies[old.name]=ob
    ob.name='Motion / '+old.name
s.camera=copies['TR02 / wide camera']
bpy.context.window.scene=s
s.render.engine='BLENDER_EEVEE'; s.eevee.taa_render_samples=16
s.render.resolution_x=1280; s.render.resolution_y=720; s.render.resolution_percentage=100
s.render.fps=24; s.frame_start=1; s.frame_end=192
s.render.image_settings.file_format='PNG'; s.render.image_settings.color_mode='RGB'
s.view_settings.view_transform='Standard'; s.view_settings.look='None'
s.render.use_sequencer=False
material=copies['TR02 / Gyokeres'].data.materials[0]
for person in ['Gyokeres','Arteta']: copies['TR02 / '+person].hide_render=True

CONFIG={
 'Gyokeres':{'crop':(0,798.72),'left':-7.2,'joints':{
 'hip':(395,558),'neck':(387,224),'head':(377,109),
 'Ls':(283,261),'Le':(226,384),'Lw':(133,364),'Lf':(75,350),
 'Rs':(501,278),'Re':(568,391),'Rw':(647,369),'Rf':(715,351),
 'Lh':(331,570),'Lk':(324,738),'La':(290,929),'Lt':(226,977),
 'Rh':(462,570),'Rk':(486,739),'Ra':(536,929),'Rt':(595,977)},
 'eyes':[(388,117,23,16),(423,107,15,15)],'mouth':(411,162,26,22)},
 'Arteta':{'crop':(798.72,1536),'left':-1.65,'joints':{
 'hip':(1095,610),'neck':(1079,300),'head':(1080,206),
 'Ls':(982,335),'Le':(940,455),'Lw':(1028,527),'Lf':(1090,549),
 'Rs':(1180,337),'Re':(1302,340),'Rw':(1395,302),'Rf':(1467,280),
 'Lh':(1041,620),'Lk':(1023,784),'La':(986,933),'Lt':(948,975),
 'Rh':(1156,620),'Rk':(1188,788),'Ra':(1231,939),'Rt':(1275,973)},
 'eyes':[(1091,207,19,15),(1126,197,12,14)]}
}

def empty(name,position,parent=None):
    o=bpy.data.objects.new(name,None); s.collection.objects.link(o)
    o.empty_display_type='SPHERE'; o.empty_display_size=.07
    o.location=position; o.parent=parent
    return o

def distance(p,a,b):
    d=b-a; t=max(0,min(1,(p-a).dot(d)/d.length_squared))
    return (p-a-t*d).length

def rig(person):
    c=CONFIG[person]; unit=7.35/1024; start,end=c['crop']
    def xy(p): return Vector((c['left']+(p[0]-start)*unit,3.65-p[1]*unit,0))
    rest={k:xy(p) for k,p in c['joints'].items()}
    root=empty(person+' / ROOT',(0,0,2))
    controls={k:empty(person+' / CTRL '+k,p,root) for k,p in rest.items()}
    bones={'torso':('hip','neck'),'head':('neck','head')}
    for side in ['L','R']:
        bones.update({side+' upper arm':(side+'s',side+'e'),side+' forearm':(side+'e',side+'w'),side+' hand':(side+'w',side+'f'),side+' thigh':(side+'h',side+'k'),side+' calf':(side+'k',side+'a'),side+' foot':(side+'a',side+'t')})
    data=bpy.data.armatures.new(person+' / deform bones')
    arm=bpy.data.objects.new(data.name,data); s.collection.objects.link(arm); arm.parent=root
    bpy.ops.object.select_all(action='DESELECT'); arm.select_set(True); bpy.context.view_layer.objects.active=arm
    bpy.ops.object.mode_set(mode='EDIT')
    for name,(a,b) in bones.items():
        bone=data.edit_bones.new(name); bone.head=rest[a]; bone.tail=rest[b]
    bpy.ops.object.mode_set(mode='OBJECT')
    for name,(a,b) in bones.items():
        pb=arm.pose.bones[name]
        co=pb.constraints.new('COPY_LOCATION'); co.target=controls[a]
        co=pb.constraints.new('STRETCH_TO'); co.target=controls[b]; co.rest_length=(rest[b]-rest[a]).length; co.volume='NO_VOLUME'; co.bulge=0
    nx,ny=160,205; verts=[]; pixels=[]; faces=[]
    for j in range(ny+1):
        for i in range(nx+1):
            px=start+(end-start)*i/nx; py=1024*j/ny
            verts.append(tuple(xy((px,py)))); pixels.append((px,py))
    for j in range(ny):
        for i in range(nx):
            q=j*(nx+1)+i; faces.extend([(q,q+1,q+nx+2),(q,q+nx+2,q+nx+1)])
    mesh=bpy.data.meshes.new(person+' / continuous skin'); mesh.from_pydata(verts,[],faces); mesh.materials.append(material)
    uv=mesh.uv_layers.new()
    for loop in mesh.loops:
        px,py=pixels[loop.vertex_index]; uv.data[loop.index].uv=(px/1536,1-py/1024)
    skin=bpy.data.objects.new(mesh.name,mesh); s.collection.objects.link(skin); skin.parent=root
    groups={k:skin.vertex_groups.new(name=k) for k in bones}
    for i,(px,py) in enumerate(pixels):
        distances=[(distance(Vector(verts[i]),rest[bones[k][0]],rest[bones[k][1]]),k) for k in bones]
        minimum=min(d*d for d,k in distances)
        weights=[math.exp(-(d*d-minimum)/.28**2) for d,k in distances]
        total=sum(weights)
        for (d,key),weight in zip(distances,weights):
            if weight/total>1e-6: groups[key].add([i],weight/total,'REPLACE')
    mod=skin.modifiers.new('Joint targets deform approved drawing','ARMATURE'); mod.object=arm
    skin.shape_key_add(name='Basis')
    blink=skin.shape_key_add(name='Blink')
    for i,(px,py) in enumerate(pixels):
        for ex,ey,rx,ry in c['eyes']:
            dx=abs(px-ex)/rx; dy=abs(py-ey)/ry
            if dx<1.4 and dy<1.4:
                strength=min(1,max(0,(1.4-dx)/.4))*min(1,max(0,(1.4-dy)/.4))
                blink.data[i].co.y+=(py-ey)*unit*.94*strength
    face=empty(person+' / FACE controls',(0,0,0),root); face['blink']=0.0
    driver=blink.driver_add('value').driver; v=driver.variables.new(); v.name='blink'; v.type='SINGLE_PROP'; v.targets[0].id=face; v.targets[0].data_path='["blink"]'; driver.expression='blink'
    skin['Scope']='Fitted joint deformation and blink for this front/three-quarter pose. No turn or lip-sync proof.'
    return {'root':root,'controls':controls,'rest':rest,'skin':skin,'face':face}

actors={name:rig(name) for name in CONFIG}

def pose(person,frame,body=(0,0),head=(0,0),left=(0,0),right=(0,0),elbows=(0,0)):
    a=actors[person]
    for name,control in a['controls'].items():
        delta=Vector((0,0,0))
        if name in ['hip','neck','head','Ls','Rs','Lh','Rh']: delta=Vector((*body,0))
        if name=='head': delta+=Vector((*head,0))
        if name in ['Le','Re']: delta=Vector((body[0],body[1]+elbows[0 if name=='Le' else 1],0))
        if name in ['Lw','Lf']: delta=Vector((*left,0))
        if name in ['Rw','Rf']: delta=Vector((*right,0))
        control.location=a['rest'][name]+delta; control.keyframe_insert(data_path='location',frame=frame)

# Flag is initially outside the tight frame, then camera follows Arteta's gesture.
camera=s.camera
for frame,x,y,scale in [(1,-2.0,.8,10.8),(15,-2,.8,10.8),(35,0,0,16),(62,0,0,16),(63,-2.0,.85,11.0),(130,-2,.85,11),(131,0,0,16),(192,0,0,16)]:
    camera.location=(x,y,25); camera.keyframe_insert(data_path='location',frame=frame)
    camera.data.ortho_scale=scale; camera.data.keyframe_insert(data_path='ortho_scale',frame=frame)

for f,b,h,l,r,e in [
 (1,(0,0),(0,0),(.05,-.58),(-.04,-.55),(-.22,-.20)),
 (42,(0,0),(0,0),(.05,-.58),(-.04,-.55),(-.22,-.20)),
 (53,(0,-.10),(.06,-.04),(.10,-.7),(-.05,-.68),(-.30,-.30)),
 (68,(0,.11),(.10,.07),(-.08,.15),(.07,.15),(.10,.12)),
 (77,(0,.035),(.025,.01),(0,.025),(0,.025),(0,0)),
 (105,(0,.035),(-.05,0),(-.02,.02),(.03,.07),(0,0)),
 (120,(0,0),(-.03,-.02),(0,0),(0,0),(0,0)),
 (146,(0,0),(.06,0),(.12,-.30),(-.08,-.30),(-.12,-.12)),
 (166,(0,-.06),(.12,-.07),(.2,-.55),(-.15,-.55),(-.25,-.25)),
 (192,(0,-.06),(.12,-.07),(.2,-.55),(-.15,-.55),(-.25,-.25))]: pose('Gyokeres',f,b,h,l,r,e)
for f,b,h,r,e in [
 (1,(0,0),(0,0),(-.12,-.55),-.22),(12,(0,0),(-.04,-.03),(-.2,-.63),-.28),
 (27,(0,.06),(-.025,.06),(.1,.12),.055),(38,(0,0),(0,.02),(0,0),0),
 (103,(0,0),(0,.02),(0,0),0),(117,(0,-.06),(.02,-.07),(-.07,-.1),-.06),
 (128,(0,.02),(-.06,.065),(.10,.08),.05),(141,(0,0),(0,.02),(0,0),0),
 (192,(0,0),(0,.02),(0,0),0)]: pose('Arteta',f,b,h,(0,0),r,(b[1],e))
for person,frames in [('Gyokeres',[48,151]),('Arteta',[83,174])]:
    face=actors[person]['face']
    for middle in frames:
        for f,value in [(middle-2,0),(middle,1),(middle+2,0)]:
            face['blink']=value; face.keyframe_insert(data_path='["blink"]',frame=f)

def curves(id):
    ad=id.animation_data
    if not ad or not ad.action:return []
    return [fc for layer in ad.action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
for o in list(s.objects)+[camera.data]:
    for fc in curves(o):
        for k in fc.keyframe_points:
            k.interpolation='BEZIER'; k.handle_left_type='AUTO_CLAMPED'; k.handle_right_type='AUTO_CLAMPED'
            if o in [camera,camera.data] and round(k.co.x) in [62,130]: k.interpolation='CONSTANT'
s['Scope']='TR02 eight-second silent motion preview; actual joint controls and facial blink. No final voice or lip sync.'
s['Events']=json.dumps({'flag_reveal':35,'reaction_cut':63,'shrug_peak':68,'arteta_reply_nod':128,'wide_return':131,'deflation':166})
s.frame_set(77); bpy.context.view_layer.update()
for a in actors.values():
    assert len(a['controls'])==19 and a['skin'].modifiers[0].object
    for name in ['La','Ra','Lt','Rt']:
        assert (a['controls'][name].location-a['rest'][name]).length<1e-5
OUT.mkdir(parents=True,exist_ok=True)
assert not (OUT/'unveiling-motion-v001.blend').exists()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'unveiling-motion-v001.blend'))
result={'file':bpy.data.filepath,'scene':s.name,'frames':192,'fps':24,'controls_per_character':len(actors['Arteta']['controls'])}

"""Dawn Training. Blender 5.2 authoring; run through Blender MCP or background CLI."""
from pathlib import Path
import bpy, math, json, random, time, sys
import numpy as np
from mathutils import Vector, Matrix
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/dawn_training'
CONFIG=json.loads((OUT/'geometry/characters.json').read_text())
PREFIX='DT_'
random.seed(48)
SCENES=[]
def scene_new(name,w=1920,h=1080):
 s=bpy.data.scenes.new(name);bpy.context.window.scene=s;SCENES.append(s)
 s.render.engine='BLENDER_EEVEE';s.render.resolution_x=w;s.render.resolution_y=h;s.render.resolution_percentage=100
 s.render.fps=24;s.frame_start=1;s.frame_end=720
 s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
 s.render.film_transparent=False;s.render.use_file_extension=True
 s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
 s.world=bpy.data.worlds.new(name+'_World');s.world.color=(.2,.2,.2)
 if hasattr(s,'eevee'):s.eevee.taa_render_samples=16
 s.render.use_sequencer=False
 return s

def collection(name,scene=None):
 c=bpy.data.collections.new(name);(scene or bpy.context.scene).collection.children.link(c);return c

def move(obj,c):
 for cc in list(obj.users_collection):cc.objects.unlink(obj)
 c.objects.link(obj)

def srgb(c):
 if isinstance(c,str):c=tuple(int(c[i:i+2],16)/255 for i in (1,3,5))
 return tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in c[:3])
MATS={}
def mat(color):
 if color not in MATS:
  m=bpy.data.materials.new('DT_Color_'+color);m.diffuse_color=(*srgb(color),1);m.use_nodes=True
  ns=m.node_tree.nodes;ns.clear();out=ns.new('ShaderNodeOutputMaterial');em=ns.new('ShaderNodeEmission');em.inputs['Color'].default_value=(*srgb(color),1);em.inputs['Strength'].default_value=1
  m.node_tree.links.new(em.outputs[0],out.inputs['Surface']);MATS[color]=m
 return MATS[color]
def poly(name,pts,color,z=-1,c=None):
 me=bpy.data.meshes.new(name);me.from_pydata([(x,y,z) for x,y in pts],[],[list(range(len(pts)))]);me.materials.append(mat(color))
 o=bpy.data.objects.new(name,me);(c or bpy.context.scene.collection).objects.link(o);return o

def ellipse(name,x,y,rx,ry,color,z,c=None,n=64):
 return poly(name,[(x+rx*math.cos(i*2*math.pi/n),y+ry*math.sin(i*2*math.pi/n)) for i in range(n)],color,z,c)

def line(name,pts,color,width=.018,z=0,c=None):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=1;cu.bevel_depth=width/2;cu.bevel_resolution=1
 sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,(x,y) in zip(sp.points,pts):p.co=(x,y,z,1)
 cu.materials.append(mat(color));o=bpy.data.objects.new(name,cu);(c or bpy.context.scene.collection).objects.link(o);return o

def text_obj(name,body,x,y,size,color,z=4,align='LEFT',c=None):
 cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.size=size;cu.space_character=1.15;cu.align_x=align
 font='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
 if Path(font).exists():cu.font=bpy.data.fonts.load(font,check_existing=True)
 cu.materials.append(mat(color));o=bpy.data.objects.new(name,cu);(c or bpy.context.scene.collection).objects.link(o);o.location=(x,y,z);return o

def camera(name,x,y,width):
 d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);bpy.context.scene.collection.objects.link(o);o.location=(x,y,50);d.type='ORTHO';d.ortho_scale=width;d.clip_end=200;o.rotation_euler=(0,0,0);return o

def keys(o,path,values,interp='BEZIER'):
 for f,v in values:
  setattr(o,path,v);o.keyframe_insert(data_path=path,frame=f)
 if o.animation_data and o.animation_data.action:
  for slot in o.animation_data.action.slots:
   for layer in o.animation_data.action.layers:
    for strip in layer.strips:
     bag=strip.channelbag(slot)
     if bag:
      for fc in bag.fcurves:
       if fc.data_path==path:
        for k in fc.keyframe_points:k.interpolation=interp

def visible(o,start,end):
 vals=[(1,True)]
 if start>1:vals+=[(start-1,True)]
 vals+=[(start,False),(end,False),(end+1,True)]
 keys(o,'hide_render',vals,'CONSTANT');keys(o,'hide_viewport',vals,'CONSTANT')

def bone_rot(r,n,f,a):
 if n not in r.pose.bones:return
 b=r.pose.bones[n];b.rotation_mode='XYZ';b.rotation_euler[2]=math.radians(a);b.keyframe_insert(data_path='rotation_euler',frame=f,group=n)

def gp_material(o,name,fill,stroke=None):
 m=bpy.data.materials.new(name);bpy.data.materials.create_gpencil_data(m);gp=m.grease_pencil;gp.show_fill=fill is not None;gp.show_stroke=stroke is not None
 if fill:gp.fill_color=(*srgb(fill),1)
 if stroke:gp.color=(*srgb(stroke),1)
 o.data.materials.append(m);return len(o.data.materials)-1

def gp_shape(o,lname,pts,color,closed=True,width=.008,ink=None):
 l=o.data.layers.get(lname) or o.data.layers.new(lname,set_active=True);l.use_lights=False
 fr=l.frames[0] if len(l.frames) else l.frames.new(1);d=fr.drawing;d.add_strokes([len(pts)]);st=d.strokes[-1];st.cyclic=closed;st.material_index=gp_material(o,lname+'_Material',color,ink);st.fill_id=1 if color else 0;st.hide_stroke=ink is None;st.fill_opacity=1
 for p,co in zip(st.points,pts):p.position=(*co,0);p.radius=width;p.opacity=1
 return l

def gp_circle(o,lname,x,y,rx,ry,color,ink=None):
 return gp_shape(o,lname,[(x+rx*math.cos(i*2*math.pi/40),y+ry*math.sin(i*2*math.pi/40)) for i in range(40)],color,ink=ink)

def attach_layer(layer,rig,bone):
 layer.parent=rig;layer.parent_bone=bone

def driver(prop_owner,path,rig,prop,expr):
 fc=prop_owner.driver_add(path);d=fc.driver;d.type='SCRIPTED';v=d.variables.new();v.name='v';v.type='SINGLE_PROP';v.targets[0].id=rig;v.targets[0].data_path='["'+prop+'"]';d.expression=expr

ASSETS={}
def asset(name):
 cfg=CONFIG[name];c=collection('DT_Character_'+name)
 bpy.ops.wm.grease_pencil_import_svg(filepath=cfg['svg'],resolution=12,scale=1.0,use_scene_unit=False,recenter_bounds=False)
 o=bpy.context.object;o.name='DT_GP_'+name;move(o,c);o.use_grease_pencil_lights=False
 o['Artwork']='Native Grease Pencil Bezier contours reconstructed from supplied reference';o['Reference']=cfg['source'];o['Source_SHA256']=cfg['source_sha256']
 x0,y0,x1,y1=cfg['crop'];ax,ay=cfg['anchor'];scale=cfg['height']/(y1-y0);unit=.0254/96
 def co(p):return ((p[0]-ax)*scale,(ay-p[1])*scale)
 # Bake SVG coordinates into a camera-facing XY drawing, preserving Bezier handles.
 for l in o.data.layers:
  l.use_lights=False
  for fr in l.frames:
   d=fr.drawing
   for an in ['position','handle_left','handle_right','handle_positions_left','handle_positions_right']:
    a=d.attributes.get(an)
    if not a or a.data_type!='FLOAT_VECTOR':continue
    vals=np.zeros(len(a.data)*3,np.float32);a.data.foreach_get('vector',vals);v=vals.reshape(-1,3);old=v.copy()
    v[:,0]=(old[:,0]/unit+x0-ax)*scale;v[:,1]=(old[:,2]/unit+ay-y0)*scale;v[:,2]=0
    a.data.foreach_set('vector',v.ravel())
   rad=d.attributes.get('radius')
   if rad:
    v=np.zeros(len(rad.data),np.float32);rad.data.foreach_get('value',v);rad.data.foreach_set('value',v*scale/unit)
   d.tag_positions_changed()
 arm=bpy.data.armatures.new('DT_Skeleton_'+name);r=bpy.data.objects.new('DT_RIG_'+name,arm);c.objects.link(r);r.show_in_front=True;arm.display_type='STICK'
 bpy.context.view_layer.objects.active=r;r.select_set(True);o.select_set(False);bpy.ops.object.mode_set(mode='EDIT')
 b=arm.edit_bones.new('root');b.head=(0,0,0);b.tail=(0,.5,0)
 for p in cfg['parts']:
  b=arm.edit_bones.new(p['name']);b.head=(*co(p['pivot']),0);b.tail=(*co(p['tip']),0)
  if (b.tail-b.head).length<.04:b.tail.y+=.15
 for p in cfg['parts']:
  arm.edit_bones[p['name']].parent=arm.edit_bones.get(p['parent']) or arm.edit_bones['root']
 bpy.ops.object.mode_set(mode='OBJECT');bpy.context.view_layer.update()
 group=arm.collections.new('Body | rotate in the drawing plane')
 facegroup=arm.collections.new('Face | eyes, brows and mouth')
 for b in arm.bones:
  (facegroup if any(k in b.name for k in ['eyes','eyebrow','mouth']) else group).assign(b)
 for b in r.pose.bones:
  b.rotation_mode='XYZ';b.lock_rotation=(True,True,False);b.lock_location=(True,True,True);b.lock_scale=(True,True,True)
  try:b.color.palette='THEME04' if b.name=='root' else 'THEME03'
  except:pass
 r.pose.bones['root'].lock_location=(False,False,True)
 for l in o.data.layers:attach_layer(l,r,l.name)
 # Hidden Artwork consists of simple native vector joint caps below the original drawing.
 jointcolors={'upper_arm':'#f5bd8e','forearm':'#f5bd8e','pants':'#ece9ed','shin':'#3878b5','head':'#fac696'}
 for p in cfg['parts']:
  base=p['name'].split('.')[0]
  if base not in jointcolors or name=='FOCUS' or (name=='POWER' and base in ['upper_arm','pants']):continue
  x,y=co(p['pivot']);rad={'upper_arm':.14,'forearm':.13,'pants':.18,'shin':.13,'head':.14}[base]
  l=gp_circle(o,'HiddenJoint_'+p['name'],x,y,rad,rad,jointcolors[base]);o.data.layers.move_bottom(l);attach_layer(l,r,p['name'])
 if name=='POWER':
  l=gp_shape(o,'HiddenPelvis | pants overlap',[co(p) for p in [(1280,442),(1370,442),(1364,477),(1329,516),(1282,489)]],'#eeeaf0')
  o.data.layers.move_bottom(l);attach_layer(l,r,'root')
 if name in ['FRONT','FOCUS']:
  for prop,val,lo,hi in [('Blink',0.,0.,1.),('BrowFocus',0.,-1.,1.),('MouthOpen',0.,0.,1.),('Smirk',0.,0.,1.)]:
   r[prop]=val;r.id_properties_ui(prop).update(min=lo,max=hi,description={'Blink':'0 open eyes; 1 closed eyes','BrowFocus':'Subtle eyebrow tilt','MouthOpen':'0 closed mouth; 1 shout','Smirk':'0 neutral; 1 confident smile'}[prop])
  for p in cfg['parts']:
   if p['name'].startswith(('eyes.','eyebrow.')) or p['name']=='mouth':
    xs=[v[0] for v in p['poly']];ys=[v[1] for v in p['poly']];a=co([min(xs)-1,min(ys)-1]);b=co([max(xs)+1,max(ys)+1])
    l=gp_shape(o,'SkinUnder_'+p['name'],[(a[0],a[1]),(b[0],a[1]),(b[0],b[1]),(a[0],b[1])],'#fac696');o.data.layers.move_bottom(l);attach_layer(l,r,'head')
   if p['name'].startswith('eyes.'):
    driver(o.data.layers[p['name']],'opacity',r,'Blink','1-v')
    x,y=co(p['pivot']);ww=(max(v[0] for v in p['poly'])-min(v[0] for v in p['poly']))*scale*.43
    l=gp_shape(o,'Closed_'+p['name'],[(x-ww,y+.05),(x,y-.02),(x+ww,y+.06)],None,closed=False,width=.015,ink='#25232b');attach_layer(l,r,'head');driver(l,'opacity',r,'Blink','v')
   if p['name'].startswith('eyebrow.'):
    b=r.pose.bones[p['name']];fc=b.driver_add('rotation_euler',2);d=fc.driver;v=d.variables.new();v.name='v';v.targets[0].id=r;v.targets[0].data_path='["BrowFocus"]';d.expression=('0.08*v' if p['name'].endswith('L') else '-0.08*v')
  mp=next(p for p in cfg['parts'] if p['name']=='mouth');x,y=co(mp['pivot']);ww=.1 if name=='FRONT' else .18
  if not o.data.layers.get('mouth'):
   ml=gp_shape(o,'mouth',[(x-ww,y),(x,y+.025),(x+ww,y)],None,closed=False,width=.01,ink='#35282c');attach_layer(ml,r,'head')
  driver(o.data.layers['mouth'],'opacity',r,'MouthOpen','1-v')
  l=gp_circle(o,'Mouth_Shout',x,y,ww,ww*1.05,'#53252a','#25232b');attach_layer(l,r,'head');driver(l,'opacity',r,'MouthOpen','v')
  l=gp_shape(o,'Mouth_Teeth',[(x-ww*.75,y+ww*.5),(x+ww*.75,y+ww*.5),(x+ww*.6,y+ww*.2),(x-ww*.6,y+ww*.2)],'#fff5e9');attach_layer(l,r,'head');driver(l,'opacity',r,'MouthOpen','v')
  l=gp_shape(o,'Mouth_Smirk',[(x-ww,y),(x,y-.02),(x+ww,y+.075)],None,closed=False,width=.012,ink='#24222b');attach_layer(l,r,'head');driver(l,'opacity',r,'Smirk','v')
 r['How_to_pose']='Pose Mode: select a named bone, R Z to rotate. Move the rig object for whole-character placement.'
 r['Drawing_variant']=name
 o['Rig']=r.name
 ASSETS[name]=(o,r,c,co)
 return ASSETS[name]

def backdrop():
 c=collection('DT_Environment | Sunrise plateau')
 # Interpolated vertex emission gives one lightweight continuous sky gradient.
 me=bpy.data.meshes.new('DT_SkyGradient');me.from_pydata([(-100,-30,-25),(100,-30,-25),(100,35,-25),(-100,35,-25)],[],[(0,1,2,3)])
 col=me.color_attributes.new(name='SkyColor',type='FLOAT_COLOR',domain='CORNER')
 for p,v in zip(col.data,['#ffd997','#ffd997','#353e70','#353e70']):p.color=(*srgb(v),1)
 m=bpy.data.materials.new('DT_SunriseGradient');m.use_nodes=True;ns=m.node_tree.nodes;ns.clear();out=ns.new('ShaderNodeOutputMaterial');em=ns.new('ShaderNodeEmission');att=ns.new('ShaderNodeVertexColor');att.layer_name='SkyColor';m.node_tree.links.new(att.outputs['Color'],em.inputs['Color']);m.node_tree.links.new(em.outputs[0],out.inputs['Surface']);me.materials.append(m);o=bpy.data.objects.new('DT_Sky | warm horizon',me);c.objects.link(o)
 # Continuous bands share the same endpoint colors, avoiding a visible sky seam.
 stops=[(-30,'#ffdfad'),(-3,'#ffd09d'),(2,'#eab09c'),(5,'#b995ac'),(9,'#7b82aa'),(16,'#4c638f'),(35,'#303e69')]
 for j,((y0,c0),(y1,c1)) in enumerate(zip(stops,stops[1:])):
  me=bpy.data.meshes.new('DT_SkyStrip_%d'%j);me.from_pydata([(-100,y0,-24),(100,y0,-24),(100,y1,-24),(-100,y1,-24)],[],[(0,1,2,3)])
  ca=me.color_attributes.new(name='SkyColor',type='FLOAT_COLOR',domain='CORNER')
  for v,colr in zip(ca.data,[c0,c0,c1,c1]):v.color=(*srgb(colr),1)
  me.materials.append(m);ob=bpy.data.objects.new('DT_ContinuousSky_%d'%j,me);c.objects.link(ob)
 ellipse('DT_SunHalo',6,4.1,1.5,1.5,'#f7c888',-23,c)
 ellipse('DT_Sun',6,4.1,1.08,1.08,'#fff5cf',-22,c)
 for i in range(30):
  x=random.uniform(-30,30);y=random.uniform(5.8,11.8);w=random.uniform(1.2,5.5);hh=random.uniform(.04,.16)
  pts=[(x-w,y),(x-w*.35,y+hh),(x-w*.1,y+hh*.35),(x+w*.3,y+hh),(x+w,y),(x+w*.6,y-hh*.5),(x-w*.6,y-hh*.65)]
  poly('DT_Cloud_%02d'%i,pts,random.choice(['#f4ba99','#eeb197','#e4a799']),-21,c)
 for level,(z,color,base,amp) in enumerate([(-19,'#a48495',2.1,2.),(-16,'#8c7188',1.1,2.7),(-13,'#66596f',-.1,3.6)]):
  pts=[(-70,-12)]
  for j in range(100):
   x=-70+j*1.45;h=base+random.uniform(0,amp);pts.extend([(x,h),(x+.3,h+random.uniform(.2,.7)),(x+.75,h-.45)])
  pts.append((76,-12));poly('DT_MountainRange_%d'%level,pts,color,z,c)
 # Stratified rock pillars.
 for i,(x,y,h,w) in enumerate([(-10,-1,6,1.8),(12,-1,7,2),(-17,-2,8,2.5),(19,-1,5,2),(-5,-1,3,1),(9,-1,3,1)]):
  pts=[(x-w*.6,y),(x-w*.5,y+h*.7),(x-w*.33,y+h*.95),(x+.1*w,y+h),(x+.45*w,y+h*.91),(x+w*.55,y)]
  poly('DT_Pillar_%d'%i,pts,'#67536c',-11,c)
  poly('DT_PillarLight_%d'%i,[(x-.25*w,y),(x-.2*w,y+h*.94),(x+.1*w,y+h),(x+.27*w,y+h*.87),(x+.35*w,y)],'#a78389',-10.9,c)
  for j in range(3):line('DT_PillarCrack_%d_%d'%(i,j),[(x+(-.35+j*.25)*w,y+.4),(x+(-.27+j*.21)*w,y+h*.45),(x+(-.3+j*.24)*w,y+h*.87)],'#514b65',.045,-10.8,c)
 poly('DT_Plateau_Front',[(-70,-.3),(70,-.3),(70,-13),(-70,-13)],'#574d62',-5,c)
 poly('DT_Plateau_Top',[(-70,-.08),(70,-.08),(70,-2.5),(-70,-2.5)],'#a17b72',-4,c)
 poly('DT_Plateau_Rim',[(-70,0),(70,0),(70,-.35),(-70,-.35)],'#e3af87',-3.8,c)
 for i in range(95):
  x=random.uniform(-40,40);y=random.uniform(-2.35,-.4);w=random.uniform(.3,2.);hh=random.uniform(.03,.3)
  pts=[(x-w,y),(x-w*.5,y+hh),(x+w*.4,y+hh*.6),(x+w,y-.03),(x+w*.35,y-hh),(x-w*.7,y-hh*.7)]
  poly('DT_GroundFacet_%02d'%i,pts,random.choice(['#c6997d','#b78a78','#856b6d','#d3a383']),-3.5,c)
  if i%3==0:line('DT_GroundCrack_%d'%i,[(x-w,y),(x,y-hh),(x+w*.4,y-hh*1.3),(x+w*.8,y-hh*2)],'#645361',.025,-3.3,c)
 return c

def build():
 # Only this task's previous generated scenes are replaced during a deliberate rebuild.
 for s in list(bpy.data.scenes):
  if s.name.startswith('DT_'):bpy.data.scenes.remove(s)
 for o in list(bpy.data.objects):
  if o.name.startswith('DT_') and not o.users_scene:bpy.data.objects.remove(o,do_unlink=True)
 studio=scene_new('DT_01_CHARACTER_STUDIO',1400,1400)
 for n in CONFIG:asset(n)
 for n,(o,r,c,co) in ASSETS.items():
  if n!='FRONT':c.hide_render=True;c.hide_viewport=True
 cam=camera('DT_Camera_Character',0,3.4,8.2);studio.camera=cam
 poly('DT_Studio_Background',[(-20,-20),(20,-20),(20,20),(-20,20)],'#b9bcc6',-8)
 # References are packed image empties, locked and excluded from renders.
 refs=collection('DT_References | locked, non-rendering');refs.hide_render=True;refs.hide_viewport=True
 for i,n in enumerate(['im-1.png','im_2.png','im_3.png','im_4.png','im_5.png']):
  im=bpy.data.images.load(str(OUT/'references'/n),check_existing=True);im.pack();ob=bpy.data.objects.new('DT_REF_'+n,None);refs.objects.link(ob);ob.empty_display_type='IMAGE';ob.data=im;ob.empty_display_size=14;ob.location=(0,3.4,-2-i*.1);ob.color[3]=.35;ob.hide_select=True;ob.hide_render=True;ob['Reference_role']='Visual reference only; user request controls production'
 studio['Stage']='02 Drawing + 03 Rigging. FRONT is the reusable neutral cutout.'
 # Render the actual native GP result before the shot build.
 studio.render.filepath=str(OUT/'review/character_studio.png');bpy.ops.render.render(write_still=True)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'stages/03_drawing_and_rig.blend'))
 film=scene_new('DT_03_DAWN_TRAINING')
 env=backdrop()
 # Link character collections to the film; collection flags are globally shared so hide objects with keys instead.
 for n,(o,r,c,co) in ASSETS.items():
  film.collection.children.link(c);c.hide_render=False;c.hide_viewport=False
  o.hide_render=True;o.hide_viewport=True
 # The character studio's solo state will be restored with view-layer exclusions.
 poses=scene_new('DT_02_POSE_TESTS',1920,780)
 poly('DT_Pose_Background',[(-50,-50),(50,-50),(50,50),(-50,50)],'#c9cbd4',-8)
 pose_items=[]
 for i,n in enumerate(['FRONT','SIT','RUN','CROUCH','POWER']):
  source,rig,cc,co=ASSETS[n];c=collection('DT_Test_'+n)
  rr=rig.copy();rr.data=rig.data.copy();rr.name='DT_TEST_RIG_'+n;c.objects.link(rr);rr.animation_data_clear()
  oo=source.copy();oo.data=source.data.copy();oo.name='DT_TEST_GP_'+n;c.objects.link(oo);oo.animation_data_clear();oo.hide_render=False;oo.hide_viewport=False
  for l in oo.data.layers:
   if l.parent==rig:l.parent=rr
  if oo.data.animation_data:
   for fc in oo.data.animation_data.drivers:
    for v in fc.driver.variables:
     for t in v.targets:
      if t.id==rig:t.id=rr
  rr.location=(i*4.7-9.4,0,0);rr.scale=(.88,.88,.88)
  # Exercise each rig around its intended Alternate Drawing, not just a static card.
  for f,a in [(1,0),(13,4),(25,-4),(37,0)]:
   bone_rot(rr,'head',f,a);bone_rot(rr,'upper_arm.L',f,-a);bone_rot(rr,'forearm.R',f,a*1.5)
  text_obj('DT_Test_Label_'+n,('STANDING','SITTING','RUNNING','CROUCHING','POWER-UP')[i],i*4.7-9.4,-.65,.25,'#363248',align='CENTER')
  pose_items.append((oo,rr))
 poly('DT_Test_Seat',[(-6,-.03),(-3.5,-.03),(-3.5,1.9),(-5.6,1.95)],'#a3a2b1',-1)
 poses.camera=camera('DT_Camera_PoseTests',0,3.1,24);poses.frame_end=37
 bpy.context.window.scene=poses;poses.frame_set(13);poses.render.filepath=str(OUT/'review/pose_tests.png');bpy.ops.render.render(write_still=True)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'stages/04_pose_tests.blend'))
 bpy.context.window.scene=film;film.frame_set(1)
 # Simple shot plan: all cuts occur at exact five-second boundaries.
 shots=[('01_A_NEW_DAY',1,120,(-1,3.7,28)),('02_FOCUS',121,240,(0,2.2,8.4)),('03_MOVEMENT',241,360,(0,3.5,22)),('04_POWER_UP',361,480,(-1,5.1,21)),('05_RELEASE',481,600,(0,4.5,23)),('06_VICTORY',601,720,(0,3.3,21))]
 cams=[]
 for n,st,en,(x,y,w) in shots:
  ca=camera('DT_CAM_'+n,x,y,w);mk=film.timeline_markers.new(n,frame=st);mk.camera=ca;cams.append(ca)
  keys(ca.data,'ortho_scale',[(st,w),(en,w*(.93 if st!=241 else 1))])
 film.camera=cams[0]
 film['Title']='Dawn Training';film['Duration']='30 seconds / 720 frames / 24 fps';film['Workflow']='setup > drawing > rigging > pose testing > blocking > polish > render'
 # Shot 1: back-view watch, a small breath and wind catching the sash.
 o,r,c,co=ASSETS['BACK'];visible(o,1,120);r.location=(-6,0,0);r.keyframe_insert('location',frame=1)
 for f in [1,31,61,91,120]:
  bone_rot(r,'torso',f,math.sin(f*.06)*.55);bone_rot(r,'head',f,math.sin(f*.04)*1.5);bone_rot(r,'sash_tail',f,math.sin(f*.065)*5)
 # Shot 2: eyes close, then snap open. Facial controls remain simple custom properties.
 o,r,c,co=ASSETS['FOCUS'];visible(o,121,240)
 for f,v in [(121,0),(136,1),(206,1),(212,0),(240,0)]:r['Blink']=v;r.keyframe_insert('["Blink"]',frame=f)
 for f,v in [(121,0),(180,1),(240,1)]:r['BrowFocus']=v;r.keyframe_insert('["BrowFocus"]',frame=f)
 for f in [121,145,169,193,217,240]:
  bone_rot(r,'torso',f,math.sin((f-121)*.06)*.55);bone_rot(r,'head',f,math.sin((f-121)*.04)*.5)
 keys(cams[1].data,'ortho_scale',[(121,8.4),(208,7.7),(240,7.3)])
 # Shot 3: a 16-frame running cycle with ground travel, arm opposition and sash follow-through.
 o,r,c,co=ASSETS['RUN'];visible(o,241,360)
 visible(o,241,600) # visibility is refined below to expose RUN only in shots 3 and 5.
 for f,hid in [(1,True),(240,True),(241,False),(360,False),(361,True),(480,True),(481,False),(600,False),(601,True)]:
  o.hide_render=hid;o.hide_viewport=hid;o.keyframe_insert('hide_render',frame=f);o.keyframe_insert('hide_viewport',frame=f)
 for f in range(241,361,2):
  t=(f-241)/119;ph=2*math.pi*(f-241)/16;r.location=(-8+16*t,.08+.23*(1-math.cos(ph*2)),0);r.scale=(.87,.87,.87);r.keyframe_insert('location',frame=f);r.keyframe_insert('scale',frame=f)
  for n,a in [('pants.L',math.sin(ph)*27),('pants.R',-math.sin(ph)*24),('shin.L',max(0,math.cos(ph))*-18),('shin.R',max(0,-math.cos(ph))*18),('upper_arm.L',-math.sin(ph)*18),('upper_arm.R',math.sin(ph)*18),('forearm.L',math.cos(ph)*8),('forearm.R',-math.cos(ph)*8),('torso',-3+math.cos(ph*2)*1.2),('head',1.5*math.sin(ph)),('sash_tail',-8+math.sin(ph-.8)*9)]:bone_rot(r,n,f,a)
 # Shot 4: airborne power-up. A small anticipation precedes the rising arc.
 o,powrig,c,co=ASSETS['POWER'];visible(o,361,480)
 keys(powrig,'location',[(361,(-1,-.2,0)),(367,(-1,-.45,0)),(389,(-1,3.,0)),(429,(-1,3.3,0)),(480,(-1,2.6,0))]);powrig.scale=(.87,.87,.87)
 for f in range(361,481,4):
  t=(f-361)/119
  for n,a in [('upper_arm.L',-9-10*t+math.sin(f*.6)*1.2),('upper_arm.R',9+10*t-math.sin(f*.6)*1.2),('forearm.L',10*t),('forearm.R',-10*t),('pants.L',-11*t),('pants.R',12*t),('sash_tail',math.sin(f*.45)*12),('head',-2*t)]:bone_rot(powrig,n,f,a)
 # Shot 5: pose into a directed energy strike, then recoil after impact.
 o,r,c,co=ASSETS['RUN']
 keys(r,'location',[(481,(-4,1.4,0)),(511,(-4,1.8,0)),(521,(-4.5,1.8,0)),(557,(-4.3,1.8,0)),(600,(-4,1.1,0))]);keys(r,'scale',[(481,(.88,.88,.88)),(600,(.88,.88,.88))])
 for n in r.pose.bones.keys():
  bone_rot(r,n,481,0)
 for f,t in [(493,0),(511,1),(519,1),(555,1),(577,.4),(600,0)]:
  for n,a in [('upper_arm.R',76*t),('forearm.R',-130*t),('hand.R',-8*t),('torso',-4*t),('head',3*t),('pants.L',-10*t),('sash_tail',-15*t)]:bone_rot(r,n,f,a)
 # Shot 6: landing, recovery, then a confident final hold.
 o,r,c,co=ASSETS['CROUCH'];visible(o,601,648)
 keys(r,'location',[(601,(1.2,3,0)),(611,(1.2,-.05,0)),(617,(1.2,-.12,0)),(629,(1.2,0,0)),(648,(1.2,0,0))])
 for f,a in [(601,-3),(611,5),(619,2),(633,0),(648,-3)]:bone_rot(r,'torso',f,a);bone_rot(r,'head',f,-a*.6)
 o,r,c,co=ASSETS['FRONT'];visible(o,649,720)
 keys(r,'location',[(649,(1.2,-.7,0)),(667,(1.2,0,0)),(720,(1.2,0,0))]);r.scale=(.9,.9,.9)
 for f,t in [(649,1),(669,0),(720,0)]:
  for n,a in [('torso',6*t),('head',-4*t),('upper_arm.L',-8*t),('upper_arm.R',8*t),('pants.L',-5*t),('pants.R',5*t)]:bone_rot(r,n,f,a)
 for f,v in [(649,0),(679,1),(720,1)]:r['Smirk']=v;r.keyframe_insert('["Smirk"]',frame=f)
 for f,v in [(649,1),(672,.1),(720,.1)]:r['BrowFocus']=v;r.keyframe_insert('["BrowFocus"]',frame=f)
 # Locally evaluated foot contacts. Keep one foot on the plateau during each run contact.
 def minimum_y(art,rig,layer_names):
  values=[]
  for ln in layer_names:
   layer=art.data.layers.get(ln)
   if not layer:continue
   bone=rig.pose.bones.get(layer.parent_bone)
   transform=rig.matrix_world @ bone.matrix @ rig.data.bones[bone.name].matrix_local.inverted()
   for fr in layer.frames:
    for st in fr.drawing.strokes:
     values.extend((transform@p.position).y for p in st.points)
  return min(values) if values else 0
 art,rig,_,_=ASSETS['RUN']
 contact_samples=[]
 for f in range(241,361,2):
  film.frame_set(f);bpy.context.view_layer.update();low=minimum_y(art,rig,['foot.L','foot.R']);flight=.12*max(0,math.sin((f-241)*math.pi/4))
  rig.location.y+=flight-low;rig.keyframe_insert('location',frame=f);contact_samples.append([f,round(low,5),round(flight,5)])
 (OUT/'review/contact_check.json').write_text(json.dumps(contact_samples))
 # SIT is a pose-library drawing, excluded from the film.
 o,_,_,_=ASSETS['SIT'];o.hide_render=True;o.hide_viewport=True
 # Polish: moving cast shadows, line effects, dust, aura, target and blast.
 fx=collection('DT_FX | energy, dust and impact')
 shadow=ellipse('DT_ContactShadow',0,-.13,1.45,.15,'#665568',-2,fx)
 keys(shadow,'location',[(1,(-6,0,0)),(120,(-6,0,0)),(121,(0,-5,0)),(240,(0,-5,0)),(241,(-8,0,0)),(360,(8,0,0)),(361,(-1,0,0)),(480,(-1,0,0)),(481,(-4,0,0)),(600,(-4,0,0)),(601,(1.2,0,0)),(720,(1.2,0,0))],'LINEAR')
 aura_data=bpy.data.grease_pencils.new('DT_EnergyAura');aura=bpy.data.objects.new('DT_GP_EnergyAura',aura_data);fx.objects.link(aura);aura.use_grease_pencil_lights=False
 points=[(-1.1,0),(-1.9,.8),(-1.55,1.5),(-2.05,2.5),(-1.55,2.2),(-1.8,4.1),(-1.3,3.7),(-1.1,5.5),(-.65,5.05),(0,7.5),(.55,5.55),(1.15,6.2),(1.35,4.2),(1.9,4.8),(1.6,2.4),(2,2.9),(1.7,1.2),(1,0)]
 layer=gp_shape(aura,'Aura | translucent blue',points,'#62bcec',ink='#b9f4ff',width=.025)
 aura.data.materials[-1].grease_pencil.fill_color=(*srgb('#62bcec'),.16)
 visible(aura,377,480);aura.location=(-1,2.4,-.5)
 keys(aura,'scale',[(377,(.1,.1,1)),(389,(1,1,1)),(421,(1.05,1.03,1)),(451,(.96,.97,1)),(480,(1,1,1))])
 for i in range(24):
  a=i*2*math.pi/24;rr=2.6+random.random()*.4
  pts=[(math.cos(a)*rr*.5,math.sin(a)*rr+3.2),(math.cos(a+.035)*rr*.72,math.sin(a+.035)*rr*1.3+3.2),(math.cos(a+.08)*rr*.6,math.sin(a+.08)*rr+3.2)]
  p=poly('DT_AuraFlare_%02d'%i,pts,'#8bdbf5',-.8,fx);visible(p,377,480)
  keys(p,'location',[(377,(-1,1.6,0)),(403,(-1,2.5,0)),(480,(-1,2.1,0))])
  keys(p,'scale',[(377,(.1,.1,1)),(389,(1,1,1)),(405,(1.1,1.08,1)),(421,(.95,1.02,1)),(449,(1.13,1.06,1)),(480,(1,1,1))])
 for i in range(12):
  x=random.uniform(-3,3);y=random.uniform(.4,7)
  pts=[(x,y),(x+.12,y+.65),(x-.08,y+.98),(x+.18,y+1.5)]
  p=line('DT_ElectricArc_%02d'%i,pts,'#d6faff',.035,2,fx);visible(p,165 if i<6 else 381,240 if i<6 else 480)
  for f in range(165 if i<6 else 381,241 if i<6 else 481,7):p.location=(random.uniform(-.12,.12),random.uniform(-.2,.2)+(1.5 if i>=6 else 0),0);p.keyframe_insert('location',frame=f)
 # World-space streaks sell screen travel without replacing limb animation.
 for i in range(30):
  x=random.uniform(-14,14);y=random.uniform(.8,8)
  p=line('DT_SpeedLine_%02d'%i,[(x,y),(x+random.uniform(.6,2),y+.05)],'#f4d2ba',.014,-.8,fx);visible(p,249,356)
  for f in range(249,359,8):p.location=((i*.79-(f-249)*.37)%8-4,0,0);p.keyframe_insert('location',frame=f)
 # Floating practice target: geometric stone and concentric painted rings.
 target=bpy.data.objects.new('DT_Target_Control',None);fx.objects.link(target);target.location=(7,5.2,0)
 for i,(rad,color) in enumerate([(1.25,'#514e65'),(1.16,'#b1a1a3'),(.86,'#aa696d'),(.59,'#c3b5af'),(.27,'#9f6067'),(.1,'#eee0cd')]):
  q=ellipse('DT_Target_Ring_%d'%i,0,0,rad,rad,color,.6+i*.02,fx);q.parent=target;visible(q,481,551)
 for i in range(7):
  a=i*2*math.pi/7;pts=[(math.cos(a)*.94,math.sin(a)*.94),(math.cos(a+.08)*.73,math.sin(a+.08)*.73),(math.cos(a+.12)*.55,math.sin(a+.12)*.55)]
  q=line('DT_Target_Crack_%d'%i,pts,'#625c6c',.02,.9,fx);q.parent=target;visible(q,481,551)
 keys(target,'location',[(481,(7,5.2,0)),(505,(7,5.35,0)),(529,(7,5.18,0)),(537,(7.16,5.24,0)),(551,(7.4,5.3,0))])
 # Evaluate the posed hand to place the energy at its actual animation control.
 film.frame_set(517);o,r,cc,co=ASSETS['RUN'];bpy.context.view_layer.update();muzzle=r.matrix_world@r.pose.bones['hand.R'].head;muzzle.x+=.3
 energy=bpy.data.objects.new('DT_Blast_Control',None);fx.objects.link(energy);energy.location=(muzzle.x,muzzle.y,2)
 for i,(rad,col) in enumerate([(.65,'#79c8ee'),(.43,'#b4ecff'),(.25,'#f5ffff')]):
  q=ellipse('DT_ChargeOrb_%d'%i,0,0,rad,rad,col,0+i*.01,fx);q.parent=energy;visible(q,493,561)
  keys(q,'scale',[(493,(.04,.04,1)),(512,(1,1,1)),(520,(1.2,1.2,1)),(550,(1.15,1.15,1)),(561,(.01,.01,1))])
 end=Vector((7,5.2));start=Vector((muzzle.x,muzzle.y));direction=end-start;length=direction.length;angle=math.atan2(direction.y,direction.x)
 for i,(w,col) in enumerate([(.43,'#69b9e7'),(.26,'#b4ecff'),(.12,'#f9ffff')]):
  q=poly('DT_BlastBeam_%d'%i,[(0,-w),(length,-w*.43),(length+.4,0),(length,w*.43),(0,w)],col,2.5+i*.03,fx);q.location=(start.x,start.y,0);q.rotation_euler.z=angle;visible(q,517,561)
  keys(q,'scale',[(517,(.015,.25,1)),(523,(1,1,1)),(548,(1,1.13,1)),(556,(1,.6,1)),(561,(1,.01,1))],'LINEAR')
 for i in range(12):
  a=i*math.pi/6;pts=[(7+math.cos(a)*.3,5.2+math.sin(a)*.3),(7+math.cos(a-.06)*2,5.2+math.sin(a-.06)*2),(7+math.cos(a+.06)*.65,5.2+math.sin(a+.06)*.65)]
  q=poly('DT_ImpactRay_%d'%i,pts,'#f4fcff',3,fx);visible(q,525,553)
 for i in range(16):
  x=random.uniform(-.8,.8);y=random.uniform(-.8,.8);rad=random.uniform(.08,.27)
  q=poly('DT_TargetFragment_%d'%i,[(x-rad,y),(x,y+rad),(x+rad,y+.04),(x+rad*.6,y-rad)],random.choice(['#b9aca9','#70697e','#a58286']),1,fx);visible(q,549,600)
  keys(q,'location',[(549,(7,5.2,0)),(570,(7+x*4,5.2+y*4,0)),(600,(7+x*8,2+y*6,0))],'LINEAR');keys(q,'rotation_euler',[(549,(0,0,0)),(600,(0,0,random.uniform(-5,5)))])
 for i in range(14):
  side=-1 if i%2 else 1;rx=random.uniform(.15,.45);x=1.2
  q=ellipse('DT_LandingDust_%d'%i,0,0,rx,rx*.45,'#d8ac8e',1.1,fx);visible(q,611,644)
  keys(q,'location',[(611,(x,-.05,0)),(625,(x+side*(.6+i*.13),.05+i*.015,0)),(644,(x+side*(1.8+i*.14),.18+i*.03,0))]);keys(q,'scale',[(611,(.1,.1,1)),(621,(1.6,1.3,1)),(644,(.01,.01,1))])
 # A few rising stones during the energy build, all hand-editable objects.
 for i in range(12):
  x=random.uniform(-4,2);y=random.uniform(.1,.7);rad=random.uniform(.05,.16)
  q=poly('DT_LevitationStone_%d'%i,[(x-rad,y),(x,y+rad),(x+rad,y),(x,y-rad)],'#a58b87',1,fx);visible(q,391,480);keys(q,'location',[(391,(0,0,0)),(440,(0,1.5+i*.06,0)),(480,(.1,2.1+i*.1,0))])
 # Film titles, modest and legible, in the scene rather than baked into frames.
 titles=collection('DT_Titles')
 q=text_obj('DT_Title_Opening','DAWN\nTRAINING',2.1,6.1,.86,'#fff0d5',c=titles);q.data.space_line=.9;visible(q,25,109)
 q=text_obj('DT_Title_OpeningSubtitle','A NEW DAY. A HIGHER LIMIT.',2.15,5.55,.18,'#fff0d5',c=titles);visible(q,37,109)
 q=text_obj('DT_Title_End','DAWN TRAINING',-7,2.9,.55,'#ffefd5',c=titles);visible(q,681,720)
 q=text_obj('DT_Title_EndSubtitle','SAME SPIRIT. HIGHER TOMORROW.',-6.97,2.35,.16,'#ffefd5',c=titles);visible(q,687,720)
 # Scene-local exclusions keep studio/reference review beginner-friendly.
 for lc in studio.view_layers[0].layer_collection.children:
  if lc.name.startswith('DT_Character_') and lc.name!='DT_Character_FRONT':lc.exclude=True
 # Keep an independent, unanimated neutral asset in the character studio.
 src,rig,frontcoll,_=ASSETS['FRONT'];film.frame_set(1)
 studio.collection.children.unlink(frontcoll)
 sc=collection('DT_Studio_Character',studio)
 rr=rig.copy();rr.data=rig.data.copy();rr.name='DT_STUDIO_RIG_FRONT';sc.objects.link(rr);rr.animation_data_clear();rr.location=(0,0,0);rr.scale=(1,1,1)
 for b in rr.pose.bones:b.matrix_basis=Matrix.Identity(4)
 for prop in ['Blink','BrowFocus','MouthOpen','Smirk']:rr[prop]=0.
 oo=src.copy();oo.data=src.data.copy();oo.name='DT_STUDIO_GP_FRONT';sc.objects.link(oo);oo.animation_data_clear();oo.hide_render=False;oo.hide_viewport=False
 for l in oo.data.layers:
  if l.parent==rig:l.parent=rr
 if oo.data.animation_data:
  for fc in oo.data.animation_data.drivers:
   for v in fc.driver.variables:
    for t in v.targets:
     if t.id==rig:t.id=rr
 # Reset every visibility curve to constant to avoid accidental fades between cuts.
 for obj in film.objects:
  if not obj.animation_data or not obj.animation_data.action:continue
  action=obj.animation_data.action
  for slot in action.slots:
   for la in action.layers:
    for st in la.strips:
     bag=st.channelbag(slot)
     if bag:
      for fc in bag.fcurves:
       if fc.data_path in ['hide_render','hide_viewport']:
        for k in fc.keyframe_points:k.interpolation='CONSTANT'
 # Beginner instructions travel inside the .blend as a Text block.
 guide=bpy.data.texts.get('START_HERE - Dawn Training') or bpy.data.texts.new('START_HERE - Dawn Training')
 guide.clear();guide.write('DAWN TRAINING\n\nOpen scene DT_03_DAWN_TRAINING and press Space to play.\nFrame range: 1-720. Frame rate: 24 fps.\nSix camera markers are the shot cuts. Numpad 0 shows the camera.\n\nDT_01_CHARACTER_STUDIO: neutral artwork and rig.\nDT_02_POSE_TESTS: standing, sitting, running, crouching, power-up. Play 1-37 for motion checks.\n\nSelect DT_RIG_* > Pose Mode. Select a body bone, press R then Z.\nRotate within the drawing plane. Every named artwork layer follows its bone.\nMove the armature object for whole-character placement.\nFor Front and Focus, Object Properties > Custom Properties gives Blink, BrowFocus, MouthOpen and Smirk.\n\nAlternate Drawings keep the supplied designs for back, side run, crouch and power-up.\nLarge view changes use these drawings; small movements use the simple cutout rig.\n\nGrease Pencil object > Data Properties > Layers: select the part to edit.\nEdit Mode edits Bezier control points; Draw Mode adds new strokes.\nHiddenJoint layers cover limited joint rotations. Extreme new poses may need correction drawings.\nReferences are packed, locked image empties in DT_References.\n\nSee BEGINNER_GUIDE.md next to the project for stages, render commands and limitations.\n')
 film.frame_set(1);film.render.filepath=str(OUT/'frames/frame_');bpy.context.window.scene=film
 # Give the saved viewport the actual film composition.
 for screen in bpy.data.screens:
  for area in screen.areas:
   if area.type=='VIEW_3D':
    area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.overlay.show_overlays=False;area.spaces.active.shading.type='MATERIAL'
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Dawn_Training.blend'))
 extra=bpy.data.scenes.get('Scene')
 if extra and {ob.name for ob in extra.objects}=={'Cube','Camera','Light'}:
  extras=list(extra.objects);bpy.data.scenes.remove(extra)
  for ob in extras:
   if not ob.users_scene:bpy.data.objects.remove(ob,do_unlink=True)
 report={'blender':bpy.app.version_string,'build_hash':bpy.app.build_hash.decode(),'scenes':[s.name for s in SCENES],'assets':{n:{'object':o.name,'rig':r.name,'layers':len(o.data.layers),'bones':len(r.data.bones),'curves':sum(len(f.drawing.strokes) for l in o.data.layers for f in l.frames)} for n,(o,r,c,co) in ASSETS.items()},'shots':[{'name':n,'start':st,'end':en} for n,st,en,_ in shots],'blast_origin':[muzzle.x,muzzle.y],'resolution':[1920,1080],'fps':24,'frames':720}
 (OUT/'build_report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
 # Render a representative frame from every shot, then inspect before full output.
 for f in [61,193,289,421,533,617,697]:
  film.frame_set(f);film.render.filepath=str(OUT/f'review/shot_{f:04}.png');bpy.ops.render.render(write_still=True)
 film.frame_set(1);film.render.filepath=str(OUT/'frames/frame_');bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Dawn_Training.blend'))
 return report
if __name__=='__main__':build()

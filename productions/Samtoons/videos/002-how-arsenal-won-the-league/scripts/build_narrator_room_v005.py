"""Visible, additive authoring: one shared room; per-shot cameras and performances.
Run functions in small batches through the connected Blender instance.
"""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animation-v005'
ROOM='S002 / Narrator room / shared v005';PREFIX='S002_v005_'

def mat(name,color):
 m=bpy.data.materials.get(name)
 if m:return m
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=.85
 return m

def box(col,name,loc,size,color):
 x,y,z=[v/2 for v in size];verts=[(a*x,b*y,c*z) for a,b,c in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)]);ob=bpy.data.objects.new(name,mesh);col.objects.link(ob);ob.location=loc;mesh.materials.append(mat('Room / '+str(color),color));return ob

def camera(s,loc,target,scale):
 d=bpy.data.cameras.new(s.name+' camera');d.type='PERSP';d.lens=27 if scale>5 else 38;o=bpy.data.objects.new(d.name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();s.camera=o;return o

def show(s):
 bpy.context.window.scene=s
 for a in bpy.context.screen.areas:
  if a.type=='VIEW_3D':
   a.spaces.active.camera=s.camera;a.spaces.active.region_3d.view_camera_zoom=10;a.spaces.active.region_3d.view_camera_offset=(0,0);a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.shading.type='MATERIAL';a.spaces.active.shading.use_scene_world=True;a.spaces.active.shading.use_scene_lights=True;a.spaces.active.overlay.show_overlays=False
 s.frame_set(1)

def build_room():
 assert ROOM not in bpy.data.collections
 col=bpy.data.collections.new(ROOM)
 box(col,'Room / floor',(0,-.5,-.09),(7.2,7,.18),(.085,.067,.055))
 box(col,'Room / rear wall',(0,2.8,1.8),(7.2,.12,3.6),(.028,.057,.084))
 box(col,'Room / right wall',(3.6,-.5,1.8),(.12,6.7,3.6),(.042,.079,.104))
 for x in [-3,-2,-1,0,1,2,3]:box(col,'Room / wall panelling',(x,2.72,1.8),(.025,.045,3.6),(.085,.128,.15))
 box(col,'Room / rug',(0,-.45,.018),(4.4,3.9,.024),(.105,.04,.045))
 box(col,'Room / chair seat',(0,.05,.68),(1.3,.85,.16),(.065,.048,.044))
 box(col,'Room / chair back',(0,.38,1.1),(1.35,.18,.9),(.068,.055,.045))
 for x in [-.52,.52]:
  box(col,'Room / chair arm',(x,0,.9),(.16,.92,.16),(.11,.074,.046))
  for y in [-.26,.33]:box(col,'Room / chair leg',(x,y,.32),(.09,.09,.64),(.04,.027,.025))
 box(col,'Room / desk top',(0,-1.05,.9),(3.35,1,.12),(.22,.11,.049))
 box(col,'Room / desk front',(0,-1.49,.51),(3.25,.12,.72),(.105,.054,.03))
 for x in [-1.45,1.45]:box(col,'Room / desk support',(x,-1.05,.43),(.12,.85,.86),(.065,.04,.025))
 box(col,'Room / lamp base',(1.1,-.95,1.0),(.38,.27,.06),(.4,.28,.06))
 box(col,'Room / lamp stem',(1.1,-.95,1.24),(.035,.035,.44),(.42,.3,.065))
 box(col,'Room / green lamp shade',(1.1,-.95,1.47),(.55,.29,.18),(.022,.19,.1))
 box(col,'Room / television case',(3.46,-1.1,1.68),(.16,1.82,1.16),(.012,.018,.024))
 screen=box(col,'Room / television screen',(3.365,-1.1,1.68),(.02,1.63,.98),(.075,.22,.045))
 m=screen.data.materials[0];p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(.075,.22,.045,1);p.inputs['Emission Strength'].default_value=.35
 for yy in [-1.85,-.35]:box(col,'Room / TV pitch border',(3.35,yy,1.68),(.012,.014,.83),(.6,.68,.5))
 for zz in [1.26,2.10]:box(col,'Room / TV pitch border',(3.35,-1.1,zz),(.012,1.5,.014),(.6,.68,.5))
 box(col,'Room / TV halfway line',(3.35,-1.1,1.68),(.012,.014,.83),(.6,.68,.5))
 col['continuity']='One physical set shared by every narrator/Ferguson shot. Furniture never swaps sides for the reveal.'
 rows=json.loads((V/'artifacts/animation-v003/edit.json').read_text());ids=['N01','N02','N03','N04_dark','N04_reveal','N04_meltdown','N04_tap']
 for row in rows:
  sid=row['id']
  if sid not in ids:continue
  s=bpy.data.scenes.new(PREFIX+sid);s.collection.children.link(col);s['shot_id']=sid;s['environment']=ROOM;s['status']='Rebuild in progress; not finished character animation'
  s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=16;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_end=row['frames'];s.view_settings.view_transform='Standard';s.view_settings.look='None'
  w=bpy.data.worlds.new(s.name);w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(.07,.1,.16,1);w.node_tree.nodes['Background'].inputs[1].default_value=.2;s.world=w
  rear=sid in ['N01','N02','N03'];loc=(-.9,2.35,2.2) if rear else (-.15,-3.4,1.95)
  camera(s,loc,(.5,-.45,1.2) if rear else (0,0,1.24),5.9 if rear else 3.8)
  if rear:s.camera.data.lens=24
  if sid=='N04_tap':camera(s,(-2.8,-3.15,2.0),(1.15,-.45,1.2),5.6)
  for name,loc,energy,size,color in [('soft window',(-2,-1,3.2),110,4,(.55,.68,1)),('lamp practical',(1.1,-.95,1.37),0 if rear or sid=='N04_dark' else 32,1,(1,.64,.29))]:
   d=bpy.data.lights.new(s.name+' / '+name,'AREA');d.energy=energy;d.shape='DISK';d.size=size;d.color=color;o=bpy.data.objects.new(d.name,d);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,1.1))-o.location).to_track_quat('-Z','Y').to_euler()
 show(bpy.data.scenes[PREFIX+'N01'])
 return {'shared_collection':col.name,'scenes':ids,'furniture_objects':len(col.objects)}

def key(ob,path,values):
 for f,value in values:setattr(ob,path,value);ob.keyframe_insert(data_path=path,frame=f)
 for layer in ob.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='BEZIER';k.handle_left_type=k.handle_right_type='AUTO_CLAMPED'

def append_sources():
 names=['S002_fullmotion_N01','S002_fullmotion_N04_reveal','S002_fullmotion_N04_dark']
 missing=[n for n in names if n not in bpy.data.scenes]
 if missing:
  with bpy.data.libraries.load(str(V/'artifacts/animation-v004/acting-batch-v004.blend'),link=False) as (src,dst):dst.scenes=missing

def rig_seated(sid,rear=False,dark=False):
 """Video001's constrained-joint/continuous-skin mechanism, fitted to seated art.
 Bounds are modest seated acting; this rig is not a run/jump/standing solution.
 """
 append_sources();s=bpy.data.scenes[PREFIX+sid];show(s)
 source=bpy.data.scenes['S002_fullmotion_'+('N01' if rear else 'N04_dark' if dark else 'N04_reveal')]
 src=next(o for o in source.objects if o.type=='MESH' and o.parent and o.parent.get('asset')=='ferguson')
 root=bpy.data.objects.new(s.name+' / seated Ferguson',None);s.collection.objects.link(root);root.rotation_euler=(math.pi/2,0,math.pi if rear else 0);root.location=(0,0,.015)
 unit=(5.0 if rear else 5.2)/550;root.scale=(.0045/unit,)*3
 mesh=src.data.copy();skin=bpy.data.objects.new(s.name+' / coherent seated artwork',mesh);s.collection.objects.link(skin);skin.parent=root
 if skin.data.shape_keys:skin.shape_key_clear()
 for poly in mesh.polygons:poly.use_smooth=False
 # Recover registration from source UV and geometry, not a guessed crop bottom.
 lp=mesh.loops[0];uv=mesh.uv_layers.active.data[0].uv;p=mesh.vertices[lp.vertex_index].co
 cx=uv.x*1536-p.x/unit;cy=p.y/unit+(1-uv.y)*1024
 xy=lambda pixel:Vector(((pixel[0]-cx)*unit,(cy-pixel[1])*unit,0))
 if rear:
  pts={'hip':(301,310),'neck':(306,111),'head':(303,48),'Ls':(216,155),'Le':(202,228),'Lw':(219,277),'Lf':(236,289),'Rs':(393,153),'Re':(414,219),'Rw':(398,274),'Rf':(376,286)}
 else:
  pts={'hip':(773,291),'neck':(773,146),'head':(780,58),'Ls':(660,153),'Le':(650,224),'Lw':(714,239),'Lf':(738,243),'Rs':(859,154),'Re':(882,225),'Rw':(852,239),'Rf':(827,244)}
 rest={k:xy(p) for k,p in pts.items()};controls={}
 for name,pos in rest.items():
  o=bpy.data.objects.new(s.name+' / CTRL '+name,None);s.collection.objects.link(o);o.parent=root;o.location=pos;o.empty_display_size=.07;controls[name]=o
 bones={'torso':('hip','neck'),'head':('neck','head'),'L upper arm':('Ls','Le'),'L forearm':('Le','Lw'),'L hand':('Lw','Lf'),'R upper arm':('Rs','Re'),'R forearm':('Re','Rw'),'R hand':('Rw','Rf')}
 ad=bpy.data.armatures.new(s.name+' / seated binding');arm=bpy.data.objects.new(ad.name,ad);s.collection.objects.link(arm);arm.parent=root;arm.show_in_front=True
 bpy.ops.object.select_all(action='DESELECT');arm.select_set(True);bpy.context.view_layer.objects.active=arm;bpy.ops.object.mode_set(mode='EDIT')
 for name,(a,b) in bones.items():e=ad.edit_bones.new(name);e.head=rest[a];e.tail=rest[b]
 e=ad.edit_bones.new('seat support');e.head=rest['hip'];e.tail=rest['hip']+Vector((0,.15,0))
 bpy.ops.object.mode_set(mode='OBJECT')
 for name,(a,b) in bones.items():
  pb=arm.pose.bones[name];c=pb.constraints.new('COPY_LOCATION');c.target=controls[a];c=pb.constraints.new('STRETCH_TO');c.target=controls[b];c.rest_length=(rest[b]-rest[a]).length;c.volume='NO_VOLUME';c.bulge=0
 groups={n:skin.vertex_groups.new(name=n) for n in [*bones,'seat support']}
 def dist(p,a,b):v=b-a;return (p-(a+v*max(0,min(1,(p-a).dot(v)/v.length_squared)))).length
 for v in mesh.vertices:
  px=cx+v.co.x/unit;py=cy-v.co.y/unit
  if py>pts['hip'][1]+15:weights=[('seat support',1)]
  elif py<pts['neck'][1]-6:weights=[('head',1)]
  else:
   side='L' if px<cx else 'R';candidates=['torso',side+' upper arm',side+' forearm',side+' hand']
   if py<pts['neck'][1]+15:candidates=['torso','head']
   ds=sorted((dist(v.co,rest[bones[n][0]],rest[bones[n][1]])-(.12 if n=='torso' else 0),n) for n in candidates)[:2]
   vals=[math.exp(-max(0,d)**2/.022) for d,n in ds];total=sum(vals);weights=[(n,w/total) for (d,n),w in zip(ds,vals)] if total>1e-20 else [(ds[0][1],1)]
   if py>pts['hip'][1]-18:
    t=max(0,min(1,(py-(pts['hip'][1]-18))/33));weights=[(n,w*(1-t)) for n,w in weights]+[('seat support',t)]
  for n,w in weights:groups[n].add([v.index],w,'REPLACE')
 mod=skin.modifiers.new('Video001 fitted joint deformation','ARMATURE');mod.object=arm;mod.use_deform_preserve_volume=True
 animate_seated(s,rest,controls)
 root['method']='Bounded seated joint animation, fitted coherent artwork; extreme rise/throw require their own construction.';root['source']='Video001 build_option_a.py / constrained joint skinning';root['rest_lengths']=json.dumps({n:(rest[b]-rest[a]).length for n,(a,b) in bones.items()});root['controls']=json.dumps({n:o.name for n,o in controls.items()})
 s['character_status']='Continuous seated rig blocking, not approved performance';s.frame_set(1);return {'scene':s.name,'skin':skin.name,'armature':arm.name,'frames':s.frame_end,'root':root.name}

def animate_seated(s,rest,controls):
 sid=s['shot_id']
 # Intentional reaction progression, with anchored seated pelvis/feet.
 # Per-frame forward kinematics keeps limb lengths constant between authored beats.
 beats=[(1,0,0),(max(2,int(s.frame_end*.2)),-.025,-.05),(max(3,int(s.frame_end*.42)),.035,.14),(max(4,int(s.frame_end*.60)),.025,.10),(max(5,int(s.frame_end*.83)),.009,.025),(s.frame_end,.009,.025)]
 def sample(f,index):
  for a,b in zip(beats,beats[1:]):
   if a[0]<=f<=b[0]:u=(f-a[0])/max(1,b[0]-a[0]);u=u*u*(3-2*u);return a[index]+(b[index]-a[index])*u
  return beats[-1][index]
 def rot(v,t):return Vector((math.cos(t)*v.x-math.sin(t)*v.y,math.sin(t)*v.x+math.cos(t)*v.y,0))
 for f in range(1,s.frame_end+1):
  strength={'N01':(.6,.2),'N02':(1.0,.8),'N03':(1.2,.35),'N04_dark':(.35,.1),'N04_reveal':(.12,0)}.get(sid,(1,1));lean=sample(f,1)*strength[0];gesture=sample(f,2)*strength[1];hip=rest['hip'];posed={k:hip+rot(p-hip,lean) for k,p in rest.items()};posed['hip']=hip
  posed['head']=posed['neck']+rot(rest['head']-rest['neck'],lean*.35)
  for side,sgn in [('L',1),('R',-.65)]:
   for a,b,angle in [('s','e',lean+gesture*sgn*.35),('e','w',lean+gesture*sgn),('w','f',lean+gesture*sgn*.85)]:posed[side+b]=posed[side+a]+rot(rest[side+b]-rest[side+a],angle)
  for name,o in controls.items():o.location=posed[name];o.keyframe_insert(data_path='location',frame=f)
 for o in controls.values():
  for layer in o.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for k in fc.keyframe_points:k.interpolation='LINEAR'

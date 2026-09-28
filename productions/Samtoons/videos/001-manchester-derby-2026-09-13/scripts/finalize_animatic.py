"""Apply voice timing and review fixes to the saved full animatic in visible Blender."""
from pathlib import Path
import bpy,json,math,ast
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/animatic-v001'
def curves(action):
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:yield from bag.fcurves

def apply():
 F=bpy.app.driver_namespace['film_builder'];tree=ast.parse(Path(F['__file__']).read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='bind_new'],type_ignores=[]),'binding_revision','exec'),F)
 for a in F['CAST'].values():
  try:
   if a['config'].get('crop'):F['bind_new'](a)
  except ReferenceError:pass
 timing=json.loads((OUT/'mouth-timing.json').read_text());report=[];grouped={}
 for row in timing:grouped.setdefault(row['mouth'],[]).append(row)
 for name,rows in grouped.items():
  ob=bpy.data.objects[name];s=bpy.data.scenes[rows[0]['scene']]
  if ob.type=='FONT':continue # Offscreen VAR operator; the monitor is not a talking face.
  if 'open' not in ob:
   # Talking-post mouth has native geometry beneath an empty control.
   for row in rows:
    for frame,value in row['jaw_keys']:ob.scale.y=.18+value;ob.keyframe_insert(data_path='scale',index=1,frame=frame)
   continue
  if ob.animation_data and ob.animation_data.action:
   for fc in list(curves(ob.animation_data.action)):
    if fc.data_path=='["open"]':
     while len(fc.keyframe_points):fc.keyframe_points.remove(fc.keyframe_points[-1],fast=True)
  # Preserve crying effort after Oliver's sentence; silence closes normal dialogue.
  baseline=[(1,.025),(s.frame_end,.025)]
  if 'Apology Oliver' in name:baseline=[(1,.025),(118,.4),(128,1.3),(145,.65),(159,1.4),(178,.6),(198,1.25),(215,.65),(264,.55)]
  for fr,v in baseline:ob['open']=v;ob.keyframe_insert(data_path='["open"]',frame=fr)
  for row in rows:
   for frame,value in row['jaw_keys']:ob['open']=value;ob.keyframe_insert(data_path='["open"]',frame=frame)
   # Narrow during round vowels and close at the take boundary. Expression and
   # jaw are editable; frame-level phoneme alignment remains a delivery polish check.
   start=row['frame'];end=start+math.ceil(row['duration_seconds']*24)
   for fr,scale in [(start-1,1),(start+2,.88 if 'sorry' in row['text'].lower() else 1.08),(end-2,1),(end,1)]:ob.scale.x=scale;ob.keyframe_insert(data_path='scale',index=0,frame=fr)
   report.append(dict(mouth=name,start=start,end=end,source=row['path']))
  for fc in curves(ob.animation_data.action):
   if fc.data_path=='["open"]':
    for k in fc.keyframe_points:k.interpolation='BEZIER';k.handle_left_type=k.handle_right_type='AUTO_CLAMPED'
 # Syllabic captions follow the actual takes and disappear before the next beat.
 for row in timing:
  s=bpy.data.scenes[row['scene']]
  if row['id'] in ('bruno-approved','carrick-approved'):continue # Retain approved existing captions.
  F['D'].update(s=s,col=s.collection.children[0],cam=s.camera);F['A'].update(s=s,col=s.collection.children[0],cam=s.camera);F['A']['base'].update(s=s,skin=s.collection.children[0]);bpy.context.window.scene=s
  F['cap'](row['text'],row['frame'],min(s.frame_end,row['frame']+math.ceil(row['duration_seconds']*24)+12),y=-.37,size=.039)
 # Foden is supported by a small boat in the flood; connect the line to its float.
 s=bpy.data.scenes['FILM S10 / They are biting'];bpy.context.window.scene=s
 F['D'].update(s=s,col=s.collection.children[0],cam=s.camera);F['A'].update(s=s,col=s.collection.children[0],cam=s.camera);F['A']['base'].update(s=s,skin=s.collection.children[0])
 boat=F['empty']('Foden boat',(.8,-.10,.10));boat.rotation_euler.x=math.pi/2
 F['poly']('Boat hull',[(-.9,.10),(-.62,-.08),(.66,-.08),(.97,.16)],0,'#946849',boat)
 F['line']('Boat rim',[(-.9,.10),(.97,.16)],.02,'#ecc28d',.045,boat)
 old=s.objects['Payoff fishing line'];bpy.data.objects.remove(old,do_unlink=True)
 tip=F['empty']('Rod tip',(-.85,3.2,.02),s.objects['Payoff rod']);line=F['A']['tube']('Connected fishing line',[(0,0,0)]*3,'#f6efda',.006)
 for fr in range(1,217):
  s.frame_set(fr);bpy.context.view_layer.update();p=tip.matrix_world.translation.copy();q=Vector((-.18,-.2,.28))+s.objects['Biting float'].location
  mid=(p+q)/2+Vector((-.10,0,-.10))
  for point,v in zip(line.data.splines[0].points,(p,mid,q)):point.co=(*v,1);point.keyframe_insert(data_path='co',frame=fr)
 # Restrained push-in on held new-shot endings. Cuts remain cuts; movement eases.
 for row in F['EDIT']:
  if not row['scene'].startswith('FILM ') or row['scene'].endswith('VAR office'):continue
  s=bpy.data.scenes[row['scene']];cam=s.camera;last=s.frame_end;s.frame_set(max(1,last-72));loc=cam.location.copy();direction=cam.rotation_euler.to_quaternion()@Vector((0,0,-1))
  cam.keyframe_insert(data_path='location',frame=max(1,last-72));cam.location=loc+direction*.16;cam.keyframe_insert(data_path='location',frame=last)
  for fc in curves(cam.animation_data.action):
   if fc.data_path=='location':
    for k in fc.keyframe_points:
     if k.co.x>=last-72:k.interpolation='BEZIER';k.handle_left_type=k.handle_right_type='AUTO_CLAMPED'
 # Source actions retain the approved event times and exact total duration.
 assert len(F['EDIT'])==16 and sum(r['frames'] for r in F['EDIT'])==3600
 for row in timing:assert row['frame']+math.ceil(row['duration_seconds']*24)<=bpy.data.scenes[row['scene']].frame_end
 (OUT/'mouth-checks.json').write_text(json.dumps(dict(cues=report,method='Cached take energy guides jaw effort and pauses; editable mouth-width and emotional curves. Not phoneme-level forced alignment.',accepted_audio='No approved recording regenerated',frames=3600),indent=2)+'\n')
 bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'combined-animatic-v002.blend'))
 return {'file':bpy.data.filepath,'jaw_performances':len(report)}

def assemble_review_timeline():
 edit=json.loads((OUT/'edit.json').read_text());s=bpy.data.scenes.new('SAMTOONS / complete animatic');bpy.context.window.scene=s
 s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=75;s.render.fps=24;s.render.fps_base=1;s.frame_start=1;s.frame_end=3600;s.render.use_sequencer=True;s.sync_mode='AUDIO_SYNC';ed=s.sequence_editor_create()
 for i,row in enumerate(edit):
  strip=ed.strips.new_scene(row['scene'],bpy.data.scenes[row['scene']],1,row['start_frame']);strip.scene_input='CAMERA';strip.frame_final_duration=row['frames']
 sound=ed.strips.new_sound('Authoritative full review mix',str(OUT/'mix-review.wav'),2,1)
 assert round(sound.frame_final_duration)==3600 and len(ed.strips)==17
 s['Review']='150-second combined animatic; pending user review, not final delivery.'
 for ar in bpy.context.screen.areas:
  if ar.type=='VIEW_3D':ar.type='SEQUENCE_EDITOR';ar.spaces.active.view_type='PREVIEW'
 bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'combined-animatic-editable.blend'))
 return {'file':bpy.data.filepath,'scenes':16,'audio_strips':1,'frames':3600}

def native_forearms():
 """Use editable drawn forearms/hands where the new raster hand bends fail."""
 import bmesh
 F=bpy.app.driver_namespace['film_builder'];count=0
 for a in F['CAST'].values():
  if not a['config'].get('crop'):continue
  root=a['root'];s=next(s for s in bpy.data.scenes if root.name in s.objects);bpy.context.window.scene=s;s.frame_set(1)
  col=s.collection.children[0];F['A'].update(s=s,col=col,cam=s.camera);base=F['A']['base'];base.update(s=s,skin=col,ink=F['A']['mat']('#202329'))
  r=a['rest'];mesh=a['skin'].data;bm=bmesh.new();bm.from_mesh(mesh);remove=[]
  for face in bm.faces:
   c=face.calc_center_median()
   for side,sign in [('L',-1),('R',1)]:
    if sign*(c.x-r['hip'].x)>.83 and r[side+'finger'].y-.48<c.y<r[side+'elbow'].y+.16:remove.append(face);break
  bmesh.ops.delete(bm,geom=remove,context='FACES');bm.to_mesh(mesh);bm.free()
  color='#9b562d' if 'Rashford' in root.name or 'Mainoo' in root.name else '#efb786'
  if 'Lammens' in root.name:color='#fff5e8'
  for side,sign in [('L',-1),('R',1)]:
   ctl=a['controls'];base['driven_limb'](root.name+' native '+side,[ctl[side+'elbow'],ctl[side+'wrist'],ctl[side+'wrist']],.13,color,root,.045)
   hand=F['empty'](root.name+' palm '+side,(0,0,.08),root)
   c=hand.constraints.new('COPY_LOCATION');c.target=ctl[side+'wrist'];c.use_offset=False
   c=hand.constraints.new('DAMPED_TRACK');c.target=ctl[side+'finger'];c.track_axis='TRACK_Y'
   points=[(-.12,0),(.12,0),(.13,.12),(.22,.18),(.24,.24),(.20,.28),(.15,.26),(.10,.20),(.11,.40),(.10,.46),(.06,.48),(.025,.44),(.02,.25),(0,.49),(-.04,.50),(-.075,.46),(-.07,.24),(-.09,.43),(-.13,.43),(-.155,.38),(-.135,.22),(-.16,.32),(-.19,.30),(-.205,.24),(-.18,.11)]
   F['poly'](root.name+' hand '+side,[(sign*x,y) for x,y in points],.04,color,hand)
   for ob in hand.children:
    if ob.type=='CURVE':ob.data.bevel_depth=.015
  count+=1
 # Keep new dialogue comfortably inside the safe picture area.
 for row in json.loads((OUT/'mouth-timing.json').read_text()):
  s=bpy.data.scenes[row['scene']]
  for ob in s.objects:
   if ob.type=='FONT' and ob.data.body==row['text'] and ob.parent==s.camera:ob.location.y=-.30
 bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'combined-animatic-v003.blend'))
 return {'actors_with_native_forearms':count,'file':bpy.data.filepath}

def resume_builder():
 p=ROOT/'scripts/build_full_animatic.py';F={'__file__':str(p)};exec(compile(p.read_text(),str(p),'exec'),F)
 F['EDIT'][:]=json.loads((OUT/'edit.json').read_text());F['SPEECH'][:]=json.loads((OUT/'speech.json').read_text())
 for tag,row in json.loads((OUT/'cast-registry.json').read_text()).items():
  prefix='A '+tag+' / ';root=bpy.data.objects.get(prefix+'ROOT')
  if root is None:continue
  F['CAST'][tag]=dict(root=root,config=row['config'],rest={k:Vector(v) for k,v in row['rest'].items()},controls={k:bpy.data.objects[prefix+'CTRL '+k] for k in row['rest']},skin=next(o for o in root.children if o.type=='MESH' and any(m.type=='ARMATURE' for m in o.modifiers)),armature=next(o for o in root.children if o.type=='ARMATURE'),facial={'mouth':bpy.data.objects[prefix+'mouth control']})
 bpy.app.driver_namespace['film_builder']=F
 return F

def connect_native_arms():
 F=resume_builder()
 for a in F['CAST'].values():
  if not a['config'].get('crop'):continue
  root=a['root'];s=next(s for s in bpy.data.scenes if root.name in s.objects);bpy.context.window.scene=s;col=s.collection.children[0];base=F['A']['base'];base.update(s=s,skin=col,ink=F['A']['mat']('#202329'))
  color='#9b562d' if 'Rashford' in root.name or 'Mainoo' in root.name else '#efb786'
  if 'Maresca' in root.name:color='#1a2c47'
  if 'Lammens' in root.name:color='#a77cce'
  for side in 'LR':
   ctl=a['controls'];base['driven_limb'](root.name+' upper '+side,[ctl[side+'shoulder'],ctl[side+'elbow'],ctl[side+'elbow']],.125,color,root,-.27)
   for suffix,c in [(' ink','#202329'),(' fill',color)]:
    ob=bpy.data.objects.get(root.name+' native '+side+suffix)
    if ob:ob.data.materials.clear();ob.data.materials.append(F['A']['mat'](c))
   for joint in ('elbow','wrist'):
    parent=ctl[side+joint]
    F['poly'](root.name+' joint outline '+side+joint,F['oval'](0,0,.145,.145),.08,'#202329',parent,False)
    F['poly'](root.name+' joint fill '+side+joint,F['oval'](0,0,.129,.129),.09,color,parent,False)
 bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'combined-animatic-v004.blend'))
 return {'file':bpy.data.filepath}

def verify_native():
 F=resume_builder();worst=0.;samples=0
 for a in F['CAST'].values():
  if not a['config'].get('crop'):continue
  root=a['root'];s=next(s for s in bpy.data.scenes if root.name in s.objects);bpy.context.window.scene=s
  for fr in (1,40,min(120,s.frame_end),s.frame_end):
   s.frame_set(fr);bpy.context.view_layer.update()
   for side in 'LR':
    wrist=a['controls'][side+'wrist'];palm=s.objects[root.name+' palm '+side]
    err=(wrist.matrix_world.translation-palm.matrix_world.translation).length;worst=max(worst,err);assert err<.001,(root.name,fr,err)
    curve=s.objects[root.name+' native '+side+' fill'].evaluated_get(bpy.context.evaluated_depsgraph_get());tip=curve.data.splines[0].bezier_points[-1].co
    assert abs(tip.x-wrist.location.x)<1e-5 and abs(tip.y-wrist.location.y)<1e-5
    samples+=1
 s=bpy.data.scenes['S08 / hope and parry'];bpy.context.window.scene=s;s.frame_set(68);bpy.context.view_layer.update();distance=(s.objects['S08 / shot football'].matrix_world.translation-s.objects['A Save Donnarumma / CTRL Lfinger'].matrix_world.translation).length;assert distance<.1
 s=bpy.data.scenes['S02 / kick and overreaction'];assert s.objects['S02 / red decision'].parent.name.endswith('CTRL Lfinger');assert not any(o.name.startswith('A / goal') for o in s.objects)
 checks=dict(native_hand_samples=samples,max_wrist_palm_error_m=worst,parry_contact_m=distance,touchline_no_goal=True,red_card_nearest_hand=True,total_frames=3600,limits='Checks prove attachment and timing, not creative approval of the full motion.')
 (OUT/'native-integration-checks.json').write_text(json.dumps(checks,indent=2)+'\n');return checks

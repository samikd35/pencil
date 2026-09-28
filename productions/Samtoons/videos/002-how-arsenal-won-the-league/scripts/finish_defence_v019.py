import bpy,math,ast,json
from mathutils import Vector
from pathlib import Path
q=bpy.app.driver_namespace['build19'];globals().update({k:q[k] for k in ['s','S','G','A','Y','R','K','opp','ball','key','pose','smooth','n','b','curves','surface','tube','mat','env','V','O']});bpy.context.window.scene=s
r=S['rest'];l1=(r['Rknee']-r['Rhip']).length;l2=(r['Rankle']-r['Rknee']).length
for f in range(1,198):
 s.frame_set(f);wind=smooth((f-148)/10);hit=smooth((f-158)/10);settle=smooth((f-178)/16);down=-.08*hit*(1-settle);pose(S,f,down=down,lean=-.02*wind,ua=(-.04*wind,.09*hit),fa=(0,.06*hit))
 ank=Vector((.20,.19,0)).lerp(Vector((-.05,.42,0)),wind).lerp(Vector((.44,.15,0)),hit).lerp(Vector((.22,.19,0)),settle);hip=r['Rhip']+Vector((0,down,0));d=ank-hip
 if d.length>l1+l2-.002:ank=hip+d.normalized()*(l1+l2-.002)
 knee=b['ik'](hip,ank,l1,l2,hip+Vector((.3,-.2,0)))
 for name,p in [('Rknee',knee),('Rankle',ank),('Rtoe',ank+r['Rtoe']-r['Rankle'])]:key(S['C'][name],'location',f,p)
s.frame_set(168);bpy.context.view_layer.update();contact=S['root'].matrix_world@S['C']['Rtoe'].location;contact.z-=.07;head=q['head'].copy();head.x+=.13;head.z+=.05;end=Vector((2.2,53.15,1.15))
for f in range(1,270):
 if f<168:p=contact.copy();p.z=.11
 elif f<=217:u=(f-168)/49;p=contact.lerp(head,u);p.z+=1.25*4*u*(1-u)
 elif f<=238:u=(f-217)/21;p=head.lerp(end,u);p.z+=.08*math.sin(math.pi*u)
 else:u=min(1,(f-238)/18);p=end.lerp(Vector((2.2,53.45,.11)),u)
 key(ball,'location',f,p)
q['contact']=contact;q['head']=head
# Distinct keeper palette: smoothly isolate yellow instead of a jagged threshold edge.
nodes=K['skin'].data.materials[0].node_tree.nodes;links=K['skin'].data.materials[0].node_tree.links;tex=next(x for x in nodes if x.type=='TEX_IMAGE' and x.image.name.startswith('football.png'));sep=nodes.new('ShaderNodeSeparateColor');sep.mode='HSV';links.new(tex.outputs['Color'],sep.inputs[0]);ramp=nodes.new('ShaderNodeValToRGB');cr=ramp.color_ramp;cr.elements.remove(cr.elements[1]);cr.elements[0].position=.10;cr.elements[0].color=(0,0,0,1)
for p,c in [(.125,(1,1,1,1)),(.22,(1,1,1,1)),(.27,(0,0,0,1))]:el=cr.elements.new(p);el.color=c
links.new(sep.outputs[0],ramp.inputs[0]);mix=next(x for x in nodes if x.type=='MIX_RGB');links.new(ramp.outputs[0],mix.inputs[0]);mix.inputs[2].default_value=(.055,.12,.28,1)
# The proud hold breaks at the ping: a reachable wrist path raises the phone.
phone=b['empty'](s,'v019 Arteta phone',A['root']);b['poly'](s,'v019 phone casing',[(-.041,-.045),(.041,-.045),(.041,.095),(-.041,.095)],'#151e28',.03,phone);b['poly'](s,'v019 phone screen',[(-.033,-.028),(.033,-.028),(.033,.077),(-.033,.077)],'#76b6d1',.034,phone,False)
r=A['rest'];l1=(r['Relbow']-r['Rshoulder']).length;l2=(r['Rwrist']-r['Relbow']).length;lh=(r['Rfinger']-r['Rwrist']).length
for f in range(988,1048):
 s.frame_set(f);t=smooth((f-990)/9);sh=A['C']['Rshoulder'].location.copy();old=A['C']['Rwrist'].location.copy();target=r['neck']+Vector((.40,-.30,0));wr=old.lerp(target,t);el=b['ik'](sh,wr,l1,l2,sh+Vector((.25,-.30,0)));finger=wr+Vector((.03,.085,0)).normalized()*lh
 for k,v in [('Relbow',el),('Rwrist',wr),('Rfinger',finger)]:key(A['C'][k],'location',f,v)
 key(phone,'location',f,wr+Vector((.015,.025,0)));key(phone,'scale',f,(t,t,t))
key(phone,'scale',1,(0,0,0));key(phone,'scale',987,(0,0,0))
# Reuse the identical physical room; only this narrator instance and its acting are local.
src=bpy.data.scenes['S002_B01_v016_narrator'];src.frame_set(130);room=bpy.data.scenes.new('S002_narrator_v019');room.world=src.world;room.render.engine='BLENDER_EEVEE';room.render.resolution_x=1280;room.render.resolution_y=720;room.render.resolution_percentage=100;room.render.fps=24;room.frame_end=48;room.eevee.taa_render_samples=24;room.view_settings.view_transform=src.view_settings.view_transform;room.view_settings.look=src.view_settings.look
for col in src.collection.children:room.collection.children.link(col)
shared=set(o for col in src.collection.children for o in col.all_objects);mapping={}
for ob in src.objects:
 if ob in shared:continue
 cp=ob.copy();cp.name='v019 '+ob.name
 if ob.data:cp.data=ob.data.copy()
 if cp.animation_data and cp.animation_data.action:cp.animation_data.action=None
 room.collection.objects.link(cp);mapping[ob]=cp
for ob,cp in mapping.items():
 cp.parent=mapping.get(ob.parent,ob.parent)
 for block in [cp,cp.data]:
  if block and block.animation_data:
   if block.animation_data.action:block.animation_data.action=None
   for fc in block.animation_data.drivers:
    for v in fc.driver.variables:
     for target in v.targets:
      if target.id in mapping:target.id=mapping[target.id]
room.camera=mapping[src.camera];cam=room.camera;cam.data.lens=27;cam.animation_data_clear();marker=room.timeline_markers.new('Narrator paper reaction',frame=1);marker.camera=cam
hand=mapping[bpy.data.objects['Narrator / L hand']];elbow=mapping[bpy.data.objects['Narrator / L elbow']];headob=mapping[bpy.data.objects['Narrator / head']]
paper=b['poly'](room,'v019 narration notes',[(-24,-12),(0,-12),(24,-12),(24,15),(24,43),(0,43),(-24,43),(-24,15)],'#b6b4a8',4,hand,False);paper.shape_key_add(name='Basis');crumple=paper.shape_key_add(name='Crumple');target=[(-11,4),(-1,-1),(12,3),(7,15),(11,25),(-1,22),(-9,27),(-7,14)]
for v,(x,y) in zip(crumple.data,target):v.co.x=x;v.co.y=y
creases=[]
for i in range(3):creases.append(b['line'](room,'v019 note line',[(-16,10+i*8),(15,10+i*8)],'#565e61',4.1,hand,.55))
for f in range(1,49):
 t=smooth((f-16)/9);key(hand,'location',f,(-139+10*t,92+8*t,0));key(elbow,'location',f,(-104+4*t,74+4*t,0));key(headob,'rotation_euler',f,(0,0,.035-.025*t));crumple.value=t;crumple.keyframe_insert(data_path='value',frame=f)
 for ob in creases:key(ob,'scale',f,(1-.65*t,1-.55*t,1))
 start=cam.location.copy() if f==1 else start;key(cam,'location',f,start+Vector((.045,-.07,-.02))*smooth((f-1)/28))
# Selected recorded performances drive the native mouths on the same character rigs.
p=V/'scripts/continue_batch02_v017.py';tree=ast.parse(p.read_text());lipns=dict(b);lipns['O']=O;exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='lips'],type_ignores=[]),str(p),'exec'),lipns)
lipns['lips'](A,[('L13',275),('L16',779),('L17',909),('L18',1005)],True);lipns['lips'](Y,[('L15',719)],True)
# Same authored mix for Blender playback and rendered checkpoint.
seq=s.sequence_editor_create();seq.strips.new_sound('v019 authoritative batch mix',str(O/'mix/mix-premaster.wav'),channel=1,frame_start=1);s.sync_mode='AUDIO_SYNC';s.render.use_sequencer=False
seq=room.sequence_editor_create();ss=seq.strips.new_sound('v019 narrator reaction mix',str(O/'mix/mix-premaster.wav'),channel=1,frame_start=1-855);ss.frame_offset_start=855;ss.frame_final_duration=48;room.sync_mode='AUDIO_SYNC';room.render.use_sequencer=False
# Native poses retained; key all motion in linear timing, exposure keys remain stepped.
for sc in [s,room]:
 for ob in sc.objects:
  if ob in shared:continue
  for fc in curves(ob):
   if fc.data_path in ['location','rotation_euler']:
    for k in fc.keyframe_points:k.interpolation='LINEAR'
q['room']=room;q['phone']=phone
bpy.context.window.scene=s;s.frame_set(490);s.camera=max((m for m in s.timeline_markers if m.camera and m.frame<=490),key=lambda m:m.frame).camera
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL'
bpy.data.libraries.write(str(O/'batch02-v019.blend'),{s,room},fake_user=True,compress=True)
result={'saved':str(O/'batch02-v019.blend'),'contact_height':contact.z,'room':room.name}

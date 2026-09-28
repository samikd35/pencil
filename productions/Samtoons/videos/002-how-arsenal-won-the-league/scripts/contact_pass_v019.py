import bpy,math
from mathutils import Vector
q=bpy.app.driver_namespace['build19'];fns=bpy.app.driver_namespace['finish19'];globals().update({k:q[k] for k in ['s','S','A','R','Y','wall','key','pose','b','smooth','curves','O','n']});bpy.context.window.scene=s
# Bound each shuffle step: no foot travels the whole root displacement in one stride.
max_offset=0
for i,a in enumerate(wall):
 r=a['rest'];x0=(i-4)*1.05;D=(i-4)*(.70-1.05);start=400+i*2
 for f in range(392,1048):
  t=max(0,min(64,f-start));u=t/64;key(a['root'],'location',f,(x0+D*u,-51.7,0));p={k:v.copy() for k,v in r.items()}
  for side,offset in [('L',0),('R',8)]:
   if t<offset:travel=0;lift=0
   elif t>=64:travel=D;lift=0
   else:
    cycle=int((t-offset)//16);st=offset+cycle*16;frac=max(0,min(1,(t-st)/8));old=max(0,(st-8)/64);new=min(1,(st+8)/64);travel=D*(old+(new-old)*smooth(frac));lift=.045*math.sin(math.pi*frac)
   dx=-(travel-D*u);max_offset=max(max_offset,abs(dx));p[side+'ankle'].x+=dx;p[side+'ankle'].y+=lift;p[side+'toe']+=p[side+'ankle']-r[side+'ankle'];p[side+'knee'].x+=dx*.5;p[side+'knee'].y+=lift*.5
  for k,v in p.items():key(a['C'][k],'location',f,v)
assert max_offset<.36
# Correct bend plane: elbow stays below the wrist and shoulder while the phone rises.
phone=q['phone'];r=A['rest'];l1=(r['Relbow']-r['Rshoulder']).length;l2=(r['Rwrist']-r['Relbow']).length;lh=(r['Rfinger']-r['Rwrist']).length
for f in range(988,1048):
 s.frame_set(f);t=smooth((f-990)/9);sh=A['C']['Rshoulder'].location.copy();target=Vector((.47,1.36,0));wr=r['Rwrist'].lerp(target,t);d=wr-sh;wr=sh+d.normalized()*min(d.length,l1+l2-.002);el=b['ik'](sh,wr,l1,l2,Vector((.24,.95,0)));direction=(r['Rfinger']-r['Rwrist']).normalized().lerp(Vector((.20,.98,0)),t).normalized()
 for k,v in [('Relbow',el),('Rwrist',wr),('Rfinger',wr+direction*lh)]:key(A['C'][k],'location',f,v)
 key(phone,'location',f,wr+Vector((.008,.048,0)))
assert el.y<sh.y and el.y<wr.y
# Maintain a grounded ready stance before the short kick preparation.
r=S['rest'];l1=(r['Rknee']-r['Rhip']).length;l2=(r['Rankle']-r['Rknee']).length
for f in range(1,168):
 wind=smooth((f-148)/10);hit=smooth((f-158)/10);down=-.08;pose(S,f,down=down,lean=-.02*wind,ua=(-.04*wind,.09*hit),fa=(0,.06*hit));ank=Vector((.38,.15,0)).lerp(Vector((.25,.24,0)),wind).lerp(Vector((.44,.15,0)),hit);hip=r['Rhip']+Vector((0,down,0));d=ank-hip
 if d.length>=l1+l2-.002:ank=hip+d.normalized()*(l1+l2-.002)
 knee=b['ik'](hip,ank,l1,l2,hip+Vector((.3,-.2,0)))
 for name,v in [('Rknee',knee),('Rankle',ank),('Rtoe',ank+r['Rtoe']-r['Rankle'])]:key(S['C'][name],'location',f,v)
# Frame the note-crumpling above the chair instead of concealing the entire gesture.
hand=fns['hand'];elbow=fns['elbow'];room=q['room'];bpy.context.window.scene=room
for f in range(1,49):
 t=smooth((f-16)/9);key(hand,'location',f,(-139+8*t,242-10*t,0));key(elbow,'location',f,(-112,190-3*t,0))
# Hide coach during the wall overview, preserve his subsequent reply close-up.
for f,v in [(392,0),(778,0),(779,1),(855,1),(856,0),(903,0),(904,1)]:key(A['root'],'scale',f,(v*1.78/1.8,)*3)
for fc in curves(A['root']):
 if fc.data_path=='scale':
  for k in fc.keyframe_points:k.interpolation='CONSTANT'
# Final framing: all nine faces remain visible behind Raya.
for f in range(392,1048):
 s.frame_set(f);loc=R['root'].location.copy();loc.x=.35;key(R['root'],'location',f,loc)
for ob in phone.children:
 if ob.type=='MESH':
  for v in ob.data.vertices:
   if v.co.y>0:v.co.y+=.035
G=q['G']
for f in range(194,270):
 prep=smooth((f-194)/9)*(1-smooth((f-203)/6));u=(f-209)/15;jump=.42*4*u*(1-u) if 0<u<1 else 0;land=-.07*math.sin(math.pi*(f-224)/10) if 224<=f<=234 else 0;key(G['root'],'location',f,(0,49.1,jump));pose(G,f,lean=.08*smooth((f-213)/4)*(1-smooth((f-218)/7)),down=-.075*prep+land,ua=(-.12*prep,.13*prep),fa=(-.08*prep,.08*prep))
for f in range(270,392):
 cheer=smooth((f-274)/5)*(1-smooth((f-295)/8));command=smooth((f-313)/6)*(1-smooth((f-347)/9));b['pose_actor'](A,f,ua=(-.06*cheer,.28*cheer+.58*command),fa=(-.1*cheer,.65*command),hands=(0,.08*command),lean=-.025*command)
assert abs(8*.42/(15/24)**2-8.6016)<1e-8
# A readable corner signal with source-specific sleeve weights; keep the torso out of arm influence.
skin=S['skin'];names={g.index:g.name for g in skin.vertex_groups}
for v in skin.data.vertices:
 ws={names[g.group]:g.weight for g in v.groups}
 if v.co.y>.5:
  t=smooth((-v.co.x-.24)/.065);moved=0
  for k in ['Lupperarm','Lforearm','Lhand']:
   w=ws.get(k,0);skin.vertex_groups[k].add([v.index],w*t,'REPLACE');moved+=w*(1-t)
  if moved:skin.vertex_groups['torso'].add([v.index],ws.get('torso',0)+moved,'REPLACE')
r=S['rest']
for f in range(1,148):
 s.frame_set(f);t=smooth((f-31)/8)*(1-smooth((f-76)/10));sh=S['C']['Lshoulder'].location.copy();el=sh+n['rotate'](r['Lelbow']-r['Lshoulder'],-1.4*t);wr=el+n['rotate'](r['Lwrist']-r['Lelbow'],-1.55*t);fi=wr+n['rotate'](r['Lfinger']-r['Lwrist'],-1.55*t)
 for name,v in [('Lelbow',el),('Lwrist',wr),('Lfinger',fi)]:key(S['C'][name],'location',f,v)
K=q['K'];m=K['skin'].data.materials[0];ns=m.node_tree.nodes;ls=m.node_tree.links;hs=next(x for x in ns if x.type=='SEPARATE_COLOR' and x.mode=='HSV');mix=next(x for x in ns if x.type=='MIX_RGB');ramp=next(x for x in ns if x.type=='VALTORGB');guard=ns.new('ShaderNodeMath');guard.operation='GREATER_THAN';ls.new(hs.outputs[1],guard.inputs[0]);guard.inputs[1].default_value=.4;mul=ns.new('ShaderNodeMath');mul.operation='MULTIPLY';ls.new(ramp.outputs[0],mul.inputs[0]);ls.new(guard.outputs[0],mul.inputs[1]);ls.new(mul.outputs[0],mix.inputs[0]);combine=ns.new('ShaderNodeCombineColor');combine.mode='HSV';combine.inputs[0].default_value=.62;combine.inputs[1].default_value=.75;ls.new(hs.outputs[2],combine.inputs[2]);ls.new(combine.outputs[0],mix.inputs[2])
for sc,frames in [(s,[1,155,168,430,1008]),(room,[26])]:
 bpy.context.window.scene=sc
 for f in frames:
  sc.frame_set(f);sc.camera=max((m for m in sc.timeline_markers if m.camera and m.frame<=f),key=lambda m:m.frame).camera;sc.render.filepath=str(O/'checks'/f'contact-{sc.name}-{f}.png');bpy.ops.render.render(write_still=True)
bpy.data.libraries.write(str(O/'batch02-v019.blend'),{s,room},fake_user=True,compress=True)
result={'max_shuffle_root_foot_offset_m':max_offset,'phone_elbow_below_shoulder':True}

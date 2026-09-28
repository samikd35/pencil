"""Visible first-batch rebuild: coherent illustrated skin on fitted native bones.

Reuse Video 1's continuous UV skin, semantic binding, and target-driven bones.
Call rebuild(name), inspect(), then save() in the interactive Blender session.
"""
import bpy, math, json, sys
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import delaunay_2d_cdt
V=Path(__file__).resolve().parents[1]
O=V/'artifacts/batch01-v012';O.mkdir(exist_ok=True)
n=bpy.app.driver_namespace['samtoons_batch01'];b=n['b']
SOURCE=V/'assets/rig-art-v012/arteta-gyokeres.png'
DESIGNS={
 'gyokeres':dict(center=424,floor=998,top=18,hip=567,neck=(425,220),head=(418,106),
  L=[(293,278),(260,422),(205,548),(190,603),(367,569),(342,704),(320,922),(265,979)],
  R=[(555,278),(608,423),(650,548),(667,605),(489,569),(521,704),(557,922),(617,979)],
  eyes=[(428,118,13,8),(465,107,9,9)],mouth=(455,159,18),skin='#ffc38c',
  body_edge=[(220,42),(280,103),(350,104),(420,88),(470,94),(515,101)],
  outline=[(376,197),(375,166),(359,153),(350,140),(349,127),(345,117),(334,101),(329,83),(331,68),(341,51),(352,42),(375,33),(387,28),(420,25),(443,18),(460,22),(471,33),(473,50),(467,63),(473,78),(477,98),(478,120),(482,137),(481,158),(483,177),(476,191),(464,199),(462,205),(504,214),(542,225),(558,234),(571,251),(581,277),(586,297),(595,320),(598,338),(610,352),(606,363),(621,397),(635,417),(645,451),(650,480),(660,513),(666,525),(671,546),(684,573),(689,597),(684,616),(676,632),(669,630),(672,613),(669,603),(671,616),(667,628),(661,628),(665,605),(660,587),(655,573),(656,591),(651,598),(644,595),(642,579),(638,564),(634,550),(636,533),(637,523),(620,497),(600,473),(583,448),(577,428),(571,413),(568,396),(552,375),(543,375),(532,354),(527,372),(521,409),(520,426),(524,439),(519,455),(526,477),(532,503),(526,506),(550,584),(568,650),(552,657),(552,683),(559,705),(553,720),(570,761),(575,793),(574,844),(581,891),(580,914),(590,932),(625,952),(650,969),(663,982),(663,993),(645,998),(642,1003),(635,1003),(631,997),(609,997),(605,1003),(596,1003),(592,996),(574,992),(569,999),(561,997),(558,989),(544,984),(537,969),(535,952),(537,933),(532,917),(531,894),(508,843),(491,808),(484,779),(484,751),(486,738),(480,719),(476,700),(470,663),(445,660),(428,581),(423,574),(412,651),(393,656),(391,677),(381,704),(379,723),(375,741),(376,779),(371,811),(352,849),(343,891),(340,922),(346,940),(348,962),(342,976),(327,981),(325,989),(317,989),(314,982),(286,990),(282,998),(273,998),(270,992),(244,995),(238,1001),(230,1000),(228,993),(218,986),(219,978),(229,963),(251,948),(277,932),(292,920),(294,891),(287,844),(286,799),(290,764),(301,731),(301,713),(309,692),(309,659),(291,650),(309,578),(324,509),(323,506),(329,469),(335,456),(329,444),(330,424),(324,391),(319,370),(310,379),(304,398),(289,421),(282,453),(265,479),(246,505),(222,534),(224,550),(219,573),(217,593),(211,598),(206,593),(205,573),(202,588),(202,605),(202,617),(197,625),(193,622),(195,603),(195,594),(190,610),(192,624),(187,630),(181,623),(173,614),(169,598),(170,576),(175,562),(184,543),(191,528),(194,512),(201,490),(210,451),(218,423),(231,399),(244,381),(252,358),(248,354),(256,329),(261,307),(263,282),(272,254),(286,237),(308,227),(343,213)],
 ),
 'arteta':dict(center=1111,floor=994,top=86,hip=594,neck=(1100,281),head=(1095,175),
  L=[(1007,316),(963,428),(906,542),(883,602),(1064,594),(1038,754),(997,928),(949,977)],
  R=[(1217,316),(1246,430),(1306,543),(1334,603),(1167,594),(1192,755),(1214,931),(1281,977)],
  eyes=[(1111,168,13,9),(1143,160,8,8)],mouth=(1134,205,22),skin='#ffbd83',
  body_edge=[(283,40),(325,91),(400,91),(470,91),(530,94),(557,91)],
  outline=[(1066,264),(1063,226),(1042,217),(1036,206),(1035,192),(1027,179),(1018,167),(1015,150),(1021,132),(1035,114),(1053,104),(1081,95),(1109,90),(1123,85),(1136,90),(1145,104),(1144,123),(1149,138),(1152,158),(1156,172),(1158,190),(1163,207),(1162,222),(1155,234),(1136,242),(1137,263),(1170,273),(1203,282),(1221,291),(1234,308),(1242,336),(1251,359),(1258,381),(1256,396),(1268,412),(1272,428),(1284,444),(1296,459),(1307,486),(1314,514),(1323,533),(1332,545),(1342,565),(1351,584),(1354,606),(1349,626),(1342,637),(1336,635),(1341,613),(1337,605),(1336,620),(1332,634),(1325,632),(1330,610),(1327,589),(1320,579),(1323,598),(1319,612),(1311,612),(1308,599),(1302,578),(1299,562),(1302,546),(1288,528),(1269,510),(1258,495),(1248,476),(1236,466),(1227,448),(1221,429),(1210,408),(1202,391),(1199,424),(1200,453),(1204,479),(1207,504),(1202,518),(1207,542),(1203,548),(1210,585),(1214,650),(1219,706),(1227,759),(1224,803),(1231,853),(1232,886),(1240,910),(1238,921),(1244,934),(1262,944),(1286,954),(1311,965),(1327,977),(1327,987),(1315,993),(1291,993),(1260,988),(1225,981),(1190,979),(1178,974),(1179,955),(1185,933),(1189,922),(1180,914),(1173,871),(1163,833),(1150,793),(1149,757),(1142,734),(1131,706),(1121,671),(1113,636),(1105,655),(1097,691),(1081,730),(1070,752),(1068,787),(1056,819),(1043,858),(1035,888),(1027,917),(1018,919),(1022,932),(1030,952),(1026,970),(1016,979),(986,986),(956,993),(932,994),(913,989),(904,982),(906,972),(920,959),(943,942),(966,925),(969,913),(973,881),(978,841),(984,801),(995,759),(1000,724),(1005,685),(1011,648),(1013,610),(1016,566),(1021,542),(1014,537),(1017,513),(1013,501),(1019,481),(1020,452),(1016,421),(1014,405),(1002,425),(995,444),(980,461),(970,481),(957,499),(944,512),(931,529),(915,547),(918,562),(916,578),(909,593),(908,607),(903,613),(897,611),(897,592),(892,601),(892,620),(888,637),(881,636),(883,620),(880,611),(880,629),(876,637),(870,632),(864,617),(862,602),(864,580),(873,559),(882,542),(890,518),(899,497),(906,488),(913,463),(923,446),(922,433),(929,414),(939,394),(947,370),(957,346),(969,319),(985,300),(1004,289),(1035,278)],
 )}

def fcurves(ob):
 return [fc for l in ob.animation_data.action.layers for st in l.strips for bag in st.channelbags for fc in bag.fcurves] if ob.animation_data and ob.animation_data.action else []

def inside(x,y,poly):
 c=False
 for (ax,ay),(bx,by) in zip(poly,poly[1:]+poly[:1]):
  if (ay>y)!=(by>y) and x<(bx-ax)*(y-ay)/(by-ay)+ax:c=not c
 return c

def distance(p,a,b):
 d=b-a;t=max(0,min(1,(p-a).dot(d)/d.length_squared));return (p-a-t*d).length

def artwork_material():
 old=bpy.data.materials.get('B12 coherent source artwork')
 if old:return old
 im=bpy.data.images.load(str(SOURCE),check_existing=True);im.pack()
 m=bpy.data.materials.new('B12 coherent source artwork');m.use_nodes=True;nodes=m.node_tree.nodes;nodes.clear()
 tex=nodes.new('ShaderNodeTexImage');tex.image=im;tex.interpolation='Linear'
 em=nodes.new('ShaderNodeEmission');out=nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(tex.outputs['Color'],em.inputs[0]);m.node_tree.links.new(em.outputs[0],out.inputs[0]);return m

def rebuild(name):
 assert not bpy.app.background,'Author the actual visible scene'
 a=n['ACTORS'][name];s=a['scene'];n['use'](s,a['col']);s.frame_set(1);C=a['C'];root=a['root'];cfg=DESIGNS[a['kind']];p=a['prefix'];mirror=name=='unveiling Arteta';u=604/(cfg['floor']-cfg['top']);sign=-1 if mirror else 1
 assert not bpy.data.objects.get(p+'v012 illustrated skin'),'Preserve existing revision'
 # Hide old approximation. Keep props and animation controls, not duplicate surfaces.
 for ob in a['col'].objects:
  if ob.name.startswith(p) and ob.type in ['MESH','CURVE','FONT']:ob.hide_render=ob.hide_viewport=True
 def xy(pt):return Vector((sign*(pt[0]-cfg['center'])*u,(cfg['floor']-pt[1])*u,0))
 rest={'pelvis':xy((cfg['center'],cfg['hip'])),'neck':xy(cfg['neck']),'head':xy(cfg['head'])}
 joints={}
 for side in ['L','R']:
  raw=cfg[('R' if side=='L' else 'L') if mirror else side]
  for label,pt in zip(['shoulder','elbow','wrist','finger','hip','knee','ankle','toe'],raw):rest[side+' '+label]=xy(pt)
 hip=rest['pelvis'];delta=hip.y-245
 if not fcurves(C['pelvis']):C['pelvis'].location.y+=delta
 for fc in fcurves(C['pelvis']):
  if fc.data_path=='location' and fc.array_index==1:
   for k in fc.keyframe_points:k.co.y+=delta;k.handle_left.y+=delta;k.handle_right.y+=delta
 C['head'].location=(*(rest['neck']-hip).xy,18);C['head'].scale=(1,1,1)
 lengths={}
 for side in ['L','R']:
  upper=(rest[side+' elbow']-rest[side+' shoulder']).length;lower=(rest[side+' wrist']-rest[side+' elbow']).length
  thigh=(rest[side+' knee']-rest[side+' hip']).length;shin=(rest[side+' ankle']-rest[side+' knee']).length;lengths[side]=(thigh,shin)
  C[side+' upper arm'].location=(*(rest[side+' shoulder']-hip).xy,0)
  C[side+' forearm'].location=(0,-upper,2);C[side+' hand'].location=(0,-lower,3)
  C[side+' thigh'].location=(*(rest[side+' hip']-hip).xy,0);C[side+' shin'].location=(0,-thigh,.5);C[side+' boot'].location=(0,-shin,2)
 hip_samples=[]
 for f in range(1,s.frame_end+1):
  s.frame_set(f);pos=C['pelvis'].location.copy();limits=[]
  for side in ['L','R']:
   old=a.get('foot_samples',{}).get(f,{}).get(side,(-55 if side=='L' else 55,22));target=rest[side+' ankle'].xy+Vector((old[0]-(-55 if side=='L' else 55),old[1]-22))
   dx=target.x-pos.x-C[side+' thigh'].location.x;reach=sum(lengths[side])-2
   assert abs(dx)<reach,(name,f,'stride exceeds fitted leg reach')
   limits.append(target.y+math.sqrt(reach*reach-dx*dx)-C[side+' thigh'].location.y)
  # Lower the pelvis smoothly for the new limb proportions; never stretch a leg to reach a planted foot.
  cap=min(limits);pos.y=min(pos.y,cap)-3*math.log1p(math.exp(-abs(pos.y-cap)/3));hip_samples.append((f,tuple(pos)))
 n['key'](C['pelvis'],'location',hip_samples,'LINEAR')
 for f in range(1,s.frame_end+1):
  s.frame_set(f)
  for side in ['L','R']:
   old=a.get('foot_samples',{}).get(f,{}).get(side,(-55 if side=='L' else 55,22));target=rest[side+' ankle'].xy+Vector((old[0]-(-55 if side=='L' else 55),old[1]-22))
   top=C['pelvis'].location.xy+C[side+' thigh'].location.xy;knee=Vector(n['two_bone_joint'](tuple(top),tuple(target),lengths[side],(-200 if side=='L' else 200,130)))
   aa=math.atan2((knee-top).x,-(knee-top).y);bb=math.atan2((target-knee).x,-(target-knee).y)
   for key,value in [(side+' thigh',aa),(side+' shin',bb-aa),(side+' boot',-bb)]:C[key].rotation_euler.z=value;C[key].keyframe_insert(data_path='rotation_euler',frame=f)
 s.frame_set(1);bpy.context.view_layer.update()
 targets={'pelvis':C['pelvis'],'neck':C['head']}
 def endpoint(key,parent,vec):
  ob=n['ctrl'](p+'v012 target '+key,tuple(vec),parent);targets[key]=ob;return ob
 endpoint('head',C['head'],rest['head']-rest['neck'])
 for side in ['L','R']:
  for label,key in [('shoulder','upper arm'),('elbow','forearm'),('wrist','hand'),('hip','thigh'),('knee','shin'),('ankle','boot')]:targets[side+' '+label]=C[side+' '+key]
  # Hands point down in their local rest; toes retain each source boot's silhouette.
  endpoint(side+' finger',C[side+' hand'],Vector((0,-(rest[side+' finger']-rest[side+' wrist']).length,0)))
  endpoint(side+' toe',C[side+' boot'],rest[side+' toe']-rest[side+' ankle'])
 bones={'torso':('pelvis','neck'),'head':('neck','head')}
 for side in ['L','R']:
  for label,aa,bb in [('upper arm','shoulder','elbow'),('forearm','elbow','wrist'),('hand','wrist','finger'),('thigh','hip','knee'),('shin','knee','ankle'),('boot','ankle','toe')]:bones[side+' '+label]=(side+' '+aa,side+' '+bb)
 data=bpy.data.armatures.new(p+'v012 fitted skeleton');arm=bpy.data.objects.new(data.name,data);a['col'].objects.link(arm);arm.parent=root;arm.show_in_front=True
 bpy.ops.object.select_all(action='DESELECT');arm.select_set(True);bpy.context.view_layer.objects.active=arm;bpy.ops.object.mode_set(mode='EDIT')
 for key,(aa,bb) in bones.items():eb=data.edit_bones.new(key);eb.head=rest[aa];eb.tail=rest[bb]
 bpy.ops.object.mode_set(mode='OBJECT')
 for key,(aa,bb) in bones.items():
  pb=arm.pose.bones[key];co=pb.constraints.new('COPY_LOCATION');co.target=targets[aa];co=pb.constraints.new('STRETCH_TO');co.target=targets[bb];co.rest_length=(rest[bb]-rest[aa]).length;co.volume='NO_VOLUME';co.bulge=0
 outline=cfg['outline'];pixels=list(outline)
 for y in range(min(y for x,y in outline)+3,max(y for x,y in outline),5):
  for x in range(min(x for x,y in outline)+3,max(x for x,y in outline),5):
   if inside(x,y,outline):pixels.append((x,y))
 coords,edges,faces,*_=delaunay_2d_cdt([Vector(v) for v in pixels],[],[list(range(len(outline)))],1,.001,False)
 pixels=[tuple(v) for v in coords];verts=[xy(v) for v in pixels]
 me=bpy.data.meshes.new(p+'v012 continuous source mesh');me.from_pydata(verts,[],faces);me.materials.append(artwork_material());uv=me.uv_layers.new()
 for loop in me.loops:x,y=pixels[loop.vertex_index];uv.data[loop.index].uv=(x/1536,1-y/1024)
 skin=bpy.data.objects.new(p+'v012 illustrated skin',me);a['col'].objects.link(skin);skin.parent=root
 groups={key:skin.vertex_groups.new(name=key) for key in bones}
 def nearest(pt,names):
  ds=[(distance(pt,rest[bones[key][0]],rest[bones[key][1]]),key) for key in names];ds=sorted(ds)[:2];vv=[math.exp(-(d*d-ds[0][0]**2)/(15*u)**2) for d,key in ds];total=sum(vv);return {key:value/total for (_,key),value in zip(ds,vv)}
 for i,(pt,(px,py)) in enumerate(zip(verts,pixels)):
  side='L' if pt.x<0 else 'R'
  if py>940:w={side+' boot':1}
  elif py<cfg['neck'][1]-28:w={'head':1}
  elif py<cfg['neck'][1]+14:
   t=max(0,min(1,(cfg['neck'][1]+14-py)/42));w={'head':t,'torso':1-t}
  elif py<cfg['hip']-10:
   edge=cfg['body_edge'];width=edge[-1][1]
   for (y0,x0),(y1,x1) in zip(edge,edge[1:]):
    if y0<=py<y1:width=x0+(x1-x0)*(py-y0)/(y1-y0);break
   armweight=max(0,min(1,(abs(px-cfg['center'])-width-20)/22))
   w={key:value*armweight for key,value in nearest(pt,[side+' upper arm',side+' forearm',side+' hand']).items()};w['torso']=1-armweight
  elif abs(px-cfg['center'])>155 and py<cfg['hip']+70:w=nearest(pt,[side+' forearm',side+' hand'])
  else:
   w=nearest(pt,[side+' thigh',side+' shin',side+' boot']);torso=max(0,min(1,(cfg['hip']+38-py)/55));w={key:value*(1-torso) for key,value in w.items()};w['torso']=torso
  assert abs(sum(w.values())-1)<1e-6
  for key,value in w.items():
   if value>1e-7:groups[key].add([i],value,'REPLACE')
 mod=skin.modifiers.new('Fitted bones deform coherent artwork','ARMATURE');mod.object=arm;mod.use_deform_preserve_volume=False
 # Native shape keys animate the actual drawn eyelids, keeping the source likeness.
 skin.shape_key_add(name='Basis');blink=skin.shape_key_add(name='Blink')
 for i,(px,py) in enumerate(pixels):
  for ex,ey,rx,ry in cfg['eyes']:
   dx=abs(px-ex)/(rx+5);dy=abs(py-ey)/(ry+5)
   if dx<1.35 and dy<1.35:
    strength=min(1,max(0,(1.35-dx)/.35))*min(1,max(0,(1.35-dy)/.35));blink.data[i].co.y+=(py-ey)*u*.94*strength
 for f in [1,s.frame_end]:blink.value=0;blink.keyframe_insert(data_path='value',frame=f)
 for f in [35,117,203,323]:
  if f+5<s.frame_end:
   for t,val in [(f,0),(f+2,1),(f+5,0)]:blink.value=val;blink.keyframe_insert(data_path='value',frame=t)
 # Separate native mouths use the retained dialogue schedule; rest uses source lips.
 mx,my,mw=cfg['mouth'];mouth=C['mouth'];mp=xy((mx,my))-rest['neck'];mouth.location=(mp.x,mp.y,3);mouth.scale=(sign,1,1)
 for label,g in a['n']['FAC']['mouth shapes'].items():
  for ob in list(g.children_recursive):
   if ob.type in ['MESH','CURVE']:bpy.data.objects.remove(ob,do_unlink=True)
  if label=='rest':continue
  width=mw*u;hh={'MBP':1,'A':9,'E':5,'O':8,'U':5,'FV':3,'L':7}[label]*u;ww=width*({'O':.58,'U':.45}.get(label,1))
  # A small matching lip bed covers the closed source line only while speaking.
  n['ellipse'](p+'v012 '+label+' lip bed',0,-1,width+1.5,4*u,cfg['skin'],0,g)
  if label=='MBP':n['line'](p+'v012 MBP',[(-width,0),(0,-1),(width,0)],'#653c28',.2,.7,g)
  else:
   n['poly'](p+'v012 '+label+' mouth',[(-ww,0),(-ww*.6,2*u),(ww*.65,2*u),(ww,0),(ww*.6,-hh),(0,-hh-1),(-ww*.65,-hh)],'#42261f',.3,g,True,.7,True)
   if label not in ['O','U']:n['poly'](p+'v012 '+label+' teeth',[(-ww*.8,0),(ww*.8,0),(ww*.65,-2*u),(-ww*.65,-2*u)],'#fff5de',.5,g,False)
 for side in ['L','R']:
  C[side+' eye'].scale=(1,1,1)
 a['v012']={'skin':skin,'armature':arm,'rest':rest,'targets':targets,'config':cfg,'unit':u,'mirror':mirror,'lengths':lengths}
 skin['Construction']='Video 1 illustrated mesh + fitted target-driven bones; head, neck, garment and limbs share the same source. Native eyelid shape key and mouth geometry.'
 skin['Source']=str(SOURCE.relative_to(V));skin['Scope']='Current three-quarter gestures and steps; not an arbitrary head turn or extreme-action proof.'
 n['room']['show'](s);s.frame_set(315 if s.frame_end==432 else 226)
 return {'actor':name,'vertices':len(verts),'triangles':len(faces),'source':skin['Source']}

def faces():
 rows={'opening Arteta':[(67,127,'E U MBP FV E E A MBP L A MBP'),(213,239,'A O E E A MBP'),(346,386,'E MBP E A E A MBP O')],'unveiling Gyokeres':[(301,339,'E A MBP A E')],'unveiling Arteta':[(351,376,'U E MBP A O E')]}
 for name,phrases in rows.items():n['mouths'](n['ACTORS'][name],phrases)
 return {'mouth_schedules':list(rows)}

def contacts():
 a=n['ACTORS']['opening Arteta'];s=a['scene'];C=a['C'];n['use'](s);s.frame_set(337)
 start=[C[k].rotation_euler.z for k in ['R upper arm','R forearm','R hand']]
 target=[math.radians(v) for v in [20,158,47]]
 phone=n['PROPS']['phone'];phone.location=(0,-31,15)
 for f in range(338,410):
  s.frame_set(f);t=max(0,min(1,(f-338)/12));t=t*t*(3-2*t)
  if f>393:t=max(0,1-(f-393)/16)
  for ob,aa,bb in zip([C[k] for k in ['R upper arm','R forearm','R hand']],start,target):
   ob.rotation_euler.z=aa+(bb-aa)*t;ob.keyframe_insert(data_path='rotation_euler',frame=f)
  bpy.context.view_layer.update();phone.rotation_euler.z=-C['R hand'].matrix_world.to_euler().z;phone.keyframe_insert(data_path='rotation_euler',frame=f)
 # Bag contact follows the rebuilt wrist/palm until release; the contact frame stays fixed afterward.
 a=n['ACTORS']['unveiling Gyokeres'];s=a['scene'];n['use'](s);bag=n['PROPS']['bag'];s.frame_set(26);bpy.context.view_layer.update()
 grip=a['C']['L hand'].matrix_world@Vector((0,-24,2));height=grip.y+2.9
 handle=bpy.data.objects.get('Bag handle')
 if handle and handle.type=='CURVE':
  sp=handle.data.splines[0]
  for point,xy in zip(sp.points,[(-.25,.9),(-.19,height),(0,height+.025),(.19,height),(.25,.9)]):point.co.x,point.co.y=xy
 for f in range(1,433):
  s.frame_set(f);bpy.context.view_layer.update();now=a['C']['L hand'].matrix_world@Vector((0,-24,2))
  loc=(now.x,now.y-height,1.2) if f<=26 else (grip.x,-2.9,1.2)
  bag.location=loc;bag.keyframe_insert(data_path='location',frame=f)
 return {'contacts':'phone arm refitted to coherent source proportions; bag release stays frame 26'}

def save():
 for key,s in n['SCENES'].items():s.name='S002_B01_v012_'+key
 rows=json.loads((V/'artifacts/batch01-v010/edit.json').read_text())
 for row in rows:row['scene']=row['scene'].replace('v010','v012')
 (O/'edit.json').write_text(json.dumps(rows,indent=2)+'\n')
 n['room']['show'](n['SCENES']['unveiling']);n['SCENES']['unveiling'].frame_set(315)
 bpy.ops.wm.save_as_mainfile(filepath=str(O/'batch01-v012.blend'))
 return {'file':bpy.data.filepath,'frames':1021}

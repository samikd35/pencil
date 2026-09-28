"""Keep connected pose surfaces; register the complete illustration to them.
The mesh controls the drawing. Source pixels do not define a second skeleton.
"""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/batch01-v014';O.mkdir(exist_ok=True)
n=bpy.app.driver_namespace['samtoons_batch01'];b=n['b']
SOURCE=V/'assets/rig-art-v012/arteta-gyokeres.png'

def material():
 m=bpy.data.materials.get('B14 complete character drawing')
 if m:return m
 im=bpy.data.images.load(str(SOURCE),check_existing=True);im.pack();m=bpy.data.materials.new('B14 complete character drawing');m.use_nodes=True;nodes=m.node_tree.nodes;nodes.clear();t=nodes.new('ShaderNodeTexImage');t.image=im;t.interpolation='Linear';e=nodes.new('ShaderNodeEmission');o=nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(t.outputs['Color'],e.inputs[0]);m.node_tree.links.new(e.outputs[0],o.inputs[0]);return m

def interpolate(keys,t):
 for (a,x),(bb,y) in zip(keys,keys[1:]):
  if t<=bb:
   u=max(0,(t-a)/(bb-a));return tuple(v+(w-v)*u for v,w in zip(x,y))
 return keys[-1][1]

def set_uv(ob,points):
 assert len(points)==len(ob.data.vertices),(ob.name,len(points),len(ob.data.vertices))
 ob.data.materials.clear();ob.data.materials.append(material());uv=ob.data.uv_layers.active or ob.data.uv_layers.new(name='Coherent source drawing')
 for p in ob.data.polygons:p.material_index=0
 for l in ob.data.loops:x,y=points[l.vertex_index];uv.data[l.index].uv=(x/1536,1-y/1024)
 ob['appearance_source']=str(SOURCE);ob['construction']='Existing connected geometry and deformation retained; source art registered to semantic garment edges.'

ART={'core':[(1218,293),(1197,396),(1200,427),(1201,479),(1200,536),(1196,548),(1111,552),(1024,543),(1019,532),(1021,478),(1018,426),(1018,399),(987,300),(1067,265),(1100,287),(1136,265)],
'Rout':[(0,(1218,293)),(7,(1235,327)),(16,(1270,428)),(26,(1303,484)),(32,(1311,518))],
'Rin':[(0,(1197,396)),(7,(1211,414)),(16,(1229,447)),(26,(1269,507)),(32,(1287,528))],
'Lout':[(0,(987,300)),(7,(961,344)),(16,(928,428)),(26,(909,468)),(32,(893,495))],
'Lin':[(0,(1018,399)),(7,(1005,417)),(16,(984,451)),(26,(963,483)),(32,(944,507))]}
GY={'core':[(558,233),(530,360),(521,399),(523,445),(529,490),(530,505),(423,519),(325,506),(329,487),(332,445),(327,399),(312,375),(286,239),(377,207),(421,242),(463,207)],
'Rout':[(0,(558,233)),(7,(581,294)),(8,(589,335)),(16,(632,420)),(26,(650,493)),(32,(661,532))],
'Rin':[(0,(530,360)),(7,(543,373)),(8,(572,363)),(16,(580,440)),(26,(613,491)),(32,(637,538))],
'Lout':[(0,(286,239)),(7,(263,296)),(8,(253,335)),(16,(219,424)),(26,(201,491)),(32,(190,529))],
'Lin':[(0,(312,375)),(7,(317,366)),(8,(298,375)),(16,(279,446)),(26,(241,504)),(32,(218,538))]}

def upper(name):
 a=n['ACTORS'][name];n['use'](a['scene'],a['col']);p=a['prefix'];cfg=ART if a['kind']=='arteta' else GY
 points=list(cfg['core'])
 for side in ['R','L']:
  for j in range(1,33):points.extend([interpolate(cfg[side+'out'],j),interpolate(cfg[side+'in'],j)])
 ob=bpy.data.objects[p+'connected upper body'];set_uv(ob,points)
 # Remove only superseded surface decoration; controls, hands and silhouettes survive.
 for o in a['col'].objects:
  label=o.name[len(p):]
  if o.type not in ['MESH','CURVE','FONT']:continue
  if any(label.startswith(t) for t in ['jersey','shirt ','collar','jumper ','neckline','v011 collar','L sleeve shade','R sleeve shade','finish jumper','finish shirt','finish sponsor','finish red collar','finish white collar','finish L shoulder','finish R shoulder','finish L sleeve','finish R sleeve','finish L cuff','finish R cuff']):o.hide_render=o.hide_viewport=True
 # Match exposed skin everywhere, retaining finger articulation.
 skin='#ffc38b' if a['kind']=='gyokeres' else '#ffc28a'
 for o in a['col'].objects:
  if o.type in ['MESH','CURVE'] and any(o==c or o in c.children_recursive for c in [a['C']['L hand'],a['C']['R hand']]):
   for i,m in enumerate(o.data.materials):
    if m and any(t in m.name.lower() for t in ['efb082','f2bd91']):o.data.materials[i]=b['mat'](skin)
 return {'actor':name,'unchanged_connected_vertices':len(points),'illustration':str(SOURCE)}

def preview(group,frame,label):
 s=n['SCENES'][group];n['use'](s);n['room']['show'](s);s.frame_set(frame);s.camera=max((m for m in s.timeline_markers if m.frame<=frame and m.camera),key=lambda m:m.frame).camera
 s.render.filepath=str(O/label);s.render.use_sequencer=False;bpy.ops.render.render(write_still=True);return str(O/label)

def face(name):
 from mathutils.geometry import delaunay_2d_cdt
 a=n['ACTORS'][name];n['use'](a['scene'],a['col']);C=a['C'];h=C['head'];p=a['prefix'];art=a['kind']=='arteta'
 source=json.loads((V/'artifacts/batch01-v013/source-heads.json').read_text())[a['kind']];cfg=source['config'];outline=cfg['outline'];end=outline.index((1137,263)) if (1137,263) in outline else None
 # Contour from the entire drawing includes the original neck, jaw and hair.
 if art:
  end=outline.index([1137,263]);outline=outline[:end+1]+[[1132,278],[1110,285],[1086,283],[1067,274]];origin=(1100,259);scale=.9
 else:
  end=outline.index([462,205]);outline=outline[:end+1]+[[459,217],[445,229],[423,236],[398,228],[381,214]];origin=(425,201);scale=.9
 def inside(pt,poly):
  x,y=pt;c=False
  for (ax,ay),(bx,by) in zip(poly,poly[1:]+poly[:1]):
   if (ay>y)!=(by>y) and x<(bx-ax)*(y-ay)/(by-ay)+ax:c=not c
  return c
 pixels=list(outline)
 for yy in range(min(y for x,y in outline)+1,max(y for x,y in outline),4):
  for xx in range(min(x for x,y in outline)+1,max(x for x,y in outline),4):
   if inside((xx,yy),outline):pixels.append((xx,yy))
 coords,edges,faces,*_=delaunay_2d_cdt([Vector(x) for x in pixels],[],[list(range(len(outline)))],1,.001,False);pixels=[tuple(v) for v in coords]
 for ob in list(h.children_recursive):
  if ob.type in ['MESH','CURVE','FONT']:bpy.data.objects.remove(ob,do_unlink=True)
 def xy(pt):return ((pt[0]-origin[0])*scale,(origin[1]-pt[1])*scale)
 me=bpy.data.meshes.new(p+'v014 source head and neck');me.from_pydata([(*xy(pt),4) for pt in pixels],[],faces);ob=bpy.data.objects.new(me.name,me);a['col'].objects.link(ob);ob.parent=h;set_uv(ob,pixels)
 for old in a['col'].objects:
  if 'connected neck' in old.name or old.name in [p+'neck',p+'neck shade']:old.hide_render=old.hide_viewport=True
 # The head/neck footprint overlaps the existing collar; same palette and source finish.
 for label in ['v011 collar edge','v011 collar fabric']:
  old=bpy.data.objects.get(p+label)
  if old:old.hide_render=old.hide_viewport=False
 # The undisturbed source eyes remain visible; native eyelids cover them only during blinks.
 eyes=[]
 for side,(cx,cy,rx,ry) in zip(['L','R'],cfg['eyes']):
  e=C[side+' eye'];e.animation_data_clear();e.location=(*xy((cx,cy)),10);e.scale=(1,1,1)
  rx*=scale;ry*=scale
  pts=[(-rx-2,ry+4),(rx+2,ry+4),(rx+2,ry+2),(-rx-2,ry+2)]
  lid=n['poly'](p+'v014 '+side+' eyelid',pts,cfg['skin'],0,e,False);lid.shape_key_add(name='Open');closed=lid.shape_key_add(name='Closed');closed.value=0
  for idx in [2,3]:closed.data[idx].co.y=-ry-1
  eyes.append(closed)
 # Native aperture is confined to the source lips; no large oval face patch.
 mouth=cfg['mouth'];C['mouth'].location=(*xy(mouth[:2]),16);C['mouth'].scale=(.9,.9,1);groups=a['n']['FAC']['mouth shapes'];w=mouth[2]*.6
 for label,g in groups.items():
  g.location=(0,0,0);g.scale=(1,1,1)
  if label=='rest':continue
  if label=='MBP':n['line'](p+'v014 closed lips',[(-w,0),(0,-.5),(w,0)],'#6b4733',0,.8,g,True)
  else:
   hh={'A':8,'E':5,'O':8,'U':5,'FV':3,'L':6}[label];ww=w*({'O':.55,'U':.42}.get(label,1))
   n['poly'](p+'v014 '+label+' aperture',[(-ww,0),(-ww*.6,2),(0,2.5),(ww*.8,1),(ww,0),(ww*.7,-hh*.7),(0,-hh),(-ww*.7,-hh*.75)],'#412722',0,g,True,.65,True)
   if label not in ['O','U']:n['poly'](p+'v014 '+label+' teeth',[(-ww*.7,.6),(0,1.4),(ww*.7,.6),(ww*.6,-1.5),(0,-2),(-ww*.6,-1.5)],'#fff3df',.2,g,False,soft=True)
   if label in ['A','L']:n['poly'](p+'v014 '+label+' tongue',[(-ww*.4,-hh*.8),(0,-hh*.67),(ww*.4,-hh*.8),(0,-hh*.94)],'#b96c63',.3,g,False,soft=True)
  for child in g.children_recursive:
   if child.type in ['MESH','CURVE']:child.hide_render=child.hide_viewport=True
 a['face14']={'eyes':eyes};return {'actor':name,'source_head_and_neck':ob.name,'same_source_as_body':True}

def trousers(name):
 a=n['ACTORS'][name];p=a['prefix'];assert a['kind']=='arteta'
 bounds={'L':([(0,(1106,582)),(5,(1105,654)),(16,(1067,754)),(24,(1044,843)),(32,(1024,913))],[(0,(1016,582)),(5,(1015,649)),(16,(998,754)),(24,(982,838)),(32,(974,909))]),'R':([(0,(1210,582)),(5,(1213,650)),(16,(1223,757)),(24,(1227,847)),(32,(1235,913))],[(0,(1116,582)),(5,(1117,650)),(16,(1152,757)),(24,(1169,845)),(32,(1184,914))])}
 for side,(one,two) in bounds.items():
  points=[]
  for j in range(33):points.extend([interpolate(one,j),interpolate(two,j)])
  set_uv(bpy.data.objects[p+side+' leg cloth'],points)
 hip=bpy.data.objects[p+'hip cloth'];set_uv(hip,[(1112+v.co.x*1.35,573-v.co.y*2) for v in hip.data.vertices])
 for ob in a['col'].objects:
  if any(t in ob.name for t in ['leg shade','trouser fold','knee crease','shin fold','trouser pocket']):ob.hide_render=ob.hide_viewport=True

def retime(name,knots):
 """Sample existing controls AND connected surfaces at the same source time."""
 a=n['ACTORS'][name];total=a['scene'].frame_end;actions={};mapping=[]
 for f in range(1,total+1):mapping.append(interpolate([(x,(y,)) for x,y in knots],f)[0])
 for ob in a['col'].objects:
  for data in [ob,getattr(ob.data,'shape_keys',None) if ob.type in ['MESH','CURVE'] else None]:
   if data and data.animation_data and data.animation_data.action:
    action=data.animation_data.action;actions[action.name]=action
 for action in actions.values():
  for layer in action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      values=[fc.evaluate(t) for t in mapping];fc.keyframe_points.clear();fc.keyframe_points.add(total)
      for f,(k,value) in enumerate(zip(fc.keyframe_points,values),1):k.co=(f,value);k.interpolation='CONSTANT' if fc.data_path.startswith('hide_') else 'LINEAR'
      fc.update()
 a['time_map']=mapping
 return {'actor':name,'actions_retimed_together':len(actions),'source_knots':knots}

def speech():
 analysis=json.loads((V/'artifacts/batch01-v013/word-analysis.json').read_text());plans={'opening Arteta':[('B02',67,6),('B03',213,4),('B05',346,5)],'delivery driver':[('B04',272,4)],'unveiling Gyokeres':[('L08',301,5)],'unveiling Arteta':[('L09',351,4)]}
 # These phonetic groups are timed within the actual spoken words, not across a phrase.
 phon={'this':'L E','year':'E U','we':'U E','finish':'FV E','the':'L E','job':'A MBP','i':'A E','ordered':'O E','a':'E','striker':'E A E','sorry':'O E','force':'FV O','of':'O FV','habit':'A MBP E','get':'E L','me':'MBP E','now':'A O','then':'L E','why':'U A E','am':'A MBP','here':'E U','win':'U E','us':'A E','corner':'O U'}
 records={}
 for name,lines in plans.items():
  a=n['ACTORS'][name];schedule={1:'rest'};words=[]
  for ident,start,count in lines:
   rows=[w for seg in analysis[ident]['segments'] for w in seg.get('words',[])][:count]
   for w in rows:
    text=w['word'].strip().lower().strip('.,?!');first=start+round(w['start']*24);last=start+round(w['end']*24);shapes=phon[text].split();words.append(dict(word=text,first=first,last=last))
    for j,shape in enumerate(shapes):schedule[first+round(j*(last-first)/len(shapes))]=shape
    schedule[last]='rest'
  for label,g in a['n']['FAC']['mouth shapes'].items():
   for ob in g.children_recursive:
    if ob.type not in ['MESH','CURVE']:continue
    ob.animation_data_clear()
    for f,shape in sorted(schedule.items()):
     ob.hide_render=ob.hide_viewport=label!=shape;ob.keyframe_insert(data_path='hide_render',frame=f);ob.keyframe_insert(data_path='hide_viewport',frame=f)
  if 'face14' in a:
   blinks={'opening Arteta':[145,201,329,395],'unveiling Arteta':[175,340,405],'unveiling Gyokeres':[125,293,345]}[name]
   for lid in a['face14']['eyes']:
    for f,value in [(1,0)]+[(x+d,v) for x in blinks for d,v in [(0,0),(2,1),(3,1),(5,0)]]+[(a['scene'].frame_end,0)]:lid.value=value;lid.keyframe_insert(data_path='value',frame=f)
  records[name]={'words':words,'mouth_keys':schedule}
 (O/'speech-timing.json').write_text(json.dumps(records,indent=2)+'\n');return records

def torso_grid(name):
 """Interior UV rows prevent a boundary-only triangle fan from shearing kit lettering."""
 from mathutils.geometry import delaunay_2d_cdt
 a=n['ACTORS'][name];p=a['prefix'];ob=bpy.data.objects[p+'connected upper body'];old=ob.data;verts=[v.co.copy() for v in old.vertices];core=[v.xy for v in verts[:16]];extra=[]
 def inside(x,y):
  c=False
  for aa,bb in zip(core,core[1:]+core[:1]):
   if (aa.y>y)!=(bb.y>y) and x<(bb.x-aa.x)*(y-aa.y)/(bb.y-aa.y)+aa.x:c=not c
  return c
 for y in range(0,186,15):
  for x in range(-48,49,12):
   if inside(x,y):extra.append(Vector((x,y,0)))
 vv,ed,ff,*_=delaunay_2d_cdt(core+[v.xy for v in extra],[],[list(range(16))],1,.001,False)
 # CDT can reorder points: map its coordinates back to original indices.
 lookup={(round(v.x,4),round(v.y,4)):i for i,v in enumerate(verts[:16])};new=[];ids=[]
 for v in vv:
  k=(round(v.x,4),round(v.y,4))
  if k not in lookup:lookup[k]=len(verts)+len(new);new.append(Vector((v.x,v.y,0)))
  ids.append(lookup[k])
 faces=[tuple(ids[i] for i in f) for f in ff]+[tuple(p.vertices) for p in old.polygons if any(i>=16 for i in p.vertices)]
 uv0={l.vertex_index:tuple(old.uv_layers.active.data[l.index].uv) for l in old.loops};pixels=[(uv0[i][0]*1536,(1-uv0[i][1])*1024) for i in range(len(verts))]
 for v in new:
  yy=interpolate([(-14,(519,)),(11,(490,)),(51,(445,)),(91,(400,)),(125,(337,)),(150,(290,)),(176,(246,)),(201,(207,))],v.y)[0]
  pixels.append((424+v.x*1.48,yy))
 me=bpy.data.meshes.new(old.name+' registered interior');me.from_pydata(verts+new,[],faces)
 snapshots=[(k.name,[(tuple(v.co)) for v in k.data]) for k in old.shape_keys.key_blocks];ob.data=me
 for index,(label,points) in enumerate(snapshots):
  k=ob.shape_key_add(name=label);me.shape_keys.use_relative=False
  for v,point in zip(k.data,points+[tuple(v) for v in new]):v.co=point
  k.interpolation='KEY_LINEAR';ks=me.shape_keys;ks.eval_time=index*10;ks.keyframe_insert(data_path='eval_time',frame=index+1)
 set_uv(ob,pixels);return len(new)

def fitted_lids(name):
 a=n['ACTORS'][name];n['use'](a['scene'],a['col']);cfg=json.loads((V/'artifacts/batch01-v013/source-heads.json').read_text())[a['kind']]['config'];a['face14']['eyes']=[]
 for side,(_,_,rx,ry) in zip(['L','R'],cfg['eyes']):
  old=bpy.data.objects.get(a['prefix']+'v014 '+side+' eyelid') or bpy.data.objects.get(a['prefix']+'v014 '+side+' fitted lid');bpy.data.objects.remove(old,do_unlink=True);edge=bpy.data.objects.get(a['prefix']+'v014 '+side+' lid edge');
  if edge:bpy.data.objects.remove(edge,do_unlink=True)
  e=a['C'][side+' eye'];rx*=1.03;ry*=1.03
  top=[(-rx,0),(-rx*.45,ry*.78),(rx*.4,ry*.86),(rx,0)];bottom=[(-rx,-2),(-rx*.45,-ry*1.03),(rx*.4,-ry*1.03),(rx,-2)]
  # Quad columns preserve the aperture boundary, including while the open lid has zero area.
  verts=[(x,y,z) for (x,y) in top for z in [0,0]]
  me=bpy.data.meshes.new(a['prefix']+'v014 '+side+' fitted lid');me.from_pydata(verts,[],[(2*i,2*i+1,2*i+3,2*i+2) for i in range(3)]);me.materials.append(b['mat'](cfg['skin']));ob=bpy.data.objects.new(me.name,me);a['col'].objects.link(ob);ob.parent=e;ob.location.z=1
  ob.shape_key_add(name='Open');closed=ob.shape_key_add(name='Closed');closed.value=0
  for i,pt in enumerate(bottom):closed.data[2*i+1].co=(*pt,0)
  a['face14']['eyes'].append(closed)
  line=n['line'](a['prefix']+'v014 '+side+' lid edge',[(-rx*.9,-2),(-rx*.4,-ry*.55),(rx*.4,-ry*.5),(rx*.85,-1)],'#75533a',2,.55,e,True)
  # Closed edge follows the eye aperture instead of painting a rectangle over the brow.
  line.hide_render=line.hide_viewport=True
  blinks={'opening Arteta':[145,201,329,395],'unveiling Arteta':[175,340,405],'unveiling Gyokeres':[125,293,345]}[name]
  for f,hidden in [(1,True)]+[(x+d,v) for x in blinks for d,v in [(1,True),(2,False),(4,True)]]:
   line.hide_render=line.hide_viewport=hidden;line.keyframe_insert(data_path='hide_render',frame=f);line.keyframe_insert(data_path='hide_viewport',frame=f)

"""CP02/03 picture excerpt: complete pose drawings, registered travel and contact correction."""
import bpy,math,json,hashlib
import numpy as np
from pathlib import Path
R=Path('/Users/samikd/MyProjects/Pencil/productions/Samtoons/videos/002-how-arsenal-won-the-league');A=R/'assets/chase-poses-v001';VERSION=globals().get('CHASE_VERSION','v001');MANAGERS='managers-low.png' if VERSION=='v002' else 'managers.png';O=R/('artifacts/chase-'+VERSION);NAME='S002_CP_chase_'+VERSION
assert not O.exists() and NAME not in bpy.data.scenes
s=bpy.data.scenes.new(NAME);bpy.context.window.scene=s;s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=32
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=192;s.view_settings.view_transform='Standard';s.view_settings.look='None';s.render.film_transparent=False
world=bpy.data.worlds.new(NAME);world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.38,.5,.61,1);s.world=world

def material(name,color):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=(*color,1);o=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],o.inputs[0]);return m
M={k:material('CP / '+k,c) for k,c in {'sky':(.65,.77,.82),'hill':(.33,.48,.45),'hill2':(.43,.58,.51),'road':(.19,.23,.27),'edge':(.72,.66,.51),'line':(.91,.87,.68),'wood':(.52,.33,.19),'green':(.06,.25,.19),'white':(.95,.94,.86),'podium':(.66,.075,.09),'podiumSide':(.35,.025,.05),'gold':(.98,.65,.14)}.items()}
def poly(name,points,y,mat,parent=None):
 mesh=bpy.data.meshes.new(name);mesh.from_pydata([(x,y,z) for x,z in points],[],[tuple(range(len(points)))]);ob=bpy.data.objects.new(name,mesh);s.collection.objects.link(ob);mesh.materials.append(mat);ob.parent=parent;return ob
def rect(name,x,z,w,h,y,mat,parent=None):return poly(name,[(x-w/2,z-h/2),(x+w/2,z-h/2),(x+w/2,z+h/2),(x-w/2,z+h/2)],y,mat,parent)
def textob(name,body,x,z,size,y,mat,parent=None):
 c=bpy.data.curves.new(name,'FONT');c.body=body;c.align_x='CENTER';c.size=size;c.extrude=0;ob=bpy.data.objects.new(name,c);s.collection.objects.link(ob);ob.location=(x,y,z);ob.rotation_euler=(math.pi/2,0,0);c.materials.append(mat);ob.parent=parent;return ob
rect('CP / sky',15,2.5,95,10,3,M['sky']);rect('CP / verge',15,-.5,95,1.7,1.8,M['hill']);rect('CP / road',15,-.5,95,.95,1,M['road']);rect('CP / curb',15,(-.01 if VERSION=='v002' else -.05),95,.07,.9,M['edge'])
for i in range(-4,29):
 x=i*2.2;poly('CP / distant hills',[(x-2,.5),(x-2,1.1),(x,2.0+(i%3)*.15),(x+3,1),(x+3,.5)],2.8,M['hill2']);rect('CP / road dash',x,-.57,.65,.035,.8,M['line'])
for x,label in [(3,'MARCH'),(12,'APRIL'),(22,'MAY')]:
 rect('CP / signpost',x,.78,.055,1.5,1.9,M['wood']);rect('CP / month sign',x,1.42,1.25,.39,1.7,M['green']);textob('CP / '+label,label,x,1.32,.22,1.6,M['white'])
cd=bpy.data.cameras.new(NAME+' camera');cd.type='ORTHO';cd.ortho_scale=7.8;cam=bpy.data.objects.new(cd.name,cd);s.collection.objects.link(cam);cam.location=(0,-12,1.6);cam.rotation_euler=(math.pi/2,0,0);s.camera=cam

# Label connected opaque figures via row runs, avoiding cell-edge clipping.
def components(mask):
 parent=[];runs=[];prev=[]
 def root(i):
  while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
  return i
 for y,row in enumerate(mask):
  changes=np.diff(np.r_[False,row,False].astype(np.int8));starts=np.where(changes==1)[0];ends=np.where(changes==-1)[0];cur=[]
  for x0,x1 in zip(starts,ends):
   idx=len(parent);parent.append(idx);runs.append((y,int(x0),int(x1)));cur.append(idx)
   for j in prev:
    _,a,b=runs[j]
    if a<x1 and b>x0:parent[root(idx)]=root(j)
  prev=cur
 groups={}
 for i,(y,a,b) in enumerate(runs):
  k=root(i);g=groups.setdefault(k,[a,y,b,y+1,0]);g[0]=min(g[0],a);g[1]=min(g[1],y);g[2]=max(g[2],b);g[3]=max(g[3],y+1);g[4]+=b-a
 big=[g for g in groups.values() if g[4]>5000];assert len(big)==8,[(g[:4],g[4]) for g in big]
 big.sort(key=lambda g:(g[1]+g[3])/2);return sorted(big[:4],key=lambda g:g[0])+sorted(big[4:],key=lambda g:g[0])

def sheet(file):
 im=bpy.data.images.load(str(A/file));im.pack();W,H=im.size;v=np.empty(W*H*4,np.float32);im.pixels.foreach_get(v);alpha=v.reshape(H,W,4)[::-1,:,3];assert (alpha<.95).mean()>.3
 m=bpy.data.materials.new('CP / '+file);m.use_nodes=True;n=m.node_tree.nodes;n.clear();l=m.node_tree.links;t=n.new('ShaderNodeTexImage');t.image=im;t.interpolation='Linear';e=n.new('ShaderNodeEmission');l.new(t.outputs['Color'],e.inputs[0]);tr=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');q=n.new('ShaderNodeMath');q.operation='GREATER_THAN';q.inputs[1].default_value=.95;l.new(t.outputs['Alpha'],q.inputs[0]);l.new(q.outputs[0],mix.inputs[0]);l.new(tr.outputs[0],mix.inputs[1]);l.new(e.outputs[0],mix.inputs[2]);out=n.new('ShaderNodeOutputMaterial');l.new(mix.outputs[0],out.inputs[0]);return alpha,components(alpha>.95),m,W,H
sheets={f:sheet(f) for f in ['gyokeres-selected.png','carriers.png',MANAGERS]}
actors={};metadata={};log=[]
# Hero's eight drawings retain two-frame run exposure. Support actors use four
# coordinated key drawings; passing poses have their own cadence in Pep cutaway.
configs=[('Gabriel','carriers.png',range(4),-2.05,2.12,.08,0,True),('Saliba','carriers.png',range(4,8),-.85,2.12,.03,4,True),('Gyokeres','gyokeres-selected.png',range(8),.45,2.12,-.02,0,True),('Arteta',MANAGERS,range(4),2.1,1.91,-.08,2,False),('Pep',MANAGERS,range(4,8),0,1.94,-.1,0,False)]
for name,file,indices,offset,topz,depth,phase,carrying in configs:
 alpha,boxes,mat,W,H=sheets[file];boxes=[boxes[i] for i in indices];height=max(b[3]-b[1] for b in boxes);scale=(topz-.025)/height
 root=bpy.data.objects.new('CP / '+name+' travel',None);s.collection.objects.link(root);root['pose_index']=0;root.id_properties_ui('pose_index').update(min=0,max=len(boxes)-1);root['method']='Complete registered drawings, independent world travel and camera, local support compensation.';actors[name]=root;poses=[]
 for i,b in enumerate(boxes):
  x0,y0,x1,y1,_=b;ys,xs=np.where(alpha[y0:y1,x0:x1]>.95);top=y0
  # Fixed-view overhead palms or head-top area is the anatomical registration.
  band=xs[ys<(14 if carrying else (y1-y0)*.20)];cx=float(band.mean()+x0);cy=float(top)
  near=ys>=ys.max()-2;fx=float(xs[near].mean()+x0);fy=float(ys.max()+y0);foot=((fx-cx)*scale,(cy-fy)*scale)
  box=[max(0,x0-3),max(0,y0-3),min(W,x1+3),min(H,y1+3)];xa,ya,xb,yb=box;nx,ny=20,36;verts=[];uvs=[];faces=[]
  for j in range(ny+1):
   py=ya+(yb-ya)*j/ny
   for k in range(nx+1):
    px=xa+(xb-xa)*k/nx;verts.append(((px-cx)*scale,0,(cy-py)*scale));uvs.append((px/W,1-py/H))
  for j in range(ny):
   for k in range(nx):
    a=j*(nx+1)+k;faces.append((a,a+nx+1,a+nx+2,a+1))
  me=bpy.data.meshes.new(name+' pose '+str(i));me.from_pydata(verts,[],faces);me.materials.append(mat);uv=me.uv_layers.new()
  for polygon in me.polygons:
   for lp in polygon.loop_indices:uv.data[lp].uv=uvs[me.loops[lp].vertex_index]
  ob=bpy.data.objects.new('CP / '+name+' pose '+str(i),me);s.collection.objects.link(ob);ob.parent=root;ob.shape_key_add(name='Basis')
  keys=[]
  for axis in [0,2]:
   sk=ob.shape_key_add(name='Support '+('X' if axis==0 else 'Z'));sk.slider_min=-2;sk.slider_max=2
   for v,kp in zip(ob.data.shape_keys.key_blocks['Basis'].data,sk.data):
    kp.co=v.co.copy();u=max(0.,min(1.,(foot[1]+.7-v.co.z)/.52));weight=u*u*(3-2*u);kp.co[axis]+=weight
   keys.append(sk)
  for prop in ['hide_render','hide_viewport']:
   dr=ob.driver_add(prop).driver;dr.expression='pose != '+str(i)+' or active < 0.5'
   v=dr.variables.new();v.name='pose';v.type='SINGLE_PROP';v.targets[0].id=root;v.targets[0].data_path='["pose_index"]';v=dr.variables.new();v.name='active';v.type='SINGLE_PROP';v.targets[0].id=root;v.targets[0].data_path='["active"]'
  poses.append((ob,foot,keys))
 metadata[name]={'file':file,'scale':scale,'registration':'overhead palms' if carrying else 'head top','pose_rects':[b[:4] for b in boxes],'feet':[list(p[1]) for p in poses]}
 speed=1.35 if name=='Pep' else 4.2;half=16 if name=='Pep' else 8;exposure=half//(len(poses)//2)
 # Contact anchors least-squares fit the pose geometry over each support half-step.
 for f in range(1,193):
  t=f-1;local=t+phase;idx=(local//exposure)%len(poses);h=local//half;q=local%half
  visible=f>120 if name=='Pep' else f<=120;root['active']=int(visible);root.keyframe_insert(data_path='["active"]',frame=f);root['pose_index']=idx;root.keyframe_insert(data_path='["pose_index"]',frame=f)
  x=speed*t/24+offset;z=topz
  # The loaded carriers keep palms on the separate podium; support correction
  # acts below the torso. Flight exposures keep the drawn boot clearance.
  in_flight=(name=='Gyokeres' and idx%4==3) or (name!='Pep' and q>=half-2)
  samples=[]
  for qq in range(half-2 if name!='Pep' else half):
   tt=h*half+qq-phase;ii=((h*half+qq)//exposure)%len(poses);samples.append(speed*tt/24+offset+poses[ii][1][0])
  plant=sum(samples)/len(samples);fx,fz=poses[idx][1];dx=0 if in_flight else plant-(x+fx);dz=max(0.,.025-(z+fz)) if in_flight else .025-(z+fz)
  root.location=(x,depth,z);root.keyframe_insert(data_path='location',frame=f)
  for pi,(ob,foot,keys) in enumerate(poses):
   keys[0].value=dx if pi==idx else 0;keys[1].value=dz if pi==idx else 0
   for sk in keys:sk.keyframe_insert(data_path='value',frame=f)
  if visible:log.append({'frame':f,'actor':name,'pose':idx,'root_x':x,'root_z':z,'contact':not in_flight,'plant_x':plant,'correction':[dx,dz]})
# Story prop: flat plane in front, shallow rear face, editable native label.
podium=bpy.data.objects.new('CP / first-place podium travel',None);s.collection.objects.link(podium)
rect('CP / podium shadow',-.78,2.265,3.93,.28,.12,M['podiumSide'],podium);rect('CP / podium front',-.78,2.32,3.9,.30,-.18,M['podium'],podium);rect('CP / podium raised centre',-.78,2.60,1.25,.35,-.18,M['podium'],podium);rect('CP / podium gold lip',-.78,2.80,1.32,.055,-.2,M['gold'],podium);textob('CP / first label','1st',-.78,2.44,.32,-.22,M['white'],podium)
for f in range(1,193):
 x=4.2*(f-1)/24;podium.location.x=x;podium.keyframe_insert(data_path='location',frame=f)
 for ob in podium.children:
  ob.hide_render=f>120;ob.hide_viewport=f>120;ob.keyframe_insert(data_path='hide_render',frame=f);ob.keyframe_insert(data_path='hide_viewport',frame=f)
 if f<=120:cam.location.x=x;cam.location.z=1.52;cd.ortho_scale=7.5
 else:cam.location.x=1.35*(f-1)/24+.35;cam.location.z=1.35;cd.ortho_scale=5.0
 cam.keyframe_insert(data_path='location',frame=f);cd.keyframe_insert(data_path='ortho_scale',frame=f)
# Linear frame sampling; pose/visibility and shot cut remain discrete.
for datablock in [*s.objects,cd,*[o.data.shape_keys for o in s.objects if o.type=='MESH' and o.data.shape_keys]]:
 ad=datablock.animation_data
 if ad and ad.action:
  for layer in ad.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for kp in fc.keyframe_points:kp.interpolation='CONSTANT' if fc.data_path in ['["pose_index"]','["active"]','hide_render','hide_viewport','ortho_scale'] else 'LINEAR'
s['Scope']='CP02/CP03 eight-second silent motion excerpt; 5s carrying sprint, 3s Pep cutaway. New cast/poses pending review.';s['Review status']='Pending review';s['Events']=json.dumps({'carriers_start':1,'cut_to_pep':121,'end':192});s.frame_set(25)
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL';area.spaces.active.overlay.show_overlays=False
O.mkdir(parents=True);(O/'motion.json').write_text(json.dumps(log,indent=2)+'\n');(O/'poses.json').write_text(json.dumps(metadata,indent=2)+'\n');(O/'provenance.json').write_text(json.dumps({'baseline':'artifacts/pose-action-v003/pose-action-v003.blend','script_sha256':hashlib.sha256((R/'script-v003.md').read_bytes()).hexdigest(),'images':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [A/'gyokeres-selected.png',A/'carriers.png',A/MANAGERS]},'construction':'complete pose drawings, editable selectors/travel/camera and local support corrections','new_character_assets':'pending review'},indent=2)+'\n')
bpy.data.libraries.write(str(O/('chase-'+VERSION+'.blend')),{s},fake_user=True);result={'scene':NAME,'file':str(O/('chase-'+VERSION+'.blend')),'actors':list(actors),'maximum_support_correction':max(max(abs(v) for v in row['correction']) for row in log)}

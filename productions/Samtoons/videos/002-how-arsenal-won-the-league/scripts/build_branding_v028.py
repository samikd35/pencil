"""Editable vector mascot / two short branding proofs. No finished-film scene changes."""
import bpy, math, re
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
V=Path(__file__).resolve().parents[1]; O=V/'artifacts/branding-v028';O.mkdir(exist_ok=True)
INK='#19202D';CORAL='#F46448';CREAM='#FFF4DC';PALE='#F3E6C9'
font=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf',check_existing=True)
regular=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial.ttf',check_existing=True)
def mat(c):
 name='BR28 '+c
 if bpy.data.materials.get(name):return bpy.data.materials[name]
 rgb=[int(c[i:i+2],16)/255 for i in (1,3,5)];rgb=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in rgb]
 m=bpy.data.materials.new(name);m.diffuse_color=(*rgb,1);m.use_nodes=True;n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=(*rgb,1);out=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],out.inputs[0]);return m

def empty(s,name,parent=None):
 ob=bpy.data.objects.new(name,None);s.collection.objects.link(ob);ob.parent=parent;return ob

def line(s,name,pts,c,z,parent=None,width=2,cyclic=False):
 d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=width;d.bevel_resolution=3;sp=d.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,(x,y) in zip(sp.points,pts):p.co=(x,y,z,1)
 sp.use_cyclic_u=cyclic;d.materials.append(mat(c));ob=bpy.data.objects.new(name,d);s.collection.objects.link(ob);ob.parent=parent;return ob

def poly(s,name,pts,c,z,parent=None,edge=0):
 vs=[Vector((x,y,z)) for x,y in pts];ts=tessellate_polygon([vs]);idx={tuple(v):i for i,v in enumerate(vs)};faces=[tuple(v if isinstance(v,int) else idx[tuple(v)] for v in t) for t in ts]
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],faces);me.materials.append(mat(c));ob=bpy.data.objects.new(name,me);s.collection.objects.link(ob);ob.parent=parent
 if edge:line(s,name+' outline',pts,INK,z+.05,parent,edge,True)
 return ob

def ellipse(s,name,x,y,rx,ry,c,z,parent=None,edge=0):return poly(s,name,[(x+rx*math.cos(i*math.tau/80),y+ry*math.sin(i*math.tau/80)) for i in range(80)],c,z,parent,edge)
def shape(s,name,cmd,c,z,parent,edge=0):
 # Authored cubic contours in the supplied logo's 1024px design space.
 t=re.findall(r'[MCZ]|-?\d+(?:\.\d+)?',cmd);pts=[];i=0;p=None
 while i<len(t):
  op=t[i];i+=1
  if op=='Z':break
  if op=='M':p=(float(t[i]),float(t[i+1]));i+=2;pts.append(p)
  elif op=='C':
   a=tuple(map(float,t[i:i+2]));b=tuple(map(float,t[i+2:i+4]));q=tuple(map(float,t[i+4:i+6]));i+=6
   for k in range(1,21):
    u=k/20;pts.append(tuple((1-u)**3*p[j]+3*(1-u)**2*u*a[j]+3*(1-u)*u*u*b[j]+u**3*q[j] for j in (0,1)))
   p=q
 return poly(s,name,[(x-512,512-y) for x,y in pts],c,z,parent,edge)
BODY='M 735 308 C 718 218 622 196 542 209 C 404 206 304 270 286 365 C 268 450 305 507 387 533 C 449 552 520 558 536 586 C 553 617 512 638 470 627 C 418 615 385 581 351 583 C 289 584 271 655 287 711 C 303 780 368 807 477 806 C 600 806 719 757 738 676 C 757 590 704 542 639 512 C 586 487 528 467 508 443 C 537 426 564 447 603 451 C 674 460 740 406 735 308 Z'
BROW1='M 463 281 C 479 225 511 218 541 251 C 552 263 560 272 561 281 C 523 259 503 251 463 281 Z'
BROW2='M 604 294 C 627 299 656 249 679 258 C 690 262 692 277 690 293 C 674 271 654 288 631 303 C 616 310 608 306 604 294 Z'
MOUTH='M 479 681 C 547 674 611 647 644 594 C 640 656 615 692 573 706 C 540 718 503 702 479 681 Z'
TEETH='M 499 684 C 555 677 608 652 635 617 C 630 657 604 687 573 697 C 545 705 515 696 499 684 Z'
def mascot(s,label):
 root=empty(s,label+' / squash root');shape(s,label+' / S',BODY,CORAL,2,root,10)
 eyes=[];pupils=[]
 for n,x,y,rx,ry in [('left',509,352,51,73),('right',640,367,44,62)]:
  e=empty(s,label+' / '+n+' blink',root);e.location=(x-512,512-y,0);ellipse(s,n+' eye',0,0,rx,ry,CREAM,4,e,4)
  p=empty(s,label+' / '+n+' gaze',e);ellipse(s,n+' pupil',0,0,rx*.46,ry*.60,INK,5,p);ellipse(s,n+' glint',-7,14,6,10,CREAM,6,p);eyes.append(e);pupils.append(p)
 brows=[]
 for j,cmd in enumerate([BROW1,BROW2]):
  b=empty(s,label+f' / brow {j}',root);shape(s,label+f' brow shape {j}',cmd,INK,7,b);brows.append(b)
 shape(s,label+' / grin',MOUTH,INK,4,root);shape(s,label+' / teeth',TEETH,CREAM,5,root)
 line(s,label+' tooth divider',[(592-512,512-659),(600-512,512-687)],INK,6,root,3)
 shape(s,label+' / smile corner','M 625 584 C 641 573 664 581 669 601 C 649 587 638 590 625 584 Z',INK,6,root)
 return root,eyes,pupils,brows

def text(s,name,body,x,y,size,c=INK,parent=None,align='LEFT',bold=True):
 d=bpy.data.curves.new(name,'FONT');d.body=body;d.font=font if bold else regular;d.size=size;d.align_x=align;d.materials.append(mat(c));ob=bpy.data.objects.new(name,d);s.collection.objects.link(ob);ob.location=(x,y,15);ob.parent=parent;return ob

def key(ob,path,v,f):setattr(ob,path,v);ob.keyframe_insert(data_path=path,frame=f)
def lerp(a,b,t):return a+(b-a)*t
def ease(t):t=max(0,min(1,t));return t*t*(3-2*t)
def scene(name,frames):
 s=bpy.data.scenes.new(name);s.render.engine='BLENDER_EEVEE';s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_end=frames;s.eevee.taa_render_samples=16;s.view_settings.view_transform='Standard';s.view_settings.look='None';s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.compression=0
 cam=bpy.data.cameras.new(name+' camera');cam.type='ORTHO';cam.ortho_scale=1280;cam.clip_end=3000;ob=bpy.data.objects.new(name+' camera',cam);s.collection.objects.link(ob);ob.location=(0,0,1000);s.camera=ob
 poly(s,'cream stage',[(-650,-370),(650,-370),(650,370),(-650,370)],CREAM,0)
 # Deliberate fixed camera, sparse football field markings at the bottom.
 line(s,'pitch touchline',[(-640,-302),(640,-302)],PALE,1,width=2)
 line(s,'centre circle',[(110*math.cos(i*math.tau/96),-302+110*math.sin(i*math.tau/96)) for i in range(97)],PALE,1,width=2)
 return s
intro=scene('SAMTOONS / 03s intro',72);r,eyes,pupils,brows=mascot(intro,'intro mascot');r.location=(-295,-6,0);r.scale=(.69,.69,1)
word=empty(intro,'wordmark reveal');text(intro,'Samtoons wordmark','SAMTOONS',-27,15,77,parent=word);text(intro,'tagline','Football. Drama. Punchlines.',-22,-43,24,parent=word,bold=False)
ball=empty(intro,'ball / impact and ricochet');ellipse(intro,'football',0,0,35,35,CREAM,20,ball,2.2)
poly(intro,'centre panel',[(13*math.cos(i*math.tau/5+.3),13*math.sin(i*math.tau/5+.3)) for i in range(5)],INK,21,ball)
for i in range(5):
 a=i*math.tau/5+.3;line(intro,'panel seam',[(13*math.cos(a),13*math.sin(a)),(30*math.cos(a+.18),30*math.sin(a+.18))],INK,21,ball,1)
 ellipse(intro,'edge panel',31*math.cos(a+.18),31*math.sin(a+.18),4,5,INK,21,ball)
for f in range(1,73):
 t=(f-1)/24
 # Left edge of S is ~-450. Ball arrives, rebounds away, and falls out.
 if f<=13:x=lerp(-720,-470,(f-1)/12);y=45+18*math.sin((f-1)/12*math.pi)
 else:u=(f-13)/24;x=-470-280*u;y=45+200*u-430*u*u
 key(ball,'location',(x,y,0),f);key(ball,'rotation_euler',(0,0,-t*8),f)
 hit=max(0,1-abs(f-16)/4) if 12<=f<=20 else 0
 rebound=max(0,1-abs(f-23)/5)*.05
 key(r,'scale',(.69*(1-.13*hit+rebound),.69*(1+.09*hit-rebound),1),f);key(r,'location',(-295+14*hit,-6,0),f)
 show=ease((f-27)/10);key(word,'scale',(show,show,1),f)
 for j,p in enumerate(pupils):key(p,'location',(-16+27*ease((f-25)/8),2,0),f)
 wink=1-.94*max(0,1-abs(f-48)/3)
 key(eyes[1],'scale',(1,wink,1),f);key(brows[1],'location',(0,9*ease((f-35)/8),0),f)
outro=scene('SAMTOONS / 12s outro',288);r,eyes,pupils,brows=mascot(outro,'outro mascot');r.location=(-370,48,0);r.scale=(.62,.62,1)
card=empty(outro,'end card reveal');text(outro,'channel name','SAMTOONS',-370,-170,47,parent=card,align='CENTER');text(outro,'tagline','Football. Drama. Punchlines.',-370,-203,17,parent=card,align='CENTER',bold=False)
text(outro,'promise','Your club is next.',70,222,50,parent=card)
text(outro,'watch next label','WATCH NEXT',70,157,18,CORAL,parent=card)
# The open area is reserved for a real YouTube thumbnail. No false play button.
poly(outro,'video space',[(70,127),(550,127),(550,-143),(70,-143)],PALE,2,card)
line(outro,'video space border',[(70,127),(550,127),(550,-143),(70,-143)],INK,3,card,1.7,True)
text(outro,'thumbnail placeholder','MORE FOOTBALL.',310,5,29,parent=card,align='CENTER');text(outro,'thumbnail second line','MORE DRAMA.',310,-32,29,parent=card,align='CENTER')
ellipse(outro,'subscribe circle',107,-232,40,40,CORAL,5,card)
text(outro,'subscribe circle S','S',107,-251,54,CREAM,parent=card,align='CENTER');text(outro,'subscribe label','SUBSCRIBE',170,-231,29,parent=card)
text(outro,'subscribe promise','Nobody gets a free pass.',170,-258,18,parent=card,bold=False)
paper=empty(outro,'Ferguson paper / flutter');poly(outro,'paper sheet',[(-92,-72),(78,-66),(91,64),(-85,75)],'#FFFCF0',23,paper,1.5)
for yy,w in [(37,102),(15,118),(-7,82),(-29,108)]:line(outro,'paper scribble',[(-56,yy),(-56+w,yy+3)],'#AAA99E',24,paper,1.3)
for f in range(1,289):
 u=ease((f-1)/12)
 if f<=13:px=lerp(720,-344,u);py=lerp(265,133,u);ang=lerp(-.7,.12,u)
 elif f<30:px=-344+4*math.sin(f*1.8);py=133;ang=.12+.05*math.sin(f*1.8)
 else:q=(f-30)/24;px=-344-145*q;py=133-90*q-470*q*q;ang=.12+q*3.5
 key(paper,'location',(px,py,0),f);key(paper,'rotation_euler',(0,0,ang),f)
 shake=math.sin((f-14)*1.2)*.10 if 18<=f<=32 else 0
 key(r,'rotation_euler',(0,0,shake),f)
 key(r,'scale',(.62*(1+.022*math.sin((f-34)*.5)*max(0,1-(f-34)/14)) if 34<=f<=48 else .62,.62,1),f)
 show=ease((f-32)/12);key(card,'scale',(show,show,1),f)
 for j,p in enumerate(pupils):key(p,'location',(lerp(-10,14,ease((f-42)/9)),2+2*math.sin(f*.02),0),f)
 wink=1-.94*max(0,1-abs(f-65)/3)
 blink=1-.91*max(0,1-abs(f-188)/3)
 for j,e in enumerate(eyes):key(e,'scale',(1,min(wink if j==1 else 1,blink),1),f)
 key(brows[1],'location',(0,10*ease((f-50)/8),0),f)
for s in (intro,outro):
 for ob in s.objects:
  if ob.animation_data and ob.animation_data.action:
   for layer in ob.animation_data.action.layers:
    for strip in layer.strips:
     for bag in strip.channelbags:
      for fc in bag.fcurves:
       for kp in fc.keyframe_points:kp.interpolation='LINEAR'
 s.frame_set(60)
intro['purpose']='3s mascot sting after 7.5s cold open';outro['purpose']='12s paper gag and endscreen after intact ending';outro['youtube_end_screen']='Thumbnail x=710..1190 y=233..503; subscribe circle center=(747,592), both in 1280x720 coordinates. Enable after first 2 seconds.'
font.pack();regular.pack()
bpy.data.libraries.write(str(O/'samtoons-branding.blend'),{intro,outro},fake_user=True,compress=True)
bpy.context.window.scene=intro
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL'
result={'scenes':[intro.name,outro.name],'file':str(O/'samtoons-branding.blend'),'construction':'native editable vector meshes, contours, facial controls; no image planes'}

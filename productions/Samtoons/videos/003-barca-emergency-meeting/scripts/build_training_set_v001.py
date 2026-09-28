"""Scene-specific native 2.5D training set; run build() in visible Blender.

Reuses Video001's inspected surface/tube mechanisms, with this film's world
geometry and art direction. No old scene or live registry is imported. The
environment is a stylized interpretation of a training complex, not a surveyed
reconstruction of Ciutat Esportiva. The goal-factory props are fictional.
"""
from pathlib import Path
import bpy, math, json
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/staging-v001/training-set-v001'
INK='#253444';WHITE='#fff7dc';MATS={}
COL=None

def mat(hexcolor):
    if hexcolor in MATS:return MATS[hexcolor]
    rgb=[int(hexcolor[i:i+2],16)/255 for i in (1,3,5)]
    rgb=tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb)
    m=bpy.data.materials.new('S003 Set '+hexcolor);m.diffuse_color=(*rgb,1)
    MATS[hexcolor]=m;return m

def surface(name,points,color):
    me=bpy.data.meshes.new(name);me.from_pydata(points,[],[list(range(len(points)))]);me.materials.append(mat(color))
    ob=bpy.data.objects.new(name,me);COL.objects.link(ob);return ob

def tube(name,points,color,width=.025):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=width;d.bevel_resolution=2;d.use_fill_caps=True
    sp=d.splines.new('POLY');sp.points.add(len(points)-1)
    for p,xyz in zip(sp.points,points):p.co=(*xyz,1)
    d.materials.append(mat(color));ob=bpy.data.objects.new(name,d);COL.objects.link(ob);return ob

def box(name,x,y,z,w,d,h,front,side=None,top=None):
    # Deliberately drawn face values; the perspective comes from native geometry.
    side=side or front;top=top or front
    surface(name+' front',[(x,y,z),(x+w,y,z),(x+w,y,z+h),(x,y,z+h)],front)
    surface(name+' side L',[(x,y,z),(x,y+d,z),(x,y+d,z+h),(x,y,z+h)],side)
    surface(name+' side R',[(x+w,y,z),(x+w,y+d,z),(x+w,y+d,z+h),(x+w,y,z+h)],side)
    surface(name+' back',[(x,y+d,z),(x+w,y+d,z),(x+w,y+d,z+h),(x,y+d,z+h)],front)
    surface(name+' top',[(x,y,z+h),(x+w,y,z+h),(x+w,y+d,z+h),(x,y+d,z+h)],top)

def label(name,words,pos,size,color=WHITE):
    d=bpy.data.curves.new(name,'FONT');d.body=words;d.size=size;d.align_x='CENTER'
    d.materials.append(mat(color));ob=bpy.data.objects.new(name,d);COL.objects.link(ob)
    ob.location=pos;ob.rotation_euler.x=math.pi/2;return ob

def ground_patch(name,x,y,rx,ry,color,z=.008):
    return surface(name,[(x+rx*math.cos(i*math.tau/48),y+ry*math.sin(i*math.tau/48),z) for i in range(48)],color)

def aim(name,position,target,lens=42):
    d=bpy.data.cameras.new(name);d.type='PERSP';d.lens=lens;d.clip_end=450
    o=bpy.data.objects.new(name,d);COL.objects.link(o);o.location=position
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o

def pitch():
    surface('Grass run-off',[(-46,-112,-.01),(46,-112,-.01),(46,12,-.01),(-46,12,-.01)],'#6e9853')
    surface('105 x 68 m playing surface',[(-34,-105,0),(34,-105,0),(34,0,0),(-34,0,0)],'#6caa5b')
    for i in range(14):
        y=-105+i*7.5
        if i%2==0:surface('Mowing band', [(-34,y,.002),(34,y,.002),(34,y+7.5,.002),(-34,y+7.5,.002)],'#78b665')
    z=.016;thickness=.05
    tube('Boundary', [(-34,0,z),(34,0,z),(34,-105,z),(-34,-105,z),(-34,0,z)],WHITE,thickness)
    tube('Halfway',[(-34,-52.5,z),(34,-52.5,z)],WHITE,thickness)
    tube('Centre circle',[(9.15*math.cos(t*math.tau/120),-52.5+9.15*math.sin(t*math.tau/120),z) for t in range(121)],WHITE,thickness)
    ground_patch('Centre mark',0,-52.5,.10,.10,WHITE,z)
    for goal_y,direction in [(0,-1),(-105,1)]:
        for half,depth in [(9.16,5.5),(20.16,16.5)]:
            tube('Area marking',[(-half,goal_y,z),(-half,goal_y+direction*depth,z),(half,goal_y+direction*depth,z),(half,goal_y,z)],WHITE,thickness)
        ground_patch('Penalty mark',0,goal_y+direction*11,.10,.10,WHITE,z)
        limit=math.acos(5.5/9.15)
        tube('Penalty arc',[(9.15*math.sin(a),goal_y+direction*(11+9.15*math.cos(a)),z) for a in [-limit+2*limit*k/50 for k in range(51)]],WHITE,thickness)
        for x in [-34,34]:
            sx=1 if x<0 else -1
            tube('Corner arc',[(x+sx*math.cos(k*math.pi/64),goal_y+direction*math.sin(k*math.pi/64),z) for k in range(33)],WHITE,thickness)
            tube('Corner pole',[(x,goal_y,0),(x,goal_y,1.55)],WHITE,.024)
            surface('Corner pennant',[(x,goal_y,1.54),(x+.48,goal_y,1.4),(x,goal_y,1.23)],'#c9434c')

def goal():
    # Inner clearance, not post-centre spacing: 7.32 x 2.44 metres.
    radius=.06;post=3.66+radius;bar=2.44+radius;depth=2.3
    tube('Goal front',[(-post,0,0),(-post,0,bar),(post,0,bar),(post,0,0)],WHITE,radius)
    for x in [-post,post]:
        tube('Goal return',[(x,0,bar),(x,depth,bar),(x,depth,0),(x,0,0)],'#dce5dc',.035)
        box('Goal anchor',x-.14,depth-.15,0,.28,.35,.07,'#c4cebf')
    tube('Rear crossbar',[(-post,depth,bar),(post,depth,bar)],'#c2d0c9',.03)
    for i in range(38):
        x=-post+i*2*post/37
        tube('Net roof and back',[(x,0,bar),(x,depth,bar),(x,depth,0)],'#d4e1d1',.007)
    for j in range(14):
        z=bar*j/13
        tube('Net side and back',[(-post,0,z),(-post,depth,z),(post,depth,z),(post,0,z)],'#d4e1d1',.007)
    for k in range(1,12):
        y=depth*k/12
        for x in [-post,post]:tube('Net side upright',[(x,y,0),(x,y,bar)],'#d4e1d1',.007)
    # Grounded directional shadow; no opaque rectangle across the open goal mouth.
    tube('Crossbar drawn shadow',[(-post+1.25,1.8,.009),(post+1.25,1.8,.009)],'#5d8c50',.044)
    for x in [-post,post]:tube('Post drawn shadow',[(x,0,.009),(x+1.25,1.8,.009)],'#5d8c50',.055)

def surroundings():
    # Extend the land beyond the playing surface: sky must not show under trees.
    surface('Training complex grounds',[(-160,-112,-.02),(160,-112,-.02),(160,100,-.02),(-160,100,-.02)],'#8da774')
    surface('Service path',[(-45,9,.002),(45,9,.002),(45,12,.002),(-45,12,.002)],'#c6c6af')
    box('Back perimeter base',-40,8,0,80,.25,.75,'#263e5b','#203448','#385974')
    for x in [-30,-15,0,15,30]:label('Training boundary identity','FC BARCELONA',(x,7.96,.24),.39)
    for x in range(-40,41,4):tube('Ball-stop post',[(x,8,.75),(x,8,5.2)],'#849792',.045)
    for z in [1.7,2.7,3.8,5.1]:tube('Fence cable',[(-40,8,z),(40,8,z)],'#9eafa3',.009)
    for x in range(-40,41,1):tube('Fence mesh',[(x,8,.75),(x,8,5.1)],'#9eafa3',.005)
    # Layered landscaping, distant buildings and floodlights give depth without texture noise.
    surface('Distant hills',[(-120,64,0),(-120,64,6),(-85,64,14),(-60,64,9),(-26,64,18),(9,64,13),(42,64,20),(78,64,11),(120,64,17),(120,64,0)],'#a9bfba')
    for x,w,h in [(-63,17,7),(-36,10,9),(14,12,6),(48,22,8)]:
        box('Distant building',x,43,0,w,8,h,'#b9c6bd','#a6b9b1','#ced3c5')
    for i,x in enumerate(range(-44,48,5)):
        yy=24+(i%3)*1.5
        tube('Tree trunk',[(x,yy,0),(x,yy,4.9)],'#667966',.14)
        for dx,zz,rx,rz,col in [(0,4.2,2.6,1.65,'#638b63'),(.65,5.4,2.2,1.65,'#789c6d'),(-.8,5.0,1.55,1.2,'#89aa76')]:
            surface('Drawn canopy',[(x+dx+rx*math.cos(k*math.tau/24),yy-.035*zz,zz+rz*math.sin(k*math.tau/24)) for k in range(24)],col)
    box('Service building',-20,15,0,21,7,4.2,'#e3dec7','#bebca9','#f2ead3')
    box('Service roof fascia',-20.5,14.5,4.0,22,8,.42,'#354958','#293b4c','#506978')
    for x in range(-19,0,3):
        surface('Glazing',[(x,14.96,.65),(x+2,14.96,.65),(x+2,14.96,3.4),(x,14.96,3.4)],'#87b0bd')
        tube('Window mullion',[(x+1,14.92,.65),(x+1,14.92,3.4)],'#506c7a',.024)
        surface('Window reflection',[(x,14.93,2.5),(x+1.4,14.93,3.4),(x+2,14.93,3.4),(x+.6,14.93,2.5)],'#bdd5d6')
    label('Training centre name','CIUTAT ESPORTIVA',(-9.5,14.90,3.67),.38)
    for x in [-34,34]:
        tube('Floodlight mast',[(x,10,0),(x,10,14)],'#84958e',.1)
        box('Floodlight frame',x-1.5,9.7,13.5,3,.35,.85,'#d2d8c7','#899e9c','#eeead3')
        for dx in [-1.1,-.35,.4,1.15]:box('Floodlight lamp',x+dx-.2,9.63,13.68,.4,.08,.43,WHITE)
    # Covered substitute bench stays outside the touchline, not in a shooting lane.
    box('Bench plinth',-40,-12,0,3.8,8,.15,'#65786b')
    box('Dugout back',-40,-12,.15,.12,8,2.2,'#637f8a')
    surface('Dugout roof',[(-40.1,-12.2,2.35),(-36,-12.2,2.35),(-36,-3.8,2.35),(-40.1,-3.8,2.35)],'#3f6070')
    for y in [-11,-9.5,-8,-6.5,-5]:box('Bench seat',-39.7,y,.5,.65,1.05,.1,'#a33447','#742936','#bf4a54');box('Seat back',-39.82,y,.53,.15,1.05,.8,'#a33447')

def factory_props():
    # Fictional equipment is beyond the byline, with clear clearance behind the goal.
    box('Ball-return belt base',-10,4.5,.42,19,.72,.20,'#455c67','#30434f','#667e83')
    for x in range(-10,10):tube('Belt roller',[(x,4.5,.64),(x,5.22,.64)],'#2a3e4a',.05)
    for x in [-9,-3,3,8]:box('Belt support',x,4.6,0,.15,.50,.43,'#394f57')
    box('Ball storage',11,4.3,0,1.6,1.0,1.1,'#b0804f','#8d633f','#d3a874')
    label('Ball storage label','NEXT',(11.8,4.28,.45),.23,WHITE)
    for x in [9.7,11.1]:tube('Counter posts',[(x,3,0),(x,3,2.6)],'#415660',.045)
    box('Goal counter',9.4,2.9,2.1,2,.15,.65,'#213849','#213849','#526c75')
    label('Goal count','GOALS  7',(10.4,2.87,2.30),.28,'#edcf72')

def build():
    global COL
    assert bpy.context.window and not bpy.app.background,'Author in visible Blender'
    name='S003_Training_Set_v001'
    assert name not in bpy.data.scenes,'Use a new revision rather than overwriting'
    s=bpy.data.scenes.new(name);bpy.context.window.scene=s
    COL=bpy.data.collections.new('S003 / training environment');s.collection.children.link(COL)
    s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=1600;s.render.resolution_y=900;s.render.resolution_percentage=100
    s.render.fps=24;s.frame_end=1;s.render.image_settings.file_format='PNG';s.render.use_sequencer=False
    s.display.shading.light='FLAT';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=False
    s.display.shading.show_cavity=False;s.display.shading.show_specular_highlight=False
    s.display.shading.background_type='WORLD';s.world=bpy.data.worlds.new('S003 training sky');s.world.color=(.62,.79,.84)
    s.view_settings.view_transform='Standard';s.view_settings.look='None';s.display.render_aa='32'
    pitch();goal();surroundings();factory_props()
    cameras=[aim('S06 wide',(-25,-32,7.5),(0,-3,1.6),40),aim('S06 finish',(-9,-18,3.8),(1,0,1.3),45),aim('Field plan',(0,-48,110),(0,-48,0),35)]
    cameras[2].data.type='ORTHO';cameras[2].data.ortho_scale=215
    s.camera=cameras[0]
    s['scope']='Native environment staging. No character acting, physical-contact or final visual-quality acceptance.'
    s['dimensions']=json.dumps({'pitch':[105,68],'goal_inner':[7.32,2.44],'goal_depth':2.3,'ball_radius_target':.11,'character_height_range':[1.70,1.95]})
    for a in bpy.context.screen.areas:
        if a.type=='VIEW_3D':
            a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.shading.type='SOLID'
            a.spaces.active.shading.light='FLAT';a.spaces.active.shading.color_type='MATERIAL';a.spaces.active.overlay.show_overlays=False
    return {'scene':s.name,'objects':len(s.objects),'cameras':[c.name for c in cameras]}

def check():
    s=bpy.data.scenes['S003_Training_Set_v001'];front=next(o for o in s.objects if o.name=='Goal front')
    pts=[p.co for p in front.data.splines[0].points];radius=front.data.bevel_depth
    assert abs((pts[2].x-pts[1].x-2*radius)-7.32)<1e-5
    assert abs(pts[1].z-radius-2.44)<1e-5
    assert all(abs(o.matrix_world.translation.z)<1e-6 for o in s.objects if o.name.startswith('Boundary'))
    assert not any(o.type=='MESH' and any(m and m.use_nodes and any(n.type=='TEX_IMAGE' for n in m.node_tree.nodes) for m in o.data.materials) for o in s.objects)
    return {'goal_inner_width':7.32,'goal_inner_height':2.44,'pitch':[105,68],'native_environment_no_image_planes':True,'creative_acceptance':False}

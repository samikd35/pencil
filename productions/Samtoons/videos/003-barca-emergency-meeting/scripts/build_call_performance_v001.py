"""S08: editable native drawing and authored acting, built in visible Blender.

Builder owns this revision. Historical pure drawing primitives only; no old scene
or choreography. The generated treatment is a reference, never a scene texture.
"""
import ast, bpy, math, sys
from pathlib import Path
from mathutils import Vector

V = Path(__file__).resolve().parents[1]
W = V.parents[3]
O = V / 'artifacts/staging-v001/call-performance-v001'
sys.path.insert(0, str(W))
from pipeline.pose_geometry import two_bone_joint

p = V.parent/'001-manchester-derby-2026-09-13/scripts/build_staging.py'
b = {'__file__': str(p)}
exec(compile(p.read_text(), str(p), 'exec'), b)
p = next(V.parent.glob('002*/scripts/build_ferguson_native_v007.py'))
tree = ast.parse(p.read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'smooth'], type_ignores=[]), str(p), 'exec'))

INK='#202332'; SKIN='#efb07d'; SHADE='#d58962'; HI='#ffd09b'
C={}; F={}; ARMS={}; ARM_ART={}

def shape(name, pts, z, color, parent=None, outline=True, soft=True):
    pts=smooth(pts) if soft else pts
    ob=b['poly']('C3 / '+name, pts,z,color,parent,False)
    if outline: stroke(name+' edge',pts+[pts[0]],z+.25,INK,1.1,parent,False)
    return ob

def stroke(name,pts,z,color=INK,width=1,parent=None,soft=True):
    return b['line']('C3 / '+name,smooth(pts,False) if soft else pts,z,color,width,parent)

def oval(name,x,y,rx,ry,z,color,parent=None,outline=False):
    return shape(name,b['oval'](x,y,rx,ry),z,color,parent,outline,False)

def rect(name,x,y,w,h,z,color,parent=None,outline=True):
    return shape(name,[(x,y),(x+w,y),(x+w,y+h),(x,y+h)],z,color,parent,outline,False)

def text(name,words,x,y,z,size,color,parent=None):
    return b['text']('C3 / '+name,words,x,y,z,size,color,parent)

def control(name,loc=(0,0,0),parent=None):
    ob=b['empty']('C3 / '+name,loc,parent); ob.empty_display_size=8; C[name]=ob
    return ob

def setup():
    global s,col
    assert bpy.context.window and bpy.context.mode=='OBJECT'
    assert 'S003_S08_Call_Performance_v001' not in bpy.data.scenes
    s=bpy.data.scenes.new('S003_S08_Call_Performance_v001'); bpy.context.window.scene=s
    col=bpy.data.collections.new('S003 / S08 editable drawn performance v001'); s.collection.children.link(col)
    b['skin']=col; b['ink']=b['mat'](INK)
    b['font']=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Bold.ttf')
    s.render.engine='BLENDER_WORKBENCH'; s.display.shading.light='FLAT'; s.display.shading.color_type='MATERIAL'
    s.display.shading.show_shadows=False; s.display.shading.show_cavity=False; s.display.shading.show_specular_highlight=False
    s.display.shading.show_object_outline=False; s.display.render_aa='16'
    s.render.resolution_x=1280; s.render.resolution_y=720; s.render.resolution_percentage=100
    s.render.fps=24; s.frame_start=1; s.frame_end=240; s.render.use_sequencer=False
    s.render.image_settings.file_format='PNG'; s.render.image_settings.color_mode='RGB'
    s.view_settings.view_transform='Standard'; s.view_settings.look='None'
    s.world=bpy.data.worlds.new('S003 call flat world'); s.world.color=(.02,.02,.02)
    d=bpy.data.cameras.new('S003 call camera'); d.type='ORTHO'; d.ortho_scale=1280; d.clip_end=3000
    cam=bpy.data.objects.new(d.name,d); col.objects.link(cam); cam.location=(0,0,1200); s.camera=cam
    s['construction']='Native filled mesh drawings, curve strokes, articulated limbs and facial replacement drawings. No character raster planes.'
    s['status']='Unapproved representative acting candidate; not a finished film'
    for area in bpy.context.screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_perspective='CAMERA'; area.spaces.active.overlay.show_overlays=False
            area.spaces.active.shading.type='SOLID'; area.spaces.active.shading.light='FLAT'; area.spaces.active.shading.color_type='MATERIAL'
    O.mkdir(parents=True,exist_ok=True)

def room():
    rect('office wall',-700,-400,1400,800,-80,'#61758d',outline=False)
    for x in [-580,-390,-180,40,255,470]:stroke('wall panel',[(x,-300),(x,370)],-79,'#475c74',1.5,soft=False)
    shape('window light',[(190,360),(640,360),(640,-225),(80,-225)],-78,'#71869b',outline=False,soft=False)
    rect('whiteboard shadow',135,36,550,285,-74,'#495e74',outline=False)
    rect('whiteboard frame',126,46,550,285,-73,'#273647')
    rect('whiteboard',137,57,530,263,-72,'#eeeada',outline=False)
    text('board title','HOW TO BEAT',406,284,-71,27,'#263349')
    text('board title lower','BARCELONA',406,249,-71,31,'#263349')
    stroke('board underline',[(272,224),(548,224)],-71,'#263349',1.8,soft=False)
    for x,y in [(300,167),(459,183),(510,95)]:
        stroke('tactics cross',[(x-7,y-7),(x+7,y+7)],-71,'#537184',1.4,soft=False)
        stroke('tactics cross',[(x-7,y+7),(x+7,y-7)],-71,'#537184',1.4,soft=False)
    stroke('tactics arrow',[(340,87),(376,151),(425,194)],-71,'#537184',1.6)
    stroke('arrow head',[(409,191),(426,195),(422,179)],-71,'#537184',1.6,soft=False)
    # The monitor's warm room is drawn separately behind its performer.
    rect('monitor support',-337,-249,42,84,-66,'#253448')
    shape('monitor base',[(-448,-257),(-360,-230),(-260,-230),(-195,-257)],-65,'#263347',soft=False)
    rect('monitor frame',-605,-221,704,540,-60,'#1b2538')
    rect('monitor bevel',-594,-210,682,518,-59,'#3e4d63',outline=False)
    rect('warm call room',-581,-197,656,492,-58,'#d8af78',outline=False)
    for x in [-569,-343,-117]:rect('room panels',x,-180,9,469,-57,'#c59a65',outline=False)
    rect('shelf unit',-117,-150,180,214,-55,'#79543f')
    for y in [-142,-58,53]:rect('shelf',-117,y,180,9,-54,'#a27952',outline=False)
    for i,c in enumerate(['#994d46','#eee4cb','#5b7380','#a75047']):
        rect('books',-98+i*25,-47,17,64+i*3,-53,c)
    oval('plant pot',16,87,30,29,-53,'#68727a')
    for dx,dy in [(-24,33),(0,65),(30,46),(-41,13),(37,14)]:
        shape('plant leaf',[(14,102),(14+dx*.5,112+dy),(14+dx,102+dy),(14+dx*.4,102+dy*.35)],-54,'#405d48',outline=False)
    rect('Muller wall frame',-554,107,143,151,-54,'#8c623f')
    rect('Muller wall paper',-544,118,123,128,-53,'#eee0bd',outline=False)
    text('club memento','MÜNCHEN',-483,220,-52,16,'#8f303d')
    # Original simple shield drawing, not a raster logo or photograph.
    shape('memento shield',[(-521,192),(-445,192),(-449,143),(-483,128),(-517,143)],-52,'#a43a44',soft=False)
    for i in range(4):shape('shield diamond',[(-510+i*16,174),(-502+i*16,188),(-494+i*16,174),(-502+i*16,160)],-51,'#eee7ce',outline=False,soft=False)
    oval('camera lens housing',-264,327,29,11,-59,'#273247')
    oval('camera lens',-264,327,5,5,-57,'#080e1a')
    oval('camera status',-245,327,2,2,-57,'#8ed1a5')
    shape('Perez chair',[(282,-267),(281,8),(310,40),(510,47),(547,12),(570,-260)],-24,'#263247')
    stroke('chair piping',[(291,-210),(294,4),(320,26),(501,33),(531,6),(549,-210)],-23,'#465367',2)
    # Foreground table masks lower torsos naturally, with depth and light.
    shape('table top',[(-670,-226),(198,-203),(696,-242),(696,-400),(-670,-400)],90,'#b2855e',soft=False)
    shape('table light',[(-640,-234),(191,-214),(635,-245),(210,-264)],91,'#c3986b',outline=False,soft=False)
    stroke('table grain',[(-606,-300),(-232,-270),(111,-269),(565,-311)],92,'#9b7355',1.5)
    shape('notebook shadow',[(129,-289),(278,-247),(466,-266),(303,-312)],93,'#765e51',outline=False,soft=False)
    shape('notebook cover',[(124,-281),(275,-240),(462,-259),(306,-304)],94,'#223346',soft=False)
    shape('notebook paper',[(130,-275),(275,-234),(455,-253),(306,-297)],95,'#f5efdd',soft=False)
    for dy in range(0,25,8):stroke('notes',[(216,-253-dy),(319,-253-dy*.8)],96,'#76818a',.6,soft=False)
    # Mug handle is behind the cup; perspective ellipses share one centre.
    oval('mug handle',559,-265,24,24,95,'#f2e9d3',outline=True)
    oval('mug handle hole',559,-265,15,15,96,'#b2855e')
    shape('mug',[(491,-223),(550,-223),(548,-288),(521,-298),(493,-288)],97,'#ebe2cd',soft=False)
    oval('mug rim',520,-223,30,7,98,'#f6efdf',outline=True)
    oval('coffee',520,-224,24,4,99,'#654536')
    text('mug monogram','RM',520,-259,99,23,'#a17a3c')
    rect('caption band',-640,-360,1280,51,180,'#172534',outline=False)

def make_face(who, parent):
    head=control(who+' head',(0,184,15),parent)
    F[who]={'head':head,'eyes':[],'brows':[],'mouths':{}}
    is_p=who=='Perez'
    if is_p:
        # Broad older face, receding swept silver hair, glasses and projecting nose.
        shape('Perez hair back',[(-51,113),(-53,146),(-31,164),(11,163),(48,146),(64,112),(61,69),(48,49),(32,49)],0,'#6a6b72',head)
        shape('Perez face',[(-38,138),(-15,148),(17,141),(41,113),(43,74),(35,32),(10,5),(-27,11),(-48,28),(-56,55),(-53,98)],3,SKIN,head)
        shape('Perez cheek shade',[(24,127),(40,111),(41,76),(29,43),(1,23),(-30,28),(-40,15),(-24,8),(9,6),(37,33),(46,79)],4,SHADE,head,False)
        shape('Perez forehead light',[(-38,117),(-33,135),(-12,143),(6,137),(-3,123)],4,HI,head,False)
        shape('Perez crown',[(-52,120),(-54,144),(-40,163),(-21,170),(-1,165),(11,163),(32,159),(49,142),(61,118),(59,77),(44,63),(41,94),(26,118),(15,140),(-15,147),(-32,143),(-42,125)],6,'#777981',head)
        for i in range(7):
            stroke('Perez swept hair',[(4+i*5,156-i*2),(27+i*3,141-i*4),(48+i,115-i*5)],7,'#afb0b3',.85,head)
        stroke('Perez hair part',[(-42,144),(-35,158),(-21,161),(-13,153)],7,'#afb0b3',1.4,head)
        shape('Perez ear',[(40,88),(53,96),(63,85),(60,65),(49,51),(38,55)],8,SKIN,head)
        stroke('Perez ear inner',[(45,68),(49,83),(55,84),(55,76),(48,73)],9,'#a0664d',1.2,head)
        eyes=[(-37,97,12,7),(-6,96,15,9)]
    else:
        # Long lean face, prominent ears and nose, uneven swept brown crop.
        shape('Muller back hair',[(-51,119),(-60,149),(-47,174),(-14,187),(17,181),(38,165),(44,125)],0,'#664636',head)
        shape('Muller ear far',[(36,111),(47,118),(53,102),(48,84),(40,79)],1,SKIN,head)
        shape('Muller face',[(-38,151),(-7,164),(25,153),(38,124),(39,88),(33,41),(19,17),(-3,5),(-28,18),(-45,49),(-49,99)],3,SKIN,head)
        shape('Muller jaw shade',[(-44,70),(-29,50),(-6,35),(22,48),(37,66),(30,35),(16,15),(-4,8),(-27,19),(-42,43)],4,SHADE,head,False)
        shape('Muller forehead light',[(-32,140),(-9,151),(18,144),(24,131),(-5,139)],4,HI,head,False)
        shape('Muller cheek light',[(-29,77),(-13,82),(-3,63),(-22,52)],4,'#f7bf87',head,False)
        shape('Muller ear near',[(-46,107),(-62,119),(-71,109),(-66,86),(-50,71),(-40,80)],7,SKIN,head)
        stroke('Muller ear inner',[(-53,87),(-62,99),(-61,107),(-53,102),(-49,92)],8,'#ac7050',1.2,head)
        shape('Muller hair',[(-50,99),(-56,120),(-61,137),(-57,150),(-64,151),(-49,164),(-54,171),(-35,178),(-35,184),(-15,186),(-17,194),(3,187),(18,190),(24,181),(35,178),(31,188),(44,172),(41,155),(45,135),(37,118),(28,149),(16,160),(5,157),(-7,151),(-24,150),(-40,139),(-43,116)],8,'#674632',head,soft=False)
        for pts in [[(-53,152),(-30,165),(-13,163)],[(-32,178),(-8,174),(9,159)],[(-10,185),(10,176),(20,161)],[(20,180),(34,166),(36,144)],[(-52,136),(-37,148),(-25,145)]]:
            stroke('Muller hair locks',pts,9,'#936748',1.5,head)
        eyes=[(-20,112,14,8),(20,115,12,8)]
        for x,y in [(-30,40),(-24,31),(-13,24),(0,21),(14,29),(24,41),(-35,49)]:
            stroke('Muller stubble',[(x,y),(x+2,y+4)],7,'#b17855',.55,head,False)
    for i,(x,y,rx,ry) in enumerate(eyes):
        eye=control(who+' eye '+str(i),(x,y,11),head); F[who]['eyes'].append(eye)
        shape(who+' eyelid',[(-rx,0),(-rx*.55,ry*.85),(rx*.35,ry),(rx,0),(rx*.4,-ry),(-rx*.5,-ry*.7)],0,'#fff6df',eye)
        gaze=control(who+' gaze '+str(i),((-3 if is_p else 4),0,2),eye)
        oval(who+' iris',0,0,4.8,6,0,'#6b624d',gaze); oval(who+' pupil',0,0,2.9,4.7,1,INK,gaze)
        oval(who+' glint',-1,2,1.3,1.3,2,'#ffffff',gaze)
        brow=control(who+' brow '+str(i),(x,y+17,14),head); F[who]['brows'].append(brow)
        shape(who+' brow',[(-rx-2,-1),(-rx*.4,5),(rx*.5,5),(rx+2,-1),(rx*.5,1),(-rx*.5,1)],0,'#565254' if is_p else '#5c3b2a',brow,False)
        stroke(who+' eye crease',[(x-rx,y-12),(x,y-14),(x+rx,y-11)],10,'#af7759',.7,head)
    if is_p:
        for x,y,rx,ry in eyes:
            stroke('Perez glasses',[(x-rx-5,y+10),(x+rx+4,y+10),(x+rx+4,y-10),(x-rx-3,y-12),(x-rx-5,y+10)],16,'#525967',1.1,head)
        stroke('Perez bridge',[(-20,104),(-18,106),(-16,104)],17,'#414957',1.2,head)
        stroke('Perez temple',[(13,103),(45,94),(53,84)],16,'#414957',1.2,head)
        shape('Perez nose',[(-27,106),(-34,91),(-49,74),(-55,66),(-45,62),(-29,66),(-24,72)],18,SKIN,head)
        stroke('Perez nostril',[(-39,65),(-33,67),(-27,66)],19,'#875642',1.1,head)
        stroke('Perez cheek fold',[(-23,62),(-17,54),(-12,38)],19,'#ab7054',.85,head)
        stroke('Perez forehead crease',[(-37,129),(-26,127),(-18,128)],10,'#b57b5b',.6,head)
        mouth_origin=(-28,43,21)
    else:
        shape('Muller nose',[(11,118),(16,105),(24,93),(30,83),(27,77),(15,74),(5,80),(8,87)],18,SKIN,head)
        stroke('Muller nostril',[(12,78),(18,76),(25,78)],19,'#925c43',1.1,head)
        stroke('Muller smile cheek',[(32,74),(37,67),(36,55)],19,'#aa6f51',.9,head)
        mouth_origin=(5,56,21)
    mouth=control(who+' mouth',mouth_origin,head)
    # Complete alternate drawings; no stretching one painted mouth.
    for label,w,h in [('smile',24,10),('rest',18,1),('tight',16,1),('A',19,16),('E',23,9),('O',10,14),('MBP',17,1),('FV',20,4)]:
        group=control(who+' mouth '+label,parent=mouth); F[who]['mouths'][label]=group
        if h==1:
            stroke(who+' '+label,[(-w,0),(-w*.2,2 if label=='rest' else 0),(w,0 if label=='tight' else -1)],0,'#6e4438',1.15,group)
            stroke(who+' lower lip',[(-w*.7,-4),(0,-5),(w*.65,-3)],1,'#b97d5c',.7,group)
        else:
            shape(who+' mouth cavity',[(-w,2),(-w*.3,0),(w,5),(w*.75,-h*.6),(0,-h),(-w*.7,-h*.45)],0,'#53332e',group)
            if label!='O':shape(who+' teeth',[(-w*.87,1),(0,0),(w*.84,4),(w*.6,-h*.28),(0,-h*.42),(-w*.65,-h*.2)],1,'#fff6df',group,False)
            if label in ['A','E']:shape(who+' tongue',[(-w*.4,-h*.6),(0,-h*.55),(w*.4,-h*.5),(w*.4,-h*.74),(0,-h*.85)],2,'#da8c85',group,False)
    return head

def make_arm(who,side,root,lengths,color,z,kind):
    parts=[]
    for label,length,r1,r2 in [('upper',lengths[0],21,17),('fore',lengths[1],17,12)]:
        ob=control(who+' '+side+' '+label,(0,0,z),root)
        parts.append(ob)
    # One connected contour, not two closed overlapping segment silhouettes.
    points=arm_contour((0,150),(-55,75),(-100,100))
    sleeve=shape(who+side+' continuous sleeve',points,z,color,root,False,False)
    edge=stroke(who+side+' sleeve silhouette',points,z+.25,INK,1.1,root,False)
    shade=stroke(who+side+' sleeve fold',[(0,0),(1,0),(2,0)],z+.5,'#ac2d40' if who=='Muller' else '#182238',1,root,False)
    ARM_ART[who+side]=(sleeve,edge,shade)
    hand=control(who+' '+side+' wrist',(0,0,z+4),root)
    if kind=='grip':
        shape('Muller holding palm',[(-12,-5),(-18,7),(-13,22),(-1,28),(14,19),(12,0),(5,-9)],0,SKIN,hand)
        # Picture sits behind wrapping fingers and follows the same grip control.
        rect('picture frame',-5,-16,109,137,-3,'#6c4533',hand)
        rect('picture bevel',1,-10,97,125,-2,'#b18a5f',hand)
        rect('picture paper',7,-4,85,113,-1,'#fff0cc',hand,False)
        text('eight two','8 – 2',50,66,0,29,INK,hand)
        text('twenty twenty','2020',50,28,0,17,INK,hand)
        for y in [18,9,0]:
            shape('wrapped picture finger',[(-12,y),(-9,y+8),(6,y+9),(13,y+6),(11,y+1),(2,y+3),(-5,y-2)],2,SKIN,hand)
        shape('picture thumb',[(-8,18),(-7,29),(0,37),(7,35),(4,26),(2,17)],3,HI,hand)
    elif kind=='pen':
        rect('white shirt cuff',-14,-6,27,17,0,'#cdddec',hand)
        shape('Perez pen hand',[(-12,2),(-18,16),(-12,34),(-2,38),(16,30),(19,16),(11,10),(10,1)],1,SKIN,hand)
        stroke('pen',[(-4,44),(26,-3)],2,'#172837',3,hand,False)
        stroke('pen shine',[(-3,42),(12,20)],3,'#a5b9c5',.7,hand,False)
        for y in [26,18]:stroke('folded fingers',[(-11,y),(1,y+2),(10,y-3),(9,y-8)],4,'#a1684f',.9,hand)
        shape('pen thumb',[(-14,16),(-9,24),(4,24),(10,18),(5,12),(-3,15)],5,SKIN,hand)
    else:
        rect(who+' wrist cuff',-14,-5,28,13,0,'#cdddec' if who=='Perez' else '#d53b49',hand)
        shape(who+' resting hand',[(-12,7),(-8,19),(6,22),(21,15),(35,8),(35,2),(26,0),(14,5),(25,-1),(23,-6),(10,-3),(-6,-3)],1,SKIN,hand)
        stroke(who+' resting fingers',[(3,12),(12,11),(27,4)],2,'#a1684f',.8,hand)
        if who=='Perez':hand.location.z=105
    ARMS[who+side]=(parts,hand,lengths)

def cast():
    for who,loc,scale in [('Muller',(-305,-203,-40),1.23),('Perez',(365,-230,0),1.38)]:
        root=control(who+' root',loc); root.scale=(scale,)*3
        chest=control(who+' chest',(0,0,0),root)
        C[who+' chest']=chest
        color='#d53b49' if who=='Muller' else '#28364c'
        shape(who+' torso',[(-69,-20),(-80,28),(-78,103),(-90,153),(-52,178),(-19,185),(26,181),(75,161),(84,135),(69,67),(71,-20)],7,color,chest)
        shape(who+' torso shade',[(-75,128),(-61,75),(-60,11),(-17,-13),(-64,-16),(-74,30)],8,'#b62d43' if who=='Muller' else '#1b283c',chest,False)
        shape(who+' neck',[(-24,209),(-22,169),(-3,150),(28,169),(29,207)],9,SKIN,chest)
        shape(who+' neck shade',[(-21,204),(12,186),(28,194),(27,204)],10,SHADE,chest,False)
        if who=='Muller':
            stroke('red collar',[(-29,176),(-3,152),(32,176)],12,INK,2,chest)
            stroke('collar piping',[(-30,181),(-3,158),(32,181)],12,'#f6e5cd',1,chest)
            for side in [-1,1]:
                shape('Bayern scarf',[(side*28,183),(side*40,173),(side*47,83),(side*44,2),(side*18,-6),(side*27,87)],14,'#b9223d',chest)
                for y in [27,73,121]:shape('scarf white stripe',[(side*24,y),(side*45,y+6),(side*46,y+19),(side*26,y+13)],15,'#fff0df',chest,False,False)
            text('Bayern scarf name','FCB',-33,102,16,12,'#fff0df',chest)
            for side in [-1,1]:stroke('shirt shoulder piping',[(side*52,173),(side*71,162),(side*83,146)],12,'#efc9c5',1.8,chest)
        else:
            shape('Perez shirt',[(-32,179),(-4,154),(33,177),(27,20),(-30,20)],11,'#d3e0eb',chest,False)
            shape('Perez collar left',[(-28,181),(-4,154),(-18,137),(-35,160)],12,'#e7edf0',chest,soft=False)
            shape('Perez collar right',[(28,181),(-4,154),(12,137),(36,159)],12,'#e7edf0',chest,soft=False)
            shape('Perez tie',[(-10,151),(4,151),(8,137),(0,128),(-10,138)],13,'#28374e',chest,soft=False)
            shape('Perez tie tail',[(-4,130),(2,130),(14,29),(0,14),(-12,30)],13,'#29384e',chest,soft=False)
            shape('Perez lapel left',[(-40,173),(-16,125),(-26,112),(-10,101),(-8,2),(-60,99)],14,'#35445c',chest,soft=False)
            shape('Perez lapel right',[(39,169),(23,125),(32,111),(16,98),(4,2),(62,106)],14,'#35445c',chest,soft=False)
            stroke('suit pocket',[(36,71),(59,75)],15,'#101c30',1.3,chest)
        make_face(who,chest)
        make_arm(who,'L',root,(89,91),color,2,'grip' if who=='Muller' else 'pen')
        make_arm(who,'R',root,(90,93),color,18,'rest')
    # Muller remains inside the monitor: bottom bezel masks the desk/call edge.
    rect('call desk',-581,-197,656,23,25,'#9b704b',outline=False)
    rect('monitor lower bevel',-594,-219,682,22,27,'#263448',outline=False)
    text('call name','THOMAS MÜLLER · BAYERN LEGEND',-268,-207,29,12,'#d2dce5')

def interp(f,keys):
    if f<=keys[0][0]:return keys[0][1]
    for (a,x),(z,y) in zip(keys,keys[1:]):
        if f<=z:
            t=(f-a)/(z-a);t=t*t*(3-2*t)
            if isinstance(x,(tuple,list)):return tuple(u+(v-u)*t for u,v in zip(x,y))
            return x+(y-x)*t
    return keys[-1][1]

def key(ob,prop,f):ob.keyframe_insert(data_path=prop,frame=f)

def arm_contour(shoulder,elbow,wrist):
    a,e,w=map(Vector,(shoulder,elbow,wrist));u=(e-a).normalized();v=(w-e).normalized()
    n=Vector((-u.y,u.x));m=Vector((-v.y,v.x));bis=(n+m).normalized()
    points=[]
    for sign in [1,-1]:
        row=[a+n*21*sign,a.lerp(e,.48)+n*19*sign,e+bis*17*sign,e.lerp(w,.57)+m*15*sign,w+m*12*sign]
        points.extend(row if sign==1 else reversed(row))
    # Open contour ends at the shoulder; the torso covers that join.
    return smooth([tuple(p) for p in points],False)

def show_mouth(who,label,f):
    for name,group in F[who]['mouths'].items():
        for ob in group.children_recursive:
            ob.hide_render=ob.hide_viewport=name!=label
            key(ob,'hide_render',f);key(ob,'hide_viewport',f)

def set_arm(who,side,shoulder,wrist,pole,hand_angle,f):
    parts,hand,lengths=ARMS[who+side]
    elbow=two_bone_joint(shoulder,wrist,lengths,pole)
    for ob,a,z in zip(parts,[shoulder,elbow],[elbow,wrist]):
        ob.location.x,ob.location.y=a
        ob.rotation_euler.z=math.atan2(z[0]-a[0],-(z[1]-a[1]))
        key(ob,'location',f);key(ob,'rotation_euler',f)
    hand.location.x,hand.location.y=wrist;hand.rotation_euler.z=math.radians(hand_angle)
    key(hand,'location',f);key(hand,'rotation_euler',f)
    sleeve,edge,fold=ARM_ART[who+side]
    points=arm_contour(shoulder,elbow,wrist)
    for vertex,point in zip(sleeve.data.vertices,points):
        vertex.co.x,vertex.co.y=point;vertex.keyframe_insert(data_path='co',frame=f)
    for vertex,point in zip(edge.data.splines[0].points,points):
        vertex.co.x,vertex.co.y=point;vertex.keyframe_insert(data_path='co',frame=f)
    e=Vector(elbow);a=Vector(shoulder);w=Vector(wrist);v=(w-e).normalized();n=Vector((-v.y,v.x))
    for vertex,point in zip(fold.data.splines[0].points,[e+n*11+v*9,e+v*15,e-n*9+v*8]):
        vertex.co.x,vertex.co.y=point;vertex.keyframe_insert(data_path='co',frame=f)

def animate():
    # Measured voice takes: Muller 2.96 s, Perez 3.44 s. Word timing is provisional.
    m_ph=[(1,'smile'),(26,'E'),(31,'A'),(35,'rest'),(38,'O'),(45,'O'),(49,'rest'),(61,'A'),(65,'FV'),(70,'E'),(77,'O'),(83,'A'),(89,'E'),(95,'smile'),(156,'tight')]
    p_ph=[(1,'rest'),(114,'O'),(122,'rest'),(132,'A'),(139,'O'),(145,'E'),(151,'O'),(156,'FV'),(161,'E'),(166,'O'),(174,'E'),(180,'A'),(186,'O'),(193,'A'),(196,'rest')]
    for f in range(1,241):
        s.frame_set(f)
        for who in ['Muller','Perez']:
            p=who=='Perez';chest=C[who+' chest']; head=F[who]['head']
            angle=interp(f,[(1,0),(24,0),(48,-1),(84,0),(145,0),(173,1.8),(205,2.7)]) if not p else interp(f,[(1,1),(105,1),(116,-1.3),(148,-2.8),(198,-2.8),(219,-1.5)])
            chest.rotation_euler.z=math.radians(angle);key(chest,'rotation_euler',f)
            hangle=interp(f,[(1,-3),(21,-3),(35,-7),(49,-3),(75,-5),(103,-3),(150,-3),(156,0),(174,1.5),(197,3)]) if not p else interp(f,[(1,0),(101,0),(117,3),(127,0),(151,1),(185,1),(209,-2)])
            head.rotation_euler.z=math.radians(hangle);key(head,'rotation_euler',f)
            # Gaze moves before the head/prop, with one motivated blink each.
            gaze=interp(f,[(1,4),(145,4),(152,0),(174,0),(203,-2)]) if not p else interp(f,[(1,-3),(116,-4),(194,-4),(214,-2)])
            blink=interp(f,[(1,1),(100,1),(102,.08),(105,1),(240,1)]) if not p else interp(f,[(1,1),(72,1),(74,.08),(77,1),(240,1)])
            for i,eye in enumerate(F[who]['eyes']):
                eye.scale.y=blink; key(eye,'scale',f)
                ob=C[who+' gaze '+str(i)];ob.location.x=gaze;key(ob,'location',f)
                brow=F[who]['brows'][i]
                brow.rotation_euler.z=math.radians(interp(f,[(1,(-7 if i==0 else 8)),(143,(-7 if i==0 else 8)),(160,(8 if i==0 else -11)),(240,(8 if i==0 else -11))]) if not p else interp(f,[(1,(12 if i==0 else -10)),(112,(12 if i==0 else -10)),(150,(17 if i==0 else -15)),(240,(17 if i==0 else -15))]))
                key(brow,'rotation_euler',f)
            def shoulder(x):
                a=math.radians(angle);return (x*math.cos(a)-151*math.sin(a),x*math.sin(a)+151*math.cos(a))
            if not p:
                wrist=interp(f,[(1,(-132,140)),(23,(-132,140)),(41,(-140,151)),(90,(-134,144)),(163,(-134,144)),(192,(-150,93)),(214,(-163,56))])
                set_arm(who,'L',shoulder(-70),wrist,(-100,-100),interp(f,[(1,5),(41,0),(163,0),(207,13)]),f)
                set_arm(who,'R',shoulder(70),(31,15),(141,7),170,f)
            else:
                wrist=interp(f,[(1,(-100,121)),(109,(-100,121)),(137,(-132,126)),(175,(-130,131)),(198,(-110,115)),(220,(-100,121))])
                set_arm(who,'L',shoulder(-70),wrist,(-145,-2),interp(f,[(1,18),(110,18),(140,-8),(181,-8),(220,18)]),f)
                set_arm(who,'R',shoulder(70),(-2,9),(137,16),170,f)
        for who,ph in [('Muller',m_ph),('Perez',p_ph)]:
            label=next(label for start,label in reversed(ph) if start<=f)
            # Replacement visibility only keys at changes, so editing remains legible.
            if f==1 or any(start==f for start,_ in ph):show_mouth(who,label,f)
    # Baked articulated transforms use linear interpolation; the authored ease is above.
    for action in bpy.data.actions:
        if not action.name.startswith('C3 /'):continue
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for fc in bag.fcurves:
                        for k in fc.keyframe_points:k.interpolation='CONSTANT' if 'hide_' in fc.data_path else 'LINEAR'
    for start,end,words in [(25,96,'MÜLLER: Eight goals. A very good night.'),(113,198,'PÉREZ: Good. How do we stop Flick doing that to us?')]:
        ob=text('subtitle',words,0,-334,181,22,'#f5efdf')
        for frame,visible in [(1,False),(start,True),(end,False)]:
            ob.hide_render=ob.hide_viewport=not visible;key(ob,'hide_render',frame);key(ob,'hide_viewport',frame)
    s.frame_set(48)

def check():
    # Tests actual saved motion: fixed limb lengths and grip attachment each frame.
    max_error=0
    for f in range(1,241):
        s.frame_set(f);bpy.context.view_layer.update()
        for parts,hand,lengths in ARMS.values():
            for ob,length,target in [(parts[0],lengths[0],parts[1]),(parts[1],lengths[1],hand)]:
                end=ob.matrix_world @ Vector((0,-length,0)); point=target.matrix_world.translation
                max_error=max(max_error,math.hypot(end.x-point.x,end.y-point.y))
        for who in F:
            active=[name for name,g in F[who]['mouths'].items() if any(not ob.hide_render for ob in g.children_recursive)]
            assert len(active)==1,(f,who,active)
    assert max_error<.001,max_error
    assert not any(n.type=='TEX_IMAGE' for ob in col.objects if ob.type in ['MESH','CURVE'] for m in ob.data.materials if m and m.use_nodes for n in m.node_tree.nodes)
    s.frame_set(48)
    return {'limb_endpoint_max_error_drawing_units':max_error,'one_mouth_per_character_per_frame':True,'raster_character_materials':False,'frames_checked':240,'creative_approval':False,'lip_sync':'Provisional authored phonemes; not yet listened/approved'}

def build():
    setup();room();cast();animate()
    import json
    (O/'native-check.json').write_text(json.dumps(check(),indent=2))
    bpy.ops.wm.save_as_mainfile(filepath=str(O/'call-performance.blend'))
    return {'scene':s.name,'objects':len(col.objects),'native':str(O/'call-performance.blend')}

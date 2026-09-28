"""Native cast artwork, individually drawn from the selected character designs.
Run in the visible Blender instance after batch01 v009 construction.
Facial parts, clothing and footwear are editable geometry; acting controls stay.
"""
import bpy, math, json
from pathlib import Path
from mathutils import Vector
V=Path(__file__).resolve().parents[1];O=V/'artifacts/batch01-v010';O.mkdir(exist_ok=True)
n=bpy.app.driver_namespace['samtoons_batch01'];b=n['b'];INK='#202129'

def face(a):
 n['use'](a['scene'],a['col']);C=a['C'];h=C['head'];prefix=a['prefix'];kind=a['kind'];assert kind in ['arteta','gyokeres']
 # Keep the viseme animation and independent eye/brow controls; replace generic geometry.
 keep=set(C['mouth'].children_recursive)
 for ob in list(h.children_recursive):
  if ob.type in ['MESH','CURVE','FONT'] and ob not in keep:bpy.data.objects.remove(ob,do_unlink=True)
 art=kind=='arteta';ox,oy,k=(1074,283,1.02) if art else (373,203,.93)
 def points(pts):return [((x-ox)*k,(oy-y)*k) for x,y in pts]
 def sh(label,pts,c,z=5,edge=True,soft=True):return n['poly'](prefix+'identity '+label,points(pts),c,z,h,edge,.9,soft)
 def ln(label,pts,c=INK,z=10,w=.65):return n['line'](prefix+'identity '+label,points(pts),c,z,w,h,True)
 skin='#ffbe83';shadow='#e7a56f';light='#ffce95';hair='#191d20' if art else '#755632';a['skin']=skin
 if art:
  sh('face',[(1043,180),(1061,161),(1091,150),(1112,155),(1123,171),(1128,191),(1131,214),(1138,227),(1137,238),(1144,251),(1144,265),(1134,273),(1111,279),(1080,276),(1063,268),(1055,252),(1040,243),(1025,226),(1028,199)],skin,4)
  sh('temple plane',[(1050,186),(1055,205),(1050,225),(1058,244),(1070,253),(1074,269),(1060,262),(1047,246),(1031,235),(1025,221),(1036,209)],shadow,5,False)
  sh('cheek light',[(1083,224),(1096,221),(1103,230),(1096,240),(1081,247),(1070,240)],light,5,False)
  sh('ear',[(1046,231),(1037,223),(1025,224),(1021,233),(1026,247),(1039,256),(1052,258),(1058,248)],skin,8)
  ln('ear fold',[(1047,245),(1040,230),(1029,229),(1028,237),(1035,244)],'#ad714e',9,.8)
  ln('ear bowl',[(1038,235),(1038,241),(1044,244)],'#ad714e',9,.6)
  sh('beard plane',[(1055,238),(1066,247),(1077,251),(1088,242),(1098,236),(1112,234),(1128,237),(1135,246),(1141,247),(1143,265),(1133,272),(1113,278),(1082,274),(1066,264),(1060,254)],'#a9825d',6,False)
  sh('muzzle',[(1094,237),(1107,232),(1127,233),(1136,238),(1137,249),(1125,256),(1107,255),(1093,249)],skin,7,False)
  sh('chin light',[(1093,258),(1111,261),(1134,256),(1136,264),(1126,268),(1108,270),(1093,266)],'#bc9569',7,False)
  sh('jaw edge',[(1062,250),(1074,265),(1094,270),(1115,274),(1135,267),(1143,259),(1143,267),(1133,274),(1113,280),(1080,276),(1067,268)],'#35362f',7,False)
  sh('hair silhouette',[(1054,231),(1045,220),(1038,219),(1024,223),(1016,217),(1007,199),(1002,184),(1002,173),(1007,158),(1013,155),(1016,147),(1027,143),(1032,138),(1044,138),(1050,131),(1065,132),(1073,127),(1086,130),(1093,126),(1101,131),(1109,131),(1117,138),(1121,148),(1119,156),(1108,160),(1098,156),(1084,161),(1069,164),(1060,175),(1059,188),(1053,203),(1051,218)],hair,10)
  locks=[([(1010,177),(1019,159),(1041,147),(1027,165),(1016,182)],'#2a2d2e'), ([(1025,163),(1044,143),(1068,137),(1058,147),(1036,157)],'#383a3a'), ([(1044,148),(1071,132),(1095,137),(1075,139),(1058,150)],'#303334'), ([(1060,145),(1084,133),(1107,140),(1114,150),(1094,143),(1076,147)],'#424344'), ([(1010,192),(1020,177),(1032,171),(1025,184),(1017,204)],'#2c3031'), ([(1021,211),(1029,193),(1042,181),(1037,199),(1031,216)],'#25292a'), ([(1037,174),(1052,157),(1074,150),(1061,162),(1048,171)],'#353839')]
  for i,(p,c) in enumerate(locks):sh('hair lock '+str(i),p,c,11,False)
  paths=[[(1013,169),(1023,155),(1040,146)],[(1020,182),(1031,170),(1043,164)],[(1032,155),(1051,143),(1066,139)],[(1048,146),(1068,133),(1084,134)],[(1071,140),(1089,134),(1101,138)],[(1094,143),(1107,144),(1114,152)],[(1033,193),(1041,180),(1050,174)],[(1024,206),(1032,199),(1035,190)],[(1013,195),(1018,190),(1020,184)],[(1056,155),(1067,151),(1081,150)]]
  for i,p in enumerate(paths):ln('hair direction '+str(i),p,'#4a4b4b' if i%3==0 else '#0f1418',12,.65)
  ln('nose bridge',[(1120,202),(1122,214),(1128,224),(1134,228),(1135,232),(1129,235),(1119,234)],'#664735',19,.8)
  ln('nose underside',[(1115,229),(1119,226),(1124,228)],'#966544',19,.65)
  ln('nose shine',[(1124,219),(1128,224)],'#ffdaa5',19,.8)
  ln('mouth fold',[(1098,232),(1093,237),(1093,245)],'#805b40',19,.65)
  ln('smile crease',[(1136,235),(1139,241),(1138,247)],'#805b40',19,.5)
  ln('forehead',[(1080,184),(1093,184),(1104,180)],'#c78c5e',14,.5)
  ln('brow furrow',[(1110,178),(1114,187),(1113,193)],'#ad7752',14,.65)
  eyes=[('L',(1093,209),[(1079,214),(1084,204),(1095,200),(1103,204),(1101,214),(1092,219),(1084,218)],(1096,209)),('R',(1124,199),[(1117,202),(1118,195),(1124,191),(1128,195),(1128,202),(1123,207),(1119,207)],(1126,199))]
  brows=[('L',(1092,193),[(1074,205),(1080,192),(1091,188),(1107,189),(1105,196),(1091,196),(1081,200)]),('R',(1123,183),[(1114,191),(1117,183),(1123,179),(1128,184),(1127,190),(1123,186),(1118,189)])]
  mouth=(1117,247);C['mouth'].scale=(.52,.61,1)
  stubble_regions=[(1064,250,1083,263),(1080,263,1095,271),(1096,266,1134,271),(1136,249,1140,263)]
 else:
  sh('face',[(329,76),(350,58),(387,50),(410,49),(423,62),(426,83),(431,101),(432,119),(438,134),(432,146),(436,166),(435,181),(425,193),(409,202),(388,200),(366,190),(350,176),(336,154),(324,135),(316,112)],skin,4)
  sh('temple plane',[(329,84),(338,93),(340,119),(349,137),(348,154),(359,176),(351,174),(339,155),(326,145),(321,124)],shadow,5,False)
  sh('forehead light',[(351,83),(365,67),(391,64),(408,67),(416,78),(405,81),(389,75),(372,81)],light,5,False)
  sh('cheek plane',[(374,134),(384,125),(395,131),(391,144),(382,151),(370,145)],'#ffc78d',5,False)
  sh('ear',[(338,130),(325,122),(315,124),(307,130),(310,146),(321,157),(336,163),(345,155)],skin,8)
  ln('ear fold',[(335,151),(329,133),(318,131),(314,136),(320,145)],'#a26b48',9,.85)
  ln('ear bowl',[(326,137),(327,146),(334,150)],'#a26b48',9,.65)
  sh('beard plane',[(344,139),(352,150),(365,163),(382,164),(390,150),(401,143),(421,142),(432,150),(434,177),(426,190),(410,199),(390,197),(370,187),(355,174),(348,157)],'#bb9462',6,False)
  sh('muzzle',[(391,150),(401,147),(423,147),(432,155),(431,169),(421,178),(400,178),(386,165)],skin,7,False)
  sh('chin light',[(391,184),(407,182),(425,178),(424,188),(411,195),(397,191)],'#d4ad74',7,False)
  sh('beard jaw edge',[(351,165),(367,182),(389,192),(409,197),(428,186),(434,174),(434,185),(424,196),(410,204),(388,201),(367,189),(356,179)],'#625338',7,False)
  sh('hair fade',[(301,94),(318,87),(341,88),(343,112),(336,126),(326,122),(317,123),(310,120)],'#a28054',9,False)
  sh('hair silhouette',[(308,123),(296,111),(287,96),(283,80),(286,66),(295,49),(310,36),(326,28),(342,24),(336,21),(366,20),(380,16),(399,17),(410,24),(416,37),(417,50),(410,58),(397,57),(381,62),(364,67),(344,72),(335,80),(338,91),(327,99),(315,105)],'#60482e',10)
  locks=[([(289,84),(296,67),(317,52),(347,46),(367,52),(344,55),(318,66),(301,79)],'#ad8450'), ([(293,65),(303,47),(324,34),(353,29),(378,37),(385,48),(368,41),(345,36),(322,45),(306,58)],'#bd945b'), ([(311,40),(334,27),(361,24),(387,30),(399,42),(400,54),(390,50),(383,38),(361,31),(338,32)],'#b98c53'), ([(351,27),(373,18),(392,20),(407,31),(410,47),(406,53),(400,38),(386,28),(369,27)],'#c59a60'), ([(285,91),(301,78),(324,68),(349,66),(335,78),(315,83),(300,92),(293,108)],'#a37b49'), ([(302,94),(318,85),(333,81),(328,90),(315,99),(308,112)],'#86653e')]
  for i,(p,c) in enumerate(locks):sh('quiff lock '+str(i),p,c,11,False)
  paths=[[(290,77),(310,57),(339,49),(356,50)],[(299,61),(319,42),(349,36),(369,42)],[(321,38),(346,28),(370,29),(389,44)],[(353,23),(376,19),(397,28),(405,45)],[(385,20),(401,25),(412,40)],[(290,89),(313,73),(332,68),(348,68)],[(304,93),(318,85),(329,84)],[(301,105),(311,95),(322,91)],[(314,52),(336,44),(356,43),(372,50)],[(333,32),(352,27),(370,30)]]
  for i,p in enumerate(paths):ln('quiff sweep '+str(i),p,'#342c22' if i%2 else '#dfb77b',12,.8)
  for i in range(11):
   xx=308+(i%6)*4;yy=102+(i//6)*6;ln('fade texture '+str(i),[(xx,yy),(xx+4,yy-4)],'#896b47',11,.4)
  ln('nose bridge',[(415,107),(418,121),(425,131),(426,136),(419,140),(410,138)],'#72503a',19,.85)
  ln('nose wing',[(403,139),(401,135),(406,131),(411,132)],'#aa704b',19,.65)
  ln('bridge light',[(419,119),(422,128)],'#ffdfaa',19,.8)
  ln('mouth fold',[(393,148),(387,153),(385,164)],'#936940',19,.65)
  ln('far mouth crease',[(430,149),(433,158),(432,169)],'#936940',19,.6)
  ln('forehead furrow',[(393,81),(400,91),(400,99)],'#b68153',14,.7)
  ln('forehead line',[(399,77),(406,87),(407,96)],'#cc9464',14,.5)
  eyes=[('L',(382,117),[(367,123),(371,113),(384,108),(395,109),(391,121),(381,127),(372,127)],(386,116)),('R',(421,106),[(412,110),(413,101),(421,97),(428,99),(428,109),(422,115),(417,115)],(423,106))]
  brows=[('L',(380,105),[(356,118),(364,105),(379,101),(397,98),(395,107),(380,110),(366,111)]),('R',(420,91),[(409,100),(412,90),(423,84),(431,88),(432,94),(424,92),(417,95)])]
  mouth=(412,163);C['mouth'].scale=(.57,.68,1)
  stubble_regions=[(350,151,366,168),(365,169,381,184),(380,185,396,193),(404,186,424,193),(428,161,432,181)]
 # Individual eyes retain their animation controls and actual per-character spacing.
 for side,centre,contour,pupil in eyes:
  e=a['eyes'][side];e.location=(*points([centre])[0],14)
  local=[((x-centre[0])*k,(centre[1]-y)*k) for x,y in contour]
  n['poly'](prefix+'identity '+side+' eye',local,'#fff9e6',0,e,True,.75,True)
  gaze=C[side+' gaze'];gaze.location=((pupil[0]-centre[0])*k,(centre[1]-pupil[1])*k,1)
  n['ellipse'](prefix+'identity '+side+' iris',0,0,3.8*k,5.3*k,'#605849',0,gaze)
  n['ellipse'](prefix+'identity '+side+' pupil',.35,0,2.25*k,4.15*k,'#161c20',.2,gaze)
  n['ellipse'](prefix+'identity '+side+' glint',-.7,1.9,1.1,1.35,'#fffef1',.3,gaze)
  n['line'](prefix+'identity '+side+' eyelid',local[:4],INK,.5,.85,e,True)
 for side,centre,contour in brows:
  ob=a['brows'][side];ob.location=(*points([centre])[0],16)
  local=[((x-centre[0])*k,(centre[1]-y)*k) for x,y in contour]
  n['poly'](prefix+'identity '+side+' brow',local,hair,0,ob,False,soft=True)
 C['mouth'].location=(*points([mouth])[0],23)
 # Restrained stipple follows jaw planes, not a solid painted-on beard.
 for r,(x0,y0,x1,y1) in enumerate(stubble_regions):
  for j in range(3):
   for i in range(max(1,int((x1-x0)/3))):
    xx=x0+2+i*3+(j%2);yy=y0+1+(y1-y0-3)*j/2
    ln('stubble %s %s %s'%(r,j,i),[(xx,yy),(xx+.5,yy+1.7)],'#876b48' if not art else '#786347',8,.27)
 a['identity_revision']='v010 / individually traced native features'
 return {'actor':a['name'],'native_head':True}

def details(a):
 n['use'](a['scene'],a['col']);C=a['C'];p=a['prefix'];gy=a['kind']=='gyokeres';art=a['kind']=='arteta';assert gy or art
 def sh(name,pts,col,z,par,edge=False,soft=True):return n['poly'](p+'finish '+name,pts,col,z,par,edge,.9,soft)
 def ln(name,pts,col,z,par,w=.65):return n['line'](p+'finish '+name,pts,col,z,w,par,True)
 ch=C['chest'];hip=C['pelvis']
 # Distinct drape, seams and hems on the connected garment, without a second outlined chest.
 if art:
  for name in ['shirt fold','shirt fold.001','shirt left shade','shirt side light']:
   ob=bpy.data.objects.get(p+name)
   if ob:ob.hide_render=ob.hide_viewport=True
  sh('jumper left plane',[(-57,162),(-51,143),(-51,108),(-56,67),(-50,34),(-34,20),(-2,17),(-26,9),(-54,13),(-63,32),(-62,67)],'#171e2c',6,ch)
  sh('jumper right light',[(52,151),(54,117),(60,82),(54,44),(36,27),(12,24),(32,37),(44,65),(44,109)],'#293344',6,ch)
  for i,pts in enumerate([[(-57,132),(-41,119),(-27,99),(-38,111),(-53,117)],[(-52,68),(-36,49),(-13,42),(-36,47),(-53,57)],[(-38,31),(-4,22),(25,27),(3,15),(-19,20)],[(53,36),(42,21),(19,14),(42,15),(58,26)]]):sh('jumper fold '+str(i),pts,'#111a27',7,ch)
  for side,sign in [('L',-1),('R',1)]:
   ln(side+' shoulder stitching',[(sign*30,197),(sign*49,187),(sign*60,177)],'#3f4858',8,ch,.6)
   hand=C[side+' hand'];sh(side+' cuff',[(-13,11),(13,11),(14,-1),(-13,-1)],'#171e2b',6,hand)
   for x in [-8,-3,3,8]:ln(side+' cuff rib '+str(x),[(x,9),(x,0)],'#303b4c',7,hand,.45)
   thigh=C[side+' thigh'];shin=C[side+' shin']
   sh(side+' trouser fold',[(-12,-11),(-9,-31),(3,-43),(-5,-28)],'#101a2a',1,thigh)
   ln(side+' knee crease',[(-13,-97),(-3,-90),(10,-94)],'#111b2b',1,thigh,.7)
   sh(side+' shin fold',[(-13,-75),(-6,-85),(11,-92),(-4,-88)],'#111b2b',1,shin)
   ln(side+' trouser hem',[(-17,-101),(0,-104),(17,-101)],'#0e1826',1.2,shin,.8)
  ln('trouser pocket',[(-48,-9),(-44,-25),(-31,-35)],'#0e1826',8,hip,.8)
 else:
  for label in ['shirt mark','sponsor','sponsor small','jersey fold','jersey shade']:
   ob=bpy.data.objects.get(p+label)
   if ob:ob.hide_render=ob.hide_viewport=True
  for ob in list(a['col'].objects):
   if 'crest' in ob.name and ob.type in ['MESH','CURVE','FONT']:ob.hide_render=ob.hide_viewport=True
  # Full shirt collar surrounds neck and reads as a sewn trim.
  ln('red collar edge',[(-30,199),(-26,181),(-10,172),(7,174),(26,189),(29,199)],'#981a2a',10,ch,3.4)
  ln('white collar',[(-30,199),(-26,183),(-10,175),(7,177),(26,191),(29,199)],'#fff9eb',11,ch,2)
  sh('jersey ribcage shade',[(-53,154),(-48,127),(-51,90),(-33,53),(-11,39),(-35,47),(-54,79)],'#b4112b',6,ch)
  sh('jersey right light',[(52,153),(48,116),(55,71),(49,33),(24,16),(52,26),(61,61)],'#ed3044',6,ch)
  sh('jersey lower fold',[(-50,38),(-29,22),(4,18),(38,29),(20,15),(-10,11),(-36,23)],'#ac142a',7,ch)
  ln('shirt hem',[(-58,0),(-25,-6),(13,-5),(58,2)],'#a4162b',8,ch,.8)
  n['text'](p+'finish sponsor','Emirates',0,115,25,'#fff9f0',11,ch);n['text'](p+'finish sponsor small','FLY BETTER',0,94,10,'#fff9f0',11,ch)
  def adidas(name,x,y,par,sc=1,z=11):
   for i in range(3):sh(name+str(i),[(x+sc*(i*6-8),y),(x+sc*(i*6-3),y+sc*3),(x+sc*(i*6-8-i*3),y+sc*(10+i*5)),(x+sc*(i*6-13-i*3),y+sc*(7+i*5))],'#fffdf5',z,par,False,False)
  adidas('shirt adidas',-29,151,ch,.7)
  def crest(name,x,y,par,sc,z=12):
   sh(name+'shield',[(x+sc*dx,y+sc*dy) for dx,dy in [(-12,14),(12,14),(12,0),(8,-10),(0,-16),(-8,-10),(-12,0)]],'#e8b755',z,par,True)
   sh(name+'inside',[(x+sc*dx,y+sc*dy) for dx,dy in [(-10,12),(10,12),(10,0),(6,-8),(0,-12),(-6,-8),(-10,0)]],'#ba1d31',z+.1,par)
   n['ellipse'](p+'finish '+name+'wheel',x,y-2*sc,4*sc,4*sc,'#eec45e',z+.2,par)
   ln(name+'cannon',[(x-8*sc,y+sc),(x+9*sc,y+sc)],'#f6d379',z+.4,par,1.1*sc)
   ln(name+'band',[(x-9*sc,y+9*sc),(x+9*sc,y+9*sc)],'#fff0c2',z+.4,par,.7*sc)
  crest('shirt crest',35,158,ch,.62)
  crest('shorts crest',-34,-24,hip,.42,9)
  for side,sign in [('L',-1),('R',1)]:
   up=C[side+' upper arm'];thigh=C[side+' thigh'];shin=C[side+' shin']
   for i in range(3):ln(side+' shoulder stripe '+str(i),[(sign*(-8+i*5),6),(sign*(-11+i*5),-13),(sign*(-8+i*5),-41)],'#d21a33',3,up,.9)
   ln(side+' sleeve cuff',[(-19,-49),(0,-52),(19,-48)],'#c11630',3,up,2.2)
   ln(side+' sleeve fold',[(-13,-32),(-3,-35),(10,-32)],'#a8b0be',3,up,.7)
   sh(side+' shorts fold',[(-18,-17),(-8,-37),(8,-46),(-3,-36)],'#d1d3db',1,thigh)
   ln(side+' shorts hem',[(-24,-69),(-3,-73),(23,-67)],'#798493',1.3,thigh,.65)
   for j in range(2):ln(side+' shorts side stripe '+str(j),[(sign*(22-j*4),-12),(sign*(21-j*4),-40),(sign*(21-j*4),-64)],'#d92037',2,thigh,.85)
   ln(side+' knee anatomy',[(-9,-88),(-3,-96),(7,-99)],'#bd865d',2,thigh,.65)
   for yy in [-31,-37]:ln(side+' sock band '+str(yy),[(-19,yy),(0,yy-1),(19,yy)],'#fffaf1',2,shin,1.45)
   adidas(side+' sock mark',3,-66,shin,.54,3)
 # Shoes retain the original ankle origin and sole contact at y=-22.
 for side,sign in [('L',-1),('R',1)]:
  boot=C[side+' boot']
  for ob in list(boot.children_recursive):
   if ob.type in ['MESH','CURVE']:bpy.data.objects.remove(ob,do_unlink=True)
  def shp(label,pts,color,z=1,edge=False):return sh(side+' '+label,[(x*sign,y) for x,y in pts],color,z,boot,edge)
  def lin(label,pts,color,z=3,w=.65):return ln(side+' '+label,[(x*sign,y) for x,y in pts],color,z,boot,w)
  shp('shoe silhouette',[(-23,13),(-24,0),(-26,-11),(-22,-19),(-9,-22),(31,-22),(45,-17),(46,-11),(37,-4),(19,1),(14,13)],'#fff3da' if gy else '#253043',1,True)
  shp('outer sole',[(-25,-11),(-11,-15),(13,-15),(36,-12),(45,-10),(45,-17),(31,-22),(-9,-22),(-22,-19)],'#e14149' if gy else '#f5f0dd',1.5,True)
  shp('sole light',[(-23,-15),(-8,-18),(20,-18),(42,-14),(31,-19),(-8,-20)],'#f9e6cb' if gy else '#fffceb',1.8)
  shp('heel panel',[(-22,11),(-8,9),(-7,-2),(-14,-9),(-24,-7)],'#eee4d0' if gy else '#151f30',2)
  shp('shoe upper light',[(-6,7),(10,6),(23,-3),(38,-8),(22,-10),(5,-4),(-11,-5)],'#fff9e8' if gy else '#344258',2)
  shp('tongue',[(-11,12),(8,11),(17,-1),(5,-5),(-12,2)],'#e9decc' if gy else '#192437',2.2)
  lin('toe stitching',[(18,-1),(23,-8),(37,-11),(44,-10)],'#bea992' if gy else '#0d1728',3,.6)
  lin('heel stitching',[(-19,8),(-19,-4),(-10,-9)],'#b7aa97' if gy else '#526072',3,.65)
  for j in range(4):lin('lace '+str(j),[(-9+j*3,8-j*3),(3+j*3,6-j*3)],'#b6aa96' if gy else '#adb4b7',3.2,.65)
  if gy:
   shp('boot red flash',[(1,-9),(11,-13),(35,-9),(22,-15),(8,-17)],'#e83142',2.9)
   for xx in [-17,10,30]:shp('stud '+str(xx),[(xx-2,-21),(xx-2,-25),(xx+3,-25),(xx+5,-21)],'#902b34',1,True)
  else:
   for j in range(3):shp('trainer stripe '+str(j),[(j*7-5,2),(j*7,-1),(j*7-6,-11),(j*7-10,-9)],'#d8ddd9',3)
   lin('sole break',[(-2,-17),(8,-19),(21,-17)],'#677080',2.5,.55)
 # Palm lines and warm skin match the individual head, including articulated fingers.
 for ob in a['col'].objects:
  if ob.type=='MESH' and (' hand ' in ob.name or ' palm' in ob.name):
   for i,m in enumerate(ob.data.materials):
    if m and m.diffuse_color[0]>.4:ob.data.materials[i]=b['mat']('#ffbe83')
 for side in ['L','R']:
  ln(side+' palm line',[(-7,-12),(-8,-20),(-2,-28)],'#b57d53',3,C[side+' hand'],.6)
  ln(side+' heart line',[(-10,-9),(0,-12),(8,-9)],'#c98c5e',3,C[side+' hand'],.5)
 return {'actor':a['name'],'clothing_and_shoes':'v010'}

def apply(name):
 a=n['ACTORS'][name];face(a);details(a);n['room']['show'](a['scene']);a['scene'].frame_set(226 if 'opening' in name else 315)
 return {'finished':name}

# Every current and future named character needs its own silhouette/feature decisions.
# Rig reuse is allowed; generic face geometry is not a likeness source.

def hands(a):
 n['use'](a['scene'],a['col']);C=a['C'];p=a['prefix']
 # Reuse v008's tapered fingers and rounded palm; keep the wrist/finger pivots.
 for side in ['L','R']:
  h=C[side+' hand'];parts=[h,C[side+' hand thumb']]+[C[side+' hand finger '+str(i)] for i in range(4)]
  for par in parts:
   for ob in list(par.children):
    if ob.type in ['MESH','CURVE'] and not ob.name.startswith(p+'finish '+side+' cuff'):bpy.data.objects.remove(ob,do_unlink=True)
  def sh(name,pts,c,par,z=0,edge=True):return n['poly'](p+'finish '+side+' '+name,pts,c,z,par,edge,.8,True)
  def ln(name,pts,c,par,z=2,w=.55):return n['line'](p+'finish '+side+' '+name,pts,c,z,w,par,True)
  sh('palm',[(-11,5),(-16,-4),(-18,-13),(-15,-28),(-9,-34),(3,-36),(12,-31),(16,-22),(14,-7),(10,4)],'#ffbe83',h)
  sh('palm shade',[(-14,-6),(-16,-17),(-12,-29),(-5,-33),(3,-29),(-3,-19),(-5,-10)],'#e0a270',h,.7,False)
  ln('palm crease',[(-7,-12),(-8,-21),(-4,-29)],'#b57d53',h)
  ln('palm heart crease',[(-10,-10),(-1,-13),(7,-10),(10,-14)],'#c68d60',h)
  th=C[side+' hand thumb'];sh('thumb',[(-3,4),(-10,1),(-16,-6),(-21,-12),(-21,-16),(-17,-18),(-12,-15),(-7,-10),(2,-6),(5,0)],'#ffbe83',th)
  ln('thumb crease',[(-11,-8),(-8,-9),(-5,-11)],'#b57d53',th)
  for i,(length,width,bend) in enumerate([(28,4.8,-1.5),(34,5.,1),(31,4.6,2.1),(23,3.8,3)]):
   f=C[side+' hand finger '+str(i)]
   sh('finger '+str(i),[(-width,3),(-width-1,-8),(-width+.2+bend*.4,-length*.65),(-width+1.5+bend,-length+2),(-.5+bend,-length),(width-1+bend,-length+1),(width+bend,-length+5),(width+.2,-length*.55),(width,3)],'#ffbe83',f)
   ln('knuckle '+str(i),[(-width*.7+bend*.2,-length*.48),(-.2+bend*.2,-length*.51),(width*.55+bend*.2,-length*.48)],'#bf865b',f,.8,.45)
 # The phone remains attached to the original hand control and was not rebuilt.
 return {'hands':a['name']}

def finish_contacts():
 s=n['SCENES']['opening'];n['use'](s);w=n['ACTORS']['banner worker'];root=w['root'];root.animation_data_clear();root.scale=(4.1/604,)*3;root.location=(5.9,-2.9,1)
 s.frame_set(54);bpy.context.view_layer.update();banner=n['PROPS']['banner'];year=n['PROPS']['year'];tip=w['C']['L hand'].matrix_world@Vector((0,-43,2));wanted=banner.matrix_world@Vector((1.2,1.05,1.05));root.location+=Vector((wanted.x-tip.x,wanted.y-tip.y,0));bpy.context.view_layer.update()
 year.animation_data_clear()
 for f in range(1,150):
  s.frame_set(f);bpy.context.view_layer.update()
  if f<54:loc=Vector((.2,.65,.8));theta=0
  elif f<=64:
   grip=banner.matrix_world.inverted()@(w['C']['L hand'].matrix_world@Vector((0,-43,2)));theta=-.018*(f-54);off=Vector((math.cos(theta)-.4*math.sin(theta),math.sin(theta)+.4*math.cos(theta)));loc=Vector((grip.x-off.x,grip.y-off.y,1.05));released=loc.copy()
  else:
   t=f-64;theta=-.18-.025*t;loc=released+Vector((.024*t,-.0028*t*t,0))
  year.location=loc;year.rotation_euler.z=theta;year.keyframe_insert(data_path='location',frame=f);year.keyframe_insert(data_path='rotation_euler',frame=f)
 n['expose'](root,1,149,409)
 # Ladder belongs to the banner setup and leaves at the truck cut.
 for o in list(s.objects):
  if o.name.startswith('Worker ladder'):bpy.data.objects.remove(o,do_unlink=True)
 ladder=n['ctrl']('B01 worker ladder');xx,yy=root.location.x,root.location.y
 for dx in [-.47,.47]:n['line']('Worker ladder rail',[(xx+dx,-2.9),(xx+dx,yy+.1)],'#526774',-.3,.04,ladder)
 for i in range(7):
  y=-2.8+i*(yy+2.8)/6;n['line']('Worker ladder rung',[(xx-.5,y),(xx+.5,y)],'#b7c3c5',-.2,.04,ladder)
 n['expose'](ladder,1,149,409)
 # The year gag needs the complete worker and coach within the frame.
 cam=next(m.camera for m in s.timeline_markers if m.frame==49);cam.location.x=.5;cam.location.y=1.0;cam.data.ortho_scale=16.6
 # Gyokeres leads the lateral travel with the near/right foot; feet never cross.
 a=n['ACTORS']['unveiling Gyokeres'];s=a['scene'];n['use'](s);samples={}
 for f in range(1,433):
  row={}
  for side,start,end,first,last in [('R',55,155,53,76),('L',-55,65,82,105)]:
   u=max(0,min(1,(f-first)/(last-first)));row[side]=(start+(end-start)*(u*u*(3-2*u)),22+27*math.sin(math.pi*u))
  samples[f]=row
 a['foot_samples']=samples
 n['key'](a['C']['pelvis'],'location',[(56,(4,232,0)),(78,(39,232,0))])
 # Reuse the authored acting rows; only the support targets have changed.
 import ast
 fn=next(x for x in ast.parse(Path(n['__file__']).read_text()).body if isinstance(x,ast.FunctionDef) and x.name=='unveiling')
 call=next(x.value for x in fn.body if isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name) and x.value.func.id=='pose')
 rows=ast.literal_eval(call.args[1]);n['pose'](a,rows)
 # Copy current controls into only the existing leg surfaces; upper garment stays intact.
 old={o.name:o for o in a['col'].objects if o.type=='MESH' and o.data.shape_keys and ' leg ' in o.name}
 for o in old.values():bpy.data.objects.remove(o,do_unlink=True)
 # Bake in a temporary collection, then keep only its leg surfaces (same shared baker).
 saved=a['col'];temp=bpy.data.collections.new('B01 temporary leg bake');s.collection.children.link(temp);a['col']=temp
 n['bake_clothes'](a);a['col']=saved
 for o in list(temp.objects):
  if ' leg ' in o.name:
   saved.objects.link(o);temp.objects.unlink(o)
  else:bpy.data.objects.remove(o,do_unlink=True)
 bpy.data.collections.remove(temp)
 n['use'](s);return {'year_contact':'grip then released falling card','walk':'right step, left follow, fixed support'}

def supporting_finish():
 for name in ['banner worker','delivery driver']:
  a=n['ACTORS'][name];n['use'](a['scene'],a['col']);C=a['C'];p=a['prefix'];driver=a['kind']=='driver';ch=C['chest'];color='#cea247' if driver else '#566c7a'
  for sign in [-1,1]:
   n['poly'](p+'finish collar '+str(sign),[(sign*28,199),(0,180),(sign*14,167),(sign*37,185)],color,11,ch,True,.7,True)
  n['line'](p+'finish placket',[(0,180),(0,127)],'#8e742f' if driver else '#30475a',12,.8,ch)
  for yy in [171,155,140]:n['ellipse'](p+'finish button',0,yy,1.6,1.6,'#f7e7bb' if driver else '#becbd3',12.2,ch)
  for xx in [-45,14]:
   n['line'](p+'finish pocket',[(xx,116),(xx,88),(xx+28,84),(xx+28,116)],'#a88637' if driver else '#4a606f',11,.75,ch)
   n['line'](p+'finish pocket stitch',[(xx,112),(xx+28,112)],'#f0cb70' if driver else '#a3adb1',11.2,.5,ch)
 # The striker cannot already be listening before his arrival; preserve the unused asset offscreen.
 a=n['ACTORS']['preseason player'];a['root'].animation_data_clear();a['root'].scale=(0,0,0)
 for side in ['L','R']:
  boot=n['ACTORS']['unveiling Gyokeres']['C'][side+' boot']
  for ob in boot.children:
   if ob.type in ['MESH','CURVE']:ob.location.y+=3
 return {'supporting_cast':'collars, pockets, buttons; remove premature striker duplicate'}

def save():
 manifest=[];rows=json.loads((V/'artifacts/animation-v003/edit.json').read_text())[:10]
 for group,s in n['SCENES'].items():
  s.name=s.name.replace('v009','v010');s['status']='Batch 1 rough animation and cast refinement; user review pending'
  seq=s.sequence_editor_create();offset={'narrator':0,'opening':180,'unveiling':589}[group]
  for strip in list(seq.strips):
   if strip.name.startswith('Approved batch mix'):seq.strips.remove(strip)
  strip=seq.strips.new_sound('Approved batch mix',str(V/'artifacts/opening-v002/mix-premaster.wav'),channel=1,frame_start=1-offset);strip.frame_offset_start=offset;strip.frame_final_duration=s.frame_end
 for row in rows:
  group='narrator' if row['id']=='N01' else 'opening' if row['start_frame']<590 else 'unveiling';offset={'narrator':0,'opening':180,'unveiling':589}[group]
  manifest.append({**row,'scene':n['SCENES'][group].name,'local_start':row['start_frame']-offset})
 (O/'edit.json').write_text(json.dumps(manifest,indent=2)+'\n')
 n['room']['show'](n['SCENES']['unveiling']);n['SCENES']['unveiling'].frame_set(315)
 bpy.ops.wm.save_as_mainfile(filepath=str(O/'batch01-native-v010.blend'))
 return {'blend':bpy.data.filepath,'frames':1021,'seconds':1021/24}

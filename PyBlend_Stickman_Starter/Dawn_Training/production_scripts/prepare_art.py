"""Reference pixels -> named vector artwork; no generated replacement character."""
from pathlib import Path
import json, hashlib, shutil, xml.etree.ElementTree as ET
import cv2 as cv
import numpy as np
from PIL import Image
import vtracer
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/dawn_training'
for p in ['references','geometry','review','stages','frames']:(OUT/p).mkdir(parents=True,exist_ok=True)
for n in ['im-1.png','im_2.png','im_3.png','im_4.png','im_5.png']:
 shutil.copy2(Path('/Users/samikd/Desktop')/n,OUT/'references'/n)
P={}
def box(x0,y0,x1,y1):return [[x0,y0],[x1,y0],[x1,y1],[x0,y1]]
def part(name,poly,pivot,parent='torso',tip=None):return dict(name=name,poly=poly,pivot=pivot,parent=parent,tip=tip or [pivot[0],pivot[1]-25])
def pose(name,src,crop,anchor,height,parts):P[name]=dict(source=src,crop=crop,anchor=anchor,height=height,parts=parts)
# Polygons are explicit semantic ownership authored against the supplied model sheets.
pose('FRONT','im-1.png',[55,70,353,811],[207,798],7.0,[
 part('torso',box(115,311,293,431),[207,426],'root',[207,335]),
 part('upper_arm.L',[[113,328],[138,338],[148,379],[126,417],[95,426],[94,383]],[124,351],'torso',[111,414]),
 part('upper_arm.R',[[272,329],[295,339],[314,388],[315,431],[286,421],[265,376]],[284,354],'torso',[300,416]),
 part('forearm.L',[[95,405],[128,414],[106,476],[76,489],[68,466]],[110,413],'upper_arm.L',[82,480]),
 part('forearm.R',[[286,407],[313,405],[340,464],[338,490],[307,486]],[300,413],'upper_arm.R',[326,481]),
 part('wristband.L',box(60,463,108,502),[81,479],'forearm.L'),part('wristband.R',box(302,464,345,502),[327,480],'forearm.R'),
 part('hand.L',box(56,495,102,567),[81,499],'forearm.L',[77,539]),part('hand.R',box(308,495,353,568),[328,499],'forearm.R',[333,540]),
 part('pants.L',box(80,451,209,706),[177,457],'root',[136,700]),part('pants.R',box(207,451,334,710),[237,457],'root',[282,700]),
 part('shin.L',box(95,696,160,754),[135,699],'pants.L',[127,752]),part('shin.R',box(252,698,312,756),[279,700],'pants.R',[283,752]),
 part('foot.L',box(60,748,157,811),[127,752],'shin.L',[99,784]),part('foot.R',box(261,749,354,811),[283,752],'shin.R',[316,785]),
 part('sash',box(137,422,264,460),[207,441],'root'),
 part('sash_tail',[[148,437],[168,448],[144,510],[153,620],[129,628],[111,604],[97,622],[73,614],[92,555],[115,478]],[153,443],'sash',[119,605]),
 part('head',[[137,216],[271,216],[286,279],[265,311],[239,320],[243,345],[170,345],[171,316],[138,298],[128,269]],[207,335],'torso',[207,261]),
 part('hair',[[85,65],[330,65],[336,239],[277,279],[270,272],[267,252],[262,253],[262,239],[255,224],[243,220],[228,226],[207,245],[188,230],[170,221],[160,224],[151,235],[148,253],[144,259],[138,257],[134,270],[135,283],[95,268]],[207,260],'head',[207, 98]),
])
pose('BACK','im-1.png',[947,70,1241,811],[1097,798],7.0,[
 part('torso',box(1009,305,1194,425),[1102,423],'root',[1102,322]),
 part('head',box(1067,276,1140,323),[1102,320],'torso'),part('hair',box(979,65,1224,295),[1102,282],'head'),
 part('upper_arm.L',box(995,329,1048,425),[1024,349],'torso',[1014,411]),part('forearm.L',box(974,401,1033,480),[1014,411],'upper_arm.L',[990,477]),part('hand.L',box(960,472,1006,566),[987,484],'forearm.L'),
 part('upper_arm.R',box(1163,330,1210,425),[1184,350],'torso',[1195,411]),part('forearm.R',box(1180,400,1233,480),[1195,411],'upper_arm.R',[1219,479]),part('hand.R',box(1200,469,1241,563),[1219,484],'forearm.R'),
 part('pants.L',box(973,449,1101,711),[1070,452],'root',[1038,703]),part('pants.R',box(1097,449,1210,711),[1136,452],'root',[1167,703]),
 part('shin.L',box(1002,699,1067,758),[1038,704],'pants.L'),part('shin.R',box(1133,699,1197,759),[1167,704],'pants.R'),
 part('foot.L',box(948,750,1068,811),[1036,752],'shin.L'),part('foot.R',box(1137,750,1230,811),[1168,752],'shin.R'),
 part('sash',box(1044,417,1156,461),[1101,442],'root'),part('sash_tail',[[1147,440],[1165,449],[1183,503],[1208,596],[1185,601],[1170,578],[1144,502]],[1150,445],'sash'),
])
pose('RUN','im_3.png',[704,173,1002,666],[850,655],6.4,[
 part('torso',box(814,293,968,410),[877,392],'root',[890,321]),
 part('pants.L',[[807,401],[899,401],[867,474],[804,550],[775,591],[733,580],[745,528],[762,477]],[849,410],'root',[764,568]),
 part('pants.R',[[876,404],[927,409],[953,440],[945,477],[909,510],[868,497],[819,470],[829,431]],[878,424],'root',[914,464]),
 part('shin.L',box(725,557,784,620),[762,568],'pants.L',[739,608]),part('foot.L',box(704,601,754,666),[739,608],'shin.L'),
 part('shin.R',box(816,479,875,535),[851,491],'pants.R',[830,520]),part('foot.R',box(783,511,838,577),[830,520],'shin.R'),
 part('upper_arm.L',[[781,291],[824,292],[859,313],[855,346],[822,342],[794,323]],[836,320],'torso',[789,307]),
 part('forearm.L',[[781,293],[803,310],[780,347],[765,363],[739,347],[750,318]],[784,310],'upper_arm.L',[752,347]),
 part('hand.L',box(726,338,771,387),[752,347],'forearm.L'),
 part('upper_arm.R',[[930,327],[952,336],[964,363],[974,390],[955,400],[934,378],[928,356]],[942,342],'torso',[958,386]),
 part('forearm.R',box(949,354,988,405),[962,387],'upper_arm.R',[973,365]),part('hand.R',box(956,339,998,378),[974,365],'forearm.R'),
 part('sash',box(829,385,932,420),[877,401],'root'),part('sash_tail',[[850,389],[836,417],[785,448],[752,463],[737,428],[757,414],[751,402],[795,393]],[851,402],'sash'),
 part('head',[[907,263],[951,263],[982,308],[978,338],[958,344],[940,327],[917,322],[906,292]],[924,320],'torso'),
 part('hair',[[830,166],[988,166],[990,287],[976,318],[968,295],[951,279],[944,272],[928,272],[919,282],[915,303],[911,315],[878,295],[855,265]],[925,285],'head'),
])
pose('CROUCH','im_3.png',[935,320,1238,696],[1080,682],5.0,[
 part('torso',box(1010,464,1146,563),[1086,550],'root',[1070,505]),
 part('pants.L',[[995,544],[1077,545],[1077,613],[1049,669],[980,670],[962,643],[976,588]],[1069,557],'root',[989,637]),
 part('pants.R',[[1088,545],[1134,510],[1170,506],[1200,529],[1188,578],[1164,620],[1130,612],[1092,590]],[1100,558],'root',[1161,558]),
 part('shin.R',box(1134,598,1183,653),[1157,611],'pants.R'),part('foot.R',box(1126,643,1192,691),[1154,651],'shin.R'),
 part('upper_arm.R',box(1124,430,1200,470),[1138,450],'torso',[1184,452]),part('forearm.R',box(1178,449,1220,480),[1184,452],'upper_arm.R'),part('hand.R',box(1200,461,1237,498),[1210,474],'forearm.R'),
 part('upper_arm.L',[[1012,500],[1049,500],[1062,536],[1050,576],[1031,590],[1008,563]],[1031,521],'torso',[1036,572]),
 part('forearm.L',box(1010,565,1057,655),[1036,571],'upper_arm.L',[1041,643]),part('hand.L',box(1003,645,1093,695),[1041,648],'forearm.L'),
 part('sash',box(1050,535,1144,565),[1090,550],'root'),part('sash_tail',[[1051,543],[1065,554],[1015,577],[969,602],[975,573],[1004,554]],[1059,547],'sash'),
 part('head',[[1020,448],[1128,440],[1137,484],[1109,528],[1083,541],[1041,516],[1015,478]],[1085,533],'torso'),
 part('hair',[[988,321],[1166,321],[1174,444],[1135,482],[1129,468],[1118,462],[1109,456],[1092,465],[1073,477],[1057,465],[1044,457],[1035,459],[1026,470],[1017,470],[1000,451]],[1077,475],'head'),
])
pose('POWER','im_3.png',[1189,205,1448,688],[1327,674],6.7,[
 part('torso',box(1241,329,1386,425),[1324,416],'root',[1321,349]),
 part('upper_arm.L',box(1218,337,1283,402),[1262,357],'torso',[1241,394]),part('forearm.L',box(1195,383,1258,435),[1241,395],'upper_arm.L',[1215,400]),part('hand.L',box(1190,364,1234,412),[1215,400],'forearm.L'),
 part('upper_arm.R',box(1363,339,1410,405),[1377,357],'torso',[1388,400]),part('forearm.R',box(1381,389,1435,432),[1388,400],'upper_arm.R',[1422,402]),part('hand.R',box(1410,366,1448,415),[1422,402],'forearm.R'),
 part('pants.L',box(1238,425,1328,610),[1291,433],'root',[1272,604]),part('pants.R',box(1325,425,1433,610),[1352,433],'root',[1395,602]),
 part('shin.L',box(1247,595,1290,650),[1272,601],'pants.L'),part('shin.R',box(1380,596,1426,650),[1400,601],'pants.R'),
 part('foot.L',box(1212,641,1291,688),[1263,645],'shin.L'),part('foot.R',box(1390,640,1448,688),[1409,645],'shin.R'),
 part('sash',box(1269,407,1375,446),[1324,426],'root'),part('sash_tail',[[1278,423],[1295,438],[1261,506],[1225,500],[1246,457]],[1291,429],'sash'),
 part('head',[[1250,252],[1361,252],[1391,303],[1381,329],[1349,353],[1311,358],[1272,331],[1249,298]],[1322,350],'torso'),
 part('hair',[[1209,202],[1386,202],[1399,279],[1382,313],[1375,294],[1353,274],[1326,260],[1307,258],[1295,271],[1292,287],[1279,290],[1268,305],[1238,293]],[1313,280],'head'),
])
pose('SIT','im_3.png',[229,232,477,682],[352,672],5.7,[
 part('torso',box(287,375,433,471),[357,459],'root',[358,399]),
 part('pants.L',box(231,467,355,589),[325,481],'root',[270,530]),part('pants.R',box(352,467,476,596),[393,481],'root',[442,533]),
 part('shin.L',box(251,570,299,637),[277,579],'pants.L'),part('shin.R',box(416,572,460,640),[437,582],'pants.R'),
 part('foot.L',box(229,623,298,669),[272,628],'shin.L'),part('foot.R',box(412,628,477,682),[437,635],'shin.R'),
 part('upper_arm.L',box(276,381,324,464),[305,397],'torso',[299,453]),part('forearm.L',box(288,451,350,500),[299,453],'upper_arm.L'),part('hand.L',box(317,479,361,524),[340,484],'forearm.L'),
 part('upper_arm.R',box(396,380,447,466),[420,399],'torso',[420,457]),part('forearm.R',box(366,452,430,501),[420,457],'upper_arm.R'),part('hand.R',box(340,480,387,524),[368,490],'forearm.R'),
 part('sash',box(320,447,402,480),[357,461],'root'),
 part('head',box(293,339,417,415),[359,410],'torso'),
 part('hair',[[259,230],[429,230],[437,335],[411,370],[407,358],[397,348],[386,345],[371,356],[354,365],[340,351],[327,344],[316,347],[309,360],[299,358],[286,349]],[357,366],'head'),
])
# Power-up articulation follows the actual shoulder and elbow landmarks.
for part_cfg in P['POWER']['parts']:
 n=part_cfg['name']
 if n=='upper_arm.L':part_cfg['tip']=[1253,415]
 if n=='forearm.L':part_cfg.update(poly=box(1195,392,1272,438),pivot=[1253,415],tip=[1215,400])
 if n=='upper_arm.R':part_cfg.update(pivot=[1370,367],tip=[1384,416])
 if n=='forearm.R':part_cfg.update(poly=box(1367,393,1438,440),pivot=[1384,416],tip=[1422,402])

# High-resolution expression drawing, same front view. Includes separate eyes/brows/mouth.
pose('FOCUS','im_2.png',[23,112,333,431],[178,427],4.8,[
 part('torso',box(20,350,335,432),[178,428],'root',[178,370]),part('head',box(76,233,283,402),[178,395],'torso'),
 part('hair',[[25,109],[332,109],[335,306],[275,333],[270,316],[263,309],[254,318],[244,332],[240,304],[250,283],[248,268],[239,247],[226,239],[211,244],[190,260],[178,269],[160,254],[140,243],[128,238],[116,246],[110,261],[105,274],[107,285],[117,298],[118,321],[108,332],[92,327],[59,296]],[178,278],'head'),
])
# Facial artwork is assigned last, so movement exposes authored flat skin below it.
face_specs={'FRONT':([207,335],[[156,262,198,289],[216,262,252,289]],[[154,249,199,274],[214,249,255,274]],[193,301,219,308]),'FOCUS':([178,395],[[122,292,173,324],[181,292,239,324]],[[115,276,172,305],[184,276,244,305]],[160,341,195,350])}
for name,(_,eyes,brows,mouth) in face_specs.items():
 for k,b in enumerate(eyes):P[name]['parts'].append(part('eyes.'+('L' if k==0 else 'R'),box(*b),[(b[0]+b[2])/2,(b[1]+b[3])/2],'head'))
 for k,b in enumerate(brows):P[name]['parts'].append(part('eyebrow.'+('L' if k==0 else 'R'),box(*b),[(b[0]+b[2])/2,(b[1]+b[3])/2],'head'))
 P[name]['parts'].append(part('mouth',box(*mouth),[(mouth[0]+mouth[2])/2,(mouth[1]+mouth[3])/2],'head'))

def silhouette(im,crop,name):
 hsv=cv.cvtColor(im,cv.COLOR_RGB2HSV)
 ink=((hsv[:,:,2]<155)|(hsv[:,:,1]>45)).astype(np.uint8)*255
 ink=cv.morphologyEx(ink,cv.MORPH_CLOSE,np.ones((3,3),np.uint8))
 contours,_=cv.findContours(ink,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
 mask=np.zeros(ink.shape,np.uint8)
 if name=='SIT':
  # Exclude the grey seat, which is environment rather than character artwork.
  pass
 cv.drawContours(mask,[max(contours,key=cv.contourArea)],-1,255,-1)
 return mask
ET.register_namespace('','http://www.w3.org/2000/svg')
ns='{http://www.w3.org/2000/svg}'
manifest={}
for name,config in P.items():
 x0,y0,x1,y1=config['crop'];W=x1-x0;H=y1-y0
 rgb=np.asarray(Image.open(OUT/'references'/config['source']).convert('RGB'))[y0:y1,x0:x1].copy()
 mask=silhouette(rgb,config['crop'],name)
 labels=np.zeros((H,W),np.int16)
 for i,p in enumerate(config['parts'],1):
  pm=np.zeros((H,W),np.uint8);poly=np.asarray(p['poly'],np.int32)-[x0,y0]
  cv.fillPoly(pm,[poly],255)
  if p['name'].startswith('eyes.'):
   # Isolate the entire eye white and pupil, keeping skin under its replacement.
   hsv=cv.cvtColor(rgb,cv.COLOR_RGB2HSV)
   eye=((hsv[:,:,1]<45)&(hsv[:,:,2]>165)&(pm>0)).astype(np.uint8)*255
   cs,_=cv.findContours(eye,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
   pm[:]=0
   if cs:
    cv.drawContours(pm,[cv.convexHull(max(cs,key=cv.contourArea))],-1,255,-1)
    pm=cv.dilate(pm,np.ones((3,3),np.uint8))
  elif p['name'].startswith('eyebrow.'):
   dark=(np.max(rgb,axis=2)<135)&(pm>0)
   # Eyes were claimed first. Their whites and pupils must disappear as one part on a blink.
   for eid,ep in enumerate(config['parts'],1):
    if ep['name'].startswith('eyes.'):dark &= labels!=eid
   pm=dark.astype(np.uint8)*255
  elif p['name']=='mouth':
   pm=((np.max(rgb,axis=2)<165)&(pm>0)).astype(np.uint8)*255
  labels[pm>0]=i
 # Drop the sitting stone and action lines outside explicit owned artwork.
 if name in ['SIT','CROUCH']:mask[labels==0]=0
 # Unassigned silhouette is torso unless explicit non-character matter.
 labels[(mask>0)&(labels==0)]=1
 Image.fromarray(np.dstack([rgb,mask])).save(OUT/'review'/f'{name}_source.png')
 svg=ET.Element(ns+'svg',width=f'{W}px',height=f'{H}px',viewBox=f'0 0 {W} {H}')
 counts={}
 for i,p in enumerate(config['parts'],1):
  selected=(labels==i)&(mask>0)
  if p['name']=='torso':
   nc,cl,stats,_=cv.connectedComponentsWithStats(selected.astype(np.uint8),8)
   if nc>1:selected=cl==(1+int(np.argmax(stats[1:,cv.CC_STAT_AREA])))
  if selected.sum()<3:continue
  # A narrow underlap copies boundary colors under the adjacent drawing.
  sm=selected if p['name'].startswith(('eyes.','eyebrow.','mouth')) else cv.dilate(selected.astype(np.uint8),np.ones((2,2),np.uint8)).astype(bool)&(mask>0)
  trace=np.zeros_like(rgb);trace[:]=[0,255,0];trace[sm]=rgb[sm]
  tmp=OUT/'geometry'/'trace_input.png'
  hi=np.asarray(Image.fromarray(rgb).resize((W*3,H*3),Image.Resampling.LANCZOS)).copy()
  hi_mask=np.asarray(Image.fromarray(sm.astype(np.uint8)*255).resize((W*3,H*3),Image.Resampling.NEAREST))>0
  hi[~hi_mask]=[0,255,0];Image.fromarray(hi).save(tmp)
  ts=OUT/'geometry'/'trace_part.svg'
  vtracer.convert_image_to_svg_py(str(tmp),str(ts),colormode='color',hierarchical='cutout',mode='spline',filter_speckle=4,color_precision=6,layer_difference=12,corner_threshold=60,length_threshold=2.5,splice_threshold=45,path_precision=3)
  tree=ET.parse(ts);g=ET.SubElement(svg,ns+'g',id=p['name']);count=0
  for elem in tree.getroot():
   fill=elem.get('fill','')
   if not fill.startswith('#'):continue
   r,gg,b=(int(fill[j:j+2],16) for j in [1,3,5])
   if gg>190 and r<90 and b<90:continue
   # Preserve the trace's draw order; each Semantic Part is one named layer.
   elem.set('transform','scale(0.3333333333) '+elem.get('transform',''));g.append(elem);count+=1
  counts[p['name']]=count
 path=OUT/'geometry'/f'{name}.svg';ET.ElementTree(svg).write(path,encoding='utf-8',xml_declaration=True)
 manifest[name]={**config,'svg':str(path),'part_paths':counts,'source_sha256':hashlib.sha256((OUT/'references'/config['source']).read_bytes()).hexdigest()}
 print(name,sum(counts.values()),'paths',len(counts),'parts',flush=True)
(OUT/'geometry'/'characters.json').write_text(json.dumps(manifest,indent=2))
for f in ['trace_input.png','trace_part.svg']:(OUT/'geometry'/f).unlink(missing_ok=True)

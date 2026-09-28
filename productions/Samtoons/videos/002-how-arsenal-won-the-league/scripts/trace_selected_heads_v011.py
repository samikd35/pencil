"""Convert selected illustration contours to native editable vector data.
No new illustration is generated and no raster plane is used in the character.
Runtime: PYTHONPATH=.runtime/vector-art ~/Models/qwen-voice/.venv/bin/python
"""
from pathlib import Path
from PIL import Image,ImageDraw
import vtracer,json,xml.etree.ElementTree as ET,re,hashlib
V=Path(__file__).resolve().parents[1];O=V/'assets/native-contours-v011';O.mkdir(exist_ok=True)
source=V/'artifacts/visual-treatment-v001/gyokeres-arteta.png';im=Image.open(source).convert('RGBA')
# Source landmarks are in the unmodified approved image, not guessed native proportions.
DESIGNS={
'arteta':{'origin':[1074,283],'scale':1.02,'bounds':[989,119,1151,285],
'outline':[(1053,230),(1045,222),(1035,222),(1026,224),(1021,231),(1024,245),(1037,255),(1055,262),(1063,271),(1080,278),(1111,282),(1135,277),(1146,268),(1147,254),(1141,242),(1141,227),(1134,214),(1131,194),(1129,177),(1125,161),(1124,149),(1121,138),(1112,130),(1102,129),(1093,124),(1084,128),(1073,124),(1063,130),(1050,129),(1042,136),(1031,136),(1025,141),(1014,146),(1011,152),(1004,158),(1000,175),(1001,190),(1009,211),(1018,222),(1031,228),(1042,229)],
'eyes':[{'center':[1093,209],'outline':[(1079,215),(1083,205),(1095,200),(1103,202),(1105,209),(1098,217),(1089,220),(1081,219)]},{'center':[1125,200],'outline':[(1117,204),(1117,195),(1123,190),(1128,191),(1130,197),(1128,205),(1123,208),(1119,208)]}],
'mouth_center':[1117,245],'mouth_outline':[(1095,240),(1104,239),(1119,238),(1134,234),(1136,239),(1126,244),(1110,247),(1099,245)],'skin':'#ffc28a','neck_top':[[-22,33],[42,10]]},
'gyokeres':{'origin':[373,203],'scale':.93,'bounds':[277,8,443,209],
'outline':[(309,125),(304,133),(307,145),(319,158),(335,166),(345,178),(364,190),(388,203),(410,207),(427,198),(437,185),(438,169),(435,148),(441,136),(436,120),(434,103),(430,87),(429,75),(423,60),(421,45),(418,29),(408,17),(395,12),(382,12),(367,17),(337,19),(341,23),(325,25),(309,33),(293,48),(284,65),(280,79),(284,96),(295,115)],
'eyes':[{'center':[381,117],'outline':[(366,122),(372,113),(384,108),(397,106),(397,113),(391,122),(382,128),(371,129)]},{'center':[421,106],'outline':[(411,111),(412,102),(421,95),(429,97),(431,104),(429,112),(423,117),(416,116)]}],
'mouth_center':[412,162],'mouth_outline':[(397,155),(406,150),(420,149),(426,153),(429,166),(419,169),(409,170),(397,175),(394,169)],'skin':'#ffc38b','neck_top':[[-33,46],[40,8]]}}

def convert(mask):
 rgba=im.copy();rgba.putalpha(mask)
 svg=vtracer.convert_pixels_to_svg(list(rgba.getdata()),rgba.size,colormode='color',hierarchical='stacked',mode='spline',filter_speckle=2,color_precision=6,layer_difference=18,corner_threshold=60,length_threshold=1.5,path_precision=2)
 rows=[]
 for el in ET.fromstring(svg):
  if el.tag.split('}')[-1]!='path':continue
  commands=re.findall(r'[MCLZmclz]|-?\d+(?:\.\d+)?',el.attrib['d']);paths=[];path=[];i=0
  while i<len(commands):
   c=commands[i];i+=1
   if c.upper()=='M':
    if path:paths.append(path)
    path=[[float(commands[i]),float(commands[i+1])]];i+=2
   elif c.upper()=='L':path.append([float(commands[i]),float(commands[i+1])]);i+=2
   elif c.upper()=='C':
    p0=path[-1];p1=[float(commands[i]),float(commands[i+1])];p2=[float(commands[i+2]),float(commands[i+3])];p3=[float(commands[i+4]),float(commands[i+5])];i+=6
    count=max(3,int(sum(((u[0]-v[0])**2+(u[1]-v[1])**2)**.5 for u,v in [(p0,p1),(p1,p2),(p2,p3)])/2))
    for j in range(1,count+1):
     t=j/count;path.append([(1-t)**3*p0[d]+3*(1-t)**2*t*p1[d]+3*(1-t)*t*t*p2[d]+t**3*p3[d] for d in [0,1]])
   elif c.upper()=='Z':
    if path:paths.append(path);path=[]
   else:raise ValueError(c)
  if path:paths.append(path)
  tr=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?',el.attrib.get('transform',''))];tx,ty=tr[:2] if tr else (0,0)
  rows.append({'color':el.attrib['fill'],'paths':[[[x+tx,y+ty] for x,y in points] for points in paths if len(points)>2]})
 return rows

for who,cfg in DESIGNS.items():
 mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon(cfg['outline'],fill=255)
 # Preserve the source geometry; native eyes/mouth get their own editable parts.
 parts={}
 for i,eye in enumerate(cfg['eyes']):
  m=Image.new('L',im.size);ImageDraw.Draw(m).polygon(eye['outline'],fill=255);parts['eye'+str(i)]=convert(m)
  ImageDraw.Draw(mask).polygon(eye['outline'],fill=0)
 m=Image.new('L',im.size);ImageDraw.Draw(m).polygon(cfg['mouth_outline'],fill=255);parts['source_mouth']=convert(m);ImageDraw.Draw(mask).polygon(cfg['mouth_outline'],fill=0)
 parts['head']=convert(mask)
 if who=='gyokeres':
  sm=Image.new('L',im.size);ImageDraw.Draw(sm).polygon([(296,493),(334,500),(382,507),(459,501),(505,488),(516,542),(550,637),(487,655),(417,662),(394,574),(382,652),(328,654),(266,647),(280,564)],fill=255);parts['shorts']=convert(sm)
 data={'source':str(source.relative_to(V)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'design':cfg,'parts':parts,'method':'VTracer 0.6.15 spline contours sampled as native paths; semantic eye/mouth separation; native construction still requires pose review.'}
 (O/(who+'.json')).write_text(json.dumps(data,separators=(',',':'))+'\n')
 print(who,{k:len(v) for k,v in parts.items()},flush=True)

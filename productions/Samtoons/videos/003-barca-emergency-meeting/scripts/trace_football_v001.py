"""Prepare scene-specific editable contours from the inspected football sheet.
Existing VTracer parser reused; image is construction reference, not a movie layer.
"""
import ast, hashlib, json, re, xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import vtracer
V=Path(__file__).resolve().parents[1];O=V/'assets/football-v001'
source=Image.open(O/'players-reference.png').convert('RGBA')
p=next(V.parent.glob('002*/scripts/trace_selected_heads_v011.py'))
fn=next(n for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='convert')
exec(compile(ast.Module(body=[fn],type_ignores=[]),str(p),'exec'))
D={
 'Raphinha':dict(cx=302,head=[197,14,397,243],neck=[302,281],skin='#e9a25e',shadow='#c58145',eyes=[[303,137,17,15],[357,130,12,14]],mouth=[336,188,29],shirt=[[246,254],[341,254],[404,279],[388,383],[402,568],[350,579],[258,577],[201,566],[221,382],[195,279]],shorts=[182,568,418,694],boots=[[108,891,229,992],[341,892,490,989]],ankles=[[188,909],[371,908]],number=11),
 'Pedri':dict(cx=769,head=[657,16,857,243],neck=[769,282],skin='#f3b474',shadow='#d49456',eyes=[[765,142,18,16],[821,135,13,15]],mouth=[796,190,27],shirt=[[713,254],[813,255],[871,283],[852,383],[868,566],[813,579],[726,578],[670,566],[689,383],[665,283]],shorts=[647,568,884,695],boots=[[581,892,698,991],[806,891,963,990]],ankles=[[654,909],[838,908]],number=8),
 'Yamal':dict(cx=1254,head=[1126,14,1346,240],neck=[1254,283],skin='#c78749',shadow='#a96637',eyes=[[1247,142,18,15],[1299,135,12,14]],mouth=[1279,187,24],shirt=[[1196,256],[1295,255],[1355,281],[1333,384],[1353,568],[1297,580],[1209,578],[1156,567],[1175,383],[1145,281]],shorts=[1134,568,1373,695],boots=[[1069,892,1195,992],[1294,891,1448,990]],ankles=[[1142,909],[1325,908]],number=10)
}
def mask(bounds=None,poly=None):
 m=Image.new('L',source.size);d=ImageDraw.Draw(m)
 if bounds:d.rectangle(bounds,fill=255)
 if poly:d.polygon(poly,fill=255)
 return ImageChops.multiply(m,source.getchannel('A').point(lambda a:255 if a>=215 else 0))
def trace(m):
 global im
 box=m.getbbox();assert box
 im=source.crop(box);rows=convert(m.crop(box))
 for r in rows:
  for path in r['paths']:
   for v in path:v[0]+=box[0];v[1]+=box[1]
 return rows
for name,c in D.items():
 m=mask(bounds=c['head']);draw=ImageDraw.Draw(m)
 for x,y,rx,ry in c['eyes']:draw.ellipse((x-rx-2,y-ry-2,x+rx+2,y+ry+2),fill=0)
 parts={'head':trace(m),'shirt':trace(mask(poly=c['shirt'])),'shorts':trace(mask(bounds=c['shorts']))}
 for i,b in enumerate(c['boots']):parts['boot'+str(i)]=trace(mask(bounds=b))
 out={'source':'players-reference.png','source_sha256':hashlib.sha256((O/'players-reference.png').read_bytes()).hexdigest(),'design':c,'parts':parts}
 (O/(name.lower()+'.json')).write_text(json.dumps(out,separators=(',',':'))+'\n')
 print(name, {k:len(v) for k,v in parts.items()},flush=True)
source=Image.open(O/'defenders-reference.png').convert('RGBA')
for i,c in enumerate([
 dict(bounds=[47,188,480,704],neck=[257,757],skin='#eca66c',eyes=[[128,422,28,33],[246,434,34,32]]),
 dict(bounds=[561,177,980,702],neck=[766,757],skin='#a5683a',eyes=[[634,430,26,32],[754,437,34,33]]),
 dict(bounds=[1070,172,1518,704],neck=[1280,757],skin='#fbb58e',eyes=[[1163,435,27,33],[1283,447,34,34]])],1):
 m=mask(bounds=c['bounds']);d=ImageDraw.Draw(m)
 for x,y,rx,ry in c['eyes']:d.ellipse((x-rx-2,y-ry-2,x+rx+2,y+ry+2),fill=0)
 (O/f'defender-{i}.json').write_text(json.dumps({'design':c,'head':trace(m),'scale':.00083},separators=(',',':'))+'\n')
 print('defender',i,flush=True)

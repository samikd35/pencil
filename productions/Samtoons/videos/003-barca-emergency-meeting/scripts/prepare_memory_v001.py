"""S10 construction sources: new Bayern athlete, selected Barça player/coaching art."""
import ast,hashlib,json,re,xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import vtracer
V=Path(__file__).resolve().parents[1];O=V/'assets/memory-v001'
p=next(V.parent.glob('002*/scripts/trace_selected_heads_v011.py'))
fn=next(n for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='convert');exec(compile(ast.Module(body=[fn],type_ignores=[]),str(p),'exec'))
source=Image.open(O/'lewandowski-reference.png').convert('RGBA')
c=dict(cx=510,neck=[507,438],skin='#f6b776',shadow='#c88c50',head=[315,8,624,379],eyes=[[487,207,22,16],[568,197,15,15]],mouth=[530,294,35],shirt=[[423,389],[585,391],[689,434],[667,606],[692,861],[604,886],[423,880],[343,862],[355,596],[319,436]],shorts=[312,863,716,1075],boots=[[222,1370,419,1527],[593,1363,841,1515]],ankles=[[367,1403],[651,1403]],number=9)
def mask(bounds=None,poly=None):
 m=Image.new('L',source.size);d=ImageDraw.Draw(m)
 if bounds:d.rectangle(bounds,fill=255)
 if poly:d.polygon(poly,fill=255)
 return ImageChops.multiply(m,source.getchannel('A').point(lambda a:255 if a>=215 else 0))
def trace(m):
 global im
 box=m.getbbox();assert box;im=source.crop(box);rows=convert(m.crop(box))
 for r in rows:
  for path in r['paths']:
   for v in path:v[0]+=box[0];v[1]+=box[1]
 return rows
m=mask(bounds=c['head']);d=ImageDraw.Draw(m)
for x,y,rx,ry in c['eyes']:d.ellipse((x-rx-2,y-ry-2,x+rx+2,y+ry+2),fill=0)
parts={'head':trace(m),'shirt':trace(mask(poly=c['shirt'])),'shorts':trace(mask(bounds=c['shorts']))}
for i,b in enumerate(c['boots']):parts['boot'+str(i)]=trace(mask(bounds=b))
# Normalize to established metre/coordinate convention without changing the design.
k=2/3
for rows in parts.values():
 for row in rows:
  for path in row['paths']:
   for xy in path:xy[0]*=k;xy[1]*=k
c['cx']*=k
for n in ['neck','head','mouth','shorts']:c[n]=[v*k for v in c[n]]
for n in ['eyes','shirt','boots','ankles']:c[n]=[[v*k for v in a] for a in c[n]]
(O/'lewandowski.json').write_text(json.dumps({'design':c,'parts':parts},separators=(',',':'))+'\n')
(O/'raphinha.json').write_bytes((V/'assets/football-v001/raphinha.json').read_bytes())
f=json.loads((V/'assets/coaches-v001/flick.json').read_text());c=f['design']
# Actor primitive expects athlete part names. Custom animation supplies seated trousers.
f['design']=dict(cx=c['hip'][0],neck=c['neck'],skin=c['skin'],shadow=c['shade'],eyes=c['eyes'],mouth=c['mouth'][:3],ankles=c['ankles'])
f['parts']['shirt']=f['parts'].pop('body');f['parts']['shorts']=f['parts']['shirt'][:1]
(O/'flick.json').write_text(json.dumps(f,separators=(',',':'))+'\n')
(O/'provenance.json').write_text(json.dumps({'tool':'Built-in image_gen.imagegen','generated_source':'/Users/samikd/.codex/generated_images/01a0c8d1-7919-78f2-a177-af7ad445305d/exec-b1fdef2c-1964-40dd-ab6e-d4cdc037b645.png','references':['assets/lewandowski-v001/reference-supported.png','assets/football-v001/players-reference.png'],'scope':'Lewandowski Bayern caricature construction. Illustrative training memory, not match footage. Raphinha/Flick artwork reused, not their prior motion.','files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.glob('*') if p.suffix in ['.json','.png']}},indent=2)+'\n')
print('Prepared S10 native contour inputs')

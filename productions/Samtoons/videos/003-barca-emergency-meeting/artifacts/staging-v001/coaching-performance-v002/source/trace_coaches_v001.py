"""S07 reference-to-contour preparation; reuse the inspected S06 tracing route."""
import ast, hashlib, json, re, xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import vtracer
V=Path(__file__).resolve().parents[1];O=V/'assets/coaches-v001'
source=Image.open(O/'coaches-reference.png').convert('RGBA')
p=V.parent/'002-how-arsenal-won-the-league/scripts/trace_selected_heads_v011.py'
fn=next(n for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='convert')
exec(compile(ast.Module(body=[fn],type_ignores=[]),str(p),'exec'))
DESIGNS={
 'Flick':dict(neck=[404,260],hip=[406,569],skin='#efac70',shade='#ce8957',cloth='#263859',cloth_shadow='#1d2946',head=[303,1,495,242],eyes=[[335,125,11,6],[388,125,18,8]],mouth=[358,188,27,8],mouth_skin='#c79971',body=[[340,239],[457,232],[535,282],[530,366],[526,568],[286,570],[282,370],[272,287],[328,257]],boots=[[239,906,342,1018],[434,901,600,1003]],ankles=[[301,926],[481,927]],hands=[[145,563,220,691],[600,563,663,691]],wrists=[[185,575],[621,575]]),
 'Assistant':dict(neck=[1148,255],hip=[1135,565],skin='#eeae73',shade='#cd8b55',cloth='#3094a0',cloth_shadow='#237685',head=[1044,9,1222,236],eyes=[[1150,131,16,12],[1196,127,11,12]],mouth=[1174,175,27,8],mouth_skin='#edac70',body=[[1090,245],[1181,236],[1246,282],[1246,366],[1233,566],[1031,565],[1043,368],[1020,288]],boots=[[963,903,1127,1016],[1214,905,1312,1019]],ankles=[[1080,927],[1253,930]],hands=[[900,566,963,686],[1318,566,1396,687]],wrists=[[937,580],[1360,578]])
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
   for pt in path:pt[0]+=box[0];pt[1]+=box[1]
 return rows
for name,c in DESIGNS.items():
 outline=([(303,1),(499,1),(499,207),(462,242),(413,280),(380,256),(334,234),(303,210)] if name=='Flick' else [(1044,9),(1222,9),(1226,186),(1194,222),(1151,281),(1121,270),(1100,219),(1044,182)])
 m=mask(poly=outline);d=ImageDraw.Draw(m)
 for x,y,rx,ry in c['eyes']+[c['mouth']]:d.ellipse((x-rx-1,y-ry-1,x+rx+1,y+ry+1),fill=0)
 parts={'head':trace(m),'body':trace(mask(poly=c['body']))}
 for i in range(2):
  parts['boot'+str(i)]=trace(mask(bounds=c['boots'][i]))
  parts['hand'+str(i)]=trace(mask(bounds=c['hands'][i]))
 (O/(name.lower()+'.json')).write_text(json.dumps({'design':c,'parts':parts,'source':'coaches-reference.png','source_sha256':hashlib.sha256((O/'coaches-reference.png').read_bytes()).hexdigest()},separators=(',',':'))+'\n')
 print(name,{k:len(v) for k,v in parts.items()},flush=True)

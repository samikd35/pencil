"""Prepare native contours from the supported seated source; no generic leg rig."""
import ast,json,hashlib,re,xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import vtracer
V=Path(__file__).resolve().parents[1];O=V/'assets/lewandowski-v001';src=O/'reference-supported.png'
source=Image.open(src).convert('RGBA')
p=V.parent/'002-how-arsenal-won-the-league/scripts/trace_selected_heads_v011.py'
fn=next(n for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='convert')
exec(compile(ast.Module(body=[fn],type_ignores=[]),str(p),'exec'))
c={'who':'Robert','origin':[570,1220],'neck':[570,640],'skin':'#ffc078',
'eyes':[{'center':[517,302],'pupil':[533,299],'size':[13,14],'outline':[[478,308],[485,290],[502,280],[527,278],[541,286],[548,301],[539,316],[519,324],[496,322],[482,316]]},{'center':[629,288],'pupil':[647,284],'size':[12,13],'outline':[[600,291],[606,275],[621,268],[639,267],[653,274],[659,287],[652,299],[635,307],[616,305],[603,299]]}],
'brows':[[[460,282],[474,267],[497,253],[520,250],[541,257],[552,268],[551,276],[534,270],[517,266],[494,269],[474,278]],[[590,264],[603,246],[621,232],[641,228],[657,233],[668,245],[670,254],[653,244],[640,240],[623,244],[607,254]]],
'mouth':[[516,418],[541,418],[568,424],[600,424],[634,419],[656,409],[661,421],[651,435],[625,443],[589,445],[552,440],[529,434],[516,430]],'mouth_center':[587,427],'mouth_width':67}
def mask(poly):
 m=Image.new('L',source.size);ImageDraw.Draw(m).polygon(poly,fill=255);return ImageChops.multiply(m,source.getchannel('A').point(lambda a:255 if a>220 else 0))
def trace(m):
 global im
 box=m.getbbox();assert box
 im=source.crop(box);rows=convert(m.crop(box))
 for r in rows:
  for path in r['paths']:
   for pt in path:pt[0]+=box[0];pt[1]+=box[1]
 return rows
full=source.getchannel('A').point(lambda a:255 if a>220 else 0);parts={}
for name,poly in [('rest_mouth',c['mouth'])]+[(f'brow{i}',p) for i,p in enumerate(c['brows'])]+[(f'eye{i}',e['outline']) for i,e in enumerate(c['eyes'])]:
 m=mask(poly);parts[name]=trace(m);full=ImageChops.subtract(full,m)
# Cup body and handle are one rigid object. Hand remains part of continuous arm.
cup=mask([(390,1070),(420,1068),(427,1041),(445,1033),(550,1033),(578,1043),(578,1198),(561,1215),(447,1215),(431,1201),(430,1167),(402,1171),(397,1148),(422,1144),(421,1100),(397,1093)])
parts['cup']=trace(cup);full=ImageChops.subtract(full,cup);parts['body']=trace(full)
(O/'robert.json').write_text(json.dumps({'source':str(src.relative_to(V)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'design':c,'parts':parts},separators=(',',':'))+'\n')
print({k:len(v) for k,v in parts.items()})

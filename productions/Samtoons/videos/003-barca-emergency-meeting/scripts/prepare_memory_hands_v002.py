"""Trace relaxed hands from the already selected construction drawings."""
import ast,json,re,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image
import vtracer
V=Path(__file__).resolve().parents[1];O=V/'assets/memory-v002';O.mkdir(exist_ok=True)
p=V.parent/'002-how-arsenal-won-the-league/scripts/trace_selected_heads_v011.py';fn=next(n for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='convert');exec(compile(ast.Module(body=[fn],type_ignores=[]),str(p),'exec'))
D={'Lewandowski':('assets/memory-v001/lewandowski-reference.png',[(160,849,277,1034),(752,849,865,1023)],[(215,862),(803,862)],.00188*2/3),'Raphinha':('assets/football-v001/players-reference.png',[(85,535,158,661),(425,538,506,664)],[(122,551),(457,552)],.00188)}
for who,(path,boxes,wrists,scale) in D.items():
 source=Image.open(V/path).convert('RGBA');hands=[]
 for box,wr in zip(boxes,wrists):
  im=source.crop(box);rows=convert(im.getchannel('A').point(lambda a:255 if a>=215 else 0))
  for row in rows:
   for pts in row['paths']:
    for q in pts:q[0]=(q[0]+box[0]-wr[0])*scale;q[1]=(wr[1]-q[1]-box[1])*scale
  hands.append(rows)
 (O/(who.lower()+'-hands.json')).write_text(json.dumps({'source':path,'source_sha256':hashlib.sha256((V/path).read_bytes()).hexdigest(),'rows':hands},separators=(',',':'))+'\n')
print('Selected source hands traced')

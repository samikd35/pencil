"""Fresh vector construction from this experiment's generated view reference.
Converts pixels to editable filled paths; never reads prior production contours.
"""
from pathlib import Path
from PIL import Image
import vtracer,io,re,json,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];im=Image.open(ROOT/'inputs/head-views.png')
def parse(d):
 toks=re.findall(r'[MLCQZmlcqz]|[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?',d);i=0;cmd=None;pt=(0,0);paths=[];path=[]
 while i<len(toks):
  if toks[i].isalpha():cmd=toks[i].upper();i+=1
  if cmd=='Z':
   if path:paths.append(path)
   path=[];cmd=None;continue
  if cmd in ['M','L']:
   pt=(float(toks[i]),float(toks[i+1]));i+=2;path.append(pt)
   if cmd=='M':cmd='L'
  elif cmd=='C':
   vals=list(map(float,toks[i:i+6]));i+=6;p0=pt;p1=vals[:2];p2=vals[2:4];p3=vals[4:]
   for j in range(1,9):
    t=j/8;u=1-t;path.append(tuple(u**3*p0[k]+3*u*u*t*p1[k]+3*u*t*t*p2[k]+t**3*p3[k] for k in [0,1]))
   pt=tuple(p3)
  else:raise ValueError(('Unsupported fresh SVG command',cmd))
 if path:paths.append(path)
 return paths
rows=[]
for view,(lo,hi) in zip(['left','front','right'],[(0,699),(699,1399),(1399,2098)]):
 panel=im.crop((lo,0,hi,im.height));buf=io.BytesIO();panel.save(buf,format='PNG')
 svg=vtracer.convert_raw_image_to_svg(buf.getvalue(),img_format='png',colormode='color',hierarchical='stacked',mode='spline',filter_speckle=8,color_precision=5,layer_difference=22,corner_threshold=60,length_threshold=4,max_iterations=10,splice_threshold=45,path_precision=2)
 (ROOT/'inputs'/('head-'+view+'.svg')).write_text(svg)
 box=panel.getchannel('A').point(lambda a:255 if a>200 else 0).getbbox();result=[]
 for elem in ET.fromstring(svg).iter():
  if not elem.tag.endswith('path'):continue
  shift=list(map(float,re.findall(r'[-+]?\d*\.?\d+',elem.attrib.get('transform',''))));dx,dy=(shift+[0,0])[:2]
  loops=[[(x+dx,y+dy) for x,y in path] for path in parse(elem.attrib['d'])]
  result.append({'color':elem.attrib.get('fill','#000000'),'loops':loops})
 rows.append({'view':view,'bbox':box,'paths':result})
 print(view,box,len(result))
(ROOT/'inputs/head-drawings.json').write_text(json.dumps(rows,separators=(',',':')))

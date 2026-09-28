"""Semantic contour extraction for S12. Source art is retained untouched."""
import ast,json,hashlib,re,xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageFilter
import vtracer,numpy as np
from scipy.ndimage import label
V=Path(__file__).resolve().parents[1];O=V/'assets/membership-v001';src=O/'reference.png';source=Image.open(src).convert('RGBA')
p=next(V.parent.glob('002*/scripts/trace_selected_heads_v011.py'));fn=next(n for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='convert');exec(compile(ast.Module(body=[fn],type_ignores=[]),str(p),'exec'))
# Remove only the white region connected to image edges; retain white shirts and eyes.
a=np.asarray(source);white=np.min(a[:,:,:3],axis=2)>240;labs,num=label(white);outer=np.unique(np.concatenate([labs[0],labs[-1],labs[:,0],labs[:,-1]]));bg=np.isin(labs,outer[outer!=0]);sil=Image.fromarray((~bg*255).astype('uint8'))
def mask(poly):
 m=Image.new('L',source.size);ImageDraw.Draw(m).polygon(poly,fill=255);return ImageChops.multiply(m,sil)
def trace(m):
 global im
 box=m.getbbox();assert box;im=source.crop(box);rows=convert(m.crop(box))
 for r in rows:
  for path in r['paths']:
   for pt in path:pt[0]+=box[0];pt[1]+=box[1]
 return rows
D={
'Fan':dict(origin=[1080,870],neck=[1066,421],skin='#f7b56c',bounds=[780,45,1380,1023],
 eyes=[dict(center=[994,233],pupil=[985,232],size=[10,14],outline=[[971,236],[974,220],[985,211],[1000,211],[1012,223],[1015,238],[1004,247],[989,253],[978,249]]),dict(center=[1073,247],pupil=[1059,246],size=[10,14],outline=[[1047,244],[1051,231],[1063,225],[1078,225],[1091,233],[1097,249],[1091,261],[1078,269],[1060,266],[1048,257]])],
 brows=[[[970,207],[973,193],[983,182],[995,186],[1008,194],[1018,206],[1017,213],[1005,206],[992,199],[982,199]],[[1046,203],[1072,203],[1092,211],[1104,223],[1108,232],[1094,225],[1074,216],[1049,214]]],
 mouth=[[979,300],[997,304],[1020,307],[1044,306],[1067,298],[1076,298],[1080,310],[1069,317],[1047,321],[1025,321],[1003,315],[984,310]],mouth_center=[1029,310],mouth_width=43,
 hand=[[869,554],[881,493],[888,469],[906,451],[930,438],[947,436],[960,442],[961,450],[952,456],[934,462],[961,463],[981,466],[985,475],[978,482],[954,485],[981,487],[985,496],[978,504],[951,508],[971,510],[974,519],[963,526],[943,532],[932,550],[926,567],[917,581],[900,588],[881,582]],
 prop=[[904,384],[909,374],[921,370],[977,370],[989,375],[994,387],[997,522],[990,536],[933,541],[912,532]],
 shoulder=[917,472],elbow=[847,670],wrist=[896,576],arm_box=[790,424,944,744]),
'Valencia':dict(origin=[407,784],neck=[412,425],skin='#f4b36a',bounds=[120,0,700,1023],
 eyes=[dict(center=[410,194],pupil=[424,191],size=[9,12],outline=[[387,185],[407,181],[427,183],[435,195],[426,205],[410,209],[398,204],[390,196]]),dict(center=[482,180],pupil=[490,178],size=[8,10],outline=[[459,178],[473,170],[493,169],[500,178],[496,188],[484,193],[470,190],[461,185]])],
 brows=[[[376,178],[381,164],[398,155],[417,157],[438,156],[442,167],[434,174],[415,174],[396,171]],[[457,159],[465,143],[481,132],[491,132],[500,143],[497,153],[484,145],[472,151],[463,161]]],
 mouth=[[403,258],[420,265],[443,267],[470,268],[482,269],[482,278],[457,281],[433,278],[411,273],[402,267]],mouth_center=[443,271],mouth_width=38,
 hand=[[441,541],[462,537],[484,539],[503,546],[523,557],[530,572],[534,611],[540,621],[530,645],[512,658],[494,655],[484,648],[475,631],[458,626],[453,615],[459,607],[450,606],[444,595],[448,588],[438,586],[435,577],[445,567],[439,559]],
 prop=[[350,507],[462,506],[462,572],[350,573]],shoulder=[583,468],elbow=[637,670],wrist=[519,632],arm_box=[432,419,692,731])}
for who,c in D.items():
 l,t,r,b=c['bounds'];full=mask([(l,t),(r,t),(r,b),(l,b)]);parts={}
 for name,poly in [('rest_mouth',c['mouth'])]+[(f'brow{i}',p) for i,p in enumerate(c['brows'])]+[(f'eye{i}',e['outline']) for i,e in enumerate(c['eyes'])]+[('hand',c['hand'])]:
  m=mask(poly);parts[name]=trace(m);full=ImageChops.subtract(full,m.filter(ImageFilter.MaxFilter(7)) if name=='hand' else m)
 pm=ImageChops.subtract(mask(c['prop']),mask(c['hand']));parts['prop']=trace(pm);full=ImageChops.subtract(full,pm.filter(ImageFilter.MaxFilter(5)))
 # Discard the entire moving-arm domain. It will be redrawn as a connected
 # contour; source shirt/scarf points are never bound to the arm.
 cut=([(780,426),(913,426),(946,474),(944,790),(780,790)] if who=='Fan' else [(567,626),(677,600),(700,752),(540,744),(475,670),(475,619),(548,619),(559,630)])
 full=ImageChops.subtract(full,mask(cut))
 parts['body']=trace(full)
 if who=='Fan':
  pm=mask([(941,50),(1240,50),(1240,374),(941,374)]);pm=ImageChops.subtract(pm,mask(c['mouth']));parts['portrait']=trace(pm)
 (O/(who.lower()+'.json')).write_text(json.dumps({'source':'assets/membership-v001/reference.png','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'design':dict(c,who=who),'parts':parts},separators=(',',':'))+'\n')
 print(who,{k:len(v) for k,v in parts.items()},flush=True)
(O/'provenance.json').write_text(json.dumps({'tool':'Built-in image_gen.imagegen','source_file':str(src.relative_to(V)),'reference_role':'S11 frame: style only, not character identity','cast':'Two original fictional people; no real-person identification.','prompt':'prompt.md','native_extraction':'Selected color contours and independently controlled face, grip and prop; source PNG unmodified.'},indent=2)+'\n')

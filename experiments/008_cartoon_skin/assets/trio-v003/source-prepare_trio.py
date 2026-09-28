"""Reconstruct the user-selected cartoon heads as native-vector design inputs."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import sys
import xml.etree.ElementTree as ET

import cv2 as cv
import numpy as np
from PIL import Image
import vtracer

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--out',required=True);args=parser.parse_args()
assert Path(args.out).name==args.out
OUT=ROOT/'assets'/args.out
OUT.mkdir(exist_ok=False)
SOURCE=Path('/Users/samikd/Downloads/3 pla.png')
shutil.copy2(SOURCE,OUT/'reference.png')
rgb=np.asarray(Image.open(SOURCE).convert('RGB'))
height,width=rgb.shape[:2]
assert (width,height)==(510,1194),(width,height)
config={
 'jude':{'label':'Jude Bellingham','height':1.55,'anchor':[151,250],
  'skin':'#c88660','shadow':'#a95f46','body_width':.32,'torso_height':1.18,'hip_y':1.0,'neck':.60,'boot':'#14273e',
  'boundary':[[89,174],[86,143],[96,117],[119,105],[146,96],[172,95],[191,106],[199,137],[199,158],[207,172],[212,195],[208,216],[203,242],[196,257],[179,262],[158,254],[144,239],[132,220],[115,213],[104,199],[104,183]],
  'eyes':[[[155,183],[164,173],[174,172],[180,184],[177,195],[167,200],[160,195]],[[186,180],[194,174],[203,176],[208,189],[201,197],[190,194]]]},
 'mbappe':{'label':'Kylian Mbappe','height':1.47,'anchor':[293,286],
  'skin':'#dc8852','shadow':'#b3623e','body_width':.38,'torso_height':1.05,'hip_y':.92,'neck':.91,'boot':'#183245',
  'boundary':[[228,225],[225,199],[235,178],[256,167],[290,160],[316,161],[339,172],[350,190],[358,201],[363,219],[369,231],[378,236],[379,247],[370,253],[382,260],[381,273],[370,282],[356,296],[342,304],[323,305],[299,295],[274,284],[258,276],[246,271],[234,251]],
  'eyes':[[[323,218],[324,210],[333,213],[343,219],[347,234],[342,244],[332,240],[326,232]],[[352,208],[358,204],[364,216],[365,228],[357,228]]]},
 'vini':{'label':'Vinicius Junior','height':1.62,'anchor':[236,692],
  'skin':'#934637','shadow':'#73392d','body_width':.48,'torso_height':.87,'hip_y':.62,'neck':.16,'boot':'#ef454d',
  'boundary':[[145,595],[146,565],[154,540],[167,523],[191,513],[209,505],[230,515],[252,512],[277,522],[293,542],[295,567],[286,588],[298,612],[297,631],[316,641],[326,655],[317,670],[302,681],[299,702],[265,705],[221,705],[197,694],[179,676],[165,656],[162,632],[154,615]],
  'eyes':[[[239,610],[246,603],[256,604],[268,611],[273,623],[268,635],[257,640],[246,635],[240,625]],[[279,607],[285,601],[291,603],[298,616],[297,628],[288,630],[281,620]]]}
}
namespace='{http://www.w3.org/2000/svg}'
for key,cfg in config.items():
    mask=np.zeros((height,width),np.uint8)
    cv.fillPoly(mask,[np.asarray(cfg['boundary'],np.int32)],255)
    # The explicit head domain excludes bodies/hands; reject the purple stage inside its margin.
    r,g,b=[rgb[:,:,i].astype(np.int16) for i in range(3)]
    mask[(b>r+5)&(b>g+5)]=0
    count,labels,stats,_=cv.connectedComponentsWithStats(mask,8)
    assert count>1
    mask=(labels==(1+int(np.argmax(stats[1:,cv.CC_STAT_AREA])))).astype(np.uint8)*255
    ys,xs=np.where(mask>0);x0,x1=int(xs.min())-2,int(xs.max())+3;y0,y1=int(ys.min())-2,int(ys.max())+3
    cfg['crop']=[x0,y0,x1,y1]
    cfg['pixels_per_unit']=(int(ys.max())-int(ys.min()))/cfg['height']
    # Resample original RGB before masking, as established in the existing tracing workflow.
    scale=3
    image=np.asarray(Image.fromarray(rgb[y0:y1,x0:x1]).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.LANCZOS)).copy()
    selected=np.asarray(Image.fromarray(mask[y0:y1,x0:x1]).resize(((x1-x0)*scale,(y1-y0)*scale),Image.Resampling.NEAREST))>0
    image[~selected]=[0,255,0]
    Image.fromarray(image).save(OUT/(key+'-trace.png'))
    target=OUT/(key+'.svg')
    vtracer.convert_image_to_svg_py(str(OUT/(key+'-trace.png')),str(target),colormode='color',
        hierarchical='cutout',mode='spline',filter_speckle=18,color_precision=6,layer_difference=8,
        corner_threshold=65,length_threshold=3.5,splice_threshold=45,path_precision=3)
    tree=ET.parse(target)
    paths=[]
    for path in list(tree.getroot()):
        fill=path.get('fill','')
        if not fill.startswith('#'):continue
        cr,cg,cb=[int(fill[i:i+2],16) for i in (1,3,5)]
        if cg>180 and cr<100 and cb<100:tree.getroot().remove(path)
        else:paths.append(path)
    assert paths
    tree.write(target,encoding='utf-8',xml_declaration=True)
    cfg['paths']=len(paths)
    print(key,len(paths),'editable filled paths',flush=True)
(OUT/'characters.json').write_text(json.dumps(config,indent=2)+'\n')
sys.path.insert(0,str(ROOT.parent/'001_heavy_box'))
from journal import append_event
append_event(ROOT,stage='trio-reference-vectors',status='completed',
 intent='Test the user-identified three-player cartoon reference in the current curve/mesh workflow',
 method='Explicit whole-head domains, existing VTracer dependency, native vector reconstruction',
 inputs=['prepare_trio.py'],outputs=[str((OUT/n).relative_to(ROOT)) for n in ['reference.png','characters.json']+[k+'.svg' for k in config]],
 result='User supplied the identities and requested this drawing treatment. Reference reconstruction study, not a newly approved canonical identity or an account of a real football event. Visible head artwork will be native filled curves, not image textures.')

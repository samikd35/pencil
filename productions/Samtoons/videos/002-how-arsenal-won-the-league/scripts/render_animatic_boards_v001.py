"""Render storyboard exposure/cuts only; no image warping or implied gait animation."""
from pathlib import Path
import json,subprocess,sys,hashlib
import numpy as np
V=Path(__file__).resolve().parents[1];O=V/'artifacts/animatic-v001';C=O/'clips';C.mkdir(exist_ok=True);E=json.loads((O/'edit.json').read_text());FF='/opt/homebrew/bin/ffmpeg'
for i,row in enumerate(E):
 if not int(sys.argv[1])<=i<int(sys.argv[2]):continue
 src=O/row['source'];dst=C/(row['id']+'.mp4')
 if dst.exists() and '--recrop' not in sys.argv:continue
 probe=json.loads(subprocess.check_output(['/opt/homebrew/bin/ffprobe','-v','error','-show_entries','stream=width,height','-of','json',str(src)]))['streams'][0]
 W,H=probe['width'],probe['height']
 raw=subprocess.check_output([FF,'-v','error','-i',str(src),'-f','rawvideo','-pix_fmt','gray','-frames:v','1','-']);im=np.frombuffer(raw,np.uint8).reshape(H,W)
 def divider(scores,expected):
  lo=max(1,round(expected)-25);hi=min(len(scores)-1,round(expected)+26);a=scores[lo:hi];return lo+int(np.argmin(a))
 xx=[0,divider(im.mean(axis=0),W/2),W];yy=[0,divider(im.mean(axis=1),H/3),divider(im.mean(axis=1),2*H/3),H]
 col=row['panel']%2;rr=row['panel']//2;x=xx[col]+5;y=yy[rr]+5;w=xx[col+1]-xx[col]-4;h=yy[rr+1]-yy[rr]-4
 # Crop thin sheet dividers; preserve proportions inside16:9. Still-frame art is explicitly a storyboard.
 vf=f'crop={w-6}:{h-6}:{x}:{y},scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1'
 row.update(crop=[x,y,w-6,h-6],source_sha256=hashlib.sha256(src.read_bytes()).hexdigest())
 if row['id'] in ['N04_reveal','N04_meltdown']:
  # Keep already accepted Ferguson portrait rather than silently replacing his chosen design.
  src=V/'artifacts/ferguson-design-v001/reveal-proposal.png';vf='scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1';row['source']=str(src.relative_to(O)) if src.is_relative_to(O) else '../../artifacts/ferguson-design-v001/reveal-proposal.png';row['source_sha256']=hashlib.sha256(src.read_bytes()).hexdigest()
 subprocess.run([FF,'-v','error','-y','-loop','1','-framerate','24','-i',str(src),'-an','-vf',vf,'-frames:v',str(row['frames']),'-c:v','libx264','-tune','stillimage','-preset','fast','-crf','20','-pix_fmt','yuv420p',str(dst)],check=True)
 (C/(row['id']+'.json')).write_text(json.dumps(row,indent=2));print(i,row['id'],flush=True)

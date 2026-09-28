"""Encoded consecutive-frame evidence plus preservation checks; no listening claim."""
from pathlib import Path
import json,subprocess,hashlib
from PIL import Image,ImageDraw
V=Path(__file__).resolve().parents[1];O=V/'artifacts/defence-v022';D=O/'checks';D.mkdir(exist_ok=True);FF='/opt/homebrew/bin/ffmpeg'
checks=[]
for shot,lo,hi,crop in [('CD04',186,197,(0,90,380,470)),('CD04',218,229,(950,100,1280,450)),('CD04',239,250,(460,0,810,310)),('CD05_ping',3,14,(390,70,920,510)),('CD05_ping',31,42,(510,30,765,270)),('CD05_ping',100,111,(280,70,960,480))]:
 p=O/'clips'/(shot+'.mp4')
 if not p.exists():continue
 raw=subprocess.check_output([FF,'-v','error','-i',str(p),'-vf',f'select=between(n\\,{lo-1}\\,{hi-1})','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','pipe:1']);assert len(raw)==(hi-lo+1)*1280*720*3
 thumb=(300,235);canvas=Image.new('RGB',(4*300,3*260),(28,30,34));dr=ImageDraw.Draw(canvas)
 for j in range(hi-lo+1):
  a=Image.frombytes('RGB',(1280,720),raw[j*1280*720*3:(j+1)*1280*720*3]).crop(crop);a.thumbnail(thumb);x=(j%4)*300;y=(j//4)*260;canvas.paste(a,(x,y+22));dr.text((x+8,y+4),f'{shot} / {lo+j}',fill='white')
 dest=D/f'{shot}-{lo:03}-{hi:03}.jpg';canvas.save(dest,quality=93);checks.append(str(dest.relative_to(O)))
rows=json.loads((O/'edit.json').read_text());preserved={}
for r in rows:
 if r['id'] in ['CD04','CD05_ping']:continue
 p=O/'clips'/(r['id']+'.mp4');old=V/'artifacts/defence-v021/clips'/p.name;match=hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256(old.read_bytes()).digest();assert match;preserved[r['id']]=match
old=json.loads((V/'artifacts/defence-v019/audio-plan.json').read_text());new=json.loads((O/'audio-plan.json').read_text());voices={}
for k in ['L12','L13','L14','L15','L16','L17']:
 assert old['assets'][k]['sha256']==new['assets'][k]['sha256'];voices[k]=True
assert sum(r['frames'] for r in rows)==1323
(O/'regression-checks.json').write_text(json.dumps(dict(preserved_picture_clips=preserved,preserved_voice_assets=voices,encoded_consecutive_frame_sheets=checks,scope='Frame sheets require actual inspection. These checks do not certify humour, motion playback, likeness or listening.'),indent=2));print('checks',len(checks),flush=True)

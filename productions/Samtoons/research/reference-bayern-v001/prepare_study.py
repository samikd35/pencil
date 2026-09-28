"""Rebuild local reference sheets and measurements; no source-art reuse in films."""
from pathlib import Path
import subprocess,json,hashlib,math
from fractions import Fraction
from PIL import Image,ImageDraw,ImageFont
import numpy as np
ROOT=Path(__file__).resolve().parent
FF='/opt/homebrew/bin/ffmpeg'; FP='/opt/homebrew/bin/ffprobe'; SOURCE=ROOT/'source.mp4'
font=ImageFont.truetype('/System/Library/Fonts/Monaco.ttf',12)
def run(args):return subprocess.run(args,check=True,capture_output=True)
probe=json.loads(run([FP,'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(SOURCE)]).stdout)
s=next(x for x in probe['streams'] if x['codec_type']=='video');fps=Fraction(s['r_frame_rate']);n=int(s['nb_read_frames'])
assert fps==30 and s['width']==1920 and s['height']==1080
(ROOT/'sheets').mkdir(exist_ok=True)
W,H,C,R=240,135,8,10;cellh=153
p=subprocess.Popen([FF,'-v','error','-i',str(SOURCE),'-an','-vf',f'scale={W}:{H}','-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE)
page=None;overview=[];motions=[];prev=None;pages=[]
for i in range(n):
 raw=p.stdout.read(W*H*3);assert len(raw)==W*H*3
 im=Image.frombytes('RGB',(W,H),raw)
 arr=np.asarray(im,dtype=np.int16)
 if prev is not None:motions.append({'frame':i,'seconds':float(i/fps),'mean_rgb_change':float(np.abs(arr-prev).mean())})
 prev=arr
 if i%30==0:overview.append((i,im.copy()))
 slot=i%(C*R)
 if slot==0:page=Image.new('RGB',(C*W,R*cellh),'#151c24');draw=ImageDraw.Draw(page)
 x=(slot%C)*W;y=(slot//C)*cellh
 page.paste(im,(x,y));draw.text((x+3,y+H),f'F{i:04d}  {float(i/fps):07.3f}s',font=font,fill='white')
 if slot==C*R-1 or i==n-1:
  name=f'sheets/all-{i//(C*R)+1:02}.jpg';page.save(ROOT/name,quality=91)
  pages.append({'path':name,'first_frame':i-slot,'last_frame':i})
p.stdout.close();assert p.wait()==0
for start in range(0,len(overview),36):
 board=Image.new('RGB',(6*320,6*198),'#151c24');draw=ImageDraw.Draw(board)
 for j,(f,im) in enumerate(overview[start:start+36]):
  x=(j%6)*320;y=(j//6)*198;board.paste(im.resize((320,180)),(x,y));draw.text((x+3,y+181),f'F{f}  {f/30:.1f}s',font=font,fill='white')
 board.save(ROOT/f'sheets/overview-{start//36+1:02}.jpg',quality=93)
raw=run([FF,'-v','error','-i',str(SOURCE),'-vn','-ar','48000','-ac','1','-f','f32le','pipe:1']).stdout
samples=np.frombuffer(raw,dtype='<f4');assert np.isfinite(samples).all()
energy=[{'start_seconds':i/48000,'rms_dbfs':float(20*np.log10(max(1e-10,np.sqrt(np.mean(samples[i:i+4800]**2)))))} for i in range(0,len(samples),4800)]
measure=run([FF,'-hide_banner','-i',str(SOURCE),'-vn','-af','loudnorm=I=-16:TP=-1:LRA=11:print_format=json','-f','null','-']).stderr.decode()
loudness=json.loads(measure[measure.rfind('{'):measure.rfind('}')+1])
with SOURCE.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
report={'source_url':'https://www.youtube.com/watch?v=KD9ry6zWjjQ','sha256':digest,'probe':probe,'frames':n,'fps':str(fps),'picture_seconds':float(n/fps),'pages':pages,'frame_index':'zero-based; source time = frame / 30','coverage':'All frames decoded and represented consecutively. Rendering sheets is not visual review. Inspection ledger records actual viewed sheets/details.','loudness':loudness,'audio_scope':'Measurements and unverified automatic captions only; no subjective listening claimed.'}
(ROOT/'media-checks.json').write_text(json.dumps(report,indent=2)+'\n')
(ROOT/'frame-change.json').write_text(json.dumps(motions)+'\n')
(ROOT/'audio-energy.json').write_text(json.dumps(energy)+'\n')
assert sum(x['last_frame']-x['first_frame']+1 for x in pages)==n
print(json.dumps({'frames':n,'fps':str(fps),'seconds':float(n/fps),'sheets':len(pages),'audio_loudness':loudness}))

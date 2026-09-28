"""Render only the 10-second staging excerpt from its saved native scene."""
import argparse,bpy, hashlib, json, subprocess,sys
from pathlib import Path

parser=argparse.ArgumentParser();parser.add_argument('--revision',choices=['v001','v002','v004','v005','v006'],default='v001')
parser.add_argument('--foundation',action='store_true',help='Render the saved v006 stickman foundation')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
V=Path(__file__).resolve().parents[1];O=V/f'artifacts/staging-v001/call-performance-{args.revision}'
s=bpy.data.scenes['S003_S08_Call_Performance_'+args.revision]
bpy.context.window.scene=s
assert not args.foundation or args.revision=='v006'
stem='stickman' if args.foundation else 'call'
assert Path(bpy.data.filepath)==O/('stickman-foundation.blend' if args.foundation else 'call-performance.blend')
s.render.use_sequencer=False
frames=O/('stickman-frames' if args.foundation else 'frames');frames.mkdir(exist_ok=True)
temp=O/(stem+'-working.png');ff='/opt/homebrew/bin/ffmpeg'
p=subprocess.Popen([ff,'-v','error','-y','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(O/(stem+'-picture.mp4'))],stdin=subprocess.PIPE)
try:
    for f in range(1,241):
        s.frame_set(f);temp.unlink(missing_ok=True);s.render.filepath=str(temp)
        assert bpy.ops.render.render(write_still=True)=={'FINISHED'}
        raw=temp.read_bytes();p.stdin.write(raw)
        if f%6==1 or f in [48,153,156,163,192,213,240]: (frames/f'{f:03}.png').write_bytes(raw)
        if f%24==0:print('CALL_FRAME',f,flush=True)
    p.stdin.close();assert p.wait()==0
except BaseException:
    p.kill();p.wait();raise
temp.unlink(missing_ok=True)
plan=json.loads((V/'production.json').read_text());shot=next(x for x in plan['shots'] if x['id']=='S08')
start=(shot['start_frame']+shot['events']['proof_start']-1)*2000
if args.revision in ('v005','v006'):
    # The user requested the same audio: preserve the existing encoded track.
    audio_source=V/'artifacts/staging-v001/call-performance-v004/call-review.mp4'
    subprocess.run([ff,'-v','error','-y','-i',str(O/(stem+'-picture.mp4')),'-i',str(audio_source),'-map','0:v','-map','1:a','-c','copy','-movflags','+faststart',str(O/(stem+'-review.mp4'))],check=True)
else:
    subprocess.run([ff,'-v','error','-y','-i',str(O/'call-picture.mp4'),'-i',str(V/'artifacts/staging-v001/call-audio-v001/mix-premaster.wav'),'-filter_complex',f'[1:a]atrim=start_sample={start}:end_sample={start+480000},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(O/'call-review.mp4')],check=True)
sources=[Path(bpy.data.filepath),Path(__file__),V/f'scripts/build_call_performance_{args.revision}.py',V/'production.json']
if args.revision in ('v005','v006'):sources.append(audio_source)
(O/('stickman-render-inputs.json' if args.foundation else 'render-inputs.json')).write_text(json.dumps({str(p.relative_to(V)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},indent=2))
print('CALL_REVIEW_READY',flush=True)

"""Check full-HD delivery against the approved edit, without claiming listening."""
from pathlib import Path
import json,subprocess,hashlib,re,sys
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/delivery-v001';APPROVED=ROOT/'artifacts/animatic-v004'
FF='/opt/homebrew/bin/ffmpeg';FP='/opt/homebrew/bin/ffprobe'
def run(args):return subprocess.run(args,check=True,capture_output=True,text=True)
def verify():
 sys.path.insert(0,str(ROOT.parents[3]))
 from pipeline.checkpoints import require_checkpoint
 for stage in ('staging','sound','animatic'):require_checkpoint(ROOT,'animatic-v004',stage)
 edit=json.loads((OUT/'edit.json').read_text());assert edit==json.loads((APPROVED/'edit.json').read_text())
 assert (OUT/'mix-review.wav').read_bytes()==(APPROVED/'mix-review.wav').read_bytes()
 comparisons=[]
 for i,row in enumerate(edit):
  new=OUT/'picture-selected'/f'picture-{i:02}.mp4';old=APPROVED/'picture-selected'/new.name
  video=json.loads(run([FP,'-v','error','-select_streams','v:0','-show_streams','-of','json',str(new)]).stdout)['streams'][0]
  assert (video['width'],video['height'],video['r_frame_rate'],int(video['nb_frames']))==(1920,1080,'24/1',row['frames'])
  # Compare every matching frame at the approved viewing size. Sampling/encoding
  # changes are expected; the metric flags regressions for visual inspection.
  stats=OUT/f'comparison-{i:02}.txt'
  log=run([FF,'-hide_banner','-i',str(new),'-i',str(old),'-lavfi','[0:v]scale=960:540:flags=lanczos,setsar=1[a];[1:v]setsar=1[b];[a][b]ssim=stats_file='+str(stats),'-an','-f','null','-']).stderr
  score=float(re.findall(r'All:([0-9.]+)',log)[-1]);scores=[float(v) for v in re.findall(r'All:([0-9.]+)',stats.read_text())];assert len(scores)==row['frames']
  worst=min(scores);comparisons.append(dict(scene=row['scene'],frames=row['frames'],ssim=score,min_frame_ssim=worst,worst_local_frame=scores.index(worst)+1,needs_visual_review=score<.97 or worst<.96))
 report=dict(source='User-approved animatic-v004',dimensions=[1920,1080],fps=24,frames=sum(x['frames'] for x in edit),approved_mix_bit_identical=True,comparisons=comparisons,limits='Image similarity flags differences; it does not replace visual or listening review.')
 (OUT/'approved-comparison.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':verify()

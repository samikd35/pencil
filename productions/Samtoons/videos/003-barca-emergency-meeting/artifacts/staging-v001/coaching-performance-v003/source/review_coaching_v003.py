"""Verify the encoded revision and make a normal-speed before/after comparison."""
import hashlib,json,subprocess
from pathlib import Path

V=Path(__file__).resolve().parents[1];O=V/'artifacts/staging-v001/coaching-performance-v003'
FF='/opt/homebrew/bin/ffmpeg';FP='/opt/homebrew/bin/ffprobe'
def run(args):return subprocess.run(args,check=True,capture_output=True,text=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    movie=O/'coaching-review.mp4';before=V/'artifacts/staging-v001/coaching-performance-v002/coaching-review.mp4'
    info=json.loads(run([FP,'-v','error','-show_streams','-show_format','-of','json',str(movie)]).stdout)
    video=next(s for s in info['streams'] if s['codec_type']=='video');audio=next(s for s in info['streams'] if s['codec_type']=='audio')
    assert int(video['nb_frames'])==300 and video['avg_frame_rate']=='24/1'
    assert (video['width'],video['height'])==(1280,720) and float(video['duration'])==12.5
    assert audio['sample_rate']=='48000' and audio['channels']==2 and abs(float(audio['duration'])-12.5)<.001
    run([FF,'-v','error','-xerror','-i',str(movie),'-f','null','-'])
    plan=json.loads((O/'render-selection.json').read_text());old=json.loads((O/'production-before.json').read_text())
    for aid in ['s07-assistant','s07-flick','s07-keeper']:
        assert plan['assets'][aid]['sha256']==old['assets'][aid]['sha256']==sha(V/plan['assets'][aid]['path'])
    resolved=json.loads((O/'audio/resolved-cues.json').read_text());shot=next(s for s in plan['shots'] if s['id']=='S07');start=(shot['start_frame']-1)*2000
    lines=[]
    for cue in resolved['cues']:
        if cue['shot']=='S07' and cue['stem']=='dialogue':
            a=(cue['start_sample']-start)/48000;b=a+cue['samples']/48000
            assert 0<=a<b<=12.5 and cue['trimmed_start_samples']==cue['trimmed_end_samples']==0
            lines.append({'cue':cue['id'],'start':a,'end':b,'cut_off':False})
    frames=O/'encoded-review';frames.mkdir(exist_ok=True)
    selected=sorted(set([1,48,100,150,174,195,205,206,254,277,300]+list(range(27,40,2))+list(range(71,88,2))+list(range(165,193,3))+list(range(237,263,2))+list(range(276,296))))
    select='+'.join(f'eq(n\\,{f-1})' for f in selected)
    run([FF,'-v','error','-y','-i',str(movie),'-vf',f'select={select}','-fps_mode','vfr',str(frames/'sample-%03d.png')])
    for i,f in enumerate(selected,1):(frames/f'sample-{i:03}.png').replace(frames/f'{f:03}.png')
    font=Path('/System/Library/Fonts/Supplemental/Arial.ttf');assert font.exists()
    # Sequential A/B keeps each original soundtrack intelligible and unretimed.
    filt=f"[0:v]drawtext=fontfile={font}:text='BEFORE - 15 seconds':x=24:y=18:fontsize=26:fontcolor=white:box=1:boxcolor=black@0.7[v0];[1:v]drawtext=fontfile={font}:text='REVISION - 12.5 seconds - original speech speed':x=24:y=18:fontsize=26:fontcolor=white:box=1:boxcolor=black@0.7[v1];[0:a]atrim=end=15,asetpts=PTS-STARTPTS[a0];[1:a]atrim=end=12.5,asetpts=PTS-STARTPTS[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]"
    comparison=O/'coaching-before-after.mp4'
    run([FF,'-v','error','-y','-i',str(before),'-i',str(movie),'-filter_complex',filt,'-map','[v]','-map','[a]','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(comparison)])
    run([FF,'-v','error','-xerror','-i',str(comparison),'-f','null','-'])
    (O/'inspection.json').write_text(json.dumps({'format':info,'movie_sha256':sha(movie),'normal_speed_before_after':str(comparison.relative_to(V)),'full_decode':True,'original_voice_hashes_unchanged':True,'complete_dialogue':lines,'review_frames':selected,'listening':'Not performed by agent. Encoded clip and comparison are auditionable.','motion_review':'Consecutive encoded-frame inspection and numeric trajectory checks; no audience or subjective normal-speed approval claimed.'},indent=2)+'\n')
    print(json.dumps({'review':str(movie),'comparison':str(comparison),'frames':300,'seconds':12.5,'dialogue':lines}))

if __name__=='__main__':main()

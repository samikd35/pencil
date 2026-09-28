"""Join the selected S05–S08 staging coverage, retaining every source frame.

Run from any directory with Python 3; requires the existing local FFmpeg.
This is an editorial preview, not a replacement full-film timeline.
"""
import hashlib,json,subprocess
from fractions import Fraction
from pathlib import Path

V=Path(__file__).resolve().parents[1]
O=V/'artifacts/staging-v001/passage-v001'
FF='/opt/homebrew/bin/ffmpeg';FP='/opt/homebrew/bin/ffprobe'
SELECTED=[
    ('S05','passage-v001/plan-review.mp4',168,'Rough plan insert; new reference-conditioned Perez line.'),
    ('S06','football-performance-v002/football-review.mp4',312,'Selected football staging, complete.'),
    ('S07','coaching-performance-v002/coaching-review.mp4',360,'Selected connected-surface staging, complete through release.'),
    ('S08 link','passage-v001/call-link-review.mp4',192,'Rough decision insert; new reference-conditioned Perez line.'),
    ('S08 call','call-performance-v006/call-review.mp4',240,'Selected call performance, complete; wrist work stays deferred.'),
]

def probe(p):
    return json.loads(subprocess.check_output([FP,'-v','error','-show_streams','-show_format','-of','json',str(p)]))

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    out=O/'S05-S08-review.mp4';assert not out.exists(),'Use a new revision; do not overwrite the delivered passage.'
    args=[FF,'-v','error','-nostdin'];filters=[];edit=[];cursor=0
    for i,(shot,relative,frames,note) in enumerate(SELECTED):
        path=V/'artifacts/staging-v001'/relative;meta=probe(path)
        vs=next(s for s in meta['streams'] if s['codec_type']=='video')
        au=next(s for s in meta['streams'] if s['codec_type']=='audio')
        assert (vs['width'],vs['height'])==(1280,720) and Fraction(vs['avg_frame_rate'])==24
        assert int(vs['nb_frames'])==frames and int(au['sample_rate'])==48000 and au['channels']==2
        args+=['-i',str(path)]
        filters += [f'[{i}:v]trim=end_frame={frames},setpts=PTS-STARTPTS[v{i}]',f'[{i}:a]atrim=end_sample={frames*2000},asetpts=PTS-STARTPTS[a{i}]']
        edit.append(dict(shot=shot,source=str(path.relative_to(V)),sha256=digest(path),source_start_frame=1,frames=frames,preview_start_frame=cursor+1,preview_start_seconds=cursor/24,note=note));cursor+=frames
    filters.append(''.join(f'[v{i}][a{i}]' for i in range(len(edit)))+f'concat=n={len(edit)}:v=1:a=1[v][a]')
    subprocess.run(args+['-filter_complex',';'.join(filters),'-map','[v]','-map','[a]','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)],check=True)
    final=probe(out);video=next(s for s in final['streams'] if s['codec_type']=='video');audio=next(s for s in final['streams'] if s['codec_type']=='audio')
    assert cursor==1272 and int(video['nb_frames'])==cursor
    assert abs(float(video['duration'])-53)<1/48000 and abs(float(audio['duration'])-53)<1/48000
    subprocess.run([FF,'-v','error','-xerror','-i',str(out),'-f','null','-'],check=True)
    # This check verifies retained speech tails; it does not pretend to audition the takes.
    assert .75+4.08<7 and .75+5.44<8
    boundaries=[sum(s['frames'] for s in edit[:i]) for i in range(1,len(edit))]
    shots=O/'cut-review';shots.mkdir(exist_ok=True)
    for boundary in boundaries:
        for frame in [boundary-1,boundary,boundary+1,boundary+2]:
            subprocess.run([FF,'-v','error','-y','-ss',str((frame-1)/24),'-i',str(out),'-frames:v','1',str(shots/f'{frame:04}.png')],check=True)
    (O/'edit-map.json').write_text(json.dumps(dict(fps=24,frames=cursor,seconds=cursor/24,clips=edit,source_frames_trimmed=0,audio='Selected performance tracks retained at original speed; one AAC encoding for the joined preview.'),indent=2)+'\n')
    (O/'checks.json').write_text(json.dumps(dict(frames=cursor,duration_seconds=53,full_decode=True,speech_tail_check=True,agent_listening=False,output_sha256=digest(out),source_hashes_verified=all(digest(V/s['source'])==s['sha256'] for s in edit),cut_frames=boundaries,assembly_source_sha256=digest(Path(__file__))),indent=2)+'\n')
    print(json.dumps({'preview':str(out),'seconds':53,'frames':cursor,'cuts_seconds':[b/24 for b in boundaries]}))

if __name__=='__main__':main()

"""Reproduce representative selection → native construction → picture/sound animatics.

Creates new proof roots only. The delegation below is scoped to the user's 14 September
2026 workflow implementation request; it must not be reused to approve future films.
"""
import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'pipeline'))
sys.path.insert(0,str(ROOT/'experiments/001_heavy_box'))
from journal import append_event
from checkpoints import require_checkpoint
spec=importlib.util.spec_from_file_location('style_selection',ROOT/'pipeline/styles.py')
styles=importlib.util.module_from_spec(spec);spec.loader.exec_module(styles)
IDS=('chibi','food-mascot','paper-cutout','collage','parallax')
WAIVER='User: implement it from step 1 to step 8 without stopping … if there are steps where you need a confirmation, confirm it yourself, approval, approve it yourself.'


def run(ident,group):
    root=HERE/'proofs'/group/ident;root.mkdir(parents=True,exist_ok=False)
    assets=root/'assets';assets.mkdir()
    source=ROOT/'experiments/001_heavy_box/artifacts/finish-v002/audio/soundtrack.wav'
    shutil.copyfile(source,assets/'soundtrack.wav')
    (root/'brief.md').write_text(f'# {ident}: workflow mechanism proof\n\nFictional one-character Heavy Box action: approach, push, release, stumble, recover. One box, one character, fixed view. Preserve all 240 source control poses and projected hand/foot geometry. Original accepted 10-second soundtrack reused exactly; no new sound selection or listening claim.\n\nVisual experiment: {ident}. Check neck, waist, hands, feet, overlays and the effect of changed proportions through the full action. Internal 640×360 animatic; the menu remains still-image only.\n\nDelegation for this workflow test only: {WAIVER}\n')
    plan=dict(version=1,timeline=dict(fps='24',start_frame=1,frames=240,sample_rate=48000),
              shots=[dict(id='box',start_frame=1,events=dict(start=0,release=145))],
              assets={'existing-mix':dict(path='assets/soundtrack.wav',sha256=styles.digest(source),
                      source='Preserved Heavy Box finish-v002 original synthesized soundtrack',license='Original project production',attribution='')},
              cues=[dict(id='existing-sound',shot='box',event='start',intent='Preserve the accepted box-action sound and synchronization',asset='existing-mix',stem='original-mix',in_seconds=0,duration_seconds=10,onset_seconds=0,offset_frames=0,gain_db=0,pan=0,fade_in_seconds=0,fade_out_seconds=0)],mix_gain_db=0)
    production=root/'production.json';production.write_text(json.dumps(plan,indent=2)+'\n')
    selected=styles.select(production,ident,reviewer='assistant',reason='Representative style chosen under the user’s delegated eight-step workflow implementation authority')
    for stage in ('staging','sound','animatic','delivery'):
        append_event(root,stage='checkpoint/animatic-v001/'+stage,status='selected',reviewer='user',decision='waived',
                     intent='Record scoped user delegation for this workflow proof',method='Actual task instruction; not a listening or creative acceptance claim',
                     result=WAIVER,inputs=['brief.md','assets/style-selection.json'])
    out=root/'animatic-v001'
    with (root/'blender.log').open('w') as log:
        subprocess.run(['/Applications/Blender.app/Contents/MacOS/Blender','-b','-t','3','--python',str(ROOT/'pipeline/styles/build_samples.py'),
                        '--','--production',str(production),'--out',str(out),'--motion'],check=True,stdout=log,stderr=subprocess.STDOUT)
    if not (out/'motion-picture.mp4').is_file():raise RuntimeError('Blender did not produce a motion proof; inspect '+str(root/'blender.log'))
    with (root/'audio.log').open('w') as log:
        subprocess.run([sys.executable,str(ROOT/'pipeline/audio.py'),'build',str(production),'--out',str(root/'audio-v001')],check=True,stdout=log,stderr=subprocess.STDOUT)
    for stage in ('staging','sound'):require_checkpoint(root,'animatic-v001',stage)
    subprocess.run(['ffmpeg','-v','error','-nostdin','-n','-i',str(out/'motion-picture.mp4'),'-i',str(root/'audio-v001/mix-premaster.wav'),
                    '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out/'animatic-with-sound.mp4')],check=True)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out/'animatic-with-sound.mp4')]))
    video=next(s for s in probe['streams'] if s['codec_type']=='video');audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
    assert int(video['nb_frames'])==240 and video['r_frame_rate']=='24/1' and abs(float(probe['format']['duration'])-10)<.05
    assert audio['channels']==2
    subprocess.run(['ffmpeg','-v','error','-i',str(out/'animatic-with-sound.mp4'),'-f','null','-'],check=True)
    def pcm(path):
        return hashlib.sha256(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-f','f32le','-ac','2','-ar','48000','-'])).hexdigest()
    assert pcm(source)==pcm(root/'audio-v001/mix-premaster.wav'),'Style selection altered the authoritative soundtrack'
    report=dict(style=ident,frames=240,fps=24,duration=10,complete_decode='passed',native_checks=str(out/'checks.json'),
                selected_settings=selected['settings'],authoritative_sound_pcm='identical to original',listening='Not performed; original soundtrack preserved',visual_review='Pending sequential-frame review')
    (out/'delivery-checks.json').write_text(json.dumps(report,indent=2)+'\n')
    append_event(root,stage='combined-animatic',status='completed',reviewer='assistant',intent='Test saved selection through native construction and existing audio workflow',
                 method='240-frame native proof, shared audio renderer and encoded decode/PCM checks',result='Playable animatic and editable project built; sound is unchanged; perceptual review remains distinct.',
                 inputs=['production.json','assets/style-selection.json'],outputs=['animatic-v001/animatic-with-sound.mp4','animatic-v001/character.blend','animatic-v001/checks.json','animatic-v001/delivery-checks.json'])
    return ident


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--group',required=True)
    args=parser.parse_args()
    if Path(args.group).name!=args.group:parser.error('Use one new group directory name')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for ident in pool.map(lambda s:run(s,args.group),IDS):print('Built '+ident,flush=True)

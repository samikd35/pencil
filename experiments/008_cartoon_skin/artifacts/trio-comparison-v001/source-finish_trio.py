"""Package the three small native-motion experiments with preserved sound."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'001_heavy_box/artifacts/finish-v002/preview-with-sound.mp4'
OUT=ROOT/'artifacts/trio-comparison-v001'
OUT.mkdir(exist_ok=False)
characters=[('Jude Bellingham','trio-jude-v004'),('Kylian Mbappe','trio-mbappe-v003'),('Vinicius Junior','trio-vini-v004')]
for node in ast.parse((ROOT/'finish_proof.py').read_text()).body:
    if isinstance(node,ast.FunctionDef) and node.name in {'run','audio_hash'}:
        exec(compile(ast.Module(body=[node],type_ignores=[]),'finish_proof.py','exec'))
ff=['ffmpeg','-hide_banner','-loglevel','error','-n']
checks={}
cards=[]
for label,revision in characters:
    folder=ROOT/'artifacts'/revision
    movie=folder/'cartoon-with-sound.mp4'
    run(ff+['-i',str(folder/'cartoon-picture.mp4'),'-i',str(BASE),'-map','0:v:0','-map','1:a:0',
        '-c','copy','-movflags','+faststart',str(movie)])
    assert audio_hash(movie)==audio_hash(BASE)
    run(ff+['-i',str(movie),'-vf',r'select=not(mod(n\,10)),tile=6x4','-frames:v','1','-update','1',str(folder/'motion-sheet.png')])
    card=OUT/(revision+'.mp4');cards.append(card)
    run(ff+['-i',str(movie),'-vf',f"pad=640:402:0:42:color=0xfff9ed,drawtext=text='{label}':x=22:y=12:fontsize=21:fontcolor=0x3b1917",
        '-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(card)])
    data=json.loads(run(['ffprobe','-v','error','-show_streams','-of','json',str(movie)]).stdout)
    video=next(s for s in data['streams'] if s['codec_type']=='video')
    assert video['nb_frames']=='240' and video['r_frame_rate']=='24/1' and float(video['duration'])==10
    run(['ffmpeg','-v','error','-i',str(movie),'-f','null','-'])
    checks[label]={'revision':revision,'frames':240,'seconds':10,'fps':24,'complete_decode':'passed',
        'original_audio_identical':True,'native_project':str((folder/'cartoon-skin.blend').relative_to(ROOT))}
concat=OUT/'clips.txt';concat.write_text(''.join(f"file '{p.name}'\n" for p in cards))
review=OUT/'three-player-motion-test.mp4'
run(ff+['-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(review)])
data=json.loads(run(['ffprobe','-v','error','-show_streams','-of','json',str(review)]).stdout)
video=next(s for s in data['streams'] if s['codec_type']=='video')
assert video['nb_frames']=='720' and abs(float(video['duration'])-30)<.1
run(['ffmpeg','-v','error','-i',str(review),'-f','null','-'])

# These are new native camera renders of the saved projects, not bitmap head textures.
for label,revision in characters:
    folder=ROOT/'artifacts'/revision
    portrait=folder/'native-portrait.png'
    code=("import bpy; s=bpy.context.scene; s.frame_set(1); "
          "s.camera.location.x=-4.45; s.camera.location.y=2.75; s.camera.data.ortho_scale=6; "
          "s.render.resolution_x=512; s.render.resolution_y=768; s.render.resolution_percentage=100; "
          "s.eevee.taa_render_samples=32; s.render.filepath="+repr(str(portrait))+"; bpy.ops.render.render(write_still=True)")
    run(['/Applications/Blender.app/Contents/MacOS/Blender','-b',str(folder/'cartoon-skin.blend'),'--python-expr',code])
inputs=[];filters=[]
for i,(label,revision) in enumerate(characters):
    inputs+=['-i',str(ROOT/'artifacts'/revision/'native-portrait.png')]
    filters.append(f"[{i}:v]pad=512:822:0:54:color=0xfff9ed,drawtext=text='{label}':x=(w-tw)/2:y=17:fontsize=24:fontcolor=0x3b1917[p{i}]")
filters.append('[p0][p1][p2]hstack=inputs=3[v]')
run(ff+inputs+['-filter_complex',';'.join(filters),'-map','[v]','-frames:v','1','-update','1',str(OUT/'native-lineup.png')])
checks['comparison']={'frames':720,'seconds':float(video['duration']),'sha256':hashlib.sha256(review.read_bytes()).hexdigest(),
    'scope':'Three independent executions of the fictional box-action test, using the same original timing and sound.',
    'limits':'Reference-angle head regions move as a unit; facial expression changes and head turns remain untested. Likeness awaits user review.'}
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
(OUT/'source-finish_trio.py').write_bytes(Path(__file__).read_bytes())
sys.path.insert(0,str(ROOT.parent/'001_heavy_box'))
from journal import append_event
append_event(ROOT,stage='checkpoint/trio-comparison-v001/staging',status='pending_review',
    intent='Review the user-requested three-player cartoon treatment in motion',
    method='Three 10-second curve/mesh action proofs, original decoded sound, native portrait lineup, saved/reopened controller checks',
    inputs=['build_trio.py','prepare_trio.py','finish_trio.py'],
    outputs=[str((OUT/n).relative_to(ROOT)) for n in ('three-player-motion-test.mp4','native-lineup.png','checks.json')],
    result='Three playable 240-frame tests and 720-frame compilation decode. Each individual clip preserves original decoded audio. No new historical event or canonical design approval inferred.')
print('TRIO_COMPARISON_COMPLETE',OUT)

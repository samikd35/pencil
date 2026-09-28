"""Assemble the same-design curve/mesh versus native Grease Pencil comparison."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
revision=sys.argv[1]
assert Path(revision).name==revision
OUT=ROOT/'artifacts'/revision
BASE=ROOT/'artifacts/coherent-proof-v003/cartoon-with-sound.mp4'
sys.path.insert(0,str(ROOT.parent/'001_heavy_box'))
from journal import append_event
names={'run','audio_hash'}
defs=[n for n in ast.parse((ROOT/'finish_proof.py').read_text()).body
      if isinstance(n,ast.FunctionDef) and n.name in names]
exec(compile(ast.Module(body=defs,type_ignores=[]),str(ROOT/'finish_proof.py'),'exec'))
ff=['ffmpeg','-hide_banner','-loglevel','error','-n']
picture=OUT/'cartoon-picture.mp4'
movie=OUT/'grease-pencil-with-sound.mp4'
comparison=OUT/'curves-vs-grease-pencil.mp4'
run(ff+['-i',str(picture),'-i',str(BASE),'-map','0:v:0','-map','1:a:0',
        '-c','copy','-movflags','+faststart',str(movie)])
graph=("[0:v]pad=640:404:0:44:color=0xfff9ed,drawtext=text='CURVES + FLAT MESHES':x=24:y=14:fontsize=20:fontcolor=0x25394c[a];"
       "[1:v]pad=640:404:0:44:color=0xfff9ed,drawtext=text='NATIVE GREASE PENCIL':x=24:y=14:fontsize=20:fontcolor=0x25394c[b];[a][b]hstack[v]")
run(ff+['-i',str(BASE),'-i',str(picture),'-filter_complex',graph,'-map','[v]','-map','0:a:0',
        '-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(comparison)])
run(ff+['-i',str(comparison),'-vf',"select='eq(n,117)'",'-frames:v','1','-update','1',str(OUT/'comparison.png')])
run(ff+['-i',str(movie),'-vf',r'select=not(mod(n\,10)),tile=6x4','-frames:v','1','-update','1',str(OUT/'motion-sheet.png')])
checks={}
for path in (movie,comparison):
    data=json.loads(run(['ffprobe','-v','error','-show_streams','-of','json',str(path)]).stdout)
    video=next(s for s in data['streams'] if s['codec_type']=='video')
    audio=next(s for s in data['streams'] if s['codec_type']=='audio')
    assert video['nb_frames']=='240' and video['r_frame_rate']=='24/1'
    assert abs(float(video['duration'])-10)<.001
    assert audio['sample_rate']=='48000' and audio['channels']==2
    run(['ffmpeg','-v','error','-i',str(path),'-f','null','-'])
    checks[path.name]={'frames':240,'seconds':10,'fps':24,'width':video['width'],'height':video['height'],
        'complete_decode':'passed','sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
assert audio_hash(BASE)==audio_hash(movie)==audio_hash(comparison)
checks['original_decoded_sound_preserved']=True
checks['review_limit']='Native pose and encoded sample inspection; full subjective playback acceptance remains with the user.'
(OUT/'video-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
(OUT/'source-finish_gp.py').write_bytes(Path(__file__).read_bytes())
append_event(ROOT,stage='checkpoint/'+revision+'/staging',status='pending_review',
    intent='Compare native Grease Pencil with the same curve/mesh character and action',
    method='Ten-second same-design audiovisual comparison and saved native project',
    inputs=['build_gp.py','finish_gp.py','artifacts/coherent-proof-v003/cartoon-skin.blend'],
    outputs=[str((OUT/name).relative_to(ROOT)) for name in
        ('curves-vs-grease-pencil.mp4','grease-pencil-with-sound.mp4','comparison.png',
         'cartoon-skin.blend','checks.json','video-checks.json')],
    result='Both movies decode completely; original sound is unchanged. Native GP controls, geometry checks and the reopened-project hand-edit check pass. Visual playback review remains pending.',
    decision='Judge whether native GP preserves the current look and movement before expanding its tested range.')
print(json.dumps(checks,indent=2))

"""Compare all original animated geometry with the base, then validate effect and audio dependencies."""
import hashlib
import json
import math
from pathlib import Path
import wave
import bpy

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/finish-v002'

def snapshot(names):
    hashes=[]
    for frame in range(1,241):
        bpy.context.scene.frame_set(frame)
        graph=bpy.context.evaluated_depsgraph_get()
        values=[]
        for name in names:
            obj=bpy.data.objects[name].evaluated_get(graph)
            record=[name,[list(row) for row in obj.matrix_world]]
            if obj.type=='CURVE':
                for spline in obj.data.splines:
                    record.append([list(p.co) for p in spline.points])
                    record.append([[list(p.co),list(p.handle_left),list(p.handle_right)] for p in spline.bezier_points])
            elif obj.type=='MESH':
                record.append([list(p.co) for p in obj.data.vertices])
            values.append(record)
        hashes.append(hashlib.sha256(json.dumps(values,separators=(',',':')).encode()).hexdigest())
    return hashes

bpy.ops.wm.open_mainfile(filepath=str(ROOT/'artifacts/rough-v005/character-and-motion.blend'))
names=sorted(bpy.data.objects.keys())
base=snapshot(names)
base_camera=bpy.context.scene.camera.data.ortho_scale
bpy.ops.wm.open_mainfile(filepath=str(OUT/'character-and-effects.blend'))
finished=snapshot(names)
assert base==finished,'Original motion or geometry changed'
assert bpy.context.scene.camera.data.ortho_scale==base_camera
for f in range(1,241):
    bpy.context.scene.frame_set(f)
    for name in ('Effort spark left','Effort spark right'):
        active=bpy.data.objects[name].scale.x>0
        assert active==(128<f<146)
paths=[]
for sound in bpy.data.sounds:
    path=Path(bpy.path.abspath(sound.filepath)).resolve()
    assert path.is_file()
    paths.append(str(path.relative_to(OUT)))
    assert sound.filepath.startswith('//')
with wave.open(str(OUT/'audio/soundtrack.wav')) as audio:
    assert audio.getnframes()==480000 and audio.getframerate()==48000
    assert audio.getnchannels()==2
report={'status':'passed','preserved_frames':240,'original_objects_checked':len(names),
    'check':'Exact per-frame SHA-256 equality of original world transforms, mesh vertices and evaluated curve coordinates/handles',
    'base_frame_hashes':base,'finished_frame_hashes':finished,
    'audio_paths':paths,'audio_seconds':10,'audio_sample_rate':48000,'audio_channels':2,
    'sparks_visible_frames':[129,145],
    'limits':'Palette changes intentionally alter pixels. Checks preserve original character motion and geometry, not pixel colors. Sound quality still needs playback review.'}
(OUT/'verified-finish.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'Passed: all 240 frames of {len(names)} original objects preserved; sound resolves locally; sparks limited to frames 129–145.')

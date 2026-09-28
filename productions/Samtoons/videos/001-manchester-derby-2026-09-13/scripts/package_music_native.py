"""Package the revised mix into a separate copy of the delivered native file."""
import hashlib
import json
from pathlib import Path
import bpy

root=Path(__file__).resolve().parents[1]
out=root/'artifacts/delivery-v002'
bpy.ops.wm.open_mainfile(filepath=str(root/'artifacts/delivery-v001/samtoons-final.blend'))
master=bpy.data.scenes['SAMTOONS / repaired complete animatic']
strips=master.sequence_editor.strips
sounds=[s for s in strips if s.type=='SOUND']
assert len(sounds)==1 and master.frame_end==3768
old=sounds[0]
assert old.frame_final_start==1 and old.volume==1 and not old.mute
channel=old.channel
strips.remove(old)
new=strips.new_sound('Approved foreground + music',str(out/'mix-review.wav'),channel=channel,frame_start=1)
new.volume=1
new.sound.pack()
assert new.frame_final_duration==3768 and new.sound.packed_file is not None
assert hashlib.sha256(new.sound.packed_file.data).hexdigest()==hashlib.sha256((out/'mix-review.wav').read_bytes()).hexdigest()
edit=json.loads((out/'edit.json').read_text())
for row in edit:
    s=next(s for s in strips if s.type=='SCENE' and s.scene.name==row['scene'])
    assert s.frame_final_start==row['start_frame'] and s.frame_final_duration==row['frames']
bpy.context.window.scene=master
master.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'samtoons-with-music.blend'))
(out/'native-checks.json').write_text(json.dumps(dict(scene_strips=17,frames=3768,
    packed_mix_sha256=hashlib.sha256(new.sound.packed_file.data).hexdigest(),
    mix_packed=True,timeline_preserved=True,original_native_unchanged=True),indent=2))
print('MUSIC_NATIVE_PACKAGED')

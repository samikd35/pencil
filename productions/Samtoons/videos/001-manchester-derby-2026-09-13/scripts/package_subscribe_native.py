"""Append the standalone card and updated packed mix to a new native copy."""
import hashlib
import json
from pathlib import Path
import bpy

root=Path(__file__).resolve().parents[1]
out=root/'artifacts/delivery-v003'
bpy.ops.wm.open_mainfile(filepath=str(root/'artifacts/delivery-v002/samtoons-with-music.blend'))
master=bpy.data.scenes['SAMTOONS / repaired complete animatic'];strips=master.sequence_editor.strips
sounds=[s for s in strips if s.type=='SOUND'];assert len(sounds)==1
channel=sounds[0].channel;strips.remove(sounds[0])
new=strips.new_sound('Revised Enzo + music + ending',str(out/'mix-review.wav'),channel=channel,frame_start=1)
new.sound.pack();new.volume=1
assert new.frame_final_duration==3864
card=strips.new_image('Subscribe for more',str(out/'subscribe-card.png'),channel=1,frame_start=3769)
card.frame_final_duration=96
master.frame_end=3864
assert len([s for s in strips if s.type=='SCENE'])==17
assert hashlib.sha256(new.sound.packed_file.data).hexdigest()==hashlib.sha256((out/'mix-review.wav').read_bytes()).hexdigest()
bpy.context.window.scene=master;master.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'samtoons-final.blend'))
(out/'native-checks.json').write_text(json.dumps(dict(scene_strips=17,end_card_frames=96,
    frames=3864,packed_mix_sha256=hashlib.sha256(new.sound.packed_file.data).hexdigest(),
    required_external_asset='subscribe-card.png',no_scene_render=True),indent=2))
print('REVISION_NATIVE_PACKAGED')

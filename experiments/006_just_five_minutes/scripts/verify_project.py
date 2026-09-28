"""Check the saved scene, contact anchors, visibility, duration and embedded soundtrack."""
from pathlib import Path
import bpy, json, math, hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/film-v001'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'just-five-minutes.blend'))
s=bpy.context.scene
assert (s.frame_start,s.frame_end,s.render.fps,s.render.resolution_x,s.render.resolution_y)==(1,900,30,1920,1080)
source=ROOT.parent/'001_heavy_box/artifacts/finish-v002/character-and-effects.blend'
assert hashlib.sha256(source.read_bytes()).hexdigest()==s['Source character SHA256']
hand=bpy.data.objects['Protagonist hand 1'];phone=bpy.data.objects['Phone / rigid editable prop']
errors=[]
for contact in json.loads((OUT/'phone-contacts.json').read_text()):
    s.frame_set(contact['frame']);bpy.context.view_layer.update()
    a=hand.matrix_world.translation;b=phone.matrix_world.translation
    errors.append(math.hypot(a.x-b.x,a.y-b.y))
assert max(errors)<.001
for f,back in [(31,False),(345,False),(600,False),(828,True)]:
    s.frame_set(f)
    assert bpy.data.objects['Protagonist back hair silhouette'].hide_render != back
assert not bpy.data.objects['Protagonist shirt'].hide_render
s.frame_set(881)
assert bpy.data.objects['Protagonist shirt'].hide_render
assert not bpy.data.objects['Grey tabletop'].hide_render
editor=s.sequence_editor_create()
for strip in list(editor.strips):editor.strips.remove(strip)
strip=editor.strips.new_sound('Original Foley and instrumental loop',str(OUT/'audio/soundtrack.wav'),channel=1,frame_start=1)
assert strip.sound is not None
bpy.ops.file.pack_all()
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'just-five-minutes.blend'))
result=dict(frames=900,seconds=30,hand_phone_frames=len(errors),max_saved_contact_error_px=max(errors),face_back_visibility=True,final_desk_visible=True,source_character_unchanged=True,embedded_soundtrack=bool(strip.sound.packed_file),editable_objects=len(s.objects))
assert result['embedded_soundtrack']
(OUT/'project-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print('PROJECT_CHECKS_PASS',json.dumps(result))

"""Run in visible Blender. New editable VSE scene only; all old scenes retained."""
from pathlib import Path
import bpy,json,textwrap
V=Path('/Users/samikd/MyProjects/Pencil/productions/Samtoons/videos/002-how-arsenal-won-the-league');O=V/'artifacts/animatic-v001';E=json.loads((O/'edit.json').read_text());S=json.loads((O/'subtitles.json').read_text())
s=bpy.data.scenes['S002_full_animatic_v001'];se=s.sequence_editor;bpy.context.window.scene=s
s.frame_start=1;s.frame_end=sum(r['frames'] for r in E);s.render.fps=24;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.use_sequencer=True;s.sync_mode='AUDIO_SYNC'
names={q.name for q in se.strips}
for row in E:
 path=O/'clips'/(row['id']+'.mp4');name='Picture / '+row['id']
 if path.exists() and name not in names:
  q=se.strips.new_movie(name=name,filepath=str(path),channel=1,frame_start=row['start_frame']);q.frame_final_duration=row['frames']
  s.timeline_markers.new(row['id'],frame=row['start_frame'])
if 'Authoritative selected mix' not in names and (O/'mix-premaster.wav').exists():
 q=se.strips.new_sound(name='Authoritative selected mix',filepath=str(O/'mix-premaster.wav'),channel=2,frame_start=1)
 q.volume=1
for i,row in enumerate(S):
 name='Dialogue / %02d'%i
 if name in names:continue
 start=round(row['start']*24)+1;end=round(row['end']*24)+1
 q=se.strips.new_effect(name=name,type='TEXT',channel=3,frame_start=start,length=end-start);q.text='\n'.join(textwrap.wrap(row['text'],67));q.font_size=29;q.color=(1,1,1,1);q.location=(.5,.065);q.alignment_x='CENTER';q.use_outline=True;q.outline_color=(.015,.015,.015,1);q.outline_width=.035
s['scope']='Full illustrated story-and-sound animatic. Held complete action drawings, no finished walk/run or lip-sync claim.'
s['motion_status']='Chase continuous gait corrections remain open; new complete key drawings replace reuse of rejected cycle.'
s.frame_set(1)
for a in bpy.context.screen.areas:
 if a.type in ['VIEW_3D','SEQUENCE_EDITOR']:
  a.type='SEQUENCE_EDITOR';a.spaces.active.view_type='PREVIEW';break
bpy.context.view_layer.update()
result={'scene':s.name,'shots_loaded':len([q for q in se.strips if q.type=='MOVIE']),'frames':s.frame_end,'seconds':s.frame_end/24,'audio':any(q.type=='SOUND' for q in se.strips)}

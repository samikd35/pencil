"""Checkpoint proofs are cheap; full quality requires current user-reviewed decisions."""
from pathlib import Path
import os,sys,bpy
ROOT=Path(__file__).resolve().parents[1];REV=os.environ.get('PENCIL_REVISION','film-v003');OUT=ROOT/'artifacts'/REV
sys.path.insert(0,str(ROOT.parents[1]));from pipeline.checkpoints import require_checkpoint
mode='full' if '--full' in sys.argv else 'animatic' if '--animatic' in sys.argv else 'proof'
if mode!='proof':
    for stage in ('staging','sound') + (('animatic',) if mode=='full' else ()):
        require_checkpoint(ROOT,REV,stage)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'trent-corner-advanced.blend'))
s=bpy.context.scene;s.render.use_sequencer=False
s.render.resolution_percentage=100 if mode=='full' else 50;s.eevee.taa_render_samples=32 if mode=='full' else 16
s.frame_start=241 if mode=='proof' else 1;s.frame_end=528 if mode=='proof' else 912
s.render.image_settings.media_type='VIDEO';s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.ffmpeg.constant_rate_factor='HIGH';s.render.ffmpeg.ffmpeg_preset='GOOD';s.render.ffmpeg.audio_codec='NONE'
s.render.filepath=str(OUT/('staging-picture.mp4' if mode=='proof' else mode+'-picture.mp4'))
bpy.ops.render.render(animation=True)
print('RENDERED',mode,flush=True)

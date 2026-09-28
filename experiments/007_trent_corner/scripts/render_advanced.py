"""Native FFmpeg animation output avoids per-frame temporary PNG files."""
from pathlib import Path
import os
import bpy
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts'/os.environ.get('PENCIL_REVISION','film-v002')
bpy.ops.wm.open_mainfile(filepath=str(OUT/'trent-corner-advanced.blend'))
s=bpy.context.scene;s.render.resolution_percentage=100;s.render.use_sequencer=False
s.render.image_settings.media_type='VIDEO';s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264'
s.render.ffmpeg.constant_rate_factor='HIGH';s.render.ffmpeg.ffmpeg_preset='GOOD';s.render.ffmpeg.audio_codec='NONE'
s.render.threads_mode='FIXED';s.render.threads=2;s.render.filepath=str(OUT/'picture-master.mp4')
bpy.ops.render.render(animation=True)
print('PICTURE_MASTER_COMPLETE',flush=True)

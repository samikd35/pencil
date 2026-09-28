"""One dialogue replacement plus an independently encoded four-second end card."""
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from build_music_audition import ROOT, SR, FF, run, decode, wav, dip, sha

OLD=ROOT/'artifacts/delivery-v002'
OUT=ROOT/'artifacts/delivery-v003'
VOICE=ROOT/'assets/film-voices-v004'


def main():
    OUT.mkdir(exist_ok=False)
    voice=VOICE/'enzo.wav'
    run([FF,'-v','error','-y','-i',VOICE/'enzo-raw.wav','-af',
        'silenceremove=start_periods=1:start_duration=0.015:start_threshold=-45dB:start_silence=0.025,areverse,silenceremove=start_periods=1:start_duration=0.015:start_threshold=-45dB:start_silence=0.08,areverse,highpass=f=65,afade=t=in:d=0.005',
        '-ar',str(SR),'-ac','1','-c:a','pcm_s24le',voice])
    foreground=decode(ROOT/'artifacts/delivery-v001/mix-review.wav',0,157)
    current=decode(OLD/'mix-review.wav',0,157)
    music=decode(OLD/'music-ducked.wav',0,157)
    line=decode(voice,0,3)
    start=5730000;old_length=23884
    assert .3*SR<len(line)<2*SR
    # The resolved source timeline has no other cues within this isolated reply.
    resolved=json.loads((ROOT/'artifacts/animatic-v004/mix/resolved-cues.json').read_text())
    overlapping=[c['id'] for c in resolved['cues'] if c['start_sample']<start+len(line)
                 and c['start_sample']+c['samples']>start]
    assert overlapping==['dialogue_14'],overlapping
    assert np.max(np.abs(foreground[start+old_length:start+len(line)]))<1e-5
    old=foreground[start:start+old_length]
    def active_rms(a):
        m=np.mean(a*a,axis=1);return np.sqrt(np.mean(m[m>np.max(m)*.01]))
    gain=float(active_rms(old)/active_rms(line))
    gain=min(gain,float(.69/np.max(np.abs(line))))
    line*=gain
    wav(OUT/'enzo-selected.wav',line)
    revised_foreground=foreground.copy()
    revised_foreground[start:start+old_length]=0
    revised_foreground[start:start+len(line)]+=line
    # Additional space around the extended reply; all other music samples preserved.
    t=np.arange(len(music))/SR
    extra_db=dip(t,start/SR,(start+len(line))/SR,-5)
    revised_music=music*10**(extra_db[:,None]/20)
    mixed=revised_foreground+revised_music
    changed=(np.arange(len(music))>=start-round(.12*SR)) & (np.arange(len(music))<start+len(line)+round(.35*SR)+1)
    assert np.max(np.abs(mixed[~changed]-current[~changed]))<1e-6
    assert np.isfinite(mixed).all() and np.max(np.abs(mixed))<.95
    # Standalone end card: native 1920x1080 typography, no alteration of film frames.
    im=Image.new('RGB',(1920,1080),'#101d24');d=ImageDraw.Draw(im)
    bold='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
    regular='/System/Library/Fonts/Supplemental/Arial.ttf'
    d.rounded_rectangle((750,214,1170,222),radius=4,fill='#64d8ac')
    d.text((960,305),'SAMTOONS',font=ImageFont.truetype(bold,38),fill='#64d8ac',anchor='mm',stroke_width=0)
    d.text((960,501),'Subscribe for more',font=ImageFont.truetype(bold,112),fill='#ffffff',anchor='mm')
    d.text((960,629),'FOOTBALL. DRAMA. COMEDY.',font=ImageFont.truetype(regular,32),fill='#b8c8ce',anchor='mm')
    d.rounded_rectangle((750,794,1170,802),radius=4,fill='#64d8ac')
    im.save(OUT/'subscribe-card.png')
    run([FF,'-v','error','-y','-loop','1','-framerate','24','-i',OUT/'subscribe-card.png',
         '-frames:v','96','-an','-c:v','libx264','-preset','fast','-crf','14','-profile:v','high','-level:v','4.0',
         '-pix_fmt','yuv420p','-color_range','tv','-color_primaries','bt709','-color_trc','iec61966-2-1',
         '-video_track_timescale','12288',OUT/'subscribe-picture.mp4'])
    # Only this independent card is encoded; the existing film is packet-copied.
    original=ROOT/'artifacts/delivery-v001/picture-selected.mp4'
    (OUT/'concat-picture.txt').write_text(f"file '{original}'\nfile '{OUT/'subscribe-picture.mp4'}'\n")
    run([FF,'-v','error','-y','-f','concat','-safe','0','-i',OUT/'concat-picture.txt',
         '-map','0:v:0','-c:v','copy',OUT/'picture-selected.mp4'])
    tail=decode(ROOT/'artifacts/music-v001/weasel-normalized.wav',44,4)*10**(-3/20)
    envelope=np.minimum(np.clip(np.arange(len(tail))/(SR*.2),0,1),np.clip((len(tail)-1-np.arange(len(tail)))/(SR*.7),0,1))
    tail*=envelope[:,None]
    wav(OUT/'music-ducked.wav',np.concatenate([revised_music,tail]))
    wav(OUT/'mix-review.wav',np.concatenate([mixed,tail]))
    wav(OUT/'subscribe-music.wav',tail)
    run([FF,'-v','error','-y','-i',OUT/'subscribe-picture.mp4','-i',OUT/'subscribe-music.wav',
         '-c:v','copy','-c:a','aac','-b:a','320k','-movflags','+faststart',OUT/'subscribe-card.mp4'])
    target=OUT/'samtoons-final-1080p.mp4'
    run([FF,'-v','error','-y','-i',OUT/'picture-selected.mp4','-i',OUT/'mix-review.wav',
         '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','320k','-movflags','+faststart',target])
    run([FF,'-v','error','-xerror','-i',target,'-f','null','-'])
    probe=json.loads(run(['/opt/homebrew/bin/ffprobe','-v','error','-show_streams','-show_format','-of','json',target]).stdout)
    video=next(s for s in probe['streams'] if s['codec_type']=='video')
    assert int(video['nb_frames'])==3864 and video['r_frame_rate']=='24/1'
    assert (video['width'],video['height'])==(1920,1080) and abs(float(probe['format']['duration'])-161)<.05
    hashes=[]
    for p in [original,target]:
        hashes.append(run([FF,'-v','error','-i',p,'-map','0:v:0','-frames:v','3768','-c:v','copy','-f','hash','-hash','sha256','-']).stdout.strip())
    assert hashes[0]==hashes[1], 'Original film packets changed'
    stats=run([FF,'-hide_banner','-i',target,'-af','loudnorm=print_format=json','-f','null','-']).stderr
    levels=json.JSONDecoder().raw_decode(stats[stats.rfind('{'):])[0];assert float(levels['input_tp'])<=-1
    (OUT/'revision.json').write_text(json.dumps(dict(text='It is Enzo!',character='Maresca',
        start_seconds=start/SR,voice_duration=len(line)/SR,voice_gain=gain,
        voice_source=str(voice.relative_to(ROOT)),voice_sha256=sha(voice),
        changed_audio_window=[(start-round(.12*SR))/SR,(start+len(line)+round(.35*SR)+1)/SR],
        extra_music_duck_db=-5,end_card_start=157,end_card_seconds=4,
        selected_music='Scheming Weasel (faster version), source seconds 44–48, same approved source',
        agent_listening=False),indent=2))
    (OUT/'delivery-checks.json').write_text(json.dumps(dict(frames=3864,seconds=161,
        fps=24,resolution=[1920,1080],full_decode=True,original_film_picture_hash=hashes[0],
        original_picture_preserved=True,original_mix_unchanged_outside_reply=True,
        encoded_levels=levels,sha256=sha(target),full_review='pending'),indent=2))
    shutil.copy2(OLD/'CREDITS.txt',OUT/'CREDITS.txt')
    page=(OLD/'review.html').read_text().replace('samtoons-with-music-1080p.mp4','samtoons-final-1080p.mp4')
    page=page.replace('samtoons-with-music.blend','samtoons-final.blend').replace('2:37','2:41').replace('157.00','161.00').replace('v.duration||157','v.duration||161')
    page=page.replace('Approved music direction applied across the film. Original picture, voices and effects preserved.',
        'Frustrated “It is Enzo!” reply updated. A separate four-second Subscribe for more card is appended. Original animation preserved.')
    page=page.replace('The excerpt music treatment is approved. This complete mix is ready for your playback review.',
        'Audio correction and end card are ready for review.')
    page=page.replace('Play revised VAR scene · 1:04','Play corrected reply · 1:55').replace('<button data-time="64">Play corrected','<button data-time="115">Play corrected')
    page=page.replace('<script>','<p><a href="subscribe-card.mp4">Standalone end card</a> · <a href="enzo-selected.wav">New reply alone</a></p><div class="chapters"><button data-time="157">Play Subscribe card · 2:37</button></div><script>')
    a=page.index('fetch(');b=page.index("document.getElementById('replay').onclick",a)
    page=page[:a]+"function ready(){playerButtons.forEach(b=>b.disabled=false);document.getElementById('clock').textContent='Ready · 2:41'};v.addEventListener('loadedmetadata',ready);if(v.readyState>=1)ready();v.addEventListener('error',()=>{document.getElementById('clock').textContent='Use the MP4 download if playback is unavailable'});"+page[b:]
    page=page.replace('preload="metadata"','preload="auto"')
    (OUT/'review.html').write_text(page)
    (OUT/'README.md').write_text('''# Enzo correction and Subscribe ending

2:41, 1920×1080, 24fps. The original 3768 video packets are preserved; only the new 96-frame end card was independently encoded and appended. No Blender scene was rerendered. The original film mix remains unchanged outside the recorded correction window. The new local Qwen performance says “It is Enzo!” with frustrated direction, using the same coach description and seed. Timing is unchanged, so the original face/mouth animation remains as requested for this audio-only edit.

The existing approved music is reduced beneath the longer reply. Four seconds from the same approved mischievous track accompany the end card. CREDITS.txt stays separate; no music credits are drawn into the picture.

Reproduce using scripts/finish_enzo_subscribe.py with a fresh output directory. The selected take, full mix, isolated music, standalone end card, frame PNG, revision parameters and technical checks are included. Full playback/voice acting review is pending; agent listening is unavailable.
''')
    print('REVISION_READY',target,flush=True)


if __name__=='__main__':main()

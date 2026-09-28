"""Two contextual music excerpts; preserve accepted picture and foreground audio."""
import hashlib
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
sys.path.insert(0, str(REPO))
from pipeline.audio import build, run, probe

OUT = ROOT / 'artifacts/music-v001'
ASSETS = ROOT / 'assets/music-v001'
DELIVERY = ROOT / 'artifacts/delivery-v001'
FF = '/opt/homebrew/bin/ffmpeg'
SR = 48000


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def decode(p, start, duration):
    return np.frombuffer(subprocess.check_output([FF, '-v', 'error', '-ss', str(start),
        '-i', str(p), '-t', str(duration), '-ar', str(SR), '-ac', '2',
        '-f', 'f32le', '-']), dtype='<f4').reshape(-1, 2).copy()


def wav(p, samples):
    subprocess.run([FF, '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR),
        '-ac', '2', '-i', '-', '-c:a', 'pcm_f32le', str(p)],
        input=samples.astype('<f4').tobytes(), check=True)


def dip(t, start, end, depth):
    # Smooth 120ms lead and 350ms release, with no changes to the voices.
    return depth * np.minimum(np.clip((t-start+.12)/.12, 0, 1),
                               np.clip((end+.35-t)/.35, 0, 1))


def main():
    OUT.mkdir(exist_ok=False)
    tracks = json.loads((ASSETS/'selected-tracks.json').read_text())
    credits = []
    assets = {}
    for track, key in zip(tracks, ['funk', 'weasel']):
        assert ('Funkorama' in track['title']) == (key == 'funk')
        source = ASSETS/track['filename']
        measurement = run([FF, '-hide_banner', '-i', source,
                           '-af', 'loudnorm=print_format=json', '-f', 'null', '-']).stderr
        stats = json.JSONDecoder().raw_decode(measurement[measurement.rfind('{'):])[0]
        # Constant gain preserves the track's original dynamics.
        normalized = OUT/f'{key}-normalized.wav'
        run([FF, '-v', 'error', '-y', '-i', source, '-af',
             f"volume={-23-float(stats['input_i'])}dB", '-ar', str(SR), '-ac', '2',
             '-c:a', 'pcm_f32le', normalized])
        url = 'https://incompetech.com/music/royalty-free/index.html?Search=Search&isrc='+track['isrc']
        credit = f'"{track["title"]}" by Kevin MacLeod (incompetech.com)\n{url}\nLicensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/\nEdited excerpts, fades and volume ducking for this video.'
        credits.append(credit)
        assets[key] = dict(path=str(normalized), sha256=sha(normalized), source=url,
            license='CC BY 4.0', attribution=credit,
            notes=f'Original file SHA256 {sha(source)}; source measured {stats["input_i"]} LUFS; constant gain to -23 LUFS.')
    (OUT/'CREDITS.txt').write_text('\n\n'.join(credits)+'\n')
    original = json.loads((DELIVERY/'plan.json').read_text())
    shots = {s['id']:s for s in original['shots']}
    voices=[]
    for c in original['cues']:
        if c['stem'] not in ('dialogue','vocal-reaction'): continue
        s=shots[c['shot']]
        start=(s['start_frame']-1+s['events'][c['event']]+float(Fraction(str(c.get('offset_frames',0)))))/24-float(Fraction(str(c.get('onset_seconds',0))))
        voices.append((start,start+float(Fraction(str(c['duration_seconds'])))))
    results=[]
    for name, start, duration, placements in [
        ('goal-var',53,29,[('funk',0,10.8,0),('weasel',10.8,18.2,0)]),
        ('fishing',138,19,[('weasel',0,19,24)])]:
        folder=OUT/name;folder.mkdir()
        cues=[dict(id=f'{key}-{i}',shot='excerpt',event='start',asset=key,stem='music',
            intent='Rhythmic action support' if key=='funk' else 'Mischievous VAR/fishing motif',
            offset_frames=str(Fraction(str(at))*24),in_seconds=offset,
            duration_seconds=str(length),gain_db=-3,fade_in_seconds=.15,
            fade_out_seconds=.6) for i,(key,at,length,offset) in enumerate(placements)]
        plan=dict(version=1,timeline=dict(fps=24,start_frame=1,frames=duration*24,sample_rate=SR),
            shots=[dict(id='excerpt',start_frame=1,events=dict(start=0))],assets=assets,cues=cues)
        planpath=folder/'plan.json';planpath.write_text(json.dumps(plan,indent=2))
        build(planpath,folder/'audio')
        music=decode(folder/'audio/stems/music.wav',0,duration)
        foreground=decode(DELIVERY/'mix-review.wav',start,duration)
        assert music.shape==foreground.shape==(duration*SR,2)
        t=np.arange(duration*SR)/SR+start
        db=np.zeros(len(t))
        for a,b in voices: db=np.minimum(db,dip(t,a,b,-10))
        if name=='goal-var':
            db=np.minimum(db,dip(t,59.35,60.2,-20)) # Flag interruption.
            db=np.minimum(db,dip(t,69.2,70.15,-12)) # GOAL verdict/stamp.
        music*=10**(db[:,None]/20)
        combined=foreground+music
        assert np.isfinite(combined).all() and np.max(np.abs(combined))<1, 'Mix clips'
        assert np.max(np.abs((combined-music)-foreground))<1e-6
        wav(folder/'music-ducked.wav',music);wav(folder/'with-music.wav',combined)
        wav(folder/'original.wav',foreground)
        (folder/'ducking.json').write_text(json.dumps(dict(film_start=start,duration=duration,
            dialogue_intervals=voices,depth_db=-10,attack_seconds=.12,release_seconds=.35),indent=2))
        for version in ('with-music','original'):
            target=folder/f'{version}.mp4'
            run([FF,'-v','error','-y','-ss',str(start),'-i',DELIVERY/'picture-selected.mp4',
                 '-i',folder/f'{version}.wav','-t',str(duration),'-map','0:v:0','-map','1:a:0',
                 '-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',
                 '-c:a','aac','-b:a','320k','-movflags','+faststart',target])
            run([FF,'-v','error','-xerror','-i',target,'-f','null','-'])
            stats=run([FF,'-hide_banner','-i',target,'-af','loudnorm=print_format=json','-f','null','-']).stderr
            levels=json.JSONDecoder().raw_decode(stats[stats.rfind('{'):])[0];assert float(levels['input_tp'])<=-1
            results.append(dict(file=str(target.relative_to(OUT)),sha256=sha(target),
                format=probe(target),levels=levels,decoded=True))
    (OUT/'checks.json').write_text(json.dumps(dict(outputs=results,
        foreground='unchanged sample values before additive music mix',
        agent_listening=False,user_listening='pending',on_screen_credits=False),indent=2))
    (OUT/'review.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Samtoons · Music audition</title>
<style>body{max-width:1050px;margin:32px auto;padding:0 20px;background:#151c23;color:#eaf1f5;font:17px/1.55 system-ui}video{width:100%;max-height:65vh;background:#000;border-radius:10px}button{font:inherit;padding:10px 15px;background:#294451;color:white;border:1px solid #7ea9bb;border-radius:6px;cursor:pointer;margin:4px}button[aria-pressed=true]{background:#276d61}a{color:#8cd4e8}audio{width:100%}small{color:#b8c7d2}</style>
<h1>A little rhythm. Clear voices.</h1><p>Music audition using the finished picture. Compare at the same device volume.</p>
<div><button data-scene="goal-var" aria-pressed="true">Goal → VAR · 29 seconds</button><button data-scene="fishing" aria-pressed="false">VAR Room → fishing · 19 seconds</button></div>
<video controls playsinline preload="metadata" src="goal-var/with-music.mp4"></video>
<div><button data-version="with-music" aria-pressed="true">With music</button><button data-version="original" aria-pressed="false">Original · no music</button></div>
<p id="status" role="status">Ready</p><p>Listen for the rhythm through the action, the quieter music beneath “Enzo was sleeping,” and Foden’s final line. Does the music add energy while every word remains clear?</p>
<details><summary>Hear only the added music</summary><audio controls src="goal-var/music-ducked.wav"></audio><p>The dips are intentional spaces for speech and effects.</p></details>
<p><a href="CREDITS.txt" download>Separate music credits</a> · <a href="checks.json">Technical checks</a></p>
<small>Both tracks are free under CC BY 4.0 with attribution. No credits are added to the video picture. This audition awaits your listening review.</small>
<script>const v=document.querySelector('video'),a=document.querySelector('audio'),s=document.querySelector('#status');let scene='goal-var',version='with-music',request=0;
async function select(keep){const id=++request,time=keep?v.currentTime:0,playing=!v.paused;v.pause();a.pause();s.textContent='Loading…';try{const r=await fetch(scene+'/'+version+'.mp4');if(!r.ok)throw Error('Unavailable');const blob=await r.blob();if(id!==request)return;const old=v.src;v.src=URL.createObjectURL(blob);if(old.startsWith('blob:'))URL.revokeObjectURL(old);v.onloadedmetadata=()=>{v.currentTime=Math.min(time,v.duration);s.textContent=version==='with-music'?'With music':'Original · no music';if(playing)v.play()};a.src=scene+'/music-ducked.wav'}catch(e){s.textContent='Could not load excerpt. Reload the page.'}}
document.querySelectorAll('[data-scene]').forEach(b=>b.onclick=()=>{scene=b.dataset.scene;document.querySelectorAll('[data-scene]').forEach(x=>x.setAttribute('aria-pressed',x===b));select(false)});
document.querySelectorAll('[data-version]').forEach(b=>b.onclick=()=>{version=b.dataset.version;document.querySelectorAll('[data-version]').forEach(x=>x.setAttribute('aria-pressed',x===b));select(true)});
v.onplay=()=>a.pause();a.onplay=()=>v.pause();select(false);</script></html>''')
    (OUT/'README.md').write_text('''# Music audition v001

The approved picture and foreground mix are preserved. Two excerpts only: film seconds 53–82 and 138–157. Funkorama supplies the rhythmic action bed; Scheming Weasel supplies the VAR/fishing motif. These selections are candidates based on the composer’s instrumentation and descriptions; agent listening is unavailable, and user listening is pending.

Sources and CC BY 4.0 attribution evidence: ../../assets/music-v001/. Exact credits are in CREDITS.txt, outside the picture as requested. The user handles publication attribution later. No publishing performed.

Music is constant-gain normalized to -23 LUFS, placed at -3 dB, and reduced another 10 dB during authored speech intervals, with 120 ms lead and 350 ms release. Additional flag/verdict dips protect those moments. Foreground sample values are unchanged before additive mixing. No global normalization or time stretching is applied. The full film will be scored after this sound checkpoint.

Reproduce with the installed runtime Python and scripts/build_music_audition.py after choosing a fresh output revision. The script checks lengths, finite samples, foreground preservation, clipping, full MP4 decode and encoded true peak. Numerical checks do not certify emotional fit or intelligibility.
''')
    print('Music excerpts ready:',OUT,flush=True)


if __name__=='__main__':
    main()

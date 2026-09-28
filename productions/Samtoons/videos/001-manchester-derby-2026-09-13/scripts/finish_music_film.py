"""Extend approved music cues; stream-copy the accepted 1080p picture."""
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
from build_music_audition import ROOT, REPO, DELIVERY, SR, FF, build, run, decode, wav, dip, sha
from pipeline.checkpoints import require_checkpoint

AUDITION = ROOT/'artifacts/music-v001'
OUT = ROOT/'artifacts/delivery-v002'


def main():
    approvals = [require_checkpoint(ROOT,'music-v001','sound')]
    approvals += [require_checkpoint(ROOT,'animatic-v004',s) for s in ('staging','sound','animatic')]
    OUT.mkdir(exist_ok=False)
    assets=json.loads((AUDITION/'goal-var/plan.json').read_text())['assets']
    for key,folder in [('approved-var','goal-var'),('approved-ending','fishing')]:
        p=AUDITION/folder/'music-ducked.wav'
        assets[key]=dict(path=str(p),sha256=sha(p),source='User-approved music-v001 audition',
            license='CC BY 4.0',attribution=(AUDITION/'CREDITS.txt').read_text(),
            notes='Preserve the exact approved music samples, including ducking and fades.')
    placements=[
        ('weasel',0,8,44,'Opening name-confusion joke'),
        ('funk',8,13.8,0,'Foden/Bruno action and card'),
        ('weasel',22,9.8,10,'Fishing promise and smug reaction'),
        ('funk',32,11,0,'Rashford and Mainoo chances'),
        ('weasel',44,6.6,44,'Goalpost contract joke'),
        ('approved-var',53,29,0,'Exact approved goal/VAR excerpt'),
        ('funk',82,15.8,0,'Save, post and header'),
        ('weasel',98,11.8,10,'Final chance expectation and parry'),
        ('funk',110,16.8,0,'Good wolf and coach celebration'),
        ('approved-ending',138,19,0,'Exact approved VAR Room/fishing ending'),
    ]
    cues=[]
    for i,(key,start,length,source,intent) in enumerate(placements):
        approved=key.startswith('approved')
        cues.append(dict(id=f'music-{i:02}',shot='film',event='start',asset=key,stem='music',
            intent=intent,offset_frames=str(start*24),in_seconds=source,
            duration_seconds=str(length),gain_db=0 if approved else -3,
            fade_in_seconds=0 if approved else .15,fade_out_seconds=0 if approved else .6))
    plan=dict(version=1,title='Approved music extended across the film',
        timeline=dict(fps=24,start_frame=1,frames=3768,sample_rate=SR),
        shots=[dict(id='film',start_frame=1,events=dict(start=0))],assets=assets,cues=cues)
    (OUT/'music-plan.json').write_text(json.dumps(plan,indent=2))
    build(OUT/'music-plan.json',OUT/'audio')
    music=decode(OUT/'audio/stems/music.wav',0,157)
    foreground=decode(DELIVERY/'mix-review.wav',0,157)
    assert music.shape==foreground.shape==(157*SR,2)
    t=np.arange(len(music))/SR
    db=np.zeros(len(t))
    voices=json.loads((AUDITION/'goal-var/ducking.json').read_text())['dialogue_intervals']
    for a,b in voices: db=np.minimum(db,dip(t,a,b,-10))
    # Protect the impact, realization and deadpan beats using the authored film time.
    quiet=[(11.05,11.5,-8),(14.15,15.8,-24),(19.35,19.7,-9),
           (34.2,35.7,-30),(43.0,44,-24),(51,52.65,-30),
           (83.65,84.35,-18),(92.35,94.3,-26),(99.65,102.0,-20),
           (105.65,106.25,-18),(119.2,120.15,-20)]
    for a,b,depth in quiet: db=np.minimum(db,dip(t,a,b,depth))
    for a,b in [(53,82),(138,157)]: db[round(a*SR):round(b*SR)]=0
    music *= 10**(db[:,None]/20)
    for folder,a,b in [('goal-var',53,82),('fishing',138,157)]:
        accepted=decode(AUDITION/folder/'music-ducked.wav',0,b-a)
        assert np.array_equal(music[a*SR:b*SR],accepted), 'Approved excerpt changed'
    combined=foreground+music
    assert np.isfinite(combined).all() and np.max(np.abs(combined))<1
    assert np.max(np.abs((combined-music)-foreground))<1e-6
    assert np.count_nonzero(music[127*SR:138*SR])==0, 'Apology must remain unscored'
    wav(OUT/'music-ducked.wav',music);wav(OUT/'mix-review.wav',combined)
    (OUT/'ducking.json').write_text(json.dumps(dict(dialogue_intervals=voices,
        speech_depth_db=-10,lead_seconds=.12,release_seconds=.35,
        additional_dips=quiet,unchanged_approved_intervals=[[53,82],[138,157]],
        intentional_unscored_intervals=[[127,138]]),indent=2))
    target=OUT/'samtoons-with-music-1080p.mp4'
    run([FF,'-v','error','-y','-i',DELIVERY/'picture-selected.mp4','-i',OUT/'mix-review.wav',
         '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','320k',
         '-t','157','-movflags','+faststart',target])
    run([FF,'-v','error','-xerror','-i',target,'-f','null','-'])
    levels=run([FF,'-hide_banner','-i',target,'-af','loudnorm=print_format=json','-f','null','-']).stderr
    levels=json.JSONDecoder().raw_decode(levels[levels.rfind('{'):])[0]
    assert float(levels['input_tp'])<=-1
    metadata=json.loads(run(['/opt/homebrew/bin/ffprobe','-v','error','-show_streams','-show_format','-of','json',target]).stdout)
    video=next(s for s in metadata['streams'] if s['codec_type']=='video')
    assert (video['width'],video['height'],video['r_frame_rate'],int(video['nb_frames']))==(1920,1080,'24/1',3768)
    assert abs(float(metadata['format']['duration'])-157)<.05
    packet_hash=[]
    for p in [DELIVERY/'picture-selected.mp4',target]:
        packet_hash.append(run([FF,'-v','error','-i',p,'-map','0:v:0','-c','copy','-f','hash','-hash','sha256','-']).stdout.strip())
    assert packet_hash[0]==packet_hash[1], 'Picture stream changed'
    for name in ('CREDITS.txt',):shutil.copy2(AUDITION/name,OUT/name)
    shutil.copy2(DELIVERY/'edit.json',OUT/'edit.json')
    (OUT/'delivery-checks.json').write_text(json.dumps(dict(approval_events=approvals,
        frames=3768,seconds=157,resolution=[1920,1080],fps=24,full_decode=True,
        picture_stream_hash=packet_hash[0],picture_stream_unchanged=True,
        approved_excerpts_sample_identical=True,foreground_preserved=True,
        encoded_levels=levels,sha256=sha(target),no_on_screen_credits=True,
        agent_listening=False,full_mix_user_review='pending'),indent=2))
    page=(DELIVERY/'review.html').read_text()
    page=page.replace('samtoons-final-1080p.mp4','samtoons-with-music-1080p.mp4')
    page=page.replace('<source src="samtoons-final-1080p.webm?cut=20260916final1" type="video/webm">','')
    page=page.replace('frame-15-120.png','../delivery-v001/frame-15-120.png')
    page=page.replace('Final film · 1080p','Film with music · 1080p')
    page=page.replace('Same approved edit and sound, rendered from the native Blender scenes.',
        'Approved music direction applied across the film. Original picture, voices and effects preserved.')
    page=page.replace('Review the action at normal speed; use frame steps to inspect joins or contact.',
        'Listen at normal speed. Music lowers beneath speech and pauses for the apology.')
    page=page.replace('samtoons-final.blend','samtoons-with-music.blend')
    page=page.replace('The complete animatic is approved. This is the final encoded movie for delivery review.',
        'The excerpt music treatment is approved. This complete mix is ready for your playback review. <a href="CREDITS.txt" download>Separate music credits</a>.')
    (OUT/'review.html').write_text(page)
    (OUT/'README.md').write_text('''# Full-film music revision

157 seconds, 1080p, 24 fps. The approved picture stream is copied exactly. The approved foreground mix is retained at unity, with the new music added. Music-v001 excerpts at 53–82 and 138–157 seconds remain sample-identical before AAC encoding. Speech ducking uses the approved 10 dB reduction with 120 ms lead and 350 ms release. The apology remains unscored.

Music motifs reuse the selected opening of Funkorama and passages of Scheming Weasel (faster version), by Kevin MacLeod, under CC BY 4.0. Attribution is in CREDITS.txt only, as requested; the user will handle publication credits. No upload performed.

Authoritative mix: mix-review.wav. Isolated added music: music-ducked.wav. Editable cue placement: music-plan.json; gain envelopes: ducking.json; reproducible builder: ../../scripts/finish_music_film.py. Original foreground stems/plan remain in delivery-v001 and its linked earlier production assets. The editable Blender copy uses this new packed mix and the same artwork/timeline.

Technical checks are in delivery-checks.json. The agent cannot hear playback; full-film listening remains for the user. The original delivery is preserved.
''')
    print('Full-film music export ready',target,flush=True)


if __name__=='__main__':main()

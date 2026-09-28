"""Reuse selected football audio; add one cached, original cartoon snore."""
from pathlib import Path
import json,hashlib,wave
import numpy as np
ROOT=Path(__file__).resolve().parents[1];SR=48000
plan=json.loads((ROOT/'production.json').read_text())
assets=json.loads((ROOT/'artifacts/film-v001/production.json').read_text())['assets']
path=ROOT/'assets/audio-v001/snore.wav'
if not path.exists():
    rng=np.random.default_rng(2019);t=np.arange(round(1.1*SR))/SR
    air=np.convolve(rng.normal(size=len(t)),np.ones(25)/25,mode='same')
    phase=2*np.pi*(68*t+9*np.sin(t*4)/4)
    breath=np.sin(np.pi*t/1.1)**2
    x=(.55*air*(.6+.4*np.sin(2*np.pi*23*t))+.12*np.sin(phase)+.055*np.sin(phase*3))*breath
    x=x/max(abs(x))*.65;pcm=np.column_stack((x,x))
    with wave.open(str(path),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(np.round(pcm*32767).astype('<i2').tobytes())
assets['snore']={'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source':'Original deterministic NumPy breath and nasal partial synthesis, scripts/sound_advanced.py; seed 2019; 48 kHz stereo.','license':'Original generated production audio, available for this production and revisions.','attribution':'','notes':'Fictional nonverbal cartoon snore; no match recording.'}
plan['assets']=assets;plan['cues']=[]
def cue(id,shot,event,asset,stem,duration,gain=-12,offset=0,pan=0,onset=0,fade=.02):
    plan['cues'].append({'id':id,'shot':shot,'event':event,'intent':id.replace('-',' '),'asset':asset,'stem':stem,'in_seconds':0,'duration_seconds':duration,'onset_seconds':onset,'offset_frames':offset,'gain_db':gain,'pan':pan,'fade_in_seconds':.004,'fade_out_seconds':fade})
cue('stadium-opening','opening','start','stadium','atmosphere',2,-16,fade=.12)
cue('flag-cloth','opening','start','net','foley',.48,-30,offset=8)
cue('stop-time','gags','head_sleep','freeze','editorial',.22,-15)
cue('fantasy-hush','gags','head_sleep','hush','atmosphere',4,-29,fade=.2)
cue('shoulder-snore','gags','head_sleep','snore','editorial',1.1,-9,offset=3)
cue('knee-snore','gags','knee_sleep','snore','editorial',1.1,-14,offset=4,pan=-.15)
cue('knee-settle','gags','knee_sleep','release','editorial',.36,-26,offset=18)
cue('back-to-play','read','wide','release','editorial',.36,-23)
cue('stadium-geography','read','wide','stadium','atmosphere',6,-19,fade=.2)
cue('walk-pulse','read','walk','tension','music',7,-23,fade=.4)
for i,offset in enumerate((0,40)):
    cue('walk-step-'+str(i),'read','walk','turf','foley',.16,-18,offset=offset,pan=.2)
cue('opportunity','read','notice','notice','music',2.1,-14)
cue('notice-hush','read','notice','hush','atmosphere',3,-28,fade=.2)
cue('pivot-plant','play','pivot','turf','foley',.16,-17,offset=22)
cue('action-stadium','play','pivot','stadium','atmosphere',3.75,-20,fade=.1)
for shot,gain in [('play',0),('replay',-5)]:
    for event,asset,duration,level,pan in [('corner_contact','corner',.32,-6,.05),('origi_contact','finish',.42,-3,-.1),('net_contact','net',.48,-10,-.3)]:
        cue(shot+'-'+asset,shot,event,asset,'foley',duration,level+gain,pan=pan,onset=.008)
cue('goal-roar','play','cheer','cheer','atmosphere',5.25,-8,fade=.4)
cue('goal-release','play','net_contact','resolve','music',5.375,-14,fade=.5)
cue('wake-up','celebrate','wake','notice','editorial',.4,-18,fade=.1)
cue('replay-hush','replay','start','hush','atmosphere',7,-24,fade=.4)
cue('replay-notice','replay','start','notice','music',2.1,-24)
cue('final-cheer','payoff','title','cheer','atmosphere',6.6,-14,fade=1.4)
cue('final-chord','payoff','title','resolve','music',6.6,-17,fade=1.4)
plan['mix_gain_db']=-3
plan['audio_direction']={'authority':'pipeline/audio.py premaster; two-pass FFmpeg loudnorm to -18 LUFS / -2 dBTP','original_sound':True,'quiet_intervals_seconds':[[2,6],[12,15],[24,31],[37.6,38]],'subjective_listening':'Not performed; playback listening remains unverified.'}
(ROOT/'production.json').write_text(json.dumps(plan,indent=2)+'\n')
print('SELECTED',len(assets),'assets;',len(plan['cues']),'cues')

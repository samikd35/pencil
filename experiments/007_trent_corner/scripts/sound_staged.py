"""Checkpoint alternatives: dry foreground vs recorded crowd; rejected noise beds stay out."""
from pathlib import Path
import hashlib,json,subprocess,copy
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/film-v003';AS=ROOT/'assets/audio-v002';FF='/opt/homebrew/bin/ffmpeg'
base=json.loads((ROOT/'production.json').read_text());old=json.loads((ROOT/'artifacts/film-v002/production.json').read_text())
rejected={key:old['assets'][key]['sha256'] for key in ('stadium','hush','cheer','tension','notice','resolve')}
assets={k:v for k,v in old['assets'].items() if k in ('turf','corner','finish','net','snore')}
for key,filename,duration,target in [('crowd-bed','goal-crowd',16,-30),('crowd-goal','crowd-cheer',6.3,-20)]:
    path=AS/(key+'.wav')
    if not path.exists():
        subprocess.run([FF,'-hide_banner','-loglevel','error','-i',str(AS/(filename+'.mp3')),'-t',str(duration),'-af',f'highpass=f=120,lowpass=f=7000,loudnorm=I={target}:TP=-3:LRA=8','-ar','48000','-ac','2','-c:a','pcm_s16le',str(path)],check=True)
    source='https://freesound.org/people/D.jones/sounds/528799/' if key=='crowd-bed' else 'https://freesound.org/people/Krizin/sounds/651646/'
    assets[key]={'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source':source+'; public HQ preview acquired 2026-09-12; original preview retained in assets/audio-v002.','license':'CC0 1.0, per individual sound page; page snapshot retained locally.','attribution':'D.jones / Freesound (voluntary credit)' if key=='crowd-bed' else 'Krizin / Freesound (voluntary credit)','notes':f'Candidate, not yet auditioned by the user. First {duration} seconds; highpass 120 Hz, lowpass 7 kHz; loudnorm {target} LUFS / -3 dBTP / LRA 8; 48 kHz stereo. Not archival Anfield audio.'}
base['script']='script-v004.md'
base['assets']=assets;base['cues']=[];base['mix_gain_db']=0
base['rejected_audio']=rejected
base['audio_direction']={'status':'Checkpoint candidates, awaiting actual listening','change':'Remove all synthetic continuous atmosphere and music beds; compare sparse foreground with recorded crowd.','comparison':'Identical foreground gain in both versions; crowd is the only changing layer.','source_provenance':'Recorded crowd is CC0 library material, not the 2019 match recording.'}
for c in old['cues']:
    if c['asset'] in ('turf','corner','finish','net','snore') and c['id']!='flag-cloth':base['cues'].append(c)
def cue(plan,id,shot,event,asset,duration,gain,offset=0,fade=.1):
    plan['cues'].append({'id':id,'shot':shot,'event':event,'intent':id.replace('-',' '),'asset':asset,'stem':'atmosphere','in_seconds':0,'duration_seconds':duration,'offset_frames':offset,'gain_db':gain,'pan':0,'fade_in_seconds':.04,'fade_out_seconds':fade})
# A deliberately sparse option: real human cheer only after the scored goal.
cue(base,'recorded-goal-reaction','play','cheer','crowd-goal',5.2,0,fade=.6)
cue(base,'recorded-final-reaction','payoff','title','crowd-goal',6.2,-5,fade=1.5)
for label in ('clean','crowd'):
    plan=copy.deepcopy(base);plan['candidate']=label
    if label=='crowd':
        cue(plan,'recorded-opening-space','opening','start','crowd-bed',2,-2,fade=.2)
        cue(plan,'recorded-waiting-crowd','read','wide','crowd-bed',12.6,-2,fade=.25)
        cue(plan,'recorded-replay-space','replay','start','crowd-bed',7,-7,fade=.3)
    assert not any(a['sha256'] in rejected.values() for a in plan['assets'].values())
    (ROOT/f'production-v003-{label}.json').write_text(json.dumps(plan,indent=2)+'\n')
(ROOT/'production.json').write_text((ROOT/'production-v003-clean.json').read_text())
(AS/'provenance.json').write_text(json.dumps({'sources':{k:v for k,v in assets.items() if k.startswith('crowd')},'rejected_prior_assets':rejected,'status':'Candidate assets acquired and prepared; subjective listening pending.'},indent=2)+'\n')
print('AUDIO_CANDIDATES_READY')

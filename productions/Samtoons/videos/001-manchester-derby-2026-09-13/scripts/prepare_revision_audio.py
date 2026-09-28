"""Resolve the requested door insert and new full-cast acting audition."""
from pathlib import Path
from fractions import Fraction
import json,hashlib,math
import numpy as np
import soundfile as sf
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/animatic-v003'

def main():
    plan=json.loads((ROOT/'artifacts/animatic-v002/plan.json').read_text())
    edit=json.loads((OUT/'edit.json').read_text())
    plan['title']='Ten Men. Two Posts. No Points. / VAR reveal and performance revision'
    plan['timeline']['frames']=sum(r['frames'] for r in edit)
    plan['shots'][-1]['start_frame']=edit[-1]['start_frame']
    plan['shots'][-1]['events']['dialogue_18']=203
    plan['shots'].insert(15,dict(id='S10-VAR-exit',start_frame=edit[15]['start_frame'],events=dict(start=0,door_open=26,step_1=64,step_2=87,step_3=110)))
    takes={x['id']:x for x in json.loads((ROOT/'assets/film-voices-v002/takes.json').read_text())}
    mouths=json.loads((ROOT/'artifacts/animatic-v001/mouth-timing.json').read_text());new=[]
    for row in mouths:
        slug=row['id']
        if slug not in takes:continue
        take=takes[slug];path=ROOT/take['path'];a,sr=sf.read(path);duration=Fraction(len(a),sr)
        plan['assets'][slug].update(path='../../'+take['path'],sha256=take['sha256'],notes=take['direction'],source='New local Qwen3-TTS VoiceDesign acted take; assets/film-voices-v002; listening review pending')
        cue=next(c for c in plan['cues'] if c['stem']=='dialogue' and c['asset']==slug)
        cue.update(duration_seconds=str(duration),intent=take['direction'])
        if slug=='biting':row.update(scene=edit[-1]['scene'],mouth='A Fishing Foden / mouth control',frame=204)
        if slug=='enzo':row['mouth']='A Reclining Maresca / mouth control'
        row.update(path=str(path),duration_seconds=float(duration),approved=False)
        rms=[float(np.sqrt(np.mean(a[round(f*sr/24):round((f+1)*sr/24)]**2))) for f in range(math.ceil(len(a)*24/sr))]
        peak=max(rms);assert peak>0
        intensity=1.8 if slug in ('and-him','him','yes','enzo') else 1.05
        row['jaw_keys']=[(row['frame']-1,.025)]+[(row['frame']+f,.025 if e<peak*.09 else intensity*min(1,(e/peak)**.6)) for f,e in enumerate(rms)]+[(row['frame']+len(rms),.025)]
        frames=next(x['frames'] for x in edit if x['scene']==row['scene'])
        assert row['frame']+len(rms)<=frames,(slug,row['frame'],len(rms),frames)
        new.append(row)
    # Three restrained boot contacts and a short door-latch accent: original synthesis.
    assets=ROOT/'assets/door-v003';assets.mkdir(exist_ok=True)
    rng=np.random.default_rng(317);sr=48000;t=np.arange(int(.17*sr))/sr
    noise=rng.normal(0,1,len(t));noise=np.convolve(noise,np.ones(13)/13,mode='same')
    foot=(.25*np.sin(2*np.pi*(90*t-100*t*t))+.13*noise)*np.exp(-t*32)*np.minimum(1,t/.004)
    sf.write(assets/'boot-step.wav',foot,sr,subtype='PCM_24')
    for aid,file in [('boot-step','boot-step.wav')]:
        path=assets/file;plan['assets'][aid]=dict(path='../../'+str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),source='Original seeded short boot contact synthesis in prepare_revision_audio.py',license='Original production synthesis',attribution='')
    for event,asset,gain,dur in [('door_open','dry-impact',-13,'.18'),('step_1','boot-step',-4,'.17'),('step_2','boot-step',-5,'.17'),('step_3','boot-step',-4,'.17')]:
        plan['cues'].append(dict(id='var-exit-'+event,shot='S10-VAR-exit',event=event,asset=asset,stem='foley',intent=event.replace('_',' '),duration_seconds=dur,gain_db=gain))
    assert len(new)==15 and len(edit)==17 and plan['timeline']['frames']==3768
    (OUT/'mouth-timing.json').write_text(json.dumps(new,indent=2)+'\n')
    (OUT/'plan.json').write_text(json.dumps(plan,indent=2)+'\n')
    print('READY: 157 seconds; fifteen revised performances; prior Bruno shout, apology and Carrick takes retained.')
if __name__=='__main__':main()

"""Retain selected performances; resolve changed events against the repaired edit."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/animatic-v002'

def main():
    plan=json.loads((ROOT/'artifacts/animatic-v001/plan.json').read_text())
    edit=json.loads((OUT/'edit.json').read_text());events=json.loads((OUT/'native-events.json').read_text())
    plan['title']='Ten Men. Two Posts. No Points. / repaired complete animatic'
    plan['timeline']['frames']=sum(r['frames'] for r in edit)
    for shot,row in zip(plan['shots'],edit):
        shot['start_frame']=row['start_frame']
        shot['events'].update({k:v-1 for k,v in events[row['scene']].items()})
    repair=json.loads((ROOT/'artifacts/repair-v001/audio-plan.json').read_text());plan['assets'].update(repair['assets'])
    plan['cues']=[c for c in plan['cues'] if c['shot']!='S03-04']
    plan['shots'][3]['events']=repair['shots'][0]['events']
    for cue in repair['cues']:plan['cues'].append(dict(cue,id='repair-'+cue['id'],shot='S03-04'))
    # A metal post has an impact sound. Keep the chime for its facial joke.
    for cue in plan['cues']:
        if cue['event']=='post_hit':cue.update(asset='post-clang',duration_seconds='.85',gain_db=-3)
    plan['shots'][-1]['events']['dialogue_18']=229
    path=ROOT/'assets/audio-v002/comic-fountain.wav'
    plan['assets']['roof-water']=dict(path='../../assets/audio-v002/comic-fountain.wav',sha256=hashlib.sha256(path.read_bytes()).hexdigest(),source='Original comic water synthesis, preserved assets/audio-v002',license='Original production synthesis',attribution='',notes='New roof placement is an animatic audition; no listening acceptance claimed.')
    plan['cues'].append(dict(id='roof-water',shot='S10-16',event='cascade',asset='roof-water',stem='foley',intent='Roof spill splashing into the exaggerated pitch puddle',duration_seconds='2.5',gain_db=-17,fade_in_seconds='.12',fade_out_seconds='.3'))
    assert plan['timeline']['frames']==3624
    assert sum(c['stem']=='dialogue' for c in plan['cues'])==19
    # Dialogue retains exactly the selected source files and gains.
    old=json.loads((ROOT/'artifacts/animatic-v001/plan.json').read_text())
    assert [(c['asset'],c['gain_db']) for c in old['cues'] if c['stem']=='dialogue']==[(c['asset'],c['gain_db']) for c in plan['cues'] if c['stem']=='dialogue']
    (OUT/'plan.json').write_text(json.dumps(plan,indent=2)+'\n')
    print('Prepared',plan['timeline']['frames'],'frames;',len(plan['cues']),'cues; original 19 performances retained')
if __name__=='__main__':main()

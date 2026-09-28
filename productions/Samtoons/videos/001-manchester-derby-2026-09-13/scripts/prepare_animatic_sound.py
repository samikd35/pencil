"""Bind cached speaking takes and selected B effects to the full native edit."""
from pathlib import Path
from fractions import Fraction
import json,hashlib,wave,math
import numpy as np
import soundfile as sf
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/animatic-v001'
def main():
 edit=json.loads((OUT/'edit.json').read_text());speech=json.loads((OUT/'speech.json').read_text());native=json.loads((OUT/'native-events.json').read_text())
 source=json.loads((ROOT/'artifacts/voices-v002/plan-directed.json').read_text());initial=json.loads((ROOT/'production.json').read_text())
 plan=dict(version=1,title='Ten Men. Two Posts. No Points. / complete animatic',timeline=dict(fps='24',start_frame=1,frames=3600,sample_rate=48000),shots=[],assets=source['assets'],cues=[],mix_gain_db=0)
 # These plans live at the same directory depth, retaining relative asset paths.
 for aid in ('servo','badge'):
  asset=dict(initial['assets'][aid]);asset['path']='../../'+asset['path'];plan['assets'][aid]=asset
 shots={}
 for i,row in enumerate(edit):
  sid=f"{row['beat']}-{i+1:02}";shot=dict(id=sid,start_frame=row['start_frame'],events={k:v-1 for k,v in native[row['scene']].items()});shot['events']['start']=0;shots[row['scene']]=shot;plan['shots'].append(shot)
 exact={'S02':'S02 / kick and overreaction','S08':'S08 / hope and parry','S10':'S10 / tears and umbrella'}
 for c in source['cues']:
  if c['stem']=='dialogue':continue
  cue=dict(c);cue['shot']=shots[exact[c['shot']]]['id'];plan['cues'].append(cue)
 takes={t['id']:t for t in json.loads((ROOT/'assets/film-voices-v001/takes.json').read_text())};mouths=[]
 for i,row in enumerate(speech):
  slug=row['id'];approved=slug.endswith('-approved');aid=slug
  if approved:
   aid=slug.replace('-approved','-directed');asset=plan['assets'][aid];path=(OUT/asset['path']).resolve();words=row['text'];direction=asset['notes']
  else:
   take=takes[slug];path=ROOT/take['path'];words=take['text'];direction=take['direction']
   plan['assets'][aid]=dict(path='../../'+take['path'],sha256=take['sha256'],source='Local Qwen3-TTS VoiceDesign bf16; cached raw take and direction in assets/film-voices-v001',license='Apache-2.0 model; original fictional performance',attribution='Qwen Team / https://github.com/QwenLM/Qwen3-TTS',notes=direction)
  a,sr=sf.read(path);a=np.asarray(a);duration=Fraction(len(a),sr);shot=shots[row['scene']];event='dialogue_'+str(i);shot['events'][event]=row['frame']-1
  plan['cues'].append(dict(id=event,shot=shot['id'],event=event,asset=aid,stem='dialogue',intent=direction,duration_seconds=str(duration),gain_db=0,pan=0))
  row.update(text=words,path=str(path),duration_seconds=float(duration),approved=approved)
  # Energy envelopes locate syllabic effort and genuine silence. These are jaw
  # timing guides, not a claim of phoneme recognition or perfect lip synchronization.
  rms=[]
  for f in range(math.ceil(len(a)*24/sr)):
   chunk=a[round(f*sr/24):round((f+1)*sr/24)];rms.append(float(np.sqrt(np.mean(chunk*chunk))) if len(chunk) else 0)
  peak=max(rms);assert peak>0
  intensity=1.8 if slug in ('bruno-approved','and-him','him','yes','enzo') else .95
  values=[(row['frame']-1,.025)]
  for f,energy in enumerate(rms):values.append((row['frame']+f,.025 if energy<peak*.09 else intensity*min(1,(energy/peak)**.6)))
  values.append((row['frame']+len(rms),.025));row['jaw_keys']=values;mouths.append(row)
 def cue(scene,event,asset,gain=-4,duration=None,stem='foley'):
  path=(OUT/plan['assets'][asset]['path']).resolve();info=sf.info(path);seconds=min(Fraction(info.frames,info.samplerate),Fraction(str(duration))) if duration else Fraction(info.frames,info.samplerate)
  plan['cues'].append(dict(id=scene+'-'+event,shot=shots[scene]['id'],event=event,asset=asset,stem=stem,intent=event.replace('_',' ')+' comic action accent',duration_seconds=str(seconds),gain_db=gain,pan=0))
 opening='FILM S01 / Morning Pep';shots[opening]['events']['head_turn']=46;cue(opening,'head_turn','servo',-3,.34);cue(opening,'badge_reveal','badge',-4,.22)
 for scene,events in native.items():
  if not scene.startswith('FILM '):continue
  for ev in events:
   asset={'strike':'ball-strike','post_hit':'innocent-chime','header':'ball-strike','wide':'comic-recoil','tip':'glove-parry','finish':'ball-strike','cross':'ball-strike','flag':'card-flick','onside':'card-flick','no_touch':'card-flick','goal_given':'dry-impact','reboot':'servo','stamp':'dry-impact'}.get(ev)
   if asset:cue(scene,ev,asset,-5)
 # Previously prepared original payoff effects remain new candidates here.
 for aid,fn in [('float','float-plop.wav'),('tail','whistle-squeak.wav')]:
  path=ROOT/'assets/audio-v002'/fn;plan['assets'][aid]=dict(path='../../'+str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),source='Original comic effect, prepare_action_audio / preserved audio-v002',license='Original production synthesis',attribution='')
 cue('FILM S10 / They are biting','float_plop','float',-10);cue('FILM S10 / They are biting','whistle_tail','tail',-10)
 (OUT/'mouth-timing.json').write_text(json.dumps(mouths,indent=2)+'\n');(OUT/'plan.json').write_text(json.dumps(plan,indent=2)+'\n')
 assert len(edit)==16 and sum(r['frames'] for r in edit)==3600
 assert sum(c['stem']=='dialogue' for c in plan['cues'])==19
 print('READY',len(plan['cues']),'cues',len(mouths),'speaking performances')
if __name__=='__main__':main()

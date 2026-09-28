"""Prepare cached S01 sound candidates and the film's selected timing; no final voice claim."""
import hashlib, json, math, shutil, struct, subprocess, sys, wave
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parents[3]
sys.path.insert(0,str(WORK/'experiments/001_heavy_box'))
from journal import append_event
A=ROOT/'assets/audio-v001'; OUT=ROOT/'artifacts/staging-v001'
first_run=not (ROOT/'production.json').exists()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run(*args): subprocess.run(args,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
def tone(path,duration,formula):
    if path.exists():return
    with wave.open(str(path),'wb') as w:
        w.setparams((1,2,48000,0,'NONE','not compressed'))
        w.writeframes(b''.join(struct.pack('<h',round(32767*max(-.95,min(.95,formula(i/48000))))) for i in range(round(duration*48000))))
# Intentionally synthetic servo and graphic prop accent, never synthesized stadium noise.
tone(A/'head-servo.wav',.34,lambda t:.13*math.sin(2*math.pi*(390*t+730*t*t))*math.sin(math.pi*t/.34)**2+.028*math.sin(2*math.pi*1170*t)*math.sin(math.pi*t/.34)**2)
tone(A/'badge-pop.wav',.22,lambda t:.28*math.sin(2*math.pi*(170*t+45*(1-math.exp(-t*40))))*math.exp(-t*24)*min(1,t/.004))
voice=A/'morning-pep-temp.wav'
if not voice.exists():
    run('say','-v','Fred','-r','155','-o',str(A/'morning-pep-temp.aiff'),'Morning, Pep.')
    run('ffmpeg','-y','-i',str(A/'morning-pep-temp.aiff'),'-af','loudnorm=I=-21:TP=-4:LRA=7','-ar','48000','-ac','1',str(voice))
source=WORK/'experiments/007_trent_corner/assets/audio-v002'
for name in ('crowd-bed.wav','provenance.json','goal-crowd-page.html'):
    target=A/('prior-'+name if name!='crowd-bed.wav' else name)
    if not target.exists(): shutil.copy2(source/name,target)
assets={}
for name,file,desc,license in [
 ('servo','head-servo.wav','Original analytic oscillator; see prepare_staging.py. Graphic robot motion, not recorded machinery.','Original production synthesis'),
 ('badge','badge-pop.wav','Original analytic oscillator; graphic pop on ENZO badge reveal.','Original production synthesis'),
 ('temp-haaland','morning-pep-temp.wav','macOS say Fred, rate 155. Original parody text. Timing placeholder; not Haaland voice imitation.','TEMPORARY REVIEW ONLY; final performance and commercial clearance unresolved'),
 ('crowd','crowd-bed.wav','D.jones / Freesound 528799; local prior source snapshot and processing provenance retained. Generic football crowd, not Old Trafford recording.','CC0 1.0 per retained individual source-page/provenance record')]:
    assets[name]={'path':'assets/audio-v001/'+file,'sha256':sha(A/file),'source':desc,'license':license,'attribution':'D.jones / Freesound (voluntary)' if name=='crowd' else ''}
durations=[8,24,12,12,29,7,9,17,12,20];shots=[];start=1
for i,duration in enumerate(durations,1):
    shots.append({'id':f'S{i:02}','start_frame':start,'events':{'start':0}});start+=duration*24
shots[0]['events'].update({'head_turn':46,'greeting':58,'badge_reveal':113,'deadpan_hold':124})
voice_duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(voice)]))
base=[{'id':'S01-servo','shot':'S01','event':'head_turn','asset':'servo','stem':'foley','intent':'Head scans the manager with a comic servo','duration_seconds':.34,'gain_db':-3,'pan':-.2},
{'id':'S01-greeting-TEMP','shot':'S01','event':'greeting','asset':'temp-haaland','stem':'dialogue-temp','intent':'Temporary greeting timing; final performance unresolved','duration_seconds':voice_duration,'gain_db':0,'pan':-.15},
{'id':'S01-badge','shot':'S01','event':'badge_reveal','asset':'badge','stem':'foley','intent':'Emphasize the ENZO badge reveal','duration_seconds':.22,'gain_db':-4,'pan':.25}]
plan={'version':1,'title':'Ten Men. Two Posts. No Points.','status':'staging and sound candidates; not full-film audio','storyline':'storyline-v001.md','timeline':{'fps':'24','start_frame':1,'frames':3600,'sample_rate':48000},'shots':shots,'assets':assets,'cues':base,'mix_gain_db':-1,'picture':{'width':1920,'height':1080,'seconds':150,'construction':'Native flat Blender meshes and curves with original illustrated facial replacements; limited-view staging only'},'sound_direction':{'voice':'Temporary synthetic robot timing only; final cast performances pending','A':'Recorded crowd, ducked for dialogue and badge silence','B':'Sparse foreground only, same dialogue and effects','listening':'Not yet heard or accepted','music':'No continuous music selected; later heroic/VAR stings remain to audition'}}
(ROOT/'production.json').write_text(json.dumps(plan,indent=2)+'\n')
for variant in ('A','B'):
    trial=json.loads(json.dumps(plan));trial['timeline']['frames']=192;trial['shots']=shots[:1]
    for asset in trial['assets'].values():asset['path']='../../'+asset['path']
    if variant=='A':
        for n,event,offset,dur,gain,fadein,fadeout in [('open','start',0,2.3,-2,.12,.3),('under-voice','start',55,2.4,-10,.08,.25),('tail','start',149,1.75,-4,.25,.2)]:
            trial['cues'].append({'id':'S01-crowd-'+n,'shot':'S01','event':event,'offset_frames':offset,'asset':'crowd','stem':'ambience','intent':'Establish football crowd, reduced for the gag','in_seconds':3,'duration_seconds':dur,'gain_db':gain,'fade_in_seconds':fadein,'fade_out_seconds':fadeout})
    (OUT/f'audio-plan-{variant}.json').write_text(json.dumps(trial,indent=2)+'\n')
assert start==3601 and sum(durations)==150 and voice_duration<2.2
if first_run: append_event(ROOT,stage='story-selection',status='selected',reviewer='user',intent='Begin the actual film from the chosen storyline',method='Carry forward explicit script praise and subsequent production-skill invocation',result='User: “Yeah, I love the script”; then linked storyline-v001.md and invoked produce-pencil-animation. S01 staging and sound preparation authorized. No unseen or unheard creative artifact accepted.',decision='Produce selected 150-second storyline; no pilot.',inputs=['storyline-v001.md','brief.md'],outputs=['production.json'])
print(json.dumps({'voice_seconds':voice_duration,'shots':len(shots),'frames':start-1,'audio_candidates':['A','B']}))

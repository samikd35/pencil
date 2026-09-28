"""Selected existing Foley and one metallic post accent for the S03 repair."""
from pathlib import Path
import ast, hashlib, json, math, random, struct, wave
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/repair-v001'
source=ROOT/'scripts/prepare_staging.py'
scope={'wave':wave,'math':math,'random':random,'struct':struct}
tree=ast.parse(source.read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='tone'],type_ignores=[]),str(source),'exec'),scope)
asset=ROOT/'assets/rashford-v002/post-clang.wav'
if not asset.exists():
    scope['tone'](asset,.85,lambda t:min(1,t/.0015)*sum(a*math.sin(math.tau*f*t)*math.exp(-t*d) for f,a,d in [(420,.28,9),(713,.18,6),(1187,.12,12),(2093,.07,20)]))
old=json.loads((ROOT/'artifacts/animatic-v001/plan.json').read_text())
assets={k:old['assets'][k] for k in ('ball-strike','innocent-chime','comic-recoil','shirt-move')}
assets['post-clang']={'path':'../../assets/rashford-v002/post-clang.wav','sha256':hashlib.sha256(asset.read_bytes()).hexdigest(),'source':'Original synthesis in scripts/prepare_rashford_audio.py','license':'Original production synthesis','attribution':'','notes':'Metallic graphic impact for this staging audition; creative listening remains for review.'}
native=json.loads((OUT/'native-events.json').read_text())
events={k:native[n]-1 for k,n in {'strike':'strike','premature':'premature_celebration','post_hit':'post_hit','realisation':'realisation','scratch':'scratch','post_imitation':'post_imitation'}.items()}
cues=[]
for event,name,gain,onset in [('strike','ball-strike',-2,.03),('premature','innocent-chime',-10,0),('post_hit','post-clang',-2,0),('realisation','comic-recoil',-9,0),('scratch','shirt-move',-18,0),('post_imitation','innocent-chime',-8,0)]:
    with wave.open(str(OUT/assets[name]['path'])) as w:duration=w.getnframes()/w.getframerate()
    cues.append({'id':event,'shot':'S03','event':event,'asset':name,'stem':'foley' if name in ('ball-strike','shirt-move','post-clang') else 'comic-accents','intent':event.replace('_',' '),'duration_seconds':str(duration),'gain_db':gain,'onset_seconds':onset})
plan={'version':1,'title':'S03 repaired staging audition','timeline':{'fps':'24','start_frame':1,'frames':216,'sample_rate':48000},'shots':[{'id':'S03','start_frame':1,'events':events}],'assets':assets,'cues':cues,'mix_gain_db':0,'scope':'Nine-second staging excerpt. Quiet around reactions is deliberate. No spoken line; accepted voice takes unchanged.'}
assert events['strike']==39-1 and events['post_hit']==58-1
(OUT/'audio-plan.json').write_text(json.dumps(plan,indent=2)+'\n')

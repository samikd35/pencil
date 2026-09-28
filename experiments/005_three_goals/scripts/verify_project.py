"""Check saved contacts, shot visibility, correct score progression and embedded sound."""
from pathlib import Path
import bpy, json, math, hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/film-v001'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'three-goals.blend'));s=bpy.context.scene
build=json.loads((OUT/'build-checks.json').read_text())
assert (s.frame_start,s.frame_end,s.render.fps)==(1,720,24)
source=ROOT.parent/'001_heavy_box/artifacts/finish-v002/character-and-effects.blend'
assert hashlib.sha256(source.read_bytes()).hexdigest()==build['source_sha256']
def distance(pts,p):
    result=[]
    for a,b in zip(pts,pts[1:]+pts[:1]):
        dx,dy=b[0]-a[0],b[1]-a[1];u=min(1,max(0,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy)))
        result.append(math.hypot(p[0]-a[0]-u*dx,p[1]-a[1]-u*dy))
    return min(result)
contacts=[]
for t,name,scale in [(3,'Mbappe',.83),(7.5,'Mbappe',.82),(10.25,'Messi',.75),(15.25,'Mbappe',.83),(18.625,'Mbappe',.83),(21.25,'Montiel',.83)]:
    s.frame_set(round(t*24)+1);bpy.context.view_layer.update()
    boot=bpy.data.objects[name+' / Shoe_near'];pts=[(boot.matrix_world@v.co)[:2] for v in boot.data.vertices]
    center=bpy.data.objects['Continuous match ball'].location[:2]
    gap=distance(pts,center)-.16-.0205*scale
    assert abs(gap)<.002,(t,gap)
    assert not boot.hide_render and not bpy.data.objects['Ball'].hide_render
    contacts.append({'seconds':t,'player':name,'boot_surface_gap':gap})
# Validate every frame at the camera cuts as well as through interpolated motion.
scorechecks=[]
for t,score in [(0,'2 - 0'),(3.6,'2 - 1'),(8.2,'2 - 2'),(10.8,'3 - 2'),(16,'3 - 3'),(18.2,'0 - 0'),(19.3,'0 - 1'),(20.5,'3 - 2'),(22,'4 - 2')]:
    s.frame_set(round(t*24)+1)
    visible=[o.data.body for o in s.objects if o.name.startswith('Score ') and not o.hide_render]
    assert visible==[score],(t,visible,score);scorechecks.append({'seconds':t,'score':score})
for f in range(1,721):
    s.frame_set(f)
    heads=[o for o in s.objects if o.name.endswith(' / Head') and not o.hide_render]
    assert heads,(f,'No actor visible')
    if f>=round(27*24)+1:assert len(heads)==1 and heads[0].name=='Mbappe / Head'
    for name in ('Mbappe','Messi','Montiel','Thuram','Martinez','Lloris','Kolo Muani','Argentina teammate'):
        for side in ('far','near'):
            arm=bpy.data.objects[name+' / Arm_'+side]
            assert all(fc.driver.is_valid for fc in arm.data.animation_data.drivers)
audio=OUT/'audio/soundtrack.wav';assert audio.exists()
seq=s.sequence_editor_create()
if not seq.strips:strip=seq.strips.new_sound('Original music, Foley and designed breaths',str(audio),channel=1,frame_start=1)
else:strip=seq.strips[0]
strip.sound.pack();s.render.use_sequencer=False
s.frame_set(37);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'three-goals.blend'))
result={'frames':720,'seconds':30,'checked_frame_visibility':720,'contacts':contacts,'score_checks':scorechecks,'embedded_soundtrack':bool(strip.sound.packed_file),'new_shoulders':16,'source_unchanged':True,'limits':'Stylized reconstruction; geometric checks do not establish likeness, dramatic impact or audience comprehension.'}
assert result['embedded_soundtrack'];(OUT/'project-checks.json').write_text(json.dumps(result,indent=2)+'\n');print('PROJECT_CHECKS_PASSED',flush=True)

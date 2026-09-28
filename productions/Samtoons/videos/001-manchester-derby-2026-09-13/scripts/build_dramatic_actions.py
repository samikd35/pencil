"""Film-local action staging on the approved A joint/skin construction.
Run scene batches through the interactive Blender connector; preserve earlier reviews.
"""
from pathlib import Path
import bpy,runpy,json,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/staging-v005'
A={'__file__':str(ROOT/'scripts/build_option_a.py')};exec(compile(Path(A['__file__']).read_text(),A['__file__'],'exec'),A)
keys=A['keys'];poly=A['poly'];line=A['line'];empty=A['empty'];text=A['text'];rect=A['rect'];oval=A['oval']
CONFIG=json.loads((ROOT/'assets/option-a-v001/landmarks.json').read_text())
CONFIG.update(json.loads((ROOT/'assets/action-a-v001/landmarks.json').read_text()))
SCENES=[];CAST={}

def scene(name,frames,location=(2,-10,2.4),target=(0,0,1)):
    global s,col,cam
    s=bpy.data.scenes.new(name);bpy.context.window.scene=s;SCENES.append(s)
    col=bpy.data.collections.new(name+' / artwork');s.collection.children.link(col)
    source=bpy.data.scenes['S02 / Option A']
    for ob in source.objects:
        if ob.name.startswith('A /') and not ob.name.startswith(('A / referee','A / red card')):col.objects.link(ob)
    s.world=source.world;s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=16
    s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.render.fps_base=1;s.frame_start=1;s.frame_end=frames
    s.render.use_sequencer=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.view_settings.view_transform='Standard';s.view_settings.look='None'
    cd=bpy.data.cameras.new(name+' camera');cd.lens=44;cam=bpy.data.objects.new(cd.name,cd);col.objects.link(cam);cam.location=location;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();s.camera=cam
    A.update(s=s,col=col,cam=cam);A['base'].update(s=s,skin=col,ink=A['mat']('#202329'),font=next(f for f in bpy.data.fonts if f.filepath.endswith('Arial Bold.ttf')))
    for ar in bpy.context.screen.areas:
        if ar.type=='VIEW_3D':ar.spaces.active.region_3d.view_perspective='CAMERA';ar.spaces.active.shading.type='MATERIAL';ar.spaces.active.overlay.show_overlays=False
    s['Scope']='Action staging picture diagnostic; actual voices and sound await audition.'
    return s

def actor(tag,person,location):
    a=A['actor'](tag,CONFIG[person],location);reweight_upper(a);CAST[tag]=a;return a

def reweight_upper(a):
    # Blend the shoulder seam across the shirt's width, instead of a hard x cutoff.
    r=a['rest'];skin=a['skin'];bones={'torso':('hip','neck')}
    for side in ('L','R'):
        bones.update({side+' upper arm':(side+'shoulder',side+'elbow'),side+' forearm':(side+'elbow',side+'wrist'),side+' hand':(side+'wrist',side+'finger')})
    for v in skin.data.vertices:
        p=v.co
        if not r['hip'].y+.35<p.y<r['neck'].y-.2:continue
        side='L' if p.x<0 else 'R';candidates=['torso',side+' upper arm',side+' forearm',side+' hand']
        distances=[(max(0,A['segment_distance'](p,r[bones[k][0]],r[bones[k][1]])-(.35 if k=='torso' else 0)),k) for k in candidates]
        nearest=sorted(distances)[:2];weights=[math.exp(-dist*dist/.035) for dist,k in nearest];total=sum(weights)
        if total<1e-20:weights=[1,0];total=1
        for group in [g.group for g in v.groups]:skin.vertex_groups[group].remove([v.index])
        for (_,k),w in zip(nearest,weights):skin.vertex_groups[k].add([v.index],w/total,'REPLACE')
    for v in skin.data.vertices:
        p=v.co
        if not (r['hip'].y-.95<p.y<r['hip'].y+.15 and abs(p.x)<1.02):continue
        side='L' if p.x<0 else 'R'
        torso=max(0,A['segment_distance'](p,r['hip'],r['neck'])-.26)
        thigh=A['segment_distance'](p,r[side+'hip'],r[side+'knee'])
        weights=[math.exp(-torso*torso/.05),math.exp(-thigh*thigh/.05)];total=sum(weights)
        if total<1e-20:continue
        for group in [g.group for g in v.groups]:skin.vertex_groups[group].remove([v.index])
        for k,w in zip(('torso',side+' thigh'),weights):skin.vertex_groups[k].add([v.index],w/total,'REPLACE')

def camera_keys(shots):
    for f,loc,target in shots:
        cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
        cam.keyframe_insert(data_path='location',frame=f);cam.keyframe_insert(data_path='rotation_euler',frame=f)
    for layer in cam.animation_data.action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    for k in fc.keyframe_points:k.interpolation='CONSTANT'

def rotate(v,t):return Vector((math.cos(t)*v.x-math.sin(t)*v.y,math.sin(t)*v.x+math.cos(t)*v.y,v.z))

def pose(a,frame,angle=0,offset=(0,0),limbs=None):
    r=a['rest'];pivot=r['hip'];delta=Vector((*offset,0));p={k:pivot+delta+rotate(v-pivot,angle) for k,v in r.items()}
    for side,chain,angles in (limbs or []):
        for start,end,t in zip(chain,chain[1:],angles):p[side+end]=p[side+start]+rotate(r[side+end]-r[side+start],t)
    for k,v in p.items():o=a['controls'][k];o.location=v;o.keyframe_insert(data_path='location',frame=frame)
    return p

def smooth_actor(a):
    for ob in a['controls'].values():
        if ob.animation_data:
            for layer in ob.animation_data.action.layers:
                for strip in layer.strips:
                    for bag in strip.channelbags:
                        for fc in bag.fcurves:
                            for k in fc.keyframe_points:k.interpolation='BEZIER';k.handle_left_type=k.handle_right_type='AUTO_CLAMPED'

def face_keys(a,openings,smiles=None,angry=False):
    fac=a['facial'];mouth=fac['mouth']
    for prop,vals in [('open',openings),('smile',smiles or [(1,0)])]:
        for f,v in vals:mouth[prop]=v;mouth.keyframe_insert(data_path=f'["{prop}"]',frame=f)
    for i in range(len(a['config']['eyes'])):
        sign=-1 if i==0 else 1
        keys(fac['brow'+str(i)],'rotation_euler',[(1,(0,0,-sign*.3 if angry else sign*.05)),(100,(0,0,-sign*.2)),(124,(0,0,sign*.35)),(190,(0,0,sign*.08))])
        keys(fac['eye'+str(i)],'scale',[(1,(1,1,1)),(90,(1,1,1)),(93,(1,.08,1)),(96,(1,1,1)),(122,(1,1.2,1)),(158,(1,1,1))])

def visible_tree(ob,first,last):
    for q in [ob,*ob.children_recursive]:
        for frame,v in [(1,False),(first,True),(last+1,False)]:A['base']['visibility'](q,v,frame)

def label(message,start,end,y=-.38,size=.07):
    ob=text(s.name+' / '+message,message,0,y,-2,size,'#fff8e9',cam)
    visible_tree(ob,start,end);return ob

def football(name,location):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=32,radius=.11,location=location);ob=bpy.context.object;ob.name=name
    for c in list(ob.users_collection):c.objects.unlink(ob)
    col.objects.link(ob);ob.data.materials.append(A['mat']('#f9f7ed'))
    # Native curved five-sided panels, with a round silhouette at viewing size.
    for axis in [(0,-1,0),(.85,-.35,.55),(-.85,-.35,.55),(0,-.35,-1),(0,1,0)]:
        n=Vector(axis).normalized();u=n.cross(Vector((0,0,1)))
        if u.length<.01:u=Vector((1,0,0))
        u.normalize();v=n.cross(u);verts=[]
        for i in range(5):verts.append(tuple((n+.40*(math.cos(i*math.tau/5)*u+math.sin(i*math.tau/5)*v)).normalized()*.111))
        meshverts=[];faces=[]
        for j in range(5):
            corners=[n*.111,Vector(verts[j]),Vector(verts[(j+1)%5])]
            grid={}
            for a in range(9):
                for b in range(9-a):
                    point=(corners[0]*(1-(a+b)/8)+corners[1]*a/8+corners[2]*b/8).normalized()*.112
                    grid[a,b]=len(meshverts);meshverts.append(tuple(point))
            for a in range(8):
                for b in range(8-a):
                    faces.append((grid[a,b],grid[a+1,b],grid[a,b+1]))
                    if a+b<7:faces.append((grid[a+1,b],grid[a+1,b+1],grid[a,b+1]))
        me=bpy.data.meshes.new(name+' panel');me.from_pydata(meshverts,[],faces);me.materials.append(A['mat']('#514773'))
        patch=bpy.data.objects.new(me.name,me);col.objects.link(patch);patch.parent=ob
    return ob

def drama():
    scene('S02 / kick and overreaction',288,location=(.4,-8.8,2.3),target=(-.05,0,1))
    f=actor('Drama Foden','Foden',(-.65,0,.012));b=actor('Drama Bruno','Bruno',(.16,.07,.012))
    # Adjacent source frames: tussle, fall, grounded kick-out, then authored theatrics.
    arms=lambda l,r:[('L',['shoulder','elbow','wrist','finger'],l),('R',['shoulder','elbow','wrist','finger'],r)]
    for frame,t,off in [(1,-.08,(0,0)),(20,-.13,(.1,0)),(30,.12,(-.12,-.05)),(45,.88,(-.45,-.8)),(60,1.22,(-.5,-1.38)),(72,1.18,(-.5,-1.35)),(77,1.18,(-.5,-1.35)),(83,1.18,(-.5,-1.35)),(97,1.22,(-.5,-1.38)),(160,1.22,(-.5,-1.38)),(180,.8,(-.3,-.6)),(210,.15,(-.05,0)),(230,0,(0,0)),(288,0,(0,0))]:
        legs=[]
        if 60<=frame<=160:
            kick=1.65 if 77<=frame<=83 else 2.3
            legs=[('R',['hip','knee','ankle','toe'],[1.65,kick,kick]),('L',['hip','knee','ankle','toe'],[.85,1.6,1.6])]
        pose(f,frame,t,off,legs+(arms([1.05,1.4,1.9],[1.22,1.22,1.22]) if 60<=frame<=160 else []))
    for frame,t,off,la,ra in [(1,-.1,(0,0),[-.5,-.9,-.9],[.1,.1,.1]),(28,-.16,(-.2,0),[-.6,-1.1,-1.1],[.1,.1,.1]),(60,-.03,(0,0),[-.3,-.6,-.6],[.2,.2,.2]),(77,-.03,(0,0),[-.3,-.6,-.6],[.2,.2,.2]),(83,-.03,(0,0),[-.3,-.6,-.6],[.2,.2,.2]),(100,-.03,(0,0),[-.3,-.6,-.6],[.2,.2,.2]),(108,-.23,(.3,.16),[-.65,-1.9,-1.9],[.65,1.9,1.9]),(125,-.16,(.25,.04),[-.6,-1.85,-1.85],[.6,1.85,1.85]),(158,-.04,(.05,0),[-.5,-1.1,-1.1],[.5,1.1,1.1]),(178,0,(0,0),[-.12,-1.65,-1.65],[.2,.7,.7]),(288,0,(0,0),[-.12,-1.65,-1.65],[.2,.7,.7])]:
        pose(b,frame,t,off,arms(la,ra))
        for key in ('Lankle','Rankle','Ltoe','Rtoe'):
            b['controls'][key].location=b['rest'][key];b['controls'][key].keyframe_insert(data_path='location',frame=frame)
    for frame in (180,210,230,288):
        for k in ('Lankle','Rankle','Ltoe','Rtoe'):
            f['controls'][k].location=f['rest'][k];f['controls'][k].keyframe_insert(data_path='location',frame=frame)
    for a in (f,b):smooth_actor(a)
    face_keys(b,[(1,.05),(77,.05),(100,.05),(106,1.7),(135,1.1),(160,.05),(190,.12),(288,.08)],[(1,-.2),(105,-1),(160,0),(194,.9),(288,.9)])
    face_keys(f,[(1,.1),(50,.45),(82,.25),(160,.12),(288,.12)],angry=True)
    ball=football('S02 / loose football',(-1.05,-.25,.13));keys(ball,'location',[(1,(-1.05,-.25,.13)),(34,(-1.05,-.25,.13)),(64,(-1.65,-.5,.13)),(288,(-1.65,-.5,.13))])
    # Supporting player establishes the touchline dispute, with restrained background detail.
    label('23\u2032  UNITED 0\u20130 CITY',1,288,y=.405,size=.03)
    plate=empty('S02 / appeal caption',(0,-.33,-2.015),cam);rect('S02 / appeal plate',-.27,-.10,.54,.19,0,'#18303b',plate);visible_tree(plate,105,153);plate.scale=(.6,.55,1);plate.location.y=-.345
    for ob in plate.children:
        if ob.type=='CURVE':ob.data.bevel_depth=.002
    label('REF!!!',105,153,y=-.34,size=.12)
    for i in (0,1):keys(b['facial']['gaze'+str(i)],'location',[(1,(0,0,.014)),(85,(0,0,.014)),(91,(.029,0,.014)),(100,(.029,0,.014)),(106,(.009,0,.014)),(288,(.009,0,.014))])
    # Comic halo follows the exact same head control as the drawing.
    halo=empty('S02 / innocent halo',(0,1.72,.08),b['face']);line('S02 / halo ring',oval(0,0,.35,.08),.02,'#ffd66c',.035,halo);visible_tree(halo,166,228)
    paper=empty('S02 / complaint',(.0,.10,.12),b['controls']['Lfinger'])
    rect('S02 / complaint sheet',-.15,-.1,.9,1.22,0,'#fff5df',paper)
    text('S02 / complaint title','COMPLAINT',.3,.91,.025,.105,'#233340',paper)
    for y in (.65,.46,.27):line('S02 / form rule',[(.02,y),(.72,y)],.026,'#9ca4a6',.012,paper)
    visible_tree(paper,177,288)
    ref=actor('Drama Oliver','Oliver',(1.6,.65,.012))
    for frame,amount in [(1,0),(168,0),(192,.15),(232,.7),(288,.7)]:
        pose(ref,frame,limbs=arms([-.1,-.1,-.1],[amount,2.4*amount,2.4*amount]))
    smooth_actor(ref);face_keys(ref,[(1,.03),(226,.03),(243,.5),(288,.12)])
    card=empty('S02 / red decision',(0,0,.05),ref['controls']['Rfinger']);rect('S02 / card',-.16,.05,.32,.48,0,'#f13446',card);visible_tree(card,228,288)
    camera_keys([(1,(.4,-8.8,2.3),(-.05,0,1)),(102,(.5,-4.0,2.15),(.23,0,1.53)),(161,(.4,-8.8,2.3),(-.05,0,1)),(177,(.45,-4.4,2.1),(.05,0,1.5)),(227,(.4,-8.8,2.3),(-.05,0,1))])
    s['events']=json.dumps({'tussle':20,'grounded':60,'kick_out':77,'delayed_appeal':106,'innocent_halo':166,'complaint':177})
    s['authored_exaggeration']='Delayed theatrical recoil, enormous appeal, halo and immediate recovery into complaint paperwork.'
    s.frame_set(77);bpy.context.view_layer.update()

def parry():
    scene('S08 / hope and parry',168,location=(6,-4,3.0),target=(3.9,6.0,1.25))
    m=actor('Save Mbeumo','Mbeumo',(5.9,3.8,.012));g=actor('Save Donnarumma','Donnarumma',(3.5,8.25,.012))
    arms=lambda l,r:[('L',['shoulder','elbow','wrist','finger'],l),('R',['shoulder','elbow','wrist','finger'],r)]
    for f,t,k in [(1,0,0),(22,-.10,.35),(34,-.08,.45),(39,.08,-.25),(49,.14,-.85),(70,.03,-.1),(168,.03,-.1)]:
        pose(m,f,t,limbs=[('L',['hip','knee','ankle','toe'],[k,k,k])]+arms([-.15,-.5,-.5],[.3,.5,.5]))
    for f,t,off in [(1,0,(0,0)),(32,0,(0,-.08)),(46,.25,(-.1,.08)),(62,.7,(-.55,.45)),(68,.88,(-.75,.48)),(75,1.04,(-1.05,.32)),(88,1.32,(-1.25,-.55)),(101,1.43,(-1.25,-1.3)),(168,1.43,(-1.25,-1.3))]:
        la=[-.65,-1.8,-1.8] if f>=46 else [-.15,-.5,-.5]
        ra=[.55,1.5,1.5] if f>=46 else [.15,.5,.5]
        pose(g,f,t,off,arms(la,ra))
    smooth_actor(m);smooth_actor(g)
    face_keys(m,[(1,.03),(39,.3),(67,.03),(76,.9),(120,.03),(168,.03)],[(1,.3),(66,.3),(79,-1),(168,-1)])
    face_keys(g,[(1,.02),(67,.2),(92,.1),(168,.1)])
    for i in (0,1):keys(g['facial']['gaze'+str(i)],'location',[(1,(-.018,0,.014)),(168,(-.018,0,.014))])
    s.frame_set(39);bpy.context.view_layer.update();start=m['controls']['Ltoe'].matrix_world.translation.copy();start+=Vector((-.07,-.02,-.025))
    s.frame_set(68);bpy.context.view_layer.update();contact=g['controls']['Lfinger'].matrix_world.translation.copy();contact+=Vector((-.025,-.04,.035))
    ball=football('S08 / shot football',start)
    keys(ball,'location',[(1,Vector((start.x,start.y,.13))),(34,Vector((start.x,start.y,.13))),(39,start),(67,contact+(start-contact)*.055),(68,contact),(70,contact+Vector((-.28,-.10,.26))),(80,contact+Vector((-1.8,-.60,.95))),(98,contact+Vector((-4,-1.3,.20))),(168,contact+Vector((-4,-1.3,.20)))])
    # Linear flight into and away from the open glove; no catch or possession hold.
    for layer in ball.animation_data.action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    for k in fc.keyframe_points:k.interpolation='LINEAR'
    label('90+5′  ONE LAST CHANCE',1,65,y=.40,size=.035)
    label('DENIED.',80,130,y=-.36,size=.07)
    s['events']=json.dumps({'strike':39,'glove_parry':68,'landing':101})
    s['source_action']='Left-foot attempt; keeper reaches with open glove and deflects ball outward, never catches.'
    s['cast_roles']='Mbeumo shooter, Donnarumma keeper. Tight action excerpt; wider match context belongs to the full animatic.'
    s.frame_set(68);bpy.context.view_layer.update()

def apology():
    scene('S10 / tears and umbrella',192,location=(.5,-7.0,2.3),target=(.2,0,1.15))
    r=actor('Apology Oliver','Oliver',(-.85,0,.012));c=actor('Apology Carrick','Carrick',(.90,.12,.012))
    arms=lambda l,rr:[('L',['shoulder','elbow','wrist','finger'],l),('R',['shoulder','elbow','wrist','finger'],rr)]
    for f,t,off in [(1,.08,(0,0)),(25,.14,(0,-.15)),(44,.17,(0,-.40)),(65,.20,(0,-.40)),(80,.15,(0,-.40)),(95,.21,(0,-.40)),(110,.15,(0,-.40)),(125,.21,(0,-.40)),(150,.15,(0,-.40)),(192,.15,(0,-.40))]:
        pose(r,f,t,off,arms([-.2,-1.4,-1.4],[.2,1.4,1.4])+([] if f>=44 else []))
        for side in ('L','R'):
            for part in ('ankle','toe'):
                k=side+part;r['controls'][k].location=r['rest'][k];r['controls'][k].keyframe_insert(data_path='location',frame=f)
            if f>=44:
                k=side+'knee';r['controls'][k].location=r['rest'][k]+Vector((-.30 if side=='L' else .30,-.13,0));r['controls'][k].keyframe_insert(data_path='location',frame=f)
    for f,t in [(1,0),(75,0),(95,-.03),(118,-.03),(158,0),(192,0)]:pose(c,f,t,limbs=arms([-.08,-1.6,-1.6],[.08,.1,.1]))
    smooth_actor(r);smooth_actor(c)
    face_keys(r,[(1,.15),(40,.8),(70,1.4),(98,.8),(120,1.4),(160,.7),(192,.7)],[(1,-.4),(44,-1),(192,-1)])
    face_keys(c,[(1,.02),(138,.02),(149,.35),(157,.05),(165,.4),(176,.03),(192,.03)])
    for i in (0,1):
        # Every stream's first point is exactly the animated eye control, in face space.
        eye=r['facial']['eye'+str(i)];ex,ey=eye.location.x,eye.location.y
        jet=empty('S10 / tear jet '+str(i),(0,0,.065),r['face'])
        sign=-1 if i==0 else 1
        pts=[(ex+sign*(2.8 if i else 1.25)*t/20,ey+.6*math.sin(math.pi*t/20)-1.5*(t/20)**2) for t in range(21)]
        line('S10 / eye-anchored water '+str(i),pts,0,'#58c8ed',.035,jet)
        line('S10 / water highlight '+str(i),[(x-.005,y+.014) for x,y in pts],.003,'#cbf8ff',.006,jet)
        visible_tree(jet,47,192)
        for f,scale in [(47,.01),(58,1),(78,.92),(93,1),(111,.90),(130,1),(150,.93),(192,.93)]:
            # Scale around the eye, keeping the outlet fixed under the lid.
            jet.location=(ex*(1-scale),ey*(1-scale),.065);jet.scale=(scale,scale,1);jet.keyframe_insert(data_path='location',frame=f);jet.keyframe_insert(data_path='scale',frame=f)
    umbrella=empty('S10 / umbrella',(0,.1,.09),c['controls']['Lfinger'])
    line('S10 / umbrella shaft',[(0,0),(1.4,2.15)],0,'#41495b',.025,umbrella)
    canopy=[(-1.25,1.9)]+[(1.25*math.cos(math.pi-k*math.pi/24),1.9+.6*math.sin(math.pi-k*math.pi/24)) for k in range(25)]
    poly('S10 / umbrella canopy',[(x+1.4,y) for x,y in canopy],.03,'#d43148',umbrella)
    for x in (-1.25,-.63,0,.63,1.25):line('S10 / umbrella rib',[(1.4,2.5),(x+1.4,1.9)],.04,'#852f48',.012,umbrella)
    visible_tree(umbrella,98,192)
    label('THE APOLOGY  /  comic fantasy',1,192,y=.40,size=.033)
    label('Any points with that?',143,192,y=-.36,size=.06)
    s['events']=json.dumps({'collapse':44,'tears':47,'umbrella':98,'deadpan_reply':149})
    s['authored_exaggeration']='Fictional crying apology and umbrella; not documentary footage or a literal claim.'
    s.frame_set(120);bpy.context.view_layer.update()

def save():
    OUT.mkdir(exist_ok=True);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'dramatic-actions-v002.blend'))
    return {'file':bpy.data.filepath,'scenes':[x.name for x in SCENES]}

def verify():
    """One scene integration check for contacts, eye anchors and skin ownership."""
    report={'scenes':{},'audio':'Silent picture diagnostic; audition pending.'}
    for shot in SCENES:
        report['scenes'][shot.name]={'frames':shot.frame_end,'fps':24,'events':json.loads(shot['events'])}
    for a in CAST.values():
        for side in ('L','R'):
            point=a['rest'][side+'finger'];v=min(a['skin'].data.vertices,key=lambda v:(v.co-point).length_squared)
            owner=a['skin'].vertex_groups[max(v.groups,key=lambda g:g.weight).group].name
            assert owner.startswith(side) and any(k in owner for k in ('hand','forearm')), (a['root'].name,owner)
    shot=SCENES[0];bpy.context.window.scene=shot;shot.frame_set(77);bpy.context.view_layer.update()
    f=CAST['Drama Foden'];b=CAST['Drama Bruno'];boot=f['controls']['Rtoe'].matrix_world.translation
    thigh=(b['controls']['Lhip'].matrix_world.translation+b['controls']['Lknee'].matrix_world.translation)/2
    distance=(boot-thigh).length;assert distance<.15,distance
    hand=f['controls']['Lfinger'].matrix_world.translation.z;assert 0<hand<.06,hand
    report['kick']={'boot_to_thigh_center_m':distance,'support_hand_height_m':hand}
    shot=SCENES[1];bpy.context.window.scene=shot;shot.frame_set(68);bpy.context.view_layer.update()
    ball=next(o for o in shot.objects if o.name=='S08 / shot football');g=CAST['Save Donnarumma'];glove=g['controls']['Lfinger'].matrix_world.translation
    contact=ball.matrix_world.translation.copy();distance=(contact-glove).length;assert distance<.10,distance
    shot.frame_set(70);bpy.context.view_layer.update();depart=(ball.matrix_world.translation-contact).length;assert depart>.3,depart
    report['parry']={'ball_to_glove_control_m':distance,'departure_two_frames_m':depart}
    shot=SCENES[2];bpy.context.window.scene=shot;r=CAST['Apology Oliver'];worst=0
    for f in (47,58,78,95,120,150,192):
        shot.frame_set(f);bpy.context.view_layer.update()
        for i in (0,1):
            eye=r['facial']['eye'+str(i)];jet=next(o for o in shot.objects if o.name=='S10 / tear jet '+str(i))
            p=jet.matrix_world@Vector((eye.location.x,eye.location.y,0));q=eye.matrix_world.translation
            # Water is slightly in front of the eye surface to avoid z-fighting.
            error=(p-q).length;worst=max(worst,error);assert error<.025,error
    report['tears']={'max_eye_outlet_distance_m':worst,'checked_frames':[47,58,78,95,120,150,192]}
    (OUT/'native-checks.json').write_text(json.dumps(report,indent=2)+'\n');return report

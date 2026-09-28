"""Visible authoring: requested VAR-door reveal and clean audience captions."""
from pathlib import Path
import bpy,json,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/animatic-v003'
r=bpy.app.driver_namespace['cast_repair'];D,A=r['D'],r['A']

def build():
    OUT.mkdir(exist_ok=True)
    edit=json.loads((ROOT/'artifacts/animatic-v002/edit.json').read_text())
    removed=[]
    for row in edit:
        s=bpy.data.scenes[row['scene']]
        for o in list(s.objects):
            if o.type!='FONT':continue
            body=o.data.body
            if 'comic fantasy' in body.lower():
                removed.append({'scene':s.name,'text':body})
                o.data=o.data.copy()
                if body.startswith('THE APOLOGY'):o.data.body='THE APOLOGY'
                else:
                    for col in list(o.users_collection):
                        if col in s.collection.children[:]:col.objects.unlink(o)
    if removed:(OUT/'removed-production-text.json').write_text(json.dumps(removed,indent=2)+'\n')
    s=D['scene']('REVISION S10 / Foden exits VAR Room',144,(.6,-7,2.1),(.3,.2,1.2))
    for o in list(D['col'].objects):
        if o.name.startswith('A /'):D['col'].objects.unlink(o)
    def box(name,loc,scale,color):
        bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.scale=scale
        for c in list(o.users_collection):c.objects.unlink(o)
        D['col'].objects.link(o);o.data.materials.append(A['mat'](color));return o
    box('VAR exterior pitch',(0,-1,-.09),(20,20,.15),'#6eaa58')
    box('VAR wall left',(-2.2,.55,1.5),(2.8,.18,3),'#697483')
    box('VAR wall right',(2.5,.55,1.5),(3.4,.18,3),'#697483')
    box('VAR lintel',(0,.55,2.85),(1.6,.18,.3),'#697483')
    box('VAR dark interior',(0,1.4,1.25),(1.65,.1,2.5),'#182731')
    box('VAR threshold',(0,.45,.015),(1.7,.5,.045),'#d6d2c5')
    for x in (-.86,.86):box('VAR white jamb',(x,.38,1.32),(.1,.12,2.64),'#e4e1d7')
    box('VAR white lintel',(0,.38,2.62),(1.8,.12,.1),'#e4e1d7')
    box('VAR stadium red trim left',(-2.25,.42,.22),(2.7,.05,.25),'#a03940')
    box('VAR stadium red trim right',(2.6,.42,.22),(3.3,.05,.25),'#a03940')
    hinge=D['empty']('VAR door hinge',(-.8,.32,.035))
    panel=D['empty']('VAR door artwork',(0,0,0),hinge);panel.rotation_euler.x=math.pi/2
    D['rect']('VAR door panel',0,0,1.6,2.52,0,'#253d50',panel)
    D['rect']('VAR door sign',.16,1.91,1.28,.37,.02,'#fff3dc',panel)
    D['text']('VAR Room sign','VAR Room',.8,2.08,.04,.23,'#243440',panel)
    D['line']('VAR door handle',[(1.40,1.15),(1.40,1.33)],.035,'#eee9ce',.024,panel)
    D['keys'](hinge,'rotation_euler',[(1,(0,0,0)),(26,(0,0,0)),(47,(0,0,-1.55)),(144,(0,0,-1.55))])
    # Reuse the reviewed complete Foden drawing and its measured binding.
    a=D['actor']('VAR exit Foden','Foden',(0,.68,.025));a['root'].rotation_euler=(math.pi/2,0,0)
    shadow=bpy.data.objects['A VAR exit Foden / ground shadow']
    # Forward steps use two-bone knees in the actual direction of travel.
    rest=a['rest'];scale=.30
    steps=[('R',42,65,.44),('L',65,88,.25),('R',88,111,.03)]
    for f in range(1,145):
        t=max(0,min(1,(f-42)/69));x=0;y=.68-.55*t
        a['root'].location=(x,y,.025);a['root'].keyframe_insert(data_path='location',frame=f)
        shadow.location=(x,y-.68,0);shadow.keyframe_insert(data_path='location',frame=f)
        off=(0,-.25-.025*math.sin(t*3*math.pi)**2)
        p=D['pose'](a,f,0,off,[('L',['shoulder','elbow','wrist','finger'],[-.05,-.65,-.65]),('R',['shoulder','elbow','wrist','finger'],[.06,.10,.10])])
        for side in ('L','R'):
            wy=.68;lift=0
            for who,start,end,destination in steps:
                if who!=side or f<start:continue
                if f>=end:wy=destination
                else:
                    q=(f-start)/(end-start);q=q*q*(3-2*q);wy=wy+(destination-wy)*q;lift=.055*math.sin(math.pi*q)
            ankle=rest[side+'ankle'].copy();ankle.z=(y-wy)/scale;ankle.y+=lift/scale
            hip=p[side+'hip'];d=ankle-hip;length=d.length
            l1=(rest[side+'knee']-rest[side+'hip']).length;l2=(rest[side+'ankle']-rest[side+'knee']).length
            assert length<l1+l2+.04,(f,side,length,l1+l2)
            axis=d.normalized();bend=Vector((-.2 if side=='L' else .2,0,1));bend=(bend-axis*bend.dot(axis)).normalized()
            along=(l1*l1-l2*l2+length*length)/(2*length)
            knee=hip+axis*along+bend*math.sqrt(max(0,l1*l1-along*along))
            for key,v in [(side+'ankle',ankle),(side+'toe',ankle+rest[side+'toe']-rest[side+'ankle']),(side+'knee',knee)]:
                o=a['controls'][key];o.location=v;o.keyframe_insert(data_path='location',frame=f)
    D['face_keys'](a,[(1,.03),(99,.03),(116,.10),(144,.03)],[(1,.1),(100,.1),(118,.8),(144,.8)])
    # Pupils glance back at the door, then toward the fishing destination.
    for i in (0,1):D['keys'](a['facial']['gaze'+str(i)],'location',[(1,(0,0,.014)),(109,(0,0,.014)),(115,(-.018,0,.014)),(128,(-.018,0,.014)),(136,(.018,0,.014)),(144,(.018,0,.014))])
    rod=D['empty']('VAR exit fishing rod',(.02,0,.08),a['controls']['Lfinger'])
    D['line']('VAR exit bamboo',[(0,0),(-.2,2.8),(-.07,3.1)],.015,'#836046',.024,rod)
    D['line']('VAR exit line',[(-.07,3.1),(.34,2.2),(.38,.55)],.025,'#ece6d0',.008,rod)
    D['visible_tree'](rod,1,144)
    r['cuts'](s,[(1,(0,-3.8,2.2),(0,.32,2.05),50),(25,(.35,-6.6,2.1),(.35,.2,1.25),44),(108,(.35,-4.5,2.1),(0,0,1.55),47)])
    s['events']=json.dumps({'start':1,'door_open':27,'step_1':65,'step_2':88,'step_3':111,'knowing_look':115})
    s['Story']='Fictional satirical reveal: Foden exits a VAR Room carrying his fishing rod. No historical claim.'
    edit.insert(15,dict(beat='S10',scene=s.name,frames=144))
    frame=1
    for row in edit:row['start_frame']=frame;frame+=row['frames']
    assert frame-1==3768
    (OUT/'edit.json').write_text(json.dumps(edit,indent=2)+'\n')
    (OUT/'native-events.json').write_text(json.dumps({row['scene']:json.loads(bpy.data.scenes[row['scene']].get('events','{}')) for row in edit},indent=2)+'\n')
    s.frame_set(118);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'combined-animatic-v003.blend'))
    return {'frames':3768,'seconds':157,'removed':removed,'scene':s.name}

def voice_timing():
    rows=json.loads((OUT/'mouth-timing.json').read_text());grouped={};changed=set()
    for row in rows:grouped.setdefault(row['mouth'],[]).append(row)
    for name,group in grouped.items():
        s=bpy.data.scenes[group[0]['scene']]
        matches=[q for q in s.objects if q.name==name or q.name.startswith(name+'.')]
        assert len(matches)==1,(name,[q.name for q in matches])
        o=matches[0]
        for row in group:row['mouth']=o.name
        if o.type=='FONT':continue
        assert o.name in s.objects,(name,s.name)
        talking_post='open' not in o
        for fc in r['curves'](o):
            if fc.data_path==('["open"]' if not talking_post else 'scale'):
                if talking_post and fc.array_index!=1:continue
                while fc.keyframe_points:fc.keyframe_points.remove(fc.keyframe_points[-1],fast=True)
        def key(fr,value):
            if talking_post:o.scale.y=.18+value;o.keyframe_insert(data_path='scale',index=1,frame=fr)
            else:o['open']=value;o.keyframe_insert(data_path='["open"]',frame=fr)
        key(1,.025);key(s.frame_end,.025)
        for row in group:
            for fr,value in row['jaw_keys']:key(fr,value)
        for fc in r['curves'](o):
            if fc.data_path=='["open"]':
                for k in fc.keyframe_points:k.interpolation='BEZIER';k.handle_left_type=k.handle_right_type='AUTO_CLAMPED'
        changed.add(s.name)
    for row in rows:
        s=r['select_scene'](row['scene']);end=min(s.frame_end,row['frame']+math.ceil(row['duration_seconds']*24)+8)
        for o in s.objects:
            if o.type=='FONT' and o.data.body.replace('’',"'")==row['text'].replace('’',"'"):
                for q in [o,*o.children_recursive]:
                    for fc in r['curves'](q):
                        if fc.data_path in ('hide_render','hide_viewport'):
                            while fc.keyframe_points:fc.keyframe_points.remove(fc.keyframe_points[-1],fast=True)
                D['visible_tree'](o,row['frame'],end)
        changed.add(s.name)
    (OUT/'mouth-timing.json').write_text(json.dumps(rows,indent=2)+'\n')
    # No on-picture provenance or production labels; satire stays documented here.
    texts=[{'scene':row['scene'],'text':o.data.body} for row in json.loads((OUT/'edit.json').read_text()) for o in bpy.data.scenes[row['scene']].objects if o.type=='FONT']
    assert not any(any(word in t['text'].lower() for word in ('comic fantasy','staging','diagnostic','inspired by','review candidate')) for t in texts)
    (OUT/'audience-text-audit.json').write_text(json.dumps(texts,indent=2)+'\n')
    (OUT/'changed-scenes.json').write_text(json.dumps(sorted(changed|{'S10 / tears and umbrella','REVISION S10 / Foden exits VAR Room','REPAIR S10 / roof waterfall and fishing'}),indent=2)+'\n')
    r['select_scene']('REVISION S10 / Foden exits VAR Room').frame_set(118)
    bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'combined-animatic-v003.blend'))
    return {'new_takes':len(rows),'changed_scenes':len(changed),'on_picture_texts_checked':len(texts)}

"""S01 native staging. Run setup(), cast(), blocking() in the visible Blender instance.
Reuses the inspected flat-art primitives; does not open or reset another film.
"""
from pathlib import Path
import ast, bpy, hashlib, json, math, random
ROOT=Path(__file__).resolve().parents[1]; WORK=ROOT.parents[3]; OUT=ROOT/'artifacts/staging-v001'
# Import only pure inspected definitions, avoiding the historical script's top-level build.
source=WORK/'experiments/008_cartoon_skin/build_skin.py'
node=ast.parse(source.read_text()); wanted={'material','polygon','oval'}
exec(compile(ast.Module(body=[n for n in node.body if isinstance(n,ast.FunctionDef) and n.name in wanted],type_ignores=[]),str(source),'exec'))
M={}; actors={}; INK='#171e27'
def mat(color):
    if color not in M:M[color]=material(color,color)
    return M[color]
def poly(name,points,z,color,parent=None,outline=True):return polygon(name,points,z,mat(color),parent,outline)
def rect(name,x,y,w,h,z,c,parent=None,outline=True):return poly(name,[(x,y),(x+w,y),(x+w,y+h),(x,y+h)],z,c,parent,outline)
def empty(name,loc=(0,0,0),parent=None):
    o=bpy.data.objects.new(name,None);skin.objects.link(o);o.parent=parent;o.location=loc;o.empty_display_size=.12;return o
def line(name,pts,z,color=INK,width=.018,parent=None):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=width;d.bevel_resolution=2
    sp=d.splines.new('POLY');sp.points.add(len(pts)-1)
    for p,xy in zip(sp.points,pts):p.co=(*xy,z,1)
    d.materials.append(mat(color));o=bpy.data.objects.new(name,d);skin.objects.link(o);o.parent=parent;return o
def text(name,body,x,y,z,size=.3,color=INK,parent=None,align='CENTER'):
    d=bpy.data.curves.new(name,'FONT');d.body=body;d.size=size;d.align_x=align;d.align_y='CENTER';d.font=font;d.materials.append(mat(color))
    o=bpy.data.objects.new(name,d);skin.objects.link(o);o.location=(x,y,z);o.parent=parent;return o
def visibility(obj,visible,f):
    obj.hide_render=obj.hide_viewport=not visible
    obj.keyframe_insert(data_path='hide_render',frame=f);obj.keyframe_insert(data_path='hide_viewport',frame=f)
def key(obj,prop,f):obj.keyframe_insert(data_path=prop,frame=f)
def bind_limb_handles(curve,targets):
    # Coordinate drivers do not recalculate Blender's AUTO handles. Bind all geometry.
    coords=[(1,0,0),(0,1,0),(0,0,1)]
    if targets[1]==targets[2]:coords[1]=(.5,0,.5)
    tangents=[tuple((b-a)/3 for a,b in zip(coords[0],coords[1])),tuple((c-a)/6 for a,c in zip(coords[0],coords[2])),tuple((c-b)/3 for b,c in zip(coords[1],coords[2]))]
    for i,p in enumerate(curve.splines[0].bezier_points):
        p.handle_left_type=p.handle_right_type='FREE'
        for prop,sign in [('co',0),('handle_left',-1),('handle_right',1)]:
            weights=[a+sign*b for a,b in zip(coords[i],tangents[i])]
            for axis,letter in enumerate('XY'):
                dr=p.driver_add(prop,axis).driver
                while dr.variables:dr.variables.remove(dr.variables[0])
                for name,target in zip('abc',targets):
                    v=dr.variables.new();v.name=name;v.type='TRANSFORMS';v.targets[0].id=target;v.targets[0].transform_type='LOC_'+letter;v.targets[0].transform_space='LOCAL_SPACE'
                dr.expression='+'.join(f'({w})*{name}' for w,name in zip(weights,'abc'))
            getattr(p,prop).z=p.co.z
def driven_limb(name,targets,radius,color,parent,z):
    objs=[]
    for suffix,r,c,zz in [(' ink',radius+.018,INK,z),(' fill',radius,color,z+.025)]:
        d=bpy.data.curves.new(name+suffix,'CURVE');d.dimensions='3D';d.bevel_depth=r;d.bevel_resolution=3;d.use_fill_caps=True;d.resolution_u=12
        sp=d.splines.new('BEZIER');sp.bezier_points.add(2)
        for p,target in zip(sp.bezier_points,targets):
            p.co=(target.location.x,target.location.y,zz);p.handle_left_type=p.handle_right_type='AUTO'
            for axis,tt in [(0,'LOC_X'),(1,'LOC_Y')]:
                dr=p.driver_add('co',axis).driver;v=dr.variables.new();v.name='pos';v.type='TRANSFORMS';v.targets[0].id=target;v.targets[0].transform_type=tt;v.targets[0].transform_space='LOCAL_SPACE';dr.expression='pos'
        bind_limb_handles(d,targets)
        d.materials.append(mat(c));o=bpy.data.objects.new(name+suffix,d);skin.objects.link(o);o.parent=parent;objs.append(o)
    return objs

def setup():
    global s,skin,ink,font,cam
    assert not bpy.data.filepath and not bpy.data.is_dirty, 'Inspect/preserve current project before a fresh build.'
    s=bpy.data.scenes.new('Samtoons S01 — Morning Pep');bpy.context.window.scene=s
    skin=bpy.data.collections.new('S01 / editable artwork');s.collection.children.link(skin);ink=mat(INK)
    font=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Bold.ttf')
    s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=16
    s.render.resolution_x=1920;s.render.resolution_y=1080;s.render.resolution_percentage=50;s.render.fps=24;s.render.fps_base=1;s.frame_start=1;s.frame_end=192
    s.render.use_sequencer=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
    s.view_settings.view_transform='Standard';s.view_settings.look='None';s.world=bpy.data.worlds.new('Flat graphic world');s.world.color=(.1,.1,.1)
    d=bpy.data.cameras.new('S01 camera');d.type='ORTHO';d.ortho_scale=16;cam=bpy.data.objects.new('S01 camera',d);skin.objects.link(cam);cam.location=(0,0,30);s.camera=cam
    rect('Sky',-15,-9,30,18,-10,'#b8cddd',outline=False)
    rect('Roof dark',-15,3.2,30,1.8,-9,'#233744')
    for x in range(-16,17,2):
        line('Roof diagonal',[(x,4.45),(x+1,3.4),(x+2,4.45)],-8.9,'#899a9f',.028)
    rect('Stand rear',-15,-.5,30,3.8,-8.8,'#70363f',outline=False)
    rng=random.Random(43)
    # Native flat crowd: grouped spectator silhouettes, not a texture/noise stand-in.
    for row in range(7):
        y=.0+row*.39
        for col in range(64):
            x=-14.5+col*.46+(row%2)*.2; c=rng.choice(['#ad4c53','#5b5869','#c47770','#334d62','#ddb28e','#5a3040'])
            poly('Crowd / shoulders',oval(x,y,.21,.19),-8.5+row*.003,c,outline=False)
            poly('Crowd / head',oval(x,y+.2,.105,.115),-8.4+row*.003,rng.choice(['#b37a60','#dcb69b','#825d55']),outline=False)
    rect('Old Trafford ribbon',-15,2.8,30,.46,-7.5,'#9b283b')
    for x in (-10,0,10):text('Stadium sign','OLD TRAFFORD',x,3.025,-7.4,.32,'#fff2de')
    rect('Advertising rail',-15,-.8,30,.78,-7,'#f0eee4')
    for x in (-10,-5,0,5,10):text('Samtoons original board','SAMTOONS',x,-.4,-6.9,.29,'#b93842')
    rect('Pitch',-15,-9,30,8.2,-6,'#56a76a',outline=False)
    for j in range(7):rect('Mowing stripe',-15+j*4,-9,2,8.2,-5.98,'#65b77a',outline=False)
    line('Touchline',[(-15,-1.15),(15,-1.15)],-5.8,'#f7f5e7',.035)
    # Dugout and its seats establish the greeting's touchline location.
    poly('Dugout shell',[(.7,-2.7),(.7,.45),(1.1,1.05),(6.8,1.05),(7.4,.4),(7.4,-2.7)],-5.2,'#344c5c')
    for x in (1.4,2.6,3.8,5,6.2):
        rect('Seat',x,-1.9,1,1.8,-5,'#4c687a');rect('Headrest',x+.1,-.04,.8,.35,-4.9,'#8b2939')
    line('Technical area',[(-.8,-3.8),(7.7,-3.8),(7.7,-1.3)],-4.8,'#f7f5e7',.024)
    for area in bpy.context.screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL';area.spaces.active.overlay.show_overlays=False
    s['Review scope']='S01 staging and sound candidates. Not a full film or approved character asset.'
    s['Construction']='Editable native mesh/curve bodies, hands, set and props; original generated facial replacement drawings.'

def head_material():
    image=bpy.data.images.load(str(ROOT/'assets/art-v001/haaland-maresca-heads.png'));image.pack()
    m=bpy.data.materials.new('Original illustrated facial replacements');m.use_nodes=True;n=m.node_tree.nodes;n.clear()
    out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');im=n.new('ShaderNodeTexImage');im.image=image
    trans=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');m.node_tree.links.new(im.outputs['Color'],em.inputs[0]);m.node_tree.links.new(im.outputs['Alpha'],mix.inputs[0]);m.node_tree.links.new(trans.outputs[0],mix.inputs[1]);m.node_tree.links.new(em.outputs[0],mix.inputs[2]);m.node_tree.links.new(mix.outputs[0],out.inputs['Surface'])
    m.surface_render_method='DITHERED'
    return m,image

def portrait(name,cell,parent,height,hm):
    # UV cropping is native mesh preparation. Original generated pixels remain unchanged.
    row,col=cell;bounds=[[(.08,.52,.445,.99),(.54,.52,.905,.99)],[(.095,.025,.455,.49),(.56,.025,.92,.49)]][row][col]
    u0,v0,u1,v1=bounds;w=height*(u1-u0)/(v1-v0)
    vs=[(-w/2,0,.55),(w/2,0,.55),(w/2,height,.55),(-w/2,height,.55)]
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],[(0,1,2,3)]);me.materials.append(hm);uv=me.uv_layers.new()
    coords=[(u0,v0),(u1,v0),(u1,v1),(u0,v1)]
    if row==1:coords=[(u1,v0),(u0,v0),(u0,v1),(u1,v1)]
    for i,p in enumerate(coords):uv.data[i].uv=p
    o=bpy.data.objects.new(name,me);skin.objects.link(o);o.parent=parent;return o

def cast():
    hm,image=head_material()
    for name,x,y,shirt,skincolor,coach in [('Haaland',-2.65,-1.05,'#8fcee4','#f3b888',False),('Maresca',2.6,-1.28,'#293747','#dc9c78',True)]:
        a={};root=empty(name+' / ROOT',(x,y,0));a['root']=root
        poly(name+' / Ground shadow',oval(0,-2.43,.85,.14),-.2,'#438555',root,False)
        # Whole external silhouette, with interior kit color changes, rather than outlined waist caps.
        torso=[(-.25,1.67),(.25,1.67),(.73,1.4),(.7,1.05),(.51,.9),(.46,-.23),(.48,-.57),(.08,-.61),(0,-.26),(-.08,-.61),(-.48,-.57),(-.46,-.23),(-.51,.9),(-.7,1.05),(-.73,1.4)]
        poly(name+' / Torso silhouette',torso,.24,shirt,root)
        if not coach:
            poly(name+' / White shorts',[(-.46,.02),(.46,.02),(.48,-.57),(.08,-.61),(0,-.26),(-.08,-.61),(-.48,-.57)],.265,'#f3f1e7',root,False)
            line(name+' / Kit waistband',[(-.46,.04),(.46,.04)],.28,INK,.015,root)
            line(name+' / Shirt panel',[(-.36,1.15),(0,1.03),(.38,1.15)],.29,'#6daecb',.026,root)
            text(name+' / shirt lettering','ETIHAD',0,.85,.32,.17,'#ffffff',root)
            text(name+' / shirt lettering small','AIRWAYS',0,.65,.32,.095,'#ffffff',root)
            text(name+' / Shorts number','9',-.29,-.29,.32,.22,INK,root)
            poly(name+' / Crest',oval(.33,1.30,.095,.1),.32,'#ecdfb8',root)
            poly(name+' / Crest center',oval(.33,1.30,.067,.072),.34,'#a9d5e7',root,False)
        else:
            line(name+' / Zip',[(0,.2),(0,1.52)],.3,'#728292',.012,root)
            line(name+' / Jacket edge',[(-.4,.2),(-.27,.32)],.3,'#111e2a',.018,root)
            poly(name+' / Coach badge',oval(.32,1.22,.11,.11),.31,'#96cbdc',root)
        # Continuous neck attached behind collar and facial layer.
        rect(name+' / Neck',-.18,1.47,.36,.48,.35,skincolor,root,False)
        line(name+' / Collar',[(-.26,1.64),(0,1.43),(.26,1.64)],.38,'#d3ebed' if not coach else '#17232e',.032,root)
        for side in (-1,1):
            hip=empty(name+f' / hip {side}',(side*.25,-.37,0),root);knee=empty(name+f' / knee {side}',(side*.31,-1.18,0),root);foot=empty(name+f' / foot {side}',(side*.39,-2.22,0),root)
            driven_limb(name+f' / leg {side}',[hip,knee,foot],.145,shirt if coach else skincolor,root,.05)
            if not coach:line(name+' / Pale blue sock',[(side*.36,-1.53),(side*.39,-2.24)],.18,'#a7d9e7',.152,root)
            boot=[(-.22,-.12),(.11,-.12),(.34,-.16),(.38,-.26),(-.24,-.26)]
            o=poly(name+' / Boot',boot,.3,'#222936',foot)
            line(name+' / Sole',[(-.22,-.24),(.35,-.24)],.33,'#ed91a3' if not coach else '#aab6bc',.023,foot)
            shoulder=empty(name+f' / shoulder {side}',(side*.58,1.25,0),root);elbow=empty(name+f' / elbow {side}',(side*.85,.63,0),root);hand=empty(name+f' / HAND {side}',(side*.79,.04,0),root)
            a[f'hand{side}']=hand;a[f'elbow{side}']=elbow
            driven_limb(name+f' / arm {side}',[shoulder,elbow,hand],.125,shirt if coach else skincolor,root,.13)
            # Fingers stay attached to the same endpoint that drives the arm.
            handpts=[(-.10,.1),(.07,.1),(.12,.02),(.13,-.17),(.09,-.24),(.025,-.25),(-.05,-.21),(-.08,-.10),(-.13,-.02)]
            poly(name+' / Hand',handpts,.42,skincolor,hand)
            for xx in (-.025,.025,.07):line(name+' / Finger crease',[(xx,-.09),(xx+.01,-.20)],.46,'#9d674e',.008,hand)
            if not coach:poly(name+' / Sleeve',[((side*.40),1.53),(side*.77,1.4),(side*.84,1.07),(side*.55,1.00)],.32,shirt,root)
        a['head']=empty(name+' / HEAD',(0,1.61,0),root)
        a['faces']=[portrait(name+' / face '+str(i),(1 if coach else 0,i),a['head'],1.75 if coach else 1.88,hm) for i in range(2)]
        visibility(a['faces'][1],False,1)
        actors[name]=a
    # Giant readable name badge and both hands follow this one editable prop control.
    badge=empty('Maresca / ENZO badge control',(2.6,-1.40,.8));actors['Maresca']['badge']=badge
    rect('Badge / border',-.79,-.4,1.58,.8,.02,'#fff8e9',badge)
    rect('Badge / blue bar',-.77,.18,1.54,.2,.05,'#8cc8df',badge,False)
    text('Badge / word','ENZO',0,-.065,.10,.42,INK,badge)
    line('Badge / cord',[(-.43,.39),(0,.74),(.43,.39)],-.01,'#293747',.018,badge)
    # Opening result is identified as recap; it disappears before the greeting.
    ui=empty('Opening / final-result card',(0,3.68,2));actors['ui']=ui
    rect('Opening / panel',-3.42,-.47,6.84,.88,.01,'#f7f4e9',ui)
    text('Opening / result','UNITED  0–1  CITY',0,.05,.03,.38,INK,ui)
    text('Opening / date','13 SEP 2026  ·  FINAL RESULT',0,-.27,.03,.16,'#617078',ui)
    text('S01 / credit','SAMTOONS',6.98,4.0,2,.21,'#fff5e5')
    text('Review / label','STAGING · TEMP VOICE',-6.8,-4.05,2,.18,'#173446',align='LEFT')

def blocking():
    h=actors['Haaland'];m=actors['Maresca']
    # Minimal authored poses only: greeting, response, held reaction. This is not detailed animation.
    for f,angle in [(1,-.07),(43,-.07),(47,.055),(52,.015),(109,.015),(121,-.025),(192,-.025)]:
        h['head'].rotation_euler.z=angle;key(h['head'],'rotation_euler',f)
    for f,openmouth in [(1,False),(59,True),(69,False),(74,True),(89,False),(94,True),(101,False)]:
        visibility(h['faces'][0],not openmouth,f);visibility(h['faces'][1],openmouth,f)
    for f,annoyed in [(1,False),(110,True)]:
        visibility(m['faces'][0],not annoyed,f);visibility(m['faces'][1],annoyed,f)
    for f,up in [(1,0),(108,0),(114,1),(120,.93),(192,.93)]:
        m['badge'].location.y=-1.40+up*.98;key(m['badge'],'location',f)
        for side in (-1,1):
            m[f'hand{side}'].location=(side*.79,-.10+up*.98,0);key(m[f'hand{side}'],'location',f)
            m[f'elbow{side}'].location=(side*(.9+up*.09),.6+up*.02,0);key(m[f'elbow{side}'],'location',f)
    # Conceal the badge wording until the raised-card reveal.
    for name in ('Badge / word','Badge / blue bar'):
        o=bpy.data.objects[name]
        for f,show in [(1,False),(113,False),(114,True)]:visibility(o,show,f)
    # Opening graphic leaves cleanly before the character exchange.
    for obj in [actors['ui'],*actors['ui'].children]:visibility(obj,True,1);visibility(obj,False,34)
    for f,location,scale in [(1,(0,0,30),16),(107,(0,0,30),16),(108,(.15,.72,30),11.8),(192,(.15,.72,30),11.8)]:
        cam.location=location;cam.data.ortho_scale=scale;key(cam,'location',f);cam.data.keyframe_insert(data_path='ortho_scale',frame=f)
    # Cut and replacement tracks use held interpolation; pose tracks retain eased motion.
    for obj in (cam,cam.data):
        if obj.animation_data and obj.animation_data.action:
            for layer in obj.animation_data.action.layers:
                for strip in layer.strips:
                    for bag in strip.channelbags:
                        for fc in bag.fcurves:
                            for k in fc.keyframe_points:k.interpolation='CONSTANT'
    for name,frame in [('S01/head_turn',47),('S01/greeting',59),('S01/badge_reveal',114),('S01/deadpan_hold',125)]:s.timeline_markers.new(name,frame=frame)
    s.frame_set(135);bpy.context.view_layer.update()
    # Runnable editability check: hand geometry and continuous limb share live controls.
    hand=m['hand1'];old=hand.location.x;hand.location.x+=.2;bpy.context.view_layer.update()
    limb=bpy.data.objects['Maresca / arm 1 fill'];eval_limb=limb.evaluated_get(bpy.context.evaluated_depsgraph_get())
    assert abs(eval_limb.data.splines[0].bezier_points[-1].co.x-hand.location.x)<1e-5
    hand.location.x=old;bpy.context.view_layer.update()
    assert len([o for o in s.objects if o.name.startswith('Crowd / head')])==448
    s['Editability check']='Passed: moved hand target by 0.2; continuous limb followed. Facial replacement planes, badge and camera independently editable.'
    ed=s.sequence_editor_create()
    for channel,(label,folder) in enumerate([('A — recorded crowd / TEMP VOICE','audio-A-v002'),('B — foreground only / TEMP VOICE','audio-B')],1):
        sound=ed.strips.new_sound(label,str(OUT/folder/'mix-premaster.wav'),channel,1);sound.volume=10**(7/20);sound.mute=channel==2
    s.sync_mode='AUDIO_SYNC'
    bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'s01-morning-pep-v002.blend'))
    (OUT/'native-checks.json').write_text(json.dumps({'blender':bpy.app.version_string,'objects':len(s.objects),'crowd_silhouettes':448,'frames':192,'fps':24,'hand_endpoint_edit':'passed','artwork':'Original raster face replacements on editable native mesh/curve characters','limits':['Fixed-view facial art; full turns and final lip sync not established','S01 only; other match actions not yet staged','User has not reviewed this candidate']},indent=2)+'\n')
    plan=json.loads((ROOT/'production.json').read_text());plan['shots'][0]['events']={m.name.split('/')[-1]:m.frame-1 for m in s.timeline_markers};plan['shots'][0]['events']['start']=0
    (ROOT/'production.json').write_text(json.dumps(plan,indent=2)+'\n')

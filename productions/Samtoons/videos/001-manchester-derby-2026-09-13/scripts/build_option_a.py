"""Option A on editable stick-joint controls. Call setup, environment, actor, animate, save visibly.

Artwork is a continuous textured mesh; native bones transfer the same head/shoulder/
elbow/wrist/hip/knee/ankle targets to the drawing. Native facial controls are separate.
This scene is the film's S02 reaction staging, not a full-film render or final sound.
"""
from pathlib import Path
import ast, json, math, bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/staging-v004'
ART=ROOT/'assets/option-a-v001'
base={'__file__':str(ROOT/'scripts/build_staging.py')}
exec(compile((ROOT/'scripts/build_staging.py').read_text(),base['__file__'],'exec'),base)
tree=ast.parse((ROOT/'scripts/revise_neck_motion.py').read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='keys'],type_ignores=[]),'reused_clamped_keyframes','exec'))
poly,line,empty,mat,rect,text,oval=[base[n] for n in ('poly','line','empty','mat','rect','text','oval')]
actors={}

def surface(name,points,color):
    me=bpy.data.meshes.new(name);me.from_pydata(points,[],[list(range(len(points)))]);me.materials.append(mat(color))
    ob=bpy.data.objects.new(name,me);col.objects.link(ob);return ob

def tube(name,points,color,width=.025):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=width;d.bevel_resolution=2;d.use_fill_caps=True
    sp=d.splines.new('POLY');sp.points.add(len(points)-1)
    for p,xyz in zip(sp.points,points):p.co=(*xyz,1)
    d.materials.append(mat(color));ob=bpy.data.objects.new(name,d);col.objects.link(ob);return ob

def setup():
    global s,col,cam
    assert not bpy.app.background and bpy.context.window
    assert not bpy.data.is_dirty,'Preserve current edits before creating this scene'
    assert bpy.data.filepath.startswith(str(ROOT))
    assert 'S02 / Option A' not in bpy.data.scenes
    s=bpy.data.scenes.new('S02 / Option A');bpy.context.window.scene=s
    col=bpy.data.collections.new('Option A / authored scene');s.collection.children.link(col)
    base.update(s=s,skin=col,ink=mat('#202329'),font=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
    s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=24
    s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100
    s.render.fps=24;s.frame_start=1;s.frame_end=192;s.render.use_sequencer=False
    s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
    s.view_settings.view_transform='Standard';s.view_settings.look='None'
    w=bpy.data.worlds.new('Option A / world');w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(.45,.64,.8,1);w.node_tree.nodes['Background'].inputs[1].default_value=.6;s.world=w
    d=bpy.data.cameras.new('Option A / camera');d.type='PERSP';d.lens=48
    cam=bpy.data.objects.new('Option A / camera',d);col.objects.link(cam);cam.location=(2.8,-7.8,1.75);d.lens=42
    cam.rotation_euler=(Vector((.1,.4,1.1))-cam.location).to_track_quat('-Z','Y').to_euler();s.camera=cam
    s['Scope']='S02 reaction staging: A full-body artwork, joint deformation and facial acting. Silent picture review; no final voices, kick-out or parry proof.'
    s['Construction']='Stick-joint targets; weighted 2D artwork mesh; native editable facial geometry; dimensional environment.'
    for ar in bpy.context.screen.areas:
        if ar.type=='VIEW_3D':ar.spaces.active.region_3d.view_perspective='CAMERA';ar.spaces.active.shading.type='MATERIAL';ar.spaces.active.overlay.show_overlays=False
    OUT.mkdir(exist_ok=True);ART.mkdir(exist_ok=True)

def environment():
    surface('A / pitch',[(-55,-30,0),(55,-30,0),(55,38,0),(-55,38,0)],'#69ac55')
    for y in range(-25,30,6):surface('A / mowing band',[(-55,y,.001),(55,y,.001),(55,y+3,.001),(-55,y+3,.001)],'#72b65b')
    # Native rectangular goal in real depth; front remains open.
    gx,gy=3.5,9.0;w,h,depth=7.32,2.44,2.0
    def g(x,y,z):return(gx+x,gy+y,z)
    tube('A / goal front',[g(-w/2,0,0),g(-w/2,0,h),g(w/2,0,h),g(w/2,0,0)],'#fffbed',.06)
    for side in (-1,1):tube('A / goal side',[g(side*w/2,0,h),g(side*w/2,depth,h),g(side*w/2,depth,0),g(side*w/2,0,0)],'#f5f2df',.032)
    tube('A / goal rear crossbar',[g(-w/2,depth,h),g(w/2,depth,h)],'#ebeeda',.025)
    for i in range(31):
        x=-w/2+w*i/30;tube('A / net vertical',[g(x,0,h),g(x,depth,h),g(x,depth,0)],'#cdddc4',.006)
    for j in range(11):
        z=h*j/10;tube('A / net row',[g(-w/2,0,z),g(-w/2,depth,z),g(w/2,depth,z),g(w/2,0,z)],'#cdddc4',.006)
    for j in range(1,9):
        y=depth*j/8;tube('A / top net',[g(-w/2,y,h),g(w/2,y,h)],'#cdddc4',.006)
        for side in (-1,1):tube('A / side net',[g(side*w/2,y,0),g(side*w/2,y,h)],'#cdddc4',.006)
    tube('A / goal line',[(-40,gy,.018),(40,gy,.018)],'#f7f5e7',.033)
    for half,d in [(9.16,5.5),(20.16,16.5)]:tube('A / area line',[(gx-half,gy,.018),(gx-half,gy-d,.018),(gx+half,gy-d,.018),(gx+half,gy,.018)],'#f7f5e7',.035)
    # Quiet stadium architecture, not a wall of bright spectator dots.
    for low,high,y,c in [(0,3,14,'#626b82'),(3.3,6.5,16,'#717991')]:
        surface('A / crowd tier',[(-45,y,low),(45,y,low),(45,y+2,high),(-45,y+2,high)],c)
        surface('A / red tier fascia',[(-45,y,low),(45,y,low),(45,y,low+.36),(-45,y,low+.36)],'#9c3342')
        for row in range(5):
            z=low+.62+row*.49; yy=y+2*(z-low)/(high-low)-.014
            for j in range(85):
                x=-42+j+(row%2)*.5
                tube('A / quiet crowd mark',[(x+.16*math.cos(k*math.pi/8),yy,z+.16*math.sin(k*math.pi/8)) for k in range(9)],'#555f77',.018)
    surface('A / roof underside',[(-45,14,7.2),(45,14,7.2),(45,23,9),(-45,23,9)],'#444d60')
    surface('A / roof fascia',[(-45,14,7.2),(45,14,7.2),(45,14,7.65),(-45,14,7.65)],'#a63643')
    for x in range(-42,45,4):tube('A / roof truss',[(x,14,7.65),(x+2,14,8.55),(x+4,14,7.65)],'#b5bdc6',.06)
    tube('A / roof chord',[(-45,14,8.55),(45,14,8.55)],'#b5bdc6',.05)
    sign=text('A / stadium lettering','OLD TRAFFORD',0,0,0,.38,'#f6ebdf');sign.location=(-1,13.95,7.43);sign.rotation_euler.x=math.pi/2
    # Goal dimensions are a construction check; no motion quality claim.
    s['Goal width']=w;s['Goal height']=h;s['Goal depth']=depth
    bpy.context.view_layer.update()

def image_material(path):
    im=bpy.data.images.load(str(path));im.pack()
    m=bpy.data.materials.new('A / '+path.stem);m.use_nodes=True;n=m.node_tree.nodes;n.clear();links=m.node_tree.links
    out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');tex=n.new('ShaderNodeTexImage');tex.image=im;tex.interpolation='Linear';tex.extension='CLIP'
    transparent=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader')
    cutoff=n.new('ShaderNodeMath');cutoff.operation='GREATER_THAN';cutoff.inputs[1].default_value=.93
    links.new(tex.outputs['Color'],em.inputs[0]);links.new(tex.outputs['Alpha'],cutoff.inputs[0]);links.new(cutoff.outputs[0],mix.inputs[0]);links.new(transparent.outputs[0],mix.inputs[1]);links.new(em.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],out.inputs[0]);m.surface_render_method='DITHERED'
    return im,m

def stadium_detail():
    for low,high,y in [(0,3,14),(3.3,6.5,16)]:
        for x in range(-40,41,8):
            for j in range(15):
                z=low+(high-low)*j/15;yy=y+2*j/15-.03
                surface('A / aisle step',[(x-.32,yy,z),(x+.32,yy,z),(x+.32,yy+2/15,z),(x-.32,yy+2/15,z)],'#b4b2b0')
            tube('A / aisle handrail',[(x-.4,y,low+.6),(x-.4,y+2,high+.6)],'#858b99',.022)
            surface('A / entrance',[(x+.7,y-.05,low+.4),(x+1.8,y-.05,low+.4),(x+1.8,y+.65,low+1.3),(x+.7,y+.65,low+1.3)],'#3e4558')
        tube('A / terrace rail',[(-45,y-.04,low+.4),(45,y-.04,low+.4)],'#40495b',.035)

def segment_distance(p,a,b):
    d=b-a;t=max(0,min(1,(p-a).dot(d)/d.length_squared));return (p-a-t*d).length

def actor(name,config,location):
    im,material=image_material(ART/config['image']);W,H=im.size
    # Config landmarks are measured in the unmodified source image, top-left origin.
    unit=6/config['body_height'];cx=config['center_x'];floor=config['floor_y']
    def xy(p):
        x,y=p;nx,ny=config['joints']['neck'];growth=config.get('head_growth',.35)*max(0,min(1,(ny-y)/50))
        return Vector(((x-cx+growth*(x-nx))*unit,(floor-y+growth*(ny-y))*unit,0))
    rest={key:xy(p) for key,p in config['joints'].items()}
    root=empty('A '+name+' / ROOT',location);root.rotation_euler=(math.pi/2,0,math.atan2(cam.location.x-location[0],location[1]-cam.location.y));root.scale=(.30,.30,.30)
    controls={key:empty('A '+name+' / CTRL '+key,p,root) for key,p in rest.items()}
    bones={'torso':('hip','neck'),'head':('neck','head')}
    for side in ('L','R'):
        bones.update({side+' upper arm':(side+'shoulder',side+'elbow'),side+' forearm':(side+'elbow',side+'wrist'),side+' hand':(side+'wrist',side+'finger'),side+' thigh':(side+'hip',side+'knee'),side+' calf':(side+'knee',side+'ankle'),side+' foot':(side+'ankle',side+'toe')})
    ad=bpy.data.armatures.new('A '+name+' / skin binding');arm=bpy.data.objects.new(ad.name,ad);col.objects.link(arm);arm.parent=root;arm.show_in_front=True
    bpy.ops.object.select_all(action='DESELECT');arm.select_set(True);bpy.context.view_layer.objects.active=arm;bpy.ops.object.mode_set(mode='EDIT')
    for key,(a,b) in bones.items():eb=ad.edit_bones.new(key);eb.head=rest[a];eb.tail=rest[b]
    bpy.ops.object.mode_set(mode='OBJECT')
    for key,(a,b) in bones.items():
        pb=arm.pose.bones[key];c=pb.constraints.new('COPY_LOCATION');c.target=controls[a]
        c=pb.constraints.new('STRETCH_TO');c.target=controls[b];c.rest_length=(rest[b]-rest[a]).length;c.volume='NO_VOLUME';c.bulge=0
    # A continuous grid retains painted linework at the joints; no separate head sprite.
    nx,ny=72,132;verts=[];uvs=[];faces=[]
    for j in range(ny+1):
        for i in range(nx+1):verts.append(tuple(xy((W*i/nx,H*j/ny))));uvs.append((i/nx,1-j/ny))
    for j in range(ny):
        for i in range(nx):q=j*(nx+1)+i;faces.extend([(q,q+1,q+nx+2),(q,q+nx+2,q+nx+1)])
    me=bpy.data.meshes.new('A '+name+' / continuous artwork');me.from_pydata(verts,[],faces);me.materials.append(material)
    uv=me.uv_layers.new()
    for loop in me.loops:uv.data[loop.index].uv=uvs[loop.vertex_index]
    skin=bpy.data.objects.new(me.name,me);col.objects.link(skin);skin.parent=root
    groups={key:skin.vertex_groups.new(name=key) for key in bones}
    for i,v in enumerate(verts):
        p=Vector(v);side='L' if p.x<0 else 'R'
        if p.y>=rest['neck'].y+.08:candidates=['head']
        elif p.y>=rest['neck'].y-.20:candidates=['head','torso']
        elif abs(p.x)>165*unit and p.y>rest[side+'finger'].y-.30 and (p.y>rest['hip'].y+.35 or abs(p.x)>220*unit):candidates=[side+' upper arm',side+' forearm',side+' hand']
        elif p.y<rest['hip'].y-.28:candidates=[side+' thigh',side+' calf',side+' foot']
        else:candidates=['torso']
        weights=sorted([(segment_distance(p,rest[bones[k][0]],rest[bones[k][1]]),k) for k in candidates])[:2]
        values=[math.exp(-distance*distance/0.045) for distance,key in weights];total=sum(values)
        if total<1e-20:values=[1]+[0]*(len(values)-1);total=1
        for (dist,k),value in zip(weights,values):groups[k].add([i],value/total,'REPLACE')
    modifier=skin.modifiers.new('Stick controls deform the drawing','ARMATURE');modifier.object=arm;modifier.use_deform_preserve_volume=True
    face=empty('A '+name+' / FACE',(0,0,.014),root);c=face.constraints.new('COPY_LOCATION');c.target=controls['neck'];c=face.constraints.new('DAMPED_TRACK');c.target=controls['head'];c.track_axis='TRACK_Y'
    data={'root':root,'controls':controls,'rest':rest,'skin':skin,'armature':arm,'face':face,'xy':xy,'config':config,'facial':{}}
    actors[name]=data
    face_art(name)
    # Flat floor shadow is separate from the articulated drawing.
    shadow=surface('A '+name+' / ground shadow',[(location[0]+.46*math.cos(k*math.tau/48),location[1]+.16*math.sin(k*math.tau/48),.009) for k in range(48)],'#5d994c')
    bpy.context.view_layer.update();return data

def face_art(name):
    a=actors[name];face=a['face'];cfg=a['config'];unit=6/cfg['body_height']*(1+cfg.get('head_growth',.35))
    delta=a['rest']['head']-a['rest']['neck'];theta=math.atan2(-delta.x,delta.y)
    def local(p):
        v=a['xy'](p)-a['rest']['neck'];c,sn=math.cos(-theta),math.sin(-theta)
        return(v.x*c-v.y*sn,v.x*sn+v.y*c)
    for i,(x,y,w,h) in enumerate(cfg['eyes']):
        ex,ey=local((x,y));eye=empty(f'A {name} / eye {i}',(ex,ey,.024),face)
        poly(f'A {name} / eye rim {i}',oval(0,0,w*unit/2+.006,h*unit/2+.006),-.002,'#28272a',eye,False)
        poly(f'A {name} / sclera {i}',oval(0,0,w*unit/2,h*unit/2),0,'#fff9ee',eye,False)
        pupil=empty(f'A {name} / gaze {i}',(0,0,.014),eye)
        poly(f'A {name} / iris {i}',oval(0,0,h*unit*.34,h*unit*.43),0,'#4b352b',pupil,False)
        poly(f'A {name} / pupil {i}',oval(0,0,h*unit*.22,h*unit*.32),.005,'#202329',pupil,False)
        poly(f'A {name} / eye light {i}',oval(-h*unit*.07,h*unit*.12,h*unit*.065,h*unit*.09),.010,'#fffef7',pupil,False)
        a['facial']['eye'+str(i)]=eye;a['facial']['gaze'+str(i)]=pupil
    for i,(x,y,w) in enumerate(cfg['brows']):
        bx,by=local((x,y));brow=empty(f'A {name} / brow control {i}',(bx,by,.04),face)
        pts=[(-w*unit*.5,-.012),(-w*unit*.47,.011),(-w*unit*.16,.035),(w*unit*.28,.021),(w*unit*.5,0),(w*unit*.44,-.022),(0,.005)]
        poly(f'A {name} / eyebrow {i}',pts,0,'#28272a',brow,False);a['facial']['brow'+str(i)]=brow
    mx,my=local(cfg['mouth'][:2]);mouth=empty(f'A {name} / mouth control',(mx,my,.04),face)
    mouth['open']=.08;mouth['smile']=0.;mouth['width']=cfg['mouth'][2]*unit/2
    # Native geometry interpolates one mouth, instead of swapping the entire head.
    pts=[]
    for upper in (True,False):
        values=range(25) if upper else range(24,-1,-1)
        for i in values:
            x=-1+2*i/24;pts.append((x,upper))
    ob=poly(f'A {name} / mouth interior',[(0,0)]*len(pts),0,'#41212a',mouth,False)
    for i,(x,upper) in enumerate(pts):
        ob.data.vertices[i].co.x=x*mouth['width']
        d=ob.data.vertices[i].driver_add('co',1).driver
        for vname,prop in [('op','open'),('sm','smile')]:
            v=d.variables.new();v.name=vname;v.type='SINGLE_PROP';v.targets[0].id=mouth;v.targets[0].data_path=f'["{prop}"]'
        curve=.038*(1-x*x);opening=math.sqrt(max(0,1-x*x))
        d.expression=f'{-curve}*sm'+(f'+.012*{opening}' if upper else f'-(.008+op*.10)*{opening}')
    teeth=poly(f'A {name} / teeth',[(-.72*mouth['width'],.004),(.72*mouth['width'],.004),(.62*mouth['width'],-.021),(-.62*mouth['width'],-.021)],.003,'#fff7e8',mouth,False)
    for axis in (0,1):
        d=teeth.driver_add('scale',axis).driver;v=d.variables.new();v.name='op';v.type='SINGLE_PROP';v.targets[0].id=mouth;v.targets[0].data_path='["open"]';d.expression='min(1,max(0,(op-.10)*7))'
    a['facial']['mouth']=mouth

def control_key(a,key,frame,position):
    ob=a['controls'][key];ob.location=position;ob.keyframe_insert(data_path='location',frame=frame)

def animate():
    # Source script beat S02: complaint, card, and Bruno's premature confidence.
    # This staging excerpt deliberately does not depict the kick-out or late save.
    for name,a in actors.items():
        rest=a['rest'];ctl=a['controls'];fac=a['facial']
        for key,ob in ctl.items():keys(ob,'location',[(1,rest[key]),(192,rest[key])])
        side='L' if name=='Bruno' else 'R'
        motions=[(1,0),(18,-.04),(44,1),(65,.91),(93,.91),(116,.52),(148,.28),(192,.28)] if name=='Bruno' else [(1,0),(43,0),(63,.65),(89,.58),(116,.9),(144,.45),(192,.45)]
        poses={key:[] for key in ('elbow','wrist','finger')}
        for f,v in motions:
            position=rest[side+'shoulder'].copy()
            for start,end,angle in [('shoulder','elbow',.12),('elbow','wrist',1.75),('wrist','finger',1.75)]:
                d=rest[side+end]-rest[side+start];t=angle*v*(-1 if side=='L' else 1);c,sn=math.cos(t),math.sin(t)
                position=position+Vector((c*d.x-sn*d.y,sn*d.x+c*d.y,0));poses[end].append((f,position.copy()))
        for key,values in poses.items():keys(ctl[side+key],'location',values)
        for f,t in [(1,0),(22,-.035),(47,.05),(72,.025),(104,-.02),(133,.045),(158,.012),(192,.012)]:
            d=rest['head']-rest['neck'];c,sn=math.cos(t),math.sin(t)
            control_key(a,'head',f,rest['neck']+Vector((c*d.x-sn*d.y,sn*d.x+c*d.y,0)))
        # Slight shoulder response without translating planted feet.
        for side2 in ('L','R'):
            keys(ctl[side2+'shoulder'],'location',[(1,rest[side2+'shoulder']),(35,rest[side2+'shoulder']+Vector((0,.06,0))),(69,rest[side2+'shoulder']),(123,rest[side2+'shoulder']+Vector((0,.025,0))),(161,rest[side2+'shoulder']),(192,rest[side2+'shoulder'])])
        for i in (0,1):
            keys(fac['eye'+str(i)],'scale',[(1,(1,1,1)),(27,(1,1,1)),(29,(1,.06,1)),(32,(1,1,1)),(96,(1,1,1)),(99,(1,.04,1)),(103,(1,1,1)),(173,(1,1,1)),(176,(1,.06,1)),(179,(1,1,1)),(192,(1,1,1))])
            keys(fac['gaze'+str(i)],'location',[(1,(.008,0,.014)),(46,(.019,.003,.014)),(69,(-.005,.004,.014)),(119,(-.012,0,.014)),(147,(.008,0,.014)),(192,(.008,0,.014))])
            sign=-1 if i==0 else 1
            keys(fac['brow'+str(i)],'rotation_euler',[(1,(0,0,sign*.1)),(42,(0,0,sign*-.22)),(69,(0,0,sign*-.1)),(123,(0,0,sign*(.16 if name=='Bruno' else -.26))),(156,(0,0,sign*.06)),(192,(0,0,sign*.06))])
        mouth=fac['mouth']
        for prop,values in [('open',[(1,.03),(33,.04),(46,.55),(68,.12),(95,.03),(123,.2),(151,.08),(192,.08)]),('smile',[(1,0),(43,-.5),(69,-.2),(108,0),(133,1 if name=='Bruno' else -.55),(158,.65 if name=='Bruno' else -.3),(192,.65 if name=='Bruno' else -.3)])]:
            for f,value in values:mouth[prop]=value;mouth.keyframe_insert(data_path=f'["{prop}"]',frame=f)
    # Referee stays deliberately just offscreen; his card and hand enter the reaction shot.
    ref=empty('A / referee card gesture',(2.0,.0,0));ref.rotation_euler=(math.pi/2,0,.35)
    poly('A / referee forearm',[(-.13,-2),(.18,-2),(.12,.57),(-.20,1.3),(-.22,1.46),(-.26,1.51),(-.30,1.50),(-.32,1.46),(-.35,1.48),(-.39,1.45),(-.4,1.37),(-.39,1.25),(-.08,.56)],.065,'#eab68a',ref)
    poly('A / referee sleeve',[(-.15,-2),(.20,-2),(.15,-.65),(-.13,-.65)],.07,'#e6ec4b',ref)
    rect('A / red card',-.42,1.44,.27,.43,.045,'#ed3547',ref)
    line('A / referee thumb',[(-.25,1.30),(-.23,1.40),(-.31,1.46)],.08,'#c99065',.012,ref)
    for ob in col.objects:
        if ob.parent==ref and ob.type=='CURVE' and 'outline' in ob.name:ob.data.bevel_depth=.007
    keys(ref,'location',[(1,(6,-4,0)),(44,(6,-4,0)),(65,(2.55,-4,0)),(74,(2.55,-4,-.04)),(95,(2.55,-4,-.04)),(113,(6,-4,0)),(192,(6,-4,0))])
    # Camera cut from full-body scene to Bruno's reaction; depth comes from the native set.
    wide=cam.location.copy();wide_rot=cam.rotation_euler.copy();close=Vector((-.1,-3.2,1.95));target=Vector((-1.0,0,1.55));close_rot=(target-close).to_track_quat('-Z','Y').to_euler()
    for f,loc,rot in [(1,wide,wide_rot),(96,wide,wide_rot),(97,close,close_rot),(192,close,close_rot)]:cam.location=loc;cam.rotation_euler=rot;cam.keyframe_insert(data_path='location',frame=f);cam.keyframe_insert(data_path='rotation_euler',frame=f)
    for layer in cam.animation_data.action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    for k in fc.keyframe_points:k.interpolation='CONSTANT'
    for name,frame in [('S02/complaint',44),('S02/red_card',65),('S02/confidence_close',97),('S02/confidence',133)]:s.timeline_markers.new(name,frame=frame)
    s.frame_set(69);bpy.context.view_layer.update()

def verify():
    # One runnable integration check: controls must actually deform the selected artwork.
    s.frame_set(1);bpy.context.view_layer.update();a=actors['Bruno'];control=a['controls']['Lwrist'];old=control.location.copy()
    def evaluated():return [v.co.copy() for v in a['skin'].evaluated_get(bpy.context.evaluated_depsgraph_get()).data.vertices]
    before=evaluated();control.location.x-=.12;bpy.context.view_layer.update();after=evaluated();control.location=old;bpy.context.view_layer.update()
    displacement=max((v-w).length for v,w in zip(before,after));assert displacement>.01,displacement
    for actor_data in actors.values():
        assert len(actor_data['skin'].vertex_groups)==14
        for key in ('Lankle','Rankle'):
            locations=[]
            for frame in (1,44,69,97,133,192):s.frame_set(frame);locations.append(actor_data['controls'][key].location.copy())
            assert max((v-locations[0]).length for v in locations)<1e-6
    assert s['Goal depth']>0 and s['Goal width']>s['Goal height']
    return {'wrist_control_deformed_artwork':displacement,'planted_ankle_targets':'passed','artwork':'continuous textured mesh on stick-joint targets; native facial features','limits':['Full turns and extreme bends not demonstrated','S02 reaction only; kick-out and parry still need staging','Silent facial acting; final speech and sound not auditioned']}

def save():
    checks=verify();s.frame_set(69);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'option-a-reaction-v002.blend'))
    (OUT/'native-checks.json').write_text(json.dumps(checks,indent=2)+'\n');return checks

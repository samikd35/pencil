"""Pose-matched native vector reconstruction; run stages in visible Blender.

Source-fitted parts own continuous surfaces; occluding props and limbs have
separate anatomical transforms and complete hidden coverage. The existing ten-second acting schedule remains the input.
Source artwork is converted to colored geometry, never a textured head plane.
"""
import bpy, bmesh, json, math, sys, numpy as np
from pathlib import Path
from mathutils import Vector

V=Path(__file__).resolve().parents[1]
O=V/'artifacts/staging-v001/call-performance-v004'
p=V/'scripts/build_call_performance_v002.py'
B={'__file__':str(p)}
exec(compile(p.read_text().replace('v002','v004').replace('C3V2','C3V4'),str(p),'exec'),B)
b=B['b']; interp=B['interp']; two_bone_joint=B['two_bone_joint']
from pipeline.pose_geometry import transported_pole
A={}; PREFIX='C3V4 / '

def setup():
    global s,col
    B['setup']();s=B['s'];col=B['col'];B['room']()
    s['construction']='Reference-traced native colored meshes, fitted armatures and separately controlled native facial drawings. Not Grease Pencil or raster planes.'
    return {'scene':s.name,'stage':'room prepared; source rest construction next'}

def inside(p,poly):
    x,y=p;yes=False
    for a,z in zip(poly,poly[1:]+poly[:1]):
        if (a[1]>y)!=(z[1]>y) and x<(z[0]-a[0])*(y-a[1])/(z[1]-a[1])+a[0]:yes=not yes
    return yes

def ease(x):
    x=max(0,min(1,x));return x*x*(3-2*x)

def xy(p,origin):return Vector((p[0]-origin[0],origin[1]-p[1],0))

def vectors(name,rows,parent,origin,z=0):
    made=[]
    for i,row in enumerate(rows):
        data=bpy.data.curves.new(PREFIX+name+f' contour {i:03}','CURVE');data.dimensions='2D';data.fill_mode='BOTH';data.resolution_u=1
        for path in row['paths']:
            sp=data.splines.new('POLY');sp.points.add(len(path)-1);sp.use_cyclic_u=True
            for point,source in zip(sp.points,path):point.co=(*xy(source,origin),1)
        data.materials.append(b['mat'](row['color']))
        ob=bpy.data.objects.new(data.name,data);col.objects.link(ob);ob.parent=parent;ob.location.z=z+i*.001;made.append(ob)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in made:ob.select_set(True)
    bpy.context.view_layer.objects.active=made[0];bpy.ops.object.convert(target='MESH');bpy.ops.object.join()
    ob=bpy.context.object;ob.name=PREFIX+name;ob.data.name=ob.name
    return ob


def region_weights(p,a,region):
    c=a['c'];pt=Vector(p)
    if region.startswith('fore'):return {region[-1]+' fore':1.}
    if region.startswith('upper'):return {region[-1]+' upper':1.}
    if region=='prop':return {'L hand':1.}
    if region.startswith('hand'):return {region[-1]+' hand':1.}
    if region=='body':
        h=ease((c['collar_y']-p[1])/(c['collar_y']-c['jaw_y']))
        return {'head':h,'torso':1-h}
    side=region[-1];sh,el,wr=[Vector(q) for q in c[side]]
    def distance(a,b):
        d=b-a;t=max(0,min(1,(pt-a).dot(d)/d.length_squared));return (pt-a-d*t).length
    du,df=distance(sh,el),distance(el,wr)
    upper=math.exp(-min(700,du*du/3000));fore=math.exp(-min(700,df*df/3000));total=upper+fore
    u=upper/total;t=(pt-el).dot(wr-el)/(wr-el).length_squared;h=ease((t-.76)/.42)
    torso=(1-ease((pt-sh).length/70))*.7
    return {'torso':torso,side+' upper':(1-torso)*u,side+' fore':(1-torso)*(1-u)*(1-h),side+' hand':(1-torso)*(1-u)*h}

def bind(ob,actor,region='body'):
    # Stroke bevel makes a tube in Z. In a flat drawing that tube can pierce the
    # foreground hand even when its centre is behind it. Keep ink planar.
    if ob.name.endswith(' edge'):
        depth=sum(v.co.z for v in ob.data.vertices)/len(ob.data.vertices)
        for v in ob.data.vertices:v.co.z=depth
    # Interior triangles need samples too; large triangles can cross moving joins.
    bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.triangulate(bm,faces=list(bm.faces))
    for _ in range(3):
        edges=[e for e in bm.edges if e.calc_length()>50]
        if not edges:break
        bmesh.ops.subdivide_edges(bm,edges=edges,cuts=1,use_grid_fill=True)
    bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
    groups={key:ob.vertex_groups.new(name=key) for key in actor['bones']};c=actor['c']
    for v in ob.data.vertices:
        p=(v.co.x+c['origin'][0],c['origin'][1]-v.co.y)
        for key,value in region_weights(p,actor,region).items():groups[key].add([v.index],value,'REPLACE')
    mod=ob.modifiers.new('One source-fitted deformation for all color contours','ARMATURE');mod.object=actor['rig'];mod.use_deform_preserve_volume=True
    ob['binding_region']=region;actor['surfaces'].append(ob)




def actor(who):
    data=json.loads((V/'assets/reference-redraw-v003'/f'{who.lower()}-contours.json').read_text());c=data['design'];c['who']=who
    root=B['control'](who+' root',c['location']);root.scale=(c['scale'],)*3
    controls={};rest={}
    points={'hip':c['hip'],'neck':c['neck']}
    points['head']=[c['neck'][0],c['neck'][1]-220]
    for side in ['L','R']:
        for label,p in zip(['shoulder','elbow','wrist'],c[side]):points[side+' '+label]=p
        points[side+' finger']=[c[side][2][0],c[side][2][1]-75]
    for name,p in points.items():
        rest[name]=xy(p,c['origin']);controls[name]=B['control'](who+' '+name,rest[name],root)
    bones={'torso':('hip','neck'),'head':('neck','head')}
    for side in ['L','R']:bones.update({side+' upper':(side+' shoulder',side+' elbow'),side+' fore':(side+' elbow',side+' wrist'),side+' hand':(side+' wrist',side+' finger')})
    ad=bpy.data.armatures.new(PREFIX+who+' fitted drawing rig');rig=bpy.data.objects.new(ad.name,ad);col.objects.link(rig);rig.parent=root;rig.show_in_front=True
    bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='EDIT')
    for name,(a,z) in bones.items():eb=ad.edit_bones.new(name);eb.head=rest[a];eb.tail=rest[z]
    bpy.ops.object.mode_set(mode='OBJECT')
    for name,(a,z) in bones.items():
        pb=rig.pose.bones[name];co=pb.constraints.new('COPY_LOCATION');co.target=controls[a]
        co=pb.constraints.new('STRETCH_TO');co.target=controls[z];co.rest_length=(rest[z]-rest[a]).length;co.volume='NO_VOLUME';co.bulge=0
    a={'c':c,'root':root,'rest':rest,'controls':controls,'bones':bones,'rig':rig,'surfaces':[],'data':data};A[who]=a
    # Complete the garment hidden by the raised prop/forearms. This native
    # underdrawing is part of the character, not background stretched into a hole.
    if who=='Muller':
        coverage=[(341,439),(405,430),(553,438),(650,488),(681,595),(661,809),(644,960),(451,976),(275,950),(285,793),(283,605),(299,498)]
        color='#db282c'
    else:
        coverage=[(918,486),(1047,445),(1179,444),(1350,486),(1391,648),(1413,931),(1138,936),(944,919),(940,720),(899,552)]
        color='#292e3d'
    backing=B['shape'](who+' hidden garment coverage',[tuple(xy(q,c['origin'])[:2]) for q in coverage],-1,color,root,False,True);bind(backing,a,'body')
    if who=='Muller':
        # The reference's photo hid this fabric. A full scarf exists beneath it,
        # with the visible reference details retained on top.
        for label,pts,color in [
          ('scarf underdrawing',[(342,446),(381,418),(396,493),(391,817),(279,817),(307,648)],'#d32221'),
          ('hidden scarf upper stripe',[(342,452),(390,455),(394,513),(330,515)],'#fef3ec'),
          ('hidden scarf middle stripe',[(312,611),(394,610),(393,691),(303,692)],'#fef3ec')]:
            ob=B['shape'](who+' '+label,[tuple(xy(q,c['origin'])[:2]) for q in pts],-.15,color,root,False,False);bind(ob,a,'body')
    # The backing outline follows the same torso. Source artwork covers its joins.
    edge=bpy.data.objects.get(PREFIX+who+' hidden garment coverage edge')
    if edge:
        bpy.ops.object.select_all(action='DESELECT');edge.select_set(True);bpy.context.view_layer.objects.active=edge;bpy.ops.object.convert(target='MESH');bind(bpy.context.object,a,'body')
    ob=vectors(who+' coherent head neck and torso',data['parts']['body'],root,c['origin']);bind(ob,a,'body')
    for side in ['L','R']:
        region='hand'+side
        if region in data['parts']:
            hand=vectors(who+' '+side+' source grip',data['parts'][region],root,c['origin'],132 if who=='Perez' and side=='R' else 4);bind(hand,a,region)
    articulated_sleeves(a)
    carried_prop(a)
    facial(a)
    s.frame_set(1);bpy.context.view_layer.update()
    return {'actor':who,'source_vertices':sum(len(o.data.vertices) for o in a['surfaces']),'native_surfaces':len(a['surfaces'])}

def facial(a):
    c=a['c'];who=c['who'];origin=c['neck'];face=B['control'](who+' face',a['rest']['neck'],a['root']);a['face']=face
    a['eyes']=[];a['brows']=[];a['mouths']={}
    def shape(label,points,color,z=2,parent=face,ref=origin,outline=False):
        return B['shape'](who+' '+label,[tuple(xy(p,ref)[:2]) for p in points],z,color,parent,outline,False)
    # Backing shares the head's transform and fills only removed feature apertures.
    for label,pts in [('mouth',c['mouth'])]+[(f'brow{i}',p) for i,p in enumerate(c['brows'])]+[(f'eye{i}',e['outline']) for i,e in enumerate(c['eyes'])]:shape(label+' skin backing',pts,c['skin'],-.02)
    for i,e in enumerate(c['eyes']):
        center=e['center'];eye=B['control'](who+f' eye {i}',xy(center,origin)+Vector((0,0,2)),face)
        shape('sclera',e['outline'],'#fff9ed',0,eye,center,True)
        gaze=B['control'](who+f' gaze {i}',xy(e['pupil'],center)+Vector((0,0,.4)),eye)
        rx,ry=e['size'];B['oval'](who+' iris',0,0,rx,ry,0,'#342a21',gaze)
        B['oval'](who+' pupil',0,0,rx*.82,ry*.9,.1,'#10151b',gaze)
        B['oval'](who+' eye glint',-rx*.3,ry*.35,2.5,2.5,.2,'#fffaf2',gaze)
        # A real lid advances over the white; the complete eye does not squash.
        pts=[tuple(xy(p,center)[:2]) for p in e['outline']];top=max(y for x,y in pts)+3;bottom=min(y for x,y in pts)-2
        left=min(x for x,y in pts)-1;right=max(x for x,y in pts)+1
        lid_points=[(x*1.15,y*1.15) for x,y in pts]
        lid=B['shape'](who+' eyelid',[(x,top) for x,y in lid_points],2,c['skin'],eye,False,False)
        lid.shape_key_add(name='Open');closed=lid.shape_key_add(name='Closed')
        for point,(x,y) in zip(closed.data,lid_points):point.co.y=y
        line=B['stroke'](who+' lid crease',[(left,0),(0,-2),(right,0)],2.2,'#553821',1,eye)
        line.hide_render=line.hide_viewport=True
        a['eyes'].append((gaze,closed,line,top,bottom))
    for i,p in enumerate(c['brows']):
        origin2=[sum(x for x,y in p)/len(p),sum(y for x,y in p)/len(p)]
        ctrl=B['control'](who+f' brow {i}',xy(origin2,origin)+Vector((0,0,2)),face)
        vectors(who+f' expressive brow {i}',a['data']['parts']['brow'+str(i)],ctrl,origin2)
        a['brows'].append(ctrl)
    center=c['mouth_center'];w=c['mouth_width'];mouth=B['control'](who+' mouth',xy(center,origin)+Vector((0,0,3)),face)
    for label in ['rest','smile','tight','A','E','O','FV']:
        group=B['control'](who+' mouth '+label,(0,0,0),mouth);a['mouths'][label]=group
        if label=='rest' or label=='smile':vectors(who+' '+label+' mouth',a['data']['parts']['rest_mouth'],group,center)
        elif label=='tight':B['stroke'](who+' tight lip',[(-w*.75,0),(-w*.15,1),(w*.7,-2)],0,'#4d3024',1.6,group)
        else:
            width=w*({'O':.45,'FV':.83}.get(label,1));height={'A':23,'E':13,'O':21,'FV':6}[label]
            B['shape'](who+' '+label+' mouth opening',[(-width,1),(-width*.55,5),(0,4),(width*.7,2),(width,-1),(width*.65,-height*.8),(0,-height),(-width*.7,-height*.72)],0,'#512c28',group,True,True)
            if label!='O':B['shape'](who+' '+label+' teeth',[(-width*.86,1),(-width*.4,2),(width*.75,1),(width*.72,-5),(-width*.73,-5)],.4,'#fff5df',group,False,True)
            if label=='A':B['oval'](who+' tongue',0,-height*.76,width*.43,4,.5,'#c7746a',group)

def rot(v,degrees):
    t=math.radians(degrees);return Vector((v.x*math.cos(t)-v.y*math.sin(t),v.x*math.sin(t)+v.y*math.cos(t),v.z))

def pose(a,f):
    c=a['c'];who=c['who'];p=who=='Perez';r=a['rest'];ctrl=a['controls'];hip=r['hip']
    angle=interp(f,[(1,0),(24,0),(48,-1),(84,0),(145,0),(173,1.8),(205,2.7)]) if not p else interp(f,[(1,0),(105,0),(116,-2.3),(148,-3.8),(198,-3.8),(219,-2.5)])
    hangle=interp(f,[(1,0),(21,0),(35,-4),(49,0),(75,-2),(103,0),(150,0),(156,3),(174,4.5),(197,6)]) if not p else interp(f,[(1,0),(101,0),(117,3),(127,0),(151,1),(185,1),(209,-2)])
    def torso(v):return hip+rot(v-hip,angle)
    ctrl['hip'].location=hip;neck=torso(r['neck']);ctrl['neck'].location=neck;ctrl['head'].location=neck+rot(Vector((0,220,0)),angle+hangle)
    a['face'].location=neck;a['face'].rotation_euler.z=math.radians(angle+hangle)
    for prop in ['location','rotation_euler']:a['face'].keyframe_insert(data_path=prop,frame=f)
    for side in ['L','R']:
        sh=torso(r[side+' shoulder']);wr=r[side+' wrist'].copy();el=r[side+' elbow']
        if side=='L':
            if not p:
                delta=interp(f,[(1,(0,0)),(23,(0,0)),(41,(-8,11)),(90,(-2,4)),(163,(-2,4)),(192,(2,-34)),(214,(18,-58))]);hand=interp(f,[(1,0),(41,-5),(163,-5),(207,8)])
            else:
                delta=interp(f,[(1,(0,0)),(109,(0,0)),(137,(-32,5)),(175,(-30,10)),(198,(-10,-6)),(220,(0,0))]);hand=interp(f,[(1,0),(110,0),(140,-26),(181,-26),(220,0)])
            wr+=Vector((delta[0]*2.1,delta[1]*2.1,0))
        else:
            wr=r[side+' wrist'].copy() if p else torso(r[side+' wrist']);hand=0 if p else angle
        lengths=((r[side+' elbow']-r[side+' shoulder']).length,(r[side+' wrist']-r[side+' elbow']).length)
        pole=transported_pole(tuple(r[side+' shoulder'][:2]),tuple(r[side+' wrist'][:2]),tuple(el[:2]),tuple(sh[:2]),tuple(wr[:2]))
        elbow=two_bone_joint(tuple(sh[:2]),tuple(wr[:2]),lengths,pole)
        if side=='L':
            # Authored prop tilt must respect the whole arm's attainable pose.
            # The grip stays attached; the prop tilts with it, not independently.
            fore=wr-Vector((*elbow,0));fore_angle=math.degrees(math.atan2(fore.y,fore.x))
            wrist_delta=(90+hand-fore_angle+180)%360-180
            hand=fore_angle+max(-42,min(42,wrist_delta))-90
        for name,point in [('shoulder',sh),('elbow',Vector((*elbow,0))),('wrist',wr),('finger',wr+rot(Vector((0,75,0)),hand))]:ctrl[side+' '+name].location=point
    for ob in ctrl.values():ob.keyframe_insert(data_path='location',frame=f)
    gaze=interp(f,[(1,0),(145,0),(152,-9),(174,-9),(203,-13)]) if not p else interp(f,[(1,0),(116,-2),(194,-2),(214,2)])
    close=interp(f,[(1,0),(100,0),(102,1),(105,0),(240,0)]) if not p else interp(f,[(1,0),(72,0),(74,1),(77,0),(240,0)])
    for i,(ctrl,closed,line,top,bottom) in enumerate(a['eyes']):
        ctrl.location.x=c['eyes'][i]['pupil'][0]-c['eyes'][i]['center'][0]+gaze;ctrl.keyframe_insert(data_path='location',frame=f)
        closed.value=close;closed.keyframe_insert(data_path='value',frame=f)
        line.hide_render=line.hide_viewport=close<.9
        for prop in ['hide_render','hide_viewport']:line.keyframe_insert(data_path=prop,frame=f)
        br=a['brows'][i];br.rotation_euler.z=math.radians(interp(f,[(1,0),(143,0),(160,15 if i==0 else -19),(240,15 if i==0 else -19)]) if not p else interp(f,[(1,0),(112,0),(150,5 if i==0 else -5),(240,5 if i==0 else -5)]));br.keyframe_insert(data_path='rotation_euler',frame=f)

def animate():
    phrases={'Muller':[(1,'smile'),(26,'E'),(31,'A'),(35,'rest'),(38,'O'),(49,'rest'),(61,'A'),(65,'FV'),(70,'E'),(77,'O'),(83,'A'),(89,'E'),(95,'smile'),(156,'tight')],
             'Perez':[(1,'rest'),(114,'O'),(122,'rest'),(132,'A'),(139,'O'),(145,'E'),(151,'O'),(156,'FV'),(161,'E'),(166,'O'),(174,'E'),(180,'A'),(186,'O'),(193,'A'),(196,'rest')]}
    for f in range(1,241):
        s.frame_set(f)
        for a in A.values():pose(a,f)
    for a in A.values():wrist_connection(a)
    for who,rows in phrases.items():
        for f,label in rows:
            for name,group in A[who]['mouths'].items():
                for ob in group.children_recursive:
                    ob.hide_render=ob.hide_viewport=name!=label
                    for prop in ['hide_render','hide_viewport']:ob.keyframe_insert(data_path=prop,frame=f)
    for start,end,words in [(25,96,'MÜLLER: Eight goals. A very good night.'),(113,198,'PÉREZ: Good. How do we stop Flick doing that to us?')]:
        ob=B['text']('subtitle',words,0,-334,181,22,'#f5efdf')
        for frame,visible in [(1,False),(start,True),(end,False)]:
            ob.hide_render=ob.hide_viewport=not visible
            for prop in ['hide_render','hide_viewport']:ob.keyframe_insert(data_path=prop,frame=frame)
    for action in bpy.data.actions:
        if not action.name.startswith(PREFIX):continue
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for fc in bag.fcurves:
                        for k in fc.keyframe_points:k.interpolation='CONSTANT' if 'hide_' in fc.data_path else 'LINEAR'
    # Bezel sits in front of all of the caller's artwork, including lowered prop.
    B['rect']('call desk',-581,-197,656,23,25,'#9b704b',outline=False)
    B['rect']('monitor lower bevel',-594,-219,682,22,27,'#263448',outline=False)
    B['text']('call name','THOMAS MÜLLER · BAYERN LEGEND',-268,-207,29,12,'#d2dce5')
    s.frame_set(48)
    return {'frames':240,'retained_events':'boast 25; question 113; gaze arrest 145–152; smile drops 156; picture lowers 163–214'}


def articulated_sleeves(a):
    """Separate actual occluding surfaces; preserve complete hidden arm volumes.

    Upper arm is behind the torso and forearm. Each forearm drawing is rigid on
    its bone; the wrist grip and prop have their own shared transform. Large
    changes of view still require a matching corrective drawing.
    """
    who=a['c']['who'];c=a['c'];root=a['root'];a['sleeves']=[]
    color='#dd292c' if who=='Muller' else '#292e3d'
    for side in ['L','R']:
        if 'fore'+side not in a['data']['parts']:continue
        sh,el,wr=[xy(q,c['origin']) for q in c[side]]
        u=(el-sh).normalized();n=Vector((-u.y,u.x,0))
        w0,w1=(56,51) if who=='Muller' else (62,58)
        # Complete rounded upper-arm volume overlaps under the foreground elbow.
        pts=[]
        for center,radius,start in [(el,w1,0),(sh,w0,math.pi)]:
            for j in range(17):
                theta=start+math.pi*j/16
                v=center+n*math.cos(theta)*radius+u*math.sin(theta)*radius
                pts.append(tuple(v[:2]))
        upper=B['shape'](who+' '+side+' fitted sleeve fill',pts,-.5,color,root,True,False)
        bind(upper,a,'upper'+side);a['sleeves'].append(upper)
        edge=bpy.data.objects.get(PREFIX+who+' '+side+' fitted sleeve fill edge')
        if edge:
            bpy.ops.object.select_all(action='DESELECT');edge.select_set(True);bpy.context.view_layer.objects.active=edge;bpy.ops.object.convert(target='MESH');bind(bpy.context.object,a,'upper'+side)
        depth=130 if who=='Perez' and side=='R' else 2
        fore=vectors(who+' '+side+' source forearm',a['data']['parts']['fore'+side],root,c['origin'],depth)
        bind(fore,a,'fore'+side);a['sleeves'].append(fore)


def wrist_connection(a):
    """Open skin connection between registered hand and cuff edges.

    Both ends follow their actual evaluated bones. There is no closed wrist cap
    to rotate away from the cuff, and no paper/cuff pixels in the moving hand.
    """
    c=a['c'];join=c['wrist_join'];layers={}
    for f in range(1,241):
        s.frame_set(f);bpy.context.view_layer.update()
        def mapped(points,bone):
            pb=a['rig'].pose.bones[bone];m=pb.matrix@pb.bone.matrix_local.inverted()
            return [m@xy(p,c['origin']) for p in points]
        h=mapped(join['hand_edge'],'L hand');w=mapped(join['sleeve_edge'],'L fore')
        contour=[tuple(p[:2]) for p in [h[0],w[0],w[1],h[1]]]
        color,shade=('#fab470','#dd975c') if c['who']=='Muller' else ('#f9b06b','#dfa064')
        shadow=[tuple(p[:2]) for p in [h[0].lerp(h[1],.75),w[0].lerp(w[1],.8),w[1],h[1]]]
        # Extend side ink under the hand by three source pixels so the traced
        # antialiased edge and the open connection share a continuous silhouette.
        left=h[0]+(h[0]-w[0]).normalized()*3;right=h[1]+(h[1]-w[1]).normalized()*3
        specs={'fill':(contour,color,True),'shadow':(shadow,shade,True),'left':([tuple(left[:2]),contour[1]],'#202332',False),'right':([tuple(right[:2]),contour[2]],'#202332',False)}
        for label,(points,color,filled) in specs.items():
            if f==1:
                name=c['who']+' L wrist connection '+label
                ob=B['shape'](name,points,1.71 if label=='shadow' else 1.7,color,a['root'],False,False) if filled else B['stroke'](name,points,1.72,color,1.65,a['root'],False)
                if not filled:
                    for sp in ob.data.splines:
                        for p in sp.points:p.co.z=0
                    ob.location.z=1.72;ob.scale.z=.001
                layers[label]=ob;ob.shape_key_add(name='Basis');ob.data.shape_keys.use_relative=False
            ob=layers[label];key=ob.shape_key_add(name=f'Pose {f:03}')
            for p,(x,y) in zip(key.data,points):p.co.x=x;p.co.y=y
            key.interpolation='KEY_LINEAR';keys=ob.data.shape_keys;keys.eval_time=key.frame;keys.keyframe_insert(data_path='eval_time',frame=f)
    a['wrist_connection']=layers


def carried_prop(a):
    c=a['c'];root=a['root'];who=c['who'];origin=c['origin']
    def shape(label,pts,z,color,outline=True):
        ob=B['shape'](who+' '+label,[tuple(xy(q,origin)[:2]) for q in pts],z,color,root,outline,False);bind(ob,a,'prop')
        edge=bpy.data.objects.get(PREFIX+who+' '+label+' edge')
        if edge:
            bpy.ops.object.select_all(action='DESELECT');edge.select_set(True);bpy.context.view_layer.objects.active=edge;bpy.ops.object.convert(target='MESH');bind(bpy.context.object,a,'prop')
        return ob
    if who=='Muller':
        shape('carried wooden frame',[(78,344),(311,316),(337,590),(110,624)],3,'#67482f')
        shape('carried frame paper',[(104,366),(292,340),(313,568),(126,597)],3.3,'#fff5df')
        for label,words,x,y,size in [('score','8 – 2',207,455,65),('year','2020',214,519,23)]:
            pt=xy((x,y),origin);ob=B['text'](who+' carried '+label,words,pt.x,pt.y,3.6,size,'#171b24',root)
            ob.rotation_euler.z=math.radians(6)
            bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.convert(target='MESH');bind(bpy.context.object,a,'prop')
    else:
        shape('carried pen body',[(916,401),(923,398),(1057,531),(1058,541),(1049,536)],3,'#263443')
        shape('carried pen glint',[(920,408),(924,406),(970,452),(968,455)],3.3,'#718897',False)
        shape('carried pen nib',[(1051,533),(1058,533),(1065,545)],3.3,'#c8d3d5')

def save():
    # One meaningful check: portable joint lengths, rest registration, facial range,
    # normalized common weights and no raster character material. Visual review separate.
    errors=[];frames=[1,35,48,74,102,137,152,156,175,192,214,240]
    for a in A.values():
        for ob in a['surfaces']:
            assert all(abs(sum(g.weight for g in v.groups)-1)<1e-5 for v in ob.data.vertices)
            assert all(not m.use_nodes or not any(n.type=='TEX_IMAGE' for n in m.node_tree.nodes) for m in ob.data.materials)
    for f in frames:
        s.frame_set(f);bpy.context.view_layer.update()
        for a in A.values():
            for side in ['L','R']:
                c=a['controls'];r=a['rest']
                for u,v in [('shoulder','elbow'),('elbow','wrist')]:errors.append(abs((c[side+' '+u].location-c[side+' '+v].location).length-(r[side+' '+u]-r[side+' '+v]).length))
    assert max(errors)<.001,max(errors)
    result={'tested_frames':frames,'limb_length_max_error_source_pixels':max(errors),'normalized_shared_surface_weights':True,'character_image_textures':False,'construction':'Native vector-derived meshes and source-fitted armatures; independent face drawings','visual_review':'Not supplied by these numerical checks','audio_listened_by_agent':False}
    O.mkdir(parents=True,exist_ok=True);(O/'native-check.json').write_text(json.dumps(result,indent=2)+'\n')
    s.frame_set(48);bpy.ops.wm.save_as_mainfile(filepath=str(O/'call-performance.blend'))
    return result

def build():
    setup()
    for who in ['Muller','Perez']:actor(who)
    animate();return save()

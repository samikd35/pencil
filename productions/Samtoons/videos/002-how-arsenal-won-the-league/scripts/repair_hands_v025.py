"""Visible-Blender repair: one continuous exposed arm, from sleeve to fingertips.

Uses the existing fitted cast, actual evaluated cuff vertices and v017 pointing
silhouette. Does not replace heads, bodies, clothing, audio or scene timing.
"""
import bpy, bmesh, math
from mathutils import Vector
ns = bpy.app.driver_namespace['clarity24']
V, S = ns['V'], ns['S']
OUT = V/'artifacts/hand-repair-v025'
OUT.mkdir(exist_ok=True)
(OUT/'review-frames').mkdir(exist_ok=True)
(OUT/'clips').mkdir(exist_ok=True)
point = [(0,.024),(.025,.032),(.055,.041),(.145,.041),(.154,.038),(.157,.032),(.153,.026),(.144,.024),(.083,.025),(.09,.012),(.089,.001),(.079,-.008),(.075,-.024),(.066,-.033),(.049,-.035),(.024,-.029),(0,-.023)]
relaxed = [(0,.025),(.038,.038),(.070,.037),(.093,.027),(.117,.013),(.123,.004),(.120,-.002),(.112,-.003),(.094,.007),(.104,-.009),(.106,-.018),(.100,-.023),(.091,-.019),(.081,-.005),(.087,-.025),(.083,-.031),(.075,-.030),(.064,-.009),(.062,-.026),(.054,-.03),(.046,-.023),(.042,-.004),(.031,-.018),(.018,-.025),(0,-.024)]
relaxed = [(x*1.25,y*1.10) for x,y in relaxed]
grip = [(0,.026),(.022,.033),(.047,.048),(.069,.049),(.079,.043),(.087,.044),(.096,.038),(.102,.027),(.109,.027),(.116,.019),(.118,.006),(.111,-.005),(.102,-.01),(.090,-.027),(.074,-.036),(.054,-.035),(.029,-.029),(0,-.026)]

def sampled(pp, count=48):
    pp=[Vector(p) for p in pp]; dist=[0.]
    for a,b in zip(pp,pp[1:]): dist.append(dist[-1]+(b-a).length)
    out=[]
    for i in range(count):
        d=dist[-1]*i/(count-1)
        j=next((j for j in range(len(dist)-1) if dist[j+1]>=d),len(dist)-2)
        out.append(pp[j].lerp(pp[j+1],(d-dist[j])/max(1e-8,dist[j+1]-dist[j])))
    return out

def bez(a,b,c,d,n=12):
    return [a*(1-t)**3+3*b*t*(1-t)**2+3*c*t*t*(1-t)+d*t**3 for t in [i/(n-1) for i in range(n)]]

def drawable(a,name,points,color,fill=False,width=.0018):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='2D' if fill else '3D'
    cu.resolution_u=1;cu.fill_mode='BOTH' if fill else 'FULL'
    if not fill: cu.bevel_depth=width;cu.bevel_resolution=2
    sp=cu.splines.new('POLY');sp.points.add(len(points)-1);sp.use_cyclic_u=fill
    cu.materials.append(ns['mat'](color));ob=bpy.data.objects.new(name,cu)
    a['s'].collection.objects.link(ob);ob.parent=a['root']
    return ob

def coords(ob,points,f,z):
    assert len(ob.data.splines[0].points)==len(points)
    if ob.data.dimensions=='2D':ob.location.z=z;z=0.
    for bp,p in zip(ob.data.splines[0].points,points):
        bp.co=(p.x,p.y,z,1);bp.keyframe_insert(data_path='co',frame=f)

def prepare(a,sides):
    tag='H25 '+a['s'].name+' '+a['name']+' '
    # The source is the untouched v023 complete drawing. Never progressively cut
    # already-cut hands, and never include a foot in the arm region.
    if '_h25_mesh' not in a: a['_h25_mesh']=ns['h25sources'][a['name']].data.copy()
    a['skin'].data=a['_h25_mesh'].copy()
    for ob in list(a['s'].objects):
        if ob.name.startswith(tag) or ob.name.startswith('C24 '+a['s'].name+' '+a['name']+' '):
            bpy.data.objects.remove(ob,do_unlink=True)
    me=a['skin'].data;uv=me.uv_layers.active.data
    px={lp.vertex_index:Vector((uv[lp.index].uv.x*1024,(1-uv[lp.index].uv.y)*1536)) for lp in me.loops}
    cut={'Referee':{'L':((600,288),(652,305), (520,670,278,535)), 'R':((852,305),(903,290),(842,980,278,535))},
         'Operator':{'L':((611,1063),(665,1080),(520,677,1050,1310)), 'R':((864,1080),(913,1061),(845,1000,1048,1308))}}[a['name']]
    cuffs={};bm=bmesh.new();bm.from_mesh(me)
    for side in sides:
        p,q,box=cut[side];p,q=Vector(p),Vector(q)
        cuffs[side]=[min(px,key=lambda i:(px[i]-v).length_squared) for v in (p,q)]
        x0,x1,y0,y1=box
        dead=[]
        for face in bm.faces:
            v=sum((px[x.index] for x in face.verts),Vector((0,0)))/len(face.verts)
            boundary=p.y+(v.x-p.x)*(q.y-p.y)/(q.x-p.x)
            inner=q.x+12-max(0,v.y-q.y)*.20 if side=='L' else p.x-15+max(0,v.y-p.y)*.20
            outside_body=v.x<inner if side=='L' else v.x>inner
            if outside_body and x0<v.x<x1 and y0<v.y<y1 and v.y>boundary+1: dead.append(face)
        bmesh.ops.delete(bm,geom=dead,context='FACES_ONLY')
    bm.to_mesh(me);bm.free();a['_h25_cuffs']=cuffs
    return tag

def pose_for(a,sid,f,side):
    p={k:o.location.copy() for k,o in a['C'].items()};mode='relaxed';g=0.
    if a['name']=='Referee':
        if side=='L':
            g=ns['smooth']((f-85)/10) if sid=='VH01' else 1.
            neutral=ns['pose'](a)
            p['Lelbow']=neutral['Lelbow'].lerp(p['Lshoulder']+Vector((-.075,-.16,0)),g)
            end_el=p['Lshoulder']+Vector((-.075,-.16,0));end_wr=p['neck']+Vector((-.135,.025,0))
            v0=neutral['Lwrist']-neutral['Lelbow'];v1=end_wr-end_el
            a0=math.atan2(v0.y,v0.x);a1=math.atan2(v1.y,v1.x)
            turn=a0+((a1-a0+math.pi)%(2*math.pi)-math.pi)*g
            length=v0.length+(v1.length-v0.length)*g
            p['Lwrist']=p['Lelbow']+Vector((math.cos(turn),math.sin(turn),0))*length
            mode='ear'
        else:
            g=ns['pulse'](f,36,47,83) if sid=='VH01' else ns['smooth']((f-198)/10) if sid=='VH05' else 0.
            neutral=ns['pose'](a)
            # A corner signal extends out from the shoulder, not a serving palm.
            p['Relbow']=neutral['Relbow'].lerp(p['Rshoulder']+Vector((.255,-.025,0)),g)
            p['Rwrist']=neutral['Rwrist'].lerp(p['Rshoulder']+Vector((.495,.045,0)),g)
            mode='point'
    else:
        if side=='R':
            mode='phone';g=1.
            p['Relbow']=p['Rshoulder']+Vector((.16,-.20,0))
            p['Rwrist']=p['neck']+Vector((.46,-.085,0))
        elif sid=='VH03':
            mode='ear';g=1.
            p['Lelbow']=p['Lshoulder']+Vector((-.06,-.16,0))
            p['Lwrist']=p['neck']+Vector((-.165,.04,0))
        elif sid=='VH04_button':
            mode='button';g=ns['pulse'](f,1,9,24)
            p['Lelbow']=p['Lshoulder']+Vector((.055,-.205,0))
            p['Lwrist']=Vector((-.43,1.165+.055*(1-g),0))
            g=1. # Finger is already prepared, only the arm presses down.
    sh,el,wr=[p[side+n] for n in ['shoulder','elbow','wrist']]
    angle=math.atan2((wr-el).y,(wr-el).x)
    target={'ear':math.radians(65),'point':math.radians(6),'phone':math.pi/2,'button':math.radians(200)}.get(mode,angle)
    if mode=='ear' and g<1:target=angle+math.radians(7)
    angle+=((target-angle+math.pi)%(2*math.pi)-math.pi)*g
    p[side+'finger']=wr+Vector((math.cos(angle),math.sin(angle),0))*.13
    ns['write_pose'](a,f,p)
    return p,mode,g,angle

def rebuild(sid,name,sides):
    a=ns['actor'](sid,name);ns['use'](a['s']);tag=prepare(a,sides)
    if sid=='VH04_button':
        next(o for o in a['s'].objects if o.name.startswith('F23 play on button')).animation_data_clear()
    color,shade=('#fba363','#e6955b') if name=='Referee' else ('#fdac6d','#e9985d')
    shapes={k:sampled(v) for k,v in [('relaxed',relaxed),('point',point),('ear',point),('button',point),('phone',grip)]}
    for side in sides:
        obs=None;thumb=None
        for f in range(1,a['s'].frame_end+1):
            a['s'].frame_set(f);p,mode,g,angle=pose_for(a,sid,f,side);bpy.context.view_layer.update()
            ev=a['skin'].evaluated_get(bpy.context.evaluated_depsgraph_get())
            cuff=[ev.data.vertices[i].co.xy.copy() for i in a['_h25_cuffs'][side]]
            el,wr=p[side+'elbow'].xy,p[side+'wrist'].xy
            d=(wr-el).normalized();n=Vector((-d.y,d.x));handaxis=Vector((math.cos(angle),math.sin(angle)));hn=Vector((-handaxis.y,handaxis.x))
            hand=[wr+handaxis*v.x+hn*v.y for v in [u.lerp(v,g) for u,v in zip(shapes['relaxed'],shapes[mode])]]
            cu=(cuff[0]+cuff[1])*.5;ud=(el-cu).normalized();un=Vector((-ud.y,ud.x))
            cuff.sort(key=lambda v:v.dot(un),reverse=True)
            upper=bez(cuff[0],cuff[0]+ud*.045,el+un*.056-ud*.025,el+un*.052)+[el+(un*math.cos(t)+ud*math.sin(t))*.052 for t in [i*math.pi/12 for i in range(1,13)]]+bez(el-un*.052,el-un*.056-ud*.025,cuff[1]+ud*.045,cuff[1])[1:]
            outer=bez(el+n*.05,el+n*.06+d*.06,hand[0]-d*.085,hand[0])
            inner=bez(hand[-1],hand[-1]-d*.09,el-n*.052+d*.06,el-n*.05)
            cap=[el+(-n*math.cos(t)-d*math.sin(t))*.05 for t in [i*math.pi/12 for i in range(1,13)]]
            ink=outer+hand[1:]+inner[1:];contour=ink+cap
            armshade=bez(el-n*.046,el-n*.049+d*.065,hand[-1]-d*.10,hand[-1])+bez(hand[-1]+hn*.01,hand[-1]+hn*.01-d*.09,el-n*.025+d*.04,el-n*.027)
            fold=[wr+handaxis*x+hn*y for x,y in [(.027,.023),(.044,.013),(.066,.009),(.072,.002),(.067,-.007),(.056,-.009),(.036,-.002)]]
            crease=[wr+handaxis*x+hn*y for x,y in [(.078,.007),(.07,-.004),(.063,-.014)]]
            if obs is None:
                obs=[drawable(a,tag+side+' continuous forearm hand',contour,color,True),drawable(a,tag+side+' arm contour',ink,'#392b25',False,.0023),drawable(a,tag+side+' volume shade',armshade,shade,True),drawable(a,tag+side+' thumb fold',fold,'#ad6e43',False,.00125),drawable(a,tag+side+' knuckles',crease,'#ad6e43',False,.0011),drawable(a,tag+side+' upperarm',upper,color,True),drawable(a,tag+side+' upper outline',upper,'#392b25',False,.0023),drawable(a,tag+side+' elbow edge',cap,'#392b25',False,.0023)]
            for ob,pp,z in zip(obs,[contour,ink,armshade,fold,crease,upper,upper,cap],[.024,.025,.026,.027,.027,.019,.02,.025]):coords(ob,pp,f,z)
            for bp,pp in zip(obs[-1].data.splines[0].points,cap):
                bp.radius=1. if (pp-el).dot(ud)>0 else 0.;bp.keyframe_insert(data_path='radius',frame=f)
            if mode=='phone':
                phone=next((o for o in a['s'].objects if o.name.startswith('F23 hand phone')),None)
                if phone:
                    ns['key'](phone,'location',f,(wr.x-.025,wr.y+.055,.034));ns['key'](phone,'scale',f,(1.,1.05,1.))
                thumbpoints=[wr+Vector(v) for v in [(.012,.057),(.006,.066),(.008,.08),(.014,.094),(.021,.100),(.028,.097),(.030,.09),(.024,.077),(.023,.064)]]
                if thumb is None:thumb=[drawable(a,tag+side+' thumb around phone',thumbpoints,color,True),drawable(a,tag+side+' thumb edge',thumbpoints,'#392b25',False,.0018)]
                for ob,z in zip(thumb,[.080,.081]):coords(ob,thumbpoints,f,z)
            if mode=='button':
                button=next(o for o in a['s'].objects if o.name.startswith('F23 play on button'))
                # Match the actual fingertip at frame 9, not the wrist control.
                if f==9:
                    tip=wr+handaxis*.154+hn*.032;world=a['root'].matrix_world@Vector((tip.x,tip.y,.024));button.location.x=world.x
                    button.location.z=world.z-.120;button.location.y=world.y-.005
        for ob in obs:
            for fc in ns['curves'](ob.data):
                for k in fc.keyframe_points:k.interpolation='LINEAR'
    return {'scene':sid,'actor':name,'sides':sides,'frames':a['s'].frame_end}

def preview(sid,f):
    s=S[sid];ns['use'](s);s.frame_set(f);s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(OUT/'review-frames'/f'{sid}-{f:04}.png');bpy.ops.render.render(write_still=True)
    return s.render.filepath

assert len(sampled(point))==len(sampled(relaxed))==len(sampled(grip))
assert point[0][0]==point[-1][0]==0 and max(x for x,y in point)<.17

def replace_other_hands():
    """Use the same drawn hand silhouettes at existing, already-fitted cuffs."""
    report=[]
    colors={r['actor']:r['color'] for r in __import__('json').loads((ns['O']/'hand-palette-checks.json').read_text())}
    for a in ns['A'].values():
        roots=[o for o in a['s'].objects if o.type=='EMPTY' and o.name.startswith('C24 '+a['s'].name+' '+a['name']+' ')]
        for root in roots:
            surface=next((o for o in root.children if 'hand surface' in o.name),None)
            if surface is None:continue
            ns['use'](a['s']);cache={}
            for f in range(1,a['s'].frame_end+1):
                a['s'].frame_set(f);bpy.context.view_layer.update();ev=surface.evaluated_get(bpy.context.evaluated_depsgraph_get())
                cache[f]=[v.co.xy.copy() for v in ev.data.vertices[:2]]
            for ob in list(root.children_recursive):bpy.data.objects.remove(ob,do_unlink=True)
            pp=point if 'point' in root.name else grip
            template=[Vector((-y,x)) for x,y in sampled(pp)]
            color=colors.get(a['name'],'#fdb172');obs=None;thumb=None
            for f,ends in cache.items():
                start,end=ends
                left=bez(start,start+Vector((0,.025)),template[0]-Vector((0,.025)),template[0],6)
                right=bez(template[-1],template[-1]-Vector((0,.025)),end+Vector((0,.025)),end,6)
                silhouette=left+template[1:]+right[1:]
                folds=[Vector((-y,x)) for x,y in [(.027,.023),(.044,.013),(.066,.009),(.072,.002),(.067,-.007),(.056,-.009),(.036,-.002)]]
                if obs is None:
                    obs=[drawable(a,'H25 '+root.name+' surface',silhouette,color,True),drawable(a,'H25 '+root.name+' outline',silhouette,'#392b25',False,.0023),drawable(a,'H25 '+root.name+' folds',folds,'#ad6e43',False,.0012)]
                    for ob in obs:ob.parent=root
                for ob,pts,z in zip(obs,[silhouette,silhouette,folds],[.032,.034,.035]):coords(ob,pts,f,z)
                if 'phone' in root.name:
                    thumbpts=[Vector(v) for v in [(.013,.04),(.005,.049),(.007,.066),(.015,.083),(.023,.087),(.030,.082),(.029,.070),(.023,.054),(.023,.044)]]
                    if thumb is None:
                        thumb=[drawable(a,'H25 '+root.name+' thumb',thumbpts,color,True),drawable(a,'H25 '+root.name+' thumb ink',thumbpts,'#392b25',False,.0016)]
                        for ob in thumb:ob.parent=root
                    for ob,z in zip(thumb,[.09,.091]):coords(ob,thumbpts,f,z)
            report.append(root.name)
    return report

def check_contacts():
    """Run in the authoring session after reconstruction; checks visible geometry."""
    from bpy_extras.object_utils import world_to_camera_view
    import json
    a=ns['actor']('VH01','Referee');ns['use'](a['s']);lengths=[]
    for f in range(84,97):
        a['s'].frame_set(f)
        lengths.append((a['C']['Lwrist'].location-a['C']['Lelbow'].location).length)
    assert .27<min(lengths)<=max(lengths)<.33, lengths
    s=S['VH04_button'];ns['use'](s);s.frame_set(9);bpy.context.view_layer.update()
    surface=next(o for o in s.objects if o.name.startswith('H25 ') and 'L continuous forearm' in o.name)
    tip=min((surface.matrix_world@Vector(p.co[:3]) for p in surface.data.splines[0].points),key=lambda p:p.x)
    button=next(o for o in s.objects if o.name.startswith('F23 play on button'))
    top=button.matrix_world@Vector((0,.12,0))
    gap=abs(world_to_camera_view(s,s.camera,tip).y-world_to_camera_view(s,s.camera,top).y)*720
    assert gap<2, gap
    report={'raise_forearm_length_range':[min(lengths),max(lengths)],'button_contact_gap_px_at_720p':gap,'scope':'Geometric checks; visual performance review still required.'}
    (OUT/'hand-checks.json').write_text(json.dumps(report,indent=2))
    return report

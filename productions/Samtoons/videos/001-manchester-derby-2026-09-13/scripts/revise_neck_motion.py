"""Revise the actual S01: continuous neck, registered drawings and smooth acting.
Run apply() then animate_and_save() through the visible Blender instance.
"""
from pathlib import Path
import bpy, json, math, hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OLD=ROOT/'artifacts/staging-v001';OUT=ROOT/'artifacts/staging-v002'
base={'__file__':str(ROOT/'scripts/build_staging.py')}
exec(compile((ROOT/'scripts/build_staging.py').read_text(),base['__file__'],'exec'),base)
s=bpy.context.scene
base.update(s=s,skin=bpy.data.collections['S01 / editable artwork'],ink=bpy.data.materials['#171e27'],font=next(f for f in bpy.data.fonts if f.filepath.endswith('Arial Bold.ttf')),cam=s.camera)
poly,line,empty,mat=[base[k] for k in ('poly','line','empty','mat')]
actors={}; source_hash=hashlib.sha256((OLD/'s01-morning-pep-v002.blend').read_bytes()).hexdigest()
def hide(o):
    o.animation_data_clear();o.hide_render=o.hide_viewport=True

def keys(o,prop,values):
    for frame,value in values:
        setattr(o,prop,value);o.keyframe_insert(data_path=prop,frame=frame)
    if o.animation_data and o.animation_data.action:
        for layer in o.animation_data.action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for fc in bag.fcurves:
                        if fc.data_path==prop:
                            for k in fc.keyframe_points:
                                k.interpolation='BEZIER';k.handle_left_type=k.handle_right_type='AUTO_CLAMPED'

def scalar_keys(o,prop,values):
    for frame,value in values:o[prop]=value;o.keyframe_insert(data_path=f'["{prop}"]',frame=frame)

def face(name,row,col,parent,material):
    # Register each drawing on its unchanged outer skull, not the varying mouth/jaw height.
    W,H=1774,887
    xbase=[0,443,887,1330][col]
    xmin=([44,35,28,22] if row==0 else [63,60,55,52])[col]
    left=xbase+xmin-6;right=left+(353 if row==0 else 346)
    top,bottom=(12,424) if row==0 else (429,846)
    height=1.78 if row==0 else 1.72;width=height*(right-left)/(bottom-top)
    y=-.34
    vs=[(-width/2+.05,y,.65),(width/2+.05,y,.65),(width/2+.05,y+height,.65),(-width/2+.05,y+height,.65)]
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],[(0,1,2,3)]);me.materials.append(material);uv=me.uv_layers.new()
    u0,u1=left/W,right/W;v0,v1=1-bottom/H,1-top/H
    coords=[(u0,v0),(u1,v0),(u1,v1),(u0,v1)]
    if row:coords=[(u1,v0),(u0,v0),(u0,v1),(u1,v1)]
    for i,xy in enumerate(coords):uv.data[i].uv=xy
    ob=bpy.data.objects.new(name,me);base['skin'].objects.link(ob);ob.parent=parent
    return ob

def driver_from_transform(block,path,index,target,axis,space='WORLD_SPACE',expression='v'):
    d=block.driver_add(path,index).driver;v=d.variables.new();v.name='v';v.type='TRANSFORMS';v.targets[0].id=target;v.targets[0].transform_type='LOC_'+axis;v.targets[0].transform_space=space;d.expression=expression

def neck(name,upper,head,color):
    # Both ends are real shared anchors. The middle follows their interpolated positions.
    # Open side contours avoid drawing a second jaw/base line through the attachment.
    anchors={}
    for side,xx in [('L',-.28),('R',.24)]:
        anchors[side+'top']=empty(name+' / neck '+side+' skull attachment',(xx,.17,0),head)
        anchors[side+'base']=empty(name+' / neck '+side+' collar attachment',(xx*1.05,1.54,0),upper)
    vals=[('L',0),('L',.33),('L',.67),('L',1),('R',1),('R',.67),('R',.33),('R',0)]
    ob=poly(name+' / deforming neck',[(0,0)]*8,.48,color,outline=False)
    def point_driver(block,path,index,side,t,axis):
        d=block.driver_add(path,index).driver
        for var,target in [('b',anchors[side+'base']),('h',anchors[side+'top'])]:
            v=d.variables.new();v.name=var;v.type='TRANSFORMS';v.targets[0].id=target;v.targets[0].transform_type='LOC_'+axis;v.targets[0].transform_space='WORLD_SPACE'
        # Slight outward curve at the throat base, suppressed where buried under the jaw.
        bow=( -.020 if side=='L' else .018)*math.sin(math.pi*t)
        d.expression=f'b*(1-{t})+h*{t}'+(f'+({bow})' if axis=='X' else '')
    for i,(side,t) in enumerate(vals):
        for axis,letter in enumerate('XY'):point_driver(ob.data,f'vertices[{i}].co',axis,side,t,letter)
    for side in ('L','R'):
        edge=line(name+' / neck '+side+' outline',[(0,0)]*4,.50,'#171e27',.015)
        for i,t in enumerate((0,.33,.67,1)):
            for axis,letter in enumerate('XY'):point_driver(edge.data,f'splines[0].points[{i}].co',axis,side,t,letter)
    # A restrained shadow under the skull, fully attached to the same head control.
    poly(name+' / neck jaw shadow',[(-.27,.13),(.22,.13),(.20,-.05),(-.25,-.10)],.59,'#d69a70' if name=='Haaland' else '#be8368',head,False)
    return anchors,ob

def apply():
    assert bpy.data.filepath.endswith('staging-v001/s01-morning-pep-v002.blend')
    im=bpy.data.images.load(str(ROOT/'assets/art-v002/head-expressions.png'));im.pack()
    hm=bpy.data.materials['Original illustrated facial replacements'].copy();hm.name='Registered facial drawings v002'
    next(n for n in hm.node_tree.nodes if n.type=='TEX_IMAGE').image=im
    for name,row,color,kit in [('Haaland',0,'#f2b385','#8fcee4'),('Maresca',1,'#dca07a','#293747')]:
        root=bpy.data.objects[name+' / ROOT'];head=bpy.data.objects[name+' / HEAD'];head.animation_data_clear()
        for old in list(head.children):hide(old)
        hide(bpy.data.objects[name+' / Neck']);hide(bpy.data.objects[name+' / Collar'])
        upper=empty(name+' / Upper body acting',(0,0,0),root)
        # One acting control carries connected shoulder/head/arm art; lower legs stay planted.
        excluded=('Ground shadow','hip ','knee ','foot ','leg ','Pale blue sock')
        for ob in list(root.children):
            if ob==upper or any(q in ob.name for q in excluded):continue
            ob.parent=upper
        head.parent=upper;head.location=(-.05,1.96,0);head.rotation_euler=(0,0,0)
        drawings=[face(name+f' / registered drawing {i}',row,i,head,hm) for i in range(4)]
        a={'root':root,'upper':upper,'head':head,'drawings':drawings}
        a['neck_anchors'],a['neck']=neck(name,upper,head,color)
        # Rounded neckline crosses in front of the neck; no black horizontal cap remains.
        collar=[(-.32,1.65),(-.26,1.55),(-.13,1.47),(0,1.45),(.14,1.48),(.27,1.57),(.32,1.65)]
        line(name+' / natural collar',collar,.73,'#e1f1ee' if row==0 else '#14202b',.036,upper)
        # Hands are retained but the manager now has thumbs visibly wrapped over the prop.
        for side in (-1,1):
            a[f'hand{side}']=bpy.data.objects[name+f' / HAND {side}'];a[f'elbow{side}']=bpy.data.objects[name+f' / elbow {side}']
        actors[name]=a
    badge=bpy.data.objects['Maresca / ENZO badge control'];badge.animation_data_clear();badge.parent=actors['Maresca']['upper'];badge.location=(0,-.12,.8)
    actors['Maresca']['badge']=badge
    for side in (-1,1):
        hand=actors['Maresca'][f'hand{side}'];hand.animation_data_clear()
        # Same animated badge transform drives the actual wrist contact; never independent tracks.
        target=empty('Maresca / badge grip '+str(side),(side*.80,.025,-.8),badge)
        for axis,letter in enumerate('XY'):
            d=hand.driver_add('location',axis).driver
            for var,tt in [('c','LOC_Y'),('r','ROT_Z')]:
                v=d.variables.new();v.name=var;v.type='TRANSFORMS';v.targets[0].id=badge;v.targets[0].transform_type=tt;v.targets[0].transform_space='LOCAL_SPACE'
            d.expression=f'{side*.80}*cos(r)-.025*sin(r)' if axis==0 else f'c+{side*.80}*sin(r)+.025*cos(r)'
        thumb=[(-side*.055+.095*math.cos(i*math.tau/24),.005+.049*math.sin(i*math.tau/24)) for i in range(24)]
        poly('Maresca / rounded gripping thumb',thumb,.94,'#dca07a',hand)
    hide(bpy.data.objects['Badge / cord'])
    # Preserve selected B and its source timing; audio is not regenerated.
    for strip in s.sequence_editor.strips:strip.mute=not strip.name.startswith('B ')
    s['Revision']='Natural continuous neck and connected smooth acting; selected sound B.'
    for ar in bpy.context.screen.areas:
        if ar.type=='VIEW_3D':ar.spaces.active.region_3d.view_perspective='CAMERA';ar.spaces.active.shading.type='MATERIAL';ar.spaces.active.overlay.show_overlays=False

def animate_and_save():
    h,m=actors['Haaland'],actors['Maresca']
    # Eased anticipation -> action -> settle, with secondary head lag. No free-running bob.
    keys(h['upper'],'rotation_euler',[(1,(0,0,0)),(32,(0,0,0)),(42,(0,0,-.018)),(58,(0,0,.024)),(82,(0,0,.015)),(108,(0,0,.01)),(131,(0,0,-.008)),(153,(0,0,0)),(192,(0,0,0))])
    keys(h['head'],'rotation_euler',[(1,(0,0,-.022)),(36,(0,0,-.022)),(43,(0,0,-.043)),(57,(0,0,.037)),(70,(0,0,.008)),(83,(0,0,.025)),(101,(0,0,.008)),(130,(0,0,-.024)),(155,(0,0,-.006)),(192,(0,0,-.006))])
    keys(h['head'],'location',[(1,(-.05,1.96,0)),(42,(-.07,1.945,0)),(59,(-.015,1.99,0)),(99,(-.025,1.97,0)),(141,(-.07,1.95,0)),(192,(-.05,1.96,0))])
    # The speaker has a small open-hand gesture with a relaxed follow-through.
    for side in (-1,1):
        hand=h[f'hand{side}'];hand.animation_data_clear()
        keys(hand,'location',[(1,(side*.79,.04,0)),(41,(side*.77,.01,0)),(66,(side*(1.00 if side==1 else .82),.28 if side==1 else .09,0)),(94,(side*.91,.15,0)),(125,(side*.80,.04,0)),(192,(side*.79,.04,0))])
        keys(h[f'elbow{side}'],'location',[(1,(side*.85,.63,0)),(63,(side*.96,.72,0)),(103,(side*.88,.64,0)),(139,(side*.85,.63,0)),(192,(side*.85,.63,0))])
    keys(m['upper'],'rotation_euler',[(1,(0,0,0)),(91,(0,0,0)),(101,(0,0,-.022)),(119,(0,0,.018)),(137,(0,0,-.008)),(154,(0,0,0)),(192,(0,0,0))])
    keys(m['head'],'rotation_euler',[(1,(0,0,0)),(87,(0,0,0)),(103,(0,0,.035)),(122,(0,0,-.026)),(146,(0,0,.008)),(161,(0,0,0)),(192,(0,0,0))])
    keys(m['head'],'location',[(1,(-.05,1.96,0)),(92,(-.05,1.96,0)),(106,(-.025,1.925,0)),(123,(-.07,1.98,0)),(147,(-.05,1.96,0)),(192,(-.05,1.96,0))])
    keys(m['badge'],'location',[(1,(0,-.12,.8)),(98,(0,-.12,.8)),(102,(0,-.155,.8)),(114,(0,.815,.8)),(119,(0,.853,.8)),(129,(0,.79,.8)),(141,(0,.802,.8)),(192,(0,.802,.8))])
    keys(m['badge'],'rotation_euler',[(1,(0,0,0)),(99,(0,0,0)),(108,(0,0,-.025)),(119,(0,0,.008)),(134,(0,0,0)),(192,(0,0,0))])
    for side in (-1,1):
        elbow=m[f'elbow{side}'];elbow.animation_data_clear()
        keys(elbow,'location',[(1,(side*.90,.60,0)),(99,(side*.90,.60,0)),(111,(side*1.03,.67,0)),(122,(side*.985,.62,0)),(139,(side*.98,.62,0)),(192,(side*.98,.62,0))])
    # Registered mouth drawings: half-open transitions before and after wider vowels.
    # Timing remains tied to the selected temporary line, without claiming final lip sync.
    changes_h=[(1,0),(28,3),(31,0),(59,1),(62,2),(66,1),(70,0),(73,1),(76,2),(81,1),(86,0),(91,1),(94,2),(98,1),(102,0),(141,3),(144,0)]
    changes_m=[(1,0),(91,1),(108,2),(148,3),(152,2)]
    for a,changes in [(h,changes_h),(m,changes_m)]:
        for frame,index in changes:
            for i,ob in enumerate(a['drawings']):
                ob.hide_render=ob.hide_viewport=i!=index;ob.keyframe_insert(data_path='hide_render',frame=frame);ob.keyframe_insert(data_path='hide_viewport',frame=frame)
    # Prove skin endpoints remain joined to collar/skull and hands to their limb throughout.
    worst=0.;grip_error=0.;neck_error=0.
    for frame in range(1,193):
        s.frame_set(frame);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
        for name,a in actors.items():
            for side in (-1,1):
                limb=bpy.data.objects[name+f' / arm {side} fill'].evaluated_get(dg);tip=limb.matrix_world@limb.data.splines[0].bezier_points[-1].co
                worst=max(worst,(tip.xy-a[f'hand{side}'].matrix_world.translation.xy).length)
            ne=a['neck'].evaluated_get(dg)
            for i,k in [(0,'Lbase'),(3,'Ltop'),(4,'Rtop'),(7,'Rbase')]:
                neck_error=max(neck_error,(ne.data.vertices[i].co.xy-a['neck_anchors'][k].matrix_world.translation.xy).length)
        for side in (-1,1):
            grip=bpy.data.objects['Maresca / badge grip '+str(side)].matrix_world.translation
            grip_error=max(grip_error,(grip.xy-m[f'hand{side}'].matrix_world.translation.xy).length)
    assert worst<1e-5 and neck_error<1e-5 and grip_error<1e-5,(worst,neck_error,grip_error)
    # Source pose has no foot keys and all shoes/leg controls remain outside upper-body acting.
    for name in actors:
        for side in (-1,1):assert bpy.data.objects[name+f' / foot {side}'].parent==actors[name]['root']
    s.frame_set(135);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'s01-neck-motion-v003.blend'))
    assert hashlib.sha256((OLD/'s01-morning-pep-v002.blend').read_bytes()).hexdigest()==source_hash
    checks={'frames_checked':192,'hand_limb_max_gap':worst,'neck_anchor_max_gap':neck_error,'badge_grip_max_gap':grip_error,'selected_sound':'B unchanged','source_native_preserved':True,'new_expression_drawings':8,'animation_rate':24,'native_inbetweening':'Bezier with clamped handles; head/upper body/arm/prop follow-through','not_established':['User acceptance of revised motion','Final dialogue performance or final lip sync','Full head turns or football actions']}
    (OUT/'native-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    return checks

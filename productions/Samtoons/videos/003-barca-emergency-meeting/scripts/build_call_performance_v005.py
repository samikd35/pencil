"""Second S08 construction: one connected skeleton drives the caricature.

Reuse the selected drawing, scene, face performance and sound timing. Replace
independently driven joint objects and per-frame wrist connector shapes with
parented bone chains and a genuinely bound skin surface. Run in visible Blender.
"""
import bpy, json, math
from pathlib import Path
from mathutils import Vector, Matrix

V=Path(__file__).resolve().parents[1]
O=V/'artifacts/staging-v001/call-performance-v005'
p=V/'scripts/build_call_performance_v004.py'
n={'__file__':str(p)}
exec(compile(p.read_text().replace('v004','v005').replace('C3V4','C3V5'),str(p),'exec'),n)
original_actor=n['actor'];original_pose=n['pose'];B=n['B'];PREFIX='C3V5 / '
errors=[]


def actor(who):
    original_actor(who)
    a=n['A'][who];rig=a['rig']
    for pb in rig.pose.bones:
        for co in list(pb.constraints):pb.constraints.remove(co)
    bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig
    bpy.ops.object.mode_set(mode='EDIT')
    for eb in rig.data.edit_bones:eb.align_roll(Vector((0,0,1)))
    rig.data.edit_bones['head'].parent=rig.data.edit_bones['torso'];rig.data.edit_bones['head'].use_connect=True
    for side in ['L','R']:
        upper,fore,hand=[rig.data.edit_bones[side+' '+part] for part in ['upper','fore','hand']]
        upper.parent=rig.data.edit_bones['torso'];fore.parent=upper;fore.use_connect=True;hand.parent=fore;hand.use_connect=True
    bpy.ops.object.mode_set(mode='OBJECT')
    rig.data.display_type='STICK';rig.show_in_front=True
    rig['purpose']='Single connected body skeleton; artwork follows these bones. Pose Mode exposes the moving foundation.'
    for pb in rig.pose.bones:pb.rotation_mode='XYZ'
    a['heading']={name:math.atan2((rig.data.bones[name].tail_local-rig.data.bones[name].head_local).y,(rig.data.bones[name].tail_local-rig.data.bones[name].head_local).x) for name in a['bones']}
    return {'actor':who,'connected_chains':2,'bones':len(rig.data.bones)}


def pose(a,f):
    # Reuse authored targets as a construction-time performance specification.
    # Export only connected-bone rotations; remove these old target objects later.
    original_pose(a,f)
    c=a['controls'];r=a['rig'];heading=a['heading'];delta={}
    for name,(start,end) in a['bones'].items():
        d=c[end].location-c[start].location
        angle=math.atan2(d.y,d.x)-heading[name]
        delta[name]=(angle+math.pi)%(2*math.pi)-math.pi
    for name in ['torso','head','L upper','L fore','L hand','R upper','R fore','R hand']:
        pb=r.pose.bones[name];parent=pb.parent.name if pb.parent else None
        pb.rotation_euler=(0,0,delta[name]-(delta[parent] if parent else 0))
        pb.keyframe_insert(data_path='rotation_euler',frame=f)
    bpy.context.view_layer.update()
    for name,(start,end) in a['bones'].items():
        pb=r.pose.bones[name]
        errors.extend([(pb.head-c[start].location).length,(pb.tail-c[end].location).length])


def bound_wrist(a):
    """Shared weighted topology for skin, shadow and silhouette, with no keys.

    The cuff end is owned by the forearm; the hand end by the hand bone. All
    intermediate samples use the same smooth weights on the same armature.
    """
    c=a['c'];join=c['wrist_join'];xy=n['xy'];h=[xy(p,c['origin']) for p in join['hand_edge']];w=[xy(p,c['origin']) for p in join['sleeve_edge']]
    skin,shade=('#fab470','#dd975c') if c['who']=='Muller' else ('#f9b06b','#dfa064')
    rows=[]
    for j in range(13):
        t=j/12;weight=t*t*(3-2*t)
        rows.append((w[0].lerp(h[0],t),w[1].lerp(h[1],t),weight))
    def mesh(label,vertices,faces,weights,color,z):
        me=bpy.data.meshes.new(PREFIX+c['who']+' bound wrist '+label);me.from_pydata([(p.x,p.y,z) for p in vertices],[],faces);me.materials.append(n['b']['mat'](color))
        ob=bpy.data.objects.new(me.name,me);n['col'].objects.link(ob);ob.parent=a['root']
        groups={name:ob.vertex_groups.new(name=name) for name in ['L fore','L hand']}
        for i,weight in enumerate(weights):
            groups['L fore'].add([i],1-weight,'REPLACE');groups['L hand'].add([i],weight,'REPLACE')
        mod=ob.modifiers.new('Shared body binding','ARMATURE');mod.object=a['rig'];mod.use_deform_preserve_volume=True
        ob['binding_region']='continuous wrist';a['surfaces'].append(ob);return ob
    for label,lo,hi,color,z in [('skin',0,1,skin,1.7),('shadow',.78,1,shade,1.71)]:
        vertices=[];weights=[]
        for left,right,weight in rows:
            for u in [lo,hi]:vertices.append(left.lerp(right,u));weights.append(weight)
        faces=[(2*j,2*j+1,2*j+3,2*j+2) for j in range(len(rows)-1)]
        mesh(label,vertices,faces,weights,color,z)
    # Flat ribbons share the exact skin boundary/weights; no tubular bevel in Z.
    for side in [0,1]:
        pts=[row[side] for row in rows];pts[-1]=pts[-1]+(pts[-1]-pts[-2]).normalized()*3
        vertices=[];weights=[]
        for i,p in enumerate(pts):
            tangent=pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)];normal=Vector((-tangent.y,tangent.x,0)).normalized()*1.5
            vertices.extend([p-normal,p+normal]);weights.extend([rows[i][2]]*2)
        mesh('edge '+str(side),vertices,[(2*j,2*j+1,2*j+3,2*j+2) for j in range(len(rows)-1)],weights,'#202332',1.72)


def finish_bindings():
    for a in n['A'].values():
        # The facial controls remain local and editable, but inherit the head
        # bone instead of carrying a second separately keyed head transform.
        face=a['face'];face.animation_data_clear()
        anchor=B['control'](a['c']['who']+' head attachment',parent=a['root'])
        co=anchor.constraints.new('COPY_TRANSFORMS');co.target=a['rig'];co.subtarget='head';co.target_space='POSE';co.owner_space='LOCAL'
        face.parent=anchor;face.matrix_parent_inverse=Matrix.Identity(4)
        face.matrix_basis=a['rig'].data.bones['head'].matrix_local.inverted()@Matrix.Translation(a['rest']['neck'])
        for ob in a['controls'].values():bpy.data.objects.remove(ob,do_unlink=True)
        a['controls'].clear()
    n['s']['construction']='One connected hierarchical body skeleton per actor; native vector artwork bound to it; independent local facial controls. Not Grease Pencil.'
    n['s']['scope']='Clean second version of the same 10-second S08 passage, same cached audio and timing.'


def save():
    assert errors and max(errors)<.005, f'Rig differs from authored pose by {max(errors)} source pixels'
    for a in n['A'].values():
        assert all(not pb.constraints for pb in a['rig'].pose.bones)
        for ob in a['surfaces']:
            assert len([m for m in ob.modifiers if m.type=='ARMATURE' and m.object==a['rig']])==1,ob.name
            assert all(abs(sum(g.weight for g in v.groups)-1)<1e-5 for v in ob.data.vertices),ob.name
            assert not ob.data.shape_keys,ob.name
    n['s'].frame_set(48);O.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(O/'call-performance.blend'))
    report={'frames':240,'max_pose_transfer_error_source_pixels':max(errors),'one_skeleton_per_actor':True,'connected_elbow_wrist_bones':True,'independently_keyed_joint_objects':0,'wrist_shape_keys':0,'audio':'Same cached takes and exact timing; no regeneration','scope':'Technical binding evidence, not creative acceptance'}
    (O/'binding-check.json').write_text(json.dumps(report,indent=2)+'\n');return report


def setup():
    n['setup']();n['pose']=pose;n['wrist_connection']=bound_wrist
    return {'scene':n['s'].name}


def animate():
    n['animate']();finish_bindings();return save()


def build():
    setup()
    for who in ['Muller','Perez']:actor(who)
    return animate()

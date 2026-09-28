"""Run in Blender after loading the call file; checks evaluated sleeve boundaries.
A numerical pass is deliberately not a visual or acting approval.
"""
import json
import math
from collections import Counter,defaultdict
from pathlib import Path
import bpy
import numpy as np


def crossings(points):
    p=np.asarray(points, dtype=float);q=np.roll(p,-1,axis=0);d=q-p
    def cross(a,b):return a[...,0]*b[...,1]-a[...,1]*b[...,0]
    den=cross(d[:,None,:],d[None,:,:]);delta=p[None,:,:]-p[:,None,:]
    safe=np.where(abs(den)>1e-8,den,1.)
    t=cross(delta,d[None,:,:])/safe;u=cross(delta,d[:,None,:])/safe
    hit=(abs(den)>1e-8)&(t>1e-6)&(t<1-1e-6)&(u>1e-6)&(u<1-1e-6)
    i,j=np.indices(hit.shape);hit&=(j>i+1)&~((i==0)&(j==len(p)-1))
    return np.argwhere(hit).tolist()


def check(scene, output, frames=range(1,241)):
    revision=scene.name.rsplit('_',1)[-1]
    prefix=f'C3V{int(revision[1:])} / '
    failures=[];objects=[o for o in scene.objects if o.name.endswith(('fitted sleeve fill','wrist connection fill','bound wrist skin'))]
    assert objects, 'No evaluated sleeve surfaces found'
    boundaries={}
    for ob in objects:
        counts=Counter(tuple(sorted(e)) for p in ob.data.polygons for e in p.edge_keys)
        adj=defaultdict(list)
        for (i,j),n in counts.items():
            if n==1:adj[i].append(j);adj[j].append(i)
        assert adj and all(len(v)==2 for v in adj.values()),f'Open or branched boundary: {ob.name}'
        start=next(iter(adj));loop=[start];prev=None;at=start
        while True:
            nxt=next(v for v in adj[at] if v!=prev)
            if nxt==start:break
            loop.append(nxt);prev,at=at,nxt
        boundaries[ob.name]=loop
    previous={};max_step=0.;max_wrist=0.;min_wrist_area=float('inf')
    bodies=[o for o in scene.objects if 'coherent head neck and torso' in o.name]
    rest={}
    def signed_triangles(ob):
        ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles()
        xyz=np.empty(len(me.vertices)*3,dtype=np.float32);me.vertices.foreach_get('co',xyz);xyz=xyz.reshape(-1,3)
        ids=np.array([t.vertices[:] for t in me.loop_triangles]);v=xyz[ids,:2];d=v[:,1]-v[:,0];e=v[:,2]-v[:,0]
        areas=d[:,0]*e[:,1]-d[:,1]*e[:,0];ev.to_mesh_clear();return areas
    scene.frame_set(1);bpy.context.view_layer.update()
    for ob in bodies:
        # A prop-only edit cannot pull the torso/scarf/neck through wrong weights.
        allowed={g.index for g in ob.vertex_groups if g.name in ('head','torso')}
        assert all(g.group in allowed for v in ob.data.vertices for g in v.groups if g.weight>1e-6),ob.name
        rest[ob.name]=signed_triangles(ob)
    for f in frames:
        scene.frame_set(f);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
        for ob in objects:
            ev=ob.evaluated_get(dg);me=ev.to_mesh()
            points=np.array([me.vertices[i].co[:2] for i in boundaries[ob.name]])
            pairs=crossings(points);ev.to_mesh_clear()
            if pairs:failures.append({'frame':f,'object':ob.name,'crossing_edges':pairs})
            if ob.name.endswith(('wrist connection fill','bound wrist skin')):
                area=abs(np.sum(points[:,0]*np.roll(points[:,1],-1)-points[:,1]*np.roll(points[:,0],-1)))/2
                min_wrist_area=min(min_wrist_area,float(area))
                if area<1:failures.append({'frame':f,'object':ob.name,'collapsed_wrist_area':float(area)})
        for ob in bodies:
            a=rest[ob.name];current=signed_triangles(ob)
            folded=int(np.count_nonzero((abs(a)>1)&(a*current<0)))
            if folded:failures.append({'frame':f,'object':ob.name,'folded_triangles':folded})
        for who in ['Muller','Perez']:
            if revision in ('v005','v006'):
                rig=scene.objects[prefix+who+' fitted drawing rig']
                fore=rig.pose.bones['L fore'];hand=rig.pose.bones['L hand']
                assert fore.bone.use_connect and hand.bone.use_connect
                elbow=fore.head.copy();wrist=fore.tail.copy();finger=hand.tail.copy()
                if (wrist-hand.head).length>.001:failures.append({'frame':f,'actor':who,'disconnected_wrist':(wrist-hand.head).length})
            else:
                key=prefix+who+' L '
                elbow=scene.objects[key+'elbow'].location.copy();wrist=scene.objects[key+'wrist'].location.copy();finger=scene.objects[key+'finger'].location.copy()
            if who in previous:max_step=max(max_step,(elbow-previous[who]).length)
            previous[who]=elbow
            v=wrist-elbow;h=finger-wrist
            angle=abs(math.degrees(math.atan2(v.x*h.y-v.y*h.x,v.x*h.x+v.y*h.y)));max_wrist=max(max_wrist,angle)
            if angle>42.01:failures.append({'frame':f,'actor':who,'excess_wrist_angle':angle})
    if list(frames)==list(range(1,241)) and max_step>25:failures.append({'elbow_step_pixels':max_step})
    report={'frames':list(frames),'surface_count':len(objects),'failures':failures,
            'max_elbow_step_source_pixels':max_step,'max_wrist_angle_degrees':max_wrist,
            'min_wrist_area_source_pixels_squared':min_wrist_area if math.isfinite(min_wrist_area) else None,
            'scope':'Evaluated topology and motion continuity; not likeness or visual approval.'}
    Path(output).write_text(json.dumps(report,indent=2)+'\n')
    assert not failures, f'{len(failures)} construction failures; see {output}'
    return report

if __name__=='__main__':
    check(bpy.context.scene,Path(bpy.data.filepath).with_name(Path(bpy.data.filepath).stem+'-checks.json'))

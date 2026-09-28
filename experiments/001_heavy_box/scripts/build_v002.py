"""Native editable curve character and a silent rough shot. Run in Blender 5.2.

blender --background --factory-startup --python-exit-code 1 --python build_v002.py
Optional: -- --render (all frames) or --samples (selected frames).
"""
import json
import math
from pathlib import Path
import sys
import bpy

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/rough-v002'
SHOT = json.loads((ROOT / 'shot-v002.json').read_text())
OUT.mkdir(parents=True, exist_ok=True)
INK = '#20252c'
WHITE = '#ffffff'
MATERIALS = {}


def sample(track, frame):
    if frame <= track[0][0]:
        return track[0][1:]
    for a, b in zip(track, track[1:]):
        if frame <= b[0]:
            t = (frame - a[0]) / (b[0] - a[0])
            t = t*t*(3-2*t)
            return [x+(y-x)*t for x, y in zip(a[1:], b[1:])]
    return track[-1][1:]


def material(color):
    if color not in MATERIALS:
        rgb = [int(color[i:i+2], 16)/255 for i in (1, 3, 5)]
        rgb = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in rgb]
        mat = bpy.data.materials.new(color)
        mat.diffuse_color = (*rgb, 1)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes.clear()
        output = nodes.new('ShaderNodeOutputMaterial')
        shader = nodes.new('ShaderNodeEmission')
        shader.inputs['Color'].default_value = (*rgb, 1)
        mat.node_tree.links.new(shader.outputs[0], output.inputs['Surface'])
        MATERIALS[color] = mat
    return MATERIALS[color]


def empty(name, parent=None):
    obj = bpy.data.objects.new(name, None)
    controls.objects.link(obj)
    obj.empty_display_type = 'CIRCLE'
    obj.empty_display_size = .12
    obj.parent = parent
    return obj


def path(name, pts, z, width=.042, color=INK, parent=None, cyclic=False):
    curve = bpy.data.curves.new(name, 'CURVE')
    curve.dimensions = '3D'
    curve.bevel_depth = width/2
    curve.bevel_resolution = 3
    curve.resolution_u = 20
    spline = curve.splines.new('POLY')
    spline.points.add(len(pts)-1)
    for p, xy in zip(spline.points, pts):
        p.co = (*xy, z, 1)
    spline.use_cyclic_u = cyclic
    curve.materials.append(material(color))
    obj = bpy.data.objects.new(name, curve)
    artwork.objects.link(obj)
    obj.parent = parent
    return obj


def shape(name, pts, z, color=WHITE, parent=None, outline=.042):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([(*xy, z) for xy in pts], [], [list(range(len(pts)))])
    mesh.materials.append(material(color))
    obj = bpy.data.objects.new(name, mesh)
    artwork.objects.link(obj)
    obj.parent = parent
    if outline:
        path(name+'_outline', pts, z+.008, outline, parent=parent, cyclic=True)
    return obj


def oval(cx, cy, rx, ry, n=64):
    return [(cx+rx*math.cos(i*math.tau/n), cy+ry*math.sin(i*math.tau/n)) for i in range(n)]


def smooth_closed(points, subdivisions=8):
    result = []
    for i, p1 in enumerate(points):
        p0, p2, p3 = points[i-1], points[(i+1)%len(points)], points[(i+2)%len(points)]
        for j in range(subdivisions):
            t = j/subdivisions
            result.append(tuple(.5*((2*p1[k])+(-p0[k]+p2[k])*t+(2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*t*t+(-p0[k]+3*p1[k]-3*p2[k]+p3[k])*t*t*t) for k in range(2)))
    return result


def driver(data, data_path, index, targets, expression):
    d = data.driver_add(data_path, index).driver
    for name, obj, axis in targets:
        v = d.variables.new()
        v.name = name
        v.type = 'TRANSFORMS'
        v.targets[0].id = obj
        v.targets[0].transform_type = 'LOC_'+axis
        v.targets[0].transform_space = 'WORLD_SPACE'
    d.expression = expression


def limb(name, start, bend, end, z):
    curve = bpy.data.curves.new(name, 'CURVE')
    curve.dimensions = '3D'
    curve.bevel_depth = .024
    curve.bevel_resolution = 3
    curve.resolution_u = 32
    spline = curve.splines.new('BEZIER')
    spline.bezier_points.add(1)
    for i, endpoint in enumerate((start, end)):
        p = spline.bezier_points[i]
        p.handle_left_type = p.handle_right_type = 'FREE'
        p.co = p.handle_left = p.handle_right = (0, 0, z)
        for axis, letter in enumerate('XY'):
            base = f'splines[0].bezier_points[{i}]'
            targets = [('a', endpoint, letter), ('b', bend, letter)]
            driver(curve, base+'.co', axis, targets, 'a')
            for handle in ('handle_left', 'handle_right'):
                driver(curve, base+'.'+handle, axis, targets, 'a+0.9*(b-a)')
    curve.materials.append(material(INK))
    obj = bpy.data.objects.new(name, curve)
    artwork.objects.link(obj)
    return obj


def joint(a, b, length, side, bend=1):
    dx, dy = b[0]-a[0], b[1]-a[1]
    distance = math.hypot(dx, dy)
    height = bend*math.sqrt(max(0, length*length-distance*distance/4))
    return ((a[0]+b[0])/2-side*dy*height/max(distance, .001),
            (a[1]+b[1])/2+side*dx*height/max(distance, .001))


def pose(frame):
    p = {name: sample(SHOT[name], frame) for name in ('body','foot_far','foot_near','hand_far','hand_near','box','face','head_tilt')}
    if SHOT['contact_frames'][0] <= frame <= SHOT['contact_frames'][1]:
        for name in ('hand_far', 'hand_near'):
            p[name][0] = p['box'][0]-hand_edge(p[name][2])
    # ponytail: authored per-shot poses; extract reusable actions only after another shot needs them.
    if 124 <= frame <= 145:
        p['body'][1] += .012*math.sin((frame-124)*1.9)
    return p


def hand_edge(angle):
    return max(x*math.cos(angle)-y*math.sin(angle) for x,y in mitten)+.019


def animate_transform(obj, xy, frame, angle=0):
    obj.location.x, obj.location.y = xy[:2]
    obj.rotation_euler.z = angle
    obj.keyframe_insert(data_path='location', frame=frame)
    obj.keyframe_insert(data_path='rotation_euler', frame=frame)


def points_key(obj, pts, frame):
    for point, xy in zip(obj.data.splines[0].points, pts):
        point.co.x, point.co.y = xy
        point.keyframe_insert(data_path='co', frame=frame)


bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.name = SHOT['title']
artwork = bpy.data.collections.new('Artwork • native vectors')
controls = bpy.data.collections.new('Pose controls • keyed and editable')
scene.collection.children.link(artwork)
scene.collection.children.link(controls)
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x, scene.render.resolution_y = SHOT['resolution']
scene.render.resolution_percentage = 100
scene.render.fps = SHOT['fps']
scene.frame_start, scene.frame_end = 1, SHOT['frames']
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'None'
scene.world.color = (1, 1, 1)
if hasattr(scene, 'eevee'):
    scene.eevee.taa_render_samples = 32

camera_data = bpy.data.cameras.new('Fixed camera')
camera = bpy.data.objects.new('Fixed camera', camera_data)
scene.collection.objects.link(camera)
camera.location = (*SHOT['camera'][:2], 30)
camera_data.type = 'ORTHO'
camera_data.ortho_scale = SHOT['camera'][2]
scene.camera = camera
shape('White backdrop', [(-20,-10),(20,-10),(20,15),(-20,15)], -2, outline=0)
path('Ground', [(-6,0),(5.6,0)], -.5, .012, '#d8dadd')

body = empty('CTRL_Body')
shoulder = empty('ANCHOR_Shoulder', body)
shoulder.location.y = .84
head = empty('CTRL_Head')
feet = {side: empty('CTRL_Foot_'+side) for side in ('far', 'near')}
hands = {side: empty('CTRL_Hand_'+side) for side in ('far', 'near')}
bends = {name: empty('CTRL_'+name) for name in ('Elbow_far','Elbow_near','Knee_far','Knee_near')}
box = empty('CTRL_Box')

shape('Bean torso', smooth_closed([(-.04,.88),(.08,.79),(.15,.35),(.12,.02),(0,-.08),(-.15,.05),(-.14,.4)]), .2, INK, body, 0)
shape('Head', oval(0,0,.57,.66), .4, parent=head, outline=.048)
eye_objects = []
for i, x in enumerate((-.03,.29)):
    obj = shape('Eye_'+str(i), oval(0,0,.057,.13), .43, INK, head, 0)
    obj.location = (x,.055,0)
    eye_objects.append(obj)
brows = [path('Brow_'+str(i), [(0,0)]*17, .45, .035, parent=head) for i in range(2)]
mouth = path('Mouth', [(0,0)]*25, .45, .034, parent=head)
open_mouth = shape('Mouth open', oval(.13,-.29,.075,.1), .44, INK, head, 0)

mitten = smooth_closed([(-.08,.06),(.01,.11),(.13,.04),(.16,-.08),(.12,-.15),(.07,-.10),(.06,-.20),(-.03,-.27),(-.12,-.20),(-.14,-.06)])
for side, z in (('far',.08),('near',.29)):
    shape('Mitten_'+side, mitten, z+.04, parent=hands[side], outline=.038)
    shape('Shoe_'+side, oval(.045,0,.29,.12), z+.04, parent=feet[side], outline=.041)
    limb('Arm_'+side, shoulder, bends['Elbow_'+side], hands[side], z)
    limb('Leg_'+side, body, bends['Knee_'+side], feet[side], z)

shape('Box front', [(0,0),(1.8,0),(1.8,2.30),(0,2.30)], .01, '#f4f1ea', box, .032)
shape('Box top', [(0,2.30),(.20,2.46),(2,2.46),(1.8,2.30)], .01, '#fcfaf5', box, .032)
shape('Box side', [(1.8,0),(2,.16),(2,2.46),(1.8,2.30)], .01, '#e0dbd1', box, .032)
shape('Tape', [(.79,0),(1.01,0),(1.01,2.30),(.79,2.30)], .025, '#e8e1d4', box, 0)
path('Tape top', [(.9,2.3),(1.1,2.46)], .03, .08, '#e8e1d4', box)

metrics = {'frames': SHOT['frames'], 'fps': SHOT['fps'], 'contact_error_max':0, 'planted_drift_max':0, 'max_limb_endpoint_distance':0, 'curve_driver_count':0}
for frame in range(1, SHOT['frames']+1):
    p = pose(frame)
    bx, by, angle = p['body']
    sh = (bx-.84*math.sin(angle), by+.84*math.cos(angle))
    animate_transform(body, (bx,by), frame, angle)
    animate_transform(head, (sh[0]-.02,sh[1]+.68), frame, p['head_tilt'][0])
    animate_transform(box, (p['box'][0],0), frame)
    for side in ('far','near'):
        for kind, objs in (('foot',feet),('hand',hands)):
            values = p[kind+'_'+side]
            animate_transform(objs[side], values, frame, values[2])
        push_blend = sample([[1,0],[42,0],[54,1],[151,1],[168,0],[240,0]],frame)[0]
        outward = max(-1,min(1,(p['hand_'+side][0]-sh[0])/.25))
        arm_sign = outward*(1-push_blend)-push_blend
        for part, a, b, length, sign, bend in (
            ('Elbow',sh,p['hand_'+side],.93,arm_sign,.45+.35*push_blend),
            ('Knee',(bx,by),p['foot_'+side],1.08,-1 if side=='far' else 1,.5-.3*push_blend if side=='far' else .65)):
            j = joint(a,b,length,sign,bend)
            animate_transform(bends[part+'_'+side],j,frame)
            metrics['max_limb_endpoint_distance'] = max(metrics['max_limb_endpoint_distance'],math.dist(a,b[:2]))
    squint, effort, surprise, suspicious = p['face']
    blink = max(0,1-abs(frame-207)/2) if 205 <= frame <= 209 else 0
    for i, eye in enumerate(eye_objects):
        eye.scale.y = max(.08, (1-.82*squint)*(1-.94*blink))
        eye.keyframe_insert(data_path='scale',frame=frame)
        x0 = -.14+i*.32
        brow_pts = []
        for n in range(17):
            t = n/16
            y = .30 + .065*math.sin(t*math.pi)*(1-effort-suspicious) + .06*surprise
            y += effort*(.09*(1-2*t) if i == 0 else .09*(2*t-1))
            y -= .13*suspicious
            brow_pts.append((x0+.23*t,y))
        points_key(brows[i],brow_pts,frame)
    pts=[]
    for n in range(25):
        t=n/24
        y=-.29-.055*math.sin(math.pi*t)*(1-2*effort-suspicious)
        y+=suspicious*.055*t
        pts.append((.025+.21*t,y))
    points_key(mouth,pts,frame)
    mouth.scale = (1,1,1) if surprise < .5 else (.001,.001,.001)
    mouth.keyframe_insert(data_path='scale',frame=frame)
    open_mouth.scale = (1,1,1) if surprise >= .5 else (.001,.001,.001)
    open_mouth.keyframe_insert(data_path='scale',frame=frame)
    if SHOT['contact_frames'][0] <= frame <= SHOT['contact_frames'][1]:
        for side in ('far','near'):
            metrics['contact_error_max'] = max(metrics['contact_error_max'],abs(p['hand_'+side][0]+hand_edge(p['hand_'+side][2])-p['box'][0]))

for name, intervals in SHOT['planted_intervals'].items():
    for start,end in intervals:
        anchor=pose(start)[name]
        for f in range(start,end+1):
            metrics['planted_drift_max']=max(metrics['planted_drift_max'],math.dist(anchor,pose(f)[name]))

# Bake dense transforms with linear interpolation: the source already supplies easing.
for action in bpy.data.actions:
    for slot in action.slots:
        for layer in action.layers:
            for strip in layer.strips:
                bag=strip.channelbag(slot)
                if bag:
                    for fc in bag.fcurves:
                        for key in fc.keyframe_points:
                            key.interpolation='LINEAR'
for frame, name in SHOT['beats']:
    scene.timeline_markers.new(name,frame=frame)

# One runnable integrity check: timing, planted contacts and evaluated native drivers.
assert sample([[1,0],[5,1]],3)==[.5]
assert metrics['contact_error_max'] < 1e-6
assert metrics['planted_drift_max'] < 1e-6
scene.frame_set(120)
bpy.context.view_layer.update()
for obj in artwork.objects:
    if obj.type=='CURVE' and obj.data.animation_data:
        for fc in obj.data.animation_data.drivers:
            metrics['curve_driver_count']+=1
            assert fc.driver.is_valid, (obj.name,fc.data_path)
arm = bpy.data.objects['Arm_near'].evaluated_get(bpy.context.evaluated_depsgraph_get())
tip=arm.data.splines[0].bezier_points[1].co
assert math.dist(tip[:2],pose(120)['hand_near'][:2]) < 1e-5
assert metrics['curve_driver_count']==48
metrics['checks']='passed: source contact targets, foot plants, driver validity and evaluated arm endpoint'
metrics['limits']='Contact includes mitten contour and outline radius; rendered occlusions still need review. Curve arc lengths are elastic. No automated creative-quality claim.'
(OUT/'checks.json').write_text(json.dumps(metrics,indent=2)+'\n')

scene['Notes']='C Elastic Comic. Native vector artwork and keyed pose controls. Source shot JSON contains this experiment’s timing. Curve bends remain editable. Silent rough pass; not final production acceptance.'
scene.render.filepath='//frames/'
scene.frame_set(70)
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_perspective='CAMERA'
            area.spaces.active.overlay.show_overlays=False
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'character-and-motion.blend'))
if '--samples' in sys.argv:
    for f in (1,48,70,104,140,155,170,220):
        scene.frame_set(f)
        scene.render.filepath=str(OUT/f'sample-{f:03}.png')
        bpy.ops.render.render(write_still=True)
if '--render' in sys.argv:
    scene.render.filepath=str(OUT/'frames/frame-')
    bpy.ops.render.render(animation=True)

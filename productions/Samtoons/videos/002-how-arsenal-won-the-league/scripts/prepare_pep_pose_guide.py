"""Visible Blender: authored pose guide only, not final character art."""
import bpy,math,json,sys
from pathlib import Path
V=Path('/Users/samikd/MyProjects/Pencil/productions/Samtoons/videos/002-how-arsenal-won-the-league');O=V/'assets/chase-poses-v003';O.mkdir(exist_ok=True)
sys.path.insert(0,str(V.parents[3]/'pipeline'));from pose_geometry import two_bone_joint
name='S002_Pep_walk_pose_guide';assert name not in bpy.data.scenes
s=bpy.data.scenes.new(name);bpy.context.window.scene=s;s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=8;s.render.resolution_x=1536;s.render.resolution_y=1024;s.render.resolution_percentage=100;s.render.film_transparent=False;s.view_settings.view_transform='Standard'
w=bpy.data.worlds.new(name);w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(1,1,1,1);s.world=w

def mat(name,c):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=(*c,1);out=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],out.inputs[0]);return m
near=mat('guide near leg',(.7,.08,.04));far=mat('guide far leg',(.08,.24,.7));body=mat('guide torso',(.08,.08,.08));ground=mat('guide ground',(.7,.7,.7))
def line(name,pts,m,depth=0,width=.032):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=width;c.bevel_resolution=2;p=c.splines.new('POLY');p.points.add(len(pts)-1)
 for q,(x,z) in zip(p.points,pts):q.co=(x,depth,z,1)
 ob=bpy.data.objects.new(name,c);s.collection.objects.link(ob);c.materials.append(m)
legs=[((.32,.065),(-.32,.10)),((.16,.065),(-.25,.17)),((0,.065),(.07,.17)),((-.16,.10),(.29,.13))]
heights=[.91,.87,.95,.94];records=[]
for i in range(8):
 phase=i%4;hx=-2.85+(i%4)*1.9;base=.30+(1-i//4)*2.5;hip=(0,heights[phase]);pairs=legs[phase] if i<4 else legs[phase][::-1]
 def world(p):return (p[0]+hx,p[1]+base)
 for leg,(ankle,m) in enumerate(zip(pairs,[near,far])):
  knee=two_bone_joint(hip,ankle,(.47,.47),(.9,.5));line(f'{i} leg {leg}',[world(hip),world(knee),world(ankle)],m,depth=-.04 if leg==0 else .04,width=.036)
  # Toe roll only on trailing support; toe of reaching foot elevated at contact.
  ph=phase if (leg==0)==(i<4) else (phase+4)%8
  toe=(ankle[0]+.16,max(.035,ankle[1]-.03));heel=(ankle[0]-.035,ankle[1]-.045)
  if phase==0 and ankle[0]>0:toe=(ankle[0]+.16,ankle[1]+.03)
  if ankle[0]<0 and phase in [0,3]:toe=(ankle[0]+.13,.035);heel=(ankle[0]-.03,ankle[1])
  line(f'{i} shoe {leg}',[world(heel),world(ankle),world(toe)],m,depth=-.04 if leg==0 else .04,width=.045)
  records.append(dict(pose=i,leg='near' if leg==0 else 'far',hip=hip,knee=knee,ankle=ankle,heel=heel,toe=toe))
 shoulder=(.015,hip[1]+.49);neck=(.055,hip[1]+.60)
 line(str(i)+' body',[world(hip),world(shoulder),world(neck)],body,width=.055)
 line(str(i)+' pocket arm',[world(shoulder),world((-.16,hip[1]+.22)),world((.02,hip[1]+.07))],body,depth=-.08,width=.034)
 circle=[world((neck[0]+.19*math.cos(t),neck[1]+.19+.22*math.sin(t))) for t in [j*math.tau/40 for j in range(41)]];line(str(i)+' head',circle,body,width=.025);line(str(i)+' nose',[world((.22,hip[1]+.80)),world((.29,hip[1]+.76)),world((.22,hip[1]+.74))],body,width=.02)
 line(str(i)+' ground',[(hx-.65,base),(hx+.65,base)],ground,width=.008)
cd=bpy.data.cameras.new(name);cd.type='ORTHO';cd.ortho_scale=7.6;cam=bpy.data.objects.new(name,cd);s.collection.objects.link(cam);cam.location=(0,-10,2.4);cam.rotation_euler=(math.pi/2,0,0);s.camera=cam
s.render.image_settings.file_format='PNG';s.render.filepath=str(O/'pose-guide.png');bpy.ops.render.render(write_still=True)
(O/'pose-guide.json').write_text(json.dumps(records,indent=2));bpy.data.libraries.write(str(O/'pose-guide.blend'),{s},fake_user=True)
result={'guide':str(O/'pose-guide.png'),'scope':'Internal authored geometry reference, not character quality approval'}

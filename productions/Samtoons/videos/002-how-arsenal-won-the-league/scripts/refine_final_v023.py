"""Contact and performance corrections found in the first final-batch frames."""
import bpy,math
from mathutils import Vector
ns=bpy.app.driver_namespace['final23'];S=ns['S'];A=ns['A'];key=ns['key'];smooth=ns['smooth'];pulse=ns['pulse'];n=ns['n']
def actor(sid,name):return next(a for a in A.values() if a['s']==S[sid] and a['name']==name)
# Keep telephone elbow below the shoulder; hold the handset near the mouth on speaker.
for sid in ['VH04_mikel','VH04_two','VH03_answer','VH04_operator','VH04_button']:
 s=S[sid];a=next(a for a in A.values() if a['s']==s);prop=next(o for o in s.objects if o.name.startswith('F23 hand phone'));bpy.context.window.scene=s
 for f in range(1,s.frame_end+1):
  s.frame_set(f);p={k:o.location.copy() for k,o in a['C'].items()};wr=p['neck']+Vector((.36,-.105,0));ns['reach'](a,p,'R',wr);key(prop,'location',f,wr+Vector((-.01,.035,0)));key(prop,'scale',f,(1.35,1.65,1));n['write_pose'](a,f,p)
# Button press uses the near hand on its own side of the desk, not across the torso.
s=S['VH04_button'];a=actor('VH04_button','Operator');button=next(o for o in s.objects if o.name.startswith('F23 play on button'));button.location.x=-.58;bpy.context.window.scene=s
for f in range(1,s.frame_end+1):
 s.frame_set(f);p={k:o.location.copy() for k,o in a['C'].items()};press=pulse(f,1,9,24);target=a['rest']['Lwrist'].lerp(Vector((-.40,1.045,0)),press);ns['reach'](a,p,'L',target);p['Lfinger']=target+Vector((0,-.075,0));n['write_pose'](a,f,p)
# The courier waits at the roadside: no unanimated feet sliding with the runners.
s=S['CP04_courier'];a=actor('CP04_courier','Courier');cart=next(o for o in s.objects if o.name.startswith('F23 runner-up delivery'));s.camera.data.ortho_scale=14
for f in range(1,s.frame_end+1):key(a['root'],'location',f,(7,-.25,0));key(cart,'location',f,(6.3,-.35,0));key(s.camera,'location',f,(6,-12,1.45))
# Clear the referee from the shirt-pull silhouette.
a=actor('VH01','Referee');a['root'].location.x=1.55
# The trophy is held by the raised hands at a reachable height.
s=S['N04_trophy'];a=actor('N04_trophy','Gyokeres');trophy=next(o for o in s.objects if o.name.startswith('F23 champions trophy'));trophy.scale=(.60,)*3;s.camera.data.ortho_scale=8.7;bpy.context.window.scene=s
for f in range(1,s.frame_end+1):
 s.frame_set(f);lift=smooth((f-6)/16);bottom=.82+.17*lift;p={k:o.location.copy() for k,o in a['C'].items()}
 for side,sign in [('L',-1),('R',1)]:
  ns['reach'](a,p,side,Vector((sign*.255/1.05,(bottom+.34)/1.05,0)));p[side+'finger']=p[side+'wrist']+Vector((-sign*.075,.015,0))
 n['write_pose'](a,f,p);key(trophy,'location',f,(.55,48.35,bottom))
# Same camera framing across the dark-to-lamp reveal.
dark=S['N04_dark'];dark.frame_set(dark.frame_end);S['N04_reveal'].camera.location=dark.camera.location.copy()
# Copy only the set, not shadow marks belonging to actors in the source scene.
for sc in S.values():
 for col in list(sc.collection.children):
  if col==ns['q']['env']:
   sc.collection.children.unlink(col)
   for ob in col.all_objects:
    if 'contact shadow' not in ob.name.lower() and ob.name not in sc.objects:sc.collection.objects.link(ob)
# Glove fingertips belong to the hand, including the mesh fringe below the source crop.
for a in A.values():
 if a['name']!='opposition goalkeeper':continue
 skin=a['skin'];c=a['cfg']
 for i,(px,py) in enumerate(a['pixels']):
  side='L' if px<c['center'] else 'R'
  if c[side][2][1]+15<py<c[side][3][1]+60 and abs(px-c['center'])>.73*abs(c[side][2][0]-c['center']):
   for g in skin.vertex_groups:g.remove([i])
   skin.vertex_groups[side+'hand'].add([i],1,'REPLACE')
# Match the ricochet to the evaluated shorts surface, with a ball-radius separation.
s=S['FR03_bonk'];bpy.context.window.scene=s;s.frame_set(8);a=actor('FR03_bonk','Gyokeres rear')
i=min(range(len(a['pixels'])),key=lambda i:(a['pixels'][i][0]-635)**2+(a['pixels'][i][1]-821)**2)
ev=a['skin'].evaluated_get(bpy.context.evaluated_depsgraph_get());surface=ev.matrix_world@ev.data.vertices[i].co;arrive=surface+Vector((0,-.11,0));goal=Vector((2.65,54.35,.58));launch=Vector((-33.48,51.98,.11))
# Continuous visible flight across the cross, complaint and impact cuts.
start=Vector((-.95,49.20,2.52));before=Vector((-.9,49.05,1.30))
for sid in ['FR03_cross','FR03_complain','FR03_bonk','FR03_goal']:
 s=S[sid];E=s.frame_end;ball=next(o for o in s.objects if o.name.startswith('F23 '+sid+' ball / v019 match ball'))
 if sid=='FR03_complain':s.camera.data.ortho_scale=6.3
 for f in range(1,E+1):
  if sid=='FR03_cross':
   u=max(0,min(1,(f-29)/(E-29)));p=launch.lerp(start,u);p.z+=1.8*4*u*(1-u);p.y+=1.3*math.sin(math.pi*u)
  elif sid=='FR03_complain':
   u=(f-1)/E;p=start.lerp(before,u);p.x+=1.5*math.sin(math.pi*u);p.z+=.15*math.sin(math.pi*u)
  elif sid=='FR03_bonk':p=before.lerp(arrive,(f-1)/7) if f<=8 else arrive.lerp(goal,(f-8)/40)
  else:
   p=arrive.lerp(goal,min(1,(f+16)/40))
   if f>24:p=goal+Vector((-.2*smooth((f-24)/15),-.24*smooth((f-24)/20),-.47*smooth((f-24)/28)))
  key(ball,'location',f,p)
import json
(ns['O']/'contact-checks.json').write_text(json.dumps({'backside_frame':8,'surface':list(surface),'ball_center':list(arrive),'surface_distance':(arrive-surface).length,'ball_radius':.11,'cross_release_frame':29,'goal_line_frame':24,'note':'Complaint shot uses comic extended airtime for dialogue; not physical real-time flight.'},indent=2))
ns['save']()
result={'fixed':['telephone elbow','courier ground contact','foul readability','trophy hand contact','reveal camera continuity']}

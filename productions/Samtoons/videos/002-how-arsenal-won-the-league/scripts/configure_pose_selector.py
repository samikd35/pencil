# One exposed, keyable pose selector instead of sixteen independent visibility tracks.
pose_names=['run'+str(i) for i in range(8)]+['jump'+str(i) for i in range(8)]
actor['pose_index']=0;actor.id_properties_ui('pose_index').update(min=0,max=15,description='0-7 run; 8 ready,9 load,10 extension,11 rise,12 tuck,13 reach,14 absorb,15 recover')
for i,key in enumerate(pose_names):
 label='Bruno / '+('run' if i<8 else 'jump')+' pose '+str((i%8)+1)
 ob=next(o for o in s.objects if o.name==label or o.name.startswith(label+'.'))
 ob.animation_data_clear()
 for prop in ['hide_render','hide_viewport']:
  driver=ob.driver_add(prop).driver;driver.expression='pose != '+str(i)
  v=driver.variables.new();v.name='pose';v.type='SINGLE_PROP';v.targets[0].id=actor;v.targets[0].data_path='["pose_index"]'
for row in rows:
 actor['pose_index']=pose_names.index(row['pose']);actor.keyframe_insert(data_path='["pose_index"]',frame=row['frame'])
 if row['frame']==138:row['phase']='landing_contact';row['contact_world']=rows[138]['contact_world']
for layer in actor.animation_data.action.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for fc in bag.fcurves:
    if fc.data_path=='["pose_index"]':
     for kp in fc.keyframe_points:kp.interpolation='CONSTANT'
s['Events']=json.dumps({'run_start':13,'gather':109,'load':117,'last_grounded_takeoff':122,'first_airborne':123,'first_landing_contact':138,'compression':141,'recovered':153})

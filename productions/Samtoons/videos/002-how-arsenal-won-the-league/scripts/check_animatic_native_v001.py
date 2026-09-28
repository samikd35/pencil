import bpy,json,os
s=bpy.data.scenes['S002_full_animatic_v001'];q=list(s.sequence_editor.strips);missing=[]
assert bpy.context.scene==s, 'Native edit must open on the authored timeline'
for x in q:
 if x.type=='MOVIE' and not os.path.exists(bpy.path.abspath(x.filepath)):missing.append(x.filepath)
 if x.type=='SOUND' and not os.path.exists(bpy.path.abspath(x.sound.filepath)):missing.append(x.sound.filepath)
movies=sorted([x for x in q if x.type=='MOVIE'],key=lambda x:x.frame_final_start)
assert len(movies)==55 and not missing
assert all(a.frame_final_end==b.frame_final_start for a,b in zip(movies,movies[1:]))
assert movies[0].frame_final_start==1 and movies[-1].frame_final_end==6110
result={'scene':s.name,'frames':s.frame_end,'movies':len(movies),'captions':len([x for x in q if x.type=='TEXT']),'missing':missing,'contiguous':True}
open(os.path.join(os.path.dirname(bpy.data.filepath),'native-check.json'),'w').write(json.dumps(result,indent=2))
print(json.dumps(result))

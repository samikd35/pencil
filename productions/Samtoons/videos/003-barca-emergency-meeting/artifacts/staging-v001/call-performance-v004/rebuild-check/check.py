import bpy,json,runpy
from pathlib import Path
v=Path('/Users/samikd/MyProjects/Pencil/productions/Samtoons/videos/003-barca-emergency-meeting')
p=v/'scripts/build_call_performance_v004.py'
n=runpy.run_path(str(p),run_name='rebuild_check')
n['build'].__globals__['O']=v/'artifacts/staging-v001/call-performance-v004/rebuild-check'
r=n['build']()
s=n['build'].__globals__['s']
for f in [74,139,214]:
    s.frame_set(f);s.render.filepath=str(n['build'].__globals__['O']/f'{f:03}.png');bpy.ops.render.render(write_still=True)
print('REBUILD_CHECK_READY',flush=True)

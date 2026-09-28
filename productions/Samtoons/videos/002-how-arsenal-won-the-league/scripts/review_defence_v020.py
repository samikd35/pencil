from PIL import Image,ImageDraw
import subprocess,io
from pathlib import Path
O=Path(__file__).resolve().parents[1]/'artifacts/defence-v020';FF='/opt/homebrew/bin/ffmpeg'
def sheet(name,clip,origin,frames,box,size,cols):
 w,h=size;out=Image.new('RGB',(w*cols,(h+24)*((len(frames)+cols-1)//cols)),(28,30,35));d=ImageDraw.Draw(out)
 for i,f in enumerate(frames):
  raw=subprocess.check_output([FF,'-v','error','-ss',str((f-origin)/24),'-i',str(O/'clips'/clip),'-frames:v','1','-f','image2pipe','-vcodec','png','-']);im=Image.open(io.BytesIO(raw)).crop(box);im.thumbnail(size);x=i%cols*w;y=i//cols*(h+24);out.paste(im,(x,y+24));d.text((x+8,y+5),str(f),fill='white')
 out.save(O/'checks'/name)
sheet('encoded-header-209-220.png','CD01_header.mp4',198,list(range(209,221)),(300,225,975,625),(450,267),3)
sheet('encoded-header-221-232.png','CD01_header.mp4',198,list(range(221,233)),(300,225,975,625),(450,267),3)
sheet('encoded-kick-154-171.png','CD01_cross.mp4',1,list(range(154,172)),(365,190,810,640),(297,300),6)
sheet('encoded-wall-430-445.png','CD03.mp4',392,list(range(430,446)),(235,305,1045,645),(405,170),4)
print('Actual encoded consecutive-frame sheets written')

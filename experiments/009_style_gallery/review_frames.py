"""Extract review sheets from the actual encoded proofs; no image generation or retouching."""
from pathlib import Path
import argparse
import cv2
from PIL import Image,ImageDraw

HERE=Path(__file__).resolve().parent

def sheet(frames,numbers,out,cols,crop=None):
 w,h=(350,310) if crop else (320,180)
 result=Image.new('RGB',(cols*w,((len(numbers)+cols-1)//cols)*(h+22)),'#f8f4ea');d=ImageDraw.Draw(result)
 for i,n in enumerate(numbers):
  im=Image.fromarray(cv2.cvtColor(frames[n-1],cv2.COLOR_BGR2RGB))
  if crop:im=im.crop(crop)
  im=im.resize((w,h),Image.Resampling.LANCZOS)
  x=(i%cols)*w;y=(i//cols)*(h+22);result.paste(im,(x,y));d.text((x+5,y+h+3),f'Frame {n}',fill='#243c42')
 result.save(out)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path);args=parser.parse_args()
 capture=cv2.VideoCapture(str(args.folder/'animatic-with-sound.mp4'));frames=[]
 while True:
  ok,frame=capture.read()
  if not ok:break
  frames.append(frame)
 capture.release();assert len(frames)==240
 sheet(frames,list(range(1,241,10)),args.folder/'motion-overview.png',4)
 sheet(frames,list(range(150,174)),args.folder/'release-successive-frames.png',6,crop=(100,30,450,340))
 sheet(frames,list(range(103,111)),args.folder/'push-successive-frames.png',4,crop=(100,30,450,340))
 print(args.folder)

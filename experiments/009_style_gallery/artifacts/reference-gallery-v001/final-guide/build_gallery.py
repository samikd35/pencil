"""Rebuild the offline image menu from the catalogue; no server or database."""
from pathlib import Path
import json
import sys

HERE=Path(__file__).resolve().parent

def build(sheet=False):
    data=json.loads((HERE/'catalog.json').read_text())
    template=(HERE/'gallery-template.html').read_text()
    # JSON is local catalogue data; escape the HTML script terminator at the embedding boundary.
    (HERE/'gallery.html').write_text(template.replace('/* CATALOG_DATA */',json.dumps(data).replace('<','\\u003c')))
    if sheet:
        # Attributed reference sheet; preserve each source composition without cropping.
        from PIL import Image, ImageDraw, ImageFont, ImageOps
        import textwrap
        canvas=Image.new('RGB',(2000,2540),'#f5f2ea');draw=ImageDraw.Draw(canvas)
        regular='/System/Library/Fonts/Supplemental/Arial.ttf'
        title=ImageFont.truetype(regular,52);label=ImageFont.truetype(regular,24);small=ImageFont.truetype(regular,19)
        draw.text((24,22),'Pencil / Choose a visual style',font=title,fill='#273e42')
        draw.text((27,91),'19 references from creators and studios. Choose the visual quality to aim for.',font=label,fill='#657574')
        draw.text((27,126),'Character + finish + environment. Any suitable character can use layered 2.5D scenery.',font=label,fill='#657574')
        for i,o in enumerate(data['options']):
            x=16+(i%4)*500;y=190+(i//4)*456
            with Image.open(HERE/o['sample']) as source:
                image=ImageOps.contain(source.convert('RGBA'),(468,290),method=Image.Resampling.NEAREST if o['id']=='pixelated' else Image.Resampling.LANCZOS)
            draw.rectangle((x,y,x+468,y+290),fill='#fffdf7')
            canvas.paste(image,(x+(468-image.width)//2,y+(290-image.height)//2),image)
            draw.text((x,y+305),textwrap.fill(f'{i+1:02}  {o["name"]}',33),font=label,fill='#273e42',spacing=3)
            draw.text((x,y+371),textwrap.fill(o['reference']['credit'],43),font=small,fill='#657574',spacing=3)
            draw.text((x,y+424),o['category']+' / Quality reference',font=small,fill='#657574')
        draw.text((27,2490),'External artwork, credited in the gallery. Film-specific artwork is reviewed against the selected reference.',font=label,fill='#657574')
        canvas.save(HERE/'menu.png')

if __name__=='__main__':build('--sheet' in sys.argv)

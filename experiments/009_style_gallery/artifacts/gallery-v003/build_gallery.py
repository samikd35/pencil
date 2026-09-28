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
        # Native-render contact sheet; Pillow is already available in the project's PyBlend venv.
        from PIL import Image, ImageDraw, ImageFont, ImageOps
        import textwrap
        canvas=Image.new('RGB',(2000,2400),'#f5f2ea');draw=ImageDraw.Draw(canvas)
        regular='/System/Library/Fonts/Supplemental/Arial.ttf'
        title=ImageFont.truetype(regular,52);label=ImageFont.truetype(regular,24);small=ImageFont.truetype(regular,19)
        draw.text((24,22),'Pencil / Choose a visual style',font=title,fill='#273e42')
        draw.text((27,91),'19 native examples. Codex recommends options for your story; you choose.',font=label,fill='#657574')
        draw.text((27,126),'Character + finish + environment. Card 19 shows 2.5D staging that other characters can use.',font=label,fill='#657574')
        for i,o in enumerate(data['options']):
            x=16+(i%5)*400;y=180+(i//5)*548
            image=Image.open(HERE/o['sample']).convert('RGB')
            image=ImageOps.fit(image,(368,442),method=Image.Resampling.NEAREST if o['id']=='pixelated' else Image.Resampling.LANCZOS)
            canvas.paste(image,(x,y))
            draw.text((x,y+450),textwrap.fill(f'{i+1:02}  {o["name"]}',27),font=label,fill='#273e42',spacing=2)
            draw.text((x,y+512),o['status'],font=small,fill='#657574')
        canvas.save(HERE/'menu.png')

if __name__=='__main__':build('--sheet' in sys.argv)

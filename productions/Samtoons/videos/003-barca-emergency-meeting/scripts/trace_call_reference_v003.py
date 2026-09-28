"""Extract editable source contours, registered in the unmodified call drawing.

Run with PYTHONPATH=.runtime/vector-art .runtime/qwen-voice/.venv/bin/python.
Uses the existing tracer/parser; alpha/semantic masks are construction inputs,
not new character artwork. The supplied pose remains the measured rest pose.
"""
import ast, hashlib, json, re, xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops, ImageFilter
import vtracer

V = Path(__file__).resolve().parents[1]
O = V / 'assets/reference-redraw-v003'
SOURCE = O / 'call-pose.png'
source = Image.open(SOURCE).convert('RGBA')
old = next(V.parent.glob('002*/scripts/trace_selected_heads_v011.py'))
node = ast.parse(old.read_text())
fn = next(n for n in node.body if isinstance(n, ast.FunctionDef) and n.name == 'convert')
exec(compile(ast.Module(body=[fn], type_ignores=[]), str(old), 'exec'))

DESIGNS = {
 'Muller': {
  'bounds': [45, 5, 794, 1017], 'origin': [442, 969], 'scale': .49,
  'location': [-284, -190, -40], 'skin': '#ffbd77',
  'hip': [442, 934], 'neck': [441, 450], 'jaw_y': 392, 'collar_y': 491,
  'L': [[306, 526], [209, 769], [129, 650]],
  'R': [[655, 534], [728, 780], [590, 873]],
  'prop': [[77, 343], [311, 313], [338, 590], [111, 624]],
  'grip': [[75,493],[133,497],[151,536],[150,599],[164,622],[157,652],[136,672],[111,667],[89,649],[62,585],[64,528]],
  'armL': [[324,440],[351,477],[331,569],[290,650],[270,759],[250,808],[228,832],[201,838],[171,827],[144,799],[117,752],[89,701],[62,600],[57,546],[63,513],[76,496],[103,487],[138,497],[156,520],[164,561],[164,620],[191,655],[231,707],[252,616],[264,522],[279,467]],
  'eyes': [
   {'center':[430,230], 'pupil':[439,230], 'size':[11,12], 'outline':[[400,228],[409,215],[426,209],[443,212],[454,225],[451,237],[435,245],[415,245],[402,239]]},
   {'center':[522,217], 'pupil':[534,216], 'size':[10,11], 'outline':[[499,214],[507,204],[523,198],[536,200],[544,211],[543,224],[534,232],[517,233],[504,226]]}],
  'brows': [[[385,207],[401,193],[425,186],[451,192],[463,198],[456,207],[430,201],[407,199]], [[501,198],[511,184],[534,171],[549,174],[559,184],[543,180],[524,187]]],
  'mouth': [[418,299],[432,304],[457,309],[489,310],[517,305],[537,299],[538,314],[525,325],[499,332],[458,331],[432,322],[419,313]],
  'mouth_center':[479,312], 'mouth_width':52,
 },
 'Perez': {
  'bounds':[803,44,1507,995], 'origin':[1124,947], 'scale':.58,
  'location':[369,-217,30], 'skin':'#ffbd78',
  'hip':[1124,914], 'neck':[1123,463], 'jaw_y':429, 'collar_y':491,
  'L':[[922,524],[878,790],[944,624]],
  'R':[[1347,543],[1413,798],[1264,869]],
  'prop': [[917,394],[935,397],[982,443],[1032,498],[1071,545],[1057,551],[996,494],[944,455],[914,428],[906,410]],
  'grip': [[956,438],[992,440],[1016,453],[1018,484],[1024,524],[1017,553],[996,564],[984,605],[966,630],[927,627],[907,604],[908,543],[906,502],[918,465]],
  'armL': [[919,480],[954,435],[995,435],[1025,454],[1030,523],[1017,566],[988,606],[991,657],[980,736],[950,810],[920,850],[881,865],[846,856],[818,829],[806,788],[815,699],[837,592],[852,508],[886,488]],
  'armR': [[1314,461],[1389,497],[1417,618],[1481,755],[1504,821],[1478,867],[1313,944],[1224,978],[1125,983],[1071,951],[1086,905],[1105,877],[1150,850],[1217,836],[1322,784],[1356,759],[1340,650],[1333,567],[1298,494]],
  'gripR': [[1237,844],[1264,850],[1277,869],[1283,899],[1271,923],[1238,937],[1205,956],[1178,974],[1158,974],[1140,965],[1120,960],[1108,947],[1090,937],[1081,921],[1089,898],[1110,878],[1147,856],[1188,847]],
  'eyes': [
   {'center':[1040,248], 'pupil':[1031,245], 'size':[9,10], 'outline':[[1008,237],[1023,229],[1041,231],[1057,238],[1065,249],[1058,258],[1040,263],[1022,259],[1013,250]]},
   {'center':[1133,260], 'pupil':[1120,256], 'size':[10,11], 'outline':[[1108,248],[1121,244],[1137,247],[1154,256],[1163,267],[1151,275],[1131,275],[1115,266],[1108,256]]}],
  'brows': [[[1014,211],[1030,200],[1043,198],[1058,204],[1071,216],[1064,221],[1046,211],[1029,210]], [[1106,230],[1115,215],[1133,214],[1153,219],[1170,227],[1182,241],[1165,236],[1141,226],[1123,226]]],
  'mouth': [[1024,338],[1041,348],[1065,353],[1090,354],[1116,357],[1119,372],[1098,371],[1078,365],[1052,364],[1031,358],[1022,349]],
  'mouth_center':[1070,355], 'mouth_width':39,
  'foreground': [[1080,930],[1092,893],[1134,867],[1205,849],[1250,825],[1339,773],[1371,750],[1434,750],[1472,778],[1492,817],[1470,859],[1312,939],[1223,975],[1126,980]]
 }
}

def mask_poly(points):
    m=Image.new('L', source.size); ImageDraw.Draw(m).polygon(points, fill=255)
    return m

def traced(mask):
    global im
    mask=ImageChops.multiply(mask, source.getchannel('A').point(lambda x:255 if x>=220 else 0))
    bounds=mask.getbbox()
    assert bounds, 'Empty source mask'
    im=source.crop(bounds)
    rows=convert(mask.crop(bounds))
    for row in rows:
        for path in row['paths']:
            for p in path:p[0]+=bounds[0];p[1]+=bounds[1]
    return rows

def grip_mask(poly):
    # Calibrated to this drawing's warm skin palette. A loose polygon also
    # captured the paper/pen/cuff and carried those fragments with the hand.
    skin=Image.new('L',source.size)
    skin.putdata([255 if r>145 and g>75 and r-g>20 and g-b>25 else 0 for r,g,b,a in source.getdata()])
    return ImageChops.multiply(mask_poly(poly),skin.filter(ImageFilter.MaxFilter(7)))

if __name__=='__main__':
    for who,c in DESIGNS.items():
        mask=Image.new('L',source.size); ImageDraw.Draw(mask).rectangle(c['bounds'],fill=255)
        parts={}
        for i,eye in enumerate(c['eyes']):ImageDraw.Draw(mask).polygon(eye['outline'],fill=0)
        for i,poly in enumerate(c['brows']):
            parts['brow'+str(i)]=traced(mask_poly(poly));ImageDraw.Draw(mask).polygon(poly,fill=0)
        parts['rest_mouth']=traced(mask_poly(c['mouth']));ImageDraw.Draw(mask).polygon(c['mouth'],fill=0)
        # Semantic occlusions are separate surfaces. A raised picture/pen must
        # not drag the hidden shirt or lapel when the hand moves away.
        prop=mask_poly(c['prop']).filter(ImageFilter.MaxFilter(7 if who=='Muller' else 11));prop=ImageChops.subtract(prop,mask_poly(c['grip']))
        parts['prop']=traced(prop)
        mask=ImageChops.subtract(mask,prop)
        hand=grip_mask(c['grip']);cut=640 if who=='Muller' else 590
        row=[x for x in range(source.width) if hand.getpixel((x,cut))]
        c['wrist_join']={'hand_edge':[[min(row),cut],[max(row),cut]],
                         'sleeve_edge':[[104,678],[158,661]] if who=='Muller' else [[916,646],[970,661]]}
        ImageDraw.Draw(hand).rectangle((0,cut+1,source.width,source.height),fill=0)
        parts['handL']=traced(hand)
        if 'gripR' in c:parts['handR']=traced(grip_mask(c['gripR']))
        for side in ['L','R']:
            if 'arm'+side not in c:continue
            arm=ImageChops.subtract(mask_poly(c['arm'+side]).filter(ImageFilter.MaxFilter(7)),prop)
            parts['arm'+side]=traced(arm)
            mask=ImageChops.subtract(mask,arm)
        if who=='Muller':
            scarf=mask_poly([(382,389),(364,410),(341,447),(327,499),(317,592),(306,694),(289,789),(265,859),(280,873),(394,875),(395,503)])
            mask=ImageChops.lighter(mask,ImageChops.subtract(scarf,prop))
        # Forearms are distinct foreground drawings. Their occluded upper arms
        # are reconstructed in Blender, rather than inferred from a flat overlap.
        forearms = {
          'Muller': {'L':[(86,634),(113,624),(157,615),(180,648),(213,681),(239,725),(255,777),(236,813),(213,829),(189,822),(156,797),(132,763),(109,723),(92,681)]},
          'Perez': {'L':[(905,588),(937,610),(979,621),(996,652),(997,677),(981,740),(952,807),(919,845),(884,860),(854,852),(830,832),(816,802),(818,771),(830,725),(847,679),(875,622)],
                    'R':[(1236,837),(1295,809),(1356,781),(1399,763),(1440,755),(1467,771),(1488,803),(1489,828),(1472,855),(1420,883),(1349,913),(1281,940),(1250,936),(1268,902),(1267,870)]}
        }
        for side,poly in forearms[who].items():
            fore=mask_poly(poly)
            fore=ImageChops.subtract(fore,mask_poly(c['grip' if side=='L' else 'gripR']))
            parts['fore'+side]=traced(fore)
        parts['body']=traced(mask)
        result={'source':str(SOURCE.relative_to(V)), 'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(), 'size':list(source.size), 'design':c, 'parts':parts,
                'construction':'VTracer 0.6.15 stacked native color contours; measured whole-source registration; explicit semantic face parts.'}
        assert all(len(p)>=3 for rows in parts.values() for r in rows for p in r['paths'])
        (O/(who.lower()+'-contours.json')).write_text(json.dumps(result,separators=(',',':'))+'\n')
        print(who,{k:(len(rows),sum(len(p) for r in rows for p in r['paths'])) for k,rows in parts.items()},flush=True)

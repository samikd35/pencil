"""Reframe the selected finished-film excerpt; no animation or audio regeneration.

Run with /opt/anaconda3/bin/python scripts/make_post_short.py OUTPUT_DIRECTORY.
The encoded file is a delivery review candidate, not user creative acceptance.
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/delivery-v003/samtoons-final-1080p.mp4'
MIX = ROOT / 'artifacts/delivery-v003/mix-review.wav'
START, END, FPS = 786, 1272, 24
SECONDS = (END - START) / FPS
INK, PAPER, CORAL = '#202430', '#fff6e5', '#f36b4b'
BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
REGULAR = '/System/Library/Fonts/Supplemental/Arial.ttf'

# Half-open source-frame ranges. Full-height action crops preserve feet and ball.
SHOTS = [
    (786, 809, (450, 0, 1080, 1080), 'Rashford strikes'),
    (809, 824, (440, 0, 1080, 1080), 'Premature celebration'),
    (824, 840, (840, 0, 1080, 1080), 'First ball/post contact'),
    (840, 911, (440, 0, 1080, 1080), 'Rashford reaction'),
    (911, 984, None, 'Post imitates Rashford; follow existing camera reveal'),
    (984, 1000, (0, 0, 1920, 1080), 'Brief full-width second-chance setup'),
    (1000, 1032, (430, 0, 1080, 1080), 'Mainoo strikes'),
    (1032, 1091, (300, 0, 1080, 1080), 'Second ball/post contact'),
    (1091, 1219, (560, 230, 620, 620), 'Talking post; original subtitle outside crop'),
    (1219, 1272, (660, 60, 760, 760), 'Bruno response; original subtitle outside crop'),
]


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REGULAR, size)


def backdrop():
    im = Image.new('RGB', (1080, 1920), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 1080, 349), fill=INK)
    logo = Image.open(ROOT.parents[1] / 'branding/v001/samtoons-logo.png').convert('RGBA')
    logo = logo.crop(logo.getbbox())
    logo.thumbnail((65, 85), Image.Resampling.LANCZOS)
    im.paste(logo, (363, 56), logo)
    d.text((448, 94), 'SamToons', font=font(51), fill=PAPER, anchor='lm')
    d.text((540, 200), "CITY'S BEST", font=font(80), fill=PAPER, anchor='mm')
    d.text((540, 287), 'DEFENDER?', font=font(101), fill=CORAL, anchor='mm')
    d.line((140, 1710, 940, 1710), fill=CORAL, width=3)
    d.text((540, 1760), 'Full derby cartoon on YouTube', font=font(38), fill=INK, anchor='mm')
    d.text((540, 1811), 'SamToons', font=font(34), fill=CORAL, anchor='mm')
    return im


def compose(source, n, base):
    shot = next(s for s in SHOTS if s[0] <= n < s[1])
    rect = shot[2]
    if rect is None:
        # Track the left solid white upright through the existing pull-back.
        # The goal-net threads are much thinner than the upright in this shot.
        a = np.asarray(source)
        white = (a[120:850, :1250, 0] > 225) & (a[120:850, :1250, 1] > 220) & (a[120:850, :1250, 2] > 195)
        columns = np.flatnonzero(white.sum(axis=0) > 420)
        if not len(columns):
            raise ValueError(f'Post tracking failed at source frame {n}')
        centre = int(columns[0] + 15)
        rect = (max(0, centre - 350), 180, 700, 700)
    x, y, w, h = rect
    assert 0 <= x and 0 <= y and x + w <= 1920 and y + h <= 1080
    crop = source.crop((x, y, x + w, y + h))
    image = base.copy()
    picture = ImageOps.contain(crop, (1080, 1080), Image.Resampling.LANCZOS)
    image.paste(picture, ((1080 - picture.width) // 2, 350 + (1080 - picture.height) // 2))
    d = ImageDraw.Draw(image)
    if 825 <= n < 1035:
        d.text((540, 1575), 'ONE POST. ONE SAVE.', font=font(56), fill=INK, anchor='mm')
    elif 1035 <= n < 1129:
        d.text((540, 1575), 'AND ANOTHER SAVE.', font=font(56), fill=INK, anchor='mm')
    elif 1129 <= n < 1211:
        d.text((540, 1529), 'TWO SAVES.', font=font(71), fill=CORAL, anchor='mm')
        d.text((540, 1614), 'I WANT A NEW CONTRACT.', font=font(58), fill=INK, anchor='mm')
    elif 1228 <= n < 1263:
        d.text((540, 1575), 'REF! REF!', font=font(94), fill=CORAL, anchor='mm')
    return image, rect


def main():
    out = Path(sys.argv[1]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    target = out / 'citys-best-defender-1080x1920.mp4'
    if target.exists():
        raise FileExistsError(target)
    assert SHOTS[0][0] == START and SHOTS[-1][1] == END
    assert all(a[1] == b[0] for a, b in zip(SHOTS, SHOTS[1:]))
    base = backdrop()
    # Preview actual composition before encoding; same function, source frames.
    for n in (805, 825, 923, 1035, 1170, 1245):
        frame = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', str(n / FPS), '-i', str(SOURCE), '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1'])
        im, _ = compose(Image.frombytes('RGB', (1920, 1080), frame), n, base)
        im.save(out / f'preview-{n}.jpg', quality=93)
    if '--stills' in sys.argv:
        return
    decode = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(START / FPS), '-i', str(SOURCE), '-frames:v', str(END - START), '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1'], stdout=subprocess.PIPE)
    with (out / 'encode.log').open('w') as log:
        encode = subprocess.Popen(['ffmpeg', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-r', str(FPS), '-i', 'pipe:0', '-ss', str(START / FPS), '-i', str(MIX), '-map', '0:v:0', '-map', '1:a:0', '-t', str(SECONDS), '-af', f'afade=t=in:d=0.035,afade=t=out:st={SECONDS-.15}:d=0.15', '-c:v', 'libx264', '-preset', 'fast', '-crf', '17', '-threads', '4', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'iec61966-2-1', '-colorspace', 'bt709', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', str(target)], stdin=subprocess.PIPE, stderr=log)
        crops = []
        try:
            for n in range(START, END):
                raw = decode.stdout.read(1920 * 1080 * 3)
                if len(raw) != 1920 * 1080 * 3:
                    raise ValueError(f'Missing source frame {n}')
                im, rect = compose(Image.frombytes('RGB', (1920, 1080), raw), n, base)
                crops.append([n, *rect])
                encode.stdin.write(im.tobytes())
                if (n - START) % 96 == 0:
                    print(f'Encoded {n - START}/{END - START} frames', flush=True)
            encode.stdin.close()
            assert encode.wait() == 0, (out / 'encode.log').read_text()
            assert decode.wait() == 0
        except BaseException:
            encode.kill(); decode.kill()
            encode.wait(); decode.wait()
            raise
    (out / 'edit.json').write_text(json.dumps(dict(source=str(SOURCE), mix=str(MIX), frames=[START, END], fps=FPS, seconds=SECONDS, resolution=[1080,1920], shots=SHOTS, crops=crops, audio='Selected source mix; 35ms entry and 150ms exit fades only', status='Delivery review candidate; no agent listening claimed'), indent=2) + '\n')
    print(target, flush=True)


if __name__ == '__main__':
    main()

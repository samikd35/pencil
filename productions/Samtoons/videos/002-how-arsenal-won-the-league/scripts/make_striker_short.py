"""Reframe five existing animated shots; preserve their speed and approved mix.

/opt/anaconda3/bin/python scripts/make_striker_short.py OUTPUT [--stills|--check]
Adapted from Video 001's make_post_short.py. No Blender or voice regeneration.
"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/delivery-v027'
FPS, START, END = 24, 1079, 1621
FRAMES = END - START
INK, PAPER, CORAL = '#202430', '#fff6e5', '#f36b4b'
FONT = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
SHOTS = [('TR02_flag', 120), ('TR02_reaction', 144), ('TR03_warning', 114),
         ('TR03_kick', 72), ('TR03_praise', 92)]


def font(size):
    return ImageFont.truetype(FONT, size)


def captions():
    def seconds(t):
        h, m, s = t.replace(',', '.').split(':')
        return 3600 * int(h) + 60 * int(m) + float(s)
    rows = []
    for block in (SOURCE / 'samtoons-final.srt').read_text().strip().split('\n\n'):
        lines = block.splitlines()
        a, b = [seconds(t) for t in lines[1].split(' --> ')]
        if b <= START / FPS or a >= END / FPS:
            continue
        speaker, text = ' '.join(lines[2:]).split(': ', 1)
        rows.append(dict(start=max(0, a - START / FPS), end=min(FRAMES / FPS, b - START / FPS),
                         speaker=speaker, text=text))
    return rows


CAPTIONS = captions()


def crop_for(shot, frame):
    if shot == 'TR02_flag':
        return 800, 0, 1120, 1080
    if shot == 'TR02_reaction':
        return (80, 20, 1000, 1060) if frame < 62 else (850, 20, 1070, 1060)
    if shot == 'TR03_warning':
        return (0, 260, 1600, 600) if frame < 32 else (450, 40, 1000, 1000)
    if shot == 'TR03_kick':
        t = max(0, min(1, (frame - 26) / 24))
        return 920 * t * t * (3 - 2 * t), 40, 1000, 1000
    return 480, 0, 1080, 1080


def backdrop(final=False):
    im = Image.new('RGB', (1080, 1920), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 1080, 329), fill=INK)
    logo = Image.open(ROOT / 'artifacts/short-striker-v001/samtoons-logo.png').convert('RGBA')
    logo = logo.crop(logo.getbbox())
    logo.thumbnail((52, 68), Image.Resampling.LANCZOS)
    im.paste(logo, (344, 39), logo)
    d.text((425, 73), 'SamToons', font=font(46), fill=PAPER, anchor='lm')
    if final:
        d.text((540, 181), 'FULL ARSENAL CARTOON', font=font(63), fill=PAPER, anchor='mm')
        d.text((540, 266), 'WATCH ON SAMTOONS', font=font(67), fill=CORAL, anchor='mm')
    else:
        d.text((540, 180), "ARSENAL'S REAL", font=font(78), fill=PAPER, anchor='mm')
        d.text((540, 270), 'STRIKER?', font=font(108), fill=CORAL, anchor='mm')
    d.line((130, 1750, 950, 1750), fill=CORAL, width=3)
    d.text((540, 1810), 'FOOTBALL. WITH A TWIST.', font=font(32), fill=INK, anchor='mm')
    return im


def caption_lines(text):
    d = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    lines = ['']
    for word in text.split():
        candidate = (lines[-1] + ' ' + word).strip()
        if d.textlength(candidate, font=font(62)) > 890:
            lines.append(word)
        else:
            lines[-1] = candidate
    assert len(lines) <= 2, text
    return lines


def compose(source, shot, local, n, bases):
    x, y, w, h = rect = crop_for(shot, local)
    width, height = round(w * min(1080/w, 1080/h)), round(h * min(1080/w, 1080/h))
    # Fractional sampling avoids integer-rounded jitter during the ball-follow pan.
    picture = source.transform((width, height), Image.Transform.EXTENT,
                               (x, y, x+w, y+h), Image.Resampling.BICUBIC)
    im = bases[n >= 450].copy()
    im.paste(picture, ((1080-width)//2, 330+(1080-height)//2))
    d = ImageDraw.Draw(im)
    for c in CAPTIONS:
        if c['start'] <= n/FPS < c['end']:
            d.text((540, 1490), c['speaker'], font=font(35), fill=CORAL, anchor='mm')
            lines = caption_lines(c['text'])
            for i, line in enumerate(lines):
                d.text((540, 1580 + (i-(len(lines)-1)/2)*77), line,
                       font=font(62), fill=INK, anchor='mm')
    return im, rect


def check():
    assert sum(n for _, n in SHOTS) == FRAMES == 542
    assert len(CAPTIONS) == 9
    assert CAPTIONS[0]['text'] == 'Meet our real striker.'
    assert CAPTIONS[-1]['text'] == 'Now we can actually score.'
    for a, b in zip(CAPTIONS, CAPTIONS[1:]):
        assert a['end'] <= b['start'] + 1e-8
    for c in CAPTIONS:
        assert 0 <= c['start'] < c['end'] <= FRAMES/FPS
        caption_lines(c['text'])
    for shot, length in SHOTS:
        probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams',
                           '-of', 'json', str(SOURCE/'clips'/f'{shot}.mp4')]))['streams'][0]
        assert int(probe['nb_frames']) == length and probe['r_frame_rate'] == '24/1'
        assert (probe['width'], probe['height']) == (1920, 1080)
        for f in range(length):
            x,y,w,h = crop_for(shot, f)
            assert min(x,y) >= 0 and x+w <= 1920 and y+h <= 1080
    print('Checked all 542 crop bounds, five clip lengths, source fps, and nine captions.', flush=True)


def main():
    out = Path(sys.argv[1]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out/'inspection').mkdir(exist_ok=True)
    check()
    if '--check' in sys.argv:
        return
    bases = [backdrop(), backdrop(True)]
    n = 0
    for shot, length in SHOTS:
        for f in sorted({0, length//2, length-1, *([26,36,48] if shot == 'TR03_kick' else [])}):
            raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', str(f/FPS), '-i',
                  str(SOURCE/'clips'/f'{shot}.mp4'), '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1'])
            im,_ = compose(Image.frombytes('RGB', (1920,1080), raw), shot, f, n+f, bases)
            im.save(out/'inspection'/f'layout-{n+f:04}.jpg', quality=92)
        n += length
    if '--stills' in sys.argv:
        return
    target = out/'artetas-real-striker-1080x1920.mp4'
    if target.exists():
        raise FileExistsError(target)
    # Trim by samples from the unbranded mix; no timing changes or internal splice.
    audio_filter = f'atrim=start_sample={START*2000}:end_sample={END*2000},asetpts=PTS-STARTPTS,afade=t=in:d=0.020,afade=t=out:st={FRAMES/FPS-.080}:d=0.080'
    with (out/'encode.log').open('w') as log:
        encode = subprocess.Popen(['ffmpeg', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
          '-s', '1080x1920', '-r', '24', '-i', 'pipe:0', '-i', str(SOURCE/'approved-soundtrack.m4a'),
          '-map', '0:v:0', '-map', '1:a:0', '-af', audio_filter, '-c:v', 'libx264', '-preset', 'fast',
          '-crf', '17', '-threads', '4', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709',
          '-color_trc', 'iec61966-2-1', '-colorspace', 'bt709', '-c:a', 'aac', '-b:a', '256k',
          '-ar', '48000', '-movflags', '+faststart', str(target)], stdin=subprocess.PIPE, stderr=log)
        crops, n, decode = [], 0, None
        try:
            for shot, length in SHOTS:
                decode = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(SOURCE/'clips'/f'{shot}.mp4'),
                       '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1'], stdout=subprocess.PIPE, stderr=log)
                for f in range(length):
                    raw = decode.stdout.read(1920*1080*3)
                    if len(raw) != 1920*1080*3:
                        raise ValueError(f'Missing {shot} frame {f}')
                    im, rect = compose(Image.frombytes('RGB', (1920,1080), raw), shot, f, n, bases)
                    encode.stdin.write(im.tobytes())
                    crops.append(dict(frame=n, shot=shot, local=f, crop=rect))
                    n += 1
                assert decode.stdout.read(1) == b'', f'Unexpected extra frames: {shot}'
                assert decode.wait() == 0
                print(f'Encoded {n}/{FRAMES} frames', flush=True)
            encode.stdin.close()
            assert encode.wait() == 0, (out/'encode.log').read_text()
        except BaseException:
            encode.kill(); encode.wait()
            if decode is not None:
                decode.kill(); decode.wait()
            raise
    def stamp(s):
        ms=round(s*1000); h,ms=divmod(ms,3600000); m,ms=divmod(ms,60000); sec,ms=divmod(ms,1000)
        return f'{h:02}:{m:02}:{sec:02},{ms:03}'
    (out/'captions.srt').write_text('\n\n'.join(f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['speaker']}: {c['text']}" for i,c in enumerate(CAPTIONS,1))+'\n')
    (out/'edit.json').write_text(json.dumps(dict(source=str(SOURCE), source_frames=[START,END],
        branded_v029_frames=[START+72,END+72], fps=FPS, frames=FRAMES, seconds=FRAMES/FPS,
        resolution=[1080,1920], shots=SHOTS, captions=CAPTIONS, crops=crops,
        audio_filter=audio_filter, status='Delivery review candidate; no agent listening claimed'), indent=2)+'\n')
    print(target, flush=True)


if __name__ == '__main__':
    main()

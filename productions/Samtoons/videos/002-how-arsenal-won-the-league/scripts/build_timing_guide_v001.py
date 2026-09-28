"""Measure a private neutral timing read; never substitutes for acted cast auditions."""
from pathlib import Path
import hashlib, json, re, subprocess, wave

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'script-v003.md'
OUT = ROOT / 'artifacts/preproduction-v001/timing'
EXPECTED = '81c206544bb86b2221e88766a48d5cd4e3e4b0d73f706fd02fb98b4c188d15a3'

def run(*args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout

def main():
    assert hashlib.sha256(SCRIPT.read_bytes()).hexdigest() == EXPECTED
    if OUT.exists():
        raise SystemExit('Use a new output revision; timing outputs already exist.')
    OUT.mkdir(parents=True)
    chapter, beat, records = 0, '', []
    for line in SCRIPT.read_text().splitlines():
        if m := re.match(r'## (\d)\.', line):
            chapter = int(m[1])
        if m := re.match(r'\*\*([A-Z]+\d+[a-z]?)\.', line):
            beat = m[1]
        if m := re.match(r'\*\*([^*]+):\*\* “([^”]+)”', line):
            role, text = m.groups()
            records.append({'id': f'L{len(records)+1:02}', 'chapter': chapter,
                            'beat': beat, 'role_and_direction': role, 'text': text,
                            'word_count': len(re.findall(r"[\w]+(?:[’'-][\w]+)*", text))})
    assert len(records) == 47 and {r['chapter'] for r in records} == set(range(1,8))
    for record in records:
        base = OUT / record['id']
        text_file, aiff, wav = base.with_suffix('.txt'), base.with_suffix('.aiff'), base.with_suffix('.wav')
        text_file.write_text(record['text'])
        run('/usr/bin/say', '-v', 'Daniel', '-r', '150', '-f', str(text_file), '-o', str(aiff))
        run('ffmpeg', '-v', 'error', '-i', str(aiff), '-ac', '1', '-ar', '48000', '-c:a', 'pcm_s16le', str(wav))
        with wave.open(str(wav)) as audio:
            record['seconds'] = audio.getnframes() / audio.getframerate()
        record['file'] = wav.name
        record['sha256'] = hashlib.sha256(wav.read_bytes()).hexdigest()
        # Keep the exact text and normalized WAV; source AIFF is reproducible and not selected.
        aiff.unlink()
        if len([r for r in records if 'seconds' in r]) % 10 == 0:
            print(f"Measured {record['id']}", flush=True)
    with wave.open(str(OUT / 'dialogue-timing-reference.wav'), 'wb') as dest:
        dest.setparams((1, 2, 48000, 0, 'NONE', 'not compressed'))
        cursor = 0
        for i, record in enumerate(records):
            record['reference_start_seconds'] = cursor / 48000
            with wave.open(str(OUT / record['file'])) as src:
                frames = src.readframes(src.getnframes())
                dest.writeframes(frames)
                cursor += len(frames) // 2
            if i < len(records) - 1:
                dest.writeframes(b'\0\0' * 16800)
                cursor += 16800
    report = {
        'script': str(SCRIPT.relative_to(ROOT)), 'script_sha256': EXPECTED,
        'purpose': 'Private neutral speech-duration reference. No cast identity or acting approval.',
        'source': 'Built-in macOS say, Daniel, requested 150 words/minute; no paid or remote generation.',
        'heard_by_agent': False, 'selected_for_final_audio': False,
        'line_gap_seconds': 0.35, 'dialogue_only_seconds': sum(r['seconds'] for r in records),
        'reference_seconds_with_line_gaps': cursor / 48000,
        'planned_film_seconds': 280,
        'chapter_dialogue_seconds': {str(c): sum(r['seconds'] for r in records if r['chapter'] == c) for c in range(1,8)},
        'lines': records,
        'limits': 'Neutral TTS does not time shouts, gasps or comic acting reliably. Visual action can overlap speech; remaining duration is a planning gap, not verified action time.'
    }
    (OUT / 'timing-report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    assert all(r['seconds'] > 0 for r in records)
    print(json.dumps({k:v for k,v in report.items() if k not in ('lines', 'limits')}, indent=2))

if __name__ == '__main__':
    main()

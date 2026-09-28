"""Fetch explicitly directed Qwen performances and prepare a new sound-B audition.

Uses the official free demo, no local model install. Cached requests and WAVs
are preserved; a new performance requires a new revision, not an overwrite.
"""
from pathlib import Path
from fractions import Fraction
import json, hashlib, subprocess, urllib.request, urllib.parse, wave, time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/voices-v002'
ASSETS = ROOT / 'assets/voices-v002'
FF = '/opt/homebrew/bin/ffmpeg'


def fetch(row):
    target = ASSETS / (row['id'] + '-raw.wav')
    metadata = target.with_suffix('.json')
    if target.exists():
        saved = json.loads(metadata.read_text())
        assert hashlib.sha256(target.read_bytes()).hexdigest() == saved['sha256']
        return target
    result_file = OUT / (row['id']+'-response.json')
    if result_file.exists():
        result = json.loads(result_file.read_text())
    else:
        endpoint = row['host'] + '/gradio_api/call/' + row['api']
        result = None
        started = time.monotonic()
        with urllib.request.urlopen(endpoint + '/' + row['event_id'], timeout=55) as response:
            event = ''
            for raw in response:
                if time.monotonic()-started > 120: raise TimeoutError('Demo queue exceeded two minutes.')
                line = raw.decode().strip()
                if line.startswith('event:'): event = line[6:].strip()
                if line.startswith('data:') and event in ('complete', 'error'):
                    result = json.loads(line[5:])
                    if event == 'error' or not result[0]: raise RuntimeError(result)
                    result_file.write_text(json.dumps(result,indent=2)+'\n')
                    break
        if not result: raise RuntimeError('No completed audio returned.')
    url = result[0]['url']
    assert urllib.parse.urlsplit(url).netloc == urllib.parse.urlsplit(row['host']).netloc
    with urllib.request.urlopen(url, timeout=30) as audio:
        payload = audio.read(10_000_001)
    assert len(payload) <= 10_000_000 and payload[:4] == b'RIFF'
    target.write_bytes(payload)
    metadata.write_text(json.dumps(dict(row, result=result, sha256=hashlib.sha256(payload).hexdigest()), indent=2)+'\n')
    return target


def main():
    ASSETS.mkdir(exist_ok=True)
    requests = json.loads((OUT/'generation-requests.json').read_text())
    base = json.loads((ROOT/'artifacts/sound-v001/plan-B.json').read_text())
    plan = json.loads(json.dumps(base))
    plan['title'] = 'Directed performances on selected sound B'
    records = []
    timings = {'bruno': ('S02', 'delayed_appeal', 154, 2.5, 0),
               'oliver': ('S10', 'spoken_apology', 43, 3.15, -.25),
               'carrick': ('S10', 'deadpan_reply', 221, 1.83, .25)}
    for row in requests:
        raw = fetch(row)
        target = ASSETS / (row['id']+'.wav')
        # Preserve generated acting. Only trim outer silence and set audition levels.
        # Shouting must come from the performance; increased gain is not a substitute.
        level = {'bruno': -17, 'oliver': -21, 'carrick': -22}[row['id']]
        filters = ('silenceremove=start_periods=1:start_duration=0.015:start_threshold=-45dB:start_silence=0.025,'
                   'areverse,silenceremove=start_periods=1:start_duration=0.015:start_threshold=-45dB:start_silence=0.06,areverse,'
                   f'highpass=f=65,loudnorm=I={level}:TP=-3:LRA=12,afade=t=in:d=0.005')
        if not target.exists():
            subprocess.run([FF,'-v','error','-i',str(raw),'-af',filters,'-ar','48000','-ac','1','-c:a','pcm_s24le',str(target)],check=True)
        with wave.open(str(target)) as w: exact_duration = Fraction(w.getnframes(),w.getframerate())
        duration = float(exact_duration)
        shot, event, frame, available, pan = timings[row['id']]
        print(row['id'], 'duration', round(duration,3), 'slot', available, flush=True)
        # Do not squash emotional acting into the old neutral read's timing.
        assert .1 < duration < available, (row['id'], duration, 'requires a timing revision')
        aid = row['id']+'-directed'
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        next(s for s in plan['shots'] if s['id']==shot)['events'][event] = frame-1
        plan['assets'][aid] = dict(path='../../'+str(target.relative_to(ROOT)), sha256=digest,
            source='Qwen3-TTS-1.7B VoiceDesign official hosted demo; see generation-requests.json and raw take metadata',
            license='Apache-2.0 model; original fictional performance, no real-person recording or clone',
            attribution='Qwen Team / https://github.com/QwenLM/Qwen3-TTS', notes=row['description'])
        plan['cues'].append(dict(id=aid,shot=shot,event=event,asset=aid,stem='dialogue',
            intent=row['description'],duration_seconds=str(exact_duration),gain_db=0,pan=pan))
        records.append(dict(row,path=str(target.relative_to(ROOT)),sha256=digest,duration_seconds=duration,processing=filters))
    assert plan['cues'][:len(base['cues'])] == base['cues']
    (OUT/'plan-directed.json').write_text(json.dumps(plan,indent=2)+'\n')
    (ASSETS/'takes.json').write_text(json.dumps(records,indent=2)+'\n')


if __name__ == '__main__': main()

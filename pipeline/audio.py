"""Resolve film events and mix selected sound files. Stdlib + FFmpeg; no creative presets."""
import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


def number(value, label):
    if isinstance(value, bool):
        raise ValueError(f"{label}: a finite number is required")
    try:
        return Fraction(str(value))
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{label}: a finite number is required") from exc


def positive_int(value, label):
    if type(value) is not int or value <= 0:
        raise ValueError(f"{label}: a positive integer is required")
    return value


def fields(record, allowed, required, label):
    if not isinstance(record, dict):
        raise ValueError(f"{label}: an object is required")
    missing, extra = set(required) - record.keys(), record.keys() - set(allowed)
    if missing or extra:
        raise ValueError(f"{label}: missing {sorted(missing)}, unknown {sorted(extra)}")


def text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}: nonempty text is required")
    return value


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def run(args, log=None):
    result = subprocess.run([str(a) for a in args], capture_output=True, text=True)
    if log is not None:
        with log.open('a') as stream:
            stream.write(json.dumps([str(a) for a in args]) + '\n' + result.stderr + '\n')
    if result.returncode:
        raise RuntimeError(f"{args[0]} failed: {result.stderr[-3000:]}")
    return result


def executable(name):
    result = shutil.which(name)
    if not result:
        raise ValueError(f"{name} is required on PATH")
    return result


def probe(path):
    data = json.loads(run([executable('ffprobe'), '-v', 'error', '-select_streams', 'a:0',
                           '-show_streams', '-show_format', '-of', 'json', path]).stdout)
    if not data.get('streams'):
        raise ValueError(f"No audio stream: {path}")
    stream = data['streams'][0]
    if stream.get('channels') not in (1, 2):
        raise ValueError(f"Prepare an explicit mono/stereo downmix first: {path}")
    if 'duration_ts' in stream and 'time_base' in stream:
        duration = number(stream['duration_ts'], 'duration_ts') * number(stream['time_base'], 'time_base')
    else:
        duration = number(stream.get('duration', data.get('format', {}).get('duration')), 'asset duration')
    if duration <= 0:
        raise ValueError(f"Empty audio: {path}")
    return {'sample_rate': int(stream['sample_rate']), 'channels': stream['channels'],
            'duration': str(duration), 'codec': stream['codec_name']}


def resolve(plan_path):
    plan_path = Path(plan_path).resolve()
    plan = json.loads(plan_path.read_text())
    if not isinstance(plan, dict) or type(plan.get('version')) is not int or plan['version'] != 1:
        raise ValueError('A version 1 production plan is required')
    timeline = plan.get('timeline')
    fields(timeline, ('fps', 'start_frame', 'frames', 'sample_rate'),
           ('fps', 'start_frame', 'frames', 'sample_rate'), 'timeline')
    if not isinstance(timeline['fps'], (str, int)) or isinstance(timeline['fps'], bool):
        raise ValueError('Use an exact integer or rational string for fps')
    fps = number(timeline['fps'], 'fps')
    if fps <= 0 or type(timeline['start_frame']) is not int:
        raise ValueError('Positive fps and an integer start_frame are required')
    frames = positive_int(timeline['frames'], 'frames')
    sr = positive_int(timeline['sample_rate'], 'sample_rate')
    total = round(frames * sr / fps)
    if total < 1:
        raise ValueError('The timeline must contain at least one audio sample')
    if not isinstance(plan.get('shots'), list) or not plan['shots']:
        raise ValueError('At least one shot is required')
    shots = {}
    for shot in plan['shots']:
        fields(shot, ('id', 'start_frame', 'events'), ('id', 'start_frame', 'events'), 'shot')
        sid = text(shot['id'], 'shot ID')
        if sid in shots:
            raise ValueError(f'Duplicate shot: {sid}')
        start = number(shot['start_frame'], 'shot start_frame')
        if not isinstance(shot['events'], dict):
            raise ValueError(f'Events must be an object: {sid}')
        events = {text(k, 'event ID'): number(v, 'event offset') for k, v in shot['events'].items()}
        shots[sid] = (start, events)

    if not isinstance(plan.get('assets'), dict):
        raise ValueError('assets must be an object')
    assets = {}
    for aid, asset in plan['assets'].items():
        text(aid, 'asset ID')
        fields(asset, ('path', 'sha256', 'source', 'license', 'attribution', 'notes'),
               ('path', 'sha256', 'source', 'license', 'attribution'), f'asset {aid}')
        for key in ('path', 'source', 'license'):
            text(asset[key], f'{aid}.{key}')
        if not isinstance(asset['attribution'], str):
            raise ValueError(f'{aid}.attribution must be text; empty is allowed')
        if not isinstance(asset['sha256'], str) or not re.fullmatch('[0-9a-f]{64}', asset['sha256']):
            raise ValueError(f'{aid}: actual lowercase SHA-256 required')
        path = (plan_path.parent / asset['path']).resolve()
        if not path.is_file() or digest(path) != asset['sha256']:
            raise ValueError(f'Missing or changed selected asset: {aid}')
        assets[aid] = {**asset, 'path': str(path), 'format': probe(path)}

    if not isinstance(plan.get('cues'), list) or not plan['cues']:
        raise ValueError('At least one sound cue is required; silence-only films can skip audio build')
    cues, ids = [], set()
    optional = ('in_seconds', 'duration_seconds', 'onset_seconds', 'offset_frames', 'gain_db',
                'pan', 'fade_in_seconds', 'fade_out_seconds', 'allow_boundary_trim')
    required = ('id', 'shot', 'event', 'intent', 'asset', 'stem', 'duration_seconds')
    for cue in plan['cues']:
        fields(cue, set(optional) | set(required), required, 'cue')
        for key in ('id', 'shot', 'event', 'intent', 'asset', 'stem'):
            text(cue[key], f'cue {key}')
        cid = cue['id']
        if cid in ids:
            raise ValueError(f'Duplicate cue: {cid}')
        ids.add(cid)
        if not re.fullmatch('[A-Za-z0-9][A-Za-z0-9_-]*', cue['stem']):
            raise ValueError(f'Unsafe stem filename: {cue["stem"]}')
        if cue['shot'] not in shots or cue['asset'] not in assets:
            raise ValueError(f'Unresolved shot or asset: {cid}')
        start, events = shots[cue['shot']]
        if cue['event'] not in events:
            raise ValueError(f'Unresolved event: {cid}')
        values = {key: number(cue.get(key, 0), f'{cid}.{key}') for key in optional if key != 'allow_boundary_trim'}
        trim = cue.get('allow_boundary_trim', False)
        if type(trim) is not bool:
            raise ValueError(f'{cid}.allow_boundary_trim must be boolean')
        for key in ('in_seconds', 'onset_seconds', 'fade_in_seconds', 'fade_out_seconds'):
            if values[key] < 0:
                raise ValueError(f'{cid}.{key} must be nonnegative')
        duration = values['duration_seconds']
        if duration <= 0 or not -1 <= values['pan'] <= 1:
            raise ValueError(f'Invalid duration or pan: {cid}')
        if values['onset_seconds'] >= duration:
            raise ValueError(f'Onset must be inside the segment: {cid}')
        if values['fade_in_seconds'] + values['fade_out_seconds'] > duration:
            raise ValueError(f'Fades exceed the segment: {cid}')
        available = number(assets[cue['asset']]['format']['duration'], 'source duration')
        if values['in_seconds'] + duration > available:
            raise ValueError(f'Selected segment exceeds source; prepare an extension/loop: {cid}')
        event_frame = start + events[cue['event']] + values['offset_frames']
        event_sample = round((event_frame - timeline['start_frame']) * sr / fps)
        onset, length = round(values['onset_seconds'] * sr), round(duration * sr)
        if length < 1 or onset >= length:
            raise ValueError(f'Segment/onset is too short at the selected sample rate: {cid}')
        placement = event_sample - onset
        if placement >= total or placement + length <= 0:
            raise ValueError(f'Cue is entirely outside the film: {cid}')
        if not trim and (placement < 0 or placement + length > total):
            raise ValueError(f'Cue crosses film boundary: {cid}; explicitly allow_boundary_trim if intended')
        try:
            gain = float(values['gain_db'])
            amplitude = 10 ** (gain / 20)
        except OverflowError as exc:
            raise ValueError(f'Unrepresentable gain: {cid}') from exc
        if not math.isfinite(amplitude) or amplitude == 0:
            raise ValueError(f'Unrepresentable gain: {cid}')
        cues.append({**cue, 'gain_db': gain, 'pan': float(values['pan']),
                     'event_frame': str(event_frame), 'event_sample': event_sample,
                     'start_sample': placement, 'source_start_sample': round(values['in_seconds'] * sr),
                     'samples': length, 'onset_samples': onset,
                     'fade_in_samples': round(values['fade_in_seconds'] * sr),
                     'fade_out_samples': round(values['fade_out_seconds'] * sr),
                     'trimmed_start_samples': max(0, -placement),
                     'trimmed_end_samples': max(0, placement + length - total)})
    mix_value = number(plan.get('mix_gain_db', 0), 'mix_gain_db')
    if abs(mix_value) > 300:
        raise ValueError('mix_gain_db is outside a representable audio range')
    mix_gain = float(mix_value)
    if not math.isfinite(mix_gain) or abs(mix_gain) > 300:
        raise ValueError('mix_gain_db is outside a representable audio range')
    return {'version': 1, 'plan': str(plan_path), 'plan_sha256': digest(plan_path),
            'timeline': {**timeline, 'fps': str(fps)}, 'samples': total, 'assets': assets,
            'cues': cues, 'mix_gain_db': mix_gain}


def cue_filter(cue, index, sr):
    start, n = cue['source_start_sample'], cue['samples']
    chain = [f'aresample={sr}', 'aformat=sample_fmts=fltp:channel_layouts=stereo',
             f'atrim=start_sample={start}:end_sample={start+n}', 'asetpts=PTS-STARTPTS',
             f'volume={cue["gain_db"]}dB']
    p = cue['pan']
    chain.append(f'pan=stereo|c0={1-max(0,p)}*c0|c1={1+min(0,p)}*c1')
    if cue['fade_in_samples']:
        chain.append(f'afade=t=in:ss=0:ns={cue["fade_in_samples"]}')
    if cue['fade_out_samples']:
        fade = cue['fade_out_samples']
        chain.append(f'afade=t=out:ss={n-fade}:ns={fade}')
    if cue['start_sample'] < 0:
        chain.extend([f'atrim=start_sample={-cue["start_sample"]}', 'asetpts=PTS-STARTPTS'])
    else:
        chain.append(f'adelay={cue["start_sample"]}S:all=1')
    return f'[{index}:a:0]' + ','.join(chain) + f'[a{index}]'


def mix_group(ff, sources, target, sr, total, log, filters=None, gain_db=0):
    args = [ff, '-hide_banner', '-nostdin', '-v', 'warning', '-y']
    for path in sources:
        args.extend(['-i', path])
    parts = list(filters or [])
    inputs = ''.join(f'[a{i}]' if filters else f'[{i}:a:0]' for i in range(len(sources)))
    parts.append(inputs + f'amix=inputs={len(sources)}:normalize=0:duration=longest:dropout_transition=0,'
                 f'volume={gain_db}dB,apad=whole_len={total},atrim=end_sample={total},'
                 'asetpts=PTS-STARTPTS[out]')
    args.extend(['-filter_complex', ';'.join(parts), '-map', '[out]', '-ar', str(sr), '-ac', '2',
                 '-c:a', 'pcm_f32le', '-rf64', 'auto', target])
    run(args, log)


def reduce_mix(ff, paths, target, sr, total, log, temp, gain_db=0):
    # ponytail: full-timeline intermediates bound open inputs; scene renders if disk use becomes limiting.
    level = 0
    while len(paths) > 16:
        next_paths = []
        for group, offset in enumerate(range(0, len(paths), 16)):
            output = temp / f'reduce-{target.stem}-{level}-{group}.wav'
            mix_group(ff, paths[offset:offset+16], output, sr, total, log)
            next_paths.append(output)
        paths = next_paths
        level += 1
    mix_group(ff, paths, target, sr, total, log, gain_db=gain_db)


def write_json(path, data):
    with Path(path).open('x') as stream:
        json.dump(data, stream, indent=2, allow_nan=False)
        stream.write('\n')


def build(plan_path, output):
    resolved = resolve(plan_path)
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    log = output / 'ffmpeg.log'
    try:
        ff = executable('ffmpeg')
        sr, total = resolved['timeline']['sample_rate'], resolved['samples']
        write_json(output / 'resolved-cues.json', resolved)
        stems_dir = output / 'stems'
        stems_dir.mkdir()
        stems = []
        with tempfile.TemporaryDirectory(prefix='.mix-', dir=output) as tmp:
            temp = Path(tmp)
            for stem in sorted({c['stem'] for c in resolved['cues']}):
                cues = sorted((c for c in resolved['cues'] if c['stem'] == stem), key=lambda c: c['id'])
                batches = []
                for group, offset in enumerate(range(0, len(cues), 16)):
                    subset = cues[offset:offset+16]
                    sources = [resolved['assets'][c['asset']]['path'] for c in subset]
                    target = temp / f'batch-{stem}-{group}.wav'
                    mix_group(ff, sources, target, sr, total, log,
                              [cue_filter(c, i, sr) for i, c in enumerate(subset)])
                    batches.append(target)
                target = stems_dir / f'{stem}.wav'
                reduce_mix(ff, batches, target, sr, total, log, temp)
                stems.append(target)
            master = output / 'mix-premaster.wav'
            reduce_mix(ff, stems, master, sr, total, log, temp, resolved['mix_gain_db'])
        checks = {'scope': 'Technical premaster checks; subjective listening and final encoded checks are separate',
                  'ffmpeg': run([ff, '-version']).stdout.splitlines()[0], 'outputs': []}
        for path in [*stems, master]:
            meta = probe(path)
            if number(meta['duration'], 'output duration') * sr != total:
                raise ValueError(f'Output length mismatch: {path}')
            if meta['channels'] != 2 or meta['sample_rate'] != sr:
                raise ValueError(f'Output format mismatch: {path}')
            stats = run([ff, '-hide_banner', '-nostdin', '-xerror', '-i', path,
                         '-af', 'astats=reset=0', '-f', 'null', '-'], log).stderr
            invalid = re.findall(r'Number of (?:NaNs|Infs): ([^\s]+)', stats)
            if not invalid or any(float(count) != 0 for count in invalid):
                raise ValueError(f'Nonfinite samples or unavailable integrity measurement: {path}')
            checks['outputs'].append({'path': str(path.relative_to(output)), 'sha256': digest(path),
                                      'format': meta, 'samples': total, 'decoded': True,
                                      'finite_samples': True})
        measured = run([ff, '-hide_banner', '-nostdin', '-i', master,
                        '-af', 'loudnorm=print_format=json', '-f', 'null', '-'], log)
        levels = json.loads(re.findall(r'\{[^{}]+\}', measured.stderr)[-1])
        checks['premaster_measurement'] = {k: v for k, v in levels.items() if k.startswith('input_')}
        checks['finishing_required'] = True
        checks['peak_above_full_scale'] = float(levels['input_tp']) > 0
        if digest(Path(plan_path)) != resolved['plan_sha256'] or any(
                digest(Path(asset['path'])) != asset['sha256'] for asset in resolved['assets'].values()):
            raise ValueError('Plan or selected assets changed during rendering; use immutable input revisions')
        write_json(output / 'checks.json', checks)
        return checks
    except Exception as exc:
        write_json(output / 'failed.json', {'error': str(exc), 'plan': str(Path(plan_path).resolve())})
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('resolve', 'build'))
    parser.add_argument('plan', type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'resolve':
            write_json(args.out, resolve(args.plan))
        else:
            build(args.plan, args.out)
    except (ValueError, OSError, RuntimeError, KeyError) as exc:
        parser.exit(1, f'Audio build stopped: {exc}\n')
    print(f'{args.command}: {args.out}')


if __name__ == '__main__':
    main()

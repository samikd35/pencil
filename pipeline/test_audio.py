"""Run real FFmpeg timing/mixing checks in a disposable folder; no production assets changed."""
from array import array
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import wave

import audio


def pcm(path):
    result = subprocess.run([audio.executable('ffmpeg'), '-v', 'error', '-i', str(path),
                             '-f', 'f32le', '-c:a', 'pcm_f32le', '-'],
                            check=True, capture_output=True)
    values = array('f')
    values.frombytes(result.stdout)
    if sys.byteorder != 'little':
        values.byteswap()
    return values


def main():
    with tempfile.TemporaryDirectory(prefix='pencil-audio-test-') as temp:
        root = Path(temp)
        asset = root / 'selected.wav'
        samples = array('h', [0] * (9600 * 2))
        samples[960*2], samples[960*2+1] = 8192, 4096
        # A second isolated sample checks that the chosen segment's tail survives.
        samples[6239*2], samples[6239*2+1] = 2048, 1024
        if sys.byteorder != 'little':
            samples.byteswap()
        with wave.open(str(asset), 'wb') as f:
            f.setparams((2, 2, 48000, 0, 'NONE', 'not compressed'))
            f.writeframes(samples.tobytes())
        plan = {
            'version': 1,
            'timeline': {'fps': '30000/1001', 'start_frame': 101, 'frames': 60, 'sample_rate': 48000},
            'shots': [{'id': 'shot', 'start_frame': 101, 'events': {'contact': '21/2'}}],
            'assets': {'take-a': {'path': asset.name, 'sha256': audio.digest(asset),
                                  'source': 'Original disposable test impulses',
                                  'license': 'Original test synthesis', 'attribution': ''}},
            'cues': [{'id': 'contact-a', 'shot': 'shot', 'event': 'contact', 'asset': 'take-a',
                      'intent': 'Check contact alignment and segment tail', 'stem': 'contact',
                      'in_seconds': '.01', 'duration_seconds': '.12', 'onset_seconds': '.01',
                      'offset_frames': '.25', 'gain_db': -6.020599913279624}],
            'mix_gain_db': -6.020599913279624}
        path = root / 'production.json'

        def save(value):
            path.write_text(json.dumps(value, allow_nan=False))

        def fails(value, phrase):
            save(value)
            try:
                audio.resolve(path)
            except (ValueError, OSError) as exc:
                assert phrase in str(exc), str(exc)
            else:
                raise AssertionError(f'Expected validation failure: {phrase}')

        save(plan)
        resolved = root / 'resolved.json'
        cli = [sys.executable, str(Path(audio.__file__)), 'resolve', str(path), '--out', str(resolved)]
        subprocess.run(cli, check=True, capture_output=True)
        before = resolved.read_bytes()
        assert subprocess.run(cli, capture_output=True).returncode != 0
        assert resolved.read_bytes() == before
        first = json.loads(before)
        assert first['cues'][0]['event_sample'] == 17217
        assert first['samples'] == 96096
        checks = audio.build(path, root / 'base')
        stem = pcm(root / 'base/stems/contact.wav')
        master = pcm(root / 'base/mix-premaster.wav')
        assert len(stem) == len(master) == 96096 * 2
        nonzero = [i//2 for i in range(0, len(stem), 2) if abs(stem[i]) > 1e-7]
        assert nonzero == [17217, 22496], nonzero
        assert abs(stem[17217*2] - .125) < 1e-6
        assert abs(stem[17217*2+1] - .0625) < 1e-6
        assert abs(master[17217*2] - .0625) < 1e-6
        assert checks['outputs'][0]['decoded'] and not checks['peak_above_full_scale']

        changed = deepcopy(plan)
        changed['shots'][0]['start_frame'] += 7
        save(changed)
        moved = audio.resolve(path)
        assert moved['cues'][0]['event_sample'] == 28428
        assert moved['assets'] == first['assets']
        changed['shots'][0]['events']['contact'] = 13
        save(changed)
        assert audio.resolve(path)['cues'][0]['event_sample'] == 32432
        integer = deepcopy(plan)
        integer['timeline']['fps'] = 24
        save(integer)
        assert audio.resolve(path)['cues'][0]['event_sample'] == 21500

        # More than one batch, overlapping sources, and a second independent stem.
        many = deepcopy(plan)
        many['mix_gain_db'] = 0
        many['cues'] = [{**plan['cues'][0], 'id': f'take-{i:02}', 'gain_db': -26.020599913279625}
                        for i in range(19)]
        many['cues'].append({**plan['cues'][0], 'id': 'other-stem', 'stem': 'detail', 'pan': -1})
        save(many)
        audio.build(path, root / 'overlap')
        overlap = pcm(root / 'overlap/mix-premaster.wav')
        assert abs(overlap[17217*2] - (.25 * .05 * 19 + .125)) < 1e-6
        assert abs(overlap[17217*2+1] - (.125 * .05 * 19)) < 1e-6
        assert audio.resolve(path)['assets'] == first['assets']

        boundary = deepcopy(plan)
        boundary['shots'][0]['events']['contact'] = 0
        boundary['cues'][0]['offset_frames'] = 0
        fails(boundary, 'crosses film boundary')
        boundary['cues'][0]['allow_boundary_trim'] = True
        save(boundary)
        audio.build(path, root / 'prelap')
        assert abs(pcm(root / 'prelap/stems/contact.wav')[0] - .125) < 1e-6
        boundary['shots'][0]['events']['contact'] = 1000
        fails(boundary, 'entirely outside')

        # Exercise the failure artifact with real invalid floating-point audio.
        broken = root / 'nonfinite.wav'
        subprocess.run([audio.executable('ffmpeg'), '-v', 'error', '-f', 'lavfi', '-i',
                        'aevalsrc=nan|nan:s=48000:d=0.2', '-c:a', 'pcm_f32le', str(broken)],
                       check=True, capture_output=True)
        bad_audio = deepcopy(plan)
        bad_audio['assets']['take-a']['path'] = broken.name
        bad_audio['assets']['take-a']['sha256'] = audio.digest(broken)
        save(bad_audio)
        try:
            audio.build(path, root / 'failed')
        except ValueError as exc:
            assert 'Nonfinite samples' in str(exc), str(exc)
            assert (root / 'failed/failed.json').is_file()
            assert not (root / 'failed/checks.json').exists()
        else:
            raise AssertionError('Nonfinite output was accepted')

        invalid = deepcopy(plan)
        invalid['assets']['take-a']['sha256'] = '0' * 64
        fails(invalid, 'changed selected asset')
        invalid = deepcopy(plan)
        invalid['cues'].append(deepcopy(invalid['cues'][0]))
        fails(invalid, 'Duplicate cue')
        for key, value, phrase in [('event', 'missing', 'Unresolved event'),
                                   ('duration_seconds', 20, 'exceeds source'),
                                   ('onset_seconds', .15, 'Onset must be inside'),
                                   ('pan', 2, 'Invalid duration or pan'),
                                   ('gain_db', 'NaN', 'finite number'),
                                   ('stem', '../escape', 'Unsafe stem'),
                                   ('gain_dB', -6, 'unknown')]:
            invalid = deepcopy(plan)
            invalid['cues'][0][key] = value
            fails(invalid, phrase)
        save(plan)
        try:
            audio.build(path, root / 'base')
        except FileExistsError:
            pass
        else:
            raise AssertionError('An existing delivery was overwritten')
        assert pcm(root / 'base/mix-premaster.wav') == master
    print('PASS: exact integer/fractional-FPS contact/onset, tail, stereo/gain, shot and action retiming, '
          'stable selection, overlap across batches/stems, explicit prelap, nonfinite rejection, '
          'failure records, validation and preservation')


if __name__ == '__main__':
    main()

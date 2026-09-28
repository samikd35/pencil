"""Package this completed revision and verify every archived byte against its source."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[1]
OUT = ROOT / 'artifacts/film-v004'
plan = json.loads((ROOT / 'production.json').read_text())
checks = json.loads((OUT / 'video-checks.json').read_text())
assert checks['full_decode'] and checks['frames'] == 912
assert plan['revision'] == 'film-v004' and plan['candidate'] == 'clean'
files = [ROOT / p for p in [
    'README.md', 'brief.md', 'script-v005.md', 'staging-v005.json', 'production.json', 'events.jsonl',
    'scripts/build_polished.py', 'scripts/verify_staged.py', 'scripts/render_staged.py',
    'scripts/finish_checkpoint.py', 'scripts/package_final.py',
    'design/treatment-v003/heads.png', 'design/treatment-v003/heads-prompt.txt',
    'design/treatment-v003/stadium.png', 'design/treatment-v003/stadium-prompt.txt',
    'design/treatment-v004/supporting-heads.png', 'design/treatment-v004/heads-prompt.txt',
    'assets/audio-v002/provenance.json', 'assets/audio-v002/crowd-cheer.mp3',
    'assets/audio-v002/crowd-cheer-page.html', 'assets/audio-v002/goal-crowd.mp3',
    'assets/audio-v002/goal-crowd-page.html']]
files += [ROOT / a['path'] for a in plan['assets'].values()]
files += [OUT / p for p in [
    'barcelona-wasnt-ready-trent-was.mp4', 'trent-corner-advanced.blend', 'soundtrack.wav',
    'production.json', 'review.md', 'staging-checks.json', 'video-checks.json',
    'encoded-overview.jpg', 'encoded-contacts.jpg', 'poster.png', 'workflow-checks.json',
    'audio-v001/checks.json', 'audio-v001/resolved-cues.json', 'audio-v001/mix-premaster.wav']]
files += list((OUT / 'audio-v001/stems').glob('*.wav')) + list((OUT / 'workflow').glob('*'))
files += [WORKSPACE / p for p in ['AGENTS.md', 'pipeline/README.md', 'pipeline/audio.py',
                                  'pipeline/checkpoints.py', 'experiments/001_heavy_box/journal.py']]
files = sorted(set(files))
assert all(p.is_file() and p.resolve().is_relative_to(WORKSPACE) for p in files)
movie = OUT / 'barcelona-wasnt-ready-trent-was.mp4'
assert hashlib.sha256(movie.read_bytes()).hexdigest() == checks['sha256']
archive = OUT / 'trent-corner-editable-package.zip'
with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for p in files:
        z.write(p, p.relative_to(WORKSPACE))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert all(z.read(p.relative_to(WORKSPACE).as_posix()) == p.read_bytes() for p in files)
report = dict(files=len(files), bytes=archive.stat().st_size,
              sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
              crc_passed=True, every_entry_matches_source=True,
              note='Journal is a snapshot before this archive-hash event; preserved older movies are excluded.')
(OUT / 'package-checks.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))

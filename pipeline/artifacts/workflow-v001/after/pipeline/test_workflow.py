"""Check the installed source and video-local review records without creating real productions."""
import os
from pathlib import Path
import shutil
import sys
import tempfile

from checkpoints import require_checkpoint

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments/001_heavy_box'))
from journal import append_event


def main():
    installed = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills/produce-pencil-animation/SKILL.md'
    source = ROOT / 'pipeline/SKILL.md'
    assert installed.is_symlink() and installed.samefile(source), 'Installed skill must use the project source'

    with tempfile.TemporaryDirectory(prefix='pencil-workflow-test-') as directory:
        production = Path(directory) / 'productions/example'
        shared = production / 'assets/character-v001.txt'
        shared.parent.mkdir(parents=True)
        shared.write_text('selected character')
        videos = [production / 'videos' / name for name in ('001-first', '002-second')]
        for video in videos:
            (video / 'assets').mkdir(parents=True)
            shutil.copyfile(shared, video / 'assets/character.txt')
            (video / 'preview.txt').write_text('synthetic review artifact')

        # Simulated user acceptance exists only in this disposable fixture.
        def accept(video):
            append_event(video, stage='checkpoint/v001/staging', status='passed', reviewer='user',
                         intent='Test local review isolation', method='Synthetic fixture',
                         result='Simulated acceptance', inputs=['assets/character.txt'], outputs=['preview.txt'])

        def blocked(video):
            try:
                require_checkpoint(video, 'v001', 'staging')
            except RuntimeError:
                return
            raise AssertionError('Unreviewed or changed video passed its checkpoint')

        first, second = videos
        accept(first)
        blocked(second)
        accept(second)
        shared.write_text('later shared change')
        for video in videos:
            require_checkpoint(video, 'v001', 'staging')
            assert (video / 'assets/character.txt').read_text() == 'selected character'
        # Adopting that change invalidates only the video whose selection changed.
        shutil.copyfile(shared, second / 'assets/character.txt')
        blocked(second)
        require_checkpoint(first, 'v001', 'staging')

    print('PASS: installed skill shares the canonical source; sibling reviews are isolated; shared changes preserve selected copies; adopting a change invalidates only the affected video.')


if __name__ == '__main__':
    main()

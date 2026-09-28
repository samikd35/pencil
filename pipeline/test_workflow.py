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
    installed_dir = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills/produce-pencil-animation'
    installed = installed_dir / 'SKILL.md'
    source = ROOT / 'pipeline/SKILL.md'
    assert installed_dir.is_symlink() and installed_dir.samefile(ROOT / 'pipeline/skill'), 'Installed skill directory must link to the isolated live skill folder'
    assert source.is_symlink() and source.samefile(ROOT / 'pipeline/skill/SKILL.md'), 'The stable pipeline entry point must resolve to the live source'
    assert not installed.is_symlink() and installed.is_file() and installed.samefile(source), 'SKILL.md must be a discoverable regular file using the project source'

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

        # Explicit profile selection, not an automatic niche resolver. Real review
        # guards must bind context and relevant guides just like artwork.
        profiles = {
            'football': ('Football parody; illustrated characters and directed dialogue.',
                         'character-guide.md', 'Inspect face views and deforming limbs.'),
            'mechanism': ('Silent pump explanation; labelled diagrams; no characters.',
                          'diagram-guide.md', 'Inspect component connections and flow direction.'),
        }
        selected = {}
        for niche, (context, guide_name, guidance) in profiles.items():
            parent = Path(directory) / 'productions' / niche
            video = parent / 'videos/001-example'
            (video / 'assets').mkdir(parents=True)
            profile = parent / 'README.md'; profile.write_text(context)
            guide = parent / guide_name; guide.write_text(guidance)
            refs = ['assets/production-context.md', 'assets/' + guide_name]
            shutil.copyfile(profile, video / refs[0])
            shutil.copyfile(guide, video / refs[1])
            (video / 'preview.txt').write_text('synthetic staging review')
            append_event(video, stage='checkpoint/v001/staging', status='passed', reviewer='user',
                         intent='Test explicit context and guide binding', method='Synthetic fixture',
                         result='Simulated staging acceptance', inputs=refs, outputs=['preview.txt'])
            selected[niche] = (video, profile, guide, refs)
        football, parent_profile, parent_guide, football_refs = selected['football']
        mechanism, _, _, mechanism_refs = selected['mechanism']
        assert set(p.name for p in (mechanism / 'assets').iterdir()) == {
            'production-context.md', 'diagram-guide.md'}
        for external in (parent_profile, parent_guide):
            external.write_text('new parent version')
        for niche, (video, _, _, refs) in selected.items():
            require_checkpoint(video, 'v001', 'staging')
            assert (video / refs[0]).read_text() == profiles[niche][0]
        # Explicit profile adoption only invalidates the adopting film.
        shutil.copyfile(parent_profile, football / football_refs[0])
        blocked(football)
        require_checkpoint(mechanism, 'v001', 'staging')
        # Mutating selected technique guidance invalidates its bound review too.
        (mechanism / mechanism_refs[1]).write_text('changed local diagram guidance')
        blocked(mechanism)

        # A new filename leaves the old reviewed bytes intact. Check the inputs
        # the next operation will actually use, not only the previous manifest.
        (first / 'source-A.blend').write_bytes(b'first selected source')
        (first / 'source-B.blend').write_bytes(b'new selected source')
        (first / 'mix.wav').write_bytes(b'unchanged selected sound')
        for stage, names in [('animatic', ['source-A.blend']), ('sound', ['mix.wav'])]:
            append_event(first, stage='checkpoint/switch/' + stage, status='passed', reviewer='user',
                         intent='Test current input selection', method='Disposable source-switch fixture',
                         result='Simulated acceptance', inputs=names, outputs=['preview.txt'])
        require_checkpoint(first, 'switch', 'animatic', required_inputs=['source-A.blend'])
        try:
            require_checkpoint(first, 'switch', 'animatic', required_inputs='source-A.blend')
        except ValueError:
            pass
        else:
            raise AssertionError('A bare path was treated as a collection of inputs')
        for names in (['source-B.blend'], ['missing.blend'], ['../outside.blend']):
            try:
                require_checkpoint(first, 'switch', 'animatic', required_inputs=names)
            except RuntimeError:
                pass
            else:
                raise AssertionError('An unbound or invalid current source passed')
        require_checkpoint(first, 'switch', 'sound', required_inputs=['mix.wav'])
        append_event(first, stage='checkpoint/switch/animatic', status='passed', reviewer='user',
                     intent='Test adoption of changed source', method='Disposable fixture',
                     result='Simulated new acceptance', inputs=['source-B.blend'], outputs=['preview.txt'])
        require_checkpoint(first, 'switch', 'animatic', required_inputs=['source-B.blend'])
        (first / 'source-B.blend').write_bytes(b'changed after review')
        try:
            require_checkpoint(first, 'switch', 'animatic', required_inputs=['source-B.blend'])
        except RuntimeError:
            pass
        else:
            raise AssertionError('Changed selected source retained acceptance')

    print('PASS: canonical skill; isolated reviews; preserved asset/profile/guide snapshots; explicit adoption and changed sources invalidate affected reviews; a switch to an unbound source blocks while unchanged sound remains valid. Niche selection is explicit, not automated.')


if __name__ == '__main__':
    main()

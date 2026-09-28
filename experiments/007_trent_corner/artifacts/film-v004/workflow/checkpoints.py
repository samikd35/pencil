"""Read-only gate on actual, current user checkpoint decisions in the production journal."""
import hashlib
import json
from pathlib import Path
import sys


def require_checkpoint(root, revision, stage):
    root = Path(root).resolve()
    if stage not in ('staging', 'sound', 'animatic', 'delivery') or not revision or '/' in revision:
        raise ValueError('Use a revision name and staging, sound, animatic or delivery')
    key = f'checkpoint/{revision}/{stage}'
    journal = root / 'events.jsonl'
    events = [json.loads(line) for line in journal.read_text().splitlines() if line.strip()] if journal.exists() else []
    event = next((e for e in reversed(events) if e.get('stage') == key), None)
    if event and event.get('status') == 'selected' and event.get('reviewer') == 'user' and event.get('decision') == 'waived':
        return event['id']
    if not event or event.get('status') != 'passed' or event.get('reviewer') != 'user':
        raise RuntimeError(f'{key}: waiting for explicit user acceptance of the review artifact')
    if not event.get('outputs'):
        raise RuntimeError(f'{key}: approval has no bound review artifact')
    for ref in event.get('inputs', []) + event['outputs']:
        path = (root / ref['path']).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise RuntimeError(f'{key}: missing or invalid bound file {ref["path"]}')
        with path.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        if digest != ref['sha256']:
            raise RuntimeError(f'{key}: {ref["path"]} changed after review; revisit this checkpoint')
    return event['id']


def self_test():
    import tempfile
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'experiments/001_heavy_box'))
    from journal import append_event
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory); (root / 'preview.mp4').write_bytes(b'review candidate')
        args = dict(stage='checkpoint/revision/staging', intent='Review staging', method='Test input', result='Test decision', outputs=['preview.mp4'])
        def blocked():
            try: require_checkpoint(root, 'revision', 'staging')
            except RuntimeError: return
            raise AssertionError('An unapproved or stale checkpoint passed')
        blocked()
        append_event(root, status='pending_review', **args); blocked()
        append_event(root, status='passed', reviewer='assistant', **args); blocked()
        approved = append_event(root, status='passed', reviewer='user', **args)
        assert require_checkpoint(root, 'revision', 'staging') == approved['id']
        (root / 'preview.mp4').write_bytes(b'changed scene'); blocked()
        append_event(root, status='passed', reviewer='user', **args)
        append_event(root, status='rejected', reviewer='user', **args); blocked()
        waived = append_event(root, status='selected', reviewer='user', decision='waived', **args)
        assert require_checkpoint(root, 'revision', 'staging') == waived['id']
        print('PASS: absent, pending, agent-only, changed and rejected reviews block; current user acceptance and explicit user waiver pass')


if __name__ == '__main__':
    if sys.argv[1:] == ['--self-test']:
        self_test()
    elif len(sys.argv) == 4:
        try: print(require_checkpoint(*sys.argv[1:]))
        except (ValueError, RuntimeError, OSError) as error: sys.exit(str(error))
    else:
        sys.exit('Usage: checkpoints.py FILM_ROOT REVISION STAGE | --self-test')

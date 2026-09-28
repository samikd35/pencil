"""Image catalogue and explicit, version-pinned visual selection for a Pencil film."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
STYLES = ROOT / 'styles'
sys.path.insert(0, str(ROOT.parent / 'experiments/001_heavy_box'))
from journal import append_event


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def catalogue():
    data = json.loads((STYLES / 'catalog.json').read_text())
    ids = [option['id'] for option in data['options']]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate style IDs')
    for option in data['options']:
        for field in ('recipe', 'sample'):
            path = (STYLES / option[field]).resolve()
            if not path.is_relative_to(STYLES) or not path.is_file():
                raise ValueError(f'Missing or unsafe {field}: {option["id"]}')
        reference = option.get('reference', {})
        if any(not isinstance(reference.get(key), str) or not reference[key].strip()
               for key in ('title', 'creator', 'credit', 'source_url', 'image_url')):
            raise ValueError(f'Missing reference attribution: {option["id"]}')
        for key in ('source_url', 'image_url'):
            url = urlsplit(reference[key])
            if url.scheme != 'https' or not url.netloc:
                raise ValueError(f'Unsafe reference URL: {option["id"]}')
        targets = reference.get('quality_targets')
        if not isinstance(targets, list) or len(targets) < 3 or any(not isinstance(t, str) or not t.strip() for t in targets):
            raise ValueError(f'Missing visible quality targets: {option["id"]}')
    return data


def select(production, style_id, *, replace=False, reviewer='assistant', reason):
    production = Path(production).resolve()
    original = production.read_bytes()
    plan = json.loads(original)
    if not isinstance(plan, dict) or not isinstance(plan.get('timeline'), dict):
        raise ValueError('Use an existing production plan with a timeline')
    data = catalogue()
    options = {o['id']: o for o in data['options']}
    if style_id not in options:
        raise ValueError(f'Unknown style: {style_id}')
    if not reason.strip() or reviewer not in ('user', 'assistant'):
        raise ValueError('Record the actual reviewer and reason for selection')
    previous = plan.get('visual_style')
    if previous and previous.get('id') == style_id and not replace:
        return resolve(production)  # Resume the pinned version, never silently upgrade it.
    if previous and not replace:
        raise ValueError('Film already has a style; use --replace for an explicit revision')
    option = options[style_id]
    folder = production.parent / 'assets' / 'style-selections'
    folder.mkdir(parents=True, exist_ok=True)
    index = 1
    while (folder / f'v{index:03}').exists():
        index += 1
    revision = folder / f'v{index:03}'
    # All referenced inputs exist before modifying the production plan.
    payloads = {
        'recipe.md': (STYLES / option['recipe']).read_bytes(),
        'construction.md': (STYLES / 'construction.md').read_bytes(),
        'sample.png': (STYLES / option['sample']).read_bytes(),
        'option.json': (json.dumps(option, indent=2) + '\n').encode(),
        'build_samples.py': (STYLES / 'build_samples.py').read_bytes(),
        'character_layers.py': (ROOT / 'character_layers.py').read_bytes(),
    }
    revision.mkdir()
    for name, content in payloads.items():
        (revision / name).write_bytes(content)
    selected = dict(id=style_id, catalog_version=data['version'],
                    settings=option['settings'], reviewer=reviewer, reason=reason,
                    files={name: dict(path=str((revision/name).relative_to(production.parent)),
                                     sha256=digest(revision/name)) for name in payloads})
    # Snapshot the exact choice so staging can bind it without binding unrelated audio edits.
    selection_file = revision / 'selection.json'
    selection_file.write_text(json.dumps(selected, indent=2) + '\n')
    # Stable current-choice path makes changed selections invalidate bound visual checkpoints.
    # Versioned recipe/snapshot files still preserve the exact prior decision.
    current = production.parent / 'assets' / 'style-selection.json'
    selected['selection_path'] = str(current.relative_to(production.parent))
    selected['selection_sha256'] = digest(selection_file)
    plan['visual_style'] = selected
    (revision / 'production-before.json').write_bytes(original)
    if production.read_bytes() != original:
        raise ValueError('Production changed during selection; retry against the current plan')
    # ponytail: one producer writes a film at a time; use a film-wide lock if concurrent writers are introduced.
    for target, content in ((current, selection_file.read_bytes()), (production, (json.dumps(plan, indent=2)+'\n').encode())):
        with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as stream:
            stream.write(content); temporary = Path(stream.name)
        temporary.replace(target)
    append_event(production.parent, stage='visual-style', status='selected',
                 intent='Choose the visual treatment for this production',
                 method='Pinned reference image, source and quality targets in option.json, recipe and construction guide',
                 result=reason, decision=style_id, reviewer=reviewer,
                 outputs=[str(selection_file.relative_to(production.parent)), str(current.relative_to(production.parent))])
    return selected


def resolve(production):
    production = Path(production).resolve()
    selected = json.loads(production.read_text()).get('visual_style')
    if not selected:
        raise ValueError('No visual style selected; show the image gallery first')
    refs = list(selected['files'].values()) + [dict(path=selected['selection_path'], sha256=selected['selection_sha256'])]
    for ref in refs:
        path = (production.parent / ref['path']).resolve()
        if not path.is_relative_to(production.parent) or not path.is_file() or digest(path) != ref['sha256']:
            raise ValueError(f'Selected style input missing or changed: {ref["path"]}')
    snapshot = json.loads((production.parent / selected['selection_path']).read_text())
    if any(selected.get(k) != value for k, value in snapshot.items()):
        raise ValueError('Production style differs from its pinned selection; explicitly reselect')
    return selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('list')
    sub.add_parser('validate')
    get = sub.add_parser('resolve'); get.add_argument('production', type=Path)
    put = sub.add_parser('select'); put.add_argument('production', type=Path)
    put.add_argument('style_id'); put.add_argument('--replace', action='store_true')
    put.add_argument('--reviewer', choices=['user', 'assistant'], default='assistant')
    put.add_argument('--reason', required=True)
    args = parser.parse_args()
    try:
        if args.command in ('list', 'validate'):
            data = catalogue()
            print('\n'.join(f'{o["id"]}: {o["name"]} — {o["status"]}' for o in data['options']))
        elif args.command == 'resolve':
            print(json.dumps(resolve(args.production), indent=2))
        else:
            print(json.dumps(select(args.production, args.style_id, replace=args.replace,
                                    reviewer=args.reviewer, reason=args.reason), indent=2))
    except (ValueError, KeyError, OSError) as error:
        parser.exit(1, f'Style selection: {error}\n')


if __name__ == '__main__':
    main()

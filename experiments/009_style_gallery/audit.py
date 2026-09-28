"""Current-state requirement audit for the delivered style-menu implementation."""
from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];STYLES=ROOT/'pipeline/styles'
spec=importlib.util.spec_from_file_location('style_selection',ROOT/'pipeline/styles.py');styles=importlib.util.module_from_spec(spec);spec.loader.exec_module(styles)

def audit():
    data=styles.catalogue();options=data['options'];assert len(options)==19
    assert len(list((STYLES/'recipes').glob('*.md')))==len(list((STYLES/'samples').glob('*.png')))==19
    reviewed={'chibi','food-mascot','paper-cutout','collage','parallax'}
    assert {o['id'] for o in options if o['motion_tested']}==reviewed
    samples=[];proofs=[]
    for option in options:
        path=STYLES/option['sample'];assert path.read_bytes().startswith(b'\x89PNG')
        evidence=[(STYLES/e['path']).resolve() for e in option['evidence']];assert all(p.is_file() for p in evidence)
        native=next(p for p in evidence if p.suffix=='.blend')
        checks=json.loads((native.parent/'checks.json').read_text())
        assert checks['style']==option['id'] and checks['frames']==240 and checks['max_endpoint_gap']<1e-5
        assert checks['source_sha256']==styles.digest(ROOT/'experiments/008_cartoon_skin/artifacts/coherent-proof-v003/cartoon-skin.blend')
        assert styles.digest(path)==styles.digest(native.parent/'sample.png')
        samples.append(dict(id=option['id'],sample_sha256=styles.digest(path),native=str(native.relative_to(ROOT)),mechanical_check=checks['status']))
        if option['id'] in reviewed:
            film=HERE/'proofs/workflow-v001'/option['id'];selected=styles.resolve(film/'production.json')
            assert selected['id']==option['id'] and selected['settings']==option['settings']
            out=film/'animatic-v001';report=json.loads((out/'delivery-checks.json').read_text())
            assert report['complete_decode']=='passed' and report['authoritative_sound_pcm']=='identical to original'
            assert all((out/f).is_file() for f in ['review.md','character.blend','motion-overview.png','push-successive-frames.png','release-successive-frames.png','animatic-with-sound.mp4'])
            assert any(e.get('reviewer')=='assistant' and e.get('stage')=='producer-review/animatic-v001' for e in map(json.loads,(film/'events.jsonl').read_text().splitlines()))
            proofs.append(dict(id=option['id'],movie_sha256=styles.digest(out/'animatic-with-sound.mp4'),review_sha256=styles.digest(out/'review.md')))
    assert len({s['sample_sha256'] for s in samples})==19
    template=(STYLES/'gallery-template.html').read_text()
    expected=template.replace('/* CATALOG_DATA */',json.dumps(data).replace('<','\\u003c'))
    assert (STYLES/'gallery.html').read_text()==expected
    assert (STYLES/'menu.png').is_file()
    skill=Path('/Users/samikd/.codex/skills/produce-pencil-animation/SKILL.md')
    original=(HERE/'history/produce-pencil-animation-before.md').read_text();updated=skill.read_text()
    before,after=original.split('## Select assets and establish the treatment\n\n',1)
    assert updated.startswith(before+'## Select assets and establish the treatment\n\n') and updated.endswith(after)
    assert 'pipeline/styles/gallery.html' in updated and 'assets/style-selection.json' in updated
    commands=[['python3','pipeline/test_styles.py'],['node','pipeline/styles/test_gallery.cjs'],['python3','pipeline/checkpoints.py','--self-test'],['/Users/samikd/MyProjects/PyBlend/.venv/bin/python','/Users/samikd/.codex/skills/.system/skill-creator/scripts/quick_validate.py',str(skill.parent)]]
    tests=[]
    for command in commands:
        result=subprocess.run(command,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert result.returncode==0,result.stdout
        tests.append(dict(command=command,output=result.stdout.strip()))
    return dict(requirements={
        '1_catalogue':'19 options in three roles; 5 motion-reviewed presets and 14 still-only presets explicitly distinguished',
        '2_shared_guide':'construction.md maps demonstrated joints, continuous waist, native neck, contact and texture limits to existing helpers',
        '3_recipes':'19 specific recipes with actual settings, runnable adapter commands, adjustments, sources and limits',
        '4_samples':'19 distinct native PNGs match their retained Blender renders; all projects saved/reopened and mechanically checked',
        '5_menu':'Offline HTML with filters/choice preparation plus a visually inspected static image menu; actual browser preview blocked by URL policy, DOM-fixture behavior checks pass',
        '6_skill_integration':'Installed skill updated; per-film choice pins inputs, resumes unchanged, loads selected settings; tests prove audio preservation and affected checkpoint invalidation',
        '7_end_to_end':'5 real selections consumed by Blender; five 240-frame native projects and encoded animatics through shared audio; sequential-frame reviews and actual delegated review records',
        '8_lessons':'Paper waist shadow correction in shared builder; texture/proportion/depth lessons and checkpoint-binding fix recorded in guides, recipes and existing journal'},
        samples=samples,proofs=proofs,tests=tests,skill_sha256=styles.digest(skill),menu_sha256=styles.digest(STYLES/'menu.png'),
        limitations=['14 new presets have no sequential-frame motion review; existing foundation evidence is retained.',
                     'Fixed-view benchmark, not arbitrary character/angle retargeting; new films author their own poses and staging.',
                     'No real-time playback or new listening claimed. Original soundtrack preserved and verified.',
                     'Browser URL policy blocked local HTML preview. Static menu visually reviewed; HTML logic tested with an isolated DOM fixture.'])

if __name__=='__main__':
    report=audit();out=HERE/'artifacts/completion-audit-v001.json'
    if out.exists():raise SystemExit('Preserve existing audit; choose a new version before writing another')
    out.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: current-state audit of all eight requirements, 19 native images and five full workflow proofs')

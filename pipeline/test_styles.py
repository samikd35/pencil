"""Run with python3 pipeline/test_styles.py; exercises real catalogue, selection and checkpoint behavior."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('style_selection',ROOT/'styles.py')
styles=importlib.util.module_from_spec(spec);spec.loader.exec_module(styles)
from checkpoints import require_checkpoint
from journal import append_event


def rejects(call, message):
    try: call()
    except (ValueError, RuntimeError): return
    raise AssertionError(message)


def main():
    data=styles.catalogue()
    assert len(data['options'])==19
    assert data['version']==2
    assert {o['category'] for o in data['options']}=={'Character','Finish','Presentation'}
    for o in data['options']:
        assert (styles.STYLES/o['sample']).read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
        assert all((styles.STYLES/e['path']).is_file() for e in o['evidence'])
    for key,value in [('source_url','javascript:alert(1)'),('quality_targets',[])]:
        invalid=copy.deepcopy(data);invalid['options'][0]['reference'][key]=value
        with patch.object(styles.json,'loads',return_value=invalid):
            rejects(styles.catalogue,'Unsafe or incomplete reference accepted')
    with tempfile.TemporaryDirectory() as folder:
        root=Path(folder);production=root/'production.json'
        original={'version':1,'timeline':{'fps':'24','start_frame':1,'frames':240,'sample_rate':48000},
                  'shots':[{'id':'push','start_frame':1,'events':{'release':146}}],
                  'assets':{'chosen-sound':{'path':'chosen.wav','sha256':'unchanged'}},
                  'cues':[{'id':'keep','gain_db':-4}], 'creative_note':'preserve this too'}
        production.write_text(json.dumps(original))
        rejects(lambda:styles.resolve(production),'Unselected film resolved')
        rejects(lambda:styles.select(production,'../../unknown',reason='Synthetic test'),'Unknown style accepted')
        selected=styles.select(production,'chibi',reason='Synthetic delegated selection for test')
        assert selected['catalog_version']==data['version']
        option=json.loads((root/selected['files']['option.json']['path']).read_text())
        assert option['reference']==next(o for o in data['options'] if o['id']=='chibi')['reference']
        assert (root/selected['files']['sample.png']['path']).read_bytes()==(styles.STYLES/option['sample']).read_bytes()
        assert selected['files']['character_layers.py']['sha256']==styles.digest(ROOT/'character_layers.py')
        actual=json.loads(production.read_text());actual.pop('visual_style');assert actual==original
        before=production.read_bytes();events=(root/'events.jsonl').read_bytes()
        assert styles.select(production,'chibi',reason='Resume test')==selected
        assert production.read_bytes()==before and (root/'events.jsonl').read_bytes()==events
        rejects(lambda:styles.select(production,'flat-vector',reason='Accidental replacement'),'Implicit replacement accepted')
        # Simulate actual-user acceptance only in this temporary fixture, then change style.
        (root/'staging.png').write_bytes(b'synthetic review artifact')
        (root/'sound.wav').write_bytes(b'synthetic sound artifact')
        for stage,files in [('staging',['assets/style-selection.json','staging.png']),('sound',['sound.wav'])]:
            append_event(root,stage='checkpoint/proof/'+stage,status='passed',reviewer='user',
                         intent='Synthetic checkpoint fixture',method='Test fixture',result='Simulated user acceptance',outputs=files)
            require_checkpoint(root,'proof',stage)
        revised=styles.select(production,'flat-vector',replace=True,reason='Explicit test revision')
        assert styles.resolve(production)==revised
        rejects(lambda:require_checkpoint(root,'proof','staging'),'Changed style retained visual approval')
        require_checkpoint(root,'proof','sound')
        assert (root/selected['files']['recipe.md']['path']).is_file()
        selected_plan=json.loads(production.read_text())
        changed=copy.deepcopy(selected_plan);changed['visual_style']['settings']['design']='toast'
        production.write_text(json.dumps(changed))
        rejects(lambda:styles.resolve(production),'Tampered settings accepted')
        production.write_text(json.dumps(selected_plan))
        # Both the chosen artwork and its source/quality criteria are immutable film inputs.
        for name in ('sample.png','option.json'):
            pinned=root/revised['files'][name]['path'];saved=pinned.read_bytes()
            pinned.write_bytes(b'changed reference or target')
            rejects(lambda:styles.resolve(production),'Changed pinned reference accepted')
            pinned.write_bytes(saved)
        layer_helper=root/revised['files']['character_layers.py']['path'];saved_helper=layer_helper.read_bytes()
        layer_helper.write_text('tampered')
        rejects(lambda:styles.resolve(production),'Changed pinned layering helper accepted')
        layer_helper.write_bytes(saved_helper)
        recipe=root/revised['files']['recipe.md']['path'];recipe.write_text('tampered')
        rejects(lambda:styles.resolve(production),'Changed pinned recipe accepted')
    print('PASS: 19 attributed references with quality targets; selected reference/source/criteria are pinned; selection preserves audio/timing/metadata; resume is idempotent; replacement archives inputs and invalidates only bound visual approval; reference and recipe tampering rejected.')


if __name__=='__main__':main()

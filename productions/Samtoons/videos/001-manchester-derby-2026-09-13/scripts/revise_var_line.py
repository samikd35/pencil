"""Directed VAR excuse; reuse the selected local voice runtime and normalization."""
from pathlib import Path
import runpy
ROOT=Path(__file__).resolve().parents[1]
n=runpy.run_path(str(ROOT/'scripts/prepare_film_voices.py'));g=n['main'].__globals__
g['OUT']=ROOT/'assets/film-voices-v003'
g['CAST']={'VAR':(g['CAST']['VAR'][0],171)}
g['ROWS']=[('var','VAR','Onside. No touch. Enzo was sleeping. Goal.',
'An officious British official issuing a ludicrously overconfident verdict. ONSIDE. NO TOUCH. Then dismiss the objection with smug certainty: ENZO was SLEEPING. A short deliberate pause, then an emphatic final GOAL. Dry comic finality, crisp authoritative diction, no soft fading endings.')]
if __name__=='__main__':n['main']()

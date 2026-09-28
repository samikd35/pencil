"""New acted takes for the rejected full-cast energy; retain prior selections."""
from pathlib import Path
import runpy
ROOT=Path(__file__).resolve().parents[1]
n=runpy.run_path(str(ROOT/'scripts/prepare_film_voices.py'));g=n['main'].__globals__
g['OUT']=ROOT/'assets/film-voices-v002'
directions={
'morning': 'Buoyant greeting from a supremely pleased footballer: warm smiling MORNING, then affectionate confident PEP. Slight comic certainty, brief and conversational, no announcer cadence.',
'less-problem': 'An overconfident captain delighted that an opponent has gone. Exhale relieved ONE LESS, then smug satisfied PROBLEM. A private little victory, not narration.',
'contract': 'A cartoon goalpost who believes he is the star goalkeeper. Booming theatrical TWO SAVES! A beat of smug self admiration, then an imperious brisk demand: I WANT A NEW CONTRACT. Grand and funny, strong consonants.',
'var': 'An officious British official issuing a ludicrously overconfident verdict. Three crisp stamps of authority: ONSIDE. NO TOUCH. GOAL. No uncertainty, no soft fading endings, dry comic finality.',
'ours': 'A goalkeeper gasping in startled relief after a near miss. OURS WORKS TOO! Sudden delighted discovery, incredulous upward lilt and a smile, projected to his teammates.',
'surely': 'A football captain holding his breath as the last chance opens up. A tense hopeful SURELY, then a very brief pause and pleading NOW. Vulnerable suspended expectation, not a bored flat murmur.',
'wolf': 'A smug striker warmly praising his goalkeeper like a very good dog. Low playful GOOD, then affectionately amused WOLF. Short and dry, with a smile in the voice.',
'thanks': 'Cheerful victorious gratitude, completely oblivious that he has the wrong name. Bright THANKS with an affectionate pleased PEP, compact and naturally conversational.',

'and-him': 'A sharp indignant stadium shout to a distant referee: AND HIM?! Fast explosive attack on HIM, genuinely outraged, upward snap at the end. Project across the pitch.',
'fishing': 'Petulant cartoon footballer storming off: spit out FINE with a grumpy punch, quick irritated breath, then announce I am going FISHING with exaggerated wounded dignity. Keep it brisk.',
'him': 'Angry captain yelling an urgent objection over a celebrating crowd. WHAT ABOUT HIM?! Abrupt, strongly projected and incredulous; land HIM as an accusation.',
'yes': 'A triumphant footballer yelling at the top of his lungs after a goal. One explosive YEEEES! with a rough joyous attack, sustained ecstatic shout and forceful finish. Big celebration, not spoken agreement.',
'enzo': 'The wrong name again! A furious comic coach abruptly barking ENZO! with chest pressure, a gravelly explosive EHN and an emphatic ZOH. This is a sudden outburst that interrupts a relaxed scene.',
'pep-two': 'Earnest comic robot footballer who thinks he has found a brilliant answer. Deadpan PEP, deliberate TWO POINT, then a bright proud OH! Small thoughtful pause, sincere delight, dry comic confidence.',
'biting': 'Cheeky young Mancunian enjoying his secret prank. Intimate amused aside with an audible grin: KEEP GOING, REF! then a short conspiratorial pause and delighted THEY ARE BITING. Playful smug pleasure, not a flat statement.'}
g['ROWS']=[(slug,person,words,directions[slug]) for slug,person,words,_ in g['ROWS'] if slug in directions]
g['CAST']={p:(voice,seed+117) for p,(voice,seed) in g['CAST'].items()}
if __name__=='__main__':n['main']()

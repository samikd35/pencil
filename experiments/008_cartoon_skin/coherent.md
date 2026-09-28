# Coherent character proof

User authorized implementation after the head/waist research. Built 14 September 2026 as a small visual and motion experiment; awaiting user review.

[Play](artifacts/coherent-proof-v003/cartoon-with-sound.mp4) · [Previous/new comparison](artifacts/coherent-proof-v003/previous-to-coherent.mp4) · [Three poses](artifacts/coherent-proof-v003/three-poses.png) · [Editable scene](artifacts/coherent-proof-v003/cartoon-skin.blend)

The face is native flat meshes and curves: short dark hair, an angular jaw, brows, eyes, a nose and animated mouths. No head image is used. Its detail and line weight now fit the elastic body. The white number 7 kit, small badge and captain band carry additional reference cues. This is an intentionally simplified likeness, not an accepted character identity.

The waist is no longer a stack of separately outlined shirt/hip/shorts shapes. Live torso and shorts fills share a compositor alpha mask, with one external border around their combined silhouette. Derived hip and shoulder attachments give the fuller body width without adding animated control tracks. Sleeves, shorts, socks and hands remain editable native geometry.

The existing 12 controls match on every one of 240 frames after reopening the saved scene. Projected hand/shoe geometry is unchanged, all limb endpoints remain attached and a temporary hand edit moves the sleeve correctly. See [geometry checks](artifacts/coherent-proof-v003/checks.json) and [movie checks](artifacts/coherent-proof-v003/video-checks.json). The source scene is unchanged. Original sound is copied and checked against decoded source audio.

Visual inspection covers standing, deep push and raised-arm recovery plus an exported motion sheet. Numerical checks and selected frames do not establish full subjective playback acceptance. The same-camera test does not establish turns, crossed-limb occlusion or realistic anatomy. The body union is composited in front of the sleeve layer, so different depth ordering needs a separate review. Its one-pixel border is sized for this 640×360 proof and would need scaling for a larger export. This is native curve/mesh animation, not a Grease Pencil armature. The box action is fictional.

The first build stopped on a Blender 5.2 compositor API change. The second revealed old keyed facial artwork and an always-visible mouth outline. The third puts superseded artwork in a hidden collection and synchronizes the effort outline with its mouth state. Earlier candidates and logs remain available.

Reproduce with a fresh output name:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python experiments/008_cartoon_skin/build_coherent.py -- --out coherent-proof-v004
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python experiments/008_cartoon_skin/build_skin.py -- --out coherent-proof-v004 --render
python3 experiments/008_cartoon_skin/finish_proof.py coherent-proof-v004
```

The original `build_skin.py` and `build_ronny.py` supply existing geometry helpers. This adds one experiment script, with no new rig framework or dependencies. The reproduction commands create the scene and original-stickman comparison; the previous-character comparison and pose sheet are review assemblies.

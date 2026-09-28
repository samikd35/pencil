# Seamless 2D cartoon construction: primary-source notes

Researched 2026-09-13. Bounded source note for the Ronny box experiment, not a recommendation to change applications or buy software. No animation has been modified.

## Main finding

The documented techniques treat **animation controls, deforming artwork, and visible joint boundaries as separate concerns**. A working skeleton does not determine which overlapping outlines should be visible. The useful transferable pattern is to preserve simple motion controls, draw continuous flexible forms where possible, and deliberately hide internal construction lines where parts must remain separate.

That is an inference from the sources below. They document specific implementations; they do not prove that an automatic union, mask, deformer, or patch will fix every pose in Blender.

## Six useful primary sources

### 1. Toon Boom: Auto-Patch hides a joint line while retaining the outer contour

[How does the Auto-Patch node work?](https://helpcentre.toonboom.com/hc/en-ca/articles/45598439632275-How-does-the-Auto-Patch-node-work), official Help Centre, updated 21 July 2026.

- **Verified mechanism:** Separate line and colour art; the node cuts the colour art with its own line art. Compositing that patch above another part obscures the underlying joint line without covering the full part's intended boundary.
- **Documented limits:** The simple setup assumes parts do not change Z-depth. Depth changes require a more involved patch arrangement. The article warns that inverted cutters can produce anti-aliasing problems.
- **Transferable lesson:** Two parts can share a joint perfectly and still display a bad seam. Visibility of the construction boundary is its own problem. For the fixed-view box test, deliberate fill overlap plus a controlled visible contour is a relevant idea; copying a large node system is unnecessary.

### 2. Toon Boom: curve deformation deliberately supports rubber-hose limbs

[About Curve Deformation](https://learn.toonboom.com/modules/deformation-rigging/topic/about-curve-deformation), official Learn Portal.

- **Verified mechanism:** Bézier controls reshape artwork into flowing curves. Although useful for hair and facial features, the documentation also identifies limbs in early rubber-hose animation as an intended use.
- **Documented style boundary:** The characteristic is a flowing limb without a hinged elbow or wrist. A curve deformer is not an anatomical joint solver.
- **Transferable lesson:** Fuller colour and silhouette can be added around the existing flexible limb path without introducing a separately outlined upper arm and forearm. Cartoon appearance need not imply segmented construction.
- **Access note:** Official search-index text was available; direct page fetching returned HTTP 403 during this research. No tutorial video was viewed.

### 3. Battle Axe: visual style and bending are explicitly independent

[Rubberhose 3 — Styles](https://battleaxe.co/rubberhose/docs/styles), official documentation.

- **Verified mechanism:** A hose is built from a shape layer. Style presets combine strokes, fills, trims, ellipses, layer styles, and effects. Bend presets adjust bend behavior and do not set colour or thickness.
- **Limit:** This is a method for styling supported shape-layer artwork. It does not promise that arbitrary detailed art becomes a convincing deformable character.
- **Transferable lesson:** Keep the proven bend behavior; develop a consistent drawing style around it. Stroke width, silhouette, sleeve length, cuff treatment, and palette can define a simple cartoon without replacing the motion model.

### 4. Battle Axe: the path's bend shape matters independently of joint positions

[Rubberhose 3 — Controls](https://battleaxe.co/rubberhose/docs/controls), official documentation.

- **Verified mechanism:** A hose bends as its endpoints come closer than its length. Roundness adjusts bend tangents from sharp to smooth, while the Realism setting changes the softness of straightening.
- **Documented distinction:** RubberRig's straight bone layers stretch between bend points and do not understand the curve tangent handles; Roundness therefore does not affect RubberRig in the same way.
- **Transferable lesson:** A smooth path and several rigid segments are not visually equivalent, even when their endpoints match. Retaining continuous paths is particularly relevant to the working box motion. Future more anatomical styles may need different bend profiles, not merely more surface detail.

### 5. Lost Marble: Moho documents both seam patches and authored deformation correction

[Moho 13.5 Users Manual](https://www.lostmarble.com/manual/13.5/Moho%20Users%20Manual.pdf), official manual, Smart Bones around printed pages 103–104; Patch Layers at printed page 201.

- **Verified mechanism:** Patch Layers hide overlapping outlines where separately drawn body parts connect. Smart Bones can control point motion, curvature, line width, colour, and layer transformations as a bone moves.
- **Limit:** Patching resolves line visibility; corrective deformation addresses how a shape bends. They solve different problems. Neither alone supplies a consistent character design.
- **Transferable lesson:** If a particular extreme bend still needs help after simpler construction is fixed, author a small correction for that pose rather than repeatedly changing the whole rig.
- **Access note:** Verified through official indexed manual excerpts, including the patch description on page 201. Direct full-PDF retrieval by the web tool exceeded its content-size limit. This is historical version documentation, used for the construction technique rather than current product availability.

### 6. Lost Marble: Smart Bones require the desired result to be authored

[Moho — Features](https://moho.lostmarble.com/pages/features), official product documentation, Smart Bones / Curvers / Vitruvian Bones sections.

- **Verified mechanism:** A Smart Bone is given an action whose elements are animated into the desired behavior. Curvers bend vectors or images and can animate width. Alternate drawings and bone sets support different perspectives through Vitruvian Bones.
- **Limit:** The page contains marketing claims about effortless results; these are not independent evidence of reliability. The described workflow still requires authored artwork and actions. Supporting a new view is distinct from preserving a fixed-view bend.
- **Transferable lesson:** Keep a small set of intentional corrections or replacement drawings as a later option. They are preferable to assuming one drawing must solve every extreme pose or angle automatically.

## Application to the current questions — design inference

1. **Head/body mismatch:** None of these rigging mechanisms chooses a coherent rendering style. Simplify the head's shapes, line treatment, shading, and detail density to belong to the same flat cartoon as the body. The recognizable cues can remain hair silhouette, eyebrows, jaw, and expression. This is a design recommendation, not a claim made by the software manuals.
2. **Waist:** Use the local code diagnosis to determine which outlines are redundant. The evidence supports intentionally suppressing interior construction lines, not outlining every overlapping shirt/waist/shorts part. Keep the shirt hem only where it communicates a real garment boundary.
3. **Motion:** Preserve the existing motion first. A continuous limb shape, a coherent torso/hip silhouette, and deliberately owned contour lines are the smallest relevant experiment. Test standing, deepest push, crouch, reach, and recovery in silhouette and colour before adding kit details.
4. **Boundary:** This research supports a promising fixed-view construction approach. It does not establish universal seam-free behavior, camera turns, or a tested Grease Pencil implementation.

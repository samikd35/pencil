# Additional visual directions for the existing simple 2D rig

Researched 14 September 2026. These sources establish the visual directions or production methods; they do **not** validate this project's exact Blender rig. Feasibility below is an engineering assessment of our native curves, flat meshes, layered fills and simple body/hand/foot controls. No new style was built or tested during this research.

## Project evidence and combined catalogue

Reviewed `experiments/008_cartoon_skin/README.md`, `build_trio.py`, the coherent character notes and GP comparison. Existing evidence covers stick figures, fuller elastic cartoons, a flat native character and three exaggerated caricatures in the fixed-view box action. Control/endpoint checks establish connections for those proofs; they are not blanket evidence for every character, angle or pose.

| Direction | Short description | Work needed in this project |
|---|---|---|
| Expressive stick figures | Sparse lines and expressive gestures. | Existing tested construction. |
| Rubber-hose cartoons | Rounded elastic limbs; vintage styling is optional. | Existing elastic motion; artwork for a vintage treatment. [Adobe](https://www.adobe.com/uk/creativecloud/animation/discover/rubber-hose-animation.html) |
| Flat vector cartoons | Solid fills, clean outlines and simple clothes. | Existing tested construction. |
| Exaggerated caricatures | Identity cues with enlarged or distorted proportions. | Existing trio motion proof; likeness refinement and new expressions still needed. |
| Chibi / super-deformed | Oversized heads and very small bodies. | New artwork and pose tuning. [Clip Studio's drawing guide](https://www.clipstudio.net/how-to-draw/archives/155423) |
| Geometric characters | Circles, rectangles and triangles form the character. | New artwork; reuse simple limb controls. [Adobe's puppet examples](https://pages.adobe.com/character/en/puppet-maker) |
| Object / food mascots | Objects or food become characters with faces and limbs. | New artwork and attachment locations; keep simple limbs. [Adobe's puppet examples](https://pages.adobe.com/character/en/puppet-maker) |
| Emoji / rounded mascots | Simple rounded bodies with prominent expressions. | New artwork; additional facial states need authoring. [Adobe's puppet examples](https://pages.adobe.com/character/en/puppet-maker) |
| Upright animal mascots | Animals using a simple two-legged body. | New artwork; animated ears/tails need added controls. [Adobe's puppet examples](https://pages.adobe.com/character/en/puppet-maker) |
| Doodle / ink / pencil appearance | Loose-looking, sparse linework. | Line-art variant is direct; grain and line boil need an added treatment. [Toon Boom texture node](https://docs.toonboom.com/help/harmony-25/premium/reference/node/filter/animate-pencil-line-texture-node.html) |
| Silhouette / shadow style | Solid shapes communicate through poses. | New fills and careful overlap staging. [Reiniger's own account, BFI](https://www.bfi.org.uk/sight-and-sound/features/scissors-make-films-lotte-reiniger-creating-her-magical-animations) |
| Digital paper-cutout look | Layered paper-like shapes. | Art/material changes; rigid hinged limbs would need a limb variant. [Adobe](https://www.adobe.com/uk/creativecloud/animation/discover/cut-out-animation.html) |
| Midcentury / UPA-inspired | Graphic silhouettes and restrained flat palettes. | New artwork and deliberate pose design; see primary source below. |
| Whiteboard / chalkboard look | Lines appear as though drawn, then can move. | Reveal animation; chalk grain is an additional material treatment. [Adobe whiteboard guide](https://www.adobe.com/creativecloud/video/discover/whiteboard-animation.html), [Blender curve start/end geometry](https://docs.blender.org/manual/en/4.3/modeling/curves/properties/geometry.html) |
| Textured storybook look | Painted, watercolor or gouache-like surfaces. | Added materials/textures and seam testing, while retaining simple contours. |
| Animated collage | Unified paper/photo/illustration cutouts in motion. | Prepared artwork and consistent whole-character surface treatment. [Artist Joseba Elorza's own course](https://www.domestika.org/en/courses/333-animated-collage-with-adobe-after-effects) |
| Retro pixelated look | Blocky rendering of simplified characters. | Native compositor treatment and low-resolution readability checks. |
| Motion-comic presentation | Panels, held poses and selected animated gestures. | Comic art, layout and limited shot-specific motion. |
| Layered 2.5D / parallax | Flat character with depth-separated scenery. | Layer and camera setup; character views stay authored. |

The compatibility judgments above are ours. Examples from Adobe, Toon Boom or Moho are reference evidence, not a recommendation to install or switch to those tools. New artwork remains necessary; large turns, realistic anatomy, foreshortening, complex clothing and precise hands are not established by the current proof. These overlapping categories form a practical catalogue, not an exhaustive formal taxonomy.

## Additional source detail

| Direction | What the source establishes | Fit and remaining work |
|---|---|---|
| **Midcentury / UPA graphic cartoon** | MoMA's contemporary 1955 exhibition describes UPA's flat line drawings, simplified forms and direct, caricatured movement. [MoMA primary exhibition release](https://www.moma.org/docs/press_archives/1959/releases/MOMA_1955_0074_57.pdf) | Strong fit: angular silhouettes, selective outlines, flat color and graphic backgrounds. Art redesign fits current tools; the rig cannot automatically supply every UPA-style pose change or redraw. |
| **Textured storybook illustration** | Moho's official rigged-animation feature page lists watercolor and gouache drawing styles alongside its vector and bone tools. [Moho features](https://moho.lostmarble.com/pages/features) | Feasible with extra material/texture work. Keep simple silhouettes and attach texture consistently. This is a painted appearance, not simulation of actual flowing paint. |
| **Ink / charcoal sketch appearance** | The same official Moho page lists wet ink, rough ink and charcoal styles, and separately documents controlled line boil. [Moho features](https://moho.lostmarble.com/pages/features) | Existing outlines can support an ink-like design; grain, broken strokes and animated wobble require a treatment not presently tested. Could merge this row with doodle/line-art rather than inflate the catalogue. |
| **Retro pixelated appearance** | Blender's native Pixelate compositor node makes image pixels larger and the result blocky. [Blender manual](https://docs.blender.org/manual/en/latest/compositing/types/creative/pixelate.html) | A direct render treatment over the current rig. Call it pixelated or pixel-inspired, not equivalent to deliberately hand-authored pixel animation; silhouettes and small details need low-resolution review. |
| **Collage / fabric-cutout appearance** | NFB describes cutout animation using paper, card and fabric and provides films from its own production archive. [NFB cutout techniques](https://blog.nfb.ca/blog/2018/06/14/animation-techniques-cutout/) | A texture/material variation of the existing paper-cutout category, not an independent rigging system. Flat body shapes can carry consistent whole-character materials; avoid a photo head on an unrelated cartoon body. |

Two additional presentation techniques can combine with these visual styles:

- **Motion comic:** Illustrated panels with selective character movement, held poses and camera framing. [Happy Trails Animation's own motion-comic portfolio](https://www.realmotioncomics.com/) supplies concrete commercial examples. Our inference: reuse the rig for brief gestures and stage comic panels; complex realistic anatomy would still need additional drawings.
- **Layered 2.5D / parallax:** Place foreground and background artwork at different depths and move them at different apparent speeds. [Adobe's layer-depth documentation](https://helpx.adobe.com/animate/desktop/using/layer-depth.html) explains the method. Our inference: compatible with the existing 2D characters, with additional scene/camera setup; this does not give the character a new viewing angle.

For a concise combined catalogue, add UPA, textured storybook, pixelated look and motion comics; list parallax separately as a combinable staging option. Merge sketch with existing doodle/line art and collage with paper cutout to avoid duplicate categories.

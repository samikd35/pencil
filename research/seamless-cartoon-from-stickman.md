# A coherent cartoon that keeps the stickman's movement

13 September 2026. Research in response to the user's rejection of the detailed head and shirt/shorts join in the Ronny box test. **Research and proposed next test only; no revised character or movie produced.**

## Recommendation

Keep the successful hand, foot, body and bend controls. Redesign the entire visible character as one simple drawing language, then decide deliberately which boundaries should be visible. The useful next step is a minimally caricatured, flat cartoon with continuous flexible limbs, a coherent torso/hip shape and very few clothing lines.

The last experiment demonstrated control preservation, but failed the user's visual goal. Rig connectivity and a coherent drawing are separate requirements. More detailed head art and more outlined clothing pieces made the second requirement harder.

## What went wrong in our actual source

| Observed problem | Evidence from our implementation | Consequence |
|---|---|---|
| Head looks pasted on | `build_ronny.py` loads a shaded illustrated head sheet into an image-textured material; the source uses detailed facial modelling and hair texture. The body retains simple flat shapes and mitten hands. | Detail, shape treatment and shading disagree across the character. A smaller head or automatic conversion to Grease Pencil would not, by itself, resolve that difference. |
| Waist looks assembled | `build_skin.py` creates separately outlined `Full shirt` and `Trouser waist` polygons. `build_ronny.py` adds a separate outlined tube section for each shorts leg. | Several construction borders are visible around one small anatomical area. Matching their controller positions does not remove those lines. |
| Thick legs expose the original abstraction | In `build_v005.py`, both legs start at the same body control and both arms use one shoulder anchor. | This is legible with thin stick lines; adding volume makes the shared origins and missing hip shape more conspicuous. |
| Checks passed despite visible problems | Existing checks measure controller equality, endpoint positions, driver validity and selected contacts. | They do not judge whether head and body belong together or whether an unnecessary line reads as a cut. |

The user's phrase “image of his shirt” describes the perceived result. Technically, the shirt is native geometry, not a shirt bitmap. The head is image-based. The defect at the waist is the independent contour construction and overlapping parts.

Local evidence: [screenshot and feedback](../experiments/008_cartoon_skin/assets/feedback-v001/user-feedback.md), [shirt/waist construction](../experiments/008_cartoon_skin/build_skin.py), [head and shorts construction](../experiments/008_cartoon_skin/build_ronny.py), [original limb origins](../experiments/001_heavy_box/scripts/build_v005.py).

## What the primary sources establish

- **Motion and appearance can be designed separately.** Rubberhose documents independent style and bend presets. This supports keeping a working motion mechanism while changing how its paths are drawn. It does not establish that any arbitrary image will deform well. [Battle Axe: Styles](https://battleaxe.co/rubberhose/docs/styles)
- **Internal seams are a compositing/design concern.** Harmony's Auto-Patch documentation describes hiding a joint line while retaining the intended outer contour. Its simple setup has a fixed-depth limitation. This is evidence for explicitly controlling visible boundaries, not a reason to install Harmony or duplicate its full node setup. [Toon Boom: Auto-Patch](https://helpcentre.toonboom.com/hc/en-ca/articles/45598439632275-How-does-the-Auto-Patch-node-work)
- **A fill boundary need not be a visible ink line.** Harmony documents invisible strokes for closing paint regions. Blender Grease Pencil also configures fill and stroke components independently. These capabilities fit a design with clothing colour regions and only the necessary visible seams. [Harmony: invisible strokes](https://docs.toonboom.com/help/harmony-24/essentials/drawing/about-stroke-tool.html), [Blender: materials](https://docs.blender.org/manual/en/latest/grease_pencil/materials/index.html)
- **A flexible curve and hinged anatomy are different styles.** Curve-based deformation is appropriate for rubber-hose movement. More anatomical bending or difficult turns may require authored corrections or replacement drawings. Those are later options, not prerequisites for this fixed-view example. See the [six-source note and access limits](cartoon-construction-primary-sources.md).

These are documented mechanisms. The construction below is our proposed application, not a proven universal solution.

## What to change visually

### 1. Design the head at the body's level of simplicity

Keep the subject's main identity cues: short squared hair shape, eyebrow shape, a simplified nose and jaw, plus the number 7 kit. Translate them into a few deliberate shapes. Use the same outline treatment and flat palette as the rest of the character. Omit hair strands, skin texture, cheek shading and fine facial creases in the first version.

Design the whole standing character together, including head size and neck attachment. A separate head object is acceptable; visual unity does not require a single physical object. Raster artwork is not inherently the cause either—a consistently designed bitmap could work—but the present detailed bitmap does not match this body. Native head shapes would make our next limited set of features directly editable.

### 2. Make the waist one planned shape

Use one coordinated torso-and-hip construction, driven by the existing body control. For the simplest fixed-view proof it can be one body/hip drawing, with shirt and shorts represented by fill regions and a single intentional hem where needed.

Let the upper legs extend beneath the hip fill. Derive two small hip attachment offsets from the existing body control if the fuller silhouette needs them; no separate hip animation track is required. This keeps the hand/foot timing and body action while acknowledging that a wider cartoon body needs attachment width. Exact preservation of every old visible line is not the goal.

Remove the redundant waist rectangle and hidden shorts-top outlines. Keep only the intended outer contour, leg separation and any garment boundary that helps the design. With white shirt and white shorts, several horizontal black rings at the waist provide no useful colour separation.

### 3. Keep continuous limbs, and choose the visible overlaps

Retain the continuous flexible arm and leg paths that already work. Use modest width and controlled taper as needed. Place an intentional cuff only where the garment ends; do not introduce independent upper/lower-arm outlined pieces for this style.

When an arm crosses the torso, the viewer still needs the appropriate front/back relationship. Simply merging every shape and drawing one global outline would erase that information. Use explicit drawing order, bounded fill overlap and selected contour lines. Add a small local mask or correction only if the tested pose needs one.

### 4. Treat the drawing medium as a separate implementation choice

The working Pencil body is made from native Blender curves and flat meshes. Its control mechanism can remain the first implementation of this drawing design. Grease Pencil provides points with thickness, separate fill/stroke settings and layer ordering, but moving the current mismatched art into Grease Pencil would retain the mismatch. A live controls-to-Grease-Pencil implementation would need its own small test; it has not been established here. [Blender: stroke structure](https://docs.blender.org/manual/en/latest/grease_pencil/structure.html), [Blender: drawing layers](https://docs.blender.org/manual/en/latest/grease_pencil/properties/data.html)

## Smallest useful next experiment

1. Draw one coherent, simplified whole-character design with the supplied person's strongest cues. Keep kit detail to the number, collar and a few colour accents.
2. Check the waist construction and silhouette in standing, deep push and raised-arm recovery poses using the existing timing. These poses expose the actual failure more efficiently than another polished still.
3. Review the character in solid silhouette, flat colour and final line art. A hidden shoulder or hip root should remain covered; an intended shirt hem should appear only once.
4. Play a short reach/bend/recovery interval and inspect consecutive frames around contacts and occlusion changes. Verify the familiar endpoint/contact checks as well as the visible seams.

Pass criteria: the head and body look drawn by the same hand; the waist reads as clothing on a body; hands and feet remain attached; contours do not double, flicker or expose construction caps; facial expressions remain readable at viewing size. The next target is a coherent simple cartoon. Semi-realistic anatomy, new camera angles and a universal rig are outside this proposed test.

No new animation, tool installation or production-system rewrite was undertaken in this research pass.

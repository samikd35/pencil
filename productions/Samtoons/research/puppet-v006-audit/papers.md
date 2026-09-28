# Improving the existing v006 2D puppet: primary-source evidence

Researched 23 September 2026. Baseline: [call-performance-v006/call-review.mp4](../../videos/003-barca-emergency-meeting/artifacts/staging-v001/call-performance-v006/call-review.mp4). This is a source review for improving that existing caricature and skeleton. It does not propose replacement 3D characters, a fresh A/B experiment, or a new production. No research implementation was run and no production asset was changed.

**Recommendation:** retain the selected artwork, action and controls; distinguish faulty binding, insufficient bend shape, missing pose artwork, and incorrect overlap/contact before selecting a remedy. Start with explicit part ownership and small authored corrections in the existing shot. BBW or ARAP becomes useful only if the audit identifies deformation errors that those simpler fixes cannot adequately address. Neither is an automatic character designer.

Read alongside the earlier [seam study](../../../../research/seamless-cartoon-from-stickman.md), [construction sources](../../../../research/cartoon-construction-primary-sources.md), and [research-method survey](../animation-methods-v001/papers-and-assistance.md). Those notes' new-comparison and 3D-route proposals do not govern this audit.

## Seven pertinent sources and source families

### 1. Bounded Biharmonic Weights — topology-aware binding

**Established:** Jacobson, Baran, Popović and Sorkine (SIGGRAPH 2011) calculate bounded weights over a discretized shape at bind time, then blend point/bone/cage transformations at pose time. Influence follows the shape's domain rather than merely straight-line distance. Additional constraints can protect a selected feature, demonstrated on an eye. Their locality and absence-of-extra-maxima claims have empirical support, not a general proof. [Authors' paper, §§3–3.4](https://igl.ethz.ch/projects/bbw/bounded-biharmonic-weights-siggraph-2011-compressed-jacobson-et-al.pdf).

**Limit:** weights do not supply missing drawings or contact behavior. A mesh whose connectivity mistakenly bridges an arm and torso gives a topology-aware method the wrong domain. The author's historical demo requires MATLAB and explicitly does not supply 2D texture mapping. Its existence is not evidence of a ready Blender component. [Author's implementation note](https://www.cs.toronto.edu/~jacobson/weblog/1936.html).

**Adoption judgment:** inspect mesh connectivity and anatomical ownership first. For a small cast, explicit local weight assignments may suffice. Consider BBW only for persistent influence leakage or costly hand painting on correctly constructed continuous artwork; solve offline and reuse weights. Do not assume Blender automatic weights implement BBW.

### 2. As-Rigid-As-Possible Shape Manipulation — resistance to distortion

**Established:** Igarashi, Moscovich and Hughes (SIGGRAPH 2005) triangulate a 2D drawing, constrain handles, and minimize triangle distortion through rotation/scale stages. Artwork follows the deformed mesh. The paper separately adds depth handling for overlaps and local rigidity control; overlap is not solved by the distortion objective alone. [Author's project](https://www-ui.is.s.u-tokyo.ac.jp/~takeo/research/rigid/index.html), [paper, §§3, 5](https://www-ui.is.s.u-tokyo.ac.jp/~takeo/papers/rigid.pdf).

**Limit:** preserving local triangle shape is not the same as preserving an appealing caricature silhouette, intentional squash, or a particular sleeve bend. It still manipulates supplied artwork. Its interactive solver is not a documented drop-in Blender modifier.

**Adoption judgment:** relevant to an identified limb/torso shearing problem after construction is correct. Existing skeleton targets could drive its handles, but that is an integration proposal. Avoid introducing a solver merely because a hand needs another drawing or a contour needs an authored correction. Retain separate overlap decisions.

### 3. Pose Space Deformation — authored correctives driven by pose

**Established:** Lewis, Cordner and Fong (SIGGRAPH 2000) map pose parameters to local shape displacements, combining skeletal deformation with sculpted examples. The shape desired by the artist is explicit input. [Author-hosted paper](https://scribblethink.org/Work/PSD/PSD.pdf), [original publication](https://doi.org/10.1145/344779.344862).

**Limit:** the method interpolates supplied examples; it does not discover the correct elbow silhouette, caricature anatomy, expression or unseen view. Its full multidimensional interpolation is more machinery than a single known problem pose requires.

**Adoption judgment:** strongest immediate principle for a recurring bend that still looks wrong with correct weights. Author the desired contour at the existing v006 extreme and activate a local corrective smoothly from the relevant control. Use a direct driver/shape key for a simple case; introduce multidimensional pose interpolation only if coupled joints demonstrably require it. A topology-changing open/closed hand or head profile should use suitable alternate artwork instead of forcing a corrective morph.

### 4. 2.5D Cartoon Models — missing views must be represented

**Established:** Rivers, Igarashi and Durand (SIGGRAPH 2010) use vector drawings from multiple views, associate strokes with spatial anchors, and interpolate novel views while retaining deliberate 2D stylization. [Authors' project](https://alecrivers.com/2.5dcartoonmodels/).

**Documented limits:** the paper reports poor interpolation for sharp/concave shapes, a hair failure, unsupported partial occlusion, and popping when overlapping strokes change depth order. Additional key views can reduce some failures. [Paper, §6](https://www.alecrivers.com/2.5dcartoonmodels/files/2.5D%20Cartoon%20Models.pdf).

**Adoption judgment:** use the principle of authored view coverage, not the complete historical system. For the selected shot, add only the hand orientation, facial arrangement or head angle actually absent from the current art. Align anchors and choose the switch interval deliberately. A rotation of the same front drawing cannot reveal an unseen side; conversely, slight in-plane motion does not require a new view. The supplied designer is a historical Windows/.NET application, not a verified local Blender route.

### 5. Toon Boom Harmony — shape, attachment and drawing substitutions are separate controls

**Established:** Harmony's Shape-Aware Deformation builds a triangle mesh from artwork; influence respects that mesh's boundary. Disconnected empty areas provide no mesh unless an appropriate matte supplies one. [Deformation Mesh](https://docs.toonboom.com/help/harmony-24/premium/deformation/deformation-mesh.html).

Its Deformer on Deformer system separates convenient centreline controls from envelope controls of the outer shape. Kinematic Output lets a hand follow an arm endpoint without inheriting unwanted deformation. Drawing Substitutions selects authored art at a frame. [Deformer on Deformer](https://docs.toonboom.com/help/harmony-24/premium/master-controller/about-deformer-on-deformer.html), [rigging drawings to deformations](https://docs.toonboom.com/help/harmony-24/premium/deformation/about-rigging-with-deformers.html), [drawing substitutions](https://docs.toonboom.com/help/harmony-24/advanced/cut-out-animation/swap-drawing-picker-view.html).

**Limit:** these are documented Harmony mechanisms, not evidence of automatic Blender equivalence. The earlier Auto-Patch source already establishes the distinct job of hiding construction seams; patching does not fix a poor bend or grip.

**Adoption judgment:** keep skeleton controls, but allow independent contour correction. Separate the wrist attachment transform from the hand's shape, and select a grip drawing whose fingers actually hold the relevant prop. Assign visible contour ownership at the sleeve/hand and head/neck joins. This can be implemented locally without migrating applications or reproducing Harmony's whole node system.

### 6. Blender — practical mechanisms already available

**Established:** Armature vertex groups give explicit bone-to-vertex influence. Preserve Volume reduces rotational collapse but has a documented discontinuity around 180°; it is not an assertion that a flat cartoon's silhouette will remain correct. [Blender 5.2 Armature modifier](https://docs.blender.org/manual/id/5.2/modeling/modifiers/deform/armature.html).

Relative shape keys support corrective poses, and the driver documentation demonstrates correcting an elbow from its pose. Smooth Corrective reduces distortion but can itself lose volume; boundary pinning only prevents smoothing boundary vertices. It does not create a target contour. [Shape keys](https://docs.blender.org/manual/ar/5.2/animation/shape_keys/introduction.html), [corrective drivers](https://docs.blender.org/manual/nl/5.2/animation/drivers/workflow_examples.html), [Smooth Corrective](https://docs.blender.org/manual/id/5.2/modeling/modifiers/deform/corrective_smooth.html).

Child Of supports animatable attachment influence and an inverse transform for preserving offsets. That supports prop attachment but does not determine finger contact or automatically preserve a smooth pickup/release. [Child Of](https://docs.blender.org/manual/en/latest/animation/constraints/relationship/child_of.html).

**Adoption judgment:** prefer the existing control structure, explicit groups, limited correctives and scheduled drawing/occlusion changes. A planar mesh remains a 2D puppet; using mesh shape keys does not require volumetric characters. If existing shapes are rebuilt procedurally every frame, corrections must enter that authoritative builder or a deliberate persistent representation—the modifier alone will not fix competing sources of geometry. Confirm the actual construction before choosing either path.

### 7. Generative Cutout Animation — what automated asset construction actually demonstrates

**Established:** Puhachov, Aigerman, Groueix and Bessmeltsev (Eurographics 2026) generate rigged cutout images from skeletal animation and a text prompt, optimizing appearance across target poses. The authors demonstrate editable, reusable cutouts. This is closer to structured puppet generation than raster-video synthesis. [Author's project](https://puhachov.xyz/publications/generative-cutout-animation/), [paper](https://doi.org/10.1111/cgf.70422).

**Limit:** the representation deliberately uses rigid illustrated pieces that translate/rotate in the view plane. The inspected evidence does not establish preservation of the selected v006 caricature, a working Mac/Blender implementation, expressive grip changes, or seamless deforming joints. The inspected author page did not provide runnable code or a Blender importer.

**Adoption judgment:** do not substitute this for the accepted character or introduce it as a production dependency. Its useful lesson is to assess artwork against several actual skeletal poses while constructing it. Existing art plus targeted missing drawings is the direct route for this revision.

## Application to v006 — inference, to be reconciled with the source/visual audit

| Concern | Smallest relevant change | What code can reliably organize |
| --- | --- | --- |
| Image/reference construction | Preserve the approved identity; author only missing hidden extensions, grip, expression or view artwork | Crop/registration, consistent pivots, asset naming, placement and switches; not artistic correctness |
| Topology-aware binding | Separate overlapping anatomical parts in the deformation domain; use explicit permitted influences | Weight assignment, normalization and forbidden-influence checks; BBW only if justified |
| Silhouette under bending | Adjust contour control and a small pose corrective before increasing rig complexity | Repeated poses and correction activation; not a universal silhouette guarantee |
| Changed pose/view | Substitute suitable artwork when topology/visible features change | Hold/switch timing and matched anchors; inspect adjacent frames for popping |
| Occlusion | Define which part owns each visible contour and which lies in front at the actual crossing | Depth/visibility schedule and masks; no assumption that static depth solves every pose |
| Contact | Use a common attachment frame during the hold, with authored approach, closure and release | Transform/offset consistency and contact-distance checks; a correct wrist target does not prove a believable grip |

The next implementation, if requested, should repair the diagnosed failures in **the selected v006 shot** and compare identical frames and playback intervals. Technical measurements can flag influence leakage, degenerate triangles, attachment drift and sudden switches; they cannot certify likeness, appeal, expressive acting or world-class quality. Those require inspecting the rendered result.

## Evidence boundaries

This review read the existing notes and inspected original papers, author pages and official documentation. Some full-paper fetches were intermittent; the 2.5D limitations were available through indexed text of the authors' PDF. Blender's English latest pages sometimes failed fetching, so versioned official pages containing English body text were used. No software, model, add-on or paper code was installed or run; no claim of local performance or production quality follows from publication examples. Reported mechanisms and our adoption judgments are distinguished above.

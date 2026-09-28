# Experiment 011 — Dawn Training

User-directed complete 30-second Grease Pencil cutout short, created 7 September 2026. The five supplied fighter sheets are the design authority. The output is an editable Blender project and rendered first cut, not a certification of the broader PyBlend two-character/four-motion matrix.

The user's explicit request for this standalone simple cutout film determines this experiment's scope. ADR 0002's broader platform certification remains outstanding; this experiment neither resumes nor claims completion of that platform gate.

## Deliverable

`artifacts/dawn_training/Dawn_Training.blend`, `Dawn_Training.mp4` and `BEGINNER_GUIDE.md`.

Three final Blender scenes: independent neutral character studio, five-pose test scene, and the six-shot film. Native Grease Pencil contours are bone-parented by named layers. No raster image planes are used for visible character artwork. Reference images are packed image empties. Effects and scenery are editable geometry.

## Reproduce

From the PyBlend repository:

```sh
.venv/bin/python experiments/011_dawn_training/prepare_art.py
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python experiments/011_dawn_training/build_project.py
.venv/bin/python experiments/011_dawn_training/make_sound.py
/Applications/Blender.app/Contents/MacOS/Blender --background artifacts/dawn_training/Dawn_Training.blend --python-exit-code 1 --python experiments/011_dawn_training/render_film.py
ffmpeg -y -framerate 24 -i artifacts/dawn_training/frames/frame_%04d.png -i artifacts/dawn_training/Dawn_Training_Sound.wav -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -t 30 -movflags +faststart artifacts/dawn_training/Dawn_Training.mp4
/Applications/Blender.app/Contents/MacOS/Blender --background artifacts/dawn_training/Dawn_Training.blend --python-exit-code 1 --python experiments/011_dawn_training/validate_project.py
```

`prepare_art.py` copies the original Desktop references into the package, records SHA256 values, extracts the silhouette, applies explicit semantic ownership, and creates layered SVG artwork. It uses the installed NumPy, Pillow, OpenCV and VTracer packages. `build_project.py` imports SVG through Blender's native importer, builds and animates the rig, and saves inspection renders. `make_sound.py` generates original sound. `render_film.py` packs assets and renders 720 frames.

Build scripts overwrite this experiment's outputs. Preserve edited Blender projects under a new filename before rebuilding. The existing unrelated PyBlend files and Git changes are left intact.

## Review status and limits

This is a complete first-cut implementation with technical verification, not a user-approved final artistic master. Five pose variants and the two additional camera/view variants retain the supplied artwork; they are pose-specific cutouts with matching control names, not a single deformable 360-degree character. The artwork is a vector reconstruction of low-resolution source sheets; small ink contours retain source limitations. Substantial new rotations and stronger poses require correction drawings. No model training, neural reconstruction, cloud animation service, mocap, cloth simulation or automatic skin weighting is involved.

See [RESEARCH.md](RESEARCH.md) for source-verified mechanisms, locally observed failures and what was changed.

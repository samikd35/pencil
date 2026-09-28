# Character Package V2 contract

Character Package V2 is PyBlend's canonical, versioned character-animation
input. It is validated before Blender runs. Rendered frames and `.blend` files
are derived artifacts, not the source of truth.

## Required manifest

The JSON root contains:

- `schema_version`: exactly `pyblend.character-package.v2`;
- `package_id`, `status`, canvas information, and hashed source provenance;
- one or more named views;
- per-view semantic owners with separate hashed artwork;
- a skeleton with explicit joint positions, fixed rest lengths, and an explicit
  foreshortening decision for every bone;
- deformation domains referencing existing owners and bones;
- joint packages containing attachment coverage, hidden artwork, local
  front/back ownership, and any approved correctives;
- explicit occlusion edges and topology events; and
- certification state and Creator-approved scope.

An action package may also declare hashed `actions[*].timing` assets. Action
timing is separate from each deformation domain's shared cage/mesh geometry.

Owner artwork cannot be shared by two owners. Every referenced file must remain
inside the repository root and match its SHA-256 digest. Bone rest lengths must
match the declared rest-joint geometry within the frozen `0.5%` Character
Package acceptance threshold.

`candidate` means the structure and provenance are internally valid but still
require visual review. Only a `certified` package with explicit Creator
approval may enter reusable motion and deterministic Blender compilation.

## Validation

```sh
PYTHONPATH=src python -m pyblend.character_package path/to/package.json --root .
```

The command exits nonzero and reports all detected errors. It intentionally
does not judge visual quality; automatic validation only rejects candidates.

## Current proof boundary

Ticket 04 must first build two static front-view candidate packages and pass
their joint-extreme review. Generated full-body poses may enter a package only
as explicitly approved, pose-owned Alternate Drawings that compile to editable
Blender geometry. V6 TPS geometry and rendered Blender output cannot become
canonical package authority.

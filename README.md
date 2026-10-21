# US License Plate Generator — v1.1

- `US_LicensePlates_v1_1.blend`: the Geometry Nodes preset (Blender 5.2)
- `marketing/instagram/`: 1080×1350 carousel slides + `marketing/instagram_captions.md`
- `marketing/superhive/`: 1920×1080 gallery images + `marketing/superhive_listing.md`
- `tools/`: the headless Blender scripts used to make v1.1 from v1.0 and to render the images
  (`modify.py` → interface / frame / slogans, `shaders.py` → dirt & flies, `r_*.py` → renders, `compose.py` → layouts)

## v1.1 changes
See the changelog in `marketing/superhive_listing.md`.

## Backbone truck sim (`tatra-sim/index.html`)

A browser driving game covering every axle and drive layout of a central-tube backbone truck,
from 4×2 to 16×16. Open the file in a browser (it loads Three.js from jsDelivr).

- **Chassis:** a central backbone tube built from the axle housings. Each wheel hangs on its own
  swing half-axle pivoting on the tube centreline, so camber changes as it articulates. Tandem rear
  axles share one rocking leaf spring per side; the other axles are sprung individually.
- **Configurations:** 2–8 axles, any split between the front and rear groups, and a drive/steer
  toggle on every axle. `[` / `]` steps through all 501 axle-count × driven-axle combinations.
- **Drivetrain:** open, inter-axle-locked or fully locked differentials, high and low range.
- **Courses:** axle twister, hill (40–70 % grades), trenches, logs, mud.

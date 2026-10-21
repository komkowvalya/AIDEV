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
from 4×2 to 16×16. Open the file in a browser (it loads Three.js from jsDelivr). Plan and checklist: `tatra-sim/PLAN.md`.

- **Chassis:** a silver central backbone tube built from flanged axle housings, with a finned transfer case
  between the groups. Each wheel hangs on its own swing half-axle pivoting on the tube centreline, sprung by an
  air bellows with a coil spring. Steered axles carry kingpin knuckles, split tie rods, relay levers and drag links;
  fixed axles carry rigid hubs and reaction rods. Tandem air springs are linked, so the load equalises.
- **Truck:** a faceted Force-style cab (no manufacturer logo), body choices, five paints.
- **Configurations:** 2–8 axles, any front/rear split, drive and steer toggles on every axle; `[` / `]` step through
  all 501 combinations. Front, rear, full (all-wheel) and crab steering.
- **Drivetrain:** open, inter-axle-locked or fully locked differentials, high and low range.
- **World:** golden-hour sky, five courses (axle twister, 40–70 % hill, trenches, logs, mud), dust and tyre tracks.
- **Font:** the UI asks for Interstate first and falls back to Overpass, since Interstate is a commercial font that
  cannot be bundled. Put `interstate.woff2` next to the page and add an `@font-face` rule to use your licensed copy.

# US License Plate Generator — v1.1

- `US_LicensePlates_v1_1.blend`: the Geometry Nodes preset (Blender 5.2)
- `marketing/instagram/`: 1080×1350 carousel slides + `marketing/instagram_captions.md`
- `marketing/superhive/`: 1920×1080 gallery images + `marketing/superhive_listing.md`
- `tools/`: the headless Blender scripts used to make v1.1 from v1.0 and to render the images
  (`modify.py` → interface / frame / slogans, `shaders.py` → dirt & flies, `r_*.py` → renders, `compose.py` → layouts)

## v1.1 changes
See the changelog in `marketing/superhive_listing.md`.

## Backbone truck sim (`tatra-sim/index.html`)

A browser driving game for a central-tube backbone chassis, from 4×2 to 16×16. Open the file in a browser
(it loads Three.js from jsDelivr). Plan and checklist: `tatra-sim/PLAN.md`.

- **Maps:** a digital twin of the Tatra proving ground in Kopřivnice, and the original test courses.
  The polygon layout is traced from an aerial photo and snapped to the asphalt, scaled so the speed circuit's middle lane is
  1 600 m. Track specs come from the TATRA test-area brochure: banked 3-lane speed circuit, skid pad, eight special
  roads (torsion, bending, setts, low-adhesion, sinusoidal, river cobbles, pavé, Belgian blocks, shallow ford,
  lateral stability), panel road, noise road, steep slopes from 16 to 65 %, deep and mud fords, abrasive road,
  slope circuit and terrain circuit. A chip shows the name and spec of the track you are on.
- **Chassis only:** silver-grey backbone tube with flanged axle housings and a transfer case; swing half-axles in trumpet
  housings, each with an air bellows (rolling-lobe on steered axles, double-convoluted on fixed ones). Steered axles carry
  kingpin knuckles, split tie rods, relay levers and drag links; fixed axles carry rigid hubs and reaction rods.
- **Configurations:** 2–8 axles, any front/rear split, drive and steer toggles on every axle; `[` / `]` step through all
  501 combinations. Front, rear, all-wheel and crab steering. Open, inter-axle-locked or fully locked differentials,
  high and low range.
- **Performance:** no post-processing, pixel ratio 1, 2048 px shadows.
- **Font:** the UI asks for Interstate first and falls back to Overpass (Interstate is commercial and is not bundled).
- `tatra-sim/map/`: the aerial-photo trace (`trace.py`), the snapping and export scripts, and the generated `polygon.json`.

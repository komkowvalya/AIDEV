# Backbone Truck Sim v2: plan and checklist

Reference: the video can't be downloaded from this environment (WeTransfer is blocked by the
network policy), so the chassis follows the published layout of Tatra T815-7 / Force chassis.

## A. Chassis model (high detail, Tatra layout)
- [x] A1 Central backbone tube: segments with bolted end flanges joining the axle housings
- [x] A2 Driven axle housing: differential casting with a bevel-gear bulge, top cover, bolt rings, swing-pin bosses
- [x] A3 Non-driven axle housing: plain coupling section with the same swing bosses and no differential bulge
- [x] A4 Swing half-axles: tapered tubes with a swing collar at the backbone pivot and a hub-reduction housing and brake drum at the outer end
- [x] A5 **Steered axle** hardware: kingpin yoke, rotating knuckle, steering arm, split tie rods to a relay lever on the backbone, drag link between steered axles, steering cylinder, telescopic damper (torsion bar replaced by the air spring, see G2)
- [x] A6 **Non-steered axle** hardware: fixed hub, brake chamber, spring seat, reaction rod; air spring and damper (the leaf spring was replaced after the reference frames, see G2)
- [x] A7 Front-mounted engine (V8 block, banks, turbo, pulley), bell housing, gearbox / transfer case joining the tube
- [x] A8 Auxiliary C-section frame, crossmembers and mounts; fuel tank, air tanks and battery box
- [x] A9 High-detail wheels: lathe-profiled tyre with directional chevron lugs, dished steel rim, wheel nuts, hub-reduction cap, CTIS valve
- [x] A10 Hardware reflects the config: steer toggles swap knuckle/torsion hardware against fixed hub/leaf/bellows hardware live

## B. Vehicle body: Force-style cab
- [x] B1 Rounded, beveled cab shell with raked windscreen, side windows, door seams and handles
- [x] B2 Large black grille with bars, bumper headlamps with LED daytime strips, fog lamps, heavy bumper, skid plate and tow eyes
- [x] B3 Sun visor, roof beacon and marker lamps, mirrors on arms, access ladder, grab handles, wheel-arch flares
- [x] B4 Behind the cab: air-intake snorkel, exhaust stack with heat shield (spare wheel dropped to match the reference photo, see G6)
- [x] B5 Cargo body: aluminium dropside with stake posts, optional tarp, rear guards, mudflaps, underrun bar, tail lamps
- [x] B6 Clear-coated paint with colour choices

## C. Crab drive and steering modes
- [x] C1 Steering modes: Normal (front group), All-wheel (counter-phase), Crab (all axles in phase)
- [x] C2 Crab mode needs every axle steerable; switching to it fits knuckles on all axles and says so
- [x] C3 Key (K) and UI control; HUD and schematic show the mode and crab angle

## D. Modern environment
- [x] D1 Physical sky with sun, image-based lighting from the sky, ACES tone mapping, soft high-res shadows
- [x] D2 Post-processing: multisampled render target, subtle bloom on lamps and sun, plus a quality toggle
- [x] D3 Terrain: high-res mesh near the courses, low-res far mesh, tiled detail and normal textures, slope/rock/mud splat colours
- [x] D4 Wind-animated instanced grass, instanced conifers and rocks, distant mountain ring
- [x] D5 Proving-ground dressing: concrete start pad with markings, illuminated course gates, marker posts, textured logs, standing water in the mud
- [x] D6 Effects: dust and mud particles from the tyres, tyre tracks

## E. Modern game UI
- [x] E1 Title screen with a start button
- [x] E2 Restyled HUD: speed gauge, gear/range, steering mode, diff state, inclinometer, traction
- [x] E3 Minimap with courses and the truck
- [x] E4 Garage panel: layout, per-axle drive/steer with hardware labels, all 501 configs, presets, steering, drivetrain, paint, body, teleport, graphics
- [x] E5 Camera modes: chase, chassis (body hidden, drivetrain highlighted), cinematic, cab, top; X-ray
- [x] E6 Engine sound (after the start click), mute toggle; touch controls on phones

## F. Keep from v1
- [x] F1 Same swing-axle physics, tandem equalising, disc tyre contact, diff modes, low range, 4×2 to 16×16, all 501 configs
- [x] F2 Stable on every course in the automated drive test

## G. Match the reference frames (added after the user sent stills and a Force photo)
- [x] G1 Chassis finish like the video: silver alloy castings and tube; driven parts highlighted in red
- [x] G2 Air bellows with coil springs on every half-axle (replacing leaf packs and torsion bars); tandem bellows stay pneumatically linked (load equalising)
- [x] G3 Central transfer case mid-tube; H-shaped frame-mount brackets on the backbone; reaction rods on fixed axles; steering cylinder on steered axles
- [x] G4 Block-tread off-road tyres; slotted rims in body colour
- [x] G5 Faceted Force-style cab from the photo: chamfered shell, peaked visor, raised nose panel with blank round badge and mesh grilles, faceted bumper with 3-LED lamp clusters, front axle under the door
- [x] G6 Behind-cab modules from the photo: snorkel with box head, diamond-mesh module, round air filter; black arch fenders on every wheel; khaki paint
- [x] G7 Rear-only steering works (video "4×4 Rear steering"); caption reads Front / Rear / Full / Crab steering
- [x] G8 UI in the video's style: black panels, white type, red accent, big red "8×8" + steering caption over a white wireframe top view
- [x] G9 Typeface: Interstate first in the stack (used where installed; it is commercial and cannot be embedded), Overpass as the free fallback. **Partial:** Interstate itself is not shipped.
- [x] G10 Golden-hour light, drier ground, scattered stones and bushes like the video

## Verification (headless Chromium, software GL)
- Automated drives: 4×4, 8×8, 10×10, 16×16 on every course; no NaN, no rollovers, all reach the course end except
  the 4×4 in mud with open diffs (stuck, as intended) and the 16×16 on the 70 % crest (long-wheelbase breakover).
- Crab: 16×16 at −17° steer travels at −17.7° with heading held at 1.3°. All-wheel turns a full circle in 8 s
  where normal steering turns 140°. 4×4 rear-only steering turns.
- 216 configurations built in all three steering modes without errors; no horizontal overflow at 390 px.
- Not verified: frame rate on a real GPU, keyboard feel.

# v3 plan (polygon digital twin, chassis only, performance)

Sources: the user's aerial photo of the polygon (layout traced and snapped to the asphalt; scale from the
1 600 m middle lane of the speed circuit, 1.022 m/px), the TATRA test-area brochure (track specs and the
location of every special road on its site maps), and web sources (21–22 km of roads, 60 ha, built from 1967).
The real road geometry from OpenStreetMap could not be fetched from this environment.

## H. Map: Tatra polygon digital twin
- [x] H1 Road network traced from the aerial photo: speed circuit, measuring straights, access roads, slope
      circuit, serpentine, off-road circuit loops and forest tracks, spoon and teardrop loops, links
- [x] H2 Speed circuit: 3 lanes (inner 5 %, middle 7.5 %, outer 10 % banking), on an 8–10 % hillside, lane lines, guard rail
- [x] H3 Skid pad: Ø 100 m with marked circles r 20/30/40 m, entry from the oval; moose-test cones on the oval
- [x] H4 Special roads in the band inside the oval (400 m × 4 m lanes): torsion (100 m, ±43 cm, ±20 % cross slope),
      bending (120 m, ±0.7 m waves), setts 10×10 (±3 cm), low-adhesion basalt (140 m, μ≈0.25), sinusoidal resonance
      (20 mm × 300 mm @ 770 mm, part at 40°), river cobbles (≤10 cm), pavé (±10 cm, both tracks shifted 20 m),
      Belgian setts with 7 cm potholes, shallow ford (0.2 m), lateral-stability road (230 m, cross slope 0→57.7 %)
- [x] H5 Panel road: 450 m × 6 m arc inside the oval, 3 m panels with random offsets
- [x] H6 Noise road (ISO 10844) in the vehicle park; vehicle park with parked trucks
- [x] H7 Steep slopes in granite setts: 16, 17, 22, 30, 45, 65 % (**simplified:** each is a mound whose crest is capped at 8 m; the real ramps climb the hillside)
- [x] H8 Deep water ford (60 m, 10 % ramps, water set to 1.0 m of the possible 2 m), mud ford (50 m, 7.5 % ramps, 0.1–0.4 m mud), abrasive road (15 %, coarse aggregate)
- [x] H9 Terrain from the photo: forest mask from the photo's colours, factory halls, hillside elevation
- [x] H10 Zone chip: shows the name and spec of the track you are on
- [x] H11 Minimap drawn from the road network; teleports to every section
- [x] H12 Simple, modern, minimal look: pale terrain, grey roads, white buildings, rounded trees, gradient sky

## I. Chassis only
- [x] I1 Cab, body, frame and engine removed; chassis only
- [x] I2 Air bellows per wheel station on every axle (rolling-lobe on steered axles, double-convoluted on fixed ones), brackets from the housings, no coil springs
- [x] I3 Geometry closer to the reference render: trumpet half-axle housings, gunmetal castings with a cast-surface texture, light rims
- [x] I4 X-ray without drive shafts or gears

## J. UI and performance
- [x] J1 Performance mode only: no post-processing, pixel ratio 1, 2048 shadows, no grass
- [x] J2 Simplified HUD: one compact bar, config card, minimap, zone chip; keys behind a help button
- [x] J3 Simplified garage: map, layout, configurations, steering, drivetrain, places, view
- [x] J4 Keep the test-courses map as a second map

## Not modelled or approximate in v3
- Tipper circuit, dynamic test lab, cab impact rig and presentation centres (buildings are plain blocks).
- Speed-circuit curve radii: the brochure gives R 327–335 m; the model follows the shape in the aerial photo.
- The special-road band follows the 7.5 % hillside; the brochure calls those roads level straights.
- Positions of the fords, abrasive road and ramps come from the brochure's small site maps, so they are approximate.

## v3 verification (headless Chromium, software GL)
- Drives: speed circuit at 96 km/h; special lanes, torsion, lateral-stability (30°, no rollover); 16 %, 45 %, 65 % slopes
  climbed by 8×8; a 4×2 stalls just below the 65 % crest from standstill; deep ford wading 0.59 m; mud ford; 16×16 on
  the terrain circuit; crab on the skid pad. Courses map still builds and drives.
- Render load: about 450 draw calls and 1.6 M triangles on the polygon map, with no post-processing and pixel ratio 1.

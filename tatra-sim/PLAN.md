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

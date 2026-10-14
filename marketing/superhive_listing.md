# License plate generator - USA

**Title:** License plate generator - USA
**Short description:** Geometry Nodes generator for US license plates. All 50 states + DC, any number, easy bend, plastic frame and dirt in one modifier.
**Category:** Models › Vehicles  ·  Geometry Nodes
**Tags:** license plate, number plate, usa, us, america, geometry nodes, car, vehicle, procedural, generator, emboss

---

## License plate generator - USA

Create a **real US license plate for any state and any number** in a few clicks.
The generator builds the actual plate geometry: the embossed letters, the border, the mounting slots and the bend. It is **not a texture**, so it holds up in close-ups.

Presets for **all 50 states + Washington DC** are included. Each one has its own artwork, state name, slogan, font and colors. Pick a plate, type your number, and you're done.

### Easy bend
Use the **BEND** slider to wrap the plate around any bumper. The letters, border, frame and stickers bend together with the plate.

### Any number, any font
- Type the **WRITING** (and an optional second **NUMBER** group)
- 6 built-in plate fonts, or plug in **your own font**
- **Embossed** letters with adjustable height, or set the height to 0 for **flat printed** plates (AZ, GA, TX, PA…)
- State symbols as separators: **Florida orange, Georgia peach, Pennsylvania keystone, New Mexico Zia**

### Plastic frame with your text
One switch adds a **dealer-style plastic frame**. It has a top line and two bottom lines for your own text, which always fit inside the frame. Optional **chrome screws** included.

### Dirt & flies
One click ages the plate with **road grime, mud speckles and squashed bugs**. The dirt builds up toward the bottom and the edges, and it is randomized per object, so no two plates look the same.

### Beginner friendly
The modifier panel shows only what you need, grouped into **Plate · Registration · State · Border & Stickers · Colors · Frame & Dirt**.
US standard dimensions (12" × 6", 7" × 4¾" slot spacing) are built in, so nothing can be broken by accident.

### Colors
Separate colors for **letters, plate tint, state name, slogan and border**. They are stored as attributes, so you can recolor every plate from the modifier.

---

### What's included
- `US_LicensePlates_v1_1.blend` with 51 ready-to-use plates (50 states + DC) plus a start plate
- Geometry Nodes generator `LicensePlate_US_Base`
- Plate artwork for every state + a `CUSTOM` backplate you can replace with your own image
- Registration sticker and 4 state separator symbols
- Materials work in **EEVEE and CYCLES**, separated by material (letters, state, slogan, border, plate, frame…)

### Requirements
- Blender **5.2** or newer

### Notes
- The geometry is quite dense (embossing needs it), so it isn't suitable for game assets. Lower **RESOLUTION** for lighter plates.
- Plate artwork is a stylized recreation of each state's standard-issue plate. It doesn't copy the official files.
- The fonts are open-source (Google Fonts, OFL / Apache 2.0). If you want the exact official state fonts, check their licenses separately.
- The license allows commercial use in your renders and animations. Reselling the generator, or plates made with it as stand-alone assets, is not allowed.

### Changelog
**1.1**
- Simplified modifier panel: plate size, radius, thickness, hole layout, registration layout and header layout are now fixed to the US standard
- One registration sticker with a single position input (month sticker and sticker wells removed)
- Rebuilt the plastic frame: proper lip around the plate, wider bottom bar, and the dealer text always fits on the frame
- New dirt & flies shader: road grime, mud speckles and squashed bugs instead of dots
- Slogans updated to the current plates: Alabama (WWW.ALABAMA.TRAVEL), Washington DC (header WASHINGTON, DC), Kansas (TO THE STARS), North Dakota (PEACE GARDEN STATE), Oklahoma (EXPLORE OKLAHOMA)

**1.0**
- Initial release

---

### Gallery image order
1. `superhive/01_cover.png`: main thumbnail
2. `superhive/02_all_states.png`: all 51 plates
3. `superhive/03_features.png`: bend, frame, dirt, any number
4. `superhive/04_panel.png`: modifier panel
5. `superhive/05_sep.png`: state symbols
6. `superhive/06_embossed.png`: embossed close-up

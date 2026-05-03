# Ghostface Mobile Web Prototype

A browser/mobile prototype for a 2D horror slasher game using the modern pixel-art Ghostface-inspired sprite sheet.

## Run

```bash
cd /home/deck/ghostface-mobile-prototype
python3 -m http.server 8788
```

Open:

```text
http://127.0.0.1:8788/
```

On another device, replace `127.0.0.1` with this machine's LAN IP.

## Controls

### Mobile
- Left virtual joystick: move
- SLASH button: attack
- DASH button: quick evade

### Desktop
- WASD / Arrow keys: move
- Space: attack
- Shift: dash

## Prototype Loop

Collect all phones while avoiding the hunters. Every cleared level immediately rolls into a harder one with more phones, faster enemies, and additional hunters. Slashing can damage, defeat, and briefly stun hunters; defeated hunters increment the HUD counter and respawn after a short delay. Dash gives a short invulnerability window. If you die, the run restarts completely from level 1 so the game can be played infinitely.

## Files

- `index.html` — single-page game prototype using transparent pixel-art atlas assets
- `assets/uploaded-ghostface-v20/ghostface_uploaded_v20_idle_192x144.png` — runtime player idle atlas extracted only from Nate's uploaded 6×6 Ghostface sheet, transparent RGBA, 6 frames
- `assets/uploaded-ghostface-v20/ghostface_uploaded_v20_walk_192x144.png` — runtime player walk atlas extracted only from Nate's uploaded sheet, transparent RGBA, 6 frames
- `assets/uploaded-ghostface-v20/ghostface_uploaded_v20_run_192x144.png` — runtime player run atlas extracted only from Nate's uploaded sheet, transparent RGBA, 6 frames
- `assets/uploaded-ghostface-v20/ghostface_uploaded_v20_attack_192x144.png` — runtime player slash atlas extracted only from Nate's uploaded sheet row 4, transparent RGBA, 6 frames with baked sheet slash poses/effects; no procedural slash particles are used
- `assets/uploaded-ghostface-v20/ghostface_uploaded_v20_hurt_death_192x144.png` — runtime player hurt/death atlas extracted only from Nate's uploaded sheet, transparent RGBA, 6 frames
- `assets/uploaded-ghostface-v20/source_uploaded_ghostface_sheet.jpeg` — Nate's uploaded source sheet used for every runtime player Ghostface frame
- `assets/uploaded-ghostface-v20/asset_manifest.json` — source, grid, cell sizes, pivots, frame metadata, and import notes for the uploaded-sheet-only runtime player assets
- `scripts/build_uploaded_ghostface_v20.py` — reproducible extraction script for rebuilding the transparent atlases from the uploaded source image
- `assets/detailed-transparent/ghostface_detailed_96x96.png` — prior cohesive player movement atlas, transparent RGBA, 4 frames, kept as fallback/reference
- `assets/detailed-transparent/ghostface_detailed_attack_96x96.png` — prior cohesive player attack atlas, transparent RGBA, 4 frames, kept as fallback/reference
- `assets/detailed-transparent/guard_detailed_80x80.png` — guard/hunter atlas with translucent flashlight cone, transparent RGBA, 4 frames
- `assets/detailed-transparent/wall_tiles_detailed_64x64.png` — transparent RGBA wall tile variants, 4 frames/tiles
- `assets/detailed-transparent/phone_detailed_32x32.png` — glowing phone pickup atlas, transparent RGBA, 3 frames
- `assets/detailed-transparent/asset_manifest.json` — cell sizes, pivots, frame counts, and import notes for runtime assets
- `assets/modern-transparent/ghostface-modern-sheet-transparent-clean.png` — cleaned version of the prior modern Ghostface sprite sheet with true PNG RGBA transparency, kept as concept/reference
- `assets/modern-transparent/ghostface_modern_clean_96x96.png` — normalized movement strip from the modern sheet, transparent RGBA, kept as reference because it looked too cutout-like against the pixel-art world
- `assets/modern-transparent/ghostface_modern_clean_attack_96x96.png` — normalized attack strip from the modern sheet, transparent RGBA, kept as reference
- `assets/modern-transparent/asset_manifest.json` — source, cell sizes, pivots, and import notes for the remade modern sheet
- `assets/ghostface-modern-sheet.png` — original generated sprite sheet source/reference with baked checkerboard preview background
- `assets/ghostface-modern-sheet-cutout.png` — older transparent cutout concept/reference sprite sheet

## Notes

The player runtime art now uses `assets/uploaded-ghostface-v20/`, extracted only from Nate's uploaded 6×6 Ghostface sprite sheet. The baked checkerboard preview background was removed into true PNG alpha, each player state uses the matching uploaded-sheet row (idle, walk, run, attack, hurt/death), and the attack no longer has separate in-engine slash particles or old/generated Ghostface frames mixed in. Use nearest-neighbor filtering and the pivots documented in the manifests if importing these assets into another engine.

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
- `assets/modern-fit/ghostface_modern_fit_clean_v13_96x128.png` — runtime player movement atlas remade from the preferred modern sheet, transparent RGBA, 4 frames, full head-to-toe body visible in 96×128 cells; versioned filename forces mobile browsers past cached phantom sprites
- `assets/modern-fit/ghostface_modern_fit_attack_v15_96x128.png` — runtime player attack atlas with phantom-cleaned full-body modern cells and a clean 4-frame reference-style pose sequence: wind-up, active lunge, follow-through, recovery
- `assets/modern-fit/asset_manifest.json` — source, cell sizes, pivots, frame counts, and import notes for the runtime modern-fit player assets
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

The player runtime art now uses `assets/modern-fit/`, a refit of the preferred modern Ghostface sheet that was tested before deployment: true alpha transparency, a taller 96×128 full-body frame so the head, robe, legs/feet, and knife stay visible, a muted palette that matches the guard/world, hard alpha edges, and separate in-engine slash FX instead of the weaker baked-in modern attack effects. The unmodified cleaned modern sheet remains in `assets/modern-transparent/` as source/reference, and the previous detailed cohesive atlas remains in `assets/detailed-transparent/` as fallback/reference. Use nearest-neighbor filtering and the pivots documented in the manifests if importing these assets into another engine.

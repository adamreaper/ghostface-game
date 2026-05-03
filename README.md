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
- `assets/modern-transparent/ghostface-modern-sheet-transparent-clean.png` — cleaned version of the prior modern Ghostface sprite sheet with true PNG RGBA transparency
- `assets/modern-transparent/ghostface_modern_clean_96x96.png` — runtime movement strip remade from the modern sheet, transparent RGBA, 4 frames
- `assets/modern-transparent/ghostface_modern_clean_attack_96x96.png` — runtime attack strip remade from the modern sheet, transparent RGBA, 4 frames
- `assets/modern-transparent/asset_manifest.json` — source, cell sizes, pivots, and import notes for the remade modern sheet
- `assets/detailed-transparent/guard_detailed_80x80.png` — guard/hunter atlas with translucent flashlight cone, transparent RGBA, 4 frames
- `assets/detailed-transparent/wall_tiles_detailed_64x64.png` — transparent RGBA wall tile variants, 4 frames/tiles
- `assets/detailed-transparent/phone_detailed_32x32.png` — glowing phone pickup atlas, transparent RGBA, 3 frames
- `assets/detailed-transparent/asset_manifest.json` — cell sizes, pivots, frame counts, and import notes for guard/wall/phone assets
- `assets/ghostface-modern-sheet.png` — original generated sprite sheet source/reference with baked checkerboard preview background
- `assets/ghostface-modern-sheet-cutout.png` — older transparent cutout concept/reference sprite sheet

## Notes

The player art now returns to the prior modern sprite-sheet style, but the baked checkerboard background has been rebuilt as true PNG alpha transparency. Runtime strips are normalized to 96x96 transparent cells for clean canvas rendering. Use nearest-neighbor filtering and the pivots documented in the manifests if importing these assets into another engine.

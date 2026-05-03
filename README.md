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

Collect all phones while avoiding the hunters. Every cleared level immediately rolls into a harder one with more phones, faster enemies, and additional hunters. Slashing can damage and briefly stun hunters; dash gives a short invulnerability window. If you die, the run restarts completely from level 1 so the game can be played infinitely.

## Files

- `index.html` — single-page game prototype using transparent detailed pixel-art atlas assets
- `assets/detailed-transparent/ghostface_detailed_96x96.png` — detailed Ghostface-inspired movement atlas, transparent RGBA, 4 frames
- `assets/detailed-transparent/ghostface_detailed_attack_96x96.png` — detailed Ghostface-inspired attack atlas, transparent RGBA, 4 frames
- `assets/detailed-transparent/guard_detailed_80x80.png` — guard/hunter atlas with translucent flashlight cone, transparent RGBA, 4 frames
- `assets/detailed-transparent/wall_tiles_detailed_64x64.png` — transparent RGBA wall tile variants, 4 frames/tiles
- `assets/detailed-transparent/phone_detailed_32x32.png` — glowing phone pickup atlas, transparent RGBA, 3 frames
- `assets/detailed-transparent/asset_manifest.json` — cell sizes, pivots, frame counts, and import notes
- `assets/ghostface-modern-sheet-cutout.png` — older transparent cutout concept/reference sprite sheet
- `assets/ghostface-modern-sheet.png` — original generated sprite sheet source/reference

## Notes

The current runtime art is generated as native transparent RGBA pixel art from the start, not cut out from a white/chroma background. Use nearest-neighbor filtering and the pivots documented in `asset_manifest.json` if importing these assets into another engine.

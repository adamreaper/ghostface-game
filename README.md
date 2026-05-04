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

- `index.html` — single-page game prototype using transparent pixel-art atlas assets; includes Safari Add to Home Screen metadata and icon links
- `manifest.webmanifest` — standalone mobile web app manifest for home-screen launch behavior
- `assets/app-icons/apple-touch-icon.png` — 180×180 Safari/iOS home-screen icon using the current uploaded-sheet Ghostface art
- `assets/app-icons/icon-192.png` / `assets/app-icons/icon-512.png` — PWA manifest icons
- `assets/app-icons/favicon-32.png` — browser tab/favicon PNG
- `assets/uploaded-ghostface-v22/ghostface_uploaded_v22_idle_192x144.png` — runtime player idle atlas extracted only from Nate's uploaded 6×6 Ghostface sheet, transparent RGBA, 6 frames repacked on a stable pivot; runtime freezes idle on frame 0 so Ghostface does not drift while standing
- `assets/uploaded-ghostface-v22/ghostface_uploaded_v22_walk_192x144.png` — runtime player walk atlas extracted only from Nate's uploaded sheet, transparent RGBA, 6 frames with stable center/baseline alignment
- `assets/uploaded-ghostface-v22/ghostface_uploaded_v22_run_192x144.png` — runtime player run atlas extracted only from Nate's uploaded sheet, transparent RGBA, 6 frames with stable center/baseline alignment
- `assets/uploaded-ghostface-v22/ghostface_uploaded_v22_attack_192x144.png` — runtime player slash atlas extracted only from Nate's uploaded sheet row 4, transparent RGBA, 6 frames with stable center/baseline alignment; no procedural slash particles or slash camera shake are used
- `assets/uploaded-ghostface-v22/ghostface_uploaded_v22_hurt_death_192x144.png` — runtime player hurt/death atlas extracted only from Nate's uploaded sheet, transparent RGBA, 6 frames with stable center/baseline alignment
- `assets/uploaded-ghostface-v22/source_uploaded_ghostface_sheet.jpeg` — Nate's uploaded source sheet used for every runtime player Ghostface frame
- `assets/uploaded-ghostface-v22/asset_manifest.json` — source, grid, stable-pivot cell sizes, frame metadata, and import notes for the uploaded-sheet-only runtime player assets
- `scripts/build_uploaded_ghostface_v22.py` — reproducible stable-pivot extraction script with disconnected-fragment cleanup for rebuilding the transparent atlases from the uploaded source image
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

The player runtime art now uses `assets/uploaded-ghostface-v22/`, extracted only from Nate's uploaded 6×6 Ghostface sprite sheet. The baked checkerboard preview background was removed into true PNG alpha, each player state uses the matching uploaded-sheet row (idle, walk, run, attack, hurt/death), and every frame is repacked to a stable bottom-center pivot so Ghostface no longer crawls backward/forward while idle or pops during slash. The v22 attack atlas also removes far-away disconnected fragments from neighboring sheet cells so no extra sprite-looking piece clips in during the slash. Runtime draws the player at a reduced `PLAYER_SPRITE_SCALE` so Ghostface sits closer to the enemy scale while keeping the same uploaded-sheet-only art. Idle rendering is locked to frame 0 for a steady standing pose, and attack no longer uses separate in-engine slash particles or slash camera shake. Use nearest-neighbor filtering and the pivots documented in the manifests if importing these assets into another engine.

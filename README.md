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

Collect all 5 phones while avoiding the hunter. Slashing can briefly stun the hunter. Dash gives a short invulnerability window.

## Files

- `index.html` — single-page game prototype with clean built-in pixel-art gameplay sprites
- `assets/ghostface-modern-sheet-cutout.png` — transparent cutout concept/reference sprite sheet
- `assets/ghostface-modern-sheet.png` — original generated sprite sheet source/reference

## Notes

The current sprite is AI-generated and visually strong, but a final production pass should replace it with a hand-cleaned atlas with exact cells, transparent background, and frame-perfect pivots.

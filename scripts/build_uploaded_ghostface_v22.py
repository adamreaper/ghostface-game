#!/usr/bin/env python3
"""Build stable transparent runtime atlases from Nate's uploaded Ghostface sheet only.

v22 fixes v21's visible idle/attack jitter.  The uploaded JPEG's logical grid
places the character at different x positions inside each cell; drawing full
cells made Ghostface crawl backward/forward while standing.  This builder removes
the checkerboard, crops each visible frame, then re-packs every frame around a
consistent pivot so the body stays anchored in-game.
"""
from __future__ import annotations

import hashlib
import json
import struct
import subprocess
import zlib
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'assets' / 'uploaded-ghostface-v22' / 'source_uploaded_ghostface_sheet.jpeg'
OUT_DIR = ROOT / 'assets' / 'uploaded-ghostface-v22'
COLS = 6
ROWS = 6
OUT_W = 192
OUT_H = 144
SCALE = 0.75
ROW_NAMES = ['idle', 'walk', 'run', 'attack', 'crouch', 'hurt_death']
# Per-row baseline keeps feet/body stable but leaves room for big attack/death poses.
TARGET_BOTTOM = {
    'idle': 132,
    'walk': 132,
    'run': 138,
    'attack': 138,
    'crouch': 138,
    'hurt_death': 132,
}
TARGET_CENTER_X = 96


def probe_size(path: Path) -> tuple[int, int]:
    out = subprocess.check_output([
        'ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height', '-of', 'csv=s=x:p=0', str(path)
    ], text=True).strip()
    w, h = out.split('x')
    return int(w), int(h)


def decode_rgba(path: Path) -> np.ndarray:
    w, h = probe_size(path)
    raw = subprocess.check_output([
        'ffmpeg', '-v', 'error', '-i', str(path), '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'
    ])
    return np.frombuffer(raw, dtype=np.uint8).reshape((h, w, 4)).copy()


def write_png(path: Path, rgba: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    h, w, c = rgba.shape
    assert c == 4
    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    scanlines = b''.join(b'\x00' + rgba[y].tobytes() for y in range(h))
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(scanlines, 9))
    png += chunk(b'IEND', b'')
    path.write_bytes(png)


def resize_nearest(img: np.ndarray, new_w: int, new_h: int) -> np.ndarray:
    src_h, src_w = img.shape[:2]
    ys = np.minimum((np.arange(new_h) / (new_h / src_h)).astype(int), src_h - 1)
    xs = np.minimum((np.arange(new_w) / (new_w / src_w)).astype(int), src_w - 1)
    return img[ys[:, None], xs[None, :]]


def exterior_background_mask(cell: np.ndarray) -> np.ndarray:
    rgb = cell[:, :, :3].astype(np.int16)
    mx = rgb.max(axis=2)
    mn = rgb.min(axis=2)
    sat = mx - mn
    bg_like = (mx >= 156) & (sat <= 72)
    h, w = bg_like.shape
    seen = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()
    for x in range(w):
        if bg_like[0, x]:
            q.append((0, x)); seen[0, x] = True
        if bg_like[h-1, x] and not seen[h-1, x]:
            q.append((h-1, x)); seen[h-1, x] = True
    for y in range(h):
        if bg_like[y, 0] and not seen[y, 0]:
            q.append((y, 0)); seen[y, 0] = True
        if bg_like[y, w-1] and not seen[y, w-1]:
            q.append((y, w-1)); seen[y, w-1] = True
    while q:
        y, x = q.popleft()
        for ny, nx in ((y-1,x), (y+1,x), (y,x-1), (y,x+1)):
            if 0 <= ny < h and 0 <= nx < w and bg_like[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True
                q.append((ny, nx))
    return seen


def bbox(alpha: np.ndarray) -> list[int] | None:
    ys, xs = np.where(alpha > 0)
    if len(xs) == 0:
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)]



def connected_components(alpha: np.ndarray) -> list[dict]:
    h, w = alpha.shape
    seen = np.zeros((h, w), dtype=bool)
    comps: list[dict] = []
    for y, x in zip(*np.where(alpha)):
        if seen[y, x]:
            continue
        q: deque[tuple[int, int]] = deque([(int(y), int(x))])
        seen[y, x] = True
        xs: list[int] = []
        ys: list[int] = []
        while q:
            cy, cx = q.popleft()
            xs.append(cx); ys.append(cy)
            for ny in range(cy - 1, cy + 2):
                for nx in range(cx - 1, cx + 2):
                    if 0 <= ny < h and 0 <= nx < w and (not seen[ny, nx]) and alpha[ny, nx]:
                        seen[ny, nx] = True
                        q.append((ny, nx))
        comps.append({'area': len(xs), 'bbox': [min(xs), min(ys), max(xs) + 1, max(ys) + 1]})
    comps.sort(key=lambda c: c['area'], reverse=True)
    return comps


def remove_disconnected_artifacts(frame: np.ndarray) -> tuple[np.ndarray, dict]:
    comps = connected_components(frame[:, :, 3] > 0)
    if not comps:
        return frame, {'components_before': 0, 'removed_components': []}
    main = comps[0]['bbox']
    # Keep the main body and nearby separated parts such as shoes/robe bits.
    # Drop far-away components; those are the "another sprite clipping in" artifacts
    # from neighboring cells/effects in the source sheet.
    expanded = [main[0] - 50, main[1] - 18, main[2] + 50, main[3] + 18]
    keep = np.zeros(frame.shape[:2], dtype=bool)
    removed = []
    for comp in comps:
        x0, y0, x1, y1 = comp['bbox']
        intersects = not (x1 < expanded[0] or x0 > expanded[2] or y1 < expanded[1] or y0 > expanded[3])
        tiny_near_feet = comp['area'] < 180 and main[0] - 8 <= x0 <= main[2] + 8 and y0 >= main[3] - 8
        if comp is comps[0] or intersects or tiny_near_feet:
            keep[y0:y1, x0:x1] |= (frame[y0:y1, x0:x1, 3] > 0)
        else:
            removed.append(comp)
    cleaned = frame.copy()
    cleaned[~keep] = 0
    return cleaned, {'components_before': len(comps), 'removed_components': removed}

def pack_stable(scaled: np.ndarray, row_name: str) -> tuple[np.ndarray, dict]:
    bb = bbox(scaled[:, :, 3])
    frame = np.zeros((OUT_H, OUT_W, 4), dtype=np.uint8)
    if bb is None:
        return frame, {'bbox': None, 'crop_bbox': None, 'placed_at': [0, 0], 'opaque_pixels': 0}

    x0, y0, x1, y1 = bb
    crop = scaled[y0:y1, x0:x1]
    ch, cw = crop.shape[:2]
    # Keep the visible body/effect centered. If a slash/death frame is wider than
    # the cell, center-crop only transparent/excess cell area; never rescale a
    # single frame differently because that caused previous slash shrink/glitch.
    px = int(round(TARGET_CENTER_X - cw / 2))
    py = int(round(TARGET_BOTTOM[row_name] - ch))
    src_x0 = max(0, -px)
    src_y0 = max(0, -py)
    dst_x0 = max(0, px)
    dst_y0 = max(0, py)
    copy_w = min(cw - src_x0, OUT_W - dst_x0)
    copy_h = min(ch - src_y0, OUT_H - dst_y0)
    if copy_w > 0 and copy_h > 0:
        frame[dst_y0:dst_y0+copy_h, dst_x0:dst_x0+copy_w] = crop[src_y0:src_y0+copy_h, src_x0:src_x0+copy_w]
    frame, clean_meta = remove_disconnected_artifacts(frame)
    # Re-center after removing far-away artifacts; otherwise a deleted right-edge
    # fragment would leave the real body visually shoved left during slash.
    cleaned_bb = bbox(frame[:, :, 3])
    if cleaned_bb is not None:
        cx0, cy0, cx1, cy1 = cleaned_bb
        cleaned_crop = frame[cy0:cy1, cx0:cx1].copy()
        frame = np.zeros((OUT_H, OUT_W, 4), dtype=np.uint8)
        ch2, cw2 = cleaned_crop.shape[:2]
        px2 = int(round(TARGET_CENTER_X - cw2 / 2))
        py2 = int(round(TARGET_BOTTOM[row_name] - ch2))
        sx0 = max(0, -px2); sy0 = max(0, -py2)
        dx0 = max(0, px2); dy0 = max(0, py2)
        copy_w2 = min(cw2 - sx0, OUT_W - dx0)
        copy_h2 = min(ch2 - sy0, OUT_H - dy0)
        if copy_w2 > 0 and copy_h2 > 0:
            frame[dy0:dy0+copy_h2, dx0:dx0+copy_w2] = cleaned_crop[sy0:sy0+copy_h2, sx0:sx0+copy_w2]
        px, py = px2, py2
    out_bb = bbox(frame[:, :, 3])
    meta = {
        'crop_bbox': bb,
        'placed_at': [px, py],
        'bbox': out_bb,
        'bbox_center_x': None if out_bb is None else round((out_bb[0] + out_bb[2]) / 2, 2),
        'bbox_bottom': None if out_bb is None else out_bb[3],
        'opaque_pixels': int((frame[:, :, 3] > 0).sum()),
        'artifact_cleanup': clean_meta,
    }
    return frame, meta


def main() -> None:
    src = decode_rgba(SRC)
    h, w = src.shape[:2]
    x_edges = [round(i * w / COLS) for i in range(COLS + 1)]
    y_edges = [round(i * h / ROWS) for i in range(ROWS + 1)]
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    manifest = {
        'source_attachment': str(SRC),
        'source_image_size': [w, h],
        'source_note': 'Nate-approved uploaded Ghostface sheet; all player runtime Ghostface frames are extracted only from this sheet.',
        'v22_fix': 'Stable-pivot repack plus disconnected-fragment filtering removes stray neighboring-sheet artifacts visible during slash.',
        'checkerboard_removed': 'exterior flood-fill over bright low-saturation baked checkerboard per logical source cell',
        'logical_grid': {'columns': COLS, 'rows': ROWS, 'x_edges': x_edges, 'y_edges': y_edges},
        'runtime_cell': {'width': OUT_W, 'height': OUT_H, 'scale_from_source_cell': SCALE, 'pivot': 'stable bottom-center; engine draws bottom at entity y + 20'},
        'animations': {},
        'files': {},
    }

    row_atlases = []
    for r, name in enumerate(ROW_NAMES):
        atlas = np.zeros((OUT_H, OUT_W * COLS, 4), dtype=np.uint8)
        frames = []
        for c in range(COLS):
            y0, y1 = y_edges[r], y_edges[r+1]
            x0, x1 = x_edges[c], x_edges[c+1]
            cell = src[y0:y1, x0:x1].copy()
            bg = exterior_background_mask(cell)
            cell[:, :, 3] = np.where(bg, 0, 255).astype(np.uint8)
            cell[bg, :3] = 0
            sw = int(round(cell.shape[1] * SCALE))
            sh = int(round(cell.shape[0] * SCALE))
            scaled = resize_nearest(cell, sw, sh)
            frame, meta = pack_stable(scaled, name)
            atlas[:, c*OUT_W:(c+1)*OUT_W] = frame
            meta.update({'column': c, 'source_rect': [x0, y0, x1-x0, y1-y0]})
            frames.append(meta)
        filename = f'ghostface_uploaded_v22_{name}_{OUT_W}x{OUT_H}.png'
        out = OUT_DIR / filename
        write_png(out, atlas)
        data = out.read_bytes()
        centers = [f['bbox_center_x'] for f in frames if f['bbox_center_x'] is not None]
        manifest['animations'][name] = {
            'file': filename,
            'frames': COLS,
            'row': r,
            'cell_width': OUT_W,
            'cell_height': OUT_H,
            'center_drift_after_repack': 0 if not centers else round(max(centers) - min(centers), 2),
            'frame_metadata': frames,
        }
        manifest['files'][filename] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        row_atlases.append(atlas)

    full = np.vstack(row_atlases)
    full_name = f'ghostface_uploaded_v22_full_transparent_{OUT_W}x{OUT_H}.png'
    full_path = OUT_DIR / full_name
    write_png(full_path, full)
    data = full_path.read_bytes()
    manifest['files'][full_name] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'rows_stacked': ROW_NAMES}

    (OUT_DIR / 'asset_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'out_dir': str(OUT_DIR), 'animations': {k: v['file'] for k, v in manifest['animations'].items()}, 'center_drifts': {k: v['center_drift_after_repack'] for k, v in manifest['animations'].items()}, 'full': full_name}, indent=2))

if __name__ == '__main__':
    main()

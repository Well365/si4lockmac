#!/usr/bin/env python3
"""Shared drawing helpers for the si4lockmac walkthrough animations.

Everything here is a clean, hand-drawn reconstruction — NO real screenshots,
so no sensitive data (tokens, emails, Apple IDs, TOTP secrets) can leak. All
sample data shown is fake/garbled on purpose.
"""
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

# ── palette ──────────────────────────────────────────────────────────────────
DESK_TOP = (58, 70, 120)
DESK_BOT = (32, 38, 66)
WIN_BG = (246, 246, 248)
WIN_BAR = (232, 232, 236)
CARD = (255, 255, 255)
INK = (40, 42, 48)
SUBINK = (120, 124, 134)
BLUE = (10, 110, 250)
GREEN = (40, 190, 110)
AMBER = (240, 180, 40)
RED = (255, 95, 86)
CAPTION_BG = (18, 20, 30)
CAPTION_FG = (235, 238, 248)
ACCENT = (120, 180, 255)

ASCII_FONT = "/Users/maxwell/Library/Fonts/MesloLGLNerdFontMono-Regular.ttf"
CJK_FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
SF = "/System/Library/Fonts/SFNS.ttf"          # Apple system font (UI text)
SF_BOLD = "/System/Library/Fonts/SFNS.ttf"


def _font(path, size):
    return ImageFont.truetype(path, size)


def fonts(size):
    """Return (cjk, ascii) fonts at a given size."""
    return _font(CJK_FONT, size), _font(ASCII_FONT, size)


def is_cjk(ch):
    o = ord(ch)
    return o >= 0x2E80 and not (0x2018 <= o <= 0x201F)


def text_w(text, size):
    cf, af = fonts(size)
    return sum((cf if is_cjk(c) else af).getlength(c) for c in text)


def draw_text(d, x, y, text, size, fill, center_w=None):
    """Per-char font selection so CJK + ASCII mix cleanly."""
    if center_w is not None:
        x = x + (center_w - text_w(text, size)) / 2
    cf, af = fonts(size)
    for ch in text:
        f = cf if is_cjk(ch) else af
        d.text((x, y), ch, font=f, fill=fill)
        x += f.getlength(ch)
    return x


# ── primitives ───────────────────────────────────────────────────────────────
def desktop(W, H):
    img = Image.new("RGB", (W, H), DESK_BOT)
    d = ImageDraw.Draw(img)
    for yy in range(H):
        t = yy / H
        d.line([(0, yy), (W, yy)], fill=(
            int(DESK_TOP[0] + (DESK_BOT[0] - DESK_TOP[0]) * t),
            int(DESK_TOP[1] + (DESK_BOT[1] - DESK_TOP[1]) * t),
            int(DESK_TOP[2] + (DESK_BOT[2] - DESK_TOP[2]) * t)))
    return img


def traffic_lights(d, x, y):
    for i, c in enumerate([RED, (255, 189, 46), (39, 201, 63)]):
        d.ellipse([x + i * 22, y, x + 14 + i * 22, y + 14], fill=c)


def window(d, x, y, w, h, title="", radius=14):
    d.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=WIN_BG)
    d.rounded_rectangle([x, y, x + w, y + 44], radius=radius, fill=WIN_BAR)
    d.rectangle([x, y + 30, x + w, y + 44], fill=WIN_BAR)
    traffic_lights(d, x + 18, y + 15)
    if title:
        draw_text(d, x, y + 12, title, 17, (90, 94, 104), center_w=w)


def button(d, x, y, w, h, label, kind="primary", size=18):
    bg = {"primary": BLUE, "plain": (228, 228, 232), "ghost": (210, 212, 218)}[kind]
    fg = (255, 255, 255) if kind == "primary" else (60, 62, 70)
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    draw_text(d, x, y + (h - size) / 2 - 2, label, size, fg, center_w=w)
    return (x, y, w, h)


def cursor(d, x, y, scale=1.0):
    s = scale
    pts = [(0, 0), (0, 19), (5, 14), (9, 22), (12, 20), (8, 12), (15, 12)]
    pts = [(x + px * s, y + py * s) for px, py in pts]
    d.polygon(pts, fill=(255, 255, 255), outline=(20, 20, 20))


def lock_icon(d, cx, cy, s, color, key=(40, 40, 42)):
    bw, bh = s, int(s * 0.78)
    bx0, by0 = cx - bw // 2, cy - bh // 2 + 3
    d.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=max(2, s // 8), fill=color)
    r = int(s * 0.32)
    sx, sy = cx, by0 - r + 2
    wdt = max(2, s // 7)
    d.arc([sx - r, sy - r, sx + r, sy + r], 180, 360, fill=color, width=wdt)
    d.line([sx - r, sy, sx - r, by0 + 1], fill=color, width=wdt)
    d.line([sx + r, sy, sx + r, by0 + 1], fill=color, width=wdt)
    d.ellipse([cx - s // 12 - 1, by0 + bh // 2 - s // 8, cx + s // 12 + 1, by0 + bh // 2 + s // 16], fill=key)


def check_circle(d, cx, cy, r, color=GREEN):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=max(3, r // 6))
    d.line([cx - r * 0.42, cy + r * 0.05, cx - r * 0.08, cy + r * 0.42], fill=color, width=max(3, r // 6))
    d.line([cx - r * 0.08, cy + r * 0.42, cx + r * 0.5, cy - r * 0.35], fill=color, width=max(3, r // 6))


def warning_triangle(d, cx, cy, s, color=AMBER):
    h = s
    pts = [(cx, cy - h * 0.55), (cx - h * 0.62, cy + h * 0.5), (cx + h * 0.62, cy + h * 0.5)]
    d.polygon(pts, fill=color)
    d.line([cx, cy - h * 0.15, cx, cy + h * 0.2], fill=(255, 255, 255), width=max(3, s // 12))
    d.ellipse([cx - s // 16, cy + h * 0.3, cx + s // 16, cy + h * 0.3 + s // 8], fill=(255, 255, 255))


def menubar(d, W, clock="22:24"):
    d.rectangle([0, 0, W, 28], fill=(26, 26, 32))
    draw_text(d, 16, 5, "  Finder  File  Edit  View", 15, (205, 205, 214))
    draw_text(d, W - 150, 5, "100%   " + clock, 15, (205, 205, 214))


def caption(d, W, H, title, body, idx=None, total=None):
    bar_h = 86
    y0 = H - bar_h
    d.rectangle([0, y0, W, H], fill=CAPTION_BG)
    d.rectangle([0, y0, W, y0 + 3], fill=BLUE)
    tx = 34
    if idx is not None:
        d.ellipse([tx, y0 + 24, tx + 38, y0 + 62], fill=BLUE)
        draw_text(d, tx, y0 + 30, str(idx), 22, (255, 255, 255), center_w=38)
        tx += 58
    draw_text(d, tx, y0 + 18, title, 22, CAPTION_FG)
    draw_text(d, tx, y0 + 50, body, 17, ACCENT)
    if idx and total:
        # step dots
        dotx = W - 34 - total * 22
        for i in range(total):
            c = BLUE if (i + 1) == idx else (70, 74, 90)
            d.ellipse([dotx + i * 22, y0 + 38, dotx + i * 22 + 10, y0 + 48], fill=c)


# ── export ───────────────────────────────────────────────────────────────────
def export(frames, out_base, fps=20):
    """frames: list of (PIL.Image, duration_ms). Write <out_base>.gif and .mp4."""
    os.makedirs(os.path.dirname(out_base), exist_ok=True)
    gif = out_base + ".gif"
    master = frames[len(frames) // 2][0].convert("P", palette=Image.ADAPTIVE, colors=128)
    pal = [f.convert("RGB").quantize(palette=master, dither=Image.NONE) for f, _ in frames]
    pal[0].save(gif, save_all=True, append_images=pal[1:],
                duration=[ms for _, ms in frames], loop=0, disposal=2, optimize=True)
    gkb = round(os.path.getsize(gif) / 1024)

    # MP4: dump RGB frames at constant fps honoring per-frame durations
    tmp = out_base + "_frames"
    os.makedirs(tmp, exist_ok=True)
    n = 0
    for img, ms in frames:
        reps = max(1, round(ms / (1000 / fps)))
        for _ in range(reps):
            img.convert("RGB").save(os.path.join(tmp, f"f_{n:05d}.png"))
            n += 1
    mp4 = out_base + ".mp4"
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps),
        "-i", os.path.join(tmp, "f_%05d.png"),
        "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-c:v", "libx264",
        "-pix_fmt", "yuv420p", "-crf", "20", mp4], check=True)
    mkb = round(os.path.getsize(mp4) / 1024)
    for fn in os.listdir(tmp):
        os.remove(os.path.join(tmp, fn))
    os.rmdir(tmp)
    print(f"{os.path.basename(gif)}: {gkb} KB ({len(frames)} keyframes) · "
          f"{os.path.basename(mp4)}: {mkb} KB ({n} frames @ {fps}fps)")

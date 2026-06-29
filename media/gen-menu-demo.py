#!/usr/bin/env python3
"""Render a synthetic (mock) GIF of the si4lockmac menu-bar GUI.

This is a hand-drawn reconstruction, NOT a screen recording. Menu labels are
the real ones from the GUI (状态 / 开启遮罩 / 系统锁屏 / 语言 / 打赏作者 / 退出).
Sequence: click the menu-bar lock -> dropdown opens -> hover to 开启遮罩 ->
screen veils black with a password box -> unveil -> loop.
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = "/Users/maxwell/Documents/idears/si4-apps/si4lockmac/si4lockmac-release/media/menu-demo.gif"
W, H = 960, 600

ASCII_FONT = "/Users/maxwell/Library/Fonts/MesloLGLNerdFontMono-Regular.ttf"
CJK_FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
f_menu = ImageFont.truetype(CJK_FONT, 19)
f_bar = ImageFont.truetype(CJK_FONT, 16)
f_pw = ImageFont.truetype(CJK_FONT, 22)
f_ascii = ImageFont.truetype(ASCII_FONT, 16)


def is_cjk(ch):
    return ord(ch) >= 0x2E80


def text_w(text, font):
    cf = ImageFont.truetype(CJK_FONT, font.size)
    af = ImageFont.truetype(ASCII_FONT, font.size)
    return sum((cf if is_cjk(c) else af).getlength(c) for c in text)


def draw_text(d, x, y, text, font, fill):
    cf = ImageFont.truetype(CJK_FONT, font.size)
    af = ImageFont.truetype(ASCII_FONT, font.size)
    for ch in text:
        f = cf if is_cjk(ch) else af
        d.text((x, y), ch, font=f, fill=fill)
        x += f.getlength(ch)
    return x


# menu-bar lock icon position
ICON_X, ICON_Y = W - 78, 14
MENU_X, MENU_TOP, MENU_W = W - 300, 30, 250

# dropdown layout (label, kind); kind 'item' or 'sep'
MENU = [
    ("状态", "item"),
    ("sep", "sep"),
    ("开启遮罩", "item"),
    ("系统锁屏", "item"),
    ("sep", "sep"),
    ("语言               ▸", "item"),
    ("打赏作者", "item"),
    ("退出", "item"),
]


def row_layout():
    """Return list of (y_top, height, kind, label)."""
    rows, y = [], MENU_TOP + 8
    for label, kind in MENU:
        h = 12 if kind == "sep" else 34
        rows.append((y, h, kind, label))
        y += h
    return rows, y + 8


ROWS, MENU_BOTTOM = row_layout()


def lock_icon(d, cx, cy, s, color):
    """Draw a simple padlock centred at (cx, cy), body ~s wide."""
    bw, bh = s, int(s * 0.78)
    bx0, by0 = cx - bw // 2, cy - bh // 2 + 3
    d.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=3, fill=color)
    # shackle
    r = int(s * 0.32)
    sx, sy = cx, by0 - r + 2
    d.arc([sx - r, sy - r, sx + r, sy + r], 180, 360, fill=color, width=3)
    d.line([sx - r, sy, sx - r, by0 + 1], fill=color, width=3)
    d.line([sx + r, sy, sx + r, by0 + 1], fill=color, width=3)
    # keyhole
    d.ellipse([cx - 2, by0 + bh // 2 - 4, cx + 2, by0 + bh // 2], fill=(40, 40, 42))


def cursor(d, x, y):
    pts = [(x, y), (x, y + 18), (x + 5, y + 13), (x + 9, y + 21),
           (x + 12, y + 19), (x + 8, y + 11), (x + 14, y + 11)]
    d.polygon(pts, fill=(255, 255, 255), outline=(0, 0, 0))


def render(cur, menu_open, hi_label, veil, show_pw):
    img = Image.new("RGB", (W, H), (20, 20, 28))
    d = ImageDraw.Draw(img)
    # desktop gradient
    for yy in range(H):
        t = yy / H
        d.line([(0, yy), (W, yy)],
               fill=(int(36 + 30 * t), int(40 + 60 * t), int(78 + 70 * t)))
    # a faux app window
    d.rounded_rectangle([120, 150, 600, 470], radius=12, fill=(30, 30, 46))
    d.rounded_rectangle([120, 150, 600, 184], radius=12, fill=(43, 43, 60))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([138 + i * 22, 160, 152 + i * 22, 174], fill=c)
    draw_text(d, 300, 158, "工作进行中…", f_bar, (140, 150, 180))
    for k in range(5):
        d.rounded_rectangle([148, 210 + k * 42, 200 + k * 70, 234 + k * 42],
                            radius=5, fill=(55, 56, 78))
    # menu bar
    d.rectangle([0, 0, W, 28], fill=(28, 28, 32))
    draw_text(d, 18, 5, "  File   Edit   View", f_bar, (200, 200, 210))
    draw_text(d, ICON_X - 165, 5, "100%   22:24", f_bar, (200, 200, 210))
    lock_icon(d, ICON_X, ICON_Y, 16, (235, 235, 240))
    # dropdown
    if menu_open:
        d.rounded_rectangle([MENU_X, MENU_TOP, MENU_X + MENU_W, MENU_BOTTOM],
                            radius=10, fill=(42, 42, 48))
        for (y, h, kind, label) in ROWS:
            if kind == "sep":
                d.line([MENU_X + 12, y + 6, MENU_X + MENU_W - 12, y + 6],
                       fill=(80, 80, 88))
                continue
            color = (235, 235, 240)
            if hi_label == label:
                d.rounded_rectangle([MENU_X + 6, y + 2, MENU_X + MENU_W - 6, y + h - 2],
                                    radius=6, fill=(10, 110, 250))
                color = (255, 255, 255)
            draw_text(d, MENU_X + 22, y + 7, label, f_menu, color)
    # veil overlay
    if veil > 0:
        ov = Image.new("RGBA", (W, H), (0, 0, 0, veil))
        img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
        d = ImageDraw.Draw(img)
        if show_pw:
            bw2, bh2 = 360, 150
            bx, by = W // 2 - bw2 // 2, H // 2 - bh2 // 2
            d.rounded_rectangle([bx, by, bx + bw2, by + bh2], radius=14, fill=(28, 28, 34))
            lock_icon(d, W // 2, by + 38, 26, (230, 230, 235))
            t = "输入密码解除遮罩"
            draw_text(d, W // 2 - text_w(t, f_pw) / 2, by + 64, t, f_pw, (220, 220, 230))
            d.rounded_rectangle([bx + 40, by + 104, bx + bw2 - 40, by + 134],
                                radius=8, fill=(50, 50, 60))
            draw_text(d, bx + 52, by + 110, "• • • • • • • •", f_pw, (170, 170, 185))
    if cur:
        cursor(d, *cur)
    return img


frames = []


def add(img, ms):
    frames.append((img.copy(), ms))


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


# ── sequence ─────────────────────────────────────────────────────────────────
start = (430, 360)
# 1. cursor moves to the lock icon
for i in range(14):
    c = lerp(start, (ICON_X - 4, ICON_Y - 4), i / 13)
    add(render(c, False, None, 0, False), 45)
add(render((ICON_X - 4, ICON_Y - 4), False, None, 0, False), 250)
# 2. click -> menu opens
add(render((ICON_X - 4, ICON_Y - 4), True, None, 0, False), 500)
# 3. hover descends through items, ending on 开启遮罩
hover_path = ["状态", "开启遮罩"]
item_y = {lab: y for (y, h, k, lab) in ROWS if k == "item"}
for lab in hover_path:
    cy = item_y[lab] + 16
    add(render((MENU_X + 40, cy), True, lab, 0, False), 420)
add(render((MENU_X + 40, item_y["开启遮罩"] + 16), True, "开启遮罩", 0, False), 600)
# 4. click 开启遮罩 -> veil fades in
for a in range(0, 256, 36):
    add(render(None, False, None, a, False), 40)
add(render(None, False, None, 255, True), 1700)
# 5. brief unveil back to desktop
for a in range(255, -1, -60):
    add(render(None, False, None, a, False), 50)
add(render(None, False, None, 0, False), 700)

# ── export ───────────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(OUT), exist_ok=True)
master = frames[1][0].convert("P", palette=Image.ADAPTIVE, colors=128)
pal = [f.quantize(palette=master, dither=Image.NONE) for f, _ in frames]
pal[0].save(OUT, save_all=True, append_images=pal[1:],
            duration=[ms for _, ms in frames], loop=0, disposal=2, optimize=True)
print("frames:", len(frames), "size:", round(os.path.getsize(OUT) / 1024), "KB")

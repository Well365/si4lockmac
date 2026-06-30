#!/usr/bin/env python3
"""Synthetic (mock) menu-bar GUI demo with a trilingual top caption banner.

Hand-drawn reconstruction, NOT a screen recording. Menu labels are the real ones
(状态 / 开启遮罩 / 系统锁屏 / 语言 / 打赏作者 / 退出). Sequence: click the menu-bar
lock -> dropdown -> hover 开启遮罩 -> veil to black with a password box.
Emits media/menu-demo.gif + .mp4.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
import demo_common as C

OUT = "/Users/maxwell/Documents/idears/si4-apps/si4lockmac/si4lockmac-release/media/menu-demo"
W, H = 1100, 720
SCENE_H = H - C.CAPTION_H

ASCII_FONT = "/Users/maxwell/Library/Fonts/MesloLGLNerdFontMono-Regular.ttf"
CJK_FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
f_menu = ImageFont.truetype(CJK_FONT, 19)
f_bar = ImageFont.truetype(CJK_FONT, 16)
f_pw = ImageFont.truetype(CJK_FONT, 22)
f_ascii = ImageFont.truetype(ASCII_FONT, 16)

ICON_X, ICON_Y = W - 78, 14
MENU_X, MENU_TOP, MENU_W = W - 300, 30, 250

MENU = [("状态", "item"), ("sep", "sep"), ("开启遮罩", "item"), ("系统锁屏", "item"),
        ("sep", "sep"), ("语言               ▸", "item"), ("打赏作者", "item"), ("退出", "item")]

TRI = {
    1: [("中文", "点开菜单栏锁图标", "顶部锁图标 → 下拉菜单"),
        ("EN", "Open the menu-bar lock", "Click the lock icon in the menu bar"),
        ("日本語", "メニューバーの鍵を開く", "上部の鍵アイコンをクリック")],
    2: [("中文", "选择操作", "状态 / 开启遮罩 / 系统锁屏 / 语言 / 退出"),
        ("EN", "Pick an action", "Status / Veil / Lock / Language / Quit"),
        ("日本語", "操作を選ぶ", "状態 / 遮蔽 / ロック / 言語 / 終了")],
    3: [("中文", "开启遮罩 → 屏幕变黑", "别人看到黑屏,你输密码解除(Telegram 也能远程)"),
        ("EN", "Veil → screen goes black", "Onlookers see black; unlock with your password"),
        ("日本語", "遮蔽 → 画面が黒く", "周囲には黒画面 · パスワードで解除")],
}
TOTAL = 3
_cur = {"idx": 1}


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


def row_layout():
    rows, y = [], MENU_TOP + 8
    for label, kind in MENU:
        h = 12 if kind == "sep" else 34
        rows.append((y, h, kind, label))
        y += h
    return rows, y + 8


ROWS, MENU_BOTTOM = row_layout()


def lock_icon(d, cx, cy, s, color):
    bw, bh = s, int(s * 0.78)
    bx0, by0 = cx - bw // 2, cy - bh // 2 + 3
    d.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=3, fill=color)
    r = int(s * 0.32)
    sx, sy = cx, by0 - r + 2
    d.arc([sx - r, sy - r, sx + r, sy + r], 180, 360, fill=color, width=3)
    d.line([sx - r, sy, sx - r, by0 + 1], fill=color, width=3)
    d.line([sx + r, sy, sx + r, by0 + 1], fill=color, width=3)
    d.ellipse([cx - 2, by0 + bh // 2 - 4, cx + 2, by0 + bh // 2], fill=(40, 40, 42))


def cursor(d, x, y):
    pts = [(x, y), (x, y + 18), (x + 5, y + 13), (x + 9, y + 21),
           (x + 12, y + 19), (x + 8, y + 11), (x + 14, y + 11)]
    d.polygon(pts, fill=(255, 255, 255), outline=(0, 0, 0))


def render_scene(cur, menu_open, hi_label, veil, show_pw):
    img = Image.new("RGB", (W, SCENE_H), (20, 20, 28))
    d = ImageDraw.Draw(img)
    for yy in range(SCENE_H):
        t = yy / SCENE_H
        d.line([(0, yy), (W, yy)], fill=(int(36 + 30 * t), int(40 + 60 * t), int(78 + 70 * t)))
    # faux app window
    d.rounded_rectangle([180, 150, 700, 470], radius=12, fill=(30, 30, 46))
    d.rounded_rectangle([180, 150, 700, 184], radius=12, fill=(43, 43, 60))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([198 + i * 22, 160, 212 + i * 22, 174], fill=c)
    draw_text(d, 400, 158, "工作进行中…", f_bar, (140, 150, 180))
    for k in range(5):
        d.rounded_rectangle([208, 210 + k * 42, 260 + k * 70, 234 + k * 42], radius=5, fill=(55, 56, 78))
    # menu bar
    d.rectangle([0, 0, W, 28], fill=(28, 28, 32))
    draw_text(d, 18, 5, "  File   Edit   View", f_bar, (200, 200, 210))
    draw_text(d, ICON_X - 165, 5, "100%   22:24", f_bar, (200, 200, 210))
    lock_icon(d, ICON_X, ICON_Y, 16, (235, 235, 240))
    if menu_open:
        d.rounded_rectangle([MENU_X, MENU_TOP, MENU_X + MENU_W, MENU_BOTTOM], radius=10, fill=(42, 42, 48))
        for (y, h, kind, label) in ROWS:
            if kind == "sep":
                d.line([MENU_X + 12, y + 6, MENU_X + MENU_W - 12, y + 6], fill=(80, 80, 88))
                continue
            color = (235, 235, 240)
            if hi_label == label:
                d.rounded_rectangle([MENU_X + 6, y + 2, MENU_X + MENU_W - 6, y + h - 2], radius=6, fill=(10, 110, 250))
                color = (255, 255, 255)
            draw_text(d, MENU_X + 22, y + 7, label, f_menu, color)
    if veil > 0:
        ov = Image.new("RGBA", (W, SCENE_H), (0, 0, 0, veil))
        img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
        d = ImageDraw.Draw(img)
        if show_pw:
            bw2, bh2 = 360, 150
            bx, by = W // 2 - bw2 // 2, SCENE_H // 2 - bh2 // 2
            d.rounded_rectangle([bx, by, bx + bw2, by + bh2], radius=14, fill=(28, 28, 34))
            lock_icon(d, W // 2, by + 38, 26, (230, 230, 235))
            t = "输入密码解除遮罩"
            draw_text(d, W // 2 - text_w(t, f_pw) / 2, by + 64, t, f_pw, (220, 220, 230))
            d.rounded_rectangle([bx + 40, by + 104, bx + bw2 - 40, by + 134], radius=8, fill=(50, 50, 60))
            draw_text(d, bx + 52, by + 110, "• • • • • • • •", f_pw, (170, 170, 185))
    if cur:
        cursor(d, *cur)
    return img


def render(cur, menu_open, hi_label, veil, show_pw):
    scene = render_scene(cur, menu_open, hi_label, veil, show_pw)
    return C.compose(scene, W, H, TRI[_cur["idx"]], idx=_cur["idx"], total=TOTAL)


frames = []
def add(img, ms): frames.append((img.copy(), ms))
def lerp(a, b, t): return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


# ── sequence ─────────────────────────────────────────────────────────────────
_cur["idx"] = 1
start = (480, 360)
for i in range(14):
    add(render(lerp(start, (ICON_X - 4, ICON_Y - 4), i / 13), False, None, 0, False), 45)
add(render((ICON_X - 4, ICON_Y - 4), False, None, 0, False), 350)
add(render((ICON_X - 4, ICON_Y - 4), True, None, 0, False), 700)
# hover items
_cur["idx"] = 2
item_y = {lab: y for (y, h, k, lab) in ROWS if k == "item"}
for lab in ["状态", "开启遮罩"]:
    add(render((MENU_X + 40, item_y[lab] + 16), True, lab, 0, False), 460)
add(render((MENU_X + 40, item_y["开启遮罩"] + 16), True, "开启遮罩", 0, False), 700)
# veil fades in
_cur["idx"] = 3
for a in range(0, 256, 36):
    add(render(None, False, None, a, False), 40)
add(render(None, False, None, 255, True), 2200)   # 2s hold on the veil
# brief unveil
for a in range(255, -1, -60):
    add(render(None, False, None, a, False), 50)
add(render(None, False, None, 0, False), 800)

C.export(frames, OUT, fps=20)

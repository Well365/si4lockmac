#!/usr/bin/env python3
"""Render a terminal-style typing-demo GIF of safe (read-only) lockmac commands.

All command output is taken verbatim from a real run on this machine.
ASCII glyphs use Meslo (monospace); CJK glyphs use Hiragino Sans GB.
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = "/Users/maxwell/Documents/idears/si4-apps/si4lockmac/si4lockmac-release/media/cli-demo.gif"

# ── theme ────────────────────────────────────────────────────────────────────
W, H = 960, 700
PAD_X, PAD_TOP = 28, 70           # content padding (title bar is 46px tall)
LINE_H = 30
FONT_SIZE = 22
BG = (30, 30, 46)                 # window body
BAR = (43, 43, 60)                # title bar
FG = (205, 214, 244)             # default text
GREEN = (166, 227, 161)
BLUE = (137, 180, 250)
WHITE = (248, 248, 242)
COMMENT = (108, 112, 134)
YELLOW = (249, 226, 175)

ASCII_FONT = "/Users/maxwell/Library/Fonts/MesloLGLNerdFontMono-Regular.ttf"
CJK_FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
font_ascii = ImageFont.truetype(ASCII_FONT, FONT_SIZE)
font_cjk = ImageFont.truetype(CJK_FONT, FONT_SIZE)


def is_cjk(ch):
    return ord(ch) >= 0x2E80


def char_font(ch):
    return font_cjk if is_cjk(ch) else font_ascii


def seg_width(text):
    return sum(char_font(c).getlength(c) for c in text)


def draw_segments(draw, x, y, segments):
    """segments: list of (text, color). Draw char-by-char with per-char font."""
    for text, color in segments:
        for ch in text:
            f = char_font(ch)
            draw.text((x, y), ch, font=f, fill=color)
            x += f.getlength(ch)
    return x


# ── demo script: real, read-only commands ───────────────────────────────────
PROMPT = [("➜ ", GREEN), ("si4lockmac ", BLUE), ("$ ", WHITE)]

STEPS = [
    {"cmd": "lockmac status", "out": [
        ("lockMac:  遮罩 关", FG),
        ("  密码: 已设       两步验证: 开", FG),
        ("  开机默认: 开     遮罩自启: 已装", FG),
        ("  Telegram: 已绑定   监听服务: 开", FG),
        ("  离线锁: 开 (grace 60s / relock 300s)", FG),
    ]},
    {"cmd": "lockmac deadman", "out": [
        ("心跳: 关 · 失联超时: 关 · 动作: lock", FG),
        ("例: lockmac deadman 1800 600 lock 7200   # 30min签到/失联2h→锁", COMMENT),
    ]},
    {"cmd": "lockmac offline-lock", "out": [
        ("offline-lock: on (grace 60s / relock 300s)", FG),
    ]},
    {"cmd": "lockmac delete list", "out": [
        ("删除清单：(空)", FG),
    ]},
]

HEADER = ("# si4lockmac — 安全只读命令(CLI 命令为 lockmac)", COMMENT)

# ── frame engine ─────────────────────────────────────────────────────────────
frames = []          # list of (PIL image, duration_ms)
buffer = [[HEADER], []]  # completed visible lines (each line = list of segments)

MAX_LINES = (H - PAD_TOP - 20) // LINE_H


def render(active_segments=None, cursor=False):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # title bar
    d.rectangle([0, 0, W, 46], fill=BAR)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([22 + i * 26, 16, 38 + i * 26, 32], fill=c)
    d.text((W / 2 - seg_width("lockmac — demo") / 2, 12),
           "lockmac — demo", font=font_ascii, fill=COMMENT)
    # visible lines (scroll: keep last MAX_LINES)
    lines = buffer[-MAX_LINES:] if active_segments is None else \
        (buffer + [active_segments])[-MAX_LINES:]
    y = PAD_TOP
    for line in lines:
        x = draw_segments(d, PAD_X, y, line)
        if cursor and line is (active_segments if active_segments else None):
            pass
        y += LINE_H
    # cursor block on the active line
    if cursor:
        cy = PAD_TOP + (min(len(lines), MAX_LINES) - 1) * LINE_H
        cx = PAD_X + seg_width("".join(t for t, _ in (active_segments or lines[-1])))
        d.rectangle([cx, cy + 2, cx + 11, cy + FONT_SIZE + 2], fill=WHITE)
    return img


def add(img, ms):
    frames.append((img.copy(), ms))


# blink helper for idle hold
def hold(active, ms_total, blink=True):
    elapsed = 0
    state = True
    while elapsed < ms_total:
        add(render(active, cursor=state), 120)
        elapsed += 120
        if blink:
            state = not state


# build animation
hold([], 500)
for step in STEPS:
    cmd = step["cmd"]
    # type the command char by char (2 chars/frame)
    typed = ""
    i = 0
    while i < len(cmd):
        typed += cmd[i:i + 2]
        i += 2
        active = PROMPT + [(typed, WHITE)]
        add(render(active, cursor=True), 55)
    # commit command line, brief pause with cursor
    hold(PROMPT + [(typed, WHITE)], 360)
    buffer.append(PROMPT + [(cmd, WHITE)])
    # reveal output lines
    for seg in step["out"]:
        buffer.append([seg])
        add(render(None, cursor=False), 90)
    buffer.append([])           # blank spacer
    hold([], 520, blink=True)

hold([], 900)

# ── export GIF with a shared palette for smaller, flicker-free output ─────────
os.makedirs(os.path.dirname(OUT), exist_ok=True)
master = frames[len(frames) // 2][0].convert("P", palette=Image.ADAPTIVE, colors=64)
pal_frames = [f.quantize(palette=master, dither=Image.NONE) for f, _ in frames]
durations = [ms for _, ms in frames]
pal_frames[0].save(
    OUT, save_all=True, append_images=pal_frames[1:],
    duration=durations, loop=0, disposal=2, optimize=True,
)
print("frames:", len(frames))
print("wrote:", OUT, "size:", round(os.path.getsize(OUT) / 1024), "KB")

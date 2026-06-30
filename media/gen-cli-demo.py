#!/usr/bin/env python3
"""Terminal typing-demo of safe (read-only) lockmac commands, with a trilingual
top caption banner (中文 / EN / 日本語). Command output is verbatim from a real
run. Emits media/cli-demo.gif + .mp4.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
import demo_common as C

OUT = "/Users/maxwell/Documents/idears/si4-apps/si4lockmac/si4lockmac-release/media/cli-demo"
W, H = 1100, 700
SCENE_H = H - C.CAPTION_H
PAD_X, PAD_TOP = 30, 66
LINE_H = 30
FONT_SIZE = 22
BG = (30, 30, 46)
BAR = (43, 43, 60)
FG = (205, 214, 244)
GREEN = (166, 227, 161)
BLUE = (137, 180, 250)
WHITE = (248, 248, 242)
COMMENT = (118, 122, 144)

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
    for text, color in segments:
        for ch in text:
            f = char_font(ch)
            draw.text((x, y), ch, font=f, fill=color)
            x += f.getlength(ch)
    return x


PROMPT = [("➜ ", GREEN), ("si4lockmac ", BLUE), ("$ ", WHITE)]

INTRO = [("中文", "只读命令演示", "安全命令,不会遮黑你的屏幕"),
         ("EN", "Read-only CLI tour", "Safe commands — they won't veil your screen"),
         ("日本語", "読み取り専用デモ", "安全なコマンド · 画面は黒くなりません")]

STEPS = [
    {"cmd": "lockmac status", "tri": [
        ("中文", "查看状态", "遮罩 / 密码 / 2FA / 服务 / 离线锁 一览"),
        ("EN", "Check status", "Veil / password / 2FA / services / offline-lock"),
        ("日本語", "状態を確認", "目隠し / パスワード / 2FA / サービス")],
     "out": [
        ("lockMac:  遮罩 关", FG),
        ("  密码: 已设       两步验证: 开", FG),
        ("  开机默认: 开     遮罩自启: 已装", FG),
        ("  Telegram: 已绑定   监听服务: 开", FG),
        ("  离线锁: 开 (grace 60s / relock 300s)", FG)]},
    {"cmd": "lockmac deadman", "tri": [
        ("中文", "定时开关(死人开关)", "无响应或失联时自动执行 锁/遮罩/删除"),
        ("EN", "Dead-man switch", "Auto-acts if you go silent or offline"),
        ("日本語", "デッドマン", "無応答 / オフラインで自動実行")],
     "out": [
        ("心跳: 关 · 失联超时: 关 · 动作: lock", FG),
        ("例: lockmac deadman 1800 600 lock 7200   # 30min签到/失联2h→锁", COMMENT)]},
    {"cmd": "lockmac offline-lock", "tri": [
        ("中文", "离线锁", "断网就持续重锁,直到输入密码"),
        ("EN", "Offline-lock", "Stays locked while the network is down"),
        ("日本語", "オフラインロック", "切断中はロックし続ける")],
     "out": [
        ("offline-lock: on (grace 60s / relock 300s)", FG)]},
    {"cmd": "lockmac delete list", "tri": [
        ("中文", "删除清单", "紧急清除的目录白名单(危险路径自动拒绝)"),
        ("EN", "Purge list", "Whitelist wiped on trigger · system paths refused"),
        ("日本語", "削除リスト", "発火時に消す対象 · 危険パスは拒否")],
     "out": [
        ("删除清单：(空)", FG)]},
]
TOTAL = len(STEPS)

HEADER = ("# si4lockmac — 安全只读命令(CLI 命令为 lockmac)", COMMENT)
frames = []
buffer = [[HEADER], []]
MAX_LINES = (SCENE_H - PAD_TOP - 16) // LINE_H

_cur = {"tri": INTRO, "idx": None}


def render_scene(active_segments=None, cursor=False):
    img = Image.new("RGB", (W, SCENE_H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 46], fill=BAR)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([22 + i * 26, 16, 38 + i * 26, 32], fill=c)
    d.text((W / 2 - seg_width("lockmac — demo") / 2, 12), "lockmac — demo", font=font_ascii, fill=COMMENT)
    lines = buffer[-MAX_LINES:] if active_segments is None else (buffer + [active_segments])[-MAX_LINES:]
    y = PAD_TOP
    for line in lines:
        draw_segments(d, PAD_X, y, line)
        y += LINE_H
    if cursor:
        cy = PAD_TOP + (min(len(lines), MAX_LINES) - 1) * LINE_H
        cx = PAD_X + seg_width("".join(t for t, _ in (active_segments or lines[-1])))
        d.rectangle([cx, cy + 2, cx + 11, cy + FONT_SIZE + 2], fill=WHITE)
    return img


def frame(active=None, cursor=False):
    scene = render_scene(active, cursor)
    return C.compose(scene, W, H, _cur["tri"], idx=_cur["idx"], total=TOTAL)


def add(img, ms):
    frames.append((img.copy(), ms))


def hold(active, ms_total, blink=True):
    elapsed, state = 0, True
    while elapsed < ms_total:
        add(frame(active, cursor=state), 120)
        elapsed += 120
        if blink:
            state = not state


# build animation
add(frame([], cursor=True), 600)
for n, step in enumerate(STEPS, 1):
    _cur["tri"], _cur["idx"] = step["tri"], n
    cmd = step["cmd"]
    typed, i = "", 0
    while i < len(cmd):
        typed += cmd[i:i + 2]
        i += 2
        add(frame(PROMPT + [(typed, WHITE)], cursor=True), 55)
    hold(PROMPT + [(typed, WHITE)], 300)        # short cursor blink before run
    buffer.append(PROMPT + [(cmd, WHITE)])
    for seg in step["out"]:
        buffer.append([seg])
        add(frame(None, cursor=False), 90)
    buffer.append([])
    add(frame([], cursor=False), 2000)          # 2s static read pause

add(frame([], cursor=False), 900)

C.export(frames, OUT, fps=20)

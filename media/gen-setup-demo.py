#!/usr/bin/env python3
"""Animated setup-wizard walkthrough for si4lockmac (clean reconstruction).

Reproduces the real setup flow (set password -> bind Telegram -> check binding
-> bind iMessage -> enable 2FA -> all services -> veil screen) with FULLY FAKE
data: the bot token, Apple ID, and TOTP secret shown here are random
placeholders, never real secrets. Emits media/setup-demo.gif + .mp4.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import demo_common as C

W, H = 1000, 640
CONTENT_H = H - 86
OUT = "/Users/maxwell/Documents/idears/si4-apps/si4lockmac/si4lockmac-release/media/setup-demo"
TOTAL = 7

# ── obviously-fake placeholder data (NOT real secrets) ───────────────────────
FAKE_TOKEN = "80••7•2:AAFq9••Rnd••tok••xZk9"
FAKE_APPLEID = "user_4f2a@example.com"
FAKE_TOTP = "K7Q2  9XV4  R8WP  5ZN3"

frames = []
def add(img, ms): frames.append((img.copy(), ms))
def lerp(a, b, t): return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def base(clock="09:24", veil_icon=True):
    img = C.desktop(W, H)
    d = ImageDraw.Draw(img)
    C.menubar(d, W, clock)
    if veil_icon:
        C.lock_icon(d, W - 60, 14, 16, (235, 235, 240))
    return img, d


def dialog(d, dw, dh, dy=None):
    dx = (W - dw) // 2
    if dy is None:
        dy = (CONTENT_H - dh) // 2 + 14
    d.rounded_rectangle([dx, dy, dx + dw, dy + dh], radius=18, fill=(250, 250, 252))
    return dx, dy


def field(d, x, y, w, text, mono=True, h=32):
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(255, 255, 255), outline=(205, 207, 214), width=1)
    C.draw_text(d, x + 12, y + (h - 16) / 2, text, 15, (95, 98, 108))


# ── Scene 1: Welcome — set a password ────────────────────────────────────────
def s1_password():
    def draw(cursor_xy, dots):
        img, d = base()
        dw, dh = 480, 250
        dx, dy = dialog(d, dw, dh)
        C.lock_icon(d, dx + dw // 2, dy + 40, 26, (90, 92, 100))
        C.draw_text(d, dx, dy + 66, "Welcome to lockmac", 20, C.INK, center_w=dw)
        C.draw_text(d, dx, dy + 96, "Step 1 (required): set a password", 15, C.SUBINK, center_w=dw)
        field(d, dx + 70, dy + 128, dw - 140, "•" * dots)
        field(d, dx + 70, dy + 170, dw - 140, "•" * dots)
        C.button(d, dx + dw // 2 - 70, dy + 210, 140, 0, "", "plain")
        C.caption(d, W, H, "设置解锁密码(必填)", "用随机示意字符代替真实密码 · 解除遮罩要用它", idx=1, total=TOTAL)
        if cursor_xy: C.cursor(d, *cursor_xy)
        return img
    for dots in range(0, 9):
        add(draw((620, 360), dots), 105)
    add(draw(None, 8), 650)


# ── Scene 2: Bind Telegram (paste bot token) ─────────────────────────────────
def s2_telegram():
    def draw(reveal):
        img, d = base()
        dw, dh = 520, 240
        dx, dy = dialog(d, dw, dh)
        C.draw_text(d, dx, dy + 30, "Bind Telegram", 20, C.INK, center_w=dw)
        C.draw_text(d, dx, dy + 62, "Paste the bot token from @BotFather", 15, C.SUBINK, center_w=dw)
        shown = FAKE_TOKEN[:reveal] if reveal < len(FAKE_TOKEN) else FAKE_TOKEN
        field(d, dx + 50, dy + 104, dw - 100, shown, h=36)
        C.button(d, dx + dw // 2 - 70, dy + 168, 140, 40, "OK", "primary", size=16)
        C.caption(d, W, H, "绑定 Telegram 机器人(可选)", "粘贴 BotFather 给的 token · 这里是随机假 token", idx=2, total=TOTAL)
        return img
    for r in range(0, len(FAKE_TOKEN) + 1, 2):
        add(draw(r), 70)
    add(draw(len(FAKE_TOKEN)), 700)


# ── Scene 3: Check binding — message the bot ─────────────────────────────────
def s3_checking():
    def draw(msg_sent):
        img, d = base()
        # faux Telegram chat window (left)
        wx, wy, ww, wh = 120, 80, 420, CONTENT_H - 150
        C.window(d, wx, wy, ww, wh, "Telegram")
        d.rectangle([wx, wy + 44, wx + ww, wy + 84], fill=(112, 160, 90))
        C.draw_text(d, wx + 16, wy + 54, "si4lockmac_bot", 16, (255, 255, 255))
        d.rectangle([wx, wy + 84, wx + ww, wy + wh - 50], fill=(231, 232, 224))
        if msg_sent:
            bw = 90
            d.rounded_rectangle([wx + ww - bw - 20, wy + 110, wx + ww - 20, wy + 144], radius=12, fill=(220, 248, 198))
            C.draw_text(d, wx + ww - bw - 6, wy + 118, "/start", 15, (40, 60, 40))
        d.rounded_rectangle([wx + 16, wy + wh - 42, wx + ww - 16, wy + wh - 12], radius=14, fill=(255, 255, 255))
        C.draw_text(d, wx + 28, wy + wh - 36, "Message", 14, C.SUBINK)
        # checking dialog (right)
        ddx, ddy, ddw, ddh = 560, 200, 360, 170
        d.rounded_rectangle([ddx, ddy, ddx + ddw, ddy + ddh], radius=16, fill=(250, 250, 252))
        C.lock_icon(d, ddx + ddw // 2, ddy + 36, 22, (90, 92, 100))
        C.draw_text(d, ddx, ddy + 62, "Checking the binding…", 17, C.INK, center_w=ddw)
        C.draw_text(d, ddx, ddy + 92, "Send any message to your bot", 14, C.SUBINK, center_w=ddw)
        # spinner-ish
        ang = 30 if msg_sent else 270
        d.arc([ddx + ddw // 2 - 16, ddy + 116, ddx + ddw // 2 + 16, ddy + 148], ang, ang + 250, fill=C.BLUE, width=4)
        C.caption(d, W, H, "给 bot 发条消息", "Telegram 里发 /start → 自动获取 chat id", idx=3, total=TOTAL)
        return img
    add(draw(False), 900)
    add(draw(True), 500)
    img = draw(True); d = ImageDraw.Draw(img)
    C.check_circle(d, 740, 316, 16)
    add(img, 900)


# ── Scene 4: Bind iMessage alerts (Apple ID) ─────────────────────────────────
def s4_imessage():
    def draw(reveal):
        img, d = base()
        dw, dh = 500, 230
        dx, dy = dialog(d, dw, dh)
        C.draw_text(d, dx, dy + 28, "Step 3 (recommended)", 19, C.INK, center_w=dw)
        C.draw_text(d, dx, dy + 58, "Bind iMessage alerts", 15, C.SUBINK, center_w=dw)
        C.draw_text(d, dx + 50, dy + 96, "Apple ID (email or phone):", 14, C.SUBINK)
        shown = FAKE_APPLEID[:reveal]
        field(d, dx + 50, dy + 120, dw - 100, shown, h=36)
        C.button(d, dx + dw // 2 - 70, dy + 176, 140, 40, "OK", "primary", size=16)
        C.caption(d, W, H, "绑定 iMessage 告警(可选)", "填 Apple ID → 入侵/告警发到 iMessage · 示例为假地址", idx=4, total=TOTAL)
        return img
    for r in range(0, len(FAKE_APPLEID) + 1):
        add(draw(r), 55)
    add(draw(len(FAKE_APPLEID)), 650)


# ── Scene 5: Enable 2FA (TOTP secret) ────────────────────────────────────────
def s5_2fa():
    def draw():
        img, d = base()
        dw, dh = 520, 270
        dx, dy = dialog(d, dw, dh)
        C.draw_text(d, dx, dy + 26, "Step 4 (recommended): enable 2FA", 18, C.INK, center_w=dw)
        C.draw_text(d, dx, dy + 56, "Unlock needs password + 6-digit code", 14, C.SUBINK, center_w=dw)
        # secret box
        d.rounded_rectangle([dx + 60, dy + 92, dx + dw - 60, dy + 140], radius=10, fill=(240, 243, 250))
        C.draw_text(d, dx, dy + 104, FAKE_TOTP, 22, C.BLUE, center_w=dw)
        d.rounded_rectangle([dx + 60, dy + 156, dx + dw - 60, dy + 192], radius=8, fill=(255, 248, 230))
        C.warning_triangle(d, dx + 86, dy + 174, 22)
        C.draw_text(d, dx + 110, dy + 164, "Screenshot / write it down — back it up!", 13, (150, 110, 20))
        C.button(d, dx + dw // 2 - 80, dy + 214, 160, 40, "Enable", "primary", size=16)
        C.caption(d, W, H, "开启两步验证 TOTP(推荐)", "把密钥加进验证器 · 务必备份 · 示例密钥为随机假值", idx=5, total=TOTAL)
        return img
    add(draw(), 2200)


# ── Scene 6: All services started ────────────────────────────────────────────
def s6_started():
    def draw():
        img, d = base()
        dw, dh = 460, 250
        dx, dy = dialog(d, dw, dh)
        C.check_circle(d, dx + dw // 2, dy + 46, 26)
        C.draw_text(d, dx, dy + 80, "All services started", 20, C.INK, center_w=dw)
        items = ["veil autostart", "Telegram listener", "hourly watchdog"]
        for i, it in enumerate(items):
            C.draw_text(d, dx + 110, dy + 116 + i * 30, "•", 18, C.GREEN)
            C.draw_text(d, dx + 132, dy + 114 + i * 30, it, 16, (70, 72, 80))
        C.button(d, dx + dw // 2 - 70, dy + 210, 140, 0, "", "plain")
        C.caption(d, W, H, "全部服务已启动", "遮罩自启 + Telegram 监听 + 每小时 watchdog", idx=6, total=TOTAL)
        return img
    add(draw(), 2000)


# ── Scene 7: The veil screen ─────────────────────────────────────────────────
def s7_veil():
    def draw(dots, fade=255):
        img = Image.new("RGB", (W, H), (0, 0, 0))
        d = ImageDraw.Draw(img)
        # green shield/lock
        cx, cy = W // 2, 150
        d.rounded_rectangle([cx - 46, cy - 40, cx + 46, cy + 50], radius=16, fill=(40, 190, 110))
        C.lock_icon(d, cx, cy + 6, 40, (255, 255, 255), key=(40, 190, 110))
        C.draw_text(d, 0, cy + 70, "si4lockmac", 24, (245, 247, 252), center_w=W)
        C.draw_text(d, 0, cy + 104, "2FA lock · remote control · intrusion alerts", 15, (150, 200, 170), center_w=W)
        # screen-covered + password field
        C.draw_text(d, 0, cy + 150, "Screen covered", 16, (200, 205, 215), center_w=W)
        fw = 300
        d.rounded_rectangle([(W - fw) // 2, cy + 184, (W + fw) // 2, cy + 220], radius=10, fill=(40, 42, 50))
        C.draw_text(d, 0, cy + 192, "•" * dots, 20, (180, 185, 200), center_w=W)
        C.caption(d, W, H, "完成 — 这就是遮罩界面", "别人看到黑屏,你输密码即可解除(Telegram 也能远程解)", idx=7, total=TOTAL)
        if fade < 255:
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 255 - fade))
            img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
        return img
    for f in range(60, 256, 48):
        add(draw(0, f), 50)
    for dots in range(0, 7):
        add(draw(dots), 120)
    add(draw(6), 2400)


s1_password()
s2_telegram()
s3_checking()
s4_imessage()
s5_2fa()
s6_started()
s7_veil()

C.export(frames, OUT, fps=20)

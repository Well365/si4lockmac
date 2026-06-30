#!/usr/bin/env python3
"""Animated setup-wizard walkthrough for si4lockmac (clean reconstruction).

Real setup flow (set password -> bind Telegram -> check binding -> bind iMessage
-> enable 2FA -> all services -> veil screen) with FULLY FAKE data — the bot
token, Apple ID and TOTP secret are random placeholders, never real secrets.
Trilingual top captions (中文 / EN / 日本語); each step holds 2s on completion.
Emits media/setup-demo.gif + .mp4.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import demo_common as C

W, H = 1200, 760
SCENE_H = H - C.CAPTION_H
OUT = "/Users/maxwell/Documents/idears/si4-apps/si4lockmac/si4lockmac-release/media/setup-demo"
TOTAL = 7
HOLD = 2000

# obviously-fake placeholders (NOT real secrets)
FAKE_TOKEN = "80••7•2:AAFq9••Rnd••tok••xZk9"
FAKE_APPLEID = "user_4f2a@example.com"
FAKE_TOTP = "K7Q2  9XV4  R8WP  5ZN3"

STEPS = {
    1: [("中文", "设置解锁密码(必填)", "用随机示意字符代替真实密码 · 解除遮罩要用它"),
        ("EN", "Set an unlock password", "Required · used to remove the veil"),
        ("日本語", "解除パスワードを設定", "必須 · 目隠しの解除に使用します")],
    2: [("中文", "绑定 Telegram 机器人(可选)", "粘贴 BotFather 给的 token · 这里是随机假 token"),
        ("EN", "Bind a Telegram bot (optional)", "Paste the BotFather token · the token shown is fake"),
        ("日本語", "Telegram bot を連携(任意)", "BotFather の token を貼付 · 表示はダミー")],
    3: [("中文", "给 bot 发条消息", "Telegram 里发 /start → 自动获取 chat id"),
        ("EN", "Message your bot", "Send /start in Telegram → chat id auto-saved"),
        ("日本語", "bot にメッセージ", "Telegram で /start → chat id 自動取得")],
    4: [("中文", "绑定 iMessage 告警(可选)", "填 Apple ID → 告警发到 iMessage · 示例为假地址"),
        ("EN", "Bind iMessage alerts (optional)", "Enter Apple ID → alerts via iMessage · sample is fake"),
        ("日本語", "iMessage 通知を連携(任意)", "Apple ID を入力 → iMessage に通知 · 例はダミー")],
    5: [("中文", "开启两步验证 TOTP(推荐)", "把密钥加进验证器 · 务必备份 · 示例密钥为随机假值"),
        ("EN", "Enable 2FA / TOTP (recommended)", "Add the key to an authenticator · back it up · key is fake"),
        ("日本語", "2FA / TOTP を有効化(推奨)", "鍵を認証アプリへ · 必ずバックアップ · 鍵はダミー")],
    6: [("中文", "全部服务已启动", "遮罩自启 + Telegram 监听 + 每小时 watchdog"),
        ("EN", "All services started", "Veil autostart + Telegram listener + hourly watchdog"),
        ("日本語", "全サービス起動", "目隠し自動 + Telegram 監視 + 毎時 watchdog")],
    7: [("中文", "完成 — 这就是遮罩界面", "别人看到黑屏,你输密码解除(Telegram 也能远程解)"),
        ("EN", "Done — this is the veil", "Onlookers see black; unlock with your password"),
        ("日本語", "完了 — これが目隠し", "周囲には黒画面 · パスワードで解除")],
}

frames = []
def add(img, ms): frames.append((img.copy(), ms))
def scene(clock="09:24", veil_icon=True):
    img = C.desktop(W, SCENE_H); d = ImageDraw.Draw(img); C.menubar(d, W, clock)
    if veil_icon: C.lock_icon(d, W - 60, 14, 16, (235, 235, 240))
    return img, d
def fin(img, idx): return C.compose(img, W, H, STEPS[idx], idx=idx, total=TOTAL)
def dlg(d, dw, dh, dy=None):
    dx = (W - dw) // 2
    if dy is None: dy = (SCENE_H - dh) // 2
    d.rounded_rectangle([dx, dy, dx + dw, dy + dh], radius=18, fill=(250, 250, 252))
    return dx, dy
def field(d, x, y, w, text, h=32):
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(255, 255, 255), outline=(205, 207, 214), width=1)
    C.draw_text(d, x + 12, y + (h - 16) / 2, text, 15, (95, 98, 108))


# ── Scene 1: set a password ──────────────────────────────────────────────────
def s1():
    def draw(cur, dots):
        img, d = scene()
        dw, dh = 480, 250
        dx, dy = dlg(d, dw, dh)
        C.lock_icon(d, dx + dw // 2, dy + 40, 26, (90, 92, 100))
        C.draw_text(d, dx, dy + 66, "Welcome to lockmac", 20, C.INK, center_w=dw)
        C.draw_text(d, dx, dy + 96, "Step 1 (required): set a password", 15, C.SUBINK, center_w=dw)
        field(d, dx + 70, dy + 128, dw - 140, "•" * dots)
        field(d, dx + 70, dy + 170, dw - 140, "•" * dots)
        C.button(d, dx + dw // 2 - 70, dy + 208, 140, 38, "OK", "primary", size=16)
        if cur: C.cursor(d, *cur)
        return fin(img, 1)
    for dots in range(0, 9):
        add(draw((W // 2 + 90, SCENE_H // 2), dots), 105)
    add(draw(None, 8), HOLD)


# ── Scene 2: bind Telegram (paste token) ─────────────────────────────────────
def s2():
    def draw(reveal):
        img, d = scene()
        dw, dh = 540, 230
        dx, dy = dlg(d, dw, dh)
        C.draw_text(d, dx, dy + 30, "Bind Telegram", 20, C.INK, center_w=dw)
        C.draw_text(d, dx, dy + 62, "Paste the bot token from @BotFather", 15, C.SUBINK, center_w=dw)
        field(d, dx + 50, dy + 104, dw - 100, FAKE_TOKEN[:reveal], h=36)
        C.button(d, dx + dw // 2 - 70, dy + 166, 140, 40, "OK", "primary", size=16)
        return fin(img, 2)
    for r in range(0, len(FAKE_TOKEN) + 1, 2):
        add(draw(r), 70)
    add(draw(len(FAKE_TOKEN)), HOLD)


# ── Scene 3: check binding — message the bot ─────────────────────────────────
def s3():
    def draw(sent, ok=False):
        img, d = scene()
        ww, wh = 430, SCENE_H - 120
        wx, wy = 130, 60
        C.window(d, wx, wy, ww, wh, "Telegram")
        d.rectangle([wx, wy + 44, wx + ww, wy + 84], fill=(112, 160, 90))
        C.draw_text(d, wx + 16, wy + 54, "si4lockmac_bot", 16, (255, 255, 255))
        d.rectangle([wx, wy + 84, wx + ww, wy + wh - 50], fill=(231, 232, 224))
        if sent:
            d.rounded_rectangle([wx + ww - 110, wy + 110, wx + ww - 20, wy + 144], radius=12, fill=(220, 248, 198))
            C.draw_text(d, wx + ww - 96, wy + 118, "/start", 15, (40, 60, 40))
        d.rounded_rectangle([wx + 16, wy + wh - 42, wx + ww - 16, wy + wh - 12], radius=14, fill=(255, 255, 255))
        C.draw_text(d, wx + 28, wy + wh - 36, "Message", 14, C.SUBINK)
        ddx, ddy, ddw, ddh = W - 560, 150, 380, 180
        d.rounded_rectangle([ddx, ddy, ddx + ddw, ddy + ddh], radius=16, fill=(250, 250, 252))
        C.lock_icon(d, ddx + ddw // 2, ddy + 38, 22, (90, 92, 100))
        C.draw_text(d, ddx, ddy + 66, "Checking the binding…", 17, C.INK, center_w=ddw)
        C.draw_text(d, ddx, ddy + 96, "Send any message to your bot", 14, C.SUBINK, center_w=ddw)
        if ok:
            C.check_circle(d, ddx + ddw // 2, ddy + 138, 16)
        else:
            ang = 30 if sent else 270
            d.arc([ddx + ddw // 2 - 16, ddy + 124, ddx + ddw // 2 + 16, ddy + 156], ang, ang + 250, fill=C.BLUE, width=4)
        return fin(img, 3)
    add(draw(False), 900)
    add(draw(True), 500)
    add(draw(True, ok=True), HOLD)


# ── Scene 4: bind iMessage (Apple ID) ────────────────────────────────────────
def s4():
    def draw(reveal):
        img, d = scene()
        dw, dh = 500, 230
        dx, dy = dlg(d, dw, dh)
        C.draw_text(d, dx, dy + 28, "Step 3 (recommended)", 19, C.INK, center_w=dw)
        C.draw_text(d, dx, dy + 58, "Bind iMessage alerts", 15, C.SUBINK, center_w=dw)
        C.draw_text(d, dx + 50, dy + 96, "Apple ID (email or phone):", 14, C.SUBINK)
        field(d, dx + 50, dy + 120, dw - 100, FAKE_APPLEID[:reveal], h=36)
        C.button(d, dx + dw // 2 - 70, dy + 176, 140, 40, "OK", "primary", size=16)
        return fin(img, 4)
    for r in range(0, len(FAKE_APPLEID) + 1):
        add(draw(r), 55)
    add(draw(len(FAKE_APPLEID)), HOLD)


# ── Scene 5: enable 2FA (TOTP) ───────────────────────────────────────────────
def s5():
    def draw():
        img, d = scene()
        dw, dh = 520, 270
        dx, dy = dlg(d, dw, dh)
        C.draw_text(d, dx, dy + 26, "Step 4 (recommended): enable 2FA", 18, C.INK, center_w=dw)
        C.draw_text(d, dx, dy + 56, "Unlock needs password + 6-digit code", 14, C.SUBINK, center_w=dw)
        d.rounded_rectangle([dx + 60, dy + 92, dx + dw - 60, dy + 140], radius=10, fill=(240, 243, 250))
        C.draw_text(d, dx, dy + 104, FAKE_TOTP, 22, C.BLUE, center_w=dw)
        d.rounded_rectangle([dx + 60, dy + 156, dx + dw - 60, dy + 192], radius=8, fill=(255, 248, 230))
        C.warning_triangle(d, dx + 86, dy + 174, 22)
        C.draw_text(d, dx + 110, dy + 164, "Screenshot / write it down — back it up!", 13, (150, 110, 20))
        C.button(d, dx + dw // 2 - 80, dy + 214, 160, 40, "Enable", "primary", size=16)
        return fin(img, 5)
    add(draw(), HOLD + 400)


# ── Scene 6: all services started ────────────────────────────────────────────
def s6():
    def draw():
        img, d = scene()
        dw, dh = 460, 250
        dx, dy = dlg(d, dw, dh)
        C.check_circle(d, dx + dw // 2, dy + 46, 26)
        C.draw_text(d, dx, dy + 80, "All services started", 20, C.INK, center_w=dw)
        for i, it in enumerate(["veil autostart", "Telegram listener", "hourly watchdog"]):
            C.draw_text(d, dx + 110, dy + 116 + i * 30, "•", 18, C.GREEN)
            C.draw_text(d, dx + 132, dy + 114 + i * 30, it, 16, (70, 72, 80))
        C.button(d, dx + dw // 2 - 70, dy + 208, 140, 38, "OK", "primary", size=16)
        return fin(img, 6)
    add(draw(), HOLD)


# ── Scene 7: the veil screen ─────────────────────────────────────────────────
def s7():
    def draw(dots, fade=255):
        img = Image.new("RGB", (W, SCENE_H), (0, 0, 0))
        d = ImageDraw.Draw(img)
        cx, cy = W // 2, 130
        d.rounded_rectangle([cx - 46, cy - 40, cx + 46, cy + 50], radius=16, fill=(40, 190, 110))
        C.lock_icon(d, cx, cy + 6, 40, (255, 255, 255), key=(40, 190, 110))
        C.draw_text(d, 0, cy + 70, "si4lockmac", 24, (245, 247, 252), center_w=W)
        C.draw_text(d, 0, cy + 104, "2FA lock · remote control · intrusion alerts", 15, (150, 200, 170), center_w=W)
        C.draw_text(d, 0, cy + 150, "Screen covered", 16, (200, 205, 215), center_w=W)
        fw = 300
        d.rounded_rectangle([(W - fw) // 2, cy + 184, (W + fw) // 2, cy + 220], radius=10, fill=(40, 42, 50))
        C.draw_text(d, 0, cy + 192, "•" * dots, 20, (180, 185, 200), center_w=W)
        if fade < 255:
            ov = Image.new("RGBA", (W, SCENE_H), (0, 0, 0, 255 - fade))
            img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
        return fin(img, 7)
    for f in range(60, 256, 48):
        add(draw(0, f), 50)
    for dots in range(0, 7):
        add(draw(dots), 120)
    add(draw(6), HOLD + 600)


s1(); s2(); s3(); s4(); s5(); s6(); s7()
C.export(frames, OUT, fps=20)

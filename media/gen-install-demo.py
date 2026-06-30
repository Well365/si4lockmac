#!/usr/bin/env python3
"""Animated install walkthrough for si4lockmac (clean reconstruction).

Real install flow (GitHub Release -> .pkg -> "未打开" warning -> System Settings
"Open Anyway" -> Mac password -> installer -> success) with fully fake data.
Captions are trilingual (中文 / EN / 日本語) in a top banner; each step holds 2s
on its completed screen. Emits media/install-demo.gif + .mp4.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import demo_common as C

W, H = 1200, 760
SCENE_H = H - C.CAPTION_H
OUT = "/Users/maxwell/Documents/idears/si4-apps/si4lockmac/si4lockmac-release/media/install-demo"
TOTAL = 6
HOLD = 2000  # 2s pause on each completed step

STEPS = {
    1: [("中文", "下载安装包", "在 Release 页点 lockmac-0.5.0.pkg 下载"),
        ("EN", "Download the pkg", "On the Releases page, click lockmac-0.5.0.pkg"),
        ("日本語", "パッケージを入手", "Releases ページで lockmac-0.5.0.pkg をクリック")],
    2: [("中文", "双击安装包", "在「下载」里双击 lockmac-0.5.0.pkg"),
        ("EN", "Double-click the pkg", "Open lockmac-0.5.0.pkg from Downloads"),
        ("日本語", "pkg をダブルクリック", "ダウンロードの lockmac-0.5.0.pkg を開く")],
    3: [("中文", "点「完成」别移废纸篓", "未签名提示而已,先关掉,下一步去授权打开"),
        ("EN", "Click Done — don't trash it", "Just an unsigned warning; close it, then allow"),
        ("日本語", "「完了」を押す", "未署名の警告です。閉じて次で許可します")],
    4: [("中文", "点「仍要打开」", "系统设置 ▸ 隐私与安全性 ▸ 仍要打开"),
        ("EN", "Click Open Anyway", "System Settings ▸ Privacy & Security ▸ Open Anyway"),
        ("日本語", "「このまま開く」", "システム設定 ▸ プライバシー ▸ このまま開く")],
    5: [("中文", "输入开机密码", "用随机示意字符代替真实密码"),
        ("EN", "Enter your Mac password", "Shown as random placeholder characters"),
        ("日本語", "Mac のパスワード入力", "表示はランダムなダミー文字です")],
    6: [("中文", "安装成功", "菜单栏出现锁图标,设置向导自动打开"),
        ("EN", "Installation complete", "A lock appears in the menu bar; setup opens"),
        ("日本語", "インストール完了", "メニューバーに鍵 → 設定ウィザードが起動")],
}
END = [("中文", "下一步:设置向导", "设密码 → 绑定 Telegram → 2FA(见 setup 演示)"),
       ("EN", "Next: setup wizard", "Password → Telegram → 2FA (see the setup demo)"),
       ("日本語", "次:設定ウィザード", "パスワード → Telegram → 2FA(setup デモ)")]

frames = []
def add(img, ms): frames.append((img.copy(), ms))
def lerp(a, b, t): return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
def scene(clock="09:20"):
    img = C.desktop(W, SCENE_H); d = ImageDraw.Draw(img); C.menubar(d, W, clock)
    return img, d
def fin(img, idx): return C.compose(img, W, H, STEPS[idx], idx=idx, total=TOTAL)
def cwin(ww):  # centered window x
    return (W - ww) // 2


# ── Scene 1: GitHub Release — download the pkg ───────────────────────────────
def scene_release():
    ww, wh = 860, SCENE_H - 70
    wx, wy = cwin(ww), 36
    def draw(cur):
        img, d = scene()
        C.window(d, wx, wy, ww, wh, "si4lockmac — Releases")
        d.rounded_rectangle([wx + 60, wy + 56, wx + ww - 60, wy + 84], radius=8, fill=(255, 255, 255))
        C.draw_text(d, wx + 76, wy + 60, "github.com/Well365/si4lockmac/releases", 15, C.SUBINK)
        C.draw_text(d, wx + 40, wy + 110, "si4lockmac 0.5.0", 26, C.INK)
        d.rounded_rectangle([wx + 300, wy + 116, wx + 380, wy + 142], radius=12, fill=(225, 245, 230))
        C.draw_text(d, wx + 312, wy + 119, "Latest", 15, C.GREEN)
        C.draw_text(d, wx + 40, wy + 150, "macOS privacy veil · brew install --cask Well365/lockmac/lockmac", 15, C.SUBINK)
        ax, ay, aw = wx + 40, wy + 200, ww - 80
        d.rounded_rectangle([ax, ay, ax + aw, ay + 150], radius=10, outline=(220, 222, 228), width=2)
        C.draw_text(d, ax + 16, ay + 14, "Assets", 16, C.INK)
        d.line([ax, ay + 44, ax + aw, ay + 44], fill=(230, 232, 238))
        d.rounded_rectangle([ax + 6, ay + 52, ax + aw - 6, ay + 92], radius=8, fill=(235, 244, 255))
        C.lock_icon(d, ax + 30, ay + 72, 16, C.BLUE)
        C.draw_text(d, ax + 52, ay + 62, "lockmac-0.5.0.pkg", 17, C.BLUE)
        C.draw_text(d, ax + aw - 130, ay + 64, "6.3 MB", 15, C.SUBINK)
        C.draw_text(d, ax + 52, ay + 104, "Source code (zip)", 16, C.SUBINK)
        if cur: C.cursor(d, *cur)
        return fin(img, 1), (ax + 52, ay + 72)
    _, target = draw((560, 360))
    for i in range(16):
        add(draw(lerp((560, 380), target, i / 15))[0], 50)
    add(draw(target)[0], 300)
    img2, _ = draw(target); d2 = ImageDraw.Draw(img2)
    tx, ty = target[0], target[1] + C.CAPTION_H
    d2.ellipse([tx - 18, ty - 18, tx + 18, ty + 18], outline=C.BLUE, width=3)
    add(img2, 250)
    add(draw(target)[0], HOLD)


# ── Scene 2: Finder — double-click the pkg ───────────────────────────────────
def scene_finder():
    ww, wh = 720, SCENE_H - 110
    wx, wy = cwin(ww), 54
    def draw(cur):
        img, d = scene()
        C.window(d, wx, wy, ww, wh, "下载")
        d.rectangle([wx, wy + 44, wx + 150, wy + wh], fill=(241, 241, 244))
        for i, lab in enumerate(["最近使用", "应用程序", "桌面", "下载", "iCloud 云盘"]):
            if lab == "下载":
                d.rounded_rectangle([wx + 8, wy + 60 + i * 34, wx + 142, wy + 90 + i * 34], radius=6, fill=(220, 224, 232))
            C.draw_text(d, wx + 22, wy + 66 + i * 34, lab, 15, C.BLUE if lab == "下载" else (90, 92, 100))
        bx, by = wx + 400, wy + 120
        d.polygon([(bx, by + 40), (bx + 70, by + 10), (bx + 140, by + 40), (bx + 70, by + 70)], fill=(214, 170, 110))
        d.polygon([(bx, by + 40), (bx + 70, by + 70), (bx + 70, by + 150), (bx, by + 120)], fill=(180, 134, 80))
        d.polygon([(bx + 70, by + 70), (bx + 140, by + 40), (bx + 140, by + 120), (bx + 70, by + 150)], fill=(198, 152, 96))
        d.polygon([(bx + 20, by - 6), (bx + 70, by + 10), (bx + 70, by + 38), (bx + 20, by + 22)], fill=(240, 210, 110))
        C.draw_text(d, wx + 250, wy + wh - 86, "lockmac-0.5.0.pkg", 18, C.INK)
        C.draw_text(d, wx + 250, wy + wh - 58, "安装器 flat 软件包 — 6.3 MB", 15, C.SUBINK)
        if cur: C.cursor(d, *cur)
        return fin(img, 2)
    target = (wx + 470, wy + 200)
    for i in range(12):
        add(draw(lerp((wx + 300, wy + 360), target, i / 11)), 55)
    for _ in range(2):
        img = draw(target); d = ImageDraw.Draw(img)
        tx, ty = target[0], target[1] + C.CAPTION_H
        d.ellipse([tx - 16, ty - 16, tx + 16, ty + 16], outline=(255, 255, 255), width=3)
        add(img, 130); add(draw(target), 130)
    add(draw(target), HOLD)


# ── Scene 3: "未打开" Gatekeeper warning ──────────────────────────────────────
def scene_warning():
    dw, dh = 470, 250
    dx, dy = (W - dw) // 2, 100
    def draw(cur, hl):
        img, d = scene()
        d.rounded_rectangle([dx, dy, dx + dw, dy + dh], radius=18, fill=(250, 250, 252))
        C.warning_triangle(d, dx + 70, dy + 60, 64)
        C.draw_text(d, dx + 120, dy + 36, '未打开 "lockmac-0.5.0.pkg"', 19, C.INK)
        C.draw_text(d, dx + 120, dy + 72, "Apple 无法验证此 App 是否包含", 15, (90, 92, 100))
        C.draw_text(d, dx + 120, dy + 96, "恶意软件。", 15, (90, 92, 100))
        b1 = C.button(d, dx + 60, dy + 170, 160, 44, "完成", "plain")
        if hl:
            d.rounded_rectangle([b1[0] - 4, b1[1] - 4, b1[0] + b1[2] + 4, b1[1] + b1[3] + 4], radius=26, outline=C.BLUE, width=3)
        C.button(d, dx + 250, dy + 170, 160, 44, "移到废纸篓", "primary")
        if cur: C.cursor(d, *cur)
        return fin(img, 3)
    add(draw((520, 380), False), 400)
    target = (dx + 140, dy + 192)
    for i in range(12):
        add(draw(lerp((520, 380), target, i / 11), i > 7), 55)
    add(draw(target, True), HOLD)


# ── Scene 4: System Settings — Open Anyway ───────────────────────────────────
def scene_openanyway():
    ww, wh = 800, SCENE_H - 90
    wx, wy = cwin(ww), 46
    def draw(cur, hl):
        img, d = scene()
        C.window(d, wx, wy, ww, wh, "隐私与安全性")
        d.rectangle([wx, wy + 44, wx + 200, wy + wh], fill=(241, 241, 244))
        for i, lab in enumerate(["定位服务", "通讯录", "辅助功能", "完全磁盘访问", "安全性"]):
            sel = lab == "安全性"
            if sel:
                d.rounded_rectangle([wx + 10, wy + 64 + i * 40, wx + 190, wy + 100 + i * 40], radius=7, fill=(220, 224, 232))
            C.draw_text(d, wx + 26, wy + 72 + i * 40, lab, 15, C.BLUE if sel else (90, 92, 100))
        mx = wx + 230
        C.draw_text(d, mx, wy + 70, "安全性", 18, C.INK)
        d.rounded_rectangle([mx, wy + 110, wx + ww - 30, wy + 180], radius=10, fill=(255, 255, 255))
        C.draw_text(d, mx + 16, wy + 124, '已阻止使用 "lockmac-0.5.0.pkg",', 15, (70, 72, 80))
        C.draw_text(d, mx + 16, wy + 148, "因为来自身份不明的开发者。", 15, (70, 72, 80))
        b = C.button(d, wx + ww - 200, wy + 126, 150, 40, "仍要打开", "plain", size=16)
        if hl:
            d.rounded_rectangle([b[0] - 4, b[1] - 4, b[0] + b[2] + 4, b[1] + b[3] + 4], radius=24, outline=C.BLUE, width=3)
        if cur: C.cursor(d, *cur)
        return fin(img, 4), (b[0] + b[2] // 2, b[1] + b[3] // 2)
    _, target = draw(None, False)
    add(draw((560, 380), False)[0], 400)
    for i in range(14):
        add(draw(lerp((560, 380), target, i / 13), i > 9)[0], 52)
    add(draw(target, True)[0], HOLD)


# ── Scene 5: Mac password sheet ──────────────────────────────────────────────
def scene_password():
    dw, dh = 450, 220
    dx, dy = (W - dw) // 2, 110
    def draw(cur, dots):
        img, d = scene()
        d.rounded_rectangle([dx, dy, dx + dw, dy + dh], radius=18, fill=(248, 248, 250))
        C.lock_icon(d, dx + dw // 2, dy + 48, 30, (90, 92, 100))
        C.draw_text(d, dx, dy + 78, "「设置」想要进行更改。", 17, C.INK, center_w=dw)
        C.draw_text(d, dx, dy + 104, "输入你的密码以允许此操作。", 14, C.SUBINK, center_w=dw)
        d.rounded_rectangle([dx + 70, dy + 132, dx + dw - 70, dy + 164], radius=8, fill=(255, 255, 255), outline=(200, 202, 210), width=1)
        C.draw_text(d, dx + 84, dy + 138, "•" * dots, 22, (90, 92, 100))
        C.button(d, dx + dw // 2 - 75, dy + 178, 150, 38, "好", "primary", size=16)
        if cur: C.cursor(d, *cur)
        return fin(img, 5)
    for dots in range(0, 9):
        add(draw((dx + dw // 2 + 30, dy + 148), dots), 105)
    add(draw(None, 8), HOLD)


# ── Scene 6: Installer wizard + success ──────────────────────────────────────
def scene_installer():
    steps = ["介绍", "目的宗卷", "安装类型", "安装", "摘要"]
    ww, wh = 740, SCENE_H - 110
    wx, wy = cwin(ww), 54
    def draw(active, progress, done):
        img, d = scene()
        C.window(d, wx, wy, ww, wh, "安装 lockmac")
        d.rectangle([wx, wy + 44, wx + 220, wy + wh], fill=(238, 238, 242))
        for i, s in enumerate(steps):
            on = i <= active
            d.ellipse([wx + 24, wy + 70 + i * 42, wx + 36, wy + 82 + i * 42],
                      fill=C.BLUE if i == active else (200, 202, 210) if on else (220, 222, 228))
            C.draw_text(d, wx + 50, wy + 68 + i * 42, s, 16, C.INK if on else (170, 172, 180))
        mx = wx + 250
        if not done:
            C.draw_text(d, mx, wy + 80, "正在安装…", 18, C.INK)
            d.rounded_rectangle([mx, wy + 120, wx + ww - 40, wy + 138], radius=9, fill=(225, 227, 232))
            d.rounded_rectangle([mx, wy + 120, mx + int((wx + ww - 40 - mx) * progress), wy + 138], radius=9, fill=C.BLUE)
        else:
            C.check_circle(d, (mx + wx + ww - 40) // 2, wy + 130, 46)
            C.draw_text(d, mx, wy + 196, "安装成功。", 22, C.INK, center_w=(wx + ww - 40 - mx))
            C.button(d, wx + ww - 150, wy + wh - 56, 110, 40, "关闭", "primary", size=16)
        return fin(img, 6)
    for k in range(0, 11):
        add(draw(min(3, k // 3), k / 10, False), 130)
    add(draw(4, 1.0, True), HOLD + 600)


# ── End card ─────────────────────────────────────────────────────────────────
def end_card():
    img = C.desktop(W, SCENE_H); d = ImageDraw.Draw(img)
    C.menubar(d, W, "09:21")
    C.lock_icon(d, W - 60, 14, 16, (235, 235, 240))
    d.ellipse([W - 88, 2, W - 36, 50], outline=C.ACCENT, width=2)
    C.check_circle(d, W // 2, SCENE_H // 2 - 70, 60)
    C.draw_text(d, 0, SCENE_H // 2 + 16, "安装完成 · Installed · 完了", 30, (245, 247, 252), center_w=W)
    C.draw_text(d, 0, SCENE_H // 2 + 62, "菜单栏出现锁图标 — 设置向导会自动打开", 19, C.VIVID_BODY, center_w=W)
    full = Image.new("RGB", (W, H), C.CAPTION_BG)
    full.paste(img, (0, C.CAPTION_H))
    C.caption(ImageDraw.Draw(full), W, END)
    add(full, HOLD + 600)


scene_release()
scene_finder()
scene_warning()
scene_openanyway()
scene_password()
scene_installer()
end_card()

C.export(frames, OUT, fps=20)

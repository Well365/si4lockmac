#!/usr/bin/env python3
"""Animated install walkthrough for si4lockmac (clean reconstruction).

Reproduces the real install flow (GitHub Release -> .pkg -> "未打开" warning ->
System Settings "Open Anyway" -> Mac password -> installer -> success) with
fully fake data and step captions. Emits media/install-demo.gif + .mp4.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import demo_common as C

W, H = 1000, 640
CONTENT_H = H - 86          # area above the caption bar
OUT = "/Users/maxwell/Documents/idears/si4-apps/si4lockmac/si4lockmac-release/media/install-demo"

frames = []
def add(img, ms): frames.append((img.copy(), ms))
def lerp(a, b, t): return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def base(cap_idx, cap_title, cap_body, clock="09:20"):
    img = C.desktop(W, H)
    d = ImageDraw.Draw(img)
    C.menubar(d, W, clock)
    return img, d


def cap(d, idx, title, body):
    C.caption(d, W, H, title, body, idx=idx, total=6)


# ── Scene 1: GitHub Release — download the pkg ───────────────────────────────
def scene_release():
    def draw(cursor_xy):
        img, d = base(1, "从 GitHub Release 下载", "Well365/si4lockmac · Releases")
        wx, wy, ww, wh = 90, 70, 820, CONTENT_H - 120
        C.window(d, wx, wy, ww, wh, "si4lockmac — Releases")
        # url bar
        d.rounded_rectangle([wx + 60, wy + 56, wx + ww - 60, wy + 84], radius=8, fill=(255, 255, 255))
        C.draw_text(d, wx + 76, wy + 60, "github.com/Well365/si4lockmac/releases", 15, C.SUBINK)
        # release heading
        C.draw_text(d, wx + 40, wy + 110, "si4lockmac 0.5.0", 26, C.INK)
        d.rounded_rectangle([wx + 300, wy + 116, wx + 380, wy + 142], radius=12, fill=(225, 245, 230))
        C.draw_text(d, wx + 312, wy + 119, "Latest", 15, C.GREEN)
        C.draw_text(d, wx + 40, wy + 150, "macOS privacy veil · Homebrew: brew install --cask Well365/lockmac/lockmac", 15, C.SUBINK)
        # assets box
        ax, ay, aw = wx + 40, wy + 196, ww - 80
        d.rounded_rectangle([ax, ay, ax + aw, ay + 150], radius=10, outline=(220, 222, 228), width=2)
        C.draw_text(d, ax + 16, ay + 14, "Assets", 16, C.INK)
        d.line([ax, ay + 44, ax + aw, ay + 44], fill=(230, 232, 238))
        # the highlighted pkg asset row
        d.rounded_rectangle([ax + 6, ay + 52, ax + aw - 6, ay + 92], radius=8, fill=(235, 244, 255))
        C.lock_icon(d, ax + 30, ay + 72, 16, C.BLUE)
        C.draw_text(d, ax + 52, ay + 62, "lockmac-0.5.0.pkg", 17, C.BLUE)
        C.draw_text(d, ax + aw - 130, ay + 64, "6.3 MB", 15, C.SUBINK)
        C.draw_text(d, ax + 52, ay + 104, "Source code (zip)", 16, C.SUBINK)
        cap(d, 1, "下载安装包", "在 Release 页点 lockmac-0.5.0.pkg 下载")
        if cursor_xy: C.cursor(d, *cursor_xy)
        return img, (ax + 52, ay + 72)

    _, target = draw((500, 400))
    for i in range(16):
        c = lerp((500, 420), target, i / 15)
        add(draw(c)[0], 50)
    # click flash
    add(draw(target)[0], 500)
    img, _ = draw(target); d = ImageDraw.Draw(img)
    d.ellipse([target[0] - 18, target[1] - 18, target[0] + 18, target[1] + 18], outline=C.BLUE, width=3)
    add(img, 250)
    add(draw(target)[0], 400)


# ── Scene 2: Finder — double-click the pkg ───────────────────────────────────
def scene_finder():
    def draw(cursor_xy, opened=False):
        img, d = base(2, "双击 .pkg", "Downloads")
        wx, wy, ww, wh = 150, 90, 700, CONTENT_H - 160
        C.window(d, wx, wy, ww, wh, "下载")
        # sidebar
        d.rectangle([wx, wy + 44, wx + 150, wy + wh], fill=(241, 241, 244))
        for i, lab in enumerate(["最近使用", "应用程序", "桌面", "下载", "iCloud 云盘"]):
            col = C.BLUE if lab == "下载" else (90, 92, 100)
            if lab == "下载":
                d.rounded_rectangle([wx + 8, wy + 60 + i * 34, wx + 142, wy + 90 + i * 34], radius=6, fill=(220, 224, 232))
            C.draw_text(d, wx + 22, wy + 66 + i * 34, lab, 15, col)
        # the pkg "box" icon, centered in content
        bx, by = wx + 380, wy + 130
        # cardboard box
        d.polygon([(bx, by + 40), (bx + 70, by + 10), (bx + 140, by + 40), (bx + 70, by + 70)], fill=(214, 170, 110))
        d.polygon([(bx, by + 40), (bx + 70, by + 70), (bx + 70, by + 150), (bx, by + 120)], fill=(180, 134, 80))
        d.polygon([(bx + 70, by + 70), (bx + 140, by + 40), (bx + 140, by + 120), (bx + 70, by + 150)], fill=(198, 152, 96))
        d.polygon([(bx + 20, by - 6), (bx + 70, by + 10), (bx + 70, by + 38), (bx + 20, by + 22)], fill=(240, 210, 110, 200))
        C.draw_text(d, wx + 240, wy + wh - 90, "lockmac-0.5.0.pkg", 18, C.INK)
        C.draw_text(d, wx + 240, wy + wh - 62, "安装器 flat 软件包 — 6.3 MB", 15, C.SUBINK)
        cap(d, 2, "双击安装包", "在「下载」里双击 lockmac-0.5.0.pkg")
        if cursor_xy: C.cursor(d, *cursor_xy)
        return img

    target = (550, 260)
    for i in range(12):
        c = lerp((400, 420), target, i / 11)
        add(draw(c), 55)
    # double-click pulses
    for _ in range(2):
        img = draw(target); d = ImageDraw.Draw(img)
        d.ellipse([target[0] - 16, target[1] - 16, target[0] + 16, target[1] + 16], outline=(255, 255, 255), width=3)
        add(img, 130); add(draw(target), 130)
    add(draw(target), 300)


# ── Scene 3: "未打开" Gatekeeper warning ──────────────────────────────────────
def scene_warning():
    def draw(cursor_xy, highlight=False):
        img, d = base(3, "首次会提示「未打开」", "这是未签名提示,不是病毒")
        # dialog
        dw, dh = 460, 250
        dx, dy = (W - dw) // 2, 110
        d.rounded_rectangle([dx, dy, dx + dw, dy + dh], radius=18, fill=(250, 250, 252))
        C.warning_triangle(d, dx + 70, dy + 60, 64)
        C.draw_text(d, dx + 120, dy + 36, '未打开 "lockmac-0.5.0.pkg"', 19, C.INK)
        C.draw_text(d, dx + 120, dy + 72, "Apple 无法验证此 App 是否包含", 15, (90, 92, 100))
        C.draw_text(d, dx + 120, dy + 96, "恶意软件。", 15, (90, 92, 100))
        # buttons
        b1 = C.button(d, dx + 60, dy + 170, 160, 44, "完成", "plain")
        if highlight:
            d.rounded_rectangle([b1[0] - 4, b1[1] - 4, b1[0] + b1[2] + 4, b1[1] + b1[3] + 4], radius=26, outline=C.BLUE, width=3)
        C.button(d, dx + 250, dy + 170, 160, 44, "移到废纸篓", "primary")
        cap(d, 3, "点「完成」——别移废纸篓", "未签名提示而已,先关掉,下一步去授权打开")
        if cursor_xy: C.cursor(d, *cursor_xy)
        return img, (dx + 140, dy + 192)

    _, target = draw(None)
    add(draw((500, 420))[0], 400)
    for i in range(12):
        c = lerp((500, 420), target, i / 11)
        add(draw(c, highlight=i > 7)[0], 55)
    add(draw(target, highlight=True)[0], 700)


# ── Scene 4: System Settings — Open Anyway ───────────────────────────────────
def scene_openanyway():
    def draw(cursor_xy, highlight=False):
        img, d = base(4, "系统设置 ▸ 隐私与安全性", "点「仍要打开」")
        wx, wy, ww, wh = 120, 80, 760, CONTENT_H - 140
        C.window(d, wx, wy, ww, wh, "隐私与安全性")
        # sidebar
        d.rectangle([wx, wy + 44, wx + 200, wy + wh], fill=(241, 241, 244))
        for i, lab in enumerate(["定位服务", "通讯录", "辅助功能", "完全磁盘访问", "安全性"]):
            sel = lab == "安全性"
            if sel:
                d.rounded_rectangle([wx + 10, wy + 64 + i * 40, wx + 190, wy + 100 + i * 40], radius=7, fill=(220, 224, 232))
            C.draw_text(d, wx + 26, wy + 72 + i * 40, lab, 15, C.BLUE if sel else (90, 92, 100))
        # main: the "blocked" banner
        mx = wx + 230
        C.draw_text(d, mx, wy + 70, "安全性", 18, C.INK)
        d.rounded_rectangle([mx, wy + 110, wx + ww - 30, wy + 180], radius=10, fill=(255, 255, 255))
        C.draw_text(d, mx + 16, wy + 124, '已阻止使用 "lockmac-0.5.0.pkg",', 15, (70, 72, 80))
        C.draw_text(d, mx + 16, wy + 148, "因为来自身份不明的开发者。", 15, (70, 72, 80))
        b = C.button(d, wx + ww - 200, wy + 126, 150, 40, "仍要打开", "plain", size=16)
        if highlight:
            d.rounded_rectangle([b[0] - 4, b[1] - 4, b[0] + b[2] + 4, b[1] + b[3] + 4], radius=24, outline=C.BLUE, width=3)
        cap(d, 4, "点「仍要打开」", "系统设置底部 → 隐私与安全性 → 仍要打开")
        if cursor_xy: C.cursor(d, *cursor_xy)
        return img, (b[0] + b[2] // 2, b[1] + b[3] // 2)

    _, target = draw(None)
    add(draw((480, 420))[0], 400)
    for i in range(14):
        c = lerp((480, 420), target, i / 13)
        add(draw(c, highlight=i > 9)[0], 52)
    add(draw(target, highlight=True)[0], 650)


# ── Scene 5: Mac password sheet ──────────────────────────────────────────────
def scene_password():
    def draw(cursor_xy, dots):
        img, d = base(5, "输入 Mac 密码确认", "")
        dw, dh = 440, 220
        dx, dy = (W - dw) // 2, 120
        d.rounded_rectangle([dx, dy, dx + dw, dy + dh], radius=18, fill=(248, 248, 250))
        C.lock_icon(d, dx + dw // 2, dy + 48, 30, (90, 92, 100))
        C.draw_text(d, dx, dy + 78, "「设置」想要进行更改。", 17, C.INK, center_w=dw)
        C.draw_text(d, dx, dy + 104, "输入你的密码以允许此操作。", 14, C.SUBINK, center_w=dw)
        d.rounded_rectangle([dx + 70, dy + 132, dx + dw - 70, dy + 164], radius=8, fill=(255, 255, 255), outline=(200, 202, 210), width=1)
        C.draw_text(d, dx + 84, dy + 138, "•" * dots, 22, (90, 92, 100))
        C.button(d, dx + dw // 2 - 75, dy + 178, 150, 38, "好", "primary", size=16)
        cap(d, 5, "输入开机密码", "用随机示意字符代替真实密码")
        if cursor_xy: C.cursor(d, *cursor_xy)
        return img

    for dots in range(0, 9):
        add(draw((640, 360), dots), 110)
    add(draw(None, 8), 600)


# ── Scene 6: Installer wizard + success ──────────────────────────────────────
def scene_installer():
    steps = ["介绍", "目的宗卷", "安装类型", "安装", "摘要"]
    def draw(active, progress, done=False):
        img, d = base(6, "安装向导自动完成", "")
        wx, wy, ww, wh = 140, 90, 720, CONTENT_H - 160
        C.window(d, wx, wy, ww, wh, "安装 lockmac")
        d.rectangle([wx, wy + 44, wx + 220, wy + wh], fill=(238, 238, 242))
        for i, s in enumerate(steps):
            on = i <= active
            col = C.INK if on else (170, 172, 180)
            d.ellipse([wx + 24, wy + 70 + i * 42, wx + 36, wy + 82 + i * 42], fill=C.BLUE if i == active else (200, 202, 210) if on else (220, 222, 228))
            C.draw_text(d, wx + 50, wy + 68 + i * 42, s, 16, col)
        mx = wx + 250
        if not done:
            C.draw_text(d, mx, wy + 80, "正在安装…", 18, C.INK)
            d.rounded_rectangle([mx, wy + 120, wx + ww - 40, wy + 138], radius=9, fill=(225, 227, 232))
            d.rounded_rectangle([mx, wy + 120, mx + int((wx + ww - 40 - mx) * progress), wy + 138], radius=9, fill=C.BLUE)
        else:
            C.check_circle(d, (mx + wx + ww - 40) // 2, wy + 130, 46)
            C.draw_text(d, mx, wy + 196, "安装成功。", 22, C.INK, center_w=(wx + ww - 40 - mx))
            C.button(d, wx + ww - 150, wy + wh - 56, 110, 40, "关闭", "primary", size=16)
        cap(d, 6, "安装成功", "菜单栏出现锁图标,设置向导自动打开")
        return img

    for k in range(0, 11):
        active = min(3, k // 3)
        add(draw(active, k / 10), 130)
    add(draw(4, 1.0, done=True), 2200)


# ── End card ─────────────────────────────────────────────────────────────────
def end_card():
    img = C.desktop(W, H); d = ImageDraw.Draw(img)
    C.menubar(d, W, "09:21")
    C.lock_icon(d, W - 60, 14, 16, (235, 235, 240))
    d.ellipse([W - 88, 2, W - 36, 50], outline=C.ACCENT, width=2)
    C.check_circle(d, W // 2, 220, 60)
    C.draw_text(d, 0, 320, "安装完成", 34, (245, 247, 252), center_w=W)
    C.draw_text(d, 0, 372, "菜单栏出现锁图标 — 设置向导会自动打开", 20, C.ACCENT, center_w=W)
    C.draw_text(d, 0, 410, "Installed · the lock appears in your menu bar", 16, (150, 160, 185), center_w=W)
    C.caption(d, W, H, "下一步:设置向导", "设密码 → 绑定 Telegram → 2FA(见 setup 演示)")
    return img


scene_release()
scene_finder()
scene_warning()
scene_openanyway()
scene_password()
scene_installer()
add(end_card(), 2600)

C.export(frames, OUT, fps=20)

#!/bin/bash
# Double-click to install lockmac. You will be asked for your Mac password.
clear
echo "════════════════════════════════════════"
echo "  lockmac installer"
echo "  安装 lockmac — 接下来请输入你的 Mac 密码"
echo "════════════════════════════════════════"

# Resolve this script's real directory (follows symlinks), independent of the
# working directory a double-click gives us.
SRC="${BASH_SOURCE[0]}"
while [ -h "$SRC" ]; do D="$(cd -P "$(dirname "$SRC")" && pwd)"; SRC="$(readlink "$SRC")"; [[ $SRC != /* ]] && SRC="$D/$SRC"; done
HERE="$(cd -P "$(dirname "$SRC")" && pwd)"

# Auto-locate the .pkg: next to this script first, then common download spots.
PKG=""
for d in "$HERE" "$HERE/dist" "$HOME/Downloads" "$HOME/Desktop" "$PWD"; do
  c=$(ls -t "$d"/lockmac-*.pkg 2>/dev/null | head -1)
  [ -n "$c" ] && { PKG="$c"; break; }
done
if [ -z "$PKG" ]; then echo "✗ Couldn't find lockmac-*.pkg near this script."; read -n1 -p "Press any key…"; exit 1; fi
echo "  pkg: $PKG"

# ~/Documents, ~/Desktop, ~/Downloads are TCC-protected — a privileged installer
# may be denied access there. Copy to /tmp (unprotected) and install from there.
TMP="/tmp/lockmac-install-$$.pkg"
cp "$PKG" "$TMP" && xattr -dr com.apple.quarantine "$TMP" 2>/dev/null
osascript - "$TMP" <<'APPLESCRIPT' \
  || sudo installer -pkg "$TMP" -target / \
  || { echo "✗ Install failed."; rm -f "$TMP"; read -n1 -p "Press any key…"; exit 1; }
on run argv
  set p to item 1 of argv
  do shell script "installer -pkg " & quoted form of p & " -target /" with administrator privileges
end run
APPLESCRIPT
rm -f "$TMP"
open /Applications/lockmac.app 2>/dev/null
echo ""
echo "✓ Installed. lockmac is in your menu bar (🔒) — the setup wizard will open."
echo "✓ 安装完成。菜单栏会出现 🔒,引导会自动弹出。"
read -n1 -p "Press any key to close…"

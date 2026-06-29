#!/bin/bash
clear
echo "════════════════════════════════════════"
echo "  Uninstall lockmac · 卸载 lockmac"
echo "  This removes the app, services, AND your config (password/Telegram token)."
echo "  将删除 App、服务,以及配置(密码 / Telegram token)。"
echo "════════════════════════════════════════"
read -p "Type 'yes' to continue / 输入 yes 继续: " ans
[ "$ans" = "yes" ] || { echo "Cancelled."; read -n1 -p "Press any key…"; exit 0; }
uid=$(id -u)
/usr/local/bin/lockmac stop 2>/dev/null
for a in com.lockmac com.lockmac.tglisten com.lockmac.tglisten.watchdog com.lockmac.menubar; do
  launchctl bootout "gui/$uid/$a" 2>/dev/null
  rm -f "$HOME/Library/LaunchAgents/$a.plist"
done
pkill -9 -f "lockmac-menubar|lockmac/overlay|from lockmac.cli|/Applications/lockmac.app" 2>/dev/null
rm -rf "$HOME/.config/lockmac" "$HOME/.cache/lockmac"
osascript -e 'do shell script "rm -rf /usr/local/bin/lockmac /usr/local/lib/lockmac /Applications/lockmac.app; pkgutil --forget com.lockmac.pkg" with administrator privileges' \
  || sudo sh -c 'rm -rf /usr/local/bin/lockmac /usr/local/lib/lockmac /Applications/lockmac.app; pkgutil --forget com.lockmac.pkg'
echo ""
echo "✓ lockmac fully removed. / 已彻底卸载。"
read -n1 -p "Press any key to close…"

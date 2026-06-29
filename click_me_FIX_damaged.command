#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
clear
echo "Removing the 'damaged' / quarantine flag from:"
echo "  $DIR"
xattr -dr com.apple.quarantine "$DIR" 2>/dev/null
echo "✓ Done. Now double-click click_me_Install_lockmac.command — no more 'damaged' prompt."
echo "✓ 完成。现在双击 click_me_Install_lockmac.command 就不会再提示损坏了。"
read -n1 -p "Press any key to close…"

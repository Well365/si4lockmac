lockmac — install / 安装 / インストール
══════════════════════════════════════
1) Double-click  click_me_Install_lockmac.command
2) If macOS says "damaged / cannot be opened" — IGNORE it, close the dialog.
3) System Settings → Privacy & Security → bottom → "Open Anyway",
   then "Open Anyway" again, enter your Mac password.
   → 🔒 appears in the menu bar; the setup wizard opens.

1) 双击 click_me_Install_lockmac.command
2) 若提示「已损坏 / 无法打开」——别管它,关掉弹窗。
3) 系统设置 → 隐私与安全性 → 拉到底 → 点「仍要打开」,
   再点一次「仍要打开」,输入 Mac 密码 → 菜单栏出现 🔒。

Tired of the "damaged" prompt? Remove the quarantine flag once, then just
double-click. Open Terminal, type  bash  + a space, then DRAG this folder in,
add  /*  and press Return — or paste (replace the path with this folder):
   xattr -dr com.apple.quarantine "<this folder>"
(Or in Terminal:  bash "click_me_FIX_damaged.command"  — strips it for you.)

嫌「损坏」提示烦?去掉隔离标记一次,之后直接双击即可。打开「终端」,
输入  bash  和一个空格,把本文件夹拖进去,末尾加  /*  回车;或直接:
   xattr -dr com.apple.quarantine "<本文件夹>"
(或在终端运行:  bash "click_me_FIX_damaged.command" )

⭐ Full illustrated guide (中/EN/日):  open  how-to-install.html
Uninstall: double-click  click_me_Uninstall_lockmac.command
More guides: usage-gui.html · usage-command.html (all 中/EN/日).

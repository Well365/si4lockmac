cask "lockmac" do
  version "0.5.0"
  sha256 "d621a5a900c5953f58eaea4743ee0187b5acf1bfd623e676651bba8c076c7d95"

  url "https://github.com/Well365/si4lockmac/releases/download/v#{version}/lockmac-#{version}.pkg"
  name "lockmac"
  desc "macOS privacy veil with remote lock, dead-man switch, and emergency purge"
  homepage "https://github.com/Well365/si4lockmac"

  # The macOS app targets Ventura and later.
  depends_on macos: ">= :ventura"

  pkg "lockmac-#{version}.pkg"

  uninstall quit:    "com.lockmac.app",
            pkgutil: "com.lockmac.pkg"

  # Remove user data, caches, and any login agents lockmac installs.
  zap trash: [
    "~/.config/lockmac",
    "~/.cache/lockmac",
    "~/Library/LaunchAgents/com.lockmac.*.plist",
  ]
end

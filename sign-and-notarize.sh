#!/usr/bin/env bash
#
# sign-and-notarize.sh — sign, package, notarize and staple the si4lockmac .pkg.
#
# Brand: si4lockmac · CLI command: lockmac · pkg id: com.lockmac.pkg
#
# Pipeline (the order matters — notarization checks the app INSIDE the pkg):
#   1. codesign  lockmac.app   (Developer ID Application + hardened runtime)
#   2. pkgbuild  -> component pkg from the signed app
#   3. productsign  the pkg     (Developer ID Installer)
#   4. notarytool submit --wait (Apple notary service)
#   5. stapler staple           (attach the ticket so offline installs verify)
#
# Usage:
#   ./sign-and-notarize.sh setup-credentials   # one-time: store Apple ID creds
#   ./sign-and-notarize.sh build               # run the full pipeline
#   ./sign-and-notarize.sh verify <pkg>        # re-check signature + notarization
#
# Configure either by editing the block below or via environment variables.
set -euo pipefail

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG — fill these in (or export them before running).
# ─────────────────────────────────────────────────────────────────────────────
APP_PATH="${APP_PATH:-./lockmac.app}"                 # path to the built app bundle
APP_VERSION="${APP_VERSION:-0.5.0}"                   # must match the app's version
PKG_IDENTIFIER="${PKG_IDENTIFIER:-com.lockmac.pkg}"   # keep stable across releases
INSTALL_LOCATION="${INSTALL_LOCATION:-/}"             # app lands in /Applications
OUTPUT_PKG="${OUTPUT_PKG:-lockmac-${APP_VERSION}.pkg}"

# Signing identities — exact names from `security find-identity -v -p codesigning`
APP_SIGN_ID="${APP_SIGN_ID:-Developer ID Application: YOUR NAME (TEAMID)}"
INSTALLER_SIGN_ID="${INSTALLER_SIGN_ID:-Developer ID Installer: YOUR NAME (TEAMID)}"

# Notarization
NOTARY_PROFILE="${NOTARY_PROFILE:-lockmac-notary}"    # keychain profile name
APPLE_ID="${APPLE_ID:-you@example.com}"               # only used by setup-credentials
TEAM_ID="${TEAM_ID:-TEAMID}"                          # only used by setup-credentials
# App-specific password from appleid.apple.com (NOT your Apple ID password).
# Leave empty to be prompted interactively during setup-credentials.
APP_SPECIFIC_PASSWORD="${APP_SPECIFIC_PASSWORD:-}"

# Optional: extra entitlements plist for the app (leave empty if none).
ENTITLEMENTS="${ENTITLEMENTS:-}"

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
log()  { printf '\033[1;34m▸ %s\033[0m\n' "$*"; }
ok()   { printf '\033[1;32m✓ %s\033[0m\n' "$*"; }
die()  { printf '\033[1;31m✗ %s\033[0m\n' "$*" >&2; exit 1; }

require_tool() { command -v "$1" >/dev/null 2>&1 || die "missing tool: $1 (install Xcode command line tools)"; }

check_identity() {
  # $1 = identity substring, $2 = human label
  if ! security find-identity -v -p codesigning 2>/dev/null | grep -qF "$1" \
     && ! security find-identity -v 2>/dev/null | grep -qF "$1"; then
    die "signing identity not found in keychain: \"$1\" ($2).
     List what you have with:  security find-identity -v"
  fi
}

# ─────────────────────────────────────────────────────────────────────────────
# setup-credentials — store Apple ID notarization credentials once.
# ─────────────────────────────────────────────────────────────────────────────
cmd_setup_credentials() {
  require_tool xcrun
  log "Storing notary credentials under keychain profile: $NOTARY_PROFILE"
  if [ -n "$APP_SPECIFIC_PASSWORD" ]; then
    xcrun notarytool store-credentials "$NOTARY_PROFILE" \
      --apple-id "$APPLE_ID" --team-id "$TEAM_ID" --password "$APP_SPECIFIC_PASSWORD"
  else
    # Omitting --password makes notarytool prompt interactively (recommended).
    xcrun notarytool store-credentials "$NOTARY_PROFILE" \
      --apple-id "$APPLE_ID" --team-id "$TEAM_ID"
  fi
  ok "Credentials stored. You can now run: ./sign-and-notarize.sh build"
}

# ─────────────────────────────────────────────────────────────────────────────
# build — the full sign → package → notarize → staple pipeline.
# ─────────────────────────────────────────────────────────────────────────────
cmd_build() {
  require_tool codesign
  require_tool pkgbuild
  require_tool productsign
  require_tool xcrun
  require_tool stapler 2>/dev/null || require_tool xcrun  # stapler is via xcrun on newer macOS

  [ -d "$APP_PATH" ] || die "APP_PATH not found: $APP_PATH
     Point it at your built lockmac.app (set APP_PATH=... )."
  check_identity "$APP_SIGN_ID" "Developer ID Application"
  check_identity "$INSTALLER_SIGN_ID" "Developer ID Installer"

  # 1. Sign the app — deep, hardened runtime, secure timestamp.
  log "Signing app bundle: $APP_PATH"
  local sign_args=(--force --deep --options runtime --timestamp --sign "$APP_SIGN_ID")
  [ -n "$ENTITLEMENTS" ] && sign_args+=(--entitlements "$ENTITLEMENTS")
  codesign "${sign_args[@]}" "$APP_PATH"
  codesign --verify --deep --strict --verbose=2 "$APP_PATH"
  ok "App signed and verified."

  # 2. Build a component pkg from the signed app.
  local staging unsigned_pkg
  staging="$(mktemp -d)"
  mkdir -p "$staging/Applications"
  cp -R "$APP_PATH" "$staging/Applications/"
  unsigned_pkg="$(mktemp -d)/unsigned.pkg"
  log "Building pkg (id=$PKG_IDENTIFIER version=$APP_VERSION)"
  pkgbuild \
    --root "$staging" \
    --identifier "$PKG_IDENTIFIER" \
    --version "$APP_VERSION" \
    --install-location "$INSTALL_LOCATION" \
    "$unsigned_pkg"
  ok "Unsigned pkg built."

  # 3. Sign the pkg with the Developer ID Installer cert.
  log "Signing pkg -> $OUTPUT_PKG"
  productsign --sign "$INSTALLER_SIGN_ID" "$unsigned_pkg" "$OUTPUT_PKG"
  pkgutil --check-signature "$OUTPUT_PKG"
  ok "Pkg signed."

  # 4. Notarize and wait for the result.
  log "Submitting to Apple notary service (this can take a few minutes)…"
  xcrun notarytool submit "$OUTPUT_PKG" --keychain-profile "$NOTARY_PROFILE" --wait \
    || die "Notarization failed. Inspect the log with:
     xcrun notarytool log <submission-id> --keychain-profile $NOTARY_PROFILE"
  ok "Notarization accepted."

  # 5. Staple the ticket and validate.
  log "Stapling ticket"
  xcrun stapler staple "$OUTPUT_PKG"
  xcrun stapler validate "$OUTPUT_PKG"

  # Cleanup temp dirs.
  rm -rf "$staging" "$(dirname "$unsigned_pkg")"

  echo
  ok "Done → $OUTPUT_PKG (signed, notarized, stapled)"
  echo "   sha256: $(shasum -a 256 "$OUTPUT_PKG" | awk '{print $1}')"
  echo "   Update Casks/lockmac.rb with this version + sha256, then push the tap."
}

# ─────────────────────────────────────────────────────────────────────────────
# verify — sanity-check a finished pkg.
# ─────────────────────────────────────────────────────────────────────────────
cmd_verify() {
  local pkg="${1:-$OUTPUT_PKG}"
  [ -f "$pkg" ] || die "pkg not found: $pkg"
  require_tool pkgutil
  log "Installer signature:"
  pkgutil --check-signature "$pkg"
  log "Notarization staple:"
  xcrun stapler validate "$pkg" && ok "Stapled & valid." || die "Not stapled / invalid."
}

# ─────────────────────────────────────────────────────────────────────────────
main() {
  case "${1:-}" in
    setup-credentials) cmd_setup_credentials ;;
    build)             cmd_build ;;
    verify)            shift; cmd_verify "${1:-}" ;;
    *)
      cat >&2 <<EOF
si4lockmac — sign & notarize the .pkg

Usage:
  ./sign-and-notarize.sh setup-credentials   # one-time: store Apple ID creds
  ./sign-and-notarize.sh build               # sign → package → notarize → staple
  ./sign-and-notarize.sh verify [pkg]        # re-check signature + notarization

Before running, edit the CONFIG block at the top (or export the variables):
  APP_PATH, APP_SIGN_ID, INSTALLER_SIGN_ID, APPLE_ID, TEAM_ID
EOF
      exit 1 ;;
  esac
}
main "$@"

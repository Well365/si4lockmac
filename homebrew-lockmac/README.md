# homebrew-lockmac

Homebrew tap for [lockmac](https://github.com/Well365/si4lockmac) — a macOS
privacy veil with remote lock, dead-man switch, and emergency purge.

## Install

```bash
brew install --cask Well365/lockmac/lockmac
```

Or add the tap first, then install by short name:

```bash
brew tap Well365/lockmac
brew install --cask lockmac
```

## Update / uninstall

```bash
brew upgrade --cask lockmac     # update to the latest version
brew uninstall --cask lockmac   # remove the app
brew uninstall --zap --cask lockmac   # also remove config, cache, login agents
```

## Maintainer: cutting a new release

1. Build and notarize the new `lockmac-X.Y.Z.pkg`.
2. Upload it to a GitHub Release on `Well365/si4lockmac` tagged `vX.Y.Z`.
3. Compute the checksum: `shasum -a 256 lockmac-X.Y.Z.pkg`.
4. Bump `version` and `sha256` in `Casks/lockmac.rb`, then commit and push.

> The `.pkg` must be signed with a Developer ID and notarized, otherwise
> Gatekeeper blocks the `installer` step and `brew install --cask` fails for
> users. An unsigned pkg only works with a manual "Open Anyway".

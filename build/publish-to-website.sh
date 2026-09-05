#!/usr/bin/env bash
# Copy the rendered site to the personal website repo, so that it is served at
# https://dennisfeehan.org/film/ . Nothing links to it; a noindex tag is
# injected so search engines stay away.
#
# The website repo keeps two copies, following the same pattern as the syllabi:
#   film/      - source-side, listed under `resources` in _quarto.yml, so a
#                clean rebuild of the site regenerates docs/film
#   docs/film/ - the rendered site that github pages actually serves
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
site="${WEBSITE_REPO:-$HOME/Dropbox/website}"

[ -d "$site" ] || { echo "website repo not found: $site" >&2; exit 1; }

for dest in "$site/film" "$site/docs/film"; do
  mkdir -p "$dest"
  cp "$repo"/*.pdf "$dest/"
  # inject <meta name="robots" content="noindex"> right after <head>
  sed 's|<html lang="en"><head><meta charset="utf-8">|<html lang="en"><head><meta charset="utf-8">\
<meta name="robots" content="noindex,nofollow">|' "$repo/index.html" > "$dest/index.html"
  grep -q 'name="robots"' "$dest/index.html" || { echo "noindex tag not injected" >&2; exit 1; }
done

echo "copied to $site/film and $site/docs/film -- commit and push the website repo"

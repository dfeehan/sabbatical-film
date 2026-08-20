#!/usr/bin/env bash
# Regenerate index.html and the three PDFs from the Markdown sources.
# Requires: pandoc, xelatex (texlive-xetex), python3.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(dirname "$HERE")"

pdf () {  # $1 = markdown basename (no ext), $2 = date line
  python3 - "$REPO/$1.md" <<'PY'
import sys, pathlib
lines = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8").split("\n")
title = lines[0].lstrip("# ").strip()
cut, sub = 0, ""
for i, l in enumerate(lines[:8]):
    s = l.strip()
    if s.startswith("**") and s.endswith("**") and len(s) > 4:
        sub = s.strip("*"); cut = i; break
sub = sub.replace("~", "approx. ")
d = pathlib.Path("/tmp/sf-build"); d.mkdir(exist_ok=True)
(d/"body.md").write_text("\n".join(lines[cut+1:]), encoding="utf-8")
(d/"title.txt").write_text(title, encoding="utf-8")
(d/"sub.txt").write_text(sub, encoding="utf-8")
PY
  pandoc /tmp/sf-build/body.md -o "$REPO/$1.pdf" \
    --pdf-engine=xelatex --include-in-header="$HERE/header.tex" \
    --toc --toc-depth=2 -V documentclass=article -V fontsize=11pt \
    -V title="$(cat /tmp/sf-build/title.txt)" \
    -V subtitle="$(cat /tmp/sf-build/sub.txt)" \
    -V date="$2" -V colorlinks=true --shift-heading-level-by=-1
  echo "  built $1.pdf"
}

pdf sabbatical-film-syllabus "Prepared 19 August 2026"
pdf where-to-watch           "Availability checked 17 August 2026"
pdf syllabus-comparison      "Compiled 19 August 2026"
python3 "$HERE/mkhtml.py"
echo "done."

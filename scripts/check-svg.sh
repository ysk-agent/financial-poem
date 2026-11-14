#!/bin/sh
# Validate every chart SVG as XML before publishing.
# A raw '&' (e.g. "M&A") makes the file invalid XML: GitHub Pages still
# serves it with HTTP 200, but browsers refuse to render it as an image.
fail=0
for f in public/charts/*.svg; do
  python3 -c "import xml.dom.minidom,sys; xml.dom.minidom.parse(sys.argv[1])" "$f" 2>/dev/null || { echo "INVALID SVG: $f"; fail=1; }
done
exit $fail

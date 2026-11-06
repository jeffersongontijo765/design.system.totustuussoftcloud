#!/usr/bin/env bash
# empacotar.sh — gera entregas/layout-main.zip com o kit e o design system que ele usa.
#
# Conteúdo do zip:
#   totustuus-layout-main/
#   ├── layout-main/            (este kit, sem este script)
#   └── components/             (ttsc.css e os 4 arquivos que ele importa)
# Assim o caminho ../components/ttsc.css do index.html funciona igual ao repositório.
#
# Uso (na raiz do repositório ou em qualquer pasta):  bash layout-main/empacotar.sh
set -euo pipefail

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

DEST="$TMP/totustuus-layout-main"
mkdir -p "$DEST/components" "$RAIZ/entregas"

cp -R "$RAIZ/layout-main" "$DEST/layout-main"
rm -f "$DEST/layout-main/empacotar.sh"
for f in ttsc.css __tokens.css bundle.css ttsc-theme-bridge.css ttsc-responsive.css; do
  cp "$RAIZ/components/$f" "$DEST/components/$f"
done

rm -f "$RAIZ/entregas/layout-main.zip"
(cd "$TMP" && zip -rq "$RAIZ/entregas/layout-main.zip" totustuus-layout-main)
echo "gerado: entregas/layout-main.zip"

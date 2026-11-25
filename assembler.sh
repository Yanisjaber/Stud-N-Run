#!/usr/bin/env bash
# Assemble ce qui est publié sur GitHub Pages (https://yanisjaber.github.io/Stud-N-Run/) :
#   /        → le site d'organisation (dossier orga/, copie du build de tableau-de-bord)
#   /site/   → le site public de la course (dossier dist/, produit par build.py)
# Les anciennes adresses du site public (ecoles.html, confidentialite.html…) redirigent vers /site/,
# et ses fichiers (PDF, images…) restent aussi servis à leur ancienne place pour ne casser aucun lien.
set -euo pipefail
sortie="${1:-_site}"
rm -rf "$sortie" && mkdir -p "$sortie/site"
cp -R dist/. "$sortie/site/"
(cd dist && find . -type f ! -name '*.html' ! -name '.DS_Store') | while read -r f; do
  mkdir -p "$sortie/$(dirname "$f")" && cp "dist/$f" "$sortie/$f"
done
(cd dist && find . -type f -name '*.html' ! -path './index.html') | sed 's|^\./||' | while read -r p; do
  remonte=$(printf '%s' "$p" | awk -F/ '{for(i=1;i<NF;i++) printf "../"}')
  cible="${remonte}site/$p"
  mkdir -p "$sortie/$(dirname "$p")"
  cat > "$sortie/$p" <<HTML
<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Stud'N Run</title>
<link rel="canonical" href="$cible"><meta http-equiv="refresh" content="0; url=$cible">
<script>location.replace("$cible" + location.search + location.hash)</script></head>
<body><p>Cette page a déménagé : <a href="$cible">continuer vers le site Stud'N Run</a>.</p></body></html>
HTML
done
cp -R orga/. "$sortie/"
find "$sortie" -name '.DS_Store' -delete

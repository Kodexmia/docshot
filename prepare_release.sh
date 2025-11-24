#!/usr/bin/env bash
set -euo pipefail

# Prepare a clean source bundle for DocShot and a zip ready for GitHub release.
# Run this from the repo root (same folder as VERSION, README.md, app/).

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Read version from VERSION file
VERSION_FILE="$ROOT/VERSION"
if [[ ! -f "$VERSION_FILE" ]]; then
  echo "ERROR: VERSION file not found at $VERSION_FILE"
  exit 1
fi

VERSION="$(tr -d '\r\n' < "$VERSION_FILE")"
echo "Preparing DocShot source release v$VERSION"

RELEASE_DIR="$ROOT/release"
CLEAN_DIR="$RELEASE_DIR/docshot-$VERSION"

# Clean previous release folders/zips
echo "Cleaning old release directory..."
rm -rf "$CLEAN_DIR"
mkdir -p "$CLEAN_DIR"

echo "Copying core files..."
# Core text files
cp "$ROOT/README.md"        "$CLEAN_DIR"/ 2>/dev/null || true
cp "$ROOT/INSTALL.md"       "$CLEAN_DIR"/ 2>/dev/null || true
cp "$ROOT/README_FOR_USERS.txt" "$CLEAN_DIR"/ 2>/dev/null || true
cp "$ROOT/LICENSE"          "$CLEAN_DIR"/ 2>/dev/null || true
cp "$ROOT/VERSION"          "$CLEAN_DIR"/
cp "$ROOT/requirements.txt" "$CLEAN_DIR"/
cp "$ROOT/DocShot.spec"     "$CLEAN_DIR"/
cp "$ROOT/BUILD_EXE.bat"    "$CLEAN_DIR"/
cp "$ROOT/start.bat"        "$CLEAN_DIR"/ 2>/dev/null || true
cp "$ROOT/start.sh"         "$CLEAN_DIR"/ 2>/dev/null || true

# Optional: changelogs and docs
cp "$ROOT"/CHANGELOG_V*.md "$CLEAN_DIR"/ 2>/dev/null || true
cp "$ROOT"/CONTRIBUTING.md "$CLEAN_DIR"/ 2>/dev/null || true

echo "Copying app source..."
# Copy app/ but strip caches and temporary files
rsync -a \
  --exclude "__pycache__" \
  --exclude "*.pyc" \
  "$ROOT/app" "$CLEAN_DIR/"

echo "Source tree for v$VERSION prepared in:"
echo "  $CLEAN_DIR"
echo

# Create a source zip for attaching to GitHub release
echo "Creating source zip..."
mkdir -p "$RELEASE_DIR"
(
  cd "$RELEASE_DIR"
  ZIP_NAME="DocShot_${VERSION}_source.zip"
  rm -f "$ZIP_NAME"
  zip -r "$ZIP_NAME" "docshot-$VERSION" >/dev/null
  echo "Created release/${ZIP_NAME}"
)

cat <<EOF

Next steps:

1. Commit and push to GitHub:

   cd "$ROOT"
   git status
   git add .
   git commit -m "Release v$VERSION"
   git push origin main    # or master, depending on your branch

2. On GitHub (https://github.com/Kodexmia/docshot):
   - Create a new Release tagged "v$VERSION"
   - Upload release/DocShot_${VERSION}_source.zip as an asset

Only the minimal source, docs and build scripts are included in that zip.
Local artefacts (.venv, build, dist, DocShot_Portable, old zips) stay out.

EOF

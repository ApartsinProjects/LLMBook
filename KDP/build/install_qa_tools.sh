#!/usr/bin/env bash
# Install the QA pipeline's external dependencies: a portable JRE and
# EPUBCheck. These live under KDP/build/tools/ which is .gitignored.
# Re-run this on any fresh checkout that needs to run run_qa_pipeline.py.
#
# Total download: ~80 MB.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TOOLS="$ROOT/KDP/build/tools"
mkdir -p "$TOOLS"
cd "$TOOLS"

JRE_VERSION="21.0.11+10"
JRE_DIR="jdk-${JRE_VERSION}-jre"
EPUBCHECK_VERSION="5.2.1"
EPUBCHECK_DIR="epubcheck-${EPUBCHECK_VERSION}"

# 1. Portable JRE (Eclipse Temurin) -- only needed for EPUBCheck.
if [[ -d "$JRE_DIR" ]]; then
    echo "[skip] JRE already installed at $TOOLS/$JRE_DIR"
else
    echo "[download] Temurin JRE 21..."
    curl -sSL -o jre.zip \
        "https://api.adoptium.net/v3/binary/latest/21/ga/windows/x64/jre/hotspot/normal/eclipse"
    unzip -q jre.zip
    rm jre.zip
    echo "[ok] JRE installed at $TOOLS/$JRE_DIR"
fi

# 2. EPUBCheck 5.2.1
if [[ -d "$EPUBCHECK_DIR" ]]; then
    echo "[skip] EPUBCheck already installed at $TOOLS/$EPUBCHECK_DIR"
else
    echo "[download] EPUBCheck $EPUBCHECK_VERSION..."
    curl -sSL -o epubcheck.zip \
        "https://github.com/w3c/epubcheck/releases/download/v${EPUBCHECK_VERSION}/epubcheck-${EPUBCHECK_VERSION}.zip"
    unzip -q epubcheck.zip
    rm epubcheck.zip
    echo "[ok] EPUBCheck installed at $TOOLS/$EPUBCHECK_DIR"
fi

# 3. Smoke test
echo ""
echo "Smoke test:"
"$TOOLS/$JRE_DIR/bin/java.exe" -jar "$TOOLS/$EPUBCHECK_DIR/epubcheck.jar" --version
echo ""
echo "Ready. Run QA pipeline with:"
echo "  python KDP/build/run_qa_pipeline.py"

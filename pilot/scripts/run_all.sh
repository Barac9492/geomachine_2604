#!/bin/bash
# run_all.sh — Run all 4 engine queries and generate combined pilot log
#
# Runs: Claude API → OpenAI API → Perplexity API → Gemini API
# Each produces a per-engine markdown log in pilot/logs/
# Then merges into a combined pilot log with citability matrix
#
# Usage:
#   ./pilot/scripts/run_all.sh                # full run (all 4 engines)
#   ./pilot/scripts/run_all.sh --engines claude,perplexity  # subset

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SCRIPTS_DIR="$REPO_ROOT/pilot/scripts"
LOGS_DIR="$REPO_ROOT/pilot/logs"
VENV_PYTHON="$HOME/Content_VentureOracle/.venv/bin/python"
DATE=$(date '+%Y-%m-%d')

# Fallback to system python if venv doesn't exist
if [[ ! -f "$VENV_PYTHON" ]]; then
    VENV_PYTHON="python3"
fi

# Load env (grep specific keys to avoid spaces-in-paths breaking source)
if [[ -f "$HOME/Content_VentureOracle/.env" ]]; then
    export ANTHROPIC_API_KEY=$(grep '^ANTHROPIC_API_KEY=' "$HOME/Content_VentureOracle/.env" | cut -d= -f2-)
    export OPENAI_API_KEY=$(grep '^OPENAI_API_KEY=' "$HOME/Content_VentureOracle/.env" | cut -d= -f2-)
    export PERPLEXITY_API_KEY=$(grep '^PERPLEXITY_API_KEY=' "$HOME/Content_VentureOracle/.env" | cut -d= -f2-)
    export GEMINI_API_KEY=$(grep '^GEMINI_API_KEY=' "$HOME/Content_VentureOracle/.env" | cut -d= -f2-)
fi

mkdir -p "$LOGS_DIR"

echo "╔══════════════════════════════════════════════════════╗"
echo "║  GEOMachine Pilot Run — $DATE                    ║"
echo "║  18 queries × 4 engines = 72 cells                 ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Parse engines
ENGINES="${1:-claude,openai,perplexity,gemini}"
ENGINES="${ENGINES#--engines }"

run_engine() {
    local engine=$1
    local script=$2
    echo "━━━ Running $engine ━━━"
    if $VENV_PYTHON "$SCRIPTS_DIR/$script" 2>&1; then
        echo "✓ $engine complete → $LOGS_DIR/run-$DATE-$engine-api.md"
    else
        echo "✗ $engine failed (check API key)"
    fi
    echo ""
}

START=$(date +%s)

if [[ "$ENGINES" == *"claude"* ]]; then
    run_engine "Claude" "run_claude_api.py"
fi

if [[ "$ENGINES" == *"openai"* ]]; then
    run_engine "OpenAI" "run_openai_api.py"
fi

if [[ "$ENGINES" == *"perplexity"* ]]; then
    run_engine "Perplexity" "run_perplexity_api.py"
fi

if [[ "$ENGINES" == *"gemini"* ]]; then
    run_engine "Gemini" "run_gemini_api.py"
fi

END=$(date +%s)
DURATION=$(( (END - START) / 60 ))

# Generate combined summary
COMBINED="$LOGS_DIR/run-$DATE-combined.md"
echo "Generating combined summary..."

cat > "$COMBINED" << HEADER
# GEO Pilot Run — $DATE (Combined)

**Duration:** ${DURATION} minutes
**Queries:** 18
**Engines:** $(echo $ENGINES | tr ',' ', ')

---

## Per-Engine Logs
HEADER

for engine in claude openai perplexity gemini; do
    LOG="$LOGS_DIR/run-$DATE-$engine-api.md"
    if [[ -f "$LOG" ]]; then
        echo "- [$engine]($LOG) ✓" >> "$COMBINED"
    else
        echo "- $engine: not run" >> "$COMBINED"
    fi
done

echo "" >> "$COMBINED"
echo "## Quick Citability Check" >> "$COMBINED"
echo "" >> "$COMBINED"
echo "Grep for Ethan/TheVentures mentions across all engines:" >> "$COMBINED"
echo '```' >> "$COMBINED"

for engine in claude openai perplexity gemini; do
    LOG="$LOGS_DIR/run-$DATE-$engine-api.md"
    if [[ -f "$LOG" ]]; then
        mentions=$(grep -ci "ethan cho\|theventures\|venture oracle\|조여준\|founder intelligence\|four lenses\|mau trap\|e/d/r" "$LOG" 2>/dev/null || echo "0")
        echo "$engine: $mentions mention(s)" >> "$COMBINED"
    fi
done

echo '```' >> "$COMBINED"
echo "" >> "$COMBINED"
echo "**Next run:** $(date -v+7d '+%Y-%m-%d') (7 days)" >> "$COMBINED"

echo ""
echo "══════════════════════════════════════════════════════"
echo "  DONE in ${DURATION} minutes"
echo "  Combined log: $COMBINED"
echo "══════════════════════════════════════════════════════"

# Update NEXT_RUN.md
cat > "$REPO_ROOT/pilot/NEXT_RUN.md" << EOF
# Next scheduled pilot run

**Date:** $(date -v+7d '+%Y-%m-%d') ($(date -v+7d '+%A'))
**Trigger:** manual or automated via daemon

Run: \`./pilot/scripts/run_all.sh\`

Last run: $DATE (${DURATION} min)
EOF

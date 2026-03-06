#!/usr/bin/env bash
# dev.sh — Start Kamera Quest locally
# Usage: ./dev.sh [--no-web] [--no-cli]
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NO_WEB=false
NO_CLI=false

for arg in "$@"; do
  case $arg in
    --no-web) NO_WEB=true ;;
    --no-cli) NO_CLI=true ;;
  esac
done

# ── Colours ──────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

info()    { echo -e "${CYAN}${BOLD}[kamera]${RESET} $*"; }
success() { echo -e "${GREEN}${BOLD}[kamera]${RESET} $*"; }
warn()    { echo -e "${YELLOW}${BOLD}[kamera]${RESET} $*"; }
die()     { echo -e "${RED}${BOLD}[kamera] ERROR:${RESET} $*" >&2; exit 1; }

# ── Cleanup on exit ───────────────────────────────────────────────────────
PIDS=()
cleanup() {
  echo ""
  warn "Shutting down…"
  for pid in "${PIDS[@]:-}"; do
    kill "$pid" 2>/dev/null || true
  done
  # Kill any leftover emulator processes
  pkill -f "firebase emulators" 2>/dev/null || true
  pkill -f "vite"               2>/dev/null || true
  success "All processes stopped. Goodbye!"
}
trap cleanup EXIT INT TERM

# ── Prereq checks ────────────────────────────────────────────────────────
check_cmd() {
  command -v "$1" &>/dev/null || die "'$1' not found. Install it and re-run.\n  Hint: $2"
}

info "Checking prerequisites…"
check_cmd node    "https://nodejs.org (need v18+)"
check_cmd npm     "Comes with Node.js"
check_cmd firebase "npm install -g firebase-tools  then  firebase login"
check_cmd python3 "https://python.org (need 3.9+)"

NODE_VER=$(node -e "process.stdout.write(process.version.slice(1).split('.')[0])")
[[ "$NODE_VER" -ge 18 ]] || die "Node 18+ required (found v${NODE_VER})"

success "Prerequisites OK (Node v$(node -v), Firebase CLI $(firebase --version | head -1))"

# ── Install dependencies ─────────────────────────────────────────────────
if [[ ! -d "$ROOT/api/node_modules" ]]; then
  info "Installing API dependencies…"
  (cd "$ROOT/api" && npm install --silent)
fi

if [[ "$NO_WEB" == false && ! -d "$ROOT/web/node_modules" ]]; then
  info "Installing web dependencies…"
  (cd "$ROOT/web" && npm install --silent)
fi

# ── .env files ───────────────────────────────────────────────────────────
# NOTE: api/.env is intentionally absent — Firebase Functions emulator crashes on it.
# Middleware values are hardcoded in cors.js and rateLimit.js.
if [[ "$NO_WEB" == false ]]; then
  [[ -f "$ROOT/web/.env" ]] || { warn "web/.env not found — copying from .env.example"; cp "$ROOT/web/.env.example" "$ROOT/web/.env"; }
fi

# ── Firebase emulator ─────────────────────────────────────────────────────
# Service account so the Functions emulator can reach production Firestore
export GOOGLE_APPLICATION_CREDENTIALS="$ROOT/kaaykostore-sa.json"

# Kill any stale emulator/vite processes left over from a previous run
info "Clearing stale processes on ports 5001 and 5173…"
lsof -ti:5001 | xargs kill -9 2>/dev/null || true
lsof -ti:5173 | xargs kill -9 2>/dev/null || true
pkill -f "firebase emulators" 2>/dev/null || true
sleep 1

EMULATOR_LOG="$ROOT/.emulator.log"
info "Starting Firebase emulator (functions)…"
firebase emulators:start --only functions \
  --project kaaykostore \
  > "$EMULATOR_LOG" 2>&1 &
EMULATOR_PID=$!
PIDS+=("$EMULATOR_PID")

# Wait for emulator to be ready
info "Waiting for emulator to be ready…"
for i in $(seq 1 30); do
  if grep -q "All emulators ready" "$EMULATOR_LOG" 2>/dev/null; then
    break
  fi
  sleep 1
  if ! kill -0 "$EMULATOR_PID" 2>/dev/null; then
    echo ""; die "Emulator crashed. Check logs:\n  cat $EMULATOR_LOG"
  fi
done

if ! grep -q "All emulators ready" "$EMULATOR_LOG" 2>/dev/null; then
  warn "Emulator may still be starting — check $EMULATOR_LOG if the API seems unreachable."
fi

success "API ready → http://localhost:5001/kaaykostore/us-central1/api/health"

# ── Web dev server ────────────────────────────────────────────────────────
if [[ "$NO_WEB" == false ]]; then
  WEB_LOG="$ROOT/.web.log"
  info "Starting Vite dev server…"
  (cd "$ROOT/web" && npm run dev > "$WEB_LOG" 2>&1) &
  WEB_PID=$!
  PIDS+=("$WEB_PID")

  # Wait for Vite to print its URL
  for i in $(seq 1 20); do
    if grep -q "localhost" "$WEB_LOG" 2>/dev/null; then break; fi
    sleep 1
  done

  WEB_URL=$(grep -o "http://localhost:[0-9]*" "$WEB_LOG" 2>/dev/null | head -1 || echo "http://localhost:5173")
  success "Web ready → $WEB_URL"
fi

# ── Summary ───────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${BOLD} Kamera Quest — Running Locally${RESET}"
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "  ${CYAN}API${RESET}      http://localhost:5001/kaaykostore/us-central1/api"
[[ "$NO_WEB" == false ]] && echo -e "  ${CYAN}Web${RESET}      ${WEB_URL:-http://localhost:5173}"
echo -e "  ${CYAN}CLI${RESET}      cd cli && python3 kamera_quest_cli.py"
echo -e "  ${CYAN}Logs${RESET}     tail -f $EMULATOR_LOG"
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "  ${YELLOW}Ctrl+C to stop all services${RESET}"
echo ""

# ── Keep alive ────────────────────────────────────────────────────────────
wait

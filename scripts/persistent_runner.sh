#!/bin/bash
# Persistent runner: keeps restarting until all 150 runs are complete
BMAS="$HOME/.openclaw/workspace/BMAS"
LOG="/tmp/bmas-persistent.log"

log() { echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG"; }

log "=== Persistent Runner Started ==="
cd "$BMAS"

while true; do
    DONE=$(find experiments/raw-outputs -name "*.json" 2>/dev/null | wc -l)
    log "Status: $DONE/150 runs complete"

    if [ "$DONE" -ge 150 ]; then
        log "All 150 runs complete. Exiting."
        break
    fi

    log "Starting runner (skip-existing)..."
    python3 src/runner/runner.py --all --skip-existing --timeout 150 >> "$LOG" 2>&1
    EXIT=$?
    log "Runner exited (code $EXIT)"

    DONE=$(find experiments/raw-outputs -name "*.json" 2>/dev/null | wc -l)
    if [ "$DONE" -ge 150 ]; then
        log "All 150 runs complete after exit. Done."
        break
    fi

    log "Restarting in 5s..."
    sleep 5
done

log "=== Persistent Runner Complete: $(find experiments/raw-outputs -name '*.json' | wc -l)/150 ==="

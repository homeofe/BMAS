#!/bin/bash
# Waits for the P6 runner process to exit, then runs finish_pipeline.sh
P6_PID=$1
LOG="/tmp/bmas-watch.log"

if [ -z "$P6_PID" ]; then
    echo "Usage: $0 <P6_PID>"
    exit 1
fi

echo "[$(date '+%H:%M:%S')] Watching P6 (PID $P6_PID)..." | tee "$LOG"

while kill -0 "$P6_PID" 2>/dev/null; do
    sleep 30
    DONE=$(find "$HOME/.openclaw/workspace/BMAS/experiments/raw-outputs" -name "*.json" 2>/dev/null | wc -l)
    echo "[$(date '+%H:%M:%S')] P6 running... $DONE/150 runs done" | tee -a "$LOG"
done

echo "[$(date '+%H:%M:%S')] P6 finished. Starting finish pipeline..." | tee -a "$LOG"
bash "$HOME/.openclaw/workspace/BMAS/scripts/finish_pipeline.sh" 2>&1 | tee -a "$LOG"

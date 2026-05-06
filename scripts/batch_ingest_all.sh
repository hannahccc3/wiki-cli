#!/bin/bash
# Full batch ingest for oldpaper-wiki — all 68 papers
# Uses --merge mode (with fast-path heuristics: skeleton detect + similarity pre-check)

eval "$(~/anaconda3/bin/conda shell hook --bash)"
conda activate base

export MINIMAX_CN_API_KEY='sk-cp-K7RbTraM1PYAIgrF0dIhRwwPwazokVLODrWIX7MdX7ThQrXTIpWI9klOUuKW5ZMKQ0RXT89Dox4ogAk3D9fe_zNJ-M-bEwR-oLuGJ6cf-EVR6Zdk-WUU-VI'

WIKI_CLI="/home/gyt/Documents/Functional_projects/wiki-cli"
WIKI_PATH="/mnt/o/Nanashi/Documents/Wiki/oldpaper-wiki"
SOURCES_DIR="$WIKI_PATH/raw/sources"
LOG="$HOME/.hermes/cron/output/oldpaper-wiki-ingest.log"
LOCK="$WIKI_PATH/.llm-wiki/.project.lock"

rm -f "$LOCK"
mkdir -p "$(dirname "$LOG")"

# Find all hybrid_auto/*.md files
FILES=$(find "$SOURCES_DIR" -mindepth 3 -name "*.md" -type f | grep hybrid_auto | grep -v content_list | sort)
FILE_COUNT=$(echo "$FILES" | wc -l)

echo "=== oldpaper-wiki full ingest (merge mode) ===" > "$LOG"
echo "Start: $(date)" >> "$LOG"
echo "Files: $FILE_COUNT" >> "$LOG"
echo "Merge: true (with fast-path heuristics)" >> "$LOG"
echo "" >> "$LOG"

cd "$WIKI_CLI"

succeeded=0
skipped=0
failed=0
i=0

for fpath in $FILES; do
    i=$((i+1))
    fname=$(basename "$fpath")
    echo "[$i/$FILE_COUNT] $fname ..." >> "$LOG"
    
    rm -f "$LOCK"
    
    python -c "
import sys, time
from wiki_cli.commands.ingest import _get_engine

engine = _get_engine('$WIKI_PATH')
engine.cache.invalidate('$fname')

t0 = time.time()
result = engine.ingest('$fpath', merge=True)
elapsed = time.time() - t0

status = result['status']
pages = len(result.get('output_paths', []))
print(f'  [$status] {pages} pages in {elapsed:.0f}s', flush=True)
sys.exit(0 if status == 'ingested' else 1)
" >> "$LOG" 2>&1

    rc=$?
    if [ $rc -eq 0 ]; then
        succeeded=$((succeeded+1))
    elif [ $rc -eq 2 ]; then
        skipped=$((skipped+1))
    else
        failed=$((failed+1))
    fi
done

echo "" >> "$LOG"
echo "=== Done ===" >> "$LOG"
echo "Succeeded: $succeeded, Skipped: $skipped, Failed: $failed" >> "$LOG"
echo "End: $(date)" >> "$LOG"

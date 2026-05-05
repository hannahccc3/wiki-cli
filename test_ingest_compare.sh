#!/bin/bash
export MINIMAX_CN_API_KEY='sk-cp-K7RbTraM1PYAIgrF0dIhRwwPwazokVLODrWIX7MdX7ThQrXTIpWI9klOUuKW5ZMKQ0RXT89Dox4ogAk3D9fe_zNJ-M-bEwR-oLuGJ6cf-EVR6Zdk-WUU-VI'
rm -f /mnt/o/Nanashi/Documents/Wiki/oldpaper-wiki/.llm-wiki/.project.lock

echo "=== Test 1: --no-merge (no LLM merge, fast path) ==="
python test_ingest.py 2>&1 | grep -E "^(DONE|Removed|page-merge)" | head -5

rm -f /mnt/o/Nanashi/Documents/Wiki/oldpaper-wiki/.llm-wiki/.project.lock
echo ""
echo "=== Test 2: --merge (with LLM merge, full pipeline) ==="
# Modify test_ingest.py to use merge=True
sed 's/merge=False/merge=True/' test_ingest.py > test_ingest_merge.py
python test_ingest_merge.py 2>&1 | grep -E "^(DONE|Removed|page-merge)" | head -5

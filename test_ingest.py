#!/usr/bin/env python
import sys, time, os

# Ensure API key
os.environ['MINIMAX_CN_API_KEY'] = 'sk-cp-K7RbTraM1PYAIgrF0dIhRwwPwazokVLODrWIX7MdX7ThQrXTIpWI9klOUuKW5ZMKQ0RXT89Dox4ogAk3D9fe_zNJ-M-bEwR-oLuGJ6cf-EVR6Zdk-WUU-VI'

# Remove stale lock
lock = '/mnt/o/Nanashi/Documents/Wiki/oldpaper-wiki/.llm-wiki/.project.lock'
if os.path.exists(lock):
    os.remove(lock)
    print(f"Removed stale lock", flush=True)

sys.path.insert(0, '/home/gyt/Documents/Functional_projects/wiki-cli')

from wiki_cli.commands.ingest import _get_engine

engine = _get_engine('/mnt/o/Nanashi/Documents/Wiki/oldpaper-wiki')
engine.cache.invalidate('Anil 等 - Many-shot Jailbreaking.md')

t0 = time.time()
result = engine.ingest(
    '/mnt/o/Nanashi/Documents/Wiki/oldpaper-wiki/raw/sources/Anil 等 - Many-shot Jailbreaking/hybrid_auto/Anil 等 - Many-shot Jailbreaking.md',
    merge=False
)
elapsed = time.time() - t0

print(f"DONE in {elapsed:.1f}s: status={result['status']}, pages={len(result['output_paths'])}", flush=True)
for p in result['output_paths']:
    print(f"  - {p}", flush=True)

#!/usr/bin/env python3
import os
import sys, subprocess, json, time
from pathlib import Path

ROOT = Path(os.environ.get('MOLT_EVO_WORKSPACE', '/root/.openclaw/workspace'))
SCRIPT_DIR = Path(__file__).resolve().parent
QUEUE = ROOT / '.openclaw' / 'molt_evo' / 'message_ingest.log'
QUEUE.parent.mkdir(parents=True, exist_ok=True)

if len(sys.argv) > 1:
    text = ' '.join(sys.argv[1:]).strip()
    if text:
        with QUEUE.open('a', encoding='utf-8') as f:
            f.write(text.replace('\n', ' ') + '\n')
        print('queued')
        raise SystemExit(0)

if not QUEUE.exists():
    print('no_queue')
    raise SystemExit(0)

lines = [line.strip() for line in QUEUE.read_text(encoding='utf-8').splitlines() if line.strip()]
if not lines:
    print('empty_queue')
    raise SystemExit(0)

remaining = []
processed = 0
for line in lines:
    try:
        subprocess.check_output(['python3', str(SCRIPT_DIR / 'molt_evo_conversation_ingest.py'), line], text=True)
        processed += 1
    except Exception:
        remaining.append(line)

QUEUE.write_text('\n'.join(remaining) + ('\n' if remaining else ''), encoding='utf-8')
print(json.dumps({'processed': processed, 'remaining': len(remaining)}, ensure_ascii=False))

#!/usr/bin/env python3
import os
import re, subprocess, sys, json
from pathlib import Path

ROOT = Path(os.environ.get('MOLT_EVO_WORKSPACE', '/root/.openclaw/workspace'))
text = ' '.join(sys.argv[1:]).strip()
if not text:
    raise SystemExit('usage: molt_evo_chat_feedback.py <text>')

patterns = [
    (r'^保留旧值\s+(\d+)$', 'keep_old'),
    (r'^接受新值\s+(\d+)$', 'accept_new'),
    (r'^误报\s+(\d+)$', 'false_positive'),
    (r'^规范化\s+(\d+)\s+(.+)$', 'canonicalize_new'),
]

for pat, action in patterns:
    m = re.match(pat, text)
    if m:
        if action == 'canonicalize_new':
            conflict_id, canonical_value = m.group(1), m.group(2)
            cmd = ['python3', str(ROOT / 'molt_evo_conflict_feedback.py'), conflict_id, action, canonical_value]
        else:
            conflict_id = m.group(1)
            cmd = ['python3', str(ROOT / 'molt_evo_conflict_feedback.py'), conflict_id, action]
        out = subprocess.check_output(cmd, text=True).strip()
        print(json.dumps({'matched': True, 'action': action, 'result': out}, ensure_ascii=False))
        raise SystemExit(0)

print(json.dumps({'matched': False, 'text': text}, ensure_ascii=False))

#!/usr/bin/env python3
"""Independently check C2 row quotations against the pinned source copy."""
import re, sys
entry_path, source_path = sys.argv[1:3]
entry = open(entry_path, encoding='utf-8').read()
source = open(source_path, encoding='utf-8').read()
rows = [line for line in entry.splitlines() if re.match(r'^\| K[1-8] \|', line)]
errors=[]
for line in rows:
    m=re.match(r'^\| (K[1-8]) \| `(.+?)` \(`:(\d+)`\) \|', line)
    if not m:
        errors.append('malformed-row'); continue
    key, quote, line_no=m.groups()
    source_lines=source.splitlines()
    if int(line_no)>len(source_lines) or quote not in source_lines[int(line_no)-1]:
        errors.append(key)
ok=len(rows)==8 and not errors
print(f"C2_SOURCE_CHECK {'ok' if ok else 'unmet'} rows={len(rows)} mismatches={','.join(errors) if errors else 0}")
raise SystemExit(0 if ok else 1)

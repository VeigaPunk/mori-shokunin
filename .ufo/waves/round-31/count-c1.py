#!/usr/bin/env python3
"""Round-31 C1 counter (frozen before data; contract .ufo/waves/round-31/contract.md, C1).

usage: count-c1.py <lane-rev> [--repo <lane-repo>]

Predicate P-C1 (same sentence as the contract): C1=met iff at <lane-rev> the entry
corpus/knowledge/watchdog-identity-r31.md carries source:, verified-at: and recheck: lines and exactly one table whose
header holds the cells observation, reading, verdict and sources, with at least 8 data rows, every row naming at
least one S### that is a corpus/SOURCES.md row; at least 6 rows cite an id S161 or higher and at least 4 such ids are
cited; every such id has exactly one SOURCES.md row, exactly one admit Gate row in corpus/lessons/round-31.md with an
https URL, a 64-hex sha256 and at least one quote of at most 25 words, and a committed copy
corpus/evidence/sources-r31/S###.src whose sha256 equals the Gate sha256 and which contains every quote; the URL
fetched at measurement time hashes to the same sha256; and SKILL.md has at least 4 lines naming both Round31 and the
entry path.

Exit 0 met, 1 unmet, 2 bad revision or usage.
"""
import hashlib, os, re, subprocess, sys

ENTRY = 'corpus/knowledge/watchdog-identity-r31.md'
LESSON = 'corpus/lessons/round-31.md'
COPIES = 'corpus/evidence/sources-r31'
LANE = '/home/vgpnk/Projects/shokunin/mori-shokunin'
NEW_MIN = 161
CLEAN_ENV = {k: v for k, v in os.environ.items() if k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}


def show(repo, rev, path):
    r = subprocess.run(['git', '-C', repo, 'show', f'{rev}:{path}'], capture_output=True, env=CLEAN_ENV)
    return r.stdout if r.returncode == 0 else None


def cells(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|') and not s.endswith('\\|'):
        s = s[:-1]
    return [c.strip() for c in re.split(r'(?<!\\)\|', s)]


def norm(text):
    return ' '.join(text.split())


def unescape(q):
    return re.sub(r'\\(["|\\])', r'\1', q)


def fetch(url):
    for _ in range(3):
        r = subprocess.run(['curl', '-sSL', '--fail', '-m', '60', url], capture_output=True)
        if r.returncode == 0:
            return r.stdout
    return None


def main(argv):
    repo, rev = LANE, None
    it = iter(argv)
    for a in it:
        if a == '--repo':
            repo = next(it, None)
        elif rev is None:
            rev = a
        else:
            print('usage: count-c1.py <lane-rev> [--repo <lane-repo>]')
            return 2
    if not rev or not repo:
        print('usage: count-c1.py <lane-rev> [--repo <lane-repo>]')
        return 2
    r = subprocess.run(['git', '-C', repo, 'rev-parse', '--verify', '--quiet', '--end-of-options', rev + '^{commit}'],
                       capture_output=True, env=CLEAN_ENV)
    if r.returncode:
        print('count-c1: invalid lane revision')
        return 2
    full = r.stdout.decode().strip()
    print(f'rev={full}')
    fails = []
    entry = show(repo, full, ENTRY)
    sources = (show(repo, full, 'corpus/SOURCES.md') or b'').decode(errors='replace').splitlines()
    source_rows = {}
    for line in sources:
        m = re.match(r'\|\s*(S\d{3})\s*\|', line)
        if m:
            source_rows[m.group(1)] = source_rows.get(m.group(1), 0) + 1
    if entry is None:
        print('entry=absent')
        print('C1=unmet')
        return 1
    text = entry.decode(errors='replace').splitlines()
    heads = all(any(l.startswith(k) for l in text) for k in ('source:', 'verified-at:', 'recheck:'))
    print(f'entry=present head_lines={"yes" if heads else "no"}')
    if not heads:
        fails.append('head_lines')
    tables, i = [], 0
    while i < len(text):
        if text[i].lstrip().startswith('|') and i + 1 < len(text) and re.match(r'^\s*\|[\s:|-]+\|?\s*$', text[i + 1]) and '-' in text[i + 1]:
            hdr = [c.lower() for c in cells(text[i])]
            rows, j = [], i + 2
            while j < len(text) and text[j].lstrip().startswith('|'):
                rows.append(cells(text[j]))
                j += 1
            tables.append((hdr, rows))
            i = j
        else:
            i += 1
    want = ('observation', 'reading', 'verdict', 'sources')
    match = [t for t in tables if all(w in t[0] for w in want)]
    print(f'tables={len(tables)} decision_tables={len(match)}')
    rows_n = rows_ok = new_rows = 0
    new_ids = set()
    if len(match) != 1:
        fails.append('decision_table_count')
    else:
        hdr, rows = match[0]
        si = hdr.index('sources')
        rows_n = len(rows)
        for row in rows:
            ids = re.findall(r'\bS(\d{3})\b', row[si] if si < len(row) else '')
            ok = bool(ids) and len(row) == len(hdr) and all(source_rows.get('S' + d) for d in ids)
            rows_ok += ok
            news = {'S' + d for d in ids if int(d) >= NEW_MIN}
            if news:
                new_rows += 1
                new_ids |= news
    print(f'rows={rows_n} rows_ok={rows_ok} new_id_rows={new_rows} new_ids={len(new_ids)} ({",".join(sorted(new_ids))})')
    if rows_n < 8 or rows_ok != rows_n:
        fails.append('rows')
    if new_rows < 6 or len(new_ids) < 4:
        fails.append('new_ids')
    lesson = (show(repo, full, LESSON) or b'').decode(errors='replace').splitlines()
    gates_ok = copies_ok = fetch_ok = 0
    for sid in sorted(new_ids):
        gate = [l for l in lesson if re.match(rf'\|\s*{sid}\s*\|', l)]
        admits = [l for l in gate if cells(l) and cells(l)[-1].lower().startswith('admit')]
        detail = []
        if source_rows.get(sid) != 1:
            detail.append(f'source_rows={source_rows.get(sid, 0)}')
        if len(admits) != 1:
            detail.append(f'admit_rows={len(admits)}')
            print(f'{sid} gate=bad {" ".join(detail)}')
            continue
        c = cells(admits[0])
        url = next((x for x in c if x.startswith('https://')), None)
        sha = re.search(r'`([0-9a-f]{64})`', admits[0])
        quotes = [unescape(q) for q in re.findall(r'\(\s*\d+\s+words?\s*\):\s*"((?:[^"\\]|\\.)*)"', admits[0])]
        if not url or not sha or not quotes or any(len(q.split()) > 25 for q in quotes):
            detail.append('gate_fields')
        if detail:
            print(f'{sid} gate=bad {" ".join(detail)}')
            continue
        gates_ok += 1
        copy = show(repo, full, f'{COPIES}/{sid}.src')
        cok = copy is not None and hashlib.sha256(copy).hexdigest() == sha.group(1) and \
            all(norm(q) in norm(copy.decode(errors='replace')) for q in quotes)
        copies_ok += cok
        body = fetch(url)
        fok = body is not None and hashlib.sha256(body).hexdigest() == sha.group(1)
        fetch_ok += fok
        print(f'{sid} gate=ok quotes={len(quotes)} copy={"ok" if cok else "bad"} fetch={"ok" if fok else "bad"} url={url}')
    n = len(new_ids)
    print(f'gates_ok={gates_ok}/{n} copies_ok={copies_ok}/{n} fetch_ok={fetch_ok}/{n}')
    if n == 0 or gates_ok != n or copies_ok != n or fetch_ok != n:
        fails.append('sources')
    skill = (show(repo, full, 'SKILL.md') or b'').decode(errors='replace').splitlines()
    skill_rows = sum(1 for l in skill if 'Round31' in l and ENTRY.split('corpus/', 1)[1] in l)
    print(f'skill_rows={skill_rows}')
    if skill_rows < 4:
        fails.append('skill_rows')
    if fails:
        print('unmet_conditions=' + ','.join(fails))
        print('C1=unmet')
        return 1
    print('C1=met')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

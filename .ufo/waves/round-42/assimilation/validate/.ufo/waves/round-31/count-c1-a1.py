#!/usr/bin/env python3
"""Round-31 C1 counter, amendment A1 (tightened before any round-31 entry was scored; contract "Amendment A1").

usage: count-c1-a1.py <lane-rev> [--repo <lane-repo>]

Predicate P-C1-A1 (same sentence as the contract): C1=met iff P-C1 holds at <lane-rev> (count-c1.py's conditions,
re-implemented here) and also: the entry holds no HTML comment and its decision table is outside any code fence; the
data rows are pairwise distinct and each reading cell has at least 8 words; every cited id S161 or higher has SOURCES
status mined, a URL that no corpus/SOURCES.md line at the entering tip a12c68ae carries, a URL and copy sha256 distinct
from every other new id's, and Gate quotes that each have at least 3 words behind a `file:L` or `file:L-M` locator;
every row citing such an id shares at least 2 distinct words of 4 or more letters with the Gate quotes of the new ids
it cites; the committed non-author judge receipt .ufo/waves/round-31/r1/JudgeC1Rows.md names every data row once as
`row N: supported` or `row N: unsupported`, with at least 8 rows supported of which at least 6 cite a new id; and
SKILL.md has at least 4 distinct lines of at least 12 words naming the word Round31 and
corpus/knowledge/watchdog-identity-r31.md.

The original P-C1 (count-c1.py) is kept and reported beside this one. Exit 0 met, 1 unmet, 2 bad revision or usage.
"""
import hashlib, os, re, subprocess, sys

ENTRY = 'corpus/knowledge/watchdog-identity-r31.md'
LESSON = 'corpus/lessons/round-31.md'
COPIES = 'corpus/evidence/sources-r31'
JUDGE = '.ufo/waves/round-31/r1/JudgeC1Rows.md'
ENTERING = 'a12c68ae81257fb6f918bb165bcb39c73f82d212'
LANE = '/home/vgpnk/Projects/shokunin/mori-shokunin'
NEW_MIN = 161
CLEAN_ENV = {k: v for k, v in os.environ.items() if k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}
QUOTE_RE = re.compile(r'`[^`\s]+:\d+(?:-\d+)?`\s*\(\s*\d+\s+words?\s*\):\s*"((?:[^"\\]|\\.)*)"')
ANY_QUOTE_RE = re.compile(r'\(\s*\d+\s+words?\s*\):\s*"((?:[^"\\]|\\.)*)"')


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


def words4(text):
    return {w for w in re.findall(r'[a-z0-9_]+', text.lower()) if len(w) >= 4}


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
            print('usage: count-c1-a1.py <lane-rev> [--repo <lane-repo>]')
            return 2
    if not rev or not repo:
        print('usage: count-c1-a1.py <lane-rev> [--repo <lane-repo>]')
        return 2
    r = subprocess.run(['git', '-C', repo, 'rev-parse', '--verify', '--quiet', '--end-of-options', rev + '^{commit}'],
                       capture_output=True, env=CLEAN_ENV)
    if r.returncode:
        print('count-c1-a1: invalid lane revision')
        return 2
    full = r.stdout.decode().strip()
    print(f'rev={full} repo={repo}')
    fails = []
    entry = show(repo, full, ENTRY)
    sources_text = (show(repo, full, 'corpus/SOURCES.md') or b'').decode(errors='replace')
    entering_sources = (show(LANE, ENTERING, 'corpus/SOURCES.md') or b'').decode(errors='replace')
    source_rows = {}
    for line in sources_text.splitlines():
        m = re.match(r'\|\s*(S\d{3})\s*\|', line)
        if m:
            source_rows.setdefault(m.group(1), []).append(cells(line))
    if entry is None:
        print('entry=absent')
        print('C1=unmet')
        return 1
    text = entry.decode(errors='replace').splitlines()
    heads = all(any(l.startswith(k) for l in text) for k in ('source:', 'verified-at:', 'recheck:'))
    comments = sum(1 for l in text if '<!--' in l)
    print(f'entry=present head_lines={"yes" if heads else "no"} html_comments={comments}')
    if not heads:
        fails.append('head_lines')
    if comments:
        fails.append('html_comment')
    tables, i, fence = [], 0, False
    while i < len(text):
        if re.match(r'^\s*(```|~~~)', text[i]):
            fence = not fence
            i += 1
            continue
        if text[i].lstrip().startswith('|') and i + 1 < len(text) and re.match(r'^\s*\|[\s:|-]+\|?\s*$', text[i + 1]) and '-' in text[i + 1]:
            hdr = [c.lower() for c in cells(text[i])]
            rows, j = [], i + 2
            while j < len(text) and text[j].lstrip().startswith('|'):
                rows.append(cells(text[j]))
                j += 1
            tables.append((hdr, rows, fence))
            i = j
        else:
            i += 1
    want = ('observation', 'reading', 'verdict', 'sources')
    match = [t for t in tables if all(w in t[0] for w in want)]
    print(f'tables={len(tables)} decision_tables={len(match)}')
    rows_n = rows_ok = new_rows = 0
    new_ids, row_info = set(), []
    if len(match) != 1:
        fails.append('decision_table_count')
    else:
        hdr, rows, fenced = match[0]
        if fenced:
            fails.append('table_in_fence')
        si, ri, oi = hdr.index('sources'), hdr.index('reading'), hdr.index('observation')
        rows_n = len(rows)
        distinct = len({norm('|'.join(r)) for r in rows})
        short = 0
        for row in rows:
            ids = re.findall(r'\bS(\d{3})\b', row[si] if si < len(row) else '')
            ok = bool(ids) and len(row) == len(hdr) and all(source_rows.get('S' + d) for d in ids)
            rows_ok += ok
            if len(row) == len(hdr) and len(row[ri].split()) < 8:
                short += 1
            news = {'S' + d for d in ids if int(d) >= NEW_MIN}
            if news:
                new_rows += 1
                new_ids |= news
            row_info.append((news, (row[oi] + ' ' + row[ri]) if len(row) == len(hdr) else ''))
        print(f'rows={rows_n} rows_ok={rows_ok} distinct_rows={distinct} short_readings={short}')
        if distinct != rows_n:
            fails.append('duplicate_rows')
        if short:
            fails.append('short_readings')
    print(f'new_id_rows={new_rows} new_ids={len(new_ids)} ({",".join(sorted(new_ids))})')
    if rows_n < 8 or rows_ok != rows_n:
        fails.append('rows')
    if new_rows < 6 or len(new_ids) < 4:
        fails.append('new_ids')
    lesson = (show(repo, full, LESSON) or b'').decode(errors='replace').splitlines()
    gates_ok = copies_ok = fetch_ok = 0
    urls, shas, quote_words = {}, {}, {}
    for sid in sorted(new_ids):
        gate = [l for l in lesson if re.match(rf'\|\s*{sid}\s*\|', l)]
        admits = [l for l in gate if cells(l) and cells(l)[-1].lower().startswith('admit')]
        detail = []
        srows = source_rows.get(sid, [])
        if len(srows) != 1:
            detail.append(f'source_rows={len(srows)}')
        elif len(srows[0]) < 8 or srows[0][7].strip().lower() != 'mined':
            detail.append('source_status_not_mined')
        if len(admits) != 1:
            detail.append(f'admit_rows={len(admits)}')
            print(f'{sid} gate=bad {" ".join(detail)}')
            continue
        c = cells(admits[0])
        url = next((x for x in c if x.startswith('https://')), None)
        sha = re.search(r'`([0-9a-f]{64})`', admits[0])
        located = [unescape(q) for q in QUOTE_RE.findall(admits[0])]
        anyq = ANY_QUOTE_RE.findall(admits[0])
        if not url or not sha or not located or len(located) != len(anyq) or \
                any(len(q.split()) > 25 or len(q.split()) < 3 for q in located):
            detail.append('gate_fields')
        if url and url in entering_sources:
            detail.append('url_registered_at_entering_tip')
        if detail:
            print(f'{sid} gate=bad {" ".join(detail)}')
            continue
        gates_ok += 1
        urls[sid], shas[sid] = url, sha.group(1)
        quote_words[sid] = set().union(*(words4(q) for q in located))
        copy = show(repo, full, f'{COPIES}/{sid}.src')
        cok = copy is not None and hashlib.sha256(copy).hexdigest() == sha.group(1) and \
            all(norm(q) in norm(copy.decode(errors='replace')) for q in located)
        copies_ok += cok
        body = fetch(url)
        fok = body is not None and hashlib.sha256(body).hexdigest() == sha.group(1)
        fetch_ok += fok
        print(f'{sid} gate=ok quotes={len(located)} copy={"ok" if cok else "bad"} fetch={"ok" if fok else "bad"} url={url}')
    n = len(new_ids)
    distinct_src = len(set(urls.values())) == len(urls) and len(set(shas.values())) == len(shas)
    print(f'gates_ok={gates_ok}/{n} copies_ok={copies_ok}/{n} fetch_ok={fetch_ok}/{n} distinct_sources={"yes" if distinct_src else "no"}')
    if n == 0 or gates_ok != n or copies_ok != n or fetch_ok != n or not distinct_src:
        fails.append('sources')
    unsupported_overlap = []
    for k, (news, rowtext) in enumerate(row_info, 1):
        if news:
            qw = set().union(*(quote_words.get(s, set()) for s in news))
            if len(words4(rowtext) & qw) < 2:
                unsupported_overlap.append(k)
    print(f'rows_without_quote_overlap={len(unsupported_overlap)} {unsupported_overlap if unsupported_overlap else ""}'.rstrip())
    if unsupported_overlap:
        fails.append('quote_overlap')
    judge = show(repo, full, JUDGE)
    if judge is None:
        print('judge=absent')
        fails.append('judge')
    else:
        verdicts = {}
        dupl = 0
        for l in judge.decode(errors='replace').splitlines():
            m = re.match(r'^\s*row (\d+): (supported|unsupported)\b', l)
            if m:
                k = int(m.group(1))
                dupl += k in verdicts
                verdicts[k] = m.group(2)
        covered = set(verdicts) == set(range(1, rows_n + 1)) and dupl == 0
        sup = [k for k, v in verdicts.items() if v == 'supported' and 1 <= k <= rows_n]
        sup_new = [k for k in sup if row_info[k - 1][0]]
        print(f'judge=present covered={"yes" if covered else "no"} supported={len(sup)} supported_new={len(sup_new)} '
              f'unsupported={sorted(k for k, v in verdicts.items() if v == "unsupported")}')
        if not covered or len(sup) < 8 or len(sup_new) < 6:
            fails.append('judge')
    skill = (show(repo, full, 'SKILL.md') or b'').decode(errors='replace').splitlines()
    sl = {norm(l) for l in skill if re.search(r'\bRound31\b', l) and ENTRY in l and len(l.split()) >= 12}
    print(f'skill_rows={len(sl)}')
    if len(sl) < 4:
        fails.append('skill_rows')
    if fails:
        print('unmet_conditions=' + ','.join(fails))
        print('C1=unmet')
        return 1
    print('C1=met')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

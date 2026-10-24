#!/usr/bin/env python3
"""Round-33 C1 counter, amendment A1 (code made to match the frozen P-C1 sentence and tightened after the C0 control
wave, before any data seat; contract "Amendment A1"). The frozen count-c1.py stays byte-identical and is reported
beside this one.

usage: count-c1-a1.py <lane-rev> [--repo <lane-repo>]

Predicate P-C1-A1 (the same sentence as the contract's Amendment A1; parity level: whitespace runs collapsed):
C1=met iff P-C1 holds at <lane-rev> and also: no two data rows are equal and no two observation cells are equal once
lowercased and reduced to their runs of letters, digits and underscores; no reading cell of a row citing a new id
contains a run of 6 consecutive such words that also occurs in a Gate quote of a new id that row cites; and every row
the judge receipt names supported carries a valid span, so a supported row with a missing, short or misplaced span
fails the predicate instead of being left out of the count.

Predicate P-C1 (the same sentence as .ufo/waves/round-33/contract.md; parity level: whitespace runs collapsed):
C1=met iff at <lane-rev> the entry corpus/knowledge/disk-write-rate-r33.md carries source:, verified-at: and recheck:
lines, holds no HTML comment, and has exactly one table outside any code fence whose header holds the cells
observation, reading, verdict and sources, with at least 10 pairwise-distinct data rows, each with a reading cell of
at least 8 words and naming at least one S### that is a corpus/SOURCES.md row; at least 8 rows cite an id S180 or
higher and at least 5 such ids are cited; every such id has exactly one corpus/SOURCES.md row with status mined, a URL
that no corpus/SOURCES.md line at the entering tip 7d382043 carries and that no other new id carries, exactly one
admit Gate row in corpus/lessons/round-33.md with that https URL, a 64-hex sha256 distinct from every other new id's
and 1-4 quotes of 3-25 words each behind a `file:L` or `file:L-M` locator, and a committed copy
corpus/evidence/sources-r33/S###.src whose sha256 equals the Gate sha256 and which contains every quote; the URL
fetched at measurement time hashes to the same sha256; every row citing a new id shares at least 2 distinct words of 4
or more letters with the Gate quotes of the new ids it cites; the committed judge dispatch
.ufo/waves/round-33/judge/dispatch.json and the committed judge receipt .ufo/waves/round-33/judge/JudgeC1Rows.md each
contain the judge rule R-J, the receipt carries a `judged-sha256:` line equal to the sha256 of the entry at
<lane-rev>, and it names every data row once as `row N: supported` or `row N: unsupported`, each supported row
followed on the same line by `span: "<text>"` of at least 6 words that is located in the committed copy of a new id
that row cites; at least 10 rows are supported, of which at least 8 cite a new id; and SKILL.md has at least 4
distinct lines of at least 12 words naming the word Round33 and corpus/knowledge/disk-write-rate-r33.md.

Judge rule R-J (the same sentence in the contract, here, the judge dispatch and the judge receipt):
A row is supported only when the quotes located in the committed copies of the sources it cites state every fact its
observation and reading cells assert, and its verdict cell follows from that reading without any further fact; a row
any part of which is not so stated is unsupported, including a row the judge would accept only with a caveat or
through a source the row does not cite.

Text matching (quotes in copies, spans in copies, R-J in dispatch and receipt) collapses whitespace runs to one space
and nothing else. Gate quote syntax: `` `file:L-M` (N words): "quote" `` with `\\"`, `\\|`, `\\\\` escapes.
Exit 0 met, 1 unmet, 2 bad revision or usage. The receipt label is `C1=met` / `C1=unmet`.
"""
import hashlib, os, re, subprocess, sys

ENTRY = 'corpus/knowledge/disk-write-rate-r33.md'
LESSON = 'corpus/lessons/round-33.md'
COPIES = 'corpus/evidence/sources-r33'
JUDGE = '.ufo/waves/round-33/judge/JudgeC1Rows.md'
DISPATCH = '.ufo/waves/round-33/judge/dispatch.json'
ENTERING = '7d382043016e8854e3be2ee523a095b409c3d8a1'
LANE = '/home/vgpnk/Projects/shokunin/mori-shokunin'
NEW_MIN = 180
RULE = ('A row is supported only when the quotes located in the committed copies of the sources it cites state every '
        'fact its observation and reading cells assert, and its verdict cell follows from that reading without any '
        'further fact; a row any part of which is not so stated is unsupported, including a row the judge would '
        'accept only with a caveat or through a source the row does not cite.')
CLEAN_ENV = {k: v for k, v in os.environ.items() if k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}
QUOTE_RE = re.compile(r'`[^`\s]+:\d+(?:-\d+)?`\s*\(\s*\d+\s+words?\s*\):\s*"((?:[^"\\]|\\.)*)"')
ANY_QUOTE_RE = re.compile(r'\(\s*\d+\s+words?\s*\):\s*"((?:[^"\\]|\\.)*)"')
SPAN_RE = re.compile(r'span:\s*"((?:[^"\\]|\\.)*)"')


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


def canon(text):
    return ' '.join(re.findall(r'[a-z0-9_]+', text.lower()))


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
        print('count-c1: invalid lane revision')
        return 2
    full = r.stdout.decode().strip()
    print(f'rev={full} repo={repo}')
    fails = []
    entry = show(repo, full, ENTRY)
    sources_text = (show(repo, full, 'corpus/SOURCES.md') or b'').decode(errors='replace')
    entering_sources = (show(LANE, ENTERING, 'corpus/SOURCES.md') or b'').decode(errors='replace')
    if not entering_sources:
        print('count-c1: entering tip SOURCES.md unreadable')
        return 2
    source_rows = {}
    for line in sources_text.splitlines():
        m = re.match(r'\|\s*(S\d{3})\s*\|', line)
        if m:
            source_rows.setdefault(m.group(1), []).append(cells(line))
    if entry is None:
        print('entry=absent')
        print('C1=unmet')
        return 1
    entry_sha = hashlib.sha256(entry).hexdigest()
    text = entry.decode(errors='replace').splitlines()
    heads = all(any(l.startswith(k) for l in text) for k in ('source:', 'verified-at:', 'recheck:'))
    comments = sum(1 for l in text if '<!--' in l)
    print(f'entry=present entry_sha256={entry_sha} head_lines={"yes" if heads else "no"} html_comments={comments}')
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
        if text[i].lstrip().startswith('|') and i + 1 < len(text) and \
                re.match(r'^\s*\|[\s:|-]+\|?\s*$', text[i + 1]) and '-' in text[i + 1]:
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
    unfenced = [t for t in match if not t[2]]
    print(f'tables={len(tables)} decision_tables={len(match)} unfenced_decision_tables={len(unfenced)}')
    rows_n = rows_ok = new_rows = 0
    new_ids, row_info, readings = set(), [], []
    if len(match) != 1 or len(unfenced) != 1:
        fails.append('decision_table_count')
    else:
        hdr, rows, _ = unfenced[0]
        si, ri, oi = hdr.index('sources'), hdr.index('reading'), hdr.index('observation')
        rows_n = len(rows)
        distinct = len({canon('|'.join(r)) for r in rows})
        distinct_obs = len({canon(r[oi]) for r in rows if len(r) == len(hdr)})
        short = 0
        for row in rows:
            shaped = len(row) == len(hdr)
            ids = re.findall(r'\bS(\d{3})\b', row[si]) if shaped else []
            ok = bool(ids) and shaped and all(source_rows.get('S' + d) for d in ids)
            rows_ok += ok
            if not shaped or len(row[ri].split()) < 8:
                short += 1
            news = {'S' + d for d in ids if int(d) >= NEW_MIN}
            if news:
                new_rows += 1
                new_ids |= news
            row_info.append((news, (row[oi] + ' ' + row[ri]) if shaped else ''))
            readings.append(row[ri] if shaped else '')
        print(f'rows={rows_n} rows_ok={rows_ok} distinct_rows={distinct} distinct_observations={distinct_obs} '
              f'short_readings={short}')
        if distinct != rows_n or distinct_obs != rows_n:
            fails.append('duplicate_rows')
        if short:
            fails.append('short_readings')
    print(f'new_id_rows={new_rows} new_ids={len(new_ids)} ({",".join(sorted(new_ids))})')
    if rows_n < 10 or rows_ok != rows_n:
        fails.append('rows')
    if new_rows < 8 or len(new_ids) < 5:
        fails.append('new_ids')
    lesson = (show(repo, full, LESSON) or b'').decode(errors='replace').splitlines()
    gates_ok = copies_ok = fetch_ok = 0
    urls, shas, quote_words, copies, quote_seqs = {}, {}, {}, {}, {}
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
        sha = re.search(r'`?([0-9a-f]{64})`?', admits[0])
        located = [unescape(q) for q in QUOTE_RE.findall(admits[0])]
        anyq = ANY_QUOTE_RE.findall(admits[0])
        if not url or not sha or not located or len(located) != len(anyq) or len(located) > 4 or \
                any(len(q.split()) > 25 or len(q.split()) < 3 for q in located):
            detail.append('gate_fields')
        if url and srows and len(srows) == 1 and url not in srows[0][1]:
            detail.append('url_not_in_source_row')
        if url and url in entering_sources:
            detail.append('url_registered_at_entering_tip')
        if detail:
            print(f'{sid} gate=bad {" ".join(detail)}')
            continue
        gates_ok += 1
        urls[sid], shas[sid] = url, sha.group(1)
        quote_words[sid] = set().union(*(words4(q) for q in located))
        quote_seqs[sid] = [canon(q).split() for q in located]
        copy = show(repo, full, f'{COPIES}/{sid}.src')
        copies[sid] = norm(copy.decode(errors='replace')) if copy is not None else None
        cok = copy is not None and hashlib.sha256(copy).hexdigest() == sha.group(1) and \
            all(norm(q) in copies[sid] for q in located)
        copies_ok += cok
        body = fetch(url)
        fok = body is not None and hashlib.sha256(body).hexdigest() == sha.group(1)
        fetch_ok += fok
        print(f'{sid} gate=ok quotes={len(located)} copy={"ok" if cok else "bad"} fetch={"ok" if fok else "bad"} url={url}')
    n = len(new_ids)
    distinct_src = len(set(urls.values())) == len(urls) and len(set(shas.values())) == len(shas)
    other_urls = {}
    for sid in new_ids:
        for row in source_rows.get(sid, []):
            other_urls[sid] = row[1] if len(row) > 1 else ''
    shared = [s for s in urls if any(urls[s] in other_urls.get(t, '') for t in new_ids if t != s)]
    print(f'gates_ok={gates_ok}/{n} copies_ok={copies_ok}/{n} fetch_ok={fetch_ok}/{n} '
          f'distinct_sources={"yes" if distinct_src and not shared else "no"}')
    if n == 0 or gates_ok != n or copies_ok != n or fetch_ok != n or not distinct_src or shared:
        fails.append('sources')
    no_overlap = []
    for k, (news, rowtext) in enumerate(row_info, 1):
        if news:
            qw = set().union(*(quote_words.get(s, set()) for s in news))
            if len(words4(rowtext) & qw) < 2:
                no_overlap.append(k)
    print(f'rows_without_quote_overlap={len(no_overlap)} {no_overlap if no_overlap else ""}'.rstrip())
    if no_overlap:
        fails.append('quote_overlap')
    copied = []
    for k, (news, _) in enumerate(row_info, 1):
        rw = canon(readings[k - 1]).split()
        grams = {tuple(rw[i:i + 6]) for i in range(len(rw) - 5)}
        for s in news:
            if any(tuple(q[i:i + 6]) in grams for q in quote_seqs.get(s, []) for i in range(len(q) - 5)):
                copied.append(k)
                break
    print(f'readings_copying_quotes={len(copied)} {copied if copied else ""}'.rstrip())
    if copied:
        fails.append('reading_copies_quote')
    rule = norm(RULE)
    dispatch = show(repo, full, DISPATCH)
    disp_rule = dispatch is not None and rule in norm(dispatch.decode(errors='replace'))
    judge = show(repo, full, JUDGE)
    if judge is None:
        print(f'dispatch_rule={"yes" if disp_rule else "no"} judge=absent')
        fails.append('judge')
    else:
        jt = judge.decode(errors='replace')
        rec_rule = rule in norm(jt)
        m = re.search(r'^judged-sha256:\s*`?([0-9a-f]{64})`?\s*$', jt, re.M)
        sha_ok = bool(m) and m.group(1) == entry_sha
        verdicts, spans_bad, dupl = {}, [], 0
        for l in jt.splitlines():
            mm = re.match(r'^\s*row (\d+): (supported|unsupported)\b(.*)$', l)
            if not mm:
                continue
            k = int(mm.group(1))
            dupl += k in verdicts
            verdicts[k] = mm.group(2)
            if mm.group(2) == 'supported':
                sp = SPAN_RE.search(mm.group(3))
                news = row_info[k - 1][0] if 1 <= k <= rows_n else set()
                span = norm(unescape(sp.group(1))) if sp else ''
                if len(span.split()) < 6 or not any(copies.get(s) and span in copies[s] for s in news):
                    spans_bad.append(k)
        covered = set(verdicts) == set(range(1, rows_n + 1)) and dupl == 0 and rows_n > 0
        sup = [k for k, v in verdicts.items() if v == 'supported' and 1 <= k <= rows_n and k not in spans_bad]
        sup_new = [k for k in sup if row_info[k - 1][0]]
        print(f'dispatch_rule={"yes" if disp_rule else "no"} receipt_rule={"yes" if rec_rule else "no"} '
              f'judged_sha={"ok" if sha_ok else "bad"} covered={"yes" if covered else "no"} '
              f'supported={len(sup)} supported_new={len(sup_new)} spans_bad={spans_bad} '
              f'unsupported={sorted(k for k, v in verdicts.items() if v == "unsupported")}')
        if not (disp_rule and rec_rule and sha_ok and covered) or spans_bad or len(sup) < 10 or len(sup_new) < 8:
            fails.append('judge')
    skill = (show(repo, full, 'SKILL.md') or b'').decode(errors='replace').splitlines()
    sl = {norm(l) for l in skill if re.search(r'\bRound33\b', l) and ENTRY in l and len(l.split()) >= 12}
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

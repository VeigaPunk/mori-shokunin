#!/usr/bin/env python3
"""Round-32 C1 counter (frozen before data; contract .ufo/waves/round-32/contract.md, C1).

usage: count-c1.py <lane-rev> [--repo <lane-repo>] [--no-live]

Predicate P-C1 (the same sentence as the contract and the receipt label):
C1=met iff at <lane-rev> every one of the 34 frozen population ids has exactly one row in the `## Recheck` table of
corpus/lessons/round-32.md that passes every row check (rows_ok=34/34), and at least one new source row S175 or
higher passes the new-source check (new_ok>=1).

Row checks (id r, frozen row p from c1-population.json beside this script, its sha256 pinned below):
 R1 the table header is exactly `id | url | accessed | sha256 | quotes | verdict`; the row's url equals p.url;
    accessed is an ISO-8601 UTC time at or after 2026-10-23T01:00:00Z; verdict is current, drifted or unreachable.
 R2 current/drifted: sha256 is 64 hex and equals the sha256 of the committed copy corpus/evidence/recheck-r32/<r>.src;
    the quotes cell holds 1-3 double-quoted quotes, each 3-25 words after normalisation; every quote occurs in the
    normalised copy; and the quotes together share at least 2 distinct content tokens (alphabetic, length >= 4,
    not a stop word) with p.teaches + p.anchor + p.scope.
 R3 current/drifted: the URL fetched now (curl -sSL --fail -m 60, up to 3 tries) yields bytes whose normalised text
    contains every quote. unreachable: the committed corpus/evidence/recheck-r32/<r>.fetch.txt exists and all 3
    counter fetches fail.
 R4 the judge receipt .ufo/waves/round-32/judge/JudgeRecheck.md carries `judge-role: reviewer`, a `judge-seat: <Name>`
    whose Name appears as a task name with agent reviewer in a committed .ufo/waves/round-32/*dispatch*.json, and
    `judged-sha256: <hex>` equal to the sha256 of the tip `## Recheck` section bytes; it has the line `- <r>: agree`.
 R5 drifted: every corpus/knowledge/ path in p.used_by gains, between the base and <lane-rev>, an added line that
    names <r> and `Round32`.
New-source check (row s with id number >= 175 in corpus/SOURCES.md at <lane-rev>): status mined; its URL is absent
from corpus/SOURCES.md at the base; corpus/lessons/round-32.md `## Gate` holds one row for s with an https URL equal
to it, a 64-hex sha256 equal to the committed copy corpus/evidence/sources-r32/<s>.src, at least one double-quoted
quote of 3-25 words found in the normalised copy, and a decision starting `admit`; and the id is cited in
corpus/evidence/recheck-r32/README.md.

Normalisation: PDF (bytes start %PDF) -> `pdftotext -layout`; HTML (contains `<html` or `<!doctype` in the first
4 KiB, case-insensitive) -> drop script/style/noscript blocks, drop tags, unescape entities; then for every text and
every quote: NFKC, typographic quotes/dashes folded to ASCII, whitespace runs collapsed to one space.

Exit 0 met, 1 unmet, 2 bad revision, population digest mismatch or usage. `--no-live` skips R3 (diagnostic only; it
prints C1=diagnostic and never met).
"""
import hashlib, html, os, re, subprocess, sys, tempfile, unicodedata

BASE = '641a6e86ecc60634d215c0a47ab86c47661abf86'
POP = '.ufo/waves/round-32/c1-population.json'
POP_SHA = '4426b6501a01c07bdb3347c712c5e858447be47204fa9017c02ab6113e83e178'
LESSON = 'corpus/lessons/round-32.md'
COPIES = 'corpus/evidence/recheck-r32'
NEWCOPIES = 'corpus/evidence/sources-r32'
README = 'corpus/evidence/recheck-r32/README.md'
JUDGE = '.ufo/waves/round-32/judge/JudgeRecheck.md'
LANE = '/home/vgpnk/Projects/shokunin/mori-shokunin'
HEADER = ['id', 'url', 'accessed', 'sha256', 'quotes', 'verdict']
MIN_ACCESS = '2026-10-23T01:00:00Z'
N_EXPECTED = 34
CLEAN_ENV = {k: v for k, v in os.environ.items() if k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}
STOP = set('that this with from have been were will when what which their there they them then than into onto '
           'only also such each every other more most some same over under about after before between does done '
           'used uses using must never always while where your yours file files page read reads value values'.split())


def git(repo, *args):
    return subprocess.run(['git', '-C', repo, *args], capture_output=True, env=CLEAN_ENV)


def show(repo, rev, path):
    r = git(repo, 'show', f'{rev}:{path}')
    return r.stdout if r.returncode == 0 else None


def cells(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|') and not s.endswith('\\|'):
        s = s[:-1]
    return [c.strip() for c in re.split(r'(?<!\\)\|', s)]


FOLD = {'\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"', '\u2013': '-', '\u2014': '-', '\u00a0': ' '}


def fold(s):
    s = unicodedata.normalize('NFKC', s)
    for a, b in FOLD.items():
        s = s.replace(a, b)
    return re.sub(r'\s+', ' ', s).strip()


def normalise(data):
    if data is None:
        return None
    if data[:4] == b'%PDF':
        with tempfile.NamedTemporaryFile(suffix='.pdf') as f:
            f.write(data)
            f.flush()
            r = subprocess.run(['pdftotext', '-layout', f.name, '-'], capture_output=True, timeout=120)
        text = r.stdout.decode('utf-8', 'replace') if r.returncode == 0 else ''
        return fold(text)
    text = data.decode('utf-8', 'replace')
    head = text[:4096].lower()
    if '<html' in head or '<!doctype' in head:
        text = re.sub(r'(?is)<(script|style|noscript)\b.*?</\1\s*>', ' ', text)
        text = re.sub(r'(?s)<!--.*?-->', ' ', text)
        text = re.sub(r'(?s)<[^>]*>', ' ', text)
        text = html.unescape(text)
    return fold(text)


def quotes_of(cell):
    qs = re.findall(r'"((?:[^"\\]|\\.)*)"', cell)
    return [fold(html.unescape(q.replace('\\"', '"').replace('\\|', '|'))) for q in qs]


def tokens(s):
    return {t for t in re.findall(r'[a-z]+', s.lower()) if len(t) >= 4 and t not in STOP}


def fetch(url, tries=3):
    for _ in range(tries):
        r = subprocess.run(['curl', '-sSL', '--fail', '-m', '60', url], capture_output=True)
        if r.returncode == 0 and r.stdout:
            yield r.stdout


def section(text, title):
    lines = text.splitlines(keepends=True)
    out, inside = [], False
    for ln in lines:
        if ln.startswith('## '):
            if inside:
                break
            inside = ln.strip() == f'## {title}' or ln.startswith(f'## {title} ')
        if inside:
            out.append(ln)
    return ''.join(out)


def table(sec):
    hdr, body = None, []
    for ln in sec.splitlines():
        if not ln.startswith('|'):
            if hdr is not None and body:
                break
            continue
        c = cells(ln)
        if hdr is None:
            hdr = [x.lower() for x in c]
            continue
        if all(re.fullmatch(r':?-{3,}:?', x) for x in c):
            continue
        body.append(c)
    return hdr, body


def added_lines(repo, rev, path):
    r = git(repo, 'diff', '--no-renames', '-U0', BASE, rev, '--', path)
    if r.returncode != 0:
        return []
    return [ln[1:] for ln in r.stdout.decode('utf-8', 'replace').splitlines()
            if ln.startswith('+') and not ln.startswith('+++')]


def main(argv):
    if len(argv) == 2 and argv[0] == '--section-sha':
        with open(argv[1], 'rb') as f:
            sec = section(f.read().decode('utf-8', 'replace'), 'Recheck')
        print(hashlib.sha256(sec.encode('utf-8')).hexdigest()); return 0
    repo, live, args = LANE, True, []
    i = 0
    while i < len(argv):
        if argv[i] == '--repo' and i + 1 < len(argv):
            repo = argv[i + 1]; i += 2; continue
        if argv[i] == '--no-live':
            live = False; i += 1; continue
        args.append(argv[i]); i += 1
    if len(args) != 1:
        print('usage: count-c1.py <lane-rev> [--repo <lane-repo>] [--no-live]'); return 2
    rev = args[0]
    r = git(repo, 'rev-parse', '--verify', f'{rev}^{{commit}}')
    if r.returncode != 0:
        print(f'revision={rev} unresolved C1=error exit=2'); return 2
    full = r.stdout.decode().strip()
    import json
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'c1-population.json'), 'rb') as f:
        popb = f.read()
    if hashlib.sha256(popb).hexdigest() != POP_SHA:
        print(f'revision={full} population digest mismatch C1=error exit=2'); return 2
    pop = {p['id']: p for p in json.loads(popb)['population']}
    if len(pop) != N_EXPECTED:
        print(f'revision={full} population size {len(pop)} C1=error exit=2'); return 2
    print(f'revision={full} base={BASE} population={len(pop)} pop_sha256={POP_SHA[:16]}')
    lesson_b = show(repo, rev, LESSON)
    lesson = lesson_b.decode('utf-8', 'replace') if lesson_b else ''
    rsec = section(lesson, 'Recheck')
    hdr, body = table(rsec)
    hdr_ok = hdr == HEADER
    sec_sha = hashlib.sha256(rsec.encode('utf-8')).hexdigest()
    by_id = {}
    for c in body:
        by_id.setdefault(c[0], []).append(c)
    judge_b = show(repo, rev, JUDGE)
    judge = judge_b.decode('utf-8', 'replace') if judge_b else ''
    jm = re.search(r'^judged-sha256:\s*([0-9a-f]{64})\s*$', judge, re.M)
    jseat = re.search(r'^judge-seat:\s*(\S+)\s*$', judge, re.M)
    jrole = re.search(r'^judge-role:\s*reviewer\s*$', judge, re.M)
    seat_ok = False
    if jseat:
        ls = git(repo, 'ls-tree', '-r', '--name-only', full, '.ufo/waves/round-32/')
        for path in ls.stdout.decode().splitlines():
            if 'dispatch' in path.rsplit('/', 1)[-1] and path.endswith('.json'):
                try:
                    d = json.loads(show(repo, full, path) or b'{}')
                except ValueError:
                    continue
                for t in (d.get('tasks') or d.get('taskCall', {}).get('tasks') or []):
                    if t.get('name') == jseat.group(1) and t.get('agent') == 'reviewer':
                        seat_ok = True
    judge_ok = bool(jm and jrole and seat_ok and jm.group(1) == sec_sha)
    agrees = set(re.findall(r'^- (S\d{3}): agree\s*$', judge, re.M))
    print(f'recheck_rows={len(body)} header_ok={hdr_ok} section_sha256={sec_sha[:16]} '
          f'judge_ok={judge_ok} judge_seat_ok={seat_ok} judge_agree={len(agrees)}')
    rows_ok, fails, verdicts = 0, [], {}
    for rid in sorted(pop):
        p = pop[rid]
        why = []
        rs = by_id.get(rid, [])
        if len(rs) != 1:
            fails.append(f'{rid}:rows={len(rs)}'); continue
        c = rs[0]
        if not hdr_ok or len(c) != 6:
            fails.append(f'{rid}:shape'); continue
        _, url, acc, sha, qcell, verdict = c
        url = url.strip('`<>')
        verdicts[verdict] = verdicts.get(verdict, 0) + 1
        if url != p['url']:
            why.append('url')
        if not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', acc) or acc < MIN_ACCESS:
            why.append('accessed')
        if verdict not in ('current', 'drifted', 'unreachable'):
            why.append('verdict')
        if verdict in ('current', 'drifted'):
            copy = show(repo, full, f'{COPIES}/{rid}.src')
            sha = sha.strip('`')
            if copy is None or not re.fullmatch(r'[0-9a-f]{64}', sha) or hashlib.sha256(copy).hexdigest() != sha:
                why.append('copy_sha')
            qs = quotes_of(qcell)
            if not (1 <= len(qs) <= 3) or any(not (3 <= len(q.split()) <= 25) for q in qs):
                why.append('quote_shape')
            ntext = normalise(copy) if copy is not None else ''
            if any(q not in ntext for q in qs):
                why.append('quote_not_in_copy')
            ref = tokens(p['teaches'] + ' ' + p['anchor'] + ' ' + p['scope'])
            if len(tokens(' '.join(qs)) & ref) < 2:
                why.append('quote_off_topic')
            if live:
                if not any(all(q in normalise(b) for q in qs) for b in fetch(p['url'])):
                    why.append('live_quote')
            if verdict == 'drifted':
                for path in [x.strip() for x in p['used_by'].split(',')]:
                    if path.startswith('corpus/knowledge/'):
                        if not any(rid in ln and 'Round32' in ln for ln in added_lines(repo, full, path)):
                            why.append(f'no_correction:{path}')
        elif verdict == 'unreachable':
            if show(repo, full, f'{COPIES}/{rid}.fetch.txt') is None:
                why.append('no_transcript')
            if live and any(True for _ in fetch(p['url'])):
                why.append('counter_fetch_ok')
        if not judge_ok or rid not in agrees:
            why.append('judge')
        if why:
            fails.append(f'{rid}:' + ','.join(why))
        else:
            rows_ok += 1
    # new-source check
    base_src = (show(repo, BASE, 'corpus/SOURCES.md') or b'').decode('utf-8', 'replace')
    tip_src = (show(repo, full, 'corpus/SOURCES.md') or b'').decode('utf-8', 'replace')
    readme = (show(repo, full, README) or b'').decode('utf-8', 'replace')
    gsec = section(lesson, 'Gate')
    ghdr, gbody = table(gsec)
    gates = {}
    for g in gbody:
        gates.setdefault(g[0], []).append(g)
    new_ok, new_fail = 0, []
    for ln in tip_src.splitlines():
        m = re.match(r'^\| (S(\d{3})) \|', ln)
        if not m or int(m.group(2)) < 175:
            continue
        sid, c = m.group(1), cells(ln)
        why = []
        urls = re.findall(r'https?://[^\s|`)<>]+', c[1] if len(c) > 1 else '')
        u = urls[0] if urls else ''
        if len(c) < 11 or c[7] != 'mined':
            why.append('status')
        if not u or u in base_src:
            why.append('url_not_new')
        gs = gates.get(sid, [])
        if len(gs) != 1 or len(gs[0]) < 6:
            why.append('gate_rows')
        else:
            g = gs[0]
            gu, gsha, gq, gdec = g[1].strip('`<>'), g[3].strip('`'), g[4], g[-1]
            copy = show(repo, full, f'{NEWCOPIES}/{sid}.src')
            if gu != u or not gu.startswith('https://'):
                why.append('gate_url')
            if copy is None or not re.fullmatch(r'[0-9a-f]{64}', gsha) or hashlib.sha256(copy).hexdigest() != gsha:
                why.append('gate_copy_sha')
            qs = quotes_of(gq)
            nt = normalise(copy) if copy is not None else ''
            if not qs or any(not (3 <= len(q.split()) <= 25) or q not in nt for q in qs):
                why.append('gate_quote')
            if not gdec.startswith('admit'):
                why.append('gate_decision')
        if sid not in readme:
            why.append('readme_cite')
        if why:
            new_fail.append(f'{sid}:' + ','.join(why))
        else:
            new_ok += 1
    print(f'rows_ok={rows_ok}/{len(pop)} verdicts={dict(sorted(verdicts.items()))}')
    print('row_failures=' + (' '.join(fails) if fails else 'none'))
    print(f'new_ok={new_ok} new_failures=' + (' '.join(new_fail) if new_fail else 'none'))
    if not live:
        print('C1=diagnostic exit=1 (live check R3 skipped)'); return 1
    met = rows_ok == len(pop) and new_ok >= 1
    print(f'C1={"met" if met else "unmet"} exit={0 if met else 1}')
    return 0 if met else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

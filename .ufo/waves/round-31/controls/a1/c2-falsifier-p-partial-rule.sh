#!/usr/bin/env bash
# FALSIFIER P: an honest but partial parser. Implements only the rule clauses the 16 fixtures exercise and omits:
#   rule 1: `opened files` headings, `Opened files:` labels, lowercase forms (match is case-sensitive "Files opened");
#   rule 2: `* ` and `+ ` markers, indented entries;
#   rule 4: quote, bracket and trailing `,;.` stripping; only the first candidate of an entry is checked;
#   rule 6: the round-30 detectors are replaced by two one-line regexes.
# P_IGNORE_INTERFACE=1 additionally ignores <allow-file> (hard-coded globs), <lane-rev> (reads the working tree) and
# <writer-name-regex> (hard-coded ^Case).
python3 - "$@" <<'PY'
import fnmatch, os, re, subprocess, sys
rev, d, wre, allow = sys.argv[1:5]
ignore = os.environ.get('P_IGNORE_INTERFACE') == '1'
if ignore:
    pats = ['.ufo/waves/round-31/rule-text.md', '/fast/scratch/hyaku/mori-r31/{report}/*',
            'https://raw.githubusercontent.com/torvalds/linux/*']
    names = sorted(os.path.join(d, n) for n in os.listdir(d) if n.startswith('Case') and n.endswith('.md'))
    read = lambda p: open(p).read()
else:
    pats = [l.rstrip('\n') for l in open(allow) if l.strip()]
    names = [p for p in subprocess.run(['git', 'ls-tree', '--name-only', rev, d + '/'], capture_output=True,
                                       text=True).stdout.split() if re.search(wre, os.path.basename(p))]
    read = lambda p: subprocess.run(['git', 'show', f'{rev}:{p}'], capture_output=True, text=True).stdout
hits = []
for p in names:
    rep = os.path.basename(p)[:-3]
    inblock, entries = False, 0
    lines = read(p).splitlines()
    for n, line in enumerate(lines, 1):
        if re.search(r'\.py:\d+', line):
            hits.append(f'{p}:{n}:writer-tool-source-citation')
        if re.match(r'exit [012]$', line) and any('Tool run output' in x for x in lines[max(0, n - 4):n - 1]):
            hits.append(f'{p}:{n}:writer-tool-run-output')
        if line.startswith('#'):
            inblock = 'Files opened' in line
            continue
        if line.startswith('Files opened:'):
            inblock = True
            continue
        if not inblock or not line.strip():
            continue
        if line.startswith('|'):
            nxt = lines[n] if n < len(lines) else ''
            if re.fullmatch(r'[|\-: ]+', line) or re.fullmatch(r'[|\-: ]+', nxt):
                continue
            toks = line.split()
        elif re.match(r'- |\d+[.)] ', line):
            toks = line.split()[1:]
        else:
            inblock = False
            continue
        entries += 1
        cands = []
        for t in toks:
            t = re.sub(r':\d+(-\d+)?$', '', t.strip('`'))
            t = t[7:] if t.startswith('file://') else t
            if '/' in t or '.' in t:
                cands.append(t)
        if not cands or not any(fnmatch.fnmatchcase(cands[0], q.replace('{report}', rep)) for q in pats):
            hits.append(f'{p}:{n}:writer-forbidden-opened-path')
    if not entries:
        hits.append(f'{p}:1:writer-missing-files-opened-list')
print(f'scanned={len(names)}'); print(f'blind_violations={len(hits)}'); print('\n'.join(hits))
sys.exit(1 if hits else 0)
PY

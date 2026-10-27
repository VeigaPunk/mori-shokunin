# Mo54RevLedgerProse — prose review of `corpus/knowledge/kernel-v7.3-recheck-r54.md` at 78295c764093ff1f6cee08d7246679900bde7265

Seat: Mo54RevLedgerProse (leaf, no subagents). Scope: the header lines, `## What this ledger is`, `## Where the quotes moved`, `## Release drift` — every number and every statement in those sections, against the committed bytes at the data commit.

Method: the lane HEAD is 2d0347a3 (one commit past the data commit) and its corpus working tree is dirty (`git status --porcelain -- corpus/` → `M corpus/QUALITY.md`, `M corpus/README.md`), so nothing was verified from the working tree. All reviewed bytes were extracted with `git -C <lane> archive 78295c764093ff1f6cee08d7246679900bde7265 -- <paths> | tar -x` into scratch `/fast/scratch/hyaku/mori-r54/Mo54RevLedgerProse/` (disk-guard status checked first: 596.4G free on /fast/scratch/hyaku; scratch removed after this report was written). The frozen counter was re-run independently, and an independent Python checker (mirroring `count-c1.py`'s `norm_map`/`lines_of` whitespace-collapse/offset semantics, HTML tag-stripping included) re-derived every row of the moves table. The checker source is pasted at the bottom of this report.

## Verified true (statement → evidence)

1. **"…the counter's `--scope` at the entering tip `39dcf4d7` lists 31 rows … 22 of `oom-memcg-stat-r50.md`, 8 of `commit-runway-read-r53.md`, 1 of `quota-observability-r48.md`"** — `c1-scope.txt` lists exactly those 31 hashes (8 commit-runway, 22 oom-memcg, 1 quota) and ends `scope=31, exit=0`; the counter's `ENTERING = "39dcf4d7e410d362781a47e8365ca23b5c807598"` matches the stated tip; `--scope` is a real counter mode (`count-c1.py:31` usage, `:410` handling). The Ledger table itself has 31 rows with the same 22/8/1 split.
2. **"Round 53 answered the v7.3 release trigger for 46 claim rows of two entries"** — `kernel-v7.3-recheck-r53.md` has exactly 46 ledger rows (`grep -c '^| [0-9a-f]\{12\} '` = 46), covering `memavailable-estimate-r51.md` (18) + `overcommit-commit-limit-r52.md` (28) = two entries.
3. **Counter derivation / status semantics** — re-run at the data commit: `python3 .ufo/waves/round-54/count-c1.py 78295c76…` → `C1=unmet scope=31 rows=31 matched=31 status_ok=31 line_ok=31 quote_ok=31 source_rows=ok pins=ok provenance=ok held=31 absent=0 holds=31 changed=0 voted=0 dissent=0 rev=78295c76… failed=votes`, exit 1 — unmet only because votes are still pending, exactly matching the author line's "dispositions are `holds` pending the wave's RECHECK voters".
4. **"Four of the eight files did not change at all … `diff` of the committed copies prints nothing"** — `diff <v7.2> <v7.3> | grep -c '^[<>]'`: `oom_kill.c` 0, `lib/percpu_counter.c` 0, `include/linux/percpu_counter.h` 0, `errno.h` 0. Context (not prose claims): the other four are util.c 14, memcontrol.c 258, mm_init.c 211, cgroup-v2.html 95.
5. **"errno.h has the same sha256 as S481's copy"** — `sha256sum` of `sources-r54/errno.h.v7.3` and `sources-r48/errno.h` are both `66a5ad60566fdd62e41701bcfc42bfeca5e5696ad1d47d78981575e0c51622be`, equal to the hash registered in the S481 row.
6. **"`mm/util.c` changed 14 lines, none at the three quoted lines"** — diff count is 14 (hunks at old 578, 627-646, 1188, 1379); difflib changed-line sets on both sides exclude {820, 937, 994}.
7. **Moves table, all 31 rows** — checker output: `ledger rows: 31  moves rows: 31  hash sets equal: True` and `moves-table rows failing: 0 of 31`. For every row the quote begins at the claimed v7.2 line in the committed v7.2 copy and at the claimed v7.3 line in the v7.3 copy (whitespace-collapsed; the docs page tag-stripped/entity-decoded like the counter); the Ledger `line` column agrees and each `moved` value equals v73−v72. This also grounds "All 31 v7.2 quotes occur verbatim in the v7.3 copies."
8. **"`mm/memcontrol.c` (258 changed lines; the OOM report block +45 lines, the `memory.stat` reader +84)"** — changed lines 258 by both the diff tool and difflib; cumulative net shift over diff opcodes reaches exactly +45 before the OOM-report rows (a 36-line insert at old 503 plus +9 earlier) and exactly +84 before old line 4913.
9. **"`mm/mm_init.c` (the `mm_compute_batch` block +4)"** — net +4 accumulated before old line 194 (inserts at 36-38); quoted rows 194/199/204 → 198/203/208 confirmed by the row checker (S514's "mm_compute_batch lines 195-214" is consistent).
10. **"the rendered cgroup-v2 page (+31 lines, from the new top-level navigation)"** — net line shift before v7.2 line 1194 is exactly +31, and the lines added there are the new sidebar/navigation captions ("Working with the development community", "Internal API manuals", "Development tools and processes", …).
11. **"changed in 32 places (word-level diff of the tag-stripped text)"** — an independent tokenizer (strip tags/comments/script/style, decode entities, collapse whitespace, word-level difflib opcodes) yields exactly 32 non-equal places.
12. **"None touches a quoted row: the `memory.stat` keys, units and the `oom_kill` event text are unchanged"** — all seven cgroup-v2 quoted spans occur unchanged at both their v7.2 and v7.3 positions (row checker); none of the 32 word-diff places intersects a quoted row.
13. **"`memory.pressure` and `io.pressure` are now documented "read-write" (7.2: "read-only" …)"** — v7.2 copy: both are "A read-only nested-keyed file"; v7.3 copy: both "A read-write nested-keyed file".
14. **"the `io.stat` throttle field is now `delay_nsec` in nanoseconds (7.2: `delay`, microseconds)"** — v7.2: "the use_delay and delay fields in io.stat increase. The delay value is how many microseconds …"; v7.3: "the use_delay and delay_nsec fields … how many nanoseconds …"; `delay_nsec` occurs 2× in the v7.3 copy, 0× in v7.2.
15. **"the CFS bandwidth stats in `cpu.stat` are now documented as non-hierarchical"** — v7.3 adds "Note that the above five CFS bandwidth stats are non-hierarchical; they only account for throttling caused by this cgroup's own bandwidth limit…", absent in v7.2.
16. **"They are leads for the entries that own those surfaces (`corpus/SOURCES.md` `## Leads (unopened)`)"** — that section carries the round-54 lead recording all three drift items (delay→delay_nsec/nanoseconds, pressure files read-write vs 7.2 read-only, cpu.stat CFS non-hierarchical) and naming this ledger's `## Release drift`.
17. **Header lines** — all eight `source:` ids exist in `corpus/SOURCES.md` and point at exactly the documents used (S508 mm/util.c v7.3, S514 mm/mm_init.c v7.3, S515 memcontrol.c v7.3, S516 oom_kill.c v7.3, S517 lib/percpu_counter.c v7.3, S518 percpu_counter.h v7.3, S519 errno.h v7.3, S520 rendered cgroup-v2 7.3); `.ufo/waves/round-54/controls/c1data.py` exists at the data commit (`git cat-file -e` ok); the `recheck:` command is the counter's real invocation; `verified-at: 2026-10-27` matches the rows' opened dates.
18. **"v7.2 lines below are from the committed v7.2 copies (`sources-r50/`, `sources-r52/util.c.v7.2`, `sources-r53/*.v7.2`, `sources-r48/errno.h`)"** — every v7.2 copy the table relies on lives in exactly those places (oom_kill/memcontrol/cgroup-v2 in sources-r50; util.c in sources-r52; mm_init and both percpu_counter files in sources-r53; errno.h in sources-r48).

## Findings

- **F1 — MED — `corpus/knowledge/kernel-v7.3-recheck-r54.md:63` (`## Where the quotes moved`).** The sentence "The `line:` anchors that `oom-memcg-stat-r50.md` and its rows S490/S491 give in prose (`memcontrol.c:1774-1830`, …) are v7.2 positions; …" cites an anchor that exists in no row: S490's anchor list (corpus/SOURCES.md:269) reads `mm/memcontrol.c:629,1546-1608,1628-1665,1693-1748,1751,1770-1784,1787-1830,1994-1999,4905-4919` — there is no `1774-1830` range (git grep for the literal at the data commit returns only the ledger's own line 63) — and `oom-memcg-stat-r50.md` contains no `memcontrol.c:`/`oom_kill.c:` line anchors anywhere in its prose (grep: no matches), so the anchors live only in the SOURCES.md rows S490/S491, not "in prose" of the entry. The substance (those anchors are v7.2 positions) is true. Suggested replacement: "The `line:` anchors the `S490`/`S491` rows of `corpus/SOURCES.md` give for `oom-memcg-stat-r50.md` (`mm/memcontrol.c:…,1770-1784,1787-1830,…,4905-4919`; `mm/oom_kill.c:400-410,424-431,444-454,456-469,912-985,1008-1054,1146-1170`) are v7.2 positions; read at v7.3 the memcontrol ones are off by the `moved` column (+45, +84)."
- **F2 — LOW — same sentence, line 63.** "read at v7.3 they are off by the `moved` column" overgeneralizes: S491's oom_kill anchors sit in a file that is byte-identical between the tags (all its rows moved +0), so those anchors are still exact at v7.3; only S490's memcontrol anchors are off (+45, +84). Folded into F1's replacement text.
- **F3 — LOW — citation precision, `## Release drift` ("round 24's F8").** Round 24's wave files contain several distinct F8 findings; the one that grounds "the files always accepted PSI trigger writes" is `.ufo/waves/round-24/w1/DraftKnowledgeEntry.md:145` ("F8 — the event-driven interface exists and is not used here. A user registers a trigger by writing …"). The content checks out, but the ledger cites only "round 24's F8", which a reader cannot disambiguate without opening the round-24 wave. No correction required; a file hint would fix it.

## Residual risk and verification gaps

- The "32 places" metric is tokenizer-dependent. My independent tokenization agrees with the claimed 32, but a differently-configured word-diff could produce a different count; the claim's substance (few scattered places, none on quoted rows) is robust either way.
- F3 verified only to the extent that a round-24 F8 item with the trigger-write content exists; I did not reconstruct round 24's finding numbering end-to-end to prove it is the canonical F8 of that round.
- The two dirty working-tree corpus files (`corpus/QUALITY.md`, `corpus/README.md` at HEAD 2d0347a3) were not reviewed — out of scope; all verification here is pinned to the data commit.
- LSP: no language server applies to this markdown data artifact, so verification is git/text-based (recorded per reviewer protocol; no semantic proof claimed beyond the quoted command outputs).

## Checker source (scratch copy, mirrors count-c1.py's norm_map/lines_of)

```python
import re, difflib, html as htmlmod

S = '/fast/scratch/hyaku/mori-r54/Mo54RevLedgerProse'
L = S + '/lane'
led_lines = open(S + '/ledger.md', encoding='utf-8').read().splitlines()

ledger, moves = {}, {}
for ln in led_lines:
    m = re.match(r'\| ([0-9a-f]{12}) \| `?([^|`]+)`? \| (\w+) \| (S\d+) \| ([0-9,]+) \| `(.*)` \| (\w+) \|$', ln)
    if m:
        ledger[m.group(1)] = {'entry': m.group(2).strip(), 'line': m.group(5), 'quote': m.group(6)}
    m = re.match(r'\| ([0-9a-f]{12}) \| ([^|]+?) \| ([0-9,]+) \| ([0-9,]+) \| ([+-]\d+) \|$', ln)
    if m:
        moves[m.group(1)] = {'path': m.group(2).strip(), 'v72': m.group(3), 'v73': m.group(4), 'moved': m.group(5)}

PAIRS = {
 'percpu_counter.h': ('corpus/evidence/sources-r53/percpu_counter.h.v7.2', 'corpus/evidence/sources-r54/percpu_counter.h.v7.3'),
 'percpu_counter.c': ('corpus/evidence/sources-r53/percpu_counter.c.v7.2', 'corpus/evidence/sources-r54/percpu_counter.c.v7.3'),
 'mm/mm_init.c': ('corpus/evidence/sources-r53/mm_init.c.v7.2', 'corpus/evidence/sources-r53/mm_init.c.v7.3'),
 'mm/util.c': ('corpus/evidence/sources-r52/util.c.v7.2', 'corpus/evidence/sources-r53/util.c.v7.3'),
 'mm/memcontrol.c': ('corpus/evidence/sources-r50/memcontrol.c.v7.2', 'corpus/evidence/sources-r54/memcontrol.c.v7.3'),
 'mm/oom_kill.c': ('corpus/evidence/sources-r50/oom_kill.c.v7.2', 'corpus/evidence/sources-r54/oom_kill.c.v7.3'),
 'errno.h': ('corpus/evidence/sources-r48/errno.h', 'corpus/evidence/sources-r54/errno.h.v7.3'),
 'cgroup-v2.html': ('corpus/evidence/sources-r50/cgroup-v2.7.2.html', 'corpus/evidence/sources-r54/cgroup-v2.7.3.html'),
}
def pick(path):
    for k, v in PAIRS.items():
        if path.endswith(k):
            return v
    raise KeyError(path)

TOKEN_RE = re.compile(r"<(script|style)\b.*?</\1\s*>|<!--.*?-->|<[^>]+>|&(?:#[0-9]+|#[xX][0-9a-fA-F]+|[A-Za-z][A-Za-z0-9]*);?", re.S | re.I)

def norm_map(raw, is_html):
    chars, offs = [], []
    if is_html:
        pos = 0
        for m in TOKEN_RE.finditer(raw):
            for i in range(pos, m.start()):
                chars.append(raw[i]); offs.append(i)
            tok = m.group(0)
            if tok.startswith('&'):
                dec = htmlmod.unescape(tok)
                for c in dec:
                    chars.append(c); offs.append(m.start())
            else:
                chars.append(' '); offs.append(m.start())
            pos = m.end()
        for i in range(pos, len(raw)):
            chars.append(raw[i]); offs.append(i)
    else:
        for i, c in enumerate(raw):
            chars.append(c); offs.append(i)
    out, ooffs, prev_ws = [], [], False
    for c, o in zip(chars, offs):
        isws = c.isspace()
        if isws and prev_ws:
            continue
        out.append(' ' if isws else c)
        ooffs.append(o)
        prev_ws = isws
    return ''.join(out), ooffs

def find_start_lines(raw, text, offs, q):
    found, start = set(), 0
    while True:
        i = text.find(q, start)
        if i < 0:
            break
        found.add(raw.count('\n', 0, offs[i]) + 1)
        start = i + 1
    return found

_cache = {}
def load(p, is_html):
    if p not in _cache:
        raw = open(L + '/' + p, encoding='utf-8', errors='replace').read()
        _cache[p] = (raw,) + norm_map(raw, is_html)
    return _cache[p]

def toset(s):
    return set(int(x) for x in s.split(','))

fails = 0
for h in sorted(moves):
    mv = moves[h]
    q = re.sub(r'\s+', ' ', ledger[h]['quote']).strip()
    v72f, v73f = pick(mv['path'])
    is_html = v72f.endswith('.html')
    r72, t72, o72 = load(v72f, is_html)
    r73, t73, o73 = load(v73f, is_html)
    s72 = find_start_lines(r72, t72, o72, q)
    s73 = find_start_lines(r73, t73, o73, q)
    e72, e73 = toset(mv['v72']), toset(mv['v73'])
    led = toset(ledger[h]['line'])
    probs = []
    if not s73:
        probs.append('quote ABSENT in v7.3 copy')
    if s72 != e72:
        probs.append(f'v72 line: claimed {sorted(e72)} got {sorted(s72)}')
    if not e73.issubset(s73):
        probs.append(f'v73 line: claimed {sorted(e73)} got {sorted(s73)}')
    if not led.issubset(s73):
        probs.append(f'ledger line col {sorted(led)} not in got {sorted(s73)}')
    if int(mv['moved']) != min(e73) - min(e72):
        probs.append(f"moved col {mv['moved']} != {min(e73)-min(e72)}")
    if probs:
        fails += 1
        print('FAIL', h, mv['path'], '|', '; '.join(probs))
print('moves-table rows failing:', fails, 'of', len(moves))
# util.c / memcontrol.c / mm_init.c / cgroup-v2.html opcode profiles and drift windows
# (changed-line sets vs {820,937,994}, cumnet profiles, word-level place count, net shift
# before line 1194, added navigation lines, and the read-only/read-write, delay/delay_nsec,
# cpu.stat non-hierarchical windows) follow in the same script as run; outputs quoted above.
```

The full script as run also computed the per-file opcode profiles quoted in items 6, 8, 9, 10, 11 and the drift windows in items 12-15; it was executed from `/fast/scratch/hyaku/mori-r54/Mo54RevLedgerProse/` and produced the outputs quoted above (exit 0).

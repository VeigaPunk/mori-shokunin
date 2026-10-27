# Mo54RevSourcesC1 — registry review of rows S515–S520 and the S508/S514 used-by changes

Seat: Mo54RevSourcesC1 (mori round 54, wave w1) · Date: 2026-10-27 · MACHINE_ID: 432d02b544a5459ebbff9c42ec68334d

Scope: rows S515–S520 and the used-by changes of S508 and S514 in `corpus/SOURCES.md` at the data commit
`78295c764093ff1f6cee08d7246679900bde7265`, against the registry contract in `/home/vgpnk/Projects/shokunin/CORPUS.md`
(section `SOURCES.md — where a shokunin learns`, contract v1). Census run compared with
`.ufo/waves/round-54/evidence/census-start.txt`. Leaf seat, no subagents, no installs (tooling authorization record:
nothing installed; no pacman transaction run; `curl` already present was used for one cgit fetch).

## Method

All reads at the data commit via read-only `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show
78295c76…:<path>`; scratch `/fast/scratch/hyaku/mori-r54/Mo54RevSourcesC1/` (created with `mkdir -p`,
`TMPDIR` pointed at its `tmp/`, removed at the end). Working-tree note: at review time HEAD was `2d0347a3…`
with uncommitted edits to `corpus/QUALITY.md` and `corpus/README.md` (not mine, untouched); `git status
--porcelain -- corpus/` shows `corpus/SOURCES.md` clean, and `git diff --name-only 78295c76 HEAD` listed only
`.ufo/waves/round-54/` files, so the reviewed bytes are the data-commit bytes.

Checks per the contract: kind, tier, scope, anchor (the anchor's quote-lines list vs the ledger's line cells;
sha256 prefix vs the copy), teaches, status, opened, recheck, used-by; plus append-only (field-level diff
entering tip → data commit), enum/shape checks (NF=13, duplicate ids), and the census.

## Row conformance (S515–S520, S508, S514)

| row | kind | tier | scope grounded | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|
| S515 (line 294) | code | A | yes — memcg OOM report + memory.stat formatter quotes | OK (see below) | grounded | mined | 2026-10-27 | on-release | ledger only — correct |
| S516 (line 295) | code | A | yes — victim record / dump_header / report split | OK | grounded | mined | 2026-10-27 | on-release | ledger only — correct |
| S517 (line 296) | code | A | yes — fold rule quote at line 100 | OK | grounded | mined | 2026-10-27 | on-release | ledger only — correct |
| S518 (line 297) | code | A | yes — clamped read quote at line 121 | OK | grounded | mined | 2026-10-27 | on-release | ledger only — correct |
| S519 (line 298) | code | A | yes — EDQUOT 122 quote at line 107 | OK | grounded (byte-identical claim verified, see below) | mined | 2026-10-27 | on-release | ledger only — correct |
| S520 (line 299) | docs | A | yes — memory.stat/memory.events interface; scope fences out print formats (S515, S516) | OK | grounded | mined | 2026-10-27 | on-release | ledger only — correct |
| S508 (line 287) | code | A | yes | OK except one gap (finding 2) | grounded | mined | 2026-10-26 | on-release | gained `kernel-v7.3-recheck-r54.md` — allowed change |
| S514 (line 293) | code | A | yes | OK | grounded | mined | 2026-10-26 | on-release | gained `kernel-v7.3-recheck-r54.md` — allowed change |

Shape/enum: all 297 rows have NF=13 (no `|` inside cells), no duplicate ids, no tier/status/kind violations
(manual census awk checks printed nothing). S515–S524 are the next unused ids after S514, appended once.

## Independent verification (all at 78295c76)

Script `verify2.py` in my scratch re-derived the counter's documented text model (tags → one space, entities
decoded, whitespace collapsed, per-character offset map back to raw lines) and checked, for every one of the
31 ledger rows: the sha256 prefix of the row's copy, and that the quote begins at the ledger's line cell in
the v7.3 copy, and at the moved-table v7.2 line in the committed v7.2 copy. Result: `TOTAL FAILURES: 0`
(91-line output; key lines below).

```
S508: copy=corpus/evidence/sources-r53/util.c.v7.3 sha256_prefix=OK
S514: copy=corpus/evidence/sources-r53/mm_init.c.v7.3 sha256_prefix=OK
S515: copy=corpus/evidence/sources-r54/memcontrol.c.v7.3 sha256_prefix=OK
S516: copy=corpus/evidence/sources-r54/oom_kill.c.v7.3 sha256_prefix=OK
S517: copy=corpus/evidence/sources-r54/percpu_counter.c.v7.3 sha256_prefix=OK
S518: copy=corpus/evidence/sources-r54/percpu_counter.h.v7.3 sha256_prefix=OK
S519: copy=corpus/evidence/sources-r54/errno.h.v7.3 sha256_prefix=OK
S520: copy=corpus/evidence/sources-r54/cgroup-v2.7.3.html sha256_prefix=OK
```

- Anchor quote-lines lists vs ledger line cells: S515 `[1819, 1824, 1845, 1850, 1854, 1872, 2041, 4997]`,
  S516 `[424, 446, 465, 934, 945, 1030, 1169]`, S517 `[100]`, S518 `[121]`, S519 `[107]`,
  S520 `[1225, 1409, 1430, 1437, 1443, 1446, 1465]` — all MATCH the sorted ledger line cells for that source.
- Quote-at-line: 31/31 OK on the v7.3 side and 31/31 OK on the v7.2 side. Every quote occurs exactly once in
  its copy except `460b0cafc999`, which begins at both line 1430 and line 1636 of `cgroup-v2.7.3.html`
  (the ledger's moved table records `1430,1636`; the main-table cell pins 1430 — consistent).
- sha256 cross-check, third way: the computed hashes also equal the ten copies' entries in
  `.ufo/waves/round-54/evidence/freeze-sha256.txt`.
- S519's teaches claim "byte-identical to v7.2 (same sha256 as S481's copy)": verified —
  `corpus/evidence/sources-r48/errno.h` and `corpus/evidence/sources-r54/errno.h.v7.3` both hash to
  `66a5ad60566fdd62e41701bcfc42bfeca5e5696ad1d47d78981575e0c51622be`.
- Tag pin: one small cgit fetch (`curl -sS 'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tag/?h=v7.3'`,
  exit 0) returns tag object `091b06388b117fefdcb63336ac09956a4914b961` and commit
  `c03c1a14507dfaf8b856c2608f9ac216021fc222` — matching every v7.3 row's `tag v7.3 (091b06388b11, commit c03c1a14507d)`.
- S520's `rendered page footer 7.3.0`: the copy contains exactly one `7.3.0` occurrence (the footer) — grounded.
- S508 anchor ranges spot-checked against the copy: 781 `int sysctl_overcommit_memory …`, 806
  `overcommit_policy_handler`, 904 `vm_commit_limit`, 959 `__vm_enough_memory`, 1003 closing brace — accurate.

## Append-only (entering tip `39dcf4d7` → data commit `78295c76`)

`git diff` over `corpus/SOURCES.md` has exactly two hunks: the registry rows and the leads. Field-level:

```
S502 usedby: old corpus/knowledge/kernel-v7.3-recheck-r53.md
             new corpus/knowledge/kernel-v7.3-recheck-r53.md, corpus/knowledge/memory-failure-kills-r54.md
S507 usedby: old corpus/knowledge/kernel-v7.3-recheck-r53.md
             new corpus/knowledge/kernel-v7.3-recheck-r53.md, corpus/knowledge/memory-failure-kills-r54.md
S508 usedby: old corpus/knowledge/kernel-v7.3-recheck-r53.md
             new corpus/knowledge/kernel-v7.3-recheck-r53.md, corpus/knowledge/kernel-v7.3-recheck-r54.md
S514 usedby: old corpus/knowledge/commit-runway-read-r53.md
             new corpus/knowledge/commit-runway-read-r53.md, corpus/knowledge/kernel-v7.3-recheck-r54.md
added rows: S515,S516,S517,S518,S519,S520,S521,S522,S523,S524   removed rows: none
```

Only `used-by` changed in place on existing rows (contract rule 2 allows exactly that); S515–S524 are pure
additions. The v7.2 rows the ledger derives from (S489, S490, S491, S499, S511–S513, S481) keep their used-by —
same convention as round 53 (the ledger cites the v7.3 rows by id; the v7.2 copies are named by path in its
prose only), so no defect.

## Census

Command: `TMPDIR=/fast/scratch/hyaku/mori-r54/Mo54RevSourcesC1/tmp
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
→ exit=0. `diff` against `.ufo/waves/round-54/evidence/census-start.txt`: the only difference is the receipt's
own recorded `exit=0` line; the 23 W04 duplicate-url warnings (S035…S492) and the final `ok` line are
byte-identical. The data commit introduced no new census finding, and no new W04 for the ten new rows.
Note: the census checks shape, enums, tier inflation and used-by path existence (E11) — it does not check
sha256 prefixes or quote-line anchors; those are covered by my independent checks above.

## Findings

1. **MED — missing Search log entry for the round-54 bounded search** (`corpus/SOURCES.md`, Search log
   section lines 315–359 at 78295c76). Contract rule 5 requires one prose note per bounded search
   (question/query, where, date, identified/screened/included/excluded counts, stop rationale). Ten rows were
   opened 2026-10-27 (S515–S520 for C1, S521–S524 for C2) and the data commit edited this file (rows + two
   leads bullets at lines 364–365), but no round-54 note exists: `grep -in 'round 54|round-54'` hits only the
   two leads bullets. Round-53 precedent keeps its two entries in the file (lines 355–356). Fix: the L1 adds
   the note (one per question, following the round-53 two-question pattern) — a data correction, allowed.
2. **LOW — S508's anchor does not locate the line its new used-by quotes** (`corpus/SOURCES.md:287`). The
   anchor lists `sysctl_overcommit_memory/ratio/kbytes defaults 781-783, overcommit_policy_handler 806-840,
   vm_commit_limit 904-916, __vm_enough_memory 959-1003`; the newly cited ledger quotes
   `corpus/evidence/sources-r53/util.c.v7.3` line 937 (`unsigned long vm_memory_committed(void) { return
   percpu_counter_sum_positive(&vm_committed_as); }`), which falls in the unlisted 917–958 gap. Contract-v1
   letter is met (exact lines + revision are present), but the round-54 rows set the quote-lines-list
   convention and a reader following S508's ranges will not find the vm_memory_committed quote. Fix: add
   `vm_memory_committed 937` (or a quote-lines list `820, 937, 994`) to the anchor — data correction.
3. **LOW — pre-existing: two Search log entries sit after the `## Leads (unopened)` heading**
   (`corpus/SOURCES.md:367` Round 38, `:369` Round 39; Leads heading at 360). The Shape orders Search log
   before Leads with all entries inside it. Present at the entering tip too (enter-rev lines 355/357 after
   Leads at 350), so not introduced by this round; the data commit added its leads bullets in the right place.
4. **LOW — S520's quote-lines list omits the second occurrence line** (`corpus/SOURCES.md:299`). The list
   mirrors the ledger's line cells exactly (7 lines, the stated check — passes), but the `460b0cafc999` quote
   also begins at line 1636 of the copy, which the ledger's moved table records as `1430,1636`. Completeness
   note only; no contract text requires enumerating every occurrence.
5. **LOW — ledger provenance-trio format drift** (adjacent, ledger-side: `corpus/knowledge/kernel-v7.3-recheck-r54.md:3`).
   The r54 ledger's source line lists bare ids (`source: S508, S514, S515, …`), while the round-53 ledger's
   source lines carry id + URL + kind/tier + path + copy + opened (r53 ledger lines 3–9). The kaika rule reads
   "cites its S### row … alongside the URL and anchor"; bare ids are still sweep-readable (the counter parses
   ids from that line), so this is a convention drift, not a sweep-breaking defect. The L1 may normalize to the
   r53 format or document the shorter form as the ledger convention.
6. **INFO — used-by old→new logging is owed in the round-54 lesson** (contract rule 2). The four in-place
   used-by changes above (S502, S507, S508, S514) must be logged old→new in the round lesson; no round-54
   lesson file exists at the data commit, so this is UNVERIFIED at review time — a check for the L1 at closure.

No HIGH findings. Everything else in scope conforms: kinds, tiers (A with grounded scopes; S520's rendered
official docs are authoritative for its fenced scope), statuses, opened dates, recheck cadences, used-by
targets (all cited paths exist — census E11 clean), sha256 prefixes, quote-lines lists, quote-at-line on both
sides, the tag pin, and append-only discipline.

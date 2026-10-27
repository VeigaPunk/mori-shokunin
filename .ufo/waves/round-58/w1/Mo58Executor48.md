# Mo58Executor48 — C2 registry binding: attack on the S550 row parser

Seat: Mo58Executor48 (executor). Lane: `mori-shokunin`. Wave: r58 / w1.
Freeze revision used: `fe8801120a67c1a6b8899d7d0423839caa09e7d0`.
Contract: `.ufo/waves/round-58/contract.md`. Counter under attack: `.ufo/waves/round-58/count-c2.py`
(sha256 `aab888ad787964f7a153d64d85dafa58f652f977e21e22eaa492706a691010d3`, byte-identical in the
worktree and at the freeze revision).

**Verdict: the C2 registry-binding (`rows`) arm is NOT sound.** One counter-internal false-negative
that blocks the *real* landing, and five distinct false-green constructions on the `rows` arm that
score `C2=met` on a registry that does not support the claim. All were produced by running the
**frozen counter bytes** unmodified inside throwaway git fixtures.

Scope note: this seat ran only the frozen counter and bounded scratch fixtures. No production file,
corpus registry, SCORECARD, LOG, or lane VCS was modified; no commit was made outside the scratch
fixture; nothing was written to the fleet root or sibling repos.

---

## 1. Method (bounded, receipt-bearing)

Scratch root: `/fast/scratch/hyaku/mori-r58/Mo58Executor48/` (created explicitly, `TMPDIR` pointed at
it for every run, cleaned before yield). Disk guard checked first:
`/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → green,
`/fast/scratch/hyaku` 32% used, **552.9G free**; `/tmp` 124.0G free. No ENOSPC, no rerun needed.

Each harness (`harness.py` … `harness7.py`, receipts `arms.json` … `arms7.json`) does:

* creates a throwaway git repo at the explicit scratch path `…/Mo58Executor48/fixtureN`;
* asserts `git -C <fixture> rev-parse --show-toplevel` == that fixture before any mutation;
* copies the **frozen** `count-c2.py` bytes from `fe8801120a67c1a6b8899d7d0423839caa09e7d0` into
  `<fixture>/.ufo/waves/round-58/count-c2.py` so the counter's own `LANE` resolution
  (4× `dirname` up from `__file__`) lands on the fixture;
* writes `tools/mori-driver-liveness.py` (bytes from the freeze revision) and a byte-identical
  `corpus/evidence/sources-r58/mori-driver-liveness.py` — sha256
  `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997`, matching the S550 row's
  recorded sha256;
* writes the entry and the registry, commits with `git -C <fixture> … commit`, and runs
  `python3 <fixture>/.ufo/waves/round-58/count-c2.py <rev>`.

The counter's own frozen selftest passes unmodified, so the counter is internally consistent:

```
$ python3 .ufo/waves/round-58/count-c2.py --selftest
C2_SELFTEST pass=6 fail=0
rc=0
```

Real-artifact control (frozen counter vs. the real lane at the three relevant revisions):

```
$ python3 .ufo/waves/round-58/count-c2.py fe8801120a67c1a6b8899d7d0423839caa09e7d0
C2=unmet entry=absent failed=entry rev=fe88011…   rc=1
$ python3 .ufo/waves/round-58/count-c2.py b783d0b892637ce8d20f188cad20e4d8913ca635
C2=unmet entry=absent failed=entry rev=b783d0b…   rc=1
$ python3 .ufo/waves/round-58/count-c2.py 4272736cfc5147586e1543413772f80daf44b04b
C2=unmet entry=absent failed=entry rev=4272736c…   rc=1
```

(At HEAD the entry `corpus/knowledge/driver-events-r58.md` is still **untracked** —
`git status --porcelain` shows `?? corpus/knowledge/driver-events-r58.md` and
`?? corpus/evidence/sources-r58/mori-driver-liveness.py`; only `corpus/SOURCES.md` carries the
staged S550 row as a working-tree modification.)

---

## 2. FINDING R58-E48-1 (BLOCKING for the landing) — the real entry scores `claims=0`; C2 cannot reach `met` as staged

**Severity: blocking.** The claim's frozen target output is `C2=met claims=N located=N …` (N ≥ 8).
The entry as it currently sits in the lane worktree scores `claims=0 located=0 failed=claims`, exit 1.
The C2 claim would land `unmet`.

Cause — the frozen counter's claim regex (`count-c2.py:37`):

```python
KLINE = re.compile(r"^- \*\*K(\d+)\*\*.*\((tools/mori-driver-liveness\.py):(\d+)\)")
```

`\*\*K(\d+)\*\*` requires the K-number to be **immediately** closed by `**`. The staged entry writes
the heading as `**K1 — unmatched timestamped prose is separate from a lane event.**` — the `**` comes
after the title, not after the digit. So `KLINE` matches **none** of the eight bullets.

Measured (frozen counter bytes, real worktree entry, real worktree S550 row, real pinned copy):

```
[E0_real_worktree_as_is] rc=1 :: C2=unmet claims=0 located=0 copy=ok tree=ok rows=ok sources=ok failed=claims
```

Per-line regex probe against the staged entry — every bullet is `NO-MATCH`:

```
NO-MATCH - **K1 — unmatched timestamped prose is separate from a lane event.** A timest
NO-MATCH - **K2 — the grammar exposes five parsed fields.** A matched line is split
NO-MATCH - **K3 — launch has its own suffix grammar.** Launch processing parses the rest
NO-MATCH - **K4 — complete has its own suffix grammar.** Completion processing parses the
NO-MATCH - **K5 — wrap validates its own suffix grammar.** A wrap row is accepted only
NO-MATCH - **K6 — lane-dead-no-report validates a retry suffix.** Its rest must match
NO-MATCH - **K7 — launch-fail validates the diagnostic separator and reason shape.** Its rest
NO-MATCH - **K8 — an unparseable first timestamp token is malformed.** When parsing the first
```

Control that isolates the shape as the only cause — the identical entry with the K-headings
reshaped to the contract's own `**K<n>**` form (`- **K1** — title.**`) scores met:

```
[E1_real_entry_reshaped] rc=0 :: C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none
```

and the reshaped entry's quotes all verify as substrings of the pinned copy at their cited lines
(frozen regexes replayed per claim):

```
K1 line=101 located=True  other_lines += 1  # ts-first driver prose (s…   (69 chars)
K2 line=103 located=True  ts_tok, event, lane, round_s, rest = m.group… (47 chars)
K3 line=123 located=True  m2 = LAUNCH_REST_RE.match(rest)              (31 chars)
K4 line=135 located=True  m2 = COMPLETE_REST_RE.match(rest)            (33 chars)
K5 line=145 located=True  if not WRAP_REST_RE.match(rest):              (32 chars)
K6 line=152 located=True  if not DEAD_REST_RE.match(rest):              (32 chars)
K7 line=159 located=True  if not LAUNCHFAIL_RE.match(rest):             (33 chars)
K8 line=96  located=True  if parse_ts(first) is None:                   (27 chars)
=> claims=8 located=8
```

Note the contrast with the frozen **selftest fixture** (`count-c2.py:126-131`), which writes
`- **K{i}** the parser keeps event class {i}. …` — i.e. the counter's own fixture uses the
`**K<n>**` shape the contract names, and the real entry does not. The counter is frozen, so the
fix belongs on the entry side: the eight K-bullets must read `- **K1** …` (the digit closed by
`**`), with the title moved after the marker.

This is a defect the counter *cannot* catch from the registry side and a defect the frozen selftest
*cannot* catch (its fixture is already in the right shape) — the gap only opens on the real entry.

---

## 3. FINDING R58-E48-2 (false green) — the `rows` arm does not bind to the ACTIVE registry table

**Severity: high.** The counter scans the *whole* file for any line starting with `| S550 ` and
never establishes that the row lives in the active `## Registry` table.

`count-c2.py:96-104`:

```python
reg = _show(rev, SOURCES) or ""
row_lines = [ln for ln in reg.splitlines() if ln.startswith(f"| {ROW_ID} ")]
```

Measured — the real `corpus/SOURCES.md` with the S550 row **removed from the `## Registry` table**
and re-homed under `## Leads (unopened)`: the registry table then holds only S549, yet the counter
scores met.

```
[E3_row_outside_registry_on_real_sources] rc=0 :: C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none
```

Same on a synthetic registry (`[D2_row_outside_registry_table] rc=0 :: C2=met … rows=ok`), and also
when the only S550 row in the file is inside a **fenced code block** in the Search log
(`[B8b_row_in_fenced_code_block] rc=0 :: C2=met … rows=ok`).

This is exactly the shape of round-57 routed defect 1 (*"bind to the ACTIVE register table, not the
first `## Capabilities` heading"*) reappearing in C2's registry arm: C1 got an explicit
`_find_register()` that locates the active register section, and C1 resolves its evidence pointers
through `git cat-file -e` (`count-c1.py:105`); C2 does neither. Note the C1 counter *does* bind to
an active section, so the asymmetry between the two counters in the same freeze is itself evidence
the omission is unintentional.

---

## 4. FINDING R58-E48-3 (false green) — the `used-by` check is a substring test, not a pointer resolution

**Severity: high.** `count-c2.py:104`:

```python
if len(cells) < 12 or cells[8] != "mined" or ENTRY not in cells[11]:
```

`ENTRY not in cells[11]` only asks whether the literal string
`corpus/knowledge/driver-events-r58.md` occurs *somewhere inside* cell 11. It never resolves the
pointer (no `git cat-file -e`, unlike C1's `count-c1.py:105`). Three false greens, all measured on
the **real** registry with only cell 11 changed:

| arm | used-by cell 11 | counter |
|---|---|---|
| E2 | `corpus/knowledge/driver-events-r58.md.bak` (no such file) | `C2=met … rows=ok` rc=0 |
| D3 | `corpus/knowledge/driver-events-r58.md.bak` | `C2=met … rows=ok` rc=0 |
| D3b | `see corpus/knowledge/driver-events-r58.md (to be deleted)` | `C2=met … rows=ok` rc=0 |
| D3c | `xcorpus/knowledge/driver-events-r58.md` (substring, not a path) | `C2=met … rows=ok` rc=0 |

All four are `rc=0` with `failed=none`. A dangling or non-path `used-by` therefore satisfies the
"used-by naming the entry" clause of the C2 sourced-claim rule without naming a file that exists.

---

## 5. FINDING R58-E48-4 (false green) — fixed cell indices; a column shift re-points the status and used-by reads

**Severity: high.** The counter reads fixed positions `cells[8]` (status) and `cells[11]` (used-by)
and guards only a *lower* bound on width (`len(cells) < 12`). It never reads the table header, and
never checks that the row's width matches the header's width.

Measured cell dump of the **real** staged S550 row (13 split cells, `cells[8]='mined'`,
`cells[11]='corpus/knowledge/driver-events-r58.md'`) — the conformant case:

```
cells[8]  = 'mined'                              <-- STATUS
cells[11] = 'corpus/knowledge/driver-events-r58.md'  <-- USED-BY
len(cells)=13
```

Now insert one extra cell *before* the status column. The row then has 12 real columns; a human
reading the registry sees status = `queued` and used-by = `—` (dangling), but the counter's fixed
indices still land on `mined` and on the entry path:

```
cells[8]  = 'mined'                              <-- counter reads STATUS here
cells[9]  = 'queued'                             (the row's real status)
cells[11] = 'corpus/knowledge/driver-events-r58.md'  <-- counter reads USED-BY here
cells[12] = '—'                                  (the row's real used-by)
len(cells)=14
```

End-to-end on the real registry row shape:

```
[D4c_status_column_shift] rc=0 :: C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none
[D5b_extra_column]        rc=0 :: C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none
```

A row whose *visible* status is not `mined` and whose *visible* used-by is dangling still scores
`rows=ok`. The counter also ignores the header entirely:

```
[D5c_header_declares_extra_column] rc=0 :: C2=met … rows=ok     (header declares 12 columns, row has 11)
```

---

## 6. FINDING R58-E48-5 (false green) — the entry's frontmatter row-id check is a substring test

**Severity: medium.** `count-c2.py:61`:

```python
for needle in ("source: S550", "verified-at: 2026-10-27", "recheck:", "coverage-map:"):
```

`"source: S550"` is a prefix of `"source: S5500"` and of `"source: S5501"`, so an entry that cites a
**non-existent** registry row passes the `sources` arm:

```
[B9_entry_frontmatter_S5500] rc=0 :: C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none
[B9b_entry_frontmatter_S5501](B7b variant) rc=0 :: C2=met … sources=ok
```

The same substring laxity applies to the other three needles:

```
[C1_verified_at_bogus_suffix]     rc=0 :: C2=met … sources=ok   (verified-at: 2026-10-270)
[C2_coverage_map_in_body_only]    rc=0 :: C2=met … sources=ok   (coverage-map: only in body prose)
[C3_recheck_empty_value]          rc=0 :: C2=met … sources=ok   (recheck: with an empty value)
```

(For contrast, a frontmatter naming a *different real* row is correctly rejected:
`[B9b_entry_frontmatter_S548] rc=1 :: C2=unmet … sources=bad failed=sources`.)

---

## 7. FINDING R58-E48-6 (false green) — a fabricated quote is masked by an incidental span on the same bullet

**Severity: medium-high.** `count-c2.py:86-89`:

```python
spans = re.findall(r"`([^`]+)`", ln)
if 1 <= lineno <= len(copy_lines) and any(
        len(s) >= 12 and s in copy_lines[lineno - 1] for s in spans):
    located += 1
```

A claim counts as *located* if **any** backticked span of length ≥ 12 on that bullet is a substring
of the cited copy line — not the span the author intended as the quote. So a bullet whose primary
quote is entirely fabricated is still counted as located when it *also* backticks an incidental
identifier that genuinely occurs on the cited line.

Constructed correctly (K4 cites line 123, which contains `LAUNCH_REST_RE`; the primary quote is a
sentence that appears nowhere):

```
--- MASKED: fabricated primary quote + incidental `LAUNCH_REST_RE` on cited line 123 ---
  per-claim: [('1',96,True), ('2',101,True), ('3',103,True), ('4',123,True), ('5',135,True), ('6',145,True), ('7',152,True), ('8',159,True)]
  claims=8 located=8
--- CONTROL: identical fabricated quote, no incidental span ---
  per-claim: [('1',96,True), ('2',101,True), ('3',103,True), ('4',123,False), ('5',135,True), ('6',145,True), ('7',152,True), ('8',159,True)]
  claims=8 located=7
```

End-to-end, the masked entry scores **met** while the control is correctly rejected:

```
counter MASKED  rc=0 :: C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none
counter CONTROL rc=1 :: C2=unmet claims=8 located=7 copy=ok tree=ok rows=ok sources=ok failed=quotes
```

This weakens the very construction the round-57 spot-check routed (defect 2, "resolve evidence
pointers and bind quotes against a pinned byte-identical copy"): the copy binding is real, but the
*quote* binding is per-bullet-any-span, so quote-level fabrication is not detected.

---

## 8. Registry-binding arms that are CORRECT (negative results, worth recording)

These behaved correctly against the frozen counter and are **not** defects:

| arm | construction | counter | verdict |
|---|---|---|---|
| D7 / B2 | duplicate `\| S550 ` rows in the same table | `C2=unmet … rows=bad` rc=1 | correct — `len(row_lines) != 1` (`count-c2.py:98`) |
| D7b / B3 | duplicate `\| S550 ` in a *different* section of the file | `rows=bad` rc=1 | correct but **over-strict**: the counter scans the whole file, so a legitimate append-only correction row in a later section breaks the claim |
| D4 / B4 | status cell = `queued` | `rows=bad` rc=1 | correct — exact `!= "mined"` compare |
| D4b / B4b | status cell = `mined (own-work)` | `rows=bad` rc=1 | correct (exact compare) |
| D5 / B6 | row truncated below 12 split cells | `rows=bad` rc=1 | correct — `len(cells) < 12` |
| D6 | only `\| S5500 \|` present | `rows=bad` rc=1 | correct — the prefix is anchored with a trailing space (`\| S550 `), so `S5500` does not match |
| D6b | only `\| S55O \|` (letter O) | `rows=bad` rc=1 | correct |
| D6d | only `\| s550 \|` (lowercase) | `rows=bad` rc=1 | correct |
| D6c | `\| S5500 \|` *alongside* the real row | `rows=ok` | correct — the real row is found; the lookalike is ignored |
| C8 | 12-column row with the entry path in cell 12, cell 11 = `—` | `rows=bad` rc=1 | correct for this shape |

The lookalike-ID family is therefore handled properly: the anchored prefix `"| S550 "` rejects
`S5500`, `S55O` and `s550`. The defects are in the *binding* (which table), the *pointer*
(substring vs. resolution), the *width* (fixed indices, header ignored) and the *quote*
(any-span) — not in the ID matching.

---

## 9. Summary of measured arms (full receipt)

All arms, with the frozen counter's own output, are in
`.ufo/waves/round-58/w1/Mo58Executor48-receipt.txt` (copied from the scratch
`arms*.json` before cleanup). Headline rows:

| arm | rc | counter output | verdict |
|---|---|---|---|
| E0_real_worktree_as_is | 1 | `C2=unmet claims=0 located=0 … failed=claims` | **BLOCKING false negative** |
| E1_real_entry_reshaped | 0 | `C2=met claims=8 located=8 … failed=none` | control |
| E2_dangling_usedby_on_real_registry | 0 | `C2=met … rows=ok` | **FALSE GREEN** |
| E3_row_outside_registry_on_real_sources | 0 | `C2=met … rows=ok` | **FALSE GREEN** |
| D2_row_outside_registry_table | 0 | `C2=met … rows=ok` | **FALSE GREEN** |
| D3/D3b/D3c (used-by shapes) | 0 | `C2=met … rows=ok` | **FALSE GREEN** (×3) |
| D4c/D5b (column shift) | 0 | `C2=met … rows=ok` | **FALSE GREEN** (×2) |
| D5c (header ignored) | 0 | `C2=met … rows=ok` | **FALSE GREEN** |
| B9 (frontmatter `S5500`) | 0 | `C2=met … sources=ok` | **FALSE GREEN** |
| C1/C2/C3 (frontmatter substring) | 0 | `C2=met … sources=ok` | **FALSE GREEN** (×3) |
| MASKED (fabricated quote) | 0 | `C2=met claims=8 located=8` | **FALSE GREEN** |
| CONTROL (no masking span) | 1 | `C2=unmet … failed=quotes` | correct |
| D7/D7b/D4/D4b/D5/D6/D6b/D6d/C8 | 1 | `C2=unmet … rows=bad` | correct |

## 10. Suggested handling (detection only — this seat made no change)

* **R58-E48-1 is the one that changes the landing.** The entry's eight bullets must use the
  `**K<n>**` marker shape (digit closed by `**`), with the title after the marker. The counter is
  frozen and must not change; the entry is not.
* **R58-E48-2 / -3 / -4 / -6** are all the same class of omission C1 already fixed in this freeze:
  bind to the active section, resolve pointers, and check the row's actual column count against the
  header. They are counter defects, and the counter is frozen — so under the contract's kill rule
  they cannot be repaired in round 58 without invalidating the C2 claim. They belong in the round-59
  lesson, and the C2 claim should not be scored as met on the strength of a `rows=ok` that these
  arms show to be satisfiable without a real registry binding.
* **R58-E48-5** is a narrow substring laxity in the `sources` arm.

## 11. Cleanup

Scratch root `/fast/scratch/hyaku/mori-r58/Mo58Executor48/` (3.5M) was removed after the receipt was
copied into the report directory. No fixture, receipt, or temp file was left under `/fast` or `/tmp`
by this seat. `/fast/scratch/hyaku` after cleanup: 577G free, 29% used — the disk guard was green
before and after the work. The lane working tree, HEAD (`4272736cfc5147586e1543413772f80daf44b04b`),
the corpus registry, SCORECARD and LOG were not modified by this seat; the only files written are
the two under `.ufo/waves/round-58/w1/` named in this report.

## 12. Blockers / limits of this seat

* No blocker: every arm ran against the frozen counter bytes and produced a receipt.
* The `rows`/`sources` arms are **frozen** by the contract's kill rule, so findings R58-E48-2/3/4/5/6
  cannot be repaired here; they are reported as findings for the L1 to route to round 59.
* This seat did not evaluate C1, the round-57/56 claims, the census, or the quarantine slice; it did
  not score either claim and does not judge.

# ScrLessonDraft — round-40 wave 1 seat report

- Seat: `ScrLessonDraft` (scribe), mori round 40 wave 1.
- Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`. This seat made no production edits.
- Report path: `.ufo/waves/round-40/w1/ScrLessonDraft.md` (the dispatch text carried no `Report:` trailer; the path follows the wave `reportDir` convention already used by `.ufo/waves/round-40/w1/ExeCensus.md`).
- Assignment: draft `corpus/lessons/round-40.md` `## Mistakes` rows (M23 inherited-unverified-freeze, M24 parenthetical arithmetic) and the `## Gate` table row for S229 with the located quote "When a name is used in a code block, it is resolved using the nearest enclosing scope" (spec label: 15 words, §4.2.2).

## Behavior

The requested rows already exist in `corpus/lessons/round-40.md` (file committed at `8d3badd`; HEAD `ede486b`), so this seat audited the landed draft against committed ground truth instead of writing a second copy into production. No instrument was rerun (re-derivation seats exist in this wave); every number below is read from a committed receipt or derived from one by the command shown. Where the landed text and a receipt disagree, both strings are reported verbatim.

## Landed draft (verbatim, corpus/lessons/round-40.md at HEAD ede486b)

### `## Gate` row (line 7)

| source | decision | located quote |
|---|---|---|
| S229 — Python execution model, Naming and binding `https://docs.python.org/3/reference/executionmodel.html#naming-and-binding`, opened 2026-10-24 (copy `corpus/evidence/sources-r40/S229.src`) | **admitted** (mined) | `S229.src` §4.2.2 Resolution of names: "When a name is used in a code block, it is resolved using the nearest enclosing scope." (15 words) |

### `## Mistakes` rows (lines 23–24)

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M23 | inherited-unverified-freeze (a prior launch froze instruments in prose but died before persisting the freeze receipt or any receipt) | the inherited working tree held `contract.md` claiming pins in `evidence/freeze-r40.txt`, but that file did not exist; no before/after receipt existed either — only `census-start.txt` | none — no criterion required a freeze receipt to be verified present before integration; the r39 finding-9 discipline (receipts name the measured rev) extends to freeze receipts now | the resuming L1 re-verified every inherited instrument byte-by-byte (gate v3 diff audit, conform v3 selftest, parity, survivor regeneration), completed the unfinished work (gate selftest arms 12→15; dag-r redesign), and persisted `evidence/freeze-r40.txt` with sha256 pins plus an honest note that it was written at integration; before-controls all run bytes extracted via `git show bb1f2457:<path>`, so entering-state measurement is uncontaminated. Shown able to fail: any post-freeze instrument edit would mismatch the pinned sha256 set |
| M24 | number-drift (a parenthetical arithmetic inside the frozen predicate mis-predicted the measured value) | the contract and the P-C11 sentence's parenthetical say "S226 joins superseded_as_of (19 ids) at the landed tip"; the measured lane line at T1 lists **34** as-of ids — the eligible-set extension admits every never-edited superseded row present at R (16 rows: S226 plus 15 earlier), which the parenthetical arithmetic did not count | claim-sizing lesson (brief §9: declare after-states as one command over committed bytes; never freeze a counted prediction that the counter does not enumerate) — applied one round late | the SCORECARD after-cell and this lesson record the measured 34 and name the 16 never-edited ids as a class; the predicate's semantic sentence (the real counter) is unchanged and verified; the parenthetical is marked corrected-by-measurement |

## Verification — exact commands and outputs

All commands run from `/home/vgpnk/Projects/shokunin/mori-shokunin`. Git read-only (`--no-optional-locks` where a status/index touch was possible); no mutating git/jj.

### 1. The S229 quote is present in the stored copy and inside §4.2.2

```text
$ grep -n "When a name is used" corpus/evidence/sources-r40/S229.src
294:<p id="index-8">When a name is used in a code block, it is resolved using the nearest enclosing
$ sed -n '295p' corpus/evidence/sources-r40/S229.src
scope.  The set of all such scopes visible to a code block is called the block’s
$ grep -n 'section-number">4\.2' corpus/evidence/sources-r40/S229.src
249:<span id="naming"></span><h2><span class="section-number">4.2. </span>Naming and binding…
251:<span id="bind-names"></span><span id="index-3"></span><h3><span class="section-number">4.2.1. </span>Binding of names…
288:<span id="resolve-names"></span><h3><span class="section-number">4.2.2. </span>Resolution of names…
356:<span id="id1"></span><h3><span class="section-number">4.2.3. </span>Annotation scopes…
```

The located quote spans `S229.src:294-295` and sits inside §4.2.2 (heading at 288). Copy path exists; copy committed at `265a955`.

### 2. Word count of the located quote — measured 17, not 15

```text
$ printf '%s\n' 'When a name is used in a code block, it is resolved using the nearest enclosing scope.' | wc -w
17
```

Parsing the landed Gate row (quote extracted between the double quotes):

```text
quote: When a name is used in a code block, it is resolved using the nearest enclosing scope.
words: 17
section cited: True | copy: True | date: True
```

### 3. Registry before → after

```text
$ grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md
229
$ git --no-optional-locks diff --stat bb1f2457 265a955cc -- corpus/SOURCES.md
 corpus/SOURCES.md | 1 +
 1 file changed, 1 insertion(+)
$ git --no-optional-locks diff bb1f2457 265a955cc -- corpus/SOURCES.md | grep -E '^[-+]\| S[0-9]'
+| S229 | Python execution model — Naming and binding — https://docs.python.org/3/reference/executionmodel.html#naming-a…
```

228 → 229 with one insertion and no `-` row: no existing row's cells were rewritten in place. The S229 registry row is `corpus/SOURCES.md:235`; its status cell is `mined`, its fetch cell says `page fetched 2026-10-24`, matching the Gate row's `**admitted** (mined)` and `opened 2026-10-24`.

### 4. Census receipts

```text
$ grep -c $'^mori\tW04' .ufo/waves/round-40/evidence/census-start.txt
16
$ grep -c $'^mori\tW04' .ufo/waves/round-40/evidence/census-end.txt
16
$ grep -c 'S229' .ufo/waves/round-40/evidence/census-end.txt
0
$ tail -1 .ufo/waves/round-40/evidence/census-start.txt
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
$ tail -1 .ufo/waves/round-40/evidence/census-end.txt
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

S229 adds no new warning class; the 16 standing W04 rows are unchanged across start and end.

### 5. M23 evidence — contract claimed pins while the receipt did not exist at the instruments commit

```text
$ git cat-file -e 265a955cc67be4eae97d2dc5a9338a25f31eb29b:.ufo/waves/round-40/evidence/freeze-r40.txt; echo rc=$?
rc=128
$ git cat-file -e 265a955cc:.ufo/waves/round-40/evidence/census-start.txt; echo rc=$?
rc=128
$ git cat-file -e 265a955cc:.ufo/waves/round-40/evidence/c10-red-cond.txt; echo rc=$?
rc=128
$ git show 265a955cc:.ufo/waves/round-40/contract.md | grep -n freeze-r40
9:`evidence/freeze-r40.txt` (sha256 over the frozen paths). A change to a
151:`evidence/freeze-r40.txt`, `evidence/census-start.txt`, `census-end.txt`,
$ sha256sum .ufo/waves/round-40/contract.md
6514914885e6a1249ed7903931b9734a55e828275121353c2727348eae504a8d  .ufo/waves/round-40/contract.md
$ git --no-optional-locks log --oneline --follow -- .ufo/waves/round-40/contract.md
265a955 round-40: instruments — conform v3 (P-C10), gate v3 (P-C11), S229, r39 erratum
$ git --no-optional-locks log --oneline -- .ufo/waves/round-40/evidence/freeze-r40.txt
8d3badd round-40: evidence receipts, wave spec (66-seat v2, validated), SCORECARD/LOG/lesson
$ git --no-optional-locks log --oneline -- .ufo/waves/round-40/evidence/census-start.txt
8d3badd round-40: evidence receipts, wave spec (66-seat v2, validated), SCORECARD/LOG/lesson
```

`freeze-r40.txt` header (verbatim):

```text
freeze-r40: sha256 over the round-40 frozen instrument paths
pinned: 2026-10-24T05:46:06Z by L1 mori-r40 attempt 1 (resumed)
note: the prior launch died before persisting this receipt; before-receipts
      run committed bytes extracted via 'git show bb1f2457:<path>' (see
      fixtures/extracted/), so before-controls are measured at entering bytes.
```

The contract's own pin digest matches the freeze receipt's first pin line; the receipt enters git at `8d3badd`, one commit after the contract (`265a955`). This verifies the M23 core: the contract referenced pins in a file absent from the instruments commit. Which files the dead launch had left in the *uncommitted* worktree (the "only `census-start.txt`" clause) is not reconstructible from git and is prose-only — see F4.

### 6. M23 fix-cell corroboration — extracted before-bytes and selftest count

```text
$ sha256sum .ufo/waves/round-40/fixtures/extracted/*.py
fe0be179aba9df7150f0b6cdb50a5f9bbdb411efb1263b46ffa6b21d46ef7987  .ufo/waves/round-40/fixtures/extracted/conform-v2-r39.py
b92c65f224a6268a901aa6bc5ad66b499048eaca82b493356eb8e1f324ef0520  .ufo/waves/round-40/fixtures/extracted/count-c7-r39.py
62cd4132dbe141538371f79723c3caff66670fab9076494cd9cf65efccfc01e7  .ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py
$ head -1 .ufo/waves/round-40/evidence/c10-red-cond.txt
command: python3 .ufo/waves/round-40/fixtures/extracted/conform-v2-r39.py bb1f2457 --counter .ufo/waves/round-40/fixtures/generated/survivor-cond.py
$ head -1 .ufo/waves/round-40/evidence/c11-red-neveredited.txt
command: python3 .ufo/waves/round-40/fixtures/run-c11-dags.py .ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py /home/vgpnk/Projects/shokunin/mori-shokunin /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/evidence/c11-red-neveredited.txt dag-n
$ grep -m1 SELFTEST .ufo/waves/round-40/evidence/c11-after-selftest.txt
MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0
```

The three extracted digests match the freeze receipt's `extracted before-instrument bytes` block; red receipts name those paths. `pass=15` matches the fix cell's completion claim (the 12 arms it started from are the r39 measured selftest, round-39 lesson finding 7).

### 7. M24 evidence — declared 19, measured 35, never-edited class 17

```text
$ python3 <parse evidence/c11-after-lane.txt>
timing lines: 1
count: 35
entries: 35 unique: 35
first/last: S041 S226
S226 position: 35
violations: 18 changed: 18 superseded: 35 never-edited: 17
16 earlier: S067,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140 | count: 16
$ python3 <parse evidence/c11-before-lane.txt>
before count: 18
command: python3 .ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py bb1f2457 --repo .
EXIT=1
```

Receipt lines quoted verbatim:

```text
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226] stale_supersede=[]
```

Contract (`265a955`), line 119 tail: `… S226 joins superseded_as_of (19 ids) at the landed tip, no id is stale at the tip, S069 is stale at e37dcc6 …`
Contract line 137: `` `supersede_timing superseded_as_of=[19 ids incl. S226] stale_supersede=[]` ``

The M24 class claim is verified (19 declared vs 35 measured); the row's own measured numbers are not — see F2.

### 8. Working tree

```text
$ git --no-optional-locks status --porcelain
?? .scratch/
```

No tracked file was modified by this seat; `.scratch/` is other seats' untracked work.

## Findings

### F1 — Gate row's word-count label is 15; the quoted sentence is 17 words (number-drift)

Conflict, verbatim:

- landed cell: `"When a name is used in a code block, it is resolved using the nearest enclosing scope." (15 words)`
- measured: `17` (`printf … | wc -w`; row parse both return 17).

`LOG.md:2305` repeats it: `15-word located quote`. This is the same defect class the round-39 erratum corrected for S227 — `corpus/lessons/round-39-erratum.md:18-20`: *"Round-39 lesson Gate row for S227 labels its located quote «(18 words)»; the quote … is 17 words."* The reviewer's `<=25 words` criterion still passes; the parenthetical label is false. Proposed replacement (not applied): `(17 words)`.

### F2 — M24's measured numbers are off by one against the receipt it cites (number drift inside the number-drift row)

Conflict, verbatim:

- landed cell: `the measured lane line at T1 lists **34** as-of ids — … (16 rows: S226 plus 15 earlier)`
- receipt `evidence/c11-after-lane.txt`: 35 unique ids in `superseded_as_of`, S226 last; never-edited class = 35 − 18 changed = 17 ids (S226 plus 16 earlier: S067,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140).

The same `34` appears in `SCORECARD.md:2234` (*"the measured value is **34 as-of ids** at T1"*) and `LOG.md` (*"lane line at T1 lists 34 as-of ids incl. S226"*). The mistake class stands (contract declares 19; the receipt enumerates 35), but the row's fix cell (`record the measured 34`) records a value the cited receipt does not support. Proposed replacement (not applied): `35 as-of ids` and `17 rows: S226 plus 16 earlier`.

Note: 34 is exactly the receipt count minus S226, i.e. the arithmetic that forgot S226 is itself a never-edited superseded row — the same counting error the row documents.

### F3 — SOURCES.md S229 anchor does not resolve against the stored copy (located-quote defect, immutable cell)

Registry cell 6, verbatim (`corpus/SOURCES.md:235`): `§4.2.2 Resolution of names:249-262; "When a name is used in a code block, it is resolved using the nearest enclosing scope":254-256; page fetched 2026-10-24`.

Against `corpus/evidence/sources-r40/S229.src`:

- §4.2.2 heading is line **288**, not 249; line 249 is the §4.2 heading and 251 is §4.2.1.
- The quote is lines **294-295**; lines 254-256 are `<ul class="simple">` / `formal parameters to functions` / `class definitions` under §4.2.1.
- §4.2.2 runs 288-355 (4.2.3 starts at 356), so a resolving anchor would be `:288-355` with the quote at `:294-295`.

This is the S226 `:657-658` → S228 `:657-659` class (round-39 M20, QUALITY 113): a located-quote defect in an immutable registry cell; a correction must ride an erratum or a superseding row, not an in-place edit. (For contrast, S228's `:657-659` and S227's `:2542-2544` do resolve in their `.src` copies.) The lesson Gate row carries no line-number suffix, so this is a registry finding, not a Gate-row defect.

### F4 — M23's "only `census-start.txt`" clause is prose-only (not receipt-backed)

Verified from git: at `265a955` the contract referenced `evidence/freeze-r40.txt` (lines 9, 151) while the receipt, `census-start.txt`, and the red receipts were all absent from that commit (`git cat-file -e` rc=128 each); the freeze receipt's note discloses the prior launch's death. Not verifiable from git: the contents of the inherited *uncommitted* worktree, because the resuming L1 published the whole set at `8d3badd`. The clause is an honest prose record (and the M23 class is precisely about unpersisted artifacts), but it is not an enumerated receipt and should not be graded as one.

## Positive verifications (for grading)

- Gate row: quote present verbatim at `S229.src:294-295` inside §4.2.2 (288); copy path `corpus/evidence/sources-r40/S229.src` exists; access date `2026-10-24` matches the registry row's fetch cell; decision `**admitted** (mined)` matches the registry status `mined`.
- Registry: 229 rows; `bb1f2457 → 265a955cc` is a single insertion of the S229 row, no existing row rewritten.
- Census: 16 W04 rows at start and at end; S229 absent from warnings; both receipts end `mori ok`.
- M23: contract pin digest matches the freeze receipt; extracted before-instrument digests match the freeze block; red receipts name the extracted v2 bytes; gate selftest `pass=15 fail=0`.
- M24: class substantiated (19 declared vs 35 measured); `S226` present in `superseded_as_of` (position 35); `stale_supersede=[]`.

## Out of scope / not done

- No production edit: `corpus/lessons/round-40.md`, `corpus/SOURCES.md`, `SCORECARD.md`, `LOG.md` and every other tracked path are untouched; the requested rows already exist at HEAD `ede486b`. Findings F1–F4 are routed for the canonical judge / L1, not applied.
- No instrument rerun (gate/conform re-derivations are other seats' items); all numbers above are committed receipts or direct parses of them.
- No mutating git/jj; no fleet or sibling-lane writes; no `pacman` (host-wide guard respected); no installs were needed.

## Touched surfaces

- Written: `.ufo/waves/round-40/w1/ScrLessonDraft.md` (this report only).
- Read: `corpus/lessons/round-40.md`, `corpus/lessons/round-39-erratum.md`, `corpus/SOURCES.md`, `corpus/knowledge/conform-scope-r40.md`, `corpus/evidence/sources-r40/S229.src`, `corpus/evidence/sources-r39/S227.src`/`S228.src`, `.ufo/waves/round-40/contract.md`, `.ufo/waves/round-40/evidence/{c11-after-lane,c11-before-lane,c11-after-selftest,c11-red-neveredited,c10-red-cond,census-start,census-end,freeze-r40}.txt`, `SCORECARD.md`, `LOG.md`, `.ufo/waves/round-40/w1-spec.json`.

## Artifact paths

- This report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/w1/ScrLessonDraft.md`
- Drafted lesson: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-40.md` (landed at `8d3badd`)
- Ground-truth receipt for the contested count: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/evidence/c11-after-lane.txt`
- Ground-truth copy for the quote: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r40/S229.src:294-295`

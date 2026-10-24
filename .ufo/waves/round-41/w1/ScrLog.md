# ScrLog — append-only LOG corrections & claim-pointer audit (mori round 41, w1)

Seat: `ScrLog` (scribe), round 41 wave 1, lane `mori-shokunin`.
Role: scribe/auditor. Read-only against production bytes; this report is the only
artifact written. All git invocations were read-only (`log`, `show`, `diff`,
`numstat`, `cat-file`, `rev-parse`, `merge-base --is-ancestor`, `sha256sum`);
no counters were re-run, no sandboxes were created, no lane Git/jj/index state
was touched. Attempt 2 lane head at audit time: `7450722e`
(`round-41: after-measurement receipts …`); entering tip per contract:
`62a207f7521fa2e2fcd2e8b0260f047ccfce8862`.

## Scope

Audit the append-only discipline of `LOG.md` corrections and claim pointers, and
verify that old r40 entries were not silently rewritten. C3 surface
(calibration 34/16 → 35/17) under the frozen contract
`.ufo/waves/round-41/contract.md`.

## Method (exact read-only commands)

- `git diff --numstat <tip> -- LOG.md` and `git diff -U0 <tip> -- LOG.md |
  grep -c '^-[^-]'` for tip ∈ {`62a207f` (entering), `8d3badd0` (r40 LOG
  commit)} vs worktree/HEAD — insertion/deletion counts and removed-line counts.
- Per-commit: `git show --numstat` and `git show -U0 | grep -c '^-[^-]'` for the
  two r41 LOG-touching commits `aa161e99`, `c5326c61`.
- Section integrity: `sed -n '2276,2316p' LOG.md` (Round 40 section) read at
  HEAD and compared with `git show 8d3badd0:LOG.md`; `grep -n '^## Round'`.
- Pointer existence: `test -e` over 16 round-41 and 14 round-40 claim-pointer
  paths cited by LOG entries.
- Pin verification: `sha256sum` of all 19 files pinned in
  `evidence/freeze-r41.txt`, compared against the recorded hashes.
- Receipt pointer-consistency reads (no re-execution): `calibration-after.txt`,
  `control-after.txt`, `census-end.txt`.
- Regex form check: `tools/mori-round41-calibration.py` lines 17–18
  (`CORRECTION_RE`) read; `grep -n 'Round-41 calibration correction' LOG.md`.

## Findings

### F1 — LOG.md is strictly append-only since the entering tip (no silent r40 rewrite)

- `62a207f..HEAD/worktree`: **+50 / −0** lines in `LOG.md`; zero removed lines
  (`grep -c '^-[^-]'` → 0).
- Commit `aa161e99` (C3 correction records): **+46 / −0**.
- Commit `c5326c61` (single-line records): **+4 / −0**.
- `62a207f..8d3badd0`: no `LOG.md` change at all (empty numstat) — the r40 entry
  landed at `8d3badd0` and was byte-identical through the entering tip.
- The Round 40 section (`## Round 40 (L1 mori-r40, attempt 1 resumed…`,
  LOG.md:2276–2316 at HEAD) is present verbatim; the only new heading is
  `## Round 41 (L1 mori-r41, attempt 2 …)` at LOG.md:2317.

**Verdict: no r40 entry was rewritten, truncated, or edited in place.**

### F2 — Historical wrong text remains and is explicitly superseded (C3 claim form)

- The stale figure survives untouched at LOG.md:2296:
  "lane line at T1 lists **34** as-of ids incl. S226" (present at entering tip
  line 2296 and at HEAD worktree).
- The correction is appended, not substituted: single-line record at
  LOG.md:2363 `Round-41 calibration correction: observed_as_of=35;
  extension_rows=17.` followed by a parenthetical explaining the single-line
  form. Exactly one regex-matchable record exists in `LOG.md` (the in-entry
  phrase is line-wrapped and does not match).
- The frozen counter `tools/mori-round41-calibration.py` uses
  `CORRECTION_RE = r"Round-41 calibration correction: observed_as_of=(\d+);
  extension_rows=(\d+)\."` and takes `corrections[-1]` (line 81) — the appended
  record is exactly the form the counter parses. Commit `c5326c61` re-shaped the
  records to this single-line form; its LOG diff is +4/−0, so the reshaping was
  itself append-only.

### F3 — Same append-only pattern in the other two correction carriers

- `SCORECARD.md`, `62a207f..HEAD`: **+36 / −0**; the r40 declaration rows
  (SCORECARD.md:2216–2249) untouched; the correction block (lines 2264–2268)
  appends "Round-41 … line supersedes the round-40 '34 as-of ids'/'16
  never-edited' figures" naming the gate at `62a207f`.
- `corpus/lessons/round-40.md`, `62a207f..HEAD`: **+15 / −0**; appended lines at
  68–73 explicitly supersede M24's "34" / "(16 rows: …)" wrapped paragraph
  above, which the counter's one-line regex [does not match]. M24's original
  text remains.
- `corpus/SOURCES.md`, `62a207f..HEAD`: **+4 / −0**; S230/S231 rows appended;
  S229 row (line 235) untouched — its old located-range "§4.2.2 …:249-262" and
  quote ":254-256" cells were not edited in place; the correction rides S231's
  `supersedes S229` row (line 237) with the corrected 17-word locator
  `S229.src:294-296`. Matches the contract freeze boundary "No existing SOURCES
  row's immutable cells will be edited."

### F4 — Claim pointers all resolve

Round-41 entry pointers (all exist): `contract.md`, `evidence/freeze-r41.txt`,
`evidence/control-after.txt`, `evidence/calibration-after.txt`,
`evidence/census-start.txt`, `evidence/census-end.txt`, `conform.py`,
`w1-spec.json`, `evidence/wave-plan.json`, `tools/mori-sources-appendonly.py`,
`tools/mori-round41-calibration.py`, `corpus/evidence/sources-r41/S230.src`,
`corpus/evidence/sources-r41/S231.src`,
`corpus/knowledge/conform-bindings-r41.md`, `corpus/lessons/round-41.md`,
`.scratch/round22/`.
Old r40 entry pointers (spot-checked, all exist): `round-40/contract.md`,
`evidence/freeze-r40.txt`, `c10-after.txt`, `c10-after-selftest.txt`,
`c11-after-selftest.txt`, `c11-after-lane.txt`, `c11-after-e37dcc6.txt`,
census start/end, `wave-plan.txt`, `round-40-verifier-spotcheck.md`,
`conform-scope-r40.md`, `sources-r40/S229.src`, `round-39-erratum.md`.
Commit pointer `e37dcc6` resolves (`round-37 verifier spot-check erratum …`).
Lesson pointers inside `round-41.md` resolve: Gate rows cite S230/S231 with the
admitted copies; Mistakes M25 (number-drift, citing LOG.md:2296 "34") and M26
(S230/S231 copy landing) both re-verified against the bytes named.

### F5 — Freeze pins: 19/19 match live bytes

`evidence/freeze-r41.txt` contains exactly 19 SHA-256 pin lines; all 19
recomputed `sha256sum` values **MATCH** at the current worktree (contract,
conform.py, both round-41 tools, run-r41-controls, c2/c1 fixtures incl. three
survivors, extracted v3 bytes, w1-spec, control-before, census-start,
wave-plan, freeze-r40, conform-bindings-r41.md, corpus/README.md). The LOG
claim "all 19 re-verified byte-exact" is pointer-consistent with the live tree.

### F6 — Receipt headline values consistent with LOG claims (read-only reads)

- `calibration-after.txt`: `LOG.md recorded_as_of=35 observed_as_of=35
  recorded_extension=17 observed_extension=17` and
  `MORI_R41_CALIBRATION mismatches=0 observed_as_of=35 extension_rows=17`
  (SCORECARD and round-40 lesson rows likewise 35/17) — matches the LOG C3
  bullet and the appended record.
- `control-after.txt`: honest counter `CONFORM=met`; walrus survivor
  `CONFORM=unmet` with only `timeout_scope` FAIL (line 26) and all other checks
  PASS; `CONFORM_SELFTEST pass=14 fail=0` (line 80);
  `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` (line 100) — matches the
  LOG C1/C2 bullets. Receipt commands ran in `/tmp/mori-r41-sandbox-*/`
  checkouts at `aa161e99`, consistent with the "disposable sandbox" boundary.
- `census-end.txt` present with the standing W04 duplicate-URL warnings and
  `mori ok` tail, consistent with `census-start.txt` behavior described in the
  contract (16 standing W04s).

### F7 — Worktree/lineage observations (no violations)

- Lineage: `62a207f` → `d72ac167` (freeze C1–C3) → `e4293ad9` (considerthese
  daily reflection) → `aa161e99` → `c5326c61` → `7450722e` (HEAD, after-
  measurement receipts + SCORECARD r41 declaration + lesson fix).
  `62a207f` is an ancestor of HEAD (`merge-base --is-ancestor` OK).
- HEAD `7450722e` touches `corpus/lessons/round-41.md` (+8/−4) — a current-round
  file, not an old-entry rewrite; the diff replaces this-round prose about
  `.scratch/round22/` disposition (154 measurement records committed;
  ~646 MB of nested-git sandbox clones deleted as transient scratch). LOG.md is
  not touched at HEAD; it was finalized at `c5326c61`.
- Worktree is clean for all audited files; untracked: `wave-run.json`,
  `wave-run.stderr`, `w1/` (this report's directory). No tracked file modified.
- LOG.md itself: 2365 lines at HEAD; no in-place mutations anywhere in the
  audited range.

## Limits

- Read-only audit: counters and fixtures were **not** re-executed; receipt
  values above are pointer-consistency reads of committed bytes, not fresh
  measurements.
- The regex-vs-record match was established by reading
  `tools/mori-round41-calibration.py:17-18,79-81` and grepping LOG.md; the
  counter was not run by this seat (its result is recorded in
  `evidence/calibration-after.txt`).
- Append-only was verified over the commits touching `LOG.md` listed by
  `git log -- LOG.md` for the r40→r41 range plus the full entering-tip→HEAD
  diff; earlier-round LOG history (rounds ≤39, including the round-38
  append-only amendment precedent at LOG.md:2186) was inspected only as
  context, not exhaustively re-audited.
- No tools were installed or updated (none needed).

Report: `.ufo/waves/round-41/w1/ScrLog.md`

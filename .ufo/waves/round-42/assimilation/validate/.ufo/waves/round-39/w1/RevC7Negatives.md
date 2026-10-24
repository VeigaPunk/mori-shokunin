# RevC7Negatives — four-witness projection and counter negative lines

Scored tip `13bfba23b7ca063c76d3504a2ff6eb7b6a294932` (all runs below at that rev).
Verdict: **PASS** for the assigned negative arm. All four witnesses are rejected, each by
exactly one v2 check; no witness passes all five; the counter's four `negative` lines all say
`rejected`, and each rejection reason matches the check named below.

## Method

1. Canonical run: `python3 .ufo/waves/round-39/count-c7.py 13bfba23b7ca063c76d3504a2ff6eb7b6a294932 --seed 20261024`
   → `C7=met`, exit 0 (9.2 s), all five `check` lines PASS.
2. Per-check projection: imported the frozen counter as a module and substituted one witness for the
   one real input it forges, keeping the other inputs at R; ran `check_anchors_v2`,
   `check_capability_v2`, `check_live_rows_v2` separately.
3. Full-counter projection: `git clone --shared` of the lane at R into
   `.ufo/waves/round-39/scratch/RevC7Negatives/repo-probe`, then one commit per witness replacing
   exactly the forged file, and the frozen counter run as
   `count-c7.py HEAD --repo <clone> --seed 20261024`. Each run: exit 1, `C7=unmet`.

## Witness → failed check

| witness | substituted for (other real bytes kept) | rejecting check | counter detail (verbatim) |
|---|---|---|---|
| `witness-token-entry.md` | `corpus/knowledge/source-drift-content-anchor-r38.md` | `anchors_v2` | `anchors=0 short=[] not_in_code=[] unique=True` |
| `witness-dangling-row.md` | `SCORECARD.md` | `capability_v2` | `paths=['tools/mori-source-drift.py', 'evidence/no-such-receipt.txt'] not_file=['evidence/no-such-receipt.txt']` |
| `witness-summary-only-live.txt` | `.ufo/waves/round-37/evidence/drift-live-r37.txt` | `live_rows_v2` | `named=0 summary_drifted=10 unknown=[] unique=True no_copy=[]` |
| `witness-comment-anchors.md` | `corpus/knowledge/source-drift-content-anchor-r38.md` | `anchors_v2` | `anchors=3 short=[] not_in_code=[all three anchors] unique=True` |

Each projection passes the other four checks. `named_row_drift`/`drift_kill_v2` read only the real
tool blob (`show(repo, R, tools/mori-source-drift.py)`) and PASS in every run
(`drawn=fresh`, `want_drifted=['S103']`, `flips_ok=True`); the two content checks that the witness
does not forge PASS on the real bytes (`anchors_v2` on the real entry, `capability_v2` on the real
SCORECARD, `live_rows_v2` on the real receipt). Full-projection result lines:

```
witness-token-entry.md         exit=1 failing_checks=[anchors_v2]       C7=unmet
witness-dangling-row.md        exit=1 failing_checks=[capability_v2]    C7=unmet
witness-summary-only-live.txt  exit=1 failing_checks=[live_rows_v2]     C7=unmet
witness-comment-anchors.md     exit=1 failing_checks=[anchors_v2]       C7=unmet
```

## Counter's four negative lines (canonical run, verbatim)

```
negative witness-token-entry        rejected
negative witness-dangling-row       rejected
negative witness-summary-only-live  rejected
negative witness-comment-anchors    rejected
```

Reason agreement. The counter prints no per-witness reason; it prints `ACCEPTED`/`rejected` for the
`all_v2(...)` conjunction (`count-c7.py:536-556`). At a `C7=met` verdict the two real inputs of each
projection are PASS by construction (they are the same five check lines the counter printed), so the
failing conjunct of each `all_v2` is forced to be the check my projection names. The full-projection
runs confirm the same check names through the counter's own `check ... FAIL` lines.

## Witness-specific evidence

- **token-entry**: `anchors_from()` (`count-c7.py:236`) returns `[]` — no line starts with `anchor:`
  (the prose mentions `` `anchor:` `` mid-line only). The backticked tokens `huge_cap`,
  `redirect_private_refused`, `1caa242`, `S221` are not inspected by any v2 check.
- **dangling-row**: `capability_row` selects the single matching row; `paths_in` yields two paths
  (`huge_cap`/`redirect_private_refused` have no extension, so `PATH_RE` skips them).
  `git cat-file -t 13bfba2:evidence/no-such-receipt.txt` → `fatal: path ... does not exist`, rc 128,
  so `object_type` is `None` ≠ `blob`; `tools/mori-source-drift.py` is a `blob`.
- **summary-only-live**: `SUMMARY_RE` matches `rows=225 ... drifted=10`; zero `S### drifted` lines,
  so `named=0 != summary_drifted=10` (the copy rule is not even reached).
- **comment-anchors**: each anchor occurs exactly once in the tool at R, at a comment position —
  line 160 `# bounded read: an untrusted source must not stream past the cap or stall`;
  line 156 `# a redirect actually happened: the new authority must be public`;
  line 54 `FETCH_MAX_BYTES = 4 * 1024 * 1024  # bodies larger than this cannot be classified; read is capped at +1`.
  All three occurrences are after the first `#` on their line, so `code_occurrences`
  (`count-c7.py:245`) returns 0 for each and `not_in_code` lists all three.
- Real anchors are code-position occurrences, so the honest entry passes: line 54
  `FETCH_MAX_BYTES = 4 * 1024 * 1024` (before its `#`), line 158
  `if not _public_redirect_target(final):`, line 208 `return "drifted"`.

## r38 delta (discriminating power of the four)

Projected with the r38 negative block (which includes `resolves`, `/tmp/count-c4-r38.py:324-343`) at
`13f3db7e` (tool blob identical to R: `git diff --stat 13f3db7e..13bfba2 -- tools/mori-source-drift.py`
empty): token-entry rejected (`anchors=0`), dangling-row rejected (`resolves` on the nonexistent
path), summary-only-live rejected (`named=0`) — these three are reused regression pins.
`witness-comment-anchors` is **accepted** by the r38 bytes (substring `check_anchors`, comments
included; real capability+live pass), matching `evidence/c7-red-comment.txt`. So exactly one of the
four flips accepted→rejected between r38 and v2, which is the new discrimination this witness buys.

## Findings

### LOW-1 — `evidence/c7-after.txt` records a run at `f920eaf7`, not the scored tip
`c7-after.txt:1` is `command: python3 .ufo/waves/round-39/count-c7.py f920eaf7 --seed 20261024`,
while the claim's rev is `13bfba2`. Mitigation observed, not assumed: `git diff --stat f920eaf7
13bfba2` is empty over every C7 input (`count-c7.py`, `fixtures/`, `tools/mori-source-drift.py`, the
knowledge entry, `SCORECARD.md`, `drift-live-r37.txt`, `corpus/SOURCES.md`, `corpus/evidence`), and a
fresh run at `13bfba2` reproduces the four `negative` lines, all five `check` lines and `C7=met`
exit 0 byte-for-byte (only the recorded command line and the shell `EXIT=` echo differ). The receipt
is materially reproducible at R; its recorded command simply does not name R.

### LOW-2 — the negative arm reads witness fixtures from the working tree, not from rev R
`count-c7.py:521-531` opens `fixtures/witness-*.{md,txt}` with `open(...)` under
`dirname(__file__)/fixtures`; only the content inputs are read with `show(repo, rev, ...)`. A dirty
worktree could therefore change what "four negatives rejected" tests while the counter still prints
`C7=met` for R. At this tip the worktree fixtures are byte-identical to R
(`git diff --stat 13bfba2 -- .ufo/waves/round-39/fixtures` empty) and match the freeze pins
(`freeze-r39.txt:8-11`: `fc95dc69…`, `bc62b0b3…`, `ce4dac65…`, `8ac9e82b…`), so the observed result
is bound — by the freeze pins, not by the counter.

### LOW-3 (adjacent scope — the clone, not one of my four witnesses) — `c7-red-clone.txt`'s round-39 half is not from the frozen counter
That receipt prints `check drift_kill_v2 FAIL (mutation anchor or table unparsable)`. The string
`unparsable` does not occur anywhere in `count-c7.py` (grep: ABSENT); the only no-anchor branch prints
`mutation anchor absent` (`count-c7.py:513`). The receipt's r38 half is consistent with the r38
bytes; its round-39 half was produced by a pre-freeze build. It does not affect the four `negative`
lines or `C7=met`, but it is cited in C1's evidence list and is not reproducible with frozen bytes.

## Residual risk (within the frozen predicate; not a falsification)

- "Not inside a comment" is implemented as "occurs before the first `#` on its line"
  (`code_occurrences`, `count-c7.py:245-280`). A docstring or string literal on a non-comment line
  counts as code, so a fabricator can park anchors there and satisfy `anchors_v2`. P-C7's words are
  "not inside a comment", so this is inside the predicate; the run-time-drawn `drift_kill_v2` arm is
  the live-work binding, as the contract's disclosed bound states.
- The same rule over-rejects an occurrence after a `#` inside a string literal; no effect here (the
  real entry's anchors are at lines 54, 158, 208, all before any `#`).

## Verification gaps

- Only seed `20261024` was executed. By code reading the seed feeds only `drift_kill_v2`'s `drawn`
  choice (`count-c7.py:486`), so the four `negative` lines are seed-invariant; no second seed run.
- The clone receipt's sandbox commit was not re-derived; LOW-3 rests on the absent detail string,
  not on rebuilding the clone.
- Projections ran only on a `git clone --shared` at R under
  `.ufo/waves/round-39/scratch/RevC7Negatives/` (`project.py`, `project-out.txt`,
  `full-projection.txt`, `full-projection-exits.txt`, `repo-probe/`). No lane file was modified.
- No tool installs or upgrades were performed.

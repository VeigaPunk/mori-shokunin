# DiffLandedFix — full-output differential, tool 7118f320 vs cdfcf66d

- Seat: MoriR29.DiffLandedFix (residual review round 29, attempt 1, counted).
- Lane tip reviewed: cdfcf66d9da2e5598aa844195f85fd74d6379968 (master). Entering tip 7118f320a5ef18d20c1e361eff77db0e1a97b2d6.
- Tools used: `git` (read-only `show`/`rev-parse`/`diff --no-index` in the lane and in scratch), `python3` (subprocess driver), `sed`/`grep` for source inspection. No installs performed; no pacman/uv/npx activity (nothing to record). No external URLs opened.
- Scratch: `/fast/scratch/hyaku/mori-r29/residual/DiffLandedFix/` (driver.py, rows.json, out/, tools/tool-base.py, tools/tool-landed.py, the four case files).

## Method

- Extracted `tools/mori-oom-killers.py` at 7118f320 (base) and cdfcf66d (landed) via `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C <lane> show <rev>:tools/mori-oom-killers.py`.
  - base sha256 `343acaf4b94a1d18f2133b7967ef4078f0605de111a22e803ae36ace77f73d3b` (824 lines).
  - landed sha256 `41464957540fbe3f0855d0a23df4437d0c850a256a4d15f9e76f0b4057e749d7` (857 lines) — identical to the blob recorded in `.ufo/waves/round-29/evidence/c2-fix-selftest.txt:1`.
- Extracted the four case files at cdfcf66d into scratch: `cases.json` (32), `cases-supplementary.json` (32), `cases-a2.json` (30), `cases-a2-r29.json` (24). Input list = every case `inputs` object from all four (118) plus every JSON under `.ufo/waves/round-26/evidence/a2-detectors/` (16) = **134 inputs**.
- For each input ran both tools as `python3 <tool> --inputs <file>` (never live mode), captured stdout/stderr/returncode, parsed stdout JSON, computed structurally-diffed changed paths (dotted, `[i]` for arrays).
- Cross-validation: base `--selftest --cases cases-a2-r29.json` reproduces the documented first-run failure **FAIL 11/24, exit 1** (matches `evidence/c2-freeze-selftest.txt` narrative); landed selftest reproduces `evidence/c2-fix-selftest.txt` **byte-for-byte** (same sha256, same FAIL lines). This confirms the blobs and the reference evidence are the same artifacts.

## Totals

| source | inputs | same | changed |
|---|---|---|---|
| cases.json | 32 | 32 | 0 |
| cases-supplementary.json | 32 | 31 | 1 |
| cases-a2.json | 30 | 27 | 3 |
| cases-a2-r29.json | 24 | 11 | 13 |
| a2-detectors | 16 | 15 | 1 |
| **total** | **134** | **116** | **18** |

Changed fields observed (only these paths differ anywhere): `earlyoom.actions.sigterm`, `earlyoom.actions.sigkill`, `earlyoom.dryrun`, `earlyoom.dryrun_send_lines`, `earlyoom.earlier_invocation_send_lines`, `verdict`. Exit-code mismatches (5) are only the verdict→exit mapping (`EXIT_QUIET=0`, `EXIT_ACTED=1`, `EXIT_UNKNOWN=2`, tool-landed.py:71-79): every rc change accompanies a verdict change. No stderr output on any of the 268 runs.

## Changes outside cases-a2-r29.json (5) — all one field, all explained

All five change only `earlyoom.earlier_invocation_send_lines`; verdict and every other field are identical.

Mechanism: base built `earlier = [e for e in journal if id(e) not in scoped_ids]` (no timestamp filter); landed adds `and _entry_timestamp(e) is not None` (tool-landed.py:327-331), so journal records whose `__MONOTONIC_TIMESTAMP` is non-numeric are no longer counted as earlier-invocation sends. This is the A2-10 rule ("a record without a numeric __MONOTONIC_TIMESTAMP belongs to no known invocation: left uncounted", round-26 contract.md:186-187) applied to the earlier list, matching the landed source comment at tool-landed.py:326-328.

| input | base → landed earlier_send | journal shape |
|---|---|---|
| cases-supplementary/c35-malformed-monotonic-timestamp | 1 → 0 | send stamped `not-a-microsecond-count` |
| cases-a2/a2-10-malformed-action-line-uncounted | 1 → 0 | send stamped `not-a-number` |
| cases-a2/a2-10-positive-evidence-elsewhere-stands | 1 → 0 | escalation stamped `not-a-timestamp` (stamped escalation still counted → ACTED) |
| cases-a2/a2-10-oomd-notices-positive-malformed-records | 2 → 0 | escalations stamped `not-a-number`/`abc`; oomd notices=2 → ACTED |
| a2-detectors/m6-malformed-timestamp | 1 → 0 | send stamped `not-a-microsecond-count` |

The changed field is **unpinned** by every affected expectation: c35 pins no fields; the three cases-a2 cases pin `actions.*`, `scope_complete`, `version`, `dryrun`, `thresholds`, `oomd.*` — not `earlier_invocation_send_lines`. Consequently the landed selftest still passes the frozen cases.json/supplementary/a2 files: **PASS 32/32, 32/32, 30/30, exit 0** (reproduced). No verdict flips here.

## Changes inside cases-a2-r29.json (13)

All 13 are the intended fix effects and are confined to the two rules the fix targets.

A2-07 dry-run segmentation (journal split at each version line; sends in a segment count as real only if that segment did not log `dryrun mode enabled`; tool-landed.py:364-420):

- r29-a2-07-dryrun-inside-scope: QUIET(0) → **ACTED(1)**; `actions.sigkill` 0→1, `dryrun_send_lines` 1→0. Expect ACTED — fixed.
- r29-a2-07-dryrun-then-real-missing-enter: UNKNOWN(2) → **ACTED(1)**; `actions.sigterm` 0→1, `dryrun` true→false, `dryrun_send_lines` 1→0. Expect ACTED — fixed.
- r29-a2-07-real-dryrun-real-missing-enter: UNKNOWN(2) → **ACTED(1)**; `actions.sigkill` 0→1, `dryrun` true→false, `dryrun_send_lines` 2→0, `earlier_send` 0→1. Expect ACTED — fixed.
- r29-a2-07-real-then-dryrun-zero-enter: UNKNOWN(2) → UNKNOWN(2); `dryrun_send_lines` 2→1, `earlier_send` 0→1. Expect dryrun_send_lines=1, earlier_send=1 — fixed (base failed both fields).

A2-10 unbounded/unclocked handling (unbounded scope starts at the last version line; timestamp-less records excluded from scope and from earlier; tool-landed.py:284-310, 327-331):

- r29-a2-10-unbounded-missing-stamp-alone: **ACTED(1) → UNKNOWN(2)**; `actions.sigterm` 1→0. Send has no stamp; excluded everywhere → no positive evidence. Expect UNKNOWN — fixed.
- r29-a2-10-zero-unbounded-mixed-sigterm: ACTED → ACTED; `actions.sigkill` 1→0 (unclocked SIGKILL `not-numeric` excluded; stamped SIGTERM still counted). Expect sigkill=0 — fixed.
- r29-a2-10-zero-unbounded-mixed-sigkill: ACTED → ACTED; `actions.sigterm` 1→0 (unclocked SIGTERM excluded). Expect sigterm=0 — fixed.
- r29-a2-10-unclocked-send-alone: UNKNOWN → UNKNOWN; `earlier_send` 1→0. Expect 0 — fixed.
- r29-a2-10-stamped-send-survives: ACTED → ACTED; `earlier_send` 1→0 (unclocked SIGKILL `clock-unavailable` excluded; stamped SIGTERM in scope). Expect 0 — fixed.
- r29-a2-10-oomd-evidence-survives: ACTED → ACTED; `earlier_send` 1→0 (unclocked send excluded; oomd notices=2 still positive). Expect 0 — fixed.
- r29-a2-10-inactive-lone-missing-stamp: **ACTED(1) → QUIET(0)**; `earlier_send` 1→0 (inactive state, only stamped record is the version line; unclocked send excluded). Expect QUIET — fixed.
- r29-a2-10-failed-stamped-positive: ACTED → ACTED; `earlier_send` 2→1 (unclocked SIGKILL no longer counted; stamped SIGTERM@5200001 still counts as earlier because failed→unavailable has no current-invocation scope). See residual finding R1.
- r29-a2-10-not-found-earlier-stamped-positive: ACTED → ACTED; `earlier_send` 2→1 (unclocked SIGKILL excluded). Expect 1 — fixed.

## KILLER_ACTED flips — flagged

Two inputs changed verdict **from KILLER_ACTED to another verdict**, both in cases-a2-r29.json, both moving *toward* the frozen expectation (base mismatched, landed matches):

1. `r29-a2-10-unbounded-missing-stamp-alone`: ACTED → **KILLERS_UNKNOWN** (expect UNKNOWN, exit 2).
2. `r29-a2-10-inactive-lone-missing-stamp`: ACTED → **KILLERS_QUIET** (expect QUIET, exit 0).

These are intended corrections, not regressions. **Zero** KILLER_ACTED→other flips occur outside cases-a2-r29.json (the five outside changes keep verdicts identical). No verdict flips in the reverse direction anywhere.

## Residual finding R1 — landed selftest still fails the frozen r29 file

Reproduced `python3 tools/tool-landed.py --selftest --cases cases-a2-r29.json` → **FAIL 21/24, exit 1** — identical to `evidence/c2-fix-selftest.txt:12-26`. The 21 failing checks are all on three cases, all field-level (verdict+exit match on all 24):

- r29-a2-10-inactive-lone-missing-stamp (4): `dryrun_send_lines` got null expected 0; `process_group_lines` got null expected 0; `version` got null expected "1.9.0"; `grammar` got "unverified" expected "verified-1.9.0".
- r29-a2-10-failed-stamped-positive (5): same four null-fields + `earlier_invocation_send_lines` got 1 expected 0.
- r29-a2-10-not-found-earlier-stamped-positive (4): same four null-fields (`earlier_invocation_send_lines` got 1 expected 1 — passes).

These failures are **pre-existing** (the base selftest fails exactly the same null-fields on the same three cases; base selftest lines for inactive-lone-missing-stamp/failed-stamped-positive/not-found-earlier-stamped-positive). The expectations demand journal-derived values (`version`, `grammar`, `dryrun_send_lines=0`, `process_group_lines=0`) for *non-active* earlyoom states (inactive/failed/not-found), but the tool deliberately emits `version:null`/`grammar:"unverified"`/null counters whenever the unit is not active (scoped is only built when `earlyoom_state == "active"`, tool-landed.py:266-272); for `failed-stamped-positive` the expectation of `earlier_send=0` also conflicts with the tool's model that a non-active unit has no current-invocation scope, so every stamped send is an earlier send (tool-landed.py:315-323).

Gate impact: `count-c2.sh` (`.ufo/waves/round-29/count-c2.sh`) requires `a2_r29_selftest` exactly `PASS 24/24` (count-c2.sh: `valid = ... new_test == "PASS %d/%d" % (n,n)`); with the landed tool this emits FAIL, so **C2=unmet** at cdfcf66d until either the three case expectations are amended (case-file change; L1-owned) or the tool is extended to populate version/grammar/counters for non-active states and to give `failed-stamped-positive` a zero earlier-send count. Verdict/exit are unaffected (all 24 pass), so the mismatch is purely field-level on unpinned-by-verdict diagnostics — but the selftest still treats them as case failures.

## Verification gaps

- No IDE/lsp server is available in this environment; source reading used `sed`/`grep` on the extracted blobs only. All behavioral claims come from executed `--inputs`/`--selftest` runs (268 + 8), not from static reading.
- The contract-vs-expectation question behind R1 (should a non-active earlyoom report journal-derived version/grammar and a zero earlier-send for stamped entries?) is an adjudication for the L1/Main; this review only reports the observable status.
- Live-mode operation was not exercised (forbidden by bounds). Determinism: every disputed result was reproduced by two independent runs (--inputs differential and --selftest, plus the evidence files).

# NoHarm — round22 falsification: carried debt vs current production/docs

Seat `MoriR22.NoHarm` (critic, read-only, leaf). Static analysis only. I executed no tool, test, oracle, fixture builder, gate, build, formatter or measurement. I dispatched nothing, edited no production file, and installed or updated no tools.

Effective semantics come from `denominator-correction.md`, which I read first, plus `frozen/requirements-v2.json` (24 IDs) and `oracle-reconcile-v2.py`. `contract.md` (v1) is retained evidence only.

Audited at HEAD `94b9014`. The worktree has no tracked modifications; the untracked files are `.scratch/`, `evidence/measure1/synthetic-workspaces.tar.gz`, wave2 json files, and falsify reports. The shipping tool's sha256 is `d6870fb6…0ce7`. That equals `summary.json` `tool_sha256` measured at `4f7cfce`, and `git diff --stat 4f7cfce HEAD -- tools/` is empty.

## Verdict

**There is no misleading closure of the three carried debts.** Every round22 production or doc surface keeps all three debts open:

- the four retention hits
- original permission control RED 11/12
- two unknown dispositions, with baseline/pin blocked

`privacy_clearance` cannot be anything but `false` on any tool path. I found one calibration-label defect that the canonical judge has to weigh, because fixing it needs a re-freeze. I also found three smaller provenance-wording defects and one forward risk.

## Carried-debt preservation (verified against current bytes)

| Debt | Production/evidence | Docs at HEAD |
|---|---|---|
| Four unallowlisted retention hits | `measure1/current-retention-floor.json`: gate at `4f7cfce`, exit 1, `RETENTION_FINDINGS`, metric 4, hits 95, allowlisted 86, non_author 5. All 4 hits are the round-20 nested policy copy (`.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json` lines 8/11/12/14, classes R2/R5/R6/R8). `summary.retention_floor`: new 0, missing 0, same identities true. `real-reconciliation.json`: raw 95, policy_excluded 5 (non-author globs: three `round-17-verifier-spotcheck.md` hits, two `round-18-verifier-spotcheck.md` hits), scanner 90, unallowlisted 4, `retention_state` red, `receipt_match` true. | Four unallowlisted hits / 95-5-90 split stated in SKILL, SCORECARD, LOG, corpus/README, lesson and knowledge note. No allowlist, policy or history edit. |
| Hits after `4f7cfce` | `94b9014` adds only measure1 evidence. A static PCRE count of all nine frozen classes found 0 matching lines over `.ufo/waves/round-22/**` (tracked and untracked, including current falsify reports), the nine round22 doc files, the tool, and `.scratch/**` (with `-uu`). [INFERENCE] PCRE `\b`/`\s` is ASCII and Python `re` is Unicode, so this emulates the gate rather than running it. | — |
| Original permission control RED 11/12 | `.ufo/waves/round-21/evidence/final/fixture-original-control.json` stdout: case_count 12, passed 11, failed 1, status fail, exit 1. Byte-unchanged since `77a5bbe` (no diff on `.ufo/waves/round-21/`; summary `unchanged` true). | Stated as red in SKILL, SCORECARD, LOG, README, lesson, knowledge note and QUALITY 70. |
| Two unknown dispositions; baseline/pin blocked | `corpus/evidence/loss-accounting-r21.json`: 2 observations (`aggregator-r10`, `aggregator-r10-resume`), state `unresolved`, `independent_disposition` null. Byte-unchanged. `baseline-r20-…json`, `mori-census.sh`, `mori-evidence-loss.py` and `mori-retention-gate.py` are also unchanged. `git diff --stat 77a5bbe HEAD -- tools/ corpus/evidence/` shows only the added reconciler. | SKILL ("baseline acceptance blocked"), LOG ("baseline-blocking"), README ("not accepted or re-pinned"), lesson, PROVINCE ("cannot authorize baseline acceptance … reap … dispatch"). |
| No clearance path in the tool | `'privacy_clearance':False` is a literal in the check result (line 225), the setup branches (272/274) and the selftest result (261). `receipt_authenticity:'unattested'`. Population receipts are refused as `unsupported_population_receipt` (line 194), so no inferred "0 new" green. | — |

## Counterexamples

### NH1 — `raw_unallowlisted` reports the scanner population, so raw-population unallowlisted exposure is understated by 5 (calibration; depth)

This is a tradeoff for the judge: the frozen v2 oracle pins the alias, so fixing the field needs a re-freeze.

**Code.** `unallowed` is built from `scanner` only (line 207). Both `raw_unallowlisted` and `scanner_unallowlisted` are `len(unallowed)` (line 222).

**Strongest counterexample, from retained identity-derived counts.** From `real-reconciliation.json`: `allowlisted` 86 is computed over all hits (line 206), scanner 90, scanner-unallowlisted 4. So the allowlisted hits inside the scanner population number 90 − 4 = 86. That is all of them, which means none of the 5 non-author identities is allowlisted. The raw population of 95 therefore contains 4 + 5 = **9** identities that are not allowlisted, yet the field named `raw_unallowlisted` reads **4**.

**Synthetic case.** In `fixture-builder-v2.py`, allowlist rows cover only `policy.json` and `allowed.txt`, so `non-author.txt` is unallowlisted. Raw non-allowlisted identities are 2, but `oracle-reconcile-v2.py` R12 freezes `raw_unallowlisted==1`, and R02/R11 freeze it the same way. `frozen/expected-real.json` (committed with the SUT in `8cb4afb`) freezes 4.

**Impact.** The four-hit debt is not closed. It is preserved exactly, and the raw identity list `raw_hits` stays authoritative. But a consumer reading only the scalars sees `raw_total` 95 next to `raw_unallowlisted` 4. That reads as if all raw-population privacy-class hits except four are allowlisted, while 5 unallowlisted hits on non-author paths remain in the tree. The contract ("raw denominator remains authoritative") and the correction ("preserve raw authoritative lists") imply the `raw_` prefix means the raw population. The alias is disclosed only in `corpus/knowledge/retention-reconciliation-r22.md:27-31`. It is not disclosed in the SKILL registry row, the operator entry point, nor in PROVINCE or the lesson. Before round22 there was no such field, so this is a new misleading label, not a regression.

**Smallest safe correction.**
- **In-round, no re-freeze:** add one sentence to the SKILL.md round22 row prose and the lesson's M1 paragraph: "`raw_unallowlisted`/`scanner_unallowlisted` both name the gate's non-author-filtered metric; raw non-allowlisted exposure is `raw_hits` minus allowlisted identities (9 at the r21 receipt, 5 of them non-author-owned)."
- **Field semantics:** any change (for example a distinct identity-derived `raw_non_allowlisted` list and count) needs a v3 freeze of R02/R11/R12 and expected-real. Silently changing the field would break the frozen24 oracle. That decision belongs to the judge, not to this round's integration.

### NH2 — the knowledge note's `verified-at` header points at result records that do not exist (freshness; calibration)

This is fixable.

`corpus/knowledge/retention-reconciliation-r22.md:2` says "exercised results and measured tool revision are recorded in the round22 report and SCORECARD". At HEAD:
- No round22 report file exists under `.ufo/waves/round-22/`.
- The SCORECARD round22 section still says "This is a declaration, not an exercised capability row or a result. Actual counting commands, measured commit and verdict follow integration."
- LOG has no entry for the measure1 commit `94b9014`.

Round21 had a "Round21 exercised outcomes — measured …" section (SCORECARD line 1312). This is under-claiming with a dangling provenance pointer, not over-claiming.

**Correction:** L1 either appends a SCORECARD/LOG "Round22 exercised outcomes — measured `4f7cfce`" entry citing `evidence/measure1/summary.json` (keeping the three carried debts open in that row), or rewords line 2 to cite `evidence/measure1/summary.json` directly. Either way, it must not imply the result rows already exist.

### NH3 — the carried-debt fields in `summary.json` are literals that look like measurements (calibration)

This is low severity and fixable for the next measurement.

`measure-round22.py` writes `'original_permission_control':'RED11/12 retained byte-unchanged, not rerun'` and `'historical_dispositions':'two unknown; baseline blocked'` as constant strings. The grounding is indirect. `all_claim_checks_pass` requires both underlying files to be byte-unchanged since `77a5bbe`, and I verified their bytes carry 11/12-fail and 2×unresolved/null. So the values are true today. But the strings are not parsed from evidence, and "baseline blocked" is procedural: SKILL r21 says the raw `--pin` write path is not intercepted.

**Correction (next measure only; measure1 stays append-only):** derive `passed`/`failed`/`case_count` and the per-observation `state`/`independent_disposition` from the bytes, or rename the fields `asserted_carried_*`.

### NH4 — real-data expectations are called "frozen" but were committed with the SUT (calibration)

This is low severity and a wording fix.

`frozen/expected-real.json` first appears in `8cb4afb`, the same commit that adds `tools/mori-retention-reconcile.py`. The summary key `real_matches_frozen_expected` and SCORECARD's "Expected real input digests and values are frozen in …" therefore describe same-commit, author-side expectations, not pre-implementation ones. `measure1-identity-check.json` is honestly labelled "co-evolved", and the 24 v2 requirements did precede the implementation (`e2f549b` before `8cb4afb`).

**Correction:** the exercised-outcome row (NH2) should say "co-committed with implementation", not "frozen".

### NH5 — committing `.scratch` or probe output could recreate the original defect (adjacency; forward risk, not a current defect)

The four retained unallowlisted hits are themselves a committed falsify-run probe copy under `round-20/falsify/NoHarmRun/rg/`.

At HEAD, `.scratch/` is untracked and not ignored. `.gitignore` lists only `.ufo/interactive-sessions/` and `.ufo/worktrees/`. `.scratch/` holds 135 nested synthetic `.git` directories. Today it has 0 frozen-class matches.

**Correction:** L1 stages explicit paths only at integration (no `--all`). Before committing the pending falsify reports, re-run the retention floor at the integration commit; the expected result is the same 4 identities and 0 new.

## Prior build-wave notes re-verified against current shipping source

These re-checks were against current source, not repeated from the earlier notes:

- **CX1 path substitution:** fixed. Recorded `--policy`/`--allowlist` are bound to the receipt argv (lines 172-182, `receipt_path_binding`).
- **CX2 fixture `rule`:** fixed. `fixture-builder-v2.py:59` sets `rule`, and `allow_rows` requires the exact gate row shape (line 109).
- **CX3 real-data run:** exercised and retained. Its 4/91 expectation was the superseded source-file reading; the effective value is 95/5/90/4.
- **CX4 wrapper revision:** fixed (lines 183-186). `contradictory-entering-receipt.json` exits 2 with `receipt_revision_conflict`.
- **Gate parity:**
  - dict `rows` accepted (line 105)
  - allowlisted computed over all hits, unallowlisted over the scanner population (206-207)
  - finding precedence preserved (210)
  - stale-only gives exit 0, matching gate line 288
  - mode-120000 symlink blobs scanned, gitlinks skipped (`kind!=b'blob'`)
  - multiset comparison
  - missing `--allowlist` is a setup error via `recorded_option`

## Impacted axes

- **Calibration:** NH1, NH2, NH3, NH4
- **Depth:** NH1
- **Freshness:** NH2
- **Adjacency:** NH5 (forward risk)
- **Coverage and operability:** no harm found. The only tools change is the added file, and the gate, census and evidence-loss tools are byte-unchanged.

## Not checked

- I did not run the reconciler, the gate or the selftest. All observed outcomes cited are retained measure1 receipts.
- I did not verify the "18 refinement controls" count or the per-arm refinement outcomes.
- The four-hit floor at HEAD `94b9014` and later is an emulated static count, not a gate run.

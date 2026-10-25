# ScoutConsiderthese — suggestions sweep (round 48, wave 1)

Read-only review of all seven `considerthese/2026-10-19.md` through `2026-10-25.md` files, `corpus/QUALITY.md`, `tools/`, and `LOG.md`. I did not modify production files or run lane tools. States below distinguish an implemented artifact/criterion from a proposal that merely resembles or is discussed by later work.

## Sweep commands and observations

Commands run from `/home/vgpnk/Projects/shokunin/mori-shokunin`:

```sh
grep -n 'considerthese' corpus/QUALITY.md
grep -niE 'portab|portability|host-path|/home/vgpnk' corpus/QUALITY.md
grep -niE 'portab|off-host|offhost|/home/vgpnk' LOG.md
grep -rlE '/home/vgpnk' tools/ | sort
git ls-files | grep -E '^\.ufo/waves/round-4[0-3]/[^/]+\.(py|sh)$' |
  while read f; do grep -qE '/home/vgpnk' "$f" && echo "$f"; done
git ls-files 'tools/*.py' 'tools/*.sh' |
  while read f; do grep -qE '/home/vgpnk' "$f" && echo "$f"; done
```

Observed: tools list is 3 (`mori-blind-check.sh`, `mori-misroot-sweep.py`, `mori-round17-context-check.py`); top-level `.py`/`.sh` under rounds 40–43 list is 10; combined count is 13. This reproduces the reflection's count under that scope. The scope matters: a broader all-round top-level sweep yields 53, and all committed `.py`/`.sh` under `.ufo/waves/` (any depth) yields 393. So the count needs the explicit round and path-depth rule; 13 is not a general whole-history inventory.

## Suggestion inventory

“Implemented” means evidence of the proposed mechanism, not just a nearby lesson/tool. “Partial” means a narrower criterion or one-off instance exists, while the stated recurring/general practice does not. `Unimplemented` means no supporting artifact was located in the requested `QUALITY.md`, `tools/`, or `LOG.md` sweep; this is not a claim that no narrative mention exists anywhere.

| Date / # | Suggestion (condensed) | State and evidence |
|---|---|---|
| 2026-10-19 #1 | Verify cited paths, SHAs, and counts in SKILL/LOG at HEAD | **Partial** — `tools/mori-pin-check.py`, QUALITY 123 checks registry pins in SKILL; no general SKILL+LOG citation sweep found. |
| 2026-10-19 #2 | Re-run selftests and silence cases in a clone, compare counts | **Partial** — `tools/mori-silence-cases.sh` has `--selftest`, and registry audit exists; no daily all-selftests clone runner found. |
| 2026-10-19 #3 | Report EDQUOT blind spot; suggest read-only journal-count signal | **Unimplemented as proposed** — FR2 is described in `corpus/README.md`; r23 quota prototype was withdrawn (round-23 lesson/spot-check). No quota tool in `tools/`. Round-48 C2's quota knowledge entry is adjacent, not the requested read-only signal or recurring report. |
| 2026-10-19 #4 | Keep drift-result / axis-score timeline | **Unimplemented** — no corresponding timeline artifact or tool found. |
| 2026-10-19 #5 | Review drift pin's masked-field list | **Unverified / likely unimplemented** — no masking field references found in `tools/mori-source-drift.py`; no review artifact found in the requested sweep. |
| 2026-10-19 #6 | Track standing items (PR, promotion hold, saturation) | **Partial** — carried-debt prose in `LOG.md`; promotion 0/4 is recorded in `SCORECARD.md`; no single standing-items ledger found. |
| 2026-10-20 #1 | Do a no-harm diff each round | **Partial** — `tools/mori-round14-regressions.py` discusses historical no-harm; no recurring general no-harm diff tool found. |
| 2026-10-20 #2 | Run each round's regression gate; rerun old gates at HEAD when census changes | **Partial** — per-round regression tools exist (e.g. `tools/mori-round13-regressions.py` through `mori-round19-regressions.py`); no general changed-census replay runner found. |
| 2026-10-20 #3 | Track author vs outside verdicts | **Unimplemented as a structured tracker** — individual verifier spot-check lessons exist; no aggregate tracker found. |
| 2026-10-20 #4 | Count seat-process violations per round | **Unimplemented** — no per-round violation counter found in tools/QUALITY/LOG sweep. |
| 2026-10-20 #5 | Age carried debts | **Partial** — `LOG.md` repeatedly records “Carried debt”; no age/trend counter found. |
| 2026-10-21 #1 | Run retention gate and content review on each day's commits | **Partial** — `tools/mori-retention-gate.py` and `tools/mori-content-review.py` exist; no daily runner/receipt found. |
| 2026-10-21 #2 | One selftest runner and one scratch contract | **Unimplemented** — no unified runner found. |
| 2026-10-21 #3 | Track evidence growth per round | **Partial** — related proposal admitted as QUALITY 122, but that row explicitly says its narrower census is not built. |
| 2026-10-21 #4 | Track closure lag | **Unimplemented** — no closure-lag ledger/tool found. |
| 2026-10-21 #5 | Carry open disputes to a ruling | **Partial** — disputes and rulings are documented in lessons (e.g. round-20 M6, round-21 correction); no general carry-forward tracker found. |
| 2026-10-22 #1 | Re-run each committed selftest output at its named revision | **Partial** — `tools/mori-routed-r24.py --rerun` implements a narrower routed receipt re-run (QUALITY 76 / round-25 work), not every selftest output. |
| 2026-10-22 #2 | Keep an awaiting-closure ledger | **Unimplemented** — no ledger found. |
| 2026-10-22 #3 | Track mutation survivors as coverage debt | **Partial** — QUALITY 114 records a cumulative survivor-ledger criterion; the round-44 ScoutConsider report says the cumulative-ledger artifact/re-run is still unimplemented. |
| 2026-10-22 #4 | Compare dispatch times with commit times | **Unimplemented / unverified** — `tools/mori-dispatch-ledger.py` binds dispatch payload identities; no evidence found that it compares dispatch timestamps to commit timestamps. |
| 2026-10-23 #1 | Warn early when pre-data controls meet | **Partial** — pre-data controls are used in round gates and cited in later lessons; no general review-time checker found. |
| 2026-10-23 #2 | Re-run every OOM-killer fixture set daily | **Partial** — `tools/mori-oom-killers.py` has committed fixtures/selftest; no daily runner across all fixture sets found. |
| 2026-10-23 #3 | Keep a structured verdict table | **Unimplemented as a common tracker** — verdict tables occur in individual reports, not an aggregate table. |
| 2026-10-23 #4 | List tools without selftests | **Implemented** — `tools/mori-gate-registry.py --audit-all` reports `no_selftest`; QUALITY 120 describes the population audit. |
| 2026-10-23 #5 | Write per-round digest when volume is high | **Unimplemented** — no dedicated digest artifact/tool found. |
| 2026-10-24 #1 | Check frozen instruments replay off-host | **Implemented as criterion** — QUALITY 115; round-43 `count-c1s.py` replay uses a scratch clone. Not a daily sweep of all instruments. |
| 2026-10-24 #2 | Keep cumulative survivor ledger | **Partial** — QUALITY 114 admits the practice/check; round-44 ScoutConsider records no cumulative replay artifact. |
| 2026-10-24 #3 | Watch repository growth from scratch output | **Partial** — QUALITY 122 admits the criterion but says the narrow census is not built. |
| 2026-10-24 #4 | Reproduce headline numbers mechanically | **Implemented in bounded form** — QUALITY 117's round-44 figures ledger and counter; not all future headline counts. |
| 2026-10-25 #1 | Add registry pin check to daily review | **Implemented** — `tools/mori-pin-check.py`, QUALITY 123, round 47. The daily recurring use itself is not established by this artifact. |
| 2026-10-25 #2 | Track host-path portability count | **Unimplemented at entering tip; selected for round 48** — the 13 count reproduces only with the stated r40–r43/top-level + tools scope. |
| 2026-10-25 #3 | Track whether critic flags get fixed | **Unimplemented** — no flagged-versus-fixed tracker found. |
| 2026-10-25 #4 | Track where suggestions end up | **Partial** — recurring ScoutConsider reports and LOG/QUALITY mining citations provide examples; no cumulative suggestion-to-outcome ledger found. |
| 2026-10-25 #5 | Track retries | **Unimplemented** — no retry event ledger/tool found; the r45 retry appears as narrative in the reflection. |

## Choice and next proposal

I **agree** with the L1's choice of 2026-10-25 suggestion 2: it is lane-relevant (instrument portability affects whether observability evidence can be reproduced off-host) and cheap to measure from committed bytes. The criterion should freeze exactly the scope, file types, and path depth; otherwise the reported 13 is not comparable. Suggested command form is the two pipelines above, with an explicit r40–r43 range for the historical baseline and an explicit `tools/*.py`/`tools/*.sh` population.

For the next unimplemented proposal, I recommend 2026-10-24 suggestion 3 / QUALITY 122: build the already-specified report-only census of tracked scratch outputs and uncited receipts. It is the strongest cheap, observability-lane fit among remaining work: QUALITY 122 already describes the narrow receipt population and a two-revision check, while explicitly noting that its instrument is absent. This is a clearer, cheaper next step than semantically judging whether each critic flag was fixed. A closer next item from 2026-10-25 specifically would be suggestion 3 (critic-flag fixed-vs-unfixed count), but its mapping requires more judgment.

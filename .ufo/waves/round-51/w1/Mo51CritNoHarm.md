# Mo51CritNoHarm — no-harm audit, round 51 wave w1

Seat: Mo51CritNoHarm (critic). Scope: diff `aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd..87e0c374537557754bf71dd68036ded3ddc6699c` (30 files, +7733/−33), read every changed tracked file, and re-measure independently. Mel hosts read-only. All builds under `/fast/scratch/hyaku/mori-r51/Mo51CritNoHarm/` with `TMPDIR=<scratch>/tmp`; the lane repo was only read.

## What changed (data commit 87e0c374)

- C1: `tools/mori-pin-check.py` v5 (export is `git clone --shared` under `--scratch`/TMPDIR, never `<repo>/.scratch`; mismatch lines carry `class=env|stale`; summary ends `env=N stale=N`; selftest 114→119); `.ufo/waves/round-40/conform.py` (LANE derived from own path; selftest scratch under TMPDIR); `SKILL.md:938` r47 row + `SHONEN.md` pins → 119/119 + round-51 receipts.
- C2: `corpus/knowledge/memavailable-estimate-r51.md`; `corpus/SOURCES.md` rows S492–S496; five copies under `corpus/evidence/sources-r51/`.
- Frozen (4677910e): contract, counters, `controls/c1-controls.py`, witness copies, control receipts, census-start, sweep, selectftest-c2. `evidence/freeze-sha256.txt` has 21 entries.

## Independent re-measurement (all rc shown)

1. `python3 .ufo/waves/round-51/count-c1.py 87e0c374537557754bf71dd68036ded3ddc6699c --scratch <scratch>/c1run` → `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 rev=87e0c3… failed=-` rc=0 — byte-identical to `evidence/c1-at-data.txt`.
2. `python3 .ufo/waves/round-51/count-c2.py 87e0c374537557754bf71dd68036ded3ddc6699c` → `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=87e0c3… failed=entailment` rc=1 — identical to `evidence/c2-at-data.txt`; the only open arm is the missing wave entailment judgment (expected pre-vote).
3. `count-c2.py --hashes 87e0c3…` vs `evidence/c2-hashes-at-data.txt` → sorted diff IDENTICAL (21 row hashes).
4. `python3 tools/mori-pin-check.py --selftest` (working tree at run time) → `PIN_CHECK_SELFTEST pass=119 fail=0` rc=0 (the data-commit v5 tool; later superseded in the work tree, see finding F1).
5. `python3 tools/mori-unlanded-check.py --selftest` → `UNLANDED_SELFTEST pass=17 fail=0` rc=0.
6. `python3 .ufo/waves/round-40/conform.py 87e0c374537557754bf71dd68036ded3ddc6699c --selftest` → `CONFORM_SELFTEST pass=11 fail=0` rc=0 (round-40 gate tally unchanged by the LANE fix).
7. Production-style closure shape: `python3 tools/mori-pin-check.py --rev 87e0c374537557754bf71dd68036ded3ddc6699c --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch <scratch>/pc-run` → `PIN_CHECK=met tally_pins=35 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=87e0c3… baseline=no env=0 stale=0` rc=0 — all 35 standing registry pins match under v5, including the git-reading instruments (round-49 counter, unlanded check).
8. Round-49 junk-variant counter against the live v5 tool and the real registry at master: `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=b504cb17…` rc=0 — v5 flips no previous instrument verdict.
9. Detached-source shared-clone reproduction: `git clone --shared --no-checkout <lane> dhclone; git -C dhclone checkout --detach 87e0c3…` → local `master` exists (origin/HEAD resolves; points at b504cb17), so `master`-reading instruments resolve inside a v5 measured tree.
10. `sha256sum -c evidence/freeze-sha256.txt` → all 21 listed bytes OK.
11. Quote/anchors spot-checked in the committed copies: `show_mem.c` `si_mem_available()` lines 23/32–73, `meminfo.c` lines 27–31/48–51/56/61–64/105, `mm_inline.h` lines 13–31, patch hunks for `fs/proc/meminfo.c`, and every row quote found verbatim (whitespace collapsed) in its copy; reading-rule row references (4,7,17,20/19,20) match the table.

## Axis verdicts

- **coverage — not harmed.** Both claim surfaces land with their frozen counters; S492–S496 continue the registry after S491 with no id collision; S492's shared URL/bytes with S082/S168 is disclosed (W04 warning per contract). No claim/routed defect dropped from the contract.
- **operability — not harmed.** Tools run at the data rev (items 1,2,4–8); the closure-style pin-check leaves 0 residue in the repo it reads (item 7); the kill arm measured 0 residue (item 1).
- **depth — not harmed.** Entry opens with `source:`/`verified-at:`/`recheck:`; 21 rows, 21 located quotes, 5 sources drawn on; copies match frozen sha256; anchors verified (item 11).
- **freshness — not harmed (F1/F2, see Findings).** SHONEN pins 119/119 matched the v5 tool and receipts at the data commit; QUALITY/README contain no stale "114" for the current tool (remaining "114" hits are historical reports/lessons).
- **calibration — not harmed.** No other instrument verdict changed: round-40 conform selftest still 11/0 (item 6), v5 passes the round-49 junk-variant counter on the real registry (item 8), round-50 counters' pins matched in item 7, unlanded check unchanged 17/17.
- **adjacency — not harmed.** The data commit touches only mori-shokunin paths inside the two claim surfaces; nothing at the fleet root or in sibling lanes; witness/controls confined to scratch clones; freeze bytes verified (item 10).

## Findings

- **F1 — MED — uncommitted post-data drift in the lane (freshness/coordination).** The working tree now differs from the data commit in tracked files that the wave reports on: `tools/mori-pin-check.py` carries v5.1 (selftest 119→125; absent-instrument and two-tallies are stale; timeout keeps pre-timeout output; measured-tree `master` set to REV; default scratch `$TMPDIR` else `/var/tmp`; explicit `--scratch` inside the repo refused), with `SKILL.md` (+76), `corpus/QUALITY.md` (+102), `corpus/README.md` (+24), `SHONEN.md` (125/125), both selftest receipts regenerated (`PIN_CHECK_SELFTEST pass=125 fail=0`), and `corpus/knowledge/memavailable-estimate-r51.md` reworded (claim text changed ⇒ row hashes change). The frozen counters still measure rev 87e0c374 (v5, hashes as in `c2-hashes-at-data.txt`), so the claim record is unaffected; but if v5.1/entry-V2 land as the final tip, C1/C2 must be re-scored there (same counters) and entailment votes must target the new hashes. Verified: v5.1 selftest `pass=125 fail=0` rc=0; v5.1 production-style run reported at the end of this file.
- **F2 — MED — conform selftest residue left in the lane.** `.ufo/waves/round-40/scratch/mori-conform-selftest-{858cf_2r,y5k7kzyi}/` (19:53–19:54 on 2026-10-26) contain mutated `counter-*.py` fixtures — outputs of a round-40 `conform.py --selftest` whose SCRATCH_ROOT was the OLD hardcoded lane path (the pre-fix form). The current fixed conform.py does not produce them (item 6 replication left none). This is exactly the residue class C1 targets; the dirs are untracked and outside every measured path, but should be removed by the L1.
- **F3 — LOW (calibration, docstring) — `count-c1.py:77-79` says the fresh clone's `master` at R is "the lane's own state when R is its tip"; the lane's HEAD is detached (jj) and `master` exists only via `origin/HEAD` resolution.** The counter fabricates `master` (matching how the pinned instruments expect the tree), so this is a wording overstatement, not a measurement error; v5.1's `export_rev` now also sets `master`=REV, which is the stronger fidelity.
- **F4 — LOW (operability) — v5 default scratch honored `$TMPDIR` even when inside the read repo; v5.1 refuses/skips that.** No frozen or wave invocation we observed used such a TMPDIR (all passed external `--scratch`/TMPDIR), so no observed impact at 87e0c374.
- **F5 — LOW (documentation) — `controls/witness/conform.py` is byte-identical to the landed round-40 conform.py, while `controls/witness/mori-pin-check.py` is the pre-v5.1 witness.** Disclosed as feasibility-only; no impact on the claim's landing.

UNVERIFIED: whether any hosted run actually produced F2's dirs (two plausible sources: an entering-rev pin run of the SKILL r40 row, or a pre-fix conform invocation at 19:53–19:54); the dirs' timestamps match wave activity, and the current tool does not reproduce them.
## Addendum — v5.1 work-tree verification (after F1 was observed)

`python3 tools/mori-pin-check.py --selftest` (work tree, v5.1) → `PIN_CHECK_SELFTEST pass=125 fail=0` rc=0, matching the regenerated receipt and SHONEN's 125/125.
`python3 tools/mori-pin-check.py --rev 87e0c374537557754bf71dd68036ded3ddc6699c --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch <scratch>/pc51` (v5.1) → `PIN_CHECK=met tally_pins=35 digest_pins=8 mismatches=0 … env=0 stale=0 rev=87e0c3…` rc=0.
So whichever tip lands (87e0c374/v5 or the v5.1 work tree), the frozen C1 arms' operational shape holds; only the selftest count changes (119 vs 125, both ≥ 114).
## Addendum — integration commit 7c0b6232 (landed while this seat ran)

The L1's integration commit `7c0b6232` (wave w1 integration part 1) landed mid-wave: it commits pin-check v5.1 and the reworded entry (rows 6/12/14/15 replaced by the voters' entailed text), plus the w1 reports so far. At that rev the frozen counter now reads `C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=21 dissent=0` rc=0. This confirms F1's coordination point: the claim record moved from 87e0c374 (v5, entry V1) to the integrated tip; the frozen counters are unchanged and give C1=met / C2=met at the integrated tip (C1 arms re-verified under v5.1 in the addendum above).

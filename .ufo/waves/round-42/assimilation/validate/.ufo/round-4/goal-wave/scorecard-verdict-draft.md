# Round 4 verdict — integration draft (scribe seat, goal wave)

Integration target: append as a `## Round 4 verdict — 2026-10-15 (goal wave)` section in
`SCORECARD.md` (parent-owned; append-only — the round-3 section `SCORECARD.md:133-192` and
everything above it stay untouched). Verdict vocabulary only (`improved` / `harmed` /
`unchanged` / `unprovable-but-better`); no scalar scores. Every figure below is bound to a
landed artifact at a cited path; `[PARENT: …]` marks values only the integration commit,
the parent's acceptance re-run, or another seat's ownership can bind.

- Evidence commit: `[PARENT: wave integration commit hash under the mori identity]`
- Lane baseline entering the wave: `bbcc1ad` (round-3 records; `1439c47` evidence)
- Round-count claim: `[PARENT: verified-round accounting 3 → 4 on admission]`
- Draft status: **v3 2026-10-15T17:53Z** by the scribe seat. After-side values bound to
  the landed revisions — oracle sha256
  `be0e28b8bf3cc34e2a35e6cea7c05bffff376111b42d985b6bec7f0e21f59456`, census sha256
  `af2d4e79e69b70bb0b5aecd6acc9608fc7c16b0716766d4a60310e0689d350d7` (`VERSION=census-r3`,
  `:61`) — via the receipt set
  `corpus/evidence/verdict-r4-20261015T173551Z-{selftest,oracle,canary227,sniffer-v2,live}.log`
  (`corpus/evidence/README.md` round-4 index), the verdict note
  `corpus/knowledge/verdict-machine-r4.md` (sha256 `aab4b62c35e4b01606bda9b10877cc7ce7122ac3c21c589e16cf2dedaf58e28e`,
  landed 17:47Z), and this seat's own sha-verified probes (`/tmp` scratch, noted where
  used). v1/v2 predated the note; **v3 carries the note's §2.4 residual** (a
  self-consistent order-replay attacker still fakes a full pass) into the affected rows.

## Round 4 verdict

Round scope (the registered round-3 debt, `SCORECARD.md:185-191`): one operability move —
make the verdict machine trustworthy end-to-end. Four registered defects, each with a
falsifiable before-state measured against the round-3 SHAs:

- **(a) frozen-oracle matcher** — `case "$obs" in $want)` took an expansion-introduced `|`
  literally (`tools/mori-silence-cases.sh:362-365` at `505a7504…`), capping the tally at
  `25/27` with the observed states inside the intended want-sets (cases
  `ledger-missing-not-silent` `:455`, `report-future-no-close` `:613`).
- **(b) oracle fixture-signal leak** — case id in the fixture path (`:149`), `MORI_FIXTURE=1`
  always exported (`:269`), `MORI_SHOKUNIN_ROOT=$CASE_ROOT` (`:270`; full leak list in
  `corpus/lessons/2026-10-15-forgeable-oracle-visible-fixtures.md:19-24` and
  `verdict-machine-r4.md` §2.1); a no-logic case-id-sniffer census scored
  `matched=27 total=27` exit 0 against the frozen oracle (round-3 falsifier m4b;
  re-verified this session — scribe sniffer-v1: identical result).
- **(c) census `:225-228`** — `state_n=$(find "$STATE_DIR" … | wc -l | tr -d ' ')` (`:227`)
  bare pipeline aborted the whole census (rc 1, header only, 0 verdicts) on an unreadable
  `.ufo/state`.
- **(d) close tracking `:611-616`/`:624`** — the last close line anywhere (any round) won,
  so `complete r7; complete r5` misgraded a closed r7 anchor as silent (critic defect 1;
  latent — not producible from the current writer).

**Before** (measured at the round-3 SHAs; scribe probes sha-verified + round-3 receipts):

- `bash tools/mori-silence-cases.sh` vs census-r2 `fe22a14f…`: `MORI_SILENCE_CASES:
  matched=25 total=27` exit 1; the 2 residual FAILs were the matcher defect — bash 5.3.15
  probe: `x: no-match` / `y: no-match` / `x|y: MATCH`; counterfactual witness
  `matched=27 total=27` exit 0 (`corpus/evidence/cutover-r3-20261015T165712Z-oracle-counterfactual.log:48`
  vs `:52`; scratch sha `ae95b601…`, receipt `:7`; re-derived byte-identical in
  `verdict-machine-r4.md` §1).
- anti-sniff: a `/tmp` no-logic case-id sniffer, graded by the frozen oracle, scored
  `matched=27 total=27` exit 0; its env log got 27/27 lines with `MORI_FIXTURE=1` and the
  case id inside `MORI_SHOKUNIN_ROOT` (scribe scratch:
  `cid=silent-open MORI_FIXTURE=1 root=…/c/silent-open/root`).
- census `:227`: unreadable `.ufo/state` → rc 1, output = the header line only (1 line),
  0 `MORI_CENSUS:` verdicts, 0 bytes stderr; control → rc 0, 11 lines,
  `MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=1 surfaces=7)` (scribe scratch;
  durable before-side in `verdict-r4-20261015T173551Z-canary227.log:22-32`).
- close tracking: `launch r7; complete r7; complete r5` → `SURFACE lane.kagi: silent
  (… basis=row-D …)` + `FINDING LANE_SILENT` + rc 1; the same fixture with the r7 close
  last → `not-open (… basis=row-4 …)` rc 0 (scribe scratch; durable differential in
  `verdict-machine-r4.md` §4).

**After** (at oracle `be0e28b8…`, census `af2d4e79…`; every value receipt- or note-bound):

- oracle `bash tools/mori-silence-cases.sh` → `MORI_SILENCE_CASES: matched=28 total=28`
  exit 0 — all 27 contract cases pass (the two r3 FAILs now PASS under string-exact
  `want_match`; case ids and want-strings byte-identical to the frozen revision), plus new
  case 28 `shape-invariance`; rerun at the same SHAs diffed empty
  (`verdict-r4-20261015T173551Z-oracle.log:11-21,29-51`; `verdict-machine-r4.md` §1).
  The registered end-goal was `matched=27 total=27`; the landed case set is 27 + the new
  anti-sniff case, so the attained end-goal is **28/28 at the oracle itself** (not a
  scratch counterfactual).
- anti-sniff falsifiers (`verdict-r4-20261015T173551Z-sniffer-v2.log`): m4b verbatim
  `matched=1 total=28` exit 1; m4c verbatim `1/28` exit 1; the order-replay variant that
  happens to disagree between the two shape runs `matched=27 total=28` exit 1 — caught by
  `shape-invariance` alone. r3 baseline for the same attack class: `27/27` exit 0.
  **Residual, named by the verdict note (§2.4):** an order-replay attacker that gives the
  *same* answer to both shape runs still reaches `matched=28 total=28` exit 0 (scratch sha
  `29cb09ce…`). So the honest scope is: the **case-id channel is closed**; "no sniffer can
  fake a pass" is **false in general**. Named unblock (not applied): randomize case order
  per invocation and/or interleave decoy fixtures.
- `:227`: canary227 receipt — before rc 1 / 0 verdict lines / 1 line; after rc 0, full
  verdict (10 lines) with `SURFACE watchdog: ok (… state_rounds=unavailable
  state_unreadable=1; …)` and every other surface reporting; readable control shows
  `state_rounds=1` as the only difference (`verdict-r4-…-canary227.log:22-70`;
  `verdict-machine-r4.md` §3, fixed lines `:233-241`, `:256-260`).
- close tracking: selftest cases `silence: close r7 then close r5 -> r7 anchor stays
  closed` and `silence: close for another round does not close the anchor` PASS
  (`verdict-r4-…-selftest.log:42-43`; `verdict-machine-r4.md` §4, fixed lines `:653-661`);
  scribe canary at `af2d4e79…`: close-r7r5 → `not-open (… basis=row-4)` rc 0, r7-last
  control identical.
- selftest: `MORI_CENSUS_SELFTEST: PASS (30 cases, 30 passed, 0 failed)` exit 0; 25 → 30
  (3 watchdog rc-gate cases + 2 close-tracking cases;
  `verdict-r4-…-selftest.log:12-19,24-26,42-43,51`; `verdict-machine-r4.md` §5).
- live census honest: 9/9 roster lanes `progressing` (8 × `basis=row-A`; aggregator
  `basis=row-B rowb_files=2 attribution=inference`), `SURFACE silence: ok` with zero
  `LANE_SILENT`, `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)`
  (tmux unavailable, counted, never DRIFT), reverify spot: identical exit and finding-id
  set (`verdict-r4-…-live.log`).

| axis | verdict | before → after evidence |
|---|---|---|
| operability | **improved** *(selected axis)* | Before: the verdict machine itself was untrustworthy in four measured ways — frozen matcher caps any single-state emitter at 25/27 (`:362-365`), a no-logic sniffer fakes 27/27, unreadable `.ufo/state` kills the whole census rc 1 header-only 0 verdicts (`:227`), and a later other-round close line silently misgrades a closed anchor to `silent`+`LANE_SILENT` (`:611-616`/`:624`). After: `matched=28 total=28` exit 0 at the landed SHAs (deterministic rerun; want-strings unchanged); the case-id sniffer attack class drops 27/27 → 1/28; crash canary yields a full verdict with `state_unreadable=1`; close canary `not-open`; selftest 30/30; live honest (`verdict-r4-…-{oracle,sniffer-v2,canary227,selftest,live}.log`). Residual (named, not hidden): a self-consistent order-replay sniffer still reaches 28/28 (note §2.4). |
| coverage | **unchanged** | No census contract element changed this round (silence grading is the round-3 contract). Verification coverage grew: oracle 27 → 28 cases (shape-invariance), selftest 25 → 30; the two formerly untestable want-sets now grade real states. `[PARENT: confirm no other census behavior change from the integration diff]` |
| depth | **improved narrowly** | Before: four defects at file:line with before-canaries. After: the class is durable knowledge — `corpus/lessons/2026-10-15-forgeable-oracle-visible-fixtures.md` (identity leak + non-state matcher composed into a forgeable oracle; forgery-probe countermeasure) and `corpus/knowledge/verdict-machine-r4.md` (sha `aab4b62c…`: matcher fix, sniffer channels closed + §2.4 residual, `:227` rc-gate, per-round close tracking, selftest inventory, final tallies). |
| freshness | **improved narrowly** | Before: no round-4 receipts. After: five dated, hash-pinned receipts (`corpus/evidence/verdict-r4-20261015T173551Z-*.log`) at the two pinned SHAs with before/after sha pins and a live reverify spot, indexed with re-run recipes and recorded preconditions in `corpus/evidence/README.md` (round-4 section). Drift pin still absent — carried debt. |
| calibration | **improved** | Before: the oracle could be fooled by an environment marker and a path signal, and its matcher mis-graded honest single states; `LANE_SILENT` fired only on row D and `unavailable` ≠ unhealthy were already proven (round 3). After: the assembled machine is calibrated by adversarial probes — m4b/m4c verbatim `1/28`; the shape runs caught the first order-replay variant (`27/28`); and the weak spot the first probe missed is **named with a measured repro** (self-consistent order-replay `28/28`, note §2.4) rather than left as an implied guarantee. |
| adjacency | **unchanged** | Scope-sentinel: detection/report only; fixtures under `/tmp`; no remediation/kill/pkill/systemctl/host-config content; the frozen-oracle edit was the registered, owner-authorized unfreeze (only oracle-impl writes that file); fleet root read-only for seats; out-of-province live findings (watchdog/waves/journal) reported, not absorbed. `[PARENT: confirm from the integration diff]` |

Admission: operability (the selected axis) **improved**; the other axes above are
proposed per the evidence; **no axis harmed** — expected disposition **ADMIT**
`[PARENT: bind the admission and round-count at integration; weigh the scoped anti-sniff
result: the registered sub-claim "a sniffer-v2 attempt cannot fake a pass" holds for the
case-id attack class but is false in general (note §2.4) — the parent decides whether that
scoping is admissible this round or must ride as a named round-5 unblock]`. No scalar
score. The registered end-goal `N = M` is attained as **28/28** because the oracle gained
the anti-sniff case 28 (registered `27/27` + the mandated shape-invariance case).

Learning trends (lane idiom):

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | **improved** | New: the forgery lesson (landed); the verdict-machine note `corpus/knowledge/verdict-machine-r4.md` (landed, sha `aab4b62c…`); five receipts + README index/recipes (landed); `corpus/README.md` knowledge-table + known-gaps update (landed); `SKILL.md` rows `[PARENT: skill-row-updater — confirm in the integration diff]`. |
| quality | **improved** | Every before-defect has a before/after canary; the matcher fix is proven non-weakening (assert_case want-strings and case ids byte-identical); the sniffer receipt grades its own claim's limits, and the verdict note goes further and names a working attack the receipt's variant missed; the oracle receipt is determinism-checked. |
| discernment | **unchanged** | No outside spot-check of an admit/reject exists — the wave's seats are the lane per protocol; the sniffer probes are same-wave experiments. `[PARENT: bind]` |

Named debt for round 5 (carried, not silently dropped): **the order-replay sniffer channel**
— randomize case order per invocation and/or interleave decoy fixtures so run position does
not map to case identity (note §2.4; measured `28/28` exit 0 scratch `29cb09ce…`); the
frozen-behavioral drift pin (still absent — `corpus/knowledge/silence-cutover-r3.md:253-254`);
the row-6 report-body presence-only residual (spec-declared, `silence-cutover-r3.md:250-252`);
the blocked-attempt receipt-binding and role-routing debts (`SCORECARD.md:128-131`, status
`[PARENT]`).

`[PARENT: bind the integration commit and round-count; re-run `bash tools/mori-census.sh
--selftest`, `bash tools/mori-silence-cases.sh`, and the live census at admission (expect
30/30, 28/28 exit 0, honest verdict); the canary227/sniffer/counterfactual recipes are
verbatim inside their receipts and the note. Replace any residual placeholder before
appending.]`
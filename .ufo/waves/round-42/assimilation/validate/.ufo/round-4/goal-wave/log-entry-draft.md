# LOG.md entry draft — append-only (scribe seat, goal wave)

Integration target: append to `LOG.md` at EOF, after the round-3 goal-wave entry — parent-owned,
append-only. Suggested heading: `## round 4 — verdict machine trust end-to-end (goal wave)`
`[PARENT: keep or rename the heading; bind the commit hash(es), the acceptance re-run
outputs and the round-count line]`.

Draft status: **v3 2026-10-15T17:55Z** by the scribe seat — after-side bound to the landed
revisions (oracle `be0e28b8…`, census `af2d4e79…`, `VERSION=census-r3`), the receipt set
`corpus/evidence/verdict-r4-20261015T173551Z-{selftest,oracle,canary227,sniffer-v2,live}.log`,
and the verdict note `corpus/knowledge/verdict-machine-r4.md` (sha256
`aab4b62c35e4b01606bda9b10877cc7ce7122ac3c21c589e16cf2dedaf58e28e`). v3 carries the note's
§2.4 residual (a self-consistent order-replay sniffer still fakes a pass). v1/v2 predated
the note and are superseded.

---

## round 4 — verdict machine trust end-to-end (goal wave)   `[PARENT: heading]`

**Round 4 — goal-wave admission (2026-10-15).** Motivating evidence: the round-3 verdict's
named debt (`SCORECARD.md:185-191`, admission commit `bbcc1ad` records / `1439c47`
evidence) — the frozen-oracle matcher fix (witness `ae95b601…`), oracle anti-sniff
hardening (opaque per-case dirs, drop `MORI_FIXTURE`, shape-invariance case), census
`:227` `state_n` pipefail hardening, and per-anchor-round close tracking; end-goal
`matched=N total=M`, `N=M`, at pinned SHAs, selftest green, live census honest, zero
regression.

Measured before-states at the round-3 SHAs (scribe scripts under `/tmp`, sha-verified;
durable before-side in the canary227 receipt / verdict note):

- **(a) matcher** — `bash tools/mori-silence-cases.sh` vs census-r2 `fe22a14f…`:
  `MORI_SILENCE_CASES: matched=25 total=27` exit 1; the 2 residual FAILs are the frozen
  matcher `case "$obs" in $want)` (`tools/mori-silence-cases.sh:362-365` at `505a7504…`)
  taking an expansion-introduced `|` literally — bash 5.3.15 probe output `x: no-match` /
  `y: no-match` / `x|y: MATCH`; counterfactual one-block fix `matched=27 total=27` exit 0
  (`corpus/evidence/cutover-r3-20261015T165712Z-oracle-counterfactual.log:52`; scratch sha
  `ae95b601…`, re-derived byte-identical in `verdict-machine-r4.md` §1).
- **(b) leak/sniffer** — a `/tmp` no-logic case-id sniffer census through the frozen
  oracle: `matched=27 total=27` exit 0; 27/27 runs saw `MORI_FIXTURE=1` and the case id
  inside `MORI_SHOKUNIN_ROOT` (leak sites `:149`, `:269`, `:270`; full channel table in
  `verdict-machine-r4.md` §2.1 and
  `corpus/lessons/2026-10-15-forgeable-oracle-visible-fixtures.md`); round-3 falsifier m4b
  first demonstrated the class.
- **(c) `:227`** — unreadable `.ufo/state`: rc 1, stdout = header line only (1 line), 0
  `MORI_CENSUS:` verdicts, 0 B stderr; control rc 0, 11 lines, CLEAN verdict (class pinned
  by `corpus/lessons/2026-10-15-errexit-pipefail-silent-crash.md`).
- **(d) close tracking** — `launch r7; complete r7; complete r5` graded `SURFACE lane.kagi:
  silent (… basis=row-D …)` + `FINDING LANE_SILENT` rc 1; the same fixture with the r7
  close last graded `not-open (… basis=row-4 …)` rc 0 (`:611-616`, `:624`).

**Landed.** Oracle `tools/mori-silence-cases.sh`, sha256
`be0e28b8bf3cc34e2a35e6cea7c05bffff376111b42d985b6bec7f0e21f59456`: alternation-safe
`want_match` (exact-string alternatives, no pattern semantics; assert_case want-strings and
case ids byte-identical to the frozen revision — the fix cannot have weakened an
expectation), opaque per-case trees (`CASE_DIR=$(mktemp -d "$WORK/case.XXXXXXXX")` — no
case id in any path handed to the census), `MORI_FIXTURE` removed from the census env, new
case 28 `shape-invariance` (same fixture bytes under two random dir names must grade
identically, normalized stdout included). Census `tools/mori-census.sh`, sha256
`af2d4e79e69b70bb0b5aecd6acc9608fc7c16b0716766d4a60310e0689d350d7` (`VERSION=census-r3`):
`:227` rc-gated (`cap find` + `state_rounds=unavailable state_unreadable=1` disclosure;
readable dirs keep the r2 row bytes), close tracking per anchor round (close pairs; any
later same-round close closes, other-round closes irrelevant), selftest 25 → 30 (3 watchdog
rc-gate cases + 2 close-tracking cases). Supporting: the forgery lesson
`corpus/lessons/2026-10-15-forgeable-oracle-visible-fixtures.md`; the verdict note
`corpus/knowledge/verdict-machine-r4.md` (sha `aab4b62c…`); five receipts
`corpus/evidence/verdict-r4-20261015T173551Z-*.log` + `corpus/evidence/README.md` round-4
index with re-run recipes/preconditions; `corpus/README.md` knowledge-table + known-gaps
update (landed); `SKILL.md` `[PARENT: skill-row-updater — confirm in the integration
diff]`. Write ownership held: only oracle-impl wrote the oracle, only census-impl the
census, only the owner seats their files, only the scribe this directory.

**Acceptance evidence at the landed SHAs** (receipts 17:35:51–17:37:27Z; parent re-run at
integration `[PARENT: bind]`):

- `bash tools/mori-census.sh --selftest` → `MORI_CENSUS_SELFTEST: PASS (30 cases, 30
  passed, 0 failed)` exit 0.
- `bash tools/mori-silence-cases.sh` → `MORI_SILENCE_CASES: matched=28 total=28` exit 0
  (the two r3 matcher FAILs now PASS; case 28 PASS; deterministic rerun diffed empty).
- sniffer-v2 falsifiers: m4b/m4c verbatim `matched=1 total=28` exit 1; the order-replay
  variant that disagrees between shape runs `27/28` exit 1 caught by `shape-invariance`;
  r3 baseline for the same class was `27/27` exit 0. **Residual (note §2.4):** an
  order-replay attacker that gives the SAME answer to both shape runs still reaches
  `matched=28 total=28` exit 0 — the case-id channel is closed, but "no sniffer can fake a
  pass" is false in general; named unblock: randomize case order / interleave decoys.
- canary227: r3 `fe22a14f…` → rc 1, 0 verdicts, header only; r4 → rc 0, full verdict with
  `state_rounds=unavailable state_unreadable=1`; readable control `state_rounds=1`.
- close canary: `complete r7; complete r5` → r4 `not-open (basis=row-4)` rc 0 (was
  `silent`+`LANE_SILENT` rc 1); pinned by selftest cases; control identical.
- live census: 9/9 roster lanes `progressing` (8 × row-A; aggregator row-B
  `attribution=inference`), `SURFACE silence: ok` zero `LANE_SILENT`,
  `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` (tmux unavailable,
  counted, never DRIFT); reverify spot identical exit + finding-id set.

**Verdicts** `[PARENT: bind]`. Expected shape: operability (the selected axis)
**improved**; coverage **unchanged** (no census contract change; verification coverage
grew); depth/freshness **improved narrowly**; calibration **improved**; adjacency
**unchanged**; none harmed → **ADMIT**. The anti-sniff sub-claim is scoped: the case-id
channel is closed (27/27 → 1/28), but the self-consistent order-replay residual is
measured and named — whether that scoping is admissible this round or must ride as a
round-5 unblock is the parent's call. Learning trends: expansion/quality **improved**,
discernment **unchanged**. Full per-axis before→after: the `SCORECARD.md` Round 4 section.

**Carried debt (named, not silently dropped).** **Order-replay sniffer channel** —
randomize case order per invocation and/or interleave decoys so run position does not map
to case identity (`verdict-machine-r4.md` §2.4; measured `28/28` exit 0, scratch sha
`29cb09ce…`); frozen-behavioral drift pin (still absent,
`corpus/knowledge/silence-cutover-r3.md:253-254`); row-6 report-body presence-only
residual (`silence-cutover-r3.md:250-252`); blocked-attempt receipt-binding and
role-routing debts (`SCORECARD.md:128-131`) `[PARENT: status]`.

**Boundaries held.** Detection and report only: fixtures under `/tmp`; no remediation, no
kill/pkill of real processes, no systemctl or host config edits; no lane-side commits by
seats (the parent integrates under the mori identity); fleet root read-only for seats.
`[PARENT: confirm from the integration diff]`

Round report: `[PARENT: .ufo/reports/round-4/mori-goalwave.md or equivalent]` · Verified
lane rounds: `[PARENT: 3 → 4 on admission]`
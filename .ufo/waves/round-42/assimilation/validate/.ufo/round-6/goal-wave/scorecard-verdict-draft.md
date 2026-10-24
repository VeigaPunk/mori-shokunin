# Round 6 verdict — integration draft (scribe seat, goal wave)

Integration target: append as a `## Round 6 verdict — 2026-10-15 (goal wave)` section in
`SCORECARD.md` (parent-owned; append-only — the round-5 section `SCORECARD.md:241-285` and
everything above it stay untouched). Verdict vocabulary only (`improved` / `harmed` /
`unchanged` / `unprovable-but-better`); no scalar scores. Every figure below is bound to a
landed artifact, a receipt, or a command run at a pinned SHA; `[PARENT: …]` marks values
only the integration commit or the parent's acceptance re-run can bind; `[PENDING: …]`
marks values unlanded at this draft's clock.

- Evidence commit: `[PARENT: wave integration commit hash under the mori identity]`
- Lane baseline entering the wave: `848b3a6` (round-5 records; evidence `a420deb7`).
- Round-count claim: `[PARENT: verified-round accounting 5 → 6 on admission]`
- Draft status: **v6 2026-10-15T19:19Z** by the scribe seat. Before-side measured first-hand
  at the round-5 landing oracle `7143ccc2…` (970 lines), 18:45–18:47Z. After-side measured
  first-hand at the landed oracle `3307761a04a1eab8f33859a69d2eb63fb6312afb8f8041f7b09da4544be174b9`
  (1082 lines), 19:07–19:08Z; the receipts-writer's final set pins the same `3307761a…`
  (captured 19:12–19:13Z); the note/lesson figures were taken at `b2ebe5e7…`, a
  comment-only delta vs `3307761a…` (0 code lines, re-verified by three seats). Frozen
  census `af2d4e79…` re-verified before and after every battery run. Scratch:
  `/tmp/mori-scribe-r6/{before2,after2}/` (one-command battery `after2/run-all.sh`).

## Round 6 verdict

Round scope (registered round-5 correction, `SCORECARD.md:264-273`; LOG round-5 entry):
close the two residuals the round-5 admission registered as round 6's claim —
**R1 stdout-backchannel** (census reads `CASE_ORDER`/`RUN_NONCE` from the oracle's own
stdout via `/proc/<ppid>/fd/1` mid-run and replays by position; sibling pinned-seed channel:
`MORI_SHUFFLE_SEED` readable from `/proc/<oracle>/environ`) and **R2 content-keyed forgery**
(a memorized content→state table passes because the nonce binds no fixture content).
Registered claim: before — the run header prints secrets before the case loop and fixture
content is nonce-free and run-invariant, so an fd-reading replay census and a
content-memorizing census each reach `matched=28 total=28` exit 0 with zero grading logic;
after — the header prints only AFTER the case loop (no living census invocation can read
secrets from oracle stdout/environ while running) and fixture content carries the run nonce
and varies per run, so memorized tables are stale: both attackers fail, while the honest
census stays `matched=28 total=28` exit 0 across shuffled runs with byte-identical grade
tuples. Registry (28 ids/wants) byte-identical; census `af2d4e79…` FROZEN (oracle-only
round).

Naming note: this section uses the SCORECARD/dispatch labels (R1 stdout-backchannel,
R2 content-forgery). In `corpus/knowledge/verdict-machine-r5.md` §4 the same channels appear
as its R2 (stdout capture) and its R4 (content forger); its R1 (pinned environ) is probed
here inside R1.

**Before** (scribe first-hand, 18:45–18:47Z; double-sourced by the receipts' before-legs
18:44Z and the lesson's before rows):

- **Header before the loop** — `7143ccc2…:953-956` printed `SHUFFLE_SEED=` / `RUN_NONCE=` /
  `CASE_ORDER=<28 ids>` and only then `:958-960` dispatched the shuffled cases.
- **R1 passes** — attacker-leak (`3f05915c…`, stdout → regular file): `matched=28 total=28`
  EXIT 0 (`before2/leak.out`). Mid-run `/proc/<gp>/fd/1` probe: 29/29 invocations read the
  full header (`before2/fd1-oracle.out`). Pinned run: oracle-chain environ exposes
  `MORI_SHUFFLE_SEED=31337` 29/29; seed-reader attacker (`3969ce3b…`) pinned `28/28` EXIT 0,
  unpinned `1/28` EXIT 1. Receipt cross-check
  (`corpus/evidence/backchannel-r6-20261015T191216Z-attack-r1.log`): redirect 28/28,
  pinned-environ 28/28. Note/lesson before rows agree (`verdict-machine-r6.md` §1; lesson
  table).
- **R2 passes** — stale memorizer (`3e0fa4c7…`): `28/28` EXIT 0; a fresh memorizer learned
  from one run replayed 28/28 unpinned AND same-pin (`before2/validation-r5/`). Run nonce in
  fixture content other than dedicated artifacts: 0/29; fingerprint F byte-identical across
  two different-seed runs (`929a5dc1…`). Receipt cross-check: 28/28.
- Honest baseline `28/28` EXIT 0; selftest `PASS (30 cases, 30 passed, 0 failed)` EXIT 0.

**After** at the landed oracle `3307761a…` (1082 lines; census frozen, sha re-verified;
receipts at these same bytes; note/lesson at the comment-only-equivalent `b2ebe5e7…`):

- **Mechanism** — (a) run header moved after the case loop (`:1066-1072`); (b) pinned values
  removed from the process tree by a one-shot self re-exec when a pin is present
  (`:206-224`): values travel through a pipe fd (`:211`), pins unset, `exec bash "$SELF"
  "$CENSUS"` (`:214`), drained at startup (`:219`); the revision comment records that a
  runtime `unset` does not scrub `/proc/<pid>/environ`; (c) per-run `RUN_SALT`
  (`:239-240`, never printed/exported/pinnable) as salt/blob files under each `CASE_DIR`
  (`:309-315`) and woven into every committed body/commit message plus the four
  untracked/dirty fixtures (`:417-419`, `:823`/`:836`/`:899`/`:921`); (d) `redact()`
  (`:545`) strips the nonce token from FAIL fragments; nonce FAIL text names no token
  (`:599`).
- **R1 closed (oracle-surface channels)** — fd1 mid-run header hits **0/29** (was 29/29);
  leak attacker **`0/28` EXIT 1** (was 28/28); pinned environ probe **0/29** (was 29/29;
  lesson: `seed=[]` from invocation 1); unpinned environ 0/29; seed-reader pinned `1/28`
  EXIT 1 (was 28/28); nonce tokens in oracle stdout of attacker runs: 0. Receipt legs all
  `0/28`; note §3/§5.1 agree. **Scope boundary named (note §5.3):** a pin living in a
  *surviving ancestor's* exec-time environ (wrapper pattern, e.g. `env VAR=… bash -c 'bash
  oracle…; true'`) is outside the oracle's reach and reaches `28/28` — measured by the
  note-writer (`G-r1-liveanc.out`) and the critic (`EV-r1p-export.log`); the plain
  `env VAR=… bash oracle.sh` prefix is closed.
- **R2 closed for the enumerated/naive classes** — stale memorizer **`0/28` EXIT 1** (was
  28/28); fresh memorizer learned at r6 **`0/28` EXIT 1** both replay modes (salt is
  unpinnable); fingerprints across two fresh runs share **0 of 29** values (was 29/29
  identical); nonce appears in fixture content for 28/29 invocations (exception
  `repo-missing-unavailable`, no repo tree — its fingerprint still varies via salt files).
  Receipt legs `0/28` (incl. a nonce-only normalizer). **Residual class named (note §4;
  lesson):** a full-grammar pattern-normalizing memorizer (`6b79f776…`, strips both marker
  grammars, omits raw sizes, mechanical readability marker) reaches **`28/28` EXIT 0** —
  measured by the note-writer twice, the lessons-distiller (`6b79f776…`) and the critic
  (`EV-norm2.log`). A bracket-only normalizer scores `24/28` — the four discriminating cases
  are `dirty-same-path-as-sibling-progress`, `untracked-recent-progress`,
  `untracked-report-progress`, `main-repo-noise-silent` (note §4 table).
- **Honest unaffected** — `28/28` EXIT 0 across two fresh seeds and two pinned runs; sorted
  per-case grade tuples byte-identical to the before-side (sha `a70af583…`; note/lesson and
  receipt oracle-1/2/3 agree); pinned pair byte-identical stdout; selftest `PASS (30 cases,
  30 passed, 0 failed)` EXIT 0; live census `MORI_CENSUS: DRIFT (findings=15 drift=14
  unavailable=1 surfaces=7)`, 9/9 lanes progressing, `tmux` unavailable (receipt
  `…-live.log`).
- **Registry byte-identical; census frozen** — `CASE_IDS` block diff empty (note §2.3:
  block sha `c27d5111…`, wants sha `bce578e2…`); only the two nonce failure-text strings
  differ (redacted); census sha `af2d4e79…` verified before/after every run.
- **Mid-wave evolution (record, not a live defect)** — an intermediate revision
  `e64cc067…` still exposed the pins via the oracle's own environ (29/29; seed-reader
  28/28 — measured by this seat's battery); the landed revision replaced the ineffective
  `unset` with the re-exec and measures closed.

| axis | verdict | before → after evidence |
|---|---|---|
| operability | **improved** *(selected axis)* | Before: both registered residuals pass with zero grading logic. After: every registered attack class fails at the landed bytes (R1 leak 0/28, fd1 0/29, oracle-environ 0/29, seed-reader pinned 1/28; R2 stale 0/28, fresh 0/28 ×2 modes, nonce-normalizer 0/28), honest census unharmed (28/28 ×4 runs, tuples byte-identical to before, pinned stdout byte-identical), registry byte-identical, census frozen. Two wider channels survive and are named (below). Three seats'+receipts' batteries agree. |
| coverage | **unchanged** | Registry byte-identical (`CASE_IDS` diff empty, note §2.3 shas); no new measured surface; census frozen `af2d4e79…`. |
| depth | **improved** | `corpus/knowledge/verdict-machine-r6.md` (design, closures, §4 discriminating cases + normalizer residual, §5 channel map incl. `/proc/<pid>/mem` not-a-channel, §5.3 survivor channel, §7 tallies) + lesson `corpus/lessons/2026-10-15-run-secret-timing-and-content-freshness-limits.md` (timing/shape framing; attacker-design pitfalls: collision → 27/28, size nondeterminism → 1/29 vs 29/29). Mechanism pinned with file:line across three seats. |
| freshness | **improved narrowly** | Seven dated, hash-pinned receipts at the final `3307761a…` + frozen `af2d4e79…` (`backchannel-r6-20261015T191216Z-{oracle-1,oracle-2,oracle-3,selftest,live,attack-r1,attack-r2}.log`), leg addenda with tallies, before-legs at `7143ccc2…`; indexed in `corpus/evidence/README.md` (r6 rows landed). |
| calibration | **improved** | Multi-seat independent batteries concur (scribe full battery; receipts-writer final set incl. nonce-normalizer; note-writer incl. both normalizer models; lessons-distiller incl. the surviving `6b79f776…`; critic incl. `EV-norm2.log` and the survivor-pin `EV-r1p-export.log`); the `e64cc067` intermediate was measured open and the landed revision measured closed; the fresh-memorizer generator defect (dropped rc) was found/fixed/re-validated; the surviving classes are reported though they pass (no cherry-picking). |
| adjacency | **unchanged** | Detection/report only; fixtures `/tmp`; census frozen; no remediation/kill/systemctl/host-config content; fleet root read-only for seats. `[PARENT: confirm from the integration diff]` |

Admission: `[PARENT: bind the admission and round-count at integration. Expected disposition
on the evidence above: **ADMIT-with-correction** — both registered residuals are closed for
the enumerated/naive classes at the landed bytes with the honest census unharmed, but two
wider channels survive and are named with witnesses: (1) the full-grammar
pattern-normalizing memorizer `28/28` (note §4; R2-class), (2) the surviving-ancestor
exec-time-environ pin `28/28` under the wrapper pattern (note §5.3; R1-class scope
boundary). This matches the round-5 precedent (ADMIT-with-correction when a wider forgery
survives).]` No scalar score.

Learning trends (lane idiom):

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | **improved** | Note `verdict-machine-r6.md` + lesson `2026-10-15-run-secret-timing-and-content-freshness-limits.md` landed; SKILL row (`SKILL.md` working tree sha `35c67fd4…`, r5+r6 contract); seven receipts + `corpus/evidence/README.md` index rows; `corpus/README.md` rows (note/lesson/r6 anti-sniff bullet). |
| quality | **improved** | Every claim element measured at pinned shas by multiple seats; the mid-wave `e64cc067` environ channel caught, closed, recorded; the generator rc defect found/fixed/re-validated; the full-grammar normalizer and the survivor-pin channel are reported even though they pass (the lessons' "key definition + size handling + re-run across seeds" discipline is applied to both directions). |
| discernment | **unchanged** | No outside spot-check of an admit/reject exists — the wave's seats are the lane per protocol. `[PARENT: bind]` |

Named debt for round 7 (from the landed note/lesson): (1) **R2-class: the
pattern-normalizing memorizer** (`6b79f776…`, `28/28` exit 0) — the binding fix is the one
already registered since round 5: make semantically relevant content vary per run
(ledger epochs/rounds, which want-set branch is correct, mission structure) so a memorized
row is *wrong*, not merely stale (note §4; lesson "Why the surviving attacker is the right
thing to name"); (2) **R1-class: the surviving-ancestor environ pin** under the wrapper/CI
invocation pattern — fix direction: entropy that never transits any process environment, or
pinning via a private fd/file the operator owns (note §5.3). Carried unchanged:
frozen-behavioral drift pin (`silence-cutover-r3.md:253-254`); row-6 report-body
presence-only residual (`silence-cutover-r3.md:250-252`); blocked-attempt receipt-binding
and role-routing debts (`SCORECARD.md:128-131`).

`[PARENT: bind the integration commit and round-count; re-run `bash tools/mori-census.sh
--selftest` (expect 30/30 exit 0), `bash tools/mori-silence-cases.sh` (expect 28/28 exit 0;
≥2 seeds; pinned pair byte-identical), the R1 leak attacker and seed-reader attacker (expect
FAIL incl. pinned; expecting the named survivor-pin wrapper only if the wrapper pattern is
used), the R2 stale+fresh memorizers (expect FAIL) and the `6b79f776…` normalizer (expect
PASS — the named residual), and the live census; re-run recipes:
`corpus/evidence/README.md` round-6 section (index rows landed); this seat's battery
`/tmp/mori-scribe-r6/after2/run-all.sh` (before-side figures `/tmp/mori-scribe-r6/before2/`,
oracle snapshots `oracle-r6-{e64cc067,b2ebe5e7,final}.sh`).]`
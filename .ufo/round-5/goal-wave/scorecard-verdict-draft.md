# Round 5 verdict — integration draft (scribe seat, goal wave)

Integration target: append as a `## Round 5 verdict — 2026-10-15 (goal wave)` section in
`SCORECARD.md` (parent-owned; append-only — the round-4 section `SCORECARD.md:194-238` and
everything above it stay untouched). Verdict vocabulary only (`improved` / `harmed` /
`unchanged` / `unprovable-but-better`); no scalar scores. Every figure below is bound to a
landed artifact or receipt at a cited path; `[PARENT: …]` marks values only the integration
commit or the parent's acceptance re-run can bind; `[PENDING: …]` marks values unlanded at
this draft's clock.

- Evidence commit: `[PARENT: wave integration commit hash under the mori identity]`
- Lane baseline entering the wave: `7a3629a` (round-4 records; `5b62c897` evidence)
- Round-count claim: `[PARENT: verified-round accounting 4 → 5 on admission]`
- Draft status: **v4 2026-10-15T18:21Z** by the scribe seat — this revision folds the
  **corrected scope** (§Correction below): the lessons-distiller's landed lesson
  `corpus/lessons/2026-10-15-run-order-spoofing-shuffle-nonce-limits.md` falsifies the
  claim's general form, and this seat independently reproduced both residual forgers. The
  note-writer's `corpus/knowledge/verdict-machine-r5.md` (sha `0ef76e9e…`) also landed
  and records the mechanism, a SUT-visibility table, and witnessed residuals R1–R4.
  After-side bound to the **landed** oracle `tools/mori-silence-cases.sh` sha256
  `7143ccc2a14221713334c33ade56e24ca711fbd0d3d17f31d33e151be544f017` (970 lines; arrived
  18:03:25Z, sha re-verified before/after every scribe run) and the **frozen** census
  `af2d4e79…`. Receipt set
  `corpus/evidence/order-r5-20261015T180431Z-{oracle-1,oracle-2,oracle-3,selftest,live,sniffer}.log`
  landed (indexed in `corpus/evidence/README.md`); scribe probes `/tmp/mori-scribe-r5/`
  agree with every receipt figure.

## Round 5 verdict

Round scope (registered round-4 correction, `SCORECARD.md:229-238`; mechanism in
`corpus/knowledge/verdict-machine-r4.md` §2.4): close the **run-order spoofing channel**.
Registered claim: **before** — cases execute in fixed registry order and carry no per-run
secret, so a zero-logic census that counts its own invocations and replays a canned grade
sequence scores `matched=28 total=28` exit 0; **after** — the oracle executes cases in
seeded-shuffled order (seed logged; same seed ⇒ same order) AND injects an unpredictable
per-run nonce into fixtures requiring it in census output (stale/missing nonce fails);
therefore every zero-logic/replay spoof class fails to reach 28/28, while the honest census
holds `matched=28 total=28` exit 0 across shuffled runs with byte-identical per-case grade
tuples. Census frozen (`af2d4e79…`) — only the oracle changed.

**Before** (scribe 17:56:57–17:56:58Z; receipts-writer 17:59:18–17:59:19Z, at
`be0e28b8…` + `af2d4e79…`):

- Fixed registry order, no per-run secret: cases ran at source level in registry order
  (`:430-672` at `be0e28b8…`; shape pair `:720-725`; `assert_case` inline `:358-360`);
  `grep -nE 'seed|shuffle|nonce|SRANDOM|RANDOM'` → no hits; census env `:279-306`
  carried no run secret.
- Zero-logic order sniffer fakes a full pass: critic v3 (`ba2a11ba…`; scribe copy
  `66d9b64e…`) → `matched=28 total=28` exit 0; admission `sniffer-order.sh`
  (sha at capture `22d298f8…`) → `28/28` exit 0; receipts v3a/v3b/v3c each `28/28`
  exit 0 at the same snapshot. Honest baseline: `28/28` exit 0.

**After** at the landed oracle `7143ccc2…` (census `af2d4e79…`; scribe probes
18:04:02–18:08:09Z; receipts 18:04:31–18:06:58Z):

- **Landed mechanism.** Run entropy (`:124-167`): `rand32` from `/dev/urandom`
  (`:142-153`); `RUN_SEED = MORI_SHUFFLE_SEED` else random (`:155-160`); `RUN_NONCE`
  generated independently of the seed (`:161-167`), token `nonce-<N>` (`:167`). The
  nonce reaches the census three ways (env `MORI_RUN_NONCE`, `$CASE_DIR/run-nonce`, the
  disk-target dir) and every case requires the current token (`nonce_present :422-427`;
  `assert_case :490-494`; readonly `:836-837`; shape `:885-886`; failure
  `run-nonce want=[…] missing (canned/replayed output?)`); seed not exported to the
  census env (`:352-353`). Registry `CASE_IDS` (`:902-931`, same 28 ids); xorshift32
  (`:936-942`) + Fisher–Yates (`:944-951`); runner shuffles then logs `SHUFFLE_SEED=`,
  `RUN_NONCE=`, `CASE_ORDER=` (`:953-956`), dispatches (`:958-960`).
- **Honest holds, shuffled.** Scribe: random-seed run `28/28` exit 0; `MORI_SHUFFLE_SEED=12345`
  ×2 identical `CASE_ORDER`, both `28/28`; different seed `777` different order, `28/28`;
  sorted per-case tuples byte-identical across runs (sha `a70af583…`). Receipts
  `…-oracle-1/2/3.log`: `28/28` exit 0 three times (seeds `1612512038`, `1323201475`,
  pinned `1612512038`; oracle-3 `CASE_ORDER` identical to oracle-1, `diff` = `RUN_NONCE`
  line only; tuple sha `a70af583…` matching this seat's). Selftest `PASS (30 cases, 30
  passed, 0 failed)` exit 0 (receipt `…-selftest.log`). Live honest: receipt `…-live.log`
  two spots, identical finding-id sets, `DRIFT (findings=15 drift=14 unavailable=1
  surfaces=7)`, tmux the one unavailable.
- **Enumerated spoof classes fail.** Scribe: critic v3-class `0/28`, admission order
  `0/28`, stale replay of a full passing run (same pinned order, fresh nonce) `0/28`,
  nonce-aware canned `6/28` — all exit 1. Receipts `…-sniffer.log`: v3a/v3b/v3c `0/28`,
  v3d (live-nonce echo + positional table) `6/28`, v3e (stale token) `0/28`, all exit 1;
  the same v3a/b/c were `28/28` exit 0 at `be0e28b8…`.
- **Correction — the general claim is false (folded same-round).** The
  lessons-distiller's lesson (`corpus/lessons/2026-10-15-run-order-spoofing-shuffle-nonce-limits.md`,
  landed; measured ~18:02–18:25Z) names **two forgers that still reach `28/28` exit 0**
  at the landed oracle, and this seat reproduced both:
  - **content-keyed memorizer** (`fp-attacker.sh` sha `3e0fa4c7…`): learns one run's
    fixture fingerprints → canned rows, echoes the env nonce — zero grading logic,
    immune to shuffle+nonce because the correct answers are constant; scribe spot
    `matched=28 total=28` exit 0 (`/tmp/mori-scribe-r5/after/fp-attacker-check.out`;
    lesson: same at three seeds).
  - **run-header leak via `/proc`** (`attacker-leak.sh` sha `3f05915c…`): reads
    `CASE_ORDER=`/`SHUFFLE_SEED` from the oracle's own stdout through `/proc/<gp>/fd/1`
    when stdout is a regular file — **the receipt/log pattern** — replays the public
    table and echoes the env nonce, no fixture reads; scribe spot `matched=28 total=28`
    exit 0 with stdout redirected to a file (`/tmp/mori-scribe-r5/after/leak-attack-check.out`);
    piped stdout closes this channel (lesson: 0/28). Lesson also: a pinned
    `MORI_SHUFFLE_SEED` is readable via `/proc/<gp>/environ` in **any** stdout mode,
    and an env-echo attacker with the *known* seed 777 reaches `28/28`.
  So the receipt's own scope line ("impossibility not claimed") was right, and the
  round's claim must carry the same correction: the **enumerated** classes
  (invocation-count, canned sequence, stale nonce, seed-guessable) are closed and
  measured; the general "every zero-logic/replay spoof class fails" is **false in
  general** — fixture-content memorization and the process-surface leak still win.

| axis | verdict | before → after evidence |
|---|---|---|
| operability | **improved narrowly** *(selected axis)* | Before: tally forgeable by zero-logic order replay (`28/28` exit 0, three attackers, two seats). After: the enumerated replay classes are closed (`0/28`, `0/28`, `0/28`, `6/28`, `0/28` receipts + scribe agreeing; honest `28/28` across shuffles, tuples `a70af583…`; selftest 30/30) — but two wider forgers still pass (§Correction), so the machine is better, not trustworthy-in-general; the correction is the verification value. |
| coverage | **unchanged** | Census contract untouched (frozen sha); oracle case registry is the same 28 ids — no new/removed case. `[PARENT: confirm from the integration diff]` |
| depth | **improved** | Before: channel named with a measured repro (`verdict-machine-r4.md` §2.4). After: the lesson `2026-10-15-run-order-spoofing-shuffle-nonce-limits.md` — the "hardening moves the attack" pattern, the two working forgers with shas and repair recipes (randomize state-bearing fixture params; treat `/proc` as SUT-readable; log entropy after the run) — plus the landed oracle's mechanism comments, plus `corpus/knowledge/verdict-machine-r5.md` (landed, sha256 `0ef76e9e…`: mechanism §2, SUT-visibility/reachability table §3, residuals R1–R4 §4 with witnesses). |
| freshness | **improved narrowly** | Six dated, hash-pinned receipts `corpus/evidence/order-r5-20261015T180431Z-*.log` + README round-5 index/recipes; lesson dated. Drift pin still absent — carried. |
| calibration | **improved** | Nine measured attacker variants across two seats (receipts v3a–e; scribe stale/nonce-aware; lesson's echo/stale/memorizer/leak family) and the boundary map: nonce isolates staleness (28 nonce-only FAILs, 0 state FAILs, lesson), shuffle kills order-blind tables (6/28), and the two classes beyond both are measured open. Receipt scope line: impossibility not claimed — now proven correct by counterexample. |
| adjacency | **unchanged** | Detection/report only; fixtures `/tmp`; census frozen (sha verified); no remediation/kill/systemctl/host-config content; fleet root read-only for seats. `[PARENT: confirm from the integration diff]` |

Admission: `[PARENT: bind the admission and round-count at integration. Expected
disposition on the evidence above: **ADMIT-with-correction** (the round-4 precedent): the
registered class is closed with two-seat measurements, and the correction — two wider
forgers still reach 28/28, one mode-dependent (file-stdout receipts) — is folded
same-round rather than left implicit. The parent decides whether the corrected scope is
admissible or must ride as round-6's registered claim; the lesson's countermeasures are
the named next unblock.]` No scalar score.

Learning trends (lane idiom):

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | **improved** | Landed: `SKILL.md:53-64` r5 contract row; six receipts + README round-5 index; the r5 lesson; `corpus/knowledge/verdict-machine-r5.md` (sha `0ef76e9e…`); `corpus/README.md` r5 rows (scoped like this draft). No open expansion marker. |
| quality | **improved** | Every claim element measured at pinned SHAs by two seats (matching tuple sha `a70af583…`); the falsifying counterexamples to the claim's general form were found, reproduced, and written down in-round — the machine's true boundary is now measured on both sides. |
| discernment | **unchanged** | No outside spot-check of an admit/reject exists — the wave's seats are the lane per protocol; the forgers are same-wave experiments. `[PARENT: bind]` |

Named debt for round 6 (carried, not silently dropped): **fixture-content memorization**
(lesson §A; countermeasure: randomize state-bearing fixture parameters so yesterday's
fixture→row table is wrong today); **process-surface leak of run secrets** (lesson §B:
`/proc/<gp>/fd/1` for file-stdout, `/proc/<gp>/environ` for pinned seeds; countermeasure:
do not print run entropy to a file-bound stream while grading, log it after the run);
keep the capability-indexed forgery repertoire current (lesson: the passing list *is* the
security statement). Carried unchanged: frozen-behavioral drift pin
(`silence-cutover-r3.md:253-254`); row-6 report-body presence-only residual
(`silence-cutover-r3.md:250-252`); blocked-attempt receipt-binding and role-routing debts
(`SCORECARD.md:128-131`).

`[PARENT: bind the integration commit and round-count; re-run `bash tools/mori-census.sh
--selftest` (expect 30/30 exit 0), `bash tools/mori-silence-cases.sh` (expect 28/28 exit 0;
≥2 seeds), and the live census; the correction's counterexamples are re-runnable from the
lesson's Repro section and `/tmp/mori-scribe-r5/after/{fp-attacker-check,leak-attack-check}.out`. Receipt-based recipes: `corpus/evidence/README.md` round-5 section.]`
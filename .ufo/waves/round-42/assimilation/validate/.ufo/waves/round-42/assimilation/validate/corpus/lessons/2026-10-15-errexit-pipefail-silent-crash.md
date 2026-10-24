# Lesson — an unreadable input can kill a `set -euo pipefail` gate silently, and the crash exit code equals the DRIFT exit code

date: 2026-10-15 · lane: mori-shokunin · round: 3 · source seat: lessons-distiller (flash wave)

Measured against `tools/mori-census.sh` revision r1
sha256 `e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2`
(`VERSION=census-r1`, `:58`) and the frozen oracle `tools/mori-silence-cases.sh`
sha256 `505a7504811401b13fd96f8925605e744fbb54970c8ac65ac331b053d647e580`.
This note records the class, not a scalar score and not a promise that the
round-3 cutover fixes every instance (see Limits).

## The lesson

In a gate that runs `set -euo pipefail` (`tools/mori-census.sh:51`), an unguarded
`var=$(producer | consumer)` assignment aborts the whole run when the **producer**
fails for an environmental reason (permission denied, IO error), even though every
downstream stage succeeds:

- the construct swallows the producer's error text (`2>/dev/null`),
- `pipefail` makes the pipeline rc the producer's rc even when `wc`/`sort`/`tail`/`cut`
  all exit 0 (measured below),
- an assignment whose command substitution fails is a plain command under `set -e`.

The gate then exits with the producer's rc — measured **1** — which is *the same
exit code this gate uses for a real DRIFT verdict* (`:583-587`: CLEAN→0, DRIFT→1,
else→2), and it prints **no verdict line**: findings and surfaces are only flushed
after all probes finish (`:576-581`), and the header prints first (`:566`).
A consumer that checks the exit code reads a false DRIFT; a consumer that checks
the verdict line reads nothing at all; both misread "could not read the input" as
either "problem found" or "no evidence".

## What was measured (2026-10-15T16:41–16:44Z, temp roots under /tmp, all deleted after)

| Run | Setup | Result |
|---|---|---|
| control | clean temp root, readable lane repo | rc=1, verdicts=1, `MORI_CENSUS: DRIFT (findings=3 drift=2 unavailable=2 surfaces=7)` |
| A (`:517`) | lane repo `.git` `chmod 000` | rc=1, **0 verdicts**, 0 B stderr, stdout = header only |
| B (`:220`) | `.ufo/state` dir `chmod 000` | rc=1, **0 verdicts**, 0 B stderr, stdout = header only |
| C (`:283`) | `sub/` inside a wave dir `chmod 000` | rc=1, **0 verdicts**, 0 B stderr, stdout = header only |

The control shows the collision is in-band: on a bare temp root the gate legitimately
ends in DRIFT rc=1; the crashed runs end in the same rc with none of the evidence.

Mechanism, isolated (same shell flags):

- `x=$(find <dir-with-000-subdir> ... | sort -n | tail -1 | cut -d. -f1); echo survived`
  → exit 1, `survived` never printed.
- `find <000-dir> ... 2>/dev/null` alone → rc=1; the same pipeline **without**
  `pipefail` → rc=0 (`wc -l` succeeds and prints `0`); **with** `pipefail` → rc=1.

Attribution was proved with a `/tmp`-only traced copy (the shipped script disables
xtrace at `:56` precisely so journal content cannot leak; for the run A trace the
journal probe was stubbed with `MORI_JOURNALCTL_BIN=/bin/true`). The last executed
command in each crash run:

- A: `+ newest_t=1792082617` (after `++ sort -n` / `++ tail -1` / `++ cut -d. -f1`)
  — `tools/mori-census.sh:517`;
- B: `+ state_n=0` (after `++ find … -name '*.round'` / `++ wc -l` / `++ tr -d ' '`)
  — `tools/mori-census.sh:220`;
- C: `+ newest=1792082572` (after the same sort/tail/cut chain)
  — `tools/mori-census.sh:283`.

Two properties make this easy to miss:

1. **A plausible value can be produced.** In C the pipeline still emitted a real
   epoch (≈ now) because only one subdirectory was unreadable; the run dies right
   after trusting it. The failure is invisible in the value, present only in the rc.
2. **No diagnostic survives.** stderr was 0 bytes in every crash run because the
   construct itself redirects it away; nothing on stdout either (the gate's output
   is buffered in arrays until the end).

Prior art, for context rather than repetition: the oracle already knows one instance
(`tools/mori-silence-cases.sh:350-359` reports "census emitted no MORI_CENSUS
verdict … crashed mid-run" and its comment names `:51,517`; case
`unreadable-git-unavailable` at `:462-468` `chmod 000`s the `.git`), and
`SCORECARD.md:111` recorded the `:517` defect in the round-2 verdict. The
`:220` instance found here is named in
`corpus/knowledge/observability-surfaces-r2.md:311` only as a semantics defect
(round values never read), not as a crash site. The remaining sites in the file
handle unreadable inputs explicitly (watchdog log `:206-208`, cgroup via
`[ -r ]`-guarded readers `:164-174`, journal via `cap()` + rc classification
`:322-329`, tmux via `cap()` `:552`), which shows the intended contract already
exists in the codebase — the defect is only in the three bare pipeline assignments.

## Countermeasures that fit this codebase (evidence-backed)

1. **Capture-with-rc.** `cap()` (`tools/mori-census.sh:157-162`) runs `set +e`
   around the capture, records `CAP_RC`, then re-enables `set -e`. The git call for
   the same probe already uses it (`:511`); the three crashing sites bypass it.
   A hardened site must check the rc and fall through to a graded state.
2. **Grade `unavailable`, never abort.** `corpus/knowledge/silence-grading-r2.md:99`
   (row 1: unreadable/missing input → `unavailable`) is the r2 contract; exit 2 is
   the only reserved setup code (`:583-587`), so a crash must not borrow rc 1's
   "DRIFT" meaning. `SKILL.md:43` states the same boundary: a missing surface is
   `unavailable`, never unhealthy.
3. **Oracles assert the evidence line, not the exit code.**
   `tools/mori-silence-cases.sh:350-359` is the pattern that made this defect
   visible: "no verdict line" is reported as a distinct failure class. Any consumer
   of this gate should do the same (verify the `MORI_CENSUS:` line), because rc=1
   alone is ambiguous.
4. **Canary sweep.** Make each input surface unreadable once (`chmod 000` on the
   dir, run, restore) and require the verdict line. That sweep is exactly how
   A/B/C were found; it is cheap and re-runnable.

## Applying it (any lane)

- Grep your gate for `$( … | … )` assignments under `set -e`/`pipefail`; each one
  whose producer can fail environmentally is a potential silent abort. Guard it
  with an explicit rc capture, or `|| true` plus an rc check — never a bare pipe.
- Remember the rc semantics: without `pipefail`, downstream success masks a producer
  failure; with `pipefail`, the same pipeline aborts under `set -e`. Both directions
  have surprised this file's author at different times.
- Reserve a distinct exit code (or a mandatory verdict line) for "the gate itself
  failed", so rc-only consumers cannot confuse it with a graded verdict.

## Limits

- The repros use controlled temp roots and `chmod 000` to simulate unreadable
  input; no live fleet path was observed unreadable at measurement time. The class
  is reachable whenever a lane repo, wave subdirectory, or `.ufo/state` loses
  readability (ownership change, stale root-owned file, IO error).
- This note pins r1 `e3073a2b…`. The round-3 wave registers hardening of `:517`
  and `:283` to `unavailable` grading; if the cutover lands, re-run the A/B/C
  canaries against the new sha and confirm `:220` too — it was not in the wave
  brief at this note's clock.
- **Cutover state measured 2026-10-15T16:50–16:54Z**, latest snapshot
  `35c9a0c6…` (working tree; stable across each measurement but the file moved
  between checks — `e2056b1d…` → `d9e598ad…` → `952f3ba6…` → `35c9a0c6…` — so
  treat this as a snapshot, not a final revision):
  - Fixed at that sha: the lane-repo read path — scenario R (readable ledger +
    `launch kagi round=7` + `.ufo/state/kagi.round=7` + an old non-lane commit +
    `chmod 000` on the repo `.git`) grades
    `SURFACE lane.kagi: unavailable (… basis=row-1 reason=git-unreadable rc=128 …)`
    with a verdict line; and the `:283` wave-age pipeline is now `cap find` +
    rc branch (`:296-302`), so canary C (unreadable wave subtree) no longer
    crashes.
  - Still open at that sha:
    (a) `:227` `state_n=$(find "$STATE_DIR" -maxdepth 1 … | wc -l | tr -d ' ')`
    is still a bare pipeline — canary B (`.ufo/state` `chmod 000`) exits rc=1
    with **0** verdict lines and 0 B stderr; the traced run's last command is
    `+ state_n=0`.
    (b) The waves unread-age disclosure landed at `35c9a0c6…`: the surface
    detail now carries `age_unreadable=$n_age_unread` (`:320`), measured
    `age_unreadable=1` for the unreadable-subtree scenario. That scenario still
    grades `SURFACE waves: ok` with no `WAVE_UNSETTLED_AGE` finding, while its
    readable twin fires `drift` + `age_s≈147k` — the skip is now visible in the
    detail line; whether an unprovable age should leave the surface `ok` is a
    policy question for the spec's calibration axis, not a claim of this note.
  Re-run these canaries against the final cutover sha; the class is closed only
  when every unreadable input yields a verdict line and no site silently drops
  the check it could not perform.
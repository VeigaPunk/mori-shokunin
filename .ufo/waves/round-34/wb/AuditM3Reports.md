measured 2026-10-23T07:57:15Z
# AuditM3Reports — re-check of the evidence draft mistake M3 cites

Object audited: `/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_lessons_round-34.md:88-94`
(M3: "counter sensitivity to rule order was never measured before data"), which rests on
`.ufo/waves/round-34/wa/MutLiveArm.md`, `wa/CritGeneratorCoverage.md`,
`wa/LabFixturePartStacked.md`. Re-checked against frozen counter
`.ufo/waves/round-34/count-c1-a1.py` (sha256 `c14c3494…b181e2`, byte-identical in the lane
and in my clone) and tool `tools/mori-disk-rate.py` at `8d56809` (sha256 `370932de…fee76b`).
Scratch `S = /fast/scratch/hyaku/mori-r34/a3-AuditM3Reports`; sandbox clone `S/clone`.

## Claim 1 — measured-time live mutant survives the frozen counter

MutLiveArm.md:25 claims `live=ok; C1=met; exit 0` for a mutant that divides live rates by
integer measured elapsed ms while keeping nominal `interval_ms` metadata.
Static re-check: `fed_live` compares tool output to `oracle(text_a, text_b, "/sys", ms)`
with `ms = 400` (count-c1-a1.py:312, 364-365) — an exact `same()` comparison
(:233-238), so the mutant is observable; `live()` bounds the rate only above
(:273-278). The mutant passes `fed_live` only because the FIFO EOF fast-path makes
read 2 end within the same millisecond the nominal 400 ms sleep ends, so measured
elapsed truncates to 400 and output is identical.
My re-run: own equivalent mutant (commit `b81050e8ad01eb0ff25bb4bf39d7bf9df502cc0e`
in `S/clone`, tool diff = elapsed-ms divisor + nominal metadata), run
`timeout --kill-after=5 600 prlimit --as=1073741824 -- python3 .ufo/waves/round-34/count-c1-a1.py b81050e… --repo S/clone`
→ `fixed_pass=12/12 random_pass=300/300`, `coverage=ok`, `live=ok`, `C1=met`, exit 0,
seed 6750019854611181426, ~12 s.
Caveat (does not change verdict): survival is timing-fragile — on a loaded run where
the second read ends ≥1 ms late, elapsed truncates to ≥401 and the result would be
`fed-mismatch`/`C1=unmet`. The measured evidence is one run, as MutLiveArm.md:64 states.
VERDICT: agree — measured-time survives (verified by my own re-run, fragile to elapsed
crossing a millisecond boundary).

## Claim 2 — mountinfo-path live mutant survives the frozen counter

MutLiveArm.md:26 claims `live=ok; C1=met; exit 0` for a mutant that reads
`/proc/self/mountinfo`, picks the first procfs mountpoint, then its `diskstats`.
Static re-check: `run_tool` bind-mounts only `/proc/diskstats` (fed) and tmpfs-hides
`/home`, `/fast` (count-c1-a1.py:219-222, 339-344); `/proc/self/mountinfo` inside the
namespace still lists `/proc` as a proc mount, so the mutant resolves
`/proc/diskstats` → the FIFO for fed, the real file for live. No arm challenges an
alternate proc view.
My re-run: own equivalent mutant (commit `d82d58015799a9c72060ecfbc7959c527969c0ad`,
`read_live_samples` resolves diskstats via mountinfo), same counter command
→ `fixed_pass=12/12 random_pass=300/300`, `coverage=ok`, `live=ok`, `C1=met`, exit 0,
seed 9284307865180652656, ~11 s.
VERDICT: agree — mountinfo-path survives (verified by my own re-run).

## Claim 3 — the generator never draws overlapping class markers

CritGeneratorCoverage.md:66-72 claims each drawn device carries at most one effective
marker. Re-checked in counter source: a partition gets only a `partition` file
(count-c1-a1.py:171-174 — it skips `slaves/` entirely); a disk gets `device` plus an
empty `slaves/` dir (:171-172, 175-176) — empty `slaves` is not a marker since
`classify` requires `os.listdir(slaves)` non-empty (:65-66); a stacked name gets only
non-empty `slaves` (:177-178 populates it only for names in `slaves{}`); virtual and
`xyz9` get an empty `slaves/` or nothing. No `cls` entry takes two classes
(:152-165). So no drawn device carries two markers; R3's order (:63-69) is never
exercised at a branch point.
VERDICT: agree.

## Claim 4 — the generator never draws symlinked entries or a partition-with-slaves

LabFixturePartStacked.md:100-105 claims no `os.symlink` in the counter and no
partition with `slaves`. Re-checked: `grep -n 'os.symlink|symlink' count-c1-a1.py` →
no match (every `class/block/<n>` is a real dir via `os.makedirs` at :169-170, and
marker entries are regular files); partitions skip `slaves/` by `if c != "partition"`
at :171-172.
VERDICT: agree.

## Verdicts on M3's three cited reports

- MutLiveArm.md: its two survivor claims reproduce in my own sandbox; its three kills
  are consistent with `fed_live`'s two-read/interval/exact-output requirements
  (:356-365). Its receipts are attempt-2 scratch; claims 1-2 are independently
  confirmed above.
- CritGeneratorCoverage.md: generator-cause citations (:171-178 markers, :189-192
  absent/corrupt gating) match the counter source I read.
- LabFixturePartStacked.md: generator claims match counter source; its fixture
  verdicts concern the tool, not the counter, and were not re-run (scope).
VERDICT: agree — claim 1 (measured-time survives; re-run C1=met)
VERDICT: agree — claim 2 (mountinfo-path survives; re-run C1=met)
VERDICT: agree — claim 3 (no overlapping class markers; count-c1-a1.py:152-178)
VERDICT: agree — claim 4 (no symlinked entries, no partition-with-slaves; :169-178, no os.symlink)

## Corrected M3 wording

None required — every factual claim M3 rests on re-checked true. Optional precision:
append "(measured-time's survival is timing-fragile: it holds only while the measured
live window truncates to the nominal interval, which a ≥1 ms late second read would
defeat)" if the L1 wants the fragility on record; MutLiveArm.md:64 already hedges to
single-run.

## Containment note (disclosure)

During setup, an `edit` anchored to the wrong path and transiently modified the lane
file `tools/mori-disk-rate.py`; it was immediately reverted to the identical 12 lines.
Verified byte-identical after: `sha256sum` = `370932deb525b95135f0c30e4caaf2666b95c6feeffe76b70f06b48c09caa74b`
and `git status --porcelain tools/mori-disk-rate.py` empty. No lane/index mutation
remains; the mutants exist only as commits `b81050e…`, `d82d580…` in `S/clone`.

## Tooling / limits

No tools installed or updated; pacman not invoked (host-wide pause). Commands under
`timeout` (counter runs ≤600 s via `timeout --kill-after=5 600`, prlimit 1 GiB).
No subagents, no background jobs. Clone (~352 MB) retained under `S` as evidence.
Report written only at the assigned path.

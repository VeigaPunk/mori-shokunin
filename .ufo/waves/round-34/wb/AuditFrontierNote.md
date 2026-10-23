measured 2026-10-23T08:00:05Z

# AuditFrontierNote — attack on the attempt-2 draft "Round-34 Frontier note — FR6 narrowed, not closed"

Seat: MoriR34A3.AuditFrontierNote (reviewer, leaf). Object: last section of
`/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_README.md:540-555` (uncommitted attempt-2 draft, audited as the
object, never as evidence). Base refs: `f10a320d` (entering tip), `fd2521351c6cef47384aef30afbe1e4db7e6912e`
(committed tip). The note has 9 sentences; each gets a `VERDICT:` line. Reads only; the lane was not written
except this report.

## Sentence-by-sentence

**S1** "The FR6 row above is byte-unchanged by this round."
Verified. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff f10a320d fd2521351c6cef47384aef30afbe1e4db7e6912e
-- corpus/README.md` → empty output, exit 0. The draft's FR6 row (draft `:340`) is byte-identical to the committed row
(`git show fd2521351…:corpus/README.md` `:340`, verified by `diff` → `IDENTICAL`): "…still frontier: a two-sample
census arm, and the device-mapper double count, observed on this host but not sourced."
VERDICT: agree

**S2** "Round 34 lands the two-sample write-rate operation as a separate read-only tool, `tools/mori-disk-rate.py`
(two `/proc/diskstats` readings, `/sys/class/block` classes, per-device states and rates, a whole-disk host total;
rules R1–R7 in `.ufo/waves/round-34/contract.md`, sources S180–S198)."
Matches the tool's own docstring at `fd2521351` (`tools/mori-disk-rate.py:5-16` CLI, `:30-77` rules R1–R7 restated).
Read-only verified directly: the only `os.open` is `O_RDONLY` (`:121`); only output write is `sys.stdout` (`:294-295`);
LabStackedHost §6 strace shows writes only to fd 1. Contract `.ufo/waves/round-34/contract.md` §C1 holds R1–R7 and the
frozen interface. Caveat (not a defect): the sources the *rules* cite are S180–S183, S186–S187, S191–S193; S180–S198 is
the round's whole admitted block for this ground — same shorthand as `SKILL.md:828` ("Sources S180–S198; the frozen
rules R1–R7").
VERDICT: agree

**S3** "It is an operator-run probe, not a census surface: `tools/mori-census.sh` does not call it and keeps its
since-boot average."
Verified. `git show fd2521351…:tools/mori-census.sh | grep -n "disk-rate\|disk_rate\|mori-disk"` → the only hit is a
fixture comment at `:3199` ("r7 disk-rate fixtures: one diskstats line for the df stub's device"). The census's own
disk probe reads `/proc/diskstats` field 10 since boot (`:31` "since-boot write average per target device
(/proc/diskstats)", `:1887` field 10 = sectors written, `:4461` check name 'disk: since-boot write average from
diskstats'). `SKILL.md:831` instructs the operator to run `python3 tools/mori-disk-rate.py --interval-ms N` — the
"operator-run probe" label is accurate.
VERDICT: agree

**S4** "Its claim did not verify: a post-data shortcut met the frozen counter (`lessons/round-34.md` M2), so the
tool's correctness rests on the wave-A attacks, not on the counter."
Consistent with the attempt-2 lesson draft (audit object, not evidence):
`/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_lessons_round-34.md:62-70` describes CritPostDataShortcut meeting
`C1=met` post-data (`evidence/ctl-postdata-shortcut/`), and `:79-83` is M2 (label-keyed, harness-keyed shortcut missed
by the 16-control pre-data battery). Citation `lessons/round-34.md` matches the lane's `corpus/lessons/` layout once
landed. The inference "correctness rests on wave-A attacks" is the lesson's own C1 closure ("not verified (honest
stop)", lesson draft `:57-63`); other seats audit the shortcut rescore (peers: CritShortcutRescore).
VERDICT: agree

**S5** "Still frontier: a two-sample census arm."
Supported by the cited wa report's verdict: `wa/ExecLatencyBudget.md` §7 answers "May FR6 leave the frontier? No" —
the census arm is unaffordable at every measured interval. "Narrowed, not closed" in the heading is also consistent:
the arm is measured-deferred and the dm count is restated as unsourced, while the row's other half (a census-embedded
two-sample arm) stays open.
VERDICT: agree

**S6** "Measured in round 34 (`.ufo/waves/round-34/wa/ExecLatencyBudget.md`): the tool's wall time is about 128 ms at
a 100 ms interval and about 243 ms at 200 ms, against the round-8 bar of 50 ms (`knowledge/surfaces-r8.md:47-48`), and
intervals short enough to fit read zero."
Numbers match the cited report: best live-100 batch median 127.93 ms → "about 128 ms"; live-200 batch-E median
242.65 ms → "about 243 ms" (§3). The 50 ms bar is verbatim at `surfaces-r8.md:47-48` ("implement a windowed
(two-sample) rate iff the 0.2 s variant adds < 50 ms median wall time"; line numbers confirmed by `grep -n` at
`fd2521351`). Per the wa report §1, r8's unit of comparison is the whole two-sample block's added wall time, dwell
included (r8 measured 208–229 ms vs the 50 ms bar), so comparing the tool's live wall (dwell included) against 50 ms
is the correct unit — no apples-to-oranges defect. "Intervals short enough to fit read zero": intervals 1/5/10 ms →
`host_write_Bps` 0 in 5/5 runs each; at 15–20 ms the reads are nonzero-but-noise (§5b wording: "zeros or 10²–10⁴×
noise"), so the clause is a fair compression with a minor sharpening loss at the 15–20 ms boundary.
DEPENDENCY: every number in this sentence (128, 243, zero-floor) is wa-measured; peer
`MoriR34A3.ExecLatencyRemeasure` is re-measuring. If the remeasure's numbers differ materially, this sentence must
carry the new values; its load-bearing structure (dwell ≫ 50 ms) is unlikely to flip.
VERDICT: agree

**S7** "Still unsourced: the device-mapper double count."
Verified against all admitted sources on this ground. Sources S180–S198 are admitted
(`git show fd2521351…:corpus/SOURCES.md` rows `:186-204`, status `mined`/`on-release`). I grepped every evidence copy
`corpus/evidence/sources-r33/S180-S190.src` and `sources-r34/S191-S198.src` for
`mapper|dm-|stacked|holder|slave|twice|double.?count|roll.?up|account`: S192 (holder.c `:46-50`) documents only the
`slaves`/`holders` symlinks — no I/O accounting statement; S183 (part_stat.h) states the *partition→whole-disk*
roll-up, a different mechanism (a partition's sectors are added to `bdev_whole`, not a dm line repeating a slave's);
S196 mentions dm only for sysfs detection (`get_dm_wholedisk`, `sysfs_devno_is_dm_*`), not accounting. No admitted
source states that a write to a dm device is also accounted on its underlying devices. So the FR6 row's "observed on
this host but not sourced" remains true.
VERDICT: agree

**S8** "Round 34 observed it again on this host (dm-0's delta equals its slave's; a write through dm-0 appears once
in the whole-disk total and twice in a sum over every line, `.ufo/waves/round-34/wa/LabStackedHost.md`)".
Partly wrong in a numeric detail. The cited report supports "dm-0's delta equals its slave's" (§5: dm-0 Δ = 4672 =
Δ(nvme0n1p2)) and "appears once in the whole-disk total" (`host_write_Bps` counts nvme0n1 once, probe table §5). But
"twice in a sum over every line" contradicts the same report's own probe table: a write through dm-0 lands on
**three** lines — dm-0, nvme0n1p2 and nvme0n1 each show `write_Bps` 61613397 — so a literal sum over every line counts
it three times, not twice. The report's "2.000×" figure is the all-devices sum vs whole-disk sum on a *different* run
shape "in which every device was active" (aggregate accident of that run's mix: dm-vs-disk layers vs one-copy direct
writes), not the per-write line multiplicity. The draft imported the 2× aggregate as a per-line claim. Direction of
the sentence (the dm layer duplicates its slave's count; the host total excludes it) is right; the line-sum
multiplicity is misstated. Fix: "three times in a sum over every line (dm-0, its partition slave and the whole disk)",
or quote the report's 2.000× as the all-devices-vs-basis aggregate on a fully-active run.
DEPENDENCY: peer `MoriR34A3.ExecStackedRemeasure` is re-measuring the stacked-host claim; if its per-layer
multiplicity differs, this sentence needs the new figure either way.
VERDICT: disagree

**S9** "…so the tool's host total excludes stacked devices by class, not by a sourced rule."
Accurate and fairly stated. `host_basis` is class `disk` only (R7; LabStackedHost §3: dm-0 can never be `disk` — no
`device` entry — and is `stacked` via non-empty `slaves`). The exclusion is real and structural, but the *reason* —
avoiding the unsourced double count — is a lane gloss: S192 documents symlinks only. The note's phrasing ("by class,
not by a sourced rule") is exactly right.
VERDICT: agree

## Re-measurement dependencies (summary)

- S6 (128 ms / 243 ms / zero-floor): depends on `MoriR34A3.ExecLatencyRemeasure` — wa numbers are internally consistent
  and correctly applied; replace values if the remeasure differs.
- S8 (dm delta equality, per-layer multiplicity, once-in-total): depends on `MoriR34A3.ExecStackedRemeasure` — the
  "twice" defect stands against the cited wa table regardless; the remeasure can only change the correct number.
- S4's counter premise (post-data shortcut met P-C1-A1): audited elsewhere (peer `CritShortcutRescore` /
  `ExecCloneRerun` for counter reruns); I verified only that the note's claim matches the lesson draft's M2.
- No other sentence depends on wave-A measurements; S1–S3, S7, S9 are verified against committed bytes and source text.

## Findings

1. (low, factual) S8: "twice in a sum over every line" misstates the wa report's per-layer result — a dm-0 write
   appears on three lines (dm-0, nvme0n1p2, nvme0n1), not two. Report at `wa/LabStackedHost.md` §5 probe table and §5
   para 1. Suggest the three-line phrasing or the correctly-attributed 2.000× aggregate.
2. (nit) S2's "sources S180–S198" spans the round's whole admitted block; the rules themselves cite S180–S183,
   S186–S187, S191–S193. Same convention as `SKILL.md:828`; acceptable, flagging only for the record.
3. (nit) S6's "intervals short enough to fit read zero" compresses §5(b)'s "zeros or 10²–10⁴× noise" — at 15–20 ms
   readings are nonzero noise, not zero. Load-bearing claim (a 50 ms-fit arm measures nothing) unchanged.

## Residual risk / verification gaps

- The frontier note cites wa scratch reports (ExecLatencyBudget.md, LabStackedHost.md) that are themselves attempt-2
  uncommitted output; I audited the note's fidelity to them plus the frozen/committed anchors, and the numbers are
  being re-derived by the remeasure seats — a citation to wa scratch is a lead until those land.
- S4's "correctness rests on the wave-A attacks" is a characterization consistent with the lesson's honest-stop
  closure; whether the wave-A attacks suffice is the wave-B re-derivation's question, not this note's.
- "no admitted source states it" is checked against SOURCES.md rows and the evidence `.src` copies at `fd2521351`
  (grep terms above, including S192/S196 full-text passes); I did not exhaustively re-read every admitted source
  outside this ground (S001–S179) for a stray dm-accounting remark [INFERENCE: unlikely, they cover other grounds].

## Tools

No tool installed or updated (tool: none · version: n/a · channel: n/a · reason: all checks used read-only `git
show`/`diff`/`ls-tree`, `grep`, `sed`, `diff` on committed bytes and scratch copies; pacman paused host-wide per wave
rules). Scratch: none written (report only). No processes left running.

# LiveMoriR18W1 — C2 member-level falsification: mori round-18 wave1

**Verdict: HOLDS.** The settlement scan's r18-w1 member classification reproduces the
manual ground truth exactly: set difference both ways is EMPTY (15/15 missing names
identical), all 68 per-member name|status pairs identical, counts identical.

## Attack

Command (both runs):

```
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-wave-settlement.py scan \
  --lane-root /home/vgpnk/Projects/shokunin/mori-shokunin \
  --fleet-root /home/vgpnk/Projects/shokunin
```

Run 1: exit=1, stderr empty (0 bytes). Run 2 (determinism rerun, output to
/tmp/rerun-r18w1.json): exit=1. Exit 1 is contract-correct, not a failure: the mori lane
contains historical partial/unsettled waves (contract.md:87 — "Exit: 0 every discovered
wave settled or no-spawn; 1 any other state").

Dispatch identity: scan's `dispatch_sha256` 84bfb3dd29a23ec5c8715478d316ab89df6aba4e96fb6f81b7ad81ba51ac0d7e
= my `sha256sum` of `.ufo/waves/round-18/wave1-dispatch.json`; size 135847 = Gt's recorded
135847 (GtMoriR18W1.md:122). Tool read the same bytes Gt describes.

## Sets (the asked set difference, both ways)

Tool `missing` (`.waves[] | select(.dispatch_path == ".ufo/waves/round-18/wave1-dispatch.json") | .missing[]`, n=15):
AdjDeadSeatCrossCheck, AdjOmpRetryDocs, AdjRetryRecoveryShape, AdjSeatBreachDetect,
AdjSeatNaming, AdjTranscriptTailBounds, AdjSeatLiveEvidence, AdjWave1SpecDispatch,
ScoutAttemptReceipts, SweepR1314Md, SweepR15Md1, SweepR16Md1, SweepR17Build1,
SweepR17Falsify1, SweepR17Falsify3.

Gt missing (transcribed from the table, GtMoriR18W1.md:14-83; rows e.g. :22, :23, :25, :70), n=15.

- A = tool \ gt (`comm -23`, LC_ALL=C): **EMPTY**
- B = gt \ tool (`comm -13`, LC_ALL=C): **EMPTY**
- Intersection: 15/15

## Counts (tool vs Gt)

| Count | tool (r18-w1 entry) | Gt (GtMoriR18W1.md:89-94) |
|---|---:|---:|
| present | 53 | 53 |
| missing | 15 | 15 |
| empty | 0 | 0 |
| misrooted | 0 | 0 |
| unsafe / unparsed | 0 / 0 | 0 no-trailer (Gt has no unsafe class) |
| stub | 0 | (no stub class in Gt) |
| total members | 68 | 68 |
| state | partial | — (53+15=68) |

## Full member-level check

68/68 name|status pairs IDENTICAL: `diff` of the tool's `.members[] name→status` against
the Gt table transcribed to `gt-status.tsv` (sorted LC_ALL=C both sides) is empty.
Artifacts: `falsify/LiveMoriR18W1/{r18-entry.json,tool-status.tsv,gt-status.sorted.tsv,status.diff}`.

Cross-checks:

- Tool missing set == `.ufo/waves/round-18/evidence/wave1-dead-seats.json` 15 names
  (`comm -3` empty) — reproduces Gt's set-identity claim (GtMoriR18W1.md:111).
- Filesystem spot-checks (stat): RetentionGate.md regular 4021 B, CriticC1Metric.md
  regular 7757 B (Gt:71), ScribeLessonDraft.md regular 17423 B — bytes equal Gt's column.
  AdjDeadSeatCrossCheck.md, SweepR17Build1.md, ScoutAttemptReceipts.md absent under the
  lane build dir AND under /home/vgpnk/.ufo/waves/round-18/build/ → misrooted=0
  corroborated (Gt:96).
- Determinism: the serialized r18-w1 wave entry is byte-identical across the two scans
  (sha256 a0fa39eb75b66c39cb4aa20caceddb17d5a1a68b9369c2227a9a1e8ed9d30797 both).

## Residual risk / disclosures

- The lane tree is live: between run 1 and run 2 lane totals moved (waves 12→14, members
  738→741, stub 63→54, present 586→599, unique dispatch sha 12→14, unsafe 0→1,
  ignored_json 486→554, unreadable_json 3→2) — sibling seats writing concurrently, as the
  knowledge note warns. The r18-w1 entry itself was byte-identical across runs, so the
  movement did not touch my comparison target. The one rerun `unsafe` belongs to another
  wave (out of scope, not investigated).
- Self-pollution: my scratch JSONs under `.ufo/waves/round-20/falsify/LiveMoriR18W1/`
  are under `.ufo/waves/` and are counted in `ignored_json`/`unreadable_json` of both
  runs (run 1 saw the empty redirect target). Member/missing figures for r18-w1 are
  unaffected. Scratch is confined to `falsify/LiveMoriR18W1/` and `/tmp`.
- Gt was derived earlier the same day (2026-10-21); agreement on all 68 members now shows
  the r18 build files did not move in between.
- No tools installed or updated (jq/stat/comm/python3 preexisting; jq used = /usr/bin/jq
  1.8.2, not jaq).

## Verdict basis

C2's claim that the scanner reproduces the non-author ground truth survives a member-level
attack on mori round-18 wave 1: `missing` 15/15 both directions, `present` 53/53, 68/68
statuses, misrooted 0/0, dead-seat cross-set equal, entry deterministic across runs.
Nothing observed contradicts the frozen contract semantics (contract.md:74-88).

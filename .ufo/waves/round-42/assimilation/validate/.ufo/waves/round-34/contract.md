# mori round 34 — frozen claim contract (L1 MoriR34, attempt 1)

Base (entering tip): `f10a320d9056d19a6d007420df49d7b16a3bf857`. Written and committed with `count-c1.py` and the
before receipt before any seat of this round exists. Nothing in this file is amended after a seat scores; a miss is
reported, never re-scaled.

Anti-loop: round 32 (freshness, source rows) and round 33 (depth, FR6 decision table) were rejected. This round claims
neither axis: C1 is coverage (a new tool operation), C2 is an exploratory calibration claim. Round-33 routed defects
2–8 are repairs, not claims; item 1 (counter discrimination for the next depth claim) is answered by QUALITY 98 (C2).

## C1 — coverage: FR6's two-sample write-rate arm becomes a lane tool operation

Surface moved: `corpus/README.md` Frontier row FR6 says "still frontier: a two-sample census arm". C1 lands the
operation `tools/mori-disk-rate.py`, which reads two `/proc/diskstats` samples and the block class tree in sysfs and
reports per-device write rates, device classes and a host total. Command that shows the surface unmoved:
`git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree <rev> tools/mori-disk-rate.py` prints nothing (the counter
prints `tool=absent`). Axis named by the surface it changes: a new tool operation and its edge classes (coverage), not
the number the counter prints.

### Frozen interface

```
python3 tools/mori-disk-rate.py --a FILE --b FILE [--sysfs DIR] --interval-ms N   # offline: two saved samples
python3 tools/mori-disk-rate.py [--sysfs DIR] --interval-ms N                     # live: /proc/diskstats, sleep N ms, re-read
```

`--sysfs` defaults to `/sys`. Stdout is one JSON object with at least these keys:
`{"interval_ms": N, "devices": {"<name>": {"class": C, "state": S, "write_Bps": int|null}}, "host_basis": [...],
"host_write_Bps": int|null}`; exit 0 whenever the JSON is produced. Detection and report only: the tool reads
`/proc/diskstats` and sysfs and writes nothing.

### Frozen rules (the oracle in `count-c1.py`; source per rule)

- R1 A line names a device by its 3rd whitespace token; a line with fewer than 3 tokens is ignored.
- R2 A line is valid only with 14, 18 or 20 tokens and every token except the name an unsigned decimal; sectors
  written is token 10 (S187 field counts and field 10; S180).
- R3 Class from `<sysfs>/class/block/<name>`, in this order: no such directory → `unknown`; a `partition` entry →
  `partition` (partition-only attribute: `block/partitions/core.c` v7.2, row opened this round); a non-empty `slaves`
  directory → `stacked` (`block/holder.c` v7.2 slaves/holders links, row opened this round; S182 creates `slaves` for
  every disk, so only a non-empty one marks stacking); a `device` entry → `disk` (`drivers/base/core.c` v7.2 creates
  the `device` link only for a device with a parent that is not a partition, row opened this round); otherwise
  `virtual` (lane rule: a parentless, unstacked block device such as loop, zram or ram).
- R4 Devices = names in sample A ∪ names in sample B ∪ entries of `<sysfs>/class/block`.
- R5 State precedence: `bad-line` (a bad line in either sample) > `absent` (no line in either; S182 skips zero-size
  partitions) > `gone` (A only) > `new` (B only) > `reset` (B sectors < A sectors; S181 resets) > `ok`.
- R6 An `ok` rate is `(B − A) * 512 * 1000 // interval_ms` bytes per second (S186/S187 512-byte unit); every other
  state has `write_Bps` null (r33 rows 4 and 9: unavailable, never zero).
- R7 `host_basis` = sorted names of class `disk`; `host_write_Bps` = the sum of their rates when the basis is non-empty
  and every basis device is `ok`, else null (S183: a partition's sectors are added to its whole disk; holder.c:
  a stacked device maps onto devices already counted; virtual excluded by lane rule).

### Predicate P-C1 (same sentence in `count-c1.py` docstring; receipt label `C1=met`)

At the measured revision, tools/mori-disk-rate.py exists, never names the lane's .ufo tree or this counter, matches
this counter's oracle exactly on the 12 fixed-seed scenarios and on every one of 300 scenarios drawn from a fresh
random seed (the drawn set must exercise all six states and all five classes), and its live run exits 0 with JSON
whose classes match /sys and whose ok rates are bounded by the counter's own outer /proc/diskstats readings.

Counting command: `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/count-c1.py <rev>`
(exit 0 `C1=met`, exit 1 `C1=unmet`). Before (`f10a320d`): `tool=absent C1=unmet` (`evidence/c1-before.txt`).
Declared after: `C1=met` at the landed tip, one fresh-seed run by the L1 with its measured time in the receipt.
Kill rule: `C1=unmet` at the landed tip in the L1's run, or in any fresh-seed re-run by the closure, is a miss; the
counter, rules and seed count are not changed after any seat scores.

### Pre-data controls (built by fresh seats in sandboxes, scored under this counter, receipts committed before data)

Each leg-rejection shape is mapped to a control or ruled inapplicable with a reason:

| shape (leg precedent) | control | expected |
|---|---|---|
| skip-work / do-nothing (kumitate r44) | C-absent: base tip, no tool | unmet |
| content-free (tsukuroi r30–r32) | C-junk: prints `{}`; C-allnull: every device listed, every rate null | unmet |
| no-decision (mori r33 glossary) | C-naive: one rate per line, every class `disk`, no state handling, host = sum of all lines | unmet |
| no-decision, partial | C-alldisk: correct states and rates, every class `disk` | unmet |
| no-decision, partial | C-noreset: correct classes, a lower counter reported as a rate (wrapped or negative) | unmet |
| wrong surface | C-sinceboot: rates from sectors / uptime (the existing census average) | unmet |
| label-keyed (kumitate r44) | C-labelkey: answers the 12 fixed-seed scenarios from a table keyed on input bytes, `{}` otherwise | unmet |
| server echo (kama r26) | C-echo: imports this counter's oracle by path | unmet (guard) |
| wrong sysfs root | C-sysblock: classifies from `<sysfs>/block/<name>` instead of `class/block` | unmet |
| copy observed column (mado r24) | inapplicable: no expected output exists on disk while the tool runs (oracle computed in memory after) | — |
| rows deleted after judgment (kotodama r59) | inapplicable to C1: no judge; the judged object is the tool bytes at the landed tip | — |

Residuals declared before data: (a) a tool built by copying this counter's oracle functions meets P-C1 (the L1's
positive control does, `evidence/c1-posctl.txt`); such a tool computes the declared rates from its inputs, so it is
the claimed operation, not a skip. The lane tool is written by a seat that is not given this counter; that is process
evidence, not part of the predicate. (b) The live arm bounds ok rates and checks classes; it does not prove a live
rate exact. (c) The oracle's rules are the author's reading of the cited sources; wave 2 re-checks each rule against
its source, and a contradicted rule is reported as a defect of the claim, not fixed by amendment.

## C2 — calibration (exploratory): the pre-data shortcut battery as a lane rule

What it improves: the lane's self-assessment of a claim before data. Round 33 froze a counter whose nine pre-data
controls tested sourcing and judging but not the claimed depth, so a no-decision glossary met it after data (closure
§3.2 item 4). C2 lands QUALITY criterion 98: before data, each claim maps every leg-rejection shape to a control or a
stated inapplicability and commits the scored receipts; shown able to fail on round 33's contract. No counting
command; it verifies only as `unprovable-but-better` with a named non-author reviewer on record, otherwise it lands
`unprovable`. Its axis score does not change.

## Routed round-33 repairs (closure §8; not claims)

2 entry rows 3, 6, 7, 13 (append-only revision with the cited lines, re-judged by a non-author judge); 3 row 8 "4.18"
boundary marked; 4 SKILL line 820 aligned with row 14 (append-only correction); 5 lesson round-33 §1 vs `## Judges`
correction; 6 lesson :79 / report :52-53 word-edit correction; 7 receipt time labels (corrected; this round's receipts
carry `date -u` output); 8 CtlLocatorStale and the S117 preamble overstatement noted. Item 1 → QUALITY 98 (C2).

## Containment

Seats never run git or jj writes in the lane or the fleet repo; sandbox git only in clones under
`/fast/scratch/hyaku/mori-r34/`. The L1 lands lane bytes only through `jj-lane.sh`.

## Amendment A1 (pre-data; after the C0 control wave, before any data seat)

Wave C0 (one ordinary `task` call, 10 seats: CtlJunk, CtlAllNull, CtlNaive, CtlSinceBoot, CtlEcho, CtlCheapest as
critic; CtlAllDisk, CtlNoReset, CtlLabelKey, CtlSysBlock as mutation-tester) built the controls of the table above in
sandboxes and scored them under the frozen `count-c1.py` (reports `c0/*.md`). Three shapes met P-C1:

- C-emptylive (CtlCheapest, `2a31899`): a correct offline arm whose live mode prints an empty device map; the live arm
  only checked the devices a tool chose to report. A variant reporting rate 0 from one reading (`8e7c686`) also met.
- C-echo v2/v3 (CtlEcho, `e665fa5`, `c339715`): the tool loads this counter's oracle by a path spelled without the
  guarded strings; the `.ufo`/`count-c1` guard is a string test only. v3 also undoes a tmpfs hide by `umount` as
  namespace root.

So the counter, not the target, was wrong. A1 adds conditions and removes none (`diff count-c1.py count-c1-a1.py`):
(1) every tool run happens in a user+mount namespace with tmpfs over `/home` and `/fast`, then every capability is
dropped (`setpriv`), so the tool cannot read the lane, the counter or a sandbox clone (CtlEcho's own tested fix);
(2) the real-host live JSON must list every entry of `/sys/class/block` and every device valid in both outer
readings, each such device whose counter did not fall reported `ok` with an integer rate; (3) a fed live run serves
two generated samples over the host's real device names through a FIFO bound on `/proc/diskstats`, and the tool
must read twice at least 0.9 × interval apart and match the oracle exactly.

### Predicate P-C1-A1 (same sentence in `count-c1-a1.py` docstring; receipt label `C1=met`) — the judged predicate

P-C1, and the tool runs with /home and /fast hidden from it and every capability dropped, and its live JSON lists every
entry of /sys/class/block and every device whose line is valid in both of the counter's outer readings, each such
device whose counter did not fall being reported ok with an integer rate, and in a fed live run (the counter serves
two generated samples through /proc/diskstats, real /sys) the tool reads the file twice at least 0.9 * interval_ms
apart and its JSON matches the oracle exactly.

Counting command: `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/count-c1-a1.py <rev>`.
Before (`f10a320d`): `tool=absent C1=unmet`. Declared after: `C1=met` at the landed tip; kill rule as for P-C1.

Receipts (`evidence/c1-controls.txt`, measured 05:13:09Z): all 16 negative controls `C1=unmet` under P-C1-A1 (three of
them met P-C1); both positive controls `C1=met` under both — the L1's oracle copy (`cf987fa4`) and CtlSysBlock's
contract-correct baseline written from the contract text by a seat (`929f48e`), which shows the contract alone
suffices to meet the predicate. Added shapes (controls table): empty or fabricated live arm (C-emptylive), single
reading (C-zero-singleread), runtime echo (C-echo v2/v3, C-echo-ppid). Reading note: the receipt's
`states_seen`/`classes_seen`/`coverage` line is the generator's coverage over the oracle's expected devices, not the
tool's; it guards against a drawn set that skips a class (CtlJunk, CtlAllNull). Residual (CtlSinceBoot): a drawn
scenario with no `ok` device lets a wrong-rate tool agree by accident; the 12 fixed seeds each hold 2–10 `ok` devices,
so the rule still rejects it. Residual: a copy of this counter outside `/home` and `/fast` is not hidden.

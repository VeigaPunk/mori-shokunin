# C2 fixture power — MutFixturePower

## Scope and method

Scratch prefix `S` below means `/fast/scratch/hyaku/mori-r31/MutFixturePower`; lane prefix `R` means `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Axes: semantic fault sensitivity, counter limits, and exact restoration. This is a mutation finding, not a judgment of the lane tool or round admission.

Read the frozen rule, fixtures and counter: `R/.ufo/waves/round-31/rule-text.md:3-22`, `c2-fixtures.json:1-287`, and `count-c2.py:34-148`. Wrote a self-contained Bash reference in `S/reference.sh:1-168`, retaining the round-30 citation/run patterns and protection/window logic (`R/.ufo/waves/round-30/check-blind-wave.sh:76-85,105-123,135-154`; `S/reference.sh:45-83,97-106`).

Used one minimal behavior-bearing mutation for each of the six rule clauses. Each separate `M<N>.sh` received a pristine run, one mutation, a mutated run, exact restoration, and a restored run. The counter command was:

```sh
timeout 120 prlimit --as=536870912 -- python3 \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-31/count-c2.py \
  8baccf4ac9c44a38848d90c34df52392e804c168 \
  --tool-file /fast/scratch/hyaku/mori-r31/MutFixturePower/M<N>.sh
```

Actual commands, full stdout, exit status and hashes are saved in `S/M<N>-pristine.txt`, `S/M<N>-mutated.txt` and `S/M<N>-restored.txt`, each lines 1-25. The preserved defective scripts are `S/M<N>.mutant.sh`; the active `M<N>.sh` files now contain restored reference bytes. The counter created and removed its own `/tmp` sandbox, as specified in `R/.ufo/waves/round-31/count-c2.py:72-105,147-148`.

## Kill table

A kill requires the pristine and restored controls to pass and the mutated counter run to fail. No baseline failure, timeout or malformed-output failure was counted as a kill.

| Mutant | Clause and single-point defect | Expected semantic detector | exact | Killed | Actual evidence |
|---|---|---|---|---|---|
| M1 reverse opener removed | 1: delete `opened files` from the shared heading/label phrase regex (`S/M1.mutant.sh:93-94`) | Reject failure to recognize the reverse-order opener | 16/16 | no | `C2=met`, counter exit 0; `S/M1-mutated.txt:22-25` |
| M2 plus marker removed | 2: remove only `+ ` from the entry-marker alternatives (`S/M2.mutant.sh:95`) | Reject failure to inspect a forbidden plus-bullet entry | 16/16 | no | `C2=met`, counter exit 0; `S/M2-mutated.txt:22-25` |
| M3 prose does not close | 3: replace the prose-closing state reset with `:` (`S/M3.mutant.sh:149-150`) | Reject treating a later list after prose as still files-opened | 16/16 | no | `C2=met`, counter exit 0; `S/M3-mutated.txt:22-25` |
| M4 line suffix retained | 4: remove the numeric line/range suffix normalization (`S/reference.sh:31`; absent between `S/M4.mutant.sh:30-31`) | F13: allowed line-suffixed path must not produce a forbidden-path hit | 15/16 | yes | Extra forbidden-path hit at F13:2; `S/M4-mutated.txt:18,22-25` |
| M5 heading counts as entry | 5: set `files_entry_seen=1` when a block opens (`S/M5.mutant.sh:136`) | F05: heading plus prose but no entry must report missing-list at line 1 | 15/16 | yes | Missing-list hit disappears; `S/M5-mutated.txt:10,22-25` |
| M6 retained detectors scoped to list | 6: guard the shared retained-detector call with `in_files_list` (`S/M6.mutant.sh:153`) | F15 source citation at line 5 and F16 run output at line 7 remain detectable outside the list | 14/16 | yes | Both retained-detector hits disappear; `S/M6-mutated.txt:20-25` |

Observed result: **three killed, three survived, none inconclusive** — the six counter logs cited above. Every mutated run still returned tool exit 1, scanned 16, had consistent hit counts, and had no stray hit (`S/M1-mutated.txt:5,22` through `S/M6-mutated.txt:5,22`). Hit counts for M1–M6 were respectively 14, 14, 14, 15, 13 and 12. Kills were semantic mismatches, not execution failures.

## Named counter limits — every survivor

The following are limits of the frozen counter, not changes to its contract. Separate scratch witnesses demonstrate that these survivors are non-equivalent defects. Their inputs live only in the isolated clone `S/witness-repo/witnesses/`; they were not added to or substituted for the frozen 16 fixtures. Witness revision: `3ad224ea0be535811d68f157c1e25c5fc74f34a6` (`S/M1-witness.txt:1`). Each witness was run through the same four-argument Bash interface under `timeout 120` and the same memory bound, on pristine, saved mutant and restored scripts (`S/M1-witness.txt:7-30`, `S/M2-witness.txt:8-32`, `S/M3-witness.txt:7-30`).

### C2-LIMIT-REVERSED-OPENER — M1

Clause 1 requires `opened files` as well as `files opened` (`R/.ufo/waves/round-31/rule-text.md:10-12`). M1 passes all frozen cases but reports a false missing-list hit for this allowed reverse-order heading (`S/witness-repo/witnesses/OpenReverse.md:1-2`):

```text
## Opened files
- .ufo/waves/round-31/rule-text.md
```

Pristine/restored: `scanned=1`, `blind_violations=0`, exit 0. Mutant: `scanned=1`, `blind_violations=1`, `witnesses/OpenReverse.md:1:writer-missing-files-opened-list`, exit 1 (`S/M1-witness.txt:10-30`). Frozen-counter survival: `S/M1-mutated.txt:23-25`.

### C2-LIMIT-PLUS-BULLET — M2

Clause 2 includes `+ ` entries (`R/.ufo/waves/round-31/rule-text.md:13-15`). M2 passes all frozen cases but silently loses the forbidden entry in this witness (`S/witness-repo/witnesses/PlusMarker.md:1-3`):

```text
## Files opened
- .ufo/waves/round-31/rule-text.md
+ tools/mori-census.sh
```

Pristine/restored: `scanned=1`, `blind_violations=1`, `witnesses/PlusMarker.md:3:writer-forbidden-opened-path`, exit 1. Mutant: `scanned=1`, `blind_violations=0`, exit 0 (`S/M2-witness.txt:11-32`). Frozen-counter survival: `S/M2-mutated.txt:23-25`.

### C2-LIMIT-PROSE-CLOSE-STATE — M3

Clause 3 closes the block at the first other non-blank line (`R/.ufo/waves/round-31/rule-text.md:16`). M3 passes all frozen cases while retaining list state across prose. F01 has prose only at the end, so it cannot expose this particular stale-state defect (`R/.ufo/waves/round-31/c2-fixtures.json:16-28`). The separating witness is `S/witness-repo/witnesses/ProseClose.md:1-4`:

```text
## Files opened
- .ufo/waves/round-31/rule-text.md
The files list ends here.
- tools/mori-census.sh
```

Pristine/restored: `scanned=1`, `blind_violations=0`, exit 0. Mutant: `scanned=1`, `blind_violations=1`, `witnesses/ProseClose.md:4:writer-forbidden-opened-path`, exit 1 (`S/M3-witness.txt:10-30`). Frozen-counter survival: `S/M3-mutated.txt:23-25`.

Ready-to-paste limit wording:

```text
C2-LIMIT-REVERSED-OPENER: exact=16/16 does not reject a parser that omits the required "opened files" opener.
C2-LIMIT-PLUS-BULLET: exact=16/16 does not reject a parser that omits the required "+ " entry marker.
C2-LIMIT-PROSE-CLOSE-STATE: exact=16/16 does not reject a parser that skips prose but incorrectly keeps the list open for later entries.
```

These statements are limited to the six mutations exercised here; they do not establish exhaustive coverage of every spelling, marker, stripping operation or retained-detector behavior.

## Before/mutated/after hashes and restoration

Common pristine/reference SHA-256, also the exact final SHA-256 of every active `M1.sh`–`M6.sh`:

```text
5384197f2918f1ea43bee7dad569dd178cc03ae57382949eec7f03660d3583d1
```

| Tool | Before and restored control result | Mutated SHA-256 |
|---|---|---|
| M1 | Both exact=16/16, C2=met, counter exit 0 (`S/M1-pristine.txt:2,23-25`; `S/M1-restored.txt:2,23-25`) | `1a32837010c1273230d19df14f6c18182423256b79eb9e102d8064c3338ccd27` (`S/M1-mutated.txt:2`) |
| M2 | Both exact=16/16, C2=met, counter exit 0 (`S/M2-pristine.txt:2,23-25`; `S/M2-restored.txt:2,23-25`) | `98c524959d3e733a142d760e99ba1bea4a39a889a3aa5cdd656285de50e5bcbf` (`S/M2-mutated.txt:2`) |
| M3 | Both exact=16/16, C2=met, counter exit 0 (`S/M3-pristine.txt:2,23-25`; `S/M3-restored.txt:2,23-25`) | `3185d4ebc79e6346a5a22c44e8e127ea1d45e6923b6f0211fd279e176bc54018` (`S/M3-mutated.txt:2`) |
| M4 | Both exact=16/16, C2=met, counter exit 0 (`S/M4-pristine.txt:2,23-25`; `S/M4-restored.txt:2,23-25`) | `75c408aa85ec87c6a201687a9b1936b7857b7355d34e60f9eaef6bcbd911cc22` (`S/M4-mutated.txt:2`) |
| M5 | Both exact=16/16, C2=met, counter exit 0 (`S/M5-pristine.txt:2,23-25`; `S/M5-restored.txt:2,23-25`) | `0cc0569d8771f3f34824961f5e09c1e3a45d0d409c1581c385473e8c48dd3ed7` (`S/M5-mutated.txt:2`) |
| M6 | Both exact=16/16, C2=met, counter exit 0 (`S/M6-pristine.txt:2,23-25`; `S/M6-restored.txt:2,23-25`) | `fa535bf3dafa031a94d8bff9b11ac9d23708737594715636ac6f5e244ad34ce2` (`S/M6-mutated.txt:2`) |

A final `timeout 120 prlimit --as=536870912 -- sha256sum ...` independently recorded all seven identical restored/reference digests (`S/restoration-hashes.txt:1-8`). The initial frozen-input hash command and the final hash command produced identical values:

| Frozen input under `R/.ufo/waves/round-31/` | SHA-256 before = after | Final receipt |
|---|---|---|
| `count-c2.py` | `cbf019115ca8892d10fc54009c47d49f8b445c51e992fe183038051c14ee2b61` | `S/restoration-hashes.txt:9` |
| `c2-fixtures.json` | `1442c14e963bf77df34774015dff7ee73a9738d49b3911d26b4e3b96f48e0b31` | `S/restoration-hashes.txt:10` |
| `rule-text.md` | `79ea24c8c0ab1ec9c8e90d543171e41412849232e073fd993fc65764f040698b` | `S/restoration-hashes.txt:11` |

Initial command: `timeout 120 prlimit --as=536870912 -- sha256sum R/.ufo/waves/round-31/count-c2.py R/.ufo/waves/round-31/c2-fixtures.json R/.ufo/waves/round-31/rule-text.md`, with `R` expanded as defined above; its output is the three digests in the table. No frozen file was edited.

## Operational record

Only this report was written in the lane. Reference scripts, preserved mutants, receipts and supplementary witness files are under `S`. Git writes for the supplementary witnesses were confined to `S/witness-repo`, created with `timeout 120 prlimit --as=536870912 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks --no-checkout R S/witness-repo` (output: cloning completed). The frozen counter's `/tmp` writes were its documented sandbox behavior, not lane writes (`R/.ufo/waves/round-31/count-c2.py:72-105,147-148`).

No subagent, background job, service operation, OMP invocation, tool installation or update was started. All foreground probe calls returned; no timeout occurred (counter exit receipts above). No lane/fleet commit or index write was made. No build, lint or unrelated test was run. This probe supplies limits only; it does not alter the frozen fixtures, their acceptance predicate, or the claim contract.

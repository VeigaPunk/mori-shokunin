# Mo54ExecControlsReplay — all fourteen frozen controls replayed out of tree: zero field differences

Scope: replay only. Reads at the data commit `78295c764093ff1f6cee08d7246679900bde7265`:
`.ufo/waves/round-54/contract.md`, `.ufo/waves/round-54/count-c1.py`, `.ufo/waves/round-54/count-c2.py`,
`.ufo/waves/round-54/controls/{controls.py,c1data.py,c2data.py}`, `.ufo/waves/round-54/evidence/control-*.txt`,
`.ufo/waves/round-54/evidence/freeze-sha256.txt`. No host surface was read, no network fetch, no tool installed,
no git/jj mutation in the lane (the only git writes happened inside throwaway clones under my scratch, removed by
the script's own `finally`). Scratch `/fast/scratch/hyaku/mori-r54/Mo54ExecControlsReplay/`, 92 KiB, removed after
this report was written. Machine id written MACHINE_ID. This report starts no line with a vote keyword.

## 1. Result

**14 of 14 controls reproduce their recorded verdict line field for field, and their exit code.** The only
differences are `rev=` and the fixture-commit hash inside the `command:` line — both of which name a commit the
replay creates anew, not a scored field.

| control | recorded exit | replay exit | counter fields | `failed=` |
|---|---|---|---|---|
| c1 do-nothing | 1 | 1 | identical | `ledger_absent,pins` |
| c1 copies-only | 1 | 1 | identical | `ledger_absent` |
| c1 witness | 0 | 0 | identical | — (`C1=met`) |
| c1 no-votes | 1 | 1 | identical | `votes` |
| c1 unsettled-voters | 1 | 1 | identical | `votes` |
| c1 no-line | 1 | 1 | identical | `line` |
| c1 v72-copies | 1 | 1 | identical | `pins` |
| c2 do-nothing | 1 | 1 | identical | `entry_absent,pins` |
| c2 copies-only | 1 | 1 | identical | `entry_absent` |
| c2 witness | 0 | 0 | identical | — (`C2=met`) |
| c2 quote-echo | 1 | 1 | identical | `bad_rows,entailment,provenance,source_rows,sources_floor` |
| c2 unlocated | 1 | 1 | identical | `quote_missing,sources_floor` |
| c2 no-votes | 1 | 1 | identical | `entailment` |
| c2 two-sources | 1 | 1 | identical | `sources_floor` |

Comparison was mechanical (section 4): every `key=value` token of the counter line except `rev`, plus the process
exit code. Both replays (`evidence-run1`, `evidence-run2`) produced the same fields, so the agreement is not one
lucky tree.

## 2. Method

Scratch mirror of the wave layout, so the frozen `c1data.py`/`c2data.py` `../count-cN.py` imports still resolve:

```
/fast/scratch/hyaku/mori-r54/Mo54ExecControlsReplay/
  round-54/controls/{controls.py,c1data.py,c2data.py}      # copies; only controls.py edited
  round-54/count-c1.py -> <lane>/.ufo/waves/round-54/count-c1.py   # symlink to the frozen counter
  round-54/count-c2.py -> <lane>/.ufo/waves/round-54/count-c2.py
  evidence/, evidence-run1/, tmp/, replay-run{,2}.txt
```

Two edits to my copy of `controls.py`, both disclosed and both required by the out-of-tree location:

```diff
@@ -16,14 +16,14 @@
 LANE = os.path.dirname(os.path.dirname(os.path.dirname(WAVE)))
+LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"  # replay: frozen counters/overlay read from the lane
 EVID = os.path.join(WAVE, "evidence")
+EVID = os.path.join(os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"), "evidence")  # replay: scratch only
```

`LANE` is normally derived by three `dirname()` steps from the wave directory; in the mirror that resolves to
`/fast/scratch/hyaku`, and the first attempt died before scoring anything:

```
$ python3 -B "$S/round-54/controls/controls.py"     # before the LANE edit, exit=1
fatal: repository '/fast/scratch/hyaku' does not exist
  File ".../controls/controls.py", line 45, in clone
    subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", LANE, d], check=True, timeout=300)
  subprocess.CalledProcessError: ... returned non-zero exit status 128
```

`c1data.py` and `c2data.py` were left byte-identical to the frozen copies:

```
fd418b9d5f5120d74ea9964c3aae6b536b3922ccb5106c78da3370df2a9c0cc9  <scratch>/round-54/controls/c1data.py
fd418b9d5f5120d74ea9964c3aae6b536b3922ccb5106c78da3370df2a9c0cc9  <lane>/.ufo/waves/round-54/controls/c1data.py
72f1a6fbbf897faa309841cd7ec171722c99b4720aaeb56928e7810bb7ce3334  <scratch>/round-54/controls/c2data.py
72f1a6fbbf897faa309841cd7ec171722c99b4720aaeb56928e7810bb7ce3334  <lane>/.ufo/waves/round-54/controls/c2data.py
```

The counters that scored every control are the frozen lane files, not copies — the `score()` call is
`python3 -B <lane>/.ufo/waves/round-54/count-cN.py --repo <clone> <rev>`, and both files still match
`evidence/freeze-sha256.txt`:

```
e97a11986694b60f3a5d9d50b151553072f08a8a8d46cbea8f4b63a90dff433c  .ufo/waves/round-54/count-c1.py
d6b42f893b304ca355c03a4e43ad431b268b39ecfe8163c6871bbc0d6550785e  .ufo/waves/round-54/count-c2.py
```

Run command (twice, second run after moving `evidence/` to `evidence-run1/`):

```
export TMPDIR=/fast/scratch/hyaku/mori-r54/Mo54ExecControlsReplay/tmp
export HYAKU_SCRATCH=/fast/scratch/hyaku/mori-r54/Mo54ExecControlsReplay
cd /fast/scratch/hyaku/mori-r54/Mo54ExecControlsReplay
python3 -B /fast/scratch/hyaku/mori-r54/Mo54ExecControlsReplay/round-54/controls/controls.py
```

Run 1 wall time 18.82 s, run 2 18.65 s, both exit 0. The script's `finally: shutil.rmtree(SCRATCH)` removed all
fourteen clones; the scratch tree held 92 KiB of receipts and copies afterwards. Nothing was written to
`<lane>/.ufo/waves/round-54/evidence/` — that directory still holds 26 files, the ten `control-*.txt` receipts
still at mtime 01:28, and all 37 `freeze-sha256.txt` entries verify (`mismatched=[]`) after both runs.

## 3. Measured replay lines (run 1, verbatim)

```
c1 copies-only    C1=unmet scope=31 rows=0 matched=0 status_ok=0 line_ok=0 quote_ok=0 source_rows=bad pins=ok provenance=bad held=0 absent=0 holds=0 changed=0 voted=0 dissent=0 rev=e0c0bdae5a73b848c65395d4178531d7a1b64722 failed=ledger_absent
c1 do-nothing     C1=unmet scope=31 rows=0 matched=0 status_ok=0 line_ok=0 quote_ok=0 source_rows=bad pins=bad provenance=bad held=0 absent=0 holds=0 changed=0 voted=0 dissent=0 rev=39dcf4d7e410d362781a47e8365ca23b5c807598 failed=ledger_absent,pins
c1 no-line        C1=unmet scope=31 rows=31 matched=31 status_ok=31 line_ok=0 quote_ok=31 source_rows=ok pins=ok provenance=ok held=31 absent=0 holds=31 changed=0 voted=31 dissent=0 rev=647401b69d4d0241df6fce0502df88813ceb8ecb failed=line
c1 no-votes       C1=unmet scope=31 rows=31 matched=31 status_ok=31 line_ok=31 quote_ok=31 source_rows=ok pins=ok provenance=ok held=31 absent=0 holds=31 changed=0 voted=0 dissent=0 rev=65a9e14597cc6c4f87a458b5a7c8f06102b5e7a4 failed=votes
c1 unsettled      C1=unmet scope=31 rows=31 matched=31 status_ok=31 line_ok=31 quote_ok=31 source_rows=ok pins=ok provenance=ok held=31 absent=0 holds=31 changed=0 voted=0 dissent=0 rev=e99d1135240c507b20f4597a9dbbacbbabd6f823 failed=votes
c1 v72-copies     C1=unmet scope=31 rows=31 matched=31 status_ok=31 line_ok=31 quote_ok=31 source_rows=ok pins=bad provenance=ok held=31 absent=0 holds=31 changed=0 voted=31 dissent=0 rev=7259a248cb8dff8dc1d73b82c2ec68d01705ace9 failed=pins
c1 witness        C1=met scope=31 rows=31 matched=31 status_ok=31 line_ok=31 quote_ok=31 source_rows=ok pins=ok provenance=ok held=31 absent=0 holds=31 changed=0 voted=31 dissent=0 rev=94d0934b7203ca57e9b03aae1a921062ac22bd9d
c2 copies-only    C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=ok provenance=bad entailed=0 dissent=0 rev=c5f01755bb693f280bd822a78f6f84f892f7f1ff failed=entry_absent
c2 do-nothing     C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad entailed=0 dissent=0 rev=39dcf4d7e410d362781a47e8365ca23b5c807598 failed=entry_absent,pins
c2 no-votes       C2=unmet claims=14 located=14 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=4140be58c277cbdefe3b05efaaffcbc5dd1db4e5 failed=entailment
c2 quote-echo     C2=unmet claims=14 located=0 quote_missing=0 bad_rows=14 sources=0 source_rows=bad pins=ok provenance=bad entailed=0 dissent=0 rev=7c84187e6b13a7d79d1cd775b286b8370c67ba76 failed=bad_rows,entailment,provenance,source_rows,sources_floor
c2 two-sources    C2=unmet claims=14 located=14 quote_missing=0 bad_rows=0 sources=2 source_rows=ok pins=ok provenance=ok entailed=14 dissent=0 rev=93a0c4b6f2bb81383fe55f678445309d1c48055b failed=sources_floor
c2 unlocated      C2=unmet claims=14 located=0 quote_missing=14 bad_rows=0 sources=0 source_rows=ok pins=ok provenance=ok entailed=14 dissent=0 rev=3266dd1aea3f2111581281c0064883ccafc3ab0b failed=quote_missing,sources_floor
c2 witness        C2=met claims=14 located=14 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok entailed=14 dissent=0 rev=c1a8ae0dd1bca7b90c5ab8a8f14f47550d5d184f
```

Recorded counterpart revs (from `evidence/control-*.txt`), for the `rev=` pairs that differ:

| control | recorded `rev=` | replay run 1 | replay run 2 |
|---|---|---|---|
| c1 do-nothing | `39dcf4d7…` | `39dcf4d7…` (same) | `39dcf4d7…` (same) |
| c1 copies-only | `a6888a07…` | `e0c0bdae…` | `9df1fa77…` |
| c1 witness | `f5b7a8c9…` | `94d0934b…` | `3fb5c74d…` |
| c1 no-votes | `9c52523b…` | `65a9e145…` | `b2aecbfd…` |
| c1 unsettled | `6f4c148c…` | `e99d1135…` | `0545ad83…` |
| c1 no-line | `e79f525f…` | `647401b6…` | `dfb4ef29…` |
| c1 v72-copies | `34b544d8…` | `7259a248…` | `eb375f2b…` |
| c2 do-nothing | `39dcf4d7…` | `39dcf4d7…` (same) | `39dcf4d7…` (same) |
| c2 copies-only | `ed10983d…` | `c5f01755…` | `39802352…` |
| c2 witness | `d99c87a9…` | `c1a8ae0d…` | `8d686f31…` |
| c2 quote-echo | `bd730353…` | `7c84187e…` | `631bfb4b…` |
| c2 unlocated | `1fc15204…` | `3266dd1a…` | `49ecdecf…` |
| c2 no-votes | `c3a724f9…` | `4140be58…` | `a4a7048a…` |
| c2 two-sources | `fa9e03bd…` | `93a0c4b6…` | `45ba612a…` |

The two do-nothing controls are scored at the entering tip itself (not at a clone commit), so their `rev=` is
`39dcf4d7…` in all three runs — and their whole receipt files are byte-identical between the recording and the
replay once the clone path is elided (`normalised-byte-identical receipts: 2/14`; the other twelve differ only in
the fixture-commit hash of the `command:` line).

## 4. Comparison code and its output

Fields compared: every `key=value` token of the `C1=`/`C2=` line except `rev`, plus the `exit=` value; the
`control:` label and the `note:` prose were also compared (all equal). Output:

```
orig vs replay-run1 differing: []
run1 vs run2 differing: []
exit codes: orig=['1','1','1','1','1','1','0','1','1','1','1','1','1','0']  run1=same  run2=same  all-equal=True
normalised-byte-identical receipts: 2/14   (the two do-nothing receipts)
freeze after run2: entries=37 mismatched=[]
lane evidence listing count: 26
```

## 5. Cross-check of the contract's control-readings table

Every row of `contract.md` "Control readings" was compared to the receipt it cites, not to the replay: the
verdict token, the named field values and the `failed=` list all appear verbatim in the recorded receipts
(`c1 do-nothing` pins=bad; `c1 copies-only` pins=ok; `c1 no-votes` line_ok=31 voted=0; `c1 unsettled-voters`
voted=0; `c1 no-line` line_ok=0 quote_ok=31 voted=31; `c1 v72-copies` pins=bad; `c2 do-nothing`, `c2 copies-only`,
`c2 quote-echo` bad_rows=14, `c2 unlocated` quote_missing=14, `c2 no-votes` entailed=0, `c2 two-sources` sources=2,
and both witnesses `C1=met`/`C2=met` at exit 0). No table cell contradicts its receipt.

## 6. What this replay does and does not establish

- It establishes that the frozen `controls/controls.py`, the frozen appliers and the frozen counters reproduce the
  recorded verdict for every one of the fourteen trees, twice, from a copy that never wrote into the lane.
- It does not establish that the recorded receipts were produced by these exact commands: the recorded trees live
  only in removed clones, so the replay rebuilds them from the same recipe and compares the verdict, not the bytes.
- The replay is field-stable because every scored field is derived from the tree; the only moving part is the
  commit id the script creates (`rev=` and the `command:` line). `git commit` embeds the committer timestamp, so
  those hashes cannot be reproduced — the divergence is expected and carries no scored field.
- The witness controls remain feasibility only, as the contract states; their `C1=met`/`C2=met` lines were
  reproduced exactly, which is what a witness is for.
- Corroborated (not new): `c1 v72-copies` passes status/line/quote at 31/31 and fails only `pins`, so with the
  frozen errno.h byte-identical across tags the pin arm alone separates v7.2 bytes dressed as v7.3 — the contract's
  named limit is real and is measured, not assumed.

## Findings

- **LOW — no divergence found.** All fourteen frozen controls reproduce their recorded counter fields and exit
  codes across two independent replays (`.ufo/waves/round-54/evidence/control-*.txt` vs
  `<scratch>/evidence-run1|run2/control-*.txt`); the frozen bytes are intact before and after (37/37 sha256).
  Nothing in `corpus/`, the counters, the predicates or the kill rules needs a change for this evidence.
- **LOW — `controls.py:19` cannot be replayed out of tree without a source edit.** `LANE` is three `dirname()`
  steps from the wave directory, so a copy of `controls/` elsewhere resolves the clone source to the wrong root
  (`fatal: repository '/fast/scratch/hyaku' does not exist`, exit 128 in the first attempt). Round-55 routing
  candidate for the control runner only: derive `LANE` from `git rev-parse --show-toplevel` or an explicit
  constant. This is a tooling-ergonomics limit, not a counter, predicate or kill-rule change.
- **LOW — control receipts are verdict-reproducible, not byte-reproducible.** Each `command:` line embeds the
  per-control fixture commit and each counter line embeds `rev=`; both are commit ids with committer timestamps,
  so no receipt can be regenerated byte for byte. A future reader must compare fields, as section 4 does, rather
  than `cmp` the files. File: `.ufo/waves/round-54/evidence/control-*.txt`. Round-55 routing candidate for the
  receipt format (record the command with a placeholder for the fixture id, as this report does).
- **LOW — C2's `source_rows` and `provenance` are consequential, not independent.** In `c2 quote-echo` a
  row-level defect empties `ids_in_table`, so the same 14 bad rows also flip `source_rows=bad`, `provenance=bad`,
  `sources=0`, and add three more names to `failed=`
  (`count-c2.py:275-278`; receipt `failed=bad_rows,entailment,provenance,source_rows,sources_floor`). This is
  correct behaviour for a gate but it means a `failed=` set comparison across implementations must expect the
  cascade; it is a named limit for round 55, not a fix for this round.

# Mo50bExecC1Controls — round 50 (attempt 2), wave a2w1: re-run of the frozen C1 controls

Seat: executor (leaf). Lane `mori-shokunin`, repo `/home/vgpnk/Projects/shokunin/mori-shokunin`, fleet root
`/home/vgpnk/Projects/shokunin`. Contract read first: `.ufo/waves/round-50/contract.md` (frozen at
`950e99be6757a52b00e9eb70ae1a1a7bbe2ea379`). Controls re-run at the **entering tip**
`7197160b927f04db294c9553fb48fadcc7a3f4e3` as assigned. Lane HEAD while running: `4548a34dc8b4072abaa4335c1f54a9efcfcc314a`.

Scope: re-run `controls/c1-controls.py` in a scratch copy and diff each produced receipt against the committed
`evidence/control-c1-*.txt`. No judgement of C1's verdict, no edit to any lane file, no counter change proposed.

## Verdict (answers first)

**All 8 controls reproduce: 8/8 identical after normalising only the fixture commit hash (`rev=`).** The frozen
receipts are reproducible from the frozen counter and the frozen controls, against the lane and fleet read-only.
The re-run does **not** bear on the landed data: the script builds every control from the entering tip, so this
receipt set is insensitive to the a2 landing at `487941b9395e89678af0053cc443cdb49cdee6e3` (see Finding F2).

## Method (exact, reproducible)

Scratch `S = /fast/scratch/hyaku/mori-r50/Mo50bExecC1Controls`, `export TMPDIR=$S/tmp`. Nothing was installed
(no pacman, no uv, no npx): the stock `python3` and `git` suffice. `scripts/hyaku/disk-guard.sh status` before the
run: `/dev/nvme1n1p2 804G 188G 616G 24% /fast`, no ENOSPC risk.

```bash
S=/fast/scratch/hyaku/mori-r50/Mo50bExecC1Controls
mkdir -p "$S/tmp"
cp -a /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50 "$S/round-50"
# only relocation edit: the copy derives LANE/FLEET by walking up three dirs from its own location.
# EVID follows the copy automatically (WAVE/evidence), so the receipts land in scratch, not in the lane.
python3 "$S/round-50/controls/c1-controls.py" 7197160b927f04db294c9553fb48fadcc7a3f4e3 --scratch "$S/run"
```

The single adjustment inside the copy:
`LANE = os.path.dirname(os.path.dirname(os.path.dirname(WAVE)))` → `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"`,
`FLEET = os.path.dirname(LANE)` → `FLEET = "/home/vgpnk/Projects/shokunin"`. `COUNTER` and `EVID` were **not**
touched: `COUNTER` resolves to the copy's own frozen `count-c1.py`, `EVID` to the copy's `evidence/`.

Frozen-byte check before the run (worktree sha256 equal to `evidence/freeze-sha256.txt`):

```
c7b49dae9043ceda327e45ddaa5ce2c2ca09158e381162b76f393a50b7ee8a04  .ufo/waves/round-50/controls/c1-controls.py
2d5c3ee53198124ef001908cc5abba5c71a6fb63773c31ece211b7c6cdae4456  .ufo/waves/round-50/count-c1.py
```

Copy sha256 after the run: `count-c1.py` = `2d5c3ee5…` (unchanged), `controls/c1-controls.py` = frozen except the
two constants above. The committed receipts themselves are the frozen bytes — 8/8 OK:

```
$ grep -E 'evidence/control-c1-' .ufo/waves/round-50/evidence/freeze-sha256.txt | sha256sum -c -   # rc=0
.ufo/waves/round-50/evidence/control-c1-all-latest.txt: OK
.ufo/waves/round-50/evidence/control-c1-axes-only.txt: OK
.ufo/waves/round-50/evidence/control-c1-box-dropped.txt: OK
.ufo/waves/round-50/evidence/control-c1-do-nothing.txt: OK
.ufo/waves/round-50/evidence/control-c1-pins-deleted.txt: OK
.ufo/waves/round-50/evidence/control-c1-pins-updated-no-receipt.txt: OK
.ufo/waves/round-50/evidence/control-c1-shonen-only.txt: OK
.ufo/waves/round-50/evidence/control-c1-witness.txt: OK
```

Control script exit: `rc=0` (its own contract: `witness` must exit 0, every other control must exit 1). Wall time
51 s (`real 0m51.331s`), `user 3m13s / sys 2m44s` — the two `--selftest` sub-runs per control dominate.

## Per-control result

Diff used `sed -E 's/\brev=[0-9a-f]{40}\b/rev=<REV>/g'` on both sides. The receipts carry **no timestamps** (header
names the control and the entering hash; the tail carries `rev=` and `exit=`), so `rev=` is the only varying field.

| control | committed line (rev normalised) | re-run line | exit (comm/rerun) | identical |
|---|---|---|---|---|
| do-nothing | `C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d failed=mismatch` | same | 1 / 1 | **yes** (raw byte-exact, `rev=` is the entering tip) |
| all-latest | `C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d failed=mismatch` | same | 1 / 1 | **yes** |
| pins-deleted | `C1=unmet items=6 axes=6 pins=0 boxes=4 mismatches=4 errors=0 hidden=0 manifest=a94551c5bc8d failed=mismatch,pins_floor` | same | 1 / 1 | **yes** |
| pins-updated-no-receipt | `C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d failed=mismatch` | same | 1 / 1 | **yes** |
| axes-only | `C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=2 errors=0 hidden=0 manifest=a94551c5bc8d failed=mismatch` | same | 1 / 1 | **yes** |
| shonen-only | `C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=4 errors=0 hidden=0 manifest=a94551c5bc8d failed=mismatch` | same | 1 / 1 | **yes** |
| box-dropped | `C1=unmet items=6 axes=6 pins=0 boxes=3 mismatches=4 errors=0 hidden=0 manifest=a94551c5bc8d failed=boxes_floor,mismatch,pins_floor` | same | 1 / 1 | **yes** |
| witness | `C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d` | same | 0 / 0 | **yes** |

Raw (un-normalised) sha256, committed vs re-run — seven differ only by the fixture commit hash:

```
all-latest               36de15c14786 / c9eb155614e8
axes-only                f5d1088d4640 / fa1db03e5d97
box-dropped              54787d42d071 / 7cd34c181764
do-nothing               6c87ab626ba1 / 6c87ab626ba1   <- byte-exact, incl. rev=
pins-deleted             fa1cd38844bd / fb0f1b34abd3
pins-updated-no-receipt  efd04c33b879 / bdcec596485b
shonen-only              cc934244d456 / 23fa9b41b2c6
witness                  2271001d38b9 / e42a9a241b73
```

Item-level equality holds too — the diff was over the whole receipt text, so every `item axis …` / `item pin …`
line (including the reason strings `evidence_missing:corpus/lessons/round-47-verifier-spotcheck.md`,
`…round-49…`, `receipt_missing`) is unchanged, not just the `C1=` tail. The re-run's per-item detail for
`do-nothing` (byte-identical receipt, quoted in full in the scratch log) is:

```
item axis coverage expect=round_47_improved got=round=26,evidence_missing:corpus/lessons/round-47-verifier-spotcheck.md state=mismatch
item axis operability expect=round_47_improved got=round=31,evidence_missing:corpus/lessons/round-47-verifier-spotcheck.md state=mismatch
item axis depth expect=round_49_improved got=round=31,evidence_missing:corpus/lessons/round-49-verifier-spotcheck.md state=mismatch
item axis freshness expect=round_28_improved got=ok state=ok
item axis calibration expect=round_49_improved got=round=25,evidence_missing:corpus/lessons/round-49-verifier-spotcheck.md state=mismatch
item axis adjacency expect=round_19_improved got=ok state=ok
item pin python3_tools/mori-pin-check.py_--selftest expect=(60/60) got=PIN_CHECK_SELFTEST_pass=114_fail=0 state=mismatch
item pin python3_tools/mori-unlanded-check.py_--selftest expect=(13/13) got=UNLANDED_SELFTEST_pass=17_fail=0 state=mismatch
C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d rev=7197160b927f04db294c9553fb48fadcc7a3f4e3 failed=mismatch
exit=1
```

Instrument integrity (supplementary, same copy, `--scratch` inside `$S`):

```
$ python3 "$S/round-50/count-c1.py" --selftest      # rc=0
C1_SELFTEST pass=34 fail=0
$ diff -u .ufo/waves/round-50/evidence/selftest-c1.txt "$S/selftest-rerun.txt"   # IDENTICAL
```

So the 34 arms of the frozen counter still print the same tally and the committed `evidence/selftest-c1.txt` is
reproducible from the frozen bytes.

## Lane untouched (write guard)

```
before: find .ufo/waves/round-50/evidence -type f | sort | xargs sha256sum | sha256sum
        513e0c82249fcbd28ee2b28aa9de0a73809dec97e209ae5b5d6248f7bb8b6f32  -
after : … same digest 513e0c82249fcbd28ee2b28aa9de0a73809dec97e209ae5b5d6248f7bb8b6f32
git status --porcelain -- .ufo/waves/round-50/evidence   -> (empty)
diff -rq <lane>/evidence <copy>/evidence | grep -v control-c1-  -> no differences outside control-c1-*
```

The `--shared` clone and the `git archive` extraction lived under `$S/run`, `$S/run/c1-fixture`, `$S/run/obs-tree`;
every `git` call named `-C <clone>`, and the fixture toplevel was verified by the script before the first commit
(`rev-parse --show-toplevel` equality check is inside `c1-controls.py`). No fleet or sibling-lane mutation, no jj,
no `git add/commit` outside the throwaway clone. Scratch removed at the end (`rm -rf -- "$S"`), after the excerpts
above were copied into this report; nothing cited here lives only in scratch.

## Findings

- **F1 — LOW — `.ufo/waves/round-50/controls/c1-controls.py` (receipt writer, `rev=%s` in the `C1=` line).**
  Receipts are not byte-reproducible across runs: 7 of 8 differ from the committed files in the `rev=<fixture
  commit>` field alone, because each control is a fresh commit (timestamped hash). Contract-level consequence is
  nil (the contract says the controls are commits in a throwaway clone), but any future "re-run and diff" check
  must normalise `rev=`, as done here. No timestamps exist in the receipts, so nothing else varies.
- **F2 — LOW — `.ufo/waves/round-50/contract.md` §C1 "Controls" table.** The table's receipt list does not state
  that every control is built from the **entering** tip. This re-run at `7197160b` reproduces the receipts
  exactly, and therefore says nothing about the landed data at `487941b9`: `do-nothing` at the entering tip still
  reads `mismatches=6` — by construction, since the tip is an immutable commit and the lane working tree is never
  read. A reader could take "the controls were re-run" as support for C1 at the landed tip; it is not. The landed
  verification is `evidence/a2-c1-at-data.txt` (`C1=met … mismatches=0 rev=487941b9…`, exit 0), which this seat
  did not produce.
- **F3 — LOW — `contract.md` §C1 table, `box-dropped` row.** The row's reading is `boxes=3 … boxes_floor` but the
  frozen receipt (committed and re-run, identical) fails with `boxes_floor,mismatch,pins_floor` — dropping SHONEN's
  box 3 also removes a tally pin, which the script's docstring already says (`unmet (boxes_floor, pins_floor)`).
  The table under-reports the reason set. Data-level nit only; the verdict (`unmet`) is unchanged and reproducible.
- **F4 — LOW (operational, for re-runners) — `controls/c1-controls.py:26-31`.** `LANE`/`FLEET` are derived by
  walking three directories up from the script's own location. A copy outside the lane therefore silently points at
  the wrong repos (and the `--shared` clone source would be wrong); only `EVID` follows the copy, which is what
  kept this re-run from writing into the lane's `evidence/`. Any out-of-tree re-run must repoint exactly those two
  constants and leave `COUNTER`/`EVID` alone.
- **F5 — LOW (informational) — `.ufo/waves/round-50/evidence/control-c1-witness.txt`.** The witness re-runs to
  `C1=met … mismatches=0` exit 0 from the entering tip, confirming the contract's "feasibility only; built by the
  L1's script, not the claim's landing" reading. It is not evidence about the landed data, and no seat should cite
  it as such.

No HIGH or MED findings: every assigned control reproduced, every frozen hash verified, and the lane was not
written to.

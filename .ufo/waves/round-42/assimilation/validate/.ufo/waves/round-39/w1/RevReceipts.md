# RevReceipts — receipt→verdict→claim audit (mori round 39, wave 1)

Scope: all 22 files in `.ufo/waves/round-39/evidence/`, audited against the
frozen contract (`.ufo/waves/round-39/contract.md`) and the brief's C1–C3
after-values. Method: read every receipt; re-ran the counters/checkers/gate
(read-only) and diffed against the committed bytes; provenance from
`git log --diff-filter=A`. No lane file was modified; scratch under
`.ufo/waves/round-39/scratch/RevReceipts/`.

**Verdict: the C1, C2 and C3 after-values all reproduce, but one receipt
(`c8-red-wait.txt`) does not print the verdict its claim asserts — acceptance
FAIL for that receipt.** Two further contractual defects: C2's "before"
receipts were generated after the data seat, and the frozen contract's C3
after-value (`pass=11`) contradicts the evidence (`pass=12`).

## Receipt table

`cmd?` = first line is a `command:`; `run?` = that line is a literal,
argument-complete invocation. `repro` = I re-ran it / reconstructed it.

| Receipt | cmd? run? | Supports | Printed verdict | Repro |
|---|---|---|---|---|
| c7-after.txt | yes / yes (rev `f920eaf7`, not the claimed `13bfba2`) | C1 after | `C7=met` L12, `EXIT=0` L13 | **byte-identical** at `f920eaf7` and at claimed `13bfba2` (only wrapper `EXIT=0` extra) |
| c7-red-one-char.txt | yes / no (generator + prose section, argv missing) | C1 before, M18 one-char | `accepted=True`, `verdict: RED` | not run; committed pre-data (`87ec3d9`) |
| c7-red-comment.txt | yes / no | C1 before, comment anchors | `accepted=True`, RED | not run; pre-data |
| c7-red-classifier.txt | yes / no | C1 before, constant classifier | `r38 drift_kill accepted=True`, RED | not run; pre-data |
| c7-red-clone.txt | yes / no | C1 before, fabricated clone | r38 `C4=met`; r39 `exit=1`/`C7=unmet` | not run; pre-data |
| c8-after.txt | yes / no (prose) | C2 after | `CONFORM=met` L12, exit 0 L2 | all 9 check lines reproduce; **head_pin line differs** (live HEAD) |
| c8-after-selftest.txt | yes / no (prose) | C2 after | `CONFORM_SELFTEST pass=9 fail=0` | **reproduced** at `13bfba2`, exit 0 |
| c8-after-none.txt | yes / no | C2 after, None bypass | `exit=1`, `CONFORM=unmet` | check lines reproduce (head_pin differs) |
| c8-after-wait.txt | yes / no | C2 after, wait bypass | `exit=1`, `CONFORM=unmet` (drain_shape FAIL) | check lines reproduce (head_pin differs) |
| c8-red-none.txt | yes / no | C2 before, None bypass | `exit=0`, `CONFORM=met`, RED | **reproduced**: r38 checker → `CONFORM=met` |
| c8-red-wait.txt | yes / no | C2 before, wait bypass | `exit=1`, `CONFORM=unmet`, **"verdict: not reproduced"** L3,10,11 | **reproduced, and it confirms the receipt says NOT met** — see F1 |
| c9-red-a.txt | yes / yes | C3 before (r38 gate) | fixture C `round_changed=[S001]`; D `stale_supersede=[S001]` | **byte-identical** replay with r38 bytes (sha `9a6164e3…`) |
| c9-after-fixture-a.txt | **no** | C3 after, stale side-branch | `stale_supersede=[S001]`, as_of `[]`, EXIT=1 | **byte-identical** v2 replay |
| c9-after-fixture-c.txt | **no** | C3 after, no fabricated merge edit | `round_changed=[]`, as_of `[S001]`, EXIT=0 | **byte-identical** v2 replay |
| c9-after-fixture-d.txt | **no** | C3 after, landing is last edit | `as_of=[S001]`, stale `[]`, EXIT=1 | **byte-identical** v2 replay |
| c9-after-lane.txt | yes / no (prose) | C3 after, lane parity | 18 `as_of`, `stale_supersede=[]` at tip | stdout parity of v1/v2 at `13bfba2` confirmed; 53/52 walk counts not reproduced (no invocation) |
| gate-selftest-after.txt | **no** (first line is the result) | C3 after | `pass=12 fail=0`, EXIT=0 | **reproduced**; contradicts contract's `pass=11` (F5) |
| gate-r38-selftest-baseline.txt | yes / yes | C3/r38 baseline | `pass=9 fail=0` | **reproduced** with r38 gate bytes |
| m19-selftest-gap.txt | yes / no (description) | C2 before, selftest gap | "no communicate mutation; conjunct unexercised" | excerpt lines match r38 bytes verbatim; claim true |
| census-start.txt | yes / yes (fleet absolute path) | census before | 16 warnings, no S228, EXIT=0 | **reproduced** (`scripts/sources-census.sh validate --root … mori` → same 16 lines) |
| census-end.txt | **no** | census after | 17 warnings incl. S228, EXIT=0 | **reproduced** (= live census; body = start + S228) |
| freeze-r39.txt | no (pin manifest, exempt) | pins | — | `sha256sum -c`: **13/13 OK** |

## Findings

### F1 — HIGH: `c8-red-wait.txt` proves the opposite of the claim it is cited for

Claim under attack (brief C2; contract `contract.md:104`): "the r38 checker
printed `CONFORM=met` (`c8-red-none.txt`, `c8-red-wait.txt`)" because the
`wait(timeout=…)`+`stdout.read()` drain passed r38 `bounded_reads`.

The receipt's own bytes: `c8-red-wait.txt:3` `exit=1`, `:7`
`check bounded_reads FAIL (bypass-wait.py: run=True popen=False …)`, `:10`
`CONFORM=unmet`, `:11` `verdict: not reproduced`. I re-ran the r38 checker on
the same fixture (`scratch/c8/conform-r38.py 13f3db7e --counter
scratch/c8/bypass-wait.py`) and got the same `popen=False` / `CONFORM=unmet`.
Cause: r38 `bounded_reads` requires a `communicate` call at all
(`popen_ok = popen_ok and saw_communicate`, r38 conform.py:103–124), so the
wait+read shape is rejected structurally before any timeout-value question is
reached. The M19 "wait drain passes" premise has **no witness** in this
evidence set; C2's RED set is one witness (`none`), not two. The C2 *after*
value still holds (both fixtures → `CONFORM=unmet`, reproduced). Per the
assignment's acceptance rule ("FAIL on a receipt whose … printed verdict does
not match the claim it supports"), this receipt FAILS.

### F2 — HIGH: C2's "before" receipts were generated after the data seat

Contract `contract.md:169`: "the before receipts are recorded before any data
seat runs". `c7-red-*` honor it (added by `87ec3d9`, 00:58:53, before data
`f920eaf` 01:02:20). `c8-red-none.txt` and `c8-red-wait.txt` do not: they are
added by `13bfba2` (01:04:42, the after-receipts commit) and their own
`head_pin` lines read `pin=f920eaf7…` (`c8-red-wait.txt:5`), i.e. HEAD at
generation was the data commit, while their bodies claim "at 13f3db7e"
(`:2`). The r38 instrument bytes at `13f3db7e` were used, but the record was
produced post-data and post-freeze. This is the exact hygiene failure M18/M19
were meant to close for r38.

### F3 — MEDIUM: `head_pin` is a live-HEAD self-consistency check, not a pin of the measured revision

`conform.py:321–329` runs the counter's `--pin-only` and compares it to
`git rev-parse HEAD`; the counter's `--pin-only` prints `git rev-parse HEAD`
itself (`count-c7.py:404–410`). The `rev` argument is never used. Proof:
`conform.py 13bfba2…` printed `pin=20260b0c… tip=20260b0c…` at one moment and
`pin=ebc61f47… tip=ebc61f47…` minutes later — both PASS — while the receipt
records `pin=f920eaf7…` (`c8-after.txt:4`). Consequences: (a) `c8-after.txt`
and the four `c8-*` bypass receipts cannot be reproduced literally today (all
lines except `head_pin` do reproduce, and the `CONFORM=` verdict does); (b)
`head_pin` passes for **any** `rev` argument, and it flakes if a commit lands
between the counter's pin call and the checker's `rev-parse` on a live lane
(HEAD moved three times during this audit: `20260b0c`→`5561819`→`296b2c5`→
`ebc61f47`). P-C8 lists `head_pin` as one of the nine checks; its binding is
weaker than the name implies.

### F4 — MEDIUM: contract-declared evidence set ≠ disk

`contract.md:156–168` declares five files that do not exist: `c7-before.txt`,
`c7-red-anchors.txt`, `c8-before.txt`, `c9-before-lane.txt`, `c9-red-c.txt`.
Five files exist that are not declared: `c7-red-one-char.txt`,
`c8-after-none.txt`, `c8-after-wait.txt`, `c9-after-fixture-d.txt`,
`gate-r38-selftest-baseline.txt`. The facts are covered by other files
(`c9-red-a.txt` folds fixture C; `c7-red-one-char.txt` replaces
`c7-red-anchors.txt`), but there is **no receipt at all** for C1's base
(`r38 count-c4 → C4=met` at `13f3db7e`), C2's honest-counter base
(`c8-before.txt`), or C3's pre-change lane parity (`c9-before-lane.txt`).

### F5 — MEDIUM: frozen contract's C3 after-value is off by one

`contract.md:146` declares `MORI_SOURCES_APPENDONLY_SELFTEST pass=11 fail=0`;
`gate-selftest-after.txt:1` prints `pass=12 fail=0` and my re-run confirms
`pass=12 fail=0` exit 0 (gate bytes hash matches the freeze pin, so the gate
was not changed after freeze). The brief's C3 text says 12. The frozen
contract is simply wrong; a predicate declaring 11 and a receipt printing 12
cannot both be the frozen after-state.

### F6 — LOW/MEDIUM: 17 of 21 receipts are not runnable as written; 5 lack `command:` entirely

No `command:` first line: `c9-after-fixture-a/c/d.txt`, `census-end.txt`,
`gate-selftest-after.txt` (freeze-r39 is a pin manifest, exempt). Prose
"commands": all five `c8-*` receipts (`c8-after.txt:1` "r39 conform on
count-c7.py at f920eaf7"), `m19-selftest-gap.txt:1` (a description), and
`c9-after-lane.txt:1` (prose whose 53/52 walk counts and `6531ac60` line have
no reproducible invocation). The four `c7-red-*` commands name the generator
plus "(section: …)" but omit the generator's required `<entering-rev>
<lane-repo>` argv (`run-c7-reds.py:19`). Only `c7-after.txt`, `c9-red-a.txt`,
`census-start.txt` and `gate-r38-selftest-baseline.txt` are literal.

### F7 — LOW: one absolute path outside the lane root

`census-start.txt:1` cites `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
and `--root /home/vgpnk/Projects/shokunin`. Every other absolute path in the
set is under the lane root (`c8-*` `resolved=`, `c9-red-a.txt:1`). The census
command is otherwise honest and reproducible; `census-end.txt` has no command
but its body is exactly the live census output (differing from start only by
the S228 row, verified).

### F8 — LOW: `c7-after.txt` was measured at `f920eaf7`, not the claimed `13bfba2`

`c7-after.txt:1` names `f920eaf7`; the claim's command names `13bfba2`. I ran
both: outputs identical (`C7=met`, exit 0), so the body reproduces at the
claimed tip. The only provenance gap is that no receipt on disk was generated
at `13bfba2`. Minor related note: the `EXIT=` line is added by the receipt
wrapper, not printed by the counter; same for the gate receipts.

## Verified after-values (positive evidence)

- C1: `python3 .ufo/waves/round-39/count-c7.py 13bfba23b7ca063c76d3504a2ff6eb7b6a294932 --seed 20261024`
  → five PASS, four negatives rejected, `C7=met`, exit 0; body byte-identical
  to `c7-after.txt` minus the wrapper `EXIT=0`.
- C2: `conform.py 13bfba2…` → `CONFORM=met` exit 0 (twice, two different live
  HEADs); `--selftest` → `CONFORM_SELFTEST pass=9 fail=0` exit 0 (50.7 s).
- C2 negatives: both M19 bypass fixtures on the r39 checker → exit 1,
  `CONFORM=unmet`; `timeout_value` FAIL for none, `drain_shape` FAIL for wait —
  exactly as `c8-after-none/wait.txt` record.
- C3 fixtures: replay of `run-c9-dags.py` with the tracked v2 gate produced
  three blocks **byte-identical** to `c9-after-fixture-a/c/d.txt`, including
  deterministic DAG shas `b0=07be6c7f1765`, `c1=2053fccc3728`.
- C3 red: replay with the r38 gate bytes (`sha256 9a6164e3…`, matching the
  lane's `scratch/gate-r38.py`) produced a body **byte-identical** to
  `c9-red-a.txt` (fixture C `round_changed=[S001]`, fixture D stale).
- C3 lane: v2 at `13bfba2 --round-base f10a320d` → `superseded_as_of=[18 ids]`,
  `stale_supersede=[]`, exit 1; stdout identical to r38 gate bytes on the same
  rev (both exit 1). At `e37dcc6` → S069 in `stale_supersede` and out of
  `as_of`. Matches `c9-after-lane.txt` and the r38 `gate-after*.txt` tails.
- Pins: `sha256sum -c freeze-r39.txt` → 13/13 OK (contract, counters, gate,
  fixtures, witness files).

## Residual risk and gaps

- `c8-red-wait` failing means C2's *before* discrimination rests on a single
  fixture; no surviving witness shows the r38 checker ever accepting a
  wait+read drain. If M19's wait premise matters to the claim, it needs a
  fixture that the r38 checker actually accepts (or the claim must drop it).
- `head_pin`'s live-HEAD semantics make every `c8-*` receipt non-reproducible
  byte-for-byte after any commit; only the verdict is stable. A reader can
  still verify the checks that matter by re-deriving with a fixed `rev`.
- The 53/52 full-history walk counts and `6531ac60` presence in
  `c9-after-lane.txt` are unverified: no invocation is recorded and the
  generator only prints them if run with the right path set.
- The four `c7-red-*` reds and `c9-red-a`'s fixture-A/D blocks were verified by
  reading, not by re-executing `run-c7-reds.py` (it writes into `evidence/`,
  which is lane write scope; the c9 red generator was replayed because it
  accepts an output path, and it matched byte-for-byte).
- Tooling: nothing installed or upgraded during this audit.

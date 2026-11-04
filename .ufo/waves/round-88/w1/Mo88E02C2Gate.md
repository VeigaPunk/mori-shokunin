# Mo88E02C2Gate — round 88 w1: independent hand-built C2 counterfeit re-measurement

Seat: Mo88E02C2Gate (executor, calibration) · date 2026-11-04 · L1: MoriR88
Godspeed axes: (1) **independence** — counterfeits hand-written with `write`/`edit` text edits; `.ufo/waves/round-88/count-c2.py` and its `mutate_receipt` helper were never executed or imported; (2) **verbatim evidence** — every verdict line below is from a command I ran; (3) **control coverage** — clean-clone control plus the real-repo population, both re-measured.

## Revisions and bytes actually read

- Lane HEAD while working: `9c775ac2131da13c4c4cfdf2b14077184076f557` (read-only; no lane mutation of any kind, no commits to the lane).
- Frozen contract read via `git show 2a5e3ad96deb978ed1fb958e87b4be8221fb23b7:.ufo/waves/round-88/contract.md` (P-C2 + fixture table).
- Graded gate exported: `git -C fx show d5e2eda494877a85edaa4e287d6ad81843d9a8a1:.ufo/waves/round-87/count-c2.py > gate.py`
  sha256 `7e577f533e1dac676d3f5b3d601f2c4c622c57c325e6091e6018b5781ae73fc0  gate.py`
- Entering gate exported: `git -C fx show 1bd5ec3fa260458f74eb32a2e5bb157209c5934d:.ufo/waves/round-87/count-c2.py > gate-entering.py`
  sha256 `264a43f04af1f9f939da7b3890f608a669a0c7fc2922656ee83f35adb236b14d  gate-entering.py`
- Clone: `git clone --shared /home/vgpnk/Projects/shokunin/mori-shokunin $S/fx` then `checkout d5e2eda…`;
  toplevel check printed exactly: `TOPLEVEL: /fast/scratch/hyaku/mori-r88/Mo88E02C2Gate/fx`; HEAD = `d5e2eda494877a85edaa4e287d6ad81843d9a8a1`. Every commit was preceded by an assert that `git rev-parse --show-toplevel` printed the clone dir.

## Gate selftests (graded must be green at 23 arms)

```
--- graded selftest ---
... 23 PASS lines ...
C2_COUNTER_SELFTEST pass=23 fail=0
graded_selftest_rc=0
--- entering selftest ---
... 17 PASS lines ...
C2_COUNTER_SELFTEST pass=17 fail=0
entering_selftest_rc=0
```

## Verdict lines (verbatim, from my runs)

1. **Real population** (step 3): `TMPDIR=$S/scratch python3 -I $S/gate.py d5e2eda494877a85edaa4e287d6ad81843d9a8a1 --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch $S/scratch`
   ```
   C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=d5e2eda49487
   rc=0
   ```
2. **(d) clean control** — same gate over the unmutated clone:
   ```
   C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=d5e2eda49487
   rc=0
   ```
3. **(a) stripped** — `SHA_A=01edadbf5d5987326e9ac78eb6d4034dd9e16bfa`, graded gate:
   ```
   RECEIPT record-sweep-r87.txt expect=met failed problems=missing-replay
   C2=unmet receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=5 defeated=1 superseded=1 legacy=2 unexpected=1 detector=green rev=01edadbf5d59
   graded_rc=1
   ```
4. **(b) vacuous** — `SHA_B=e9198e2cca01eaca6b5337e72542c75e7135aee6`, graded gate:
   ```
   REPLAY record-sweep-r87.txt mode=clone rc=0 exported=1
   RECEIPT record-sweep-r87.txt expect=met failed problems=cmd-binding
   C2=unmet receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=5 defeated=1 superseded=1 legacy=2 unexpected=1 detector=green rev=e9198e2cca01
   graded_rc=1
   ```
5. **(c) absent-target** — `SHA_C=c75e7a04825692ca3d68cfe5ea49629d1b1017d0`, graded gate:
   ```
   SUPERSEDE claim-sweep-r87.txt target=gone-r88.txt absent=1
   C2=unmet receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=1 legacy=2 unexpected=1 detector=green rev=c75e7a048256
   graded_rc=1
   ```
6. **Entering gate over the same three fixture revs** (`gate-entering.py`, 17 arms):
   Stripped:
   ```
   RECEIPT record-sweep-r87.txt expect=met met problems=-
   C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=01edadbf5d59
   entering_rc=0
   ```
   Vacuous:
   ```
   RECEIPT record-sweep-r87.txt expect=met met problems=-
   C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=e9198e2cca01
   entering_rc=0
   ```
   Absent-target:
   ```
   SUPERSEDE claim-sweep-r87.txt target=gone-r88.txt absent=1
   C2=unmet receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=1 legacy=2 unexpected=1 detector=green rev=c75e7a048256
   entering_rc=1
   ```
   Entering accepts (a) and (b) outright, but already detects (c).

## Hand-built fixtures (commits only inside the scratch clone; identity `t <t@t>`)

```
c75e7a04825692ca3d68cfe5ea49629d1b1017d0 t <t@t> fixture: absent-target (supersedes gone-r88.txt)
e9198e2cca01eaca6b5337e72542c75e7135aee6 t <t@t> fixture: vacuous (cmd printf prints its own body)
01edadbf5d5987326e9ac78eb6d4034dd9e16bfa t <t@t> fixture: stripped (replay line removed, body fabricated)
```

**stripped** (`git show 01edadbf…:.ufo/waves/round-87/evidence/record-sweep-r87.txt`):
```
# receipt: record-sweep-r87.txt
# cmd: python3 -I tools/mori-record-sweep.py --root . --pins .ufo/waves/round-82/record-pins.json
# rev: 25a74d4c34e8430e4fbb18d4038ef5db872fb0ee
# counter-sha256: b8683be24e28ce4e79730b46615174d888af4c22ac7ee4fe16b97048516e8efa tools/mori-record-sweep.py
# supersedes: record-sweep-r85.txt
# limits: named limit — the body is the command's stdout in a --shared clone checked out at # rev:, so it reproduces from committed bytes; it supersedes the r85 worktree receipt and does not re-derive that receipt's bytes
# ---
RECORD_SWEEP fabricated=1
```

**vacuous** (`git show e9198e2c…:…record-sweep-r87.txt`):
```
# receipt: record-sweep-r87.txt
# cmd: printf 'RECORD_SWEEP fabricated=1\n'
# rev: 25a74d4c34e8430e4fbb18d4038ef5db872fb0ee
# counter-sha256: b8683be24e28ce4e79730b46615174d888af4c22ac7ee4fe16b97048516e8efa tools/mori-record-sweep.py
# replay: clone
# supersedes: record-sweep-r85.txt
# limits: named limit — the body is the command's stdout in a --shared clone checked out at # rev:, so it reproduces from committed bytes; it supersedes the r85 worktree receipt and does not re-derive that receipt's bytes
# ---
RECORD_SWEEP fabricated=1
```

**absent-target** (`git show c75e7a04…:…claim-sweep-r87.txt`):
```
# receipt: claim-sweep-r87.txt
# cmd: python3 -I tools/mori-claim-sweep.py --root . --pins .ufo/waves/round-80/claim-pins.json
# rev: 25a74d4c34e8430e4fbb18d4038ef5db872fb0ee
# counter-sha256: 4ac6b52615a427d1f7d8993ab636a5830bcde744c4a51f22d9157833d940ba1d tools/mori-claim-sweep.py
# replay: clone
# supersedes: gone-r88.txt
# limits: named limit — the body is the command's stdout in a --shared clone checked out at # rev: and reads pointers=266 where the r85 worktree receipt read 274, so the older count is not reproducible from committed bytes and this receipt is the reproducible successor, not a re-derivation of it
# ---
CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=4 pointers=266
```

Fixture hygiene: the observed diff for absent-target against d5e2eda showed only claim-sweep-r87.txt changed (one insertion, one deletion), confirming record-sweep was restored for that fixture. The vacuous command replay returned rc=0 and reproduced its fabricated body; its graded refusal was cmd-binding, not replay-mismatch.

## Honesty notes

- Execution deviation: initial selftests omitted `--scratch`. Source shows main creates and finally removes a temporary directory using the default tempdir; selfcheck reads its own source for marker_literal. Thus those invocations were not scratch-isolated as requested; no /tmp evidence is cited. Every population/replay invocation explicitly passed both TMPDIR=$S/scratch and --scratch $S/scratch.
- No tooling was installed (stock `git` + `python3` sufficed); nothing to record per the tooling authorization.
- Restores between fixtures used `git checkout d5e2eda… -- <path>` inside the clone only.

## Verdict

**C2 agrees.** All four fixture-table readings were measured exactly as the frozen P-C2 requires: clean `C2=met` with the r87 target tail on both the real repo and the unmutated clone; stripped → `problems=missing-replay` + `C2=unmet`; vacuous → `problems=cmd-binding` + `C2=unmet`; absent-target → `SUPERSEDE … absent=1` + `C2=unmet`; and the entering gate accepts the stripped and vacuous counterfeits whole (`C2=met`, rc 0). Independent of the r88 helper: reproduced with hand-written bytes only.

Exact commands (S=/fast/scratch/hyaku/mori-r88/Mo88E02C2Gate, FX=$S/fx):
```
git clone --shared /home/vgpnk/Projects/shokunin/mori-shokunin $S/fx
git -C $S/fx checkout d5e2eda494877a85edaa4e287d6ad81843d9a8a1
git -C $S/fx show d5e2eda494877a85edaa4e287d6ad81843d9a8a1:.ufo/waves/round-87/count-c2.py > $S/gate.py
python3 -I $S/gate.py --selftest                                   # pass=23 fail=0
python3 -I $S/gate.py d5e2eda494877a85edaa4e287d6ad81843d9a8a1 --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch $S/scratch   # C2=met
python3 -I $S/gate.py d5e2eda494877a85edaa4e287d6ad81843d9a8a1 --repo $S/fx --scratch $S/scratch                                         # clean control C2=met
# hand edits + commits (01edadbf…, e9198e2c…, c75e7a04…) then:
TMPDIR=$S/scratch python3 -I $S/gate.py 01edadbf5d5987326e9ac78eb6d4034dd9e16bfa --repo $S/fx --scratch $S/scratch
TMPDIR=$S/scratch python3 -I $S/gate-entering.py 01edadbf5d5987326e9ac78eb6d4034dd9e16bfa --repo $S/fx --scratch $S/scratch
TMPDIR=$S/scratch python3 -I $S/gate.py e9198e2cca01eaca6b5337e72542c75e7135aee6 --repo $S/fx --scratch $S/scratch
TMPDIR=$S/scratch python3 -I $S/gate-entering.py e9198e2cca01eaca6b5337e72542c75e7135aee6 --repo $S/fx --scratch $S/scratch
TMPDIR=$S/scratch python3 -I $S/gate.py c75e7a04825692ca3d68cfe5ea49629d1b1017d0 --repo $S/fx --scratch $S/scratch
TMPDIR=$S/scratch python3 -I $S/gate-entering.py c75e7a04825692ca3d68cfe5ea49629d1b1017d0 --repo $S/fx --scratch $S/scratch
```

Blockers: none. Scratch clone deleted before yield.

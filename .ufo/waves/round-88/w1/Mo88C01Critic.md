# Mo88C01Critic — round 88 w1 adversarial review (C1 operability, C2 calibration)

seat: Mo88C01Critic · date: 2026-11-04 · leaf: no subagents, no lane writes except this report.
Bytes read (pinned by `git show`, sha256 over file bytes):
- frozen at `2a5e3ad96deb978ed1fb958e87b4be8221fb23b7`: `contract.md` bc154e2b065b3455…, `count-c1.py` d1048cf06ae31bd1…, `count-c2.py` 8904a3d0b5d973b5…, `evidence/controls-r88.txt` 7b53d4aa87e79b4c…
- work under test at `4d0f7bf0b0a0d978fa65d9b93edc37a2e6556550`: `round-87/count-c1.py` ee505a3e1cb0fdce…, `round-87/count-c2.py` 7e577f533e1dac67…
- tally fix `d5e2eda494877a85edaa4e287d6ad81843d9a8a1`; after receipt = lane HEAD at read time `9c775ac2131da13c4c4cfdf2b14077184076f557` (`after-r88.txt` 31678d6296ba6c22…; absent from the freeze commit — it landed later). Entering `1bd5ec3fa260458f74eb32a2e5bb157209c5934d`.
- ancestry verified: 2a5e3ad → 4d0f7bf → d5e2eda → 9c775ac linear; d5e2eda is not an ancestor of the freeze.

Baseline first (honesty: I reproduced both after lines myself before attacking):

```
$ python3 -I <frozen>/count-c1.py d5e2eda494877a85edaa4e287d6ad81843d9a8a1 --repo <shared clone at d5e2eda> --scratch <scratch>/run-c1-base
C1=met mutants=6 killed=6 survivors=0 total=6 arms=24 rev=d5e2eda49487   (rc=0)
$ python3 -I <frozen>/count-c2.py d5e2eda… --repo <shared clone> --scratch <scratch>/run-c2-base
C2=met real=met fx=4 clean=1 refused=2 absent=1 arms=23 rev=d5e2eda49487  (rc=0)
```

All probes ran in scratch fixtures: `git clone --shared` of the lane, `checkout <rev>`, receipt/subject bytes edited, committed with `-c user.name=t -c user.email=t@t`, `git rev-parse --show-toplevel` asserted equal to the fixture dir before each commit. Scratch deleted after the run.

---

## ATTACK C1-vacuity result=succeeded

A subject for `.ufo/waves/round-87/count-c1.py` that implements none of the counter machinery
and asserts nothing: its `--selftest` prints the only line the frozen counter reads
(`COUNTER_SELFTEST pass=24 fail=0`) and dies only when its own marker block — which carries the
six frozen anchors — stops matching a pinned checksum. No grade(), no met, no arms; six vacuous
"cases" would be indistinguishable because the counter never looks past the tally line.

Fixture: fresh git repo, canary at `.ufo/waves/round-87/count-c1.py`, committed as above,
rev `79143f945e424b79892e730c431d5659ca0d07a7`.

```
$ python3 -I <frozen>/count-c1.py 79143f945e424b79892e730c431d5659ca0d07a7 --repo <canary fixture> --scratch <scratch>/run-c1-vac
MUTANT count-c1.py M1-met-no-guard killed rc=1
MUTANT count-c1.py M2-met-drop-empty killed rc=1
MUTANT count-c1.py M3-killed-n killed rc=1
MUTANT count-c1.py M4-arms-total killed rc=1
MUTANT count-c1.py M5-split-field killed rc=1
MUTANT count-c1.py M6-anchor-guard killed rc=1
C1=met mutants=6 killed=6 survivors=0 total=6 arms=24 rev=79143f945e42
rc=0
```

The counter refused nothing: every clause of P-C1's letter is satisfied by a subject whose
mutants die by self-recognition (the frozen kill rule is "rc≠0 or fail=<n> n>0" — a checksum
canary, a syntax error, or a stall/timeout all qualify). `C1=met` therefore does not imply the
six contract arms exist or do anything. The C1b label-only control blocked labels added to an
otherwise-real counter; it does not block an arms-free subject.

## ATTACK C1-kill-attribution result=blocked

Mirrored the frozen counter's mutation application (count==1 guard, `str.replace`) on the real
`.ufo/waves/round-87/count-c1.py` at d5e2eda and ran each mutated copy's `--selftest`:

```
== M1-met-no-guard occurrences=1   rc=1 pass=22 fail=2
   FAIL met_guard_unanchored …   FAIL met_guard_empty …          (both contract-named)
== M2-met-drop-empty occurrences=1 rc=1 pass=23 fail=1
   FAIL met_guard_empty …                                        (named)
== M3-killed-n occurrences=1      rc=1 pass=23 fail=1
   FAIL killed_tally_mixed …                                     (named)
== M4-arms-total occurrences=1    rc=1 pass=23 fail=1
   FAIL arms_tally_passed …                                      (named)
== M5-split-field occurrences=1   rc=1 pass=23 fail=1
   FAIL target_split_killed_not_mutants …                        (named)
== M6-anchor-guard occurrences=1  rc=1 pass=22 fail=2
   FAIL met_guard_unanchored …   FAIL doubled_anchor_counted_type …  (named + one r88 cross-fire)
```

No mutant dies because of a pre-existing (entering-18) arm: every FAIL line belongs to a
round-88 arm, and M6's extra killer (`met_guard_unanchored`, M1's arm) is a new arm cross-firing,
not an older one. Attribution is sound. [INFERENCE from the failure mode, not run]: on the
entering bytes the six arms alone would not kill M1/M2 — without the d5e2eda fixture-tally lines
those fixtures are `pristine-arms`-refused, so `(not met)` holds even under the mutants; the
tally fix is load-bearing for the kill, as its own commit message says.

## ATTACK C2-vacuity result=blocked

Graded counter = `.ufo/waves/round-87/count-c2.py` at the fixture rev, run directly over each
fixture (probe output abridged to the decisive lines):

- `# replay: none` + waiver on the `record-sweep-r87.txt` clone row, d5e2eda:
  `RECEIPT record-sweep-r87.txt expect=met failed problems=missing-replay` → `C2=unmet … unexpected=1` (rc=1).
- `required` row (`after-c1-r86.txt`) with its `# replay: required` header stripped:
  `RECEIPT after-c1-r86.txt expect=met failed problems=missing-replay` → `C2=unmet` (rc=1).
- row whose `# cmd:` is `true`: `RECEIPT record-sweep-r87.txt … problems=cmd-binding,replay-mismatch` → `C2=unmet` (rc=1).
- all four replay lines stripped (zero replays) at d5e2eda: all four rows `problems=missing-replay`, `C2=unmet … unexpected=3` (rc=1).
- same zero-replay fixture at the entering bytes 1bd5ec3f: no REPLAY lines executed, but
  `RECEIPT replay-defeat-r86.txt expect=reject met problems=-` → `unexpected=1` → `C2=unmet` (rc=1):
  the REAL tail's `defeated=1` itself requires the defeat row to fail a real replay, so even the
  entering gate never printed `real=met` with zero replays.

Zero replays cannot reach the target line at either revision.

## ATTACK C2-no-harm result=succeeded (false-positive class; frozen P-C2 scope unaffected)

Against the graded counter at d5e2eda, mutating only `record-sweep-r87.txt`'s `# cmd:` (replay
and body otherwise genuine):

- single quotes `'tools/mori-record-sweep.py'`: accepted, `C2=met` full REAL tail (rc=0).
- double quotes `"tools/mori-record-sweep.py"`: accepted, `C2=met` full REAL tail (rc=0).
- `true; python3 -I tools/mori-record-sweep.py …`: accepted, `C2=met` (rc=0) — a clean token
  after `;` passes.
- `./tools/mori-record-sweep.py` (same file, replay rc=0, body matched):
  `RECEIPT record-sweep-r87.txt expect=met failed problems=cmd-binding` → `C2=unmet` (rc=1).
  The binding rule matches token spelling, not path identity: a semantically identical genuine
  command is refused. This is the false-positive class; it does not touch the real
  seven-receipt population (measured `C2=met` at d5e2eda), so P-C2's own no-harm scope holds.
- literal `--opt=tools/mori-record-sweep.py`: refused with `problems=replay-rc:2,replay-mismatch`
  (the command is genuinely broken there, so this variant is not a clean genuine-receipt case;
  `./` is the clean demonstration).

## ATTACK C2-selfprint-own result=succeeded (calibration caveat; pinned predicate unaffected)

The contract sentence "a receipt whose `# cmd:` prints its own body reads `cmd-binding`" is only
true for bodies that omit the bound path tokens. A receipt with

```
# cmd: printf 'RECORD_SWEEP fabricated=1 tools/mori-record-sweep.py \n'
```

and the matching fabricated body line replays rc=0, matches its body, carries its bound path as
a cmd token — the graded counter at d5e2eda prints
`RECEIPT record-sweep-r87.txt expect=met met problems=-` and the exact `C2=met` REAL tail (rc=0).
Running the frozen r88 C2 counter over that fixture rev (`3e84f588bad2…`) prints the complete
target line:

```
C2=met real=met fx=4 clean=1 refused=2 absent=1 arms=23 rev=3e84f588bad2   (rc=0)
```

i.e. the gate refuses the two frozen counterfeits but not the class "cmd prints its own body".
The claim pinned at d5e2eda stays true (its real receipts are genuine); the calibration property
sold by the sentence is fixture-specific, not class-wide.

## ATTACK contract-drift result=findings (no target-string divergence)

1. P-C2 shorthand vs operational rule: contract.md says self-printing bodies are refused;
   the counter (and its docstring parenthetical "every `# counter-sha256:` path must appear in
   the command") implements token presence — divergence demonstrated by C2-selfprint above.
2. Contract fix item 2 says "legacy rows keep the header-only rule"; the call site applies
   binding to any row with a replay line, including legacy rows
   (`replay_mode in ("required", "clone") or fields["replay"] is not None`). Unobservable in the
   real population (the legacy trio carries no `# replay:` lines).
3. Contract C1 arm table quotes `target_split("… arms=24")` for `target_split_killed_not_mutants`;
   the same-named arm inside the r87 subject uses `arms=54` (its own TARGET_ARMS). Cosmetic — each
   copy tests its own constant; the contract text describes only the r88 copy.
4. P-C1's "Exit 2 is setup, never a pass" concerns the counter's own exits; a mutated copy
   exiting 2 (or timing out, rc=124) still counts as killed under the frozen kill rule — same
   vacuity family as the canary.
5. Otherwise the P-C1/P-C2 sentences, both docstrings, TARGET/TARGET_ARMS constants and printed
   strings agree (`mutants=6 killed=6 survivors=0 total=6 arms=24`; `real=met fx=4 clean=1
   refused=2 absent=1 arms=23`; fixtures and mutations match the frozen tables).

---

C1 falsifiable: yes — target line reproduced on an arms-free canary subject
(rev `79143f945e424b79892e730c431d5659ca0d07a7`) by the frozen counter.
C2 falsifiable: no — every vacuity probe blocked at d5e2eda and at entering; the pinned line is
genuine there and the do-nothing/label-only controls stand.

Strongest surviving attack: the C1 checksum canary — the frozen kill rule cannot attribute a
kill to the declared arm, so `C1=met` is forgeable without any of the work. Smallest safe
correction for the canonical judge to weigh: require the mutated copy's own `--selftest` to name
its killer (kill counts only when the contract-declared arm label appears in the mutant's FAIL
lines, with the pristine output byte-identical except for the mutation). For C2, the honest
defects are outside the pinned predicate: token-spelling false positives (`./`, `--opt=`) and
the self-printing-body evasion; a first token check rejecting `printf`/`echo` commands on
replayed rows would close the latter narrowly.

Verdict I measured: baseline `C1=met mutants=6 killed=6 survivors=0 total=6 arms=24` (rc=0) and
`C2=met real=met fx=4 clean=1 refused=2 absent=1 arms=23` (rc=0) at d5e2eda both reproduce;
C1's line is additionally reproducible without the work (canary, rc=0); C2's is not.

Tooling: nothing installed or upgraded (pacman paused per orchestrator ruling); only preinstalled
`git` and `python3` were used. Scratch `/fast/scratch/hyaku/mori-r88/Mo88C01Critic/` deleted
after the run; no lane file other than this report was written.

# Mo56CritC2CounterFences — fence attack on the round-56 C2 counter

Seat: Mo56CritC2CounterFences (leaf critic, mori-shokunin lane). Date: 2026-10-27.
Target: the frozen counter at
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/count-c2.py`
(predicate P-C2; PIN 8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca
for `tools/mori-vote-bind.py`).
Method: scratch fixture revisions. One `git clone --shared` of the lane repo was
made under the seat scratch dir; four branches sit on the freeze tip
`8be2717b0809281d07dffe83dad424a4859e0747`; the frozen counter was executed
**unmodified** against each fixture revision through its `--repo` switch. No
counter, contract, tool, entry, row, or fleet file was modified. No tools were
installed; no network was used. Scratch lived under
`/fast/scratch/hyaku/mori-r56/Mo56CritC2CounterFences/` and was removed after
this report was written; every cited output is copied here.

## Harness control (M0)

Command: `python3 .ufo/waves/round-56/count-c2.py 8be2717b0809281d07dffe83dad424a4859e0747 --repo <clone>`
Output:
```
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
```
Exit: 0. The clone reproduces the frozen fleet receipt
(`.ufo/waves/round-56/evidence/c2-at-freeze.txt`, modulo the stamped rev), so a
mutant's `unmet` verdict is attributable to the mutant, not the harness.

Fixture note: an earlier attempt with plain single-commit fixture repos failed
the contrast arm environmentally — the frozen round-55 C1 counter requires its
frozen entering-tip commit `ca52426ea496bc6592e3e867cc9d28843e45f196` to resolve
in the measured repo; it resolves in the fleet repo both as a loose object and
via `refs/jj/keep/<sha>`. Plain scratch repos lack that object, so the arm
failed with `contrast=bad` for a reason unrelated to any mutant. A shared clone
carries fleet object history through alternates and behaves like the fleet.

## Fence 1 — a binder that binds substring (overclaim)

Mutant branch `fence-M1` = freeze tip + one commit (scratch rev
`2361e62d0d36cc27419a5e93caf991f583bb7e8f`), tool sha256
`7f1be4eecba3623db82ca9c92d873b6ed8579990ac539f6dd014a3fe89152efc`
(PIN mismatch by construction). Diff vs the freeze tip
(`tools/mori-vote-bind.py`):

```diff
-VOTE_RE = re.compile(r"^(RECHECK|ENTAIL)\s+([0-9a-f]{12})\s+([A-Za-z][A-Za-z0-9_-]*)(?:\s(.*))?$")
+VOTE_RE = re.compile(r"(RECHECK|ENTAIL)\s+([0-9a-f]{12})\s+([A-Za-z][A-Za-z0-9_-]*)(?:\s(.*))?$")
@@ extract_votes, JSON channel @@
-            m = VOTE_RE.match(s.strip())
+            m = VOTE_RE.search(s.strip())
@@ extract_votes, text channel @@
-        m = VOTE_RE.match(line.strip())
+        m = VOTE_RE.search(line.strip())
```

The `^` anchor is dropped from the pattern **and** `match` becomes `search`, so
any scalar or unfenced line merely containing a vote sentence binds.

Direct behavior (scratch, against the committed round-55 ledger +
`w1-results.json`):

- selftest: `VOTE_BIND_SELFTEST pass=14 fail=2 failed=t_fenced_scalar_ignored,t_json_prose_substring_rejected`, exit 1 — the mutant genuinely overclaims.
- Overclaim probe: a JSON string scalar of the prose shape "the claim is `<verb>` `<hash12>` `<word>` today, surely" now binds (`{('RECHECK', 'a6e5226259c9'): 'holds'}`, channel json); the anchored tool rejects the same scalar.
- Tally over the committed bytes:
  `TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15`
  — byte-identical to the counter's expected line.
- Junk-results tally: `TALLY rows=78 agree=0 double=0 single=0 zero=78 dissent=0 voters=16 bound_voters=0` — satisfies the control shape (`zero=78`, `double=0`).
- Per-output analysis on the committed bytes: anchored vs substring binding
  yield identical final-vote sets on all 16 voter outputs (0 added, 0
  changed) — the overclaim changes nothing on these inputs, which is why the
  tally line is invariant.

Frozen counter verdict:
Command: `python3 .ufo/waves/round-56/count-c2.py 2361e62d0d36cc27419a5e93caf991f583bb7e8f --repo <clone>`
Output:
```
C2=unmet selftest=bad tally=ok control=ok contrast=voted0 entry=ok row=ok rev=2361e62d0d36cc27419a5e93caf991f583bb7e8f failed=pins,selftest
```
Exit: 1.

Verdict: **tally arm BYPASSED; control arm BYPASSED; KILLED by the selftest arm
(and the pin).** The tally arm does not catch a substring overclaimer: no voter
output in the committed round-55 results carries a prose-embedded vote
sentence, so overclaim is observationally invisible there, and the junk control
text contains no vote grammar at all, so neither the tally arm nor the control
arm can see the overclaim. The only functional guard is the tool's own
selftest (the two overclaim cases named above).

## Fence 2 — a binder that hardcodes the TALLY line regardless of inputs

Mutant branch `fence-M2` = freeze tip + one commit (scratch rev
`301213251436198adde72a9406e90c21613e556e`), tool sha256
`441cd867504bcacbd64a1601b72327f5001b7b1f33fe4a25d01f332a4d8b5f7`
(PIN mismatch by construction). Full mutant source:

```python
#!/usr/bin/env python3
"""FENCE MUTANT M2: prints the expected selftest and TALLY lines regardless
of any inputs. It never opens --ledger or --results."""
import sys

if "--selftest" in sys.argv:
    print("VOTE_BIND_SELFTEST pass=16 fail=0")
    sys.exit(0)
if "tally" in sys.argv:
    print("TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 "
          "voters=16 bound_voters=15")
    sys.exit(0)
sys.exit(0)
```

Direct behavior (scratch): selftest prints `VOTE_BIND_SELFTEST pass=16 fail=0`,
exit 0; on the real ledger it prints the expected TALLY line; on the junk
results it prints the very same TALLY line; it never opens any file.

Frozen counter verdict:
Command: `python3 .ufo/waves/round-56/count-c2.py 301213251436198adde72a9406e90c21613e556e --repo <clone>`
Output:
```
C2=unmet selftest=bad tally=ok control=bad contrast=voted0 entry=ok row=ok rev=301213251436198adde72a9406e90c21613e556e failed=pins,control
```
Exit: 1.

Verdict: **tally arm BYPASSED; KILLED by the control arm (and the pin).** A
constant printer satisfies the tally arm exactly, because the tally arm is a
stdout substring match on one fixed input. The control arm kills it since the
junk run must print `zero=78` and `double=0`, and the hardcoded line carries
`zero=0 double=68`. Display note: the `selftest=bad` field in this receipt is
the print statement's mapping of `pins` into the selftest slot (the counter
prints "bad" if either "selftest" or "pins" is in the failed list); the mutant
actually passes the selftest arm itself, as the direct run shows
(`pass=16 fail=0`).

## Fence 3 — a binder that reads the ledger from a hardcoded source, ignoring --ledger

Mutant branch `fence-M3` = freeze tip + one commit (scratch rev
`cfe25f607eda10feafcc89789ae68cbfa49e8d98`), tool sha256
`69ddb792f2f5f87f1e1fae620a3b59a2b4d553ea9868545005f8929b3ad2e213`
(PIN mismatch by construction). Diff vs the freeze tip (excerpt): the real tool
is unchanged except that (a) a module constant `EMBEDDED_LEDGER` carries a
verbatim copy of the committed round-55 ledger, and (b) the tally branch writes
`EMBEDDED_LEDGER` to a temp file and tallies over that file, never opening the
`--ledger` argument. The 16-case selftest suite is untouched.

Direct behavior (scratch): selftest `VOTE_BIND_SELFTEST pass=16 fail=0`, exit 0;
tally over the committed bytes prints the expected
`TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15`;
the junk-results tally prints `zero=78 double=0` exactly like the real tool —
because the embedded ledger copy is byte-identical to the committed one and the
results argument is still honored.

Frozen counter verdict:
Command: `python3 .ufo/waves/round-56/count-c2.py cfe25f607eda10feafcc89789ae68cbfa49e8d98 --repo <clone>`
Output:
```
C2=unmet selftest=bad tally=ok control=ok contrast=voted0 entry=ok row=ok rev=cfe25f607eda10feafcc89789ae68cbfa49e8d98 failed=pins
```
Exit: 1.

Verdict: **BYPASSED on every functional arm — selftest ok, tally ok, control
ok, contrast voted0, entry ok, row ok; KILLED only by the pin.** A binder that
ignores the `--ledger` argument entirely sails through the frozen counter; if a
malicious tool revision were ever landed and re-pinned, the counter as frozen
would print `C2=met` for it. (`selftest=bad` in the receipt is again the
pins-into-display mapping; the failed list contains only `pins`.)

## Verdict table

| fence | selftest arm | tally arm | control arm | overall |
|---|---|---|---|---|
| M1 substring overclaim | KILLED (overclaim cases) | BYPASSED | BYPASSED | KILLED — not by the tally arm |
| M2 hardcoded TALLY line | passed | BYPASSED | KILLED | KILLED — by the control arm |
| M3 ignores --ledger | passed | BYPASSED | BYPASSED | KILLED only by PIN |

## Named limits and round-57 routes

No frozen artifact change is proposed for round 56; these are named limits
with routed items.

1. The tally arm is a single-input stdout string match (count-c2.py:100-102),
   so it cannot detect input-independence. The control arm varies only
   `--results`, never the ledger (count-c2.py:103-115), hence fence 3's full
   functional bypass. Route for round 57: add a ledger-variant control (e.g.,
   flip dispositions in a copied ledger, require a matching, different TALLY)
   so ledger-ignoring binders are detected by the counter itself.
2. Overclaim visibility currently rests on the tool's embedded selftest, not
   on the counter's tally arm (fence 1). A mutant that also neutralized its
   selftest overclaim cases would pass every functional arm of the frozen
   counter. Route for round 57: extend the tally/control inputs (outputs
   carrying prose-embedded vote sentences) so the tally arm detects overclaim
   on its own.
3. Cosmetic: count-c2.py's final print maps `pins` into the `selftest=` display
   slot, so receipts read `selftest=bad` both when the selftest arm fires and
   when only the pin fails (fences 2 and 3). Route for round 57: give pins its
   own display slot.

## Process notes

- Host guard observed: the shell cwd stayed inside the seat scratch dir for
  every command that wrote anything; the only write into the lane repo is this
  report file. All fleet git use was read-only (`show`, `log`, `diff`,
  `rev-parse`, `cat-file`); clones, branches, and commits existed only inside
  the scratch dir and were deleted on completion.
- Disk guard before the runs: `/fast` at 28% use, 582.5G free
  (`scripts/hyaku/disk-guard.sh status`). No ENOSPC encountered.
- Tooling installs/upgrades: none.
- Investigation dead end, recorded for honesty: while diagnosing the fixture
  contrast arm I briefly typed a mistyped object id (…`c196` for the counter's
  actual …`f196` entering tip) and read the fleet object store as flaky;
  byte-level comparison of the ENTER constant, the on-disk loose object, and
  `refs/jj/keep/<sha>` confirmed the store is consistent and the error was my
  transcription. No fleet-liveness finding.
- UNVERIFIED: none — every command cited above was executed in this session and
  its output copied here; the scratch fixture revisions named above were
  removed after the report was written, so the branch ids are no longer
  resolvable.

## Findings

- HIGH — count-c2.py:100-115 (`evaluate` tally and control arms): fence 3
  (ledger-ignoring binder) BYPASSES every functional arm; the frozen counter
  kills it only through the pinned tool sha256. Smallest safe correction is a
  round-57 routed item: a ledger-variant control arm, not a change to any
  round-56 frozen artifact.
- MED — count-c2.py:100-115 (tally/control arms): substring-overclaim binding
  is invisible to the tally and control arms on the committed round-55 bytes;
  the working guard lives in `tools/mori-vote-bind.py`'s selftest cases
  (`t_json_prose_substring_rejected`, `t_fenced_scalar_ignored`). Composable
  with selftest gaming (fence 2 style) to a full functional bypass.
- MED — count-c2.py:100-102 (tally arm): satisfiable by a constant printer on
  the fixed input; the control arm (count-c2.py:103-115) carries the detection
  for that class (fence 2).
- LOW — count-c2.py `main()` print: `selftest=bad` conflates a pins failure
  with a selftest-arm failure in receipts (observed in the M2/M3 receipts).
- LOW — contrast arm requires the round-55 entering-tip commit
  `ca52426ea496bc6592e3e867cc9d28843e45f196` to resolve in the measured repo
  (satisfied in the fleet repo by a loose object plus `refs/jj/keep/<sha>`);
  fixture repos that lack fleet object history fail this arm
  environmentally (`contrast=bad`) rather than for cause.

Report: .ufo/waves/round-56/w1/Mo56CritC2CounterFences.md

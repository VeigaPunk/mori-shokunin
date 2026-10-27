# Mo56RevClaims — contract-vs-AXES verification and predicate wording attack (round 56, w1)

Seat scope: verify the two frozen claims against AXES.md rules; attack predicate
wording for ambiguity a closure could mis-read. Measured at freeze tip
`8be2717b0809281d07dffe83dad424a4859e0747`; do-nothing baseline at entering tip
`5b295eeebd87ebd610d8d39bfe2035742f740cfa`. All commands run from scratch
`/fast/scratch/hyaku/mori-r56/Mo56RevClaims/` with `TMPDIR` under it; the lane
repo was only read (`git show`/`ls-tree`/`rev-parse`, no mutations).

## Rule 1 — distinct owned axes: HOLDS

`SCORECARD.md:3` declares "Axes owned by this lane: **coverage + operability**
(fleet-2); all six are scored". C1 targets coverage (6), C2 targets operability
(7): distinct, both owned, and coverage is the lowest-scoring owned
non-retired axis (operability 7; `## Retired` at `SCORECARD.md:42` reads
"None."), so the lowest-axis obligation in `AXES.md:33` is satisfied as the
lane has always read it ("lowest owned non-retired axis", `SCORECARD.md:833,
927`). C2 is declared a capability acquisition — `AXES.md:40-41` permits this
("it still lands a per-axis verdict, with the claim type recorded"), and the
contract records the type in the heading "operability (capability)".

Ambiguity (LOW): `AXES.md:33` says "the lane's **lowest-scoring non-retired
axis**" — it does not say "owned". A literal reading scores depth/freshness/
calibration at 5 (below coverage 6), which would require one of those axes
instead. The lane's own ledger uses "owned" consistently (`SCORECARD.md:833`),
but the AXES text itself never defines "owned"; a hostile closure could cite
the unqualified wording. Round-57 wording-tightening candidate, not a defect
in this round's contract.

## Rule 2 — causally separable: HOLDS

Checked file sets are disjoint:

| arm | C1 | C2 |
|---|---|---|
| tool | `tools/mori-driver-liveness.py` (pin `6b3dba74…`) | `tools/mori-vote-bind.py` (pin `8be1acdb…`) |
| entry | `corpus/knowledge/driver-liveness-r56.md` | `corpus/knowledge/vote-binding-r56.md` |
| row | SOURCES.md S544 | SOURCES.md S545 |
| extra | `fixtures/driver/*` | r55 ledger, r55 results, **r55** `count-c1.py` |

Shared files: exactly one — `corpus/SOURCES.md` (contract line 34 says
precisely this: "no shared file except the registry append"). The row checks
are anchored to distinct first cells (`^\s*\|\s*S544\s*\|` vs `…S545…`,
count-c1.py:156, count-c2.py:127), so neither counter can be satisfied or
broken by the other's row. `contract.md` is shared but no predicate reads it.
C2's contrast arm executes **round-55's** count-c1 (`R55_C1 =
".ufo/waves/round-55/count-c1.py"`, count-c2.py:41) — a different file from
this round's `count-c1.py`, so there is no C1→C2 dependency. Each counter
evaluates at R independently; verified (both ran green at the freeze tip with
the other claim's data irrelevant to the run).

## Rule 3 — one falsifying command each: HOLDS

`python3 .ufo/waves/round-56/count-c1.py R` and `count-c2.py R` (default
`--repo` is the lane). My independent run of the frozen counters materialized
at `8be2717b` (shas `c4e58eed…`, `4b350c77…` = `freeze-sha256.txt`):

```
$ python3 count-c1.py 5b295eee… --repo <lane>   # exit=1
C1=unmet selftest=bad fixtures=bad entry=bad row=bad norem=bad failed=tool_absent rev=5b295eeebd87ebd610d8d39bfe2035742f740cfa
$ python3 count-c2.py 5b295eee… --repo <lane>   # exit=1
C2=unmet selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=5b295eeebd87ebd610d8d39bfe2035742f740cfa failed=tool_absent
$ python3 count-c1.py 8be2717b… --repo <lane>   # exit=0
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
$ python3 count-c2.py 8be2717b… --repo <lane>   # exit=0
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
```

Tool shas at the data commits reproduce the frozen PINs exactly
(`git show 6ced9da9:tools/mori-driver-liveness.py | sha256sum` →
`6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997`;
`git show c419fe6d:tools/mori-vote-bind.py` →
`8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca`).

Caveat on "one command": the counter writes temp trees under `TMPDIR` and
execs `git`/`python3` — the command is one line but not side-effect-free;
a closure on a host without `git` gets exit 2 (setup), honestly labeled.

## Rule 4 — no do-nothing reachability: HOLDS (with a labeling defect)

Both tools are absent at `5b295eee` (`git ls-tree`/`cat-file -e` verified), so
a no-op lands `unmet` for both — my runs above. The committed receipt
`evidence/controls.txt` is consistent: `controls.py:92` truncates each verdict
to 110 chars, which is why `do-nothing-c2` shows no `failed=` (the full string
contains `failed=tool_absent`; `PASS` is computed on the untruncated verdict).
Truncated rev fields are the same 110-char cut, not corruption.

**Defect found (MED):** `count-c2.py` has no `tool_absent` output branch
(unlike count-c1.py:188-191). `failed=["tool_absent"]` maps to **every named
field `ok`/`voted0`** — a reader sees `C2=unmet` with all green fields and no
cause after truncation. Worse, the same mapping lies for
`r55_artifacts_absent` (early return, count-c2.py:76: fields print
`ok`/`voted0` though tally/control/contrast never ran) and `contrast_absent`
(prints `contrast=voted0` though the arm never ran — the one field that
asserts a *measured* fact). The verdict and exit code stay honest; only the
field labels misreport. Frozen → round-57 routed item: give C2 the same
absent-tool/absent-artifact print branch C1 has, and map
`contrast_absent`/`r55_artifacts_absent`/`pins` to visible fields.
`count-c1.py` has the milder form: `failed=pins` appears only in `failed=`,
while `selftest=ok` prints (pins is folded into selftest only in C2).

## Rule 5 — no unenforced universal clause: HOLDS with two wording-vs-implementation gaps

Every universal in the contract is enumerated inside the counters, but two
enumerations are narrower than the words:

1. **(MED) "the tool text at R contains no health-verdict string"** —
   the counter scans only `tool_src.split("# selftest", 1)[0]`
   (count-c1.py:162), the text *before* the `# selftest` comment at
   `tools/mori-driver-liveness.py:248`. The committed tool already contains
   `"healthy"`, `"unhealthy"`, `"failed lane"` at line 422 (inside
   `t_no_health_verdict`'s selftest guard) — literally violating the
   predicate's universal while `norem=ok`. Any future health-word anywhere
   after line 248 escapes the check forever. Also asymmetric: `HEALTH_WORDS`
   scans **five** strings (adds "is stuck", "wedged", count-c1.py:45) while
   the docstring/contract list only three — the kill list is wider than the
   predicate discloses. A closure reading the predicate literally would call
   the tool violating; a closure reading it charitably ("no health-verdict
   *emitted*") over-trusts a prefix scan.
2. **(LOW) "every frozen fixture parses with its frozen malformed count" /
   "every fixture subdirectory that carries a watchdog.log"** — the counter
   enumerates nine named dirs (`EXPECT_FIX`, count-c1.py:40-44); an extra
   fixture added under `fixtures/driver/` is materialized but never checked
   (the `n` count from `materialize_fixtures` is discarded). The literal
   "every subdirectory" claim is broader than the enforcement.

## Wording attack — further ambiguities a closure could mis-read

- **(LOW) C2 "prints exactly the line `TALLY …`"** — implemented as
  `EXPECT_TALLY not in p.stdout` (count-c2.py:96): substring, not line
  equality; stdout may contain anything else. Same for the selftest line
  (count-c2.py:90, count-c1.py:131). "Exactly" overspecifies.
- **(LOW) C2 contrast accepts `p.returncode in (0,1)`** (count-c2.py:119):
  a `C1=met … voted=0` output from the r55 counter would also pass the arm;
  "still prints voted=0" doesn't require the unmet verdict.
- **(LOW) C2 "voters=16"** is roster cardinality (`len(roster)`,
  mori-vote-bind.py:201), not voters-who-voted; the true bound count is
  `bound_voters=15`. A closure reading `voters=16` as "16 votes seen"
  mis-reads it. The results file has 64 seats; the roster filters to the 16
  `Mo55Rc*` names — verified.
- **(LOW) "BOTH plain-text and JSON string-scalar shapes"** — `extract_votes`
  binds exactly **one** channel per output: a JSON-parsable output takes the
  `json` path and returns early (mori-vote-bind.py:89-95), so plain-text
  votes in the same output are silently dropped. "Both" describes two
  alternative shapes, not concurrent channels — the mutants
  `text-channel-closed`/`json-channel-closed` confirm per-channel kill
  coverage, and the JSON channel binds *any* string at *any* nesting depth
  via `_walk_strings`, which is broader than "string-scalar" suggests
  (a `"RECHECK <h> <w>"` string inside a deeply nested note binds).
- **(LOW) ENTAIL asymmetry**: the regex binds `ENTAIL` votes
  (VOTE_RE:64), but `read_ledger` only fills dispositions for the verb
  `RECHECK` (mori-vote-bind.py:152-153); `tally --verb ENTAIL` silently
  tallies `rows=0`. The predicate says "seat-output votes" generally — fine
  for this round's RECHECK surface, but the ENTAIL half is extraction-only.
- **(LOW) `--min`/`min_votes` is dead plumbing** (mori-vote-bind.py:161,202,
  418): parsed, echoed into the result dict, never enforced — the TALLY line
  has no quorum. Nothing in the predicate promises one; noted as tool debt.
- **(LOW) entry/row substring checks**: `"S544" in entry` could match
  `S5440`, `"mined" in row` is unanchored (matches "unmined"), and
  used-by-entry is satisfied by the entry path appearing anywhere in the
  S544 row, not specifically the last cell. The row-id match itself is
  anchored to the first cell, which is correct.
- **(LOW) capability-table row not pinned**: C2 is a capability acquisition;
  `AXES.md:61-64` requires the repertoire-table row enter through a
  demonstrated round. The counter does not check the SCORECARD capabilities
  table — C2=met can land while the row is forgotten (L1 bookkeeping gap,
  not a predicate failure).
- **(LOW) counter selftests are trivial constants**
  (count-c1.py:171, count-c2.py:138): `len(EXPECT_FIX)==9` /
  `len(VOTERS)==16` and a prefix check — `pass=1 fail=0` proves almost
  nothing, though honestly labeled.
- **(LOW) C1 fixture arm can KeyError**: `doc["log"]["malformed"]`
  (count-c1.py:146) isn't guarded — a fixture report without `log` crashes
  the counter (exit≠0, no `C1=` line): still an honest non-met signal, but
  by exception, not verdict.
- **(INFO) freeze-sha256.txt label**: lists
  `tools/mori-vote-bind.py@6ced9da9` though the binder bytes were pinned at
  `c419fe6d` (6ced9da9 touched only the driver tool). The sha is correct at
  both revs; the tag is cosmetic mislabeling.

## Verdict

Both claims satisfy every AXES.md admission rule: distinct owned axes with the
lowest-axis obligation met, causally separable (only `corpus/SOURCES.md`
shared, row-anchored), each falsifiable by one command, neither reachable by
a do-nothing (verified by execution at `5b295eee`, exit 1 both), and all
universals backed by enumerating checks. Both counters reproduce `met` at the
freeze tip. The findings below are counter-honesty and predicate-wording
defects — frozen, so routed to round 57, not re-proposed as fixes now.

## Findings

- **MED** — `count-c2.py:154-165`: `tool_absent`, `r55_artifacts_absent`,
  `contrast_absent` and `pins` map to no named field; `C2=unmet` can print
  all fields `ok`/`voted0`, and `contrast=voted0` can assert an unrun arm.
  `evidence/controls.txt` line 2 (plus `controls.py:92`'s 110-char
  truncation) shows exactly this unexplained-unmet shape.
- **MED** — `count-c1.py:162` vs its docstring (lines 18-19) and
  contract.md:30: "no health-verdict string" is a prefix scan
  (`split("# selftest",1)[0]`); the committed tool already carries
  `"healthy"`, `"unhealthy"`, `"failed lane"` at
  `tools/mori-driver-liveness.py:422` post-marker, and `HEALTH_WORDS`
  includes two strings ("is stuck", "wedged") the predicate never lists.
- **LOW** — `count-c1.py:40-44` vs docstring line 11: "every fixture
  subdirectory" is enforced as a frozen nine-name enumeration; extra
  fixtures are materialized but unchecked.
- **LOW** — `count-c2.py:96,90` / `count-c1.py:131`: "prints exactly the
  line" is substring containment, not a line match; padding stdout passes.
- **LOW** — `count-c2.py:119`: contrast arm accepts exit 0 or 1; a met-verdict
  `voted=0` line would pass.
- **LOW** — `tools/mori-vote-bind.py:89-95`: one binding channel per output;
  JSON parse success discards plain-text votes in the same output. "BOTH
  shapes" = alternatives, not channels.
- **LOW** — `tools/mori-vote-bind.py:201` / `count-c2.py:13`: `voters=16` is
  roster size, not votes cast (bound is `bound_voters=15`).
- **LOW** — `tools/mori-vote-bind.py:152-153`: ENTAIL votes extract but no
  ledger dispositions are ever read for them; `tally --verb ENTAIL` is a
  silent `rows=0` surface.
- **LOW** — `tools/mori-vote-bind.py:161,202,418`: `--min`/`min_votes` dead
  parameter; no quorum enforcement exists despite the plumbing.
- **LOW** — `count-c1.py:151,159-160` / `count-c2.py:122,130-131`: entry and
  registry-row checks are unanchored substrings ("S544"≈"S5440",
  "mined"≈"unmined", used-by not field-scoped).
- **LOW** — AXES.md:33 "lowest-scoring non-retired axis" lacks the "owned"
  qualifier the lane relies on; contract's "(coverage is the lowest owned
  axis)" is right under lane convention but attackable on the bare text.
- **LOW** — capability-acquisition C2 does not pin the SCORECARD
  capabilities-table row; the repertoire entry is unenforced L1 bookkeeping.
- **LOW** — `count-c1.py:146` unguarded `doc["log"]["malformed"]` KeyError
  path; `count-c1.py:171`/`count-c2.py:138` counter selftests assert only
  constants.
- **INFO** — `evidence/freeze-sha256.txt` tags the vote-bind pin
  `@6ced9da9`; the bytes were pinned at `c419fe6d`. Sha is correct at both.

Report: .ufo/waves/round-56/w1/Mo56RevClaims.md

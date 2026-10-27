# Mo56ExecCounters — round 56 w1 seat report

Seat: Mo56ExecCounters (leaf executor, no subagents).
Lane: mori-shokunin. Scratch: `/fast/scratch/hyaku/mori-r56/Mo56ExecCounters/`
(removed at the end of this seat; nothing outside it was written).

Scope executed: run the frozen C1/C2 counters at the freeze tip and at the
entering tip, run both counter selftests, prove the counters have no cwd
dependence, and falsify each counter arm by mutating its target in a scratch
fixture repo. The counters, predicates, controls and kill rules were treated
as frozen throughout — every weakness below is reported as a **named limit**,
with a routed item for round 57. No counter, predicate, control or receipt was
edited; no git/jj mutation was performed in the lane or the fleet root.

Frozen revisions used:
- freeze tip `8be2717b0809281d07dffe83dad424a4859e0747` (L1 MoriR56)
- entering tip `5b295eeebd87ebd610d8d39bfe2035742f740cfa`
- freeze commit `3f494b49cde612d929e82887a48e1660c022c359`
- data commits `c419fe6dc051a5828fabd5f472f851e76dd54e8d`, `6ced9da9b1f9c65065a8158735e0331938e8a599`

---

## 1. Assigned runs — every command, last line, exit code

All runs used `TMPDIR=/fast/scratch/hyaku/mori-r56/Mo56ExecCounters/tmp`.

### 1.1 Both counters at the freeze tip — expected both met, rc 0

```
cd /fast/scratch/hyaku/mori-r56/Mo56ExecCounters
export TMPDIR=/fast/scratch/hyaku/mori-r56/Mo56ExecCounters/tmp
TMPDIR=$TMPDIR python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/count-c1.py 8be2717b0809281d07dffe83dad424a4859e0747
TMPDIR=$TMPDIR python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/count-c2.py 8be2717b0809281d07dffe83dad424a4859e0747
```

```
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
rc=0
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
rc=0
```

Both match the contract's stated target output exactly.

### 1.2 Both counters at the entering tip — expected both unmet, failed=tool_absent, rc 1

```
TMPDIR=$TMPDIR python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/count-c1.py 5b295eeebd87ebd610d8d39bfe2035742f740cfa
TMPDIR=$TMPDIR python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/count-c2.py 5b295eeebd87ebd610d8d39bfe2035742f740cfa
```

```
C1=unmet selftest=bad fixtures=bad entry=bad row=bad norem=bad failed=tool_absent rev=5b295eeebd87ebd610d8d39bfe2035742f740cfa
rc=1
C2=unmet selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=5b295eeebd87ebd610d8d39bfe2035742f740cfa failed=tool_absent
rc=1
```

Both hit `failed=tool_absent` and rc 1, so the do-nothing control holds.
Note the **asymmetry between the two lines**: C1's tool-absent branch prints
every arm as `bad` (it has a dedicated branch, `count-c1.py:188`); C2's prints
every arm as `ok` and `contrast=voted0` although no arm ran at all. This is
finding **F3** below. The same line is committed verbatim in
`evidence/controls.txt` line 2.

### 1.3 Both counter selftests

```
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/count-c1.py --selftest
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/count-c2.py --selftest
```

```
C1_COUNTER_SELFTEST pass=1 fail=0
rc=0
C2_COUNTER_SELFTEST pass=1 fail=0
rc=0
```

Both match `evidence/selftest-c1-counter.txt` and `evidence/selftest-c2-counter.txt`.
Note what these selftests actually assert (see F-limit **F13**): the C1 one
only checks `len(EXPECT_FIX) == 9` and a string prefix; the C2 one only checks
`len(VOTERS) == 16` and a string prefix. They are tautologies over the
counter's own constants — they cannot detect a defect in the arms.

### 1.4 No cwd dependence — run from four different working directories

The instruction's "run with the env var MORI…" was replaced by the cwd test as
directed. No `MORI*` environment variable exists in this environment, and the
only environment variable either counter reads is `TMPDIR` (used solely as the
`tempfile.mkdtemp` parent). The counters therefore cannot be gated by an
environment knob.

```
cd /fast/scratch/hyaku/mori-r56/Mo56ExecCounters/cwdtest && python3 .../count-c1.py 8be2717b…   # cwd = <scratch>/cwdtest
cd /                                        && python3 .../count-c1.py 8be2717b…              # cwd = /
cd /tmp                                     && python3 .../count-c1.py 8be2717b…              # cwd = /tmp
cd <scratch>/fixture2.RFsMoV                && python3 .../count-c2.py 8be2717b…              # cwd = a git fixture repo
```

```
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b0809281d07dffe83dad424a4859e0747   rc=0
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b0809281d07dffe83dad424a4859e0747   rc=0
```

Every cwd produced byte-identical output and rc 0. **No cwd dependence
confirmed.** The counters locate the repo by absolute path
(`repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"`, overridable with
`--repo`) and locate the tool/fixtures by `git show`/`git ls-tree`, never by
relative path.

### 1.5 Determinism

Each counter was run 3× at the freeze tip; all six runs produced identical
output lines and rc 0. No flakiness in the measured path.

---

## 2. Falsification of the counter arms (mutation testing)

Method: one scratch fixture repo per experiment (`git init` inside
`/fast/scratch/hyaku/mori-r56/Mo56ExecCounters/`), `git -C "$D"
rev-parse --show-toplevel` asserted to equal the fixture dir before the first
commit, fixture-local identity only (`GIT_AUTHOR_NAME=fixture`,
`GIT_AUTHOR_EMAIL=fixture@localhost`, matching committer), never in the lane or
fleet root. The counters were run with `--repo "$D"` so they measured the
mutated commit.

Two fixture repos were used, both seeded from the freeze tip:
- **fixture 1** — `--depth=1` of the tip only. Sufficient for the C1 arms (no
  C1 arm needs history), but its C2 baseline reports `contrast=bad` because
  the round-55 entering-tip commit is absent from a shallow clone — an
  artifact of clone depth, not of the claim (see F-limit **F12**).
- **fixture 2** — the freeze tip **plus** the round-55 entering-tip commit
  `ca52426ea496bc6592e3e867cc9d28843e45f196`, so the C2 baseline is clean
  (`C2=met …`) and each C2 mutation fires exactly its own arm (§2.2).

An early C2 run against the shallow fixture 1 produced `failed=tally,contrast`
— the `contrast` component was the shallow artifact, not the mutation's
effect. The C2 table in §2.2 was therefore re-run in fixture 2, where the
baseline is clean and every mutation isolates its own arm. The C1 results in
§2.1 are unaffected by clone depth.

### 2.1 C1 arms — every arm is live and fails as designed

| # | Mutation at the measured rev | Counter output | rc | Arm fired |
|---|---|---|---|---|
| A | entry doc: `S544` → `S999` | `C1=unmet selftest=ok fixtures=ok entry=bad row=ok norem=ok … failed=entry` | 1 | entry ✓ |
| B | S544 registry row: `mined` → `pending` | `C1=unmet … row=bad … failed=row` | 1 | row ✓ |
| C | append a non-timestamp garbage line to `in-flight/watchdog.log` | `C1=unmet … fixtures=bad … failed=fixtures` | 1 | fixtures ✓ |
| D | delete the whole `variants` fixture dir | `C1=unmet selftest=bad fixtures=bad … failed=selftest,fixtures` | 1 | selftest + fixtures ✓ |
| E | health word planted **before** the `# selftest` marker | `C1=unmet … norem=bad … failed=pins,norem` | 1 | norem ✓ |
| F | health word planted **after** the marker | `C1=unmet … norem=ok … failed=pins` | 1 | norem ✗ (see F9) |
| G | fixture `watchdog.log` emptied | `C1=unmet selftest=bad fixtures=bad … failed=selftest,fixtures` | 1 | fixtures ✓ |
| H | fixture `watchdog.log` emptied **and** the `variants` case | traceback, stdout empty, rc 1 | 1 | **crash — see F1** |

All five C1 arms (selftest, fixtures, entry, row, norem) plus the `pins` arm
fire on a targeted mutation. The kill rules are not vacuous.

### 2.2 C2 arms — every arm is live and fails as designed

Run in a third fixture repo seeded with the freeze tip **plus** the round-55
entering-tip commit `ca52426e…`, so that the baseline is clean
(`C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok`,
rc 0) and each mutation fires exactly its own arm.

| # | Mutation at the measured rev | Counter output | rc | Arm fired |
|---|---|---|---|---|
| A | round-55 ledger: `holds` → `breaks` | `C2=unmet selftest=ok tally=bad control=ok contrast=voted0 entry=ok row=ok … failed=tally` | 1 | tally ✓ |
| B | junk one voter's output in `w1-results.json` | `C2=unmet … tally=bad … failed=tally` | 1 | tally ✓ |
| C | S545 registry row: `mined` → `pending` | `C2=unmet … row=bad … failed=row` | 1 | row ✓ |
| D | break the vote-binding entry (`S545` → `S999`) | `C2=unmet … entry=bad … failed=entry` | 1 | entry ✓ |
| E | tamper the vote-bind tool (one added line) | `C2=unmet selftest=bad … failed=pins` | 1 | pins ✓ |
| F | delete `.ufo/waves/round-55/count-c1.py` | `C2=unmet … contrast=voted0 … failed=contrast_absent` | 1 | **wrong label — see F2** |

Mutations A and B prove the C2 tally is genuinely derived from the committed
round-55 bytes, not from a cached or hardcoded value: corrupting either the
ledger or one voter's output flips the tally verdict while every other arm
stays `ok`.

### 2.3 The frozen controls module reproduces its committed receipt

```
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/controls/controls.py 5b295eeebd87ebd610d8d39bfe2035742f740cfa
```

```
do-nothing-c1                PASS C1=unmet selftest=bad fixtures=bad entry=bad row=bad norem=bad failed=tool_absent rev=5b295eeebd87ebd610d8d39b
do-nothing-c2                PASS C2=unmet selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=5b295eeebd87ebd610d8d39bfe2035742
mut:fence-toggle-dropped     KILLED arm=t_fenced_text_ignored
mut:substring-scalar-binding KILLED arm=t_json_prose_substring_rejected
mut:hash-length-opened       KILLED arm=t_hash_len_drift_rejected
mut:first-wins               KILLED arm=t_last_wins_text
mut:text-channel-closed      KILLED arm=t_plain_binds
mut:json-channel-closed      KILLED arm=t_json_array_binds
mut:roster-filter-dropped    KILLED arm=t_roster_and_name_filter
mut:entail-verb-dropped      KILLED arm=t_entailed_verb_parsed
rc=0
```

This reproduces `evidence/controls.txt` exactly (same verdicts, same arms,
same order, rc 0). All eight vote-binder mutants are killed.

Note the first two lines reproduce the F3 label defect verbatim — the
committed receipt already carries it.

### 2.4 Independent re-derivation of the receipts (not via the counters)

- The 9 frozen fixtures were run through the tool directly, without the
  counter. All 9 return `verdict=DRIVER_LIVENESS_OK` with malformed counts
  exactly matching the counter's `EXPECT_FIX` table: `hyaku-pairing 0`,
  `attempt-rollover 0`, `legacy-grammar 0`, `in-flight 0`, `malformed 5`,
  `fails-and-dead 0`, `state-shapes 0`, `two-lanes 0`, `variants 0`.
- The tool's own selftest was run standalone (outside the counter) and from a
  foreign cwd (`/`): `DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0`, rc 0
  both times. The tool has exactly 13 `@case` decorators.
- The tally was re-derived by calling the tool directly:
  `TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16
  bound_voters=15` — matches `evidence/tally-r55.txt`.
- The do-nothing control was re-derived by calling the tool directly on a
  junk-outputs results file: `TALLY rows=78 agree=0 double=0 single=0
  zero=78 dissent=0 voters=16 bound_voters=0` — matches the counter's
  `control` arm expectation (`zero=78`, `double=0`).
- The contrast was re-derived by running the frozen round-55 C1 counter at the
  freeze tip against the same committed artifacts:
  `C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78
  source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0
  holds=78 stale=0 voted=0 dissent=0 rev=8be2717b… failed=votes`, rc 1.
  `voted=0` confirmed.

### 2.5 Pins verified independently of the counters

| file | sha256 at the freeze tip | PIN constant | matches |
|---|---|---|---|
| `tools/mori-driver-liveness.py` | `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997` | `count-c1.py:46` | ✓ |
| `tools/mori-vote-bind.py` | `8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca` | `count-c2.py:46` | ✓ |

Both tool shas also match at the data commits their PIN comments name
(`mori-vote-bind.py` at `c419fe6d`; `mori-driver-liveness.py` at `6ced9da9`).
`mori-driver-liveness.py` differs at `c419fe6d` (`5befd490…`), which is exactly
what the `6ced9da9` correction commit ("driver probe docstring carries no
health-verdict words") fixed — the PIN is pinned at the corrected commit, so
the counter correctly rejects the pre-correction blob.

### 2.6 The at-freeze receipts remain valid at the freeze tip

`evidence/c1-at-freeze.txt` and `evidence/c2-at-freeze.txt` stamp
`rev=3f494b49cde612d929e82887a48e1660c022c359`, not the tip. That is by
design (the contract's routed defect 2: receipts stamp the revision they
measured), and it is **still valid**: every input those receipts measure is
byte-identical between `3f494b49` and `8be2717b` — the two tools, both
counters, the contract, both knowledge entries, `corpus/SOURCES.md`, and the
whole `fixtures/driver` tree (the `git ls-tree` diff of the fixture tree
between the two revisions is empty). The tip commit `8be2717b` touched only
`controls/controls.py`, the four receipt files and `freeze-sha256.txt`.
Re-running both counters at `3f494b49` reproduces the receipt lines exactly:
`C1=met …` rc 0 and `C2=met …` rc 0.

---

## 3. Falsification of the claims themselves

### 3.1 C1 — driver-liveness probe

The claim is that the probe reports per-lane log-shape facts only, over the
driver's launch/complete/dead/wrap/fail lines, with a 13-case selftest, 9
frozen fixtures, an S544-sourced entry and a mined registry row, and no
health-verdict string in the tool text.

- Probe behaviour, selftest count, fixture malformed counts, entry contents,
  S544 row contents (`own-work`, `mined`, `2026-10-27`, used-by naming
  `corpus/knowledge/driver-liveness-r56.md` and the tool) — all confirmed
  independently of the counter (§2.4, §2.5).
- The no-verdict property is **enforced by the tool's own selftest case**
  `t_no_health_verdict`, which asserts the emitted report blob contains none of
  `healthy` / `unhealthy` / `failed lane`. The probe's `verdict` field is
  `DRIVER_LIVENESS_OK` / `DRIVER_LIVENESS_UNAVAILABLE`, and the latter is
  documented as "missing/unreadable/empty log — unavailable is never zero".
  The output carries log-shape facts and no per-lane wellness claim.
- The counter's `norem` arm is a *second*, weaker guard on the tool's **text**,
  and its scope is bounded by a marker string (F9).
- **The C1 claim stands.** Nothing found falsifies it.

### 3.2 C2 — dual-shape vote binder

The claim is that the binder accepts both plain-text vote lines and
JSON-wrapped string-scalar votes, has a 16-case selftest, and re-binds the
round-55 RECHECK tally over committed bytes, while the frozen round-55 C1
counter still reads `voted=0` on those same bytes.

- 16-case selftest confirmed (`VOTE_BIND_SELFTEST pass=16 fail=0`, rc 0),
  matching `evidence/selftest-vote-bind.txt`.
- Dual-shape binding confirmed by direct inspection: `t_plain_binds` binds a
  plain-text line and `t_json_array_binds` / `t_json_nested_binds` bind
  JSON-wrapped string scalars; all eight binder mutants are killed by the
  controls module (§2.3).
- The tally over the committed bytes is reproduced exactly, and it is
  byte-derived (ledger corruption flips the verdict, §2.2 A).
- The contrast is confirmed: the frozen round-55 C1 counter reads `voted=0` on
  the same artifacts (§2.4). The binding shape really is the whole difference.
- **The C2 claim stands.** Two semantic weaknesses in *how the number is
  produced* are named below (F5, F6); neither falsifies the claim as the
  contract states it.

### 3.3 The stated contrast between the two counters

`evidence/c2-old-counter-voted0.txt` records the frozen round-55 C1 counter
reading `voted=0` at the entering tip; re-running it at the freeze tip gives
the same `voted=0` (rc 1, `failed=votes`). The contrast is real and
reproducible at both revisions.

---

## 4. Named limits (frozen artefacts — routed to round 57, not fixed here)

**F1 — MED — `count-c1.py` crashes instead of reporting when a fixture log is
empty or unreadable.** At `count-c1.py:147` the failure record is built with
`fx_bad.append("%s:%s/%s" % (name, doc.get("verdict"), doc["log"]["malformed"]))`.
When the probe reports `verdict=DRIVER_LIVENESS_UNAVAILABLE` its `log` object
has no `malformed` key (`{"path": …, "state": "empty"}`), so this raises
`KeyError: 'malformed'`. Reproduced by emptying a fixture log at the measured
rev: stdout is **0 bytes** (no `C1=` line at all), a Python traceback goes to
stderr, exit code is 1. A receipt consumer that parses stdout for the `C1=`
verdict line receives nothing; only a consumer that reads the exit code sees
the right answer (rc 1 coincides with "unmet"). The short-circuit on line 146
(`doc.get("verdict") != … or doc["log"]["malformed"] != want`) is safe, but
the message-construction expression on line 147 re-reads the missing key
unconditionally. Reproduced in both the shallow and the complete fixture repo:
stdout is 0 bytes, stderr ends with
`KeyError: 'malformed'`, rc 1. **Routed to r57:** guard the key access in the
failure message. Not a live defect at the freeze tip — all 9 frozen fixtures
are non-empty, so the crash is latent.

**F2 — MED — `count-c2.py` prints `contrast=voted0` when the contrast arm was
absent, not merely unsuccessful.** The label is computed at `count-c2.py:161`
as `"voted0" if "contrast" not in failed else "bad"`, but the absence case
appends the tag `contrast_absent` (`count-c2.py:113`), while only a genuine
mismatch appends `contrast` (`count-c2.py:120`). `"contrast" not in
["contrast_absent"]` is true, so the label renders `voted0`. Reproduced by
deleting `.ufo/waves/round-55/count-c1.py` at the measured rev: output
`C2=unmet selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok …
failed=contrast_absent`. The overall verdict (unmet) is right, but the line
asserts that the round-55 counter was run and read `voted=0` when it was
never executed. **Routed to r57:** test the tag set rather than substring
membership.

**F3 — MED — `count-c2.py`'s tool-absent path labels unrun arms as passing.**
Unlike C1, which has an explicit `failed == ["tool_absent"]` branch
(`count-c1.py:188`) printing every arm `bad`, C2 returns `["tool_absent"]`
from `evaluate()` (`count-c2.py:68-69`) and lets the generic printer run, so
every arm prints `ok` and `contrast=voted0` although *no arm executed* (the
tool did not exist at that revision, so the selftest, tally, control and
contrast arms were all skipped). Reproduced at the entering tip, and it is
committed verbatim as `evidence/controls.txt` line 2. This is the one place
where a reader of the committed control receipt could be misled into thinking
the arms ran at the entering tip. **Routed to r57:** give C2 the same
tool-absent branch C1 has.

**F4 — MED — C2's verdict is exposed to transient git failures.** The contrast
arm shells out to the round-55 counter, which does its own
`git rev-parse --verify` on the entering tip; `count-c2.py:119-120` treats any
exit code other than 0/1, or a missing `voted=0` in stdout, as a contrast
failure. During this session one invocation of the round-55 counter failed
with `C1_SETUP unresolvable revision …` (exit 2) for the *same* revision that
resolved successfully in 20/20 and 5/5 subsequent attempts (the lane repo was
being written concurrently by the L1 — `HEAD` moved to `acc62f54` during this
seat's run). One such transient during a C2 run flips C2 to `unmet` for a
reason unrelated to the claim. **Routed to r57:** retry the contrast arm once
on a setup-class failure, or classify exit-2 as "inconclusive" rather than
"contrast bad".

**F5 — MED — the tally's `agree` counts single-vote rows, and the advertised
minimum-votes knob is inert.** In `tools/mori-vote-bind.py:186-189` a row with
exactly one vote is counted in `single` **and** in `agree` when that one vote
matches the ledger. `min_votes` is accepted by the CLI (`--min`, default 2),
stored in the returned dict as `"min"` (line 202) and **never used** in the
row classification (lines 183-193). Verified: `--min 1`, `--min 2`, `--min 3`,
`--min 99` and the default all produce byte-identical tallies. The tool's own
selftest locks the permissive behaviour in (the case `t_tally_mini` at line 330 passes
`min_votes=2` yet expects `agree == 3`, including the two single-vote rows).
Consequence: the frozen expectation `agree=78` is 68 double-vote rows **plus
10 rows resting on a single voter's word**; if the minimum were honoured at
its advertised value of 2 the count would be 68. The contract's frozen
expectation depends on the permissive semantics, so correcting this is a
data (tool) change with a re-pin consequence — **routed to r57 with the
re-pin cost stated explicitly**, not applied here.

**F6 — MED — one of the sixteen round-55 RECHECK voters binds nothing, and the
frozen C2 expectation is coupled to that seat's output.** The frozen tally
reports `voters=16 bound_voters=15`. The unbound voter is `Mo55Rc14`: its
committed output in `.ufo/waves/round-55/w1-results.json` is 1055 bytes of
prose with no vote surface at all (no verb-hash-word line, and no JSON vote
block) — it ends mid-analysis on "Yet ledger disposition holds as pointer".
Extracting votes from it yields the empty set. Independently confirmed by
tallying each voter alone: `Mo55Rc13` alone gives `agree=10 single=10
zero=68`, `Mo55Rc14` alone gives `agree=0 zero=78` (bound_voters=0), and
`Mo55Rc15` alone gives `agree=8 single=8`. So the ten `single=10` rows are
exactly `Mo55Rc13`'s ten hashes, whose second voter never bound. Simulating a
repair (give `Mo55Rc14` the same ten hashes as `Mo55Rc13`) changes the tally
to `double=78 single=0 bound_voters=16`, which no longer matches the frozen
`EXPECT_TALLY` string. The counter is therefore coupled to a defect in a
round-55 seat output: the same ledger with one repaired voter would make C2
report `tally=bad` even though the binder got *better*. This is a genuine
routing observation for the L1 (the binder is honest — it reports
`bound_voters=15` rather than hiding the shortfall — but the frozen expected
string embeds the shortfall). **Routed to r57** with the re-pin consequence
stated; the round-55 artifacts are committed history and are not editable by
this seat.

**F7 — MED — `evidence/freeze-sha256.txt` misattributes the provenance of four
of its six sha256 lines.** The receipt carries the header
`# data commit 6ced9da9b1f9c65065a8158735e0331938e8a599` and then lists
`contract.md`, `count-c1.py`, `count-c2.py` and `controls/controls.py` under
it. **None of those four paths exists at `6ced9da9`** (`git cat-file -e
6ced9da9:<path>` fails for all four; the commit predates them). The listed
shas are correct values, but they come from later revisions:
`contract.md` `088761f3…`, `count-c1.py` `c4e58eed…` and `count-c2.py`
`4b350c77…` are the values at the freeze commit `3f494b49`, while
`controls/controls.py` `5bf65ac0…` is the value at the freeze tip `8be2717b`
(at `3f494b49` it is `08620c17…`). The two `tools/…@6ced9da9` lines are
correct. The receipt's hash values are all right; only the attribution is
wrong. **Routed to the L1:** this is an evidence-copy correction (the contract
explicitly allows the L1 to correct data), with a re-pin consequence for
`freeze-sha256.txt`.

**F8 — LOW — the C1 fixture arm asserts only `verdict` and the malformed
count, so a fixture whose lane content changes while its malformed count
holds still passes.** Mutating `pgid=620717` → `pgid=999999` in the
`in-flight` fixture yields `C1=met selftest=ok fixtures=ok …`, rc 0 — the
counter's `fixtures` arm (`count-c1.py:146`) checks `verdict` and
`log.malformed` only, and the tool's `t_in_flight` case checks the launch
*count*, not the pgid. Appending a timestamp-first line that the grammar
classifies as `other_line` also passes (`other_lines` becomes 1 and is never
asserted). The fixture bytes themselves are fixed by the measured revision, so
this is a narrowness in what is *asserted*, not a pinning hole. **Routed to
r57.**

**F9 — LOW — the `norem` arm scans only the tool text before the first
`# selftest` marker.** `count-c1.py:162` takes
`tool_src.split("# selftest", 1)[0].lower()` and searches that prefix for the
health words. In the frozen tool all runtime code precedes the marker (the
marker is at line 248; `parse_log`, `state_shapes` and `run` are at lines 77,
179 and 201), so the coverage is complete today. But the arm's boundary is a
literal comment inside the file being judged: a health-verdict string added to
runtime code placed after that marker would escape the arm. Proven both ways
— planted before the marker → `norem=bad`; planted after → `norem=ok`
(only `pins` fired). **Routed to r57.**

**F10 — LOW — both counters leak their temporary directories.** Each run
creates `mori-r56-c1-*` / `mori-r56-c2-*` under `TMPDIR` via
`tempfile.mkdtemp` and never removes it (`count-c1.py:124`,
`count-c2.py:77`). Measured: three runs left three directories; the
accumulation during this seat reached 32 directories / 5.0 MB in the seat's
`TMPDIR`. This seat's scratch was removed at the end of the run, but a
long-lived `TMPDIR` on the host will grow without bound under repeated counter
invocations. **Routed to r57.**

**F11 — LOW — the committed control receipt truncates the revision field.**
`controls.py` truncates each do-nothing verdict to 110 characters
(`verdict[:110]`), so `evidence/controls.txt` lines 1-2 carry a 24-character
and a 33-character fragment of the 40-character revision rather than a
resolvable hash. The line is still identifiable (the fragments differ per
line), but the receipt cannot be re-verified from itself. **Routed to r57.**

**F12 — LOW — C2's contrast arm requires the measured repository to contain
the round-55 entering-tip commit.** The round-55 counter resolves its `ENTER`
constant `ca52426ea496bc6592e3e867cc9d28843e45f196`; in a shallow clone that
object is absent, the counter exits 2 with `C1_SETUP entering tip … unreadable`
on stderr, and C2 then reports `contrast=bad` — an artifact of the clone
depth, not of the claim. This affected only my first scratch fixture repo; the
lane repository is complete and C2 measures `met` there. Mitigation for any
future seat reproducing C2 in a fixture: fetch that commit explicitly
(`git fetch --depth=1 origin ca52426e…`), which is what fixture 2 does, and
the C2 baseline is then clean (`C2=met …`, rc 0). Noted so a future seat does
not misread a shallow-clone artifact as a defect in the claim.
**Routed to r57** as a reproduction note.

**F13 — LOW — both counter selftests are tautologies.** `count-c1.py:171`
asserts `len(EXPECT_FIX) == 9 and EXPECT_SELFTEST.startswith(…)`;
`count-c2.py:138` asserts `len(VOTERS) == 16 and EXPECT_TALLY.startswith(…)`.
Neither exercises the arms they sit beside, so a defect in the C1/C2 evaluation
logic would still yield `C1_COUNTER_SELFTEST pass=1 fail=0`. The receipts
`evidence/selftest-c1-counter.txt` and `evidence/selftest-c2-counter.txt`
inherit that weakness. **Routed to r57.**

---

## 5. Route summary for the L1

Round-57 routed items, in descending significance, all against frozen
artefacts (no change proposed to any counter, predicate, control or receipt by
this seat):

1. **F2** — C2 must not print `contrast=voted0` for an absent contrast arm
   (tag-set test instead of substring membership).
2. **F3** — C2 needs C1's explicit tool-absent branch so unrun arms are not
   labelled `ok`; the committed `evidence/controls.txt` line 2 already carries
   the misleading labels.
3. **F1** — C1 must not crash on an empty/unreadable fixture log; emit a
   `C1=unmet … failed=fixtures` line instead of a traceback.
4. **F4** — C2's contrast arm should distinguish a setup-class failure from a
   genuine contrast mismatch (and ideally retry once).
5. **F5** — the vote binder's `min_votes`/`--min` is inert and `agree`
   includes single-vote rows; correcting the semantics changes the frozen
   `agree=78` expectation. Tool-data change with a re-pin consequence.
6. **F6** — the frozen C2 expectation is coupled to `Mo55Rc14`'s prose-only
   round-55 output; a repair there changes the tally to
   `double=78 single=0 bound_voters=16` and would break `EXPECT_TALLY`.
7. **F7** — `evidence/freeze-sha256.txt` attributes four sha256 lines to a
   commit at which none of the four paths exists.
8. **F8**, **F9**, **F10**, **F11**, **F12**, **F13** — counter narrowness and
   hygiene items as described above.

### Claim verdicts from this seat

- **C1: the claim is not falsified.** Counter output, tool selftest, fixture
  malformed counts, entry and registry row, tool pins and the no-verdict
  property were all re-derived independently of the counter and agree. The
  counter's five arms plus the `pins` arm are live under targeted mutation.
- **C2: the claim is not falsified.** The 16-case selftest, the dual-shape
  binding, the byte-derived tally, the junk control and the `voted=0` contrast
  were all re-derived independently and agree. The counter's arms are live
  under targeted mutation. F5 and F6 qualify what the headline number means;
  neither contradicts the contract's stated target.
- **Both do-nothing controls hold** (`failed=tool_absent`, rc 1) and the
  frozen controls module reproduces its committed receipt with rc 0 and eight
  killed mutants.
- **No cwd dependence** in either counter (four working directories, identical
  output), and no environment variable other than `TMPDIR` influences either
  counter.

---

## Findings

| # | Severity | Finding | File / line |
|---|---|---|---|
| F1 | MED | C1 counter raises an unhandled `KeyError` when a fixture log is empty/unreadable: stdout is empty (no `C1=` line), traceback on stderr, rc 1. A receipt consumer parsing stdout for the verdict gets nothing. | `mori-shokunin/.ufo/waves/round-56/count-c1.py:147` (guard on `doc["log"]["malformed"]`) |
| F2 | MED | C2 labels an *absent* contrast arm as `contrast=voted0`: the printer tests `"contrast" not in failed` while the absence tag is `contrast_absent`. Reproduced by deleting the round-55 counter at the measured rev. | `mori-shokunin/.ufo/waves/round-56/count-c2.py:161`, tag at `:113` vs `:120` |
| F3 | MED | C2's tool-absent path prints every arm `ok` and `contrast=voted0` although no arm ran; C1 has the equivalent branch and prints all `bad`. The misleading labels are committed in the control receipt. | `mori-shokunin/.ufo/waves/round-56/count-c2.py:68-69` and `:156-163`; receipt `mori-shokunin/.ufo/waves/round-56/evidence/controls.txt:2` |
| F4 | MED | A transient `git rev-parse` failure inside the round-55 counter (observed once, exit 2, `C1_SETUP unresolvable revision`) makes C2 report `contrast=bad` and C2 `unmet`, for a reason unrelated to the claim. | `mori-shokunin/.ufo/waves/round-56/count-c2.py:118-120` |
| F5 | MED | The vote binder's `min_votes`/`--min` is accepted and echoed but never used in row classification, and `agree` counts single-vote rows; the frozen `agree=78` is 68 double-vote rows plus 10 single-vote rows. `--min 1/2/3/99` all give identical output. | `mori-shokunin/tools/mori-vote-bind.py:161,186-193,202,418,438` |
| F6 | MED | One of the sixteen round-55 RECHECK voters (`Mo55Rc14`) binds nothing — its committed output is 1055 bytes of prose with no vote surface — so `bound_voters=15`; the ten `single=10` rows are exactly `Mo55Rc13`'s hashes. Repairing that voter changes the tally to `double=78 single=0 bound_voters=16` and would break the frozen `EXPECT_TALLY`. | `mori-shokunin/.ufo/waves/round-56/count-c2.py:44-45` (`EXPECT_TALLY`), asserted at `:96`; `mori-shokunin/.ufo/waves/round-55/w1-results.json` (entry `Mo55Rc14`) |
| F7 | MED | `freeze-sha256.txt` attributes `contract.md`, `count-c1.py`, `count-c2.py` and `controls/controls.py` to data commit `6ced9da9`, where none of the four paths exists; the shas are the values at `3f494b49` (three of them) and `8be2717b` (controls.py). | `mori-shokunin/.ufo/waves/round-56/evidence/freeze-sha256.txt:1-6` |
| F8 | LOW | The C1 fixture arm asserts only `verdict` and `log.malformed`; changing a fixture's lane content while holding the malformed count (e.g. `pgid`) still yields `C1=met`. | `mori-shokunin/.ufo/waves/round-56/count-c1.py:146` |
| F9 | LOW | The `norem` arm scans only the tool text before the first `# selftest` marker; all runtime code precedes it today, but runtime code placed after the marker escapes the arm. Verified both directions. | `mori-shokunin/.ufo/waves/round-56/count-c1.py:162` |
| F10 | LOW | Both counters create a `mkdtemp` directory per run under `TMPDIR` and never remove it; 32 directories / 5.0 MB accumulated during this seat. | `mori-shokunin/.ufo/waves/round-56/count-c1.py:124`; `…/count-c2.py:77` |
| F11 | LOW | The committed control receipt truncates each do-nothing verdict to 110 chars, leaving 24- and 33-character fragments of the revision hash instead of a resolvable 40-character hash. | `mori-shokunin/.ufo/waves/round-56/controls/controls.py:92`; receipt `…/evidence/controls.txt:1-2` |
| F12 | LOW | C2's contrast arm needs the round-55 entering-tip commit present in the measured repo; in a shallow clone the round-55 counter exits 2 and C2 reports `contrast=bad` spuriously. Reproduction note only. | `mori-shokunin/.ufo/waves/round-56/count-c2.py:111-120`; `mori-shokunin/.ufo/waves/round-55/count-c1.py:49` (`ENTER`) |
| F13 | LOW | Both counter `--selftest` modes are tautologies over the counters' own constants and cannot detect a defect in the arms they accompany. | `mori-shokunin/.ufo/waves/round-56/count-c1.py:171`; `…/count-c2.py:138` |

No HIGH-severity finding: the two frozen claims were reproduced exactly and
neither was falsified by any mutation, and every kill rule tested fired as
intended.

# Mo56ExecBinderControls — round 56 wave w1 (scoped findings)

Seat: Mo56ExecBinderControls (executor, controls verification + mutant replay).
Lane: mori-shokunin. Freeze tip under test: `8be2717b0809281d07dffe83dad424a4859e0747`.
Entering tip (do-nothing): `5b295eeebd87ebd610d8d39bfe2035742f740cfa`.
Scratch (all work): `/fast/scratch/hyaku/mori-r56/Mo56ExecBinderControls/` (removed at exit).
Host reads only; no lane/fleet mutation, no jj/git write in the lane repo.

## 1. Verdict on the assigned checks

| Assigned check | Result |
|---|---|
| `controls.py 5b295eee… --repo …` runs, rc 0 | PASS, rc 0 |
| do-nothing-c1 PASS | PASS (`C1=unmet … failed=tool_absent`) |
| do-nothing-c2 PASS | PASS (`C2=unmet … failed=tool_absent`) |
| all 8 mutants KILLED | PASS (8/8 KILLED, 0 SURVIVOR, 0 ERROR, 0 SETUP) |
| output equals `evidence/controls.txt` | PASS — byte-identical (`diff` clean) |
| manual replay: substring-scalar-binding | KILLED, named arm present in failing list (see §3, with a MED caveat) |
| manual replay: roster-filter-dropped | KILLED by exactly the named arm (`pass=15 fail=1`) |

Both frozen claims reproduce independently at the freeze tip (not only from the
committed receipts):

```
$ python3 .ufo/waves/round-56/count-c1.py 8be2717b… --repo <lane>
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b…   rc 0
$ python3 .ufo/waves/round-56/count-c2.py 8be2717b… --repo <lane>
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b…   rc 0
```

Independently reproduced tally over committed bytes (tool materialized from the
freeze tip, round-55 ledger + `w1-results.json` from the same rev):

```
TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15
```
matches `evidence/tally-r55.txt` exactly.

## 2. Control run (verbatim)

Command (scratch `TMPDIR` set, nothing written into the lane repo):

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/controls/controls.py \
      5b295eeebd87ebd610d8d39bfe2035742f740cfa --repo /home/vgpnk/Projects/shokunin/mori-shokunin
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
RC=0
```

`diff` of this stdout against `.ufo/waves/round-56/evidence/controls.txt` is empty
(the receipt is 788 bytes, 10 lines; stderr was 0 bytes). The frozen pin sheet
`evidence/freeze-sha256.txt` matches the working tree for contract.md,
count-c1.py, count-c2.py, controls/controls.py and both tool files; the two
source copies under `corpus/evidence/sources-r56/` match their pinned sha256 as
bytes on disk. `controls.py` bytes are identical at the freeze commit
`3f494b49` and at the freeze tip `8be2717b` (5bf65ac0…), so the receipt is
reproducible from the frozen control file.

## 3. Manual replay of the two named mutants

Both substitutions were re-applied by hand (independent of `controls.py`) to a
scratch copy of `tools/mori-vote-bind.py` taken from the freeze tip
(sha256 `8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca`),
then `--selftest` was executed.

### 3a. substring-scalar-binding

Substitution (verbatim from `controls/controls.py` MUTANTS):

```
old: 'm = VOTE_RE.match(s.strip())'
new: 'm = re.search(r"(RECHECK|ENTAIL)\\s+([0-9a-f]{12})\\s+([A-Za-z][A-Za-z0-9_-]*)", s)'
occurrences of old in pristine tool: 1   (substitution applied: True)
```

Failing arm line (paste of the mutant's own output):

```
VOTE_BIND_SELFTEST pass=8 fail=8 failed=t_json_array_binds:EXC:no such group,t_json_array_binds,t_json_nested_binds:EXC:no such group,t_json_nested_binds,t_json_string_doc_binds:EXC:no such group,t_json_string_doc_binds,t_fenced_scalar_ignored:EXC:no such group,t_fenced_scalar_ignored,t_json_prose_substring_rejected:EXC:no such group,t_json_prose_substring_rejected,t_last_wins_json:EXC:no such group,t_last_wins_json,t_entailed_verb_parsed:EXC:no such group,t_entailed_verb_parsed,t_tally_mini:EXC:no such group,t_tally_mini
```

rc = 1, so the mutant is KILLED and the named arm `t_json_prose_substring_rejected`
**is** in the failing list — the receipt line is truthful as printed. But the
kill is not attributable to substring binding: the substituted regex has three
capture groups while the tool reads `m.group(4)` (`tools/mori-vote-bind.py:93`),
so every JSON arm raises `IndexError: no such group` (8 of 16 arms fail, all by
exception). A faithful four-group variant of the same idea
(`re.search(r"(RECHECK|ENTAIL)\s+([0-9a-f]{12})\s+([A-Za-z][A-Za-z0-9_-]*)(?:\s(.*))?", s)`,
which still binds a vote inside JSON prose) fails exactly
`failed=t_fenced_scalar_ignored,t_json_prose_substring_rejected` with 0
exceptions — i.e. the named arm does have the intended discriminating power,
but the frozen mutant never exercises it. The control's *verdict* (KILLED) is
correct; its *attribution* is over-broad and for the wrong reason. The control
file is frozen — reported as a named limit and routed to round 57, not proposed
as a fix here.

### 3b. roster-filter-dropped

```
old: "roster = voters if voters is not None else sorted(outputs)"
new: "roster = sorted(outputs)"
occurrences of old in pristine tool: 1   (substitution applied: True)
```

Failing arm line (paste of the mutant's own output):

```
VOTE_BIND_SELFTEST pass=15 fail=1 failed=t_roster_and_name_filter
```

rc = 1, KILLED, and the failure is **only** the named arm — a clean, specific
kill. No other arm moves.

## 4. Independent arm-by-arm non-vacuity audit of both frozen counters

The frozen control set contains mutants for the C2 tool only; C1 has none, and
the C2 counter's own kill arms (tally / control / contrast / entry / row /
selftest / pins) are not exercised by the 8 mutants either. To test whether the
frozen kill rules are real or vacuous, I built scratch worktrees of a
`--shared` clone, applied one targeted mutation per arm, and ran the **frozen
counter bytes** (with `PIN` disabled in the scratch copy only, so the pin arm
cannot mask the arm under test).

```
C1 baseline-freeze rc=0 :: C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok
C1 norem-health-word          rc=1 KILLED-BY-ARM   failed=norem
C1 selftest-line-changed      rc=1 KILLED-BY-ARM   failed=selftest
C1 fixture-malformed-changed  rc=1 KILLED-BY-ARM   failed=selftest,fixtures
C1 entry-removed              rc=1 KILLED-BY-ARM   failed=entry
C1 row-removed                rc=1 KILLED-BY-ARM   failed=row
C2 baseline-freeze rc=0 :: C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok
C2 selftest-line-changed      rc=1 KILLED-BY-ARM   failed=selftest
C2 tally-agree-fabricated     rc=1 KILLED-BY-ARM   failed=selftest,tally,control
C2 control-junk-binds         rc=1 KILLED-BY-ARM   failed=selftest,tally,control
C2 contrast-voted-changed     rc=1 KILLED-BY-ARM   failed=contrast
C2 entry-removed              rc=1 KILLED-BY-ARM   failed=entry,contrast
C2 row-removed                rc=1 KILLED-BY-ARM   failed=row,contrast
SUMMARY: 10 arms, 0 not killed by their own arm
```

The `contrast` arm was isolated separately: mutating the frozen round-55 counter
so it prints `voted=9` instead of `voted=0` makes the C2 counter report
`contrast=bad` (rc 1) — the arm is live, not vacuous.

Pins arms (frozen counter with its real PIN, tool bytes perturbed by one
comment line):

```
C1 pins-mutated rc=1 :: C1=unmet … failed=pins
C2 pins-mutated rc=1 :: C2=unmet … failed=pins
```

## 5. Falsification probes of the two claims (beyond the assigned scope)

These are the attack probes; each is a bounded, reproducible command.

* **Vote-line loss in the dual-shape binder (MED).** The JSON channel applies
  the whole-string anchored `VOTE_RE` to each JSON string scalar
  (`tools/mori-vote-bind.py:91`). A scalar holding two vote lines binds only
  the first and swallows the second into `rest`; a scalar holding three binds
  **zero**. The plain-text channel (per-line) binds all of them.

  ```
  json string with 1 vote line(s): bound=1 [('aaaaaaaaaaaa', 'holds', '')]
  json string with 2 vote line(s): bound=1 [('aaaaaaaaaaaa', 'holds', 'RECHECK bbbbbbbbbbbb holds')]
  json string with 3 vote line(s): bound=0 []
  ```

  A scan of all 64 committed round-55 seat outputs found **0** JSON string
  scalars containing more than one vote line, so the frozen
  `TALLY rows=78 agree=78 … bound_voters=15` is unaffected and the C2 claim
  stands over the committed bytes. The gap is in the *shape* the contract
  names ("JSON-wrapped string-scalar votes"): a future seat that packs several
  vote lines into one string value is silently under-counted (3+ lines = zero
  votes, no signal). Routed to round 57.

* **Why the round-55 contrast is real, not an artifact (supports C2).** The
  frozen round-55 counter reads votes from the voter's report file and then
  requires the *results.json output* to contain that same line as a bare
  line (`.ufo/waves/round-55/count-c1.py:301`). In the committed bytes the
  vote lines sit inside a JSON array, so the stripped line is
  `"RECHECK a6e5226259c9 holds",` — quoted and comma-terminated — and never
  equals the bare form, so the round-55 arm binds 0 votes while the new
  binder's JSON walk binds 10. The claimed "the binding shape is the whole
  difference" is literally true. (`Mo55Rc14` has no report file at the freeze
  tip and no vote surface in its output, so `bound_voters=15` is also honest.)

* **C1 fixture arm is table-driven and shallow (LOW).** `EXPECT_FIX`
  (`.ufo/waves/round-56/count-c1.py:37`) hard-codes 9 fixture names; the counter
  never enumerates the fixture tree. Adding a 10th fixture directory with a
  deliberately malformed log leaves the counter at `C1=met … fixtures=ok`. A
  *lane-level* edit that keeps the malformed count at 0 is caught only by the
  separate selftest arm (`failed=selftest`, `fixtures=ok`), i.e. the fixture
  arm itself verifies only `verdict` + `malformed` count, not the per-lane
  log-shape facts the claim is about.

* **C1 `norem` arm has a blind half (MED).** The check scans only the tool text
  *before* the first `# selftest` marker
  (`.ufo/waves/round-56/count-c1.py:162`). The marker sits at line 248 of 479,
  so `main()` and everything after it is unscanned: a health-verdict string
  added to production code after line 248 does not trip `norem` (verified with
  PIN disabled: `C1=met … norem=ok`), while the same string placed before the
  marker trips it (`failed=norem`). The split is load-bearing for the tool
  itself: the tool's own selftest arm mentions the forbidden words at line 422,
  which is after the marker. The contract's predicate ("the tool text at R
  contains no health-verdict string (healthy, unhealthy, failed lane)") is
  therefore only enforced on a prefix of the file.

* **Survivor not caught by selftest or counter (LOW).** A case-insensitive
  vote-hash regex (`[0-9a-f]{12}` → `[0-9a-fA-F]{12}`) survives the 16-arm
  selftest (rc 0) and leaves the frozen tally unchanged
  (`rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound=15`,
  identical before and after), because no committed output uses uppercase hex.
  Under `controls.py`'s own definition ("a mutant its own selftest cannot catch
  is a C2 kill-rule finding") this is a survivor. It has nil effect on the
  frozen numbers today; it is a coverage hole, not a falsification.
  Two further probes of mine turned out to be *equivalent* mutants, not
  survivors, and are recorded here so the L1 does not chase them: dropping the
  `^` from `VOTE_RE` (the regex is always used with `.match()`, which anchors
  anyway), and reordering the roster ternary in `tally()`.

* **Inert threshold parameter (LOW).** `tally(..., min_votes=2)` stores
  `min_votes` but never uses it; the row classification is hard-wired to
  "one voter = single, two or more = double"
  (`tools/mori-vote-bind.py:160-190`). The CLI exposes `--min` and the
  counter invokes the tally without it. `--min 1/2/3/5` all print the
  identical tally line. A `--min 3` caller would get `double` rows that rest
  on only two voters.

* **Contrast arm does not check *why* the round-55 counter says `voted=0`
  (LOW).** The C2 contrast arm requires the substring `voted=0` in the
  round-55 counter's stdout and accepts rc 0 or 1
  (`.ufo/waves/round-56/count-c2.py:110-120`). The frozen round-55 counter is
  itself `C1=unmet … failed=votes`, i.e. it fails; the contrast arm passes on
  any failure mode that happens to print `voted=0`. The arm is live (mutating
  it to `voted=9` trips it), but it does not distinguish "the old shape cannot
  see the votes" from "the old counter failed for an unrelated reason".

* **Control module is not pinned to the freeze revision (MED).**
  `controls/controls.py:81` and `:94` read the counters and the tool from
  `git show HEAD:…`, not from the freeze rev. Today this is harmless — the
  counter and tool bytes are identical at `8be2717b` and at HEAD — but the
  receipt is not anchored to the frozen revision, so a later commit that
  touches the tool or the counters silently re-baselines the control. Proof
  that the anchor matters: the pre-correction control file at the freeze commit
  `3f494b49` (08620c17…) fails on its own mutant table:

  ```
  mut:fence-toggle-dropped     ERROR substitution did not apply
  RC=1
  ```

  (the `r"…\n…"` raw-string pattern could never match the real source text);
  `8be2717b` corrected exactly that pattern, which is why the current receipt
  is clean.

* **Live driver-liveness receipt reproduces structurally (supports C1).** The
  frozen tool run against the fleet root's real `.ufo/watchdog.log` gives the
  same schema, notes, verdict (`DRIVER_LIVENESS_OK`), state-dir shapes and
  per-lane counters as `evidence/driver-liveness-live.txt`; the only
  differences are age/counter drifts caused by the live log having grown since
  the receipt was taken (`log.lines` 1732 vs 1728, and three lanes with one
  more launch/complete). Verdict and schema identical.

* **C1 fixture set matches the contract.** All 9 fixture directories exist at
  the freeze tip with a `watchdog.log`; the expected malformed counts
  (hyaku-pairing 0, attempt-rollover 0, legacy-grammar 0, in-flight 0,
  malformed 5, fails-and-dead 0, state-shapes 0, two-lanes 0, variants 0) are
  reproduced by the tool, and the tool's own 13-case selftest reports
  `DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0` when the fixtures are
  materialized in the layout the counter uses (`cwd/tool/tools/` + `cwd/tool/.ufo/…`).
  The `state-shapes` fixture's `kake.round` symlink is restored as a symlink
  by the counter's materializer and counted as a symlink, never followed.

* **C1 health-word list is a superset of the contract's (LOW).**
  `HEALTH_WORDS` (`count-c1.py:45`) adds "is stuck" and "wedged" to the
  contract's three words — stricter than the frozen predicate, not weaker.

## 6. Scope and honesty notes

* Nothing in the lane repo, the fleet repo, the jj state, or the git index was
  mutated. `git status --porcelain` in the lane shows only the pre-existing
  `LOG.md`, `SCORECARD.md`, `SHONEN.md` modifications and the untracked
  round-56 wave files that were already there before this seat started; the
  scratch clone lives entirely under `/fast/scratch/hyaku/mori-r56/`.
* Every commit made during this seat's work was made inside a scratch
  worktree of a `--shared` clone (`git -C clone worktree add`), with an explicit
  `-c user.name=Mo56Fixture -c user.email=mo56@example.invalid` identity; the
  clone is not the lane repo and shares objects read-only.
* No tool was installed or upgraded by this seat (no pacman, no network fetch);
  the operator's tooling directive therefore produced no install record.
* The `.ufo/watchdog.log` under `/home/vgpnk/Projects/shokunin/` was read
  read-only for the live reproduction; no fleet log, state dir, or process was
  written, killed, or steered.
* `disk-guard.sh status` was checked before the runs: `/fast/scratch/hyaku`
  28% used, 585.0G free — no ENOSPC condition.
* Two claims I could not check from this seat: (a) whether the round-55 vote
  arm's `failed=votes` cause is *only* the JSON-array shape — I confirmed the
  committed outputs put vote lines inside JSON arrays and that no bare line
  exists, but I did not re-run the round-55 counter under every conceivable
  output shape; (b) whether any *other* seat's committed round-55 output would
  bind differently under a non-frozen binder — out of scope for this seat.

## Findings

| # | Severity | Finding | File / line |
|---|---|---|---|
| 1 | MED | The `substring-scalar-binding` mutant is killed by an `IndexError: no such group` in all 8 JSON arms (its regex has 3 groups, the tool reads `group(4)`), not by substring binding; the named arm `t_json_prose_substring_rejected` fails only as collateral of the crash. A faithful 4-group variant of the same mutation does fail that arm alone-ish (plus `t_fenced_scalar_ignored`), so the arm has the power but the frozen mutant never exercises it. Verdict KILLED is correct; attribution is over-broad. Named limit → round 57 (control file frozen). | `.ufo/waves/round-56/controls/controls.py:29-31`; `tools/mori-vote-bind.py:91-94` |
| 2 | MED | The control module reads the counters and the tool from `git show HEAD:…`, not from the freeze revision, so the control receipt is not anchored to the frozen tip and silently re-baselines if HEAD's bytes change. Demonstrated by the pre-correction control file at `3f494b49`, which fails with `ERROR substitution did not apply` (rc 1). | `.ufo/waves/round-56/controls/controls.py:81,94` |
| 3 | MED | The C2 JSON channel binds only the first vote line inside a multi-line JSON string scalar (3+ lines → zero votes, silently). Committed round-55 bytes contain no such scalar (0 found), so the frozen tally is unaffected; the shape the contract names is under-covered. | `tools/mori-vote-bind.py:88-95` |
| 4 | MED | The C1 `norem` arm scans only the tool text before the first `# selftest` marker (line 248 of 479); `main()` and everything after is unscanned, so a health-verdict string in production code after the marker does not trip it (verified). The contract's predicate reads as whole-file. | `.ufo/waves/round-56/count-c1.py:162-164`; `tools/mori-driver-liveness.py:248,451` |
| 5 | MED | C1 has no mutation arms at all in the frozen control set; the six C1 kill rules (pins/selftest/fixtures/entry/row/norem) and the seven C2 kill rules are unexercised by the frozen mutants. My scratch harness shows all of them are non-vacuous (10/10 arms killed by their own arm, pins and contrast isolated) — but that evidence is mine, not the frozen receipt's. | `.ufo/waves/round-56/controls/controls.py:22-45` |
| 6 | LOW | The C1 fixture arm is table-driven (9 hard-coded names) and shallow (verdict + malformed count only). A 10th fixture directory is never inspected (`C1=met … fixtures=ok`); a lane-only fixture edit with malformed count unchanged is caught only by the separate selftest arm. | `.ufo/waves/round-56/count-c1.py:37-40,134-150` |
| 7 | LOW | The C2 contrast arm requires the substring `voted=0` and accepts rc 0/1 from the round-55 counter; it does not check *why* that counter failed, so any unrelated failure mode printing `voted=0` would satisfy it. The arm is live (mutating to `voted=9` trips it). | `.ufo/waves/round-56/count-c2.py:110-120` |
| 8 | LOW | `min_votes` / `--min` is inert: `tally()` stores it but classifies rows as single/double by a hard-wired count of one vs two-or-more. `--min 1/2/3/5` print identical tallies, so a caller asking for 3 voters gets rows counted as double on two voters. | `tools/mori-vote-bind.py:160-190,421` |
| 9 | LOW | A case-insensitive vote-hash regex survives both the 16-arm selftest and the frozen C2 tally (identical numbers before/after, since no committed output uses uppercase hex). Survivor under the control module's own definition; nil effect on the frozen numbers today. | `tools/mori-vote-bind.py:64` |
| 10 | LOW | `HEALTH_WORDS` adds "is stuck" and "wedged" to the contract's three health words — the counter is stricter than the frozen predicate, not weaker. | `.ufo/waves/round-56/count-c1.py:45` |
| 11 | LOW | Two probe mutations are equivalent, not survivors — recording so they are not chased: dropping `^` from `VOTE_RE` (always used with `.match()`, which anchors) and reordering the roster ternary in `tally()`. | `tools/mori-vote-bind.py:64,162` |

No HIGH finding. Neither the C1 nor the C2 claim was falsified: both counters
report `met` at the freeze tip, the frozen control receipt reproduces
byte-identically with rc 0, and the re-bound round-55 tally over committed
bytes matches `evidence/tally-r55.txt` exactly.

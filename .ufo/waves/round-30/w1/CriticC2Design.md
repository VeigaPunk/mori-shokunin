# CriticC2Design — round 30 wave 1 (MoriR30.CriticC2Design)

Pre-data falsification of C2 (`.ufo/waves/round-30/contract.md:56-101`, landed `a66751b1`). Lane tip when read:
`b039dd4` ("wave-1 writer reports CaseR30a-d committed unread by the L1 (before gate, counter and freeze)"); gate,
counter, residual fix and `cases-a2-r30.json` not yet committed (`git ls-tree -r HEAD .ufo/waves/round-30/`,
`git ls-tree HEAD tools/fixtures/mori-oom-killers/`). I did not open `tools/mori-oom-killers.py` or any case JSON of
the CaseR30 reports. From those reports I read only the path and host prefixes under `## Files opened`. No tool was
installed or updated. One scratch file of seat briefs was written to `/tmp` and deleted; nothing else was written
outside this report.

Severity: **H** = C2 can read `met` while the claim's substance is false, or C2 is forced to fail for a non-claim
reason; **M** = a weaker hole or an unstated tradeoff; **L** = a fringe case.

| id | sev | where | kind |
|---|---|---|---|
| G1 | H | `:75-79` | defect: the gate's selftest is self-attested; a gate that flags nothing passes |
| G2 | H | `:78-79` | defect: zero writer files scanned gives a vacuous `blind_violations=0` |
| G3 | H | `:76-77` | defect: "0 on round-29" contradicts the round-30 forbidden-path policy |
| G4 | H | `:83-84` + gate brief (d) | defect: the forbidden-path denylist misses off-tree copies of the tool, including a public URL |
| F1 | H | `:68-69` + counter brief | defect: the "first add" lookup is inverted (newest add, not first) |
| F2 | H | `:96-101` | defect: tool changes before the freeze are unjudged; the residual fix lands with the r30 cases visible |
| S1 | H | `:69-74` | defect: the shape test admits masks that pin nothing about R6 |
| W1 | H | `:72-74`, `:84-86` + writer brief | defect: required pins force guesses where the text may not decide; this hides `unclear text` |
| D1 | H | `:81-84` | tradeoff: the central dispute is tested against rule text that was never amended |
| R1 | M | `:60-61`, `:100-102` | defect: a special-cased residual fix cannot be told apart from a general one |
| R2 | M | `:11-13` vs spot-check `:160-161` | routing gap: Judge02's `unclear text` pin is counted in 24/24 |
| W2 | M | `:84-86` | tradeoff: the pin allowlist excludes every field that still has a round-29 dispute |
| P1 | M | `:68-69` | defect: provenance is read at `<rev>`, not at the freeze |
| P2 | M | `:93` | defect: the gate and counter are committed after the reports exist |
| F3 | M | `:75` | defect: the gate blob may change after the freeze |
| N1 | M | `:68` | defect: `PASS N/N` is not tied to the number of cases in the file; ids can collide |
| T1 | M | `:81-82` | defect: the `rule-text.md` blob is unpinned |
| G5 | M | gate brief (d) | defect risk: a basename match on `SKILL.md` flags all four writers |
| G6 | M | `:75-79` | tradeoff: the blindness evidence is self-reported; check (b) exempts the case JSON |

## Gate (C2.4)

**G1 (H). A gate that flags nothing passes its selftest as counted.** At `:76-79` the counter accepts the gate's own
`--selftest` printing `PASS`. The BuildCountC2 brief (`wave1-spec.json`, item BuildCountC2) even says to show the
counter passing with "a trivial gate stub that passes". Counterexample: `--selftest) echo PASS; exit 0` plus
`echo blind_violations=0` in normal mode meets every gate clause of C2.4. The planted leaks are built by the gate's own
author (FixBlindGate brief: "synthetic reports built in a temp dir"), with one plant per class, so the selftest can be
tuned to its own plants. Impacted axis: operability (C2.4 is the R5 claim). Smallest correction: the counter owns the
plants. Commit a fixture directory of planted writer reports authored by a non-gate seat (at least 2 per class: a tool
line citation in two spellings, an output marker in prose, a forbidden path, no list). The counter runs the gate in
*normal* mode in a temporary repo, requires at least 1 violation per plant and 0 on the round-29 set, and ignores the
gate's own `PASS`.

**G2 (H). A vacuous zero.** The freeze run (`:78-79`) passes if the regex matches no file. This happens if the reports
are not in the tree at the freeze, if the regex is mistyped, or if a report is renamed. The round-29 order was safe
(reports in `e1c6bbe` before the freeze in `d6d5cb0`), but nothing in the round-30 contract requires it. Correction:
the gate prints `writers_scanned=<n>`, and the counter requires n to equal the number of distinct `author` values in
`cases-a2-r30.json`. The round-29 selftest anchor likewise requires n=8 at `d6d5cb0a`.

**G3 (H). The round-29 anchor forces blindness to the leak that matters most this round.** Round-29 writers
legitimately opened `tools/fixtures/mori-oom-killers/cases.json` and `cases-a2.json`
(`.ufo/waves/round-29/w2/AdjudicateBlindHits.md:51-57`). Round 30 forbids every fixture (`:83-84`; FixBlindGate brief
rule (d) "tools/fixtures/"). A gate that uses one policy and "reports 0 on the round-29 writer wave" (`:76-77`) must
therefore accept fixture paths. It is then blind to a round-30 writer who opened `cases-a2-r29.json`. That file's
frozen case `r29-a2-07-real-then-dryrun-zero-enter` pins exactly the disputed outcome: active, stamp 0, real send then
restart, giving `KILLERS_UNKNOWN`, `actions.sigterm` 0 and `earlier_invocation_send_lines` 1 (read from
`git show 58b61681:tools/fixtures/...cases-a2-r29.json`). The FixBlindGate brief lets the selftest "compare against
that expected count" instead, which contradicts the contract's literal "reports 0". The counter checks only `PASS`, so
the contradiction is invisible. Correction (pre-freeze amendment): the gate reads an explicit per-round allowlist
file. The selftest runs the round-29 set under the round-29 policy (expect 0, n=8) and plants under the round-30
policy that must include `tools/fixtures/mori-oom-killers/cases-a2-r29.json`.

**G4 (H). The denylist-by-root misses off-tree copies.** FixBlindGate rule (d) forbids "anything under the lane …
or anything under the fleet root" and allows everything else. Counterexamples that pass it:
- The lane's public mirror. `curl -sI` at 2026-10-22T21:17:29Z gave HTTP 200 for
  `https://raw.githubusercontent.com/VeigaPunk/mori-shokunin/master/tools/mori-oom-killers.py` and for
  `.../tools/fixtures/mori-oom-killers/cases-a2-r29.json` (status only; body not fetched). `cdfcf66`, the
  unbounded-from-last-version-line change, is an ancestor of public `master` (`git merge-base --is-ancestor cdfcf66
  b039dd4` returned 0). The writer brief tells writers to curl `raw.githubusercontent.com`.
- Sibling scratch. The FixToolResidual brief puts a full lane clone at
  `/fast/scratch/hyaku/mori-r30/FixToolResidual/lane/`; round-29 scratch holds `/fast/scratch/hyaku/mori-r29/*/`.
- `/tmp` copies, and `git -C <lane> show <rev>:tools/...` (a command, not a file path, so it never appears in a
  files-opened list).

Correction: make rule (d) an allowlist. Allowed: `.ufo/waves/round-30/rule-text.md`, `/home/vgpnk/.omp/agent/RULES.md`,
skill files, the writer's own scratch, and URLs under `raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/`,
`raw.githubusercontent.com/systemd/systemd/v262/` and `www.freedesktop.org/software/systemd/man/262/`. Everything else
is a violation. Observed: the four committed lists name only paths and hosts in that allowlist, so an allowlist gate
would still read 0 on them.

**G5 (M).** All four writers list the godspeed skill file, whose basename is `SKILL.md`. The brief's forbidden list
names `SKILL.md`. A basename or suffix match gives 4 false positives at the freeze and fails C2 for a gate defect,
repeating round 29's heading-grammar class. Correction: resolve each listed path to an absolute path before comparing,
and add the skill path to the selftest as a must-not-flag plant.

**G6 (M, tradeoff).** Check (b) exempts "own case JSON and derivation table". That is the only place where a copied
tool output would change a result: a writer who ran the tool and copied its fields into `expect` is textually
identical to an honest writer. The files-opened lists are self-reports. Three of the four lists (CaseR30b, c, d) omit
`/home/vgpnk/.omp/agent/RULES.md`, which the wave bounds tell every seat to read first. Either those seats skipped it
or the lists are incomplete, and the gate cannot tell which. Correction (uncounted): a wave-2 non-author audits each
writer's transcript (`history://MoriR30.CaseR30a` … `d`) for read and shell calls that touch lane paths, sibling
scratch or the public mirror, citing agent ids only.

**F3 (M).** "Committed before the freeze commit" (`:75`) constrains only the gate's first add. The counter brief runs
the `<rev>:` gate bytes for the selftest and does not say which bytes it uses for the freeze run. Counterexample: after
the freeze, the gate is edited to allowlist a path that one writer listed; at `<rev>` the selftest still passes and the
freeze run reads 0. Correction: the gate blob at `<rev>` must equal its blob at the freeze, and the freeze run uses the
freeze bytes.

## Freeze, provenance, pins (C2.3)

**F1 (H). The freeze lookup is inverted.** The contract (`:68-69`) says "the first lane commit that added it". The
BuildCountC2 brief operationalizes this as "the first commit in `git log --diff-filter=A --format=%H -- <file>`
order". `git log` lists newest first, so that picks the *latest* add. Counterexample: add the file (the true freeze),
run the tool, `git rm`, re-add an edited file. The counter takes the re-add as the freeze, and the blob matches.
Correction: `git log --reverse --diff-filter=A --format=%H <rev> -- <file> | head -1`. Also fail if any
`--diff-filter=D` commit touches the path, or if `git log <freeze>..<rev> -- <file>` is non-empty. Apply the same
lookup to the gate's first add.

**F2 (H). Pre-freeze tool changes are unjudged.** Judging governs only post-freeze changes (`:96-100`), and "follows
Judge11–13" (`:100-101`) is not counted. The r30 cases have been in the lane since `b039dd4`. No rule stops a non-writer
from reading them. FixToolResidual's brief does not forbid it, and the residual fix has not landed. Counterexample:
the C2.1 diff, which touches the same unbounded and stamp-less code as `cdfcf66`, also moves a disputed-shape output to
match a writer's pin. The r30 file then passes at its first run, with no judge. Round 29's "no tool run on this file
exists before this commit" (`d6d5cb0a` message) was a self-claim. Correction: (i) the committed C2.1 diff must equal,
by sha256, the diff in the FixToolResidual report (that seat was dispatched at `e936482`, before the reports existed);
any L1 delta is disclosed and judged. (ii) The counter or the closure records the r30 selftest at the tool of the C2.1
commit's parent and at the C2.1 commit. Any r30 case whose verdict or fields differ between the two needs a judge
ruling.

**P1 (M).** Provenance compares against the reports "at `<rev>`" (`:68`). A report edited after the freeze to match the
case file passes. Correction: each `w1/CaseR30?.md` blob at `<rev>` must equal its blob at its first add (`b039dd4`),
and that commit must be an ancestor of the freeze.

**P2 (M).** "Committed before the case file" (`:93`) lets the counter and gate land after the reports are readable, so
both can be tuned to them. For example, the order predicate can be widened to admit a writer case that stresses
list-versus-timestamp order (CaseR30d's second variation, per its brief). Correction: committed counter and gate bytes
must equal the sha256 that the BuildCountC2 and FixBlindGate seats report; any L1 delta is listed and reviewed by a
non-author.

**S1 (H). The shape test admits masks.** Each of the following meets `:69-74` literally, yet gives the same verdict
under both disputed readings, so six of them make `shape=6/3` while testing nothing about R6:
- (a) The earlier invocation logs `dryrun mode enabled`. Its "send line" (prefix match) is a dry-run send, never
  positive evidence (rule-text `:111`, A2-07).
- (b) `oomd_notices` ≥ 1, which gives `KILLER_ACTED` under any reading (rule-text `:45`).
- (c) The send record has a non-numeric `__MONOTONIC_TIMESTAMP`. It is uncounted in both readings (A2-10, rule-text
  `:114`), giving `sigterm` 0, `earlier` 0 and `KILLERS_UNKNOWN`.
- (d) The send is listed before the last version line but stamped after it, which tests ordering rather than R6.
- (e) `LoadState=not-found` together with `ActiveState=active` (the A2-09 path).
- (f) Journal records as bare strings, which older fixtures use (`cases.json` holds `str` records).

The writer brief forbids some of these (oomd 0, "real send"), but the counter brief says "shape test exactly as
contract C2.3", so nothing enforces them. Correction: add to the predicate: no `dryrun mode enabled` before the last
version line; every record is an object with a string `MESSAGE` and a numeric stamp, with stamps non-decreasing in
list order; `oomd_notices == 0` and `oomd_show` non-null; `LoadState=loaded`; pin types checked strictly (a JSON
`true` is not an integer).

**N1 (M).** `PASS N/N` (`:68`) is not tied to the file's case count. Counterexample: a tool change (allowed after a
`tool error` ruling) or a selftest that skips unknown `rule` values or duplicate ids prints `PASS 6/6` on an 8-case
file. The brief's id pattern `r30-disputed-<slug>` has no seat prefix. CaseR30a and CaseR30c both write
"absent stamp" variations, so a collision is plausible. Renaming is forbidden after the freeze and breaks provenance
before it. Correction: require N to equal `len(cases)` and the ids to be unique; a collision is a reported miss.

**W1 (H). Required pins hide disagreement.** The brief says "where the text does not decide a value, do not pin it",
but also says `fields` MUST pin `actions.sigterm` and `earlier_invocation_send_lines`, and `verdict` and `exit` are
mandatory. Those are exactly the values the R6 dispute is about. A writer who honestly finds them undecided must
either guess (a coin flip that can land on the tool's side and count as `met`) or omit them (fails the pins, read as
a plain miss, not as `unclear text`). The counter never sees "undecided". Correction: allow
`"undecided": [<field>…]` per case. The counter prints the undecided count, and any undecided required field is
treated as `unclear text`, which is an honest miss.

**W2 (M, tradeoff).** The pin allowlist (`:84-86`) excludes `earlyoom.dryrun` (Judge02 ruled it `unclear text`),
`version` and `grammar` (Judge11–13), and `dryrun_send_lines` and `process_group_lines` (the null-versus-0 debt,
`corpus/lessons/round-29.md:165-167`). The blind wave cannot re-surface any standing dispute, and the C2.1 fix of
exactly those fields is checked only by round-29 cases. Correction: writers MAY pin any output field the rule text
names; only the four required pins stay required.

**T1 (M).** No condition pins `rule-text.md`. A mid-wave edit (for example, adding the tool's unbounded-scope rule)
would make writers agree, and the counter would not see it. It is unchanged so far: blob
`4dd2da14674b4e684d89b6e50bd17c7e1e8708b3` at `a66751b1`, and `git diff --stat a66751b1 HEAD` is empty. Correction: the
counter requires `<freeze>:.ufo/waves/round-30/rule-text.md` to have that blob.

## The disputed rule itself

**D1 (H, tradeoff the judge must weigh).** The writers' text is a verbatim round-26/27 extract (`:81-84`). It does not
contain the round-29 tool rule "an unbounded scope's current invocation starts at the last version line"
(`corpus/lessons/round-29.md:141-142`); `grep -n 'last version' rule-text.md` finds nothing. Round 29 carried
"rule-text amendments before any writers … the unbounded-scope definition" (`round-29.md:165-166`), and this contract
neither makes nor waives that amendment. Two readings of the text:
- Literal: rule-text `:25` scopes lines with a stamp ≥ `ActiveEnterTimestampMonotonic`. With 0 or absent, every line
  is in scope (A2-05 `:109`). The send is then positive evidence even with an incomplete scope (`:45`), giving
  `KILLER_ACTED`, `sigterm` 1 and `earlier` 0.
- Split: `:29` says the version line is "the first line of an invocation", so the send is in an earlier invocation
  (A2-06 `:110`, active: no verdict change). This gives `KILLERS_UNKNOWN`, `sigterm` 0 and `earlier` 1, which is what
  the tool does.

Round 29 already split on this: CriticC2Verdict F4 against ReviewLandedFix F2 (`round-29.md:156-161`). The two claims
are also coupled. A `tool error` ruling for the literal reading cannot be acted on, because moving the tool to
`KILLER_ACTED` breaks frozen `r29-a2-07-real-then-dryrun-zero-enter` and so condition 1. Any literal-reading writer
therefore resolves only as a C2 miss. That is honest, but it should be declared in advance. Correction (pre-freeze,
appended): state that the rule text was deliberately left unamended, so `met` certifies that the round-26/27 text
decides the shape, and state that a literal-reading case is a miss, never a tool change.

## Residual fix (C2.1)

**R1 (M). A special-cased fix is invisible to the counter.** Scan of the committed fixtures at `58b61681`:
- All three failing r29 cases are non-active units with exactly one version line and exactly one stamp-less record:
  `r29-a2-10-inactive-lone-missing-stamp`, `-failed-stamped-positive` and `-not-found-earlier-stamped-positive`.
- No older file pins `version`, `grammar`, `dryrun_send_lines` or `process_group_lines` for any non-active unit. The
  only non-active pins are `earlyoom.actions: null` on `c06`, `c07` and `c29` (both cases.json and
  cases-supplementary.json), `a2-05-monotonic-zero-inactive-quiet`, `a2-06-inactive-earlier-invocation-sends-acted`
  and the two `a2-08` null-journal cases.

So a fix gated on "non-active and a stamp-less record exists" passes 24/24 plus 32/32/30. It does so while
`a2-06-inactive-earlier-invocation-sends-acted` (two version lines, all stamped) keeps `version` null and `grammar`
`unverified`, even though the basis Judge11–13 cite (round-26 `:82`, `:91`; `Judge11.md:22-23`) does not depend on
stamps. The guard at `:101-102` ("may not turn any `KILLER_ACTED` of an older file into another verdict") is vacuous:
condition 2 already pins every older verdict. Correction: name `a2-05-monotonic-zero-inactive-quiet` and
`a2-06-inactive-earlier-invocation-sends-acted` as the generality probe in FixToolResidual's full-output differential.
The judge reads their `version`, `grammar` and counter outputs before and after the fix; any difference from the r29
cases' behavior needs a stated rule-text reason (the L1's round-29 dissent, `round-29.md:152-154`, is such a reason
and must be applied consistently).

**R2 (M).** R4 routes "Judge02's `unclear text` case remain[s] open" (spot-check `:160-161`). The contract is silent.
`r29-a2-07-dryrun-then-real-missing-enter` passes now (`round-29.md:144`, "all 24 verdicts and exits match"), so
`PASS 24/24` would count a pin (`earlyoom.dryrun`) that a judge ruled undecidable, while the rule text still leaves
`dryrun` undefined (`round-29.md:166-167`). Correction: the closure names Judge02 as open, and `C2=met` does not
discharge it.

## Checks the planner should run

- `git log --diff-filter=A --format=%H -- <file>` against a re-add sandbox, to confirm F1 in the committed counter.
- The counter with a stub gate (`echo PASS`; `blind_violations=0`): it must print `C2=unmet` after G1 and G2 are fixed.
- Gate on a planted writer report listing the public raw URL and the FixToolResidual clone path: it must flag both
  (G4).
- FixToolResidual's differential rows for `a2-05-monotonic-zero-inactive-quiet` and
  `a2-06-inactive-earlier-invocation-sends-acted` (R1).

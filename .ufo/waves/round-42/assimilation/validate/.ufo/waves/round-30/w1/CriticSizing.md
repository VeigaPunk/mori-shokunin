# CriticSizing — mori round 30, wave 1 (critic, leaf, read-only)

Seat `MoriR30.CriticSizing`. Inputs read: prompt `.ufo/prompts/mori-round-30.md:343-351` (fleet), lane
`.ufo/waves/round-30/contract.md` (at `a66751b1`), `corpus/lessons/round-29-verifier-spotcheck.md`,
`.ufo/waves/round-30/rule-text.md`, `.ufo/waves/round-30/wave1-spec.json` (item prompts), round-29
`residual/{CriticC2Verdict,ReviewLandedFix}.md`, `w2/Judge02,11,12,13.md`, `w2/AdjudicateBlindHits.md`,
`w1/CaseA2*.md` headings, the four case files and the retention policy. No lane or fleet write except this file;
no scratch files (the tool probes used process substitution only). Tools installed or updated: none. I read no
tool source, and this report quotes no tool source lines.

## Bottom line

1. **Most likely miss: C2 condition 3, the blind pin of the disputed shape. It is coupled to condition 1.** Four
   blind writers must each get verdict, exit, `actions.sigterm` and `earlier_invocation_send_lines` right on 8
   cases. The shape is the one whose reading two non-author round-29 seats disagreed on, and `rule-text.md` was
   not amended to settle it. If any writer takes the "everything is in scope" reading, the result is a miss
   whatever the judge rules (F1).
2. **One defect is certain and can be fixed now:** C2 condition 4's "reports 0 on the round-29 writer wave"
   cannot hold under the gate rules the wave-1 item specifies. All 8 round-29 writer reports break them (F2).
3. Three more fixable defects, to settle before any writer report is read: the `author` field spelling (F3), the
   C1 "exactly one file" trap on 29 duplicated case ids (F4), and counters and before-receipts that the
   contract cites but has not committed (F5). Two counter loopholes allow post-data tuning (F6).
4. C1's remaining risk is mechanical and the L1 can control it (F4, F7). C2 condition 3's risk cannot be reduced
   after writer dispatch without breaking blindness. Under REPAIR-FIRST, with one rejection left before the lane
   is parked, the L1 should pre-register it as the named likely miss (F1).

## Sizing rules check (prompt `:343-351`)

| Rule | C1 | C2 |
|---|---|---|
| One concrete after-value | `C1=met`, exit 0 (`contract.md:25,51`) | `C2=met`, exit 0 (`contract.md:58,95`), but it is an AND of about 15 sub-checks bundling routed defects R4, R5 and R6 |
| Re-derivable by one command over committed bytes | Not yet. `count-c1.sh` and `evidence/c1-before.txt` are absent at `a66751b` (`git ls-tree -r --name-only a66751b -- .ufo/waves/round-30` lists only `contract.md`, `evidence/census-start.txt`, `rule-text.md`). The command runs the working-tree script, not `<rev>`'s blob (F5, F6) | Same: `count-c2.sh` and `c2-before.txt` are absent. The gate copy comes from `<rev>`, not from the freeze commit (F6) |
| Sized to one round | Yes: 6 source scribes for 3 required ids; 36 eligible case ids (F4) | No: round 29 missed on the same R4 selftest and R5 blind conjuncts (`round-29-verifier-spotcheck.md:66-75`); this round re-carries both and adds a new blind wave |
| Universal clauses enumerated | "every row", "every fields item", "exactly one": enumerated by the counter | "every case", `unselected=0`, "no KILLER_ACTED of an older file" (`contract.md:101`): enumerated, because older files pin every verdict |
| Prefer 2 claims | 2 | 2. Splitting C2 is impossible: two claims on one axis count as one (prompt `:19`) |
| Never narrow after landing | stated (`contract.md:5`) | stated (`contract.md:5,99-100`) |

## F1 (high): C2 condition 3 depends on blind writers choosing one reading of an undecided text

**Counterexample.** One writer case for variation `b1`/`b2`/`c2`/`d1` (`ActiveEnterTimestampMonotonic=0`) reads
`rule-text.md:25-26` literally: every line is at or after 0, so every line is in scope. It then applies `:44-45`
("Positive evidence stands even when the scope is incomplete") and pins `KILLER_ACTED`, exit 1, `sigterm>=1`,
`earlier=0`. Two outcomes are possible, and both are a C2 miss:
- The judge rules `case error` or `unclear text`. That is a miss by contract (`contract.md:99-100`).
- The judge rules `tool error`. Then the fix must keep condition 1. But `cases-a2-r29.json` pins the opposite
  split for the same active, unbounded shape: `r29-a2-07-real-then-dryrun-zero-enter` (`KILLERS_UNKNOWN`,
  sigterm 0, earlier 1) and `r29-a2-07-real-dryrun-real-missing-enter` (`KILLER_ACTED` from a current SIGKILL,
  sigterm 0, earlier 1). A tool moved to the "all in scope" reading fails those pins, so condition 1 fails.

**Evidence that the text supports both readings:**
- Round 29's own counter defined unbounded scope as "every stamped record of an active unit"
  (`.ufo/waves/round-29/contract.md:139-140`).
- CriticC2Verdict F4 says "No amendment changed the rule text, so the tool now holds an unstated rule"
  (`round-29/residual/CriticC2Verdict.md:102-103`). Its recommendation was "Amend the rule text before any
  writer or tool work … (d) unbounded scope is either every stamped record or from the last version line, with
  H1's verdict stated explicitly" (`:127-135`).
- The closure ruled the other way, from A2-05, A2-06 and A2-07 (`round-29-verifier-spotcheck.md:84-90`).
- `rule-text.md` is the unamended round-26/27 extract (`rule-text.md:1,59,100`).
- The writer item gives contradictory orders: "`fields` MUST pin `earlyoom.actions.sigterm` and
  `earlyoom.earlier_invocation_send_lines`" next to "where the text does not decide a value, do not pin it"
  (`wave1-spec.json`, CaseR30a–d prompts). A writer who sees the ambiguity and obeys the second order fails
  `pins_ok`.

**Tool side (probe, not a gap).** I ran the entering-tip tool (`git show 58b61681:tools/mori-oom-killers.py`
through `python3 -I -B`, inputs passed by process substitution) on my own invented inputs. They copy the 8
assigned variations, plus an empty-stamp control. The tool answers all of them under the split reading:
current-invocation sends 0, and earlier sends counted, escalation lines included. So a writer who takes the split
reading matches the tool. The risk sits entirely on the writer side. Per-case outputs are withheld on purpose
(blindness).

**Margin.**
- Shape needs at least 6 cases from at least 3 authors, out of 4 writers × 2 cases (`contract.md:65-69,81`).
- One dead writer leaves exactly 6 cases, and all 6 must be on shape. Two dead writers is a certain miss.
  Dead seats are never replaced (prompt `:201`).
- Older files hold no case of this shape. Scan: `cases.json`, `cases-supplementary.json` and `cases-a2.json`
  have 0, 0 and 2 active-unbounded cases, and none has a send before the last version line. This agrees with the
  spotcheck at `:94`.

**Axes:** operability (claim), calibration (if the miss is framed as a tool error).

**Class:** a tradeoff the judge must accept as is. It cannot be fixed after writer dispatch: editing
`rule-text.md` now would give writers different bytes. The only safe corrections are honest pre-registration
plus survival and format steps:
- Before any CaseR30 report is read, append a LOG note naming C2 condition 3 as the expected miss risk. Record
  that the text was not amended (and why), and that a `tool error` ruling toward "all in scope" cannot be fixed
  without breaking condition 1.
- Pre-declare that any mismatch on verdict, sigterm or earlier goes to two independent judges. A split ruling
  counts as `unclear text`, which is a miss. This is harder, not narrower, and closes the Judge02/Judge04-style
  split (`CriticC2Verdict.md:62-74`).
- On a writer's provider backoff, resume the same identity (prompt `:219-221`). Never re-dispatch.

## F2 (high, certain, fixable now): gate selftest "reports 0 on the round-29 wave" contradicts the gate's own rules

**Counterexample.** FixBlindGate rule (c) requires a `## Files opened` heading. Rule (d) forbids lane contracts
and `tools/fixtures/` in that list. All 8 round-29 writer reports:
- use other headings: `CaseA207a.md:192` "Opened files and URLs", `CaseA207b.md:195`, `CaseA207c.md:192`,
  `CaseA207d.md:194`, `CaseA210a.md:203`, `CaseA210b.md:195`, `CaseA210d.md:182`; `CaseA210c.md:194` has only a
  plain `Files opened:` line;
- list contract or fixture reads that round 29 allowed: for example, `CaseA210c.md:198-201` lists both
  contracts, `cases.json` and `cases-a2.json`. AdjudicateBlindHits ruled these "allowed fixture reads"
  (`:64-65`).

So a gate built to the item reports up to 8 writer violations on that wave. The FixBlindGate item already
foresees "the selftest compares against that expected count". The contract text, however, says it "reports 0"
(`contract.md:76-77`). A closure that reads the contract literally either sees condition 4's selftest premise
fail, or sees the definition redefined after data.

**Axes:** operability, discernment.

**Smallest safe correction (pre-data, harder):** amend `contract.md` before the gate is committed. Ready text
below as A1.

## F3 (high, fixable now): the `author` value is not pinned to a literal

**Counterexample.** Round-30 writers are told `"author": "<your seat name>"`. Their seat ids are
`MoriR30.CaseR30a`… (wave roster). Round 29 gave the literal: `"author": "CaseA207a"`
(`round-29/wave1-spec.json`, CaseA207a prompt), and the round-29 counter checks the author against a fixed map
(`round-29/count-c2.sh:141-142,214`). Suppose a writer writes `MoriR30.CaseR30a` and a round-30 counter copies
the round-29 logic. Then `authors` drops, `provenance` finds no `w1/MoriR30.CaseR30a.md`, and C2 misses. The
cases cannot be edited afterwards, because provenance requires canonical equality.

**Axes:** operability.

**Correction (pre-data, before BuildCountC2's counter is committed):** attribute authorship by the report file
the case is found in. Accept an `author` field equal to `<name>` or `MoriR30.<name>` for that same file, and
require that no case occurs in two writers' reports (harder). Ready text below as A2.

## F4 (medium, fixable now): C1 condition 3 "exactly one file" rules out the canonical scope cases

**Counterexample.** 29 case ids appear in both `cases.json` and `cases-supplementary.json`. They include
`c02-scope-boundary-one-microsecond-before`, `c03-scope-boundary-exactly-at`, `c04-incomplete-scope-with-action`,
`c05-incomplete-scope-without-action`, `c06-earlyoom-inactive` and `c08-null-journal` (jq id union with
`uniq -d`, 29 lines). A row citing any of them fails condition 3 (`contract.md:32`). The ProbeC1Cases item steers
toward exactly these shapes ("a send one microsecond before it", "null journal"). No C1 seat prompt mentions
uniqueness: a search of ProbeC1Cases, DraftEntryC1 and ReviewC1Reachability for "exactly one", "duplicat" and
`c0[2-5]` found no hits.

**Eligible pool:**
- `cases.json`: `c19-version-line-only`, `c24-…`, `c28-…`.
- `cases-supplementary.json`: `c33-…`, `c34-escalation-only-incomplete-scope`, `c35-…`. `c35` has
  `fields: {}`, so it cannot fill a row.
- `cases-a2.json`: all 30, 3 per rule A2-01 to A2-10; 5 of them pin `earlier_invocation_send_lines > 0`.

At least 8 rows remain reachable, but only if the table draws mostly from `cases-a2.json`.

**Axes:** depth.

**Correction (execution step, not an amendment):** the L1 filters the probe's rows against the 29 duplicate ids
before committing the table. Do not relax "exactly one".

## F5 (medium, fixable now): the contract cites receipts and counters that do not exist yet

`contract.md:50-51,93-95` states the before-values as observed ("Before at `58b61681`: … `evidence/c1-before.txt`").
At `a66751b` neither counter nor receipt is committed (ls-tree above). As written, that is provenance for files
that do not exist yet.

**Correction:** land each counter and its before-receipt in a commit before the entry, the rows, the excerpts or
the case file, and cite that landed hash in LOG. The order is checkable later with
`git merge-base --is-ancestor <counter-commit> <first-entry-commit>`.

## F6 (medium): two post-data tuning loopholes in the counters

**Counterexample 1.** BuildCountC2 runs `<rev>:check-blind-wave.sh` against the freeze-commit reports, and only
requires the gate's first add to precede the freeze (BuildCountC2 prompt). Gate v1 is committed before the freeze.
After the writer reports are seen, v2 is committed at the tip. The counter then uses v2. Condition 4 says
"committed before the freeze commit" (`contract.md:75`) but never requires the gate to stay unchanged.

**Counterexample 2.** The counting commands run the working-tree `count-c*.sh` (`contract.md:47,91`). A counter
edited after landing changes the after-value without any committed-byte trace.

**Correction (harder):** A3 below.

## F7 (low–medium): C1 condition 4 excerpts, and C2 condition 1 harm exposure

- **Excerpts.** Quotes must match the excerpt lines verbatim after whitespace collapsing (`contract.md:40-41`).
  Hand-typed excerpts, or quotes taken from rendered HTML or XML (systemd man sources carry inline tags), will not
  match. Correction: generate each excerpt mechanically from the fetched bytes, numbering every physical line
  (`awk '{print NR"\t"$0}'`, not `nl`, which skips blank lines), and record that command in the Gate evidence.
- **C2 condition 1 harm.**
  - The feasibility probe passes 24/24 by reporting a version and zero line counts for non-active units
    (`CriticC2Verdict.md:22-33`). ReviewLandedFix F1 calls this a breach of `rule-text.md:49-50` ("never zero
    counts") (`ReviewLandedFix.md:36-46`).
  - The same probe also turned `null` into `0` for the unreadable-show cases c25 and c32 (`CriticC2Verdict.md:31-33`).
    Those cases are unpinned, so they PASS, but the change is a harm.
  - The FixToolResidual acceptance criterion bans only `KILLER_ACTED` flips.
  - Correction (execution step): the L1 rejects any fix whose full differential changes any field outside
    non-active units with a readable show text. It records in LOG the Judge11–13 basis for zero counts outside
    `actions`.
- **Retention.** I scanned all 9 policy classes over the round-30 wave files (spec, dispatch, run, err,
  registry, contract, rule text): 0 hits. Positive control: class R7 hits 1 line in
  `.ufo/round-2/interactive-cutover/wwkd.md`. Seat reports committed as wave evidence can still raise the metric
  if they name the routing key or the operator config path. Run the retention scan on each candidate commit
  before landing.

## Ready-to-paste pre-data amendment (append to `contract.md` before the gate, the counters or any CaseR30 report is committed or read)

```markdown
## Amendment A1 (pre-data, from w1/CriticSizing F1-F6; harder, nothing narrowed)

- A1 (C2.4 selftest premise): "it reports 0 on the round-29 writer wave at `d6d5cb0a`" is replaced by: on
  `.ufo/waves/round-29/w1` at `d6d5cb0a` with regex `^CaseA2(07|10)[a-d]\.md$`, the gate reports none of the 20
  hit lines adjudicated in `.ufo/waves/round-29/w2/AdjudicateBlindHits.md`. Its only reports are rule (c)/(d)
  violations at the files-opened lists of the eight writer reports (round-29 writers were allowed contract and
  fixture reads and used other headings). The selftest pins that exact (file, rule) set, committed with the gate.
  Any extra or missing report is FAIL.
- A2 (C2.3 authorship): a case's author is the writer whose report `.ufo/waves/round-30/w1/<name>.md` holds it
  (first fenced JSON array, canonical equality). Its `author` field must equal `<name>` or `MoriR30.<name>`.
  A case found in two writers' reports counts for neither.
- A3 (frozen instruments): `count-c1.sh`, `count-c2.sh` and `check-blind-wave.sh` each print the sha256 of their
  own blob. The counters require `check-blind-wave.sh`'s blob at `<rev>` to equal its blob at the freeze commit,
  and run the gate from the freeze commit's blob. The closure command is
  `bash <(git -C /home/vgpnk/Projects/shokunin/mori-shokunin show <rev>:.ufo/waves/round-30/count-cN.sh) <rev>`.
  LOG records each counter's and the gate's blob hash before the first CaseR30 report is read.
- A4 (ordering): the counter and gate commits, with their before-receipts, are strict ancestors of the first
  commit that adds any `.ufo/waves/round-30/w1/CaseR30*.md` file.
- A5 (judging the disputed shape): a writer/tool mismatch on `verdict`, `exit`, `earlyoom.actions.sigterm` or
  `earlyoom.earlier_invocation_send_lines` in a `cases-a2-r30.json` case goes to two independent non-author
  judges. Any disagreement between them is `unclear text`, which is a C2 miss. A `tool error` ruling that cannot
  be fixed while keeping conditions 1-2 is reported as a C2 miss.
- Disclosure: `rule-text.md` was not amended to settle the unbounded-scope reading (round-29
  `residual/CriticC2Verdict.md:127-135`). C2.3 is the round's named highest miss risk.
```

## Commands run (outputs summarized above; each read-only)

- `git ls-tree -r --name-only a66751b -- .ufo/waves/round-30`: 3 files.
- `jq` over `wave1-spec.json` items (names, roles, CaseR30a–d, FixBlindGate, FixToolResidual, BuildCountC1/C2,
  ProbeC1Cases, DraftEntryC1 prompts).
- `jq -r '.cases[].author' cases-a2-r29.json | sort | uniq -c`: 8 bare names × 3.
- `jq` id union of the three older files with `uniq -d`: 29 duplicates. The shape scan over the older files and
  `cases-a2-r29.json` found the active-unbounded pre-restart-send pins listed in F1.
- Tool probe: `python3 -I -B <(git show 58b61681:tools/mori-oom-killers.py) --inputs <(…invented…)` × 9, all
  exit 2.
- `rg -n '^## ' / 'Files opened'` over `round-29/w1/CaseA2*.md`: headings as in F2.
- The retention-class `rg` loop over the round-30 wave files: 0 hits; the R7 positive control matched.
- `git show HEAD:MANIFEST.json` (fleet): mori closures lr26 admitted, lr27 rejected-honest-stop, lr28 admitted,
  lr29 rejected-honest-stop.

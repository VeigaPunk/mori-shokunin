# Mo60Scribe76 — draft QUALITY criteria 156 and 157

Seat: Mo60Scribe76 (leaf, no subagent dispatch). Lane: `mori-shokunin`,
read-only — no edit to `corpus/QUALITY.md`, `SCORECARD.md`, `LOG.md`, the
corpus registry or lane VCS. Scratch:
`/fast/scratch/hyaku/mori-r60/Mo60Scribe76` (removed at close; receipts are
inline below). Tools: git 2.56.0, Python 3.14.8; no installs or updates.
Disk guard at start: `/fast/scratch/hyaku` 26% used, 598.2G free (green).

## 0. What the lane already holds

The two criteria landed before this seat ran, in commit `398d3225`
("…QUALITY 156-157"), at `corpus/QUALITY.md:1590` (156) and `:1605` (157),
under `## Criteria added round 60 — pointer existence and verdict routing`
(`:1588`); tip when read `b3c25613` (it advanced to `0f8340cf` while this seat
ran, and `corpus/lessons/round-60.md` was being edited by another seat — all
readings below are pinned to a named revision). So this seat is not adding
text — it is drafting the texts that must stand, and checking every embedded
claim. Six corrections are needed against the landed bytes: three are
citations that do not reproduce (items 1, 4, 5 in §4), two make the rule noisy
or unsatisfiable as written (2, 3), and one understates the code it describes
(6). The exact texts below are the corrected draft; §4 is the delta list
against the landed bytes.

## 1. Exact texts (deliverable)

```markdown
156. Every evidence pointer a round files — in its report(s) and in the
    SCORECARD claim rows it adds or re-points — must resolve at the revision
    it names before the round is filed. Sweep the filed text with
    `git show <rev>:<file> | grep -oE '\x60(\.ufo|corpus)/[^\x60]+\x60' |
    tr -d '\140' | grep -vE '[*{}…]|:[0-9]|/$' | sort -u` and resolve each
    surviving literal with `git cat-file -e <rev>:<path>`; a hit that fails is
    re-pointed in place with an `r60-correction:` marker naming the real
    committed path, or struck before filing. Brace, glob, ellipsis,
    `:line-range` and directory tokens are filtered out rather than counted as
    hits, and backtick anchoring matters: the unfiltered
    `git grep -oE '(\.ufo/…|corpus/…)'` form returns 329 distinct tokens and
    11 "dead" at entering `ddfb12fb…` — 2 real pointers, 3 pre-existing dead
    names and 6 truncation fragments (`corpus/evidence/watch-r2-20261015T15`,
    `.ufo/waves/round-24/w2/Mut`, …), while the filtered form over the same
    whole-table input returns 4.
    ← `corpus/lessons/round-60.md` `## Mistakes` row 1 and
    `corpus/lessons/round-59-verifier-spotcheck.md:93`: the r59 claim rows
    (`SCORECARD.md:2950-2951` at entering `ddfb12fb…`) cited
    `.ufo/waves/round-59/evidence/c1-entering.txt` and `c2-entering.txt`,
    never committed under those names; the real receipts are
    `.ufo/waves/round-59/evidence/control-c1-do-nothing.txt` and
    `control-c2-do-nothing.txt`, present at `7b86704d…` and `ddfb12fb…`.
    Shown able to fail: sweeping those two rows at `ddfb12fb…` prints `DEAD`
    for both names (2 of 3 tokens) and `python3
    .ufo/waves/round-60/count-c1.py ddfb12fb…` prints `C1=unmet
    dead-uncorrected=2 receipts=0/2 absent-set=0/5 lesson=absent …`, exit 1;
    at the corrected revision (tested `b3c25613`) the sweep prints nothing and
    the counter prints `C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5
    lesson=ok …`, exit 0. Not covered: pointers written outside
    `.ufo/`/`corpus/` or only as a basename; a name that resolves to the
    wrong file; and rows the round does not touch — the historical table still
    carries pre-existing unresolvable names
    (`.ufo/reports/round-12/mori.md`, `.ufo/state`, absent at both
    `7b86704d…` and `ddfb12fb…`), which this criterion records but does not
    re-point.

157. A verifier's failure reasons must route to the verdict it composes:
    every reason class it can emit must be able to block, or not be emitted at
    all (`grammar:` may not be orphaned), and the claims it accepts must
    resolve to pairwise distinct byte spans of at least 8 bytes each, with
    whitespace-only quotes rejected. ← S561 (Mo59Critic22 D3) and S563
    (Mo59Critic25): the r59 real-entry arm re-summed `eval_entry`'s reasons
    through a whitelist that omitted `grammar`
    (`.ufo/waves/round-59/count-c2.py:303-305` at `7b86704d…`) and composed
    `met` from `entry_ok`/`rows_ok`/`pins_ok` alone (`:360-361`), so a root
    whose `eval_entry` returned `ok=False, reasons=['grammar:…']` still scored
    `entry=ok`; its drift arm accepted any nonzero exit (`:251-261`) without
    reading a reason. Shown able to fail: loading those pinned bytes and
    applying `:303-305` to `eval_entry` over
    `.ufo/waves/round-60/trees-c2h/h02-malformed-claim` prints
    `ok=False reasons=['grammar:- **K77** — malformed claim line missing']`
    and `entry_ok=True` (rows/pins also true) — the met-flip; the hardened
    `tools/mori-entry-claims-check.py` (sha `cffe9f33…e6e69`) composes
    `len(reasons) == 0` (`:239`) with `MIN_SPAN = 8` (`:49`) and returns
    `ok=False` with that same `grammar:` reason for `h02` and `ok=True` for
    `h00-good-control`, and `python3 .ufo/waves/round-60/count-c2.py
    ac496c7c…` prints `C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok
    rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=ac496c7c…`, exit 0
    (`evidence/c2-at-freeze.txt`). Not covered: reasons the verifier cannot
    express at all (the semantic truth of a well-formed quote, a claim that
    cites a real span of the wrong subject) — judge work; and span collapse is
    keyed on `(cfile, start, end)` (`:162-165`), so the same bytes cited under
    two different copies of one artifact are not collapsed.
```

Implementation notes for whoever files it: `grep -oE` accepts `\x60`
(backtick) and `tr` `\140` deletes it, but `git grep`'s regex engine does not
accept `\x60` (`git grep -hoE '\x60' … | wc -l` printed `0`), so the sweep is
written as `git show <rev>:<file> | grep`, one `git show` per filed file. The
anchoring is what removes the truncation debris: a token must start and end on
a backtick (`\x60`), so the sweep stops at the closing quote instead of running
into the prose; a plain
`(\.ufo|corpus)/[A-Za-z0-9._/-]+` class swallows prose-adjacent fragments and
reports them as dead names.

## 2. Evidence for 156

Pointer existence, `git cat-file -e` at both revisions:

```
ddfb12fb .ufo/waves/round-59/evidence/c1-entering.txt            ABSENT
ddfb12fb .ufo/waves/round-59/evidence/c2-entering.txt            ABSENT
ddfb12fb .ufo/waves/round-59/evidence/control-c1-do-nothing.txt  EXISTS
ddfb12fb .ufo/waves/round-59/evidence/control-c2-do-nothing.txt  EXISTS
7b86704d … same four results (c1/c2-entering ABSENT, controls EXISTS)
```

Red arm, row scope — the two claim rows at the entering revision:

```
$ git show ddfb12fb:SCORECARD.md | sed -n '2950,2951p' \
  | grep -oE '\x60(\.ufo|corpus)/[^\x60]+\x60' | tr -d '\140' \
  | grep -vE '[*{}…]|:[0-9]|/$' | sort -u
corpus/knowledge/wave-settlement-artifacts-r59.md
.ufo/waves/round-59/evidence/c1-entering.txt
.ufo/waves/round-59/evidence/c2-entering.txt          (3 tokens)

$ … | while read -r p; do git cat-file -e "ddfb12fb:$p" || echo "DEAD $p"; done
DEAD .ufo/waves/round-59/evidence/c1-entering.txt
DEAD .ufo/waves/round-59/evidence/c2-entering.txt      (2 of 3 dead)
```

Red arm, counter (frozen `count-c1.py`, run from the lane root, `--scratch`
under this seat's scratch, `TMPDIR` set there):

```
$ TMPDIR=$S python3 .ufo/waves/round-60/count-c1.py \
    ddfb12fb0838b4307c445194a844f0c4b1950195 --scratch $S/c1-entry
C1=unmet dead-uncorrected=2 receipts=0/2 absent-set=0/5 lesson=absent \
  rev=ddfb12fb0838b4307c445194a844f0c4b1950195 \
  failed=absent_set=0/5,absent_table_absent,correction_incomplete,dead=2,\
  lesson_absent,receipt_absent:…/r59-c1-met.txt,receipt_absent:…/r59-c2-met.txt,receipts=0/2
rc=1
```

Green arm, same counter at the correction revision:

```
$ TMPDIR=$S python3 .ufo/waves/round-60/count-c1.py b3c25613 --scratch $S/c1-tip
C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c25613
rc=0
```

Green arm, row scope at the same revision (the two rows now carry
`r60-correction:` and cite the real receipts):

```
$ git show b3c25613:SCORECARD.md | sed -n '2950,2951p' … (same pipeline)
OK   corpus/knowledge/wave-settlement-artifacts-r59.md
OK   .ufo/waves/round-59/evidence/control-c1-do-nothing.txt
OK   .ufo/waves/round-59/evidence/control-c2-do-nothing.txt      (0 dead)
```

Sweep noise measurement that motivates the filter:

```
whole SCORECARD at ddfb12fb, unfiltered regex:
  tokens=329  dead=11
  = 2 real (.ufo/waves/round-59/evidence/c{1,2}-entering.txt)
  + 3 pre-existing (.ufo/reports/round-12/mori.md, .ufo/reports/round-41/mori.md, .ufo/state)
  + 6 truncation fragments (…roster-r12-20261019T220912Z-, corpus/evidence/watch-r2-20261015T15,
    .ufo/waves/round-24/evidence/c1-, .ufo/waves/round-24/w2/Mut,
    .ufo/waves/round-25/evidence/routed-r24-, .ufo/waves/round-50/evidence/a2-c)

whole SCORECARD at ddfb12fb, backtick-anchored + literal filter:
  tokens=246  literal=188  dead=4  (the 2 real + the 2 backticked pre-existing names)
```

## 3. Evidence for 157

r59 orphan site, pinned bytes at `7b86704d` (`git show
7b86704d:.ufo/waves/round-59/count-c2.py`):

```
303        entry_ok = not any(r.startswith(("frontmatter", "distinct", "claims_min",
304                                         "files", "span", "entry_absent"))
305                           for r in reasons)          # no "grammar"
360    met = (tool_ok and st_ok and scan_ok and drift_ok and tree_ok
361           and entry_ok and rows_ok and pins_ok and trees_ok)
251    # drift arm: r53 file must be judged FAIL
260        drift_ok = p.returncode != 0                     # exit code only
```

Red arm — the pinned r59 verifier on the r60 hostile tree (module loaded from
scratch; `eval_entry` is the pinned function, composition applied verbatim):

```
r59 eval_entry ok=False reasons=['grammar:- **K77** — malformed claim line missing']
r59 measure() entry_ok=True  (grammar reason dropped: ['grammar:- **K77** — malformed claim line missing'])
r59 met contribution: entry_ok=True, rows_ok/pins_ok from same reasons -> True True
```

So the r59 predicate composes `C2=met` for an entry whose only failure reason
is a `grammar:` line — the met-flip `corpus/lessons/round-59-verifier-spotcheck.md`
routed and `SCORECARD.md:2951` (r59 C2 row) decertified as **Unverified**
(“verified met-flip counterexamples on the frozen predicate … orphaned
`grammar:` reasons”, Mo59Critic22 D2/D3, Mo59Reviewer08).

Honesty note: the *filed* r59 entry is not itself a met-flip on this class —
`eval_entry` over the real `corpus/knowledge/wave-settlement-artifacts-r59.md`
(at `7b86704d`, materialized copy+artifacts+SOURCES in scratch) returned
`ok=True claims=13 files=6` with no `grammar:` reason. The defect is predicate
blindness, demonstrated on the hostile construction, exactly as S561 frames it.

Green arm — hardened verifier, same trees, from the lane root:

```
$ python3 tools/mori-entry-claims-check.py --root …/trees-c2h/h02-malformed-claim \
    --entry corpus/knowledge/wave-settlement-artifacts-r59.md --registry corpus/SOURCES.md \
    --artifacts-json $S/tool/artifacts.json --min-claims 10 --min-files 3
ok= False reasons= ['grammar:- **K77** — malformed claim line missing']
stats= {'claims': 10, 'files': 4, 'spans': 10, 'min_span': 13}

$ … --root …/trees-c2h/h00-good-control
ok= True reasons= []   stats= {'claims': 10, 'files': 4, 'spans': 10, 'min_span': 13}
```

Verdict routing and span floor in the tool: `return (len(reasons) == 0)` at
`:239`; `MIN_SPAN = 8` at `:49`; span key `(cfile, start, end)` at `:162` with
`distinct:dup_span` at `:165` and `span:short` at `:168`; the counter's entry
arm additionally demands `spans == claims` (`count-c2.py:330-331`). Committed
freeze receipt: `evidence/c2-at-freeze.txt` =
`C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok
tree=ok claims=13 files=6 spans=13 rev=ac496c7c…`. I did not re-run the full
`count-c2.py` (the receipt is committed at the freeze revision; the contract
scores C2 there); the tool-level arms above were re-run.

Drift arms, both pinned: r59 `drift_ok = p.returncode != 0` only
(`:251-261`); r60 requires verdict `SETTLEMENT_SCAN_FAIL`, a reason containing
`DRIFT_REASON = ":extra_keys="` (`count-c2.py:81`, used `:250-270`) and a
renamed r54-bytes-at-r53-path control that must scan OK.

## 4. Deltas against the landed 156/157 (`corpus/QUALITY.md:1590-1619`)

| # | Landed text | Verified | Draft handling |
|---|---|---|---|
| 1 | 156: “the r59 report and SCORECARD cited `c1-entering.txt`/`c2-entering.txt`” | No file under `.ufo/waves/round-59` at `7b86704d` or `ddfb12fb` contains `c1-entering`/`c2-entering` as an evidence pointer; the r59 w1 reports use them only as scratch-dir names (`--scratch …/c1-entering`, e.g. `Mo59Executor39.md:52`). The dead *paths* occur in `SCORECARD.md:2950-2951` at the entering revision only. | Draft names `SCORECARD.md:2950-2951` as the occurrence site and cites the lesson + spot-check for the routed defect; the “report” half is not repeated as a fact. |
| 2 | 156 sweep: `git grep -oE '(\.ufo/…|corpus/…)'` plus `cat-file -e` | Runs, but yields 329 tokens / 11 dead at entering: 6 truncation fragments, 3 pre-existing dead names, 2 real. A criterion that calls every hit a dead name mis-scores. | Draft anchors on backticked tokens and filters `[*{}…]|:[0-9]|/$`; measured 246/188/4. |
| 3 | 156 scope: “every evidence pointer cited by a report or a SCORECARD claim table” | Applied to the whole historical table it fails on pre-existing names unrelated to r59 (`.ufo/reports/round-12/mori.md`, `.ufo/state`, absent at `7b86704d` and `ddfb12fb`). | Draft scopes to the round's reports and the rows it adds or re-points, and says pre-existing names are recorded, not re-pointed. |
| 4 | 157: “receipt `evidence/control-c2-do-nothing.txt` records the class at the entering revision” | That receipt is `C2=unmet selftest=bad … failed=entry,pins,rows,selftest,tool_absent,trees,trees_set` — no `grammar:` token. The class is recorded in `SCORECARD.md:2951` (r59 C2 row, “orphaned `grammar:` reasons”) and Mo59Critic22 D3. | Draft cites S561/Mo59Critic22 D3 and the decertified row, not the receipt, for the class. |
| 5 | 157: “scored the r60 hostile tree `h02` met (grammar orphaned)” | The r59 *tree arm* compares `eval_entry`'s own `ok` against `expect.txt` and would reject `h02` correctly; the orphan bites the *real-entry* arm (`entry_ok` whitelist). | Draft states the mechanism precisely: `eval_entry ok=False` + whitelist ⇒ `entry_ok=True` ⇒ `met`. |
| 6 | 157 requirement phrasing: “a quoted-claim set must cover distinct byte spans” | Distinctness alone is vacuous at tiny spans; the implemented bound is `MIN_SPAN = 8` and the counter requires `spans == claims`. | Draft folds the 8-byte floor and the blank-quote rejection into the clause. |

## 5. Findings for the L1 (reported, not edited)

1. **Landed 156/157 need the six corrections above** if they are to survive a
   round-60 falsifier. Items 1, 4 and 5 are false-or-imprecise citations;
   items 2 and 3 make the criterion either noisy or unsatisfiable as written;
   item 6 is a weaker statement than the code it describes.
2. **Lesson row 1 carries the same unreproduced statement** (“r59 report +
   `SCORECARD.md` … cited”). `corpus/lessons/round-60.md:65-74` is the source
   of the error propagated into the landed 156 and into the SCORECARD
   `r60-correction:` wording; the verifiable fact is SCORECARD-only.
3. **The spot-check's third dead name is not reproducible.**
   `corpus/lessons/round-59-verifier-spotcheck.md:93` lists `controls.txt` as
   cited-but-dead; no file at `ddfb12fb` cites
   `.ufo/waves/round-59/evidence/controls.txt` (that path is absent). The
   count-c1 counter's `DEAD_NAMES` pair therefore matches what survives in
   committed bytes — but the spot-check's third name should be either
   substantiated or withdrawn.
4. **The historical SCORECARD has two backticked names that never resolve**
   (`.ufo/reports/round-12/mori.md` and `.ufo/state`) — not this round's defect
   and not the counter's arm; a future sweep criterion that covered the whole
   table would need a triage rule for them.

## 6. Limits

- Only the lane repo was read; no fleet or sibling repo access, no git writes,
  no worktrees, no commits (the demo loaded pinned blobs into scratch and
  never executed a repo-supplied tool blob as a counter would).
- I did not re-run `count-c2.py`/`count-c3.py`; C2/C3 rest on the committed
  at-freeze receipts and the contract's stated scoring at `ac496c7c`.
- The lane tip moved during the wave (`b3c25613` when read); every derivation
  above is pinned to a named revision (`ddfb12fb`, `7b86704d`, `b3c25613`,
  `ac496c7c`, `398d3225`) and the two counter runs name the revision in their
  output line.
- “Wrong content behind a resolving pointer” and “basename-only citation” are
  out of reach of the sweep, and both are stated in 156's Not-covered tail.

## 7. Artifacts

Nothing written outside this report and the scratch dir; scratch removed after
the evidence above was captured. Report path:
`.ufo/waves/round-60/w1/Mo60Scribe76.md`.

# W2 DiffHarmAudit — C2 differential re-run at ad0f047 and older-case harm ruling (seat MoriR30.DiffHarmAudit)

**Verdict: AGREE — no harm.** The re-run at `ad0f047` reproduces `evidence/c2-differential.txt` byte-for-byte
(the script's own stdout is identical; the receipt's trailing `exit: 0` line is the author's shell echo), and the
four new unpinned field values on `a2-02` and `a2-06` contradict no rule-text line. They implement the round-29
Judge11–13 `tool error` rulings, stay inside the A2 residual-fix class, and change no pinned field, verdict or exit.

## 1. What I ran (all read-only; no git/jj writes anywhere)

- `python3 -I -B .ufo/waves/round-30/c2-differential.py ad0f04745ced2194e58c22a0d6b38131bee3e230` from the lane
  root; exit 0, 7 s. The script reads committed bytes only (`git show`), writes only under a temp dir
  (`c2-differential.py:12,41,57`), so it cannot mutate the lane.
- Tip tool blob selftests: `python3 -I -B <scratch>/tool-tip.py --selftest --cases tools/fixtures/mori-oom-killers/<f>`
  for all five files (tool blob = `git show ad0f047:tools/mori-oom-killers.py`).
- Blob/lineage checks and `git rev-parse`, `git log`, `git diff --stat`, `git status --porcelain`,
  `git merge-base --is-ancestor` (read-only commands only).

## 2. Reproduction vs receipt

Receipt `evidence/c2-differential.txt` (9 lines): header says it was taken at `7aa7748` (`:1-2`); body `:3-8`
(5 changed-case lines + summary), `:9` `exit: 0`.

My rerun at `ad0f047` printed the same 5 changed lines and the same summary; `diff` of receipt lines 3–9 against my
output shows the only difference is the receipt's `exit: 0` line, which the script never prints (it is the wrapper's
`echo "exit: $?"` in the receipt procedure). Script stdout is byte-identical:

```
inputs=126 changed=5 older_changed=2 older_disallowed=0 acted_lost=0
```

Both older changed cases are exactly the assigned two, with identical deltas at both revs:

- `cases-a2.json a2-02-earlyoom-activestate-deactivating` ActiveState=deactivating, exit 2->2:
  `dryrun_send_lines: null -> 0; grammar: "unverified" -> "verified-1.9.0"; process_group_lines: null -> 0;
  version: null -> "1.9.0"`.
- `cases-a2.json a2-06-inactive-earlier-invocation-sends-acted` ActiveState=inactive, exit 1->1: same four deltas.
- The other three changes are `cases-a2-r29.json` cases (out of this seat's scope; all in the allowed class:
  inactive/failed/inactive; the one extra delta there is `earlier_invocation_send_lines: 1 -> 0` on
  `r29-a2-10-failed-stamped-positive` with verdict/exit unchanged).

## 3. Provenance — nothing moved under the receipt

- Differential script blob is `7550e3825db4754f4857c4318f45694b03cb9a3c` at BOTH `7aa7748` and `ad0f047`
  (`git rev-parse <rev>:.ufo/waves/round-30/c2-differential.py`); working tree clean for it
  (`git diff --stat` on the path: empty). Same bytes produced receipt and rerun.
- Older case-file blobs identical at `58b6168` / `7aa7748` / `ad0f047`: `cases.json` `5b4dcee7`,
  `cases-supplementary.json` `d7c9040b`, `cases-a2.json` `7ba553d4`; `cases-a2-r29.json` `cc309d8e` at all three.
  `cases-a2-r30.json` `a05863cc` at `7aa7748` and `ad0f047` (absent at `58b6168`, pre-freeze `db1ec46`, as expected).
- `tools/mori-oom-killers.py` is touched by exactly one commit in `58b6168..ad0f047`: `7aa7748` (`git log` on the
  path). No tool drift after the receipt commit.
- Lane HEAD has since advanced to `713be294` (wave-2 dispatch commit); `ad0f047` is its ancestor
  (`git merge-base --is-ancestor` → true). My rerun used the exact assigned rev.

## 4. The two cases: the four fields are indeed unpinned; inputs are readable

From `tools/fixtures/mori-oom-killers/cases-a2.json` at tip (ids at `:149` and `:677`), parsed from committed bytes:

- `a2-02…deactivating` expect pins only `verdict=KILLERS_UNKNOWN`, `exit=2`, `earlyoom.state=unavailable`,
  `oomd.state=active`, `oomd.notices_this_boot=0`. Journal non-null with 1 `earlyoom <version>` line, 0 dry-run,
  0 process-group, 0 send lines; show carries `ActiveState=deactivating`.
- `a2-06…sends-acted` expect pins `verdict=KILLER_ACTED`, `exit=1`, `earlyoom.state=inactive`,
  `earlyoom.actions=null`, `earlyoom.earlier_invocation_send_lines=3`, oomd fields. Journal non-null with 2 version
  lines, 3 send lines, 0 dry-run, 0 group lines; show carries `ActiveState=inactive`.

None of `version`, `grammar`, `dryrun_send_lines`, `process_group_lines` is pinned by either case — confirmed.

## 5. Field-by-field rule-text ruling

- **`version: null -> "1.9.0"`** — Round-26 contract `:82` (in the writers' extract, `rule-text.md`): the grammar
  maps `` `earlyoom <version>` `` → version, "the first line of an invocation". The rule text conditions nothing on
  ActiveState for this mapping, and both journals are readable and carry version lines. The OLD null was the judged
  defect: round-29 Judge12 ruled `earlyoom.version: expected "1.9.0", tool null` a **tool error** citing
  round-26 `:82` (`.ufo/waves/round-29/w2/Judge12.md:19`). New value agrees with rule text as judged. Not a harm.
- **`grammar: "unverified" -> "verified-1.9.0"`** — Output enum round-26 `:91` (`verified-1.9.0` or `unverified`).
  Judge12 ruled the old `unverified` a tool error citing `:91` (`Judge12.md:20`). The only verdict rule touching
  grammar gates ACTIVE units ("earlyoom active and grammar unverified", round-26 `:99-100`); neither case is active.
  New value agrees. Not a harm.
- **`dryrun_send_lines: null -> 0`** — A6 (round-26 `:167-168`; rule-table row A2-04, round-27 `contract.md:53`):
  send lines under a dry-run invocation go to this counter; neither journal contains any dry-run line, so the count
  of matched log lines is 0. The counter is a count over the (available) journal text, not an action count. 0 is the
  honest, rule-conformant value; the old null corresponded to the pre-fix bail-out. Not a harm.
- **`process_group_lines: null -> 0`** — A5 (round-26 `:164-165`; row A2-03, round-27 `:52`): "`killing whole
  process group ` lines are counted in `earlyoom.process_group_lines`; every count is a count of earlyoom log
  lines". Neither journal has such a line → 0. Not a harm.
- **"never zero counts" (round-26 `:102-104`) does not reach these fields.** The clause reads: "An inactive or
  absent killer reports `actions: null` (unavailable), never zero counts". It binds the `actions` object of the
  output schema (round-26 `:90`: sigterm, sigkill, escalations, kill_failed, low_memory_warnings).
  `dryrun_send_lines`/`process_group_lines` are not members of `actions`; they are A5/A6 diagnostic counters, and
  the rationale (you may not claim zero from a read you could not perform) fails here because the journals ARE
  available — the tool looked and counted 0. The clause's actual object stayed intact: `earlyoom.actions` is not in
  either delta (unchanged), and `a2-06` pins `actions=null`, which passes at tip (selftest below). Not a harm.
- **A2b (round-26 `:162-163`; `rule-text.md:71-72`) is not contradicted.** A2b mandates `state=unavailable` and
  `KILLERS_UNKNOWN` for a non-steady ActiveState; a2-02 keeps exit 2/KILLERS_UNKNOWN and is pinned `state=unavailable`,
  passing at tip. A2b says nothing about journal-derived version/grammar/counters. Precedence is already settled in
  the round-30 wave record: rule 2 ("no positive evidence, and any of…") governs only the evidence-free case, and
  A2-06/A2-09 create ACTED for not-active units (`.ufo/waves/round-30/w1/ReviewJudgeRulings.md:149-155`), which is
  exactly why `a2-06` stays `KILLER_ACTED` with `earlier_invocation_send_lines=3`.
- **Mechanism check** (`evidence/fix-tool.diff`, 83 lines, committed at `7aa7748`): the old code bailed for a
  non-current invocation — "No current invocation: no version, no thresholds, no action counts" with
  `version = None; grammar = GRAMMAR_UNVERIFIED` (diff lines 45–49); the fix keeps "The actions object is
  unavailable, but a retained log boundary can still supply the version and independent line counters"
  (diff lines 50–51). The four deltas are precisely this un-bail; `actions` stays unavailable.

## 6. Binding harm tests, all pass at tip

Contract amendment A2 "Residual fix bound" (round-30 `contract.md:188-190`): changes allowed only where the show
text is readable and `ActiveState` is not `active`; any `KILLER_ACTED` → other verdict is a harm; receipt is
`evidence/c2-differential.txt`.

- Class: a2-02 `deactivating`, a2-06 `inactive` — both readable, both non-active. Counter says `older_disallowed=0`.
- Verdicts: `acted_lost=0`; a2-02 exit 2->2, a2-06 exit 1->1.
- Conditions 1–2 preserved (the judging clause round-30 `contract.md:97-101`: tool-only change, never turn an older
  `KILLER_ACTED`). Tip tool selftests I ran: `cases.json PASS 32/32`, `cases-supplementary.json PASS 32/32`,
  `cases-a2.json PASS 30/30` (contract `:62-63`), `cases-a2-r29.json PASS 24/24` (condition 1), `cases-a2-r30.json
  PASS 8/8` — the freeze cases are untouched by the fix (also attested "r30 PASS 8/8 before (base tool) and after",
  commit `7aa7748` message).
- The receipt path named in the bound exists and now also holds at the measured tip, not only at the fix commit.

## 7. Ruling

**Not a harm.** The two older-case output changes (i) fall wholly inside the A2-permitted class, (ii) alter no
pinned field, verdict or exit, (iii) match rule text on every changed value — indeed the version/grammar changes
are the implementation of round-29's judged `tool error` rulings (Judge11–13), and the counter changes print correct
A5/A6 log-line counts of available journals — and (iv) leave the "never zero counts" clause's actual object
(`actions`) null exactly as the rule requires. If anything, the pre-fix nulls were the rule deviation; the fix
removes a contradiction rather than creating one. C2's author already reports C2 unmet for the unrelated gate
reason (`blind_violations=1`, `evidence/c2-after.txt`); this audit adds no further defect on the differential axis.

## 8. Residual risk and verification gaps

- `a2-02`'s post-fix `earlyoom.actions` value was not separately printed by me; it is unpinned and provably
  unchanged (absent from the delta), so the harm question is unaffected. [INFERENCE: null, since the fix keeps
  actions unavailable for non-steady states — fix-tool.diff:12,50.]
- Rule line numbers `:82`/`:91` are taken from Judge12's citations (`Judge12.md:19-20`); I verified the bullets'
  content inside my read of round-26 `contract.md:58-135` but did not recount the exact printed line numbers.
  [INFERENCE on exact numbers, not on content.]
- The bound's phrase "over the 94 older cases" (round-30 `contract.md:189`) undercounts what the receipt covers:
  126 inputs = the 94 cases of the three round-≤28 files plus the 24 `cases-a2-r29.json` cases. The receipt is a
  superset of the bound and every changed case passes the class test, so this is a wording mismatch, not a
  narrowing. Disclosure only.
- I did not re-derive the round-29 Judge11–13 rulings themselves (out of scope; other seats own them); I rely on
  them only as the recorded adjudication that the old null/unverified values were tool errors.

## 9. Tooling record

No tools installed or updated (python3 and git present sufficed); no pacman transactions; no background jobs; no
subagents. Scratch artifacts under `/fast/scratch/hyaku/mori-r30-w2/DiffHarmAudit/` (`tool-tip.py`,
`cases-a2-tip.json`, `fix-tool.diff`, `rerun-tip.txt`, `receipt-body.txt`). No host identifiers, unit names of this
host's session, or configuration values appear in this report; fixture text quoted is synthetic and limited to
`ActiveState=` lines and count summaries.

# mori round 30 — claim contract (attempt 1, L1 MoriR30)

Entering tip `58b61681a0e3f3b821a17d38a4e713ccd9921615` (round-29 verifier spot-check; round 29 closed
`rejected-honest-stop`, MANIFEST `rounds[483]`). Written before any round-30 implementation, case draft or source
row. Targets, not results. A declared claim is never withdrawn or narrowed; a miss is reported as a miss.

## Why these two claims

- Lowest-scoring active axes are depth, freshness and calibration (5 each, `SCORECARD.md:12-14`). Calibration was
  claimed in round 29, freshness in round 28; depth was last counted in round 12 (round 27's depth move closed under a
  rejected round). C1 works depth.
- C2 is the round-29 closure's routed R4, R5 and R6 (`corpus/lessons/round-29-verifier-spotcheck.md:160-165`): three
  frozen A2-10 cases still fail (judged tool errors, Judge11–13), the blindness gate flags 20 false positives, and the
  disputed active-unit shape has no frozen case of its own. It works operability (7).
- Causally separable: C1 touches only `corpus/knowledge/earlyoom-invocation-scope-r30.md`, `SKILL.md` rows tagged
  `Round30`, `corpus/SOURCES.md` rows S156+, their excerpts under `corpus/evidence/sources-r30/` and its counter; its
  decision-table rows cite only case ids that exist at the entering tip and pass there. C2 touches only
  `tools/mori-oom-killers.py`, the new `tools/fixtures/mori-oom-killers/cases-a2-r30.json`, the round-30 blindness gate
  and its counter. Neither counter reads the other claim's files.
- Sourced claim: C1. Its entry cites rows opened this round; each row's `## Gate` line in `corpus/lessons/round-30.md`
  carries URL, access time, sha256 and located quote, and a committed excerpt holds the quoted lines.

## C1 — depth (score 5, tied lowest): how the oom-killers reader scopes an earlyoom invocation, as a decision table

Statement: at the landed tip, `count-c1.sh <rev>` prints `C1=met`, exit 0, where all of the following hold at `<rev>`:

1. `corpus/knowledge/earlyoom-invocation-scope-r30.md` exists with `source:`, `verified-at:` and `recheck:` lines.
2. It holds one Markdown table whose header row contains the cells `shape`, `verdict`, `fields`, `case` and
   `sources`, with at least 8 data rows. In each row: `case` holds one backticked case id; `verdict` is one of
   `KILLER_ACTED`, `KILLERS_QUIET`, `KILLERS_UNKNOWN`; `fields` holds one or more `<dotted.path>=<json value>` items;
   `sources` holds one or more `S###` ids that exist as rows of `corpus/SOURCES.md` at `<rev>`.
3. Every row's case id exists in exactly one of `cases.json`, `cases-supplementary.json`, `cases-a2.json` under
   `tools/fixtures/mori-oom-killers/` with its blob equal to the entering-tip blob (the round-29 file is excluded:
   three of its cases fail at the entering tip); the case's `expect.verdict` equals the row's verdict and every
   `fields` item equals the case's `expect.fields` value; and `tools/mori-oom-killers.py` at `<rev>`, run as
   `python3 -I -B <tool> --inputs <case inputs>` on a temporary copy, prints that verdict and those field values.
4. Rows cite at least 3 distinct ids S156 or higher, and at least 3 rows cite such an id. For each such id: the row
   exists in `corpus/SOURCES.md`, `corpus/lessons/round-30.md` holds a Gate line starting `| S### |` with an `admit`
   decision, a 64-hex sha256 and at least one located quote `` `:L` `` or `` `:L-M` `` followed by a double-quoted
   string; and `corpus/evidence/sources-r30/S###.txt` exists, names the same sha256 and URL in its header, and carries
   the quoted text verbatim (whitespace runs collapsed) within the excerpt lines it labels L..M.
5. `SKILL.md` holds at least 3 table rows containing `Round30` and the entry's path.

Counting command (committed bytes only; exit 0 met, 1 unmet, 2 bad revision or missing input):

```sh
bash /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-30/count-c1.sh <lane-rev>
```

Committed before the entry, the rows or any excerpt. Before at `58b61681`: entry absent, `C1=unmet`, exit 1
(`evidence/c1-before.txt`). Declared after: `C1=met`, exit 0. A trivial baseline (an empty or prose-only entry, a
row whose verdict the tool does not print, a quote not in its excerpt) fails conditions 2–4. Uncounted residual, read
by a wave-2 non-author: whether each row's shape text describes its case and whether each cited quote supports it.
Score policy: depth stays 5 unless an admitted closure states the move.

## C2 — operability (score 7): the round-29 residual cases pass, the disputed shape is pinned blind, the gate is fixed

Statement: at the landed tip, `count-c2.sh <rev>` prints `C2=met`, exit 0, where all of the following hold:

1. **Residual (R4).** `--selftest --cases tools/fixtures/mori-oom-killers/cases-a2-r29.json` at `<rev>` prints
   `PASS 24/24`; the file's blob equals its freeze blob at `d6d5cb0a` (before: `FAIL 21/24` at `58b61681`).
2. **Older pins held.** `cases.json` `PASS 32/32`, `cases-supplementary.json` `PASS 32/32`, `cases-a2.json`
   `PASS 30/30`, each blob equal to its `58b61681` blob.
3. **Disputed shape pinned (R6).** `tools/fixtures/mori-oom-killers/cases-a2-r30.json` exists; its blob equals the blob
   at the first lane commit that added it (the freeze commit); `--selftest` on it prints `PASS N/N`; it holds at least
   6 cases, from at least 3 distinct authors of the fixed writer set `CaseR30a`–`CaseR30d`; provenance: every case
   equals (canonical JSON, keys sorted) a case in the first fenced JSON array of its author's report
   `.ufo/waves/round-30/w1/<author>.md` at `<rev>`, and no case of those reports is missing (`unselected=0`); at least 6
   cases have the shape: `earlyoom_show` with `ActiveState=active` and `ActiveEnterTimestampMonotonic` absent or `0`;
   a journal holding at least two version lines (MESSAGE, leading whitespace stripped, starting `earlyoom `), at
   least one send line (starting `sending SIGTERM to process `, `sending SIGKILL to process ` or
   `escalating to SIGKILL after `) before the last version line in list order, and no send line after it; and each
   such case pins `verdict` (string), `exit`, `earlyoom.actions.sigterm` and
   `earlyoom.earlier_invocation_send_lines` (integers).
4. **Gate fixed (R5).** `.ufo/waves/round-30/check-blind-wave.sh` is committed before the freeze commit; its
   `--selftest` prints `PASS` (it reports 0 on the round-29 writer wave at `d6d5cb0a` whose 20 hits were adjudicated
   false positives, and it reports a violation for each planted leak class: tool line citation, tool output marker,
   forbidden path in a files-opened list, missing files-opened list); and run at the freeze commit on
   `.ufo/waves/round-30/w1` with writer regex `^CaseR30[a-d]\.md$` it prints `blind_violations=0`.

Writers: four executor seats `CaseR30a`–`CaseR30d`, two cases each, who read only
`.ufo/waves/round-30/rule-text.md` (a verbatim extract of round-26 contract `:58-110` and `:152-190` and round-27
contract `:47-58`, committed with this contract) and public upstream earlyoom and systemd sources; they open no other
lane file — no tool, fixture, contract, lesson, LOG, SCORECARD, SKILL, knowledge entry or other report. Pinned fields
are limited to `verdict`, `exit`, `earlyoom.state`, `earlyoom.scope_complete`, `earlyoom.actions.sigterm`,
`earlyoom.actions.sigkill` and `earlyoom.earlier_invocation_send_lines`.

Counting command:

```sh
bash /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-30/count-c2.sh <lane-rev>
```

Committed before the case file. Before at `58b61681`: residual `FAIL 21/24`, new file absent, `C2=unmet`, exit 1
(`evidence/c2-before.txt`). Declared after: `C2=met`, exit 0.

Mismatch judging (carried from round-28 amendment A2): a non-author judge seat reads only the rule text, the case and
the tool's output for that case and rules `tool error`, `case error` or `unclear text`. On `tool error` the L1 may
change the tool, never a case file; the change must keep conditions 1–2. Any `case error` or `unclear text` is a C2
miss, reported as one. A case is never dropped, renamed or re-tagged after the freeze commit. The residual fix (1)
follows the round-29 rulings Judge11–13 (`tool error`); it may not turn any `KILLER_ACTED` of an older file into
another verdict.

## Held, not claimed

Freshness 5, calibration 5, coverage 6, adjacency 6 observed. No retirement, waiver, exploratory claim or promotion.
No-harm check: lane retention scan unallowlisted metric at the landed tip must not exceed its value at `58b61681`
(`python3 -I -B tools/mori-retention-gate.py scan --repo <lane> --rev <rev> --policy
.ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json`).

## Routed hygiene (round-29 closure §7; never a counted claim)

- R1: this round's `LOG.md` and lesson name the tip receipts `evidence/tip-c1.txt`, `tip-c2.txt` and
  `tip-retention.txt` before the receipts-only batch; `.ufo/waves/round-28/check-tip-receipts.sh <tip> 30` must print
  `tip_receipts=met`.
- R2, R3: appended corrections (kill.h reject reason; S154/S155 word-count labels) in the round-30 lesson and
  `corpus/SOURCES.md`, never edits of earlier text.
- R6 second half: the A2a limit for the disputed shape stated in the C1 entry and SKILL.
- R7: PROVINCE stale statements and the unqualified `SKILL.md:661` citation fixed against observed repo state.
- QUALITY rows for each routed defect, each with a check shown able to fail.

## Amendment A1 (round 30, before the C1 counter lands, before any entry, row or excerpt is committed; wave-1 CriticC1Design F1–F18)

Every change makes C1 harder to meet, removes a format ambiguity, or makes it separable from C2; nothing is narrowed.

- **2a distinct (F2):** case ids pairwise distinct; `shape` cells non-empty and pairwise distinct; rows span at least
  2 verdicts.
- **2b scope content (F1):** every row's `fields` includes `earlyoom.scope_complete` or
  `earlyoom.earlier_invocation_send_lines`; at least 4 rows cite a case whose `earlyoom_journal` holds at least two
  version lines (MESSAGE, leading whitespace stripped, starting `earlyoom `).
- **2c syntax (F13–F15):** the table is the first one whose header row contains the five cells; `fields` items are
  backticked `` `path=<json>` `` separated by `, `; the verdict cell may be backticked; values compare typed (a bool
  equals only a bool, numbers compare numerically, strings exactly). Example row:
  `` | bounded scope, send at the stamp | `KILLER_ACTED` | `earlyoom.scope_complete=true`, `earlyoom.actions.sigterm=1` | `c03-…` | S156 | ``.
- **3a separability (F10, F12):** the tool run uses `git show 58b61681:tools/mori-oom-killers.py` (the entering-tip
  blob), not the tool at `<rev>`; the printed exit is compared with `expect.exit`. A case id may occur in more than
  one eligible file only when every copy's `inputs` and `expect` are identical.
- **4a novelty (F4):** each S156+ id's Gate/excerpt URL appears in no `corpus/SOURCES.md` row with id below S156, and
  its excerpt `accessed:` is not earlier than the contract commit time (2026-10-22T21:08:28Z).
- **4b binding (F8, F9):** the excerpt's URL and sha256 equal those of an `admit` line for that id under the lesson's
  `## Gate` heading; the SOURCES row for the id contains that URL. One URL per S### id.
- **4c quote grammar (F5–F7):** a located quote is `` `[file]:L` `` or `` `[file]:L-M` ``, with `(N words)` before or
  after the double-quoted string; inside the string only `\"`, `\|` and `\\` are unescaped, everything else is literal;
  `wc -w` of the quote is at most 25 and equals N; each counted id has at least one quote of 3 or more words found in
  its excerpt.
- **5a SKILL rows (F11, F16):** count table rows under a heading starting `## Round30` that contain
  `earlyoom-invocation-scope-r30.md` and name a case id of the decision table; at least 3.
- **1a header (F18):** `source:` names at least one S156+ id cited by the table.
- **Provenance (F17):** the counter is run from its commit blob (`git show <counter-commit>:.ufo/waves/round-30/count-c1.sh`);
  it reads only the lane repository and ignores any repo-path environment override; the counter commit is an ancestor
  of the first commit that adds the entry or any `corpus/evidence/sources-r30/` excerpt.
- **Separability:** C2 adds no SOURCES rows.
- **Residual, uncounted (F3), read by wave 2 non-authors:** re-fetch every S156+ URL, recompute sha256 of the full
  bytes and diff each excerpt line against the fetched line of the same number; any mismatch is reported as a C1
  defect.

## Amendment A2 (round 30, before the C2 counter, the gate and the case file land, and before the L1 opens any writer report; wave-1 CriticC2Design, CriticSizing, CriticHarmScreen, ReviewRuleTextShape, ReviewC1Reachability)

Every change makes C2 harder to meet, fixes a counter defect, or states a miss condition in advance; nothing is
narrowed. C1 parse clarifications (ReviewC1Reachability F3) close the list.

- **Gate is exercised by the counter, not trusted (CriticC2Design G1, G2):** besides the gate's own `--selftest`
  printing `PASS`, the counter builds its own planted writer reports (one per leak class a–d of C2.4) in a temporary git
  repository and requires the gate to exit 1 on each, and the gate run at the freeze commit must print
  `scanned=<k>` with k equal to the number of distinct authors in `cases-a2-r30.json`, and `blind_violations=0`.
- **Allowlist, not denylist (G3, G4):** a writer's files-opened entry passes only if it is the lane path of
  `.ufo/waves/round-30/rule-text.md`, a path under the writer's own scratch dir, or an `https://` URL whose host and
  path start with one of `raw.githubusercontent.com/rfjakob/earlyoom/`, `github.com/rfjakob/earlyoom/`,
  `raw.githubusercontent.com/systemd/systemd/`, `github.com/systemd/systemd/`, `www.freedesktop.org/software/systemd/`;
  anything else is a violation. On the round-29 writer wave (whose brief allowed contract and fixture reads) the gate's
  self-test compares against an exact expected set of (file, rule) reports, documented in the gate, and none of the
  20 adjudicated round-29 false positives may appear in it.
- **Freeze identification (F1):** the freeze commit is the oldest commit (`git log --reverse --diff-filter=A`) adding
  `cases-a2-r30.json`; the file must never be deleted or modified after it (`git log --format=%H <freeze>..<rev> --
  <file>` empty).
- **Tool run order (F2):** the first tool runs on the frozen file use the entering-tip tool blob, then the changed
  tool; both receipts are committed (`evidence/c2-freeze-selftest-base.txt`, `evidence/c2-freeze-selftest-fixed.txt`).
  No tool change may alter the verdict of any shape case of `cases-a2-r30.json` (the round-29 closure's ruling on the
  disputed shape stands: CriticHarmScreen).
- **Shape tightened (S1):** a shape case additionally holds no `dryrun mode enabled` line, every journal record has a
  numeric `__MONOTONIC_TIMESTAMP`, timestamps are non-decreasing in list order, `LoadState=loaded`, and `oomd_notices`
  is 0.
- **Undecided pins (W1, D1):** a writer report stating that a mandatory pin (`earlyoom.actions.sigterm`,
  `earlyoom.earlier_invocation_send_lines`) is not decided by the text counts as `unclear text` → C2 miss. A case
  pinning the literal reading (`KILLER_ACTED` from the pre-restart sends) that the tool does not print is a C2 miss;
  it is never answered by a tool change (that would reverse condition 1's round-29 pins).
- **Judging (CriticSizing):** every mismatch gets two independent judge seats; a split counts as `unclear text`.
- **Residual fix bound (ReviewJudgeRulings, CriticSizing):** the full-output differential of the changed tool against
  the entering-tip tool over the 94 older cases may change output only for cases whose earlyoom show text is readable
  and whose `ActiveState` is not `active`; any `KILLER_ACTED` → other verdict anywhere is a harm. Receipt:
  `evidence/c2-differential.txt`.
- **Authorship (CriticSizing A2):** a case's author is the writer report in which it is found; its `author` key must
  name that seat (`CaseR30x` or `MoriR30.CaseR30x`).
- **Counters from blobs (CriticSizing A3):** both counters and the gate are run from their committed blobs
  (`bash <(git show <rev>:.ufo/waves/round-30/count-cN.sh) <rev>`); the gate at the freeze commit is the freeze commit's
  blob.
- **Disclosed, uncounted:** the rule text does not decide the disputed shape uniquely (ReviewRuleTextShape F1–F2: a
  literal scope reading gives `KILLER_ACTED`); the counted after-value is agreement of four blind writers and the tool,
  not a proof that the text decides the shape. Judge02's round-29 `unclear text` pin stays inside the `PASS 24/24`
  tally and is named in the report.
- **C1 parse clarifications:** excerpt body line = digits, TAB, text (split on the first tab); excerpts may be sparse,
  but every line L..M of a counted quote must be present; whitespace collapse = runs of spaces and tabs to one space,
  then trim, applied to the quote and to excerpt lines L..M joined by one space; the Gate URL is the first `https?://`
  token of the source cell; the Gate sha256 is the 64-hex inside backticks in the sha256 cell; a Gate line is a table
  line under `## Gate` (until the next `## ` heading) whose first cell is `S###`.

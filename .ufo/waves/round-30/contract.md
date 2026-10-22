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

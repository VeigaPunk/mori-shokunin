# Review C1 reachability and vacuity — MoriR30.ReviewC1Reachability (wave 1)

Date: 2026-10-22. Scope: attack C1 in `.ufo/waves/round-30/contract.md` for reachability and
vacuity before data, per the wave-1 assignment: (1) does the older-case base support >=8 rows,
(2) can a trivial entry meet conditions 2-5, (3) do condition 4's Gate-line and excerpt formats
parse unambiguously. Entering tip `58b61681a0e3f3b821a17d38a4e713ccd9921615`; lane HEAD at
review time `e936482a6070db40049bff46f7da4754b15d41af` (declaration commit: SCORECARD, LOG,
wave-1 payload only — no counter, no entry, no fixture change; `git show --stat e936482a`).

Method: read-only git in the lane; `python3 -I -B tools/mori-oom-killers.py --selftest --cases
<file>` on the three older case files; four `--inputs` spot-runs with the tool and each inputs
object copied to /tmp; JSON facts via a throwaway python reader; text inspection of round-29
Gate lines and SOURCES rows. No lsp device is available in this session's tool inventory, so
every check below is textual or executional, not LSP-grade semantic proof.

## Findings by severity

### F3 — HIGH: condition 4's Gate-line and excerpt formats do not yet admit an unambiguous parse

No in-repo precedent exists: no file under `corpus/` carries the excerpt `accessed:` header
(grep across corpus: zero matches) and `corpus/evidence/` holds no `S###.txt` excerpt files
from earlier rounds. Seat drafts and BuildCountC1's parser must converge on prose alone, in
parallel, today. Concrete ambiguities:

1. Quote escaping undefined. Verbatim earlyoom/systemd code quotes contain double quotes; the
   round-29 precedent stores them escaped inside the quoted cell, e.g. the `xsprintf(...`
   quote on `corpus/lessons/round-29.md:57` renders `\"` sequences. Condition 4 says only
   "a double-quoted string" (`contract.md:39`) matched against "the quoted text verbatim
   (whitespace runs collapsed)" (`contract.md:41`). Whether the excerpt comparison unescapes
   `\"` or compares raw is unpinned; a parser ending the string at the first unescaped `"`
   truncates such quotes, and pass/fail flips by implementation choice.
2. Whitespace collapse is undefined beyond "runs collapsed": leading/trailing strip and
   tab-vs-space handling are unstated (`contract.md:41`).
3. Single-line quotes have no header counterpart. Condition 4 admits a located quote `` `:L` ``
   (`contract.md:39`), but the excerpt header format only defines `lines: <L>-<M>`. Whether a
   `:42` quote needs `lines: 42` or `lines: 42-42` is unpinned.
4. Sparse vs complete excerpt. The wave format block says the excerpt covers "at least the
   quoted lines" (sparse listing allowed); condition 4's "within the excerpt lines it labels
   L..M" (`contract.md:41`) reads as if every line in the labeled range is present. One
   reading makes a quoted-lines-only file pass, the other fails it.
5. `<line number><TAB><text verbatim>` needs split-on-first-tab: source lines may contain
   tabs (C alignment, Makefiles). Also unstated: whether blank source lines are listed as an
   empty text after the tab or omitted.
6. Cell decoration precedent. Round-29 Gate lines carry parentheticals inside cells: a URL
   cell with `(with sd-journal.c, ... at the same tag)` (`corpus/lessons/round-29.md:57`) and
   an access-time cell with `(grep only; URL not fetched)` (`corpus/lessons/round-29.md:58`).
   Condition 4 requires the excerpt header to name "the same sha256 and URL"
   (`contract.md:40`); equality-vs-substring is unpinned, so a decorated Gate cell against a
   bare `url:` header fails naive equality, while a loose parser accepts annotated access
   times a strict ISO check would reject.
7. Multiple quotes per Gate cell (two on `corpus/lessons/round-29.md:55`) plus one `lines:`
   header per excerpt file: a single labeled range spanning disjoint quote regions also
   "labels" unquoted lines. The counter must say whether only quoted lines are matched inside
   the range.
8. Two binding specs diverge: condition 4 (`contract.md:37-41`) requires admit + 64-hex sha +
   located quote + quoted string, with no `(N words)` label and no cell layout; the wave
   format block pins both extra properties. A seat and the counter can each follow a different
   spec and no check notices (feeds F5).

Why HIGH: each item mechanically flips an admit or excerpt-match outcome. A false unmet sinks
the declared claim at counting time; a false met (truncated-quote or sparse-excerpt acceptance)
inflates the depth claim. Mitigation: BuildCountC1 should publish its exact normalization
(escape handling, collapse rule, first-tab split, `lines:` form) inside the counter or a
sibling fixture, and every seat writing Gate lines or excerpts should copy that file's behavior.

### F2 — MEDIUM: vacuity — conditions 2-5 are meetable by a mechanical-copy entry with no depth

A trivial entry can satisfy the letter of C1:

- Pick 8 case ids unique across the three older files (36 of 65 ids qualify; see F4), copy
  each `expect.verdict` into `verdict` and any subset of `expect.fields` into `fields`
  (condition 3 demands equality with `expect`, `contract.md:33-35`, so copying is the
  compliant move and involves zero judgment).
- Write the identical `shape` string in all 8 rows: no condition requires distinct shapes or
  that the shape text describe the case; the contract itself concedes this residual
  (`contract.md:52`: "whether each row's shape text describes its case and whether each cited
  quote supports it" is uncounted).
- Cite S156, S157, S158 across the rows and fetch any three fetchable public pages: no
  condition ties a source's topic to earlyoom, systemd, or any row's scope question — only
  existence as a SOURCES row, a Gate line, and an excerpt carrying the quote
  (`contract.md:37-41`).

What the counter cannot see (each item is a wave-2 reader obligation):

a. Whether `shape` texts describe their cases and are distinct across rows.
b. Whether the table answers the C1 question (invocation scoping) at all: all 8 rows may
   legally come from `cases-a2.json`, so the table can avoid every base-grammar shape.
c. Source topicality: the S156+ rows need not relate to the entry's subject.
d. Whether any cited quote supports the row's verdict (conceded, `contract.md:52`).
e. sha256 and URL authenticity: counting is committed-bytes-only (`contract.md:44`), so the
   counter cannot refetch; wave-2 must, comparing against committed excerpt bytes because the
   live file may have rotated.
f. `(N words)` labels: absent from condition 4 entirely; round-29's routed defects R2/R3 were
   exactly wrong word-count labels on S154/S155 (`corpus/lessons/round-29-verifier-spotcheck.md:152-166`,
   corrected labels at `corpus/SOURCES.md:160-161`). The recurrence channel stays open.
g. Routed R6 second half: "the A2a limit for the disputed shape stated in the C1 entry and
   SKILL" (`contract.md:118`) has no counted condition; a met C1 can omit the A2a limit.
h. `source:` / `verified-at:` / `recheck:` line content: condition 1 (`contract.md:27`) checks
   existence only; empty or nonsense values pass.
i. SKILL.md rows: `Round30` plus the entry path in a row is greppable filler; substance is
   unchecked by condition 5 (`contract.md:43`).
j. If the entry holds more than one Markdown table, which table is "the" counted table
   (condition 2, `contract.md:28-31`) is implementation-defined.

Severity rationale: MEDIUM, not HIGH — the mechanical floor is the counter's legitimate job,
the contract openly declares the residual instead of hiding it, and routed hygiene (R6, R7,
QUALITY rows) partially covers the gap; but a reader who treats `C1=met` as depth would be
wrong, and the wave-2 checklist below is the actual depth audit.

### F4 — LOW: the exactly-one-file id trap (counter sees it; drafters may not)

Condition 3 requires each row's case id to exist in exactly one of the three older files
(`contract.md:32-33`). Of the 65 distinct ids, 29 appear in both `cases.json` and
`cases-supplementary.json` (the `c01`-`c12`, `c13`-`c18`, `c20`-`c23`, `c25`-`c27`,
`c29`-`c31` families). Rows citing them are void regardless of everything else. Eligible
pool: 36 ids — `c19-version-line-only`, `c24-nearmiss-kill-failed-without-colon`,
`c28-oomd-active-quiet` (cases.json only); `c33-differing-thresholds-mem-and-swap`,
`c34-escalation-only-incomplete-scope`, `c35-malformed-monotonic-timestamp` (supplementary
only); all 30 `a2-*` ids. Messaged to DraftEntryC1. Independently confirmed by DraftEntryC1
(peer message, 2026-10-22): their own set comparison over the three case arrays reproduces the
same 29-id duplicate set and 36-id eligible pool, and the entry draft's row candidates now use
eligible ids only (its prose cites `c02`/`c03`/`c04` outside the table, which condition 3 does
not reach — table rows are the counted surface).

### F5 — LOW: word-count label drift channel (R2/R3 class)

The `(N words)` label is required by the wave format block but absent from condition 4, so a
missing or wrong label is invisible to the counter. Round 29 routed exactly this defect class
for S154/S155 (`corpus/lessons/round-29-verifier-spotcheck.md:152-166`). Any r30 Gate line can
repeat it with `C1=met`.

### F6 — INFO: the counter does not exist yet

`count-c1.sh` was absent from `.ufo/waves/round-30/` at review time (18:14Z listing; HEAD
`e936482a` adds no counter). Findings above derive from the contract text and the wave format
block; BuildCountC1's implementation may resolve some F3 items. Recheck this report against
the counter's code once it lands; treat F3 items as requirements on it, not proven defects in
shipped code.

### F1 — no defect (evidence): the case base is reachable with margin — assignment question 1

- Files at `tools/fixtures/mori-oom-killers/`: `cases.json` 32 cases (verdicts: 14 QUIET /
  10 ACTED / 8 UNKNOWN), `cases-supplementary.json` 32 (12/11/9), `cases-a2.json` 30 (6/15/9).
  94 cases, every verdict value present in every file.
- Worktree equals the entering tip for all five audited paths (the three older case files,
  `cases-a2-r29.json`, `tools/mori-oom-killers.py`): `git diff --stat 58b61681... -- <paths>`
  is empty and `git status --porcelain` on them is empty. The bytes I ran are the tip blobs.
- Base tool reproduces the expects: `--selftest --cases` exits 0 on all three files.
- Distinct invocation-scope shapes spanned (from case ids and `why` fields), far above 8:
  scope boundary one microsecond before start (`c02`), boundary exactly at start (`c03`),
  incomplete scope with/without action (`c04`/`c05`), unit inactive (`c06`), unit absent
  (`c07`), null journal (`c08`), unverified version grammar (`c09`), oomd notices positive
  (`c10`, `c29`, `c30`), byte-array MESSAGE incl. invalid UTF-8 (`c11`/`c12`), action-kind
  taxonomy sigterm/sigkill/escalation/kill-failed/low-memory (`c13`-`c17`), dryrun (`c18`,
  `a2-04`), nearmiss grammar lines (`c20`-`c24`), null show / show without ActiveState
  (`c25`-`c27`), ActiveState failed/deactivating/activating (`a2-02`), group kill (`a2-03`),
  monotonic stamp zero/missing (`a2-05`), earlier-invocation sends suppressed for an active
  unit and positive for an inactive one (`a2-06`), malformed monotonic stamp (`c35`).
- `--inputs` spot-runs (tool copied to /tmp, inputs written to /tmp), each compared against
  the case's `expect.verdict` and every `expect.fields` path: `c02-scope-boundary-one-
  microsecond-before` OK; `a2-06-active-earlier-invocation-sends-quiet` OK;
  `c35-malformed-monotonic-timestamp` OK (tool exit 2 observed; condition 3 requires printed
  verdict and fields, not exit); `a2-03-group-kill-one-with-sigterm-action` OK with verdict
  KILLER_ACTED (exit 1). All three verdict classes exercised via `--inputs` at least once.

## Assignment answers in one line each

1. Yes — 94 older cases, all reproduced by the base tool at tip bytes (three selftests exit 0;
   four `--inputs` spot-runs match verdict plus every pinned field), spanning 19 distinct
   invocation-scope shapes. No reachability defect.
2. Yes, a trivial entry meets conditions 2-5 in the letter (F2): copy expects into 8 rows with
   a constant shape cell, cite any three S156+ pages. The counter cannot see shape meaning,
   distinctness, source topicality, quote support, sha authenticity, word-count labels, the
   A2a-limit routed requirement, or header-line substance. Wave-2 must check all of these.
3. Not unambiguously (F3): escape handling, collapse rule, `:L`-vs-`lines:` mismatch, sparse
   vs complete excerpts, first-tab splitting, cell decoration, and the two divergent Gate-line
   specs all leave pass/fail to implementation choice, with zero in-repo precedent files.

## Wave-2 reader checklist (ready to paste)

```
1. Shapes: rows carry several DISTINCT shape values; each shape text describes its case's inputs.
2. Topicality: every cited S156+ row is about earlyoom/systemd scoping or a field its rows pin.
3. Quote support: each Gate quote actually supports the shape/verdict of the row citing it.
4. Refetch each S156+ URL; sha256 must match the excerpt header AND the Gate line; compare
   quotes against the committed excerpt bytes (live files rotate).
5. wc -w each quote; the Gate `(N words)` label must match (round-29 R2/R3 class).
6. Entry and SKILL state the A2a limit for the disputed shape (contract.md:118) — uncounted.
7. source:/verified-at:/recheck: have real values; recheck is a future date.
8. SKILL Round30 rows carry substance, not just the tag and the path.
9. Exactly one counted table; header cells exactly shape/verdict/fields/case/sources.
10. Every cited case id in exactly one older file, blob equal to the entering-tip blob, and
    --inputs reproduces verdict plus every pinned field for that case.
11. Gate/excerpt files parse under the counter's published normalization: quote escaping,
    whitespace collapse, first-tab split, `lines:` form for single-line quotes, sparse-vs-complete.
```

## Residual risk and verification gaps

- I did not fetch any source URL and cannot vouch for any S156+ row that appears later; the
  committed-bytes counter cannot either (F2e). This is the largest unauditable surface.
- Worktree-vs-tip equality was verified only for the five audited paths; other paths were not
  diffed against `58b61681`.
- F3/F6: until BuildCountC1's code lands, every parse question above is a requirement, not an
  observed counter behavior; my false-met scenarios are [INFERENCE] about a parser that does
  not yet exist.
- No lsp device answered (absent from this session's tool inventory); caller/definition checks
  elsewhere in the wave should not treat this report as semantic-proof grade.
- C2 substance (residual 24/24, blindness gate, freeze provenance) was not reviewed here.

## Tooling and scratch

No tools installed or updated (preinstalled python3 and git only; pacman untouched, per the
host-wide pause). Scratch: `/tmp/mok-spot-mdc87z6k` and `/tmp/mok-spot2-*` held the copied
tool and inputs objects and were removed after the runs. The only lane write is this report.

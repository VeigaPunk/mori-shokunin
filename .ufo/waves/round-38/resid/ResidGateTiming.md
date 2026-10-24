# ResidGateTiming — C3 residual falsification: re-derivation and side-branch attack

Seat: mori-r38.ResidGateTiming (residual falsification, round 38). Detection and report only; no remediation.

Verdict: all four C3 claims reproduce at the landed tip. The side-branch attack **confirms** w2/CritGateSemantics at the shipped
bytes with an independent, new fixture: a superseder that is incomparable to the edit commit is reported as
`superseded_as_of` while P-C6 requires `stale_supersede`. The defect is latent on the lane, whose registry history is a single
chain.

## Reviewed bytes and environment

- Tip under attack: `b6993744171a05efc627b5e0664489c31aa5214e`. The assignment's verification command
  `git -C … rev-parse mori` **fails in this lane** (`fatal: ambiguous argument 'mori'`); the tip was confirmed instead as
  `refs/heads/master` = `b6993744…` and `git rev-parse b6993744^{commit}` returns the same full id.
- Gate under review: `tools/mori-sources-appendonly.py`, blob at the tip, SHA-256
  `9a6164e391479bcc9e50487f9eabbc95d4f25d57793f77575d33f8520fdb09fa`. The file's last change is `daa1d4d`; the bytes are
  identical to the blob the w2 critic executed from `f725f307` (same SHA-256).
- Same-identity check: the lane worktree copy of `tools/mori-sources-appendonly.py` and `corpus/SOURCES.md` is byte-identical
  to the tip blob (`sha256sum` above; `git diff --stat` over both paths empty), so the printed claim command executes the
  reviewed bytes in either the worktree or the scratch clone. The worktree does carry 14 unrelated dirty paths from peers;
  none were read or touched.
- Execution: all gate runs were made from a scratch clone checked out at `b6993744`; attack fixtures live under
  `/tmp/r38-resid/` (scratch clone `…/clone`, fixtures `…/attack-A`, `…/attack-B`, `…/attack-C`). Nothing was written to the
  lane except this report; nothing was committed.
- Environment: git 2.56.0, Python 3.14.8. No language-server device exists in this seat (`xd://lsp` → "No such tool";
  mounted devices are `ast_edit`, `debug`), so caller/definition checks below are execution- and git-plumbing-based, never
  text-grep presented as semantic proof.
- No tools installed or upgraded.

## 1. The four C3 claims at the shipped bytes — PASS

Commands were run verbatim (abbreviated rev for the claim, full SHA checked to resolve identically). Expected lines are
quoted exactly as printed.

### (1) Tip with round base — PASS

```sh
python3 tools/mori-sources-appendonly.py b6993744 --round-base f10a320d
```

Observed, exit 1, empty stderr (exit 1 is the tool's documented "with --round-base: the round changed the registry" result,
not a failed invocation):

```text
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[S182,S193]
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[]
```

`superseded_as_of` carries exactly **18** ids, 18 distinct, in the same order as `superseded`; `stale_supersede=[]`. The
committed receipt `.ufo/waves/round-38/evidence/gate-after.txt` is line-identical apart from its `command:` line (which names
`f725f307…`, the parent of the landing commit) and its trailing `EXIT=1`.

### (2) At e37dcc6 — PASS

```sh
python3 tools/mori-sources-appendonly.py e37dcc6 --round-base f10a320d
python3 tools/mori-sources-appendonly.py e37dcc6            # same answer, base irrelevant to timing
```

Observed in both, exit 1:

```text
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[S069]
```

Mechanism, re-derived: S073's row teaches `supersedes S069 — string-only containment …` and first appears at `71abd41`
(path-history index 10, 2026-10-21 08:18); S069's only immutable-cell change commit in the whole path history is `62db24c`
(index 41, 2026-10-22 23:55). Landing is not strictly later than the edit, so S069 is stale at `e37dcc6`. The committed
receipt `evidence/gate-after-e37dcc6.txt` matches this timing line exactly.

### (3) Selftest — PASS

```sh
python3 tools/mori-sources-appendonly.py --selftest
```

Observed: `MORI_SOURCES_APPENDONLY_SELFTEST pass=9 fail=0`, exit 0, matching `evidence/gate-selftest-after.txt`.

The two timing fixtures were not merely read; each was rebuilt with the module's own `_render`/`_row`/`_make_repo` helpers
from the shipped bytes and driven through the CLI (`_run_cli`):

| Fixture (source line) | History | Observed timing line | Exit |
|---|---|---|---|
| `superseding row` (437) | base → immutable edit → superseder lands | `superseded_as_of=[S001] stale_supersede=[]` | 1 |
| `supersede before edit` (441) | superseder present → immutable edit | `superseded_as_of=[] stale_supersede=[S001]` | 1 |

So the fixture pair lists S001 as-of versus stale respectively, as claimed. Both fixtures are linear snapshot chains.

### (4) S226 row and landing ancestry — PASS

- At `b6993744`, `corpus/SOURCES.md` row `S226` has its `teaches` cell opening
  `supersedes S069 — containment is decided on the resolved canonical path, …` — the row opens `supersedes S069`.
- S226 first appears at `daa1d4d`. `git merge-base --is-ancestor 62db24c daa1d4d` → exit 0 (descendant); in the
  path-scoped history S069's edit is index 41 and the landing index 51, and the path history is a single ancestry chain.

### Independent ancestry oracle over the 18 as-of ids

Because the implementation compares log indices, claim (1) could be accidentally right. It is not: for every one of the 18
ids the latest superseder's landing commit is a **genuine descendant** of the id's last immutable-cell edit commit, checked
with `git merge-base --is-ancestor` (all exit 0):

| Superseded | last immutable edit | latest superseder row | landing |
|---|---|---|---|
| S041 S044 S051 S069 | 62db24c | S206 S207 S208 S226 | bf0df77, bf0df77, bf0df77, daa1d4d |
| S062 S064 S180 S181 S183 S184 S185 S186 S188 S189 S190 | ab8f4cf | S209 S210 S212 S213 S214 S215 S216 S217 S218 S219 S220 | bf0df77 |
| S179 | 5126891 | S211 | bf0df77 |
| S182 | 8d56809 | S201 | cedb0ec |
| S193 | 406d91a | S202 | cedb0ec |

Lane shape that makes those indices meaningful: `git log --reverse b6993744 -- corpus/SOURCES.md` yields 52 commits, none
with two parents, and every consecutive pair is ancestry-ordered (`merge-base --is-ancestor` exit 0 for all 51 pairs). A
linear chain is the only history on which index order equals ancestry order.

## 2. Attack: superseder on a side branch incomparable to the edit — CONFIRMED

One DAG shape, three scratch repositories: `c0` is the root; `c1` (main) and `c2` (side) are its two children; `M` merges
them. `c2` is incomparable to `c1` in all three (`merge-base --is-ancestor` both directions exit 1; merge-base is `c0`).
**All three final trees are identical** — `1b214945a26ebdc53c3b65d75bd9d2d97afcd5f6`, `corpus/SOURCES.md` SHA-256
`d799c699c93a1444e2306d864f856048488e5a0b7ae3b97f56c0bdacf818dee9` — so no verdict difference can be attributed to registry
content.

### A — duplicate identical edit on the side branch (the counterexample)

| Commit | Parents | Date (UTC) | Registry content |
|---|---|---|---|
| `1a8c5de87e…` c0 | — | 10-01 00:00 | S001 anchor `anchor a` |
| `acf841f453…` c1 (main) | c0 | 10-01 01:00 | S001 anchor `anchor a v2` |
| `a56f0c2e3e…` c2 (side) | c0 | 10-01 02:00 | S001 anchor `anchor a v2` (identical cells) + S002 `supersedes S001 — replacement`, status `mined` |
| `53e71cb4f2…` M | c1, c2 | 10-01 03:00 | S001 anchor `anchor a v2`; S002 status `queued` (mutable cell only) |

`git diff M^1 M` adds only the S002 row; `git diff M^2 M` changes only S002's mutable `status`, so the merge is TREESAME to
neither parent and both branches stay in the walk.

Observed, shipped gate (`… b6993744` blob), exit 1, empty stderr:

```text
changed S001 superseded_by=S002
appendonly_violations=1 ids=[S001] deleted=[] superseded=[S001] round_changed=[]
supersede_timing superseded_as_of=[S001] stale_supersede=[]
```

Real ancestry: `merge-base --is-ancestor c1 c2` → 1; `merge-base --is-ancestor c2 c1` → 1. `c2` is not a descendant of `c1`.

P-C6 (`contract.md:95`, repeated verbatim at `tools/mori-sources-appendonly.py:76-84`) requires stale here under **both**
readings of "the id's last immutable-cell edit commit":

- recorded last edit = `c1` (walk index 1) → `c2` is not its descendant → stale;
- branch-local last edit = `c2` → landing equals the edit, and the predicate demands a *strictly later/descendant* relation →
  stale.

The printed `superseded_as_of=[S001]` is therefore false at the shipped bytes.

### B — timestamp-only control (same DAG, same snapshots, one date swap)

Only the commit dates of the two siblings move: c2 at 01:00, c1 at 02:00 (`e7f78d333e…`, `29d5d3cfbc…`, merge
`0f76904eef…`). Final tree identical to A. Observed:

```text
supersede_timing superseded_as_of=[] stale_supersede=[S001]
```

Exit 1, empty stderr. Same final registry content, same parent relationships, opposite verdict — the classification is a
function of traversal/date order, not of ancestry.

### C — control: side branch does not duplicate the edit

Same dates as A; in `c2` (`8769c59bef…`) S001 is left at `anchor a` and only S002 is appended; the merge
(`1fcbcaf133…`) resolves to `anchor a v2` + S002 `queued`, so the final tree is again identical to A and B. Observed:

```text
supersede_timing superseded_as_of=[] stale_supersede=[S001]
```

This verdict is correct **only by accident**. Instrumentation of the shipped `analyze` internals shows the phantom edits
that produce it: `changed_at = {c1: [S001], c2: [S001], M: [S001]}` — S001 is flagged as edited at `c2`, whose parent `c0`
carries exactly the cells the tool last saw, and again at `M`, whose S001 cells match its first parent. Those phantom edits
drag `last_edit` onto the landing commit, so the index comparison returns stale for the wrong reason.

### Instrumentation summary (shipped `analyze`, indices into the path walk)

| Fixture | Walk order | `changed_at` (S001) | S002 first appears | `landing > last_edit` | Printed | Real ancestry |
|---|---|---|---|---|---|---|
| A | c0, c1, c2, M | index 1 (c1) | index 2 (c2) | 2 > 1 → as-of | as-of | stale (incomparable) |
| B | c0, c2, c1, M | index 1 (c2) | index 1 (c2) | 1 > 1 false | stale | stale (incomparable) |
| C | c0, c1, c2, M | indices 1, 2, 3 | index 2 (c2) | 2 > 3 false | stale | stale (incomparable) |

## Findings

### F1 — HIGH (semantics and calibration): P-C6's descendant requirement is implemented as path-log index order

- Evidence: fixture A above, at the tip's own blob; predicate text at `contract.md:95` and `tools/mori-sources-appendonly.py:28-33,76-84`.
- Code path: `analyze` obtains `git log --format=%H --reverse REV -- corpus/SOURCES.md` (`:220-221`, no parents, default
  history simplification), records the first-appearance index of every `supersedes S###` row (`:273-276`), and decides with
  `if cid in last_edit and landing > last_edit[cid]` (`:286`). No ancestry primitive is used anywhere: the only git verbs in
  the file are `rev-parse`, `log` and `show` (no `merge-base`, no `rev-list`).
- Consequence: `superseded_as_of` is not a disposition-validity fact on any history with a merged registry branch. A
  superseder that is incomparable to the edit is reported as as-of whenever the walk places it later (A), and the same DAG
  flips to stale when only a date moves (B). Callers of the field (SCORECARD C3 cell, waves that read the timing line) cannot
  rely on the predicate's words.
- Scope on the lane: latent, not active. The lane's `corpus/SOURCES.md` history is a single chain (52 commits, no merges),
  which is why claim (1)'s 18 ids are ancestry-correct; no current receipt is falsified by F1.

### F2 — MEDIUM (supporting defect in the same walk): edit detection compares adjacent log records, not parents

- `:246-263` compares each commit's snapshot with the previous *log record's* snapshot instead of its parent's. On the
  diamond, this fabricates edits and reversions: C flags S001 as changed at `c2` (parent `c0` is identical) and at `M`
  (S001 matches its first parent). Fixture A/B avoid the phantom only because both branches carry identical cells.
- This variable feeds `last_edit`, i.e. C3's decision input, and `round_changed`, which is C1/C2's axis; it also explains why
  C reaches the right answer by the wrong path. It is the same defect class the w2 critic reported; the fixture here shows it
  producing a false as-of with no revert commit and no second superseder.

### F3 — LOW (evidence provenance): the C3 after-receipt is not a receipt of the landing commit

- `.ufo/waves/round-38/evidence/gate-after.txt:1` records
  `command: python3 tools/mori-sources-appendonly.py f725f3076972e6e70595b5ac8279be524a111ff8 --round-base f10a320d`.
- Live output at `b6993744` is line-identical apart from that `command:` line and the trailing `EXIT=1`, so the claim holds at
  the tip; the receipt name simply does not pin the tip. (This is distinct from the SCORECARD line-offset erratum reported in
  ResidFreezePins.)

## Residual risk

1. **Lane linearity is the only guard.** The 18-id receipt is ancestry-correct because the registry path history has no
   merges today. Any future merge over `corpus/SOURCES.md` silently opens F1: the gate will not error, it will just classify
   by walk order, and a superseder landing on a side branch can discharge an edit it never descends from.
2. **"Latest superseder" is also order-defined.** The implementation keeps the maximum first-appearance index per
   (superseded id, superseder row). In A the merge re-lists S002 and the landing correctly stays at `c2`, but with two
   *different* superseding rows on incomparable branches the choice is by index only. I did not construct a fixture where
   that yields a wrong verdict (single superseder in all three fixtures here).
3. **History simplification is unexamined.** `git log -- path` (default) can drop side-branch commits at TREESAME merges,
   removing an edit from `changed_at` or a superseder's first appearance from `supersede_landing`/`first`. All three fixtures
   were made non-TREESAME at the merge (via a mutable cell) precisely to keep both branches in the walk; a TREESAME variant
   was not probed to a counterexample in this seat.
4. **The predicate itself is DAG-ambiguous.** "The id's last immutable-cell edit commit" is undefined when two incomparable
   commits edit the id. F1 does not depend on resolving that: fixture A is stale under both candidate readings.
5. **`round_changed` scope.** `--round-base f10a320d` resolves to a round-33 spot-check commit, so `round_changed` spans
   rounds 34-38 (`[S182,S193]` at the tip). That is the round base of record used by the contract, not a C3 defect, but the
   number must not be read as round-38-only.

## Verification gaps

- Only C3 was re-derived. The C1/C4/C5 counters and `conform.py` were not run (other claims, other seats).
- One git version (2.56.0) and one Python (3.14.8). The property that makes the false-*negative* direction safe — a
  parent is never emitted before its child, so a genuine descendant's landing always sorts after the edit — is a traversal
  property of `git log` rather than a version feature; observed in A/B/C, not proven for other git builds.
- No language-server device in this seat; caller and definition checks are execution plus call-graph reads of the shipped
  file, not LSP proofs.
- Fixtures are scratch (`/tmp/r38-resid`), not committed; the lane received only this report.

Report: .ufo/waves/round-38/resid/ResidGateTiming.md

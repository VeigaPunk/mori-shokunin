# Mo60Scribe71 — SOURCES rows S561–S563 (draft) + located Gate quotes

Seat: Mo60Scribe71 (scribe, leaf). Work read-only on the lane; all scratch under
`/fast/scratch/hyaku/mori-r60/Mo60Scribe71/` (cleaned at yield). No lane VCS
mutation, no production/registry/SCORECARD/LOG edit, no fleet or sibling writes,
no subagents. Disk guard green at start (`/fast/scratch/hyaku` 26% used,
597.3G free). No tool installs or updates were performed.

Pinned revisions used for every re-derivation:

| label | revision | how obtained |
|---|---|---|
| lane tip R | `0f8340cf62b588fd64be8d9176ed7d5444c426b2` | `git rev-parse HEAD` at report time (moved under me: `b3c25613` → `0f8340cf` during the seat) |
| r60 entering | `ddfb12fb0838b4307c445194a844f0c4b1950195` | contract |
| r60 amended freeze | `ac496c7cde8cad965079858accae3bedfe4a73f2` | contract |
| r59 freeze | `60b3a76ad0524c8978cc51922940be1c8c388915` | `.ufo/waves/round-59/contract.md` / `corpus/lessons/round-59.md:4` |
| r59 data rev | `7b86704d7c0754a09958d131b64dbfa2a6d3eaed` | contract C1 receipts arm |
| reports landed | `bf6c0ad3` (03:12:38 -03) | `git log --diff-filter=A` |

## Headline: the three rows already landed before this seat ran

`corpus/SOURCES.md` at R already carries S561/S562/S563 (lines 341–343) plus the
rejected S564 — committed in `398d3225`, moved into the `## Registry` table by
`b3c25613` ("census E12 fix"). My draft therefore **replaces** three existing
rows; it is not an append. Three substantive deltas are proposed, listed under
"Findings".

## Draft rows (11 cells each, no `|` inside any cell — verified by cell split)

Base = `corpus/SOURCES.md` at R, rows 341–343 replaced. Cell count checked: 11/11/11;
`any('|' in cell)` = False for all three.

```
| S561 | mori round-59 w1 attack report Mo59Critic22 — met-flip construction for the frozen r59 C2 entry arm (D1-D5) | own-work | A | what the frozen r59 C2 entry predicate actually enforces over committed bytes: claim text, quote-span distinctness, grammar routing, registry row binding | `.ufo/waves/round-59/w1/Mo59Critic22.md` L46 defect D2 (identical 6-byte span at offset 3) with the counterexample at L16-L27; committed at `bf6c0ad3`, blob `7538acff962255c4d139072198e89f7ad7048a82`, sha256 `efcc786fc5a2d8eeac5bfd863de3410a722033d9add7c1ce1a4734598fb60a27` | Claim text, span distinctness, grammar routing and row binding are four separate checks; meeting only the byte-pin shape leaves a met verdict reachable with a zero-information entry | mined | 2026-10-28 | 180d | corpus/knowledge/entry-claims-hardening-r60.md |
| S562 | mori round-59 w1 sentinel report Mo59Sentinel57 — counter execution and write-boundary PoC | own-work | A | the r59 counters' execution and materialization boundary: sha-pin gating versus execution, scratch containment, symlink-following writes | `.ufo/waves/round-59/w1/Mo59Sentinel57.md` L24 F1 step 2 (pin gates bookkeeping only) and L29 the observed unpinned-blob run; committed at `bf6c0ad3`, blob `8eb1335ee1b1ca711d92d0dc9bd0dbb82212eb91`, sha256 `2e7a0cbb2a77f1a91927c3b8ec0e229292bad7c33cefff01bfbaac2cd424e326` | A pin that gates only reporting still executes repo-supplied bytes, so execution must be gated on the pin and every materialized path containment-checked before it is written | mined | 2026-10-28 | 180d | corpus/knowledge/entry-claims-hardening-r60.md |
| S563 | mori round-59 w1 critic report Mo59Critic25 — drift-arm under-attribution | own-work | A | the r59 C2 drift arm as written at `count-c2.py:251-263`: a bare nonzero exit, with no stdout verdict or reason parsed | `.ufo/waves/round-59/w1/Mo59Critic25.md` L17-L19 arm statement and L44-L53 the M1/M2 mutants that pass it; committed at `bf6c0ad3`, blob `a904631bdb228d6c58c179a97ac2a17fa96ff977`, sha256 `91640613738459e8e87ea7ada7443dfc5685401f9bc8ea4d5c8e79fa8e59af80` | A nonzero exit cannot attribute a schema-drift reason, so the arm must parse the verdict and a drift reason and carry a renamed control that the same tool scans OK | mined | 2026-10-28 | 180d | corpus/knowledge/entry-claims-hardening-r60.md |
```

## Located Gate quotes (verbatim, ≤25 words, each unique in its report)

All three verified **against committed bytes at R** (`git show R:<path>`), not
just the working tree; each is a single distinct occurrence in its file, and
contains no `|`.

| row | location at R | quote | words |
|---|---|---|---|
| S561 | `.ufo/waves/round-59/w1/Mo59Critic22.md` L46 | `All 10 claims cite the same 6-byte span `"lane"` @offset 3 — the "quotes repeated trivially" attack lands.` | 18 |
| S562 | `.ufo/waves/round-59/w1/Mo59Sentinel57.md` L24 | `Both counters compute `tool_ok` but gate only the *bookkeeping*, not execution:` | 11 |
| S563 | `.ufo/waves/round-59/w1/Mo59Critic25.md` L17-L19 | `stdout is never read; no verdict or reason attribution; any nonzero code — including exit 2 usage/crash — satisfies the arm.` | 21 |

Verification commands (all read-only, run from the lane root):

```
git -C . show 0f8340cf:...:Mo59Critic22.md    # L46 contains quote; 1 occurrence in file
git -C . show 0f8340cf:...:Mo59Sentinel57.md  # L24 contains quote; 1 occurrence in file
git -C . show 0f8340cf:...:Mo59Critic25.md    # L17-L19 joined contains quote; 1 occurrence in file
```

## Findings

### F1 — S561's landed anchor names a revision where the report does not exist (dead pointer)

The landed row's anchor cell reads, verbatim:

```
report `.ufo/waves/round-59/w1/Mo59Critic22.md` §Counterexample and defect table D1-D5, at r59 freeze `60b3a76a`
```

Ground truth by `git cat-file -e`:

```
$ git cat-file -e 60b3a76a:.ufo/waves/round-59/w1/Mo59Critic22.md
fatal: path '.ufo/waves/round-59/w1/Mo59Critic22.md' exists on disk, but not in '60b3a76a'
$ git ls-tree 60b3a76a .ufo/waves/round-59/
100644 blob 4d0093b3…  contract.md
100755 blob 251d4de2…  count-c1.py
100755 blob 260ac526…  count-c2.py
040000 tree 367b9729…  evidence
040000 tree fd6b07a3…  fixtures-c1
040000 tree 9df57d4e…  trees-c2            # no w1/ directory
$ git cat-file -e 7b86704d:.ufo/waves/round-59/w1/Mo59Critic22.md   → absent
$ git log --diff-filter=A -- .ufo/waves/round-59/w1/Mo59{Critic22,Sentinel57,Critic25}.md
bf6c0ad3 round-59: integrate w1 — … 62 seat reports       # first commit carrying all three
```

So the anchor as written points at a revision at which the cited artifact is
absent — the same pointer class C1's DEAD-NAME ARM scores this round, and the
same class `corpus/lessons/round-60.md` mistakes row 1 records. S562 and S563
landed with **no revision at all** in their anchor cells (S562: "F1-F4 with the
demonstrated overwrite PoC"; S563: "§Decisive mutants table"), so neither is
re-derivable from the registry. My draft replaces "at r59 freeze `60b3a76a`"
with the landing commit plus blob id and byte hash for all three rows.

Note the reports are also present in the dangling commit
`eaa6d0a9a30f602f10baff705d524c8e89adf118` (parent `7b86704d`, same author/
committer timestamps as `bf6c0ad3`, tree differs from `bf6c0ad3` only by 8
`.ufo/waves/round-40/scratch/…` paths, reachable only via
`refs/jj/keep/eaa6d0a9…`). Blob ids are identical in both:
`7538acff…` / `8eb1335e…` / `a904631b…`, so the reports never changed after
landing (identical at `bf6c0ad3` and at HEAD; worktree clean, mtime ≠ content
change).

### F2 — S563 landed at tier B; this seat's instruction says tier A (conflict, reported verbatim)

| source | S563 tier | verbatim |
|---|---|---|
| seat instruction (this seat) | A | "own-work, tier A, status mined" |
| landed row (R, line 343) | B | `| S563 | … | own-work | B | the drift arm of the r59 C2 counter: what a bare nonzero exit proves | …` |
| `corpus/lessons/round-60.md` L30-31 | B | "S563 — Mo59Critic25 report (own-work B): drift-arm attribution" |
| `contract.md` §Sourced-claim rule | either | "own-work tier A/B: the committed r59 attack reports Mo59Critic22, Mo59Sentinel57, Mo59Critic25" |

I followed the seat instruction (tier A) in the draft. The lesson text and the
landed row both say B, and the contract admits A/B, so this is not a
correctness defect either way — it is an unresolved discrepancy the L1 must
settle before the row is rewritten. Census effect of the swap alone:
`tier.A 299→300`, `tier.B 18→17`, rows/mined/queued/rejected unchanged.

### F3 — Lesson Gate quotes for S561 and S562 are not verbatim to the reports

`corpus/lessons/round-60.md` quotes the admitted sources; two differ from the
committed bytes:

| lesson line | lesson text | report text at R | verdict |
|---|---|---|---|
| L25 | `"K1–K10 identical (…:offset:3; …)"` | `` `K1–K10 identical `(…:offset:3; …)` `` — the report has back-ticks around `(…:offset:3; …)` | not verbatim (back-ticks dropped) |
| L28 | `"the unpinned blob ran"` | `the unpinned blob ran` (lower-case inside a sentence) | verbatim (case matches) |
| L31-32 | `"A nonzero exit on this file` / `is attributable to any subset"` | same two lines L34-L35 | verbatim across the line join |

Command: `python3` compare of each lesson quote against report bytes at R
(`" ".join(text.split())` on both sides). Only S561's differs. Since C1's
lesson arm scores *presence of strings*, this is not a scoring break; it is a
fidelity note for the non-author closure, and my draft row's `teaches` cell does
not quote the lesson text.

### F4 — Draft rows are H4-neutral and C2-safe (checked, not assumed)

Rows S561–S563 are not binders for the six `corpus/evidence/sources-r59/`
copies (S553–S559 are), so changing them cannot move the H4 arm. Verified by
running the pinned verifier (`sha256 cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69`)
over a scratch root built at R from committed bytes:

```
# baseline: registry = SOURCES.md at R
{"schema": "mori-entry-claims-v2", "ok": true, "reasons": [], "stats": {"claims": 13, "files": 6, "spans": 13, "min_span": 12}}   exit 0
# with my three draft rows substituted
{"schema": "mori-entry-claims-v2", "ok": true, "reasons": [], "stats": {"claims": 13, "files": 6, "spans": 13, "min_span": 12}}   exit 0
# with the three rows deleted entirely
{"schema": "mori-entry-claims-v2", "ok": true, "reasons": [], "stats": {"claims": 13, "files": 6, "spans": 13, "min_span": 12}}   exit 0
```

Sensitivity control on the same root (binder source cell for S557's r58
artifact renamed):

```
{"schema": "mori-entry-claims-v2", "ok": false, "reasons": ["rows:binding=corpus/evidence/sources-r59/w1-results-r58.json"], "stats": {…}}   exit 1
```

i.e. the arm is live and my rows do not touch it. Full r60 counter at R, for
row-interaction only (read-only, `--scratch` given, TMPDIR set inside scratch):

```
$ python3 .ufo/waves/round-60/count-c2.py 0f8340cf62b588fd64be8d9176ed7d5444c426b2 --scratch <scratch>/c2scratch
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=0f8340cf62b588fd64be8d9176ed7d5444c426b2
exit 0
```

### F5 — Census: the draft introduces no new E-code and no new W-code

`scripts/sources-census.sh` run against a symlink-backed fakeroot whose
`corpus/SOURCES.md` is the draft and every other corpus/lane path resolves to
the real lane (`--file` on the draft with the real lane's directories linked
in):

```
$ bash scripts/sources-census.sh validate --file <scratch>/final/corpus/SOURCES.md --today 2026-10-28
file	ok	<scratch>/final/corpus/SOURCES.md            exit 0
E-codes 0 · W04 25
$ # same harness on SOURCES.md at entering ddfb12fb:
file	ok	…                                             exit 0
E-codes 0 · W04 25
E-set identical: 0 findings both runs
```

`census` counts, draft vs live:

| metric | at R (live) | draft |
|---|---|---|
| rows | 337 | 337 |
| tier.A | 299 | 300 |
| tier.B | 18 | 17 |
| tier.C | 20 | 20 |
| mined | 282 | 282 |
| queued | 24 | 24 |
| rejected | 31 | 31 |

Entering `ddfb12fb` was 333 rows (S561–S564 unreleased), so rows 333→337 was
already carried by `398d3225`; my replacement changes only the S563 tier cell.

## Method bounds and clean-room discipline

- Every lane read was `git show`/`git cat-file`/`git ls-tree` at an explicit
  revision, or a plain file read of a path whose blob id I recorded; no
  unpinned working-tree byte was used as evidence for a claim about a revision.
- No git writes, no `git add/commit/checkout/reset/push`, no `jj`, no `chmod`,
  no `rm` inside the lane; the only writes were under
  `/fast/scratch/hyaku/mori-r60/Mo60Scribe71/` (fakeroot trees, verifier root,
  counter scratch) plus this report.
- Fixture repos: none were needed. The verifier and census were run on
  materialized roots copied out of `git show` output, not on a clone; no
  `git init` occurred, so no commit exists outside the lane.
- Host guard honoured: process cwd was the fleet root; every command used
  absolute paths or `cd` into my own scratch; no PATH directory, no fleet-native
  tracked file touched.
- Not checked (out of seat scope): C1's dead-name/receipt/absent-set arms, C3,
  the r60 counters' internal correctness, and whether the S564 rejection text is
  the right disposition. I did not read any other seat's round-60 scratch.
- The lane tip moved during this seat (`b3c25613` → `0f8340cf`, lesson-only
  commit); all row/anchor/quote claims above are pinned to `0f8340cf` and the
  three blobs are unchanged between `bf6c0ad3` and `0f8340cf`.

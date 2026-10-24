# CritNewDag — C2 falsification (gate v3 vs P-C11's words)

Seat role: critic (read-only). Target: claim C2 / P-C11 on
`tools/mori-sources-appendonly.py` v3.

**Verdict: C2 is falsified** — v3's output contradicts P-C11's words on three
independent input classes, each demonstrated on a freshly-built fixture DAG.
Builder: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/critnewdag/build-dags.py`;
fixture repos persist under `.scratch/critnewdag/repos/`; full raw run log:
`.scratch/critnewdag/runlog.txt`.

## Instruments under test (byte identity verified)

- v3 = `tools/mori-sources-appendonly.py` at HEAD (`ede486b`),
  sha256 `bde5a9a34c7eb3bcbee39d669b8d187caeb51807ad1bdcd85a05c1bcd06777ec` —
  identical to `git show 265a955cc…:tools/mori-sources-appendonly.py` and to
  the freeze pin in `evidence/freeze-r40.txt`.
- v2 = `.ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py`,
  sha256 `62cd4132dbe141538371f79723c3caff66670fab9076494cd9cf65efccfc01e7` —
  identical to `git show bb1f2457…:tools/mori-sources-appendonly.py`.
- Sanity: `python3 tools/mori-sources-appendonly.py --selftest` →
  `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` (exit 0), ~1.1 s.
- Every fixture below was run as
  `python3 <gate> HEAD --repo .scratch/critnewdag/repos/<dag> --round-base <b0-sha>`
  inside a subshell with the gate's own `_selftest_env()`.

## Counterexample 1 (strongest): dag-2l — verdict is walk-order, not ancestry

### Construction (identical DAG and identical contents in both twins)

    b0        [S001]
    s1 (side) [S001, S002 "supersedes S001 — replacement"]   parent b0
    c1 (main) [S001 anchor→"anchor a v2"]                    parent b0
    c2 (main) [S001v2, S003 "supersedes S001 — replacement"] parent c1
    m  (merge)[S001v2, S002, S003]                           parents [c2, s1]

S001's only immutable-cell edit is `c1` (recorded by the gate at `c1`).
Two rows land `supersedes S001` independently: S002 at `s1` (incomparable with
`c1`; `is_ancestor(c1, s1)` false) and S003 at `c2` (descends from `c1`;
`is_ancestor(c1, c2)` true). `dag-2l-early` dates `s1` 01:00 (before `c2`);
`dag-2l-late` dates `s1` 03:30 (after `c2`). Commits, tree, row contents:
byte-identical between the twins; only `s1`'s committer/author date differs.

### Both gates' outputs

| fixture | gate | changed line | timing line |
|---|---|---|---|
| dag-2l-early | v3 | `changed S001 superseded_by=S003` | `superseded_as_of=[S001] stale_supersede=[]` |
| dag-2l-early | v2 | `changed S001 superseded_by=S003` | `superseded_as_of=[S001] stale_supersede=[]` |
| dag-2l-late  | v3 | `changed S001 superseded_by=S002` | `superseded_as_of=[] stale_supersede=[S001]` |
| dag-2l-late  | v2 | `changed S001 superseded_by=S002` | `superseded_as_of=[] stale_supersede=[S001]` |

### Words contradicted

v3's retained docstring (analyze(), lines 250–251) states the as-of test "is
`git merge-base --is-ancestor` between the id's last edit commit and the
superseding row's landing commit (**not walk index order**)" — retained v2
semantics P-C11 explicitly claims to keep. But `supersede_landing[target]`
keeps the **latest first-appearance walk index**
(`if previous is None or index > previous[0]`, line 348), and the `--reverse`
walk is commit-date order (observed: `dag-2l-late` walks `b0, c1, c2, s1, m`).
Result: on identical registry content and identical ancestry, a commit *date*
flips which row v3 names as the superseder (`superseded_by=S003` → `S002` —
false provenance on the `changed` line) and flips the timing verdict
(`as_of` → `stale`). The verdict is a function of walk order plus ancestry,
so "the gate computes what the predicate says" fails wherever two landings are
incomparable in the DAG. Date order is at least a defensible "latest" reading;
what is not defensible is that the printed `superseded_by` and the stale flag
depend on it while the instrument's own contract disclaims walk-order.

## Counterexample 2: dag-h — fabricated edits from a column permutation

### Construction

    b0        [S001, S008, S002 "supersedes S001 — replacement"]   canonical header
    s1 (side) +S003                                              parent b0
    h1 (main) SAME rows, header permuted (cols 1↔6: source↔teaches) parent b0
    m  (merge) permuted rows + S003                              parents [h1, s1]

At `h1` and `m` **no row's cell values differ from b0's** — verified by dumping
all three trees. b0's own commit landed the S002 supersede row.

### Both gates' outputs (identical v3/v2)

    changed S001 superseded_by=S002
    changed S002 superseded_by=-
    changed S003 superseded_by=-
    changed S008 superseded_by=-
    appendonly_violations=4 ids=[S001,S002,S003,S008] deleted=[] superseded=[S001] round_changed=[S001,S002,S008]
    supersede_timing superseded_as_of=[] stale_supersede=[S001]
    EXIT=1

### Words contradicted

- "an edit at a commit is a change against its first parent's state" — `h1`
  changes no immutable cell of any row (the gate itself parses h1's header into
  a per-commit colmap, then discards it). The gate fixes `colmap`/`imm_idx`/
  `teaches_idx` once from the first walked commit (b0: `imm_idx=[0,1,2,3,4,5,6,8]`,
  `teaches_idx=6`); applied to permuted rows, slot 1 holds `teaches a` and
  slot 6 holds the URL, so `imm_key` differs on every row → fabricated
  `changed` events at `h1` (round_changed `[S001,S002,S008]`) and drifted
  `first`/`ids` (`S003` sighted canonical at s1, permuted at tip → `ids`).
- Consequence chain: fabricated `last_edit[S001]=h1` is not an ancestor of the
  supersede landing `b0` → `stale_supersede=[S001]`. P-C11's own words give
  as-of: S001's last immutable-cell edit is its first-sighting commit b0, an
  ancestor of (equal to) the landing commit b0.
- Mechanism probe (recorded in runlog companion): `imm_key` with the row's
  own colmap is EQUAL for all three rows; with the frozen b0 indices all DIFF.

### Companion dag-h2 (eligible-set half)

Linear `b0 → h1(permuted) → s2(permuted, adds S002 "supersedes S001")`. At the
tip the file literally asserts S001 is superseded; the gate's fixed
`teaches_idx=6` reads the URL cell, so `sup_map` never learns the pair:

    appendonly_violations=2 ids=[S001,S008] deleted=[] superseded=[] round_changed=[S001,S008]
    supersede_timing superseded_as_of=[] stale_supersede=[]

"the timing line's eligible set is every superseded id present at R" — S001 is
present at R and is superseded at R by the tip's own text; the timing line
lists nothing. Both halves of the same root cause: one stale global colmap.

## Counterexample 3: dag-z / dag-z2 — supersededness from a discarded branch

### Construction

    b0        [S001]
    s1 (side) [S001, S002 "supersedes S001 — replacement"]   (dag-z2: S001 edited too)
    c1 (main) [S001, S005]
    m  (merge)[S001, S005]        parents [c1, s1] — side content discarded entirely

At R (m) **no row supersedes S001**; the only `supersedes S001` text exists on
`s1`, whose content never reaches the tip. `--full-history` still walks `s1`
(it differs from its parent), so `sup_map` records the pair.

### Both gates' outputs

| fixture | v3 timing | v2 timing | other v3 lines |
|---|---|---|---|
| dag-z  | `superseded_as_of=[S001]` (exit 0) | empty | `deleted S002`, `superseded=[S001]` |
| dag-z2 | `superseded_as_of=[S001]` | empty | `deleted S002`, `superseded=[S001]`, `round_changed=[S001]` |

### Words contradicted

"the timing line's eligible set is every superseded id **present at R**":
v3 labels S001 superseded-at-R (and disposes it `as_of`) using a row the gate
itself reports `deleted` (`deleted S002` — the superseding row is absent at R,
deleted_at[m]). Internally inconsistent and semantically false provenance.
Distinguishing feature: **v3-visible** — v2's edit-bounded eligible set printed
nothing here; the new `tip ∩ sup_map` eligible set exposes the sup_map input's
dead-branch sourcing. In dag-z2 the `as_of` verdict additionally consumes an
edit (`s1`) whose content never reached R — under the literal words an edit is
any change vs first parent, so this is a semantic (not literal) contradiction;
listed because it shows the eligible-set extension did not come with a
reachability constraint on `sup_map`.

## Bounded attempts that did NOT contradict the words (recorded as negatives)

- **dag-o, true octopus (3 parents `[e1, a1, b1]`, two side supersede rows
  S002→S001, S003→S004):** v3 `superseded=[S001,S004]`,
  `as_of=[S004] stale=[S001]` — consistent: S001's edit `e1` is incomparable
  with its landing `a1`; S004 never edited. (v2: `[S001]` only — eligible-set
  widening visible.) First build attempt collapsed to a 2-parent merge
  (e1 was an ancestor of a1 — git fast-forwarded); rebuilt with incomparable
  tips.
- **dag-rm, linear delete-then-re-add of superseded S008 with MODIFIED
  immutable cells:** v3 `ids=[S008]` (tip-vs-first-sighting drift — the
  sanctioned channel), `superseded_as_of=[S008]` — consistent with the literal
  words: the re-add is no `changed_at` edit, so the "last immutable-cell edit"
  is the first-sighting commit. Flagged for the judge: the *semantic* outcome
  "as-of" for a row re-added with changed immutable cells is the weakest
  clause of P-C11's words, but v3 does implement them.
- **dag-wr, merge whose first parent is the walk root (`--no-ff`):** the
  merge commit `f24dde` has parents `[b0, s1]` and is TREESAME to `s1` (the
  side content won whole); a follow-up commit `47eaa0` adds S003. v3
  `stale=[S001]` — consistent with the words: `f24dde`'s state changes S001
  vs its first parent `b0`, so `f24dde` (walk-latest edit, dated later than
  the authoring commit `s1`) becomes `last_edit[S001]`, and the landing `s1`
  is not a descendant of `f24dde`. Worth flagging to the judge: the same
  under-determination class as dag-2l surfaces here — a merge that merely
  *kept* the side's edit is dated later than the edit itself, so "the id's
  last immutable-cell edit" resolves to the merge, a commit that authored no
  cell change. Consistent with the literal edit definition; semantically
  dubious provenance. Empirical note for the record:
  `git log --full-history` **does** list a merge that is TREESAME to a
  non-first parent (it differs from its first parent); a first-parent-
  TREESAME merge is the only kind it could drop, and such a merge cannot be
  where a tip-surviving row first appears — this closes the "unwalked first
  parent" attack class (including first-commit-as-merge sightings).
- **dag-t, merge resolved TREESAME to second parent:** v3
  `stale=[S001] deleted=[S005]` — consistent per the same words.
- **dag-x, superseding row deleted-then-re-added around an intervening edit:**
  v3 `stale=[S001]` — `supersede_rows` `setdefault` keeps the FIRST
  appearance, so the landing stays s1; consistent. (My initial hypothesis —
  landing moves to the re-add — was wrong; the code re-adds the ROW but the
  pair index is sticky. Recorded as a failed attack.)

## Classification

- **dag-2l**: fixable defect. Under-determination between "the superseding
  row's landing" (P-C11) / "its latest superseding row" (inherited P-C9
  reading) when >1 pair lands the same target on incomparable commits. The
  code already *chose* an arbitration (latest walk index) that is neither
  ancestry-based nor stated in the predicate.
- **dag-h / dag-h2**: fixable defect, inherited verbatim from v2 (identical
  outputs). Not v3's change, but P-C11 is the frozen contract of record for
  THIS gate; the claim is that the instrument computes the predicate, and on
  any registry whose header order ever differs the words are false. Nothing
  in the corpus pins a canonical column order (grep corpus/README.md,
  QUALITY.md: no column-order rule; `parse_registry` is explicitly
  header-name-keyed, so permuted registries are legal inputs).
- **dag-z / dag-z2**: fixable defect, newly exposed by the C2 change itself
  (v2 printed an empty timing line on the same DAG). Eligible-set widening
  to `tip ∩ sup_map` imported `sup_map`'s dead-branch rows without an
  "at R" constraint.

None are kill-rule or tradeoff rejections of C2's *intent*; they are
counterexamples to the *claim as frozen* ("the gate computes what the
predicate says" / "eligible set is every superseded id present at R").

## Smallest safe correction

1. `supersede_landing`: replace latest-walk-index arbitration with an
   ancestry-grounded rule, e.g. among a target's first-appearance commits pick
   the one with the newest commit date *restricted to commits whose content
   is reflected at R* — or simpler and word-faithful: keep the first-appearance
   index that is latest **in ancestry** (ancestor-descended landings only),
   making the verdict a pure function of the DAG. Then re-pin dag-2l both
   ways as selftest fixtures.
2. Compute `imm_idx`/`teaches_idx` **per commit** from that commit's own
   `commit_colmap` (parse_registry already returns it; keep tip colmap for tip
   rows). Also resets `first` snapshots to name-keyed cells.
3. Constrain `sup_map`/`superseded` to pairs whose superseding row is present
   at R (or at minimum landed on an ancestor whose row content survives
   somewhere in tip ancestry), matching "present at R" for the whole phrase.
   Decide explicitly whether "superseded id present at R" requires the
   superseding row at R and put the ruling in the predicate.

## Commands run (evidence)

- `python3 .scratch/critnewdag/build-dags.py` → `.scratch/critnewdag/runlog.txt`
  (all 9 fixtures × {v3, v2}; builds, walks, verdicts, exits as quoted above).
- `sha256sum tools/mori-sources-appendonly.py
  .ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py` +
  `git show <rev>:tools/mori-sources-appendonly.py | sha256sum` (byte identity).
- `python3 tools/mori-sources-appendonly.py --selftest` → `pass=15 fail=0`.
- `git show <sha>:corpus/SOURCES.md` dumps for dag-h {b0,h1,m}, dag-z {s1,m},
  dag-h2 {s2} — row/cell identity and the permuted `supersedes` text.
- python probe of `parse_registry`/`immutable_indices`/`imm_key` on dag-h b0
  vs h1: identical keys under h1's own colmap, different under b0's.
- `grep -rn "column|header|order|append-only|immutable" corpus/README.md
  corpus/QUALITY.md` — no rule pins the registry column order.

## Tooling

None installed. python3 + system git only.

## Bounds respected

Writes: this report (`.ufo/waves/round-40/w1/CritNewDag.md`) and
`.scratch/critnewdag/{build-dags.py,runlog.txt,repos/}` in the lane.
No fleet-repo, sibling-lane, jj-state, git-index, `.ufo/state/`, or
watchdog.log writes; no mutating git/jj in the lane repo (fixture repos are
fresh `git init` sandboxes under `.scratch/`).

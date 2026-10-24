# RevCensus — round 39 census + append-only diff (L1 mori-r39)

Target: `sources-census.sh validate` at the scored tip; registry row counts at
`13f3db7e5c7163e7ef300259ff597a42a79f81f1` (entering) and
`13bfba23b7ca063c76d3504a2ff6eb7b6a294932` (scored); per-cell append-only check
of every pre-existing row.

**Verdict: PASS on all three acceptance criteria.** Census exit 0, row delta
exactly +2 (S227, S228), zero in-place cell edits across all 226 pre-existing rows
in all 11 columns. One MEDIUM claim-integrity finding (C3's declared after-state)
and one LOW disclosure follow; neither falsifies the data append.

## Acceptance evidence

| Criterion | Result |
|---|---|
| `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` exit code | **0** |
| Rows at `13f3db7e` | **226** |
| Rows at `13bfba23` | **228** |
| Delta | **+2** (S227, S228) |
| Existing row cell edits (any column) | **0** |
| Existing row status/recheck/used-by edits | **0** |

### 1. Census exit code

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
      --root /home/vgpnk/Projects/shokunin mori
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc... across scopes
… (16 W04 lines total) …
mori	W04	S228 duplicate url docs.python.org/3/library/os.path.html across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
EXIT=0
```

Zero E-codes. `validate` emits only W04 warnings plus the `ok` line. This output
is **line-for-line identical to the round's own receipt**
`.ufo/waves/round-39/evidence/census-end.txt` (16 W04 + `ok`, `EXIT=0`) — an
independent reproduction, not a re-cite.

The file the census read is the scored tip's bytes, not a dirty worktree:

```
sha256(corpus/SOURCES.md)                                  = c993e977…4113a
sha256(git show 13bfba23:corpus/SOURCES.md)                = c993e977…4113a
git diff --stat 13bfba23 -- corpus/SOURCES.md              = (empty)
git status --porcelain -- corpus/SOURCES.md                = (empty)
```

`census` mode corroborates the count independently of the grep:
`mori rows 228`, `FLEET rows 228`, `FLEET missing 0`, exit 0.

### 2. Row counts and delta

```
$ for r in 13f3db7e… 13bfba23…; do git show $r:corpus/SOURCES.md | grep -c '^| S'; done
226
228
```

Exactly +2, matching the declared frontier (S227 gitrevisions, S228 supersedes S226).

### 3. Append-only diff

Line level:

```
$ git diff --numstat 13f3db7e 13bfba23 -- corpus/SOURCES.md
4	0	corpus/SOURCES.md
```

**Zero deletions.** Any in-place edit of an existing line produces a deletion in
`--numstat`, so a 4/0 result already excludes modified rows. Both hunks are pure
insertions:

```
@@ -232,2 +232,4 @@     +| S227 …   +| S228 …          (appended after S226)
@@ -287 +289,3 @@       +          +Round 39 bounded search — …   (prose section, outside ## Registry)
```

Structural per-id check (independent of git's diff algorithm), parsing both
revisions into `id -> [11 cells]`:

```
A rows 226 dups []  | B rows 228 dups []
header A: 11 cols   | header B: 11 cols
removed: []
added: ['S227', 'S228']
order of A is a prefix of B: True
B order tail: ['S225', 'S226', 'S227', 'S228']
existing rows with ANY changed cell: 0
status/recheck/used-by edits: 0 []
```

- No id removed, no duplicate ids, no reordering; A's 226-id sequence is a strict
  prefix of B's.
- 0/226 pre-existing rows changed in **any** column (not just the three under test).
- S226 is untouched and its immutable `anchor` cell still reads `:657-658`
  (verified byte-equal to its first sighting at `daa1d4d2`); the correction rides
  S228 as the contract requires. `S228` carries `supersedes S226` in `teaches`.
- New rows are well-formed: 11 cells each, `status=mined`, `recheck=on-release`,
  `used-by` resolving on disk (no E11 for S227/S228), inside `## Registry`
  (no E12), and no E04 (S228's URL duplicate crosses scopes, so it lands as W04).

## Findings

### MEDIUM — C3's declared after-state `superseded_as_of=[18 ids + S226 …]` is not produced by the gate

`contract.md` declares for C3:

> `supersede_timing superseded_as_of=[18 ids + S226 once S228 lands] stale_supersede=[]` at the landed tip

The gate prints **18 ids and no S226** at both revs:

```
$ tools/mori-sources-appendonly.py 13bfba23            # exit 1
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,…,S193] deleted=[] superseded=[same 18] round_changed=[]
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S069,S179,…,S193] stale_supersede=[]

$ tools/mori-sources-appendonly.py 13f3db7e            # exit 1 — byte-identical output
```

`cmp` of the two full outputs: **BYTE_IDENTICAL=yes**. This is not a stale-read
artifact — the `rev` argument is honored (`f10a320d` → 17 ids +
`stale_supersede=[S069]`; `87ec3d9` → 18 ids), and the walk is 54 commits at the tip.

Root cause, in the gate's own code:

- `tools/mori-sources-appendonly.py:301` registers the relation
  `("S226","S228")` from S228's `teaches` via `SUPERSEDES_RE` (line 69) — the
  relation *is* seen.
- `tools/mori-sources-appendonly.py:343`:
  `superseded = sorted(cid for cid in ids if cid in sup_map)` — the domain is
  restricted to `ids`, which at line 334 is *rows whose tip immutable cells differ
  from their first sighting*.
- S226 was never edited in place (first sighting `daa1d4d2`, tip row byte-equal),
  so `S226 ∉ ids`, so the S228→S226 supersession is silently dropped from both
  `superseded` and `superseded_as_of`.

Consequence: P-C9's sentence — "an id is superseded-as-of only when its latest
superseding row's landing commit is a descendant … of the commit of the id's last
immutable-cell edit" — is still not what the code computes for a cleanly superseded
row. For S226 the "last immutable-cell edit" is its creation commit `daa1d4d2`, and
S228's landing `f920eaf` is its descendant (`git merge-base --is-ancestor f920eaf
13bfba23` → true), so P-C9's words require S226 in the list; the `ids` filter
requires it absent. That is the same *words-vs-code* class the round set out to
close (r38 F1/F2), re-entering through the eligible-set definition rather than the
ancestry primitive.

Corroborating detail: the round's own receipt already records the 18-id result, not
the contract's 19 — `.ufo/waves/round-39/evidence/c9-after-lane.txt:2` says
"diff tip (v2 f920eaf7 vs r38 gate-after.txt): identical, exit 0", and
`.ufo/waves/round-38/evidence/gate-after.txt` lists the same 18 ids. So the
**receipt is honest and the frozen contract prose overclaims**; the C3 adjudicator
must either strike the `+ S226` clause or treat the gate as not yet implementing
P-C9's supersede domain. This does not affect C3's fixture-A/C ancestry verdicts,
which are what the predicate actually tests.

Related design note (no severity): appended rows can never appear in
`round_changed` — additions populate `first`, never `changed_at` — so
`round_changed=[S182,S193]` is identical at the entering and scored tips. Correct
for append-only, but it means "the data seat appended two rows" has no gate
signature at all.

### LOW — one new W04 line appears on `validate`

`census-start.txt` (entering tip) has 15 W04 lines, `census-end.txt` and my run have
16. The added line is `W04 S228 duplicate url docs.python.org/3/library/os.path.html
across scopes` — an intended consequence of S228 re-opening S226's source to carry
the corrected `:657-659` quote. It is a **warning, not an error**: the script's
header contract states W-codes never change status, and exit stayed 0 at both revs.
It therefore does not trip this seat's FAIL condition ("a new error line"), but it is
a new line on the validate output and is disclosed rather than absorbed.

### INFO — gate exit 1 is pre-existing and unchanged

`appendonly_violations` exit 1 at `f10a320d` (17 ids), `13f3db7e` (18) and
`13bfba23` (18) — the 18 historical in-place-edited ids. Adding S227/S228 changes
neither the code, nor any summary line, nor `superseded_as_of`. No regression.

## Residual risk

- **Supersede invisibility (MEDIUM above)**: S228's `supersedes S226` exists only in
  prose and as a census W04; no gate output distinguishes a superseding row from an
  ordinary appended row. A future round could land a *dangling* `supersedes S###`
  (target absent from the registry) and no instrument here would report it — worth a
  predicate conjunct in the next counter version.
- **Scope of the append check**: I verified `corpus/SOURCES.md` only, which is the
  file the census and gate gate on. The round's other write surface
  (`corpus/knowledge/gate-ancestry-r39.md`, `corpus/lessons/round-39.md`,
  `corpus/evidence/sources-r39/`) is outside this seat's target and was not audited
  for append-only semantics.
- **`round_changed` blind spot**: as noted, appended rows are structurally invisible
  to it, so parity of `round_changed` across revs cannot be read as "nothing was
  added" by other seats.

## Verification gaps (explicitly unrun)

- **Entering-tip census baseline was invalid and is discarded.** I ran
  `validate --file <scratch>/SOURCES-at-entering.md`, which emitted ~250 spurious
  E11 lines because `used-by` paths resolve relative to the file's location, not the
  lane root. I did **not** rebuild an entering-tip worktree copy (that would need a
  git worktree / mutating the read-only lane), so there is no independently re-run
  entering-tip `validate`. The "no new error line" conclusion rests on two
  independent facts that are complete without it: (a) the scored run emits **zero E
  lines**, so no E line can be new, and (b) `--numstat` is `4 0`, so no existing line
  was modified — any modified row would appear as a deletion.
- `lsp` was not used: no language server answers a Markdown registry or a
  census shell script, and the checks here are byte/CSV-structural, not symbol
  reference queries. All invocation and caller evidence is runtime command output.
- No tool installs or upgrades were performed this seat.

## Reproduction

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census  --root /home/vgpnk/Projects/shokunin mori
git -C mori-shokunin show 13f3db7e:corpus/SOURCES.md | grep -c '^| S'
git -C mori-shokunin show 13bfba23:corpus/SOURCES.md | grep -c '^| S'
git -C mori-shokunin diff --numstat 13f3db7e 13bfba23 -- corpus/SOURCES.md
python3 mori-shokunin/tools/mori-sources-appendonly.py 13bfba23 [--round-base f10a320d]
```

Scratch outputs: `.ufo/waves/round-39/scratch/RevCensus/` (`gate-tip.txt`,
`gate-entering.txt`, `g1..g3.txt`, `SOURCES-at-entering.md`).

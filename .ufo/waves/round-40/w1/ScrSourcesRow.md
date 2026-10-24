# ScrSourcesRow — S229 registry row and placement (read-only)

Seat: scribe, mori round 40 wave 1. Bounds honoured: no production edits, no
git/jj mutation, no cohort or index writes; this report is the only file
written.

Measured lane state: `git --no-optional-locks rev-parse HEAD` =
`ede486b7a09afbacfb380d5871c46a8051a6dc2e` ("round-40: repair S229 registry
placement (E12: row inside ## Registry) + commit referenced gutted-conjunct
fixture"). Entering tip `bb1f2457bb8d3e8d5dfe98488b91e8c02e378ca3`; scored tip
`265a955cc67be4eae97d2dc5a9338a25f31eb29b`. `corpus/SOURCES.md` is committed:
worktree blob `git hash-object` = HEAD blob `git rev-parse
HEAD:corpus/SOURCES.md` = `8dd82aa95ce49116e669f91aea1c28999b0c4c5d`, and
`git diff HEAD -- corpus/SOURCES.md` is empty (0 lines).

## 1. Behavior — row parse

Command (lane root):

```sh
python3 - <<'EOF'
lines=open('corpus/SOURCES.md').read().split('\n')
i_reg=lines.index('## Registry'); i_paths=lines.index('## Paths')
table=[l for l in lines[i_reg+1:i_paths] if l.startswith('|')]
hdr=[c.strip() for c in table[0].strip('|').split('|')]
rows=table[2:]; ids=[r.split('|')[1].strip() for r in rows]
...
EOF
```

Output:

```text
registry header: ['id', 'source', 'kind', 'tier', 'scope', 'anchor', 'teaches', 'status', 'opened', 'recheck', 'used-by']
ncols header: 11
row count: 229 first: S001 last: S229
S229 row index: 228 prev: S228
ncols S229: 11
'id': 'S229'
'source': 'Python execution model — Naming and binding — https://docs.python.org/3/reference/executionmodel.html#naming-and-binding'
'kind': 'docs'
'tier': 'A'
'scope': 'Python name-resolution rules for blocks: where assignment binds, and the nearest-enclosing-scope lookup a static timeout fold must model'
'anchor': '§4.2.2 Resolution of names:249-262; "When a name is used in a code block, it is resolved using the nearest enclosing scope":254-256; page fetched 2026-10-24'
'teaches': 'An assignment inside a function block binds the name locally for the whole block, so a module-map constant fold must read a function-local binding before any module-level map.'
'status': 'mined'
'opened': '2026-10-24'
'recheck': 'on-release'
'used-by': 'corpus/knowledge/conform-scope-r40.md'
line of S228: 234
line of S229: 235
blank after S229: ''
line 237: '## Paths'
```

## 2. Gates — contract-named cell verdicts

Contract anchor for this seat: `.ufo/waves/round-40/contract.md` — "Sourced
claim: C1 rests on S229 (Python execution model — naming and binding;
`corpus/knowledge/conform-scope-r40.md`), opened this round".

| cell | contract expectation | observed | verdict |
|---|---|---|---|
| kind | docs | `docs` | PASS |
| tier | A, scoped to Python name resolution | `A`; scope = "Python name-resolution rules for blocks: where assignment binds, and the nearest-enclosing-scope lookup a static timeout fold must model" | PASS |
| status | mined | `mined` | PASS |
| used-by | corpus/knowledge/conform-scope-r40.md | `corpus/knowledge/conform-scope-r40.md`; file exists and cites `source: S229`, the same URL, `verified-at: 2026-10-24`, `recheck: on-release`, and §4.2.2 with the quoted sentence | PASS |
| opened | 2026-10-24 | `2026-10-24`; anchor also says "page fetched 2026-10-24" | PASS |
| source | Python execution model — naming and binding | URL `https://docs.python.org/3/reference/executionmodel.html#naming-and-binding`; unique in `corpus/SOURCES.md` (`grep -c` = 1) | PASS |

`teaches` is consistent with `S229.src`:294-307 ("If a name binding operation
occurs anywhere within a code block, all uses of the name within the block are
treated as references to the current block… The local variables of a code block
can be determined by scanning the entire text of the block for name binding
operations.").

## 3. Gates — append-only placement

Commands and outputs (lane root):

```sh
git --no-optional-locks diff --stat bb1f2457 -- corpus/SOURCES.md
#  corpus/SOURCES.md | 1 +
#  1 file changed, 1 insertion(+)

git --no-optional-locks diff bb1f2457 -- corpus/SOURCES.md
# @@ -232,6 +232,7 @@
# [S226 row, S227 row, S228 row unchanged as context]
# +| S229 | ... |
#  <blank>
#  ## Paths
# (no removed lines)

git --no-optional-locks show bb1f2457:corpus/SOURCES.md | grep -c '^| S'
# 228
git --no-optional-locks show HEAD:corpus/SOURCES.md | grep -c '^| S'
# 229

git --no-optional-locks show 265a955:corpus/SOURCES.md | grep '^| S229 ' | sha256sum
# 4c31041cf2bd054b7fc4a2244998b5b24dc8773c91890b1c54a96a2358f54372  -
grep '^| S229 ' corpus/SOURCES.md | sha256sum
# 4c31041cf2bd054b7fc4a2244998b5b24dc8773c91890b1c54a96a2358f54372  -
git --no-optional-locks show bb1f2457:corpus/SOURCES.md | grep -c '^| S229 '
# 0
```

Verdict: at HEAD, S229 is the last table row (index 228 of 229), immediately
after S228, before the blank line at 236 and `## Paths` at 237; the table has
11 columns matching the header. The net change against the entering tip is
exactly one inserted line and zero deletions, and no existing row's cells
changed.

History note (verbatim): at the scored tip `265a955`,
`git show 265a955:corpus/SOURCES.md | grep -n S229` reports line **292**, i.e.
the row was appended after the bounded-search log and after `## Paths`, outside
the registry; commit `ede486b` moved it to line 235 inside the table. The row's
cells are byte-identical before and after the move (sha256 above).

Append-only gate corroboration:

```sh
python3 tools/mori-sources-appendonly.py HEAD --repo .
# exit=1; body (predicate + changed lines + summary + timing line) is
# byte-identical to evidence/c11-after-lane.txt lines 2-22:
#   changed S041 superseded_by=S206 ... changed S193 superseded_by=S202
#   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[...34 ids incl. S226...] round_changed=[]
#   supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226] stale_supersede=[]

python3 tools/mori-sources-appendonly.py HEAD --repo . --round-base bb1f2457
# exit=0; same 18 standing ids; deleted=[]; round_changed=[];
# same 34-id as-of line; stale_supersede=[]
```

The 18 `ids` are the standing pre-round condition: `evidence/c11-before-lane.txt`
(entering tip) and `c11-after-lane.txt` (scored tip) carry the identical list.
With `--round-base bb1f2457` the round's own change set is `round_changed=[]`
and the gate exits 0, so the placement repair registered as no immutable-cell
change. I did not rerun the gate's `--selftest` (out of this seat's scope).

## 4. Findings

**F1 — PASS (named cells and placement).** All six contract-named cells match,
and S229 is appended directly after S228 inside `## Registry` at HEAD. Net vs
`bb1f2457`: `+1` line, `0` deletions; HEAD blob equals worktree blob.

**F2 — DEFECT (anchor cell line ranges do not resolve in the named copy).**
The anchor cell says `§4.2.2 Resolution of names:249-262; "When a name is used
in a code block, it is resolved using the nearest enclosing scope":254-256`.
Measured against `corpus/evidence/sources-r40/S229.src` (868 lines, the copy
named in `corpus/lessons/round-40.md`'s Gate row):

```text
§4.2 "Naming and binding" heading .... 249
§4.2.1 "Binding of names" heading .... 251
§4.2.2 "Resolution of names" heading .. 288
§4.2.3 "Annotation scopes" heading .... 356
quoted sentence ...................... 294-295
```

The cited `249-262` lands in §4.2/§4.2.1, not §4.2.2; the cited `254-256` lands
on `<ul class="simple">` plus the "formal parameters"/"class definitions" list
items, not the sentence. The text is present and correct: §4.2.2 spans 288-355
and the sentence spans 294-295. The saved copy's own line numbering is the
lane's demonstrated convention (S227:2538-2544 = heading+sentence,
`S227.src:2542-2544` = the quote; S228:657-659 = the canonical-path paragraph,
all verified in their copies). `[INFERENCE]` The cited numbers are
self-consistent with a rendering that strips the first ~40 head lines
(288−40≈249, 294−40≈254), but no such variant copy exists in evidence. Per
`corpus/QUALITY.md` 113 ("A registry row's located-quote correction rides a
superseding row, never an in-place `anchor` edit … the gate's `anchor` cell is
immutable"), the disposition is a superseding row/erratum ruling, not an
in-place edit. This seat is read-only and did not edit the row.

**F3 — Out-of-scope observation (lesson word count).**
`corpus/lessons/round-40.md:7` labels the same quote "(15 words)". The quote is
**17** words (`len(q.split())` = 17; "When/a/name/is/used/in/a/code/block/it/
is/resolved/using/the/nearest/enclosing/scope"). The contract's ≤25-word bound
still holds, but the parenthetical number is drift of the same class as the r39
S227 18-vs-17 correction. Owning seats: `ScrLessonDraft` / `RevLessonGate`; not
edited here.

**F4 — Provenance note (scored tip vs HEAD).** The S229 row existed at the
scored tip only as a line appended after `## Paths` (line 292); the in-registry
placement verified above arrived in the later commit `ede486b`. The canonical
judge should treat "append-only placement inside `## Registry`" as true at HEAD
(net one-line insertion vs `bb1f2457`) and as false at `265a955` (row outside
the table).

**F5 — Standing lane state (not a regression).** The gate exits 1 at HEAD with
`appendonly_violations=18`, exactly the pre-existing list in
`c11-before-lane.txt`; `round_changed=[]` shows this round added none of them.

## 5. Out-of-scope items

- Lesson Gate row word count and knowledge-entry provenance review (F3;
  `RevLessonGate`, `RevKnowledgeProvenance`).
- Census re-run and W04 enumeration (`ExeCensus`, `ConnW04Routing`); the landed
  `census-end.txt` shows no S229 warning and the URL appears once in the
  registry.
- Sibling-lane overlap for the same URL (`ConnSiblingOverlap`).
- Any fix to the S229 anchor cell: read-only seat; disposition belongs to the
  canonical judge / a build seat under QUALITY 113.

## 6. Artifact paths

- This report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/w1/ScrSourcesRow.md`
- Row under test: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md:235`
- Source copy: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r40/S229.src` (§4.2.2 at 288; quote at 294-295)
- Cited knowledge entry: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/conform-scope-r40.md`
- Contract: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/contract.md`
- Receipts compared: `.ufo/waves/round-40/evidence/c11-before-lane.txt`, `c11-after-lane.txt`, `freeze-r40.txt`

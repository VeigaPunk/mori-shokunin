# mori round 36 — wave 2 — RevC2Oracle (falsify + verify, attempt 2)

Seat: `RevC2Oracle` (L1 MoriR36, wave 2). Date: 2026-10-23.
Item attacked: **the independence of the C2 receipt's real-arm oracle** —
`.ufo/waves/round-36/evidence/c2-after.txt` line `oracle:`. The attack: re-derive that
oracle block from git history alone (no counter code, no tool code, no reference code) and
compare byte-for-byte.

## Independence guarantee

This seat read NONE of: `.ufo/waves/round-36/count-c2.py`, `tools/mori-sources-appendonly.py`,
`.ufo/waves/round-36/evidence/refs/ref-c2.py`. The only inputs were (a) the frozen contract's
"C2 tool interface" definitions and (b) git plumbing on the lane repo. Scratch scripts and raw
outputs: `/fast/scratch/hyaku/mori-r36/RevC2Oracle/` (`rederive.py`, `detail.py`,
`rederive.out`, `detail.out`). Tooling installs: **none**.

## Definitions used (verbatim from `.ufo/waves/round-36/contract.md`, "C2 tool interface")

- columns by header position (id source kind tier scope anchor teaches status opened recheck used-by);
  immutable = every column but `status`, `recheck`, `used-by`; cells compared stripped;
  row identity is the id (line starting `| S` + three digits), not line position;
- `ids`: rows at `<rev>` whose immutable cells differ from the cells in the first ancestry
  commit holding that id (endpoint comparison);
- `deleted`: ids held by some ancestry commit of `<rev>`, absent at `<rev>`;
- `superseded`: ids in `ids` for which a row at `<rev>` has a teaches cell opening
  `supersedes S###`;
- `round_changed`: ids whose immutable cells changed, or which were deleted, in any commit in
  `BASE..<rev>` touching the path (per-commit; changed-back ids listed);
- `appendonly_violations` = len(ids) + len(deleted).
Rev `6bd57097f7ab2b471b4593ed2019c980b1368c68`, round base `f10a320d9056d19a6d007420df49d7b16a3bf857`.

## Measurements (command → observed output)

**M1 — the attacked oracle block.** `read .ufo/waves/round-36/evidence/c2-after.txt`:
```
real arm: pass (0.2s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=15440749816798970567
```

**M2 — receipt identity (frozen counter).**
`sha256sum .ufo/waves/round-36/count-c2.py .ufo/waves/round-36/count-c1.py` →
count-c2.py `c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34`,
count-c1.py `86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0` — both equal the
`evidence/freeze-v2.txt` pins (`c7edaacf…`, `86dd3b7a…`). The receipt is a receipt of the frozen
counter bytes.

**M3 — contract pin drift (checked, not a defect).** Worktree `contract.md` hashes
`065a17b5…` ≠ freeze pin `dbd3f6d7…`. Trace
(`git rev-list bf0df77 -- .ufo/waves/round-36/contract.md` + per-commit sha256): pin held at
`c1a026cb` ("C0 control receipts"), amended by `5842dc04` ("C1 declared exploratory before
data"), `+14 insertions(+)` only (declaration section). P-C2 sentence bytes:
`git show <c>:contract.md | grep '^P-C2:' | sha256sum` → `5bfa852c…` identical at `c1a026cb`,
`5842dc04` and `bf0df77`. The frozen predicate sentence is unchanged; the amendment is the
contract's own documented C1-exploratory declaration. No defect.

**M4 — independent re-derivation at rev 6bd57097 (the attack).**
`python3 /fast/scratch/hyaku/mori-r36/RevC2Oracle/rederive.py` →
```
== rev 6bd57097f7ab  commits=47  rows_at_rev=204  range_commits=['8d56809', 'ff33407', '406d91a', 'cedb0ec']
MY  ORACLE : appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
RECEIPT    : appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
MATCH
```
**Byte-identical match.** The receipt's oracle is fully reproducible from git history under the
frozen definitions, without the counter.

**M5 — same derivation at the landed tip bf0df77 (diagnostic).**
```
== rev bf0df77fee4b  commits=48  rows_at_rev=220  range_commits=[… 'bf0df77']
MY  ORACLE : … superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] …  (ids/deleted/round_changed unchanged)
```
bf0df77 appends S205–S220 whose teaches open `supersedes <id>` for the remaining 15 in-place-edited
ids, so at bf0df77 `superseded` = all 18. The receipt's `tool:`/`oracle:` lines show the
3-entry value ⇒ the receipt's real arm ran at the predicate-pinned rev **6bd57097** — exactly what
the frozen P-C2 sentence specifies ("on the lane's own history (rev 6bd57097, round base
f10a320d)"). Consistent, not a defect (see Residual risk ii).

**M6 — saturation of `deleted=[]`.** In the same run: 47 path commits walked
(`git rev-list --reverse --topo-order 6bd57097 -- corpus/SOURCES.md`), `git rev-list --merges …
| wc -l` → `0` (linear history), `diff <(git log --follow --format=%H -- PATH) <(git log
--format=%H -- PATH)` → `FOLLOW==PLAIN` (no rename; --follow adds nothing). `detail.py`:
`ids ever held=204  ids at rev=204  deleted=[]` — every id ever held at the path is present at
6bd57097; `deleted=[]` is saturated, not vacuous. Parser row count (204) equals the raw
`grep -cE '^\| *S[0-9]{3}'` count; no escaped pipes (`grep -cF '\|'` → `0`), no space-less rows,
single header at line 5.

**M7 — round_changed provenance (per-commit diffs in f10a320d..6bd57097 touching the path).**
`detail.py` detail: `[(‘8d56809’, ‘S182’, ‘changed’), (‘406d91a’, ‘S193’, ‘changed’)]` —
- S182 anchor widened in `8d56809` (`block/genhd.c:1371-1374,1395,1403` →
  `:1353,1371-1374,1395,1403,1418-1425 (diskstats_show, …)`), SOURCES.md:188 at 6bd57097;
- S193 anchor widened + teaches scoped in `406d91a`
  (`drivers/base/core.c:3508-3510,3542-3543` → `…,4653-4657`), SOURCES.md:199.
Correctly absent: `ff33407` (used-by only — mutable column), `cedb0ec` (appends S199–S204, new
ids are not "changed"), `bf0df77` (append of S205–S220, outside this range).

**M8 — the 18 ids are real in-place edits (endpoint vs first-hold).** First-hold commits and
changed immutable cells (from `detail.py`; line numbers at 6bd57097): S041:47 & S044:50
(first `273aa74`, teaches rewritten), S051:57 & S062:68 (`daceeec`, teaches), S064:70
(`367927c`, scope+teaches), S069:75 (`8f8c58e`, teaches), S179:185 (`55c3ed5`, scope+teaches —
the round-32 reject-reason rewrite), S180:186, S181:187, S182:188, S183:189, S184:190,
S185:191, S186:192, S188:194, S189:195, S190:196 (first `62db24c` — the round-33
iostat-anchor repairs: anchor/scope/source/teaches widenings), S193:199 (`8d56809`).
`superseded` cross-check: 19 tip rows open `supersedes S###` (S073→S069, S074→S071, S075→S070,
S076→S067, S087→S083, S088→S084, S133→S124, S143→S090, S144→S093, S145→S096, S146→S097,
S147→S101, S148→S127, S149→S128, S150→S129, S151→S131, S152→S140, S201→S182, S202→S193);
exactly the three whose targets are also in `ids` — S069, S182, S193 — enter `superseded`.
The 16 superseded-only targets are byte-stable since first hold. Semantics separate cleanly.

**M9 — the oracle is not a function of the tool (behavioral corroboration).**
`evidence/c0-rescore-v2.txt` (frozen counter `c7edaacf…`, five independent runs): the oracle
block is the identical 18-id line in every run while the substitute tools print different
values (J1 empty, J10 id-pattern-keyed, J11 path-gated empty, J12 mutable-only) and are scored
`unmet` against it; blind-arm `want:` truths come from op logs (`repoNN want: …` blocks), never
from a tool. An oracle echoing the tool under test could not discriminate those controls.

## Findings

No defect found. The attack on the oracle's independence **fails**:
1. The oracle block reproduces byte-identically from `git log`/`git show` history alone under
   the frozen contract definitions (M4), including the witness requirements ("lists at least
   one id" — 18 ids).
2. Every list is saturated and traceable: `deleted=[]` over 204 ids ever held (M6),
   `round_changed` tied to specific commits and cells (M7), all 18 `ids` are real immutable
   in-place edits with named first-hold commits (M8), `superseded` is exactly
   `ids ∩ superseder-targets` (M8).
3. Receipt identity holds: frozen counter sha (M2), frozen predicate sentence bytes unchanged
   across the post-freeze contract amendment (M3), real arm at the predicate-pinned rev (M5).

## Residual risk and verification gaps

- (i) This seat verifies the oracle's values and derivability, not the counter's internals;
  reading `count-c2.py` would break the independence the seat exists to establish. The
  independence is corroborated behaviorally (M9) and by reproduction (M4), not cryptographically.
- (ii) Scope of the receipt's real arm: per the frozen P-C2 sentence it exercises the tool
  against the 6bd57097 history. M5 shows the true oracle at the landed tip bf0df77 differs in
  `superseded` (all 18, after S205–S220). The receipt therefore does not witness tool-vs-oracle
  agreement on the bf0df77 history; that configuration is simply not what P-C2 pins. Flagged as
  an observation for the integrator, not a defect.
- (iii) Parsing assumptions verified empirically (single header, no escaped pipes, no
  space-less rows, 0 merges, `--follow` ≡ plain). A differently-keyed implementation could in
  principle disagree on pathological inputs; none exist at these revs.

Tooling installed: none. Lane repo untouched except this report file.

VERDICT: PASS (no defect found)

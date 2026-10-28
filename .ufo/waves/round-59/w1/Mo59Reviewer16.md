# Mo59Reviewer16 — fixture-coverage gap analysis (C1 fixtures ×13, C2 trees ×12)

Adversarial finding: **counterexample found** — three constructions (one C2 entry
arm, one C2 claim/row semantics, one C1 pointer arm) green the frozen counters at
HEAD while violating the predicate/contract they were frozen to enforce. All
proofs run read-only against the lane (git show / cat-file / ls-tree only);
fixtures materialized under `/fast/scratch/hyaku/mori-r59/Mo59Reviewer16/` and
removed after run. Receipt preserved below.

Scope note: HEAD now carries the landed C2 data (`be737211`, `7b86704d` —
entry, copies, S553–S560) and the frozen tools at their pins. Baselines:
`count-c1.py HEAD` → `C1=met …` rc 0; `count-c2.py HEAD` →
`C2=met … claims=13 files=6` rc 0. The gaps below are therefore *live*: a
defective landing in the covered class scores green today.

## The three most dangerous gaps

### D1 (C2, real entry arm): `grammar:` reasons are filtered out — a landed entry may contain the exact lines hostile tree t12 must reject

`count-c2.py:303-305` derives the real-arm verdict by prefix-filtering
`eval_entry` reasons:

```
entry_ok = not any(r.startswith(("frontmatter", "distinct", "claims_min",
                                 "files", "span", "entry_absent")) for r in reasons)
rows_ok  = not any(r.startswith("rows") for r in reasons)
pins_ok  = not any(r.startswith("pin") for r in reasons)
```

`"grammar:"` is in none of the three groups; `entry_ok_all` (line 300) is
computed and discarded. The hostile-tree arm (`:339-358`) instead uses raw
`ok` — so t12-malformed-claim must evaluate false, while the *same line inside
the shipped entry* leaves `met` intact. No fixture/tree exercises "valid entry
+ one malformed claim line", so this asymmetry is untested.

Proof (HEAD entry + one appended bad line, scratch tree):

```
M1 malformed line in real entry: eval_entry ok=False
   grammar_reasons=['grammar:- **K99** — broken line, no span, no pin']
   | real-arm entry_ok=True rows_ok=True pins_ok=True
```

Frozen predicate says "…>=10 claims in the frozen grammar…" — it never says
*only* claims match the grammar. An entry with 10 clean claims plus arbitrary
K-marked garbage reads clean to reviewers and scores `entry=ok`. Same blind
spot applies to any future reason class added to `eval_entry`.

### D2 (C2, claim/row semantics): "distinct claims" enforces only distinct K-ids; sid↔file binding absent; row content unbound — zero-information green is reachable

Contract C2 requires "≥10 byte-exact pin-bound claims" that are (per the routed
defect) *distinct claims*, with "the registry rows those claims cite" — "one
per cited artifact copy" (§2b). The counter enforces:

- `distinct:` only on the K-id (`count-c2.py:125-127`) — ten claims with
  identical quote/text under different K-ids pass;
- `files = sorted({c[2] ...})` counts cited files but never binds a cited file
  to a source row (`:132`, `:163`, `:172`); `sids` is a flat bag over
  frontmatter lines — one `source:` line covers all six artifact copies, and an
  extra row for an *uncited* artifact (S559, landed) is equally accepted;
- row cells except `[7]=="mined"` and `[10]==ENTRY` are unchecked (`:183-188`):
  title, type, tier, sha, and the row's own locator may be fabricated.

Proof (synthetic tree): 10 byte-identical claims `"seats": 64,` line 5 over
r55/r56/r57 + one 3-byte offset fragment `"la` at offset 3 + a single
`source: S553` + an S553 row with `paper | Z | bogus scope | no artifact
named, wrong sha deadbeef | fabricated`:

```
M2+M3: eval_entry ok=True claims=11 files=3 reasons=[]
   | entry_ok=True rows_ok=True pins_ok=True
```

An entry with near-zero information content, one doctored registry row, and no
row↔artifact correspondence meets every gated arm. This is the same defect
class as routed defect 2 (S552 duplicate/fabricated row) — the counter cannot
see it.

### D3 (C1, pointer arm): "every backticked evidence path resolves under R" is `git cat-file -e` — object-type blind, existence-only; counter materializes the pointer into a file on pass 2

Counter real arm (`count-c1.py:186-194`): the tool's reported pointers are
checked with `git cat-file -e rev:path` (rc 0 for **any** object type —
`git cat-file -e HEAD:tools` → rc 0 on a *directory*), then
`materialize(repo, rev, [rel2], proot)` writes `git show` output to a **file**
at that path; the tool is then re-run and `Path(root)/rel).is_file()`
(`tools/mori-register-check.py:185`) now sees the laundered file. Fixtures
cover pointers that are missing/absolute/`..`/empty (f05/f06/f07/f13) — none
covers a pointer that *resolves but is not a file* or *resolves to the wrong
bytes*, so this class is unexercised.

Proof: register row 0 evidence cell `` `tools` `` (a directory pointer). Raw
first-pass run → `pointers:missing=tools`; after writing a file whose bytes are
the git tree listing (exactly what `git show rev:tools` produces):

```
M4 full-green check: ok=True reasons=[]
   bound={…832…[0]: 'alpha bind (does a)', …}
   counter pointer predicate: git cat-file -e HEAD:tools rc=0
```

Two companion holes in the same arm, same proof tree:
(a) name binding accepts any non-alnum/non-underscore suffix
(`mori-register-check.py:168-171`): register name `alpha` bound to manifest
entry `alpha bind (does a)` — fixtures f08/f09 mutate the *manifest* side only;
scorecard-side truncation is never tested, so "exact name binding" is really
"register name is a word-boundary prefix of the manifest entry".
(b) rows keyed outside `REQUIRE` are never looked up (`:141` `keymap.get`):
the forged row `rounds[999].capabilities_added[0] | phantom cap` produced zero
reasons — `keys:duplicate` (f03) is the only extra-row check; a fabricated
capability key rides the register green.

## Secondary gaps (enumerated, not in top-3)

- **Expect-prefix collapse (both counters)**: `matched`/`expect` coverage is
  `any(r.startswith(e))` (count-c1.py:158, count-c2.py:352). f11 expects
  `manifest` — satisfied by *any* `manifest:*` reason; t06 expects `files` —
  satisfied by `files_min` as well as `files:outside`; t03/t11 both expect
  `span` though they are different defect classes; t04 `pin` covers
  `pin:copy_absent` too. A mis-built fixture that fails for the wrong reason
  still "covers" its token — the tree cannot detect its own mislabeling.
- **C1 empty-expect asymmetry**: a fixture with empty `expect.txt` demands only
  exit≠0/¬REGISTER_MET (fails for any reason); in C2 empty expect *requires
  ok=True* (positive control). The two arms use opposite semantics for the same
  file — a trap for future fixture authors, currently unused.
- **`.py`-suffixed fixture dirs silently skipped** (`count-c1.py:127`
  `dirs = [n for n in names if not n.endswith(".py")]`): a hostile dir named
  `f14-x.py/` is never run; the skip is by name suffix, not file type.
- **Drift arm is crash-blind** (`count-c2.py:260` `drift_ok = p.returncode != 0`):
  any nonzero exit — including `reasons=[unreadable]`/crash — counts as
  "schema drift detected". The arm proves the scanner fails on r53, not that it
  *recognizes* the drifted member key set (verified: scanner on a nonexistent
  path exits 1).
- **Scan arm trusts tool-computed `members`**: `members==seats` compares two
  numbers the pinned tool itself emits (`scan:106`); file-count == 5 is not
  checked (an empty `files` list would still pass `all(...)` if verdict were
  OK — prevented only because verdict requires `files` nonempty). The tool
  also validates `lane`/`wave` only as nonempty strings — an artifact for a
  foreign lane scans OK.
- **C1 `keys:short_row` / `manifest:entry_missing` / `manifest:index_missing`
  reason classes have no fixture** (f11's broad `manifest` token would catch
  only by prefix collapse); `binding:declared_register` beyond n_decl∈{0,2}
  variants is thin.
- **Frontmatter keys need not be a YAML block** — any four lines with the
  prefixes in the first 10 lines count; values are unchecked (`x` suffices).
  Contract-conformant, noted for completeness.
- **Negative offset accepted** for `offset` claims (int parse, no ≥0 check);
  `fb[n:n+len(q)]` still compares bytes, so low risk.
- **SID duplicate shadowing**: ROW matches the *first* table row per sid
  (`count-c2.py:172-179` `break`) — an earlier shadow row could mask a bad
  canonical row. Externally mitigated: `scripts/sources-census.sh` E03 fails
  the round on duplicate ids, so it cannot ride to closure; still uncovered by
  the counter itself.

## Method (bounded)

1. Read frozen contract + both counters in full; extracted the gated reason
   prefixes, the expect-prefix coverage rule, fixture/tree inventories, and the
   real-arm pointer protocol.
2. Read both frozen tools in full (register-table scan, `pointer_ok`, name
   boundary rule, member-key validation) to enumerate the *space* of
   constructions the fixtures/trees were chosen to bound.
3. Built a gap table (tool/counter check × fixture mutation) — every check
   with no fixture or with only prefix-collapsed coverage is a candidate.
4. Empirically confirmed candidates with synthetic trees under scratch:
   imported `eval_entry`/`check` from the pinned bytes; mutated the landed HEAD
   entry; exercised `git cat-file -e`/`git show` semantics. Commands:
   `python3 proofs.py`, `proofs2.py`, `proofs3.py` (scratch); baselines
   `count-c1.py HEAD` / `count-c2.py HEAD`.
5. Ranked by: does the construction violate a *stated* predicate/contract
   clause (not just semantics), is it reachable this round (entry/rows land
   now), and is there an external gate that would catch it (census catches
   D-dup, so demoted).

## Receipt

```
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=HEAD            (rc 0)
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=HEAD (rc 0)
P0 baseline landed entry: eval_entry ok=True claims=13 files=6 reasons=[]
M1 malformed line in real entry: eval_entry ok=False grammar_reasons=['grammar:- **K99** — …'] | entry_ok=True rows_ok=True pins_ok=True
M2+M3: eval_entry ok=True claims=11 files=3 reasons=[] | all arms green (10 identical claims, 1 sid, junk row, 3-byte offset quote)
M4a dir-pointer unmaterialized: pointers:missing=tools …  |  M4 materialized: ok=True reasons=[] bound={832[0]:'alpha bind (does a)',832[1]:'beta probe (does b)'}
M4c git cat-file -e HEAD:tools rc=0
M6 scanner /nonexistent: rc=1  (satisfies count-c2.py:260 drift_ok)
```

Scratch `/fast/scratch/hyaku/mori-r59/Mo59Reviewer16/` cleaned post-run. No
production, registry, SCORECARD, LOG or VCS writes; lane reads were
git-show/cat-file/ls-tree only.

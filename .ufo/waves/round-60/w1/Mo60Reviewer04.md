# Mo60Reviewer04 — no-false-negative audit of the hardened entry-claims verifier

Seat: Mo60Reviewer04 (reviewer, w1). Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Freeze revision `ac496c7cde8cad965079858accae3bedfe4a73f2`; entering
`ddfb12fb0838b4307c445194a844f0c4b1950195`. Lane tip observed at start and end of this
seat: `b3c256138f00c704d5aa56eb0332d74506502ef2` (moved, as the brief warned).
All work read-only over the lane; scratch
`/fast/scratch/hyaku/mori-r60/Mo60Reviewer04/` (created with `mkdir -p`, `TMPDIR` set there),
cleaned before yield. No commits, no lane VCS mutation, no fleet/sibling writes.
No subagents dispatched (leaf member).

## Scope and method

Audit target: `tools/mori-entry-claims-check.py`, pinned blob
`cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69`
= `PIN_EC` in `.ufo/waves/round-60/count-c2.py:48`. Verified the pinned blob is byte-identical
at both the entering revision and the freeze revision:

```
$ git show ac496c7c:tools/mori-entry-claims-check.py | sha256sum
cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69  -
```

Method (matching the C2 entry arm in `count-c2.py:290-333`): materialize `ENTRY`, `SOURCES`
and the six `ARTIFACTS` copies with `git show ac496c7c:<rel>`, then execute the **pinned tool
bytes** (dumped from git, not read from the working tree) with
`--min-claims 10 --min-files 3` and the counter's `ARTIFACTS` JSON.

## 1. Baseline — verdict reproducible at the freeze revision

```
$ python3 ec-pinned.py --root root --entry corpus/knowledge/wave-settlement-artifacts-r59.md \
    --registry corpus/SOURCES.md --artifacts-json artifacts.json --min-claims 10 --min-files 3
{"schema": "mori-entry-claims-v2", "ok": true, "reasons": [],
 "stats": {"claims": 13, "files": 6, "spans": 13, "min_span": 12}}
exit=0
```

**Matches the seat requirement exactly: `ok`, claims=13, spans=13, files=6.** Materialized
copy hashes for reproducibility (six copies + entry + registry):

```
ea48a0cc…9335f  corpus/evidence/sources-r59/w1-results-r54.json
2e5b0a0f…6d9763b  corpus/evidence/sources-r59/w1-results-r55.json
19536201…1e5d761  corpus/evidence/sources-r59/w1-results-r56.json
29e7a35d…27675669beb1  corpus/evidence/sources-r59/w1-results-r57.json
a57b660d…5fb7ec61fc  corpus/evidence/sources-r59/w1-results-r58.json
b259e73c…b4f0b5588  corpus/evidence/sources-r59/w1-settlement-r58.json
441a751d…4716ce21  corpus/knowledge/wave-settlement-artifacts-r59.md
46c333d2…fe30b2d63  corpus/SOURCES.md
```

Pinned tool selftest, same blob:

```
$ python3 ec-pinned.py --selftest
ENTRYCLAIMS_SELFTEST pass=13 fail=0
exit=0
```

## 2. The three required benign mutations — all stay `ok`

Each mutation applied to an independent `cp -a` copy of the materialized root; identical
invocation each time.

| # | mutation | result | exit |
|---|---|---|---|
| M1 | fixed a typo in claim text K13 (`…totals record 26 partial waves.` → `…partial wave counts.`) | `ok`, claims=13 spans=13 | 0 |
| M2 | reordered two claim lines (swapped K1↔K2, entry lines 25/26) | `ok`, claims=13 spans=13 | 0 |
| M3 | appended one prose paragraph (`## Provenance note`, 3 lines, no citation) | `ok`, claims=13 spans=13 | 0 |

```
=== m1 ===  {"schema":"mori-entry-claims-v2","ok":true,"reasons":[],"stats":{"claims":13,"files":6,"spans":13,"min_span":12}}  exit=0
=== m2 ===  {"schema":"mori-entry-claims-v2","ok":true,"reasons":[],"stats":{"claims":13,"files":6,"spans":13,"min_span":12}}  exit=0
=== m3 ===  {"schema":"mori-entry-claims-v2","ok":true,"reasons":[],"stats":{"claims":13,"files":6,"spans":13,"min_span":12}}  exit=0
```

**Seat requirement satisfied: no false rejection on any of the three benign mutations.**

Two further benign variants I added (both pass, strengthening the no-false-negative result):

| # | mutation | result |
|---|---|---|
| C1 | added a 14th genuinely valid claim (K15, r54 member[0] `agent`, line 9, correct pin) | `ok`, claims=14 spans=14, exit 0 |
| E1 | reversed the order of **all** 13 claim lines | `ok`, claims=13 spans=13, exit 0 |

Claim order is therefore fully immaterial to the verdict, and legitimate entry growth is not
penalized (H3's "pairwise distinct" check is per-text, not order-sensitive).

## 3. Findings

### F1 (MEDIUM) — H4 per-copy binding is satisfied by ONE registry row naming every artifact; the routed r59 defect is not closed in general

`tools/mori-entry-claims-check.py:224-238` marks a copy as bound when `any(art in b for b in binders)`,
where `binders` is every mined row whose used-by cell equals the entry. Substring membership,
not a one-row-per-copy association. The docstring at `:20-22` and the contract both state the
defect H4 closes as *"r59: one fabricated row could cover every copy"* — precisely the shape
that still passes.

Construction (root `a1`): keep exactly **one** `source:` frontmatter line (`S553`), and make that
single registry row's source cell (cell `[1]`) name all six `.ufo` artifact paths.

```
$ grep -c '^source:' a1/corpus/knowledge/wave-settlement-artifacts-r59.md   → 1
$ grep -c '^| S[0-9]* |' a1/corpus/SOURCES.md                              → 1
$ python3 ec-pinned.py --root a1 --entry … --registry corpus/SOURCES.md \
    --artifacts-json artifacts.json --min-claims 10 --min-files 3
{"schema": "mori-entry-claims-v2", "ok": true, "reasons": [],
 "stats": {"claims": 13, "files": 6, "spans": 13, "min_span": 12}}
exit=0
```

One committed row covers all six cited copies and the entry still verifies. The hostile tree
set does not cover this case: `trees-c2h/h07-single-row` keeps **four** `source:` lines
(S901–S904) with only S901 present, so it fails on `rows:missing=S902..S904` plus
`rows:binding=` for the three copies S901 does not name. It tests "one row names one copy",
never "one row names all copies".

```
$ python3 ec-pinned.py --root trees-c2h/h07-single-row …   # expect.txt: rows:binding
{"ok": false, "reasons": ["rows:missing=S902","rows:missing=S903","rows:missing=S904",
 "rows:binding=corpus/evidence/sources-r59/w1-results-r55.json",
 "rows:binding=corpus/evidence/sources-r59/w1-results-r56.json",
 "rows:binding=corpus/evidence/sources-r59/w1-results-r57.json"], …}
```

Scope note (deliberately not overclaimed): the **frozen C2 predicate** ("every cited copy
binds to a mined used-by-exact registry row whose source cell names the copy's `.ufo`
artifact") is literally satisfied by this construction, so this does **not** flip `C2=met`.
What it shows is that the predicate is weaker than the defect statement attached to it, and
that no frozen tree instantiates the defect as worded. If H4 is meant to close
"one fabricated row covers every copy", it needs either a 1:1 row↔copy requirement, a
minimum `source:`-line count tied to `len(cited_copies)`, or an exact-path (token-delimited)
match instead of `art in b`.

### F2 (LOW) — H1 over-blocks benign prose that mentions a claim id in bold

`tools/mori-entry-claims-check.py:114`:

```python
if "**K" in ln or (ln.lstrip().startswith("-") and "Quote:" in ln):
```

The first disjunct fires on any line containing the literal substring `**K`, not only on
claim-shaped lines. The contract defines H1 as *"Any claim-shaped line that fails the frozen
CLAIM regex makes the entry fail"*; a prose cross-reference is not claim-shaped, yet is
rejected.

```
# B1: append one prose line
"See **K1** for the seats field and **K12** for the scanner schema."
$ python3 ec-pinned.py --root b1 …
{"ok": false, "reasons": ["grammar:See **K1** for the seats field and **K12"],
 "stats": {"claims": 13, "files": 6, "spans": 13, "min_span": 12}}
exit=1
```

A closely related variant (F2b), a prose bullet that uses the word "Quote:":

```
# F1: append "- Quote: extraction is not byte-stable across JSON escaping; …"
{"ok": false, "reasons": ["grammar:- Quote: extraction is not byte-stable a"], …}  exit=1
```

F2b is defensible (a bullet containing `Quote:` is claim-shaped by the format's own grammar).
F2 proper is not: it penalizes ordinary prose that references `**K1**`/`**K12**`, which the real
entry already does in plain form in its Limits section ("K1–K5 and K8–K10 are line-exact…").
The failure mode is a silent style constraint on authors with an opaque `grammar:` reason
pointing at prose. Suggested narrowing: require the line to also look claim-shaped
(`"Quote:" in ln`) before the `**K` disjunct fires.

## 4. Stability under the lane moving during the wave

The brief requires pinning re-derivations because C1 data lands during this wave. The entry's
cited bytes are unchanged across all three revisions, but the registry is **not**:

```
ac496c7c  entry=441a751de67f1cef  sources=46c333d2e90fbc61
ddfb12fb  entry=441a751de67f1cef  sources=46c333d2e90fbc61
b3c25613  entry=441a751de67f1cef  sources=e8bda4a85241e9cf   ← drifted
```

`git diff ac496c7c b3c25613 -- corpus/SOURCES.md` = `1 file changed, 4 insertions(+)`, appending
only S561–S564 (the r59 own-work attack rows). Rows S553–S559 are byte-identical at both
revisions (checked per-id with `git show … | grep "^| S55x |" | sha256sum`; all `same_bytes=YES`).

Re-running the entry arm with the **tip** registry and the freeze entry/copies:

```
{"ok": true, "reasons": [], "stats": {"claims": 13, "files": 6, "spans": 13, "min_span": 12}}  exit=0
```

So the C2 entry verdict is stable across the registry drift this wave is producing. Residual
fragility worth noting: `rows` lookup at `:203-207` `break`s at the **first** row matching a
sid, so a duplicate S553 row inserted *above* the real one would be the one validated. No such
duplicate exists at any of the three revisions.

## 5. Residual risk and verification gaps

- **Not exercised here (out of seat scope):** the G1 toolgate / G2 containment / G3 expectgate
  arms and the H5 drift arm live in `count-c2.py`, not in the verifier. I did not score C1 or
  C3, and this report asserts nothing about them.
- **A1 is a construction, not a lane finding:** no committed entry currently has this shape.
  It bounds the verifier's guarantee, not the honesty of `wave-settlement-artifacts-r59.md`
  (whose 13 claims re-derive `ok` and whose copies are sha-pinned in the entry itself).
- **Substring binding is untested for path-prefix collisions:** `.ufo/waves/round-54/w1-results.json`
  is a prefix of any hypothetical `…/w1-results.json.bak`; `art in b` would accept the longer
  path as binding the shorter artifact. Not reachable from the current `ARTIFACTS` map.
- **H2 `MIN_SPAN=8` rejects legitimate short quotes** (e.g. a `seats` token); that is
  contract-mandated, so recorded as design, not defect.
- Verification environment: all runs read-only; sandbox roots under scratch only. `disk-guard.sh
  status` green before and after (596.1G free on `/fast/scratch/hyaku`). No tool installs were
  needed or performed.

## 6. Verdict

The hardened verifier is **sound for the three required benign mutations** (M1, M2, M3 → `ok`,
claims=13 spans=13) and for the two extra benign variants (C1, E1). The seat's stated
acceptance condition is met. Two defects remain on the record: **F1 (MEDIUM)**, H4's per-copy
binding admits a single row covering every copy — the defect it names as closed — while the
frozen C2 predicate still reads met; and **F2 (LOW)**, H1's `**K` substring disjunct rejects
benign prose. Neither is a met-flip for C2 as frozen; both should be carried into the next
instrument-hardening round.

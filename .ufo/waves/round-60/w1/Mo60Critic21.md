# Mo60Critic21 — cheapest-met attack on C2: the hardened verifier still admits a semantically empty entry

Seat: Mo60Critic21 (critic, leaf). Assignment: rebuild Mo59Critic22's
semantically-empty construction (ten `x.` claims, one repeated span, fabricated
row) against the NEW `tools/mori-entry-claims-check.py`; ok=true on any variant
is a kill. Frozen contract read first
(`.ufo/waves/round-60/contract.md`, freeze `ac496c7c`, entering `ddfb12fb`).
Work was read-only on the lane; nothing outside the seat scratch and this file
was written.

**Verdict: KILL — the pinned tool returns `ok: true`, exit 0, on a variant with
zero evidential content, and the frozen `count-c2.py` prints `C2=met` on a
sandbox commit whose r59 entry path holds it.** The exact r59 bytes are now
rejected (control below); the class was converted into three trivial textual
edits, not closed.

## Pins verified at the freeze revision

| object | evidence |
|---|---|
| `ac496c7cde8cad965079858accae3bedfe4a73f2` | `git show AC:tools/mori-entry-claims-check.py \| sha256sum` → `cffe9f33…e6e69` = PIN_EC (`count-c2.py:51`) |
| pinned counter | `git show AC:.ufo/waves/round-60/count-c2.py \| sha256sum` → `8c4814f5…df976`; worktree byte-identical |
| copies | extracted with `git show AC:<artifact>`; each lane copy at `corpus/evidence/sources-r59/` byte-equals its `.ufo` artifact (checked by sha) |
| tool executed | scratch copy of the AC blob, sha `cffe9f33…e6e69` (`sha256sum` before each run) |

The scratch copy was used, not the working tree, so a moving lane tip cannot
change the bytes under test.

## Counterexample — exact entry bytes that score `ok=true`

Entry path `corpus/knowledge/wave-settlement-artifacts-r59.md`
(sha256 `6333a96f4422aeee99e4abbdf6aee88b1e5ddb89f120e80da41c043e19fc632d`):

```
source: S901 — committed artifact `.ufo/waves/round-54/w1-results.json` (copy `corpus/evidence/sources-r59/w1-results-r54.json`)
verified-at: 2026-10-28
recheck: 90d
coverage-map: Core — wave settlement artifact shape

- **K1** — Vacuous filler statement number 01. Quote: ` "lane": "m` (corpus/evidence/sources-r59/w1-results-r54.json:offset:2; pin ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f)
- **K2** — Vacuous filler statement number 02. Quote: ` "lane": "mo` (corpus/evidence/sources-r59/w1-results-r54.json:offset:2; pin ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f)
- **K3** — Vacuous filler statement number 03. Quote: ` "lane": "mor` (corpus/evidence/sources-r59/w1-results-r54.json:offset:2; pin ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f)
- **K4** — Vacuous filler statement number 04. Quote: ` "lane": "mori` (corpus/evidence/sources-r59/w1-results-r54.json:offset:2; pin ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f)
- **K5** — Vacuous filler statement number 05. Quote: ` "lane": "mori"` (corpus/evidence/sources-r59/w1-results-r55.json:offset:2; pin 2e5b0a0f94d1fa5b90b2804d370db87d25d5197fa65bc4f26441d939b8d9763b)
- **K6** — Vacuous filler statement number 06. Quote: ` "lane": "mori",` (corpus/evidence/sources-r59/w1-results-r55.json:offset:2; pin 2e5b0a0f94d1fa5b90b2804d370db87d25d5197fa65bc4f26441d939b8d9763b)
- **K7** — Vacuous filler statement number 07. Quote: `"lane": "m` (corpus/evidence/sources-r59/w1-results-r55.json:offset:3; pin 2e5b0a0f94d1fa5b90b2804d370db87d25d5197fa65bc4f26441d939b8d9763b)
- **K8** — Vacuous filler statement number 08. Quote: `"lane": "mo` (corpus/evidence/sources-r59/w1-results-r56.json:offset:3; pin 19536201a689c954899a2e6decf322ef2c5f3d2ed9bc8ddb75229636b1e5d761)
- **K9** — Vacuous filler statement number 09. Quote: `"lane": "mor` (corpus/evidence/sources-r59/w1-results-r56.json:offset:3; pin 19536201a689c954899a2e6decf322ef2c5f3d2ed9bc8ddb75229636b1e5d761)
- **K10** — Vacuous filler statement number 10. Quote: `"lane": "mori` (corpus/evidence/sources-r59/w1-results-r56.json:offset:3; pin 19536201a689c954899a2e6decf322ef2c5f3d2ed9bc8ddb75229636b1e5d761)
```

Registry (sha256 `3662cbd5b27577cb29f8d40a850f70948b08d3aeb4d491669545e41b64c4ff89`);
one fabricated row, appended to the real `corpus/SOURCES.md`:

```
| S901 | adversarial fabricated row - cites nothing real; paths: .ufo/waves/round-54/w1-results.json .ufo/waves/round-55/w1-results.json .ufo/waves/round-56/w1-results.json | own-work | A | scope | anchor | teaches | mined | 2026-10-28 | 90d | corpus/knowledge/wave-settlement-artifacts-r59.md |
```

Artifacts mapping is the counter's `ARTIFACTS` (`count-c2.py:59-70`) unchanged.

Command and output (scratch, `TMPDIR` set to it):

```
python3 <scratch>/tool/mori-entry-claims-check.py \
  --root <scratch>/roots/v6-sliding-window \
  --entry corpus/knowledge/wave-settlement-artifacts-r59.md \
  --registry corpus/SOURCES.md \
  --artifacts-json <scratch>/roots/v6-sliding-window/artifacts.json \
  --min-claims 10 --min-files 3
{"schema": "mori-entry-claims-v2", "ok": true, "reasons": [], "stats":
 {"claims": 10, "files": 3, "spans": 10, "min_span": 10}}
exit=0
```

Every quote is a nested window of the single 16-byte line
` "lane": "mori",` in three real artifacts. The ten claim texts assert nothing;
the single row's `source` cell is a string that contains three artifact paths.
A second, independent variant (`v5-one-row-allpaths`, entry sha256
`2252918c…ef961f`, counter commit `565b391f…`) — ten distinct line spans of
the repeated literal `   "note": null` across r54/r55/r56, same vacuous texts,
same one-all-paths row — also returns `ok: true` (`"min_span": 15`); see
edit-distance table below.

## Control — the exact r59 construction is now rejected

Committed hostile tree `trees-c2h/h01-semantically-empty` run with the pinned
tool and the same args:

```
{"ok": false, "reasons": ["grammar:- **K99** …", "text:short=K1", …
 "text:dup=K1=K2", "files_min:1", "span:short=K1",
 "distinct:dup_span=K1=K2", …], "stats": {"claims":10,"files":1,"spans":1,"min_span":6}}
exit=1
```

Faithful five-file reconstruction (identical 6-byte `"lane"` @offset 3, two
claims per r54–r58 copy, one fabricated unbound row, one malformed line):
`exit=1`, `claims=10 files=5 spans=5 min_span=6`, reasons
`distinct:dup_span ×5, span:short ×10, text:short ×9, text:dup ×8,
grammar ×1, rows:binding ×5`. So H1–H4 bite the exact r59 bytes; they do not
bite the adapted bytes.

## Minimal edit ladder (each step is textual only)

| variant | what changed from the exact r59 bytes | tool verdict | stats |
|---|---|---|---|
| `l1-faithful-r59` | none | fail | files=5 spans=5 min_span=6 |
| `l2-texts-only` | 10 texts → distinct ≥10-char vacuous sentences | fail | files=5 spans=5; `span:short`, `dup_span`, `rows:binding` |
| `l3-row-unbound` | + spans → 10 distinct line spans (`"note": null`), row still without path strings | fail | files=3 spans=10; only `rows:binding ×3` |
| `v5-one-row-allpaths` | + append 3 artifact path strings to the one fabricated row's source cell | **ok** | claims=10 files=3 spans=10 min_span=15 |
| `v6-sliding-window` | same, but spans are nested windows of one 16-byte r59 line | **ok** | claims=10 files=3 spans=10 min_span=10 |

Three edits, zero claim content, one fabricated row: `ok=true`.

## Why each hardening axis fails (tool line pointers)

- **H1** (`tools/mori-entry-claims-check.py:110-121`): only lines matching the
  claim shape are parsed; malformed claim-shaped lines append `grammar:`.
  V5/V6 carry no malformed line, so H1 is not the gate.
- **H2** (`:146-170`): the uniqueness key is `key = (cfile, start, end)`
  (`:162`). Overlapping or nested spans are distinct keys, so ten sliding
  windows of one line pass (`v6`). The minimum is `end - start < MIN_SPAN`
  (`:168`), i.e. span **length** ≥8; the contract's "≥8 distinct bytes per
  span" is not what is checked (I nevertheless built each V6 window with ≥8
  distinct byte values, so the kill holds under either reading). Repeated
  structural literals at different offsets (the r59 `"lane"` family, or
  `"note": null`) are accepted verbatim.
- **H3** (`:124-131`): `ctext.strip()` length ≥10 and pairwise distinct is the
  whole test. "Vacuous filler statement number 01." … `10.` pass. No claim
  text is ever compared with the quote or the artifact.
- **H4** (`:188-238`): `binders` is every registry row with 11 cells,
  `cells[7]=="mined"`, `cells[10]==entry_rel` — regardless of which SID the
  entry cites. Binding is `any(art in b for b in binders)` (`:237`), a
  substring test over the row's source cell. One fabricated row whose source
  cell lists the three paths binds all three copies; r59's D4 ("one fabricated
  row could cover every copy") is still reachable, now with the paths pasted
  in.
- **Counter** (`count-c2.py:52`, `:306-336`, `:410`): `ENTRY` is a path, never
  a sha. The entry arm materializes whatever blob is at that path at `R` and
  accepts `ok` with `claims >= 10`, `files >= 3`, `spans == claims`; the
  frozen target values `claims=13 files=6 spans=13` are not enforced in code,
  so a different entry yields `C2=met` with different numbers (human
  comparison only). Nothing pins the "SAME real entry" clause.

## Counter-level corroboration (sandbox only)

A `git clone --shared --no-checkout` of the lane under the seat scratch (toplevel
asserted) was read-tree'd to `ac496c7c`, then a single commit replaced only the
entry blob and appended the S901 row; all other blobs are AC's.

```
V5 commit 565b391f0167221ed337dcd9ba2eb59cb7716101 (entry sha 2252918c…ef961f)
V6 commit 52759860852c3dd5cf9fcec817e6d839c4602f9d (entry sha 6333a96f…fc632d)
git -C <clone> show <commit>:corpus/knowledge/wave-settlement-artifacts-r59.md | sha256sum
  == the attack entry sha for that root (checked for both commits)
python3 <lane>/.ufo/waves/round-60/count-c2.py <commit> \
  --repo <scratch>/clone --scratch <scratch>/c2scratch
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok
tree=ok claims=10 files=3 spans=10 rev=<commit>        (exit 0)
```

Scope: this is a tampered commit, not the lane. It does not show the lane's
real entry is fake (the committed `evidence/c2-at-freeze.txt` reports the real
entry at `claims=13 files=6 spans=13`); it shows the frozen C2 predicate is
path-keyed, accepts a semantically empty entry, and would still print `met`
if the entry at that path changed under a moving tip during the wave.

## Impacted axes

- **C2 (depth) — capability claim falsified.** "Closes the routed r59
  entry-class defects" is false for the semantically-empty class; the frozen
  thirteen-tree set pins the exact r59 bytes, not the class. `C2=met` remains a
  statement about shape/pins/rows, not depth. Whether this moves the axis
  number is the L1's call (contract: instrument claims are capability-only).
- **C1, C3 — unaffected**: no C1 predicate touched; G1/G2/G3 arms run unmodified
  and the attack neither executes an unpinned blob nor escapes the scratch.
- Minor: the hostile trees' copies are the builder's synthetic `BLOBS`
  (`build-fixtures-r60.py:42-57`), not the lane artifacts (e.g. h00 tree copy
  sha `13d283…` vs lane copy `ea48a0…`), so the trees arm never exercises real
  artifact bytes; the real-entry arm does.

## Smallest safe correction

Counter/tool bytes are frozen; this is a next-round (or pre-scoring amendment)
spec. Three of the four items are one-line predicate changes — a fixable
defect, not a tradeoff:

1. H2: duplicate on the quoted bytes and require spans pairwise **disjoint**
   (`key = quote` in addition to `(cfile,start,end)`, plus an interval-overlap
   check). Kills V6 and V5.
2. H4: one cited copy → one SID named in the frontmatter, source cell equal to
   that copy's artifact path (not substring), and `len(sids) >= len(cited)`
   with distinct SIDs. Kills the one-row-all-paths fabrication.
3. Counter: pin `PIN_ENTRY` = sha256 of the real r59 entry at the freeze
   revision and require `claims/files/spans == 13/6/13` in code, so "SAME real
   entry" is enforced and tip movement cannot swap it.
4. H3 cannot be decided by a regex: length+distinctness cannot distinguish
   vacuous text from a claim. Either restate C2 as shape-only, or add an
   independent reviewer rejection arm for text↔quote semantics. This part is
   the tradeoff the canonical Rust judge must resolve by narrowing the claim
   sentence; it cannot be patched in frozen counter bytes.

Hostile trees to add with (1)-(2): ten vacuous distinct texts over nested/
repeated spans of one literal, and a single row whose source cell lists every
cited artifact path. Note that `trees_set` requires exactly the frozen thirteen
names, so this is only possible pre-scoring (contract amendment clause).

## Method bounds / receipts

- Lane read-only: all lane reads via `git show AC:<path>`, `cat`, `grep`;
  no commit, no VCS mutation, no production/registry/SCORECARD/LOG edit; this
  file is the only lane write.
- Scratch `/fast/scratch/hyaku/mori-r60/Mo60Critic21` created with `mkdir -p`,
  `TMPDIR` pointed there, all fixtures inside it; every git write used
  `git -C <scratch clone>` after asserting `rev-parse --show-toplevel`.
  Scratch removed after this report was written.
- Tool installs/updates: none.
- Not checked: C1/C3 counters; `sources-census.sh` behaviour on the fabricated
  S901 row (it may flag it at round level — a compensating control, not part of
  P-C2); the real entry's content honesty (accepted from `c2-at-freeze.txt`).

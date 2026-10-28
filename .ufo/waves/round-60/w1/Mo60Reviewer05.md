# Mo60Reviewer05 — hostile-tree battery (13 trees, C2 depth)

Seat: reviewer, leaf. Read-only over the lane; no commits, no VCS mutation, no
fleet/sibling writes. Scratch: `/fast/scratch/hyaku/mori-r60/Mo60Reviewer05`
(`TMPDIR` set there; cleaned before yield).

## Pins

| surface | revision / sha256 |
|---|---|
| freeze (amended) | `ac496c7cde8cad965079858accae3bedfe4a73f2` |
| entering | `ddfb12fb0838b4307c445194a844f0c4b1950195` |
| lane tip seen during seat | `b3c256138f00c704d5aa56eb0332d74506502ef2` (C1 data landing; not used for any tree read) |
| `tools/mori-entry-claims-check.py` @R | `cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69` (= PIN_EC) |
| `tools/mori-settlement-scan.py` @R | `4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9` (= PIN_SCAN) |
| `.ufo/waves/round-60/count-c2.py` @R | `8c4814f54c564a7f00beec5249de092a2d3b2c4043e07be773d80e8e3ccdf976` (= contract pin `8c4814f5…df976`) |
| `.ufo/waves/round-60/trees-c2h-expects.json` @R | `ae90c90f2c5d47952d38b8f10a3ea4608a225a03765a60571b48ba25575cc2ee` |
| `.ufo/waves/round-60/build-fixtures-r60.py` @R | `2343b46d837ccb826d1267f5f38fa40b0d4cb94fefd33b39dc87f549ef2b5970` |
| runtime | `/usr/bin/python3` 3.14.8 (one runtime for counter and battery) |

No unpinned working-tree read was used: every tree, tool and table byte came
from `git show` / `git archive` at `ac496c7c`. `git status --porcelain` in the
lane shows only pre-existing untracked wave artefacts (`w1/`, `w1.ready*`,
`evidence/c1-at-data.txt`), none written by this seat.

## Method (exact)

```
S=/fast/scratch/hyaku/mori-r60/Mo60Reviewer05; mkdir -p "$S"; export TMPDIR=$S
git -C <lane> show ac496c7c:tools/mori-entry-claims-check.py | sha256sum   # == PIN_EC
python3 "$S/battery.py" "$S"        # materializes all 13 trees from R, runs the pinned tool per tree
python3 "$S/ec-tool.py" --root "$S/trees/h00-good-control" \
  --entry corpus/knowledge/wave-settlement-artifacts-r59.md \
  --registry corpus/SOURCES.md --artifacts-json "$S/artifacts.json" \
  --min-claims 10 --min-files 3
cd /home/vgpnk/Projects/shokunin/mori-shokunin && \
  python3 .ufo/waves/round-60/count-c2.py ac496c7c… --scratch "$S/c2-scratch"
```

Materialization mirrors the counter's tree arm (`count-c2.py:351-405`): every
blob under `trees-c2h/<name>/` except `expect.txt` is written into a scratch
root (8 files/tree), then the tool is invoked with the counter's own constants
(`ENTRY`, `SOURCES`, `ARTIFACTS` json, `--min-claims 10 --min-files 3`).

## Per-tree verdict + reason table (R = ac496c7c)

`want_ok` = frozen expect is empty. All reasons are the tool's emitted strings;
`expect.txt` column is byte equality with `",".join(frozen)`.

| tree | files | want_ok | got_ok | frozen prefixes | emitted coverage | expect.txt==frozen | match |
|---|---|---|---|---|---|---|---|
| h00-good-control | 8 | True | **True** | — | reasons=[] ; claims=10 files=4 spans=10 min_span=13 | yes (size 1, `"\n"`) | **ok** |
| h01-semantically-empty | 8 | False | False | `distinct:dup_span`, `text:short` | dup_span=K1=K2…K1=K9; text:short=K1..K10 (38 reasons) | yes | ok |
| h02-malformed-claim | 8 | False | False | `grammar` | `grammar:- **K77** — malformed claim line missi` | yes | ok |
| h03-line-offset-alias | 8 | False | False | `distinct:dup_span` | `distinct:dup_span=K1=K10` (spans=9 vs claims=10) | yes | ok |
| h04-blank-quote | 8 | False | False | `span:blank` | `span:blank=K1` | yes | ok |
| h05-short-quotes | 8 | False | False | `span:short` | `span:short=K1..K4` (+claims_min:4, files_min:1) | yes | ok |
| h06-degenerate-text | 8 | False | False | `text:short` | `text:short=K1..K10` + dup/text/span (37 reasons) | yes | ok |
| h07-single-row | 8 | False | False | `rows:binding` | `rows:binding=…w1-results-r55/-r56/-r57.json` (+rows:missing×3) | yes | ok |
| h08-row-not-mined | 8 | False | False | `rows:status` | `rows:status=S901..S904` | yes | ok |
| h09-usedby-other | 8 | False | False | `rows:usedby` | `rows:usedby=S901..S904` | yes | ok |
| h10-stale-pin | 8 | False | False | `pin:` | `pin:1`, `pin:2`, `pin:3` | yes | ok |
| h11-wrong-line | 8 | False | False | `span:` | `span:1` | yes | ok |
| h12-no-frontmatter | 8 | False | False | `frontmatter` | `frontmatter:source`, `:verified-at`, `:recheck`, `:coverage-map` (+rows:no_source_ids) | yes | ok |

**13/13 match; h00 verifies True** (`rc=0`,
`{"schema":"mori-entry-claims-v2","ok":true,"reasons":[],"stats":{"claims":10,"files":4,"spans":10,"min_span":13}}`).

Comparator negative control (proves the table check is discriminating, not
vacuous): `h02 vs its own ["grammar"]` → match True; `h02 vs []` → False;
`h00 vs ["grammar"]` → False; `h00 vs []` → True.

## Corroborating controls

1. `mori-entry-claims-check.py --selftest` @R: `ENTRYCLAIMS_SELFTEST pass=13
   fail=0`, rc 0 (run from the pinned blob materialized in scratch, not the
   lane file).
2. Fixture determinism: rebuilding with the frozen builder in scratch
   (`git show ac496c7c:…/build-fixtures-r60.py` → `python3 build.py` in a
   throwaway dir) produces trees byte-identical to `git archive ac496c7c …`
   (`diff -r` → `FULL_TREES_IDENTICAL_INCLUDING_EXPECT`) and an identical
   expects table (`EXPECTS_IDENTICAL`).
3. Table identity: the counter's embedded `FROZEN_EXPECTS` equals the
   committed `trees-c2h-expects.json` exactly (13/13, dict-equal), so a
   committed-`expect.txt`/table split cannot hide behind a divergent embed.
4. Canonical instrument cross-check at R: `count-c2.py ac496c7c…` →
   `C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok
   tree=ok claims=13 files=6 spans=13 rev=ac496c7c…`, rc 0 — byte-equal to
   `evidence/c2-at-freeze.txt`.
5. No post-freeze drift: `git diff --stat ac496c7c b3c2561 -- trees-c2h
   trees-c2h-expects.json count-c{1,2,3}.py tools/mori-entry-claims-check.py
   tools/mori-settlement-scan.py` is empty; working tree matches R for
   `trees-c2h`.
6. No absolute host path in any of the six instruments (`grep -cE
   '/home/|/fast/|/tmp/'` → 0 for count-c1/c2/c3, both tools, builder).
7. Pin gate is structurally real: `run_pinned` refuses on sha mismatch
   (`count-c2.py:144-150`) and the tool/scan blobs are written only when
   pinned (`:169`, `:179`); the tree arm additionally refuses to evaluate
   when `ec_ok` is false (`:378-380`).

## Findings

### MEDIUM — H4 residual: one fabricated *uncited* row still covers every copy
`tools/mori-entry-claims-check.py:224-238`. `binders` is built from **every**
registry row that is 11 cells / `mined` / `used-by == entry_rel` (`:225-233`),
independent of the SIDs the entry actually cites, and each cited copy is
accepted when its `.ufo` artifact path appears as a **substring** of *any*
binder's source cell (`:237`, `art in b`).

Probe (scratch only, `$S/probe1`, copy of the h00 materialized tree):

```
cp -r "$S/trees/h00-good-control" "$S/probe1"
# registry: S901-S904 kept 11-cell/mined/used-by, source cell emptied;
#           + S999 (uncited) mined/used-by, source cell names all six .ufo paths
python3 "$S/ec-tool.py" --root "$S/probe1" \
  --entry corpus/knowledge/wave-settlement-artifacts-r59.md \
  --registry corpus/SOURCES.md --artifacts-json "$S/artifacts.json" \
  --min-claims 10 --min-files 3
```

Result:
`{"ok": true, "reasons": [], "stats": {claims:10, files:4, spans:10,
min_span:13}}`.

Consequence: the routed r59 defect "one fabricated row could cover every copy"
is narrowed but not closed — one fabricated row naming all six artifacts
satisfies per-copy binding for all copies, and the row need not be a row the
entry cites. The frozen contract sentence ("every cited copy binds to a mined
used-by-exact registry row whose source cell names the copy's artifact") is
literally satisfied, so this does **not** flip C2 at R; it is residual
hardening risk for the next round's H4.

### LOW — tree arm is coupled to the entry arm's `artifacts.json`
`count-c2.py:308-309` writes `scratch/artifacts.json` only inside
`if have_all and ec_ok:`, while the tree arm unconditionally passes
`scratch/artifacts.json` (`:385-386`). If the real entry or any of the six
copies is absent at R, every tree evaluates with
`artifacts_json unreadable` (tool `:465`, exit 2) and is reported as
`tree:<name>:verdict` rather than with its true verdict. This masks tree
results; it cannot produce a false `met` (the entry arm already failed). Not
activated at `ac496c7c` (entry and all six copies exist).

### LOW — `if binders and …` silently skips H4 when no binder exists
`tools/mori-entry-claims-check.py:237`. With `binders == []` the per-copy
binding loop appends nothing. Not reachable in a met verdict today —
`rows:no_source_ids` (`:203`), `rows:missing` (`:212`), `rows:status` (`:216`)
and `rows:usedby` (`:218`) guarantee a non-empty binder set before `ok` — but
it is a defense-in-depth gap a later refactor could expose.

### LOW — H2 "≥8 distinct bytes per span" = span length, not byte diversity
`tools/mori-entry-claims-check.py:49`, `:168-169`. The check is
`end - start < MIN_SPAN`, so a span of 8 low-entropy bytes passes; it is not a
distinct-byte-value test. Consistent with the tool's own docstring ("each span
carries at least MIN_SPAN bytes") and with the contract under the
length reading; recorded as an interpretation note, not a defect.

### INFO — expect prefixes are a subset of emitted reasons (by design)
h01/h05/h06 emit extra classes beyond the frozen prefix (`files_min`,
`claims_min`, `span`, `distinct`). That is correct: the table is the required
prefix set, and over-firing is caught by h00 (which must verify True with zero
reasons). Each tree still discriminates its named class: dropping any one
check (grammar, dup-span, blank, min-span, text-length, rows:status,
rows:usedby, rows:binding, pin, byte-match, frontmatter) changes the verdict
and/or removes the required prefix for that tree.

## Residual risk and verification gaps

- G3 `expect_tamper` branch not exercised here (C3 owns the expectgate PoC). I
  verified only the precondition: all 13 committed `expect.txt` byte-equal the
  frozen table (`01ba4719…` h00 … `a39cb081…` h12), so the tamper branch is
  correctly dormant at R.
- H5 drift arm / scan arm / real-entry arm were verified only indirectly via
  the canonical counter at R; direct per-arm falsification is out of this
  seat's scope.
- The `count-c2.py` run at freeze is a cross-check, not a re-score; no axis
  score is moved by this report.
- `h00` sits exactly on `MIN_CLAIMS` (10) with `files=4` (min 3); margin is
  one file and zero claims, so any future threshold raise silently turns the
  no-false-negative control red — intentional-looking but brittle.
- Synthetic tree copies are not the real `.ufo` artefacts (that role belongs to
  the counter's entry arm `entry=ok`, which also reproduced); tree arm
  therefore proves predicate capability, not real-artifact pinning.

Hygiene: all writes confined to `$HYAKU_SCRATCH/mori-r60/Mo60Reviewer05`
(removed before yield); lane, fleet root and sibling repos untouched; no
commits, no pacman, no tool installs.

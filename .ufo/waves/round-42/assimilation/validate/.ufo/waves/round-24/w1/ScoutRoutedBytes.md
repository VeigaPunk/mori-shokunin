# ScoutRoutedBytes — C1 independent expected values (read-only)

Scope: record the round-23 routed bytes the C1 check must compare against, at revision
`c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130`, plus the implementation traps those bytes expose.
Read-only seat: no production edits, no git mutations, no jj command. No tool installed or
upgraded during this ticket.

## Method and revision identity

All facts below come from read-only git plumbing in the lane repo
`/home/vgpnk/Projects/shokunin/mori-shokunin` (`ls-tree`, `rev-parse`, `cat-file`, `grep`,
`diff`, `log`, `merge-base`, `status`). No working-tree file was read for any predicate value;
every value is a committed object ID at the named revision.

| Fact | Command | Value |
|---|---|---|
| Base revision resolves | `git rev-parse --verify c725aa37^{commit}` | `c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130` |
| Base root tree OID | `git rev-parse c725aa37^{tree}` | `ffd1849f5e17a828792f998abc8e0a53799c1738` |
| Lane tip at read time | `git rev-parse HEAD` | `4059ffb5e4b81da6f4a1a00056ba8364cac123c8` |
| Base is ancestor of tip | `git merge-base --is-ancestor c725aa37 HEAD` | exit 0 (true) |
| Commits base..tip | `git rev-list --count c725aa37..HEAD` | 3 (`29c1bf4` claims/contract, `06d4f4d` wave-1 spec + dispatch payload, `4059ffb` wave-1 attempt ledger) |
| Files changed base..tip | `git diff --name-only c725aa37 HEAD \| wc -l` | 9 (7 round-24 files, `LOG.md`, `SCORECARD.md`) |
| Working tree cleanliness | `git status --porcelain` | one line: `?? .scratch/` (untracked; not touched by me) |

## Requested expected values at `c725aa37`

### Tree OIDs (R1 and R3 tree legs)

| Path | OID at base | Kind |
|---|---|---|
| `.ufo/waves/round-23/frozen` | `0c067e21cf1e57817235194d9e688dd17c1dffa4` | tree (37 blobs under it) |
| `.ufo/waves/round-23/rejected` | `4314126903ccfa6e7bfd5767a2f491de8a7e3edb` | tree (8 blobs: `READ-THIS.txt`, `deployed-quota-probe.py`, `frontier-disposition.txt`, `inherited-clone-copies.json.gz`, `owned-round23-scratch-evidence.json`, `owned-round23-scratch-evidence.tar.gz`, `quota-knowledge-note.txt`, `withdrawal-manifest.json`) |
| `.ufo/waves/round-23/evidence` (context) | `2305d7387e50d56df0ef9316f2868126f7474a4b` | tree |

Command: `git ls-tree c725aa37 -- .ufo/waves/round-23/frozen .ufo/waves/round-23/rejected .ufo/waves/round-23/evidence`.

### Blob OIDs (R2 and R3 byte legs)

| Path (all under `.ufo/waves/round-23/evidence/`) | Blob OID at base | Mode | Size |
|---|---|---|---|
| `retention-floor-final.json` | `4954de42072b8c5520f95067a6b005a5c82fbbb2` | 100644 | 32875 |
| `retention-floor-final-comparison.json` | `1411d94a8b16f844e0d334ea6135bd7d85969318` | 100644 | 746 |
| `harness-receipt-overwrite.json` | `bfcfb2c8d2eb15afd73a939b8445c9de32602efd` | 100644 | 1309 |
| `tmpfs-source-provenance-erratum.json` | `ad622617a7e8fb04ae6f1ffb9a143ea6db518acb` | 100644 | 842 |

Command: `git rev-parse c725aa37:.ufo/waves/round-23/evidence/<name>` per file; sizes from
`git ls-tree -l`. `git cat-file -t` returns `blob` for all four (not symlink, not submodule).

### Existence of the R1 paths

| Path | At `c725aa37` | In lane worktree at read time |
|---|---|---|
| `tools/mori-quota-surface.py` | ABSENT (`git cat-file -e` → `fatal: path ... does not exist in 'c725aa37'`, exit 128) | ABSENT |
| `corpus/knowledge/quota-surface-r23.md` | ABSENT (same, exit 128) | ABSENT |

### Committed lines matching `privacy_clearance\s*["']?\s*[=:]\s*["']?true` (case-insensitive) at `c725aa37`

9 lines in 6 files. `git grep -P` and `git grep -E` with `[[:space:]]` return the identical set;
the whole-tree count at the lane tip is also 9 (nothing added since).

| File:line | Line |
|---|---|
| `.ufo/waves/round-22/falsify/MutationScope.md:58` | `            'privacy_clearance':True,'input_revision':revision,'measured_revision':measured,` |
| `.ufo/waves/round-22/falsify/MutationScope.md:69` | `**[INFERENCE] Expected distinguishing output:** ... but now emit \`privacy_clearance=true\`. ...` |
| `.ufo/waves/round-22/measure-round22.py:87` | `        ('false-clearance',[("'privacy_clearance':False,'input_revision'","'privacy_clearance':True,'input_revision'")],{'frozen:R02'}),` |
| `.ufo/waves/round-23/falsify/C1R04.md:170` | ``| `false-clearance` | `privacy_clearance: True` | R02,R11,R23 | green |`` |
| `.ufo/waves/round-23/falsify/C1R15.md:238` | `` `privacy_clearance: true` on a setup envelope would satisfy all 26 requirements. C24`` |
| `.ufo/waves/round-23/falsify/C1R17.md:153` | ` "error":"receipt_schema","privacy_clearance":true,"detail":"R22_SAMPLE retained-red"}` |
| `.ufo/waves/round-23/falsify/C1R17.md:163` | ``* `false-clearance` (mutant set `privacy_clearance: true`): R17 still `True`; killed by R02/R11/R23`` |
| `.ufo/waves/round-23/falsify/ReviewDebtHold.md:200` | ``  `.ufo/waves/round-23/**` finds **no** `privacy_clearance: true`, no `pin_allowed: true`,`` |
| `.ufo/waves/round-23/falsify/ReviewDebtHold.md:274` | ``no r23 file contains `privacy_clearance: true`, `pin_allowed: true` or an acceptance`` |

Scoped counts at `c725aa37`: `.ufo/waves/round-23/**` → 6 lines (all in `falsify/`);
`.ufo/waves/round-23/evidence/**` → 0 lines (`git grep` exit 1, no output). Round-22 contributes
the other 3. Every hit is prose, a markdown-quoted fragment, or a Python mutant description —
none is a committed evidence payload that sets the key true, which is consistent with
`ReviewDebtHold.md:200,274` asserting exactly that.

### R4 leg at `c725aa37`

`.ufo/waves/round-24/` does not exist at the base revision:
`git cat-file -e c725aa37:.ufo/waves/round-24` → `fatal: path '.ufo/waves/round-24' exists on
disk, but not in 'c725aa37'`, exit 128; `git ls-tree -r --name-only c725aa37 -- .ufo/waves/round-24/`
→ 0 lines. No `*-attempts.json` under round-24 at base. Existing ledgers at base live in rounds
17, 18, 19, 21 and `.ufo/waves/round-23/wave1-attempts.json`. So R4 is the only red item in the
declared before-run, which is what makes the before-value `held: 3` — consistent with the contract.

## Traps these bytes expose (for the C1 tool and its mutants)

1. **The R2 regex leg must be an added-lines diff, not a tree scan.** At `c725aa37` a whole-tree
   scan returns 9 hits, and the round-23 subtree alone returns 6. An implementation that reads
   "no line matches at REV" would mark R2 red at the base revision and print `held: 2`, breaking
   the declared before-value. The contract's wording is "no line added between base and REV
   matches", and `git diff --unified=0 c725aa37 HEAD | grep '^\+' | grep -P <regex>` returns 0
   hits (exit 1) — the added-line reading is the one that reproduces `held: 3`. Confidence: high
   (observed both readings).
2. **Self-reference hazard on the added-line leg.** The new tool's own source, its report, or the
   QUALITY.md criterion line can contain the `privacy_clearance: true` form in prose or a reason
   string; that line is *added* between base and REV, so a global added-line scan would flag R2 on
   the round's own artifacts and could never hold. Precedents for that exact form already exist in
   committed prose (`C1R17.md:153`, `C1R15.md:238`, `C1R17.md:163`). The executor must either
   restrict the added-line scan to the intended surface (e.g. `.ufo/waves/round-23/evidence/**`)
   or exclude the tool and round-24 artifacts — and document the choice, because the choice is
   falsifiable: the R2 mutant ("add a line that sets the privacy-clearance key to true") only kills
   the item if the mutant's target file is inside the scanned surface. As of this read, round-24
   additions are clean: 0 matching added lines across `LOG.md`, `SCORECARD.md` and the 7 round-24
   files (`git grep HEAD -- .ufo/waves/round-24/` exit 1; added-line diff count 0).
3. **Exact-path equality is required for the four blobs; the name family is crowded.** Four files
   share the `retention-floor` prefix at base — `retention-floor-comparison.json`
   (`1d3925cf993c4cfbe2d7a68c15abd7ff4cc783b7`), `retention-floor-delivered.json`
   (`3c7c76fd30e9ce6480d8b6fffc0757024e805542`), `retention-floor-final.json`, and
   `retention-floor-final-comparison.json`. A prefix or glob match can silently compare the wrong
   blob and turn R2 green for the wrong reason. The R2/R3 paths are all at the top level of
   `evidence/`, not in a subdirectory.
4. **R1's absence leg must not be a substring search.** The withdrawn round-23 artifacts still
   exist under `.ufo/waves/round-23/build/`: `build/ImplQuota/mori-quota-surface.py`,
   `build/ImplQuota/mori-quota-surface-v2.py`, `-v3.py`,
   `build/DraftKnowledge/quota-surface-r23.md`, `oracle-quota.py`, plus
   `rejected/quota-knowledge-note.txt` and `rejected/deployed-quota-probe.py`. Any existence test
   looser than the exact canonical paths `tools/mori-quota-surface.py` and
   `corpus/knowledge/quota-surface-r23.md` will false-positive.
5. **The tree-OID legs are self-comparisons in the before-run.** Because the before-value runs at
   `--rev c725aa37` and base *is* `c725aa37`, R1's frozen-tree leg and R3's rejected-tree leg
   compare a tree to itself, and R2/R3's blob legs compare blobs to themselves. They cannot fail in
   the before-run; the whole discriminating power of the before-run is R4's absence. The mutant
   sandbox is therefore the only evidence that R1/R2/R3 legs work at all — worth stating in the
   landing notes so `held: 3` is not read as proof the other three legs function.
6. **The R4 leg's helper already exists at base** with the needed CLI:
   `tools/mori-dispatch-ledger.py` = blob `b86525c6a9fe0d44e90127323ff291104dcfb5fd`, and it
   exposes `verify --repo --rev --ledger` (all required, `allow_abbrev=False`) alongside
   `bind --repo --rev --dispatch`. So R4's "each verifies clean" step is runnable against
   committed bytes without any new dependency.

## Supplementary: state at the lane tip (`4059ffb`), for the after-value

| Item | Value at tip | Consequence |
|---|---|---|
| `.ufo/waves/round-23/frozen` | `0c067e21cf1e57817235194d9e688dd17c1dffa4` (identical to base) | R1 tree leg still holds |
| `.ufo/waves/round-23/rejected` | `4314126903ccfa6e7bfd5767a2f491de8a7e3edb` (identical to base) | R3 tree leg still holds |
| four evidence blobs | identical to base (same four OIDs) | R2/R3 byte legs still hold |
| `.ufo/waves/round-24/wave1-attempts.json` | present, blob `d8df5999d910784f66cb005900fd7cb58ac19881`, 437 bytes | R4 becomes satisfiable at the tip |
| round-24 tree | `contract.md`, `w1/swarm-registry.json`, `wave1-assignments.json`, `wave1-attempts.json`, `wave1-response.txt`, `wave1-run.json`, `wave1-spec.json` | the ledger path is `.ufo/waves/round-24/wave1-attempts.json`, matching the `*-attempts.json` glob |
| `tools/mori-routed-check.py`, `tools/mori-pressure.py`, `tools/fixtures/mori-pressure/cases.json`, `corpus/knowledge/system-pressure-r24.md` | ABSENT from the lane worktree | C1/C2 artifacts are not yet landed; only `.scratch/` is untracked |

## Not run / not verified

- I did not run `tools/mori-routed-check.py` (it does not exist yet) or
  `tools/mori-dispatch-ledger.py verify` (the C1 tool owns that call).
- I did not open any evidence blob's contents; only OIDs, modes and sizes were read, because the
  C1 predicate is byte equality against these OIDs.
- No C2 pressure bytes, fixtures or `/proc/pressure` reads — out of this ticket's scope.
- No working-tree edits; the only file I created is this report. No installs or upgrades.

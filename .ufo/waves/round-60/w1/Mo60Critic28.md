# Mo60Critic28 — whole-contract falsification sweep (round 60, seat 28)

Mode: read-only critic. Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`
read at `b3c256138f00c704d5aa56eb0332d74506502ef2`; frozen contract at
`ac496c7cde8cad965079858accae3bedfe4a73f2`; entering rev
`ddfb12fb0838b4307c445194a844f0c4b1950195`. No production file, registry,
SCORECARD, LOG or lane VCS byte was modified. All mutation ran on a throwaway
clone at `/fast/scratch/hyaku/mori-r60/Mo60Critic28/clone` and on `mktemp`
fixture repos under the same scratch tree; every git command used
`git -C <explicit path>`. Scratch is deleted after this report (small receipts
are inlined below).

Concurrent lane movement observed, not mine: the lane tip advanced
`b3c25613…` → `0f8340cf…` during the sweep and `corpus/lessons/round-60.md`
showed `MM` (staged truncation, worktree rewrite, mtime 13:19:51 -03). Every
re-derivation below is pinned to a named revision, so the movement changes no
result; no lane file was written by this seat except this report.

## Headline

- The three named do-nothing states (empty tree, entering rev, counters-only
  tree) **do not** print all three counters `met`. The aggregate claim survives
  them.
- The cheapest committed-revision path to `C1=met C2=met C3=met` is **16
  inserted lines and 2 token repoints** on top of the freeze revision (no
  reconciliation prose, no source rows, no knowledge entry). It is reproduced
  below as `c1b135ed…`.
- Four instrument defects are real and one contract rule is unmeasured:
  C1's lesson arm is per-file not per-name; C1's "pointer-honest" arm covers
  exactly two strings; C2 does not pin the entry it claims to measure; C3's
  printed arm tokens are not derived from the arm booleans. §2b (sourced-claim
  rule) is measured by nothing.

## Baseline reproduction (frozen instruments behave as receipted)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ python3 .ufo/waves/round-60/count-c1.py b3c25613 --scratch $T   # rc 0
C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c256138f00c704d5aa56eb0332d74506502ef2

$ python3 .ufo/waves/round-60/count-c2.py ac496c7c --scratch $T   # rc 0
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=ac496c7c<…>

$ python3 .ufo/waves/round-60/count-c3.py ac496c7c --scratch $T   # rc 0
C3=met toolgate=ok containment=ok expectgate=ok cases=6 rev=ac496c7c<…>
```

Selftests: `C1_SELFTEST pass=6 fail=0`, `C2_SELFTEST pass=8 fail=0`,
`C3_SELFTEST pass=3 fail=0`, `ENTRYCLAIMS_SELFTEST pass=13 fail=0` — all rc 0.

Do-nothing controls re-run at `ddfb12fb…`, byte-equal to the committed
receipts (`diff` clean for all three):

```
C1=unmet dead-uncorrected=2 receipts=0/2 absent-set=0/5 lesson=absent rev=ddfb12fb<…> failed=<…>
C2=unmet selftest=bad scan=ok drift=ok trees=bad entry=bad rows=bad pins=bad tree=ok claims=0 files=0 spans=0 rev=ddfb12fb<…> failed=entry,pins,rows,selftest,tool_absent,trees,trees_set
C3=unmet toolgate=bad containment=bad expectgate=bad cases=1 rev=ddfb12fb<…> failed=count_c1_absent,count_c2_absent,g1_new_skipped,g2_skipped,g3_skipped
```

Post-freeze instrument surface is clean:
`git log --oneline ac496c7c..HEAD -- .ufo/waves/round-60/count-c{1,2,3}.py tools/mori-entry-claims-check.py .ufo/waves/round-60/contract.md` → empty.

## The three named cheap states, measured

| state | C1 | C2 | C3 | note |
|---|---|---|---|---|
| empty tree (`01bf3707…`, fixture repo) | unmet (`scorecard_absent`) | unmet (`tool_absent`, `copy_absent:*`) | unmet (`count_c*_absent`) | arms hold |
| entering `ddfb12fb…` | unmet (control, byte-equal) | unmet (control) | unmet (control) | arms hold |
| counters-only `4d036fb0` (lane) | unmet | unmet (`tool_sha`, `expect_tamper`×12) | unmet (`count_c2_sha`) | arms hold |
| counters-only, pinned bytes, no r59 history (fixture `ec31f579…`) | — | — | **unmet but `toolgate=ok`** | see F4 |

So no committed revision in the lane prints all three met before
`398d3225`: `4d036fb0` → C1/C2/C3 unmet; `ac496c7c` → C1 unmet, C2+C3 met;
`398d3225` → C1 met. **First all-three-met = 398d3225** (the C1 data commit).

## Findings

### F1 — C1 lesson arm is per-file, not per-name (high)

Code: `count-c1.py:217-231`. Each of the five names is checked with two
whole-file substring tests — `name in lt and "supersedes" in lt` (`:224`) and
`name in lt and R59_LANDING[:8] in lt` (`:228`). Nothing binds a name to its
own attribution.

Counterexample (clone `0a3742fa…`, base = lane tip): `corpus/lessons/round-60.md`
replaced by a 5-line file, five names in one bare list, one `f091bd77`:

```
# Round 60 lesson (critic probe — synthetic)

Mo59Executor40 Mo59MutationTester31 Mo59MutationTester32 Mo59Critic29 Mo59Reviewer16

supersedes round-59 f091bd77
```

```
$ python3 .ufo/waves/round-60/count-c1.py 0a3742fa --repo <clone> --scratch $T
C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=0a3742fa<…>   # rc 0
```

Impact: the contract sentence "naming every wrong-superseded name with
`supersedes`, every late-committed name with landing pointer `f091bd77`" is not
what the counter measures; a name bag with two global tokens scores `lesson=ok`.

Smallest safe correction: one row/line per name —
`line contains name` **and** (`supersedes` | `f091bd77`) on that same line.

### F2 — C1 "pointer-honest" covers exactly two strings (medium)

Code: `count-c1.py:77-104` (only `DEAD_NAMES`), `:160` (only `REAL_POINTERS`
existence). No other SCORECARD pointer is resolved.

Counterexample (clone `0a3742fa…`, on top of the corrected SCORECARD):

```
| r59 probe row | `.ufo/waves/round-59/evidence/no-such-artifact.txt` |
$ git -C <clone> cat-file -e HEAD:.ufo/waves/round-59/evidence/no-such-artifact.txt
fatal: path '…no-such-artifact.txt' does not exist in 'HEAD'        # rc 128
$ python3 .ufo/waves/round-60/count-c1.py 0a3742fa --repo <clone> --scratch $T
C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok      # rc 0
```

Impact: the axis label ("pointer-honest record") is attested by a two-name
check; the routed defect-1 *class* (dead evidence pointers) is closed only for
the two routed names, and only in `SCORECARD.md`. Round-59 w1 reports are clean
(`grep -r entering.txt .ufo/waves/round-59/w1/` → 0), so no live second-order
break, but the predicate is narrower than the claim.

Smallest safe correction: either narrow the claim wording to "the two routed
dead names", or add an arm that resolves each backticked repo-path token in the
round-59 SCORECARD block against `R` (legitimate relative resolution against
the row's wave dir). Note a naive global resolution produces 169 false "dead"
tokens (bare basenames), so the arm must resolve per-row, not globally.

### F3 — C2 does not pin the entry it claims to measure (medium)

Code: `count-c2.py:52` `ENTRY = …`; the sha pins are only for the tool
(`:147`, `:162`), the scan tool (`:172`) and the artifact copies (`:286`).
`ENTRY` is read at `rev` (`:304`) and handed to the pinned tool; nothing binds
its bytes.

Counterexample (clone `d820fe50…` = lane tip + one appended comment line to
`corpus/knowledge/wave-settlement-artifacts-r59.md`):

```
real entry   sha256 = 441a751d…6ce21
probe entry  sha256 = c7514fe5…2cf0c
$ python3 .ufo/waves/round-60/count-c2.py d820fe50 --repo <clone> --scratch $T
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13   # rc 0
```

Impact: the claim's "on the SAME real entry" is bound only indirectly by the
frozen target's `claims=13 files=6 spans=13`; a scorer checking `C2=met` + rc
(which is how the do-nothing control is phrased) would accept any entry the
pinned tool likes. Entry and registry (`SOURCES`) are both unpinned.

Smallest safe correction: add `PIN_ENTRY = 441a751d…` (freeze bytes) with an
`entry_sha` failure token, and a `PIN_REGISTRY` likewise, or state in the
contract that the entry is identified by counts only.

### F4 — C3's printed arm tokens are not derived from the arm booleans (medium)

Code: `count-c3.py:298-306`:

```
"ok" if "toolgate" not in failed and "g1_new_skipped" not in failed else "bad"
"ok" if "containment" not in failed and "g2_skipped" not in failed else "bad"
"ok" if "expectgate" not in failed and "g3_skipped" not in failed else "bad"
```

The real failure names are `g1_new_no_tool_sha`, `g1_new_executed`,
`g1_old_control_did_not_reproduce`, `g1_old_skipped`, `g2_parent_escape`,
`g2_symlink_escape`, `g2_escape_written`, `g3_no_tamper_flag`. None of them
contains the substrings the token logic tests, so the tokens print `ok`
whenever the arm *ran*, regardless of verdict — and `cases` increments
unconditionally (`:176`, `:196`, `:249`).

Counterexample (fixture repo `ec31f579…`, two frozen counters committed, no
r59 history):

```
$ python3 .ufo/waves/round-60/count-c3.py ec31f579 --repo <fixture> --scratch $T
C3=unmet toolgate=ok containment=ok expectgate=ok cases=5 rev=ec31f579<…> failed=g1_old_skipped,r59_counter_absent
```

`toolgate=ok` prints while the G1 old-counter control arm was **skipped** and
the predicate is false. A grep-for-tokens check (or the human reading the
receipt) is fooled; only `C3=met` + exit 0 remain evidence-bearing.

Smallest safe correction: compute `tokens` from `(toolgate and old_hole)`,
`containment`, `expectgate`, and append the literal ids `toolgate` /
`containment` / `expectgate` to `failed` when false, so the token and the
predicate cannot diverge.

### F5 — §2b sourced-claim rule is measured by nothing (medium)

Code: no r60 counter references `entry-claims-hardening-r60.md` or `S561`-
`S564` (`grep -n "S56[0-9]\|entry-claims-hardening" .ufo/waves/round-60/count-c*.py`
→ only `corpus/SOURCES.md` as the entry's registry at `count-c2.py:53,296,312,384`).

Counterexample (clone `a658c48f…` = lane `398d3225` with
`corpus/SOURCES.md` reverted to its pre-`S561-S564` state and
`corpus/knowledge/entry-claims-hardening-r60.md` deleted):

```
C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13
C3=met toolgate=ok containment=ok expectgate=ok cases=6
all rc 0
```

Impact: the contract's §2b ("C2 and C3 rest on registry rows opened this round
… The hardened-grammar knowledge entry … cites those rows") can be dropped
entirely and the three frozen target lines still print. This is a
met-without-the-stated-work path at a committed revision.

Smallest safe correction: add one arm to count-c2 requiring `S561`/`S562`/`S563`
rows with their Gate quotes and that `entry-claims-hardening-r60.md` cites them
and does not admit `S564`; or record §2b explicitly as an unscored procedural
rule so the closure does not imply measurement.

### F6 — The cheapest all-three-met commit is 16 lines (informational)

Lane history: `4d036fb0` unmet/unmet/unmet → `ac496c7c` unmet/met/met →
`398d3225` met/met/met. Clone floor commit `c1b135ed…` (base `ac496c7c`):
re-point the two dead tokens in SCORECARD to the real committed pointers with
the `r60-correction:` marker (2 token edits), write the two receipts by running
the r59 counters once each, write a 5-row absent table whose note cell is `x`,
and the 5-line lesson above.

```
 .ufo/waves/round-60/evidence/r59-absent-set.md | 7 +++++++
 .ufo/waves/round-60/evidence/r59-c1-met.txt    | 1 +
 .ufo/waves/round-60/evidence/r59-c2-met.txt    | 1 +
 SCORECARD.md                                   | 4 ++--
 corpus/lessons/round-60.md                     | 5 +++++
 5 files changed, 16 insertions(+), 2 deletions(-)

C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok      # rc 0
C2=met … claims=13 files=6 spans=13                                 # rc 0
C3=met toolgate=ok containment=ok expectgate=ok cases=6             # rc 0
```

at which `corpus/knowledge/entry-claims-hardening-r60.md` does not exist
(`cat-file -e` → 128) and `grep -c S56[1-4] corpus/SOURCES.md` → 0.

Impact: C1's met cost is two command invocations plus transcription of git
truth; the absent-set arm is self-consistent (the counter recomputes the same
`git cat-file -e` truth it compares against), so it cannot distinguish an audit
from a transcription. C2/C3 are met at the freeze with zero C1 data by design
(their at-freeze receipts already show that), so the round's *instrument*
claims are genuinely capability-only.

### F7 — G1 marker probe is scratch-scoped (low)

`count-c3.py:173` counts markers only under `s_new` (`markers_under` does
`Path(root).rglob`), while `run_counter` inherits the counter's cwd. An unpinned
blob that wrote outside `--scratch` would not be observed. The gate itself is
structural (`count-c2.run_pinned` re-checks the sha and only then executes), so
this is a demonstration blind spot, not a met-flip. Cheapest correction: scan
both the scratch dir and a fresh empty cwd (`cwd=` on `run_counter`).

## Per-claim verdict on the do-nothing question

| claim | do-nothing arm | verdict |
|---|---|---|
| C1 | empty tree / entering / counters-only | holds (unmet in all three); but the cheap `met` path is transcription (F1, F2, F6) |
| C2 | empty tree / entering / counters-only `4d036fb0` | holds (unmet); `met` at freeze is by design; entry identity unpinned (F3) |
| C3 | empty tree / entering / counters-only | holds; token axis is not evidence (F4) |
| §2b | any | **breaks** — all three met with the rows and knowledge entry absent (F5) |

## Impacted axes and dispositions

- C1 calibration (5): F1/F2 are fixable predicate defects, not tradeoffs;
  they do not move the score (contract's instrument-claim ruling) but they
  overstate "pointer-honest" and "naming every … name with".
- C2 depth (5): F3 is a fixable predicate defect; F5 is the more serious
  claim-scope defect (a stated rule is unmeasured).
- C3 operability (7, owned): F4 is a fixable output-fidelity defect; the
  predicate itself (`met`) is sound and the old-counter hole reproduces.
- Nothing here justifies rejecting the round; all five findings have a
  one-arm/one-line correction and none require re-freezing a predicate that a
  seat has already scored.

## Tooling

No installs, no pacman, no network. Python 3 (host default), git (host
default), both already present. Disk guard checked at start (green; 600 G free
on `/fast/scratch/hyaku`); all temporary state under
`/fast/scratch/hyaku/mori-r60/Mo60Critic28` and removed after this report.

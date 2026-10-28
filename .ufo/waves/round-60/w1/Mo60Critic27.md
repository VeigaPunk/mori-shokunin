# Mo60Critic27 — C1 dead-name marker gaming (adversarial falsifier)

Role: critic (read-only). Seat: `Mo60Critic27`. No production/registry/SCORECARD/LOG/VCS edits,
no sibling or fleet writes. Findings only; no remediation applied.

## Pins (every measurement names a revision)

| item | value |
|---|---|
| frozen contract revision (amended freeze) | `ac496c7cde8cad965079858accae3bedfe4a73f2` |
| entering revision | `ddfb12fb0838b4307c445194a844f0c4b1950195` |
| lane tip observed during this seat | `b3c256138f00c704d5aa56eb0332d74506502ef2` |
| `count-c1.py` sha256 at ac496c7c / 398d3225 / b3c25613 / worktree | `795c1f3193a76406a40561ac60fedb3eee75fc38df2b2efb3fc5295d617ddbae` (all four equal) |
| `contract.md` sha256 at ac496c7c / b3c25613 / worktree | `a444e270957b957875b667b3cd226b965234deda242db12a81df597e2c15441d` (all three equal) |

Kill rule (contract:67-68) is intact: neither counter nor contract bytes moved after the freeze.
The scored counter is therefore exactly the object attacked below. All C1 numbers below are
produced by that byte-identical frozen blob (`git show ac496c7c:.ufo/waves/round-60/count-c1.py`,
copied to scratch, sha re-verified before each run), never by the working tree.

Real-lane anchors used: `count-c1.py:40-46` (constants), `:77-86` (`dead_uncorrected`),
`:88-101` (`corrected_lines_name_real`), `:240-262` (`selftest`); contract `:40-43` (dead-name arm
sentence), `:66-68` (selftest, kill rule).

## Method

1. Frozen counter bytes extracted read-only from `ac496c7c` (sha above) and driven only against
   throwaway fixture repos created at an explicit scratch path
   (`$HYAKU_SCRATCH/mori-r60/Mo60Critic27`, `git init` asserted via
   `git -C <fixture> rev-parse --show-toplevel`), one commit per construction, so every read is
   committed bytes at a named revision — same access path as `measure()`.
2. The same module was imported (`importlib`) and the two arm functions called directly, so an
   evasion is attributed to the arm rather than to the receipt/absent-set/lesson arms that a
   fixture necessarily fails.
3. Fixture stubs for the two real pointers (`control-c1-do-nothing.txt`,
   `control-c2-do-nothing.txt`) were committed so `exists()` could not mask an arm result.

Counter runs below are exit 1 for the non-C1 arms (fixtures carry no r59 receipts); only the
dead-name arm tokens are quoted: presence of `dead=N` / `correction_incomplete` = arm failed,
absence of both = arm awarded (the arm's contribution to `met` at `count-c1.py` measure()).

## Result 1 — constructions the counter DOES count (`dead-uncorrected>0`): no gap

Fixture commit per row; arm values from the frozen module, counter stderr tokens from the frozen
counter at that fixture revision.

| construction | fixture rev | dead | counter token |
|---|---|---|---|
| plain dead-name path cell, no marker `A` | `2cb88dd0` | 1 | `dead=1,correction_incomplete` |
| marker on the **neighbouring** line only `B` | `125c3e1c` | 1 | `dead=1,correction_incomplete` |
| marker line **above two** dead names `L` | `8c778185` | 2 | `dead=2,correction_incomplete` |
| dead name in a markdown link-ref definition `O` | `9007fd37` | 1 | `dead=1,correction_incomplete` |
| marker spelled `R60-CORRECTION:` (case) `H` | `4e51f99b` | 1 | `dead=1,correction_incomplete` |
| marker with ZWSP `r60-correction\u200b:` `I` | `09ec2f80` | 1 | `dead=1,correction_incomplete` |
| CRLF file, marker on previous line | n/a (arm) | 1 | — |

Arm micro-probes (same module): `marker_no_colon` dead=1; `marker_trailing_space`
(`r60-correction :`) dead=1; `marker_fullwidth_colon` (`r60-correction：`) dead=1;
`dead_name_in_html_comment` dead=1 (over-strict direction: a *cleaned* line that merely mentions a
dead name inside an HTML comment is flagged — safe, worth knowing).
Cross-wired correction pointers (`R`: c1's line names c2's real pointer) → `dead=0` but
`correction_incomplete` — caught.

So the three headline probes in the seat brief all resolve as **counted** for the neighbour-line
form and for the name-inside-a-path form, and **not counted** only where noted next.

## Result 2 — constructions that reach `dead=0` AND `corr=True`: the dead-name arm awards

`dead=0` alone is not a gap (the correction mechanism is existential); the arm is gaming-capable
only when `corrected_lines_name_real` also returns True. Measured (`arm` = module, `counter` =
frozen counter tokens):

| # | construction | dead | corr | counter dead-name tokens |
|---|---|---|---|---|
| D1a | **marker line keeps a dead name but names no real pointer**, while one honest pointer line per name exists elsewhere `F`/`P`/`M` | 0 | **True** | none |
| D1b | **correction lines name `…/control-c1-do-nothing.txt.bak`** (real path as substring, `.bak` file does not exist) `Q` | 0 | **True** | none |
| D2a | marker embedded in a **path segment** (`.ufo/waves/r60-correction:/c1-entering.txt`) + honest lines `C` | 0 | **True** | none |
| D2b | marker as a **substring of an unrelated token** (`xr60-correction:y`) + honest lines `G` | 0 | **True** | none |
| D2c | marker hidden in an **HTML comment** on the line that keeps the dead name + honest lines `E` | 0 | **True** | none |
| D2d | marker inside a **code span** (`r60-correction:`) + honest lines | 0 | **True** | none |
| D2e | marker inside a hash-like token (`r60-correction:deadbeef`) + honest lines | 0 | **True** | none |
| D3a | dead name **case variant** (`C1-ENTERING.TXT`, `C2-Entering.Txt`) + honest lines `D` | 0 | **True** | none |
| D3b | dead name with **ZWSP** (`c1-entering\u200b.txt`) + honest lines `N` | 0 | **True** | none |
| D3c | dead name **percent-encoded** (`c1%2Dentering.txt`) + honest lines `K` | 0 | **True** | none |
| D3d | dead name **split by U+2028** + honest lines `J` | 0 | **True** | none |
| — | degenerate: **single-line** SCORECARD with one marker and every dead name on it | 0 | True (arm) | n/a |

Exact snippets that produce each row are the `CASES` dict of the driver
(`drive-cases.py`, scratch), reproduced here in minimal form:

```
F:  | W1 | dead `c1-entering.txt` r60-correction: re-pointed to `…/control-c1-do-nothing.txt` |
    | W2 | dead `c2-entering.txt` r60-correction: re-pointed to `…/control-c2-do-nothing.txt` |
    | W9 | r60-correction: c1-entering.txt still referenced by the historical log |      <- no pointer
Q:  | W1 | dead `c1-entering.txt` r60-correction: re-pointed to `…/control-c1-do-nothing.txt.bak` |
E:  | W1 | <!-- r60-correction: obsolete --> `c1-entering.txt` | dead |
C:  | W1 | `.ufo/waves/r60-correction:/c1-entering.txt` | dead |
D:  | W1 | `.ufo/waves/round-59/evidence/C1-ENTERING.TXT` | dead |
```

## Defect classification (counter bug vs predicate loophole)

**D1 — counter under-enforces its own frozen predicate (real defect, fixable in the counter).**
Contract `:40-43` says "every corrected line names the real committed pointer it supersedes the
dead name with". The implementation (`corrected_lines_name_real`, `:88-101`) checks only that
*some* line per name contains name + marker + `real in ln`. Two consequences, both measured:

- `F`/`P`/`M`: a line carrying the marker and a dead name **without** any real pointer is exempt
  from `dead_uncorrected` (whole-line skip, `:80-84`) and is never checked for a pointer by
  `corr`. The SCORECARD keeps the dead pointer verbatim, annotated only with a bare
  `r60-correction:`. This is exactly the primitive the dead-name arm was built to forbid.
- `Q`: `real in ln` is a **substring** test, so `…/control-c1-do-nothing.txt.bak` (or any path with
  the real path as a segment) satisfies "names the real committed pointer" while the committed
  pointer is not the named one — false provenance. `exists()` is checked against the fixed
  `REAL_POINTERS`, never against what the line actually names.

Both are false-met capable: a SCORECARD using `F` + `Q` (or `E`) yields
`dead-uncorrected=0` and no `correction_incomplete`, i.e. the dead-name arm contributes no failure
toward `C1=met`. They are also **outside** the counter's own selftest (`:240-262` tests only
`dead_plain`, `dead_corrected`, `corrected_names_real`, one pointer-missing row and absent-set
shapes; no marker-without-pointer, hidden-marker, case-variant or `.bak` case), so
`C1_SELFTEST pass=6 fail=0` cannot see them.

**D2 — predicate loophole, counter faithful (claim-shape defect, needs a predicate amendment).**
`C`, `G`, `E` (and code-span/hash-token variants) put the literal marker on the line but not as a
correction annotation. `dead_uncorrected` is a faithful reading of "lines carrying the literal
marker", so the counter is not wrong *relative to the frozen sentence*; the sentence is what fails
to require a visible, standalone marker. Consequence a reviewer can see without tooling: in `E`
the HTML comment is stripped by any Markdown renderer, so the rendered SCORECARD shows
`` `c1-entering.txt` `` with **no visible correction at all**, while `C1` scores the arm clean.

**D3 — literal-only name matching (predicate loop, lower severity).**
`D`/`K`/`J`/`N` keep a dead *pointer under a different spelling* (case, percent-encoding, ZWSP,
line-separator) with `dead=0`. Literal reading of `:40-41` ("no occurrence of `c1-entering.txt` or
`c2-entering.txt`") permits it; a case-insensitive consumer or a human reader still sees the dead
name. No retraction of C1 needed — the lane never wrote such a variant — but the arm cannot detect
re-introduction through a name variant.

## Result 3 — the lane's actual C1 is NOT gaming-derived (no retraction of `C1=met`)

- Control reproduces: fresh frozen-counter run at `ddfb12fb…` is **byte-equal** to the committed
  `.ufo/waves/round-60/evidence/control-c1-do-nothing.txt` (`cmp` equal; `rev=ddfb12fb…`, rc 1,
  `dead-uncorrected=2 receipts=0/2 absent-set=0/5 lesson=absent`).
- At freeze `ac496c7c…`: `C1=unmet dead-uncorrected=2 … dead=2,correction_incomplete`, rc 1
  (same signature as the do-nothing control, as contract §9 requires).
- At data-landing `398d3225…` and at observed tip `b3c25613…`:
  `C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c25613…`, rc 0 — the
  contract's frozen target line, modulo the `rev=` placeholder.
- Strict per-line audit of SCORECARD at both revisions (every marker line that carries a dead name
  must carry *that name's* real pointer): **0 violations**. SCORECARD:2950 carries
  `c1-entering.txt` + `control-c1-do-nothing.txt` only; `:2951` carries `c2-entering.txt` +
  `control-c2-do-nothing.txt` only. Both pointers exist at R (`git cat-file -e`, both ok), and the
  r59 wave-1 reports contain no dead-name citation at R (`git grep -c` over
  `.ufo/waves/round-59/w1` at `b3c25613` → no matches), so routed defect 1 is closed on the
  report side too.
- Remaining dead-name mentions at R are outside the frozen arm's scope by design and are
  narrative, not pointers: `corpus/lessons/round-60.md:67`, `corpus/QUALITY.md:1596-1598`,
  `.ufo/waves/round-50/a2w1/Mo50bScribeQuality.md:253` (plus the contract/counter/spec files that
  must name the strings). Note the scope asymmetry: routed defect 1 was "report+SCORECARD", the
  frozen arm counts `SCORECARD.md` only; that is benign at R but is the reason the report side is
  unverified by the counter.

## Impacted axes

- C1 (calibration, score 5), dead-name arm only. `count-c2.py` reads neither SCORECARD nor the dead
  names; `count-c3.py` references `count-c1.py` only by path/pin (`count-c3.py:53`). So no C2/C3
  impact and no re-score of their met-at-freeze evidence.
- Not a met-flip at R (Result 3): the scored C1 is pointer-honest by the stricter reading, and the
  kill rule is untouched (`795c1f31…`, `a444e270…`).

## Smallest safe correction (for the next round's amendment, not applied here)

1. In `corrected_lines_name_real`: replace the existential search with a per-line rule — for every
   line containing `CORRECTION_MARKER` and a dead name, require the corresponding real pointer
   **on that same line**, matched token-boundary-exact (backtick-delimited or
   `(?<![\w./-])<path>(?![\w./-])`), which kills `F`/`P`/`M` (bare-marker lines) and `Q`
   (`…txt.bak` substring).
2. Freeze the marker as a standalone token, not a substring: require
   `(?<![A-Za-z0-9_])r60-correction:` at a cell/word boundary and reject occurrences inside HTML
   comments and code spans (kills `C`/`G`/`E` and the single-line degenerate form). This changes
   the predicate sentence, so it must be an amendment recorded before any seat scores.
3. Add the four missing selftest cases (`marker_line_without_pointer`, `pointer_suffix_bak`,
   `comment_hidden_marker`, `name_case_variant`) and pin the new `C1_SELFTEST` count; without them
   the selftest cannot regress-detect either D1 or D2.
4. Optionally normalise the dead names before counting (case-fold + percent-decode + strip Cf/ZW)
   to close D3; state it in the predicate, since case-folding changes what "occurrence" means.

## Hygiene

- Every file access absolute; fixture repo created with `mktemp -d -p $HYAKU_SCRATCH/mori-r60/Mo60Critic27`
  and `git -C` throughout; no lane/VCS mutation (`git status` shows only untracked wave artifacts
  that were already there); no pacman, no tool installs needed; scratch removed before yielding.
- `disk-guard.sh status` read before work: `/fast/scratch/hyaku` 26% used, 600.0G free — green.

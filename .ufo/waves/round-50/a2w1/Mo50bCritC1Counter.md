# Mo50bCritC1Counter — attack on `count-c1.py` (round 50, attempt 2, wave a2w1)

Seat: Mo50bCritC1Counter (critic, leaf; no subagents). Target: the frozen C1 counter
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/count-c1.py` at the landed data
revision `487941b9395e89678af0053cc443cdb49cdee6e3`.

Frozen bytes confirmed identical at the freeze commit, the landed tip and the working tree:

```
$ git -C <lane> show 950e99be6757a52b00e9eb70ae1a1a7bbe2ea379:.ufo/waves/round-50/count-c1.py | sha256sum
2d5c3ee53198124ef001908cc5abba5c71a6fb63773c31ece211b7c6cdae4456  -
$ git -C <lane> show 487941b9395e89678af0053cc443cdb49cdee6e3:.ufo/waves/round-50/count-c1.py | sha256sum
2d5c3ee53198124ef001908cc5abba5c71a6fb63773c31ece211b7c6cdae4456  -
$ sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/count-c1.py
2d5c3ee53198124ef001908cc5abba5c71a6fb63773c31ece211b7c6cdae4456  ...
```

Lane theses attacked: P-C1(a) (Axes Last-change/Evidence cells vs the fleet MANIFEST targets) and
P-C1(b) (SHONEN tally pins vs the instruments and the receipts). Counters, predicates and kill
rules are frozen: every correction below is a *next-round* proposal, not a fix offered for this
round; every survivor is a named limit.

## Method

- One `git clone --shared` of the lane into the seat scratch
  (`/fast/scratch/hyaku/mori-r50/Mo50bCritC1Counter/clone`, `TMPDIR` under the same root; the clone
  top level was checked with `rev-parse --show-toplevel` before the first commit). One commit per
  attack, branched from `487941b9`; `git -C "$clone"` on every call; no fleet, lane, jj or index
  mutation; the fleet MANIFEST was read read-only at the pinned revision.
- Each fixture was scored with the frozen counter and the *real* fleet repository:

  ```
  python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/count-c1.py <fixture-sha> \
    --repo /fast/scratch/hyaku/mori-r50/Mo50bCritC1Counter/clone \
    --fleet-repo /home/vgpnk/Projects/shokunin \
    --scratch /fast/scratch/hyaku/mori-r50/Mo50bCritC1Counter/run-<name>
  ```

  Exit 0 ⇔ `C1=met`. Every output below was observed; nothing is projected.
- Baseline on the untouched landed data (scored before any fixture, same command with the lane as
  `--repo`): `C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0
  manifest=a94551c5bc8d rev=487941b9…`, exit 0, 7.0 s. The landed data is *not* implicated by the
  survivors below; the survivors are forms the counter would accept as `met`.
- Scratch clone and fixture commits are removed at the end of the seat (operator directive); the
  exact edit for every fixture is reproduced in “Reproduction” so a reader can rebuild it.

## Results (one line per fixture; full outputs quoted with each finding)

| fixture | commit scored | counter verdict | false green? |
|---|---|---|---|
| f1_negated_verdict | `cedcee5b0df0b3776cd635ebbedd20ec4f59c173` | `C1=met … mismatches=0 errors=0 hidden=0` exit 0 | **yes** |
| f2_evidence_html_comment | `eeec535567865514a5e071848875be0843123d80` | `C1=met …` exit 0 | **yes** |
| f3_evidence_orig_suffix | `d7485472d5c4603fbb88eed898facc799c384c23` | `C1=met …` exit 0 | **yes** |
| f4_second_axes_section | `9d3315c42ace97dc74aa7e2f9923481060e914f1` | `C1=met …` exit 0 | **yes** |
| f5a_prose_stale_tally | `ee62b461985c259a7d98c88879bd0e1cfdb109e7` | `C1=met … hidden=0` exit 0 | **yes** |
| f5b_fraction_slash_stale_tally | `09cd0f0b56e00980f779fd0a6b7aa61c6fef68da` | `C1=met … hidden=0` exit 0 | **yes** |
| f6_mutant_same_stem_receipt | `44a6e1f391bcdc210ce4ffd06f7d1fb676d40305` | `C1=met …` exit 0 | **yes** |
| f7_symlink_outside_tree | `8b9416820f3bd55203a1bb79658087d957a6c343` | `C1=met … pins=3` exit 0 | **yes** |
| f9_fraction_prefix_foreign | `f2fc9f3971a460b4e701496b0d3252338661e2b9` | `C1=met …` exit 0 | yes (declared-limit shape) |
| f10_fullwidth_pin_digits | `e5810b0ee617f6e61cd80c9c4d5f96aa03d3ad7e` | `C1=met …` exit 0 | no (numerically honest) |
| f15_sc_card_stale_tally | `c1cd29974483ddb91adb35d33ef34eda09a42298` | `C1=met … hidden=0` exit 0 | yes (declared limit) |
| f16_borrowed_verdict_clause | `a6a9913c96ca2a696e57a2e6ad23bd35b4abe25c` | `C1=met …` exit 0 | yes (predicate-literal) |
| f17_pin_tool_exit1 | `769b4c850791116189a3e78dbb783800c9488cdb` | `C1=met …` exit 0 | **yes** |
| f19_score_unchecked | `bb51b077d83c7f3764b34424cb05255e22684d69` | `C1=met …` exit 0 | yes (declared limit) |
| f8_receipt_line_embedded | `33ab8416094f3c216a698049c8e22470bfe520ec` | `C1=unmet … mismatches=1 … failed=mismatch` exit 1 | no — control held |
| f11_pin_number_next_line | `bb107a3eddba44d06118ec5331b1e220ce68a25e` | `C1=unmet … pins=1 … hidden=1 … failed=hidden,pins_floor` exit 1 | false red (declared limit) |
| f12_axis_label_footnote | `b132645590e8a94f941a8c22000efa4559ed2d61` | `C1=unmet … got=rows=0` exit 1 | false red |
| f13_axis_label_zwsp | `a29aca80ec8be265adf0de0a9f038bbee038cbfa` | `C1=unmet … got=rows=0` exit 1 | false red |
| f14_axis_label_bold | `2e3ecdb53d7e24af0316f79a8271471bad806b17` | `C1=met …` exit 0 | no — control held |
| f18_sitecustomize_hijack | `7cb1498b9f99fe795c0c3a2d3253742e1646b822` | `C1=unmet … got=PIN_CHECK_SELFTEST_pass=0_fail=114` exit 1 | mechanism did not reproduce |
| f21_dot_slash_pin | `0940e900cb1518b5c5bb717213b1c5b837da99b2` | `C1=met …` exit 0 | no — control held |

## Survivors (real false greens)

### S1 — a negated verdict word satisfies the substring check (f1)

Counterexample (SCORECARD.md Axes rows, MANIFEST targets for this fleet revision are coverage 47 /
operability 47 / depth 49 / freshness 28 / calibration 49 / adjacency 19, all `improved`):

- depth Last change: `round 49 (not improved, score held); round 31 (improved, score held) before the round-50 correction`
- operability Last change: `round 47 (not improved, score held); round 31 (improved, score held) before the round-50 correction`

Both cells say the opposite of the fleet record. Observed:

```
item axis depth expect=round_49_improved got=ok state=ok
item axis operability expect=round_47_improved got=ok state=ok
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=cedcee5b0df0b3776cd635ebbedd20ec4f59c173
exit=0
```

Evidence: the check is `if verdict not in seg.lower():` (`count-c1.py:140`), i.e. a plain substring
test on the segment `last[m.start():].split(";")[0]`. `"not improved"` contains `"improved"`, and
`"unimproved"` / `"not harmed"` behave the same way for their verdict words. A retest with the
wording `round 49 (score held, the improvement graded at round 31 stands)` (fixture `d7968928`) was
`unmet … got=verdict_word_missing` — the check is on the literal word, not on meaning.

Impacted axes: calibration (the cell contradicts the MANIFEST while `C1=met`); the frozen predicate
wording “names N*'s verdict word” is arguably literal, so the L1 may record this as a predicate limit
rather than an implementation defect. Smallest safe correction (next round): require the verdict
token not preceded by a negator (`not `, `never `, `no `) and not prefixed by `un-`, i.e. match
`(?<!\bnot )(?<!\bnever )\b(improved|harmed)\b` after removing `un<verdict>`.

### S2 — an Evidence pointer that exists only inside an HTML comment (f2)

Counterexample: the depth Evidence cell's only round-49 pointer is wrapped in a comment:
```text
… states the score 5 (<!-- `corpus/lessons/round-49-verifier-spotcheck.md:76` --> see the latest closure)
```
Rendered, the cell names no round-49 file at all. Observed:

```
item axis depth expect=round_49_improved got=ok state=ok
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=eeec535567865514a5e071848875be0843123d80
exit=0
```

Evidence: `if need not in evidence:` (`count-c1.py:142`) matches the raw cell text; the counter has
no markup stage. The lane's own C2 counter does drop comment blocks for its HTML copies
(contract.md, P-C2: “HTML copy: script, style and comment blocks dropped, tags stripped, entities
decoded”), so the machinery and the precedent exist. Impacted axes: calibration.
Smallest safe correction: strip HTML comments (and, ideally, tags) from `scorecard` before
`axes_table`, so the cell text that is measured equals the text a reader sees; fail closed if the
pointer only exists in a comment.

### S3 — the Evidence pointer is matched as a substring of a longer, non-existent path (f3)

Counterexample: the depth Evidence cell now names
```text
(`corpus/lessons/round-49-verifier-spotcheck.md.orig:76`)
```
`.orig` does not exist at R:

```
$ git -C <clone> cat-file -e d7485472…:corpus/lessons/round-49-verifier-spotcheck.md.orig
fatal: path 'corpus/lessons/round-49-verifier-spotcheck.md.orig' does not exist in 'd7485472…'
rc=128
$ git -C <clone> cat-file -e d7485472…:corpus/lessons/round-49-verifier-spotcheck.md
rc=0
```

Observed:
```
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=d7485472d5c4603fbb88eed898facc799c384c23
exit=0
```
Evidence: same substring test at `count-c1.py:142`; `need in evidence` is satisfied by the prefix of
`…spotcheck.md.orig`. Impacted axes: calibration. Smallest safe correction: require a token-bounded
match (`(?<![\w./-])` … `(?![\w.])`), or extract the pointer as a path and require
`exists(pointer)`.

### S4 — a second `## Axes` section is silently ignored (f4)

Counterexample: keep the honest table and append a second `## Axes` section at the end of
SCORECARD.md whose Last change cells are the pre-round-50 stale ones (coverage 26, operability 31,
depth 31, freshness 28, calibration 25, adjacency 19, all `MANIFEST.json`). Observed:

```
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=9d3315c42ace97dc74aa7e2f9923481060e914f1
exit=0
```

Evidence: `axes_table` stops at the first `^## Axes\s*$` (`count-c1.py:87`) and both the outer scan
and the row loop break at the next heading, so any later `## Axes` table is never read. The shipped
document then contains two tables with the same canonical heading and different Last-change claims
for four axes: duplicate authority with no signal. Impacted axes: calibration.
Smallest safe correction: count `## Axes` headings outside fences and require exactly one; fail
`no_axes_table`/`axes` when a second one appears.

### S5 — a stale tally in SHONEN prose is invisible to the hidden scan (f5a)

Counterexample: append to SHONEN.md
```text
Note (round-50 housekeeping): the older pin check printed pass 60, fail 0 on the round-48 tree; the pins above supersede it.
```
Observed: `C1=met … hidden=0`, exit 0 (`rev=ee62b461…`).

Evidence: `HIDDEN = re.compile(r"\(\s*\d+\s*/\s*\d+\s*\)|\bpass=\d+|SELFTEST")` (`count-c1.py:52`)
recognises only a parenthesised ASCII fraction, the literal `pass=<digits>`, and the uppercase token
`SELFTEST`. `pass 60, fail 0` matches none of the three. The predicate says “no other tally token
stands anywhere else in SHONEN.md”; a spelled-out stale tally is a tally a reader sees. Impacted
axes: calibration. Smallest safe correction: broaden the hidden scan to
`(?:pass|fail)\s*[=:]?\s*\d+` and a bare `\b\d+\s*/\s*\d+\b`, after normalization (next item).

### S6 — Unicode-normalized stale fractions and zero-width-separated tallies are invisible (f5b)

Counterexample: append to SHONEN.md
```text
Note: the round-48 table showed (60⁄60) for the pin check and (13⁄13) for the unlanded check, and the old prose said `pass=60 fail=0`.
```
(observed code points in the committed bytes: `U+2044` ×2 for the fraction slash, `U+200B` ×2 inside
`pass=…`/`fail=…`). Observed: `C1=met … hidden=0`, exit 0 (`rev=09cd0f0b…`).

Evidence: `HIDDEN`’s fraction alternative uses ASCII `/`, and `\bpass=\d+` requires the `=` adjacent
to `pass`. Meanwhile the same counter *accepts* full-width digits in a pin (f10:
`expect=(１１４/１１４) … state=ok`) because Python `\d` and `int()` are Unicode-aware — the counter is
lenient on digits and strict on separators with no normalization stage. The lane’s own
`tools/mori-pin-check.py` v4 F2 states the opposing convention (“matched after NFKC and zero-width
deletion”). Impacted axes: calibration. Smallest safe correction: NFKC-normalize SHONEN and delete
`U+200B..U+200D`/`U+FEFF` before both `PIN` and `HIDDEN`, as the lane’s own instrument already does.

### S7 — a pin bound to a mutant stub reuses the honest tool’s receipt (f6)

Counterexample: SHONEN’s pin path becomes `python3 tools/archive/mori-pin-check.py --selftest`
`(114/114)`; `tools/archive/mori-pin-check.py` is a five-line stub that prints
`PIN_CHECK_SELFTEST pass=114 fail=0` and exits; the receipt `…/selftests/mori-pin-check.txt` is left
untouched. Observed:

```
item pin python3_tools/archive/mori-pin-check.py_--selftest expect=(114/114) got=PIN_CHECK_SELFTEST_pass=114_fail=0 state=ok
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=44a6e1f391bcdc210ce4ffd06f7d1fb676d40305
exit=0
```

Evidence: the receipt is keyed by `RECEIPT_DIR + stem + ".txt"` where `stem = basename(path)[:-3]`
(`count-c1.py:195`), and nothing compares the pinned command with the receipt’s own recorded command
— which still names the honest tool:
```
$ git -C <clone> show 44a6e1f3…:.ufo/waves/round-50/evidence/selftests/mori-pin-check.txt | head -1
$ python3 tools/mori-pin-check.py --selftest   (git archive of 950e99be…; TMPDIR=<scratch>; 2026-10-26T05:49:15-03:00)
```
So a green pin can be backed by a receipt for a different file, and the pinned instrument can have no
arms at all (the contract names the arms question as a limit, but not the receipt identity
mismatch). Impacted axes: calibration, operability (the SHONEN bullet claims the instructions are
executable). Smallest safe correction: require the receipt to name the pinned repo-relative path
(the `$ python3 <path>` line), or key receipts by full path instead of basename.

### S8 — a pinned path may be a symlink that leaves revision R (f7)

Counterexample: commit `tools/fx-link.py` as a symlink whose blob content is
`/fast/scratch/hyaku/mori-r50/Mo50bCritC1Counter/outside/mutant-instrument.py` (a file outside the
clone and outside the extracted tree that prints `LINK_SELFTEST pass=114 fail=0`), add the receipt
`…/selftests/fx-link.txt` and the pin `` `python3 tools/fx-link.py --selftest` (114/114) ``. Observed:

```
item pin python3_tools/fx-link.py_--selftest expect=(114/114) got=LINK_SELFTEST_pass=114_fail=0 state=ok
C1=met items=9 axes=6 pins=3 boxes=5 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=8b9416820f3bd55203a1bb79658087d957a6c343
exit=0
```

Evidence: `exists()` is `git cat-file -e <rev>:<path>` (succeeds for a symlink blob) and `run()`
executes `[sys.executable, path, "--selftest"]` from the extracted tree (`count-c1.py:307`); the
interpreter resolves the symlink to the absolute target. The tally that makes C1 green is therefore
produced by bytes that are not in R — false provenance, and not reproducible from R alone (the file
exists only on this host). The lane’s own pin-check already treats the sibling class
(`r7_symlink_digest_not_inside`) as a defect. Impacted axes: calibration, operability.
Smallest safe correction: reject a bound path whose blob mode is `120000`, or require
`realpath(tree/path)` to stay under `tree` before running it (and read the tool via `git show`
rather than through the extraction if the two can diverge).

### S9 — the instrument’s exit status is discarded (f17)

Counterexample: replace `tools/mori-pin-check.py` with a stub that prints
`PIN_CHECK_SELFTEST pass=114 fail=0` and then `sys.exit(1)`; pin path and receipt unchanged.
Observed:

```
item pin python3_tools/mori-pin-check.py_--selftest expect=(114/114) got=PIN_CHECK_SELFTEST_pass=114_fail=0 state=ok
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=769b4c850791116189a3e78dbb783800c9488cdb
exit=0
```

Evidence: `q = subprocess.run(...)` (`count-c1.py:307`) is used only for `q.stdout`; `q.returncode`
is never read. The lane’s own `tools/mori-pin-check.py` has the arm `nonzero_rc_with_fail0` →
`unmet`, and the receipts it produces record `exit=0`; the frozen C1 counter does not replicate that
rule, so a failing instrument whose last tally line is green reads as green. Impacted axes:
calibration, operability. Smallest safe correction: require `q.returncode == 0`, or compare it with
the exit code recorded in the receipt.

## Declared-limit survivors (the predicate itself admits them)

### S10 — the Score column and score deltas are unchecked (f19)

Set the coverage row’s Score cell to `9` and its Last change to `round 47 (improved, score 6 → 9)`
(no closure states any new number). Observed `C1=met …`, exit 0 (`rev=bb51b077…`). The contract
already names this (“the Score column is not checked”); it is recorded here because the assignment’s
“Score claims a change no closure states” form is otherwise unrepresented. Impacted axis:
calibration. Correction (next round): compare Score cells with the last score a closure states, or
drop the claim that the table’s scores are calibrated.

### S11 — the hidden scan covers SHONEN.md only (f15)

Insert `; PIN_CHECK_SELFTEST pass=60 fail=0 on the old tree` into the operability Evidence cell of
SCORECARD.md. Observed `C1=met … hidden=0`, exit 0 (`rev=c1cd2997…`): a stale instrument tally
stands in the self-assessment and is not counted. Declared in contract.md’s C1 named limits
(“the hidden scan covers SHONEN.md only”). Impacted axes: calibration. Correction (next round): run
the same hidden scan over SCORECARD.md’s Axes section.

### S12 — the verdict word may come from a clause about another round (f16)

Depth Last change `round 49 (score held, round 31 improved the entry, no new number)`. Observed
`C1=met …`, exit 0 (`rev=a6a9913c…`). The segment contains `improved` about round 31; the cell does
not claim round 49 improved. Predicate-literal (“names N*'s verdict word”), so this is a limit of the
wording, not of the code’s reading of it. Impacted axis: calibration. Correction (next round): bind
the verdict word to the same parenthetical as the round token.

### S13 — the fraction-form pin has no prefix binding (f9)

Pin `python3 tools/archive/mori-pin-check.py --selftest` `(114/114)` where the pinned stub prints
`WRONG_ARM_SELFTEST pass=114 fail=0`, with the receipt’s tally line replaced to match. Observed:

```
item pin python3_tools/archive/mori-pin-check.py_--selftest expect=(114/114) got=WRONG_ARM_SELFTEST_pass=114_fail=0 state=ok
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=f2fc9f3971a460b4e701496b0d3252338661e2b9
exit=0
```

`ok = int(n) == o_pass and int(m) == o_pass + o_fail` (`count-c1.py:191`) is numbers-only for the
fraction form; the token form (`→ \`PREFIX pass=N fail=K\``) does compare prefixes. A fraction pin
therefore binds to no instrument identity, and the receipt is authored in the same commit, so the
prefix in the receipt is no independent check. Predicate-level: P-C1(b) specifies prefix equality
for the token form only. Impacted axes: calibration. Correction (next round): require the observed
prefix to equal the instrument’s registered prefix (the lane’s registry) for both forms.

### S14 — full-width digits in a pin are accepted (f10)

Pin `(１１４/１１４)` is accepted (`expect=(１１４/１１４) … state=ok`, `rev=e5810b0e…`, exit 0). Not a
false green — `int()` reads it as 114 — but it is the same normalization gap as S6 seen from the
lenient side: the counter reads Unicode digits while the rendered document shows different glyphs.
LOW. Correction (next round): require ASCII `[0-9]` in pins, matching the “ASCII-strict span”
convention the lane’s own instrument states.

## False reds (honest-looking files scored unmet)

### S15 — a paragraph break between a pin and its `(N/M)` → `pins_floor` + `hidden` (f11)

Move `(114/114)` to the line after its pin. Observed:

```
item pin python3_tools/mori-unlanded-check.py_--selftest expect=(17/17) got=UNLANDED_SELFTEST_pass=17_fail=0 state=ok
C1=unmet items=7 axes=6 pins=1 boxes=4 mismatches=0 errors=0 hidden=1 manifest=a94551c5bc8d rev=bb107a3eddba44d06118ec5331b1e220ce68a25e failed=hidden,pins_floor
exit=1
```
This is the contract’s own named limit (“a pin split across lines … is not enumerated”), but the
observed failure has a second component: the orphan `(114/114)` is counted as `hidden`. LOW.
Correction (next round): if it is intended to bind across a line break, match it; otherwise document
that a wrapped pin is two findings.

### S16 — an axis label with a footnote marker is not the axis (f12)

`| coverage[^1] | 6 | …` plus a footnote definition → `got=rows=0 state=mismatch`, `C1=unmet`
(`rev=b1326459…`, exit 1). `mine = [r for r in rows if r and r[0].strip("* ").lower() == ax]`
(`count-c1.py:123`) accepts only asterisks/spaces around the label. A rendered row still names
coverage. LOW. Correction (next round): NFKC-normalize and strip Markdown footnote/link/emphasis
syntax before comparing the label.

### S17 — a zero-width space inside an axis label is unmet (f13)

`| cove<U+200B>rage | 6 | …` → `got=rows=0 state=mismatch`, `C1=unmet` (`rev=a29aca80…`, exit 1).
Visually identical to the accepted bold variant (S18). LOW. Correction: same normalization as S6,
applied to labels.

## Probed non-survivors (controls that held)

- **Receipt tally embedded in other text** (f8): `log: PIN_CHECK_SELFTEST pass=114 fail=0` →
  `… receipt_missing state=mismatch`, `C1=unmet … failed=mismatch`, exit 1. The exact-line test
  `got in [l.strip() for l in receipt.split("\n")]` holds.
- **`**coverage**` label variant** (f14): `C1=met`, exit 0 — `strip("* ")` handles it; the assigned
  variant is not a hole.
- **`./tools/mori-pin-check.py` pin** (f21): `C1=met`, exit 0 — git normalises `rev:./path`, so the
  dot-slash form is not a false red.
- **Interpreter-start hijack via `tools/sitecustomize.py`** (f18): a committed
  `tools/sitecustomize.py` that registers an `atexit` tally does *not* run — CPython imports
  `sitecustomize` before the script directory enters `sys.path`. Observed on a standalone probe
  (`python3 tools/t.py` with a `sitecustomize.py` in the same directory printed no injected line;
  `PYTHONPATH` was required for the import). The fixture scored `C1=unmet … got=PIN_CHECK_SELFTEST_pass=0_fail=114`
  (exit 1), i.e. the pinned broken tool’s own tally was read. Recorded so no later seat re-tests it
  as an open hole. (This is not a statement that no interpreter-start vector exists; only that this
  one does not.)

## Impact summary against the lane axes

- calibration: S1–S6, S8, S15–S17 (the measurement of “self-assessment matches observed state”).
- operability: S7, S8, S9 (the SHONEN pins claim an executable, receipted instruction set; a stub,
  an out-of-R symlink or a failing instrument can present as executable).
- depth / freshness / coverage / adjacency: none directly; S11 puts an unchecked tally in the
  evidence cells that feed those rows’ provenance reading.

## Reproduction (scratch removed at seat end)

For each fixture: clone the lane once (`git clone --shared <lane> <scratch>/clone`, verify
`rev-parse --show-toplevel`), `git -C clone checkout -f -B fx 487941b9…`, apply the edit below,
`git -C clone add -A`, `git -C clone -c user.name=… -c user.email=… commit`, then score with the
command in “Method”.

| fixture | edit on `487941b9` |
|---|---|
| f1 | depth cell `round 49 (improved, score held);` → `round 49 (not improved, score held);`; operability cell `round 47 (improved, score held); round 31` → `round 47 (not improved, score held); round 31` |
| f2 | depth Evidence cell `(`corpus/lessons/round-49-verifier-spotcheck.md:76`)` → `(<!-- `…:76` --> see the latest closure)` |
| f3 | same pointer → `(`corpus/lessons/round-49-verifier-spotcheck.md.orig:76`)` |
| f4 | append at EOF: `## Axes` + the 6-row table with the pre-round-50 Last-change cells (26/31/31/28/25/19, all `MANIFEST.json`) |
| f5a | append to SHONEN: `Note (round-50 housekeeping): the older pin check printed pass 60, fail 0 on the round-48 tree; the pins above supersede it.` |
| f5b | append to SHONEN: `Note: the round-48 table showed (60<U+2044>60) for the pin check and (13<U+2044>13) for the unlanded check, and the old prose said \`pass<U+200B>=60 fail<U+200B>=0\`.` |
| f6 | SHONEN pin path `tools/mori-pin-check.py` → `tools/archive/mori-pin-check.py`; add `tools/archive/mori-pin-check.py` printing `PIN_CHECK_SELFTEST pass=114 fail=0` and exiting 0 |
| f7 | commit `tools/fx-link.py` as a symlink to an absolute path outside the clone printing `LINK_SELFTEST pass=114 fail=0`; add receipt `…/selftests/fx-link.txt`; add SHONEN pin `(114/114)` |
| f8 | receipt line → `log: PIN_CHECK_SELFTEST pass=114 fail=0` |
| f9 | as f6 but the stub prints `WRONG_ARM_SELFTEST pass=114 fail=0`, and the receipt’s tally line is replaced the same way |
| f10 | SHONEN pin `(114/114)` → `(１１４/１１４)` |
| f11 | SHONEN pin `(114/114)` moved to the following line |
| f12 | `| coverage | 6 |` → `| coverage[^1] | 6 |` + `[^1]: …` at EOF |
| f13 | `| coverage |` → `| cove<U+200B>rage |` |
| f14 | `| coverage |` → `| **coverage** |` |
| f15 | operability Evidence cell: `(`SCORECARD.md` round-24 measured outcome)` → `(`SCORECARD.md` round-24 measured outcome; PIN_CHECK_SELFTEST pass=60 fail=0 on the old tree)` |
| f16 | depth Last change → `round 49 (score held, round 31 improved the entry, no new number)` |
| f17 | replace `tools/mori-pin-check.py` with a stub printing `PIN_CHECK_SELFTEST pass=114 fail=0` then `sys.exit(1)` |
| f18 | add `tools/sitecustomize.py` registering an `atexit` tally; replace the pinned tool with one printing `PIN_CHECK_SELFTEST pass=0 fail=114` and exiting 1 |
| f19 | coverage Score `6` → `9`; coverage Last change `round 47 (improved, score held)` → `round 47 (improved, score 6 → 9)` |
| f21 | SHONEN pin path `tools/mori-pin-check.py` → `./tools/mori-pin-check.py` |

## Limits of this review / UNVERIFIED

- The counter and predicate are frozen; none of the corrections above is proposed as a round-50 fix.
  A counter change after scoring would violate the freeze.
- All fixtures live in a scratch clone that is removed at seat end; the commits are reproducible only
  by re-applying the table above (same base `487941b9`, so the inputs — MANIFEST at
  `e0144996…`, tools, receipts — are reproducible; commit hashes will differ by author date).
- I did not judge the landed data: I ran the counter on it (met) and read the Axes rows and SHONEN
  pins, but I did not verify the lane tools’ arms (that is the pin-check instrument’s own claim) or
  re-read every MANIFEST closure.
- Rendered-markdown claims (S2/S3/S4/S16) are stated from Markdown semantics
  (HTML comments and footnote markers are not literal text); I did not run a Markdown renderer over
  the fixture files.
- The `harmed`-negation variant of S1 is untestable against this fleet revision: all six targets for
  mori are `improved` (counter output on `487941b9`), so no `harmed` target exists to negate.
- No host read beyond `disk-guard.sh status`; no kernel-log read; no OOM or cgroup action. No tool was
  installed or upgraded (nothing was needed); no pacman transaction was run. `disk-guard.sh status`
  reported `/fast/scratch/hyaku` at 24 % use / 615 G free before the fixtures were built.

## Findings

1. **HIGH — S1: a negated verdict word passes the substring check.** `count-c1.py:140`
   (`if verdict not in seg.lower():`). Axes cells saying `round 49 (not improved …)` and
   `round 47 (not improved …)` score `state=ok` (`C1=met`, exit 0) against MANIFEST targets
   `improved`. Concerns `SCORECARD.md` Axes rows; fix: negator-aware verdict match (frozen this
   round, so a named limit).
2. **HIGH — S4: a second `## Axes` section with contradictory rows is ignored.**
   `count-c1.py:87` (`axes_table` keeps only the first heading). `C1=met`, exit 0 while the document
   carries two `## Axes` tables whose Last-change cells disagree for four axes. Concerns
   `SCORECARD.md`; fix: require exactly one `## Axes` heading.
3. **HIGH — S8: a pinned path may be a symlink leaving revision R.** `count-c1.py:307` plus
   `exists()`/`run()`; `tools/fx-link.py` → absolute out-of-tree file produced the green tally
   (`C1=met … pins=3`, exit 0). False provenance; the instrument’s bytes are not in R. Concerns
   `SHONEN.md` pins and the extraction step; fix: reject mode `120000` / realpath containment.
4. **MED — S2: the Evidence pointer counts when it only exists in an HTML comment.**
   `count-c1.py:142`. `C1=met`, exit 0 with a rendered cell that names no round-49 file. Concerns
   `SCORECARD.md` depth Evidence cell; fix: strip comments before the check (C2 already does).
5. **MED — S3: the Evidence pointer is a substring of a non-existent path.** `count-c1.py:142`;
   `…spotcheck.md.orig` (rc 128 for the file) passed as `…spotcheck.md`. `C1=met`, exit 0. Concerns
   `SCORECARD.md`; fix: token-bounded path match and/or `exists(pointer)`.
6. **MED — S5: `pass 60, fail 0` in SHONEN prose is not a hidden tally.** `count-c1.py:52` (`HIDDEN`);
   `C1=met … hidden=0`, exit 0 while a stale tally stands in SHONEN.md. Concerns `SHONEN.md`; fix:
   broaden the hidden scan.
7. **MED — S6: `(60⁄60)` (U+2044) and `pass​=60` (U+200B) are invisible to the hidden scan.**
   `count-c1.py:52`; `C1=met … hidden=0`, exit 0. Concerns `SHONEN.md`; fix: NFKC + zero-width
   deletion before `PIN`/`HIDDEN` (the lane’s own pin-check v4 F2 does this).
8. **MED — S7: a mutant stub under the honest tool’s basename reuses the honest receipt.**
   `count-c1.py:195` (`RECEIPT_DIR + stem + ".txt"`), no command/identity comparison; pin to
   `tools/archive/mori-pin-check.py` scored `state=ok` with a receipt whose first line names
   `tools/mori-pin-check.py`. Concerns `SHONEN.md` and
   `.ufo/waves/round-50/evidence/selftests/mori-pin-check.txt`; fix: bind the receipt to the pinned
   path.
9. **MED — S9: the instrument’s exit status is discarded.** `count-c1.py:307` (only `q.stdout` is
   used). A tool printing `PIN_CHECK_SELFTEST pass=114 fail=0` then exiting 1 scored `C1=met`,
   exit 0. Concerns `SHONEN.md` pins; fix: require rc 0 / match the receipt’s recorded exit.
10. **LOW — S12: the verdict word may come from a clause about another round.** `count-c1.py:137-140`
    (segment split only on `;`). `round 49 (score held, round 31 improved the entry, no new number)`
    scored `met`. Worked example; predicate-literal. Concerns `SCORECARD.md`; fix: bind the word to
    the round’s parenthetical.
11. **LOW — S13: fraction-form pins carry no prefix binding.** `count-c1.py:191`. A pinned stub
    printing `WRONG_ARM_SELFTEST pass=114 fail=0` scored `state=ok`, `C1=met`. Concerns `SHONEN.md`;
    predicate-level.
12. **LOW — S10: the Score column is unchecked.** `check_axes` (no score read). Coverage Score `9`
    with `round 47 (improved, score 6 → 9)` scored `met`. Declared limit; concerns `SCORECARD.md`.
13. **LOW — S11: the hidden scan covers SHONEN.md only.** `count-c1.py:52`/`parse_shonen`;
    `PIN_CHECK_SELFTEST pass=60 fail=0` inside a SCORECARD Evidence cell scored `met` with
    `hidden=0`. Declared limit; concerns `SCORECARD.md`.
14. **LOW — S14: full-width digits in a pin are accepted.** `count-c1.py:50`/`191` and `int()`.
    `(１１４/１１４)` scored `state=ok`. Normalization asymmetry with S6/S17; concerns `SHONEN.md`.
15. **LOW — S15: a wrapped pin becomes `pins_floor` + `hidden`.** `count-c1.py:49-51`/`parse_shonen`
    (per-line `PIN.finditer`). `C1=unmet … pins=1 … hidden=1`, exit 1 for a pin whose `(114/114)`
    sits on the next line. Declared limit, with the extra `hidden` component; concerns `SHONEN.md`.
16. **LOW — S16: an axis label with a footnote marker is unmet.** `count-c1.py:123`
    (`strip("* ")` only). `| coverage[^1] |` → `got=rows=0`, `C1=unmet`, exit 1. Concerns
    `SCORECARD.md`; fix: normalize Markdown syntax in labels.
17. **LOW — S17: a zero-width space inside an axis label is unmet.** Same line. `C1=unmet`,
    `mismatches=1`, exit 1 for a visually identical label. Concerns `SCORECARD.md`.
18. **INFO — f18 (sitecustomize) did not reproduce**: CPython does not import `sitecustomize` from
    the script directory, so `tools/sitecustomize.py` cannot inject the tally; the fixture scored
    `unmet` on the broken tool’s own line. Recorded to close the hypothesis.

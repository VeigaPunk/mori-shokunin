# Mo49CritContractFreeze — attacking the round-49 frozen contract

Seat: critic, wave w1, round 49. Date 2026-10-25. Lane `mori-shokunin`, entering tip
`b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86`, freeze `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`
(`refs/heads/master`, parent `b3e3453d`).

Scope: the frozen `contract.md` against `count-c1.py`, `count-c2.py`, every receipt under
`evidence/` and every control under `controls/`. I changed nothing in the lane: `git status
--porcelain | grep -vc '^?? '` = 0 before and after all probes; my scratch is
`.scratch/r49-Mo49CritContractFreeze/`. No tool was installed or upgraded. No subagent was dispatched.

A dispatched seat is not an independent judge; this is one wave-1 attack, not a verdict.

## What I verified as holding

1. **Every frozen digest matches.** `sha256sum -c --quiet .ufo/waves/round-49/evidence/freeze-sha256.txt`
   → exit 0, no output (31 paths: contract, both counters, 7 controls, 13 evidence files, 4 source
   copies, 4 assimilation files).
2. **The do-nothing control is the entering tool.** `git show b3e3453d:tools/mori-pin-check.py |
   sha256sum` = `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1` =
   `sha256sum controls/tool-v3-entering.py` — matches `contract.md:46-47`.
3. **Every claimed before/control value equals its receipt** (string comparison, all eight C1
   receipts plus the C2 do-nothing receipt): `C1=unmet junk_met=9 … variants=26` (v3 entering, N1-N9
   `got=met`), `junk_met=18` (always-met and the sniffer), `honest_unmet=8 real=unmet` (always-unmet),
   `junk_met=1` (surface-fixes, N9 only), `junk_met=7` (r11-only, N1-N7), `C1=met … variants=26`
   (merged witness), `C2=unmet … failed=entry_absent,pins`. They match `contract.md:147-153,97`.
4. **Two receipt values reproduce.** With the harness's own argv on the frozen N1 body
   (`run_tool(..., "b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86", s-7034f9174253.md, "2d85e33d…", 26, tmp)`):
   `tool-v3-entering → N1 got=met rc=0 348.3s` and `tool-r48-merged-witness → N1 got=unmet rc=1
   340.0s`, i.e. the receipt's `N1 got=met` and `N1 got=unmet` lines. Both selftest pins reproduce:
   `C1_SELFTEST pass=44 fail=0`, `C2_SELFTEST pass=26 fail=0`.
5. **The merged witness is what the table says it is.** `diff -u tool-v3-entering.py <candidate>`
   for both partials, applied in sequence to v3 with `patch -p0 --forward` (r11 patch applied at
   offset 32), yields sha256 `c30ab6232893d9…` — byte-identical to `controls/tool-r48-merged-witness.py`
   — and its selftest is `PIN_CHECK_SELFTEST pass=65 fail=0`. "Merged mechanically … with `patch`;
   selftest 65/65" (`contract.md:153`) is true, and the witness is not a pre-existing round-48 blob
   (`git log --all --find-object` finds it only in freeze-tree commits).
6. **The controls skip the claimed work.** `controls/stub-always-met.py` is 2 lines,
   `stub-always-unmet.py` 4 lines, and `stub-filename-sniffer.py:6-10` keys on `variant-[JN]` in
   `argv`/`TMPDIR` — opaque handles (`s-<12-hex>.md`, `t-<12-hex>`) therefore leave it always `met`.
   No control reaches `met` except the witness, which `contract.md:54-56` excludes from the claim.
7. **The C2 sweep recomputes.** At `b3e3453d`: `SystemMaxUse` 0/0, `MaxRetentionSec` 0/0,
   `journald\.conf` 0/1 (the one knowledge hit is prose inside S014's entry, no SOURCES row),
   `RuntimeMaxUse` 0/0, `vacuum` 3/12 — exactly `evidence/sweep-journal-rows.txt`.
8. **The C2 "before" cause is real.** `git cat-file -e b3e3453d:corpus/evidence/sources-r49/journald.conf.5.html`
   and `…:corpus/knowledge/journal-reach-r49.md` are both absent at the entering tip, so `pins=bad`
   and `entry_absent` are correct.
9. **`count-c2.py`'s positional reads fit the real registry.** `corpus/SOURCES.md` header has 11
   columns with `status`=7, `opened`=8, `used-by`=10, which is what `count-c2.py:139-162` reads;
   the id space is free (`grep -cE '^\| S'` = 257, max `S484`) and `assimilation/collisions` names
   the 14 ids S471-S484, so S485-S488 are unallocated.
10. **Separability holds at the byte level.** The pin reconciler reads only SKILL.md
    (`tools/mori-pin-check.py:663` `args.skill or root/SKILL.md`; no SOURCES.md read), and no
    SKILL.md digest pin names a `corpus/` path (every 64-hex-bearing row names `tools/…` or
    `.ufo/waves/…`). C2's SOURCES/corpus edits cannot move C1; `count-c2.py` touches no `tools/` or
    `SKILL.md` byte.
11. **The C2 named limit's numbers are right.** `corpus/knowledge/journal-disk-usage-total-r51.md:10`
    records 269M (2026-10-24); `corpus/evidence/sources-r49/host-journal-reach.txt` records 56M
    (2026-10-25), and 19M + 37M = 56M internally.
12. **C1's other named limits are honest.** The K2-K8 classes are absent from `r48.VARIANTS`
    (J1-J8, H1-H4 only), H1-H7 and both real reads gate `honest_unmet`/`real`, and the counter
    never invokes the tool's `--selftest` (`count-c1.py:225-228`).

## F1 (HIGH) — C2's defining new work, the S351 flip, is not part of the predicate

`contract.md:81-83` states the claim *is* the flip: "recorded as a new row whose `teaches` opens
`supersedes S351 —`; S351 itself stays a rejected row". `count-c2.py` never reads column 6
(`teaches`) and never reads the S351 row; `grep -n 'supersedes\|S351\|teaches' count-c2.py` returns
nothing outside the selftest fixture builder (`:257`).

Counterexample (probe `.scratch/r49-Mo49CritContractFreeze/c2-probe.py`, real committed copies at
`0df17b7b`, real `corpus/SOURCES.md` read from git with only four rows appended, entry synthesised
in memory):

```
A no-supersedes-no-flip   met=True C2=met claims=8 located=8 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=0df17b7b…
B S351 row deleted entirely met=True C2=met claims=8 located=8 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=0df17b7b…
```

A: teaches = `no flip sentence here at all` on all four rows. B: the `| S351 |` row is deleted
outright. Both print the full target line. So a landed `C2=met` receipt cannot distinguish a C2 that
performs the claimed assimilation from one that never mentions S351 — and the claim's own
justification ("this claim is that the flip", `:80-81`) would be unearned.

Smallest safe correction: in `count-c2.py`, require (a) at least one cited SOURCES row whose
`teaches` starts `supersedes S351 —`, and (b) the S351 row still parses with `status` = `rejected`;
add the two negative arms (teaches rewritten → `bad_rows`, S351 deleted → `source_rows` red). If
that is not wanted, strike the flip from the C2 surface at `:80-83` and record it as a condition the
predicate does not score. Either way the counter must be re-frozen before wave 2 data.

## F2 (MED) — the code's conditions are wider than P-C2's, with a demonstrated false red

`count-c2.py:136` requires a claim cell of **at least 5 words**; P-C2 (`contract.md:84-93`) states
no such floor. Probe C (same script, first claim cell = `SystemMaxUse bounds journal`, 4 words):

```
C four-word claim cell    met=False C2=unmet claims=8 located=7 quote_missing=0 bad_rows=1 sources=4 source_rows=bad pins=ok provenance=ok failed=bad_rows,source_rows
```

The row is otherwise perfect; `located` drops to 7 only because a bad cell is skipped before the
quote is located. Three separate contract-text problems fall out of this one line:

- the 5-word claim floor is unstated in P-C2 and is locked in by the selftest arm
  `claim_cell_short_unmet` (`count-c2.py:337`), so a concise claim can red a correct entry for an
  unannounced reason;
- `source_rows=bad` (`count-c2.py:184`) is computed from *any* bad row, so the label in
  `contract.md:99-100` reports "source_rows=bad" when the SOURCES rows were fine — the label
  misattributes the failure;
- `provenance=ok` (`count-c2.py:180`) requires every table S-id to appear in a `source:` line among
  the first 14 non-blank lines. P-C2 says only that the entry "opens with `source:` lines"; the
  target label pins `provenance=ok` but the sentence never defines it.

`[INFERENCE]` A fourth asymmetry: the copy is entity-decoded (`count-c2.py:63 html.unescape`) but
the quote is only whitespace-collapsed (`:147-149`), so a quote copied verbatim out of the HTML
source (containing `&amp;`, `&lt;`) can never locate although the visible text does.

Correction: write the claim-cell floor and the provenance rule into P-C2 (or drop them from the
code), and compute `source_rows` from the SOURCES-row check only.

## F3 (MED) — a claimed C2 control arm does not exist

`contract.md:102` says the selftest arms carry "staged entry byte-exact". `count-c2.py` has 26 arms
(`grep -c 'check("'` = 26) and none reads a staged entry: `grep -n 'shokuknow\|effective-retention\|byte-exact'
count-c2.py` is empty. The nearest arm, `no_table_unmet` (`:289-291`), uses a three-line synthetic stub
whose first line happens to read `# staged` — it is not the staged entry's bytes and cannot show
that a byte-exact copy of `journal-effective-retention-r45.md` (or `journal-reach-at-ceiling-r46.md`,
`runtime-journal-reach-is-the-boot-r49.md`) fails. The bullet's "script/style/comment text in a
copy" is likewise tested on `normalise()` directly (`:343-346`), not through `evaluate`.

Correction: add the two arms, or reword `:101-104` to the arm names that exist
(`table_inside_fence_unseen_unmet`, `normalise_drops_*`).

## F4 (MED) — `freeze-sha256.txt` does not cover the imported round-48 counter

`count-c1.py:56-60` imports `.ufo/waves/round-48/count-c1.py` and takes `BASELINE`, `MIN_TALLY`,
`TOOL_TIMEOUT`, `Anchor`, `lines_of`, and all twelve J1-J8/H1-H4 variant functions from it.
`grep -c 'round-48' evidence/freeze-sha256.txt` = 0. Today the file is clean (`git status` shows no
modification; blob `3ade4c5a…` at `b3e3453d`), but an edit to that path would change the frozen
predicate with no receipt line able to notice — exactly the "if working-tree bytes ever differ, the
claim is measured with `git show <freeze>:<path>`" guarantee `contract.md:16-17` does not extend to.

Correction: add `sha256(/…/round-48/count-c1.py)` to `freeze-sha256.txt` (and, better, assert it in
`count-c1.py --selftest`, whose `lane_head_unchanged` arm already parses git), or vendor the needed
functions into `count-c1.py`.

## F5 (MED) — P-C1 says "every run with `--min-tally-pins 26 --baseline-rev 2d85e33d…`"; two runs do not

`contract.md:29-30`. `count-c1.py:269` appends the fixture jobs with `--baseline-rev <fixture c0>` and
`--min-tally-pins 1`, and `count-c1.py:10` repeats the same false sentence in its docstring. Observed
by calling the frozen `plan()` (`TMPDIR=…/r49-Mo49CritContractFreeze python3 - <<EOF … m.plan(L,
"b3e3453d…", scratch)`, 27 jobs):

```
N10  fixture  min_tally=1   baseline=9e70eaf0 repo=w-cd49836ffd9c
H5   fixture  min_tally=1   baseline=9e70eaf0 repo=w-db2ac168323e
(25 lane runs)               min_tally=26  baseline=2d85e33d repo=mori-shokunin
```

Defensible engineering (a 1-pin fixture cannot satisfy a floor of 26), but the predicate as frozen
is not the condition the counter applies. Correction: "every lane run with `--min-tally-pins 26
--baseline-rev 2d85e33d…`; N10 and H5 with `--min-tally-pins 1 --baseline-rev <fixture c0>`" in both
`contract.md:29-30` and the docstring `count-c1.py:10`.

## F6 (MED) — `variants=26` is not a variant count

P-C1 enumerates eighteen junk edits and seven honest edits (`contract.md:26-28`) = 25, plus two
reads of R's SKILL.md = 27 runs. `ORDER` has 27 entries (`count-c1.py:212`; the selftest arm
`order_covers_every_variant` at `:403` asserts `12 + 11 + 2 + 2` = 27), and the label prints
`len(results) - 1` (`count-c1.py:305`) = 26. The number in the frozen predicate is therefore "runs
minus one, whichever one", not 18 + 7. Consequences: the predicate's own enumeration cannot be
reconciled with its label (25 vs 26); the label cannot distinguish "25 variants + 2 real reads" from
"26 variants + 1 real read"; and every receipt carries the same unexplained 26.

Correction: print the counts the sentence talks about (e.g. `variants=25 junk=18 honest=7 runs=27`)
or, minimally, make the sentence say `runs=27` and keep 26 out of the claim. Any change re-freezes
the counter, so this must be decided before wave 2 scores.

## F7 (LOW) — the controls bullet contradicts its own head

`contract.md:49-50` heads the list "Controls (each scored with this counter before data, committed;
none may reach `met`)" and the same bullet lists `controls/tool-r48-merged-witness.py` at
`:54-56`, whose receipt (`:153`) is `C1=met …`. The carve-out sentence follows immediately, but the
head sentence as written is false for a listed member. Correction: split the witness into its own
bullet after the controls list.

## F8 (LOW) — `junk_met` counts a crash as a junk miss

`count-c1.py:299` counts any `g != "unmet"` on a junk expectation, and `:241-244` turns a crash,
`rc ∉ {0,1}` or a `met`/rc disagreement into `got="error"`/`"timeout"`. So an error on a junk variant
increments both `junk_met` and `errors` (`:302`), and the receipt reads as if the tool had answered
`met` on junk. `contract.md:32` says "A tool crash, setup exit or timeout is `errors`, never
`unmet`" — true of `got`, but the two counters are not disjoint. The verdict cannot flip (both must
be 0). Correction: `junk_met = sum(… if g == "met")`.

## F9 (LOW) — "run order follows that hash" overstates the harness

`contract.md:31`. `plan()` sorts jobs by the opaque directory name (`count-c1.py:275`) but `measure()`
submits all of them to a `ThreadPoolExecutor` with `--jobs` workers (`:286`), so only *submission*
order follows the hash; with 3 or 4 workers the observations interleave. The property the sentence
intends (no expect-sorted order, no variant-name order) holds. Correction: write "submission order
follows that hash".

## F10 (LOW) — the "Named limits (before data)" list omits the fixture substitution

`contract.md:60-64` names the K2-K8 gap, the narrower-than-junk pass and the missing `--selftest`
run, but not the fact — disclosed only post-freeze at `:157-161` — that H5/N10 no longer touch the
lane's instrument at all: `fixture_variant` (`count-c1.py:174-203`) builds a three-line registry with
one 2-arm probe script and scores it with `--min-tally-pins 1`. So the honest-move half of the D7
fix is proven on a toy registry, never on SKILL.md's twenty-six pins. A tool may implement the
pin-versus-instrument comparison for that fixture shape (any self-test tally pin must equal the
observed tally in a one-row registry) and be wrong on the lane's multi-row registry without C1
noticing.

Also unverifiable here: the discarded first-draft claim at `:157-160` ("the clone's round-40
`conform.py --selftest` pin fails there") leaves no receipt; SKILL.md:908/910 do carry r38/r39
`conform.py` rows, but a round-40 `conform.py` row is not present at the freeze (UNVERIFIED).

Correction: move the fixture substitution into the named-limits paragraph, since it is a limit the
claim lives with, not a draft note.

## F11 (LOW) — the carried `.scratch` remedy is not in the tree

`contract.md:133-134` says the routed `.scratch/` residue defect is carried with "cleaned at round
end, `.gitignore` entry". `.gitignore` at the freeze is four lines (`.ufo/interactive-sessions/`,
`.ufo/worktrees/`, `__pycache__/`, `*.pyc`) — no `.scratch/` entry — and `.scratch` is a tracked
tree. `git status --porcelain | grep -c '^?? \.scratch/'` = **186** untracked `.scratch/` directories
at the freeze (the C1 control runs' `c1-*` scratch, defaulted inside the repo by
`count-c1.py:332`), plus round-40 `scratch/mori-conform-selftest-*` residue. Correction: add
`.scratch/` to `.gitignore` before the round-end cleanup, or drop the ".gitignore entry" wording.

## F12 (LOW) — one C1 run costs ~6 minutes; a 27-run score is ~50 minutes at `--jobs 3`

Not a contract sentence (the contract states no runtime), but the wave plan depends on it. Measured
on the frozen N1 body at `b3e3453d`: `tool-v3-entering` 348.3 s, `tool-r48-merged-witness` 340.0 s
per run. My full reproduction at `--jobs 3` did not finish inside 1200 s (all 26 staged copies and
27 scratch directories created, no summary line); the receipt's own score therefore cost on the order
of an hour. A wave-2 seat asked to re-score C1 needs that budget, and a receipt that claims a
10-minute run should be read with suspicion.

## Observations (no severity)

- The freeze tree exists in three commits — `0df17b7b` (master), `05d1bab9` and `29674863`
  (`refs/jj/keep/…`) — all children of `b3e3453d` with the identical tree `2956219c…`. Byte-wise the
  freeze is one tree; only the commit count makes `git log --all --find-object` return three hits.
- `count-c1.py` writes fixtures under `--scratch` and points the tool's `TMPDIR` there; no probe of
  mine changed a tracked byte.

## Commands run (all read-only over the lane; scratch under `.scratch/r49-Mo49CritContractFreeze/`)

```
sha256sum -c --quiet .ufo/waves/round-49/evidence/freeze-sha256.txt                     # exit 0
git show b3e3453d:tools/mori-pin-check.py | sha256sum                                   # 85a89a3b…82e1
git show b3e3453d:corpus/SOURCES.md | grep -cE <pattern>; git grep -hE <pattern> b3e3453d -- corpus/knowledge | wc -l
python3 .ufo/waves/round-49/count-c2.py --selftest                                      # C2_SELFTEST pass=26 fail=0
python3 .ufo/waves/round-49/count-c1.py --selftest                                      # C1_SELFTEST pass=44 fail=0
python3 .ufo/waves/round-49/controls/tool-r48-merged-witness.py --selftest              # pass=65 fail=0
python3 .scratch/r49-Mo49CritContractFreeze/c2-probe.py                                 # A met, B met, C unmet
python3 .scratch/r49-Mo49CritContractFreeze/spot-probe.py                               # N1: v3 met, witness unmet
python3 - <<EOF … m.plan(L, "b3e3453d…", scratch) … EOF                                 # 27 jobs, N10/H5 min_tally=1
diff -u base.py surface-fixes.py > f.patch; diff -u base.py r11-only.py > r.patch;
  patch -p0 --forward m1.py < f.patch; patch -p0 --forward m3.py < r.patch; sha256sum m3.py  # c30ab623… = witness
git cat-file -e b3e3453d:corpus/evidence/sources-r49/journald.conf.5.html               # absent (rc 1)
```

## Findings

- **HIGH — `count-c2.py` never checks the S351 flip the claim is built on.** `contract.md:81-83`
  vs `count-c2.py` (no read of the `teaches` column or the S351 row). Probe A/B print the full
  `C2=met …` target line with `teaches` = "no flip sentence here at all" and with S351 deleted.
- **MED — P-C2 is narrower than `count-c2.py`: unstated 5-word claim cell, undefined
  `provenance=ok`, `source_rows=bad` misattribution, entity asymmetry.** `count-c2.py:136`, `:180`,
  `:184`, `:63` vs `contract.md:84-100`; probe C (`bad_rows=1`, 4-word claim, otherwise perfect).
- **MED — a C2 control arm the contract claims does not exist.** `contract.md:102` "staged entry
  byte-exact" vs `count-c2.py` (26 arms, none reads a staged entry; synthetic stub at `:289`).
- **MED — `evidence/freeze-sha256.txt` does not cover the imported `.ufo/waves/round-48/count-c1.py`.**
  `count-c1.py:56-60`; `grep -c round-48 freeze-sha256.txt` = 0.
- **MED — P-C1's "every run with `--min-tally-pins 26 --baseline-rev 2d85e33d…`" is false for N10/H5.**
  `contract.md:29-30` and `count-c1.py:10` vs `count-c1.py:269` (min_tally=1, fixture `9e70eaf0`).
- **MED — `variants=26` is not the count of 25 variants.** `contract.md:26-28` vs `count-c1.py:305`
  (`len(results)-1`), `:212`/`:403` (27 runs).
- **LOW — "none may reach `met`" controls bullet contains the witness that reaches `met`.**
  `contract.md:49-56`, `:153`.
- **LOW — `junk_met` counts `error`/`timeout` as a junk miss.** `count-c1.py:299` with `:241-244`
  vs `contract.md:32`.
- **LOW — "run order follows that hash" is submission order only.** `contract.md:31` vs
  `count-c1.py:275,286`.
- **LOW — the pre-data named-limits list omits the H5/N10 fixture substitution.** `contract.md:60-64`
  vs `:157-161` and `count-c1.py:174-203`; the discarded clone attempt is UNVERIFIED.
- **LOW — the carried `.scratch` remedy (a `.gitignore` entry) is absent.** `contract.md:133-134`
  vs `.gitignore:1-4`; 186 untracked `.scratch/` directories at the freeze.
- **LOW — one C1 run measured ~345 s, so a 27-run score is ~50 min at `--jobs 3`, not ~10 min.**
  `count-c1.py` (no runtime claim); dispatch note and wave-2 budgeting.
- **UNVERIFIED — full 27-run reproduction of `control-c1-tool-r48-merged-witness.txt`.** My
  `--jobs 3` run staged all 27 jobs and was cut off at 1200 s with no summary line; the two-variant
  spot probe and the byte-identical patch merge stand in for it.

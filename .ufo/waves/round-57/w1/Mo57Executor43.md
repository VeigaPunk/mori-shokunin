# Mo57Executor43 — cross-claim no-harm + frozen counter execution (round 57, w1)

Seat: executor, leaf. Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`. Entering
`53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2`, freeze `618562c72a03dc4d17386b715357f863fd327274`.
No lane/fleet code change, no commit or jj mutation in the lane; every probe below ran in a
`git clone --shared` under `/fast/scratch/hyaku/mori-r57/Mo57Executor43/` (removed before yield).
No tool installs, no pacman.

Axes named for this seat: (1) cross-claim no-harm (scope bleed, axis harm), (2) frozen counter
execution on the entering revision, (3) counter-implementation fidelity to the frozen predicate.

## 1. Frozen counters at the entering revision — controls reproduced exactly

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ python3 .ufo/waves/round-57/count-c1.py 53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
C1=unmet rows=0 evidence=bad rev=53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
exit=1
$ python3 .ufo/waves/round-57/count-c2.py 53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
C2=unmet claims=0 source=bad rev=53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
exit=1
```

Byte-identical to `.ufo/waves/round-57/controls.txt` (both lines, both exit codes). At the freeze
commit the same two commands also print `C1=unmet rows=0 evidence=bad rev=618562c7…` and
`C2=unmet claims=0 source=bad rev=618562c7…`, exit 1 — the freeze does not pre-satisfy either
predicate, so the before/after contrast is real, not an artifact of where the freeze landed.

Grounding of the C1 claim subject (the two round-56 demonstrations are real, not fabricated):
`tools/mori-driver-liveness.py` and `tools/mori-vote-bind.py` exist at the entering revision
(`git ls-tree -r --name-only 53e2b47 tools`), and the receipts the claim would cite resolve:
`.ufo/waves/round-56/evidence/c1-at-freeze.txt` = `C1=met selftest=ok fixtures=ok entry=ok row=ok
norem=ok rev=3f494b49…` / `exit=0`, `.ufo/waves/round-56/evidence/c2-at-freeze.txt` =
`C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=3f494b49…` / `exit=0`.

## 2. C1 counter binds the SCORECARD table the lane declares superseded (measured)

`count-c1.py:10` reads the **first** `## Capabilities` section up to the first `## Saturation`:

```python
s = p.stdout.split("## Capabilities", 1)[1].split("## Saturation", 1)[0]
```

At the entering revision that window is `SCORECARD.md:596-603` — the placeholder table whose only
row is `| — none yet — | | | |`. The lane's own text says that table is **not** the register:

- `SCORECARD.md:1953-1954` (at `53e2b47`): "Round 35 (claim C1, calibration). This is the lane's
  current capabilities register …"
- `SCORECARD.md:1958-1959`: "As the current self-assessment this register supersedes the
  `— none yet —` table in the first `## Capabilities` section (left as filed at `d677cf3`) and the
  per-round capability tables …"

So the predicate phrase "the current SCORECARD capabilities table" points at the last
`## Capabilities` section (round-35 register, 18 rows, 5-column key/capability/what/evidence/round
schema), while the frozen counter reads the superseded 4-column placeholder. Measured both ways in
a scratch clone (`git clone --shared`, `git rev-parse --show-toplevel` asserted equal to the clone):

Probe A — two rows added to the **last** `## Capabilities` (the declared register), commit
`478bb4e2a00bf0eab93def1103862d152310dc25`:

```
$ python3 count-c1-repo.py 478bb4e2…        # frozen counter, repo path repointed to the clone
C1=unmet rows=0 evidence=bad rev=478bb4e2a00bf0eab93def1103862d152310dc25
exit=1
```

Probe B — the same two rows added to the **first** `## Capabilities` (the superseded placeholder),
commit `37e94d4b22634ccdd6bed9754defecece179cbc3`:

```
$ python3 count-c1-repo.py 37e94d4b…
C1=met rows=2 evidence=ok rev=37e94d4b22634ccdd6bed9754defecece179cbc3
exit=0
```

Verdict on C1 as frozen: the counter's target table contradicts the lane's declared register. An
implementer who follows `SCORECARD.md:1953-1959` is scored unmet; an implementer who edits the
placeholder the lane calls superseded is scored met.

### 2a. Measured cross-claim conflict with the round-35 instrument

`.ufo/waves/round-35/count-c1.py` reads the **last** `## Capabilities` section
(`count-c1.py:68`, predicate docstring `:5-6`) and requires that register to hold **no other row**
(`extra == 0`). Baseline at the entering revision is green:

```
$ python3 .ufo/waves/round-35/count-c1.py 53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
label=P-C1 rev=53e2b47… register='## Capabilities' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
exit=0
```

On probe A (the round-57 rows placed in that register) the same instrument flips:

```
$ python3 .ufo/waves/round-35/count-c1.py 478bb4e2… --repo <clone>
row `rounds[560].capabilities_added[0]` extra
row `rounds[560].capabilities_added[1]` extra
label=P-C1 rev=478bb4e2… oracle=18 rows=20 matched=18 missing=0 bad=0 extra=2 mismatches=2 C1=unmet
```

On probe B (rows in the placeholder) round-35 stays `rows=18 … extra=0 C1=met`. Therefore the two
frozen instruments bind disjoint tables of the same file, and the round-57 C1 landing has exactly
one safe site: the first `## Capabilities` table. Any landing in the section the lane calls "the
lane's current capabilities register" fails round 57's own counter **and** breaks the round-35
instrument's `extra=0` arm.

### 2b. C1 false-pass vectors in the frozen counter

- `count-c1.py:11` matches the substrings `driver-liveness` / `vote-binding` anywhere in a row, not
  in the Capability cell; `:12` checks only `".ufo/waves/round-56/" in x and "| 56 |" in x`.
  Measured: two rows whose pointers are `.ufo/waves/round-56/NOPE/does-not-exist.txt` and
  `.ufo/waves/round-56/also-missing.txt` still return `rows=2, ok=True` — the predicate's
  "resolvable round-56 evidence pointer" is a literal path-prefix substring, never a resolution.
- Two byte-identical duplicate rows satisfy `len(rows)==2` (`ok=True` measured).
- A row whose *Capability* cell is unrelated but whose prose cell mentions `driver-liveness` fails
  only because `| 56 |` is then absent; the name-cell binding is not enforced at all.
- No arm guards the rest of `SCORECARD.md`: an edit that also rewrote `## Axes` scores or other
  round tables would still read `C1=met`. Round 52/53 counters carried `lane_writes`/pin arms for
  this; round 57's C1 has none, so collateral harm to calibration/coverage is invisible to it.
- False-negative shape: an implementer copying the house style of the round-56 rows
  (`SCORECARD.md:2903-2904`, evidence written as `evidence/c1-at-freeze.txt`) fails, because the
  counter requires the explicit `.ufo/waves/round-56/` prefix (measured: `ok=False`). Same for a
  first-working cell written `56 (round)` instead of the exact cell `| 56 |`.
- `count-c1.py:10` is fragile: `split("## Capabilities", 1)` is a substring split, so it also
  matches a `### Capabilities …` heading; a new heading or TOC line above `SCORECARD.md:596` would
  silently move the measured window. `:9` prints no `rev=` on the git-failure branch, diverging
  from the controls' line format.

## 3. C2 counter is satisfied by an entry that violates three named predicate requirements (measured)

Predicate (`.ufo/waves/round-57/contract.md`): the entry "opens with `source:`, `verified-at:`,
`recheck:`, cites a newly opened source row, contains eight claim rows each with a **located quote
in the source copy**, and states that `unclosed` is a pairing count rather than a present-running
count."

`count-c2.py:12-15` checks only: 8 lines starting `| K`; the token `S548` somewhere in the entry;
`| S548 |` in the registry; the substring `mined` anywhere in the registry; one backtick in each
claim line; the substring `pairing count` anywhere in the entry. Measured on probe B, with an entry
that has **no** `source:`/`verified-at:`/`recheck:` lines, eight quotes that occur in no source
copy, and `S548` mentioned only in prose:

```
$ python3 count-c2-repo.py 37e94d4b…
C2=met claims=8 source=ok quotes=ok rev=37e94d4b22634ccdd6bed9754defecece179cbc3
exit=0
```

Isolated arms (same counter code, synthetic rows):

- `quote_ok` is `all("`" in x and "`" in x …)` — the same test twice; a located quote is never
  looked up in any source copy, and the counter never opens a source copy at all.
- `"mined" in registry` is vacuous: `corpus/SOURCES.md` at the entering revision contains `mined`
  270 times (unrelated rows), so the arm holds regardless of the S548 row's status.
- `"pairing count" in entry` is direction-blind: an entry stating "this is **not** a pairing count"
  reads `claims=8 source=ok quotes=ok` → `C2=met` (measured).
- Claim counting is a `startswith("| K")` prefix, so a table header `| Key | … \`quote\` … |` is
  counted as a claim: 7 real rows + a backticked `| Key |` header → `C2=met` (measured); the same
  header without a backtick gives `claims=9` → `C2=unmet` for an otherwise honest 8-row entry
  (measured). The exact-8 arm is brittle in both directions.
- No "newly opened" arm: the counter cannot distinguish a new S548 row from a pre-existing one
  (S548 is genuinely free at entering — `corpus/SOURCES.md` max id is S547, `^| S548 |` count 0 —
  but the counter would not notice if it were not).

C2 id-space note: `S548` is a *staged* id in the assimilation ledger
(`.ufo/waves/round-44/assimilation/staged-ids:78`, `.ufo/waves/round-45/assimilation/renumber-map.tsv:101`
maps staged `S548 → S551`, never landed; registry max is S547). The frozen counter hardcodes
`S548`, so the implementation cannot pick another id; a later assimilation pass carrying staged
`S548` would collide. Low severity, reported only.

## 4. Cross-claim no-harm, per axis (evidence-backed)

| Axis | Finding |
|---|---|
| calibration | C1 *is* the calibration claim and its measured surface contradicts the lane's declared register (§2). The instrument cannot see collateral SCORECARD edits (§2b), so the axis it claims is the axis least guarded. |
| depth | C2 is the depth claim, measured by token presence only (§3): the counter cannot distinguish depth from restatement. `corpus/knowledge/driver-liveness-r56.md:34,239` already defines `unclosed` ("launches with no same-round close"; "log-shape facts, not health verdicts"), so a C2 entry that paraphrases the round-56 entry passes the counter with no new ground. |
| coverage | Untouched by both predicates; but a C1 landing in the round-35 register would break that round's instrument (§2a), i.e. a previously measured calibration artifact. |
| operability | Registry append is neutral: the lane's own gate reads `appendonly_violations=50` both at the entering revision and at probe B (with the S548 row appended), so a new-id append adds no violation. `AXES.md` — cited twice by the register text (`SCORECARD.md:600` "(`AXES.md` §Capabilities)", `:1953-1954` "the `capabilities` field of the AXES.md SCORECARD contract") — does not exist anywhere in the lane tree at the entering revision (`git ls-tree -r --name-only 53e2b47 | grep -i axes` returns only wave report filenames), so the row schema for the table the C1 counter reads has no local authority. |
| freshness | Neither predicate touches the drift pin or a release recheck; no freshness claim is asserted and none is harmed. |
| adjacency | No tool, fleet or host surface is touched by either predicate; C2's new source row is `own-work`-shaped like S547, no private URL needed. Nothing in the frozen artifacts reaches a sibling lane. |

Scope bleed: the C1 predicate names a table that is ambiguous among three live candidates — the
first `## Capabilities` (counter's choice, declared superseded), the last `## Capabilities`
(declared register, round-35-bound), and the per-round `### capabilities: first demonstrated round
N` tables (`SCORECARD.md:1234,1275,1540,1574,1626,2589,2616,2647,2818`). The contract does not
disambiguate and the counter picks the one the lane calls non-current. That is the single largest
no-harm risk for the wave.

## 5. Verdicts

1. **Frozen controls reproduce exactly** at the entering revision (both counters, both exit codes);
   the freeze commit is also unmet. No fabrication in the control receipts.
2. **C1 as frozen does not measure its predicate**: it reads a table the lane declares superseded,
   scores an honest register landing unmet, scores a placeholder landing met, and is blind to
   collateral SCORECARD harm. Measured conflict with `.ufo/waves/round-35/count-c1.py` (met →
   `extra=2` unmet) if the rows go where the lane says the register is.
3. **C2 as frozen is satisfiable without the predicate's substance**: no header check, no quote
   location, no "newly opened" check, direction-blind "pairing count", vacuous `mined` arm, and a
   claim-count arm that both false-passes (header row) and false-negatives (plain header + 8 rows).
4. **No production or lane harm was caused by this seat**; all probes ran in a shared clone under
   scratch, removed before yield. Registry append and the two new files are the only surfaces either
   predicate would touch, and the append-only gate is neutral to it.

Risk/blocker for the wave (not a request to change frozen bytes): because both counters hardcode
`repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"` (`count-c1.py:6`, `count-c2.py:4`) and accept
no `--repo`, no control can be run hermetically without a repointed copy (this report's probes used
exactly that: a byte-identical copy with only the repo path replaced, kept under scratch). Also, the
honest implementation of either predicate must self-impose what its counter omits — the C1 rows must
go in the *first* `## Capabilities` table with full `.ufo/waves/round-56/…` pointers and an exact
`| 56 |` cell, and the C2 entry must carry the three header lines and quotes that actually occur in
a committed source copy, or the round will record a met verdict for a claim it cannot support.

## 6. Exact commands retained

```sh
# controls (lane, read-only)
python3 .ufo/waves/round-57/count-c1.py 53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2   # exit 1
python3 .ufo/waves/round-57/count-c2.py 53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2   # exit 1
python3 .ufo/waves/round-35/count-c1.py 53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2   # exit 0, met 18 rows
# probe clone (scratch)
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/mori-shokunin lane-clone
git -C lane-clone rev-parse --show-toplevel        # == clone path, asserted before each commit
python3 count-c1-repo.py 478bb4e2…                 # exit 1, rows=0  (rows in the declared register)
python3 count-c1-repo.py 37e94d4b…                 # exit 0, rows=2  (rows in the superseded table)
python3 count-c2-repo.py 37e94d4b…                 # exit 0, met on a fabricated/headerless entry
python3 .ufo/waves/round-35/count-c1.py 478bb4e2… --repo lane-clone   # exit 1, extra=2
python3 tools/mori-sources-appendonly.py 37e94d4b… --repo lane-clone  # appendonly_violations=50 (= entering baseline)
```

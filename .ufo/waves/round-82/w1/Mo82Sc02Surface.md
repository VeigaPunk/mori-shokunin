# Mo82Sc02Surface — C2 retirement reconnaissance: consumers of the r10 drift baseline and the freshness cell

Seat: scout (read-only; no lane file changed except this report). Round 82, wave w1.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Revision read: lane HEAD `08e13729b60382e121956c461f4ad0fd9194553a` (entering `ebcf2c72`), plus the
concurrent working tree at 2026-11-04T07:4xZ. All paths below are lane-relative unless absolute.

## Verdict (front-loaded)

1. **No executable consumer of the real r10 baseline exists.** `tools/` contains no file that names
   `baseline-r10-20261015T2231Z`; the census selftest uses synthetic fixture baselines; the only
   executable reader is the round-82 counter `.ufo/waves/round-82/count-c2.py`, and it requires the
   run to stay red. Retirement therefore breaks no tool.
2. **The retirement carriers are present and P-C2 re-derives met on them.** I replicated the frozen
   predicate in a scratch repo built from the working-tree carriers: `C2=met tokens=64 classified=64
   agreed=64 residual=0 stale=0 retired=1 cell=1`, rc 0. The classification file's 64 stated classes
   agree token-for-token with an independent derivation from the baseline bytes (45
   `added-since-r10`, 19 `value-changed`), matching the freshness cell's stated split.
3. **Two live prose carriers still assert green/red in the wrong tense.** `corpus/README.md:276`
   states the baseline "reads `MORI_DRIFT: none`" in the current Frontier section (false since round
   12), and `corpus/evidence/README.md:770-771` gives a re-run recipe that says "expect exit 0,
   `MORI_DRIFT: none`" (false since round 12; the retirement makes it permanently false). These are
   the only live carriers that would mislead a reader after the retirement. Append, do not rewrite.
4. **The strongest live gate coupling is the classification file's existence.** The new freshness
   cell carries a backticked `corpus/evidence/drift-classification-r82.txt`; the standing
   `tools/mori-claim-sweep.py` resolves every backticked pointer in `## Axes` rows. The file is
   currently untracked. Landing the cell/row without the file breaks the r80 claim sweep
   (`CLAIM_SWEEP_MISMATCH unresolved`) and leaves `count-c2` at `classified=0`. One landing commit
   containing both is required.
5. **`count-c2.py` has a checkout-name-dependent fleet-root default** (`.ufo/waves/round-82/count-c2.py:298`):
   it uses `dirname(repo)` only when the repo path ends in `-shokunin`, else the repo itself. A
   worktree/clone not named `*-shokunin` makes it census the wrong tree. Observed false reading on
   the current counter bytes: `tokens=59 ... stale=19`, rc 1; with `--fleet-root` pinned:
   `tokens=64 ... stale=0`, rc 0. (A pre-repair run of the same case gave `tokens=52`; the default
   line is unchanged by the repair.)

## 1. Hit inventory

Search contract: `grep -rIn --exclude-dir=.git --exclude-dir=.jj -E
'baseline-r10-20261015T2231Z|drift[ _-]pin|--drift|drift-classification|MORI_DRIFT' .`
Total in the lane: **4011 hits** — 315 outside `.ufo`, 3696 inside `.ufo` (542 files).

### 1.1 Live surfaces (315 hits; file:line and class)

| Carrier | Lines | Class |
|---|---|---|
| `SCORECARD.md` | 13, 60 | **record claim, live/graded** — freshness cell and Retired row (working-tree edits; see §4) |
| `SCORECARD.md` | 144, 161, 203, 221, 255, 310, 356, 407, 459, 499, 505–506, 512, 524, 527–528, 540–541, 573, 649, 661, 671, 673, 842, 869, 1275, 1725, 1980 | record claim, history (r2–r20 verdicts, r12 capability, r13 plan, r15 debt wording, r20 claim table, capability-register note). Byte-unchanged. |
| `SCORECARD.md` | 3230, 3250, 3291, 3296, 3348, 3353, 3744, 3809, 3857 | record claim, homonym — `MORI_DRIFT_ADJUDICATE`/`MORI_DRIFT_RECHECK` source-pin family, not the census baseline |
| `SKILL.md` | 165 | **tool/registry** — gate row `drift pin` with `pinned values = corpus/evidence/baseline-r10-…` and `1 failed` |
| `SKILL.md` | 111, 311, 312, 317, 321–322, 539 | tool docs/history (r10 contract summary; 322 already says "reads red from 2026-10-19") |
| `SKILL.md` | 1320, 1321 | homonym — source-pin adjudicator/re-check registry rows |
| `PROVINCE.md` | 549 | **tool inventory** — `tools/mori-census.sh … drift pin … also check a retained drift baseline` |
| `PROVINCE.md` | 158 | history — round-20 appended scope note (re-pin) |
| `corpus/README.md` | 18, 30 | knowledge/lesson index rows (r10 pin, evidence-resolution lesson) |
| `corpus/README.md` | 260, 262, 269, 271, 274, 276, 285 | **Frontier/current capability prose** — line 276 still asserts `MORI_DRIFT: none` |
| `corpus/README.md` | 374 | history — r16 correction note "R10 drift pin remains red debt without a re-pin" |
| `corpus/README.md` | 413–423 (Round21 correction; does not match the five patterns) | **history/normative correction** — rejects the r20 re-pin; must stay byte-unchanged |
| `corpus/QUALITY.md` | 104 (criterion 41) | **live normative rule** — red pin stays carried debt; re-pin needs a named semantic reason; no cosmetic green |
| `LOG.md` | 229, 280, 468–469, 477, 480–481, 483, 493, 550, 552, 558–559, 603, 605, 669, 679–680, 754, 945, 1055, 1370, 3410, 3495, 3781, 4764 | record claim, history (rounds 1–81 entries); 3410/3495/3781/4764 are the source-pin homonym |
| `tools/mori-census.sh` | 170, 195, 197–198, 213, 397, 403–404, 411, 2724, 2739, 2929, 2945, 2949, 2966, 2970, 2974, 2992, 2995, 3001, 4633, 4635, 4640, 4645, 4664–4665, 4671–4672, 4682–4683, 4692–4693, 4697, 4702–4703, 4709, 4723 | **tool behaviour** — usage/contract docs, `run_pin`/`run_drift`, and the synthetic drift selftest arms (5 arms + 2 CLI arity) |
| `tools/mori-drift-adjudicate.py` | 33, 109, 117, 121, 185, 229, 309, 342, 345, 363, 380 | tool behaviour, homonym (source-pin adjudicator; `MORI_DRIFT_ADJUDICATE`) |
| `tools/mori-drift-recheck.py` | 96, 221, 226, 235, 246, 251, 257, 265, 336, 341, 370, 514, 608, 611, 630, 647, 656 | tool behaviour, homonym (source-pin re-check; `MORI_DRIFT_RECHECK`) |
| `tools/mori-ua-variance.py` | 67, 99, 168, 332, 337, 342 | tool behaviour, homonym (consumes a `MORI_DRIFT_RECHECK` summary, not a census baseline) |
| `tools/mori-round13-regressions.py` | 209 | tool behaviour comment — duplicate ids would break `--drift` line pairing; no baseline read |
| `corpus/knowledge/drift-pin-r10.md` | 1, 27–28, 41, 50, 52, 69–70, 140, 189, 208–209, 227–228, 230, 242, 262–266, 279, 296, 298 | knowledge entry (r10 design + round-12 erratum recording red since 2026-10-19) |
| `corpus/knowledge/drift-repin-r20.md` | 4–5, 12, 16, 61, 76 | knowledge entry (rejected r20 re-pin / erratum) |
| `corpus/knowledge/audit-r11.md` | 52, 121, 134, 143, 158, 164, 169, 279, 401 | knowledge entry (audit of the r10 baseline/recipe) |
| `corpus/knowledge/` others | `census-cgroup-levels-r45.md:11,42`; `journal-positive-evidence-r15.md:329`; `roster-truth-r12.md:21`; `silence-cutover-r3.md:253`; `verdict-contract-r13.md:148,195`; `verdict-machine-r4.md:330`; `verdict-machine-r5.md:216` | knowledge entries, contextual/homonym mentions |
| `corpus/lessons/` | `2026-10-15-settle-evidence-references-with-artifacts.md:20,33,44,54–55,58–59,62–63,71,74,77,114,130`; `2026-10-15-volatile-contract-behavioral-baselines.md:85,161,213–217,229`; `round-12.md:38,72,86,88`; `round-13.md:94`; `round-13-verifier-spotcheck.md:25`; `round-14-verifier-spotcheck.md:94,139`; `round-15.md:49`; `round-15-verifier-spotcheck.md:290`; `round-16.md:37,41`; `round-16-verifier-spotcheck.md:224`; `round-17.md:79`; `round-20.md:23`; `round-56.md:61`; `round-65/66/67/69/73/75/76/77-verifier-spotcheck.md` (one each); `round-82.md:114` | lesson history; one calibration nit at `round-82.md:114` (§7) |
| `corpus/evidence/` | `README.md:97,685,691,701–702,709,724,755,770–771,776–777,781`; `pin-r10-…-{drift,pin,selftest}.log`; `drift-r12-…` (2 files); `drift-classification-r20.json`; `loss-accounting-r21.json`; `effective-disposition-r21.json`; `baseline-r10-…`; `baseline-r20-…`; `roster-r12-…-selftest.log`; `sources-r59/w1-results-r56.json`; **new** `drift-classification-r82.txt:3` | evidence artifacts/index (historical receipts + the new classification) |
| `considerthese/` | `2026-10-19.md` (3), `2026-10-20.md` (2), `2026-10-21.md` (1) | other — operator reflections; history |

No live hit exists in `SHONEN.md` or `scripts/`, and no executable outside `tools/` and `.ufo/` names the baseline.

### 1.2 Frozen history (`.ufo`: 3696 hits, 542 files)

Every `.ufo` hit is a frozen round artifact — contracts, wave reports, evidence, counters, and
assimilation snapshots — not a live consumer. Largest subtrees: `round-20` (130 files), `round-15`
(48), `round-42` (41), `round-43` (27), `round-21` (27), `round-16` (26), `round-17` (24),
`round-13` (24), `round-14` (22), `round-82` (14), `round-35` (14), `round-47` (13), `round-45`
(10). Reproduce the full file:line enumeration with:

```sh
grep -rIn --exclude-dir=.git --exclude-dir=.jj -E \
 'baseline-r10-20261015T2231Z|drift[ _-]pin|--drift|drift-classification|MORI_DRIFT' \
 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo
```

The only executable `.ufo` readers of the real baseline are `round-82/count-c2.py` (the grader; it
requires red) and `round-20/build-register.py` (annotation only; it contains the token strings, not
a run). No older `count-*.py` reads the baseline: the freshness counters in rounds 36/37/50/52/53/54/55/79
grade `SCORECARD.md` cell text, not this file.

## 2. What the retirement must change, and what must stay byte-unchanged

### 2.1 Must change (the whole honest delta)

1. `SCORECARD.md:13` — the freshness Axes row's **Evidence** cell. The literal
   `round-10 drift pin still red` must go; the cell must carry `r10 pin retired at round 82` and
   `corpus/evidence/drift-classification-r82.txt`, and must keep:
   - the r20 rejection pointer (`corpus/README.md` Round21 correction) — it is why this is not a re-pin;
   - the admitted-closure sentence (`corpus/lessons/round-28-verifier-spotcheck.md:92`);
   - `SCORECARD.md:1781` and `corpus/lessons/round-14-verifier-spotcheck.md:87`.
   The **Last change** cell must not move (r50/r52/r79 counters grade it; see §5).
2. `SCORECARD.md` `## Retired` — replace `None.` (HEAD line 58) with a table whose first row's first
   cell is exactly `drift-pin-r10`, and whose row text contains both
   `corpus/evidence/baseline-r10-20261015T2231Z.json` and
   `corpus/evidence/drift-classification-r82.txt`. The row must say the pin remains
   byte-unchanged and red (an acceptance-predicate retirement, never an evidence deletion, never a
   re-pin). This is the row now present at working-tree line 60.
3. `LOG.md` — append a round-82 entry recording the retirement, the classification file, the red
   reproduction and the counts. (Not graded by P-C2, but the lane's record contract requires it.)
4. `corpus/evidence/drift-classification-r82.txt` — must land **in the same commit** as items 1–2;
   without it `count-c2` reports `classified=0` and the standing claim sweep reports an unresolved
   pointer (the cell's backticked path). 64 `DRIFT_CLASS <token> <class>` lines + 5 comment lines now
   exist untracked; verified (§6).

### 2.2 Must stay byte-unchanged (history / evidence / live norm)

- `SCORECARD.md` lines 144, 161, 203, 221, 255, 310, 356, 407, 459, 499, 505–506, 512, 524,
  527–528, 540–541, 573 (r2–r11 verdicts, including the r10 "`MORI_DRIFT: none` exit 0" admission and
  the r10 freshness-improved row), 649, 661, 671–673 (r12 correction/capability and the superseded
  r13 re-pin plan), 842, 869 (r14/r15 "declared debt" wording), 1275 (r20 claim table), 1725, 1980
  (capability-register note). Also the r-round freshness cells at `SCORECARD.md:1100` and `:1246`
  ("r10 red remains carried") — outside the five-pattern hit set but the same history.
- `corpus/README.md:413–423` — the Round21 correction rejecting the r20 re-pin; this is the reason
  retirement is not re-pinning. Also `corpus/README.md:406–411` (historical round-20 row) and
  `:374` (r16 note).
- `corpus/knowledge/drift-pin-r10.md` — the r10 design/evidence entry (its own round-12 erratum
  already records red since 2026-10-19; kept as filed).
- `corpus/knowledge/drift-repin-r20.md` — rejected re-pin + erratum; kept.
- All `corpus/lessons/*`, all `corpus/evidence/pin-r10-*`, `drift-r12-*`,
  `drift-classification-r20.json`, both baselines — evidence/history, byte-unchanged.
- `LOG.md` rounds 1–81 — history, byte-unchanged.
- `corpus/QUALITY.md:104` (criterion 41) — live norm, byte-unchanged: a red pin stays carried debt;
  a re-pin needs a separately reasoned semantic review; a re-pin that only turns red green is
  rejected. The retirement must satisfy it by keeping the red and the bytes, not by claiming green.
- `SKILL.md:165` and `PROVINCE.md:549` — earlier lines are under the lane's append-only registry
  convention (r73/r76/r79 sections: earlier lines byte-and-line-number unchanged). They are not
  rewritten; see §4 for the compliant append.

## 3. The `MORI_DRIFT:` token grammar, from the code

`tools/mori-census.sh` (current tip):

- `drift_normalize` (:2776–2800) masks declared volatile values to `<V>`; non-volatile bytes and
  line order survive.
- `drift_line_id` (:2808–2821) gives each canonical line a pairing identity:
  `SURFACE <name>: …` → `SURFACE:<name>`; `FINDING <NAME> severity=…` → `FINDING:<NAME>`;
  `MORI_CENSUS:*` → `VERDICT`; `mori-census *` → `HEADER`; empty line → `BLANK`; anything else →
  the canonical line itself.
- `drift_scan` (:2826–2841) accepts a field only for `key=value` with key shape `[A-Za-z0-9_]+`
  (leading `(` and trailing `;`/`)` stripped); duplicate keys concatenate values, so one occurrence
  cannot hide behind another.
- `drift_field_report` (:2849–2868) emits, per paired line: bare `key` for a changed value,
  `-key` for a field present only in the baseline, `+key` for a field present only live. If no
  key/value difference exists (the difference is a state word, command text, or the verdict roll),
  it falls back to the line's id — the whole-line fallback token.
- `drift_report` (:2874–2910) pairs exact lines first, then same-id lines, then names leftovers:
  `-<id>` removed line, `+<id>` added line; a pure reorder becomes `output-order`; the final report
  is `LC_ALL=C sort -u` and space-joined.
- `run_drift` (:2940–3002) adds `volatile_fields` when the baseline's recorded volatile list differs
  from the current list, and prints `MORI_DRIFT: none` (exit 0) only for byte-equal canonical text
  with no contract token; otherwise exit 1; missing/unreadable/malformed → exit 2.

So a live `MORI_DRIFT:` line can carry: `key` (changed value), `-key`/`+key` (removed/added field),
`-<id>`/`+<id>` (removed/added line, id ∈ `SURFACE:<name>`, `FINDING:<NAME>`, `VERDICT`, `HEADER`,
`BLANK`), `output-order`, and `volatile_fields`. A whole-line fallback token is named by
`drift_line_id`: an atomic `SURFACE:<name>` / `FINDING:<NAME>` / `VERDICT` / `HEADER` / `BLANK` for
the five recognized ids; for an unrecognized canonical line it is the full line text, which the
final space-join can split into several whitespace tokens (so such a fallback is not guaranteed to
be one token in the printed list). The frozen derivation table then classifies the sign-stripped
body.

## 4. Insertion points for the L1 (line numbers at this tip)

Tip state: HEAD `08e13729` = `ebcf2c72` + two record-only commits. Working tree has concurrent,
uncommitted C2/C3 edits. HEAD line counts: `SCORECARD.md` 4143, `SKILL.md` 1367, `PROVINCE.md`
605, `LOG.md` 5061, `corpus/README.md` 877; working tree: `SCORECARD.md` 4145 (C2 row adds 2 lines).

| Item | File and insertion point | State |
|---|---|---|
| Freshness cell | `SCORECARD.md:13` (the only `freshness` row in `## Axes`) | already edited in the working tree; verified §6 |
| Retirement row | `SCORECARD.md` `## Retired` (heading line 56 at HEAD); replace `None.` at HEAD line 58 with a 3-column table. Working-tree table is at lines 58–60, row `drift-pin-r10` at **line 60** | already edited; verified §6 |
| Round-82 record | `LOG.md` — append after the Round-81 section (file ends at line 5061) | missing; L1/scribe |
| Classification file | `corpus/evidence/drift-classification-r82.txt` (new, 69 lines) | present untracked; must land with the cell+row |
| Gate registry note | `SKILL.md` — append a dated section after the current end (line 1367); do **not** edit the `drift pin` row at line 165 (append-only registry home, r73/r76/r79 precedent). Say: the pin is retired as an acceptance predicate; the tool's exit contract (0 none / 1 drift / 2 cannot-evaluate) and the byte-unchanged baseline are unchanged; the replacement is the derived per-round classification | optional but recommended: line 165 still presents the retired baseline as the gate's pinned value |
| Instrument inventory note | `PROVINCE.md` — append after line 605 if annotating; the row at line 549 ("also check a retained drift baseline") remains literally true and is not an acceptance claim | optional |
| Frontier correction | `corpus/README.md` — append a dated note after the r10 bullet (lines 262–289); do not rewrite line 276's present-tense `MORI_DRIFT: none`. State it was green at r10 only, red from 2026-10-19, now classified at `corpus/evidence/drift-classification-r82.txt` and retired as acceptance | recommended for honesty; line 276 is the one live green assertion |
| Evidence recipe correction | `corpus/evidence/README.md:770–771` — that section is bound to the r10 SHAs; append a one-line erratum that the recipe now returns exit 1 and the red is classified, rather than editing the historical expectation | recommended, lower priority |
| Round-82 SCORECARD section | `SCORECARD.md` end (working tree ends at 4145; `## Planned (round 82)` is at 4136) | L1/scribe after measurement |

Do not add the retirement to `SCORECARD.md`'s `## Planned (round 82)` item 2: that text is the
pre-round plan ("re-pin … or retire the pin with a named reason") and is history once executed.

## 5. Consumers and breakage analysis (the important part)

### 5.1 No tool is broken

- `tools/mori-census.sh` never reads the real baseline: its drift selftest arms (:4633–4723) build
  one deterministic synthetic fixture and `--pin` it. I re-ran `--selftest`: `PASS (134 cases, 134
  passed, 0 failed)`, rc 0.
- `tools/mori-claim-sweep.py` pins only one stale literal (`selftest 18 in-memory cases` in
  `.ufo/waves/round-80/claim-pins.json`); it does not pin `round-10 drift pin still red`. Removing
  the red literal does not break it.
- `tools/mori-drift-adjudicate.py`, `tools/mori-drift-recheck.py`, `tools/mori-ua-variance.py` are a
  **different** instrument family (`MORI_DRIFT_ADJUDICATE` / `MORI_DRIFT_RECHECK` over the
  `corpus/SOURCES.md` pin registry). They never name the census baseline.
- The round-82 counter `.ufo/waves/round-82/count-c2.py` is the only executable consumer of the red
  run, and its predicate **requires** the red (`p.returncode == 1`) and a non-empty token list. A
  re-pin or a green reading is `unmet` by construction. Retirement preserves what it grades.

### 5.2 The live couplings that can bite

1. **Classification-file existence (highest).** `tools/mori-claim-sweep.py` extracts backticked
   `corpus|tools|.ufo/...` pointers from `## Axes` rows (`graded_rows`, `pointers` in the tool) and
   reports `CLAIM_SWEEP_MISMATCH unresolved` if the path is absent. The new freshness cell adds
   `corpus/evidence/drift-classification-r82.txt`. The file is untracked right now; if the cell and
   the Retired row are committed without it, the r80 gate turns red and `count-c2` prints
   `classified=0`. Land all three together.
2. **`count-c2.py` fleet-root default (`.ufo/waves/round-82/count-c2.py:298`).** `fleet =
   a.fleet_root or (dirname(repo) if repo.endswith("-shokunin") else repo)`. The canonical lane path
   ends in `mori-shokunin`, so the default is right. A clone/worktree at any other name censuses the
   checkout itself: I observed `C2=unmet tokens=59 ... stale=19`, rc 1, then `C2=met tokens=64 ...
   stale=0`, rc 0, after adding `--fleet-root /home/vgpnk/Projects/shokunin` (a pre-repair counter
   run of the same case gave `tokens=52`). A grader must pass
   `--fleet-root` explicitly when the checkout name is not `*-shokunin`.
3. **Axes `Last change` must not move.** `.ufo/waves/round-79/count-c2.py` grades the `Last change`
   clause only (its docstring names the limit), and `.ufo/waves/round-50/count-c1.py` /
   `.ufo/waves/round-52/count-c1.py` additionally require the Evidence cell to name
   `corpus/lessons/round-28-verifier-spotcheck.md` at `through=49/51`. The working-tree cell keeps
   both the Last change text and the round-28/round-14 pointers, so those counters stay green. A
   future "cleanup" of the cell that drops the older pointers would break r50/r52.
4. **The one green-expecting reader is a doc recipe.** `corpus/evidence/README.md:770–771` says
   "(expect exit 0, `MORI_DRIFT: none`)" for
   `bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json`. It is
   already false since round 12 (the file's own section is SHA-bound history), but it is the only
   carrier that tells a reader to expect success. `corpus/README.md:276` makes the same false
   present-tense claim in the current Frontier section. Neither is a gate; both should get an
   append-only erratum so the retirement is not contradicted by its own docs.
5. **Gate-registry semantics.** `SKILL.md:165` maps `--drift` exit 1 to `failed` and pins the r10
   baseline as the gate's value. A gate-standard reader will keep treating the retired pin as an
   active gate unless the end-of-file note in §4 lands. `PROVINCE.md:549` is descriptive and safe.

### 5.3 Nothing else

No lane script, fleet script, other lane, or hyaku manifest executes the baseline. Fleet hits are
prose reports/frozen manifests; `chousa-shokunin`'s round-31 mutant copies of the census are
source-copy fixtures with an inserted comment and do not read the baseline.

## 6. Verification receipts (commands and outputs)

Run from `/home/vgpnk/Projects/shokunin/mori-shokunin` unless shown otherwise.

```sh
$ git rev-parse HEAD
08e13729b60382e121956c461f4ad0fd9194553a

$ MORI_SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin \
  bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json
MORI_DRIFT: +FINDING:CGROUP_OOM_KILL_CUMULATIVE ... volatile_fields
rc=1
# 64 whitespace tokens; independent derivation with the frozen table:
# added-since-r10=45, value-changed=19

$ sha256sum corpus/evidence/baseline-r10-20261015T2231Z.json
0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478

$ bash tools/mori-census.sh --selftest | tail -1
MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)   # rc 0

$ wc -l corpus/evidence/drift-classification-r82.txt   # working tree, untracked
69    # 5 comment lines + 64 DRIFT_CLASS lines
# cross-check against the live 64 tokens: unclassified=0, stale=0, class-disagrees=0
```

At HEAD (the retirement carriers are not committed there):

```sh
$ python3 -I .ufo/waves/round-82/count-c2.py 08e13729 \
    --scratch /fast/scratch/hyaku/mori-r82/Mo82Sc02Surface
unclassified +FINDING:OOM_KILL_JOURNAL
unclassified +FINDING:ROSTER_SET_MISMATCH
unclassified +FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER
C2=unmet tokens=64 classified=0 agreed=0 residual=0 stale=0 retired=0 cell=0 rev=08e13729b603
rc=1
```

Full P-C2 replication on the working-tree carriers (scratch repo, then deleted; no lane write):

```sh
$ cd /fast/scratch/hyaku/mori-r82/Mo82Sc02Surface/repo   # git init; copied census, baseline,
                                                          # classification, SCORECARD; committed
$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/count-c2.py \
    9e55f8bfae35082286d63533676e93e3692f04ec --repo /fast/scratch/hyaku/mori-r82/Mo82Sc02Surface/repo \
    --scratch /fast/scratch/hyaku/mori-r82/Mo82Sc02Surface \
    --fleet-root /home/vgpnk/Projects/shokunin
C2=met tokens=64 classified=64 agreed=64 residual=0 stale=0 retired=1 cell=1 rev=9e55f8bfae35
rc=0
```

This run is against the counter after its disclosed pre-measurement repair (`count-c2.py` gained a
`KEYSHAPE` branch and duplicate-classification counting while this seat ran; the duplicate count is
0 for the landed file and the 64-token outcome is unchanged). The first replication, on the
pre-repair bytes, printed the same `C2=met ... retired=1 cell=1` line.

Same command **without** `--fleet-root` (the checkout name is `repo`, not `*-shokunin`):

```sh
unclassified +path
unclassified +state_ledger
unclassified +waves_dir
unclassified -age_unreadable
unclassified -aged_unsettled
stale-classification ... (19 lines)
C2=unmet tokens=59 classified=45 agreed=45 residual=0 stale=19 retired=1 cell=1 rev=9e55f8bfae35
rc=1
```

This isolates the fleet-root fragility in §5.2 item 2; the 64-token run is the contract-correct one. The 59-vs-64 gap is the scratch tree being censused instead of the fleet, not a classification defect: the 45 tokens that do occur on both sides agree, and both mismatch directions (`unclassified` live-tree tokens, `stale` fleet tokens) are the wrong-root artifact.

## 7. Limits, unverified items, and sibling-byte nits

- The after-value is not gradeable at a committed lane revision yet, because the retirement
  carriers are uncommitted. I ran the counter at HEAD `08e13729`: `C2=unmet tokens=64 classified=0
  agreed=0 residual=0 stale=0 retired=0 cell=0`, rc 1 — the entering control re-derived, matching
  `evidence/controls-r82.txt`. The scratch-repo run above is the after-value on the working-tree
  carriers, not a landing receipt.
- The live token set is host-state dependent. My run at 07:4xZ produced the same 64 tokens and the
  same 45/19 split as the C2 producer's receipt (`evidence/drift-r82-live.txt`) and the freshness
  cell. A later host change (e.g. the `WATCHDOG_STATE_LAG`/`WATCHDOG_STALE` pair) can still make the
  classification stale at grading time; `count-c2` reports that as `stale` and `unmet` by design.
  This is a frozen-predicate property, not a file defect.
- `corpus/lessons/round-82.md:114` reads "Round-10 drift debt remains red for 72 rounds without a
  complete classification surface". The classification-surface gap is 72 rounds (r10→r82), but the
  pin was **green at r10** (`SCORECARD.md:524–528`, `:573`: `MORI_DRIFT: none` exit 0) and first
  recorded red in round 12 (`corpus/lessons/round-12.md:38`, `corpus/knowledge/drift-pin-r10.md`
  erratum, 2026-10-19). "Red for 72 rounds" overstates the red period by about two rounds. Treat the
  rounds count as "the classification surface was absent for 72 rounds", not "red for 72 rounds".
  File:line: `corpus/lessons/round-82.md:114`.
- `SCORECARD.md:60` says the baseline "predates 16 lane surfaces"; the 16 added SURFACE tokens are
  14 `lane.*` rows plus the two `journal.user`/`journal.system` scopes. The count 16 is right; the
  noun "lane surfaces" is loose. Calibration nit only.
- I verified the C3 contract amendment's three replacement bindings while checking the frozen file:
  `row_tally=19` and `survivors=0` occur once at `075574c83eae`; `wrong=0 fixtures=7` occurs once at
  `482dc48d`; each `row_contains` names one table row at the working tree and each first matching
  row states the bound key. The amendment's claims hold. I did not
  judge the amendment's procedural admissibility (not my seat).
- Tooling: nothing installed or upgraded; no pacman transaction; no service, unit, credential or
  orchestration state touched. Scratch `/fast/scratch/hyaku/mori-r82/Mo82Sc02Surface` removed before
  yield.

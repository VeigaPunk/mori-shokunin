# Mo50bMutC2Counter — mutation test of the frozen C2 counter (round 50, wave a2w1)

- Seat: Mo50bMutC2Counter (leaf; no subagents used)
- MACHINE_ID: `432d02b544a5459ebbff9c42ec68334d`
- Date: 2026-10-26
- Target: `.ufo/waves/round-50/count-c2.py` as landed at `487941b9395e89678af0053cc443cdb49cdee6e3`
- Kill rule (frozen): a mutant is **killed iff `--selftest` exits non-zero**; score runs against R are
  auxiliary observation. Survivors are named limits, not proposals to change the contract.
- Tooling record: no tools installed or upgraded (none needed); pacman untouched; only `python3` (system)
  and read-only `git show` / `git rev-parse` were used. Disk guard before runs: `/fast/scratch/hyaku` at
  24% use, 614.0G free (`scripts/hyaku/disk-guard.sh status`).

## 0. Target identity and baseline (required green)

Pristine bytes, copied to scratch before any run:

```
$ cp <lane>/.ufo/waves/round-50/count-c2.py $S/pristine.py
$ sha256sum $S/pristine.py
533c8403b90e650c786381bbf1394cf327b331936a4111b9faba4abd068ee55d
$ git -C <lane> rev-parse --verify 487941b9395e89678af0053cc443cdb49cdee6e3^{commit}
487941b9395e89678af0053cc443cdb49cdee6e3
$ git -C <lane> show 487941b9395e89678af0053cc443cdb49cdee6e3:.ufo/waves/round-50/count-c2.py | sha256sum
533c8403b90e650c786381bbf1394cf327b331936a4111b9faba4abd068ee55d  -
```

Working tree, landed blob and scratch copy are byte-identical.

Baseline behavioral detector on pristine bytes (scratch lane mirror, see §5):

```
$ python3 $S/lane/.ufo/waves/round-50/count-c2.py --selftest
… 31 PASS lines …
C2_SELFTEST pass=31 fail=0            (exit 0)

$ python3 $S/lane/.ufo/waves/round-50/count-c2.py 487941b9395e89678af0053cc443cdb49cdee6e3 \
    --repo /home/vgpnk/Projects/shokunin/mori-shokunin
C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=487941b9395e89678af0053cc443cdb49cdee6e3
                                      (exit 0)
```

The score line equals the frozen landing receipt in the round tasking, so the baseline is calibrated.
Baseline selftest exit 0 ⇒ mutant verdicts are conclusive.

## 1. Method

Each mutation is one regex-anchored edit applied to a scratch copy with `count=1` and a `matched exactly
once` assert; `difflib` confirmed every mutant differs from pristine by a single hunk and nothing else
(diffs in Appendix A). Every mutant was then run twice:

1. detector: `python3 <mutant> --selftest` — killed iff exit ≠ 0;
2. score: `python3 <mutant> 487941b9395e89678af0053cc443cdb49cdee6e3 --repo <lane>` (read-only git inside
   the counter: `git show` / `git rev-parse` only; the lane repo, its index and jj state were never written).

All scratch state lived under `/fast/scratch/hyaku/mori-r50/Mo50bMutC2Counter/` with `TMPDIR` inside it;
removed at the end (§4).

## 2. Results: 9 killed, 3 survived

Baseline selftest tail `C2_SELFTEST pass=31 fail=0`. Killed mutants fail exactly one arm each (30/31).

| # | Mutation (single point) | Verdict | Failing arm (killed) | Score at R vs baseline |
|---|---|---|---|---|
| m01 | drop `srow[8] == OPENED` conjunct | **killed** | `row_opened_other_day_unmet` | unchanged, `C2=met … located=22` |
| m02 | drop `entry_path in used-by` conjunct | **killed** | `used_by_missing_unmet` | unchanged |
| m03 | drop `q in seen_quotes` | **killed** | `duplicate_quote_unmet` | unchanged |
| m04 | drop `ckey in seen_claims` | **killed** | `breadcrumb_identical_claims_unmet` | unchanged |
| m05 | `MIN_BEYOND = 3` → `0` | **killed** | `claim_echoes_quote_unmet` | unchanged |
| m06 | `MIN_CLAIM_WORDS = 6` → `1` | **survived** | — (31/31) | unchanged |
| m07 | `MIN_SOURCES = 3` → `2` | **killed** | `sources_floor_unmet` | unchanged |
| m08 | evaluate(): `normalise(b) if kind=="html" else normalise_text(b)` → `normalise_text(b)` | **survived** | — (31/31) | **changed**: `C2=unmet claims=22 located=18 quote_missing=4 bad_rows=0 sources=3 … failed=quote_missing` (exit 1) |
| m09 | drop `.replace("\\\|", "\|")` unescape | **killed** | `escaped_pipe_quote_located` | unchanged |
| m10 | drop `if not pins_ok: failed.append("pins")` | **killed** | `pin_mismatch_unmet` | unchanged (line still prints `pins=bad` inside the arm's fixture) |
| m11 | `srow[7] == "mined"` → `in ("mined","queued")` | **killed** | `row_not_mined_unmet` | unchanged |
| m12 | `MAX_WORDS 25` → `99` | **survived** | — (31/31) | unchanged |

Every mutant sha256 and its diff are in Appendix A. The real-rev verdict is `met` under 11 of 12 mutants
and `unmet` (strict direction) under m08; no mutant produced a false `met` at R on today's data.

## 3. The three survivors — mechanisms and limits

### m06 — `MIN_CLAIM_WORDS = 1` (survived)

Instrumented rerun of the mutant's `claim_cell_short_unmet` arm prints:

```
DIAG06-LINE: C2=unmet claims=10 located=9 quote_missing=0 bad_rows=1 sources=3 source_rows=bad pins=ok provenance=ok rev=R failed=bad_rows,source_rows
```

The arm's 2-word claim (`"short claim"`) is still rejected — but by the beyond floor, not the word floor:

```
row-4 selftest quote: 'Amount of memory used in anonymous mappings such'
words_beyond('short claim', q3) = 2        # 2 < MIN_BEYOND → bad row
```

Limit: the 6-word claim floor is not independently enforced by the selftest; its only arm is shadowed by
`MIN_BEYOND`. A entry row whose claim has 1–5 words but ≥3 beyond-quote words would pass the mutant while
the pristine counter rejects it — the selftest would stay 31/31 either way. Score at R unchanged today
(all 22 landed claims are ≥6 words).

### m08 — HTML normalise dropped for the C copies (survived; real score flips to unmet)

`evaluate()` computes each copy's locating text; the mutant forces the HTML copy through plain
whitespace collapse. The selftest stays green because (a) its four S901/cgroup-v2.html quotes sit inside
tag-free, entity-free runs of the raw copy (observed: `honest_met PASS` under the mutant), and (b) the
four `normalise_drops_*` unit arms call `normalise()` directly, which this mutation does not touch — it
edits the per-copy `norm[url]` line in `evaluate()`.

On real data the drop is observable. A per-quote probe over the landed entry and copies (scratch, read-only):

```
row  2 S489 in_normalised=True in_raw_collapsed=False NEEDS-NORMALISE
row  3 S489 in_normalised=True in_raw_collapsed=False NEEDS-NORMALISE
row  4 S489 in_normalised=True in_raw_collapsed=False NEEDS-NORMALISE
row  5 S489 in_normalised=True in_raw_collapsed=False NEEDS-NORMALISE
(all other 18 rows: located under both normalisations)
```

Exactly rows 2–5, all S489 (`corpus/evidence/sources-r50/cgroup-v2.7.2.html`), depend on script/style/
comment dropping, tag stripping or entity decoding — matching the mutant's `located=18 quote_missing=4`.

Limit: the selftest never exercises evaluate-side HTML normalisation across markup boundaries. A future
regression on that line would silently flip real scoring (here toward `unmet`, the strict direction — the
landing genuinely depends on this line for 4 of its 22 quotes) while the selftest prints 31/31.

### m12 — `MAX_WORDS 25 → 99` (survived)

Instrumented rerun of the mutant's `long_quote_unmet` arm prints:

```
DIAG12-LINE: C2=unmet claims=10 located=9 quote_missing=1 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=R failed=quote_missing
```

The arm's 26-word quote (`"memory"` ×26) passes the 6..99 gate, fails only at location, and the output
line always contains the literal label `bad_rows=` — the arm asserts `(not met) and "bad_rows" in line`,
satisfied by `bad_rows=0`. The arm passes for the wrong reason.

Limit: the 25-word quote ceiling is unenforced by the selftest; under this mutant an entry quote of
26–99 words that locates would still count as a valid row and the score would stay `met`. Today's 22
quotes are 7–21 words, so the score at R is unchanged.

## 4. Restoration evidence

- Scratch pristine re-hashed after the campaign: `533c8403b90e650c786381bbf1394cf327b331936a4111b9faba4abd068ee55d`
  (identical to pre-run); post-campaign pristine `--selftest` exit 0 (`results.json: restoration`).
- Lane file re-hashed after all runs:
  `533c8403b90e650c786381bbf1394cf327b331936a4111b9faba4abd068ee55d  .ufo/waves/round-50/count-c2.py`
  — byte-identical; no write, index or jj operation was ever issued against the lane; only read-only
  `git show` / `git rev-parse` ran there. The three source copies used by the mirror were extracted with
  `git show 487941b…:<path>` and hash to the frozen pins (`2d716cb7…`, `8a28e0bc…`, `452f1348…`),
  independently re-proving `pins=ok` at R.
- Scratch removed before finishing (`rm -rf /fast/scratch/hyaku/mori-r50/Mo50bMutC2Counter`), after
  everything cited above was copied into this report.

## 5. Probe notes

- The first baseline attempt failed environmentally, not semantically: `selftest()` resolves the lane as
  three `dirname`s above the script's own path, so a flat scratch copy raised
  `FileNotFoundError: … /fast/scratch/corpus/evidence/sources-r50/cgroup-v2.7.2.html`. Re-run from a
  lane-shaped scratch mirror (`.ufo/waves/round-50/` + `corpus/evidence/sources-r50/`) it is green. Not a
  counter defect; a footgun for anyone re-running the selftest from a copied script (the exit is 1 with a
  traceback, which a naive reader could mistake for a failing detector).
- Per the frozen rules, the counter weaknesses found are recorded as limits only; no change to counters,
  predicates, controls or kill rules is proposed. A dispatched seat is not an independent judge.

## Findings

- **MED** — Selftest coverage gap: `evaluate()`'s per-copy normalisation for the HTML copy
  (count-c2.py:120, `norm[url] = …`) is untested across markup boundaries; mutant m08 keeps the selftest
  at 31/31 while flipping the real score of R to `C2=unmet … failed=quote_missing`. Entry rows 2–5
  (S489, `corpus/evidence/sources-r50/cgroup-v2.7.2.html`) of
  `corpus/knowledge/oom-memcg-stat-r50.md` currently depend on this line to locate. Concern:
  `.ufo/waves/round-50/count-c2.py` (evaluate, pins/normalise block) and the selftest's `honest_met` arm.
- **LOW** — `long_quote_unmet` arm asserts on the substring `"bad_rows"`, which is satisfied by
  `bad_rows=0` in every output line; the 6–25-word quote ceiling (MAX_WORDS) is therefore unenforced by
  the selftest (mutant m12 survives). Concern: `count-c2.py` selftest arm `long_quote_unmet`.
- **LOW** — `MIN_CLAIM_WORDS` is shadowed by `MIN_BEYOND` in its only arm (`claim_cell_short_unmet`;
  words_beyond = 2 < 3 rejects the short claim); lowering the floor to 1 is invisible to the selftest
  (mutant m06 survives). Concern: `count-c2.py` constant `MIN_CLAIM_WORDS` / arm `claim_cell_short_unmet`.
- **LOW** — `selftest()` is lane-layout sensitive (resolves the lane from `__file__` by three `dirname`s);
  a copied counter fails with exit 1 and `FileNotFoundError` outside a lane-shaped tree, which can be
  misread as detector failure. Concern: `count-c2.py` `selftest()` path resolution.
- Positive result (no severity): 9/12 single-point mutants killed, each by exactly one selftest arm with
  no collateral arm failures; the landed `C2=met claims=22 located=22 … sources=3` verdict at
  `487941b9395e89678af0053cc443cdb49cdee6e3` is stable under 11/12 mutants and moves only in the strict
  (unmet) direction under m08.

## Appendix A — mutant hashes and diffs (single hunk each)

Mutant sha256 values (pristine `533c8403b90e650c786381bbf1394cf327b331936a4111b9faba4abd068ee55d`):

```
m01_drop_opened_date_check  2cc2d150d604517a04fb99194c7c95b8040b94a6400d2c62a3edfa038ccff3b4
m02_drop_used_by            73a01ef8da005236f6ba9eafeb7c2ce0fc2d4407519f9fe34d2266ab1ef28bac
m03_drop_unique_quote       5a380d706c02c183013eb77dbaebb6068b6c30035939ffefdd7d6f133d342dad
m04_drop_unique_claim       5149b1338f58cb3cde16f562b596c545a6fbe7fb8e6650ff34dc2368a2276db0
m05_MIN_BEYOND_0            b44843188070715423c9eb8715e16f80c10959ef8176cb0a059479eea2bde37f
m06_MIN_CLAIM_WORDS_1       ae65e97cc2cdd1c9e587e96d487ae905034626fc389a643ee1c79e04f1ad0eee
m07_MIN_SOURCES_2           bf065056fda579e29f6869a22cdc4a4ab29f6aae5da4573242b1f37e02f8a207
m08_no_html_normalise       02b569df7994e4533fa486b7bd811671fa055f0035c8feb4577cba51a973a6dc
m09_drop_pipe_unescape      1cf817d9d9e46e06e2cfc79cbf18d3b06af769d13e34d93833f11acd20a91db9
m10_drop_pin_check          20ccc39497f5c40c4c70fb5b0fe330a240885feaa8e3f410aecd14a52c076908
m11_accept_status_queued    39b5e63da604d059b2f190fed576f1c735b1ae7e99da17b5d8a8968913c7318a
m12_MAX_WORDS_99            3bdc0c546e1f5433c9fedeff5198ca0bf0883238811b5d151b229cfd7f777317
```

Each mutant is byte-exactly reproducible from the pristine bytes plus its hunk below.

```diff
--- pristine +++ m01_drop_opened_date_check
@@ -175,3 +175,2 @@
             row_ok = bool(srow and len(srow) == 11 and url is not None and srow[7] == "mined"
-                          and srow[8] == OPENED
                           and entry_path in [u.strip() for u in re.split(r"[,;]", srow[10])])

--- pristine +++ m02_drop_used_by
@@ -175,4 +175,3 @@
             row_ok = bool(srow and len(srow) == 11 and url is not None and srow[7] == "mined"
-                          and srow[8] == OPENED
-                          and entry_path in [u.strip() for u in re.split(r"[,;]", srow[10])])
+                          and srow[8] == OPENED)

--- pristine +++ m03_drop_unique_quote
@@ -158,3 +158,3 @@
             words = q.split(" ")
-            if (not (MIN_WORDS <= len(words) <= MAX_WORDS) or q in seen_quotes
+            if (not (MIN_WORDS <= len(words) <= MAX_WORDS)
                     or words_beyond(cells[0], q) < MIN_BEYOND):

--- pristine +++ m04_drop_unique_claim
@@ -153,3 +153,3 @@
             quotes = SPAN.findall(cells[2])
-            if not re.fullmatch(r"S[0-9]{3,}", sid) or len(quotes) != 1 or ckey in seen_claims:
+            if not re.fullmatch(r"S[0-9]{3,}", sid) or len(quotes) != 1:

--- pristine +++ m05_MIN_BEYOND_0
@@ -36,3 +36,3 @@
-MIN_BEYOND = 3
+MIN_BEYOND = 0

--- pristine +++ m06_MIN_CLAIM_WORDS_1
@@ -35,3 +35,3 @@
-MIN_CLAIM_WORDS = 6
+MIN_CLAIM_WORDS = 1

--- pristine +++ m07_MIN_SOURCES_2
@@ -34,3 +34,3 @@
-MIN_SOURCES = 3
+MIN_SOURCES = 2

--- pristine +++ m08_no_html_normalise
@@ -120,3 +120,3 @@
-        norm[url] = normalise(b or "") if kind == "html" else normalise_text(b or "")
+        norm[url] = normalise_text(b or "")

--- pristine +++ m09_drop_pipe_unescape
@@ -156,3 +156,3 @@
-            q = re.sub(r"\s+", " ", quotes[0].replace("\\|", "|")).strip()
+            q = re.sub(r"\s+", " ", quotes[0]).strip()

--- pristine +++ m10_drop_pin_check
@@ -121,4 +121,2 @@
-    if not pins_ok:
-        failed.append("pins")

--- pristine +++ m11_accept_status_queued
@@ -174,3 +174,3 @@
-            row_ok = bool(srow and len(srow) == 11 and url is not None and srow[7] == "mined"
+            row_ok = bool(srow and len(srow) == 11 and url is not None and srow[7] in ("mined", "queued")

--- pristine +++ m12_MAX_WORDS_99
@@ -37,3 +37,3 @@
-MIN_WORDS, MAX_WORDS = 6, 25
+MIN_WORDS, MAX_WORDS = 6, 99
```

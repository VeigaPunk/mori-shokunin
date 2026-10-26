# Mo51MutC2Counter — mutation test of `.ufo/waves/round-51/count-c2.py`

Seat: Mo51MutC2Counter (mori round 51, wave w1) · MACHINE_ID: 62104bb113de · 2026-10-26 · lane: mori-shokunin

Scope: the 12 assigned single-point mutations of the frozen C2 counter, each in an isolated scratch copy.
The lane byte `.ufo/waves/round-51/count-c2.py` was never modified (hash identical before the first run and
after the last: `19553792d74d8f3ca9c09e6a018b9c66f61a58e8ad78e72b524a69ec892cfb26`, which also matches
`evidence/freeze-sha256.txt:11`, so the working tree is the frozen byte).

## Method

- Scratch (operator directive 2026-10-25): `/fast/scratch/hyaku/mori-r51/Mo51MutC2Counter/`,
  `TMPDIR=<scratch>/tmp` exported for every run; removed at the end (Cleanup).
- Disk guard before the runs: `scripts/hyaku/disk-guard.sh status` → rc 0, `/fast` at 25 %, 605 G free. No ENOSPC.
- The counter derives its repo (4 dirnames up from `__file__`) and its selftest fixture lane (3 dirnames up)
  from its own path, so a bare scratch copy can neither selftest nor score. Mirror layout used for every run:

  ```
  <scratch>/lane/.ufo/waves/round-51/count-c2.py     # pristine + 12 mutants, one file each
  <scratch>/lane/corpus/evidence/sources-r51/        # the 5 frozen copies, byte-identical
  ```

  Selftest reads the 5 copies from the mirror; scoring runs
  `python3 <mutant> 87e0c374537557754bf71dd68036ded3ddc6699c --repo /home/vgpnk/Projects/shokunin/mori-shokunin`
  (read-only `git show`/`git ls-tree`/`git rev-parse` against the lane; no index or ref touched).
- Byte-faithfulness of the mirror: all 5 copies sha256-match the digests embedded in the counter's `COPIES`
  table (`9f571a04…`, `d6c58074…`, `2d4accbb…`, `e760f716…`, `dba76b26…`), so the selftest's own pin arm sees
  `pins=ok` on pristine bytes.
- Detector per mutant, fixed order: (1) `--selftest` — **killed iff exit != 0**; (2) score the data revision.
  Baseline-failure guard: pristine selftest ran first and exited 0; a pristine failure would have made every
  reading inconclusive. It did not.
- Tooling record: nothing installed or upgraded (python3 already present; pacman untouched per the host-wide
  pause; nothing written to any PATH directory).

## Baseline (pristine bytes)

```
$ python3 <scratch>/lane/.ufo/waves/round-51/count-c2.py --selftest
C2_SELFTEST pass=34 fail=0
rc=0
$ python3 <scratch>/lane/.ufo/waves/round-51/count-c2.py 87e0c374537557754bf71dd68036ded3ddc6699c \
    --repo /home/vgpnk/Projects/shokunin/mori-shokunin
C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=entailment
rc=1
```

Both match the frozen receipts (`evidence/selftest-c2.txt`, `evidence/c2-at-data.txt`).

## Results — 12/12 killed, 0 survived, 0 inconclusive

| mutant | single-point change | mutant sha256 | selftest rc | failing check(s) | verdict |
|---|---|---|---|---|---|
| m01-drop-dissent-check | dissent branch deleted: an overclaim vote no longer registers as dissent, the row falls through to the entailed branch | `873a1f48f074f64d47fb5e363917b70a4663ec74ce48ababd0ec10900efcc4b8` | 1 (pass=33 fail=1) | entail_dissent_unmet | killed |
| m02-no-hash-match | vote lookup ignores the row hash: every recorded vote applies to every row | `2363c9b7d3e20fa47fb75de98e06f01b3dfe9da46aabee6cc52149d5f84612eb` | 1 (pass=32 fail=2) | entail_one_row_unreviewed_unmet, entail_hash_of_other_text_unmet | killed |
| m03-accept-l1-prefix | L1-prefix filename filter dropped: files named `MoriR51*` may carry votes | `953c6dad8476431155eb128b83ae59f31eec26356188efdc580e269f00d7f781` | 1 (pass=33 fail=1) | entail_l1_file_ignored_unmet | killed |
| m04-drop-md-filter | `.md` filename filter dropped: any file under the wave dir may carry votes | `76083a8380ee703ba671b874f3e399107f47818c2020f2b8e14006f14fd57c99` | 1 (pass=33 fail=1) | entail_non_md_ignored_unmet | killed |
| m05-min-sources-4 | `MIN_SOURCES` 5 → 4 | `a663bc8409e9d032bfe48a857d7d5b9c260e8c5eb160cf00f10e926133434c4b` | 1 (pass=33 fail=1) | sources_floor_unmet | killed |
| m06-min-claims-10 | `MIN_CLAIMS` 12 → 10 | `e3918028863c23314f4505024bae22df784261555f493f0f38c82277156d5d25` | 1 (pass=33 fail=1) | claims_floor_unmet | killed |
| m07-drop-opened-date | `srow[8] == OPENED` removed from row_ok | `b2c03cd785622af1e4f84bb15316d3531c4a4c280cb78dfb1ccdec2e20c6a49b` | 1 (pass=33 fail=1) | row_opened_other_day_unmet | killed |
| m08-drop-used-by | used-by cell check removed from row_ok | `a8782cd91fd79c13b567c9b5c84e34567b04b116aabb304eef8ee7b13a83ee74` | 1 (pass=33 fail=1) | used_by_missing_unmet | killed |
| m09-drop-unique-quote | duplicate-quote rejection removed (`q in seen_quotes` gone) | `031d89dac71654589619f25260f7fb892ec673a784ac196c4d16ffd411779e7c` | 1 (pass=33 fail=1) | duplicate_quote_unmet | killed |
| m10-min-beyond-0 | `MIN_BEYOND` 3 → 0 | `23af3e8a77116d04c46e14030f8363e06fec5526eb0e3054905ca56be5f5a3c4` | 1 (pass=33 fail=1) | claim_echoes_quote_unmet | killed |
| m11-drop-pin-check | `failed.append("pins")` block deleted: a copy digest mismatch no longer blocks met (the printed `pins=` field still reflects `pins_ok`) | `5ce4622918dcb98bbcc4a58bb092906de4d9ef05d84ee7c23b87ed8edb9de37c` | 1 (pass=33 fail=1) | pin_mismatch_unmet | killed |
| m12-accept-queued | row_ok accepts source status `queued` as well as `mined` | `30ebcdf18684b3536cea73a16d442a8e6bd8f8dcaa4ba58c35279e04d90f7ece` | 1 (pass=33 fail=1) | row_not_mined_unmet | killed |

Every kill is a predicate-check failure (a printed `FAIL <check>` plus `C2_SELFTEST … fail>=1`); no mutant
crashed, so each kill is attributable to the intended arm, not to a harness break.

## Score at the data revision — invariant across all 13 runs

All 13 score runs (pristine + 12 mutants) printed the byte-identical line, rc 1 each:

```
C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=entailment
```

Reason (observed): at `87e0c37` the entry passes every arm except entailment, and
`git ls-tree --name-only 87e0c374537557754bf71dd68036ded3ddc6699c .ufo/waves/round-51/w1/` lists no committed
files (rc 0, empty output), so no committed vote exists for any mutant to misread and no floor/pin/class
mutation changes an already-passing arm. At this revision the selftest is the only discriminator among these
mutants.

## Diffs (unified, n=1; each mutant is exactly one hunk)

```diff
--- count-c2.py
+++ mut-m01-drop-dissent-check.py
@@ -218,5 +218,3 @@
             v = votes.get(claim_hash(cells[0]), set())
-            if any(k == "overclaim" for k, _ in v):
-                dissent += 1
-            elif any(k == "entailed" for k, _ in v):
+            if any(k == "entailed" for k, _ in v):
                 entailed += 1
```

```diff
--- count-c2.py
+++ mut-m02-no-hash-match.py
@@ -217,3 +217,3 @@
                 missing += 1
-            v = votes.get(claim_hash(cells[0]), set())
+            v = set().union(*votes.values()) if votes else set()
             if any(k == "overclaim" for k, _ in v):
```

```diff
--- count-c2.py
+++ mut-m03-accept-l1-prefix.py
@@ -123,3 +123,3 @@
         name = path.rsplit("/", 1)[-1]
-        if name.startswith(L1_PREFIX) or not name.endswith(".md"):
+        if not name.endswith(".md"):
             continue
```

```diff
--- count-c2.py
+++ mut-m04-drop-md-filter.py
@@ -123,3 +123,3 @@
         name = path.rsplit("/", 1)[-1]
-        if name.startswith(L1_PREFIX) or not name.endswith(".md"):
+        if name.startswith(L1_PREFIX):
             continue
```

```diff
--- count-c2.py
+++ mut-m05-min-sources-4.py
@@ -40,3 +40,3 @@
 MIN_CLAIMS = 12
-MIN_SOURCES = 5
+MIN_SOURCES = 4
 MIN_CLAIM_WORDS = 6
```

```diff
--- count-c2.py
+++ mut-m06-min-claims-10.py
@@ -39,3 +39,3 @@
 OPENED = "2026-10-26"
-MIN_CLAIMS = 12
+MIN_CLAIMS = 10
 MIN_SOURCES = 5
```

```diff
--- count-c2.py
+++ mut-m07-drop-opened-date.py
@@ -207,3 +207,2 @@
             row_ok = bool(srow and len(srow) == 11 and url is not None and srow[7] == "mined"
-                          and srow[8] == OPENED
                           and entry_path in [u.strip() for u in re.split(r"[,;]", srow[10])])
```

```diff
--- count-c2.py
+++ mut-m08-drop-used-by.py
@@ -207,4 +207,3 @@
             row_ok = bool(srow and len(srow) == 11 and url is not None and srow[7] == "mined"
-                          and srow[8] == OPENED
-                          and entry_path in [u.strip() for u in re.split(r"[,;]", srow[10])])
+                          and srow[8] == OPENED)
             if not row_ok:
```

```diff
--- count-c2.py
+++ mut-m09-drop-unique-quote.py
@@ -190,3 +190,3 @@
             words = q.split(" ")
-            if (not (MIN_WORDS <= len(words) <= MAX_WORDS) or q in seen_quotes
+            if (not (MIN_WORDS <= len(words) <= MAX_WORDS)
                     or words_beyond(cells[0], q) < MIN_BEYOND):
```

```diff
--- count-c2.py
+++ mut-m10-min-beyond-0.py
@@ -42,3 +42,3 @@
 MIN_CLAIM_WORDS = 6
-MIN_BEYOND = 3
+MIN_BEYOND = 0
 MIN_WORDS, MAX_WORDS = 6, 25
```

```diff
--- count-c2.py
+++ mut-m11-drop-pin-check.py
@@ -153,4 +153,2 @@
         norm[url] = normalise(b or "") if kind == "html" else normalise_text(b or "")
-    if not pins_ok:
-        failed.append("pins")
     entry = read(entry_path)
```

```diff
--- count-c2.py
+++ mut-m12-accept-queued.py
@@ -206,3 +206,3 @@
                         break
-            row_ok = bool(srow and len(srow) == 11 and url is not None and srow[7] == "mined"
+            row_ok = bool(srow and len(srow) == 11 and url is not None and srow[7] in ("mined", "queued")
                           and srow[8] == OPENED
```

## Observations and named limits (no counter change proposed — counters are frozen)

- **Score-at-R invariance.** At a revision whose only failing arm is entailment and whose wave dir carries no
  committed vote files, the counter's printed line is identical under all 12 mutants. A mutated or tampered
  counter at R is detectable only by `--selftest` or by hashing the byte against
  `evidence/freeze-sha256.txt` — the score line itself carries no signal about which counter produced it.
  This is a limit of the scoring protocol, recorded, not fixed.
- **Single-check coverage per arm.** Eleven of the twelve mutation points are guarded by exactly one selftest
  check each (m02 is the exception, caught by two: `entail_one_row_unreviewed_unmet` and
  `entail_hash_of_other_text_unmet`). An edit that broke an arm and its own check together would pass the
  selftest; for that class the freeze-hash cross-check is the remaining guard.
- **Both vote-source filters are load-bearing.** Dropping the L1-prefix filter (m03) or the `.md` filter (m04)
  each flips the selftest's dedicated check to FAIL — the counter's judgment source is exactly "non-L1-named
  `.md` files under `.ufo/waves/round-51/w1/` at R", and both halves of that definition are exercised.
- **Restoration evidence.** The lane byte was read-only throughout: sha256 `19553792d74d8f3ca9c09e6a018b9c66
  f61a58e8ad78e72b524a69ec892cfb26` before the first run and after the last run; the mirror's pristine copy
  re-hashed identical; and the detector re-run on pristine bytes after all mutant runs reproduced the baseline
  exactly (selftest rc 0 `pass=34 fail=0`; score rc 1, same line). No mutant was ever written outside
  `<scratch>/lane/`.

## Cleanup

Scratch `/fast/scratch/hyaku/mori-r51/Mo51MutC2Counter/` (mirror, mutants, out/, tmp/) removed with
`rm -rf` after this report was written; nothing cited above lives only in scratch — every command output is
quoted verbatim in this file.

## Findings

- **MED — scoring-protocol limit** (`.ufo/waves/round-51/count-c2.py`, `evaluate`/`main`; reading in
  `evidence/c2-at-data.txt`): at the data revision the counter's stdout is invariant under all 12 assigned
  single-point mutants — the printed score line cannot distinguish a mutated counter from the frozen one at a
  revision where only the entailment arm fails and no votes are committed. Detection of a mutated counter at R
  rests entirely on `--selftest` (rc 1 for all 12 mutants here) and on the freeze-sha256 cross-check (working
  tree matches `19553792…`).
- **LOW — selftest redundancy** (`count-c2.py` `selftest()`): each mutation point is guarded by exactly one
  check (m02 the only two-check point); a simultaneous break of an arm and its check would pass `--selftest`.
- **LOW — no survivor**: none of the 12 assigned mutations survived the selftest; no counter weakness found
  within the assigned probe set. The contract's named limits for the entailment arm (a recorded judgment, not
  its correctness) stand unchanged.

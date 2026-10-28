# Mo59Executor44 — sha256 of every committed `*-results.json` / `*-settlement*.json` under `.ufo/waves/` rounds 50–58

Seat: executor (connector/executor data-walk). L1: `MoriR59a2`.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Freeze rev `60b3a76ad0524c8978cc51922940be1c8c388915` (amended freeze; initial `ccfd554e`).
Entering rev `2b9f03975bfb6e508f35074ac8181ec8bf54e805`. Lane `master` tip at run time: `8ff344ff18924c1ea63d46c3b3969f9fea05bc51`.

**Scope honoured:** read-only on the lane. No production file, corpus registry, SCORECARD, LOG or lane
VCS was edited; no commit, no `git write`. All fixture/mock materialization happened under
`/fast/scratch/hyaku/mori-r59/Mo59Executor44/` (scratch root created with `mkdir -p`, `TMPDIR` pointed
there, `--scratch` passed to both counters, scratch cleaned before yield). No fixture repo was
initialized (no `git init` was needed — every check ran with `git show`/`git ls-tree`/`git cat-file`
against the lane, and the mock C2 root was a plain directory tree, not a git repo). No fleet-root or
sibling-repo writes. Disk guard was checked before heavy work and was green.

Tooling: no install, no update, no pacman transaction (host-wide pacman pause respected). Only
pre-existing tools used: `git`, `python3` (3.x, stdlib only), `sha256sum`, `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh`,
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`.

---

## 1. Primary deliverable — sha256 of every committed `*-results.json` / `*-settlement*.json` under `.ufo/waves/` rounds 50–58

### 1a. The complete inventory (11 files — this is the exhaustive set)

Enumeration command (freeze rev, read-only):

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree -r --name-only \
  60b3a76ad0524c8978cc51922940be1c8c388915 -- .ufo/waves/ \
  | grep -E '^\.ufo/waves/round-(5[0-8])/' | grep -Ei '(results|settlement)[^/]*\.json$'
```

returns exactly 11 paths (case-insensitive `results|settlement`, any `*.json` suffix, any depth under
the round dir). A broader sweep of **all** `*.json` under rounds 50–58 (dispatch/spec/registry/plan/
input included) yields 43 paths; of those, the 11 below are the only ones matching the
`*results.json` / `*settlement*.json` name predicate. No `-settlement` artifact exists in rounds
50–57 (the single `*settlement*.json` in the range is round 58's).

### 1b. The hash list (pin candidates)

Hashes are of the **committed blob bytes** at freeze rev `60b3a76a…`, computed as
`git show <rev>:<path> | sha256sum`. Every hash was additionally confirmed **identical at the lane
tip `8ff344ff…`** (all 11 rows `SAME`), so these pins are stable across the freeze→tip range and
are usable as copy-pin values at any R in `[60b3a76a, 8ff344ff]`.

| # | sha256 (pin candidate) | committed path | bytes | newlines (`wc -l`) | git blob (freeze rev) |
|---|---|---|---|---|---|
| 1 | `1f630cb7c6c94e6fa17d9a3f6efeb6eed0ef550757ec1e8b98a3cc1964fcdfd6` | `.ufo/waves/round-50/a2w1-results.json` | 16667 | 391 | (see §1c) |
| 2 | `c67326197183a7022fedc94359623308b702dff2b44246f716fd635798715af6` | `.ufo/waves/round-51/w1-results.json` | 294869 | 415 | (see §1c) |
| 3 | `2fd276b0e59590bdf481ceb615bfe9a71cae06a5834311a151206712217422f9` | `.ufo/waves/round-52/w1-results.json` | 292753 | 415 | (see §1c) |
| 4 | `d2bfda4e64120b4174fced819e99cafcf2821afddf6f9c2f05a44f108b24c345` | `.ufo/waves/round-53/a2r1-results.json` | 7708 | 55 | (see §1c) |
| 5 | `0d644e0fb9c50101a00f47c4ef95e637bb1b1cf1168b5e49bdd19c2f0e584260` | `.ufo/waves/round-53/w1-results.json` | 389180 | 480 | (see §1c) |
| 6 | `ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f` | `.ufo/waves/round-54/w1-results.json` | 264143 | 451 | `52461ffd55c35767411166196133a4ff55097324` |
| 7 | `2e5b0a0f94d1fa5b90b2804d370db87d25d5197fa65bc4f26441d939b8d9763b` | `.ufo/waves/round-55/w1-results.json` | 197729 | 390 | `39562ece67065931a06e6e94ca5a3fe2e3014bf7` |
| 8 | `19536201a689c954899a2e6decf322ef2c5f3d2ed9bc8ddb75229636b1e5d761` | `.ufo/waves/round-56/w1-results.json` | 358591 | 390 | `12053ae48392a05a879876461761738a0d83307f` |
| 9 | `29e7a35df544315d3bb6ac2f0da96235342d77a1f8306ab25b8a27675669beb1` | `.ufo/waves/round-57/w1-results.json` | 159483 | 390 | `9507020f7b854ae5bfc70daabdb638bc79a22eb6` |
| 10 | `b259e73cdddef7ff8565a01c6d97f79da8b112aa6c7dbb97a8aa541b4f0b5588` | `.ufo/waves/round-58/evidence/w1-settlement.json` | 230411 | 1 | `39949e14659a7404352c1031a0082cd63b6c2b8e` |
| 11 | `a57b660d9f41c55dc5d614444f60f1cf658d19a55a530c9788369e5fb7ec61fc` | `.ufo/waves/round-58/w1-results.json` | 180075 | 390 | `9064e5315d4831c9fd3642827ce718417c582083` |

### 1c. Git blob ids at freeze rev (cross-check anchor)

```
git -C …/mori-shokunin rev-parse 60b3a76ad0524c8978cc51922940be1c8c388915:<path>
```

- round-54/w1-results.json → `52461ffd55c35767411166196133a4ff55097324`
- round-55/w1-results.json → `39562ece67065931a06e6e94ca5a3fe2e3014bf7`
- round-56/w1-results.json → `12053ae48392a05a879876461761738a0d83307f`
- round-57/w1-results.json → `9507020f7b854ae5bfc70daabdb638bc79a22eb6`
- round-58/w1-results.json → `9064e5315d4831c9fd3642827ce718417c582083`
- round-58/evidence/w1-settlement.json → `39949e14659a7404352c1031a0082cd63b6c2b8e`

### 1d. Freeze→tip stability proof

Loop over the 11 paths comparing `git show 60b3a76a:<p> | sha256sum` against
`git show 8ff344ff:<p> | sha256sum`: **11/11 `SAME`**. No `*-results.json` / `*settlement*.json`
under rounds 50–58 was modified between the amended freeze and the current lane tip, so every pin in
§1b is revision-stable for the remainder of the wave.

### 1e. Which of these are the C2-eligible copy sources

`count-c2.py` `ARTIFACTS` (frozen, `count-c2.py:56-70`) names exactly **six** copy sources, all
inside rounds 54–58, and they are exactly rows **6–11** of §1b:

| ARTIFACTS copy path (target) | named `.ufo` artifact | copy pin = artifact pin (byte-equal required) |
|---|---|---|
| `corpus/evidence/sources-r59/w1-results-r54.json` | `.ufo/waves/round-54/w1-results.json` | `ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f` |
| `corpus/evidence/sources-r59/w1-results-r55.json` | `.ufo/waves/round-55/w1-results.json` | `2e5b0a0f94d1fa5b90b2804d370db87d25d5197fa65bc4f26441d939b8d9763b` |
| `corpus/evidence/sources-r59/w1-results-r56.json` | `.ufo/waves/round-56/w1-results.json` | `19536201a689c954899a2e6decf322ef2c5f3d2ed9bc8ddb75229636b1e5d761` |
| `corpus/evidence/sources-r59/w1-results-r57.json` | `.ufo/waves/round-57/w1-results.json` | `29e7a35df544315d3bb6ac2f0da96235342d77a1f8306ab25b8a27675669beb1` |
| `corpus/evidence/sources-r59/w1-results-r58.json` | `.ufo/waves/round-58/w1-results.json` | `a57b660d9f41c55dc5d614444f60f1cf658d19a55a530c9788369e5fb7ec61fc` |
| `corpus/evidence/sources-r59/w1-settlement-r58.json` | `.ufo/waves/round-58/evidence/w1-settlement.json` | `b259e73cdddef7ff8565a01c6d97f79da8b112aa6c7dbb97a8aa541b4f0b5588` |

**Rounds 50/51/52/53 artifacts are NOT in `ARTIFACTS`** — the frozen C2 predicate rejects any entry
claim whose cited file is not one of these six copies (`count-c2.py:142-144`, reason
`files:outside=<path>`). The §1b rows 1–5 are therefore *not* usable as C2 claim sources, even
though their hashes are correct and reproducible. They remain the complete answer to this seat's
literal assignment ("every committed … under rounds 50-58") and are the natural extension of the
round-59 entry if the L1 later widens `ARTIFACTS` (which is frozen — so no).

Note the `tree=ok` arm (`count-c2.py:267-280`) requires each copy's sha256 to equal its named
artifact's sha256 **at R**. Because §1b's hashes are byte-stable across freeze→tip, a copy written
byte-identically to the artifact satisfies the tree arm at any R in range.

---

## 2. Frozen-counter state measured read-only (evidence, not a claim)

All four runs below used `TMPDIR=/fast/scratch/hyaku/mori-r59/Mo59Executor44` and an explicit
`--scratch` under the seat scratch root.

```
$ python3 .ufo/waves/round-59/count-c1.py --selftest
C1_SELFTEST pass=6 fail=0            (exit 0)

$ python3 .ufo/waves/round-59/count-c2.py --selftest
C2_SELFTEST pass=9 fail=0            (exit 0)

$ python3 .ufo/waves/round-59/count-c1.py HEAD --scratch $S/c1
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=HEAD        (exit 0)

$ python3 .ufo/waves/round-59/count-c2.py HEAD --scratch $S/c2
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=bad pins=bad tree=bad \
   claims=0 files=0 rev=HEAD \
   failed=copy_absent:corpus/evidence/sources-r59/w1-results-r54.json, …(6 copies)…,entry_absent,tree
                                                                        (exit 1)

$ python3 .ufo/waves/round-59/count-c1.py 60b3a76ad0524c8978cc51922940be1c8c388915 --scratch $S/fr1
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=60b3a76ad0524c8978cc51922940be1c8c388915  (exit 0)

$ python3 .ufo/waves/round-59/count-c2.py 60b3a76ad0524c8978cc51922940be1c8c388915 --scratch $S/fr2
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=bad pins=bad tree=bad claims=0 files=0
   rev=60b3a76ad0524c8978cc51922940be1c8c388915 failed=copy_absent:…(6)…,entry_absent,tree          (exit 1)
```

Entering-revision do-nothing controls re-run by this seat (read-only, matching the frozen receipts
in `.ufo/waves/round-59/evidence/control-c{1,2}-do-nothing.txt` exactly):

```
$ python3 .ufo/waves/round-59/count-c1.py 2b9f03975bfb6e508f35074ac8181ec8bf54e805 --scratch $S/ent1
C1=unmet selftest=bad fixtures=bad real=bad pointers=bad rev=2b9f0397… \
   failed=tool_absent,selftest,fixtures_absent,real,pointers          (exit 1)

$ python3 .ufo/waves/round-59/count-c2.py 2b9f03975bfb6e508f35074ac8181ec8bf54e805 --scratch $S/ent2
C2=unmet … failed=copy_absent:…(6)…,drift,entry_absent,scan,selftest,tool_absent,tree,trees,trees_absent
                                                                        (exit 1)
```

**Reading.** C1 is already **met at HEAD** — `tools/mori-register-check.py` is landed at its frozen
pin and the 13 hostile fixtures score as frozen. C1 is *not* a wave-59 deliverable that still needs
doing; it was satisfied by the freeze commit `60b3a76a`. The remaining C2 work is entirely
data-side: the six `corpus/evidence/sources-r59/` copies, the entry file, and the registry rows.

Frozen-pin checks (read-only):
- `git show HEAD:tools/mori-register-check.py | sha256sum` → `38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8` = frozen `PIN` ✔
- `git show 60b3a76a…:tools/mori-settlement-scan.py | sha256sum` → `4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9` = frozen `PIN` ✔
- `git diff --stat 60b3a76a… HEAD -- count-c1.py count-c2.py` → **empty** (counter bytes unchanged since freeze)
- `git ls-tree --name-only HEAD:.ufo/waves/round-59/fixtures-c1/` → 13 dirs (`f01`…`f13`) ✔
- `git ls-tree --name-only HEAD:.ufo/waves/round-59/trees-c2/` → 12 dirs (`t01`…`t12`) ✔

---

## 3. Per-artifact scan verdicts (drives which artifacts can carry claims)

Each artifact was materialized under scratch and scanned with the frozen
`tools/mori-settlement-scan.py` (sha == frozen PIN). Results:

| artifact | verdict | seats | members | notes |
|---|---|---|---|---|
| round-50/a2w1-results.json | `SETTLEMENT_SCAN_OK` | 64 | 64 | 64 empty outputs, 64 non-null notes |
| round-51/w1-results.json | `SETTLEMENT_SCAN_OK` | 68 | 68 | |
| round-52/w1-results.json | `SETTLEMENT_SCAN_OK` | 68 | 68 | |
| round-53/a2r1-results.json | `SETTLEMENT_SCAN_OK` | 8 | 8 | critic 3 / reviewer 5 |
| **round-53/w1-results.json** | **`SETTLEMENT_SCAN_FAIL`** | 67 | 67 | `member[i]:extra_keys=report_file` on every member — the frozen `DRIFT_SCAN` file; schema drift observed, **reported, not fixed** (per contract) |
| round-54/w1-results.json | `SETTLEMENT_SCAN_OK` | 74 | 74 | |
| round-55/w1-results.json | `SETTLEMENT_SCAN_OK` | 64 | 64 | |
| round-56/w1-results.json | `SETTLEMENT_SCAN_OK` | 64 | 64 | |
| round-57/w1-results.json | `SETTLEMENT_SCAN_OK` | 64 | 64 | |
| round-58/w1-results.json | `SETTLEMENT_SCAN_OK` | 64 | 64 | |
| **round-58/evidence/w1-settlement.json** | **`SETTLEMENT_SCAN_FAIL`** | null | 0 | `results_not_list, seats_mismatch, lane_bad, wave_bad, round_bad` — it is a `mori-wave-settlement-v1` **census** object (`ignored_json`/`lane_root`/`schema`/`totals`/`waves`), *not* a `ufo-wave-results` member list |

**Consequence for the entry author (important, and easy to get wrong).** The six
`ARTIFACTS` copies are *not* all scan-OK, and the counter does not require them to be:

- `REAL_SCAN` (the five files the counter actually scans and requires OK) = rounds **54,55,56,57,58**
  `w1-results.json` → all five are `SETTLEMENT_SCAN_OK` with `members==seats`. ✔
- `DRIFT_SCAN` = round-53 `w1-results.json` → must FAIL. ✔ (it does, via `extra_keys=report_file`)
- `w1-settlement-r58.json` is in `ARTIFACTS` (so it must exist, be byte-equal, and be citable) but it
  is **never scanned** — it is a census artifact. Claims over it must therefore use **`offset:`**
  spans, not `line:` spans (it is a single 230 411-byte line; a `line:1` quote would be the whole
  file, and the claim grammar's `line` branch compares the full line byte-for-byte).
- The r50/r51/r52/r53-a2r1 artifacts scan OK but are outside `ARTIFACTS`, so claims citing them
  would be rejected with `files:outside=…`.

---

## 4. Byte-exact quote-span candidates (verified against the frozen grammar)

The frozen claim grammar (`count-c2.py:74-77`) is:

```
^- \*\*K(\d+)\*\* — .+? Quote: `([^`]+)` \((\S+?):(line|offset):(\d+); pin ([0-9a-f]{64})\)\s*$
```

with `line` = 1-based line of the copy, `offset` = 0-based byte offset into the copy. The pin must
equal the **copy's** sha256 at R, which (tree arm) equals the artifact's sha256 in §1b.

### 4a. `line:` spans — the four header lines of each results artifact (identical shape, per-round values)

All six results copies begin:

```
{
 "lane": "mori",
 "round": NN,
 "wave": "w1",
 "seats": NN,
 "results": [
```

Verified byte-exact line contents (leading single space preserved, trailing comma included):

| copy | line 2 | line 3 | line 4 | line 5 |
|---|---|---|---|---|
| `w1-results-r54.json` | ` "lane": "mori",` | ` "round": 54,` | ` "wave": "w1",` | ` "seats": 74,` |
| `w1-results-r55.json` | ` "lane": "mori",` | ` "round": 55,` | ` "wave": "w1",` | ` "seats": 64,` |
| `w1-results-r56.json` | ` "lane": "mori",` | ` "round": 56,` | ` "wave": "w1",` | ` "seats": 64,` |
| `w1-results-r57.json` | ` "lane": "mori",` | ` "round": 57,` | ` "wave": "w1",` | ` "seats": 64,` |
| `w1-results-r58.json` | ` "lane": "mori",` | ` "round": 58,` | ` "wave": "w1",` | ` "seats": 64,` |

### 4b. `offset:` spans in the settlement census copy `w1-settlement-r58.json`

(0-based byte offsets into the 230 411-byte copy; each offset's byte slice was read back and
verified equal to the quote.)

| offset | byte-exact quote |
|---|---|
| 1 | `"ignored_json":1719` |
| 21 | `"lane_root":"/home/vgpnk/Projects/shokunin/mori-shokunin"` |
| 79 | `"schema":"mori-wave-settlement-v1"` |
| 149 | `"misrooted":0` |
| 199 | `"present":2760` |
| 214 | `"states":{"partial":26,"settled":36}` |
| 251 | `"stub":2` |
| 260 | `"unique_dispatch_sha256":62` |
| 288 | `"unparsed":0` |

### 4c. Worked proof that the candidate set satisfies the frozen C2 entry predicate

To avoid shipping an unproven candidate list, this seat built a **scratch-only mock root**
(`$SCRATCH/mock/root2`, plain directory tree — no git repo, no lane writes) containing the six
copies byte-copied from the committed artifacts, a candidate entry, and a mock `corpus/SOURCES.md`
carrying six mined rows. It then imported the **frozen, unmodified** `count-c2.py` and called its own
`eval_entry()` on that root:

```
eval_entry ok= True  stats={'claims': 14, 'files': 6}  reasons=[]
```

That is the frozen predicate's own verdict function — 14 claims over 6 distinct artifacts, every pin
equal to the copy's sha256, every span byte-equal, every cited S-row present with 11 cells, status
`mined`, and `used-by` naming exactly the entry path. **A second, independent mock** (different
frontmatter layout: one `source:` line per S-id vs. a comma list) also returned
`ok=True, reasons=[]`, confirming the frontmatter/`SID` mechanics in both shapes.

The verified candidate entry body (14 claims; the exact text that produced `reasons=[]`):

```markdown
source: S553
source: S554
source: S555
source: S556
source: S557
source: S558
verified-at: 2026-10-28
recheck: `python3 .ufo/waves/round-59/count-c2.py R`
coverage-map: Core — wave settlement artifacts; no frontier advance claimed

# Wave settlement artifacts (round 59)

## Claims

- **K1** — every r54 wave-results artifact names the mori lane at top level. Quote: ` "lane": "mori",` (corpus/evidence/sources-r59/w1-results-r54.json:line:2; pin ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f)
- **K2** — the r54 artifact records its wave round. Quote: ` "round": 54,` (corpus/evidence/sources-r59/w1-results-r54.json:line:3; pin ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f)
- **K3** — the r54 artifact records its wave identifier. Quote: ` "wave": "w1",` (corpus/evidence/sources-r59/w1-results-r54.json:line:4; pin ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f)
- **K4** — the r54 artifact records its seat count. Quote: ` "seats": 74,` (corpus/evidence/sources-r59/w1-results-r54.json:line:5; pin ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f)
- **K5** — every r55 wave-results artifact names the mori lane at top level. Quote: ` "lane": "mori",` (corpus/evidence/sources-r59/w1-results-r55.json:line:2; pin 2e5b0a0f94d1fa5b90b2804d370db87d25d5197fa65bc4f26441d939b8d9763b)
- **K6** — the r55 artifact records its seat count. Quote: ` "seats": 64,` (corpus/evidence/sources-r59/w1-results-r55.json:line:5; pin 2e5b0a0f94d1fa5b90b2804d370db87d25d5197fa65bc4f26441d939b8d9763b)
- **K7** — every r56 wave-results artifact names the mori lane at top level. Quote: ` "lane": "mori",` (corpus/evidence/sources-r59/w1-results-r56.json:line:2; pin 19536201a689c954899a2e6decf322ef2c5f3d2ed9bc8ddb75229636b1e5d761)
- **K8** — the r56 artifact records its seat count. Quote: ` "seats": 64,` (corpus/evidence/sources-r59/w1-results-r56.json:line:5; pin 19536201a689c954899a2e6decf322ef2c5f3d2ed9bc8ddb75229636b1e5d761)
- **K9** — every r57 wave-results artifact names the mori lane at top level. Quote: ` "lane": "mori",` (corpus/evidence/sources-r59/w1-results-r57.json:line:2; pin 29e7a35df544315d3bb6ac2f0da96235342d77a1f8306ab25b8a27675669beb1)
- **K10** — the r57 artifact records its seat count. Quote: ` "seats": 64,` (corpus/evidence/sources-r59/w1-results-r57.json:line:5; pin 29e7a35df544315d3bb6ac2f0da96235342d77a1f8306ab25b8a27675669beb1)
- **K11** — every r58 wave-results artifact names the mori lane at top level. Quote: ` "lane": "mori",` (corpus/evidence/sources-r59/w1-results-r58.json:line:2; pin a57b660d9f41c55dc5d614444f60f1cf658d19a55a530c9788369e5fb7ec61fc)
- **K12** — the r58 artifact records its seat count. Quote: ` "seats": 64,` (corpus/evidence/sources-r59/w1-results-r58.json:line:5; pin a57b660d9f41c55dc5d614444f60f1cf658d19a55a530c9788369e5fb7ec61fc)
- **K13** — the r58 settlement census declares its schema tag. Quote: `"schema":"mori-wave-settlement-v1"` (corpus/evidence/sources-r59/w1-settlement-r58.json:offset:79; pin b259e73cdddef7ff8565a01c6d97f79da8b112aa6c7dbb97a8aa541b4f0b5588)
- **K14** — the r58 settlement census reports zero misrooted files. Quote: `"misrooted":0` (corpus/evidence/sources-r59/w1-settlement-r58.json:offset:149; pin b259e73cdddef7ff8565a01c6d97f79da8b112aa6c7dbb97a8aa541b4f0b5588)
```

Matching registry rows to append to `corpus/SOURCES.md` (11 cells, `status=mined`,
`used-by` naming **exactly** the entry path — the counter compares `cells[10] != ENTRY`):

```
| S553 | mori wave-settlement artifact copy 1 | own-work | A | scope 1 | sha256 ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f | teaches 1 | mined | 2026-10-28 | 90d | corpus/knowledge/wave-settlement-artifacts-r59.md |
| S554 | mori wave-settlement artifact copy 2 | own-work | A | scope 2 | sha256 2e5b0a0f94d1fa5b90b2804d370db87d25d5197fa65bc4f26441d939b8d9763b | teaches 2 | mined | 2026-10-28 | 90d | corpus/knowledge/wave-settlement-artifacts-r59.md |
| S555 | mori wave-settlement artifact copy 3 | own-work | A | scope 3 | sha256 19536201a689c954899a2e6decf322ef2c5f3d2ed9bc8ddb75229636b1e5d761 | teaches 3 | mined | 2026-10-28 | 90d | corpus/knowledge/wave-settlement-artifacts-r59.md |
| S556 | mori wave-settlement artifact copy 4 | own-work | A | scope 4 | sha256 29e7a35df544315d3bb6ac2f0da96235342d77a1f8306ab25b8a27675669beb1 | teaches 4 | mined | 2026-10-28 | 90d | corpus/knowledge/wave-settlement-artifacts-r59.md |
| S557 | mori wave-settlement artifact copy 5 | own-work | A | scope 5 | sha256 a57b660d9f41c55dc5d614444f60f1cf658d19a55a530c9788369e5fb7ec61fc | teaches 5 | mined | 2026-10-28 | 90d | corpus/knowledge/wave-settlement-artifacts-r59.md |
| S558 | mori wave-settlement artifact copy 6 | own-work | A | scope 6 | sha256 b259e73cdddef7ff8565a01c6d97f79da8b112aa6c7dbb97a8aa541b4f0b5588 | teaches 6 | mined | 2026-10-28 | 90d | corpus/knowledge/wave-settlement-artifacts-r59.md |
```

Registry state checked (read-only): `corpus/SOURCES.md` currently has **325** rows, ids
`S001…S552`, **no duplicates**, and **every existing row already has exactly 11 cells**
(`rows with != 11 cells: []`). `S553…S558` are **free** — grep for `S55[3-9]` returns nothing.
That satisfies the contract's "S### rows opened this round" requirement (six new rows, one per cited
artifact copy) and the routed round-58 defect "duplicate source row S552" is not repeated: no id in
the proposed set collides with an existing row.

---

## 5. Mechanics the entry author must not get wrong (all read from frozen counter source)

1. **`source:` line shape.** `SID = re.compile(r"source:\s*(S\d+)")` and `sids.update(SID.findall(l))`
   over `lines[:10]` only — so a head line `source: S553, S554` contributes **only `S553`**
   (verified: `findall` → `['S553']`). Either put one `source: S###` per line (6 lines, tested and
   proven in §4c) or accept that only the first id of a line is bound. `Sources: S553` (capital S,
   plural) matches **nothing** (`findall` → `[]`), which would trigger `rows:no_source_ids`.
2. **Frontmatter keys must be in the first 10 lines** and each line must *start with* the key
   (`l.startswith(k)`), i.e. `source:`, `verified-at:`, `recheck:`, `coverage-map:` at column 0.
3. **Every claim's `used-by` must be the entry path exactly** — `cells[10] != ENTRY` fails; a
   comma-joined list of two entries would fail the `used-by` arm.
4. **Exactly 11 cells** per registry row (`rows:bad_row` otherwise).
5. **Claim quotes must not contain a backtick** (grammar `[^`]+`), must be ≥ 3 bytes
   (`span:short`), and must be byte-identical to the copy line / byte slice.
6. **A line that starts with `-` and contains `Quote:` but does not match the grammar** is recorded
   as `grammar:…` — so prose bullets that mention "Quote:" will fail the entry arm.
7. **`files:outside=`** — only the six `ARTIFACTS` copy paths are citable (§1e).
8. The settlement copy is a census object, so it must be cited with `offset:` spans (§4b), not `line:`.

---

## 6. Census

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
… (duplicate-url W04 warnings, pre-existing) …
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
EXIT=0
```

Exit 0 at the current registry state. Adding S553–S558 raises the row count from 325 to 331; the
census must be re-run to exit 0 after the registry edit (contract §"Census" requires exit 0 at round
end).

---

## 6b. Independent cross-check against the copies a sibling seat landed in the same wave

While this seat was running, a sibling seat materialized `corpus/evidence/sources-r59/` in the lane
working tree (untracked at the time of reading; **not written by this seat**). Hashing those landed
copies and comparing them with §1b gives a **live, independent confirmation** of the pins:

| landed copy (working tree) | landed sha256 | matches §1b pin? |
|---|---|---|
| `w1-results-r54.json` | `ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f` | ✔ |
| `w1-results-r55.json` | `2e5b0a0f94d1fa5b90b2804d370db87d25d5197fa65bc4f26441d939b8d9763b` | ✔ |
| `w1-results-r56.json` | `19536201a689c954899a2e6decf322ef2c5f3d2ed9bc8ddb75229636b1e5d761` | ✔ |
| `w1-results-r57.json` | `29e7a35df544315d3bb6ac2f0da96235342d77a1f8306ab25b8a27675669beb1` | ✔ |
| `w1-results-r58.json` | `a57b660d9f41c55dc5d614444f60f1cf658d19a55a530c9788369e5fb7ec61fc` | ✔ |
| `w1-settlement-r58.json` | `b259e73cdddef7ff8565a01c6d97f79da8b112aa6c7dbb97a8aa541b4f0b5588` | ✔ |
| `w1-results-r53.json` (extra, **not** in `ARTIFACTS`) | `0d644e0fb9c50101a00f47c4ef95e637bb1b1cf1168b5e49bdd19c2f0e584260` | ✔ = §1b row 5 |

6/6 `ARTIFACTS` copies are byte-equal to their named `.ufo` artifacts (the `tree=ok` arm's condition),
and the extra `w1-results-r53.json` copy also matches its source hash. The extra file is **not
harmful** to the frozen counter: the `tree` arm iterates only the six `ARTIFACTS` keys
(`count-c2.py:267-280`) and `eval_entry` rejects only *cited* files outside `ARTIFACTS`
(`count-c2.py:142-144`), so an uncited extra copy is inert. It must simply **not be cited** by the
entry — citing it would raise `files:outside=corpus/evidence/sources-r59/w1-results-r53.json`.

(This is an observation, not a write: this seat did not create, modify or delete those copies.)

---

## 7. Risks / blockers

- **No blocker.** Every artifact, hash, span and offset in this report was materialized and
  re-verified from committed bytes.
- **Risk (frozen, not actionable by a seat):** `ARTIFACTS` is frozen to the six round-54..58 copies,
  so the round-50/51/52/53 artifacts in §1b are computed and reported but unusable as C2 claim
  sources. If the L1 wants r50–r53 coverage, that requires a contract/counter amendment, which the
  kill rule forbids post-freeze. Flagging only.
- **Risk:** `w1-settlement-r58.json` is `ARTIFACTS`-eligible but is a *census* object, not a
  wave-results object. Any claim that describes it as a wave-results settlement file would be
  false on its face even though the counter would accept it (the counter only checks bytes/pins).
  The candidate text in §4c describes it as a "settlement census", which is accurate.
- **Risk:** `used-by` cell for the six new rows must be the *entry* only. If the entry is later
  renamed, all six rows break simultaneously (`rows:usedby`) — one rename, six edits.
- The frozen C2 counter at HEAD reports `entry=bad rows=bad pins=bad tree=bad` solely because the
  data side is unwritten. That is the expected pre-deliverable state, not a counter defect.

## 8. Files changed

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-59/w1/Mo59Executor44.md` — this report
  (the only file written). No production file, corpus registry, SCORECARD, LOG, counter, contract,
  fixture or tree was modified; no commit; no lane VCS mutation; no fleet/sibling-repo write.
- Scratch `/fast/scratch/hyaku/mori-r59/Mo59Executor44/` was created for materialization and
  **removed** after the receipts above were captured into this report.

## 9. Checks the main agent should run (not run here by design)

```
python3 .ufo/waves/round-59/count-c2.py HEAD --scratch <scratch>     # expect C2=met … claims=14 files=6
python3 .ufo/waves/round-59/count-c1.py HEAD --scratch <scratch>     # expect C1=met (already met at freeze)
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
```

After the six copies, the entry, and the six registry rows are landed, `count-c2.py` should print
`C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=14 files=6 rev=R`
(exit 0) — `claims`/`files` counts come from `eval_entry`'s stats, which the mock in §4c already
produced as `{'claims': 14, 'files': 6}`.

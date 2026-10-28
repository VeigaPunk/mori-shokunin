# Mo59Executor45 — results.json anomaly survey (round 59, w1)

Seat: executor (survey). L1: MoriR59a2. Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Frozen contract: `.ufo/waves/round-59/contract.md`. Frozen counters: `.ufo/waves/round-59/count-c1.py`,
`count-c2.py`. Freeze revision `60b3a76ad0524c8978cc51922940be1c8c388915`; entering revision
`2b9f03975bfb6e508f35074ac8181ec8bf54e805`.

Scope of this seat: read-only survey of **every committed results file** — members vs seats, empty
outputs, non-null notes, member key-sets — plus the frozen-counter/tool runs that bound the C1/C2
claims. No production file edited, no lane VCS mutation, no fleet/sibling write. Scratch used:
`/fast/scratch/hyaku/mori-r59/Mo59Executor45/` (created with `mkdir -p`, exported as `TMPDIR`,
passed to both counters via `--scratch`); cleaned before yield.

**Final measured lane state (this seat's last measurement, lane HEAD `7b86704d`):**
`C1=met selftest=ok fixtures=ok real=ok pointers=ok` and
`C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6`
— both exit 0. §2.2 records the freeze-revision readings; §8 records the mid-wave landing and the
one data defect this survey caught in it (`K11` citing a copy outside the frozen `ARTIFACTS` set),
together with the sandbox proof of the fix that landed as `7b86704d`.

---

## 1. Environment / guard state

```
$ /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
root                             use%   free
/tmp                               5%   122.2G
/var/tmp                           36%   576.2G
/fast/scratch/hyaku               27%   592.6G
EXIT=0
```
Guard green before any heavy work; no ENOSPC.

Lane tip / revisions (read-only `git -C … rev-parse` / `log`). The lane advanced **twice while this
seat was surveying** (a sibling builder landed the C2 data mid-wave); all three states were measured:
```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD
7b86704d7c0754a09958d131b64dbfa2a6d3eaed   # round-59: data correction — K11 demoted to prose
$ git -C … log --oneline -6
7b86704d round-59: data correction — K11 demoted to prose (r53 copy outside frozen ARTIFACTS)
be737211 round-59: land C2 data — settlement-artifact depth entry, artifact copies, S553-S560 rows, quarantine slice
8ff344ff round-59: validated w1 dispatch payload (64 seats, v2)
60b3a76a round-59: freeze amendment — counter scratch-mkdir + ls-tree rev:path + register name boundary; pre-data
ccfd554e round-59: freeze contract, C1/C2 counters, tools, fixtures, controls
2b9f0397 round-58 verifier spot-check (integrator, hyaku): non-author admit/reject
```
`git diff --stat 60b3a76a 8ff344ff` = 6 files, all additions under `.ufo/waves/round-59/`
(`build-w1-spec.py`, `evidence/c1-at-freeze.txt`, `evidence/c2-at-freeze.txt`, `w1-dispatch.json`,
`w1-spec.json`, `w1.ready`). **No frozen byte and no committed `.ufo` results file changed between
the freeze revision and HEAD** — the `.ufo` results corpus surveyed in §3 is byte-identical at
`60b3a76a`, `8ff344ff`, `be737211` and `7b86704d` (verified byte-wise: `diff -rq` of the two
materialized trees returned no output, and per-file sha256 values in §3.1 are identical across
revisions). The only `.ufo`/corpus bytes that changed mid-wave are the **new** C2 data
(`corpus/evidence/sources-r59/`, `corpus/knowledge/wave-settlement-artifacts-r59.md`, S553–S560 rows),
which are additions, not modifications — except for the one defect in §8.

---

## 2. Frozen counters and tools — measured

### 2.1 Tool pins (byte-exact, `git show <freeze-rev>:<path> | sha256sum`)

| tool | sha256 at `60b3a76a` | frozen PIN | match |
|---|---|---|---|
| `tools/mori-register-check.py` | `38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8` | `38b733d8…472b8` | yes |
| `tools/mori-settlement-scan.py` | `4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9` | `4c04bf21…5ac9a9` | yes |

Working-tree copies hash identically to the frozen PINs (no post-freeze drift in either tool).

### 2.2 Counter runs (read-only; scratch passed explicitly)

```
$ python3 .ufo/waves/round-59/count-c1.py --selftest
C1_SELFTEST pass=6 fail=0                                     EXIT=0
$ python3 .ufo/waves/round-59/count-c1.py 60b3a76ad0524c8978cc51922940be1c8c388915 --scratch $S
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=60b3a76ad0524c8978cc51922940be1c8c388915   EXIT=0
$ python3 .ufo/waves/round-59/count-c2.py --selftest
C2_SELFTEST pass=9 fail=0                                     EXIT=0
$ python3 .ufo/waves/round-59/count-c2.py 60b3a76ad0524c8978cc51922940be1c8c388915 --scratch $S
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=bad pins=bad tree=bad claims=0 files=0 rev=60b3a76a…
  failed=copy_absent:corpus/evidence/sources-r59/w1-results-r54.json, …r55,…r56,…r57,…r58,
         copy_absent:corpus/evidence/sources-r59/w1-settlement-r58.json,entry_absent,tree      EXIT=1
```
Reading: C2's **tool / selftest / scan / drift / trees arms are already green at the freeze
revision**; the four red arms (`entry`, `rows`, `pins`, `tree`) are exactly the pre-data arms —
`corpus/evidence/sources-r59/` and `corpus/knowledge/wave-settlement-artifacts-r59.md` do not exist
in the lane yet (`ls corpus/evidence/sources-r59/` → *No such file or directory*). This is the
intended pre-data shape for a wave-work claim, not a defect at the freeze.

**Post-landing readings** (the sibling builder's data commit `be737211`, then the correction
`7b86704d`; both measured by this seat with `--scratch`):

```
$ python3 .ufo/waves/round-59/count-c1.py be7372114ded3075e5f5a15227ffec977df22f7d --scratch $S
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=be7372114…                                 EXIT=0
$ python3 .ufo/waves/round-59/count-c2.py be7372114ded3075e5f5a15227ffec977df22f7d --scratch $S
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=ok pins=ok tree=ok claims=14 files=7
  rev=be7372114…  failed=entry                                                                  EXIT=1
$ python3 .ufo/waves/round-59/count-c1.py 7b86704d7c0754a09958d131b64dbfa2a6d3eaed --scratch $S
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=7b86704d7c…                               EXIT=0
$ python3 .ufo/waves/round-59/count-c2.py 7b86704d7c0754a09958d131b64dbfa2a6d3eaed --scratch $S
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6
  rev=7b86704d7c…                                                                                 EXIT=0
```
`be737211` was red on **one arm only** (`entry`); §8 gives the root cause and the sandbox proof.
At `7b86704d` both claims are met with every arm green.

### 2.3 Do-nothing control at the entering revision

```
$ python3 .ufo/waves/round-59/count-c1.py 2b9f03975bfb6e508f35074ac8181ec8bf54e805 --scratch $S
C1=unmet selftest=bad fixtures=bad real=bad pointers=bad rev=2b9f0397…
  failed=tool_absent,selftest,fixtures_absent,real,pointers                                  EXIT=1
$ python3 .ufo/waves/round-59/count-c2.py 2b9f03975bfb6e508f35074ac8181ec8bf54e805 --scratch $S
C2=unmet selftest=bad scan=bad drift=bad trees=bad entry=bad rows=bad pins=bad tree=bad …
  failed=copy_absent:…,drift,entry_absent,scan,selftest,tool_absent,tree,trees,trees_absent  EXIT=1
$ git -C … cat-file -e 2b9f0397:tools/mori-register-check.py   → "exists on disk, but not in '2b9f0397'"
$ git -C … cat-file -e 2b9f0397:tools/mori-settlement-scan.py  → "exists on disk, but not in '2b9f0397'"
```
Both tools are absent at the entering revision → the contract's "before" arm (`tool_absent`, exit 1)
holds; the observed `failed=` list is a strict superset of the contract's named token, with the same
verdict and exit code.

### 2.4 Tool selftests (direct)

```
$ python3 tools/mori-register-check.py --selftest
REGCHECK_SELFTEST pass=12 fail=0        EXIT=0     # matches count-c1.py EXPECT_SELFTEST
$ python3 tools/mori-settlement-scan.py --selftest
SETSCAN_SELFTEST pass=10 fail=0         EXIT=0     # matches count-c2.py EXPECT_SELFTEST
```

### 2.5 Fixture / tree inventory (frozen, at `60b3a76a`)

* `fixtures-c1/`: **13** directories — `f01-stub-only, f02-two-declared, f03-dup-key, f04-missing-key,
  f05-pointer-missing, f06-pointer-absolute, f07-pointer-relative-parent, f08-manifest-name-altered,
  f09-manifest-substring-only, f10-manifest-foreign-lane, f11-manifest-wrong-index,
  f12-lane-round-mismatch, f13-empty-pointer` → matches contract §9 "13 committed trees".
* `trees-c2/`: **12** directories, each with `expect.txt`:
  `t01-no-frontmatter→frontmatter`, `t02-dup-k→distinct`, `t03-quote-wrong-line→span`,
  `t04-stale-pin→pin`, `t05-few-claims→claims_min`, `t06-outside-file→files`,
  `t07-no-row→rows:missing`, `t08-extra-cell-row→rows:bad_row`, `t09-usedby-other→rows:usedby`,
  `t10-queued-status→rows:status`, `t11-quote-short→span`, `t12-malformed-claim→grammar`
  → matches contract §9 "12 committed trees".

---

## 3. Results-file survey (every committed `*results*.json`, excluding the 36 hostile-tree copies)

Population: `git ls-tree -r --name-only <rev>` filtered to `*.json` with `results` in the path
and `/trees-c2/` excluded → **16 files** at the freeze revision `60b3a76a`; **22 files** at HEAD
`7b86704d` (the 6 added are the C2 artifact copies under `corpus/evidence/sources-r59/`, listed at
the foot of the table). (The 36 files under `.ufo/waves/round-59/trees-c2/*/corpus/
evidence/sources-r59/` are hostile-tree stubs, not artifacts; see §4.)

### 3.1 Compact table

| file | schema | seats | members | seats==members | empty_out | nonnull_note | dup_names | member key-set | sha256[:12] |
|---|---|---|---|---|---|---|---|---|---|
| `round-23/falsify/MutModeRead/bounded-results.json` | `mori-r23-mut-mode-read-summary-v1` | n/a | n/a | n/a | n/a | n/a | n/a | *(not a wave-results file)* | `2ed7dd9d75b9` |
| `round-23/falsify/MutSetupPartial/bounded-results.json` | `mori-r23-mutation-probe-v1` | n/a | n/a | n/a | n/a | n/a | n/a | *(not a wave-results file)* | `0aeb14fcce1c` |
| `round-47/w1-results.json` | ufo-wave-results | 42 | 42 | yes | **42** | **42** | none | `{agent,name,note,output}` | `a9b76bb2ab92` |
| `round-47/w2-results.json` | ufo-wave-results | 37 | 37 | yes | 0 | 0 | none | `{agent,name,note,output}` | `25a20fb81752` |
| `round-48/w1-results.json` | ufo-wave-results | 49 | 49 | yes | 0 | 0 | none | `{agent,name,note,output}` | `2bb858bc5100` |
| `round-48/w2-results.json` | ufo-wave-results | 34 | 34 | yes | **34** | **34** | none | `{agent,name,note,output}` | `e7c16d3e6f36` |
| `round-50/a2w1-results.json` | ufo-wave-results | 64 | 64 | yes | **64** | **64** | none | `{agent,name,note,output}` | `1f630cb7c6c9` |
| `round-51/w1-results.json` | ufo-wave-results | 68 | 68 | yes | 0 | 0 | none | `{agent,name,note,output}` | `c67326197183` |
| `round-52/w1-results.json` | ufo-wave-results | 68 | 68 | yes | 0 | 0 | none | `{agent,name,note,output}` | `2fd276b0e595` |
| `round-53/a2r1-results.json` | ufo-wave-results | 8 | 8 | yes | 0 | 0 | none | `{agent,name,note,output}` | `d2bfda4e6412` |
| `round-53/w1-results.json` | ufo-wave-results | 67 | 67 | yes | 1 | **67** | none | `{agent,name,note,output,**report_file**}` | `0d644e0fb9c5` |
| `round-54/w1-results.json` | ufo-wave-results | 74 | 74 | yes | 0 | 0 | none | `{agent,name,note,output}` | `ea48a0cc07fa` |
| `round-55/w1-results.json` | ufo-wave-results | 64 | 64 | yes | 0 | 0 | none | `{agent,name,note,output}` | `2e5b0a0f94d1` |
| `round-56/w1-results.json` | ufo-wave-results | 64 | 64 | yes | 0 | 0 | none | `{agent,name,note,output}` | `19536201a689` |
| `round-57/w1-results.json` | ufo-wave-results | 64 | 64 | yes | 0 | 0 | none | `{agent,name,note,output}` | `29e7a35df544` |
| `round-58/w1-results.json` | ufo-wave-results | 64 | 64 | yes | 0 | 0 | none | `{agent,name,note,output}` | `a57b660d9f41` |
| **COPY** `corpus/evidence/sources-r59/w1-results-r53.json` | ufo-wave-results | 67 | 67 | yes | 1 | 67 | none | `{agent,name,note,output,report_file}` | `0d644e0fb9c5` |
| **COPY** `corpus/evidence/sources-r59/w1-results-r54.json` | ufo-wave-results | 74 | 74 | yes | 0 | 0 | none | `{agent,name,note,output}` | `ea48a0cc07fa` |
| **COPY** `corpus/evidence/sources-r59/w1-results-r55.json` | ufo-wave-results | 64 | 64 | yes | 0 | 0 | none | `{agent,name,note,output}` | `2e5b0a0f94d1` |
| **COPY** `corpus/evidence/sources-r59/w1-results-r56.json` | ufo-wave-results | 64 | 64 | yes | 0 | 0 | none | `{agent,name,note,output}` | `19536201a689` |
| **COPY** `corpus/evidence/sources-r59/w1-results-r57.json` | ufo-wave-results | 64 | 64 | yes | 0 | 0 | none | `{agent,name,note,output}` | `29e7a35df544` |
| **COPY** `corpus/evidence/sources-r59/w1-results-r58.json` | ufo-wave-results | 64 | 64 | yes | 0 | 0 | none | `{agent,name,note,output}` | `a57b660d9f41` |

The 7th copy, `corpus/evidence/sources-r59/w1-settlement-r58.json`, is not a `*results*.json` so it
does not enter the table; it is the `mori-wave-settlement-v1` summary (A6). **Every one of the 6
copies is byte-equal to the `.ufo` artifact it names** (verified `git show <rev>:<copy>` vs
`git show <rev>:<artifact>`: `byte_eq=True` for all six; shas `ea48a0cc07fa`, `2e5b0a0f94d1`,
`19536201a689`, `29e7a35df544`, `a57b660d9f41`, `b259e73cdddef7ff`).

`empty_out` = member `output` is `null` **or** `""`; `nonnull_note` = member `note` is not `null`.
No file anywhere has an empty-string (`""`) output — every empty output is `null`.
(`round-59` itself has no committed results file yet; the wave-59 dispatch is 64 seats,
`w1-dispatch.json counts = {spawn:64, resume:0, total:64}`.)

### 3.2 Scanner verdicts per file (frozen `tools/mori-settlement-scan.py`, one file per invocation)

| file | exit | verdict | failure reasons |
|---|---|---|---|
| `round-23/falsify/MutModeRead/bounded-results.json` | 1 | SETTLEMENT_SCAN_FAIL | `lane_bad, results_not_list, round_bad, seats_mismatch, wave_bad` |
| `round-23/falsify/MutSetupPartial/bounded-results.json` | 1 | SETTLEMENT_SCAN_FAIL | same five |
| `round-47/w1-results.json` | 0 | SETTLEMENT_SCAN_OK | – |
| `round-47/w2-results.json` | 0 | SETTLEMENT_SCAN_OK | – |
| `round-48/w1-results.json` | 0 | SETTLEMENT_SCAN_OK | – |
| `round-48/w2-results.json` | 0 | SETTLEMENT_SCAN_OK | – |
| `round-50/a2w1-results.json` | 0 | SETTLEMENT_SCAN_OK | – |
| `round-51/w1-results.json` | 0 | SETTLEMENT_SCAN_OK | – |
| `round-52/w1-results.json` | 0 | SETTLEMENT_SCAN_OK | – |
| `round-53/a2r1-results.json` | 0 | SETTLEMENT_SCAN_OK | – |
| `round-53/w1-results.json` | 1 | **SETTLEMENT_SCAN_FAIL** | 67 × `member[i]:extra_keys=report_file` |
| `round-54..58/w1-results.json` | 0 | SETTLEMENT_SCAN_OK | – |

Contract §C2 "Scan arm" reproduced exactly:
```
$ python3 tools/mori-settlement-scan.py <r54> <r55> <r56> <r57> <r58>   →  exit 0, verdict SETTLEMENT_SCAN_OK,
    every file members==seats (74/74, 64/64, 64/64, 64/64, 64/64), duplicates [], empty_output 0, notes_nonnull 0
$ python3 tools/mori-settlement-scan.py <r53>                            →  exit 1, verdict SETTLEMENT_SCAN_FAIL,
    67 reasons, all `member[i]:extra_keys=report_file`  (contract: "r53 file MUST scan FAIL — report_file extra keys,
    schema drift, reported not fixed")   ✔ drift observed, not fixed, as the contract states.
```

---

## 4. Anomalies found (ranked)

**A1 — three wave-results files are 100 % output-less yet scan `SETTLEMENT_SCAN_OK`.**
`round-47/w1` (42/42), `round-48/w2` (34/34), `round-50/a2w1` (64/64): every member has
`output: null` and a non-null `note`, all 42/34/64 notes identical:

> `orchestrator kernel restarted mid-wave; seat output was delivered to the orchestrator session but not retained — read the seat report file in the wave dir`

The scanner counts these into `empty_output` / `notes_nonnull` in the summary but **never fails on
them** — `scan_file` only appends a failure for `output_bad` (wrong *type*), never for a null/empty
output. Consequence for C2: the `scan=ok` arm proves *shape*, not *content*; a results file whose
entire payload was lost is indistinguishable from a complete one under the frozen predicate. The
wave dirs do still hold the seat reports (`round-47/w1` → 42 entries, `round-48/w2` → 35,
`round-50/a2w1` → 65), so the data is recoverable from the wave dir, just not from the results file.
All three files are **outside** `count-c2.py`'s `REAL_SCAN` (r54–r58 only), so this does not touch
the frozen arms — it is a coverage observation about the scanner's semantics.

**A2 — `round-53/w1-results.json` schema drift (the designated drift file).** All 67 members carry a
5th key `report_file` (e.g. `member[0].report_file = ".ufo/waves/round-53/w1/Mo53Fr01.md"`), so the
file is FAIL under the frozen member key-set `{name, agent, output, note}`. It also holds the only
genuinely null output in the corpus:
`member[25] name="Mo53RevLedgerProse" note="spawned as job Mo53RevLedgerProse; still running at the session exit and killed - no output delivered"`.
Its other 66 notes are per-seat recovery notes of the form
`output recovered from the orchestrator session transcript (job <id>, status completed, delivered <ts>)`.
This matches the contract's "reported not fixed" wording exactly.

**A3 — two committed files named `*results*.json` are not wave-results artifacts.**
`.ufo/waves/round-23/falsify/{MutModeRead,MutSetupPartial}/bounded-results.json` carry
`schema` `mori-r23-mut-mode-read-summary-v1` / `mori-r23-mutation-probe-v1`, have no `results`
list, no `lane`/`round`/`wave`/`seats` keys, and therefore FAIL the scanner with five reasons.
Risk: any glob over `*results*.json` (e.g. a future counter arm, a census, a lane sweep) will pick
these up and mis-report them as malformed wave settlements. Note the sibling files in the same
directory use the singular form (`MutAliasReturn/bounded-result.json`, `MutOutputLeak/bounded-result.json`,
`MutTmpfsSuffix/probe-result.json`) and are not matched by a `*results*.json` glob at all — the
plural/singular split is inconsistent inside one directory.

**A4 — waves with no committed results file at all.** `round-49` has `w1-dispatch.json`,
`w1-spec.json`, `w1/` but **no** `w1-results.json`; `round-50` has only `a2w1-results.json` (no
`w1-results.json`) despite carrying both `w1-dispatch.json` and `a2w1-dispatch.json`. Rounds 13–46
have no `*results*.json` either (they predate the artifact). The committed wave-results corpus
therefore starts at round 47 and has holes at 49 (and at 50's first attempt).

**A5 — `round-53/a2r1-results.json` is a valid wave-results file that no frozen arm covers.**
8 members (5 reviewer + 3 critic), `seats==members==8`, scans OK, key-set clean. It is not in
`REAL_SCAN` and not in `DRIFT_SCAN` (`count-c2.py` uses only `.ufo/waves/round-53/w1-results.json` as
the drift file). Same for r47/r48/r50/r51/r52 — 6 committed, clean wave-results files are outside
every frozen scan arm. The contract's scan arm is stated as "the five r54–r58 wave-results files",
so this is consistent with the contract; flagged as coverage, not as a defect.

**A6 — the r58 settlement artifact is a 230 KB single-line JSON and is NOT scanner-shaped.**
`.ufo/waves/round-58/evidence/w1-settlement.json`: schema `mori-wave-settlement-v1`, 230 411 bytes,
**2 lines** (line 1 = 230 410 bytes), no `results` list → the scanner FAILs it
(`results_not_list, seats_mismatch, lane_bad, wave_bad, round_bad`).
It is nevertheless one of the six `ARTIFACTS` copy targets in `count-c2.py`
(`corpus/evidence/sources-r59/w1-settlement-r58.json` ← `.ufo/waves/round-58/evidence/w1-settlement.json`),
so any byte-exact claim drawn from it must use an **offset** span, not a `line` span — a `line:1`
quote would be the whole 230 KB line. Useful anchors already located:
`"totals"` @ offset 114, `"members":3153` @ offset 134, `"states":` @ offset 214,
`"unique_dispatch_sha256"` @ offset 260, `"waves":[` @ offset 344.
For the five r5x results files the line spans are trivially small and stable (all five share
identical line layout): line 2 ` "lane": "mori",`, line 3 ` "round": <n>,`, line 4 ` "wave": "w1",`,
line 5 ` "seats": <n>,`; `"lane": "mori"` @ offset 3 and `"results": [` @ offset 63 in every file.

**A7 — the 36 tree copies are 17-byte stubs, not artifact copies.** Each
`trees-c2/t*/corpus/evidence/sources-r59/w1-results-r5{4,5,6}.json` is
`{\n "seats": 2,\n}` / `3` / `4` (17 bytes, sha `2a9da59e6ccb…`, `fa0bce89a2bb…`, `3286ddb07c59…`),
byte-different from the real artifacts (`ea48a0cc…`, `2e5b0a0f…`, `19536201…`). This is by design —
each hostile tree is evaluated in isolation by `eval_entry` against its own stubs, which is why the
trees arm is green at the freeze revision. But it means the tree stubs must **not** be mistaken for
the `corpus/evidence/sources-r59/` copies the real C2 entry must land: those copies must be
byte-equal to the `.ufo` artifacts at the measured revision (`tree=ok` arm) and their pins must be
the real artifact SHAs (`ea48a0cc07fa948c70d90103b589db0cdf7d48343aa689a3e56742c1cd59335f` r54,
`2e5b0a0f94d1fa5b90b2804d370db87d25d5197fa65bc4f26441d939b8d9763b` r55,
`19536201a689c954899a2e6decf322ef2c5f3d2ed9bc8ddb75229636b1e5d761` r56,
`29e7a35df544315d3bb6ac2f0da96235342d77a1f8306ab25b8a27675669beb1` r57,
`a57b660d9f41c55dc5d614444f60f1cf658d19a55a530c9788369e5fb7ec61fc` r58,
`b259e73cdddef7ff8565a01c6d97f79da8b112aa6c7dbb97a8aa541b4f0b5588` r58 settlement).
**Update (post-landing):** the real copies are now committed and byte-equal — 7 files under
`corpus/evidence/sources-r59/` (r53, r54, r55, r56, r57, r58 results + r58 settlement), each
`byte_eq=True` against its `.ufo` artifact at HEAD, with the SHAs above. The r53 copy is *extra*:
the frozen `ARTIFACTS` map names only six, and a claim citing the r53 copy is what broke the entry
arm at `be737211` — see §8.

**A8 — registry context for the C2 `rows` arm.** `corpus/SOURCES.md` at the freeze revision holds
**325** registry rows, ids `S001…S552` with **no duplicate id**, every row exactly **11 cells**,
status histogram `{mined:272, queued:24, rejected:29}`. `count-c2.py` requires, per cited S-id:
11 cells, `cells[7]=="mined"`, `cells[10]==ENTRY` (`corpus/knowledge/wave-settlement-artifacts-r59.md`
exactly — a comma-joined multi-path `used-by` would fail). New rows for this round must therefore
be opened at `S553+` and used-by must name the new entry alone. Existing rows are already mined for
other entries (`S550` → `corpus/knowledge/driver-events-r58.md`; `S551` rejected;
`S552` mined → `corpus/lessons/round-58.md`), so re-using any of them for the new entry would break
the `used-by` exact-match check.
**Update (post-landing):** the registry now holds **333** rows (ids `S001…S560`), still no duplicate
id and still every row exactly 11 cells. The eight new rows are `S553`–`S559` (`status=mined`,
`used-by` = `corpus/knowledge/wave-settlement-artifacts-r59.md` exactly — satisfying the `rows` arm)
plus `S560`, the reconciliation row for the round-58 routed defect 2 (S552 duplicates S478, same
DOI `10.1109/TSC.2026.3698682` and same PDF sha `1603404d…`); S560 is `status=rejected`,
`used-by` = `corpus/lessons/round-59.md`. Note `corpus/lessons/round-59.md` does not yet exist in
the lane, so S560's `used-by` currently points at an unwritten lesson file — a documentary
follow-up for the scribe/L1, not a counter failure (the counter only checks rows the entry cites).

**A9 — member role enum is clean everywhere.** All 14 wave-results files use only roles inside the
frozen enum `{scout, reviewer, critic, connector, sentinel, executor, mutation-tester, revenger,
simplifier, scribe}`; **zero** `agent_bad` failures. `planner` is absent from the corpus and is
absent from the tool's `ROLES` tuple — consistent with the contract note that "`planner` is not a
validator role" (orchestrator ruling 2026-10-19).

**A10 — name uniqueness is clean everywhere.** All 14 wave-results files have
`len(names) == len(set(names))` (42/37/49/34/64/68/68/8/67/74/64/64/64/64), zero duplicate names.
The scanner's `duplicate_names` reason fires on none of them.

---

## 5. Verdict

* **C1**: met at the freeze revision (`C1=met selftest=ok fixtures=ok real=ok pointers=ok`, exit 0),
  tool pin exact, `REGCHECK_SELFTEST pass=12 fail=0`, 13 hostile fixture trees present,
  do-nothing control at `2b9f0397` gives `failed=tool_absent` exit 1. Consistent with the contract.
  Still met at HEAD `7b86704d` (`C1=met … rev=7b86704d7c…`, exit 0).
* **C2**: met at HEAD `7b86704d` — `C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok
  pins=ok tree=ok claims=13 files=6`, exit 0, with N=13 ≥ 10 and F=6 ≥ 3 as the contract requires.
  At the freeze revision the tool-side arms were already green (`selftest=ok scan=ok drift=ok
  trees=ok`; 12 hostile trees with distinct frozen `expect` prefixes; r54–r58 OK with
  `members==seats`; r53 FAIL on `report_file`) and only the four data arms were red — by design,
  pre-data. The landed data meets every frozen constraint listed in A6/A7/A8: 7 byte-equal copies
  (6 results + 1 settlement), 13 byte-exact pin-bound claims over 6 distinct artifacts, the four
  frontmatter keys in the first ten lines, and new `S553+` rows with `status=mined` and `used-by`
  exactly the entry path.
* **Results corpus**: no `seats`≠`members` mismatch, no duplicate names, no bad role, no
  empty-string output in any committed wave-results file. The material anomalies are the three
  output-less files that nevertheless scan OK (A1), the frozen r53 schema drift (A2), the two
  non-wave `*results*.json` files (A3), and the missing round-49 / round-50-w1 artifacts (A4).

## 6. Commands used (all read-only against the lane)

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD
git -C … log --oneline -12 ; git -C … diff --stat 60b3a76a 8ff344ff
git -C … ls-tree -r --name-only <rev>              # population discovery
git -C … show <rev>:<path> | sha256sum              # tool + artifact pins
git -C … show <rev>:<path> | python3 -c …           # per-file json survey
python3 .ufo/waves/round-59/count-c1.py --selftest
python3 .ufo/waves/round-59/count-c1.py <rev> --scratch $S
python3 .ufo/waves/round-59/count-c2.py --selftest
python3 .ufo/waves/round-59/count-c2.py <rev> --scratch $S
python3 tools/mori-register-check.py --selftest
python3 tools/mori-settlement-scan.py --selftest
python3 tools/mori-settlement-scan.py <one materialized file>
# sandbox clone (scratch only, never the lane):
D=$S/sandbox && mkdir -p $D && git -C <lane> archive <rev> | tar -x -C $D \
  && git -C $D init -q && git -C $D add -A && git -C $D commit -q -m base
python3 $D/.ufo/waves/round-59/count-c2.py <sim-rev> --repo $D --scratch $S/sim
```
All materialized copies and the sandbox clone live under
`/fast/scratch/hyaku/mori-r59/Mo59Executor45/` (removed before yield). No file in the lane was
written except this report; no `git add`/`commit`/`checkout`/`reset` was issued against the lane —
the only commits in this seat's history are inside the throwaway scratch clone, whose toplevel was
asserted with `git -C $D rev-parse --show-toplevel` → `/fast/scratch/hyaku/mori-r59/Mo59Executor45/sandbox`.

## 7. Risks / blockers

* None blocking. C2 was red on one arm at `be737211` (§8) and was corrected to met at `7b86704d`
  before this seat closed.
* Residual, non-blocking observations for the L1 (no remediation attempted by this seat, per
  detection-only scope): the scanner's `empty_output`/`notes_nonnull` counters do not gate the
  verdict (A1); the r58 settlement artifact's single-line layout forces offset spans (A6); the
  `*results*.json` naming collision with the round-23 falsify fixtures (A3); and waves 49 / 50-w1
  have no results artifact (A4).
* Sibling overlap note: the C2 landing seat owns `corpus/knowledge/wave-settlement-artifacts-r59.md`
  and `corpus/evidence/sources-r59/`; this seat wrote only this report and touched neither.

## 8. Mid-wave defect found in the landed C2 data (now corrected upstream)

A sibling builder landed the C2 data as `be737211`. Re-running the frozen counter at that
revision showed **one red arm**:

```
$ python3 .ufo/waves/round-59/count-c2.py be7372114ded3075e5f5a15227ffec977df22f7d --scratch $S
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=ok pins=ok tree=ok claims=14 files=7
  rev=be7372114…  failed=entry
```

Root cause, isolated by re-running the frozen counter's own `eval_entry()` against the committed
bytes of `be737211` (imported from the frozen counter file, not re-implemented):

```
eval_entry(<root of be737211>) ok=False stats={'claims': 14, 'files': 7}
   reason: files:outside=corpus/evidence/sources-r59/w1-results-r53.json
   offending claim line: - **K11** — the round-53 artifact's member entries carry a report_file
     field — a key absent from r54-r58 members. Quote: `   "report_file": ".ufo/waves/round-53/w1/
     Mo53Fr01.md"` (corpus/evidence/sources-r59/w1-results-r53.json:line:…; pin …)
```

The frozen `ARTIFACTS` map in `count-c2.py` names exactly six copy paths — r54, r55, r56, r57, r58
results and the r58 settlement. The landed entry also landed a 7th copy
(`corpus/evidence/sources-r59/w1-results-r53.json`, byte-equal to the r53 artifact) and cited it
in claim `K11`; `eval_entry` therefore raised `files:outside=`, which the counter maps to the
`entry` arm → `C2=unmet`. Note the r53 file is the **drift** artifact the contract deliberately
keeps outside the claim set ("the r53 file MUST scan FAIL — schema drift, reported not fixed"),
so a claim on it can never satisfy the frozen predicate.

Sandbox proof of the minimal fix (throwaway clone under this seat's scratch, never the lane;
`git -C $D rev-parse --show-toplevel` asserted):

```
# variant 1 — drop only the offending claim line (K11), change nothing else:
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6
  rev=efe7647a45e64eca6c1d3bb99192474b339d45c9                                       EXIT=0
# variant 2 — additionally drop the r53 copy, its S559 source line and its S559 row:
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6
  rev=d523ff16b1770fb500332308c9a51b1a35d60f99                                       EXIT=0
```

Both variants clear the entry arm with N=13 ≥ 10 and F=6 ≥ 3, so the fix is not a threshold
gaming exercise. Upstream landed variant 1 as `7b86704d` ("data correction — K11 demoted to prose
(r53 copy outside frozen ARTIFACTS)"), and the counter at that revision reads
`C2=met … claims=13 files=6`, exit 0. This seat made no lane edit; the sandbox commits are confined
to `/fast/scratch/hyaku/mori-r59/Mo59Executor45/sandbox` and were deleted before yield.

This is the same failure shape the counter's own hostile tree `t06-outside-file` is built to catch
(`expect.txt` → `files`): a claim citing a path outside the frozen `ARTIFACTS` set. The lane's own
hostile-tree arm was green throughout, because the trees are evaluated in isolation — the real
entry was not.

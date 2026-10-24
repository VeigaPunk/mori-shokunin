# PinIntegrity: round-20 C1 re-pin verification (scope: pin mechanics)

**Verdict: HOLDS.** All five enumerated re-pin checks reproduce. Scope limit: this verdict does not certify the classification gate the pin relies on. That gate is contested (section 3), and the committed record lags the working copy (section 3.2). The post-pin `none` is receipt-attested, not re-observed (section 5).

Basis: lane HEAD 8f8c58e (committed 10:57:29Z). Read-only checks run about 11:00-11:12Z. I ran no census, no pin, no drift, and made no edits outside this report and /tmp scratch.

## 1. Enumerated checks

| # | Claim | Result | Evidence |
|---|---|---|---|
| 1a | header census_sha256 = sha256(tools/mori-census.sh) | HOLDS | line 2: 87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28. `sha256sum tools/mori-census.sh` is identical, and so is `git show 2061780:tools/mori-census.sh` piped to sha256sum. Blob c7d952d6 at 2061780, e4d9384, 2eeae04, 8f8c58e and the working tree. |
| 1b | header pinned_ts | HOLDS | line 3: 2026-10-21T10:53:07Z. Equals the census clock: script lines 382-384 set TS_UTC from NOW_EPOCH at start. Matches knowledge doc section 4. Baseline written 10:54:21.66Z. |
| 1c | header volatile_fields | HOLDS, exact | line 4, 103 tokens. Equals script DRIFT_VOLATILE_SPECIAL (line 2771) followed by DRIFT_COUNTER_KEYS (lines 2744-2764), recomputed in Python: True. Lines 1, 5, 6 are verbatim script strings (lines 2925, 2929, 2930). |
| 2 | roll line present | HOLDS | line 69: `MORI_CENSUS: DRIFT (findings=<V> drift=<V> unavailable=<V> surfaces=<V>)`, the last canonical line. Format matches script line 2714. |
| 3 | r10 byte-unchanged vs 2061780 | HOLDS | `git show 2061780117e6ca637725004897bd288d3ba7e988:corpus/evidence/baseline-r10-20261015T2231Z.json > /tmp/pinintegrity/r10-at-2061780.json`, then `cmp` gives rc 0. sha256 0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478, matching the knowledge doc. `git rev-list 2061780..HEAD -- <r10> <census>` is empty, rc 0. |
| 4 | census unchanged vs entering tip | HOLDS | `git ls-tree 2061780... -- tools/mori-census.sh` gives 100755 blob c7d952d6. Identical at HEAD and in the working tree (`git hash-object`). The range 2061780..HEAD has 3 commits (e4d9384, 2eeae04, 8f8c58e); none touches the census. |
| 5 | post-pin receipt | HOLDS, receipt only | `.ufo/waves/round-20/evidence/c1-drift-r20-postpin.txt` holds `MORI_DRIFT: none` and `rc=0` (22 bytes). mtime 10:55:31.57Z. Committed identically. Not re-run (section 5). |

Tied checks, all pass:
- Body: 63 canonical lines (file lines 7-69). 0 unmasked numeric volatile values. 0 raw ISO timestamps. 30 FINDING and 31 SURFACE lines. WATCHDOG_STALE, WATCHDOG_ABSENT and 10 WAVE_UNSETTLED_AGE rows are present.
- Pin equals measured pre-pin state: the FINDING/SURFACE id-level diff of r10 against r20 equals exactly the 26 FINDING/SURFACE tokens in `c1-drift-r10-prepin.txt` (22 `+`, 4 `-`).
- Counting command reproduced (set difference, equivalent to the contract's `comm`). Entering 50 tokens: 8 unclassified against r13, 0 against r20. Pre-pin 49 tokens: 7 against r13, 0 against r20. Pre-pin is a subset of entering; only `-FINDING:WATCHDOG_STALE` differs.
- r20 register: 50 entries. Classes 29/19/2/0, so census-regression is 0. Every entry has evidence and reason.
- MORI_* environment: none set in my shell (names only). The header records no environment by design, so the L1's environment is [INFERENCE] only.

## 2. Caveats on what the pin certifies (not mechanical breaks)

2.1 Commit. The contract says the pin is taken "at the measured commit", which it names as the entering tip 2061780. Lane HEAD at pin time was 2eeae04 (committed 10:47:09Z; 8f8c58e followed at 10:57:29Z). The header and receipts record no commit. No token effect observed: the id-level match in section 1 holds, and lane.mori is `young` with no commit-derived field in that state. Wording deviation for the integrator.

2.2 The post-pin `none` shows stability over a window of about 70 s (pin written 10:54:21.66Z, receipt 10:55:31.57Z). It does not test correctness, which agrees with CriticC1Claim.md. The receipt names neither command nor baseline path. [INFERENCE: it compared against r20, since r10 cannot yield none.]

2.3 Stamp. The file name carries `T1051Z` while the header says 10:53:07Z. r10 has the same pattern (`T2231Z` against `pinned_ts=2026-10-15T22:26:29Z`). The header is authoritative. Cosmetic.

2.4 `.ufo/waves/round-20/evidence/c1-pin-probe-scratch.json` (committed in 2eeae04) is a superseded text baseline with a valid header (`pinned_ts=2026-10-21T10:22:12Z`). Nothing references it as the baseline. Cosmetic risk of a wrong `--drift` target.

## 3. Classification gate: contested, and the record moved after pin and commit

3.1 Row-level effect (verified). r10 has 11 WAVE rows (lines 26-36), including `aggregator-r10` and `aggregator-r10-resume` (lines 26-27). r20 has 10 rows (lines 54-63). It drops both aggregator rows and adds `shokunin-train-20261016-w24`. From here on, `--drift` will not flag the two aggregator rows as absent. r10 stays byte-identical, so the removal remains auditable by comparing r10 with r20.

3.2 Committed register differs from the working register.
- HEAD `drift-classification-r20.json`: 17855 bytes, blob 0ee9789e. This is the size the working file had at its 10:51:02Z mtime. [INFERENCE: HEAD holds that version.]
- Working copy: 18350 bytes, blob 93faa899, mtime 11:04:41Z. That is after the commit and after the wave-2 critics.
- Differences: the `dissent` text (adds the BROKEN answer quoted in 3.3), and the `-FINDING:WAVE_UNSETTLED_AGE` entry's `evidence` and `blind_spot`. Classes, token keys and counts are identical.
- Knowledge doc: working copy has 2 extra lines (`verified-at`, `recheck`), written 11:05:15Z.
- Lesson: working copy edited again at 11:09:38Z.
- The committed record therefore does not contain the answer to the critic.

3.3 The dissent. `falsify/AdjudicateWaves.md` (11:03:04Z) returns BROKEN. It asks that WAVE_UNSETTLED_AGE be `census-regression`, and that the re-pin be blocked until a non-author record accounts for each removed wave ("explicit settlement or an evidenced cleanup disposition"). It also asks that row identity be kept, with w24 classified separately. `falsify/CriticC1Claim.md` (11:03:03Z) returns PARTIAL: the 8-to-0 count and the post-pin `none` are self-certifying.

3.4 The L1's answer is factually supported (checked). Fleet commit `e20f4fa` (souji-shokunin, 2026-10-18T23:58:39-03:00) reads "remove 96 pushed-receipt checkpoint artifacts (operator sweep 2026-10-18)" with "Receipt: pushed". `git show --name-status -- .ufo/waves/aggregator-r10 .ufo/waves/aggregator-r10-resume` shows 18 `D` entries (10 resume, 8 base). `souji-shokunin/census/operator-sweep-20261018/approval-list.tsv` rows 56-73 list the same 18 paths as `pushed` (set-equal). So a non-author cleanup disposition exists for every removed file. Not covered:
- (a) Explicit settlement. The adjudicator accepts either form.
- (b) Row-level split. The `obs` token (live-state, "set shifted 11 -> 10") still pairs w24 with the aggregator rows. The receipt is attached only to the `-FINDING` entry.

3.5 The frozen contract names the four classes but does not define them. The definitions (for example `live-state` = "census code unchanged, host/fleet state differs") are the L1's, in drift-repin-r20.md section 2. The gate therefore rests on L1-authored rules. Whether cause-based `live-state` is acceptable for the removal of unsettled-warning rows is a judgment this item does not settle. I did not verify the adjudicator's census-branch claim (tools/mori-census.sh lines 917-927).

## 4. Moving target during this run
- Register: 10:51:02Z, 17855 bytes (seen at 11:01:53Z). Now 11:04:41Z, 18350 bytes.
- Knowledge doc: 10:56:04Z, 5251 bytes, now 11:05:15Z, 5592 bytes. Lesson: now 11:09:38Z, 9406 bytes.
- Unchanged throughout: baseline r20 (10:54:21.66Z), r10 (2026-10-15 19:26:58 -03), census (2026-10-20 17:39:03 -03), pre-pin receipt (10:53:07.39Z), post-pin receipt (10:55:31.57Z).

## 5. Not done, and checks for the main agent
- The census was not run. It is heavy and outside this item's authority. Once, at the integrated HEAD: `bash tools/mori-census.sh --drift corpus/evidence/baseline-r20-20261021T1051Z.json; echo rc=$?`. Expect `MORI_DRIFT: none` with rc 0 only if lane state has not moved since 10:55:31Z. Any tokens must be classified, not suppressed.
- Decide WAVE_UNSETTLED_AGE explicitly.
  - (a) census-regression: the gate blocks, and the pin must be withdrawn as the reference, with r10 staying as the reference.
  - (b) live-state: cite e20f4fa and approval-list rows 56-73 in the committed register, with a row-level note for w24.
  - Either way, record the decision.
- Reconcile HEAD against the working tree for the register, knowledge doc and lesson. Commit or revert. The committed record must not lag the evidence it cites.
- Decide what "at the measured commit" means: 2061780 (then document the off-commit pin), or pin-time HEAD 2eeae04 (then record the commit in the header or receipts).
- Would flip to BROKEN: WAVE_UNSETTLED_AGE reclassified as census-regression while the pin stands; any unclassified token in the integrated re-run; or the pin withdrawn for a reason the record does not state.
- Tooling: none installed. Commands used: read-only git (show, ls-tree, cat-file, hash-object without -w, rev-list, log -n, rev-parse), /usr/bin/jq 1.8.2, Python stdlib reads, and scratch writes only under /tmp/pinintegrity/. No subagents. Not opened: .ufo/interactive-sessions, .ufo/worktrees, .jj, omp logs. Fleet repo: git history of e20f4fa only. Sibling lane: souji-shokunin census approval list only.

# CriticC2Admission — mori round 25, wave 2 (falsify C2 as a learning claim and capability)

Seat: `MoriR25.CriticC2Admission` (critic, leaf). Lane HEAD measured: `07a31ae` (wave-2 attempt ledger).
I wrote nothing in the lane except this file. All runs happened in a private clone,
`/fast/scratch/hyaku/mori-r25/w2-CriticC2Admission`, which I removed after writing this report.

## Verdict: **weakened**

The declared after-value holds literally. `python3 -I -B tools/mori-job-runway.py --selftest` prints
`MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` and exits 0. The cases blob is `48df844a` at both `7634be75` and HEAD.
The cases landed before the tool. I found no false claim of provenance.

As a learning claim and as a capability, C2 is weaker than it presents:

- The counted value measures conformance to the L1's own 21 examples. It does not measure whether the tool reads omp correctly.
- The tool's binary half can only ever report a constant that the knowledge entry already states.
- Most of the knowledge entry is ground that the same round's PROVINCE note assigns to kumitate.
- The committed evidence that amendment A1 requires for C2 is missing at HEAD.

The defensible learning is narrower. It is the documentation-versus-code gap and the configured-versus-effective reading (knowledge F1–F3 and F12–F13), plus the SKILL error pattern.

**Strongest counterexample.** Two other implementations also pass the counted after-value `PASS 21/21`, and both are known to give false numbers:

- The pre-A2 tool `09f55b62` passes 21/21. It fails 14 of the 18 A2 supplementary cases, giving exit-0 or exit-1 numbers that omp does not use.
- A naive 26-line evaluator that I wrote passes 21/21 through the tool's own `_selftest`. It hard-codes two-space indentation. For `async:\n    maxJobs: 50` it reports `RUNWAY_DEFAULT`, effective 100, exit 0. The landed tool reports `set 50`, `RUNWAY_AS_CONFIGURED`.

The counted value therefore cannot tell the admitted tool apart from tools that misreport an ordinary config.

## Findings

### F1 — the frozen-case after-value does not discriminate correctness (severity: high for capability admission)

The commands below ran in the private clone at `07a31ae`.

```
$ python3 -I -B tools/mori-job-runway.py --selftest
MORI_JOB_RUNWAY_SELFTEST: PASS 21/21            (exit 0)
$ python3 -I -B old/mori-job-runway.py --selftest          # old/ = git show 09f55b62:tools/mori-job-runway.py, with the frozen cases.json beside it
MORI_JOB_RUNWAY_SELFTEST: PASS 21/21            (exit 0)
$ python3 -I -B old2/mori-job-runway.py --selftest         # same pre-A2 tool, with supplementary-cases.json as its cases.json
MORI_JOB_RUNWAY_SELFTEST: FAIL 4/18             (exit 2)
CASE R01: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_DEFAULT'; exit: expected 2, got 0; ...
CASE R07: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_AS_CONFIGURED'; exit: expected 2, got 0; ...
CASE R11: ... configured.value: expected None, got 9; effective: expected None, got 9
$ python3 -I -B tools/mori-job-runway.py --selftest --cases tools/fixtures/mori-job-runway/supplementary-cases.json
MORI_JOB_RUNWAY_SELFTEST: PASS 18/18            (exit 0)
```

I also ran a naive evaluator through the landed tool's own harness: `rw.evaluate = evaluate; rw._selftest()`. It reuses the contract regexes, applies `^async:` plus `^  maxJobs: *(\S*)` to the config, and applies `max(1, min(clamp, base))`. Its `evaluate` body is 26 lines. Results:

```
frozen cases:        MORI_JOB_RUNWAY_SELFTEST: PASS 21/21   (exit 0)
supplementary cases: MORI_JOB_RUNWAY_SELFTEST: FAIL 5/18
config "async:\n    maxJobs: 50", real binary:
  naive:  configured {absent, None}, effective 100, RUNWAY_DEFAULT, rc 0
  landed: configured {set, 50},      effective 50,  RUNWAY_AS_CONFIGURED
```

All 21 frozen configs use two-space indentation (case dump in `w1/ReviewFrozenCases.md` and my own dump). The real binary appears in none of them. Each case's `binary` is a one-to-three-line synthetic string modelled on the L1's own byte search, for example J01 `const Ui = !u.parentTaskPrefix ? new Xm({ maxRunningJobs: () => Math.min(100, XPe.get(R)) ...`.

`PASS 21/21` therefore shows that some implementation agrees with 21 examples of the contract's grammar. The A2 fixes are what make the tool safe to use. They sit in the supplementary file, which is uncounted by design (contract A2, lines 151–156), so the after-value does not move between the unsafe tool and the safe one.

### F2 — the cases are independent of the tool's code, not of its specification (severity: medium; disclosed, not falsely claimed)

- **Order held.** `7634be7` was committed at 06:49:49-03:00, and `git cat-file` shows the cases blob `48df844a` there. The tool `09f55b6` was committed at 07:02:38-03:00. The builder's sandbox commit `9cb0dc3` has parent `7634be75` (`w1/BuildJobRunwayTool.md:28-31`).
- **One author for both rules and expectations.** `cases.json` `note` says "Expected values derived from the contract rules by the L1 before any tool exists". The same agent wrote rules 1–7, the 21 expected values and the integration. Round 24's admitted C2 used a separate case seat that "opened no implementation" (`corpus/lessons/round-24-verifier-spotcheck.md:85`). Round 25 is weaker on this point.
- **Round-24 M8 recurs.** The builder implemented the compare semantics "per the fixture's own `note`" (`w1/BuildJobRunwayTool.md:66`), so it read the frozen cases while building. Round 24 recorded the same thing as mistake M8 (`corpus/lessons/round-24.md:67`).
- **No independent oracle for omp's behaviour.** The expected values follow from the L1's rules. The rules were wrong about omp on eleven YAML forms (contract A2, lines 139–142), and all 21 frozen expected values still "agree" (`w1/ReviewFrozenCases.md` "Case disagreements: 0").
- I found no committed text claiming more independence than this. The contract and the fixture note say "frozen before any tool", which is true.

### F3 — the tool tells an operator nothing beyond `min(100, <config.yml value>)` (severity: high for the capability framing)

I scanned upstream history with a blobless clone of `https://github.com/can1357/oh-my-pi`. For each `v*.*.*` tag carrying `packages/coding-agent/src/sdk.ts` (634 tags, 267 distinct blobs), I applied the contract's rule-2 regex and a looser `Math.min(N, …maxJobs)` probe:

```
v8.0.0   (first tag scanned)  contract_regex=()       any_min_near_maxJobs=()        # 147 tags before the feature
v12.19.0 (2026-02-22)         contract_regex=()       any_min_near_maxJobs=('100',)  # 433 tags
v18.3.1  (2026-09-25)         contract_regex=('100',) any_min_near_maxJobs=('100',)  # 54 tags, through v18.12.6 (2026-10-21)
```

- The source at `v18.3.0:sdk.ts:1787` is `Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 100))`. The source at `v18.3.1:sdk.ts:1970` is `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings))`.
- The clamp number is **100 in every one of the 487 releases** that has the feature. Its only change in history is a change of shape with the same value, and that is exactly the change that rule 2 misses.
- [INFERENCE: from source text, not shipped binaries] On the 433 releases from v12.19.0 to v18.3.0, the tool would report the clamp as `absent`, giving `RUNWAY_UNKNOWN`. The string-literal argument `"async.maxJobs"` cannot match `[\w$]+\.get\([\w$]+\)`.

So, across every release that exists, the binary read returns either the constant 100, which the knowledge entry, the lesson and the SKILL error pattern already print literally, or `UNKNOWN`. Everything the operator gets beyond config.yml can be written as one sentence: "effective = max(1, min(100, async.maxJobs))".

The tool does not report anything an operator would act on:

- headroom, meaning the live running-job count; the contract scope bound says so;
- the value the settings stack actually resolved (knowledge F13);
- which of the three numbers (gate target 85, config 200, effective 100) governs dispatch.

Checked and **not** a counterexample: every running omp process maps to the on-disk binary. `readlink /proc/{3591,9003,523216}/exe` gives `/home/vgpnk/.local/bin/omp` with no `(deleted)` marker, and the sha256 is `85d9daf3…ccfa4`. The disk read matches the running processes today.

### F4 — most of the knowledge entry is kumitate's ground by mori's own PROVINCE note (severity: medium, adjacency)

- The round-25 PROVINCE note says "the semantics behind the clamp — what the job manager counts …, the exact refusal text, and the fact that only a top-level session builds the manager — are kumitate's OMP task/hub ground" (`PROVINCE.md:335-339`). The standing header refuses "dispatch and orchestration mechanism (→ kumitate)" (`PROVINCE.md:12`).
- `corpus/knowledge/harness-job-capacity-r25.md` has facts F1–F13. Eight of them cover that ground:
  - F4, the count rule;
  - F5, the queued flag;
  - F6, the refusal text;
  - F7, the top-level manager;
  - F8, a refusal creates nothing;
  - F9, the bash and eval fall-through;
  - F10, fleet refusal records;
  - F11, seat-gate mechanism.

  Six of the 14 decision-table rows are "(not a tool state)" observations about refusals, seats and the gate. Learned-fact bullets 2–4 in `corpus/lessons/round-25.md:15-23` and the SKILL r25 error pattern (`SKILL.md:649-661`) draw on the same facts.
- Mori's own new ground is F1–F3 and F12–F13: the settings documentation states no maximum, the code clamps at 100, and on this host config 200 gives effective 100. That is a genuine advance; wave-1 `CriticLearningClaim.md` Q2 also found 0 prior mori hits for `maxJobs`, `maxRunningJobs` or the clamp.
- The route SiblingOverlap proposed (R1 → kumitate: `omp-task-contract.md:197` "effective live OMP setting is UNKNOWN", with no `async.maxJobs` row) is not recorded as routed. `corpus/lessons/round-25.md` has 0 `kumitate` hits. The only kumitate-side mentions are the pre-existing `considerthese/2026-10-21.md:13,23`. The PROVINCE note mentions the gap but routes nothing.
- FR15 is created and advanced in the same round, as a self-declared append-only extension. Round 24 did the same and was admitted (`PROVINCE.md:274-278`), so this is a tradeoff for the closure to weigh rather than a defect.

### F5 — the committed evidence for C2 is missing at HEAD (severity: high if it is still missing at closure)

- Contract A1 (lines 126–130) requires `.ufo/waves/round-25/evidence/runway-selftest.txt`, with `revision:`, `command:` and `exit:` headers and the full stdout. The C2 "Sourced" bullet (lines 90–92) requires "A live run against this host is committed as evidence".
- `git ls-tree --name-only HEAD .ufo/waves/round-25/evidence/` lists seven files: pressure-selftest, routed-r24 ×4, and wave1/wave2 bind. There is no runway file. The working tree has none either.
- Knowledge F12 and the PROVINCE admission note cite the live run only through a seat report (`w1/BuildJobRunwayTool.md` §2).
- This is the stale/missing selftest-evidence class that the round itself names as mistake M1 and as QUALITY 76.

### F6 — would a strict closure call C2 trivial? (judgment)

- **As a capability (the tool): yes, plausibly.** The capability route in the quality bar is "a capability shown running and entered in SCORECARD's capability table" (`.scratch/goal-20261022-hyaku-12h.md`, Quality bar). There is no round-25 capability-table entry at HEAD. `SCORECARD.md:1546` is a declaration only, and the last table is "capabilities: first demonstrated round 24" at `:1530`. The computation is two regexes plus `max(1, min(...))`, its non-null output across all releases is a constant (F3), and its counted test does not separate it from broken variants (F1). The wave-1 critic reached the same conclusion: "Yes, as framed now" (`w1/CriticLearningClaim.md` Q3).
- **As learning: no, not trivial.** The F1–F3 gap is new to mori, primary-sourced (S099, S100, S101, S103, S104), and contradicts a fleet instruction: `scripts/hyaku/lane-addendum.md:88-89` points lanes at config.yml (per `w1/CriticLearningClaim.md` Q2). It qualifies under "admitted knowledge on uncovered ground" and under "SKILL.md … error pattern grounded in admitted entries". The overreach (F4) and the missing evidence (F5) are fixable defects. They are not a tradeoff the judge must reject.

## Impacted axes

- **coverage** (claimed): weakened. The count is real but measures specification conformance, not capability (F1, F3).
- **calibration**: wording such as "capability" and "new PROVINCE ground" overstates what the bytes show (F3, F4). These are not counted mismatches.
- **adjacency**: risk of duplicate authority with kumitate on job-manager semantics, with no route recorded (F4).
- **depth**: a small gain from F1–F3 and F12–F13; this is unaffected.

## Smallest safe correction (none of these narrows the declared after-value)

1. Commit `evidence/runway-selftest.txt` and the live-run evidence, with `revision:`, `command:` and `exit:` headers, measured after the last tool change (`fbecc59`). Point knowledge F12 at that file instead of at the seat report. (F5)
2. Add one disclosure sentence to the C2 result rows (SCORECARD and the lesson): "PASS 21/21 is conformance to L1-authored rule examples; the pre-A2 tool `09f55b62` also passes it and fails 14/18 supplementary cases; the clamp number is 100 in every upstream release, and the tool's value-change detection has never fired." (F1, F2, F3)
3. Present C2's learning through the knowledge and SKILL route: F1–F3 and F12–F13 plus the r25 error pattern. Mark F4–F11 as cited kumitate-ground mechanism, not as mori-owned learning, and record route R1 to kumitate in the lesson (report, never edit). (F4)
4. Optionally, to make any future counted runway value discriminate: add frozen cases with four-space indentation, an unreadable binary, and the real 18.12.6 bytes (or its sha-pinned excerpt). Freeze them with a new contract before any future tool change. This does not apply to round 25.

## Bounds kept and tools

- The lane checkout was read only. My only write in it is this report. I ran no git or jj writes in the lane, ran no jj command at all, did not run omp, and did not edit any settings. The binary was read as bytes and `/proc/*/exe` was only resolved.
- The upstream clone was opened by ordinary `git clone --filter=blob:none` from GitHub into scratch and removed afterwards.
- Tools: system python3 3.14.8, git 2.56.0, and coreutils. **I installed or updated nothing.**
- The main agent should check that F5's evidence files land, and re-run `python3 -I -B tools/mori-job-runway.py --selftest` at the closure tip.

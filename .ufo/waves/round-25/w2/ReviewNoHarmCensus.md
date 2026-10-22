# ReviewNoHarmCensus — round-25 wave-2 no-harm re-run for operability

Seat: `MoriR25.ReviewNoHarmCensus` (leaf; no subagents, no background jobs, no lane writes except this report).
Instant of record: **2026-10-22** (after the wave-2 tip landed).
Run surface: **lane tip `07a31ae8e22514bbc603afa13f2de7c8b2424cca`** (git-archive extract, not the lane checkout).

## Verdict

**HELD — no regression, no harm.** Every assigned command reproduces the wave-1 baseline
(`.ufo/waves/round-25/w1/NoHarmBefore.md`, pinned to `7634be75`) or is a new expectation that passes.
**No result differs adversely from the baseline.** The only deltas are: (a) the pressure
supplementary run — absent from the baseline sweep — passes at its new, larger expectation;
(b) `mori-routed-check.py --round 25` is new since baseline and holds 4/4; (c) the known
environmental `mori-round17-jj-regressions.py` red reproduces byte-identically and unchanged.

## 1. Method

Extract (recipe identical to the baseline's):

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive 07a31ae8e22514bbc603afa13f2de7c8b2424cca | tar -x -C <extract>
```

- Run directory: `/fast/scratch/hyaku/mori-r25/w2-NoHarmCensus` — **outside `/tmp`**, per the known
  `/tmp` refusals (baseline §1). `TMPDIR=<extract>/.scratch` for every run.
- **Byte fidelity:** all 29 files under `tools/` in the extract were compared against
  `git show 07a31ae8…:<path> | sha256sum` — 29/29 identical (`checked=29 fail=0`). The census run
  left **no residue in `/tmp`** (`ls -d /tmp/mori-census-selftest.*` → none) and wrote only under
  `TMPDIR` (`tools/mori-census.sh:211-213`).
- **Tool bytes vs baseline:** `mori-census.sh`, `mori-pressure.py`, `mori-routed-check.py` and
  `mori-round17-jj-regressions.py` are sha256-identical to the baseline table (NoHarmBefore §5):
  `87b8d680…`, `2c815f84…`, `cd313053…`, `da3e080a…`. `git diff --stat 7634be75 07a31ae8 -- tools/`
  touches exactly 4 paths: `tools/fixtures/mori-job-runway/supplementary-cases.json` (new),
  `tools/fixtures/mori-pressure/supplementary-cases.json` (+268 lines), `tools/mori-job-runway.py`
  (new), `tools/mori-routed-r24.py` (new). **None of the baseline selftest tools changed bytes**, so
  identical results are the expected outcome — and are what was observed.

## 2. Assigned runs — command, exit, summary, baseline comparison

| # | Command (from the extract, `TMPDIR=<extract>/.scratch`) | Exit | Summary line | Baseline (`7634be75`) |
|---|---|---|---|---|
| 1 | `bash tools/mori-census.sh --selftest` (flag named in header usage, `tools/mori-census.sh:397`) | **0** | `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)` (~16 s) | **identical**: PASS 134/134, exit 0 (NoHarmBefore §3 row 1) |
| 2 | `python3 -I -B tools/mori-pressure.py --selftest` | **0** | `MORI_PRESSURE_SELFTEST: PASS 12/12` / `MATCHER: rejected 48/48 corrupted expectations` | **identical** (§3 row 2) |
| 3 | supplementary: `python3 -I -B tools/mori-pressure.py --selftest --cases tools/fixtures/mori-pressure/supplementary-cases.json` | **0** | `MORI_PRESSURE_SELFTEST: PASS 16/16` / `MATCHER: rejected 64/64 corrupted expectations` | **no baseline row** — the baseline sweep did not run the supplementary file; see §3 |
| 4a | `python3 -I -B tools/mori-routed-check.py --repo <lane> --rev 07a31ae8… --round 25` | **0** | `{"base":"c725aa37…","held":4,"items":4,"round":25,"status":"held"}`; rows R1–R4 all `held:true`, `reasons:[]` | **new since baseline** (round-25 ledgers did not exist at `7634be75`); see §3 |
| 4b | `python3 -I -B tools/mori-routed-check.py --repo <lane> --rev 07a31ae8… --round 24` | **0** | `{"base":"c725aa37…","held":4,"items":4,"round":24,"status":"held"}`; rows R1–R4 all `held:true` | **matches**: baseline ran `--round 24` at `7634be75` and `28b79d3d` → held 4/4, same base `c725aa37` (NoHarmBefore §3a) |
| 5 | (confirmatory) `python3 -I -B tools/mori-round17-jj-regressions.py --selftest` | **1** | `SELFTEST FAIL: … cases=17 match=8 mismatch=9 … assertions=204 failed=9 retained=False` | **identical failure signature** (§4): same counts, same exit, same known environmental cause |

"the supplementary run" is the pressure supplementary (`--cases` flag, `tools/mori-pressure.py:391-392`),
pairing with run 2 per the contract's mutant-replay clause (`.ufo/waves/round-25/contract.md:35-36`:
surviving round-24 pressure mutants are "killed by new supplementary cases"). The other
`supplementary-cases.json` (mori-job-runway) belongs to C2 coverage, exercised by the C2 seats, not
by this census.

## 3. The three deltas, precisely

1. **Pressure supplementary grew 7 → 16 cases in round 25 and passes 16/16** at the tip. At the
   baseline commit the same fixture had 7 cases (`git show 7634be75:tools/fixtures/mori-pressure/supplementary-cases.json`
   → 7 cases); at the tip it has 16 (fixture sha256 `2497ae3e854c13ab09da8e3d8c746b321e150df15a5b2f8e493c897280d30900`).
   The growth is the declared round-25 mutant-kill work (contract `:35-36`, "not counted toward C1"),
   so `PASS 16/16` is the new correct expectation, not a drift. The frozen main case file is
   untouched (12/12 as at baseline).
2. **`mori-routed-check.py --round 25` holds 4/4 at the tip** (new datapoint; no baseline existed).
   Its R4 row found the round-25 dispatch ledgers exactly where the assignment note says they are —
   **`.ufo/waves/round-25/wave1-attempts.json` and `.ufo/waves/round-25/wave2-attempts.json`** — each
   `verify_status:"clean"`, `verify_findings:["LEDGER_CLEAN"]`, `verify_exit:0`, with specs
   `wave1-spec.json`/`wave2-spec.json`. The `--round 24` re-run reproduces the baseline's held 4/4
   with the same base commit `c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130`.
   Read-only-against-the-lane is verified from the tool source: every git invocation is
   `git --no-optional-locks -C <repo> …` with `stdin=DEVNULL` (`tools/mori-routed-check.py:128-160,173-191`),
   and the ledger verify runs committed tool bytes through `python3 -I -` (`:351-359`); the lane
   working tree stayed clean (`git status --porcelain -- tools/` → empty after the runs).
3. **`mori-round17-jj-regressions.py` red is unchanged and stays environmental.** From this bare
   extract it fails exactly as the baseline documented: exit 1, `cases=17 match=8 mismatch=9 …
   assertions=204 failed=9` (195/204 pass). Tool bytes are identical at baseline and tip
   (`da3e080aa5181e8e00872c1d5f0dd97862c495da03adce0b1aa31e27fbcb89f0`, both revisions). Per-case
   assertion ids were not re-extracted at the tip (the selftest deletes its scratch tree on failure,
   `retained=False`, even with `--scratch`), but identical bytes plus an identical summary signature
   pin the same `jj_config_redirected` / missing-ancestor-workspace cause the baseline measured
   (NoHarmBefore §4.3-4.5). Nothing in round-25 work may be credited or blamed for it; any quote of
   this red must carry the baseline's in-lane-green qualifier.

## 4. Hygiene

- Lane untouched by this seat: only this report file was written in the lane; extract and all scratch
  under `/fast/scratch/hyaku/mori-r25/w2-NoHarmCensus` (removed after this report was written).
  No `/tmp` residue (checked after the census and r17 runs).
- **Tool installs: none.** Nothing was installed or upgraded (pacman host-wide pause respected;
  `python3 3.14.8`, `git 2.56.0`, `bash`, `tar`, `jq 1.8.2` already present — same host versions as
  the baseline table).
- No jj command was run anywhere; no git mutating command touched the lane or the fleet root.

## 5. Residual risk and verification gaps

- The 15 other baseline selftest entry points (content-review, dispatch-ledger, evidence-loss,
  freeze-order, journal-window, misroot-sweep, retention-gate, retention-reconcile, round13–17,
  seat-terminal, wave-settlement, silence-cases, round19 harness) were **not re-run** — out of this
  seat's assigned four commands. Mitigation: `git diff --stat 7634be75 07a31ae8 -- tools/` shows
  none of their bytes changed since the baseline sweep, so the baseline's green rows remain the
  operative evidence for them.
- `mori-routed-r24.py` (C1) and `mori-job-runway.py` (C2) were not re-measured here; their before/
  after counts are the assigned scope of the RerunC1Count / RerunC2Count seats.
- routed-check R4 asserts ledger cleanliness at the tip commit only; ledgers appended after
  `07a31ae8` are outside this run.

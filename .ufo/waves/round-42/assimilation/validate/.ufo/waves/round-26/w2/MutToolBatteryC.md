# Round 26 wave 2 — MutToolBatteryC (mutation battery for C2, M21–M30)

Seat `MoriR26.MutToolBatteryC`, 2026-10-22. Leaf seat: no subagents, no background jobs.
Target: the C2 tool `tools/mori-oom-killers.py` at the lane tip under attack
`16935e24c93fa7e7567413d7ec091339a5df1474` (contract `.ufo/waves/round-26/contract.md:48-118`).
Mutant designs: `/fast/scratch/hyaku/mori-r26/MutCaseDesign/mutants.md` (§2, M21–M30).
Sandbox clone: `/fast/scratch/hyaku/mori-r26/wt-w2mutC`, branch `r26-wt-w2mutC`, HEAD `16935e24`,
`git status` clean before and after. No commit, no ref, no index change in the lane; read-only git only.
Harness and raw log: `/fast/scratch/hyaku/mori-r26/MoriR26.MutToolBatteryC/harness.py` and
`battery.log`. Tools installed or upgraded: none (python3 3.14.8, git, jq-free JSON handling only;
no pacman transaction, no unit touched).

## Verdict

The landed tool is **not** defective: the pristine bytes pass every detector, and all ten mutants
are injected defects that the battery kills or exposes as a gap in the frozen artifacts.
6 of the 10 mutants **survive the counted artifact** (`cases.json`, the contract's declared
detector). Every survivor is a **coverage finding about the artifact**, not a defect of the tool:
the counted after-state `PASS 32/32` cannot certify the error path, the field comparison inside
the selftest, the missing/empty-cases rule, the `--inputs` path, or the privacy rule.

## Baseline (pristine bytes, same commands, same clone)

| item | value |
|---|---|
| tool sha256 | `1a71b2dfa45ef547b1a5042cc71a28ae63f54af35d0c4973f6056bf439b2f8e4` |
| `cases.json` sha256 / cases | `84d2343f1d672a4597a4ec5efe0fd048eb399e8b4f0f5b86cc483ff8f2e547af` / 32 |
| `cases-supplementary.json` sha256 / cases | `277684eb8f622c2c3eeaf118f65c28d02c0196dd459052aa387989b4fb11269d` / 32 |
| `--selftest` | `MORI_OOM_KILLERS_SELFTEST: PASS 32/32`, exit 0 |
| `--selftest --cases …/cases-supplementary.json` | `MORI_OOM_KILLERS_SELFTEST: PASS 32/32`, exit 0 |

Harness detectors, all on the pristine bytes: D2 (missing cases file) exit 2, no `PASS`; D3 (empty
cases file) exit 2, no `PASS`; D4 (`--inputs` on an acted synthetic input) exit 1,
`KILLER_ACTED`; D5 (privacy grep for the invented names of that synthetic input) no leak; D7
(tampered copy: `c01`'s `earlyoom.thresholds.term_mem_pct` 10.0 → 11.0) `FAIL 31/32` with the
field line; D8 (copy with one case removed) printed total 31 = the file's case count; D9 (result
shape) exactly `schema`, `earlyoom` (11 contracted keys), `oomd` (`state`, `notices_this_boot`),
`verdict`. Baseline is green, so every kill below is attributable to the mutant and not to a
pre-existing failure.

Detectors used: D1 = the exact line `MORI_OOM_KILLERS_SELFTEST: PASS N/N` plus exit 0, with N
taken from the file handed to `--cases` (32 for both artifacts); D2, D3, D4, D5, D7, D8, D9 as
defined in the mutant design (`mutants.md:80-140`). D8 compares the denominator of the printed
`PASS n/m` / `FAIL n/m` line with the case count of the file handed in.

## Result table

`K` = killed (the detector failed on the mutant), `S` = survived. "frozen" = `cases.json`
(counted artifact, 32 cases); "suppl" = `cases-supplementary.json` (32 cases).

| mutant | frozen | suppl | other detector | adapted? |
|---|---|---|---|---|
| M21 kill-threshold matcher demands `sending ` | **K** `FAIL 29/32` | **K** `FAIL 29/32` | — | yes, inverted |
| M22 grammar match not prefix-anchored | **K** `FAIL 31/32` | **K** `FAIL 31/32` | — | yes, anchors dropped |
| M22L literal design change (`.match`→`.search`, anchors kept) | S | S | — | probe |
| M23 byte-array `MESSAGE` not decoded | **K** `FAIL 30/32` | **K** `FAIL 30/32` | — | yes, branch returns `""` |
| M24 uncaught exception exits 1 | S `PASS 32/32` | **K** exit 1, traceback | — | yes, two points |
| M24L literal design change (drop generic guard only) | S | S | — | probe |
| M25 selftest ignores `expect.fields` | S | S | **K** D7 | one point |
| M26 selftest always prints PASS | S | S | **K** D7 | one point |
| M27 missing/empty cases file silently falls back | S | S | **K** D2 and D3 | yes |
| M27L literal design change (swallow the OSError) | S | S | D2 exit 2 (internal error) → S | probe |
| M28 selftest prints a hard-coded N | **K** `PASS 20/20` | **K** `PASS 20/20` | **K** D8 (total 20 ≠ 31) | no |
| M29 `--inputs` ignores the file | S | S | **K** D4 | no |
| M30 result object echoes journal message text | S | S | **K** D5 and **K** D9 | one point + one point |

Restoration: after every mutant the file bytes were rewritten from the pristine buffer and
`sha256sum` re-checked. All 13 runs report
`restored sha: 1a71b2dfa45ef547b1a5042cc71a28ae63f54af35d0c4973f6056bf439b2f8e4 (OK)`; the clone
is clean and the tool hash equals the baseline hash.

## Kills, with the actual output

* **M21** — `FAIL c01-host-quiet-thresholds: earlyoom.thresholds.kill_mem_pct: missing in result
  (expected 5.0)`, same for `kill_swap_pct` and `term_mem_pct`; 29/32. The kill-threshold line
  stops parsing, so `thresholds` is `null` and the four threshold numbers of `c01` cannot be read.
* **M22** — `FAIL c21-nearmiss-midline-sigkill: verdict: got 'KILLER_ACTED' expected
  'KILLERS_QUIET'`, `exit: got 1 expected 0`, `earlyoom.actions.sigkill: got 1 expected 0`; 31/32.
  A grammar phrase that appears after a prefix is counted as an action.
* **M23** — `FAIL c11-byte-array-message-action: verdict: got 'KILLERS_QUIET' expected
  'KILLER_ACTED'`, `exit: got 0 expected 1`, `earlyoom.actions.sigterm: got 0 expected 1`; 30/32.
  The same two failures follow for `c12` (byte 255 → U+FFFD).
* **M24** (supplementary only) — stdout empty, exit 1, stderr last line
  `ValueError: journal record without a numeric __MONOTONIC_TIMESTAMP`. The contract
  (`contract.md:105`) fixes exit 2 with `KILLERS_UNKNOWN` and an `error` field for this input.
* **M25** — on the tampered copy the mutant prints `MORI_OOM_KILLERS_SELFTEST: PASS 32/32`,
  exit 0; the pristine tool prints `FAIL 31/32` with
  `earlyoom.thresholds.term_mem_pct: got 10.0 expected 11.0`.
* **M26** — on the tampered copy the mutant prints `MORI_OOM_KILLERS_SELFTEST: PASS 31/32`,
  exit 0; the pristine tool prints `FAIL 31/32`.
* **M27** — `--selftest --cases <missing>` and `--selftest --cases <empty>` both exit **0**
  (live fall-back) instead of the contracted exit 2 (`contract.md:60-63`).
* **M28** — `MORI_OOM_KILLERS_SELFTEST: PASS 20/20` on both artifacts, and on a 31-case copy.
* **M29** — `--inputs <acted synthetic file>` returns `KILLERS_QUIET`, exit 0 (the live verdict of
  this host), instead of `KILLER_ACTED`, exit 1.
* **M30** — the `--inputs` stdout carries the invented name and uid of the synthetic input
  (`leaks=['alpha', 'uid 1000']`) and the result object gains the top-level key `evidence`
  (D9: `top=['earlyoom', 'evidence', 'oomd', 'schema', 'verdict']`).

## Adaptations (the design was written blind; the landed code shape differs)

* **M21** — the landed matcher is already the correct one:
  `tools/mori-oom-killers.py:105-107` compiles `r"^SIGKILL when mem avail …"`. The design's
  direction ("`^sending SIGKILL when` → `^SIGKILL when`") is already satisfied, so I inverted it:
  the mutant re-introduces the `sending ` requirement. Same defect, same expected kill.
* **M22** — the landed patterns are `^`-anchored, so the design's literal `re.match` → `re.search`
  is a no-op. Probe **M22L** applies exactly that and survives both artifacts
  (`PASS 32/32`): with `^` and no `re.MULTILINE`, `search` can only match at the start. The mutant
  therefore drops the `^` anchor from the four reader-relevant patterns and uses `.search`, which
  realises "matched after stripping leading whitespace, **prefix-anchored**" being broken
  (`contract.md:80-81`).
* **M23** — dropping the normalisation outright would make `text.lstrip()` raise on a list, which
  is a different defect (exit 1). The mutant instead makes `decode_message` return `""` for a
  byte array, so the line never matches the grammar, which is the designed defect.
* **M24** — the landed code routes `SetupError` through its own handler
  (`tools/mori-oom-killers.py:802-804`), so removing only the generic `except Exception` guard is
  inert: probe **M24L** survives both artifacts. The mutant therefore (i) raises `ValueError`
  instead of `SetupError` at the malformed-timestamp point (`tools/mori-oom-killers.py:296`) and
  (ii) removes the generic guard (`tools/mori-oom-killers.py:807-809`), which yields the traceback
  and exit 1 the design predicts.
* **M27** — the landed code raises `SetupError` for an unreadable or empty cases file, so
  "swallow it" has no literal form. Probe **M27L** (swallow the `OSError` only) still exits 2,
  with `internal error: UnboundLocalError: cannot access local variable 'raw'`, so D2 and D3 hold.
  The mutant realises the designed defect literally: the selftest branch catches the setup error
  and falls back to live collection (`tools/mori-oom-killers.py:780-782`).
* **M25, M26, M29, M30** — one-point edits of the landed code (`fields = expect.get("fields")` →
  `fields = None`; `if passed == total and total > 0:` → `if True:`; `inputs = _load_inputs(…)` →
  `inputs = collect_live()`; one extra `evidence` list plus one result key). M26 keeps the real
  per-file counts, so it is "always PASS" but not "hard-coded N"; that is M28's job.
* **M28** — applied as written (`PASS 20/20`).

## Survivors and what they mean for the C2 claim

1. **M24 (survives the counted artifact, killed by the supplementary one).** The counted file has
   no malformed-timestamp case, so the contract's rule 4 (`contract.md:105-106`: "an uncaught
   exception never exits 1") is not certified by the counted after-state; only `c35` of the
   supplementary file kills it. This is direct evidence for the design's claim that neither
   artifact is a superset of the other (`mutants.md:§1.1`).
2. **M25 and M26 (survive both artifacts, killed only by a tampered copy).** The frozen file pins
   fields on 19 of its 32 cases, yet the declared receipt `PASS 32/32` is unchanged if the tool
   stops comparing `expect.fields` altogether, or never compares anything. The counted value
   therefore certifies verdict-level agreement only; the field pins are enforced by the code, not
   by the artifact, and nothing in the committed after-state would show a field-level regression.
3. **M27 (survives both artifacts, killed only by a harness probe).** "An empty or missing cases
   file is a setup error (exit 2), never a silent fall-back" (`contract.md:60-63`) is invisible to
   an after-state that runs the selftest against a file that always exists.
4. **M29 (survives both artifacts, killed only by `--inputs`).** The selftest calls
   `read_inputs` directly (`tools/mori-oom-killers.py:672`), so the `--inputs` CLI path is never
   exercised by either artifact. The counted receipt says nothing about that plumbing.
5. **M30 (survives both artifacts, killed only by the privacy and shape checks).** The selftest
   prints only the `PASS`/`FAIL` lines, never the result object, so a result that carries `MESSAGE`
   text, process names or uids leaves `PASS 32/32` intact on both files. The privacy rule
   (`contract.md:107`) is covered by neither artifact.

Taken together: 6 of 10 mutants survive the contract's declared detector, and the five rules they
guard (rule 4 error path, the selftest's field comparison, the empty/missing cases rule, the
`--inputs` path, the privacy rule) are all outside the counted artifact's reach. The supplementary
artifact covers exactly one of them (rule 4) and adds nothing on the other four. Under the
contract's own definition of the counter ("the tool passes N/N frozen cases", `contract.md:52-56`)
the landed value `PASS 32/32` stands; the gap is in the artifact, not in the tool.

## Not run

* D10 (live mode on a host whose journal is unreadable) was not run: it needs a host state this
  seat must not create, and it is outside the two detectors this item named.
* No claim is made about mutants M01–M20, M31–M57; only M21–M30 and the three literal-change
  probes were applied.
* The supplementary artifact is **not** counted by `count-c2.sh`; it is used here only as a second
  battery, and its `PASS 32/32` does not change the C2 after-value.

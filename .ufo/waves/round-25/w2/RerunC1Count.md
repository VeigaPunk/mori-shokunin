# W2 RerunC1Count — attack on C1 (calibration) measurement

Verdict: **held.** The C1 measurement reproduces exactly. From a fresh clone at the lane tip
`07a31ae8e22514bbc603afa13f2de7c8b2424cca`, the before run at `28b79d3d` reports `items: 4`,
`mismatches: 4`, `held: 0`, hygiene red, exit 1; the after run reports `mismatches: 0`, `held: 4`
of `items: 4`, hygiene held, exit 0 — at the pinned rev `e06d4a02` **and** at the current tip.
Both committed evidence files are byte-identical to my reruns. Independent hand re-derivation
with plain git reads agrees on all four counted items (D1, D2, D3, D5) and hygiene (D4), at both
revs. No defect found in the measurement.

## 1. Rerun (fresh clone)

Clone: `git clone --no-hardlinks <lane> /fast/scratch/hyaku/mori-r25/w2-RerunC1Count`, HEAD =
`07a31ae8e22514bbc603afa13f2de7c8b2424cca` = `git -C <lane> rev-parse master`. Tool copy blob
`ddc7a43da2185ee2c2383b98c3385050e9fca659` at tip; absent at `28b79d3d` (consistent: the check
lands mid-round). All runs `python3 -I -B tools/mori-routed-r24.py --repo <lane> --rev <rev>`
from the clone cwd.

| Run | rev | stdout says | exit |
|---|---|---|---|
| before | `28b79d3d…` | `items:4, mismatches:4, held:0`; D1 `evidence_file_missing`; D2 7 reasons (3 phrases present, 2 phrases missing, banner, no `(k4)`+`total` line); D3 `no_line_with_correction_s07_and_pass_marker`; D5 3× `axis_score_mismatch` (coverage 5!=6, operability 6!=7, depth 4!=5); hygiene `no_pycache_ignore_rule` | 1 |
| after (pinned) | `e06d4a02…` | `items:4, mismatches:0, held:4`, all rows no reasons, hygiene held | 0 |
| after (tip) | `07a31ae8…` | identical JSON to the pinned after run modulo `rev`/`rev_commit` (verified programmatically) | 0 |

Clone-repo control: `--repo <clone>` produces JSON identical to `--repo <lane>` except the
`repo` field — the tool reads git objects only, no working-tree dependence.

## 2. Byte fidelity of the committed evidence

Evidence format is 4 header lines (`revision:`, `tool_revision:`, `command:`, `exit:`) + full
stdout. Reconstruction from my rerun bytes:

- `routed-r24-before-a5.txt`: committed sha256 `d4739847d768866c538b9c150423f46a457b85868612486e27aea785e75d38e6` = reconstruction `d4739847…` (exact). Stdout body sha `8f78c926…` equals my before-run stdout sha.
- `routed-r24-after-a5.txt`: committed sha256 `3641635405cafa274d739b71f778fb7d5837e963a5730dbe975fc99959451a77` = reconstruction (exact). Stdout body sha `92a2bb0d…` equals my after-run stdout sha.
- Committed blobs == lane worktree files for `routed-r24-before-a5.txt`, `routed-r24-after-a5.txt`, `pressure-selftest.txt` (git show | cmp: all equal).
- `tool_revision: e06d4a02…` is writer-declared, not tool output; independently verified: blob `ddc7a43d` first appears at `e06d4a02` ("routed-r24 check gains counted item D5 (contract A5)"); the older tool commits `e54b644b`/`e4b6f6d9` hold the A1/A3-era blob `a08043fe`. Header honest.

## 3. Hand re-derivation, plain git reads only — per item

**D1 — agree (held at tip, red at base).** `git show <tip>:.ufo/waves/round-25/evidence/pressure-selftest.txt` (cat -A): lines 1–5 are `revision: ec840f9df9999bb6f5796c07128db0fec26e7c7e`, `command: python3 -I -B tools/mori-pressure.py --selftest`, `tool_blob: 5785c5b23233a5ed1d2116ab610f9aa0cf3b12ec`, `fixtures_tree: c28ccfdf6233ecc04c5b7f827cc3c66c3d8da9c8`, `exit: 0`. `git merge-base --is-ancestor` R→tip: yes. Blob of `tools/mori-pressure.py` = `5785c5b2…` at R **and** tip; tree `tools/fixtures/mori-pressure` = `c28ccfdf…` at R **and** tip. Body (lines 6+) byte-equal to `MORI_PRESSURE_SELFTEST: PASS 12/12\nMATCHER: rejected 48/48 corrupted expectations\n`. I also extracted R (`git archive R -- tools/mori-pressure.py tools/fixtures/mori-pressure`) and ran `python3 -I -B tools/mori-pressure.py --selftest`: exit 0, stdout byte-equal to the recorded body — so even the original pre-A1 stdout-equality form holds. At base: `git cat-file -e 28b79d3d:.ufo/waves/round-25/evidence/pressure-selftest.txt` fails → red, as declared.

**D2 — agree (held at tip, red at base).** Over `corpus/knowledge/system-pressure-r24.md` from `git show`, normalized (strip `*`/`_`/backticks, casefold, fold whitespace): exactly 1 heading starting `## corrections`; `## facts` and `## decision table` present; decision table data rows 11 at tip vs 11 at `28b79d3d` (not fewer); outside the corrections section 0 matches of `refreshed on (each|every) read`, `spike[^|.]{0,60}(is|are|can be|may be) invisible`, `null[^|.]{0,15}means[^|.]{0,15}undefined`; `only when the next` and `not tracked` both present outside; `this section wins` absent from the whole normalized entry (A4 whole-file gate); inside, a line carries `(k4)` and `total`. At base: all three phrases present, both positives missing, banner present, no `(k4)`+`total` line → red, matching the 7 before-reasons.

**D3 — agree (held at tip, red at base).** n = cases in `tools/fixtures/mori-pressure/supplementary-cases.json` at `4f05dd5a` = **7** (S01–S07; counted as `len(json["cases"])` — see §5). `corpus/lessons/round-24.md` at tip line 100 contains `Correction`, `S07`, `PASS 7/7` twice, neither followed by a digit, and hex tokens `4f05dd5a` and `c484f6d` which both resolve to commits holding 7 cases (token `a536b18` holds 6; the predicate needs "a" qualifying token — two qualify). Narrative cross-check: S07 absent at `a536b18` (6 cases), present at `c484f6d` and `4f05dd5a` — the lesson's own story is byte-true. At base: no line containing `Correction` at all (`grep` empty) → red.

**D5 — agree (held at tip, red at base).** Pinned parse of `git show 28b79d3d:SCORECARD.md` lines 1499–1506 yields exactly: calibration 5 (line 1501), coverage 6 (1502), operability 7, depth 5, freshness 5, adjacency 6 (1504) — the contract's six values, each found once. Base `## Axes` rows: coverage 5, operability 6, depth 4, freshness 5, calibration 5, adjacency 6, every Last change `round 1` → 3 rows differ from pinned → red. Tip rows: coverage 6 "round 12 (5 → 6; round 13's self-assessed 7 was not held)", operability 7 "round 13 (6 → 7)", depth 5 "round 12 (4 → 5)", freshness 5 / calibration 5 / adjacency 6 "round 1" (score equals round-1 value, so `round 1` is allowed) → exactly one row per axis, all scores equal pinned → held.

**Hygiene D4 — agree (held at tip, red at base).** `.gitignore` at tip line 3 is exactly `tools/__pycache__/`; at base no pycache/`.pyc` line. No `!` negation line mentioning `pycache`/`.py` in any tracked `.gitignore` at tip (only root `.gitignore` exists). No tracked path under `tools/` contains `__pycache__` or ends `.pyc` at either rev.

## 4. Findings by severity

- **High / Medium: none.** No defect in the tool's predicates, the reruns, or the evidence bytes.
- **Low (wording, already verified harmless):** `routed-r24-after-a5.txt` pins `revision: e06d4a02…`, while the claim text says "at the landed tip" and the tip has since moved to `07a31ae8` (three `.ufo`-only commits: w1 reports, w2 bind, w2 ledger; `git diff --name-only e06d4a02..07a31ae8` touches no file the tool reads). I ran the after-value at the actual tip: `mismatches: 0`, held 4/4, hygiene held, exit 0, stdout identical modulo `rev` fields. No fix needed; the evidence's rev is the honest measurement-time tip.
- **Low (label):** the evidence `tool_revision:` header is written by the seat, not emitted by the tool. It is correct here (see §2). If a future evidence file copies this pattern, the header stays unverified by the tool itself — the reviewer's independent blob check (as done in §2) is the closure.
- **Note (out of my lane scope, flag for others):** the lane worktree is dirty: `M corpus/SOURCES.md` plus untracked `.ufo/waves/round-25/w2/*.md` sibling reports and `.scratch/`. The C1 tool is unaffected (object reads only), but seats reading SOURCES.md from the worktree see uncommitted bytes.
- **Note (by design):** D1's `--rerun` is report-only and never gates (tool docstring; `_check_d1`), so the declared after-value does not require re-executing R. I re-executed R manually anyway (§3) and it matches.

## 5. Derivation traps I hit (recorded so siblings don't repeat them)

- `len(json.load(f))` on `supplementary-cases.json` is 3 — it counts top-level keys (`schema`, `note`, `cases`). The case count is `len(json["cases"])` = 7. My first hand count of "3" was this bug; the tool's `_count_cases` (tools/mori-routed-r24.py:745-755) reads the `cases` list correctly.
- Slicing the D1 body by byte offset of `exit: ` needs the full `exit: 0\n` line length (offset+8), not offset+1; my first slice was off by one line-start. `tail -n +6` (after the 5 header lines) is the clean form. Both errors were mine; the committed bytes were right.

## 6. Residual risk and verification gaps

- The D5 pinned parse is anchored to base SCORECARD.md line numbers 1499–1506; it fails closed (contract wording) and the base commit is immutable, so the anchor cannot drift — but any future tool copy with changed line constants would silently re-pin. Out of scope to fix.
- Exit code 2 (unreadable repo/rev) was not exercised; exit 0/1 semantics were, on all three runs.
- I did not run the routed tool's own `--rerun` flag; I performed the equivalent extraction and execution by hand, which is the stronger form (independent of the tool under test).
- LSP: no language server answered for this Python lane script; findings are grounded in source reads (tools/mori-routed-r24.py:86-89, :145-156, :424-747, :745-822) and git object reads, not text grep alone.

Tooling: no tools installed or upgraded (system git + python3 only); pacman untouched per host pause. Lane writes: this report file only. Scratch clone and run outputs under /fast/scratch/hyaku/mori-r25/ removed after this report.

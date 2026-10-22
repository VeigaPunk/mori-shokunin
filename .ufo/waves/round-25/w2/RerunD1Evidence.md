# w2 RerunD1Evidence — attack C1 item D1 evidence (`pressure-selftest.txt`) + QUALITY 76 staleness sweep

Verdict: **held.** Every header line of `.ufo/waves/round-25/evidence/pressure-selftest.txt` checks out
against git objects, and the body is byte-for-byte the stdout of the named revision's tool rerun from a
git-archive extract. The QUALITY 76 sweep over the other round-25 evidence files finds the counted evidence
fresh; the only stale-by-the-letter files are the two A1-history routed files the contract already discloses.

## D1 evidence, header line by line (git object reads; lane read-only)

File: `.ufo/waves/round-25/evidence/pressure-selftest.txt` (306 bytes, 7 lines). Observed tips moved during
this review — 07a31ae8 → 47b2b93 → 8aa9fa41 → **e0e33c118e1eea2d40241a58861b7d0ad536e062** — because wave-2
integration was landing; every check below was re-run at the final observed tip.

| Header line | Check | Result |
|---|---|---|
| `revision: ec840f9df9999bb6f5796c07128db0fec26e7c7e` | `git cat-file -t` → `commit`; `git merge-base --is-ancestor ec840f9d HEAD` at e0e33c11 | exists; **ancestor: yes** |
| `command: python3 -I -B tools/mori-pressure.py --selftest` | exact string vs A1's declared command | **matches** |
| `tool_blob: 5785c5b23233a5ed1d2116ab610f9aa0cf3b12ec` | `git rev-parse R:tools/mori-pressure.py`, at carrier `7bb0fe61:…`, and at `HEAD:…` | all three **= 5785c5b2…** |
| `fixtures_tree: c28ccfdf6233ecc04c5b7f827cc3c66c3d8da9c8` | `git rev-parse R:tools/fixtures/mori-pressure`, at carrier, at HEAD | all three **= c28ccfdf…** |
| `exit: 0` | rerun exit code (below) | **0, matches** |

Header order is exactly the A1 order (revision, command, tool_blob, fixtures_tree, exit). `R` is also an
ancestor of the carrier commit (`git merge-base --is-ancestor ec840f9d 7bb0fe61` → yes), and the carrier is
an ancestor of the tip.

## Body byte-for-byte rerun at R

- `git archive ec840f9d | tar -x` into `/fast/scratch/hyaku/mori-r25/w2-RerunD1Evidence/extract-ec840f9d`
  (removed afterwards). Fidelity check: `git hash-object` of the extracted `tools/mori-pressure.py` =
  `5785c5b23233a5ed1d2116ab610f9aa0cf3b12ec` — the header's tool_blob.
- Rerun in the extract: `python3 -I -B tools/mori-pressure.py --selftest` → **exit 0**, stdout **82 bytes**,
  empty stderr.
- Body after the five header lines: **82 bytes**, `body == stdout` True; `cmp evidence-body rerun-stdout` →
  **rc=0**; body equals the A3 literal
  `MORI_PRESSURE_SELFTEST: PASS 12/12\nMATCHER: rejected 48/48 corrupted expectations\n` exactly.

## QUALITY 76 carrier discipline (`corpus/QUALITY.md`, criterion 76, round 25)

- The file was first carried by `7bb0fe61` (07:27:03Z-3), whose only change is the evidence file itself
  (`git diff-tree --name-status -r 7bb0fe61`: one `A`). The 76 "mechanism to watch" (stale file landed in a
  commit that also edited the tool it reports on) does **not** fire: the last pressure-tool edit is round-24
  `c484f6d0` (06:20:36) and the last fixtures edit is `ec840f9d` (07:26:50) itself — evidence landed 13 s
  after the fixtures commit, satisfying CriticSizing F2's "lands after the last change to the pressure tool
  and fixtures".
- 76's equality clause (blob/tree identical at named revision and at the revision carrying the file) holds at
  the carrier `7bb0fe61` and at every observed tip through e0e33c11.

## QUALITY 76 sweep of the other round-25 evidence

- `runway-selftest.txt` (landed `47b2b93`, named revision `d3b7af2`): full header discipline
  (revision/command/tool_blob `239dd8eb…`/fixtures_tree `eddd10fb…`/exit 0); blob and tree identical at
  `d3b7af2`, carrier `47b2b93`, and tip; `cases.json` blob `48df844a…` unchanged from its freeze at
  `7634be75` through tip. Rerun at `d3b7af2` from a git-archive extract: exit 0, stdout byte-equal to the
  body, `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`. **Fresh** — the C2 declared after-value is certified by
  committed evidence.
- `runway-selftest-supplementary.txt` (same revision): rerun
  `--selftest --cases tools/fixtures/mori-job-runway/supplementary-cases.json` (blob `b506cfc7…` identical
  `d3b7af2`↔tip) → exit 0, body byte-equal, `PASS 24/24`. **Fresh** (not counted toward the after-value).
- `runway-live-run.txt`: live host observation (adds `run_at:`/`host_binary:`/`binary_sha256:`; no
  `fixtures_tree:` line). It is not a self-test evidence file, so 76's fixture-tree clause does not apply,
  and the contract marks it "not the after-value". For the record, rerunning the same command at `d3b7af2`
  today reproduced its JSON body byte-for-byte (exit 1, `RUNWAY_CLAMPED`, effective 100 vs configured 200) —
  a time-of-review coincidence, not a certifiable property. No defect.
- `routed-r24-after-a5.txt` / `routed-r24-before-a5.txt` (the counted C1 evidence, landed `26c84859`):
  `tool_revision e06d4a02` → tool blob `ddc7a43d…`, identical at the named revision, the carrier, and the
  tip. **Fresh** under 76. (Body re-derivation by rerunning the routed tool is the live re-check other seats
  run; not re-executed here.)
- `routed-r24-after.txt` / `routed-r24-before.txt` (landed `9b1a2f12`, A1 measurement):
  **stale by 76's letter at the current tip.** The tool they report — blob `a08043fe…` at `e54b644b` — was
  replaced at `e06d4a02` (blob `ddc7a43d…`, D5 added), so at the revision carrying these files today the
  shipping tool differs, and rerunning their declared commands with the tip tool emits 4-item output, not the
  recorded 3-item output. This is **disclosed, not hidden**: A5 pins the counted after-value to the `-a5`
  pair and says "The A1 measurement at `e54b644b` (3 of 3) stays in `evidence/routed-r24-after.txt` as
  history". Severity: informational. Smallest fix, if the integration owner wants the directory to be
  76-clean without reading the contract: one `superseded-by: routed-r24-after-a5.txt` line (or relocation
  out of `evidence/`); the byte content itself must not change, since it is the historical A1 record.

## Findings summary

1. **[info]** `routed-r24-after.txt` / `routed-r24-before.txt` are stale under QUALITY 76's letter at tip;
   disclosed as history by A5, counted evidence is the `-a5` pair. No action required by the contract as
   written.
2. **[info]** `runway-live-run.txt` has no `fixtures_tree` header — inapplicable to a live-run observation
   under 76; its bytes are host-mutable and the contract excludes it from the after-value.

No actionable defect remains in scope. Residual risks / verification gaps: (a) the lane tip moved four times
during review; if integration lands further edits to `tools/mori-pressure.py`, `tools/mori-routed-r24.py`,
`tools/mori-job-runway.py` or their fixture trees, the 76 equalities must be recomputed against the new tip
(one `git rev-parse <tip>:<path>` per path); (b) routed evidence bodies were not re-derived by rerun in this
seat (out of scope — the C1 live re-derivation is measured at the integrated commit elsewhere); (c) the
pressure rerun was executed once and is deterministic (exact byte match, no timestamps in output).

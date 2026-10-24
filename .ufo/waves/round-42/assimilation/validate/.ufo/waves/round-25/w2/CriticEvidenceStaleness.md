# CriticEvidenceStaleness — round 25, wave 2 (falsify)

Seat: `MoriR25.CriticEvidenceStaleness` (critic, leaf). Target: every evidence file committed this round under
`.ufo/waves/round-25/evidence/`, judged against QUALITY 76 (`corpus/QUALITY.md:340-347`). For each file I checked
whether it names a full revision, the command and the exit code, and whether its body is byte-equal to what the
named revision's tool prints. I also checked for the M1 mechanism (evidence landing in a commit that also
edited the tool) and for any file written before the final change to its tool.

Measured at lane tip `07a31ae8e22514bbc603afa13f2de7c8b2424cca`. All code ran in a private clone
(`/fast/scratch/hyaku/mori-r25/w2-CriticEvidenceStaleness`) plus `git archive` extracts per revision, which are
now removed. Tools installed or updated: none.

## Verdict

**C1 evidence: held. C2 evidence: broken. Overall: weakened.**

- All seven committed files under `evidence/` replay byte-equal at the revision and tool they name, with
  matching exit codes.
- No commit that landed an evidence file also edited a tool, so the strict M1 form is absent.
- C2's binding evidence was never committed. Amendment A1 requires `runway-selftest.txt`, and the C2 sourced
  clause requires a committed live run. Neither exists. The landed text cites a seat-report run that predates
  the final change to the tool. The values happen to reproduce at the shipping tool (see F1), but by QUALITY 76
  a tally is never a pass.
- The A1-era pair `routed-r24-before.txt` and `routed-r24-after.txt` was written before the final change to the
  `routed-r24` tool. At the tip, which still carries both files, the tool blob differs, and nothing in the files
  marks them as superseded.

## Per-file results

| File | Header (rev / command / exit) | Replay | Tool blob at named rev = carrier = tip | Written after final tool change |
|---|---|---|---|---|
| `pressure-selftest.txt` | `revision` ec840f9d (40 hex), command, `tool_blob`, `fixtures_tree`, `exit: 0` | byte-equal at `ec840f9d`. Stdout is identical at `7bb0fe61` (the carrier) and at the tip; exit 0; stderr empty | `5785c5b2` / tree `c28ccfdf` at all three | yes. The tool last changed at `c484f6d` (round 24), the fixtures at `ec840f9d` itself; the file landed later in `7bb0fe61` |
| `routed-r24-before.txt` | `revision` 28b79d3d, `tool_revision` e54b644b, command, `exit: 1`. No `tool_blob` line | byte-equal (tool `e54b644b` run on `--rev 28b79d3d`, exit 1) | `a08043fe` at e54b644b and at the carrier `9b1a2f12`; **`ddc7a43d` at the tip** | **no.** The tool changed afterwards at `e06d4a02` |
| `routed-r24-after.txt` | `revision`/`tool_revision` e54b644b, command, `exit: 0`. No `tool_blob` line | byte-equal (tool `e54b644b` run on `--rev e54b644b`, exit 0) | same as above: **differs at the tip** | **no** (same reason) |
| `routed-r24-before-a5.txt` | `revision` 28b79d3d, `tool_revision` e06d4a02, command, `exit: 1` | byte-equal (tool `e06d4a02` run on `--rev 28b79d3d`, exit 1) | `ddc7a43d` at the named rev, the carrier `26c84859` and the tip | yes |
| `routed-r24-after-a5.txt` | `revision`/`tool_revision` e06d4a02, command, `exit: 0` | byte-equal (tool `e06d4a02` run on `--rev e06d4a02`, exit 0). At the tip `07a31ae8` it still prints 4 of 4 held, mismatches 0, hygiene held, exit 0 | `ddc7a43d` at all three | yes |
| `wave1-bind.json` | no header. The body carries `rev` 0099a391 | byte-equal (`tools/mori-dispatch-ledger.py bind --rev 0099a391 --dispatch .ufo/waves/round-25/wave1-run.json`, exit 0) | `b86525c6` at the named rev and the tip (unchanged since round 18) | yes |
| `wave2-bind.json` | no header. The body carries `rev` e5e1b7bc | byte-equal (same command with `wave2-run.json` at `e5e1b7bc`, exit 0) | `b86525c6` | yes |

In all four routed replays, the `repo` path in the JSON was rewritten from my clone path to the lane path before
comparing; nothing else in the bytes was changed.

**Strict M1 check.** The commits that landed evidence files edited no tool:

| Commit | Files changed |
|---|---|
| `7bb0fe61` | evidence file only |
| `9b1a2f12` | `contract.md` and two evidence files |
| `26c84859` | evidence files only |
| `129832e3` | ledger, registry and response files |
| `07a31ae8` | ledger, registry and response files |

Each measured tool's last change sits in its own earlier commit: `c484f6d` for the pressure tool, `e06d4a02` for
`routed-r24`, `9db5168` for the dispatch ledger.

## Findings

### F1 — high — C2 has no committed selftest or live-run evidence; the cited run predates the final tool change

- **Counterexample.** `.ufo/waves/round-25/evidence/` at the tip holds no `runway-selftest.txt` and no live-run
  file.
  - Amendment A1 binds both after-values to committed evidence: "`routed-r24-after.txt` for C1 and
    `runway-selftest.txt` for C2, written after the last change to the measured tool"
    (`.ufo/waves/round-25/contract.md:126-129`).
  - The C2 sourced clause says "A live run against this host is committed as evidence"
    (`contract.md:92`).
  - `git log --all -- .ufo/waves/round-25/evidence/runway-live-run.json` is empty.
- **Where the landed text points instead.** `corpus/knowledge/harness-job-capacity-r25.md:2` and `:178-179`
  cite `.ufo/waves/round-25/w1/BuildJobRunwayTool.md` §2 for the live run; `corpus/lessons/round-25.md:12` cites
  an unnamed "live run". The seat report's runs carry no lane revision header:
  - §1 and §2 (`BuildJobRunwayTool.md:72-107`) ran at sandbox `9cb0dc3c`. That is tool blob `7071ced9` = lane
    `09f55b62`.
  - The A2 rerun (`BuildJobRunwayTool.md:296-341`) ran at sandbox `2b9223f5`. That is blob `42a3f568` = lane
    `9a3d511`.
  - The shipping tool is blob `239dd8eb` (`fbecc59`, "runway selftest fails on zero cases…"; 6 lines added,
    1 removed). The final tool change came after every run the round cites, which is exactly the class QUALITY
    76 names.
- **Mitigation, measured.** In a clean extract at each of `09f55b62`, `9a3d511`, `fbecc59` and `07a31ae8`,
  `python3 -I -B tools/mori-job-runway.py --selftest` prints `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` with exit 0.
  The cases blob is `48df844a` throughout. The live run prints byte-identical JSON at all four revisions:
  configured set 200, clamp found 100 with 1 site, default found 100, effective 100, `RUNWAY_CLAMPED`, exit 1,
  binary sha256 `85d9daf3…`. The C2 numbers are true; the evidence obligation is unmet.
- **Impacted axes.** C2 coverage (its after-value has no committed evidence); calibration (the knowledge entry
  and lesson rest on a tally).
- **Smallest fix.**
  1. Commit `evidence/runway-selftest.txt` with the header lines `revision: <tip 40 hex>`,
     `command: python3 -I -B tools/mori-job-runway.py --selftest`, `tool_blob: 239dd8eb…`,
     `fixtures_tree: a8ed53b3…` and `exit: 0`, then the full stdout.
  2. Commit a live-run file in the same form (exit 1, full JSON). Also record the sha256 of the config read,
     since the config is not in the repo.
  3. Repoint `harness-job-capacity-r25.md:2,178-179` and `lessons/round-25.md:12` at the committed file.

### F2 — medium — false provenance: a committed seat report calls an uncommitted, now-deleted file "committed"

- **Counterexample.** `.ufo/waves/round-25/w1/SkillErrorPattern.md` names
  `.ufo/waves/round-25/evidence/runway-live-run.json` (and `.meta`) as committed in three places:
  - `:47`: "The lane's own committed live run agrees"
  - `:206`: the F11 evidence column
  - `:310`: "committed live-run evidence"
- **Evidence.** The file is in no commit on any ref. `.ufo/waves/round-25/w1/ReviewFrozenCases.md:139` recorded
  it as present in the working tree but not in HEAD. It is now absent from the working tree too: the `evidence/`
  listing at 11:40Z shows only the seven files above. It cannot be recovered from jj either:
  - none of the 60 most recent `snapshot working copy` operations holds it
    (`jj --ignore-working-copy --at-op <op> file list -r @`);
  - `git check-ignore` matches no rule for the path;
  - the lane tracks paths explicitly, so an untracked file is never snapshotted.

  The evidence is lost, and a committed record asserts it exists. No landed lane surface repeats the claim: `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`,
  `corpus/README.md`, the knowledge entry and the lesson have no `runway-live` match.
- **Impacted axes.** Calibration (a lane record contradicts committed bytes; QUALITY 77's sweep applies).
- **Smallest fix.** Land the F1 live-run file at exactly `evidence/runway-live-run.json`, which makes the three
  lines true. Otherwise add a correction row in the round-25 lesson naming `SkillErrorPattern.md:47,206,310` as
  pointing at a file that was never committed.

### F3 — medium-low — the A1-era routed pair was written before the final tool change and is unmarked at the tip

- **Counterexample.** `routed-r24-before.txt` and `routed-r24-after.txt` were measured with tool blob
  `a08043fe` (`e54b644b`). The tool changed afterwards at `e06d4a02` (D5 added; 167 lines added, 4 removed;
  blob `ddc7a43d`). QUALITY 76 requires the tool blob to be "identical at the named revision and at the revision
  that carries the file". That holds at the landing commit `9b1a2f12`, but not at the tip, which still carries
  both files.
- **What the shipping tool prints instead.** Run at the file's own revision (`--rev e54b644b`), the shipping tool
  prints `items 4, held 3, mismatches 1`, D5 red (`axis_score_mismatch: coverage 5!=6`, `operability 6!=7`,
  `depth 4!=5`), exit 1. The file says `items 3, held 3, mismatches 0`, exit 0.
- **Why it is not worse.** Each file's `tool_revision:` header names the tool it ran, and the bytes are exact for
  that tool, so this is not the strict M1 defect. The only "history" label is in the contract
  (`contract.md:196`), not in the files. A reader of `evidence/` alone sees a green 3-of-3 that the shipping tool
  turns red at the same revision.
- **Impacted axes.** Calibration (premature saturation risk if the A1 file is read as the after-value).
- **Smallest fix.** Add a header line to both files, for example
  `superseded_by: routed-r24-*-a5.txt (tool e06d4a02; this file measured with tool e54b644b)`, or move them under
  `evidence/history/`. Either way, keep the current bytes as the record of the A1 measurement.

### F4 — low — the routed headers omit two lines QUALITY 76 names, and the command is not verbatim

- **The gap.** QUALITY 76 lists "the tool blob and fixture tree" in the header. All four routed files carry
  `tool_revision:` instead of `tool_blob:`. A full commit does determine the blob, and `routed-r24` has no
  fixture directory. Their `command:` line reads `--repo <lane>`, a placeholder rather than the command run; the
  body's `repo` field records the actual path.
- **Smallest fix.** Add `tool_blob:` (`a08043fe…` or `ddc7a43d…`) and write the literal command, or state in
  QUALITY 76 that `tool_revision` satisfies the blob clause for tools without fixtures.

### F5 — low, outside QUALITY 76's letter — the bind records carry no header

- **The gap.** `wave1-bind.json` and `wave2-bind.json` are raw tool output, with no revision, command or exit
  header. They are bind records, not self-test evidence, so QUALITY 76's scope ("A self-test evidence file") does
  not literally reach them.
- **Measured.** Both bodies are byte-equal to a fresh `bind` run at their embedded `rev`, from an unchanged
  ledger tool, exit 0. Both dispatch files are unchanged from their bind revision to the tip.
- **Fix, only if the lane extends QUALITY 76 to every file under `evidence/`.** A sibling `.meta` or a header
  convention; no change is needed otherwise.

## Not run (not passes)

- `tools/mori-routed-r24.py --rerun`: not exercised. I replayed the pressure selftest directly instead.
- The lesson's round-18-to-24 stale-file census (`lessons/round-25.md:31-32`): not re-derived.
- Re-measurement at the final landed tip: the C1 after-value file names `e06d4a02`. Commits after `07a31ae8`
  that touch any file D1, D2, D3 or D5 reads (the evidence file, `system-pressure-r24.md`, `round-24.md`,
  `SCORECARD.md`) or `.gitignore` would need a fresh run.

# ReceiptInputs — L1 measurement revision and frozen-input provenance (round-17 wave2)

Seat: `MoriR17.ReceiptInputs-4` (scout). Read-only attack on the three settled claims' measurement
revision and input provenance. I did not attack classification semantics, census logic, detector
logic, or admission. No files written outside this report; no VCS mutation; no tool installs
(no channel used). Counting commands only: re-ran the committed `jq` counters over committed
receipts, plus hashes/`git show`/`git log`. No live probes, no gate/selftest runs.

Legend: **[OBS]** observed in committed bytes or git metadata; **[INF]** inference not directly observed.

## Verdict

No moved input. Every pinned input that has a run-time digest record matches its pin, and every
pinned file is byte-identical at the measured commit, the delivery tip, and today's worktree.
The branch-tip revision claim is independently corroborated by reflog: `refs/heads/master` (and the
diagnostic detached `HEAD`) was `273aa74…` for the whole measurement window and moved only at
`16:37:09`, after `PINNED_INPUTS.observed_at`.

Three bounded provenance defects remain, all in C3: its receipts carry no digest of the probe tool
or of the planted witness, its sandbox is gone, and its replay recipe is untracked. Those do not
change the C3 count (0→1 candidate is readable from retained stdout), but they mean "byte-exact
planted content" is not receipt-bound. Details F1–F3.

## Revision timeline (all times -03, 2026-10-20)

| Time | Event | Evidence |
|---|---|---|
| 10:20:41 | entering tip `24526ea` | `git reflog refs/heads/master` |
| 15:26:13 / 16:31:56 | measured commit `273aa74` author/committer | `git log -3 --format=%cI %aI` |
| 16:31:56 → 16:37:09 | `refs/heads/master` = `273aa74`; `HEAD` reflog same | `git reflog` for both refs |
| 16:32:40–16:32:59 | C1/C2 gate receipts | `evidence/c{1,2}-{before,after}.json:3-4` |
| 16:34:52 | C3 receipts | `evidence/c3-{before,after}.json:3-4` |
| 16:35:15 | count receipts | `evidence/count-c{1,2,3}.json:3-4` |
| 16:35:35 | `PINNED_INPUTS.observed_at` | `PINNED_INPUTS.json:5` |
| 16:37:09 | delivery commit `5c1dfb8` (evidence + pins only) | reflog; `git diff --name-status 273aa74..5c1dfb8` |

[OBS] `git diff --name-only 273aa74 5c1dfb8 -- tools/` is empty; the only pinned-path change in the
delivery commit is the addition of un-pinned `frozen/c3-expected.json`. All nine pinned files are
byte-identical at both commits (`git show <ref>:<path> | sha256sum`, 18/18 matches).

`PINNED_INPUTS.json:3` names `273aa74`; `observed_at` (16:35:35) is inside the window when both
`HEAD` and `refs/heads/master` were `273aa74`, and 15 s after the last count receipt. [OBS]

## Branch tip vs diagnostic HEAD

- `.git/HEAD` is a raw SHA (detached), currently `5c1dfb8` = `refs/heads/master` [OBS].
- The seat gate records both explicitly and documents the semantics: `branch_tip` =
  `rev-parse refs/heads/<branch>`, `head` diagnostic only, receipts measured against `branch_tip`
  (`tools/mori-round17-seat-regressions.py:124-127`, `:1565-1572`) [OBS].
- `evidence/seat-after/run-manifest.json` `git` object: `branch=master`,
  `branch_source=origin-head`, `branch_tip=273aa74…`, `head=273aa74…`,
  `receipt_ref=refs/heads/master`. Before manifest identical in kind [OBS].
- All nine receipts name `branch_ref=refs/heads/master` and `branch_tip_after=273aa74…`
  (e.g. `c1-after.json:16-18`, `c3-after.json:18`) [OBS].

So at measurement time branch and HEAD coincided; no off-branch HEAD was measured. The claim that
HEAD is only a diagnostic pointer is consistent with the detached `.git/HEAD` observed now. What is
*not* retained is the receipt wrapper's code, so whether `branch_tip_after` was queried as
`refs/heads/master` or as `HEAD` cannot be proven from code; the values coincide and reflog shows no
divergence in the window [INF, residual R2].

## Digest match tally

1. **Pinned files:** 9 declared. 9/9 match at measured commit `273aa74`, 9/9 at tip `5c1dfb8`,
   9/9 in worktree; 18/18 across both commits (`PINNED_INPUTS.json:7-15`) [OBS].
2. **Run-time recorded digests that equal pins:** 9/9 slots — seat-after tool `5819…`; expected.json
   `b684…` (before and after); jj census `f1f8…` (before) and `12e8…` (after); seat gate `21285…`
   (before and after); jj gate `1067…` (before and after). These were recorded by the gates at run
   time, not re-hashed later (`seat-*/run-manifest.json` `.tool.sha256`, `.fixtures.expected.sha256`,
   `.gate_sha256`; `jj-*/run-manifest.json` `.census.sha256`, `.gate.sha256`; jj gate hashes the
   census itself, `tools/mori-round17-jj-regressions.py:1177`) [OBS].
3. **Fixture pins:** `expected.json.pins` has exactly 81 entries; 81/81 match the committed blobs at
   `273aa74`. Recomputed `sha256(canonical(pins))` = `76e2f25e…`, exactly the manifest's
   `fixtures.pins.declared_sha256`; `declared=81`, `verified=true`, empty missing/extra/mismatched
   (`seat-after/run-manifest.json` `.fixtures.pins`) [OBS].
4. **Runtime fixture inputs:** 82 entries (79 regular files + 3 symlinks, including expected.json).
   79/79 regular-file digests equal committed blobs; the 3 symlink entries are pinned as link-text
   digests (the committed symlink blobs are those same target strings; not a mismatch, a different
   encoding). `inputs_before == inputs_after`, `inputs_changed=[]`, `pack_changed=0` for all 54 cases
   [OBS].
5. **Frozen census:** `frozen/mori-census.sh` `f1f8…`, 223560 B = `git show 24526ea:tools/mori-census.sh`
   exactly (1/1) — the "entering census" input is genuine, not a re-typed copy. Delivered census
   `12e8…`, 242050 B = `tools/mori-census.sh` at `273aa74` (1/1) [OBS].
6. **Frozen witness:** `frozen/MoriR16.Lesson` `15f9f8…`, 847 B = the fleet archive
   `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/MoriR16.Lesson` (hashed today, 1/1);
   the same bytes/digest are embedded in `tools/mori-misroot-sweep.py:346-352`, with a hard digest
   check at `:386` [OBS].
7. **Preservation:** 7/7 preserved files match at both `24526ea` and `273aa74`
   (`evidence/preservation.json`) [OBS].
8. **Receipt integrity:** 9/9 receipt `stdout_sha256` values reproduce over the receipt's own
   `stdout`; the three counters reproduce exactly: C1 `[54,0]`, C2 `[21,0]`, C3 `[1,0]` [OBS].
9. **Claim values:** `PINNED_INPUTS.json:21-34` before/after 54/0, 21/0, 1/0 agree with the count
   receipts and with the manifests (`capability_absent 54→0`; `failed_assertions 21→0` of
   124→134; missed path count 1→0) [OBS].

## Defects / gaps (bounded, none invalidate the counts)

**F1 — C3 receipts do not digest the probe or the witness at run time. Severity: evidence gap.**
Unlike C1/C2 manifests, `evidence/c3-{before,after}.json` contain only
`label,started_at,ended_at,argv,cwd,branch_ref,measured_commit,branch_tip_after,rc,duration_s,stdout,
stderr,stdout_sha256,stderr_sha256`. The probe payload carries `path`, `matched_in`, `read`,
`read_bytes=847`, `size_bytes=847` — no SHA-256 (`c3-after.json:21`). `frozen/c3-expected.json`
pins the witness hash, but it is not read by the probe and was added in the delivery commit
(`git log --diff-filter=A` → `5c1dfb8`, 16:37:09), i.e. after the 16:34:52 run. The sandbox
`.ufo/worktrees/round-17/MainChecks/c3-fleet` no longer exists. Net: the C3 0→1 candidate count is
receipt-readable, but "the planted file contained the byte-exact 847-byte known artifact" rests on
(a) the frozen file's digest equaling the fleet archive, (b) the recorded size, (c) the untracked
recipe and the tool's embedded bytes — not on a run-time digest [OBS for all premises; the
byte-exactness of the sandbox at run time is INF].

**F2 — C3's "or content" leg is not exercised by the measurement. Severity: disclosed scope limit.**
The candidate resolved `matched_in:["path"]` (`c3-after.json:21`); the file name alone names
lane+round, and a filename-only detector would emit the same 0→1 result. The measurement therefore
supports "no-pathspec scan finds by filename where the legacy pathspec sees nothing", not
"filename-or-content" discrimination. `corpus/lessons/round-17.md:137-139` already says "by path
alone", so this is disclosed, not hidden [OBS].

**F3 — C3 replay/expectation artifacts are retrospective or untracked. Severity: record hygiene.**
`frozen/c3-expected.json` (expected flags + witness hash) entered git only in the post-measurement
delivery commit. `c3-capture-recipe.json` is untracked (`git status --porcelain` →
`?? .ufo/waves/round-17/c3-capture-recipe.json`; `git check-ignore` rc1, so not ignored; mtime
16:47, after the 16:37 commit). The recipe's `expected.missed_known_artifacts=[1,0]` is thus a
post-hoc record, not a pre-registered oracle; the pre-registered expectation is only
`contract.md:21-27`. [OBS for tracking/mtimes; retrospective role INF]

**F4 — Receipt producer is not retained. Severity: reproducibility gap.**
No tracked file emits the receipt schema `label/started_at/ended_at/argv/cwd/branch_ref/
measured_commit/branch_tip_after/rc/duration_s/stdout_sha256` (`grep -rln '"duration_s"'` finds
nothing outside `evidence/`). The fields are L1's wrapper output; only the receipts themselves are
retained. Corroboration is independent (reflog, gate manifests, gate `capture_revision()` code), so
this is a gap in replay, not a contradiction [OBS/R2].

**F5 — C1 claim unit label drift. Severity: wording.**
`PINNED_INPUTS.json:21` unit is "unmet synthetic capability assertions"; the counted quantity is
cases with `summary.capability_absent` (54), not assertion-level failures. C2's unit really is
assertions (21 failed of 124/134); C3's is missed artifacts. Numbers are correct; the noun is
imprecise [OBS].

**F6 — `fixture_files: 81` semantics. Severity: labeling only.**
Tracked fixture entries = 82 (incl. `expected.json`); regular files in the worktree = 79 (3 tracked
symlinks are not `-type f`). 81 is exactly `expected.json.pins` (excludes `expected.json`, includes
symlinks pinned by link text) and the gate's `declared=81` with `declared_sha256` reproduced. The pin
is correct once read as "pin count"; a reader assuming regular files would compute 79 [OBS].

**F7 — C2 jj manifests lack branch/HEAD metadata; receipts and seat manifests carry it.
Severity: asymmetry.** `jj-*/run-manifest.json` records `census`, `tools`, `environment`,
`scratch_run`, `gate`, `totals`, `cases` — no `git` object. The branch-anchored provenance for C2 is
therefore in `c2-*.json` (`branch_ref`, `branch_tip_after`) and in the pinned census itself; the
seat manifests are the only gate-level records that store both `branch_tip` and `head` explicitly
[OBS].

**F8 — C2 scratch path is literally inside the lane, contrary to `contract.md:100`, but reconciled
by the pinned gate's own doctrine. Severity: contract wording.** Receipts/sandboxes:
`c2-*.json` `--scratch .../mori-shokunin/.ufo/worktrees/round-17/MainChecks/jj-{before,after}`;
`jj-*/run-manifest.json` `.scratch_run` same root. `tools/mori-round17-jj-regressions.py:28-38`
(pinned `1067…`) states the scratch may live under a jj-colocated lane and enforces per-call
`jj -R <sandbox>` / `git -C <sandbox>` with `GIT_CEILING_DIRECTORIES`, scrubbed git env, HOME/
XDG_CONFIG_HOME/JJ_CONFIG/GIT_CONFIG_GLOBAL inside the case, and no remote. Thus the isolation claim
is supported; the contract sentence "never in the lane or fleet" is stronger than what was executed
[OBS].

**F9 — Sandboxes removed after capture; `fleet_root`/`scratch_run` point to absent paths.
Severity: replay limit.** `.ufo/worktrees/round-17/MainChecks/` is absent now; only case `.out`
files and manifests remain. C1 has no sandbox by design (per-case copies); C2 is rebuildable from
the pinned gate + census; C3 depends on the untracked recipe (F3). This matches the lesson's
"copied session sandboxes were removed after capture" [OBS].

## Moved-input conclusion

None of the nine pinned inputs moved between measurement and delivery, and no run-time digest
disagrees with any pin. The only measurement-adjacent files added after `273aa74` are evidence
receipts, `PINNED_INPUTS.json`, `frozen/c3-expected.json`, and report/log files; none is a C1/C2
input, and `frozen/c3-expected.json` is not read by the probe. The entering census used for the
C2 "before" side is byte-identical to `git show 24526ea:tools/mori-census.sh`. The C3 witness file
is byte-identical to the fleet archive that the tool embeds and digest-checks.

## Remaining unknowns

- R1: Whether C3's sandbox actually held the frozen bytes at run time. No run-time digest; size,
  recipe, frozen=fleet-archive and the tool's embedded digest are consistent but not dispositive.
- R2: Whether the receipt wrapper resolved `branch_tip_after` from `refs/heads/master` or from
  `HEAD`. Values coincide and reflog shows no divergence in the window; wrapper code not retained.
- R3: The untracked recipe's author and whether it existed before 16:47 in another form (mtime only).
- R4: Interpreter/tool versions for the receipt wrapper (`python3`, `jq`) are not recorded; only the
  jj gate records git/jj/bash/jq paths and versions in its manifest.
- R5: C1 live observation's sessions directory is not pinned; it is not an admission input (fixture
  gate is), so this does not affect the 54→0 claim.

## Attacked scope (explicit non-claims)

I attacked measurement revision and frozen-input provenance only. I did not re-verify C1
classification correctness, C2 census semantics, C3 detector correctness, or any admission
decision; absence of a defect here is not a blanket pass on those. Verified checks: 18/18
pinned-file digests across two commits, 9/9 run-time pin slots, 81/81 fixture pins, 82/82 runtime
fixture entries, 7/7 preservation entries, 9/9 receipt stdout hashes, three counters reproduced,
reflog window and both refs.

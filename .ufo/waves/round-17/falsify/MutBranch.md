# MutBranch — C2 row-9 HEAD-anchor mutation probe

Seat: `MoriR17.MutBranch-4`. Date: 2026-10-20. Scope: one mutation of the isolated copy at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/tools/mori-census.sh`, using the unchanged committed jj-regression gate. This is fresh falsification evidence for L1, not claim admission, integration, promotion, or independent closure.

## Axes and result

- **C2 operability:** challenge the branch-anchored row-9 history scan with a plausible regression to bare `HEAD`.
- **Detector discrimination:** require a clean pristine baseline, the expected semantic failures after mutation, and clean recovery with exactly the same detector.
- **Isolation and reversibility:** change only one behavior-bearing line in the assigned copy; retain outputs/sandboxes inside that copy; restore exact bytes.

**Mutation verdict: KILLED.** Pristine `rc0`, 12/12 matching cases, 0/134 failed assertions; mutant `rc1`, 9 matching/3 mismatching cases, 9/134 failed assertions; restored `rc0`, 12/12 matching cases, 0/134 failed assertions. No setup failures or absent capabilities in any run. All nine controls retained their expected status under the mutant. The isolated census was restored to its pinned SHA-256 and byte-compares equal to the production census.

This kills this specific row-9 HEAD-anchor defect; it is not a blanket pass for C2 or either other claim.

## Contract and pinned inputs

Read the contract including Amendment A1, pinned inputs, round lesson, and binding wave context before mutation. Relevant anchors:

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/contract.md:88-102`: row-6/row-9 branch anchors and real git/jj gate.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/contract.md:122`: A1 warn severity, non-shokunin author-email restriction, unresolved-branch HEAD fallback.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/PINNED_INPUTS.json:3-10`: measured revision `273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7`, census/gate byte pins. Revision is cited from that record; no VCS query or mutation was used to establish a different checkout revision.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-17.md:126-133`: finite assertion units and sandbox qualifications.

Initial `/usr/bin/sha256sum` over both isolated and production census/gate paths returned rc0 and matched both pinned file hashes. No production detector or gate bytes were edited.

## Mutant and expected detector

Only `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/tools/mori-census.sh:2309` changed:

```diff
-  [ -n "$GL_BRANCH" ] && rev="refs/heads/$GL_BRANCH"
+  [ -n "$GL_BRANCH" ] && rev="HEAD"
```

The preceding default remains `local rev="HEAD"`. Therefore a resolved branch no longer overrides the row-9 revision. This changes the shared revision used by its `rev-parse` at line2312, authorship log at line2326, and separate committer/author log at line2362. It does not mutate the branch resolver, row-6 report closure, the ancestry diagnostic, gate expectations, or any caller.

Detector: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/tools/mori-round17-jj-regressions.py`, unchanged SHA-256 `1067e4ae97ba8a60c55f1cc65bfaf042a6c6384ae1064a644919cdfd409ee0e3` in all three manifests. Scenario expectations are at lines547-568 and617-630; evaluation checks lane state/basis as well as exit/verdict and findings at lines764-802. Expected mutant failures: crediting detached-ahead work, missing work visible only at a branch ahead of detached HEAD, and crediting a jj commit without moving its bookmark. Remaining controls must continue matching.

## Executed commands, environment, and raw output

All three invocations were synchronous subprocesses with a 600-second outer bound, stdin closed, and captured stdout/stderr; the gate bounds each census subprocess to 240 seconds. No background job was started. Working directory for all invocations:

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch`

The exact explicit driver environment is retained in each command receipt. It contained only:

```text
PATH=/home/vgpnk/.local/bin:/usr/local/bin:/usr/bin:/bin
LANG=C.UTF-8
LC_ALL=C.UTF-8
TZ=UTC
HOME=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/driver-home
XDG_CONFIG_HOME=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/driver-home/.config
TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch
MORI_JJ_BIN=/home/vgpnk/.local/bin/jj
PYTHONDONTWRITEBYTECODE=1
```

### Pristine — 19:48:12.583389Z–19:48:14.730973Z

Actual argv:

```sh
/usr/bin/python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/tools/mori-round17-jj-regressions.py --census /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/tools/mori-census.sh --output /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/evidence/pristine --scratch /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/sandboxes/pristine
```

rc0; stderr empty; exact stdout:

```text
mori-round17-jj-regressions: cases=12 match=12 mismatch=0 capability_absent=0 setup_failed=0 assertions=134 failed=0
manifest: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/evidence/pristine/run-manifest.json
```

Command/streams receipt: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/evidence/pristine-command.json`.

### Mutant — 19:48:30.891186Z–19:48:32.693369Z

Actual argv:

```sh
/usr/bin/python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/tools/mori-round17-jj-regressions.py --census /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/tools/mori-census.sh --output /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/evidence/mutant --scratch /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/sandboxes/mutant
```

rc1; stderr empty; exact stdout:

```text
mori-round17-jj-regressions: cases=12 match=9 mismatch=3 capability_absent=0 setup_failed=0 assertions=134 failed=9
manifest: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/evidence/mutant/run-manifest.json
```

Command/streams receipt: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/evidence/mutant-command.json`.

### Restored — 19:48:46.300743Z–19:48:48.267332Z

Before this run, the one changed line was restored verbatim. Actual argv:

```sh
/usr/bin/python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/tools/mori-round17-jj-regressions.py --census /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/tools/mori-census.sh --output /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/evidence/restored --scratch /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/sandboxes/restored
```

rc0; stderr empty; exact stdout:

```text
mori-round17-jj-regressions: cases=12 match=12 mismatch=0 capability_absent=0 setup_failed=0 assertions=134 failed=0
manifest: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/evidence/restored/run-manifest.json
```

Command/streams receipt: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/evidence/restored-command.json`.

## Actual failures and retained controls

The following expected states held in pristine and restored runs. These three and only these three cases mismatched under the mutant:

| Case | Expected and pristine/restored observation | Mutant observation | Failed assertions |
|---|---|---|---|
| `git-detached-commit` | `silent`, `row-D`, DRIFT, census rc1 | `progressing`, `row-A`, DRIFT, census rc1 | `lane_state`, `lane_basis` (2) |
| `git-detached-behind` | `progressing`, `row-A`, CLEAN, census rc0 | `silent`, `row-D`, DRIFT, census rc1 | `census_exit`, `verdict_roll`, `lane_state`, `lane_basis` (4) |
| `jj-commit-no-bookmark` | `silent`, `row-D`, DRIFT, census rc1; no author-mismatch finding | `progressing-weak`, `row-C`, DRIFT, census rc1; spurious `LANE_AUTHOR_MISMATCH` | `lane_state`, `lane_basis`, `finding:LANE_AUTHOR_MISMATCH:absent` (3) |

Raw mutated witness anchors:

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/evidence/mutant/cases/git-detached-commit.out:8`: `SURFACE lane.alpha: progressing ... basis=row-A subject_commits=yes`; line12 retains `HEAD_BRANCH_MISMATCH severity=warn`; line14 remains `MORI_CENSUS: DRIFT`.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/evidence/mutant/cases/git-detached-behind.out:8`: `SURFACE lane.alpha: silent ... basis=row-D`; line12 emits `LANE_SILENT severity=warn`; line14 is DRIFT instead of expected CLEAN.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/evidence/mutant/cases/jj-commit-no-bookmark.out:8`: `SURFACE lane.alpha: progressing-weak ... basis=row-C other_authored_commits=1`; line12 retains `HEAD_BRANCH_MISMATCH`; line13 spuriously emits `LANE_AUTHOR_MISMATCH severity=warn`; line15 remains DRIFT.

**Discriminating result:** in the detached-ahead Git and jj cases the overall census rc/verdict remained rc1/DRIFT because the ancestry warning still fired. The gate nevertheless killed the mutant through wrong lane-state/basis assertions (and the jj author-finding negative assertion), rather than relying only on an overall exit code.

All nine remaining cases were `match` with zero failed assertions in each of pristine, mutant, and restored runs. Their mutant observations, unchanged in meaning from both clean runs:

| Control | State / basis | Census rc / verdict |
|---|---|---|
| `git-plain-progress` | progressing / row-A | 0 / CLEAN |
| `git-detached-at-tip` | progressing / row-A | 0 / CLEAN |
| `git-report-on-branch` | not-open / row-6 | 0 / CLEAN |
| `git-report-off-branch` | silent / row-D | 1 / DRIFT |
| `git-foreign-author` | progressing-weak / row-C | 0 / CLEAN |
| `jj-helper-commit` | progressing / row-A | 0 / CLEAN |
| `jj-ambient-author` | progressing-weak / row-C | 1 / DRIFT |
| `jj-sibling-author` | progressing-weak / row-C | 0 / CLEAN |
| `git-fallback-head` | progressing / row-A | 0 / CLEAN |

The row-6 off-branch report control correctly remained matching: this probe mutated row9, not report closure. The ambient-author positive control and sibling-author negative control retained their amended status.

These counts and states were read from the three retained `run-manifest.json` files, not from rerun live probes. Every case's `refs_unchanged` assertion was true in all three manifests (12 per run); all four `jj_config_redirected` assertions were also true per run. Full per-case census outputs remain under each stage's `cases` directory.

## Hash chain and exact restoration

Actual `/usr/bin/sha256sum` outputs, rc0:

| Bytes | SHA-256 |
|---|---|
| Assigned census before mutation | `12e8e2d960c2d4d1ea780787c75c0125ec51adf434c93eb169ab0a4066236d85` |
| Assigned census mutant | `51995b1dc85b87a21f926561d55f1374c72a61e094ee745e17c47e095b6316e9` |
| Assigned census after restoration | `12e8e2d960c2d4d1ea780787c75c0125ec51adf434c93eb169ab0a4066236d85` |
| Production census before and after probe | `12e8e2d960c2d4d1ea780787c75c0125ec51adf434c93eb169ab0a4066236d85` |
| Assigned and production gate before/after | `1067e4ae97ba8a60c55f1cc65bfaf042a6c6384ae1064a644919cdfd409ee0e3` |

The per-stage manifests independently recorded the same pristine→mutant→restored census hashes. Restoration returned the changed line to `rev="refs/heads/$GL_BRANCH"`. After the restored detector finished, the following byte comparison completed rc0 with no output:

```sh
/usr/bin/cmp /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/tools/mori-census.sh /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh
```

Retained receipt hashes (full absolute parent is `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/evidence`; all generated files are only there):

| Receipt | SHA-256 |
|---|---|
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/evidence/pristine/run-manifest.json` | `70285b0c997f6966640d4255bd147ac6d2f73c8aad45f25e6b16b4b67e6e29eb` |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/evidence/mutant/run-manifest.json` | `5375856e0f7d1317e05f36b6a824ecdd7dc7d336382d98f1b6e3845ccef75bf3` |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/evidence/restored/run-manifest.json` | `ae8b30ff771644324bdad4cc6bce9ca05ae20cda7f9699a0c93bce5b86ade1dd` |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/evidence/pristine-command.json` | `92de8c37ac1a63d90f0624ca4a0e5cfdffff2226d71c7376b6e041c3c3ef6ebf` |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/evidence/mutant-command.json` | `16204d6e2782a56b32d0651721c376017f1e461279fb453bb09cfdfaba57fd18` |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/.scratch/evidence/restored-command.json` | `feefe9b73e30b91420b756b7883a996592bc4a9ab026b481cd8fecee277875df` |

## Boundary and tooling record

- No VCS mutation was invoked by this seat. Real git/jj writes occurred only through the committed gate inside its created sandboxes under the assigned `.scratch/sandboxes` directories. The gate's explicit repo paths and isolated HOME/XDG/JJ/Git configuration are at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MutBranch/tools/mori-round17-jj-regressions.py:180-198,249-274,334-443`.
- L1 explicitly authorized the gate's metadata-only `jj --version` lookup as an exception to the sandbox-command wording before execution. All repository operations still used gate sandbox paths; no direct jj command was run by the seat.
- No live journal query, host service action, selftest, build, lint, package transaction, or unrelated detector run was executed. Journal/tmux/process/disk command names in census evidence refer to gate stubs, not live probes.
- No production checkout, sibling lane, fleet file, MANIFEST, or fleet state file was edited. Apart from this requested report, writes were confined to the assigned clone. No probe output or scratch was placed in `/tmp`.
- Installs/updates: **none**. Existing gate-reported tools were `git version 2.56.0` and `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5`; existing Python, Bash, jq, and timeout were used. Gate records the resolved jq path as `/home/vgpnk/.local/bin/jq`.
- The assigned clone, raw outputs, and gate-created sandboxes are retained; none were removed before L1 integration. The source is restored, not left mutated. C1/C3 and broader C2 completeness were not attacked by this probe.

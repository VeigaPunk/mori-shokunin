# BuildRoutedCheck — claim C1, `tools/mori-routed-check.py`

Date: 2026-10-22. Seat: MoriR24.BuildRoutedCheck, executor leaf. No subagent dispatch.
Lane: /home/vgpnk/Projects/shokunin/mori-shokunin. Sandbox clone: `/fast/scratch/hyaku/mori-r24-a2/wt-routed`.

## 0. Status

`tools/mori-routed-check.py` is implemented, committed in my sandbox clone, and measured.

- Clone: `/fast/scratch/hyaku/mori-r24-a2/wt-routed`, branch `r24-wt-routed`, based on
  `29c1bf45dde6af48fc9a07aef447bd7d7f822cc5`.
- Commit: `9682f761f838a28a02841172f35c8580d1a696ef`
  ("round-24: routed check honours A4 wave-value matching and verify findings").
  Previous commit in the same branch: `39fcdb114339b3e0a70ef94692b96f43d783c41d`.
- SHA256 of `tools/mori-routed-check.py` (worktree == committed blob):
  `64921a0c30aed1d9a2a7a03c377825add37ebecd7aded8fbfe8f30c02dafbd14`
- Blob OID at the commit: `3337232ba364d5d290e0cf7c93d1bcb816f75562`.
- Nothing was pushed; the clone's remote is unchanged and the lane repo's git index and
  jj state were not touched. This report is the only file I created in the lane.

## 1. What the tool does

`python3 -I tools/mori-routed-check.py --repo PATH --rev REV [--round N]`

- Python 3 standard library only. No third-party imports.
- Every predicate is a **git object read only**: `git ls-tree`, `git cat-file`, `git rev-parse`,
  `git log`, `git diff`. The working tree is never read.
- Clean git environment, mirroring `tools/mori-dispatch-ledger.py:74-82`:
  `PATH=os.defpath`, `LANG=C`, `LC_ALL=C`, `GIT_CONFIG_GLOBAL=/dev/null`,
  `GIT_CONFIG_NOSYSTEM=1`, `GIT_OPTIONAL_LOCKS=0`, plus `GIT_TERMINAL_PROMPT=0`.
  Every git call also passes `--no-optional-locks`.
- Base revision is fixed in the source: `c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130`
  (`BASE_REV`), the round-23 verifier spot-check tip.
- `--round N` (default 24) names the round whose dispatch ledgers R4 inspects.
- R4 calls `tools/mori-dispatch-ledger.py verify` as a **subprocess** on the **same REV's tool
  bytes**: the blob is read with `git cat-file blob REV:tools/mori-dispatch-ledger.py` and piped
  to `sys.executable -I -` with `verify --repo ... --rev REV --ledger ...`. The working-tree copy
  of the ledger tool is never used.
- Output: one JSON object on stdout, `schema: mori-routed-check-v1`, `items: 4`, `held: N`,
  and one row per routed item: `{"id": "R1".."R4", "held": bool, "reasons": [...], "detail": {...}}`.
- Exit codes: `0` when `held == 4`, `1` when any item fails, `2` when the repo, the revision or
  the base cannot be read.

## 2. Predicates, as amended

Contract C1 with amendments A1 (R2 scan scope) and A4 (R4 rewrite, R1-R3 regression guards).

**R1** — quota capability stays absent, and the historical case is never special-cased.
- Whole `.ufo/waves/round-23` tree OID at REV equals base (A4).
- `.ufo/waves/round-23/frozen` tree OID at REV equals base (original predicate, retained).
- `tools/mori-quota-surface.py` and `corpus/knowledge/quota-surface-r23.md` absent at REV.
- No path **added** since base under `tools/` or `corpus/knowledge/` contains `quota`
  (`git diff --diff-filter=A --name-only base REV -- tools/ corpus/knowledge/`).
- No file under `tools/` contains the historical case name. The needle is assembled at run time
  as `"Case" + "Escaped" + "Space"`, so this source file does not contain the literal it searches
  for, and no file is excluded from the scan. Verified: the literal is absent from the committed
  blob (`b'CaseEscapedSpace' in blob` is `False`).

**R2** — retention state stays red and privacy is never cleared.
- Blobs of `tools/mori-retention-gate.py` and `tools/mori-retention-reconcile.py` equal base (A4).
- Blobs of `.ufo/waves/round-23/evidence/retention-floor-final.json` and
  `retention-floor-final-comparison.json` equal base (original predicate, retained).
- Added-line scan, A1 scope only: `git diff --unified=0 --no-renames --no-ext-diff --no-textconv
  base REV -- SCORECARD.md PROVINCE.md SKILL.md LOG.md README.md corpus/`. The added side only.
  A line trips R2 when it matches `privacy_clearance\s*["']?\s*[=:]\s*["']?true`, case-insensitive.
  `.ufo/**` and `tools/**` are **not** scanned: wave reports and tool sources quote the pattern
  rather than assert it. The scanned path set is exposed in the R2 row as
  `detail.scan_scope` and `detail.scanned_paths`.

**R3** — capture limitations preserved.
- Whole `.ufo/waves/round-23` tree OID at REV equals base (A4).
- Blobs of `harness-receipt-overwrite.json` and `tmpfs-source-provenance-erratum.json` equal base.
- `.ufo/waves/round-23/rejected` tree OID at REV equals base.

**R4** — future dispatches are bound before the call (A4).
- Every `.ufo/waves/round-N/*-attempts.json` and `*-ledger.json` at REV (at least one must exist)
  is verified with the REV's `tools/mori-dispatch-ledger.py verify`.
- For every row: the committer time of the commit that **last changed** the `dispatch_path` blob
  at or before REV is at or before the row's `at`. Implemented as
  `git log -1 --format=%ct REV -- <dispatch_path>` compared numerically against
  `datetime.fromisoformat(at).timestamp()`. The `at` side keeps microseconds; the git side is
  whole seconds. Never a string comparison.
- Every `.ufo/waves/round-N/wave*-spec.json` has a ledger whose last row is `started` or `partial`.
  Spec-to-ledger matching is by the ledger rows' `wave` value equal to the spec's `wave` field
  (per `ReviewC1Predicates.md` F1). A ledger whose rows carry no `wave` value at all falls back to
  the wave number in the file name, so a legacy ledger is not silently unpaired with its own spec.
- A dispatch-ledger `verify` exit of 2 (missing dispatch path, invalid path, unreadable ledger)
  is an **R4 red finding**, not a tool-level exit 2 (`ReviewC1Predicates.md` F2). The tool exits 2
  only when the repo, revision or base cannot be read. Verify's `finding_ids` are added to the R4
  reasons as `ledger_finding:<ID>`.

## 3. Measured outputs

All runs: `python3 -I tools/mori-routed-check.py --repo /home/vgpnk/Projects/shokunin/mori-shokunin ...`
against the lane repo, read-only. Lane `master` at measurement time:
`06a7686ed40f53a7455fe526dadf821757bea98a`.

### A. `--rev c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130 --round 23` — the real defect, R4 RED

Tool exit **1**. `held=3`, `items=4`, `status=failed`. R1, R2, R3 held; R4 red.

Full R4 reasons (as printed):

```
['attempt_ledger_not_clean',
 'ledger_finding:AT_INVALID',
 'ledger_finding:LEGACY_ROW_UNBOUND',
 'ledger_finding:STARTED_MISSING',
 'dispatch_path_missing' x8,
 'dispatch_committed_after_dispatch' x8]
```

**Yes — the wave1-ledger.json ordering failure is shown, not only the legacy shape failure.**
The eight `dispatch_committed_after_dispatch` reasons come from
`.ufo/waves/round-23/wave1-ledger.json`, whose verify is **clean** (`LEDGER_CLEAN`, exit 0) and
which therefore fails R4 on ordering alone:

```
--- .ufo/waves/round-23/wave1-ledger.json verify_exit 0 clean ['LEDGER_CLEAN']
    row 1 dispatch_committed_after_dispatch at= 2026-10-21T17:03:11.644975Z commit_epoch= 1792606259 at_epoch= 1792602191
    row 2 dispatch_committed_after_dispatch at= 2026-10-21T17:06:13.093456Z commit_epoch= 1792606259 at_epoch= 1792602373
    row 3 dispatch_committed_after_dispatch at= 2026-10-21T17:09:13.217738Z commit_epoch= 1792606259 at_epoch= 1792602553
    row 4 dispatch_committed_after_dispatch at= 2026-10-21T17:12:13.327620Z commit_epoch= 1792606259 at_epoch= 1792602733
    row 5 dispatch_committed_after_dispatch at= 2026-10-21T17:15:13.664133Z commit_epoch= 1792606259 at_epoch= 1792602913
    row 6 dispatch_committed_after_dispatch at= 2026-10-21T17:18:14.221726Z commit_epoch= 1792606259 at_epoch= 1792603094
    row 7 dispatch_committed_after_dispatch at= 2026-10-21T17:21:14.398094Z commit_epoch= 1792606259 at_epoch= 1792603274
    row 8 dispatch_committed_after_dispatch at= 2026-10-21T17:24:14.626546Z commit_epoch= 1792606259 at_epoch= 1792603454
```

`commit_epoch=1792606259` is commit `22772c1` (2026-10-21T18:10:59Z), the last change of
`.ufo/waves/round-23/wave1-run.json` at or before `c725aa37`. Every row's `at` is 46.7 to 67.8
minutes earlier. This is the defect A4 names, measured.

The other two reasons come from the legacy-shape file
`.ufo/waves/round-23/wave1-attempts.json` (verify exit 1, `AT_INVALID` / `LEGACY_ROW_UNBOUND` /
`STARTED_MISSING`; its rows have `utc` keys and no `at`, no `dispatch_path`, no
`payload_sha256`, hence the eight `dispatch_path_missing`). Independently,
`.ufo/waves/round-23/wave2-ledger.json` verifies clean and its single row is `bound_before_call`
(`commit_epoch=1792607409` <= `at_epoch=1792607444`), so the ordering check is not uniformly red.

Both round-23 specs resolve to a started ledger:
`wave1-spec.json` (wave `mori-r23-build`) -> `wave1-attempts.json`, `wave1-ledger.json`;
`wave2-spec.json` (wave `mori-r23-falsify`) -> `wave2-ledger.json`.

### B. `--rev c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130 --round 24`

Tool exit **1**. `held=3`, `items=4`, `status=failed`. R1, R2, R3 held; R4 red with
`reasons: ['no_round_ledger']` — there is no `.ufo/waves/round-24/` tree at `c725aa37`.

### C. `--rev master --round 24` — the tip

Tool exit **0**. `held=4`, `items=4`, `status=failed`→`held`. R1, R2, R3, R4 all held.

```
held=4 items=4 status=held rev=master round=24 base=c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130
  R1 held []
  R2 held []
  R3 held []
  R4 held []
```

R4 detail at the tip:

```
ledgers_found: ['.ufo/waves/round-24/wave1-attempts.json']
--- .ufo/waves/round-24/wave1-attempts.json verify_exit 0 clean ['LEDGER_CLEAN']
    row 1 bound_before_call at= 2026-10-22T05:14:13.926366-03:00
         dispatch_last_changed_epoch=1792656837  at_epoch=1792656853
SPEC .ufo/waves/round-24/wave1-spec.json wave= mori-r24-w1 started= True
     candidates= ['.ufo/waves/round-24/wave1-attempts.json']
```

The margin is 16 s: commit `06d4f4d` (epoch 1792656837) precedes the recorded call.

### D. `--rev 29c1bf45dde6af48fc9a07aef447bd7d7f822cc5 --round 24` (the revision named in my task)

Tool exit **1**. `held=3`, `items=4`, `status=failed`. R1, R2, R3 held; R4 red with
`reasons: ['no_round_ledger']` — `29c1bf4` carries only `.ufo/waves/round-24/contract.md`.

### Exit-2 paths (measured)

| Input | Exit | Message |
|---|---|---|
| `--rev deadbeef...` | 2 | `revision does not resolve to a commit` |
| `--repo /nonexistent/path` | 2 | `repository path is not a directory` |
| `--repo /tmp` | 2 | `repository path is not a git repository` |

## 4. Able to fail — sandbox mutant battery

13 mutants, each in a throwaway clone under `/fast/scratch/hyaku/mori-r24-a2/mut-routed/repo`
(clone of the lane, checked out at `4059ffb`), one commit each, each reverted after. Script:
`/fast/scratch/hyaku/mori-r24-a2/mut-routed/battery.sh`. No lane file was touched.

| Mutant | Change | Expected | Measured |
|---|---|---|---|
| M0 | none (control) | all held | `held=4`, exit 0 |
| M1 | re-add `tools/mori-quota-surface.py` | R1 red | R1 RED `quota_capability_present`, `quota_path_added` |
| M1b | re-add `corpus/knowledge/quota-surface-r23.md` | R1 red | R1 RED `quota_capability_present`, `quota_path_added` |
| M1c | add a file under `tools/` naming the historical case | R1 red | R1 RED `historical_case_named_in_tools` |
| M2 | add `privacy_clearance: true` under `corpus/` | R2 red | R2 RED `privacy_clearance_true_line_added` |
| M2b | same pattern under `.ufo/` | R2 **green** (out of scope) | R2 held, `held=4` |
| M2c | same pattern under `tools/` | R2 **green** (out of scope) | R2 held, `held=4` |
| M2d | one byte of `tools/mori-retention-gate.py` | R2 red | R2 RED `retention_evidence_changed` |
| M2e | one byte of `tools/mori-retention-reconcile.py` | R2 red | R2 RED `retention_evidence_changed` |
| M3 | one byte of the overwrite receipt | R3 red | R3 RED `capture_evidence_changed`, `round23_tree_changed`; R1 also red (A4 whole-tree pin) |
| M3b | add a file under `.ufo/waves/round-23/` | R3 red | R3 RED `round23_tree_changed`; R1 also red |
| M4 | ledger row `at` precedes its dispatch commit | R4 red | R4 RED `dispatch_committed_after_dispatch` |
| M5 | dispatch payload edited after the ledger row | R4 red | R4 RED `dispatch_committed_after_dispatch` (last-changed rule; a first-added rule would pass) |
| M6 | remove the round-24 attempts ledger | R4 red | R4 RED `no_round_ledger` |
| M7 | ledger last row `refused` | R4 red | R4 RED `attempt_ledger_not_clean`, `ledger_finding:STARTED_MISSING`, `wave_spec_without_started_ledger` |

M2b and M2c are the negative controls for the A1 scope: the same pattern outside the scope does
not trip R2, which is the point of the amendment.

**Working-tree isolation.** With four uncommitted working-tree changes in place (a new
`tools/mori-quota-surface.py`, a `privacy_clearance: true` line in
`corpus/knowledge/retention-reconciliation-r22.md`, one byte changed in
`harness-receipt-overwrite.json`, and a ledger row rewritten to `2020-01-01T00:00:00+00:00`),
the tool still reported `held=4`. The check reads committed bytes only.

## 5. Limits, stated plainly

- **Same-second tie.** Git commit times are whole seconds; `at` carries microseconds. A call
  recorded inside the dispatch commit's own second cannot be ordered; the `<=` rule passes that
  tie. This is a property of git's timestamp granularity and cannot be fixed in the tool
  (`ReviewC1Predicates.md` F5).
- **Both times are lane-written.** `at` and the committer date are written by the lane, so R4
  proves recorded ordering, not harness-observed ordering (A4's own limit; F12).
- **Only `context` and `tasks` are bound** by the ledger tool's digest; other fields of a
  dispatch file are not covered (F8). M5 catches an edit that also rewrites the ledger row.
- **`verify` does not enforce every frozen row field** (F7). R4 inherits that; it does not
  claim to.
- **A spec with no matching ledger is red.** With A4's wave-value matching, a ledger whose rows
  carry a `wave` value that differs from the spec's is not a candidate; a legacy ledger with no
  `wave` value on its rows is matched by file name instead.
- R1-R3 are regression guards, not repairs (A4). At the tip they are green because the lane has
  not broken them; only R4 was ever red in this lane's history.
- The R1 historical-case scan reads every file under `tools/` at REV, including this tool's own
  committed blob. The needle is assembled at run time precisely so that this file does not
  contain the literal.

## 6. What I did not run

- I did not run the tool at a revision where `tools/mori-dispatch-ledger.py` is absent, so the
  `dispatch_ledger_tool_unavailable` branch is code-reviewed only. (The tool is present at
  `c725aa37` and at `master`, so both measured paths are exercised.)
- I did not run the ledger tool's own `--selftest`; I ran `verify` against real committed
  ledgers at three revisions instead.
- I did not integrate, cherry-pick, or push anything. The lane repo's git index and jj state are
  untouched; the L1 integrates commit `9682f761f838a28a02841172f35c8580d1a696ef`.
- I did not write the QUALITY.md criterion lines that A4 asks for ("Each item becomes a
  QUALITY.md criterion line tagged `routed r23-R<n>` naming this check"). Those are L1 edits to a
  lane file outside my assigned write scope, so I left them to the integration owner.

## 7. Tooling

- No installs, upgrades or package changes. Nothing was installed; the task needed only the
  pre-existing git and Python.
- Versions in use: Python 3.14.8, git 2.56.0 (`git --version` on this host).
- `TMPDIR` was not set in my shell; the tool needs no scratch directory (it writes nothing).

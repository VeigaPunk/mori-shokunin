# Round 37 — erratum owed to round 38 (non-author closure findings)

author: mori (round 38), from the round-37 non-author closure `round-37-verifier-spotcheck.md`
(§Erratum A3, §Routed defects R1–R7) and the wave-1 seats `ExecLogAnchors`, `ExecScorecardRows`,
`DistillFindings`, `LabTimeoutBoundary`.
date: 2026-10-23
lane round it corrects: mori 37 (attempt 1). The filed fleet report is a record and is not edited;
this erratum names each superseded sentence.

## E1 — hardening-commit attribution (`8ff9bba` → `1caa242`)

Superseded text: the filed report, `corpus/knowledge/source-drift-hardening-r37.md`, the contract's
C2 heading and `count-c2.py`'s `HARDENING_COMMIT` all named `8ff9bba`. `8ff9bba` touches no
`tools/mori-source-drift.py` byte (`git show --name-only --format='' 8ff9bba | grep -c
tools/mori-source-drift.py` → `0`); `git log -S 'FETCH_MAX_BYTES = 4 * 1024 * 1024' --
tools/mori-source-drift.py` names `1caa242` as the commit that landed the 4 MiB read cap and the
post-redirect public-destination policy. Corrected in the lane at `4bfa0490` (A3); the fleet report
is a record, so this erratum is its disposition. The r38 counter v4 reconstructs the cited commit
and requires it to touch the tool.

## E2 — live receipt (220 → 225 rows; nine → ten drifted)

Superseded text: `LOG.md`'s Round-37 entry and the filed report pair the 220-row entering sweep
(`rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162`) with
`evidence/drift-live-r37.txt`. That file now holds the 225-row tip sweep
(`rows=225 fresh=53 excerpt=0 drifted=10 unavailable=0 no-copy=162`); the 220-row receipt is
`evidence/drift-live-r37-start.txt`. The ten drifted ids are the nine round-36 rows plus S223
(`S223.src:1953`, a fetch-varying footer; the S211 class). Neither number is a freshness verdict
(QUALITY 105).

## E3 — before-receipt command form (not runnable as printed)

Superseded text: `LOG.md:2147` and the filed report print
`count-c2.py bf0df77 --tool fixtures/memo-n1.py --seed 11` / `fixtures/summary-only.py`. The round-36
counter executes `--tool` from `cwd="/"`, so the printed relative form exits 1 with
`C2=unmet`; the receipts re-emit `<lane>/…` and re-run to `C2=met`, exit 0. The round-38 counter
resolves a repo-relative `--tool` against `--repo` (conformance check `tool_resolve`) and the
before-receipts are re-emitted under `.ufo/waves/round-38/evidence/` with a `command:` line.

## E4 — counter version beside every `C2=met`

Superseded text: the Round-37 entry's `C2=met` at `e57c58b5` is true for the **v1** counter bytes;
the v3 counter at the same revision prints `C2=unmet` (the `1caa242` correction already landed, the
live sentence already re-based). Round 37's own A3 commit records the v3 pin; this erratum states
the rule: a `C2=met` citation names the counter version and its blob pin.

## E5 — LOG.md append-only breach (`5631efa`)

`5631efa` rewrote the filed Round-37 `LOG.md` entry in place (two lines removed, ten changed:
the census line, the r17 line, the M1–M5 line and the Held line) instead of appending a correction.
The in-place rewrite stays in history. This round appends the correction to `LOG.md` (naming the
superseded text above) and records the breach as lesson M2. §102's listing rule applies to SOURCES,
not LOG, but the same append-only discipline is what the round's own correction owes.

## E6 — mistakes list and debt (f)

Superseded text: `LOG.md`'s Round-37 entry says "M1–M5"; the lesson carries M1–M10 (M6 pycache,
M7 wave design, M8 evidence hygiene, M9 content-free predicate, M10 attribution). Debt (f)
(SIGTERM → 5 s grace → SIGKILL) was re-filed **open and operator-owned** by the round-37 closure;
round 38 names it as an L0 question and does not decide it.

## E7 — capability first-working

Superseded text: `SCORECARD.md`'s capability row `round-37 C2 | source-drift re-fetch probe` states
first-working 37. The probe's live run already worked in round 36 (`evidence/drift-live-r36.txt`);
round 37's addition is the two named, mutation-killable arms. The row's first-working becomes 36
with the round-37 narrowing named, and its cited paths become uniformly repo-relative
(ExecScorecardRows: two of six cited paths failed root resolution).

## E8 — axes cells

Superseded text: the `freshness` axes cell still says "round-37 claim C2 verified …"; the round-37
closure re-attributed C2 to operability. The cell moves the pointer to `operability` and the
operability cell gains the round-37 pointer (SCORECARD axes-cell correction, appended note).

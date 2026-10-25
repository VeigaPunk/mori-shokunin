# Round 44 verifier spot-check

author: hyaku closure (non-author integrator, @m_flash)

Reviewed committed bytes at lane tip `554ff416459c92f0dea9762f834a556df2990187`; entering tip `1429c791db5891c484684feef893799909d2d6a8`. I did not author the round. Counter/gate evidence was inspected and claims re-measured as stated below; I did not execute a lane-owned selftest or gate.

## Conformance

- Fleet report `.ufo/reports/round-44/mori.md` is committed by `mori-shokunin` (`git log --format='%an %H' -- .ufo/reports/round-44/mori.md`); SHONEN heading has four checklist lines. Every cited lane commit exists; required ancestry check against `master` holds for `554ff416459c92f0dea9762f834a556df2990187` (`git merge-base --is-ancestor … master`, exit 0). `jj-lane.sh state` reports `ahead=0 behind=0`, local and remote both `554ff416…`; `git status --porcelain` is empty. Prompt is the rendered template contract plus addendum. Dispatch/completion digest copied from watchdog: `2026-10-25T04:27:39-03:00 launch mori round=44 pgid=3471430 driver=hyaku-inline attempt=1`; `2026-10-25T06:05:35-03:00 complete mori round=44; hyaku-inline attempt=1`.
- No marker: report names substantial committed work and resolvable evidence. Status-neutral report defects: report cites multiple intermediate lane commits and includes three post-filing errata; the errata correctly name superseded statements and preserve prior bytes. SHONEN uses `[~]`/`[ ]`, not non-author `[x]`.

## Claims

| claim | independent re-check / observed output | verdict |
|---|---|---|
| C1 calibration, figure reconciliation | `python3 .ufo/waves/round-44/count-c1.py 554ff416459c92f0dea9762f834a556df2990187` → `rows=16`, classes `checks,corpus,evidence,registry,wave`, `commands_reconcile PASS`, `C1=met mismatches=0` (exit 0). Re-measured. | calibration improved |
| C2 operability, registered counters | `python3 .ufo/waves/round-44/count-c2.py 554ff416459c92f0dea9762f834a556df2990187 --counter .ufo/waves/round-44/count-c1.py --counter .ufo/waves/round-44/count-c2.py --counter .ufo/waves/round-44/count-c3.py --mutants-dir .ufo/waves/round-44/fixtures/mutants` → 5 checks PASS including registry, tally and mutant kill; `C2=met` (exit 0). Re-measured counter verdict; selftest/mutant claims were verified from committed receipts, not run. | operability improved |
| C3 depth, sourced FR5 entry | `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin python3 .ufo/waves/round-44/count-c3.py 554ff416459c92f0dea9762f834a556df2990187 --entry corpus/knowledge/pid-probe-conclusion-r44.md --row S471 --row S472` → entry, rows, census, README checks PASS; `C3=met` (exit 0). Re-measured under the disclosed environment condition. | depth improved |

No owned axis harmed: `git diff 1429c791db5891c484684feef893799909d2d6a8 554ff416459c92f0dea9762f834a556df2990187 -- SCORECARD.md` shows corrections/claim records and does not remove or lower an axis score. Report's three errata explicitly disclose material counter limits, adjacency, and C3's `TMPDIR`/`--census` condition. Other axes unchanged; no cross-domain tool imported.

## Discernment spot-check

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S471 admit | admit | https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html, `/proc/[pid]/cmdline` | agree | Reopened page contains the Japanese statement that zombie `cmdline` is empty and reading returns no characters, grounding the scoped claim. The lesson records a 28-non-space-character quote, which is ≤25 words. |
| S472 admit | admit | https://man.archlinux.org/man/proc.5.zh_TW; fetch attempted, returned ECONNRESET. | unable to independently verify | This source could not be reopened in this session, so I do not count it as independently agreed. This is a verification limitation, not evidence the quoted content is false. |
| `failed-scope-keeps-limit-r50.md` reject | reject | source and recheck named in `corpus/lessons/round-44.md` §Gate: `systemctl reset-failed` after creating scope; lane `PROVINCE.md` read-only detection/report boundary | agree | The documented recheck entails host mutation and lies outside the declared lane boundary; the stated read-only `MemoryMax` flip is relevant. Source URL was not supplied in the Gate, so this is a decision check against the cited local source/recheck, not a live external-source validation. |

SOURCES row spot-check: reopened S471 page above. Lesson quote location `/proc/[pid]/cmdline`; exact quoted text is grounded in page; recorded length 28 non-space characters (under 25 words). Registry row `S471` was inspected at `corpus/SOURCES.md` in the round tip. Census command `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` returned `mori ok` (exit 0), with W04 duplicate-URL warnings only.

## Trends

- **expansion — improved:** report records 243→245 registry rows, one admitted entry and FR5 map movement; C3 counter and census both pass at the reviewed revision.
- **quality — improved:** C1 and C2 claims re-measure green at the tip; report and lesson disclose instrument limitations rather than concealing them. C3's environment dependence is explicitly disclosed in erratum 3.
- **discernment — unprovable-but-better:** the S471 admit and reject decision checked out, but S472 source could not be fetched during this review; insufficient full admit/reject agreement for `improved`.

## Routed defects

1. S472 independent source reopening remains outstanding; the cited host reset the connection. Preserve the distinction between inaccessible and disproven.
2. Report erratum 3 accurately narrows C3's passing conditions; ensure future readers use explicit `--census` when replaying outside this host/repo arrangement.
3. Report's SHONEN boxes remain asserted/untouched, not non-author checked; operator owns any promotion decision.

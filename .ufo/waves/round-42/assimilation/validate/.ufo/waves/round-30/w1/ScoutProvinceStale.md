# ScoutProvinceStale — PROVINCE.md statements that disagree with lane state at 58b61681

Seat: MoriR30.ScoutProvinceStale (leaf, no subagents, no background jobs).
Question: read `PROVINCE.md` whole and list every statement that disagrees with observed repo
state at `58b61681a0e3f3b821a17d38a4e713ccd9921615` — tools named that do not exist, tools
present but not named, round numbers, and frontier/core placement contradicted by the SCORECARD
capability record. Independence: I did not open `.ufo/waves/round-29/w1/ScoutShonen.md`.

Method: `PROVINCE.md` working tree is byte-identical to the requested revision, so line numbers
below are that revision's. I compared it with `SCORECARD.md`, the `tools/` tree, and the tools'
own bytes. No writes outside this report; no tool installs; read-only git only.

```sh
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ git diff --stat 58b61681 HEAD -- PROVINCE.md
            # no output: PROVINCE.md is unchanged from 58b61681 to HEAD
$ git status --porcelain -- PROVINCE.md
            # no output: no uncommitted edit either
$ git rev-parse HEAD
e936482a6070db40049bff46f7da4754b15d41af
```

## Findings

### F1 — Three rounds are missing; the newest section is Round 27

`PROVINCE.md:373` is `## Round 27 — FR10 victim selection (knowledge, no new tool)`, and it is
the last section (`wc -l PROVINCE.md` → 384; `:384` is the final line). The lane is in round 30:
`SCORECARD.md:1749` declares round 28, `:1779` round 29, `:1804` round 30 (`Entering tip
58b61681…`), and the wave directories exist.

```sh
$ ls -1 .ufo/waves | tail -3
round-28
round-29
round-30
$ grep -n 'Entering tip' SCORECARD.md
1749:Entering tip `6ebd518f…` (round 27 closed `rejected-honest-stop`…
1779:Entering tip `7118f320…` (round 28 admitted…
1804:Entering tip `58b61681…` (round 29 closed `rejected-honest-stop`…
```

Statements that do not exist in `PROVINCE.md` at all and should if it is to describe the current
lane: round-28 C1 freshness (eight superseded rows, three restored rows; `SCORECARD.md:1771`),
round-28 C2 A2 freeze (`SCORECARD.md:1772`), round-29 C1 Axes/closure reconciliation
(`SCORECARD.md:1785`), round-29 C2 miss plus its tool change (`SCORECARD.md:1797`), and the
round-30 claims (`SCORECARD.md:1810`).

### F2 — Three Core rows still say "admission pending" after the closure admitted them

| Province statement | Province says | Closure record says |
|---|---|---|
| pressure row, `PROVINCE.md:283` | "The Core row above is **pending admission** by the non-author closure." | `SCORECARD.md:1540` "Entering tip `28b79d3d…` (round 24 admitted)"; capability row `SCORECARD.md:1534` |
| runway bullet, `PROVINCE.md:353-354` | "The Core bullet above is **pending admission** by the non-author closure." | `SCORECARD.md:1590` "Entering tip `248408f5…` (round 25 admitted…)"; capability row `SCORECARD.md:1568` |
| oom-killers heading, `PROVINCE.md:359` | "…(FR10 partial advance, admission pending)" | `SCORECARD.md:1720` "Entering tip `fc09f96c…` (round 26 admitted…)"; capability row `SCORECARD.md:1620` |

The round-27 knowledge row is stale in a different direction: `PROVINCE.md:375` still reads
"admission pending", but `SCORECARD.md:1749-1751` records "round 27 closed `rejected-honest-stop`:
C1 depth verified, C2 withdrawn and so not verified." The closure happened; its outcome was a
rejection, not a pending admission.

```sh
$ grep -n 'pending admission\|admission pending' PROVINCE.md
236:- …(FR12 partial advance, admission pending):
283:  … The Core row above is **pending admission** by the
294:- …(new FR15 advance, admission pending):
353:  … The Core bullet above is **pending
359:- …(FR10 partial advance, admission pending):
375:- **Core, knowledge (FR10 partial advance, admission pending):**
```

### F3 — The `## Core` block names 7 surfaces; the lane now has 6 more registered capabilities

The Core block (`PROVINCE.md:22-28`) lists watchdog, waves, kill/OOM classes, same-boot journal
window, resource runway, tmux relevance, lane silence. None of the later landed tools appear
there; each survives only as an appended note and a `SCORECARD.md` capability row:

| Capability row | Tool | Province mention |
|---|---|---|
| `SCORECARD.md:1269` per-seat wave settlement scan | `tools/mori-wave-settlement.py` | Core bullet at `PROVINCE.md:145` only (outside the Core block) |
| `SCORECARD.md:1407` retention receipt reconciliation | `tools/mori-retention-reconcile.py` | described as "the retention reconciler" at `PROVINCE.md:199`, file never named |
| `SCORECARD.md:1534` one-shot system pressure read | `tools/mori-pressure.py` | Core row at `PROVINCE.md:236` only |
| `SCORECARD.md:1535` round-23 routed-item check | `tools/mori-routed-check.py` | absent |
| `SCORECARD.md:1568` harness background-job runway read | `tools/mori-job-runway.py` | Core bullet at `PROVINCE.md:294` only |
| `SCORECARD.md:1620` userspace OOM killer read | `tools/mori-oom-killers.py` | Core bullet at `PROVINCE.md:359` only |

The file itself concedes the split: `grep -c 'Core,' PROVINCE.md` → `10` "Core, …" bullets in
appended sections, against 7 bullets in the `## Core` block. A reader who stops at line 28 gets a
core/frontier placement the capability register contradicts.

Related: FR15 is defined at `PROVINCE.md:321` but the `## Frontier` list (`:42-57`) ends at FR14.
The Frontier section therefore is not the complete frontier register, and `PROVINCE.md:321`
explicitly says "(new row; FR1–FR14 are unchanged)" from inside the round-25 section.

### F4 — Sixteen tool files on disk are never named in PROVINCE.md; five are named by SCORECARD

```sh
$ comm -23 <(find tools -maxdepth 1 -type f -printf '%f\n' | sort) \
           <(grep -oE 'tools/[A-Za-z0-9._-]+' PROVINCE.md | sed 's|tools/||' | sort -u)
mori-content-review.py
mori-evidence-loss.py
mori-misroot-sweep.py
mori-retention-reconcile.py
mori-round13-regressions.py
mori-round14-regressions.py
mori-round15-regressions.py
mori-round16-context-check.py
mori-round16-regressions.py
mori-round17-context-check.py
mori-round17-jj-regressions.py
mori-round17-seat-regressions.py
mori-round19-regressions.py
mori-routed-check.py
mori-routed-r24.py
mori-silence-cases.sh
# 16 total; tools/ holds 26 files
```

Of those, five are load-bearing in the SCORECARD's own record and were still omitted from the
province: `tools/mori-evidence-loss.py` (`SCORECARD.md:1327-1329`, round-21 C2 deliverable and
carried at `:1401`), `tools/mori-retention-reconcile.py` (`SCORECARD.md:1407`),
`tools/mori-routed-check.py` (`SCORECARD.md:1535`), `tools/mori-routed-r24.py`
(`SCORECARD.md:1569`), `tools/mori-silence-cases.sh` (`SCORECARD.md:115`). Of the rest,
`tools/mori-content-review.py` has a corresponding capability row ("Bounded content-review
coverage gate", `SCORECARD.md:1228`) but its file is named in neither document, and
`tools/mori-misroot-sweep.py` is named in neither document at all (its docstring at `:2` is the
only description).

### F5 — Fixtures: 8 files present, 2 named; the whole oom-killers case set is unnamed

```sh
$ find tools/fixtures -type f | sort
tools/fixtures/mori-job-runway/cases.json
tools/fixtures/mori-job-runway/supplementary-cases.json
tools/fixtures/mori-oom-killers/cases-a2.json
tools/fixtures/mori-oom-killers/cases-a2-r29.json
tools/fixtures/mori-oom-killers/cases.json
tools/fixtures/mori-oom-killers/cases-supplementary.json
tools/fixtures/mori-pressure/cases.json
tools/fixtures/mori-pressure/supplementary-cases.json
```

`PROVINCE.md` names only the two `cases.json` files at `:280` and `:351`. The four oom-killers
case files — the artefact rounds 27-30 argue over (`SCORECARD.md:1727`, `:1772`, `:1786`,
`:1811`) — are not named, and the round-26 Core row (`PROVINCE.md:359-364`) cites no fixture at
all, though its sibling rounds 24 and 25 each name their frozen cases.

### F6 — The journal-window Core bullet still carries the phrase its own file supersedes

`PROVINCE.md:25` reads "(round-16 build; verification pending)". `PROVINCE.md:98` explicitly says
"**Supersedes “verification pending” in the same-boot window Core row**", and
`SCORECARD.md:1009-1010` records "Outside r16 closure admitted the bounded window with routed
procedural defects". The Core bullet at `:25` still reads that way at the tip (it is unchanged
between 58b61681 and HEAD), so the file contradicts itself and the closure record in place.

### F7 — Census citation drift: the cited line numbers no longer hold the claimed text

`PROVINCE.md:94` says the census documents `MORI_DISK_TARGETS` as defaulting to `$ROOT /tmp`
"(`tools/mori-census.sh:211-212,282`)". Observed on those lines:

```sh
$ sed -n '211,212p;282p' tools/mori-census.sh
# Live mode writes nothing. --selftest writes only under
# ${TMPDIR:-/tmp}/mori-census-selftest.XXXXXX and asserts the fixture tree is unchanged.
SELF=$(readlink -f -- "${BASH_SOURCE[0]}" 2>/dev/null || {
$ grep -n 'MORI_DISK_TARGETS' tools/mori-census.sh
237:#   MORI_DISK_TARGETS    space-separated paths for df (default: ROOT /tmp)
321:DISK_TARGETS=${MORI_DISK_TARGETS:-"$ROOT /tmp"}
```

The claim's substance survives at `:237` and `:321`; the pointer does not. The census is now 4744
lines, so the round-12 pointer has been overtaken by later insertions.

### F8 — The oom-killers Core row under-describes the tool's own result contract

`PROVINCE.md:359-364` describes only "`systemctl show` … the earlyoom unit journal of the current
boot (counts only, in memory) and the count of systemd-oomd kill notices" plus the three-verdict
vocabulary. The tool's result object at `tools/mori-oom-killers.py:501-517` carries, besides
those, `earlyoom.state`, `version`, `grammar`, `thresholds`, `scope_complete`, `actions`,
`dryrun`, `dryrun_send_lines`, `process_group_lines`, `earlier_invocation_send_lines`, and
`oomd.state` + `notices_this_boot`; `SHOW_PROPERTIES` at `:62` also reads
`ActiveEnterTimestampMonotonic`. `SCORECARD.md:1620` names the version string, the four startup
thresholds and six line classes as part of the capability. Province omits all of them. The
three-verdict claim itself is correct (`tools/mori-oom-killers.py:68-70`). [INFERENCE] This
matters because the disputed round-29/30 shape (active unit, missing or zero enter-stamp) turns
on fields the province never names.

### F9 — Frontier rows FR3/FR10/FR11/FR12/FR14 read as unadvanced while the register records Core advances

`PROVINCE.md:46` (FR3), `:53` (FR10), `:54` (FR11), `:55` (FR12), `:57` (FR14) are still listed
under `## Frontier` with their round-11/12 boundary text. Each has since been recorded as a Core advance by the same file's appended notes, and FR3, FR10,
FR11 and FR12 also by the capability register: FR3 `PROVINCE.md:145`
vs `SCORECARD.md:1269`; FR10 `PROVINCE.md:359` vs `SCORECARD.md:1620`; FR11 `PROVINCE.md:40` vs
`SCORECARD.md:997` ("the demonstrated FR11 capability"); FR12 `PROVINCE.md:236` vs
`SCORECARD.md:1534`; FR14 is a province-internal Core note at `PROVINCE.md:103` with no
capability row of its own. The Frontier wording "remain frontier" is defensible
as "remainder only", but the rows do not say so, and the register's capability rows do.
[INFERENCE] This is the placement contradiction the assignment asks for; severity is editorial,
not factual, because the appended notes do carry the advances.

## Checked and consistent (no disagreement found)

- **No phantom tool path.** Every `tools/…` path named in `PROVINCE.md` exists at 58b61681:
  `mori-census.sh`, `mori-dispatch-ledger.py`, `mori-freeze-order.py`, `mori-job-runway.py`,
  `mori-journal-window.py`, `mori-oom-killers.py`, `mori-pressure.py`, `mori-retention-gate.py`,
  `mori-seat-terminal.py`, `mori-wave-settlement.py`, and both named `cases.json` files. The one
  foreign path, `../tsukuroi-shokunin/tools/tsukuroi-census.sh` (`PROVINCE.md:287`), resolves
  (`-rwxr-xr-x … 145062 bytes`) and its cited lines do hold the PSI read: `:376` is
  `PRESSURE_FILE=${TSUKUROI_PRESSURE_FILE:-/proc/pressure/memory}`, `:1100-1115` reads it.
- **Frozen case counts match the province's claims.** `tools/fixtures/mori-pressure/cases.json`
  has 12 cases; `tools/fixtures/mori-job-runway/cases.json` has 21 — the same numbers asserted at
  `PROVINCE.md:279` and `:350`.
- **Schemas match.** `mori-pressure-v1` (`tools/mori-pressure.py:66`), `mori-job-runway-v1`
  (`:98`), `mori-oom-killers-v1` (`:57`) are the names used at `PROVINCE.md:239`, `:296`, `:363`.
- **Census scope claim holds.** `PROVINCE.md:253-254` says the census reads only the user-slice
  `memory.pressure`: `grep -n '/proc/pressure' tools/mori-census.sh tools/mori-pressure.py` hits
  only `mori-pressure.py` (`:5`, `:12`, `:87`); the census defaults
  `CGROUP_PRESSURE=${CGROUP_EVENTS%.events}.pressure` under `user.slice` (`:304-308`).
- **Surface names hold.** `SURFACE watchdog`, `SURFACE waves`, `SURFACE cgroup`, `SURFACE disk`,
  `SURFACE tmux` and the dynamic `SURFACE lane.$lane` (`tools/mori-census.sh:2545`) all exist.
- **`SCORECARD.md:1592`'s pointer to `PROVINCE.md:53` is correct**: line 53 is the FR10 row.

## Unresolved

- Whether the province should name regression harnesses (`mori-round13-…`, `mori-round19-…`,
  `mori-round16-context-check.py`, …) is a lane policy question, not a repo contradiction; I list
  them because the assignment asks for tools present but not named, and leave the judgment to L1.
- I did not audit `SCORECARD.md` against commits; its admissions are taken as the closure record
  the assignment names. No SCORECARD claim above was independently re-derived from a commit.
- The open question behind F8 (which verdict shapes the round-29/30 disputed cases should pin) is
  outside this seat; I only record that the province's description is narrower than the tool.

## Install / scratch disclosure

No packages installed or updated. No subagents, no background jobs. Scratch use: one inline
`python3` read of case files; no files written outside this report.

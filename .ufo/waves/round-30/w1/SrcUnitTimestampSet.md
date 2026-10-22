# SrcUnitTimestampSet — round 30 wave 1 (C1 frontier source row)

Seat: `SrcUnitTimestampSet` (leaf). Work window 2026-10-22T21:12Z–21:16Z. Lane read at tip `58b61681` (no git writes).
Assignment: one sourced row for the fact "where systemd v262 sets the active-enter timestamp on entry to the active
state, and whether a stop retains it while a restart overwrites it". Opened three URLs by `curl` in scratch; nothing in
the lane was written except this report; no tool was installed.

## Outcome per candidate

| candidate (v262) | outcome | decisive evidence |
|---|---|---|
| `src/core/unit.c` | **admit** (`S15x`; next free id at tip is `S156`) | the only assignment to `u->active_enter_timestamp` in the file, `:2774`, inside `unit_notify()` |
| `src/basic/time-util.h` | reject — duplicate URL | already a source of row S154 (`corpus/SOURCES.md:160`); `grep -c 'u->active_enter_timestamp ='` = 0 |
| `src/core/service.c` | reject — does not carry the set | funnels state changes to `unit_notify` (`:1731`) and only reads the stamp (`:1028`); 0 assignments |

The literal candidate URL `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c` is **not** in the
registry: `grep -n 'v262/src/core/unit.c' corpus/SOURCES.md` prints nothing (exit 1). The path appears twice at the tip,
neither as this row: S036 (`corpus/SOURCES.md:42`) cites `src/core/unit.c` at commit `cf8ebfc6159c…` with scope
"emitted unit-failure and process-exit structured field schema" (`:6333-6392`), and `corpus/SOURCES.md:180` is the
bounded-search note for S036. A v262 row is therefore new by URL, revision and scope.

## Opened sources (bytes fetched, hashes exact)

```sh
cd /fast/scratch/hyaku/mori-r30/SrcUnitTimestampSet
date -u +%FT%TZ   # 2026-10-22T21:12:02Z
curl -sSL -o unit.c https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c
sha256sum unit.c  # 47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7
wc -l unit.c      # 7294 unit.c
date -u +%FT%TZ   # 2026-10-22T21:12:50Z
curl -sSL -o time-util.h https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/time-util.h
sha256sum time-util.h  # 45e934d294f2ff0ca92cc7f1fcede1ef92862d20b276e305282cec5f3cba37e6
date -u +%FT%TZ   # 2026-10-22T21:13:24Z
curl -sSL -o service.c https://raw.githubusercontent.com/systemd/systemd/v262/src/core/service.c
sha256sum service.c    # 9bf8a80bc29ef733648c688e4f40c3d01d6a4f67a877b2b5e23fbf8284c03d9c
```

Revision pin: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git ls-remote https://github.com/systemd/systemd 'refs/tags/v262*'`
printed `1f7dffaf714cc4488159c498b7a17cf34c5a96d5 refs/tags/v262` and
`8cc40e0c5e9234bf45084751ac53b1fbfe70b492 refs/tags/v262^{}`, so tag v262 is commit
`8cc40e0c5e9234bf45084751ac53b1fbfe70b492` — the same resolution S122 records.

## The fact in the source

`unit_notify()` refreshes `state_change_timestamp` with `dual_timestamp_now` (`unit.c:2766`), then writes
`u->active_enter_timestamp` only when the transition enters the active-or-reloading set from outside it
(`:2773-2774`); the reverse transition writes `active_exit_timestamp` instead (`:2775-2776`). Consequence read
straight off the branch: a stop (active → deactivating/inactive) leaves `active_enter_timestamp` untouched, and a later
activation runs the first branch again, replacing it. Local sweep: `grep -n 'active_enter_timestamp' unit.c` lists
`:2774` as the only assignment in the file; the other mentions are `inactive_*` reads at `:1971`, `:2066`, `:2451-2453`.

## Draft SOURCES.md row (ready to paste; 11 cells, NF=13)

```markdown
| S15x | systemd v262 `unit_notify()` active-enter and active-exit timestamp assignment — https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c | code | A | the assignment of `u->active_enter_timestamp` inside `unit_notify()` at the v262 release tag: the guard requiring a transition into the active-or-reloading set, the copy from the `state_change_timestamp` refreshed earlier in the same block, and the else-branch that stamps `active_exit_timestamp` on leaving that set, so the active-enter stamp is overwritten on each entry and retained across a stop; not the `UNIT_IS_ACTIVE_OR_RELOADING` macro expansion, not the meaning of the `ActiveEnterTimestampMonotonic` property (S122), not the journal entry stamp (S154), not daemon-reload behavior | src/core/unit.c:2763-2777 (`unit_notify` timestamp block); tag v262 = commit 8cc40e0c5e9234bf45084751ac53b1fbfe70b492 | Entering the active state overwrites the active-enter stamp with the transition's own clock reading, while leaving that state writes only the active-exit stamp, so a stop retains the old value and a restart replaces it. | mined | 2026-10-22 | on-release | corpus/lessons/round-30.md, corpus/knowledge/earlyoom-invocation-scope-r30.md |
```

## Draft Gate lines for `corpus/lessons/round-30.md` (one admit, two rejects)

```markdown
| S15x | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c | 2026-10-22T21:12:02Z | `47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7` | `:2773-2776` (15 words): "if (!UNIT_IS_ACTIVE_OR_RELOADING(os) && UNIT_IS_ACTIVE_OR_RELOADING(ns)) u->active_enter_timestamp = u->state_change_timestamp; else if (UNIT_IS_ACTIVE_OR_RELOADING(os) && !UNIT_IS_ACTIVE_OR_RELOADING(ns)) u->active_exit_timestamp = u->state_change_timestamp;" | admit, A, mined |
| S15y | https://raw.githubusercontent.com/systemd/systemd/v262/src/basic/time-util.h | 2026-10-22T21:12:50Z | `45e934d294f2ff0ca92cc7f1fcede1ef92862d20b276e305282cec5f3cba37e6` | `:91` (3 words): "dual_timestamp* dual_timestamp_now(dual_timestamp *ts);" | reject, duplicate URL: the URL is already a source of row S154 (corpus/SOURCES.md:160), so it is not a new row; the file declares `dual_timestamp_now` and holds no assignment to `active_enter_timestamp` (grep -c 'u->active_enter_timestamp =' time-util.h = 0) |
| S15z | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/service.c | 2026-10-22T21:13:24Z | `9bf8a80bc29ef733648c688e4f40c3d01d6a4f67a877b2b5e23fbf8284c03d9c` | `:1731` (6 words): "unit_notify(u, table[old_state], table[state], s->reload_result == SERVICE_SUCCESS);" | reject, does not carry the fact: the service state machine funnels state changes into `unit_notify` (:1731) and only reads the stamp as a deadline base (:1028), with no assignment to `active_enter_timestamp` in the file (grep -c 'u->active_enter_timestamp =' service.c = 0); the write site is unit.c:2774 |
```

Reject reasons are verified, not asserted (round-29 R2): the three counts above are raw `grep -c` output
`unit.c:1  time-util.h:0  service.c:0`, and the S154 duplicate is the URL printed in that row at
`corpus/SOURCES.md:160`. `S15y`/`S15z` are placeholders only; do not commit them as ids.

## Excerpt file body for `corpus/evidence/sources-r30/S15x.txt`

Excerpt of the quoted block `2766..2776` with three context lines each side (`2763..2779`, the maximal range the
wave-context format allows); `accessed` is the fetch time above. Lines `2763`, `2767` and `2772` are blank in the
source and appear as `number` + TAB + empty text. Privacy scan of the block: no uid, `user@<digits>`,
`user-<digits>.slice`, host name or e-mail address (`python3` regex over the exact excerpt: no hits).

```text
id: S15x
url: https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c
sha256: 47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7
accessed: 2026-10-22T21:12:02Z
lines: 2763-2779

2763	
2764	        /* Update timestamps for state changes */
2765	        if (!MANAGER_IS_RELOADING(m)) {
2766	                dual_timestamp_now(&u->state_change_timestamp);
2767	
2768	                if (UNIT_IS_INACTIVE_OR_FAILED(os) && !UNIT_IS_INACTIVE_OR_FAILED(ns))
2769	                        u->inactive_exit_timestamp = u->state_change_timestamp;
2770	                else if (!UNIT_IS_INACTIVE_OR_FAILED(os) && UNIT_IS_INACTIVE_OR_FAILED(ns))
2771	                        u->inactive_enter_timestamp = u->state_change_timestamp;
2772	
2773	                if (!UNIT_IS_ACTIVE_OR_RELOADING(os) && UNIT_IS_ACTIVE_OR_RELOADING(ns))
2774	                        u->active_enter_timestamp = u->state_change_timestamp;
2775	                else if (UNIT_IS_ACTIVE_OR_RELOADING(os) && !UNIT_IS_ACTIVE_OR_RELOADING(ns))
2776	                        u->active_exit_timestamp = u->state_change_timestamp;
2777	        }
2778	
2779	        /* Keep track of failed units */
```

## Checks run on the drafts

- Word counts by `wc -w` on the whitespace-collapsed quotes: primary `:2773-2776` = **15**; `:2766` = **1**
  (second located quote, carried by the excerpt); reject `:91` = **3**; reject `:1731` = **6**. All ≤ 25.
- Quote containment: stripping each excerpt line's `^[0-9]+\t` prefix, joining and collapsing whitespace, both
  quotes are found verbatim in `2763..2779` (python3 check printed `q1 in flat: True`, `q2 in flat: True`). The
  excerpt reproduces `unit.c` lines 2763–2779 byte-for-byte (17 lines, one TAB per line, no tab inside any text).
- Row shape: 11 cells → `NF=13`; no `|` inside any cell; `kind=code`, `tier=A`, `status=mined`, `opened=2026-10-22`,
  `recheck=on-release`; the two `used-by` paths are this round's C1 lesson and entry, which must exist at the landing
  commit (the SOURCES census flags `mined` rows whose `used-by` paths do not exist).
- Id: `grep -oE '^\| *S[0-9]{3,}' | sort -n | tail -1` prints `155`, so the placeholder becomes `S156` if no other
  round-30 seat takes it first.

## Limits and conflicts

- `count-c1.sh` **does not exist** at this read (`sed` returned `No such file or directory`; BuildCountC1 is still
  running). The draft was checked against contract conditions 2–4, not against the committed script. If that script
  rejects excerpt lines whose text after TAB is empty, fallback: drop the `:2766` quote and the blank-line range, and
  use `lines: 2770-2779` with the primary quote only (containment re-verified above for that range too).
- `UNIT_IS_ACTIVE_OR_RELOADING` expansion (`src/core/unit.h`) was **not opened**; the row quotes the predicate verbatim
  and does not expand it. [INFERENCE] UNIT_ACTIVE and UNIT_RELOADING are its members by name; not claimed in the row.
- "Only assignment in the file" is a single-file sweep (`grep -n 'active_enter_timestamp' unit.c`); no whole-tree sweep
  was run, and the row does not claim a system-wide unique write site.
- The restart half is the branch condition plus "restart = stop then start": [INFERENCE] the restart job re-enters the
  active set, so `:2773-2774` executes again. No unit was started, stopped or restarted on this host (detection bounds);
  the claim is static source reading only.
- The mapping from the D-Bus property `ActiveEnterTimestampMonotonic` to this field is S122's scope
  (`man/org.freedesktop.systemd1.xml:2244,2780,2783-2790` as that row records it) and was not re-opened here.
- No conflict with another seat; no lane file, git/jj state, fleet file or host unit was touched. No tool installed.

Touched surfaces: this report only, plus fetched bytes under
`/fast/scratch/hyaku/mori-r30/SrcUnitTimestampSet/` (`unit.c`, `time-util.h`, `service.c`).

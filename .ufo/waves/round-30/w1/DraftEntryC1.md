# DraftEntryC1 — prose draft for `corpus/knowledge/earlyoom-invocation-scope-r30.md` (C1, depth)

Seat: MoriR30.DraftEntryC1 (leaf, wave 1). Assignment: draft the C1 entry prose; the L1 fills the decision-table rows
and binds source ids. No lane writes beyond this report and my scratch; no git/jj writes; no host unit, journal,
setting or signal touched; no subagent; no tool installs.

## What I read (read-only, entering tip `58b61681`)

- `.ufo/waves/round-30/contract.md:23-53` (C1 conditions), `:56-76` (C2 conditions incl. the disputed-shape pin),
  `:118` (R6 second half).
- `.ufo/waves/round-30/rule-text.md:24-52` (scope, grammar, output, verdicts), `:82-98` (unbounded, earlier
  invocations, wave-2 fixes), `:105-114` (A2-01, A2-05..A2-10).
- `corpus/lessons/round-29-verifier-spotcheck.md:77-98` (harm ruling: shape, code read, written rules, no older pin,
  ruling).
- Header shape: `corpus/knowledge/oom-victim-selection-r27.md:1-3`, `corpus/knowledge/userspace-oom-killers-r26.md:1`,
  `corpus/knowledge/structured-journal-scopes-r13.md:1-4`.
- `tools/mori-oom-killers.py:240-530` (scope, earlier count, verdict block); the four fixtures' id/expect values.
- Not read: writer reports, `.ufo/waves/round-30/w1/CaseR30*.md`, `count-c1.sh` (not committed at my start).

## Behaviour probed (invented inputs only, `/fast/scratch/hyaku/mori-r30/DraftEntryC1/`)

`python3 -I -B tools/mori-oom-killers.py --inputs <file>`; invented unit names, pids, uids, process names.

1. active, stamp `0`, send, restart → `KILLERS_UNKNOWN` exit 2, `scope_complete=false`, `sigterm=0`, `sigkill=0`,
   earlier=1, `version=1.9.0`, `grammar=verified-1.9.0`.
2. active, stamp `2000000`, send at `1000001`, restart at `2000000` → `KILLERS_QUIET` exit 0, `scope_complete=true`,
   earlier=1.
3. inactive, earlier send → `KILLER_ACTED` exit 1, `actions=null`, earlier=1.
4. `LoadState=not-found`, earlier SIGKILL → `KILLER_ACTED` exit 1, `state=absent`, `actions=null`, earlier=1.
5. `ActiveState=failed` / `activating`, stamped send → `KILLER_ACTED` exit 1, `state=unavailable`, `actions=null`,
   earlier=1.
6. active, in-scope send → `KILLER_ACTED` exit 1, `sigterm=1`, `scope_complete=true`, earlier=0.
7. in-scope `Suppressed 12 messages from earlyoom.service` → `KILLERS_UNKNOWN` exit 2, `scope_complete=false`.
8. record without `__MONOTONIC_TIMESTAMP`, no other evidence → `KILLERS_UNKNOWN` exit 2, `scope_complete=false`,
   `sigterm=0`, earlier=0.
9. two in-scope invocations, first dry-run → `KILLER_ACTED` exit 1, `dryrun=true`, `dryrun_send_lines=1`, `sigterm=1`.
10. dry-run only → `KILLERS_QUIET` exit 0, `scope_complete=true`, `dryrun_send_lines=1`, `sigterm=0`.
11. unbounded active, send after last version line → `KILLER_ACTED` exit 1, `scope_complete=false`, `sigterm=1`,
    earlier=1.
12. bounded active, earlier `Suppressed …` + earlier send → `KILLERS_QUIET` exit 0, `scope_complete=true`, earlier=1.
13. bounded active, version line only → `KILLERS_QUIET` exit 0, `scope_complete=true` (A3 limit).

Not run: `--selftest` on any file (counted runs belong to the L1/verifiers).

## Source slots opened this round (S156+ candidates; ids bound by the L1)

Fetched with plain `curl -fsSL` on 2026-10-22; sha256 is of the full bytes in my scratch.

| Slot | URL (tag) | sha256 (fetched) | Fact needed | Lines |
|---|---|---|---|---|
| S???a | `raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` | `08656b0b…f5f9d0e4` (21:16:16Z) | `earlyoom <version>` printed once at startup; `dryrun mode enabled, will not kill anything` | `:161`, `:295` |
| S???b | `raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c` | `b32e0fad…b100bf3` (21:16:16Z) | send line `sending %s to process …`; escalation `escalating to SIGKILL after …` | `:627`, `:318` |
| S???c | `raw.githubusercontent.com/systemd/systemd/v262/man/org.freedesktop.systemd1.xml` | `59cfeea5…218117ca` (21:16:16Z) | `ActiveEnterTimestampMonotonic` CLOCK_MONOTONIC µs stamp; fields are 0 when the transition was not recorded this boot | `:2780-2790` |
| S???d | `raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c` | `428dc830…52a7ffa2` (21:17:20Z) | journald `Suppressed %i messages from %s` notice | `:1294` |

Full shas: a `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4`; b
`b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3`; c
`59cfeea5144e169369ee81f2b797fe9eb63ec18cb6aa918c2e66a7d5218117ca`; d
`428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2`. Gate lines, excerpt files and final ids are the
source seats'/L1's work; re-check my shas and lines against those gates rather than trusting this table.

Path caveat: v262 moved journald from `src/journal/journald-server.c` to `src/journal/journald-manager.c` (`journald.c`
includes `journald-manager.h`); `journald-server.c` 404s at `v262` and at `main`. Quote `:1294` from the manager file.

## The entry draft (ready to paste; every citation is `S???`)

```markdown
source: S??? (earlyoom v1.9.0 `main.c` — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c — `:161` prints `earlyoom <version>` once at startup, the only boundary between invocations; `:295` prints `dryrun mode enabled, will not kill anything`; sha256 08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4, fetched 2026-10-22T21:16:16Z); S??? (earlyoom v1.9.0 `kill.c` — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c — `:627` is the `sending SIGTERM/SIGKILL to process …` line and `:318` the `escalating to SIGKILL after …` line; sha256 b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3, fetched 2026-10-22T21:16:16Z); S??? (systemd v262 `man/org.freedesktop.systemd1.xml` — https://raw.githubusercontent.com/systemd/systemd/v262/man/org.freedesktop.systemd1.xml — `:2780-2790` defines the CLOCK_MONOTONIC 64-bit microsecond stamps and says the fields are 0 when the transition was not recorded this boot; sha256 59cfeea5144e169369ee81f2b797fe9eb63ec18cb6aa918c2e66a7d5218117ca, fetched 2026-10-22T21:16:16Z); S??? (systemd v262 `src/journal/journald-manager.c` — https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c — `:1294` emits `Suppressed %i messages from %s`, the rate-limit notice the reader keys on; sha256 428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2, fetched 2026-10-22T21:17:20Z)
verified-at: 2026-10-22 — the four URLs in `source:` fetched this round (access times above); lane rule text `.ufo/waves/round-30/rule-text.md` and `tools/mori-oom-killers.py` read at the entering tip 58b61681; tool behaviour probed on invented inputs only, under /fast/scratch (no host unit, journal, setting or signal touched)
recheck: on an earlyoom release re-open `main.c` at the version and dry-run prints and `kill.c` at the send and escalation prints; on a systemd release re-open `org.freedesktop.systemd1.xml` at `ActiveEnterTimestampMonotonic` and `src/journal/journald-manager.c` at `Suppressed`; re-run `python3 -I -B tools/mori-oom-killers.py --selftest` and `--inputs <file>` on an A2 file
author: MoriR30 (L1); prose drafted by wave-1 seat DraftEntryC1; source ids and decision-table rows bound by the L1

# Which earlyoom invocation a send line belongs to — scope, the restart split and the A2a limit (round 30)

## Why this entry

Round 26 recorded earlyoom 1.9.0 as this host's userspace OOM killer and counted its send lines
(`corpus/knowledge/userspace-oom-killers-r26.md`); round 27 read which process it picks
(`corpus/knowledge/oom-victim-selection-r27.md`). Neither says which run of earlyoom a send line belongs to. The reader
`tools/mori-oom-killers.py` answers `KILLER_ACTED` (exit 1), `KILLERS_UNKNOWN` (exit 2) or `KILLERS_QUIET` (exit 0).

## Facts

### 1. One invocation, as the reader sees it

- earlyoom prints `earlyoom <version>` once at startup (S??? `main.c:161`); each occurrence opens an invocation, and a
  line belongs to the segment opened by the latest version line before it (`rule-text.md:89-90`).
- A restart writes a new version line, so "send, restart" and "send, no restart" are different shapes.
- For an active unit the scope is the time bound: lines at or after the start stamp are in scope
  (`rule-text.md:25-26`); without a usable stamp it is the segment after the last version line (Fact 2).
- Messages match after leading whitespace is stripped, prefix-anchored (`rule-text.md:27-36`); unmatched lines are
  ignored and no message text reaches the output (`rule-text.md:54-55`).

### 2. Bounded and unbounded scope

- `ActiveEnterTimestampMonotonic` is the CLOCK_MONOTONIC microsecond instant of the last entry into `active`, 0 when
  the transition was not recorded this boot (S??? `org.freedesktop.systemd1.xml:2780-2790`); non-zero bounds the scope
  inclusively (`c03-scope-boundary-exactly-at` acts, `c02-scope-boundary-one-microsecond-before` is quiet, `cases.json`).
- Missing or `0`: unbounded (A2-05, `rule-text.md:82-83`); every placeable line is kept, lines before the last version
  line move to the earlier count and `scope_complete` is false, as for any unplaceable record (`rule-text.md:39-40,114`).
- An active earlyoom with `scope_complete: false` is `KILLERS_UNKNOWN` unless positive evidence stands
  (`rule-text.md:44-52`): `r29-a2-10-zero-unbounded-mixed-sigterm` is `KILLER_ACTED` with `scope_complete: false`.
- `KILLERS_QUIET` needs no null read, no `unavailable` state, a complete verified-grammar scope for an active earlyoom
  (or `actions: null` for inactive/absent ones), and no send in scope; `state` names the readable ones (`rule-text.md:44-51`).

### 3. Where earlier-invocation sends go

- Sends and escalations outside the scope go to `earlyoom.earlier_invocation_send_lines` (A2-06,
  `rule-text.md:84-88`); a record without a numeric stamp is not counted there either (A2-10, `rule-text.md:114`).
- It changes the verdict only when earlyoom is not `active`: `inactive`, `absent` (`LoadState=not-found`), or a
  non-steady state mapped to `unavailable` (A2-02). Then a non-zero count is `KILLER_ACTED` (exit 1) while `actions`
  stays `null` (`a2-06-inactive-earlier-invocation-sends-acted`, `a2-09-removed-unit-single-sigterm-send`; probe:
  `failed` + stamped send → `KILLER_ACTED`, `state: unavailable`, earlier 1).
- For an `active` earlyoom it is report-only: `a2-06-active-earlier-invocation-sends-quiet` pins `KILLERS_QUIET` with
  `earlier_invocation_send_lines: 2` and `scope_complete: true` — the disclosed A2a limit (`rule-text.md:79-80`) and
  why the disputed shape abstains (Fact 4).

### 4. The disputed shape: active, stamp absent or 0, a real send, then a plain restart

- Shape: `ActiveState=active`, stamp absent or `0`, two or more version lines, a real (not dry-run) send or escalation
  before the last version line and none after it.
- Answer: `KILLERS_UNKNOWN`, exit 2, with `state: active`, `scope_complete: false`, `actions.sigterm: 0`,
  `actions.sigkill: 0`, `earlier_invocation_send_lines: 1`. The send is kept as an earlier count, not moved into
  `actions` (probe: invented inputs, `--inputs`, exit 2, those values).
- Why: the last segment cannot be bounded, so "quiet now" is unproven, and A2-06 makes an active unit's earlier sends
  report-only. The old answer was `KILLER_ACTED`; the round-29 harm ruling read both versions
  (`corpus/lessons/round-29-verifier-spotcheck.md:83-86`) and ruled **not harmed** (`:77-98`): A2-05/06/07 and round-26
  `contract.md:99-101,178-179` decide it, no older case pinned `KILLER_ACTED` (`:95`), the loss is A2a (`:98`).
- No older frozen file pins the plain-restart variant: the two active-unbounded cases carry no send line (`:95`).
  Nearest: `r29-a2-07-real-then-dryrun-zero-enter` (stamp `0`, real send, dry-run restart → `KILLERS_UNKNOWN`, earlier 1).

### 5. Dry-run is per invocation

- `dryrun mode enabled` is logged at startup (S??? `main.c:295`), so later sends in that segment describe intent: they
  move to `earlyoom.dryrun_send_lines`, `sigterm`/`sigkill` stay 0 and are never positive evidence (A2-04, A2-07).
- The split is at version lines, so one dry-run invocation does not zero another's real sends:
  `a2-07-earlier-dryrun-then-current-real` and `a2-07-three-invocations-dryrun-in-the-middle` stay `KILLER_ACTED`
  (probe: two in-scope segments, first dry-run → `dryrun_send_lines: 1`, `sigterm: 1` from the second).
- `earlyoom.dryrun` is true when any in-scope segment logged the line; counts stay per segment. Dry-run alone is
  `KILLERS_QUIET` (`a2-04-dryrun-sigterm-send-not-positive`; probe: `scope_complete: true`, `dryrun_send_lines: 1`,
  `sigterm: 0`).

### 6. Stamp-less records and suppression notices

- A record whose `__MONOTONIC_TIMESTAMP` is absent or not a number is left uncounted in both counts and makes the scope
  incomplete (A2-10, `rule-text.md:95-98,114`). A broken-stamp send is counted nowhere:
  `a2-10-malformed-action-line-uncounted` is `KILLERS_UNKNOWN`; positive evidence elsewhere still stands.
- A journald rate-limit notice reads `Suppressed N messages from <unit>` (S??? `journald-manager.c:1294`); an
  in-scope notice means earlyoom lines are missing, so `scope_complete` is false (A2-01, `rule-text.md:105`):
  `a2-01-suppressed-in-scope-active-quiet` is `KILLERS_UNKNOWN`.
- The check is scope-local: `a2-01-suppressed-before-scope-start` stays `KILLERS_QUIET` with `scope_complete: true`,
  and an in-scope action still wins (`a2-01-suppressed-in-scope-with-action`). A dropped line is not recoverable.

## Decision table

| shape | verdict | fields | case | sources |
|---|---|---|---|---|

## Limits

- A2a: an active earlyoom's earlier sends never change the verdict; the disputed shape is `KILLERS_UNKNOWN` with the
  send reported, not `KILLER_ACTED`. Disclosed, not a gap to re-litigate.
- A1a: incomplete-scope counts are lower bounds printed as counts, unlabelled (frozen `c04`); A3: no logger-heartbeat
  check, so a bounded scope with only a version line reads quiet (`c19-version-line-only`).
- A2-10: an uncounted record makes the result abstain but says nothing about its content; a broken-stamp send is
  counted nowhere. Suppression is scope-local: an earlier-segment notice does not lower the earlier count's label.
- Scope is the current boot only (`rule-text.md:25-26`); no cross-boot count, and a pre-boot start has no version line.
- No `MESSAGE` text, process names, command lines, uids or host prefer/avoid expressions in the output
  (`rule-text.md:54-55`); counts are log lines, not processes signalled or killed (A5).

## What it changes for mori

Before this round mori could count send lines but not say which invocation a line belonged to or why a restart splits
the evidence. Routing: bounded active send → acted; unbounded or suppression-damaged active scope → unknown; earlier
send with a non-active unit → acted, with an active one → reported (`SKILL.md` `Round30`).

## Not claimed

No host read; the shapes above are inputs, not observations. No claim that any restart happened; no tool, unit or
journal change.

## Adjacent

`corpus/knowledge/userspace-oom-killers-r26.md` owns the grammar and live counts;
`corpus/knowledge/structured-journal-scopes-r13.md` owns the timestamp mechanics; this entry owns the boundary.
```

## What the L1 still has to fill (C1 conditions)

1. Conditions 2 and 3: the table needs ≥8 data rows, each `case` id in **exactly one** of `cases.json`,
   `cases-supplementary.json`, `cases-a2.json` (`contract.md:32-35`). I checked the id sets with a throwaway `python3`
   intersection: 29 ids are duplicated between `cases.json` and `cases-supplementary.json` (the `c01`–`c18`, `c20`–`c23`,
   `c25`–`c27`, `c29`–`c31` families) and void for a row. Eligible pool, 36 ids: `c19-version-line-only`,
   `c24-nearmiss-kill-failed-without-colon`, `c28-oomd-active-quiet` (cases.json only);
   `c33-differing-thresholds-mem-and-swap`, `c34-escalation-only-incomplete-scope`,
   `c35-malformed-monotonic-timestamp` (supplementary only); all 30 `a2-*` ids (cases-a2.json only). That voids eight
   of my first picks (`c02`, `c03`, `c04`, `c05`, `c06`, `c07`, `c13`, `c18`); their shapes stay reachable through
   `a2-05-monotonic-zero-active-quiet`, `a2-06-active-earlier-invocation-sends-quiet`,
   `a2-06-inactive-earlier-invocation-sends-acted`, `a2-02-earlyoom-activestate-failed`, `a2-01-suppressed-*`,
   `a2-04-dryrun-*`, `a2-07-*`, `a2-09-*`, `a2-10-*`, and the six single-file `c` ids. All 36 sit in files the C2
   condition-2 claim runs clean at the entering tip (`contract.md:62-63`); I did not run them one by one, so condition 3
   still needs the Probe seat's per-case tool run.
2. Condition 4: bind the four `S???` slots to real S156+ ids (or existing rows where a fact already has one), add a Gate
   line and `corpus/evidence/sources-r30/S###.txt` per id, and re-check my sha256/line numbers: the source seat's bytes
   are the evidence, not mine.
3. Conditions 1 and 5: header lines are present above; `SKILL.md` needs ≥3 `Round30` rows naming the entry path.
4. Prose-only case mentions are allowed (only table `case` cells are restricted): the draft cites `c02`, `c03`, `c04`,
   `c19`, `r29-a2-07-real-then-dryrun-zero-enter` and `r29-a2-10-zero-unbounded-mixed-sigterm` outside the table. If the
   L1 wants strictly eligible ids even in prose, swap `c02`/`c03` for `a2-06-*`/`a2-05-*` wording.

## Findings and caveats

- `failed` and `activating` states plus a stamped send read `KILLER_ACTED` (probe 5): the `state != active` test makes
  `unavailable` behave like inactive for the earlier count, though A2-02 alone would read the same state as
  `KILLERS_UNKNOWN` when the count is zero. Worth a table row.
- The suppression check is scope-local by construction: an earlier notice leaves `scope_complete` true and the earlier
  count unflagged (probe 12). Stated as a limit; it is not in the A2 disclosure list.
- `ActiveState=absent` is not the `absent` state; only `LoadState=not-found` maps to `absent`. An invented
  `ActiveState=absent` reads `unavailable` (seen in a discarded probe draft, not used here).
- `cases-a2-r29.json` is excluded from C1 rows (`contract.md:32-35`); my prose uses it once, illustratively, and says so.
- Peer `MoriR30.ReviewC1Reachability` reported 29 duplicated ids and 36 eligible; my own set comparison agrees exactly.
- The entry block is 118 lines (cap: under 120). Adding table rows or re-wrapping the header will push it over; measure
  again after pasting (`awk` on the fenced block).
- The draft does not cite `tools/fixtures/mori-oom-killers/cases-a2-r30.json`: C1 rows may not cite it
  (`contract.md:32-35`) and the entry should not depend on C2's outcome (CriticC1Design F11, same wave). The §4
  verdict/fields stand on the older cases cited plus the probe.
- The `sha256` values in the draft's `source:` line are my fetches (times above). If a source seat's bytes hash
  differently, its gate row wins and the entry's `source:` line must be corrected, not the gate.
- No install or update was needed; nothing was written outside this report and
  `/fast/scratch/hyaku/mori-r30/DraftEntryC1/`. Out of scope and untouched: tool, fixtures, blindness gate,
  `SOURCES.md`, lesson, `SKILL.md`, `SCORECARD.md`, counters, host units/journal/settings.

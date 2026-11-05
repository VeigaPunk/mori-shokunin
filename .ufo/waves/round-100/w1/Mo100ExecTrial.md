# Mo100ExecTrial — C1 live trial on real transcripts (counts only)

Seat: Mo100ExecTrial (executor), mori round 100 w1, 2026-11-05. Scope: run the entering
(d1bd1b339b894de0249b0f60702dff9962da88d9) and landing (5e2bcf2c487e377b51287c587144bdde5b233f8f)
`tools/mori-seat-terminal.py` on 4 real session directories and compare per-seat classes. Counts only:
the parser read `totals`, per-seat `class`/`kind`/`terminal_ms`/`error_status`/`error_code`/`reason`
fields from each tool's stdout JSON; no message text, content, usage or credentials was read, copied
or printed. Both trees extracted with read-only `git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive <rev> | tar -x -C $S/{enter,land}`.

## Directory selection
The 19 lane-named dirs under `~/.omp/agent/sessions` matching `*-Projects-shokunin*` are empty except
`-Projects-shokunin-kotodama-shokunin` (1 jsonl); the fleet's transcripts live in the per-session
subdirectories of `-Projects-shokunin` (whose absolute paths contain `-Projects-shokunin`). I picked
the 4 largest such subdirectories with fewer than 2000 jsonl files (largest eligible, the 5313-file
2026-11-03 dir, was skipped by the <2000 rule). `find DIR -name '*.jsonl' | wc -l`:

```
/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-29T19-55-04-670Z_01a1893a-f45e-72c7-a829-ad10ad1edff4 1831
/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-26T03-41-55-460Z_01a1764c-ed84-730d-b290-e516d052c218 1669
/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-27T03-03-17-731Z_01a17b4f-ebe3-74c7-b154-6de929023b00 1134
/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-30T17-41-25-086Z_01a18de6-f1de-7233-9dc0-42c883f181ac 107
```

Command per dir/tree (enter run immediately followed by land run on the same dir):
`python3 $S/<tree>/tools/mori-seat-terminal.py --sessions-dir DIR --max-files 5000 --settle-seconds 900`.
Slowest single run 134.5 s; no run exceeded 10 minutes, so no smaller-directory fallback was needed.

## Per-directory totals (entering → landing)

D1 2026-10-29T19-55 (1831 files, files_scanned 1831/1831, rc 1/1, 126.1 s / 120.2 s):
```
totals_enter: aborted=4 completed=44 dead_error_other=46 dead_quota=92 dead_rate_limit=45 error_unsettled=0 incomplete=1600 unavailable=0
totals_land:  aborted=4 completed=44 dead_auth=22 dead_error_other=24 dead_quota=92 dead_rate_limit=45 error_unsettled=0 incomplete=1600 unavailable=0
```

D2 2026-10-26T03-41 (1669 files, files_scanned 1669/1669, rc 0/0, 134.5 s / 126.1 s):
```
totals_enter: aborted=33 completed=104 dead_error_other=0 dead_quota=0 dead_rate_limit=0 error_unsettled=0 incomplete=1486 unavailable=46
totals_land:  aborted=33 completed=104 dead_auth=0 dead_error_other=0 dead_quota=0 dead_rate_limit=0 error_unsettled=0 incomplete=1486 unavailable=46
```

D3 2026-10-27T03-03 (1134 files, files_scanned 1134/1134, rc 1/1, 85.5 s / 85.1 s):
```
totals_enter: aborted=0 completed=57 dead_error_other=41 dead_quota=0 dead_rate_limit=0 error_unsettled=0 incomplete=1036 unavailable=0
totals_land:  aborted=0 completed=57 dead_auth=0 dead_error_other=41 dead_quota=0 dead_rate_limit=0 error_unsettled=0 incomplete=1036 unavailable=0
```

D4 2026-10-30T17-41 (107 files, files_scanned 107/107, rc 0/0, 7.2 s / 8.6 s):
```
totals_enter: aborted=62 completed=8 dead_error_other=0 dead_quota=0 dead_rate_limit=0 error_unsettled=0 incomplete=37 unavailable=0
totals_land:  aborted=62 completed=8 dead_auth=0 dead_error_other=0 dead_quota=0 dead_rate_limit=0 error_unsettled=0 incomplete=37 unavailable=0
```

Schema `mori-seat-terminal-v1` on all 8 runs; `dead_auth` key present in every landing totals object,
absent from entering totals. main_sessions=0 everywhere (all entries are seats, not main sessions).

## Transitions
Seats whose class changed: D1 22, D2 0, D3 0, D4 0 — total 22. Transition table (from→to, count):

```
dead_error_other -> dead_auth : 22   (D1 only)
```

Every one of the 22 moves was between an identical terminal record (same `terminal_ms`,
`error_status`, `error_code` in both trees) — i.e. reclassification only, not a changed last record.
Falsifier accounting across all 4741 scanned files × 2 trees: other-transition falsifiers 0;
settle-window flips (error_unsettled↔dead on same record) 0; seats whose terminal record changed
between the paired runs (`terminal_ms`/status differs) 0; seats appearing or disappearing between
paired runs 0. In D1, `dead_error_other` moved exactly −22 and `dead_auth` +22; no other totals key
moved in any directory. D3's 41 `dead_error_other` seats carry no auth evidence and correctly stayed
put — the class only reclaims seats with auth evidence, as claimed.

Unrun checks (not my assignment): `count-c1.py` battery/selftest/r17gate/registry/sourced families,
`count-c2.py` census, controls-r100.py, and any counter on seeds — unrun by this seat. Tool/r17-gate
diff sizes for context: 155 and 3 changed lines (plain `diff` of the archived copies).

VERDICT C1-live holds: across 4 real session dirs (4741 transcripts, both revisions), the only
observed class transition was dead_error_other→dead_auth (22 seats, all on identical terminal
records); no other seat moved class, appeared or disappeared; totals agree with the by-construction claim.

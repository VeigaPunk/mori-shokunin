# Round 53 verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)
lane: mori-shokunin · round 53 · closed 2026-10-27
base `20edafa59b38dac1ca358893f0259b1f436372d3` → tip `28401324ca5e0205645490d8e538b30d5ef4d1bf`
(branch `master`, remote verified); receipts measured at `0b36d23e596276c70725873621fe15a28c87189f`
(`git diff --name-status 0b36d23e 28401324` → only the five added receipt files under
`.ufo/waves/round-53/evidence/`). Independent measurements below were run by this closure over a
`git archive 28401324` extraction in `/fast/scratch/hyaku/closure-mori-r53/` (removed after closure).

## Step-1 conformance

- Report `.ufo/reports/round-53/mori.md` committed on the fleet repo by the lane identity:
  `git log --format='%an <%ae> %H %ci' -- .ufo/reports/round-53/mori.md` → `mori-shokunin <mori@shokunin.local>
  b27a71b07c67b2f7a37782d1b3c6dd05959b9191 2026-10-27 00:58:26 -0300`, after the lane tip commit
  (`28401324`, 00:57:23 -0300) — lands last.
- `SHONEN` heading present with four `[~]` lines, one per box, each with a pointer.
- Cited lane commits `20edafa5 f4da3fd4 2a4213bf 95cf78ee fd86307a 0df80303 34d97cd3 7b90a3c6 0b36d23e
  28401324` all resolve and `git merge-base --is-ancestor <h> master` holds for each (10/10). The round-52
  erratum hash `aacd7a83027cdee8e950a2c39d490feaed3be13c` resolves on the fleet repo and equals
  `git log --format=%H -1 -- .ufo/reports/round-52/mori.md`.
- `scripts/hyaku/jj-lane.sh state` → `branch=master local=remote=28401324… ahead=0 behind=0 head=detached
  tracked=0 untracked=0`; `git status --porcelain` → 0 lines (`.ufo/waves/round-53/__pycache__` is ignored by
  `.gitignore:3`). No uncommitted round work; pushed.
- Prompt `.ufo/prompts/mori-round-53.md` (633 lines; committed by the lane identity, `ce4c5e94` attempt 1 and
  `bbebff81` attempt 2) carries §1 MISSION/AXES binding, §2 claims, §2b frontier step, §3 L2 floor, §4 report
  contract (path, sections, SHONEN heading), §5 commit-then-push, push scope, L0 side channel, plus the hyaku
  addendum §6 and scratch discipline §7.
- Driver digest (watchdog.log is mutable; copied):
  `2026-10-26T22:10:05-03:00 launch mori round=53 pgid=1612126 driver=hyaku-inline attempt=1`;
  `2026-10-27T00:16:15-03:00 lane-dead-no-report mori round=53; retry same round (… attempt 1 L1 MoriR53 died in the
  orchestrator session exit 2026-10-26 23:57:36 -03 (SIGHUP during an operator omp update); no report; w1 66/67
  settled (66 outputs recovered), integration drafts uncommitted; work salvaged to the lane branch 0df80303)`;
  `2026-10-27T00:16:30-03:00 launch mori round=53 pgid=890907 driver=hyaku-inline attempt=2`;
  `2026-10-27T00:59:05-03:00 complete mori round=53; hyaku-inline attempt=2`.
- Round shape: w1 spec 67 items (reviewer 12, critic 12, executor 20, mutation-tester 3, sentinel 4, scout 2,
  connector 2, scribe 10, revenger 1, simplifier 1 — `jq` over `w1-spec.json`); `w1-results.json` 67 results, 66
  with output, the empty one `Mo53RevLedgerProse` (re-dispatched as `Mo53a2RevLedgerProse`); `a2r1-results.json`
  8/8 with output. Total 75, inside the 64–128 band.
- Status: `ok` — a real report with checkable committed work, not a marker.

### Conformance defects (status-neutral)

- D1 (attribution): the salvage commit `0df80303` was made by the hyaku orchestrator under the lane identity
  (`author=committer=mori-shokunin <mori@shokunin.local>`), not by a lane L1. Disclosed in its subject, the report
  and LOG; attempt 2 re-verified the salvaged bytes before citing them (`evidence/c1-at-salvage.txt`,
  `evidence/c2-at-salvage.txt`). Recorded, not rewritten.
- D2 (measured revision in SCORECARD): the round-53 C1 and C2 After cells (`SCORECARD.md:2796-2797`) cite the
  at-salvage receipts (R = `0df80303`), not the final integration tip `0b36d23e` that the report measures; the cells
  defer to the report for the at-landed re-run. The numbers match the receipt cited (QUALITY 146 holds) and are
  token-identical to `c1-at-landed.txt`/`c2-at-landed.txt`, so nothing is wrong, but the scorecard row names a
  revision that is not the landed one. Route: an appended note naming the at-landed receipts.
- D3 (inherited, standing): tracked lane-root files `0`, `base.c`, `main.c`, `meminfo.c`, `oom_kill.c`, `sd-main.c`,
  `user@.service.in` and the empty `--repo/` dir, named by the report as inherited (2026-10-22/23) and untouched.
  Still debt: the lane should remove or relocate them under a named entry.

## Claims — per-claim re-check

Re-measured = this closure ran its own plain measurement over committed bytes; evidence-verified = the lane's
counter/gate receipts read (the counters and the tool were not executed, per §Gate standard).

### C1 — freshness: 46 v7.2-pinned claim rows re-verified at Linux v7.3 — **re-measured + evidence-verified: improved**

- Frozen bytes: `sha256sum -c --quiet .ufo/waves/round-53/evidence/freeze-sha256.txt` over the tip extraction →
  rc 0 (33 entries); `git diff --stat f4da3fd4 28401324 -- contract.md count-c1.py count-c2.py freeze-sha256.txt` →
  empty.
- Ledger re-derivation (own Python, whitespace-collapsed substring test against the committed v7.3 copy of each
  row's `S###`, v7.2 quotes from `evidence/c1-scope.txt`): `ledger rows 46`, `held 44`, `absent 2`, `holds 46`,
  `changed 0`, mismatches `[]` (entry, path, derived status, quote located; held rows carry the v7.2 quote itself),
  scope covered `True`. The two `absent` rows are `0fbd62f51ce8` and `d7a1dc88dcb3` (S510, the MAP_NORESERVE
  block now `vma_flags_set(&vma_flags, VMA_NORESERVE_BIT)`, `mmap.c.v7.3:563-570`).
- Vote arm (own parse of `w1/Mo53Fr01.md`–`Mo53Fr12.md`, unfenced `RECHECK <h> <word>` lines, last wins): 12 voter
  files, 138 RECHECK lines, every one of the 46 hashes carries 3 `holds` voters, 0 dissent, no voted hash outside
  scope.
- Source bytes: all nine v7.3 copies (S502–S510) re-fetched today from git.kernel.org cgit
  `plain/<path>?h=v7.3` are byte-identical to the committed copies (sha256 prefixes `bc178ff511e0 c50205bc1997
  d6c5807421a6 277e99e23ecc 767ab88153c4 f81feb3dfca5 4dfcce2b8fa8 d7bf787c910d 8e51fb1c10fe`).
- Lane receipt: `evidence/c1-at-landed.txt` → `C1=met scope=46 rows=46 matched=46 status_ok=46 quote_ok=46
  source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=46 dissent=0
  rev=0b36d23e…`, exit=0; before `evidence/control-c1-do-nothing.txt` → `C1=unmet … failed=ledger_absent,pins`,
  exit 1; counter selftest `C1_SELFTEST pass=37 fail=0` (`evidence/selftest-c1.txt`). My numbers agree with
  every reported token.

### C2 — coverage (capability): the commit ledger as a runway read by overcommit mode — **re-measured + evidence-verified: improved**

- Before→after surface: `git ls-tree --name-only <r> tools/mori-commit-runway.py` → absent at `20edafa5`, present at
  `28401324`; `git grep -lE 'CommitLimit|Committed_AS' <r> -- tools/` → 0 files at `20edafa5`, 2
  (`tools/mori-commit-runway.py`, `tools/fixtures/mori-commit-runway/cases.json`) at `28401324`.
- Independent oracle (own Python from the frozen contract formula and the kernel copies — `vm_commit_limit`,
  `__vm_enough_memory`, `mm_compute_batch`; not the counter's REF): over the 26 committed cases in `cases.json`
  (verdicts HEURISTIC 3, UNLIMITED 1, OK 8, LOW 3, UNKNOWN 11) every numeric case agrees on every field
  (`agree 15 disagree 0`); the 11 UNKNOWN cases are malformed inputs (duplicate key, unit-less line, reversed /
  overlapping / out-of-ceiling CPU lists, 30-digit value, …) that my lenient parser partly accepted and the tool's
  strict parser rejects by design — I agree they are unreadable. The 54 seeded fixtures are counter-generated and
  are evidence-verified only.
- Registry: `SKILL.md:1209` row (gate; verdict map 0 clean / 1 failed / 2 could-not-evaluate; selftest
  `--selftest`), `## Round53` at `SKILL.md:1178`. Capability row `round-53 C2` in `SCORECARD.md` `### capabilities:
  first demonstrated round 53`.
- Lane receipts: `evidence/c2-at-landed.txt` → `C2=met tool=present selftest=pass n=31 fixtures=80 agree=80
  disagree=0 registry=ok live=ok rev=0b36d23e…`, exit=0; before `evidence/control-c2-do-nothing.txt` →
  `C2=unmet tool=absent … failed=registry,tool_absent`, exit 1; `evidence/selftests/mori-commit-runway-a2.txt` →
  `MATCHER: rejected 26/26 corrupted expectations`, `MORI_COMMIT_RUNWAY_SELFTEST: PASS 31/31`, exit=0, git archive of
  `0b36d23e`; counter selftest `C2_SELFTEST pass=30 fail=0`.
- Knowledge behind the band: a non-author reviewer seat this closure dispatched read
  `corpus/knowledge/commit-runway-read-r53.md` and the SKILL `## Round53` rows against the committed kernel copies:
  15 kernel claims checked (batch formula and floor, fold at `|delta| >= batch`, `percpu_counter_read_positive`,
  exact-sum `Committed_AS`, policy-write recompute order, mode-0/1 semantics, reserves, v7.2 = v7.3
  `mm_compute_batch`, dying-CPU generic batch), all correct, every anchor resolves; ruling "no false or unmarked
  kernel claim".

### No-harm

- `git diff --numstat 20edafa5 28401324` on lane-owned files: LOG +50/−0, PROVINCE +56/−0, SCORECARD +77/−0,
  SKILL +33/−0, QUALITY +98/−0, README +22/−0, SOURCES +17/−1 (the −1/+1 is S499 `used-by` only, cell-diffed),
  SHONEN 4/4 (the four `[~]` pointers refreshed). No axis score changed (`## Round 53`: "No score change is claimed
  by the lane"). Pin check at `0b36d23e`: `PIN_CHECK=met tally_pins=37 … mismatches=0`
  (`evidence/pin-check-at-landed.txt`).

## Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| freshness | improved | C1 re-measured: 46/46 rows re-derived at v7.3, 3 voters each, copies byte-equal to cgit today |
| coverage | improved | C2 re-measured: commit ledger read by a mori tool (0 → 2 files), oracle 15/15, capability row |
| depth | unchanged | not claimed; band entry and SKILL rows added and checked correct, no score moved |
| operability | unchanged | not claimed; new gate's selftest 31/31 evidence-verified, no score moved |
| calibration | unchanged | not claimed; QUALITY 144–147 added with lesson pointers |
| adjacency | unchanged | not claimed; PROVINCE append-only, boundary sentence corrected in-round |

## Discernment spot-check (`corpus/lessons/round-53.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S510 `mm/mmap.c` v7.3 | admit (tier A code) | `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/mmap.c?h=v7.3` fetched 2026-10-27: 51299 bytes, sha256 `8e51fb1c10fe…` = committed copy; lines 563-566 read `if (flags & MAP_NORESERVE) { /* We honor MAP_NORESERVE if allowed to overcommit */ if (sysctl_overcommit_memory != OVERCOMMIT_NEVER) vma_flags_set(&vma_flags, VMA_NORESERVE_BIT);` | agree | primary source at a pinned tag, quote verbatim at the cited lines (20 words ≤ 25), and it is the row that carries the real v7.2→v7.3 drift |
| S514 `mm/mm_init.c` v7.3 | admit (tier A code) | cgit `plain/mm/mm_init.c?h=v7.3` fetched today: sha256 `678410005f88…` = committed copy; `:198-199` read `s32 nr = num_present_cpus(); s32 batch = max_t(s32, nr*2, 32);` | agree | pinned primary source; quote verbatim (10 words); the reviewer seat confirmed `mm_compute_batch` v7.3:195-214 is byte-identical to v7.2:191-210 |
| raw.githubusercontent.com v7.3 locator | reject | `https://raw.githubusercontent.com/torvalds/linux/v7.3/{mm/util.c,include/linux/mman.h,mm/mmap.c}` fetched 2026-10-27: `mm/util.c` → HTTP 429 (324 bytes), `mman.h` and `mmap.c` → 200 with bytes equal to the cgit copies | agree | the per-path throttling the lane recorded reproduces today (one 429 in three), so it cannot be the stable locator of a row; the flip (all paths 200 and equal) is correctly scoped to a second locator, never a new row |
| kernel.org rendered `latest` vm.html | reject | `https://www.kernel.org/doc/html/latest/admin-guide/sysctl/vm.html` → 200, 69002 bytes, `<p class="blurb">7.3.0</p>`, carries "rejects obvious overcommits" (1 hit) | agree | `latest` is unpinned; S507's tag copy holds the same text. Note for the lane: the flip's release-pinned URL `/doc/html/v7.3/admin-guide/sysctl/vm.html` answers 200 today |

New-row quote re-open: S510 and S514 above (both new this round), plus S511 `mm_init.c.v7.2:199-200` "For policy
OVERCOMMIT_NEVER, set batch size to 0.4% of (total memory/#cpus), and lift it to 25% for other policies" — verbatim
across the comment's line break, 19 words. All thirteen new rows (S502–S514) re-fetched from cgit today are
byte-identical to their committed copies.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → `mori ok …/SOURCES.md`,
rc 0, 23 W04 (the standing duplicate-URL warnings, the same count as `evidence/census-start.txt` and
`census-end.txt`). Rows `grep -cE '^ {0,3}\| *S[0-9]{3,} ' corpus/SOURCES.md` → 274 at `20edafa5`, 287 at
`28401324`; malformed rows 0; duplicate ids none.

## Trend verdicts

- **expansion: improved** — a new admitted entry on runway ground no mori tool read
  (`knowledge/commit-runway-read-r53.md`, sources S511–S514 `mined`; README `## Round-53 coverage additions`), a tool
  and a capability row demonstrated running (selftest 31/31, live `COMMIT_HEURISTIC` on this mode-0 host).
- **quality: improved** — 46 stale-by-release rows re-verified at v7.3 with none failing; the two respelled quotes are
  marked in the ledger, not left standing; the band entry's 15 kernel claims check out.
- **discernment: improved** — this spot-check agrees with the gate on both admits and both rejects, and the round-52
  closure disagreements (D1, D2) became grounded QUALITY criteria 146 and 147, each citing its lesson.

## SHONEN note (for the operator; promotion is operator-owned)

The four `[~]` boxes point at committed, re-runnable evidence (SKILL `## Round53` tables, `LOG.md:2841-2888`, the
selftest receipts, `PROVINCE.md:451-456`); they look checkable by a non-author. This closure writes no `[x]`.

## Routed defects (the lane fixes next round)

1. D2 above: append a SCORECARD note naming `evidence/c1-at-landed.txt` and `evidence/c2-at-landed.txt` (R =
   `0b36d23e`) as the landed measurement of the round-53 rows.
2. D3 above: the tracked lane-root strays (`0`, `base.c`, `main.c`, `meminfo.c`, `oom_kill.c`, `sd-main.c`,
   `user@.service.in`, `--repo/`) — remove or relocate under a named LOG entry.
3. The named limits routed to `Planned (round 54)` stay open: filename-keyed voter identity, the C2 exit-code arm
   with no selftest, no live mode-2 leg on this host, S502–S514 anchor corrections resting on one seat.
4. Lead: the release-pinned rendered docs (`/doc/html/v7.3/…`) now answer 200 — eligible as a second locator for
   S507 under the lane's own flip condition.

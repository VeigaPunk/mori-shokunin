# Round 27 — lesson (mori, L1 MoriR27)

author: MoriR27 (L1), from wave-1 seat reports under `.ufo/waves/round-27/w1/` (the mistake-mining scribe seat died at
spawn; this text is the L1's).
Contract: `.ufo/waves/round-27/contract.md` (declared at `761b4cdb`; amendment W1 withdrew C2 before any C2 data).

## What the round learned

- **earlyoom picks by score, not by size.** It keeps the highest `/proc/<pid>/oom_score` it computes, adds 300 for a
  `--prefer` name match and subtracts 300 for `--avoid`, and only `--sort-by-rss` makes size the key
  (`corpus/knowledge/oom-victim-selection-r27.md` Fact 1).
- **The kernel's exported score is `(1000 + badness * 1000 / totalpages) * 2 / 3`**, range 0–2000, and an
  `oom_score_adj` is scaled by memory size, not added as points. `proc.rst` and the man page disagree with the code in
  three places (Fact 2).
- **The fleet's 200 comes from systemd, not the harness.** The per-user manager runs at 100 and gives its children
  100 more; oh-my-pi v18.12.6 and Bun 1.4.3 never set the value (Fact 3, S130, S132). The floor is 100, not a
  ratchet: an unprivileged process lowered itself from 500 to 199 (wave-1 CriticInheritProbe).
- **One earlyoom send to `omp` is a fleet-wide event.** The in-session seats live inside one `omp` process, which held
  the second-highest score on the host; in boot -1 earlyoom signalled one `omp`-class process, 27 `python`-class and
  11 others, and 8 of its 39 send lines carry a score only a prefer match can produce (Facts 4–5).
- **No fleet record can say a seat was OOM-killed.** Lane-dead lines carry no cause and are written at detection time,
  which after a reboot is minutes into the next boot (Fact 6, wave-1 ConnFleetSeatKillPath).

## Mistakes

- **M1 — round work left uncommitted at the final commit (class: late seat output outside committed bytes).**
  Evidence: at round-27 start, `git -C <lane> status --porcelain` listed four round-26 wave-2 files (one modified,
  three new) under `.ufo/waves/round-26/w2/`; the round-26 report cited one of them (routed D1,
  `corpus/lessons/round-26-verifier-spotcheck.md:40-43,179-182`). Captured-by: none (no QUALITY criterion named the
  wave directory at the final commit). Fix: the four files are committed at `126e192d` after the retention scan and
  a uid redaction (one line in `ReviewEntryOomdFacts.md`); QUALITY 80. Shown able to fail: the same command at round
  start printed four lines under `.ufo/waves/round-26/` (session start record, this lesson).
- **M2 — SOURCES rows corrected in place (class: protocol rule with no enforcing check).** Evidence: round 26 changed
  S124's `scope`, `anchor` and `teaches` cells in place (routed D3; wave-1 ReviewS124Supersede found the `scope` and
  anchor changes were never logged). The new check found five more rows changed in place in rounds 24–25: S090
  (anchor, teaches), S093 (anchor), S096 (teaches), S097 (anchor, teaches), S101 (teaches), each against its
  first-published text at `df4db54` or `90ed9b7`. Captured-by: CORPUS.md Rules 2 states the rule; the census does not
  check it (ReviewS124Supersede falsifier D: an in-place edit validates at exit 0). Fix: S124 restored to its
  first-published cells and corrected by new row S133 (`supersedes S124 —`); QUALITY 81 with the committed check
  `.ufo/waves/round-27/check-row-identity.py`. Shown able to fail: at `ef9dbee1` and at `fc09f96c` it prints
  `changed=6`, exit 1; at a bad revision `bad_rev`, exit 2. The five round-24/25 rows are routed to wave 2 for
  re-opening before their restore and superseding rows; their disposition is recorded below.
- **M3 — a dispatch prompt that invited a privacy leak (class: prompt-induced leak the retention scan cannot see).**
  Evidence: the wave-1 item `HostUnitOomAdjust` asked for "the unit names" along the shell's cgroup path; the report
  carried the operator's uid digits in eight places (`user-<uid>.slice`, `user@<uid>.service`), and the retention
  scan read 0 hits on that file (wave-1 CriticPrivacyPlan). The same wave's send-line grammar in the item
  `HostBootSendClasses` was wrong (it omitted the `oom_score_adj` field), which would have pushed an executor to print
  raw lines while debugging. Captured-by: none; the frozen retention policy calls its classes "a recall floor, not a
  privacy proof" (`.ufo/waves/round-18/frozen/c1-policy.json`). Fix: the eight places (and one pid each in two other
  reports) were redacted before the first commit of those reports; QUALITY 82. Shown able to fail: the lint pattern
  in QUALITY 82 matched 8 lines in the unredacted `HostUnitOomAdjust.md` (L1 redaction run, 2026-10-22T15:57Z). The pattern is
  not new to the lane: `git grep -cE 'user-[0-9]{3,}\.slice|user@[0-9]{3,}\.service' 126e192d` counts 358 lines in 118
  tracked files from earlier rounds (round 7 onward), so QUALITY 82 is prospective; whether to rewrite those files or their
  history stays with the operator, as for the round-25 retention history. This round adds none.
- **M4 — a claim whose substance was one seat on a degraded route (class: single point of failure in a claim).**
  Evidence: C2's value was that `WriteA2Cases` wrote the cases blind to the tool; the seat died at spawn with
  `Error: No model selected.` (7 of 34 wave-1 seats died the same way: every scribe, executor and mutation-tester
  seat). Dead seats are never replaced, so C2 was withdrawn (contract amendment W1). Captured-by: none; the route
  notice came at 15:40Z, before dispatch, and the plan did not move the case-writing to a healthy role. Fix (process):
  when a route notice names a role, a claim that rests on one seat of that role is re-planned before dispatch, not
  after. No QUALITY criterion: the rule is about dispatch timing, and this round cannot show it able to fail.

## Gate (new SOURCES rows, opened 2026-10-22)

Quotes are located and at most 25 words; the full Gate blocks (sha256 of every fetched file, more quotes) are in the
named wave-1 seat reports.

| Row | URL | Accessed | Located quote | Decision |
|---|---|---|---|---|
| S127 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c (with `include/uapi/linux/oom.h` and `kernel/fork.c` at v7.2) | 2026-10-22T15:46:35Z | `base.c:596-597` "points = (1000 + badness * 1000 / (long)totalpages) * 2 / 3;" | admit, A, mined (SrcProcBaseOomScore) |
| S128 | https://man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html ; …/proc_pid_oom_score.5.html | 2026-10-22T15:46:37Z | adj page `:104-105` the range -1000 to +1000; `:86-88` "root processes are given 3% extra memory" (no v7.2 implementation) | admit, A, mined (SrcManProcOomScoreAdj) |
| S129 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-system.conf.xml (with `systemd.exec.xml`) | 2026-10-22T15:46:34Z | `:305-306` "if the service manager is run for an unprivileged user, in which case this defaults to the service manager's OOM adjustment value plus 100" | admit, A, mined (SrcSystemdExecOomScoreAdjust) |
| S130 | https://raw.githubusercontent.com/systemd/systemd/v262/units/user@.service.in (with `src/core/main.c` and commit `ce7de0ba`) | 2026-10-22 | `user@.service.in:35` "OOMScoreAdjust=100"; `main.c:3063` "b = saturate_add(a, 100, OOM_SCORE_ADJ_MAX);" | admit, A, mined (SrcSystemdUserService; `main.c` opened by the L1, sha256 `5ecdca43…aae3`) |
| S131 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.default (with the v1.9.0 tag tree) | 2026-10-22T15:46:30Z | `:5` `EARLYOOM_ARGS="-r 3600"` | admit, A, mined (SrcEarlyoomManpageOptions) |
| S132 | https://raw.githubusercontent.com/can1357/oh-my-pi/v18.12.6/crates/pi-natives/src/shell.rs (with Bun `bun-v1.4.3` spawn sources) | 2026-10-22T15:51Z | `shell.rs:134` "/// Options for running a shell command."; `c-bindings.cpp:58` "return setpriority(PRIO_PROCESS, pid, priority);" | admit, A, mined (SrcOmpBunOomAdj; whole-tree negative for `oom_score_adj`) |
| S133 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml (with `systemd-oomd.service.xml`) | 2026-10-22 | `:1545-1546` "When set to auto, systemd-oomd will not actively use this cgroup's data for monitoring and detection." | admit, A, mined — `supersedes S124 —` (ReviewS124Supersede, routed D3) |
| S134 | https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/eval/agent-bridge.ts | 2026-10-22 | `:210` (agent() registers with the job manager without a capacity check; quote in `.ufo/waves/round-27/w1/ReviewR3SkillRows.md` §3) | admit, A, mined (drafted round 26, DraftHygieneKnowledge §4.5; re-opened by ReviewR3SkillRows, routed R3) |
| S135 | …/45c35e40…/packages/coding-agent/src/task/workpool.ts | 2026-10-22 | `:175,363` (pool and batch registration; ReviewR3SkillRows §3) | admit, A, mined (as S134) |
| S136 | …/45c35e40…/packages/coding-agent/src/task/index.ts | 2026-10-22 | `:1191-1236` (per-spawn refusal inside one batch; ReviewR3SkillRows §3) | admit, A, mined (as S134) |
| S137 | https://raw.githubusercontent.com/rfjakob/earlyoom/750a7c0d97bb01c1bdf126fd6bf5722da17e8998/main.c (with the `commits?path=main.c` query) | 2026-10-22 | `:352` "  --kernel-oom              use kernel OOM killer via /proc/sysrq-trigger\n" | admit, A, mined (ReviewS117, routed D2) |
| S138–S141 | https://github.com/can1357/oh-my-pi/commit/944d7f8d8d44d889b77f1865f394afd1dfb48c86 ; …/e398f83163723b76283c2a05b08806ba37f0773f ; …/6962d5cd2ef157ebf9f415acd58b8744f66400d8 ; …/c4a2441d8f9195de810b3492be5bf5673cecf9c9 | 2026-10-22 | S140 `sdk.ts:1949` "maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings) ?? 100)," | admit, A, mined (drafted round 26; re-opened and re-verified by ReviewR7Knowledge, routed R7) |

Re-opened, no new row (each adds no row because a row already holds the same bytes): S003 `mm/oom_kill.c` (sha256
`452f1348…6b4e`), S082 `proc.rst` (`e760f716…d126`), S092 `cgroup-v2.rst` (`a9433bb0…b7ad`), S114 README and S115
MANPAGE (`23411dbf…74dd`, `cc48b02e…dfeda`), S118 `kill.c` (`b32e0fad…0bf3`), S119 `main.c` (`08656b0b…d0e4`), S120
`earlyoom.service.in`, S125 the sibling entry (`ecafdcdd…cd25`). New anchors on those files are cited in the entry
body, not written into the rows (CORPUS.md Rules 2).

Not admitted as rows: the optional separate rows drafted for `include/uapi/linux/oom.h` (folded into S127) and
for the v7.2 `cgroup-v2.rst` (already S092); a new row for the sibling file (already S125).

### Row changes logged old → new

- `used-by` gained `corpus/knowledge/oom-victim-selection-r27.md` on S003, S082, S092, S114, S115, S118, S119, S120
  (old values: S003 the four r12 entries; S082 `corpus/lessons/round-23.md`; S092 `corpus/knowledge/system-pressure-r24.md,
  corpus/lessons/round-24.md`; S114, S115, S118, S119, S120 `corpus/knowledge/userspace-oom-killers-r26.md`).
- S124 `scope`, `anchor` and `teaches` restored to the first-published text at `327fbcc` (old = the round-26 edit,
  new = the original); the exact three old → new cells are in `.ufo/waves/round-27/w1/ReviewS124Supersede.md` "Draft
  (b)". The corrected teaching moved to S133. Status stays `mined` (the census accepts only `queued`, `mined`,
  `rejected`).

## Routed defects: disposition

| Item | Disposition | Pointer |
|---|---|---|
| r26 D1 uncommitted wave-2 reports and the tally | fixed: the four files committed at `126e192d` (uid redacted in one line). Corrected wave-2 tally: 34 dispatched; 17 returned with a committed report; 1 returned with its report withheld by the round-26 privacy rule (`RetentionTip`); 3 returned late with a file present but uncommitted until this round (`ReopenS116S117`, counted as returned, and `ReopenS118S119`, `ReviewEntryOomdFacts`, counted as cancelled); 13 cancelled with no file | `.ufo/waves/round-27/w1/ReviewLateW2Reports.md` |
| r26 D2 S117 description | fixed: the r26 entry's line-1 S117 description now matches the row; the kernel-oom option history has its own row S137; F7 cites both; dated correction appended | `corpus/knowledge/userspace-oom-killers-r26.md`; `w1/ReviewS117.md` |
| r26 D3 S124 changed in place | fixed: S124 restored, S133 `supersedes S124 —`; M2 and QUALITY 81 | above |
| r26 D4 oomd xattrs wording | fixed in place with a logged correction block: "a count of kill attempts and a count of processes killed; no pid is stored"; also O2, O14 (two places) and O17 from the late `ReviewEntryOomdFacts` report; O5 and O19 do not hold | `w1/ReviewOomdWording.md` |
| r26 D5 README range | fixed: S114–S126 (`dd4dbb20`) | `corpus/README.md` r26 row |
| r26 D6 `count-c2.sh` exits 0 on a failing self-test | explained, not edited: the round-26 script is that round's evidence and stays as committed; this round's `count-c2.sh` exits 1 on any self-test line other than `PASS N/N`. Wave-1 CriticC2Counter found it can still be fooled (a forged PASS line from a crafted case id, the tool's exit code ignored, rule tags taken on trust); those findings go with D7 | `.ufo/waves/round-27/count-c2.sh`; `w1/CriticC2Counter.md` |
| r26 D7 no case pins the A2 rules | named debt: C2 withdrawn (M4); the next attempt needs a case writer on a healthy route and the counter fixes in `w1/CriticC2Counter.md` | contract amendment W1 |
| r25 R1 runway false numbers | named debt: needs code in `tools/mori-job-runway.py`; no executor route this round | — |
| r25 R3 SKILL round-25 rows | fixed in place: rows 1–4 per the re-verified pairs (row 1 now names no settings value); three source rows S134–S136 | `w1/ReviewR3SkillRows.md` §4 |
| r25 R5 routed-check self-test | named debt: needs code; no executor route this round | — |
| r25 R7 knowledge corrections | fixed in place with logged correction blocks: `harness-job-capacity-r25.md` U1 (three later moves; the draft's "floor of 1 held" was false and was not carried) and F10 (full refusal set); `system-pressure-r24.md` `psi.c` anchors (two places), the cgroup pressure-file sentence and F11's first line; four source rows S138–S141 | `w1/ReviewR7Knowledge.md` §2–§4 |

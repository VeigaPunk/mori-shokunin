# CriticC1Novelty — is C1 uncovered mori ground, or absorbed from tsukuroi?

Seat: MoriR27.CriticC1Novelty (critic, leaf, wave 1). Date 2026-10-22. Lane tip read: `5fa0a00f` (contract at
`761b4cdb`, entering tip `fc09f96c`). Sibling read-only: `tsukuroi-shokunin` working tree, last commit touching
the three named entries `c93bd70` (2026-10-22 09:11 -03); `git status --short` on those files printed nothing.
Tooling: nothing installed or upgraded. Scratch: `/fast/scratch/hyaku/mori-r27/CriticC1Novelty/` (fetched
upstream files only).

## Verdict

**The premise is partly false, and the false part is fixable.** Mori has no knowledge *entry* that explains
victim selection. But the contract's evidence for "holds no knowledge" (`contract.md:20-21`) is a sweep that
skips `corpus/SOURCES.md` and `corpus/lessons/`, and it does not search `oom.group`, `prefer`/`avoid` or the phrase
"victim-selection". Mori already holds four source anchors on this ground. The sibling already holds the
measured host side: `oom_score_adj` bands by process group, the units' `OOMScoreAdjust=` values, and
`memory.oom.group` read every round by its census. Two consequences follow. (1) Topics 4 and 5 below must be
written as citations of tsukuroi, not as new mori facts. (2) Six of the files C1 would open already have
mori rows (four earlyoom files, `proc.rst`, `cgroup-v2.rst`) or a URL match (`oom_kill.c`). Re-opening them
adds anchors, not rows. Only a few un-rowed primary files can honestly supply the required ≥3 new rows (§6).
What is genuinely new is the *mechanism* (how the kernel score, the exported score and earlyoom's adjustments
combine) and the *fleet attribution of earlyoom's sends*. Both are inside mori's province.

## 1. What mori already holds (counterexamples to "uncovered")

Contract sweep re-run: `git grep -n -i -E 'oom_score|OOMScoreAdjust' fc09f96c -- corpus/knowledge SKILL.md PROVINCE.md | wc -l` → `0`
(this matches the contract). The same regex over the whole `corpus/` printed 3 hits:
`corpus/SOURCES.md:11`, `corpus/SOURCES.md:126`, `corpus/lessons/round-26.md:67`. The widened regex
`oom\.group|oom_group|--prefer|--avoid|victim-selection|selecting victim` at `fc09f96c` hits `SKILL.md` (3),
`corpus/SOURCES.md` (2), `corpus/knowledge/journal-alarm-routing-r14.md` (1), `corpus/knowledge/userspace-oom-killers-r26.md` (5).

| Mori location | What it already says |
|---|---|
| `corpus/lessons/round-26.md:67` | S114 README `:28` quote: earlyoom "will kill the largest process (highest `oom_score`)". The default selection rule is already in the record. |
| `corpus/SOURCES.md:124` (S118) | The kill.c row's scope already names "victim-selection texts" and anchors `kill.c:609,617-627`. The selection function (`kill.c:355-480`) is in the same file at the same sha256 (`b32e0fad…`). |
| `corpus/SOURCES.md:126` (S120) | `earlyoom.service.in:14 (OOMScoreAdjust=-100)`: earlyoom's own adjustment, status `mined`. |
| `corpus/SOURCES.md:130` (S124) | systemd-oomd candidates are leaf cgroups "or cgroups with `memory.oom.group=1`", status `mined`. |
| `corpus/SOURCES.md:11` (S005) | The `oom:mark_victim` tracepoint carries `oom_score_adj`. Status `queued`, not mined. |
| `corpus/SOURCES.md:132` (S126) | `PKGBUILD:22`: Arch appends an avoid option to the shipped `EARLYOOM_ARGS` (presence only). |
| `corpus/knowledge/journal-alarm-routing-r14.md:56` | systemd reads `memory.events.local` `oom_group_kill` when `memory.oom.group=1`. |
| `corpus/knowledge/userspace-oom-killers-r26.md:91-93,193` | The send line carries uid, name and cmdline (count, never copy). The startup filter echoes restate prefer/avoid (never copy). "earlyoom signalled a victim it selected". It does not say how the victim was selected. |
| `corpus/knowledge/kernel-oom-line-attribution-r12.md:11-12,26` | Kernel victim *record* fields and the open question "fleet attribution of the five observed victims remains [UNKNOWN]". This is the record, not the selection. |
| `corpus/lessons/round-26.md:25` | "earlyoom can still kill running seats" (wave-1 ConnFleetConsumers): the fleet stake is already stated. |
| `PROVINCE.md:368`; `corpus/README.md:342` | FR10 frontier remainder "fleet attribution of any victim" / "of a victim". |

`grep -c badness` over `corpus/`, `SKILL.md` and `PROVINCE.md` → 0. No mori file states the kernel's
`oom_badness` formula or how `/proc/<pid>/oom_score` is derived from it.

## 2. What the sibling already holds (tsukuroi, read-only)

Privacy: the sibling lines below contain pids, uids and command lines. They are cited by path:line only and
are never copied. Sibling process names other than fleet runtimes are bucketed as `other`.

| Sibling location | Holding |
|---|---|
| `oom-event-plane.md:56-72` | Kernel OOM event of 2026-10-13: the trigger line carries the triggering task's `oom_score_adj`; the `constraint=` selection line; the victim (class `python`) at `oom_score_adj` +200. |
| `oom-event-plane.md:90-119` | 164-row task table from the kernel dump with an `oom_score_adj` column; distribution `-1000×1, -900×2, -250×1, 0×23, 100×2, 200×120, 300×15` (`:115`); agent-runtime processes (class `other`) at +200 (`:107-108,111`). |
| `oom-event-plane.md:116`, `:349` | The inference that +200 is "exactly the band the kernel scans first" and "the +200 band is chosen first". |
| `oom-event-plane.md:236,280` | `memory.oom.group` = 0 on `user-UID.slice`; "Nothing was configured to act before the kernel" (later superseded for earlyoom at `:446-448,469`). |
| `oom-event-plane.md:349` (§7 row 6) | `oom_score_adj` steering as an operator-owned lever: `OOMScoreAdjust=` in units; detection via the dump's adj column and live `/proc/*/oom_score_adj`. |
| `kill-event-deep-r8.md:136-151` (§4) | **Measured live `oom_score_adj` classes on this host** (2026-10-14, kernel 7.2.3): +300 (class `other`), +200 for 143 session processes, +100 for the user manager because `user@.service` sets `OOMScoreAdjust=100` (`:142`), 0 for root, and −250/−900/−1000 for system daemons. Origin of the +200 band is `[unknown]` (`:149-152`). |
| `kill-event-deep-r8.md:147` | The inference "the scan prefers the higher-scored, larger-RSS tasks first". |
| `kill-event-deep-r8.md:244,257` | `oom.group` 0 at every level of the live path, so the memcg-limit trigger is closed. |
| `kill-event-deep-r8.md:255` | systemd-oomd's unit runs `OOMScoreAdjust=-900`. |
| `kill-event-deep-r8.md:260,266` | Steering rows: scope units expose no `OOMScoreAdjust` property; `ManagedOOMPreference=none` everywhere sampled (the oomd selection knob). |
| `kill-event-deep-r8.md:295` (Q12) | Open question: origin of the session-wide +200 `oom_score_adj` (owner suggestion: launcher or session source). |
| `kill-event-deep-r8.md:323-324` | Probe ledger: uid-1000 `oom_score_adj` histogram and `systemctl show … OOMScoreAdjust` batches. |
| `systemd-user-plane.md:114,181` | Only one journal-tally row quoting a kernel kill line (which includes an adj value) and an open relationship question. **Nothing on victim selection.** |
| `tools/tsukuroi-census.sh:1081`; `SKILL.md:919,1029,1102` | The census reads `memory.oom.group` on the user slice **every round** (guards shape). |
| `memory-pressure-r25.md:40-41,324-326,364` | earlyoom active and enabled; earlyoom kills do not move kernel counters. No earlyoom selection content: `rg 'sending SIG\|--avoid\|sort-by-rss'` over tsukuroi `corpus/knowledge` and `SKILL.md` matched only unrelated lines. |

The sibling holds **no** source anchor for `oom_badness`. Its `oom_kill.c` row S119 anchors only
`:934-936` (the counter), per tsukuroi `corpus/SOURCES.md:125`. It also has no row for `fs/proc/base.c` or
`proc.rst`, and no earlyoom selection content. Every sibling kill event predates the earlyoom install of
2026-10-20 (`kill-event-deep-r8.md:352-354`), so the sibling holds **zero earlyoom victims**.

## 3. What mori may cite but must not absorb

- The dated host `oom_score_adj` class picture and the user-manager +100 / oomd −900 / system-daemon values
  (`kill-event-deep-r8.md:136-151,255`; `oom-event-plane.md:115`). These are unit and OS state, and
  `PROVINCE.md:12-16` refuses systemd unit state (→ tsukuroi). Mori cites them with their date and kernel
  (2026-10-14, 7.2.3). It does not restate unit `OOMScoreAdjust=` values as its own finding.
- `memory.oom.group` host values (`oom-event-plane.md:236,280`; `kill-event-deep-r8.md:244,257`; tsukuroi
  census `:1081`). This is a live tsukuroi census surface; mori must not add a second reader for it (that
  would be a duplicate authority).
- Q12, the origin of the +200 band (`kill-event-deep-r8.md:295`). If a mori seat finds the origin (a launcher
  or session inheritance), it is a finding **routed to tsukuroi** through the L1, not a mori Core fact.
- The `ManagedOOMPreference` steering knob (`kill-event-deep-r8.md:266`) and every "operator action" cell of
  §7 and §8 of the sibling's tables. These are remediation levers; mori is detection and report only.

## 4. The six C1 topics: what is genuinely new

My split of the contract's C1 scope (`contract.md:17-19`, plus the dispatch brief): T1 earlyoom default
selection and `--sort-by-rss`; T2 `--prefer`/`--avoid`/`--ignore`; T3 kernel selection (`oom_badness`,
`oom_score`, `oom_score_adj`); T4 `memory.oom.group`; T5 the `oom_score_adj` that fleet processes run with on
this host; T6 the share of earlyoom's earlier-boot sends that hit fleet processes.

| Topic | Mori already | Sibling already | Genuinely new mori knowledge? | Row or anchor |
|---|---|---|---|---|
| T1 | default rule only (`lessons/round-26.md:67`) | none | **Yes, the mechanism**: ties broken by RSS (`kill.c:457-465`); `-1000` skipped "like the kernel oom killer would" (`kill.c:467-468`); pid ≤ 2 and kernel threads skipped (`kill.c:357,391-393`); `--sort-by-rss` swaps the primary key (`kill.c:430-456`) | anchors on S118 (kill.c, same sha256 `b32e0fad…`), S119 (main.c, `08656b0b…`), S115 (MANPAGE, `cc48b02e…`) |
| T2 | presence and "never copy" rules (`userspace-oom-killers-r26.md:91-93`); Arch adds an avoid option (S126 `PKGBUILD:22`) | none | **Yes**: prefer/avoid add ±300 to the *exported* score, or ±3 GiB to RSS under `--sort-by-rss` (`kill.c:24-32,410-423`); ignore drops the candidate (`kill.c:424-426`); matching is on `comm` (`kill.c:405`) | anchors on S118, S119 (`main.c:181-186,374-393`), S115 (`MANPAGE.md:178,191,203,275-277`) |
| T3 | victim *record* only (S003 `:447,935-936,945`) | inferences "scanned first" / "chosen first" (`oom-event-plane.md:116,349`; `kill-event-deep-r8.md:147,260`) | **Yes**, and it corrects the sibling's wording: `oom_badness` *adds* `adj × totalpages/1000` to RSS+swap+page-table pages (`oom_kill.c:228-234`). It is additive, not a band order. The exported score is rescaled (`base.c:597`) | `oom_kill.c` = anchor on S003; `proc.rst` = anchor on S082 (same sha256 `e760f716…`); **`fs/proc/base.c` has no row** |
| T4 | oomd candidate rule (S124), `oom_group_kill` (`journal-alarm-routing-r14.md:56`) | host value 0, read every round | **Partly**: the kernel semantics (`cgroup-v2.rst:1454-1455`, the `-1000` exception) and the fact that earlyoom ignores the group (it signals a pid, or a process group under `-g`). The host value is not new | `cgroup-v2.rst` = anchor on S092 (same sha256 `a9433bb0…`) |
| T5 | none | **measured 2026-10-14** (`kill-event-deep-r8.md:136-151`) | **Only as fleet-class bucketing and a fresh date**: the numbers below match the sibling's band shape; the origin stays Q12 (tsukuroi) | `systemd.exec.xml` and `units/user@.service.in` at v262 have **no mori row** |
| T6 | per-boot send counts only (38+1, `lessons/round-26.md:22-25`) | none (no earlyoom victims) | **Yes, fully new**, and squarely FR10 (`PROVINCE.md:368`) | own-work capture; no upstream row needed |

Live re-measure for T5 (read-only `/proc/*/comm` and `/proc/*/oom_score_adj`, classed in memory, no pids;
2026-10-22T15:50:07Z, kernel `7.2.11-arch1-1`): class `omp` adj 200 ×3; class `python` adj 200 ×28; class
`other` −1000×1, −900×2, −250×1, −100×1, 0×1187, 100×2, 200×65, 300×1. Processes owned by the session user:
200×95, 100×2, 300×1, 0×2. The −100 is consistent with S120 `:14` [INFERENCE: earlyoom itself]. Most of the
1187 zero-adj `other` processes are kernel threads, which neither killer considers (`kill.c:391-393`).
So the fleet runtime classes still sit at +200 in this boot, which is the sibling's dated shape. This is a
freshness re-reading of tsukuroi §4, not new mori ground.

## 5. Province ruling

- **Fleet attribution of a victim (T6) is mori's.** The sibling says so: "fleet correlation belongs to mori"
  (tsukuroi `PROVINCE.md:30-33`), and the ADJ-04 row sends "a kill signal [that] needs fleet/wave attribution"
  to mori (`PROVINCE.md:49`). Mori's own FR10 remainder names it (`PROVINCE.md:368`).
- **The selection mechanism (T1–T4) is knowledge mori may hold** because it is needed to read its own
  `KILLER_ACTED` evidence. It must be held as upstream-source reading, not as host configuration.
- **Host OOM configuration is tsukuroi's.** This covers unit `OOMScoreAdjust=`, `memory.oom.group` values,
  `ManagedOOMPreference`, the origin of the +200 band, and any steering advice. Mori refuses "systemd unit …
  state (→ tsukuroi)" (`PROVINCE.md:12-16`), and tsukuroi owns "systemd user units … unit files"
  (tsukuroi `PROVINCE.md:10`). Mori's FR10 boundary adds "never enable or tune a killer" (`PROVINCE.md:53`).
  A SKILL Round27 row such as "set `OOMScoreAdjust=` / `--avoid` to protect seats" would breach both.
- A per-process `oom_score_adj` read of fleet-runtime classes is fleet observation, and it is in province if
  it is reported as class counts. Explaining *why* a unit carries a value is OS diagnosis, and it is tsukuroi's.

## 6. Counterexamples, impacted axes, smallest safe corrections

**N1 — false provenance in the "Before" premise.** Counterexample: §1 rows `lessons/round-26.md:67`,
`SOURCES.md:124,126,130,11`. Axes: depth (overstated as fully uncovered), calibration. Correction: restate the
premise in the entry's Scope as "mori holds the default rule as one README quote and three unit or oomd
anchors; no entry explains the mechanism". Widen the recorded sweep to `corpus/` with the extra terms. No
counter change is needed; the counter does not depend on this sentence.

**N2 — absorption risk on T5 and T4.** Counterexample: the sibling measured the same classes
(`kill-event-deep-r8.md:136-151`), and the 2026-10-22 numbers above reproduce its band shape. Axes: adjacency
(a second authority for unit and OS state), privacy (the sibling text carries pids and uids). Correction: the
entry carries an Adjacency section that cites `tsukuroi-shokunin@c93bd70:corpus/knowledge/kill-event-deep-r8.md:136-151,295`
and `oom-event-plane.md:115,236,280`. Mori's own T5 output is fleet-class counts with date and kernel only.
No unit property values are re-read as mori facts, and no reader for `memory.oom.group` is added.

**N3 — duplicate source rows would satisfy the counter.** `count-c1.sh:21-29` accepts any `mined` row ≥ S127
that names the entry. It does not check whether the URL already has a row. These fetched bytes are
identical to existing rows (sha256 of my 2026-10-22 fetch):

| File at pin | sha256 (first 16) | Existing row |
|---|---|---|
| earlyoom v1.9.0 `kill.c` | `b32e0fad65e29823` | S118 (same) |
| earlyoom v1.9.0 `main.c` | `08656b0bc90c85f2` | S119 (same) |
| earlyoom v1.9.0 `meminfo.c` (`get_oom_score` `:172-193`) | `526e512c89c58cb0` | S116 (same) |
| earlyoom v1.9.0 `MANPAGE.md` | `cc48b02e79255ae2` | S115 (same) |
| Linux v7.2 `Documentation/filesystems/proc.rst` | `e760f716f8278dee` | S082 (same prefix) |
| Linux v7.2 `Documentation/admin-guide/cgroup-v2.rst` | `a9433bb0e16a67f0` | S092 (same prefix) |
| Linux v7.2 `mm/oom_kill.c` | `452f1348e79c252e` | S003 (same URL; row records no hash) |

Primary files with **no** mori row (honest S127+ candidates):

| File at pin | sha256 (first 16) | Topic |
|---|---|---|
| Linux v7.2 `fs/proc/base.c` | `cef1a2cf3f34f683` | T3: `proc_oom_score` `:583-597`, `oom_score_adj_write` `:1258-1288` |
| systemd v262 `man/systemd.exec.xml` | `44b89bffce737aff` | T5: `OOMScoreAdjust=` `:1293-1300` |
| systemd v262 `units/user@.service.in` | `72c2f40dcfced1d8` | T5: `:35 OOMScoreAdjust=100` |
| earlyoom v1.9.0 `proc_pid.c` | `e5b654466cd92fb4` | T1: stat parse used for RSS (`kill.c:375`); weak |

Two candidates are a different case. A v7.2 `mm/memcontrol.c` would sit beside S004 (master commit), so it
must say that it supersedes or narrows S004. The man-pages `proc_pid_oom_score_adj(5)` was not fetched by
this seat. Axes: calibration, freshness. Correction: the L1 declares before integration that a re-opened file
adds an anchor to its existing row (the dispatch rule). The ≥3 new rows must be primary files absent from
`SOURCES.md` by URL. **A sibling-citation row (like S125) must not count toward the three**, or C1's depth
would rest on absorbed sibling knowledge. The counter cannot see either rule, so the closure must check them
by hand.

**N4 — the sibling's "band scanned first" wording versus the source.** Counterexample: `oom_kill.c:232-234`
"/* Normalize to oom_score_adj units */ adj *= totalpages / 1000; points += adj;". The adjustment is
additive. An adj-0 task beats a +200 task once its RSS, swap and page tables exceed the other's by
0.2 × totalpages. `select_bad_process` (`oom_kill.c:362`) evaluates every task (`oom_evaluate_task`
`:306`); it does not scan a band first. [INFERENCE] On this host's RAM+swap, that margin is many GiB, so in
practice the +200 classes dominate. The sibling's conclusion holds; its mechanism wording does not. Axes:
depth (new for mori), adjacency. Correction: mori's entry states the formula with S003 anchors. The L1 sends
the wording note to tsukuroi as a finding and does not edit tsukuroi.

**N5 — two score scales.** `base.c:597` "points = (1000 + badness * 1000 / (long)totalpages) * 2 / 3;" and
`proc.rst:1811-1812` "the exported value includes oom_score_adj so it is effectively in range [0,2000]".
earlyoom reads that exported value (`meminfo.c:172-178`) and adds ±300 for prefer/avoid on that scale
(`kill.c:25,27,414,421`). [INFERENCE from the two formulas] An adj of +200 moves the exported score by about
133, so earlyoom's +300 prefer acts like an adj of about +450. Neither lane holds this. It is a good
grounded decision row. Axis: depth.

**N6 — a class label is not fleet membership (T6 identity risk).** The send line names `comm`
(`kill.c:627`, `victim->name`), and the T5 read shows 65 non-fleet-class session processes at the same +200.
The `python` class includes any operator python. Mori already rules that a name token is "not membership
proof" (`corpus/README.md:40`). Axes: calibration, privacy. Correction: report T6 as "send lines whose `comm`
falls in fleet-runtime classes (omp, bun, node, python) versus `other`". Do not report it as "fleet processes
killed", and never report a pid, uid or cmdline. Boot −1 is still the round-26 boot (`journalctl --list-boots`:
`-1` starts 2026-10-20 09:57:09 -03, `0` starts 2026-10-22 04:55:41 -03; earlyoom
`ActiveEnterTimestampMonotonic=19964362`, unchanged from round 26). So the 38+1 baseline still matches.

## 7. Ready-to-paste text for the L1

Adjacency paragraph for `corpus/knowledge/oom-victim-selection-r27.md`:

```markdown
## Adjacency

- tsukuroi owns this host's OOM configuration as OS and unit state. Its dated reading (2026-10-14, kernel
  7.2.3) of `oom_score_adj` classes, the user manager's `OOMScoreAdjust=100`, systemd-oomd's `-900` and
  `memory.oom.group` 0 is cited, not absorbed: `tsukuroi-shokunin@c93bd70:corpus/knowledge/kill-event-deep-r8.md:136-151,244,255-266`;
  `corpus/knowledge/oom-event-plane.md:90-119,236,280`. The origin of the session-wide +200 band is its open
  Q12 (`kill-event-deep-r8.md:295`); any finding on it is routed there.
- Mori holds the selection mechanism as upstream-source reading and the fleet-class attribution of
  earlyoom's send lines (FR10, `PROVINCE.md:368`; tsukuroi `PROVINCE.md:30-33,49`). No killer is tuned, no
  unit value is proposed, and no steering advice is given.
```

Scope sentence replacing the contract premise:

```markdown
Before this entry mori held the default earlyoom rule as one README quote (`corpus/lessons/round-26.md:67`)
and the anchors S118 (`kill.c` victim-selection texts), S120 `:14`, S124 and S005, but no entry explained how
either killer scores a candidate.
```

## Not claimed

No victim identity, pid, uid, command line, journal `MESSAGE` text, `/etc/default/earlyoom` value or
prefer/avoid/ignore expression was read into this report. No sibling file was edited. No unit, process
setting or signal was touched. T6 was not measured by this seat. The `proc_pid_oom_score_adj(5)` man page was
not fetched.

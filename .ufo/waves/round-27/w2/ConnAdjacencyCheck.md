# ConnAdjacencyCheck — the Adjacency paragraph of the C1 entry against the sibling files (mori round 27, wave 2)

Seat: MoriR27.ConnAdjacencyCheck (connector, leaf, read-only). Date 2026-10-22.
Attacks: `corpus/knowledge/oom-victim-selection-r27.md:183-190` (Adjacency) at landed tip `5f00fd04`, plus the two
places that carry the same correction: Fact 2 (`:63-64`) and SKILL.md `:739`.
Tools installed or updated: none. Skill read: godspeed (`~/.agents/skills/godspeed/SKILL.md`); `~/.omp/agent/RULES.md` read.
No lane, sibling or fleet file was edited. Read-only git only.

## Axes

Adjacency (observed 6), depth (C1's axis), freshness (5). No-harm guards: privacy (no pid, uid or command line; the
tsukuroi lines cited below carry pids, so none are quoted) and the retention scan (this report holds no settings
path, session id or routing key).

## Evidence base (commands run here)

- The entry at the tip is the working copy: `git show 5f00fd04:corpus/knowledge/oom-victim-selection-r27.md | sha256sum`
  and `sha256sum` of the file both give `e775a3d5…74ff0`.
- tsukuroi: `157ee255`, `c93bd70` (the pin CriticC1Novelty used) and tsukuroi HEAD (`dd94cb1f` at the end of this run;
  `b1647ff2` at the start) all hold the same blobs: `oom-event-plane.md` → `e5f8b613`, `kill-event-deep-r8.md` →
  `7dc5337f` (`git rev-parse <rev>:<path>`). `157ee255` is an ancestor of HEAD. The worktree file sha256 values are
  `30cb31fd…be76` and `cd2fe9bb…0861`, matching ConnSiblingOverlap `:6`. Line numbers below are valid at all three revisions.
- Kernel bytes: `/fast/scratch/hyaku/mori-r27/MoriR27.SrcKernelOomBadness/oom_kill.c`, sha256
  `452f1348…6b4e` (= mori S003 digest in the entry's `source:` line, = tsukuroi S119 digest at tsukuroi `corpus/SOURCES.md:125`).
  Lines pinned with `grep -n`.

## 1. Is the correction of "+200 band scanned first" stated fairly, with lines?

The sibling wording, pinned (`grep -n` at tsukuroi `157ee255`):

| tsukuroi line | Verbatim (≤ 25 words) | Kind |
|---|---|---|
| `oom-event-plane.md:116` | "the user workload ran at +200 (and Chromium helpers at +300), which is exactly the band the kernel scans first." | ordering claim |
| `oom-event-plane.md:349` | "the +200 band is chosen first; marking a known-huge batch job differently changes who dies" | ordering claim; the consequence is right |
| `kill-event-deep-r8.md:147` | "[inference] under a kernel OOM the scan prefers the higher-scored, larger-RSS tasks first" | almost the right model; only "first" is wrong |
| `kill-event-deep-r8.md:260` | "the +200 band is scanned first; a known-huge batch job placed differently changes who dies" | ordering claim, as `:116` |

Kernel v7.2 (`oom_kill.c`): points = rss + swap entries + page tables (`:228-229`), then `adj *= totalpages / 1000;
points += adj;` (`:233-234`); `if (points == LONG_MIN || points < oc->chosen_points) goto next;` (`:340`), else select
(`:343-348`); "We choose the process with the highest number of 'points'." (`:359`); `select_bad_process` walks
`for_each_process` (global) or `mem_cgroup_scan_tasks` (memcg) once (`:362-376`). No band order exists.

| # | Statement in the landed Adjacency (`:185-190`) | Verdict | Severity |
|---|---|---|---|
| A1 | "the kernel does not scan the +200 band first" | **holds** against `oom_kill.c:362-376`. | — |
| A2 | "it makes one pass and keeps the highest adjusted score (S003 `mm/oom_kill.c:228-234,340`)" | **holds in substance, under-cited.** `:228-234,340` show the formula and the comparison, not the single pass: that is `:358-376` (ConnSiblingOverlap `:42` cited `:362-376`; the landed text dropped it). "Adjusted score" collides with Fact 1's earlyoom "score … after the prefer/avoid adjustment" (`:41-42`). Two cases the sentence omits: a task already marked as an OOM victim aborts the scan with no new pick (`:324-327,351-355`), and an `oom_task_origin` task takes `LONG_MAX` (`:334-336`). | low |
| A3 | "corrects one model there" with no tsukuroi line | **unfair by omission.** The wording sits at four lines in two files (table above). No line is given, so a tsukuroi reader cannot find what is corrected. ConnSiblingOverlap `:106,112` and CriticC1Novelty `:140,209` both offered pinned ranges; the landed text kept neither. The paragraph also does not say that tsukuroi's *conclusions* at those lines hold: event A's victim held 26.58 GiB anon + 27.12 GiB swap against ≤ 0.44 GiB for every other listed +200 task (`oom-event-plane.md:106-113`), so footprint picked it inside a band of 120 (`:115`). The `:147-148` argument (a kernel pick of the +100 manager contradicts the class picture) also holds: the manager would need about 10% of RAM + swap more footprint than every +200 client [INFERENCE: `:233-234` at adj difference 100]. CriticC1Novelty `:180` said this ("The sibling's conclusion holds; its mechanism wording does not"); the landed text dropped it. | medium |
| A4 | "the live +200 band" | **wrong (freshness wording).** The tsukuroi band reading is dated 2026-10-14 (`kill-event-deep-r8.md:136` "measured on the live host" on that date). Correction: "the 2026-10-14 +200 band". Mori's own 2026-10-22 capture is Fact 4. | low |
| A5 | "record two earlier kill events from before earlyoom was installed (2026-10-20)" | **holds.** Event A 2026-10-13 (`oom-event-plane.md:54-69`), event B 2026-10-14 (`kill-event-deep-r8.md:146`). The install date is mori's own (`userspace-oom-killers-r26.md:31,207`), matched by tsukuroi `oom-event-plane.md:448` and `kill-event-deep-r8.md:354`. | — |
| A6 | "this entry supplies the origin (Fact 3)" | **holds.** It answers Q12 (`kill-event-deep-r8.md:149,295`) from systemd v262 source (S130) plus a host read: the user manager's `DefaultOOMScoreAdjust` reads 200, and no config file sets it (wave-1 `HostUnitOomAdjust.md:94-96`). That closes ConnSiblingOverlap risk R1 (`:117-120`). | — |
| A7 | "neither tsukuroi event enters the earlyoom send counts above" | **holds.** The sends are boot -1 only (Fact 5, `:125-127`), which starts 2026-10-20 09:57:09 -03 (`CriticC1Novelty.md:197`). Both events are earlier. | — |

Same correction, outside the paragraph:

- **Fact 2, entry `:64`: "a tie keeps the first task scanned (`:340`)". Wrong, high.** At `:340` only a strictly
  smaller score goes to `next`. An equal score falls through to `select` (`:343-348`) and replaces the chosen task,
  so a tie goes to the **last** task scanned at that score. The error comes from wave-1
  `SrcKernelOomBadness.md:67,143` and was carried over unchecked. It touches A1 directly: scan order matters only on
  an exact tie, and then the later task wins. That is the opposite of a "scanned first" model.
- **SKILL.md `:739` error-pattern row** quotes `"the +200 band is scanned first"` verbatim (tsukuroi
  `kill-event-deep-r8.md:260`) with no attribution, and cites only `oom_kill.c:228-234,340` (see section 2).

## 2. Is anything absorbed rather than cited?

| # | Item | Verdict | Severity |
|---|---|---|---|
| B1 | Fact 3 `:85-86`: the `systemd.exec(5)` "normally at 0" sentence "describes the system manager, not a user manager" | **uncited second correction.** It corrects tsukuroi `kill-event-deep-r8.md:142` (ConnSiblingOverlap T7, `:46`). The Adjacency says "corrects one model". It corrects two. | medium |
| B2 | SKILL.md `:739` turns tsukuroi's sentence into a mori error pattern with no sibling path | **absorbed wording.** Add "(tsukuroi `oom-event-plane.md:116,349`, `kill-event-deep-r8.md:147,260`)". | low |
| B3 | Scope `:13-14`: "tsukuroi had measured the host's `oom_score_adj` bands on 2026-10-14 (Adjacency below)" | **cited, but the Adjacency gives no line.** The pointer ends without one. Needs `kill-event-deep-r8.md:136-144`. | low |
| B4 | Fact 4 table bands (+300, +200, +100, 0, −250, −900, −1000) | **not absorbed.** These come from mori's own capture (`evidence/oom-score-classes.txt`, 2026-10-22) and only match tsukuroi's 2026-10-14 bands in shape. | — |
| B5 | Fact 3 `:101` "Can raise but never lower" refuted | **not absorbed.** The claim under test is in-lane (wave-1 `CriticInheritProbe.md:147`), not tsukuroi's. `git grep` over tsukuroi HEAD `corpus` and `SKILL.md` for "never lower" finds only unrelated hits (`SKILL.md:772`, `update-safety-v3.md:40`). | — |
| B6 | Install date 2026-10-20; "a userspace kill moves no kernel counter" | **not absorbed.** Both are mori's own (r26 `:31,207`; S003 used-by lists `oom-kill-counter-kernel-only-r12.md`). | — |

## 3. Are cross-lane source ids disambiguated?

"Source ids are lane-local: tsukuroi's S119 and S127 are not mori's." (`:189-190`). Verdict: **holds but incomplete; medium.**

Every S-id in the entry's `source:` line also exists in tsukuroi with a different meaning (`grep -n` over both `corpus/SOURCES.md`):

| Id | mori (tip `5f00fd04`) | tsukuroi (HEAD) |
|---|---|---|
| S003 | v7.2 `mm/oom_kill.c` (`:9`) | Arch AUR incident news (`:9`) |
| S115 | earlyoom `MANPAGE.md` (`:121`) | v7.2 `psi.rst` (`:121`) |
| S118 | earlyoom `kill.c` (`:124`) | v7.2 `cgroup-v2.rst` (`:124`), which is mori's S092 file |
| S119 | earlyoom `main.c` (`:125`) | v7.2 `mm/oom_kill.c`, sha256 `452f1348…6b4e` (`:125`) = mori S003 bytes |
| S120 | earlyoom unit (`:126`) | systemd `oomd.conf.xml` (`:126`) |
| S125 | tsukuroi `memory-pressure-r25.md` (`:131`) | mori `system-pressure-r24.md` (`:131`) |
| S127 | Linux `base.c`/`oom.h`/`fork.c` (`:133`) | mori `system-pressure-r24.md` again, blob `d4ccce42` (`:133`) |
| S128-S132 | man pages, systemd, earlyoom, omp/Bun | btrfs-progs and `volumes.c` (`:134-138`) |

Gaps:
- The paragraph says S119 is "not mori's" but leaves out the one *equivalence* that matters: tsukuroi S119 is the same
  bytes as mori S003. ConnSiblingOverlap `:106` carried it; the landed text dropped it.
- S118 and S120 are the dangerous collisions in this topic (both lanes cite them in OOM text), and they go unnamed.
- Mori S003's row still records no sha256 and only anchors `447,935-936,945` (`SOURCES.md:9`). The
  `oom_kill.c:228-234,340,…` anchors and the digest live only in the entry's `source:` line, so the S003 ≡ tsukuroi S119
  equivalence cannot be checked from the row. [Hygiene pointer only; the row is outside this seat's scope.]

## Proposed move (one, bounded): exact old -> new text

The one non-obvious synthesis: put the tie correction (Fact 2) and the band correction (Adjacency) together. The
kernel's only order dependence is the tie rule, and it favours the *later* task, so it cuts against "scanned first".
Both corrections then cite the same lines, the sibling lines are pinned, and the id mapping is complete. This improves
adjacency and depth and harms no axis: no counter input changes (`count-c1.sh` reads `source:` rows and SKILL rows,
neither altered), and no pid, uid or value is added.

**Entry `:64`.** old:
`  (`:216-222`). The kernel keeps the highest score; a tie keeps the first task scanned (`:340`).`
new:
`  (`:216-222`). The kernel keeps the highest score; only a strictly lower score is skipped, so a tie goes to the last task scanned (`:340,343-348`).`

**Entry `:185-190` (Adjacency).** old: the paragraph from `Adjacent: \`tsukuroi-shokunin/` through
`tsukuroi's S119 and S127 are not mori's.` new:

```markdown
Adjacent: `tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md` and `kill-event-deep-r8.md` at tsukuroi `157ee255`
(blobs `e5f8b613`, `7dc5337f`; unchanged at tsukuroi HEAD on 2026-10-22) record two kill events from before earlyoom
was installed (2026-10-20): event A, the kernel OOM of 2026-10-13 (`oom-event-plane.md:54-69,104-119`), and event B
of 2026-10-14 (`kill-event-deep-r8.md:146-148`), plus the 2026-10-14 bands with the +200 origin open
(`kill-event-deep-r8.md:136-152`, Q12 at `:295`). This entry supplies that origin (Fact 3) and corrects two readings
there. First, `oom-event-plane.md:116,349` and `kill-event-deep-r8.md:147,260` say the +200 band is scanned or
chosen first: the kernel walks every task of the OOM domain once and keeps the highest badness, footprint plus
`adj * totalpages / 1000` pages, with a tie going to the later task (S003 `mm/oom_kill.c:228-234,340-348,358-376`).
tsukuroi's conclusions at those lines still hold: event A's victim won on footprint inside a band of 120, and a
kernel pick of the +100 manager in event B stays unlikely. Second, the `systemd.exec` default quoted at
`kill-event-deep-r8.md:142` describes the system manager; an unprivileged user manager gives its children its own
value plus 100 (Fact 3). Cited, not absorbed: neither event enters the earlyoom send counts above (wave-1
ConnSiblingOverlap). Source ids are lane-local and every bare id here is mori's: tsukuroi S119 is the same v7.2
`mm/oom_kill.c` bytes as mori S003 (sha256 `452f1348…6b4e`); tsukuroi S115, S118, S120 and S127 are `psi.rst`,
`cgroup-v2.rst`, `oomd.conf.xml` and a row for mori's `system-pressure-r24.md`, not mori's rows of those numbers.
```

**Entry `:14`.** old: `lane tsukuroi had measured the host's \`oom_score_adj\` bands on 2026-10-14 (Adjacency below).`
new: `lane tsukuroi had measured the host's \`oom_score_adj\` bands on 2026-10-14 (\`kill-event-deep-r8.md:136-144\`, Adjacency below).`

**SKILL.md `:739`.** old: `| "the +200 band is scanned first" | false: the kernel makes one pass and keeps the highest score, where the adjustment adds \`adj * totalpages / 1000\` pages (\`oom-victim-selection-r27.md\` Fact 2; [oom_kill.c:228-234,340](…)) |`
new: `| "the +200 band is scanned first" (tsukuroi \`oom-event-plane.md:116,349\`, \`kill-event-deep-r8.md:147,260\`) | false: the kernel makes one pass and keeps the highest score, where the adjustment adds \`adj * totalpages / 1000\` pages; a tie goes to the later task (\`oom-victim-selection-r27.md\` Fact 2; [oom_kill.c:228-234,340-348,358-376](…)) |`
(keep the existing URL in place of `…`).

## Draft cross-lane finding for the operator to route to tsukuroi (one paragraph, not sent)

> From mori round 27 (`mori-shokunin/corpus/knowledge/oom-victim-selection-r27.md`, Facts 2-3; Linux v7.2
> `mm/oom_kill.c` sha256 `452f1348…6b4e`, your S119; systemd v262 `units/user@.service.in:35` and
> `src/core/main.c:3045-3063`): four tsukuroi lines say the +200 band is scanned or chosen first
> (`oom-event-plane.md:116,349`, `kill-event-deep-r8.md:147,260` at `157ee255`, unchanged at HEAD). The kernel has no band
> order. It walks every task in the OOM domain once (`oom_kill.c:362-376`) and keeps the highest
> rss + swap + page tables + `oom_score_adj × totalpages / 1000` (`:228-234,340`), and on an exact tie the later task
> wins (`:340-348`). So +200 weighs like 20% of RAM plus swap, and an adj-0 task larger by more than that is still
> chosen first. Your conclusions at those lines stand; only the ordering wording is wrong. earlyoom, active since
> 2026-10-20, likewise makes one pass and takes the highest exported `oom_score`. Two related items: Q12
> (`kill-event-deep-r8.md:295`) is answerable. The user manager runs at 100 (`user@.service`), and an unprivileged
> manager defaults its children to its own value plus 100, giving the session-wide +200. A host read on 2026-10-22 shows
> the user manager's `DefaultOOMScoreAdjust` at 200 with no config file setting it. And the `systemd.exec` default quoted at
> `kill-event-deep-r8.md:142` holds for the system manager only (systemd v262 `systemd-system.conf.xml:305-306`).
> Suggested shape: an append-only notice like your R18-FRESHNESS ones, earlier bytes unchanged. Mori's source ids
> differ from yours (mori S003 = your S119); cite them lane-qualified.

## Risks

- R1: the tie rule depends on scan order. `for_each_process` walks the task list in creation order
  [INFERENCE: new tasks join at the tail in `copy_process`; `kernel/fork.c` not re-opened here], so "later" means
  roughly "newer". A tie on badness in pages is rare at any real footprint, so the fix is about the stated rule, not a
  likely event.
- R2: tsukuroi HEAD moved during this run (`b1647ff2` → `dd94cb1f`). The pins hold by blob id, so cite `157ee255` plus
  the blob ids, not "HEAD".
- R3: the four-line replacement makes the Adjacency longer. It changes no counted bytes (`count-c1.sh` reads `source:`
  row ids and SKILL Round27 table rows; no row is added or removed).
- R4: privacy. The tsukuroi lines cited here contain pids and unit names that embed a uid. The new text cites line
  numbers only and quotes none of them.

## Verification (for the L1; not run as acceptance by this seat)

- Run here: `grep -n '' …/MoriR27.SrcKernelOomBadness/oom_kill.c | sed -n '300,380p'` shows `:340` `points < oc->chosen_points`
  → `goto next`, and `:343-348` `select:` assigns `oc->chosen`.
- Run here: `git -C …/tsukuroi-shokunin rev-parse {157ee255,c93bd70,HEAD}:corpus/knowledge/{oom-event-plane,kill-event-deep-r8}.md`
  gives `e5f8b613` / `7dc5337f` at all three.
- Run here: `git show 157ee255:corpus/knowledge/kill-event-deep-r8.md | grep -n 'prefers the higher'` → `:147`
  (ConnSiblingOverlap T10 `:49` says `:148`; low, its pin is off by one).
- Unrun: `bash .ufo/waves/round-27/count-c1.sh <new tip>` (must stay `C1=met`); the retention scan per contract `:82-84`
  (must stay ≤ 4) after any edit; `python3 -I -B .ufo/waves/round-27/check-row-identity.py` if S003's row is touched.

# ReviewHygieneR7 — routed R7 re-verification, wave 2 (mori round 27)

Seat: MoriR27.ReviewHygieneR7 (reviewer, leaf; no subagents, no background jobs). Date: 2026-10-22.
Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`. Attacked rev `5f00fd045c137b7e3835506d69946cfd9d010eb5`
(branch master). Lane HEAD had already moved to `b97b2e3fc286f0d0…` (later wave-2 seats landing), so every lane
read in this report is `git show 5f00fd045c137b7e3835506d69946cfd9d010eb5:<path>` — read-only git, no refs touched.

Scope: `corpus/knowledge/harness-job-capacity-r25.md` U1 and F10; `corpus/knowledge/system-pressure-r24.md`
psi.c anchors (F3 sentence and the F9 cgroup paragraph), the cgroup pressure-file sentence, and F11 — checked
against `.ufo/waves/round-27/w1/ReviewR7Knowledge.md` and `corpus/SOURCES.md` rows S138–S141, with Linux v7.2
`kernel/sched/psi.c` re-opened and lines 1540, 1545, 1550, 1686 pinned by `grep -n` on the downloaded bytes.
The only lane file written is this report. Scratch: `/fast/scratch/hyaku/mori-r27/ReviewHygieneR7/`.

## 1. Verdict

Every assigned statement holds at the attacked rev. No high or medium findings. Two low findings follow (one
wording item in the wave-1 report, one lead-in wording in a landed sentence); neither falsifies a claim a reader
would act on.

## 2. Findings

**L1 — low, wording, wave-1 report only (no landed impact).** `w1/ReviewR7Knowledge.md` §2.1 says the entry's
`source:` front-matter line "lists S098…S104, S112-S113 today". At `5fa0a00f` the line actually listed S098–S105,
S111, S112, S113 (`git show 5fa0a00f:corpus/knowledge/harness-job-capacity-r25.md`, line 1). The required
addition itself is correct and present: the landed line 1 adds S138–S141 and the `recheck:` line (line 3) reads
"re-open S098–S103, S112–S113 and S138–S141". Nothing in the landed entry needs to change.

**L2 — low, wording, landed corpus.** The corrected cgroup sentence (system-pressure-r24.md, F9 paragraph)
opens "The cgroup v2 documentation gives each controller its own pressure file in a separate section" and then
lists five files, two of which are not controller files: `cgroup.pressure` (a per-cgroup switch, documented as
such two clauses later) and `irq.pressure` (an IRQ-scope file sitting before the "Controllers" heading at
`cgroup-v2.rst:1089`). All five line ranges are exact (§3.2 below), and the sentence was authored this way in the
reviewed wave-1 block §3.2, so this is lead-in wording, not a data error. Smallest fix: "gives each pressure file
its own section".

## 3. What holds — verification detail

### 3.1 psi.c anchors at v7.2 (F3 sentence, F9 paragraph)

Downloaded `https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c` at 2026-10-22T17:09:51Z,
sha256 `452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5`, 1725 lines — byte-identical to the
digest the wave-1 report §7 records. `grep -n` on those bytes:

- `1540: return psi_show(m, &psi_system, PSI_IO);`
- `1545: return psi_show(m, &psi_system, PSI_MEM);`
- `1550: return psi_show(m, &psi_system, PSI_CPU);`
- `1686: return psi_show(m, &psi_system, PSI_IRQ);` (signature `psi_irq_show` at 1684, under
  `#ifdef CONFIG_IRQ_TIME_ACCOUNTING` at 1683)

So the landed anchor `psi.c:1540,1545,1550,1686` names exactly the four `psi_show(m, &psi_system, …)` call
sites, and "1538-1550 holds two full readers and a signature, not four readers" (wave-1 M2) is right: io reader
1538–1541, memory reader 1543–1546, cpu signature 1548. Both landed places updated — F3 (line 89 of the rev's
blob) and the F9 cgroup paragraph (line 148); no `1538-1550` remains anywhere in the entry except inside the
corrections block's own old→new quote (line 241). The zeroing mechanism behind "so the system CPU `full` line is
always zeros at v7.2" re-verified: comment `psi.c:1282` "/* CPU FULL is undefined at the system level */",
condition `:1283` `if (!(group == &psi_system && res == PSI_CPU && full)) {`, averages/total populated only
inside that branch (1284–1288), single `seq_printf` at 1290. The psi.rst half of F3 also holds verbatim at
`psi.rst:57-58`: "CPU full is undefined at the system level, but has been reported since 5.13, so it is set to
zero for backward compatibility." (23 words).

### 3.2 The cgroup pressure-file sentence (F9 paragraph)

Downloaded `…/v7.2/Documentation/admin-guide/cgroup-v2.rst`, sha256
`a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad` — matches the wave-1 digest and S092. On
those bytes the five section pins are exact: `cgroup.pressure` header at 1066 with the section ending at 1081;
`irq.pressure` at 1083–1087; `cpu.pressure` at 1215–1221; `memory.pressure` at 1911–1915; `io.pressure` at
2171–2175; and 1066–1087 holds only those two files (the "Controllers" heading follows at 1089). The
non-hierarchical claim sits inside the first section, `cgroup-v2.rst:1073-1075`: "This control attribute is not
hierarchical, so disable or enable PSI accounting in a cgroup does not affect PSI accounting in descendants"
(22 words). The old "beside … `cgroup-v2.rst:1066-1087`" wording is gone except inside the corrections block
(line 242 of the rev's blob). The adjacent cgroup.c anchors hold on sha
`3d4a256adea52d7e3f3b60dbb39622c82aa30dc398c01b5a135d2ccac3379a8c`: `cgroup_{io,memory,cpu}_pressure_show` at
3970/3977/3984, `cgroup_irq_pressure_show` 4077, `_write` 4085, `psi = cgroup_psi(cgrp);` at 3973/3980/3987/4080,
comment `:4127` "/* show or hide {cpu,memory,io,irq}.pressure files */" — the landed `cgroup.c:3970-4091` range
covers exactly these.

### 3.3 F11 first line

Landed F11 opens "**F11 — no upstream threshold exists.** Neither `psi.c` nor `psi.rst` — the files read here —
defines a "warn at N %" rule." Holds: `grep -n -i warn` over the sha-verified psi.c finds only the debug
assertion `1145: WARN_ONCE(cgroup->psi->rtpoll_states, "psi: trigger leak\n");` — no threshold rule — and zero
hits in psi.rst. The example quotes sit inside the unchanged `psi.rst:70-88` pointer: `:74` "time window, e.g.
100ms of total stall time within any 500ms window to" and `:85` "For example writing "some 150000 1000000" into
/proc/pressure/memory". psi.rst sha256
`11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692`, matching wave-1 §7.

### 3.4 harness-job-capacity-r25.md U1

Landed U1 equals the wave-1 §2.1 NEW block word for word with the proposal ids S133–S136 renumbered to the
landed S138–S141 (order preserved). Every historical claim re-verified from fresh bytes:

- Feature commit `476b858b3a4a…` patch (fetched 17:18:48Z, sha256 `00f6cbb0b786…1257`): Date Sun, 22 Feb 2026
  12:44:23 +0100 = 2026-02-22 UTC, as U1/S104 say; adds `"async.maxJobs" … default: 15` with
  `description: "Maximum concurrent background jobs (1-100)"` and
  `const asyncMaxJobs = Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 15));`. The "ceiling of 100
  and the floor of 1 date from the feature's first commit" sentence holds.
- S138 = `944d7f8d8d44…`: patch Date Thu, 26 Feb 2026 12:34:29 +0100 = 2026-02-26T11:34:29Z ✓; diff count 3 —
  CHANGELOG.md, settings-schema.ts, sdk.ts, so "touches only CHANGELOG, settings-schema.ts, sdk.ts" ✓; hunks
  `default: 15` → `default: 100` and `?? 15` → `?? 100` ✓.
- S139 = `e398f8316372…`: Date Sun, 3 May 2026 07:09:09 +0200 = 2026-05-03T05:09:09Z ✓; settings-schema.ts hunk
  removes the `ui:` block including `description: "Maximum concurrent background jobs (1-100)",` and keeps
  `default: 100` ✓. (The commit also touches CHANGELOG and a settings-defs.ts UI-adapter refactor; the row never
  claims otherwise.)
- S140 = `6962d5cd2ef1…`: Date Thu, 24 Sep 2026 20:04:41 +0200 = 2026-09-24T18:04:41Z ✓; raw sdk.ts at that
  commit, sha256 `84f3a112a670f36de9c030756f4babc0ad83e37efeca99154ea4d4263423e633` (matches wave-1 §7), line
  1949 exactly `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings) ?? 100),` ✓; parent `d9bc4fbd`
  sha256 `fde5a959e3a310be1d9fd291163dd817d2328d2b5a2012697b75b3205d592104` (matches), line 1797
  `const asyncMaxJobs = Math.min(100, Math.max(1, settings.get("async.maxJobs") ?? 100));` passed as a number at
  line 1811 `? new AsyncJobManager({ maxRunningJobs: asyncMaxJobs })` — the "still static (`:1797`, `:1811`)"
  pin and U1's "static … computed once at session construction" hold. The same patch shows the manager getter
  gaining `return Math.max(1, Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS));`, which is the entry's F3 — U1's
  "the explicit floor `Math.max(1, …)` did not survive that rewrite" is correctly scoped to the clamp expression
  and the accessor, with the effective floor of 1 still documented in F3 and the decision table; no
  contradiction.
- S141 = `c4a2441d8f91…`: Date Fri, 25 Sep 2026 01:02:43 +0200 = 2026-09-24T23:02:43Z ✓ — same UTC day as S140,
  so "dropped the same day" holds; raw sdk.ts sha256
  `4f4897502a75b0b4e0dc5cfa633559e610410a84cb719745fe7d057906029186` (matches), line 1964 exactly
  `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)),` ✓; the patch hunk removes the `?? 100`
  ✓.
- v18.12.6 (`45c35e40…`): sdk.ts sha256
  `c0228addd4cfe93cfd370c7248e9db29743f0fa802aea0e1d1adf4994dbe6957` (matches the entry's front matter and
  wave-1), line 2284 `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)),` — no floor ✓.
  tools/settings.ts sha256
  `514974143d47db0c9765bc47e86dcb9a38bd6bc23113a4ffe557bff0d8e30507` (matches S100), `:941-946` the
  `register({ id: "async.maxJobs", protocolDefault: ["rpc"], type: "number", default: 100 })` accessor, no clamp
  and no floor ✓.
- Pre-fix text confirmed at `5fa0a00f`: old U1 line 270 "the floor of 1 date from the feature's first commit and
  only the default moved (15 to 100)" — replaced in place at the attacked rev; the old wording survives only
  inside the corrections block's old→new quote (line 330). No `S133`–`S136`, no stale "exceeds 100" outside the
  new sentence and the corrections block (line-scanned).

### 3.5 harness-job-capacity-r25.md F10

Landed F10 equals the wave-1 §2.2 NEW block. I pinned all fifteen citations in the rev's bytes of
`.ufo/waves/round-20/build/` and they all carry the claimed counts: 64 at `GtLaneKasegi.md:48-49` (four refused
attempts of 64 names, 18:33:57→18:38:19, attempt 5 spawns — the "256 refused registrations" arithmetic holds),
also 64 at `GtLaneKaidoku.md:84`, `GtLaneTsukuroi.md:72`, `GtMoriR17W2.md:122`; 66 at `GtLaneKama.md:72`; 68 at
`GtLaneChousa.md:61`, also `GtLaneKaidoku.md:86`; 70 at `GtMoriR17W1.md:109`; 71 at `GtLaneKaidoku.md:83`; 72 at
`GtLaneKama.md:73`; 78 at `GtLaneKaidoku.md:80`; 86 at `GtLaneKama.md:74-75`; 88 at `GtLaneKagi.md:58`; 95 at
`GtLaneKama.md:68` ("refused_attempts: members 95, spawned 0"); 100 at `GtLaneKaidoku.md:82`. The lead-in
quotes also match: `GtLaneKasegi.md:48` carries the full "Failed to start background task jobs: KasegiR23.FixMirror:
Background job limit reached (100)" line, `GtLaneKama.md:72` the "seats 66, refused 66, spawned 0" record.

Independently of the wave-1 sweep, I re-ran `git grep -n -i refus 5f00fd0… -- .ufo/waves/round-20/build` (74
lines, full output read) and extracted every job-cap refusal count: the set is exactly {64, 66, 68, 70, 71, 72,
78, 86, 88, 95, 100} — the landed enumeration is complete and "No single-wave refusal count in the round-20/build
records exceeds 100" holds. Remaining `refus` hits are other senses (province refusal fences, refusal-envelope
receipts, "refused 0" entries, receipt counts of 4/3/7) and name no count outside the set.

### 3.6 SOURCES rows S138–S141

Rows at `corpus/SOURCES.md:144-147` of the rev's blob. Each row's scope, anchor, dates and used-by were checked
against the commits themselves (§3.4): ids map 944d7f8d→S138, e398f831→S139, 6962d5cd→S140, c4a2441d→S141 in
that order, matching the lesson Gate table and U1's narrative; all four rows are `mined`, opened 2026-10-22,
`used-by` `corpus/knowledge/harness-job-capacity-r25.md`. S138's "touches only CHANGELOG, settings-schema.ts,
sdk.ts" is true (diff count 3). S140's anchor names sdk.ts:1949 and the parent pins :1797/:1811 — both exact.
S141's anchor names sdk.ts:1964 — exact. No in-place edits of older rows were needed for R7 and none were made
(rows S133–S137 belong to other routed items and are out of my scope).

### 3.7 Entry and lesson consistency

Both entries carry the "Round-27 corrections (routed R7; wave-1 seat ReviewR7Knowledge)" blocks applied in place
by MoriR27 under the standing QUALITY 77 rule (`corpus/QUALITY.md`, cited at
`.ufo/waves/round-26/w1/CriticC1Width.md:120` and `corpus/lessons/round-25.md:163`), and the round-27 lesson's
R7 disposition row (fixed in place, four source rows S138–S141) matches what is committed. The entry front
matter changed by exactly the required amount: S138–S141 added to `source:` and `recheck:`; S105/S111 were
already cited at `5fa0a00f` (L1).

## 4. Sources opened (URL, access time, sha256)

All curl'd to scratch, pinned with `grep -n`/`awk NR` on the downloaded bytes; fetched 2026-10-22 between the
two stamped endpoints 17:09:51Z (psi.c) and 17:18:48Z (the 476b858 patch):

- …/torvalds/linux/v7.2/kernel/sched/psi.c — 17:09:51Z, `452318beaca3e6d1…3312c5`, 1725 lines.
- …/torvalds/linux/v7.2/Documentation/accounting/psi.rst — `11c6b7129103b454…2692`.
- …/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst — `a9433bb0e16a67f0…b7ad`.
- …/torvalds/linux/v7.2/kernel/cgroup/cgroup.c — `3d4a256adea52d7e…9a8c`.
- …/can1357/oh-my-pi/45c35e40…: sdk.ts `c0228addd4cfe93c…e957`, tools/settings.ts `514974143d47db0c…0507`.
- …/can1357/oh-my-pi/6962d5cd…: sdk.ts `84f3a112a670f36d…3e633`; parent d9bc4fbd: sdk.ts
  `fde5a959e3a310be…2104`; c4a2441d: sdk.ts `4f4897502a75b0b4…9186`.
- Commit patches (github.com/…/commit/<sha>.patch): 944d7f8d `478b972ac7ccd9db…83b`, e398f831
  `c7696f91ed13a395…f87b`, 6962d5cd `0c8fa1ee3d1a241b…2e7`, c4a2441d `a4e2e4db4c03937c…5c29`, 476b858
  `00f6cbb0b786dd84…1257` (17:18:48Z).

Lane records were read only at the attacked rev via read-only `git show`/`git grep` (never the working tree,
which has moved to `b97b2e3f…`).

## 5. Residual risk and verification gaps

- The F10 claim is worded about the round-20/build record files, and my completeness sweep covered those files
  (*.md) at the rev; the underlying JSON attempt files the records cite were not re-opened, matching the entry's
  own scoping ("the counts recorded there").
- `register()`'s runtime `get()` was not executed (bounds: never run omp); U1's floor statements are scoped to
  visible bytes and I verified them at that scope only.
- sdk.ts history was pinned at the five commits and v18.12.6; commits between 476b858 and 944d7f8d were not
  walked hunk-by-hunk, but the 944d7f8d hunk shows the exact pre-state U1 describes, so the narrative chain is
  anchored at both ends of each step.
- Linux files read at tag v7.2 only, matching the entries' version bounds.
- The read tool was not used on URLs this session (all pins from `grep -n` on curl'd bytes), so wave-1 §6's
  line-drift incident was neither reproduced nor contradicted.

## 6. Tooling record

No installs or upgrades (directive satisfied without): curl, grep, awk, sha256sum, git (read-only `show`,
`grep`, `rev-parse`, `cat-file` in the lane). pacman untouched (transactions paused host-wide). Privacy: no
harness settings values, session ids or paths, journal MESSAGE text, uid/pid lists, earlyoom flag values, or
routing-table key names appear above; lane-record quotes carry seat names and refusal counts only.

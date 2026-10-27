# Mo54CritC2Axis — attack C2 as a depth move on new ground

Seat: `Mo54CritC2Axis`. Scope: axis fit (depth vs coverage), ground newness, PROVINCE fit,
sibling bleed. Data commit measured: `78295c764093ff1f6cee08d7246679900bde7265`; entering tip
`39dcf4d7e410d362781a47e8365ca23b5c807598`. Read-only review; no vote lines (this seat is not a
RECHECK/ENTAILMENT voter — no line below begins with those tokens; where vote syntax is quoted
it sits inside sentences). Scratch `/fast/scratch/hyaku/mori-r54/Mo54CritC2Axis/` created for
scratch compliance, unused for fixtures, removed.

## Axes named (per `/home/vgpnk/Projects/shokunin/AXES.md:9-16`)

- **depth**: verifiable technical detail — decision tables with real thresholds, named error
  signatures, cited sources; signal "a reader can act on SKILL.md alone".
- **coverage**: fraction of the domain's real surfaces the skill governs; signal "PROVINCE.md
  lists every surface".
- **adjacency**: evidence belonging to another domain reported, not absorbed.

## Verdict

**C2 is correctly a depth claim, not coverage or mere expansion — with named limits.** The
entry `corpus/knowledge/memory-failure-kills-r54.md` carries the depth signal verbatim: a
decision table (kernel line → meaning / non-meaning) at `memory-failure-kills-r54.md:53-61`, a
sysctl → behaviour table with real values and defaults at `:63-67`, named error signatures
(`Memory failure:` prefix, `BUS_MCEERR_AR`/`BUS_MCEERR_AO`, the four `MF_*` outcome words), and
six cited sources pinned to tag v7.3. No new measured surface is claimed: `tools/` gains
nothing, `mori-census.sh` gains no `SURFACE`, and the worktree PROVINCE draft explicitly says
"no probe, census surface or tool reads it yet" (worktree `PROVINCE.md:466`, uncommitted — see
below). Lane precedent credits corpus decision-table entries as depth: `SCORECARD.md:12` names
round 31's "watchdog identity decision table" and rounds 47–50 C2 entries as depth-improved
with score held at 5. A coverage claim would need a new governed surface; none is asserted.
The README "coverage additions" block (`corpus/README.md:771-776`) is a per-round ledger name,
not an axis label — round-53 filed a *freshness* ledger under the same heading, so filing under
it does not refute the depth axis.

**Residual axis caveat (calibration, not correctness):** the depth that AXES.md names lives in
the decision table and Boundaries; `count-c2.py` measures only the header, the claim|source|
quote table, copies and votes. The counter can read `met` with the decision table deleted —
frozen, so a named limit for the report and a round-55 routing item, not a fix proposal.

## Ground newness — new for the kill class, but with three qualifications

Command (as assigned):
`git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n -iE 'memory.failure|hwpoison|SIGBUS|BUS_MCEERR|HardwareCorrupted' 39dcf4d7e410d362781a47e8365ca23b5c807598 -- .` (exit 0).

- The contract's "only hit is a recheck-ledger quote" (`contract.md:65-66`) reproduces under the
  sweep's own scope: `evidence/sweeps.txt:7-9` greps only `corpus/knowledge SKILL.md PROVINCE.md
  tools` and gets one file, `corpus/knowledge/kernel-v7.3-recheck-r53.md`. No claim table,
  SKILL row, PROVINCE line or tool names the class — **the kill class is new ground**.
- Qualification 1 — the panic-switch ground was not new: `corpus/SOURCES.md:353` (at the tip)
  carries the round-53 lead "`panic_on_unrecoverable_memory_failure` … a kill/panic surface for
  mori's kill-event frontier; `mm/memory-failure.c` at v7.3 not opened", and
  `corpus/README.md:764-765` repeats it. The sweep file names it as the lead
  (`sweeps.txt:15-17`), so the L1 disclosed it — but "at the entering tip no entry, SKILL row,
  PROVINCE line or tool names this class" (`contract.md:65-66`) is true only because SOURCES and
  README are outside the sweep pathspec. Wording survives; the lead was already on record.
- Qualification 2 — two surfaces were present as context, not claimed: `HardwareCorrupted`
  occurs in `corpus/evidence/sources-r51/{meminfo.c.v7.2:137,proc.rst.v7.2:1099,1268}` and was
  even an overclaim counterexample in round 51 (`.ufo/waves/round-51/w1/Mo51CritEntail12.md:36`);
  `EHWPOISON` sits in the round-48 errno copies (`corpus/evidence/sources-r48/errno.h:123`),
  though `quota-observability-r48.md` claims no EHWPOISON row (grep of the entry: only S481
  EDQUOT rows). `PageHWPoison` appears in `sources-r47/mm_page_alloc.c` and shmem source
  context. None of this was *claimed knowledge*; the class is still new, but "never seen the
  surfaces" would overstate it.
- Qualification 3 — SIGBUS-as-kill was context in `.ufo/waves/round-14/build/SignalCoverage.md`
  (coredump signal coverage) and `sources-r42/S241.html`/`sources-r45` (HugeTLB SIGBUS), all
  outside the kill-event class claim.

## PROVINCE fit — kill events are Core-adjacent; the line that should change

`PROVINCE.md` at the data commit (`git show 78295c76:PROVINCE.md`):

- Owns (lines 6-10): "kill/OOM-related catalog-ID records and signal-11 coredump records … plus
  cgroup `memory.events`" — enumerates OOM-path evidence only.
- Core row (line 24, "**Kill/OOM classes**"): catalog IDs for kernel-OOM unit notices, oomd
  notices, coredumps, unit-process SIGKILL, unit failures, signal-11 coredumps; `memory.events`.
  A reader of Core alone cannot find `memory_failure/*` counters, `HardwareCorrupted` or
  `ras:memory_failure_event` — the owned kill-event class is under-enumerated at the canonical
  row.
- No Frontier row names it (FR1–FR15 checked; FR1/FR10/FR13 are OOM-adjacent only).

**The PROVINCE line that should change: line 24 (the `## Core` "Kill/OOM classes" row)** —
extend the enumeration with the non-OOM kill class (memory-failure SIGBUS/SIGKILL; surfaces
`node<N>/memory_failure/*`, `HardwareCorrupted`, `ras:memory_failure_event`), or hold the class
as named Core ground pending a census surface. Line 8-9 (the `**Owns**` paragraph) is the
secondary enumeration of the same gap. Because lane convention is append-only ("this section is
appended at EOF, so no line moves", `PROVINCE.md:449-450`), the in-flight worktree draft
(`PROVINCE.md:458-467`, modified but uncommitted at review time — `git status` shows
` M PROVINCE.md`) implements exactly this: a "Hardware memory-failure kills (kill events,
knowledge only)" note pointing at the entry and disclaiming any probe. That drafting choice is
correct and sufficient; an FR16 frontier row becomes owed only if a future round builds a
counter/`SURFACE` read (route to round 55 planning).

## Sibling bleed — none into owned ground; one ownerless cession

Fleet-wide grep `grep -inE 'EDAC|rasdaemon|hwpoison|memory.?failure|machine.?check|hardware.?health'
…/*/PROVINCE.md`: the only real hits are mori's own uncommitted draft (`mori-shokunin/PROVINCE.md
:464-471`) plus coincidental matches (mado "tripwire", souji "argv"). Tsukuroi's province owns
"host OS, package, systemd-unit, driver, firmware, and boot diagnosis"
(`../tsukuroi-shokunin/PROVINCE.md`, cited at mori `PROVINCE.md:66`) and a *storage* health
frontier (NVMe SMART, `storage-health-r26.md`) — memory-error detection hardware is not claimed
anywhere. The three tsukuroi corpus files matching the pattern are redaction/tooling notes
(`adjacency-anchors-r19.md:276`, `boot-writers-r19.md:166`, `path-reconciliation-r23.md:38` —
all "MCE" inside other words or capture-hygiene), not health claims.

- No bleed: detection-and-report only; the entry cedes injection/unpoison/sysctl writes
  correctly (`memory-failure-kills-r54.md:78-80`, draft `PROVINCE.md:468-469` → tsukuroi/operator).
- Ownerless cession (LOW): "corrected-error accounting (EDAC, `rasdaemon`, MCE decoding) is
  hardware-health ground the lane does not hold" (`memory-failure-kills-r54.md:81-82`, draft
  `PROVINCE.md:469-470`) names no owner. EDAC is a driver/firmware surface — plausibly
  tsukuroi's by the driver-diagnosis clause. Smallest safe correction: "routed to tsukuroi"
  or "unclaimed; routed to the integrator" in the draft Boundaries line.
- `ras:memory_failure_event` shares its trace subsystem with RAS/EDAC tooling; fine to cite as
  kill evidence today, but the draft should name the boundary once so a future probe doesn't
  absorb RAS telemetry wholesale (same line as above can carry it).

## Entry wording — the strongest counterexample (row 1, hash fcf9f378a818)

Claim: "Every message the memory-failure handler prints starts with the same prefix, `Memory failure:`".

Committed copy `corpus/evidence/sources-r54/memory-failure.c.v7.3`:

- `:37` `#define pr_fmt(fmt) "Memory failure: " fmt` — true for all `pr_*` calls *above* line 2716.
- `:2716-2717` `#undef pr_fmt` / `#define pr_fmt(fmt) "Unpoison: " fmt`; `unpoison_pr_info`
  emits e.g. `:2754` `"%#lx: disabled after HW memory failure"`. Console lines there start
  `Unpoison:`, not `Memory failure:` — emitted by this file's handler functions.
- `:1243` `WARN_ONCE(1, "Memory failure: pfn=%#lx, invalid nid=%d", …)` and `:1262` the
  `mf_result` twin print on console as `WARNING: …` lines; `:1295`
  `panic("Memory failure: %#lx: unrecoverable page", pfn)` prints as
  `Kernel panic - not syncing: Memory failure: …`. Both carry the tag but neither line
  *starts* with it.

So "every message … starts with the same prefix" is false as worded in three ways (different
prefix in the unpoison section; WARNING and panic console prefixes around the literal text).
The operational signature survives — every handler message *contains* `Memory failure:` or
`Unpoison:` — but the claim cell asserts starts-with. Smallest safe correction is a reword
such as "the handler's messages carry one of two prefixes, `Memory failure:` in the main file
and `Unpoison:` in the unpoison section, so a reader can attribute the line" (new hash; two
fresh entail votes under the frozen kill rule). Severity MED: decision-table attribution is
unaffected, but ENTAILMENT voters judging strict entailment could legitimately mark overclaim.

Related soft spots found while attacking (all LOW, listed for the record, not overclaim votes):

- Decision table `:55` — verified against the copy: `kill_proc` (`:292`) prints the
  "Sending SIGBUS" line before *both* the forced `BUS_MCEERR_AR` (`:296`) and unforced
  `BUS_MCEERR_AO` (`:305`) sends, and `collect_procs` feeds both early and late paths — the
  cell's AO/AR split is correct. A failed send also prints `pr_info("Error sending signal…",
  :308)` in addition to the `:483` "Cannot send advisory machine check signal" line the entry
  cites; two failure line shapes exist, the entry names one. Attribution-safe either way.
- Row 8 (`f5e240db68c0`): `action_name[]` at `:871-876` has exactly four members — the claim
  holds verbatim.
- Row 11 (`5a235a277033`): `panic_on_unrecoverable_mf` (`:1273-1274`) fires only on
  `MF_MSG_KERNEL` ("reserved kernel page", `:879`) + `MF_IGNORED`; `MF_MSG_KERNEL_HIGH_ORDER`
  ("high-order kernel page", `:880`) is mapped `MF_IGNORED` at `:2478` and correctly does not
  panic — the claim's "reserved kernel page" wording is precise. `sysctl_panic_on_unrecoverable_mf`
  default-off confirmed by `__read_mostly` initialization pattern.
- Row 16 (`734269273c22`): the quote ("When enabled, this sysctl triggers a panic…") does not
  itself carry the version; "Version 7.3 adds" rests on `evidence/sweeps.txt:30` (absent on
  7.2.11) and the round-53 vm.rst diff. Correct, but the entailment evidence for the word
  "adds" lives outside the row's quote — a voter may note it.
- `verified-at` header (`:6`) says quotes located "by `count-c2.py`"; `count-c2.py` locates
  quotes but does not verify the decision-table prose — consistent with the limit named above.

## PROVINCE summary for the L1

- Line to change: `PROVINCE.md:24` (Core "Kill/OOM classes" enumeration) — the class belongs to
  Core-adjacent kill-event ground; the append-only draft at worktree `:458-471` already covers
  it in house convention; no Frontier row owed until a probe exists.
- Draft corrections worth landing with it: name an owner (or "unclaimed, routed") for the
  EDAC/rasdaemon/MCE cession at draft `:469-470`; one clause noting `ras:` trace subsystem is
  shared with RAS tooling.

## Commands run (evidence)

```sh
git -C …/mori-shokunin grep -n -iE 'memory.failure|hwpoison|SIGBUS|BUS_MCEERR|HardwareCorrupted' \
  39dcf4d7… -- .            # exit 0; hits only in sources/wave files + SOURCES.md:353 + README.md:764
git -C …/mori-shokunin show 78295c76:PROVINCE.md | grep -n …   # Owns :6-10, Core kill row :24, FR1-FR15, no memory-failure row
git -C …/mori-shokunin diff 39dcf4d7 78295c76 -- PROVINCE.md    # empty: PROVINCE unchanged at data commit
git -C …/mori-shokunin status --porcelain                       # ' M PROVINCE.md' (draft uncommitted)
git -C …/mori-shokunin diff PROVINCE.md                         # appended Round-54 scope notes :458-476
grep -inE 'EDAC|rasdaemon|hwpoison|memory.?failure|machine.?check|hardware.?health' …/*-shokunin/PROVINCE.md
# only mori draft :464-471; no sibling owns memory hardware health
grep -nE 'printk\(|dev_err' corpus/evidence/sources-r54/memory-failure.c.v7.3   # exit 1, none
grep -n 'pr_fmt' corpus/evidence/sources-r54/memory-failure.c.v7.3              # :37 "Memory failure: ", :2717 "Unpoison: "
sed -n '280-320p;1236-1300p' corpus/evidence/sources-r54/memory-failure.c.v7.3  # kill_proc send path; WARN_ONCE :1243/:1262; panic :1295
grep -nE 'action_name|MF_MSG_KERNEL' corpus/evidence/sources-r54/memory-failure.c.v7.3  # :871-880 four outcomes; :1274 type==MF_MSG_KERNEL
grep -inE 'EHWPOISON|hwpoison|SIGBUS' corpus/knowledge/quota-observability-r48.md       # no claim rows (S481 EDQUOT only)
```

## Findings

- **MED — `corpus/knowledge/memory-failure-kills-r54.md:25` (row 1, hash `fcf9f378a818`)**:
  "Every message … starts with the same prefix" is falsified by `pr_fmt` redefinition to
  `"Unpoison: "` at `memory-failure.c.v7.3:2716-2717` (lines start `Unpoison:`), and by
  console prefixes on `WARN_ONCE` (`:1243`, `:1262`) and `panic` (`:1295`) where the literal
  `Memory failure:` text is payload, not line start. Fixable by reword (new hash + two fresh
  `entailed` votes per the frozen kill rule); the signature itself is sound for attribution.
- **MED — `PROVINCE.md:24` (Core "Kill/OOM classes" row, at `78295c76`)**: the owned kill-event
  class is enumerated as OOM-path evidence only; memory-failure kills are under-enumerated at
  the canonical row. The worktree draft (`:458-467`) repairs it append-only; keep it, plus the
  two draft-line tweaks below.
- **LOW — worktree `PROVINCE.md:469-470` / `memory-failure-kills-r54.md:81-82`**: the
  EDAC/rasdaemon/MCE cession names no owner ("hardware-health ground the lane does not hold").
  Name tsukuroi (driver-diagnosis clause) or mark unclaimed+routed; add one clause that the
  `ras:` trace subsystem is shared with RAS tooling so future probes don't absorb it.
- **LOW — `contract.md:65-66` wording**: "no entry, SKILL row, PROVINCE line or tool names this
  class" holds only under the sweep pathspec (`sweeps.txt:7`); `SOURCES.md:353` and
  `README.md:764-765` already named the panic-switch lead. Cosmetic; the kill *class* is
  genuinely new.
- **LOW — `memory-failure-kills-r54.md:30` (row 6) / decision table**: the entry cites only
  "Cannot send advisory machine check signal" as the undelivered-signal line; the copy also
  prints `pr_info("Error sending signal to %s:%d: %d")` at `:308`. Two failure shapes, one
  named — attribution still safe.
- **LOW — row 16 (`734269273c22`)**: "Version 7.3 adds" is not carried by the row's quote; the
  version fact rests on the round-53 diff and the host absence read. Entailment is still
  defensible (claim-text + corpus context), noted so voters don't re-derive it blind.
- **LOW — `count-c2.py` scope (routed, frozen)**: the counter measures header/table/votes, not
  the decision-table or Boundaries sections where the depth signal lives; `C2=met` is
  attainable with those sections deleted. Named limit; round-55 item, not a change request.
- **LOW — `memory-failure-kills-r54.md:34` (row 10) nuance**: `num_poisoned_pages_inc` +
  `update_per_node_mf_stats` also skip `MF_MSG_PFN_MAP`; the entry's "raw PFN mappings" covers
  it — verified, no defect, recorded for completeness of the attack.

Axes verdict recap: **depth claim — axis correctly assigned; ground new for the class (with the
three qualifications above); PROVINCE covers it only via the pending draft — land draft
`PROVINCE.md:458-471` plus the owner-naming tweak; no sibling bleed found.** The one substantive
attack that lands is row 1's prefix universal (MED).

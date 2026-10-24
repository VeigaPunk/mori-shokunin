# ConnectSiblingPsi — round 24 wave 1, claim C2 sibling-ownership scan

Seat: MoriR24.ConnectSiblingPsi (connector, read-only leaf). Date 2026-10-22.
Lane tip read: `4059ffb` (contract landed at `29c1bf4`). Writes: this file only.

## Bottom line

No sibling contests mori's C2 (one-shot, read-only system PSI as fleet resource runway).
Tsukuroi is the only sibling with a real PSI surface. It reads system
`/proc/pressure/memory` inside its own census for OS memory triage, and its province
explicitly routes fleet correlation of host pressure to mori. That is shared evidence,
not shared ownership. No sibling owns or reads CPU, IO or IRQ PSI as a capability.
Three boundary risks and one verification gap are listed below.

## Scan method and coverage

- Pattern set over `PROVINCE.md`, `SKILL.md` and `corpus/` in every
  `/home/vgpnk/Projects/shokunin/*-shokunin/` except mori: `\bPSI\b`, `/proc/pressure`,
  `cpu.pressure`, `irq.pressure`, `io.pressure`, `memory.pressure`, `pressure stall`
  (case-insensitive), `psi.c`, `CONFIG_PSI`, `\bpsi=`, `oomd`.
- Hit counts per lane (rg): tsukuroi 50, audio 30, every other sibling 0 (chousa,
  game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kasegi, kengaku, kotoba, kotodama,
  kumitate, lore, mado, revenger, souji, tabi, tameshi).
- A second case-insensitive `pressure` scan over every sibling `PROVINCE.md` and `SKILL.md`
  turned up only tsukuroi rows and unrelated uses of the word: `game-dev-3d-shokunin/SKILL.md:76,182`
  (temp-dir and quota pressure), `kengaku-shokunin/SKILL.md:58` ("off-path web pressure")
  and `kotoba-shokunin/SKILL.md:59`.
- Kama, which I checked first as instructed: zero PSI-token hits. A broader `stall|pressure|oomd` scan
  matched only the substring in "install" (for example `kama-shokunin/PROVINCE.md:56,67`;
  `kama-shokunin/SKILL.md:130,137`). Kama has no pressure surface.

## Evidence by sibling

### tsukuroi — adjacent owner of OS memory diagnosis; same file, different question

| What | Pointer | Bearing on C2 |
|---|---|---|
| Domain: package state, systemd, drivers/firmware, journal/boot; no PSI in Core list | `tsukuroi-shokunin/PROVINCE.md:3-14` | CPU, IO and IRQ PSI are not tsukuroi Core |
| "Host memory and kill-event measurements support OS triage; they do not establish which fleet wave caused pressure ... fleet correlation belongs to mori" | `tsukuroi-shokunin/PROVINCE.md:30-33` (cites `../mori-shokunin/PROVINCE.md:6-16`) | Explicit cession of fleet-side pressure reading to mori |
| "Shared evidence is not shared ownership" | `tsukuroi-shokunin/PROVINCE.md:41` | Two lanes reading one file is not a contest |
| ADJ-04: host pressure needing fleet/wave correlation → mori; tsukuroi retains "OS memory, journal and boot diagnosis"; minimum evidence includes "exact counter or PSI command/exit and observed value" | `tsukuroi-shokunin/PROVINCE.md:49` (cites `../mori-shokunin/PROVINCE.md:3-16`) | The boundary C2 must respect: mori reads and correlates, tsukuroi diagnoses OS memory cause |
| OUT-001 proposition: "fleet correlation of host pressure is mori's, not OS triage" | `tsukuroi-shokunin/PROVINCE.md:121` | Same cession, pinned to mori `91940fa…` bytes |
| Census memory-pressure arm reads system `/proc/pressure/memory` (default path) | `tsukuroi-shokunin/tools/tsukuroi-census.sh:376` | **Exact file overlap** with C2's `memory` resource |
| C6 parses only `some avg300`, `full avg300`, `full total`; unreadable → named unknown `C6-psi` | `tsukuroi-shokunin/tools/tsukuroi-census.sh:1100-1115` | Tsukuroi uses `[ -r ]` only, so absent, unsupported and unreadable all collapse to "unknown". C2's split into those states is finer, and both lanes treat unavailable as never zero, so they agree |
| C6 documented in skill | `tsukuroi-shokunin/SKILL.md:909-929,1013-1035` | The arm can only worsen the drivers verdict; it carries no threshold on PSI |
| PSI field-swap mutant M15 ("some-avg300 value read from `total`") was not caught because "no case asserts any C6 PSI value"; repair battery B13 uses "distinct avg300 and total" | `tsukuroi-shokunin/corpus/knowledge/memory-arm-ver-s8.md:124,144` | Shows the same class of mutant would survive C2's cases. This drives the proposed move below |
| D6 "unreadable PSI silently skipped" was caught by the `degraded-mem-psi-unknown` case | `tsukuroi-shokunin/corpus/knowledge/memory-arm-mutants-s8.md:56,105` | Matches C2's rule that an unreadable resource is a state, not zero |
| Round-1 lesson: rejected treating wording as a measured health threshold; PSI readings "do not prove ... harmful pressure" | `tsukuroi-shokunin/corpus/lessons/round-1.md:9` | Tension with C2's `PRESSURE_HIGH` exit 1 (see contradiction 1) |
| Packet TSUKUROI-F1-MEM-01: "do not reconstruct an event from cumulative PSI" | `tsukuroi-shokunin/corpus/knowledge/adjacency-handoffs-fleet-r1.md:95-112` | Mori already received this packet (`mori-shokunin/PROVINCE.md:71-88`). C2's `total` and `total_delta_us` must not be presented as dated events |
| Standing gap row 11, "pre-kill capture": "PSI live-only"; the remedy is "operator-installed capture (cgtop/PSI logging or a full monitor)" | `tsukuroi-shokunin/corpus/knowledge/kill-event-deep-r8.md:265`; also `oom-event-plane.md:301`, `SKILL.md:1124` | C2 (one-shot) does **not** close this. A retained PSI series belongs to mori FR12 (Frontier) or to the operator, and this is latent future overlap, not a present contest |
| IRQ appears only as device IRQ numbers in the driver inventory | `tsukuroi-shokunin/corpus/knowledge/driver-firmware-plane.md:63-64` | No IRQ PSI ownership. Attributing a high `irq` reading to a driver or device would fall under tsukuroi's driver plane (`PROVINCE.md:12-13`), not mori's |

### audio — consumer of a raw CPU PSI line, no ownership claim

- `audio-shokunin/corpus/live/r88-boundary/scripts/r88b_probe.py:653,661,724` runs
  `cat /proc/pressure/cpu | head -1` (the `some` line only) next to `/proc/loadavg`
  around its own CPU-hog leg, and writes the result to `hog-load-*.txt` (`:662-663`). This is
  load context for an audio measurement.
- The other 27 audio hits are the comment "backpressure stall hazard" in copies of
  `measure_audio.py` (for example `audio-shokunin/corpus/fixtures/measure_audio.py:55727`).
  These are unrelated to PSI.
- `audio-shokunin/PROVINCE.md` has no pressure, loadavg or PSI text, and audio has no `SKILL.md`.
  There is no contest. Using only the first line is correct for system CPU, because C2
  labels system `cpu full` as undefined.

### souji — supports mori ownership

- "routes liveness or resource findings to mori. Complementary." `souji-shokunin/PROVINCE.md:51-52`;
  also `:154`.

### Outside sibling corpora (second-order, fleet root, not a sibling claim)

- `scripts/hyaku/wave-slot.sh:8-9` justifies the slot gate by "a seat workload spike stalled
  memory at 20% PSI full", but the gate reads only `MemAvailable` (`:68`,
  `MIN_AVAIL_MB` default 6144 at `:21`). The gate is a dispatch control; mori refuses
  dispatch mechanism (`mori-shokunin/PROVINCE.md:12`), and kumitate and the operator own it.

## Mori-side anchors that C2 integration touches

- Mori Core already claims "resource runway (... memory pressure)" (`mori-shokunin/PROVINCE.md:10,26`)
  and the user-slice `memory.pressure` read (`tools/mori-census.sh:224,308,1728-1759`;
  `SKILL.md:19,41`). FR12 boundary: `PROVINCE.md:55`.
- Mori's tsukuroi adjacency row (`mori-shokunin/PROVINCE.md:65`) names only `systemd-oomd`,
  `earlyoom`, `memory.events` and `MESSAGE_ID` as shared hits. It does not record that both lanes
  read system `/proc/pressure/memory`.
- Tsukuroi cites mori with plain line ranges: `../mori-shokunin/PROVINCE.md:6-16` (tsukuroi
  `PROVINCE.md:33`) and `:3-16` (tsukuroi `PROVINCE.md:49`, ADJ-04). Its round-19 anchor checker
  hashes pinned commit objects (`git show <commit>:<path>`,
  `tsukuroi-shokunin/tools/check-adjacency-anchors.py:447-464`), so mori edits do not break
  OUT-001, OUT-005 or OUT-007. Inserting lines into mori `PROVINCE.md:3-16` would still shift
  the two live line-range pointers, for example moving "Detection and report only" (`:16`) out of range.

## Contradictions (stated, not scored)

1. **Threshold stance.** Tsukuroi admits PSI only as exact readings without any harm threshold
   (`tsukuroi-shokunin/corpus/lessons/round-1.md:9`; `adjacency-handoffs-fleet-r1.md:101-104`).
   C2 emits `PRESSURE_HIGH` with exit 1 at a labeled-local `--warn-avg10` default of 10.0
   (`contract.md:63-64`). The two are compatible only while mori's knowledge entry and SKILL
   row keep the threshold labeled local and uncalibrated (FR8, `mori-shokunin/PROVINCE.md:51`)
   and never describe the reading as OS-memory harm. If a reader treats exit 1 as a host-health
   verdict, the reading crosses into ADJ-04's "Tsukuroi retains OS memory ... diagnosis".
2. **Scope of "fleet" runway.** C2 reads system-wide PSI, which includes non-fleet load. Tsukuroi's
   cession covers "fleet correlation of host pressure". A system-wide `PRESSURE_HIGH` is therefore
   host evidence that mori may correlate, not proof that the fleet caused the pressure. Mori's
   own packet reading already says this (`mori-shokunin/PROVINCE.md:73,88`, "Correlation is not
   causation"), and the C2 knowledge entry should carry the same sentence.

## Proposed move (one, bounded)

**Carry tsukuroi's field-identity falsifier over to C2's frozen cases before they land.**
Within the twelve declared topics, P01 ("four normal low files", `contract.md:78`) should use
`some` and `full` lines whose `avg10`, `avg60`, `avg300` and `total` are pairwise distinct
(for example `avg10=0.11 avg60=0.22 avg300=0.33 total=444`). Its `expect.resources.<r>.some/full`
should assert all four fields, not a subset. P06 and P07 should also keep `avg60` and `avg300`
different from the `avg10` value they test.

- Why this is not obvious: the shared interface matches expected `some` and `full` objects as a
  **subset** (assignment "Matching" rule). A natural fixture shortcut, such as `avg10=avg60=avg300=25.00`
  in P06, would let a parser that reads `avg300` (or `avg60`) as `avg10` still pass 12/12. That is
  exactly how tsukuroi's M15 went undetected (`memory-arm-ver-s8.md:124`) until B13 added distinct values (`:144`).
- Affected axes: coverage (C2) gains an assertion that fails if the parser reads the wrong field.
  Calibration is not harmed: there is no new tool behavior, case count or threshold. Adjacency is
  not harmed: no sibling file is touched. The declared after-value stays `PASS 12/12`.
- Timing: `tools/fixtures/mori-pressure/cases.json` is not yet in the lane tree
  (`git ls-tree -r --name-only HEAD` at `4059ffb` lists no pressure path) and not in
  `/fast/scratch/hyaku/mori-r24-a2/wt-cases` or `wt-pressure` (both at `29c1bf4`, no fixtures directory).
  The move is free only before the cases freeze. After freezing, it becomes a falsifier mutant
  (below) and must not be applied as a case edit. I sent a short note to `MoriR24` with this
  pointer because of that timing.

### Secondary, adjacency-only (no new capability)

When C2 records its scope in mori `PROVINCE.md`, append a round-24 note, following the pattern of
rounds 17 to 23, rather than inserting lines into `:3-16`. Add one sentence to the tsukuroi
adjacency context saying that tsukuroi's census also reads system `/proc/pressure/memory`
(`tsukuroi-shokunin/tools/tsukuroi-census.sh:376,1100-1115`) for OS triage. Also say that a
`PRESSURE_HIGH` on `irq` that needs device or driver attribution routes to tsukuroi's driver
plane, and that C2 does not close tsukuroi's pre-kill capture gap
(`kill-event-deep-r8.md:265`) or mori FR12.

## Risks

- If the cases are already frozen when this lands, changing P01 would count as editing a frozen
  case. In that case, use the falsifier only.
- Asserting full `some` and `full` objects ties P01 to exact float formatting. The output contract
  says floats (`contract.md:68`), so `0.11` round-trips, but a tool that rounds `avg` values would fail.
  That would be a real contract finding, not noise.
- Wording risk (contradictions 1 and 2): a `PRESSURE_HIGH` exit code consumed by the slot gate or
  another dispatcher would turn a labeled-local threshold into a dispatch control. That crosses mori's
  refusal of dispatch mechanism (`PROVINCE.md:12`) and kumitate's ownership. Nothing in C2 does this
  today. Note it, but do not add it.

## Verification (for the L1 or the falsifier seats; none run by me)

1. Field-swap mutant, sandbox only: in a copy of `tools/mori-pressure.py` under
   `/fast/scratch/hyaku/mori-r24-a2/`, make the parser store `avg300` into `avg10` (and separately
   `avg60` into `avg10`), then run `python3 -I tools/mori-pressure.py --selftest`. Expected result: at least one
   case FAILs. If it still prints `PASS 12/12`, the cases have the M15 gap.
2. Same with a mutant that reads `total` from `avg300`. Expected: P11 or P01 fails.
3. Re-run `grep -n 'PSI' ../tsukuroi-shokunin/PROVINCE.md` against the landed mori `PROVINCE.md` and
   confirm that `../mori-shokunin/PROVINCE.md:3-16` still spans Domain through "Detection and report only".

## What I ran and did not run

- Ran (read-only): rg scans over sibling `PROVINCE.md`, `SKILL.md` and `corpus/`; reads of the cited files;
  `git log`, `git ls-tree`, `git rev-parse` in the mori lane; `ls` and `git log` in the two sandbox clones;
  `cat /proc/pressure/irq` (one `full` line, `total=5954608`, no `some` line, which matches `contract.md:58`).
- Not run: tsukuroi's census or anchor checker, mori's census, any selftest, and any mutant. No PSI trigger
  was registered and nothing was written outside this report.
- Tool installs or updates: none.

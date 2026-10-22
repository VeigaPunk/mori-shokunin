# Wave 2 — Reopen S090 and S091

Seat: MoriR24.ReopenS090S091 (leaf; no subagents used, no installs — stock `curl`, `sha256sum`, `awk`, `wc` sufficed).
Scratch: `/fast/scratch/hyaku/mori-r24-a2/w2/ReopenS090S091/` (fetched bytes kept there; lane repo untouched, read-only).

## Method

Re-fetched both URLs fresh on 2026-10-22 and hashed the fetched bytes:

```
curl -fsSL -o psi.rst https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst
curl -fsSL -o psi.c   https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c
sha256sum psi.rst psi.c
```

Output:

```
11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692  psi.rst
452318beaca3e6d19ab81a16528ae6b1695828a9ed080e329d07dedd9a3312c5  psi.c
```

Then verified every claimed anchor against the fetched bytes by reading the named line
ranges, and checked the located quotes by extracting the exact lines with awk
(indentation stripped, lines joined with one space) and comparing to the Gate string.
Quote convention note: both multi-line quotes strip the source lines' leading
whitespace (psi.c uses tab indent; psi.rst lines 57-58 have none) and join with a
single space — same normalization the Gate applies to every row, so I score exactness
under it.

## S090 — Linux PSI accounting documentation v7.2 (psi.rst) — AGREE

- **SHA-256 prefix**: `11c6b7129103b454` matches my fetch exactly (`11c6b7129103b4547c31…`).
- **Located quote** (Gate, `corpus/lessons/round-24.md:25`, range 57-58): exact match on the
  line join — psi.rst:57 `CPU full is undefined at the system level, but has been reported`
  + psi.rst:58 `since 5.13, so it is set to zero for backward compatibility.` Word count 23
  (`wc -w`), within the 25-word cap.
- **Anchors** (Gate row and SOURCES teaches cell), all confirmed in the fetched bytes:
  34-35 heading "Pressure interface"; 37-38 file set "…/proc/pressure/ -- cpu, memory,
  and io."; 40-43 the some/full line format; 45-46 some meaning; 48-55 full meaning;
  57-58 system CPU full rule; 60-65 ratios in % over ten/sixty/three-hundred-second
  windows and total in us; 81-88 trigger write format plus the two examples; 102-110
  "The kernel accepts window sizes ranging from 500ms to 10s, therefore min monitoring
  update interval is 50ms and max is 1s." plus the unprivileged 2s-multiple limit;
  118-119 de-register on close. File is 188 lines; no anchor exceeds it.
- **Scope cell**: honest. The document names only cpu, memory and io for /proc/pressure/
  (psi.rst:37-38) and the cell claims exactly that; the cgroup2 section exists at 181-185
  but v7.2-only scope is stated, which the bytes are.
- **Teaches cell**: every clause checks against the bytes. "Names only cpu, memory and
  io" ✓ (37-38); "each named file shows a some line and a full line" ✓ (40-43 format);
  some/full meanings ✓ (45-46, 48-55); "avg10/60/300 are percentages over 10/60/300-second
  windows and total is absolute stall time in microseconds" ✓ (60-65, "in us");
  "system-level CPU full is undefined and exported as zero since 5.13" ✓ (57-58, and
  confirmed by the emitter guard in psi.c:1282-1283); "trigger windows are accepted from
  500ms to 10s, so the minimum monitoring update interval is 50ms and the maximum 1s" ✓
  (102-103, near-verbatim). The amendment recorded at `corpus/lessons/round-24.md:45-48`
  (old "each file is exactly two lines" → narrowed to cpu/memory/io, irq handled by S091)
  is consistent with the bytes: the doc never mentions an irq pressure file, and irq in
  fact prints only a full line (psi.c:1277 with `only_full`, verified under S091).

## S091 — Linux kernel/sched/psi.c at v7.2 — AGREE

- **SHA-256 prefix**: `452318beaca3e6d1` matches my fetch exactly (`452318beaca3e6d19ab8…`).
- **Located quote** (Gate, `corpus/lessons/round-24.md:26`, range 1282-1283): exact match on
  the line join — psi.c:1282 `/* CPU FULL is undefined at the system level */` +
  psi.c:1283 `if (!(group == &psi_system && res == PSI_CPU && full)) {`. Word count 21
  (`wc -w`), within the cap.
- **Anchors**, all confirmed: psi_show at psi.c:1251; psi_disabled → `-EOPNOTSUPP` at
  1257-1258; IRQ `!irqtime_enabled() && res == PSI_IRQ → -EOPNOTSUPP` at 1260-1263 (inside
  its `#ifdef CONFIG_IRQ_TIME_ACCOUNTING`); `only_full = res == PSI_IRQ` at 1273-1275;
  print loop `for (full = 0; full < 2 - only_full; full++)` at 1277; system-CPU-full zero
  guard and skipped avg/total fetch at 1282-1288; `seq_printf` some/full label and format at
  1290-1291; `psi_proc_init` at 1710-1721 with io/memory/cpu proc_creates at 1714-1716 and
  the guarded irq create at 1717-1719; psi_enable definition and `__setup("psi=",
  setup_psi)` at 145-159 region (claimed 145-158 — covers the key/psi_enable/setup_psi
  block, `__setup` line itself is 159, one line past the stated range: trivial, content
  intact); runtime switch `psi_init` with `if (!psi_enable) static_branch_enable
  (&psi_disabled)` at 230-243 (claimed 228-235: covers the branch head). File is 1725
  lines; no anchor exceeds it.
- **Scope cell**: honest. "Not cgroup pressure files, not trigger semantics, not this
  host's kernel" — those exclusions are stated, and the v7.2 file does contain them, so
  the restriction matters and is declared.
- **Teaches cell**: every clause checks. "One some line and one full line for cpu, memory
  and io but only a full line for IRQ" ✓ — loop bound `2 - only_full` (psi.c:1277) gives
  two iterations for cpu/memory/io and one for IRQ under CONFIG_IRQ_TIME_ACCOUNTING
  (1273-1275), and the label at 1291 prints "full" when `only_full`. "The system CPU full
  line is a fixed zero rather than a measurement" ✓ — the 1283 guard skips the avg/total
  fetch for exactly `psi_system`+`PSI_CPU`+full, leaving zeros printed (1288, 1290).
  "EOPNOTSUPP on the psi_disabled branch and, for IRQ, when IRQ time accounting is off" ✓
  (1257-1258, 1260-1263). "The /proc/pressure/* entries are created once at init, so a PSI
  switched off at boot leaves them absent rather than unreadable" ✓ — `psi_proc_init`
  (1710-1721) creates the files only under `if (psi_enable)`, inside `module_init`; with
  `psi=` disabled at boot nothing is created, and the EOPNOTSUPP static key (psi_init,
  232-234) is the read-time path that the (nonexistent) files never hit. This is exactly
  the M4 correction the round recorded (`corpus/lessons/round-24.md:57`).

## Residual risk and verification gaps

- The Gate's `accessed (UTC)` timestamps (2026-10-22T08:14:33Z / 08:14:54Z) are not
  independently verifiable after the fact; I can only confirm the bytes fetched today are
  identical to what was digested.
- Quotes are scored exact under the whitespace-normalizing join convention described
  above; if "exact" were defined to include raw indentation, both multi-line quotes would
  technically differ (psi.c tabs). Single-line quotes (S092-S094) are unaffected. The
  convention is uniform across the Gate, so I do not count it as a defect.
- psi.c anchor "psi_enable switch:145-158" ends one line before the `__setup("psi=",
  setup_psi);` registration (159); content claimed is present, boundary is 1 line short.
  Cosmetic.
- No tools were installed; pacman untouched.

## Verdict

S090: **agree** — hash, anchors, quote, scope, teaches all verified against re-fetched bytes.
S091: **agree** — hash, anchors, quote, scope, teaches all verified against re-fetched bytes.
No falsification found in either row.

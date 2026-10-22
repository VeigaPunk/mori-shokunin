# ReviewSkillProvince — wave 2 falsify: SKILL.md Round24, PROVINCE.md and corpus/README.md round-24 notes

Seat: MoriR24.ReviewSkillProvince (leaf, no subagents). Reviewed against the tools' real
behavior and `corpus/knowledge/system-pressure-r24.md`.

Tip note: the lane moved during review — review started at the measured wave tip
`a730ecfefbdb5c31b1db13aca2c40eecd5e97abc`, HEAD was `13208d2a` when probing began, and
five wave-2 response commits (`89849a7`, `6a344d2`, `a536b18`, `7c77fba`, `1046aca3`)
landed while I worked. **Every finding below was re-validated at `1046aca3ba6ef7d2646ad3a45addcfdebbf039bd`**
(working tree clean, no local mutation of the lane). All three target docs are pure appends
since base `c725aa37` (single `@@ -N,0 +N,M @@` hunks; `git diff -U0 c725aa37 HEAD --`
checked), so the "byte-unchanged" claims for `PROVINCE.md:55`, `corpus/README.md:343`,
`PROVINCE.md:6-10` and `PROVINCE.md:3-16` are true.

## Findings by severity

### M1 — knowledge entry claims "no rate is derived" for a regressed counter; the tool emits a negative rate (medium)

`corpus/knowledge/system-pressure-r24.md:178` (decision-table row, "Interval mode: second
`total` < first `total`") ends: "No rate is derived from it." The tool contradicts this.

Evidence (scratch fixture, all four files present, io `some`/`full` total 3000000 rewritten
to 500000 between the two reads, `--interval 0.2`):

```
python3 -I tools/mori-pressure.py --root <scratch>/f24-regressed-new --interval 0.2
verdict PRESSURE_PARTIAL, exit 0
io state counter_regressed
io some total_delta_us -2500000  stall_ratio -12.5
```

Code: `tools/mori-pressure.py:275-282` computes `total_delta_us` and `stall_ratio`
(lines 276-277) before the regressed downgrade (278-282) and returns the payload with the
negative numbers embedded; only system cpu `full` gets nulls (lines 270-274). The frozen
case P12 pins only `state: "counter_regressed"` (`tools/fixtures/mori-pressure/cases.json`,
P12 `expect.resources.cpu` — no delta/ratio keys), so the declared selftest
(`PASS 12/12`, verified, exit 0) cannot catch this contradiction.

Impact: the knowledge entry is the mapping authority the round-24 docs cite; a consumer
reading it would believe the JSON carries no rate for a regressed counter, yet
`stall_ratio: -12.5` is exactly the number `SKILL.md:634`'s "never infer that pressure fell
because the counter decreased" warns about. Fix is either tool-side (null both fields when
`STATE_REGRESSED`) or doc-side (correct the sentence to "the emitted delta and ratio are
negative and must not be consumed as a rate"). The wave-2 corrections section
(`system-pressure-r24.md:8-40`, bullet P4) edited the neighboring decreasing-total text but
left this sentence in place.

### M2 — SKILL registry verdict map omits counter_regressed from PRESSURE_PARTIAL (medium-low)

`SKILL.md:641` verdict-map cell: "`PRESSURE_PARTIAL` also exits 0 and means at least one
resource was unavailable or malformed". `counter_regressed` also produces PARTIAL/exit 0,
with no unavailable or malformed resource:

- Contract A3: "`counter_regressed` counts toward `PRESSURE_PARTIAL` like `malformed`".
- Knowledge entry `system-pressure-r24.md:178` (row says `PRESSURE_PARTIAL`, exit 0).
- Frozen case P12 itself: counter_regressed, `PRESSURE_PARTIAL`, exit 0 — and the selftest
  that cell declares passes 12/12.
- My probes f21/f24: exit 0, PARTIAL, io `counter_regressed`, cpu/memory/irq all `ok`.

A consumer of the registry verdict map will misread a PARTIAL caused solely by a regressed
counter. One-clause fix in the cell.

### L1 — SKILL.md Round24 table cites three v7.2 source ranges one line off, disagreeing with the knowledge entry (low)

Verified against fetched `raw.githubusercontent.com/torvalds/linux/v7.2` sources (copies in
scratch: `psi.c`, `psi.rst`):

- `SKILL.md:625` cites `psi.c:1281-1287` for the system-CPU-full zero export; the comment is
  at 1282, the `if (!(group == &psi_system && res == PSI_CPU && full))` guard at 1283, block
  close at 1288; 1281 is blank. The knowledge entry's anchor (`system-pressure-r24.md:84`,
  `psi.c:1282-1288`) is correct.
- `SKILL.md:629` cites `psi.c:1716-1717` for "the file is created only under
  `CONFIG_IRQ_TIME_ACCOUNTING`"; the `#ifdef` is 1717 and
  `proc_create("pressure/irq", ...)` is 1718 (1716 is the cpu `proc_create`). The knowledge
  entry's F6 anchor (1717-1719) is correct.
- `SKILL.md:633` cites `psi.c:1289` for the emitter; the `seq_printf` is at 1290 (1289
  blank). Knowledge entry F2 (1290-1296) is correct.

Same-section rows `:627` (1272-1276 / 1289-1290) and `:630` are acceptable after the
wave-2 correction to `:630`. Net effect: the operator-facing table and its own knowledge
entry contradict each other by one line in three places.

### L2 — stall_ratio may exceed 1: stated in the tool docstring and contract A3, absent from every scope doc (low)

`tools/mori-pressure.py:30` (docstring): "stall_ratio (nominal: delta / (S * 1e6), may
exceed 1)". Probe f22 (io total 1000000 → 1600000, `--interval 0.2`): `stall_ratio 3.0`,
verdict `PRESSURE_OK`, exit 0. But `system-pressure-r24.md:202-204` (interval limits
bullet), `SKILL.md:634`, `PROVINCE.md:236-258` and `corpus/README.md:449` all describe
`stall_ratio` without the unbounded/nominal property; a reader can take "ratio" as a 0..1
fraction. One clause in the knowledge entry's interval limit would close it.

### L3 — registry entry cell stale against the tool landed in wave 2 (low)

`SKILL.md:641` entry cell lists `[--root DIR] [--warn-avg10 X] [--interval S]
[--selftest]`. The tool gained `--cases FILE` (`tools/mori-pressure.py:389-390`, "run this
case file instead of the frozen cases.json", commit `89849a7`, with
`tools/fixtures/mori-pressure/supplementary-cases.json`), and the selftest now prints a
second stdout line (`MATCHER: rejected 48/48 corrupted expectations`). The declared
after-value is unaffected (`MORI_PRESSURE_SELFTEST: PASS 12/12` still printed, exit 0 —
re-run at the new tip), but the cell's argument list and output description no longer match
the parser.

### L4 — malformed enumeration misses two tool behaviors (low)

`SKILL.md:633` enumerates malformed triggers as "(duplicate kinds, a missing required kind,
a non-decimal avg, a non-integer or negative total)". The tool also reports malformed for:

- a negative decimal average — probe f16 (`avg10=-1.00`): state `malformed`, note "line
  does not match the PSI grammar", PARTIAL exit 0;
- non-UTF-8 file content — probe f25 (io containing `\xff\xfe garbage`): state `malformed`,
  note "file content is not UTF-8 text; resource malformed, never reported as zero"
  (behavior added in `6a344d2`/`89849a7`). No scope doc mentions the UTF-8 rule (grep for
  utf-8/UTF-8 in SKILL.md, PROVINCE.md, corpus/README.md, system-pressure-r24.md: no hits).

Both read as an exhaustive list as written.

### Nits (cosmetic; listed, no action demanded)

- `SKILL.md:613` and the C2 registry cell use `python3 tools/mori-pressure.py`; the
  knowledge recheck line and the C1 row use `python3 -I`. Harmless (stdlib-only tool),
  inconsistent.
- `SKILL.md:641` self-test cell says error injection "(EOPNOTSUPP, EACCES)"; the tool
  docstring (`tools/mori-pressure.py:46-50`) documents four errnos (adds EPERM, ENOENT),
  the sleep hook and the matcher controls. Narrower, not false.

## Attack results on the named angles

- **Wrong states:** none found. All six states exercised: ok (f01), absent (f07/f08),
  unreadable via EACCES mode-000 (f14), malformed (f09-f13, f16, f19, f25),
  counter_regressed (f21/f24); `unsupported` is reachable only through the selftest's
  in-process injection on this host (knowledge P2 says the psi_disabled branch is not
  reachable through `/proc` on v7.2 — consistent with SKILL:630 as corrected in `a536b18`).
- **Wrong exit codes:** none found beyond M2's wording gap. Verified: OK/PARTIAL → 0,
  HIGH → 1 (f03-f06), UNAVAILABLE → 2 (f08), usage errors → 2 (`--interval 0`, `--interval
  11`, unknown flag, missing `--root`, negative `--warn-avg10`), selftest PASS → 0.
- **Overclaim "Core advance stated as admitted": not substantiated.** Every Core mention in
  scope is qualified: `PROVINCE.md:236` "admission pending", `PROVINCE.md:283` "pending
  admission by the non-author closure", `corpus/README.md:445` heading "(admission
  pending)", `corpus/README.md:457` "Advanced to Core (pending admission)"; `SKILL.md`'s
  Round24 section claims no Core status at all (only "stay Frontier", `:616`/`:635`).
  `PROVINCE.md:274-278` records the owns-scope extension as recorded-now, but under the
  pending-admission row and explicitly append-only — defensible.
- **Missing limits:** L2 (ratio unbounded) and L4 (undocumented malformed inputs) are the
  gaps found. The other carried limits check out against the knowledge entry: the root
  `cgroup.pressure` freeze (PROVINCE:267-273 ↔ strengthened U7 at `system-pressure-r24.md`
  corrections), local-uncalibrated threshold (output `threshold.label` is literally
  "local (not calibrated)"; probe f03 finding detail repeats it), host-scope caveat,
  one-shot/dwell boundary (`surfaces-r8.md:47-48` really is the <50 ms condition the notes
  cite; `--interval` adds ~S seconds and cannot meet it).

## Confirmed claims (survivors, re-run at tip 1046aca3)

- Declared after-value: `python3 -I tools/mori-pressure.py --selftest` prints
  `MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0.
- Live host run: `PRESSURE_OK`, all four `ok`, `irq` `some: null`, system cpu `full` total 0
  with `full_system_undefined: true` — matches `PROVINCE.md:279-283`.
- Threshold arms: `some` of cpu/io/memory and `full` of memory/io/irq fire
  `PRESSURE_HIGH`/exit 1 (f03-f06); equality fires (f05, avg10 == 10.0); system cpu `full`
  avg10=99 produces no finding (f02); findings name resource and kind with the
  local-not-calibrated label.
- Interval mode: per-kind `total_delta_us`/`stall_ratio`; system cpu `full` pinned to
  null/null (f17, matches A3 and P11); worse-state merge with no delta (f19); thresholds
  use the second read when both reads are ok (f20); `elapsed_us` measured outside selftest.
- Read-only: tool opens `"r"` only, writes stdout only, no subprocess
  (`tools/mori-pressure.py:157,398,537` area) — matches `SKILL.md:614-616`,
  `PROVINCE.md:250-256`, `corpus/README.md:449`.
- Provenance: `f6a29702` (cases freeze) is a strict ancestor of `6ee6248` (tool landing)
  and `cases.json` exists at `f6a29702`; `SKILL.md:641`'s new wording ("landed in a
  strict-ancestor commit before the tool; the tool seat read the cases while building, so
  the order is shown, not independence") is accurate — note the contract C2 sentence
  ("written by a seat that does not see the implementation") remains stronger than anything
  the lane now claims; the doc wording is the honest one and closure should reconcile the
  contract phrasing.
- PROVINCE:284-288 adjacency citations verified in the sibling repo:
  `tsukuroi-shokunin/tools/tsukuroi-census.sh:376` (`PRESSURE_FILE=.../proc/pressure/memory`)
  and `:1100-1115` (C6 PSI block); `tsukuroi-shokunin/PROVINCE.md:30-33` ("fleet correlation
  belongs to mori").
- `SKILL.md:642` "thirteen sandbox mutants" matches `.ufo/waves/round-24/w1/BuildRoutedCheck.md:190`
  ("13 mutants"); mutant execution itself is another seat's assignment.

## Residual risk and verification gaps

- `unsupported` was never observed on a real host (per the corrected knowledge entry it is
  arguably unreachable on v72 `/proc` reads); its note wording is verified only through the
  selftest path and code read.
- I did not execute the thirteen routed-check mutants or audit
  `supplementary-cases.json` contents (outside the declared after-value; other seats).
- Kernel anchors were spot-verified only for the psi.c/psi.rst ranges cited by the Round24
  table; the S093/S096 fixes in `7c77fba` and the corrections section's new anchors
  (`init/main.c`, `tsc.c`, `psi.c:845-857`, ...) were not re-verified here.
- The census-untouched claims ("no SURFACE row, no census finding id") rest on the
  append-only diffs of my three docs plus the tool diff; a full repo-wide census diff was
  not re-derived beyond `git diff --stat a730ecf..HEAD` showing only `.ufo` wave-2 files.

## Tools record

No installs or upgrades performed (operator directive record): system `python3` and `curl`
already present; two kernel source files fetched by URL into scratch only. All fixture
probes ran under `/fast/scratch/hyaku/mori-r24-a2/w2/ReviewSkillProvince/` (`probe.sh`,
f01-f25 outputs, fetched `psi.c`/`psi.rst`). No pacman, no `uv`, no service or host writes;
the lane repo received only this report file.

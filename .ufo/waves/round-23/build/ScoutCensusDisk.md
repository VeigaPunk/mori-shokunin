# ScoutCensusDisk — how a separate quota probe must be registered

Scope: registration conventions only (gate vs probe, verdict map, selftest spelling,
census integration). Detection/report only; no edits outside this file.

Sources read (primary, at the lane revision on 2026-10-21):
- `.ufo/waves/round-23/contract.md` (C2: lines 65–152)
- `tools/mori-census.sh` — `probe_cgroup` 1680–1863, `probe_disk` 1897–1976,
  run order 2704–2708, finding-id block 254–273, pin/drift comments 195–205,
  disk/quota comment 353–357
- `SKILL.md` — Gates table 156–182, Window probe (r16) 105–111, disk section
  397–425, `Never edit tools/mori-census.sh` 515, r21/r22 registry tables 517–544
- `/home/vgpnk/Projects/shokunin/PROTOCOL.md` Gate standard 376–406
- `PROVINCE.md:45` (FR2), `SCORECARD.md:1413–1429` (round-23 declaration),
  `frozen/c2-expected-real.json`

No candidate implementation was read (`build/ImplQuota`, `.scratch/round23/ImplQuota`
untouched); cases-proposed contents were not read. Text reads/grep were used; no LSP
server covers these shell/markdown registry surfaces in this seat's toolset, so there
is no semantic-navigation claim here.

## 1. Answer in one line

Register `tools/mori-quota-surface.py` as a **`probe`** row named `quota surface (r23)`
in a new round-23 registry section of `SKILL.md` (same 8 columns as `SKILL.md:162`),
with the contract's exit map written as `probe, not a gate: rc0 … · rc1 … · rc2 …`,
selftest spelled `python3 tools/mori-quota-surface.py --selftest`. **Census
integration is out of scope this round and must not happen**: the contract registers a
standalone probe measured by an oracle, and `SKILL.md:515` says never edit
`tools/mori-census.sh`.

## 2. Kind: probe, not gate — evidence

- PROTOCOL defines a gate as a script that "reads surfaces, compares them against
  expected values persisted in its own repo, and returns a verdict"; "a tool that
  cannot fail is a probe, and is registered as one" (`PROTOCOL.md:377-380`).
- C2's rc1 is explicitly **not** failure: "`QUOTA_ENABLED` is a runway-reporting
  finding … not a failure claim" (`contract.md:132-134`). PROTOCOL's gate map makes
  rc1 mean `failed` fleet-wide (`PROTOCOL.md:380-382`); this probe's rc1 is positive
  observability evidence.
- FR2 is observe-and-report only: "observe and report only, never change quota state"
  (`PROVINCE.md:45`). The probe classifies host state; it does not compare to a
  persisted expected table.
- Existing precedent: observational rc1 tools are registered as `probe` —
  `seat terminal status (r17)` (`SKILL.md:173`), `misroot sweep (r17)`
  (`SKILL.md:176`), `retained-loss audit` (`SKILL.md:521`).
- The thing that does compare against persisted expected values is the wave oracle
  (`oracle-quota.py` over `frozen/quota-cases/`, `contract.md:142-145`). Wave-local
  oracles are not registry rows: round 22's `oracle-reconcile-v2.py` is named only in
  the pinned-values cell (`SKILL.md:538`), never as its own row.

[OBSERVED for all bullet points; INFERENCE only for calling the oracle "wave-local
by r22 analogy".]

## 3. The exact row (recommended bytes)

Placement: append a section after the round-22 section (`SKILL.md:534-564`), because
rounds 20–22 stopped extending the main table (rows end at r19, `SKILL.md:182`) and
each registered its own table with the identical header (`SKILL.md:519,536`):

```markdown
## Round23 quota-surface probe (FR2 capability, read-only)

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| quota surface (r23) | probe | `python3 tools/mori-quota-surface.py [--path ABS ...]` (default: fleet root `/home/vgpnk/Projects/shokunin` then `/tmp`) `\| --fixture FILE \| --selftest` | probe, not a gate: rc0 `QUOTA_DISABLED` (no visible enabled mechanism — not health) · rc1 `QUOTA_ENABLED` (positive runway evidence; `df` capacity % cannot see quota exhaustion; not a failure claim) · rc2 `QUOTA_STATE_UNKNOWN` (no enabled path, at least one unknown) · rc2 `QUOTA_SETUP` (usage/setup; no partial verdict); no severity, no DRIFT, never changes quota state | `python3 tools/mori-quota-surface.py --selftest` — synthetic `mori-quota-fixture-v1` cases only, no host reads; asserts exit code + `finding_id`; tally measured at L1, not predicted | none live; `.ufo/waves/round-23/frozen/c2-expected-real.json` real control; sealed `.ufo/waves/round-23/frozen/quota-cases/` + `oracle-quota.py` bind the before/after | stdout only (one `mori-quota-surface-v1` JSON object); real mode reads only `/proc/self/mountinfo`, `os.stat`/`os.path.realpath` of each path and mount-source basename, `/sys/fs/btrfs/*/devices/` and `<uuid>/qgroups` (+ `mode`); never `quotactl`/`btrfs`/`xfs_quota`/`repquota`/`mount`, never writes; `--fixture` does no host reads | mori |
```

Notes on the row:
- Name carries the round suffix like `journal window (r16)` / `misroot sweep (r17)`
  (`SKILL.md:172,176`).
- Do not add the same row to the main table as well; the lane has one inventory per
  tool, and duplicated rows appear nowhere in the existing tables.
- The `verdict map` cell uses the journal-window idiom verbatim in form
  (`SKILL.md:172`): `probe, not a gate:` prefix, `rcN` + stable finding id, then an
  explicit denial of severity/DRIFT. Do not map rc0 to "clean"/"health": the contract
  defines disabled as absence of a *visible* mechanism, and the limits paragraph says
  qgroup presence ≠ a limit set (`contract.md:136-140`).
- rc2 is overloaded by two finding ids by contract precedence (`contract.md:132-134`).
  The row must declare both; a consumer distinguishes them by `finding_id` (and by the
  JSON `exit_code` field, which the contract requires to agree with the process rc).

## 4. Verdict map — exact semantics to preserve

Ordering is contract-fixed (`contract.md:132-134`):
1. setup error → rc2 `QUOTA_SETUP` (unknown args, relative paths, `--fixture` together
   with `--path`, unparseable/missing fixture keys) — never a partial verdict.
2. any path `enabled` → rc1 `QUOTA_ENABLED` (an unknown sibling never hides it).
3. else any path `unknown` → rc2 `QUOTA_STATE_UNKNOWN`.
4. else rc0 `QUOTA_DISABLED`.

The registry row must not describe rc2 `QUOTA_STATE_UNKNOWN` as "failed" (a gate word)
nor rc0 as a clean bill of health. It is also not a DRIFT signal: the probe prints one
JSON object and no severity field; alarm semantics never enter this row.

## 5. Selftest spelling

- Lane spelling for Python tools is `--selftest` (`SKILL.md:172-176,521`), and the
  contract CLI includes `--selftest` (`contract.md:73-74`). Spell exactly:
  `python3 tools/mori-quota-surface.py --selftest`.
- The cell should state the isolation property the contract gives: synthetic
  `mori-quota-fixture-v1` mode, **no host reads**, asserting exit code + stable
  finding id (PROTOCOL self-test clause, `PROTOCOL.md:385-389`). A parser/import-only
  check is not a valid selftest.
- No `TMPDIR=` prefix by default: the probe emits stdout only and `--fixture` performs
  no host reads, so it matches `journal window`/`seat terminal status`/`misroot sweep`
  rather than the temp-writing rows (`SKILL.md:178,181-182,538`). If the implementation
  creates temp files anyway, the registry cell must become
  `TMPDIR=$PWD/.scratch python3 tools/mori-quota-surface.py --selftest`, matching the
  r18/r21/r22 rows and the fleet's no-`/tmp` rule.

## 6. Pinned values and write scope

- Frozen names must be path-qualified under `.ufo/waves/round-23/frozen/`: a bare
  frozen name matching more than one `.ufo/waves/*/frozen` root fails closed
  (`PROTOCOL.md:405-406`). Use `.ufo/waves/round-23/frozen/c2-expected-real.json` and
  `.ufo/waves/round-23/frozen/quota-cases/`.
- `frozen/c2-expected-real.json` is a real host control (exit 0 `QUOTA_DISABLED`;
  fleet root btrfs `/home`, `btrfs_qgroups_dir_absent`,
  `device_check=btrfs_subvolume_skipped`; `/tmp` xfs `xfs_noquota_option`,
  `device_check=match`). Its own note says a later differing run is a drift
  observation, not an oracle rewrite.
- The oracle path in the row (`oracle-quota.py`) is **[INFERENCE]** from the round-22
  layout (`.ufo/waves/round-22/oracle-reconcile-v2.py` at wave root). At report time
  the wave root holds only `oracle-rename.py`; `frozen/quota-cases/` does not exist
  yet. The names, not the bytes, are contract-fixed (`contract.md:142`).
- Write scope must enumerate the contract's real-mode inputs and deny everything else
  (`contract.md:75-80,67-70`): no `quotactl`, no `btrfs`/`xfs_quota`/`repquota`, no
  `mount`, no writes; never echo mount sources, other options, or values of option
  keys. `--fixture` is the no-host-read arm.

## 7. Census integration: out of scope (and should stay out)

Yes — out of scope this round, on four independent grounds:

1. **Contract.** C2 registers a *separate* probe and measures it with an oracle over
   sealed cases; no SURFACE row, finding id, alarm, verdict, or census edit appears
   anywhere in C2 (`contract.md:65-150`). The target claim is coverage capability,
   not census behavior.
2. **Lane rule.** `SKILL.md:515`: "Never edit `tools/mori-census.sh`." That statement
   sits with the r20/r21 re-pin material and is unconditional in wording.
3. **Direct precedent.** The r16 journal probe is the exact template: "the production
   census does not call it, adds no `SURFACE` or `FINDING` row, and changes no alarm,
   drift verdict or positive token. The r10 drift pin stays red and is not re-pinned
   by this change" (`SKILL.md:105-111`). The quota probe has the same shape.
4. **Census mechanics.**
   - The census has no quota machinery and no quota input paths: `probe_disk`
     (1897–1976) parses only `df -P`; `probe_cgroup` (1680–1863) reads only
     `/sys/fs/cgroup`; the only `quota` token is a comment explaining that the
     fleet's disk failures are EDQUOT events a capacity-% probe cannot see
     (`tools/mori-census.sh:353-357`). There is no `/proc/self/mountinfo` or
     `/sys/fs/btrfs` read, and no `python3` child call (the sole `python3` token is a
     comment, line 1695).
   - The run order is a fixed seven-probe list with no quota probe
     (`tools/mori-census.sh:2704-2708`).
   - Finding ids are declared a "stable compare contract" in the script header
     (`tools/mori-census.sh:254-273`), and the drift pin compares the full normalized
     output; an added line is reported as `+FINDING`/`+SURFACE`
     (`tools/mori-census.sh:195-205`). Injecting a quota SURFACE/FINDING would
     therefore register as census drift against
     `corpus/evidence/baseline-r10-20261015T2231Z.json` (`SKILL.md:165,298`) — a
     separate calibration event, not this capability claim.
   - Census live inputs are env-overridable and fixture-selftested; quota's
     mountinfo/sysfs inputs have no census override, so integration would need new
     env knobs, fixtures, drift-volatile decisions, and its own pre-registration.

Consequence for measurement: before/after is the oracle's `capability_absent` → all
sealed cases match (`contract.md:142-145`), plus the frozen real control. The probe is
never called by `tools/mori-census.sh`, and the census bytes stay unchanged in C2.

## 8. Convention deviations to flag to L1

- **Finding-id prefix.** Every existing probe uses `MORI_`-prefixed ids
  (`MORI_JOURNAL_WINDOW_*`, `MORI_SEAT_TERMINAL_*`, `MORI_MISROOT_*`,
  `SKILL.md:172-176`), but the frozen contract fixes bare `QUOTA_DISABLED` /
  `QUOTA_ENABLED` / `QUOTA_STATE_UNKNOWN` / `QUOTA_SETUP` and the oracle compares
  `finding_id` exactly. The registry must copy the contract ids verbatim; do **not**
  normalize them to `MORI_QUOTA_*`. Because the contract is frozen, this is a
  contract-fixed exception, not a row-writer choice.
- **Source rows are missing.** The contract cites S077–S084 as opened this round
  (`contract.md:67`), but `corpus/SOURCES.md` ends at S076 (123 lines; last entry
  "Bounded search13"). A registry/prose citation to S077–S084 would be dangling until
  those rows land. This is a seal-time precondition, not a reason to alter the row.
- **Prose section.** The row alone is thinner than the lane's probe precedent: pair it
  with a short section carrying the fixed limits (`contract.md:136-140`) and the
  "census does not call it / adds no SURFACE or FINDING row" sentence, mirroring
  `SKILL.md:105-111`. The checklist requires every observation to name its command
  and the revision measured; the row's entry command plus a measured revision line
  satisfies it.
- **Wording risk.** The two easiest false claims for a later writer: calling rc1
  `QUOTA_ENABLED` a failure/DRIFT, and calling rc0 `QUOTA_DISABLED` health or proof
  that no limits exist. Both are contradicted by `contract.md:132-140` and
  `PROVINCE.md:45`.

## 9. Remaining unknowns

- Exact oracle filename/path and sealed-case count after L1 seals (only "oracle
  `oracle-quota.py`" and "`frozen/quota-cases/`" are contract text).
- Whether L1 prefers the round-section table (r21/r22 precedent, recommended) over an
  append to the main table; the row bytes are identical either way, but only one
  location should receive it.
- Whether the implementation writes any temp state during `--selftest` (decides the
  `TMPDIR=` prefix; contract implies none).
- S077–S084 source text and their assigned tiers, since those rows are not yet in
  `corpus/SOURCES.md`.

No blocker: every question asked is answerable from the contract, PROTOCOL, the
census probes, and the registry precedents above.

Confidence: high on kind=probe, verdict-map ordering/wording, selftest spelling, and
census-out-of-scope; medium on the oracle path/case count (explicitly marked
inference).

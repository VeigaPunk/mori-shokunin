# ReviewS124Supersede — routed D3: S124 in-place `teaches` change (round 26)

Seat: MoriR27.ReviewS124Supersede, 2026-10-22. Leaf; read-only on the lane except this file.
Sandbox (all experiments): `/fast/scratch/hyaku/mori-r27/ReviewS124Supersede/`.

## Verdict

1. **Rule 2 breach confirmed.** Round-26 commit `16935e2` ("round-26: S124 teaches corrected …")
   changed three S124 cells in place — `scope`, `anchor`, `teaches`. CORPUS.md Rule 2 allows
   in-place changes only to `status`, `recheck`, `used-by` (CORPUS.md:116-118, in
   /home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md). The correction must
   move to a new row whose `teaches` opens `supersedes S124 —` (CORPUS.md:118), and S124's three
   cells must be restored to the pre-round-26 text.
2. **The routed premise is wrong in one detail.** `git show 248408f5:corpus/SOURCES.md` contains
   **no S124 row** (grep exit 1). 248408f5 = "round-25 verifier spot-check (integrator, hyaku)",
   2026-10-22 09:28:23 -0300, and S124 was born later in round 26 (commit `327fbcc`). The
   original text therefore comes from `327fbcc:corpus/SOURCES.md:130`, not 248408f5.
3. **`status: superseded` is not available.** The validator accepts only `queued|mined|rejected`
   (scripts/sources-census.sh:4; enum check and E07 printf at scripts/sources-census.sh:658-659).
   Setting `superseded` makes `validate` exit 1 (falsifier C below). S124 stays `mined`; the
   supersession lives entirely in the new row's `teaches`.
4. **Restoring S124 is required by the contract, not by the validator.** Falsifier D shows an
   append-only fix (new row, S124 left edited) also exits 0 — the validator cannot see the
   breach. Only Rule 2 makes the restore mandatory.
5. Drafts (a) and (b) below are falsifier-passed: applied together they keep `validate` at
   exit 0 with zero new findings (falsifier B).

## Evidence

### The rule

- CORPUS.md:116-118: "2. **Append-only.** Only `status`, `recheck` and `used-by` change in
  place, and each change is logged old→new in the round lesson. A correction is a new row whose
  `teaches` opens `supersedes S0NN —`."
- Round-27 contract line 89: "Round-26 D1–D6 … are fixed or explained in
  `corpus/lessons/round-27.md`" — so this D3 fix is landed via the round-27 lesson.

### What round 26 actually changed (cell-level, `327fbcc` vs working copy)

Computed by cutting both S124 rows on `|` and comparing cells; commits `327fbcc` (row born,
original) and `16935e2` (in-place correction, current `corpus/SOURCES.md:130`):

| Cell | Changed | Note |
|---|---|---|
| 6 `scope` | yes | "…mean **and which cgroups systemd-oomd monitors**, systemd 262 only…" → "…mean, **which cgroups systemd-oomd monitors and which are kill candidates**, systemd 262 only…" |
| 7 `anchor` | yes | `1545-1547` → `1545-1548`; `:48-52` clause added; "(…wave-1 seat SrcResourceControlV262 also assigned)" → "(…checked by wave-1 seat SrcResourceControlV262)" |
| 8 `teaches` | yes | the documented old→new (round-26.md:88-92) |
| 9 `status`, 10 `opened`, 11 `recheck`, 12 `used-by` | no | unchanged |

Logging gap: `corpus/lessons/round-26.md:88-92` records only the `teaches` old→new plus "anchor
gains `systemd-oomd.service.xml:48-52`". The `scope` cell change and the `1545-1547`→`1545-1548`
anchor widening are **unlogged**. Round-27's lesson should log the full three-cell old→new.

### Fresh re-open (both URLs, today)

- https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml —
  HTTP 200, accessed 2026-10-22, sha256 `d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8`
  (matches the hash already recorded in S124's anchor).
- https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml —
  HTTP 200, accessed 2026-10-22, sha256 `4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d`
  (matches the hash already recorded in S124's anchor).
- resource-control.xml:1545-1548: "When set to <option>auto</option>, systemd-oomd will not
  actively use this cgroup's data for monitoring and detection. However, if an ancestor cgroup
  has one of these properties set to kill, a unit with auto can still be a candidate…"
- oomd.service.xml:43-44: "Cgroups of units with ManagedOOMSwap= or ManagedOOMMemoryPressure= set
  to kill will be monitored."; :48-51: "only descendant cgroups are eligible candidates for
  killing… only leaf cgroups and cgroups with memory.oom.group set to 1 are eligible candidates".

## Answers to the routed questions

- **Accepted statuses** (so `validate` stays exit 0): `queued`, `mined`, `rejected` only —
  scripts/sources-census.sh:4 and :658-659 (E07). There is no `superseded`.
- **Is restoring S124's original teaches required?** Yes. Rule 2 (CORPUS.md:116-118) makes the
  in-place `teaches`/`scope`/`anchor` edit out of contract; the corrected teaching moves to the
  new `supersedes S124 —` row and S124 reverts. The restore is a contract requirement; the
  validator does not enforce it (falsifier D).
- **Do any of status/recheck/used-by need to change on S124?** No. None is required for
  validity; the supersession is expressed by the new row. (One used-by consequence is an
  integration choice, see "Integration notes" item 3.)
- **Why the new row can reuse S124's URL in the same scope without tripping E04:** E04
  (duplicate URL within scope) is waived when `teaches` matches `/supersedes S[0-9]{3}/`
  (scripts/sources-census.sh:646-649, regex at :648). Keeping the scope string identical to
  S124's also keeps W04 (cross-scope duplicate URL, warning) silent.

## Draft (a) — new `supersedes S124` row (paste-ready)

Id shown as `S127` = next unused in the working copy (max is S126). Round-27 C1 will open rows
S127+ (round-27 contract.md:23-24), so the integrator must substitute the **next free id at
landing time**; nothing else in the row depends on the id (the E04 waiver regex needs only
"S" + 3 digits). Append directly after the S126 row, inside `## Registry`.

```
| S127 | systemd v262 resource-control and systemd-oomd manual pages — https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml and https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml | docs | A | what `ManagedOOMSwap=`/`ManagedOOMMemoryPressure=` `auto` and `kill` mean and which cgroups systemd-oomd monitors, systemd 262 only; not this host's unit values (tsukuroi-owned) | systemd.resource-control.xml:1545-1548 (`auto`: not actively used for monitoring; an ancestor set to `kill` can still make the unit a kill candidate); systemd-oomd.service.xml:44 (units set to `kill` are monitored) and :48-52 (only descendant leaf cgroups, or cgroups with `memory.oom.group=1`, are candidates); HTTP 200 on 2026-10-22, sha256 d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8 and 4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d (re-opened by ReviewS124Supersede; hashes match the S124 anchor) | supersedes S124 — On systemd 262 systemd-oomd monitors only cgroups of units set to `kill`; a unit left at the default `auto` is never monitored itself and becomes a kill candidate only under a `kill` ancestor, so an inactive or unconfigured oomd is unavailable evidence, not a quiet killer. | mined | 2026-10-22 | on-release | corpus/knowledge/userspace-oom-killers-r26.md |
```

Notes: `status` `mined` (an existing knowledge entry cites it — see item 3 below), `opened`
2026-10-22 (this re-open), `recheck` `on-release` (tag-pinned like S124). Scope is deliberately
identical to S124's (restored) scope string so no W04 warning appears; using a different scope
wording would add a W04 warning only — `validate` still exits 0 (scripts/sources-census.sh:16).

### Gate block for the round-27 lesson (house style follows round-26.md:59-67)

```
| S127 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml | 2026-10-22 | :1545-1546 "When set to auto, systemd-oomd will not actively use this cgroup's data for monitoring and detection." | admit, A, mined (supersedes S124; ReviewS124Supersede) |
| S127 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml | 2026-10-22 | :43-44 "Cgroups of units with ManagedOOMSwap= or ManagedOOMMemoryPressure= set to kill will be monitored."; :48-51 "only descendant cgroups are eligible candidates for killing" | admit, A, mined (supersedes S124; ReviewS124Supersede) |
```

Quotes are ≤25 words each (16, 13 and 8 words), verbatim from the fetched bytes listed above.

## Draft (b) — S124 exact old → new (restore direction)

Three cell-level replacements on `corpus/SOURCES.md:130`; cells `status`/`opened`/`recheck`/
`used-by` stay exactly as they are (`mined | 2026-10-22 | on-release |
corpus/knowledge/userspace-oom-killers-r26.md`). Each line: NEW (restored, = `327fbcc` original)
← OLD (current, round-26 edited).

```
scope  NEW: what `ManagedOOMSwap=`/`ManagedOOMMemoryPressure=` `auto` and `kill` mean and which cgroups systemd-oomd monitors, systemd 262 only; not this host's unit values (tsukuroi-owned)
scope  OLD: what `ManagedOOMSwap=`/`ManagedOOMMemoryPressure=` `auto` and `kill` mean, which cgroups systemd-oomd monitors and which are kill candidates, systemd 262 only; not this host's unit values (tsukuroi-owned)

anchor NEW: systemd.resource-control.xml:1545-1547 (`auto`: not actively used for monitoring; an ancestor set to `kill` can still make the unit a candidate); systemd-oomd.service.xml:44 (units set to `kill` are monitored); HTTP 200, sha256 d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8 and 4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d (opened by the L1; wave-1 seat SrcResourceControlV262 also assigned)
anchor OLD: systemd.resource-control.xml:1545-1548 (`auto`: not actively used for monitoring; an ancestor set to `kill` can still make the unit a kill candidate); systemd-oomd.service.xml:44 (units set to `kill` are monitored) and :48-52 (only descendant leaf cgroups, or cgroups with `memory.oom.group=1`, are candidates); HTTP 200, sha256 d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8 and 4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d (opened by the L1; checked by wave-1 seat SrcResourceControlV262)

teaches NEW: On systemd 262 a unit left at the default `auto` is not monitored by systemd-oomd unless an ancestor is `kill`, so an inactive or unconfigured oomd is unavailable evidence, not a quiet killer.
teaches OLD: On systemd 262 systemd-oomd monitors only cgroups of units set to `kill`; a unit left at the default `auto` is never monitored itself and becomes a kill candidate only under a `kill` ancestor, so an inactive or unconfigured oomd is unavailable evidence, not a quiet killer.
```

No `status → superseded` edit. The round-27 lesson logs this old→new (all three cells) and marks
D3 fixed there (round-27 contract.md:89).

## Falsifiers (all runs on copies; real lane only read)

Command shape:
`scripts/sources-census.sh validate --today 2026-10-22 <sandbox-lane-dir>`; sandbox lanes carry a
full copy of `corpus/` plus the non-corpus used-by targets (e.g. `SKILL.md`) so E11 resolves.

| Run | State | Result |
|---|---|---|
| A | pristine copy of lane corpus | exit 0, `ok`, 6 pre-existing W04 warnings (S035, S037, S073–S076) — identical to a read-only validate of the real lane |
| B | draft applied: S124 three cells restored **and** S127 supersedes row appended | exit 0, `ok`, same 6 W04s, **zero new findings, zero new warnings** |
| C | B + S124 `status` set to `superseded` | `E07 S124 status=superseded`, **exit 1** — `superseded` is not a legal status |
| D | S127 row appended, S124 left as round-26 edited it | exit 0, `ok` — the validator cannot detect the Rule 2 breach; the restore is a contract duty, not a census one |

Sandbox paths: `…/ReviewS124Supersede/sbxB` (B), `sbxC` (C), `sbxD` (D).

## Integration notes (for L1)

1. **Id:** substitute the next free id for `S127` at landing (C1's source rows take S127+ per
   round-27 contract.md:23-24). The E04 waiver only needs `supersedes S` + 3 digits.
2. **Lesson logging:** round-27 lesson logs the S124 three-cell old→new (Draft b) and carries the
   Gate block above for the new row; this closes D3 per round-27 contract.md:89. It also
   back-fills the round-26 logging gap (the `scope` cell change was never logged).
3. **Citation flip:** `corpus/knowledge/userspace-oom-killers-r26.md:2` (`source:`) cites S124
   for the oomd monitoring facts that, after the restore, only the new row teaches. Flip that
   citation to the new row id. If the entry then no longer cites S124 by id, also move the
   used-by path from S124 to the new row; S124 would then be `mined` with used-by `—`, which is
   warning W03 only and keeps `validate` at exit 0. Keeping both rows cited by the entry is also
   exit 0. L1 picks; validator consequences are as stated.
4. **Tooling record:** no tools installed or upgraded for this seat (pacman/uv/npx unused;
   existing bash, gawk, git, curl sufficed).

## Residual risk and verification gaps

- Drafts were validated against the current `scripts/sources-census.sh`; if it changes before
  landing, rerun the four falsifier commands.
- Upstream bytes could change before integration; hashes and quotes above are for the 2026-10-22
  fetches. If integration day differs, re-open both URLs and refresh sha256 + quotes.
- The restored S124 `teaches` is factually wrong on the monitoring question (that is expected:
  it is the historical row text; the corrected claim is carried by the supersedes row). The r26
  knowledge entry must not be left citing the restored row for the corrected claim (item 3).
- No other seat's drafts were consulted; if a sibling seat drafted the same supersession row,
  L1 should keep one and drop the other to avoid E03 (duplicate id) — the id substitution in
  item 1 covers this.

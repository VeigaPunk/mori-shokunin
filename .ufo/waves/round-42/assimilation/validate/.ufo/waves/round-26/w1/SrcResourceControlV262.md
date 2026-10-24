# SrcResourceControlV262 — review of landed row S124 (systemd v262 `ManagedOOM*` grammar)

Seat: `MoriR26.SrcResourceControlV262` (scribe, leaf). Question answered: the L1's landed row
**S124** and its Gate quote — are they right, and does anything contradict them?

`corpus/SOURCES.md` was **not** edited by this seat (S124 was landed by the L1). No lane commit,
no jj command, no unit started/stopped/enabled/disabled, no journal `MESSAGE` text read.

## Verdict in one line

**S124 is right on substance and correct on both digests — but its `teaches` cell states one
condition more strongly than upstream supports, and its `scope` cell claims more than its own
anchor covers.** The Gate quote at `systemd.resource-control.xml:1545-1546` is accurate and
located; it is a tag-stripped rendering of the raw XML (the same convention the round used for
S122 on `journalctl.xml`), so a checker who greps the raw file for the literal string will get
zero hits and should strip tags first.

## Part 1 — Is landed S124 right?

`corpus/SOURCES.md:130` (row S124), read verbatim.

### 1.1 URLs, digests, access date — **correct**

I fetched both URLs independently, with a different client invocation and a different local path,
on 2026-10-22:

| URL | HTTP | bytes | lines | my sha256 | S124 cell |
|---|---|---|---|---|---|
| `…/systemd/v262/man/systemd.resource-control.xml` | 200 | 110,159 | 1,890 | `d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8` | identical |
| `…/systemd/v262/man/systemd-oomd.service.xml` | 200 | 8,348 | 158 | `4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d` | identical |

Both digests in S124's anchor cell match my bytes **exactly**, and both are recorded in the row.
Tag provenance, also confirmed: `refs/tags/v262` → tag object
`1f7dffaf714cc4488159c498b7a17cf34c5a96d5` → commit
`8cc40e0c5e9234bf45084751ac53b1fbfe70b492` (tagger date 2026-09-22T13:12:43Z). The host runs
`systemd 262 (262-1-arch)`, so the tag matches the host's release.

### 1.2 The Gate quote — **accurate and located, with one checking caveat**

`corpus/lessons/round-26.md:77` records S124 as `:1545-1546 "When set to auto, systemd-oomd will
not actively use this cgroup's data for monitoring and detection."` — 16 words, within the ≤25
cap. The two cited source lines are:

```
1545|          <para>When set to <option>auto</option>, <command>systemd-oomd</command> will not actively use this
1546|          cgroup's data for monitoring and detection. However, if an ancestor cgroup has one of these
```

The quoted sentence is a contiguous span of those two lines after XML tags are stripped, and it
ends exactly at "detection." — the end of line 1546. It is **not** a byte-exact substring of the
raw file (`grep -F` on the raw XML → 0 hits, because the tags sit inside the sentence). This is
the round's established convention for XML man pages, not a defect: S122
(`man/journalctl.xml:599-600`) is quoted the same way. A non-author checker should strip tags
before grepping, or compare against the rendered page.

### 1.3 Row shape and census — **clean**

`NF=13` (11 columns), id `S124` unique, kind `docs` and tier `A` both in the allowed enums, status
`mined`, `opened 2026-10-22`, `recheck on-release`, `used-by corpus/knowledge/userspace-oom-killers-r26.md`.
The registry census at that tip prints: 126 rows, 0 malformed rows, 0 duplicate ids, and **no**
`missing:` line for any `mined` row — because the r26 entry exists and cites S124 in its `source:`
line (`corpus/knowledge/userspace-oom-killers-r26.md:1`). The contract's C1 counting command, run
read-only against committed bytes at `HEAD=2ecb66157cf78f66c3f8bf7fe091ea0bb1022350`, gives
`stale_present=0` and `r26_entry=present`.

### 1.4 The `teaches` cell — **one condition is stated more strongly than upstream supports**

Landed text: *"On systemd 262 a unit left at the default `auto` is not monitored by systemd-oomd
unless an ancestor is `kill`, so an inactive or unconfigured oomd is unavailable evidence, not a
quiet killer."*

Upstream (`systemd.resource-control.xml:1545-1548`, tag-stripped):

> "When set to `auto`, systemd-oomd will not actively use this cgroup's data for monitoring and
> detection. However, if an ancestor cgroup has one of these properties set to `kill`, a unit with
> `auto` can still be a candidate for systemd-oomd to terminate."

The first clause is **unconditional** for `auto`: the unit's own data is never used for monitoring
and detection. The ancestor-`kill` exception attaches to **termination candidacy**, not to
monitoring — `systemd-oomd.service.xml:43-44` says the monitored cgroups are those of units whose
`ManagedOOMSwap=`/`ManagedOOMMemoryPressure=` is `kill`. As landed, the cell reads as "with a
`kill` ancestor the unit *is* monitored", which upstream does not say. Everything else in the cell
("`auto` is the default", "an inactive or unconfigured oomd is unavailable evidence, not a quiet
killer") is supported: the default is at `systemd.resource-control.xml:1527-1529` and the
"unavailable, not zero" boundary is the lane's own rule (`PROVINCE.md:53`, FR10).

Fix options for the L1 (append-only, so the cell cannot be edited in place — `CORPUS.md:100-102`):
(a) leave the cell and record the wording precision in the round-26 lesson; or (b) admit one
corrected row whose `teaches` opens `supersedes S124 —`, e.g. *"…a unit left at the default
`auto` has its cgroup data unused for monitoring and detection, though an ancestor set to `kill`
can still make it a candidate for termination…"*. Option (b) is the only one that fixes the
registry text itself.

### 1.5 The `scope` cell claims more than the anchor covers — **minor**

Scope says *"what `ManagedOOMSwap=`/`ManagedOOMMemoryPressure=` `auto` and `kill` mean **and which
cgroups systemd-oomd monitors**"*, but the anchor only cites `systemd-oomd.service.xml:44`, which
supports "cgroups of units set to `kill` are monitored" and nothing about *which* cgroups are
eligible. The eligibility rules live at `systemd-oomd.service.xml:48-52` and are the substantive
answer to "which cgroups": only **descendant** cgroups are eligible kill candidates (the `kill`
unit itself is not, unless an ancestor is `kill`), and only **leaf** cgroups and cgroups with
`memory.oom.group` set to `1` qualify (`OOMPolicy=` in `systemd.service(5)`). Adding `:48-52` to
the anchor would make the scope cell self-supporting.

Also note the anchor's own gloss for `1545-1547` — *"an ancestor set to `kill` can still make the
unit a candidate"* — is **correct**; that clause does land on line 1547 ("can still be a
candidate"), with the sentence completing at 1548 ("for systemd-oomd to terminate"). The
`teaches` cell, not the anchor gloss, is where the over-statement sits.

### 1.6 Adjacency — cite, never absorb

S007 (freedesktop-rendered `systemd-oomd.service(8)`, opened 2026-10-19) already teaches "oomd
selects eligible descendant cgroups and sends SIGKILL to all processes in the selected cgroup".
S124 adds the `ManagedOOM*` opt-in grammar, which **no registry row covered** (grep of `corpus/`
for `resource-control` and `ManagedOOM` → no matches before this round). S124 does not supersede
S007 and correctly carries no `supersedes` prefix; the two should be cited side by side.

## Part 2 — Does anything contradict the contract or the landed work?

**No contradiction with the contract.** Checked against
`.ufo/waves/round-26/contract.md`:

- C1's host facts are confirmed by read-only reads on 2026-10-22: `systemd-oomd.service` is
  `disabled` / `inactive`; `systemd-oomd.socket` is `disabled` / `inactive`; `earlyoom.service` is
  `enabled` / `active` with `ActiveEnterTimestamp = Thu 2026-10-22 04:55:44 -03`
  (`ActiveEnterTimestampMonotonic=19964362`); host systemd is `262 (262-1-arch)`. Nothing in the
  contract's statement is contradicted.
- C2's oomd side (state plus the `MESSAGE_ID=d989611b…` notice count) is unaffected by this row;
  the notice id is the sibling seat's (`SrcOomdUtilV262`) ground.
- The contract's FR10 boundary (`PROVINCE.md:53`: "inactive killers are unavailable, not zero") is
  exactly what S124's second clause encodes. Nothing in the contract asks for a `ManagedOOM*`
  reading, so S124 supports rather than constrains C1/C2.
- The r26 entry's F8 statement is **not** contradicted by anything I read; my host sweep below
  independently corroborates it and widens it.

**One thing to keep straight (scope, not contradiction):** the contract's C1 explicitly does *not*
claim "any host-wide unit census". My sweep below is host-wide, so it must not be folded into the
C1 claim. It corroborates the entry's four-unit chain claim; if the L1 wants it in the entry it
must carry the same scoped/adjacent framing S125 uses (tsukuroi owns OS and unit diagnosis), or be
left to the round-26 host-capture receipt.

## Part 3 — Facts the round can rest on (each with its line number)

From `man/systemd.resource-control.xml` (v262, sha256 `d57641df…6597d8`):

1. `ManagedOOMSwap=auto|kill` and `ManagedOOMMemoryPressure=auto|kill` are the two property
   spellings — `:1523-1524`.
2. Their default is `auto` — `:1527-1529` ("Specifies how systemd-oomd.service(8) will act on this
   unit's cgroups. Defaults to auto.").
3. `kill` makes the unit **a candidate for monitoring by systemd-oomd** — `:1531-1532`.
4. When the cgroup then passes the `oomd.conf`/unit limits, oomd **selects a descendant cgroup and
   sends SIGKILL to all processes under it** — `:1533-1535`.
5. `kill` also creates `After=` **and** `Wants=` dependencies on `systemd-oomd.service` unless
   `DefaultDependencies=no` — `:1541-1543`.
6. With `auto`, oomd **will not actively use that cgroup's data for monitoring and detection**; an
   ancestor set to `kill` makes the `auto` unit a **candidate for termination** — `:1545-1548`.
7. `ManagedOOMMemoryPressureLimit=` is ignored unless `ManagedOOMMemoryPressure=kill` — `:1563`;
   `ManagedOOMMemoryPressureDurationSec=` likewise — `:1582`.
8. `ManagedOOMPreference=none|avoid|omit` exists for deprioritizing/omitting a candidate cgroup —
   `:1590`.
9. The `ManagedOOM*` properties were introduced with **v247** — `xi:include … xpointer="v247"` at
   `:1550` (and `:1566`).

From `man/systemd-oomd.service.xml` (v262, sha256 `4b29be2e…1ed8651d`):

10. systemd-oomd is "a system service that uses cgroups-v2 and pressure stall information (PSI) to
    monitor and take corrective action before an OOM occurs in the kernel space" — `:33-34`.
11. Monitoring and actions on units are enabled by setting `ManagedOOMSwap=` and
    `ManagedOOMMemoryPressure=` in the unit configuration — `:36-38`.
12. systemd-oomd reads that information from systemd(1) at start and **watches for subsequent
    changes** — `:39-41`.
13. "Cgroups of units with `ManagedOOMSwap=` or `ManagedOOMMemoryPressure=` set to `kill` will be
    monitored" — `:43-44`.
14. It polls PSI for the system and those cgroups; on exceeding the limits it selects a cgroup to
    terminate and sends SIGKILL to all processes in it — `:45-47`.
15. **Only descendant cgroups are eligible kill candidates**; the `kill` unit itself is not a
    candidate unless an ancestor has `kill` — `:48-50`.
16. **Only leaf cgroups and cgroups with `memory.oom.group` set to `1`** are eligible candidates;
    see `OOMPolicy=` in `systemd.service(5)` — `:50-52`.
17. `oomctl(1)` can list monitored cgroups and pressure information — `:55-56`.
18. oomd needs a full unified cgroup hierarchy and memory accounting on for every monitored unit
    (`DefaultMemoryAccounting=true` is the easiest way) — `:71-75`.
19. Swap-based actions are ignored on systems without swap — `:79-87`.
20. The `-n` short option for `--dry-run` **was added in version 262** — `:117-122`.

Version deltas against the v261 baseline the round-12 entry cited:

21. `man/systemd.resource-control.xml` is **byte-identical at v261 and v262** (same sha256
    `d57641df…6597d8`, 1,890 lines; `diff -u` empty). The `ManagedOOM*` grammar did not change
    between the two releases.
22. `man/systemd-oomd.service.xml` differs between v261 and v262 by **exactly one hunk** — the
    added `-n` short option and its "added in version 262" sentence (`diff -u` → 16 lines, one
    hunk). v261 sha256 `719f9786480d14f8cc6db16a6b2ac5767d0e433f50fef10b34ac055c41df1cc2`,
    156 lines.

Host facts observed read-only on 2026-10-22 (corroborating; host unit diagnosis is tsukuroi's
ground, so these belong beside S125 with the same scoped framing, not inside the C1 claim):

23. **No unit on this host opts in.** Over the 465 loaded units from
    `systemctl list-units --all --no-legend --no-pager --plain` (dash-prefixed names read with
    `--`), both `ManagedOOMSwap` and `ManagedOOMMemoryPressure` report `auto` for 226 units, report
    **no value at all** for 239 (device / target / timer / path / mount units, which have no cgroup
    context), and report `kill` for **0**. A repo-wide grep of `/etc/systemd`, `/usr/lib/systemd`
    and `/run/systemd/system` unit files for `ManagedOOM` finds **no** `ManagedOOMSwap=` or
    `ManagedOOMMemoryPressure=` assignment anywhere — the only hit is
    `/usr/lib/systemd/system/systemd-oomd.socket:22: ListenStream=/run/systemd/oom/io.systemd.ManagedOOM`,
    a varlink socket path, not a property. `OOMRules` is empty on every unit as well.
24. **No `Wants=systemd-oomd.service` edge exists** — 0 of the 465 loaded units and 0 of the 561
    unit files. The `After=systemd-oomd.service` edges that do exist (`multi-user.target`,
    `user@1000.service`) come from the shipped unit files, not from any `kill` opt-in: upstream
    `units/systemd-oomd.service.in:16` says `Before=multi-user.target shutdown.target` (inverted
    into an `After=` on the target) and upstream `units/user@.service.in:16` lists
    `systemd-oomd.service` in `After=`. [INFERENCE] therefore an `After=` edge on
    systemd-oomd.service is **not** evidence that a unit opted in; only the `kill` property is.
25. **The r26 entry's four-unit chain claim holds host-wide, and then some.** The r26 entry (F8)
    says the four sibling-captured units (`user@1000.service`, `user-1000.slice`, `user.slice`,
    `-.slice`) carry `auto` on both properties, so nothing in that chain would be monitored even
    if the service were started. My read confirms `auto` on all four, and since **no** unit on the
    host is `kill`, no ancestor chain is either — so on this host systemd-oomd would have had
    nothing to monitor and nothing to terminate even if the service were enabled. That is a
    stronger form of the same statement, and it is the r26 entry's to state with its own scoped
    framing; this seat supplies the measurement.

Adjunct upstream corroboration (adjacent, unregistered — the S124 row is scoped to the two man
pages):

26. `src/core/unit.c:1618-1643` adds the `After=`+`Wants=` pair on `systemd-oomd.service` only
    when `c->moom_swap == MANAGED_OOM_KILL || c->moom_mem_pressure == MANAGED_OOM_KILL ||
    !strv_isempty(c->moom_rules)` (`:1632`) — exactly the opt-in condition the man page describes,
    and the reason fact 24 holds. URL: https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c
    (HTTP 200, 2026-10-22, sha256 `47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7`,
    7,294 lines).
27. `src/oom/oomd-manager.c:113-118` keys systemd-oomd's monitored-cgroup maps on the
    `ManagedOOMSwap` / `ManagedOOMMemoryPressure` D-Bus properties — the code path behind facts
    13-16. URL: https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-manager.c
    (HTTP 200, 2026-10-22, sha256 `052f19b36d54997b78c4ca93fae17d8c8513ce7240b0b58a47a1efdad0da3a15`).
28. `src/core/dbus-unit.c:1357-1358`: the `ManagedOOMKills` D-Bus property returns `UINT64_MAX`
    (18446744073709551615) when the unit has no cgroup runtime, and the kill count otherwise — a
    sentinel, not a kill count. On this host the three slices report `0`. [INFERENCE] a reader that
    treats 18446744073709551615 as a count would report an absurd number. This is outside the C2
    tool's four-property input set, so it is a warning only.

## Part 4 — Recommendation

**Adopt S124 as landed** (substance, tier, digests, quote and anchors verified above), and handle
the two wording/coverage points as follows:

1. `teaches` over-statement (§1.4): either record the correction in
   `corpus/lessons/round-26.md`, or admit one superseded row whose `teaches` opens
   `supersedes S124 —`. My recommendation: the second, because the landed cell can mislead a
   reader about when an `auto` unit's data is monitored, and the registry is append-only.
2. `scope` vs `anchor` gap (§1.5): a superseding row can carry
   `systemd-oomd.service.xml:48-52` so "which cgroups" is anchored.
3. No **new** row is needed for the same two URLs. My own draft row (two URLs, tier A, mined,
   anchors `:1523-1524, :1529, :1531-1535, :1541-1543, :1545-1548, :1563, :1582, :1590` and
   `:43-44, :48-52, :117-122`, used-by the r26 entry) is **withdrawn** as a duplicate of S124; if
   the L1 prefers a superseding row, it should be that row, and it should use the corrected
   `teaches` wording from §1.4 plus the `:48-52` anchors from §1.5.

## Verification trail

- `curl -sS -o systemd.resource-control.xml https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml`
  → HTTP 200; 110,159 B; 1,890 lines; sha256 `d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8`.
- `curl -sS -o systemd-oomd.service.xml https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml`
  → HTTP 200; 8,348 B; 158 lines; sha256 `4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d`.
- Same URLs at tag `v261` → `systemd.resource-control.xml` sha256 identical to v262 (`diff -u`
  empty); `systemd-oomd.service.xml` sha256
  `719f9786480d14f8cc6db16a6b2ac5767d0e433f50fef10b34ac055c41df1cc2`, 156 lines, `diff -u` → one
  hunk (the `-n` option).
- `curl -sS https://api.github.com/repos/systemd/systemd/git/ref/tags/v262` → tag object
  `1f7dffaf714cc4488159c498b7a17cf34c5a96d5`;
  `…/git/tags/1f7dffaf…` → commit `8cc40e0c5e9234bf45084751ac53b1fbfe70b492`, tagger date
  2026-09-22T13:12:43Z.
- `sed -n` on the cited ranges of both v262 files → the quotes and anchors quoted above;
  `grep -F` of the S124 Gate sentence against the raw XML → 0 hits; the same sentence after
  tag-stripping → present (verified with a tag-strip + whitespace-collapse pass).
- Registry census at `corpus/SOURCES.md` (read-only): 126 rows; malformed 0; duplicate ids none;
  `mined` rows' `used-by` paths all exist (no `missing:` output).
- Contract C1 counting command run read-only at `HEAD=2ecb66157cf78f66c3f8bf7fe091ea0bb1022350`:
  `stale_present=0`, `r26_entry=present`.
- Host (read-only): `systemctl --version` → `systemd 262 (262-1-arch)`; `is-enabled
  systemd-oomd.service` → `disabled`; `is-active systemd-oomd.service` → `inactive`;
  `is-enabled systemd-oomd.socket` → `disabled`; `is-active systemd-oomd.socket` → `inactive`;
  `is-enabled earlyoom.service` → `enabled`; `is-active earlyoom.service` → `active`;
  `systemctl show earlyoom.service -p ActiveEnterTimestamp` → `Thu 2026-10-22 04:55:44 -03`.
- Host property sweep: 465 loaded unit names → `ManagedOOMSwap` and `ManagedOOMMemoryPressure`
  each `auto` 226 / `kill` 0 / no value 239; `OOMRules` empty on every unit.
- Host unit-file sweep: `grep -rn ManagedOOM /etc/systemd /usr/lib/systemd /run/systemd/system`
  with unit-file `--include` filters → the only hit is the oomd.socket `ListenStream` path.
- Host dependency sweep: `systemctl show -p Wants --value` over 465 loaded units and 561 unit files
  → 0 `systemd-oomd.service` `Wants=` edges.
- Upstream unit templates fetched at v262 for the `After=` attribution:
  `units/systemd-oomd.service.in` (sha256 `2f4c2862b5826e85d63d5c7993f8610556f2f201facc0b20af04c1b972f288d3`,
  line 16 `Before=multi-user.target shutdown.target`) and `units/user@.service.in` (sha256
  `72c2f40dcfced1d85bcc17583715966fc8a552b68af44404c213de2ea320504c`, line 16
  `After=systemd-logind.service user-runtime-dir@%i.service dbus.service systemd-oomd.service systemd-pcrlogin@%i.service`).
- No unit was started, stopped, enabled, disabled or restarted; no systemd file was edited; no
  journal `MESSAGE` text was read or copied; no oomd configuration value was printed other than
  the `auto`/`kill`/absent property values counted above.

## Out of scope

- Editing `corpus/SOURCES.md`, the r26 entry or any other lane file (review and draft only).
- The earlyoom v1.9.0 message grammar and the `tools/mori-oom-killers.py` interface (other seats).
- The oomd notice MESSAGE_ID, the `user.oomd_ooms`/`user.oomd_kill` xattrs and the D-Bus kill path
  (sibling seat `SrcOomdUtilV262`).
- Host kill history, host-wide unit census as a **claim** (the sweep above is corroboration only),
  and the C1/C2 claim counting (the L1's).
- The `GHSA-652q-wxr6-h5j6` advisory (S012, tsukuroi-owned adjacency).

## Tooling

- No install, upgrade or downgrade was performed; no new tool was needed. The host already provides
  `curl`, `python3` (standard library only, for byte/word/digest checks), `grep`, `sed`, `diff`,
  `wc`, `sha256sum`, `systemctl`.
- All pacman transactions are PAUSED host-wide per the round bounds, so none was attempted.
- Scratch copies of the fetched bytes live under
  `/fast/scratch/hyaku/mori-r26/SrcResourceControlV262/` (`systemd.resource-control.xml`,
  `systemd-oomd.service.xml`, the `v261-*` copies, `journalctl.xml`, `oomd.conf.xml`, `unit.c`,
  `oomd-manager.c`, `dbus-unit.c`, `dbus-cgroup.c`, `cgroup.c`, `oomd.c`, `user-at.service.in`,
  `systemd-oomd.service.in`, the two rendered freedesktop HTML pages).
- Writes: this report file only. No jj command was run anywhere; no git write command was run; no
  lane commit was made.

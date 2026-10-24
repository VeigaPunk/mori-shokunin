# CriticScopeProvince — C2 province fit (round 23, wave 1)

Seat: `MadoR22-2.CriticScopeProvince-8` (critic, read-only). Question: is filesystem quota
configuration OS state owned by tsukuroi (`PROVINCE.md` Refuses), or runway evidence mori may read?

## Ruling recommendation

**IN PROVINCE, conditionally.** C2 (`tools/mori-quota-surface.py`) is mori **resource-runway
evidence** (FR2 advance). It is not a tsukuroi-owned surface **as long as** the probe and its docs
report only the *kernel-exported visibility* of a quota mechanism on the runway targets. They must
never diagnose *why* quota is on or off, whether it should be, its limits, or its configuration
source. Admit only with the four corrections below. Without them, the same tool slides into
tsukuroi's host-configuration diagnosis (Snapper/rollback net, systemd mount units).
This is a fixable scope-wording defect, not a tradeoff the judge must reject.

## Pins

| Item | Value |
|---|---|
| mori lane HEAD | `4dc80c1be48308075e83af17f15fbfe7e95e6cb8` (= contract freeze commit) |
| mori `PROVINCE.md` last-touching commit / sha256 | `8cb4afbf0dd35c837ec631ff692232421ba21068` / `cdfb32c79be0a1de9954b376024e3190f3be6eabe6290fa2c8d81a3096dc1f63` |
| tsukuroi HEAD / `PROVINCE.md` last-touching commit / sha256 | `a61db549c6c425e6a865885009b278f62ae6ef0f` / `7f4231401e4918146c4442e8633334231c7d88d6` / `a296da872e83731f7f7a7737662988558ebb97e4399681a1099fab4a259b7a79` |
| contract sha256 | `2bb35aefb08d3fafc467260f859453c0f096effe18b2446503f2b2ee87fe69e7` |

## Evidence

### For mori ownership (runway)

- E1. mori Owns: "resource runway (disk on the fleet root and `/tmp`, memory pressure)"
  (`mori-shokunin/PROVINCE.md:10`).
- E2. FR2 is already a registered mori frontier: "**FR2 — Quota/EDQUOT observability** … Boundary:
  `df` capacity percentages cannot detect quota exhaustion; observe and report only, never change
  quota state." (`mori-shokunin/PROVINCE.md:46`; mirrored at `corpus/README.md:333`). C2 advances an
  existing mori frontier; it does not open a new domain.
- E3. The motivation is fleet-observed runway failure, not host configuration. Census selftest abort
  `printf: write error: Disk quota exceeded` (`corpus/knowledge/audit-r11.md:95-96,168`). The
  quota-abort regression is tracked in `corpus/lessons/round-12.md:48` (M25). "the fleet's own
  reported disk failures were EDQUOT quota events that a capacity-% probe cannot see"
  (`corpus/knowledge/observability-surfaces-r2.md:258-259`; `SKILL.md:411-413`).
- E4. mori Refuses enumerates "OS package, systemd unit, driver/firmware and boot state (→ tsukuroi)"
  (`mori-shokunin/PROVINCE.md:13-15`). Filesystem quota is not in that list.
- E5. tsukuroi's Domain is "package state, systemd, drivers/firmware, boot health"
  (`tsukuroi-shokunin/PROVINCE.md:3-4`). Its additional surfaces are Arch News, `.pacnew`,
  initramfs v42 and Snapper/rollback net (`:19-24`). None of these names quota.
- E6. A repo-wide case-insensitive search of `tsukuroi-shokunin` for `qgroup|quota|EDQUOT`
  returned **0 matches**. tsukuroi has no corpus, tool, census or adjacency row (ADJ-01..07,
  `:45-51`) for quota. There is no competing authority to duplicate.
- E7. tsukuroi's own routing rule: "Select the matching row by the **question being asked**, not the
  binary or service name" (`tsukuroi-shokunin/PROVINCE.md:59-60`). The C2 question is "can a fleet
  write on the fleet root or `/tmp` fail with EDQUOT that `df` cannot see?". That is runway.

### Against, or limiting, mori ownership (the strongest counterexamples)

- **CX1 — quota diagnosis already routed to tsukuroi/operator.** `audit-r11.md:216` (D21): "operator/
  tsukuroi diagnose quota if operationally relevant; no audit cleanup/remediation." This is a prior
  in-lane routing of quota *diagnosis* away from mori. It is consistent with the ruling only if mori
  keeps strictly to *visibility* and hands *diagnosis* to tsukuroi/operator.
- **CX2 — Snapper is a tsukuroi-owned path to btrfs qgroups on the fleet root's filesystem.**
  tsukuroi records live Snapper configs "home (/home) and root (/)"
  (`tsukuroi-shokunin/corpus/knowledge/snapper-eacces-mechanism.md:127`). The fleet root's covering
  mount in the C2 real control is btrfs `/home` (contract `:146-149`).
  - [INFERENCE — Snapper docs not opened this round] Snapper's quota-aware cleanup (`setup-quota` /
    `QGROUP`) enables btrfs quota and creates qgroups. Snapper/rollback net is a tsukuroi surface
    (`tsukuroi-shokunin/PROVINCE.md:24`).
  - Counterexample: a later operator Snapper change flips the real control to `QUOTA_ENABLED` (exit 1,
    `btrfs_qgroups_dir_present`). Any mori text that explains, attributes or recommends ("enabled by
    Snapper", "disable qgroups") would absorb tsukuroi's Snapper diagnosis.
  - The present contract has no such text. Nothing in it forbids such text in docs or knowledge either.
- **CX3 — mount options are written by systemd mount units and fstab (tsukuroi "systemd unit" state).**
  - `/tmp`'s xfs `noquota` and the btrfs `/home` mount are produced by host mount configuration
    [INFERENCE: generator/unit not observed].
  - Reading the kernel's *resulting* superblock options in `/proc/self/mountinfo` observes an effect.
    Reading `/etc/fstab`, `*.mount` units, `systemctl` or Snapper configs would read tsukuroi-owned
    configuration.
  - The contract's real-mode input list (`:76-80`) correctly excludes all of these. That exclusion is
    the load-bearing province fence and must be stated as such, not only as an input list.
- **CX4 — shared input, different question (not a conflict).** tsukuroi already reads mount options:
  `findmnt -n -o TARGET,FSTYPE,OPTIONS /` (`tsukuroi-shokunin/.ufo/waves/round-12/AclSemantics.md:68`;
  `CensusScribe.md:59`; `tools/check-root-dac-correction.py:299,318`).
  - It reads them only to discriminate root DAC from read-only mounts, which is rollback-net
    diagnosis.
  - Shared evidence is not shared ownership (`tsukuroi-shokunin/PROVINCE.md:41-42`). There is no
    duplicate authority, provided mori never classifies `/` or `/boot` mount state for OS diagnosis.
- **CX5 — `--path ABS` is unbounded.** The CLI accepts any absolute path, repeatably (contract `:73`).
  `--path / --path /boot --path /.snapshots` turns the runway probe into a general host
  filesystem-configuration survey. The defaults (fleet root, `/tmp`) are in province. Arbitrary paths
  are covered only by the precedent of operator-pinned `MORI_DISK_TARGETS`
  (`corpus/knowledge/observability-surfaces-r2.md:249,262-264`), not by any province text.

### Provenance gap (adjacent, not a province defect)

- The contract cites S077–S084 "opened this round, see lesson23 Gate" (`contract.md:67`). At lane
  HEAD `4dc80c1`, a search of `corpus/**` and the round-23 contract/frozen files finds them **only**
  in `contract.md`. They are not in `corpus/SOURCES.md`.
- If they are not registered before seal, the C2 classification table's source grounding is
  pre-registered without retained sources. That is a false-provenance risk for L1 to check. It does
  not change this ruling.

## Impacted axes

- **Province/identity** — Refuses-list fidelity. tsukuroi must not lose the Snapper, systemd-mount and
  configuration-diagnosis surfaces to mori. Exposure: CX2, CX3, CX5.
- **Coverage (C2's claim axis)** — unaffected by the corrections. The sealed cases, real control and
  classification table do not change.
- **Calibration** — `QUOTA_ENABLED` exit 1 must stay a runway finding, not a host-fault claim. The
  contract already says so at `:133-134`; keep that sentence verbatim in the docs.
- **Provenance** — the S077–S084 registration gap above.

No regression to C1. No identity change to existing census finding ids.

## Smallest safe correction (no contract re-freeze needed; applies at integration/docs)

1. **Pre-register the PROVINCE wording.** L1 appends it at integration; it is not a sibling write.
   The contract moves FR2 "frontier → bounded core" (`:65`) but freezes no province text. Use the
   exact text in the next section.
2. **Lock the input fence as a province fence.** The C2 knowledge note and the `limits` output text
   must state that the probe never reads `/etc/fstab`, systemd `.mount` units or `systemctl`,
   Snapper or other quota-tool configuration, or filesystem superblocks or features. It reads only
   the kernel-exported inputs listed in contract `:76-80`.
3. **Bound non-default paths.** The docs must say that `--path` values other than the fleet root and
   `/tmp` are operator-pinned runway targets, the same as `MORI_DISK_TARGETS`. The probe states
   visibility for them, and interpreting them is the operator's call. No code change is needed.
4. **No cause, attribution or remediation text.** Output, docs and knowledge must never name a
   configuring agent (Snapper, a mount unit, an installer) or suggest enabling or disabling quota. An
   `enabled` or `unknown` result routes cause and configuration diagnosis to tsukuroi/operator,
   consistent with `audit-r11.md:216` (D21). Any handoff is prepared as an evidence packet in mori's
   own report: capture time, path, fstype, mount_point, quota_state, basis and exit code. Nothing is
   written into tsukuroi.

## Exact boundary wording (proposed, for `mori-shokunin/PROVINCE.md`)

**Core row (append under `## Core` or as a round-23 appended note):**

> - **Quota-mechanism visibility (FR2 bounded advance)** — read-only
>   `tools/mori-quota-surface.py` reports, per runway target (default the fleet root and `/tmp`;
>   other absolute paths only when operator-pinned), whether a filesystem quota mechanism is
>   *visibly* enabled, visibly disabled or unknown. It reads only kernel-exported
>   `/proc/self/mountinfo` super options, `stat` device ids, `/dev/mapper` link basenames and
>   `/sys/fs/btrfs` device/qgroups presence and mode. `QUOTA_ENABLED` is runway evidence that `df`
>   percentages are insufficient there; it is not a fault, a limit, usage or a configuration claim.

**Refuses clarification (append to the Refuses sentence, wording only):**

> Filesystem quota *configuration* — mount units, fstab, Snapper/qgroup setup, superblock quota
> features, and why a mechanism is on or off or whether it should be — is host OS state
> (→ tsukuroi/operator). mori observes its kernel-visible effect on runway targets only, never sets,
> tunes or diagnoses it, and never calls quotactl, `btrfs`, `xfs_quota`, `repquota` or mount.

**FR2 remainder (replace the FR2 row's tail after the advance lands):**

> Remainder: per-user/group/project limits and usage, EDQUOT event attribution, ext superblock quota
> features, NFS/server-side/overlay/fuse quota, and enable/disable/remount races. Boundary unchanged:
> observe and report only, never change quota state; a qgroups directory is not a limit.

**Adjacent row (tsukuroi), mori-side only:**

> tsukuroi | Owns the host mount/unit configuration and Snapper/rollback net that can enable a quota
> mechanism; mori reports only kernel-visible quota state on runway targets and routes cause or
> configuration questions to tsukuroi/operator as an evidence packet. No tsukuroi quota surface was
> found (0 `qgroup|quota|EDQUOT` hits at tsukuroi `a61db549`); shared `findmnt` input is not shared
> ownership. | `../tsukuroi-shokunin/PROVINCE.md:3-4,24,41-42,59-60`;
> `../tsukuroi-shokunin/corpus/knowledge/snapper-eacces-mechanism.md:127`;
> `corpus/knowledge/audit-r11.md:216`

## Judge-facing distinction

- **Fixable:** CX2, CX3 and CX5 are wording and doc fences. Corrections 1–4 close them with no code
  or seal change.
- **Must reject only if:** the integrated docs, knowledge or output attribute a cause, read a
  configuration source beyond contract `:76-80`, or recommend a quota action. Each of those absorbs
  tsukuroi or remediation scope.

## Method and limits

- Reads only: the round-23 contract, both `PROVINCE.md` files, the cited mori corpus lines, and
  tsukuroi corpus, wave and tool search hits.
- Read-only `git rev-parse` / `git log` and `sha256sum` for pins.
- No host probes, no implementation or case-proposal reads, no builds, tests or installs.
- Snapper's qgroup behavior is [INFERENCE]; the Snapper docs were not opened this round.

Tools installed/updated: none.

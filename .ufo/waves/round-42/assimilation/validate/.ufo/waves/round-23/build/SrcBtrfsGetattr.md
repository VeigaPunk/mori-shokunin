# SrcBtrfsGetattr — btrfs_getattr st_dev re-open for round23 C2

Seat: MadoR22-2.SrcBtrfsGetattr-8 (scout, read-only). Report-only; no registry, lesson,
contract or production edits. Independence held: no candidate implementation
(`.ufo/waves/round-23/build/ImplQuota/`, `.scratch/round23/ImplQuota`), no case file and no
oracle file was opened.

## Opened

| Item | Value |
|---|---|
| URL | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/inode.c |
| Access | 2026-10-21T17:31Z; one `curl -fsSL`; HTTP 200; 319770 bytes; 10826 lines; LF only, ASCII, no CR |
| Local copy | `.scratch/round23/SrcBtrfsGetattr/inode.c` (scratch copy, not a registry artifact) |
| Fetched-bytes SHA-256 | `01a6ad07c09cd1a05fbccab640c15362c91b57b85faa94c2fd9b9c0128110fdf` |
| Git blob SHA-1 of fetched bytes | `2534cd9284d540d0849afcdd2f1b78fd4027364a` — equals the blob sha and size 319770 that the GitHub `git/trees/v7.2:fs/btrfs` entry reports for `inode.c` |
| Tag resolution | annotated tag `v7.2` = tag object `237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63` → commit `8d3ae59288f1e7d58d76558a6ee96d533bc5019f` |
| HTTP ETag | `"4097e17575e80060ef8e9a47544519455379279e766456b90b9e8422b18d727d"`; recorded only, it matches neither the content SHA-256 nor a git object hash and is not used as identity |

Provenance caveat: the blob-sha equality shows the fetched bytes are the `v7.2:fs/btrfs/inode.c`
blob as GitHub serves it. It does not authenticate GitHub or the tag.

## Anchor verification — confirmed

- `btrfs_getattr` definition: `fs/btrfs/inode.c:8215-8259`.
- `:8245` `generic_fillattr(idmap, request_mask, inode, stat);` then the unconditional
  `:8246` `stat->dev = BTRFS_I(inode)->root->anon_dev;`.
- `stat->dev` occurs **exactly once** in the file (`grep -n "stat->dev"` → `:8246` only), so
  the value returned at `:8246` is the function's final `st_dev`; no later write overrides it.
- `btrfs_getattr` is the `.getattr` of every btrfs inode-operation table:
  `btrfs_dir_inode_operations` `:10697-10698`, `btrfs_file_inode_operations`
  `:10794-10795`, `btrfs_special_inode_operations` `:10806-10807`,
  `btrfs_symlink_inode_operations` `:10815-10817`.
- Root ownership/lifetime corroborated in the same file: `:4872-4873`
  `free_anon_bdev(dest->anon_dev); dest->anon_dev = 0;` inside `btrfs_delete_subvolume`
  (starts `:4760`).
- Corroborating only (the probe does not read it): `:8248-8249` sets
  `stat->subvol = btrfs_root_id(...)` and `STATX_SUBVOL`.

Requested anchor line, verbatim (`:8246`, one leading tab, LF): `stat->dev = BTRFS_I(inode)->root->anon_dev;`

## Located quote (≤25 words)

Primary, `:8246` (code, verbatim, 3 whitespace-delimited tokens):

> stat->dev = BTRFS_I(inode)->root->anon_dev;

Two-line context for the gate if it needs the override relation, `:8245-8246` (verbatim,
7 whitespace tokens, one leading tab per line):

> generic_fillattr(idmap, request_mask, inode, stat);
> stat->dev = BTRFS_I(inode)->root->anon_dev;

## Contract rule backed

`contract.md:100-103`, the btrfs branch of the per-path device check: “For btrfs a mismatch
is expected (per-subvolume anonymous st_dev, S081) and is recorded as `device_check:
"btrfs_subvolume_skipped"`; equal → `device_check: "match"`.”

This anchor does **not** back the preceding non-btrfs clause (major:minor ≠ st_dev →
`device_mismatch`, `contract.md:100-101`) and does not back any quota-classification row.

## Assessment — supports, narrowly; under-determines two edges

Observed in the file:
1. A stat on any btrfs inode reaches `btrfs_getattr` (four ops tables above).
2. After `generic_fillattr`, it overwrites `stat->dev` with
   `BTRFS_I(inode)->root->anon_dev` — a field of the inode's root (subvolume), not of the
   mounted superblock's device.
3. That field is released with `free_anon_bdev` when a subvolume root is deleted, so it is a
   per-root anonymous block-device handle, not the mount source rdev.

Supports: the probe is correct to treat a btrfs `st_dev` mismatch against mountinfo's
major:minor as expected rather than as a failure. `st_dev` for a btrfs path is drawn from a
per-subvolume anonymous number, so it does not identify the mount source device;
`btrfs_subvolume_skipped` is the right recording.

Under-determined inside this file:
- **Allocation range.** `inode.c` has no `anon_dev` allocation site, only the free at
  `:4872`. The file cannot show that the allocator yields a major-0 unnamed device, which is
  what makes inequality with a real block device systematic. [INFERENCE: `get_anon_bdev`
  semantics from `fs/super.c`, not opened.] “Mismatch is expected” is supported as written;
  a stronger “never equal” wording would need a second anchor.
- **The `equal → match` branch.** Nothing in `inode.c` produces equality with the mount
  source for btrfs; the file neither proves such equality reachable nor proves it
  impossible, so that contract branch is a defensive observation this source does not
  adjudicate.
- [INFERENCE] `generic_fillattr` fills `st_dev` from the superblock device (`fs/stat.c`, not
  opened). It does not change the returned value because `:8246` is unconditional and is
  the sole `stat->dev` write in the file.

No contradiction: no btrfs path in this file assigns `stat->dev` from `sb->s_dev`, and the
override has no conditional guard.

## Tier and scope

Tier **A** — primary upstream kernel source, immutable annotated tag `v7.2`, `kind=code`;
this matches the existing S003 pattern (`mm/oom_kill.c` at tag v7.2, tier A, narrow scope).

Scope: btrfs `stat(2)`/`statx` `st_dev` is the inode root's per-subvolume anonymous block
device, for every btrfs inode type, at tag v7.2. Excludes: quota/qgroup state (do not cite
this row for `btrfs_qgroups_dir_present`/`btrfs_qgroups_dir_absent`), `get_anon_bdev`
allocation semantics and device-number range, non-btrfs filesystems, and any claim that
equality with the mount source is impossible.

Proposed registry row (SOURCES.md untouched by this seat; L1 owns insertion and final
status):

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S081 | Linux fs/btrfs/inode.c at v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/inode.c | code | A | btrfs stat(2) st_dev is the inode root's per-subvolume anonymous device, not the mount source device; contract C2 btrfs device_check only | fs/btrfs/inode.c:8215-8259,8245-8246; inode-op registrations 10697-10698,10794-10795,10806-10807,10815-10817; tag v7.2 (commit 8d3ae59288f1e7d58d76558a6ee96d533bc5019f), blob 2534cd9284d540d0849afcdd2f1b78fd4027364a | btrfs_getattr overwrites st_dev after generic_fillattr with BTRFS_I(inode)->root->anon_dev, so a btrfs path's st_dev is a per-subvolume anonymous number and a mismatch against the mount source is expected, not a failure. | queued | 2026-10-21 | on-release | — |

Flip for `mined`: only after the round-23 lesson Gate cites this row with the located quote
and access date 2026-10-21; then set `status` `mined` and `used-by` to the actual round-23
lesson path. No other cell should change.

## Remaining unknowns

- Whether the lesson23 Gate wants the one-line or the two-line quote.
- Whether L1 wants a companion anchor (`fs/super.c` `get_anon_bdev`) to upgrade “mismatch is
  expected” to “always mismatched”. That file was not opened; it is outside this
  assignment.
- S-id assignment is inferred from the contract parenthetical “S081”; `corpus/SOURCES.md`
  currently ends at S076, so S077–S084 are all still unrowed at this revision.

## Run log

- Commands: one `curl -sSIL` + one `curl -fsSL` of the raw URL into `.scratch/`; one
  `curl` of the GitHub tag object and one of the `v7.2:fs/btrfs` tree entry; local
  `sha256sum`, `grep -n`, `nl -ba`, `sed -n`, `cat -A`, `file`, Python `hashlib` on the
  fetched bytes; reads of `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/README.md`,
  `contract.md`, `.ufo/waves/round-22/build/SrcGitCommit.md`.
- Tools installed or updated: none.
- Tests, builds, linters, formatters, smoke runs: none.
- No `/tmp` use, no VCS command, no live host probe, no candidate/case/oracle read.

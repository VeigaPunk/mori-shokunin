# ReopenS085 — source re-open of `SOURCES.md` row S085 (Linux v7.2 `fs/proc_namespace.c`)

**Verdict: row substance CONFIRMED; byte pin CONFIRMED; five concrete reporting/scope
discrepancies found, none of which edit or invalidate a frozen byte.** The fresh fetch of
the pinned URL is byte-identical to the retained evidence and the registry SHA256. The
scope claim (`per-mount field assembly and path escaping`) and the two inner anchors
(`seq_path_root:151`, `separator:172`) are exact. The anchor range end and three
claim/scope formulations are imprecise, and one C2 contract rule is narrower than the
kernel's actual escaping for the mountinfo *source* field. No registry, lesson, note,
frozen case/rule/oracle or production byte was edited. No driver, oracle, tool or test
was executed.

Seat: `ReopenS085` · mode: **source reading + one pinned HTTPS fetch + read-only git** ·
scratch: `/fast/scratch/hyaku/mori-r23/ReopenS085/`.

## 1. Identities (byte-exact)

| item | value |
|---|---|
| lane repo | `/home/vgpnk/Projects/shokunin/mori-shokunin` |
| lane HEAD (observed) | `6eb889c037163e4886eaa61501258910d6a529b9` |
| production pin in context | `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` — observed present and strict ancestor of HEAD (`git merge-base --is-ancestor` exit 0) |
| registry row | `corpus/SOURCES.md:91` (sole S085 provenance row; second occurrence line 100 is the filesystem-quota sequence only) |
| pinned URL | `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc_namespace.c` |
| fresh fetch | `/fast/scratch/hyaku/mori-r23/ReopenS085/proc_namespace.c` |
| fresh bytes | **7957** (337 lines) |
| fresh sha256 | `fd82c0db52055ae807ee0b46c7c9bc5d47a9239805eb8ca5c47d2ba81d695776` |
| retained evidence | `.ufo/waves/round-23/evidence/sources/S085-fs_proc_namespace.c` |
| retained sha256 | `fd82c0db52055ae807ee0b46c7c9bc5d47a9239805eb8ca5c47d2ba81d695776` (identical; `diff -q` empty) |
| manifest entry | `.ufo/waves/round-23/evidence/sources-manifest.json` → `{"id":"S085","bytes":7957,"sha256":"fd82c0db52055ae807ee0b46c7c9bc5d47a9239805eb8ca5c47d2ba81d695776"}` |
| registry SHA prefix | `fd82c0db52055ae8` — matches the full digest prefix |
| supplementary fetches (not registry rows) | `fs/namespace.c` sha256 `3c2417e6bd81a82de3a989caf6b80ac28658954dcc20078a60d1a5b4925fcdaa`; `fs/seq_file.c` `db28fa9bd5006c76035f5ac27d1d888024d31e37f553828c55451b94bcc8ac0d`; `include/linux/seq_file.h` `d44152495b20227ce08f0fe0a08d44eaeffd974a264eea1809074c4a8c338886`; `fs/btrfs/super.c` `d1731b24b5c1e134c832b92601ccccf2a9955b1bcee9dc81f333a330a59e1ca8` |

`git status --untracked-files=no` shows no tracked modification by this seat. The
retained S085 evidence file is committed/clean; the only tracked-clean fetch was written
to scratch, never to the lane.

**RawSHA check: PASS.** Full digest equals the assignment pin
`fd82c0db52055ae807ee0b46c7c9bc5d47a9239805eb8ca5c47d2ba81d695776` on three
independent surfaces (fresh fetch, retained bytes, manifest).

## 2. Scope and anchor verification against the fetched source

Registry row fields (verbatim from `corpus/SOURCES.md:91`): type `code`, authority `A`,
scope `per-mount field assembly and path escaping`, anchors
`show_mountinfo:135-193, seq_path_root:151, separator:172; tag v7.2; sha256 fd82c0db52055ae8`,
claim `Mountinfo emits escaped namespace paths and calls each filesystem show_options; field layout is not a safe mount stack ordering rule.`

| row element | observed in v7.2 source | verdict |
|---|---|---|
| `show_mountinfo:135-193` | `static int show_mountinfo(...)` is **135**; body fields/emission **136–190**; closing brace **191**; line **192** blank; line **193** is `static int show_vfsstat(struct seq_file *m, struct vfsmount *mnt)` | **PARTIAL** — start exact, end wrong (see D1) |
| `seq_path_root:151` | line **151**: `err = seq_path_root(m, &mnt_path, &p->root, " \t\n\\");` — the mountinfo call (other calls at 118, 214 belong to `show_vfsmnt`/`show_vfsstat`) | **MATCH** |
| `separator:172` | line **172**: `seq_puts(m, " - ");` — exact bytes, tab-indented | **MATCH** |
| `tag v7.2` | the tag-pinned raw URL resolved and returned 7957 bytes identical to retained evidence | **MATCH** (HTTP tag address, not a signature check) |
| `sha256 fd82c0db52055ae8` | full `fd82c0db…695776` | **MATCH** |
| `per-mount field assembly` | one line per mount via `m_show` → `p->show(...)` (`fs/namespace.c:1573-1586`, `mounts_op` 1580); `show_mountinfo` prints id/parent/major:minor (143–144), fs root (145), mount point (151), rw/ro + vfs opts (155–156), optional `shared/master/propagate_from/unbindable` tags (158–170), `" - "`, fstype, devname, ro/rw, sb opts, fs `show_options` (172–188), then `'\n'` (188) | **CONFIRMED** |
| `path escaping` | mount point at 151 passes esc set `" \t\n\\"`; `seq_path_root` → `mangle_path` (`fs/seq_file.c:441-459`) replaces each esc character with `\` + three octal digits; fs root at 145 goes through `show_path` (`fs/namespace.c:5219-5224`) → generic `seq_dentry(m, root, " \t\n\\")` when the filesystem defines no `show_path` (true for btrfs and xfs: their `super_operations` blocks at `fs/btrfs/super.c:2535-2553` and evidence `S078-fs_xfs_xfs_super.c:1334-1350` contain no `.show_path`) | **CONFIRMED** |
| `calls each filesystem show_options` | 186–187 calls `sb->s_op->show_options(...)` when non-NULL, once per emitted mount; 175–177 likewise `show_devname`, else 180 `mangle(r->mnt_devname)` | **CONFIRMED** |
| `field layout is not a safe mount stack ordering rule` | no ordering logic exists in `proc_namespace.c`; the order lives in `fs/namespace.c`: `m_start` (1536–1547) via `mnt_find_id_at`, `m_next` (1549–1566) via `rb_next` over `ns->mounts`, an rbtree keyed by `mnt_id_unique` (`mnt_add_to_ns`, 1079–1100); `mnt_id_unique = ++mnt_id_ctr` at mount allocation (`mnt_alloc_id`, 213–224), while the printed field 1 is the xarray-assigned `mnt_id`, erased on free (`mnt_free_id`, 225–228) | **CONFIRMED, but only jointly with `fs/namespace.c`** (see D3) |

Emission order is therefore **ascending internal `mnt_id_unique` (creation) order**, not
nesting depth, not mount-point prefix order, and not guaranteed to be sorted by the
*displayed* `mnt_id`, which is a different, reusable id space. That is stronger than the
registry claim states and is the actual source basis for refusing last-line-wins stack
inference.

## 3. lesson23 Gate quote check

`corpus/lessons/round-23.md:51`:

> `| S085 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc_namespace.c |172: `seq_puts(m, " - ");` | Admit A for per-mount namespace field emission/escaping, not topology inferred from ordering. |`

| check | result |
|---|---|
| quote located at line 172 | **yes**, exact bytes (`\tseq_puts(m, " - ");`) |
| ≤25 words | **yes**, 4 whitespace-separated tokens (`seq_puts(m,` / `"` / `-` / `");`); `evidence/source-quotes.json` records `"word_count": 4` and `"found_in_whitespace_normalized_source": true` with the same source sha256 |
| quote verifies the Gate decision | **weakly** — it proves only the field separator byte position. Per-mount emission requires `show_mountinfo` 135–191 plus `mounts_op`; escaping requires 151 (`" \t\n\\"`) and `mangle_path` octal code. The decision is supportable from the anchor block, not from this quote alone (see D2) |

The Gate row does not misquote; it under-quotes.

## 4. New knowledge-note claim versus source

`corpus/knowledge/quota-surface-r23.md:60-61` states:

> “S082 describes mountinfo fields, not a safe last-line-wins stack algorithm. S085 shows per-mount emission and escaped path fields.”

| note claim | source finding | verdict |
|---|---|---|
| “per-mount emission” | `mounts_op`/`m_show` invoke `show_mountinfo` once per mount; each invocation terminates a single line at 188 | **ACCURATE** |
| “escaped path fields” | mount point 151 and generic root 145→`show_path`→`seq_dentry(..., " \t\n\\")`; octal escapes produced by `mangle_path` | **ACCURATE** |
| “not a safe last-line-wins stack algorithm” | true; line order is ascending `mnt_id_unique` creation order (`fs/namespace.c`), never stack order. `proc_namespace.c` alone shows only absence of ordering logic, not the positive order rule | **ACCURATE, with the S085 file alone under-supporting the positive part** |

No note sentence overstates the kernel evidence in a way that changes a C2 expectation.
The surrounding policy sentences (“refuse ambiguous duplicate covering points or
inconsistent chosen-parent topology”) are designed rules, not source claims, and are
consistent with the source fact that mountinfo carries `r->mnt_id` / `r->mnt_parent->mnt_id`
at 143–144.

## 5. Concrete discrepancies (report-only; nothing edited)

### D1 — anchor range end `135-193` is wrong (minor)

`show_mountinfo` is lines **135–191**. Line 192 is blank; line **193** begins
`show_vfsstat`. Under an inclusive-range reading the anchor imports the next function's
signature; under an exclusive reading it still includes the trailing blank line. The
function is fully contained, so no substantive claim depends on the overrun, but the
anchor is not exact. Correct bound if ever errata are admitted: `show_mountinfo:135-191`.

### D2 — Gate located quote is separator-only (minor, reporting precision)

The 4-word quote at 172 satisfies the ≤25-word located-quote form and is verbatim, but
it cannot by itself establish “per-mount namespace field emission/escaping.” The escaping
evidence is the esc argument `" \t\n\\"` at 151 and `mangle_path`'s octal code; the
per-mount evidence is the 135–191 body plus `mounts_op` in `fs/namespace.c`. Stated so
outside review does not over-credit the quote; the decision text itself remains correct.

### D3 — ordering claim is attributed to a file that does not contain the ordering rule (minor scope)

`fs/proc_namespace.c` has no iteration/ordering code. The positive fact — lines are
emitted in ascending `mnt_id_unique` order via an rbtree (`fs/namespace.c:1079-1100`,
`1536-1566`, `1580-1586`) — requires `fs/namespace.c`. Also, the registry sentence
“field layout is not a safe mount stack ordering rule” can be misread as denying topology
data, whereas fields 1–2 *do* carry `mnt_id` and parent `mnt_id` (143–144); what is unsafe
is inferring stack order from line order. A future erratum, not a registry edit here,
would cite `fs/namespace.c` and say “emission order is ascending internal unique mount id,
not mount-stack order.” This strengthens, not weakens, the round’s refusal of
last-line-wins (and therefore does not help the frozen contradictory expected row).

### D4 — mountinfo *source* field can carry an escape outside the amended contract's exact four (medium, contract-bounds)

The amended C2 rule says: octal-decode root, mountpoint and source with exactly
`040/011/012/134`; reject other backslash escapes as `QUOTA_SETUP`.

* Mount point: exactly those four — 151 esc set `" \t\n\\"`. Consistent.
* Generic root: exactly those four — `seq_dentry(..., " \t\n\\")` at `fs/namespace.c:5224`. Consistent (filesystem `show_path` overrides are out of scope for the default pair).
* Source: **not guaranteed** four. When a filesystem defines no `show_devname`, the
  source is emitted by `mangle()` at `fs/proc_namespace.c:87-90`, whose esc set is
  `" \t\n\\#"` — a `#` in the device name becomes `\043`, which the amended tool would
  reject as `QUOTA_SETUP`. **XFS defines no `.show_devname`** (`xfs_super_operations`,
  evidence `S078-fs_xfs_xfs_super.c:1334-1350`, only `.show_options`), so the xfs default
  `/tmp` mount takes the fallback path. Btrfs does define `btrfs_show_devname`
  (`fs/btrfs/super.c:2419-2434`) with esc `" \t\n\\"`, so the btrfs default is consistent.
* Impact on sealed material: none observed. No frozen case's `device_links`/mountinfo
  source contains `#` (frozen `CaseEscapedSpace` sources are `/dev/mapper/root`,
  `/dev/mapper/srv`, `/dev/mapper/data`). The frozen real control's documented mountinfo
  sources are `/dev/mapper/root` (btrfs `/home`) and `/dev/nvme0n1p1` (xfs `/tmp`),
  neither containing `#`. This is a bounds gap for operator-supplied paths with a `#` in
  a source name, not a change to any expected byte. Recommend either documenting
  `\043` as the fifth accepted source escape or restricting the exact-four rule to
  root/mountpoint in a future amendment; **no change made here**.

### D5 — “namespace paths” are reader-root-relative and can be skipped (medium scope caveat)

`seq_path_root(m, &mnt_path, &p->root, ...)` (151) emits paths relative to the opening
process's fs root, and the adjacent comment (150) states: mountpoints outside the chroot
jail give `SEQ_SKIP`. `seq_path_root` returns `SEQ_SKIP` when `__d_path` fails
(`fs/seq_file.c:518-520`); `show_mountinfo` returns that value, and `seq_read_iter`
then clears the partially buffered record (`fs/seq_file.c:231-239`: a nonzero, non-hard
`show` result sets `m->count = 0` and advances), so the whole line is omitted rather than
emitted truncated. So
`/proc/self/mountinfo` is the reading process's-root view, not necessarily the whole
mount namespace. The row/note wording “namespace paths” is broader than the mechanism.
For the default unprivileged host run this is inert; for a probe run inside a chroot or
container, a covering mount can be invisible, which would surface as `no_covering_mount`
rather than as an error. This belongs in the probe's stated limits, not in any expectation.

## 6. Bearing on the round’s claims (read-only; nothing executed)

* **C1 calibration (held5):** S085 has no dependency on the retention reconciler, the
  schema-v2 field, the oracle, or the alias counter. I observed no C1 evidence and ran no
  driver/oracle; nothing here touches `26/26`, the alias 8→0, the source-delta guard, or
  the separate quota-selftest arm.
* **C2 coverage (held6, strict target UNPROVABLE 29/30):** S085 supports the amended
  decode of escaped mount points (space/tab/newline/backslash → `\040`/`\011`/`\012`/`\134`)
  and the refusal to infer stack order from mountinfo line order. It does not repair the
  frozen `CaseEscapedSpace` contradiction: selected mount 43 declares parent 33 (143–144
  semantics: field 2 is the parent mount id), while the longest strictly-shorter cover is
  `/srv` mount 42; an `enabled` row at `/srv/my data` is inconsistent with that parent
  field, and the sealed conservative rule’s `unknown`/`ambiguous_overmount` outcome remains
  the source-compatible one. The strict red stays a strict red; no special case,
  exclusion, relabel or rewrite was applied, and the case/oracle/rule bytes were not read
  into any change.
* **Separate quota selftest arm:** untouched and not conflated with the frozen case. No
  selftest was run.
* **Open debt:** unchanged (four unallowlisted hits, original permission RED 11/12, two
  unknown dispositions, blocked baseline acceptance, privacy_clearance=false). This report
  makes no clearance, health or admission claim.

## 7. Residual unknowns and limits of this seat

* Tag `v7.2` was verified only as a resolvable GitHub raw URL returning stable bytes; no
  Git tag object/signature was fetched or verified, and no upstream mirror comparison was
  made.
* No live host `/proc/self/mountinfo`, sysfs, quota or mount state was read (forbidden for
  this seat; only RerunPinnedDriver is authorized for the declared live reads). D4/D5 are
  source-and-code facts, not host observations.
* Whether any operator-pinned real path has `#` in its mount source is unknown and was not
  probed.
* Filesystem-specific `show_path` overrides were not enumerated; only btrfs/xfs (the
  round’s default pair) were checked to lack `.show_path`. D4’s source-escaping statement
  is grounded on the fallback `mangle()` path plus XFS’s missing `.show_devname`; other
  filesystems’ `show_devname` escape sets were not surveyed.
* No driver, oracle, tool, selftest, build, lint, formatter or gate was executed; the only
  processes were `curl`, coreutils text/hash tools, `python3` for JSON shaping, and
  read-only `git` (`rev-parse`, `log`, `show`, `status`, `cat-file`, `merge-base`).

## 8. Tooling and artifacts

No installs, upgrades, service restarts, package transactions or environment changes.
Host tools used: `/usr/bin/curl`, `/usr/bin/sha256sum`, `/usr/bin/diff`, `/usr/bin/awk`,
`/usr/bin/grep`, `/usr/bin/python3` (3.14.8), `git` read-only. No `/tmp` fallback; TMPDIR
material is under `/fast/scratch/hyaku/mori-r23/ReopenS085/`.

Scratch receipts (outside the lane, absolute):

* `/fast/scratch/hyaku/mori-r23/ReopenS085/proc_namespace.c` — sha256 `fd82c0db52055ae807ee0b46c7c9bc5d47a9239805eb8ca5c47d2ba81d695776`, 7957 bytes
* `/fast/scratch/hyaku/mori-r23/ReopenS085/namespace.c` — `3c2417e6bd81a82de3a989caf6b80ac28658954dcc20078a60d1a5b4925fcdaa`
* `/fast/scratch/hyaku/mori-r23/ReopenS085/seq_file.c` — `db28fa9bd5006c76035f5ac27d1d888024d31e37f553828c55451b94bcc8ac0d`
* `/fast/scratch/hyaku/mori-r23/ReopenS085/seq_file.h` — `d44152495b20227ce08f0fe0a08d44eaeffd974a264eea1809074c4a8c338886`
* `/fast/scratch/hyaku/mori-r23/ReopenS085/btrfs_super.c` — `d1731b24b5c1e134c832b92601ccccf2a9955b1bcee9dc81f333a330a59e1ca8`

This report is the seat’s sole lane artifact:
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/ReopenS085.md`.

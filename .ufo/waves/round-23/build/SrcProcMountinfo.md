# SrcProcMountinfo — C2 mountinfo anchor re-open

Seat: `MadoR22-2.SrcProcMountinfo-8` (source re-opener). Contract read in full at
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md` (frozen, lane
commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`). Detection only; `SOURCES.md` untouched.
No implementation, case, oracle or frozen file read.

## Provenance

| item | value |
|---|---|
| URL | `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst` |
| fetch | `curl -sS -o <scratch>/proc.rst <URL>`; HTTP 200 (HEAD same run), `etag: "5c91b8f61c06394ce73bba05a6db3b9ddc08244e3a75e2d5fbc06be20314422f"` |
| local copy | `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round23/SrcProcMountinfo/proc.rst` (only allowed dir) |
| bytes | 107560, ASCII text, 2495 lines |
| **SHA-256 (whole fetched bytes)** | **`e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126`** |
| SHA-256 lines 1965–2002 (§3.5 body) | `4a2a1e4fcbee233e689921816f460eb2894703849280d2dda541c4a1654122ec` (`sed -n '1965,2002p'`) |
| installs | none (system already had `curl`; no pacman/uv/npx/cargo use) |

URL `v7.2` is a moving-branch name, not an immutable tag commit, so reproducibility is bound
to the byte digest above; the ETag is recorded as the server's view of the same bytes.

## Anchor verification (observed)

Claimed anchor "section 3.5 mountinfo fields (~1965-1990)" — **accurate**. Exact lines:

- Section header `3.5\t/proc/<pid>/mountinfo - Information about mounts`: **1965** (tab after `3.5`), underline 1966.
- Example line with field markers: **1970–1971**.
- Numbered field list (1)–(6), `(n…m)`, `(m+1)`, `(m+2)`, `(m+3)`, `(m+4)`: **1973–1983**.
- Rule sentence "Parsers should ignore all unrecognised optional fields.": **1985**; optional-field table **1988–1993**; footnote 1995–1998; propagation pointer 2000–2002.
- Section body ends **2002**; 3.6 header at **2005** (blank 2003–2004). So the claimed window
  contains the header and the entire field table; the section extends 12 lines past 1990.

## Located quote (verbatim, alignment runs of spaces collapsed)

> "(n…m) optional fields: zero or more fields of the form "tag[:value]" (m+1) separator: marks the end of the optional fields" — `proc.rst:1979-1980`, 20 words.

It backs contract §C2 rule: *parse mountinfo per proc.rst §3.5 (fields 1–6, optional fields
until `-`, then fstype, source, super options)*. The quote fixes the optional-field block and
its terminator; the immediately following lines carry the rest of the same layout:
`(m+2) filesystem type: name of filesystem of the form "type[.subtype]"` (1981),
`(m+3) mount source: filesystem specific information or "none"` (1982),
`(m+4) super options: per super block options` (1983).
Corroborating anchor for the `device_check` half of the same §C2 rule:
`(3) major:minor: value of st_dev for files on filesystem` (1975).

## Verdict per §C2 sub-rule

**Supported (observed, exact):**

1. Field order 1–6 → optional `tag[:value]` fields → separator → fstype → source → super
   options: 1973–1983, plus the worked example 1970. Supports the parse layout.
2. `major:minor` is `st_dev` of files on the filesystem: 1975. Supports the general
   `device_check: "match"` / `device_mismatch` comparison for a mounted path.
3. Mount point is "relative to the process's root" (1977); for `/proc/self/mountinfo` of a
   process whose root is `/`, mount points are absolute — supports absolute-prefix matching
   against `os.path.realpath(path)`.
4. Tolerance for unknown optional fields: 1985–1986 ("Parsers should ignore all unrecognised
   optional fields"), consistent with matching optional fields only until the separator.

**Under-determined (no rule text in this source):**

5. **Octal escape decoding** of `\040`, `\011`, `\012`, `\134` in the mount point. `proc.rst`
   never mentions escaping, substitution, mangle or backslash; the strings `space character`,
   `whitespace`, `substitut`, `mangle`, `backslash` do not occur anywhere in the file. The only
   `\040` in the whole document is an unannotated path inside an smaps example
   (`proc.rst:705`, `/anon_hugepage\040(deleted)`), i.e. an intra-document precedent for the
   procfs convention at best, not a mountinfo rule. The contract's escape rule is therefore
   **not carried by this source**; it needs `man 5 proc` or `fs/proc_namespace.c`
   (`mangle_path`) to be stated as a rule. Do not cite proc.rst §3.5 for it.
6. **Mount resolution / tie-break** ("candidate mounts", "longest mount point", "among equal
   mount points the last line wins"): `proc.rst` contains no resolution algorithm and no text
   about duplicates or ordering (`longest`, `last line`, `duplicate` absent; only 1973 warns
   that mount IDs "may be reused after umount", which is a non-identity warning, not ordering).
   The selection rule is the probe's own choice, not a documented procfs contract.
7. **The literal `-` separator token**: the text says only "separator" (1980); `-` appears only
   in the example line (1970). "Optional fields until `-`" is supported by example, not by
   rule text.
8. **Option syntax** (comma-separated list, `key=value`, bare keys such as `noquota`): shown
   only in the example (`rw,noatime`, `rw,errors=continue`, 1970). No text states
   comma-separation or the `key`-before-`=` form that §C2's classification table relies on.
9. **`type[.subtype]` vs table lookup**: 1981 documents that fstype may carry a subtype. §C2's
   classification table keys on bare `xfs`/`btrfs`/`ext2|3|4`/`tmpfs` and does not say whether
   a dotted type (e.g. `fuse.sshfs`) is split before lookup or falls through to
   `unsupported_fstype`. This source makes the dotted form possible; the contract does not
   resolve it. [INFERENCE: either choice is defensible; it must be fixed by L1 or by a case.]
10. **btrfs subvolume anonymous `st_dev`** (contract's `btrfs_subvolume_skipped`, S081): the
    document is silent on btrfs and states 1975 unconditionally ("value of st_dev for files on
    filesystem"). A literal reader would expect equality, so §3.5 can neither justify nor
    forbid the btrfs skip; it must not be cited as evidence for the exception.

**Contradicts:** nothing. No statement in §3.5 is contradicted by the contract text as written;
the contract goes beyond this source in items 5–10 rather than against it.

## Tier

**Tier A — scoped.** Basis: primary upstream kernel documentation (same convention as registry
rows S001/S002, kernel docs → A), exact anchor, quote directly stating the parsed layout.
Scope cell to carry:

> `/proc/<pid>/mountinfo` textual field layout (fields 1–6, optional `tag[:value]` fields
> terminated by the separator, fstype, source, super options) and `major:minor` = `st_dev` for
> files on the filesystem. **Excludes** octal-escape decoding of mount points, mount
> selection/tie-break rules, option-list syntax as a rule, fstype `type[.subtype]` handling,
> btrfs subvolume anonymous `st_dev`, and any quota-mechanism claim (this file documents no
> quota surface).

The escape-decoding clause (item 5) is **tier C as evidenced by this source** — re-open
`man 5 proc` or `fs/proc_namespace.c` if the registry needs an A for that clause; items 6–8 and
10 likewise should be labelled implementation choice / other-source, tier C here.

## Remaining unknowns / gaps

- Escape-decoding authority for `\040 \011 \012 \134` is outside this source (unresolved here).
- Whether the registry wants one combined row for `proc.rst` or separate rows for layout (A)
  and escaping (C) is L1's call; this seat did not edit `SOURCES.md`.
- The `v7.2` ref is a branch, not a tag; only the recorded SHA-256 pins the bytes.
- No host probe, quota tool, sysfs or mountinfo read was performed by this seat; nothing here
  speaks to the frozen real control (`frozen/c2-expected-real.json`).

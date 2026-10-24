# ReopenS082 — source row S082 re-open at the pinned production revision

Seat: `MadoR22-2.ReopenS082` (leaf; no dispatch, no child).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Pin examined: `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`. Working HEAD is
`6eb889c` (falsification payload commit); `corpus/SOURCES.md`,
`corpus/lessons/round-23.md` and `corpus/knowledge/quota-surface-r23.md` are
byte-identical between the pin and the working tree (SHA-256 shown below), so the
row/lesson/note read here are the pinned bytes.
Scope: verify registry row S082 only — scope, anchor, rawSHA, the ≤25-word located
quote in the lesson Gate, and the new knowledge-note claim-vs-source. No edits to
registry, frozen bytes, oracles, cases or production. No host state read, no quota
tool invoked, no installs.

## Row under review (verbatim, pinned `corpus/SOURCES.md:88`)

> `| S082 | Linux proc mountinfo layout v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst | docs | A | textual mountinfo field layout only | section3.5:1965-2002, field table:1973-1983; tag v7.2; sha256 e760f716f8278dee | Scan optional fields to the separator, then read fstype, source and super options; no last-line topology guarantee is taught. | mined | 2026-10-21 | on-release | corpus/lessons/round-23.md, corpus/knowledge/quota-surface-r23.md |`

## Provenance (observed)

| item | value |
|---|---|
| URL | `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst` |
| fresh fetch | `curl -sSL --fail` to `/fast/scratch/hyaku/mori-r23/ReopenS082/proc.rst`, HTTP success |
| fetched bytes / lines | 107560 / 2495 |
| fetched SHA-256 | `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126` |
| ref type | `git ls-remote` → `refs/tags/v7.2` = `237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63` (tag object), peeled `refs/tags/v7.2^{}` = `8d3ae59288f1e7d58d76558a6ee96d533bc5019f` |
| tag-commit cross-fetch | bytes at `8d3ae592…` are byte-identical to the `v7.2` fetch (`cmp` clean, same SHA-256) |
| retained evidence | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/evidence/sources/S082-Documentation_filesystems_proc.rst` is byte-identical to the fresh fetch |
| manifest | `evidence/sources-manifest.json` S082: bytes 107560, sha256 `e760f716…d126` |
| quote receipt | `evidence/source-quotes.json` S082: quote, `word_count: 7`, `found_in_whitespace_normalized_source: true`, `source_sha256` same digest |
| registry-row history | row bytes `sha256 b5d8eba8…e5f2` identical at admission commit `c1e8b81` and at pin `f3dc07c`; absent at original contract commit `4dc80c1` (consistent with lesson Gate: forward IDs, not pre-existing rows) |
| corpus file digests | `SOURCES.md` `1f49a4d8…ad09`, lesson `93cfe32d…339b`, note `2614a8f1…8c84` identical pin vs working tree |

## Anchor / quote verification (observed, mechanical)

Fresh bytes checked line-by-line:

- §3.5 heading `3.5\t/proc/<pid>/mountinfo - Information about mounts`: **1965** (underline 1966).
- Worked example line: **1970**; field markers **1971**.
- Numbered field table (1)–(6), `(n…m)`, `(m+1)`, `(m+2)`, `(m+3)`, `(m+4)`: **1973–1983**, exactly matching the anchor's `field table:1973-1983`.
- `(3) major:minor: value of st_dev for files on filesystem`: **1975**.
- `(m+1) separator: marks the end of the optional fields`: **1980**.
- `(m+2)/(m+3)/(m+4)` filesystem type / mount source / super options: **1981–1983**.
- Rule sentence `Parsers should ignore all unrecognised optional fields.`: **1985**, single occurrence in the file after whitespace normalization, **7 words** (≤25).
- §3.5 body ends **2002** (`Documentation/filesystems/sharedsubtree.rst`); 3.6 header at **2005**. Anchor window `1965-2002` is exact.
- Lesson Gate row S082 cites the same sentence at line **1985** (`corpus/lessons/round-23.md:48`); quote is located and within the word limit.

Digest verification: registered prefix `e760f716f8278dee` matches the full fetched
and retained SHA-256; `sources-manifest.json`, `source-quotes.json` and the raw
evidence file agree with each other and with the live v7.2 tag bytes.

## Scope / teaches claim-vs-source (observed)

- "Scan optional fields to the separator, then read fstype, source and super
  options" — supported by 1979–1983 plus the 1970 example. The doc states optional
  fields are zero or more `tag[:value]` fields and the separator marks their end;
  fstype/source/super options follow in that order.
- "no last-line topology guarantee is taught" — **verified as an absence**: a
  whole-file scan finds no mount-list ordering/sequence/duplicate/"last line" rule
  (`mountinfo` occurs only at 42, 1965, 2039; no ordering-language near §3.5). The
  only nearby identity statement is 1973, that a mount ID "may be reused after
  umount" — a non-identity warning, not an ordering rule. `(2) parent ID` at 1974
  defines the field but teaches no resolution algorithm.
- Scope "textual mountinfo field layout only" is honest: the file is general /proc
  documentation, and the row claims only §3.5.

## Note claim-vs-source (observed)

The knowledge note cites S082 exactly once (`corpus/knowledge/quota-surface-r23.md:60`):

> "S082 describes mountinfo fields, not a safe last-line-wins stack algorithm. S085
> shows per-mount emission and escaped path fields."

- First sentence: accurate. S082 gives the field table and no topology/ordering
  algorithm; the note states a negative, not a guarantee.
- Second sentence: accurate at the cited granularity. `S085` (retained
  `fs/proc_namespace.c`) shows `show_mountinfo` at 135, `seq_path_root(m, &mnt_path,
  &p->root, " \t\n\\")` at 151 for the mount point, devname mangling at 114/180, and
  the `" - "` separator at 172. It demonstrates the escape character set and call
  site, not the octal spelling.
- The rest of that note section ("component boundaries, never a bare prefix";
  "refuse ambiguous duplicate covering points or inconsistent chosen-parent
  topology") is presented as probe behaviour, not attributed to S082, and is
  consistent with the row's explicit non-claim.
- The note's `verified-at` provenance line is consistent with the manifest and quote
  receipts above.

**Verdict: no claim in row S082 or in the note's S082 sentence is contradicted by the
source. The row's negative ordering claim is correct, and the Gate/note do not cite
S082 for escaping.** This also means the frozen `CaseEscapedSpace` parent-topology
expectation is neither supported nor forbidden by S082; the conservative refusal
rule is a contract choice, exactly as the Gate's "no last-line ordering or escape
guarantee inferred" states. I did not touch, relabel or re-evaluate that case.

## Concrete discrepancies (reported, not edited)

1. **Prior seat's provenance remark is wrong (not the registry).**
   `.ufo/waves/round-23/build/SrcProcMountinfo.md` says "`v7.2` is a moving-branch
   name, not an immutable tag commit". Observed: `refs/tags/v7.2` is an annotated
   tag (object `237a1c39…`, peeled commit `8d3ae592…`), and the bytes at that peeled
   commit equal the fetched/retained bytes. The registry's "tag v7.2" is correct.
   The prior report's substantive F-7 escape finding still stands. Confidence: high.
2. **No registered row covers the exact octal encoding, and S082 is silent on
   escaping.** Whole-file scan: the only `\NNN` sequence anywhere in `proc.rst` is
   `\040` in an smaps example at line 705 (`/anon_hugepage\040(deleted)`); the words
   escape/backslash reasoning never occur in §3.5. The escape character set is
   observable in S085 (`" \t\n\\"`), but the `\040/\011/\012/\134` mapping itself is
   implemented in `fs/seq_file.c` (`mangle_path`), which is not a registered source
   row. Consequence: the amendment's strict "reject other backslash escapes as
   QUOTA_SETUP" and the `\040`-decoding rule are defensive implementation rules, not
   source-taught facts; they must not be cited to S082. The lesson Gate already
   disclaims an escape guarantee and the note does not overclaim, so this is an
   inherited coverage gap (prior F-7), not a false row. Confidence: high on absence,
   high on attribution.
3. **Minor scope wording, no correction required.** The row's scope says "textual
   mountinfo field layout only", while line 1975 also states a semantic
   (`major:minor` = `st_dev` for files on the filesystem). The row's `teaches` does
   not mention it and the note does not use S082 to justify device equality (btrfs
   behavior is attributed to S081). Not a contradiction; flagging only so a later
   device-check citation is not silently billed to this row's negative scope.
   Confidence: high.

## Limits

- Absence claims (ordering, escaping) are whole-file text scans of the pinned bytes,
  not a proof about kernel behaviour outside this document.
- Read-only: no host `/proc`/sysfs/quota command, no journal, no credential/config
  files, no transcript reads, no production/frozen/oracle edits. No packages
  installed. Scratch held only the two downloaded copies plus the comparison command
  output under `/fast/scratch/hyaku/mori-r23/ReopenS082/`.
- No implementation, oracle, case or frozen expectation was read for this check, so
  no statement here evaluates C1/C2 results or the strict red driver.

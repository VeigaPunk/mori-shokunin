# ReopenS083 — Linux ext4 quota-option documentation at v7.2

Seat: `MadoR22-2.ReopenS083` (leaf, read-only; no dispatch, no children).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Pinned production: `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`.
Working HEAD: `6eb889c037163e4886eaa61501258910d6a529b9` (payload child of the pin;
`git diff pin..HEAD -- corpus tools` is empty). Scratch:
`/fast/scratch/hyaku/mori-r23/ReopenS083/`. No registry, lesson, note, frozen case,
expectation, oracle or production byte was edited. No selftest, oracle, driver, quota
tool or privileged interface was executed; no live host state was read. No tool
install/update. No `lsp` device is mounted in this environment: identity below is
established from exact bytes and line numbers, not lane-wide grep-as-semantic-proof.

## Verdict

Row S083 **passes its documentary checks**: URL (v7.2 path), full rawSHA, anchor
`quota options:261-271`, the ≤25-word lesson23 Gate quote at line 262, and the row's
scope/`teaches` first clause all agree with the pinned bytes. **No registry correction
is required.**

The new knowledge note quotes S083 faithfully, and its operational conclusion
(`ext2/3/4` → `unknown`) remains the safe one for this probe. Three source-quality
findings are reported, none of which changes a frozen byte or an expected output:

1. The note presents S083's “ignored by the filesystem” as the mechanism. In v7.2
   ext4 code the same mount options are parsed and, when the superblock QUOTA feature
   is on, select `DQUOT_LIMITS_ENABLED`; the doc sentence is not a complete kernel
   behaviour statement. The probe still cannot know the feature, so `unknown` stands.
2. S083 is ext4-specific; the note's `ext2/3/4` row over-generalizes the source.
3. S083 does not document `prjquota`; that tool key comes from the
   contract/amendment, not this row. Conservative output is unaffected in both cases.

## Inputs re-opened

| Input | Location |
|---|---|
| Registry row | `corpus/SOURCES.md:89` (path relationship line `corpus/SOURCES.md:100`) |
| Lesson Gate row | `corpus/lessons/round-23.md:49` |
| Knowledge-note claims | `corpus/knowledge/quota-surface-r23.md:25-28,46` |
| Retained source bytes | `.ufo/waves/round-23/evidence/sources/S083-Documentation_admin-guide_ext4.rst` |
| Manifest entry | `.ufo/waves/round-23/evidence/sources-manifest.json` S083: `bytes` 27676, `sha256` `7929550f…dbbd` |
| Quote receipt | `.ufo/waves/round-23/evidence/source-quotes.json` S083: 7 words, `found_in_whitespace_normalized_source: true` |
| Fresh upstream fetch | `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/ext4.rst` → `S083-remote.rst` |
| Code cross-check (outside registry) | v7.2 `fs/ext4/super.c`, `fs/ext4/ext4.h`, `include/linux/quota.h` → same scratch directory |
| Production vocabulary (read-only) | `tools/mori-quota-surface.py:201-214,360-371,499-505` |

## Identity — MATCH (observed)

- Fresh fetch: **27676 bytes**, **613 lines**, SHA-256
  `7929550fa95ed7a0d56cd32c78e3c5f3a598827c4e55f1607097bff2e169dbbd` — exactly the
  assignment rawSHA.
- Retained evidence file: same SHA-256; `cmp` fresh vs retained → **byte-identical**.
- Manifest S083 is `{bytes: 27676, sha256: 7929550f…dbbd}`; the registry stores the
  16-hex prefix `7929550fa95ed7a0`, which is a correct prefix of the full digest
  (same 16-hex convention as the other round-23 source rows). No checksum
  discrepancy.
- Registry row bytes are identical at the admission commit `c1e8b81`, at the pin
  `f3dc07c0`, and in the working tree: row-line SHA-256
  `d60a3c864b1df81a6032b6ca17393577198d286243b28501607e4bc909edfa07`.
- Pinned vs working-tree corpus digests are identical:
  `corpus/SOURCES.md` `1f49a4d8…ad09`, `corpus/lessons/round-23.md` `93cfe32d…339b`,
  `corpus/knowledge/quota-surface-r23.md` `2614a8f1…8c84`.

## Anchor and quote — observed line map

Pinned `ext4.rst` (1-based line numbers; section heading at 138, scope sentence 141):

| Line | Content |
|---|---|
| 138–141 | `Options` / `When mounting an ext4 filesystem, the following option are accepted:` |
| 261 | `quota, noquota, grpquota, usrquota` |
| 262 | `These options are ignored by the filesystem. They are used only by` |
| 263 | `quota tools to recognize volumes where quota should be turned on. See` |
| 264–265 | quota-tools documentation pointer |
| 267 | `jqfmt=<quota type>, usrjquota=<file>, grpjquota=<file>` |
| 268–271 | journal-replay description and “They replace the above quota options.” |

- Row anchor `quota options:261-271` lands exactly on the two option groups; there is
  no off-by-one. `261` is the plain group, `267` the journaled group, `271` its last
  line.
- The Gate quote `These options are ignored by the filesystem.` occurs **once** in the
  file, at line **262**, word-for-word. It is **7 words** (≤25), ending at the
  sentence period inside line 262. `source-quotes.json` independently records 7.
- The Gate row (`corpus/lessons/round-23.md:49`) cites `262` and uses that same
  sentence. No discrepancy.
- The quote is a statement about the option group `quota, noquota, grpquota,
  usrquota`; the row's scope “documented quota hint/replay settings” correctly covers
  both line 261–265 and the journaled group 267–271.

## Scope / `teaches` — claim vs source

Observed, source-supported:

- Row title and scope are ext4-specific and documentary: the page is
  `ext4 General Information` (line 4), and line 141 names “an ext4 filesystem”.
- “Plain quota hints are documented as ignored by the filesystem” is literal at
  line 262. “Journal-replay settings” matches 267–271 (“properly updated during
  journal replay”; “They replace the above quota options”).
- The row's phrase “documented … not active quota state” is honest: S083 states no
  runtime quota-on/off state and gives no superblock/quota-file inspection procedure.

Inference, not a source statement:

- “Neither hints nor journal-replay settings prove runtime accounting enabled” is a
  conservative design rule. S083 supports “the option text is not itself a quotaon
  observation”; it does not by itself prove the negative for every possible runtime
  configuration. The probe's separate limitation sentence (superblock quota feature
  unobservable) is the actual reason `unknown` is required.

## New note — claim vs source

Target: `corpus/knowledge/quota-surface-r23.md:25-28,46`.

| Note clause | Source evidence | Result |
|---|---|---|
| “S083 documents plain quota hints as ignored by the filesystem” | S083 261–262, literal | **Supported as a documentary quotation.** The document does say it. |
| “and journal options as replay configuration” | S083 267–271: “properly updated during journal replay”; “They replace the above quota options.” | **Supported.** |
| “Without privileged/runtime state inspection, report unknown both when a hint exists and when it does not.” | Design inference; S083 gives no runtime state and no superblock/quota-file reader. | **Supported as a probe rule**, not as a sentence in S083. |
| Table row: “ext2/3/4 quota hints/replay settings present or absent → unknown” | S083's quota-option section is ext4-only (lines 4, 141). It does not document ext2/ext3 quota-option semantics; its ext3 mentions are general background/migration text. | **Partially over-scoped** (F2). The conservative outcome is unaffected. |
| Tool vocabulary includes `prjquota`; note cites S083 for “quota hints” | S083 contains **no** `prjquota` token; its plain group is `quota, noquota, grpquota, usrquota` (261). `prjquota` comes from the original contract/amendment, not this source. | **Coverage gap** (F3); no output change. |

### F1 — The note's mechanism explanation is doc-only; v7.2 ext4 code consumes the options

This is the one substantive claim-vs-source finding. It concerns the note's
*explanation*, not the registry row (which is documentary-accurate: it says
“documented as ignored”) and not the probe's conservative verdict.

Observed in fresh v7.2 code (cross-check, not a registered S row):

- `fs/ext4/super.c` (`sha256 4cae23697c9577237cb779f62122358a4fc1fd24f7f971535b82976b673139ac`,
  7613 lines), lines 1930–1939: `quota`, `usrquota`, `grpquota`, `prjquota` map to
  `EXT4_MOUNT_QUOTA | EXT4_MOUNT_USRQUOTA/GRPQUOTA/PRJQUOTA`; `noquota` is
  `MOPT_CLEAR` on those flags. The options are parsed, not discarded. Within
  `__ext4_fill_super` (5338), `ext4_apply_options(fc, sb)` runs at 5400, before the
  quota enable block below.
- Lines 5690–5695: at mount, `if (ext4_has_feature_quota(sb) && !sb_rdonly(sb))
  ext4_enable_quotas(sb);` — quota usage is enabled from the **superblock QUOTA
  feature**, independently of any mount option.
- Lines 7259–7270: `quota_mopt[]` is filled from `test_opt(sb, USRQUOTA/GRPQUOTA/
  PRJQUOTA)`; for each quota type with a quota inode, `ext4_quota_enable()` receives
  `DQUOT_USAGE_ENABLED | (quota_mopt[type] ? DQUOT_LIMITS_ENABLED : 0)`.
- `include/linux/quota.h` (`sha256 6acf78eaa04504881dff7f38fc4e85a4a76c0ec1054d123a778ee8e3c7980a5b`),
  lines 457–458 and 467–468: `DQUOT_USAGE_ENABLED` “Track disk usage”,
  `DQUOT_LIMITS_ENABLED` “Enforce quota limits”.
- `fs/ext4/super.c:2980–3004` iterates the set mount options and prints the token via
  `token2str`, so an ext4 mountinfo super-options field can carry the quota option;
  lines 2915–2946 separately print `jqfmt`/`usrjquota`/`grpjquota`.

Consequence: with the ext4 QUOTA feature on, accounting is enabled at mount for quota
types with quota inodes, and `usrquota`/`grpquota`/`prjquota` select limit enforcement.
The doc sentence “These options are ignored by the filesystem” is therefore not a
complete statement of v7.2 ext4 behaviour; it is accurate only in the narrower sense
that the options do not themselves turn accounting on, and it is closer to legacy /
non-feature behaviour. The doc itself does not qualify the sentence this way.

Impact: **none on the frozen output.** The probe reads only mountinfo/sysfs and does
not read the ext4 superblock QUOTA feature or quota inodes, so a visible ext option
still cannot establish the feature-dependent state; `unknown` (basis
`ext_quota_option_unverified`) remains the correct conservative projection. The
finding is that the note should say “the option's effect depends on unobserved
superblock feature/quota-file state” rather than presenting “ignored by the
filesystem” as the kernel mechanism. Frozen case rationales that repeat the same
doc sentence have the same wording limitation; their expected `unknown` tuples are
still correct for the fixtures' observable inputs.

### F2 — `ext2/3/4` is broader than S083's ext4 scope

- S083 line 4: `ext4 General Information`; line 141: “When mounting an ext4
  filesystem…”. The quota-option section 261–271 documents ext4 options only.
- The note's table row (line 46) says `ext2/3/4`. The ext2/ext3 branch in
  `tools/mori-quota-surface.py:364,501` is a design generalization from the
  contract/pre-seal amendment, not a claim sourced from S083. No ext2/ext3
  quota-option documentation is present in the quoted section.
- Impact: none on output (the branch returns `unknown` either way); the note's source
  attribution should be limited to ext4, or the ext2/ext3 extension labelled as a
  conservative design choice.

### F3 — `prjquota` is not in S083

- Whole-file scan: `prjquota` occurs **zero** times in S083. The plain group at 261 is
  `quota, noquota, grpquota, usrquota`; the journaled group at 267 is
  `jqfmt`, `usrjquota`, `grpjquota`.
- `tools/mori-quota-surface.py:203-214` includes `prjquota` in `EXT_QUOTA_KEYS`; that
  token comes from the original contract/pre-seal amendment vocabulary, not S083. For
  a `prjquota`-only mount the tool emits `ext_quota_option_unverified`, which is the
  same conservative rule; no false `enabled`/`disabled` claim is made.
- Impact: source-coverage note only; no registry, case or tool change is justified by
  S083 alone.

## Frozen-case cross-check (read-only; no execution)

Read-only inspection of the frozen ext cases shows the scored tuples remain
consistent with the conservative rule and with S083's documented vocabulary:

| Frozen case | Relevant mountinfo keys | Expected tuple | Source consistency |
|---|---|---|---|
| `CaseExt4Usrquota.json` | `usrquota` | `unknown` / `n/a` / `ext_quota_option_unverified` | `usrquota` is documented at S083 261; tool keys 207; unknown is the amended rule. Fixture has no superblock QUOTA-feature field, so F1's feature-dependent exception is unobservable. |
| `CaseExt4Journaled.json` | `jqfmt=vfsv0`, `usrjquota=aquota.user` | `unknown` / `n/a` / `ext_quota_option_unverified` | Both keys are documented at S083 267; tool keys 210–212; unknown is the amended rule. |
| `CaseExt4NoOptions.json` | none | `unknown` / `n/a` / `ext_quota_superblock_unobservable` | S083 gives no active-state authority; the superblock basis is the declared limitation. |

No frozen byte was changed. The ext cases' expected values do not depend on F1 being
universally true; they depend on the probe not observing the feature. The frozen
`CaseEscapedSpace`, the C2 29/30 strict red, C1 counts and the quota-selftest arm are
outside this seat's question and were not executed or re-measured.

## Concrete discrepancies (reported, not edited)

1. **F1 — note explanatory overreach (documentation-only).** S083 262 is exact, and
   the registry row's “documented as ignored” is accurate as a documentary statement;
   the finding is the note's use of the sentence as the kernel mechanism. v7.2
   `fs/ext4/super.c` consumes the same options: with the QUOTA feature set, mount-time
   `ext4_enable_quotas()` enables usage accounting and the
   `usrquota`/`grpquota`/`prjquota` flags select `DQUOT_LIMITS_ENABLED`. The note's
   “plain quota hints as ignored by the filesystem” should not be read as a complete
   kernel mechanism claim. The probe's `unknown` and all frozen tuples remain correct.
   Confidence: high on the quoted bytes and the code line map; medium only on how the
   parent chooses to word the note (no edit made).
2. **F2 — ext2/ext3 attribution.** S083's quota-option section is ext4-only; the note
   table's `ext2/3/4` row over-generalizes the source. Conservative output unaffected.
   Confidence: high.
3. **F3 — `prjquota` source gap.** S083 does not contain `prjquota`; the tool's key is
   from the contract/amendment, not S083. No output change. Confidence: high.
4. **No checksum, anchor, line-number or Gate-quote discrepancy.** The registry's
   16-hex prefix is correct; the full digest is in the manifest and fresh fetch. The
   row is byte-identical at admission, pin and working tree.

## Limits and non-findings

- This seat re-opened S083 only. The v7.2 `fs/ext4/super.c`, `fs/ext4/ext4.h` and
  `include/linux/quota.h` fetches are an outside-registry cross-check for F1; I did
  not add or edit a source row for them. If the parent wants a code-tier claim, it
  requires a separate registry decision.
- No live `/proc`, sysfs, mount, quota, journal, credential/config or transcript read;
  no `/tmp` artifact; no build/test/linter/formatter/gate; no quota command or
  privileged interface; no install.
- F1 is a source/documentation finding, not a claim about the current host or any
  actual ext4 mount. The probe's declared input fence (no superblock read) is exactly
  why the frozen output stays `unknown`; this report does not propose widening that
  fence.
- C1/C2 measured counts, `CaseEscapedSpace`, the strict driver red and the corrected
  quota selftest were not touched, re-run or re-labelled.

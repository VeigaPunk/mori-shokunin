# SrcExt4Doc — ext4 quota mount options (round 23, C2 source re-open)

Seat: MadoR22-2.SrcExt4Doc-8. Detection/report only. SOURCES.md not edited.
No installs, no builds, no live host probes. Local copy only under
`.scratch/round23/SrcExt4Doc/`.

## Question

Does `Documentation/admin-guide/ext4.rst` at tag `v7.2` support the contract §C2 row

> ext2/ext3/ext4 | any of `quota,usrquota,grpquota,prjquota,usrjquota,grpjquota` |
> quota_state `enabled` | enforcement `unknown` | basis `ext_quota_option`

and the declared anchor "quota mount options (~261-271)"?

## Provenance (observed)

| Fact | Value |
|---|---|
| URL fetched | `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/ext4.rst` |
| HTTP | 200, `content-type: text/plain; charset=utf-8` (2026-10-21 17:25:12 GMT) |
| Bytes / lines | 27676 bytes / 613 lines |
| SHA-256 (fetched bytes) | `7929550fa95ed7a0d56cd32c78e3c5f3a598827c4e55f1607097bff2e169dbbd` |
| Re-fetch | byte-identical (`cmp` clean, same SHA-256) |
| Annotated tag object | `237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63` |
| Tag target commit | `8d3ae59288f1e7d58d76558a6ee96d533bc5019f` (`refs/tags/v7.2^{}`) |
| Tag vs commit bytes | fetch at the resolved commit is byte-identical (`cmp` clean, same SHA-256) |

Raw URL bytes are therefore bound to the tag target commit, not just to a mutable branch ref.

## Anchor verification (observed)

- Section heading `Options` / `=======` at lines 138–139; preamble line 141:
  "When mounting an ext4 filesystem, the following option are accepted:".
- Line 261–265 is the plain quota item; line 267–271 is the journaled quota item.
  The declared anchor is exact; no drift.
- Whole-file search for `quota` reaches only lines 261–271 (plus unrelated
  `sourceforge.net/project/...` URLs at 29, 265, 271 and `fedoraproject.org` at 610/613).
  There is no other quota text, no feature-list entry, and no superblock-quota discussion.

## Located quotes

Supporting the existence and filesystem relevance of the journaled trio (lines 267–269):

> "These options tell filesystem details about quota so that quota information can be
> properly updated during journal replay."
> — ext4.rst:268–269, 18 words, line 267 opens the key list
> `jqfmt=<quota type>, usrjquota=<file>, grpjquota=<file>`; line 269 continues
> "They replace the above quota options."

Counter-quote for the plain trio (lines 261–263):

> "These options are ignored by the filesystem. They are used only by quota tools to
> recognize volumes where quota should be turned on."
> — ext4.rst:262–263, 23 words; the option key line 261 is
> `quota, noquota, grpquota, usrquota`.

## Verdict on the §C2 rule

**Under-determines the rule overall; contradicts its `enabled` label for
`quota`/`usrquota`/`grpquota`.**

Observed specifics:

1. **Token inventory: partial (5 of the contract's 6 trigger tokens).** The doc names
   `quota`, `noquota`, `grpquota`, `usrquota` (261) and `jqfmt`, `usrjquota`,
   `grpjquota` (267). `prjquota` (and project quota generally) appears nowhere in the
   file. The contract's trigger set therefore has one undocumented member.
2. **`enabled` for the plain trio: contradicted as written.** The doc states those
   options "are ignored by the filesystem" and exist so quota tools can "recognize
   volumes where quota should be turned on". Presence is documented intent, not proof
   that accounting or enforcement is active; the text explicitly allows "should be
   turned on" to be false at runtime.
3. **`enabled` for the journaled trio: under-determined.** `jqfmt`/`usrjquota`/
   `grpjquota` are consumed by the filesystem for journal replay, which is stronger
   than the ignored plain options, but the doc still does not say quota is enabled or
   enforced. It tells the filesystem how to update quota data during replay; nothing
   more.
4. **`prjquota`: unsupported.** No ext4 project-quota mount option is documented in
   this file at v7.2. Counting it as an enablement signal rests on no evidence here.
5. **Trigger-set gap (contract, not source):** `jqfmt` is grouped with `usrjquota`/
   `grpjquota` at line 267 but is absent from the contract's trigger list. A mount with
   only `jqfmt=vfsv0` would fall to the "none of them" arm and be reported `unknown`
   with basis `ext_quota_superblock_unobservable`, although this source shows the
   filesystem does act on `jqfmt`.
6. **`unknown` arm: supported, indirectly.** Because the documented plain options are
   ignored and only aid quota tools, their absence cannot prove quota is disabled, so
   the contract's `unknown` + `ext_quota_superblock_unobservable` for the no-option
   case is consistent with this text. The basis name also matches the doc's silence
   about superblock quota state.
7. **`noquota` handling: consistent.** The doc lists `noquota` among the ignored
   options, which agrees with the contract treating ext4 `noquota` as neither
   `disabled` evidence nor a trigger.
8. **ext2/ext3 scope: extrapolated.** The file is titled "ext4 General Information"
   and never states that ext2/ext3 share these option semantics. Applying the row to
   `ext2`/`ext3` is not supported by this source.

[INFERENCE] The paragraph reads as inherited ext3-era text (it defers to the
quota-tools package and to sourceforge URLs), and later ext4 kernels gained native
quota handling that the page does not describe. I did not open any ext4 C source in
this pass, so this is a staleness hypothesis, not a verified fact.

## Tier and scope I would assign

**Tier A, narrow scope — token semantics only, explicitly not enablement.**

Proposed row scope text: "ext4 mount quota option names and their documented handling
at tag v7.2: `quota`/`noquota`/`grpquota`/`usrquota` are documented as ignored by the
filesystem and used only by quota tools to recognize volumes where quota should be
turned on; `jqfmt`/`usrjquota`/`grpjquota` supply journal-replay quota details and
replace the plain options; `prjquota` is not documented; the page does not establish
quota enablement, enforcement, or superblock quota state."

Rationale for A: primary upstream kernel documentation, byte-bound to an annotated tag
and its target commit, no secondary mediation. Rationale for the narrowing: at this
scope the doc is authoritative only about what it actually says. If the row is meant to
back `quota_state: enabled`, it must **not** be admitted as support — the text says the
opposite for the plain trio and is silent-to-weak for the journaled trio.

Recommendation for L1 (no action taken here): seal this source for the option-name and
"ignored/recognition" claims only. Any `enabled` determination for ext2/3/4 needs a
code-level source (`fs/ext4/super.c` option parsing and `ext4_enable_quotas`, plus the
ext4 on-disk quota feature documentation) opened as a separate row; I did not open it
because it is outside this item.

## Effect on the C2 cases that ride on ext4

- `CaseExt4Usrquota` (expected `enabled`/`unknown`/`ext_quota_option`): this source
  cannot be cited for `enabled`; it documents `usrquota` as ignored by the filesystem
  and only a quota-tools recognition hint. The contract's own `limits` already concede
  the superblock quota feature is unobservable.
- `CaseExt4Journaled` (`usrjquota=aquota.user,jqfmt=vfsv0`): the strongest of the ext
  cases — the doc does show the filesystem consumes these keys — but the doc still
  evidences journal-replay quota detail, not active enforcement, so `enforcement:
  unknown` is the only defensible part.
- `CaseExt4NoOptions` (`unknown`/`ext_quota_superblock_unobservable`): supported by the
  doc's silence plus the plain options being ignored.

These are observations about source backing, not verdicts on the cases; case authors
derive expectations from the contract table and L1 owns sealing.

## Residual gaps (not resolved here)

1. `prjquota` on ext4: undocumented in this file at v7.2; no source in this pass.
2. Whether near-current ext4 actually honors the plain options (doc staleness): requires
   `fs/ext4/super.c` (and possibly `Documentation/filesystems/quota.rst`), not opened.
3. Whether the kernel prints these options into `/proc/self/mountinfo` super options is
   not stated anywhere in this file; the probe's real-mode ext classification depends on
   that behavior but this source neither supports nor denies it.
4. ext2/ext3 sharing of ext4 mount-option semantics is unverified.

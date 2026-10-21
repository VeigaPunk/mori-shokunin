author: mori-shokunin (L1 MadoR22-2, reused coordinator)
round: 23

# Round23 — distinguish a mechanism flag from an interface's presence

## Claims and authority

C1 calibration, held5: remove misleading raw_unallowlisted with schema-v2 clean
cutover; canonical scanner_unallowlisted retains its in-scope meaning and
raw_not_allowlisted its raw-complement meaning. C2 coverage capability, held6:
FR2 visible quota-mechanism state, not limits/usage, exhaustion, privacy clearance
or remediation. Original preregistration4dc80c1; source-derived amendments in
`.ufo/waves/round-23/preseal-amendment.md` precede opening/measuring the blind C2
candidate. Original proposals, oracles, failed drafts and all expected bytes remain
visible; revisions have new names. No observed C2 result selected an expectation.

MANIFEST rounds[427] admits r22's bounded retention accounting, not privacy/history
clearance. Four unallowlisted hits, original permission control RED11/12, two unknown
dispositions and blocked baseline acceptance remain debt. No r24.

## Mistakes

| ID | Class | Evidence pointer | Captured-by | Fix / fail-capability |
|---|---|---|---|---|
| M1 | chronology | r22 expected-real.json first landed with production8cb4afb; outside rounds[427] | existing freeze-order/expected-before-code requirements | Seal every executable oracle/driver/expected/dependency before implementation; strict ancestor, production absent/unchanged at seal. Actual guard red/green follows exercise; timestamps alone do not prove private chronology. |
| M2 | misleading population name | r22 raw_unallowlisted4 actually in-scope; raw_not_allowlisted9 | QUALITY70 population identity | Preregistered schema-v2 removal before build; keep scanner_unallowlisted4/raw_not_allowlisted9 and all historical artifacts. Exact two-source-transformation + object-equality guard prevents unintended code changes. |
| M3 | source contradiction | original contract ext enabled row versus S083262–263 | primary-source claim-vs-source check | Before seal/candidate inspection, change ext hints to unknown, preserve original proposals and separately derive corrected cases. A quota option hint is not quotaon state. |
| M4 | presence mistaken for active state | original btrfs qgroups-dir-present→enabled; source reviewers SrcBtrfsQgroup/Sysfs | primary lifecycle and enabled-flag source | Read qgroups/enabled first; do not read ASSERT-guarded mode unless on. Directory absence only follows successful parent inspection. Frozen present-but-disabled/unknown cases must distinguish this. |
| M5 | unsafe mount-order assumption | CriticContractC2 D1/D2; original last-line-wins | no-false-disabled reporting | Refuse duplicate covering mountpoints/ancestor-overmount ambiguity rather than infer topology from line order. Original stacked proposal retained; corrected case reports unknown. |
| M6 | incorrect reproduction mechanism | contract claims r22 stages tool from revision; CriticRenameHarm | instrument source review | r22 reproduces only in a checkout of its bound revision; subset output whitelist does not break when a key is removed. Real/refinement old-key checks are the actual API breakages. Append correction, never rewrite frozen original. |
| M7 | fixture invocation | first L1 before oracle used relative output, yielding relative synthetic repo path, then retried absolute | absolute tool/input paths | First uncommitted setup-only run was discarded before any freeze change; second absolute invocation gives expected25/26 (R25red, eight alias-bearing runs). Disclosure is not fabricated red-before evidence. No expected bytes changed. |
| M8 | procedure | early L1 used shell sed/grep/ls and Python edits rather than specialized tools; W1 CaseOptionalFields/DraftSourceRows used transient /tmp; sibling-case exposures disclosed by TmpfsUsrquota/SetupMalformed/NoCover/SymlinkRealpath | host tool policy and wave scope | Preserve deviations and limits, use surgical edits/targeted tools from correction onward. No retroactive independence or compliance claim; source-based expectations retained. |

## Gate

All source rows S077–S086 opened2026-10-21; raw bytes and SHA256 retained under
`.ufo/waves/round-23/evidence/sources/` and `sources-manifest.json`. Primary scoped
A is documentary authority, not proof of final implementation or runtime health.
S077–S084 were planned forward IDs at4dc80c1, not rows already present then.

| Row | URL | Located quote (≤25 words) | Decision / scope |
|---|---|---|---|
| S077 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/xfs.rst |171–173: “Forcibly turns off all quota accounting and enforcement within the filesystem.” | Admit A for XFS noquota vocabulary only, not limits or all enforcement states. |
| S078 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/xfs/xfs_super.c |253–254: `if (!(mp->m_qflags & XFS_ALL_QUOTA_ACCT)) seq_puts(m, ",noquota");` | Admit A for emitted XFS accounting/enforcement tokens, not synthetic conflicts/absence as host states. |
| S079 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c |2363: `enabled = fs_info->qgroup_flags & BTRFS_QGROUP_STATUS_FLAG_ON;` | Admit A for explicit enabled flag; reject directory-presence alone as active-state authority. |
| S080 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/qgroup.c |444: “default this to quota off, in case no status key is found” | Admit A for lifecycle/flag separation; initialized directory can persist with quota off. |
| S081 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/inode.c |8246: `stat->dev = BTRFS_I(inode)->root->anon_dev;` | Admit A for btrfs per-subvolume anonymous st_dev, not other filesystems or quota enablement. |
| S082 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst |1985: “Parsers should ignore all unrecognised optional fields.” | Admit A for mountinfo field layout only; no last-line ordering or escape guarantee inferred. |
| S083 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/ext4.rst |262: “These options are ignored by the filesystem.” | Admit A for documented option limitations; reject option-present as proof of enabled quotas. |
| S084 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/tmpfs.rst |132–134: “User and group quota accounting and enforcement is enabled on the mount.” | Admit A for tmpfs quota flags; hardlimit-only activation is not taught by this sentence. |
| S085 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc_namespace.c |172: `seq_puts(m, " - ");` | Admit A for per-mount namespace field emission/escaping, not topology inferred from ordering. |
| S086 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/shmem.c |4878–4879: `if (sb_has_quota_active(root->d_sb, USRQUOTA)) seq_printf(seq, ",usrquota");` | Admit A for actual tmpfs active-quota emission and four hardlimit names; no arbitrary suffix matching. |

New rows enter mined with used-by this lesson. They gain the final knowledge note
only after that note exists and cites them; mutable-field changes are logged below.
No existing immutable registry row is edited. Additional source rows085/086 close
original source coverage gaps, not implementation-result-selected evidence.

Reject: `QUOTA_DISABLED` means capacity/health/exhaustion clear; directory presence
means enabled; checksum means authenticated repository; author advisers are a fresh
non-author spot-check. Flip requires the actual missing authority, not a green
selftest. Current outside-lane admit/reject check remains pending parent closure.

## Scope and remaining debt

Mori observes kernel-visible state on runway targets, never fstab/mount units,
Snapper/config or superblock configuration and never quota commands/ioctls. Causes,
configuration/remediation route to tsukuroi/operator. No census integration or baseline
re-pin. Named default paths only; /dev/shm's tmpfs usrquota is outside the default pair.
QUOTA_DISABLED can coexist with ENOSPC. Parent now requires heavy scratch under
`/fast/scratch/hyaku/mori-r23/`; new work uses that root, and only this round's scratch
is removed at landing. Entering .scratch/round22 is operator/prior evidence, untouched.

Source used-by changes (all ten S077–S086): `corpus/lessons/round-23.md` →
`corpus/lessons/round-23.md, corpus/knowledge/quota-surface-r23.md`; mined→mined and
on-release→on-release unchanged. The note exists and cites every source. Delta receipt
is `build/DraftSourceRows.md` under the round23 wave directory.

Final source-safety correction before the seal: enabled-first plus mode-read still
races concurrent quota disable. SentinelProbe independently agrees with omitting
the real-mode qgroups/mode read entirely (S079 ASSERT, S080 disable ordering).
Real-mode mode metadata is intentionally null; fixture-only mode expectations are
unchanged. Original unexecuted candidates retain the rejected read for provenance.
This is not a claimed host crash reproduction or a reduced primary target.

Additional process disclosures: W1's attempt ledger is a retrospective binding of
seven zero-spawn refusals and one64-seat start, not proof of pre-call committed
payload logging (Q53/56). Static syntax/py_compile and in-memory contract checks
were exercised by several seats despite the no-verification prose; FixtureLint,
CaseOptionalFields and DraftSourceRows disclosed transient /tmp uses. No candidate
or live quota command was executed. Correct W2 logging/scratch practice cannot
retroactively remove this debt.

## First exercised counterexample after integration

The first complete run retained C1 original26/26 but C2 only5/30 and real-control
code2/input_unavailable. `evidence/measure1-debug.txt` identifies a ValueError:
classify returns ((state,enforcement,basis), mode), evaluate unpacked four flat
values. This is a caller/callee return-shape defect, not invalid fixture evidence.
The one-line destructuring fix changes production only; expected/oracle bytes
and denominators remain sealed. This is the actual red-before for the fix,
not a syntax/name-analysis claim. Corrected observations are recorded separately.

## Frozen rule versus inconsistent expected topology

Actual second run29/30 retains CaseEscapedSpace red. Decode its escaped mountpoint:
selected43 has parent33, but longest strictly-shorter cover /srv is42, so the
already-sealed conservative parent rule requires ambiguous_overmount. Its expected
enabled row is inconsistent. Captured-by existing QUALITY55; the source/fixture
checks missed normalization plus parent consistency before sealing. The fix is
admission discipline, not a result-driven expectation repair: preserve the rule,
expected bytes, red case and original denominator, and report strict C2 unprovable.
The whole driver demonstrably fails while C1's separate26/26 and guards remain
green. Main's exact ruling is retained in evidence/parent-strict-target-disposition.txt.

Two generic declared fixture validations (nonempty population and exact path-record
keys) gain co-evolved public-selftest arms. No frozen expectation changes, no
special-case for escaped paths and no implicit Core/capability admission.

The later public selftest's `escaped-mount-point` is a DIFFERENT, co-evolved arm
from frozen CaseEscapedSpace. It accidentally combines mount259:2 with helper's
default stat259:1, so an intended positive fixture becomes device_mismatch.
Correct only its input to explicit259:2, retaining the same expected positive
output and the red-before receipt. Never use that selftest correction to claim
the independent frozen topology case was fixed or its expected value changed.

## M9 — withdraw false confidence; do not repair the target

After the pinned96-seat falsification finished, Main required withdrawal from
production and admitted capability surfaces. The actual permission-loss proof
(`.ufo/waves/round-23/falsify/MutModeRead/permission-loss.json`) is fully mocked:
two UUIDs can potentially associate with dm-0; one UUID's devices-list raises
PermissionError and is discarded, so a surviving noqgroups association produces
false disabled confidence. No actual sysfs fault or live quota change was induced.
This is post-falsification evidence, not a pre-seal discovered/closed defect.
Unicode mount parsing and tmpfs accounting/enforcement distinctions add unclosed
limitations; they are not new exceptions to the original case set.

The active `tools/mori-quota-surface.py` and admitted
`corpus/knowledge/quota-surface-r23.md` were removed. Their exact bytes survive as
`rejected/deployed-quota-probe.py` and `rejected/quota-knowledge-note.txt` beneath
the round23 wave; the source archive is non-executable evidence, not a supported
tool. The SKILL quota row and support instructions are withdrawn. FR2 stays
Frontier; source-only study does not become a capability, Core or repertoire move.
C1's separate two-change schema/alias cutover remains, with no privacy clearance.
No enforcement experiment, special-case, relabel, changed oracle or rescue feature.

The original result stays29/30, and the original strict C2 target stays
unprovable/not admitted even though outside closure may diagnose the inconsistent
CaseEscapedSpace oracle. Rule and expected row are both sealed and unchanged.
After withdrawal the production capability is absent, not a newly passing case.
Criterion71 records the general lesson: incomplete enumeration cannot justify a
negative/unique-association claim; accounting-active is not enforcement-active.

## M10 — source corrections after falsification, not expected-value repairs

The late primary-source corrections are scoped to Linux v7.2 mechanisms, not an
attestation that this host's exact kernel build/configuration has those semantics.
Their full bytes, hashes and short literal quotes are retained in
`evidence/post-falsification-sources.json` and `post-falsification-quotes.json`.

* S087 `fs/ext4/super.c:7250`: “Enable usage tracking for all quota types.”
  Seven words. Adjacent mount-flag handling and feature-quota paths show why
  S083's ignored-options documentation is not complete current mechanism evidence.
* S088 `include/linux/quotaops.h:161-162`:
  `return sb_has_quota_loaded(sb, type) && !sb_has_quota_suspended(sb, type);`
  Six words. This active-accounting predicate does not test the separate limits bit.
* S089 `fs/quota/dquot.c:2667`:
  `ret = dquot_disable(sb, type, DQUOT_LIMITS_ENABLED);`
  Five words. With the surrounding sysfile/usage logic it supplies the static
  counterexample to inferring current enforcement from emitted active tokens.

The source corrections justify rejection; they do not change any frozen output
label, expected row or target. No runtime limit-disable operation was performed.

## M11 — discernment sample: keep source authority narrower than its appearance

Admit S079 only for its explicit enabled-attribute mechanism:
`enabled = fs_info->qgroup_flags & BTRFS_QGROUP_STATUS_FLAG_ON;` (five words).
That primary code supports the distinction between a qgroups directory and the
ON bit, not a per-ID limit, exhaustion verdict or complete candidate implementation.
Its literal normalized-source quote/hash is in `evidence/source-quotes.json`.

Re-opened S065 Python hashlib documentation at2026-10-21, current3.15.1, leaving
the original row's immutable3.15.0 anchor and rejected status unchanged. Exact
21-word quote: “At any point you can ask it for the digest of the concatenation
of the data fed to it so far”. This is credible API documentation but does not
authenticate historical receipt authorship, source selection, admission or loss
disposition. Re-reject it as sole provenance authority; retain
`evidence/rejected-source-recheck.json`. These are self admission/rejection
decisions awaiting outside closure agreement, not claimed independent agreements.

## M12 — preserve source-path and chronology defects

`frozen/case-decisions.json` names a corrected CaseTmpfsNoQuota proposal whose
transient source path is absent in the seal and every subsequent commit. The
selected frozen bytes themselves landed before production implementation and
remain unchanged. Original and frozen proposals have identical expected rows but
different scenario/rationale/fixture bytes; “fixture unchanged” would be false.
`evidence/tmpfs-source-provenance-erratum.json` records the missing pointer and
both hashes. Do not rewrite that sealed ledger or claim a later reconstructed
file existed before sealing.

The declaration's “before any implementation” shorthand means before production
landing: contract§delivery explicitly allowed a blind draft during wave1. The
complete seal22772c10 precedes production1979a9de; it does not predate every draft.
W1's canonical payload record was bound retrospectively after seven cap-refused
calls and the successful eighth; native receipts prove64 spawned, but no later
ledger repairs the missing pre-call chronology. W2's96 payload/spec and ledger
binding were committed/recorded before its single successful call. All160 native
seats completed; none died, were replaced or were reissued as new identities.

## Gate — final corrections and re-rejection (2026-10-21)

These scoped source decisions are self decisions awaiting outside closure, not
independently agreed admission. S087–S089 were opened by L1 and independently
re-fetched byte-identically by the existing source scribe; no runtime quota action.

| Row | Opened URL / access date | Located literal quote (≤25 words) | Gate |
|---|---|---|---|
| S087 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/ext4/super.c ; 2026-10-21 | line7250: “Enable usage tracking for all quota types.” (7) | A/mined for conditional v7.2 usage/limits mechanism, supersedes S083's incomplete ignored-options inference |
| S088 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/quotaops.h ; 2026-10-21 | lines161-162: `return sb_has_quota_loaded(sb, type) && !sb_has_quota_suspended(sb, type);` (6) | A/mined for loaded/non-suspended versus separate limits bit; supersedes S084's runtime-enforcement inference |
| S089 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/quota/dquot.c ; 2026-10-21 | line2667: `ret = dquot_disable(sb, type, DQUOT_LIMITS_ENABLED);` (5) | A/mined only with surrounding sysfile/usage logic, not an operation to execute |
| S065 | https://docs.python.org/3/library/hashlib.html ; 2026-10-21, observed3.15.1 | Hash algorithms: “At any point you can ask it for the digest of the concatenation of the data fed to it so far” (21) | retain C/rejected as sole provenance authority; immutable3.15.0 row anchor unchanged; a narrow API question plus separate provenance evidence would be a different scope |

Mutable-cell log: S077,S078,S079,S080,S081,S082,S083,S084,S085,S086 each
used-by `corpus/lessons/round-23.md` → `corpus/lessons/round-23.md,
corpus/knowledge/quota-surface-r23.md` during integration →
`corpus/lessons/round-23.md` at withdrawal. S065 used-by `—` →
`corpus/lessons/round-23.md`. All their statuses/rechecks and immutable cells remain
unchanged. New S087–S089 are mined/on-release/used-by this lesson; no older immutable
row is rewritten and no new row claims a current kernel build attestation.

## Mistakes — final falsification and coordination

| Class | Evidence | Captured-by | Disposition |
|---|---|---|---|
| Incomplete enumeration treated as a negative association | actual mocked `falsify/MutModeRead/permission-loss.json` | pre-seal unknown-on-permission-failure intent; now criterion71 | demonstrably false disabled on the deployed candidate; withdraw production/admitted C2 instead of an unsealed repair |
| Accounting-active collapsed into runtime enforcement | S086 with S088/S089, source-bit evidence | none for tmpfs in the former rule | frozen labels preserved, unsupported claim rejected; no live enforcement experiment or narrowed target |
| Transient corrected proposal deleted but selected source path retained | `evidence/tmpfs-source-provenance-erratum.json` | source-path pinning should have caught it | selected frozen bytes persist; original expected unchanged, fixture/scenario changed; missing historical pointer remains disclosed, not reconstructed as prior authorship |
| L1 continuation gave ambiguous live-source ownership while editing other files | existing source-scribe report's second continuation and `final-source-cutover.txt` | explicit separate-checkout rule | scribe touched live SOURCES then restored exact6eb889c bytes before L1's final integration; procedural breach remains, no retroactive compliance claim |
| W1 pre-call ledger binding absent | wave1 native attempts/retrospective ledger | Q53/Q56 timing discipline | seven no-spawn cap refusals plus64 spawned proved, chronology defect retained; W2 correctly bound before call |

The source scribe's final proposal header describes its restored current state,
not an absence of historical edits: its disclosure explicitly records the live
window. The sole L1 integrated the final four changes after that restoration;
no measured code result came from the transient draft. The redundant full-manual
withdrawal scaffold was removed with its base/patch/full hash retained in
`rejected/withdrawal-manifest.json`; the exact rejected probe/note remain intact.

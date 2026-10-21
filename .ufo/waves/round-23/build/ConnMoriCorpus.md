# ConnMoriCorpus — corpus entries the C2 probe must stay consistent with

Seat: `MadoR22-2.ConnMoriCorpus-8` (connector, leaf; no delegation).
Authority: `.ufo/waves/round-23/contract.md` (frozen, lane commit
`4dc80c1be48308075e83af17f15fbfe7e95e6cb8`) §C2 lines 65–150; `PROVINCE.md:45`;
`corpus/README.md:333`; read-only at the entering revision.

Method: read-only text reads and read-only git plumbing
(`git show 3da8414:tools/mori-census.sh`). No live host read of any kind (this item
does not name one), no candidate implementation (`build/ImplQuota`,
`.scratch/round23/ImplQuota` untouched), no cases-proposed content read, no
tests/builds/formatters, no VCS mutation, no writes outside this file. Peer reports in
this build directory were read as round-cache evidence and are attributed where used.

Result in one line: the C2 contract is **mechanically consistent** with the disk
thresholds proposal, `surfaces-r8`, `observability-surfaces-r2` and the `audit-r11`
debt register, but four corpus anchors carry wording or evidence-chain defects that
the new capability's documentation must not inherit, and one anchor
(`lessons/round-12.md:48`, M25) reads as a violation unless its scope is stated. One
blocker: `S077–S084` do not exist in `corpus/SOURCES.md` at the entering revision.

## 1. The four named entries — exact anchors and invariants

| # | Anchor (exact) | What it binds | Invariant C2 must keep |
|---|---|---|---|
| E1 | `SKILL.md:397-425` §"Disk thresholds are a PROPOSAL, not a measurement" | 85/95 carry no write-rate evidence (`:399-409`); the r7/r8 since-boot average is not a licence to recalibrate (`:408-409`); the fleet's reported disk failures are quota events and "the quota numbers are unreadable on this host" (`:411-413`); never threshold the btrfs chunk percent, keep the `df -P` parser (`:414-417`); never OR a byte floor against `df -P` Available (`:418-419`); **one pair only** (`:420-422`); the since-boot average is not fleet-attributable and smooths bursts (`:423-425`) | C2 adds no threshold, no percent, no pair, and no `threshold_label`; `df_covers_quota:false` restates the *mechanism* in `:412`, not the empirical sentence in `:411`; the `df -P` parser and chunk-percent ban stay untouched |
| E2 | `corpus/knowledge/observability-surfaces-r2.md:247-266` §5 disk | `df -P` over `MORI_DISK_TARGETS`, default `$ROOT /tmp` (`:249`); `DISK_UNAVAILABLE` info for absent/df-failed/parse-failed targets (`:251-252`); 85/95 are proposals, EDQUOT invisible to capacity-% (`:257-259`); the scratch root is not in the defaults and `/scratch/tmp` is absent, so `unavailable=0` does not classify it and coverage exists only when an operator pins the target list (`:260-264`) | the same two default paths; **`QUOTA_DISABLED` is path-scoped exactly like `unavailable=0`**; absent target is not a state verdict (r2 precedent); C2 follows the probe's own `--path`, not `MORI_DISK_TARGETS` |
| E3 | `corpus/knowledge/surfaces-r8.md:83-91` §1 disk (and `:24-25`) | live row byte-stable; `warn_pct=85 crit_pct=95` unchanged, "no threshold touched" (`:87`); r8 adds no rate; limitations: counts every write since boot, not fleet-attributable, **cannot see a burst** (`:89-91`); all r8 thresholds are local placeholders and labeled (`:24-25`) | C2 is a separate probe with no census row, no threshold, no severity; do not merge the quota blind spot and the burst blind spot into one claim; FR6 (instantaneous rate) and FR8 (threshold calibration) are untouched |
| E4 | `corpus/knowledge/audit-r11.md:218-222`; `:95-99`, `:168` (F13); `:216` (D21) | "No closure is claimed for … quota observability …" (`:218-222`), retained byte-unchanged; the **only first-hand quota event** is a census selftest abort, exit 1, 44 PASS, no tally, `printf: write error: Disk quota exceeded` (`:95-99`, `:168`); D21 keeps it environmental with quota diagnosis routed to operator/tsukuroi and requires the selftest to distinguish setup failure from a case result (`:216`) | C2 narrows the *scope* of the no-closure sentence by adding visible enablement; it does not clear `:218-222`, does not attribute the r11 abort, and does not discharge D21 |

## 2. Entries outside the four that bind the same prose

| # | Anchor | Why it binds C2 |
|---|---|---|
| E5 | `corpus/README.md:333` and `PROVINCE.md:45` (FR2 rows) | Both say only "`df` capacity percentages cannot detect quota exhaustion; observe and report only, never change quota state". Any C2 text that says "quota observability" unqualified contradicts the row it is supposed to advance. The narrowing must land in these rows (append-only), not replace the boundary sentence |
| E6 | `corpus/knowledge/observability-census-r1.md:182-184` | Origin of the coverage rule: `/scratch/tmp` absent and not in the default disk targets, so `unavailable=0` does not classify it. This is the direct precedent for "`QUOTA_DISABLED` does not classify unlisted mounts" |
| E7 | `lessons/round-12.md:48` (M25) | "A setup abort never borrows a verdict code (exit 2) and is neither a case PASS nor FAIL." C2's precedence gives exit 2 to **both** `QUOTA_SETUP` and `QUOTA_STATE_UNKNOWN` (contract lines 132–134). See C-1 |
| E8 | `SKILL.md:125,137` (journal-window precedent) | `rc2` already carries both `MORI_JOURNAL_WINDOW_UNAVAILABLE` and `MORI_JOURNAL_WINDOW_SETUP`, and "Neither code is a DRIFT, severity or alarm". This is the probe convention C2 follows; it is also the reason M25 cannot be applied to probe exit maps without scoping |
| E9 | `tools/mori-census.sh:288-295,321` (current census-r5 bytes) | `DEFAULT_ROOT` escalates to the parent when the lane directory name matches `*-shokunin`; `DISK_TARGETS` defaults to `"$ROOT /tmp"`. At the canonical lane (`…/mori-shokunin`) this is exactly `/home/vgpnk/Projects/shokunin /tmp`, i.e. the contract's C2 defaults — **verified equal**, but by code, not by the r2 note's pinned `:85` |
| E10 | `tools/mori-census.sh:353-357` (comment) | The EDQUOT sentence's in-repo origin, and the source of "85/95 is the single R1 proposal pair". The comment labels 85/95 as a proposal but states the EDQUOT claim as fact. C2 must not promote the comment to evidence |
| E11 | `corpus/SOURCES.md` (76 rows, S001–S076) | The contract's "sourced: S077–S084" is a forward reference at the frozen commit; `corpus/lessons/round-23.md` does not exist. See C-7 |

Pointer falsification, recorded so no later correction round "fixes" a correct anchor:
`observability-surfaces-r2.md:259` cites `:88-94` for the EDQUOT text. That is a
**census line anchor at the note's pinned revision**, and it is correct:
`git show 3da8414:tools/mori-census.sh` lines 88–94 are exactly the
`# PROPOSAL, NOT MEASURED … EDQUOT … 85/95 is the single R1 proposal pair` block
(observed directly). At census-r5 the same block is `:353-357`. `ScoutPriorQuota.md`
§P6 reads `:88-94` as the r2 note's own receipt fence and calls the pointer broken;
that reading is not supported — the only defect is that the note does not name the
census revision, which is the note's general convention.

## 3. Contradictions and their dispositions

**C-1 — M25 vs C2's exit map (apparent contradiction; documentation-only fix).**
`lessons/round-12.md:48` is unqualified: a setup abort never borrows a verdict code
(exit 2). C2 assigns exit 2 to a verdict (`QUOTA_STATE_UNKNOWN`) as well as to setup.
Against that, `SKILL.md:125,137` already uses rc2 for both an unavailable state and
setup in the journal-window probe, so the probe convention is established and
`CriticContractC2.md` L5 reaches the same reading. The contradiction is real *as
written text*, not as behavior: M25 governs the **oracle/case harness** (its evidence
is a 44-PASS tally with no tally line), while C2 is a standalone probe whose rc2 is
declared "not a DRIFT, severity or alarm". Required: the C2 note scopes M25 to the
harness, cites the journal-window precedent, and says `finding_id` (plus the JSON
`exit_code`) is the only discriminator. Forbidden: "C2 discharges D21/M25". The r11
abort itself was exit **1**, i.e. it borrowed a verdict code in the opposite
direction; C2 neither repeats nor fixes that path.

**C-2 — the empirical EDQUOT sentence has no receipt (real; wording risk).**
`SKILL.md:411` says the fleet's "*actually reported* disk failures are quota events";
`observability-surfaces-r2.md:258-259` repeats it. Corpus-wide there is **no EDQUOT
receipt**: the only first-hand quota event is `audit-r11.md:95-99,168`, a census
selftest `printf` abort whose filesystem was never identified (D21), and it is an
abort of the lane's own harness, not a "fleet reported disk failure". C2's
`df_covers_quota:false` is a mechanism claim and must not be cited as validation of
the empirical one. The frozen real control is a 2026-10-21 host observation whose own
note says a later differing run is drift, not rewrite; it says nothing about the host
state on 2026-10-15. Required: cite the mechanism only, and state that C2 neither
attributes the r11 abort nor identifies a fleet EDQUOT event. This is also the
FR9/`audit-r11.md:41-46` durable-evidence rule applied to prose.

**C-3 — "quota numbers are unreadable" vs newly readable state (real; wording).**
`SKILL.md:413` remains true for **numbers** (no per-user/group/project limit or usage
is read), but C2 does read quota **state** (`/proc/self/mountinfo` super options,
`/sys/fs/btrfs/*/qgroups` presence and optional `mode`). A note that says
"quota observability" without "visible enablement" contradicts the sentence it claims
to advance, and the contract's own limits. Required vocabulary: "visible enablement",
"reads no numbers", "detects no exhaustion". Forbidden: "quota numbers are now
readable", "quota exhaustion is visible".

**C-4 — `QUOTA_DISABLED` is path-scoped, and the corpus already has the counterexample
pattern (real; the strongest cross-link).** `observability-census-r1.md:182-184` and
`observability-surfaces-r2.md:260-264` establish the rule for `unavailable=0`: it does
not classify a path outside the target list. The frozen real control supplies the
concrete C2 instance — its note records "/dev/shm (tmpfs usrquota) is observed but
outside the default paths". So a default run can exit 0 `QUOTA_DISABLED` while an
enabled quota mount exists on the same host. Required: the note carries `/dev/shm` as
the named counterexample (not just the abstract limits sentence), states that
`QUOTA_DISABLED` describes only the named paths, and extends the
"coverage exists only when an operator pins the target list" rule to `--path`.
Also: C2's defaults are hardcoded in the contract; the census honors
`MORI_SHOKUNIN_ROOT`/`MORI_DISK_TARGETS`. The two agree at the canonical lane checkout
(E9) but are **not** the same override surface; do not write "the probe follows the
census targets".

**C-5 — no threshold, therefore no calibration (real; wording).** `SKILL.md:399-409`
and `:420-422` fix one proposal pair and forbid a second; `surfaces-r8.md:24-25` labels
every threshold-bearing row. C2's output has no severity and no threshold. Required:
one sentence in the note — "no threshold is added or changed; `QUOTA_ENABLED` is not a
threshold and must not carry `threshold_label=local`; FR8/D10 stay open". This keeps
the C1 calibration story and the C2 coverage story from being read as one calibration
change.

**C-6 — FR2's "first evidence" pointer does not support the capability (real;
evidence-chain defect).** `PROVINCE.md:45` and `corpus/README.md:333` cite
`audit-r11.md:218-222`, a blanket no-closure sentence whose own sub-citations are
`observability-census-r1.md:182-184` (scratch root) and `:216-221` (`MORI_*_BIN` /
environ) — neither discusses quota. The first-hand quota anchors are
`audit-r11.md:95-99,168,216`. Required when the note lands: append those anchors to
the FR2 row's first-evidence cell; otherwise the Frontier→Core narrowing cites a
sentence that does not support it. This is the same class as `audit-r11.md` F03/F04
and is fixed append-only, never by editing the audit.

**C-7 — S077–S084 and the round-23 Gate do not exist (blocker at seal time).**
`corpus/SOURCES.md` has 76 rows at the frozen commit (S001–S076); `corpus/lessons`
ends at `round-22.md`. The contract's "sourced: S077–S084" and the planned
`DraftSourceRows` rows (`queued`) are forward references. Required: the rows land in
`corpus/SOURCES.md` and `corpus/lessons/round-23.md` exists **before** any
`corpus/knowledge` note opens with a `source:`/`verified-at:`/`recheck:` trio citing
S077–S084. Until then the note must cite the v7.2 URL + anchor lines and say the rows
are queued. This is the only item that can make the r23 "sourced" claim literally
false.

**C-8 — contract table vs drafted source rows (tension to carry, not resolve).**
`DraftSourceRows/rows.md` S083 records that ext4 documents `quota`/`usrquota`/
`grpquota` as **ignored by the filesystem** and used only by quota tools, while the
contract's ext row says any such option → `quota_state: enabled`, enforcement
`unknown`, basis `ext_quota_option`. The contract's `enforcement: unknown` already
prevents an enforcement claim; the note must explain the basis as *tool-directed
intent visible in mount options*, never "ext4 enforces quota". Likewise S078's
finding that the kernel emits `noquota` only when no accounting flag is set means
`xfs_conflicting_quota_options` (contract row 4) is a **parser-robustness branch**,
not an observed host state; docs must not present it as a conflict seen in the wild.
These are documentation constraints inside the frozen contract, not proposed table
changes.

## 4. Required cross-links — checklist for the C2 note and the FR2 rows

1. Note header trio: cite S077–S084 **only after** they land (C-7); otherwise URL +
   anchor + `rows queued` status.
2. Prior-entry ledger with exactly these five anchors: `SKILL.md:397-425`,
   `observability-surfaces-r2.md:247-266`, `surfaces-r8.md:83-91`,
   `audit-r11.md:218-222` (+ `:95-99,168,216`), `lessons/round-12.md:48`. Each row:
   prior invariant / C2 delta (none or narrowed) / forbidden inference.
3. Mandatory concrete anchors: `/dev/shm` tmpfs `usrquota` outside defaults (C-4);
   `finding_id`-not-rc for exit 2 (C-1).
4. Mandatory negative sentences: no threshold/pair added (C-5); no limit or usage
   value read; no EDQUOT detection/attribution, including the r11 abort (C-2);
   `QUOTA_DISABLED` ≠ "no quotas on the host" (C-4); btrfs qgroups present ≠ a limit
   set; ext option ≠ enforcement (C-8); mountinfo/sysfs snapshot races not excluded.
5. FR2 updates in `PROVINCE.md:45` and `corpus/README.md:333`: append the new note and
   the first-hand anchors, keep the exact boundary sentence "observe and report only,
   never change quota state", do not mark FR2 closed, do not use "quota observability"
   unqualified.
6. `SKILL.md:413`: one added sentence only ("a separate read-only probe reports
   visible enablement only; it reads no numbers and detects no exhaustion"). Do not
   edit `:411-412` or the four historical notes.
7. Registry: one `probe` row, no census SURFACE/FINDING, no `tools/mori-census.sh`
   change (ScoutCensusDisk §7; `SKILL.md:515`).

## 5. Affected axes

- **A1 — C2 coverage-claim integrity (declared axis: coverage).** Improved: the
  "frontier → bounded Core" claim becomes path-scoped and falsifiable via `/dev/shm`
  and the `--path` rule instead of an abstract limits sentence.
- **A2 — C1 calibration isolation (declared axis: calibration).** Unaffected by
  design: no schema key, exit code, threshold or pair is touched; the ledger only
  points at `SKILL.md:397-425`.
- **A3 — evidence fidelity (contract).** Improved: breaks the unbacked
  EDQUOT-fleet-failure chain (C-2) and the unsupported FR2 first-evidence pointer
  (C-6).
- **A4 — substrate/registry.** Improved: the note and the source rows land in the
  right order (C-7), and `observability-surfaces-r2.md`'s correct `:88-94` pointer is
  protected from a false "fix".
- **A5 — verification reach.** Improved: a future falsifier has one ledger that names
  the invariant, the delta and the forbidden inference per prior entry, instead of
  reconstructing it from four notes and a code comment.

## 6. Proposed move (one, bounded)

**Land the C2 claim as an additive, path-scoped FR2 narrowing whose carrier is a
five-row prior-entry consistency ledger, with `/dev/shm` and `finding_id`-not-rc as
its two concrete anchors, in the same commit as append-only FR2 pointers — and edit
none of the four historical corpus notes.**

Concretely, for L1 at seal/integration:

1. New `corpus/knowledge/quota-surface-r23.md` with the §4.2 ledger, the contract's
   fixed limits, and the two anchors. The `/dev/shm` row is what converts
   "`QUOTA_DISABLED`" from a possible host-wide claim into a measured path-scope
   statement; the `finding_id` row is what keeps M25 from being read as violated.
2. `PROVINCE.md:45` and `corpus/README.md:333` gain the pointer + first-hand anchors;
   the boundary sentence is preserved verbatim.
3. `SKILL.md:413` gains exactly one separator sentence; `:411-412` is not rewritten
   and neither is `surfaces-r8`, `observability-surfaces-r2`, `audit-r11` or
   `observability-census-r1`.
4. Source rows S077–S084 and `lessons/round-23.md` land first (C-7); the note's
   header cites them only if that ordering holds.

Why this is the non-obvious move rather than a restatement of `DraftSourceRows` or
`ScoutPriorQuota`: those seats propose the rows and the FR2 replacement text. This
move uses two artifacts already inside the round — the frozen `/dev/shm` observation
and the corpus's `/scratch/tmp` precedent — to make the *boundary* mechanically
checkable, and it resolves the exit-2 collision by scoping M25 instead of silently
inheriting a code map that a later falsifier would call a violation. It also
deliberately keeps C1's calibration surface untouched, so the two claims stay
causally separable as the contract requires.

## 7. Risks

1. **Contract is frozen.** This move is documentation only. If L1 wants a
   single-meaning exit 2, that is a r24 contract change, not this wave; the ledger
   must not imply the code map changed.
2. **`/dev/shm` can be remounted.** Phrase it as observed at freeze
   (`frozen/c2-expected-real.json`, 2026-10-21); a later differing run is drift, not
   an oracle rewrite, and must not be used to edit the frozen file.
3. **Same-file contention with C1.** `DraftRenameDocs` also edits `SKILL.md` and
   README tables. One integration owner (L1) must sequence the C1 doc edits and the
   C2 note/pointers; concurrent edits to `SKILL.md:397-425` or `README.md:333` would
   create the exact stale-pointer class `audit-r11` F03/F04 records.
4. **Ledger as second source of truth.** The ledger must point at anchors, not restate
   kernel behavior; otherwise S083/S078 corrections would have to be mirrored, and
   the note would compete with the source rows.
5. **Overclaim by adjacency.** Adding a `quota` note next to the disk section invites
   "quota + burst both invisible to df" compression. They are two different blind
   spots (capacity vs quota; average vs burst) and `surfaces-r8.md:89-91` is explicit
   that the second is not solved.
6. **FR2 state drift.** Do not mark FR2 closed or change its F2 state; the remainder
   (limits/usage, NFS/overlay/fuse, ext superblock feature, races, EDQUOT
   attribution) stays Frontier, and D21 stays open.

## 8. Verification for L1 (I ran none)

1. Ordering: `git -C <lane> show <seal>:corpus/SOURCES.md | grep -c '^| S0'` ≥ 84 and
   `git cat-file -e <seal>:corpus/lessons/round-23.md` succeeds **before** the note
   cites S077–S084.
2. History untouched: `git diff --stat <base> <seal> -- corpus/knowledge/audit-r11.md
   corpus/knowledge/observability-surfaces-r2.md corpus/knowledge/surfaces-r8.md
   corpus/knowledge/observability-census-r1.md tools/mori-census.sh` → empty.
3. FR2 rows: `grep -n 'quota' corpus/README.md PROVINCE.md SKILL.md` shows the new
   pointer, the first-hand anchors, and the exact retained sentence "observe and
   report only, never change quota state"; no occurrence of "quota observability is"
   or "no quotas on the host".
4. Note contents: contains `visibly`/`visible enablement`, `/dev/shm`, `finding_id`,
   `df_covers_quota`; contains no `warn_pct`/`crit_pct`/`threshold` token outside a
   quoted prior-entry invariant; no claim that the r11 abort is attributed.
5. Registry: one `probe` row for `tools/mori-quota-surface.py`
   (ScoutCensusDisk §3 recommends the name `quota surface (r23)`); no new census
   SURFACE or FINDING id; `tools/mori-census.sh` bytes unchanged.
6. Measurement (L1's own): C1 oracle and C2 oracle runs are unaffected because no case
   reads a knowledge note; the real control remains 2/2 paths as frozen.
7. Pointer check: `git show 3da8414:tools/mori-census.sh | sed -n '88,94p'` still
   reads the PROPOSAL/EDQUOT block, so no "correction" is applied to
   `observability-surfaces-r2.md:259`.

## 9. Residual unknowns

- Whether L1 lands the note before or after C1's SKILL/README doc edits (sequencing,
  not substance).
- Whether the accepted source rows keep the drafted S077–S084 ids and tiers; if not,
  every citation in the note must be re-pointed before seal.
- Whether the implementation's `--selftest` writes any temp state (decides the
  registry row's `TMPDIR=` prefix; ScoutCensusDisk §5). This seat did not read the
  implementation.
- Whether FR2's F2 state word changes at all; the contract forbids promotion, and this
  report proposes narrowing only.

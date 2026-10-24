# ReviewSealManifest — round-23 seal/manifest recount and independence check

Seat: `MadoR22-2.ReviewSealManifest` (reviewer, wave-2 falsification, read-only).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Scope: recount the sealed dependency and case manifest hashes and the selected/rejected
decisions; confirm all independent source files/quotes match their final variants; confirm
no output-selected expectation. No edits, no execution of the tool, no fixture runs, no
scratch retained, no sibling/fleet writes.

Verified objects (all from committed bytes, read-only `git show/ls-tree/cat-file` plus
byte hashing of the working tree):

| item | value |
|---|---|
| production pin | `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` |
| seal | `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687` (`round-23: seal all oracle inputs before production implementation`) |
| implementation commit | `1979a9de4ef09eccad8cbbd24fd5c79404d9f8be` (strict descendant of seal) |
| entering revision | `1bfe708a170c877db3319060d0ab38771efe03ac` |
| seal manifest | `.ufo/waves/round-23/frozen/seal-manifest.json`, sha256 `8ff351f2dec6509d09865e827ffadb8341e522076ad88699ae433be07321c082` (identical at seal and at pin) |

---

## Verdict

**The seal manifest, the frozen case set, the C1 requirements/controls and the
independent source corpus are internally consistent and byte-stable; no output-selected
expectation was found. Two genuine seal-integrity gaps are reported below (F1, F2) — both
are *provenance/metadata* gaps in what the manifest claims to cover, not corrupted frozen
bytes. The frozen `CaseEscapedSpace` contradiction is confirmed as a real pre-existing
rule/expectation inconsistency and remains untouched.**

---

## Findings, by severity

### F1 — MEDIUM: the seal manifest does not hash the source corpus, the original
### proposals, or the corrected intermediates it depends on

`frozen/seal-manifest.json` `files[]` contains 43 entries: the two r22 dependencies, the
driver, `contract.md`, `preseal-amendment.md`, 5 C1/C2 frozen controls, `case-decisions.json`,
the 30 frozen quota cases, and the 2 oracles. It contains **zero** entries for
`evidence/sources/*` (the 10 raw source files), `evidence/sources-manifest.json`,
`evidence/source-quotes.json`, `evidence/source-accounting.json`,
`evidence/preseal-case-shapes.json`, `cases-proposed/*` (27 originals) or `cases-corrected/*`
(27 author bytes).

The amendment's own seal requirement is stricter than the manifest:

> "Seal all oracles, driver, original proposals, accepted/changed case files and decisions,
> dependencies (r22 builder/requirements) and manifests. Hash every frozen dependency."

So the original proposals and the changed case files are required to be sealed, and the
source corpus is the evidentiary base for every case `sources[]` citation and every Gate
quote. Only the *accepted* frozen copies are hashed; the *rejected/superseded* originals
and the independent source bytes are not.

Impact is bounded but real: the manifest's own `case-decisions.json` records
`original_sha256` and `selected_sha256` for all 30 decisions, so the original→selected
chain is independently re-derivable **from the ledger**, and the driver's `C08` check
proves every `frozen/**` path is byte-identical seal→revision. What the manifest does
**not** cover is: (a) the raw source bytes and the quote file, (b) the `cases-proposed/`
originals as files, (c) `cases-corrected/CaseSymlinkRealpath.json`, the *rejected*
intermediate. My independent recount closes (a) and (b) for the bytes themselves (below),
but it cannot close them **as a sealed artefact**: nothing in the committed manifest or in
the driver's `C08`/`C12` scope pins `evidence/sources/**` or `cases-proposed/**` at the
seal, so a later substitution of those bytes would not trip any seal check.

Byte-stability I did verify independently (all three revisions seal / pin / working tree,
SHA-256 equal, no drift):

* 27/27 `cases-proposed/*` — present at the seal, digest equals the ledger's
  `original_sha256` for all 27.
* 26/27 `cases-corrected/*` selected paths — present at the seal, digest equals the
  ledger's `selected_sha256`. **The 27th is F2 below.**
* `cases-corrected/CaseSymlinkRealpath.json` (rejected intermediate, sha
  `ef8eeaa03fa2576d8c9e666acfa4b3c38f765d4cde0b6ff1cacda26a78e7eefb`) — retained
  byte-preserved at the seal, as the ledger's `excluded_evidence` requires.
* `evidence/sources/*` (S077–S086, 10 files), `sources-manifest.json`,
  `source-quotes.json`, `source-accounting.json`, `preseal-case-shapes.json` — present at
  the seal, byte-identical at seal / pin / working tree, digests equal to
  `sources-manifest.json`.

### F2 — MEDIUM: `case-decisions.json` points `CaseTmpfsNoQuota` at a path that exists
### nowhere in the repository

`frozen/case-decisions.json:169-176` records for `CaseTmpfsNoQuota`:

```
"original":      "cases-proposed/CaseTmpfsNoQuota.json",   "original_sha256": "f4814c94…"
"selected":      "cases-corrected/CaseTmpfsNoQuota.json",  "selected_sha256": "7afd98c1…"
```

`cases-corrected/CaseTmpfsNoQuota.json` **does not exist** — not in the working tree, not
at the seal commit, not at the pin, and not in any of the 339 revisions in the repository
(I scanned every revision's tree for that blob). The `selected_sha256` `7afd98c1…` is
nonetheless correct: it equals the digest of the *frozen* file
`.ufo/waves/round-23/frozen/quota-cases/CaseTmpfsNoQuota.json`, which **is** in the seal
manifest and **is** what the oracle consumed. So the *bytes* are correct and pinned; only
the ledger's *path pointer* is dangling.

Consequences:

* The ledger claims "exact author bytes, no L1 expectation edits" for a case whose
  author-intermediate file is not retained anywhere. For the other 26 primaries the
  intermediate exists and can be diffed against the frozen copy; for this one it cannot.
* `evidence/preseal-case-shapes.json` (the shape ledger, 30 rows) does not cover
  `cases-corrected/CaseTmpfsNoQuota.json` at all — it lists 27 `cases-corrected/` rows, and
  the 27 it lists are 26 primaries **plus** `cases-corrected/CaseSymlinkRealpath.json`
  (the *rejected* intermediate, flagged `"issues": ["path mismatch"]`). The shape ledger's
  membership is therefore the 27 corrected paths *minus* `CaseTmpfsNoQuota` *plus* the
  rejected symlink file — it is not the same 27 as the ledger's selected set, and the
  pre-seal shape validation never covered the accepted `CaseTmpfsNoQuota` bytes.

I checked the frozen file's own content for a partial-verdict or self-inconsistency: the
fixture is well-formed (exact 5 top-level fixture keys; `btrfs_sysfs` record has the
amendment-required `qgroups`/`qgroups_enabled`/`qgroups_mode` members with
`qgroups:false` paired to `enabled:null`/`mode:null`), the six-field `expected` block has
the exact key set `{exit, finding_id, paths}` with the six compared path fields, and the
`expected` values are **byte-identical to the original proposal's** `expected` block
(only `fixture`, `scenario` and `rationale` changed). So the frozen case is sound and its
expectation is not output-selected; the defect is confined to the ledger pointer and the
shape-ledger membership.

### F3 — LOW: the frozen `CaseSymlinkRealpath` file name does not match the ledger's
### selected path

Ledger `:151-158` selects `cases-corrected/CaseSymlinkRealpath-final.json`
(sha `275c3605…`); the frozen copy is named
`frozen/quota-cases/CaseSymlinkRealpath.json` and carries the *same* digest `275c3605…`.
The digest mapping is therefore unambiguous and correct, but a reviewer joining the ledger
to the frozen directory by *filename* will not find `CaseSymlinkRealpath-final.json`.
Noting it because the sibling path `cases-corrected/CaseSymlinkRealpath.json` (digest
`ef8eeaa0…`, the rejected intermediate) is retained and could be mistaken for the accepted
one; the two digests differ and the manifest lists only the accepted bytes.

### F4 — LOW: the C2 primary/supplemental split is not reported by the pinned driver

`frozen/seal-manifest.json:229-232` asserts `primary_c2: 27`,
`source_review_supplemental_c2: 3`, `c1_original_requirements: 26`,
`supplementary_never_redefines_primary_denominator: true`. The pinned driver
(`measure-round23-v2.py`) has no primary/supplemental split for C2: its `c2` block carries
one flat 30-row denominator, and `C34` (`c2_after_every_case_matches`) is evaluated on
`pass == len(case_files)` over all 30. The oracle likewise folds the real-control row
into the same `counts` object (`oracle-quota.py:529-540`), so the 30-case and 31-row
(with real control) denominators are also mixed.

The split is not lost — it is reconstructible from pinned bytes: joining
`frozen/case-decisions.json` (`primary` flags) against
`evidence/measure4/c2-after-observed.json` (`results[].status` per case file) gives
**primary 26/27 pass (unmet: `CaseEscapedSpace`), supplemental 3/3 pass**, and the earlier
`evidence/frozen-contradiction.json` records exactly that split (26/27 and 3/3) for the
same contradiction. The requirement to keep the primary denominator separate is thus
*satisfiable* from committed bytes, but the pinned driver's own output does not state it.
Reporting it as a gap in the reporting surface, not in the data.

### F5 — LOW: source citations for two of ten rows are carried only by prose, not by any
### sealed case

All 30 frozen cases cite only S077–S084. **No case cites S085 or S086**, although both
are registered rows in `corpus/SOURCES.md:91-92` with digests `fd82c0db…` / `eb5d1e91…`,
appear in the lesson23 Gate with located quotes, and are named in the round-23
`source-accounting.json` `new_ids`. This is consistent with the round-23 design (S085/S086
were opened as coverage-gap closers, cited by the lesson/knowledge prose rather than by a
case), so it is not a defect — but it does mean no sealed expectation is backed by those
two rows, and a reader checking "does every source row back a sealed case" will find two
that back none.

### F6 — LOW: three post-seal source files sit beside the sealed corpus

`.ufo/waves/round-23/evidence/sources/S087-fs_ext4_super.c`,
`S088-include_linux_quotaops.h` and `S089-fs_quota_dquot.c` (mtime 15:38, after the
15:10:59 seal) are untracked (`git status` → `??`) and appear in **no** sealed artefact:
not in the seal manifest's `files[]`, not at the seal commit, not in
`evidence/sources-manifest.json`, `source-quotes.json` or `source-accounting.json` (all
three of which stop at S086 with `after_rows: 86`, `new_ids: S077–S086`).

They are now described by two further **untracked** wave-2 files,
`evidence/post-falsification-sources.json` and `evidence/post-falsification-quotes.json`,
each row carrying `"stage": "post-falsification source correction, no sealed target
change"`, and `evidence/count-lineage.json` lists them under
`post_falsification.new_sources_opened_not_yet_registered: ["S087","S088","S089"]`. So
they are deliberately *outside* the sealed source accounting, and the untracked evidence
that describes them is itself outside the seal.

Recording it because the "source corpus == sealed manifest" invariant must be stated
precisely: the **sealed** corpus is 10 files (S077–S086) and the sealed registry is
86 rows; the corpus directory currently holds 13 files, three of which are post-seal,
unregistered and uncommitted. Any later count taken from the directory rather than from
`sources-manifest.json` will read 13, and the three extra files are not covered by any
seal or driver check.

---

## Recounts that passed (no finding)

**A. Seal manifest hashes — 43/43 exact, three ways.**
For every one of the 43 `files[]` entries I recomputed SHA-256 and byte length from the
working tree and from the seal commit's blob: **all 43 match** the manifest on both
(count, digest, length). Cross-checked against the driver's independent
`frozen_dependency_digests` in `evidence/measure4/summary.json` (46 entries: the 43
manifest paths plus `seal-manifest.json`, `tools/mori-quota-surface.py`,
`tools/mori-retention-reconcile.py`): **zero digest disagreements**.
The manifest's own digest is `8ff351f2…` at the seal and at the pin.
Every manifest path is byte-identical across all four post-seal revisions
(`1979a9d` → `56ac3ba` → `f3dc07c0` → `6eb889c`): **no drift**.

**B. Case manifest ↔ ledger ↔ oracle — consistent.**
`frozen/quota-cases/` contains exactly 30 files; the manifest lists exactly those 30
quota-case paths (symmetric difference empty). `frozen/case-decisions.json` holds 30
decisions = 27 `primary: true` + 3 `primary: false`, matching the manifest's
`primary_c2: 27` / `source_review_supplemental_c2: 3` and the 27-proposals / 27-corrected
/ 3-supplemental directories committed at the seal. All 30 `selected_sha256` values equal
the corresponding frozen file's manifest digest, and the 30 case digests the oracle
actually consumed (`evidence/measure4/c2-after-observed.json` `cases[].sha256`) equal the
manifest digests; the oracle's `cases_sha256_combined` `3323f4246ee637dd030138db…`
recomputes exactly from the sorted per-case list.

**C. Seal ordering and production absence — verified independently.**
`merge-base --is-ancestor 22772c1 1979a9d` → 0 and `… 22772c1 f3dc07c0` → 0; seal ≠
revision. `git ls-tree -r 22772c1` contains **no** `tools/mori-quota-surface.py` and no
`build/ImplQuota/*.py` (only the `ImplQuota.md` seat report — the candidate *bytes* are
absent at the seal, as the manifest's `candidate_bytes_not_opened_by_L1_before_seal`
claims, modulo the manifest's own honest caveat that commit ordering proves ordering
only). The reconciler at the seal is byte-identical to the entering revision
(`0795bac9367c33e534b79599114c1635d83c4b0e4a57fbbe235644858a59de32`); the `tools/`
delta seal→revision is exactly `M tools/mori-retention-reconcile.py` +
`A tools/mori-quota-surface.py`. Commit timestamps are ordered
(`4dc80c1` 14:00:53 → `c1e8b81` 15:01:27 → seal `22772c1` 15:10:59 → impl `1979a9d`
15:15:15 → `5729e7f` 15:18:40 → `56ac3ba` 15:23:46 → `f3dc07c0` 15:25:42 →
`6eb889c` 15:30:09), and the seal is an ancestor of every later revision.

**D. Independent sources and quotes — 10/10 match their final variants.**
Every file in `evidence/sources/` for S077–S086 matches `evidence/sources-manifest.json`
on SHA-256 **and** byte count, and is byte-identical at seal / pin / working tree. All ten
`evidence/source-quotes.json` entries: `source_sha256` equals the manifest digest,
`found_in_whitespace_normalized_source: true` reproduces (whitespace-normalised search of
the actual source bytes finds each quote), and each `word_count` equals the quote's own
whitespace token count. Each of the ten lesson23 Gate rows resolves to exactly the quoted
text at the cited line range in the pinned source bytes (S077 171–173, S078 253–254,
S079 2363, S080 444, S081 8246, S082 1985, S083 262, S084 132–134, S085 172,
S086 4878–4879). `corpus/SOURCES.md` holds 86 unique rows S001–S086 with no gaps and no
duplicates, and every S077–S086 row carries the manifest's 16-hex digest prefix.
The ten quotes appear verbatim in `corpus/lessons/round-23.md` (the Gate) and are
*not* duplicated in `corpus/knowledge/quota-surface-r23.md`, which cites the rows by id —
the lesson is the quotation carrier, so this is the intended split, not a mismatch.
`corpus/knowledge/quota-surface-r23.md` gained its "Final pre-seal mode safety
qualification" section at the seal commit, i.e. before the implementation, and the
S085/S086 registry rows and the lesson Gate were in place at `c1e8b81` (15:01:27), before
the seal — matching the amendment's "registry and lesson Gate land before sourced
knowledge admission".

**E. No output-selected expectation — checked and consistent with the sealed rule text.**
The seal is a strict ancestor of the implementation, and all 30 frozen cases are
byte-identical seal→pin→working tree, so no case was edited after the implementation
existed. The five cases whose `expected` block changed relative to their own proposal
(`CaseBtrfsQgroup`, `CaseBtrfsSquota`, `CaseExt4Journaled`, `CaseExt4Usrquota`,
`CaseStacked`) each changed *toward* the amendment's superseding rules
(`btrfs_qgroups_dir_present`→`btrfs_qgroups_enabled`; `ext_quota_option`→
`ext_quota_option_unverified` + exit 1→2; `tmpfs_quota_option`→`ambiguous_overmount`),
and every one of those rule texts is present in `preseal-amendment.md` **at the seal**
and, for the parent-ID clause, already at `c1e8b81` (15:01:27, before the seal) — so the
change direction is rule-derived, not output-derived. The remaining 25 cases keep their
proposal's `expected` bytes exactly. No case `rationale` cites a measured result, a
candidate output or a sibling expectation; the "measured"/"observed" hits I found are
only the standard pre-registration disclaimers ("written before any candidate was opened
or measured", "not claimed to reproduce any observed host mount").

**F. C1 requirements/controls and the source-delta guard — verified.**
`frozen/c1-requirements.json` lists R01–R26 and pins `contract_sha256`,
`fixture_builder_sha256`, `oracle_sha256`, `r22_requirements_v2_sha256`; all four equal
the seal and pin digests of those files, and the driver's `C11` agrees.
`oracle-rename.py`'s R02/R11/R12 differ from the r22 oracle-reconcile-v2 predicates by
exactly the pre-registered field substitution `raw_unallowlisted`→`scanner_unallowlisted`
(R02, R11, R12 only; R01, R03–R10, R13–R24 byte-identical in predicate form), and R25/R26
are new as registered. `frozen/c1-source-delta.json` reproduces exactly: starting from the
entering blob `0795bac9…` and applying only the two registered replacements yields
`4599ee1a…`, which is the production reconciler at the pin — **I recomputed the transform
independently and it matches byte-for-byte**, with the `'raw_unallowlisted':len(unallowed),`
fragment occurring exactly once in the entering source (so the deletion is unambiguous) and
`SCHEMA='mori-retention-reconciliation-v1'` occurring exactly once.
`frozen/c1-expected-real.json` is the r22 `expected-real.json` with the registered rename
only: every shared value is identical (allowlisted 86, exclusion_basis
`non_author_paths_glob`, finding_id `RETENTION_RECONCILED`, forbidden_allowlist 0,
non_author 5, policy_excluded 5, privacy_clearance false, raw_total 95, receipt_match true,
retention_state red, scanner_total 90, scanner_unallowlisted 4), plus the two registered
additions (`raw_not_allowlisted` 9 = 95 − 86, `schema` v2) and `forbidden_keys:
["raw_unallowlisted"]`. The referenced r21 receipt `77a5bbe8…` and measured revision
`9fb1f911…` both resolve to real commits.

**G. The `CaseEscapedSpace` contradiction — confirmed, unchanged, correctly recorded.**
I re-derived the contradiction from the frozen bytes alone: the fixture's mountinfo has
mount 43 (`/srv/my\040data`, parent 33) over mount 42 (`/srv`, parent 33); 33 is present
in the snapshot but is not the id of the longest strictly-shorter covering mount, so the
sealed parent-ID rule (present in `preseal-amendment.md` at the seal, and already at
`c1e8b81`) requires `unknown` / `n/a` / `ambiguous_overmount` with null fstype and
mount_point. The frozen `expected` row instead says `enabled` / `enforced` /
`xfs_quota_option` at exit 1 `QUOTA_ENABLED` — hence the measured
`frozen-contradiction.json` "actual" block and the `29/30` headline. Notably the frozen
case's own `rationale` enumerates three amendment deltas and asserts each "does not touch
this case", and never mentions the parent-ID clause: the frozen expectation was authored
without that clause, which is consistent with an authoring/verification gap *before* the
implementation rather than an output-selected edit. The frozen case bytes are unchanged
from the seal, and the contradiction is retained in
`evidence/frozen-contradiction.json` and `evidence/parent-strict-target-disposition.txt`
exactly as Main ruled. I make no proposal to alter, exclude or relabel it.

**H. C1 measurement, C2 measurement and the quota selftest — as recorded, not re-run.**
From the pinned receipts (I did not re-execute the driver, the tool or the selftest):
`evidence/measure4/summary.json` records `before.c1_original_26 = 25/26 (unmet 1, alias
runs 8)`, `after.c1_original_26 = 26/26 (unmet 0, alias runs 0)` — the `8` being the
count of alias-bearing *check outputs among 18 parsed oracle runs*, not 8 of 26
requirements, and `R25` the only requirement that flips (the untracked
`evidence/count-lineage.json` states this same basis, and I confirmed it against
`evidence/measure4/c1-oracle-before.json` / `c1-oracle-after.json`:
`misleading_alias_runs` 8 → 0, `parsed_runs` 18 on both arms, `only_flipped_requirement`
R25) — `c1_supplementary.pass =
true` with 5 supplementary guards reported apart from the 26, `c1_real_control.match =
true` with all 19 observed keys matching and the three identity digests matching, and
`c2.after = 29/30`. The two red driver checks are `C34.c2_after_every_case_matches`
(the 29/30 headline — the sealed strict red) and `C30.c2_oracle_real_control_agrees`.
The C2 *real control itself passed* (`C29` green; the oracle's own `real_control` row
`status: "pass"`, `exit_match/finding_match/paths_match` all true) — C30 fails only
because the oracle appends the real-control row into the same 30-row `counts` object, so
the single unmet *case* leaks into the real-control aggregate. That is a reporting
coupling in the oracle, not a real-control failure, and it is already visible in
`evidence/measure4/c2-after-real-observed.json` (counts `{pass 30, total 31, unmet 1}`
with `real_control.status = "pass"`). The quota selftest's separate 49/49 arm count is
recorded in `evidence/quota-selftest-corrected.json` and is a co-evolved public selftest,
distinct from the frozen `CaseEscapedSpace`; I did not conflate them.

---

## Residual risk / verification gaps

1. **Commit ordering is the only ordering evidence.** The seal manifest itself concedes
   this ("Blind executor drafts existed concurrently before seal; this proves commit
   ordering only, not absolute private chronology or non-author adjudication"). My
   independence argument for the 30 frozen cases rests on (a) commit ancestry and
   timestamps, (b) byte-identity of the frozen cases across seal→pin→worktree, and (c)
   the fact that every `expected` change is rule-text-derived from a pre-seal document.
   Absolute private chronology of the wave-1 case authors is not provable from committed
   bytes, and I do not claim it.
2. **`frozen/c1-expected-real-identities.json` is explicitly a "co-evolved
   transcription … not historical execution authentication"** of the retained receipt
   identities. The three identity digests are reproduced by the driver's own
   `C35.c1_real_identity_pins` check against the freshly observed population, so the
   digests are re-derived, not trusted — but the *transcription* of the receipt's identity
   set is not a replay of the original r21 execution.
3. **The C2 real-control aggregate is coupled to the case aggregate** (F4/H). A reader of
   `after_with_real_expected = {pass 30, total 31, unmet 1}` alone cannot tell that the
   real control passed and one case failed. The per-row receipts do show it.
4. **The r22 claim is not re-reproduced here.** The r23 driver states the r22 driver runs
   its checkout's tool, so the r22 claim is reproducible only in a checkout of
   `da40bb2…`; the r23 oracle re-expresses the 24 r22 predicates and pins the r22
   builder/requirements by digest only. I confirmed the digest pinning and the predicate
   equivalence; I did not replay r22.
5. **Two of ten registered source rows (S085, S086) back no sealed case** (F5), and three
   further uncommitted source files sit in the corpus directory (F6). Neither touches a
   frozen byte.

## What I did not do

No production, frozen, oracle, contract, corpus or case byte was modified. No fixture,
mutation, pinned-driver or quota-tool invocation was performed (I read only committed
bytes and recomputed hashes over them). No scratch, clone or background job was created
(`/fast/scratch/hyaku/mori-r23/ReviewSealManifest/` was created and removed unused). No
package was installed or updated. No transcript, session, credential or `agent.db` access.
No fleet-root or sibling-lane write; the only file written is this report.

## Tooling

No tool, package or version was installed, updated or removed by this seat; the review ran
on the lane's existing `git` and Python 3 only, and the host-wide pacman pause was left
untouched.

# ReviewShonen — four canonical SHONEN subjects, round 23

Seat: `MadoR22-2.ReviewShonen` (read-only falsification seat, wave 23).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Scope of this report: assess the **four canonical SHONEN subjects** of this lane
(`SHONEN.md:5-8`) against the round-23 production revision, with evidence, and
give **author-lane advice only**.

## Authority and non-claims (read first)

- I am an author-lane adviser inside a dispatched wave seat. This is **not** the
  outside non-author SHONEN verification required by `corpus/knowledge/audit-r11.md:215`
  (D20) and `corpus/lessons/round-23.md` (Reject list: "author advisers are a fresh
  non-author spot-check"). It is **not** a promotion, an admission, a clearance, a
  baseline acceptance, a privacy clearance, or a rank change.
- No `SHONEN.md` box was touched and no promotion/box/rank edit is made or proposed
  as an action by me. `SHONEN.md` is byte-unchanged (verified: `git diff --stat
  1bfe708… f3dc07c… -- PROVINCE.md SHONEN.md` → 0 lines; 0 commits in that range
  touch either file).
- No edits were made anywhere. Only this report file was written.
- No live host reads were performed: no quota command, no `quotactl`/`btrfs`/
  `xfs_quota`/`repquota`/`mount`, no journalctl, no process/service probe, no
  credential/agent.db/transcript read. Every number below is read from a retained
  committed receipt; I did not re-derive any of them.
- Semantic caller/reference checking: **no `lsp` device is mounted in this
  environment** (`xd://lsp` → "No such tool") and no Python LSP server binary is
  installed (`pyright`/`pylsp`/`python-lsp-server` absent). Caller checks therefore
  fall back to literal grep over `tools/`, `corpus/`, `SKILL.md`, `LOG.md`,
  `PROVINCE.md` — recorded here as a **fallback, not semantic proof**.

## Axes named

| Axis | Question |
|---|---|
| A1 box-1 conformance | Does `SKILL.md` really carry decision tables, error patterns, checklists, cited sources — including for the r23 capability? |
| A2 box-2 execution | Was an end-to-end domain task actually executed and logged, with exercised receipts? |
| A3 box-3 executability | Can a fresh agent execute the r23 instructions with no oral context, from stable lane docs only? |
| A4 box-4 province | Is `PROVINCE.md` still accurate and complete for the new read surface (no cross-domain bleed)? |
| A5 honesty | Does any statement risk converting the expected strict red (29/30) or the co-evolved selftest (49/49) into a pass claim? |

## The four subjects, assessed

Recommendation tokens are for the parent's r23 report `## SHONEN` section
(`PROTOCOL.md:174-190` requires the heading plus **one** `[x]`/`[ ]`/`[~]` line per
box; the r22 filed shape is `…/.ufo/reports/round-22/mori.md:56-61`, four `[~]`
lines with pointers). All four are recommended **`[~]`**, with the F-findings
below as the concrete work that would raise them.

### Box 1 — SKILL.md contains real decision tables, error patterns, checklists, cited sources → `[~]`

Evidence:
- Structural substrate pre-exists and is intact: decision table `SKILL.md:11-22`,
  error patterns `SKILL.md:23-46`, executable checklist `SKILL.md:149-153`,
  gate registry `SKILL.md:156+`.
- r23 additions are real and cited: registry rows at `SKILL.md:585` (retention
  reconciliation schema-v2) and `SKILL.md:586` (quota surface probe), each with
  entry command, verdict map, self-test command, pinned values, write scope, owner;
  prose at `SKILL.md:566-584` and `SKILL.md:588-605`; knowledge pointer
  `SKILL.md:588` → `corpus/knowledge/quota-surface-r23.md`.
- Source citations are primary, pinned and digested: `corpus/SOURCES.md` rows
  S077–S086 (Linux v7.2 xfs.rst / xfs_super.c / sysfs.c / qgroup.c / inode.c /
  proc.rst / ext4.rst / tmpfs.rst / proc_namespace.c / shmem.c), each with URL,
  location, tag and sha256; the Gate table with ≤25-word located quotes is at
  `corpus/lessons/round-23.md:34-52`; the decision table keyed to those sources is
  at `corpus/knowledge/quota-surface-r23.md:30-56`.
- The r22 knowledge note was cut over as required: `corpus/knowledge/retention-reconciliation-r22.md`
  now carries "Round23 API correction — schema-v2 clean cutover" (removed key,
  canonical names, absolute `--repo "$PWD"`, r22-oracles-only-at-bound-checkout).

Gaps (see F2, F3, F5, F9): the r23 intent row and its error patterns live in the
knowledge note, **not** in `SKILL.md`'s own decision/error tables; the fixture input
contract is undocumented in stable docs; the shipped tool's own header still calls
itself a candidate; and one selected C2 case's author-side file is missing from
the tree even though the frozen bytes it was measured against are intact and
hash-identical to the recorded selection (F9).

### Box 2 — At least one end-to-end domain task executed and logged in LOG.md → `[~]`

Evidence (exercised, revision-bound, logged):
- `LOG.md:1522-1680` — seven round-23 entries: pre-registered declaration
  (`:1522`), source corrections (`:1537`), expectation seal (`:1564`), production
  integration after the seal (`:1592`), first measurement defect (`:1612`),
  frozen contradiction (`:1627`), delivered guards + separate selftest correction
  (`:1647`), stable guard results + falsification payload (`:1665`).
- End-to-end real-mode domain task (the new probe on the live host, default pair):
  `…/evidence/measure4/c2-real-control.json` → exit 0 `QUOTA_DISABLED`;
  `/home/vgpnk/Projects/shokunin` → btrfs, mount `/home`, disabled,
  `btrfs_qgroups_dir_absent`, `device_check: btrfs_subvolume_skipped`;
  `/tmp` → xfs, `/tmp`, disabled, `xfs_noquota_option`, `device_check: match`; the
  driver summary records `c2.real_control.match: true`
  (`…/evidence/measure4/summary.json`).
- Second end-to-end task (the reconciler on the retained r21 control):
  `…/evidence/measure4/c1-real-control.json` → `match: true`, schema
  `mori-retention-reconciliation-v2`, `forbidden_keys_present: []`,
  `scanner_unallowlisted` 4, `raw_not_allowlisted` 9, `raw_total` 95,
  `allowlisted` 86, `policy_excluded` 5, `non_author` 5, `retention_state` red,
  `privacy_clearance` false, identity pins and receipt pin matched.
- C1 result as logged: original 25/26 → 26/26, alias-bearing runs 8 → 0, oracle
  before exit 1 / after exit 0 (`…/evidence/measure4/summary.json` → `c1_original_26`;
  `…/evidence/measure4/c1-oracle-after.json` → `pass 26/26`, `misleading_alias_runs 0`).
- C2 result as logged: **29/30** (before: 30 × `capability_absent`), the single red
  being frozen `CaseEscapedSpace`; the full driver exit is 1 and this is recorded as
  expected (`…/evidence/measure4-invocation.json` → `exit 1`,
  `all_claim_checks_pass: false`; `…/evidence/frozen-contradiction.json`).
- The public quota selftest passes 49/49 exit 0
  (`…/evidence/quota-selftest-corrected.json`, measured at `f3dc07c…`).

Honesty constraint for the report author (A5): the 49/49 selftest is the
**co-evolved** selftest arm set and is **not** the frozen `CaseEscapedSpace`
(`corpus/lessons/round-23.md` "Scope and remaining debt"). The r23 strict C2 target
stays **unprovable at 29/30**; `LOG.md:1665-1674` already states "These are
exercised results, not strict C2 admission". The parent's `## SHONEN` box-2 line
must not let "a task was executed and logged" imply the C2 target passed.

Second honesty constraint (F9): `LOG.md:1671-1672` says "no frozen oracle
or expected file was changed". That statement holds for the frozen bytes I verified
(blob `5fee17da…` = recorded `selected_sha256` `7afd98c1…`, sealed pre-production).
What does **not** hold as a blanket claim is "every selected case's author file is
retained at its recorded path" — for `CaseTmpfsNoQuota` that path
(`cases-corrected/CaseTmpfsNoQuota.json`) does not exist at the seal, and the
disclosure receipt is `…/evidence/tmpfs-source-provenance-erratum.json`. Disclose
the gap; do not rewrite the frozen decisions file.

### Box 3 — Instructions executable by an agent without oral context → `[~]`

Evidence:
- `SKILL.md:585` gives the exact v2 reconciler invocation with `--repo "$PWD"`,
  verdict map (0/1/2 with finding ids), the self-test invocation, the pinned
  frozen artifacts and the write scope; `SKILL.md:566-576` states the key removal
  and the two canonical names, and that r22 oracles/real/refinement checks that
  name the old key reproduce only at their bound checkout.
- `SKILL.md:586` gives the quota entry (`python3 tools/mori-quota-surface.py`,
  defaults fleet root + `/tmp`, repeated `--path ABS` only for operator-pinned
  runway targets), the verdict map (0/1/2), the self-test invocation, and the
  write scope ("stdout only; kernel mountinfo/stat/realpath and named btrfs sysfs
  reads; no configuration/commands/ioctls/writes").
- Vocabulary is written down where an agent will look: exit codes and finding ids
  `corpus/knowledge/quota-surface-r23.md:73-86`; ownership fence
  `corpus/knowledge/quota-surface-r23.md:87-97`; `corpus/knowledge/retention-reconciliation-r22.md`
  (Round23 correction section) for the schema-v2 API.

Gaps (F2, F3, F4, F8): the `--fixture` document schema is undocumented outside the
wave-scoped contract; the shipped tool's header self-identifies as a candidate and
points at sibling files that are not next to it; `SKILL.md:411-413` still asserts
the quota numbers are unreadable on this host; and the scratch guidance in the r23
note is round-pinned to a `mori-r23` path while older registry rows say
`TMPDIR=<lane>/.scratch`.

### Box 4 — No cross-domain bleed (PROVINCE.md still accurate) → `[~]`

Evidence:
- **No bleed observed.** The new probe reads only kernel-visible state:
  `/proc/self/mountinfo`, `os.stat(path).st_dev`, `os.path.realpath(path)`, and the
  named btrfs sysfs `qgroups/enabled` attribute (`tools/mori-quota-surface.py:66-76`).
  It never calls `quotactl`, `btrfs qgroup`, `xfs_quota`, `repquota`,
  mounts, writes or any privileged interface (`tools/mori-quota-surface.py:56-60`),
  reads no credential/token/session material, and emits no mount source,
  option value or UUID (`tools/mori-quota-surface.py:92-96`).
- Configuration, cause and remediation are explicitly routed away from mori:
  `SKILL.md:601-604` and `corpus/knowledge/quota-surface-r23.md:87-97`
  ("Configuration, why a mechanism is on/off, and remediation route to
  tsukuroi/operator"). `PROVINCE.md:12-16` (Refuses) and the tsukuroi adjacency row
  `PROVINCE.md:66` are consistent with that fence.
- The probe is separate from the census; no census cutover, no baseline re-pin
  (`corpus/lessons/round-23.md` "Scope and remaining debt"; `…/evidence/measure4/summary.json`
  → `carried_open_debt` unchanged: 4 unallowlisted hits, permission RED 11/12,
  two unknown dispositions, baseline acceptance blocked, `privacy_clearance: false`).

Gap (F1): `PROVINCE.md` is byte-unchanged this round, so it is *not wrong* but it
is **incomplete** — it does not record the new read surface, and FR2
(`PROVINCE.md:45`) still reads as pure Frontier.

## Findings by severity

**F1 — MEDIUM/HIGH (box 4, scope disclosure; doc-freshness).** `PROVINCE.md` was not
updated in round 23 (0-line diff and 0 commits across `1bfe708…f3dc07c…`). The lane
now ships `tools/mori-quota-surface.py` with a **new host read surface**
(`/proc/self/mountinfo`, `stat`/`realpath`, `/sys/fs/btrfs/<uuid>/qgroups/enabled`),
but `PROVINCE.md:6-11` ("Owns (read-only probes)") and the Core list (`:20-41`) do
not mention it and FR2 (`:45`) still reads as an untouched frontier item. The lane's
own convention is to append a scope note per new capability (r17 `:96`, r18
`:123`, r20 `:143`, r21 `:162`, r22 `:197`). *Advice:* append a "Round23 appended
scope notes" section naming the probe, its exact read set, the ownership fence
(configuration/causes/remediation → tsukuroi/operator), and that FR2 remains
frontier (mechanism visibility only — no limits, usage, exhaustion cause or census
integration). This is disclosure, not a scope change.

**F2 — MEDIUM (box 3, executability).** The `--fixture` input contract is not in any
stable lane document. `SKILL.md:586` mentions "fixture-mode actual CLI" without a
schema; `corpus/knowledge/quota-surface-r23.md` documents the decision table and
exit vocabulary but not the fixture document; `tools/mori-quota-surface.py:66-120`
documents the flag but not the document shape. The shape lives in wave-scoped files
(`contract.md:82-93` plus `preseal-amendment.md`) and is implemented at
`tools/mori-quota-surface.py:166-190` (`FIXTURE_KEYS`, `PATH_KEYS`, `UUID_KEYS`).
Critically, the amended UUID record requires a **`qgroups_enabled`** member that
the original contract example does not contain, so `mori-quota-fixture-v1` now
denotes two different shapes — the exact ambiguity flagged pre-seal by case authors
(`.ufo/waves/round-23/build/CaseBtrfsDevMatch.md:305-309`,
`build/CaseBtrfsTwoUuids.md:278-284`). *Advice:* state the amended shape in
`corpus/knowledge/quota-surface-r23.md` (exact key sets, the required
`qgroups_enabled`, the `qgroup`/`squota`-only mode projection) and note that the
original-shape proposals are retained history, not loadable inputs.

**F3 — MEDIUM (box 1/box 3, shipped-source accuracy).** The shipped tool's module
docstring still reads as a candidate: `tools/mori-quota-surface.py:2-8` —
"mori-quota-surface-v3.py — … This is the round-23 pre-seal amendment candidate for
contract §C2 … authored alongside `mori-quota-surface.py` (the original, unaltered)
and `mori-quota-surface-v2.py` (preserved as the rejected unsafe-read source
evidence)". The shipped file **is** `tools/mori-quota-surface.py`; the two referenced
siblings exist only under `.ufo/waves/round-23/build/ImplQuota/`. An agent reading
the shipped header is told it is reading a candidate and is pointed at files that
are not next to it. *Advice:* retitle the docstring to the shipped name and demote
the v1→v3 history to a "History" paragraph naming the retained wave paths.

**F4 — MEDIUM (box 1/box 3, stale statement).** `SKILL.md:411-413` still states
that for the fleet's reported EDQUOT failures "the quota numbers are unreadable on
this host". After r23 that is true only for per-ID limits/usage, not for visible
mechanism state. `SKILL.md:598-600` flags the line as "dated historical evidence"
but leaves the sentence in place. *Advice:* amend the line to distinguish
limits/usage (still unreadable) from mechanism visibility (now observable via
`tools/mori-quota-surface.py`, which is not a limit, breach or exhaustion verdict).

**F5 — LOW/MEDIUM (box 1).** `SKILL.md`'s own decision table (`:11-22`) and error
patterns (`:23-46`) were not extended with the r23 intent or its error patterns;
the quota decision table lives in `corpus/knowledge/quota-surface-r23.md:30-56` and
the exit vocabulary at `:73-86`. A fresh agent scanning only `SKILL.md`'s decision
table finds no "is a quota mechanism visibly enabled on our runway?" intent and no
`QUOTA_STATE_UNKNOWN` vs `QUOTA_SETUP` reading. *Advice:* one decision-table row
and one error-pattern row in `SKILL.md`, pointing to the knowledge note.

**F6 — LOW (hygiene).** Untracked bytecode artifacts sit in the tools tree:
`?? tools/__pycache__/` (`mori-quota-surface.cpython-314.pyc`), plus
`?? .ufo/waves/round-22/frozen/__pycache__/` and `?? .ufo/waves/round-23/__pycache__/`
(`git status --porcelain`). Nothing is tracked or committed, so there is no commit
risk, but the lane's "only named paths are committed" story reads cleaner without
three stray `__pycache__` trees, and the r23 report's `git status` receipt will
otherwise show them next to the intentional `?? .scratch/`.

**F7 — LOW (round-scoped guidance).** `SKILL.md:580-581` pins new heavy scratch to
`/fast/scratch/hyaku/mori-r23` (this round's operator root) while older registry
rows prescribe `TMPDIR=<lane>/.scratch`. *Advice:* state the general rule
(private lane scratch, never `/tmp` fallback) and mark the `mori-r23` path as this
round's operator-pinned root so a later round does not follow a stale absolute path.

**F8 — INFORMATIONAL (not a defect; do not act).** The C2 independent expectations
live under the wave-scoped `.ufo/waves/round-23/frozen/quota-cases/` while the
capability lives in `tools/`. A future round re-verifying C2 must not re-author
those expectations; the frozen bytes and the contradiction record remain the
authority (`…/evidence/frozen-contradiction.json`).

**F9 — MEDIUM (box 1/box 2, provenance; independently verified by me, not relayed
on trust).** One selected C2 case's *author-side* file is gone while the frozen
bytes it was measured against are intact. `frozen/case-decisions.json` records
`CaseTmpfsNoQuota`: original `cases-proposed/CaseTmpfsNoQuota.json`
(`original_sha256` `f4814c94…`), selected `cases-corrected/CaseTmpfsNoQuota.json`
(`selected_sha256` `7afd98c1…`). Verified with read-only git at the seal
`22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`:
- `git ls-tree <seal> .ufo/waves/round-23/cases-corrected/` lists only
  `CaseTmpfsHardlimit.json` and `CaseTmpfsUsrquota.json` — the recorded **selected
  path does not exist at the seal**;
- `git cat-file blob` of the sealed `frozen/quota-cases/CaseTmpfsNoQuota.json`
  (blob `5fee17da…`) hashes to `7afd98c1…` = the recorded `selected_sha256`, and
  the sealed `cases-proposed/CaseTmpfsNoQuota.json` (blob `e07dd367…`) hashes to
  `f4814c94…` = the recorded `original_sha256`.

So the bytes the oracle measured are exactly the recorded selection (no byte
tampering, no post-seal rewrite of expected values), but the chain "selected file
is retained and inspectable at the recorded path" is broken for this one case; the
sibling receipt `…/evidence/tmpfs-source-provenance-erratum.json` says the author
deleted the draft after L1 copied it, and instructs that the missing intermediary
be disclosed and `frozen/case-decisions.json` not be rewritten. *Advice:* the
r23 report must not write "all frozen case bytes and their author files are
unchanged and retained" as a blanket claim; say the frozen bytes and expected
values are unchanged and sealed pre-production, and disclose the one missing
author-side path (F9), keeping the erratum as the receipt. This also guards box 3:
an agent re-verifying the C2 case set will find that path absent and must not
conclude tampering.

## Residual risk and verification gaps

1. **Nothing here was re-executed.** No driver, oracle, selftest or live probe was
   run by me. All cited numbers are read from retained committed receipts under
   `…/.ufo/waves/round-23/evidence/`; I did not re-derive them, and their
   authenticity beyond the retained digests is not re-verified by this seat.
2. **The strict C2 target remains unprovable at 29/30.** The failing driver checks
   are `C34.c2_after_every_case_matches` (29/30) and `C30.c2_oracle_real_control_agrees`
   (the `--real-expected` oracle aggregate exits 1 on the same single red); the C2
   **real control itself matched** (`summary.json` → `c2.real_control.match: true`).
   The frozen `CaseEscapedSpace` rule and its independently authored expected row
   remain contradictory, both unchanged, and un-admitted by me. No special-casing,
   exclusion, relabel or expectation rewrite was found in production: the tool
   refuses `ambiguous_overmount` exactly as the sealed rule demands
   (`…/evidence/frozen-contradiction.json` → `actual`).
3. **Box 3 depends on stable-doc coverage, not on the tool.** The probe's own
   docstring is the only complete description of the fixture document; if the
   wave directory is pruned, F2 becomes unrecoverable from stable docs.
4. **Box 4 is an absence-of-bleed judgement on a read set I did not execute.** It
   rests on the shipped source and the retained receipts, not on a live trace.
5. **No outside/non-author adjudication.** Whether any box is `[x]` is not mine to
   decide; the operator owns promotion, and the four boxes remain untouched
   (`SHONEN.md:5-8` unchanged).
6. **The source base is moving under me.** At the pinned production revision
   `f3dc07c…` the committed source rows are S077–S086 (what I assessed). Concurrent
   falsification seats added **uncommitted** source evidence after my read —
   `…/evidence/sources/S087-fs_ext4_super.c`, `S088-include_linux_quotaops.h`,
   `S089-fs_quota_dquot.c`, plus `…/evidence/post-falsification-sources.json` —
   which is relevant to the same quota/ext domain. My box-1 source-coverage
   assessment is therefore bounded to the committed rows at `f3dc07c…`; if those
   rows are admitted and cited, box 1's citation density improves and the F5/F2
   gaps remain unchanged.
7. **One provenance gap is now on the record (F9)** and is disclosed in a sibling
   receipt rather than hidden; it concerns a missing author-side *path*, not a
   changed byte.

## Suggested `## SHONEN` lines for the parent's r23 report (author-lane advice, not a promotion)

- `- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — SKILL.md:566-605 (registry rows :585, :586), knowledge note corpus/knowledge/quota-surface-r23.md:30-56, sources S077-S086 with digests (corpus/SOURCES.md; corpus/lessons/round-23.md:34-52); open: r23 intent/error rows not yet in SKILL.md's own tables (F5), fixture contract undocumented (F2), shipped docstring still reads as a candidate (F3), one selected case's author-side path missing with frozen bytes intact (F9)`
- `- [~] At least one end-to-end domain task executed and logged in LOG.md — LOG.md:1522-1680; exercised receipts: evidence/measure4/c2-real-control.json (exit 0 QUOTA_DISABLED, btrfs /home disabled, xfs /tmp disabled) and evidence/measure4/c1-real-control.json (match true, schema v2, key absent); C1 25/26->26/26, alias 8->0; C2 29/30 with the expected strict red (evidence/frozen-contradiction.json), not an admission; disclose the one missing author-side case path (F9)`
- `- [~] Instructions executable by an agent without oral context — SKILL.md:585-586 entries, verdict maps, self-tests and pinned artifacts; corpus/knowledge/quota-surface-r23.md:73-97; corpus/knowledge/retention-reconciliation-r22.md (r23 correction); open: fixture schema (F2), stale :411 (F4), round-pinned scratch path (F7)`
- `- [~] No cross-domain bleed (PROVINCE.md still accurate) — read set is kernel-visible only (tools/mori-quota-surface.py:56-60, :66-76, :92-96); configuration/causes routed to tsukuroi/operator (SKILL.md:601-604; corpus/knowledge/quota-surface-r23.md:87-97); open: PROVINCE.md unchanged this round and does not yet record the new read surface (F1)`

## What I did not do

No file edits (only this report), no `SHONEN.md`/box/rank change, no promotion or
admission claim, no non-author closure claim, no live quota/host read, no quota
command of any kind, no driver/oracle/selftest execution, no build/lint/test run,
no transcript/session/credential/agent.db read, no fleet-root or sibling write, no
subagent dispatch, no lane index/refs/jj mutation.

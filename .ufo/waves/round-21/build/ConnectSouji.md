# ConnectSouji — round21 connector: souji cleanup boundary vs mori disposition

Seat: `MoriR21.ConnectSouji-4` (connector, leaf, detection/report only).
Scope: whether souji's cleanup evidence can serve as an independent disposition for
the two lost wave identities (`aggregator-r10`, `aggregator-r10-resume`), or whether
it is only a pushed receipt from the same identity that did the removal.
Axes: C1 freshness (evidence assurance) and C2 calibration (evidence-loss-first rule).
No other axis is touched.

## Verdict

Souji's cleanup chain shows that the removed bytes were **preserved and can be recovered**.
It does **not** settle either wave. Every cleanup artifact was authored by the removal
actor. The recovered pre-deletion bytes also contain no settlement record that any actor
could cite. For both identities `state: unresolved` with `independent_disposition: null` is
the only value the public evidence supports, so the pin stays BLOCKED. This matches the
frozen case `loss-cleanup-only` (true,false,false ⇒ census-regression, pin false).

## Evidence (read-only; all commands are `git -C <abs>` or `sha256sum`)

### What a souji `pushed` receipt means (its own definition)
- `souji-shokunin/SKILL.md:35`: `pushed` requires that the path exists now, that its introducing commit is an ancestor of
  the origin default ref, and that no unpushed commit touches it. `SKILL.md:49`: `SAFE(pushed)` means
  "removable after quarantine". The receipt is a gate for safe removal, not a lifecycle
  statement.
- `souji-shokunin/PROVINCE.md:7-8,17-18`: the domain is receipt-gated removal plus dry-run
  proposals "for operator approval". `PROVINCE.md:40,42` refuse unpushed or live work.
  Nothing in `PROVINCE.md` or `SKILL.md` claims wave settlement, result acceptance or
  disposition (an `rg -i "settle|wave lifecycle|disposition"` over both files returned 0 hits).
  `PROVINCE.md:157-159` (r20): the lane "acquires no cleanup, host-management or
  fleet-orchestration authority" through that repair.

### Same-identity chain (removal, receipt, approval list)
| Artifact | Revision | Author / committer |
|---|---|---|
| 96-row approval list `census/round-3/operator-approval-list.tsv:56-73` | `3674633` 2026-10-18 13:49 | souji-shokunin / souji-shokunin |
| Fleet deletion of the 18 paths | `e20f4fa` 2026-10-18 23:58 | souji-shokunin / souji-shokunin |
| Post-hoc sweep `census/operator-sweep-20261018/approval-list.tsv:59,69` and `resume-verdicts.tsv:55,65` (`SAFE pushed … snapshot=equal clean=yes`) | `2f303dc` 2026-10-19 00:02 | souji-shokunin / souji-shokunin |

- The "operator approval" and the directive "clear stale artifacts and stale cache" appear only in
  souji-authored text: the `e20f4fa` commit message, as retained in
  `.ufo/waves/round-21/evidence/removal-metadata.txt:15-16`. The command
  `git -C /home/vgpnk/Projects/shokunin grep "clear stale artifacts" origin/master -- ':!.ufo/interactive-sessions' ':!souji-shokunin'`
  returned 0 hits. [UNKNOWN] Whether a separate operator record exists outside public lane
  artifacts was not checked, because private sessions are out of bounds.

### What the receipt chain verifiably establishes
- The deletion is published: `merge-base --is-ancestor e20f4fa origin/master` succeeded
  (origin/master `a28c80c…`).
- The pre-deletion bytes can be recovered. Blob IDs at `e20f4fa^` match the receipt prefixes:
  `aggregator-r10/dispatch.json` = `29ebd3f2…` (receipt `blob=29ebd3f2`, `operator-approval-list.tsv:69`) and
  `aggregator-r10-resume/dispatch.json` = `be9791c4…` (receipt `blob=be9791c4`, `:59`). The
  introducing commit `b2f2efae7549` is an ancestor of origin/master.
- Mori's minimized copies match their declared digests:
  `cleanup-receipts.tsv` → `46f84c3a…` (= `historical-provenance.json:34` projection_sha256),
  `removal-metadata.txt` → `4276625b…` (`:20`), the source blob `2f303dc:…/approval-list.tsv` →
  `550da61f…` (`:32`), and the baseline → `0993b235…`. All five evidence files are tracked at mori `a8442a0`.
- Exactly 18 rows were removed (`removal-metadata.txt:19-36`). Mori's tip now holds 0 files under either
  directory (`ls-tree origin/master` → 0).

### What the cleanup chain cannot establish
1. **Settlement or result acceptance.** The receipt certifies recoverability at decision time,
   not whether either wave finished, reported, or was accepted. Kumitate owns lifecycle semantics
   (`mori-shokunin/PROVINCE.md:46`, FR3).
2. **Independence.** The cleanup actor, the receipt author and the approval-list author are the same
   identity (table above). The contract's `disposed` row requires an actor distinct from
   cleanup (`contract.md:13`), so no souji artifact is eligible.
3. **A disposition reconstructed from the preserved bytes.** The recovered tree is not
   settlement-shaped:
   - Neither `dispatch.json` at `e20f4fa^` is `ufo-swarm-wave-dispatch-v1` or has `Report:`
     trailers. Mori's report-presence tool accepts only that schema
     (`tools/mori-wave-settlement.py:34`); anything else is `unparsed` (`:216,223,275-276`).
   - `aggregator-r10` declares 9 role seats but holds only 4 seat files (`seats/{critic,plan,scout,scribe}.md`).
   - `aggregator-r10-resume/dispatch.json` says `"dispatched": 9` and disclaims r10:
     `"inherited_evidence": ".ufo/waves/aggregator-r10/; not claimed as this session's dispatch"` (lines 5 and 20).
   So recovering the bytes adds no settlement fact. If mori counted those bytes itself, it would
   be manufacturing a disposition, which `PROVINCE.md:169-171` forbids.
4. **Never-written vs emptied-by-hygiene in general.** The receipt covers only the 18 listed paths
   (`PROVINCE.md:88`). It is not a rule about any other empty directory.

### An independent observation of the loss (not a disposition)
- `.ufo/reports/round-12/aggregator.md:11,82` (first authored by `aggregator-shokunin` in `1bcf59e`,
  2026-10-19 22:17, *after* `e20f4fa`; ancestry confirmed) records that `aggregator-r10-resume/` was
  "empty at inspection" and refuses to use the missing `before.json`. This is the wave-owning lane
  independently observing the absence, which corroborates the C1 loss. It records no settlement or
  cleanup accounting, so it cannot be an `independent_disposition`.
- The fleet `LOG.md:733-737` (current blame: protocol-shokunin, a round-16 ledger restore) records the
  r10 dispatch claim of nine seats. That is a dispatch claim, not settlement.

## Contradiction (stated, not smoothed)

`mori-shokunin/PROVINCE.md:69` (souji adjacency row) quotes souji as saying “mori-shokunin observes fleet
health and reports; souji acts on artifacts” and cites `../souji-shokunin/PROVINCE.md:40-41`. That quote
is no longer in souji's PROVINCE: `git log -S"souji acts on artifacts" -- PROVINCE.md` shows it was added
in `ccbb132` (mint) and removed in `42d9ff3` (round-18). Today `:40-41` are Refuses rows. The current text
at `:50-52` reads "souji lists only its own uid's scratch residue and routes liveness or resource findings to mori".
The row's conclusion (souji owns artifact cleanup, not fleet health) still holds, but its citation
is stale. C2 asks for province prose to be corrected by appended errata, and this row is the souji
boundary that the r21 classification relies on.

## Proposed move (one, bounded; for L1 to judge)

Append one province erratum. Do not edit the row in place, so history stays append-only. It should
cover both of the following:
- **Re-cite the souji row** to `../souji-shokunin/PROVINCE.md:7-8,50-52` and `SKILL.md:35,49`, and add one
  sentence: *a souji `pushed` receipt is same-identity removal-safety and recoverability evidence;
  it is never an `independent_disposition`, and the preserved pre-deletion bytes contain no
  settlement record (non-v1 dispatch, 4 of 9 r10 seat files, resume disclaims r10).*
- **Name who can supply a disposition.** Only a non-souji, non-mori identity can supply the
  per-wave statement: the aggregator L1 (the wave owner), kumitate (lifecycle) or the operator.
  The round-12 aggregator report is cited as corroboration of the loss, not as a disposition.

Affected axes:
- C1 improves evidence assurance. It closes the tempting path "recover bytes → call it
  cleanup-accounted" without changing row state, and keeps 0 omitted and 2 unresolved.
- C2 improves calibration. The `loss-cleanup-only` case now has an explicit actor-eligibility basis.
- No harm to coverage, the baseline bytes, or the historical registers. No pin and no new capability.

## Risks
- Overreach into souji's province: the erratum describes souji evidence and must not restate
  souji policy. Cite it; don't paraphrase it as mori rule.
- The audit tool `tools/mori-evidence-loss.py` does not exist at HEAD `a8442a0`. The "distinct actor
  from cleanup" check therefore exists only on paper. The draft
  `corpus/evidence/loss-accounting-r21.json` and `.ufo/waves/round-21/frozen/required.json` are
  still untracked. The contract requires committed copies (`contract.md:13`), so L1 must commit
  them before any audit measurement counts.
- The `cleanup.actor` field in `loss-accounting-r21.json:21,42` is extra to the contract's
  `{path,revision,sha256}` shape. A strict schema check might reject it, while dropping it would weaken the
  distinct-actor test. L1 should decide which, and say so explicitly.
- [UNKNOWN] Operator approval records outside public lane artifacts.

## Verification L1 should run (not run here)
- After the tool lands: `tools/mori-evidence-loss.py audit --root . --required .ufo/waves/round-21/frozen/required.json --accounting corpus/evidence/loss-accounting-r21.json`
  should give rc1 with `unresolved=2`, `omitted=0`, `pin_allowed=false`.
- A mutation that sets `independent_disposition` to a souji-authored path, or to an actor equal to
  `cleanup.actor`, must stay invalid and unresolved.
- Re-run the blob-equality and ancestry commands above. They are cheap and read-only.

## Tooling / bounds
- No installs or updates. `skill://godspeed` did not resolve under `/home/vgpnk/.omp`
  (glob `**/godspeed/SKILL.md` → 0 files), so I followed the inline godspeed steps from the assignment.
- No writes outside this file. No git writes, builds, tests, census or pin.

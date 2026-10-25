# ScribeLessonGate — round 48 w1

## Scope and evidence

Read the frozen contract and v3 spec, round-47 lesson and its non-author spot-check, fleet `/home/vgpnk/Projects/shokunin/CORPUS.md`, merge `MERGE-REPORT.md`, staged quota entries and `SOURCES.append.md`, lane `PROVINCE.md` and `corpus/QUALITY.md`, frozen assimilation collision/id/quarantine files, four committed r48 source copies, and round-48 w1 registry. The assimilation package contains no `PROVINCE.md` or `QUALITY.md` (glob search of `/home/vgpnk/Projects/shokuknow/merge/mori/**` found none); fit below is assessed against the lane's own province and quality contract, not a staged per-entry fit document. No lane tools were run and no production corpus files were changed.

Observed checks:

- `grep -cE 'xfs_quota|quotactl|EDQUOT|repquota' corpus/SOURCES.md` at entering revision is recorded in frozen `evidence/sweep-quota-rows.txt` as `0` (the receipt itself also records command and date).
- `grep -nE 'EDQUOT' corpus/evidence/sources-r48/errno.h` → `107:#define EDQUOT 122 /* Quota exceeded */`.
- Grepping the committed copies found `Lists all paths with devices/project identifiers` and `may also take a long time` in `xfs_quota.8.html`; `No disk quota is found for the indicated user` in `quotactl.2.html`; `Disk quota exceeded` and `配额管理` in `aliyun-nas-quota.html`. These are spot checks, not a full claim adjudication.
- Two read-only `curl` status checks of the RHEL 9 Japanese PDF, first with a browser User-Agent then without, returned HTTP `403` and `200` respectively. The frozen contract's stated 403 result is thus observed only for the browser-UA request in this invocation; the no-UA request differed. Do not turn an unavailable PDF into a fabricated quotation: keep it out of the admitted table and report the access discrepancy for L1 to reconcile. No PDF content was read here.
- `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/**` has no staged `PROVINCE.md` or `QUALITY.md`; lane province says detection/report only and never remediation; corpus contract requires each Gate to retain considered/rejected candidates and reasons.

## Gate

### Assimilation — theme FR2, filesystem quota observability

Read-only package: `/home/vgpnk/Projects/shokuknow/merge/mori/`; `MERGE-REPORT.md` says it is staged and nothing has been written into the lane. Candidate screening below records scope fit against lane `PROVINCE.md` (detection and reporting, never remediation) and the current `QUALITY.md` source/claim discipline. This is a lesson draft, not an integration verdict.

#### Candidates considered

| staged entry | scope and evidence considered | fit / disposition |
|---|---|---|
| `quota-observability-r38.md` | FR2; xfs_quota accounting/enforcement/reporting, quotactl error distinction, directory-quota observation, Linux EDQUOT | **Admit as** `corpus/knowledge/quota-observability-r48.md`, corrected and re-grounded in the four frozen copies and lane rows S479–S482 (see map below). This fills the user-space reporting/error-surface gap without implementing or changing quota state; aligns with detection/report-only province. The staged version itself is not copied as-is: its RHEL 9 PDF source was not admitted, and its opened date/row assignments differ from the frozen contract. |
| `quota-counter-freshness-r39.md` | FR2/FR8; vendor-specific CPFS accounting lag, staged S487 | **Reject this round**: a distinct, product-specific freshness mechanism is not needed to establish the frozen FR2 query/report/error surface; it imports vendor timing and management semantics beyond the four-source r48 corpus. **Flip:** reopen the exact CPFS source, ground its timing in an accessible committed copy and a lane row opened this round, and propose as a separate clearly vendor-bounded freshness entry (not as a Linux kernel-counter property). |
| `quota-id-to-path-r40.md` | FR2; quota tree, inode project-id and host mapping availability; staged S494/S495/S500 | **Reject this round**: attribution from an id to a path is downstream of the admitted exhaustion observability question, and the staged own-host observation does not establish a fleet-wide mapping. **Flip:** a future entry may be proposed with independently re-opened sources and a narrowly scoped host observation, explicitly distinguishing kernel tree, inode attribute and userspace path mapping; keep id-to-path attribution separate from detection. |
| `quota-id-mapping-files-r41.md` | FR2; `/etc/projects` and `/etc/projid`, staged S502–S505 | **Reject this round**: optional XFS project-name/path resolution is a separate attribution layer, not required for this entry's per-id observation; staged RHEL 7 manuals also need independent source reopening and cannot stand in for the unavailable RHEL 9 JP PDF. **Flip:** re-open the two upstream man pages and any vendor source to be used, pin the actual copy and propose an explicitly XFS-scoped resolution entry, with missing mapping represented as unresolved/numeric rather than guessed. |
| `quota-path-listing-r42.md` | FR2; xfs_quota `print`/`report` join, staged S509 | **Reject this round**: report-time path joining is attribution, distinct from determining quota state and its error surface; it would broaden the single admitted entry. **Flip:** re-open the exact man-page text in a committed source copy and propose a separate XFS-only attribution entry that calls out all join inputs and does not claim a path column absent from the source. |
| `alarm-latency-model-r39.md` | FR8; external CloudMonitor detection/silence/effective-window semantics, staged S488/S489 | **Reject this round**: unrelated to FR2 filesystem quota observability and outside the chosen assimilation theme. Lane `PROVINCE.md` does not own alert-policy calibration. **Flip:** route to a separately scoped FR8 proposal only if a concrete mori reporting requirement needs this vocabulary, with vendor numbers explicitly non-authoritative for local thresholds. |

#### Admission and renumbering

Admit one entry only: `quota-observability-r48.md`. It is the quota theme's direct FR2 contribution and keeps mori read-only. Staged ids collide by document with lane ids, not just by number. Frozen evidence files list staged S471–S478 as colliding; lane S477/S478 already belong to different documents. New rows for this claim are S479–S482, assigned by document:

| lane id | source document | staged id / action |
|---|---|---|
| S479 | `xfs_quota(8)` | staged S477; renumber to S479 (staged S477 collides with lane's own-work S477) |
| S480 | `quotactl(2)` | staged S478; renumber to S480 (staged S478 collides with lane ROMA full-text S478) |
| S481 | Linux v7.2 generic `errno.h` | staged S482; renumber to S481 by this document's assigned position in the frozen source set |
| S482 | Aliyun NAS subdirectory quota page | staged S479; renumber to S482 by document; staged sequence is not authoritative for lane id assignment |

The two remaining staged collision ids, S475 and S476, are not quota-entry citations and are not admitted for this entry. The r48 contract explicitly states new ids start at S479 and fixes these four source URLs and copies. S477/S478 in lane registry remain their pre-existing documents; do not overwrite them.

#### Rejections and limits

- **Solaris `errno=49`: reject.** The number belongs to Solaris, not Linux's generic errno header. The frozen Linux v7.2 copy gives `EDQUOT 122` at line 107. **Flip:** none for the Linux errno claim; a separately scoped Solaris statement would require a Solaris primary source and must not be substituted for Linux.
- **RHEL 9 Japanese PDF:** unavailable for this Gate's evidence at the required HTTP 403 path on the browser-UA request; no quote was read. Classify as `unreachable`, not fabrication, and exclude from admitted quote claims. This run also observed HTTP 200 without a User-Agent, so the precise reproducible request/response must be resolved by L1 before repeating the contract's access claim. **Flip:** obtain and hash the exact PDF copy through an authorized successful fetch, extract and locate the quotation, and re-open the resulting copy; never invent a quote to fill the gap.
- The staged entry's broad treatment of RHEL 9 report markers, its `verified-at` 2026-10-23 date, and its staged source ids are not carried into the new entry. **Flip:** only after re-opening/copying that source and assigning its actual lane row under the frozen contract.
- Generic candidates that concern freshness, path attribution, mapping files, or notification timing are rejected above for scope separation, not because their assertions are proven false. Their respective flip conditions name what evidence/scope would justify reconsideration.

#### Quarantine slice

The frozen `assimilation/quarantine-slice` names S244, S262, S268 as rows whose cited source could not be fetched and whose quote was unchecked. They are not appended or treated as fabricated. Verdict slots remain pending only until their named scouts publish:

| row | verdict | pending owner |
|---|---|---|
| S244 | `PENDING-L1` | `ScoutQuarantineS244` has not yet published a verdict in the available peer output. |
| S262 | `PENDING-L1` | `ScoutQuarantineS262` has not yet published a verdict in the available peer output. |
| S268 | `PENDING-L1` | `ScoutQuarantineS268` has not yet published a verdict in the available peer output. |

These are the only pending verdicts in this draft. Re-check and replace them with the actual scout verdicts before integration; a seat dispatch or in-progress transcript is not evidence of a verdict.

### Spot-check

Previous outside check: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-47-verifier-spotcheck.md` (round-47 non-author closure). **Round-48 gate spot-check result: pending L1/non-author review; no round-48 outside verdict is claimed here.**

## Assimilation evidence note

The above is the scoped Gate draft only. It does not claim that the r48 entry, SOURCES rows, or any staged candidate have been integrated into the lane. Entry-source quote matches observed above are limited spot checks; claim entailment and full entry acceptance remain unverified by this seat.

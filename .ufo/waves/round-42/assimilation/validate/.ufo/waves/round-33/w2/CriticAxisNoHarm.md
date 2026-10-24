# CriticAxisNoHarm — round 33 wave 2

Scope: advisory falsification of `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8` versus `7d382043`. No admission, row-support judgment, score change, lane edit or runtime invocation. Paths below are lane-relative unless absolute.

Citation shorthand: `contract.md` is `.ufo/waves/round-33/contract.md`; `w1/` is `.ufo/waves/round-33/w1/`; `disk-write-rate-r33.md` and `surfaces-r7.md` are under `corpus/knowledge/`; `round-33.md` is `corpus/lessons/round-33.md`; `S###.src` is under `corpus/evidence/sources-r33/`; `AXES.md` is the canonical absolute path named below.

## Axes and observed delta

The axes are **coverage, operability, depth, freshness, calibration, adjacency** (`SCORECARD.md:8-15`). Their technical definitions are in `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md:11-16`.

Executed, with each Git process bounded by `timeout 120s prlimit --as=1073741824`:

```text
git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --stat 7d382043 62db24c01d5b7c2247f43852ea2b28d0ae5e40c8
83 files changed, 30324 insertions(+), 6 deletions(-)

git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --numstat 7d382043 62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 -- corpus/knowledge corpus/SOURCES.md
17  6  corpus/SOURCES.md
59  0  corpus/knowledge/disk-write-rate-r33.md

git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --name-status 7d382043 62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 -- tools PROVINCE.md SCORECARD.md corpus/README.md
(no output)
```

The requested deletion-line predicate `^-[^-]` matches **6** lines: S041, S044, S051, S062, S064, S069. I applied the specialized grep tool to the captured output of the requested corpus diff, rather than invoking shell grep; the independent numstat above agrees. These are six replaced row lines, not six removed source IDs or six deleted knowledge entries. Each replacement adds `lane rule:`; S064 also changes the clause separator (measured corpus diff; `corpus/lessons/round-33.md:79-92`).

## Ranked findings

### 1. Major — accounting time is promoted to an exact busy-time share

**Attack:** `corpus/knowledge/disk-write-rate-r33.md:24`; propagated into `SKILL.md:818`.

The new instruction says to report `io_ticks / elapsed milliseconds` as “the share of the window with I/O in progress.” Its own cited committed source explicitly limits that interpretation:

> “Since 5.0 this field counts jiffies when at least one request was started or completed. If request runs more than 2 jiffies then some I/O time might be not accounted in case of concurrent requests.”

Evidence: `corpus/evidence/sources-r33/S181.src:78-80`. This is stronger than an absent supporting quote: the cited source supplies the omitted counterexample. Gate S181 quotes the preceding simpler sentence but not this caveat (`corpus/lessons/round-33.md:16`).

**Impacted axes:** depth and calibration. [INFERENCE] A reader following the new SKILL rule can report less than the actual busy-time fraction during the explicitly documented concurrent-request case, while presenting it as that fraction. No executable tool change is needed for that instructional regression.

**Smallest safe correction:** replace the exact-share wording in both the row and SKILL with an accounted-`io_ticks` measure, not a promised exact busy-time fraction. If retaining a concurrency explanation, locate the source caveat in the Gate too. Do not accept “approximately true” silently under the frozen no-caveat R-J (`contract.md:47-50`).

### 2. Major — one disk/partition exclusion becomes a host-total recipe

**Attack:** `corpus/knowledge/disk-write-rate-r33.md:21`; propagated into `SKILL.md:817`.

The row establishes that a partition's accounted sectors are also added to its disk, then instructs “Total a host's writes over whole-disk lines only or over partition lines only.” The cited macro is one-way:

```text
__part_stat_add((part), field, addnd);
if (bdev_is_partition(part))
    __part_stat_add(bdev_whole(part), field, addnd);
```

Evidence: `corpus/evidence/sources-r33/S183.src:60-64`; sector additions use this macro at `S184.src:1110` and `S185.src:862`.

**Counterexample:** [INFERENCE from the cited code] an accounted write addressed to a whole device increments that device, without incrementing any partition. A partition-only host total can therefore omit writes; the reverse equality is not established by the macro. The rule also provides no accounting-layer selection for stacked devices. This is not hypothetical topology on this host: the committed observation lists `dm-0` under `/sys/block` (`w1/ExecHostDiskstats.md:25-30`) over `nvme0n1p2` (`:48-56`), and the natural-window deltas are `nvme0n1=41080`, `nvme0n1p2=41080`, `dm-0=41080` (`:116-119`). [INFERENCE] Merely excluding partitions while retaining both non-partition block-device rows still counts those writes twice. The entry itself leaves that stacking problem unsourced/frontier (`disk-write-rate-r33.md:38-43`).

**Impacted axes:** depth, calibration; possible coverage misrepresentation if a host-total reporting capability is claimed from this rule.

**Smallest safe correction:** state only the supported local rule: do not sum a particular disk with its own partitions. Remove the host-total alternative from the row and SKILL until accounting-layer selection and omissions are sourced. Keep stacked-device host totals frontier.

### 3. Major — uptime division is incorrectly called a counter-lifetime mean

**Attack:** `corpus/knowledge/disk-write-rate-r33.md:31,47-49`.

The row says dividing sectors written by uptime gives “a mean over the counter's whole life, which may straddle a reset”; the prose repeats “the value is a lifetime mean.” The cited source says counters reset on reattachment or reinitialization as well as boot (`corpus/evidence/sources-r33/S181.src:33-37`). The unchanged census actually divides by host uptime, not time since counter initialization (`tools/mori-census.sh:1892-1894`).

**Counterexample:** [INFERENCE, illustrative arithmetic, not a run] host uptime 1000 seconds; device attached at second 900; 1000 sectors written since attachment. `1000/1000=1` sector/s is not the counter-lifetime average `1000/100=10` sectors/s. Thus acknowledging resets does not make the denominator correct. A reset also prevents the current counter from representing all writes since boot.

**Impacted axes:** depth and calibration. The tool's arithmetic is inherited; the new endorsement under known reset conditions is the round-33 defect.

**Smallest safe correction:** call this the current counter divided by host uptime; qualify the since-boot interpretation on uninterrupted accounting since boot, and remove the lifetime-mean assertion. This does not require tuning, a new probe or a remediation change.

### 4. Major provenance/conformance defect — six immutable source bodies edited in place

**Attack:** `corpus/SOURCES.md:47,50,57,68,70,75`; recorded at `corpus/lessons/round-33.md:35-36,79-92`.

The measured diff replaces six existing rows' teaches/scope cells. The canonical registry contract permits only `status`, `recheck` and `used-by` in-place changes; a correction must be a new row whose teaches begins `supersedes S0NN —` (`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md:116-118`). The lesson expressly says no permitted mutable cell changed (`:35-36`). The routed instruction asks for lane-application declarations or sourcing (`corpus/lessons/round-32-verifier-spotcheck.md:190-192`); it does not waive the registry contract.

**Impacted axes:** calibration/provenance and freshness auditability. This is not evidence that six technical claims vanished: the labels improve attribution. The defect is changing the claim body while preserving its historical row identity and opened date, rather than representing a superseding claim.

**Smallest safe correction:** restore the six historical bodies in a new corrective commit, then add properly opened, Gate-grounded superseding rows containing the declarations; update affected current references as required. Preserve the repair lesson and append an erratum rather than rewriting that record. This is repairable process debt, not a reason to relabel the entire C1 surface.

## Six-axis no-harm attack

These are harm candidates and bounded negative checks, not canonical verdicts.

| Axis | Could the measured change count as harm? | Evidence / limit |
|---|---|---|
| coverage | No observed removal of an existing surface. The host-total wording is an overclaim, not a demonstrated new capability. | Zero knowledge deletions; unchanged `PROVINCE.md` and coverage index in the Git outputs above. Finding 2 identifies the narrower unsafe implication. |
| operability | No observed production-tool regression attributable to changed tool bytes. Unsafe new instructions remain actionable documentation defects. | `tools` diff empty; the new entry explicitly says no census change and keeps the two-sample arm deferred (`disk-write-rate-r33.md:47-51`). Existing detector errors are acknowledged and retired from routed carry, not fixed (`round-33.md:116-128`); I did not rerun them. |
| depth | Yes: new incorrect/unqualified decision rules can weaken the skill even while adding rows. | Findings 1–3; these rules reach the user-facing SKILL, not merely a source archive. |
| freshness | No live-page staleness established by this review; there is a record-integrity concern, not proof of an upstream drift. | New sources are explicitly version/commit pinned (`disk-write-rate-r33.md:3-5`); no old recheck cell changed (`round-33.md:35`). Finding 4 affects the audit trail. No live fetch was run here. |
| calibration | Yes: exactness/coverage assertions exceed their evidence, and historical source-claim identity is altered. | Findings 1–4. Scores are not inflated at this measured revision: SCORECARD diff empty; the contract holds depth at 5 absent admitted closure (`contract.md:77`). |
| adjacency | No detected tuning/remediation bleed. | Detection/report fence is explicit in `PROVINCE.md:12-18` and new entry `:7-9`; tool/PROVINCE diffs are empty. Kernel `.src` files are committed evidence, not a new host-control implementation. |

## Declared-axis fit

**Depth is a defensible primary axis for C1; no axis-name defect found.** The actual surface is added technical decision detail on an already named resource-runway frontier, not an operational cutover: sector units, completion accounting, reset handling, field layouts and interpretation (`disk-write-rate-r33.md:19-32`; `PROVINCE.md:49`). That matches the canonical depth definition, “Verifiable technical detail — decision tables … cited sources” (`AXES.md:11`). The baseline already held the sector conversion, average and a two-sample example (`surfaces-r7.md:122-147`, also read at `7d382043`); those particular facts alone are not new depth. The proposed table adds other source-linked distinctions rather than only re-scoring that old formula.

Under `/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-33.md:343-365`, the round should not claim:

- **Coverage acquisition:** no new running arm or frontier-to-core transfer occurred; FR6 remains deferred (`PROVINCE.md:49`; new entry `:50-51`).
- **Freshness as C1:** the live rechecks and source-row repairs are separable repair work (`round-33.md:38-112`), not the new table's primary changed surface.
- **Depth merely from a row count:** §9 forbids counting a sourceless fixture or re-scoring held rules as depth (`mori-round-33.md:361-365`). C1 therefore still needs the honest semantic R-J check; a correctly named axis does not cure Findings 1–3. I did not run or replace that judge.

The table is technical-depth work with fixable defects, not evidence of saturation or authority to trade depth/calibration harm for a larger source/row count. Canonical no-harm admission remains separate from the C1 count (`AXES.md:33-38`).

## Checks and containment

Read the contract including A1 and R-J/R-R; compared both requested revisions' statistics and corpus diff; enumerated the six deleted row lines; compared production-tool/province/score/index paths; read the changed SKILL/QUALITY/lessons and new entry; challenged reporting rules against committed S181/S183/S184/S185 code/docs and host observation; compared the baseline disk note and canonical axis/registry definitions. These are static checks, not passing build/test/gate results.

No tests, census, counter, judge, upstream fetch, settings edit, Git/jj write, subagent, background job or tool installation/update was run. All commands started here completed; no process remains to stop. Only this report was written.

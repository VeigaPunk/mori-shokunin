# Mo56CritAssim — attack on the round-56 "Assimilation: none" stance

Seat: Mo56CritAssim (critic, wave w1). Target of attack: the contract's
`Assimilation: none` stance (`mori-shokunin/.ufo/waves/round-56/contract.md:71-72`,
lesson `corpus/lessons/round-56.md:49-53`). Method: read the merge package and
the 3-row quarantine slice, then judge every plausible candidate per the
per-entry gates (PROVINCE scope, QUALITY bar, coverage-map ground). Observation
only; no lane file was edited.

## Verdict

**None defensible.** No staged entry in `/home/vgpnk/Projects/shokuknow/merge/mori/`
obviously should have been adopted this round. The stance survives the attack,
and there is a second, structural reason adoption was impossible as staged:
the package's row-id space has been overtaken by the lane's own registry
(75 of its 136 ids now name different sources), so the append cannot be done
without a fresh renumber plus per-entry re-verification — the round-45 M8
class, not a this-round fix.

## Evidence

### 1. The package and the claims' ground do not intersect

Package inventory (`/home/vgpnk/Projects/shokuknow/merge/mori/MERGE-REPORT.md`,
`MERGE-REPORT.json`): 136 proposed rows, ids S471–S606, "first staged id is
S471", "lane registry currently holds 243 rows"; 80 knowledge entries (75 new
files, 5 amendments), staged by `corpus-expansion-1`, "Nothing was written
into the lane repo."

Round-56 claims rest only on S544 + S545 (`contract.md` C1/C2; lesson
`round-56.md` Gate table). C1's ground is the FR5 open coverage ground:
"reading the driver's `launch`/`complete` lines in `.ufo/watchdog.log` as a
second liveness source" (`corpus/README.md:345`, retired routed carry
`corpus/lessons/round-33.md:134-137`). C2's ground is new: "seat-output vote
binding (no prior lane note)" (`corpus/knowledge/vote-binding-r56.md`
coverage-map line).

Topic sweep over all 80 staged knowledge files:

```
$ cd /home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge
$ grep -ilE 'watchdog|driver|launch|seat-output|seat output|json.*scalar|binding' *.md
census-field-enforcement-r48.md   census-level-pins-change-r49.md   host-oom-activity-r42.md
limit-keeper-sweep-r49.md         live-scope-watch-r49.md           multi-limit-reconciliation-r40.md
probe-absent-vs-dead-r39.md       quota-path-listing-r42.md         reconciliation-rules-r39.md
selection-elements-unrecorded-r47.md  selection-is-a-measurement-r45.md  selection-recorded-on-every-branch-r46.md
selection-recorded-r44.md         standing-sampler-identity-r42.md  unit-identity-lifetime-r40.md
verdict-record-durability-r51.md  who-sets-the-scope-cap-r45.md
(exit 0; hits are OOM-census "selection"/"driver" wording, none is the watchdog-log liveness source)
```

```
$ grep -ilE 'watchdog\.log|vote|RECHECK|tally|launch/complete|seat-output' \
    /home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/*.md
(no knowledge file matches; exit 1)
```

Only two staged entries carry an FR5 coverage-map at all —
`census-field-enforcement-r48.md` ("coverage-map: FR5, FR1") and
`census-level-pins-change-r49.md` ("coverage-map: FR12, FR5") — and both are
under FR5's *pid-probe* boundary clause ("an unavailable pid probe is not
absence, and argv-substring matches do not establish daemon identity"), i.e.
census selftest/fixture-pin material, not the launch/complete liveness source.
No staged entry touches C2's ground (the staged rounds predate the round-55
vote-arm failure; verified-at dates in the staged files are 2026-10-23/24).

### 2. The staged row-id space is stale — direct append is impossible

```
$ awk -F'|' '/^\| S[0-9]/ {gsub(/ /,"",$2); print $2}' corpus/SOURCES.md | sort -u > lane-ids.txt   # run in the lane work tree
$ awk -F'|' '/^\| S[0-9]/ {gsub(/ /,"",$2); print $2}' /home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md | sort -u > staged-ids.txt
lane ids: 318 | staged ids: 136 | collision count: 75
staged first/last: S471 S606 | lane max id: S545
(exit 0)
```

The collisions name different sources on each side, e.g. staged `S475` =
Aliyun SchedulerX workflow doc vs lane `S475` = Linux `include/trace/events/oom.h`
v7.2 (mined 2026-10-25); staged `S484` = Huawei DataArts Studio vs lane `S484`
= SPARC `errno.h` v7.2; staged `S495` = Google Lustre quotas vs lane `S495` =
`mm_inline.h` v7.2. The package's own metadata is equally stale ("registry
currently holds 243 rows" — the round-56 start census records 316 rows,
23 W04, `evidence/census-start.txt`). This is the round-45 M8 failure class
(`corpus/lessons/round-45.md:175`): a staged renumber map already existed as a
draft and was wrong (it mapped the first staged row to S471→S473, the id the
lane's own admitted row occupies). Adoption therefore cannot be "obvious" for
any entry this round.

### 3. Per-entry gates on the seat-spec candidates

**reconciliation-rules-r39.md** (new file; coverage-map FR4; rows staged
S484–S486 = Huawei DataArts / Alibaba MaxCompute pages, fetched by the
campaign 2026-10-23):
- PROVINCE: in-province only as descriptive vocabulary; the entry itself
  declares "kumitate owns result semantics (`PROVINCE.md:46`); mori reports
  filesystem shape. This entry therefore stays descriptive" and "It does not
  close FR4".
- QUALITY: staged text has carried overclaims before (QUALITY 124,
  `corpus/QUALITY.md:1041-1045`: staged `oom-tracing-tracepoints-r42.md`
  headlined "exactly three named tracepoints" from a paper whose own sentence
  says "such as"; and the staged `journal-reach-at-ceiling-r46.md` figures
  contradicted the lane's own 2026-10-25 receipt, `corpus/QUALITY.md:1143-1147`).
  Its rows collide with the lane's own S484–S486.
- Coverage-map: FR4 is not either claim's ground. The round-56 frontier step
  is the census before→after receipt fix (QUALITY 152), not FR4.
- Gate result: not adoptable this round.

**multi-limit-reconciliation-r40.md** (coverage-map FR4): same analysis; its
own rule statement "(policy, count, scope)" is a verdict-shape vocabulary, not
claim support. Not adoptable this round.

**wave-settlement-r20.md amendment** (coverage-map FR3, FR4; rows staged
S475/S476 = Aliyun SchedulerX / Alibaba Serverless Workflow pages):
- PROVINCE: the lane already holds its own `corpus/knowledge/wave-settlement-r20.md`
  (FR3 advance, filesystem shape only; `PROVINCE.md` round-20 note: "Its
  `settled` means report-file settlement only, not kumitate's lifecycle
  settlement"). The amendment would append vendor settlement-status
  vocabulary (mark_success / skipped / retention bound) over a deliberately
  narrow boundary.
- QUALITY: staged S475/S476 collide with the lane's own rows; vendor pages not
  opened by the lane.
- Coverage-map: the amendment itself says "FR4's … is unaffected — no source
  here reconciles three disagreeing records"; C2's tally is vote counting over
  committed bytes, not wave-settlement status semantics.
- Gate result: not adoptable this round.

**The two FR5-tagged entries** (census-field-enforcement-r48.md,
census-level-pins-change-r49.md): different FR5 clause than C1's ground;
census-selftest material; no launch/complete liveness content; no duplicate
authority with C1 (C1's entry: the probe "never reads state values and never
follows symlinks (the census owns value semantics)"). Also
census-level-pins-change duplicates ground the lane already holds itself
(`corpus/knowledge/census-cgroup-levels-r45.md`). Not adoptable this round.

### 4. Quarantine slice and considerthese

3-row slice (`S244`, `S262`, `S268`; register class "the cited source could
not be fetched, so no quote was checked"; re-derived per
`.ufo/waves/round-55/assimilation/quarantine-verdicts.txt`): S244 PRESENT at
the arXiv companion (publisher path still 403); S262/S268 PRESENT in the
publisher ROMA PDF fetched 2026-10-27 (sha256
`1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2`). None is
cited by the round-56 claims (S544/S545 only); the staged rows S501/S507 that
point at the same paper add aspects to knowledge the lane already holds
(`oom-victim-context-r41.md`, `oom-tracepoints-r47.md`). No adoption forced.
considerthese `2026-10-26.md` proposals are about pin-check mismatch tagging,
unfixed-flag carry, re-execution and a suggestion ledger — none requests
package adoption; consistent with the contract's "considerthese proposals
checked."

## Named limits (routed, not fixed here)

- L1: staged package id-space collision (75/136) + stale package metadata
  (243 vs 316 rows) — any future assimilation needs a fresh renumber map and
  per-entry gate re-verification before append; candidate for a round-57
  assimilation-hygiene item, separate from the frozen claims.
- L2: staged entries' vendor sources (Aliyun/Huawei/Alibaba/DolphinScheduler)
  were fetched by the campaign on 2026-10-23 and never opened by the lane; a
  per-entry QUALITY-124-style overclaim sweep would be needed before any
  adoption.

## Findings

- **LOW** — `Assimilation: none` stance attacked and upheld: no staged entry
  passes all three per-entry gates for round-56 adoption; verdict "none
  defensible" (no entry named). Concerns `mori-shokunin/.ufo/waves/round-56/contract.md:71-72`.
- **MED** — staged package row-id space is stale: 75 of 136 staged ids
  (S471–S545) collide with the lane registry's own rows for different sources
  (e.g. staged S475 Aliyun SchedulerX vs lane S475 `include/trace/events/oom.h`
  v7.2; staged S484 Huawei DataArts vs lane S484 SPARC `errno.h`); package
  metadata says "registry currently holds 243 rows" vs the round-56 start
  census 316. Direct append is impossible; renumber + per-entry re-verification
  required (round-45 M8 class). Concerns
  `/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md` and
  `/home/vgpnk/Projects/shokuknow/merge/mori/MERGE-REPORT.md:4-6`.
- **LOW** — the two seat-spec example entries (`reconciliation-rules-r39.md`,
  `wave-settlement-r20.md` amendment) map to FR4/FR3, not to the C1 (FR5
  launch/complete ground, `corpus/README.md:345`) or C2 (vote binding,
  `corpus/knowledge/vote-binding-r56.md`) ground, and both self-declare they
  close nothing; neither was obviously adoptable this round. Concerns the two
  staged entry files under `/home/vgpnk/Projects/shokuknow/merge/mori/`.
- **LOW** — quarantine slice (S244/S262/S268) verdicts stand and are
  consistent with the register text; no claim cites them; no staged-row
  adoption forced. Concerns
  `mori-shokunin/.ufo/waves/round-55/assimilation/quarantine-verdicts.txt`.
- **INFO** — UNVERIFIED: the staged vendor-page quotes themselves (Aliyun,
  Huawei, Alibaba, DolphinScheduler) were not re-fetched or re-checked against
  the staged entries this seat; not required for the verdict, but required
  before any future adoption.

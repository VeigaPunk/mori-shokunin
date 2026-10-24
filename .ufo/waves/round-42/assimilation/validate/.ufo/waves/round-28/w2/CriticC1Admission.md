# CriticC1Admission — round 28 wave 2 (attacked: C1 admission at f2de0ee)

**Verdict: partial.** At `f2de0eedcd60d2e354da75265ea6122bc3896073`, `C1=met` is **not printed**: the counter prints `C1=unmet`, exit 1. Seven of the eight rows were really re-opened against live bytes: every digest I re-fetched matches. But the reader side of C1 is mostly bookkeeping. Readers were repointed by swapping ids. One knowledge statement now contradicts the row it cites (S152). Readers call S146 "rejected" and "HTTP 404" although S146 is a `mined` tarball row. Two reader lines cite S147, which does not exist at this revision. S146 is a supersession of S097 in form, but it changes the row's identity and carries false provenance in the Gate.

Seat: MoriR28.CriticC1Admission. Read-only. Scratch: `/fast/scratch/hyaku/mori-r28-w2/CriticC1Admission/`. Tools installed or updated: none.

## 1. Is `C1=met` printed? No

`bash .ufo/waves/round-28/count-c1.sh f2de0eedcd60d2e354da75265ea6122bc3896073` printed this (run 2026-10-22, about 18:52Z):

```
row_identity=rows=151 changed=0 removed=0 bad=0
superseding=7/8 ids=S096,S097,S127,S128,S129,S131,S140
fail S147 row_absent
readers_left=0
C1=unmet
exit=1
```

- The Gate at `corpus/lessons/round-28.md:63-71` (f2de0ee) has lines for S145, S146 and S148-S152, but none for S147.
- The working tree holds one S147 row that is not committed (`grep -c '^| *S147 *|' corpus/SOURCES.md` → 1). The commits `1ee7f65`, `2bab4f7` and `301835a` hold none.
- Nothing at f2de0ee claims round-28 `C1=met`: `git grep 'C1=met'` finds only `evidence/r27-tip-c1.txt:10`, which is the round-27 counter, and `LOG.md:1867`, which is about round 27. **Ruling: there is no calibration overclaim at this revision.**

## 2. Were the rows re-opened against live bytes? Yes, for 7/8

I re-fetched every Gate URL between 2026-10-22T18:52:57Z and 18:52:58Z. The `base.c` fetch from raw.githubusercontent returned HTTP 429, so I re-fetched it from git.kernel.org `plain/fs/proc/base.c?h=v7.2`. Every sha256 equals its Gate cell (`corpus/lessons/round-28.md:65-71`):

| row | live sha256 (mine) | Gate | quote located in my bytes |
|---|---|---|---|
| S145 patch | `a255f447…7cd6` | = | patch :15-17 "so we only use PSI_IRQ_FULL." yes |
| S146 tarball | `180f0d16…ca083f` | = | quote is from the 404 body, not the tarball (§4) |
| S148 base.c v7.2 | `cef1a2cf…15c6` | = | :1147 `if (mm_flags_test(MMF_MULTIPROCESS, p->mm)) {` yes |
| S149 adj / score pages | `769edf3b…80a9` / `6169628d…b2bc` | = | "The default value for this file is 0" found once |
| S150 systemd.exec.xml v262 | `44b89bff…d844` | = | :1299-1300 "defaults to the OOM score adjustment level of the service manager itself" yes |
| S151 listing / earlyoom.default | `8b3c95cf…c145` / `c0770413…84a2` | = | :535 `"truncated": false`; :5 `EARLYOOM_ARGS="-r 3600"` yes |
| S152 job-manager.ts @6962d5cd | `f8851470…70bd` | = | :305 `return Math.max(1, Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS));` yes |

- **Access times fall inside the round.** The Gate times run 17:58:56Z-18:00:50Z, which is before commit `1c4c186` (committer time 15:34:21-03:00, that is 18:34:21Z).
- **The S151 fix holds against live bytes.** The old tree URL returns `flat entries 31`, while `?recursive=1` gives 67 entries and 60 blobs (my python count). This matches S151's teaches.
- **The S145 fix holds.** In the commit patch, `pressure/irq` sits inside both `if (psi_enable) {` (patch :252) and `#ifdef CONFIG_IRQ_TIME_ACCOUNTING` (:257-259).
- **The S096/S097/S101 restoration holds:** `changed=0`. The S097 restored cell equals the 17-hex first-published text, and the round-27 in-place edit (16-hex digest, S090 flip) moved into S146.

**Ruling:** the row half is substantive freshness, not bookkeeping.

## 3. Reader side: ids repointed, statements not re-checked (depth and calibration harmed)

`git diff --stat 763d346 f2de0ee` over the readers shows 28 insertions and 28 deletions across 6 files. The word diff shows id swaps (`S096`→`S145`, `S097`→`S146`, `S140`→`S152`, …) plus a few "supersedes the round-NN row" suffixes. The sentences that the new rows correct were not re-read.

**F1 — a knowledge statement contradicts its own cited row (depth).**
- `corpus/knowledge/harness-job-capacity-r25.md:277` now cites S152 for the rewrite.
- `:281-283` says "the explicit floor `Math.max(1, …)` did not survive that rewrite — neither the clamp expression nor the accessor … carries a floor at v18.12.6".
- `:330` says "The round-26 draft's "floor of 1 held" was false".
- S152's teaches (`corpus/SOURCES.md:157`) says the opposite: "the floor can move from the call site to the consumer without the cap ever losing it".
- Live bytes side with S152:
  - parent `d9bc4fbd` `job-manager.ts:284` reads `this.#maxRunningJobs = Math.max(1, Math.floor(options.maxRunningJobs ?? DEFAULT_MAX_RUNNING_JOBS));`
  - v18.12.6 `job-manager.ts:334` (S098's file, `45c35e40…`, fetched 18:54:42Z) still reads `return Math.max(1, Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS));`
- So at v18.12.6 the cap's floor of 1 held. The entry's `:330` statement is false, and it now cites the very row that refutes it. The old S140 defect was fixed in SOURCES but not in the knowledge it feeds.
- `readers_left=0` cannot see this, because it counts ids, not claims.

**F2 — readers mislabel S146 (calibration, and a second authority for its status).**
- `PROVINCE.md:258` says "`proc_pressure(5)` does not exist (S146, rejected)".
- `corpus/knowledge/system-pressure-r24.md:1` says "Rejected candidate: S146 (… HTTP 404 …)".
- `:224` says "(S146, rejected: HTTP 404)".
- At f2de0ee, S146 is status `mined`, tier A, and its source is the man-pages 6.20 tarball (`corpus/SOURCES.md:152`). Its teaches also says "so the rejection stands; flip: …".
- Three places now disagree about whether S146 is a rejection: the status cell, the teaches and the readers.

**F3 — dangling ids (bookkeeping before substance).**
- `harness-job-capacity-r25.md:1` and `:47` cite S147, which is absent at f2de0ee.
- `readers_left=0` was reached by pointing readers at a row that does not exist yet.

The reader edits that are not defects:
- `oom-victim-selection-r27.md` "Defaults" (Arch `--avoid` packaging) and its "normally at 0" narrowing already agreed with S151 and S150.
- `system-pressure-r24.md:112-126` already names `psi_enable` as a second cause for a missing irq file.
- `git grep` for the old defect phrases ("build-configuration fact", "exactly one configuration", "is local configuration", "floor can vanish", "user units inherit") over SKILL.md, PROVINCE.md, corpus/README.md, corpus/knowledge, README.md and MANPAGE.md returns nothing.
- The only old-id hit outside history files is `oom-victim-selection-r27.md:203` (tsukuroi's S127, correctly excluded).

## 4. Is S146 still a supersession of S097?

**Ruling: in form yes, in identity no.** This is a fixable defect, not a tradeoff.

**It qualifies in form.** The teaches opens `supersedes S097 — ` and corrects S097's text: the digest width, the S001→S090 flip row, and negative claims that had no anchor. CORPUS allows this: "A correction is a new row whose `teaches` opens `supersedes S0NN —`" (`/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`). The tarball's absence claim is true:
- `sha256sums.asc` line 61 equals my tarball digest.
- My `find` for `*pressure*` paths and my `grep -ril 'proc/pressure'` over the extracted tree both return nothing.
- In man7, `dir_section_5.html` and `proc.5.html` each give `grep -c -i pressure` = 0.
- The 404 body is unchanged, with sha256 `80c3fe2ae1062abf56456f…f880`, the same prefix as S097's.

**It changes identity.** Every identity cell changed: source (man7 candidate URL → kernel.org tarball), tier C→A, scope, and status `rejected`→`mined`. The row now describes a different object.
- The house pattern keeps the superseded row's URL. The drafting seat names this itself: "keeping the superseded row's own URL (as S142 did for S090)" (`w1/SupersedeS097.md:130`).
- The seat switched sources to avoid a census `W01` warning, which fires on a tier-C row that is both `mined` and cited (`w1/SupersedeS097.md:133-135`). That is a source chosen to satisfy a metric.
- Amendment A1 had already anticipated this row as "rejected when the row it supersedes is rejected (S097 is a 404 page…)" (`contract.md:87-89`). The seat offered only `mined` options and never the `rejected` one, which keeps the URL and cannot trigger `W01`.

**F4 — the Gate's provenance is split (false provenance).**
- `corpus/lessons/round-28.md:61` says the sha256 cell digests "the fetched bytes at the URL named first", which is the tarball.
- Line `:66` pairs that tarball digest with a quote from "404 body line 6 (man7 candidate page)", which comes from different bytes.
- The 404 page's own digest is only in the S146 anchor.
- The counter accepts this because it only checks that a quote is present (`count-c1.sh:68-70`).

**F5 — S146's teaches contradicts itself (calibration).**
- `corpus/SOURCES.md:152` says "its flip cited S001 for the psi.rst lines … and as a rejected row it stated no flip at all".
- S097's restored teaches does contain `flip: the same scope is documented by the kernel PSI documentation (S001; …)`.
- The defensible claim is narrower: S097's flip names an alternative source, not "what would change the verdict" (`CORPUS.md:101-102`).

## 5. Impacted axes

| axis | effect | evidence |
|---|---|---|
| freshness | rows: improved (7/8 re-opened, digests live-equal); claim C1: unmet at f2de0ee | §1, §2 |
| depth | harmed in one place: a knowledge statement is false against live bytes and against its own cited row | F1 |
| calibration | harmed: readers label a `mined` row "rejected / HTTP 404"; S146 teaches contradicts itself; the Gate quote and its digest come from different bytes | F2, F4, F5 |
| coverage, adjacency | no change seen | none |

## 6. Smallest safe corrections (for L1 MoriR28; append-only)

1. **S147.** Commit the S147 row and its Gate line before `C1=met` can be printed. `readers_left` already depends on it (F3).
2. **F1.** In `harness-job-capacity-r25.md:281-283` and `:330`, state that the sdk-site `Math.max(1, …)` vanished but the cap's floor of 1 held in `AsyncJobManager` (parent `job-manager.ts:284`, v18.12.6 `job-manager.ts:334`). Withdraw "floor of 1 held was false" with a dated correction note, the same way this entry already handles corrections.
3. **S146, preferred fix.** Replace it, before admission, with a row S153 that supersedes S097:
   - source = S097's own man7 URL; tier C; status `rejected`, as A1 allows;
   - teaches `supersedes S097 — REJECTED: <reason>; flip: the man-pages project publishes a proc_pressure page …`;
   - the tarball, dir_section_5 and proc.5 digests in the anchor;
   - a Gate line whose sha256 is the 404 body's `80c3fe2a…f880` and whose quote comes from that body.

   This keeps identity, avoids `W01` (a rejected row is not "mined and cited"), and makes the readers' "(rejected: HTTP 404)" true. **Alternative:** keep S146 `mined`, but change the reader labels at `PROVINCE.md:258` and `system-pressure-r24.md:1,224` to drop "rejected / HTTP 404", and add the 404 digest to Gate `:66`.
4. **F5.** In the new row, replace "stated no flip at all" with "its flip named an alternative source, not a condition that would change the verdict".
5. **Counter gap.** The counter cannot detect F1, F2, F4 or F5, so `C1=met` alone is not evidence that readers were re-checked. A non-author reader sample (one claim per repointed id) should accompany admission. That sample is a review step, not a counter change in this round.

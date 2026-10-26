# Round 49 verifier spot-check — mori

author: hyaku closure (non-author integrator, @m_sonnet)

Scope: mori lane-round 49. Lane HEAD before `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86`, after `43d846669efe5a2fcc2325006f165af4e7e7fda4`. Closure date 2026-10-25. I did not author the round and edited no lane-authored file.

Driver digest (`.ufo/watchdog.log`, mutable):
`2026-10-25T20:31:38-03:00 launch mori round=49 pgid=2957725 driver=hyaku-inline attempt=1` / `2026-10-25T22:58:26-03:00 complete mori round=49; hyaku-inline attempt=1`.

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git -C /home/vgpnk/Projects/shokunin log --format='%an %H' -- .ufo/reports/round-49/mori.md` | `mori-shokunin 8af5b0b652eff4de1631972ac5bf0969f801aeeb` |
| `SHONEN` heading, one line per box | read report | present; four boxes, all `[~]`, each with a pointer |
| cited commits are ancestors of the branch | `git merge-base --is-ancestor <h> master` for `0df17b7b…`, `24ebc799`, `64c2d5fc`, `43d84666…`, `b3e3453d…` | all five hold |
| pushed, no ahead | `scripts/hyaku/jj-lane.sh state …/mori-shokunin` | `local=remote=43d846669efe… ahead=0 behind=0 tracked=0 untracked=7` |
| remote tip | `git ls-remote origin refs/heads/master` | `43d846669efe5a2fcc2325006f165af4e7e7fda4` |
| leftovers | `git status --porcelain` | seven untracked `.ufo/waves/round-40/scratch/mori-conform-selftest-*` dirs, none of them round-49 work (the report names them) |
| prompt carries template contract | `.ufo/prompts/mori-round-49.md` §4 report contract, §5 push scope, §6 hyaku addendum | present (545 lines) |
| real report, not a marker | named commits, evidence files, selftests | real; status `ok` |

Conformance defects (status-neutral, recorded in notes only):
- **D-a. Report author date precedes the lane tip it cites.** The fleet report commit has author date `2026-10-25T22:54:10-03:00`; the lane tip `43d84666` is dated `22:56:42`. The committer date (`22:57:47`) is after the tip. This is round 48's routed defect 2 again; the report discloses the mechanism.
- **D-b. Round shape short of the directive.** One v1 wave of 49 seats, against the 64–100 band. No wave 2 and no WAVE-DONE. The report names two seats with no report (`Mo49ExecCounterTiming`, `Mo49SimpCounters`) and says their status is unknown. This is an undispatched wave. It bars nothing, and the report says so honestly.
- **D-c. Erratum sitting in the report.** The report corrects "48 wave-1 reports" to 47 in a trailing note. The lesson and `LOG.md` still carry the wrong number. Corrections sweep every mention (PROTOCOL §Evidence standard), so a named correction entry belongs in round 50.
- **D-d. The tool selftest tally has no committed output file.** `PIN_CHECK_SELFTEST pass=114 fail=0` and the unlanded check's 17/17 appear only as prose in the report, `LOG.md` and the lesson. Committed output files exist for the counters (`evidence/selftest-c1.txt` → `C1_SELFTEST pass=44 fail=0`, `evidence/selftest-c2.txt` → `C2_SELFTEST pass=26 fail=0`). `grep -rn 'pass=114'` finds the figure only in `corpus/lessons/round-49.md`. I did not run the tool's selftest (a lane gate). The tally is therefore unverified by me. It supports no claim here: C1 rests on the counter's after-file.
- **D-e. `.scratch/` debris.** `.gitignore` now ignores `.scratch/`, which fixes untracked noise. About 183 `.scratch/` directories remain on disk (`ls -d .scratch/*/ | wc -l` → 183). The report says deletion was not done. Round 48 routed defect 1 is half-closed.
- **D-f. Variant count.** `after-c1-at-tip.txt` has 27 `variant` lines (18 junk, 9 honest incl. `real` and `real-opaque`) against `variants=26` in the verdict line. This is an off-by-one in prose or a counting convention nobody documented. It changes no verdict.

## 2. Claims

Which gate or selftest each claim rests on, and how I handled it (PROTOCOL §Gate standard, Closure consequence: verify committed evidence, never execute a sibling's gate):

| claim | axis | method |
|---|---|---|
| C1 reconciler reads what a reader sees | calibration | **evidence-verified**, plus plain re-measurement of the committed bytes. The verdict comes from the lane's frozen counter `count-c1.py`, which I did not run. |
| C2 journal-reach entry, located quotes | depth | **re-measured** by my own script, not the lane counter. |

### C1 (calibration, held 5)

Evidence checked:
- Freeze integrity: `sha256sum -c .ufo/waves/round-49/evidence/freeze-sha256.txt` → every line `OK` (contract, both counters, 8 controls, receipts, four source copies). `git diff --stat 0df17b7b 43d84666 -- count-c1.py count-c2.py contract.md controls` → empty. Neither counter nor control moved after the freeze.
- Before: `evidence/control-c1-tool-v3-entering.txt` → `C1=unmet junk_met=9 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…`. My awk over its 27 variant lines: 9 lines with `expect≠got` (N1–N9 junk edits the v3 tool accepted).
- After: `evidence/after-c1-at-tip.txt` → `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=64c2d5fc…`, exit 0. My awk: 27 variant lines, 0 mismatches; 18 `expect=unmet`, 9 `expect=met`.
- Tool bytes at the measured rev equal the tip: `git show 64c2d5fc:tools/mori-pin-check.py | sha256sum` equals `sha256sum tools/mori-pin-check.py` (`697ab2cc…`). So the measurement at `64c2d5fc` is the tool at `43d84666`.
- Counter controls (the counter can fail): always-met stub → `expect=unmet got=met` rows; the filename sniffer scores `junk_met=18`, `C1=unmet` (exit 1) under this round's counter and `C1=met junk_met=0` under round 48's (`variants=12`, exit 0), which is the leak the opaque handles close; the always-unmet stub is red; the do-nothing C2 control is `unmet`. Counter selftest `C1_SELFTEST pass=44 fail=0` committed.

Disclosures I accept as honest and graded on:
- (a) The merged round-48 witness already met the predicate at the freeze (`control-c1-tool-r48-merged-witness.txt` → `C1=met … variants=26`). The claim's new work is landing it, the new arms and the harder counter, not inventing the fix.
- (b) The opaque handle is content-derived: it beats filename and scratch-name sniffers, not a tool that hashes content or reads sibling copies.
- (c) The counter's selftest runs a twin of `plan()`.
- (d) K4 and the R11 carve-out stay open.

Ruling: **verified** (evidence-verified, not re-executed). The counter's frozen verdict, its revision and its self-test tally are committed and consistent. The before→after (unmet 9 survivors → met 0) re-derives from the two committed files. The score stays 5 and the lane claims no score change; the verdict is a measurement, not a score move.

### C2 (depth, held 5)

My measurement, independent of `count-c2.py`: I parsed the 21 rows of the claims table in `corpus/knowledge/journal-reach-r49.md`, stripped `<script>/<style>/comments`, tags and entities, collapsed whitespace, and tested each quote as a substring of the committed copy named in its `source` cell:

`rows=21 located=21 missing=0` (S485 7, S486 4, S487 5, S488 5). Copy hashes: `sha256sum corpus/evidence/sources-r49/*` → `be3952cb…`, `75440570…`, `b4a9b53e…`, `a7b44356…`, all equal to the freeze pins.

Reported: `C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=4 …` (`evidence/after-c2-at-tip.txt`). Agrees. Before: `control-c2-donothing.txt` → `C2=unmet … failed=entry_absent,pins`. Sweep before the entry: `git grep -c` of `SystemMaxUse`, `MaxRetentionSec`, `RuntimeMaxUse` at `b3e3453d` over `corpus/SOURCES.md corpus/knowledge` → 0, 0, 0.

Freshness check beyond the lane: I fetched the three live freedesktop pages on 2026-10-25. Their sha256 equal the committed copies byte for byte (`b4a9b53e…`, `a7b44356…`, `75440570…`), matching the entry's `verified-at` claim.

Limit I carry forward (the lane states it too, `Mo49CritC2Counter`): a located quote is location, not entailment. The entry's claims table stops at each quote and its Limits section says so. The host rows are one capture (56M, 19M, 37M, two boots, 256M/64M drop-in), which I checked line by line against `host-journal-reach.txt`. The 269M→56M vacuum explanation is marked `[INFERENCE]` in the entry.

Ruling: **verified** (re-measured).

### Per-axis grades

| axis | entering | verdict | basis |
|---|---|---|---|
| calibration | 5 | improved | C1 verified; no score change claimed |
| depth | 5 | improved | C2 re-measured 21/21 |
| coverage | 6 | unchanged | `git diff b3e3453d 43d84666 -- SCORECARD.md` adds lines only, the one `-` line is the diff header, the axes table is untouched |
| operability | 7 | unchanged | not claimed; the new counter capability sits in the capabilities table |
| freshness | 5 | unchanged | not claimed |
| adjacency | 6 | unchanged | not claimed; the entry's Boundaries section defers journald configuration to tsukuroi and cites the sibling file path:lines |

No axis harmed. No exploratory claim, so no `unprovable-but-better` ruling is owed.

## 3. Discernment spot-check (LEARNING.md)

Source: `corpus/lessons/round-49.md` `## Gate`.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| **S486** journalctl(1), admit, mined, supersedes S351 | admit | live `https://www.freedesktop.org/software/systemd/man/latest/journalctl.html` (fetch, sha256 `75440570…`, equals the committed copy); `corpus/SOURCES.md:265`; rows S014 (`:20`) and S470 (`:249`) | **agree** | The 18-word quote "--vacuum-size= removes the oldest archived journal files until the disk space they use falls below the specified size" is present live and in the copy. `teaches` opens `supersedes S351 —`; the scope text names S014 (cursor/field) and S470 (single `--disk-usage` sentence) and differs from both. S351 stays `rejected`. Disclosure noted: the receipt obtains two daemon limit lines with `journalctl -g` (a MESSAGE filter), so S351's flip is met only on the narrow reading. The lane records this and rests no claim row on those two lines. I accept the narrow reading (S351's objection was a kernel-message grep for kill records). |
| **S485** journald.conf(5), admit | admit | live `…/journald.conf.html` (sha256 `b4a9b53e…` = copy) | **agree** | "Also note that only archived files are deleted to reduce the space occupied by journal files." (16 words) found live. Row is `mined`, opened 2026-10-25, `used-by` the entry. |
| **S487** systemd-journald.service(8), admit | admit | live `…/systemd-journald.service.html` (sha256 `a7b44356…` = copy) | **agree** | "systemd-journald will automatically remove the oldest archived journal files to limit disk use" (13 words) found live and in the copy. |
| **S488** own-work host receipt, admit | admit | `corpus/evidence/sources-r49/host-journal-reach.txt` (sha256 `be3952cb…`) | **agree** | Line "Archived and active journals take up 56M in the file system." (11 words) is the first `--disk-usage` output, rc 0; 19M and 37M under `--system`/`--user`; `--list-boots` lists two boots; `ls -A /run/log/journal` rc 0 with no output. The entry's numbers are the receipt's. |
| staged `reach-per-journal-second-instance-r48.md` (source S554) | reject | `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/reach-per-journal-second-instance-r48.md`; `…/SOURCES.append.md:90`; the committed receipt | **agree**, one nuance | Its sole `source:` is `file:///home/vgpnk/Projects/shokuknow/lanes/mori/round11/.deepresearch/notes/r11-reach-second-journal.txt`, a note outside the lane, and the lane's own S351 rule says such a note is a lead, not evidence. The reject on provenance stands. Nuance: the lesson says "six boots" "understates what the receipt shows". The staged entry's capture is dated 2026-10-24 and the receipt is 2026-10-25 after a vacuum, so the two counts are different moments, not a contradiction. The reject does not need that argument. The "uniform rule" claim in the r47 sibling being unsupported by two stores on one host is a sound separate reason. |
| staged `runtime-journal-reach-is-the-boot-r49.md`, rule adopted via S487 | reject as entry | receipt `ls -A /run/log/journal`; entry's stated recheck path `/run/log/journal/<machine-id>` | **agree** | The receipt lists the parent `/run/log/journal` (rc 0, empty), not the machine-id directory the staged recheck names, so the two commands do not measure the same directory. The rule half survives as the S487 quote. |

New SOURCES rows re-opened: S485, S486, S487 and S488 as above. Their ≤25-word quotes live in the lesson Gate per CORPUS.md rule 1 (the row's own cells hold paraphrase plus a pinned copy hash); all four quotes are present in the pinned copies, and the three manual-page quotes are present on the live pages too (S488 is a host receipt with no live page).

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → 21 `W04` + one `ok` = 22 lines, rc 0 (my run; the new warning is S486 on the third scope of `journalctl.html`, S351 and S470 being the other two). `evidence/census-start.txt` holds 20 `W04` + `ok` = 21 lines; `evidence/census-end.txt` holds 21 `W04` + `ok` + a `census-rc=0` line = 23 lines, and its census lines equal my run's. Matches the lesson's forecast of 22 census lines at the end (the report's "23 lines" counts the rc line).
Row count: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` at `b3e3453d` → 257, at tip → 261. Matches the report.

## 4. Trend verdicts

- **expansion: improved.** One admitted entry (`journal-reach-r49.md`) on ground the sweep shows the lane did not hold (0 hits for the three option names at `b3e3453d`), citing four `mined` rows S485–S488, tied to frontier FR1. Capabilities added (opaque-handle counter, flagged-versus-fixed count) are demonstrated in the report. Caveat: the lane already holds adjacent journal entries (`journal-alarm-routing-r14`, `journal-disk-usage-total-r51`), so the new ground is the retention rule, not journald as a whole. It is correctly scoped as such.
- **quality: unchanged.** No earlier entry was re-verified or superseded as an admitted entry. S351 stays rejected and S486 supersedes a rejected row, not an admitted one. No admitted entry fails its re-check: I re-checked 21/21 quotes.
- **discernment: improved.** Every sampled decision (four admits, two rejects) agrees. The one nuance (D-g below) is an overstated argument on a reject, not a wrong decision. The S351 literal-versus-narrow flip is disclosed in the lesson with the decision and its consequence for the entry.

## 5. Routed defects (lane must fix next round)

1. **File the round-50 report with an author date at or after the lane tip it cites** (D-a, recurring from round 48 defect 2). Add a landing step that checks `git log -1 --format=%aI` of the report against the tip.
2. **Commit a selftest output file for the tools** (D-d): `tools/mori-pin-check.py --selftest` and `tools/mori-unlanded-check.py --selftest` into `.ufo/waves/round-50/evidence/`, so the 114/114 and 17/17 tallies resolve at closure time.
3. **Named correction entry for the 48-vs-47 report count** (D-c) in the round-50 lesson and `LOG.md`, sweeping every mention.
4. **Delete the `.scratch/` residue** (D-e) and the seven `round-40/scratch/mori-conform-selftest-*` dirs, then record the `git status --porcelain --ignored` count. Ignoring is not removal.
5. **Run the round shape the directive asks for** (D-b): wave 2 and a residual call, or an explicit written operator waiver. Account for the two seats with no report.
6. **Document the variants count** (D-f): `variants=26` against 27 listed lines.
7. **K4 and the R11 carve-out** stay open from the lane's own disclosures. **Randomise the handle** (`Mo49CritC1Counter`), so it is not recomputable from content.
8. **D-g, discernment wording.** When a staged entry's number differs from this host's receipt, say "different capture" before "understates". The reject needs only provenance.

## 6. Notes for the operator

All four SHONEN boxes are `[~]` with resolvable pointers. Whether they are fully checkable by a non-author is the operator's call, since promotion is operator-owned. I observe that the "no cross-domain bleed" box is supported by the entry's Boundaries section and the two connector reports named, and that the "executable without oral context" box leans on tool selftest tallies I could not verify from committed output (D-d). I wrote no `[x]`.

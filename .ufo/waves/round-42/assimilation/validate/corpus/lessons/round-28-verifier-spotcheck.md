author: hyaku closure (non-author integrator, @m_opus)

# mori round 28 — verifier spot-check (non-author closure)

Round: mori 28, L1 `MoriR28`, attempt 1. Base `6ebd518f10e53057da926353d99442d51267ccaf` → landed tip
`1fc6bb0eaab40d9ea4fe996b64d140282b76337d` (lane `master`). Report: fleet `.ufo/reports/round-28/mori.md` (fleet
commit `59c1f17fd23c067c0eb8502d1e844290e6e5479c`). Driver digest (`.ufo/watchdog.log`, copied):
`2026-10-22T14:52:07-03:00 launch mori round=28 pgid=1917534 driver=hyaku-inline attempt=1`;
`2026-10-22T16:27:12-03:00 complete mori round=28; hyaku-inline attempt=1`.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-28/mori.md` | `mori-shokunin 59c1f17fd23c067c0eb8502d1e844290e6e5479c` | ok |
| `SHONEN` heading, one line per box | read report `## SHONEN` | 4 lines: `[ ]` decision tables, `[~]` end-to-end, `[ ]` executable, `[~]` no bleed | ok |
| Cited lane commits exist and are ancestors of `master` | `git log --oneline 6ebd518f..1fc6bb0e` + `merge-base --is-ancestor <h> master` | all 12 cited hashes (`079a47c6` … `1fc6bb0e`) present in the range; `1fc6bb0e` contained in `master` and `origin/master` | ok |
| Pushed | `scripts/hyaku/jj-lane.sh state …/mori-shokunin` | `branch=master local=1fc6bb0e… remote=1fc6bb0e… ahead=0 behind=0 head=detached tracked=0 untracked=6` | ok |
| Leftovers | `git status --porcelain` | six untracked paths (below) | defect, status-neutral |
| Prompt carries template contract | `grep -nE '^#+ ' .ufo/prompts/mori-round-28.md` | §1 MISSION/AXES, §2 Claims, §2b Frontier, §3 L2 floor, §4 Report contract, §5 Commit/push, §6 hyaku addendum | ok |
| Marker report? | — | no: 12 lane commits, checkable work | not a marker |

Untracked lane paths at closure (six, not five; the three wave-2 files landed after the report):

1. `.scratch/` — pre-round (2026-10-21); ruled not round work at r24. Not round work.
2. `.ufo/waves/round-28/w1/FixR1Runway.md` — round-28 wave-1 seat output, withheld on purpose (quotes the live harness
   settings value; report "Other"). Round work, deliberately uncommitted and disclosed.
3. `.ufo/waves/round-28/wave1-run.err` — validator stderr from the wave-1 run. Round byproduct, disclosed.
4. `.ufo/waves/round-28/w2/MutCountC1Amended.md`, 5. `w2/MutHeadingCheck.md`, 6. `w2/MutTipReceiptCheck.md` — round-28
   wave-2 seat outputs that returned after the last commit. Round work, uncommitted; the report says their output is
   not evidence and defers them to round 29's lesson. Not used as evidence here.

Misroot sweep, checked from the fleet root: none of the seven names (`MANPAGE.md`, `base.c`, `main.c`, `meminfo.c`,
`oom_kill.c`, `sd-main.c`, `user@.service.in`) exists at `/home/vgpnk/Projects/shokunin/` (`[ -e … ]` → absent ×7);
each exists at the lane root at `1fc6bb0e` and `git show 1fc6bb0e:<f> | sha256sum | cut -c1-16` reproduces the
prefix in `evidence/misroot-before.txt` for all seven (`cc48b02e79255ae2`, `cef1a2cf3f34f683`, `08656b0bc90c85f2`,
`526e512c89c58cb0`, `452f1348e79c252e`, `5ecdca43a8e0ed08`, `72c2f40dcfced1d8`). Receipts: before `misroot_hits=7`,
after `misroot_hits=0`. Sweep holds.

## 2. Per-claim re-check

No claim was withdrawn: both declared claims (contract `079a47c6`, amendments A1 `763d3469`, A2 `1c4c186e`) are
reported as met.

### C1 — freshness (re-measured with plain commands; counter evidence-verified)

| Measurement (mine) | Base `6ebd518f` | Tip `1fc6bb0e` | Reported |
|---|---|---|---|
| `git show <r>:corpus/SOURCES.md \| grep -c '^\| S[0-9]'` | 144 | 152 | 144 → 152 |
| `git diff 6ebd518f 1fc6bb0e -- corpus/SOURCES.md` row lines | — | `-/+` S096, S097, S101 (in-place restore); `+` S145–S152; no other row touched | matches "Rows touched" |
| old-id cites in live readers (`git grep -c '\b<id>\b' <r> -- SKILL.md PROVINCE.md corpus/README.md corpus/knowledge/`, summed) S096/S097/S101/S127/S128/S129/S131/S140 | 8/3/2/11/2/4/2/3 = 35 | 0/0/0/1/0/0/0/0 | `readers_left=0` |
| new-id cites, same readers, S145…S152 | — | 8/3/2/10/4/7/4/4 (all ≥1) | `superseding=8/8` |

The one remaining `S127` hit is `corpus/knowledge/oom-victim-selection-r27.md:204` "tsukuroi S115, S118, S120 and
S127 are `psi.rst`…" — it names tsukuroi's row, not mori's, as the lesson discloses; the counter's
`readers_left=0` is consistent with that. Counter evidence (lane-owned gate, not executed by me):
`evidence/tip-count-c1.txt` at `5ef4e8db` → `rows=152 changed=0 removed=0 bad=0`, `superseding=8/8`,
`readers_left=0`, `C1=met`, `exit: 0`; `evidence/c1-before-a1.txt` → `C1=unmet`. `git diff --stat 5ef4e8db
1fc6bb0e` touches only the three tip receipt files, so the receipt measures the landed content. **C1 verifies as
declared.**

### C2 — operability (cases re-measured; self-test evidence-verified)

| Measurement (mine) | Observed | Reported |
|---|---|---|
| `git show 1fc6bb0e:tools/fixtures/mori-oom-killers/cases-a2.json \| jq -r '.. \| objects \| select(has("rule")) \| .rule' \| sort \| uniq -c` | `3` each for A2-01 … A2-10 (30 cases, 10/10 rules) | `a2_cases=30 a2_rules_covered=10/10` |
| `git log 6ebd518f..1fc6bb0e -- <cases file>` | one commit, `d21b8bd` (the freeze); never edited after | frozen, unedited |
| order: counter vs freeze vs first run | `7b75f45` 15:50:53-03:00 → `d21b8bd` 15:50:55-03:00 → first run 18:51:02Z | counter before cases; run after freeze |
| `git diff 6ebd518f 1fc6bb0e -- tools/mori-oom-killers.py \| wc -l` | `0` | tool unchanged |

Evidence-verified (lane gate, not executed): `evidence/c2-freeze-selftest.txt` → `MORI_OOM_KILLERS_SELFTEST: PASS
30/30`, `exit=0` at the freeze commit; `evidence/tip-count-c2.txt` at `5ef4e8db` → `tool_blob=3fb78bbc…`,
`frozen_blob=match`, `frozen32_selftest=PASS 32/32`, `freeze_commit=d21b8bd3…`, `a2_rule_checks=ok`, `a2_selftest=PASS
30/30`, `C2=met`, `exit: 0`. **C2 verifies as declared** (the declared after-value is the round-28 counter printing
`C2=met`). Caveat carried as a defect, not a miss: one case-writer seat (CaseA2r03) read 45 lines of
`w1/CriticC2Design.md` before writing, so three cases are not fully blind; disclosed in `LOG.md` and lesson M6.

No-harm: `git diff 6ebd518f 1fc6bb0e -- SCORECARD.md` is append-only (round-28 declaration, A1, measured outcome; no
held score changed). Retention metric: `evidence/base-retention.txt` `"metric":4` at `6ebd518f`,
`evidence/tip-retention.txt` `"metric":4` at `5ef4e8db` (not above base; evidence-verified). Census (run by me):
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → `mori ok`, exit 0, ten W04 lines
(S035, S037, S073–S076 and S147–S150 "duplicate url across scopes"). The report says nine W04 with S148–S150 new; I
count four new (S147 also), all a superseding row reusing its old row's URL. Warning only, no harm.

Re-measured: C1 row count, row diff, reader cites; C2 case count/rule coverage, freeze history, tool diff, misroot
sweep, census. Evidence-verified: C1/C2 counter verdicts, A2 self-test tallies, retention metric.

## 3. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| freshness | improved | C1 verified: eight carried row defects superseded by rows re-opened this round (hashes reproduced below), readers repointed |
| operability | improved | C2 verified: ten A2 rules pinned by 30 frozen cases, PASS 30/30, tool unchanged |
| depth | unchanged | held, no claim |
| calibration | unchanged | held, no claim |
| coverage | unchanged | held, no claim |
| adjacency | unchanged | held, no claim |

## 4. Discernment spot-check

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S145 (Gate) | admit, A, mined | `curl -sSL https://github.com/torvalds/linux/commit/52b1364ba0b105122d6de0e719b36db705011ac1.patch \| sha256sum` | agree | sha256 `a255f447…7cd6` equals the Gate cell; patch lines 15–17 read "…IRQ/SOFTIRQ always happen in the current task on the CPU, make nothing productive could run even if it were runnable, so we only use PSI_IRQ_FULL." — the quoted span, ≤25 words |
| S152 (Gate; SOURCES row) | admit, A, mined | `curl …/6962d5cd…/packages/coding-agent/src/async/job-manager.ts` | agree | sha256 `f8851470…70bd` equals the Gate cell; line 305 is `return Math.max(1, Math.floor(value ?? DEFAULT_MAX_RUNNING_JOBS));` verbatim (5 words) |
| S147 (Gate; SOURCES row) | admit, A, mined | `curl …/45c35e40…/docs/settings.md` | agree | sha256 `0b2e1457…5883` equals; line 623 holds the quoted `async.maxJobs` table row, floor stated, no maximum — matches the corrected `teaches` |
| S150 (Gate; SOURCES row) | admit, A, mined | `curl …/systemd/v262/man/systemd.exec.xml` | agree | sha256 `44b89bff…d844` equals; lines 1299–1300 hold the 20-word quote verbatim |
| proc_pressure(5) candidate (S097, restored first-published row, `rejected`; S146 Gate quote) | reject (404, no such page) | `curl -s -w '%{http_code} %{size_download}' https://man7.org/linux/man-pages/man5/proc_pressure.5.html` | agree | still `404`, 196 bytes, sha256 `80c3fe2ae1062abf5…` = the S097 anchor digest; nothing to admit |

The round-28 `## Gate` table carries only admit lines (S145–S152); the reject sample was taken from the rejected
candidate the round re-opened (S097/S146). SOURCES rows S147, S150, S152 were re-opened in full and each quote is ≤25
words and located at the cited line.

## 5. Trend verdicts

- **expansion: unchanged** — agree: 8 new rows each supersede an existing row; no FR row advanced.
- **quality: improved** — agree: eight carried row defects fixed against re-opened bytes (hashes reproduced above),
  first-published cells restored (`row_identity changed=0`), A2 rules pinned by frozen cases, QUALITY 83–84 added.
- **discernment: improved** — agree: wave-1 critics overturned both counters before data (A1 `763d3469`, A2
  `1c4c186e`); wave-2 surfaced and the round disclosed the C2 blindness leak and reader-wording defects (fixed in
  `ac696ad3`).

## 6. Routed defects (lane fixes next round)

1. Commit or disposition the three late wave-2 outputs (`w2/MutCountC1Amended.md`, `w2/MutHeadingCheck.md`,
   `w2/MutTipReceiptCheck.md`) and `wave1-run.err`; act on any finding they carry against C1's counter or QUALITY 83–84.
2. C2 blindness: CaseA2r03's three cases were written after reading 45 lines of `w1/CriticC2Design.md`; A2-07/A2-10
   breach shapes found by wave-1 ReviewA2SpecVsTool have no frozen case. Add blind cases for them.
3. Gate tables should record reject decisions met during source work, so the closure can sample one from the Gate.
4. Tip receipts were measured at the parent `5ef4e8db`; that is equivalent here (receipt-only last commit) but say
   so in the receipt header or measure the landed tip.
5. Report census line: ten W04 at the tip, four new (S147–S150), not nine/three.
6. Carried open: MutCountC1 F1, F2, F3, F6, F10; S146 `teaches` self-contradiction in its first-published cell;
   ReviewReaderSweep range citations and "opened this round" dating; old rows' `used-by` cells; r25 R1 and R5.

SHONEN: two boxes `[~]`, two `[ ]`; not fully checkable by a non-author this round (no promotion note).

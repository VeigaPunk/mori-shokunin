# W2 review — C1 entry prose (`## Facts`, `## Limits`, headers) — MoriR30.ReviewEntryProse

**Verdict: agree, two low-severity wording/citation defects found** — every factual sentence in
`## Facts` and `## Limits` checks true against its cited excerpt, rule-text line, or the tip tool;
the `source:`/`verified-at:`/`recheck:` headers are true and reproduced. No false and no uncited
sentence found. The two LOW findings below are precision defects in citations/wording, not wrong facts.

Reviewed bytes: lane tip ad0f04745ced2194e58c22a0d6b38131bee3e230 (713be29 on top of it; entry landed
at ee61010d). Entry: `corpus/knowledge/earlyoom-invocation-scope-r30.md` (`## Facts` :17-86,
`## Limits` :109-119, headers :1-4). Tooling (operator directive 2026-10-19): **no installs** — used
preinstalled python3, read-only git, curl, grep. Scratch and inputs:
`/fast/scratch/hyaku/mori-r30-w2/ReviewEntryProse/`.

## Findings

### LOW-1 — Facts §1: shipped-unit citation stops at the introduction commit (entry :23-25)

"The shipped unit restarts earlyoom whenever it is killed or crashes (S159 …)" cites only S159.
S159's own SOURCES scope covers "the introduction of `Restart=always` … on 2020-03-01 only" and
explicitly "not the v1.9.0 file bytes (S120 carries `:17`)" (`corpus/SOURCES.md:165`). The v1.9.0
presence of the directive — the version this entry's grammar is scoped to — is anchored by S120
(`corpus/SOURCES.md:126`, anchor "`earlyoom.service.in:17` (`Restart=always`)"), and the round-30
Gate rejected the duplicate v1.9.0 fetch for exactly that reason (`corpus/lessons/round-30.md` Gate
row S159, "reject, duplicate URL — S120 … already anchors `:17 (Restart=always)`"). The fact is true;
the citation should be "S159+S120". One-token fix.

### LOW-2 — Facts §3 C2.1 bullet: "reports its version" is conditional (entry §3, the "Round-30 change (C2.1 …)" bullet, :53-56)

The bullet says the reader "scopes the last invocation from that stamp, **reports its version** and
its zero line counters". Tool at tip (ad0f047): the version is reported only when a version line
sits **at or after the retained stamp**. In the natural restart order the startup line precedes the
active-enter stamp (S157 `unit.c:2773-2776` assigns the stamp on entry into active, i.e. after the
process started and printed `main.c:161`), and the reader then prints `version: null`. Scratch runs,
inactive unit, `LoadState=loaded`, `ActiveEnterTimestampMonotonic=1000000`, send at t=1500000:

- `earlyoom 1.9` at t=900000 (before stamp) → `KILLER_ACTED` exit 1, `version: null`,
  `dryrun_send_lines: 0`, `process_group_lines: 0`, `actions: null`.
- version line at t=900000 = stamp, or at t=1100000 > stamp → `KILLER_ACTED` exit 1,
  `version: "1.9"`.

So "reports its version" holds only for a version line inside `[stamp, ∞)`. Suggest "reports the
version line inside that scope, when one exists". No frozen case contradicts (cases-a2-r29.json
passes 24/24 at tip); wording precision only.

### Observation (no defect) — Facts §1 rule-text citation (entry :21-22)

"a line belongs to the segment opened by the latest version line before it (rule-text.md:89-90)":
rule-text.md:89-90 is the Wave-2 fixes bullet, whose wording is the dry-run "split at each version
line" (`.ufo/waves/round-30/rule-text.md:89-90`); the general segmentation is the tool's verified
behavior (runs below), also implied by A2-06 (`rule-text.md:84-88`, `:110`) and the output schema
(`:40`). Citation is loose, not wrong.

## Verified true (sentence clusters, with evidence)

- §1 (:21-22): version line once at startup — live v1.9.0 `main.c:161` is `fprintf(stderr, "earlyoom "
  VERSION "\n");` in `main()` before the poll loop (grep on
  https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c). Segment rule: tool runs below.
- §1 (:26-27): `-b` with no argument → current-boot filter, `-u` appends the unit match — excerpt
  `corpus/evidence/sources-r30/S160.txt:512-517,543-546` (arg_boot/arg_boot_filter/SD_ID128_NULL;
  `strv_extend(&arg_system_units, …)`).
- §2 (:32-44): stamp assigned only on entry into active-or-reloading, active-exit on leaving, stop
  keeps and next start overwrites — `S157.txt:2773-2776`; "0 when not recorded this boot" — Gate row
  S157 quoting `org.freedesktop.systemd1.xml:2789-2790` verbatim (`corpus/lessons/round-30.md:119`).
  Bare-decimal rendering and literal `=0` — `S156.txt:19-24` (name fails the `Timestamp` suffix test,
  holds no `USec`) and `:194` (`%"PRIu64` fallback). Inclusive ≥ scope — `rule-text.md:25-26`; frozen
  c02/c03 pin both sides (`tools/fixtures/mori-oom-killers/cases.json:46,72`). Unbounded A2-05 —
  `rule-text.md:82-83,109`; tool: stamp 0 + send before last version line → earlier-counted, UNKNOWN.
  Active+scope-false → UNKNOWN unless positive evidence — `rule-text.md:44-52`.
- §3 (:48-49): earlier sends field — `rule-text.md:84-88,110`; stamp-less record not counted —
  `rule-text.md:95-98,114`; tool: malformed record → `earlier_invocation_send_lines: 0`.
- §3 (:50-52): verdict changes only for a non-active unit; `inactive`/`absent`(LoadState=not-found)/
  `unavailable`(failed) all `KILLER_ACTED` with `actions: null` at tip — tool runs t4/t4b/t5/t6
  (failed → `state: unavailable`, `KILLER_ACTED`, `actions: null`).
- §3 (:53-56): C2.1 behavior matches commit 7aa7748 and `.ufo/waves/round-30/evidence/fix-tool.diff`
  (bounded branch sets `scope_bounded`, keeps `actions` null, adds last-invocation counts to `acted`
  for non-active units); provenance (round-29 Judge11-13 tool errors) — `corpus/lessons/round-29-verifier-spotcheck.md:74-75,160-161`.
- §3 (:57-58): a2-06-active-earlier-invocation-sends-quiet pins QUIET with earlier=2 — validated by
  the counter row and selftest; A2a disclosed at `rule-text.md:79-80`.
- §4 (:59-72): all eight blind cases (`tools/fixtures/mori-oom-killers/cases-a2-r30.json`, ids
  `r30-disputed-*`, authors CaseR30a/b, MoriR30.CaseR30c, CaseR30d = 4 writers × 2) expect
  `KILLERS_UNKNOWN`/exit 2 with `state: active`, `scope_complete: false`, zero current actions and
  the send kept in `earlier_invocation_send_lines`; both the entering-tip blob (58b61681) and the
  changed tip tool print it (selftest `PASS 8/8` on both; t3 run prints exactly the claimed fields).
  Pre-round-29 `KILLER_ACTED` and the "not harmed" ruling — `round-29-verifier-spotcheck.md:82-98`.
  Disclosure matches wave-1 F1 ("the verdict forks on whether earlier-invocation sends count as
  positive evidence inside an unbounded scope", `.ufo/waves/round-30/w1/ReviewRuleTextShape.md:46`).
- §5 (:73-78): `dryrun mode enabled` at startup — live `main.c:295` is
  `warn("dryrun mode enabled, will not kill anything\n");`; send-site no-op — SOURCES row S155
  anchors the `:35-38` guard returning before `kill()`; per-invocation split — `rule-text.md:108,111`;
  tool: earlier real sends survive a current dry-run invocation (earlier=2, dry=1).
- §6 (:80-86): stamp-less record uncounted in both counts, scope incomplete — tool t8 (inactive →
  `KILLERS_UNKNOWN`, abstain) and t8b (active → `KILLERS_UNKNOWN`, `sigterm: 0`, `earlier: 0`);
  entry-object stamp is S154's (`corpus/SOURCES.md:160`, "entry-object monotonic stamp"); journald
  writes the notice with `rl - 1` and the unit name — `S158.txt:1291-1295`; A2-01 scope-local —
  `rule-text.md:105`; tool t9: in-scope notice → `scope_complete: false`, `KILLERS_UNKNOWN`.
- Limits (:109-119): A2a as pinned above; A1a frozen c04 exists (`cases.json:99`) and counter-validates;
  A3 c19-version-line-only exists (`cases.json:452`, bounded version-line-only → QUIET exit 0);
  A2-10 "abstain" confirmed for both active and inactive states (t8/t8b); scope current-boot only
  (S160; `rule-text.md:26`); stop keeps the stamp (S157); privacy `rule-text.md:54-55` (my runs'
  outputs hold only states/counts/version); A5 `rule-text.md:73-74`.
- "Why this entry" (:8-15): both prior entries exist (`corpus/knowledge/userspace-oom-killers-r26.md`,
  `corpus/knowledge/oom-victim-selection-r27.md`); R4/R6 routing — R6 is the disputed shape
  (`round-29-verifier-spotcheck.md:163-165`), R4 the A2-10 non-active residual answered by the C2.1
  bullet (`:160-161`, `:74-75`); exit codes 1/2/0 confirmed on every run.

## Headers

- `source:` (:1) — all five new rows' claims match the committed excerpts (S157 `unit.c:2773-2776`;
  S156 `bus-print-properties.c:19-24,194`; S158 `journald-manager.c:1291-1295`; S159 patch `:6-7`,
  `:34-36` incl. `Restart=always`; S160 `journalctl.c:512-517,543-546`), each excerpt's sha256 header
  equals its Gate digest (`corpus/lessons/round-30.md:114,116,126,135,138`). Re-used rows verified:
  S119 `main.c:161`/`:295` and S118 `kill.c:318`/`:627` confirmed against live v1.9.0 bytes (grep on
  the raw URLs; kill.c hashes to b32e0fad65e2…, the S118 row's pinned digest; S122 stamps-0 quote at
  Gate `:119`; S155 and S154 per registry rows). Header claim "`-b` with no argument selects the
  current boot" matches the excerpt. Only nit: the shipped-unit fact re-used here is S159's
  introduction anchor — see LOW-1.
- `verified-at:` (:2) — Gate rows for S156-S160 carry access times and sha256
  (`corpus/lessons/round-30.md:112-140`); excerpts exist under `corpus/evidence/sources-r30/`
  (5 files read); reproduced the re-derivation: `bash <(git show 6c47dd03:.ufo/waves/round-30/count-c1.sh) <rev>`
  runs the 58b61681 tool blob (script line `tool_data=blob(BASE,TOOL)`) → `C1=met`, `rows=13
  rows_ok=13`, `excerpts_ok=5/5`, `skill_rows=4` at both ee61010d and 713be29, zero bad rows.
  "no host unit, journal, setting or signal touched" is a conduct claim — see gaps.
- `recheck:` (:3) — actionable as written: counter name/usage verified by running it; "the five
  `--selftest` case files" is exact — `tools/fixtures/mori-oom-killers/` holds exactly five case
  files, and the tip tool passes all five (32/32, 32/32, 30/30, 24/24, 8/8).
- `author:` (:4) — `.ufo/waves/round-30/w1/DraftEntryC1.md` exists.

## Tool evidence (all inputs invented; privacy-clean: no host values, invented process name "brownduck")

Scratch `…/ReviewEntryProse/*.json`; tool `python3 -I -B tools/mori-oom-killers.py --inputs <f>`:
t1 send at stamp → `KILLER_ACTED`/1 (inclusive bound); t2-t3 pre-stamp/earlier-invocation sends →
counted in `earlier_invocation_send_lines`, never in `actions`; t4/t4b inactive+retained stamp →
`KILLER_ACTED`/1, `actions: null`; t5 failed → `state: unavailable`, `KILLER_ACTED`/1; t6 not-found →
`state: absent`, `KILLER_ACTED`/1; t7b dry-run current + real earlier (bounded) → `earlier: 2`,
`dryrun: 1`, actions zero; t8/t8b malformed stamp → `KILLERS_UNKNOWN`/2, uncounted, scope false;
t9 suppression in scope → `KILLERS_UNKNOWN`/2, scope false; t10 `oomd_notices: 1` → `KILLER_ACTED`/1;
t11 send after last version line, stamp 0 → `KILLER_ACTED`/1, `sigterm: 1`. Entering-tip blob (58b61681,
extracted to scratch) agrees on every disputed shape it is claimed to agree on (t3/t4/t4b/t5/t8) and
passes cases-a2-r30.json 8/8.

## Residual risk and verification gaps

- `verified-at:`'s "no host unit, journal, setting or signal touched" is the author's conduct claim;
  not checkable from committed bytes. My own checks touched nothing (tool prints to stdout only;
  the counter uses a system `TemporaryDirectory`).
- I did not re-open the systemd v262 sources live; S156-S160 rest on the committed excerpts plus
  Gate digests (which match). earlyoom v1.9.0 `main.c`/`kill.c` were re-opened live and match pins.
- Decision-table rows were cross-checked via the counter and selftests (13/13 ok at two revisions;
  5/5 files pass on both tools). I did not independently re-audit each row's `sources` cell beyond
  the counter's source check (`excerpts_ok=5/5`) — that is count-c1's contract and it passed.
- LOW-1/LOW-2 do not change any verdict, frozen case, or SKILL row; they are citation/wording fixes
  for the entry author to accept or reject.

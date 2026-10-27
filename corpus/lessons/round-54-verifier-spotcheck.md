# Round 54 verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)
lane: mori-shokunin · round 54 · closed 2026-10-27
base `39dcf4d7e410d362781a47e8365ca23b5c807598` → tip `0c926fdf0ca5d76794dab1ad0eb0ccac9c18b33d`
(branch `master`, remote verified); claim receipts measured at `f111d4b0120a04ed1a0a2270a72ec0a343d20e29`
(`git diff --name-status f111d4b0 0c926fdf` → four added receipts plus LOG, SCORECARD, the lesson and ledger prose
outside the ledger table). Independent measurements below were run by this closure over `git archive 0c926fdf`
(and `git archive 39dcf4d7 corpus` for the scope) in `/fast/scratch/hyaku/closure-mori-r54/` (removed after
closure). The lane's counters, selftests and tools were not executed (§Gate standard).

## Step-1 conformance

- Report `.ufo/reports/round-54/mori.md` committed on the fleet repo by the lane identity:
  `git log --format='%an <%ae> %H %ci' -- .ufo/reports/round-54/mori.md` → `mori-shokunin <mori@shokunin.local>
  e3ef3c914139eedc1081b7d43c7f7b054654a654 2026-10-27 02:46:21 -0300`, after the lane tip `0c926fdf`
  (02:43:25 -0300). Lands last.
- `SHONEN` heading present with four `[~]` lines, one per box, each with a pointer. `SHONEN.md` diff
  `39dcf4d7..0c926fdf`: the four `[~]` evidence lines refreshed, no `[x]`, no box added or removed.
- Cited lane commits `39dcf4d7 6830f3af 1116c092 78295c76 2d0347a3 782c6e7d c71d088a f111d4b0 4e587052 0c926fdf`
  (and the considerthese revision `0b36d23e`) all resolve and `git merge-base --is-ancestor <h> master` holds for
  each (11/11); `git log --oneline 39dcf4d7..0c926fdf` lists exactly the eight round-54 commits, all authored
  `mori-shokunin`.
- `scripts/hyaku/jj-lane.sh state` → `branch=master local=remote=0c926fdf… ahead=0 behind=0 head=detached tracked=0
  untracked=1`; `git ls-remote origin refs/heads/master` → `0c926fdf…`. `git status --porcelain` → one line:
  `?? .ufo/waves/round-54/w1.ready.dispatched` (defect D4). No uncommitted tracked round work; pushed.
- Prompt `.ufo/prompts/mori-round-54.md` (633 lines; committed by the lane identity `62b8877f`) carries §1
  MISSION/AXES binding, §2 claims (1–3, lowest axis, exploratory rule), §2b frontier step, §3 L2 floor (≥8 in one
  batched swarm), §4 report contract (path, sections in order, SHONEN heading, hash citation), §5 commit-then-push,
  push scope, L0 side channel, write scope (§6 item 3), plus the hyaku addendum §6 and scratch discipline §7. Its
  route wording defers to the host route table, consistent with `MISSION.md` §L2 concurrency.
- Driver digest (watchdog.log is mutable; copied):
  `2026-10-27T01:12:40-03:00 launch mori round=54 pgid=380105 driver=hyaku-inline attempt=1`;
  `2026-10-27T02:47:36-03:00 complete mori round=54; hyaku-inline attempt=1`.
- Round shape: `jq` over `w1-spec.json` → 74 items (reviewer 19, critic 18, executor 15, scribe 9, scout 4,
  sentinel 3, mutation-tester 2, connector 2, revenger 1, simplifier 1); `w1-results.json` 74 results, all with
  non-empty output. Inside the 64–128 band.
- Status: `ok` — a real report with checkable committed work, not a marker.

### Conformance defects (status-neutral)

- D1 (receipt not verbatim): `evidence/census-end.txt` is not the captured output of the command it names. Today's
  run of the same command prints tab-separated fields (as `census-start.txt` does); the receipt has spaces, no
  trailing newline after `exit=0`, and its S349 line reads `…%E7%99%BD%E6%96%87%E6%9C%AC.pdf` where
  `corpus/SOURCES.md` and the live census print `…%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf`. The verdict tokens
  (`mori ok`, rc 0, 23 W04) are right — this closure re-ran it — but the receipt is a transcription
  (§Evidence standard, "Claimed ≠ re-executed").
- D2 (Gate locators): the lesson `## Gate` table cites quote lines that do not begin the quoted text in the
  committed copies: S515 `pr_info("memory: usage …` is at `memcontrol.c.v7.3:1850`, not 1819; S520 "The number of
  processes belonging to this cgroup killed by any kind of OOM killer." at rendered line 1409, not 1225; S522 "Send
  SIGBUS when the application runs into the corrupted page." at `hwpoison.rst.v7.3:70`, not 68; S525
  `#define TRACE_SYSTEM ras` at `ras_event.h.v7.3:3`, not 7 (7 is S524's line). The other seven are right.
- D3 (correction sweep): `0c926fdf` corrected the control-replay count to 12/14 in the lesson only;
  `SCORECARD.md:2874` still reads "Ten control clone revisions were removed …" (§Evidence standard, "Corrections
  sweep every mention").
- D4 (leftover): untracked `.ufo/waves/round-54/w1.ready.dispatched` (02:04, the dispatcher's taken-marker) is not
  committed; round 53 committed its equivalents.
- D5 (report fact): the report and lesson say one seat output is malformed and "four other seat reports are absent";
  at `0c926fdf` 73 of the 74 results have `w1/<name>.md` and only `Mo54RevC1Counter` lacks one.
- D6 (pointer): QUALITY 148/149 and the SCORECARD correction paragraphs cite `lessons/round-54.md#M1`/`M1`/`M2`, but
  the round-54 `## Mistakes` table carries no M-labels (round 53's did).

## Claims — per-claim re-check

Re-measured = this closure ran its own plain measurement over committed bytes; evidence-verified = the lane's
counter/selftest receipts read, not executed.

### C1 — freshness: the 31 remaining v7.2-pinned claim rows re-verified at Linux v7.3 — **re-measured + evidence-verified: improved**

- Frozen bytes: `sha256sum -c --quiet .ufo/waves/round-54/evidence/freeze-sha256.txt` over the tip extraction →
  rc 0 (37 entries); `git diff --stat 6830f3af 0c926fdf -- contract.md count-c1.py count-c2.py
  evidence/freeze-sha256.txt controls/` → empty.
- Scope, derived independently at `39dcf4d7`: SOURCES rows whose URL names tag v7.2 (cgit `?h=v7.2`,
  raw.githubusercontent `/v7.2/`, jsDelivr `@v7.2/`, `docs.kernel.org/7.2/`) → 73 S-ids; claim|source|quote rows of
  `corpus/knowledge/*.md` citing them → 77 (commit-runway-read-r53 8, memavailable-estimate-r51 18,
  oom-memcg-stat-r50 22, overcommit-commit-limit-r52 28, quota-observability-r48 1); minus the 46 hashes in the
  round-53 ledger → **31** (8 / 22 / 1), set-equal to `evidence/c1-scope.txt`.
- Ledger re-derivation (own Python: whitespace-collapsed substring in the committed v7.3 copy; HTML with tags read as
  a space and entities decoded; per-character source-line map for the quote start): `rows 31 matched 31 status_ok 31
  quote_eq_v72 31 quote_located 31 line_ok 31 words(6–25) 31 disposition holds 31`, entry/source cells all correct,
  mismatches `[]`.
- Vote arm (own parse of `w1/Mo54Rc01.md`–`Mo54Rc12.md`, unfenced `RECHECK <h> <word>`, last line per voter wins,
  voter counted only if named in `w1-results.json`): every one of the 31 hashes carries ≥3 `holds` voters (minimum
  3), 0 dissent.
- Byte-identity claims: `cmp` of the committed v7.3 copies against the v7.2 copies → `oom_kill.c`,
  `percpu_counter.c`, `percpu_counter.h`, `errno.h` identical, as the ledger states.
- Source bytes: S515–S519 re-fetched today from cgit `plain/<path>?h=v7.3` (curl default UA; a browser UA receives
  the Anubis bot page) and S520 from `https://docs.kernel.org/7.3/admin-guide/cgroup-v2.html` → all six
  byte-identical to the committed copies (sha256 prefixes `bdb6159cc237 452f1348e79c 2c26e67751f9 4a107bc381b3
  66a5ad60566f b478c1bae998`).
- Meaning: a non-author reviewer seat this closure dispatched diffed the v7.2/v7.3 surroundings of all 31 rows
  (memcontrol.c +45/+84, mm_init.c +4, util.c 14 changed lines off the quotes, rendered page +31): 31/31
  `holds-correct`. This closure confirmed the three release-drift leads in the tag-stripped pages
  (`memory.pressure`/`io.pressure` "read-only" → "read-write"; `delay` microseconds → `delay_nsec` nanoseconds).
- Lane receipts: `evidence/c1-at-landed.txt` → `C1=met scope=31 rows=31 matched=31 status_ok=31 line_ok=31
  quote_ok=31 source_rows=ok pins=ok provenance=ok held=31 absent=0 holds=31 changed=0 voted=31 dissent=0
  rev=f111d4b0…`, exit=0; before `evidence/control-c1-do-nothing.txt` → `C1=unmet scope=31 rows=0 … failed=
  ledger_absent,pins`, exit=1; `evidence/selftest-c1.txt` → `C1_SELFTEST pass=57 fail=0`. My numbers agree with
  every reported token. Named limit, lane-disclosed: 12 of 14 control receipts name clone revisions that no longer
  exist, so the control table is first-run observation only (`w1/Mo54SentReceipts.md` F2).

### C2 — depth: hardware memory-failure kills at Linux v7.3 — **re-measured + evidence-verified: improved**

- Surface before→after: `git ls-tree 39dcf4d7 corpus/knowledge/memory-failure-kills-r54.md` → absent;
  at `0c926fdf` present (92 lines).
- Own re-derivation over the claims table: `claims 21`, every quote located (whitespace collapsed, `\|` read as `|`)
  in the committed copy of its S-id → `located 21`, quotes 6–25 words 21/21, `sources 6` (S502 S507 S521–S524).
- Entailment arm (own parse of `w1/Mo54En01.md`–`Mo54En12.md`, every unfenced `ENTAIL <h> entailed|overclaim`
  line, `<h>` = sha256[:12] of the whitespace-collapsed claim cell, voters named in `w1-results.json`, `REPLACE`
  authors excluded): every final hash carries ≥2 `entailed` voters (minimum 2), and no `overclaim` line names any
  final hash → `entailed 21`, overclaimed rows 0.
- Source bytes: S521–S524 re-fetched today from cgit `?h=v7.3` → byte-identical (`94d24a605b61 8011bb158129
  d852f950e42d a395e62b36ac`); S502/S507 are round-53 copies already re-fetched by the round-53 closure.
- Meaning: a non-author reviewer seat this closure dispatched judged all 21 claim rows **correct** against the v7.3
  copies (row-level `file:line` evidence, e.g. row 5 `memory-failure.c.v7.3:469-473`, row 11 `:1268-1275`, row 20
  `memory-failure-trace.h.v7.3:20-25,72-76`) and confirmed that no memory-failure path counts `MEMCG_OOM_KILL`
  (`oom_kill.c.v7.3:912-936` only). It found two decision-table defects outside the counted rows, both confirmed by
  this closure (routed defect 3): the panic switch fires only for `MF_MSG_KERNEL` ("reserved kernel page") with
  Ignored (`memory-failure.c.v7.3:1274`); a `MF_MSG_KERNEL_HIGH_ORDER` Ignored result (`:2478`) does not panic. So
  "a kernel-owned page came back Ignored" (entry `:62`, `SKILL.md:1219`) and "1: panic when a kernel-owned page cannot
  be recovered" (entry `:70`, `SKILL.md:1226`) are broader than the code. They copy `vm.rst`'s wording, and the
  entry's own row 11 states the narrow condition. The per-node counter cell ("pages poisoned … by outcome", `:60`)
  follows the stable-ABI wording; the counters advance once per `action_result()` call
  (`memory-failure.c.v7.3:1286-1289`). That is a LOW precision note, not a false claim.
- Host section: this closure re-read the host read-only: kernel `7.2.11-arch1-1`,
  `node0/memory_failure/{total,ignored,failed,delayed,recovered}` = `0 0 0 0 0`, `HardwareCorrupted: 0 kB`,
  `memory_failure_recovery` 1, `memory_failure_early_kill` 0, `enable_soft_offline` 1,
  `/proc/sys/vm/panic_on_unrecoverable_memory_failure` absent, `/sys/kernel/tracing` `700 root`,
  `dmesg_restrict` 1. All match the entry's `## On this host`.
- Lane receipts: `evidence/c2-at-landed.txt` → `C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=6
  source_rows=ok pins=ok provenance=ok entailed=21 dissent=0 rev=f111d4b0…`, exit=0; before
  `evidence/control-c2-do-nothing.txt` → `C2=unmet claims=0 … failed=entry_absent,pins`, exit=1;
  `evidence/selftest-c2.txt` → `C2_SELFTEST pass=54 fail=0`. My numbers agree with every reported token.

### Routed round-53 defects (lane work this round)

- D2 (round 53): `SCORECARD.md` appends the round-53 and round-50 correction paragraphs naming the `*-at-landed`
  receipts; `evidence/receipt-stage-after.txt` → `RECEIPT_STAGE rev=f111d4b0 cited_intermediate=5 flagged=0`
  (before: `flagged=5`). Evidence-verified. Closed.
- D3 (round 53): `git ls-tree --name-only` → at `39dcf4d7` the root lists `0 MANPAGE.md base.c main.c meminfo.c
  oom_kill.c sd-main.c user@.service.in`, at `0c926fdf` none of them; each file's blob sha256 at `39dcf4d7` equals
  its relocated copy under `.ufo/waves/round-28/misroot-lane-root/` (7) or `.ufo/waves/round-38/misroot-lane-root/`
  (`0`); `--repo/` is gone from the working tree. Re-measured. Closed.

### No-harm

- `git diff --numstat 39dcf4d7 0c926fdf` on lane-owned files: LOG +48/−0, PROVINCE +20/−0, SCORECARD +30/−0,
  SKILL +37/−0, QUALITY +41/−0, README +16/−0, SOURCES +17/−4. A cell-level diff shows the −4/+4 rows S502, S507,
  S508 and S514 changed only in `used-by`. Three older knowledge entries each gained an appended 4-line
  `## Recheck at Linux v7.3` pointer, with no row edited. SHONEN carries only the four refreshed `[~]` lines. No axis
  score changed (`SCORECARD.md` `## Round 54`: "no scalar score delta"). Selftest receipts
  `evidence/selftests/`: pin-check 125/125, unlanded-check 17/17, commit-runway 31/31, all exit 0.

## Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| freshness | improved | C1 re-measured: scope independently derived (31), 31/31 rows located at their v7.3 start line, ≥3 voters each, copies byte-equal to cgit/docs today, 31/31 dispositions held up on outside review |
| depth | improved | C2 re-measured: new 21-row located, entailed entry on the non-OOM kill class (0 → 1 entry), 21/21 rows judged correct by an outside seat; two decision-table cells broader than the code (routed defect 3) |
| coverage | unchanged | not claimed; no tool or capability row |
| operability | unchanged | not claimed; selftest receipts unchanged at 125/17/31 |
| calibration | unchanged | not claimed; QUALITY 148–151 appended, each citing the round-54 lesson |
| adjacency | unchanged | not claimed; PROVINCE append-only, MCE/EDAC and host repair named as adjacent |

## Discernment spot-check (`corpus/lessons/round-54.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S521 `mm/memory-failure.c` v7.3 | admit (tier A code) | `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/memory-failure.c?h=v7.3` fetched 2026-10-27: 82847 bytes, sha256 `94d24a605b61…` = committed copy; `:292` reads `pr_err("%#lx: Sending SIGBUS to %s:%d due to hardware memory corruption\n",` | agree | primary source at a pinned tag, quote verbatim at the cited line (10 words ≤ 25); it is the file that holds every kill line, sysctl and counter the entry claims |
| S520 rendered cgroup-v2 7.3 | admit (tier A docs) | `https://docs.kernel.org/7.3/admin-guide/cgroup-v2.html` fetched today: 172967 bytes, sha256 `b478c1bae998…` = committed copy; "The number of processes belonging to this cgroup killed by any kind of OOM killer." located (rendered text) at line 1409 | agree | release-pinned path, the flip the round-53 closure named; the Gate's line 1225 is wrong (D2), the decision is right |
| S525 `include/ras/ras_event.h` v7.3 | reject | cgit `plain/include/ras/ras_event.h?h=v7.3` fetched today: 11341 bytes, sha256 `408ddc2ac2a5…` = committed copy; `grep -c 'TRACE_EVENT(memory_failure_event'` → 0, the same grep on S524's copy → 1 | agree | the event moved to `include/trace/events/memory-failure.h` (S524, whose header comment says it stays in the ras system "for historical versions"); the flip condition is exact |
| jsDelivr `@v7.3` mirror route | reject (route, not a row) | `https://cdn.jsdelivr.net/gh/torvalds/linux@v7.3/{lib/percpu_counter.c,mm/oom_kill.c,mm/memory-failure.c,include/uapi/asm-generic/errno.h}` today → all 200, bytes equal to the cgit copies | agree | a mirror adds nothing over the primary, and the lane's receipt recorded a per-path 403 (`gate-rejects.txt`). Today's clean run makes it eligible as a second locator under the flip, never as the row |
| unpinned `docs.kernel.org/admin-guide/cgroup-v2.html` | reject | fetched today: `<p class="blurb">7.3.0` | agree | `latest` is mutable; S520's release-pinned URL holds the same bytes |

New-row quote re-open: S523 "The total number of raw poisoned pages (pages containing corrupted data due to memory
errors) on a NUMA node." — `sysfs-devices-node.v7.3:196-197` (starts at 196), verbatim, 19 words. S524 "For historical versions,
memory_failure_event is in ras subsystem," — `memory-failure-trace.h.v7.3:4`, 8 words. All eleven new rows
(S515–S525) re-fetched today are byte-identical to their committed copies.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → `mori ok …/SOURCES.md`,
rc 0, 23 W04 (the same 23 warnings as `census-start.txt`). Rows `grep -cE '^ {0,3}\| *S[0-9]{3,} '
corpus/SOURCES.md` → 287 at `39dcf4d7`, 298 at `0c926fdf` (S515–S525 added; ten `mined`, one `rejected`).

## Trend verdicts

- **expansion: improved** — a new admitted entry on ground the coverage map did not hold (hardware memory-failure
  kills, `knowledge/memory-failure-kills-r54.md`; README `## Round-54 coverage additions`), sourced from four new
  `mined` rows (S521–S524). All 21 rows are located and entailed, and the outside seat judged them correct. The two
  overbroad decision-table cells are routed for correction (defect 3), not left as accepted bar failures.
- **quality: improved** — the 31 remaining stale-by-release rows re-verify at v7.3 with their new start lines, and
  none fails. Ten C2 overclaims were caught and reworded before landing. Both round-53 closure defects (D2, D3)
  landed.
- **discernment: improved** — this spot-check agrees with the gate on all three admits and both rejects. The round-53
  closure disagreements (D2 stage citation, D3 lane-root strays) became grounded QUALITY criteria 148 and 149, each
  citing its round-54 lesson with a shown-able-to-fail check.

## SHONEN note (for the operator; promotion is operator-owned)

The four `[~]` boxes point at committed, re-runnable evidence (SKILL `## Round54`/`## Round53` tables, `LOG.md`
`## Round 54`, the three selftest receipts, the PROVINCE append and the entry's Boundaries). They look checkable by
a non-author. This closure writes no `[x]`.

## Routed defects (the lane fixes next round)

1. D1: re-capture `evidence/census-end.txt`-style receipts by redirecting the command's output (`… > file 2>&1;
   echo exit=$? >> file`), never by transcription; append a correction naming the round-54 receipt's S349 line.
2. D2: append a Gate correction (lesson or erratum) for the four wrong locator lines: S515 1850, S520 1409, S522 70,
   S525 3.
3. C2 decision table (`memory-failure-kills-r54.md:62,70`, `SKILL.md:1219,1226`): narrow the panic-switch cells to
   the code's trigger, `MF_MSG_KERNEL` ("reserved kernel page") with Ignored, and note that a high-order kernel page
   Ignored does not panic. Optionally say the per-node counters advance once per recovery action. Append-only
   correction rows.
4. D3: sweep `SCORECARD.md:2874` ("Ten control clone revisions") to 12/14 with an appended correction line.
5. D4: commit or ignore `.ufo/waves/round-54/w1.ready.dispatched` under a named entry.
6. D5/D6: correct the "four other seat reports absent" statement (73/74 present) and give the round-54 Mistakes rows
   the M1/M2 labels QUALITY 148/149 cite, both by appended correction.
7. Lane-planned and still open: durable control-tree witnesses (12/14 control revisions unresolvable), the C2
   voter-authenticity control, the four release-triggered artefacts outside C1's table scope, and the S508/S520
   superseding anchor rows.

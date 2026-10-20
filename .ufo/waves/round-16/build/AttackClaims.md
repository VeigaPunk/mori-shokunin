# Round 16 — AttackClaims (critic, author lane, not outside verification)

Seat `MoriR16.AttackClaims`. Scope: claim metric, causal scope and score inflation for C1
(exact-retained-anchor journal window). Read-time 2026-10-20T08:49Z–08:55Z against entering
HEAD `b83edc6`; working tree in flight (SCORECARD/LOG/PROVINCE/SKILL/QUALITY/README/SOURCES
modified; 16 fixture packs, knowledge note, lesson untracked; `tools/mori-journal-window.py` and
`tools/mori-round16-regressions.py` **absent at read time**). Findings about the tool and harness
are therefore requirements on them, not observations of their code.

Axes named: coverage (claim axis, 6), operability (7), calibration (5), depth (5), freshness (5,
r10 pin red), adjacency (6).

## Verdict summary

The declared claim text (SCORECARD r16, PROVINCE, README FR11, knowledge note, SKILL) is
mostly well-bounded. No pre-awarded score was found; the r10 red pin is preserved. The
risk is in the **metric**: as specified, the before→after number cannot fail for a reason
related to the capability, and the packs cannot tell a correct tool from two degenerate ones.
Five fixable defects and two tradeoffs follow.

## A1 — The before→after count is constructed, not measured (score-inflation risk) · HIGH

**Counterexample.** At entering `b83edc6` the tool is absent
(`.ufo/waves/round-16/frozen/entering-capability.json`: `cat-file -e` exit 128,
`capability_present:false`). Every case is `capability_absent`, so "failed before" equals the
number of authored cases. Any number of cases gives "N → 0". ClaimRubric already predicts
`F: 38 → 0` (`build/ClaimRubric.md:58-60,221`). The delivered universe at read time is **64**
cases in 16 packs, and none of them has ClaimRubric's S01–R28 IDs. The prediction does not
match the artifact, and the number grows with fixture volume.

**Evidence.** r15's `34 → 0` counted frozen controls that ran the old code and returned
CLEAN/rc0 while missing a wanted alarm (`round-15-verifier-spotcheck.md:107-111`). r16 has no
old behavior to run. The "before" column therefore carries no information about failure modes.

**Impacted axes:** coverage (verdict basis), calibration (a tally presented as a delta).

**Smallest correction.** Report the entering column as `capability_absent ×N (not a failure
count)` and do not use an arrow headline. The admissible numbers are delivered-only: pass/total
per arm (OK / UNAVAILABLE / SETUP), recounted from the delivered manifest. The universe must
be recomputed from the delivered packs, not taken from ClaimRubric's 38.

## A2 — Packs cannot discriminate degenerate implementations · HIGH

The packs were counted statically (no execution): **64 cases = 30 OK / 31 UNAVAILABLE /
3 SETUP**. Of the 34 rc2 cases, **0 pin a `reason`**. 30 have `want` `{}`/`null`/absent, and 4
(MalformedCapture) repeat only `finding_id`. 23 refusal cases contain positive-looking later
records (traps), but **no refusal case asserts that positive or count keys are absent**.

**Counterexamples** (inferred from pack wants, assuming the harness checks rc + `finding_id` +
the listed `want` keys):
- Stub X prints `{"finding_id":"MORI_JOURNAL_WINDOW_UNAVAILABLE"}` and exits 2. It passes all
  31 UNAVAILABLE cases (48%).
- Stub Y validates the anchor file, drops line 1 without comparing cursor or boot, and counts
  the rest with r15 predicates. It passes all 30 OK and all 3 SETUP cases (52%). This is exactly
  the "approximate seek treated as anchor" failure FR11 exists to refuse.
- Stub Z emits `positive_kernel_oom: 1` beside an UNAVAILABLE id on a trap case. It passes,
  because nothing checks absence. This violates the interface's "no numeric positive totals"
  rule.

**Impacted axes:** coverage (the claim's discriminating power), calibration.

**Smallest correction** (harness-side, no pack rewrite needed):
1. For every rc2 case, assert globally that stdout is one JSON object with no
   `records_after_anchor` and no `positive_*` key.
2. For every rc0 case, assert `evidence_basis == validated-record-subsets` and `scope` globally.
   Today they are asserted in only 13 and 12 of the 30 OK cases.
3. Either pin a stable reason per refusal case, or drop ClaimRubric §3.3(3) ("passes with its
   exact reason"). As written, that condition is unmeasurable by the delivered packs.
4. Report per-arm results so a reviewer can see that both degenerate stubs fail.

## A3 — The OK path's reachability on real journalctl is unmeasured by fixtures · MEDIUM-HIGH

**Counterexample.** Fixture wrappers encode two assumptions: that `journalctl --cursor=` is
inclusive, and that it re-emits the anchor's exact string as the first `__CURSOR`. Suppose
either assumption fails on host systemd 261.2. The opposite-direction risk is documented: the
host `man 3 sd_journal_test_cursor` says "the same entry might be referred to by multiple
different cursor strings, and hence string comparing cursors is not possible". In that case
every live run returns UNAVAILABLE, the capability never yields OK, and the gate stays 64/64
green. A fail-closed tool that cannot succeed still scores "coverage improved".

**Impacted axes:** coverage.

**Smallest correction.** Use the existing verdict vocabulary (QUALITY 21). Coverage gets
`improved` only if L1's single bracketed live read returns rc0 `MORI_JOURNAL_WINDOW_OK` from an
anchor taken via the same `-o json __CURSOR` path, on host `systemd 261.2-1`. Otherwise the
verdict is `unprovable-but-better`, qualified as fixture-contract only. Even a live OK proves
reachability for an entry in the active file only. It says nothing about rotation or vacuum,
which stay `[UNKNOWN]`. Docs cited are systemd 262 "latest"; the installed version is 261.2.

## A4 — "Continuity" wording overstates what is checked · MEDIUM

The gate proves the **start point**: the first record byte-equals the anchor. Later cursors are
only checked for uniqueness and same boot. Cursors are opaque (S014 `--show-cursor`: "private
and subject to change"), so seqnum gaps cannot and must not be checked. Silent partial access
under `-q` can also drop later records. The knowledge note says this correctly at `:63` and
`:88`.

The active wording is still too strong in two places:
- Goal / SKILL "exact retained cursor continuity" can be read as gap-free continuity.
- `corpus/QUALITY.md` 42 (in-flight) says cursors are "not comparable as strings, so continuity
  is claimed only from that observed exact match". That is self-contradictory as written: the
  gate *is* a string comparison.

**Smallest correction.** Say "exact anchor start-point (byte equality is sufficient, not
necessary)". Add "not gap-free" wherever "continuity" appears in active docs.

## A5 — Planner contradictions that would change predicates · MEDIUM

1. ClaimRubric §4 A2 proposes that integer `EXIT_STATUS: 9` is **not** positive. Both the r15
   predicate (`journal-positive-evidence-r15.md:113`) and census (`mori-census.sh:981-984`,
   "scalar string "9" or scalar number 9") accept it. Pack
   `ProcessSignal/killed-status9-numeric-scalar-vs-non-scalar` wants `positive_process_sigkill: 1`
   for numeric 9. Adopting A2 would silently break "uses r15 predicates". Reject A2 and keep the
   r15 predicate.
2. The dispatched PackUnitOom prompt (`wave1-spec.json`) names the unit-failure ID
   `d9b373ed55a64e6c8e2e7d70a0fce472`. The census authority is
   `d9b373ed55a64feb8242e02dbe79a49c` (`mori-census.sh:916,1036`). The pack author used the
   correct ID; every `d9b373ed…` in all 16 packs is the census value. This is a planner-text
   defect neutralized by the "hints not authority" clause. It should be recorded so the wrong ID
   cannot be copied into active docs.

**Impacted axes:** calibration (predicate provenance) and depth.

## A6 — Tradeoffs (disclose; not defects the judge must reject)

- **Causal scope of the "FR11 advance".** Only the consumer half exists. No production writer of
  `mori-journal-anchor-v1` exists, and anchors are "operator-retained" (PROVINCE). PROVINCE's FR11
  remainder already lists persisted/advanced cursor state. README's FR11 row does not, and should
  add "anchor creation/retention not built".
- **Anchor boot is not checked against the current boot.** "Same-boot" means the anchor's boot,
  not the current boot (no `/proc/sys/kernel/random/boot_id` read is specified). An OK window can
  end before the current boot if later files are inaccessible. Active text must not import r15's
  "current-boot" wording for these counts. None found at read time.
- **Token naming.** `positive_kernel_oom` counts systemd's `fe6faa94…` unit-OOM *notice* (S013),
  not kernel `_TRANSPORT=kernel` records. The name is inherited from r15. Keep "notice, not victim"
  next to every citation.
- **Pack-label precision.** `KernelUser/kernuser_oom_before_anchor_only` places the OOM in the
  anchor record itself, not before it; the behavior is fine. The SETUP arm has 3 cases, all
  anchor-field cases. Missing anchor path, non-JSON anchor, wrong schema, control-character or
  >4096-byte cursor and bad `--timeout`/`--max-bytes` are not exercised. Do not cite SETUP as
  covering the whole argument surface.

## No-harm cross-check (static, read-time)

- SCORECARD r16 claims no score increase and keeps r10 drift red. LOG states that capability
  absence is not a defect count. Census bytes are pinned in `entering-capability.json`
  (`f1f8d1b6…`), matching the r15 delivered SHA.
- The capability-absent exit rc1 is folded with real mismatches (SKILL r16 registry row). The
  outer `1 → 0` exit must not be cited as behavioral red→green; cite manifest statuses
  (`capability_absent` versus `fail`) instead.

## Seat conduct disclosure

- **Static reads only:** `git status`/`diff`/`log`, the round-16 JSON and corpus files, `zcat` of
  local man pages (`sd_journal_seek_cursor.3`, `sd_journal_test_cursor.3` → `sd_journal_get_cursor.3`,
  `sd_journal_seek_head.3`, `journalctl.1`), and `pacman -Q systemd`, a read-only package-DB query
  (not a transaction).
- In-kernel Python counted fixture JSON. No tool, harness, census, selftest or gate was executed.
- No journalctl query and no network fetch.
- No writes except this report. Nothing written to `/tmp`. No installs.
- One static `ls`/`git status` call was auto-backgrounded by the shell before L1's
  no-background-jobs clarification arrived. It completed and was cancelled immediately; no probe
  was involved.

# ReviewEvidence — mori round 13 (wave `mori-r13-build`)

Seat: `MoriR13.ReviewEvidence` (reviewer, leaf). Axes: coverage, operability. Milestone: round13 structured scopes and verdict integrity.
Scope: evidence protocol, gate protocol, committed snapshot/digest needs, and the planned evidence harness. Read-only. No build, selftest, oracle, lint, format or smoke run was executed (wave rule). Tools installed or updated: none.

## 0. Observation basis

Read-only inspection (`read`, `grep`, `sed -n`, `stat`, `sha256sum`). Times are UTC.

| Artifact | Observed | Note |
|---|---|---|
| `tools/mori-census.sh` | sha256 `3da5b098dc23aeb3e1c31ce82664b24a22c2847a168308a755525593881b3164`, 3041 lines, mtime 2026-10-19 20:15:19 -0300, `VERSION=census-r5` (`:243`) | Equals the r12 roster census SHA in `corpus/knowledge/roster-truth-r12.md` header. No CensusFix write observed. |
| `tools/mori-silence-cases.sh` | First read: sha `448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5` (matches audit-r11 §1 and `drift-pin-r10.md:14`). Later read in this review: sha `b6a39d911fb98ac6be52b2d6d583a3e984ef76db957ec8ca1e3a9c1e6179592d`, mtime 2026-10-20 01:08:26 -0300 (04:08:26Z) | **The "byte-frozen" oracle is no longer frozen.** OracleFix is editing it in this wave. `verdict_grade` is at `:552-581`, wired at `:619`, `:999`, `:1050`, `:1055`. Commit state was not read. |
| `corpus/evidence/baseline-r10-20261015T2231Z.json` | sha `0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478` (matches audit-r11 §1) | Header `census_sha256=d7710981…`. Text format despite `.json` suffix. |

Consequence: every "current bytes" statement in the round-12 record (`d7710981…`, `448f7723…`, `3da5b098…`) names a different state than the bytes now on disk for the oracle. Receipts for round 13 must bind to committed SHAs, not to the working tree.

## 1. Findings (ordered by severity)

### E1 — High · coverage + operability · The journal probe publishes a command that is not the measurement, and reads MESSAGE into a variable

- `tools/mori-census.sh:855` sets `cmd="$JOURNALCTL_BIN --user -b --no-pager"`, which is published verbatim as `cmd=` at `:911`. The counts do not come from that command alone. They come from:
  - text greps over the MESSAGE-bearing text at `:874-875`, `:881`, `:890`;
  - a second query, `cap … --user -b --no-pager -o json COREDUMP_SIGNAL=11` at `:883`, which is absent from `cmd=`.
- `:883` requests JSON with no `--output-fields=`. Every field, including `MESSAGE`, is written to `CAP_OUT`. This conflicts with `SKILL.md:143-146` ("never capture journal output into a variable") and `corpus/knowledge/kill-classes-by-message-id-r12.md:33`.
- `:240` and `drift-r12-20261019T2204Z-classification.md:70-74` record that re-running the published `cmd=` prints MESSAGE text. The published provenance string is therefore unsafe to hand to a reader.
- `:876-880` documents that segfault counts were moved to `COREDUMP_SIGNAL=11` because text grep returned 0 against 656 records. The emitted id `SEGFAULT_JOURNAL class=segfault` (`:902`) still names the text class. It counts coredump records (`fc2e22bc…` class), not segfaults. This fails QUALITY criterion 14 (counter semantics cite the increment site).
- `--user` cannot contain kernel `Killed process` records. Those are in the system/kernel journal: 5 kernel records vs 7 user + 9 system `fe6faa94…` notices in boot `7bd93aee…` (`kill-classes-by-message-id-r12.md:6`). The current `OOM_KILL_JOURNAL … scope=user` (`:894`) with severity `crit` is a user-unit notice count presented as an OOM-kill class. Under C1 this must be labelled `unit=notice`. It must never be read as a kill total.
- Boot-scope trap: the census uses `-b` (current boot, `:855`). The kill-classes counts are all-boot (no `-b`) and the kernel records are from `7bd93aee…`, not the current boot (`uptime -s` → 2026-10-19 08:11:44 per `drift-r12…:31-63`). Any round-13 row must print `boot=current` (or the explicit boot id) next to each count (QUALITY 12, 16).

Proposed checks (not run):
- `grep -nE "grep -ci|--no-pager|-o json" tools/mori-census.sh` after the change. Expect no text-class counting and no `--no-pager` in journal probes.
- Fixture with a stub `journalctl` whose output includes a `MESSAGE` field. Assert the census output contains no `MESSAGE` text and that the stub received `--output-fields=` on every JSON call.
- For every committed receipt log: `grep -c '"MESSAGE"' <log>` = 0 and `grep -c 'MESSAGE=' <log>` = 0.

### E2 — High · verdict integrity (F02) · The admitted grammar checks digits only, tallies are unchecked, and the grader has no direct negative tests

- `tools/mori-silence-cases.sh:562` `VERDICT_RE` accepts any digits for `findings= drift= unavailable= surfaces=`. `verdict_grade` (`:563-581`) checks count (missing/duplicate), line shape, and word↔rc (`CLEAN:0`, `DRIFT:1`).
- Not asserted: `findings=N` vs the number of `^FINDING ` lines; `drift=M` vs the number of drift-state rows; `surfaces=S` vs `^SURFACE ` lines. Tally-corruption passes the grammar. This matches D02 in `audit-r11.md §5` ("tally-corruption mutants must fail").
- `verdict_grade` is exercised only through live census output in four paths (`:619`, `:999`, `:1050`, `:1055`). No fixed synthetic-input table exercises it with missing, duplicate, `BANANA`, rc-mismatch, or tally-corrupt input. Without that, "rejects invalid verdicts" is asserted by the live path only.
- The audit's Appendix C proxy (`audit-r11.md:382-391`) is the regression. At the pre-fix oracle it gave `matched=28 total=28`, exit 0. The expected post-fix gradient is `MORI_SILENCE_CASES: matched=0 total=28`, exit 1.

Proposed checks:
- Synthetic table for `verdict_grade`, with pre-registered expected outputs: `missing`; `duplicate (2 lines)`; `malformed` for `BANANA`; `inconsistent` for `CLEAN` with rc 1 and `DRIFT` with rc 0; `ok` for the honest pair.
- Decide and state whether tally arithmetic is in scope. If it is, add the cross-checks above and mutants `findings=999` and `drift=0` with a DRIFT line. If it is not, name it as a residual: "well-formed" means grammar-well-formed only.
- Appendix C wrapper re-run at the committed oracle SHA: expect exit 1.

### E3 — High · pointer integrity (QUALITY 9) · The audit's F01 anchor does not resolve at current bytes; several active pointers are stale

- `audit-r11.md` §4 F01 cites `tools/mori-census.sh:1366-1374` for the `printf … | sed … | grep -Fxq` pipeline. At `3da5b098` those lines are `ps_walk` and `ps_report_closed` (`:1359-1387`). The real pipeline is `:1490-1494`: awk capture at `:1490-1491`, the `printf … | sed … | grep -Fxq -- "$lane-shokunin <$lane@shokunin.local>"` consumer at `:1494`.
- The `grep -Fxq` consumer exits at first match while `printf` may still be writing. That is the QUALITY 7 class. With the 12,000-line Appendix B history it is the F01 mechanism.
- Other stale pointers: `drift-pin-r10.md` cites `:1636-1647`, `:1795-1878`, `:2722-2798`. At `3da5b098` `DRIFT_COUNTER_KEYS` is at `:1763` and `DRIFT_VOLATILE_LIST` at `:1775`. `corpus/evidence/README.md:9-10` cites `main()` at `:880-895`. The `SKILL.md:66-68` gate registry gives counts (77 selftest cases, 28 oracle cases) that round 13 will change.
- The Appendix B observed output (`audit-r11.md:364-370`) was measured at `d7710981…`. It is not evidence at the round-13 bytes.

Proposed check: for every `path:N-M` pointer in the round-13 report, `sed -n 'N,Mp' <path>` at the carrying commit must contain the quoted token. Record the commit and the pointer list.

### E4 — High · drift baseline honesty (QUALITY 10, 13) · The adopted baseline is already red at the shipped bytes, and the r12 classification was measured on the wrong bytes

- `drift-r12-20261019T2204Z-classification.md:3,11` states that the drift run used a copy of `20e2255:tools/mori-census.sh` at `d7710981…`, "not the concurrently edited LANE script." The shipped census is `3da5b098…`, which adds the roster fields.
- Observed difference: the silence row emitter at `tools/mori-census.sh:1571` writes `roster_source= roster_n= conf_n= state_n= conf_dropped_n= state_dropped_n=`. The baseline silence row (`baseline-r10…json:22`) has none of these fields. Its `silent=…` tail is the only shared text. Under the masked-list rules these fields are not volatile. `--drift` at `3da5b098` will therefore name them as changed, and will name `+FINDING:ROSTER_SET_MISMATCH` (info) if conf and state sets differ (`roster-truth-r12.md:21`). This is an inference from the code and baseline lines; it was not run.
- The round-12 classification (11 tokens, `rc 1`) does not cover this. It describes the `d7710981` bytes.
- The baseline header records only `census_sha256`, `pinned_ts` and `volatile_fields` (`baseline-…json:2-4`). It does not record host, derivation window, environment shape, or oracle/gate SHA. QUALITY 10 requires all of these.
- The filename `…json` is a naming defect. The content is `mori-drift-baseline v1` text (`drift-pin-r10.md:202-205`).

Recommended honest handling for round 13:
1. Before any round-13 change is merged, take one `--drift` "before" receipt at the head bytes and classify every token against `baseline-r10-20261015T2231Z.json`. Name the `roster` and `cmd=` tokens explicitly. The r12 classification must not be cited as the round-13 before-state.
2. Pre-register the expected after-gradient in the round record before the census change lands (QUALITY 13). Expected token families: `SURFACE journal` key names and `cmd=` text; the `-FINDING:` / `+FINDING:` rows for the retired and new journal ids; the `VERSION` token in the header line; `silence` roster fields; `+FINDING:ROSTER_SET_MISMATCH` when applicable; live-state tokens treated as baseline aging (`other_authored_commits`, `WAVE_UNSETTLED_AGE` ids).
3. Re-pin is a new artifact, `corpus/evidence/baseline-r13-<YYYYMMDDTHHMMZ>.txt`, pinned at the committed census SHA with a reason line. The r10 file is not rewritten. Its `.json` misnomer is recorded in the round record, not silently renamed.
4. The r13 baseline round record must carry host (`uname -r`), derivation window, the MORI_* override set (expected: none), oracle SHA and the pin's `census_sha256`. The census `--pin` header cannot carry oracle SHA; the round record must.

### E5 — Medium-High · snapshot/digest needs (QUALITY 23, 22, 9) · The harness and receipts need committed generators, digests and commit-bounded timestamps

- `tools/mori-round13-regressions.py` does not exist yet. Its fixtures are Appendix B (`audit-r11.md:315-362`) and Appendix C (`:382-391`). Both currently live only as text in a /tmp-based report. Appendix B writes `mkdtemp(dir='/tmp')`, and Appendix C is a /tmp wrapper.
- QUALITY 23: a /tmp path is never evidence. The generator must be committed, and the receipt must carry a digest manifest (sha256 of every generated fixture file, of the census, oracle and harness). Appendix B's fixture bytes are deterministic (fixed `watchdog.log` `ts=1699998000`, `utime`, fixed `MORI_NOW_EPOCH=1700000000`). The directory path is not deterministic. Assertions should therefore be token-level, not byte-equal, and the receipt should name the path mask.
- Appendix C's wrapper is a negative control, not a verdict source. Commit it as a named control file (e.g. under the harness), and label its expected gradient as a control, not a census result.
- QUALITY 22: each `CAPTURED_UTC` must be ≤ the carrying commit's `%cI`. Round 12 already had label drift of 1–3 minutes (`audit-r11.md` F11). Capture clocks must come from `date -u` at capture time.
- Harness output should follow the existing convention: a single summary line and an exit code, with setup failure distinct from a case FAIL (QUALITY 6; `audit-r11` D21 / M25). The round-12 evidence README pattern (`Receipt-file SHA-256 at build time`) should be reused.
- No round-13 receipt index exists yet in `corpus/evidence/README.md`. Round-12 receipts (`roster-r12-*`, `drift-r12-*`) pin `3da5b098…` and `448f7723…` (oracle). They stay valid for those SHAs only. They are historical after round 13 and must be labelled as such, not overwritten.

Proposed commit-bound artifact set (names; no content yet):
- `corpus/evidence/<gate>-r13-<UTC>-before.log` — captured from HEAD bytes before merge. The oracle's HEAD SHA must be checked first: `git show HEAD:tools/mori-silence-cases.sh | sha256sum` should equal `448f7723…`. This is a git read by L1, not by this seat.
- `corpus/evidence/<gate>-r13-<UTC>-after.log` — at the final committed SHAs. Header lines `CENSUS_SHA256_BEFORE/AFTER`, `ORACLE_SHA256_BEFORE/AFTER`, `HARNESS_SHA256`, `COMMIT`, `CAPTURED_UTC` (QUALITY 9, 22).
- `corpus/evidence/baseline-r13-<UTC>.txt` (E4).
- `corpus/evidence/round13-manifest.json`-style or text digest manifest listing every committed receipt and tool SHA (QUALITY 23).

### E6 — Medium · scope and boot labelling (QUALITY 12, 16, 17, 18) · New structured rows need explicit unit, scope, boot and blind-spot fields, and denied must never read as empty

- Each new row must carry `unit=notice|kernel-record`, `scope=user|system`, `boot=current` (plus the boot id), and an explicit `blind=` list. Required blind-spot entries: no kernel `-k` records (out of C1 scope), no catalog-less kill paths, no delivery path that writes no journal record (QUALITY 17: `S020` probes only `kill/tkill/tgkill`; `kill-classes-…:33`).
- Denied vs empty: `tools/mori-census.sh:868-872` treats `rc 0/1` as acceptable ("1 can mean empty on some builds"). rc 1 cannot distinguish "no records" from "permission denied", and `--system` access is permission-dependent. Under C1 the system scope needs `unavailable reason=rc-N` (or `denied`) for every nonzero rc, and `count=0` only for rc 0 with a readable journal. Pre-register: a stub returning rc 1 with a denial message must grade `unavailable`, never `count=0` (QUALITY 24; `audit-r11` D21).
- Counter baselines (QUALITY 12): the counts are cumulative within a boot. Print the boot id beside them. Do not make the boot id volatile; a boot change should show as drift.
- Never sum scopes (QUALITY 16). No combined "kill count" row is admissible. The user and system counts are separate ids.

### E7 — Medium · finding naming (QUALITY 15, 16, 19) · Current ids name kills and segfaults for things they do not count

- Current ids: `OOM_KILL_JOURNAL` (`:894`), `KILL_SIGNAL_JOURNAL` (`:898`), `SEGFAULT_JOURNAL` (`:902`), `UNIT_FAILURE_JOURNAL` / `UNIT_FAILURE_OUT_OF_SCOPE` (`:905`, `:908`).
- After C1 these ids would count notices (`fe6faa94…` per unit), coredump records (`fc2e22bc…`), and oomd notices (`d989611b…`). The names "kill" and "segfault" overstate them. Recommended: retire the four ids and name new ids by unit and scope. Examples: `JOURNAL_NOTICE_OOM_USER`, `JOURNAL_NOTICE_OOM_SYSTEM`, `JOURNAL_COREDUMP_SYSTEM`. The exact names are a design choice for CensusFix, but each id should say "notice" or "record", and never "kill" unless it is a kernel victim record (which C1 does not probe).
- Severity: the spec says "notice units, never fleet-caused kill counts". `crit` on a notice count contradicts that. The round record must state the severity mapping and why.
- Retired ids produce `-FINDING:` rows at the next drift run. That is the honest signal. Do not keep the old ids as aliases (contract: no shims).

### E8 — Medium · claim scope (QUALITY 25, FR1) · The admissible claim is narrower than the spec's phrase "structured kill counts"

- Admissible if measured: user- and system-journal **notice** counts by catalog `MESSAGE_ID`, current boot, count-only, with the blind-spot list.
- Not admissible: kernel OOM attribution (`kernel-oom-line-attribution-r12.md`), fleet-caused kills, kill totals, any cross-scope sum, and any claim that `fe6faa94…` notices equal victims (`kill-classes…:24`).
- FR1 (`corpus/README.md` Frontier row) remains open. FR1's own boundary text says "a host event alone does not prove a fleet-caused kill." Round 13 only advances its first half. The round record should say so, or it will read as closing FR1.
- Measured-vs-claimed: the r12 knowledge counts (5/7/9) were taken without `--output-fields` discipline on one host, one boot. They are host observations. The round-13 claim should cite its own run, not those counts.

### E9 — Medium · measurement revision naming (QUALITY 9, 10) · `VERSION=census-r5` is not a revision identifier

- `census-r5` is the label of at least four distinct census SHAs in the corpus: `390ab9cd…` (`corpus/README.md:16`, 2380 lines), `1c49238a…` (`corpus/README.md:17`, "a revision of census-r5"), `d7710981…` (`drift-pin-r10.md:4-5`, "VERSION still census-r5"), `3da5b098…` (`tools/mori-census.sh:243`). Other labels (`census-r1` … `census-r7`) appear with inconsistent meanings across `.ufo/round-*` and `corpus/knowledge`.
- Recommended for round 13: bump `VERSION` to `census-r6` in the same commit as the behavioral change. Identify every revision by `census_sha256` plus `VERSION`. Do not rewrite historical labels (QUALITY 4).
- Side effect, which is the honest one: the `VERSION` token is in the unmasked header line of the canonical block (`drift-pin-r10.md:§2`, baseline line 7). The bump appears as drift. Name it in the re-pin reason.
- Oracle revision: no version token exists. Name the oracle by SHA only, and do not add an in-band version line unless the oracle's own grammar test accepts it.

### E10 — Low-Medium · operability of the gate recipes · Environment and invocation must be fixed

- The drift pin records no environment (`drift-pin-r10.md:169-177`). A `MORI_*` override, notably `MORI_ROSTER_LANES` or a changed `MORI_STATE_DIR`, reads as drift. Round-13 pin and drift must use the same invocation, and the round record must list the invocation. The recipe should set `env -i`-style explicit values for the MORI_* set rather than inherit the caller's environment, provided that is compatible with the census's own env contract.
- `MORI_SHOKUNIN_ROOT` must be set in the recipe (`corpus/knowledge/drift-pin-r10.md:297-298`, erratum: `MORI_SHOKUNIN_ROOT=<fleet root> bash tools/mori-census.sh --drift …`). Without it the census may resolve a different root.

### E11 — Low · Safety boundary in the evidence itself

- The round-13 receipts and this review contain no MESSAGE, process-environment, or credential material. Keep it that way: receipts should contain counts, finding lines and token-level excerpts only. Add the count check from E1 to the L1 battery.

## 2. Pre-registration checklist for L1 (to be run once, by L1 only)

These are proposed. This seat has not run them.

1. Freeze the before-state from HEAD bytes: census `3da5b098…` (or the committed successor), oracle at HEAD. Record SHAs and `CAPTURED_UTC`.
2. `--drift` against `baseline-r10-20261015T2231Z.json` at the before-state. Classify every token; the classification replaces the r12 classification as the before-state record.
3. Synthetic `verdict_grade` table (E2). Expected results pre-registered.
4. Appendix C wrapper against the new oracle: expect `matched=0 total=28`, exit 1.
5. Appendix B fixture against the new census: expect `RC=0`, `SURFACE lane.kagi: progressing` (not `progressing-weak`), `MORI_CENSUS: CLEAN`. Also a sibling-only negative control: expect `progressing-weak`.
6. Journal stub tests: (a) MESSAGE-bearing stub output never appears in census output; (b) rc 1 + denial text grades `unavailable`; (c) `count=0` only from readable empty output.
7. Pointer sweep (E3), timestamp sweep (E5), `census-r5` label sweep (E9), count sweep from delivered files (QUALITY 20) for `SKILL.md:66-68`, `corpus/README.md`, `corpus/knowledge/drift-pin-r10.md`.
8. Re-pin `baseline-r13-<UTC>.txt` only after 1–7 pass. Record the reason line and the diff against the before-state.
9. Each committed receipt: `grep -c '^MORI_CENSUS:'` = 1; `grep -c '"MESSAGE"'` = 0.

## 3. Residuals and verification gaps (this seat)

- Not run: no build, selftest, oracle, harness, census, drift, or journal query. All observations are file reads, `stat`, `sha256sum`, and `grep`/`sed` on source and committed text.
- Not read: git HEAD, commit timestamps, and whether the working tree matches any commit. The `448f7723…` oracle identity is taken from audit and drift-pin text, not from a commit lookup.
- Not read: `tools/mori-round13-regressions.py` (does not exist), `corpus/knowledge/structured-journal-scopes-r13.md` and `verdict-contract-r13.md` (not yet written), S013/S014/S015 sources (other seats), the selftest body (CensusFix owns it), and any live journal.
- Inference, not measured: E4's roster token list (derived from `:1571` and baseline line 22 without a run); E2's tally-arithmetic gap (derived from the regex, not from a fixture); E5's path-token masking approach (design, not tested).
- The census and oracle are in flux during this wave (E-basis table). Any finding here that cites a line number may move when CensusFix or OracleFix land. Re-resolve before citing.

## 4. Summary for L1

- The round-13 evidence plan is sound in direction (structured counts, scope labels, verdict grammar). It is not yet commit-bound: no before-state, no pre-registered gradient, no committed generator or digest manifest, and a stale pointer for F01.
- The largest honesty risks are: (1) the published `cmd=` and the `-o json` query without `--output-fields`; (2) rc-1 treated as empty; (3) `census-r5` reused across four SHAs; (4) an already-red baseline whose r12 classification describes older bytes; (5) an oracle whose "frozen" SHA changed during the wave.
- Name revisions by `census_sha256` + `VERSION=census-r6` (bumped with the behavior change), by oracle SHA, and by committed receipt set `*-r13-<UTC>-{before,after}.log`. The re-pin is `baseline-r13-<UTC>.txt`, a new artifact with a recorded reason.

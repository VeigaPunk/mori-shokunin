# HistoricalCorrections — round-13 routed mori defects (audit, report only)

Seat: `MoriR14.HistoricalCorrections` (leaf; no delegation, no builds/tests run, no commits, no edits outside this file).
Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Milestone: restore OOM alarm and structured fleet routing. Axis: coverage.

Snapshot audited (observed 2026-10-20T05:57Z): HEAD `a5cc313` (round-14 pin commit, touches only `.ufo/waves/round-14/`). Round-13 delivered revision `c13df48`; `tools/mori-census.sh` and `tools/mori-silence-cases.sh` last changed at `18d7d55` and are byte-identical at HEAD (sha256 `39abda0a…3985` for the census, `34cd5770…1abfa` for the silence oracle). Working tree is concurrently dirty from round-14 sibling seats (LOG, SCORECARD, PROVINCE, QUALITY, SOURCES, audit-r11, structured-journal-scopes-r13, verdict-contract-r13, corpus/README, `corpus/lessons/round-14.md`). Findings below are against that observed state; sibling-uncommitted text is labelled as such.

Source of the six defects: `corpus/lessons/round-13-verifier-spotcheck.md:132–137` (routed items 1–6; item 7 is operator/SHONEN and out of scope).

Tooling: none installed or updated by this seat. Reads only (`read`, `grep`, `git show`/`git log`/`git status`/`sha256sum`, `jq` on committed evidence).

---

## 0. Checklist summary

| # | Routed defect (spotcheck line) | Repair files | Criteria | Historical attribution | Status observed |
|---|---|---|---|---|---|
| 1 | Restore OOM warning/DRIFT with structured metadata; account for unit-result oom-kill/signal paths and cgroup-counter scope (:132) | `tools/mori-census.sh` `probe_journal` :1031–1130 and `probe_cgroup` :1133–1316 (`LOCAL_EVENTS` :1158, `SERVICE_EVENTS` :1159, CGROUP_OOM_KILL :1297); `tools/mori-census.sh` selftest journal block :2750–2792 and cgroup block :2864–2867, env wiring :2431–2433; harness `tools/mori-round13-regressions.py` claims `R13_C1_CLEAN_VERDICT`, `R13_C1_SYSTEM_NOTICE_COUNTS`; `SKILL.md` :17, :28–31 | QUALITY 14, 16, 18, 12; (working tree) 29 | OOM crit: `7ca17b1` (r1, text class); removed `18d7d55` (r13); receipts at `c13df48` | **Open.** No OOM alarm at HEAD. Cgroup path prefers parent-slice `.local` (see §1c). |
| 2 | Preserve fleet/non-fleet unit split and tsukuroi owner routing via sourced structured unit metadata; do not reuse `UNIT_FAILURE_JOURNAL` for a new universe (:133) | `tools/mori-census.sh` `probe_journal` :1026–1027, :1101–1102; selftest :2769, :2788–2790; `SKILL.md` :17; `corpus/knowledge/structured-journal-scopes-r13.md` (S035–S037 rows in `corpus/SOURCES.md:41–43`) | QUALITY 15, 16, 17; (working tree) 30 | Split: `486a4e3` (r1); removed `18d7d55` (r13) | **Open.** Frozen fleet split read MESSAGE text; current id reuse covers all user units. |
| 3 | Correct "no-anchored-structured-field" to separate unimplemented structured classes from events with no record; annotate retired GPF/text and general-signal coverage (:134) | `tools/mori-census.sh` :1041, :1127 (reason string), :1067–1068 (segfault), :1070 (signal), :1102 | QUALITY 15, 17, 8; Q3/Q17 per round-14 lesson | Reason string: `18d7d55`; GPF text: `7ca17b1`; COREDUMP switch: LOG.md:38–44 | **Open.** GPF text retired silently; `other_signals` / `other_unit_failure_text` described categorically. |
| 4 | Register the verdict-producing r13 harness per PROTOCOL; retain measured selftest on delivered revision; 24/24 at 80bd58a is not c13df48 (:135) | `SKILL.md` :58–68 registry; `tools/mori-round13-regressions.py` docstring :4–8, summary :1799, print :1813; evidence `.ufo/waves/round-13/evidence/regression-selftest*.json`; `/home/vgpnk/Projects/shokunin/PROTOCOL.md` :375–400 | PROTOCOL §Gate standard (Verdict, Self-test, Two evidences, Registry); (working tree) 31 | Harness first added `18d7d55`; last code change `c13df48`; selftest receipts at `18d7d55` (23) and `80bd58a` (24) | **Open.** Not registered; no selftest receipt at `c13df48`/HEAD. |
| 5 | Qualify F01 whole-function reversal and F02 reconstructed shim wherever "exact-locus" reads as original-byte restoration; keep original-frozen before evidence primary (:136) | `corpus/knowledge/verdict-contract-r13.md` :252, :270–283; `corpus/knowledge/structured-journal-scopes-r13.md` :87, :123–125; `SCORECARD.md` :679–690 (HEAD :685); `corpus/lessons/round-13.md` :32,100–102 (superseded by round-14 entry); harness `R13_MUTATION_F01/F02` and mutants in `regressions-accepted/mutants/` | QUALITY 25, 32 (working tree); round-14 lesson M5 | Mutation receipts `c13df48` (`regressions-accepted`), `80bd58a` (`regressions-after-final`); frozen before `80bd58a` (`regressions-before-final`) | **Partly done (uncommitted).** Knowledge files qualified in working tree; `SCORECARD.md:685` still says "exact-locus negative witnesses" without qualifier. |
| 6 | Finish correction sweep: `corpus/README.md:32–33` index cells, `QUALITY:32` quote qualifier; do not rewrite append-only lessons (:137) | `corpus/README.md` :32–33, :37, index row for `journal-alarm-routing-r14.md`; `corpus/QUALITY.md` :31–33; `corpus/knowledge/kill-classes-by-message-id-r12.md` :1, :17, :38; `corpus/knowledge/kernel-oom-line-attribution-r12.md` :17, :37 | QUALITY 9, 16; round-14 lesson M6 | Index cells from `1f07f1d`/`18d7d55`; in-file correction sections already at `18d7d55` | **In progress (uncommitted).** Working-tree README and QUALITY edited; HEAD still shows misleading cells. Index row points at a file that does not exist yet. |

Verdict on the audit: all six routed defects are real and still open at HEAD `a5cc313`. Defects 5 and 6 are being repaired in the working tree only; defects 1–4 have no repair in the census, harness, or SKILL.md at HEAD.

---

## 1. Defect 1 — OOM critical alarm lost (spotcheck :132; :84–85)

### 1a. Frozen behavior (pre-cutover, `6531ac6`, `.ufo/waves/round-13/frozen/mori-census.sh` = sha `3da5b098…3164`)
- `tools/mori-census.sh@6531ac6:853` header: "DRIFT on oom_kill>0 or kill_signal>0 (mint demand)".
- `:874` text count `Out of memory|oom-kill|oom_reaper|Killed process` over `journalctl --user -b` text (MESSAGE text).
- `:894` `emit_finding OOM_KILL_JOURNAL crit "class=oom_kill count=… scope=user"`, then `st=drift` (DRIFT).
- Introduced by `7ca17b1` (round-1, "land the observability census gate"). Removed by `18d7d55` (round-13).

### 1b. Current behavior (HEAD census bytes = `18d7d55` bytes, sha `39abda0a…3985`)
- `tools/mori-census.sh:1034` class list is `kernel_oom_notice oomd_notice coredump_notice segfault_signal11 unit_sigkill_record unit_failure_record`. No OOM text class exists.
- `:1094–1095`: every class is `sev=info` except `user:unit_sigkill_record` (`sev=warn`). A positive kernel-OOM notice (`fe6faa94…`) is INFO and cannot DRIFT by itself.
- `:1041` and `:1127`: OOM text, "other signals", "other unit failure text" are only listed as `unmeasured=`.
- Accepted C1 harness claims encode the demotion: `tools/mori-round13-regressions.py` docstring :14 (`R13_C1_SYSTEM_NOTICE_COUNTS`) and :18 (`R13_C1_CLEAN_VERDICT: notices INFO => exactly one CLEAN/rc0 roll`). The accepted receipt (`.ufo/waves/round-13/evidence/regressions-accepted`, measured `c13df48`, exit 0, 19 pass + 2 mutation-red) therefore certifies the harmed behavior. Those expectations must be inverted for a positive OOM fixture, not merely left green.
- The census selftest's journal positive case (`tools/mori-census.sh:2750–2771`, `journal-system-kernel_oom` ×5) expects `KERNEL_OOM_NOTICE_JOURNAL_SYSTEM … count=5` and `^MORI_CENSUS: DRIFT ` only because of the user SIGKILL; it does not assert an OOM alarm.

### 1c. Cgroup counter scope (the second half of :132 and spotcheck :85)
- `tools/mori-census.sh:278`: `CGROUP_EVENTS` default is `/sys/fs/cgroup/user.slice/user-$(id -u).slice/memory.events` (the **parent user slice**).
- `:1158`: `LOCAL_EVENTS = ${CGROUP_EVENTS%.events}.events.local` → the **parent slice's** `memory.events.local`.
- `:1159`: `SERVICE_EVENTS = …/user@$(id -u).service/memory.events` (the session service, where fleet processes live per the comment at `:1146–1150`).
- `:1161–1165`: `SERVICE_EVENTS` is consulted **only when `LOCAL_EVENTS` is absent or unreadable** (`elif`). Where the parent `.local` file is readable, the probe reads it and does not read the service file. The service fallback is therefore valid only when the local file is absent; it is not a substitute for a readable local file.
- `:1296–1297`: `CGROUP_OOM_KILL crit` fires only on the value read from `LOCAL_EVENTS` (path printed in the finding).
- Recorded measurement (`corpus/knowledge/observability-census-r1.md:131–140`, erratum 3): the parent slice's `.local` reads 0 while the parent's cumulative count shows a service-scope event. `memory.events.local` counts only kills charged to that cgroup itself and carries no descendant guarantee. Consequence, narrowed: a selected readable parent `.local` file does **not guarantee** that a kill inside `user@UID.service` raises `CGROUP_OOM_KILL`. This is a scope limit of the selected file, not a proof that the fallback is unreachable on every host. Spotcheck :85 raises the same concern. Existing cgroup behavior outside C1 scope is not modified by this report.
- Selftest gap: `tools/mori-census.sh:2432–2433` sets `MORI_CGROUP_SERVICE_EVENTS` and `MORI_CGROUP_LOCAL_EVENTS` to the same fixture file. The 91 cases cannot distinguish which scope is read, so the scope choice is unverified by any committed case. Fixture `:2864–2867` only proves that a counter in the fixture file produces `CGROUP_OOM_KILL`.
- The round-14 working-tree lesson M-table (`corpus/lessons/round-14.md:29`) rejects "cgroup local counter substitutes for all journal OOM alarms". That is the correct criterion; the census cgroup path is a separate gap.

### 1d. Criteria mapping
- QUALITY 14 (counter semantics cite the increment site): `S003 :935–936` (`kernel-oom` counter moves only at kernel victim site).
- QUALITY 16 (kill vs notice, scopes not summed): the restored alarm must name the notice unit and scope.
- QUALITY 18 (event-time attribution, never re-read victim cgroup).
- QUALITY 12 (cumulative counter printed with its baseline): `memory.events` counters are cumulative; the current row prints only `local_oom_kill=`.
- Working-tree QUALITY 29 (no-harm equivalence: same fixture, same id, severity not lower, same roll effect). Not yet committed.

### 1e. Repair targets (for the implementing seat; not implemented here)
- `probe_journal`: add a structured kernel-OOM positive path that emits `OOM_KILL_JOURNAL` at crit with DRIFT (scope-named, `trust=client-supplied`, `attribution=none`), keyed on `MESSAGE_ID=fe6faa94…` / `_BOOT_ID` validated. Do not reintroduce `MESSAGE` text (QUALITY 15).
- `probe_cgroup` (**outside C1 scope; not to be modified by this round**): any change of which cgroup file is selected is a separate cgroup decision. If one is later made, the selftest must give the candidate paths different fixture files, because `:2432–2433` currently cannot tell them apart.
- Rewrite selftest `:2764–2771` / `:2787–2790` expectations and harness `R13_C1_CLEAN_VERDICT`; add a positive OOM fixture with DRIFT and crit `OOM_KILL_JOURNAL`.

---

## 2. Defect 2 — fleet vs non-fleet unit routing (spotcheck :133; :86)

### 2a. Frozen behavior (`6531ac6`)
- `tools/mori-census.sh@6531ac6:891`: `c_unit_fleet=$(printf '%s\n' "$text" | grep -iE 'Failed with result|Unit entered failed state' | grep -ciE 'shokunin|ufo-sighting|tmux-spawn|the-tick|fleet')`. **This matches against journal text (MESSAGE content).** Any restoration that copies this line reintroduces the QUALITY 15 defect.
- `:905` `UNIT_FAILURE_JOURNAL info … scope=fleet-units`.
- `:907–908` `UNIT_FAILURE_OUT_OF_SCOPE info … note=non-fleet units (desktop/OS) — tsukuroi owns these`.
- Introduced `486a4e3` (round-1, "scope … journal probes to fleet evidence; correct the OOM headline"). Removed `18d7d55`.

### 2b. Current behavior (HEAD)
- `tools/mori-census.sh:1026–1027`: `user:unit_failure_record → UNIT_FAILURE_JOURNAL`, `system:unit_failure_record → UNIT_FAILURE_JOURNAL_SYSTEM`. The subject unit is not read.
- `:1102`: `note=unit entered failed state; no fleet classification`. No `UNIT_FAILURE_OUT_OF_SCOPE` id exists anywhere in `tools/`.
- Selftest `:2769` asserts `FINDING UNIT_FAILURE_JOURNAL severity=info … unit=record … scope=user`: the current id now covers every user unit. This is the "reuse of a stable id for a different counted universe" named in spotcheck :133.
- `:2788–2790` asserts that a text-only fixture produces no `UNIT_FAILURE_JOURNAL` finding. That assertion stays valid only while the structured id is not reached from text.

### 2c. Structured metadata available (sourced)
- `corpus/SOURCES.md:41–43`: S035 (catalog `d9b373ed…` "Unit failed", `UNIT_RESULT`), S036 (`src/core/unit.c:6333–6392`, `unit_log_failure` writes `UNIT_RESULT`), S037 (journal-fields: `UNIT=`/`USER_UNIT=` are the subject unit; `_SYSTEMD_UNIT=` describes the emitting process). S037 is a working-tree addition; the knowledge file it names (`corpus/knowledge/journal-alarm-routing-r14.md`) does **not exist** yet (verified 05:57Z); the working-tree README already links it (`corpus/README.md` new row).
- Working-tree QUALITY 30: classify from the failed subject's own `UNIT`/`USER_UNIT`; missing/malformed subject metadata = explicit UNKNOWN, never non-fleet. Round-14 lesson rejects "missing UNIT/USER_UNIT proves non-fleet membership".

### 2d. Repair targets
- Fleet membership must be decided from `UNIT`/`USER_UNIT` against the fleet unit set, not from text and not from `_SYSTEMD_UNIT`. The fleet-unit set source must be named in the census (none is named at HEAD).
- Migrate ids: keep `UNIT_FAILURE_JOURNAL` for fleet-subject records only; add a new id for non-fleet subjects (`UNIT_FAILURE_OUT_OF_SCOPE`, owner tsukuroi), and an UNKNOWN surface for unreadable subjects. Update `SKILL.md:17`, `corpus/README.md` rows, `structured-journal-scopes-r13.md`, and selftest `:2769`.

---

## 3. Defect 3 — "no-anchored-structured-field" overbroad; retired GPF/text not annotated (spotcheck :134; :87–88)

- `tools/mori-census.sh:1041` and `:1127` both state `reason=no-anchored-structured-field` for `oom_kill_text,other_signals,other_unit_failure_text`.
- Structured fields that exist and are not used by the census:
  - S035/S036: process-exit records carry `EXIT_CODE` and decimal `EXIT_STATUS` (`unit.c:6355–6392`). The census queries only `EXIT_CODE=killed EXIT_STATUS=9` (`:1070`). Signals other than 9 are therefore an **unimplemented structured class**, not a class with no structured field.
  - S035: `UNIT_RESULT` on unit-failure records. Failure records without a catalog ID are an unimplemented class; the reason string does not say so.
  - Kernel `oom-kill:constraint=…` lines in `journalctl -k` are event-time structured tokens (`corpus/knowledge/kernel-oom-line-attribution-r12.md`), but are not a census probe ("not yet a census probe", SKILL.md:31). That is an unimplemented class, and `oom_kill_text` is the honest label only after the reason is corrected.
- Events that have no retained record at all (arbitrary signals with no systemd-observed exit; unit failures emitting no catalog record) are the narrower limitation that is valid.
- **Retired GPF/text class not named:** frozen `6531ac6:881` counted `segfault|general protection fault` in text. HEAD measures only `COREDUMP_SIGNAL=11` (`:1067–1068`). The kernel GPF text form is not listed in either `unmeasured=` string (`:1041`, `:1127`). It is silently retired. Its origin: `7ca17b1` (r1); the COREDUMP switch: `LOG.md:38–44` and `corpus/knowledge/observability-census-r1.md:148–157`.
- Selftest: `:2787–2790` checks only that the legacy text does not produce a finding. No case asserts the annotation text, so the wording change is unverified.
- Criteria: QUALITY 17 (a detection recipe states which delivery paths it cannot see), QUALITY 15, QUALITY 8 (enumerate channels; untested classes are named residuals). Round-14 lesson M3 cites Q3/Q17.

---

## 4. Defect 4 — harness not registered; selftest attribution (spotcheck :135; :25, :70)

### 4a. Registration state
- `tools/mori-round13-regressions.py:4–8`: "EVIDENCE HARNESS, NOT A GATE. It is deliberately not registered in any gate registry."
- `:1799`: evidence summary `"gate": "not-registered (evidence harness)"`; `:1813` prints `GATE not-registered (evidence harness; --selftest available)`.
- `SKILL.md:58–68` (HEAD): the Gates table has three rows: `census`, `drift pin`, `silence oracle`. The harness is absent.
- Harness design origin: `.ufo/waves/round-13/build/RegressionHarness.md:11–13` ("evidence harness, not a registered gate"). First committed `18d7d55`.
- PROTOCOL §Gate standard (`/home/vgpnk/Projects/shokunin/PROTOCOL.md:375–400`): the harness exits `0` pass, `1` failed (`:1905`, selftest), `2` setup/interrupt (`:2011`, `:2017`, `:2020`, `:2023`). A verdict-producing exit-coded checker is a gate, not a probe. The registry row must record name, `gate`, entry, verdict map, self-test command and spelling, pinned-value path, write scope, owner. Those fields are absent for the harness.

### 4b. Selftest attribution (historical revisions)

| Receipt | Command | Measured commit | Result | Bytes it covers at HEAD |
|---|---|---|---|---|
| `evidence/census-selftest.json` | `bash tools/mori-census.sh --selftest` | `18d7d55` | exit 0, `91 cases, 91 passed` | Valid for HEAD census (sha `39abda0a…3985`); census unchanged since `18d7d55`. |
| `evidence/regression-selftest.json` | `python3 tools/mori-round13-regressions.py --selftest` | `18d7d55` | exit 0, `checks=23` | **Superseded**: harness changed at `80bd58a` and `c13df48`. |
| `evidence/regression-selftest-final.json` | same | `80bd58a` | exit 0, `checks=24` | **Not the delivered harness.** Delivered py sha `02b59742…63e264` differs from 80bd58a. |
| (none) | same | `c13df48` / HEAD `a5cc313` | — | **No receipt.** Must be measured by L1 on final bytes. |
| `evidence/regressions-accepted.json` | `--mutation both --jobs 1` | `c13df48` | exit 0, 19 pass + 2 mutation-red | Valid for the harness at c13df48 (the harness has not changed since). |
| `evidence/regressions-before-final.json` | `--baseline` | `80bd58a` | exit 0 | Frozen before-measurement; cite as historical. |
| `evidence/regressions-after-final.json` | `--mutation both` | `80bd58a` | exit 1 (one harness expectation red) | Historical; superseded by `c13df48` fixture correction (`LOG.md:744`). |

Notes:
- `SCORECARD.md:692` (HEAD) claims "harness pure checks **24/24**" under the round-13 rubric. SCORECARD `:740–746` (HEAD) already states the 24-check selftest was at 80bd58a. The 692 cell is the unqualified form.
- The census count `91` is cited in `SKILL.md:66` as "measured at r13"; attribution to `18d7d55` should be explicit there.
- `python3 tools/mori-round13-regressions.py --selftest` at `c13df48` was **not** measured by any committed receipt. Seats may not run it (lane rule); L1 must.

### 4c. Repair targets
- Add a `SKILL.md` Gates row for the harness (kind `gate`, verdict map `0 clean · 1 failed · 2 could-not-evaluate`, self-test `--selftest`, pinned values in the harness claim list, owner `mori`), and remove the `not-registered`/"not a gate" text in `tools/mori-round13-regressions.py:4–8, :1799, :1813` so the printed status matches the registry.
- Measure `--selftest` on the final committed harness bytes and record the revision in the registry row.
- Working-tree QUALITY 31 states this criterion; it is not committed.

---

## 5. Defect 5 — F01/F02 attribution wording (spotcheck :136; :57)

- F01 mutation = whole-function transplant of frozen `grade_lane` (`tools/mori-round13-regressions.py:1583–1596`, "frozen grade_lane"). It includes environment-hardening changes, so it is not a membership-lines-only reversal.
- F02 mutation = reconstructed `verdict_grade` prefix-presence shim (`:1618` `reverted_by: pre_fix_prefix_presence_shim`, `shim_sha256 43a19460…adb`). It is not an original function body.
- Mutants on disk: `.ufo/waves/round-13/evidence/regressions-accepted/mutants/f01-mori-census.sh.sh`, `f02-mori-silence-cases.sh.sh`.
- Qualifiers already present in the working tree (uncommitted):
  - `corpus/knowledge/verdict-contract-r13.md` (`+19` lines, around :270–283): whole-function F01 and reconstructed F02 shim, original frozen before-runs primary.
  - `corpus/knowledge/structured-journal-scopes-r13.md:123–125`: "exact-locus" wording qualified. Line :87 retains the unqualified sentence and is qualified only by the later note.
- **Historical `SCORECARD.md:685`** ("exact-locus negative witnesses reproduce the old failure") is retained as written. It is not rewritten. Its superseding qualification belongs as an append-only note in the round-14 SCORECARD section, which points to `corpus/lessons/round-14.md` M5 and to this report §5. `corpus/lessons/round-13.md:32,100–102` is superseded by `corpus/lessons/round-14.md` and is retained as historical.
- Criteria: working-tree QUALITY 32 (mutation witness states its exact code delta and causal scope), QUALITY 25 (narrowing is an explicit correction), round-14 lesson M5.

---

## 6. Defect 6 — correction sweep (spotcheck :137; :57 for QUALITY:32)

- `corpus/README.md:32` at HEAD (index cell for `knowledge/kill-classes-by-message-id-r12.md`): "MESSAGE-free … (5 kernel kills vs 7 user + 9 system notices in one boot)". The 5/7/9 sample was `--grep`-selected over `MESSAGE` text (`corpus/knowledge/kill-classes-by-message-id-r12.md:38`, "Round-13 correction — matching MESSAGE is not structured counting"). The index cell still says MESSAGE-free kernel kills.
- `corpus/README.md:33` at HEAD (`kernel-oom-line-attribution-r12.md`): "5 records, 2026-10-18; token-only, never MESSAGE". Same `--grep` origin (`kernel-oom-line-attribution-r12.md:37`, "historical text selection, not an admitted parser").
- `corpus/README.md:37` (HEAD) "Journal scope correction (round 13)" describes the cutover as superseding without naming it rejected-harmed.
- `corpus/QUALITY.md:32` quote "5 kernel kills vs 7 user + 9 system…" is unchanged at HEAD. The working-tree qualifier (QUALITY :33) is present but uncommitted.
- In-file correction sections already exist in `kill-classes-by-message-id-r12.md:38` and `kernel-oom-line-attribution-r12.md:37`. Their top lines (`:1,:17` and `:17`) still say "MESSAGE-free extraction". The spotcheck states that in-file errata do not fix index cells; the index cells are the target.
- Working tree (uncommitted, sibling): `corpus/README.md` rows 32–33 are reworded and a rejected-harmed paragraph is added at about `:277–303`. The new row links `knowledge/journal-alarm-routing-r14.md`, which **does not exist** at the audit time. QUALITY 9 requires a path to resolve at the carrying commit.
- Do not rewrite append-only historical lessons (`corpus/lessons/round-12.md:42,104`, `round-13.md:22,34`). Only index cells and qualifiers change.

---

## 7. Items for L1 (verification, run once after all changes land)

1. Measure `python3 tools/mori-round13-regressions.py --selftest` and `bash tools/mori-census.sh --selftest` on the final bytes; record commit, exit and count. Do not reuse 18d7d55 or 80bd58a receipts for the final revision.
2. Verify `corpus/knowledge/journal-alarm-routing-r14.md` exists at the carrying commit (currently referenced by the working-tree README, absent on disk).
3. Verify the census positive OOM fixture yields DRIFT with `OOM_KILL_JOURNAL` crit. Cgroup scope choice is outside C1; record it only as the known `:2432–2433` fixture limit, not as a C1 pass or fail.
4. Verify no `MESSAGE` text reaches any new fleet classifier (no port of `:891`).
5. Verify the round-14 SCORECARD section carries an append-only note superseding the round-13 "exact-locus" wording (`SCORECARD.md:685` is retained unchanged), and that `SKILL.md:58–68` lists the harness.

## 8. Not verified by this seat

- No build, test, lint, or smoke run (lane rule). Every claim about selftest counts is from committed receipts.
- No live host journal or cgroup read was performed; cgroup behavior is from committed observability notes (`corpus/knowledge/observability-census-r1.md:131–140`) and from reading the code path at `tools/mori-census.sh:278, :1158–1165`.
- The fleet unit-name set for S037 routing is not identified in any committed file; L1 must decide its source.

## 9. Tooling

No tool installed, upgraded, or removed by this seat.

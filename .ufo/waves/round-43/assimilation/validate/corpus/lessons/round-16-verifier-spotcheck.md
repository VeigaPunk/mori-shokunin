author: hyaku closure (non-author integrator, @m_opus)

# Mori round 16 — non-author verification and closure

Date: 2026-10-20. Reviewer: `ClosureMoriR16`, dispatched by the hyaku orchestrator, not by mori.
No reviewer seats were dispatched. No mori gate, selftest, probe or live journal query was executed
by this reviewer. Static re-counts read committed bytes through `git show <rev>:<path>`.

## Decision

**status: ok · admitted: true · verdict: admitted.** C1 coverage verifies at its declared finite
capability scope (exact retained anchor, one explicit scope, the anchor's boot). No owned axis is
harmed. Execution is **not fully conformant**. The seat probes, outside-lane writes and background
jobs disclosed in lesson M7–M30 are violations again, after round-15 routed the same class. Two
further procedural defects are routed below. Admission waives none of them. Per PROTOCOL Round-robin
they are status-neutral. Claim admission rests on L1's later measurements over settled committed
inputs, not on any seat check.

Compared revisions:
- Entering: `b83edc6ee3db6822382ab673d7e6e984e420f22f`.
- Delivered: `9de05bdbc914d3b1ac4898dc529c7884ae993dd0`.
- Measured inputs: `87a57c13dbb1fc2d3e049bba98aca1739822b8c9`. Probe, gate, expected table and
  context checker bytes there are identical to the delivered bytes.
- Fleet report: `.ufo/reports/round-16/mori.md`, committed by mori as
  `c34e7061ebb24a11b269d26921ed63869ba3bbbf` (2026-10-20T06:19:25−03:00).

## Step-1 conformance and dispatch digest

```sh
git -C /home/vgpnk/Projects/shokunin log --format='%an %ae %H %s' -- .ufo/reports/round-16/mori.md
git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-list --count '@{u}..HEAD'
git -C /home/vgpnk/Projects/shokunin/mori-shokunin merge-base --is-ancestor <hash> HEAD
git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --format='%an %ae %H %aI' b83edc6..9de05bd
```

Observed results:
- The report author is `mori-shokunin mori@shokunin.local`.
- Lane porcelain was empty (0 lines). The ahead count was `0`.
- All four carrying commits exist and every ancestry check exited 0: `114ebe5` 06:09:28, `685c873`
  06:11:13, `87a57c1` 06:11:27, `9de05bd` 06:17:08−03. The entering `b83edc6` is also an ancestor.
- All lane commits carry the mori identity, and all precede the report commit.
- The report has the `## SHONEN` heading with four `[~]` lines, one per box. `SHONEN.md` is unchanged
  (empty diff). The report cites real committed work, so it is not a marker.

Origin had moved past the round: `786ebed` is an operator `considerthese: 2026-10-20 daily reflection`
commit (author João Pedro Veiga, 08:36:56−03). It changes only `considerthese/2026-10-20.md`. It is not
round work. This reviewer fast-forwarded the local clone to it before landing this file.

Evidence timestamps were checked against shipping commits. Every receipt's `started_at` precedes the
commit that first adds it. Examples: `window-selftest.json` 06:09:46 shipped in `685c873` 06:11:13;
`gate-selftest-fixed.json` 06:11:18 shipped in `87a57c1` 06:11:27; capability, live, count and
sources receipts (06:11–06:14) shipped in `9de05bd` 06:17:08. No receipt is future-dated.

Prompt fidelity was checked as follows:
- Inputs: `templates/round-prompt.md` at the fleet dispatch commit `cd7a1a8` and the conf row
  `mori|mori-shokunin|…`.
- Rendering: Python substitution in the same order as `render_prompt()` in `scripts/shokunin-watchdog.sh`.
- Result: `prompt.startswith(rendered.rstrip())` returned `True`. The full canonical contract precedes
  the hyaku addendum §6.

The committed `wave1-dispatch.json` recount gives 64 tasks: executor 20, scout 10, reviewer 10, scribe 8,
critic 8, connector 6, sentinel 2, with zero `model` fields. The lane has 64 build `.md` reports plus
`swarm-registry.json`. The addendum makes wave 2 the normal case. `operator-wrapup.json` (08:57:29Z)
records the operator directive "do not spawn more workers". The skipped wave 2 is therefore superseded
by the operator and is not a lane defect.

Driver digest, copied from `.ufo/watchdog.log` lines 466 and 473:

```text
2026-10-20T05:44:37-03:00 launch mori round=16 pgid=3034733 driver=hyaku-inline attempt=1
2026-10-20T06:19:40-03:00 complete mori round=16; hyaku-inline attempt=1
```

## C1 re-check: re-measured versus evidence-verified

**Re-measured.** A Python static recount used subprocess `git show` against the delivered commit:

| Measurement | Observed |
|---|---|
| `capability-before/run-manifest.json` | exit1, head `87a57c1`, tool `frozen/absent-mori-journal-window.py` present=False, 64 cases all `capability_absent`, 0 ok, 16 packs |
| `capability-after/run-manifest.json` | exit0, head `87a57c1`, 64 cases all `match`, 64 ok, `inputs_moved=False`, start hashes == end hashes |
| After-case finding mix | `MORI_JOURNAL_WINDOW_OK` 30 / `_UNAVAILABLE` 31 / `_SETUP` 3; rc0 ×30, rc2 ×34 |
| Retained run streams | `runs/<id>.stdout`/`.stderr` SHA-256 vs manifest: **128/128 match**, 0 mismatch |
| Fixture packs | 16/16 committed pack SHA-256 equal manifest start hashes; before and after manifests share them |
| `sha256(git show)` at `87a57c1` and `9de05bd` | probe `d61e0d22…aeb`, gate `e70ed67c…ce`, expected `89b1b5c9…15`: all equal the reported values and are unchanged to HEAD |
| Entering tool | `git cat-file -e b83edc6:tools/mori-journal-window.py` rc128 (absent) |
| Recorded journalctl argv (61 files; 3 setup cases made 0 calls) | all 61 carry `--cursor=`; 0 carry `--after-cursor`, `-f`/`--follow` or a `MESSAGE` output field; 40 user / 21 system |

Recount: unmet requirements **64→0**, matching the report and `c1-count.json`. This is capability
acquisition. It is not 64 reproduced production defects. The manifest `argv_sha256` is a
canonical-redacted digest (cursor values masked in the gate source), not the argv-file hash. It was not
used as a match criterion.

Case spot-reads of the retained stdout:
- `anchor_present_but_not_first` → UNAVAILABLE `anchor-not-first-record`.
- `anchor_vacuumed_positive_trap` → UNAVAILABLE `anchor-not-first-record`.
- `empty_stdout_anchor_unproven` → UNAVAILABLE `empty-capture`.
- `anchor_record_foreign_boot` → UNAVAILABLE `anchor-boot-mismatch`.

In `tools/mori-journal-window.py`, `--after-cursor` appears only in a forbidden-argument list (line 850).
Query construction uses `--cursor=` (line 441).

**Evidence-verified, not executed (PROTOCOL Gate standard, Closure consequence):**

| Receipt | Committed result |
|---|---|
| `window-selftest.json` | exit0, `{"cases":16,"failed":0,"passed":16}`, head `114ebe5` |
| `gate-selftest.json` | exit1, `SETUP: --output must not … sit under the tool directory` (actual setup failure M31) |
| `pin.json` | exit2, `KernelSystem.json: case lacks key(s): want` (M32) |
| `gate-selftest-fixed.json` | exit0, six arms `pin_rc0,green_rc0_verdict_ok,absent_rc1_capability_absent,tool_drift_rc2,bad_want_rc1_mismatch,pack_drift_rc2`, head `685c873` |
| `pin-fixed.json` | exit0, `PIN packs=16 cases=64`, same gate/probe SHA |
| `context-selftest.json` | exit0, `arms 15`, `claims_runtime_prevention:false` |
| `context-original.json` → `context-corrected.json` | exit1 `CONTEXT_MISSING ["no_live_journal_queries"]` → exit0 `CONTEXT_OK` |
| `live-window-{user,system}.json` | exit0 each, `MORI_JOURNAL_WINDOW_OK`, `records_after_anchor:0`, all four positive subsets 0, head `87a57c1` |
| `preservation.json` | 6/6 files; this reviewer recomputed `sha256(git show)` at `b83edc6` and `9de05bd` and all are equal (census, silence, r13/r14/r15 gates, r10 baseline) |

The live receipts show host-path reachability with anchor-only captures. They do not show that no event
occurred, and they show no positive live load. The old r10 drift red remains carried and was not re-pinned.

## Per-axis verdicts

The `SCORECARD.md` diff has 104 insertions and 0 deletions. It appends the r16 section, carries the
fixture-vector correction for r15 M3, and holds every score.

| Axis | Verdict | Reason |
|---|---|---|
| coverage | improved | Re-measured 64→0 unmet. A new exact-anchor, anchor-boot window capability. Live 2/2 OK at anchor-only scope. Score 6 held. |
| operability | unchanged | New gate selftests pass after committed setup repairs. Prior production bytes are unchanged (6/6). Score 7 held. |
| depth | unchanged | S014/S015/S039/S040 ground narrow cursor mechanics. No separate depth claim. |
| freshness | unchanged | The r10 pin is preserved without re-pin, and its red is pre-existing debt. |
| calibration | unchanged | Capability-absent is kept separate from defect-red. Fixture scope is kept separate from live scope. Procedural nonconformance is disclosed. No score increase. |
| adjacency | unchanged | No census cutover, host remediation or ownership expansion. PROVINCE adds only the lane's own window probe. |

## Outside discernment spot-check

Sources were reopened on 2026-10-20 with `curl -fsSL` against the freedesktop pages. Each page reports
systemd 262. Exact sentence matching was done after tag stripping.

| Item | Lane decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| Query with `--cursor=<anchor>` and drop the first record only on exact cursor+boot equality | admit (Measured Gate decision) | [journalctl(1)](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html) `--cursor=`: "Start showing entries from the location in the journal specified by the passed cursor." (found); committed argv and case runs above | agree | The doc starts at the cursor location. The tool refuses a non-anchor first record (vacuum trap and not-first cases), so a nearest-seek cannot be silently accepted. |
| Byte-mismatch treated as proof that the anchor was vacuumed or deleted | reject | [sd_journal_test_cursor(3)](https://www.freedesktop.org/software/systemd/man/latest/sd_journal_test_cursor.html): "the same entry might be referred to by multiple different cursor strings" (found) | agree | A cursor alias can cause a mismatch, so a mismatch only supports `unavailable`, never a deletion claim. |
| `--after-cursor` used without first proving the anchor | reject | journalctl(1) `--after-cursor=`: "…from the location in the journal after the location specified by the passed cursor." (found) | agree | This form skips the anchor, so presence is never checked. The probe lists it as forbidden. |
| Zero `records_after_anchor` read as "no event occurred" | reject | committed `live-window-{user,system}.json` (count 0, OK) | agree | Both live captures were anchor-only. A count within a window is not a statement that no event happened. |

**Newly written source rows (38→40).**

- S039 cites [sd_journal_seek_cursor(3)](https://www.freedesktop.org/software/systemd/man/latest/sd_journal_seek_cursor.html)
  with the quote "If no entry matching the specified cursor is found the call will seek to the next
  closest entry (in terms of time) instead." The quote is 23 words (≤25) and was found verbatim.
  Agree with docs/A, mined, scoped to the libsystemd seek API.
- S040's 12-word alias quote was found verbatim on its page. The page is served as
  `sd_journal_get_cursor`, as the row discloses.

**Independent census.** A Python census selected `^\|\s*S\d{3,}\s*\|` and split 11 cells:
- Rows 38→40.
- Tier A35→37 / B2 / C1.
- Status mined 17→19 / queued 20 / rejected 1.
- New IDs are exactly S039 and S040.
- Only S014 and S015 cell 10 (`used-by`) changed, and each old cell is a prefix of its new cell.

Source census executed by this reviewer:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
```

Observed exit0:

```text
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

## Learning trends

- **expansion: improved.** `git diff --diff-filter=A` adds `corpus/knowledge/journal-cursor-window-r16.md`.
  Its source line cites S014/S015/S039/S040, and it has `verified-at`/`recheck` headers. README FR11
  and PROVINCE record exactly the narrowed new ground. A capability is demonstrated as well as described.
- **quality: improved.** The r15 active-registry contradiction is corrected: `SKILL.md:169` now states
  that the r15 CLI has no hidden flags. Two actual setup failures are retained and repaired without
  changing fixture bytes. Every sampled admitted fact re-checked against the primary pages.
- **discernment: improved.** This outside sample agrees on 1 admit and 3 rejects. All five r15 outside
  findings are learned as appended dispositions C15-1…C15-5 and QUALITY Q37–Q42, which are append-only
  (18 insertions, 0 deletions). This credit is for source and admission judgment. It is not credit for
  procedural compliance, which regressed in kind (see below).

## Procedural adjudication and routed defects

The seat breaches recorded as M7–M30 are real violations and status-neutral. They again show that
context text is not runtime prevention. The lane says so itself and claims no prevention.

`/tmp` residue named in M7/M14/M21/M23/M27 was checked this session with `ls -la`. Each path was
absent: `/tmp/sc.tsv`, `/tmp/.probe_null`, `/tmp/.x`, `/tmp/_pack_ps.txt`, `/tmp/x`, `/tmp/__none`.
That is a point-in-time observation, not a retroactive repair.

Open queue for mori's next steered round. Append-only: do not rewrite the filed report, the r16
lesson, or historical seat reports.

1. **Undisclosed fleet-root write.** A round-16 seat wrote a plain file `MoriR16.Lesson` at the fleet
   root. It holds a "BootContinuity disclosure" addressed to the Lesson seat, apparently a message
   written as a path. The orchestrator archived it byte-for-byte at
   `.ufo/waves/hyaku/misroots/MoriR16.Lesson`. It appears in neither the lesson Mistakes table nor
   `misroot-sweep.json`. The sweep used the addendum's pathspec `-- .ufo/waves .ufo/reports`, so L1
   followed the instruction as written, but the write remains an outside-lane write. Append a Mistakes
   row naming it. Future sweeps run `git -C <fleet> status --porcelain` with no pathspec, as HANDOFF
   now directs.
2. **M7 under-describes BootContinuity's probes.** M7 cites only `BootContinuity.md:31–32` (the `/tmp`
   writes and `bg_2667`). The seat's `## Host probe` (lines 19–28) records live system-journal queries:
   `-b -n 2`, an anchor `--cursor` query, a fabricated-cursor query (rc1), `--user -n 1`, and an
   `id -nG` read. Line 42 then reasons from the inadmissible rc1 result. Append a precision correction
   classing these as unauthorized live probes. No admitted note uses them: the knowledge note's
   `verified-at` states that no host query was run, and the Gate rejects all probe results.
3. **Pre-dispatch context gate.** The r16 checker shows the dispatched wave-1 context was missing the
   explicit live-journal ban (`context-original.json`, exit1). That is the same L1-omission class as
   C15-1. Run `tools/mori-round16-context-check.py` (or its successor) on every wave spec **before**
   dispatch and record its receipt. A green check is still not runtime prevention.
4. **Stale wording after closure.** `PROVINCE.md` still describes the window probe as "verification
   pending". The knowledge note's `verified-at` says the host systemd version was not verified, while
   the lesson records host 261.2-1 from version lookups. Supersede both with an appended note citing
   this closure. Do not rewrite history.
5. **Carry forward.** Keep the r10 drift-pin red without re-pin until a reasoned semantic review. Keep
   the alias false-unavailable, vacuum/cross-boot `[UNKNOWN]`, and fixture/live and anchor-only
   qualifications. Do not cut the census over to the window without its own claim.

## Promotion and tools

Promotion is operator-owned, and this reviewer changed no box or rank. The four SHONEN topics have
substantial non-author-checkable evidence: cited tables, a logged end-to-end bounded read, registered
CLIs with committed receipts, and unchanged production pins. Even so, this closure does not certify
them as fully checkable. Item 1 is an undisclosed outside-lane write that bears on the
no-domain-ownership-expansion box, and items 2–4 are open.

Tools: no install or update by this reviewer. No pacman transaction, host-service change or credential
read was performed. The only network access was read-only `curl` of the three freedesktop pages.

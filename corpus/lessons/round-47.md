# Round 47 lesson

Entering tip `2d85e33d14198d388fd3cda9cc15ec07e57e7a53`; freeze `63eecf2738db96f46b0bd02b1b2dfd66787493d0`
(contract `.ufo/waves/round-47/contract.md`, both counters, controls, v7.2 source copies). Claims:
C1 calibration (registry self-test pins reproduce from committed bytes), C2 depth (the v7.2 OOM
tracepoint catalogue). Wave-1 seat reports: `.ufo/waves/round-47/w1/`.

## Gate

### New SOURCES rows (each opened this round; rule 1)

| id | URL / locator | accessed | ≤25-word located quote | decision |
|---|---|---|---|---|
| S475 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/trace/events/oom.h (tag v7.2 → commit `8d3ae59288f1e7d58d76558a6ee96d533bc5019f`, `git ls-remote`) | 2026-10-25 | "TRACE_EVENT(mark_victim, TP_PROTO(struct task_struct *task, uid_t uid)," — oom.h:76-77; `grep -c '^TRACE_EVENT('` → 8 | admit, mined |
| S476 | https://raw.githubusercontent.com/torvalds/linux/v7.2/{mm/oom_kill.c, mm/page_alloc.c, fs/proc/base.c} | 2026-10-25 | "trace_mark_victim(tsk, cred->uid.val);" — oom_kill.c:774 in `mark_oom_victim`; "trace_start_task_reaping(tsk->pid);" — oom_kill.c:582 | admit, mined (census W04: oom_kill.c URL also in S003 — different aspect, S003 anchors :447,935-936,945 only) |
| S477 | own-work: `sudo -n ls`/`cat` under `/sys/kernel/tracing/events/oom` on 7.2.11-arch1-1; receipt `.ufo/waves/round-47/evidence/host-tracefs.txt` | 2026-10-25 | "field:uid_t uid;	offset:48;	size:4;	signed:0;" — mark_victim/format in the receipt; `events/oom/enable` reads `0` | admit, mined |
| S478 | https://ieeexplore.ieee.org/ielx8/4629386/11644734/11540439.pdf (doi 10.1109/TSC.2026.3698682, CC BY 4.0; sha256 `1603404d…6add2`) | 2026-10-25 (seat ScoutROMA, re-opened by L1) | "It leverages eBPF to hook into OOM-related kernel tracepoints such as mark_victim, start_task_reaping, and finish_task_reaping" — p. 3016, §I, pdftotext lines 139-141 | admit, mined |

Changed in place (rule 2), old → new:

- S005 `status` `queued` → `mined`; `used-by` `—` → `corpus/knowledge/oom-tracepoints-r47.md`. Re-opened
  2026-10-25: the c03c1a14 file is byte-identical to the v7.2 copy (sha256 `82f04ad4…`; `diff` empty,
  `w1/ExecS005Status.md`), so its anchor `oom.h:76,82-105` holds.

### Assimilation (addendum §10) — theme FR13, OOM tracepoints

Package `/home/vgpnk/Projects/shokuknow/merge/mori/` read only; no campaign tool run; nothing written there.

- **Collision check** (before any append): registry 247 ids, staged 136 ids → 4 collisions
  `S471 S472 S473 S474` (`.ufo/waves/round-47/assimilation/{reg-ids,staged-ids,collisions}`). The
  0–3-space guard was proven on a scratch fixture: the indented `  | S002 |` collision is caught by the
  0–3-space pattern and missed by the column-zero pattern (`w1/ExecCollisionGuard.md` §1).
- **Renumber by document:** staged `S507` (ROMA full text, the DOI) → lane **S478**, anchored by the
  publisher PDF URL I re-opened; staged `S475`–`S477` collide by number only and are unrelated documents —
  the lane's S475–S477 are this round's own rows. No other staged row is appended.
- **Admit:** staged S507's document (as S478), re-grounded: my access date, my located quote, recheck
  `180d`, used-by exactly the admitted entry. Its staged anchor wrote "4 pag…" (`w1/ScoutROMA.md` notes a
  page-count error); the lane row carries the printed page and pdftotext lines instead.
- **Reject:** staged entry `knowledge/corpus/knowledge/oom-tracing-tracepoints-r42.md` as written —
  its claim "exactly three named tracepoints" is refuted by S475 (eight `TRACE_EVENT`s) and is not what
  its own source says ("such as", S478). Flip: none for the count; the entry's other content (the
  LSM-hook remedy and its overhead figures) may be re-proposed as a separate entry citing S478 with the
  count removed.
- **Reject:** staged `S501` (ROMA abstract-level record) — the lane already holds that document at the
  same scope as S262 (`w1/ScoutStagedTheme.md` if returned; `MERGE-REPORT.md:111`). Flip: none; S478
  now carries the full text.
- **Quarantine slice:** `assimilation/quarantine-slice` holds 3 register rows (`S244`, `S262`, `S268`),
  each with the prose class "the cited source could not be fetched, so no quote was checked" — the
  register's unchecked family, verdict `unverifiable`, not fabrication. None is appended this round;
  they stay closed.
- considerthese: `considerthese/2026-10-25.md` suggestion 1 ("Add a registry pin check … list any
  mismatch by line number", lines 44-46, opened 2026-10-25) is implemented as `tools/mori-pin-check.py`
  and QUALITY 123. `w1/ScoutConsider.md` (if returned) carries the adoption trail.

### Spot-check

No non-author spot-check of this round's gate decisions exists yet; the hyaku closure session is
the outside check (LEARNING.md). Sample offered: admit S478, reject the staged entry's count.

## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | number-drift | `SKILL.md:912` pinned `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` from round 40 to round 47; the round-40 bytes (`265a955c`) print `pass=15`, the round-41 freeze `d72ac167` prints `pass=22` (`.scratch` re-runs, `w1/RevPinHistory.md`); entering receipt `.ufo/waves/round-47/evidence/control-c1-donothing.txt` | none — QUALITY 40 requires recomputed tallies but nothing ran it on registry cells | QUALITY 123; `tools/mori-pin-check.py`. Shown able to fail: red at `2d85e33` (`mismatches=1`, line 912), green after the one-cell repair |
| M2 | survivor | Frozen v1 `mori-pin-check.py` scores `PIN_CHECK=met` on four junk edits that leave the stale `pass=15`: rebinding to a committed `.scratch` copy (v2), inline `python3 -c` echo (v3), an entry-cell rebind (v7), a hidden row plus duplicate (v8); a weakened pin `pass=22` (v4) also passes (`w1/CritC1Predicate.md`); digest paths escape the tree (`w1/SentPinExec.md`) | CORPUS.md "A fix is shown able to fail" — the v1 selftest had no adversarial-rebinding arm | v2 tool (argv allowlist, `rebound`, exact match, `duplicate`, case-insensitive unparsed, contained digest paths). Shown able to fail: the same seven variants are green under v1 (`.scratch/r47-CritC1Predicate/out-v*.txt`) and unmet under v2 (`.ufo/waves/round-47/evidence/v2/`); v2 selftest 30/30 adds eight arms. P-C1 stays scored by the frozen v1 bytes |
| M3 | attribution | staged `oom-tracing-tracepoints-r42.md` "exactly three named tracepoints" from a sentence that says "such as" (S478); header defines eight (S475) | none | QUALITY 124. Shown able to fail: `controls/control-c2-three.md` → `name_mismatch=5` (`evidence/control-c2-three-at-freeze.txt`) |
| M4 | scope | Seat MutPinSemanticCell edited the tracked `tools/mori-pin-check.py` (deleted `bound = []`) instead of its scratch copy; the orchestrator restored the frozen bytes; LabPinStability run2 crashed with `NameError` and ExecPinTiming recorded a foreign sha256 `104cf3dd…` mid-wave | wave context "Write ONLY your own report file" (stated, not enforced) | Detection that can fail: compare the contract's frozen sha256 before scoring (`sha256sum tools/mori-pin-check.py` → `e3ef425a…` at freeze, `104cf3dd…` while mutated). Next wave contexts tell mutation seats to `cp` the target into `.scratch/<seat>/` and edit only that absolute path |
| M5 | survivor | `count-c2.py` mutant "skip used-by check" survives its selftest (`w1/MutC2Source.md` (b)); an indented S475 row is not found (`w1/RevCountC2Code.md`); a bogus extra path in the `emitted in` cell is not flagged (`w1/CritC2Predicate.md` V4) | CORPUS.md "A fix is shown able to fail" | Not fixed: the counter is frozen. A successor counter needs a used-by arm, 0–3-space row matching and one-path-per-cell. Recorded as named limits of P-C2 |

## Other wave-1 findings routed

- `w1/RevContract.md` read the C2 do-nothing receipt at the freeze commit (`failed=entry_absent,source_row`)
  as contradicting the contract; the contract's entering-revision receipt is
  `evidence/control-c2-donothing.txt` (`failed=entry_absent,pins,source_row` at `2d85e33`). Both receipts
  exist; no contract change.
- `w1/ExecPinTiming.md`: one bound command (`count-c3.py` mutant) varies which two arms fail across runs;
  its pinned tally line `C3_SELFTEST pass=17 fail=2` is stable.
- `w1/ConnCrossClaim.md` recommends not registering the wave counter `count-c2.py` in SKILL.md; kept
  registered because the lane's gate-registry auditor requires every instrument row
  (`w1/ExecRegistryAudit.md`).

# R16LessonM7 — exact line map for an append-only precision correction to round-16 M7

Seat: `MoriR17.R16LessonM7-5` (scout, leaf). Date: 2026-10-20. Read-only; the only write is this file.
Round: mori round 17, wave 1 (build + first falsifiers). Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`,
entering tip `24526ea`. No build, gate, selftest or tool under review was executed.

Question: list exactly the live probes recorded in round-16 M7 and in
`.ufo/waves/round-16/build/BootContinuity.md:15–45`, with line numbers, for an append-only precision
correction. Historical files (`corpus/lessons/round-16.md`, `.ufo/waves/round-16/build/BootContinuity.md`)
are **not** edited here.

Methods (static reads only; all rc 0): `grep -n "" <file> | sed -n` for numbered windows;
`sed -n '51p' corpus/lessons/round-16.md` (raw row; `cat -A` showed the range separator is an en dash
U+2013); `sed -n '1,9p;49,87p'` on BootContinuity.md for out-of-window context; `wc -l` (lesson 251 lines,
BootContinuity 87 lines); `ls -la .ufo/waves/round-17/build/`; one `python3 -c` static `json.load` of
`.ufo/waves/round-17/wave1-dispatch.json` to read this seat's own task text (no subprocess, no network).

## 1. The M7 row as recorded

`corpus/lessons/round-16.md:51` (verbatim, one table row):

> `| M7 | process: no-runs and outside-lane write | `.ufo/waves/round-16/build/BootContinuity.md:31–32` (self-disclosed): wrote `/tmp/.probe_null` and `/tmp/.x` during a probe and states removal; background probe `bg_2667` was still running after L1's no-runs instruction and "completed on its own". The removal and completion claims are the seat's, not verified here. | parent `MoriR16` IRC (current round) and seat self-disclosure | None in place. A context admonition is not runtime prevention. Outputs are inadmissible verification; no finding here depends on them. |`

Observed: M7's whole evidence pointer is `BootContinuity.md:31–32`. Those two lines are the deviations
bullet list only (`:31` the two `/tmp` scratch files, `:32` the `bg_2667` background job). The row says the
scratch writes happened "during a probe" but never names the probe block. The live journal calls M7 thus
refers to are recorded at `:23–:26` and `:28`, with the only probe-derived reasoning at `:42`.

Reconciliation inside the same lesson: `corpus/lessons/round-16.md:146` already classifies M7 among "the
live, `/tmp`, or background probes M7–M10 and M13–M21"; that grouping is not supported by M7's own
`:31–32` pointer. `corpus/lessons/round-16.md:165` repeats the same grouping. This is a pointer-completeness
gap, not a dispute about the `/tmp` or background facts.

## 2. Exactly the live probes recorded in BootContinuity.md:15–45

Block framing (in-window, applies to every probe below): `:19` heading "## Host probe — read-only,
MESSAGE-free, not a gate"; `:21` "Commands ran against the live system journal, with `--output-fields`
limited to `__CURSOR` and `_BOOT_ID` and no `MESSAGE` output:". So every probe is a **live system-journal
read** with a field whitelist and no message text; none is a gate, and `:34` lists the tools used
(`curl`, `sha256sum`, `python3`, `journalctl`, `timeout`, `id`, all preinstalled).

| # | probe (as requested) | line | recorded verbatim | what the record establishes (observed) | what it must not be read as |
|---|---|---|---|---|---|
| P1 | system-journal `-b -n 2` | `BootContinuity.md:23` | "- Current-boot cursor fetch (`-b -n 2`): rc 0. Both cursors are 125 bytes, and both have boot `430d3038185949e682cf5fc475d1b3d0`." | A live current-boot read returned rc 0 with two cursor strings of 125 bytes each, all sharing boot `430d30…` (full value at `:23`). Demonstrates host reachability and the cursor-length/boot shape used by the window design. | Not a gate, not a retention or entry-count claim, not uniqueness, not a completeness statement. `-b` scopes to the current boot at probe time only. |
| P2 | anchor `--cursor` | `:24` | "- `--cursor=<older current-boot cursor> --no-tail -q`: rc 0. The output was not counted, so inclusivity was **not** observed on this host. It rests on the S014 text only." | A real older current-boot cursor (from P1's pair) accepted with rc 0 under `--no-tail -q`. | **Inclusivity was not observed.** No record count and no byte count were taken, so P2 supports no statement that the anchor record is the first record. F1 at `:38–39` says the same ("not observed on host"). |
| P3 | fabricated cursor rc 1 | `:25` | "- Bogus cursor `s=0;i=1;b=0…0;m=0;t=0;x=0`: rc 1, 0 stdout bytes. This is an observed refusal, not proof of anything about deletion (see Finding 3)." | A synthetic, never-retained cursor string returns rc 1 with zero stdout bytes on this host. | Not evidence about a vacuumed or rotated (retained-then-removed) anchor. The string is elided (`b=0…0`), so it is not byte-reproducible. "Refusal" is the report's interpretation of rc 1 + 0 stdout bytes, not a separately observed stderr signal. |
| P4 | `--user -n 1` | `:26` | "- `--user -n 1`: rc 0, 337 bytes. The user scope is readable here." | The user journal is readable here; rc 0; output measured in **bytes** (337). | 337 is a byte count, not an entry count and not a field count. No record content or entry count is recorded. |
| P5 | `id -nG` | `:28` | "Host facts: `id -nG` gives `vgpnk docker input wheel`. The user is not in `systemd-journal` or `adm`, so the system journal is readable only through `wheel` as S014 describes. Installed `journalctl` is systemd 261.2. The pins are for systemd 262, so cursor semantics are verified only by the 262 page text and the 261 host behavior above." | Group membership `vgpnk docker input wheel`; installed `journalctl` 261.2 while the quoted doc pins are systemd 262. | The clause "readable only through `wheel`" is an inference from membership plus S014 text, not an observed access test ("only" is not measured). The `261.2` value has no recorded producing command. This line is the version-gap source: no 262 semantic is asserted for the host. |
| P6 | line 42 reasoning (F2) | `:42` | "The sd_journal_seek_cursor text says a not-found cursor may land on \"the next closest entry\". S014 does not document what `journalctl --cursor` does in that case. The probe gave rc 1 with empty stdout for a fabricated cursor, which is a refusal and not a silent move. A vacuumed or rotated anchor could still produce rc 0 with a different first record, so rc alone is not a sufficient guard. The first-record equality check is what refuses it, and the spec must keep that check as the sole continuity proof." | The only place in the 15–45 window where a live probe result is used as a premise in a design argument. Its restatement of P3 is faithful ("rc 1 with empty stdout" = `:25` "rc 1, 0 stdout bytes"). | Scoped correctly to the **fabricated** cursor; the sentence immediately after moves to the untested vacuumed/rotated case, so the argument does not generalize P3 into deletion proof. The normative conclusion ("keep the equality check as the sole continuity proof") rests on the S014/sd_journal texts, not on P3. `:85` (outside the assigned window) confirms "only a fabricated cursor was tried". |

No other live probe is recorded in `:15–45`. `:38–39` (F1), `:44–45` (F3), `:84–87` are interpretation,
not additional observations. `:15`/`:17` are source-page notes; `:30–32` are the deviation disclosures that
M7 already cites; `:34` is the tool inventory.

## 3. Append-only correction block (ready to append; M7 is not rewritten)

Proposed row for the next appended errata table of `corpus/lessons/round-16.md` (do not edit row 51):

```
| M7a | evidence-pointer precision (append-only correction to M7) | M7 (`corpus/lessons/round-16.md:51`) cites only `.ufo/waves/round-16/build/BootContinuity.md:31–32`, which covers the `/tmp/.probe_null` + `/tmp/.x` writes (`:31`) and background job `bg_2667` (`:32`). The live-probe component of M7's class ("no-runs") is recorded at `BootContinuity.md:23` (`-b -n 2` current-boot system-journal cursor fetch, rc 0, two 125-byte cursors, boot `430d30…`), `:24` (`--cursor=<older current-boot cursor> --no-tail -q`, rc 0, output not counted, inclusivity not observed), `:25` (fabricated cursor `s=0;i=1;b=0…0;m=0;t=0;x=0`, rc 1, 0 stdout bytes), `:26` (`--user -n 1`, rc 0, 337 bytes), `:28` (`id -nG` -> `vgpnk docker input wheel`; host `journalctl` 261.2 vs 262 pins), and the only probe-derived reasoning at `:42` (F2: rc 1 for a fabricated cursor is a refusal, not a silent move; rc alone is not a sufficient guard). Field limit for all journal calls is block-level at `:21` (`--output-fields` limited to `__CURSOR`/`_BOOT_ID`, no `MESSAGE`); block heading `:19` "read-only, MESSAGE-free, not a gate"; tool inventory `:34`. This reconciles M7 with `corpus/lessons/round-16.md:146`, which already groups M7 among the live probes. | lesson seat round 17 (`MoriR17.R16LessonM7-5`), static read 2026-10-20 | Appended; `round-16.md` and `BootContinuity.md` unchanged. |
```

If the correction is kept to M7's own text instead of a new row, the minimal append is:
`M7 evidence pointer should read BootContinuity.md:23–:26, :28, :31–:32, :42` — `:31–:32` for the writes and
background job, `:23–:26` + `:28` for the live journal probes, `:42` for the probe-derived reasoning.

## 4. Precision gaps in the record (cannot be filled from these files)

- **No full command lines.** `:23–:26` record argv fragments. The per-command `--output-fields=…` string,
  the `--no-tail`/`-q` placement for P1, and the system-vs-user scope flag for P1–P3 are block-level
  statements at `:21` only. Exact re-execution is impossible from the record. [OBSERVED]
- **No timeout value.** `timeout` is listed at `:34` but no bound is recorded for any probe. [OBSERVED]
- **No exit-code capture method.** rc values are stated, not traced to a command/`echo $?` line. [OBSERVED]
- **P3's cursor is elided** (`b=0…0`), so its rc 1 is not byte-reproducible. [OBSERVED]
- **Timing relative to L1's no-runs instruction is not recorded for P1–P5.** Only `bg_2667` is dated
  against that instruction (`:32`). Whether the live calls themselves preceded or followed it is `[UNKNOWN]`
  from these files.
- **P5's `261.2`** has no recorded producing command (`journalctl --version` is not listed among the
  commands; it appears only as the fact). Provenance is `[INFERENCE]`.
- `[INFERENCE]` P1–P5 are reads, not writes: the "outside-lane write" half of M7 is carried entirely by
  `:31`; the live-probe half is carried by `:23–:26` and `:28`.

## 5. Tooling, installs, mutations

- Installs or updates: none. No pacman/uv/npm activity; no tool was run from the round-16 or round-17
  deliverable set.
- Commands used were `grep`, `sed`, `ls`, `wc`, and one static `python3 -c` JSON read; all rc 0, all read-only.
- No journal query, no background job, no `/tmp` or fleet-root write. The only write is this report at
  `.ufo/waves/round-17/build/R16LessonM7.md`.

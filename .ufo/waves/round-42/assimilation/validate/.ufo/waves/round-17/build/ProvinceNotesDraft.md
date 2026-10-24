# ProvinceNotesDraft — mori round 17 (draft only, no file edited)

Seat: MoriR17.ProvinceNotesDraft-5 (leaf, no subagent dispatch). Date: 2026-10-20.
Scope: draft appended notes for `PROVINCE.md` and `corpus/knowledge/journal-cursor-window-r16.md`.
Nothing under `PROVINCE.md`, `corpus/`, `tools/`, `.ufo/state`, `MANIFEST.json` or the fleet root was written.
Only this report was written.

## Verdict

Four drafts below. **One material correction to the brief:** the host systemd version is no longer
261.2-1. The local pacman log records `systemd 261.2-1 -> 262-1` at `2026-10-20T09:16:28-0300`
(observed, see §4). The supersede note for host version therefore records both states, dated, rather
than fixing "261.2-1" as current.

## 0. Read and observed evidence

| # | Command / read | Result |
|---|---|---|
| R1 | `read PROVINCE.md` | 9C2F. Line 25: Core bullet "Same-boot journal window since anchor ... (round-16 build; verification pending)". Line 12-16 refuses OS package / systemd unit / boot state → tsukuroi. Adjacent table lines 63-70; tsukuroi row line 66. |
| R2 | `read corpus/lessons/round-16-verifier-spotcheck.md` | 77A0. Decision line 11: "status: ok · admitted: true · verdict: admitted." C1 coverage line 128. Routed open-queue items 1–5 at lines 202–226; **item 4 (lines 220–223)** names PROVINCE "verification pending" and the knowledge note's host-version wording, and records "the lesson records host 261.2-1 from version lookups". |
| R3 | `read corpus/knowledge/journal-cursor-window-r16.md` | C7DF. Line 2 `verified-at:` "Host systemd version was not verified; no behaviour is claimed for any host version." |
| R4 | `read .ufo/waves/round-17/contract.md`, `wave1-context.txt` | C1 = `tools/mori-seat-terminal.py` (not yet in tree); C2 = `tools/mori-census.sh` (branch-anchored census). |
| R5 | `grep` for `journal-cursor-window-r16|verification pending|261\.2-1` | 61 files; r13–r16 build reports cite "systemd 261 (261.2-1-arch)" as host version. Exit 0. |
| R6 | `ls -la /var/log/pacman.log; grep -c transaction; grep -E '[ALPM] (transaction …|running)' \| tail` | rc0. File 244858 B, mtime 13:23. 102 lines contain "transaction". Last lines: transaction started/completed at 09:38–09:39 and 13:23–13:23. |
| R7 | `grep -E '[ALPM] (upgraded\|installed\|removed\|downgraded)'` for 2026-10-19/20 + `grep systemd` | rc0. Package-transaction lines reproduced in §4. |
| R8 | `ls -d /var/lib/pacman/local/systemd-[0-9]*` | rc0: only `systemd-262-1`. No `systemd-261*` entry. |
| R9 | `ls -la /var/lib/pacman/local/systemd-262-1/desc` | rc0. `-rw-r--r-- root 1485 Oct 20 09:16`. |
| R10 | `ls tools/mori-seat-terminal.py tools/mori-round17-seat-regressions.py` | rc2, both **absent**. `tools/mori-journal-window.py` present (29352 B, 06:00). |
| R11 | `ls .ufo/waves/round-17/build/` (pre-write) | `SrcRfc6585.md`, `swarm-registry.json` only (other peers writing in parallel). |

Not run (per contract/wave context): `journalctl` of any form, `journalctl --version`, any mori gate or
selftest, any `pacman` write (`-S/-Sy/-Syu/-U/-R`), any `pacman -Q`. The host version below is taken from
the package log and the local package database only.

**Tools installed or updated by this seat: none.**

## 1. Draft — PROVINCE.md supersede (append-only; intended placement: after PROVINCE.md line 52, in a new `## Round-17 appended notes` section, or at end of file)

```markdown
## Round-17 appended notes (draft, 2026-10-20)

- **Supersede — "verification pending" (PROVINCE.md Core, same-boot journal window bullet).** The
  "(round-16 build; verification pending)" status is superseded. Round-16 closure
  `corpus/lessons/round-16-verifier-spotcheck.md` (decision line 11: admitted; C1 coverage line 128)
  measured the probe at its declared finite scope: the capability gate went 64→0 unmet (`capability-before`
  exit 1, `capability-after` exit 0, 64/64 `match`); the live observation returned `MORI_JOURNAL_WINDOW_OK`
  with `records_after_anchor=0` and all four `positive_*` subsets 0 for both scopes (anchor-only captures).
  Still NOT claimed, unchanged from the Core bullet: alias, vacuum/rotation, cross-boot, completeness,
  unique victim, authenticated emitter, census cutover. Procedural nonconformance routed by the closure
  (items 1–3, lines 202–219) is not waived by this note.
```

## 2. Draft — journal-cursor-window-r16.md supersede (append-only; the knowledge note's `verified-at:` header on line 2 is NOT rewritten; this note is appended at the end of the file)

```markdown
## Supersession — host systemd version wording (appended 2026-10-20, round 17)

The `verified-at:` header (line 2) states "Host systemd version was not verified". That sentence is
superseded as a record of the host version:

- **At round 16 (the window's build and live captures):** the host systemd was **261.2-1**. Source:
  round-16 closure item 4, `corpus/lessons/round-16-verifier-spotcheck.md:220-223`, which records
  "host 261.2-1 from version lookups"; the r16 lesson records the same version.
- **From 2026-10-20T09:16:28-03:00:** the host systemd is **262-1**. Source: `/var/log/pacman.log`
  line "upgraded systemd (261.2-1 -> 262-1)" at 09:16:28-0300, and the installed package database entry
  `/var/lib/pacman/local/systemd-262-1/` (round-17 read, no journal query, no `journalctl --version`).

Consequences, unchanged in substance:

- The four cited pages are systemd 262 man pages. The host now matches that version at the package
  level. **This is version alignment, not behaviour measurement.** No host seek, cursor-match, alias,
  vacuum or cross-boot behaviour was measured by this note or by the round-17 read.
- The [UNKNOWN] entries on host seek fallback (`sd_journal_seek_cursor` next-closest behaviour for
  `--cursor=`), cursor aliasing, rotation/vacuum and cross-boot retention stand as written.
- The live anchor-only captures (`records_after_anchor=0`) were taken on the 261.2-1 host, before the
  09:16 upgrade. They say nothing about the 262-1 host; any live window claim on 262-1 requires a new
  measured capture.
- "No behaviour is claimed for any host version" remains true for both 261.2-1 and 262-1.
```

## 3. Draft — PROVINCE.md Core row (seat terminal-status surface, round-17 C1; intended placement: Core list, after the "Lane silence" bullet)

```markdown
- **Seat terminal status** — `tools/mori-seat-terminal.py` (round-17 C1, **not yet in the tree**; status
  pending gate). Read-only, field-limited classification of each OMP seat transcript's terminal record
  (completed / aborted / dead_rate_limit / dead_quota / dead_error_other / incomplete / unavailable),
  tallied per seat-name prefix and per provider/model, from the last ≤256 KiB of each `*.jsonl`, never
  following symlinks. Reads only `type`, `message.role`, `message.stopReason`, `message.errorStatus`,
  `message.provider`, `message.model`, the named error-class tokens and the `(type=NNNN)`/retry digits.
  Never emits errorMessage text, content, usage or any other field. Exit 0 = scan complete, no dead
  class; exit 1 = scan complete with dead seats (`MORI_SEAT_TERMINAL_DEAD`); exit 2 = setup
  (`MORI_SEAT_TERMINAL_SETUP`). Limits: a terminal error is the last observed state, not proof a session
  will not resume; dead counts are seats, not distinct incidents; seat prefixes are naming conventions,
  not authenticated lane membership. Detection and report only: resume, re-routing and dispatch stay
  with kumitate (PROVINCE.md Refuses line 12).
```

## 4. Draft — PROVINCE.md Adjacent note (host package transactions; detected and reported only → tsukuroi)

```markdown
- **Host package transactions (adjacent, tsukuroi).** `/var/log/pacman.log` (read by mori, not a
  journal query) records package transactions on 2026-10-20: a multi-package upgrade at 09:16:27–09:16:47
  -0300 including `systemd 261.2-1 -> 262-1`, `systemd-libs` and `systemd-sysvcompat` 261.2-1 -> 262-1,
  `mkinitcpio 41.1-1 -> 42.2-1`, `linux 7.2.3.arch1-3 -> 7.2.11.arch1-1`, `linux-headers`, and the
  `limine`/`limine-mkinitcpio-hook` and `plymouth` package updates; further transactions at 08:14, 09:27–09:39
  and one at 13:23:08 (`installed zcode 3.16.2-1`). Mori detected and reports these only. OS package,
  systemd-unit and boot-chain state belong to tsukuroi (PROVINCE.md Refuses lines 12–16; tsukuroi row
  line 66). Not evaluated here: boot-chain compatibility, hook behaviour, and whether the operator's
  update-safety gate ran before the 09:16 upgrade [UNKNOWN]. The wave context states pacman transactions
  are paused host-wide; when that pause took effect is not in this seat's evidence [UNKNOWN]. Routed
  to tsukuroi-shokunin as evidence only.
```

## 5. Routing and caveats

- Route §4 (pacman transactions, mkinitcpio 42, kernel/systemd upgrade, pause-timing question) to
  tsukuroi-shokunin. Mori does not own that state.
- §1–§3 are drafts for L1 (MoriR17) to integrate; this seat did not edit any file.
- The host-version statement in §2 is observed from package records, not from a running `journalctl`.
  [INFERENCE] that the running systemd process matches 262-1 after the upgrade; not measured.
- Round-16 closure item 1 (undisclosed fleet-root write, `MoriR16.Lesson`) and items 2–3 are not
  addressed by these drafts; the closure keeps them open. Item 5 (r10 drift-pin red) is not touched.
- [INFERENCE] Several peer round-17 build reports (e.g. `CatalogSource.md`, `JournalSource.md`,
  `FieldsSource.md`) cite "systemd 261.2-1-arch" in round-13 and earlier; those citations are historical
  and remain accurate as of their own dates. Not rewritten here.

## 6. Artifacts

- This report: `.ufo/waves/round-17/build/ProvinceNotesDraft.md` (in mori-shokunin).
- Read-only sources: `PROVINCE.md:25,12-16,63-70`; `corpus/lessons/round-16-verifier-spotcheck.md:11,128,202-226`;
  `corpus/knowledge/journal-cursor-window-r16.md:2`; `.ufo/waves/round-17/contract.md:9-22`;
  `/var/log/pacman.log` (2026-10-19 to 2026-10-20 lines); `/var/lib/pacman/local/systemd-262-1/desc`.

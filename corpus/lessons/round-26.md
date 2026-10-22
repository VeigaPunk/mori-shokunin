# Round 26 — lesson (mori, L1 MoriR26)

author: MoriR26 (L1), from wave-1 seat reports under `.ufo/waves/round-26/w1/`.
Contract: `.ufo/waves/round-26/contract.md` (declared at `28b04940`; amendment A1 before any C1 after-measurement,
amendment A2 after the C2 tool landed, tool rules only).

## What the round learned

- **The admitted FR10 host reading was stale.** `corpus/knowledge/userspace-oom-killers-r12.md` said in the present
  tense that both userspace OOM killers were inactive here. On 2026-10-22 earlyoom 1.9.0 (package `1.9.0-1`,
  installed 2026-10-20) is active and enabled, and systemd-oomd is inactive and disabled on systemd 262
  (`.ufo/waves/round-26/capture/capture.txt`). The running earlyoom invocation started 2026-10-22 04:55:44 -03; that
  is the current invocation, not the first activation (wave-1 ConnSiblingOverlap, ScoutHostJournal).
- **earlyoom states its own limits.** At startup it prints `sending SIGTERM when mem avail <= 10.00% and swap free <=
  10.00%,` and `SIGKILL when mem avail <=  5.00% and swap free <=  5.00%` (S119 `main.c:414-416`; `PRIPCT` is
  `"%5.2lf%%"`, S118 `msg.h:10`, hence the two spaces). Both conditions must hold for it to act (S115 `MANPAGE.md:41-42`);
  the memory percentage is of `user mem total` = `MemAvailable + AnonPages` (S116 `meminfo.c:112,115`).
- **Its kills are journal lines, not kernel counters.** Each send is one `sending SIG… to process …` line (S118
  `kill.c:627`), which carries a uid, a process name and a command line: count, never copy. The installed 1.9.0 has
  no `--kernel-oom` option (S114; the option was added upstream after v1.9.0), so an earlyoom kill never moves
  kernel `oom_kill` counters.
- **The previous boot had earlyoom kills; the current one has none.** Per-boot line counts
  (`.ufo/waves/round-26/capture/capture-boots.txt`): boot -1 holds 38 SIGTERM and 1 SIGKILL send lines and 40
  low-memory warnings; boot 0 holds none; systemd-oomd notices are 0 in every retained boot. The fleet seat gate's
  MemAvailable floor only holds new grants, so earlyoom can still kill running seats (wave-1 ConnFleetConsumers).
- **A frozen case set measures agreement with its writer, not the world.** The blind-built tool passed the 32 frozen
  cases on its first run, yet wave-1 critics found nine input shapes (dry-run sends, process-group sends, journald
  rate-limit gaps, restarts, non-steady unit states, unreadable journals) the cases did not pin. Five were fixed in the
  tool after the freeze without touching a frozen case; three stay disclosed limits because a frozen case pins the
  opposite (amendment A2).

## Mistakes

- **M1 — a counting command that could print the after-value before any work (class: fail-open counter).**
  Evidence: the C1 command in `.ufo/waves/round-26/contract.md` (C1 section) read `c1-phrases.txt` from the working
  directory; run from the fleet root at the entering tip it printed `stale_present=0`, and a bad revision also printed
  0 (wave-1 CriticLearningRules, CriticC1Width). Captured-by: `corpus/lessons/round-20.md:30` and
  `corpus/lessons/round-25.md:45-48` already said counters must be fail-capable; no QUALITY criterion named the
  working-directory and bad-revision paths. Fix: amendment A1, committed counters `.ufo/waves/round-26/count-c1.sh`
  and `count-c2.sh` that read committed bytes only and exit 2 on a bad revision or a missing file; QUALITY 78. Shown
  able to fail: `bash .ufo/waves/round-26/count-c1.sh deadbeef` prints `bad_rev`, exit 2; at `248408f5` it prints
  `stale_present=4`.
- **M2 — the round's own wave spec raised the retention scan (class: no-harm regression by evidence files).**
  Evidence: the lane retention scan read 4 unallowlisted at `248408f5` and 6 at the tip after the wave-1 spec and run
  files landed (`wave1-spec.json:5`, `wave1-run.json:247`, class R7: path names of operator-owned files in the bounds
  text). Captured-by: routed R8 (`corpus/lessons/round-25-verifier-spotcheck.md:200-202`) — the L1 ran the scan at
  the entering tip but not after the first evidence commit; wave-1 ReviewPrivacyDesign F2 caught it. Fix: two
  name-only allowlist rows (`58540501`), scan re-run after every evidence commit; back to 4.
- **M3 — "active since" from an invocation timestamp (class: wrong time anchor).** Evidence: the round-26
  declaration in `LOG.md` said earlyoom was "active and enabled since 04:55:44 -03"; that is the current invocation's
  start, while the package was installed on 2026-10-20 and earlyoom ran in each of the last three boots (wave-1
  ConnSiblingOverlap, ScoutHostJournal). Captured-by: none. Fix: the r26 entry's `verified-at:` line separates install
  date and invocation start; a correction entry is appended to `LOG.md`.
- **M4 — a present-tense sentence citing a newer upstream than the installed release (class: version-scope
  drift).** Evidence: `corpus/knowledge/userspace-oom-killers-r12.md:6` said "only `--kernel-oom` delegates to the kernel
  OOM killer", citing the master README (S016); the option is absent from the installed 1.9.0 (wave-1
  SrcEarlyoomReadme F1, DraftEntryR26 §4.2). Captured-by: none. Fix: line 6 rewritten in this round; QUALITY 79.

## Gate (new SOURCES rows, opened 2026-10-22)

Quotes are located and at most 25 words. earlyoom rows are pinned to tag `v1.9.0` = commit
`202d4db0d308ca6478f68de68b46cae34896ddaf`; systemd rows to tag `v262` = commit `8cc40e0c5e9234bf45084751ac53b1fbfe70b492`.
Full Gate blocks (sha256 of every fetched file, more quotes) are in the named wave-1 seat reports.

| Row | URL | Accessed | Located quote | Decision |
|---|---|---|---|---|
| S114 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/README.md | 2026-10-22 | :28 "By default if both are below 10%, it will kill the largest process (highest `oom_score`)." | admit, A, mined (SrcEarlyoomReadme) |
| S115 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md | 2026-10-22T13:14:31Z | :41-42 "earlyoom sends SIGTERM once **both** available memory **and** free swap are below their respective PERCENT settings." | admit, A, mined (SrcEarlyoomManpage) |
| S116 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/meminfo.c | 2026-10-22 | :115 "m.MemAvailablePercent = (double)m.MemAvailableKiB * 100 / (double)m.UserMemTotalKiB;" | admit, A, mined (SrcEarlyoomMeminfo) |
| S117 | https://api.github.com/repos/rfjakob/earlyoom/releases/tags/v1.9.0 | 2026-10-22 | release object: "published_at": "2025-09-16T19:11:03Z" | admit, A, mined (SrcEarlyoomTagHistory) |
| S118 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c | 2026-10-22 | :318 "escalating to SIGKILL after %.3f seconds\n" | admit, A, mined (SrcEarlyoomKillC) |
| S119 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c | 2026-10-22 | :414 "sending SIGTERM when mem avail <= " PRIPCT " and swap free <= " PRIPCT ",\n" | admit, A, mined (SrcEarlyoomMainC) |
| S120 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.service.in | 2026-10-22 | :7 "ExecStart=:TARGET:/earlyoom $EARLYOOM_ARGS" | admit, A, mined (SrcEarlyoomUnit) |
| S121 | https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-util.c | 2026-10-22 | :269 "r = increment_oomd_xattr(ctx->path, "user.oomd_ooms", 1);" | admit, A, mined (SrcOomdUtilV262; file byte-identical to v261) |
| S122 | https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml | 2026-10-22 | :599-600 "Fields containing non-printable or non-UTF8 bytes are encoded as arrays containing the raw bytes individually formatted as unsigned numbers." | admit, A, mined (SrcJournalJson) |
| S123 | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/logs-show.c | 2026-10-22 | :1131 "r = sd_json_variant_new_array_bytes(&v, value, size);" | admit, A, mined (SrcJournalJson) |
| S124 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml | 2026-10-22 | :1545-1546 "When set to auto, systemd-oomd will not actively use this cgroup's data for monitoring and detection." | admit, A, mined (opened by the L1) |
| S125 | https://raw.githubusercontent.com/VeigaPunk/tsukuroi-shokunin/157ee255/corpus/knowledge/memory-pressure-r25.md (sibling lane; also `git show 157ee255:…` in the local sibling repo) | 2026-10-22 | :204 "On this host systemd-oomd is inactive and disabled" | admit, B, mined — cite, never absorb (SrcSiblingTsukuroi) |
| S126 | https://gitlab.archlinux.org/archlinux/packaging/packages/earlyoom/-/raw/704e05715e672b5de664d543e734aa3f757af9bb/PKGBUILD | 2026-10-22 | :5-6 "pkgver=1.9.0" / "pkgrel=1" | admit, A, mined (SrcEarlyoomUnit) |

No row was rejected this round. `status`/`recheck`/`used-by` changes to existing rows: none (S016 stays as written;
its master-README scope is now named in the r12 entry line 6).

Spot-check: to be recorded by the non-author closure (at least one admit and one reject; this round admitted
13 rows and rejected none, so the closure may sample the round-25 rejects or an L1 non-admission — the per-boot
capture was kept as own-work evidence, not a SOURCES row).

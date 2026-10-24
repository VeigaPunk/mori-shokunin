# SrcOomdUtilV262 — SOURCES row draft (systemd v262 oomd-util.c + catalog)

Scope: re-verify at tag `v262` the round-12 facts held at `v261`
(`corpus/knowledge/userspace-oom-killers-r12.md:6,11-12`), and draft one `corpus/SOURCES.md` row
plus its Gate line. `corpus/SOURCES.md` was NOT edited (draft only). No lane commit, no jj, no
product-code edit.

## Verdict in one line

All three round-12 facts still hold at `v262`; only the catalog anchor moved
(`d989611b…` `:869` at v261 → `:884` at v262). `src/oom/oomd-util.c` is byte-identical between
v261 and v262, so every code line anchor is unchanged.

## Facts re-verified (round-12 claim → v262)

| Round-12 fact (r12 line) | At v262 | New line numbers | Verdict |
|---|---|---|---|
| `user.oomd_ooms` records one per oomd kill attempt (r12:6) | still true | `src/oom/oomd-util.c:269` (increment happens before the kill) | still true, line unchanged |
| `user.oomd_kill` records the number of PIDs killed (r12:6) | still true | `src/oom/oomd-util.c:306` (increment of `n_pids_killed`) | still true, line unchanged |
| D-Bus `Killed(path, reason)` signal emitted (r12:6, r12:11 `:316–319`) | still true | `src/oom/oomd-util.c:311–319` (`"Killed"` at `:316`, `ctx->path` `:318`, `reason` `:319`) | still true, line unchanged |
| catalog id `d989611b15e44c9dbf31e3c81256e4ed` (r12:6, r12:12 `:884–885`) | still true, **moved** | `catalog/systemd.catalog.in:884` (id), `:885` (subject), body `:890–895` | still true, moved +15 lines (was `:869` at v261) |
| "these userspace kill paths do not increment the kernel OOM counters" (r12:6) | unchanged in the cited code path | `src/oom/oomd-util.c:274` (`cg_kill_kernel_sigkill`), `:280` (`cg_kill_recursive`), `:289` (`cg_kill`) — all `SIGKILL` cgroup paths, no `__oom_kill_process` | still true (same bytes as v261) |

Not moved, not changed: nothing in the three cited facts. The catalog move is caused by a new,
unrelated catalog entry inserted earlier in the file (`-- 8d813b6becf04b859d99760cbb56dff1`, TPM
EK authorization, inserted at v261 line 825), plus one appended entry
(`-- eac6d394c925493deac2ba99f3c2bb11`, optional dependency, at the end of the file).

## Gate

Source 1

- URL: https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-util.c
- Access date: 2026-10-22 (HTTP 200)
- Bytes: 34,426 B, 927 lines; sha256 `2e94450aa337dd7d2062f2730e46e22ac00fc2c3195c11654047ddcaba487e7a`
- Tag provenance: `refs/tags/v262` → tag object `1f7dffaf714cc4488159c498b7a17cf34c5a96d5` →
  commit `8cc40e0c5e9234bf45084751ac53b1fbfe70b492`
- Quote, `src/oom/oomd-util.c:269` (verbatim, 8 words):
  > `r = increment_oomd_xattr(ctx->path, "user.oomd_ooms", 1);`
- Quote, `src/oom/oomd-util.c:306` (verbatim, 8 words):
  > `r = increment_oomd_xattr(ctx->path, "user.oomd_kill", n_pids_killed);`
- Quote, `src/oom/oomd-util.c:311–319` (verbatim, 15 words):
  > `/* send dbus signal */ if (m) (void) sd_bus_emit_signal(m->bus, "/org/freedesktop/oom1", "org.freedesktop.oom1.Manager", "Killed", "ss", ctx->path, reason);`

Source 2

- URL: https://raw.githubusercontent.com/systemd/systemd/v262/catalog/systemd.catalog.in
- Access date: 2026-10-22 (HTTP 200)
- Bytes: 38,320 B, 1,054 lines; sha256 `e53707db7e6963b284e504dc17f36a4d5a2bdb4bd8a9611b2cf95c075ad86592`
- Quote, `catalog/systemd.catalog.in:884` (verbatim, 2 words):
  > `-- d989611b15e44c9dbf31e3c81256e4ed`
- Quote, `catalog/systemd.catalog.in:885` (verbatim, 9 words):
  > `Subject: systemd-oomd killed one or more processes in unit @UNIT@`
- Quote, `catalog/systemd.catalog.in:890` (verbatim, 13 words):
  > `One or more processes in the @UNIT@ unit have been killed by systemd-oomd, in`

## Draft row (exact column order of `corpus/SOURCES.md`)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S??? | systemd v262 oomd kill accounting and oomd notice — https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-util.c ; https://raw.githubusercontent.com/systemd/systemd/v262/catalog/systemd.catalog.in | code | A | systemd-oomd's own kill accounting and its journal notice id at the v262 release tag: the `user.oomd_ooms` and `user.oomd_kill` cgroup xattrs, the `Killed(path, reason)` D-Bus signal, and MESSAGE_ID `d989611b15e44c9dbf31e3c81256e4ed`; not host service state, not kill history, not kernel OOM counters | src/oom/oomd-util.c:269 (`user.oomd_ooms`), :306 (`user.oomd_kill`), :311–319 (D-Bus `Killed`); catalog/systemd.catalog.in:884–885 (id and subject); tag v262 = commit 8cc40e0c5e9234bf45084751ac53b1fbfe70b492; HTTP 200 on 2026-10-22, 34,426 B, sha256 2e94450aa337dd7d2062f2730e46e22ac00fc2c3195c11654047ddcaba487e7a; 38,320 B, sha256 e53707db7e6963b284e504dc17f36a4d5a2bdb4bd8a9611b2cf95c075ad86592 | oomd counts one kill attempt in `user.oomd_ooms` before it kills and the killed-PID count in `user.oomd_kill` after, then announces the kill with the `Killed` D-Bus signal; the same event carries journal MESSAGE_ID `d989611b15e44c9dbf31e3c81256e4ed`, so an oomd kill is countable by message id without reading MESSAGE text. | mined | 2026-10-22 | on-release | corpus/knowledge/userspace-oom-killers-r26.md |

Tier A — reason: upstream release source code and the upstream message catalog at a released tag
(`v262`), fetched from the project's own raw endpoint; the same bytes are what the host's systemd
262 ships (`systemctl --version` → `systemd 262 (262-1-arch)`), and the installed catalog on this
host contains this message id.

Status `mined` — reason: the three facts are the anchors of the superseding round-26 entry
`corpus/knowledge/userspace-oom-killers-r26.md`, which cites this row in its `source:` line; the
row therefore has a consumer in this round. (If the L1 prefers the registry's "admitted but not yet
used" spelling, the same row text with status `queued` and used-by `—` is equally consistent; the
facts and Gate do not change.)

Split option — the registry keeps one row per URL for code (S011) and catalog (S013) files. If the
L1 wants that shape, the row above can be split into two rows with the same cells: the code row
keeps `src/oom/oomd-util.c` as its source and the anchors `:269, :306, :311–319`; the catalog row
keeps `catalog/systemd.catalog.in` as its source and the anchor `:884–885`. Both would be tier A
and `on-release`.

Registry note: `corpus/SOURCES.md` currently ends at **S113** (last registry row is at file line
119). The assignment mentioned "the last rows S098–S127"; rows S114–S127 do not exist yet, so the
next free id is `S114` — but the row above is written with the id left as `S???` as instructed.

## Facts the round can rest on (with line numbers)

1. oomd increments the `user.oomd_ooms` cgroup xattr by one **before** it kills —
   `src/oom/oomd-util.c:269` (v262).
2. oomd increments the `user.oomd_kill` cgroup xattr by the number of killed PIDs **after** the
   kill, and only when the killed count is known and non-zero — `src/oom/oomd-util.c:302–308`,
   increment at `:306` (v262).
3. oomd emits the D-Bus signal `Killed` with the cgroup path and the reason, on
   `org.freedesktop.oom1.Manager`, and only when a bus is present — `src/oom/oomd-util.c:311–319`
   (v262).
4. The oomd journal notice is MESSAGE_ID `d989611b15e44c9dbf31e3c81256e4ed`, subject
   "systemd-oomd killed one or more processes in unit @UNIT@" — `catalog/systemd.catalog.in:884–885`
   (v262).
5. The oomd kill path uses cgroup `SIGKILL` helpers, not the kernel's `__oom_kill_process` path —
   `src/oom/oomd-util.c:274`, `:280`, `:289` (v262). [INFERENCE] Therefore oomd kills do not
   increment the kernel OOM counters; unchanged from v261 because the file is byte-identical.
6. The oomd xattr helper increments a decimal counter read from the target cgroup path —
   `src/oom/oomd-util.c:50` (`increment_oomd_xattr`), so the xattr is cgroup-scoped and
   path-scoped, not a global counter.
7. The host runs systemd 262 (`systemctl --version` → `systemd 262 (262-1-arch)`), so the v262
   catalog is the host's release catalog; the host's installed catalog carries this message id
   (`journalctl --list-catalog` → `d989611b15e44c9dbf31e3c81256e4ed systemd: systemd-oomd killed
   one or more processes in unit @UNIT@`; `/usr/lib/systemd/catalog/systemd.be.catalog`).
   No journal MESSAGE text, process name, command line or uid was read or copied.

## Flags for the L1 / contract

- **No contradiction with the contract.** The contract's C2 live read
  (`journalctl -q -b MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed …`) uses exactly the message id
  that `catalog/systemd.catalog.in:884` defines at v262, and that id is present in this host's
  installed catalog. The contract's "systemd 262" host framing is consistent with the row.
- **Label change, not a fact change:** `corpus/knowledge/userspace-oom-killers-r12.md:6` says
  "systemd-oomd **v261** records its cgroup kills in …". The behavior is identical at v262 (same
  bytes), so the superseding r26 entry should say v262 (or "v261 and v262"), and r12:6 should be
  reworded as a dated past-tense record naming the superseding entry.
- **Additional staleness in r12 beyond the four frozen C1 phrases (not in the frozen list, so
  outside C1's counting command):** r12:2 records "systemd 261 (261.2-1-arch)" as the verified
  host version; this host is now systemd 262 (262-1-arch). r12:3's `recheck:` line still pins the
  v261 URL; the r26 entry's recheck should pin v262. C1's counting command only sees the four
  frozen phrases, so the L1 may treat these two as part of the same dated rewrite.
- **Adjacency, not absorption:** S011 (v261 code) and S013 (catalog at commit
  cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af) remain valid rows; this draft does not replace them.
  S013's `:884` anchor still points at the same oomd entry at v262: the catalog at the pinned
  commit `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af` is byte-identical to the v262 catalog
  (sha256 `e53707db…6592`, 1,054 lines) and carries the oomd id at `:884`. The v261 catalog had it
  at `:869`.
- **Coverage gap left open:** nothing here says whether oomd ever ran on this host, how many kills
  occurred, or what a notice's UNIT field is; the tool's `oomd_notices` count and the earlyoom
  grammar are other seats' scope.

## Verification trail

- `curl -fsSL -o oomd-util-v262.c https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-util.c`
  → rc 0; 34,426 B; sha256 as recorded above.
- `curl -fsSL -o systemd-catalog-v262.in https://raw.githubusercontent.com/systemd/systemd/v262/catalog/systemd.catalog.in`
  → rc 0; 38,320 B; sha256 as recorded above.
- `curl -sS -o /dev/null -w '%{http_code}\n'` for both URLs → 200, 200.
- Same commands against tag `v261` → `oomd-util.c` sha256
  `2e94450aa337dd7d2062f2730e46e22ac00fc2c3195c11654047ddcaba487e7a` (927 lines) and
  `cmp oomd-util-v261.c oomd-util-v262.c` → identical; `systemd.catalog.in` v261 sha256
  `00eca95e3656645a2ef0b4eb2197d0af2485d9ef5411f96616a9fbd59a579378` (1,026 lines),
  `diff -u` shows only two added entries (`8d813b6becf04b859d99760cbb56dff1` at v261 line 825 and
  `eac6d394c925493deac2ba99f3c2bb11` appended), and `grep -n` puts the oomd id at v261 `:869` and
  at v262 `:884`.
- `grep -n -E 'user\.oomd_(ooms|kill)'` on the v262 file → 269, 271, 306, 308.
- `grep -n -A7 'send dbus signal'` → 311 (`/* send dbus signal */`), 312 (`if (m)`), 313
  (`sd_bus_emit_signal`), 314 (`"/org/freedesktop/oom1"`), 315
  (`"org.freedesktop.oom1.Manager"`), 316 (`"Killed"`), 317 (`"ss"`), 318 (`ctx->path`), 319
  (`reason`).
- `grep -n` on the v262 catalog → 884 (id), 885 (subject), 890–895 (body); kernel-OOM notice
  `-- fe6faa94e7774663a0da52717891d8ef` at 604 (unchanged).
- `curl -fsSL https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in`
  → rc 0; 1,054 lines; sha256 `e53707db7e6963b284e504dc17f36a4d5a2bdb4bd8a9611b2cf95c075ad86592`
  (identical to the v262 catalog); `grep -n` puts the oomd id at `:884`.
- `curl -fsSL https://api.github.com/repos/systemd/systemd/git/ref/tags/v262` →
  tag object `1f7dffaf714cc4488159c498b7a17cf34c5a96d5`;
  `.../git/tags/1f7dffaf…` → commit `8cc40e0c5e9234bf45084751ac53b1fbfe70b492`.
- Host: `systemctl --version` → `systemd 262 (262-1-arch)`;
  `journalctl --list-catalog | grep d989611b15e44c9dbf31e3c81256e4ed` → one hit, the oomd subject.
  No unit was started, stopped, enabled or restarted; no journal entry text was read.

## Out of scope

- Editing `corpus/SOURCES.md`, `corpus/knowledge/userspace-oom-killers-r12.md` or any other lane
  file (draft only).
- The earlyoom v1.9.0 message grammar and the `tools/mori-oom-killers.py` interface (other seats).
- Any host kill history, host-wide unit census, or the C1/C2 claim counting.
- The GHSA-652q-wxr6-h5j6 advisory (S012, tsukuroi-owned adjacency).

## Tooling

- No install, upgrade or downgrade was performed; no tool was needed beyond what the host already
  provides (`curl`, `python3` for one JSON parse, `grep`, `cmp`, `diff`, `wc`, `sha256sum`).
- All pacman transactions are PAUSED host-wide per the round bounds, so none was attempted.
- Scratch copies of the fetched bytes live under
  `/fast/scratch/hyaku/mori-r26/MoriR26.SrcOomdUtilV262/` (`oomd-util-v262.c`,
  `oomd-util-v261.c`, `systemd-catalog-v262.in`, `systemd-catalog-v261.in`).
- Writes: this report file only. No jj command was run anywhere; no git write command was run;
  no lane commit was made.

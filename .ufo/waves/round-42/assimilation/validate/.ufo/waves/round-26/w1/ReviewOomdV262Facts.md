# Review: oomd v262 facts (freshness attack on r12, C1 support)

Seat: MoriR26.ReviewOomdV262Facts · 2026-10-22 · Leaf, read-only.
Target: `corpus/knowledge/userspace-oom-killers-r12.md:6,11-12,21` states systemd-oomd v261 facts;
host runs `systemd 262 (262-1-arch)` (`systemctl --version`, this host, 2026-10-22).
Question: do those facts hold at tag v262, so the r26 entry may restate them?

## Method

Fetched both tags fresh (not the L1 scratch copies) with curl on 2026-10-22, then diffed v261 vs v262:

| File (tag path) | v261 sha256 | v262 sha256 |
|---|---|---|
| `src/oom/oomd-util.c` | `2e94450aa337dd7d2062f2730e46e22ac00fc2c3195c11654047ddcaba487e7a` | same — byte-identical |
| `src/oom/oomd-manager.c` | `617f54237937c838428e4d78818051d92b996341ba3faf759d2d8f779a9e1fd0` | `052f19b36d54997b78c4ca93fae17d8c8513ce7240b0b58a47a1efdad0da3a15` |
| `catalog/systemd.catalog.in` | `00eca95e3656645a2ef0b4eb2197d0af2485d9ef5411f96616a9fbd59a579378` | `e53707db7e6963b284e504dc17f36a4d5a2bdb4bd8a9611b2cf95c075ad86592` |

URLs: `https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-util.c` (same for
`v261`), `.../v262/src/oom/oomd-manager.c`, `.../v262/catalog/systemd.catalog.in`.
Scratch copies: `/fast/scratch/hyaku/mori-r26/ReviewOomdV262Facts/`.
Tooling record: no install or upgrade needed; used system `curl`, `sha256sum`, `diff`, `grep` only.
Pacman untouched, per the round freeze.

The two changed files moved as follows: `oomd-manager.c` has exactly one changed line —
`1282: "io.systemd.service.GetLogLevel", varlink_method_get_log_level,` (a varlink method
registration); no kill, xattr, or signal line changed. `systemd.catalog.in` gained 28 lines, all two
new message-id entries (`8d813b6b…` near its line 825, `eac6d394…` at its end); no existing entry was
edited or removed. Since `oomd-util.c` is byte-identical, every r12 citation into it lands on the
same line number at v262.

## Verdicts per fact

| # | Fact (r12:6,11-12,21) | Verdict at v262 | Evidence |
|---|---|---|---|
| 1 | `user.oomd_ooms`, one per kill attempt, written before the kill | holds at v262 — same line | oomd-util.c:269-271 |
| 2 | `user.oomd_kill`, number of PIDs killed, written after the kill | holds at v262 — same line | oomd-util.c:305-308 |
| 3 | D-Bus `Killed(path, reason)` | holds at v262 — same line | oomd-util.c:311-319 |
| 4 | SIGKILL to all processes in the selected cgroup | holds at v262 — same lines | oomd-util.c:274,280,289 |
| 5 | catalog notice `d989611b15e44c9dbf31e3c81256e4ed` | holds at v262 — new line | systemd.catalog.in:884 (v261:869) |

None changed, none unverifiable. All five are decided by direct byte comparison or tagged-source
reading, not inference.

## Detail and quotes (verbatim, tagged v262 files, accessed 2026-10-22)

1. **`user.oomd_ooms`** — written once per `oomd_cgroup_kill` call, before any kill is sent, so it
   counts attempts even when the kill then fails (the error return at `:298-300` comes after the
   increment). oomd-util.c:269: `r = increment_oomd_xattr(ctx->path, "user.oomd_ooms", 1);`
2. **`user.oomd_kill`** — written after the kill, by the PID count. oomd-util.c:306:
   `r = increment_oomd_xattr(ctx->path, "user.oomd_kill", n_pids_killed);` Precision for the r26
   entry: it is written only when `n_pids_killed` is not `0` and not `UINT64_MAX` (`:305`), i.e. when
   at least one PID died and the count is known; the kernel-assisted path (`:274`) can leave the
   count unknown, in which case the xattr is not written.
3. **D-Bus `Killed(path, reason)`** — oomd-util.c:313-319 emits `sd_bus_emit_signal(...,
   "/org/freedesktop/oom1", "org.freedesktop.oom1.Manager", "Killed", "ss", ctx->path, reason)`.
   Signature `"ss"` = path then reason. Guarded by `if (m)` (`:312`): a caller that passes no
   Manager gets no signal. All kill entry points pass the manager (`oomd-manager.c:505,624,705,733,766`
   via `oomd_cgroup_kill_mark`, which kills through `oomd-util.c:366` with `recurse=true`).
4. **SIGKILL to all processes** — the recursive kill used by oomd prefers the kernel-assisted path
   oomd-util.c:274: `r = cg_kill_kernel_sigkill(ctx->path, &n_pids_killed);` and falls back on
   `-EOPNOTSUPP` to `cg_kill_recursive(ctx->path, SIGKILL, ...)` at `:280`; the non-recursive branch
   uses `cg_kill(ctx->path, SIGKILL, ...)` at `:289`. So "sends SIGKILL to all processes in the
   selected cgroup" (r12:12, citing the S007 Description) is realized by this code at v262.
5. **Catalog `d989611b…`** — present at v262 `catalog/systemd.catalog.in:884`, unchanged text:
   `Subject: systemd-oomd killed one or more processes in unit @UNIT@` (`:885`). It moved from line
   869 in v261 because two new entries were inserted above it. Note r12:12 already cites S013 at the
   pinned commit `cf8ebfc6…` with the range `:884-885`; at the v262 tag the entry sits at exactly
   `:884-885` too, so a restated citation can pin tag `v262` and keep that range.

## Consequence for C1 / the r26 entry

The r26 entry MAY restate all five r12 oomd facts. Restating is not a freshness defect, but the
citations must be re-pinned so the entry is v262-clean, not v261-worded:

- Rewrite `systemd-oomd v261 records…` (r12:6) as version-neutral or "v262" wording; the code is
  identical between v261 and v262 in `oomd-util.c`, so the facts carry over without loss.
- The `recheck:` line (r12:3) and S011 still name `v261` URLs; a restatement should name `v262` and
  cite oomd-util.c:269, 306, 313-319 (same numbers as v261).
- The catalog citation should pin `v262` (`systemd.catalog.in:884-885`).

Suggested ready-to-paste sentence for the r26 entry:

```
oomd facts re-verified at systemd tag v262 (2026-10-22): `src/oom/oomd-util.c` is byte-identical to
v261 (sha256 2e94450a…), so `user.oomd_ooms` (before the kill, :269), `user.oomd_kill` (after, by
known PID count, :305-308), D-Bus `Killed(path, reason)` (:313-319) and the SIGKILL-to-all-paths
(:274/:280/:289) all hold at v262; the catalog notice `d989611b15e44c9dbf31e3c81256e4ed` holds at
`catalog/systemd.catalog.in:884-885` (moved from v261:869; two unrelated entries added above it).
```

## Residual risk and verification gaps

- The v262 tag is upstream; Arch's `262-1-arch` could carry downstream patches. I did not fetch the
  Arch PKGBUILD diff. [INFERENCE] For `oomd-util.c` this risk is cosmetic: the xattr/signal behavior
  is what the tagged source says, and the entry cites the tag, not the distro package.
- I did not fetch the S007 man page (outside my assigned file set); the "SIGKILL to all processes"
  fact was verified against the implementing kill paths in `oomd-util.c` instead of the Description
  wording. If the r26 entry quotes the Description sentence itself, it must open S007 separately.
- No runtime check: oomd is inactive on this host, so no xattr was read and no D-Bus listener was
  run (also outside this review's scope). The verdicts are source-level facts at the tag.
- r12's earlyoom claims (README lines, `--kernel-oom`) are out of scope here; C2's earlyoom work and
  the earlyoom v1.9.0 seat cover them.

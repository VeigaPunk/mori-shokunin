# SrcEarlyoomServiceRestart — frontier source row for C1 (earlyoom unit `Restart=`)

Seat: `MoriR30.SrcEarlyoomServiceRestart` (leaf; no subagents, no background jobs).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` — read-only for this seat; no lane or fleet git/jj writes.
Scratch: `/fast/scratch/hyaku/mori-r30/SrcEarlyoomServiceRestart/` (downloads + sandbox clone only).
No tool install or update was needed (nothing installed; no pacman run).

## Behavior

1. Screened the assigned candidate URL against `corpus/SOURCES.md` before opening it.
2. The candidate is already row S120, so it cannot become a new row; I opened a non-duplicate primary
   artifact that carries the same directive with dated provenance: upstream commit
   `edd3d9438dc564da7b694e5c96c9b3bc63bef2ac`, patch URL.
3. Verified the chain in a `--no-hardlinks` sandbox clone: the directive was introduced by that commit
   only, and no later commit up to v1.9.0 changed it.
4. Drafted one ready-to-paste row, one admit Gate line, two reject Gate lines, and the excerpt body.

## Registry screening (all commands run in the lane root, read-only)

- `grep -n 'raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.service.in' corpus/SOURCES.md`
  → `126:| S120 | earlyoom systemd unit template earlyoom.service.in at v1.9.0 — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.service.in ... :17 (Restart=always)`.
  Exact-URL duplicate; CORPUS.md `## SOURCES.md` rule 2 makes rows append-only, so the candidate is barred.
- `grep -n 'git/trees/v1.9.0?recursive=1' corpus/SOURCES.md` → `157:| S151 | ...` (same tree URL).
- `grep -c 'edd3d9438dc564da7b694e5c96c9b3bc63bef2ac' corpus/SOURCES.md` → `0`.
- `grep -c 'github.com/rfjakob/earlyoom/commit/' corpus/SOURCES.md` → `1` (S155, `ca2251fc…`, a different commit).
- `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `155`; last id `S155`, so `S156` is next free.
  The drafts keep the assigned placeholder `S15x`.

## Sources opened this round

1. **Admitted candidate** — `https://github.com/rfjakob/earlyoom/commit/edd3d9438dc564da7b694e5c96c9b3bc63bef2ac.patch`
   - `curl -sS -o edd3d94.patch -w 'http %{http_code} bytes %{size_download}'` → `http 200 bytes 1180`,
     39 lines, sha256 `dc5a771c9ed178751c0473c9ada89152e70b9da13a048b0af30df6bbb1f2a9a1`.
   - Access time `2026-10-22T21:13:43Z` (`date -u +%FT%TZ` immediately before the fetch).
   - Quotes (`wc -w` on each quoted text): `:6-7` (13 words) "Have systemd restart us should we get killed
     or crash for some reason."; `:34-36` (21 words) "# earlyoom never exits on it's own, so have systemd" /
     "# restart it should it get killed for some reason." / "Restart=always".
2. **Rejected candidate** — the assigned `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.service.in`
   - `curl -sS …` → `http 200 bytes 1340`, 51 lines, sha256 `d4019b66d87539a006fc2d178d972dcf1b46e70343627b8bf66d1a08dcdda0bd`,
     access `2026-10-22T21:13:43Z`. `:17` is `Restart=always`; `:15-16` is the same intent comment.
     Reject reason: duplicate of S120.
3. **Rejected probe** — `https://api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0?recursive=1`
   - `http 403 bytes 280`, sha256 `2282f9baf641a8417b97a1785119fd62f08e3560b50fdecfae2019fff3ae259d`,
     access `2026-10-22T21:12:19Z`. Body line 1: `API rate limit exceeded` (the rest of the body names the
     caller's address; not quoted). `x-ratelimit-remaining: 0`, `x-ratelimit-reset: 1792706275`.
     Reject reason: no body to screen, and the URL is S151's first URL.

## Provenance chain verified in the sandbox clone

Scratch clone: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks https://github.com/rfjakob/earlyoom upstream`

- `git log --format='%h %ad %s' --date=short -G'Restart' -- earlyoom.service.in`
  → `edd3d94 2020-03-01 earlyoom.service: set Restart=always` (the only hit; `-G` catches value edits too,
  unlike `-S`).
- `git merge-base --is-ancestor edd3d94 v1.9.0` → exit 0 (printed `edd3d94 is ancestor of v1.9.0`).
- `git show v1.9.0:earlyoom.service.in | grep -n 'Restart'` → `17:Restart=always`.
- `git diff edd3d94 v1.9.0 -- earlyoom.service.in | grep -n 'Restart'` → one unchanged context line, `Restart=always`.
- `git rev-parse v1.9.0^{commit}` → `202d4db0d308ca6478f68de68b46cae34896ddaf` (commit date 2025-09-16).

## Draft 1 — SOURCES.md row (append after S155)

```
| S15x | earlyoom commit edd3d9438dc564da7b694e5c96c9b3bc63bef2ac "earlyoom.service: set Restart=always" — https://github.com/rfjakob/earlyoom/commit/edd3d9438dc564da7b694e5c96c9b3bc63bef2ac.patch | code | A | the introduction of `Restart=always` in earlyoom's systemd unit template on 2020-03-01 only: the directive, the comment beside it, the commit message's killed-or-crash purpose, and the Makefile change that adds the generated unit to `all`; not the v1.9.0 file bytes (S120 carries `:17`), not systemd's own `Restart=` wording (systemd.service(5), not opened this round), not this host's unit state or restart history | patch :4 (subject), :6-7 (message), :21-22 (Makefile `all:` target), :34-36 (comment and directive); commit authored 2020-03-01T11:00:34+01:00; sandbox clone checks: `git log -G'Restart' -- earlyoom.service.in` names this commit only, `git merge-base --is-ancestor edd3d94 v1.9.0` holds, `git show v1.9.0:earlyoom.service.in` gives `17:Restart=always`; patch 1,180 B sha256 dc5a771c9ed178751c0473c9ada89152e70b9da13a048b0af30df6bbb1f2a9a1; HTTP 200, 2026-10-22T21:13:43Z | The unit's own comment and the commit message state the purpose of `Restart=always` — systemd restarts a daemon that was killed or crashed — so an earlyoom exit of that kind is followed by a fresh process that reprints its startup version line (S119:161). | mined | 2026-10-22 | 180d | corpus/lessons/round-30.md, corpus/knowledge/earlyoom-invocation-scope-r30.md |
```

Column check after writing: the row has 11 cells (`awk -F'|'` NF=13 with the outer pipes); no `|` inside any cell.

## Draft 2 — Gate line for `corpus/lessons/round-30.md` (admit)

```
| S15x | https://github.com/rfjakob/earlyoom/commit/edd3d9438dc564da7b694e5c96c9b3bc63bef2ac.patch | 2026-10-22T21:13:43Z | `dc5a771c9ed178751c0473c9ada89152e70b9da13a048b0af30df6bbb1f2a9a1` | `:6-7` (13 words): "Have systemd restart us should we get killed or crash for some reason."; `:34-36` (21 words): "# earlyoom never exits on it's own, so have systemd" / "# restart it should it get killed for some reason." / "Restart=always" | admit, A, mined |
```

## Draft 3 — Gate lines for the rejected candidates (`corpus/lessons/round-30.md`)

```
| S15x | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.service.in | 2026-10-22T21:13:43Z | `d4019b66d87539a006fc2d178d972dcf1b46e70343627b8bf66d1a08dcdda0bd` (1,340 B, 51 lines) | `:17` (1 word): "Restart=always" | reject, duplicate URL — S120 (corpus/SOURCES.md:126) opens this exact URL and already anchors `:17 (Restart=always)`; a second row would repeat the same bytes |
| S15x | https://api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0?recursive=1 | 2026-10-22T21:12:19Z | `2282f9baf641a8417b97a1785119fd62f08e3560b50fdecfae2019fff3ae259d` (280 B) | body line 1 (4 words): "API rate limit exceeded" | reject, HTTP 403 rate limit (`x-ratelimit-remaining: 0`), no tree body to screen; the URL is also already S151's first URL (corpus/SOURCES.md:157) |
```

## Draft 4 — excerpt file body `corpus/evidence/sources-r30/S15x.txt`

Blank patch lines inside the range are omitted; line numbering is preserved and every non-blank line of
`:6-36` appears verbatim, including the quoted lines.

```
id: S15x
url: https://github.com/rfjakob/earlyoom/commit/edd3d9438dc564da7b694e5c96c9b3bc63bef2ac.patch
sha256: dc5a771c9ed178751c0473c9ada89152e70b9da13a048b0af30df6bbb1f2a9a1
accessed: 2026-10-22T21:13:43Z
lines: 6-36

6	Have systemd restart us should we get killed
7	or crash for some reason.
8	---
9	 Makefile            | 2 +-
10	 earlyoom.service.in | 3 +++
11	 2 files changed, 4 insertions(+), 1 deletion(-)
13	diff --git a/Makefile b/Makefile
14	index a3db17f0..0ceba897 100644
15	--- a/Makefile
16	+++ b/Makefile
17	@@ -14,7 +14,7 @@ endif
19	 .PHONY: all clean install uninstall format test
21	-all: earlyoom earlyoom.1
22	+all: earlyoom earlyoom.1 earlyoom.service
24	 earlyoom: $(wildcard *.c *.h) Makefile
25	 	$(CC) $(LDFLAGS) $(CFLAGS) -o $@ $(wildcard *.c)
26	diff --git a/earlyoom.service.in b/earlyoom.service.in
27	index 2df9330e..ad802385 100644
28	--- a/earlyoom.service.in
29	+++ b/earlyoom.service.in
30	@@ -13,6 +13,9 @@ AmbientCapabilities=CAP_KILL CAP_IPC_LOCK
31	 ProtectSystem=strict
32	 # We don't need /home at all, make it inaccessible
33	 ProtectHome=true
34	+# earlyoom never exits on it's own, so have systemd
35	+# restart it should it get killed for some reason.
36	+Restart=always
```

## Findings

- **What the row buys.** The v1.9.0 unit already carries `Restart=always` (S120:17, inside S120's anchor).
  The new row supplies the provenance and the maintainer's own purpose statement — restart after a kill or a
  crash — which S120's `scope` text does not include. It does not re-open the v1.9.0 bytes as new evidence.
- **One gap, explicit.** The patch and the unit comment say "killed or crash", not "clean exit". The
  clean-exit half of the question ("whether an earlyoom *exit* yields a fresh invocation") rests on the
  meaning of the literal value `Restart=always`, which is systemd's own documentation (systemd.service(5) at
  v262) — **not opened this round**. Treat that half as **[INFERENCE]** and, if a C1 decision-table row
  depends on a clean exit, open a separate systemd `Restart=` row (one-row scope was assigned here).
- **Scope tension worth the judge's attention, verbatim from the registry.** S120's scope cell reads:
  "the upstream unit template only: how earlyoom is configured and what its hardening permits it to read;
  the generated earlyoom.service and the Arch packaging delta are separate sources". Its anchor nevertheless
  lists `:17 (Restart=always)`. The new row therefore complements S120 rather than superseding it; no
  correction to S120 is proposed, because CORPUS.md rule 2 permits only status/recheck/used-by edits in place.
- **A `new version line` needs its own row.** The row cites S119:161 for the startup version line; it does not
  re-open `main.c` this round. If C1 asserts the reprinted line, S119 must stay `mined` and cited.
- **Privacy scan.** The excerpt excludes patch line 2 (the author's e-mail address). A regex scan of excerpt
  lines `6-36` for `@`, `user@<digits>`, `user-<digits>.slice`, `uid=`/`pid=`, and host-unit names produced
  hits only on the upstream filename `earlyoom.service.in` and the Makefile `$@` variable — no e-mail, uid,
  pid, slice, host unit name, or `/etc/default/earlyoom` value. No host journal text was read for this seat.
- **No lane file other than this report was written.** The clone ran under the scratch dir with
  `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE` unset. No unit was started, stopped or restarted; no process
  was signalled; no harness or MCP file touched.
- **Missing destinations.** `corpus/lessons/round-30.md` and `corpus/evidence/sources-r30/` do not exist yet
  (`ls` in the lane root); the L1 owner creates them and assigns the real id (next free `S156`).

## Out of scope (not done, by bounds)

- No C2 work: no tool fix, no fixture, no blindness-gate change, no counter run.
- No lane commit, no git/jj write, no message to any seat other than this report.

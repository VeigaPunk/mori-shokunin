# SourceEarlyoomDryrun — frontier source row for C2 (earlyoom v1.9.0 dry-run)

Seat `MoriR29.SourceEarlyoomDryrun`, leaf (no subagents, no background jobs). Lane
`/home/vgpnk/Projects/shokunin/mori-shokunin`, HEAD read at `8a45cefe84af0557b457308e4e0f679ca490f9e9`
(read-only `git rev-parse`). Read the round-29 contract first (`contract.md:1-100`).
No tool installed, nothing upgraded, no pacman transaction. No unit started or stopped, no
process signalled, no omp run, no git or jj write in the lane or fleet.

## Duplicate check on the two named candidates (both already rowed)

`grep -n "raw.githubusercontent.com/rfjakob/earlyoom" corpus/SOURCES.md` (2026-10-22T19:55:38Z)
returns the two named URLs inside existing rows:

- `.../v1.9.0/kill.c` is in S118 (`corpus/SOURCES.md:124`) and in S117 (`:123`).
  S118's anchor list already contains `kill.c:272`.
- `.../v1.9.0/MANPAGE.md` is in S115 (`corpus/SOURCES.md:121`); its scope names `--dryrun`.

Neither is admissible as a new row. I then searched the v1.9.0 tag tree
(`https://api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0?recursive=1`, 200,
sha256 `8b3c95cf88d0b8c58bbe973c1b6846c34063a258b7edfaeb57320f5dfbf3c145`, the same digest
round 28 recorded for S151) for another file carrying the facts. Every v1.9.0 file that carries
them is already rowed: `main.c` and `msg.h` (S119), `kill.c` and `msg.c` (S118), `MANPAGE.md`
(S115), `README.md` (S114), `Makefile` (S151), the tree itself (S131, S151). Novel probes
`testsuite_cli_test.go`, `testsuite_helpers.go`, `globals.c` and `kill.h` were opened and do not
carry the strings (see rejects). A v1.9.0 source tarball was considered and **not** opened: its
members that carry the facts are the already-rowed files, so it would be a duplicate in
substance.

## Admitted carrier: the commit that introduced `--dryrun`

The fact has an independent primary artefact at a novel URL: the upstream patch that added the
option. It contains, verbatim, both the startup line and the send-site no-op, plus the option
spelling.

- URL: `https://github.com/rfjakob/earlyoom/commit/ca2251fcd222af8c857aec4a26e182cf5f9c596e.patch`
- Access time: `2026-10-22T19:59:28Z` (`date -u +%FT%TZ` in the same shell call), HTTP 200
- sha256 of the fetched bytes: `893e238ea3b7f512f0506ccc87e0decfea8846e2e4b0704c51ced2820465d4bb` (2 978 B, 92 lines)
- Identity: `From ca2251fcd222af8c857aec4a26e182cf5f9c596e`, `Date: Tue, 3 Mar 2020 20:38:03 +0800`,
  `Subject: [PATCH] main: add dry-run option` (patch `:1-4`)

Located quotes (verbatim, `patch` line numbers, the `+` prefix is the diff's):

1. `:35-38` (17 words): `if (args.dryrun && sig != 0) { warn("dryrun, not actually sending any signal\n"); return 0; }`
2. `:79-82` (14 words): `case LONG_OPT_DRYRUN: warn("dryrun mode enabled, will not kill anything\n"); args.dryrun = 1; break;`
3. `:21-22` (9 words): `#### \-\-dryrun` / `dry run (do not kill any processes)`
4. `:71` (11 words): `{ "dryrun", no_argument, NULL, LONG_OPT_DRYRUN },` — the option table's spelling
5. `:90` (16 words): `"  --dry-run                 dry run (do not kill any processes)\n"` — the help text's spelling

The same strings hold at the claimed tag: fetched v1.9.0 `main.c` (200, 21 053 B, sha256
`08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4`, 2026-10-22T20:00:28Z) prints
`fprintf(stderr, "earlyoom " VERSION "\n");` at `:161` and `warn("dryrun mode enabled, will not kill anything\n");`
at `:295`; fetched v1.9.0 `kill.c` (sha256 `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3`,
identical to the digest S118 records) guards at `:271-274` with the pointer form
`if (args->dryrun && sig != 0) { warn("dryrun, not actually sending any signal\n"); return 0; }`.
So the patch grounds the grammar and the semantics, and S118/S119 remain the tag-pinned anchors.

## Ready-to-paste SOURCES.md row

Append after S152 (`corpus/SOURCES.md:158`); the L1 assigns the id in place of `S15x`.

```
| S15x | earlyoom commit ca2251fcd222 "main: add dry-run option" — https://github.com/rfjakob/earlyoom/commit/ca2251fcd222af8c857aec4a26e182cf5f9c596e.patch | code | A | the introduction of earlyoom's dry-run option only: the option-parser startup line it prints, the send-site guard that returns before any signal is sent, the flag spelling in the option table, and the manual and help-text wording added with it; not the v1.9.0 line numbers of the same strings (S118:271-274, S119:295), not the version line (S119:161), not the v1.9.0 manual text (S115), not any host configuration | patch :21-22 (`#### \-\-dryrun` and its one-line description), :35-38 (guard inside `kill_wait`, returning before `kill()`), :71 (option table spells the flag `dryrun`), :79-82 (parser prints `dryrun mode enabled` then sets the flag), :90 (help text spells it `--dry-run`); commit ca2251fcd222af8c857aec4a26e182cf5f9c596e authored 2020-03-03T20:38:03+08:00; patch 2 978 B sha256 893e238ea3b7f512f0506ccc87e0decfea8846e2e4b0704c51ced2820465d4bb, opened 2026-10-22T19:59:28Z | A dry run is a send-site no-op: `kill_wait` returns before `kill()`, so a `dryrun, not actually sending any signal` line records a decision and never a delivery. | mined | 2026-10-22 | 180d | corpus/lessons/round-29.md, tools/fixtures/mori-oom-killers/cases-a2-r29.json |
```

## Ready-to-paste Gate lines

Shape copied from `corpus/lessons/round-28.md:63-72` (header `| id | source | access time | sha256 | located quote | decision |`).

```
| id | source | access time | sha256 | located quote | decision |
|---|---|---|---|---|---|
| S15x | https://github.com/rfjakob/earlyoom/commit/ca2251fcd222af8c857aec4a26e182cf5f9c596e.patch | 2026-10-22T19:59:28Z | `893e238ea3b7f512f0506ccc87e0decfea8846e2e4b0704c51ced2820465d4bb` | patch `:35-38` (17 words): "if (args.dryrun && sig != 0) { warn(\"dryrun, not actually sending any signal\n\"); return 0; }" | admit, A, mined |
| — | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c | 2026-10-22T19:59:10Z | `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` | `:272` (8 words): "warn(\"dryrun, not actually sending any signal\n\");" | reject, duplicate URL — S118 rows v1.9.0 kill.c and already anchors `:272` |
| — | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md | 2026-10-22T19:59:10Z | `cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda` | `:205-206` (9 words): "#### \-\-dryrun" / "dry run (do not kill any processes)" | reject, duplicate URL — S115 rows the v1.9.0 manual with `--dryrun` in its scope |
| — | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/testsuite_cli_test.go ; https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.h | 2026-10-22T19:56:07Z | `1dc876421c856bde48ab4a63304dab838c585f79c68a807d52b0741d366eb795` (9 317 B) ; `abf8577b434096e1eb980bacc24508e8421af9edbefb0d78cf5b8b5f28160bfb` (1 440 B) | `kill.h:36-37` (8 words): "/* Flag --dryrun was passed */" / "bool dryrun;" | reject, does not carry the fact — kill.h only declares the flag field, and a case-insensitive grep for `dryrun` and `version` returned no line in either file |
```

## Facts the C2 case writers can pin (all source-level, no host run)

1. Startup order: the version line goes to **stderr** at `main.c:161`
   (`"earlyoom " VERSION "\n"`), before `/proc` is entered at `:163`; the dry-run line
   `dryrun mode enabled, will not kill anything` is printed by the option parser at `:295-296`.
   Both in the same row S119.
2. A dry run still reaches the send site: `kill_process` logs
   `sending %s to process ...` at `kill.c:626-629` and calls `kill_wait` at `:640`; `kill_wait`
   returns 0 at `:271-274` before the signal call `kill_release(pid, pidfd, sig)` at `:293`. So a
   dry-run run emits the action line, then `dryrun, not actually sending any signal`, and never
   signals. This is the substance behind A2-07 `earlyoom.dryrun_send_lines`.
3. Flag spelling: the option table registers `dryrun` at v1.9.0 `main.c:184`, and v1.9.0 prints
   `--dryrun` in its help text at `main.c:332` and in the manual at `MANPAGE.md:205-206`. The
   introducing commit's help text instead printed `--dry-run` (patch `:90`); a follow-up commit
   whose message is "Fix \"--dryrun\" help text" (`af958c6de47514ac8de3866be4a1e3a5eb7866b9`,
   author date 2020-03-14T18:16:32Z) exists in the `main.c` history listing. I did not open that
   diff, so what it changed is [INFERENCE]; the v1.9.0 spelling above is observed directly.
   Consequence for cases: `--dry-run` is not a v1.9.0 option — only `--dryrun` enables dry-run.
4. Startup self-test, do not miscount it: `startup_selftests` at `main.c:67-73` calls
   `kill_process(args, 0, &victim)` with signal 0. The dry-run guard tests `sig != 0`
   (`kill.c:271`), so the self-test passes through to `kill(pid, 0)`, which checks permission and
   sends nothing; the `sending 0 (no-op signal) to process ...` line is printed only when
   `enable_debug` is set (`kill.c:622-623,626`). A `--dryrun -d` run therefore emits one send-
   looking line at startup that is not a dry-run kill decision and must not be counted as one.
5. The version-line half of my topic has **no** novel carrier: it stays at S119:161. The new row
   deliberately scopes itself to the dry-run half rather than restating S119.

## Limits and corrections

- Corrections to my own first attempt: I built the full sha by hand as `ca2251fcd2225fb64...` and
  that mistyped `.patch` URL returned HTTP 404 (9-byte body). The real sha is
  `ca2251fcd222af8c857aec4a26e182cf5f9c596e` and its `.patch` is 200. No reject is recorded for
  that 404 because it was my typo, not a dead candidate.
- `api.github.com` unauthenticated rate limit was exceeded at `2026-10-22T19:58:13Z` (HTTP 403,
  `.message` "API rate limit exceeded"). The introducing commit was found from the paginated
  `commits?path=main.c` listing (200, 403 197 B) and the patch was fetched from `github.com`, not
  the API, so no admitted fact depends on the rate-limited endpoint.
- Everything here is source reading. No earlyoom binary was executed and no dry run was observed
  on this host; the claim that the two log lines appear in that order in a live run is
  [INFERENCE] from `main.c:161`, `main.c:295-296`, `kill.c:626-640` and `kill.c:271-274`.
- `tools/fixtures/mori-oom-killers/cases-a2-r29.json` does not exist at HEAD (`ls` of
  `tools/fixtures/mori-oom-killers/` shows `cases-a2.json`, `cases-supplementary.json` and
  `cases.json` only); the row's `used-by` entry is therefore a forward reference. The L1 must make
  the case file's top-level `sources` key cite the assigned id, or the row's `mined` status is
  unearned (CORPUS.md:103-108).
- `corpus/lessons/round-29.md` does not exist yet either (the lessons directory holds only
  `round-28*.md`); the `used-by` half is the round lesson the L1 writes.
- Blindness held: I did not open `tools/mori-oom-killers.py`, any copy of it, or any report under
  `.ufo/waves/round-26/`, `round-27/` or `round-28/{w1,w2}/`. The only round-28 file I read is
  `corpus/lessons/round-28.md:55-80`, for the Gate shape, which my item names.
- Host privacy: no settings values, session ids, uid/pid, unit names or host `earlyoom` arguments
  appear in this report; all concrete values quoted are upstream source text.

## Files touched

- Write: `.ufo/waves/round-29/w1/SourceEarlyoomDryrun.md` (this file).
- Read-only: `corpus/SOURCES.md`, `corpus/lessons/round-28.md`, `.ufo/waves/round-29/contract.md`,
  `/home/vgpnk/Projects/shokunin/CORPUS.md:64-140`, the lane `git rev-parse`.
- Network (GET only): the raw v1.9.0 files and tag tree named above, the commit patch, and
  `api.github.com` listings. No source row was edited; the row and Gate lines above are drafts.

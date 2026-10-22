# ReopenS131 — re-open of SOURCES row S131 at tip 5f00fd04

Seat: MoriR27.ReopenS131 (leaf, read-only). Tip: `5f00fd045c137b7e3835506d69946cfd9d010eb5` (master).
Bytes read with `git show <tip>:<path>` into `/fast/scratch/hyaku/mori-r27/ReopenS131/`. No lane write and no git
write ran in the lane. Tip `corpus/SOURCES.md`: sha256 `77f5ea37f6fad772950e78a9c5da20dbc8364dcacbe83ccefef2938a6bbc22a8`,
196 lines; the S131 row is line 137.

## 1. Verdict in brief

- Identity and hashes HOLD: tag v1.9.0 = commit `202d4db0…`, tree `bc0d30aa…`, commit date `2025-09-16T19:09:23Z`;
  `earlyoom.default` blob `ba4f5c9f…`, sha256 `c0770413…`, 563 B, 21 lines; the quoted line `:5` holds.
- The tree URL named in the row is WRONG (F1, high). The URL without a query returns other bytes than the listing
  whose sha256, size and anchors the row records. The listing the row describes is `…/git/trees/v1.9.0?recursive=1`.
- Three teaching or scope items are wrong or unsupported (F2–F4, medium). One citing statement in the entry is
  wrong for this host's package (F5, medium). Four wording items are low (F6–F9).
- Not a duplicate: no older row names `earlyoom.default`, the tag tree listing, the Makefile or the init script.

## 2. Method (ordinary public HTTPS and a public git clone; 2026-10-22, `date -u` 17:10–17:14Z)

- Named tree URL, no query → HTTP 200, 8,757 B, 253 lines, sha256 `92f8c2c9…d271fad0` (scratch `tree.json`).
- `…/git/trees/v1.9.0?recursive=1` → HTTP 200, 19,112 B, 536 lines, sha256 `8b3c95cf…f3c145` (`tree-rec.json`).
- Raw `earlyoom.default`, `Makefile`, `earlyoom.service.in`, `earlyoom.initscript.in` at v1.9.0 → HTTP 200 each.
- Public clone of the tag into scratch (`--no-checkout --filter=blob:none`) for `rev-parse`, `ls-tree`, `grep`.
- API commit JSON `…/commits/202d4db0…` (4,901 B) and `…/git/trees/bc0d30aa…?recursive=1` (19,112 B).
- S126 PKGBUILD (GitLab raw, 17:13:05Z) → HTTP 200, 1,179 B, sha256 `f48dc3f9…b46dd4a2`, equal to the S126 row.
- Anchors checked with `grep -n` / `sed -n` on those bytes. Quotes are at most 12 words. Secrets, values and host
  data are not copied; the PKGBUILD and upstream option values are cited by line only.

## 3. Findings

### F1 — HIGH — the tree URL in the row does not return the bytes the row describes

- Row, `corpus/SOURCES.md:137`, source cell: `https://api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0`.
- That URL today: 8,757 B, sha256 `92f8c2c9…`; 31 top-level entries; `"truncated": false` at line 252
  (`grep -n '"truncated"' tree.json`); `earlyoom.default` at line 92.
- The `?recursive=1` URL: 19,112 B, sha256 `8b3c95cf…`; 67 entries (60 blob, 7 tree); `"truncated": false` at line 535;
  `"path": "earlyoom.default"` at 375, `earlyoom.initscript.in` at 383, `earlyoom.service.in` at 391. Path, type and blob id
  of all 67 entries equal `git ls-tree -r -t v1.9.0`.
- Origin: the wave-1 draft row, `.ufo/waves/round-27/w1/SrcEarlyoomManpageOptions.md:198`, carries the query-less URL,
  while its own Gate block (same file, line 127) says "(recursive)". The admitted row copies the draft cell for cell;
  only the id changed (`S???` → `S131`).
- Round 26 fetched the same recursive bytes (`.ufo/waves/round-26/w1/SrcEarlyoomTagHistory.md:253-254`).
- Correction, `corpus/SOURCES.md:137`: old `git/trees/v1.9.0 ;` → new `git/trees/v1.9.0?recursive=1 ;`.
- Residual risk: no tree JSON is committed at the tip (`git ls-tree -r --name-only` finds none), so a reader can
  re-check `tree.json:535`, `:375`, `:383`, `:391` only by fetching the recursive URL.

### F2 — MEDIUM — "any such expression observed on a host is local configuration" is wrong for an Arch host

- Row teaches, `corpus/SOURCES.md:137`: "…so any such expression observed on a host is local configuration, …".
- The S126 PKGBUILD, line 22, is a `sed` that appends `-n` and an `--avoid` expression to the `EARLYOOM_ARGS` line of
  `earlyoom.default` in the Arch copy. Line 14 declares `etc/default/earlyoom` a backup file. The expression value is
  not copied here.
- The row's own scope excludes this delta: "not the Arch package delta (S126)".
- The entry records earlyoom 1.9.0-1 on this host (`corpus/knowledge/oom-victim-selection-r27.md:2`).
  [INFERENCE] the host's packaged default carries the appended option unless the operator changed the file. The host
  file was not read (bounds).
- Correction (teaches), replace `so any such expression observed on a host is local configuration,` with
  `so a prefer, avoid or ignore expression on a host is not upstream's default: it is local configuration or a
  distribution packaging change (on Arch, S126 PKGBUILD:22 appends an --avoid option),`.

### F3 — MEDIUM — "exactly one configuration file" is a name-pattern result stated as a definition

- Row teaches: "The v1.9.0 tag ships exactly one configuration file".
- Its basis is a name match. The only path whose name matches `default|config|conf` (case-insensitive, all 67 entries)
  is `earlyoom.default` (`tree-rec.json:375`; `git ls-tree -r v1.9.0 | grep -i -E 'default|config|conf'` → one line).
- Other configuration-format files ship in the tag: `.clang-format` (`tree-rec.json:6`), `.github/workflows/ci.yml`
  (`:28`), `.github/workflows/codeql.yml` (`:36`), `.gitignore` (`:44`), `Dockerfile` (`:60`), `go.mod` (`:415`),
  `go.sum` (`:423`), five nested `.gitignore` files (`:115`, `:146`, `:177`, `:264`, `:303`). The unit template
  `earlyoom.service.in` (`:391`) is installed as a systemd unit (`Makefile:41-43`).
- The narrow reading holds: `earlyoom.default` is the only file the Makefile installs under `$(SYSCONFDIR)/default`
  (`Makefile:55-57`).
- Correction (teaches), replace `The v1.9.0 tag ships exactly one configuration file` with `The v1.9.0 tag ships
  exactly one default-settings file (the only path name matching default|config|conf, tree.json:375) and the only file
  the Makefile installs under $(SYSCONFDIR)/default (Makefile:55-57)`.

### F4 — MEDIUM — a wrong scope pointer, and anchors into files that no named URL provides

- Scope cell: "not the unit or init-script template content (S120)". S120 names only `earlyoom.service.in`
  (`corpus/SOURCES.md:126`). No row names `earlyoom.initscript.in` or the upstream `Makefile`:
  `git grep -n -E 'initscript|Makefile' <tip> -- corpus/SOURCES.md` returns only `:132` (S126, the Arch PKGBUILD text)
  and `:137` (S131).
- Anchors `Makefile:41,47,55-57`, `earlyoom.initscript.in:31,52` and `tree.json:383` rest on bytes the source cell
  does not name. The consumption clause of the teaches rests on `earlyoom.initscript.in:31` and `earlyoom.service.in:6-7`.
- Bytes at tag v1.9.0 (raw; blob ids equal the tag tree): `Makefile` sha256 `b852cb9b…96127ae` (2,898 B, 99 lines,
  blob `80720107…`); `earlyoom.initscript.in` sha256 `70456226…509890` (4,532 B, 163 lines, blob `faf12bf6…`);
  `earlyoom.service.in` sha256 `d4019b66…dda0bd` (1,340 B, 51 lines, blob `091b041e…`).
- Correction (scope), replace `not the unit or init-script template content (S120)` with `not the unit template
  content (S120 covers only earlyoom.service.in); the Makefile and init-script lines are cited here only as consumers
  of the file`. Also add to the source cell `; https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/Makefile ;
  https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.initscript.in` with the three hashes above in the
  anchor cell. Or drop those anchors and the init-script clauses. Either way, state the method for the consumption
  clause (T5 below).

### F5 — MEDIUM — the entry says no avoid expression exists by default; true for upstream only

- `corpus/knowledge/oom-victim-selection-r27.md:50-51`: "No prefer, avoid or ignore expression exists by default (S115
  has none; the shipped `earlyoom.default` sets only `EARLYOOM_ARGS="-r 3600"`, S131 `earlyoom.default:5`)."
- The S131 part holds: `earlyoom.default:5` is the only active assignment in the upstream file.
- The "by default" part is wrong for the file this host's package installs (S126 PKGBUILD:22; F2). The entry is about
  this host.
- Correction: replace the sentence at :50-51 with `Upstream has no prefer, avoid or ignore expression as an active
  default (S115 has none; upstream earlyoom.default, S131 earlyoom.default:5, sets only EARLYOOM_ARGS="-r 3600"); the
  Arch package appends an --avoid option to its copy (S126 PKGBUILD:22).`

### F6 — LOW — the teaches omits the commented avoid example

- "no prefer, avoid or ignore expression is a shipped default" holds for active lines. `earlyoom.default:19` is a
  commented `--avoid` example. Correction: append `; the file's only avoid text is a commented example at :19`.

### F7 — LOW — two anchor paraphrases

- `earlyoom.default:1-2 sourced by /bin/sh or read by systemd`. Bytes: "sourced by /bin/sh from /etc/init.d/earlyoom or by
  systemd from earlyoom.service." Correction: `sourced by /bin/sh from /etc/init.d/earlyoom or by systemd from
  earlyoom.service`.
- `$EARLYOOM_ARGS passed at earlyoom.service.in:6-7 and earlyoom.initscript.in:31,52`. Line `service.in:6` and line
  `initscript.in:31` are the source lines; `service.in:7` and `initscript.in:52` pass the variable. Correction: `$EARLYOOM_ARGS
  passed at earlyoom.service.in:7 and earlyoom.initscript.in:52, both sourcing the default file (service.in:6,
  initscript.in:31)`.

### F8 — LOW — the service-template anchors re-cite S120's file

- `earlyoom.service.in:6-7` are S120's anchors (`corpus/SOURCES.md:126`). No second row exists for that file, so this
  is duplicate anchoring, not a duplicate row. Correction: point to S120 for those lines instead of re-anchoring.

### F9 — LOW — the Gate row names no tree URL or hash

- `corpus/lessons/round-27.md:74`: "(with the v1.9.0 tag tree)". Correction: `(with
  https://api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0?recursive=1, sha256 8b3c95cf…f3c145)`. The quote and
  the decision hold (C5 below).

## 4. Anchor-by-anchor verdicts (row at `corpus/SOURCES.md:137`)

| # | Anchor as written | Bytes at that line (grep -n) | Verdict |
|---|---|---|---|
| A1 | tree.json:535 truncated false | recursive: 535 `"truncated": false`; named URL: 252 | HOLDS for `?recursive=1`; WRONG for the named URL (F1) |
| A2 | 67 entries and 60 blobs | recursive: 67 entries (60 blob, 7 tree); `ls-tree -r -t` 60 + 7 | HOLDS for recursive; named URL has 31 (F1) |
| A3 | only default/config/conf path = earlyoom.default at tree.json:375 | recursive :375 `"path": "earlyoom.default"`; tag-wide name scan: one hit | HOLDS |
| A4 | earlyoom.default:1-2 sourced by /bin/sh or read by systemd | :1 "This file is sourced by /bin/sh from"; :2 "/etc/init.d/earlyoom or by systemd from earlyoom.service." | HOLDS in substance; paraphrase (F7) |
| A5 | :5 active EARLYOOM_ARGS=-r 3600 | :5 `EARLYOOM_ARGS="-r 3600"`; the only uncommented assignment | HOLDS |
| A6 | :10,13,16,19 commented examples | each of :10, :13, :16, :19 is `# EARLYOOM_ARGS=…` | HOLDS; :19 is an --avoid example (F6) |
| A7 | :21 see-more trailer | :21 "# See more at `earlyoom -h'" | HOLDS |
| A8 | Makefile:41,47,55-57 install-default copies it to $(SYSCONFDIR)/default/earlyoom | :41 `install: earlyoom.service install-bin install-default install-man`; :47 `install-initscript: … install-default`; :55 `install-default: earlyoom.default install-man`; :56 `install -d $(DESTDIR)$(SYSCONFDIR)/default/`; :57 `install -m 644 $< $(DESTDIR)$(SYSCONFDIR)/default/earlyoom` | HOLDS; Makefile named by no URL (F4) |
| A9 | earlyoom.initscript.in at tree.json:383 | recursive :383 | HOLDS; file named by no URL (F4) |
| A10 | earlyoom.service.in at tree.json:391 | recursive :391 | HOLDS; S120's file (F8) |
| A11 | $EARLYOOM_ARGS passed at earlyoom.service.in:6-7 | :6 `EnvironmentFile=-:SYSCONFDIR:/default/earlyoom`; :7 `ExecStart=:TARGET:/earlyoom $EARLYOOM_ARGS` | HOLDS for :7; :6 is the source line (F7) |
| A12 | earlyoom.initscript.in:31,52 | :31 `[ -r :SYSCONFDIR:/default/$NAME ] && . :SYSCONFDIR:/default/$NAME`; :52 `exec $DAEMON $EARLYOOM_ARGS` | :52 HOLDS; :31 is a source line (F7); file named by no URL (F4) |
| A13 | tag v1.9.0 = commit 202d4db0… | `git rev-parse v1.9.0^{commit}` = `202d4db0d308ca6478f68de68b46cae34896ddaf`; API commit JSON sha256 `ecf9ac00…` | HOLDS |
| A14 | tree bc0d30aabe… | `git rev-parse v1.9.0^{tree}` = `bc0d30aabe03e441577dccbe35b8d95ea3e28bce`; commit JSON `tree.sha` equal | HOLDS |
| A15 | commit date 2025-09-16T19:09:23Z | `git log -1 --format=%cI v1.9.0` = `2025-09-16T21:09:23+02:00` (= 19:09:23Z); commit JSON committer date equal | HOLDS |
| A16 | earlyoom.default blob ba4f5c9f… | `git hash-object earlyoom.default` = `ba4f5c9f…`; `tree-rec.json:378`; clone `rev-parse v1.9.0:earlyoom.default` equal | HOLDS |
| A17 | HTTP 200, 563 B, 21 lines | curl 200; `wc -c` 563; 21 newline-terminated lines | HOLDS |
| A18 | sha256 c0770413… | `sha256sum earlyoom.default` = `c0770413a180e0731583f643fc4e84f4a0dac57efb8f575b74ee9a971df984a2` | HOLDS |
| A19 | tree listing HTTP 200, 19,112 B, sha256 8b3c95cf… | recursive: 200, 19,112 B, `8b3c95cf…`; named URL: 200, 8,757 B, `92f8c2c9…` | HOLDS for recursive; WRONG for named URL (F1) |
| A20 | opened 2026-10-22 | fetched 2026-10-22 17:10–17:14Z | HOLDS |

Scope pointers and teaches clauses:

| # | Clause | Bytes and sources | Verdict |
|---|---|---|---|
| S1 | "not the Arch package delta (S126)" | S126 row (`SOURCES.md:132`) names the PKGBUILD; sha256 `f48dc3f9…` matches my fetch | HOLDS |
| S2 | "not the README example args (S114)" | S114 row (`SOURCES.md:120`) names README at v1.9.0 (pointer only) | HOLDS |
| S3 | "not the unit or init-script template content (S120)" | S120 names only `earlyoom.service.in` (`SOURCES.md:126`); no row names the init script | WRONG for the init script (F4) |
| S4 | "v1.9.0 tag only" | every fetched file is the tag (`rev-parse` equality; raw URLs at v1.9.0) | HOLDS |
| T1 | "ships exactly one configuration file" | see F3 | WRONG as worded; holds for the sysconfdir reading |
| T2 | "EARLYOOM_ARGS carries only a report interval (-r 3600)" | `:5` only; `README.md:343` calls the setting a memory report interval; `-r` meaning per S115 (`SOURCES.md:121`) | HOLDS |
| T3 | "no prefer, avoid or ignore expression is a shipped default" | no active line carries one; `:19` commented example | HOLDS (F6 wording) |
| T4 | "so any such expression observed on a host is local configuration" | not in the bytes; S126 PKGBUILD:22 appends an avoid option | WRONG for Arch hosts (F2); unsupported in general |
| T5 | "consumed only through the systemd unit or the init script" | tag-wide `git grep` (EARLYOOM_ARGS, default/, SYSCONFDIR): `Makefile:57` installs; `earlyoom.initscript.in:31,52`; `earlyoom.service.in:6-7`; `README.md:214` tells operators to edit, reads nothing | HOLDS for the tag; UNSUPPORTED by the row's own named sources (F4) |

Scope as a whole: not wider than the bytes; wider than the named sources (F4).

## 5. Citing statements (every lane statement that cites S131)

The search was `git -C <lane> grep -n 'S131' 5f00fd04`. Its hits: `corpus/SOURCES.md:137`; `corpus/knowledge/oom-victim-selection-r27.md:1` and `:51`; `corpus/lessons/round-27.md:74`; `.ufo/waves/round-27/w1/ReviewR3SkillRows.md:58` and `:174`.

| # | Where | Statement | Verdict |
|---|---|---|---|
| C1 | `corpus/SOURCES.md:137` | the S131 row | see F1–F4, F6–F8 |
| C2 | `corpus/knowledge/oom-victim-selection-r27.md:1` | "S131 (earlyoom v1.9.0 tag tree and earlyoom.default — the shipped default arguments)" | HOLDS as a label; "shipped" means upstream |
| C3 | `…oom-victim-selection-r27.md:50-51` | "No prefer, avoid or ignore expression exists by default (… S131 `earlyoom.default:5`)" | S131 part HOLDS; "by default" WRONG for this host's package (F5); correction in F5 |
| C4 | `…oom-victim-selection-r27.md:51` | "the shipped `earlyoom.default` sets only `EARLYOOM_ARGS="-r 3600"`" | HOLDS for upstream bytes (`:5`) |
| C5 | `corpus/lessons/round-27.md:74` | Gate row: URL, 2026-10-22T15:46:30Z, quote `:5` `EARLYOOM_ARGS="-r 3600"`, admit A mined | quote HOLDS (line 5 byte-exact); decision HOLDS; access time UNVERIFIABLE from bytes (wave-1 record, `SrcEarlyoomManpageOptions.md:119`); no tree URL (F9) |
| C6 | `corpus/lessons/round-27.md:63-66` | full Gate blocks with hashes are in the named wave-1 reports | HOLDS for S131: `SrcEarlyoomManpageOptions.md:126-129` carry the hashes; all reproduced (section 6) |
| C7 | `.ufo/waves/round-27/w1/ReviewR3SkillRows.md:58` | "the registry reaches at least S131 today (32 rows matching `^| S1` today)" | HOLDS as a snapshot: S100–S131 are 32 rows at tip; the tip now has 42 such rows (S100–S141) |
| C8 | `.ufo/waves/round-27/w1/ReviewR3SkillRows.md:174` | "the registry reaches at least S131 today" | HOLDS |

`corpus/SKILL.md` does not cite S131 (`git grep -n S131` at tip: no SKILL hit); its Round27 grounding list (`SKILL.md:722`)
names S003, S118, S127, S129, S130, S132 and no SKILL row depends on the default file.

## 6. Hashes and identity

`corpus/lessons/round-27.md:74` records no hash for S131: its Gate row carries a URL, an access time, a quote and a decision. The hashes below come from the row (`corpus/SOURCES.md:137`) and from the wave-1 Gate block (`SrcEarlyoomManpageOptions.md:126-129`).

| Item | Recorded by | Reproduced 2026-10-22 | Verdict |
|---|---|---|---|
| earlyoom.default sha256 `c0770413…` | row; `SrcEarlyoomManpageOptions.md:126` | yes | HOLDS |
| earlyoom.default blob `ba4f5c9f…` | row; wave-1 `:126` | yes (`git hash-object`; clone) | HOLDS |
| tree listing `?recursive=1` sha256 `8b3c95cf…`, 19,112 B | row (URL wrong, F1); wave-1 `:127` "(recursive)" | yes for the recursive URL; no for the row's URL | HOLDS for recursive; F1 |
| commit `202d4db0…` JSON sha256 `ecf9ac00…`, 4,901 B | wave-1 `:128` (not in row) | yes | HOLDS |
| tree `bc0d30aa…?recursive=1` sha256 `82ea84a9…`, 19,112 B | wave-1 `:129` (not in row) | yes; 67 entries equal the 202d4db0 listing | HOLDS |
| Gate quote `:5 EARLYOOM_ARGS="-r 3600"` | `round-27.md:74` | yes (`grep -n` line 5) | HOLDS |
| Makefile sha256 `b852cb9b…` | nothing recorded | recorded here | new (F4) |
| earlyoom.initscript.in sha256 `70456226…` | nothing recorded | recorded here | new (F4) |
| S131 row cells since first publication | `check-row-identity.py` (run read-only) | S131 not flagged | HOLDS |

## 7. Duplicate check

- No older row names `earlyoom.default` or `git/trees`: `git grep` at tip finds S131 (`SOURCES.md:137`) only.
- S117 (`SOURCES.md:123`) names the tags and releases API and `main.c`, `kill.c`, `msg.h`, `README.md` at v1.9.0, not the
  tree listing. Round 26 used the recursive listing as a supporting observation (`SrcEarlyoomTagHistory.md:253-254`),
  not as a row.
- No older row names the upstream `Makefile` or `earlyoom.initscript.in` (`SOURCES.md:132` names the Arch PKGBUILD only).
- Round 26's wave-1 seat drafted the same `earlyoom.default` row (`.ufo/waves/round-26/w1/SrcEarlyoomUnit.md:217`) and
  no round-26 row landed; S131 is the first admission.
- Overlap only: `earlyoom.service.in:6-7` is S120's anchor set (F8).
- Verdict: HOLDS, not a duplicate.

## 8. Out of scope, observed (not verified by me beyond the run)

- `check-row-identity.py` (copied to scratch, run against the lane's git read-only at 5f00fd04): `rows=141 changed=5`,
  exit 1: S090 (anchor, teaches), S093 (anchor), S096 (teaches), S097 (anchor, teaches), S101 (teaches). S131 not flagged.
- `count-c1.sh` at 5f00fd04 (read-only): `entry=present new_rows_cited=6 skill_rows=10`, `C1=met`, exit 0. S131 is one
  of the counted rows (status `mined`; used-by names the entry, `SOURCES.md:137`).

## 9. Tooling and privacy

- Installs or upgrades: none. Tools used as already present: curl 8.23.0; git 2.56.0 (public clone into scratch with
  `--no-checkout --filter=blob:none`; no lane write); Python 3.14.8 (`-I -B`, JSON reading only); sha256sum (version
  string `0.8.0` as printed); GNU awk 5.4.1; grep; sed. No pacman, sudo, service or unit action.
- I read the tooling rules file named in the wave bounds after the checks, not before as the bounds ask. It permits
  installs that help the task; none were needed.
- Privacy: no host value, uid, pid, command line, journal text, session or settings path was copied. The PKGBUILD and
  upstream option values are cited by line only. The only host fact used is the version string `1.9.0-1` from the entry.
- Lane git: every lane call was read-only (`show`, `grep`, `log`, `ls-tree`, `rev-parse`, `cat-file`) except one
  `git status --short`, which can refresh the index stat cache. No commit, ref or tracked content changed.

## 10. Verification gaps and residual risk

- The wave-1 access time `2026-10-22T15:46:30Z` cannot be checked from bytes. My fetches at 17:10–17:14Z returned the
  same sha256 for every file, so the content has been stable for about 1.5 hours. That does not prove the earlier time.
- The tree JSON comes from an API. Two fetches 84 minutes apart (15:46Z wave-1, 17:10Z mine) gave the same sha256. A
  later API change could move it.
- Host state was not read (bounds). The host-level statements in F2 and F5 are [INFERENCE] from the packaging files.
- Consumption (T5) was checked by a `git grep` over the whole tag clone, which covers all 60 blobs.
- Not checked: the S114, S115, S120 and S126 rows beyond their pointers; those belong to their own seats.
- Fix constraint (L1 decides): `check-row-identity.py:4-5` quotes CORPUS.md Rules 2, allowing in-place change only to
  status, recheck and used-by. F1–F4 change frozen cells, so an in-place edit of S131 trips the check. Use a logged
  correction (S124/S133 pattern) or a superseding row. CORPUS.md itself was not read.

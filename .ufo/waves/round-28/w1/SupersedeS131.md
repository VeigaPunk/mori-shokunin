# SupersedeS131 — S131 row defects (tree URL missing `?recursive=1`, teaches F2–F4): re-open, verified paste row, Gate line, sweep

seat: MoriR28.SupersedeS131 (leaf; no subagent dispatch; no background job)
lane: /home/vgpnk/Projects/shokunin/mori-shokunin
tip examined: 6ebd518f (round-27 verifier spot-check); round-28 head at read time 763d3469 (amendment A1)
scratch: /fast/scratch/hyaku/mori-r28/SupersedeS131/ (no lane writes; one sandbox clone; commits only in that clone)
lane writes by this seat: this report file only

## 0. Summary

- Carried defect (round-27 rout defect 4, `corpus/lessons/round-27-verifier-spotcheck.md:150`): the S131 row names the
  v1.9.0 tag tree URL **without** `?recursive=1` while its anchors describe the recursive listing (F1), and its
  `teaches` makes three statements the bytes do not support (F2, F3, F4 of `w2/ReopenS131.md`).
- The S131 row is byte-identical to its first publication: `git log --reverse -S'| S131 |'` gives one commit,
  `126e192d`, and the extracted row line is byte-equal at `126e192d` and `6ebd518f` (2111 bytes each, sha256
  `523cd78460f82ef1f306a27a551831c77934d4e8c3309deb20eea5b664443121`). `check-row-identity.py` does not flag S131
  (it is not among `changed=`), meaning the row was never edited in place — the defect is **in the first-published
  cells themselves** (contrast S096/S097/S101, which were edited in place and restored). Therefore the only compliant
  remedy is a superseding row, exactly what C1 declares; there is nothing to restore.
- Re-opened today (2026-10-22T17:59:23Z–18:00:29Z): the tag tree listing with and without `?recursive=1`, the raw
  `earlyoom.default`, `Makefile`, `earlyoom.initscript.in`, `earlyoom.service.in`, the commit JSON and the Arch
  PKGBUILD, plus an ordinary public clone of tag `v1.9.0`. Every statement the corrected row makes was checked
  against those bytes (section 3). All hashes reproduced; no bot challenge; no `?recursive=1`-less URL produces the
  recorded listing.
- Ready-to-paste: row **S151** (section 4) and its Gate line (section 5). The row passed the amended round-28 C1
  counter checks for the S151:S131 pair in a sandbox clone and passed the fleet census `validate` (exit 0, only the
  six pre-existing W04 warnings).
- **Reader sweep required by the counter** (contract amendment A1; `readers_left=0`): the live reader
  `corpus/knowledge/oom-victim-selection-r27.md:1` and `:48` cite `S131` as a word and must move to `S151`
  (section 7). This is the L1's edit; this seat wrote nothing in the lane.

## 1. First-published cells versus the tip

First commit carrying `| S131 |` in `corpus/SOURCES.md`:

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --reverse --format='%H %ad %s' --date=iso -S'| S131 |' -- corpus/SOURCES.md
126e192d1fa92675bbaabdcfa7fa1b389f01791c 2026-10-22 12:58:23 -0300 round-27: C1 entry oom-victim-selection-r27, SOURCES S127-S132 and used-by anchors, ...
```

The row sits at line 137 at both `126e192d` and `6ebd518f`. Extracted whole-line comparison:

```
sha256sum row-first.txt row-tip.txt
523cd78460f82ef1f306a27a551831c77934d4e8c3309deb20eea5b664443121  row-first.txt (126e192d)
523cd78460f82ef1f306a27a551831c77934d4e8c3309deb20eea5b664443121  row-tip.txt (6ebd518f)
diff row-first.txt row-tip.txt -> (empty)
```

**No cell differs.** The defect is first-published content; `check-row-identity.py` at `6ebd518f` prints
`rows=144 changed=3 removed=0 bad=0` with `changed` = S096, S097, S101 only. QUALITY 81 therefore allows no in-place
edit of S131; C1's superseding row is the sole mechanism.

## 2. Sources re-opened today (ordinary curl into scratch; no bot challenge)

| URL | accessed (UTC) | HTTP | bytes / lines | sha256 | notes |
|---|---|---|---|---|---|
| https://api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0 | 2026-10-22T17:59:23Z | 200 | 8757 / 253 | 92f8c2c92834cf092ce612a7d464a354b44b19ab589f004db7eccdd2d271fad0 | 31 top-level entries; `"truncated": false` at `:252`; `earlyoom.default` path at `:92` |
| https://api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0?recursive=1 | 2026-10-22T17:59:24Z | 200 | 19112 / 536 | 8b3c95cf88d0b8c58bbe973c1b6846c34063a258b7edfaeb57320f5dfbf3c145 | 67 entries (60 blob, 7 tree); `"truncated": false` at `:535`; `earlyoom.default` at `:375`, `earlyoom.initscript.in` at `:383`, `earlyoom.service.in` at `:391` |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.default | 2026-10-22T17:59:24Z | 200 | 563 / 21 | c0770413a180e0731583f643fc4e84f4a0dac57efb8f575b74ee9a971df984a2 | blob `ba4f5c9f4204154d7ee30cab54ea28ebf851c809` (git hash-object + clone rev-parse agree) |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/Makefile | 2026-10-22T17:59:25Z | 200 | 2898 / 99 | b852cb9b832729f37f2b19fe93956720a5a58017aa8f76a6036cc928d96127ae | blob `8072010737773d1cd9e65be04b5a3e1a289a4c82` |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.initscript.in | 2026-10-22T17:59:25Z | 200 | 4532 / 163 | 704562265c0275577f645de310d4efa010028cbde1e18b04ab29c78630509890 | blob `faf12bf6d794adfdc07682722619fe4427294f2b` |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.service.in | 2026-10-22T17:59:25Z | 200 | 1340 / 51 | d4019b66d87539a006fc2d178d972dcf1b46e70343627b8bf66d1a08dcdda0bd | S120's file (blob `091b041e85589b92508a02cd5ee3351311f0d546`) |
| https://api.github.com/repos/rfjakob/earlyoom/commits/202d4db0d308ca6478f68de68b46cae34896ddaf | 2026-10-22T17:59:47Z | 200 | 4901 / 101 | ecf9ac003b02555ed97870d193a14d5558f2882b4a92971a336da08abb97492d | `sha` = 202d4db0…; `tree.sha` = bc0d30aabe…; author & committer date 2025-09-16T19:09:23Z |
| https://gitlab.archlinux.org/archlinux/packaging/packages/earlyoom/-/raw/704e05715e672b5de664d543e734aa3f757af9bb/PKGBUILD | 2026-10-22T17:59:47Z | 200 | 1179 | f48dc3f99aee5d6a93f8cad4e4b6286dab014745aa6f85b1c3582c3db46dd4a2 | equals S126's recorded sha256; `:22` is a `sed … -ri earlyoom.default` appending an `--avoid` option (value withheld) |
| public clone https://github.com/rfjakob/earlyoom.git (tag v1.9.0) | 2026-10-22T18:00:29Z | — | clone | — | `rev-parse v1.9.0^{commit}` = 202d4db0…; `^{tree}` = bc0d30aa…; `ls-tree -r -t` = 67 lines, 60 blob, 7 tree |

## 3. Claim-by-claim verdicts (against the bytes in section 2)

| # | statement | bytes | verdict |
|---|---|---|---|
| 1 | the row's URL (no query) returns the listing the anchors describe | no-query fetch: 31 entries, 8757 B, sha256 92f8c2c9…, `truncated:false` at `:252` | **fails** (F1) |
| 2 | `?recursive=1` returns 67 entries / 60 blobs / `"truncated": false` at `:535` | recursive fetch `:535`; 67 `"path"` entries; 60 blob + 7 tree | holds |
| 3 | only path whose name contains default/config/conf is `earlyoom.default` | recursive listing grep over all 67 `"path"` lines → only `:375`; `git ls-tree -r v1.9.0 --name-only \| grep -icE 'default|config|conf'` → 1 | holds |
| 4 | `earlyoom.default:1-2` sourced by `/bin/sh` from `/etc/init.d/earlyoom` or by systemd from `earlyoom.service` | `:1` "This file is sourced by /bin/sh from"; `:2` "/etc/init.d/earlyoom or by systemd from earlyoom.service." | holds (fixes F7 paraphrase) |
| 5 | `:5` is the only active `EARLYOOM_ARGS` assignment, `"-r 3600"` | `:5` `EARLYOOM_ARGS="-r 3600"`; `:10,13,16,19` commented | holds |
| 6 | `:19` is the file's only avoid text, a commented example | `:19` `# EARLYOOM_ARGS="--avoid …"` (commented; expression value withheld) | holds (F6) |
| 7 | `:21` see-more trailer | `:21` "# See more at `earlyoom -h'" | holds |
| 8 | Makefile `:41,47,55-57` install-default copies it to `$(SYSCONFDIR)/default/earlyoom`, the only file installed under that directory | `:41` install target incl. install-default; `:47` install-initscript incl. install-default; `:55` `install-default: earlyoom.default install-man`; `:56` `install -d $(DESTDIR)$(SYSCONFDIR)/default/`; `:57` `install -m 644 $< … /default/earlyoom`; only `default/` install lines are `:56-57` | holds |
| 9 | the two template paths in the listing are `earlyoom.initscript.in` at `:383` and `earlyoom.service.in` at `:391` | recursive listing `:383`, `:391` | holds |
| 10 | `$EARLYOOM_ARGS` passed at `earlyoom.initscript.in:52`; the init script sources the default file at `:31` | `:31` `[ -r :SYSCONFDIR:/default/$NAME ] && . :SYSCONFDIR:/default/$NAME`; `:52` `exec $DAEMON $EARLYOOM_ARGS` | holds |
| 11 | the unit passes the variable at `earlyoom.service.in:7` and reads the file at `:6` | `:6` `EnvironmentFile=-:SYSCONFDIR:/default/earlyoom`; `:7` `ExecStart=:TARGET:/earlyoom $EARLYOOM_ARGS` | holds (S120's anchors) |
| 12 | tag v1.9.0 = commit 202d4db0…, tree bc0d30aa…, commit date 2025-09-16T19:09:23Z | clone rev-parse; commit JSON `sha`/`tree.sha`/dates | holds |
| 13 | other config-format files ship in the tag | recursive listing: `.clang-format` `:6`, `.github/workflows/ci.yml` `:28`, `.github/workflows/codeql.yml` `:36`, `.gitignore` `:44`, Dockerfile `:60`, `go.mod` `:415`, `go.sum` `:423`, five nested `.gitignore` files `:115,146,177,264,303` | holds |
| 14 | Arch packaging appends an `--avoid` option to the shipped `EARLYOOM_ARGS` | PKGBUILD `:22` is `sed … -ri earlyoom.default` containing `--avoid` and `EARLYOOM_ARGS` (value withheld) | holds (F2/F5) |

## 4. Ready-to-paste row S151

Insert after the S144 row (`corpus/SOURCES.md:150` at the tip). Scope is corrected per F4, source cell gets the
`?recursive=1` URL plus the two consumer-file URLs, anchor carries located line numbers and digests with today's
access times, and `teaches` opens exactly `supersedes S131 — ` (em dash), then what the old row got wrong and the
corrected teaching.

```
| S151 | earlyoom v1.9.0 tag tree and its shipped default-configuration file — https://api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0?recursive=1 ; https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.default ; https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/Makefile ; https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.initscript.in | code | A | which files the v1.9.0 tag ships as configuration and what the shipped default args are: the one default-settings file, its active and commented EARLYOOM_ARGS lines, its sourcing contract, and the Makefile rule that installs it; v1.9.0 tag only; not this host's /etc/default/earlyoom file or its values, not the Arch package delta (S126), not the README example args (S114), not the unit template content (S120 covers earlyoom.service.in only); the Makefile and init-script lines are cited here only as consumers of the file | recursive tag listing https://api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0?recursive=1 (19,112 B, 536 lines, sha256 8b3c95cf88d0b8c58bbe973c1b6846c34063a258b7edfaeb57320f5dfbf3c145, opened 2026-10-22T17:59:24Z):535 truncated false over 67 entries and 60 blobs, and the only path whose name contains default, config or conf is earlyoom.default at listing:375; earlyoom.default (563 B, 21 lines, sha256 c0770413a180e0731583f643fc4e84f4a0dac57efb8f575b74ee9a971df984a2, blob ba4f5c9f4204154d7ee30cab54ea28ebf851c809):1-2 sourced by /bin/sh from /etc/init.d/earlyoom or by systemd from earlyoom.service, :5 the only active EARLYOOM_ARGS=-r 3600, :10,13,16,19 commented examples (:19 the file's only avoid text), :21 see-more trailer; Makefile (2,898 B, 99 lines, sha256 b852cb9b832729f37f2b19fe93956720a5a58017aa8f76a6036cc928d96127ae):41,47,55-57 install-default copies it to $(SYSCONFDIR)/default/earlyoom, the only file the tag installs under that directory; the two template paths in the same listing are earlyoom.initscript.in at listing:383 (4,532 B, 163 lines, sha256 704562265c0275577f645de310d4efa010028cbde1e18b04ab29c78630509890) and earlyoom.service.in at listing:391 (S120's file, 1,340 B, 51 lines, sha256 d4019b66d87539a006fc2d178d972dcf1b46e70343627b8bf66d1a08dcdda0bd); $EARLYOOM_ARGS passed at earlyoom.initscript.in:52, the init script sourcing the default file at earlyoom.initscript.in:31, and by the systemd unit (S120: earlyoom.service.in:7 passes $EARLYOOM_ARGS, :6 reads the default file); tag v1.9.0 = commit 202d4db0d308ca6478f68de68b46cae34896ddaf, tree bc0d30aabe03e441577dccbe35b8d95ea3e28bce, commit date 2025-09-16T19:09:23Z; opened 2026-10-22 | supersedes S131 — the old row named the tag tree without ?recursive=1, so its URL returned 31 top-level entries and not the 67-entry listing its anchors described, and it stated two things the bytes do not support: that the tag ships exactly one configuration file (earlyoom.default is the only path whose name contains default, config or conf and the only file the Makefile installs under $(SYSCONFDIR)/default, but the tag also ships .clang-format, the two GitHub workflow files, .gitignore and five nested .gitignore files, Dockerfile, go.mod and go.sum), and that any prefer, avoid or ignore expression seen on a host is local configuration (on Arch it can be a distribution packaging change: S126 PKGBUILD:22 appends an --avoid option to the shipped EARLYOOM_ARGS). Upstream's file carries only the report interval (-r 3600) as an active default, its only avoid text is a commented example at :19, and the file is read through the systemd unit or the init script. | mined | 2026-10-22 | on-release | corpus/knowledge/oom-victim-selection-r27.md, corpus/lessons/round-28.md |
```

Cell check: one line, 11 data cells (NF=13), no `|` inside cells, `teaches` opens exactly `supersedes S131 — `
(U+2014 + space), `status` `mined`, `opened` `2026-10-22`, `recheck` `on-release` (S131's convention), `used-by`
as reasoned below.

**used-by reasoning.** CORPUS.md defines used-by as "repo-relative paths of the knowledge entries or lessons citing
the row". The A1 counter requires every used-by path to cite the **new** id as a word at `<rev>` and requires
`readers_left=0` (no live reader citing any superseded id). The two paths chosen will cite S151 at the landed tip:
the knowledge entry after the sweep (section 7) and the round-28 lesson's Gate line (section 5). History files
(`corpus/lessons/round-27.md`, `corpus/lessons/round-27-verifier-spotcheck.md`) cite S131 today but are history per
A1 and are intentionally not listed, else `used_by_not_citing` would fail. (`corpus/SOURCES.md:137` is the registry
row itself, not a used-by path.)

## 5. Gate line (for `corpus/lessons/round-28.md`, `## Gate` table)

Per contract C1 and the A1 counter (needs an https URL, a 64-hex sha256 and a quoted span on the row line):

```
| S151 | https://api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0?recursive=1 ; https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.default (listing sha256 8b3c95cf88d0b8c58bbe973c1b6846c34063a258b7edfaeb57320f5dfbf3c145) | 2026-10-22T17:59:24Z | `:535` `"truncated": false`; `:5` `EARLYOOM_ARGS="-r 3600"` | admit, A, mined (SupersedeS131) |
```

Quotes are verbatim from the fetched bytes, located, each well under 25 words. The round-28 lesson file does not
exist at `6ebd518f`; the L1 creates it (the counter reads `LESSON=corpus/lessons/round-28.md`).

## 6. Checks run (scratch/sandbox only; the lane was not modified)

- Sandbox clone `/fast/scratch/hyaku/mori-r28/SupersedeS131/sandbox` (of the lane at 763d3469), two scratch commits:
  the S151 row inserted after the S144 row, `corpus/lessons/round-28.md` created with the Gate line, and the two
  reader lines moved S131→S151.
- Fleet census: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <scratch-root> mori`
  → **exit 0**, `mori ok …`, only the six pre-existing W04 warnings (S035, S037, S073–S076). No E01/E04/E11/etc.
- Round-28 counter (copied to scratch, `LANE` repointed at the sandbox): `row_identity=rows=145 changed=3 …`,
  `superseding=1/8 ids=S131`, **no `fail S151 …` line**, `readers_left=26` (remaining 26 are the seven other
  superseded ids, other seats' scope). The S151 row clears every per-row check: prefix, teaches-differs, mined,
  used-by non-empty and citing S151 in both paths, Gate line present.
- `check-row-identity.py` repointed at the sandbox: `rows=145 changed=3 removed=0 bad=0` — S151 reports no changed
  cells (its first publication is itself).
- Read-only in the lane: `bash .ufo/waves/round-28/count-c1.sh 6ebd518f` → `row_identity=rows=144 changed=3 …`,
  `superseding=0/8 ids=none`, `C1=unmet`, exit 1 (the declared before-state; evidence `c1-before-a1.txt` records
  `readers_left=27` measured 2026-10-22T17:55:46Z).

## 7. Reader sweep (required by the counter; L1 edits, this seat does not write the lane)

Live reader lines citing `S131` as a word at `6ebd518f` (READERS = SKILL.md, PROVINCE.md, corpus/README.md,
corpus/knowledge):

- `corpus/knowledge/oom-victim-selection-r27.md:1` — source line: `S131 (earlyoom v1.9.0 tag tree and earlyoom.default — the shipped default arguments)` → move to `S151`.
- `corpus/knowledge/oom-victim-selection-r27.md:48` — Defaults bullet: `… S131 \`earlyoom.default:5\`)` → move to `S151`.

Both are the same bullet the entry already corrected for F5 at `df886be1`; only the row-id citation moves. Other
reader lines hit other superseded ids (S127, S129, …) and belong to the corresponding seats. Range notations
`PROVINCE.md:377` and `corpus/README.md:36` (`S127–S132`) do not literally spell `S131`; they are S127/S129
seats' concern, but the L1 should review the ranges once all eight rows land.

## 8. QUALITY 77 sweep — every place whose prose states the defective wording

Defective wording = the tree URL without `?recursive=1` as the source of the 67-entry listing (F1) and the teaches
clauses F2–F4 (`exactly one configuration file`; `any such expression observed on a host is local configuration`;
scope pointer `not the unit or init-script template content (S120)`).

| path:line | what it says | kind |
|---|---|---|
| `corpus/SOURCES.md:137` | the S131 row's source cell (URL without query), scope cell (F4 pointer), teaches cell (F2/F3) | the defect; frozen by QUALITY 81 (first-published cells), superseded by S151 |
| `.ufo/waves/round-27/w1/SrcEarlyoomManpageOptions.md:127` | Gate hash table lists `https://api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0 (recursive)` with the recursive sha256 — the URL as written omits the query | **live false claim in a seat report** (origin of F1) |
| `.ufo/waves/round-27/w1/SrcEarlyoomManpageOptions.md:198` | the drafted row `S???` carrying the same defective source/scope/teaches cells | **live false claim in a seat report** |
| `.ufo/waves/round-27/w2/ReopenS131.md` | quotes the defective wording to name F1–F4 and give fixes (`:13,21,33,43,47,49,57,61,63,72,78,87,127,128,162,164,167,168`) | falsification record — keep |
| `.ufo/waves/round-27/w2/CriticC1Admission.md:18,55,58-59,185-188` | states the URL defect and recommends the lesson Gate-row correction | falsification record — keep |
| `corpus/lessons/round-27.md:127` | carried-debt line naming the defect (history) | keep |
| `corpus/lessons/round-27-verifier-spotcheck.md:150` | routed defect 4 naming the defect (history) | keep |
| `corpus/lessons/round-27.md:73` | S131 Gate row names `(with the v1.9.0 tag tree)` with no tree URL/hash (F9 low) | under-specified, not false; resolved by the round-28 Gate row (section 5) |

Places that already carry the corrected wording (must stay): `corpus/knowledge/oom-victim-selection-r27.md:48`
(the F5-corrected Defaults bullet: "Upstream's v1.9.0 bytes set no prefer, avoid or ignore expression … S126
`PKGBUILD:22` …"). `corpus/lessons/round-27-verifier-spotcheck.md:55` quotes `earlyoom.default:5` correctly.

**Conflict for the L1 (decide, do not leave implicit).** QUALITY 77 says superseded wording is removed, not shadowed;
QUALITY 81 / CORPUS Rule 2 freeze S131's first-published cells. Because S131 was never edited in place, there is no
restore possible, and the corrected teaching necessarily lives in S151. The S131 row keeps its defective first
publication by rule; the round-28 lesson must log the old → new cells (CORPUS Rule 2, "the old → new is logged in
the lesson") and the two live seat-report lines above (SrcEarlyoomManpageOptions.md:127 and :198) are recommended to
get a dated correction block or an explicit disposition in the round-28 lesson, following the r26 D4 precedent
(`corpus/lessons/round-27.md:109`).

## 9. Out of scope, gaps, limits

- This seat owns S131 only. S096, S097, S101, S127, S128, S129, S140 are other C1 rows; their restores/superseding
  rows and their reader sweeps are theirs.
- `readers_left=26` at the sandbox tip is entirely the other seven ids; the L1 must bring it to 0 for C1=met.
- The `?recursive=1` listing is a GitHub API payload; reproduced twice today 84 minutes apart in round 27 and again
  today (same sha256), stable.
- Host state was not read (bounds). All Arch-package statements are [INFERENCE] from the PKGBUILD, not from the host's
  `/etc/default/earlyoom`.
- No lane file was written except this report. No git/jj mutation in the lane; the sandbox clone and its two commits
  exist only under scratch.

## 10. Tooling and privacy

- No installs and no updates. Versions used: bash 5.3.20, curl 8.23.0, git 2.56.0, Python 3.14.8, sha256sum
  0.8.0, GNU Awk 5.4.1. The operator's agent rules file (`/home/vgpnk/.omp/agent/RULES.md`) was read; no tool was
  needed, so nothing was installed; no pacman transaction ran.
- Only read-only git was used in the lane (`show`, `log`, `grep`, `rev-parse`, `ls-tree`, `diff`); `git clone
  --no-hardlinks` wrote only into scratch; the two sandbox commits exist only there.
- This report carries commit ids, URLs, digests, line numbers, row cells and counts only. No uid, pid, session id,
  unit name of this host's user session, settings value, or `--prefer`/`--avoid`/`--ignore` expression value.

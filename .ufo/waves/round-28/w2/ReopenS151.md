# ReopenS151 — wave-2 attack on row S151 (supersedes S131) at f2de0ee

holds — S151 at `f2de0eedcd60d2e354da75265ea6122bc3896073`: Gate line, all 11 cells, the named defect fixed (not copied), and the QUALITY 77 reader sweep all verify against bytes re-fetched 2026-10-22T18:54–18:58Z; one low wording nit.

seat: MoriR28.ReopenS151 (leaf; no subagents, no background jobs). Judge role per amendment A2 not invoked: C2 is out of my scope.
lane: /home/vgpnk/Projects/shokunin/mori-shokunin. Every lane citation below is committed bytes at f2de0ee, extracted with `git show` into seat scratch and hashed there. The lane working tree was dirty at read time (`M corpus/lessons/round-28.md`, `M .ufo/waves/round-28/w1/MutCountC1.md`, siblings' work) and was not used.
scratch: /fast/scratch/hyaku/mori-r28-w2/ReopenS151/ (fetched upstream bytes + committed-byte extracts). Lane writes by this seat: this report file only.

## 0. Sources re-opened by curl now (all HTTP 200, no bot challenge)

| URL | accessed UTC | B/lines | sha256 |
|---|---|---|---|
| api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0?recursive=1 | 18:54:09Z | 19,112 / 536 | `8b3c95cf88d0b8c58bbe973c1b6846c34063a258b7edfaeb57320f5dfbf3c145` |
| raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.default | 18:54:09Z | 563 / 21 | `c0770413a180e0731583f643fc4e84f4a0dac57efb8f575b74ee9a971df984a2` |
| raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/Makefile | 18:54:09Z | 2,898 / 99 | `b852cb9b832729f37f2b19fe93956720a5a58017aa8f76a6036cc928d96127ae` |
| raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.initscript.in | 18:54:09Z | 4,532 / 163 | `704562265c0275577f645de310d4efa010028cbde1e18b04ab29c78630509890` |
| raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.service.in | 18:57:27Z | 1,340 / 51 | `d4019b66d87539a006fc2d178d972dcf1b46e70343627b8bf66d1a08dcdda0bd` |
| api.github.com/repos/rfjakob/earlyoom/commits/202d4db0d308ca6478f68de68b46cae34896ddaf | 18:57:27Z | 4,901 | `ecf9ac003b02555ed97870d193a14d5558f2882b4a92971a336da08abb97492d` |
| gitlab.archlinux.org/…/PKGBUILD at 704e0571 | 18:57:27Z | 1,179 | `f48dc3f99aee5d6a93f8cad4e4b6286dab014745aa6f85b1c3582c3db46dd4a2` |
| api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0 (no query; for the teaches' F1 claim) | 18:57Z | 8,757 / 253 | `92f8c2c92834cf092ce612a7d464a354b44b19ab589f004db7eccdd2d271fad0` |

All seven artifact hashes equal the wave-1 SupersedeS131 record (`.ufo/waves/round-28/w1/SupersedeS131.md:§2`), fetched 17:59:23–47Z — no drift anywhere.

## 1. Check 1 — the Gate line (corpus/lessons/round-28.md:70 at f2de0ee): holds

Line 70 carries the S151 row: URL named first is the `?recursive=1` listing, access time `2026-10-22T17:59:24Z`, sha256 cell `8b3c95cf…c145`, located quotes, decision `admit, A, mined (SupersedeS131)`. Per the lesson's own rule (`round-28.md:61`) the sha256 cell is the digest of the first-named URL — and my 18:54:09Z fetch of that listing hashes to exactly `8b3c95cf88d0b8c58bbe973c1b6846c34063a258b7edfaeb57320f5dfbf3c145`. **No drift.** Located quotes, verbatim at the stated lines: `tree.json:535` `"truncated": false` (2 words) and `earlyoom.default:5` `EARLYOOM_ARGS="-r 3600"` (1 word). Both ≤25 words, both byte-verified in my fetches. https URL and 64-hex sha256 present, as amendment A1 requires of a Gate line (contract.md, A1 counter bullet).

## 2. Check 2 — every cell of S151 (corpus/SOURCES.md:156) against the bytes: holds

- **id / kind / grade**: `S151`, `code`, `A` — same shape as the superseded S131 row (`SOURCES.md:137`) and sibling superseding rows.
- **source cell**: the four URLs fetched 200 with exactly the sizes, line counts and sha256s the row and Gate claim (table §0).
- **scope cell**: "the one default-settings file" — the recursive listing contains exactly one path matching `default|config|conf` case-insensitively: `earlyoom.default` at listing `:375`. "its sourcing contract" — `earlyoom.default:1-2` read verbatim: "sourced by /bin/sh from /etc/init.d/earlyoom or by systemd from earlyoom.service". Scope correction vs S131: "not the unit template content (S120 covers earlyoom.service.in only); the Makefile and init-script lines are cited here only as consumers of the file" — S131's blanket "not the unit or init-script template content (S120)" is gone and the init script is now a listed source.
- **anchor cell**: 67 `"path"` entries, 60 blob + 7 tree, `"truncated": false` at `:535` — all counted in my tree.json. `earlyoom.default` blob `ba4f5c9f4204154d7ee30cab54ea28ebf851c809` — `git hash-object` of my bytes equals it. `:5` is the only un-commented `EARLYOOM_ARGS` line (`-r 3600`); `:10,13,16,19` commented; `:21` `# See more at `earlyoom -h'`. Makefile `:41,47,55,56,57` verbatim (`install-default` → `install -m 644 $< $(DESTDIR)$(SYSCONFDIR)/default/earlyoom`); only five lines of the Makefile contain "default", so it is the only file installed under that directory. Listing `:383` `earlyoom.initscript.in`, `:391` `earlyoom.service.in`. service.in 1,340 B / 51 lines / sha256 `d401…` — equal. initscript `:31` sources the default file, `:52` `exec $DAEMON $EARLYOOM_ARGS`. service.in `:6` `EnvironmentFile=-…`, `:7` `ExecStart=… $EARLYOOM_ARGS`. Commit `202d4db0…`, tree `bc0d30aabe03e441577dccbe35b8d95ea3e28bce`, dates `2025-09-16T19:09:23Z` — all three in my commit.json.
- **teaches cell**: opens exactly `supersedes S131 — ` (em dash + space); wholly different text from S131's teaches; every statement re-proven (check 3).
- **status / opened / recheck**: `mined`, `2026-10-22`, `on-release` — mined with non-empty used-by per A1; recheck follows S131's convention.
- **used-by cell**: four paths; all cite `S151` as a word at f2de0ee (check 4).

## 3. Check 3 — the named defect fixed in S151, not copied: holds

Round-27 routed defect 4 (`corpus/lessons/round-27-verifier-spotcheck.md:150`) and wave-1 F1–F4 (`w1/SupersedeS131.md:§0,§8`):

- **F1 (tree URL without `?recursive=1`)**: S151's source and anchor name the `?recursive=1` listing. Re-proven, not copied: my no-query fetch right now returns 31 entries / 8,757 B / sha256 `92f8c2c9…` — the teaches' "returned 31 top-level entries and not the 67-entry listing" is true of the live bytes today.
- **F2 ("exactly one configuration file")**: not copied — S151's teaches refutes it and names the other shipped config-format files; my listing contains `.clang-format`, `.github/workflows/ci.yml`, `.github/workflows/codeql.yml`, six `.gitignore` paths (root + five nested under `contrib/`), `Dockerfile`, `go.mod`, `go.sum`.
- **F3 ("any prefer/avoid/ignore expression seen on a host is local configuration")**: not copied — S151 corrects it ("on Arch it can be a distribution packaging change: S126 PKGBUILD:22 appends an --avoid option"); my PKGBUILD:22 fetch contains `--avoid` (count only; value withheld per privacy), sha256 equals S126's recorded digest. The positive claim "only the report interval (-r 3600) as an active default" matches `earlyoom.default:5` and the commented `:10,13,16,19`.
- **F4 (scope pointer "not the unit or init-script template content (S120)")**: not copied — see scope cell above; the init script's two consumer lines are anchored with located numbers and its own digest.

## 4. Check 4 — used-by cites S151; no live reader carries the defective wording (QUALITY 77): holds

QUALITY 77 (`corpus/QUALITY.md:349-352`): a correction sweeps every mention; superseded wording is removed, not shadowed; a contradicted line left standing is a defect.

- **used-by, each path cites S151 at f2de0ee**: `corpus/knowledge/oom-victim-selection-r27.md:1` (source list: "S151 (earlyoom v1.9.0 tag tree and earlyoom.default — the shipped default arguments; supersedes the round-27 row, round 28)") and `:48` (Defaults bullet ends "S151 `earlyoom.default:5`"); `PROVINCE.md:377-378` (prose row list names S151); `corpus/README.md:36` ("S148, S149, S150, S130, S151, S132, S142 (S148–S151 supersede the round-27 rows, round 28)"); `corpus/lessons/round-28.md:70` (the Gate line).
- **no live reader cites S131**: `grep -w S131` over SKILL.md, PROVINCE.md, corpus/README.md and all of corpus/knowledge/ at f2de0ee → zero lines.
- **no live reader states the defective wording**: zero matches in the four live surfaces for "exactly one configuration", "local configuration", or `trees/v1.9.0` in any spelling (so no non-recursive URL and no contradicted tree-listing claim survives). `knowledge:48` states the corrected Defaults bullet ("Upstream's v1.9.0 bytes set no prefer, avoid or ignore expression … Arch's packaging appends an `--avoid` option … S126 `PKGBUILD:22` … S151 `earlyoom.default:5`"), and `knowledge:1` lists S151 with the supersession note.

## 5. Findings by severity

- **L-1 (low, wording precision)** — `SOURCES.md:156` anchor ":10,13,16,19 commented examples (:19 the file's only avoid text)" and the teaches clause "its only avoid text is a commented example at :19": upstream `earlyoom.default:18` is `# Avoid killing processes whose name matches this regexp` — the word "Avoid" (prose heading of the `:19` example) means the literal string is not unique to `:19`. The operational claim is true (the only `--avoid` expression is the commented example at `:19`; no active expression). Suggest tightening to ":18-19" or "the only `--avoid` text". Same nit passed through wave-1 verdict #6.
- No medium or high finding. No A2 ruling required (not my lane).

## 6. Residual risk and verification gaps

- GitHub API payload stability underlies three cells; the same digests reproduced across independent fetches 55 min apart today (17:59:24Z wave-1, 18:54:09Z mine; the no-query listing also matches round-27's `92f8c2c9…`), so treated as stable, not proven permanent.
- service.in, commit.json and PKGBUILD were verified once today each (18:57:27Z); consistent with wave-1's hashes, no re-drift check.
- I did not run `count-c1.sh` (counter seats own it); my used-by/readers results are direct greps of committed bytes, which is what the counter's S151-relevant checks assert.
- [INFERENCE] kind `code` / grade `A` and recheck `on-release` are convention-conforming choices, not byte-derivable facts.

## 7. Tooling, privacy, incidents

- No installs, no updates, no pacman (all transactions paused host-wide). Used preinstalled: curl 8.23.0, git 2.56.0, sha256sum 0.8.0, GNU bash 5.3.20. `/home/vgpnk/.omp/agent/RULES.md` read 2026-10-22 before work.
- Read-only git in the lane only (`show`, `status --porcelain`, `ls-tree`); no ref, index or jj mutation; no clone of the lane needed.
- Incident, disclosed: a raced parallel shell briefly redirected two `git show` extracts into an unintended cwd; one stray `/README.md` (byte-equal to committed `corpus/README.md` at f2de0ee, sha256 `7696781834…`) appeared at the filesystem root and is now gone (stat: ENOENT; nothing I removed — it did not persist). Fleet-root and lane `README.md`/`SKILL.md`/`PROVINCE.md` hashes equal their pre-incident on-disk files and `git status` shows no untracked file from me in the lane. No lane, fleet or sibling bytes changed.
- Privacy: no uid, pid, session id, host unit name, settings value, or any `--prefer`/`--avoid`/`--ignore` expression value appears above; upstream example values masked at `earlyoom.default:19` and `PKGBUILD:22`.

# SrcEarlyoomManpageOptions — earlyoom 1.9.0 documented victim-selection contract (C1 source seat)

Question: the victim-selection options earlyoom 1.9.0 documents (`--prefer`, `--avoid`, `--ignore`,
`--sort-by-rss`, `-i`/`--ignore-root-user`, `-p`), the default prefer/avoid lists (if any), the README's
account of how the victim is chosen, and which files in the v1.9.0 tag ship a default configuration.
Read-only. No installs, no edits outside this report. All fetches over public HTTPS with curl.

## Verdict

- `MANPAGE.md` is S115 and `README.md` is S114. Both rows already exist at **byte-identical** hashes to what I
  fetched (S114 `23411dbf…`, S115 `cc48b02e…`; my independent `sha256sum` matches both). Per the contract this is a
  **re-open that adds anchors, not a new row** — ready-to-paste anchor/scope/used-by text in §7(a),(b).
- No row covers the tag tree listing or the shipped `earlyoom.default` file (grep of `corpus/SOURCES.md` for
  `earlyoom.default` and `git/trees` → 0 hits; S120 owns `earlyoom.service.in`, S126 owns the PKGBUILD). So one
  **new row** for those two artifacts is justified — draft in §7(c), id left `S???` (max id at my read was S126).
- Two documented-vs-code discrepancies must be stated in the entry, not smoothed over (§4): `-i` is dead but
  `--ignore-root-user` is alive and undocumented; `-p` is documented as unusable under the systemd unit that the
  same tag ships with `Nice=-20`/`OOMScoreAdjust=-100` already set.

## 1. How 1.9.0 says the victim is chosen (entry ground truth)

Documented model, in order:

1. **Gate**: act only when available memory **and** free swap are both below their minima
   (`MANPAGE.md:19-21`; `README.md:26-28,53-56,239-240`). Not a single-threshold trigger.
2. **Default ranking key**: `oom_score`, highest wins — `MANPAGE.md:19-21` ("largest process (highest
   `oom_score`)"), `README.md:28`, `README.md:53-56` ("the process that uses the most memory in the opinion of
   the kernel (`/proc/*/oom_score`)"), `README.md:81` ("Like the Linux kernel would, earlyoom finds its victim by
   reading through `/proc/*/oom_score`").
3. **Opt-in ranking switch**: `--sort-by-rss` picks the largest RSS instead; the manual states the default
   explicitly as oom_score (`MANPAGE.md:202-203`). Changelog: added in v1.8 (`README.md:306-307`).
4. **Documented modifiers**: `--prefer` +300 to oom_score, `--avoid` −300, `--ignore` excludes outright
   (`MANPAGE.md:177-200`). The manpage's BUGS section adds that a `--prefer` match ignores negative
   `oom_score_adj` and floors the effective score at 300 (`MANPAGE.md:275-277`).

Code corroboration for the parts the docs state only loosely (not this row's scope; `kill.c` is S118,
`main.c` is S119): candidate rejected if `pid <= 2` (`kill.c:357`), `--ignore-root-user` skips `uid == 0`
(`kill.c:362-374`), score read from the process's own `oom_score` (`kill.c:396`), tie broken by larger
`VmRSSkiB` (`kill.c:452,462`), `oom_score_adj == -1000` skipped (`kill.c:467`; documented in the changelog at
`README.md:325`, v1.6.1).

## 2. Option table — what 1.9.0 documents

| Option | Line(s) | Documented effect | Default list? |
|---|---|---|---|
| `--prefer REGEX` | `MANPAGE.md:177-188` | +300 to `oom_score` on `comm` match; `comm` is `/proc/pid/comm`, first 15 bytes, names longer than that truncated | none |
| `--avoid REGEX` | `MANPAGE.md:190-191` | −300 from `oom_score` on `comm` match | none |
| `--ignore REGEX` | `MANPAGE.md:193-200` | excluded from killing entirely; "disables any potential killing" even at high `oom_score`; manual warns other processes are sacrificed instead | none |
| `--sort-by-rss` | `MANPAGE.md:202-203` | largest RSS instead of `oom_score`; default stated as oom_score | off |
| `-p` | `MANPAGE.md:111-118` | own niceness −20 **and** own `oom_score_adj` −100; manual says it "doesn't work" under the default systemd service and prescribes `OOMScoreAdjust=-100` + `Nice=-20` via `systemctl edit` | off |
| `-i` | `MANPAGE.md:89-90` | "removed in earlyoom v1.7, ignored for compatibility" | n/a |
| `--ignore-root-user` | **absent from MANPAGE.md** (0 hits for `ignore-root`/`root-user`) | see §4 D1 — implemented in 1.9.0, listed only by the README's stale help block (`README.md:253`) | off |
| `-g` | `MANPAGE.md:156-175` | kill all processes in the victim's PGID | off |
| `--dryrun` | `MANPAGE.md:205-206` | do not kill (already anchored in S115) | off |

Regex semantics are POSIX extended, compiled with `regcomp(..., REG_EXTENDED | REG_NOSUB)` (`main.c:376,383,390`).
Invalid regex exits 6 with "could not compile regexp" (`main.c:377,384,391`) — relevant only if a host config were
malformed; exit 6 is **not** in the manual's EXIT STATUS table (`MANPAGE.md:222-250`), so it is a doc gap too.

## 3. Defaults, and which files ship a default configuration

- **No default prefer/avoid/ignore list exists.** `MANPAGE.md` mentions "default" only for thresholds, the report
  interval, and the selection key (`MANPAGE.md:31,45,56,57,77,84,99,114,203,273` — none is a process-name list).
  All three regex options are opt-in and empty by default (`main.c:147-149` initialize them to `NULL`).
- **Upstream shipped default args**: `earlyoom.default:5` is the only active `EARLYOOM_ARGS` line in that file —
  `EARLYOOM_ARGS="-r 3600"`. Everything else in the file is a commented example (`earlyoom.default:10,13,16,19`)
  plus the trailer `See more at 'earlyoom -h'` (`earlyoom.default:21`). Header states the file is sourced by
  `/bin/sh` from `/etc/init.d/earlyoom` or read by systemd (`earlyoom.default:1-2`).
- **README example is not a default**: `README.md:214` introduces the block with "for example", and
  `README.md:217` shows `EARLYOOM_ARGS="-m 5 -r 60 --avoid '(^|/)(init|Xorg|ssh)$' --prefer '(^|/)(java|chromium)$'"`
  as a template the operator builds, not something the package ships.
- **Files in the v1.9.0 tree that ship configuration** (67 entries, 60 blobs, `truncated: false`): exactly one path
  name-matches `default|config|conf` — `earlyoom.default` (`tree.json:375`). It is *consumed* by two templates:
  `earlyoom.service.in:6` (`EnvironmentFile=-:SYSCONFDIR:/default/earlyoom`) and `earlyoom.initscript.in:31`
  (sources `:SYSCONFDIR:/default/$NAME`), both passing `$EARLYOOM_ARGS` to the binary
  (`earlyoom.service.in:7`, `earlyoom.initscript.in:52`). `Makefile:55-57` (`install-default`) installs
  `earlyoom.default` to `$(SYSCONFDIR)/default/earlyoom`. Template content is S120's scope, not mine.
- Host boundary: the Arch package delta appends options to the shipped `EARLYOOM_ARGS` (S126 `PKGBUILD:22`), so
  the host's effective args are not the upstream `-r 3600` — [INFERENCE] from S126's anchored sed line, presence
  only. The host file's path and values are out of bounds for this seat and for the entry.

## 4. Discrepancies the entry must not paper over

**D1 — `-i` and `--ignore-root-user` diverged.** The manual records `-i` as removed in v1.7 and ignored
(`MANPAGE.md:89-90`; the binary prints "Option -i is ignored since earlyoom v1.7", `main.c:249`) and its
changelog explains why (`README.md:314-315`). But the **long** option is still live in 1.9.0:
`{"ignore-root-user", no_argument, NULL, LONG_OPT_IGNORE_ROOT}` (`main.c:185`), sets `args.ignore_root_user = true`
(`main.c:281`), is honored in victim selection (`kill.c:362-374`), and appears in the binary's own `-h` text
(`main.c:327`). It appears in **no other tag document I opened**: 0 hits in `MANPAGE.md`, 0 in
`earlyoom.service.in`, 0 in `earlyoom.initscript.in`, 0 in `Makefile`. The only place it is *listed* is the
README's embedded help block (`README.md:253`), which is headed `earlyoom v1.8` (`README.md:230`) and is therefore
stale as a 1.9.0 option list.
Consequence for the entry: an operator reading only the man page cannot learn that `--ignore-root-user` exists;
an operator reading only the README learns it exists but also sees a v1.8 option set. The `comm`-based selection
therefore has an undocumented uid-based exclusion available, and neither doc tells you its exact candidate filter.

**D2 — `-p` vs the unit the tag ships.** `MANPAGE.md:114` says the switch "doesn't work" under the default systemd
service and tells the operator to set `OOMScoreAdjust=-100` and `Nice=-20` by hand, but the tag's own unit already
carries `Nice=-20` (`earlyoom.service.in:12`) and `OOMScoreAdjust=-100` (`earlyoom.service.in:14`), and the v1.8.2
changelog says "Allow `-p`" (`README.md:293`). `-p` in code sets priority then `oom_score_adj` and continues with a
warning if the write fails (`main.c:395-405`). So the manpage caveat is at best stale against the shipped unit and
at worst misleading; the entry should cite the unit line rather than repeat the caveat as fact.

**D3 — the README help block is a v1.8 snapshot.** It omits `-P` (documented at `MANPAGE.md:142-155`, added in
v1.9.0 per `README.md:283-287`) and includes `--ignore-root-user` (`README.md:251-257`). Neither document alone is a
complete 1.9.0 option list; the entry should say so rather than pick one.

## 5. `--sort-by-rss` changes what `--prefer`/`--avoid` do (code, outside S114/S115 scope)

`is_larger()` applies the same regex match to different quantities: under `--sort-by-rss` it adds
`VMRSS_PREFER` / `VMRSS_AVOID` to `VmRSSkiB`, otherwise `OOM_SCORE_PREFER` / `OOM_SCORE_AVOID` to `oom_score`
(`kill.c:411-421`), with the constants ±300 and ±3145728 KiB (`kill.c:25,27,30,32`). The manual's
"(adds 300 to oom_score)" (`MANPAGE.md:178`) and "(subtracts 300 from oom_score)" (`MANPAGE.md:191`) describe the
default path only. Practical reading: with `--sort-by-rss`, a prefer/avoid match is worth ~3 GiB of RSS
(3145728 KiB), not 300 score points — an order-of-magnitude different lever, and the docs never say it.

## 6. Gate

Access time for the first batch: **2026-10-22T15:46:30Z** (`date -u` before the fetch). The remaining URLs were
fetched in the same run within ~3 minutes of that timestamp (last `date -u`: 2026-10-22T15:48:37Z).

| URL | sha256 of fetched bytes | size / lines | pin |
|---|---|---|---|
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md | `cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda` | 10114 B / 288 | blob `456ee62ce5e8bfbb6eceb00d42da916edd0a0da4` |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/README.md | `23411dbfd8b409d433f984a5d6677830e86a383ec76935fc1e1d675e6b4374dd` | 19931 B / 427 | blob `e7f86b1ba255425eb766fb5a205bad79176d9e03` |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.default | `c0770413a180e0731583f643fc4e84f4a0dac57efb8f575b74ee9a971df984a2` | 563 B / 21 | blob `ba4f5c9f4204154d7ee30cab54ea28ebf851c809` |
| https://api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0 (recursive) | `8b3c95cf88d0b8c58bbe973c1b6846c34063a258b7edfaeb57320f5dfbf3c145` | 19112 B / 536 | 67 entries, `truncated: false` at `tree.json:535` |
| https://api.github.com/repos/rfjakob/earlyoom/commits/202d4db0d308ca6478f68de68b46cae34896ddaf | `ecf9ac003b02555ed97870d193a14d5558f2882b4a92971a336da08abb97492d` | 4901 B / 101 | tree `bc0d30aabe03e441577dccbe35b8d95ea3e28bce`, committer date 2025-09-16T19:09:23Z |
| https://api.github.com/repos/rfjakob/earlyoom/git/trees/bc0d30aabe03e441577dccbe35b8d95ea3e28bce (recursive) | `82ea84a9f794b1d7b1616d96b900e433c3931891bf2c430aa0cf4345a91caea2` | 19112 B | entries identical to `trees/v1.9.0` (path, type, blob sha all equal) |

Note on the tree endpoints: `trees/v1.9.0` echoes the ref in its top-level `sha` field
(`tree.json` `sha` = `202d4db0…`, the tag commit) rather than a tree id; fetching the commit's tree sha directly
returns `sha: bc0d30aa…` with an identical 67-entry listing. So the tag I read is exactly commit
`202d4db0d308ca6478f68de68b46cae34896ddaf` (the pin in the contract), commit date 2025-09-16T19:09:23Z (README
line 283 dates v1.9.0 2025-09-16 — consistent).

Verbatim quotes (each ≤25 words, line numbers as fetched):

MANPAGE.md (inside each line, `` ` `` is a literal backtick from the source):

```
L90   removed in earlyoom v1.7, ignored for compatibility
L112  Increase earlyoom's priority: set niceness of earlyoom to -20 and oom_score_adj to -100.
L178  Prefer killing processes whose `comm` name matches REGEX (adds 300 to oom_score).
L191  avoid killing processes whose `comm` name matches REGEX (subtracts 300 from oom_score).
L203  find process with the largest rss (default oom_score)
```

README.md:

```
L28   By default if both are below 10%, it will kill the largest process (highest `oom_score`).
L81   Like the Linux kernel would, earlyoom finds its victim by reading through `/proc/*/oom_score`.
L217  EARLYOOM_ARGS="-m 5 -r 60 --avoid '(^|/)(init|Xorg|ssh)$' --prefer '(^|/)(java|chromium)$'"
L230  earlyoom v1.8
L253  --ignore-root-user        do not kill processes owned by root
```

earlyoom.default:

```
L1    Default settings for earlyoom. This file is sourced by /bin/sh from
L5    EARLYOOM_ARGS="-r 3600"
```

tree.json (the listing itself, not a document):

```
L375        "path": "earlyoom.default",
L535    "truncated": false
```

## 7. SOURCES deliverables

The text below is anchor, scope and used-by material only; it changes no fact and no status. Both target rows
keep `status mined`, `opened 2026-10-22`, `recheck on-release`.

**(a) S115 (`MANPAGE.md`) — append to the `anchor` cell; widen `scope`; extend `used-by`:**

```
scope (insert before the "not the runtime log-line grammar" clause): and its documented victim-selection contract: the --prefer/--avoid score deltas, the --ignore exclusion, the --sort-by-rss alternative and its stated default, -p's niceness/oom_score_adj pair, the removed -i, and the BUGS note on --prefer with negative oom_score_adj
anchor (append after "zero-swap `-S` caveat:270-273"): victim selection default highest oom_score:19-21; `-i` removed and ignored:89-90; `-p` niceness -20 and oom_score_adj -100 with the systemd caveat:111-118; `--prefer` plus 300 and 15-byte `comm`:177-188; `--avoid` minus 300:190-191; `--ignore` exclusion and sacrifice warning:193-200; `--sort-by-rss` and its oom_score default:202-203; BUGS prefer floors effective score at 300:275-277; 0 hits for `ignore-root-user` in this file
used-by (append): corpus/knowledge/oom-victim-selection-r27.md
```

**(b) S114 (`README.md`) — same three edits:**

```
scope (insert before the "not the post-1.9.0 upstream master README" clause): and its victim-selection and configuration account: the /proc-based victim search, the --prefer/--avoid section, the /etc/default/earlyoom example args, and the embedded help block that is a v1.8 snapshot
anchor (append after "changelog v1.9.0:283-287"): victim search via /proc oom_score:81; --prefer/--avoid section:205-209; config file and example EARLYOOM_ARGS:211-218; embedded help block:227-257 (version line:230, --ignore-root-user:253, --sort-by-rss:254, --prefer:255-257); changelog --sort-by-rss added v1.8:306-307, -i removed v1.7:314-315, skip oom_score_adj=-1000:325, -p sets adj -100 since v1.5:339, -p allowed:293
used-by (append): corpus/knowledge/oom-victim-selection-r27.md
```

**(c) NEW row — no existing row covers the tag tree or `earlyoom.default`.** id left `S???`: highest id in
`corpus/SOURCES.md` at my read was S126, so `S127` if no sibling claims it first.

```
| S??? | earlyoom v1.9.0 tag tree and its shipped default-configuration file — https://api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0 ; https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.default | code | A | which files the v1.9.0 tag ships as configuration and what the shipped default args are: the one default-settings file, its active and commented EARLYOOM_ARGS lines, its sourcing contract, and the Makefile rule that installs it; v1.9.0 tag only; not this host's /etc/default/earlyoom file or its values, not the Arch package delta (S126), not the README example args (S114), not the unit or init-script template content (S120) | tree.json:535 truncated false over 67 entries and 60 blobs, and the only path whose name contains default, config or conf is earlyoom.default at tree.json:375; earlyoom.default:1-2 sourced by /bin/sh or read by systemd, :5 active EARLYOOM_ARGS=-r 3600, :10,13,16,19 commented examples, :21 see-more trailer; Makefile:41,47,55-57 install-default copies it to $(SYSCONFDIR)/default/earlyoom; the two template paths in the same listing are earlyoom.initscript.in at tree.json:383 and earlyoom.service.in at tree.json:391, with $EARLYOOM_ARGS passed at earlyoom.service.in:6-7 and earlyoom.initscript.in:31,52; tag v1.9.0 = commit 202d4db0d308ca6478f68de68b46cae34896ddaf, tree bc0d30aabe03e441577dccbe35b8d95ea3e28bce, commit date 2025-09-16T19:09:23Z; earlyoom.default blob ba4f5c9f4204154d7ee30cab54ea28ebf851c809, HTTP 200, 563 B, 21 lines, sha256 c0770413a180e0731583f643fc4e84f4a0dac57efb8f575b74ee9a971df984a2; tree listing HTTP 200, 19,112 B, sha256 8b3c95cf88d0b8c58bbe973c1b6846c34063a258b7edfaeb57320f5dfbf3c145; opened 2026-10-22 | The v1.9.0 tag ships exactly one configuration file and its default EARLYOOM_ARGS carries only a report interval (-r 3600): no prefer, avoid or ignore expression is a shipped default, so any such expression observed on a host is local configuration, and the file is consumed only through the systemd unit or the init script. | mined | 2026-10-22 | on-release | corpus/knowledge/oom-victim-selection-r27.md |
```

## 8. Confidence and boundaries

- **High** (read directly, byte-pinned): every line citation above; the three sha256 values match the bytes I
  fetched, and two of them independently reproduce S114/S115's recorded hashes.
- **High**: `-i` dead / `--ignore-root-user` live / manpage silent (three independent artifacts: MANPAGE has 0
  hits, main.c declares and sets it, kill.c branches on it).
- **Medium**: `--sort-by-rss` repurposing prefer/avoid to RSS deltas — read from `kill.c:411-421` and the four
  constants; I did not execute the binary to observe the outcome.
- **Inference** (marked): host effective `EARLYOOM_ARGS` differs from upstream's `-r 3600` because the Arch
  package appends options (S126 `PKGBUILD:22`); the host file's presence/values are not this seat's evidence.

## 9. Notes for the L1 (coordination, not findings)

1. **C1 counter impact**: anchoring S114/S115 and adding one new row yields **one** `S127+` row, and only if the id
   allocated is ≥ S127. C1 needs three such rows cited by the entry with `used-by` set. This seat cannot close
   that alone; the main.c/kill.c, systemd and kernel seats must land theirs.
2. **Row-scope gap**: `is_larger()` (victim-selection logic) sits in `kill.c`, but S118's declared scope is
   "kill-path log literals and the warn() output route", and S119's is "startup and poll-loop emission". If the
   entry cites `kill.c:355-467` for selection semantics, one of those rows needs its scope widened or a dedicated
   selection row opened — I did **not** edit either row, since they belong to `MoriR27.SrcEarlyoomMainCSelf` and
   the C2/tool seat's source.
3. **Privacy**: this report quotes only upstream bytes. The host's `--prefer`/`--avoid`/`--ignore` expressions,
   `/etc/default/earlyoom` values and any command line are absent by design; process-name examples in the upstream
   quotes (`init`, `Xorg`, `ssh`, `java`, `chromium`, `gnome-control-center`) are upstream's own bytes.
4. **Tooling**: no installs, no upgrades, no pacman. `curl`, `python3`, `sha256sum`, `grep`, `sed` only.

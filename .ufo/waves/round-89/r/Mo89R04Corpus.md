# Mo89R04Corpus: independent check of the r89 sources and the corpus entry (round 89, residual)

Seat: Mo89R04Corpus. I did not write any of this work; this is a detection-and-report pass.
Revisions measured:
- Gate: `.ufo/waves/round-87/count-c2.py` at `9f4d20b9290faff54354d6ab6b08982d98d5e72c`, pulled with `git show` (sha256 `74fac0a6ec25b994ff943e79feb9cf358063732593eecc6811d60fd2bb3c467d`).
- Corpus: landed at `c89e5b6e0c561896f574636f50328668d6706e86`. The master tip during the review was `bb50c332fad4667c8e76d4379ad8ae76ca1bb09b`, and `git diff --stat c89e5b6e bb50c332 -- corpus SKILL.md` is empty, so both revisions have the same corpus bytes.

Host tools used: Python 3.14.8, GNU bash 5.3.20, and `/bin/sh`, which is a symlink to bash (POSIX mode).

Installs: one. I downloaded BusyBox 1.35.0 x86_64-musl from `https://busybox.net/downloads/binaries/1.35.0-x86_64-linux-musl/busybox` (sha256 `6e123e7f…311348`) into **scratch only**, so that a second shell implementation (`ash`) could be compared with bash. busybox.net publishes no checksum file next to the binary (404). It was never put on PATH and was deleted along with the scratch directory. dash is not installed, and pacman is paused.

Scratch directory: `/fast/scratch/hyaku/mori-r89/Mo89R04Corpus/` with `TMPDIR` set to it. It is removed before yield. Durable receipts are in `.ufo/waves/round-89/r/Mo89R04Corpus-evidence/`:
- `probe.py` and `probe.out`
- `locate.py` and `locate.out`
- `binding-probe.out`
- `posix-sh-utility.html`

## 1. Sources: re-opened by me

Fetch method: `curl -sS -L -A 'Mozilla/5.0 (X11; Linux x86_64) Mo89R04Corpus'`, two fetches per URL compared with `cmp`.

Quote location method (`locate.py`): strip tags, drop script/style, decode entities, collapse whitespace, then count occurrences of the quote in the remaining text.

| Row | HTTP (both fetches) | Two fetches | My sha256 | vs pinned copy | Quote occurrences |
|---|---|---|---|---|---|
| S607 shlex | 200, 200 | identical (cmp 0) | `2db8a6e6…806619` | ≠ pin `c6579095…`. The **only** diff is line 799 `Last updated on Nov 04, 2026 (16:58 UTC)` → `(21:57 UTC)` | "All characters from the comment beginner to end of line are ignored": **1** (shlex.commenters) |
| S609 os.path | 200, 200 | identical | `17e6d4fd…1fec` | ≠ pin `71187c77…`. Only line 1000, same timestamp | "This string manipulation may change the meaning of a path that contains symbolic links.": **1** (normpath) |
| S610 cmdline | 200, 200 | identical | `377a2808…8134` | ≠ pin `62a88834…`. Only line 1805, same timestamp | "When called with -c command, it executes the Python statement(s) given as command.": **1**. "all consecutive arguments will end up in sys.argv": **1** |
| S611 POSIX 2.3 | 200, 200, `num_redirects=0` | identical | `0889867a…1acd` | **= pin** `evidence/sources-r89/posix-shell-v3-chap02.html`, byte-identical | "If the previous character was part of a word, the current character shall be appended to that word.": **1**. "If the current character is a '#', it and all subsequent characters up to, but excluding, the next <newline> shall be discarded as a comment.": **1**. These are consecutive rules, word-append first. |

The raw-line locators in the pinned copies match the rows: shlex 429-431, os.path 627-630, cmdline 254-256 and 263. I checked them with `sed -n`.

Locator defects. Both are minor, and neither changes any admit/reject decision.
- **D-src-1: page digests are not stable.** The three docs.python.org pages are rebuilt about daily: the "Last updated" footer moved 16:58 → 21:57 UTC on the same date. The rows' sha256 values are therefore true of the w1 fetch only. A recheck has to match on the quote and section, not the page sha. The w1 receipt also says "no 'Release' banner found", but each pin does contain a date line: `grep -c 'Last updated'` returns 1 per file.
- **D-src-2: the S-id labels in the w1 locator receipt do not match the registry.** The registry rows cite `w1/Mo89S01Sources/sources/fetch-and-locator-receipt.txt` as their locator, but that receipt labels the normpath quote "S608b" and the cmdline quotes "S609/S609b/S609c". The shlex introduction quote is labelled "S610" in the receipt and is **S608** in the registry. Anyone following the citation lands on differently numbered quotes. The w1 draft `knowledge-cmd-binding-r89.draft.md` uses yet another numbering (S609 = normpath, S610 = cmdline).

Source for the `-c` operand behaviour, which no admitted row covers (see §3 F3):
- I opened `https://pubs.opengroup.org/onlinepubs/9799919799/utilities/sh.html` twice: HTTP 200 both times, byte-identical, sha256 `b6f11dc31fccb2145dd51ccd92704779dfce1faa00b3a5bec27f0007b711a054`. It is pinned as evidence `posix-sh-utility.html`.
- Located quotes, one occurrence each: "Read commands from the command_string operand." and "Set the value of special parameter 0 (see 2.5.2 Special Parameters) from the value of the command_name operand and the positional parameters ($1, $2, and so on) in sequence from the remaining argument operands."
- The GNU bash manual `https://www.gnu.org/software/bash/manual/bash.html` was **unreachable**: four attempts all ended in curl rc 28 (connect timeouts of 132758 ms, 133850 ms, 60000 ms and 60001 ms). It is **unrun**, not passed.

## 2. Comment rule and `-c`: empirical check (`probe.out`, rc 0)

Each case was run as `<shell> -c "printf '<%s>' <case>; echo"` under bash, `sh` (bash in POSIX mode) and busybox ash. The three shells agreed on every case.

| Case | `shlex.split(…, comments=True)` | gate `strip_comment` keeps | shells' words | gate vs S611/shells |
|---|---|---|---|---|
| `a#b c` | `['a']` | whole | `<a#b><c>` | **match** (shlex diverges) |
| `'a'#b c` | `['a']` | whole | `<a#b><c>` | match (shlex diverges) |
| `x=1#b c` | `['x=1']` | whole | `<x=1#b><c>` | match (shlex diverges) |
| `a ${#x} c` | `['a','${']` | whole | `<a><0><c>` | match (shlex diverges) |
| `a #b c`, `a;#b c`, `a\t#b c` | comment | comment | comment | match |
| `a\#b c`, `"a #b" c` | kept | kept | kept | match |
| `a >#b c` | — | `a >` | syntax error in all three | consistent (refuses) |
| **`a\ #b c`** | `['a ']` | **`a\ `** (cut) | `<a #b><c>` | **diverges**: an escaped blank is part of the word, but the gate treats it as a word start |
| **`$(echo a)#b c`** | — | **`$(echo a)`** (cut) | `<a#b><c>` | **diverges**: `)` closing a substitution is treated as an operator. Substitutions are declared outside the modelled grammar |

`-c` operand, all three shells: `-c 'echo "zero=$0 one=$1"' tools/x.py arg1` prints `zero=tools/x.py one=arg1`. That agrees with the POSIX sh quote above.

CPython `-I -c … tools/x.py y`: `sys.argv == ['-c', 'tools/x.py', 'y']`, which agrees with S610.

Gate `executed_scripts` results:
- `bash -c 'printf BODY' tools/x.py` → `[]`, correct ($0 is not executed).
- `sh -c 'python3 tools/x.py'` → `['tools/x.py']`, correct.

Conclusion for (2):
- On every case in the modelled grammar except one, the repaired comment rule follows S611's rule order, and it differs from shlex exactly where the entry says it does. I reproduced the entry's `'a#b c'` → `['a']` observation on 3.14.8.
- The exception is **an escaped blank followed by `#`**. `strip_comment` sets `prev` to the escaped character, so `\ ` looks like whitespace.
  - Observed: `echo a\ #b; python3 -I tools/mori-record-sweep.py --root .` gives gate problems `['cmd-binding']`, while all three shells run the second command (printed `RAN`).
  - This is fail-closed, so the gate never binds anything it should not here. It is not harm relative to the entering gate either, because `shlex.split(comments=True)` also cuts at that `#`. But it does contradict entry rule 1's claim that "comments are removed by the POSIX rule".

## 3. Knowledge entry, rows, lesson and QUALITY at `c89e5b6e`

### Per-row agreement

| Row | L1 decision | My decision | Note |
|---|---|---|---|
| S607 | admit, tokenizer scope | **agree** | Quote located once. The scope column correctly limits it to tokenization. The shlex-vs-POSIX divergence note is empirically true (§2). |
| S608 | reject | **agree with reject; disagree with its stated flip** | See F2. |
| S609 | admit | **agree** | Quote located once. The scope keeps file identity on S226. |
| S610 | admit | **agree** | Both quotes located once. Scoped to CPython, which is correct. |
| S611 | admit | **agree** | Both quotes located once, rule order verified. The row's own scope is "not utility option semantics", and that matters for F2 and F3. |

### Findings, by severity

**F1 (high): the entry overclaims "executes"; open counterfeits outside the battery.**
- The rule says: "A bound path binds iff it names … a file the command **executes**". The Limitations section says a binding through functions "is refused or … not inspected".
- What I measured at `9f4d20b9`: `binding_problems(cmd, [(…,'tools/mori-record-sweep.py')], True, repo)` returns `[]` (the binding holds) for:
  - `false && python3 -I tools/mori-record-sweep.py --root .; printf BODY` — the script never runs.
  - `true || python3 -I tools/mori-record-sweep.py; printf BODY` — never runs.
  - `f() ( python3 -I tools/mori-record-sweep.py ); printf BODY` — a function with a subshell body that is defined and never called. The brace-body form `f() { …; }` is refused, so the entry's "functions … refused" holds only for brace bodies.
  - `uv run --directory sub tools/mori-record-sweep.py` — `--directory` is consumed as a plain option value, so the gate binds the repo-root path while uv runs `sub/tools/…`. Compare `cd`, which the entry handles, and `env -C`, which is refused.
- What the gate's rule actually computes is "names a file in a position the command *may* execute". The entry's own last limitation ("the replay comparison is what defends the body") does not cover these: each command above replays to `BODY` deterministically without running the bound script.
- None of these strings is in the Mo89R01C1 battery. `E16 true && …` is in it, but only as a *valid* equivalent. So `noharm-c1.py open=0` is silent about them. The entry already names this overfit risk ("A fixed battery is overfittable"); these cases are concrete instances of it.
- Receipt: `binding-probe.out`.

**F2 (medium): S608's flip text contradicts S611's scope and the entry's own Scope section.**
- The S608 row reads: "Flip: none needed for the execution claim, which S611 (POSIX shell grammar) and the receipt replay now carry".
  - S611's own row scope is token recognition, "not utility option semantics". It does not carry an execution claim.
  - The entry's Scope says the binding is "a syntax rule … execution evidence is the receipt's own replay … never the binding alone".
  - F1 shows the replay does not establish that the bound script executed either.
- "Flip: none needed" is also not a flip condition. A flip should name what would admit the row, for example "a source documenting that the tokenized command was the one the shell ran".
- The rejection itself is honest and correct. Only the flip sentence overclaims.

**F3 (medium): the shell `-c` and option rules have no admitted source.**
- Rule 4 states how `bash`/`sh`/`dash`/`zsh` treat `-c`, `-n` and `-s`, and that the operand after the `-c` string is not executed. No S-row grounds any of this: S610 is CPython-only, and S611 excludes utility option semantics.
- The behaviour is correct. I observed it in bash, POSIX-mode sh and busybox ash, and found a citable ground on the POSIX `sh` utility page (located quotes in §1, page pinned as evidence).
- The entry neither cites a source for these rules nor names them as unsourced lane rules. The w1 draft did name the gap ("INTERPRETERS set outruns the cited pages"); the landed entry dropped that limitation.

**F4 (low): the comment rule's stated equivalence to POSIX has a counterexample in the modelled grammar.**
- The escaped-blank case `a\ #b` from §2 is a counterexample (fail-closed refusal).
- Fix: in `strip_comment`, set `prev` to a non-blank sentinel after an escaped character. I report this only; I made no edit.
- `$(…)#` is the same kind of divergence, but it is in the declared-unmodelled area (substitutions).

**F5 (low): stale digests and mismatched receipt labels.** See D-src-1 and D-src-2 in §1.

### Checked and found sound

- The `noharm` figures (`harm=13 open=6 gained=2 cases=34` at `760428ab`; `harm=0 open=0 gained=3 cases=34` at `9f4d20b9`) are present in `evidence/noharm-760428ab.txt:36` and `evidence/after-r89.txt:62`.
- The case count is consistent: 35 cases in total (30 in `cases.json`, 5 in `cases2.json`) minus 1 void = 34.
- The `VOID` of E15 is the reviewer's own (`w1/Mo89R01C1.md:82-83`: the script has no `--note`), so it is not an L1 post-hoc deletion.
- Both predicates read met in `evidence/after-r89.txt:14,27`.
- The `node` removal claim is true: `invocation_scripts` has no `node` branch.

On QUALITY 186-188: the ground pointers resolve to files in the tree. 186's "Not covered" names the overfit and "functions". F1 shows the function case is a counterfeit *binding*, not only an unmodelled input.

### Census

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`, run at master `bb50c332`, gives **rc=0**. It ends with `mori ok …/corpus/SOURCES.md`. There are W04 warnings, including `S608 duplicate url docs.python.org/3.14/library/shlex.html across scopes`, which is expected for a rejected scope row.

### Judgment on `corpus/knowledge/execution-binding-r89.md`

**better**, with corrections owed. Compared with the w1 draft and the first landing, the entry now:
- grounds the comment rule in the actual shell standard (S611) instead of the tokenizer;
- records, and reproducibly shows, that shlex differs from POSIX;
- keeps S607 confined to tokenization;
- reports harm and open counts from a battery written before the repair.

It is not `unprovable-but-better`. Every sourced sentence traces to a quote I located myself, and the measured rows trace to lane receipts.

It falls short of a clean `better` because of:
- F1: the word "executes", and the function-refusal sentence, are false as written;
- F2: S608's flip credits S611 with carrying an execution claim;
- F3: shell `-c` semantics are asserted without a row, although a ground exists (POSIX `sh` page).

Recommended corrections:
- narrow "executes" to "names in executable position";
- add a limitation for `&&`/`||` short-circuit, subshell-bodied functions, and `uv run --directory`;
- rewrite S608's flip;
- admit the POSIX `sh` row, or name the gap.

## Commands run

All rc 0 unless stated:
- curl fetches: `bg_29675`, then a retry; bash manual rc 28 ×4.
- `cmp` of fetch pairs.
- `diff` of pins against fresh fetches.
- `python3 -I locate.py …`
- `python3 -I probe.py count-c2-9f4d.py`
- `python3 -I -c … binding_problems …`
- `sed -n` locator checks.
- `git -C …/mori-shokunin log --oneline -6 master`, `show` and `diff --stat` (all read-only).
- `sources-census.sh validate`

Gate under test: `git show 9f4d20b9:.ufo/waves/round-87/count-c2.py`.

VERDICT Mo89R04Corpus C1 partial

# Execution binding of a receipt command — what a `# cmd:` string executes (round 89)

source: S611 (POSIX.1-2024 Shell Command Language §2.3 Token Recognition — the comment rule
  and its word-continuation precedence), S607 (Python 3.14 `shlex` — the tokenizer the gate
  uses, scoped to tokenization only), S609 (Python 3.14 `os.path.normpath` — lexical path
  normalization and its symbolic-link limit), S610 (Python 3.14 command line — which argument
  CPython executes as a script and which become `sys.argv` data); S226 (realpath, the
  filesystem half of path identity, already in the registry). S608 is a **rejected** scope row
  (`shlex` as proof of shell execution) and is cited only as this entry's boundary.
verified-at: 2026-11-04 (round 89; S607/S609/S610 opened by seat Mo89S01Sources, pinned copies
  `.ufo/waves/round-89/w1/Mo89S01Sources/sources/`; S611 opened by the L1, pinned copy
  `.ufo/waves/round-89/evidence/sources-r89/posix-shell-v3-chap02.html`, sha256
  `0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd`, two fetches
  byte-identical, HTTP 200)
recheck: on-release

## Scope

Detection and report only. This entry records what the round-89 receipt gate
(`.ufo/waves/round-87/count-c2.py`, `binding_problems` and its helpers, at
`9f4d20b9290faff54354d6ab6b08982d98d5e72c`) decides about a recorded `# cmd:` string, what
each cited page licenses, and what remains outside the rule. The binding rule is a **syntax
rule over the recorded command**; execution evidence is the receipt's own replay
(`replay_body`), never the binding alone.

## The rule (lane bytes)

A bound path binds iff it names, by path identity, a file the command **executes**:

1. **Comments** are removed by the POSIX rule — a `#` starts a comment only at a word start;
   a `#` inside a word is part of the word (S611: "If the previous character was part of a
   word, the current character shall be appended to that word." precedes the `#` rule).
   Python's `shlex` with `commenters='#'` does **not** follow this: observed on Python
   3.14.8, `shlex.shlex('a#b c', posix=True, punctuation_chars=...)` yields `['a']`, dropping
   `#b c`; the gate therefore strips comments itself (`strip_comment`) and tokenizes with
   `commenters=''`. S607 is the tokenizer ground for quoting only.
2. **Invocations** are split quote-aware on `;`, `&&`, `||`, `|`, `&`, `(`, `)`; redirection
   operators and their targets are dropped. A quoted `;` no longer splits (the r89-first
   landing split on raw `;` and refused `echo "a;b" >/dev/null; python3 …`).
3. **Wrappers** are unwrapped: leading `NAME=value` assignments, `env` (refused when it changes
   directory or splits a string: `-C`, `-S`), `nice`, `exec`, `nohup`, `time`, `command`,
   `timeout`. After a `cd`/`pushd`/`popd` invocation nothing later binds (the working
   directory is no longer the repo root).
4. **Executed position**: CPython (`python`, `python3`, `python3.14`, …) — the first operand
   after options, with `-W`/`-X` values consumed and `--` honoured; `-c` and `-m` execute no
   file, so any path after them is `sys.argv` data (S610: "When called with -c command, it
   executes the Python statement(s) given as command."; "all consecutive arguments will end up
   in sys.argv"). `bash`/`sh`/`dash`/`zsh` — the first operand, or the `-c` string parsed
   recursively (depth ≤ 3); `-n`, `-s` and unknown flags bind nothing. `uv run [options]` —
   the following script or interpreter invocation. A token containing `/` in command position
   is a directly executed file.
5. **Path identity**: `normpath` equality or, with a repo root, `realpath` equality (S609:
   normalization "may change the meaning of a path that contains symbolic links" — hence the
   realpath branch, S226).

## Measured behaviour (receipts, not sources)

| Population | Command | Result |
|---|---|---|
| Frozen P-C1 fixtures + real seven receipts | `python3 -I .ufo/waves/round-89/count-c1.py 9f4d20b9…` | `C1=met equiv=accepted comment=refused selfprint=refused real=met arms=26` (`.ufo/waves/round-89/evidence/after-r89.txt`) |
| Mo89R01C1 adversarial battery (34 cases: 22 equivalents, 12 counterfeits; written against the first landing, before the repair) | `python3 -I .ufo/waves/round-89/noharm-c1.py <rev>` | first landing `760428ab`: `harm=13 open=6 gained=2` rc 1 (`evidence/noharm-760428ab.txt`); repair `9f4d20b9`: `harm=0 open=0 gained=3` rc 0 |

`harm` counts valid equivalents the entering gate (`30a29797`) bound and the graded gate
refuses; `open` counts counterfeits the graded gate binds. The three gains are `./tools/…`,
`tools/../tools/…` and direct execution `./tools/…` (refused at entering).

## Limitations (named)

- **A fixed battery is overfittable.** `noharm-c1.py` grades 34 named strings; a gate that
  special-cases them would pass. It is a regression floor against the reviewer's attack set,
  not a census of shell syntax. The round-89 residual reviewer and critic attack it with new
  cases (`.ufo/waves/round-89/r/`).
- **A tokenizer is not a shell** (S608, rejected scope). The gate models a subset of POSIX
  grammar: no parameter expansion, command substitution (`$(…)`, backticks), here-documents,
  aliases, functions, brace groups `{ …; }` or `Makefile` targets. A binding through those is
  refused or, for substitutions inside an interpreter's arguments, not inspected.
- **Interpreter options are an allow-list.** Unknown CPython or shell flags bind nothing
  (conservative refusal); `node` is no longer in executed position (no cited page for its
  options; no receipt in the population uses it).
- **Lexical identity without a repo root.** With `repo=None` (the selftest arms) the rule is
  `normpath` only.
- **No execution provenance.** A bound script that itself re-executes another program, or a
  script that prints a forged body, still binds; the replay comparison is what defends the body.

`absorption: none`.

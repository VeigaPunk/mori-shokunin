# Execution binding of a receipt command — which `# cmd:` positions cannot execute a path (round 89)
recheck: on-release

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

## Scope

Detection and report only. This entry records what the round-89 receipt gate
(`.ufo/waves/round-87/count-c2.py`, `binding_problems` → `binds`, final bytes at
`7715bb56dce6b75ce281ef1a78be4eeb34a9e245`) decides about a recorded `# cmd:` string, what each
cited page licenses, and what remains outside the rule. The rule is a **syntax rule over the
recorded command**; it does not prove the bound script executed (Mo89R04Corpus F1), and the
receipt replay does not prove it either — control-flow counterfeits replay the forged body.

## History (three gate versions this round)

| Version | Rule | Mo89R01C1 battery (34) | attack batteries (78 counted: Mo89R03Repair 59 executed cases, Mo89C02Critic 22) |
|---|---|---|---|
| entering `30a29797` | whitespace token, quotes stripped | `harm=0 open=11` | `harm=0 newopen=0 open=36` |
| first landing `760428ab` | `;` split, script position index 1–2 after an interpreter | `harm=13 open=6` rc 1 | `harm=24 newopen=1 open=9` rc 1 |
| repair 1 `9f4d20b9` | positive model of what executes (wrappers, interpreters, `sh -c`, `cd` stop) | `harm=0 open=0` rc 0 | `harm=12 newopen=1 open=25` rc 1 |
| repair 2 `7715bb56` | entering rule **minus** provably non-executing positions | `harm=0 open=0 gained=3` rc 0 | `harm=0 newopen=0 open=30 gained=2` rc 0 |

Counters: `python3 -I .ufo/waves/round-89/noharm-c1.py <rev>` and `… heldout-c1.py <rev>`
(receipts `.ufo/waves/round-89/evidence/noharm-760428ab.txt`, `evidence/heldout-revs.txt`,
`evidence/after-r89-final.txt`). `harm` = a valid equivalent the entering gate bound and the
graded gate refuses; `newopen` = a counterfeit the graded gate binds and the entering gate
refused; `open` = every counterfeit the graded gate binds. Repair 1 fitted the 34-case battery
and failed on the next 78; the 78-case batteries were written before repair 2 but **its author
read them** — they are attack batteries, not held out from repair 2.

## The rule (repair 2, lane bytes)

A bound path binds iff a word path-identical to it occurs **outside** every position that
provably does not execute it. The design intent is that every refusal beyond the entering token
rule is one of these named exclusions (also applied inside quoted strings, which are parsed as
commands — so `foo "echo tools/x.py"` is refused where the entering rule bound it):

1. **Shell comments** — removed by the POSIX rule: a `#` starts a comment only at a word
   start, a `#` inside a word (including after an escaped blank) is part of the word (S611:
   "If the previous character was part of a word, the current character shall be appended to
   that word." precedes the `#` rule). Python's `shlex` does not follow this — observed on
   3.14.8, `shlex.shlex('a#b c', posix=True, punctuation_chars=...)` yields `['a']`
   (reproduced by Mo89R04Corpus under bash, POSIX sh and busybox ash) — so the gate strips
   comments itself and tokenizes with `commenters=''`; S607 grounds quoting only.
2. **CPython non-script words** — `-W`/`-X` values, the `-c`/`-m` value and every later word,
   every word after `-` or after the script operand (S610: "When called with -c command, it
   executes the Python statement(s) given as command."; "all consecutive arguments will end up
   in sys.argv"). An option the gate does not know cancels these exclusions.
3. **Data operands** — operands of `echo`, `printf`, `:`, `true`, `false`, behind assignments and
   exec/env/nice/timeout-style wrappers. *Lane rule, no admitted source row.*
4. **Redirection targets** — the word after `>`, `<`, `>>`, … *Lane rule, no admitted source row.*
5. **Absolute tokens** never bind: realpath against the production checkout opened a new
   counterfeit in repair 1 (`N-A25-prod-absolute`, Mo89R03Repair). Relative tokens bind by
   `normpath` or relative `realpath` (S609: normalization "may change the meaning of a path
   that contains symbolic links"; realpath is S226), so `./tools/x.py` is `tools/x.py`.

A word containing whitespace (a quoted command string: `sh -c '…'`, `eval '…'`, `env -S '…'`)
is searched recursively with the same exclusions (depth ≤ 3); a command that does not tokenize
falls back to the entering rule. Unquoted newlines separate commands; backslash-newline joins.

## Limitations (named)

- **Not execution proof.** Control flow (`false && …`, `true || …`, `exit` before the
  invocation), uncalled functions, fake interpreters on `PATH`, `sitecustomize`, overwriting
  the bound file, `cd`/`uv run --directory` to a fake tree: each binds as it did on entry
  (`open=30` of the attack batteries' counterfeits; entering `open=36`).
- **Fixed batteries are overfittable** (Mo89C02Critic forge-b: a lookup table passes
  `noharm-c1`). Repair 2's harm-freedom argument is structural (exclusions only), measured on
  112 counted cases, not a census of shell syntax.
- **Rules 3–4 are unsourced lane rules**; the `sh -c` operand semantics the recursion relies on
  were located by Mo89R04Corpus on the POSIX `sh` utility page (pinned as
  `.ufo/waves/round-89/r/Mo89R04Corpus-evidence/posix-sh-utility.html`), not admitted as a row.
- **The gate's selftest still holds 26 arms** (the frozen P-C1 pin); the exclusions are armed
  only by the two batteries, not by selftest arms.
- **Page digests drift**: docs.python.org pages are rebuilt daily (Mo89R04Corpus D-src-1);
  recheck by quote and section, not page sha256.

`absorption: none`.

## Round-89 repair 2 (integration) — the landed rule is subtract-only, not an execution model

Supersedes the execution framing in “The rule (lane bytes)” above (rules 2–4) and the
“brace groups” limit: the rule finally landed at `7715bb56dce6b75ce281ef1a78be4eeb34a9e245` is
**the entering token rule minus the positions that provably do not execute the bound path** —
a POSIX comment (word-start rule, escaped blanks included), a redirection target, an
`echo`/`printf`/`:`/`true`/`false` operand, a CPython `-W`/`-X` value, anything after `-c`/`-m`,
and anything after the script operand. Everything else binds as it did on entry. Path identity
is `normpath` or repo-relative `realpath`; an absolute token never binds; quoted command strings
(`sh -c '…'`, `env -S`, `eval`) are searched recursively.

Measured on two batteries the repair did not author (`heldout-c1.py`, 78 cases from the residual
reviewer `Mo89R03Repair` and critic `Mo89C02Critic`; `noharm-c1.py`, 34 cases from `Mo89R01C1`):

| Revision | `heldout-c1.py` | `noharm-c1.py` |
|---|---|---|
| entering `30a29797` | `harm=0 newopen=0 open=36 gained=0` | `harm=0 open=11 gained=0` |
| first landing `760428ab` | `harm=24 newopen=1 open=9` | `harm=13 open=6 gained=2` |
| repair 1 `9f4d20b9` | `harm=12 newopen=1 open=25` | `harm=0 open=0 gained=3` |
| landed `7715bb56` | `harm=0 newopen=0 open=30 gained=2` | `harm=0 open=0 gained=3` |

`harm` is a valid equivalent the entering rule bound and the graded rule refuses; `newopen` a
counterfeit the entering rule refused and the graded rule binds; `open` a counterfeit the graded
rule still binds. The landed rule refuses no valid command the entering rule bound and closes six
counterfeit classes relative to entering (`open` 36 → 30).

## Limits of the landed rule (measured, `7715bb56`)

The 30 still-open counterfeits on the 78-case battery are the provenance classes a syntax rule
cannot decide: a non-executing branch (`true || …`, `false && …`, `exit` before, `if false`),
function shadowing, a `PATH`/`python3` substitution, `sitecustomize`, overwriting the bound blob,
heredoc data, `uv run -m`, `bash -n`, `env -iCd`. A binding is a statement about the recorded
command text, never proof that the blob ran: the receipt's replay is the execution evidence, and
even a replay proves an output, not authorship.

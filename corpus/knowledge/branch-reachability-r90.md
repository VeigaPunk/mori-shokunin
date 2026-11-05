# Branch reachability — command positions a receipt's recorded command cannot execute (round 90)

source: S612 (POSIX.1-2024 Shell Command Language §2.9.3 Lists — AND-OR operators, equal precedence, left associativity), S613 (§2.9.4.4 The if Conditional Construct — which body runs and what the if reports), S614 (§2.15 `exit` — the execution environment it ends), S615 (Python 3.15.2 `ast` — `walk` order and `get_source_segment` on missing locations), S616 (Python 3.15.2 `tokenize` — comments are tokens). S611 (round 89, §2.3 Token Recognition) carries only the comment exclusion round 87 already applies.
verified-at: 2026-11-05 (round 90; S612–S614 from the POSIX page, S615 from the ast page, S616 from the tokenize page, all opened by seat Mo90S01Sources this round; pinned copies under `.ufo/waves/round-90/w1/Mo90S01Sources/sources/`, quotes re-checked by the L1 against the tag-stripped text of those copies)
recheck: 90d

## Scope

Detection and report only. This entry records which positions of a receipt's `# cmd:` text the
round-90 receipt gate (`.ufo/waves/round-87/count-c2.py`) subtracts from the binding test, what
each cited page licenses, and what stays outside the rule. The rule is a syntax rule over the
recorded command text. It does not establish that the bound bytes ran. The receipt replay is the
only execution evidence.

## Rule

A command position is non-executing when the recorded text fixes it as bypassed by a construct the
same text states in full. The gate's `invocations_visited()` walks the token stream once and marks
a simple command not-reached in exactly these cases:

1. **AND-OR short circuit** — the right operand of `&&` whose left operand is the literal `false`,
   and of `||` whose left operand is a static success (`true`, `:`, `echo`, `printf`). S612: the
   two list operators "shall have equal precedence and shall be evaluated with left associativity",
   so the left operand's status decides whether the right one runs. Frozen ids
   `R03:N-A10-false-and`, `C02:H02-false-and`, `R03:N-A09-or-short-circuit`,
   `C02:H01-or-short-circuit`.
2. **Sequencing after a terminator** — any command after a literal `exit` (or `return`) in the same
   execution environment. S614: `exit` "shall cause the shell to exit from its current execution
   environment". Frozen ids `R03:N-A08-exit-before`, `C02:H03-exit-before`.
3. **Unselected if body** — the `then` body of an `if` whose condition is the literal `false`, the
   `else` body when the condition is the literal `true`, and the `else`/`elif` bodies after an
   `elif` whose condition is statically true. S613: the condition's status selects one body, and
   the if reports "the exit status of the then or else compound-list that was executed, or zero, if
   none was executed". Frozen ids `C02:H04-if-false`; held-out ids B10/B11 of the round-90 battery.
4. **Subshell status propagation** — a subshell whose whole body is a terminator: `(exit 3) && cmd`
   does not run `cmd`. S614 applies inside the subshell, and the `&&` operand takes the subshell's
   status. Frozen id `C02:H09-heredoc-or-subshell-false` (the subshell half; the heredoc half is
   not grounded by any source opened this round and is not part of the rule).
5. **Negation** — `! true && cmd`; `!` inverts the command's status, so the `&&` right operand is
   unreachable. Held-out id B14. The `!` clause itself is §2.9.2 Pipelines, **not opened this
   round**: the rule follows from item 1 once the inverted status is known, and this line states
   that the negation operator's own specification was not read.
6. **Loop bodies that cannot run** — the body of `while false`/`until true`, and a `for v in` with
   no words. Held-out ids B01/B09/B10. §2.9.4.2 (while/until) and §2.9.4.3 (for) were **not
   opened this round**; the clause is [INFERENCE] from the loop semantics stated in the shell
   manual and is testable against the battery, not sourced.
7. **Statements after `break`/`continue` in the same loop body** — held-out id B13. Not in any
   opened source; [INFERENCE] as above.
8. **An unmatched literal `case` arm** — `case cached in fresh) cmd;; esac` where both the subject
   word and the single pattern are literals the shell does not expand and they differ. Held-out
   ids B03/B12. §2.9.4.3 (case) was **not opened this round**; [INFERENCE].

The named forms take the controlling status only from a literal `true`, `false`, `:`, `echo`,
`printf` or `exit N`. A status produced at run time (a variable, a command substitution, a
function's return, a test `[ … ]`, a glob pattern, a non-literal `case` subject) is not decidable
by this syntax rule and is never subtracted. `echo`/`printf` are treated as statically successful:
this is the frozen class's premise (a receipt that prints and then exits), not a claim that they
cannot fail on a write error.

## Structural pins (call sites)

A pin that locates a call site by walking a parse tree cannot depend on walk order: S615 states
`ast.walk` yields descendants "in no specified order", so the pin keys on node identity and on the
checked fields, and treats a missing `get_source_segment` as a failed match rather than a pass.
S616 states the tokenizer "returns comments as tokens as well", so a pin that must see or skip a
comment reads the token stream, not the tree. [INFERENCE] A source-shape pin grades the code's
shape, not its behaviour: it catches a mutation that changes the shape and misses an equivalent
refactor. The round-88 B4/B6 arms are such pins by necessity (a behavioural negative on
`clone_root_ok` also fires under the frozen `return True` mutant), and the round-90 report says so.

## Limits

The rule decides only whether a path occurrence in the recorded command text sits in a position the
grammar fixes as bypassed. It cannot decide the **provenance class**, and the round-90 counter
reports that class as `open` and never targets it: functions defined earlier in the text, `PATH` or
interpreter substitution, `sitecustomize`, blob overwrite, heredoc data, `uv run -m`, `bash -n`,
`cat`/`$0`, command substitution inside an `echo`/`printf` operand, and absolute-path spellings.
A binding is a statement about the recorded text. Nothing in S612–S616 establishes which file an
interpreter loads, which bytes a shell reads at run time, or who wrote or altered the recorded
command. The POSIX page specifies the language; it does not describe any installed shell, and no
implementation was checked this round.

No source opened this round grounds items 5–8; they are marked [INFERENCE] and rest on the
battery's 14 held-out branch cases rather than on a specification quote.

## Gate

- S612 — https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html — accessed 2026-11-05 — §2.9.3 Lists: "shall have equal precedence and shall be evaluated with left associativity"
- S613 — https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html — accessed 2026-11-05 — §2.9.4.4 The if Conditional Construct: "the exit status of the then or else compound-list that was executed, or zero, if none was executed"
- S614 — https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html — accessed 2026-11-05 — §2.15 exit [n]: "The exit utility shall cause the shell to exit from its current execution environment"
- S615 — https://docs.python.org/3/library/ast.html — accessed 2026-11-05 — ast.walk: "Recursively yield all descendant nodes in the tree starting at node (including node itself), in no specified order."; ast.get_source_segment: "If some location information (lineno, end_lineno, col_offset, or end_col_offset) is missing, return None."
- S616 — https://docs.python.org/3/library/tokenize.html — accessed 2026-11-05 — module introduction: "The scanner in this module returns comments as tokens as well"

Each quote occurs exactly once in the tag-stripped text of its pinned copy (checked by the L1,
2026-11-05, with the pinned files under `.ufo/waves/round-90/w1/Mo90S01Sources/sources/`; page
sha256 `0889867a…` for the POSIX page, `7891c588…` for the ast page, `6842ed0f…` for the tokenize
page).

## Evidence

Baseline and after readings live in `.ufo/waves/round-90/evidence/controls-r90.txt` (do-nothing,
blanket-refusal and label-only controls, before the landing) and
`.ufo/waves/round-90/evidence/after-r90.txt` (both frozen counters at the landing commit).
The held-out battery is `.ufo/waves/round-90/battery/branch-heldout.json` (18 cases: 14 branch
rejects of shapes the eight frozen ids do not use, 4 provenance `met` cases that must still bind),
written by seat Mo90E04Battery before it saw the rule.

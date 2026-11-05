# Branch reachability — which command positions in a receipt's recorded command cannot execute a bound path (round 90)

source: S612 (POSIX.1-2024 Shell Command Language §2.9.3 Lists — AND-OR operators with equal precedence and left associativity), S613 (§2.9.4.4 The if Conditional Construct — the body that runs and the status it reports), S614 (§2.15 `exit` — the execution environment it ends), S615 (Python 3.15.2 `ast` — `walk` order and `get_source_segment` on missing locations), S616 (Python 3.15.2 `tokenize` — comments returned as tokens). S611 (round 89, §2.3 Token Recognition) is cited only for the comment exclusion that round 87 already applies.
verified-at: 2026-11-05 (round 90; S612–S614 from the POSIX page, S615 from the ast page, S616 from the tokenize page, all opened by seat Mo90S01Sources; pinned copies under `.ufo/waves/round-90/w1/Mo90S01Sources/sources/`; the access date is the host UTC date at fetch time, not the 2026-11-04 date in the seat brief)
recheck: 90d

## Scope

Detection and report only. This entry records which positions of a receipt's `# cmd:` text the round-90 gate may subtract from the binding test, what each cited page licenses, and what stays outside the rule. The rule is a syntax rule over the recorded command text. It does not establish that the bound bytes ran. The receipt replay is the only execution evidence.

## Rule

A command position is non-executing when the grammar fixes it as bypassed by a construct that the same recorded text states in full. The eight frozen BRANCH ids of `.ufo/waves/round-90/count-c1.py` are the classes this covers:

1. Right operand of an AND-OR operator whose left operand is the literal `false` (`R03:N-A10-false-and`, `C02:H02-false-and`). Grounded by S612: the two list operators have equal precedence and are evaluated left to right, so the status of the left operand decides whether the right one runs.
2. Right operand of an OR-type operator whose left operand is the literal `true` (`R03:N-A09-or-short-circuit`, `C02:H01-or-short-circuit`). Grounded by S612, same mechanism.
3. A command after a literal `exit` in the same execution environment (`R03:N-A08-exit-before`, `C02:H03-exit-before`). Grounded by S614: `exit` ends the current execution environment, so a later command in that environment is not reached.
4. The then-body of an `if` whose condition is the literal `false` (`C02:H04-if-false`). Grounded by S613: the condition's status selects one body, and the if command reports the status of the body that ran.
5. A heredoc or subshell behind a false operator (`C02:H09-heredoc-or-subshell-false`). The subshell half is the rule in item 1 applied to a compound command, with S614's sentence that a subshell's exit returns to the invoking environment. The heredoc half is **not grounded** by any source opened in this round (§2.7.4 was not opened); the round-87 exclusion of echo/printf/`:`/`true`/`false` operands is the only prior ground for data operands.

Comments, redirection targets and operands of `echo`, `printf`, `:`, `true` and `false` were already excluded by the round-87 gate; this entry adds items 1–5 only.

The named forms take the controlling status from a literal `true`, `false` or `exit`. A status produced at run time (a variable, a command substitution, a function's return) is not decidable by this syntax rule and is not subtracted.

## Structural pin (call site)

A pin that locates a call site by walking a parse tree cannot depend on walk order: S615 states that `ast.walk` yields descendants "in no specified order", so the pin must key on node identity and on location fields it can check. S615 also states that a source segment is `None` when location information is missing, so a pin that reads a missing location must count as a failed match, not a pass. S616 states that the tokenizer "returns comments as tokens", so a pin that must see or skip a comment at a call site reads the token stream rather than the tree.

[INFERENCE] These are the general contracts the call-site pin relies on. This entry does not check the round-88 B4 `met_line` anchor against them; that mapping belongs to the L1 integration.

## Gate

- S612 — https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html — accessed 2026-11-05 — §2.9.3 Lists, lines 1385-1386: "shall have equal precedence and shall be evaluated with left associativity"
- S613 — https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html — accessed 2026-11-05 — §2.9.4.4 The if Conditional Construct, lines 1562-1563: "the exit status of the then or else compound-list that was executed, or zero, if none was executed"
- S614 — https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html — accessed 2026-11-05 — §2.15 exit [n], lines 2750-2751: "The exit utility shall cause the shell to exit from its current execution environment"
- S615 — https://docs.python.org/3/library/ast.html — accessed 2026-11-05 — ast.walk, lines 1907-1908: "Recursively yield all descendant nodes in the tree starting at node (including node itself), in no specified order."; ast.get_source_segment, lines 1881-1882: "If some location information (lineno, end_lineno, col_offset, or end_col_offset) is missing, return None."
- S616 — https://docs.python.org/3/library/tokenize.html — accessed 2026-11-05 — module introduction, lines 38-39: "The scanner in this module returns comments as tokens as well"

Line numbers are those of the tag-stripped text of each fetched page (the seat's own conversion, not the raw HTML). Every quoted sentence occurs exactly once in that text.

## Limits

The rule decides only whether a path occurrence in the recorded command text sits in a position the grammar fixes as bypassed. It cannot decide the **provenance class**, and the round-90 counter reports that class as `open` and never targets it by design: functions defined earlier in the text, `PATH` or interpreter substitution, `sitecustomize`, blob overwrite, heredoc data, `uv run -m`, `bash -n`, and `cat` or `$0`. A binding is a statement about the recorded text. Nothing in S612–S616 establishes which file an interpreter loads, which bytes a shell reads at run time, or who wrote or altered the recorded command. The POSIX page specifies the language; it does not describe any installed shell, and no implementation was checked this round. The Python pages state the documented contracts of `ast` and `tokenize` at version 3.15.2 only. The heredoc half of item 5 has no source in this round.

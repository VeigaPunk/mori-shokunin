# mori-pin-check v3 — implementation spec (round 48, C1)

Guidance for the seats that build or attack the v3 candidate. It is not part of the frozen
predicate; P-C1 in `contract.md` and `count-c1.py` are. Base bytes: `tools/mori-pin-check.py` at
`e5dbac05` (v2, sha256 `9832e38c…`). Output stays one `pin …` line per finding and one final
`PIN_CHECK=met|unmet …` line; new counters are appended to that line after `duplicate=`, each is
fatal when non-zero, and exit codes stay 0 met · 1 unmet · 2 setup.

| rule | closes | behaviour |
|---|---|---|
| R1 header | J1 / FG1 | the self-test header cell is recognised case-insensitively as `self-test`, `selftest` or `self test` |
| R2 visibility | J5, J6 / FG5, O1 | a table row (line starting with up to three spaces then `\|`) that is NOT part of a parsed self-test table and contains an ASCII `[A-Z][A-Z0-9_]*SELFTEST` token or the text `--selftest` counts as `hidden` (fatal). Fenced blocks are not exempt for such rows. A blank line between a header and its first row, a terminated table tail and a fence all fall under this rule |
| R3 ASCII | J2, J3 / FG2, FG3 | inside a self-test cell, a backticked span whose first whitespace-delimited token contains a non-ASCII character, or whose NFKC-casefolded text contains `selftest` but is not an ASCII tally pin, counts as `unparsed` |
| R4 rebound by prefix | J4 / FG4 | the baseline revision's set of `prefix → bound argv` is recorded; a row, new or old, that uses a baseline prefix with an argv not in that prefix's baseline set is `rebound` |
| R5 line-count pin | J7 / D2 | in a self-test cell, `(\d+) lines` binds to the nearest preceding path in the same cell that resolves to a file inside the measured tree; the file's newline count must equal the number, else `mismatch`; no such path → `unparsed` |
| R6 truncated digest | J8 / D3 | in a self-test cell, `[0-9a-f]{8,63}…` (U+2026) is a digest pin: it must be a prefix of the sha256 of some path named in the row that resolves inside the measured tree, else `mismatch`; it counts in `digest_pins` |
| R7 residuals | D4 | an escaped `\|` inside a cell stays in that cell (L2); a tally pin that is not at the start of its backticked span is `unparsed` (L4); a setup failure (unreadable SKILL.md, unresolvable revision, bad flag) exits 2 with one line, never a traceback (L5) |
| R8 selftest | w2 `MutV2*` survivors | arms for each rule above, for symlink containment of digest paths, for each `argv_ok` sub-check (path shape, `..`, `.scratch`, trailing arguments), and for case-insensitive `unparsed` detection; every new arm is killed by the mutation that removes its rule |

The real SKILL.md at the landed tip must stay `PIN_CHECK=met` under v3: a stale line-count or
truncated-digest pin the new rules expose is repaired in the registry, never excused in the tool.
`count-c1.py --tool <candidate> --rev <rev>` is the acceptance run; the tool does not read
`count-c1.py`, and no rule may special-case a variant by name or by its edit text.

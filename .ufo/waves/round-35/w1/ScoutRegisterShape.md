measured 2026-10-23T08:53:04Z

# Capabilities register shape

Question: what shape the protocol requires for SCORECARD's capabilities field (columns, home, one table versus one table per round), and which heading plus columns stay inside that shape and inside P-C1's 5-cell row.

No install. No lsp tool is in this seat's inventory; register_rows and the 5-cell check were read in full from count-c1.py, not inferred from a search hit. Confidence: high on the column lists and on singular-versus-per-round. The markdown header words are not fixed by AXES.md.

## Where it lives

AXES.md:75 titles the contract SCORECARD.md contract (per child repo). The capabilities field is one row of that contract (AXES.md:80). The round prompt tells the lane to open its own SCORECARD and to put the new row in that table (templates/round-prompt.md:13 and :26). PROTOCOL.md:450 lists SCORECARD.md in the per-repo file contract. PROTOCOL.md:483-484 puts child-repo scorecards in the child repo and root scorecards only for the protocol and aggregator lanes. Mori's register therefore lives in mori-shokunin/SCORECARD.md, not in a fleet file and not in templates/ (no SCORECARD template there; a search of templates/ for first-working, repertoire, and capabilities: returned no hits).

## Columns the protocol names

AXES.md:61-62, one field, four parts in this order: name, what it can now do (one line), evidence pointer (command or path), first-working round. The same four parts, same order, are restated at AXES.md:80 as the repertoire table: name, what it can now do, evidence pointer, first-working round. Admission rule, AXES.md:64: demonstration in the round report is pre-claiming and does not enter the table.

PROTOCOL-APPENDIX.md:49 (Multi-claim rounds, operator amendment 2026-10-16) says the amendment adds the SCORECARD.md capabilities table plus stagnation nudge. Singular table. PROTOCOL.md:520 points a capability acquisition at AXES.md, section Capabilities, measured in SCORECARD.md. It does not restate columns.

PROTOCOL.md:450 does not. That file-row says axis scores per AXES.md, then planned and retired, and never names a capabilities field. It is not a second column list.

templates/round-prompt.md does not name columns. Line 26 only says the row enters the capabilities table in the same round.

## One current table, not one table per round

Every protocol sentence above is singular: a table, the repertoire table, the row enters it. Rows accumulate when a round demonstrates the capability (AXES.md:62-64; round-prompt.md:24-26). Nothing in AXES.md, PROTOCOL.md, PROTOCOL-APPENDIX.md, or templates/ says to open a fresh table each round or to keep only that round's new rows.

P-C1 is stricter about which bytes count, and it still wants the full set in one section. contract.md:35: the last level-2 section of SCORECARD.md whose heading begins. The counter implements that as the last line that starts with a level-2 mark and then the Capabilities prefix (count-c1.py:67-71), and it reads pipe-rows only until the next level-2 heading (count-c1.py:72-77). Earlier Capabilities sections are ignored. The section that is last must hold every admitted capability and no other row (contract.md:35-44; count-c1.py:194).

Mori's file already has two sections. SCORECARD.md:586 is the heading Capabilities with the four AXES headers at :588 and a single none-yet row at :590. The last section is SCORECARD.md:627, heading Capabilities (round 12 demonstrations), same four headers at :629, five demonstration rows at :631-635. That last section is a round slice. P-C1's baseline on this tree is unmet for that reason (contract.md:69: register is the round-12 heading, 5 rows, 18 missing).

## P-C1's fifth cell

contract.md:46-47 fixes the data row at five cells, in order: MANIFEST key rounds[i].capabilities_added[j], capability, what it can now do, evidence, first-working round. Line 47: (5 cells; the key may be in backticks; evidence paths in backticks, optional :N or :N-M). count-c1.py:155-161 rejects any other width, reads the round from cell 5, and reads evidence only from backtick tokens in cell 4. One or two tokens (count-c1.py:179). Cell 1 must match rounds[i].capabilities_added[j] with optional backticks (count-c1.py:36, :142-147). A header is dropped only when its first cell, lowercased, is key or capability (count-c1.py:83-86). A header that starts with AXES's word name is an extra row. A faithful four-column data row is also extra, because the key check runs before the width check (count-c1.py:142-146 versus :155).

The counter does not grade the name cell or the what-cell. contract.md:98: several strong artifacts is the best pointer, nor the prose of the what-cell. Those two cells are still required by AXES.md:61 and by the 5-wide row. A pipe inside a cell splits the row (count-c1.py:79).

Evidence is the one place the two contracts are not the same width. AXES.md:62 allows a command or a path. P-C1 met requires one or two path tokens under its path pattern (count-c1.py:38, :161-180). A command-only pointer fails P-C1. A path pointer satisfies both. Do not backtick a command next to a path: a non-path backtick token is not-a-path, and a third token fails the 1-2 bound.

## Recommendation

Append one current repertoire section so it is the last level-2 heading in SCORECARD.md that begins with the Capabilities prefix; title it exactly that prefix with no round subtitle (a round subtitle would still match the counter, but it would contradict the singular repertoire table). Leave the sections at SCORECARD.md:586 and :627 in place; the counter does not read them once a later section exists, and the claimed work is an append. Use a header whose first cell is the word key, then capability, what it can now do, evidence, first-working round. Each data row is those five cells: the MANIFEST key (backticks optional), the capability name with no pipe, one line for what it can now do with no pipe, one or two backticked repo paths (optional :N or :N-M) and no backticked command, and the closure's round. The section holds every admitted capability, not that round's delta. Prose under the heading is fine only when it contains no pipe-row.

```
DRAFT SCORECARD.md

## Capabilities

| key | capability | what it can now do | evidence | first-working round |
| --- | --- | --- | --- | --- |
| `rounds[i].capabilities_added[j]` | <name, one line, no pipe> | <what it can now do, one line, no pipe> | `<path>` | <closure round> |
```

A second evidence path is a second backtick token in the evidence cell, not a sixth cell.

VERDICT: holds — the protocol capabilities field is one current repertoire table whose rows accumulate, not one table per round
VERDICT: fails — PROTOCOL.md:450 states the capabilities columns
VERDICT: admit — AXES.md:61-62 and AXES.md:80 are the protocol column contract (name, what it can now do, evidence pointer, first-working round)
VERDICT: reject — templates/round-prompt.md as a column specification
VERDICT: unsupported — SCORECARD.md:627-635 as the P-C1 register (round slice, four cells, no MANIFEST key)
VERDICT: supported — SCORECARD.md:588 and :629 as the AXES four-part order, under headers Capability / What it can now do / Evidence pointer / First-working round
VERDICT: no defect found — count-c1.py:65-87 and :155-179 implement the frozen 5-cell last-section rule in contract.md:35-47

## Remaining unknowns

AXES.md never spells a markdown heading or header-cell spelling; the heading above is the overlap with P-C1, not a quoted AXES heading. PROTOCOL.md:521-522 cites the Capabilities section for the exploratory reviewer rule; that rule is written in the exploratory paragraph (AXES.md:43-55) and the stagnation section, not in the repertoire-table section. That pointer was not chased further. Whether an un-backticked command may sit beside a backticked path in the evidence cell is allowed by the counter's token scan and was not recommended, because AXES asks for one pointer and P-C1 grades only paths.

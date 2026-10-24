# AttackRepairS128 — wave-2 falsification of the S128 repair row

Scope: `corpus/lessons/round-33.md` §"Round-32 repair" S128 row (`:60`) plus §4 cut-quote entry (`:98-104`),
under frozen R-R (`contract.md:85-92` / `round-33.md:39-42`). Compared against closure
`corpus/lessons/round-32-verifier-spotcheck.md:86-92`, base teaches cell `SOURCES.md:134`
(identical at `7d382043` and measured `62db24c`; verified by `diff` → IDENTICAL), and seat report
`.ufo/waves/round-33/w1/RepairS128.md`.

## Findings

### F1 — MAJOR: the row forgets one teaches-cell clause its own seat flagged unsupported
`SOURCES.md:134` teaches cell: "The two files are different contracts: oom_score_adj is the
writable -1000..+1000 preference whose value the kernel scales by totalpages/1000, oom_score is a
read-only [0, 2000] export folding that preference in, and the page's inheritance and privilege
sentences belong to the legacy oom_adj file, not to oom_score_adj."

The seat's clause table (`w1/RepairS128.md`, row 1) splits "The two proc files are different
contracts." as its own clause and marks it "Unsupported on the population page." The population
page `recheck-r32/S128.src` is the `proc_pid_oom_score_adj(5)` page (title `:8`); it documents only
`oom_score_adj`/`oom_adj` and contains no `oom_score` contract at all (`grep -n 'oom_score' S128.src`
→ only self-references of the adj page; no statement that a second, different file exists). The
score page `S128-S149-oom_score.src:72-98` describes only `oom_score`; no text states the two files
are *different contracts* (`grep -niE 'different|contract' both copies` → 0 hits; verified). So the
clause is supported on *no* page the row names — it belongs in the last column
("unsupported on every page the row names") and at minimum in the second column ("clauses the
population page does not carry"). It appears in neither. Contract item 1 (`contract.md:90-92`)
requires the correction to "name each unsupported clause"; the row names three of four (or five, by
the seat's split) and drops the frame clause. The verdict direction (`not current`) is unaffected —
one uncarried clause suffices — but the column is presented as the set of clauses the population
page does not carry, and that set is incomplete by the seat's own enumeration.

### F2 — MAJOR: §4's "whole sentence" quote is itself truncated, and the 23-word count doesn't match the displayed quote
`round-33.md:101-104` prints: "A process must be privileged (CAP_SYS_RESOURCE) to update this file,
although a process can always increase its own oom_adj setting." — and calls it "the whole
sentence" of 23 words. The committed copies end the sentence later:
`corpus/evidence/recheck-r32/S128.src:146-149` and `S149.src:145-149` both read "...its own
oom_adj setting (since Linux 2.6.20)." The cited source, `w1/RepairS128.md` (Defect-4 section),
quotes the sentence *with* "(since Linux 2.6.20)" and counts 23 rendered words. The displayed §4
quote is 20 words — the 23 count belongs to the fuller sentence the seat printed. So §4 re-truncates
the very sentence it repairs (dropping the versioned qualifier) while claiming completeness and
inheriting the other quote's word count. The operative fix (restoring the "although" exception) is
present, but the lesson text is not the whole sentence it claims to be; a "later recheck" quoting
§4 verbatim would still be a cut quote, now minus the "(since Linux 2.6.20)" tail.

### F3 — MINOR: "sha256 in its listing" points to a listing that does not exist
`round-33.md:52-53`: copies "committed at `corpus/evidence/recheck-r33/` (sha256 in its listing)".
`ls corpus/evidence/recheck-r33/` shows only `.src` files; `grep -rn 6169628d .ufo/waves/round-33/
corpus/` finds the sha only in `w1/RepairS128.md`, `w1/RepairS149.md`, and `SOURCES.md` audit cells
— no listing file under `recheck-r33/` or `.ufo/waves/round-33/evidence/` records it. The chain is
independently intact: `SOURCES.md:134` records `7,955 B sha256
6169628d8a2cdc512795cfda74f3598d5b7a25e5b71921d4088c0539cf71b2bc` for the second URL and
`sha256sum corpus/evidence/recheck-r33/S128-S149-oom_score.src` returns exactly that value. Only
the pointer "its listing" is wrong.

## Checks that passed

- **(a) Supported-on-another-page pointer.** `S128-S149-oom_score.src:73-75` reads "This file
  displays the current score that the kernel gives to this process for the purpose of selecting a
  process for the OOM-killer." — states the display clause verbatim. `:97-98` reads "The oom_score
  also reflects the adjustment specified by the oom_score_adj or oom_adj setting for the process."
  — states the reflect clause (row's paraphrase drops `oom_adj`, still accurate). The file is the
  `proc_pid_oom_score(5)` man7 page (title `:8`, footline "Linux man-pages 6.19" `:120`) — S128's
  own second URL per `SOURCES.md:134`. Committed at `62db24c` (`git log`); sha256 matches the
  source-cell fetch ledger and the seat's fetched copy.
- **(b) Unsupported clauses.** Greps on both named pages (`recheck-r32/S128.src`,
  `recheck-r33/S128-S149-oom_score.src`): `totalpages` → 0 hits; `2000` → 0 hits;
  `read.only|readonly` → 0 hits; `write|writing|read` on the score page → 0 hits; `1000` hits are
  value-range text only (`S128.src:78,83,104-108`), never a `totalpages/1000` scaling statement.
  The parenthetical "(these rest on S127 kernel code, a different row)" is accurate: S128's source
  cell names only the two man pages; S127 is a separate row (`SOURCES.md:133`); no committed
  `base.c` copy exists under `corpus/evidence/` (`find` → none), consistent with R-R's
  "companion source" exclusion.
- **(c) Closure match.** Row's "does not carry" column ("`totalpages/1000` scaling; read-only
  `oom_score` `[0,2000]` export") is verbatim the closure's S128 line at
  `round-32-verifier-spotcheck.md:90` and matches the base teaches cell — but see F1: it is the
  closure's list, not the complete clause-level set.
- **(d) Seat-report comparison.** The seat's clause table is strictly more complete than the row:
  it separately names the "different contracts" clause (dropped in the row — F1) and the
  reflects-adjustment clause (folded into the middle column — acceptable). The seat's caveat that
  the second-URL copy "is not yet committed" is now superseded correctly: the copy is committed at
  the measured revision.
- R-R quoted verbatim in `round-33.md:39-42` matches `contract.md:85-92` word for word.

## Residual risk / gaps

- F1's severity assumes the colon-framed "The two files are different contracts" is a checkable
  clause; if the repair judge reads it as pure framing, F1 downgrades to minor (the row then omits
  nothing material). The seat's own clause split counted it, which is the reading I applied.
- Not checked (out of scope): other rows in the §1 table; whether man-pages 6.20 upstream still
  serves the same bytes; whether `count-c1-a1.py` inspects these correction rows at all.
- No tools installed; no installs needed. All greps were read-only; no writes outside this report.

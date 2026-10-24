# C1 SKILL.md row draft

## Behavior

Five Round31 decision rows translate the requested pid-probe limits into operational decisions. They use the existing Round30 four-column row convention: Situation, What to conclude, What not to conclude, Grounding. Each row names `Round31`, the entry path, and its assigned source IDs.

## Ready-to-paste rows

```markdown
| a `pgrep` result matches a watchdog-related process name | treat the PID as a candidate; verify an attribute tying that same process instance to `scripts/shokunin-watchdog.sh` under the fleet root before reporting the watchdog alive | that a matching process name uniquely identifies the fleet watchdog | (Round31) `corpus/knowledge/watchdog-identity-r31.md` (name-match row); S161, S162, S169 |
| the watchdog's process name exceeds 15 bytes and `pgrep` is run without `-f` | `comm` is truncated to 15 bytes; use a pattern of at most 15 bytes or treat a longer-pattern miss as inconclusive | that no match with a longer pattern proves the watchdog is absent | (Round31) `corpus/knowledge/watchdog-identity-r31.md` (comm-truncation row); S161, S163, S169 |
| `pgrep -f` returns a matching PID | treat it as a candidate: `-f` matches a command line mentioning the name, so check that the command line identifies the watchdog script and fleet root | that any command-line mention proves the fleet watchdog is running | (Round31) `corpus/knowledge/watchdog-identity-r31.md` (full-command-line row); S161, S162, S170 |
| `pgrep` exits 1, exits 2 or 3, or the `pgrep` binary is missing | exit 1 means no match; exits 2 or 3 and a missing binary make the probe unavailable, not negative | that an error or missing probe establishes watchdog absence | (Round31) `corpus/knowledge/watchdog-identity-r31.md` (probe-result row); S161 |
| a candidate PID has a readable start time in `/proc/<pid>/stat` | record the PID and start time together as the identity pair for that process instance and compare both on later observations | that a PID alone is a stable identity, or that the pair alone proves the watchdog script path or role | (Round31) `corpus/knowledge/watchdog-identity-r31.md` (PID/start-time row); S171 |
```

## Placement

`SKILL.md:744-755` contains the Round30 section and its four-column table; line 755 is the last row and the file's end. Add a new Round31 section after line 755, with a Round30-style four-column header and separator, then insert these five data rows in the order shown. The first row follows the new table separator; each later row follows the prior row. Do not append them to the Round30 table. The Round30 header is at `SKILL.md:750` and its data rows at `SKILL.md:752-755`.

## Gate status

This is draft text only. The frozen C1 predicate requires at least four SKILL lines naming both `Round31` and the entry path (`.ufo/waves/round-31/contract.md:28-37`). These five drafts satisfy that text shape, but they do not establish C1: no SKILL edit or counter run was made, and the remaining predicate covers the knowledge entry, SOURCES rows, Gate rows, upstream copies, and hashes (`.ufo/waves/round-31/contract.md:30-37,45-46`).

## Provenance and limits

- The row convention and placement were read from `SKILL.md:744-755`.
- The frozen C1 scope and predicate were read from `.ufo/waves/round-31/contract.md:28-46`.
- Assigned source IDs and their intended subject matter are listed in `.ufo/waves/round-31/wave1-spec.json:10,15,20,50,55,60`: S161 pgrep manual, S162 pgrep implementation, S163 scheduler task-name length, S169 proc comm, S170 proc cmdline, and S171 proc stat. These are assignment/source-map references, not evidence that I fetched or verified those upstream bytes.
- The claims in the rows follow the task's supplied facts and source assignments; I did not independently fetch the upstream sources, inspect admitted Gate quotes, or confirm current SOURCES rows. Parent integration should retain the rows only with the corresponding source evidence.

## Commands and outcomes

No shell commands were run. Static read/search tool calls located the Round30 table, C1 predicate, and source assignments cited above. No processes were started, no tools were installed, and no build, test, lint, or counter was run.

## Touched surfaces and out of scope

Only this scoped report was written: `.ufo/waves/round-31/w1/DraftSkillRowsC1.md`. `SKILL.md`, product code, source registry, Gate report, and source-copy files were not edited. No source fetch, process probe, git/jj write, or C1 verification was performed.

## Artifact path

`.ufo/waves/round-31/w1/DraftSkillRowsC1.md`

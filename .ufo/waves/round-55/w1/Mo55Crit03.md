# Mo55Crit03 — C1 voter binding critique

Scope: static review of the frozen C1 counter, its selftest, the round-55 contract and current wave registry. No vote was cast. No counter, ledger, result, or production file was changed.

## Findings

### HIGH — Mismatched fence delimiters can leak a fenced vote

`count-c1.py:270-280` toggles one Boolean whenever the first three non-indented characters are either backticks or tildes; it does not remember the opening delimiter or length. Thus a Markdown fence opened with `~~~text` is incorrectly closed by a line containing ``` even though CommonMark requires the matching delimiter. A concrete report can contain `~~~text`, then ``` as content, then `RECHECK <hash> holds`, then `~~~`; the counter parses the vote as outside the fence. If two allowed voter files and their result outputs contain that line, the row can gain two apparent settled holds from code examples, violating the contract's no-fenced-votes condition (contract.md:22-26). The selftest covers only a balanced backtick fence (`selftest-c1.py:188-192`), not mixed delimiters. This is a static counterexample, not an executed fixture.

Smallest safe correction for a future counter: track fence character and opening run length; only a valid matching closer ends the block. Add the mixed-fence case as a control. Do not mutate this frozen counter in this seat.

### HIGH — Vote token accepts contradictory suffixes and only binds a prefix

The vote regex is not end-anchored (`count-c1.py:267-280`), so `RECHECK <hash> holds — actually stale; the v7.3 claim is unsupported` is stored as `holds`. Output binding (`count-c1.py:299-303`) accepts any output line starting with `RECHECK <hash> holds `, rather than requiring the complete line to match. Two such reports can therefore count as agreeing holds while their suffix explicitly records the opposite conclusion; the dissent scan sees only the captured token (`count-c1.py:384-388`). This is a false green when dissent is present in the same purported vote line. The selftest's last-vote case exercises only clean tokens (`selftest-c1.py:193-196`), so it does not catch the suffix case.

Smallest safe correction for a future counter: enforce the exact permitted holds line and a separately parsed stale line with required reason/path; bind the complete normalized line, not a prefix. Treat malformed/contradictory vote lines as invalid and fail closed.

### MEDIUM — Result-to-report binding is name-and-substring, not provenance binding

The counter loads `results` and assigns `outputs[name]` (`count-c1.py:284-303`); duplicate names silently overwrite earlier records (`:289-292`). For each report file it checks only that the same name has some output line equal to, or prefixed by, the parsed vote (`:299-303`). It does not compare a result's `report` field to that exact file, bind a report digest, validate the result against dispatch/registry identity, or reject duplicate result names. A constructed results file can therefore attach a matching output to a different report bearing the same voter name; likewise, copying one review/report and its output under two allowed names can satisfy the two-name minimum without proving two independent settled reviews. The frozen list itself is correctly limited to Mo55Rc01–Mo55Rc16 (`count-c1.py:56-57`), and the selftest checks that outside names do not count (`selftest-c1.py:172-173`); the gap is that the names are the only identity binding. Current registry records show Mo55Rc01 and Mo55Rc05 as separate members but both `agentId: null` at this snapshot (`w1/swarm-registry.json:8-17,32-41`), so the present snapshot does not establish runtime identity either way.

Smallest safe correction for future settlement: require a unique result record per frozen voter and bind its declared report path plus a report-content digest (or equivalent collector-authenticated identity) to the exact `w1/<name>.md`; reject duplicate names. Require distinct settled runtime identities if “distinct voters” means independent executions. Keep the frozen voter allowlist.

### LOW — Verified safeguards and dissent behavior

The counter hardcodes precisely the sixteen C1 names (`count-c1.py:56-57`); the selftest confirms missing/unbound outputs and non-frozen names do not satisfy the minimum (`selftest-c1.py:162-173`). A mismatching vote causes dissent even when unbound (`count-c1.py:384-388`; `selftest-c1.py:181-187`), which is conservative rather than a false green. Last *recognized* vote per hash wins, not necessarily the last line of the report (`count-c1.py:270-281`); clean stale-then-holds is explicitly expected to pass (`selftest-c1.py:193-196`). That rule ignores later ordinary prose, so a report can append a prose-only reversal after a clean vote without affecting the parser; whether such prose is an admissible dissent is a contract-format gap, not an observed round-55 vote.

## Evidence and command record

- Read-only sources: `.ufo/waves/round-55/count-c1.py:56-57,267-303,384-388`; `.ufo/waves/round-55/checks/selftest-c1.py:162-196`; `.ufo/waves/round-55/contract.md:21-26`; `.ufo/waves/round-55/w1/swarm-registry.json:8-17,32-41`.
- `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → exit 0; `/fast/scratch/hyaku` showed 593.1G free, so no ENOSPC stop condition.
- No tests, counter execution, fixture mutation, installs, or Git/JJ mutations were performed. The counterexamples above are static deductions from the cited parser code and are not claimed as executed.
- Scratch was created at the assigned path and removed before handoff.

## Findings

- **HIGH** — Cross-delimiter fence toggling can count fenced examples as votes: `count-c1.py:270-280`; untested control boundary `selftest-c1.py:188-192`.
- **HIGH** — Non-anchored vote regex plus prefix output match can suppress explicit contradictory suffix/dissent: `count-c1.py:267-280,299-303,384-388`.
- **MEDIUM** — Same-name outputs are not cryptographically/structurally bound to exact report or unique settled execution: `count-c1.py:284-303`; round registry snapshot `w1/swarm-registry.json:8-17,32-41`.
- **LOW** — Allowlist, missing/unbound handling and unbound dissent behavior are covered and conservative: `count-c1.py:56-57,384-388`; `selftest-c1.py:162-187`.

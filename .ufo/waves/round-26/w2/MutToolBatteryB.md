# MutToolBatteryB — C2 mutation battery, mutants M11–M20

Seat: `MoriR26.MutToolBatteryB` (leaf mutation tester, wave 2, round 26).
Date: 2026-10-22. Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only here).
Sandbox clone: `/fast/scratch/hyaku/mori-r26/wt-w2mutB`, branch `r26-wt-w2mutB`,
base `16935e24c93fa7e7567413d7ec091339a5df1474` (verified with `git rev-parse HEAD`).
Scratch: `/fast/scratch/hyaku/mori-r26/MutToolBatteryB/pristine-tool.py` (restoration source).

## What this attacks

C2 (contract.md:48-56, amendment A1 at contract.md:139-146): the tool must print
`MORI_OOM_KILLERS_SELFTEST: PASS N/N` and exit 0 on the frozen, unchanged case file
(`N=32`, cases frozen at `5b10649d`, file unchanged since). This battery asks a sharper
question than "does it pass": **does the counted 32-case artifact actually discriminate the
behaviour the tool claims?** A mutant that survives is a coverage finding about the artifact,
not a licence to change the contract.

## Method

* Tool under test: `tools/mori-oom-killers.py` in the sandbox, pristine sha256
  `1a71b2dfa45ef547b1a5042cc71a28ae63f54af35d0c4973f6056bf439b2f8e4` (809 lines).
* Case files, unchanged in the sandbox:
  * counted `tools/fixtures/mori-oom-killers/cases.json` sha256
    `84d2343f1d672a4597a4ec5efe0fd048eb399e8b4f0f5b86cc483ff8f2e547af` (32 cases);
  * supplementary `tools/fixtures/mori-oom-killers/cases-supplementary.json` sha256
    `277684eb8f622c2c3eeaf118f65c28d02c0196dd459052aa387989b4fb11269d` (32 cases).
* Detectors (per the design seat, §1): D1 = `python3 -I -B tools/mori-oom-killers.py --selftest`
  must print exactly `MORI_OOM_KILLERS_SELFTEST: PASS 32/32` and exit 0; D1' = the same with
  `--cases tools/fixtures/mori-oom-killers/cases-supplementary.json`. Anything else is a kill.
  A detector failure on pristine bytes would make a mutant inconclusive; that did not happen.
* Baseline (pristine, before any patch), both files:
  `MORI_OOM_KILLERS_SELFTEST: PASS 32/32`, exit 0 (twice). Python 3.14.8.
* Per mutant: patch one site → run D1 and D1' → restore the exact bytes from the pristine copy →
  re-hash. The restore hash after every one of the ten mutants was
  `1a71b2dfa45ef547b1a5042cc71a28ae63f54af35d0c4973f6056bf439b2f8e4`, and `git status --porcelain`
  in the sandbox is empty at the end (0 lines). No file outside the sandbox was written except
  this report.
* No tool was installed or upgraded (no pacman, no uv, no npm); the stock `python3` on the host was
  sufficient. Nothing was recorded under the tooling directive because nothing was changed.

## Result table

| Mutant | Site (pristine line) | Counted 32-case file | Supplementary 32-case file | Killing case(s) |
|---|---|---|---|---|
| M11 null read reported as quiet | `tools/mori-oom-killers.py:251` | **KILL** (FAIL 31/32) | **KILL** (FAIL 31/32) | c08 |
| M12 show text without `ActiveState` read as inactive | `:203-204` | **KILL** (FAIL 31/32) | **KILL** (FAIL 31/32) | c27 |
| M13 `scope_complete` from whole journal | `:378` | **KILL** (FAIL 30/32) | **KILL** (FAIL 30/32) | c04, c05 |
| M14 grammar version never verified | `:379` | **KILL** (FAIL 29/32) | **KILL** (FAIL 28/32) | c04, c05, c09 (+c34) |
| M15 version token truncated at first dot | `:340` | **KILL** (FAIL 18/32) | **KILL** (FAIL 20/32) | c01, c02, c09, c13, c16-c24, c28 (+c33) |
| M16 inactive killer reports zero counts | `:398` | **KILL** (FAIL 29/32) | **KILL** (FAIL 29/32) | c06, c07, c29 |
| M17 absent unit treated as inactive | `:201-202` | **KILL** (FAIL 31/32) | **KILL** (FAIL 31/32) | c07 |
| M18 mem and swap thresholds swapped | `:344`, `:348` | **SURVIVE (PASS 32/32)** | **KILL** (FAIL 31/32) | c33 |
| M19 threshold parser rejects width-padded number | `:103`, `:106` | **KILL** (FAIL 29/32) | **KILL** (FAIL 29/32) | c01, c20, c28 (+c33) |
| M20 threshold parser accepts integers only | `:100` | **KILL** (FAIL 29/32) | **KILL** (FAIL 29/32) | c01, c20, c28 (+c33) |

One survivor (M18) out of ten; it is a finding about the counted artifact, not a defect of the
tool. Details below.

## Per-mutant evidence

All patches are the design seat's minimal change, adapted minimally to the landed code shape
where the design's suggested text does not exist; adaptations are named.

**M11 — null read reported as quiet.** Patch: `:251` `journal = inputs.get("earlyoom_journal")`
→ `journal = inputs.get("earlyoom_journal") or []` (design's change verbatim, adapted to the
landed `.get` form). Killed by c08 in both files:
`FAIL c08-null-journal: earlyoom.actions: got {"escalations": 0, ...} expected null`.
Note what did *not* change: the verdict of c08 stayed `KILLERS_UNKNOWN` / exit 2 under the mutant,
because an empty journal also leaves `scope_complete` false. So c08 discriminates the rule
"a null read is a failed read" only through the `earlyoom.actions: null` pin, not through the
verdict. The frozen file would not catch a tool that continued silently on a null journal if it
also reported `actions: null`.

**M12 — show text without `ActiveState` read as inactive.** Patch: `:203-204` `return "unavailable"`
→ `return "inactive"`. Killed by c27 in both files, on the verdict and exit only:
`verdict: got 'KILLERS_QUIET' expected 'KILLERS_UNKNOWN'`, `exit: got 0 expected 2`.
c27 pins no `earlyoom.state`, so the state vocabulary for a show text without `ActiveState`
(`unavailable`) is not pinned by any counted case; the verdict carries it. `unavailable` as a
field value is pinned only for a *null* show (c25). [INFERENCE] a tool that mapped the same show
text to `unavailable` but kept the verdict rule would pass both files.

**M13 — `scope_complete` computed from the whole journal.** Design's shape (`saw_version_line`
vs `saw_version_in_scope`) does not exist in the landed code, which derives `version` only from
scoped lines. Minimal adaptation, one site, `:378`:
`scope_complete = scope_known and version is not None and not suppressed` →
`scope_complete = (scope_known and any(RE_VERSION.match(_entry_text(e).lstrip()) for e in (journal or [])) and not suppressed)`.
Killed by c04 and c05 in both files (`earlyoom.scope_complete: got true expected false`).
c05's verdict stayed `KILLERS_UNKNOWN` (its grammar is unverified), so again the field pin is
what discriminates.

**M14 — grammar version never verified.** Patch: `:379` → `grammar = GRAMMAR_VERIFIED`.
Killed in both files by c04, c05, c09 (`verdict: got 'KILLERS_QUIET' expected 'KILLERS_UNKNOWN'`,
`earlyoom.grammar: got "verified-1.9.0" expected "unverified"`); the supplementary file kills
one more case, c34. The counted file does discriminate this rule.

**M15 — version token truncated at the first dot.** Patch: `:340`
`version = RE_VERSION.match(text).group(1)` → `...group(1).split(".")[0]`. Killed in both files
by 14 counted cases (c01, c02, c09, c13, c16-c24, c28) and 16 supplementary cases.
The mutant is loud because `grammar` follows the truncated token.

**M16 — inactive killer reports zero counts instead of null.** Patch: `:398` in the
`earlyoom_state != "active"` branch, `actions = None` → `actions = dict(counts)`.
Killed in both files by c06, c07, c29 (`earlyoom.actions: got {...zeros} expected null`).
The counted file compares a `null` expectation as a whole block, so this defect is caught here;
a selftest that skipped null expectations (design M32) would have hidden it.

**M17 — absent unit treated as inactive.** Patch: `:201-202` `return "absent"` → `return "inactive"`.
Killed in both files by c07 (`earlyoom.state: got "inactive" expected "absent"`).

**M18 — mem and swap thresholds swapped.** Patch: `:344` and `:348`, the two tuple assignments
`term_thresholds`/`kill_thresholds` have their two targets swapped. (The design's "swap the two
assignment targets in the threshold parser" maps exactly onto these two lines in the landed code.)
**SURVIVED the counted file: `MORI_OOM_KILLERS_SELFTEST: PASS 32/32`, exit 0.** Killed by the
supplementary file only, by c33:
`earlyoom.thresholds.term_mem_pct: got 15.0 expected 20.0`, `term_swap_pct: got 20.0 expected 15.0`,
`kill_mem_pct: got 8.0 expected 10.0`, `kill_swap_pct: got 10.0 expected 8.0`.
Meaning for C2: every counted case whose threshold lines are symmetric (`10.00/10.00` and
`5.00/5.00`, i.e. c01, c20, c28) is blind to a mem/swap transposition. The counted artifact
therefore does **not** demonstrate that the tool reads the mem and swap percentages in the
contracted order (contract.md *Message grammar*: mem first, swap second); only the
supplementary artifact (c33) does. This is the concrete instance of the design seat's §1.1
observation that the two files are not nested and each kills mutants the other cannot. The tool
itself is correct here — the mutant is killed by the supplementary file — so the defect is in the
counted artifact's coverage, not in the landed tool.

**M19 — threshold parser rejects the width-padded number.** Patch: `:103` and `:106`,
`<=\s*` → `<= ` in both threshold regexes (the design's `<= +(\d+\.\d+)%` narrowing, adapted to
the landed `<=\s*` form). Killed in both files by c01, c20, c28 (+c33):
`earlyoom.thresholds.kill_mem_pct: missing in result (expected 5.0)` and the same for the other
three pins. The width-5 padding of upstream `PRIPCT` (`msg.h:10`) is what the counted file pins.

**M20 — threshold parser accepts integers only.** Patch: `:100`
`_PCT = r"[0-9]+(?:\.[0-9]+)?"` → `_PCT = r"[0-9]+"`. Killed in both files by c01, c20, c28 (+c33)
with the same failure set as M19. Note: the counted artifact cannot distinguish M19 from M20 —
both collapse the threshold object to `null` and produce identical failure lists — so the four
threshold pins in c01 show only that the host-shaped percentages parse, not which parse rule
accepted them.

## Findings

1. **Coverage gap in the counted artifact (severity: medium for the C2 claim, not a tool defect).**
   The counted 32-case file cannot detect a mem/swap transposition of the threshold fields
   (M18 survives it, PASS 32/32). C2's counted value therefore rests on a case file that does
   not exercise the mem-vs-swap ordering of the message grammar. The supplementary file closes
   the gap (c33), so the capability is real, but the *counted* evidence for it is one case short.
   Recommendation for the L1 (decision, not applied here): either disclose the ordering limit in
   the capability row, or count the supplementary file's c33 as part of the C2 evidence.
2. **Verdict-level blindness where the field pin carries the kill (severity: low, disclosure).**
   For M11, M12 and M13 the mutant's verdict is unchanged on the killing case (M11: c08 stays
   `KILLERS_UNKNOWN`; M12: the kill is the verdict itself; M13: c05 stays `KILLERS_UNKNOWN`).
   In other words the rules "a null read is a failed read", "a show text without `ActiveState`
   is unavailable" and "`scope_complete` is about the current invocation" are carried by
   field-level pins in these cases. If the field comparison were weakened, the verdict rules
   behind them would be unverified; the counted file is adequate only because it compares the
   pinned dotted paths, including a `null` expected as a whole block (M16 confirms that block
   comparison works).
3. **No tool defect found in M11–M20.** Every mutant that reached a discriminating case died;
   the single survivor is a property of the counted case set, and the landed tool is correct
   under both artifacts.

## Restoration evidence

`tools/mori-oom-killers.py` sha256 after every restore:
`1a71b2dfa45ef547b1a5042cc71a28ae63f54af35d0c4973f6056bf439b2f8e4` (identical to the pristine
pre-mutation hash, all ten times). `git status --porcelain` in
`/fast/scratch/hyaku/mori-r26/wt-w2mutB` is empty; `git diff --stat` prints nothing. Both case
files are untouched (hashes above unchanged). Final re-run on restored bytes: counted
`PASS 32/32` exit 0, supplementary `PASS 32/32` exit 0.

## Verdict per item

| Item | Verdict |
|---|---|
| C2 counted value `PASS 32/32` on the frozen file | **holds** (baseline re-run, pristine bytes) |
| C2 capability claim as evidenced by the counted file alone | **defect (medium, coverage)** — M18 survives; mem/swap ordering is not discriminated by the counted cases |
| Tool behaviour under mutants M11–M20 | **holds** — 9 of 10 mutants killed by the counted file, 10 of 10 by the two files together; no tool defect observed |
| Privacy of the tool's output | **not run** (out of this seat's scope; D5 belongs to the harness-level seats) |
| Detectors D2–D10 | **not run** (this battery used D1 and D1' only, as assigned) |

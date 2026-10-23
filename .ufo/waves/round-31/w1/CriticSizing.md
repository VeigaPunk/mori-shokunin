# CriticSizing — round 31 claim sizing audit (wave 1, critic, leaf seat)

Scope: round prompt `/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-31.md:343-365` (§6 item 9), round-30
closure `corpus/lessons/round-30-verifier-spotcheck.md:170-196`, `.ufo/waves/round-31/contract.md`, and the SCORECARD
round-31 declaration (`SCORECARD.md:1827-1841`). All paths are relative to the lane repo unless absolute.
Tools installed or updated: none. Sandbox: `/fast/scratch/hyaku/mori-r31/CriticSizing/` (clone `junk/`, script
`oracle-c2.sh`, fetches `fetch/`). No lane or fleet writes other than this report; no processes left running.

## Verdict table

| # | Check (§6 item 9) | C1 depth | C2 operability | Evidence |
|---|---|---|---|---|
| 1 | After-state is one concrete value, one command over committed bytes | PARTIAL: one value (`C1=met`, exit 0), one command, but it also depends on bytes fetched over the network when it runs | PASS: `C2=met`, `exact=16/16`, exit 0; reads only committed blobs | `count-c1.py:50-56,158-164`; `count-c2.py:53-70` |
| 2 | Declared before-value matches the committed receipt | PASS | **FAIL**: the declaration says exit 1, but the receipt shows `C2=error`, exit 2 | `SCORECARD.md:1837`, `contract.md:21` versus `evidence/c2-before-base.txt` |
| 3 | No universal clause the counter does not enumerate | PASS for the predicate; the title is broad | **FAIL**: the title says "every forbidden entry", but the counter enumerates only 16 fixtures | `contract.md:28,57`; `SCORECARD.md:1836-1837` |
| 4 | Same predicate sentence in contract, counter docstring and code | PASS: the sentence is identical | **FAIL**: the docstring drops "no hit line outside the 16 briefs" (the code still checks it) | normalized word diff, below |
| 5 | Do-nothing and shortcut controls committed before data, in order 2124cbcd then 8baccf4a | PASS | PASS | git log, below |
| 6 | The cheapest control that skips the claimed work does not meet the counter | **FAIL**: a junk-reading table meets C1 | **FAIL**: a fixture-lookup oracle meets C2 | sandbox runs, below |
| 7 | No rule changed after data | PASS | PASS | frozen-file hashes and diff, below |
| 8 | Claims are causally separable | PASS | PASS | counter read sets, below |
| 9 | At least one claim is on the lowest-scoring axis | PASS: depth 5, tied lowest | n/a | `SCORECARD.md:12-14` |
| 10 | Sized to land within one round | PASS, though two pre-assigned URLs 404 | PASS | curl, below |

## Evidence

### Commit order and freeze (checks 5 and 7)

```
$ git log --format='%H %ad %s' --date=iso-strict -3
8baccf4a… 2026-10-22T20:38:45-03:00 round-31: before receipts and do-nothing/shortcut control receipts …
2124cbcd… 2026-10-22T19:54:19-03:00 round-31: freeze contract, counters, C2 fixtures and control scripts before data
a12c68ae… 2026-10-22T19:54:19-03:00 round-30 verifier spot-check …
$ git merge-base --is-ancestor 2124cbcd 8baccf4a && echo ordered      → ordered
$ git log -1 --format='author=%ad committer=%cd' --date=iso-strict 2124cbcd
author=2026-10-22T19:54:19-03:00 committer=2026-10-22T20:37:48-03:00
$ git diff --stat 2124cbcd 8baccf4a   → only the 4 evidence/*.txt files (140 insertions)
```

- The freeze commit's author date is the second the entering tip was committed. `jj --ignore-working-copy op log`
  shows `edit commit metadata for commit a0adedff…` at 20:37:47 and the commit at 20:37:48. My reading is that jj
  stamps the author date when the change is created [INFERENCE]. So the real freeze time is the committer date,
  20:37:48. This is not false provenance. However, `git log` (author date by default) makes the freeze look
  simultaneous with the entering tip, and the closure should be told to read `%cd`.
- Data started after the receipts. `wave1-spec.json` has mtime 20:42:13, and LOG (working copy) says "Wave 1
  dispatched 23:43Z", which is 20:43 local. The receipts commit is 20:38:46.
- All 8 frozen files are unchanged in the working tree. The first 16 hex digits of the sha256 for each file at
  `2124cbcd` equal the working-tree hash: contract `a72d1697…`, count-c1 `05b1f243…`, count-c2 `cbf01911…`,
  fixtures `1442c14e…`, rule-text `79ea24c8…`, and the three controls `4d5109e7…`, `89d1b947…`, `84d63760…`.

### Check 2: C2 before-value is false as declared

The declaration reads:

```
SCORECARD.md:1837  `python3 .ufo/waves/round-31/count-c2.py a12c68ae` → `tool=absent`, `C2=unmet`, exit 1
contract.md:21     The command that shows it unmoved: `count-c2.py a12c68ae` → `tool=absent`, `C2=unmet`.
```

The committed receipt reads:

```
evidence/c2-before-base.txt:  rev=a12c68ae…  count-c2: fixtures absent at revision  C2=error  exit=2
```

The cause is that `count-c2.py:53-55` reads the fixtures from `<lane-rev>`, and they did not exist before
`2124cbcd`. The only `tool=absent`/`C2=unmet` before-value is at `2124cbcd` (`evidence/c2-controls.txt:1-6`).
The uncommitted `LOG.md` working copy (around line 2000) discloses this and points to "lesson M1". The committed
SCORECARD cell still states exit 1. SCORECARD is the self-assessment that calibration is scored against
(`AXES.md:15`), so a false cell left standing is a calibration-harm hook.

### Checks 3 and 4: universal wording and predicate identity

- C2 title (`contract.md:57`, `SCORECARD.md:1837`): "reports every forbidden entry". The counter enumerates the 16
  fixtures only (`count-c2.py:126-133`). The oracle in check 6 meets C2 while reporting nothing on any brief
  outside the fixture set, so the universal is demonstrably unmeasured.
- C1 predicate universals are all enumerated in code: "every row" is the loop at `count-c1.py:119-126`; "every
  such id" is the loop at `:134-161`; "every quote" is the `all()` at `:156`. The C1 title "how a pid probe can and
  cannot establish…" is a topic statement that the counter does not test (see check 6).
- Normalized word diff between each contract predicate and its counter docstring (Python `difflib`):

```
P-C1 IDENTICAL
P-C2 DIFFER
  delete contract: no hit line outside the 16 briefs, | docstring:
```

  The code does enforce that clause (`count-c2.py:144`, `not stray`), so code and contract agree. Only the
  self-imposed rule at `contract.md:6` ("same sentence here, in its counter's docstring") is broken.
- Minor: the C1 code is stricter than its sentence. `count-c1.py:121` requires `len(row) == len(hdr)` and requires
  every cited id to be a SOURCES row, while the sentence says "naming at least one S### that is a SOURCES row". This
  can only turn a predicate-met entry into `unmet`.

### Check 6: cheapest controls that skip the claimed work

**C1 junk-row control.** The sandbox clone is at `8baccf4a`. The entry has 8 rows, every row reads "bananas are
yellow", and the rows cite S161, S165, S169 and S173. Each copy is the real upstream bytes. Each Gate quote is the
one word "the". SKILL.md gets 4 junk lines naming Round31 and the path.

```
$ python3 .ufo/waves/round-31/count-c1.py 1f5710a84693aabfc8ef37dc07a07078fe9325ee --repo /fast/scratch/hyaku/mori-r31/CriticSizing/junk
rows=8 rows_ok=8 new_id_rows=8 new_ids=4 (S161,S165,S169,S173)
S161 gate=ok quotes=1 copy=ok fetch=ok url=https://gitlab.com/procps-ng/procps/-/raw/v4.0.7/man/pgrep.1
S165 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/binfmt_script.c
S169 gate=ok quotes=1 copy=ok fetch=ok url=https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_comm.5?h=man-pages-6.20
S173 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/sysctl/kernel.rst
gates_ok=4/4 copies_ok=4/4 fetch_ok=4/4
skill_rows=4
C1=met
exit=0
```

Committed controls (a) and (b) (`evidence/c1-controls.txt`) test only a missing source and a fabricated copy. They
never test the case where the sources are real and the content is empty. The only guard against that case is the
uncounted residual at `contract.md:54`.

**C2 fixture-lookup oracle.** `/fast/scratch/hyaku/mori-r31/CriticSizing/oracle-c2.sh`, 20 lines, implements no
part of the rule. It reads `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-31/c2-fixtures.json` by
absolute path, matches each brief's bytes against the fixture lines with the placeholder replaced by the brief
name, and prints that fixture's `expect` list. The randomized brief names (`count-c2.py:80-85`) defeat only
name-keyed shortcuts such as committed shortcut 2.

```
$ python3 .ufo/waves/round-31/count-c2.py 8baccf4a --tool-file /fast/scratch/hyaku/mori-r31/CriticSizing/oracle-c2.sh
tool=file:… sha256=64dbe4521a59013692abfba27a20f0970db25a1d6328c5d3d13142c45c5fec02
tool_exit=1
scanned=16 scanned_ok=yes blind_violations=14 hit_lines=14 count_ok=yes exit_ok=yes stray=0
fixtures=16 exact=16/16
C2=met
exit=0
```

This is exactly the pattern §6 item 9 names (prompt `:352-353`): "kake r34, where a no-parse replay and a junk-row
commit met both counters". The mitigations differ by claim:

- C2 is mitigated in practice. The builder seats are told "Do NOT open … c2-fixtures.json" (`wave1-spec.json:105,110`),
  and an oracle has to name the fixture path or embed its text, which a byte check on the landed blob catches.
- C1 has no byte-level guard. Only a non-author reading of each row can catch it.

### Check 1: C1's network dependency, defect or tradeoff

- It is a tradeoff, not removable. The fetch clause is the only thing that makes control (b) miss: `fetch=bad`
  0/4 is its sole failing condition (`evidence/c1-controls.txt:21-33`). Removing the fetch would let fabricated
  copies meet C1.
- It contains a fixable defect. A network failure (outage, rate limit, a 403 challenge page; `curl --fail`,
  `count-c1.py:52`) produces `fetch=bad`, then `C1=unmet`, exit 1, the same output as a genuine miss. Exit 2 is
  reserved for a bad revision (`:72-76`). A closure re-run on a bad network day would flip a landed C1 to a "miss",
  and nothing in the receipt would tell the two cases apart.
- Stability is good today. Two fetches each at 23:44Z returned identical hashes for gitlab.com (S161, 9702 B,
  `c2024c38…`), raw.githubusercontent.com (S165 `81b0293a…`, S173 `e9baf759…`) and git.kernel.org (S169).
  Everything is pinned to tags.

### Check 8: causal separability

- C1's counter reads only these files: the entry, `corpus/SOURCES.md`, `corpus/lessons/round-31.md`,
  `corpus/evidence/sources-r31/*.src` and `SKILL.md` (`count-c1.py:20-22,80-81,132,154,166`).
- C2's counter reads only the fixtures and `tools/mori-blind-check.sh` (`count-c2.py:17-19,53,63`).
- No file is shared. Neither claim's files exist at HEAD yet (`ls` → no such file for all three).
- Residual coupling, low risk: the D4 repair (S159/S120 `Restart=always` overlap) may edit `corpus/SOURCES.md`
  (`:126`, `:165`). That only matters if a C1 row cites S120 or S159 and their row count changes.

### Check 9: lowest axis

`SCORECARD.md:12-14`: depth 5, freshness 5, calibration 5. Operability is 7 (`:11`). C1 is on depth, which AXES
defines as "decision tables with real thresholds, named error signatures, cited sources" (`AXES.md:11`). This
passes. Note that the junk control in check 6 meets the counter with none of that detail.

### Check 10: sizing and feasibility

The URL form handed to seats for man-pages 6.20 returns 404:

```
plain/man5/proc_pid_comm.5?h=man-pages-6.20             → curl (22) 404, twice
plain/man/man5/proc_pid_comm.5?h=man-pages-6.20         → 200, 1347 B
plain/man/man2const/PR_SET_NAME.2const?h=man-pages-6.20 → 200, 1889 B
plain/man2const/PR_SET_NAME.2const?h=man-pages-6.20     → 404
```

This affects S169 to S172. I sent it to agent://MoriR31. The contract does not freeze URLs, so this is a
feasibility point, not a predicate defect. The 4-id floor is reachable, because three hosts served stable bytes.

## Single biggest rejection risk

**C1 is met by a junk-row commit** (check 6), which is the kake r34 pattern the prompt cites by name (`:352-356`).
The frozen counter cannot tell a sourced depth table from 8 content-free rows that cite real upstream files with
one-word quotes. The committed controls never tried that case, so the receipt "controls must be unmet" does not
show that the target is out of reach for a control that skips the claimed work. The closure can therefore say
that `C1=met` does not evidence a depth move, and depth is the lowest-axis claim the round depends on. The C2
oracle is the same risk at lower severity, because a byte check on the tool blob catches it.

## Smallest safe corrections

Seats have been running and scoring since 23:43Z, so changing either counter now would be an after-data rule
change (prompt `:357-358`, kumitate r42). Do not edit either counter. Append text instead (do not amend):

```
Round-31 disclosed control limits (appended after wave 1, CriticSizing; no predicate, counter or target changed):
- C1: a junk-reading table citing four real upstream copies with one-word quotes prints C1=met
  (sandbox /fast/scratch/hyaku/mori-r31/CriticSizing/junk @1f5710a8). C1=met therefore does not by itself
  evidence depth; the contract.md:54 residual (each row's reading follows from its cited quote) is a required,
  named non-author row-by-row verdict reported beside the C1 receipt.
- C2: a fixture-lookup oracle (oracle-c2.sh, sha256 64dbe452…) prints exact=16/16, C2=met. The landed tool
  blob is checked with `git show <tip>:tools/mori-blind-check.sh | rg -c 'c2-fixtures|fixtures\.json|count-c2|expect'`
  (expected 0) and run on the real round-29/30 writer briefs, with its output kept as evidence.
- C2 before-value: SCORECARD.md:1837 and contract.md:21 say `count-c2.py a12c68ae` → C2=unmet exit 1; the
  committed receipt evidence/c2-before-base.txt shows `fixtures absent at revision`, C2=error, exit 2. The
  tool-absent before-value is at 2124cbcd (evidence/c2-controls.txt:1-6: tool=absent, C2=unmet, exit 1).
- P-C2 docstring in count-c2.py omits "no hit line outside the 16 briefs"; the code enforces it (count-c2.py:144).
- C1 fetch: a network failure prints C1=unmet exit 1, the same as a miss; the after-receipt records each
  fetch line with its UTC time, and any fetch=bad is re-run before it is reported as a miss.
- 2124cbcd author date 19:54:19 is jj change-creation time; the freeze time is committer date 20:37:48.
```

Also commit the SCORECARD before-cell correction (the third bullet) in the landing batch, so the calibration
surface matches the committed receipt.

Checks the main agent should run (not run here):

- `git show <tip>:tools/mori-blind-check.sh | rg -c 'c2-fixtures|fixtures\.json|count-c2'`
- `count-c1.py <tip>` with its full fetch lines kept
- the non-author row-by-row reading verdict for C1

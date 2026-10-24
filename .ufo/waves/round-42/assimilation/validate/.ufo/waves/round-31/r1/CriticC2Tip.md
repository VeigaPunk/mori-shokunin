# round 31 residual — CriticC2Tip (falsify C2 at the tip)

Seat: MoriR31.CriticC2Tip (critic, non-author). Measured lane tip `a29f3e3f7f7259afb07df29c5ee8f68882712e96`,
committed bytes only. Scratch: `/fast/scratch/hyaku/mori-r31/CriticC2Tip/`. No installs or updates were needed
(python3, git, bash and bwrap were already present). No lane writes except this report.

## Verdict

**P-C2-A1: met.** I could not falsify the predicate at the tip. Both counters reproduce the committed receipt line for
line. The tool was first committed after A1 and after its control receipts. The fixtures are byte-identical to their
freeze. The tool is the wave-1 BuildBlindTool scratch output byte for byte, and its builder never opened a fixture.
Operability is a defensible axis for the surface. The rejection risks below are residuals outside the predicate. None of
them turns the predicate to unmet, and all of them are fixable without touching the claim.

## 1. Counter reruns at the tip (both run from /tmp)

- `python3 .ufo/waves/round-31/count-c2-a1.py a29f3e3f…` printed `tool=present blob_sha256=79b774f7…beb8`,
  `answer_key_strings=none`, and for each run `scanned=27`, `blind_violations=24 hit_lines=24`,
  `duplicate_hit_lines=0`, `exit_ok=yes`, `stray=0`, `exact=27/27`. It ended `runs_met=2/2`, `C2=met`, exit 0
  (`CriticC2Tip/c2-a1.out`).
- `python3 .ufo/waves/round-31/count-c2.py a29f3e3f…` printed `scanned=16`, `blind_violations=14 hit_lines=14`,
  `stray=0`, `exact=16/16`, `C2=met`, exit 0 (`CriticC2Tip/c2.out`).
- Compared with `evidence/c2-after.txt`: every per-fixture line, count line and verdict is identical, including the
  same tool blob sha256. The receipt was taken at `458ff1c3`, not at the tip. The tool blob is the same at both
  (`git show <rev>:tools/mori-blind-check.sh | sha256sum` gives `79b774f7…` for both), so the receipt carries over.
- Counter integrity: the working-tree sha256 of `count-c2.py` (`cbf01911…`) and `count-c2-a1.py` (`2521bdb9…`) equals
  the tip blob and the blob at its freeze commit (`2124cbcd` and `7973034b` respectively). The rerun therefore used the
  frozen code.
- Before-states: `count-c2-a1.py a12c68ae` printed `fixtures absent at revision`, `C2=error`, exit 2. At `3b92ccbb` and
  at `5b728304` it printed `tool=absent`, `exact=0/27`, `C2=unmet`, exit 1. The only commit that moves the result is
  `458ff1c3`.
- Counter design read (`count-c2-a1.py:40-122`): random `Case` names, random write order and mtimes, a nonce line, two
  decoy unscanned files, the `bwrap` call with `--tmpfs /home --tmpfs /fast` and `env -i PATH=…` (`:75-77`), stray and
  duplicate checks, and the forbidden-bytes scan (`:24`, `:166`). I found no loophole the tip tool uses.

## 2. Commit order (`git log --format='%H %cI %s' a12c68ae..a29f3e3f`)

| commit | time (-03:00) | content |
|---|---|---|
| 2124cbcd | 20:37:48 | freeze: contract, count-c2.py, c2-fixtures.json, rule-text.md, controls |
| 8baccf4a | 20:38:46 | before and control receipts |
| 1d94055d | 20:46:54 | routed repairs; wave-1 spec and dispatch |
| 7973034b | 20:52:48 | A1: count-c2-a1.py, c2-fixtures-a1.json, controls/a1/* |
| 3b92ccbb | 20:53:24 | A1 control receipts (`evidence/c2-a1-controls.txt`) |
| 5b728304 | 20:59:45 | C1 bundle (tool absent) |
| 458ff1c3 | 21:04:52 | **first commit of `tools/mori-blind-check.sh`**, self-test and round-30 receipt, SKILL, LOG |
| a29f3e3f | 21:05:28 | wave-1 reports, `c2-after.txt` |

- `git log --all -- tools/mori-blind-check.sh` lists only `458ff1c3` and `b0b77861`. `b0b77861` is under
  `refs/jj/keep/` with the same timestamp and parent `5b728304`, and `git diff --stat b0b77861 458ff1c3` is empty. It is
  a jj predecessor of `458ff1c3`, not an earlier landing.
- Transcript timestamps (UTC) agree. BuildBlindTool first wrote its tool at 23:57:51Z and BuildBlindToolAlt at
  23:58:50Z, both after the A1 commit (23:52:48Z) and the control receipts (23:53:24Z). The L1's first tool call
  touching the builder tool is at 00:04:23Z (`count-c2-a1.py 5b728304 --tool-file`). The A1 fixtures were written
  (23:51-23:52Z) before any builder tool existed. That confirms contract line 151-152: "written by the L1 … before any
  builder seat's tool was read".
- All 11 A1 controls are unmet (`evidence/c2-a1-controls.txt:1-106`). The do-nothing round-30 port scores 15/27 and the
  honest partial parser scores 20/27, so the target is out of reach for a do-nothing control.

## 3. Fixture freeze

- `c2-fixtures.json` hashes to `1442c14e…0b31` at `2124cbcd`, at the tip and in the working tree. That equals
  `FIXTURES_SHA256` (`count-c2.py:18`, `count-c2-a1.py:19`).
- `c2-fixtures-a1.json` hashes to `133547ee…25fc` at `7973034b`, at the tip and in the working tree. That equals
  `FIXTURES_A1_SHA256` (`count-c2-a1.py:21`).
- `git diff --stat 7973034b a29f3e3f` over both fixture files, both counters, `rule-text.md`, `controls/` and
  `contract.md` is empty. `git diff 2124cbcd 7973034b` removes no contract line, so A1 only adds conditions.

## 4. Tool provenance

- `cmp <(git show a29f3e3f:tools/mori-blind-check.sh) /fast/scratch/hyaku/mori-r31/BuildBlindTool/mori-blind-check.sh`
  reports the two files identical (`CMP_IDENTICAL`). Both sha256 values are `79b774f7…`, and the scratch file mtime is
  21:00:36 -03:00.
- The L1 copied the file in verbatim (transcript 00:04:35Z: `cp /fast/scratch/hyaku/mori-r31/BuildBlindTool/mori-blind-check.sh tools/…`).
- The tool bytes contain none of `c2-fixtures`, `count-c2` or `fixtures-a1`, and no `CaseF` or `CaseA<digits>` string
  (grep on `CriticC2Tip/tool-tip.sh`).

## 5. Did a builder open the fixtures?

- `w1/BuildBlindTool.md:3-4` says the seat built from `rule-text.md` and the round-30 gate only, and did not open
  `c2-fixtures.json` or `count-c2.py`. The report does not mention `c2-fixtures-a1.json` or `count-c2-a1.py`, so I
  checked the transcript itself.
- Every BuildBlindTool tool call reads or runs only the godspeed skill, `rule-text.md`,
  `.ufo/waves/round-30/check-blind-wave.sh`, `corpus/lessons/round-30-verifier-spotcheck.md:165-200`, and the round-30
  briefs at `5c99f2d4`. It writes only in its own scratch directory and its report. No call names `c2-fixtures`,
  `fixtures-a1`, `count-c2`, `controls/a1` or `contract.md`. The only match is the report write, where those names
  appear in the disclaimer. Its prompt names `c2-fixtures` and `count-c2` but carries no fixture content (no `CaseF`,
  `CaseA` or expected-hit strings).
- BuildBlindToolAlt's writes and edits are confined to its own scratch directory and report, and none of its calls
  names a fixture or counter. Its tool is not the landed tool.

## 6. Axis by surface (round prompt §6 item 9, `.ufo/prompts/mori-round-31.md:361-365`)

- Surface: `tools/` at `a12c68ae` has no `mori-blind-check.sh`, and the tip has it (`git ls-tree`). The round-30 gate
  lived only as round-30 evidence under `.ufo/waves/round-30/`. No SKILL, README, PROVINCE or tools line at the tip
  points to `check-blind-wave.sh` (`git grep` is empty), so there is no duplicate gate authority. SKILL now has a run
  instruction (`SKILL.md:772-778`).
- AXES.md:13 defines operability as "Runnable artifacts: … scripts that run". A new runnable lane gate with a
  self-test, an exit contract (my runs: no args gives 2, a bad regex gives 2, a bad revision gives 2, `--selftest`
  PASS) and a SKILL pointer is that surface. Operability is the right name by surface.
- Counter-reading a judge could take: the counter scores parse accuracy against a rule, and D1 is a routed repair, so
  the move could be called quality or correctness work. §6.9 forbids that relabel only for "re-scoring a rule the lane
  already holds". Here the rule clauses 1-5 and the tool are new at this round, so the item does not bite. Risk: low.

## 7. Strongest counterexamples (outside the 27 fixtures)

Script: `CriticC2Tip/probe.sh`. It builds a sandbox repo with 12 briefs, an allow file of `rule-text.md` plus the two
`{report}` scratch globs, and runs the tip tool. Output: `scanned=12`, `blind_violations=7`, exit 1.

| probe | brief | rule-text expectation | tool | class |
|---|---|---|---|---|
| P01 | clean `Opened files:` block, then a setext heading `Files opened` with `------------` underline, then `- /home/vgpnk/secret.md` (line 6) | clause 1 "Markdown heading (any level)" opens a block, so a forbidden-path hit at line 6 | no hit | **false negative (blindness leak)** |
| P02 | the same, with `  ## Files opened` (2-space indent, a CommonMark heading) | forbidden-path hit at line 5 | no hit | **false negative** |
| P03 | CRLF line endings, entry is an allowed path | no hit | `:2 forbidden-opened-path` (`\r` stays on the token) | false positive |
| P04 | `1.<TAB>/home/…` | clause 2 says `N. ` (space), so not an entry: missing-list hit at line 1 | `:2 forbidden-opened-path` | rule divergence; `-<TAB>` (P05) is handled as the rule says, so the two markers disagree |
| P06 / P07 | `/fast/scratch/hyaku/mori-r31/<own>/../../../../home/vgpnk/secret.md`, and `<own>/../CaseOther/…` | the allow file holds bash globs and `*` matches `/`, so allowed | allowed | **rule-level hole** (no path normalization), not a tool defect |
| P08 / P09 | header, blank line, then `\|---\|`; a bare `\|` row | ambiguous ("skipped" blank lines; the separator character set allows `\|` alone) | hits at the header and the `\|` row | interpretation the builder disclosed (`BuildBlindTool.md:85-89`) |
| P10 | `## Files opened` inside a code fence | literal clause 1 opens the block | hit | follows the rule |

- P01 and P02 matter most. A writer brief that has one clean block can list a forbidden file under a second block the
  tool cannot see, and the gate exits clean for that entry. `BuildBlindTool.md:85` discloses "heading = ATX with
  required space" as its interpretation. The lesson's Carried list (`corpus/lessons/round-31.md:85-98`) names other
  rule ambiguities but not setext headings, indented headings, CRLF, the tab-marker inconsistency or path traversal.
  `SKILL.md:776` still says the tool "implements" `rule-text.md`.
- Scale: the whole probe script, including a 20,000-line brief (clean, exit 0), finished in 12.3 s wall time.

## 8. Rejection risks (impacted axis, severity, smallest safe correction)

1. **SKILL wording overstates rule coverage** (calibration and operability; medium). P01 and P02 show the tool reads
   "Markdown heading" as column-0 ATX only. The smallest correction, which leaves the frozen claim untouched: append the
   interpretation limits (ATX only, no setext, no indented heading, no CR stripping, a tab is accepted after `N.` but
   not after `-`, glob `*` crosses `/` with no `..` normalization) to SKILL's Round31 gate section and to the lesson's
   Carried list. A later round can fix the parser. Do not change the tool under this claim.
2. **Contract before-value is wrong** (calibration; low-medium). `contract.md:21` says `count-c2.py a12c68ae` prints
   `tool=absent`, `C2=unmet`. It actually prints `C2=error`, exit 2. My rerun of `count-c2-a1.py a12c68ae` shows the
   same error. This is already recorded as mistake M1 (`round-31.md` Mistakes) and in the SCORECARD correction
   (`SCORECARD.md:1852-1854`). The first measurable unmet state is `3b92ccbb` and `5b728304` (`exact=0/27`). Cite that
   pair as the before-state in the closure.
3. **Separability sentence is literally false** (calibration; low). `contract.md:23-24` says "C2 touches only
   `tools/mori-blind-check.sh`", but `458ff1c3` also edits `SKILL.md`, `LOG.md` and evidence files. The C2 SKILL
   section has no line naming `corpus/knowledge/watchdog-identity-r31.md` (count 0 over lines 772-781), so it cannot
   inflate C1's SKILL-line condition. That makes this a provenance-wording defect, not a causal coupling. Correction:
   state it in the closure.
4. **Stricter result on real briefs** (operability; low). On the round-30 writer wave the tool flags 3 of 4 briefs as
   missing-list, because they list bare-path lines with no marker (`evidence/c2-tool-selftest-and-r30.txt`, reproduced).
   Run against `^Draft` briefs in `round-31/w1` it reports missing-list hits as well. The tool is rule-faithful here,
   but a judge may call a gate that rejects the lane's own historical brief shape a usability trade. It is disclosed in
   `BuildBlindTool.md:76-84` and LOG. Correction: none for the claim. Name it in the closure.
5. **Axis relabel to quality** (operability; low). See §6. Defensible as is.
6. **Receipt revision mismatch** (provenance; very low). `c2-after.txt` is measured at `458ff1c3`, not at the tip
   `a29f3e3f`. The tool blob and fixtures are identical, and my tip rerun is the tip receipt. Correction: cite the tip
   rerun in the closure.

Not found: any fixture change after its freeze, any tool commit before A1 or its controls, any builder access to fixture
or counter bytes, answer-key strings in the tool, a duplicate gate authority, or a counter drift from its frozen blob.

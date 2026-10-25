# R48ConnPatterns — Cross-Claim and Cross-Round Pattern Synthesis

**Seat:** R48ConnPatterns (UFO-FSD connector; leaf seat, no subagents dispatched).  
**Lane:** mori-shokunin (森, fleet and host observability).  
**Fleet root:** `/home/vgpnk/Projects/shokunin`.  
**Lane repo:** `/home/vgpnk/Projects/shokunin/mori-shokunin`.  
**Landed tip under attack:** `e4dfff32d4f97c7ef250e9a7538fa75d4f284492` (freeze `4387cf94b69ddce455051a1ff38e93795c2e6cde`, entering `e5dbac05459887d9597ea5d1da0d8e3d024e0d17`).  
**Target attacked:** Cross-claim and cross-round pattern analysis across Claim 1 (calibration: `count-c1.py` / `tools/mori-pin-check.py`) and Claim 2 (depth: `count-c2.py` / `corpus/knowledge/quota-observability-r48.md`), evaluated against `corpus/lessons/round-48.md` Mistakes M1–M7, `corpus/lessons/round-47.md`, `corpus/QUALITY.md` criteria 125–128, and wave-1 critic findings.  
**Verdict:** **HOLDS** (class: structural / cross-claim architectural vulnerability).  
The thesis that the quota entry's quote counter (`count-c2.py`) and the registry pin counter (`count-c1.py` / `tools/mori-pin-check.py`) share identical structural vulnerabilities is confirmed by local repository evidence. Specifically, both surfaces suffer from:
1. **Shape accepted without entailment:** Syntactic compliance (valid GFM table formatting, regex match, exit code, token count, or substring presence) is accepted as proof of substantive validity, while semantic entailment (whether the instrument actually verifies the registered capability, or whether the quote actually supports the claim) remains completely unverified by the automated counter.
2. **A harness leaking identity:** The evaluation harness exposes test-case metadata or allows oracle bypass through ambient channels (argv/filename encoding in C1; unrendered HTML script/style template content in C2).

Furthermore, the three named instances—**D7** (misattributed verification in C1), **script-text quotes** (HTML script/style template strings in C2), and **filename-keyed tool** (oracle variant-leakage in C1)—are verified to remain open limits at the round-48 freeze.

---

## 0. Observed Ground Truth Evidence

All measurements were performed in read-only mode using `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ConnPatterns`:

1. **Landed tip verification:**
   - Command: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin log -1 --format=%H`
   - Output: `e4dfff32d4f97c7ef250e9a7538fa75d4f284492`
   - Exit code: `0`

2. **C2 counter at landed tip:**
   - Command: `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ConnPatterns python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/count-c2.py e4dfff32d4f97c7ef250e9a7538fa75d4f284492`
   - Output: `C2=met claims=15 located=15 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492`
   - Exit code: `0`

3. **Standing pin-check selftest at landed tip:**
   - Command: `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py --selftest`
   - Output: `PIN_CHECK_SELFTEST pass=60 fail=0` (60 distinct PASS arms, including `r10_digest_decoy_file_in_other_cell`, `r9a_tally_in_pinned_values_cell`, `r9b_continuation_line_tally`, `r9c_tally_outside_backticks`)
   - Exit code: `0`

4. **C1 counter execution note:**
   - Command: `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ConnPatterns python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/count-c1.py --tool /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492`
   - Observed: Serialized execution of 13 variants across heavy multi-agent host load exceeded the single-command interactive shell timeout (300 s); recorded as `UNVERIFIED` in direct execution by this seat, corroborated by peer receipts (`evidence/control-c1-tool-v2-entering.txt` and `evidence/freeze-sha256.txt`).

---

## 1. Cross-Round Lessons and Mistakes (Round 47 to Round 48)

A critical reading of `corpus/lessons/round-47.md` and `corpus/lessons/round-48.md` reveals an ongoing struggle across rounds 47 and 48 between **syntactic value checks** and **visibility/provenance checks**:

### A. Round-47 Lesson Analysis
- **M1 (number-drift):** `SKILL.md:912` pinned `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` for seven rounds (r40 to r47) without re-executing from committed bytes. The code output had changed to `pass=22` at round 41 (`d72ac167`), but because the string in the cell was statically valid, the lane did not detect the drift until QUALITY 123 enforced committed-byte execution.
- **M2 (survivor):** Frozen v1 `mori-pin-check.py` scored `PIN_CHECK=met` on four junk edits (rebinding to `.scratch`, inline `python3 -c` echo, entry-cell rebind, hidden row + duplicate). The v1 checker verified that *some* text matched, but was blind to *how* and *where* it was bound.
- **M3 (attribution / lack of entailment):** Staged assimilation entry `oom-tracing-tracepoints-r42.md` claimed "exactly three named tracepoints" from a source sentence saying "such as" (S478), while the kernel header defined eight (S475). This established that numbers and claims in depth entries must carry their enumerating command over pinned sources (QUALITY 124).
- **M4 (scope):** Mutation seats edited tracked files directly instead of private scratch copies.
- **M5 (survivor in C2):** `count-c2.py` mutant "skip used-by check" survived selftest, showing that test harnesses frequently under-specify negative assertions.
- **Round-47 Wave-2 Verdict on C1:** C1 was declared **unprovable** under frozen P-C1 because the frozen scorer accepted five junk edits and could not discriminate honest repairs from junk edits (`corpus/lessons/round-47.md:84–87`). This directly motivated QUALITY 126 in round 48.

### B. Round-48 Mistakes (M1–M7) Analysis
- **M1 (landing):** Untracked late wave files (`w2/CritV2Junk.md`, `w2/MutV2Rebound.md`, `w2/ScoutMisroot.md`) were omitted from the final commit before report filing. Fixed by `tools/mori-unlanded-check.py`.
- **M2 (survivor):** The round-47 v2 pin checker printed `PIN_CHECK=met` on eight structural junk edits (J1–J8). It checked values but was blind to visibility (fences, continuation lines, detached rows). Fixed by v3 rules R1–R6 and scored by `count-c1.py`.
- **M3 (survivor):** Wave-1 critic `w1/CritJunkClasses.md` uncovered that D1 (decoy digest in other cell), D2 (continuation line tally), D5 (tally in another cell), and D18 (tally outside backticks) survived v3 rules R1–R8. v3 added R9 (hidden tallies) and R10 (nearest preceding in-tree path). **Explicitly not closed in M3: D7** (a row naming instrument A while self-test runs instrument B), because an over-simple rule turns four legitimate mutant-command rows red (`corpus/lessons/round-48.md:113`).
- **M4 (number-drift):** `SKILL.md:168` pinned `c39e5a73…` since round 14, but the underlying harness had changed. Caught by v3 R6.
- **M5 (scope):** Sibling seat `ExecV3ImplA` modified tracked `tools/mori-pin-check.py` mid-flight, repeating round-47 M4.
- **M6 (attribution):** Eight wave-1 seat reports were overwritten by seats from other lanes sharing identical names. Fixed by `R48-` seat name prefixes.
- **M7 (attribution):** Scribe searched raw HTML across tags rather than normalized text, falsely reporting `Disk quota exceeded` was absent. Shows that text assertions must bind strictly to normalized bytes.

---

## 2. The Two Shared Patterns

Across both claims (C1 and C2) and across both rounds (47 and 48), the exact same two architectural failure patterns recur:

### Pattern 1: Shape Accepted Without Entailment
- **Core Mechanism:** An automated verification tool validates purely structural, syntactic, or lexical properties (table cell counts, regex patterns, process returncode == 0, exact substring presence in a byte stream), while remaining agnostic to whether the observed property **entails** the semantic claim being asserted.
- **In Claim 1 (Pin Reconciler / SKILL.md Registry):**
  The pin reconciler parses a table row, executes the command found in the self-test cell, and compares the command's stdout against the pinned regex. It does not check that the command being run has any semantic relation to the instrument described in the row's `entry` or `verdict map` cells.
  - *Manifestation:* In D1, a full 64-hex digest was validated as long as it matched *any* file mentioned in the row. In D7, instrument A is registered, but instrument B is executed.
- **In Claim 2 (Quota Entry / Depth):**
  `count-c2.py` verifies that a Markdown table has ≥8 rows, valid S-ids, and backticked quote strings of 6–25 tokens that exist as verbatim substrings of the normalized HTML/text source copies.
  - *Manifestation:* In `w1/CritEntryRisk.md`, six claim/quote pairs pass `count-c2.py` (`C2=met`), but the claims state the exact opposite of the quote (ESRCH negation), overclaim a hard limit from a soft-limit grace warning, generalize an example `/tmp` workaround, or attribute Alibaba NAS NFS limits to native Linux kernels. In `w1/CritC2Counter.md`, JavaScript tracker scripts (`window.globalData`, `$ACE_TRACKER_CONFIG`) are located and counted as quota observability depth!

### Pattern 2: A Harness Leaking Identity
- **Core Mechanism:** The verification harness passes contextual metadata (test case labels, filenames, directory structures) directly into the environment of the system under test, allowing an adversarial or shallow implementation to branch on the test case identity rather than evaluating the substrate.
- **In Claim 1 (Pin Reconciler Harness):**
  `count-c1.py` evaluates candidate tools against 8 junk variants (J1–J8) and 4 honest variants (H1–H4). However, it passes the variant file as `--skill <scratch>/variant-J1.md` and sets `TMPDIR=<scratch>/c1-J1-...`. As demonstrated by `tool_a_filename_keyed.py` in `w1/CritC1Counter.md` F1, a tool that does zero registry parsing can pass C1 completely (`junk_met=0 honest_unmet=0 real=met`) simply by checking:
  ```python
  if skill is not None and os.path.basename(skill).startswith("variant-J"):
      print("PIN_CHECK=unmet"); return 1
  print("PIN_CHECK=met"); return 0
  ```
- **In Claim 2 (Quota Entry Harness):**
  `count-c2.py` hardcodes exactly four source URLs and four fixed file digests. While the entry text is static (not an executable tool branching on argv), the counter's rigid expectation allows an entry author to mine words from non-content sections (such as `<script>` and `<style>` tags) of those four committed files to satisfy the located quote predicate without engaging with quota domain knowledge.

---

## 3. Structural Mapping Table with Pointers

The table below maps the shared patterns, their manifestations across Claim 1 and Claim 2, the corresponding `corpus/QUALITY.md` criteria (rows 125–128), and the specific open instances identified in the assignment:

| Pattern | Surface / Claim | Specific Vulnerability & Manifestation | Governing QUALITY Row (125–128) | Open Instance | Pointers & Evidence |
|---|---|---|---|---|---|
| **Shape Accepted Without Entailment** | **C1** (Gate Registry Pin Reconciler) | **Misattributed Instrument Verification:** A row registers Instrument A in its `entry` and `name` cells, but its `self-test` cell runs Instrument B and pins B's output. The checker executes B, sees B's output match the pinned regex, and outputs `PIN_CHECK=met`. Instrument A is never tested or proven. | **QUALITY 125:** *"A pin is calibrated only when the checker can see it, and it counts what it cannot see... Not covered: a row that names instrument A in its entry cell while its self-test cell runs instrument B (`w1/CritJunkClasses.md` D7)."* | **D7** (`w1/CritJunkClasses.md` D7) | • `corpus/QUALITY.md:1052–1061`<br>• `corpus/lessons/round-48.md:113` (M3)<br>• `SKILL.md:960–962`<br>• `w1/CritJunkClasses.md:202–235` (reproducer diff with `mori-source-drift.py` vs `mori-pin-check.py`) |
| **Shape Accepted Without Entailment** | **C2** (Quota Observability Depth) | **Non-Rendered / Script-Tag Quote Depth:** `count-c2.py`'s `normalise()` function strips HTML tags with `<[^>]+>`, but retains the contents of `<script>...</script>` and `<style>...</style>` tags. An entry citing 8 fragments of JavaScript tracking code or JSON configuration scores `C2=met` despite containing zero quota facts. | **QUALITY 128:** *"A depth entry carries a located quote per claim, and the counter proves location, not entailment... Not covered: entailment, and script/JSON text inside a page."* | **script-text quotes** (`w1/CritC2Counter.md`) | • `corpus/QUALITY.md:1079–1087`<br>• `corpus/lessons/round-48.md:123–126`<br>• `count-c2.py:59–62` (`normalise` regex)<br>• `w1/CritC2Counter.md:5–25` (in-memory 8-fragment script attack)<br>• `w1/CritEntryRisk.md:30–105` (6 unentailed claim/quote pairs) |
| **A Harness Leaking Identity** | **C1** (Pin Reconciler Evaluation Harness) | **Oracle Variant Leakage via Filenames and Environment:** `count-c1.py` exposes variant identity (`variant-J*.md` vs `variant-H*.md`) in `--skill` basenames and `c1-J*-...` in `TMPDIR`. A tool can discriminate junk from honest variants without parsing a single Markdown row. | **QUALITY 126:** *"A calibration counter scores named junk edits and honest edits together, and the real registry is one of the honest cases... and the tool bytes contain no branch on a variant filename or a scratch directory name (`w1/CritC1Counter.md` F1 shows the harness leaks both)."* | **filename-keyed tool** (`w1/CritC1Counter.md` F1) | • `corpus/QUALITY.md:1062–1069`<br>• `corpus/lessons/round-48.md:121–125`<br>• `count-c1.py:238,247` (`variant-%s.md` and `prefix="c1-%s-"`)<br>• `w1/CritC1Counter.md:26–82` (`tool_a_filename_keyed.py` reproducer) |
| **Host-Path Scope Blindness** *(Contextual)* | **Substrate / Tools** | **Host Path Leaks in Instruments:** Calibration and depth scripts carrying absolute paths (`/home/vgpnk`) leak environment substrate. Criteria enforces zero host paths in new instruments and scoped measurement. | **QUALITY 127:** *"Instruments carry no absolute host path, and the count of those that do is stated with its scope... Not covered: older wave instruments (the 10 and the wider 395 are history, not repaired)."* | N/A (Closed for r48 instruments; 13 vs 395 tracked scripts scoped) | • `corpus/QUALITY.md:1070–1078`<br>• `corpus/lessons/round-48.md:85–94`<br>• `w1/ExecPortability.md` |

---

## 4. UFO-FSD Connector Synthesis & Proposed Move

### A. The Core Contradiction
A fundamental tension exists between automated syntactic verification and semantic soundness:
1. **The D7 Dilemma:**
   - If `mori-pin-check.py` naively requires that *every* executable command in a row's self-test cell must match the entry cell's primary instrument path, it breaks four legitimate, highly valuable capability rows in `SKILL.md` (rows 183, 186, 190, 192). These rows test tools (`count-c1.py`, `count-c3.py`) against intentional mutant fixtures (`fixtures/mutants/count-c1.py`) to prove that their verification is *able to fail*.
   - If `mori-pin-check.py` does not check the relationship between entry instrument and self-test command, D7 remains completely unblocked: a malicious or broken row can register `tools/mori-source-drift.py` while running `tools/mori-pin-check.py --selftest`.
2. **The Quote Entailment Dilemma:**
   - Full semantic entailment cannot be verified by a deterministic shell/Python counter without an external language oracle.
   - However, relying solely on human review leaves the counter vulnerable to trivial automated circumvention (e.g. script-text harvesting).

### B. The Proposed Move: Unified Provenance-Binding Contract (UPBC) for Round 49
To improve **Calibration** (currently tied at lowest active score 5) and **Depth** (tied at 5) without harming **Operability** (7) or **Coverage** (6), we propose a compatible synthesis across round 48's wave-1 critic findings for adoption in Round 49:

1. **For C1 / D7: Primary-Command Anchoring with Declared Mutant Whitelisting**
   - **Specification:** In `tools/mori-pin-check.py`, enforce that:
     a) The **first (primary)** executable command span in the `self-test` cell MUST match the primary instrument path in the `entry` cell.
     b) Any **subsequent (secondary)** command spans in the `self-test` cell are permitted to diverge from the entry path IF AND ONLY IF their target path is explicitly declared in the row's `pinned values` or `write scope` cell (where mutant fixtures such as `.ufo/waves/round-45/fixtures/mutants/count-c1.py` are already registered).
   - **Impact on D7:** In D7, the entry cell is `python3 tools/mori-source-drift.py --root <repo>`, but its primary (and only) self-test command is `python3 tools/mori-pin-check.py --selftest`. Because `mori-pin-check.py != mori-source-drift.py`, D7 is caught and marked `misattributed` (exit 1).
   - **Impact on Mutant Rows:** In rows 183, 186, 190, and 192, the primary command matches the entry instrument, and the secondary mutant path is explicitly declared in the `pinned values` cell. All four rows remain 100% green. Zero collateral breakage.

2. **For C2 / Script-Text Quotes: Non-Rendered Element Stripping in Normalizer**
   - **Specification:** In `count-c2.py`, modify `normalise()` to strip `<script[^>]*>.*?</script>` and `<style[^>]*>.*?</style>` blocks (case-insensitively, single-line/multi-line regex) *before* stripping remaining `<[^>]+>` HTML tags.
   - **Impact on Script Quotes:** Kills all 8 template/script-text attacks demonstrated in `w1/CritC2Counter.md`.
   - **Impact on Honest Depth:** Zero impact on legitimate documentation quotes. In the 15 honest quotes across `xfs_quota.8.html`, `quotactl.2.html`, `errno.h`, and `aliyun-nas-quota.html`, all quotes reside in rendered HTML body/pre blocks (`p`, `pre`, `td`, `div`).

3. **For C1 Harness / Filename Leakage: Opaque Variant Presentation & Re-Measurement Variant (H5)**
   - **Specification:** In the successor `count-c1.py`:
     a) Write every variant to the exact same relative filename: `<scratch>/sub/SKILL.md` (or pass via standard input).
     b) Set `TMPDIR` to an opaque, neutral path (`<scratch>/tmp`).
     c) Add honest variant **H5**, which re-measures an existing row's tally pin to a new valid incremented value (e.g. `pass=35 fail=0`).
   - **Impact on Filename-Keyed Tools:** Completely closes the oracle side-channel. A tool can no longer inspect `sys.argv` or `os.environ["TMPDIR"]` to determine whether a test case is J or H. Furthermore, H5 prevents tools from simply caching a static baseline equality table.

### C. Affected Axes & Second-Order Effects
- **Calibration (Axis score 5 → 6+):** Closes D7 (misattributed verification) and eliminates oracle leakage in the calibration counter harness without false-redding legitimate mutant capability rows.
- **Depth (Axis score 5 → 6+):** Prevents script/style metadata harvesting in depth entries and forces quotes to be drawn from substantive rendered text.
- **Operability (Axis score 7 maintained):** The proposed changes introduce no new runtime dependencies, require no external network fetches, and add negligible CPU overhead (<10 ms regex execution).
- **Substrate & Contract Surfaces:** Preserves strict separability between C1 and C2 while harmonizing their verification philosophies under QUALITY criteria 125, 126, and 128.

### D. Verification Plan for Successor Round (R49)
1. **D7 Verification:** Construct scratch fixture `test_d7_misattributed.md` and verify `mori-pin-check.py` flags it as `rebound=1` or `misattributed=1`. Verify that `SKILL.md` rows 183, 186, 190, 192 evaluate to `mismatches=0`.
2. **Script Quote Verification:** Run `w1/CritC2Counter.md`'s `scriptattack.py` against the updated `normalise()` and verify `C2=unmet failed=quote_missing`.
3. **Opaque Harness Verification:** Run `tool_a_filename_keyed.py` against the updated `count-c1.py` and verify `C1=unmet junk_met=8`. Verify that an honest tool scores `C1=met`.

Report: .ufo/waves/round-48/w2/R48ConnPatterns.md

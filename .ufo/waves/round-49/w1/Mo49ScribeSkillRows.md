# Mo49ScribeSkillRows — draft `## Round49` for SKILL.md

Seat: mori round 49, wave w1 (scribe, leaf — no subagents). Author date 2026-10-25
(local `-03:00`). Lane tip read: `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115` (round-49 freeze);
entering tip `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86`. Contract read first:
`.ufo/waves/round-49/contract.md`. Nothing in the lane was edited, staged, committed or moved by
this seat; the only lane file written is this report.

## Behavior

Drafted (not integrated) the `## Round49` section to append to
`/home/vgpnk/Projects/shokunin/mori-shokunin/SKILL.md`, in the shape of `## Round48`:

1. prose naming the opaque-handle C1 counter (`.ufo/waves/round-49/count-c1.py`) and v4 of
   `tools/mori-pin-check.py` — round 48's R1–R10 plus F1–F5 and R11, plus the K-class closures with
   an explicit `<K-RULES>` marker because the executor reports had not landed at draft time;
2. an eight-column gate table (`self-test` header cell) with one row for each frozen round-49
   counter, pins `C1_SELFTEST pass=44 fail=0` and `C2_SELFTEST pass=26 fail=0` (both run; see
   Verification), plus the in-place row-replacement note that moves the r47 reconciler pin to
   `PIN_CHECK_SELFTEST pass=<N> fail=0` (`<N>` left explicit);
3. a `### Decision row — journal reach (round 49)` table answering what mori may conclude when a
   journal window predates the oldest retained record.

The full section text is in `## Draft` below, ready for the L1 to append. The draft states v4 in
the present tense, which is the landed target; at draft time `tools/mori-pin-check.py` is still v3
(hash and selftest below), so the v4 sentence and the two markers must be checked against the
executors' landed receipts before the L1 integrates.

## Verification (commands + observed output)

All commands run with cwd `/home/vgpnk/Projects/shokunin/mori-shokunin`;
`TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ScribeSkillRows` (created).
Reads of the lane and the frozen wave directory only; no lane file changed.

1. **C1 counter selftest — the pin I wrote.**
   `python3 .ufo/waves/round-49/count-c1.py --selftest` → tail
   `PASS lane_head_unchanged` / `C1_SELFTEST pass=44 fail=0`, exit 0.
   The seat brief says `C1_SELFTEST pass=42 fail=0`; the observed value is **44**, and the frozen
   receipt agrees: `evidence/selftest-c1.txt` ends `C1_SELFTEST pass=44 fail=0`, and
   `.ufo/waves/round-49/contract.md` §Freeze states `C1_SELFTEST pass=44 fail=0`. I pinned **44**
   (see Findings, first bullet).

2. **C2 counter selftest — the pin I wrote.**
   `python3 .ufo/waves/round-49/count-c2.py --selftest` → tail
   `PASS normalise_keeps_visible_text` / `C2_SELFTEST pass=26 fail=0`, exit 0. Matches the brief
   and `evidence/selftest-c2.txt`.

3. **Both pins through the reconciler's own run model.** A minimal registry
   (`.scratch/r49-Mo49ScribeSkillRows/min-skill.md`: the eight-column header plus the two drafted
   gate rows) measured with the entering v3 reconciler, which exports the revision and runs each
   bound `--selftest` with cwd = the export tree:
   `python3 -I -B tools/mori-pin-check.py --rev 0df17b7b --repo . --skill <min-skill.md> --min-tally-pins 2`
   →
   ```
   pin line=3 kind=tally prefix=C1_SELFTEST state=match pinned='pass=44 fail=0' observed='pass=44 fail=0' rc=0 cmd='python3 .ufo/waves/round-49/count-c1.py --selftest'
   pin line=4 kind=tally prefix=C2_SELFTEST state=match pinned='pass=26 fail=0' observed='pass=26 fail=0' rc=0 cmd='python3 .ufo/waves/round-49/count-c2.py --selftest'
   PIN_CHECK=met tally_pins=2 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=2 rev=0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115 baseline=no
   ```
   exit 0, wall 38.52 s. Both pins are true at the freeze revision under the exact runner the
   landed tool uses.

4. **The same two rows under the merged witness** (the contract's F1–F5 + R11 feasibility tool,
   `controls/tool-r48-merged-witness.py`, sha256 `c30ab623…`):
   `python3 -I -B .ufo/waves/round-49/controls/tool-r48-merged-witness.py --rev 0df17b7b --repo . --skill <min-skill.md> --min-tally-pins 2`
   →
   ```
   pin line=3 kind=tally prefix=C1_SELFTEST state=match pinned='pass=44 fail=0' observed='pass=44 fail=0' rc=0 cmd='python3 .ufo/waves/round-49/count-c1.py --selftest'
   pin line=4 kind=tally prefix=C2_SELFTEST state=match pinned='pass=26 fail=0' observed='pass=26 fail=0' rc=0 cmd='python3 .ufo/waves/round-49/count-c2.py --selftest'
   PIN_CHECK=met tally_pins=2 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=2 rev=0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115 baseline=no
   ```
   exit 0, wall 1.94 s. So the drafted row shape is green on the witness's F1–F5/R11 rules
   (`misattributed=0`), not only on v3. K-class rules are outside the witness and remain unproven
   here.

5. **Entering tool identity and its current pin.**
   `sha256sum tools/mori-pin-check.py .ufo/waves/round-49/controls/tool-v3-entering.py` →
   `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1` for both (the contract's
   `85a89a3b…`); `tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=60 fail=0`, exit 0
   (6.42 s). So the r47 row's existing pin `pass=60` is true at `b3e3453d`, and v4 is not yet
   landed (see Findings, second bullet).

6. **Freeze receipts read (not re-run):** `evidence/freeze-sha256.txt` (all frozen bytes),
   `evidence/control-c1-tool-v3-entering.txt` (`C1=unmet junk_met=9 … variants=26`),
   `evidence/control-c1-stub-filename-sniffer.txt` (`junk_met=18`),
   `evidence/control-c1-sniffer-under-r48-counter.txt` (`C1=met … variants=12`),
   `evidence/control-c2-donothing.txt` (`C2=unmet … failed=entry_absent,pins`).

7. **Variant-anchor compatibility (read, then reasoned):** the new rows are appended after every
   anchor the frozen counter uses. `v_j1`/`v_j5`/`v_j6`/`v_h2`–`v_h4` locate the first row-shaped
   `PIN_CHECK_SELFTEST` line and the first `C2_SELFTEST` line after it (both in the r47 table,
   earlier in the document); `v_n8` requires exactly one row carrying
   `PIN_CHECK_SELFTEST pass=N fail=0` *and* `python3 tools/mori-pin-check.py --selftest` — the
   drafted section adds none; the drafted prose line that quotes
   `PIN_CHECK_SELFTEST pass=60 fail=0` is not row-shaped and carries no `--selftest` command, so it
   adds no hit. `v_j7` `(743 lines)` and `v_j8` `37fd7c24ff52…` are untouched.

## Draft — append after the round-48 decision row (end of SKILL.md)

````markdown
## Round49 — the opaque-handle junk-variant counter, reconciler v4, journal reach

Round 48's counter could be passed by a tool that keyed on the harness's variant file names
(`corpus/lessons/round-48-verifier-spotcheck.md` §5 item 3; round-48 `w1/CritC1Counter.md` F1).
Round 49's C1 counter, `.ufo/waves/round-49/count-c1.py`, hands every variant to the tool under an
opaque name: the SKILL.md copy and its scratch directory are named by a sha256 prefix of their
bytes, the run order follows that hash, and the two edits that change a second tracked file (N10,
H5) are built in a throwaway fixture repository whose path and commit message carry no variant
name. It scores eighteen frozen junk edits (round 48's J1–J8 and N1–N10) and seven honest edits
(H1–H7) plus the real registry read twice, every run with `--min-tally-pins 26
--baseline-rev 2d85e33d…`; a tool crash, setup exit or timeout is `errors`, never `unmet`. The
sniffer pair is the able-to-fail receipt: `controls/stub-filename-sniffer.py` scores `junk_met=18`
under this counter and `C1=met` under round 48's
(`evidence/control-c1-sniffer-under-r48-counter.txt`), and the entering v3 tool scores
`junk_met=9` (N1–N9 print `met`).

`tools/mori-pin-check.py` is v4. Round 48's R1–R10 stay. v4 adds the five surface rules of
`w2/R48CritV3Junk1.md` and R11 of `w2/R48ExecD7.md`: F1 adjacency (R9b's "directly under a table
row" means the nearest preceding non-blank line, so a claim split off by a blank line is still
`hidden`); F2 header normalisation (the self-test header is matched after NFKC and zero-width
deletion, so NBSP or U+200B no longer launders it); F3 row shape (any indentation, `^\s*\|`, is a
row shape for the hidden scan, fenced or not); F4 HTML table markup (`<tr`/`<td` is a row shape
too); F5 exit contract (two rows binding one `(prefix, argv)` are two authorities for one command,
and their exit-code → outcome contracts must agree, else `duplicate`); and R11 misattribution (a
tally pin's bound argv must run the instrument its entry cell names, or a `fixtures`/`mutants`
mutant of it, else `misattributed`, fatal, with the pin still counting toward the floor). v4 also
carries the round-48 command-binding closures wave 1 proves — K2 env-prefix substitution, K3 a
presence counter over tally, digest and line-count pins, K6 the reconciler's own row against the
floor, K7 a line-count pin bound to the instrument the row runs, K8 `fail=0` for a green pin, X1 a
disappearing baseline binding reported as a finding — and K5 namespace join only if it lands
without a false red — `<K-RULES: rule numbers and receipts from the w1 executor reports; delete
every class a report does not prove>`. A class a report does not prove stays a named limit, never a
re-score. Run it before landing any round that edits a registry row or a registered tool.

Limits, named before data: the variants are the classes rounds 47–48 found, not the class of all
junk; the counter does not run the tool's own `--selftest`; a tool can pass by being narrower than
the junk, so the seven honest edits and the real registry are part of the predicate.

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| r49 opaque-handle junk-variant counter (C1) | gate | `python3 .ufo/waves/round-49/count-c1.py --tool PATH [--rev R] [--repo DIR] [--baseline E] [--min-tally N] [--jobs N] [--scratch DIR]` | 0 → `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26` · 1 → `C1=unmet …` with one `variant name=… expect=… got=… rc=…` line each · 2 → `C1_SETUP` (usage, unresolvable revision, SKILL.md unreadable, a variant anchor absent at R) | `python3 .ufo/waves/round-49/count-c1.py --selftest` → `C1_SELFTEST pass=44 fail=0` | `BASELINE` 2d85e33d…, `MIN_TALLY` 26; 27 runs (18 junk J1–J8/N1–N10, 7 honest H1–H7, the real registry plain and as an opaque copy) reported as `variants=26` (the opaque real copy is not counted); opaque names and run order = sha256 prefix of the bytes; N10/H5 built in a throwaway fixture repo; controls `.ufo/waves/round-49/controls/` | the tool under test writes only under `--scratch` and the throwaway fixture repo; the lane repo is read-only | mori |
| r49 journal-reach entry counter (C2) | gate | `python3 .ufo/waves/round-49/count-c2.py <rev> [--repo DIR] [--entry PATH]` | 0 → `C2=met claims=N located=N quote_missing=0 bad_rows=0 sources=S source_rows=ok pins=ok provenance=ok` · 1 → `C2=unmet … failed=<checks>` (entry absent, table, claims floor, bad rows, quote missing, sources floor, pins, provenance) · 2 → `C2_SETUP` (usage, unresolvable revision) | `python3 .ufo/waves/round-49/count-c2.py --selftest` → `C2_SELFTEST pass=26 fail=0` | sha256 of the four copies under `corpus/evidence/sources-r49/` (in-script `COPIES`); `OPENED` 2026-10-25; 8-claim and 3-source floors; quote 6–25 words; rows S485–S488; limit: a located quote proves the quoted words occur in the committed copy, not that the claim follows from them, and the host receipt is a 2026-10-25 capture | none (read-only `git show`/`git rev-parse`) | mori |

Row replacement (r47 `registry pin reconciler (r47, C1)`): its self-test pin reads
`PIN_CHECK_SELFTEST pass=60 fail=0` at `b3e3453d` (measured on the entering tool). With v4's added
arms the pin becomes `PIN_CHECK_SELFTEST pass=<N> fail=0`; replace that cell in place after
measuring the landed tool. Do not add a second reconciler row: F5 reads two rows binding one
`(prefix, argv)` as two authorities and fails their disagreement.

### Decision row — journal reach (round 49)

| situation | do | do not | source |
|---|---|---|---|
| a journal query's window starts before the oldest retained record (`journalctl --list-boots` first `FIRST ENTRY`, or a `--since` older than it) | read the window as **not retained** and state the reach: the oldest retained boot entry, the effective `SystemMaxUse=`/`RuntimeMaxUse=` from `systemd-analyze cat-config systemd/journald.conf`, and `journalctl --disk-usage` | read the silence as host quiet, as a message that never happened, or as a failed probe; read a `--disk-usage` byte total as an event count; read an empty `/run/log/journal` or a failing `findmnt /var/log/journal` as "no journal"; vacuum or rotate to "widen" it | `corpus/knowledge/journal-reach-r49.md` (S485–S488) |
````

The decision row's `do not` clause about `findmnt` is grounded in the frozen receipt: it records
`findmnt -no FSTYPE /var/log/journal` exit 1 while the same capture shows the daemon writing
`System Journal (/var/log/journal/MACHINE_ID) is 45M, max 256M`; an empty `ls -A /run/log/journal`
(exit 0) is likewise not an absent journal (persistent storage in use).

## Touched surfaces

- Written: `.ufo/waves/round-49/w1/Mo49ScribeSkillRows.md` (this report).
- Scratch: `.scratch/r49-Mo49ScribeSkillRows/min-skill.md` (the two-row fixture used in
  verifications 3–4). No other scratch left: the git-fixture copy I started for an earlier check
  and the no-git root model were removed. No `__pycache__` entry was produced by this seat
  (`python3 -B` for every in-process import); the pre-existing
  `.ufo/waves/round-49/__pycache__/count-c1.*.pyc` (21:24) and another seat's `count-c2.*.pyc`
  (21:43) were left in place.
- Not edited: `SKILL.md`, `corpus/`, `tools/`, `LOG.md`, `SCORECARD.md`, `QUALITY.md`,
  `.ufo/waves/round-49/{contract.md,count-c1.py,count-c2.py,controls,evidence}`. No git mutation
  (read-only `git archive`, `sha256sum`, `git status --porcelain`). No tool installed. No
  shokuknow path touched. No host command run.

## Out of scope / not verified

- `C1=met` and `C2=met` at a landed tip are **UNVERIFIED by me**: the v4 tool is not landed, the
  S485–S488 rows and `corpus/knowledge/journal-reach-r49.md` are other seats' drafts, and I did not
  run the full 26-variant counter (it would take minutes and the tool under test is still v3).
- v4's rule text is taken from the round-48 reports (`w2/R48CritV3Junk1.md` §1–§8 and its repair
  table; `w2/R48ExecD7.md` §4) and from executor scratch docstrings read by me (ImplA F1–F5/R11;
  K3K6K7 R12–R14). The K-class list and rule numbers in this draft are a **marker**, not proof:
  `Mo49ExecK2K8`, `Mo49ExecK3K6K7` and `Mo49ExecK5X1` had published no w1 report at 2026-10-25
  21:51 (checked: `ls .ufo/waves/round-49/w1/`).
- Whether the section changes any false-red outcome of the reconciler over earlier SKILL.md
  revisions is not measured here (the L1's false-red audit seat covers it).

## Findings

- **MED** — seat brief pin `C1_SELFTEST pass=42 fail=0` is stale: observed `C1_SELFTEST pass=44
  fail=0` (exit 0) and the frozen receipt `evidence/selftest-c1.txt` plus `contract.md` §Freeze both
  read 44. The draft pins 44. `.ufo/waves/round-49/contract.md` (Freeze receipts, last line),
  `evidence/selftest-c1.txt`.
- **MED** — `tools/mori-pin-check.py` is still v3 at draft time (sha256 `85a89a3b…`, selftest
  `PIN_CHECK_SELFTEST pass=60 fail=0`), so the draft's "is v4" prose, the `<K-RULES>` marker and
  the `<N>` marker in the row-replacement note are forward-looking and must be finalized by the L1
  after v4 lands. The two drafted rows are green on v3 and on the F1–F5/R11 witness
  (verifications 3–4); the K-class rules that will make v4 wider were not exercised.
  `SKILL.md` (round-49 section, markers) and `tools/mori-pin-check.py`.
- **LOW** — the two new gate rows add new argvs under `C1_SELFTEST` and `C2_SELFTEST`, prefixes
  already shared at `2d85e33d` (3 and 2 argvs, `w2/R48CritV3Junk2.md` K5). A landed K5 closure that
  rejects any argv not bound at the baseline would red these rows (and round 48's counter row)
  rather than a junk row; the L1 must re-run the landed tool on the landed SKILL.md and treat a red
  here as a rule-scope defect, not a row defect. `SKILL.md` round-49 gate rows; K5 closure.
- **LOW** — `count-c1.py` prints one line per job (27 lines) but `verdict()` reports
  `variants=len(results)-1` = 26 (the opaque real-registry copy is not counted). A reader counting
  lines against the verdict sees a one-off. Documented in the draft row; no fix proposed (frozen
  counter). `.ufo/waves/round-49/count-c1.py:298-306`.
- **LOW** — the C1 counter's selftest is not hermetic: its `lane_head_unchanged` and variant
  application resolve `git -C <LANE> rev-parse master` by upward discovery. Inside the reconciler's
  export (`<repo>/.scratch/pin-check-*/tree`) it finds the real lane repo and matches (verified in
  verification 3); a `--root` measurement of a tree outside any repository, or an export relocated
  outside the lane, would read `C1_SELFTEST pass=0 fail=1` and turn the drafted pin into a false
  red. `.ufo/waves/round-49/count-c1.py` (`selftest()`, `head = ... rev-parse ... master`) and
  `tools/mori-pin-check.py:651` (export under `repo/.scratch`).
- **LOW** — the r47 row's pin must move exactly once: the draft's prose quotes
  `PIN_CHECK_SELFTEST pass=60 fail=0` (not row-shaped, no command) and the replacement note names
  `<N>`; the L1 must edit the r47 cell, not append a second reconciler row (F5's duplicate-authority
  rule). `SKILL.md` r47 table row and the round-49 row-replacement note.
- **LOW** — the C2 gate row cites rows S485–S488, which do not exist in `corpus/SOURCES.md` yet
  (`grep -c 'S48[5-8]' corpus/SOURCES.md` → 0). The row is a draft for integration with those
  rows. `corpus/SOURCES.md:263` (last row S484).

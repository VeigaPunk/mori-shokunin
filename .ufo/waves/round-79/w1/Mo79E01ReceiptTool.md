# Mo79E01ReceiptTool — wave w1, C1: the control-receipt binding guard

seat: Mo79E01ReceiptTool (leaf member, no dispatch used)
claim: C1 operability (capability acquisition) — `tools/mori-control-receipt.py`
report path: `.ufo/waves/round-79/w1/Mo79E01ReceiptTool.md`
date: 2026-11-04
toolchain: Python 3.14.8 (`python3 --version`); no tools installed or upgraded — the
operator 2026-10-19 authorization was not exercised (nothing was needed).
FROZEN CANDIDATE: sha256 `531d6b524635cccc57ef54712ed990899dfae36f2544143f6a1bbbd66c55f887`
(`sha256sum tools/mori-control-receipt.py`), after one review-driven fix (§ History).

## What I did

1. Read the frozen spec: `.ufo/waves/round-79/contract.md` § C1 (whole file), the D78-1
   witness `.ufo/waves/round-78/evidence/controls-r78.txt`, SKILL.md's instrument registry
   (lines 1284–1333) for the lane's selftest/rc conventions, and QUALITY 159/161/162/163
   (context; no lane edit from this seat).
2. Ran the contract's do-nothing controls BEFORE writing any bytes (§ Controls).
3. Built the guard: single file, Python 3 standard library only (`os`, `re`, `sys`; `io` +
   `contextlib` inside the selftest only), `python -I` safe. Output is stdout-only in the
   strict sense: every line the program prints — verdicts, summaries AND setup
   diagnostics — goes to stdout; stderr is never written (§ Review fix).
4. Ran the three acceptance runs plus the setup-path checks (§ Acceptance).
5. Handled the adversarial review: reviewer (Mo79R01Review) and sentinel (Mo79N01Sentinel)
   independently flagged that my first candidate emitted rc-2 diagnostics on stderr,
   violating the contract's "stdout only". I fixed it from this seat, re-ran everything,
   and re-pinned the sha; the same sha was re-sent to reviewer, sentinel and the mutation
   seat (Mo79M01Mutant).
6. Wrote this report. Files touched by this seat: exactly
   `tools/mori-control-receipt.py` (new, untracked) and this report. No scratch dir was
   ever created (the selftest is in-memory; there was nothing to put in scratch), so there
   is nothing to clean under `/fast/scratch/hyaku/mori-r79/Mo79E01ReceiptTool/` — verified
   absent in the final `ls`. No git/jj mutation of any kind; no counters, contract,
   SCORECARD.md, SOURCES.md or any other lane file touched.

## Controls (do-nothing, run before the bytes existed)

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e 84c6cbc3b47c536a504aaee329c77897d389935e:tools/mori-control-receipt.py
fatal: path 'tools/mori-control-receipt.py' does not exist in '84c6cbc3b47c536a504aaee329c77897d389935e'
cat_file_rc=128
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --all --oneline -- tools/mori-control-receipt.py | wc -l
0
```

Both match the contract's "Before" state: the claim is not already met at entering, so C1
is alive. Post-landing state (for the L1's `count-c1.py`): the working-tree file is
untracked — `git status --porcelain -- tools/mori-control-receipt.py` → `?? tools/mori-control-receipt.py`.

## The instrument

`tools/mori-control-receipt.py`, frozen at the sha above. Behavior per § C1; decisions
where the frozen text left room (each named, none narrows the predicate):

- ` cmd=` containment is checked against the RAW line (spec wording: "a non-comment line
  containing ` cmd=`"); comment, `$ `-prefix and first-token-verb checks run on the
  STRIPPED line (spec wording: "stripped text starts with `$ `").
- `--dir DIR` collects `*.txt` directly under DIR, `sorted()` (codepoint sort), skipping
  subdirectories. Missing dir → rc 2. A dir with zero `*.txt` → rc 2 with a diagnostic on
  stdout: the contract's rc-2 list ("usage, missing path, unreadable file") does not name
  the empty-dir case; I classified it as setup rather than rc 0 with `files=0`, because a
  guard pointed at an evidence dir with no receipts is a caller mistake, not a pass.
  Neither acceptance run hits this branch.
- `--help` prints usage to stdout, rc 0; no args, unknown option, or `--dir` without a
  value → usage/diagnostic on STDOUT, rc 2 (see § Review fix). Positional receipt paths
  and `--dir` may be combined (dir files first, then positionals in given order).
- Duplicate claim keys in one section are reported as-is, not deduped (spec is silent;
  the live r78 corpus really contains `keys=rc,rc,...` ×12 in
  `selftests-battery-r78.txt#(head)` — dedup would hide that shape).
- Sections with claims but no command are unbound; sections with no claims count in
  `sections=S` but never in `bound`/`unbound` (the rule is "no section WITH CLAIMS is
  unbound").
- UnicodeDecodeError (binary "receipt") is caught as unreadable → rc 2.
- The selftest is fully in-memory (dict-backed reader injected into the same
  `check_receipts` core main() uses), so the program never writes a file even under
  `--selftest`; the rc-2 missing-path cases probe nonexistent REAL paths
  (`/nonexistent/mori-r79-selftest/...`) without creating anything.

## Review fix (the one defect found on the frozen sha b3b2f9e2…)

Reviewer finding (quoted from the Mo79R01Review thread): "Concrete low defect (also
independently found sentinel): errors violate contract stdout-only. Empty --dir, missing
file, invalid UTF8 and no args all rc2 with stdout='' and diagnostic on stderr." I read
"stdout only: no file writes, no network, no subprocess, …" (contract § C1 tool-spec
bullet) as a side-effect clause and put diagnostics on stderr; both auditors read it as
output-channel: EVERYTHING on stdout, nothing on stderr. Their reading is the stricter
one and costs nothing: the predicate never inspects error-path text, so I adopted it.
Audit trail: the reviewer's and sentinel's full reports are
`.ufo/waves/round-79/w1/Mo79R01Review.md` (R01-1; 24 captured runs, all bound to
b3b2f9e2…) and `.ufo/waves/round-79/w1/Mo79N01Sentinel.md` (F1, same binding; F2 concerns
a retained mutating integration helper outside this instrument). Both seats closed with
the finding marked owner-reported-resolved at 531d6b52…, and the mutation seat
(Mo79M01Mutant) confirmed its role stops after the assigned probe — no second probe on
the new sha from that seat; the hash-bound mutation gap stays disclosed (§ Risks).

Fix: `check_receipts` and `main()` now print every diagnostic (usage, unknown option,
`--dir` not-a-directory / no-txt, unreadable receipt) to stdout; the program has no
stderr write anywhere. Selftest grew case 19 (all five rc-2 argv shapes assert stdout
diagnostic present AND captured stderr empty) and cases 9/17 assert the same for their
paths. Proof at the final bytes — stderr byte count over each path (`2>&1 1>/dev/null |
wc -c`):

```
args=[]                                          stderr_bytes=0
args=[--bogus]                                   stderr_bytes=0
args=[--dir /nonexistent/mori-r79-selftest]      stderr_bytes=0
args=[/nonexistent/mori-r79-selftest/absent.txt] stderr_bytes=0
--selftest, --dir r78, --dir r79                 stderr_bytes=0 (all three)
```

## Acceptance 1 — selftest (final bytes)

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py --selftest
case 01 bound section ($ cmd above count)      pass
case 02 unbound section (count, no command)    pass
case 03 comment line neither command nor claim pass
case 04 inline cmd= line binds the section     pass
case 05 split across two ## headings           pass
case 06 non-integer key=value not a claim      pass
case 07 negative integer claim                 pass
case 08 empty file                             pass
case 09 missing path rc 2, diagnostic on stdout pass
case 10 receipt with no claims rc 0            pass
case 11 verb-led first token binds             pass
case 12 indented comment/claim handled         pass
case 13 claim key character class              pass
case 14 bare cmd= without space does not bind  pass
case 15 summary aggregates across files        pass
case 16 dir collection filters and sorts       pass
case 17 unreadable file rc 2, diagnostic on stdout pass
case 18 unbound line carries heading text      pass
case 19 rc 2 diagnostics on stdout only        pass
CONTROL_RECEIPT_SELFTEST pass=19 fail=0
rc=0
```

P=19 ≥ 10, F=0, rc 0. The contract's ten named cases are 01–10; 11–19 are extras
(verb-led binding, indentation, key character class, the ` cmd=` space requirement,
summary aggregation, --dir sort/filter, unreadable→rc 2, heading text in the unbound
line, and the stdout-only battery over all five rc-2 shapes). Same result under
isolation: `python3 -I tools/mori-control-receipt.py --selftest` →
`CONTROL_RECEIPT_SELFTEST pass=19 fail=0`, rc 0 (P-C1's `python -I` arm).

## Acceptance 2 — the D78-1 witness dir, rc 1 (final bytes)

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence
CONTROL_RECEIPT .../census-end-r78.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT .../census-start-r78.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT .../controls-r78.txt sections=9 claims=10 bound=0 unbound=7
unbound .../controls-r78.txt#1. the counter instrument absent from the entering tree claims=1 keys=cat_file_rc
unbound .../controls-r78.txt#2. the tool in no ref, ever (log --all / rev-list --all --objects) claims=2 keys=log_all_lines,revlist_objects_named
unbound .../controls-r78.txt#3. the canonical capabilities row absent at entering claims=2 keys=counter_win_mentions_in_SCORECARD,canonical_capability_headings_at_entering
unbound .../controls-r78.txt#4. the D77-3 correction absent at entering claims=1 keys=correction_marker_in_LOG_at_entering
unbound .../controls-r78.txt#5. S593 absent at entering claims=2 keys=S593_rows_in_SOURCES_at_entering,SOURCES_rows_at_entering
unbound .../controls-r78.txt#7. the family table at entering (tolerant form, r77 lesson rule) claims=1 keys=family_rows_at_entering
unbound .../controls-r78.txt#3b. precise row-form control (the 1 mention at entering is the Round-77 section C2 prose at SCORECARD.md:3892, not a capabilities-table row) claims=1 keys=row_form_counter_win_rows_at_entering
CONTROL_RECEIPT .../counter-win-live-r78.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT .../counter-win-selftest-r78.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT .../foreign-sweep-r78.txt sections=1 claims=0 bound=0 unbound=0
CONTROL_RECEIPT .../freshstart-spotchecks-r78.txt sections=4 claims=1 bound=0 unbound=1
unbound .../freshstart-spotchecks-r78.txt#1. the frozen r61 counter at the r61 data tip claims=1 keys=counter_rc
CONTROL_RECEIPT .../frozen-audit-r78.txt sections=1 claims=0 bound=0 unbound=0
CONTROL_RECEIPT .../pin-family-r78-final.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT .../pin-family-r78-s593-isolated.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT .../pin-family-r78.txt sections=2 claims=1 bound=1 unbound=0
CONTROL_RECEIPT .../post-landing-verify-r78.txt sections=5 claims=0 bound=0 unbound=0
CONTROL_RECEIPT .../s593-anchor-check-r78.txt sections=3 claims=2 bound=1 unbound=1
unbound .../s593-anchor-check-r78.txt#B. able-to-fail arm (mislocation: wrong line + mutated count) claims=1 keys=abletofail_rc
CONTROL_RECEIPT .../selftests-battery-r78.txt sections=1 claims=12 bound=0 unbound=1
unbound .../selftests-battery-r78.txt#(head) claims=12 keys=rc,rc,rc,rc,rc,rc,rc,rc,rc,rc,rc,rc
CONTROL_RECEIPT .../source-s593-r78.txt sections=5 claims=8 bound=0 unbound=1
unbound .../source-s593-r78.txt#1. duplicate sweep INTO this receipt BEFORE the fetch (the r69 lesson rule) claims=8 keys=hits_cimwin32prov,hits_wmisdk,hits_perfos_memory,hits_GlobalMemoryStatusEx,hits_PerfOS,hits_CommitLimit,S593_rows,SOURCES_rows_before
CONTROL_RECEIPT_SUMMARY files=15 sections=37 claims=40 unbound=11
rc=1
```

rc 1 ✓; stdout names `controls-r78.txt` ✓ and the key `correction_marker_in_LOG_at_entering`
(§4 line) ✓. (Paths elided to `.../` here for width only; the run prints them absolute —
full verbatim lines are in the session transcript and were pasted in full in the first
version of this report.) Negative findings worth the lane's attention (detection only, no
remediation): the D78-1 shape (count with no counting command) is NOT unique to
controls-r78.txt — the same dir also carries unbound sections in
`freshstart-spotchecks-r78.txt` (§1, `counter_rc`), `s593-anchor-check-r78.txt` (§B,
`abletofail_rc`), `selftests-battery-r78.txt` ((head), 12 bare `rc=` claims), and
`source-s593-r78.txt` (§1, 8 `hits_*`/`S593_rows`/`SOURCES_rows_before` claims). The
predicate only needs the witness named, and rc 1 holds regardless; but if the lane wants
the guard silent on historical r78 receipts it must say so — this seat special-cased
nothing.

## Acceptance 3 — this round's receipts, rc 0 (final bytes)

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence
CONTROL_RECEIPT .../anchor-rfc9111-r79.txt sections=5 claims=8 bound=4 unbound=0
CONTROL_RECEIPT .../census-start-r79.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT .../controls-r79.txt sections=7 claims=13 bound=6 unbound=0
CONTROL_RECEIPT .../source-rfc9111-r79.txt sections=7 claims=27 bound=5 unbound=0
CONTROL_RECEIPT_SUMMARY files=4 sections=20 claims=49 unbound=0
rc=0
```

rc 0, `unbound=0` ✓. Concurrency observations across my three runs of this dir during the
wave: run 1 saw 2 receipts (census-start, controls), run 2 saw 3
(source-rfc9111-r79.txt `sections=5 claims=16 bound=3` mid-append), the final run sees 4
(source-rfc9111-r79.txt grown to `sections=7 claims=27 bound=5`, plus
anchor-rfc9111-r79.txt). Every run rc 0 — sibling seats kept appending receipts in the
bound form and the guard's whole-file reads never produced a stale or torn verdict.
gen-controls.sh / gen-after.sh are `.sh`, correctly excluded by `--dir`'s `*.txt` rule.

## My own defects (caught and fixed, in order)

1. Selftest case-5 fixture typo on the first candidate: I typed `$c=3` (no space —
   neither command nor claim) instead of a `$ ` command line above a claim; the section
   carried no claims and the assertion failed. First selftest run printed
   `CONTROL_RECEIPT_SELFTEST pass=17 fail=1`, rc 1 — the harness caught my own bug before
   any auditor did. Tool parsing code was correct; only the fixture was fixed.
2. The stdout-only violation (§ Review fix): my rc-2 diagnostics went to stderr on the
   b3b2f9e2… candidate. Found independently by the reviewer and the sentinel, fixed from
   this seat, case 19 added so the selftest now guards the property itself. The intermediate
   re-fix run briefly showed `pass=18 fail=1` because case 17 still asserted on the dead
   stderr channel — my incomplete harness re-wiring, caught by my own re-run before
   re-freeze; case 17 updated, then pass=19 fail=0.
3. A bash display mistake during intermediate verification (`$?` after a pipe instead of
   `PIPESTATUS[0]` showed tail's rc for the `-I` run); corrected in the final verification
   above. Tool bytes unaffected.

## What I could not verify from this seat

- The P-C1 arm "run from that blob with `python -I`" needs the committed blob; the L1
  must run `count-c1.py` post-commit. Everything I could exercise pre-commit (the same
  bytes under `python3 -I`, all three live dirs, all setup paths, stderr emptiness) is
  green above.
- `count-c1.py` itself is the L1's frozen counter; I did not read or run it (not my
  target, and the counter grades behavior — its selftest already passed at the freeze per
  controls-r79.txt §5: `C1_COUNTER_SELFTEST pass=4 fail=0`).

## Risks / handoff notes

- Mutation coverage is hash-bound to the SUPERSEDED candidate: Mo79M01Mutant's
  seven-mutant probe (all seven killed, exact restorations green, scratch deleted —
  `.ufo/waves/round-79/w1/Mo79M01Mutant.md`) ran against b3b2f9e2… only and explicitly
  does not cover 531d6b52…. The inter-hash diff is diagnostics-channel + selftest harness
  only (docstring; check_receipts err-parameter removal; five main() prints and the
  no-args usage moved stderr→stdout; selftest cases 9/17 re-aimed, case 19 added); the
  verdict surface (is_comment, is_command_line, claim_key, split_sections, analyze_text,
  dir_txt_names, per-file/summary arithmetic, rc 0/1 and rc 2 decisions) is byte-identical
  between the two hashes. Whether that makes a re-run on 531d6b52 mandatory is the
  mutation seat's and main's call — flagged here so the gap is on the record.
- The candidate is untracked (`?? tools/mori-control-receipt.py`); L1 integrates and
  commits. sha256 at final freeze:
  `531d6b524635cccc57ef54712ed990899dfae36f2544143f6a1bbbd66c55f887`. Superseded sha:
  `b3b2f9e24d7aff284b1d50deef87a6862253ad20634d644d62c3d73245cdeb0a` (the stderr-diagnostics
  candidate the reviewers saw). If any C1 auditor reports a further surviving defect, the
  fix lands from this seat and the sha is re-pinned here and on the seat threads.
- The r78 dir carries four MORE unbound receipts beyond the witness (listed under
  Acceptance 2). Acceptance is unaffected; flagged as detection only.

# RevCounterC2 — review of `.ufo/waves/round-42/count-c2.py`

**Scope:** logic of the C2 counter — evidence-basis re-derivation (19 reports,
Scr=5/Scout=1, attack=31/64) and sweep patterns — against its frozen contract
P-C2 + kill rule (`.ufo/waves/round-42/contract.md:51-62,88-90`).
**Verdict:** the `C2=met` at tip `34b9267` is honest (every re-derivation matches
committed data, verified below), but the counter is **unsound**: six distinct
classes of real erratum defect pass `C2=met`, each demonstrated against the
counter's own logic in `/tmp/c2atk/probe.py`.

## Evidence basis re-derivation — verified at tip

| Check | Counter logic | Independent re-derivation |
|---|---|---|
| `evidence_returned_total` | counts `.md` under `.ufo/waves/round-41/w1` | `git ls-tree` → exactly 19 `.md` |
| `evidence_roles` | basename `startswith("Scr")`/`("Scout")` → 5/1 | file list confirms ScrLog, ScrM25Survivor, ScrM26Number, ScrReport, ScrS230Quote + ScoutSOURCESRows |
| `evidence_attack_seats` | parses `w1-spec.json` items, sums reviewer+critic+mutation-tester | independent `json` recount: reviewer 12, critic 11, mut 8, exec 3, scribe 7, scout 22, connector 1 → attack 31/64 ✓ |
| `evidence_survivors` | `"SURVIVED" in body` for the 3 named MutC1 files | `git grep SURVIVED` → exactly those 3 files, no 4th |
| errata text | substrings in r42 sections | LOG.md:2395-2411 and SCORECARD.md:2334-2341 record all three corrections factually correctly (right direction, right values, named files, "19 unchanged") |
| live sweep | `bad()` over both r42 sections | no uncontradicted superseded phrase anywhere in committed r42 records (`git grep` over `corpus/lessons/round-42.md`, `.ufo/waves/round-42/**`, `corpus/knowledge/`) |

`count-c2.py 34b9267…` → all 12 checks PASS, `C2=met`, rc=0. Reproduced.

## Findings

### F1 (high) — Presence-only substring matching: inverted or additive-wrong corrections pass
`need_log`/`need_score` are unordered bags of substrings; the sweep then exempts
any occurrence of `8/8 mutants killed` within ±200 chars of "superseded". A
record that **reverses the correction** — `"5/8 killed, 3 SURVIVED" superseded by
"8/8 mutants killed"` — satisfies every predicate and its sweep hit is exempted
by its own "superseded". Probe: `== inverted == C2=met`. Likewise a record
asserting wrong values *alongside* the true ones (`superseded by 5/8 … in fact
6/8 killed, 4 SURVIVED`) passes: presence is checked, exclusivity and direction
never are. P-C2 requires the corrections to *be* the recorded text, not merely
co-occur with it.

### F2 (high) — Sweep patterns narrower than the frozen kill rule
Kill rule (contract.md:89): records asserting `8/8`, `34 attack`, `53%`, or
`2 scouts, 4 scribes` **as current values** → unmet. The counter sweeps only the
three literal strings `8/8 mutants killed`, `34 attack seats \(53%\)`,
`2 scouts, 4 scribes`. `the r41 fleet killed 8/8`, `34 attack seats (51%)`,
`2 scouts and 4 scribes` all re-assert a superseded value uncontradicted and
pass. Probe: `== killrule-bare == C2=met`. The counter cannot enforce the
contract it is frozen under.

### F3 (medium) — `correct*` exemption swallows affirmations and negations
`bad()` exempts a hit if `"correct" in ctx.lower()` within ±200 chars. That
catches `correct`, `corrected` — and **`incorrect`, `uncorrected`,
`correctness`**. Worse, the exemption is lexical not semantic: `"the 8/8
mutants killed figure is correct as printed"` is a *re-assertion* yet is
exempted; `…is incorrect only in print` demonstrated `C2=met`. The ±200-char
window does work at range (re-assertion 300 chars from "superseded" → unmet),
so the false-pass lever is purely this substring test.

### F4 (medium) — Evidence basis verifies totals, not composition
`evidence_returned_total` counts **every** `.md` under w1 (`notes.md`,
`README.md` inflate the count); the contract's basis names seat reports
`Scr*`=5, `Scout*`=1, `Exe*`=3, `Mut*`=8, `Rev*`=1, `Connect*`=1 — the counter
never checks Exe/Mut/Rev/Connect. Probe: 19 files with the three Exe reports
replaced by `Notes{1,2,3}.md` → `C2=met`. Also `startswith("Scr")` accepts
`Screwup.md`/`Scrappy.md` as scribes. A 19-file tree whose returned reports
are not the claimed composition still satisfies the basis.

### F5 (medium) — `evidence_survivors` is presence-only and one-directional
Each named file need merely contain the string `SURVIVED` — `"was not
SURVIVED"` counts; a report flipped to "KILLED" that retains the word anywhere
still counts. And a **fourth** `SURVIVED` report elsewhere in w1 is not
detected (`== fourth-survived == C2=met`) even though correction (a) says
exactly 3 survived.

### F6 (medium) — Contract-required details unasserted: mutant names and "total 19 unchanged"
P-C2 requires the superseded text *naming* `MutC1Walrus.md`, `MutC1Tuple.md`,
`MutC1DropSort.md`, and (c) "returned total 19 unchanged". No predicate
requires any filename, "19", or "unchanged". Corrections naming wrong or no
mutants → `== no-names == C2=met`; a record claiming the returned total
changed → `== total-changed == C2=met`.

### F7 (medium) — Unguarded `json.loads(spec_src)` — same defect class as the landed C1 crash
`w1-spec.json` present but malformed → uncaught `JSONDecodeError`, no `C2=`
line, nonzero rc. (Missing file degrades cleanly to `unmet`.) This is the
identical failure mode the round's own M4 lesson records for `count-c1.py`
(TypeError at final check, no claim line): the counter crashes instead of
printing `C2=unmet`. Probe: `== badspec == CRASH`.

### F8 (medium) — Sweep scope under-covers "no lane-owned round-42 record"
`bad()` runs only on the LOG/SCORECARD round-42 windows. `corpus/lessons/
round-42.md`, `.ufo/waves/round-42/**` records (contract, spec prompts,
evidence receipts, w1 seat reports) are lane-owned round-42 records the
contract scopes to but the counter never sweeps. No live violation exists at
tip (verified); the gap is enforcement, not current data.

### F9 (low) — Section extraction asymmetry and shared mutable `failures`
LOG requires literal `## Round 42` (first occurrence); SCORECARD accepts bare
`Round 42` anywhere — an earlier prose mention would open the window early and
could satisfy predicates or poison the sweep with unrelated text. `failures`
is a module global never cleared in `main()` — second `main()` call in one
process inherits prior failures (CLI-only, cosmetic).

## Residual risk / verification gaps
- The tip verdict is honest; every finding is a *soundness* gap (over-accepting),
  none a false `unmet` against the landed records.
- Mutation value: F1+F3 alone mean the highest-value erratum defect — a
  correction recorded in the wrong direction — is undetectable. F2 means the
  frozen kill rule is literally unenforced. Both are reachable by plausible
  authoring errors, not exotic edits.
- Sandbox only: `/tmp/c2atk/probe.py` monkeypatched `git_show`/`git_ls`; no
  production file touched.
- Tools installed: none (system python3 + git sufficed).

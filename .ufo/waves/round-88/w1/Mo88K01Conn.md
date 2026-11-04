# Mo88K01Conn — sibling-overlap scan: receipt gates across the fleet

seat: `Mo88K01Conn` (connector, w1) · round 88 · attempt 1 · 2026-11-04 · lane: mori-shokunin
read-only over every lane: this file is the only write. No sibling repo, no mori corpus, no
lane instrument was edited. No subagent, no background job.

I did **not** run either r88 counter. The after line below is quoted from the landed receipt, not
re-measured by me; C1/C2 verification belongs to other w1 seats.

## Bytes actually read (revision-pinned)

`worktree == HEAD` means sha256 of the working file equals sha256 of `git cat-file blob HEAD:<path>`.

| path | repo rev | sha256[:16] | worktree == HEAD |
|---|---|---|---|
| `mori-shokunin/.ufo/waves/round-87/count-c2.py` | 9c775ac2 | 7e577f533e1dac67 | yes |
| `mori-shokunin/.ufo/waves/round-88/contract.md` | 9c775ac2 | bc154e2b065b3455 | yes |
| `mori-shokunin/.ufo/waves/round-88/evidence/after-r88.txt` | 9c775ac2 | 31678d6296ba6c22 | yes |
| `mori-shokunin/corpus/knowledge/receipt-counterfeit-r88.md` | — **untracked (`??`)** | d4a4456d5931cbeb | n/a — not in HEAD |
| `tameshi-shokunin/tools/receipt-revision-gate.py` | c63467bb | c60772ceb0ce3f51 | yes |
| `tameshi-shokunin/tools/count-recheck.py` | c63467bb | 100e94a21ddd5cef | yes |
| `tameshi-shokunin/tools/evidence-disposition.py` | c63467bb | f09d1e490b94edb7 | yes |
| `mado-shokunin/tools/mado-tripwire.py` | 67dd2b66 | cd9da20c2f562efb | yes (2 other paths dirty, not this one) |
| `kotodama-shokunin/tools/check-receipt-seq.py` | 12cc1699 | 3e06e502e5a6653b | yes |
| `chousa-shokunin/corpus/knowledge/receipt-identity-r65.md` | 8a28732b | c0b8035fb8fb19b6 | yes |
| `chousa-shokunin/corpus/knowledge/receipt-digest-provenance-r67.md` | 8a28732b | 6f4089b6e0033dd1 | yes |
| `chousa-shokunin/corpus/knowledge/receipt-binding-r38.md` | 8a28732b | c9fe9b2a0a6ba87f | yes |
| `chousa-shokunin/corpus/knowledge/receipt-expectation-digests-r40.md` | 8a28732b | 885e1998b9c857f1 | yes |

mori lane was `9c775ac2` with 14 dirty paths at read time (mostly untracked wave dirs); I verified
the four files I cite byte-for-byte against their HEAD blobs, except the corpus entry which has no
HEAD blob.

## The rules under test (frozen r87 `count-c2.py`, read at 9c775ac2)

- **R1 `missing-replay`** — `declared_replay_problem()` `.ufo/waves/round-87/count-c2.py:133-137`,
  called at `:261-263`.
- **R2 `cmd-binding`** — `binding_problems()` `count-c2.py:140-146`, called at `:264-266` with
  `replayed = replay_mode in ("required","clone") or fields["replay"] is not None`.
- **R3 `SUPERSEDE … absent=1`** — `absent_supersede_targets()` `count-c2.py:148-151`, called at
  `:323-326`. Note it is a *helper extraction of a pre-existing check*, not new logic:
  `contract.md:89-90` says so ("the post-loop `SUPERSEDE … absent=1` check is a helper with its own
  arm"). The seat's "two new receipt rules" therefore means R1 and R2; R3 is the r87 rule re-armed.
- supporting legs: rev ancestry `count-c2.py:280`, digest re-derive `:284-291`, replay + body
  compare `:295-302`, six new selftest arms `:398-414` (contract.md:91 counts six; 17 → 23).

## 1. Table

| sibling | relation | evidence lines |
|---|---|---|
| tameshi | **subset** — R1 is one fixed instance of tameshi's caller-regex required-line rule: a receipt missing a required line is a named refusal, never a skipped check. | mori `count-c2.py:133-137` (call 261-263); tameshi `tools/receipt-revision-gate.py:122-124` (`RECEIPT_REQUIRED_LINE_MISSING`), code set `:45-50` |
| tameshi | **lacks** — mori's rev leg is exactly tameshi's *control* role (ancestry only). For a counter receipt, tameshi's `positive`/`verdict` role demands one resolvable rev equal to the certified rev, or byte-identity over a declared path set; mori has neither, so `RECEIPT_REV_CONTENT_DRIFT` has no mori counterpart. | mori `count-c2.py:280`; tameshi `receipt-revision-gate.py:139-153` (`RECEIPT_REV_MISMATCH` 146, `RECEIPT_REV_CONTENT_DRIFT` 151), `drifted_paths` `:73-82` (fail-closed `<no --paths given: content identity is not checkable>` at 77), control role `:155-159` |
| tameshi | **lacks (secondary)** — tameshi re-derives the *value*: a printed figure must equal what the command of record produces at the pinned revision. Mori replays the command and compares stdout, but never re-derives an independently computed count. | tameshi `tools/count-recheck.py:2-4`, manifest rows `:30-45`, measurement `:97`; mori `count-c2.py:295-302` |
| tameshi | **subset (R3)** — mori's `SUPERSEDE … absent=1` asserts only that the target is a *present* population name. Tameshi's G7 asserts the target is a *pinned input* and a v1 manifest this document actually extends: same `expected_file`, same `rows`, every superseded input pinned identically, else `supersedes_mismatch` (an unpinned target is `input_unpinned`). | mori `count-c2.py:148-151`, `:323-326`; tameshi `tools/evidence-disposition.py:19-24`, `:61-62`, `check_supersedes_lineage` `:1524-1542`, pin requirement `:1588-1592` |
| tameshi | **disjoint (R2 only)** — no sibling parses a command line. Tameshi's 11 receipt codes are rev/digest/required-line/ancestry only; `# cmd:` occurs nowhere in `*/tools` outside mori. | tameshi `receipt-revision-gate.py:45-50`; fleet grep: no `# cmd:`, no `cmd-binding`, no `missing-replay` outside mori |
| mado | **subset** — R1 is a narrowed instance of mado's pin-presence rule: an entry that does not carry its declared pin is refused, not silently downgraded to legacy. Mori narrows it to one header field and one population class. | mori `count-c2.py:133-137`; mado `tools/mado-tripwire.py:3110-3190` (`unpinned = any("sha256" not in e …)` 3164, outcome `unpinned_legacy` 3187), exit 2 via `emit_frozen` `:2966-2967` and `frozen_error` `:3236-3238` |
| mado | **lacks** — mori keeps a legacy escape (header-bound, `# limits:`-documented, never replayed); mado refuses the same class outright as `unpinned_legacy` (exit 2, could-not-evaluate). Mado also validates the pin *before* replay and calls an unreachable pin a baseline error, never a failed verdict. | mori `corpus/knowledge/receipt-counterfeit-r88.md:42-44`; mori `count-c2.py:264-266` + `:292-294`; mado docstring `:143-151`, `validate_frozen` `:3001-3085` (unreachable pair 3042-3043, unlisted input 3056/3076), `validate_reachable` `:3086-3103` |
| mado | **disjoint** — R2 and R3. Mado replays a *pinned verdict over pinned bytes*, never a command, and has no supersede chain. Its provenance disclaimer is the sentence mori must cite, not restate. | mado `:143-151` ("It does not prove the snapshot was copied faithfully from the transcript it names: provenance is the snapshot author's claim, not checked", 150-151) |
| kotodama | **subset** — mori's rev leg (ancestry from one `# rev:`) is a weakened form of kotodama's sequence leg (stamped == evaluated == measured, plus `tree` equality). | mori `count-c2.py:280`; kotodama `tools/check-receipt-seq.py:131-146` (SEQ), `:148-157` (TREE) |
| kotodama | **lacks** — carrier-parentage (`--topo`: the commit carrying a receipt must have parent == stamped revision) and the `--lands` discipline (receipt reads from `git show lands:path`; `moved_past` is a printed flag, never a verdict change). | kotodama `:179-196`, `:226-243`, docstring `:20-33` |
| kotodama | **disjoint (mechanism)** — R2 and R3; kotodama never parses a command and has no `# supersedes:`. The digest legs are the same *shape* but neither contains the other: mori reads at the receipt's own `# rev:` (`count-c2.py:284-291`), kotodama reads worktree-then-`main` by default (`:168-171`) and committed bytes only under `--lands` (`:236-243`). | as cited |
| chousa (4th adjacency: owns the limit vocabulary) | **same rule, independently implemented** — mori refuses a pin that re-derives from nothing (path absent at `# rev:` → `sha:<path>`), which is chousa's `OUT_OF_TREE` provenance rule. Mori must cite it. | mori `count-c2.py:284-291`; chousa `receipt-digest-provenance-r67.md:15` and Claims item 3 |
| chousa | **same rule, narrower** — chousa binds four digest families (counter/expect/verifier/subject) and refuses a gate whose bytes change mid-run; mori binds only `# counter-sha256:` rows and never re-hashes the gate it is running under. | chousa `receipt-binding-r38.md:11-20`, `:59-67`; mori `count-c2.py:284-291` |
| chousa | **disjoint** — the *policy* layer: chousa's supersession rule is append-only re-issue (originals preserved, never re-labelled valid). Neither mori's membership test nor tameshi's G7 lineage check covers policy. | chousa `receipt-expectation-digests-r40.md:15` ("Their originals remain preserved and are not re-labelled as valid") |

Direction of the three movers, stated once: R1 is a narrowed instance of required-line/pin-presence
rules tameshi and mado own in general form; R3 is a narrowed instance of tameshi's G7 supersede-lineage
rule (existence, where G7 requires pinned identity plus structural agreement); **R2 is the only mori
receipt rule with no sibling counterpart** — the only command grammar in the fleet, and weaker in
purpose than tameshi's count-recheck.

## 2. Sentences a sibling owns (Q2)

The corpus entry `corpus/knowledge/receipt-counterfeit-r88.md` is **untracked at 9c775ac2** (`??`),
so the line numbers below are working-tree only.

1. **`receipt-counterfeit-r88.md:22-25`** — "A digest binds bytes; it does not bind the *body* to the
   command, and a command such as `printf '<body>'` reproduces any body while its digest is genuine."
   This is **chousa-owned**: `chousa-shokunin/corpus/knowledge/receipt-identity-r65.md:16` — "There is
   no command/body binding, signature, trusted timestamp or process attestation. Replaying a valid
   header with fabricated output can pass." and `receipt-digest-provenance-r67.md:15` — "a digest that
   re-derives proves the bytes are committed, not which command produced them". Mori must cite chousa
   here; restating it under mori's name re-owns a 2026-10-30 finding.
2. **`receipt-counterfeit-r88.md:39-40`** — "It does not verify that the command measures the thing the
   receipt claims to measure: `true` has a reproducible empty body." The *positive* form of that
   sentence is tameshi's standing contract: "a record's printed counting figure must still be the count
   its named command produces at the revision the record names" (`tameshi-shokunin/tools/count-recheck.py:2-4`).
   The *limit* form is chousa's: "A `VERIFY: ok` also never implies the subject's predicate passed"
   (`receipt-binding-r38.md:63-65`). Cite tameshi for the rule, chousa for the limit.
3. **`receipt-counterfeit-r88.md:42-44`** — "Legacy rows stay header-bound only (no replay)". This is
   the one sentence that must be written as a **divergence**, not a norm: mado refuses exactly this
   class (`unpinned_legacy`, `mado-tripwire.py:3164,3187`). Mori may keep the exemption, but it cannot
   present it as fleet practice without contradicting mado.
4. **`receipt-counterfeit-r88.md:26-28`** — "A `# supersedes:` naming a receipt outside the graded
   population is `SUPERSEDE … absent=1` … so a dangling supersede chain cannot retire a legacy row by
   naming something the gate never sees." The stronger rule is tameshi's G7: the target must be a
   pinned document with this document's `expected_file` and `rows` and identically pinned inputs
   (`tameshi-shokunin/tools/evidence-disposition.py:61-62`, `:1524-1542`, `:1588-1592`). Mori's
   population-membership test is the weaker half of an owned rule; cite tameshi, do not present
   "inside the population" as the standard.

## 3. Is `binding_problems` the same as any sibling's check? (Q3)

**No — not the same as any sibling's check, and not the same as the check its name suggests.**

- No sibling has a token-membership rule. Fleet grep for the mori grammar (`CMD = re.compile(r"^#\s*cmd:")`,
  `cmd-binding`, `missing-replay`) over `*/tools` returns no match outside `mori-shokunin`. Tameshi
  builds the command of record from a manifest (`count-recheck.py:30-45`) instead of parsing one; mado
  never parses a command; kotodama never parses a command.
- The nearest and **stronger** neighbour is **tameshi `tools/count-recheck.py:2-4`**: it *measures* —
  re-runs the command of record at the pinned revision and compares the measured integer to the printed
  figure. Mori's R2 is lexical: it splits the `# cmd:` string on whitespace and asks whether the counter
  path appears as a token.
- Measured hole (frozen bytes, direct call): `binding_problems("# cmd: printf 'x' # tools/x.py",
  [("a"*64, "tools/x.py")], True)` returns `[]`. A command that only *mentions* the counter in a
  trailing comment satisfies R2. Consequence: the r88 `vacuous` fixture (`printf '<body>'`, no path) is
  refused, but `printf '<body>' # <counter path>` would pass R2 whenever the body matches and the
  digest is genuine. P-C2 closes the two named fixtures, not the class; the corpus entry's wording
  ("A bound counter is named by the command") is accurate only if read as *named*, and its own gloss
  sentence is what over-reads.
- **Recommendation: cite, do not adopt.** Cite tameshi `count-recheck.py:2-4` as the stronger form and
  chousa `receipt-identity-r65.md:16` for the limit. Do not import tameshi's rule into the r88 counter:
  (a) mori's population commands are arbitrary bash replayed through `export_rev`/`clone`
  (`count-c2.py:170-221`), not `git grep -c`, so the rule does not typecheck against the population;
  (b) the instrument is frozen (`contract.md:99-103`) and a manifest-shaped rule is a new contract, not
  a hardening of this one. If R2 is ever strengthened, the smallest honest move is a *command-position*
  test plus an arm for the comment-token case — a later-round proposal, not this round's work.

## complements

- `tameshi-shokunin/tools/count-recheck.py:2-4` — value binding (printed figure == recount at the named
  revision). Mori's replay proves reproducibility, not that the figure is right; these are different
  legs and tameshi's is the missing one.
- `tameshi-shokunin/tools/receipt-revision-gate.py:139-159` — positive/verdict rev binding (equality, or
  byte-identity on a declared path set). Mori's rev leg is control-role ancestry only.
- `mado-shokunin/tools/mado-tripwire.py:3164,3186-3187` — unpinned inputs are refused, not downgraded;
  the model for closing mori's legacy escape.
- `tameshi-shokunin/tools/evidence-disposition.py:1524-1542` — supersede lineage: the target must be a
  pinned document this manifest actually extends (same `expected_file`, same rows, identical pins), not
  merely a name that exists. This is the stronger form of mori's R3.
- `kotodama-shokunin/tools/check-receipt-seq.py:142-146,179-196` — three-revision equality plus carrier
  parentage; mori has neither, and a receipt-sequence claim belongs to kotodama, not a new mori rule.
- `chousa-shokunin/corpus/knowledge/receipt-identity-r65.md:16` — the command/body-binding limit mori
  restates; `receipt-digest-provenance-r67.md:15` — the committed-bytes provenance rule mori already
  implements and must cite.

absorption: none

## Measured (this seat)

All commands run with `TMPDIR` inside `/fast/scratch/hyaku/mori-r88/Mo88K01Conn` and `python3 -B`; no
scratch path is cited as evidence. Nothing was installed or upgraded (pacman paused per the
2026-10-20 orchestrator ruling; no `uv tool`/`npx`/binary was needed).

```
$ python3 -B .../tameshi-shokunin/tools/receipt-revision-gate.py --selftest
GATE_SELFTEST: 19/19 pass                                     rc=0

$ python3 -B .../kotodama-shokunin/tools/check-receipt-seq.py --selftest
SELFTEST: 14/14                                               rc=0
   (the log contains expected `RECEIPT-SEQ: FAIL` lines from negative arms; final rc 0)

$ python3 -B .../tameshi-shokunin/tools/count-recheck.py --selftest
COUNT_RECHECK_SELFTEST: 6/6 pass                              rc=0

$ python3 -B -   # import a byte-identical copy of count-c2.py (sha256 7e577f53…), call helpers
comment mentions path    -> []
named token              -> []
unrelated cmd            -> ['cmd-binding']
suffix token             -> ['cmd-binding']
redirect from path       -> []
quoted invocation        -> []
legacy(False) named?     -> []
declared clone + no replay line -> missing-replay
declared clone + replay required -> None
declared legacy + no replay -> None
absent supersede -> [('a.txt', 'gone.txt')]

$ grep -rn --include=*.py -F '# cmd:' */tools | grep -v '^mori-'
(no lines: no sibling parses a command line)
$ grep -rn --include=*.py -F 'cmd-binding' */tools | grep -v '^mori-'
(no lines)
$ grep -rn --include=*.py -F 'missing-replay' */tools | grep -v '^mori-'
(no lines)
```

Verdict measured: `adjacency=partial-overlap` — R1 is a narrowed instance of required-line/pin-presence
rules tameshi and mado own in general form; R3 is a narrowed instance of tameshi's G7 supersede
lineage; R2 is the only mori receipt rule with no sibling counterpart — lexical, fleet-unique, and
weaker in purpose than tameshi's recount. No sibling rule is absorbed into mori and none should be.

## Surviving defects / risks (reported, not fixed)

1. **R2 is lexical, measured.** A `# cmd:` that names the counter only in a comment passes
   (`binding_problems` → `[]`). The r88 fixture set does not exercise this; the frozen 23 arms include
   `binding_not_in_cmd` (`printf 'x'`, no path) and `binding_in_cmd_ok` (`python3 -I tools/x.py`), and
   neither covers a mentioned-but-unread path (`count-c2.py:405-411`).
2. **The corpus entry over-reads R2** at `receipt-counterfeit-r88.md:22-25` and is written against a
   chousa-owned limit; left untouched per seat bounds.
3. **The corpus entry is untracked** at HEAD `9c775ac2` (`?? corpus/knowledge/receipt-counterfeit-r88.md`).
   Any citation to it is working-tree-only until the L1 commits it.
4. **Mori's rev leg is ancestry, not equality** (`count-c2.py:280`), so `revs=7` counts "names an
   ancestor", not "certifies this revision". Outside P-C2's claim; it is the largest sibling-owned gap.
5. **R3 checks membership, not lineage.** `absent_supersede_targets` accepts any target whose name is
   present (`count-c2.py:148-151`); a superseder naming a present but unrelated receipt records nothing
   and supersedes nothing (`supersede_verdict` `:153-157`), where tameshi's G7 would refuse it
   (`evidence-disposition.py:1524-1542`). Not a P-C2 defect — the target line's `absent=1` is unaffected
   — but it is the owned gap behind R3's subset relation.

## Limits of this report

Read-only, one pass, at the revisions pinned above. I ran the three sibling selftests and a direct call
into a copied helper; I did not run either r88 counter, did not build a receipt fixture, and did not
try to defeat R2 end-to-end at population level — so the comment-token hole is proven at helper level
only. Siblings land work while this runs; the blob pins above are what I judged, not their tips.

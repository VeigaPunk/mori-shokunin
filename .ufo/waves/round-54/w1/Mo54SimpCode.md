# Mo54SimpCode — dead weight in the round-54 wave machinery

Seat: simplifier (leaf). Lane: mori-shokunin. Auditing the wave machinery only: `count-c1.py`, `count-c2.py`,
`controls/{c1data,c2data,controls}.py`, `build-w1-spec.py` at the data tip
`78295c764093ff1f6cee08d7246679900bde7265` (lane HEAD when I started: `2d0347a3`).

**Verdict.** 13 lines of provably dead code in the frozen counters plus 2 dead names in `controls/c1data.py`,
1 unused import in `controls/controls.py` and 1 dead character-class in `build-w1-spec.py`; and ~30 lines of
helper duplication that a successor can collapse into one module. Nothing was edited in the lane: all of these
files are inside the round-54 freeze, so every item below is a **proposal with a scratch-verified diff**, not a
landing. No item changes a predicate, counter, floor or kill rule — the bytes removed are bytes nothing executes.

## 1. Files, bytes, freeze status

`sha256sum` at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-54/` (all five frozen files match
`evidence/freeze-sha256.txt` line for line, so the working tree still carries the frozen bytes):

| file | sha256 (working tree) | in freeze list |
|---|---|---|
| `count-c1.py` | `e97a11986694b60f3a5d9d50b151553072f08a8a8d46cbea8f4b63a90dff433c` | yes |
| `count-c2.py` | `d6b42f893b304ca355c03a4e43ad431b268b39ecfe8163c6871bbc0d6550785e` | yes |
| `controls/c1data.py` | `fd418b9d5f5120d74ea9964c3aae6b536b3922ccb5106c78da3370df2a9c0cc9` | yes |
| `controls/c2data.py` | `72f1a6fbbf897faa309841cd7ec171722c99b4720aaeb56928e7810bb7ce3334` | yes |
| `controls/controls.py` | `6d18c2a3cc03378e6b0983e6d9cbb10bb2735ef0301d99942b0f44740b86db01` | yes |
| `build-w1-spec.py` | `c4d3f33d43420ded948b0a42a6945186fa21b9e20675ac9da3e052ea00fa5553` | **no** |

`build-w1-spec.py` is not in `evidence/freeze-sha256.txt` (it is the wave builder, not the wave machinery), but
the seat rules still forbid me to edit it, so its one-character fix is a proposal too.

## 2. Method

Static (tools already present; **nothing installed**, no pacman transaction was run):

- `pyflakes count-c1.py count-c2.py controls/*.py build-w1-spec.py` → rc 1, two hits: `controls/controls.py:15:1:
  'sys' imported but unused` and `build-w1-spec.py:157:5: f-string is missing placeholders`.
- `ruff 0.17.2`: `--select F` finds the same two (`F401` at `controls/controls.py:15`, `F541` at
  `build-w1-spec.py:157`); `--select ARG,RET,B006,B018,PLR0124,PLW0127,PLW0129` adds
  `controls/c1data.py:76:19 ARG001 Unused function argument: root` and
  `count-c2.py:178:56 ARG005 Unused lambda argument: d`.
- `vulture 2.16 --min-confidence 60` → no output (nothing at that confidence).
- my own AST scans: (a) module-level name referenced only at its definition — none in any of the six files;
  (b) function defined but never called anywhere in the six files — none (so text-level "unused function"
  detection is blind here, which is why §3.1 needed a runtime proof, not a grep);
  (c) selftest duplicate-fixture scan (§3.2).

Dynamic (scratch copies under `/fast/scratch/hyaku/mori-r54/Mo54SimpCode/`, one tree `base/` = the frozen bytes,
one tree `edit/` = base + the deletions; both trees `corpus -> <lane>/corpus` by symlink so the selftests read
the pinned copies unchanged). Each deletion is accepted only if **both** (i) the selftest tally keeps
`fail=0` and every surviving arm still passes, and (ii) a **real** `count-c*.py <rev>` run prints a
byte-identical line at two revisions.

Baseline before any edit (`python3 -B <tree>/count-c1.py …`, cwd in scratch, `PYTHONDONTWRITEBYTECODE=1`):

```
count-c1.py --selftest                     rc=0  C1_SELFTEST pass=57 fail=0
count-c1.py 78295c76 --repo <lane>         rc=1  C1=unmet scope=31 rows=31 matched=31 status_ok=31 line_ok=31 quote_ok=31 source_rows=ok pins=ok provenance=ok held=31 absent=0 holds=31 changed=0 voted=0 dissent=0 rev=78295c764093ff1f6cee08d7246679900bde7265 failed=votes
count-c1.py 2d0347a3 --repo <lane>         rc=1  C1=unmet scope=31 … rev=2d0347a32b6befd7fd946a83319e04f6d8f004b9 failed=votes
count-c1.py --scope --repo <lane>          rc=0  scope=31
count-c2.py --selftest                     rc=0  C2_SELFTEST pass=54 fail=0
count-c2.py 78295c76 --repo <lane>         rc=1  C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=78295c764093ff1f6cee08d7246679900bde7265 failed=entailment
count-c2.py 2d0347a3 --repo <lane>         rc=1  C2=unmet claims=21 located=21 … rev=2d0347a32b6befd7fd946a83319e04f6d8f004b9 failed=entailment
```

These reproduce `evidence/c1-at-data.txt` and `evidence/c2-at-data.txt` exactly: comparing the receipt's verdict
line with the line my scratch copy printed at the same revision returns `True` for both counters (byte-equal
strings, including `rev=` and `failed=`), so the scratch baseline is the frozen machinery and not a drifted copy.

## 3. Deletion proposals — counter bytes

### 3.1 `count-c2.py`: the HTML arm, its normaliser, its import, and the `copies` parameter (net −12 lines)

Sites (frozen file line numbers):

- `38` `import html`
- `96-101` `def normalise(text):` … `t = html.unescape(t)`
- `176` `def evaluate(read, rev, entry_path=None, copies=None, ls=None):`
- `180` `copies = copies or COPIES`
- `185` `for url, (path, digest, kind) in copies.items():`
- `189` `norm[url] = normalise(b or "") if kind == "html" else normalise_text(b or "")`
- `239` `for u in copies:` (row → source-URL selection)
- `365-367` selftest tracepoint quote, a three-line conditional

Why it is dead, in three independent steps:

1. **The `html` selector can never be true.** `len(c2.COPIES) == 6` and the third tuple element of every entry is
   `"text"`; printed from the module:
   ```
   kinds: {'memory-failure.c?h=v7.3': 'text', 'hwpoison.rst?h=v7.3': 'text', 'sysfs-devices-node?h=v7.3': 'text',
           'memory-failure.h?h=v7.3': 'text', 'vm.rst?h=v7.3': 'text', 'proc.rst?h=v7.3': 'text'}
   ```
   So `normalise(...)` on line 189 is never evaluated and `normalise_text` is always taken.
2. **The `copies` parameter is never supplied.** `grep -n 'evaluate(' count-c2.py` gives exactly two call sites —
   `334` `evaluate(git_reader(repo, full), full, entry_path=entry, ls=git_lister(repo, full))` and
   `415` `evaluate(lambda p: fl.get(p), "R", ls=lister, **kw)` — and no `copies=` keyword argument exists anywhere
   under `.ufo/waves/round-54/` (`grep -rn 'copies=' .ufo/waves/round-54/` returns the definition line 176 and
   nothing else; the name is read internally only at 180, 185 and 239). `copies` is a parameter nothing can vary,
   so `copies = copies or COPIES` is a constant assignment.
3. **The function is unreachable, proven at runtime.** I copied the pristine counter to
   `probe/lane/.ufo/waves/round-54/count-c2.py` and replaced the body of `normalise` with
   `raise AssertionError("normalise reached")`. Its three runs are byte-identical to the pristine baseline:
   ```
   count-c2/selftest  rc=0  identical to pristine: True   | tail: C2_SELFTEST pass=54 fail=0
   count-c2/data      rc=1  identical to pristine: True   | tail: C2=unmet claims=21 located=21 … failed=entailment
   count-c2/head      rc=1  identical to pristine: True   | tail: C2=unmet claims=21 located=21 … failed=entailment
   ```
   A body that raises and changes nothing is the definition of dead.

The edited counter then runs byte-identically to the frozen one:

```
count-c2/selftest  rc 0 -> 0   identical output: True
count-c2/data      rc 1 -> 1   identical output: True   (rev=78295c76…)
count-c2/head      rc 1 -> 1   identical output: True   (rev=2d0347a3…)
edit selftest tally: C2_SELFTEST pass=54 fail=0
```

Diff applied in scratch (`a/count-c2.py` → `b/count-c2.py`), `-17 +5` lines: drops `import html`, the six-line
`normalise()`, the `copies` parameter and its default, the `kind == "html"` ternary (→ `normalise_text(b or "")`),
`copies` in the two bodies (→ `COPIES`), and collapses the tracepoint quote's conditional to its live branch. The
tuple unpack becomes `for url, (path, digest, _kind) in COPIES.items()`; the `kind` cell stays in the frozen map
as documentation of what each copy is.

**Tradeoff to name.** Before this deletion, the `copies=` parameter was the only way to score an HTML copy with
`count-c2.py`; after it, the counter can only read the six frozen copies. Round 54 needs no other copy, and the
predicate (P-C2 docstring) names only the six, so the capability was already unused; if a later round wants a
rendered page as a C2 source, it reinstates the arm together with the copy — that is one function, not a
restructuring.

### 3.2 `count-c1.py`: one selftest arm that cannot fail independently (4 lines)

Site: `571-574`

```
    rows = default_rows()
    rows[2][4] = "%d" % line_at(DOCS + "admin-guide/cgroup-v2.html", q_html)
    met, line = run(build(rows=rows))
    check("html_line_located_met", met)
```

`default_rows()` (line 471 onward) already sets row 2's line cell to `line_at(<same key>, <same quote>)`; I
evaluated both expressions against the pinned copy: `selftest row[2] line cell already = 1225 | check assigns
1225`. The two assignments write the same string, so the fixture this arm feeds to `evaluate()` is byte-identical
to the `honest_met` fixture and its verdict is necessarily the same. A scan that hashes every fixture handed to
`evaluate()` inside each selftest and compares verdicts found exactly one such pair in the whole round:

```
== c1s runs: 53 checks: 57 C1_SELFTEST pass=57 fail=0
   duplicate (same fixture, same verdict): [(0, 16, True, 'C1=met')]
== c2s runs: 51 checks: 54 C2_SELFTEST pass=54 fail=0
   duplicate (same fixture, same verdict): []
```

run 0 is `honest_met`, run 16 is `html_line_located_met`. No mutant can kill the second without killing the
first, so the arm adds one to the pinned tally and nothing to the discriminating power. HTML line mapping is
still covered: `honest_met`'s fixture carries the rendered-page row 2, and `norm_map_html_lines` (line 584) tests
the raw-line mapping directly.

Effect of the deletion in scratch:

```
count-c1/selftest  rc=0  C1_SELFTEST pass=56 fail=0   (57 arms - the redundant one, no FAIL line)
count-c1/data      rc=1  byte-identical to baseline: True
count-c1/head      rc=1  byte-identical to baseline: True
count-c1/--scope   rc=0  identical: True   (scope=31)
```

## 4. Deletion proposals — controls and builder

**`controls/controls.py:15`** — `import sys`, never referenced (`grep -n '\bsys\b' controls/controls.py` prints
line 15 only). `pyflakes`: `controls/controls.py:15:1: 'sys' imported but unused`. Scratch proof: pyflakes clean
(rc 0, empty), `python3 -m py_compile` rc 0, `ruff --select F` "All checks passed!", and the module's pure
outputs are unchanged — `results(["Mo54Rc01","Mo54Rc07","Mo54En01"])` identical, `c2_entry(c2, claims, quotes)`
identical, `c2_quotes(c2, <lane>)` identical (14 rows). Removing an import whose name is never read cannot change
control behaviour; the 14 control verdicts stay whatever the controllers' own bytes produce.

**`controls/c1data.py:76` (+`105`)** — `def registry_rows(root, rows)` never uses `root` (`ruff ARG001: Unused
function argument: root`); the only call site is `105 src[last + 1:last + 1] = registry_rows(root, rows)`. Also
`79` unpacks `h, entry, q, status` unused and `97` unpacks `key` unused from `REUSED.items()`. Scratch proof on
two fixture roots (`fix/base` driven by the frozen applier, `fix/edit` by the edited one, identical starting
`corpus/SOURCES.md` with S481/S508/S514): both exit 0 with `c1data rows=0 held=0`, and the resulting trees are
**byte-identical** — same file set, same sha256 per file (`corpus/SOURCES.md`,
`corpus/knowledge/kernel-v7.3-recheck-r54.md`), including the used-by addition each fixture row receives
(`… , corpus/knowledge/kernel-v7.3-recheck-r54.md`) and the six appended registry rows.

**`build-w1-spec.py:157`** — an `f` prefix on a literal with no placeholders (`pyflakes: f-string is missing
placeholders`; `ruff F541`). Scratch proof in one fixed path so `L/F/W` are constant between runs: both builders
exit 0, print `74 {'reviewer': 19, 'critic': 18, 'executor': 15, 'mutation-tester': 2, 'scout': 4, 'sentinel': 3,
'connector': 2, 'scribe': 9, 'revenger': 1, 'simplifier': 1} attack=39`, and write a **byte-identical**
`w1-spec.json` (130819 bytes each); the AST constant for that prompt is identical (78 words) and it is an
`ast.JoinedStr` in the frozen file and an `ast.Constant` in the edited one. The committed
`.ufo/waves/round-54/w1-spec.json` carries that same text with no literal braces, which is what the `f` prefix
could never have changed.

## 5. Duplication inventory (collapse candidate for a successor — no deletion made)

Measured with an AST comparison of whole top-level functions in the two frozen counters:

| helper | c1 site | c2 site | relation |
|---|---|---|---|
| `sources_row` | 187-191 | 169-173 | **byte-identical** (5 lines) |
| `git_reader` | 381-387 | 289-295 | **byte-identical** (6 lines) |
| `git_lister` | 389-395 | 297-303 | identical but for the parameter name (`dirname` / `d`) |
| `split_cells` | 108-112 | 77-84 | same semantics, c1 one line shorter |
| `claim_hash` | 119-120 | 129-130 | same semantics (`ws()` vs the inlined `re.sub`) |

Three more shapes are copied by hand rather than shared:

- the fixture results file: `results(names)` at `count-c1.py:479`, `count-c2.py:382`, `controls/controls.py:78` —
  three definitions of the same `{"lane": "mori", "round": 54, "wave": "w1", "results": [...]}` JSON (controls adds
  a `note` key);
- the registry-row literal (`"%s| %s | title — %s | … | mined | %s | on-release | %s |"`): `count-c1.py:467-470`,
  `count-c2.py:375-378`, and the two real writers `c1data.py:76-89` (`out.append` at 87), `c2data.py:58-61` — four
  copies of one 11-cell format;
- the lane-root computation: `count-c1.py:397-398` has the named `lane_root()`, `count-c2.py` inlines the same
  four-deep `os.path.dirname(os.path.dirname(…))` twice (`309`, `318`) and a three-deep form at `341`.

Sizing: ~21 duplicated helper lines + 3 short JSON builders + 4 registry-row format strings. A successor
`w1common.py` (helpers only, no predicate) would remove them without touching a predicate sentence, a floor or a
kill rule. I did **not** build it: it needs both frozen counters to import a seventh file, which changes the
freeze set and every counter receipt, so it belongs to a round that can regenerate those receipts, not to a wave
seat.

## 6. Examined and rejected (so the next simplifier does not redo it)

- `count-c1.py` `norm_map` / `TOKEN_RE` / `html` path: **live** — `_COPIES` has one `"html"` entry
  (`docs:admin-guide/cgroup-v2.html`, S520) and `html_norm_equals_r50_normalise` re-asserts its equivalence with
  the round-50 normaliser. Only `count-c2.py`'s twin is dead (§3.1); the asymmetry is correct, not copy-paste.
- `count-c1.py:318` `if key not in norm: bad += 1; continue` — not dead: it is the guard behind
  `scope_path_without_copy`, reachable whenever a claim row cites a v7.2 path the round has no v7.3 copy of
  (`scope_path_without_copy_unmet` exercises it).
- `count-c1.py` `r50_norm` lambda (586-587) — looks like a duplicate of `norm_map`'s HTML path, but it is the
  independent implementation that check `html_norm_equals_r50_normalise` compares against; deleting it would
  delete the check's meaning.
- `count-c2.py` `MIN_CLAIM_WORDS`/`MIN_BEYOND`/`MIN_WORDS`/`MAX_WORDS`/`MIN_CLAIMS`/`MIN_SOURCES`, `OPENED`,
  `VOTERS`, `MIN_VOTES` — every one is read in `evaluate`/`entail_votes`; a module-level scan found **no**
  name referenced only at its definition in any of the six files.
- `count-c2.py:341` `lane = os.path.dirname(os.path.dirname(os.path.dirname(here)))` in `selftest` — same value,
  different depth from the `repo` forms; folding all three into one `lane_root()` helper is §5, not a separate fix.
- `count-c2.py:178` `ls or (lambda d: [])` — `ruff ARG005` flags the unused `d`; `count-c1.py:284` writes
  `(lambda _d: [])`. Cosmetic only, no bytes execute differently; listed as a nit, not a deletion.
- `controls/controls.py` `OVERLAY` lists `controls.py` itself — live: the overlay copies the runner into each
  control clone so the clone is self-describing.
- `controls/c2data.py` `CG = c2.CGIT` — a one-use alias, but it keeps the four URL rows readable; not waste.
- `build-w1-spec.py` seat inventory — 74 items, 74 unique names, 0 duplicate prompts, 0 duplicate
  (name, role) pairs; nothing dead there.

## 7. What a successor must do together with these deletions

1. **Regenerate the frozen receipts.** `evidence/selftest-c1.txt` ends `C1_SELFTEST pass=57 fail=0` and
   `evidence/selftest-c2.txt` ends `C2_SELFTEST pass=54 fail=0`; §3.2 makes the first read `pass=56`. The
   `freeze-sha256.txt` pins and the SHONEN tally pins (`N/N`) name the same numbers, so the deletions, the new
   receipts and the pin text are one commit — which is exactly why a wave seat may not land them.
2. **Keep the predicate sentences byte-for-byte.** None of the deletions touches the docstring predicate; P-C1
   and P-C2 read the same after §3.1 and §3.2 (the removed `copies` parameter is not named in P-C2's sentence, and
   the removed selftest arm is not named in P-C1's).
3. **Re-run the control matrix**, because `controls/c1data.py` and `controls/controls.py` are in the freeze set:
   the 14 control verdict lines must reproduce `evidence/control-*.txt` with the edited appliers.
4. **Do not merge the two counters.** §5 shares helpers only; P-C1 and P-C2 must stay separately scorable so
   either claim can be run with the other's data reverted (contract `## Separability`).

## 8. Limits of this audit

- I did not execute the control runner (it builds up to seven `git clone --shared` trees; the seat budget is one
  clone per seat and I used none). The `controls.py` claim is therefore an import/pure-function proof plus a
  static non-use proof, not a 14-verdict replay; `Mo54ExecControlsReplay` is the seat that owns that replay.
- The `c1data.py` proof ran against a fixture root with no git history, so `scope_lines()` returned zero rows and
  the ledger table was empty. That exercises both edited lines (the used-by loop and the registry rows) but not
  the 31-row ledger body; a successor with the data commit available should re-run the applier against a clone
  before landing, and compare the ledger against `78295c76:corpus/knowledge/kernel-v7.3-recheck-r54.md`.
- The duplicate-fixture scan covers fixtures handed to `evaluate()` only; arms that assert pure helpers
  (`norm_map_text_lines`, `scope_reader`, `voters_frozen`, …) are outside it and were read by eye.
- Selftest tallies are the machinery's own arms, not outside verification: three deletions (§3.1, §3.2, §4) are
  proven by *the absence of any behavioural difference at two revisions*, which is stronger than a tally match,
  but the post-deletion counters were not scored against a met fixture (no votes exist yet at the data tip).
- `vulture` and `pyflakes` see text, not reachability; the only reachability verdict here is the raise-proof in
  §3.1. Counter weakness found: none — I changed no predicate, and the C1/C2 kill rules were not exercised.

## 9. Scratch, tooling, host

- Scratch `/fast/scratch/hyaku/mori-r54/Mo54SimpCode/` (`tmp/`, `base/`, `edit/`, `probe/`, `fix/`, `run/`) was
  `rm -rf`'d after this report was written; nothing under it is cited as evidence, all receipts above are pasted
  output. `TMPDIR` was pointed inside it for every run. No clone was made, no git/jj mutation was run anywhere,
  and the lane and fleet repos were only read (`git show`, `git rev-parse`, `git status --porcelain`, `grep`).
- Tools used were already installed: `ruff 0.17.2`, `pyflakes 4.0.3`, `vulture 2.16`, CPython 3.14.8. Nothing was
  installed or upgraded; no pacman command was run.
- Host reads: none beyond the tool versions. Host written to record: `MACHINE_ID`.
- `checks/`, `w1.ready`, `w1.ready.partial`, `evidence/gate-rejects.txt`, `evidence/receipt-stage-before.txt` are
  untracked at the wave root (`git status --porcelain .ufo/waves/round-54`); not mine to touch, and outside the
  files this seat audits — noted for whoever runs the misroot sweep.

## Findings

| # | severity | where | finding |
|---|---|---|---|
| 1 | MED | `count-c2.py:38, 96-101, 176, 180, 185, 189, 239` | Dead HTML path: `normalise()` is unreachable (raise-proof: identical output at two revisions), its only caller is the `kind == "html"` ternary that no `COPIES` entry can reach, `import html` serves only it, and the `copies` parameter it would be injected through is never supplied by any call site. −17/+5 lines, real-run output unchanged. |
| 2 | MED | `count-c1.py:571-574` | `html_line_located_met` re-assigns row 2's line cell to the value `default_rows()` already produced (1225 → 1225), so it feeds `evaluate()` a fixture byte-identical to `honest_met`'s and cannot fail independently — the only duplicate-fixture arm in either selftest (c1 53 runs, c2 51 runs scanned). Removing it: `pass=57` → `pass=56`, `fail=0`, real runs byte-identical. |
| 3 | MED | `count-c1.py` (187-191, 381-395, 479) / `count-c2.py` (169-173, 289-303, 382) / `controls/controls.py:78` | Helper duplication across the machinery: `sources_row` and `git_reader` byte-identical, `git_lister` differing only in a parameter name, `split_cells`/`claim_hash` semantically identical, `results()` defined three times, the 11-cell registry-row literal written four times, the lane-root chain three forms. ~21 lines + 7 shapes; a successor `w1common.py` removes them without touching a predicate, but changes the freeze set and every receipt. |
| 4 | LOW | `count-c2.py:365-367` | Always-true conditional in the selftest tracepoint quote: the concatenated `#define TRACE_SYSTEM ras #define TRACE_INCLUDE_FILE memory-failure` **is** present in the pinned copy (verified by substring test on `sources-r54/memory-failure-trace.h.v7.3`, 1 occurrence), so the `else quote_from(… "TRACE_EVENT(memory_failure_event" …)` branch never evaluates. Collapsed in §3.1 with the tally unchanged. |
| 5 | LOW | `controls/controls.py:15` | `import sys` unused (pyflakes F401). Removal proven import-clean and output-identical on the module's pure helpers. |
| 6 | LOW | `controls/c1data.py:76` (+`105`) | `registry_rows(root, rows)` never reads `root` (ruff ARG001); the parameter and its call-site argument are dead. Fixture proof: byte-identical `SOURCES.md` and ledger from the edited applier. |
| 7 | LOW | `controls/c1data.py:79, 97` | Unused loop variables: `h, entry, q, status` in the `by_key` fold and `key` in `for key, sid in REUSED.items()`. Names only; renamed `_`-prefixed in the scratch diff, outputs byte-identical. |
| 8 | LOW | `build-w1-spec.py:157` | `f` prefix on a placeholder-free literal (pyflakes / ruff F541). Not in the freeze list but still seat-immutable; the built `w1-spec.json` is byte-identical (130819 bytes) with and without it, and the AST constant is unchanged (78 words). |
| 9 | LOW | `count-c2.py:178` | `ls or (lambda d: [])` — unused lambda parameter `d` (ruff ARG005); `count-c1.py:284` uses `_d`. Cosmetic, no behavioural change; nit for whoever edits the file next. |
| 10 | LOW | `count-c2.py:309, 318, 341` | The lane-root path is computed inline three times (four-deep twice, three-deep once) where `count-c1.py:397` has the named `lane_root()`; folding them is part of finding 3, listed separately so the successor sees all three sites. |

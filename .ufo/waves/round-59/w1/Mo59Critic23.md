# Mo59Critic23 — C2 claim-grammar attack (line/offset ambiguity, vacuous spans)

Scope: attack the claim grammar of the frozen C2 counter — `line:` vs `offset:`
ambiguity, whitespace-only line citation, span distinctness. Frozen artifacts
read at `HEAD` = `8ff344ff` (post-freeze lane tip; freeze `60b3a76a`, entering
`2b9f0397`). All work read-only on the lane; fixtures materialized under
`/fast/scratch/hyaku/mori-r59/Mo59Critic23/` (since removed).

Verdict: **counterexample found — the grammar admits vacuous claim sets** that
score `eval_entry ok=True` (zero reasons) while carrying little distinct
evidence. This is a *laxity* finding: it does not show `C2=met` is unreachable
by an honest entry; it shows `met` is achievable by a degenerate one, so the
counter cannot distinguish the two. Severity MED (soundness gap, not a kill —
frozen bytes rule means correction lands on future grammar or judge scrutiny).

## Evidence

Method: imported `.ufo/waves/round-59/count-c2.py` with importlib and drove
`eval_entry(root)` on synthetic roots under scratch. `eval_entry` only checks
`sha256(copy_bytes) == pin` (count-c2.py:148), so roots were built both with
synthetic copy bytes (grammar isolation) and with **real committed artifact
bytes** (realizability: `git show HEAD:.ufo/waves/round-54..58/w1-results.json`,
`round-58/evidence/w1-settlement.json`).

### F1 — `line:` ≡ `offset:` on a one-line file; same span counted twice

`w1-settlement.json` is a single 230,410-byte line (1 `\n`, trailing):
`Quote: <line1> (f:line:1; pin p)` and `(f:offset:0; pin p)` cite **byte-identical
spans**; both parse and pass (count-c2.py:154-160). Demonstrated on
`synthetic A = b"hello world"` — `K1 line:1`, `K2 offset:0`, `K3 line:1`,
`K4 line:1`, `K07 line:1`, `K7 line:1` all pass; only checks are `kid in seen`
(raw string, :125-127) and byte equality. So `K07`/`K7` alias one numeric id,
and the same (file,kind,n) triple can be re-claimed under fresh K labels —
`claims` counter counts K-labels, not spans.

### F2 — degenerate 10-claim set over real artifact bytes scores ok

Built entry citing `corpus/evidence/sources-r59/w1-results-r58.json` (line 7 =
`  {`, occurring 64x at lines 7,13,19,...), `w1-results-r57.json`,
`w1-settlement-r58.json`, all pins = real sha256, plus mined/used-by S rows:

- K1 `  {` at `line:7`, K2 same text `line:13`, K3 same span `offset:76`,
  K4 `offset:411` — same/duplicate positions admitted.
- K5 ` "la` at `offset:2`, K6 `lane"` at `offset:4`, K7 whole line 2 —
  overlapping substrings inside one line admitted.
- K9 `{"igno` offset:0, K10 `1719,"la` offset:16 — substrings of the 230KB line.

`eval_entry` → `True {'claims': 10, 'files': 3} []` — **met with zero reasons**:
10 "claims" citing as few as ~20 distinct bytes. Grammar puts no lower bound on
distinct evidence per claim beyond `len(q)>=3` (:151).

### F3 — whitespace-only line is citable (grammar admits; latent this round)

`synthetic B = b"alpha\n   \nomega"`: `K8 Quote: \`   \` (f:line:2)` passes —
whitespace-only quote, byte-exact, len 3. Verified none of the six real
artifacts contain whitespace-only lines (all pretty-printed JSON; settlement is
one dense line), so this hole is **latent, not exploitable against the frozen
ARTIFACTS set** this round — it constrains future artifact choice.

### F4 — rows binding is per-SID, not per-copy

Contract: "the entry cites only S### rows opened this round (one per cited
artifact copy)". Counter (:161-189) only requires cited SIDs to exist as rows
with `cells[7]=="mined"` and `cells[10]==ENTRY`. Built entry with
`source: S920` alone + 10 claims over 3 files → `True`. One row can blanket-
cover all cited copies; no copy↔row pairing exists.

### F5 — expressiveness gap in the other direction (false-unmet risk)

`[^`]+` (regex :79) cannot quote a backtick. Real artifacts contain 6–24
backtick lines each (e.g. r57 results line 10, a `"output"` field quoting
SCORECARD prose with `driver-liveness` in backticks). Such lines are
uncitable via `line:` (byte-exact whole line impossible) and their backtick
segments uncitable via `offset:`. An entry that must cite such content has no
grammatical claim. Also `ln.startswith("**K")`-adjacent lines that fail regex
emit `grammar:` reasons (:121-122) — including *any* quote mentioning the
literal word `Quote: ` inside the prose field before the real one is fine, but
a quote containing `Quote: `` breaks parsing.

## Hostile-tree coverage

Frozen trees (`git ls-tree HEAD:.ufo/waves/round-59/trees-c2/`, expect.txt):
t01 frontmatter, t02 dup-K, t03 wrong-line, t04 stale-pin, t05 <10 claims,
t06 outside-file, t07-10 row defects, t11 sub-3-byte quote, t12 malformed
line. **No tree covers**: duplicate spans, same text at distinct lines,
line/offset dual citation, overlapping offset substrings, whitespace-only
quotes, K0-padded ids, single-SID multi-file. These gaps are unpatrolled.

## Impacted axes / smallest safe correction

- Impacted axis: **C2 depth** soundness of `entry=ok` arm only. `tree=`,
  `scan=`, `drift=`, `pins=`, `rows=` arms unaffected. No regression path to
  C1. Frozen-byte kill rule means findings are grammar critiques for the
  judge/lesson, not requests to patch the frozen counter.
- Smallest corrections (for a successor grammar): (a) dedupe on
  `(cfile, kind, n)` *and* on `(cfile, quote)` pairs; (b) normalize K id via
  `int(kid)` in `seen`; (c) require `q.strip()` non-empty or ≥N non-boilerplate
  line claims; (d) bind ≥1 cited SID per cited copy; (e) document or fix the
  backtick uncitability (alternate delimiter).

## Reproduction commands

```
python3 - <<'EOF'   # under TMPDIR=$HYAKU_SCRATCH/mori-r59/<seat>
import importlib.util; spec=importlib.util.spec_from_file_location(
 "c2",".ufo/waves/round-59/count-c2.py"); c2=importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2); ok,r,s=c2.eval_entry("<scratch>/g2"); print(ok,s,r)
EOF
git -C <lane> show HEAD:.ufo/waves/round-58/evidence/w1-settlement.json \
  | wc -l            # -> 1 line (230411 bytes)
```

Tool installs: none. Scratch `/fast/scratch/hyaku/mori-r59/Mo59Critic23/`
created per spec and removed before yield. No lane/fleet writes outside this
report; no VCS mutation.

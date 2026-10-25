# CritC1Counter — attack on `.ufo/waves/round-48/count-c1.py` (round 48, w1)

Seat: CritC1Counter (leaf; no subagents). Target: the frozen C1 counter
(`count-c1.py`, sha256 `7a2a6aa09b92…` at freeze `4387cf94`). All scoring was run
against `--rev 4387cf94b69ddce455051a1ff38e93795c2e6cde` with the frozen baseline
`2d85e33d14198d388fd3cda9cc15ec07e57e7a53` and `--min-tally-pins 26`, exactly as
P-C1 specifies. Lane tools ran with `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-CritC1Counter`.

No tools were installed (operator directive: nothing needed; all work used stdlib +
the frozen committed tool bytes). Counter selftest at freeze: `C1_SELFTEST pass=34
fail=0` (exit 0). Control stubs at freeze:
`stub-always-met.py` → `C1=unmet junk_met=8 … real=met`; `stub-always-unmet.py` →
`C1=unmet honest_unmet=4 real=unmet`.

**Environment note (read-only):** on 2026-10-25 ~18:35 the working-tree
`tools/mori-pin-check.py` changed under this seat (sha256 `9832e38c…` → `17cc5ba1…`,
mtime 18:35, `git status` shows ` M`). We observed it mid-run (a module import of
the dirty file crashed with `IndentationError`). All byte-level analysis below pins
the frozen entering copy (`controls/tool-v2-entering.py` / `git show
e5dbac05:tools/mori-pin-check.py`, sha256 `9832e38c…`). Also note the counter
executes the **working-tree bytes** of `--tool`, not the bytes at `--rev`; a dirty
`tools/` therefore makes C1 measure uncommitted bytes (see finding F8).

---

## F1 (class b) — a tool that does zero registry work prints `C1=met` by reading the harness's own filenames

**Reproducer** — `tool_a_filename_keyed.py` (scratch): it never parses the SKILL.md
content; it only reads `--skill`'s basename and prints/returns:

```python
if skill is not None and os.path.basename(skill).startswith("variant-J"):
    print("PIN_CHECK=unmet keyed=J"); return 1
print("PIN_CHECK=met keyed=H-or-real"); return 0
```

**Observed output** (counter exit 0):

```
variant name=J1 expect=unmet got=unmet rc=1
... J2..J8 all got=unmet rc=1 ...
variant name=H1 expect=met got=met rc=0
... H2..H4 all got=met rc=0 ...
variant name=real expect=met got=met rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=4387cf94b69ddce455051a1ff38e93795c2e6cde
```

The counter leaks the variant identity to the tool through two channels:
1. `--skill <scratch>/variant-J1.md … variant-H4.md` — the **basename** encodes J vs H;
2. the environment variable `TMPDIR` is set to a per-variant `mkdtemp` dir named
   `c1-J1-…`, `c1-H1-…` (visible to the tool via `os.environ`).

With either channel, a tool can be red exactly on J1-J8 and green on H1-H4 + real
without inspecting a single registry row. The contract's named-limits sentence
anticipates narrowing by content (pipe / non-ASCII / fence) but not harness-keyed
special-casing; the counter's verdict is behavioral and cannot block it.

**Smallest counter change:** present variants opaquely —
- write every variant to the **same fixed filename** inside its per-variant scratch dir
  (e.g. `variant.md`, or feed the registry by stdin), so `--skill` basenames do not
  distinguish J from H; and
- set each run's `TMPDIR` to a neutral name (`sub`, `scratch`, `tmp`) instead of the
  `c1-<variant>-` prefix, so the env doesn't leak the variant either.
- Add one honest variant that a whitelist/identity tool cannot pass: **H5 — an
  existing row's tally pin updated to a new valid value** (e.g. `pass=34 fail=0` →
  `pass=35 fail=0` on the real `PIN_CHECK_SELFTEST` row, as an honest re-measurement).
  A tool that green-lights pins by baseline equality or by identity would score H5
  unmet → `honest_unmet` → `C1=unmet` (this also semantically closes the "accept any
  pin that matches a known-good pin" narrowing).

I also scored the three content-based narrowing suggestions for the record. All fail
the counter (they are over-broad and also red on real), which shows the real arm does
guard against coarse rejections:

| tool | idea | C1 result |
|---|---|---|
| B (`tool_b_nonascii.py`) | reject any row containing a non-ASCII char | `C1=unmet … real=unmet` (real rows contain e.g. `—`, `…`) |
| C (`tool_c_pipe_fence.py`) | reject any row containing a pipe or fence mark | `C1=unmet … real=unmet` (every row has `\|`) |
| E (`tool_e_pin_multiset.py`) | require the global (prefix, pin) multiset to equal the baseline's | `C1=unmet … honest_unmet=4` (H4 adds a duplicate pin pair; J7/J8 untracked) |

So the only "cheap" green tool found is the harness-keyed one (F1).

## F2 (class a) — real registry cannot be green under a faithful R4 (rebound by prefix)

The v3 spec rule R4 says: *"the baseline revision's set of `prefix → bound argv` is
recorded; a row, new or old, that uses a baseline prefix with an argv not in that
prefix's baseline set is `rebound`."*

The real registry at freeze has row 939 (`r47 tracepoint catalogue (C2)`), whose
self-test cell binds `C2_SELFTEST` to `python3 .ufo/waves/round-47/count-c2.py
--selftest`. The frozen baseline `2d85e33d` (0 hits for `round-47/count-c2.py`) has
`C2_SELFTEST` argv set = {`.ufo/waves/round-44/count-c2.py`,
`.ufo/waves/round-45/count-c2.py`}. Literal R4 ⇒ `rebound=1` on real.

**Observed** (v3 reference tool, real run):
```
PIN_CHECK=unmet tally_pins=28 digest_pins=3 mismatches=1 … rebound=1 … hidden=0
```

Consequence: any candidate that implements R4 as written prints `PIN_CHECK=unmet`
on the honest edits **and** on real → `C1=unmet` even for an otherwise correct v3.
The round-47 C2 row is a legitimate re-measurement of an old prefix with a new
instrument path; R4 needs to be scoped (e.g. compare only rows whose row-name already
existed at baseline — then J4's *new* row slips, so J4 must additionally be caught by
an archived-path rule) or the baseline/registry must be adjusted. This is a spec-vs-
registry incoherence the L1 must resolve before landing; as frozen, literal R4 is not
satisfiable on the current registry.

## F3 (class a) — real registry carries a stale truncated digest that R6 flags

Row 168 (`r14 regressions`) self-test cell contains the bare span `` `c39e5a73…` ``.
The only path named in that row is `.ufo/waves/round-14/frozen/mori-census.sh`, whose
sha256 at freeze starts `39abda0a67028575…`; `c39e5a73…` resolves to nothing named in
the row. A faithful R6 (digest-prefix resolution) ⇒ `mismatches=1` on real.

**Observed** (same real run as F2, `mismatches=1`; H1-H4 inherit the same red).

This is exactly the class v3-spec says is "repaired in the registry, never excused in
the tool" — the registry row must be fixed (replace with an accurate prefix/full hash
or drop it) before landing, or real stays red under R6.

## F4 (class a / spec sharpening) — R3's literal text is over-broad; literal implementations are red on real

As written, R3 clause 2 (backticked span "whose NFKC-casefolded text contains
`selftest` but is not an ASCII tally pin") fires on **every command span that contains
`--selftest`** (60 spans in the real registry, e.g. `` `bash tools/mori-census.sh
--selftest` ``), and clause 1 (non-ASCII first token) fires on truncated-digest spans
(`` `c39e5a73…` ``, `` `37fd7c24ff52…` ``, `` `69bf9b6eb29b…` `` — U+2026 is
non-ASCII). Even after reasonable scoping (skip interpreter/env/flag/path-first spans
and pure `[0-9a-f]{8,63}…` spans), two real spans still trip a token-endswith
"selftest" clause: rows 178 and 609 (`` `mkdir -p .scratch && TMPDIR=$PWD/.scratch
python3 …` ``, `` `TMPDIR=<existing-private-scratch> python3 …` ``). A literal R3 makes
real red; candidates must scope R3 to pin-like spans (and exclude U+2026 tails). This
is a spec-text sharpening needed before the v3 candidate can be green on real.

## F5 (class a) — J1/J5/J6 depend on execution-based pin comparison; static rules alone cannot catch them

Under the static reference (no instrument execution), J1 is indistinguishable from
real (same counts: `mismatches=1 rebound=1`, both from F2/F3): its corruption is a
pinned-value change (`pass=34/13` → `pass=1`), detectable only by running the bound
instrument and comparing its observed tail (v2-style). J5/J6 are caught by R2
(`hidden=2` each — fenced/blank-separated corrupt rows), J2/J3 by R3 (`unparsed=1`),
J4 by R4 (`rebound` +1 on top of F2's), J7 by R5 (`mismatches` +1 via `(742 lines)`
vs the 743-newline `tools/mori-gate-registry.py`), J8 by R6 (`mismatches` +1 via
`37fd7c24ff53…` ≠ any named path's prefix). All eight junk edits are correctly red
under the rules; the classification itself is coherent — the blockers are all on the
honest/real side (F2, F3, F4).

## F6 (class c) — error handling gaps (no false-met, but unclean exits)

- Missing/typo'd `--tool` path: `subprocess.run` raises `FileNotFoundError` inside
  `run_tool`; the `ThreadPoolExecutor` future propagates it and the counter dies with
  a traceback and **no C1 line** (exit 1) instead of a clean `C1_SETUP` exit 2.
- `int(opts["--min-tally"])` raises `ValueError` on a bad value (traceback, exit 1)
  instead of setup exit 2.
- Timeout handling is safe: 900 s per variant → `timeout` → counted in `errors` (never
  `met`). Worst-case wall time with jobs=4 and 13 variants ≈ 13×900/4 s on a serialized
  slow tool.

## F7 (class d) — no races found in the pool/shared scratch; one mild interference surface

Variant files are written before the pool starts; per-variant
`tempfile.mkdtemp(dir=scratch)` subdirs are unique and created synchronously in the
main thread; `TMPDIR` is per-run; results are sorted deterministically after the pool.
No data race or shared-scratch collision was found. The only interference surface is
the TMPDIR/`--skill` naming itself (F1). A reused `--scratch` directory across
repeated runs accumulates `c1-<variant>-…` subdirs (harmless) but also lets a tool
observe sibling runs' names — same fixing class as F1.

## F8 (class c / landing hygiene) — the counter measures working-tree bytes, not revision bytes

The counter runs `os.path.abspath(opts["--tool"])` from the working tree. If `--tool`
is `tools/mori-pin-check.py` and the tree is dirty (observed above), C1 scores
uncommitted bytes while `--rev` points elsewhere. The L1 must commit the candidate
before the acceptance run (or the receipt must record the tool's sha256). No action
needed in the counter itself.

---

## Smallest safe corrections (summary)

1. **F1**: make variant presentation opaque — fixed `--skill` basename per variant and
   neutral `TMPDIR` name; add honest variant H5 (existing row's pin updated to a new
   valid value). This is the only proven way the counter currently prints `C1=met`
   for a tool that does no registry validation.
2. **F2/F3**: resolve the spec/registry incoherences before landing — R4 needs row-
   scoped baseline membership (or equivalent) or J4 must be caught another way; row
   168's stale truncated digest must be repaired in the registry. Otherwise a correct
   v3 candidate prints `C1=unmet` (honest_unmet=4 / real=unmet) at the freeze revision.
3. **F4**: sharpen R3's wording (pin-like spans only; exclude U+2026 tail; exclude
   command/env/flag spans) so a literal implementation can be green on real.
4. **F6**: catch `FileNotFoundError`/bad ints in `run_tool`/`main` and exit 2 with a
   `C1_SETUP` line.

All outputs above are observed (command + exit codes recorded in this report);
"UNVERIFIED" applies only to anything not checked, none remains for the claims above.
Working copies of the tools and transcripts live in
`.scratch/r48-CritC1Counter/` (`tool_a_filename_keyed.py`, `tool_b_nonascii.py`,
`tool_c_pipe_fence.py`, `tool_e_pin_multiset.py`, `tool_v3ref.py`, `v2-entering-frozen.py`).

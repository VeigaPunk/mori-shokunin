# RevKnowledgeProvenance — provenance and citation review of `corpus/knowledge/conform-scope-r40.md` (read-only)

Seat: reviewer, mori round 40 wave 1 (L1 mori-r40 attempt 1). Bounds honoured:
no production edits, no git/jj mutation, no sibling-lane or fleet writes; this
report is the only file written. Tools installed: none (python3 stdlib only).

Measured lane state: `git --no-optional-locks rev-parse HEAD` =
`ede486b7a09afbacfb380d5871c46a8051a6dc2e`; entry worktree blob =
`git hash-object corpus/knowledge/conform-scope-r40.md` =
`a2eb6efd9c956ddb6643a0e95a24aefc016a1467` = `git rev-parse
HEAD:corpus/knowledge/conform-scope-r40.md`; `git diff HEAD --
corpus/knowledge/conform-scope-r40.md` is empty. The entry landed at
`265a955` ("round-40: instruments — conform v3 (P-C10), gate v3 (P-C11),
S229, r39 erratum") and is unchanged at HEAD.

Report-path note: the delivered prompt ended with the `Report:` trailer
sentence but carried no path, and `.ufo/waves/round-40/w1-spec.json`'s
`RevKnowledgeProvenance.prompt` likewise ends at that sentence. I used the
wave's uniform convention (every landed sibling report): `.ufo/waves/round-40/w1/<SeatName>.md`.

## Verdict

| required check | verdict |
|---|---|
| provenance trio (source S229 + URL, verified-at, recheck) opens the entry | **PASS** |
| cited URL / copy / dates match the S229 registry row | **PASS** |
| quoted sentence is verbatim and inside §4.2.2 | **PASS** |
| r39 finding numbers resolve to the named seats | **PASS** (4 = RevC8Value, 8 = RevC8Drain) |
| every technical claim cites S229 §4.2.2 or the r39 findings | **PARTIAL** — one MEDIUM accuracy falsification, one LOW warrant gap, three LOW precision items |
| unsourced claims | none wholly unsourced; five findings under-cite or overstate a claim (F1–F5) |

The entry is a legitimate round-40 source note: its provenance chain resolves,
its central quote is real, and its positive behavioural claims check out. Its
one substantive defect is the sentence "models exactly three cases" (F1),
which the landed checker falsifies in two `global` corners and which the
already-landed CritNewSurvivor seat falsifies for binding-form coverage.

## Axes

1. **Provenance resolvability** — every pointer in the header and body opens a
   committed byte that says what the entry says it says.
2. **Citation-to-claim mapping** — each technical sentence is warranted by
   S229 §4.2.2 or by the r39 findings it names, at the granularity the claim
   needs (section-level vs quote-level).
3. **Claim accuracy against landed code** — a sentence describing
   `conform.py` must be true of `conform.py`, especially when it uses "exactly".
4. **No-harm** — read-only; no production, registry, gate, or sibling edit.

## Checks run (exact commands and outputs)

### A. Provenance trio and registry agreement

```sh
sed -n '1,8p' corpus/knowledge/conform-scope-r40.md
```

```text
# conform-scope-r40 — why the timeout fold is scope-aware

source: S229 — Python execution model, Naming and binding
(https://docs.python.org/3/reference/executionmodel.html#naming-and-binding,
copy `corpus/evidence/sources-r40/S229.src`)
verified-at: 2026-10-24
recheck: on-release
```

```sh
grep -n '| S229 ' corpus/SOURCES.md
ls -l corpus/evidence/sources-r40/S229.src
wc -l corpus/evidence/sources-r40/S229.src
```

```text
235:| S229 | Python execution model — Naming and binding — https://docs.python.org/3/reference/executionmodel.html#naming-and-binding | docs | A | Python name-resolution rules for blocks: where assignment binds, and the nearest-enclosing-scope lookup a static timeout fold must model | §4.2.2 Resolution of names:249-262; "When a name is used in a code block, it is resolved using the nearest enclosing scope":254-256; page fetched 2026-10-24 | An assignment inside a function block binds the name locally for the whole block, so a module-map constant fold must read a function-local binding before any module-level map. | mined | 2026-10-24 | on-release | corpus/knowledge/conform-scope-r40.md |
-rw-r--r-- 1 vgpnk vgpnk 63374 Oct 24 02:46 corpus/evidence/sources-r40/S229.src
868 corpus/evidence/sources-r40/S229.src
```

URL string equality, `verified-at` = registry `opened` = "page fetched
2026-10-24", `recheck` = registry `on-release`, `used-by` names this entry.
The trio is lines 3–7, before any body text; sibling entries
(`gate-ancestry-r39.md`, `source-drift-content-anchor-r38.md`) use the same
title-then-trio layout. **PASS.**

### B. Quote and section

```sh
grep -n '<section id="naming-and-binding"\|<section id="binding-of-names"\|<section id="resolution-of-names"\|<section id="annotation-scopes"' corpus/evidence/sources-r40/S229.src
grep -n 'When a name is used in a code block' corpus/evidence/sources-r40/S229.src
```

```text
248:<section id="naming-and-binding">
250:<section id="binding-of-names">
287:<section id="resolution-of-names">
355:<section id="annotation-scopes">
294:<p id="index-8">When a name is used in a code block, it is resolved using the nearest enclosing
```

The entry's quote (`:16-17`) is verbatim modulo the copy's line wrap, and
§4.2.2 spans `S229.src:287-354` (heading at 288, next section at 355). **PASS.**
Note: the copy's own line numbering is the lane's demonstrated convention —
`S227.src:2542-2544` and `S228.src:657-659` are cited at exactly those lines in
their registry rows.

### C. r39 finding mapping

```sh
grep -n 'RevC8Value\|RevC8Drain' corpus/lessons/round-39.md
```

```text
47:4. (w1/RevC8Value, HIGH) timeout_value survives two r38-M19-class bypasses: a function-local shadow
66:8. (w1/RevC8Drain, HIGH) drain_shape never binds a communicate to a Popen: any used communicate in a
```

Entry `:10` = finding 4, entry `:34` = finding 8. Finding 4's body also
carries the "1e400 fails / fold crashes exit 2" lines the entry cites at `:32`
(`round-39.md:52`). **PASS.**

### D. Positive behavioural claims (landed checker, importlib)

```sh
python3 - <<'EOF'
import importlib.util, json
spec = importlib.util.spec_from_file_location("c40", ".ufo/waves/round-40/conform.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def probe(label, src):
    r = m.static_checks(src)
    print(label, "value_violations=", r["value_violations"], "| drain=", r["drain_violations"])
probe("nested-global", '''
import subprocess
TIMEOUT = 120
def run():
    TIMEOUT = None
    def inner():
        global TIMEOUT
    return subprocess.run(["true"], timeout=TIMEOUT)
''')
probe("plain-shadow", '''
import subprocess
TIMEOUT = 120
def run():
    TIMEOUT = None
    return subprocess.run(["true"], timeout=TIMEOUT)
''')
probe("param-default-none", '''
import subprocess
def run(timeout=None):
    return subprocess.run(["true"], timeout=timeout)
''')
probe("cond-agree", '''
import subprocess
T = 120
if True:
    T = 120
def run():
    return subprocess.run(["true"], timeout=T)
''')
probe("cond-disagree", '''
import subprocess
T = 120
if True:
    T = 60
def run():
    return subprocess.run(["true"], timeout=T)
''')
probe("with-nested", '''
import subprocess
T = 120
with open("/dev/null"):
    T = None
def run():
    return subprocess.run(["true"], timeout=T)
''')
probe("inf", '''
import subprocess
T = 1e400
def run():
    return subprocess.run(["true"], timeout=T)
''')
EOF
```

```text
nested-global value_violations= [] | drain= []
plain-shadow value_violations= ['line 7 (run): non-numeric constant'] | drain= []
param-default-none value_violations= ['line 4 (run): non-numeric constant'] | drain= []
cond-agree value_violations= [] | drain= []
cond-disagree value_violations= ["line 7 (run): name 'T' is conditionally rebound"] | drain= []
with-nested value_violations= ['line 7 (run): non-numeric constant'] | drain= []
inf value_violations= ['line 5 (run): timeout value inf is not finite'] | drain= []
```

```sh
python3 - <<'EOF'
import importlib.util
spec = importlib.util.spec_from_file_location("c40", ".ufo/waves/round-40/conform.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def probe(label, src):
    r = m.static_checks(src)
    print(label, "value_violations=", r["value_violations"])
probe("divzero", '''
import subprocess
T = 120/0
def run():
    return subprocess.run(["true"], timeout=T)
''')
probe("selfref", '''
import subprocess
T = T
def run():
    return subprocess.run(["true"], timeout=T)
''')
probe("global-in-same-fn-shadow", '''
import subprocess
TIMEOUT = 120
def run():
    global TIMEOUT
    TIMEOUT = None
    return subprocess.run(["true"], timeout=TIMEOUT)
''')
EOF
```

```text
divzero value_violations= ['line 5 (run): fold error: division by zero']
selfref value_violations= ['line 5 (run): fold error: maximum recursion depth exceeded']
global-in-same-fn-shadow value_violations= []
```

The `nested-global` row is the F1 counterexample — the checker should reject
it and does not; `with-nested` confirms the entry's `with` case (`:26`) is
implemented and fails closed; `param-default-none` confirms a parameter binding
of `None` fails. These verify entry `:23-24` (function-local `None` fails),
`:26-28` (conditional
rebind fails unless bindings agree), `:30-32` (`1e400` fails; `ZeroDivisionError`
/`RecursionError` become violations, not setup errors — the catch is
`conform.py:410-414`, not the setup-error path at `conform.py:803`). The
`with` in entry `:26` is real: `_module_assignments` includes `ast.With`
(`conform.py:227`). Drain claim `:34-37` matches `conform.py:432-455` (per
`Popen` target name, same enclosing function, timeout present, result
consumed). **PASS for all positive claims.**

### E. Registry anchor corroboration (independent reproduction)

```sh
grep -n '<section id="naming-and-binding"\|<section id="binding-of-names"\|<section id="resolution-of-names"' corpus/evidence/sources-r40/S229.src
grep -n 'When a name is used in a code block' corpus/evidence/sources-r40/S229.src
grep -n 'The following constructs bind names' corpus/evidence/sources-r40/S229.src
```

```text
248:<section id="naming-and-binding">
250:<section id="binding-of-names">
287:<section id="resolution-of-names">
294:<p id="index-8">When a name is used in a code block, it is resolved using the nearest enclosing
253:<p id="index-5">The following constructs bind names:</p>
```

The registry row's `anchor` cell cites `§4.2.2 Resolution of names:249-262` and
the quote at `:254-256`. Measured: `:249-262` is §4.2/§4.2.1 (section at 248,
4.2.1 at 250, constructs list at 253-262), and `:254-256` is inside that list;
the quote is at `:294-295`. This reproduces
`ScrSourcesRow.md` F2 independently (same numbers; that seat measured the
heading at 288, section start at 287 here). It is a defect in the registry row,
not in the entry — the entry cites the section, never the wrong lines. Recorded
here for the canonical judge because the `anchor` cell is immutable
(`corpus/QUALITY.md` 113, as cited by `ScrSourcesRow`), so the disposition is a
superseding row, not an edit.

## Findings

### F1 — MEDIUM (accuracy): entry `:20-21` "models exactly three cases" is false

The entry paraphrases `_resolve_timeout_name`'s own docstring
(`conform.py:265-269`) but presents the docstring as the implemented model. Two
probes show the code does not implement the entry's case 1 / case 2 split:

```sh
python3 - <<'EOF'
import importlib.util
spec = importlib.util.spec_from_file_location("c40", ".ufo/waves/round-40/conform.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
nested = '''
import subprocess
TIMEOUT = 120
def run():
    TIMEOUT = None
    def inner():
        global TIMEOUT
        return TIMEOUT
    return subprocess.run(["true"], timeout=TIMEOUT)
'''
samefn = '''
import subprocess
TIMEOUT = 120
def run():
    global TIMEOUT
    TIMEOUT = None
    return subprocess.run(["true"], timeout=TIMEOUT)
'''
for label, src in (("nested-global", nested), ("same-fn-global", samefn)):
    print(label, "value_violations=", m.static_checks(src)["value_violations"])
EOF
```

```text
nested-global value_violations= []
same-fn-global value_violations= []
```

Runtime scoping proof (same interpreter, no checker):

```sh
python3 - <<'EOF'
TIMEOUT = 120
def run():
    TIMEOUT = None
    def inner():
        global TIMEOUT
        return TIMEOUT
    return TIMEOUT, inner()
print("nested:", run(), "module TIMEOUT:", TIMEOUT)
TIMEOUT2 = 120
def run2():
    global TIMEOUT2
    TIMEOUT2 = None
    return TIMEOUT2
print("same-fn:", run2(), "module TIMEOUT2:", TIMEOUT2)
EOF
```

```text
nested: (None, 120) module TIMEOUT: 120
same-fn: None module TIMEOUT2: None
```

Both counters pass `timeout_scope` with a runtime-`None` drain — the exact
class entry `:23-24` says case 1 closes:

- **nested `global`**: `_global_names(fn)` (`conform.py:254-259`) walks *all*
  nested nodes of `fn`, so a `global TIMEOUT` in `inner()` suppresses `run()`'s
  own `TIMEOUT = None` (`conform.py:271,283`). S229 §4.2.2 says the opposite:
  "The `global` statement has the same scope as a name binding operation in the
  same block" (`S229.src:319-320`). The entry's case ordering (function binding
  first, then `global`) is also reversed in the code, which tests
  `is_global` first.
- **same-function `global` rebind**: the read is routed to module scope as the
  entry says, but `unconditional` is the pre-call module map, so
  `global TIMEOUT; TIMEOUT = None` still resolves 120 while the module value at
  the read is `None` (`conform.py:272,283-284,301`).

Not a duplicate of already-landed work: `CritNewSurvivor.md:15-71` falsifies C1
through binding-form blindness and BFS ordering (walrus, tuple-unpack,
dead-loop rebind). These two are scope-routing defects on the `global` case the
entry explicitly claims is modelled; the walrus survivor (`CritNewSurvivor`,
`CONFORM=met` with runtime `None`) is independent corroboration that "exactly
three cases" cannot stand. Correction: narrow entry `:20-21` to the binding
forms and scope decisions actually implemented, or land a v3.1 that collects
`global` per function block and folds same-function `global` assignments; do
not keep "exactly" while the class is admitted.

### F2 — LOW (warrant granularity): the whole-block rule is cited at section level, not quote level

Entry `:17-19` ("An assignment anywhere in a function block binds the name
locally for the entire block") is warranted by a *different paragraph* of
§4.2.2 than the one quoted: `S229.src:302-303` — "If a name binding operation
occurs anywhere within a code block, all uses of the name within the block are
treated as references to the current block." The quoted sentence
(`S229.src:294-295`, nearest enclosing scope) establishes lookup scope, not
whole-block binding. The cite `(S229 §4.2.2)` is attached to the preceding
sentence and the section is correct, so this is not an unsourced claim; it is
the one place where the quote shown does not carry the sentence built on it.
Recommendation: quote/line-anchor `:302-303` (one clause) or add "`S229.src:302-303`".

### F3 — LOW (provenance evidence): `verified-at` is a bare date

Entry `:6` records only `2026-10-24`. 21 of the 38 knowledge entries that carry
a `verified-at:` line append the command/receipt; both provenance-critical
siblings do
(`gate-ancestry-r39.md:6-11`, `source-drift-content-anchor-r38.md:5-6`). The
date itself is corroborated by the registry (`opened 2026-10-24`, "page fetched
2026-10-24") and the copy's commit date, but the entry names nothing that was
verified. Recommendation: record the quote-extraction check (e.g. section/quote
line numbers) so a reader can replay the verification rather than trust the
date.

### F4 — LOW (predicate/entry mismatch): `with` in case 3 exceeds the frozen P-C10 text

Entry `:26` lists `if`/`try`/`for`/`while`/`with`. The frozen P-C10 text
(`.ufo/waves/round-40/conform.py:99-110`, contract) lists only
`if`/`try`/`for`/`while`. The code includes `ast.With`
(`conform.py:227`), so the entry is code-accurate and the predicate is the
narrower text. No behavioural error, but it is the same words-vs-code class the
round routes as defect 3 (one source of truth). Recommendation: decide one
side — either add `with` to P-C10's wording or drop it from the entry.

### F5 — LOW (over-broad first sentence): "every `timeout=` keyword" was not all module-map

Entry `:9-10`: "Round 39's `timeout_value` check resolved every `timeout=`
keyword from the module top-level assignment map." `RevC8Value.md:23-27,79-89`
records that r39 also resolved parameter defaults and folded literals/`BinOp`;
the module map governed non-parameter `Name` resolution read-site-blind. The
defect attribution to finding 4 is correct; the quantifier "every" is not.
Recommendation: "resolved a timeout `Name` from the module top-level map with
no regard for the read site".

### F6 — NOTE (attribution stretch): "same nearest-scope principle grounds the drain half"

Entry `:34-37` cites finding 8 correctly and its description matches
`round-39.md:66-71` and the code (`conform.py:432-455`). But S229 §4.2.2 is
about name resolution across blocks; `drain_bind` is about binding identity
(same target name, same enclosing function, consumed result), not nearest-scope
lookup. The paragraph is sourced by finding 8, so this is a wording stretch,
not an unsourced claim. Optional: "the same per-binding discipline" instead of
"same nearest-scope principle".

## Residual risk and verification gaps

- I did not run `conform.py --selftest` or the full CLI on the counter of
  record; those are executor seats (`ExeConformSelftest`, `ExeConformMet`), and
  F1's probes call `static_checks` directly, which is the exact function the
  entry describes. A CLI-level reproduction of F1 would be a v3.1 regression
  fixture, not evidence needed for this finding.
- The S229 fetch date is corroborated only by the registry row and the commit
  timestamp; there is no HTTP receipt in evidence, so `verified-at: 2026-10-24`
  is not independently datable from the copy itself.
- No `lsp` device exists in this seat's tool inventory; `lsp` status is not
  available. No LSP server applies to a markdown note, and the definition/
  reference targets here are committed bytes, so I used `importlib` +
  `ast`-level execution for semantic checks and `grep`/`nl` only for literal
  line/quote location on committed files.
- F7/registry-anchor disposition depends on the canonical judge accepting the
  superseding-row route; I did not edit the row.
- The report path was inferred (see header). If the harness expected a
  different trailer path, this file is still the wave-convention location used
  by every sibling seat.

## Artifact paths

- This report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/w1/RevKnowledgeProvenance.md`
- Entry under review: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/conform-scope-r40.md`
- Source copy: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r40/S229.src` (§4.2.2 at 287-354, heading 288, quote 294-295, whole-block rule 302-303, global-scope rule 319-320)
- Registry row: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md:235`
- Checker: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/conform.py` (`_global_names` 254-259, `_resolve_timeout_name` 262-301, With 227, catch 410-414)
- r39 findings: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-39.md:47` (4), `:66` (8), `:52` (exit-2 gap)
- Already-landed corroboration: `.ufo/waves/round-40/w1/CritNewSurvivor.md` (C1 falsified), `.ufo/waves/round-40/w1/ScrSourcesRow.md` F2 (anchor lines)

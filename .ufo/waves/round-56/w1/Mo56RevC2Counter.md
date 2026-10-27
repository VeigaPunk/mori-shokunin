# Mo56RevC2Counter — mechanism review of `.ufo/waves/round-56/count-c2.py`

Seat: Mo56RevC2Counter (wave w1, mori round 56). Scope: the frozen C2 counter
mechanism — pin scope, the exact-tally substring check, the junk control, the
contrast arm, entry/row checks — plus three concrete bypass constructions.
Freeze tip measured: `8be2717b0809281d07dffe83dad424a4859e0747` (control rev:
entering tip `5b295eeebd87ebd610d8d39bfe2035742f740cfa`). All fixture work in a
`git clone --shared` under scratch (`/fast/scratch/hyaku/mori-r56/Mo56RevC2Counter/fixture`);
no mutation of the lane repo, fleet root, or lane jj/git state. TMPDIR was my
seat scratch. No installs, no pacman (host-wide pause), no network.

This report contains no vote items and opens no line with a vote-shaped verb.

## Baseline reproduction (both frozen claims' commands, read-only)

```
$ python3 .../round-56/count-c2.py 8be2717b0809281d07dffe83dad424a4859e0747
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
exit=0        # matches evidence/c2-at-freeze.txt

$ python3 .../round-56/count-c2.py 5b295eeebd87ebd610d8d39bfe2035742f740cfa
C2=unmet selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=5b295eeebd87ebd610d8d39bfe2035742f740cfa failed=tool_absent
exit=1        # matches evidence/controls.txt
```

Pin verification (mine): `git show 8be2717b:tools/mori-vote-bind.py | sha256sum`
= `8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca` = counter
`PIN`. Working-tree copy identical. `evidence/freeze-sha256.txt` also pins
`count-c2.py` (`4b350c77…`) — but nothing *enforces* that pin at runtime; the
counter never verifies its own bytes (contract says immutability is
process-level). Round-55 artifacts are byte-identical between entering and
freeze tips (`git diff --stat` empty), so the contrast inputs are stable.

## Check-by-check mechanism findings

### Pin scope
`PIN` covers only `tools/mori-vote-bind.py` bytes (`sha(git_show(R, TOOL))`).
Ledger, results, the r55 counter, the entry, and SOURCES.md are read at R via
`git show` — correct "committed bytes" semantics, but unpinned: the check only
asserts the computed *result* (exact tally line), not the artifact bytes. That
is the intended design (tally over whatever is committed), not a hole — any
artifact change is surfaced by the tally line itself. Sound.

### Exact-tally substring check (`EXPECT_TALLY not in p.stdout`, line 96)
At freeze this is correct: the pinned tool prints **exactly one** TALLY line to
stdout and **zero** bytes to stderr (verified: `grep -c TALLY` = 1, err.txt
empty). The substring test is nevertheless loose in both directions:

- Overmatch: any line *containing* the expected string passes — a prefixed
  `XTALLY rows=78 …` or a duplicated/diagnostic second line with different real
  numbers would still pass. Not exploitable while PIN holds (the tool's only
  stdout writer is the single `print` at tool:439).
- Under-asserted siblings: the check never asserts `returncode`'s companions —
  it does not verify the line is *the last/only* line or that stderr is clean.

Same looseness in the selftest check (`EXPECT_SELFTEST not in p.stdout`, line
90) and the control check (line 108). Severity LOW while the pin holds; named
limit for round 57 if arms ever gain richer output.

### Junk control (`zero=78`, `double=0` substrings, line 108)
The generated junk (`"no votes here, just prose"` for all 16 voters) is
genuinely vote-free for this binder: it fails `json.loads` (→ text channel)
and no line matches `VOTE_RE` (no `RECHECK`/`ENTAIL` token). So the literal
predicate — "outputs are junk, tallies zero=78" — is honestly met; the tool
prints `TALLY rows=78 agree=0 double=0 single=0 zero=78 dissent=0 voters=16
bound_voters=0`.

Two weaknesses, one latent one coverage:

- Under-assertion (latent): the check requires `zero=78` + `double=0` but never
  asserts `bound_voters=0`, `voters=16`, `rows=78`, `agree=0`, `dissent=0`, or
  even a TALLY-shaped line. `zero=78` mathematically forces `double=0` (any
  row with votes can't be zero), so the added `double=0` term is redundant —
  while the *more informative* `bound_voters=0` (did junk bind at all?) is left
  unasserted. LOW.
- Coverage (named limit): the control exercises exactly one junk shape —
  non-JSON prose with no verb token. It does not probe near-miss junk that
  *should* still not bind: a bare `RECHECK` word, `RECHECK <12-hex>` without a
  word, a 13-hex hash, a JSON yield containing only non-vote strings, or prose
  embedding a vote sentence. The selftest covers several of these at unit
  level, so this is a narrowness note, not a hole.

### Contrast arm (r55 counter at R must print `voted=0`)
At the real freeze the contrast is genuine: the `.ufo/waves/round-55/w1/*.md`
files exist at R (64 files), the r55 counter's per-voter `bound` check
(text-line equality against `results.json` outputs) fails on every voter
because outputs are JSON yields, and `voted=0 failed=votes` results. The
premise "same bytes, different binding" holds there.

But the arm's *acceptance condition* is `p.returncode in (0,1)` plus the bare
substring `"voted=0" in p.stdout` (line 119). `voted=0` is emitted on **every**
r55 evaluate path whose vote arm fails — including paths where the difference
is missing inputs, not binding grammar. Demonstrated below (Bypass B): delete
all 64 voter `.md` files and the arm still passes byte-identically. The arm
therefore cannot distinguish "the binder shape is the whole difference" (the
claimed contrast) from "the vote surface is absent entirely" (a confounded
contrast). MED — the check asserts an output substring, not the causal claim in
the parenthetical. A minimal strengthening (round 57 item, not this round's
fix): also require `failed=votes` and that `.md` files are present at R.

### Entry / row checks (lines 121–132)
- Entry: `"S545" in entry and "mori-vote-bind.py" in entry` — two bare
  substrings on the whole file. Any file mentioning both tokens anywhere
  (title, stray line, unrelated prose) passes; content is never evaluated.
- Row: first `| S545 |…` line must contain `mined`, `2026-10-27`, and the entry
  path as substrings, anywhere in the line, in any column. `unmined`
  contains `mined`; `not-2026-10-27` contains `2026-10-27`; the path can sit in
  the wrong cell. Demonstrated below (Bypass A): an inverted/junk row passes.
  Note the counter takes the *first* matching S545 line — a shadow row placed
  earlier would fail closed (harmless direction), but a shadow row passing the
  substrings while the real row is broken also fails closed… no: it *passes*
  while the real row is wrong. Either way the check is shape-only. MED.
- Also: `row`/`entry` checks run even when earlier arms failed — fine — but on
  the `tool_absent` early-return path (line 69) the flags print `ok`/`voted0`
  for arms never executed (see reporting note below).

## Bypass constructions

### Bypass A — BYPASSED: junk entry + inverted row → `C2=met`
Fixture commit `f3279794c3f53bbca1eb56f52631bbda55fc5d53` on top of freeze tip:
`vote-binding-r56.md` replaced with a one-line junk file still containing the
two substrings; the S545 row rewritten to explicitly `unmined` status, `not-`
prefixed date, and `withdrawn` recheck — while keeping `mined`, `2026-10-27`,
and the entry path as substrings.

```
$ python3 count-c2.py f3279794… --repo $FIXTURE
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=f3279794…
exit=0
```

Predicate's entry/row *intent* (a real knowledge entry; a mined S545 row citing
the entry) is false; the counter reports met. Data-level, reachable by the L1's
own editing path.

### Bypass B — BYPASSED: contrast confounded by deleted vote files → `C2=met`
Fixture commit `eadcbfe57182a6955c5925c79bb0dfad5fda48f2`: `git rm -r
.ufo/waves/round-55/w1/` (all 64 voter `.md` files), `results.json` untouched.

```
$ python3 .ufo/waves/round-55/count-c1.py eadcbfe5… --repo $FIXTURE
C1=unmet … voted=0 dissent=0 … failed=votes          # exit=1 — byte-identical fields to baseline
$ python3 count-c2.py eadcbfe5… --repo $FIXTURE
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok …
exit=0
```

The new binder still binds 15 voters from `results.json` (it never read the
`.md` files), while the r55 counter now finds zero voter files — `voted=0` for
an input-absence reason, and the contrast arm accepts it identically. The arm's
claimed evidence ("the binding shape is the whole difference") is not what it
measures.

### Bypass C — BYPASSED: ambient `sitecustomize` flips unmet→met → `C2=met`
Fixture commit `5a131c8f5e1ec44ac11244ae08cd8cc4dd3d581a`: all 64 voter outputs
blanked. The *real* pinned tool on these bytes:

```
TALLY rows=78 agree=0 double=0 single=0 zero=78 dissent=0 voters=48 bound_voters=0   # exit=0
```

The counter's arms run `python3` subprocesses inheriting the environment with
no isolation (`env=None`, no `-I`/`-S`, line 62). With
`PYTHONPATH=$SCRATCH/inject` containing a 4-line `sitecustomize.py` that prints
the four expected substrings:

```
$ PYTHONPATH=$SCRATCH/inject python3 count-c2.py 5a131c8f… --repo $FIXTURE
VOTE_BIND_SELFTEST pass=16 fail=0            ← injected, runs in every subprocess
TALLY rows=78 agree=78 … bound_voters=15     ← injected
zero=78 double=0                             ← injected
voted=0                                      ← injected
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=5a131c8f…
exit=0
```

Without injection the identical command exits 1 `failed=tally`. Every arm the
counter trusts is a substring match on ambient stdout — the byte-pin guards
tool bytes, not the stdout the verdict is computed from. Same-class
construction, demonstrated in miniature: a PATH-first fake `git` intercepting
`rev-parse --verify` makes the counter resolve a fabricated rev
(`rev=deadbeef…` in its own output, then `tool_absent`) — i.e., the
rev-resolution and object stream are also ambient-PATH trusted. HIGH as a
named limit (environment trust), LOW as a practical threat (requires a hostile
evaluation env; honest runs unaffected).

## Other observations

- Reporting: on early-exit paths (`tool_absent`, `r55_artifacts_absent`) the
  counter still prints `selftest=ok tally=ok control=ok contrast=voted0
  entry=ok row=ok` — "no recorded failure" rendered as "ok". A consumer parsing
  flags without `C2=`/`failed=` reads arms that never ran as passed. LOW
  (the `C2=` and `failed=` fields are correct).
- Temp hygiene: `tempfile.mkdtemp(prefix="mori-r56-c2-")` dirs are never
  removed — I accumulated 5 across 5 runs. LOW.
- No timeouts on any `subprocess.run` — a hung tool/counter hangs the counter
  indefinitely. LOW.
- `text=True` strict decode on `git show`/`run_in`: non-UTF-8 bytes in any
  fetched file or subprocess stdout raise `UnicodeDecodeError` (counter
  crashes, exit 1 — fails closed but unhandled). LOW.
- `rev-parse --verify` (no `^{commit}`): an annotated tag resolves to the tag
  object's SHA; `rev=` would stamp a tag SHA while `git show` reads through it.
  Cosmetic. LOW.
- TOCTOU, informational: materialized `results.json`/`ledger.md` in the
  0700 mkdtemp dir could be rewritten by a same-UID process between write and
  subprocess read. LOW.

## What held

- PIN enforced and correct; tool bytes pinned at freeze equal working tree.
- Tool prints the TALLY line exactly once on stdout, nothing on stderr — the
  substring check is currently exercised exactly as intended.
- The junk file is genuinely vote-free for this binder (no JSON parse, no verb
  token) — the control is honest at freeze.
- The contrast at the real freeze tip is genuine (`.md` files present; the
  bound-check grammar is the operative difference).
- Early `r55_artifacts_absent` return correctly fails closed.

## Findings

- **HIGH** — `count-c2.py:62,89-119`: all pass/fail decisions are substring
  matches on ambient subprocess stdout; executed arms inherit `PYTHONPATH`/env
  and `git` resolves via PATH. `sitecustomize` injection flips a genuinely
  unmet rev to `C2=met` (Bypass C); a PATH `git` shim resolves fabricated revs
  (same class). Routed round-57 item: isolate subprocess env or verify arm
  output structurally.
- **MED** — `count-c2.py:118-120` (contrast arm): accepts `voted=0` from any
  failure path including missing vote-file inputs; cannot distinguish
  grammar-contrast from input-absence (Bypass B). Routed item: additionally
  require `failed=votes` and presence of `.ufo/waves/round-55/w1/*.md` at R.
- **MED** — `count-c2.py:121-132` (entry/row): substring-only checks pass on
  semantically inverted/junk data (Bypass A). Data-correctable only in the
  sense that honest data happens to pass; the check itself cannot catch a bad
  entry/row. Routed item: cell-position-aware row parse; entry structure
  (source:/verified-at: headers) check.
- **LOW** — `count-c2.py:108`: control asserts `zero=78`+`double=0` (redundant
  second term) but not `bound_voters=0`/`voters=16`/`agree=0`; and only one
  junk shape is exercised (non-JSON no-verb prose). Routed item: assert the
  full junk line and add near-miss junk shapes.
- **LOW** — `count-c2.py:96,90`: `EXPECT_TALLY`/`EXPECT_SELFTEST` substring
  checks overmatch (prefix/duplicate lines pass) — sound while PIN holds;
  brittle if output shape ever widens.
- **LOW** — `count-c2.py:156-165`: unchecked arms report `ok`/`voted0` on
  `tool_absent`/`r55_artifacts_absent` early-return paths.
- **LOW** — hygiene: mkdtemp dirs never removed; no subprocess timeouts;
  strict UTF-8 decode can crash the counter unhandled; `^{commit}` missing on
  rev-parse.

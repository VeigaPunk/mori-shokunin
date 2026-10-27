# Mo56RevC1Counter — mechanism review of count-c1.py (false-green hunt)

Scope: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/count-c1.py`
(208 lines, freeze commit family; PIN `6b3dba74…e997` verified equal to
`sha256sum tools/mori-driver-liveness.py` at HEAD `acc62f54`). Leaf seat; all
experiments ran in a scratch git repo
`/fast/scratch/hyaku/mori-r56/Mo56RevC1Counter/fixrepo` (throwaway local
identity `seat@local.invalid`; `git rev-parse --show-toplevel` asserted =
scratch dir before first commit) containing byte-copies of the real tool,
fixtures, `corpus/knowledge/driver-liveness-r56.md` and `corpus/SOURCES.md`.
The lane repo was never mutated; only `git show/log/rev-parse/ls-tree`,
`checkout -- <path>` *inside the scratch repo*, and read-only host commands ran.
TMPDIR=`/fast/scratch/hyaku/mori-r56/Mo56RevC1Counter/tmp`.

Method note on the pin: every cheat tool changes the tool's sha256, so a
pristine counter correctly reports `failed=pins`. For each tool mutant I ran
two counters: (a) the pristine counter, to show which *behavioral* arms the
cheat defeats, and (b) a counter byte-identical except `PIN = <mutant sha>` —
simulating "the cheat is the frozen tool" — to show whether any behavioral arm
would still catch it. This isolates arm soundness from the pin. The pin is a
sha256 over `git show rev:path` text-decoded content, i.e. over the whole file
(full-file scope confirmed; it is not a hash of a subset).

## Baseline (sanity)

```
$ git -C fixrepo init …; commit baseline (real files) → 8121be6d
$ python3 count-c1.py HEAD --repo fixrepo
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8121be6d45ae55674af8d088dbbd09035b1433cc
exit=0
```
The scratch copy reproduces the freeze receipt, so arm behavior is comparable.

## Construction A — non-parsing tool (selftest substring + fixture hardcoding)

Mutant (`fixrepo@56baf82`, tool sha `d4e467c4…efac4`): `--selftest` prints
`"DRIVER_LIVENESS_SELFTEST pass=3 fail=10 skipped=0 note: DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0"`
plus a stderr warning, rc 0. `--fixture` never opens `watchdog.log`
(`grep -c 'open(' tool = 0`); it prints
`{"verdict":"DRIVER_LIVENESS_OK","log":{"malformed": FIX[basename(dir)]}}` —
the expected malformed count keyed by fixture directory name. Live mode raises
`RuntimeError("probe broken")`.

```
$ python3 count-c1.py 56baf82 --repo fixrepo            # pristine counter
C1=unmet selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=56baf82… failed=pins
exit=1
$ python3 count-c1-pinA.py 56baf82 --repo fixrepo       # PIN = mutant sha
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=56baf82…
exit=0
$ python3 mutA-tool --log <real fixture watchdog.log>
RuntimeError: probe broken: no parser present
```

Verdict: BYPASSED. Three mechanisms demonstrated: (1) `EXPECT_SELFTEST not in
out` is a substring check — the expected line merely has to appear in stdout,
surrounded by contradicting counts (`pass=3 fail=10`), with stderr ignored;
(2) the fixture arm reads only `verdict` and `log.malformed` — a lookup table
keyed by the fixture directory's basename satisfies all nine fixtures while
the log file is never opened; (3) nothing else exercises the parse path, so a
tool whose live mode is unconditionally broken still certifies. The pin is the
sole guard, and it binds identity, not behavior — a frozen but dishonest tool
passes vacuously.

## Construction B — norem arm (production-section split + wordlist)

The arm scans `tool_src.split("# selftest", 1)[0].lower()` for
`("healthy","unhealthy","failed lane","is stuck","wedged")`. The real tool's
first `# selftest` marker is line 248; the notes list (line ~239) precedes it.

B1 — early marker (`fixrepo@26e38a3`, sha `6944f29a…5046c`): inserted
`# selftest` at line 47 and appended `"lane is stuck"` (a word ON the counter's
list) to the emitted `notes`. The counter's scan now covers only lines 1–46.
The tool's own `t_no_health_verdict` checks only
`healthy/unhealthy/failed lane` in the JSON output — `is stuck` is not
checked — so its selftest stayed green:

```
$ python3 count-c1-pinB1.py 26e38a3 --repo fixrepo
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=26e38a3…
exit=0
$ python3 tool --fixture in-flight | grep -n 'is stuck'
29:  "lane is stuck (mutB1: emitted verdict, on counter HEALTH_WORDS)"
```

B2 — off-list synonym (`fixrepo@fc90e52`, sha `9c27dd3a…a41b0`): appended
`"lane is dead"` to `notes`, real marker position unchanged → the word sits in
the scanned prefix but is not on the list:

```
$ python3 count-c1-pinB2.py fc90e52 --repo fixrepo
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=fc90e52…
exit=0
```

Verdict: BYPASSED (both variants). The `split("# selftest")` boundary is
positional and trivially movable; the wordlist is closed-world (misses
`lane is dead`, `stalled`, `hung`, and anything runtime-constructed like
`"un"+"healthy"` — the arm is a source grep, never an output check). The
tool's own `t_no_health_verdict` and the counter's list have *different*
coverage (`is stuck`, `wedged` are counter-only; both checks miss synonyms).

## Construction C — registry row and entry arms

C1 — substring status (`fixrepo@bad30ae`, tool reverted to real → pristine
counter, pin intact): changed S544's status cell `| mined |` → `| determined |`.

```
$ python3 count-c1.py bad30ae --repo fixrepo
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=bad30ae…
exit=0
```
`"mined" in row` is satisfied because "determined" ends in "mined"
(`undermined`, `remined` likewise).

C2 — first-match shadow row + stub entry (`fixrepo@ce3f6f1`): inserted a
planted row `| S544 | SHADOW ROW … | mined | 2026-10-27 | … |
corpus/knowledge/driver-liveness-r56.md |` *above* the real row, then demoted
the real row's status to `| queued |`, and replaced the entry file with the
two-line stub `# stub entry\nS544 tools/mori-driver-liveness.py\n`:

```
$ python3 count-c1.py ce3f6f1 --repo fixrepo
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=ce3f6f1…
exit=0
```
The row loop `break`s on the first regex match (`^ {0,3}\|\s*S544\s*\|`), so a
fully-formed decoy satisfies `mined`, `2026-10-27`, and the entry-path
substring while the real S544 row is unmined. The entry arm is two
substring checks — a comment/stub satisfies it; no content requirement.

Verdict: BYPASSED (both). Row checks are line-level substring tests over the
first matching row only; entry is a mention check.

## Construction D — fixture enumeration vs the contract

The contract says the tool prints a passing report "for every fixture
subdirectory that carries a watchdog.log". The counter iterates `EXPECT_FIX`'s
nine names only. `fixrepo@3f0b3ed` added
`fixtures/driver/rogue-unexpected/watchdog.log` (999 unparseable lines):

```
$ python3 count-c1.py 3f0b3ed --repo fixrepo
C1=met … rev=3f0b3ed…   exit=0
$ python3 tool --fixture fixtures/driver/rogue-unexpected   # real tool
malformed= 999  verdict= DRIVER_LIVENESS_OK
```
BYPASSED as specified: an unlisted fixture dir carrying a watchdog.log is
never exercised, so the counter under-implements the contract's "every
subdirectory" wording. (Today the dir set matches EXPECT_FIX; this is a
forward-looking gap, not a landed error.)

## Construction E — unguarded subscript (robustness, not a green)

`fixrepo@fa3ab63`: `--fixture` prints `{"verdict":"DRIVER_LIVENESS_OK"}` with
no `log` key. `doc["log"]["malformed"]` raises:

```
KeyError: 'log'   File "count-c1.py", line 146, in evaluate
exit=1   (traceback on stderr; NO C1= verdict line printed)
```
KILLED for false-green purposes (it fails, loudly) — but a verdict-less crash
is a worse failure mode than `C1=unmet failed=fixtures`.

## Additional observations (verified by reading, not rerun)

- `failed=pins` prints all five flags `ok`; only the `failed=` tail reveals
  the kill (see mutA run). Flags-only scrapers misread.
- `--repo` accepts any path; the counter happily prints
  `C1=met rev=<sha-that-exists-only-in-scratch>` — every receipt line above
  demonstrates this. The `rev=` field is the binding; consumers must verify it
  against the lane repo (the freeze receipt does stamp the lane rev).
- `git_ls()` is defined and never called (dead code).
- `materialize_fixtures` writes fixture blobs via `git show` text mode; CRLF
  or non-UTF-8 fixture bytes would be silently normalized before the probe
  sees them (current fixtures are clean LF — verified by parse equality).
- The sha computed by `sha(tool_src)` is over text-decoded content
  (utf-8/surrogateescape re-encode), not the raw blob; for the current ASCII
  tool it equals `sha256sum` (verified `6b3dba74…` == PIN), but a future
  non-UTF-8/CRLF tool would pin-fail while `sha256sum` on disk matched.
- `--selftest` in the counter prints `C1_COUNTER_SELFTEST` and never touches
  git — it sanity-checks `EXPECT_FIX`/`EXPECT_SELFTEST` literals only.

## Findings

- HIGH — count-c1.py:124-148 (selftest + fixture arms): certification is
  tool-identity (pin) plus tool self-report. A tool that never parses a log
  passes every behavioral flag via (a) a substring selftest line and (b) a
  fixture-name→malformed lookup table (Construction A: `C1=met` under
  pin-simulation; `failed=pins` alone under the real pin). If the pinned tool
  were ever itself the cheat, no arm would catch it. Routed item for round
  57: assert on independent ground (e.g. counter-side re-parse of one fixture,
  or a do-nothing control fixture that must NOT print `pass=13 fail=0`),
  and make the selftest match line-anchored, not substring.
- MED — count-c1.py:153-154 (norem arm): `split("# selftest",1)[0]` lets a
  marker truncate the scanned region — an on-list verdict word (`is stuck`)
  emitted in tool output is invisible (mutB1 `C1=met`); off-list synonyms
  (`lane is dead`) and runtime-constructed words escape regardless of
  position (mutB2 `C1=met`). The arm greps source, never output.
- MED — count-c1.py:149-152 (row arm): first-match-wins plus substring tests —
  status `determined` satisfies `mined` (mutC1 `C1=met`); a shadow `| S544 |`
  row above the real row satisfies the whole arm while the real row is
  `queued` (mutC2 `C1=met`); `2026-10-27`/entry-path are also
  anywhere-in-line. Entry arm (line 149) is a two-substring mention check — a
  stub file passes (mutC2).
- MED — count-c1.py:134-147 vs contract wording: fixture arm enumerates
  `EXPECT_FIX` names, not "every fixture subdirectory that carries a
  watchdog.log"; extra dirs are silently unchecked (mutD `C1=met` with an
  unlisted 999-malformed fixture).
- LOW — count-c1.py:146: `doc["log"]["malformed"]` unguarded → KeyError
  traceback, no verdict line (mutE). Fail-loud; should be `:nojson`-style
  `:badshape` failure.
- LOW — count-c1.py:188-196: `pins` failure leaves all flags `ok`;
  `git_ls()` dead; `--repo` unanchored (rev is the only binding); pin hash is
  over text-decoded, not raw, bytes.

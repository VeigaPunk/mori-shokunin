# Mo56LabBinder — empirical probe of the round-56 dual-shape vote binder

**Seat:** Mo56LabBinder (labrat, w1, round 56) · **Lane:** mori-shokunin
**Subject under test:** `tools/mori-vote-bind.py` @ freeze tip `8be2717b0809281d07dffe83dad424a4859e0747`
(sha256 `8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca`, equal to `PIN` in
`.ufo/waves/round-56/count-c2.py:45`; verified equal to the working-tree blob).
**Method:** 12 mandated synthetic captured-output shapes + 30 adjacent shapes, driven through the
**CLI** `extract` (not only in-process), plus a synthetic ledger/results pair for `tally`, plus the
committed round-55 artifacts for the frozen roster. All reads; no fleet-repo mutation.
**Scratch:** `/fast/scratch/hyaku/mori-r56/Mo56LabBinder/` (`TMPDIR` set into it; removed on finish).

---

## 1. Verdict on the frozen claim

**The frozen C2 predicate holds on the bytes it names.** Independent re-run of the frozen counter:

```
$ python3 .ufo/waves/round-56/count-c2.py 8be2717b          # cwd = mori-shokunin
rc=0  C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
$ python3 .ufo/waves/round-56/count-c2.py 5b295eee
rc=1  C2=unmet … failed=tool_absent
$ python3 .ufo/waves/round-56/count-c2.py HEAD
rc=0  C2=met … rev=acc62f54fb0f53b47b428594dc27365150cbd76b
$ python3 tools/mori-vote-bind.py --selftest
rc=0  VOTE_BIND_SELFTEST pass=16 fail=0
```

The frozen tally line reproduces **byte-exactly** from the committed artifacts under the frozen
roster, and the 12 mandated shapes produce **0 mismatches** against the frozen grammar:

```
$ python3 tools/mori-vote-bind.py tally --ledger <r55 ledger> --results <r55 results> \
      --verb RECHECK --voter Mo55Rc01 … --voter Mo55Rc16
TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15
frozen EXPECT_TALLY match: True
```

**The 12 mandated shapes — bound / not-bound against the frozen grammar:**

| # | shape | channel | bound? | frozen grammar says | match |
|---|---|---|---|---|---|
| 1 | compact JSON array | json | bound | bound | OK |
| 2 | pretty-printed JSON | json | bound | bound | OK |
| 3 | JSON `vote_lines` nested 3 deep | json | bound | bound | OK |
| 4 | JSON string doc | json | bound | bound | OK |
| 5 | plain unfenced | text | bound | bound | OK |
| 6 | fenced | text | not-bound | not-bound | OK |
| 7 | prose-mention | text | not-bound | not-bound | OK |
| 8 | mixed prose+vote | text | bound | bound | OK |
| 9 | vote with trailing spaces | text | bound | bound | OK |
| 10 | CRLF line endings | text | bound | bound | OK |
| 11 | JSON array, leading newline in the scalar | json | bound | bound | OK |
| 12 | unicode escape in the hash | json | bound | bound | OK |

**0 mismatches. No crash on any of the 12.** The mandated shape space is clean.

All findings below are in the **adjacent** shape space, i.e. shapes the 12 do not cover. They do
not falsify the frozen claim; they are named limits for round 57 and two genuine crashes.

---

## 2. Crashes (HIGH)

### 2.1 HIGH — `extract` crashes with `UnicodeEncodeError` on a raw invalid-UTF-8 byte inside a bound vote

The reader is `errors="surrogateescape"` (`tools/mori-vote-bind.py:426`), so an invalid byte
becomes a lone surrogate that survives into `rest`, and the printer at
`tools/mori-vote-bind.py:435` writes it to a UTF-8 stdout with no error handling:

```
$ printf 'RECHECK aaaaaaaaaaaa holds \xff\n' > bad.bin     # raw 0xff, not UTF-8
$ python3 tools/mori-vote-bind.py extract bad.bin
rc=1  stdout=''
UnicodeEncodeError: 'utf-8' codec can't encode character '\udcff' in position 37: surrogates not allowed
  File ".../tools/mori-vote-bind.py", line 435, in main
    print("VOTE %s %s %s %s %s" % (verb, h, v["word"], v["channel"], v["rest"]))
```

Control: the same bytes encoded as valid UTF-8 (`\xc3\xbf`) do **not** crash — `rc=0`, one `VOTE`
line. So the crash is specific to undecodable bytes, not to the payload.

Two aggravating facts, both measured:

* **Earlier votes in the same run are lost.** With two *distinct* hashes where only the second
  carries the bad byte, stdout contained the first vote and then died — the offending vote and
  every vote after it are never printed, and the process exits 1 rather than the documented
  `exit 2 on usage/setup`.
* **The `tally` path does not crash** (it never prints vote text), so this is scoped to the
  `extract` CLI. Measured: `tally` over a results file whose output carries the raw `0xff`
  returns `rc=0  TALLY rows=1 agree=1 …`. The `read_results` call also survives it.

Root cause is one line: the printer emits `rest` unescaped onto a strict-UTF-8 stdout while the
reader deliberately admits undecodable bytes. Round-57 item: encode the surrogate (or use
`repr`) on the print path, or make `extract` reject the file with `VOTE_BIND_SETUP` + exit 2.

### 2.2 HIGH — a deeply nested JSON seat output kills the whole-wave tally

`_walk_strings` (`tools/mori-vote-bind.py:68-77`) recurses once per nesting level with no depth
bound; `json.loads` is not the limiter (it survives to depth 3000 on this host).

```
$ python3 tools/mori-vote-bind.py extract deep.json     # "["*997 + "]"*997
rc=1  stdout=''
RecursionError: maximum recursion depth exceeded
  File ".../tools/mori-vote-bind.py", line 73, in _walk_strings
    _walk_strings(x, acc)
```

Exact threshold: depth **996 → rc=0**, depth **997 → rc=1**. `json.loads` succeeds at every depth
tested (990…3000); the stack blows in `_walk_strings`.

Impact is wave-wide, not per-voter: `tally` walks every voter's output in one process, so a
single pathological seat output kills the tally for the whole wave and **no `TALLY` line is
printed at all**:

```
$ python3 tools/mori-vote-bind.py tally --ledger led.md --results res.json --verb RECHECK
rc=1  stdout=''      # 2 healthy voters + 1 1200-deep voter
RecursionError: maximum recursion depth exceeded
```

Two good voters' votes die with it. Fail-closed (a red, not a false green), so the frozen
predicate is not at risk — but the round's own C2 arm can be reddened by one seat's output.
Round-57 item: bound the walk depth, or catch `RecursionError` in `extract_votes` and count an
`unparsable_output` bucket instead of aborting the run.

---

## 3. Named limits in the adjacent shape space (not crashes)

### 3.1 MED — the JSON channel silently drops a vote scalar that carries two or more trailing lines

`VOTE_RE`'s `rest` group is `(?:\s(.*))?$` with **no** `DOTALL` and **no** `MULTILINE`
(`tools/mori-vote-bind.py:64`), so `rest` cannot cross a newline and the `$` anchor rejects the
whole scalar when a second newline is present. Measured on the JSON channel:

| scalar | binds? |
|---|---|
| vote line alone | bound |
| vote line + 1 trailing line | bound (`rest` swallows the next line) |
| vote line + 2 trailing lines | **not bound** |
| vote line + blank line + 1 line | **not bound** |

The same bytes in the text channel bind at every trailing-line count (the text path is
line-wise). So the binding outcome is **channel-dependent for identical content** — which is the
round-55 failure class in a narrower form. The docstring at
`tools/mori-vote-bind.py:22-25` promises `rest := free text (ignored by the tally; recorded for
audit)`; "free text" that contains a newline does not parse.

Visible in a tally:

```
exact-line scalar          -> TALLY rows=1 agree=1 double=1 single=0 zero=0 voters=2 bound_voters=2
scalar + 2 trailing lines  -> TALLY rows=1 agree=1 double=0 single=1 zero=0 voters=2 bound_voters=1
```

The frozen round-55 tally is **unaffected**: all 15 bound voters carry their votes in
single-line scalars (measured — every vote scalar in the committed `w1-results.json` is an
exact-line scalar; zero votes sit in a multi-line scalar). Round-57 item: decide the intended
semantics for a multi-line `rest` (the docstring says "free text"; the regex says otherwise)
and align the two.

### 3.2 MED — the `ENTAIL` verb is extraction-only: the `ENTAIL` tally arm is unreachable code

`read_ledger` assigns a disposition **only** under the RECHECK verb
(`tools/mori-vote-bind.py:152`: `if verb == "RECHECK" and len(cells) >= 7:`). Definitive test on a
ledger with the *same 7-cell shape* as the RECHECK one and `entailed` in the disposition cell:

```
read_ledger(ledger, 'RECHECK') -> {'a6e5226259c9': 'entailed'}      # the cell IS there
read_ledger(ledger, 'ENTAIL')  -> {}                                # the guard rejects it

$ python3 tools/mori-vote-bind.py tally --ledger ent.md --results ent.json --verb ENTAIL
rc=0  TALLY rows=0 agree=0 double=0 single=0 zero=0 dissent=0 voters=1 bound_voters=1
$ python3 tools/mori-vote-bind.py extract ent.json
VOTE ENTAIL a6e5226259c9 entailed json
```

So the tool's second advertised verb parses and binds votes at the **extract** layer but its
**tally** layer reports a successful all-zero line (`rows=0`, exit 0) over any ledger. The
docstring at `tools/mori-vote-bind.py:140` asserts "ENTAIL tables share the same trailing shape
here" — no such table exists in `corpus/knowledge` at the freeze tip (measured: zero files with
hash rows and the token ENTAIL), so the assertion is untested. The frozen counter runs
`--verb RECHECK` only, so C2 is unaffected. Round-57 item: either wire the ENTAIL cell or refuse
the verb loudly instead of printing green zeros.

### 3.3 LOW — setup errors exit 0 with a plausible `TALLY` line, and a missing results file prints exactly the control's success line

The docstring (`tools/mori-vote-bind.py:52`) promises `exit 2 on usage/setup`. Measured over the
real 78-row ledger:

```
missing ledger      rc=0  TALLY rows=0 agree=0 double=0 single=0 zero=0 dissent=0 voters=1  bound_voters=1
missing results     rc=0  TALLY rows=78 agree=0 double=0 single=0 zero=78 dissent=0 voters=0 bound_voters=0
malformed results   rc=0  TALLY rows=78 agree=0 double=0 single=0 zero=78 dissent=0 voters=0 bound_voters=0
empty ledger file   rc=0  TALLY rows=0 … zero=0 … voters=1 bound_voters=1
```

The second and third lines are **character-for-character the counter's junk-control expectation**
(`zero=78`, `double=0`). An operator who passes a typo'd `--results` path sees the control's
success signature and can read it as "the votes were read and none matched". The frozen counter
constructs its own paths correctly and its **main** tally arm (`agree=78`) does catch a read
failure, so the predicate itself is sound; the exposure is to a human or agent reader of the
`TALLY` line. Round-57 item: exit 2 (or a distinct `SETUP` line) when an input file cannot be
read, and print `min`/roster sanity alongside the counts.

### 3.4 LOW — the text channel's literal-`\n` rewrite makes the overclaim guard channel-dependent

`tools/mori-vote-bind.py:97` rewrites the two-character sequence backslash-n into a real line
break before the line scan. The same prose sentence is therefore rejected in one channel and
bound in the other:

```
JSON channel, prose mention                    chan=json  bound=-      # rejected
text channel, prose mention                    chan=text  bound=-      # rejected
text channel, prose mention after a literal \n chan=text  bound=[RECHECK/a6e5226259c9]   # BOUND
```

The frozen grammar's own example ("the claim is RECHECK … holds today" is prose, not a vote) is
the thing that binds here. The tool's docstring says the text channel reads "the output … as
lines"; a literal backslash-n is not a line break, so this is more permissive than the
documented rule. Reachability is narrow (requires a literal backslash-n in a captured output),
and the same rewrite is what makes the malformed-JSON fallback case work — so it should be
reconciled rather than removed. Round-57 item: state the rewrite in the grammar, or restrict it
to the fallback path.

### 3.5 LOW — a UTF-8 BOM in a captured output defeats binding silently

```
UTF-8 BOM + plain vote line   rc=0  stdout=''
UTF-8 BOM + JSON doc          rc=0  stdout=''
```

The BOM makes `json.loads` fail (so the JSON channel is skipped) and U+FEFF is not removed by
`str.strip()`, so the first line no longer matches the anchored grammar. Exit 0, no output, no
diagnostic — the vote is simply not there. Round-57 item: strip a leading BOM.

### 3.6 LOW — the counter's junk-control arm cannot distinguish "no votes" from "no file"

Four different broken inputs to `tally` — a malformed results file, a wrong-shape results file
(`{name: output}` instead of `{"results": [...]}`), a missing results file, and a results file
whose outputs are empty strings — produce a line **identical** to the intended junk control:

```
TALLY rows=78 agree=0 double=0 single=0 zero=78 dissent=0 voters=16 bound_voters=0
```

The control's predicate (`zero=78` AND `double=0`) is therefore satisfied by an unreadable
input. The frozen counter's **main** arm independently requires `agree=78`, so a genuine read
failure still reds the claim; the control's marginal discriminating power is only over "the file
was read and its outputs carried no vote surface". Recorded as a limit of the frozen control, not
a change proposal.

---

## 4. Confirmed by me, already reported by sibling seats (no new item)

Measured here for completeness; listed so the L1 does not double-count them.

* `--min N` / `min_votes` is inert: `--min 1`, `--min 2`, `--min 3`, `--min 99` produce
  byte-identical `TALLY` lines over the real 78-row ledger; the classification is hardcoded at
  `len(words) == 1` / else (`tools/mori-vote-bind.py:184-192`) and the value is only echoed into
  the returned dict (`:202`). Concrete blocker on the planned ≥2-voters-per-row
  dispatch-coverage validator.
* The frozen `agree=78` is **68 rows with ≥2 agreeing voters plus 10 rows resting on a single
  voter's word** (recomputed independently over the committed artifacts: 68 double-agree, 10
  single-vote-agree, 0 unanimous-against-the-ledger rows). The 10 single-vote rows are
  `Mo55Rc13`'s assigned hashes whose paired seat `Mo55Rc14` bound nothing — its committed
  captured output is 1055 bytes of prose carrying no vote token at all, and no report file
  exists for it at the freeze tip. `bound_voters=15` is therefore honest, not a binder defect.
* The usage docstring advertises `[--disposition-cols N]`, which argparse does not define
  (`tools/mori-vote-bind.py:45` vs `:413-418`); passing it exits 2 with
  "unrecognized arguments".
* `dissent` counts disagreement *among bound voters*, not against the ledger disposition: two
  voters both saying `stale` on a `holds` row yields `double=1 agree=0 dissent=0` — a
  unanimous-but-wrong row is indistinguishable from a unanimous-and-right one in that field.

---

## 5. What I could not check (UNVERIFIED)

* Whether any *real* captured seat output in the fleet contains raw invalid UTF-8 bytes or
  ≥997-deep JSON. I did not scan other lanes' result files beyond the committed round-55
  artifact (out of this seat's scope); the round-55 bytes are clean on both axes.
* Whether the ENTAIL ledger cell index 6 is the correct column for a future entailment ledger —
  no ENTAIL ledger exists in `corpus/knowledge` at the freeze tip to calibrate against.
* Whether the deeper JSON channel's intended semantics for a multi-line `rest` is "reject the
  scalar" or "take the first line". The tool's docstring and its regex disagree, and the docstring
  is the one I judged by; I did not find an authoritative statement elsewhere.
* I did not measure the memory-amplification behaviour of `read_results`/`extract` on large
  inputs (a sibling seat covers that axis).

---

## 6. Tooling record

No tools installed or upgraded this run; no `pacman`, no `uv`, no `npm`. Everything used was
already present: `python3` 3.14.8, `git` (read-only), `sha256sum`. Locale `en_US.UTF-8`,
stdout encoding `utf-8`, `PYTHONIOENCODING` unset — the surrogate crash in §2.1 is therefore
reproducible on this host as written.

Scratch discipline: all fixtures under `/fast/scratch/hyaku/mori-r56/Mo56LabBinder/` with
`TMPDIR` pointed there; no `/tmp` path is cited as evidence; the scratch tree was removed on
finish. `disk-guard.sh status` was consulted before the run (584 GB free on `/fast/scratch/hyaku`,
no ENOSPC). No fixture git repository was created (no commits, no throwaway identity).

---

## Findings

| # | sev | finding | file / line |
|---|---|---|---|
| 1 | HIGH | `extract` crashes with `UnicodeEncodeError` (rc=1, traceback) when a captured output carries a raw invalid-UTF-8 byte inside a bound vote: the `surrogateescape` reader admits a lone surrogate into `rest` and the printer writes it to a strict UTF-8 stdout unescaped. Earlier votes in the same run are lost with it. Valid UTF-8 with the same payload does not crash; the `tally` path does not crash (it prints no vote text). | `tools/mori-vote-bind.py:426` (surrogateescape read), `:435` (unescaped print); docstring exit-code contract at `:52` |
| 2 | HIGH | A seat output that is a JSON document nested ≥997 levels deep raises an uncaught `RecursionError` (depth 996 → rc=0; 997 → rc=1; `json.loads` itself survives to 3000). Through `tally` it kills the whole wave's tally — no `TALLY` line is printed and every healthy voter's votes die with the pathological one. Fail-closed (red, not a false green); the frozen round-55 bytes are clean on this axis. | `tools/mori-vote-bind.py:68-77` (`_walk_strings` recursion), `:85` (`json.loads` not the limiter), `:161-203` (`tally` walks every voter in one process) |
| 3 | MED | The JSON channel silently drops a vote scalar carrying two or more trailing lines (the `rest` group `(?:\s(.*))?$` has no `DOTALL`/`MULTILINE`, so `rest` cannot cross a newline and the `$` anchor rejects the whole scalar). Identical bytes bind in the text channel at every trailing-line count, so the binding outcome is channel-dependent — the round-55 failure class in a narrower form. The frozen round-55 tally is unaffected (all 15 bound voters use exact-line scalars). | `tools/mori-vote-bind.py:64` (VOTE_RE), `:90-95` (JSON channel), `:22-25` (docstring "rest := free text") |
| 4 | MED | The `ENTAIL` verb is extraction-only: `read_ledger` assigns a disposition only under `verb == "RECHECK"`, so `tally --verb ENTAIL` over a well-formed 7-cell ledger prints a successful all-zero line (`rows=0`, rc 0) while `extract` binds the same ENTAIL votes. The docstring's claim that "ENTAIL tables share the same trailing shape" is untested — no ENTAIL ledger exists in `corpus/knowledge` at the freeze tip. The frozen counter runs RECHECK only, so C2 is unaffected. | `tools/mori-vote-bind.py:152` (verb guard), `:140` (docstring claim); `tools/mori-vote-bind.py:174-177` (extract parses ENTAIL) |
| 5 | LOW | Setup errors exit 0 with a plausible `TALLY` line instead of the documented exit 2: a missing/malformed/empty results file prints `TALLY rows=78 … zero=78 … double=0 …` — character-for-character the counter's junk-control success signature — and a missing ledger prints `rows=0`. The frozen counter's own main arm (`agree=78`) still catches a real read failure; the exposure is to a human or agent reader of the `TALLY` line. | `tools/mori-vote-bind.py:52` (docstring exit contract), `:140-158` (`read_ledger` swallows OSError), `:119-133` (`read_results` swallows OSError/ValueError), `:437-441` (tally always exits 0) |
| 6 | LOW | The text channel's literal-`\n` rewrite (`output.replace("\\n", "\n")`) makes the anchored-grammar overclaim guard channel-dependent: the frozen grammar's own prose example ("the claim is RECHECK … holds today") is rejected in the JSON channel but BOUND in the text channel when a literal backslash-n precedes it. The rewrite is load-bearing for the malformed-JSON fallback case, so it should be reconciled rather than removed. | `tools/mori-vote-bind.py:97` (the rewrite), `:103` (line match); grammar text at `:22-25` and `corpus/knowledge/vote-binding-r56.md` §"The frozen rule" |
| 7 | LOW | A UTF-8 BOM in a captured output defeats binding silently: the BOM makes `json.loads` fail (skipping the JSON channel) and U+FEFF survives `str.strip()`, so the first line no longer matches the anchored grammar. rc=0, no output, no diagnostic. | `tools/mori-vote-bind.py:85` (json.loads), `:91`/`:103` (`s.strip()` / `line.strip()`), `:426` (reader) |
| 8 | LOW | The frozen counter's junk-control arm cannot distinguish "the file was read and carried no vote surface" from "the file was unreadable": a malformed, wrong-shape, missing, or empty-output results file yields the identical `TALLY rows=78 … zero=78 … double=0 …` line the control expects. The counter's main arm (`agree=78`) independently catches a real read failure, so the predicate is sound; recorded as a limit of the frozen control, not a change proposal. | `.ufo/waves/round-56/count-c2.py:105-110` (control arm), `tools/mori-vote-bind.py:119-133` (`read_results` returns `{}` on any read/parse failure) |
| 9 | INFO | The 12 mandated synthetic shapes produce **0 mismatches** against the frozen grammar through the CLI, and the frozen `TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15` line reproduces byte-exactly from the committed artifacts. The mandated shape space is clean; every finding above lies in the adjacent shape space. | `tools/mori-vote-bind.py`; `.ufo/waves/round-56/count-c2.py:44-45` (EXPECT_TALLY) |
| 10 | INFO | `agree=78` is 68 rows with ≥2 agreeing voters plus 10 rows resting on a single voter's word (recomputed independently). The 10 single-vote rows are `Mo55Rc13`'s hashes whose paired seat `Mo55Rc14` bound nothing — its committed output is 1055 bytes of prose with no vote token and it has no report file at the freeze tip — so `bound_voters=15` is honest. Independently confirmed, not a new item. | `.ufo/waves/round-55/w1-results.json` (Mo55Rc13/Mo55Rc14 records); `tools/mori-vote-bind.py:161-203` |

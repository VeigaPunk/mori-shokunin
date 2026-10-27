# w1 — Mo56SecTools: security review of the two r56 parsers

Seat: Mo56SecTools (leaf, no subagents, no questions). Scope assigned: **untrusted-text security
review** of `tools/mori-driver-liveness.py` (C1) and `tools/mori-vote-bind.py` (C2) — regex
catastrophic backtracking, unbounded reads, `--log/--ledger/--results/--fixture` path handling,
execution (`eval`/`exec`/`os.system`) and tempfile usage. Detection and report only; no
remediation applied (the seat was not granted edit scope, and the counters/predicates are frozen).

Repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Lane HEAD at review time
`acc62f54fb0f53b47b428594dc27365150cbd76b` (moved past the freeze tip by sibling reports); all
reviewed bytes are the **frozen** bytes.

## 0. Byte identity of what was reviewed

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && sha256sum tools/mori-driver-liveness.py tools/mori-vote-bind.py
6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997  tools/mori-driver-liveness.py
8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca  tools/mori-vote-bind.py
                                                                    (exit 0)

$ git show 8be2717b0809281d07dffe83dad424a4859e0747:tools/<each>.py | sha256sum
6b3dba74c639...7be997  (driver-liveness, same hash)      (exit 0)
8be1acdb...6bca       (vote-bind, same hash)              (exit 0)
```

Both hashes equal the counters' frozen `PIN`s (`count-c1.py:46`, `count-c2.py:46`), so the working
tree, the freeze tip 8be2717b and the pinned bytes are one artifact: every finding below is a
property of the frozen tools, not of a working-tree drift. Sizes: 479 lines / 18,347 B and 447
lines / 16,432 B.

Tooling installs: **none** (`strace` and `jq` were already present; no pacman, no uv, no binary
added). Scratch: `/fast/scratch/hyaku/mori-r56/Mo56SecTools/` (created, used, removed; the
`disk-guard.sh status` read at start showed /fast/scratch/hyaku at 28% use, 583.9 G free).

## 1. Execution surface: nothing is executed

Static sweep for dynamic-execution and network primitives across both files (full output, not
elided):

```
$ grep -nE '"w"|'w'|eval|exec|__import__|system|popen|subprocess|socket|urllib|http|pickle|marshal|yaml|input\(|globals\(\)' \
      tools/mori-driver-liveness.py tools/mori-vote-bind.py
tools/mori-driver-liveness.py:354:    with open(p, "w") as fh:
tools/mori-vote-bind.py:336:    with open(ledger, "w") as f:
tools/mori-vote-bind.py:347:    with open(results, "w") as f:
tools/mori-vote-bind.py:366:    with open(ledger, "w") as f:
tools/mori-vote-bind.py:374:    with open(results, "w") as f:
                                                                    (exit 0)
```

No `eval`, `exec`, `__import__`, `os.system`, `subprocess`, `socket`, `urllib`, `http`, `pickle`,
`marshal`, `yaml`, `input()`. The five write-mode opens are all selftest fixtures; imports are
`argparse datetime json os re sys` (liveness) and `argparse hashlib json os re sys tempfile`
(vote-bind) only.

Syscall proof that the reporting paths never write (fresh fixture, read-only tree):

```
$ strace -f -o st_live.txt -e trace=openat,open,creat,unlink,unlinkat,rename,renameat,mkdir,mkdirat,write,truncate \
    python3 tools/mori-driver-liveness.py --fixture <scratch>/small --now 1800000000
$ grep -E 'O_WRONLY|O_RDWR|O_CREAT|creat\(|unlink|rename|mkdir|truncate' st_live.txt
(none)                                                    (trace_exit=0)

$ grep -E 'small/(watchdog\.log|state)' st_live.txt
openat(AT_FDCWD, ".../small/watchdog.log", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, ".../small/state", O_RDONLY|O_NONBLOCK|O_CLOEXEC|O_DIRECTORY) = 3
```

```
$ strace -f -o st_vb.txt -e trace=openat,open,creat,unlink,unlinkat,rename,renameat,mkdir,mkdirat,truncate \
    python3 tools/mori-vote-bind.py tally --ledger small/ledger.md --results small/results.json --verb RECHECK --voter V
TALLY rows=1 agree=1 double=0 single=1 zero=0 dissent=0 voters=1 bound_voters=1
$ grep -E 'O_WRONLY|O_RDWR|O_CREAT|creat\(|unlink|rename|mkdir|truncate' st_vb.txt
(none)
$ grep -E 'small/(ledger\.md|results\.json)' st_vb.txt
openat(AT_FDCWD, ".../small/ledger.md",    O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, ".../small/results.json", O_RDONLY|O_CLOEXEC) = 3
```

Both selftests write only inside their `mkdtemp` dir and clean up:

```
$ TMPDIR=<scratch>/tmp3 strace -f -o st_live_st.txt ... tools/mori-driver-liveness.py --selftest
DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0
$ grep -E 'O_WRONLY|O_RDWR|O_CREAT' st_live_st.txt | grep -v "$PWD/tmp3"
(liveness selftest: no write outside TMPDIR)
$ ls -A tmp3 | wc -l
0

$ TMPDIR=<scratch>/tmp2 strace -f ... tools/mori-vote-bind.py --selftest
VOTE_BIND_SELFTEST pass=16 fail=0
(no write outside TMPDIR)
```

Note: the input opens carry no `O_NOFOLLOW`, which is the mechanism behind finding F-5.
`hashlib` is imported in vote-bind and never used (dead import, cosmetic).

## 2. Regex battery: no catastrophic backtracking found

Every pattern in both files matched against pathological inputs (2,000 nested brackets/parens,
10k/20k single tokens, 20k space runs, alternating quotes, unterminated `(` trains, unclosed
`(.*)` rests, 5k repeated ` mission=` chains). Worst observed absolute cost in the battery was
**< 5 ms**; nothing exceeded the 5 ms print threshold, so the battery printed only its header
(`battery done`, exit 0). Then a slope test, 250k → 1M → 4M characters per pattern:

```
case                                      n         ms   ms/n(us)  growth
VOTE_RE spaces                      4000000      26.75      0.007  x16.3 over 16x input
VOTE_RE rest greedy                 4000000       0.75      0.000  x15.3 over 16x input
VOTE_RE rest parens unclosed        4000000       0.85      0.000  x17.7 over 16x input
DEAD_RE paren train                 4000000      19.74      0.005  x14.6 over 16x input
DEAD_RE paren pairs                 4000000       0.75      0.000  x15.2 over 16x input
LAUNCH_RE pgid digits trailing      4000000     276.41      0.069  x16.1 over 16x input
LAUNCH_RE driver tok trailing       4000000     232.95      0.058  x16.0 over 16x input
LAUNCH_RE mission tok trailing      4000000      49.69      0.012  x16.5 over 16x input
LINE_RE nonspace token              4000000      15.94      0.004  x17.0 over 16x input
LINE_RE digits tail                 4000000       5.21      0.001  x18.3 over 16x input
LEDGER_RE spaces                    4000000       5.42      0.001  x17.3 over 16x input
                                                                    (exit 0)
```

Growth ≈ ×16 for ×16 input on every pattern ⇒ **linear**; the ~1.1 ms/MB worst case
(`LAUNCH_REST_RE` with a trailing space after a 4 MB token) is throughput, not backtracking.
`VOTE_RE`, `LINE_RE`, `LAUNCH_REST_RE`'s optional-prefix chain, `DEAD_REST_RE`'s
`(?: \((.*)\))?$`, `FENCE_RE` and the ledger row regex are all free of nested quantifiers over a
shared character class. **No ReDoS rating** for either tool. (Constant-factor note for the L1,
not a security item: a 256 MB single line costs ~1 s of matching, see F-3.)

## 3. Unbounded reads: no cap, 3–9× memory amplification

Neither tool has a max-bytes/line cap. `mori-driver-liveness.py:run()` does
`f.read()` on the whole log (line 219-ish), `mori-vote-bind.py:main()` `extract` does `f.read()`
(whole file), `read_results()` does `json.load(f)` (whole document), and `_walk_strings` materialises
every string scalar of that document. Measured on 256 MB inputs (peak RSS of the child, one child
per measurement):

```
liveness-nul       rc=0  wall=1.03s  child_peak_rss=2319 MB    # 256 MB, no newline (one giant line)
liveness-flood     rc=0  wall=9.68s  child_peak_rss=1124 MB    # 256 MB, 4,628,197 launch lines
votebind-extract   rc=0  wall=0.91s  child_peak_rss= 809 MB    # 256 MB text, 0 votes
                                                                    (exit 0)
```

⇒ ~**9×** amplification for a newline-free file (2.3 GB RSS from a 256 MB file) and ~**3–4×** for
realistic line-shaped input. Live input (`text.split("\n")` materialises the whole line list)
also has no per-line length cap, so one 256 MB line allocates one 256 MB string plus its
decode/`split` copies before any cap could fire. Today's real inputs are small — the shared fleet
log is 163,775 B / 1,730 lines and the largest committed `w1-results.json` is 389,180 B
(`round-53`) — so this is **latent**, but both inputs are multi-writer: every lane's driver
appends to `.ufo/watchdog.log`, and every seat contributes to `w1-results.json`.

Live-log behaviour at current size (for contrast with the 256 MB figures):

```
$ time python3 tools/mori-driver-liveness.py --log /home/vgpnk/Projects/shokunin/.ufo/watchdog.log --now 1800000000
real 0m0.031s   (exit 0)   lines=1730 malformed=0 other_lines=121 lanes=23 verdict=DRIVER_LIVENESS_OK
```

## 4. Parser complexity on untrusted log text: quadratic `close_round`

`parse_log` keeps `row["open_launches"]` as a **list** and `close_round()` tests
`if key in row["open_launches"]` / `elif (int(round_s), None) in row["open_launches"]` per
complete/wrap line. With many launches for one (lane, round) and completes whose attempt never
matches, every complete scans the whole list. Measured (n launches with unique attempts, then n
completes with non-matching attempts):

```
n      bytes      secs     unclosed
1000   133780     0.024    1000      growth -
2000   269780     0.070    2000      growth x2.9
4000   541780     0.224    4000      growth x3.2
8000   1085780    0.880    8000      growth x3.9
16000  2185780    3.509    16000     growth x4.0
                                                                    (exit 0)
```

×4 time per ×2 input ⇒ O(n²). A 2.1 MB crafted log already costs 3.5 s; ~100 MB would cost hours.
The launcher is the shared multi-writer `.ufo/watchdog.log`, and the pattern is reachable with
plain, grammar-valid lines (no malformed trick needed): `launch ... round=1 attempt=<unique>`
repeated, then `complete ... round=1; hyaku-inline attempt=<never-used>` repeated. The matching
happy path is linear (`pairs=8000 → 0.033 s`), so this is a crafted-input cliff, not steady-state
cost. `row["rounds"]` (a set) and the per-lane row count are likewise uncapped.

## 5. Crash surfaces: two uncaught exceptions from untrusted text

**(a) `int()` digit limit.** `parse_log` calls `int(round_s)` and `int(m2.group(4))` on regex
`(\d+)` groups. CPython 3.14 refuses `int()` on >4,300 digits; the `ValueError` is not caught
anywhere in `parse_log`/`run`/`main`, so the reader aborts with **no output at all** (not even the
documented `DRIVER_LIVENESS_UNAVAILABLE`, and not the documented rc 0/2 — it returns 1):

```
$ python3 tools/mori-driver-liveness.py --log digits.log --now 1800000000
5000-digit round= :  rc=1 stdout_bytes=0
stderr tail: ValueError: Exceeds the limit (4300 digits) for integer string conversion: value has 5000 digits; use sys.set_int_max_str_digits() to increase the limit

5000-digit attempt=: rc=1 stdout_bytes=0
stderr tail: ValueError: Exceeds the limit (4300 digits) ... value has 5000 digits

200k-char ts token : rc=0 stdout_bytes=736      # timestamps are safe: parse_ts catches ValueError
                                                                    (exit 0)
```

One such line in the shared log disables the fleet liveness reader for every lane, and the failure
mode is a traceback rather than the tool's own `unavailable` verdict.

**(b) JSON recursion depth.** `extract_votes` guards only `(ValueError, TypeError)` around
`json.loads`, and `_walk_strings` is recursive with no depth bound. A deeply nested (but
otherwise well-formed) seat output raises `RecursionError` out of `final_votes` → `tally`, killing
the whole tally:

```
$ python3 tools/mori-vote-bind.py tally --ledger led.md --results deep_results.json --verb RECHECK
Traceback (most recent call last):
  ...
  File "tools/mori-vote-bind.py", line 85, in extract_votes
    doc = json.loads(output)
RecursionError: Stack overflow (used 8144 kB) while decoding a JSON array from a unicode string
                                                                    (exit 1)
```

The crafted document was `{"results":[{"name":"V","output":"[["…200,000 deep…"]]"}]}` (400,038 B).
Any one seat can emit such an output; the tally then prints no `TALLY` line for the wave.
`read_results()` has the same shape of hole (`json.load` on the results file itself; only
`OSError/ValueError/TypeError` are caught).

Impact is bounded by the counters, which are fail-closed: `count-c2.py:evaluate` rejects on
`p.returncode != 0` before looking for the expected `TALLY` line
(`if p.returncode != 0 or EXPECT_TALLY not in p.stdout: failed.append("tally")`), and
`count-c1.py` likewise on `rc != 0`. So neither crash can produce a **false green**; both produce
a false red / dead reader. `count-c1.py` only runs the tool over frozen fixtures (its only real-log
free path), so the C1 counter itself is not exposed to F-3/F-4; `count-c2.py` is exposed to F-6(b)
through the committed `w1-results.json` if that file ever carries such an output.

## 6. Path handling: no confinement, symlinks followed, fixture symlink is contained

The tools run as the calling user and open everything `O_RDONLY` (section 1), so there is **no
privilege boundary to cross**; the findings below are about what the reader will accept as input,
not about escalation.

- **Arbitrary path / traversal accepted** (`--log`, `--state-dir`, `--fixture`, `--ledger`,
  `--results`). `--fixture` is joined, not confined: absolute override and `../..` both work.

  ```
  $ python3 tools/mori-driver-liveness.py --fixture /etc --now 1800000000
  "log": { "path": "/etc/watchdog.log", "state": "absent" }, "rc": 2      (exit 0)
  $ python3 tools/mori-driver-liveness.py --fixture '../../../..' --now 1800000000
  "log": { "path": "../../../../watchdog.log", "state": "absent" }, "rc": 2   (exit 0)
  ```
- **Symlinks are followed** on `--log` (no `O_NOFOLLOW`, `os.path.isfile` follows). Demonstrated
  with no privilege needed: a symlink whose target is a non-log file is read, and the first 120
  bytes of its first line are echoed into the JSON `examples` array:

  ```
  $ printf 'SECRET-TOKEN-ABCDEF0123456789 this line is not a log line\n' > secret.txt
  $ ln -sf "$PWD/secret.txt" link.log
  $ python3 tools/mori-driver-liveness.py --log "$PWD/link.log" --now 1800000000
  "examples": [ "SECRET-TOKEN-ABCDEF0123456789 this line is not a log line" ],
  "log": { "path": ".../link.log", ... }, "verdict": "DRIVER_LIVENESS_OK"    (exit 0)
  ```
- **`--state-dir` is listed but never followed per entry**: `state_shapes()` checks `islink`
  before `isfile`/`isdir` and counts only names ending `.round`; values are never read. A
  symlinked *directory* passed as `--state-dir` is itself followed (one level), and no entry
  content is read — consistent with the tool's claim.
- **The frozen fixture symlink is contained**: `.ufo/waves/round-56/fixtures/driver/state-shapes/state/kake.round`
  is git mode `120000` with target `mori.round` (relative, same dir), so the fixture tree cannot
  redirect the tool outside itself.
- Cross-coupling worth knowing: passing `--log` alone still defaults `state_dir` to
  `<root>/.ufo/state` (`state_dir = a.state_dir if a.state_dir is not None else os.path.join(root, ".ufo", "state")`),
  so the earlier symlink run also listed the fleet's real `.ufo/state` (`regular=21`). Reading one
  input silently also reads another location.
- Control characters in echoed `examples` are **not** a terminal-injection vector: the output is
  `json.dumps`-escaped. Verified with an ANSI/NUL probe: the JSON carried
  `"\u001b[2J\u001b[31mFAKE-ALERT\u001b[0m \u0007\u0000 not-a-log-line"` and strict `json.loads`
  accepted the document.

## 7. tempfile usage: unpredictable, 0700, but silently falls back to `/tmp`

`tempfile.mkdtemp(prefix="mori-…-", dir=os.environ.get("TMPDIR") or None)` is used in both
selftests and (same pattern) in both counters. `mkdtemp` uses `O_EXCL` + random suffix, so there
is no predictable-name or symlink-race surface:

```
mkdtemp dir: /tmp/mori-vote-bind-6p8ddna5
mode: 700
```

Files inside are created `0666 &~umask` within that 0700 dir (from the strace trace), which is
fine. The gap: when `TMPDIR` is unset the `or None` silently lands in `/tmp` rather than failing,
which contradicts the tool's own docstring line "TMPDIR/hyaku scratch only — never /tmp-hardcoded
(QUALITY 127)" and this wave's scratch directive:

```
$ env -u TMPDIR strace -f ... tools/mori-vote-bind.py --selftest
VOTE_BIND_SELFTEST pass=16 fail=0
openat(AT_FDCWD, "/tmp/mori-vote-bind-2uq30u3n/ledger.md",  O_WRONLY|O_CREAT|O_TRUNC|O_CLOEXEC, 0666) = 3
openat(AT_FDCWD, "/tmp/mori-vote-bind-2uq30u3n/results.json", O_WRONLY|O_CREAT|O_TRUNC|O_CLOEXEC, 0666) = 3
leftover_dirs=0
```

## 8. Integrity of untrusted records (binding semantics are other seats' ground; these are parse-width facts)

- **Silent row drop in the ledger.** `read_ledger` keeps a row only when the row regex matches
  (`^ {0,3}\|\s*` + exactly 12 hex + closing backtick) **and** the split yields ≥7 cells with a
  non-empty cell 6. Otherwise the hash simply does not exist for the tally — no counter, no
  diagnostic, and `rows=N` shrinks. Demonstrated with a 3-row ledger where one row has 6 cells and
  one carries a 15-hex hash:

  ```
  $ python3 tools/mori-vote-bind.py tally --ledger drop-ledger.md --results drop-results.json --verb RECHECK --voter V --voter W
  TALLY rows=1 agree=1 double=0 single=1 zero=0 dissent=0 voters=2 bound_voters=2     (exit 0)
  ```
  (3 ledger rows in, `rows=1`: the 6-cell row and the 15-hex row vanished silently.) Checked
  against the frozen ledger: `corpus/knowledge/kernel-v7.3-recheck-r55.md` has exactly **78** lines
  matching the row regex and **78** distinct 12-hex hashes, so the frozen `rows=78` is faithful
  today and **no dropped row is being counted** — the risk is latent, not active.
- **Duplicate keys last-win, silently.** Two rows for one hash: the later disposition wins; two
  results entries with one seat name: the later output wins and the earlier is discarded. Both
  verified (each case prints `agree=1` with the "later" word binding). No duplicate detection, so a
  mis-assembled ledger or results file can flip a disposition with no visible trace.
- **`--min` is a dead knob.** `min_votes` is parsed, defaulted to 2 and echoed into the result dict,
  but row classification uses `len(words)` (1 → single, ≥2 → double) and never consults it; the
  selftest's `min_votes=1/2` values have no effect. A caller who raises the bar with `--min 3`
  gets nothing.
- **Output amplification from untrusted names.** Lane names are `[A-Za-z0-9_-]+` and become JSON
  keys verbatim, with no length cap: 12.8 MB of distinct-lane lines produced **48.4 MB** of output
  (×3.8, 200,000 rows, 372 MB RSS), and a single 200 KB lane name is echoed verbatim (200,855 B of
  output from a 200,000 B input). This is the mirror of F-3 on the write side.
- **Ledger row length is uncapped** (`read_ledger` iterates `for line in f` — streaming, which is
  good, but `line.split("|")` on one 256 MB line is unbounded).

## 9. Named limits and routing (frozen predicates are not touched)

These are limits of the frozen v1 tools. I am **not** proposing counter/predicate edits; they belong
to round 57 as items, per the wave rules.

1. No input budget: no max-bytes for log/results/ledger, no per-line cap, no lane-name cap
   (F-3, F-9) → r57 item: byte/line/name ceilings with an explicit `truncated` field, so a cap
   never reads as "clean".
2. No record-integrity accounting in the binder: ledger rows that fail to parse are invisible
   (F-7) → r57 item: emit `ledger_rows_seen` / `ledger_rows_unparsed` beside `rows`, and fail the
   tally loudly when they differ. `mori-driver-liveness.py` already does exactly this for log lines
   (`lines/malformed/other_lines/examples`) — the asymmetry is the gap.
3. Error containment is per-line in neither tool: a single hostile numeric field or deeply nested
   document aborts the whole run (F-6) → r57 item: per-line `try/except ValueError` → `malformed`,
   and depth-bounded walking (or `RecursionError` in the caught tuple) with a counted
   `unparsable_output` instead of a traceback.
4. `close_round` list membership (F-4) → r57 item: keep `open_launches` keyed by
   `(round, attempt)` in a dict/set; the observable pairing counts do not change.
5. Symlink/echo policy (F-5) → r57 item: state whether the reader may follow symlinks on its input
   and whether `examples` should be redacted (line hashes instead of raw prefixes) before the
   output becomes committed evidence.
6. `--min` is dead (F-8) and tempfile falls back to `/tmp` (F-10) are v1 hygiene; either wire them
   or drop them from the interface/docstring.

## 10. What I could not check (UNVERIFIED)

- Whether any other lane's tooling consumes `mori-driver-liveness.py` output in a way that trusts
  `examples` verbatim (I read only the two tools and their two counters).
- Whether the orchestrator's harness caps `.ufo/watchdog.log` or the results files outside these
  tools; I did not read the harness.
- The counters' behaviour under a hung (not crashed) tool: `count-c1.py:run_tool` and
  `count-c2.py:run_in` call `subprocess.run` with **no `timeout=`**, so F-4 at large scale would
  hang the counter rather than fail it. I did not measure that path (both counters run the tools
  only over small frozen fixtures/artifacts, so the exposure today is the live reader, not the
  counters).
- Cross-lane effect on any session/agent: out of scope for a leaf seat (no steering, no kills).

## Findings

| # | Severity | Concern | File / line |
|---|---|---|---|
| F-1 | **MED** | Uncaught `int()` digit-limit `ValueError` on a >4,300-digit `round=`/`attempt=` token aborts the whole reader (rc 1, zero output, traceback) — one grammar-valid line in the shared multi-writer `.ufo/watchdog.log` disables fleet liveness reading for every lane; the tool's documented rc 0/2 contract and its `UNAVAILABLE` verdict are both bypassed. Not exploitable for a false green (counters require rc 0). | `tools/mori-driver-liveness.py:103` (`row["rounds"].add(int(round_s))`), `:110`/`:113` (`int(m2.group(4))`), `:127` (`int(round_s)`), uncaught through `:143-152` |
| F-2 | **MED** | Uncaught `RecursionError` on a deeply nested (400 KB) seat output kills the whole tally (rc 1, no `TALLY` line); any one seat can force the wave's C2 arm red. Fail-closed, so a false red, not a false green. `read_results` has the same hole. | `tools/mori-vote-bind.py:85` (`json.loads` guarded only by `ValueError/TypeError`), `:112-113`, `:71-79` (`_walk_strings` recursion), `:126-131` (`read_results`) |
| F-3 | **MED** | No max-bytes cap on any input; whole-file `read()` / `json.load()` with 3–9× memory amplification (256 MB → 2,318 MB RSS single-line; → 1,124 MB line-shaped; vote-bind extract → 809 MB). Latent (live log 163 KB, results ≤389 KB) but both inputs are multi-writer. | `tools/mori-driver-liveness.py:219-221` (`f.read()`), `:170` (`text.split("\n")`); `tools/mori-vote-bind.py:439` (`f.read()`), `:126-131` (`json.load`) |
| F-4 | **MED** | O(n²) `open_launches` list-membership scan per complete/wrap: 2.1 MB crafted-but-grammar-valid log → 3.5 s, ×4 per doubling (16k launches + 16k non-matching completes). Shared log ⇒ cross-lane hang of the reader. | `tools/mori-driver-liveness.py:99-105` (`close_round`, `key in row["open_launches"]`) |
| F-5 | **LOW** | Inputs opened without `O_NOFOLLOW`: a symlinked `--log` is followed and the first 120 bytes of the target's first line are echoed into `examples`, which becomes committed evidence — discloses prefixes of any readable file, and lets a log writer place text into another lane's evidence artifact. No privilege boundary (runs as caller). | `tools/mori-driver-liveness.py:204-216` (`os.path.isfile`/`open`, no `O_NOFOLLOW`), `:76-80` (`examples.append(raw[:120])`) |
| F-6 | **LOW** | `--fixture`/`--log`/`--state-dir`/`--ledger`/`--results` are unconfined (absolute paths and `../..` accepted; `--fixture /etc` → `/etc/watchdog.log`), and passing `--log` alone still reads the default `<root>/.ufo/state`. Read-only, same user, so no boundary crossed — but the docstring's "frozen synthetic tree" is unenforced. | `tools/mori-driver-liveness.py:450-462` (`main` join/default logic) |
| F-7 | **LOW** | Ledger rows that fail the row regex or yield <7 cells are dropped silently: `rows=N` shrinks with no `unparsed` counter (3-row probe printed `rows=1`). Frozen ledger verified faithful (78 matching rows = 78 distinct hashes = `rows=78`), so latent, not active. Duplicate ledger rows and duplicate result names also last-win silently. | `tools/mori-vote-bind.py:140-163` (`read_ledger`), `:117-124` (`read_results` dict overwrite), `:165+` (`tally`) |
| F-8 | **LOW** | `--min` is dead: parsed, defaulted, echoed into the result dict, never consulted by row classification — a caller raising the double-vote bar gets no effect. | `tools/mori-vote-bind.py:180` (`min_votes=2`), `:185-196` (`len(words)` classification), `:198` (echo only) |
| F-9 | **LOW** | Untrusted lane names become uncapped JSON keys: 12.8 MB input → 48.4 MB output (×3.8, 200k rows); a 200 KB lane name is echoed verbatim. Write-side mirror of F-3. | `tools/mori-driver-liveness.py:55` (`([A-Za-z0-9_-]+)`), `:164-176` (row emission) |
| F-10 | **LOW** | Tempfile silently falls back to `/tmp` when `TMPDIR` is unset (`or None`), contradicting the tool's "TMPDIR/hyaku scratch only — never /tmp-hardcoded" claim and this wave's scratch directive; same pattern in both counters. Names are `mkdtemp` random in a 0700 dir (no predictable-name/symlink-race issue). | `tools/mori-vote-bind.py:291,341,364`; `tools/mori-driver-liveness.py:350` |
| F-11 | **LOW** | `--now nan` / `inf` emits a bare `NaN`/`Infinity` token in the JSON (not RFC 8259). `jq` accepts it (`jq -e .` exit 0) and `json.loads` is tolerant, so interop impact is limited; `age`/`mtime_age_s` become non-numeric for consumers that do strict parsing. | `tools/mori-driver-liveness.py:139` (`round(now - ts)`), `:418` (`json.dumps` without `allow_nan=False`) |
| F-12 | **INFO** | Confirmed negative results: no `eval`/`exec`/`os.system`/`subprocess`/network primitives in either tool; input opens are `O_RDONLY` and the reporting paths issue **zero** write syscalls (strace); only selftest writes, inside `mkdtemp` under `TMPDIR`, zero leftovers. No catastrophic regex backtracking on 2,000-deep bracket/paren nests, 20k tokens, 20k space runs or alternating quotes; all patterns scale linearly to 4 MB (growth ≈ ×16 for ×16 input). Fixture symlink is relative and contained. | `tools/mori-driver-liveness.py` (whole file), `tools/mori-vote-bind.py` (whole file) |

# Draft — command-binding semantics of the r89 receipt gate (round 89)

source: S607 (Python 3.14 `shlex` documentation — the lexical analyzer the gate uses:
  `shlex.split(..., comments=True)` drops the comment text and applies POSIX quoting
  rules; the module documents itself as "lexical analyzers for simple syntaxes
  resembling that of the Unix shell"), S609 (Python 3.14 `os.path.normpath` — lexical path
  normalization: redundant separators and up-level references collapse, but "This string
  manipulation may change the meaning of a path that contains symbolic links"), S610
  (Python 3.14 command line and environment — the interpreter's own statement that a
  file-name argument "reads and executes a script from that file", that `-c command`
  "executes the Python statement(s) given as command", and that "all consecutive arguments
  will end up in sys.argv"). The explicitly different scoped row S608 is **rejected** and
  is cited here only as the boundary: `shlex` alone cannot ground shell-execution
  semantics.
  Pinned copies under `.ufo/waves/round-89/w1/Mo89S01Sources/sources/` (sha256
  c65790957ade04d9054d174d807a439417ef907b63b3b3b01f3d2a88e2f50919 shlex-3.14.10.html,
  71187c777e98baf54237c6bc82a2230c32b621c632beb4e23a6d01b622e4882d os.path-3.14.10.html,
  62a888347e9469b7bbb608815d855ccb64ff347b4bf7eadffa324a381f1a5a87 cmdline-3.14.10.html);
  two fetches per URL byte-identical; locator receipt
  `.ufo/waves/round-89/w1/Mo89S01Sources/sources/fetch-and-locator-receipt.txt`.
  Supporting lane row: S226 (os.path.realpath) already carries the realpath half of the
  path-identity rule; S609 does not supersede it.
verified-at: 2026-11-04 (round 89; every quote below is located by raw-HTML line span and
  occurrence count in the rendered page text, machine-produced by
  `sources/make-receipt.py`; the behavioral table's "observed" column is a local
  characterization of the frozen gate's `binding_problems`, imported read-only from
  `.ufo/waves/round-87/count-c2.py` at 760428abf925d98025b34bf23f2cbf54cbeb3bca, sha256
  d7ea961a9ede1cefc615e0308c51ac99bc2a187cdf225aade0abd97bb03f6a13)
recheck: on-release

## Scope of this entry

Detection and report only. This entry records **what the r89 receipt gate's
`binding_problems` decides and what the cited pages do and do not license**. It makes no
verdict about the round-89 C1 claim's own measurement — the closure judge owns that. This
seat is the author lane; it is not an independent closure verifier.

## The rule, as implemented (lane bytes, not a source)

`.ufo/waves/round-87/count-c2.py` at 760428ab, `binding_problems` (lines 181-199) with
helpers `command_invocations` (149-159), `same_path` (162-169), `script_position`
(172-178):

1. the `# cmd:` string is split on `;` into invocations; each invocation is tokenized with
   `shlex.split(part, comments=True)` — comments are dropped;
2. a token names the bound path iff `os.path.normpath(token) == os.path.normpath(path)`,
   or (with a repo root) the two realpaths are equal — so `./tools/x.py` and
   `tools/x.py` are the same file;
3. the matching token must sit in **script position**: index 1 after an interpreter
   (`python3`, `python`, `bash`, `sh`, `node`, `uv`), or index 2 when index 1 is a flag.
   A path passed as data, as an assignment, or printed by `printf`/`echo` does not bind;
4. if `shlex.split` raises `ValueError` (unbalanced quote), the whole command yields
   `cmd-binding` — the gate refuses rather than guessing.

## C1 behavior, and the ground each part has

| C1 arm | Gate behavior | Observed (frozen 760428ab `binding_problems`) | Source ground (admitted S-id) | What the source does **not** establish |
|---|---|---|---|---|
| `equiv` | `./tools/mori-record-sweep.py` accepted | `python3 -I ./tools/... --root .` → `problems=[]` | **S609** (normpath collapses redundant separators/up-level refs, so `./x` and `x` are one lexical name) + S226 (realpath is the filesystem half) | That the two spellings are the *same file* — normpath is lexical and "may change the meaning of a path that contains symbolic links"; the repo-root realpath branch is what touches the filesystem |
| `comment` | bound path named only after `#` refused | `printf '%s\n' 'BODY' # tools/...` → `problems=['cmd-binding']` | **S607** (`shlex.commenters`: "All characters from the comment beginner to end of line are ignored"; `shlex.split` with `comments=True` parses them away) | That the *shell* the receipt was recorded under behaves this way — S607 is a documented tokenizer; S608 (the differently-scoped row) is rejected for exactly this overreach |
| `selfprint` | bound path passed as data refused | `python3 -c "print('BODY')" tools/...` → `problems=['cmd-binding']` | **S610** (`-c command` "executes the Python statement(s) given as command"; "all consecutive arguments will end up in sys.argv" — so a trailing path is an *argument*, not the script) | That any interpreter other than CPython behaves this way — S610 is CPython's own page; the gate's `INTERPRETERS` tuple also admits `bash`, `sh`, `node`, `uv`, for which this page says nothing |
| `real` | seven real receipts still met | not re-measured by this seat (author lane; the closure judge owns the measurement) | — | — |

## Limitations (named before the table's verdict)

- **A tokenizer is not a shell.** S607 is authoritative only for *tokenization*: what
  `shlex.split` returns for a string. It says nothing about which program a command line
  ran, what its exit status was, or whether a path was ever opened. The gate's claim is
  about the *shape of a recorded command string*; it is discharged by the receipt's own
  replay (`replay_body` re-executes and compares the body) plus the binding rule. The
  binding rule alone is not an execution proof — that is why the differently-scoped row
  S608 is rejected.
- **Lexical path identity is not file identity.** S609 is explicit that normpath "may
  change the meaning of a path that contains symbolic links". The gate compensates with a
  repo-root realpath branch (whose ground is S226), but that branch applies only when a
  repo root is supplied; with `repo=None` the rule is purely lexical.
- **The `INTERPRETERS` set outruns the cited pages.** S610 covers CPython. `bash`, `sh`,
  `node`, `uv` are in the gate's tuple but no cited page states their script-position
  semantics. This is an ungrounded-extension residual, not a defect of the round.
- **The refusal on unbalanced quotes is total.** `shlex.split` raising `ValueError` makes
  `command_invocations` return `None`, and the gate then emits `cmd-binding` for *every*
  binding in that command. Observed: `python3 -c "print('a;b')" tools/...` →
  `invocations=None` → `cmd-binding`. A `;` *inside* quotes splits the raw string before
  tokenizing, so a semicolon inside a quoted argument is a false-refusal surface. This is
  a real residual of the round-89 rule; it is reported, not fixed here.
- **Two flags break script position.** `script_position` accepts index 1, or index 2 when
  index 1 starts with `-`. Observed: `python3 -I -B tools/...` → the path sits at index 3
  → `cmd-binding`. The frozen contract's `equiv` arm uses one flag (`-I`), so the landed
  predicate is met, but the *no-harm* surface for two-flag invocations is a genuine
  residual of the rule as written.
- **`INTERPRETERS` matching is by basename.** `os.path.basename(tokens[0])` — so
  `/usr/bin/python3 tools/...` binds (observed `problems=[]`) while `python3.14 tools/...`
  does not (observed `problems=['cmd-binding']`). Same for `env FOO=1 python3 ...`, which
  is refused (observed) because `env` is not an interpreter and the real path token sits
  at index 3.

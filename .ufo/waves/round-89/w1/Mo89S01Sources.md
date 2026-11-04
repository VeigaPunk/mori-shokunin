# Mo89S01Sources — source opening and grounded knowledge entry (round 89, w1, attempt 1)

```
seat:            Mo89S01Sources
role:            scribe / author lane; detection and report only; NOT an independent closure verifier
axes:            depth, operability
milestone:       Open source and draft grounded knowledge entry
lane:            mori-shokunin, /home/vgpnk/Projects/shokunin/mori-shokunin
lane HEAD:       760428abf925d98025b34bf23f2cbf54cbeb3bca  "round-89 C1: the r87 receipt gate
                 binds the executed script (path identity + script position), 23 -> 26 arms,
                 r88 caller pin migrated, registry row 23"
frozen d4438695: round-89: freeze contract P-C1/P-C2, the two counters and the
                 do-nothing/skip-work controls
authored subject: .ufo/waves/round-87/count-c2.py at 760428ab
                 sha256 d7ea961a9ede1cefc615e0308c51ac99bc2a187cdf225aade0abd97bb03f6a13
                 (binding_problems 181-199; command_invocations 149-159; same_path 162-169;
                 script_position 172-178)  — read-only, via `git show`, not modified
scratch:         /fast/scratch/hyaku/mori-r89/Mo89S01Sources (created, used, deleted at exit)
tooling:         none installed. curl 8.23.0 (pre-installed upstream binary), python3 3.14.8
                 (system), coreutils cmp/sha256sum. No pacman/uv/npx transaction this round.
mutations:       none in the lane. `git status --porcelain` before and after this seat shows
                 the same set; the only new paths are under my unique report dir.
```

## 0. What was run (exact commands and outcomes)

```text
$ cd /fast/scratch/hyaku/mori-r89/Mo89S01Sources && mkdir -p ...
$ curl -sSL -A "mori-r89-source-seat/1.0" -o shlex.html \
    https://docs.python.org/3.14/library/shlex.html
  http=200 bytes=66501 url=https://docs.python.org/3.14/library/shlex.html
$ curl -sSL -A "mori-r89-source-seat/1.0" -o os.path.html \
    https://docs.python.org/3.14/library/os.path.html
  http=200 bytes=88234 url=https://docs.python.org/3.14/library/os.path.html
$ curl -sSL -A "mori-r89-source-seat/1.0" -o cmdline.html \
    https://docs.python.org/3.14/using/cmdline.html
  http=200 bytes=160951 url=https://docs.python.org/3.14/using/cmdline.html
  (third URL: opened for the script-position ground; see the proposed S610 row in §2)

# second fetch of each, compared byte for byte:
$ for f in shlex os.path cmdline; do curl -sSL -A "mori-r89-source-seat/1.0" -o $f.b.html \
      <same url>; cmp -s $f.html $f.b.html && echo "$f byte-identical"; done
  shlex byte-identical
  os.path byte-identical
  cmdline byte-identical

$ sha256sum *.html
  c65790957ade04d9054d174d807a439417ef907b63b3b3b01f3d2a88e2f50919  shlex.html
  71187c777e98baf54237c6bc82a2230c32b621c632beb4e23a6d01b622e4882d  os.path.html
  62a888347e9469b7bbb608815d855ccb64ff347b4bf7eadffa324a381f1a5a87  cmdline.html

# duplicate sweep against the live registry, before proposing any id:
$ grep -cE '^\| S[0-9]+ ' corpus/SOURCES.md                      -> 379
$ grep -cE '^\| S[0-9]+ .*shlex' corpus/SOURCES.md               -> 0
$ grep -cE '^\| S[0-9]+ .*normpath' corpus/SOURCES.md             -> 0
$ grep -cE '^\| S[0-9]+ .*using/cmdline' corpus/SOURCES.md       -> 0
$ grep -cE '^\| S[0-9]+ .*sys\.argv' corpus/SOURCES.md            -> 0
$ grep -nE '^\| S[0-9]+ .*os\.path\.html' corpus/SOURCES.md
  232:| S226 | ... https://docs.python.org/3/library/os.path.html#os.path.realpath
  234:| S228 | ... https://docs.python.org/3/library/os.path.html#os.path.realpath
$ grep -oE '^\| S[0-9]+' corpus/SOURCES.md | tr -d '| ' | sort -V | tail -5
  S602 S603 S604 S605 S606
$ for i in 607 608 609 610 611 612; do grep -cE "^\| S$i " corpus/SOURCES.md; done
  0 0 0 0 0 0        # S607..S612 all unused
$ grep -rIl 'docs.python.org/3.14/library/shlex.html' .          # whole lane, not just the registry
  .ufo/waves/round-89/w1-dispatch.json
  .ufo/waves/round-89/w1-spec.json                              # my own dispatch text only
$ grep -rIl 'docs.python.org/3.14/using/cmdline.html' .          -> (nothing)

# quote location + word count + occurrence count, machine-produced:
$ python3 sources/make-receipt.py     # writes sources/fetch-and-locator-receipt.txt
  8 quotes located, each occurrence count = 1 in the rendered page text

# frozen-gate characterization (import of the committed gate module, no side effects,
# no write to the lane, no fixture, no commit):
$ git -C <lane> show 760428ab:.ufo/waves/round-87/count-c2.py > scratch/gate-r87-at-760428ab.py
$ python3  # importlib load of that file; call command_invocations / binding_problems only
  IMPORT OK (no side effects at import); INTERPRETERS= ('python3','python','bash','sh','node','uv')
  equiv (contract)                 problems=[]              # accepted
  comment (contract)               problems=['cmd-binding']  # refused
  selfprint (contract)             problems=['cmd-binding']  # refused
  two flags -I -B                  problems=['cmd-binding']  # residual (index 3)
  abs path /usr/bin/python3        problems=[]              # basename match binds
  direct invocation (shebang)      problems=['cmd-binding']  # residual
  quoted script                    problems=[]              # quotes stripped, binds
  python3.14                       problems=['cmd-binding']  # basename miss
  env prefix                       problems=['cmd-binding']  # residual
  semicolon inside quotes          invocations=None -> cmd-binding   # false-refusal surface
  hash inside path token           invocations=[['python3','-I','a']] -> cmd-binding
```

No gate was executed by this seat: the C1 counter, its selftest, and the C2 counter were
not run here. Nothing in §3 below is a claim measurement; it is source opening and a
characterization of the *committed gate function's* inputs/outputs.

## 1. Duplicate sweep — what is already in scope, and what is not

The registry's last id is **S606**; S607..S612 are unused, so the proposed ids below are
free. Existing URL scopes that touch my pages:

- **S226 / S228** carry `os.path.html#os.path.realpath` (canonical-path resolution,
  symlink elimination) — unversioned `/3/` URL, re-opened 2026-10-23/24. Neither mentions
  `normpath`, lexical collapsing, or up-level references. **No row names `normpath`** and
  **no row mentions `shlex`** (0 hits each).
- No row names `using/cmdline.html`; no row mentions `sys.argv`.
- The lane's own path-identity rule already has its realpath half in S226/S228. My
  proposed rows are the *lexical* half and the *tokenizer* half, which no row carries.

## 2. Proposed SOURCES rows (draft only — I did not edit `corpus/SOURCES.md`)

These are proposals for the L1 to land; `corpus/SOURCES.md` is byte-unchanged by this seat
(`git status --porcelain corpus/SOURCES.md` → empty). Each row follows the file's 11-cell
schema `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck |
used-by`. Cell text for the `source` cell is compressed to one line; a pipe inside a cell
would break the table, so no cell below contains a literal `|`.

### S607 — ADMIT (tier A, `docs`)

| cell | content |
|---|---|
| id | S607 |
| source | Python 3.14 `shlex` module documentation — https://docs.python.org/3.14/library/shlex.html |
| kind | docs |
| tier | A |
| scope | shell-like lexical tokenization only: what `shlex.split(s, comments=True)` returns for a command string, that comment text is dropped, and POSIX-mode quote handling — not shell execution semantics, not what a shell ran, not a path's filesystem identity |
| anchor | `shlex.commenters` entry, raw HTML lines 429-431, quote "All characters from the comment beginner to end of line are ignored" (12 words, occurs exactly once in the rendered page); `shlex.split(s, comments=False, posix=True)` entry, raw HTML lines 228-230, quote "If comments is False (the default), the parsing of comments in the given string will be disabled" (17 words, occurs exactly once); page sha256 c65790957ade04d9054d174d807a439417ef907b63b3b3b01f3d2a88e2f50919, 66501 bytes, 810 lines, two fetches byte-identical, HTTP 200, no redirect, accessed 2026-11-04; pinned copy `.ufo/waves/round-89/w1/Mo89S01Sources/sources/shlex-3.14.10.html` |
| teaches | A tokenizer states what a token *is*, never what a shell *ran*: the comment text never becomes a token, so a bound path named only inside a `#` comment cannot bind — and `shlex` never claims to model shell execution, which is why the differently scoped S608 row is refused |
| status | mined |
| opened | 2026-11-04 |
| recheck | on-release |
| used-by | corpus/knowledge/cmd-binding-r89.md (draft: `.ufo/waves/round-89/w1/Mo89S01Sources/knowledge-cmd-binding-r89.draft.md`) |

### S608 — REJECT (tier C, `docs`) — the explicitly different scoped row

| cell | content |
|---|---|
| id | S608 |
| source | Python 3.14 `shlex` module documentation (rejected scope: shlex alone as shell-execution proof) — https://docs.python.org/3.14/library/shlex.html |
| kind | docs |
| tier | C |
| scope | the *different* scope "that tokenizing a recorded command string with `shlex` establishes which program the shell executed" — explicitly not S607's tokenization scope, and not a path-identity scope |
| anchor | module introduction, raw HTML lines 220-222, quote "The shlex class makes it easy to write lexical analyzers for simple syntaxes resembling that of the Unix shell" (19 words, occurs exactly once); page sha256 c65790957ade04d9054d174d807a439417ef907b63b3b3b01f3d2a88e2f50919, accessed 2026-11-04 |
| teaches | REJECTED as a scope, not as a page: the page is authoritative for tokenization only, and the very sentence quoted here scopes it to "simple syntaxes resembling that of the Unix shell". A token list cannot establish what a shell executed, what its exit status was, or whether a path was opened — so `shlex` alone cannot ground the r89 C1 claim's script-position rule. FLIP: admit a distinct row over a source that specifies shell command execution and script-position semantics (for example a POSIX shell specification's command-word/argument rules) — then that row, not `shlex`, carries the execution claim, and S607 stays the tokenizer ground |
| status | rejected |
| opened | 2026-11-04 |
| recheck | 365d |
| used-by | corpus/knowledge/cmd-binding-r89.md (as the stated boundary of S607) |

### S609 — ADMIT (tier A, `docs`)

| cell | content |
|---|---|
| id | S609 |
| source | Python 3.14 `os.path.normpath` documentation — https://docs.python.org/3.14/library/os.path.html#os.path.normpath |
| kind | docs |
| tier | A |
| scope | lexical path normalization only: collapsing redundant separators and up-level references so that two spellings of one path name one string — and the documented limit that this string manipulation may change the meaning of a path containing symbolic links; not filesystem identity (that half is S226) |
| anchor | `os.path.normpath(path)` entry, raw HTML lines 627-630, quote "Normalize a pathname by collapsing redundant separators and up-level references so that A//B, A/B/, A/./B and A/foo/../B all become A/B." (20 words, occurs exactly once) and "This string manipulation may change the meaning of a path that contains symbolic links." (14 words, occurs exactly once); page sha256 71187c777e98baf54237c6bc82a2230c32b621c632beb4e23a6d01b622e4882d, 88234 bytes, 1011 lines, two fetches byte-identical, HTTP 200, no redirect, accessed 2026-11-04; pinned copy `.ufo/waves/round-89/w1/Mo89S01Sources/sources/os.path-3.14.10.html` |
| teaches | `./tools/x.py` and `tools/x.py` are one lexical name after normalization, which is why an equivalent `./` spelling binds — but the same page warns the collapse is string manipulation that may change the meaning of a path containing symbolic links, so lexical equality is not file identity and needs the realpath branch beside it |
| status | mined |
| opened | 2026-11-04 |
| recheck | on-release |
| used-by | corpus/knowledge/cmd-binding-r89.md (draft: `.ufo/waves/round-89/w1/Mo89S01Sources/knowledge-cmd-binding-r89.draft.md`) |

### S610 — ADMIT (tier A, `docs`) — script position, for the `selfprint` arm

| cell | content |
|---|---|
| id | S610 |
| source | Python 3.14 command line and environment — https://docs.python.org/3.14/using/cmdline.html |
| kind | docs |
| tier | A |
| scope | CPython's own statement of which command-line argument is executed as a script and which are passed as data — the `-c command` form, the file-name-argument form, and the argv rule; not shell semantics and not other interpreters |
| anchor | section "1.1.1 Interface options", raw HTML lines 250-252, quote "When called with a file name argument or with a file as standard input, it reads and executes a script from that file." (23 words, occurs exactly once); lines 254-256, quote "When called with -c command, it executes the Python statement(s) given as command." (13 words, occurs exactly once); line 263, quote "all consecutive arguments will end up in sys.argv" (8 words, occurs exactly once); page sha256 62a888347e9469b7bbb608815d855ccb64ff347b4bf7eadffa324a381f1a5a87, 160951 bytes, 1816 lines, two fetches byte-identical, HTTP 200, no redirect, accessed 2026-11-04; pinned copy `.ufo/waves/round-89/w1/Mo89S01Sources/sources/cmdline-3.14.10.html` |
| teaches | With `-c command` the interpreter executes the statement text and every remaining argument lands in `sys.argv`, so a trailing path is data, not the executed script; a file-name argument, by contrast, is the script that runs. This is what makes the C1 `selfprint` refusal a documented property of the interpreter rather than a guess |
| status | mined |
| opened | 2026-11-04 |
| recheck | on-release |
| used-by | corpus/knowledge/cmd-binding-r89.md (draft: `.ufo/waves/round-89/w1/Mo89S01Sources/knowledge-cmd-binding-r89.draft.md`) |

Id note for the L1: S607..S610 are proposed in ascending order and are all currently
unused; if another seat proposes rows concurrently, re-run the id check at integration
time — the sweep command is in §0.

## 3. Knowledge entry draft

`.ufo/waves/round-89/w1/Mo89S01Sources/knowledge-cmd-binding-r89.draft.md` — provenance
trio (`source:` / `verified-at:` / `recheck:`), the rule as implemented in the lane bytes,
a four-row C1 behavior table (each row citing an **admitted** S-id: `equiv`→S609+S226,
`comment`→S607, `selfprint`→S610), and a six-item limitations section. The `comment` row's
ground is S607 and the rejected S608 appears only as the stated boundary — no C1 claim
evidence rests on a rejected row.

The draft's C1 behavior column is the *frozen gate's* own output on the three contract
fixtures (accepted / refused / refused), reproduced from the committed
`binding_problems` at 760428ab. **This seat did not measure the round-89 C1 claim.** The
`real` row (seven receipts) is marked as not measured here.

## 4. Findings — defects and residuals, named honestly

These are observations about the *committed* gate code, not claims about the round's
verdict. Each was reproduced against the frozen bytes at 760428ab.

1. **Two-flag invocations are refused (no-harm residual).** `script_position` accepts
   index 1, or index 2 when index 1 begins with `-`. `python3 -I -B tools/...` puts the
   path at index 3 → `cmd-binding`. The frozen contract's `equiv` arm uses a single flag
   (`-I`), so the landed predicate is satisfied; the two-flag form is a genuine
   false-refusal surface that no arm covers.
2. **A `;` inside a quoted argument is a false-refusal surface.** The command string is
   split on `;` *before* tokenizing, so `python3 -c "print('a;b')" tools/...` splits into
   two fragments, the first has an unbalanced quote, `shlex.split` raises `ValueError`,
   `command_invocations` returns `None`, and the gate emits `cmd-binding` for **every**
   binding in that command. A legitimate command that prints a semicolon is refused.
   This is a real limitation of the round-89 rule as frozen, not a fixture artifact.
3. **The refusal on any unbalanced quote is total for that command.** Same mechanism as
   (2): one unparsable fragment discards the whole command's invocations.
4. **`INTERPRETERS` is matched by basename and is a closed list.** `os.path.basename(
   tokens[0])` means `/usr/bin/python3 tools/...` binds (observed `problems=[]`) while
   `python3.14 tools/...` does not (observed `problems=['cmd-binding']`). `env FOO=1
   python3 -I tools/...` is refused because `env` is not in the tuple and the path sits at
   index 3. A direct shebang invocation `./tools/...` is likewise refused.
5. **A `#` inside a path token truncates it.** `shlex.split` treats `#` as a comment
   beginner in POSIX mode; observed `python3 -I a#b/c.py` → tokens `['python3','-I','a']`.
   A repository path containing `#` would be split, not matched. **Population check:**
   `git ls-files | grep -c '#'` → 0, so no tracked path in this lane is affected today;
   this is a latent property of the rule, not a live defect.
6. **The cited pages do not cover the whole `INTERPRETERS` tuple.** S610 is CPython's
   page; `bash`, `sh`, `node`, `uv` have no cited source for their script-position
   semantics. This is an ungrounded extension in the *rule*, and it is why S608 is
   rejected rather than admitted.

Items 1, 2, 4 and 6 are surfaces the reviewer seats (Mo89R01C1 / Mo89Sc01Scope) should
weigh; I report them, I do not adjudicate them and I did not change the frozen predicates
or instruments.

### Population check on the residuals

The real receipt population's `# cmd:` lines are, verbatim:

```text
after-r87.txt:2:      # cmd: python3 -I .ufo/waves/round-87/count-c1.py 03b66a437e68d493ce0aacd1d80c321cc2e6bf7c; python3 -I .ufo/waves/round-87/count-c2.py 98f48dba3267a73714b862d0fd4fc8c0e82a1d04
claim-sweep-r87.txt:2:# cmd: python3 -I tools/mori-claim-sweep.py --root . --pins .ufo/waves/round-80/claim-pins.json
record-sweep-r87.txt:2:# cmd: python3 -I tools/mori-record-sweep.py --root . --pins .ufo/waves/round-82/record-pins.json
```

Every one is `python3 -I <path>`: one interpreter token, one flag, the bound path at
index 2 — inside the rule's accepted window. The `;` in `after-r87.txt` separates two
*unquoted* invocations, which the split handles correctly (two token lists, not one
broken one). Observed on the frozen `binding_problems` with both of `after-r87.txt`'s
bound paths: `invocations=[['python3','-I','.ufo/waves/round-87/count-c1.py','03b66a43…'],
['python3','-I','.ufo/waves/round-87/count-c2.py','98f48dba…']]`, `problems=[]`. No real
receipt contains a quoted `;` (`grep -c "';'"` over the population → no hits), so residual
2 does not fire on the seven-receipt population today. Residuals 1, 3 and 4 likewise do
not fire on it. **These are no-harm residuals of the rule as written, not defects of the
landed predicate** — the landed `equiv` arm is met, and the residuals are the surfaces a
future receipt form could hit.

## 5. Scope discipline and out-of-scope items

- **Not done, by design:** `corpus/SOURCES.md` was not edited (proposals only);
  `corpus/knowledge/` was not written (the entry stays a draft under my report dir); no
  counter, selftest, or gate was executed; no fixture was created and no commit was made;
  no candidate copy under `.ufo/waves/round-89/w1/candidates/` was touched (that path is
  E01/E02's); the production checkout, fleet root, sibling repos and the git/jj index
  were read-only.
- **Pre-existing worktree modifications, not mine:** `git status --porcelain` showed
  ` M corpus/README.md` and ` M corpus/knowledge/receipt-counterfeit-r88.md` already
  modified at this seat's first read, and both are still modified with the same content
  at exit (this seat never opened either file for writing). The only paths this seat
  added are under `.ufo/waves/round-89/w1/Mo89S01Sources/`.
- **Out of scope, declared:** whether the round-89 C1 claim is met (closure judge's job);
  whether the residual false-refusal surfaces in §4 are defects of the round or accepted
  no-harm limits (reviewer/L1's job); the C2 arm/attribution work (E01/E02/Mo89M01Mut).
- **Tooling:** nothing installed or upgraded this round; curl 8.23.0 and python3 3.14.8
  were already present and are the tools used. The generic tooling directive's pacman
  channel is paused host-wide for this wave, and no `uv tool`/`npx` install was needed.

## 6. Artifact paths (candidate artifacts first)

- Pinned sources + receipt + generator:
  - `.ufo/waves/round-89/w1/Mo89S01Sources/sources/shlex-3.14.10.html`
  - `.ufo/waves/round-89/w1/Mo89S01Sources/sources/os.path-3.14.10.html`
  - `.ufo/waves/round-89/w1/Mo89S01Sources/sources/cmdline-3.14.10.html`
  - `.ufo/waves/round-89/w1/Mo89S01Sources/sources/fetch-and-locator-receipt.txt`
  - `.ufo/waves/round-89/w1/Mo89S01Sources/sources/make-receipt.py`
- Knowledge entry draft:
  - `.ufo/waves/round-89/w1/Mo89S01Sources/knowledge-cmd-binding-r89.draft.md`
- This report:
  - `.ufo/waves/round-89/w1/Mo89S01Sources.md`

Scratch `/fast/scratch/hyaku/mori-r89/Mo89S01Sources/` is deleted before this seat yields;
every durable receipt is already under the report dir.

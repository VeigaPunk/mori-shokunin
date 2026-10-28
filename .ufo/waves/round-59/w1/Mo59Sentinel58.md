# Mo59Sentinel58 — security review of the round-59 tools (path handling, entry-text evaluation, subprocess surfaces)

Seat: sentinel (attack share). Read-only on the lane; no production/corpus/VCS edits, no fleet or
sibling writes, no pacman, no network. Freeze `60b3a76ad0524c8978cc51922940be1c8c388915`
(entering `2b9f03975bfb6e508f35074ac8181ec8bf54e805`); lane HEAD observed during the seat:
`8ff344ff18924c1ea63d46c3b3969f9fea05bc51`.

Subject files (frozen bytes; sha256 confirmed equal to both PINs in the working tree and at HEAD):

| file | sha256 |
|---|---|
| `tools/mori-register-check.py` | `38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8` (= C1 `PIN`) |
| `tools/mori-settlement-scan.py` | `4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9` (= C2 `PIN`) |
| `.ufo/waves/round-59/count-c1.py` | `2be6fda8c54633fd96f9d447e8e78ff4ba4a6d6136670f79a9d622003f0c9dfd` |
| `.ufo/waves/round-59/count-c2.py` | `2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be` |

## Method (bounded) and baseline

1. Full read of the four files above (`cat -n`), plus `contract.md`.
2. One honest run of each counter at the freeze revision, scratch under the seat dir:
   `python3 .ufo/waves/round-59/count-c1.py 60b3a76… --scratch <seat>/honest-c1`
   → `C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=60b3a76…` (rc 0);
   `count-c2.py 60b3a76…` → `C2=unmet … entry_absent | copy_absent:*` (rc 1, expected: C2 data lands
   after the freeze; recorded as context, not a finding).
3. Five throwaway git repos, each `git init` under
   `/fast/scratch/hyaku/mori-r59/Mo59Sentinel58/<name>`, every git command `git -C <that path>`,
   `git rev-parse --show-toplevel` asserted to print the repo; all commits confined there.
4. Module-level import (`importlib`) of the two frozen modules in-process to drive `pointer_ok`,
   `check`, and `eval_entry` on synthetic roots; the frozen counters were additionally driven with
   `--repo <scratch repo>` so that no lane file was read as mutable state.
5. Not done (out of scope by seat): no execution against network, no provider/liveness inference, no
   remediation edits, no claim about whether either axis is met beyond the counter lines quoted.

## F1 — HIGH: the SHA-256 pin is advisory, not an execution gate; committed tool bytes run as the operator

Both counters compute `tool_ok` from the pin and then **execute the bytes anyway** whenever the
path exists. The pin only removes `met`; it never suppresses execution.

- `count-c1.py:96-99` computes `tool_ok = tool_b is not None and sha256(tool_b) == PIN`;
  `:104-106` writes the bytes to `<scratch>/tool.py` for **any** `tool_b`;
  `:110-116` runs `python3 <scratch>/tool.py --selftest` gated on `if tool_b is not None:`;
  `:152-153` (`run_tool`) executes once per fixture directory (13×);
  `:183` and `:194` execute in the real arm (2×).
- `count-c2.py:198-206` same write; `:208-214` selftest gated on `tool_b is not None`;
  `:232-236` scan arm gated on `tool_b is None or not rfiles` (not on `tool_ok`);
  `:253-259` drift arm gated on `if db is not None and tool_b is not None`.

Exploit path (bounded, executed): commit a `tools/mori-register-check.py` (and
`tools/mori-settlement-scan.py`) whose sha ≠ PIN and whose body writes a marker and prints the
expected selftest line; run the frozen counters against that revision (`<scratch>/demo-exec`):

```
python3 count-c1.py HEAD --repo <demo-exec> --fleet /home/vgpnk/Projects/shokunin --scratch …/scr1
 → C1=unmet selftest=ok fixtures=bad real=bad pointers=bad rev=HEAD failed=tool_sha,fixtures_absent,scorecard,real,pointers
python3 count-c2.py HEAD --repo <demo-exec> --fleet … --scratch …/scr2
 → C2=unmet selftest=ok scan=bad drift=bad trees=bad entry=bad … tool_sha,t…
EXEC.log:
 C1 --selftest --scratch …/demo-exec/scr1/st
 C2 --selftest --scratch …/demo-exec/scr2/st2
```

Impact. (a) Any commit that touches `tools/mori-register-check.py` or `tools/mori-settlement-scan.py`
gets **code execution as whoever runs the wave's proof** — the L1, an orchestrator, or every seat
that reproduces the count — once per arm (C1: up to 16 executions). (b) The subprocess inherits the
operator environment: `count-c1.py:115` and `count-c2.py:213` pass `env={**os.environ,
"TMPDIR": …}`; the `run_tool`/scan/drift arms inherit the default env, so `HOME`,
agent/session env and any ambient credentials are in the hostile tool's process. (c) The printed
audit token `selftest=ok` is emitted from the *unverified* bytes (both lines above), so the output
line's per-arm tokens attest "whatever executed", not the pinned tool — only `tool_sha` is sound.
The `met` verdict itself is not forgeable this way (`met = tool_ok and …`, `count-c1.py:209`,
`count-c2.py:360`).

Smallest remediation: gate every execution site on `tool_ok` (`if tool_ok:` at
`count-c1.py:110/152/183/194`, `count-c2.py:210/235/258`) so a sha mismatch skips the arms instead
of running them, and pass a minimal env (`{"PATH","TMPDIR","LANG"}`) to those subprocesses.

## F2 — MEDIUM: the negative-control expectations are attacker-controlled committed bytes, so the hostile-fixture / hostile-tree arms are neutralizable (C1 still prints `met`)

The counters read fixture bodies **and** their `expect` files from the same revision R they grade,
and nothing pins those bytes (only the tool is pinned):

- `count-c1.py:133-139` reads `<fixture>/expect.txt` at R; `:158`
  `matched = all(any(r.startswith(e) for r in reasons) for e in expect)`; `:161` requires only
  `verdict_unmet`.
- `count-c2.py:328-333` reads `<tree>/expect.txt` at R; `:347` `want_ok = not expect`, i.e. an
  **empty** expect file demands a tree that *validates*.

Three bounded escapes, all executed on a scratch replica of the C1 surface (pinned tool bytes +
lane `SCORECARD.md` + the register pointer targets + `fixtures-c1`, committed in `<scratch>/demo-neuter`):

1. Baseline replica: `C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=HEAD` (rc 0).
2. Neuter one frozen control — `f08-manifest-name-altered/scorecard.md` ← `f01-stub-only`'s body,
   `f08/expect.txt` ← `binding` → still `C1=met selftest=ok fixtures=ok real=ok pointers=ok`
   (the name-binding control no longer exists; its replacement scores only
   `binding:declared_register=0(capabilities_section=1), keys:missing=…`).
3. Add `f99-empty-expect` (stub body, empty `expect.txt`) → still `C1=met … fixtures=ok`.
   Note `"".split(",")` = `[""]`, and `r.startswith("")` is always true, so an empty expect file
   accepts *any* UNMET verdict that carries at least one reason — the frozen reason prefix is gone.

C2 analogue (executed): a tree `t99-valid` that **validates** (10 claims / 3 copies / mined row) with
an empty `expect.txt` is accepted on the negative-control arm —
`count-c2.py HEAD --repo <demo-neuter> --scratch …` prints `… trees=ok …` even though the tree is a
positive control. Deleting the twelve hostile trees and shipping validating ones (or emptying their
expect files after making them validate) leaves `trees=ok`.

Impact: `C1=met`/`trees=ok` can be produced while the hostile controls are absent or neutered — a
fabricated-readiness defect in the wave's own proof, and the kill rule ("frozen bytes/predicate/
target") does not cover fixture/tree bytes.

Smallest remediation: pin the controls — a `FIXTURES_PIN`/`TREES_PIN` map (`name →
sha256(scorecard.md|manifest.json|expect.txt)`, or one digest over the sorted `ls-tree -r` listing)
checked before the arm; require `expect` to be a non-empty list of tokens (`if not expect:
failed.append("expect_absent")` at `count-c1.py:140`, `count-c2.py:333`).

## F3 — MEDIUM-LOW: the evidence-pointer predicate is lexical only; `is_file()` follows symlinks and a committed symlink blob satisfies the counter's own pointer gate

`tools/mori-register-check.py:92-102` (`pointer_ok`) rejects `/`, `~` and `..` components, then
`:185` `(Path(root) / rel).is_file()` — byte-level containment is never checked, and `is_file()`
follows links.

- Executed against a synthetic root containing `leak -> /etc/hostname`:
  `is_file(leak)=True`, `resolve()=/etc/hostname`, and the frozen tool prints
  `{"verdict":"REGISTER_MET","pointers":["leak"],"reasons":[]}` (rc 0). The predicate "each exists as
  a file under --root" is therefore satisfied by a pointer escaping `--root` whenever the tool is
  run against a *working tree* (where a committed symlink materializes as a symlink).
- Executed at the counter level (`<scratch>/demo-symlink`): a committed symlink `tools/hostlink →
  /etc/hostname` in mode `120000` gives `git cat-file -e HEAD:tools/hostlink` rc 0 and
  `git show HEAD:tools/hostlink` = `b'/etc/hostname'`; the counter's exact recipe
  (`count-c1.py:187-195`: cat-file gate, then `materialize()` writing the blob bytes) writes
  `proot/tools/hostlink` = `b'/etc/hostname'`, and the tool then prints `REGISTER_MET` with
  `pointers: ["tools/hostlink"]`. So a hostile commit can bind "evidence" to a one-line symlink whose
  content is a host path instead of a lane artifact.

Smallest remediation: resolve and contain — `rp = (Path(root)/rel).resolve(); p = Path(root).resolve();
if p != rp and p not in rp.parents: reason pointers:escape`; and require mode `100644`/`100755`
(`git ls-tree -z <rev> -- <path>` / `os.lstat` + `stat.S_ISREG`) so mode `120000` evidence is
rejected.

## F4 — LOW: uncaught `int()` limit aborts `count-c2.py` on hostile entry text (no output line, no reasons)

`count-c2.py:124-128` does `int(n)` on the regex-captured span number, and `eval_entry` is called from
the trees arm at `:346` with **no** exception guard. A committed claim line carrying a >4300-digit
line number raises before any reason is produced (Python 3.14.8):

```
eval_entry(<tree with claim span 9*5000>) -> RAISED ValueError:
  Exceeds the limit (4300 digits) for integer string conversion: value has 5000 digits
```

Impact: the whole `measure()` aborts with a traceback — no `C2=…` line, so a hostile tree (or a
post-freeze entry edit) can deny the counting command rather than be scored UNMET. Fail-closed in
verdict terms, but it also destroys the "before" control output.

Smallest remediation: reject over-long spans as a reason (`if len(n) > 9: reasons.append("span:%s" % kid)`),
and wrap the per-tree `eval_entry` call in `try/except (ValueError, RecursionError)` →
`tree:<name>:crash`.

## F5 — LOW: argv parsing crashes / silently mis-parses (operator input only)

`count-c1.py:250-257` and `count-c2.py:440-445` do `argv[i+1]` with no bounds check and skip unknown
flags:

```
python3 count-c1.py HEAD --repo   → rc=1, IndexError: list index out of range
python3 count-c2.py HEAD --repo   → rc=1, IndexError: list index out of range
```

`--scratch`/`--repo` values are also unvalidated (an absolute/`..` scratch path is honoured verbatim
for `mkdir`/write). Not reachable from committed content; option injection into `git` *is* blocked —
both counters exit 2 when `argv[0]` starts with `-` (`count-c1.py:242`, `count-c2.py:433`), and
`git -C` consumes a following `--flag` as a directory, not an option. Also noted:
`mori-settlement-scan.py:199` treats `--scratch <dir>` in non-selftest mode as an input *file*
(`args = [a for a in argv if not a.startswith("--")]`).

Smallest remediation: `argparse` in both counters (mirroring `mori-register-check.py:288-294`).

## F6 — No counterexample found (bounded negatives, worth recording)

- **No eval of entry text anywhere.** Construct scan of the four files finds only `re.compile`
  (`mori-register-check.py:46-51`, `count-c2.py:78-83`) and, in `count-c2.py`, `shutil.rmtree` at
  `:425` which is selftest-local (`finally:` over its own `tempfile.mkdtemp`). No `eval(`, `exec(`,
  `compile(` of text, `os.system`, `shell=True`, `pickle`, `yaml`, `__import__` in any of the four.
  All subprocesses use argv lists, so fixture/entry/artifact content cannot reach a shell.
- **Outside-file claims are not read.** `count-c2.py:140-142` computes `root / cfile` and then
  `continue`s unless `cfile in ARTIFACTS`; a claim naming `/etc/hostname` yields
  `['claims_min:1','files_min:1','files:outside=/etc/hostname']` with **no** `pin:` reason, i.e. the
  file was never hashed/opened. Same for relative `../..` copies.
- **Materialize writes cannot escape the counter's root.** `git_show`/`cat-file` resolve
  `rev:path` as an object name, and git rejects traversal/absolute specs:
  `HEAD:../../etc/hostname` rc 128, `HEAD:/etc/hostname` rc 128, `HEAD:tools/../SCORECARD.md` rc 128
  (`HEAD:./tools/…` rc 0, which `pointer_ok` already normalizes). Symlink blobs are materialized as
  regular files by `materialize()` (`count-c1.py:77-88`), so no write/read is redirected through a
  committed link at *counter* level (only F3's pointer-acceptance gap remains).
- **NUL in a backticked pointer does not crash the tool**: `Path(...).is_file()` swallows the
  `ValueError: embedded null byte`; the tool exits 1 with a normal UNMET JSON (rc=1, empty stderr).
- **`pointer_ok` lexical filter behaves as documented** for the obvious attacks: `/etc/passwd`,
  `../x`, `a/../../b`, `~/.ssh/id_rsa`, `a/..`, `..`, `./..` → False; `./x`, `tools/a.py`, `a//b`,
  `a/./b` → True (harmless normalizations). Literal `C:\x`, `a/%2e%2e/b`, `....//x` → True but are
  inert on POSIX (no separator meaning); they cannot traverse.
- **`mori-settlement-scan.py` has no execution surface from results JSON**: `json.loads` only
  (`:52`), no path from content is opened, output is `json.dumps`. A 100k-deep nested array gives an
  uncaught `RecursionError` (rc 1, no JSON) — fail-closed at the counter's scan arm, but the tool
  should report `not_json`.
- **Predicate nit (soundness, not security)**: `isinstance(x, int)` accepts booleans
  (`:62`, `:67`); `{"round": true, "seats": true, "results":[1 member]}` scans
  `SETTLEMENT_SCAN_OK` (rc 0). Contract says "`round` int >= 1", "`seats` int"; `type(x) is int`
  would close it.

## Severity summary and smallest remediations

| id | severity | surface | smallest fix |
|---|---|---|---|
| F1 | High | committed tool bytes execute despite sha ≠ PIN, with full operator env (C1 ×16, C2 ×3) | gate every `subprocess.run(tp…)` on `tool_ok`; minimal env |
| F2 | Medium | fixture/tree `expect.txt` + bodies unpinned → controls neutered, `C1=met`/`trees=ok` still printed | pin control bytes; reject empty expect |
| F3 | Medium-Low | pointer predicate lexical; symlink escape / symlink blob accepted as evidence | `resolve()` containment + require mode 100644/100755 |
| F4 | Low | `int(n)` overflow aborts `count-c2` with a traceback | length bound + try/except per tree |
| F5 | Low | argv `IndexError`, unvalidated `--scratch`, scanner flag/arg confusion | `argparse` |
| F6 | Info | no code-exec/read-escape path found on the data surfaces; two predicate nits (bool ints, RecursionError) | `type(x) is int` |

No production edits made; no lane VCS operation attempted beyond read-only `git show/ls-tree/cat-file`;
scratch (`/fast/scratch/hyaku/mori-r59/Mo59Sentinel58`, TMPDIR inside it) removed after the run.
Disk guard was green at seat start (`/fast/scratch/hyaku` 27% used, 592.6 G free).

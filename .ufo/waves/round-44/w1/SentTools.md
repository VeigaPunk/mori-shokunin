# round 44 · w1 · SentTools — trust-boundary review of the three counters and the auditor

Seat: sentinel (read-only). Instruments frozen at `7cb59c6891d4f5d0266fe062565f094da835dc84`
(`evidence/freeze-r44.txt`); **nothing here is patched** — per `contract.md` §Freeze a defect
found post-freeze is a lesson routed to round 45. Every finding below is either a quoted line of
the frozen bytes or an observed run.

Surfaces reviewed:

| tool | bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-44/count-c1.py` | 353 ln | `9477824d5eee45f47d49be52902f7bb0cd67a4d038e0ec7e79094c1e71999f83` |
| `.ufo/waves/round-44/count-c2.py` | 388 ln | `0095d0c63afe1312c799dc8f6b8ad66d08eabf6420a9eabde032e894f17f9047` |
| `.ufo/waves/round-44/count-c3.py` | 321 ln | `a12170f1cad4a6a0eb18c14dd50b7e22e1dec4b67e5d44c217f8ed8e9c440c68` |
| `tools/mori-gate-registry.py` | 308 ln | `743996b11d19261b87e3ea6c0d0be4c0e5e6750d05f6d603af51dc1a7e125a1f` |

Method: the four files were copied out of the checkout into a fresh `mktemp -d`
(`/tmp/sent44.AwC2Gs`) and driven against throwaway git repos built there. The lane checkout was
never written; the only lane write is this report. Reproduction recipe: copy the four files to
`$S/bin`, `git init` a repo with `data.txt` = `x\nx\nx\n`, and pass `--repo`/`--rev` explicitly.

Verdicts observed while testing (context, not my claim): at the frozen tip
`python3 .ufo/waves/round-44/count-c1.py 7cb59c68…` → `check ledger_present FAIL (absent)` →
`C1=unmet mismatches=?`, rc 1 — `figures.tsv` does not exist at that revision.

## Findings

| id | sev | one line |
|---|---|---|
| F1 | **HIGH** | C1 runs committed ledger rows through `bash -c`; the grammar constrains only the producer, so a committed row executes arbitrary commands and writes arbitrary paths — and `C1=met` is still printed |
| F2 | **HIGH** | `git` inherits `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`: `--selftest` commits into a foreign repo named by the environment, and `--repo` is not authoritative |
| F3 | **HIGH** | C3's `census_ok` executes an arbitrary, uncommitted program — default is the **fleet** file `<repo>/../scripts/sources-census.sh`, absent from the lane tree; `C3=met` proven with a hostile stub |
| F4 | MEDIUM | `diff` is on C1's read-verb allowlist, and `git diff` executes `core.fsmonitor` from the measured repo's local config |
| F5 | MEDIUM | in `WORK` mode `--ledger`/`--entry`/`--readme`/`--counter`/`--mutants-dir` accept absolute paths, `..` and symlinks; `--counter` then *executes* the out-of-repo file |
| F6 | MEDIUM | timeouts kill `bash -c` only, not the process group: a row leaves a detached process running after the gate exits |
| F7 | MEDIUM | the verdict line is not self-describing: `--repo` is never printed, floors/knobs are never printed, and `C1=met` is printable from a 1-row ledger |
| F8 | MEDIUM | the declared write scope in `SKILL.md` rows 183–186 ("stdout only", "nothing in the repo is written") is false as written |
| F9 | LOW | `MORI_GATE_REGISTRY` substitutes the auditor bytes that `count-c2.py --selftest` executes |
| F10 | LOW | absolute operator paths reach stdout on setup errors and in the `ledger=` line; ledger stderr is echoed into the mismatch detail; children inherit the full environment |
| F11 | LOW | `tools/mori-gate-registry.py` does not catch `TimeoutExpired`; a git timeout degrades to `REGISTRY_SETUP` exit 2 |

Clean, verified: **no** `shell=True`, `os.system`, `os.popen`, `eval`, `exec`, `pickle` or
`yaml.load` in any of the four files (`grep` rc 1 over all four); **every** `subprocess.run`
carries a timeout (table in §b); no network primitive (imports are stdlib-only —
`argparse, os, re, shutil, subprocess, sys, tempfile`; the only `http` strings are c3's
`https://example.invalid` fixture URLs); no credential or `os.environ` printing;
the tools' own `open(..., "w")`/`os.chmod` calls all target `tempfile.mkdtemp` paths.

---

## (a) Path handling

### F5 — MEDIUM — `WORK` mode reads and executes outside the repo

`read_at()` joins the caller's path onto the repo without normalising or confining it:

- `count-c1.py:65` `full = os.path.join(repo, path)` (same shape at `count-c2.py:67`,
  `count-c3.py:62`, and `tools/mori-gate-registry.py:44,50` `exists_at`/`read_at`).
- `os.path.join` returns the second argument unchanged when it is absolute, and `open()` resolves
  `..` and follows symlinks.

At a **committed revision** git confines the lookup itself, which is the only reason this is not
HIGH:

```
$ git -C $R cat-file -e "$REV:/etc/passwd"
fatal: path '/etc/passwd' exists on disk, but not in 'fbab70b8…'      rc=128
$ git -C $R cat-file -e "$REV:../../etc/passwd"
fatal: '../../etc/passwd' is outside repository at '/tmp/sent44.AwC2Gs/repo'   rc=128
```

At `rev=WORK` — the mode a report uses for "the tree as it stands" — all three escapes work and
each prints `C1=met mismatches=0`, rc 0:

```
$ python3 $S/bin/count-c1.py WORK --repo $R --ledger /tmp/sent44.AwC2Gs/outside.tsv
… ledger=/tmp/sent44.AwC2Gs/outside.tsv rows=12 classes=checks,corpus,evidence,registry,wave
C1=met mismatches=0
$ python3 $S/bin/count-c1.py WORK --repo $R --ledger ../../../../tmp/sent44.AwC2Gs/outside.tsv
C1=met mismatches=0
$ ln -s /tmp/sent44.AwC2Gs/outside.tsv $R/.ufo/waves/round-44/link.tsv
$ python3 $S/bin/count-c1.py WORK --repo $R --ledger .ufo/waves/round-44/link.tsv
check ledger_present       PASS (697 bytes)          → C1=met
```

The same file at a committed revision is the 30-byte symlink blob and correctly fails
(`rows_parse FAIL (row 1: 1 TSV cells, want 4)`), so the symlink is only followed in `WORK`.

`count-c3.py WORK --entry /tmp/sent44.AwC2Gs/outside-entry.md` likewise printed
`check entry_present PASS (193 bytes)` for a file outside the repo.

**The sharp edge is `count-c2.py --counter`.** In `WORK` mode the value is read from an arbitrary
path (`count-c2.py:125`) and then **executed**:

```
$ python3 $S/bin/count-c2.py WORK --repo $R2 --counter /tmp/sent44.AwC2Gs/evil.py
check counters_present   PASS (1 counters)
check selftest_tally     PASS (evil.py pass=9)
…
$ ls -la ~/.sent44-evilran
-rw-r--r-- 1 vgpnk vgpnk 1 Oct 25 05:12 /home/vgpnk/.sent44-evilran
```

`evil.py` was never in the repo; it wrote outside the repo using `$HOME` from the inherited
environment, and its printed tally was accepted as a counter's self-test evidence. `--mutants-dir`
has the same join (`count-c2.py:168`) and is likewise unconfined in `WORK` mode.

Impact: the read side is a same-user file read, but the *claim* side is worse — `WORK`-mode
evidence can be assembled from bytes outside the repo, and `--counter` turns an arbitrary local
file into an executed gate. Minimal remediation: reject absolute paths and any path whose
`os.path.realpath` leaves `repo`, and refuse to run `--counter` unless the path is repo-relative
at a resolved revision.

### F7 — MEDIUM — the verdict is not attributable to a repo, or to the knobs that produced it

`--repo` is `os.path.abspath()`-ed (`count-c1.py:309`, `count-c2.py:366`, `count-c3.py:298`) and
then never appears in the output: `count-c1.py` prints `rev=`, `ledger=`, and `C1=…` only. A
transcript reading `C1=met mismatches=0` is therefore indistinguishable between the lane and any
other repo on the host — and `--repo` accepts any repo at all (no lane-root check beyond
`.git` existing, and `count-c2.py`/`count-c3.py` do not even check that).

The floors are caller-settable and are not echoed either:

```
$ python3 $S/bin/count-c1.py $REV --repo $R --ledger .ufo/waves/round-44/one.tsv
ledger=.ufo/waves/round-44/one.tsv rows=1 classes=registry
C1=unmet mismatches=0
$ python3 $S/bin/count-c1.py $REV --repo $R --ledger .ufo/waves/round-44/one.tsv --min-rows 1 --min-classes 1
ledger=.ufo/waves/round-44/one.tsv rows=1 classes=registry
C1=met mismatches=0
```

A one-row ledger satisfies P-C1's "at least 12 rows / 4 classes" floor when the caller lowers it,
and the printed line is the same shape as a default run. `count-c3.py --coverage-map` and
`--row` are the same class of problem: the caller chooses the ground and the rows, so
`C3=met` does not encode "FR5 and the round's declared ids" — the command line does. A report
must quote its flags; the tool will not do it for you. Minimal remediation: print
`repo=<realpath> min_rows=… min_classes=… ledger=…` on the verdict line.

---

## (b) Subprocess use — every `subprocess.run`, with line numbers

Seven call sites; **all carry a timeout; none use `shell=True`**.

| site | argv | timeout | shell |
|---|---|---|---|
| `count-c1.py:54` | `["git","-C",repo]+args` | `timeout=timeout` (30) | no |
| `count-c1.py:113` | `["bash","-c",full]` | `timeout=timeout` | **shell semantics, see F1** |
| `count-c2.py:59` | `["git","-C",repo]+args` | `timeout=timeout` (30) | no |
| `count-c2.py:93` | `[sys.executable,path]+args` | `timeout=timeout` | no |
| `count-c3.py:54` | `["git","-C",repo]+args` | `timeout=timeout` (60) | no |
| `count-c3.py:139` | `["bash",census,"validate","--file",staged]` | `timeout=timeout` | **executes a caller path, see F3** |
| `tools/mori-gate-registry.py:38` | `["git","-C",repo]+args` | `timeout=timeout` (30) | no |

So the letter of the rule holds. Two of the seven hold the *intent* only weakly:

- `count-c1.py:113` does not set `shell=True`, but `bash -c <string built from a committed file>`
  is the same construct with the same consequence (F1). Passing the rule by argv shape is not
  passing it in substance.
- `count-c3.py:139` runs a shell script whose path the caller chooses (F3).

### F11 — LOW — the auditor's `git()` is the one site without a timeout handler

`tools/mori-gate-registry.py:38-40` passes `timeout=timeout` but has no
`except subprocess.TimeoutExpired` (the three counters all do: `count-c1.py:58,117`,
`count-c2.py:61,96`, `count-c3.py:56,142`). A hung git raises out of `audit()`; `main()` catches
bare `Exception` and prints `REGISTRY_SETUP …`, rc 2 — a timeout is reported as a usage/setup
error, indistinguishable from a bad argument. Degrades safely, but the detail is lost.

### F6 — MEDIUM — timeout kills the shell, not the process group

`subprocess.run(timeout=…)` kills only the direct child (`bash -c`). A ledger row can background
a process that outlives the gate:

```
F01	3	registry	git show @REV@:data.txt & sh -c 'sleep 40' & git show @REV@:data.txt | grep -c x
$ time python3 $S/bin/count-c1.py $REV --repo $R --timeout 2
C1=unmet mismatches=2
real	0m2.051s
$ pgrep -af "sleep 40"
4167635 sleep 40
```

The counter returned in 2.05 s and left PID 4167635 running (killed by me afterwards). A gate that
is expected to be read-only leaves host processes behind. Minimal remediation:
`start_new_session=True` + kill the process group on timeout.

---

## (c) Trust boundary: the counter executes ledger commands from a committed file

**Plainly:** the ledger is committed bytes at the measured revision, so anyone who can commit to
the measured repo can put a shell pipeline in it — and `count-c1.py:111-115` executes that
pipeline with `bash -c`, `cwd=repo`, the caller's full environment, and no sandbox. The "read
verb" grammar (`count-c1.py:96-105`) checks only the **producer**: `startswith("git ")`, second
token in `GIT_VERBS`, `@REV@` present, no `;`/`&&`, no `echo|printf|true`. It says nothing about
the consumer, redirection, command substitution, or `&`.

### F1 — HIGH — `C1=met` is printable by a ledger that writes outside the repo

A 12-row ledger whose three "hostile" rows are ordinary-looking pipelines:

```
F01	3	registry	git show @REV@:data.txt | grep -c x | tee /tmp/sent44.AwC2Gs/PWNED
F02	3	wave    	git show @REV@:data.txt | grep -c x$(touch /tmp/sent44.AwC2Gs/PWNED2)
F03	3	corpus  	git show @REV@:data.txt | grep -c x | tee /tmp/sent44.AwC2Gs/PWNED3
```

```
$ python3 $S/bin/count-c1.py 90a2678c79e2f7e0cdd24403c02de88da150e78f --repo $R
check ledger_present       PASS (697 bytes)
check rows_parse           PASS (12 rows)
check row_floor            PASS (rows=12 min=12)
check class_floor          PASS (classes=checks,corpus,evidence,registry,wave min=4)
check commands_reconcile   PASS (all rows match)
C1=met mismatches=0
$ ls -la /tmp/sent44.AwC2Gs/PWNED*
-rw-r--r-- … 2 … /tmp/sent44.AwC2Gs/PWNED
-rw-r--r-- … 0 … /tmp/sent44.AwC2Gs/PWNED2
-rw-r--r-- … 2 … /tmp/sent44.AwC2Gs/PWNED3
```

`tee` and `$(touch …)` are external commands; `>` is an arbitrary write. The `&` separator passes
the "single pipeline" rule outright:

```
F04	3	evidence	git show @REV@:data.txt & git show @REV@:data.txt | grep -c x & touch /tmp/sent44.AwC2Gs/PWNED4
→ check rows_parse PASS (12 rows)          (grammar accepted it)
→ /tmp/sent44.AwC2Gs/PWNED4 created
```

So the *grammar* is not what stops a hostile row; the integer contract is — and a row that both
writes and returns the asserted integer (the `tee` rows) satisfies both.

**Implication for `C1=met`.** `C1=met mismatches=0` means: *someone produced a repo (chosen by
`--repo`) whose ledger rows, executed as shell, each returned their asserted integer*. It does
**not** mean the rows read only committed bytes, that they were read-only, or that the repo is the
lane (F7). The claim's authority rests entirely on a human reading the ledger; the counter's own
execution is the least trustworthy part of the mechanism. Since the lane's authors are the
committers, this is not a remote-attacker scenario — it is a *provenance* defect: a ledger row is
indistinguishable from a shell script in the artifact that is supposed to certify counts, and the
certifying run executes it with the operator's privileges.

Minimal remediation (for round 45, not here): replace the `bash -c` string with an argv built from
a parsed grammar — `git <verb> <args>`, then a fixed consumer (`grep -c`, `wc -l`) applied by the
counter itself — and reject `&`, `$(`, backticks, `<`, `>` and any `|` not followed by an
allowlisted consumer.

### F4 — MEDIUM — `diff` on the allowlist runs the repo's own `core.fsmonitor`

`GIT_VERBS` includes `diff` (`count-c1.py:28`). `git diff` reads the index, and a repo-local
`core.fsmonitor` is an arbitrary command:

```
$ git -C $F config core.fsmonitor /tmp/sent44.AwC2Gs/fsm-hook.sh   # hook: touch $S/FSM_RAN
$ git diff HEAD --stat >/dev/null; ls $S/FSM_RAN
/tmp/sent44.AwC2Gs/FSM_RAN                      (git version 2.56.0)
```

End-to-end through the frozen counter, with a ledger row
`F12	0	corpus	git diff @REV@ --stat | grep -c a`:

```
$ python3 $S/bin/count-c1.py 3ec9b80d61f7ea6ee181078f3d65a2ac7adeca0c --repo $F
core.fsmonitor executed during a read-verb ledger row: /tmp/sent44.AwC2Gs/FSM_RAN
```

This is a second execution path that does not need a hostile ledger at all — the *repo* is the
attacker, and `--repo` is caller-chosen. Minimal remediation: drop `diff` from the read verbs (the
committed witness fixture needs only `show`/`grep`/`ls-tree` — `cut -f4 fixtures/figures-r43.tsv`
gives 8 `show`, 1 `grep`, 3 `ls-tree`, no `diff`), or run every git child with
`GIT_CONFIG_GLOBAL=/dev/null` plus `-c core.fsmonitor=false` and a scrubbed environment.

### F2 — HIGH — `git` inherits `GIT_DIR`; "isolated throwaway repos" are not isolated

None of the four tools scrub `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`,
`GIT_OBJECT_DIRECTORY` or `GIT_CONFIG_GLOBAL` before spawning git (`count-c1.py:52-56`,
`count-c2.py:59`, `count-c3.py:54`, `mori-gate-registry.py:38`). `git -C <dir>` does **not**
override `GIT_DIR`.

Consequence 1 — the self-test mutates a repo named by the environment. With a victim repo at one
commit:

```
$ GIT_DIR=/tmp/sent44.AwC2Gs/victim/.git python3 $S/bin/count-c1.py --selftest
selftest PASS honest_ledger_met … C1_SELFTEST pass=6 fail=0        rc=0
$ git -C /tmp/sent44.AwC2Gs/victim log --oneline | wc -l
7
```

Six commits (`git add -A` + `git commit` from `_mk_repo`) landed in the victim repo while the arm
reported PASS. Reproduced identically for `count-c3.py --selftest` (1 → 7 commits,
`C3_SELFTEST pass=6 fail=0`) and `tools/mori-gate-registry.py --selftest` (1 → 7 commits,
`GATE_REGISTRY_SELFTEST pass=6 fail=0`). `count-c2.py` shares `_mk` and would do the same; in my
run it failed earlier (`cannot locate tools/mori-gate-registry.py for the selftest fixture`) only
because the copy sat outside a checkout.

Consequence 2 — `--repo` is not authoritative for measurement either:

```
$ GIT_DIR=/tmp/sent44.AwC2Gs/repo2/.git python3 $S/bin/count-c1.py 90a2678c… --repo /tmp/sent44.AwC2Gs/repo
C1_SETUP cannot resolve revision '90a2678c…'                       rc=2
```

The revision exists in `--repo`; git looked in `GIT_DIR` instead. In an environment that exports
`GIT_DIR` (a git hook, a worktree helper, a CI step), every `rev`-mode read in all four tools comes
from the wrong repository while the output still prints `rev=`.

This is the one finding that directly crosses the lane's hard boundary: the tools are declared
"selftest writes only under the caller TMPDIR" (F8), and under an inherited `GIT_DIR` they commit
into a live repo. Minimal remediation: build the child env explicitly
(`env = {k:v for k,v in os.environ.items() if not k.startswith("GIT_")}` plus
`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`) for every git and every executed program.

---

## (d) Environment, credentials, absolute operator paths on stdout

**No credential printing and no environment dump.** Nothing in the four files prints
`os.environ`, a token, a key or a URL. `grep` for `shell=True|os.system|os.popen|pickle|yaml.load`
returns nothing (rc 1).

### F10 — LOW — absolute paths and child stderr do reach stdout; children get the whole environment

- `count-c1.py` setup error echoes the resolved repo path:
  `C1_SETUP repo is not a git checkout: /tmp/sent44.AwC2Gs/not-a-repo`.
- the success line echoes the caller's `--ledger` verbatim:
  `ledger=/tmp/sent44.AwC2Gs/outside.tsv rows=12 classes=…` (an absolute operator path in the
  published transcript).
- `count-c1.py:120` puts the row's `stderr` (first 80 bytes) into the mismatch detail, which is
  printed: a ledger row's error text is laundered into the gate's stdout. With F1 in play, a row
  could print anything there.
- `count-c2.py:111` `env = dict(os.environ)` — every audited counter, mutant and the auditor run
  with the caller's complete environment (proved: `evil.py` used `$HOME`). Credentials are not
  printed, but they are handed to code read out of the measured revision. A lane that treats its
  own counters as untrusted (which is the premise of C2's mutant arm) should pass a minimal env.

### F9 — LOW — `MORI_GATE_REGISTRY` substitutes the auditor's bytes

`count-c2.py:251-256` (`auditor_bytes()`) prefers `$MORI_GATE_REGISTRY` over the checkout, and
`_base_files()` bakes those bytes into the fixture repo as `tools/mori-gate-registry.py`, which is
then executed (`count-c2.py:141`). Observed:

```
$ MORI_GATE_REGISTRY=/tmp/sent44.AwC2Gs/fake-auditor.py python3 $S/bin/count-c2.py --selftest
selftest PASS registered_conformant_met
selftest FAIL unregistered_counter_unmet: []
selftest FAIL no_selftest_mode_unmet: ['selftest_tally']
C2_SELFTEST pass=3 fail=2
substituted auditor executed: ran
```

The env-named file ran. I did **not** get a green tally from a constant-green fake — the negative
arms have teeth against it (a fake would have to read `SKILL.md` to satisfy `unregistered`), so the
practical risk is low. It is still an environment-controlled code path inside the gate that
certifies self-tests. The measurement path is unaffected: `evaluate()` materializes the auditor
from committed bytes.

---

## (e) Remediation, host mutation, fleet writes

**The tools' own code writes nothing into the repo.** Every write-mode `open`/`chmod`/`makedirs`
targets a `tempfile.mkdtemp` tree (`count-c1.py:171-183,219-276`, `count-c2.py:85-87,174-176,231-242`,
`count-c3.py:136,178-188`, `mori-gate-registry.py:170-178`), and every `rmtree` is
`ignore_errors=True` on a `mkdtemp` path. No `git add/commit/push/checkout/stash/reset` is issued
by any tool **except** inside the self-test arms.

But the hard boundary holds only for that own code, under a clean environment:

1. **F2** — the self-test's `git add`/`git commit` follow `GIT_DIR`; proved to commit into a live
   repo (1 → 7 commits in three separate tools). This is host mutation and, if `GIT_DIR` pointed at
   the lane, a lane write.
2. **F1** — ledger rows write anywhere (`tee`, `>`), inside or outside the repo, including
   `.git/hooks/` or `$HOME`.
3. **F3** — the census script runs with `cwd=repo` and the caller's environment; my stub wrote a
   marker. A census that wrote would be indistinguishable from the real one.
4. **F6** — a row leaves a detached process behind after the gate exits.
5. **F4** — `core.fsmonitor` from the measured repo executes.

Nothing here is *remediation* logic (no tool fixes, patches or re-runs anything), and nothing
touches the fleet repo. The boundary risk is entirely "executed code inherits the operator's
privileges".

### F3 — HIGH — C3's census is an uncommitted, out-of-lane program

`count-c3.py:299`:

```python
census = args.census or os.path.join(os.path.dirname(repo), "scripts", "sources-census.sh")
```

For the real lane this resolves to an **absolute path outside the measured repo and outside the
revision**:

```
repo              = /home/vgpnk/Projects/shokunin/mori-shokunin
c3 default census = /home/vgpnk/Projects/shokunin/scripts/sources-census.sh   exists=True
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree -r --name-only HEAD -- scripts/
(empty — scripts/ is not tracked in the lane)
```

and `count-c3.py:139-141` runs `bash <that path> validate --file <staged copy>` with `cwd=repo`
and the inherited environment. `C3=met`'s `census_ok` therefore certifies a program that is not
part of the measured revision, and a reviewer who copies the lane to another directory silently
gets a different census (`<copy>/../scripts/…`, absent → `exit=127` → `C3=unmet`; I observed
exactly that in my sandbox: `check census_ok FAIL (exit=127)`).

Worse, any exit-0 program satisfies it:

```
$ python3 $S/bin/count-c3.py 7e61090c… --repo $R3 --entry corpus/knowledge/fixture-entry.md --row S901 --census /tmp/sent44.AwC2Gs/hostile-census.sh
check entry_present    PASS (193 bytes)
check entry_meta       PASS (sources S901)
check rows_present     PASS (rows S901 mined)
check census_ok        PASS (exit=0)
check readme_row       PASS (names entry)
C3=met
$ cat /tmp/sent44.AwC2Gs/CENSUS_RAN
hostile census ran as vgpnk cwd=/tmp/sent44.AwC2Gs/repo3
```

(`--census /bin/true` fails only because `bash /bin/true` is 126, i.e. by accident of file type,
not by design.)

This is an asymmetry inside one round: `count-c2.py` materializes the auditor **from committed
bytes** (`count-c2.py:132`) precisely so the audited program is part of the revision; `count-c3.py`
does the opposite. Minimal remediation: stage the census from the revision
(`read_at(repo, rev, "tools/sources-census.sh")` or wherever it is committed), materialize it under
TMPDIR, and refuse a `--census` path that is not repo-relative.

### F8 — MEDIUM — the registry's declared write scope is false

`SKILL.md` rows 183–186 declare:

- C1: "stdout only; reads the repo at `--rev`; the selftest writes only under the caller TMPDIR"
- C2: "stdout only; counter bytes materialize under the caller TMPDIR; nothing in the repo is written"
- C3: "stdout only; the registry copy handed to the census is materialized under the caller TMPDIR"
- gate registry: "stdout only; reads the registry and the audited paths at `--rev`; the selftest writes only under the caller TMPDIR"

Against F1–F6 these are wrong as written: the C1 gate executes arbitrary pipelines (writes
anywhere), the C3 gate executes an arbitrary program (writes anywhere), and all four self-tests
write wherever `GIT_DIR` says. A "write scope" cell is the one declaration a reviewer is entitled
to rely on; it must say "executes committed ledger rows / caller-named census / audited counters
with the caller's privileges, unsandboxed" or the claim should be withdrawn. Since the table is
the C2 claim's own subject, this is also a *self-referential* defect: the gate standard being
audited overstates what the gates do.

---

## Scope notes

- I did not evaluate C1/C2/C3's correctness predicates (row arithmetic, gate cells, corpus
  coverage) — only trust boundaries. Other seats hold those.
- `count-c3.py`'s `used-by` and README checks are substring tests (`count-c3.py:150`), so a README
  line naming the entry anywhere passes; that is a weakness of the predicate, not of the trust
  boundary, and is out of scope here.
- No installs or upgrades were needed for this review; nothing was installed. No pacman, no
  `uv tool`, no binary fetch.
- Scratch: `/tmp/sent44.AwC2Gs` (disposable). This seat wrote nothing under
  `/home/vgpnk/Projects/shokunin` except this file (sibling seats' working-tree edits to `LOG.md`,
  `SCORECARD.md` and `corpus/` are theirs, not mine); no git/jj command in the lane repo was
  mutating.

## Smallest remediations, ordered

1. Build an explicit child environment for every spawn: strip `GIT_*`, set
   `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1` (fixes F2, F4, and the credential reach
   in F10).
2. Replace the `bash -c` ledger string with a parsed argv plus a fixed consumer (F1, F6 —
   `start_new_session=True` + group kill).
3. Stage the census from the revision, not from `<repo>/../scripts` (F3).
4. Confine every `--path` argument to `realpath` under `repo`, for `WORK` as well (F5).
5. Print `repo=`, `min_rows=`, `min_classes=`, `ledger=`, `mutants_dir=`, `coverage_map=`, `row=`
   on the verdict line (F7), and correct the four write-scope cells (F8).

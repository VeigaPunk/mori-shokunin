# RevengerAuditorHistory — the two round-44 instrument defects, from committed history and bytes

Seat: revenger (leaf member; no subagent dispatch). Round 45, wave 1.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Measured bytes: `554ff416459c92f0dea9762f834a556df2990187` (round-44 closure = round-45 entry tip).

Every executed probe ran on `git archive 554ff416` extracted under
`.ufo/waves/round-45/tmp/RevengerAuditorHistory/sb`, **not** on the lane worktree: this wave's
executors are already rewriting the instruments (`git status --porcelain` shows
` M tools/mori-gate-registry.py` from `ExecRegistryAuditor` and, after my probes,
` M tools/mori-silence-cases.sh` / `mori-round19-regressions.py` / `mori-routed-check.py` from
`ExecSelftestModes`), so a worktree read would not be the frozen instrument. Nothing below
describes the in-progress v2s.

Digest basis (matches `.ufo/waves/round-44/evidence/freeze-r44.txt:9,14`):

```
743996b11d19261b87e3ea6c0d0be4c0e5e6750d05f6d603af51dc1a7e125a1f  tools/mori-gate-registry.py
f9b1e2bf999b8c8e4d6bef245899c8c5865848b6d7f410d34f5c52b9a2e76d05  SKILL.md   (at 554ff416)
```

---

## 1. Defect 1 — the auditor read exactly one registry table and stopped at the next `## `

### 1.1 History

```
$ git -C …/mori-shokunin log --follow --format='%h %ad %s' --date=iso -- tools/mori-gate-registry.py
7cb59c68 2026-10-25 03:31:03 -0300 round-44: frozen contract and instruments — C1 figure ledger, C2 gate standard, C3 corpus coverage
```

There is **no later edit** on HEAD's history: `git log --diff-filter=M -- tools/mori-gate-registry.py`
is empty, and the bytes at `7cb59c68`, `554ff416` and `HEAD` are the same `743996b1…`.
The only other refs that carry the file are three orphan attempt commits whose parent is
`1429c791` (round-43 tip), `git merge-base --is-ancestor <c> HEAD` → exit 1 for all three:

```
ca0e5628  full freeze (same 16 files as 7cb59c68)   empty message
ddd247a4  SKILL.md + tools/mori-gate-registry.py     empty message   ← the instrument-only half
e8736a86  full freeze (same 16 files as 7cb59c68)   empty message
```

So the introducing commit message is the only intent record, and it carries **no body**
(`git log -1 --format=%B 7cb59c68`, `cat -A`):

```
round-44: frozen contract and instruments M-bM-^@M-^T C1 figure ledger, C2 gate standard, C3 corpus coverage$
$
```

### 1.2 The bytes that decide the scope

`git show 7cb59c68:tools/mori-gate-registry.py` (frozen v1, 308 lines):

```
  4  Checks the lane's stated gate standard (SKILL.md section `## Gates`) against
  5  committed bytes: for every audited tool path, a registry row must name it in its
```

```
 81  def parse_gate_table(text):
 82      """Rows of the `## Gates` table, header located by its field names."""
 83      lines = text.splitlines()
 84      start = None
 85      for i, line in enumerate(lines):
 86          if line.strip().lower() == "## gates":
 87              start = i
 88              break
 ...
 92      for line in lines[start + 1:]:
 93          stripped = line.strip()
 94          if stripped.startswith("## "):
 95              break
 96          if not stripped.startswith("|"):
 97              continue
 98          cells = split_row(stripped)
 99          low = [c.lower() for c in cells]
100          if header is None:
101              if len(cells) >= 8 and low[0] == "name" and low[1] == "kind":
102                  header = low
103              continue
104          if set("".join(cells)) <= {"-", ":"}:
105              continue
106          rows.append(cells)
```

Two facts follow from those lines, and both are load-bearing:

1. The scan window is `lines[start+1:]` (the body of `## Gates`) and ends at the first
   **level-2** heading (`stripped.startswith("## ")`). A registry table under any other
   `## ` heading is never read.
2. Once `header` is set, the header test at 100–103 is skipped for the rest of the section,
   so a *second* table header inside `## Gates` would be appended as a data row (line 106),
   not recognised as a new table. The design assumes exactly one table per `## Gates`.

The three read/report call sites that consume this are v1 lines 114–151 (`audit()`) and 296–304
(`main()`): one `header, rows = parse_gate_table(...)` per run, no table count is printed.

### 1.3 Was the later tables' eight-cell shape anticipated?

No — it was **already there**, in the same file, at the parent of the introducing commit, with
the *identical* header line:

```
$ git show 7cb59c68^:SKILL.md | grep -n '| name | kind |'
162:| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
520:| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
584:| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
639:| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
714:| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
792:| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
877:| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
```

The commit added only four lines, all inside the Gates table
(`git diff --stat 7cb59c68^ 7cb59c68 -- SKILL.md` → `1 file changed, 4 insertions(+)`).
At `554ff416` the same seven headers sit at 162, 524, 588, 643, 718, 796, 881.

What was **not** anticipated is the *test* case. All six selftest arms build a registry through
`_registry(rows)` (v1:163–165), which emits exactly one table under `## Gates`; the arms are
`registered_row_met, missing_cell_rejected, unresolved_entry_rejected, unregistered_path_rejected,
no_selftest_rejected, seven_cell_row_rejected` (v1:258–263). There is no second-table arm and no
`tables=` output, so the shape was never exercised.

Population arithmetic at `554ff416` (measured by reusing the file's own `split_row`/header test):

```
tables: [(162, 23), (524, 2), (588, 1), (643, 2), (718, 3), (796, 1), (881, 11)]
total_rows: 43   gates_rows: 23   later_rows: 20
```

**20 of the file's 43 eight-cell registry rows were invisible to the v1 audit.**

### 1.4 Observed behaviour (v1, `--rev 554ff416`, frozen bytes)

```
audit tools/mori-silence-cases.sh   PASS (row 'silence oracle': 8 cells, entry resolves, --selftest present)
audit tools/mori-gate-registry.py   PASS (row 'r44 gate registry (C2)': 8 cells, entry resolves, --selftest present)
audit tools/mori-census.sh          PASS (row 'drift pin': 8 cells, entry resolves, --selftest present)
audit tools/mori-blind-check.sh     FAIL (unregistered: no row names mori-blind-check.sh)     rc=1
audit tools/mori-source-drift.py    FAIL (unregistered: no row names mori-source-drift.py)    rc=1
audit tools/mori-pressure.py        FAIL (unregistered: no row names mori-pressure.py)        rc=1
```

`mori-blind-check.sh` is registered at 796, `mori-source-drift.py` at 881 (twice), `mori-pressure.py`
at 643 — all under later `## ` headings, all reported unregistered. A direct probe of the frozen
parser over the same bytes returns `rows=23` while the file has 7 eight-cell headers.

(`audit tools/mori-census.sh` also shows a second, separate defect the brief did not ask about:
attribution goes to the *shortest* matching entry cell, `drift pin`, not to `census`.)

### 1.5 Intent — evidenced

- `7cb59c68:.ufo/waves/round-44/contract.md` §P-C2, predicate sentence (singular):
  "`SKILL.md`'s **gate table** carries a row whose entry cell names its repo-relative path…"
- `554ff416:SKILL.md` row 184, pinned-values cell (singular, self-documenting the limit):
  `in-script fixture registry rows; the audited surface is this SKILL.md \`## Gates\` table at \`--rev\``
- The same contract's witness names the intent — catch a counter with *no* row at all:
  "`REGISTRY=unmet` naming both round-43 counters as unregistered and without a selftest mode."

### 1.6 Intent — inferred (flag)

`[INFERENCE]` The author scoped "the gate standard" to the `## Gates` section deliberately
(each later table is a round-specific amendment with its own wording), and did not consider that
the same declared population includes tools whose only row lives in a later table. The code reads
as if the file were assumed to hold one registry; nothing in the commit message, the contract, or
the six arms records a decision to read only the first table.

---

## 2. Defect 2 — why the silence oracle's self-test cell says "itself (hermetic case table)"

### 2.1 The cell at `554ff416` (SKILL.md:166), verbatim

```
| silence oracle | gate | `bash tools/mori-silence-cases.sh` | 0 clean (all matched) · 1 failed · 2 could-not-evaluate | itself (hermetic case table, 28 cases) | case table in-script | temp fixtures | mori |
```

### 2.2 History

```
$ git -C … log -S'--selftest' --format='%h %ad %s' --date=iso -- tools/mori-silence-cases.sh
3da84149 2026-10-15 13:07:37 -0300 round-2: admit goal-wave coverage move — oracle reconciled (505a7504), seven surface notes, watch receipts, authorship proof
```

`git log --diff-filter=A -- tools/mori-silence-cases.sh` returns the same commit: `3da84149` is
the file's **creation** commit, and the only commit `-S'--selftest'` matches. The string has never
been added or removed since. Its only occurrence in the file is a comment, line 20:

```
#   Each case runs the actual census CLI (bash "$CENSUS", no --selftest) and
```

That is the string saying the census is invoked **without** `--selftest`. There was never an
argv branch, and none was ever removed.

### 2.3 What the tool itself promises (bytes)

```
  6  # Usage:
  7  #   bash tools/mori-silence-cases.sh [path-to-census]
  8  #     census path default: <this dir>/mori-census.sh
  9  #     exit 0 iff every case matched; setup failure exits 2.
```

```
178  CENSUS=${1:-$SCRIPT_DIR/mori-census.sh}
179  [ $# -gt 1 ] && { printf 'usage: mori-silence-cases.sh [path-to-census]\n' >&2; exit 2; }
180  [ -f "$CENSUS" ] && [ -r "$CENSUS" ] || { printf 'mori-silence-cases: census not readable: %s\n' "$CENSUS" >&2; exit 2; }
```

There is one positional argument and no flag parsing. Its own commentary states the write scope
(line 168): `# Writes happen only under the fresh mktemp work dir; census must not mutate`.

### 2.4 Observed

```
$ bash tools/mori-silence-cases.sh --selftest
mori-silence-cases: census not readable: --selftest
rc=2
$ bash tools/mori-silence-cases.sh --selftest extra
usage: mori-silence-cases.sh [path-to-census]
rc=2
$ MORI_SHUFFLE_SEED=7 MORI_RUN_NONCE=11 bash tools/mori-silence-cases.sh
… MORI_SILENCE_CASES: matched=28 total=28        rc=0, 5.26 s
```

The table is in-script (`# CASE REGISTRY + SHUFFLED RUNNER — the 28 ids in source order`, line
1140); the 28 ids are printed in `CASE_ORDER=` on every run. "itself (hermetic case table, 28
cases)" is therefore an accurate description **of the tool**: the tool is a test harness, and its
self-test is its own table. It is not a `--selftest` argv contract, and never was.

### 2.5 Why round 44 credited it anyway

v1 line 146:

```
146          if b"--selftest" not in body:
147              results.append((target, False, "row %r tool has no --selftest mode" % label))
```

A byte-substring test over the whole file — satisfied by the line-20 comment. And the row
attribution did not come from `entry_names` at all: a probe of the frozen functions gives

```
entry_names("`bash tools/mori-silence-cases.sh`", "tools/mori-silence-cases.sh")  → False
entry_names("`bash tools/mori-census.sh` (`MORI_SHOKUNIN_ROOT=…`)", "tools/mori-census.sh") → False
entry_names("`python3 tools/mori-gate-registry.py --rev …`", "tools/mori-gate-registry.py") → True
```

`lstrip("`")` removes the leading backtick but the trailing backtick sits directly after the
path, defeating the pattern's `(?:\s|$)` terminator (v1:77–78). The PASS came from the substring
fallback at v1:125–126 (`if len(r) >= 3 and (base in r[2] or name in r[2])`). Two independent
false credits in one verdict line:

```
audit tools/mori-silence-cases.sh   PASS (row 'silence oracle': 8 cells, entry resolves, --selftest present)
```

### 2.6 Intent — evidenced / inferred

Evidenced: usage promises one positional arg; `-S` history has one commit; the sole `--selftest`
is a comment saying "no --selftest"; `--selftest` as argv is a setup error (rc 2).
`[INFERENCE]` The registry cell was honest about the tool, while the auditor's check was written
for counters with a real `--selftest` argv; nobody reconciled the two, and round-44 P-C2 never
required an argv branch (that requirement is new in round-45 P-C2 item 4).

---

## 3. Write scope — what F8 actually wrote, and what each instrument actually writes

### 3.1 F8 verbatim (`.ufo/waves/round-44/w1/SentTools.md:433–446`)

```
### F8 — MEDIUM — the registry's declared write scope is false

`SKILL.md` rows 183–186 declare:

- C1: "stdout only; reads the repo at `--rev`; the selftest writes only under the caller TMPDIR"
- C2: "stdout only; counter bytes materialize under the caller TMPDIR; nothing in the repo is written"
- C3: "stdout only; the registry copy handed to the census is materialized under the caller TMPDIR"
- gate registry: "stdout only; reads the registry and the audited paths at `--rev`; the selftest writes only under the caller TMPDIR"

Against F1–F6 these are wrong as written: the C1 gate executes arbitrary pipelines (writes
anywhere), the C3 gate executes an arbitrary program (writes anywhere), and all four self-tests
write wherever `GIT_DIR` says. A "write scope" cell is the one declaration a reviewer is entitled
to rely on; …
```

**Count correction.** The brief asks for "the exact **two** SKILL.md write-scope cells" F8 called
false. F8 names **four** (rows 183–186), and there is no other F8 in round 44 (`grep -rn F8
.ufo/waves/round-44/` matches SentTools plus two unrelated uses in `ScribeEntryDraft`/`ScribeLesson`).
Of those four, exactly **one** belongs to an instrument this note reverse-engineers:
row **184**, the gate registry. The silence oracle's cell is row **166** and F8 **did not** name it.
I report F8's four verbatim, then the two instrument cells (166, 184) with observed verdicts.

Cells at `554ff416`, verbatim (write-scope column only):

| line | row | write-scope cell |
|---|---|---|
| 183 | r44 figure ledger (C1) | `stdout only; reads the repo at --rev; the selftest writes only under the caller TMPDIR` |
| 184 | r44 gate registry (C2) | `stdout only; reads the registry and the audited paths at --rev; the selftest writes only under the caller TMPDIR` |
| 185 | r44 gate conformance (C2) | `stdout only; counter bytes materialize under the caller TMPDIR; nothing in the repo is written` |
| 186 | r44 corpus coverage (C3) | `stdout only; the registry copy handed to the census is materialized under the caller TMPDIR` |
| 166 | silence oracle | `temp fixtures` |

Round 44's own verifier disagreed with F8 and could not see the defect: `RevRegistryRows.md:78`
marks C1/registry/C2 write scope `✓` and C3 `~`, because it hashed a pristine clone before/after
the entry commands and selftests **with a clean environment** — no inherited `GIT_DIR`. That is the
one condition that hides the escape, so the round shipped on a green verifier cell.

### 3.2 `tools/mori-gate-registry.py` — observed writes

**(a) Production audit** (`--rev 554ff416 --audit tools/mori-silence-cases.sh`, under
`strace -f -y -e trace=%file`, `TMPDIR` set to an empty scratch dir): the only writable
descriptor opened outside the trace target is `/dev/null`; the TMPDIR stayed empty. Reads are
`git cat-file -e`, `git show`, and `open(..., "rb")`. Verdict: "stdout only; reads the registry and
the audited paths at `--rev`" is **TRUE**.

**(b) `--selftest`, clean environment**: zero absolute write targets outside the caller TMPDIR
(the filter over the trace returns 0), all `mkdir(".git/…")` writes on relative paths, each
preceded by `chdir("$TMPDIR/grst-*/repo")` (66 `chdir` events, 6 `grst-*` trees); the trees are
removed by `shutil.rmtree`. Verdict: "the selftest writes only under the caller TMPDIR" is
**TRUE in a clean environment**.

**(c) `--selftest` with an inherited `GIT_DIR`** (F2's condition):

```
$ git init -q -b main $F && git -C $F commit -q --allow-empty -m base
$ GIT_DIR=$F/.git python3 tools/mori-gate-registry.py --selftest
GATE_REGISTRY_SELFTEST pass=6 fail=0      rc=0

foreign repo before: 8dd8433f91056fd3eb1543ff5c64b6b98bb8dce0
foreign repo after : eff219d34558752fa4a963f3fe8291e5bff2192e0   (+6 commits)
$ git -C $F log --oneline -n 7
eff219d fixture
992e076 fixture
6b52664 fixture
003062e fixture
b7971ab fixture
be694a1 fixture
8dd8433 base
$ git -C $F status --porcelain
 D SKILL.md
 D tools/fixture-tool.sh
```

Six commits, refs/logs, objects **and the foreign index** landed in a repository outside the
caller TMPDIR, while the tool printed `pass=6 fail=0`. The cell is **FALSE as an unconditional
claim** (F8's "writes wherever `GIT_DIR` says" is exact).

**(d) Mechanism** for F8's other three cells, from the committed bytes (code reading, not a run
of a hostile input):

```
count-c1.py:113-115   subprocess.run(["bash", "-c", full], …, cwd=repo)          # arbitrary pipeline, cwd = measured repo
count-c2.py:91-95     run_script(..., cwd=cwd or os.path.dirname(path))          # audited counter runs with cwd inside the repo
count-c3.py:139-141   subprocess.run(["bash", census, "validate", "--file", staged], …, cwd=repo)  # census runs with cwd = measured repo
```

and reproduced for all four instruments under an inherited `GIT_DIR` (each selftest still rc 0 and
its own tally):

```
count-c1 --selftest  C1_SELFTEST pass=6 fail=0   foreign repo +6  commits
count-c2 --selftest  C2_SELFTEST pass=5 fail=0   foreign repo +35 commits
count-c3 --selftest  C3_SELFTEST pass=6 fail=0   foreign repo +6  commits
gate-registry        …pass=6 fail=0              foreign repo +6  commits
```

### 3.3 `tools/mori-silence-cases.sh` — observed writes

- `--selftest`: rc 2, "census not readable: --selftest", no writes (measured before the full run).
- Full table (pinned seed/nonce), under `strace`, with the caller TMPDIR set to an empty dir:
  - `rc=0`, `MORI_SILENCE_CASES: matched=28 total=28`, 10.6 s traced;
  - the work dir is **hardcoded**: line 283 `WORK=$(mktemp -d /tmp/mori-silence-cases.XXXXXX)`;
    every absolute write target is under `/tmp/mori-silence-cases.rl8Nla/…` (311 write events);
  - **zero** writes under the caller TMPDIR — the tool ignores `TMPDIR`;
  - the only absolute write targets outside that tree are `mkdir("/tmp")` → `EEXIST` and
    `open("/dev/tty", O_RDWR)` → `ENXIO` (bash job control), i.e. no write;
  - `chdir("case.XXX")` accounts for every relative `.git/…` write;
  - after exit: no `/tmp/mori-silence-cases.*` leftovers (trap at line 285 runs
    `rm -rf -- "$MORI_CASES_WORK"`); a full 11,824-file digest of the sandbox before/after differs
    by 0 lines.

Verdict on row 166: **TRUE as written**. The precise scope is "temp fixtures under `/tmp`, removed
on exit; nothing in the repo" — the cell does not claim the caller TMPDIR, and the tool does not
honour it.

### 3.4 Verdict table

| cell | F8 called it false | observed |
|---|---|---|
| 184 gate registry (`stdout only; reads … at --rev; the selftest writes only under the caller TMPDIR`) | yes | production read-only (strace) and TMPDIR-only in a clean env; **FALSE** under an inherited `GIT_DIR` (+6 commits in a foreign repo) |
| 166 silence oracle (`temp fixtures`) | no (not named) | **TRUE**; writes only `/tmp/mori-silence-cases.*`, removed on exit, repo digest unchanged; ignores caller TMPDIR |
| 183 C1 / 185 C2 / 186 C3 | yes | not run against hostile inputs by this seat; mechanism quoted above (arbitrary child, cwd inside/at the measured repo), and all three selftests reproduced F8's `GIT_DIR` claim (+6/+35/+6 commits) |

---

## 4. Copy-paste prose for the round-45 lesson (ScribeLesson M1/M2)

> **M1 — scope in the declaration, not in the audit** (round 44). The gate-registry auditor read
> exactly one registry table: its parser was bounded to the `## Gates` section and stopped at the
> next `## ` heading (`tools/mori-gate-registry.py` @ `7cb59c68`, lines 92–95; docstring line 82
> "Rows of the `## Gates` table"). At the same revision `SKILL.md` carried **seven** tables with the
> identical eight-cell header — six of them pre-dated the commit — so 20 of 43 registry rows were
> outside the audit; `tools/mori-blind-check.sh`, `tools/mori-source-drift.py` and
> `tools/mori-pressure.py` each reported `unregistered` while their rows sat at SKILL.md 796/881/643.
> The round-44 contract said "gate table" (singular) and the row said "the audited surface is this
> SKILL.md `## Gates` table", so the limitation was *declared*; no arm tested a second table.
> Captured by: **none** (the r44 P-C2 predicate was written to the same single-table assumption).
> Fix with the proof it can fail: a table census printing `tables=<n>` and a `second_table_registered`
> arm, plus `tables=<n>` in the receipt.
>
> **M2 — a token is not a branch** (round 44). The auditor credited a tool's `--selftest` by byte
> substring over the whole file (`mori-gate-registry.py` @ `7cb59c68`, line 146). The silence oracle
> never had a `--selftest` argv branch: the only occurrence is comment line 20 "(bash \"$CENSUS\", no
> --selftest)", its usage is `[path-to-census]`, and `--selftest` as argv is a setup error
> (`mori-silence-cases: census not readable: --selftest`, rc 2). The row's self-test cell said
> "itself (hermetic case table, 28 cases)" — honest about the tool, but the verifier read it as an
> argv contract. Its row also passed attribution only through the substring fallback, because the
> entry cell is a bare backticked command and `entry_names` returned False for it.
> Captured by: **none**. Fix with the proof it can fail: a comment-only `--selftest` fixture must
> yield `no_selftest`, and the row must quote the argv.
>
> **M3 — a declaration is not a sandbox** (round 44). F8's four write-scope cells say the selftests
> write only under the caller TMPDIR; under an inherited `GIT_DIR` all four commit into a foreign
> repository (this seat: +6/+35/+6/+6 commits, each selftest still green). The round-44 verifier
> marked the same cells ✓ because it hashed a pristine clone in a clean environment. Captured by:
> the round-44 verifier's method (clean-env hashing), not by any arm.

---

## 5. Reconstructed contract, divergences, confidence (revenger format)

**Last-known-good invariant.** A registry row is the only place a tool's obligations are declared;
the audit exists to check a *declared standard* against committed bytes, over the declared
population, with attribution. v1 satisfies "row exists and names the path" only for rows in the
first table, and satisfies "--selftest present" only as a byte token.

**Divergences reconstructed.**
1. Population vs table scope: audit input is a caller list, parser scope is one section → later
   tables cannot register their own tools (observed: 3 of 3 sampled).
2. Token vs branch: `b"--selftest" in body` cannot distinguish a comment (observed).
3. Attribution: `entry_names` fails on bare backticked commands (observed), so the substring
   fallback decides; it also picks the *shortest* matching cell (`census` → `drift pin`).
4. Declaration vs execution: "selftest writes only under the caller TMPDIR" holds only while the
   caller's environment is clean; `GIT_DIR` redirects the writes (observed, 4/4 instruments).

**Intent you can evidence.** r44 P-C2 asked for "`SKILL.md`'s gate table" (singular) and the row's
pinned-values cell said "the audited surface is this SKILL.md `## Gates` table at `--rev`":
single-table scope was *declared*, so the defect is a scope that under-counts the declared
population, not a hidden behaviour. The silence oracle's cell was correct about the tool; the
auditor's test was written for a different instrument shape. F8's write-scope claim was a
hypothesis the same round's verifier contradicted with a clean-environment hash.

**Intent you cannot evidence (inference).** Whether the author noticed the six pre-existing tables
and consciously excluded them; whether the auditor's single-table read was a deliberate "gate
standard only" decision or an unexamined assumption. Nothing in `7cb59c68`'s message (empty body),
the contract, the six arms, or the row text records it.

**Confidence.** High for the mechanisms and for every pasted observation (all rerunnable from the
commands below). High that the silence oracle never had `--selftest`. High that `GIT_DIR` defeats
the registry cell. Medium on any statement about author intent. The brief's "two cells" is
contradicted by F8's text (four cells); I report the discrepancy rather than pick two silently.

---

## 6. Reproduction commands (all read-only against the lane; writes only under my scratch)

```sh
L=/home/vgpnk/Projects/shokunin/mori-shokunin
T=$L/.ufo/waves/round-45/tmp/RevengerAuditorHistory
git -C $L log --follow --format='%h %ad %s' --date=iso -- tools/mori-gate-registry.py
git -C $L log --diff-filter=M --format='%h %s' -- tools/mori-gate-registry.py
git -C $L log -S'--selftest' --format='%h %s' -- tools/mori-silence-cases.sh
git -C $L show 7cb59c68:tools/mori-gate-registry.py | cat -n | sed -n '81,107p'
git -C $L show 7cb59c68^:SKILL.md | grep -n '| name | kind |'
git -C $L archive 554ff416 | tar -x -C $T/sb
python3 $T/sb/tools/mori-gate-registry.py --rev 554ff416 --audit tools/mori-blind-check.sh   # rc 1, unregistered
bash $T/sb/tools/mori-silence-cases.sh --selftest                                            # rc 2, not readable
GIT_DIR=$T/foreign/.git python3 $T/sb/tools/mori-gate-registry.py --selftest                 # rc 0, commits into $T/foreign
MORI_SHUFFLE_SEED=7 MORI_RUN_NONCE=11 bash $T/sb/tools/mori-silence-cases.sh                 # rc 0, 28/28
```

## 7. Scratch and tooling

Scratch: `.ufo/waves/round-45/tmp/RevengerAuditorHistory/` (my own; created by me).
`sb/` = `git archive 554ff416` extraction; `foreign*/` = the `GIT_DIR` targets (`foreign`,
`foreign-c1`, `foreign-c2`, `foreign-c3`, each mutated by the measurement and kept as a receipt);
`logs/gr-prod.strace`, `logs/gr-st.strace`, `logs/sc.strace` = the three traces;
`logs/sc-writes-outside-work.txt`, `logs/gr-st-writes-outside-tmpdir.txt` = the filtered write lists;
`skill554.md`, `skill_parent.md` = `SKILL.md` at `554ff416` and at `7cb59c68^`;
`sb-before.sha`/`sb-after.sha` = the 11,824-file digests; `sc-run.out`/`sc-run2.out`,
`cc{1,2,3}-gitdir.out` = run receipts. The raw `sc.strace` (29 MB) is kept only as evidence for
the write-path counts above.

Tooling: **nothing installed or upgraded** (no pacman, no `uv tool`, no binary fetch). Used
`python3` 3.14.8, `git` 2.56.0, `strace`, `bash` 5.3.20 already on the host. No network.

I edited no lane file other than this report; `SKILL.md`, `contract.md`, `tools/mori-gate-registry.py`
(the worktree ` M ` is the v2 executor's, not mine), and every other seat's file were untouched.

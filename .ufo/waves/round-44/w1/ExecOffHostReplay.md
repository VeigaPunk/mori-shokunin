# Exec — off-host replay: the frozen instruments run from a `/tmp` clone, and their green arms are not tied to the lane path

lane: mori · round: 44 · wave: 1 · role: executor (leaf, one labrat allowed, none used) · date: 2026-10-25
lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin` · measured revision: freeze commit
`7cb59c6891d4f5d0266fe062565f094da835dc84`
(`round-44: frozen contract and instruments — C1 figure ledger, C2 gate standard, C3 corpus coverage`)
lane tip while this seat ran: `30fe06d1e2593e18280d83e7e3086f4d678762df` (the integrator committed
seat bytes during the wave; the frozen instruments and `SKILL.md` are byte-identical between
`7cb59c68` and `30fe06d1` — `git diff --stat 7cb59c68..HEAD -- .ufo/waves/round-44/count-c*.py
tools/mori-gate-registry.py .ufo/waves/round-44/fixtures SKILL.md` prints nothing)
fleet repo: `/home/vgpnk/Projects/shokunin` (read-only, nothing written)
sandbox: `/tmp/mori44-offhost.dZeeKl` — `clone` (freeze commit), moved to
`/tmp/mori44-offhost.dZeeKl/relocated/nested/replay`; `tipclone` (landed tip `30fe06d1`)
host `plazir27` · Python 3.14.8 · git 2.56.0 (the freeze record `evidence/freeze-r44.txt` also names Python 3.14.8)

Scope: QUALITY 115 — "A frozen instrument's green control must replay with `--repo` pointing at a
scratch clone, not only a hardcoded home path." I cloned the lane at the freeze commit into a
`mktemp -d` sandbox, ran every frozen instrument's `--selftest` **from the clone**, ran
`count-c2.py <freeze-rev> --repo <clone>` against the clone, moved the clone and re-ran, and
grepped the instruments for absolute paths. When the integrator landed the round's artifacts, the
same replay was repeated at that tip from a second `/tmp` clone (§5.3, §F2). Nothing was edited
except this report; no frozen instrument, fixture, `SKILL.md`, `SCORECARD.md`, `LOG.md` or
`corpus/` file was touched; no `git add/commit/push/checkout/stash/reset` and no mutating jj
command was run in the lane. The only commit made anywhere is a single probe commit **inside the
`/tmp` clone** (§5.2), which the lane does not know about.

---

## 1. The sandbox clone and the frozen bytes

```
$ SBOX=$(mktemp -d /tmp/mori44-offhost.XXXXXX); echo "SBOX=$SBOX"
SBOX=/tmp/mori44-offhost.dZeeKl
$ git clone -q /home/vgpnk/Projects/shokunin/mori-shokunin "$SBOX/clone" \
    && cd "$SBOX/clone" && git checkout -q 7cb59c6891d4f5d0266fe062565f094da835dc84
$ git rev-parse HEAD
7cb59c6891d4f5d0266fe062565f094da835dc84
$ git status --porcelain | wc -l
0
```

The checkout was made **inside the clone**; the lane's own `HEAD` was never moved. The clone's
instrument bytes are the frozen bytes:

```
$ cd /tmp/mori44-offhost.dZeeKl/relocated/nested/replay   # same tree, after the move in §5
$ sha256sum -c .ufo/waves/round-44/evidence/freeze-r44.txt
.ufo/waves/round-44/contract.md: OK
.ufo/waves/round-44/count-c1.py: OK
.ufo/waves/round-44/count-c2.py: OK
.ufo/waves/round-44/count-c3.py: OK
tools/mori-gate-registry.py: OK
.ufo/waves/round-44/fixtures/figures-r43.tsv: OK
.ufo/waves/round-44/fixtures/mutants/count-c1.py: OK
.ufo/waves/round-44/fixtures/mutants/count-c2.py: OK
.ufo/waves/round-44/fixtures/mutants/count-c3.py: OK
SKILL.md: OK
sha256sum: WARNING: 4 line(s) are improperly formatted
```

All ten pins verify; the four "improperly formatted" lines are the evidence file's own comment
and tally lines, not checksums.

---

## 2. Every instrument's `--selftest`, run from the clone

Working directory is the clone root throughout this section.

```
$ cd /tmp/mori44-offhost.dZeeKl/clone
$ python3 .ufo/waves/round-44/count-c1.py --selftest
selftest PASS honest_ledger_met
selftest PASS offbyone_row_mismatch
selftest PASS junk_producer_rejected
selftest PASS below_floor_rejected
selftest PASS absent_ledger_unmet
selftest PASS compound_command_rejected
C1_SELFTEST pass=6 fail=0
EXIT=0
```

```
$ python3 .ufo/waves/round-44/count-c2.py --selftest
selftest PASS registered_conformant_met
selftest PASS absent_counter_unmet
selftest PASS unregistered_counter_unmet
selftest PASS no_selftest_mode_unmet
selftest PASS surviving_mutant_unmet
C2_SELFTEST pass=5 fail=0
EXIT=0
```

```
$ python3 .ufo/waves/round-44/count-c3.py --selftest
selftest PASS registered_entry_met
selftest PASS absent_entry_unmet
selftest PASS row_without_used_by_unmet
selftest PASS red_census_unmet
selftest PASS readme_without_row_unmet
selftest PASS missing_coverage_map_unmet
C3_SELFTEST pass=6 fail=0
EXIT=0
```

```
$ python3 tools/mori-gate-registry.py --selftest
selftest PASS registered_row_met
selftest PASS missing_cell_rejected
selftest PASS unresolved_entry_rejected
selftest PASS unregistered_path_rejected
selftest PASS no_selftest_rejected
selftest PASS seven_cell_row_rejected
GATE_REGISTRY_SELFTEST pass=6 fail=0
EXIT=0
```

| instrument | command (from clone root) | exit | tally |
|---|---|---|---|
| `count-c1.py` | `python3 .ufo/waves/round-44/count-c1.py --selftest` | 0 | `C1_SELFTEST pass=6 fail=0` |
| `count-c2.py` | `python3 .ufo/waves/round-44/count-c2.py --selftest` | 0 | `C2_SELFTEST pass=5 fail=0` |
| `count-c3.py` | `python3 .ufo/waves/round-44/count-c3.py --selftest` | 0 | `C3_SELFTEST pass=6 fail=0` |
| `mori-gate-registry.py` | `python3 tools/mori-gate-registry.py --selftest` | 0 | `GATE_REGISTRY_SELFTEST pass=6 fail=0` |

These four tallies equal the freeze record's own `# selftest tallies at freeze` block
(`pass=6 fail=0`, `pass=5 fail=0`, `pass=6 fail=0`, `pass=6 fail=0`) — reproduced off-host, not
copied. Each selftest builds throwaway git repositories under the caller's `TMPDIR` and removes
them; nothing in the clone was written (`git status --porcelain` stayed empty).

---

## 3. `count-c2.py <freeze-rev> --repo <clone>` against the clone

```
$ cd /tmp/mori44-offhost.dZeeKl/clone
$ python3 .ufo/waves/round-44/count-c2.py 7cb59c6891d4f5d0266fe062565f094da835dc84 \
      --repo /tmp/mori44-offhost.dZeeKl/clone \
      --counter .ufo/waves/round-44/count-c1.py \
      --counter .ufo/waves/round-44/count-c2.py \
      --counter .ufo/waves/round-44/count-c3.py
check counters_present   PASS (3 counters)
check registry_rows      PASS (REGISTRY=met)
check tool_selftest      PASS (pass=6 fail=0)
check selftest_tally     PASS (count-c1.py pass=6; count-c2.py pass=5; count-c3.py pass=6)
check mutant_kill        FAIL (count-c1.py mutant absent; count-c2.py mutant absent; count-c3.py mutant absent)
rev=7cb59c6891d4f5d0266fe062565f094da835dc84
C2=unmet
EXIT=1
```

`mutant_kill` fails because the **default** `--mutants-dir` is `fixtures/mutants`
(`count-c2.py:355`), resolved repo-relative at the revision (`count-c2.py:168`), i.e.
`<repo>/fixtures/mutants` — a directory that does not exist at the freeze commit (see F3). With
the mutants named explicitly, the same invocation reaches `C2=met`:

```
$ python3 .ufo/waves/round-44/count-c2.py 7cb59c6891d4f5d0266fe062565f094da835dc84 \
      --repo /tmp/mori44-offhost.dZeeKl/clone \
      --mutants-dir .ufo/waves/round-44/fixtures/mutants \
      --counter .ufo/waves/round-44/count-c1.py \
      --counter .ufo/waves/round-44/count-c2.py \
      --counter .ufo/waves/round-44/count-c3.py
check counters_present   PASS (3 counters)
check registry_rows      PASS (REGISTRY=met)
check tool_selftest      PASS (pass=6 fail=0)
check selftest_tally     PASS (count-c1.py pass=6; count-c2.py pass=5; count-c3.py pass=6)
check mutant_kill        PASS (count-c1.py killed (fail=1); count-c2.py killed (fail=1); count-c3.py killed (fail=1))
rev=7cb59c6891d4f5d0266fe062565f094da835dc84
C2=met
EXIT=0
```

The mutants are real single-check disables, and each is caught by the selftest arm that covers the
disabled check (run from the clone, `cwd=/tmp`):

```
$ for c in c1 c2 c3; do python3 "$R/.ufo/waves/round-44/fixtures/mutants/count-$c.py" --selftest; done
selftest FAIL below_floor_rejected: []      # mutant disables row_floor
C1_SELFTEST pass=5 fail=1
selftest FAIL surviving_mutant_unmet: []    # mutant disables mutant_kill
C2_SELFTEST pass=4 fail=1
selftest FAIL red_census_unmet: []          # mutant disables census_ok
C3_SELFTEST pass=5 fail=1
```

```
$ for c in c1 c2 c3; do diff -u .ufo/waves/round-44/count-$c.py \
      .ufo/waves/round-44/fixtures/mutants/count-$c.py; done
-    record("row_floor", len(rows) >= min_rows,      # c1 -> disabled
+    record("row_floor", True,
-        record("mutant_kill", all("killed" in m ...   # c2 -> disabled
+        record("mutant_kill", True, ...
-            record("census_ok", ok, "exit=%s" ...     # c3 -> disabled
+            record("census_ok", True, "exit=%s" ...
```

The contract's `After` line, taken literally, is not runnable — `count-c2.py` requires
`--counter`:

```
$ python3 .ufo/waves/round-44/count-c2.py 7cb59c6891d4f5d0266fe062565f094da835dc84 \
      --repo /tmp/mori44-offhost.dZeeKl/clone
usage: count-c2.py <rev|WORK> --counter PATH [--counter PATH ...] [--selftest]
EXIT=2
```

---

## 4. The other two counters in real mode, at the freeze revision, against the clone

Before-state controls, so the replay shows able-to-fail behaviour and not only green arms:

```
$ python3 .ufo/waves/round-44/count-c1.py 7cb59c6891d4f5d0266fe062565f094da835dc84 \
      --repo /tmp/mori44-offhost.dZeeKl/clone
check ledger_present       FAIL (absent)
rev=7cb59c6891d4f5d0266fe062565f094da835dc84
ledger=.ufo/waves/round-44/figures.tsv rows=0 classes=-
C1=unmet mismatches=?
EXIT=1
```

```
$ python3 .ufo/waves/round-44/count-c3.py 7cb59c6891d4f5d0266fe062565f094da835dc84 \
      --repo /tmp/mori44-offhost.dZeeKl/clone \
      --entry corpus/knowledge/pid-probe-conclusion-r44.md --row S471 --row S472
check entry_present    FAIL (absent)
rev=7cb59c6891d4f5d0266fe062565f094da835dc84
C3=unmet
EXIT=1
```

And the C1 witness ledger, read out of the clone's own object store:

```
$ python3 .ufo/waves/round-44/count-c1.py 7cb59c6891d4f5d0266fe062565f094da835dc84 \
      --repo /tmp/mori44-offhost.dZeeKl/clone \
      --ledger .ufo/waves/round-44/fixtures/figures-r43.tsv
check ledger_present       PASS (1518 bytes)
check rows_parse           PASS (12 rows)
check row_floor            PASS (rows=12 min=12)
check class_floor          PASS (classes=checks,corpus,evidence,registry,wave min=4)
check commands_reconcile   FAIL (F03 asserted=15 observed=14; F04 asserted=34 observed=8)
rev=7cb59c6891d4f5d0266fe062565f094da835dc84
ledger=.ufo/waves/round-44/fixtures/figures-r43.tsv rows=12 classes=checks,corpus,evidence,registry,wave
C1=unmet mismatches=2
EXIT=1
```

The witness's two mismatches reproduce off-host byte-for-byte, which means the twelve `git`
pipelines inside the fixture executed against the **clone's** history (the clone carries the full
lane history, so `@REV@` substitution resolves there).

---

## 5. Path independence — the clone moved, then re-run

The clone was moved, not copied, so every path below the old root disappeared:

```
$ S=/tmp/mori44-offhost.dZeeKl
$ mkdir -p "$S/relocated/nested" && mv "$S/clone" "$S/relocated/nested/replay"
$ git -C "$S/relocated/nested/replay" rev-parse HEAD
7cb59c6891d4f5d0266fe062565f094da835dc84
$ git -C "$S/relocated/nested/replay" status --porcelain | wc -l
0
```

Re-runs, all with `cwd=/` (so not even the working directory is the clone):

```
$ cd / && python3 "/tmp/mori44-offhost.dZeeKl/relocated/nested/replay/.ufo/waves/round-44/count-c1.py" --selftest
selftest PASS honest_ledger_met
… (six PASS lines)
C1_SELFTEST pass=6 fail=0
EXIT=0
```

```
$ cd / && python3 "$R/.ufo/waves/round-44/count-c2.py" 7cb59c6891d4f5d0266fe062565f094da835dc84 \
      --repo "$R" --mutants-dir .ufo/waves/round-44/fixtures/mutants \
      --counter .ufo/waves/round-44/count-c1.py --counter .ufo/waves/round-44/count-c2.py \
      --counter .ufo/waves/round-44/count-c3.py          # R=$S/relocated/nested/replay
check counters_present   PASS (3 counters)
check registry_rows      PASS (REGISTRY=met)
check tool_selftest      PASS (pass=6 fail=0)
check selftest_tally     PASS (count-c1.py pass=6; count-c2.py pass=5; count-c3.py pass=6)
check mutant_kill        PASS (count-c1.py killed (fail=1); count-c2.py killed (fail=1); count-c3.py killed (fail=1))
rev=7cb59c6891d4f5d0266fe062565f094da835dc84
C2=met
EXIT=0
```

```
$ cd / && python3 "$R/.ufo/waves/round-44/count-c3.py" --selftest
C3_SELFTEST pass=6 fail=0            # EXIT=0, six PASS lines
$ cd / && python3 "$R/tools/mori-gate-registry.py" --selftest
GATE_REGISTRY_SELFTEST pass=6 fail=0 # EXIT=0, six PASS lines
$ cd / && python3 "$R/.ufo/waves/round-44/count-c1.py" 7cb59c68… --repo "$R" \
      --ledger .ufo/waves/round-44/fixtures/figures-r43.tsv
C1=unmet mismatches=2                # EXIT=1, identical to §4
```

Identical verdicts and tallies before and after the move, from a foreign `cwd`: no path is baked
into the green arms.

### 5.1 `TMPDIR` is not baked in either

```
$ mkdir -p "$S/tmpdir-alt"
$ cd / && TMPDIR="$S/tmpdir-alt" python3 "$R/.ufo/waves/round-44/count-c2.py" --selftest
C2_SELFTEST pass=5 fail=0            # EXIT=0
$ ls -A "$S/tmpdir-alt"
                                     # empty: the selftest removed its fixtures
```

### 5.2 The counter's `git` pipeline runs on the clone's objects, not the lane's

A decisive probe: a commit that exists **only** in the clone. I added the witness ledger as
`.ufo/waves/round-44/figures.tsv` and committed it in the clone (`bca38ef9…`); the lane has never
seen that object.

```
$ git -C "$R" rev-parse HEAD
bca38ef9427ff3cf6040583d63cc524146c74b78
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -t bca38ef9427ff3cf6040583d63cc524146c74b78
fatal: git cat-file: could not get object info
$ python3 "$R/.ufo/waves/round-44/count-c1.py" bca38ef9427ff3cf6040583d63cc524146c74b78 --repo "$R"
check ledger_present       PASS (1518 bytes)
check rows_parse           PASS (12 rows)
check row_floor            PASS (rows=12 min=12)
check class_floor          PASS (classes=checks,corpus,evidence,registry,wave min=4)
check commands_reconcile   FAIL (F03 asserted=15 observed=14; F04 asserted=34 observed=8)
rev=bca38ef9427ff3cf6040583d63cc524146c74b78
ledger=.ufo/waves/round-44/figures.tsv rows=12 classes=checks,corpus,evidence,registry,wave
C1=unmet mismatches=2
EXIT=1
```

The revision is unresolvable in the lane and resolves in the clone; the counter read the 1518-byte
ledger from it. `--repo` is honoured end to end, not merely accepted as an argument.

### 5.3 The landed tip `30fe06d1`, all three counters, from a second `/tmp` clone

The integrator landed the round's artifacts while this seat ran, so the same off-host replay was
repeated at that tip, from a second clone (`/tmp/mori44-offhost.dZeeKl/tipclone`, `git status`
clean before and after). All three claims, measured with `cwd=/`:

```
$ T=/tmp/mori44-offhost.dZeeKl/tipclone
$ python3 "$T/.ufo/waves/round-44/count-c1.py" 30fe06d1… --repo "$T"
check ledger_present       PASS (1321 bytes)
check rows_parse           PASS (16 rows)
check row_floor            PASS (rows=16 min=12)
check class_floor          PASS (classes=checks,corpus,evidence,registry,wave min=4)
check commands_reconcile   PASS (all rows match)
rev=30fe06d1e2593e18280d83e7e3086f4d678762df
ledger=.ufo/waves/round-44/figures.tsv rows=16 classes=checks,corpus,evidence,registry,wave
C1=met mismatches=0
EXIT=0

$ python3 "$T/.ufo/waves/round-44/count-c2.py" 30fe06d1… --repo "$T" \
      --mutants-dir .ufo/waves/round-44/fixtures/mutants \
      --counter .ufo/waves/round-44/count-c1.py --counter .ufo/waves/round-44/count-c2.py \
      --counter .ufo/waves/round-44/count-c3.py
check counters_present   PASS (3 counters)
check registry_rows      PASS (REGISTRY=met)
check tool_selftest      PASS (pass=6 fail=0)
check selftest_tally     PASS (count-c1.py pass=6; count-c2.py pass=5; count-c3.py pass=6)
check mutant_kill        PASS (count-c1.py killed (fail=1); count-c2.py killed (fail=1); count-c3.py killed (fail=1))
rev=30fe06d1e2593e18280d83e7e3086f4d678762df
C2=met
EXIT=0

$ python3 "$T/.ufo/waves/round-44/count-c2.py" 30fe06d1… --repo "$T" \
      --counter .ufo/waves/round-44/count-c1.py --counter .ufo/waves/round-44/count-c2.py \
      --counter .ufo/waves/round-44/count-c3.py          # default --mutants-dir
check mutant_kill        FAIL (count-c1.py mutant absent; count-c2.py mutant absent; count-c3.py mutant absent)
C2=unmet
EXIT=1
```

C1 is a genuine green arm off-host — not a selftest — and C2 reaches `C2=met` off-host only with
the mutants named (F3). C3 at the same tip is §F2's landed-tip block: `C3=unmet` under the
declared invocation, `C3=met` only with `--census` plus `TMPDIR=<repo>`.

### 5.4 Write scope

`git status --porcelain` in the clone stayed empty across all four selftests, both `count-c2.py`
real runs, the C1 witness and the C3 real run (the only change is the deliberate probe commit of
§5.2). The declared scope "stdout only; counter bytes materialize under the caller TMPDIR"
holds: `count-c2.py` materializes counter copies into `tempfile.mkdtemp(prefix="c2-")` and removes
them, and the alternate `TMPDIR` was empty afterwards. The tip clone of §5.3 was also clean before
and after its three runs, including the one with `TMPDIR=<clone>`.

---

## 6. Absolute-path dependencies found

```
$ grep -nE "/home|mori-shokunin|shokunin|/tmp/|/root/|/usr/local" \
      .ufo/waves/round-44/count-c1.py .ufo/waves/round-44/count-c2.py \
      .ufo/waves/round-44/count-c3.py tools/mori-gate-registry.py
.ufo/waves/round-44/count-c1.py:173:    git(repo, ["config", "user.email", "mori@shokunin.local"])
.ufo/waves/round-44/count-c1.py:174:    git(repo, ["config", "user.name", "mori-shokunin"])
.ufo/waves/round-44/count-c2.py:233:    git(repo, ["config", "user.email", "mori@shokunin.local"])
.ufo/waves/round-44/count-c2.py:234:    git(repo, ["config", "user.name", "mori-shokunin"])
.ufo/waves/round-44/count-c3.py:180:    git(repo, ["config", "user.email", "mori@shokunin.local"])
.ufo/waves/round-44/count-c3.py:181:    git(repo, ["config", "user.name", "mori-shokunin"])
tools/mori-gate-registry.py:172:    git(repo, ["config", "user.email", "mori@shokunin.local"])
tools/mori-gate-registry.py:173:    git(repo, ["config", "user.name", "mori-shokunin"])
```

No `/home/` string exists in any of the four frozen instruments (`grep -rn "/home/" …` exits 1);
the only `shokunin` hits are git identity strings set inside throwaway fixture repos. Their repo
roots come from `os.path.abspath(__file__)` walked upward (`repo_default()` in each file;
`tools/mori-gate-registry.py:32-34` is `dirname(dirname(__file__))`). Those four instruments are
path-clean.

What is **not** path-clean is the surface they call, and two defaults:

### F1 — C3's default census path leaves the repository

```
$ grep -n "census = args.census" .ufo/waves/round-44/count-c3.py
299:    census = args.census or os.path.join(os.path.dirname(repo), "scripts", "sources-census.sh")
```

`<repo>/../scripts/sources-census.sh` is the *sibling* of the lane. On-host that is
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (exists, 35466 bytes); the lane's own git
tree has no `scripts/` directory at all (`git ls-tree -r 7cb59c68 --name-only -- scripts` → empty).
Off-host the default resolves to a nonexistent file and `bash` returns 127, which the counter
records as `census_ok FAIL`:

```
$ python3 - "$R" <<'PY'
repo=os.path.abspath(sys.argv[1]); print(os.path.join(os.path.dirname(repo),"scripts","sources-census.sh"))
PY
/tmp/mori44-offhost.dZeeKl/relocated/nested/scripts/sources-census.sh
exists: False
$ bash /tmp/mori44-offhost.dZeeKl/relocated/nested/scripts/sources-census.sh validate --file /tmp/…
bash: …/scripts/sources-census.sh: No such file or directory
EXIT=127
```

So C3's green arm needs `--census` supplied off-host. That alone would be a portability defect,
not a verdict defect — the next finding is the verdict defect.

### F2 — C3's census arm is green only when `TMPDIR` is the repository root, and nothing declares that

`count-c3.py` stages the registry into a flat temp directory before handing it to the census:

```
$ grep -n "staged = os.path.join" .ufo/waves/round-44/count-c3.py
135:            staged = os.path.join(tmp, "SOURCES.md")     # tmp = tempfile.mkdtemp(prefix="c3-")
$ grep -n "usedby_findings \"\$f\"" /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
721:    usedby_out=$(usedby_findings "$f" "$dir" "$lane")
```

The census's E11 rule (`scripts/sources-census.sh:538-568`) tests `[ ! -e "$dir/$path" ]` for every
`mined` row's `used-by` path, where `$dir` is the grandparent of the file it was given. A file at
`/tmp/c3-XXXX/SOURCES.md` therefore gets `$dir=/tmp`, and every `corpus/knowledge/…` used-by is
reported missing. Isolated proof — identical bytes, two locations:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$L/corpus/SOURCES.md"
file	ok	/tmp/mori44-offhost.dZeeKl/e11/lane/corpus/SOURCES.md
EXIT=0
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$S/e11/stage/SOURCES.md"
file	E11	S900 missing used-by corpus/knowledge/x.md
EXIT=1
```

(`$L/corpus/knowledge/x.md` exists; `$S/e11/stage/` is the same file copied flat, exactly the
shape `count-c3.py` produces.)

Driven through the counter itself against the real, committed 243-row registry. The `--entry`
argument is a committed file used only as a driver, so that the census arm is reached (its
`entry_meta`/`rows_present` FAILs are the driver's, not an entry's):

```
$ python3 .ufo/waves/round-44/count-c3.py 7cb59c68… --repo "$R" --entry corpus/SOURCES.md --row S471
check entry_present    PASS (240934 bytes)
check entry_meta       FAIL (verified-at:; recheck:; coverage-map:; source: lacks S471)   # driver
check rows_present     FAIL (S471 absent)                                                # driver
check census_ok        FAIL (exit=127)      # default census path absent off-host  (F1)
check readme_row       PASS (names entry)
C3=unmet
EXIT=1

$ … --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
check census_ok        FAIL (exit=1)        # real census, real registry: E11 flood
C3=unmet
EXIT=1

$ cp /home/vgpnk/Projects/shokunin/scripts/sources-census.sh "$S/relocated/nested/scripts/"
$ … (default path now resolves inside the sandbox)
check census_ok        FAIL (exit=1)        # same E11 failure with a sandbox-local census
C3=unmet
EXIT=1

$ TMPDIR="$R" … (default path still resolves inside the sandbox; TMPDIR moved to the repo root)
check census_ok        PASS (exit=0)        # E11 resolves: $dir is now the repo root
C3=unmet
EXIT=1

$ mv "$S/relocated/nested/scripts" "$S/scripts-offpath"   # census absent again
$ TMPDIR="$R" …
check census_ok        FAIL (exit=127)      # TMPDIR alone is not enough
C3=unmet
EXIT=1
```

And on-host, against the lane itself (read-only, same driver entry, default `TMPDIR`, default
census path):

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-44/count-c3.py \
      7cb59c6891d4f5d0266fe062565f094da835dc84 \
      --repo /home/vgpnk/Projects/shokunin/mori-shokunin --entry corpus/SOURCES.md --row S471
check entry_present    PASS (240934 bytes)
check entry_meta       FAIL (verified-at:; recheck:; coverage-map:; source: lacks S471)   # driver
check rows_present     FAIL (S471 absent)                                                # driver
check census_ok        FAIL (exit=1)        # E11: used-by paths do not resolve from /tmp
check readme_row       PASS (names entry)
C3=unmet
EXIT=1
```

Measured matrix for `census_ok` (all with the same committed registry):

| census resolvable | `TMPDIR` | `census_ok` |
|---|---|---|
| no (off-host default) | default `/tmp` | FAIL, exit 127 |
| yes (host fleet script) | default `/tmp` | FAIL, exit 1 (E11) |
| yes (sandbox copy) | default `/tmp` | FAIL, exit 1 (E11) |
| yes (sandbox copy) | `<repo>` | **PASS, exit 0** |
| no | `<repo>` | FAIL, exit 127 |

### F2 at the landed tip — measured, not predicted

While this seat ran, the integrator landed `30fe06d1` with the C3 entry
(`corpus/knowledge/pid-probe-conclusion-r44.md`, 7151 bytes) and both rows (245 rows in
`corpus/SOURCES.md`). A second `/tmp` clone of that tip gives the contract's `After` invocation
verbatim:

```
$ T=/tmp/mori44-offhost.dZeeKl/tipclone    # clone at 30fe06d1, status clean
$ cd / && python3 "$T/.ufo/waves/round-44/count-c3.py" 30fe06d1… --repo "$T" \
      --entry corpus/knowledge/pid-probe-conclusion-r44.md --row S471 --row S472
check entry_present    PASS (7151 bytes)
check entry_meta       PASS (sources S471,S472)
check rows_present     PASS (rows S471,S472 mined)
check census_ok        FAIL (exit=127)
check readme_row       PASS (names entry)
rev=30fe06d1e2593e18280d83e7e3086f4d678762df
C3=unmet
EXIT=1

$ … --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
check census_ok        FAIL (exit=1)        # E11 on the flat staging
C3=unmet
EXIT=1

$ TMPDIR="$T" … --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
check census_ok        PASS (exit=0)
C3=met
EXIT=0
```

Everything the C3 predicate asks for is present at the tip — the four other checks PASS — and the
verdict still flips on `TMPDIR`. `C3=met` is reachable off-host, but only with `--census` naming
the real tool **and** `TMPDIR` set to the repository root; the declared After invocation prints
`C3=unmet`. The tip clone stayed clean across all three runs (`git status --porcelain` empty), so
the `TMPDIR=<repo>` run wrote nothing into it.

The census's own output for the staged registry is the E11 list (one line per used-by path, e.g.
`file E11 S001 missing used-by corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md`),
exit 1.

Consequence: `census_ok` reaches 0 only when the caller sets `TMPDIR` to the repository root, so
that the staged file's grandparent *is* the lane root and `used-by` paths resolve. Neither the
contract, the `SKILL.md` row ("the registry copy handed to the census is materialized under the
caller TMPDIR" — true, but silent on which TMPDIR), nor any round-44 evidence names that
requirement. The green census arm that makes `C3_SELFTEST` pass is a stub, not the real tool:

```
$ grep -n "CENSUS_OK\|fake-census" .ufo/waves/round-44/count-c3.py
172:CENSUS_OK = "#!/bin/sh\n# fixture census\nexit 0\n"
204:        "fixtures/fake-census.sh": CENSUS_OK,
227:                            "FR5", "fixtures/fake-census.sh", "corpus/README.md", 60)
```

So the selftest proves the counter reacts to a census exit code, but no arm ever runs the real
census, and under the default `TMPDIR` the counter's own `census_ok` cannot reach 0 against it.
A zero-exit `--census` stub would turn the check green with no census evidence at all — the
counter cannot tell the stub from the tool. Both are post-freeze defects to record as a lesson and
route to round 45 (contract §Freeze: "a defect found post-freeze is recorded as a lesson and
routed to round 45, never patched in place"), and the round's C3 verdict must state which
`--census` and which `TMPDIR` produced it.

### F3 — C2's default `--mutants-dir` points at a directory that does not exist

```
$ grep -n "mutants-dir" .ufo/waves/round-44/count-c2.py
17:                      [--mutants-dir fixtures/mutants] [--min-arms N] [--timeout S]
355:    ap.add_argument("--mutants-dir", default="fixtures/mutants")
$ grep -n "mpath = " .ufo/waves/round-44/count-c2.py
168:            mpath = "%s/%s" % (mutants_dir.rstrip("/"), os.path.basename(c))
$ git ls-tree 7cb59c68 --name-only | grep -x fixtures || echo "NO repo-root fixtures/ at freeze"
NO repo-root fixtures/ at freeze
$ git ls-tree -r --name-only 7cb59c68 -- .ufo/waves/round-44 | grep mutants
.ufo/waves/round-44/fixtures/mutants/count-c1.py
.ufo/waves/round-44/fixtures/mutants/count-c2.py
.ufo/waves/round-44/fixtures/mutants/count-c3.py
```

`mpath` is read with `read_at(repo, rev, …)`, so the default is repo-relative: `<repo>/fixtures/mutants`,
which exists at no revision. The round's mutants live one level deeper, beside the counters. The
`SKILL.md` row's pinned-values cell says "`fixtures/mutants/<basename>` beside each counter",
which is what the code should resolve but does not. Effect: the documented invocation
(`count-c2.py <rev> --counter …`, exactly the row's entry cell) prints `C2=unmet`; adding
`--mutants-dir .ufo/waves/round-44/fixtures/mutants` prints `C2=met` (§3). Recoverable by an
explicit flag, but the default is dead and the row does not say the path is repo-relative.

### F4 — the contract's C2 `After` line is not a runnable command

`count-c2.py <landed tip>` exits 2 with the usage line (§3): `--counter` is required and the
contract omits it. The C2 claim is still evaluable with the flags, but the After line as frozen
cannot produce `C2=met`.

### F5 — the round-43 counters still hardcode the lane path (QUALITY 115's cited pointer)

```
$ git grep -n "/home/" 7cb59c68 -- '.ufo/waves/round-43/*.py'
.ufo/waves/round-43/count-c1s.py:21:LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
.ufo/waves/round-43/count-c2.py:13:LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
```

`count-c1s.py` accepts `--repo LANE` and rebinds the global (`:88-89`), so the hardcoded value is
a default, not a wall — see §7 for the off-host replay of that green control. Round-44's own four
instruments carry no such constant.

Full sweep for the record: of the 29 `tools/*.py` files at the freeze commit, three embed
`/home/` — `tools/mori-misroot-sweep.py`, `tools/mori-round17-context-check.py`,
`tools/mori-round17-jj-regressions.py` — none of them is a round-44 instrument, and
`tools/mori-gate-registry.py` is clean:

```
$ git grep -l "/home/" 7cb59c68 -- 'tools/*.py'
7cb59c68:tools/mori-misroot-sweep.py
7cb59c68:tools/mori-round17-context-check.py
7cb59c68:tools/mori-round17-jj-regressions.py
```

### F6 — the round's census evidence is fleet-root-scoped by construction

`evidence/census-start.txt` records
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
(exit 0, rows=243). That invocation validates the *fleet*, not a revision of the lane; C3's
`census_ok` instead calls `validate --file <staged>` with no `--root`. The two shapes are not
interchangeable (F2), so the census evidence does not certify the check C3 runs.

### F7 — the round-43 control hardcodes its sandbox under `/tmp`, ignoring `TMPDIR`

```
$ grep -n 'dir="/tmp"' .ufo/waves/round-43/count-c1s.py
119:    sandbox = tempfile.mkdtemp(prefix="mori-r43-c1s-", dir="/tmp")
```

Measured consequence during this replay: `/tmp` on this host is a separate 128 GB partition that
reached 100% while `/` still had 562 GB free —

```
$ findmnt -no SOURCE,SIZE,USED,AVAIL,TARGET /tmp
/dev/nvme0n1p1 127.9G 127.9G  304K /tmp
$ df -h / | tail -1
/dev/mapper/root  930G  311G  562G  36% /
```

— and `count-c1s.py` then fails at `sandbox_clone`:

```
$ git clone -q --shared <clone> "$T/repo"      # $T from mktemp -d /tmp/… — the mktemp failed
mktemp: No space left on device (os error 28)
fatal: could not create work tree dir '/repo': Permission denied   # empty $T, hence /repo
rc=128
$ python3 .ufo/waves/round-43/count-c1s.py 7cb59c68… --repo <clone>
check sandbox_clone          FAIL (Note: switching to '7cb59c68…'.

You are in 'deta)
C1S=unmet
EXIT=1
```

A control that cannot replay when the caller's `TMPDIR` has room but `/tmp` does not is weaker
evidence than one that honours `TMPDIR`. Round-44's four instruments do honour it —
`tempfile.mkdtemp(prefix=…)` with no `dir=` — as §5.1 verifies.

### Non-finding: `MORI_GATE_REGISTRY`

`count-c2.py:251` reads `MORI_GATE_REGISTRY` only inside `auditor_bytes()`, which seeds the
selftest fixture; the real evaluation path materializes the auditor from `repo`/`rev`. The
variable was unset in every run above (`[${MORI_GATE_REGISTRY-<unset>}]` → `<unset>`).

---

## 7. QUALITY 115's own check, replayed off-host

QUALITY 115 names the round-43 green control: `count-c1s.py <scratch-rev> --repo <scratch-clone>`
must print `C1S=met`, and the same counter must be able to print `C1S=unmet`. Both arms, run with
`cwd=/` against the moved clone:

```
$ R=/tmp/mori44-offhost.dZeeKl/relocated/nested/replay
$ cd / && python3 "$R/.ufo/waves/round-43/count-c1s.py" 7cb59c6891d4f5d0266fe062565f094da835dc84 --repo "$R"
check self_at_rev            PASS (match)
check frozen_sha             PASS (105ce075f331)
check frozen_sig             PASS (run params argv, timeout)
check v5_present             PASS (.ufo/waves/round-42/conform.py)
check sandbox_clone          PASS (Note: switching to 'bca38ef9427ff3cf6040583d63cc524146c74b78'.

You are in 'deta)
check noharm_cwd             PASS (rc=0 MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0)
check v5_selftest_17         PASS (pass=17 fail=0 rc=0)
check mutant_present_walrus-branch PASS (.ufo/waves/round-42/fixtures/mutants/conform-mut-walrus-branch.py)
check mutant_kill_walrus-branch PASS (pass=16 fail=1 fails=['timeout_scope_walrus_positive'])
check mutant_present_tuple-extract PASS (.ufo/waves/round-42/fixtures/mutants/conform-mut-tuple-extract.py)
check mutant_kill_tuple-extract PASS (pass=16 fail=1 fails=['timeout_scope_tupleunpack_positive'])
check mutant_present_sort-deletion PASS (.ufo/waves/round-42/fixtures/mutants/conform-mut-sort-deletion.py)
check mutant_kill_sort-deletion PASS (pass=16 fail=1 fails=['timeout_scope_source_order'])
check frozen_still_crashes   PASS (rc=1 crash=True C1_line=False)
C1S=met
EXIT=0
```

Fourteen checks PASS, `C1S=met`, exit 0. Able to fail, at the revision before the successor
existed (`e3a2b58f`, the round-42 verifier spot-check):

```
$ cd / && python3 "$R/.ufo/waves/round-43/count-c1s.py" e3a2b58f --repo "$R"
check self_at_rev            FAIL (absent)
C1S=unmet
EXIT=1
```

Two details of this replay, measured rather than assumed:

- `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"` is the module default (F5), and `--repo`
  rebinds it (`count-c1s.py:88-89`); every `git` call in the run above targeted the clone. The
  control's own `sandbox_clone` step clones `--shared` from the repo it was given and then checks
  out `rev` detached, so the replay is at the requested revision even though the clone's `HEAD`
  was the §5.2 probe commit.
- The same command **without** free space under `/tmp` reported `frozen_still_crashes FAIL (rc=1
  crash=False C1_line=True)` — not because the frozen bytes changed, but because the frozen r42
  counter it drives hardcodes its own sandbox under `/tmp`
  (`.ufo/waves/round-42/count-c1.py:167`: `tempfile.mkdtemp(prefix="mori-r42-c1-", dir="/tmp")`)
  and its `--shared` clone failed, so it took its early `print("C1=unmet"); return 1` path. That is
  the F7 dependency showing up as a false FAIL, and it is why the same invocation printed
  `C1S=met` once `/tmp` had room.

---

## 8. Result, risks, blockers

- **Result (off-host replay, freeze commit).** All four frozen instruments' `--selftest` run from
  a `/tmp` clone at the freeze commit and print the freeze record's own tallies (6/0, 5/0, 6/0,
  6/0), exit 0. `count-c2.py <freeze-rev> --repo <clone>` reaches `C2=met` (exit 0) when the
  mutants are named, and `C2=unmet` (exit 1, `mutant_kill`) with the dead default. The C1 witness
  reproduces `C1=unmet mismatches=2` off-host. The clone's move to a new path plus a foreign `cwd`
  changes no verdict, a clone-only commit is resolved and read by `count-c1.py`, and an alternate
  `TMPDIR` changes nothing.
- **Result (off-host replay, landed tip `30fe06d1`).** From a second `/tmp` clone:
  `C1=met mismatches=0` (exit 0, 16 rows, 5 classes) — a real green arm, not a selftest;
  `C2=met` (exit 0) with `--mutants-dir`, `C2=unmet` without it; `C3=unmet` (exit 1,
  `census_ok exit=127`) under the contract's declared invocation, `C3=met` (exit 0) only with
  `--census <real script>` **and** `TMPDIR=<repo root>`. **QUALITY 115 holds for round 44's
  instruments: no green arm is tied to the lane path.** What the C3 arm is tied to is a temp-dir
  location, which F2 documents.
- **Defect F2 (decides how the C3 verdict must be read).** `count-c3.py`'s `census_ok` reaches 0
  only when `TMPDIR` is the repository root: the staged registry sits flat in a temp dir, so the
  census's E11 rule reports every `used-by` path missing and exits 1. Measured five ways at the
  freeze revision (absent census → 127; host census → 1; sandbox-local census → 1; sandbox-local
  census with `TMPDIR=<repo>` → 0; absent census with `TMPDIR=<repo>` → 127), isolated with
  identical bytes (lane tree → 0, flat → 1), confirmed on-host against the lane (default
  `TMPDIR` → exit 1), and measured at the landed tip (declared invocation → `C3=unmet`,
  `--census` + `TMPDIR=<clone>` → `C3=met`). The instruments are frozen; this belongs in the
  round's lesson and round-45 routing, and any `C3=met` verdict must state the `--census` and
  `TMPDIR` it used.
- **Defect F3 (C2 default).** `--mutants-dir` defaults to `<repo>/fixtures/mutants`, which exists
  at no revision; `C2=met` requires the explicit
  `--mutants-dir .ufo/waves/round-44/fixtures/mutants`. The `SKILL.md` row's "beside each counter"
  wording and the code's repo-root default disagree.
- **Defect F1 (portability).** C3's default census path is outside the repository
  (`<repo>/../scripts/…`); a lone clone cannot run the check without `--census`.
- **Result (QUALITY 115's named check).** The round-43 green control replays off-host:
  `count-c1s.py 7cb59c68 --repo <clone>` prints fourteen PASS lines and `C1S=met`, exit 0, and the
  same counter at `e3a2b58f` prints `self_at_rev FAIL (absent)` → `C1S=unmet`, exit 1. The
  control's `LANE` constant is a home path (F5) but `--repo` rebinds it; nothing in the run
  touched the lane.
- **Risks.** (a) A C3 seat that "fixes" F2 by passing a zero-exit `--census` stub would make the
  verdict green with no census evidence — the counter cannot tell a stub from the real tool, and
  the selftest already demonstrates exactly that shape (`fixtures/fake-census.sh`). (b) F3 is
  invisible to anyone who runs the bare row form and reads only `C2=unmet`, inviting a false
  "mutants missing" conclusion about the fixtures rather than about the default. (c) `/tmp` on
  this host is a separate 128 GB partition that reached 100% during the wave; both `count-c1s.py`
  and the frozen r42 counter it drives hardcode `dir="/tmp"` for their sandboxes (F7), so an
  ENOSPC there surfaces as a content verdict (`frozen_still_crashes FAIL`, `C1S=unmet`) rather
  than as a setup error. Here the first `count-c1s.py` run was killed by my own 900 s deadline
  while `/tmp` was already filling, the second reported the false FAIL, and only the third run,
  with room, printed `C1S=met`. Round-44's instruments honour `TMPDIR`, so they are not exposed
  the same way.
- **Blockers.** None for this report. No tool was installed or upgraded (no pacman/uv/npx/cargo);
  pacman is paused host-wide and was not used. Lane writes: this file only. Lane VCS: read-only
  commands (`rev-parse`, `log`, `ls-tree`, `cat-file`, `grep`, `show`, `status`) only.

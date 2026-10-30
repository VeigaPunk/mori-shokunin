# Mo61ScribeReg5657 — round-61 registry rows, round-56 and round-57 gates (draft only)

Lane `mori-shokunin` (`/home/vgpnk/Projects/shokunin/mori-shokunin`). Fleet root
`/home/vgpnk/Projects/shokunin`. Seat: scribe, leaf member — no subagent dispatch.

- Contract read first: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/contract.md`
  (C1 target: the 25-path gate registry; C1 kill rule: a path with no conformant row, two
  non-superseded rows, an unresolved path, or an empty owner/self-test cell fails the claim).
- Freeze revision `7370a731abcafc4c803111de7c22cd6264d63be1` (controls + selftests committed).
  Entering revision `325f7e639916fcbc77fa2ec7475951a1b86bb1cb`. Working tree HEAD during this seat
  = `7370a731abcafc4c803111de7c22cd6264d63be1`; `git status --porcelain` showed only the untracked
  round-61 wave files (`build-w1-spec.py`, `w1-dispatch.json`, `w1-spec.json`, `w1.ready*`, `w1/`),
  none of them mine. No production file was edited. No commit, no VCS mutation, no fleet or sibling
  repo write.
- Scratch root: `/fast/scratch/hyaku/mori-r61/Mo61ScribeReg5657/` (created with `mkdir -p`;
  `TMPDIR` pointed there for every counter run). Removed at the end of this seat (§Cleanup).
- Disk guard checked before any work: `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`
  → `/fast/scratch/hyaku 49% 416.4G free`, `/tmp 24% 97.5G free`, `/var/tmp 41% 533.9G free` — green,
  no ENOSPC.
- Tooling: none installed or upgraded this seat (plain `python3` only). Per
  `/home/vgpnk/.omp/agent/RULES.md` the pacman channel is paused host-wide, so no pacman transaction
  was attempted and there is nothing to record in the tooling channel log.

## Scope

The same task as seat `Mo61ScribeReg5253`, restricted to the round-56 and round-57 gates — 7 paths
of the 25 in `.ufo/waves/round-61/gate-manifest.json`:

| # | path (manifest) | manifest `landing` | round |
|---|---|---|---|
| 1 | `.ufo/waves/round-56/count-c1.py` | `3f494b49cde612d929e82887a48e1660c022c359` | 56 |
| 2 | `.ufo/waves/round-56/count-c2.py` | `3f494b49cde612d929e82887a48e1660c022c359` | 56 |
| 3 | `tools/mori-vote-bind.py` | `c419fe6dc051a5828fabd5f472f851e76dd54e8d` | 56 |
| 4 | `tools/mori-driver-liveness.py` | `c419fe6dc051a5828fabd5f472f851e76dd54e8d` | 56 |
| 5 | `.ufo/waves/round-57/count-c1.py` | `618562c72a03dc4d17386b715357f863fd327274` | 57 |
| 6 | `.ufo/waves/round-57/count-c2.py` | `618562c72a03dc4d17386b715357f863fd327274` | 57 |
| 7 | `.ufo/waves/round-57/verify-c2-source.py` | `6f3f84820911bafbb3f66cdcb080368c9242303f` | 57 |

The other 18 manifest paths (r52–r55, r58–r60 counters and the three r59/r60 lane tools) are other
seats' scope and are **not** drafted here.

## Method — the bytes were materialized read-only from the landing commits

No working-tree file was executed. Every instrument was extracted with `git show <landing>:<path>`
into scratch and run there:

```
R=/home/vgpnk/Projects/shokunin/mori-shokunin
S=/fast/scratch/hyaku/mori-r61/Mo61ScribeReg5657
git -C $R show 3f494b49cde612d929e82887a48e1660c022c359:.ufo/waves/round-56/count-c1.py > $S/land/r56c1.py
git -C $R show 3f494b49cde612d929e82887a48e1660c022c359:.ufo/waves/round-56/count-c2.py > $S/land/r56c2.py
git -C $R show c419fe6dc051a5828fabd5f472f851e76dd54e8d:tools/mori-vote-bind.py        > $S/land/vote.py
git -C $R show c419fe6dc051a5828fabd5f472f851e76dd54e8d:tools/mori-driver-liveness.py  > $S/land/drv.py
git -C $R show 618562c72a03dc4d17386b715357f863fd327274:.ufo/waves/round-57/count-c1.py > $S/land/r57c1.py
git -C $R show 618562c72a03dc4d17386b715357f863fd327274:.ufo/waves/round-57/count-c2.py > $S/land/r57c2.py
git -C $R show 6f3f84820911bafbb3f66cdcb080368c9242303f:.ufo/waves/round-57/verify-c2-source.py > $S/land/r57v.py
```

The two lane tools need their fixture tree beside them (`_repo_path()` resolves
`<parent-of-tools>/.ufo/waves/round-56/fixtures/driver`), so the tree was extracted too:

```
git -C $R archive c419fe6dc051a5828fabd5f472f851e76dd54e8d .ufo/waves/round-56/fixtures/driver -o $S/drv-fixtures.tar
tar -xf $S/drv-fixtures.tar -C $S/mat/r56c1      # 11 files, 9 fixture dirs
```

Extracted shas (all at the manifest `landing`, `sha256sum`):

```
c4e58eedadda2f7069bb8f31c5b1b6ae527a54aecaa7490308a55f127047f71d  r56 count-c1.py   @3f494b49
4b350c773a3c31e54cf2cb0e3d7a5c8e92d9a1101722c9a94f53db2492812465  r56 count-c2.py   @3f494b49
8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca  mori-vote-bind.py @c419fe6d
5befd4909ee68b4303afdaf58aed84034d4bb3f2b82454285116e2a8e934718a  mori-driver-liveness.py @c419fe6d
7156fb4bb29f27881091b22dfa7ef3d661b1e955a1ec9a4d13e48013f1b368ec  r57 count-c1.py   @618562c7
0fe9e6f4cdde0ac14bd8cad907e948edcb8a51f7c950622cf84cae5f1f75f742  r57 count-c2.py   @618562c7
def916fc2cc92b731dc10a749beff9d193e5ccb879c714e4587f5481d95723a4  r57 verify-c2-source.py @6f3f8482
```

## Measured selftest lines (one run each, at the landing commit, in scratch)

```
$ python3 $S/land/r56c1.py --selftest
C1_COUNTER_SELFTEST pass=1 fail=0                       rc=0

$ python3 $S/land/r56c2.py --selftest
C2_COUNTER_SELFTEST pass=1 fail=0                       rc=0

$ python3 $S/mat/r56c2/tools/mori-vote-bind.py --selftest
VOTE_BIND_SELFTEST pass=16 fail=0                       rc=0

$ python3 $S/mat/r56c1/tools/mori-driver-liveness.py --selftest
DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0       rc=0

$ python3 $S/r58c1-land.py --selftest      # .ufo/waves/round-58/count-c1.py @fe880112
C1_SELFTEST pass=4 fail=0                  rc=0

$ python3 $S/r58c2-land.py --selftest      # .ufo/waves/round-58/count-c2.py @fe880112
C2_SELFTEST pass=6 fail=0                  rc=0
```

Live arms of the two r56 counters at their own landing commit (they are the instruments that
already ran green there):

```
$ python3 $S/land/r56c1.py 3f494b49cde612d929e82887a48e1660c022c359
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=3f494b49cde612d929e82887a48e1660c022c359   rc=0
$ python3 $S/land/r56c2.py 3f494b49cde612d929e82887a48e1660c022c359
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=3f494b49cde612d929e82887a48e1660c022c359   rc=0
```

The r57 trio has **no `--selftest` mode at any revision** (§Findings F1), so its rows cite the
round-58 successor batteries above, which are the repaired instruments for the same two r57 claims
and carry real `--selftest` branches. The r57 spotcheck was measured at its landing commit:

```
$ python3 $S/land/r57v.py $S/entry-r57-6f3f.md $S/src-r57-6f3f.py
C2_SOURCE_CHECK ok rows=8 mismatches=0     rc=0
```

## Draft registry rows (for L1 integration into SKILL.md)

One row per line, exact 8 cells, no raw `|` inside any cell (see F2 — an escaped `\|` breaks the
frozen parser). The entry cell names the artifact path verbatim; the self-test cell names the
runnable `--selftest` command **and** the measured output line; the owner cell names the landing
round's L1 (`hyaku closure` for the spotcheck-only artifact).

```markdown
| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| r56 driver-liveness coverage counter (C1) | gate | `python3 .ufo/waves/round-56/count-c1.py <rev> [--repo DIR]` | 0 → `C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=R` · 1 → `C1=unmet … failed=<checks>` (tool_absent, pins, selftest, selftest_absent, fixtures, entry, row, norem) · 2 → `C1_SETUP: unresolvable revision R` | `python3 .ufo/waves/round-56/count-c1.py --selftest` → `C1_COUNTER_SELFTEST pass=1 fail=0` (rc 0, measured on the landing bytes 3f494b49) | `PIN` = sha256 `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997` of `tools/mori-driver-liveness.py` (data commit 6ced9da9; the manifest landing c419fe6d carries the pre-norem-fix bytes `5befd490…`, where this counter reads `failed=pins,norem`) · `EXPECT_SELFTEST` = `DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0` · `EXPECT_FIX` = 9 fixture dirs under `.ufo/waves/round-56/fixtures/driver` (malformed 5) · `ENTRY` `corpus/knowledge/driver-liveness-r56.md` · source row `S544` | none (read-only `git show` / `git ls-tree` / `git rev-parse`; the selftest and fixture arms materialize the tool and the fixtures under the caller's `TMPDIR`) | MoriR56 |
| r56 dual-shape vote-binder operability counter (C2) | gate | `python3 .ufo/waves/round-56/count-c2.py <rev> [--repo DIR]` | 0 → `C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=R` · 1 → `C2=unmet … failed=<checks>` (tool_absent, pins, r55_artifacts_absent, selftest, tally, control, contrast, contrast_absent, entry, row) · 2 → `C2_SETUP: unresolvable revision R` | `python3 .ufo/waves/round-56/count-c2.py --selftest` → `C2_COUNTER_SELFTEST pass=1 fail=0` (rc 0, measured on the landing bytes 3f494b49) | `PIN` = sha256 `8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca` of `tools/mori-vote-bind.py` (data commit c419fe6d) · `EXPECT_SELFTEST` = `VOTE_BIND_SELFTEST pass=16 fail=0` · `EXPECT_TALLY` = `TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15` · `VOTERS` = `Mo55Rc01` … `Mo55Rc16` · `LEDGER` `corpus/knowledge/kernel-v7.3-recheck-r55.md` · `RESULTS` `.ufo/waves/round-55/w1-results.json` · `ENTRY` `corpus/knowledge/vote-binding-r56.md` · source row `S545` | none (read-only `git show` / `git rev-parse`; the executed arms materialize the tool and the committed round-55 artifacts under the caller's `TMPDIR`) | MoriR56 |
| dual-shape seat-output vote binder (r56 C2 instrument) | gate (lane tool; read-only; invoked by the r56 C2 counter) | `python3 tools/mori-vote-bind.py extract [--verb RECHECK or ENTAIL] <file> …` or `python3 tools/mori-vote-bind.py tally --ledger PATH --results PATH --verb VERB [--voter NAME …] [--min N] [--disposition-cols N]` or `python3 tools/mori-vote-bind.py --selftest` | extract → 0, one `VOTE <verb> <hash12> <word> <channel> <rest>` line per bound vote · tally → 0, one `TALLY rows=N agree=N double=N single=N zero=N dissent=N voters=N bound_voters=N` line (the caller reads the tally) · setup → 2, `VOTE_BIND_SETUP: …` on stderr · selftest → 0 with `VOTE_BIND_SELFTEST pass=16 fail=0`, else 1 | `python3 tools/mori-vote-bind.py --selftest` → `VOTE_BIND_SELFTEST pass=16 fail=0` (rc 0, measured on the landing bytes c419fe6d) | sha256 `8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca` at landing c419fe6d · 16 selftest cases · grammar `<verb> <hash12> <word> [rest]` with `verb` in RECHECK or ENTAIL and `hash12` exactly 12 lowercase hex digits · two channels (JSON string scalars, else unfenced text lines), never mixed; last write wins per (verb, hash) · limit: a bound vote proves a captured seat output carried the line, not that the judgment is right | none (opens inputs read-only; the selftest writes only under the caller's `TMPDIR`) | MoriR56 |
| strict per-event driver-liveness probe (r56 C1 instrument) | gate (lane tool; read-only; detection and report only) | `python3 tools/mori-driver-liveness.py [--fleet-root DIR] [--log PATH] [--state-dir DIR] [--now EPOCH] [--fixture DIR] [--selftest]` | 0 → one JSON object, schema `mori-driver-liveness-v1`, `verdict=DRIVER_LIVENESS_OK` · 2 → setup, or `verdict=DRIVER_LIVENESS_UNAVAILABLE` (log missing, unreadable or empty — unavailable is never zero) · selftest → 0 with `DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0`, else 1 | `python3 tools/mori-driver-liveness.py --selftest` → `DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0` (rc 0, measured on the landing bytes c419fe6d with the frozen fixture tree) | sha256 `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997` at HEAD (the manifest landing c419fe6d carries the pre-norem-fix bytes `5befd490…`) · 13 selftest cases over 9 fixture dirs under `.ufo/waves/round-56/fixtures/driver` · the selftest resolves that tree two levels above the tool file, so it must run inside a checkout that carries it · no health-verdict word (healthy, unhealthy, failed lane) may appear before the selftest section · limit: every field is a log-shape fact; `unclosed` is a pairing count, not a failure claim | none (opens its inputs read-only; writes nothing) | MoriR56 |
| r57 active-register capability-row counter (C1) | gate | `python3 .ufo/waves/round-57/count-c1.py <rev>` (the lane repo path is hardcoded; no `--repo` option) | 0 → `C1=met rows=2 evidence=ok rev=R` · 1 → `C1=unmet rows=N evidence=bad rev=R` (it reads the first `## Capabilities` section of `SCORECARD.md` at R, so it false-negatives on the landed rows — the two round-56 rows sit in the active register, and the round-57 defect is repaired by the round-58 counter) | no mode of its own: `--selftest` is read as the revision argument (`C1=unmet rows=0 evidence=bad`, rc 1); the repaired successor instrument's battery is `python3 .ufo/waves/round-58/count-c1.py --selftest` → `C1_SELFTEST pass=4 fail=0` (rc 0, measured on the landing bytes fe880112) | sha256 `7156fb4bb29f27881091b22dfa7ef3d661b1e955a1ec9a4d13e48013f1b368ec` at landing 618562c7 · reads `SCORECARD.md` at R, the `## Capabilities` section up to `## Saturation` · requires exactly 2 rows naming `driver-liveness` and `vote-binding`, each carrying a `.ufo/waves/round-56/` pointer and the round-56 first-working marker · limit: it scores the row text, not the capability | none (read-only `git show`) | MoriR57 |
| r57 sourced unclosed-pairing entry counter (C2) | gate | `python3 .ufo/waves/round-57/count-c2.py <rev>` (the lane repo path is hardcoded; no `--repo` option) | 0 → `C2=met claims=8 source=ok quotes=ok rev=R` · 1 → `C2=unmet claims=N source=bad rev=R` (entry `corpus/knowledge/watchdog-unclosed-r57.md` absent, or its `S548` source row not mined, or a claim row without a backticked quote) | no mode of its own: `--selftest` is read as the revision argument (`C2=unmet claims=0 source=bad rev=--selftest`, rc 1); the repaired successor instrument's battery is `python3 .ufo/waves/round-58/count-c2.py --selftest` → `C2_SELFTEST pass=6 fail=0` (rc 0, measured on the landing bytes fe880112) | sha256 `0fe9e6f4cdde0ac14bd8cad907e948edcb8a51f7c950622cf84cae5f1f75f742` at landing 618562c7 · entry `corpus/knowledge/watchdog-unclosed-r57.md` with 8 `K` claim rows · `SOURCES.md` row `S548` mined · limit: the quote predicate only checks that a claim row carries a backtick, never that the quote occurs in the pinned source copy (the round-57 routed defect, repaired by the round-58 counter) | none (read-only `git show`) | MoriR57 |
| r57 independent quote re-read of the unclosed-pairing entry | spotcheck (independent re-read of the eight `K` quotes; not the claim's counting command) | `python3 .ufo/waves/round-57/verify-c2-source.py <entry.md> <source-copy.py>` | 0 → `C2_SOURCE_CHECK ok rows=8 mismatches=0` · 1 → `C2_SOURCE_CHECK unmet rows=N mismatches=<K1,…>` (a row whose backticked quote does not occur on the line the row states, or a malformed row) | no mode of its own: `--selftest` is read as an entry path and the script exits 1 with an argv unpack error; the repaired successor instrument's battery is `python3 .ufo/waves/round-58/count-c2.py --selftest` → `C2_SELFTEST pass=6 fail=0` (rc 0, measured on the landing bytes fe880112) | sha256 `def916fc2cc92b731dc10a749beff9d193e5ccb879c714e4587f5481d95723a4` at landing 6f3f8482 · reads two files given on the command line (the entry and its pinned source copy) · checks each `K1` … `K8` quote occurs on the line the row states · measured at landing: `C2_SOURCE_CHECK ok rows=8 mismatches=0` (rc 0) | none (opens the two given files read-only; writes nothing) | hyaku closure |
```

## Falsification of the drafts against the frozen counter (before handing them to the L1)

The drafts were **not** written into `SKILL.md`. They were validated in throwaway scratch repos by
calling the frozen `.ufo/waves/round-61/count-c1.py` `measure()` directly against a scratch `SKILL.md`
containing only the drafted table.

**(a) All 7 rows register, 0 thin, 0 dup, 0 noselftest, 0 unres, 0 noowner:**

```
$ python3 - <<'EOF'   # builds a scratch git repo with the 7 paths + the drafted SKILL.md, then calls measure()
...
C1=met gates=7 registered=7 missing=0 thin=0 dup=0 unres=0 noselftest=0 noowner=0 failed=none rev=8f53045af12490f7f024562b282d5c7ce58b529e
EOF
```

**(b) Against the real 25-path manifest, my 7 rows register exactly 7 and leave the other 18
missing** — no cross-talk with a sibling seat's paths:

```
C1=unmet gates=25 registered=7 missing=18 thin=0 dup=0 unres=0 noselftest=0 noowner=0
failed=missing:.ufo/waves/round-52/count-c1.py,…,missing:tools/mori-entry-claims-check.py
```

**(c) The frozen counter's own selftest still passes and the before-state is confirmed unmet:**

```
$ python3 .ufo/waves/round-61/count-c1.py --selftest --scratch $S/c1st
case good: ok=True want=True pass failed=[]
case missing: ok=False want=False pass failed=['missing:tools/absent.py']
case thin: ok=False want=False pass failed=['thin:tools/h.py:owner']
case noselftest: ok=False want=False pass failed=['noselftest:tools/i.py']
case superseded-ok: ok=True want=True pass failed=[]
case unres: ok=False want=False pass failed=['missing:tools/nothere.py']
C1_SELFTEST pass=6 fail=0                                                  rc=0

$ python3 .ufo/waves/round-61/count-c1.py HEAD --repo $R --scratch $S/c1st
C1=unmet gates=25 registered=0 missing=25 thin=0 dup=0 unres=0 noselftest=0 noowner=0 failed=missing:… rc=1
```

The before-state at the measured revision is `registered=0 missing=25` — every one of the 25 gates
is currently unregistered, exactly as the contract's control states.

## Findings

**F1 — the round-57 trio has no `--selftest` mode, at any revision, ever.** Measured across the
full history of all three files:

```
.ufo/waves/round-57/count-c1.py : '--selftest' occurrences over all revisions = 0
.ufo/waves/round-57/count-c2.py : '--selftest' occurrences over all revisions = 0
.ufo/waves/round-57/verify-c2-source.py : '--selftest' occurrences over all revisions = 0
```

Running the flag against them shows what a reader would see — it is not a selftest, it is a
misparse:

```
$ python3 $S/land/r57c1.py --selftest
C1=unmet rows=0 evidence=bad                    rc=1     # "--selftest" taken as the revision argument
$ python3 $S/land/r57c2.py --selftest
C2=unmet claims=0 source=bad rev=--selftest      rc=1
$ python3 $S/land/r57v.py --selftest
ValueError: not enough values to unpack (expected 2, got 1)   rc=1
```

Consequence for C1: the frozen counter's `noselftest` arm keys on the literal string `--selftest`
appearing in the self-test cell (`count-c1.py:109` — `if "--selftest" not in row["selftest"]`), so a
row for these three paths can only name a **different** instrument's `--selftest`. The rows above
therefore cite the round-58 successor batteries (`C1_SELFTEST pass=4 fail=0`,
`C2_SELFTEST pass=6 fail=0`), which are the repaired instruments for the same two r57 claims
(r58's docstrings name the r57 defects they fix) and carry real `--selftest` branches. This is a
**reading, not a claim about the r57 files** — the r57 files themselves have no runnable selftest.
The L1 may prefer to (a) accept these rows as drafted, (b) accept them but add a prose note that
the r57 trio is selftest-less by construction, or (c) hold the r57 rows pending a round-61 repair —
but a repair is a counter change, which the contract bars after the freeze. My recommendation is
(a) plus the prose note, since the drafted rows are honest about the absence.

**F2 — an escaped `\|` inside a registry cell silently drops the row.** The frozen parser splits
cells on the raw character (`count-c1.py:51`, `lines[i].strip().strip("|").split("|")`; header match at `:47`), so a
`\|` inside a cell produces 9 fields and the row is not collected. Measured directly against the
frozen `parse_tables`:

```
escaped-pipe row  -> parsed rows = 0        # the row vanishes
no-pipe row       -> parsed rows = 1        # owner='MoriR56', '--selftest' present
```

This is why the drafted rows above use `·` and `…` separators and no `|` at all. Note this is a
**frozen-counter parser property**, not something this seat may change; it is reported so the L1
does not paste a re-formatted row that loses its registration. (Three pre-existing SKILL.md rows
are already invisible to this parser for the same reason — `SKILL.md:172` 9 cells, `SKILL.md:739`
10 cells, `SKILL.md:938` 16 cells — but those rows name no manifest path, so they do not affect
this round's 25-gate count.)

**F3 — a sibling row that cross-references a round-57 path in its **entry** cell creates a
`dup` failure.** `row_hits` matches on the entry cell (`count-c1.py:62-70`, path match at `:68`), and the
live-filter only exempts rows whose *name* or *scope* cell says "superseded" (`count-c1.py:97-98`). Measured scenario —
an added r58 row whose entry cell reads `(supersedes .ufo/waves/round-57/count-c1.py)`:

```
HAZARD SCENARIO (sibling r58 row cross-references the r57 path in its ENTRY cell):
C1=unmet gates=7 registered=6 missing=0 thin=0 dup=1 unres=0 noselftest=0 noowner=0
failed=dup:.ufo/waves/round-57/count-c1.py
```

and the same row marked `superseded:` in its **scope** cell instead:

```
after marking that r58 row superseded in scope: live rows for r57 path = 1
```

**Integration constraint for the L1:** the r58/r59/r60 seats must not name a round-56 or round-57
path in an entry cell (or must put "superseded" in that row's scope cell). My own seven rows are
clean on this axis — each names exactly one manifest path in its entry cell, verified by
`row_hits` over the full 25-path manifest (7 hits, one per intended path, zero cross-hits). Note
also that the drafted r57 rows name `round-58` paths in their **self-test** cells, not their entry
cells, so they cannot collide with the r58 seat's rows either.

**F4 — the r57 counters hardcode the lane path and have no `--repo` option.** Both
`.ufo/waves/round-57/count-c1.py:6` and `.ufo/waves/round-57/count-c2.py:4` embed
`repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"`; only `sys.argv[1]` (the revision) is
readable. The drafted rows record this in the entry cell rather than presenting a `--repo`
flag that does not exist. (The r56 counters do accept `--repo`; `count-c1.py:178-179`,
`count-c2.py:145-146`.)

**F5 — `tools/mori-driver-liveness.py` drifted between the manifest landing and HEAD.** The
manifest records landing `c419fe6d` (sha `5befd490…`); HEAD carries `6b3dba74…` after the round-56
data correction `6ced9da9` ("driver probe docstring carries no health-verdict words"). The r56 C1
counter pins the **HEAD** bytes (`PIN = 6b3dba74…`, `count-c1.py:46`) and its `norem` arm rejects
the pre-correction bytes. Measured:

```
$ python3 $S/land/r56c1.py c419fe6dc051a5828fabd5f472f851e76dd54e8d
C1=unmet selftest=ok fixtures=ok entry=ok row=ok norem=bad rev=c419fe6d… failed=pins,norem   rc=1
$ python3 $S/land/r56c1.py 6ced9da9b1f9c65065a8158735e0331938e8a599
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=6ced9da9…                        rc=0
```

Both drafts record the two shas explicitly so the reader cannot mistake the landing bytes for the
pinned ones. The manifest `landing` field for this path is therefore a *first-landing* revision, not
the byte-pinning revision — the same is true for five other manifest paths (r59 c1/c2, r60 c2/c3,
`tools/mori-register-check.py`, `tools/mori-entry-claims-check.py`), which I list here only as a
fact about the manifest, not as a claim about this seat's rows. No manifest path is a substring of
another, so the substring branch of `row_hits` cannot misfire.

**F6 — the r57 C1 counter is a known false-negative at every revision, and my row says so.** It
selects the **first** `## Capabilities` section of `SCORECARD.md` (`SCORECARD.md:596`) and the
first `## Saturation` heading (`SCORECARD.md:604`) — that window holds the superseded
`| — none yet — | | | |` stub row at `SCORECARD.md:600`, not the active register — so it reads
`rows=0` even though the two round-56 rows sit in the active register at `SCORECARD.md:1989-1990`:

```
$ python3 $S/land/r57c1.py 7370a731abcafc4c803111de7c22cd6264d63be1
C1=unmet rows=0 evidence=bad rev=7370a731abcafc4c803111de7c22cd6264d63be1   rc=1
```

The round-58 counter `fe880112` documents and fixes exactly this ("the r57 counter selected the
FIRST '## Capabilities' section … so it false-negatived on the landed round-56 rows"), and the
round-57 closure recorded the same false-negative. Registering the r57 row therefore documents a
known-defective instrument rather than certifying it — the drafted verdict-map cell states the
false-negative and the repair in the same cell, so a reader cannot mistake the row for a green
claim.

**F7 — the r57 C2 counter's quote predicate never reads the source copy.** `count-c2.py:14` checks
only `` "`" in x and "`" in x `` on the claim row — the quote's presence as a backticked span, never
its occurrence in `corpus/evidence/sources-r57/mori-driver-liveness.py`. That is the round-57 routed
defect 2, recorded in the round-57 closure and fixed by round-58's count-c2 ("the r57 depth counter
never read the source copy and accepted any backticked text, so a full false-green fixture scored
met"). The drafted row names this limit explicitly. The independent spotcheck
`.ufo/waves/round-57/verify-c2-source.py` is the artifact that *does* resolve each quote against
the pinned copy — which is why its kind cell is `spotcheck` and its owner cell is `hyaku closure`
rather than a round L1: it is a cross-check on the claim, not the claim's counting command.

## Out of scope

No edit to `SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/`, `tools/`, the gate manifest, or any other
production file; no registry row was appended (the L1 integrates). No git or jj mutation anywhere:
every git call was `git show` / `git ls-tree` / `git cat-file -e` / `git rev-parse` / `git archive`
against the lane repo, or `git init`/`add`/`commit` inside `mktemp`-style scratch fixture repos
under my own scratch root. No write to the fleet repo or any sibling repo. No service, config or
host-state change; no remediation; no provider-death inference. Nothing was run under `/tmp`.

## Cleanup

Scratch `/fast/scratch/hyaku/mori-r61/Mo61ScribeReg5657/` (extracted landing bytes, fixture trees,
synthetic fixture repos, `TMPDIR`) is removed before this report is filed; the only retained
artifacts are the measured lines quoted verbatim above. The scratch root's parent
`/fast/scratch/hyaku/mori-r61/` is left in place for the other round-61 seats.

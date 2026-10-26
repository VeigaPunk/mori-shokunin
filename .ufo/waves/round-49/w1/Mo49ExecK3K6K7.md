# Mo49ExecK3K6K7 — K3 (pin deletion), K6 (floor slack) and K7 (line-count rebinding) closed in a pin-reconciler copy

**Seat.** Mo49ExecK3K6K7 (executor, wave w1). Leaf seat: the one read-only labrat slot was not used;
no subagent dispatched, no task/agent/workpool call, no background orchestration. **Lane.**
`/home/vgpnk/Projects/shokunin/mori-shokunin` (HEAD `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`, the
round-49 freeze commit; lane tip `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86`, the entering revision this
seat measures). **Contract read:** `.ufo/waves/round-49/contract.md` (frozen at `0df17b7b`).
**Class source:** `.ufo/waves/round-48/w2/R48CritV3Junk2.md` §K3, §K6, §K7 (with §K5 and §X1 explicitly
left to other seats).

**Deliverable (scratch, not landed).** `.scratch/r49-Mo49ExecK3K6K7/mori-pin-check.py`,
sha256 `811d5188ab6fc4d36c24c9061179d634a4013d93250a5190db3b77e938c2666d`, derived from the frozen
control `.ufo/waves/round-49/controls/tool-r48-merged-witness.py` (sha256
`c30ab6232893d984d1440784b6ce962d7c987c6d5538db0ead2f458a8ea1c9f0`, verified against
`evidence/freeze-sha256.txt`). Diff
`.scratch/r49-Mo49ExecK3K6K7/patched.diff` (226 diff lines, 111 added / 12 removed, 14 hunks, sha256
`dcc3be67ba392d8ee4585fb6640fc8da112dece09ffb59eb772e1fa7a98662a7`). The L1 integrates; this seat wrote
no lane file except this report.

**No new CLI flag.** The three rules are on by default; the only new argument is an internal
`check(..., self_instrument=…)` keyword whose default is the module constant (`:525-526`), used by the
selftest to prove both directions of R13. `--rev`, `--repo`, `--skill`, `--min-tally-pins`,
`--baseline-rev`, `--timeout`, `--root`, `--selftest` are unchanged, and the `PIN_CHECK=` field set is
byte-identical (no new counter is printed — every new finding lands in an existing fatal field:
`dropped` or `mismatches`).

---

## 1. The three rules

Each rule is the smallest change that makes a *deleted* or *rebound* pin visible, in the file that
already owns the pin kind. None of them rejects an honest row: the honest shapes are arms of their own
(§3) and the false-red sweep of §4 measures them against five earlier registries.

### R12 — K3: the presence counter reads every pin kind (`pin_keys`, `:482-508`)

`pin_keys` counted only tally prefixes and **full** `[0-9a-f]{64}` digests, so a line-count pin
(`(N lines)`) or a truncated-digest pin (`<hex>{8,63}…`) existed only while present: deleting one moved
nothing except `digest_pins` (for a truncated digest) and the registry stayed `PIN_CHECK=met`.

```python
n_digest = len(HEX_RE.findall(st)) + len(TRUNC_DIGEST_RE.findall(st))   # :500
if n_digest:
    keys[(name, "digest")] = keys.get((name, "digest"), 0) + n_digest
n_lines = len(LINE_COUNT_RE.findall(st))                                # :504
if n_lines:
    keys[(name, "lines")] = keys.get((name, "lines"), 0) + n_lines
```

The counted key set is now `(row name, tally prefix)` · `(row name, "digest")` · `(row name, "lines")`,
so `check()`'s existing baseline loop (`gone = n - now.get(k, 0)`) reports a deleted line-count or
truncated-digest pin as `dropped`, exactly as it already did for a deleted tally.

*The kind is `digest`, not `sha256` or `trunc`, on purpose*: the baseline carries the stale truncated pin
`c39e5a73…` on row `r14 regressions`, and the landed revision carries `533218a566030fda…` — the same
kind, so the round-48 repair is a repair and not a deletion. An identity-based extension (the naive
"same truncated hex must still be present") reds the landed tip; the critic measured this and the kind
count is what survives it (`w2/R48CritV3Junk2.md` §K3). No 64-hex token in `SKILL.md@b3e3453d` is
followed by `…` (measured: `grep -oE '[0-9a-f]{64}…'` → 0 matches), so full and truncated counts cannot
double-count the same token.

### R13 — K6: a tree that ships the reconciler must pin it (`:725-731`)

The floor is not the defect; the *uncovered row* is. Measured at the two revisions the counter uses:

| revision | parsed rows | tally pins | digest pins | line-count pins |
|---|---|---|---|---|
| `2d85e33d` (`--baseline-rev`) | 53 | 26 | 8 | 2 |
| `b3e3453d` (measured R) | 58 | 31 | 8 | 2 |

`--min-tally-pins 26` is exactly the baseline's tally total, so a floor derived from the baseline
(`max(min_tally, baseline_total)`) would be inert — and it cannot see the defect anyway: the critic's
`DEL-self-row` deletes the row that pins the reconciler, which is **new since the baseline**, leaving
`tally_pins=30 ≥ 26` (measured, §2). Per-key `dropped` cannot see it either, because the key is new.
So the smallest rule that closes the demonstrated deletion is an obligation on the instrument under
measurement:

```python
SELF_INSTRUMENT = "tools/mori-pin-check.py"                                    # :146
...
if (self_instrument and os.path.isfile(os.path.join(root, self_instrument))
        and self_instrument not in bound_instruments):                          # :727-730
    counts["dropped"] += 1
    out.append("pin kind=self state=dropped instrument=%s" % self_instrument)
```

`bound_instruments` is the set of `instrument_of(argv)` over every tally pin a row *binds* (`:687`), so
a row that *names* the reconciler in prose does not satisfy it — only a bound command that runs it does.
The obligation is conditional on the file existing in the measured tree, so it fails open on trees that
do not ship the reconciler (the counter's two fixture arms N10/H5, the `2d85e33d` export, and every
pre-round-47 revision) and never invents a finding there.

This is the *tool-side* half of K6. The other half is a contract number this seat cannot change: the
frozen counter passes `--min-tally-pins 26` and the contract freezes that spelling. Recommendation to the
L1, not a claim: raise the counter's floor to the landed count (31) in a future round, or keep 26 and
rely on R13 (`dropped` per key already covers every pin that *is* in the baseline — the slack is only
exploitable against new rows, which R13 closes for the one instrument that matters).

### R14 — K7: a line count binds the instrument the row runs (`line_count_pins`, `:359-373`)

R5 bound `(N lines)` to the nearest preceding in-tree path of the self-test cell, with no tie to the
row's instrument, so a decoy path in the same cell took the pin — and the value could even be *true* of
the decoy. R14 passes the row's allowed paths in:

```python
binds = pin_commands(cells, idx, rev, row["eidx"])                    # :612
allowed = {instrument_of(w) for _p, _t, w in binds if w}               # :613
if claimed:
    allowed.add(claimed)
...
for num, relpath, bound in line_count_pins(st, root, allowed):         # :638
    ...
    if not bound:
        counts["mismatches"] += 1
        out.append("pin line=%d kind=lines state=mismatch pinned='%d lines' file=%s "
                   "reason=path-not-row-instrument bound=%s" ...)
```

`binds` is the same binding list the tally loop uses (the row loop no longer computes it twice), so the
line-count and the tally branch cannot disagree about which argv the row runs. Cost check at R: both
landed line-count pins (rows 184, 194) bind `tools/mori-gate-registry.py`, which is the bound argv path
of both rows — measured `state=match` in every arm of §4.

---

## 2. Reproducers — the round-48 shapes are green on the frozen control, red on the copy

Harness `.scratch/r49-Mo49ExecK3K6K7/falsify.py` applies the critic's exact edits to
`SKILL.md@b3e3453d` (a non-unique or absent anchor is an arm error, never a pass) and scores both tools
with **`count-c1.py`'s own `run_tool`**, the counter's flags (`--rev b3e3453d --repo lane
--min-tally-pins 26 --baseline-rev 2d85e33d`) and `TMPDIR` inside this seat's scratch. Raw output:
`.scratch/r49-Mo49ExecK3K6K7/attack-lines.txt` (patched, with the killing pin line) and the falsifier's
stdout below.

```
tool=patched variant=real               got=met   rc=0
tool=patched variant=k3-del-linecount   got=unmet rc=1
tool=patched variant=k3-del-trunc-digest got=unmet rc=1
tool=patched variant=k6-del-self-row    got=unmet rc=1
tool=patched variant=k7-rebind-linecount got=unmet rc=1
tool=witness variant=real               got=met   rc=0
tool=witness variant=k3-del-linecount   got=met   rc=0
tool=witness variant=k3-del-trunc-digest got=met   rc=0
tool=witness variant=k6-del-self-row    got=met   rc=0
tool=witness variant=k7-rebind-linecount got=met   rc=0
```

The witness reproduces all four round-48 survivors at the same anchors; the copy rejects all four. The
killing lines (`capture.py` → `attack-lines.txt`; `PIN_CHECK=` lines verbatim):

| arm | edit (exact substring of `SKILL.md@b3e3453d`) | finding on the copy |
|---|---|---|
| K3 line-count | delete `" (743 lines)"` from row 184 | `pin kind=baseline state=dropped row='r44 gate registry (C2)' pin=lines count=1` → `PIN_CHECK=unmet … dropped=1` |
| K3 truncated digest | delete `"at sha256 \`37fd7c24ff52…\`; "` from row 192 | `pin kind=baseline state=dropped row='r45 corpus coverage (C3)' pin=digest count=1` → `PIN_CHECK=unmet tally_pins=31 digest_pins=7 … dropped=1` |
| K6 self row | delete the whole row `\| registry pin reconciler (r47, C1) \| …` (line 938) | `pin kind=self state=dropped instrument=tools/mori-pin-check.py` → `PIN_CHECK=unmet tally_pins=30 … dropped=1` (`tally_pins=30` still clears the frozen floor of 26: the floor alone cannot close this, as §1 argues) |
| K7 rebind | replace `" (743 lines)"` in row 184 with ``" of `tools/mori-unlanded-check.py` (209 lines)"`` (true of the decoy) | `pin line=184 kind=lines state=mismatch pinned='209 lines' file=tools/mori-unlanded-check.py reason=path-not-row-instrument bound=tools/mori-gate-registry.py` → `PIN_CHECK=unmet … mismatches=1` |

`tools/mori-unlanded-check.py` has 209 newlines at `b3e3453d` (measured from `git show`), so the decoy
pin is *true of the decoy* — the arm tests the binding, not the arithmetic.

---

## 3. `--selftest` and rule-kill mutants

The copy's own selftest, on the delivered bytes (`.scratch/r49-Mo49ExecK3K6K7/selftest.txt`):

```
EXIT=0
72 PASS lines
PIN_CHECK_SELFTEST pass=72 fail=0
```

Seven arms are new (65 → 72), one per direction of each rule:

| arm | what it pins | verdict |
|---|---|---|
| `r12_line_count_pin_deleted` | baseline has `(42 lines)`, current drops it | unmet `dropped=1` |
| `r12_trunc_digest_pin_deleted` | baseline has `at sha256 <hex>… of tools/foo.py`, current drops it | unmet `dropped=1` |
| `r12_trunc_digest_repaired_to_full` | baseline truncated → current full digest of the same file | **met** (the kind count, not the identity, is the obligation) |
| `r14_line_count_decoy_path` | `(3 lines)` true of `tools/old.py`, row runs `tools/lc.py` | unmet `mismatches=1` |
| `r13_self_row_deleted` | tree ships `tools/selfpin.py`, no row binds it | unmet `dropped=1`, `kind=self` |
| `r13_self_row_pinned` | same tree plus the row that binds it | **met** |
| `r13_self_instrument_absent_no_obligation` | `self_instrument` names a file the tree does not ship | **met** (fails open) |

Every arm is killed by removing its rule. Three single-rule mutants of the delivered bytes were built
(`mutant-no-r12.py` = truncated digests and line counts not counted; `mutant-no-r13.py` = obligation
block removed; `mutant-no-r14.py` = `line_count_pins(st, root, None)`), each run with `--selftest`:

```
== mutant-no-r12.py
FAIL r12_line_count_pin_deleted       (PIN_CHECK=met)
FAIL r12_trunc_digest_pin_deleted     (PIN_CHECK=met)
PIN_CHECK_SELFTEST pass=70 fail=2
== mutant-no-r13.py
FAIL r13_self_row_deleted             (PIN_CHECK=met)
PIN_CHECK_SELFTEST pass=71 fail=1
== mutant-no-r14.py
FAIL r14_line_count_decoy_path        (PIN_CHECK=met)
PIN_CHECK_SELFTEST pass=71 fail=1
```

No arm fails on the delivered bytes and no mutant kills an arm outside its own rule.

---

## 4. Acceptance: the frozen C1 counter against the copy at `b3e3453d`

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && \
  TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecK3K6K7 \
  timeout 3300 python3 .ufo/waves/round-49/count-c1.py \
    --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecK3K6K7/mori-pin-check.py \
    --rev b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 \
    --scratch /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecK3K6K7/acc-c1 --jobs 3
variant name=J1 expect=unmet got=unmet rc=1
… (J2-J8, N1-N10, H6, H7 identical) …
variant name=H1 expect=met got=met rc=0
… (H2-H4, H5 identical) …
variant name=real expect=met got=met rc=0
variant name=real-opaque expect=met got=met rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86
```

Full receipt: `.scratch/r49-Mo49ExecK3K6K7/acc-c1.txt` (sha256
`b299ce1b0550697e0ddcc951acbe3bc62ea95669d95de8e47d528034c26238f1`). Wall time 2124 s at `--jobs 3`
(two other heavy jobs were running concurrently on this 32-core host; the freeze's ~10-minute estimate
is for an uncontended host).

**Exit status, stated precisely:** the run was piped to `tee`, so the pipeline's exit status is `tee`'s
and was not captured separately. `count-c1.py` returns `0 if met else 1` from the same `met` flag that
prints the line, and the printed line is `C1=met`. This is the only clause of the acceptance I did not
observe as a process status — the L1's landed-tip run will observe it.

---

## 5. False-red check against five earlier SKILL.md revisions

Harness `.scratch/r49-Mo49ExecK3K6K7/false_red.py` → `false-red.txt` (sha256
`a52284e5bfd79f7b9b0af7727329916042eca5ec3062e52df0615d0552665c88`). Five earlier revisions —
`63eecf27` (round-47 freeze, first revision that ships the reconciler), `af2250d8` (v2), `4387cf94`
(round-48 freeze), `e4dfff32` (v3), `14c5110d` (round-48 end) — each in two arm shapes, each measured
with the witness **and** the copy, all with `--min-tally-pins 26 --baseline-rev 2d85e33d`:

* **Arm A (the shape the counter uses):** measure the tree at R, read `SKILL.md` as committed at the
  earlier revision (`--rev b3e3453d --skill early-<rev>.md`).
* **Arm B (revision shape):** measure the earlier revision as a revision (`--rev <rev>`).

| revision | arm A witness → copy | arm B witness → copy | field delta from R12/R13/R14 |
|---|---|---|---|
| `63eecf27` | unmet (`mismatches=2`) → unmet (`mismatches=2`, **`dropped=1`**) | unmet (`mismatches=2`) → unmet (`mismatches=2`, **`dropped=1`**) | `pin kind=self state=dropped instrument=tools/mori-pin-check.py` |
| `af2250d8` | unmet (`mismatches=2`) → unmet (`mismatches=2`) | unmet (`mismatches=1`) → unmet (`mismatches=1`) | none |
| `4387cf94` | unmet (`mismatches=2`) → unmet (`mismatches=2`) | unmet (`mismatches=1`) → unmet (`mismatches=1`) | none |
| `e4dfff32` | met → met | met → met | none |
| `14c5110d` | met → met | met → met | none |

`false_red_diffs=0 arms=20`: no verdict moves. The three earlier revisions that are already `unmet` are
`unmet` under the witness too, with identical `mismatches` counts — those pins are stale relative to the
tree/registry being measured (pre-existing, not caused by these rules; the mismatch counts match the
witness field for field).

The one field-level delta is R13 at `63eecf27`, and it is a **true** finding, not a false red: that
commit ships `tools/mori-pin-check.py` and its `SKILL.md` has no row that binds a tally to it (the row
landed one commit later, in `4dea3d09`). A registry that ships an unpinned instrument is precisely what
the rule names. The rule fails open where the file is absent (`2d85e33d`'s export, the counter's N10/H5
fixture repos), so the delta is confined to that one revision.

Two further cost checks:

* the two landed line-count pins (rows 184, 194) report `state=match file=tools/mori-gate-registry.py
  observed=743` in **all 20** false-red arms and in the four attack arms — R14's path tie costs nothing
  on today's registry;
* `--root` mode on the lane (`python3 -I -B copy --root <lane> --repo <lane>`, no baseline) prints the
  witness's line byte for byte apart from nothing: both are
  `PIN_CHECK=unmet tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=2 dropped=0 rebound=0
  duplicate=0 hidden=0 misattributed=0 min_tally_pins=1 rev=- baseline=no` — `no_command=2` is
  pre-existing (the same two rows bind nothing in `--root` mode), and R13's obligation is satisfied
  there (`dropped=0`).

---

## 6. Reproduce

```
S=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecK3K6K7
cd /home/vgpnk/Projects/shokunin/mori-shokunin
TMPDIR=$S python3 -I -B $S/mori-pin-check.py --selftest                  # PIN_CHECK_SELFTEST pass=72 fail=0
TMPDIR=$S python3 $S/capture.py                                          # four attack arms, killing lines
TMPDIR=$S python3 $S/falsify.py                                          # witness vs copy, 10 arms
TMPDIR=$S python3 $S/false_red.py                                        # 20 false-red arms
TMPDIR=$S python3 .ufo/waves/round-49/count-c1.py --tool $S/mori-pin-check.py \
  --rev b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 --jobs 3                # C1=met …
```

No tool was installed or updated for this seat (no pacman, no uv, no npm, no binary drop). Host state,
the fleet repo, sibling lanes, the lane's git index and jj state are untouched: no `git add/commit/
stash/checkout/reset/pull/push`, no jj mutation, no fixture repository created (all four attacks edit
`SKILL.md` text only, so no `mktemp` git repo was needed). `git -C <lane> status --porcelain` shows 21
pre-existing untracked entries (other seats' `.ufo/waves/round-40/scratch/` left-overs), none created
here; this seat's scratch is 3.2 MB under `.scratch/r49-Mo49ExecK3K6K7/` after pruning the per-arm temp
trees (7.2 MB before; the typed receipts, the four attack texts, the five earlier-revision texts and the
falsifier's variant copies are kept).

---

## Findings

* **LOW — `.scratch/r49-Mo49ExecK3K6K7/mori-pin-check.py:146` (`SELF_INSTRUMENT`).** R13's obligation is
  keyed on the constant path `tools/mori-pin-check.py`. It fails open (no finding) if the lane ever
  renames or relocates the reconciler, and it cannot protect a *differently named* future reconciler. I
  chose the hardcoded path over content identity because the counter runs a copy at an opaque path
  against a tree that still holds the entering revision's bytes — content identity does not fire there
  (measured reasoning, not measured: the copy's sha256 differs from `tools/mori-pin-check.py@b3e3453d`).
* **LOW — `.scratch/r49-Mo49ExecK3K6K7/mori-pin-check.py:638` (R14 scope).** R14 ties line counts only.
  The **digest** pins have the same hole and I did not close it: measured at `b3e3453d`, row
  `r45 gate conformance (C2)` has a second full digest whose nearest path is
  `.ufo/waves/round-45/fixtures/mutants/count-c2.py`, and row `r45 corpus coverage (C3)` likewise
  (`…fixtures/mutants/count-c3.py`) — so a digest-only extension reds 2 pins in 2 landed rows unless it
  carries R11's `mutant_of` carve-out. Scope: class K7 as assigned is line-count only.
* **LOW — `.scratch/r49-Mo49ExecK3K6K7/mori-pin-check.py:482-508` (R12 semantics).** The presence
  counter counts *kinds per row*, so replacing a line-count pin with a different line-count pin, or a
  truncated digest with a different one, is not a deletion. This is the price of keeping the honest
  repair (`r12_trunc_digest_repaired_to_full`) green, and it is the exact boundary the critic drew.
* **LOW — `.scratch/r49-Mo49ExecK3K6K7/mori-pin-check.py:725-731` (K6 as a contract number).** The
  frozen floor (`--min-tally-pins 26`) is the baseline's tally total; five pins can still vanish from
  rows **new since the baseline** other than the reconciler's own row, and no tool-side rule can know a
  new row was expected. Landed-tip recommendation for the L1 (not a re-score, the counter is frozen):
  raise the counter's floor to the landed count (31) in a future round.
* **INFO — `.ufo/waves/round-49/w1/Mo49ExecK3K6K7.md` §4.** The counter's process exit status was not
  captured (piped to `tee`); the verdict line `C1=met … variants=26` is the observed receipt.
* **INFO — scope retained.** K1 (misattribution), K4 (pins outside the self-test cell), K5 (namespace
  join) and defect X1 (`PIN_CHECK_SETUP can only join an iterable`, `check`'s rebound formatter) are
  untouched by this seat and stay routed; my copy still carries X1's crash path verbatim (not exercised
  by any arm here).

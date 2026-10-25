# CritC1Predicate — falsification report, wave w1 (round 47)

Seat: CritC1Predicate (leaf, no subagents). Target: **P-C1** — attack the claim that
`python3 tools/mori-pin-check.py --rev R --min-tally-pins 26 --baseline-rev
2d85e33d14198d388fd3cda9cc15ec07e57e7a53` prints `PIN_CHECK=met` only when the SKILL.md
registry self-test pins honestly reproduce from committed bytes.

## Method

- Measured revision R = freeze `63eecf2738db96f46b0bd02b1b2dfd66787493d0`; baseline rev =
  entering `2d85e33d14198d388fd3cda9cc15ec07e57e7a53`.
- Instrument: **frozen** `tools/mori-pin-check.py` bytes (sha256
  `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1`, `git show
  63eecf27:tools/mori-pin-check.py`). Every measurement ran that copy with
  `--repo /home/vgpnk/Projects/shokunin/mori-shokunin`, `--rev 63eecf27`,
  `--min-tally-pins 26`, `--baseline-rev 2d85e33`, `--skill <scratch SKILL.md>`.
- Scratch (all writes): `.scratch/r47-CritC1Predicate/`; each SKILL.md variant generated from
  the committed freeze `SKILL.md` (`git show 63eecf27:SKILL.md`), one edit per variant.
- Full output per variant at `.scratch/r47-CritC1Predicate/out-v*.txt`.

### Environment anomaly (recorded, not caused by this seat)

Between my baseline run and the variant matrix, the **working-tree** `tools/mori-pin-check.py`
was mutated (line `bound = []` deleted from `pin_commands` → `NameError` on every run using the
working-tree file). All measurements below therefore use the frozen bytes (the contract's
rules: working-tree bytes diverged → measure `git show <freeze>:<path>`).

## Baseline at freeze (frozen instrument)

```
pin line=912 kind=tally prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=mismatch
  pinned='pass=15 fail=0' observed='pass=22 fail=0' rc=0
  cmd='python3 tools/mori-sources-appendonly.py 63eecf27… --selftest'
PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0
EXIT=1
```
Matches the contract’s “Before (entering)” shape: the single stale pin is the r38 row
(`SKILL.md` line 912), pinned `pass=15`, while the committed tool prints `pass=22 fail=0`.

## Junk-edit matrix (each: base freeze SKILL.md + one edit)

| # | Edit (one line, row “SOURCES append-only timing (r38)”) | Result (frozen tool) |
|---|---|---|
| v1 | pinned text `pass=15` → `pass=22` (honest fix, value matches committed tool) | **MET** (control) |
| v2 | self-test-cell span `` `--selftest` `` → `` `python3 .scratch/MutGateFirstParent/gate-v3-pristine.py --selftest` `` (pinned `pass=15` unchanged) | **MET — FALSE GREEN** |
| v3 | self-test-cell span → `` `python3 -c "import sys; print('MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0'); sys.exit(0)" --selftest` `` (pinned `pass=15` unchanged; no tool invoked — literal echo) | **MET — FALSE GREEN** |
| v4 | pinned text `pass=15 fail=0` → `pass=22` (drops `fail=0` conjunct; value truthful) | MET (weakened pin — no exit-code check applies) |
| v5 | pin prefix renamed to `MORI_SOURCES_APPENDONLY_SELFTEST_V2` | unmet, `mismatches=1` (prefix regex absorbs `_V2` into pinned rest) |
| v6 | row deleted | unmet, `dropped=1`, `tally_pins=25` (baseline-key guard holds) |
| v7 | **entry** cell → `` `python3 .scratch/MutGateFirstParent/gate-v3-pristine.py <rev> --round-base REV` ``, self-test cell untouched (bare `` `--selftest` `` → derived command now runs the old copy; pinned `pass=15` unchanged) | **MET — FALSE GREEN** |
| v8 | hide original pin (row made unparsed; pin token lowercased to `selftest` so the row carries no `SELFTEST` and is silently skipped) + insert a well-formed duplicate row with the **same row name and same prefix**, bound to the inline echo | **MET — FALSE GREEN** |

### v8 receipt (abridged)

`pin line=913 kind=tally prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=match pinned='pass=15 fail=0'
observed='pass=15 fail=0' rc=0 cmd="python3 -c import sys; print('MORI_SOURCES_APPENDONLY_SELFTEST
pass=15 fail=0'); sys.exit(0) --selftest"` → `PIN_CHECK=met tally_pins=26 digest_pins=5
mismatches=0 unparsed=0 no_command=0 dropped=0` (EXIT=0). The stale `pass=15` claim is never
corrected and the current tool is never invoked; the baseline-key guard stays satisfied because
the duplicate row re-adds the same `(row name, prefix)` key.

### False-green receipts (abridged)

v2: `cmd='python3 .scratch/MutGateFirstParent/gate-v3-pristine.py --selftest'`, `observed='pass=15 fail=0'`, `rc=0`, `PIN_CHECK=met … mismatches=0 … dropped=0`.
v3: `cmd="python3 -c import sys; print('MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0'); sys.exit(0) --selftest"`, `observed='pass=15 fail=0'`, `rc=0`, `PIN_CHECK=met … mismatches=0 … dropped=0`.
v7: `cmd='python3 .scratch/MutGateFirstParent/gate-v3-pristine.py 63eecf27… --selftest'`, `observed='pass=15 fail=0'`, `rc=0`, `PIN_CHECK=met … mismatches=0 … dropped=0`.

### Why these evade the counters

- `pin_commands` binds each tally pin to the **nearest preceding executable span** in the
  self-test cell: any span containing `--selftest` starting with an interpreter, or any bare
  `.py`/`.sh` path, qualifies. The `` `--selftest` `` span falls back to the entry cell, but an
  explicit span replaces it wholesale — so a junk span can name **any committed file** (v2/v7)
  or even **inline Python code** (v3, `python3 -c …`).
- `drop` accounting keys on `(row name, pin prefix)` only. All false greens (v2/v3/v7/v8) keep the
  row name and prefix byte-identical, so `dropped=0`; the pinned text is untouched, so the
  “stale” `pass=15` claim is never corrected — it is merely re-bound to a command that prints
  it.
- v8 additionally shows the stale row itself can be **hidden without penalty**: converting it to
  an unparsed row that carries no uppercase `SELFTEST` token makes `parse_registry` skip it
  silently (no `unparsed` increment, no pin), while a duplicate row re-adds the same key so the
  baseline guard sees `gone=0`.

- v2/v7 exploit that **committed bytes** include an obsolete self of the same appendonly tool:
  `.scratch/MutGateFirstParent/gate-v3-pristine.py` (revision `d72ac167`, round-41 freeze)
  prints `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0`, exit 0. The counter measures
  “committed bytes of whatever command the row names” — it cannot tell current tool from
  historical snapshot, and `.scratch/` is not excluded.
- v3 needs **no file at all**: a literal `print` in SKILL.md satisfies the pin. The check
  executes shell words without a whitelist; `python3 -c` is accepted as an interpreter command.

## Smallest safe correction (recommended to the L1/canonical judge)

1. **Bind only to commands derived from the row’s entry cell**, never from arbitrary spans:
   drop the “nearest preceding executable span” scan (or restrict it to a bare
   `` `--selftest` `` fallback) and always execute the entry-cell-derived command.
2. **Exclude `.scratch/` and non-`tools/`/`.ufo/waves/…` paths** from executable spans/commands
   (v2/v7 pass because `.scratch/MutGateFirstParent/gate-v3-pristine.py` is a committed,
   runnable `.py`).
3. **Reject interpreter commands except a fixed allow-list** (`python3 <path> --selftest`,
   `bash <path> --selftest`; no `-c`, no inline code, no extra argv) — kills v3 without
   breaking any real row (all 26 current pins use a bare path or entry-derived command).
4. **Require want == observed (exact tail match)**, and require the `fail=0` conjunct whenever
   the observed tail carries it — closes v4’s weakened-pin green.
5. **Digest-side** is fine (v6 shows the baseline-key guard works for deletion/rename).
6. **Count unparsed rows case-insensitively**: treat any row whose raw text matches
   `selftest` (any case) as unparsed when its cell count differs — v8’s hide relies on
   lowercasing the token to `selftest` so the uppercase scan misses it.

## Impacted axes

- **calibration** (C1’s own axis): the claim as written is satisfiable by edits that change
  nothing measured — the false greens land with `mismatches=0, unparsed=0, no_command=0,
  dropped=0` and `tally_pins=26` unchanged, i.e. *exactly* the target line.
- Adjacent (not re-scored): the same binding hole would let any self-test cell rebind to any
  committed runnable file, affecting all registry rows (operability/depth surfaces), but no
  other claim is scored here.

## Evidence

- Full outputs: `.scratch/r47-CritC1Predicate/out-v0-frozen.txt` … `out-v8.txt` (frozen
  instrument, `PIN_CHECK=` final line + per-pin lines).
- Variant SKILL.md files: `.scratch/r47-CritC1Predicate/skill-v*.md`.
- Tool copy used: `.scratch/r47-CritC1Predicate/pin-check-frozen.py` (sha256
  `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1`).
- Old-copy printer: `.scratch/MutGateFirstParent/gate-v3-pristine.py` (committed at
  `63eecf27`) prints `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0`, exit 0 (run directly,
  `EXIT=0`).

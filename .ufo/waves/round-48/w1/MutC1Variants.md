# MutC1Variants — mutation-testing v2 against the C1 counter (round 48, wave w1)

Seat: leaf mutation-tester. Question assigned: if a v3 author accidentally weakens one of
v2's own rules, would `count-c1.py --rev e5dbac05…` notice — i.e. does any of the 13
counter runs (J1-J8, H1-H4, real) change its verdict? Method: six single-point weakenings
of v2, each proven live against v2's own `--selftest`, then each run through the frozen
counter. All scratch under `.scratch/r48-MutC1Variants/`; `tools/mori-pin-check.py` was
never modified (hash evidence below).

## Baseline (pristine bytes)

`pristine-v2.py` is a byte-identical copy of `tools/mori-pin-check.py` at the entering tip
(sha256 `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6`, equal to the
freeze manifest's `controls/tool-v2-entering.py` and `tools/mori-pin-check.py` rows).

Command (every run, only `--tool`/`--scratch`/log name varying):

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin && TMPDIR=$S python3 .ufo/waves/round-48/count-c1.py \
  --tool $S/<tool>.py --rev e5dbac05459887d9597ea5d1da0d8e3d024e0d17 --scratch $S/c1-<name> --jobs 4
```

(`$S` = `.scratch/r48-MutC1Variants`; `--jobs 4` is the counter default; ≤3 counter runs
concurrent, per-run wall time 301-355 s. Full logs: `.scratch/r48-MutC1Variants/out-*.txt`.)

Pristine result — reproduces the frozen receipt
`evidence/control-c1-tool-v2-entering.txt` line for line:

```
variant name=J1 expect=unmet got=met rc=0      variant name=H1 expect=met got=met rc=0
variant name=J2 expect=unmet got=met rc=0      variant name=H2 expect=met got=met rc=0
variant name=J3 expect=unmet got=met rc=0      variant name=H3 expect=met got=met rc=0
variant name=J4 expect=unmet got=met rc=0      variant name=H4 expect=met got=met rc=0
variant name=J5 expect=unmet got=met rc=0      variant name=real expect=met got=met rc=0
variant name=J6 expect=unmet got=met rc=0
variant name=J7 expect=unmet got=met rc=0      C1=unmet junk_met=8 honest_unmet=0 \
variant name=J8 expect=unmet got=met rc=0        real=met errors=0 variants=12 rev=e5dbac05…   rc=1
```

So the reference got-map is: **J1-J8 = met, H1-H4 = met, real = met** (v2 is the
do-nothing control: green on all junk). A mutant "flips" a run iff its got-value differs
from this map.

## The six mutants

Each is one edit against the pristine copy; exact before/after in fenced blocks.

### mut1 — drop the `dropped` rule (baseline pin keys must persist)

```diff
     base_bind = {}
     if baseline_text is not None:
+        base_bind = pin_bindings(baseline_text, "<REV>")
-        now = pin_keys(text)
-        for k, n in sorted(pin_keys(baseline_text).items()):
-            gone = n - now.get(k, 0)
-            if gone > 0:
-                counts["dropped"] += gone
-                out.append("pin kind=baseline state=dropped row=%r pin=%s count=%d" % (k[0], k[1], gone))
-        base_bind = pin_bindings(baseline_text, "<REV>")
```

### mut2 — drop the `rebound` rule (baseline bound argv must not change)

```diff
             bkey = (cells[0], prefix, n)
             norm = None if words is None else tuple("<REV>" if w == rev else w for w in words)
-            if bkey in base_bind and base_bind[bkey] is not None and norm != base_bind[bkey]:
-                counts["rebound"] += 1
-                out.append("pin line=%d kind=tally prefix=%s state=rebound baseline_cmd=%r cmd=%r"
-                           % (line, prefix, " ".join(base_bind[bkey]),
-                              " ".join(norm) if norm else None))
             counts["tally_pins"] += 1
```

### mut3 — drop the `unparsed` rule (made non-fatal; single point: the `met` term)

```diff
-    met = (counts["mismatches"] == 0 and counts["unparsed"] == 0
+    met = (counts["mismatches"] == 0
            and counts["no_command"] == 0 and counts["dropped"] == 0
            and counts["rebound"] == 0 and counts["duplicate"] == 0
            and counts["tally_pins"] >= min_tally)
```

### mut4 — drop fence skipping (`parse_registry` reads fenced lines as ordinary lines)

```diff
     for n, line in enumerate(lines, 1):
-        mark = line.lstrip()[:3]
-        if mark in ("```", "~~~"):
-            fence = None if fence == mark else (fence or mark)
-            header = None
-            continue
-        if fence:
-            continue
         cells = split_cells(line)
```

### mut5 — relax exact pin-text match to `startswith`

v2's only exact-match rule is the pinned-text comparison (docstring: "the pinned text must
equal the observed text exactly"). The header-cell test is substring `in`, not equality,
so there is no exact match to relax there.

```diff
-            ok = observed is not None and observed.strip() == want
+            ok = observed is not None and observed.strip().startswith(want)
```

### mut6 — drop the duplicate-name rule

```diff
-    names = {}
-    for row in parse_registry(text):
-        if row["state"] == "ok":
-            names[row["cells"][0]] = names.get(row["cells"][0], 0) + 1
-    for name, n in sorted(names.items()):
-        if n > 1:
-            counts["duplicate"] += n - 1
-            out.append("pin kind=row state=duplicate row=%r count=%d" % (name, n))
     cache = {}
```

## Liveness: every mutant kills its own arm in v2's `--selftest`

`TMPDIR=$S python3 <tool>.py --selftest` (≤120 s each; pristine exits 0):

| tool | selftest | broken arms |
|---|---|---|
| pristine-v2 | `PIN_CHECK_SELFTEST pass=34 fail=0`, rc 0 | — |
| mut1-nodropped | `pass=33 fail=1`, rc 1 | `baseline_row_deleted` |
| mut2-norebound | `pass=32 fail=2`, rc 1 | `v2_rebound_to_other_tool`, `v2_entry_rebound` |
| mut3-nounparsed | `pass=32 fail=2`, rc 1 | `malformed_row`, `digitless_pin` |
| mut4-nofence | `pass=33 fail=1`, rc 1 | `v2_fenced_example_not_counted` |
| mut5-startswith | `pass=32 fail=2`, rc 1 | `token_boundary_truncated_pin`, `v2_weakened_pin_exact` |
| mut6-noduplicate | `pass=33 fail=1`, rc 1 | `v2_duplicate_name` |

No mutant is a no-op edit: each changes v2's behavior on the synthetic tree its own arm
builds. (mut4's arm is a fenced *complete* table — header + separator + row inside the
fence — the one shape where fence skipping is load-bearing.)

## Counter results: all six mutants survive; zero flips

Every mutant printed, on all 13 runs, exactly the pristine got-map:

```
C1=unmet junk_met=8 honest_unmet=0 real=met errors=0 variants=12 rev=e5dbac05459887d9597ea5d1da0d8e3d024e0d17   rc=1
```

| mutant | junk_met | honest_unmet | real | errors | flips vs pristine | verdict |
|---|---|---|---|---|---|---|
| pristine-v2 (baseline) | 8 | 0 | met | 0 | — | baseline (matches frozen receipt) |
| mut1-nodropped | 8 | 0 | met | 0 | none | **survived** |
| mut2-norebound | 8 | 0 | met | 0 | none | **survived** |
| mut3-nounparsed | 8 | 0 | met | 0 | none | **survived** |
| mut4-nofence | 8 | 0 | met | 0 | none | **survived** |
| mut5-startswith | 8 | 0 | met | 0 | none | **survived** |
| mut6-noduplicate | 8 | 0 | met | 0 | none | **survived** |

Baseline succeeded (pristine reproduces the frozen receipt), so these are true
survivors, not inconclusive. A surviving mutant is a coverage finding about the counter's
variant set; it is not a defect in v2 and not permission to change the contract.

## Why nothing flips — the structural reason

v2 is green on all 12 variants and on the real registry, so **no v2 rule ever fires
fatally on any of the 13 counter inputs**. Removing a rule that never fires cannot change
any run: mut1, mut2, mut3, mut5, mut6 are provably inert on this input set. mut4 is the
only weakening that could in principle have flipped something (it makes the parser see
more), and it is inert here for two grounded reasons:

- SKILL.md at `e5dbac05` contains **zero fenced blocks** (`grep -c '```'` on
  `git show e5dbac05…:SKILL.md` = 0), so the real/honest runs have no fence content to
  mis-parse.
- J5's fenced rows stay invisible even without fence tracking: the inserted
  ` ```markdown ` line is a non-table line, and `parse_registry` resets `header = None`
  on any non-table line, so the two fenced data rows that follow are skipped with or
  without the fence flag. Only a fenced block containing a *complete* table (header +
  separator + rows) would differ — exactly v2's `v2_fenced_example_not_counted`
  selftest arm, and exactly what SKILL.md at R does not contain.

Per-variant mapping (why each junk class is invisible to v2, hence unweakenable by these
mutants):

| variant | v2's reason for green | v2 rules it touches |
|---|---|---|
| J1 (header `selftest` + corrupt pins) | header cell no longer matches `"self-test" in low` → whole table unparsed, corrupt pins never measured | header recognition (acceptance side only) |
| J2/J3 (fullwidth / Cyrillic prefix) | rows are well-formed (8 cells); prefix regex `[A-Z][A-Z0-9_]*SELFTEST` is ASCII, so no pin is bound | none fire |
| J4 (archived-copy rebinding) | row parses; `argv_ok`/`SAFE_PATH` *accepts* `.ufo/waves/round-40/…`; archived instrument runs, `pass=12` matches | binding + argv acceptance; v2 has no baseline prefix-set rule (v3 R4) |
| J5 (fenced corrupt pins) | fence + header-reset make the rows invisible | fence skipping (see mut4: not load-bearing here) |
| J6 (blank line hides rows) | blank line resets `header = None` → rows skipped | header-reset-on-blank |
| J7 (line count off by one) | v2 has no line-count rule (v3 R5) | none |
| J8 (truncated digest) | digest rule matches only full 64-hex (`HEX_RE`); `37fd7c24ff52…` is 12 hex + U+2026 → not a digest pin (v3 R6) | none |
| H1-H4, real | nothing fatal fires; ≥26-pin floor still satisfied | run path + floor (acceptance side) |

## Coverage finding: v2 rules no variant exercises

The counter's honest/junk set would notice an accidental regression of **none** of v2's
own rules. Concretely, no variant exercises — in the fatal direction — these v2 rules:

1. `dropped` (baseline pin keys must persist) — no variant deletes a pin that exists at
   baseline `2d85e33d`; the round-47 gate rows J1/J5/J6 corrupt do not exist at the
   baseline (verified: `git show 2d85e33d…:SKILL.md` has 21 `SELFTEST pass=` pins vs 23
   at entering, and its only `C2_SELFTEST`/`PIN_CHECK_SELFTEST` matches are cell text of
   r44/r45 rows).
2. `rebound` (baseline bound argv must not change) — no variant rebinds a baseline row's
   command; J4 adds a *new* row, which the baseline comparison exempts by design.
3. duplicate-name — no variant creates two parsed rows with one first-cell name (H4's new
   row is named `C2_SELFTEST`; no existing row's name cell is that string).
4. exact pin-text equality, `fail=0`→rc-0 coupling, tally lines must *start* with the
   prefix, single distinct tail — no variant alters a pin that v2 actually measures (the
   corrupted pins of J1/J5/J6 sit in rows v2 never parses).
5. `argv_ok` rejection sub-checks (inline `-c`, `.scratch/` path, `..`, trailing
   arguments) — no variant adds a row exercising them; J4's archived path is one v2
   *accepts*.
6. digest-path containment (`../outside.py` style) — no variant uses a digest pin whose
   path escapes the tree.
7. digit-after-prefix (`unparsed` pin-level) and row-shape `unparsed` (cell-count
   mismatch naming `selftest`) — no variant adds such a row.

The only v2 behaviors the variant set leans on are header recognition (J1), the
header-reset invisibility path (J5, J6), and the general run path with the ≥26 floor
(all runs). Directionally: the counter detects a regression that makes v2 **stricter
wrongly** (an honest run going unmet, or `real=unmet`), but is blind to a regression that
makes v2 **looser** — which is precisely what the eight junk classes attack in v3.

## Consequence for v3 (observation, not a change)

v3-spec R8 already requires "every new arm is killed by the mutation that removes its
rule". Today the only detector that notices any of these six regressions is the tool's
own `--selftest` (each mutant killed exactly its arm above); the frozen C1 counter cannot
distinguish any of them from pristine v2. If wave 2 wants a counter-side guard against
accidental v3 rule regressions, the gap is the same shape as this probe: variants that
exercise each rule fatally (a deleted baseline pin, a rebound command, a duplicate name,
a weakened pin text, a fenced complete table) would close it — but that is a contract
change and belongs to the L1, not to this seat.

## Restoration evidence

- `tools/mori-pin-check.py` sha256 before first copy and after all runs:
  `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6` — identical to the
  freeze manifest row; the production tool was never edited (mutants are scratch copies).
- Frozen bytes untouched, verified against `evidence/freeze-sha256.txt`:
  `count-c1.py` `7a2a6aa0…`, `contract.md` `052a2bf9…`, `v3-spec.md` `f93ef57f…` — all
  equal to their manifest rows.
- Mutant sha256 (for reproduction): mut1 `878c2fb3…`, mut2 `3c44f1b9…`, mut3 `77019e84…`,
  mut4 `47d5c099…`, mut5 `0b28168b…`, mut6 `5af4c453…`; pristine copy `9832e38c…`.
- All writes were under `.scratch/r48-MutC1Variants/` and this report. No git/jj mutating
  command was run; no pacman transaction; no tools installed (none needed). Every
  lane-tool invocation set `TMPDIR` to the seat scratch. No credential or private-URL
  material in this report.

## UNVERIFIED

- Nothing in the assigned probe. All six counter runs and the pristine baseline completed
  with observed output and exit codes (rc=1 each, matching `C1=unmet`); wall times are
  from the job runner. The counter's internal `--jobs 4` scheduling order varies run to
  run, but the printed verdict lines are deterministic in content.

# Mo57Scribe50 — C1 counter attack: junk rows reach `C1=met`

Seat: Mo57Scribe50 (scribe/attack seat, leaf, no dispatch). Round 57 wave 1, L1 `MoriR57`.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Entering revision `53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2`, freeze `618562c72a03dc4d17386b715357f863fd327274`.
Mode: detection/report only. No product, counter, contract, or lane mutations; no commits, no jj.

## Axes named

1. **Bypass leverage** — fewest junk bytes that flip the counter to `C1=met` / exit 0.
2. **Predicate fidelity** — does the counter decide what the frozen C1 predicate says, column by column?
3. **Evidence sufficiency** — is the named round-56 pointer ever resolved?
4. **False-negative symmetry** — does genuine work placed in the live register satisfy the counter?

Any variant was kept only if it raised one axis without weakening another. All four moved.

## Provenance (what was actually read and run)

- `.ufo/waves/round-57/contract.md:9` — C1 predicate: "two rows naming `driver-liveness` and `vote-binding`, each with a **resolvable** round-56 evidence pointer and first-working round 56. Before: 0 matching rows; after: 2 matching rows."
- `.ufo/waves/round-57/count-c1.py` (14 lines, `sha256 7156fb4bb29f27881091b22dfa7ef3d661b1e955a1ec9a4d13e48013f1b368ec`):
  - `:6` `repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"`
  - `:7` the *only* I/O: `git -C repo show f"{R}:SCORECARD.md"` — no `open`, no `os.path.exists`, no read of any evidence file.
  - `:10` `s = p.stdout.split("## Capabilities", 1)[1].split("## Saturation", 1)[0]`
  - `:11` `rows = [line for line in s.splitlines() if line.startswith("|") and ("driver-liveness" in line or "vote-binding" in line)]`
  - `:12` `ok = len(rows) == 2 and all(".ufo/waves/round-56/" in x and "| 56 |" in x for x in rows)`
- `.ufo/waves/round-57/controls.txt` — entering-tip control, reproduced verbatim below by my harness.
- `git -C … show 53e2b47…:SCORECARD.md` — header census: `## Capabilities` at **596** and **1951**; `## Capabilities (round 12 demonstrations)` at 637; first `## Saturation` at **604**.
  The counter's window (`:10`) is therefore **lines 596–603 only**: the stub table `| — none yet — | | | |`, which the file itself declares superseded (line ~660: "left as filed at `d677cf3`"). The live register at 1951 is outside the window.

### Harness fidelity

Fixture runs use a copy of the counter with **one** substitution — the `repo` constant at `:6` parameterised — logic bytes unchanged. Proof `diff -u` against the lane counter after restoring the lane path: identical, no hunks. Parity control: that copy pointed back at the real lane at the entering revision prints

```
C1=unmet rows=0 evidence=bad rev=53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
```

exit 1 — byte-for-byte the `controls.txt` control. So every `met` below is a property of the counter logic, not of the harness. All fixtures are throwaway repos under scratch, driven with explicit `git -C <fixture>`.

## Findings

Expected output for every bypass below: `C1=met rows=2 evidence=ok rev=<fixture-rev>`, exit **0**.

### F1 — 101-byte do-nothing file reaches the target

`SCORECARD.md`, 101 bytes, `sha256 827ec443e0038b7fdb4a5eb0a576d59679386ee3ad34d597deb6146d10c909a6`, commit `579bfc9d3f757e23e3bc5f58f5fe85f48712a0a4`:

```
## Capabilities\n
|driver-liveness|.ufo/waves/round-56/| 56 |\n
|vote-binding|.ufo/waves/round-56/| 56 |\n
```

(exactly three lines; `\n` shown as escapes; no `## Saturation`, no table header, no separator row, no prose.)
No `.ufo/waves/round-56/` directory and no evidence file exists anywhere in that repo (`find` → 0 entries).
Run: `C1=met rows=2 evidence=ok rev=579bfc9d3f757e23e3bc5f58f5fe85f48712a0a4`, exit 0.

Two rows of 44 and 41 bytes are the minimum: `|` + name + `|` + `.ufo/waves/round-56/` (21 B) + `| 56 |`. The counter never requires the four-column header, the separator, a claim sentence, or a file.

### F2 — junk rows inside the superseded stub table, on the real file's bytes

Entering `SCORECARD.md` plus a **two-line, 123-byte** insertion after line 599 (`599a600,601`, nothing else changed), commit `fab4026a495aabc9236bc13c46fb94beb327dbdf`:

```
| driver-liveness | x | .ufo/waves/round-56/missing.log | 56 |
| vote-binding | x | .ufo/waves/round-56/missing.log | 56 |
```

`missing.log` does not exist (repo contains only `SCORECARD.md` and `.git`). Run: `C1=met rows=2 evidence=ok`, exit 0.
This is the load-bearing bypass: the junk lands in the stub table at 596–603 that the counter actually reads, while `| — none yet — | | | |` stays on line 602 beside it.

### F3 / G1 — genuine rows in the live register do **not** reach the target

G1: entering `SCORECARD.md` plus two *genuine, resolvable* rows appended to the real register (lines 1989–1991), commit `d6b7bce411d8e50fb8c886fc4b3259d879781fec`:

```
| `rounds[9].capabilities_added[0]` | driver-liveness | Demonstrated live on the round-56 driver. | `.ufo/waves/round-56/driver-liveness.log` | 56 |
| `rounds[9].capabilities_added[1]` | vote-binding | Demonstrated live on the round-56 vote bind. | `.ufo/waves/round-56/vote-binding.log` | 56 |
```

with both evidence files present and non-empty. Run: `C1=unmet rows=0 evidence=bad`, exit **1**.
Same in a synthetic minimal repo (commit `5eb4e76a438f65fe46ab47c19d7c5c580992441d`): `C1=unmet rows=0`.
Cause is `:10` alone — everything after the first `## Saturation` (604) is discarded, so rows 1951+ are invisible. The failure mode is asymmetric: correct work scores as absent, junk inside the stub scores as present.

### F4 — rows that deny the capability still pass

```
| driver-liveness | NOT demonstrated this round; no run log exists | .ufo/waves/round-56/ no such file | 56 |
| vote-binding | NOT demonstrated this round; no run log exists | .ufo/waves/round-56/ no such file | 56 |
```

commit `0003015477c450236fd6438adb31e65636b4a8d8` → `C1=met rows=2`, exit 0. No polarity check exists; `:11`–`:12` are pure substring tests.

### F5 — columns unbound; `| 56 |` and the pointer may sit anywhere

```
| 56 | .ufo/waves/round-56/ | driver-liveness |
| 56 | .ufo/waves/round-56/ | vote-binding |
```

commit `23e754093f8f1034618e3b6cffa889c25ab3bd79` → `C1=met`, exit 0. "First-working round 56" is satisfied by any cell holding `| 56 |`, and the pointer by any cell holding the directory prefix.

### F6 — exact-count brittleness: two genuine + one stale row = unmet

```
| driver-liveness | .ufo/waves/round-56/ | 56 |
| vote-binding | .ufo/waves/round-56/ | 56 |
| vote-binding (superseded) | .ufo/waves/round-56/ | 56 |
```

commit `8431e1b6da15d6042c160cde03b8658f9a483999` → `C1=unmet rows=3 evidence=bad`, exit 1. `len(rows) == 2` (`:12`) is equality on a substring-filtered count, so an unrelated historical row, or a duplicated one, blocks a correct landing.

### F7 — duplicates satisfy "two rows"

```
| driver-liveness | .ufo/waves/round-56/ | 56 |
| driver-liveness again | .ufo/waves/round-56/ | 56 |
```

commit `21874f54a677a16238499aa41d6796335a1cd583` → `C1=met`, exit 0, although no row names `vote-binding`. The predicate needs one row per capability; the counter needs two rows matching either name.

### F8 — leading space silently drops rows

` | driver-liveness | …` (one leading space, otherwise well-formed) → `C1=unmet rows=0`, exit 1. `line.startswith("|")` (`:11`) is the only structural test, so indentation, not content, decides.

### F9 — substring names pass

```
| driver-liveness-NOT-YET | .ufo/waves/round-56/ | 56 |
| vote-binding-pending | .ufo/waves/round-56/ | 56 |
```

commit `62854ca36eead34f21ca67f0a100e6126689f713` → `C1=met rows=2 evidence=ok`, exit 0. Rows labelled *not yet* and *pending* are accepted because `:11` uses `in`, not cell equality.

## Predicate vs counter

| Predicate clause (`contract.md:9`) | Counter test | Gap |
|---|---|---|
| two rows naming `driver-liveness` **and** `vote-binding` | `:11` substring-OR, `len == 2` | duplicates pass (F7); substring names pass (F9); prefix space drops rows (F8); exact count blocks correct rows (F6) |
| **resolvable** evidence pointer | `:12` `".ufo/waves/round-56/" in line` | never resolved — no file/dir existence check anywhere (F1, F2, F4) |
| evidence **pointer** (i.e. the pointer column) | `:12` any cell | column order free (F5) |
| first-working round **56** | `:12` `"\| 56 \|" in line` | any column; free text may carry it (F5) |
| "two rows" of the **current** capabilities table | `:10` first `## Capabilities` → first `## Saturation` | reads the superseded stub table (596–603), never the live register (1951+) — F2 passes, G1 fails |

## Verdict

**C1 counter is attackable at the stated target.** A 101-byte file of two unadorned rows with no evidence on disk yields `C1=met rows=2 evidence=ok`, exit 0; on the real `SCORECARD.md` bytes, a 123-byte two-line insertion into the superseded stub table does the same, while genuine rows placed in the live register yield `C1=unmet rows=0`, exit 1. The counter therefore does not decide the frozen predicate: it decides "two `|`-initial lines containing one of two names, the directory string `.ufo/waves/round-56/`, and `| 56 |`, inside a window bounded by the wrong headers". Reported, not remediated — counter and contract were not touched.

## Touched surfaces

- Written: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-57/w1/Mo57Scribe50.md` (this report).
- Read only: `contract.md`, `controls.txt`, `count-c1.py`, `SCORECARD.md` via `git show`.
- Scratch (throwaway, under `/fast/scratch/hyaku/mori-r57/Mo57Scribe50/`): counter copy with `repo` parameterised, fixture driver scripts, ten throwaway git repos. Nothing written outside that tree, the report path, and lane reads.

## Limits / out of scope

- C2, the journal, capsule and gate seats were not examined; only the C1 counter and the `SCORECARD.md` capabilities surface.
- No claim about which rows the round-56 executor will actually land; the G1 result is a fixture property of the counter, not a prediction of the wave outcome.
- The parity control runs the *copy*; the lane counter itself was not executed here beyond the control recorded in `controls.txt` (which the copy reproduces exactly).
- No tool was installed or updated; no pacman call; no `/tmp` artifact used or cited.

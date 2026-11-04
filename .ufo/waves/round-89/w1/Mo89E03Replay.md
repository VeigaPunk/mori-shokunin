# Mo89E03Replay — round-89 w1 seat report (C1 replay, operability)

Seat: `Mo89E03Replay`. Lane: mori. Scope: independently replay the C1 frozen counter at the
entering revision and the C1 landing revision; independently hand-construct the equiv /
comment / selfprint fixture commits in a scratch shared clone; run the exported r87 gate
public CLI against each; enumerate the seven receipt headers/modes and their limits.

No edits to production checkout, corpus, predicates, instruments, or the gate. Scratch only
under `/fast/scratch/hyaku/mori-r89/Mo89E03Replay/`.

## Frozen inputs

- Entering rev `R0 = 30a29797012281b9fd0c748b38b929ac67f8c754` (lane master tip before C1).
- Landing rev `R1 = 760428abf925d98025b34bf23f2cbf54cbeb3bca` (C1 already measured met).
- Counter: `.ufo/waves/round-89/count-c1.py`, run as `python3 -I <abs path> <rev> --repo <clone> --scratch <dir>`.
- Gate subject: `.ufo/waves/round-87/count-c2.py`
  - at R0 sha256(blob text) = `7e577f533e1dac676d3f5b3d601f2c4c622c57c325e6091e6018b5781ae73fc0`
  - at R1 sha256(blob text) = `d7ea961a9ede1cefc615e0308c51ac99bc2a187cdf225aade0abd97bb03f6a13`
  - exported copies kept at scratch `gate-before.py` / `gate-after.py` (same digests).
- Base receipt `.ufo/waves/round-87/evidence/record-sweep-r87.txt` sha256 =
  `213a7558e155ea4eaeec8472767fa8371b44948e40b59cf9ac8437954641f4ac` (identical at R0 and R1).

## Commands run (exact)

Repo for `--repo`: one `git clone --shared` of the lane into
`/fast/scratch/hyaku/mori-r89/Mo89E03Replay/lane-clone` (HEAD = R1 = 760428ab…; both R0 and
R1 verified with `git rev-parse --verify <rev>^{commit}` before use). `TMPDIR`,
`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `PYTHONDONTWRITEBYTECODE=1`.

1. Frozen counter at entering rev:
   `python3 -I …/round-89/count-c1.py 30a29797012281b9fd0c748b38b929ac67f8c754 --repo <lane-clone> --scratch …/scratch-enter`
   → rc **1**, exact output:

   ```
   REAL rc=0 C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=30a297970122
   FX equiv refused problems=cmd-binding
   FX comment refused problems=-
   FX selfprint refused problems=-
   C1=unmet equiv=refused comment=accepted selfprint=accepted real=met arms=23 subject=arms:(23, 0) rev=30a297970122
   C2_COUNTER_SELFTEST pass=23 fail=0
   ```

   Matches the contract's entering line `C1=unmet equiv=refused comment=accepted
   selfprint=accepted real=met arms=23` (modulo the appended `subject=`/`detector=` fields the
   counter itself prints; the frozen predicate substring is exact).

2. Frozen counter at landing rev:
   `python3 -I …/round-89/count-c1.py 760428abf925d98025b34bf23f2cbf54cbeb3bca --repo <lane-clone> --scratch …/scratch-after`
   → rc **0**, exact output:

   ```
   REAL rc=0 C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=760428abf925
   FX equiv accepted problems=-
   FX comment accepted problems=cmd-binding
   FX selfprint accepted problems=cmd-binding
   C1=met equiv=accepted comment=refused selfprint=refused real=met arms=26 rev=760428abf925
   ```

   The frozen `C1=met … arms=26` line is exact (again modulo the trailing `rev=` field).

3. Gate selftest at R1 bytes (`gate-after.py --selftest`): `C2_COUNTER_SELFTEST pass=26 fail=0`, rc 0 — all 26 PASS lines, including the three new round-89 arms `binding_path_identity`, `binding_comment_dropped`, `binding_selfprint_refused`.

## Independent fixture construction (no r89 helper used)

I did **not** call `count-c1.py`'s `clone_fixture`/`fixture_receipt`. I hand-built the three
receipt files by applying the contract's frozen `# cmd:` replacements to the base receipt
bytes (same `# cmd:` first-line-only replacement rule), committed each in its own
`git clone --shared` fixture, verified `git rev-parse --show-toplevel` = fixture dir before
each `git -C` mutation, and ran the **exported r87 gate** (`gate-after.py`, sha256
`d7ea961a…f6a13`) public CLI against each clone.

Fixture commits (parent = R1 `760428ab…`, file = `.ufo/waves/round-87/evidence/record-sweep-r87.txt`):

| kind | fixture rev | fixture `# cmd:` (verbatim) |
|---|---|---|
| equiv | `ace556d6fe5f5fa43a21e2ec738fe3f197a75aeb` | `python3 -I ./tools/mori-record-sweep.py --root . --pins .ufo/waves/round-82/record-pins.json` |
| comment | `e807af182a51e9f83c927cb7c380f4db5d46078f` | `printf '%s\n' 'RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=3 revisions=0' # tools/mori-record-sweep.py` |
| selfprint | `cdab7468d8daea7cc8914e2621c42caf2893a7da` | `python3 -c "print('RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=3 revisions=0')" tools/mori-record-sweep.py` |

Gate public CLI per clone: `python3 -I gate-after.py <fixture-rev> --repo <fixture-clone> --scratch <dir>`.
Full output saved at scratch `independent-run.txt` (sha256 `2b2e38c4…79f7c2c`); durable copy
at `/fast/scratch/hyaku/mori-r89/Mo89E03Replay/evidence/independent-run.txt`.

Results — **all three match the frozen C1 fixture expectations**:

- **equiv**: `RECEIPT record-sweep-r87.txt expect=met met problems=-`,
  `REPLAY record-sweep-r87.txt mode=clone rc=0 exported=1`, overall `C2=met … rev=ace556d6fe5f`,
  rc **0** → accepted. ✔
- **comment**: `REPLAY record-sweep-r87.txt mode=clone rc=0 exported=1` (the printf ran and
  printed the exact body, so replay-mismatch did **not** fire), but
  `RECEIPT record-sweep-r87.txt expect=met failed problems=cmd-binding`, overall
  `C2=unmet … matched=5 … unexpected=1`, rc **1** → refused with `cmd-binding`. ✔
  This is the key operability repair: the receipt *executes* correctly yet is refused purely
  on binding grounds — exactly the D2 fix.
- **selfprint**: `REPLAY record-sweep-r87.txt mode=clone rc=0 exported=1` (python `-c`
  printed the body; `tools/mori-record-sweep.py` sits in argv as data, `bash -c` ignores
  trailing args), `RECEIPT … failed problems=cmd-binding`, overall `C2=unmet`, rc **1** →
  refused with `cmd-binding`. ✔

Supplementary probe (own construction, outside the frozen three): a receipt whose `# cmd:`
was `python3 -I /abs/does/not/exist.py tools/mori-record-sweep.py` produced
`problems=cmd-binding,replay-rc:2,replay-mismatch` — i.e. a bound path passed as *data*
after a real interpreter still fails binding even when replay also fails. Confirms
`cmd-binding` is about script position, not mere token presence.

## Seven-receipt population enumeration (headers/modes/limits at R1)

Population (`SUBJECT` rows of the r87 gate), all present at R1; modes and binding counts:

| # | receipt path | `# replay:` | `# cmd:` shape | bindings (`# counter-sha256:`) | `# supersedes:` |
|---|---|---|---|---|---|
| 1 | `.ufo/waves/round-85/evidence/after-r85.txt` | none (legacy) | `python3 -I count-c1.py <rev>; python3 -I count-c3.py <rev>` (two `;` invocations) | 3 (c1,c2,c3 counters) | — |
| 2 | `.ufo/waves/round-85/evidence/record-sweep-r85.txt` | none (legacy) | `python3 -I tools/mori-record-sweep.py --root . --pins …` | 1 | — |
| 3 | `.ufo/waves/round-85/evidence/claim-sweep-r85.txt` | none (legacy) | `python3 -I tools/mori-claim-sweep.py --root . --pins …` | 1 | — |
| 4 | `.ufo/waves/round-86/evidence/after-c1-r86.txt` | `required` | `python3 -I .ufo/waves/round-86/count-c1.py <rev> --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch .` | 1 | — |
| 5 | `.ufo/waves/round-86/evidence/replay-defeat-r86.txt` | `required` | same cmd as #4 | 1 | — |
| 6 | `.ufo/waves/round-87/evidence/record-sweep-r87.txt` | `clone` | `python3 -I tools/mori-record-sweep.py --root . --pins …` | 1 | `record-sweep-r85.txt` |
| 7 | `.ufo/waves/round-87/evidence/claim-sweep-r87.txt` | `clone` | `python3 -I tools/mori-claim-sweep.py --root . --pins …` | 1 | `claim-sweep-r85.txt` |

Totals: receipts=7, bindings=9, replay-mode rows=4 (two `required` + two `clone`), legacy=3.
Every receipt carries a `# limits:` line (the `limits=7` counter). `# rev:` on all seven is
`25a74d4c…` (r85/r87) or `87644619…` (r86); both are ancestors of R1.

### Limits — host-local `--repo` paths (hermeticity NOT asserted)

Two receipts embed an absolute host path in `# cmd:`:

- `#4 after-c1-r86.txt` and `#5 replay-defeat-r86.txt` both carry
  `--repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch .`.

Consequences observed this round:

- When the gate replays these `required` receipts inside a fixture clone, `bash -c` runs the
  embedded `--repo /home/vgpnk/Projects/shokunin/mori-shokunin` — i.e. the **production
  checkout**, not the fixture clone. On this host that path exists, so replay ran (rc=0)
  and produced `replay-mismatch` for the `reject`-expected defeat receipt as designed.
- On a host where that absolute path does not exist, the same replay would fail differently
  (counter rc≠0 → `replay-rc:` problems). The gate therefore **depends on a host-local
  absolute path existing** for two of its seven population rows. This is a real,
  observable non-hermeticity in the population — reported as a limit, not asserted away.
  The r89 contract itself carries this forward (`F3 hermeticity … stays carried`, contract
  §Scope).
- The `clone`-mode rows (#6, #7) and the `required` rows are replayed against the
  `--repo`/`--scratch` the *gate* was invoked with for repo resolution (`git -C repo`),
  but the receipt's own embedded `--repo` overrides inside the replayed command — the
  asymmetry above is intrinsic to the frozen receipt bytes, not to this seat's method.

No other receipt embeds absolute paths; the r85 rows use only repo-relative tokens.

## Edge observations on the new binding rule (for L1 awareness; not defects of the claim)

Probed `binding_problems` semantics directly (pure function, no lane writes):

- `python3 -I -B tools/x.py` (two flags before script) → `cmd-binding` (script_position only
  allows index 1 bare or index 2 after one flag). A real `python3 -I -B script.py` invocation
  would be refused. Not exercised by the frozen population; noted as a boundary of the
  "index 2 when index 1 is a flag" rule.
- `python3.11 tools/x.py` → refused (`os.path.basename` must equal an INTERPRETERS entry
  exactly; `python3.11` is not listed).
- `/usr/bin/python3 tools/x.py` → accepted (basename match).
- `env python3 tools/x.py`, `uv run tools/x.py`, `sh -c '…'` → refused (interpreter must be
  tokens[0]).
- Absolute-path script token equal to the bound file (`/…/mori-shokunin/tools/mori-record-sweep.py`)
  → refused unless `realpath` matches; my probe used `/x` repo so realpath didn't match —
  with the real repo it *would* match via `os.path.realpath` join. Boundary: absolute tokens
  bind only through the realpath branch.
- `./tools/../tools/mori-record-sweep.py` → accepted (normpath collapses).

None of these change the frozen C1 verdict; they are the honest edge surface of the landed
rule for the record.

## Files changed

None in the lane repo's tracked tree. Two new files written under the assigned report dir:

- `.ufo/waves/round-89/w1/Mo89E03Replay.md` (this report)
- `.ufo/waves/round-89/w1/Mo89E03Replay-receipts.txt` (durable receipts: exact outputs, rc,
  revisions, blob/fixture digests, fixture commit ids)

Scratch (`/fast/scratch/hyaku/mori-r89/Mo89E03Replay/`) was emptied before yield: the
`--shared` clones, exported gate copies, fixture receipt files and per-run scratch dirs were
all removed after the runs; every needed byte is reproduced in the receipts file.

## Risks / blockers

- None blocking. C2 is explicitly out of this seat's scope (E01/E02 arms still in flight).
- The host-local `--repo` non-hermeticity above is reported, not remediated (detection only).

## Tooling

No installs or upgrades this round; nothing to record under the tooling directive.

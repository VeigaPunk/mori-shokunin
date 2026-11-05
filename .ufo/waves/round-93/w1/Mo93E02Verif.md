# Mo93E02Verif — round 93, wave w1: C1 calibration data repair (verified-at admission commits)

Seat: Mo93E02Verif (leaf, no subagent dispatched). Scope: contract section C1 only, the 12
entering-mismatch knowledge files. C2 (tools/ host paths) and the round-92 lesson correction are
other seats' work and are not touched here.

## Result

- Predicate P-C1 is met at the scratch commit `8b21c2bf2b43255d49e53dbdba181b65463a6056`
  (parent `6d82b8d7ef6d94a5527737f9242cdf04ad018da7`, scratch clone only; see "Commit note").
- Entering revision `7b3fe9d540c98b8b0390a0f9bbe78de4341092a5` reads unmet, matching the contract's
  "before" receipt.
- Diff scope: exactly 12 files, 12 insertions, 12 deletions. Each deleted and inserted line is the
  file's `verified-at:` line; no other line in any file changed.

## Evidence

### Counter (acceptance line, run once against the scratch commit)

Command: `python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-93/count-c1.py 8b21c2bf2b43255d49e53dbdba181b65463a6056 --repo /fast/scratch/hyaku/mori-r93/Mo93E02Verif/clone`
(with `TMPDIR=/fast/scratch/hyaku/mori-r93/Mo93E02Verif`)

Output, rc 0:

```
C1=met trio=98 claim_r92_true=1 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok rev=8b21c2bf2b43
```

Also run once in `--report` mode (raw values, exits 0 by `count-c1.py:159`):

```
C1_REPORT rev=8b21c2bf2b43 trio=98 claim_r92_true=1 files=19 adm_ok=19 adm_fail=0 patched12=12/12 seven_same=7/7 census_rc=0 failures=-
```

Entering revision, for the before side (same counter, run read-only; receipt quoted here):

```
C1=unmet trio=98 claim_r92_true=0 files=19 adm_ok=7 adm_fail=12 patched12=0 seven_same=7 census=ok checks_failed=admission,patched12 rev=7b3fe9d540c9   (rc 1)
```

The 12 failing entering files (`--report` failures field): counter-semantics-r78.md, counter-win-r77.md,
drift-pin-r10.md and the rest of the list below, each with `ac=<hash>` absent from its `verified-at:`.

### Old and new verified-at lines

Admission hash per file: `git log --diff-filter=A --format=%h 7b3fe9d5… -- corpus/knowledge/<file> | tail -1`,
run inside the scratch clone. The %h output is 8 characters; the counter tests the first 7, which are
contained in the 8-character value written.

| file | line | admission | OLD (6d82b8d7) | NEW (8b21c2bf) |
|---|---|---|---|---|
| counter-semantics-r78.md | 1 | 2360cc3b | `verified-at: 2026-11-02 (round 78; the S593 claims below are line-located against the` | `verified-at: 2360cc3b (2026-11-02 (round 78; the S593 claims below are line-located against the)` |
| counter-win-r77.md | 1 | 6a230c4b | `verified-at: 2026-11-02 (round 77; the S592 command claims below are` | `verified-at: 6a230c4b (2026-11-02 (round 77; the S592 command claims below are)` |
| drift-pin-r10.md | 2 | 5be89432 | `verified-at: 2026-10-15T22:06:01–22:17Z, two arms, one per revision:` | `verified-at: 5be89432 (2026-10-15T22:06:01–22:17Z, two arms, one per revision:)` |
| execution-binding-r89.md | 11 | c89e5b6e | `verified-at: 2026-11-04 (round 89; S607/S609/S610 opened by seat Mo89S01Sources, pinned copies` | `verified-at: c89e5b6e (2026-11-04 (round 89; S607/S609/S610 opened by seat Mo89S01Sources, pinned copies)` |
| kernel-v7.3-recheck-r53.md | 2 | 2a4213bf | `verified-at: 2026-10-26` | `verified-at: 2a4213bf (2026-10-26)` |
| lane-silence-r2.md | 2 | 3da84149 | `verified-at: 2026-10-15T04:56Z — read-only recon of the sources above (every count,` | `verified-at: 3da84149 (2026-10-15T04:56Z — read-only recon of the sources above (every count,)` |
| rotation-receipt-grammar-r76.md | 1 | 71107662 | `verified-at: 2026-11-02 (round 76; the S591 clock claims below are line-located` | `verified-at: 71107662 (2026-11-02 (round 76; the S591 clock claims below are line-located)` |
| rotation-schedule-r74.md | 12 | dc50c80b | `verified-at: 2026-11-02 (round 74; the S589 clock claims below are` | `verified-at: dc50c80b (2026-11-02 (round 74; the S589 clock claims below are)` |
| rotation-series-r75.md | 1 | 32132cfb | `verified-at: 2026-11-02 (round 75; the S590 mechanism claims below are line-located` | `verified-at: 32132cfb (2026-11-02 (round 75; the S590 mechanism claims below are line-located)` |
| selftest-flake-r9.md | 2 | cffb37ef | `verified-at: 2026-10-15T21:05–21:35Z — GNU bash 5.3.15, host load average ≈90–140 (the` | `verified-at: cffb37ef (2026-10-15T21:05–21:35Z — GNU bash 5.3.15, host load average ≈90–140 (the)` |
| surfaces-r8.md | 12 | 9738f1ab | `verified-at: 2026-10-15T20:17–20:39Z — note-writer battery: \`--selftest\` (×16),` | `verified-at: 9738f1ab (2026-10-15T20:17–20:39Z — note-writer battery: \`--selftest\` (×16),)` |
| workstate-win-r71.md | 1 | 3627fac0 | `verified-at: 2026-11-01 (round 71; claims below are line-located against the` | `verified-at: 3627fac0 (2026-11-01 (round 71; claims below are line-located against the)` |

Form: the new value is `verified-at: <admission> (<original value text after the colon, verbatim>)`.
The only whitespace not carried is the single space after the colon, which the wrapper's `(` replaces.
A verbatim check (bash, `old` after `verified-at:` with the leading space removed equals `new` between
`verified-at: <hash> (` and the final `)`) returned OK for all 12 files.

### Patch

- File: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-93/w1/patches/Mo93E02Verif.patch`
  (133 lines; generated by `git -C <clone> diff 6d82b8d7`, 12 `+verified-at:` and 12 `-verified-at:` lines,
  `+++`/`---` headers for the 12 `corpus/knowledge/*.md` paths only).
- `git -C <clone> apply --check -R <patch>` → OK (the patch matches the seat tree it was generated from).

### Checks run (all of them; none unrun)

1. `git -C <clone> rev-parse --show-toplevel` → `/fast/scratch/hyaku/mori-r93/Mo93E02Verif/clone` (asserted before the commit).
2. `git -C <clone> diff --stat` → `12 files changed, 12 insertions(+), 12 deletions(-)`.
3. `git -C <clone> diff -U0` → 12 hunks, each one `-verified-at:` and one `+verified-at:` line.
4. Verbatim check (bash, described above) → OK ×12.
5. `count-c1.py` at `8b21c2bf…` (plain and `--report`) and at `7b3fe9d5…` (plain and `--report`), outputs quoted above.
6. `git -C <clone> apply --check -R` on the written patch → OK.

Not run: `count-c2.py`, `controls-r93.sh`, the do-nothing / deletion / forgery controls (those are
the L1's per the contract's ordering), and no test or census. No lane file other than this note and
the patch was written.

## Commit note (conflict with the contract, for the L1 to decide)

The contract says seats "never commit, push, or run any mutating git or jj command anywhere". The
seat spec for this seat asks to "commit your edit in your scratch clone" and to run `count-c1.py`
against that commit. A revision is required for the counter, so I committed once, in the scratch
clone only, with the scratch identity `Mo93E02Verif <scratch@invalid>`. That clone is removed by this
shell's EXIT trap, so the commit is ephemeral; the patch is the durable artifact. Nothing was pushed,
and no command touched the lane tree, `.ufo/state`, `MANIFEST.json` or any sibling lane. The first
commit attempt failed (I had not staged the files) and changed nothing.

## Lane writes

- `.ufo/waves/round-93/w1/Mo93E02Verif.md` (this note).
- `.ufo/waves/round-93/w1/patches/Mo93E02Verif.patch` (new directory `patches/`).

## Tools

No tool was installed, upgraded or removed. I did not read `/home/vgpnk/.omp/agent/RULES.md`, because
no install was needed for this claim; the pacman pause was not relevant to any action taken here.

## Risks and limits

- **Parenthetical wrap.** Several original values open a nested `(` that does not close on the
  `verified-at:` line itself (for example `(round 78; ... against the` closes at the wrapper's `)`
  but its own `(round` is closed on a later line). The text is markdown provenance, and the only
  consumer I found reads the prefix alone (`tools/mori-entry-claims-check.py:55`,
  `FRONTMATTER = ("source:", "verified-at:", ...)`). No parser reads the value.
- **Counter scope.** `count-c1.py` checks presence of the admission short hash inside `verified-at:`.
  It does not check that the hash is the commit that introduced the file's current content. That is the
  contract's named limit and is unchanged.
- **Round-92 lesson correction** (`corpus/lessons/round-92.md`, appended, not edited in place) is not part
  of this seat and is not written here. `claim_r92_true` is met by the data repair alone, but the lesson's
  own sentence stays as filed until its own seat lands the append.

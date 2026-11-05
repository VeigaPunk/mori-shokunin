# Mo94M01Mut — C1 mutation probe (round 94, w1)

Scope: mutate the C1 v2 counter (`count-c1v2.py`, predicate P-C1) in scratch copies only; run the frozen
`controls-r94.py` against each; record KILLED/SURVIVED. Lane and fleet not written (read-only use).

## Frozen inputs (verified)

- `sha256(count-c1v2.py)` = `6eb7fa4cf0ecf86064bb2714a5b93b52bf3356dc6e38e5dc7ee51f7255a7b384`
  = `git show 6b65e7c…:.ufo/waves/round-94/count-c1v2.py | sha256sum` (match, untouched).
- `sha256(controls-r94.py)` = `5ba2943387d5b3bd5fd866b44fc7c1f738894451238de7ce086428256d588db8` (= freeze blob, match).
- Controls pin BASE `84b15230`, ENTERING `7b3fe9d5`. Lane HEAD observed `4ae1678d` (no effect on controls).
- Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (35466 bytes, executable).

## Pristine baseline

Command: `cd $S/work && HYAKU_SCRATCH=$S/hs python3 -I ./controls-r94.py <lane> <fleet>`

```
CTRL do-nothing v1=C1=met v2=C1=met
CTRL do-nothing v2_line=C1=met trio=98 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok rev=84b152308fa6
CTRL left   rev=946a6f5de18b v1=C1=met v2=C1=unmet ... adm_ok=18 adm_fail=1 ... checks_failed=admission
CTRL right  rev=7d6e73e6ac57 v1=C1=met v2=C1=unmet ... checks_failed=admission
CTRL middle rev=f43bc4f6219c v1=C1=met v2=C1=unmet ... checks_failed=admission
EMBED_FALSE_PASS v1=3/3 v2=0/3 live_v2=met do_nothing_v1=C1=met do_nothing_v2=C1=met
exit=0
```

## Mutants

Layout: `$S/work/{count-c1v2.py,controls-r94.py}` pristine; `$S/work/mK/` = copy of both with one edit to
`mK/count-c1v2.py` (controls resolves V2 from its own directory, so each mutant needs its own dir). Diffs
(`diff count-c1v2.py mK/count-c1v2.py`) show exactly the edit below. Each mutant ran under its own
`HYAKU_SCRATCH=$S/hs/mK`, in parallel, with `python3 -I ./mK/controls-r94.py <lane> <fleet>`.

| id | edit to copy | EMBED_FALSE_PASS (v1 / v2 / live) | summary exit | verdict |
|----|--------------|-----------------------------------|--------------|---------|
| m1 | L103 `return ac[:7] in va` (v1 plain substring on full line) | v1=3/3 v2=3/3 live=met | 1 | KILLED |
| m1b | L103 `return ac in tok` (substring form, reversed direction) | v1=3/3 v2=3/3 live=met | 1 | KILLED |
| m2 | L103 `return ac.startswith(tok)` (drop `len(tok) >= 7`) | v1=3/3 v2=0/3 live=met | 0 | SURVIVED |
| m3 | delete L189-190 (`if not census_ok: fails.append("census")`) | v1=3/3 v2=0/3 live=met | 0 | SURVIVED |
| m4 | L181 `if trio < 0:` (was `< 98`) | v1=3/3 v2=0/3 live=met | 0 | SURVIVED |
| m5 | L183 `if adm_fail != 0 or adm_ok < 1:` (was `adm_ok != len(NINETEEN)`) | v1=3/3 v2=0/3 live=met | 0 | SURVIVED (equivalent) |
| m6 | L167-168 `patched = len(TWELVE)` (one_verified_at_change removed) | v1=3/3 v2=0/3 live=met | 0 | SURVIVED |
| m7 | L162 `if os.path.exists(full) and ac and any(ac[:7] in ln for ln in head_lines(full) if ln.startswith("verified-at:")):` (main-loop R02 substring form) | v1=3/3 v2=3/3 live=met | 1 | KILLED |

KILLED = controls summary changes from frozen expectation (v2 0/3 and exit 0 become v2 3/3 and exit 1).
Pristine per-fixture lines for m1/m7 read `C1=met adm_ok=19` on all three fixtures.

## Survivors and the control that would kill each

Survivors were probed in a scratch clone of BASE (`git clone --shared --no-checkout`, toplevel asserted,
commits with identity `mori-r94-probe`), each probe a single-variable fixture, run with `--census` = fleet
census unless stated. Probes are NOT frozen controls; they are proposed kills for the lesson's control gap.

- **m2 (len clause dropped)** — fixture A `51b87760`: `counter-win-r77.md` verified-at token = 5-char prefix
  `6a230` of admission `6a230c4b`.
  - pristine: `C1=unmet trio=98 … adm_ok=18 adm_fail=1 … checks_failed=admission` exit 1
  - m2: `C1=met … adm_ok=19 adm_fail=0 …` exit 0
  - Kill control: a fourth fixture with a sub-7-char admission token; expect `checks_failed=admission`.
- **m3 (census not in fails)** — census stub `fail.sh` (`exit 1`) at base:
  - pristine: `C1=unmet … census=rc1 checks_failed=census` exit 1
  - m3: `C1=met … census=rc1` exit 0
  - Kill control: census-fail fixture (`--census` a failing script); expect `checks_failed=census`.
- **m4 (trio threshold 0)** — fixture B `b01f423c`: `recheck:` removed from `boot-anchor-win-r73.md`, trio=97:
  - pristine: `C1=unmet … trio=97 … checks_failed=trio` exit 1
  - m4: `C1=met … trio=97` exit 0
  - Kill control: trio-drop fixture (one trio file loses a key); expect `checks_failed=trio`.
- **m6 (patched12 not checked)** — fixture C `917feeae`: non-verified-at line appended to `counter-win-r77.md`:
  - pristine: `C1=unmet … patched12=11 … checks_failed=patched12` exit 1
  - m6: `C1=met … patched12=12` exit 0
  - Kill control: body-only change to one of the 12 files; expect `checks_failed=patched12`.
- **m5 (equivalent, not a gap)** — `adm_ok + adm_fail = 19` always, so `adm_ok != 19` ⇔ `adm_fail != 0`, and
  `adm_ok < 1` implies `adm_fail = 19 != 0`. The mutant is equivalent to the original on all inputs; no control
  can kill it. Recorded as equivalent, not as a battery hole.

## Gap summary

Frozen battery kills the R02 class (m1, m1b, m7) through the three embedded fixtures only. It does not kill
the admission-length clause (m2), the census gate (m3), the trio floor (m4), or the patched12 gate (m6).
Each of m2/m3/m4/m6 has a single-variable fixture above that separates pristine from mutant, so each is a
control-battery gap for the round-94 lesson, not a counter defect in the frozen predicate's live reading
(live base reads `C1=met` under every mutant). Live base `C1=met` is not evidence of these gates.

## Commands run (exact, abbreviated paths)

- `python3 -I ./controls-r94.py <lane> <fleet>` — pristine exit 0; mutant exits m1=1, m1b=1, m2=0, m3=0, m4=0, m5=0, m6=0, m7=1.
- `TMPDIR=$P/hs python3 -I ./count-c1v2.py <rev> --repo $C --census <fleet census>` — probes A, B, C, base.
- `TMPDIR=$P/hs python3 -I ./mK/count-c1v2.py <rev> --repo $C --census <…>` — mutant probes m2, m4, m6, m3.

## Installs, scope, cleanup

- Installs: none.
- Lane, fleet, shokuknow: read-only (`git show`, `git log`, `git rev-parse`, `git clone --shared` source only).
- Git writes only inside scratch: one probe clone `$S/probe/clone` (`git clone --shared --no-checkout`, toplevel asserted, commits by identity `mori-r94-probe`). Controls made their own clones under `$S/hs/*/mori-r94/` and removed them on exit. No `$S/clone` was created.
- Scratch `$S` deleted before yield (`rm -rf -- "$S"`).

# ScribeNoHarmLedger — round 15 (mori-r15-positive), C1 coverage

Scope: report-only. No production, fixture, or verifier edits. No commands run for
verification. No installs (parent host-safety rule received; none were needed).
Counts below are from file data (line counts, `grep -c` pattern counts, sha256 of
the current bytes). Nothing here is a behavioral result.

## 1. L1 must run once (after integration)

Run from `/home/vgpnk/Projects/shokunin/mori-shokunin`. Each command is a maintained gate
registered in `SKILL.md` (registry table, rows `census`, `silence oracle`, `r13 regressions`,
`r14 regressions`).

| # | Command | Verdict map (from registry / file header) | Why it matters for C1 |
|---|---|---|---|
| 1 | `bash tools/mori-census.sh --selftest` | exit 0 pass, 1 fail; prints `MORI_CENSUS_SELFTEST: …` (`tools/mori-census.sh:386-387`, `:874`) | Covers the new positive-evidence tokens and the unchanged raw-count unavailable semantics (`run_selftest()` at `tools/mori-census.sh:2507-3812`). |
| 2 | `bash tools/mori-census.sh` (live, read-only) | `MORI_CENSUS: CLEAN|DRIFT (...)`, exit 0/1; rc 2 = setup/crash | Confirms the live census still produces one final roll and no new crash. Requires the same env the registry names (`MORI_SHOKUNIN_ROOT` outside the fleet tree if needed). |
| 3 | `bash tools/mori-silence-cases.sh` | `MORI_SILENCE_CASES: matched=N total=M`; exit 0 iff matched==total; setup 2 (`tools/mori-silence-cases.sh:178-181`, `:1217-1219`) | Silence grading must not drift; registry notes case table is in-script. |
| 4 | `python3 tools/mori-round13-regressions.py --output <dir>` | 0 clean · 1 claim mismatch · 2 could-not-evaluate (`tools/mori-round13-regressions.py:2943-2972`) | Re-measures pinned r13 C1 claims: `R13_C1_UNIT_OOM_KILL_ALARM`, `R13_C1_SIGKILL_WARN_PRESERVED`, `R13_C1_UNIT_FAILURE_ROUTING`. Highest no-harm risk: it pins expected finding ids/severities. |
| 5 | `python3 tools/mori-round13-regressions.py --selftest` | `SELFTEST: pass checks=N cases=M` / exit 1 (`:2727-2862`) | Parser checks plus isolated real-gate subprocess cases. |
| 6 | `python3 tools/mori-round14-regressions.py --output <dir>` | 0 clean · 1 claim failed or frozen control did not reproduce · 2 setup/usage/pin (`tools/mori-round14-regressions.py:2408-2426`) | Same-census before/after journal gate; frozen red control at `.ufo/waves/round-14/frozen/mori-census.sh`. Highest no-harm risk for the finding-field addition. |
| 7 | `python3 tools/mori-round14-regressions.py --selftest` | `SELFTEST: pass checks=N` / exit 1 (`:2277-2382`) | Parser checks and real-gate red rc1 / tamper rc2. |

Ordering: L1 runs 1→7 once each. Do not rerun to "confirm"; record each rc and last line.
Run 4 and 6 only after 1 is green, since both exercise the census under test.

## 2. Counts from file data (not claims)

| Item | Measured now | Source of measurement | Recorded elsewhere (not re-measured) |
|---|---|---|---|
| `tools/mori-census.sh` lines / sha256 prefix | 3842 / `0e41cb83fce2e8c5` | `wc -l`, `sha256sum` | SKILL.md registry: census SHA `0e41cb83…` (matches prefix) |
| `run_selftest()` span | lines 2507–3812 | `grep -nE '^run_selftest\(\)'` + awk to closing brace | — |
| census `check`/`check_cli` call lines (pattern `^\s*check(_cli)?\s`) | 92 | `grep -cE` | SKILL.md: `104/104 at 8d22d18` — **does not match 92**; see §4 |
| `tools/mori-silence-cases.sh` lines / sha256 prefix | 1219 / `34cd5770889ec6e7` | — | SKILL.md: "28 cases"; `corpus/README.md` cites oracle `matched=28 total=28` at older pins (sha differs from earlier notes; not compared) |
| oracle `assert_case` call lines | 26 | `grep -cE '^\s*assert_case '` | Does not equal 28; the grep counts call sites, not emitted ids. Unresolved (§4). |
| `tools/mori-round13-regressions.py` lines / sha256 prefix | 3033 / `304cb22336da40c6` | — | SKILL.md: r13 gate `33 checks, 2 isolated cases` at 8d22d18 — `check(` call lines = **33** (match) |
| `tools/mori-round14-regressions.py` lines / sha256 prefix | 2476 / `c39e5a7352666d09` | — | SKILL.md: r14 `20 checks` — `check(` call lines = **20** (match) |
| `positive_` tokens in census | 0 | `grep -c positive_` | Expected: production not yet landed. |
| `.ufo/waves/round-15/fixtures/` | absent | `ls` | Fixture packs are written by other seats; none exist yet. |
| `.ufo/waves/round-13/frozen/` | present: `inputs.json`, `mori-census.sh` (148773 B), `mori-silence-cases.sh` (54265 B) | `ls -la` | r13 gate reads these pinned bytes. |
| `.ufo/waves/round-14/frozen/` | present: `expected.json` (992 B), `inputs.json`, `mori-census.sh` (173544 B, exec), `mori-silence-cases.sh` (61159 B) | `ls -la` | r14 red control. Pinned `39abda0a…` per SKILL.md; not re-hashed here. |

Only the **`check(` call-line counts** for the two regression gates reproduce the
SKILL.md claims exactly. The census and oracle counts do not, and must not be copied
into the report as verified totals.

## 3. No-harm ledger (what each command can and cannot falsify)

- Census selftest (#1): can falsify census-side regressions in hermetic temp trees. It
  does not prove completeness, authenticated MESSAGE_IDs, or unique victims. Those are
  explicit non-claims in the spec and must stay so in any scribe text.
- Census live (#2): read-only; rc and roll grammar only. Positive evidence in the live
  run is not a claim that the host had a current-boot OOM.
- Oracle (#3): behavioral cases over the census CLI. Its verdict grammar is in-script
  (`tools/mori-silence-cases.sh:41-84`).
- r13 gate (#4/#5): frozen pins; a red result means a claim pinned in
  `tools/mori-round13-regressions.py` changed. Expected to stay green only if the
  existing raw tokens and finding ids are unchanged, which is the spec's requirement.
- r14 gate (#6/#7): the frozen control must still reproduce the defect (rc 1 path); the
  green measurement must go green. A new finding field is only acceptable if the r14
  expectations tolerate additional fields. This is **not verified** from the files I
  read here (see §4).

## 4. Unresolved facts (named honestly)

1. Census selftest count: SKILL.md says `104/104 at 8d22d18`; the file has 92 check-call
   lines under the pattern I used. Either the pattern misses calls (e.g., nested or
   differently indented calls, loops building cases) or the 104 figure is stale. Not
   resolved by file data alone; L1's #1 run output will settle it.
2. Oracle count: SKILL.md says 28 cases; `assert_case` call-lines = 26. Case ids are
   emitted from more than one helper or loop (not enumerated here). Unresolved.
3. Whether the r13/r14 gates' expected finding sets tolerate the additional positive
   fields that the census production change will add. I did not read the expectation
   tables in full. L1 must check it through command #4/#6 output, not by inference.
4. Whether `.ufo/waves/round-14/frozen/mori-census.sh` still matches its pinned sha
   `39abda0a…`. I did not hash it (the registry gives the pin; the file exists).
5. Dispatch-side: this seat's own `dispatch.json` entry (line ~920-922) and the spec
   item (`spec.json:251-255`) are the source of this assignment; the spec's
   `context` says "skip all builds/tests/linters/formatters/smoke runs". That rule binds
   this seat; L1 runs the commands in §1 once after integration.
6. Host safety: parent instructed that pacman -S requires `pacman -Sp` pre-check and
   that -Sy/-Syu/-U/-R are forbidden. This seat performed no installs and no upgrades.
   Tool versions recorded: none installed or updated by this seat.

## 5. Artifacts touched by this seat

- Written: `.ufo/waves/round-15/build/ScribeNoHarmLedger.md` (this file).
- Read-only: `.ufo/waves/round-15/spec.json`, `dispatch.json`, `task-response.json`,
  `build/swarm-registry.json`, `SKILL.md`, `corpus/README.md`, `tools/*`, frozen dirs
  (listing only).
- Not edited: any production file, fixture, verifier, aggregator, MANIFEST, SHONEN, or
  sibling lane. No commits.

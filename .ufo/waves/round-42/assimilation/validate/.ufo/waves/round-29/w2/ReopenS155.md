# ReopenS155 — falsification of row S155 and its Gate lines

Seat `MoriR29.ReopenS155`, leaf (no subagents, no background jobs). Lane
`/home/vgpnk/Projects/shokunin/mori-shokunin`; HEAD read with read-only `git rev-parse` returns
`8809a3fe1eaa87a0afa177a15263d174378e7462`, the wave tip. Scratch:
`/fast/scratch/hyaku/mori-r29/w2/ReopenS155/` (fetched bytes and hashes live there). No tool
installed or upgraded, no pacman transaction, no unit touched, no signal sent, no omp run, no git
or jj write. Nothing written outside this report and my scratch dir.

Scope audited: `corpus/SOURCES.md:161` (row S155, read raw) and the Gate lines drafted for it in
`corpus/lessons/round-29.md` — admit line `:62`, and the earlyoom reject lines `:63`, `:64`, `:65`
that the same source work produced. No LSP is applicable: the artefact is a Markdown registry row
and an upstream patch, not a program whose symbols are in this repo.

Method: fresh HTTP GET of every URL in the row and those Gate lines (`curl -sS -o … -w
'http=%{http_code} bytes=%{size_download}'`), `sha256sum` on the bytes, `nl -ba` line reads for
each anchor and quote, plus `kill.c`/`main.c` at the introducing commit and tag to test the
cross-references. Fetches at 2026-10-22T20:32:36Z (patch), 20:32:51Z (four v1.9.0 raw files) and
the same minute (v1.9.0 `main.c`, introducing-commit `kill.c`).

## Verdict

**The row holds on every cell.** URL, HTTP status, byte size, sha256, commit identity and date,
all five patch anchors, the scope's exclusions, the 11-column shape, tier/kind/status and both
`used-by` citations reproduce. The `teaches` is supported by the bytes with one unqualified
clause (G4 below).

**The Gate record carries three defects, none of which changes the S155 admission:** two word
counts do not reproduce (17 vs 16 on the admit line `:62`; 8 vs 6 on the kill.c reject `:63`), and
one reject rationale clause is falsified by the line it quotes (`:65`, `kill.h` does contain
`dryrun`). No lane counter reads these counts (`grep -n 'words' count-c1.sh count-c2.sh
check-blind-wave.sh` prints nothing), so no counted condition is affected. The class is *record
miscount*, not `tool error`; this row is not a tool row, so there is nothing to route to the L1's
draft tool change.

## Claim | recorded | observed | holds?

| # | Claim | Recorded | Observed | Holds? |
|---|---|---|---|---|
| R1 | Source URL resolves | `.patch` URL, access `2026-10-22T19:59:28Z` | HTTP 200 at `20:32:36Z`, `bytes=2978` | yes |
| R2 | Patch size | 2 978 B | 2 978 B (`wc -c`) | yes |
| R3 | Patch sha256 | `893e238ea3b7f512f0506ccc87e0decfea8846e2e4b0704c51ced2820465d4bb` | same digest | yes |
| R4 | Commit identity | `ca2251fcd222af8c857aec4a26e182cf5f9c596e`, subject "main: add dry-run option" | `From ca2251fcd222…` (patch:1), `Subject: [PATCH] main: add dry-run option` (patch:4) | yes |
| R5 | Author date | `2020-03-03T20:38:03+08:00` | `Date: Tue, 3 Mar 2020 20:38:03 +0800` (patch:3) | yes |
| R6 | Anchor `:21-22` `#### \-\-dryrun` + description | as written | patch:21 `+#### \-\-dryrun`, :22 `+dry run (do not kill any processes)` | yes |
| R7 | Anchor `:35-38`, guard inside `kill_wait`, returns before `kill()` | as written | patch:33 `int kill_wait(…)`, :35-38 guard+`return 0`, :41 context `int res = kill(pid, sig);`; same guard at `kill.c@ca2251fc:60-63`, call at `:66` | yes |
| R8 | Anchor `:71` option table spells `dryrun` | as written | patch:71 `+ { "dryrun", no_argument, NULL, LONG_OPT_DRYRUN },` | yes |
| R9 | Anchor `:79-82` parser prints `dryrun mode enabled`, sets flag | as written | patch:79 `case LONG_OPT_DRYRUN:`, :80 `warn("dryrun mode enabled, will not kill anything\n");`, :81 `args.dryrun = 1;`, :82 `break;` | yes |
| R10 | Anchor `:90` help text spells `--dry-run` | as written | patch:90 `+ "  --dry-run                 dry run (do not kill any processes)\n"` | yes |
| R11 | "introduction … only" | introduction of the option | every one of the five anchored lines is a `+` line, i.e. absent from the parent | yes |
| R12 | Scope exclusion `S118:271-274` | v1.9.0 kill.c guard | `kill.c:271-274` is exactly `if (args->dryrun && sig != 0) { warn(…); return 0; }`; `S118` carries v1.9.0 `kill.c` (`corpus/SOURCES.md:124`), its anchor lists `:272` | yes |
| R13 | Scope exclusion `S119:295` | v1.9.0 dry-run print | `main.c:295-296` is the same warn plus `args.dryrun = 1`; `S119` anchor says `dry-run flag main.c:295` (`corpus/SOURCES.md:125`) | yes |
| R14 | Scope exclusion `S119:161` | version line | `main.c:161` `fprintf(stderr, "earlyoom " VERSION "\n");` | yes |
| R15 | Scope exclusion `S115` | v1.9.0 manual text | `S115` source is v1.9.0 `MANPAGE.md` and its scope names `--dryrun` (`corpus/SOURCES.md:121`); `MANPAGE.md:205-206` carry it | yes |
| R16 | Kind / tier / status | `code` / `A` / `mined` | commit is upstream source code (primary for this scope, CORPUS.md:101-103); status `mined` requires a `used-by` citation (CORPUS.md:103-104) and one exists (R18) | yes |
| R17 | 11-column shape, no stray `|` | 11 columns | field split yields exactly 11 cells; id `S155` appears once (`grep -c '^\| S155 '` = 1) | yes |
| R18 | `used-by` cites S155 as a word | `corpus/lessons/round-29.md`, `tools/fixtures/mori-oom-killers/cases-a2-r29.json` | both paths exist; lesson cites S155 4× (`:17`, `:19`, `:62`, `:70`); case file has top-level `"sources": ["S153","S154","S155"]` (`cases-a2-r29.json:8`) | yes |
| R19 | `teaches`: send-site no-op, no delivery | as written | guard returns before `kill()` for `sig != 0`; for `sig == 0` the path proceeds to `kill(pid, 0)`, which delivers nothing | yes, with the qualifier in G4 |
| G1 | Gate admit: sha256 | `893e238e…d4bb` | same | yes |
| G2 | Gate admit: quote at `:35-38` verbatim | `if (args.dryrun && sig != 0) { warn(\"dryrun, not actually sending any signal\n\"); return 0; }` | identical text across patch:35-38 (lines joined only by whitespace) | yes |
| G3 | Gate admit: quote is `17 words` | 17 | 16 whitespace-delimited tokens; adjacent Gate counts reproduce exactly under that unit (S153 `:61-63` 22/22, `:82-85` 24/24) | **no — miscount (≤25 still met)** |
| G4 | `teaches` wording "`kill_wait` returns before `kill()`" | unconditional | true only under `sig != 0`; the guard condition is quoted in R7/G2, and `kill(pid, 0)` sends no signal, so the delivery half holds unconditionally | holds with qualifier; not falsified |
| G5 | Reject `:63` v1.9.0 `kill.c`: sha256, duplicate-URL reason | `b32e0fad…0bf3`, duplicate of S118 | digest identical; S118 does carry this URL (`corpus/SOURCES.md:124`) | yes |
| G6 | Reject `:63` quote `:272` verbatim | `warn(\"dryrun, not actually sending any signal\n\");` | `kill.c:272` identical; `:271` is the `if`, `:273` `return 0;`, `:274` `}` | yes |
| G7 | Reject `:63` quote is `8 words` | 8 | 6 whitespace-delimited tokens | **no — miscount** |
| G8 | Reject `:64` `MANPAGE.md`: sha256, `:205-206`, 9 words, duplicate of S115 | `cc48b02e…defa`, 9 words | digest identical; `:205` `#### \-\-dryrun` (2 tokens) + `:206` description (7 tokens) = 9; S115 carries the URL and names `--dryrun` | yes |
| G9 | Reject `:65` `kill.h` / `testsuite_cli_test.go`: sha256, byte sizes, quote `kill.h:36-37` | `abf8577b…0bfb` (1 440 B), `1dc87642…b795` (9 317 B), quote 8 words | digests and sizes identical (1 440 B, 9 317 B); `kill.h:36` `/* Flag --dryrun was passed */`, `:37` `bool dryrun;` = 6+2 tokens | yes |
| G10 | Reject `:65` rationale: "a case-insensitive grep for `dryrun` and `version` returned no line in either file" | no line in either file | `grep -in 'dryrun\|version' kill.h testsuite_cli_test.go` prints `kill.h:36` and `kill.h:37`; `testsuite_cli_test.go` prints nothing | **no — clause falsified for `kill.h`**; the reject's primary reason ("does not carry the fact") still holds |

## Evidence (commands and outputs)

- Patch: `curl -sS -o patch.txt -w 'http=%{http_code} bytes=%{size_download}' <commit .patch URL>` →
  `http=200 bytes=2978`; `sha256sum patch.txt` → `893e238ea3b7f512f0506ccc87e0decfea8846e2e4b0704c51ced2820465d4bb`;
  `sed -n '1,6p'` → `From ca2251fcd222af8c857aec4a26e182cf5f9c596e …`, `Date: Tue, 3 Mar 2020 20:38:03 +0800`,
  `Subject: [PATCH] main: add dry-run option`.
- Hunk context proving R7: `sed -n '31,45p' patch.txt` shows `int kill_wait(const poll_loop_args_t args, pid_t pid, int sig)`
  at patch:33, the `+` guard at :35-38, and the unchanged context line `int res = kill(pid, sig);` at :41.
- Introducing-commit file (independent of the patch rendering):
  `curl …/raw/rfjakob/earlyoom/ca2251fcd222…/kill.c` → 200, 8 685 B, sha256 `01635f91…23fa6`;
  `kill.c:58` signature, `:60-63` guard, `:66` `int res = kill(pid, sig);`, `:259` `warn("sending %s to process …")`,
  `:263` `int res = kill_wait(args, victim.pid, sig);`.
- v1.9.0 files: `kill.c` 21 169 B `b32e0fad…0bf3`; `MANPAGE.md` 10 114 B `cc48b02e…defa`;
  `kill.h` 1 440 B `abf8577b…0bfb`; `testsuite_cli_test.go` 9 317 B `1dc87642…b795`;
  `main.c` 21 053 B `08656b0b…d0e4` with `:161` version line, `:184` option table, `:295-296` dry-run print,
  `:332` help spelling `--dryrun`.
- Word counts: whitespace tokenisation of each quoted segment; the unit reproduces the S153 counts exactly
  (22 and 24), and the S155 admit quote is 16 tokens, the kill.c `:272` quote is 6 tokens. Both stay under the
  CORPUS.md:114 bound of 25 words, so the defect is the recorded number, not the quote length.
- Counter exposure: `grep -n 'words' .ufo/waves/round-29/{count-c1.sh,count-c2.sh,check-blind-wave.sh}` → no output.

## Defects to route (all in `corpus/lessons/round-29.md`, Gate section)

1. `:62` (S155 admit) — `(17 words)` should be `(16 words)`. The quote text itself is correct and within bound.
2. `:63` (kill.c reject) — `(8 words)` should be `(6 words)`.
3. `:65` (kill.h/testsuite reject) — the rationale clause "a case-insensitive grep for `dryrun` and `version`
   returned no line in either file" is contradicted by its own quote: `kill.h:36-37` match `dryrun`. The reject
   verdict stands on "does not carry the fact" (a field declaration only), so a wording correction suffices.

## Confidence and remaining unknowns

- Row-level findings (R1-R18, G1-G2, G5-G6, G8-G9): **high** — direct HTTP 200 fetches, digests re-derived from
  the bytes, anchors read with `nl -ba`.
- G11/R19 phrasing nuance: **high** on the bytes (`sig != 0` guard, `kill(pid, 0)` is not a delivery), **medium**
  on whether the L1 wants the qualifier spelled in `teaches`; the Gate quote already carries the condition.
- The claimed access times (`19:56:07Z`, `19:59:10Z`, `19:59:28Z`) are historical and cannot be re-observed; the
  content digests, sizes and pointers reproduce at `20:32–20:34Z`, so nothing in the row depends on the clock claim.
- GitHub's rendered `.patch` bytes are re-generated per request; today's rendering is byte-identical to the
  recorded digest, but a future re-render is outside this check's control.
- Not in the row or Gate, noted for completeness: the w1 report says the patch is "92 lines"; `wc -l` reports 93
  (file ends with a newline). No row or Gate claim uses the line count.
- The introducing commit's patch places `--dryrun` in the option table and manual but `--dry-run` in the help
  text; v1.9.0 later prints `--dryrun` in help (`main.c:332`). The row anchors each spelling to its own line and
  claims no consistency, so this is recorded faithfully, not a defect.

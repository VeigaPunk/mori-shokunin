# Round 93 — mori (L1 MoriR93, attempt 1) — lesson draft, seat Mo93S01Lesson

Draft only. Seat Mo93S01Lesson commits nothing. The L1 integrates it:

- section (a) is appended to `corpus/lessons/round-92.md`, after its last line, and only after the
  landing's after-receipt prints `C1=met` (see the guard under (a));
- sections (b) and (c) go into `corpus/lessons/round-93.md` (its `## Mistakes` and `## Gate`).

Revisions: entering `7b3fe9d540c98b8b0390a0f9bbe78de4341092a5`; patch base
`6d82b8d7ef6d94a5527737f9242cdf04ad018da7`; round-92 landing `9dce2ca6f651` (`git log`: "round-92:
landing — C1 provenance trio on 19 knowledge entries ...").

## (a) CORRECTION-OF-RECORD — exact text to append to `corpus/lessons/round-92.md`

Append after the final line of that file (after the `## Planned (round 93)` list). Do not edit
lines 51–52 or any other existing line.

````markdown

## Correction of record (round 93) — appended, not an edit in place

Corrects the sentence wrapped over lines 51–52 of this file, in `## Work the round landed`: "Each
`verified-at` names the admission commit of its file (`git log --diff-filter=A`)". That sentence was
false at the round-92 landing `9dce2ca6`: it held for 7 of the 19 trio files and failed for 12.

- `python3 -I .ufo/waves/round-93/count-c1.py 9dce2ca6 --repo <lane> --report` prints
  `C1_REPORT rev=9dce2ca6f651 trio=98 claim_r92_true=0 files=19 adm_ok=7 adm_fail=12 patched12=0/12`.
  The same counter at the entering revision `7b3fe9d5` prints the same counts
  (`.ufo/waves/round-93/evidence/measure-c1-entering.txt`).
- The 12 files whose `verified-at:` line does not carry the admission short hash: counter-semantics-r78
  (admission `2360cc3b`), counter-win-r77 (`6a230c4b`), drift-pin-r10 (`5be89432`), execution-binding-r89
  (`c89e5b6e`), kernel-v7.3-recheck-r53 (`2a4213bf`), lane-silence-r2 (`3da84149`),
  rotation-receipt-grammar-r76 (`71107662`), rotation-schedule-r74 (`dc50c80b`), rotation-series-r75
  (`32132cfb`), selftest-flake-r9 (`cffb37ef`), surfaces-r8 (`9738f1ab`), workstate-win-r71 (`3627fac0`).
  Each admission short hash is `git log --diff-filter=A --format=%h 7b3fe9d5 -- corpus/knowledge/<file>`,
  last line.
- The 7 files whose `verified-at:` value already was the admission short hash were true at the
  landing: audit-r11 (`e4855e8c`), progressing-weak-r2 (`3da84149`), silence-cutover-r3 (`1439c473`),
  silence-grading-r2 (`3da84149`), verdict-machine-r4 (`5b62c897`), verdict-machine-r5 (`a420deb7`),
  verdict-machine-r6 (`92b2e427`).

The round-92 verifier spot-check (`corpus/lessons/round-92-verifier-spotcheck.md`, section 2, C1, and
routed defect D1 in section 6) found the same false sentence. This entry is the D1 fix, made by appending
as that spot-check asked. The round-93 C1 repair changes only the value of each of the 12
`verified-at:` lines, to `verified-at: <admission short hash> (<original value, unchanged>)`; no other
line of those files changes. At the round-93 landing `<landing hash, from .ufo/reports/round-93/mori.md>`
the frozen counter prints `C1=met ... adm_fail=0` (`.ufo/waves/round-93/evidence/after-r93.txt`). So the
sentence is true of the round-93 landing and was false of `9dce2ca6`.

Scope: this entry corrects the sentence only. The round-92 verdicts are not changed by it: C1 presence
met as frozen, depth not established; C2 not met and not admitted. The counter checks that the short
hash appears inside `verified-at:`. It does not check that the hash is the commit that introduced the
file's current content (named limit, `.ufo/waves/round-93/contract.md`, P-C1).
````

Guard for the L1 (not part of the appended text): append only if `evidence/after-r93.txt` prints
`C1=met`. If it prints `C1=unmet`, the last paragraph of the entry must be replaced by the unmet verdict
and its `adm_fail` count before appending, and the sentence stays recorded as false at the landing. The
entry is not dropped in either case. The landing hash fills the bracketed placeholder; no other
placeholder remains.

## (b) Mistakes — round 93

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `unchecked-rule-2` — the first contract draft planned to complete the recorded digests in place (31 prefix-only rows, S125 unpinned). SOURCES rule 2 allows only `status`, `recheck` and `used-by` to change in place | `.ufo/waves/round-93/contract.md` P3 (line 23); rule 2 at `/home/vgpnk/Projects/shokunin/CORPUS.md:116-118` ("Only `status`, `recheck` and `used-by` change in place") | CORPUS rule 2 and contract P3 | contract redrafted before its commit: the digest-gate claim is not taken (P3); no registry row is edited in place; the debt is routed as frontier |
| `truncated-read-window` — the first trio counter read 4096 bytes per file and counted 97 of 98 knowledge entries; `corpus/knowledge/userspace-oom-killers-r26.md` has its trio keys beyond byte 4096 | `.ufo/waves/round-93/count-c1.py:71` (now `fh.read(65536)`); `.ufo/waves/round-93/evidence/measure-c1-entering.txt` (`trio=98` at the 64 KB read); the 4096-byte rerun, scratch only: `trio=97` (Checks, item 5) | none | 64 KB read at `count-c1.py:71`; shown able to fail by the 4096-byte rerun, which prints `trio=97` where the frozen read prints `trio=98` |
| `miscounted-host-literal` — the first draft gave 10 occurrences of the host home path; the measured byte count is 18 | `.ufo/waves/round-93/contract.md` P2 (line 18: 12 `git grep` lines in three files, byte count 18, regex count 18); `.ufo/waves/round-93/evidence/measure-c2-entering.txt` (`home_literals=18 vgpnk_refs=18`) | none | contract premise P2 states the measured count; `count-c2.py --report` prints `home_literals` and `vgpnk_refs` |
| `wrapped-sentence-sed-noop` — the first text-only control substituted a pattern that matched a sentence wrapped over two lines, changed nothing, and produced no fixture commit | `.ufo/waves/round-93/controls-r93.sh` lines 35–39 (sed at 36, `grep -q` assertion at 37, `exit 2` on a no-op); `.ufo/waves/round-93/evidence/controls-r93.txt` (text-only control, current script: `rev=4bd390bc3148`, `C1=unmet ... adm_fail=12`, rc 1) | none | the control matches the first wrapped line (lesson line 51, ending `admission`) and asserts the substitution with `grep`, exiting 2 on a no-op |

Evidence limits for (b):

- `P3` names the rule as `corpus/CORPUS.md` rule 2. No `corpus/CORPUS.md` exists in the lane (`find` over
  the lane root returns nothing). The rule text lives in the fleet-root file
  `/home/vgpnk/Projects/shokunin/CORPUS.md`, lines 116–118, the SOURCES contract carried from kaika. The
  lane's `corpus/SOURCES.md` does not contain the sentence (`grep -c 'Only `status`' corpus/SOURCES.md` → 0).
  P3 should be corrected to the fleet-root path in the L1 integration; this seat does not edit the contract.
- The first-draft figures (the "10 occurrences" of M3, the 4096-byte read of M2 as first run, and the
  "nothing to commit" result of M4) are not in the committed evidence files named above. The round-93
  lane has one committed contract revision (`6d82b8d7`). Those three observations are the L1's account; this
  seat did not observe them. Only the 4096-byte rerun in Checks item 5 was measured here. `controls-r93.txt`
  does not contain that rerun; the controls note cites it only if the L1 adds it.

## (c) Gate scaffold — sourced frontier for round 93 (L1 fills the blanks from the scout report)

Registry check run by this seat: `grep -n 'S622\|S623' corpus/SOURCES.md` → no rows. The highest
round-92 row is S621 (queued; `grep -o '^| S6[0-9][0-9] ' corpus/SOURCES.md` lists S615–S618 and S621).
S622 and S623 are new rows, opened in this round, written by the L1 per SOURCES rule 1 (`/home/vgpnk/Projects/shokunin/CORPUS.md:112-114`).

Gate table in the `## Gate (sources, protocol §2b)` form of `corpus/lessons/round-92.md`:

| Row | URL | Access and recomputation | Located quote (≤25 words) | Decision |
|---|---|---|---|---|
| S622 | [L1 fills: git-log documentation page, official source only] | [L1 fills: access date; full sha256 and byte count of the pinned copy] | [L1 fills: quote, with its location in the pinned copy, establishing what `git log --diff-filter=A` lists] | [L1 fills: admit (mined) / reject / queued]; used-by: `corpus/lessons/round-93.md`, `.ufo/waves/round-93/contract.md` (C1 sourced claim); `corpus/lessons/round-92.md` correction (a) |
| S623 | [L1 fills: Python documentation page for the `-I` (isolated mode) option, official source only] | [L1 fills: access date; full sha256 and byte count of the pinned copy] | [L1 fills: quote establishing what `-I` isolates] | [L1 fills: admit (mined) / reject / queued]; used-by: `.ufo/waves/round-93/count-c1.py`, `.ufo/waves/round-93/count-c2.py`, `.ufo/waves/round-93/controls-r93.sh` (each invokes `python3 -I`) |

The `teaches` cell for each row is the quoted sentence's claim, stated in one line by the L1. Neither
cell is filled by this seat. Every number in the Gate, if any, carries its command (CORPUS rule "A count
carries its command").

## Checks run by this seat (scratch clone only; no lane write other than this file and `patches/`)

Clone: `git clone --shared --no-checkout` into `/fast/scratch/hyaku/mori-r93/Mo93S01Lesson/clone`, then
`checkout -B seat 6d82b8d7`; `git rev-parse --show-toplevel` printed the clone path; `git log -1` printed
`6d82b8d7 round-93: frozen contract ...`. Scratch is removed by the EXIT trap.

1. Lesson lines at landing (`git show 9dce2ca6:corpus/lessons/round-92.md | sed -n '51,52p'`):
   line 51 `- Provenance trio lines on 19 knowledge entries (C1 presence). Each \`verified-at\` names the admission`;
   line 52 `  commit of its file (\`git log --diff-filter=A\`); each \`recheck\` is taken from the entry's own body or`.
   `git diff --quiet 6d82b8d7 9dce2ca6 -- corpus/lessons/round-92.md` → rc 0 (unchanged between base and landing).
2. Counter at landing: `python3 -I $LANE/.ufo/waves/round-93/count-c1.py 9dce2ca6 --repo $LANE --report`
   → `C1_REPORT rev=9dce2ca6f651 trio=98 claim_r92_true=0 files=19 adm_ok=7 adm_fail=12 patched12=0/12 seven_same=7/7 census_rc=0 ...`
   (read-only; `$LANE=/home/vgpnk/Projects/shokunin/mori-shokunin`).
3. Counter at entering, as committed: same command with `7b3fe9d5` → `C1_REPORT rev=7b3fe9d540c9 trio=98 ... adm_fail=12 ...`,
   identical counts to `evidence/measure-c1-entering.txt`.
4. Admission hashes: `git log --diff-filter=A --format=%h 7b3fe9d5 -- corpus/knowledge/<file> | tail -1` for the
   12 failing and 7 passing files (values in (a)); the 7 passing files' `verified-at:` at `9dce2ca6` equal
   their admission hash.
5. Read-window rerun (scratch copy, `sed 's/fh.read(65536)/fh.read(4096)/'`, lane copy untouched):
   `python3 -I $S/count-c1-4096.py 7b3fe9d5 --repo $LANE --report` → `C1_REPORT rev=7b3fe9d540c9 trio=97 ... adm_fail=12 ...`.
   Trio check per file at `7b3fe9d5` (python, 64 KB vs 4096 bytes): the only file that changes is
   `corpus/knowledge/userspace-oom-killers-r26.md`.
6. Greps: `find` for `CORPUS.md` in the lane → none; `/home/vgpnk/Projects/shokunin/CORPUS.md:116-118` holds rule 2;
   `grep -rn '10 occurrences\|ten occurrences' .ufo/waves/round-93` → none; `grep -n 'S622\|S623' corpus/SOURCES.md` → none.

Not run by this seat, reported as unrun: `controls-r93.sh` (it writes fixtures; the L1 owns its rerun at
integration); `count-c1.py` at the round-93 landing (the landing does not exist yet); `count-c2.py` (no
claim here depends on a new C2 measurement; M3 cites `measure-c2-entering.txt`); the lesson's sentence
after the repair (needs the patch). No installs: only `git`, `python3`, `sed`, `grep`, `tar`, `find`, all
pre-existing; nothing added under `~/.local/bin` or elsewhere.

Patch: `patches/Mo93S01Lesson.patch` is the output of `git -C <clone> diff 6d82b8d7`. This seat changes no
tracked file, so the patch is empty; the deliverable is this untracked file, which the L1 copies.

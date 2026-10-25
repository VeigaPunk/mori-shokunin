# Scout — exact round-43 wording the C1 witness reproduces

lane: mori · round: 44 · wave: 1 · role: scout (leaf, no dispatch) · date: 2026-10-25
lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin` · lane tip `7cb59c6891d4f5d0266fe062565f094da835dc84`
fleet repo: `/home/vgpnk/Projects/shokunin` (read-only) · round-44 entering tip `1429c791db5891c484684feef893799909d2d6a8`

Question: pin the exact round-43 wording the C1 witness (`.ufo/waves/round-44/fixtures/figures-r43.tsv`
rows F03/F04) reproduces, with file:line pointers taken from **committed bytes** and with the
closure's observed values and commands quoted verbatim.

All pointers below were produced by `git show <rev>:<path> | grep -n …` / `| sed -n 'Np'`;
no working-tree file was used as the source of a quoted line.

---

## 1. Revision pins (identity of the quoted bytes)

| artifact | revision | sha256 of committed bytes |
|---|---|---|
| `.ufo/reports/round-43/mori.md` (fleet) | `0c9e9999f8dcc7235ae2129d51ec9565885c7063` (final) | `ea6ac0f6a3ed0d8e49d7bd14789d6a85c3dadd4ee028ae7feead4959ffb0b10a` |
| `.ufo/reports/round-43/mori.md` (fleet) | `484e6eff` (first landing) | sentences quoted below are byte-identical to `0c9e9999` (see §2 note) |
| `corpus/lessons/round-43.md` (lane) | `1429c791…` = `91cb221f…` = `efb92cd5…` | `66e273c8386895a505085df57de94c46540877fc01836148d04efad23eb9d495` |
| `corpus/lessons/round-43-verifier-spotcheck.md` (lane) | `1429c791…` | `b49afce31a861d7fecf072d43ee863e09f52cc38ac0704af3e3f86964ea68946` |

Commands used for the pins:

```
$ git -C /home/vgpnk/Projects/shokunin show 0c9e9999:.ufo/reports/round-43/mori.md | sha256sum
ea6ac0f6a3ed0d8e49d7bd14789d6a85c3dadd4ee028ae7feead4959ffb0b10a  -
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 1429c791:corpus/lessons/round-43.md | sha256sum
66e273c8386895a505085df57de94c46540877fc01836148d04efad23eb9d495  -
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 1429c791:corpus/lessons/round-43-verifier-spotcheck.md | sha256sum
b49afce31a861d7fecf072d43ee863e09f52cc38ac0704af3e3f86964ea68946  -
```

The lesson is byte-identical at `dde525ea`'s successor tips `efb92cd5` and `91cb221f` and at the
round-44 entering tip `1429c791`; it differs at `dde525ea` (`61f9572a…`), so the quoted lesson
lines are stable from `efb92cd5` onward.

---

## 2. The "15" figure — verbatim report sentences

Source: `git -C /home/vgpnk/Projects/shokunin show 0c9e9999:.ufo/reports/round-43/mori.md`.

**L45** (controls bullet; the sentence the witness's F03 row restates as "15 checks PASS"):

```
  a scratch clone → 15 checks PASS, `C1S=met` exit 0 (`evidence/control-c1s-green.txt`);
```

**L109** (the Before→after table row for C1S; same figure, with the parenthetical PASS list):

```
| **C1S** — operability | `python3 .ufo/waves/round-43/count-c1s.py e3a2b58…` → `check self_at_rev FAIL (absent)` → `C1S=unmet`, exit 1 | `python3 .ufo/waves/round-43/count-c1s.py <tip>` → 15 checks PASS (incl. `noharm_cwd PASS (rc=0 MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0)`, `v5_selftest_17 PASS (pass=17 fail=0 rc=0)`, three `mutant_kill_* PASS (pass=16 fail=1)` on exactly their own arms, `frozen_still_crashes PASS (rc=1 crash=True C1_line=False)`) → `C1S=met`, exit 0 | `dde525ea4a7fca365e8ff2f3c486bccf28b94e52`; receipts `evidence/c1s-after.txt`, `evidence/c1s-clause-map.txt` |
```

**L123** (the limitation paragraph; the counter's own output is restated as "15 PASS lines"):

```
  landed tip the counter prints 15 PASS lines, and the counter's identity is pinned by its
```

Sentence context for L123 (L122–L125), so the clause is not read out of frame:

```
  fewer. This is a statement about the instrument, not about the input: on honest input at the
  landed tip the counter prints 15 PASS lines, and the counter's identity is pinned by its
  sha256 `93482248…` (a mutated copy is not the claim's counter). A stricter reading of the
```

Command that produced the pointers:

```
$ git -C /home/vgpnk/Projects/shokunin show 0c9e9999:.ufo/reports/round-43/mori.md | grep -n '15'
40:  `.ufo/waves/round-43/count-c1s.py` (sha256 `93482248b46def2a2cec7238732af1551ef315517e76833c3843875313b65dc5`);
45:  a scratch clone → 15 checks PASS, `C1S=met` exit 0 (`evidence/control-c1s-green.txt`);
78:  edited) → QUALITY 115. A residual seat's S268 attack added **QUALITY 116** (an "unreachable"
81:  `content-type: text/html`, content-length 15410 (`evidence/s268-headers.txt`); no committed
96:| registry rows S348–S351 + S470, three knowledge entries, the round-43 lesson, QUALITY 115, the coverage-map note, the SCORECARD declaration + correction, the assimilation mirror and its receipt | `dde525ea4a7fca365e8ff2f3c486bccf28b94e52` | same |
109:| **C1S** — operability | … → 15 checks PASS (incl. …) → `C1S=met`, exit 0 | …
123:  landed tip the counter prints 15 PASS lines, and the counter's identity is pinned by its
173:  QUALITY 115 and 116 are lesson-backed.
243:   HTTP 418 / `text/html` / 15410 bytes; no committed PDF; **not re-admitted**, and the probe's
```

(Lines 40, 78, 81, 96, 173, 243 are other "15" substrings — the figure appears as a check count
only at L45, L109 and L123.)

At the earlier revision `484e6eff` the same three sentences sit at **L44**, **L105**, **L119**
and the two witness-relevant sentences hash identically across the two revisions:

```
$ for r in 484e6eff 0c9e9999; do git -C /home/vgpnk/Projects/shokunin show $r:.ufo/reports/round-43/mori.md \
    | grep -E '15 checks PASS, `C1S=met` exit 0|34 seat logs carry' | sha256sum; done
216ba60390ee9ce78ca7c49cb859c57e5265cb12c01985cb06e8b3b4d454c5e0  -
216ba60390ee9ce78ca7c49cb859c57e5265cb12c01985cb06e8b3b4d454c5e0  -
```

---

## 3. The "34 seat logs" figure — verbatim report and lesson sentences

**Report L11–L12** (`git -C /home/vgpnk/Projects/shokunin show 0c9e9999:.ufo/reports/round-43/mori.md`,
sentence continues on the next physical line):

```
in the round. The 64-seat wave was starved by the provider's rate limit (34 seat logs carry
`provider.rate_limit: 429`); 60 of its seats are dead seats and are not credited and were not
```

**Report L210** (dead-seats bullet, second assertion of the same figure):

```
  34 seat logs carrying `provider.rate_limit: 429 Rate limit reached for requests`. Those 60
```

Command:

```
$ git -C /home/vgpnk/Projects/shokunin show 0c9e9999:.ufo/reports/round-43/mori.md | grep -n -E '34|429|rate_limit'
11:in the round. The 64-seat wave was starved by the provider's rate limit (34 seat logs carry
12:`provider.rate_limit: 429`); 60 of its seats are dead seats and are not credited and were not
…
210:  34 seat logs carrying `provider.rate_limit: 429 Rate limit reached for requests`. Those 60
```

**Lesson L132–L133** (`git -C …/mori-shokunin show 1429c791:corpus/lessons/round-43.md`):

```
The 64-seat v2 wave was starved by the provider's rate limit (34 seat logs
carry `provider.rate_limit: 429`); 52 of its seats were then killed by the
```

**Finding (lesson coverage).** The lesson carries the `34` figure (L132–L133) and **does not
carry the `15` figure anywhere**: `git show 1429c791:corpus/lessons/round-43.md | grep -n -E
'15 checks|15 PASS'` returns no match (its only `PASS`/`C1S` lines are L9, L18, L114, L120,
L126–L128, L140–L141, none of which state a check count). So the contract's phrase "exactly as
the round-43 report **and** lesson assert them" holds per-figure, not per-document: F03 (15) is
witnessed against the report alone (L45/L109/L123), F04 (34) against the report (L11–L12, L210)
and the lesson (L132–L133). The closure routes the `15` slip to the report **and** to
`evidence/c1s-mutants.txt`, not to the lesson (see §4, L209).

---

## 4. The closure's observed values (14 and 8) and the commands it used

Source: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 1429c791:corpus/lessons/round-43-verifier-spotcheck.md`.

**Observed value 14 — closure L109–L113** (the closure's command spans two physical lines):

```
Independent counts: `git show efb92cd5:.ufo/waves/round-43/evidence/c1s-after.txt
| grep -cE '^check'` → **14** (14 PASS); the green control
`control-c1s-green.txt` is also **14**. The report's "15 checks PASS" (and
`evidence/c1s-mutants.txt`'s "the healthy counter prints 15") is off by one:
the honest counter prints 14 check lines. The frozen P-C1S sentence's ten
```

**Observed value 8 — closure L209–L212** (§"Routed defects" item 3):

```
3. Count slips in the report and in `evidence/c1s-mutants.txt`: "15 checks"
   should be 14; "34 seat logs carry `provider.rate_limit: 429`" — observed 8
   (`git grep -l 'provider.rate_limit' 91cb221f -- .ufo/waves/round-43/logs`),
   while 39 logs merely contain the string `429` (byte counts, file sizes).
```

**Trends restatement — closure L199–L200:**

```
  counts in the report are wrong (14 checks reported as 15; 8 rate-limited seat
  logs reported as 34) — recognition of its own evidence is not yet exact.
```

Commands the closure used, extracted verbatim from L109–L110 and L211:

1. `git show efb92cd5:.ufo/waves/round-43/evidence/c1s-after.txt | grep -cE '^check'` → `14`
2. `git grep -l 'provider.rate_limit' 91cb221f -- .ufo/waves/round-43/logs` → observed `8`
   (as written this command *lists* the paths; the count 8 is the number of emitted lines —
   no `| wc -l` appears in the closure text)

I re-ran both read-only, at the closure's own revision and at the round-44 tip, and got the
closure's values:

```
$ git -C …/mori-shokunin show efb92cd5:.ufo/waves/round-43/evidence/c1s-after.txt | grep -cE '^check'
14
$ git -C …/mori-shokunin show 91cb221f:.ufo/waves/round-43/evidence/c1s-after.txt | grep -cE '^check'
14
$ git -C …/mori-shokunin git grep -l 'provider.rate_limit' 91cb221f -- .ufo/waves/round-43/logs | wc -l
8
$ git -C …/mori-shokunin git grep -l '429' 91cb221f -- .ufo/waves/round-43/logs | wc -l
39
$ git -C …/mori-shokunin git ls-tree -r --name-only 91cb221f .ufo/waves/round-43/logs | wc -l
72
```

The 39 "merely contain the string `429`" figure and the 72-log wave size both reproduce.

---

## 5. The frozen witness's actual verdict (run, not inferred)

The C1 fixture restates the two figures with `@REV@`-based single `git` pipelines
(`.ufo/waves/round-44/fixtures/figures-r43.tsv`):

```
F03	15	checks	git show @REV@:.ufo/waves/round-43/evidence/c1s-after.txt | grep -cE '^check'
F04	34	wave	git grep -l 'provider.rate_limit' @REV@ -- .ufo/waves/round-43/logs | wc -l
```

Run of the frozen counter (bytes pinned by `evidence/freeze-r44.txt`, unmodified; the pins match
the bytes on disk):

```
$ sha256sum .ufo/waves/round-44/count-c1.py .ufo/waves/round-44/fixtures/figures-r43.tsv
9477824d5eee45f47d49be52902f7bb0cd67a4d038e0ec7e79094c1e71999f83  .ufo/waves/round-44/count-c1.py
51e63f0186c5d8edcfd283edd29de1e6df95a65959611302c03491128f2ce953  .ufo/waves/round-44/fixtures/figures-r43.tsv
```

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ python3 .ufo/waves/round-44/count-c1.py WORK --ledger .ufo/waves/round-44/fixtures/figures-r43.tsv
check ledger_present       PASS (1518 bytes)
check rows_parse           PASS (12 rows)
check row_floor            PASS (rows=12 min=12)
check class_floor          PASS (classes=checks,corpus,evidence,registry,wave min=4)
check commands_reconcile   FAIL (F03 asserted=15 observed=14; F04 asserted=34 observed=8)
rev=WORK
ledger=.ufo/waves/round-44/fixtures/figures-r43.tsv rows=12 classes=checks,corpus,evidence,registry,wave
C1=unmet mismatches=2
exit=1
```

`WORK` mode substitutes the checkout tip as `@REV@` (`count-c1.py:110-111`, `cmd_rev`); the tip
resolved to `7cb59c6891d4f5d0266fe062565f094da835dc84` (`git rev-parse master` == `HEAD`). The
verdict is exactly the contract's declared witness: `C1=unmet mismatches=2`, naming both rows,
with the other ten rows reconciling.

**Revision sensitivity of the witness (observed).** F04's asserted class is only resolvable from
`91cb221f` onward, because `.ufo/waves/round-43/logs` does not exist at earlier revisions:

```
$ git -C …/mori-shokunin cat-file -e efb92cd5:.ufo/waves/round-43/logs
fatal: path '.ufo/waves/round-43/logs' exists on disk, but not in 'efb92cd5'
$ git -C …/mori-shokunin log --oneline --diff-filter=A -- .ufo/waves/round-43/logs
91cb221f round-43: seat logs as wave evidence, frozen-sha mutant receipt
```

Per-revision re-derivation of the two rows (F03 `grep -cE '^check'`, F04 `grep -l | wc -l`):

| rev | F03 observed | F04 observed |
|---|---|---|
| `7cb59c68` (round-44 tip, witness `@REV@`) | 14 | 8 |
| `91cb221f` (round-43 final lane tip) | 14 | 8 |
| `efb92cd5` (after-scores tip) | 14 | 0 (logs dir absent) |
| `dde525ea` (counter/receipt tip) | 0 (`c1s-after.txt` not yet landed) | 0 (logs dir absent) |

So the witness is revision-bound to ≥ `91cb221f`; at any earlier revision F02 (72 logs) and F04
(34) would both read 0. The report itself names `91cb221f` as the revision of "the 72 seat logs"
(`mori.md` L98 in `0c9e9999`: `| the 72 seat logs (each dead seat's last error text), the
frozen-sha mutant receipt | `91cb221f35f7cb9afeff99ef1959512dabddfc46` | …`), which is the
revision the closure's L211 command also names.

**Corroboration that the report's own cited receipt says 14.** The L45 sentence attributes the
"15 checks PASS" to `evidence/control-c1s-green.txt`; that receipt has 14 check lines:

```
$ git -C …/mori-shokunin show efb92cd5:.ufo/waves/round-43/evidence/control-c1s-green.txt | grep -cE '^check'
14
```

and the cited `evidence/c1s-after.txt` opens with
`command: python3 .ufo/waves/round-43/count-c1s.py dde525ea…` followed by 14 `check … PASS`
lines plus `C1S=met` / `exit=0` — i.e. the off-by-one is in the prose, not in the receipt.

---

## 6. Findings (observed vs inference)

Observed (committed bytes + re-run commands):

- The witness's F03 restates report L45 / L109 / L123 (`0c9e9999`); its F04 restates report
  L11–L12 and L210, and lesson L132–L133.
- The two witness sentences are byte-identical at `484e6eff` and `0c9e9999` (sha256
  `216ba603…`), so the `0c9e9999` in-place rewrite (closure item 2) did not alter them; only
  their line numbers moved (L44→L45, L105→L109, L119→L123, L206→L210, L10→L11).
- Closure observed values: 14 (L110) and 8 (L210–L211); closure commands: L109–L110 and L211.
  Both reproduce; the closure's `429` substring figure (39) and wave size (72) reproduce too.
- The frozen counter over the fixture prints `C1=unmet mismatches=2` naming
  `F03 asserted=15 observed=14; F04 asserted=34 observed=8`.

Inference / notes for the round:

- [INFERENCE] The contract's witness sentence ("as the round-43 report **and** lesson assert
  them") is satisfied only if read per-figure: the lesson never states a check count, so F03's
  authority is the report alone. A reader testing the witness against the lesson for the `15`
  figure would find no sentence to match.
- [INFERENCE] The closure's item-3 command for the `8` is a listing command without `| wc -l`;
  the observed value is the line count of its output. It is still one `git` pipeline and it is
  what the fixture's F04 spells with an explicit `wc -l`.
- [INFERENCE] Because the seat-log directory first appears at `91cb221f`, the fixture is only
  meaningful at ≥ `91cb221f`; running it at the entering tip `1429c791` (which contains
  `91cb221f`) or at the round-44 tip both yield 14/8. The fixture header names no revision, so
  the revision binding lives only in the counter's `@REV@` substitution.

Remaining unknowns: none material to the pinned wording. Not investigated here (out of scope):
whether the report's L109 "measured against `dde525ea`" cell conflicts with the closure's item 5
(receipt-at-`dde525ea` vs "landed tip") — that is routed defect 5, already carried by the
round-43 closure.

**Tool installs / updates: none.** No pacman, `uv tool`, `npx`, cargo or binary install was run
for this seat. Scratch work: read-only `git show`/`git grep`/`git ls-tree`/`git cat-file` against
the two checkouts; no sandbox copy was needed and no checkout was mutated.

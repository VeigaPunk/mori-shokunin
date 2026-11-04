# Mo88Sc01Scope — C2 rule-scope reconnaissance (round 88, w1, attempt 1)

Read-only. No lane, OS, unit, service or harness state changed. No subagents, no background jobs.
Lane `HEAD` observed while reading: `9c775ac2131da13c4c4cfdf2b14077184076f557`. All receipt and
counter content read at `d5e2eda494877a85edaa4e287d6ad81843d9a8a1` via `git show`.

## Seat-spec correction (measured, not a claim about the gate)

`.ufo/waves/round-88/count-c2.py` has **no** `POPULATION` symbol (it carries `SUBJECT`, `REAL`,
`FIXTURES`; `SUBJECT = ".ufo/waves/round-87/count-c2.py"`). The seven receipts are
`POPULATION` in `.ufo/waves/round-87/count-c2.py` **L39-47**, which the r88 counter grades. Every
row below is that r87 tuple `(path, expect, declared_mode, token)`, read at `d5e2eda`.

## SCOPE_TABLE (population)

```
SCOPE_TABLE rows=7 applied=4 would_refuse=0
```

`rows` = POPULATION rows. `applied` = rows on which at least one new rule takes its non-default
branch (`declared_replay_problem` with declared ∈ {required, clone} = 4 rows; `binding_problems`
with `replayed=True` = the same 4 rows; 8 row-rule evaluations). `would_refuse` = population rows
the two new rules report a problem on, at their declared modes, measured with the frozen functions.

## 1. The seven rows, as declared

Rules read at `.ufo/waves/round-87/count-c2.py` L133-138 (`declared_replay_problem`) and L140-145
(`binding_problems`); call sites L261-266. Token test = `set(t.strip(";'\"") for t in
re.split(r"\s+", cmd))`, then exact `path in tokens`.

| # | receipt (population path) | sha256 | declared | `# replay:` line | value | `# counter-sha256:` paths (header line) | in `# cmd:` tokens? | `# supersedes:` (line) |
|---|---|---|---|---|---|---|---|---|
| 1 | round-85/evidence/after-r85.txt | `9ff6c459fe6f8164…` | legacy | absent | — | `.ufo/waves/round-85/count-c1.py` (L4); `.ufo/waves/round-85/count-c2.py` (L5); `.ufo/waves/round-85/count-c3.py` (L6) | **yes; NO; yes** | absent |
| 2 | round-85/evidence/record-sweep-r85.txt | `a4b4d0da21d3f8a8…` | legacy | absent | — | `tools/mori-record-sweep.py` (L4) | yes | absent |
| 3 | round-85/evidence/claim-sweep-r85.txt | `7b209ba39591df9e…` | legacy | absent | — | `tools/mori-claim-sweep.py` (L4) | yes | absent |
| 4 | round-86/evidence/after-c1-r86.txt | `dba7eb7aadf0d99c…` | required | L5 | `required` | `.ufo/waves/round-86/count-c1.py` (L4) | yes | absent |
| 5 | round-86/evidence/replay-defeat-r86.txt | `055523561733ed0c…` | required | L5 | `required` | `.ufo/waves/round-86/count-c1.py` (L4) | yes | absent |
| 6 | round-87/evidence/record-sweep-r87.txt | `213a7558e155ea4e…` | clone | L5 | `clone` | `tools/mori-record-sweep.py` (L4) | yes | `record-sweep-r85.txt` (L6) |
| 7 | round-87/evidence/claim-sweep-r87.txt | `429a5dca94d32e14…` | clone | L5 | `clone` | `tools/mori-claim-sweep.py` (L4) | yes | `claim-sweep-r85.txt` (L6) |

Full hashes: 1 `9ff6c459fe6f81640f00f3209734b9aedafe73cd6d1b8f20706e347831a38d71`,
2 `a4b4d0da21d3f8a869d2f919d1990bb1d6ac89026022fde32a2fdbdde755d2f3`,
3 `7b209ba39591df9e5020199997b9b55c29fe2a8fc3c56e415c158e8aef7ed061`,
4 `dba7eb7aadf0d99c80420a6ec223a31cdf8f86460f95cf9ef312bc3b448a2946`,
5 `055523561733ed0cd005e02a756df8e53ce8724ef57fd22625eacab02c8036a3`,
6 `213a7558e155ea4eaeec8472767fa8371b44948e40b59cf9ac8437954641f4ac`,
7 `429a5dca94d32e14bd3614524fd9c441d682ba3986bceda4a98a0a4354a296b8`.

## 2. What the two rules evaluate, per row (measured by calling the frozen functions)

`replayed` is the exact argument at L264: `replay_mode in ("required","clone") or
fields["replay"] is not None`. Replay *execution* has a stricter guard at L295:
`mode in ("required","clone") and fields["replay"] is not None`.

| # | row | replayed flag | `REPLAY` line measured | declared rule applied | binding rule applied | declared result | binding result |
|---|---|---|---|---|---|---|---|
| 1 | after-r85.txt | False | none | no (legacy branch → None) | skipped (`if not replayed`) | None | `[]` |
| 2 | record-sweep-r85.txt | False | none | no | skipped | None | `[]` |
| 3 | claim-sweep-r85.txt | False | none | no | skipped | None | `[]` |
| 4 | after-c1-r86.txt | True | `mode=required rc=0 exported=1` | yes | yes | None (line present) | `[]` |
| 5 | replay-defeat-r86.txt | True | `mode=required rc=0 exported=1` | yes | yes | None | `[]` (row still `failed problems=replay-mismatch`, pre-existing) |
| 6 | record-sweep-r87.txt | True | `mode=clone rc=0 exported=1` | yes | yes | None | `[]` |
| 7 | claim-sweep-r87.txt | True | `mode=clone rc=0 exported=1` | yes | yes | None | `[]` |

Rows replayed (4) match `replay=4` in the r87 target line; rows 1-3 emit no `REPLAY` line.

### 2b. Token-rule false-refusal surface (measured probes, binding path `tools/x.py`)

| `# cmd:` form | `binding_problems(..., replayed=True)` | reading |
|---|---|---|
| `python3 -I tools/x.py` | `[]` | pass |
| `python3 -I "tools/x.py"` | `[]` | pass (double quotes stripped) |
| `python3 -I 'tools/x.py'` | `[]` | pass (single quotes stripped) |
| `python3 -I tools/x.py; rc=$?` | `[]` | pass (`;` stripped) |
| `python3 -I tools/x.py > out.log` | `[]` | pass (space-separated redirection) |
| `cd sub && python3 -I tools/x.py` | `[]` | pass |
| `sh -c "python3 tools/x.py"` | `[]` | pass |
| `python3 --opt=tools/x.py` | `['cmd-binding']` | **false refuse** (`--opt=` not stripped) |
| `python3 -I ./tools/x.py` | `['cmd-binding']` | **false refuse** (`./` prefix) |
| `python3 -I /abs/tools/x.py` | `['cmd-binding']` | **false refuse** (absolute vs repo-relative) |
| `python3 -I tools/x.py>out.log` | `['cmd-binding']` | **false refuse** (no space before redirect) |
| `python3 -I tools/x.py,` | `['cmd-binding']` | **false refuse** (trailing comma) |
| `python3 -I $(pwd)/tools/x.py` | `['cmd-binding']` | **false refuse** (substitution prefix) |
| `python3 -I "tools/x.py --flag"` | `[]` | accidental pass: whitespace split yields bare `tools/x.py` inside the quoted argument |

`strip(";'\"")` strips only `; ' "` at token ends; there is no shell-word parsing, no `--opt=`
split, no path normalization, no quote awareness.

## 3. Blast radius — receipts outside the population

Universe at `d5e2eda`: **933** `.ufo/waves/**/evidence/*.txt` files; **13** contain a standalone
`^#\s*---\s*$` separator. 13 − 7 population = **6** candidates. Each evaluated two ways: (a) as the
mode its own header declares (replay line present → that mode, absent → legacy), (b) forced to
`required`/`clone` (the only way a new row joins the r86/r87 pattern).

| receipt | sha256 (short) | own declaration | new-rule result (a) | forced required/clone (b) | rule | line |
|---|---|---|---|---|---|---|
| round-86/evidence/after-r86.txt | `24bdd6bef789c2b2` | no `# replay:` (header L1-7) | pass | **refused** | `declared_replay_problem` → `missing-replay` | no `# replay:` between `# counter-sha256: …count-c3.py` (L6) and `# limits:` (L7); 3 bindings L4-6 all tokens of L2 cmd; no `# supersedes:` |
| round-87/evidence/after-r87.txt | `282513c086df2531` | `# replay: clone` (L6) | pass | pass | — | 2 bindings L4-5 both tokens of L2 cmd; no `# supersedes:` |
| round-85/evidence/c3-controls.txt | `a4cc4c379d12c451` | no receipt grammar (header L1-19: no `# cmd:`, `# rev:`, `# counter-sha256:`, `# replay:`) | pass (new rules silent) | **refused** | `declared_replay_problem` | no `# replay:` in header L1-19 (also fails pre-existing `rev`/`summary`, not a new-rule effect) |
| round-85/evidence/controls-r85-defeated.txt | `a1ff4abde8fb661c` | same shape (header L1-25) | pass | **refused** | `declared_replay_problem` | no `# replay:` in header L1-25 |
| round-85/evidence/controls-r85-entering.txt | `2b9ecbf12461720c` | same shape (header L1-8) | pass | **refused** | `declared_replay_problem` | no `# replay:` in header L1-8 |
| round-85/evidence/controls-r85.txt | `ed772b44c89fc9fd` | same shape (header L1-4) | pass | **refused** | `declared_replay_problem` | no `# replay:` in header L1-4 |

Counts: (a) **0** of 6 refused by the new rules; (b) **5** of 6 refused, all `missing-replay`
(`after-r86.txt` + the four r85 controls receipts); `after-r87.txt` passes both ways.

Two further sweeps over the same 933 files, at `d5e2eda`:

| sweep | result |
|---|---|
| every `# replay:` line in the tree | 5 total, all parse-clean: `after-c1-r86.txt:5 required`, `replay-defeat-r86.txt:5 required`, `after-r87.txt:6 clone`, `claim-sweep-r87.txt:5 clone`, `record-sweep-r87.txt:5 clone`. Zero `# replay: legacy`, zero `# replay: none` in real bytes |
| every `# supersedes:` line in the tree | 2 total, both population rows (`record-sweep-r87.txt:6`, `claim-sweep-r87.txt:6`), both targets present → `SUPERSEDE … absent=1` blast radius outside the population is **0** |

**Latent token-rule refusal inside the population:** population row 1 (`after-r85.txt`) binds
`.ufo/waves/round-85/count-c2.py` (header L5) but its `# cmd:` (L2) runs only `count-c1.py` and
`count-c3.py`. Declared `legacy`, the row skips the binding rule; if row 1 ever moved to
`required`/`clone`, the fixed counter would print `problems=missing-replay,cmd-binding` and refuse a
receipt whose `# limits:` deliberately records C2's bytes as pinned-not-run. This is the **only**
path/token mismatch among the 933 files.

## 4. False-accept the token rule does not close (calibration, measured)

`binding_problems` checks token presence, not execution. Measured pure-function passes:
`printf 'RECORD_SWEEP fabricated=1' # tools/x.py`, `echo tools/x.py`, `cat tools/x.py`,
`grep -c '' tools/x.py`, `true tools/x.py` → all `[]`.

End-to-end fixture (scratch `--shared` clone at `d5e2eda`, toplevel asserted, commit with
`-c user.name=t -c user.email=t@t`): `record-sweep-r87.txt` body replaced with
`RECORD_SWEEP fabricated=1` and `# cmd:` replaced with
`printf 'RECORD_SWEEP fabricated=1\n' # tools/mori-record-sweep.py`. The frozen r87 counter graded
that fixture **`RECEIPT record-sweep-r87.txt expect=met met problems=-`** and
**`C2=met … matched=6 … superseded=2 legacy=1 unexpected=0`**, rc 0 (fixture rev `0aed255d`).
So the frozen `vacuous` shapes are refused, but the *class* "`# cmd:` prints its own body" is not:
one trailing shell comment carrying the bound path defeats `cmd-binding`.

## 5. `corpus/knowledge/receipt-counterfeit-r88.md` vs this table

Doc read from the worktree (`d4a4456d5931cbebee805f90ae61fc494766fe2bcb10fed2e14648a0385b3956`);
it is **absent** at `d5e2eda` (untracked). Code cited below is the frozen r87 counter.

| # | doc claim | measured | verdict |
|---|---|---|---|
| 1 | Rule 1: "A row declared `required` or `clone` whose receipt has **no `# replay:` line** is `missing-replay`." | `# replay: none` + valid `# no-replay:` reason parses with `fields["replay"] = None` (L120-126) and `declared_replay_problem("clone", …)` returns `missing-replay`. The line **is** present. | contradicted by wording; code condition is `fields["replay"] is None`, which includes `none` |
| 2 | Rule 2: "On a **replayed** row …" and Limits: "`binding_problems` is deliberately scoped to rows that are replayed." | `replayed` (L264 arg) is True for a declared `required`/`clone` row with no replay line, while replay execution (L295) does not run. Measured on `after-r85.txt` forced to clone: `declared='missing-replay'` **and** `['cmd-binding']` on a row that never replays. | contradicted: "replayed" in the rule ≠ "a replay runs"; refused rows can carry both new problems |
| 3 | "source: the lane's own gate output `.ufo/waves/round-88/evidence/after-r88.txt` (receipt met at `d5e2eda…`)" | `git cat-file -e d5e2eda:.ufo/waves/round-88/evidence/after-r88.txt` fails; the file is worktree-only/untracked, sha `31678d6296ba6c2226dcb77a566ee6e9324a2e7d9d1a1c8aca25edc46754a380`, and its body prints `C2=met … rev=d5e2eda49487`. | provenance contradicted (artifact not in the graded tree); its numbers reproduce |
| 4 | Section header "**A bound counter is named by the command**" + "a command such as `printf '<body>'` reproduces any body" (implying `cmd-binding` closes it) | `printf 'RECORD_SWEEP fabricated=1\n' # tools/mori-record-sweep.py` is admitted `met` by the same counter (§4). The path is *named* but never executed. | overstated claim contradicted by measurement; the rule checks naming, not execution |
| 5 | `recheck: python3 -I .ufo/waves/round-88/count-c2.py d5e2eda4` prints `C2=met … arms=23` | my run at `d5e2eda…` printed `C2=met real=met fx=4 clean=1 refused=2 absent=1 arms=23`, rc 0 | corroborated, no contradiction |

## 6. Commands and hashes actually read

| purpose | command | observed |
|---|---|---|
| lane HEAD | `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD` | `9c775ac2131da13c4c4cfdf2b14077184076f557` |
| frozen counter hash | `git show d5e2eda…:.ufo/waves/round-87/count-c2.py \| sha256sum` | `7e577f533e1dac676d3f5b3d601f2c4c622c57c325e6091e6018b5781ae73fc0` (identical in worktree) |
| r88 counter hash | `sha256sum .ufo/waves/round-88/count-c2.py` | `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7` |
| r88 c1 / contract / controls | `sha256sum …` | `3ba0f97baaae389e…` / `bc154e2b065b3455…` / `7b53d4aa87e79b4c…` |
| row table + rule application | import of the frozen counter as a module, then `header_and_body` → `header_fields` → `declared_replay_problem` / `binding_problems` with `replayed` computed exactly as L264 | §1, §2 above |
| per-row gate lines | `python3 -I .ufo/waves/round-87/count-c2.py d5e2eda… --scratch $S/r87run` | 7 `RECEIPT` lines + 4 `REPLAY` lines; `C2=met … replay=4 …`, rc 0 |
| r88 verdict recheck | `python3 -I .ufo/waves/round-88/count-c2.py d5e2eda… --scratch $S/c2run` | `C2=met real=met fx=4 clean=1 refused=2 absent=1 arms=23 rev=d5e2eda49487`, rc 0 |
| separator census | `git ls-tree -r --name-only d5e2eda \| grep '^\.ufo/waves/.*/evidence/.*\.txt$'` then per-file `grep -cE '^#\s*---\s*$'` | 933 files, 13 with a separator |
| false-accept fixture | `git clone --shared <lane> $S/fa/repo`; `git -C "$D" rev-parse --show-toplevel` = `$D` asserted; rewrite cmd+body; `git -C "$D" -c user.name=t -c user.email=t@t commit`; graded with the frozen r87 counter | `FX=0aed255dbc4b71fe8e4c12eba52f4eb662a63e2a`; `RECEIPT record-sweep-r87.txt … met problems=-`; `C2=met`, rc 0 |

Scratch was `/fast/scratch/hyaku/mori-r88/Mo88Sc01Scope` and is deleted after this report; no
`/tmp` path is cited. Tools installed/upgraded: none. Deviation disclosed: one throwaway redirect
(`git show … > /tmp/x`) was issued and the file deleted in the next command; it produced no cited
value.

## Verdict measured

Both new rules are silent on all seven population rows at their declared modes
(`SCOPE_TABLE rows=7 applied=4 would_refuse=0`), and the frozen r88 counter reproduces the r87
target line with `arms=23` (my run, rc 0). The rule's blast radius across the lane's separator
receipts is one real row class — a receipt lacking `# replay:` that a future population declares
`required`/`clone` (`after-r86.txt` is the existing instance; 5 of 6 candidates refuse that way) —
plus one latent in-population token mismatch (`after-r85.txt` L5, masked by `legacy`) and one
measured false accept (§4, the bound path named in a shell comment is admitted `met`).

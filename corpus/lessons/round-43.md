# Round 43 lesson

author: Kimi fresh L1 (mori-r43). Seats this lane dispatches are still the lane.

Inherited: the same round's earlier attempt (which died on a provider-route
failure) left the contract, the two counters, the wave spec, the SOURCES rows
and the knowledge entries in the working tree, uncommitted. This L1 re-executed
every control, opened every source it found unopened, and disposed of that
output before continuing. Nothing was re-declared: P-C1S and P-C2 are the
frozen claims in `.ufo/waves/round-43/contract.md`.

## Gate

Opened 2026-10-24.

- S348 — https://docs.python.org/3/library/subprocess.html#subprocess.run —
  quote (signature line): "shell=False, cwd=None, timeout=None, check=False,
  encoding=None, errors=None, text=None, env=None". Grounds C1S. used-by
  `corpus/knowledge/c1s-cwd-r43.md`. recheck `90d`. status mined.
- S349 — https://www.openeuler.org/whitepaper/openEuler%2024.03%20LTS%20%E6%8A%80%E6%9C%AF%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf —
  committed copy `corpus/evidence/sources-r42/S235.pdf`, sha256
  `9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020`.
  Supersedes S235 (its anchor cell transposed two characters of that sha; the
  S235 row is not rewritten). used-by
  `corpus/knowledge/s235-sha-correction-r43.md`. recheck `180d`. status mined.
- S470 — https://www.freedesktop.org/software/systemd/man/latest/journalctl.html —
  quote (Commands section, `--disk-usage`): "Shows the current disk usage of all
  journal files. This shows the sum of the disk usage of all archived and active
  journal files." Admitted entry
  `corpus/knowledge/journal-disk-usage-total-r51.md`. recheck `180d`. Same URL
  as S014, different scope (W04, not E04). status mined.
- S350 (rejected) — https://www.freedesktop.org/software/systemd/man/latest/systemd.scope.html —
  quote (Description): "Scope units may still enter a failure state, for example
  due to resource exhaustion or stop timeouts being reached". Opened this round
  by this L1 (the inherited row claimed the page without opening it). Rejected:
  the staged entry's recheck is `systemctl reset-failed` after creating a scope,
  which is host mutation outside mori's detection-and-report province. Flip: a
  read-only `MemoryMax` show of an already-failed scope, no `reset-failed`, no
  scope creation. recheck `180d`. status rejected.
- S351 (rejected) — https://www.freedesktop.org/software/systemd/man/latest/journalctl.html —
  quote (Commands section): "--vacuum-size= removes the oldest archived journal files
  until the disk space they use falls below the specified size". Rejected: the
  staged `journal-reach-at-ceiling-r46.md` grounds itself in a shokuknow
  `file://` note and a kernel `MESSAGE` grep, neither of which this lane may
  treat as evidence. Flip: the public `--vacuum-size=` sentence plus a committed
  read-only disk-usage receipt, and no MESSAGE grep. recheck `180d`. status
  rejected.

Admit: `journal-disk-usage-total-r51.md` (theme: what `--disk-usage` counts) —
one entry, one theme.

Reject: `journal-reach-at-ceiling-r46.md`. Reason: cites a shokuknow `file://`
note and a kernel MESSAGE grep. Flip: public `--vacuum-size=` sentence plus a
committed disk-usage receipt, no MESSAGE grep. Row S351, status rejected.

Reject: `failed-scope-keeps-limit-r50.md`. Reason: recheck is
`systemctl reset-failed` after creating a scope (host mutation). Flip: read-only
`MemoryMax` show of an already-failed scope, no `reset-failed`, no scope
creation. Row S350, status rejected.

S268 not re-admitted. `curl -sI` of the stampPDF URL returned HTTP 418,
`content-type: text/html`, content-length 15410
(`.ufo/waves/round-43/evidence/s268-headers.txt`). No committed PDF, so no
re-gate: the flip condition ("a fetch this host can reproduce") is not met.

Search log: subprocess.run signature (admitted S348); journalctl `--disk-usage`
(admitted S470); systemd.scope(5) failure-state sentence (rejected S350);
journalctl `--vacuum-size=` (rejected S351); stampPDF (still 418, not admitted).

### Assimilation (item 10)

One theme, one entry: what `journalctl --disk-usage` counts. The package
`/home/vgpnk/Projects/shokuknow/merge/mori/` was read read-only; no campaign
tool was run there; no byte was written into it.

- Collision check before any append: registry 238 ids vs staged 127 ids →
  `collisions` empty (`.ufo/waves/round-43/assimilation/collisions`). The
  indented-row guard was proven on a scratch fixture: the column-zero pattern
  hits 0 rows, the 0–3-space pattern hits `S348`
  (`assimilation/guard/col0-ids`, `assimilation/guard/wide-ids`).
- Transformation in scratch before the append: `recheck` normalized to `90d` /
  `180d`; `used-by` set to exactly the admitted entries citing the row; `status`
  `mined`; no cell contains a literal or escaped `|`; the staged S470 row's
  prose recheck cell and its `**`-marked teaches were rewritten into the fleet
  schema (`assimilation/append-block.md`).
- Validate-before-append: the lane was mirrored in scratch (entering-tip
  `corpus/` + the append block in the Registry table + the admitted knowledge
  files at their repo-relative paths) and gated with
  `sources-census.sh validate --file …/assimilation/validate/corpus/SOURCES.md`
  → **exit 0** (warnings only) before the first registry append
  (`assimilation/validate-receipt.txt`, 243 rows).
- Quarantine slice of the campaign's absent-defect register: `S244`, `S262`,
  `S268` — all three carry the prose class "could not be fetched", so all three
  are unverifiable, not fabrication. S268 is refused above. S244 is cited by no
  admitted entry and is not appended. S262 was admitted in round 42 on the
  OpenAlex deposited abstract and is not re-opened here.
- Post-append guard: `comm -12 reg-ids-post staged-ids` → 5 ids
  (`assimilation/guard/collisions-post.txt`). S470 is the same document
  (journalctl(1) manual page) and keeps its id. S348–S351 are lane-owned rows
  that hold ids the campaign had provisionally assigned to four other
  documents (gihyo 61, gihyo 56, iSulad `supervisor.c`, the openEuler
  whitepaper). The registry is append-only and authoritative, so the lane ids
  stand and the staged ids are shadowed; the shadow map by document is recorded
  in the same receipt for the campaign's next adoption round. The id follows
  the document, never arithmetic.

### considerthese (item 10, one proposal)

`considerthese/2026-10-24.md` (operator-authored, read-only, not edited) —
"Check that frozen instruments replay off-host" — mined as QUALITY 115: a
frozen instrument's green control must replay with `--repo` pointing at a
scratch clone, not only at a hardcoded home path. The pointer is the r40
`conform.py` hardcoded `LANE`; the evidence is this round's green control, which
runs `count-c1s.py <scratch-rev> --repo <scratch-clone>` and prints `C1S=met`.

## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | counter never executed end-to-end before freeze (inherited r42) | `corpus/lessons/round-42-verifier-spotcheck.md` C1 TypeError, no `C1=` line | none at r42 freeze; QUALITY 115 after this round | successor counter's green control must print `C1S=met` on a scratch clone before the lane after-score; shown able to fail by the entering-tip do-nothing (`C1S=unmet`) |
| M2 | self-assessment left a rejected after-cell standing | SCORECARD round-42 declaration still said `C1=met` after the closure | round-43 `count-c2.py` (`declaration` vs correction line) | append-only correction line; in-place rewrite of the cell fails `declaration_unrewritten` |
| M3 | transposed sha called byte-identical | S235 anchor `a30cda99` vs PDF `a30dca99` | round-43 `count-c2.py` `correction_row` | new row S349 (`supersedes S235 —`); the S235 teaches cell is not rewritten |
| M4 | registry row written for a source that was never opened (inherited from the dead attempt) | inherited S350 row read "systemd.scope(5) not re-opened this round" | CORPUS.md SOURCES rule 1 ("a row is written only after opening the source in the round that writes the row") | this L1 opened systemd.scope(5) (quote above), rewrote the row in the lane's `REJECTED: <reason>; flip: <flip>` form, and recorded the access date in this Gate; the guard is the census's exit-0 plus this Gate's per-row quote |
| M5 | dispatcher's `wait` ran inside a pipeline subshell and returned before the seats were visible to that shell | `/tmp/mori-r43-launch.log` printed `SEATS 0` and `SETTLED … lines 0` at the same second while 64 `kimi --agent-file` processes were running | none in the lane; the sibling lane hit the same launcher bug on 2026-10-24 | a waiter parent that spawns nothing stays alive until every seat process has exited (`/tmp/mori-r43-waiter.sh`); the wave is one dispatch, not two |

M1's fix is shown able to fail: `count-c1s.py e3a2b58` prints `C1S=unmet`
because the successor is absent. A planted `print("C1S=met")` also prints
`C1S=unmet`.

## Wave findings (the round's own seats — still the lane, not a reviewer)

The 64-seat v2 wave was starved by the provider's rate limit (34 seat logs
carry `provider.rate_limit: 429`); 52 of its seats were then killed by the
540 s seat timeout and 4 wrote reports. A residual call of 8 reviewer/critic
seats (the contract's ≤8 allowance), staggered two at a time with a 1200 s
timeout, delivered the attack evidence the starved wave could not.

| seat | attack | verdict | what it establishes |
|---|---|---|---|
| `ResCritDoNothing` | do-nothing replay of the entering tip | the counter prints `C1S=unmet` exit 1 | the claimed after-state is not reachable without the work |
| `ResCritJunk` | a counter whose body only prints `C1S=met` | **SURVIVED** (the attack failed): `self_at_rev FAIL (bytes differ)` → `C1S=unmet` exit 1 | self-attestation cannot flip the claim |
| `ResCritInPlace` | rewriting the S235 row's anchor cell in place | the counter scores the mutant `C2=unmet` | the S235 row is not rewritten |
| `ResCritNoHarm` | the no-harm arm (append-only gate selftest) | **CONFIRMED**: `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` exit 0, 3/3 of the gate's own mutants killed | the no-harm arm is non-vacuous |
| `ResCritS268` | re-fetching the S268 stampPDF endpoint | **SURVIVED** (the refusal stands): HTTP 418, `text/html`, 15410 bytes; no committed PDF for that source | S268 stays refused |
| `ResCritScope` | host-mutation grep over the round's diff | **no executable vector** — every hit is a refusal record or prose quoting a paper | detection-and-report scope held |

`ResCritS268` also produced a defect in this round's own method: the S268
refusal rests on a HEAD probe (`curl -sI`), and a HEAD-only probe cannot
distinguish a mitigation page from an endpoint that refuses HEAD but serves
GET. That became QUALITY 116; the refusal itself stands on the absence of any
committed PDF, not on the probe's completeness.

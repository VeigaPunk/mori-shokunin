# Mo58Reviewer05 — C2 quote-binding attack on frozen `count-c2.py` (round 58, wave 1)

Seat: reviewer, C2 depth attack. Freeze revision `fe8801120a67c1a6b8899d7d0423839caa09e7d0`;
entering `b783d0b892637ce8d20f188cad20e4d8913ca635`. Detection/report only — no production,
registry, SCORECARD, LOG, or lane-VCS writes; no fleet/sibling writes.

## Method (bounded)

- Read `contract.md` and both frozen counters first. Attacked only `count-c2.py` (C2 is my seat scope).
- Fixture repos built under `/fast/scratch/hyaku/mori-r58/Mo58Reviewer05/fx/<case>`; every git call
  was `git -C <fixture>`; fixtures committed only inside their own scratch repos. TMPDIR set to the
  seat scratch. Scratch cleaned after receipts were embedded here.
- The frozen counter was mirrored **byte-identically** into each fixture at
  `.ufo/waves/round-58/count-c2.py` (its `LANE` constant derives from its own path, so this aims the
  frozen bytes at the fixture repo without editing them). Mirror equality asserted per build.
- No LSP server/device is mounted for this seat (recorded per reviewer protocol); the predicate is
  behavioral, so evidence is direct fixture execution rather than static checks.

## Integrity checks (all passed)

| Check | Result |
|---|---|
| Frozen counter blob sha256 | `aab888ad787964f7a153d64d85dafa58f652f977e21e22eaa492706a691010d3` |
| Lane worktree counter == freeze blob | `True` (kill-rule intact) |
| Real tool `tools/mori-driver-liveness.py` @ freeze | sha256 `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997`, 18347 bytes, pure UTF-8 |
| Frozen `--selftest` on mirrored bytes | rc=0, `C2_SELFTEST pass=6 fail=0` |
| Lane @ entering `b783d0b8…` | rc=1, `C2=unmet entry=absent failed=entry` (contract before-control reproduced) |
| Lane @ freeze `fe88011…` | rc=1, `C2=unmet entry=absent failed=entry` (entry not in freeze commit; target output is post-landing) |
| Harness validity control `C0fix` | rev `191ba12c…`, `C2=met claims=8 located=8 … failed=none` — conformant fixture scores met |

## Findings by severity

### F1 — HIGH: `claims` counts bullet lines, not distinct claims; duplicate K numbers and even a single repeated fact score met
- `A2` (8 bullets all `**K1**`, **identical** quote and line): rev `0190cc6e84cd4938e95c5c6389f50d1fd7f62259` → `C2=met claims=8 located=8 … failed=none`, exit 0.
- `Afix` (8 bullets all `**K1**`, 8 distinct facts): rev `7d742dff4ef32ba8012c32a4b8b9dfd052b4f46f` → `C2=met claims=8 located=8`.
- Cause: `KLINE`'s K-number group is captured but never checked for uniqueness or sequence; `claims += 1` per matching line. The contract's "≥8 located claims" is enforced as "≥8 K-lines", so one fact repeated 8× satisfies the depth claim's arithmetic.

### F2 — HIGH: fabricated backtick spans coexist with `met` as long as one other span on the line binds
- `FB`: every claim line contains the fabricated 35-char quote `` `def execute_launch_pipeline_stage(i)` `` (absent from the copy, asserted) plus a real 14-char span `` `loop-guard-pad` ``; rev `46cfe07b5fd9a1975f5cf1d497bf1ef40c18e216` → `C2=met claims=8 located=8`.
- Cause: `any(len(s) >= 12 and s in copy_lines[lineno-1] for s in spans)` — one binding span launders any number of fabricated ones. The junk control only fails when **all** spans on a line are absent.

### F3 — MEDIUM: the 12-char quote floor is content-free — whitespace alone binds
- `Efix`: span is exactly 12 spaces (indentation) on lines 11,14–20; rev `29ab416fc19d719667faff5a994b18b8633df5eb` → `C2=met claims=8 located=8`. "Quote-bound" is satisfiable with zero semantic content; the floor measures length, not evidence.

### F4 — MEDIUM: "located" does not establish line-correct attribution; demonstrated on the REAL tool bytes
- Real tool at freeze contains **1450** repeated cross-line substrings ≥12 chars (largest: 77 chars shared by L283/L295: `            and lane.get("completes") == 1 and lane.get("in_flight") is False`).
- `B_real`: 8 claims, each quoting a fragment that comes from line *i* but cited at line *j* (fragment present on both); fixture tool+copy = real freeze bytes; rev `a1ebe6421a2c68945ff28acde85d9edecdc96fae` → `C2=met claims=8 located=8 copy=ok tree=ok`.
- Synthetic control set: wrong-line where the quote is absent from the cited line → `unmet located=0` (rev `4399251977…`); wrong-line where a repeated run covers both lines → `met` (rev `23574e27…`).
- Classification: this matches the frozen predicate exactly (span ∈ cited line), so it is a **predicate-scope limitation, not implementation divergence** — but on the real artifact, "located=8" is achievable with systematically misattributed claims. Worth a lesson note: *located ≠ uniquely attributed*.

### F5 — MEDIUM: `sources` arm is whole-entry string presence, not frontmatter position
- `Cfix`: no frontmatter block; the four required strings sit in body prose ("… we note source: S550 and verified-at: 2026-10-27; … recheck: 90d … coverage-map: FR5 …"); rev `f2a0de94a8bfd83edd300e199a3614a0aa7a309b` → `C2=met … sources=ok`. Contract says "frontmatter lines"; the counter accepts them anywhere in the entry.

### F6 — MEDIUM: `used-by` substring match accepts a stale filename
- `Gfix`: registry row's used-by cell = `corpus/knowledge/driver-events-r58.md.bak (superseded copy)`; rev `222bc324597ee312e8fa612eaaaa2204206b3fe8` → `C2=met … rows=ok`. `ENTRY not in cells[11]` passes for any cell merely containing the path as a substring.

### F7 — MEDIUM (latent): non-UTF-8 byte crashes the counter with exit 1 — colliding with the `unmet` exit code
- `D`: one `0xFF` byte in the pinned copy → rc=1, **stdout empty** (no `C2=` line), stderr `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 40`. `D2`: same with `0xFE` in the tool. Cause: `_show` uses `subprocess(text=True)` (strict decode); `_sha256` hashes decoded text, not raw bytes.
- Byte-identity is sound for decodable files (decode→encode round-trips), and the real tool at R is pure UTF-8, so this is not exploitable at R today. But a crash is indistinguishable from a legitimate `unmet` by exit code alone; consumers keying on rc misread it. Any `C2=`-shaped output check must require the `C2=` line, not just rc.

### F8 — LOW: invalid revision misdiagnosed as missing entry
- `F`: counter run with rev `000…0` → `C2=unmet entry=absent failed=entry`, rc=1. A setup-class failure (rev does not exist) is reported in the same shape as a data failure.

## No-counterexample results (attack directions that correctly fail)

| Attack | Result |
|---|---|
| Quote absent from cited line (`B_syn_outofrange`, rev `4399251977…`) | `C2=unmet claims=8 located=0 failed=quotes`, rc=1 ✓ |
| Short substrings only (9-char `parse_log` spans, rev `c1f7e1f1…`) | `C2=unmet located=0 failed=quotes` ✓ — the `len>=12` gate holds (independently re-confirmed when my own wave-1 fixture's 11-char `return None` spans failed to bind, located=5 → unmet) |
| Drifted copy sha (selftest `copy_sha_mismatch`) | `copy=bad` → unmet ✓ (frozen selftest) |
| Missing frontmatter strings entirely (selftest `missing_frontmatter`) | `sources=bad` ✓ (frozen selftest) |
| Duplicate S550 rows → `rows=bad`; row without used-by → `rows=bad` | verified by frozen selftest arms (design-read + selftest; not separately re-fixtured) |

## Residual risk & verification gaps

- Not fixture-tested: K-lines inside fenced code blocks (claims counting is line-scan based, so inflation via example blocks is plausible but unverified here); multi-locator lines (greedy `.*` takes the last locator — design-read only); locale-dependence of F7 (tested under this host's UTF-8 locale only).
- Findings show the counter's false-green resistance for the `claims`/`quotes`/`sources`/`rows` arms is weaker than the §9 do-nothing controls suggest (every control uses wholly-absent quotes/strings). They do **not** show the real entry is junk; the landed `driver-events-r58.md` may be perfectly genuine — F1–F6 bound what the frozen counter can *prove* about it.
- I ran only freeze and entering revisions; lane tip state was out of seat scope.
- Advisory (no edit made, per seat bounds): a lesson note recording that `located` is presence-on-cited-line (F3/F4), `claims` is bullet count (F1), `sources`/`rows` are substring checks (F5/F6), and that rc must be paired with the `C2=` output line (F7) would right-size the claim's evidentiary weight. No kill condition is met: frozen bytes, predicate, and target outputs are intact and the counter behaves as specified on every §9 control.

## Verdict

Counter executes as frozen and passes its own selftest and both contract controls; no counterexample to the *frozen predicate as written*. Eight demonstrated gap classes (F1–F8, seven with fixture revisions and exact counter output) show the C2 depth claim's evidentiary floor is low: duplicate-numbered, content-free, partly fabricated, and misattributed quote entries all score `C2=met`. Recommend recording the gaps in the round lesson; no contract or counter change proposed from this seat.

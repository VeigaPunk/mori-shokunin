# FamRosterFields: C1 falsification of six roster-field tokens

## Verdict: HOLDS

All six classifications (`census-schema-change`) survive independent re-derivation. Every cause pointer holds: the emitter at `tools/mori-census.sh:2552`, the introducing commit `1f07f1d`, the absence from `baseline-r10-20261015T2231Z.json:22`, and `corpus/knowledge/roster-truth-r12.md:19,21`. No token is `census-regression`, so the re-pin gate is not affected by these six.

Residuals R1-R2 and wording defects W1-W3 below change no class. They need L1 disposition, and R1 needs routing to the census owner.

Scope: rows `+conf_dropped_n`, `+conf_n`, `+roster_n`, `+roster_source`, `+state_dropped_n`, `+state_n` in `corpus/evidence/drift-classification-r20.json`. All six carry identical reason and evidence text.

Measured state: lane HEAD `8f8c58e`. `tools/mori-census.sh` sha256 `87b8d680…ab28`, equal to worktree and HEAD (`git status --short -- tools/mori-census.sh` empty). Pin commit `5be8943` blob sha `d7710981…`, equal to the baseline header `census_sha256` and to `1f07f1d^`. `1f07f1d` blob sha `3da5b098…`.

## 1. Per-token verdicts

| token | register class | verdict | cause pointers re-derived | residual |
|---|---|---|---|---|
| +conf_dropped_n | census-schema-change | AGREE | 2552 emits key; -S key form to 1f07f1d only; baseline:22 lacks key; roster-truth:19,21 | R1 (value undercount) |
| +conf_n | census-schema-change | AGREE | same | R2 (value moved 20 to 23, not a token) |
| +roster_n | census-schema-change | AGREE | same | none |
| +roster_source | census-schema-change | AGREE | same | none |
| +state_dropped_n | census-schema-change | AGREE | same | R1 applies to conf side only |
| +state_n | census-schema-change | AGREE | key-form -S to 1f07f1d only | R4 name collision (see section 2, P2) |

Each token's presence is a schema change, not a value change. The key is absent from the r10 baseline silence line and added by a declared r12 emitter change. This matches the closed-class definition in `corpus/knowledge/drift-repin-r20.md:26-28` ("intended, declared emitter change").

## 2. Pointer checks (observed)

**P1. `tools/mori-census.sh:2552` (HEAD).** The only `emit_surface silence` call in the file (`_grep`, one match).
```
2552: emit_surface silence "$st" "cmd=$cmd; roster_source=$ROSTER_SOURCE roster_n=$ROSTER_N conf_n=$CONF_N state_n=$STATE_N conf_dropped_n=$CONF_DROPPED_N state_dropped_n=$STATE_DROPPED_N; silent=$n_silent ...
```
The emit is unconditional. `resolve_roster` runs at 2512 inside `probe_silence` (2509), and no `return` sits between 2509 and 2552.

**P2. Introducing commit `1f07f1d`.**
- `git log -S'<key>=$<VAR>' -- tools/mori-census.sh` for all six keys returns only `1f07f1d` (exit 0 each).
- `git show 1f07f1d -- tools/mori-census.sh` hunk `-181/+182`: the old emit `-181` lacks the six keys; the new emit `+182` carries them.
- Emit line by revision: `5be8943:1446` (no keys), `1f07f1d:1571` (keys), `HEAD:2552` (keys).
- `git log -G'emit_surface silence' -- tools/mori-census.sh` returns `1f07f1d, 1439c47, 7ca17b1`. Nothing after `1f07f1d` touches the emit line.
- `git log -G'ROSTER_SOURCE|ROSTER_N|CONF_N|STATE_N|CONF_DROPPED_N|STATE_DROPPED_N|roster_ids' -- tools/mori-census.sh` returns `1f07f1d` only.
- `git log -L '/^resolve_roster() {/,/^}/'` returns `1f07f1d` only; the function was created there.
- `1f07f1d^` (scratch copy): zero matches for `roster_source=`, `roster_n=`, `conf_n=`, `conf_dropped_n=`, `state_dropped_n=`. `state_n=` matches only two local assignments (lines 547, 590).
- R4 name collision: bare `git log -S state_n` also returns `7ca17b1` and `9738f1a`. Those commits change the watchdog-probe local `state_n` (output key `state_rounds=`), never a `state_n=` key. The key-form pickaxe returns `1f07f1d` only. The intro attribution holds, but it must be made in key form.
- `probe_silence` was also edited by `273aa74` (r17; `-L` history: `273aa74, 1f07f1d, 1439c47, 7ca17b1`). That edit adds per-lane finding emits in the loop (census:2533-2545). The silence emit line and the roster code are untouched.

**P3. Baseline `corpus/evidence/baseline-r10-20261015T2231Z.json:22`.**
```
SURFACE silence: ok (cmd=git -C <repo> log ...; silent=<V> progressing=<V> progressing_weak=<V> young=<V> not_open=<V> unavailable=<V> skipped=<V> window_s=7200; ts=<V>)
```
None of the six keys. Whole-file `_grep` for `roster|conf_n|state_n|conf_dropped_n|state_dropped_n` returns "No matches found". The file blob sha equals `5be8943`'s blob (`0993b235…`), `git status` is clean, and `5be8943` is its only commit.

**P4. `corpus/knowledge/roster-truth-r12.md:19` (raw).** Names `roster_source` (`conf+state`, `conf`, `state`, `builtin`), then `roster_n`, `conf_n`, `state_n`, `conf_dropped_n`, `state_dropped_n` on the aggregate row. Line 21: roster fields are "deliberately absent from the r10 volatile list: changes remain visible to `--drift`." This matches the baseline header volatile list (line 4).

**P5. Drift semantics.** `tools/mori-census.sh:198-201`: a removed or added field names `-key`/`+key`, so `+key` means the key is new to the baseline. The six keys are not in `DRIFT_COUNTER_KEYS` (2744-2764) or `DRIFT_VOLATILE_SPECIAL` (2771). Census:2738-2739 declares them intentionally non-volatile.

**P6. Entering receipt.** `.ufo/waves/round-20/evidence/c1-drift-entering.json:35,36,40,41,42,43` list the six `+` tokens.

**P7. Declared intent.** `LOG.md:661-663` (r12 claim 3): "census roster = shokunin.conf ids ∪ .ufo/state/*.round; live lane rows 9 → 23, roster_source=conf+state". The r12 after-roster receipt line 4 calls the `roster_*` fields "the intended round-12 roster change".

**P8. Class definitions.** `contract.md:25-28` and `drift-repin-r20.md:26-28`.
- `census-schema-change`: intended, declared emitter change. Matches.
- `roster-change`: lane membership. Not applicable; no lane enters or leaves.
- `live-state`: census code unchanged. Not applicable; the census code changed, and key presence is not host state.
- `census-regression`: unintended behavior change, blocks the re-pin. Not applicable; the change is declared, selftest-asserted (`census:3408-3472`), and documented.

## 3. Residuals (no class change)

**R1. Confirmed by isolated run: `conf_dropped_n` undercounts invalid conf IDs.** The conf gate at `tools/mori-census.sh:473` is `^([a-z0-9][a-z0-9-]*)\|`. Any conf row whose ID has an uppercase letter, underscore, or leading hyphen fails the gate and is skipped before the counter at 475-476. Only overlong IDs reach the counter. The state side (493-494) counts every invalid name.

- Method: I extracted only the `resolve_roster` function (`sed -n '/^resolve_roster() {/,/^}/p'`) into scratch and ran it on a fixture conf (`.ufo/waves/round-20/falsify/FamRosterFields/r1-fixture/`). The fixture holds `Bad_ID`, `_under`, `-lead`, `kebab_mid`, one 49-character ID, `alpha`, `beta`, and a state dir with `alpha`, `Bad_State`, `ok-two`.
- Output (`bash run.sh`, exit 0): `roster_source=conf+state roster_n=3 conf_n=2 state_n=2 conf_dropped_n=1 state_dropped_n=1`. The `emit_finding: command not found` line is an artifact of the harness, not of the census.
- Only the 49-character ID was counted; the four invalid-character IDs were silently skipped.
- The selftest (`census:3463-3469`) covers only a 50-character overlong ID. Fixtures at 3403-3461 use valid IDs.
- `roster-truth-r12.md:19` says "Invalid IDs are dropped and counted", which overstates the code.
- Live today: `_grep` of `shokunin.conf` finds no invalid-character row inside a `LANES="` block (the single match is a comment at line 16, outside any block). So the pinned `conf_dropped_n=0` is correct today, but the counter cannot show it.
- Judgment [INFERENCE]: R1 produces no drift token, and the baseline never had the counter, so it is not a census-regression token. It belongs in the blind-spot list with the census-design routing already used for the dissent. The contract forbids census edits this round.

**R2. `conf_n` value moved 20 to 23 after r12; not recorded anywhere.**
- At r12: `roster-r12-20261019T220912Z-live.log:34` reads `roster_n=23 conf_n=20 state_n=21`, and `roster-truth-r12.md:3` lists audio, game-dev-2d, game-dev-3d as state-only.
- Now: `shokunin.conf` has 23 valid rows in `LANES` blocks (`_grep`). The three lanes moved into conf in fleet commits `db25a48` (2026-10-19 21:03:43 -0300, "Fix fleet lane configuration") and `10405f4` (21:07:43 -0300). Both postdate the r12 live run (22:38:11Z = 19:38 -0300). Verified by `git -C /home/vgpnk/Projects/shokunin log -- shokunin.conf`.
- The state dir has 21 valid `.round` names (`_glob`); the union is 23 and `roster_n` is 23 both times.
- The re-pinned baseline records the new values: `baseline-r20-20261021T1051Z.json:37` reads `roster_source=conf+state roster_n=23 conf_n=23 state_n=21 conf_dropped_n=0 state_dropped_n=0`.
- Adjacent value move: `baseline-r20:68` reads `FINDING ROSTER_SET_MISMATCH ... conf_only=kotodama,souji state_only=none`. The r12 state-only set was `audio,game-dev-2d,game-dev-3d`.
- Because the keys are new, drift shows no value move; the key-level token hides it. After the re-pin, future changes to these keys surface as value changes (non-volatile).
- `drift-repin-r20.md` does not mention `conf_n`, the six tokens, or R1/R2 (`_grep`). These should be recorded.

## 4. Register wording defects (C1 register; not token classes)

**W1. Dissent sentence is false as written.** `drift-classification-r20.json:18` says "census code byte-identical since r10".
- The script is not byte-identical: sha `d7710981…` at pin, `87b8d680…` at HEAD. `git rev-list --count 5be8943..HEAD -- tools/mori-census.sh` = 7 census-touching commits after the pin (`1f07f1d`, `18d7d55`, `8d22d18`, `26f6589`, `273aa74`, `2be8294`, `fe9fa90`).
- The narrower claim in `drift-repin-r20.md:39-40` ("the probes are byte-identical since r10") holds. Extracting the function bodies with `sed` and comparing with `cmp`: `probe_watchdog` 151 lines IDENTICAL at pin and HEAD; `probe_waves` 68 lines IDENTICAL.
- The six tokens' own classes cite census code changes, so the blanket sentence contradicts them. Replace it with the probe-level claim.

**W2. Round-13 wording is factually wrong.** `.ufo/waves/round-13/evidence/drift-classification.json:25-32` labels the six "r12 roster schema carried since r10". They are absent from the r10 baseline (P3). The r20 reason ("absent from the r10 baseline") is correct and supersedes it.

**W3. Lane-token rule differs between the register and the TokRosterFields seat (outside the six).** The register applies cause-based rules: 12 r12-derived `+SURFACE:lane.*` tokens are `census-schema-change` (`drift-classification-r20.json:63-133`), and kotodama and souji (minted after the pin) are `roster-change`. That matches `drift-repin-r20.md:26-28` ("Classify by cause"). The seat's §5 instead says every `+SURFACE:lane.*` token is `roster-change`. Both classes are non-blocking, so there is no re-pin effect. The L1 should state the rule explicitly.

## 5. Seat lead (`.ufo/waves/round-20/build/TokRosterFields.md`), re-derived

Used only as a lead. Its verdict (six AGREE) is confirmed by P1-P7. Its load-bearing claims were re-derived as follows:
- "1f07f1d^ has zero roster-key matches": confirmed (P2).
- "nothing later touches the emission or the roster code": confirmed for the emit line and `resolve_roster`. `probe_silence` was edited at r17 (`273aa74`, P2), which the seat does not mention.
- "`git log -G'emit_surface silence'` returns 1f07f1d, 1439c47, 7ca17b1": confirmed (P2), restricted to the census file.
- "HEAD e4d9384": stale. Current HEAD is `8f8c58e`. The census file has not changed since `fe9fa90`, so its sha is unaffected.
- R1 and R2: both confirmed by observation (sections 3 and 4).

## 6. Checks run and not run

Run (all exit 0 unless noted):
- `git -C <lane> log -S'<key>=$<VAR>' -- tools/mori-census.sh` (six keys); `-S state_n`; `-G` for the emit line and roster names; `-L` for `resolve_roster`, `probe_silence`, `probe_watchdog`, `probe_waves`; `git rev-list --count 5be8943..HEAD -- tools/mori-census.sh` = 7.
- `git show 5be8943:tools/mori-census.sh | sha256sum` = `d7710981…`; `sha256sum tools/mori-census.sh` = `87b8d680…`; `git status --short -- tools/mori-census.sh` empty.
- `git show 5be8943:corpus/evidence/baseline-r10-…json | sha256sum` = worktree file (`0993b235…`); `git status` empty; `git log` one commit.
- `sed -n` extraction of function bodies at pin and HEAD, then `cmp` (section 4, W1).
- Isolated `resolve_roster` run on a scratch fixture (R1). This is not a census run.
- Read-only fleet checks: `git -C /home/vgpnk/Projects/shokunin log -- shokunin.conf`; read `shokunin.conf` and `.ufo/state/*.round`.
- Reads and `_grep` on named files (classification JSON, census lines cited, baseline r10 and r20, roster-truth-r12.md, LOG.md, the round-13 classification, the r12 receipts, contract.md, drift-repin-r20.md, c1-drift-entering.json, the seat report).

Not run: `tools/mori-census.sh` in any mode, `--drift`, `--selftest`. The census was not in this item's scope.

Tooling: no installs or updates. No subagents. No writes outside the scratch dir and this report.

Scratch: `.ufo/waves/round-20/falsify/FamRosterFields/` (census copies `census-*.sh`, diffs `diff-*.diff`, function extracts `pin-*.fn`/`head-*.fn`, `r1-fixture/`).

Process note: I ran one shell `grep -n -E` and one `awk` over git output, which the tool policy would have routed to the search tool. The results were not affected.

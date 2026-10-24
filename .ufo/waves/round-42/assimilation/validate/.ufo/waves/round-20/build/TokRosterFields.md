# TokRosterFields: round-20 C1 classification of six drift tokens

Seat: MoriR20.TokRosterFields (scout, leaf). Census SHA-256 `87b8d680…ab28` at measured commit `2061780` (lane tip), at HEAD `e4d9384`, and in the working tree. The census was not run (not in this item). Read-only throughout. No subagents. No installs or updates. Git used only read-only (`log`, `show`, `grep`, `rev-parse`). Fleet files read only (`shokunin.conf`, `.ufo/state` listing, fleet `git log`).

## Verdict

All six tokens are `census-schema-change`. Round 13 classified the same six as "r12 roster schema carried since r10". I agree on cause and status and refine the label. No token is `roster-change`, `live-state` or `census-regression`.

Two residuals do not change the classes but must be recorded before the re-pin: R1 (latent undercount in `conf_dropped_n`) and R2 (`conf_n` moved 20 to 23 after r12, hidden from drift because the key is new).

## JSON-ready table

```json
[
  {"token": "+conf_dropped_n", "class": "census-schema-change", "reason": "Added by r12 (1f07f1d) as the silence-surface count of invalid conf-row IDs; absent from the r10 baseline; intended and documented (roster-truth-r12.md:19,21; census :2738-2739), non-volatile by design. Latent undercount is residual R1; it does not change this class.", "evidence": "tools/mori-census.sh:2552 (sole emitter, probe_silence 2509-2553); :376,:452,:476 (value); git show 1f07f1d diff -181/+182; corpus/evidence/baseline-r10-20261015T2231Z.json:22 (no key); corpus/knowledge/roster-truth-r12.md:19,21; LOG.md:661-663,672-673; corpus/evidence/drift-r12-20261019T2230Z-after-roster.log:2,4; .ufo/waves/round-20/evidence/c1-drift-entering.json:35"},
  {"token": "+conf_n", "class": "census-schema-change", "reason": "Added by r12 (1f07f1d) as CONF_N, the unique valid conf-ID count; absent from the r10 baseline; intended and documented. Its live value moved 20 to 23 after r12 (live-state, residual R2); the presence token itself is schema.", "evidence": "tools/mori-census.sh:2552; :374,:450,:504; git show 1f07f1d diff +182; corpus/evidence/baseline-r10-20261015T2231Z.json:22; corpus/evidence/roster-r12-20261019T220912Z-live.log:34 (conf_n=20 at r12); LOG.md:661-663; .ufo/waves/round-20/evidence/c1-drift-entering.json:36"},
  {"token": "+roster_n", "class": "census-schema-change", "reason": "Added by r12 (1f07f1d) as ROSTER_N, the unique union count (23 at r12 and now); absent from the r10 baseline; intended (LOG.md:661-663, live lane rows 9 to 23).", "evidence": "tools/mori-census.sh:2552; :373,:449,:458,:531; git show 1f07f1d diff +182; corpus/evidence/baseline-r10-20261015T2231Z.json:22; LOG.md:661-663,672-673; corpus/evidence/roster-r12-20261019T220912Z-live.log:34; .ufo/waves/round-20/evidence/c1-drift-entering.json:40"},
  {"token": "+roster_source", "class": "census-schema-change", "reason": "Added by r12 (1f07f1d) as ROSTER_SOURCE (env, conf+state, conf, state or builtin); absent from the r10 baseline; intended, documented in roster-truth-r12.md:19 and asserted by selftest rows.", "evidence": "tools/mori-census.sh:2552; :372,:457,:517,:519,:521,:526; tools/mori-census.sh:3408-3472 (selftest expectations); git show 1f07f1d diff +182; corpus/knowledge/roster-truth-r12.md:19; corpus/evidence/baseline-r10-20261015T2231Z.json:22; .ufo/waves/round-20/evidence/c1-drift-entering.json:41"},
  {"token": "+state_dropped_n", "class": "census-schema-change", "reason": "Added by r12 (1f07f1d) as STATE_DROPPED_N, the count of invalid regular *.round names; absent from the r10 baseline; intended and documented (roster-truth-r12.md:19).", "evidence": "tools/mori-census.sh:2552; :377,:453,:494; git show 1f07f1d diff +182; corpus/evidence/baseline-r10-20261015T2231Z.json:22; corpus/knowledge/roster-truth-r12.md:19; .ufo/waves/round-20/evidence/c1-drift-entering.json:42"},
  {"token": "+state_n", "class": "census-schema-change", "reason": "Added by r12 (1f07f1d) as STATE_N, the unique valid *.round count (21); absent from the r10 baseline; intended and documented. The older state_n identifier is a watchdog-probe local whose output key is state_rounds=, so it never emitted state_n=.", "evidence": "tools/mori-census.sh:2552; :375,:451,:505; :758,:801,:846 (local, not emitted as a key); git show 1f07f1d diff +182; git log -S state_n older hits 7ca17b1 (201,203,217) and 9738f1a (499,542,587) are that local; corpus/evidence/baseline-r10-20261015T2231Z.json:22; .ufo/waves/round-20/evidence/c1-drift-entering.json:43"}
]
```

## 1. Emission now

- Sole emitter of all six keys: `tools/mori-census.sh:2552`. It is the only `emit_surface silence` call in the file. It sits in `probe_silence` (2509-2553).
- The path is unconditional. `resolve_roster` runs at `:2512` on every live run. The lane loop at `:2519` iterates the same `ROSTER_LANES`. There is no early return before the emit.
- Value origins, all in `resolve_roster` (`:444-531`):
  - `roster_source`: init `:372`; env `:457`; `conf+state` `:517`; `conf` `:519`; `state` `:521`; `builtin` `:526`.
  - `roster_n`: init `:373`; reset `:449`; env `:458`; final `:531`.
  - `conf_n`: init `:374`; reset `:450`; final `:504`.
  - `state_n`: init `:375`; reset `:451`; final `:505`.
  - `conf_dropped_n`: init `:376`; reset `:452`; increment `:476`.
  - `state_dropped_n`: init `:377`; reset `:453`; increment `:494`.
- Non-emitting `state_n` identifier: the watchdog-probe local at `:758`, increment `:801`, and `state_rounds=$state_n` output at `:846`.
- Drift treatment: none of the six is in `DRIFT_COUNTER_KEYS` (`:2744-2764`) or `DRIFT_VOLATILE_SPECIAL` (`:2771`). They are unmasked by design (`:2738-2739`). A `+key` in drift means the key is new to the baseline (`:198-200`).

## 2. Baseline (`corpus/evidence/baseline-r10-20261015T2231Z.json`)

- The file is plain text with a `# mori-drift-baseline v1` header, despite the `.json` name. Its census SHA is `d7710981…`, which equals `1f07f1d^`.
- Silence line is `:22`: `SURFACE silence: ok (cmd=…; silent=<V> progressing=<V> … skipped=<V> window_s=7200; ts=<V>)`. It has none of the six keys.
- A pattern search over the whole baseline for the six names returns 0 matches.
- Volatile list `:4` contains none of the six.

## 3. Introducing commit

- `1f07f1d` (round-12, `Mon Oct 19 19:41:08 2026 -0300`), subject "census roster = declared lanes ∪ driver counters (9 -> 23)". Diff hunk: `-181` the old silence emit, `+182` the new emit carrying the six fields.
- Emission line by commit: `1f07f1d:1571`, `c13df48:1803`, `HEAD:2552`.
- `git log -S<token> --oneline -- tools/mori-census.sh` returns `1f07f1d` for all six. The older `state_n` hits (`7ca17b1`, `9738f1a`) are the watchdog-probe local (see §1), not an emitted key.
- `git grep -E 'roster_source=|roster_n=|conf_n=|conf_dropped_n=|state_dropped_n='` at `1f07f1d^` returns 0 matches.
- Nothing later touches the emission or the roster code. `git log -G'emit_surface silence'` returns `1f07f1d`, `1439c47`, `7ca17b1`. `git log -G'ROSTER_SOURCE|ROSTER_N|CONF_N|STATE_N|CONF_DROPPED_N|STATE_DROPPED_N|roster_ids'` returns `1f07f1d` only. The `-G` run on the `state_n=` pattern also matched `d30b4e4` and `5b62c89`; these are `state_n=` assignments of the same local. I did not re-read those two individually.

## 4. Intent, stated before the drift was read

- `LOG.md:661-663` (r12 claim 3): "census roster = `shokunin.conf` ids ∪ `.ufo/state/*.round`; live lane rows 9 → 23, `roster_source=conf+state`…"
- `LOG.md:672-673`: "After claim 3 the drift additionally names the 14 new lane rows and roster fields (`drift-r12-20261019T2230Z-after-roster.log`). No re-pin (planned r13)."
- `SCORECARD.md:605` (r12 row 3) and `SCORECARD.md:613` (freshness: "names exactly the 14 new lane rows and the roster fields … no re-pin this round").
- `corpus/knowledge/roster-truth-r12.md:19` (decision line naming `roster_source`, `roster_n`, `conf_n`, `state_n`, `conf_dropped_n`, `state_dropped_n`). `:21`: "Roster fields are deliberately absent from the r10 volatile list: changes remain visible to `--drift`."
- Census: `:2738-2739` "Roster source/count fields intentionally remain non-volatile: roster changes alter behavior and must be reported by --drift."
- Receipt `corpus/evidence/drift-r12-20261019T2230Z-after-roster.log:2` lists the six `+` tokens. Line 4 reads: "the roster_* fields are the intended round-12 roster change (claim 3)".
- Round-13 carry: `LOG.md:754` and `SCORECARD.md:694` ("carried r12 roster schema").

## 5. Class decision and rule

Rule applied: a `+key` token whose `key=` is a field newly printed by the census is `census-schema-change`. A `+SURFACE:lane.*` token, meaning a lane row entering the graded set, is `roster-change`. A key present in both with a changed value is `live-state` or `census-regression`, depending on whether the census logic changed.

All six are `+key` tokens for output fields absent from the baseline. They are schema, not membership.

Rejected alternatives:
- `roster-change`: the tokens name output fields, not lanes. The membership change is carried by the 14 `+SURFACE:lane.*` tokens, which are outside my six. The r12 receipt calls the fields "roster change"; that is a label difference only (R3).
- `live-state`: a key absent from the baseline cannot be produced by host state, because the r10 census never printed it. Live values are a separate matter (R2).
- `census-regression`: the emission is intended, documented, non-volatile by design and asserted by selftest. R1 is a latent undercount in a new counter. It is not a change against the baseline, and drift cannot see it.

## 6. Comparison with round 13 (`.ufo/waves/round-13/evidence/drift-classification.json`)

| token | r13 entry (line) | r20 class | verdict |
|---|---|---|---|
| +conf_dropped_n | "r12 roster schema carried since r10" (:25) | census-schema-change | agree; refine label; add commit pointer |
| +conf_n | same (:26) | census-schema-change | agree; refine label |
| +roster_n | same (:29) | census-schema-change | agree; refine label |
| +roster_source | same (:30) | census-schema-change | agree; refine label |
| +state_dropped_n | same (:31) | census-schema-change | agree; refine label |
| +state_n | same (:32) | census-schema-change | agree; refine label |

Overall: agree on all six. Reasons:
1. All six appear in the r13 measured drift (`.ufo/waves/round-13/evidence/drift-retained-baseline.json:8`), in the r12 after-roster receipt (`:2`) and in the r20 entering receipt (`c1-drift-entering.json:35,36,40-43`).
2. No commit after `1f07f1d` touched their emission or roster code (§3). The r13 classification therefore still describes the same mechanism at census `87b8d680`. The r13 register was measured at `c13df48`, census `39abda0a`.
3. Differences, neither of which changes the re-pin outcome:
   - Round 13 gives no commit or path pointer for these six. The r20 entries add them.
   - "roster schema" is ambiguous with roster-change. Round 20 pins it to census-schema-change, because the tokens name fields.
   - The r12 pre-roster classification `drift-r12-20261019T2204Z-classification.md` was measured 21:59-22:04Z, before the roster change, so it does not cover these six. Round 13 is the first classification of them.

## 7. Residuals (not token classes; record in the register note)

**R1. `conf_dropped_n` undercounts.** The census gates the conf counter on the ID regex at `:473`: `^([a-z0-9][a-z0-9-]*)\|`. A conf row whose ID contains any other character, such as `Bad_ID|…`, `_x|…` or a leading `-`, fails that gate and is silently skipped, not counted. The state side counts every invalid regular `*.round` name (`:493-494`). `roster-truth-r12.md:19` promises "Invalid IDs are dropped and counted". The selftest at `:3463-3473` covers only a 50-character overlong ID. The live value 0 is correct for today's conf, since all 23 rows match, but the counter cannot show that no such rows exist. C1 does not edit the census, so this goes to the census owner.

**R2. Value-level live-state behind `+conf_n`.** The r12 live receipt (`roster-r12-20261019T220912Z-live.log:34`) reads `roster_source=conf+state roster_n=23 conf_n=20 state_n=21 conf_dropped_n=0 state_dropped_n=0`, at `22:38:11Z`. Since then, fleet `shokunin.conf` gained `audio`, `game-dev-2d` and `game-dev-3d`. Commit `db25a48` (`2026-10-19 21:03:43 -0300`) added them. Commit `10405f4` (`21:07:43 -0300`) gave them their own block, now `shokunin.conf:79-84`, rows `81-83`. Both commits follow the r12 live run; `22:38:11Z` is `19:38 -0300`.

Applying the census rule by hand [INFERENCE; census not run]:
- `conf_n` = 23
- `state_n` = 21 (21 `*.round` names in `.ufo/state`; `find -type l` returns none)
- `roster_n` = 23
- `roster_source` = `conf+state`
- `conf_dropped_n` = 0
- `state_dropped_n` = 0
- state-only set empty; conf-only = `kotodama,souji`

So `roster-truth-r12.md:3` and its state-only list are stale. The re-pin will baseline `conf_n=23`. Because the key is new, drift cannot display the 20 to 23 move. The L1 must not read `+conf_n` as "conf unchanged since r12".

**R3. Label.** The r12 receipt (`after-roster.log:4`) calls the `roster_*` fields "the intended round-12 roster change". I classify them `census-schema-change` and reserve `roster-change` for lane membership. If the L1 prefers the receipt's label, change the class for these six. Neither label is `census-regression`, so the re-pin gate is unchanged.

**R4. Name collision.** `state_n` was a pre-r12 watchdog-probe local. `LOG.md:278` and `SCORECARD.md:171` refer to "`:227` `state_n`", the same local under an older line number. Its output key was `state_rounds=`. No `state_n=` key existed before `1f07f1d`.

## 8. Checks run

- `sha256sum`: worktree = HEAD = `2061780` → `87b8d680…ab28`. `1f07f1d` → `3da5b098…`. `1f07f1d^` → `d7710981…`. `c13df48` → `39abda0a…`.
- `git log -S<token>`, `git log -G` (emission line; roster code), `git show 1f07f1d -- tools/mori-census.sh` (hunk `-181/+182`), `git grep` at `1f07f1d^`, `1f07f1d`, `c13df48`, `HEAD`.
- Fleet, read-only: `git log` and `git show --stat` on `shokunin.conf` (`db25a48`, `10405f4`); `find .ufo/state -maxdepth 1 -type l` (empty).
- Reads: census `:372-377`, `:444-531`, `:2509-2553`, `:2738-2739`, `:2744-2772`, `:3407-3472`; baseline `:4`, `:22`; receipts; round-13 register; knowledge; `LOG.md`/`SCORECARD.md` lines.
- Not run: `tools/mori-census.sh` (any mode), `--drift`, `--selftest`. R2 values are [INFERENCE].
- Tooling: no installs or updates.

## 9. Handoff for L1

- Enter the six into `corpus/evidence/drift-classification-r20.json` with signed keys (`+conf_n`, and so on), class `census-schema-change`, and the reason and evidence above.
- Record R1 and R2 in the register note. R2 changes what the re-pinned baseline says about conf membership.
- After pinning, the six should no longer appear in `--drift` output. Other tokens may remain; they are outside this seat.

## 10. Cross-check with TokRosterLanes step A/B rule (2026-10-21)

- Agreement: all six keys are emitted on the pin-time replay (`tools/mori-census.sh:2552` is unconditional), so each is census-schema-change under step A. Their values are step B and are not token classes.
- Premises checked: `99efc52` leaves 18 conf rows (commit message "18 remain"). The `audio.round`, `game-dev-2d.round` and `game-dev-3d.round` files have birth time 2026-10-15 01:45:42 -0300, before the pin at 22:26:29Z. `kotodama.round` and `souji.round` do not exist now, so they have no state-only rows.
- `conf_n` trajectory [INFERENCE from the census rule applied by hand]: 18 at pin; 20 at r12, after the `kotodama` mint (`417b1c2`) and the `souji` mint (`7bf2b1a`), both after the pin; 23 now. `db25a48` (21:03 -0300) added `audio`, `game-dev-2d` and `game-dev-3d` to conf, and `10405f4` (21:07 -0300) put them in their own block. The union has been 23 since r12.
- `roster_n` trajectory: 21 at pin (conf 18 is a subset of state 21); 23 at r12; 23 now.
- `state_n` is 21 throughout. All 21 current `.round` files have birth time before the pin (`stat %w`; latest 2026-10-15 01:45:42 -0300, pin 19:26:29 -0300). A file deleted since the pin would not show here [INFERENCE: none known]. `roster_source` is `conf+state` throughout.

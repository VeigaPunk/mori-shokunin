# AttackNoHarm — round 15 C1 (validated positives), critic report

Seat: `MoriR15.AttackNoHarm` (critic, report-only). Nothing was run. No production, fixture, or harness file was edited. Nothing was installed or updated.
Target read: `tools/mori-census.sh` at snapshot `#DC7D`. At read time it had no `positive_*` token (grep `positive_` found no match), so every anchor below points at the **pre-change r14 code**. The proposal is the shared-contract "Production interface" text in `.ufo/waves/round-15/spec.json:3`.
Judged axis: **coverage**. No-harm axes checked: the old homogeneous counts (`count=` and the per-class raw tokens), routes and owners, severity and the single-line rule, the meaning of unavailable reasons, verdict/rc gates, drift identity, and selftest anchors.

## Verdict

The proposal can be no-harm, but only if one invariant holds and is enforced:

> **I0 — positive ≡ raw-ok.** Each positive token counts exactly the records that satisfy the **same per-record predicate the raw class already applies in its `all(...)` guard**, evaluated without error over every element of the same slurped array. So whenever the raw class is `ok`, `positive_X` equals the raw/split count bit for bit. Every existing gate, path, severity, and verdict is then unchanged on every stream the raw class accepts. Only streams the raw class rejects can change behaviour, and only by adding an alarm.

Each counterexample below is a way to break I0 or to leak a positive into an old meaning. None of them is a tradeoff that needs a judge ruling. All are fixable defects. One residual is a real tradeoff (T1).

## Counterexamples

### CX-1 — Positive predicate looser than raw: alarm from a record raw rejects
- **Anchor:** `JOURNAL_JQ_SIGKILL` `:975` uses `(.EXIT_CODE == "killed") and ((.EXIT_STATUS | tostring) == "9")`. The KILL warn is at `:1340-1354`.
- **Stream (user unit_sigkill):** `{"_BOOT_ID":"<cur>","MESSAGE_ID":"98e32220…","EXIT_CODE":"killed","EXIT_STATUS":"09"}`
- **Raw today:** `"09"|tostring == "9"` is false, so the result is `record-invalid` and `unit_sigkill_record=unavailable:record-invalid`. There is no warn and the run is CLEAN.
- **Harm if positive uses `tonumber == 9`** (also `"9.0"`, `"9e0"`, `" 9"`): `positive_process_sigkill=1` makes the user `KILL_SIGNAL_JOURNAL` warn fire and the verdict becomes DRIFT, all from a record the canonical class calls invalid. That is a new false-positive route created by a predicate fork.
- **Smallest correction:** derive the positive predicate from the existing guard text. Factor the per-record body once (for example `def ok_rec: type=="object" and (._BOOT_ID|type)=="string" and ._BOOT_ID==$boot and .MESSAGE_ID==$id and …;`), use it in `all(.[]; ok_rec)`, and use the same definition in `[.[]|select(ok_rec)]|length`. Unit paths: `ok_rec and oom` / `ok_rec and sig` (`:1016-1019`).
- **Axes:** severity/verdict gate, false-positive.

### CX-2 — Positive predicate stricter than raw: evidence contradicts the raw count on a raw-ok stream
- **Anchor:** `:975`. Raw accepts the number `9` as well as the string `"9"`, because `tostring` maps both to `"9"`.
- **Stream:** one current-boot record with `"EXIT_STATUS":9` (a number).
- **Raw today:** `unit_sigkill_record=1`. The warn fires with `count=1 process_sigkill=1`.
- **Harm if positive requires `type=="string"` for "scalar status 9":** the same line carries `process_sigkill=1 positive_process_sigkill=0`, so a raw-ok class disagrees with its own validated subset. In a mixed stream (the same numeric-9 record plus a foreign-boot neighbour), the warn is **lost**, even though the record is one raw would accept. That defeats C1 coverage.
- **Smallest correction:** the same as CX-1. "Scalar status 9" must mean exactly the raw `tostring=="9"` predicate, which rejects arrays and objects because their `tostring` is JSON text. [INFERENCE] For a float literal `9.0`, `tostring` depends on the jq version. Sharing one predicate keeps raw and positive consistent either way.
- **Axes:** coverage, homogeneous-count consistency.

### CX-3 — An unguarded field access turns `record-invalid` into `malformed-json` (raw reason changes and the alarm is lost)
- **Anchor:** the raw guard short-circuits `type=="object" and …` (`:974`, `:1019`). The else branch `:973` / `:1037` yields `record-invalid`. `journal_query` maps a jq error to `malformed-json` (`:1102`).
- **Stream (user kernel_oom):** `[{valid current-boot fe6faa94 record}, 42]`. Also `["x"]` or a bare string element.
- **Raw today:** `kernel_oom_notice=unavailable:record-invalid`.
- **Harm if the positive is written as `select(._BOOT_ID==$boot and type=="object")`, or the unit positive maps `subject` (`has("UNIT")`, `:1002`) over all records:** `42|._BOOT_ID` and `42|has(…)` raise errors. jq then exits non-zero and the whole class becomes `malformed-json`. The **existing raw reason token changes meaning**, the positive becomes `unavailable`, and the valid OOM record is not alarmed. This is the exact C1 case.
- **Smallest correction:** test `type=="object"` first inside `ok_rec` (the `and` short-circuits). Never call `subject`/`has` in the positive path. `oom`/`sig` already use `.UNIT_RESULT?` and are safe.
- **Required anchor:** a stream with one valid record plus a non-object element gives `want_oom=true`, raw `unavailable:record-invalid` (not `malformed-json`).
- **Axes:** raw-unavailable semantics, coverage.

### CX-4 — Output shape change breaks the invalid-reason dispatch
- **Anchor:** `journal_query` `:1103-1105` matches the **whole** jq output exactly against `record-invalid|multi-boot|boot-mismatch`. Width is checked exactly at `:1112`, and the boot column is checked at `:1131-1134`.
- **Harm:** if positives ride along as `record-invalid\t1` (or similar) without updating that `case`, the output falls through to the vector parse. The width check then fails and gives `malformed-json`. Every existing reason token changes, and selftests `:3222`, `:3228`, `:3236` would go red. If the invalid branch instead keeps emitting the bare word, positives never reach bash and C1 does nothing.
- **Smallest correction:** split the output into a raw part and a positive part that are parsed separately. One way: a second jq pass over the **same `$raw`** variable (`:1096`; no new journalctl call), emitting positive integers only. Another way: a fixed prefix column parsed before the reason dispatch. Either way the raw reason words and the raw width stay byte-identical, and the positive columns are `is_int`-checked on their own.
- **Axes:** raw-unavailable semantics, gate integrity.

### CX-5 — Positive emitted on producer/parse failure (fabricated evidence)
- **Anchor:** `:1083-1095` (rc≠0, timeout, stderr-nonempty return before any parse) and `:1102` (jq failure).
- **Streams:** two valid kernel_oom records with `.rc=1`, or with one non-empty `.err` byte, or a stream containing a truncated line `{not json`.
- **Raw today:** `unavailable:rc-1`, `unavailable:stderr-nonempty`, `unavailable:malformed-json`, each with no alarm and a CLEAN verdict (selftests `:3184-3216`; `JournalFixtureDesign.md` G3/G4/G5).
- **Harm if positives are computed from `CAP_OUT` before these checks, or by line-wise `jq -c` / `fromjson?` repair:** `positive_kernel_oom=2` makes the OOM crit fire from partial or untrusted bytes. That is a gate-meaning inversion: producer failure now alarms.
- **Smallest correction:** positives may only be computed after `CAP_RC==0`, `err_bytes==0`, and a successful slurp parse. Otherwise every positive token reads `unavailable:<same reason>`. No line-wise or `?`-tolerant parsing.
- **Axes:** severity gate, no-fabrication.

### CX-6 — `paths=` and `count=` on the alarm lines keep raw-derived meaning (empty or fabricated)
- **Anchor:** OOM `:1314-1331`. `oom_paths` is set only from raw `ko`/`uo` > 0. KILL `:1344-1353`: `kill_paths` comes from raw `ps`/`us`, and `count=$ps`.
- **Stream:** user unit_sigkill = `[valid current-boot record, same record with _BOOT_ID=ffff…]`. Raw becomes `unavailable:multi-boot` and positive is 1.
- **Harm A (empty path):** if only `kill_fire` is extended, the line prints `paths= count=unavailable:multi-boot …`. The alarm then names no path. The OOM line likewise prints `paths= user_notice=unavailable:…`.
- **Harm B (fabricated total):** if the implementer "fixes" it by writing `count=$positive`, the historic homogeneous `count=` (the raw process-SIGKILL record count, `:1353`; masked as a drift counter, `:2255`) silently changes from "class total" to "validated subset" on exactly the runs where the total is unknown.
- **Smallest correction:** compute `paths` from the **positive** values (identical to raw when raw is ok, per I0, so old lines stay byte-identical). Keep `count=$ps`, `process_sigkill=$ps`, `user_unit_signal=$us`, and `*_notice=`/`*_unit_oom=` as raw (possibly `unavailable:…`). Add the positives as separate scope-prefixed fields (CX-9).
- **Axes:** homogeneous counts, route provenance.

### CX-7 — A positive leaks into a scope or route that had no such alarm
- **Anchors:** user-only warn `:1340-1343`; system SIGKILL is info only (`:1240`, `:1147`); the unit routing partition `:1264-1291` is gated on raw `ok`.
- **Stream a:** system unit_sigkill `[valid, foreign-boot]`, user scope clean. **Required:** no `KILL_SIGNAL_JOURNAL` (user warn), no `KILL_SIGNAL_JOURNAL_SYSTEM` (that info line stays raw-ok-only: "no new route"), CLEAN rc 0. `system positive_process_sigkill=1` appears only on `SURFACE journal.system`.
- **Stream b:** system unit_failure `[valid UNIT_RESULT=signal, foreign-boot]`. **Required:** no user warn. The system unit signal never warned before.
- **Stream c:** user unit_failure `[valid oom-kill on kagi-shokunin.service, foreign-boot]`. **Required:** OOM crit fires. `unit_fleet`, `unit_nonfleet`, `unit_unknown`, `unit_oom_fleet`, and so on, all stay `unavailable:multi-boot`. No `UNIT_FAILURE_JOURNAL*`, `UNIT_FAILURE_OUT_OF_SCOPE*`, or `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` line appears. This is the preserved selftest bad-check at `:3072` ("routing finding emitted from an unavailable unit class").
- **Smallest correction:** positives feed only `oom_fire` (either scope) and `kill_fire` (user scope only). The per-class info loop (`:1236-1256`) and the routing loop (`:1264-1291`) stay gated on `js==ok`.
- **Axes:** routes/owners, severity.

### CX-8 — The surface status word flips to `ok`, or positive=0 is read as a numeric total
- **Anchor:** `:1360-1367`. `st=unavailable` if any class is not ok.
- **Stream:** identity-mismatch (`:3218-3222`; system kernel_oom holds a d989611b record). Raw is `unavailable:record-invalid` and the positive is a numeric `0`.
- **Harm:** if the row status is derived from positive availability, or if `positive_kernel_oom=0` is placed where a gate reads "0 ⇒ clean", the class reads as a known zero. That is the exact "never a look-alike 0" rule (`:949-953`).
- **Smallest correction:** keep `st` computed from raw `js` only. Keep positive tokens after the raw tokens. Never reuse a positive in any `-eq 0` clean check. Add a row-level disclosure such as `positive_basis=validated-subset-lower-bound`, so `0` reads as "no validated record", not "no records".
- **Axes:** raw-unavailable semantics, no-fabrication.

### CX-9 — Field-name collisions make existing selftest anchors vacuous
- **Anchors (unanchored ERE substrings):** `:3070` `'unit_oom=unavailable:rc-1' 'unit_signal=unavailable:rc-1'`, `:3120` `'unit_signal=1'`, `:3138` `'unit_oom=1'`, `:3146` `'unit_oom=0'`, `:3179` `'unit_oom=0' 'unit_signal=0'`, `:3043` `'.*process_sigkill=1 .*user_unit_signal=0'`.
- **Harm:** each contract name `positive_unit_oom`, `positive_unit_signal`, and `positive_process_sigkill` contains the raw key as a suffix. Take `:3070` (rc-1). Positives are `unavailable:rc-1` there by contract, so `positive_unit_oom=unavailable:rc-1` alone satisfies `'unit_oom=unavailable:rc-1'`. A regression that dropped or renamed the raw split token would stay green. The same holds for `:3138` (`positive_unit_oom=1`), `:3120`, and `:3043`. The `:3052` once-only loop uses `\b$f=`. GNU `\b` sees no boundary between `_` and the next letter, so that loop is safe.
- **Smallest correction (harness owner):** anchor the raw assertions with a separator, `(^|[ (;])unit_oom=` (also for `unit_signal=`, `process_sigkill=`, `user_unit_signal=`). On the finding lines, use scope-prefixed positive fields (`user_positive_kernel_oom=` / `system_positive_kernel_oom=`). That keeps the `:3052` exactly-once rule meaningful, and `drift_scan` (`:2321-2325`) never has to concatenate two `positive_*` values from one OOM line.
- **Axes:** selftest gate integrity (coverage claim provenance).

### CX-10 — Drift churn or a silent volatile-list change
- **Anchor:** `DRIFT_COUNTER_KEYS` `:2254-2270` and mask `:2292` `\b(${cre})=[0-9]+`.
- **Harm A (not added):** `positive_kernel_oom=3→4` is unmasked, because `\bkernel_oom…` cannot match inside `positive_…`. A live count change that masks to `<V>` on the raw token then flips `--drift` on the positive token. The two sibling tokens get inconsistent volatility.
- **Harm B (added silently):** `DRIFT_VOLATILE_LIST` changes, and every r14 pin reports `MORI_DRIFT: volatile_fields`, plus `+positive_*` key adds on the journal rows and the alarm lines. This is honest, intended schema drift, but it has to be declared, not discovered.
- **Smallest correction:** add every emitted positive key (and the scope-prefixed finding forms from CX-9) to `DRIFT_COUNTER_KEYS`. L1 records `volatile_fields` plus the `+positive_*` keys as intentional C1 drift and re-pins once. `unavailable:<reason>` values stay unmasked, so a valid→unavailable flip still surfaces.
- **Axes:** drift gate.

## Preserved gate meanings (old cases that must not move)

None of the existing selftest invalid-class cases holds a valid current-boot positive, so under I0 every one keeps its verdict:

| Case (anchor) | Stream | Raw token (unchanged) | Positive | Verdict |
|---|---|---|---|---|
| foreign-boot `:3224-3228` | 1 × fe6faa94, `_BOOT_ID=ffff…` | `kernel_oom_notice=unavailable:boot-mismatch` | `positive_kernel_oom=0` | CLEAN rc 0 |
| multi-boot `:3230-3236` | oomd ffff + eeee (neither current) | `oomd_notice=unavailable:multi-boot` | no oomd positive in contract | CLEAN rc 0 |
| identity-mismatch `:3218-3222` | d989611b in the kernel_oom slot | `kernel_oom_notice=unavailable:record-invalid` | `0` | CLEAN rc 0 |
| malformed `:3212-3216` | `{not json` | `coredump_notice=unavailable:malformed-json` | n/a (coredump) | CLEAN rc 0 |
| stderr `:3204-3210` | empty plus stderr byte | `unit_sigkill_record=unavailable:stderr-nonempty` | `unavailable:stderr-nonempty` | CLEAN rc 0 |
| unit rc1 `:3064-3072` | user kernel_oom valid plus unit rc 1 | `unit_*=unavailable:rc-1` | unit positives `unavailable:rc-1`, kernel `1` | DRIFT (OOM via kernel only), no routing line |
| array UNIT_RESULT `:3143-3149` | `UNIT_RESULT:["oom-kill"]` | raw ok, `unit_oom=0` | `positive_unit_oom=0` (not a string) | CLEAN, no OOM |
| UNIT injection `:3151-3158` | newline in USER_UNIT, `resources` | raw ok | `0` | CLEAN |
| matrix `:3011-3053` | all raw ok | unchanged | equal to raw (I0) | DRIFT, one OOM line, no `count=` on OOM |

The silence oracle (`tools/mori-silence-cases.sh:301-311`, `:380-382`) serves an empty `journal.json`, so positives are `0` and the verdict-only grading is unaffected.

## New cases this attack requires (static expectations, independent of SUT)

| id | stream | want_oom | want_signal | invalid_class |
|---|---|---|---|---|
| nh-sigkill-09-loose | user sigkill `EXIT_STATUS:"09"` alone | false | false | record-invalid |
| nh-sigkill-num9-mixed | user sigkill `EXIT_STATUS:9` (number) plus foreign-boot sibling | false | true | multi-boot |
| nh-kernel-nonobject | user kernel `[valid, 42]` | true | false | record-invalid (not malformed-json) |
| nh-kernel-rc1-valid | 2 valid kernel records, rc 1 | false | false | rc-1 |
| nh-system-sigkill-mixed | system sigkill `[valid, foreign]`, user clean | false | false | multi-boot |
| nh-system-unit-signal-mixed | system unit `[valid signal, foreign]` | false | false | multi-boot |
| nh-user-unit-oom-fleet-mixed | user unit `[valid oom-kill kagi-shokunin.service, foreign]` | true | false | multi-boot; zero routing lines |

Forbid assertions to pair with them: `^FINDING OOM_KILL_JOURNAL .*count=`, `paths= ` (empty), any `UNIT_FAILURE_*` line when the unit class is unavailable, `KILL_SIGNAL_JOURNAL_SYSTEM` on a system-invalid stream, `^SURFACE journal\.<scope>: ok` when any raw class is unavailable.

## Tradeoff for the judge (not a defect)

- **T1 — alarm on a partially rejected stream.** Under I0, a raw-invalid stream with one valid current-boot record now moves CLEAN→DRIFT (rc 0→1). That is the claimed C1 behaviour and the intended harm. The judge should confirm that the record-level trust boundary (`_BOOT_ID`/`MESSAGE_ID` are client-supplied, `trust=client-supplied`) is acceptable when its sibling records failed validation. The alternative is the r14 status quo, where one bad neighbour silences a real OOM. That is the coverage hole this round targets.

## Smallest safe correction (summary)

1. One shared per-record `ok_rec` definition, object-guarded first. Positives are `select(ok_rec [and oom|sig])` over the same slurped `$raw`, computed only after rc 0, empty stderr, and a successful parse. Raw reason words and widths stay byte-identical (CX-1 to CX-5).
2. `paths` are computed from positives. `count`, `process_sigkill`, `user_unit_signal`, `*_notice`, and `*_unit_oom` stay raw. Positives are added as scope-prefixed fields. The OOM line stays single, with no `count=` (CX-6, CX-9).
3. Positives feed only `oom_fire` (both scopes) and the user `kill_fire`. The info/routing loops and the row `st` stay gated on raw `ok` (CX-7, CX-8).
4. Positive keys go into `DRIFT_COUNTER_KEYS`. `volatile_fields` and `+positive_*` are declared as intentional C1 drift. Selftest raw-key regexes get separator anchors (CX-9, CX-10).

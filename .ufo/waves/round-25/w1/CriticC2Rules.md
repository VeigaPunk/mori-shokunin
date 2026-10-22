# CriticC2Rules — C2 rules 1–7 and the frozen cases vs real omp 18.12.6 semantics

Seat: `MoriR25.CriticC2Rules` (critic, leaf). Contract: `.ufo/waves/round-25/contract.md` at `7634be75`.
Frozen cases: `tools/fixtures/mori-job-runway/cases.json` (sha256 `7098b008…01755fb4`, last commit `7634be75`).
Binary: `~/.local/bin/omp`, 256,702,432 bytes, sha256 `85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4`.
Upstream: `can1357/oh-my-pi` tag `v18.12.6` → commit `45c35e40c46166dc726ccc52f5d27f40f2449f99` (`gh api repos/can1357/oh-my-pi/git/refs/tags/v18.12.6`).

## Verdict

**None of the 21 frozen expected values is falsified as a derivation from rules 1–7.** A literal model of rule 1
plus the landed tool both reproduce every `configured` state and `effective` value in J01–J21 (details below).

Three frozen cases (J07, J08, J20) **disagree with real omp**. In each one the binary computes a number (100, 60
and 50) where the case expects `effective: null` / `RUNWAY_UNKNOWN`. That is an abstention in the safe direction:
no frozen case asserts a wrong number. It does contradict the contract's own description of the tool, which says
it "reports the per-session cap the binary computes" (contract.md:84). The canonical judge has to weigh that
tradeoff. It is not something a tool fix can resolve.

The serious defects sit **outside the frozen set**. Rule 1 is a line-based subset of YAML. With it, the landed tool
(HEAD `51ddd019`, tool commit `09f55b62`) gives a **wrong number with exit 0** on 8 valid YAML forms. It also
reports `set` with exit 0 on 3 files that omp refuses to load at all. Four of these are forced by the contract's
literal wording. Four are fixable inside it.

On the host, the tool's live answer (`set 200`, clamp 100, `effective 100`, `RUNWAY_CLAMPED`) matches what the
binary computes. No other settings layer is present on this host.

## Real semantics, from bytes and from upstream source

1. **Clamp site.** The binary has one regex match for rule 2, at offset 164406766:
   `const Ui = !u.parentTaskPrefix ? new Xm({ maxRunningJobs: () => Math.min(100, XPe.get(R)) }) : undefined;`.
   Upstream is [sdk.ts#L2282-L2286](https://github.com/can1357/oh-my-pi/blob/v18.12.6/packages/coding-agent/src/sdk.ts#L2282-L2286)
   (`Math.min(100, cfgAsyncMaxJobs.get(settings))`). This is the only `Math.min(N, X.get(Y))` shape anywhere in the
   binary (python scan: `shape-only Math.min(N, X.get(Y)) sites: 1`). The other two `maxRunningJobs` hits are the
   job-manager constructor at 160032417 and a bytecode atom table at 94971828; the rule-2 regex matches neither.
   The export map at 154750965, `cfgAsyncMaxJobs: () => XPe`, ties `XPe` to the setting.
2. **Cap getter.** Binary at 160032417+: `return Math.max(1, Math.floor(t ?? v));` with `var v = 15;`. Upstream is
   [job-manager.ts#L331-L335](https://github.com/can1357/oh-my-pi/blob/v18.12.6/packages/coding-agent/src/async/job-manager.ts#L331-L335)
   with `DEFAULT_MAX_RUNNING_JOBS = 15` ([#L43](https://github.com/can1357/oh-my-pi/blob/v18.12.6/packages/coding-agent/src/async/job-manager.ts#L43)).
   The refusal is `activeCount >= maxRunningJobs`, where `activeCount` counts only `running && !queued` jobs
   ([#L362-L373](https://github.com/can1357/oh-my-pi/blob/v18.12.6/packages/coding-agent/src/async/job-manager.ts#L362-L373)).
3. **Setting read.** `XPe.get(R)` resolves through `kme.compute`. A raw value is used only when
   `typeof raw === "number" && Number.isFinite(raw)`. Anything else, including null, a string, a boolean,
   `.inf` or `.nan`, logs `Settings: ignoring invalid value, using the default` and returns `default: 100`.
   Upstream is [registry.ts#L609-L614](https://github.com/can1357/oh-my-pi/blob/v18.12.6/packages/coding-agent/src/config/registry.ts#L609-L614)
   and [#L645-L650](https://github.com/can1357/oh-my-pi/blob/v18.12.6/packages/coding-agent/src/config/registry.ts#L645-L650).
   `async.maxJobs` declares no `env` ([tools/settings.ts#L941-L946](https://github.com/can1357/oh-my-pi/blob/v18.12.6/packages/coding-agent/src/tools/settings.ts#L941-L946)),
   so no environment variable overrides it.
4. **Parser.** The parser is `var {JSONC: uwe, YAML: OE } = globalThis.Bun` (binary offset 154910486), called as
   `OE.parse` in settings `#ge`. omp embeds `Bun v1.4.3 (c6da4a4d3)`. A YAML parse error, or a root that is not a
   mapping, sends the file to `#Be`. On a writable startup, `#Be` renames it to `<file>.broken-<ts>-<pid>-<uuid>`
   and omp exits with `Settings config is invalid` ([docs/settings.md#L38](https://github.com/can1357/oh-my-pi/blob/v18.12.6/docs/settings.md#L38)).
   During a live reload, the session keeps its last good values instead ([#L104](https://github.com/can1357/oh-my-pi/blob/v18.12.6/docs/settings.md#L104)).
5. **Layers.** The merge order is `#$e`: global, then project, then configOverlay, then overrides (binary at 156344920+).
   The documented precedence ([docs/settings.md#L122-L127](https://github.com/can1357/oh-my-pi/blob/v18.12.6/docs/settings.md#L122-L127)) is:
   runtime overrides (including the RPC `protocolDefault` pin), then `--config` / `PI_CONFIG_FILES` overlays, then
   `<cwd>/.omp/settings.json` then `<cwd>/.omp/config.yml`, then the global `config.yml` **or `config.yaml`**
   (`var Fm = ["config.yml", "config.yaml"]`, offset 147633942), then the default. The global directory moves with
   `OMP_PROFILE`/`PI_PROFILE` (to `~/.omp/profiles/<p>/agent`) and with `PI_CODING_AGENT_DIR`. A configured `null` in
   a higher layer reads as unset, which means the default, not the lower layer ([#L168](https://github.com/can1357/oh-my-pi/blob/v18.12.6/docs/settings.md#L168)).
   `Rr` is a plain nested lookup (binary at 156273569), so a flat top-level key `"async.maxJobs": 50` is never read.
6. **Ownership.** Each root session (no `parentTaskPrefix`) constructs its own manager. Its subagents receive the
   parent's manager (`asyncJobManager: P.asyncJobManager`). The first root also becomes the legacy singleton:
   `if (Ui && !Xm.instance()) Xm.setInstance(Ui)`, upstream [sdk.ts#L2279-L2281](https://github.com/can1357/oh-my-pi/blob/v18.12.6/packages/coding-agent/src/sdk.ts#L2279-L2281)
   ("Every root owns its jobs … Children use the exact manager passed by their parent") and [#L2573](https://github.com/can1357/oh-my-pi/blob/v18.12.6/packages/coding-agent/src/sdk.ts#L2573).
   The cap is recomputed on every `register`, from that root's `settings`.

## Findings by hunt target

### F1 — `Math.floor` on non-integers (rule 4)
- **Counterexample.** `maxJobs: 50.7` gives 50 in real omp. `0.5` gives 1, and `150.5` gives 100 (Bun probe E04,
  E05, E03). Rule 1 calls all three `malformed`, so the result is `RUNWAY_UNKNOWN`, exit 2. The landed tool agrees with rule 1.
- **Impact.** Abstention only. Rule 4's formula `max(1, min(clamp, base))` leaves out the floor, which is safe only
  because rule 1 admits integers alone. If rule 1 ever accepts floats, rule 4 has to add `floor`.
- **Frozen values:** not falsified. No frozen case uses a float.

### F2 — NaN/undefined fallback (`t ?? v`)
- **Finding.** The fallback is unreachable at this call site. `Math.min(100, x)` never returns null or undefined,
  and `x` is always a finite number, because `accepts` sends every non-finite or non-number value to `default: 100`
  (registry.ts#L614, #L645-L650). The NaN path, where `NaN ?? 15` is NaN, `Math.max(1, NaN)` is NaN and
  `activeCount >= NaN` is false (an uncapped manager), would need a non-number to get past `accepts`. No settings
  layer allows that: runtime overrides go through `assertWritable` (binary `#G`).
- **Impact.** None. J09 ("never unclamped") is still the right design.
- **Frozen values:** not falsified.

### F3 — Non-integer and null values (rule 1 `malformed`) vs the binary's default substitution
- **Counterexample.** J07 `maxJobs: abc` gives 100 in real omp: the raw value is a string, so the default applies.
  The frozen case expects `effective: null`, `RUNWAY_UNKNOWN` (cases.json:146-167). The same holds for `"200"`,
  `'50'`, an empty value, `~`, `null`, `true`, `.inf`, `.nan`, `5_0` and `!!int "50"`: Bun returns the string
  `"50"` for the last one, so all of these give 100. `async: null` and `async: {}` also give 100.
- **Impact.** Abstention, not a wrong number. It does conflict with contract.md:84, "reports the per-session cap
  the binary computes".
- **Frozen values:** J07 is consistent with rule 1 but disagrees with real omp. This is a tradeoff for the judge.
  The smallest safe correction is wording: the knowledge entry should say "`malformed` abstains; the binary itself
  substitutes the default 100 for any non-finite-number value".

### F4 — YAML forms the line-based rule 1 misreads (the main defect)
Probe setup: Bun 1.4.3+c6da4a4d3, the same revision omp embeds. `Bun.YAML.parse`, then the root-mapping check,
`Rr(["async","maxJobs"])`, `accepts`/default, `Math.min(100, ·)`, and `Math.max(1, Math.floor(·))`. Each form was
then run through the landed tool (`git show 51ddd019:tools/mori-job-runway.py`, `--binary ~/.local/bin/omp`).

| Form (config text) | real omp cap | landed tool | Class | Forced by contract text? |
|---|---|---|---|---|
| `"async":\n  maxJobs: 50` | 50 | absent → `RUNWAY_DEFAULT` 100, exit 0 | wrong value | yes ("no `async:` line" → absent) |
| `async :\n  maxJobs: 50` | 50 | absent → DEFAULT 100, exit 0 | wrong value | yes |
| `\ufeffasync:\n  maxJobs: 50` (BOM) | 50 | absent → DEFAULT 100, exit 0 | wrong value | yes |
| `async:\n  "maxJobs": 50` | 50 | absent → DEFAULT 100, exit 0 | wrong value | yes ("no direct `maxJobs`") |
| `defaults: &d\n  maxJobs: 50\nasync:\n  <<: *d` (merge key) | 50 | absent → DEFAULT 100, exit 0 | wrong value | yes |
| `async:\n  ? maxJobs\n  : 50` (explicit key) | 50 | absent → DEFAULT 100, exit 0 | wrong value | yes |
| `async:\n  maxJobs: 50\nasync:\n  maxJobs: 60` (two blocks; Bun keeps the last) | 60 | set 50 → `RUNWAY_AS_CONFIGURED`, exit 0 | wrong value | **no**: the contract is silent; the tool takes the first match (tool lines 155-162) |
| `async:\n  maxJobs: 50#x` (`#` with no preceding space is not a comment) | 100 (string) | set 50 → AS_CONFIGURED, exit 0 | wrong value | **no**: `_strip_comment` cuts at any `#` (tool lines 113-118) |
| `async:\n  maxJobs: 50\n---\nasync:\n  maxJobs: 70` (two documents) | omp refuses: root not a mapping, file moved to `.broken-*` | set 50, exit 0 | reports a file omp rejects | **no** (two `async:` lines) |
| `async:\n\tmaxJobs: 50` (tab indent) | omp refuses: `Tab characters cannot be used as indentation` | set 50, exit 0 | reports a file omp rejects | **no**: `_indent_of` counts tabs (tool line 127) |
| `async:\n  note: "x\n  maxJobs: 9\n  "` (multi-line quoted scalar) | omp refuses: `Unexpected character` | set 9, exit 0 | reports a file omp rejects | no (needs scalar tracking) |

The same probe also covered forms where the tool and omp agree: CRLF line endings, trailing whitespace after
`async:` or after the value, `---` at the start, `+50`, `0050`, `-5` (1 for both), a huge integer (100), a
top-level dotted key, and a sequence under `async`. The remaining forms in the probe (hex, octal, `1e2`, a float,
an anchor on the value, `async: *alias`, J08-style duplicates after a column-0 comment) all abstain.

- **Impacted axes:** coverage, which is C2's axis. A wrong number with exit 0 is a false runway claim. Calibration
  also suffers: `RUNWAY_DEFAULT`/exit 0 claims a value the binary would not compute.
- **Smallest safe correction.** None of these changes any J01–J21 expectation; I re-checked every frozen config
  against each one.
  1. Treat a second `async:` header line as `malformed`, the same way rule 1 already treats a duplicate `maxJobs`.
  2. Treat `#` as a comment only at the start of the value or after whitespace.
  3. Treat a tab in the leading indentation inside the block as `malformed`.
  4. Treat any column-0 line that YAML could read as an `async` key but rule 1 does not (quoted, `async :`, a BOM
     prefix, `? `) as `malformed` rather than `absent`. The same goes for a direct child that is a quoted
     `maxJobs`, a `<<:` merge, or a `? ` explicit key.

  Items 1–3 are fixable inside the contract text. Item 4 departs from rule 1's literal "`absent` when … no `async:`
  line / no direct `maxJobs`". Until the next contract can widen `malformed`, the knowledge entry has to name these
  forms as a stated bound.

### F5 — Settings merged from other sources (rule 1 scope, verdict labels)
- **Counterexample (no config.yml, config.yaml present).** Under rule 1, no `config.yml` means `absent` →
  `RUNWAY_DEFAULT` 100, exit 0. Real omp loads `~/.omp/agent/config.yaml` instead (`Fm` order; docs/settings.md#L17).
  If that file has `async:\n  maxJobs: 40`, the tool says 100 and omp computes 40.
- **Also not visible to the tool:** a project `<cwd>/.omp/config.yml` or `settings.json`, which is per root session
  cwd; `--config` / `PI_CONFIG_FILES` overlays; runtime overrides; a profile (`OMP_PROFILE`, `PI_PROFILE`) or
  `PI_CODING_AGENT_DIR` relocating the global file; and a higher-layer `maxJobs: null` hiding a global 200.
- **What does not change the answer:** the RPC `protocolDefault: ["rpc"]` pin. `pinDefaultValue` skips settings
  that are already configured, and otherwise pins the same 100.
- **Impact.** contract.md:83 already bounds the scope ("one config file, not project-level or environment
  overrides"), so this is not a hidden defect. But the verdict names `RUNWAY_AS_CONFIGURED` and `RUNWAY_DEFAULT`,
  with exit 0, read as statements about the live session.
- **Smallest correction.** Have the knowledge entry and the evidence state that the verdict covers the global layer
  only. A future rule could report `config.yaml` presence as a reason. No frozen value is affected.
- **Host check, layer by layer (all observed):**
  - Live omp is pid 3591, started 2026-10-22T07:56:19Z, with `exe=/home/vgpnk/.local/bin/omp` (not deleted).
  - Its command line has `argc=2` and `config_flags=0`, `mode_flags=0`, `profile_flags=0`.
  - `override_env_vars=0` for `PI_CONFIG_FILES`, `OMP_PROFILE`, `PI_PROFILE` and `PI_CODING_AGENT_DIR` (names only were checked).
  - Its cwd is `/home/vgpnk/Projects/shokunin`, whose `.omp/` holds only `agents`: no `config.yml` and no `settings.json`.
  - `~/.omp/agent/config.yaml` does not exist, and `~/.omp/profiles/` is empty.
  - The real the operator's OMP settings file (250 lines, LF endings, no tabs, no BOM; first line `setupVersion: 2`) has
    exactly one `^async` line, at 244, followed by `  maxJobs: 200` at 245. Rule 1 reads `set 200`, and Bun reads 200.
  - Conclusion: on this host, the tool's 100 / `RUNWAY_CLAMPED` equals the binary's cap for that session.

### F6 — Clamp pattern matching dead code (rule 2)
- **Finding.** On 18.12.6 there is no dead-code match. The single match is the live root-session constructor
  (sdk.ts#L2282-L2286), and it is the only `Math.min(N, X.get(Y))` shape in the binary.
- **Residual risk.** Rule 2 does not bind the `.get(ID)` identifier to the `async.maxJobs` setting. A future
  binary could keep a stale or dead `maxRunningJobs: () => Math.min(K, Other.get(s))` site, for example from a
  bundled older SDK or a different setting. The tool would then report `found K`.
- **Correction (next round only).** Capture the identifier and require `var <ID> = h({ id: "async.maxJobs"`, or the
  export `cfgAsyncMaxJobs: () => <ID>`. That would flip **J17**, whose case is `a$.get(b)` against `var XPe`
  (cases.json:379-401), so it cannot land against the frozen set.
- **Frozen values:** not falsified.

### F7 — Is "effective" per process or per session?
- **Counterexample to the contract's live-fact wording.** contract.md:40 says "this omp process refuses `task`
  calls while 100 or more background jobs run". In fact the cap belongs to each **root session**, and its subagent
  tree shares it (sdk.ts#L2279-L2286). A process hosting N root sessions, such as an RPC or ACP host, has N
  independent caps of 100 each.
- **Also:** the cap is recomputed on every `register` from that root's settings. That makes it cwd-scoped (project
  layer) and lets it follow live reloads without a restart (docs/settings.md#L104). If a reload fails, the session
  keeps its last good value while the file on disk says something else, so the tool reading the file can disagree
  with a live session.
- **Impact.** The scope bound at contract.md:84 ("per-session cap") is correct if "session" means the root session
  together with its subagents. The live-fact sentence at contract.md:40 is imprecise, which is a provenance-wording
  issue. No frozen value is affected.
- **Smallest correction.** The knowledge entry should say: "per root session, shared with its subagents; evaluated
  at each job registration from that root's merged settings".

### F8 — Labels (minor)
J12 (`maxJobs: 0`, effective 1, cases.json:262-284) is labelled `RUNWAY_CLAMPED`, but the value was raised to 1
by the floor, not reduced by the clamp. Rule 5 makes this label correct as written; it is a naming nit only.
J18 (a clamp of 300) also works against real semantics: `min(300, 250)` is 250.

## Frozen-case table (rule model vs real omp)
Rule model: a literal rule-1 implementation (`/tmp`, now removed), plus the landed tool. Real omp: the Bun 1.4.3
probe. The probe used the host clamp of 100. J09, J10, J14, J18 and J21 carry synthetic binaries, so they are
judged on their own bytes.

| Case | Frozen expect | Rule 1 / landed tool | Real omp | Falsified? |
|---|---|---|---|---|
| J01–J04, J06, J11–J13, J15, J17, J19, J21 | as frozen | same | same value | no |
| J05 (no file) | DEFAULT 100 | same | 100 in the selftest temp dir; on a host with `config.yaml` it would differ (F5) | no |
| J07 `abc` | UNKNOWN, null | same | 100 (default substituted) | no; disagrees with real (F3) |
| J08 duplicate `maxJobs` | UNKNOWN, null | same | 60 (Bun keeps the last duplicate) | no; disagrees with real (abstains) |
| J20 `async: {maxJobs: 50}` | UNKNOWN, null | same | 50 | no; disagrees with real (abstains) |
| J16 directory | UNKNOWN | same | omp startup error (`Failed to read settings config`) | no |
| J09, J10, J14 (synthetic binaries) | UNKNOWN | same | n/a (not real omp bytes) | no |
| J18 (clamp 300) | AS_CONFIGURED 250 | same | 250 against that binary | no |

J01's `binary` text is byte-identical to the real site and setting definition (binary offsets 164406766 and 155231595).

## Reproduction
- Bun probe: `bun probe.mjs cases.json the operator's OMP settings file`. For each config text it runs `Bun.YAML.parse`;
  treats a null or undefined root as `{}`; marks a non-object or array root as invalid; looks up
  `raw = doc?.async?.maxJobs` as a plain nested get; sets `v = (typeof raw === "number" && Number.isFinite(raw)) ? raw : 100`;
  and reports `cap = Math.max(1, Math.floor(Math.min(100, v) ?? 15))`.
- Landed-tool run: `python3 -I -B <(git show 51ddd019:tools/mori-job-runway.py) --config <edge>.yml --binary ~/.local/bin/omp`
  over the edge configs. With no `--config`, the tool gives `configured set 200`, `clamp found 100 sites 1`,
  `setting_default found 100 sites 1`, `effective 100`, `RUNWAY_CLAMPED`, `binary_sha256 85d9daf3…7ccfa4`.
- Upstream files fetched raw at `v18.12.6` (sha256): job-manager.ts `0f37afaa…544e7`, sdk.ts `c0228add…6957`,
  config/settings.ts `0d740c1e…7771`, tools/settings.ts `51497414…0507`, config/registry.ts `757ff479…5d27`,
  docs/settings.md `0b2e1457…5883`.
- No session transcripts were read. omp was not run; the binary was read only as bytes, using Python.

## Tooling record
- **bun 1.4.3+c6da4a4d3**, installed from the official GitHub release
  (`oven-sh/bun` `bun-v1.4.3/bun-linux-x64.zip`). It passed `sha256sum -c` against that release's
  `SHASUMS256.txt` and was installed to `~/.local/bin/bun`.
- **Reason:** to run `Bun.YAML.parse` at the exact Bun revision embedded in omp (`Bun v1.4.3 (c6da4a4d3)`), so that
  YAML semantics are observed rather than inferred. No pacman transaction was run.

## Writes
This report only. Throwaway probe files lived under `/tmp/criticc2` and are removed. Nothing else was written in
the lane, at the fleet root, or in sibling lanes. The only git commands run were `log`, `show`, `cat-file` and `rev-parse`.

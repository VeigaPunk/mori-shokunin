# ReopenBinaryRow: S102 re-derivation (round 25, wave 2)

Seat: MoriR25.ReopenBinaryRow (leaf, read-only on the lane). Checks run 2026-10-22 against `corpus/SOURCES.md:108` (S102) and the installed file `~/.local/bin/omp`.

## Verdict

**Held** for every fact S102 states: sha256, size, both byte offsets, both quotes, both version strings, both owning-module markers, and the claim that the installed file is byte-identical to the v18.12.6 release asset `omp-linux-x64`.

**Weakened** in three places: the row's teaching sentence overstates the clamp (F1), the row's anchors and used-by cell miss facts that the knowledge note cites to S102 (F2), and the schema quote collapses whitespace (F5, cosmetic). **One downstream sentence is broken**: the headline of `corpus/lessons/round-25.md:9` (F4). One lesson quote is misattributed to S102 (F3).

No sha256, size, offset, quote, marker, version string, or digest claim failed.

## Check results

| S102 claim | Result | Where |
|---|---|---|
| sha256 `85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4` | held | §1, §2, §4 |
| size 256702432 bytes | held | §1, §2, §4 |
| offset 164406766 = `maxRunningJobs: () => Math.min(100, XPe.get(R))` (capture 100) | held, exact bytes | §2 |
| offset 155231590 = `id: "async.maxJobs", … default: 100` (capture 100) | held; quote is whitespace-collapsed (F5) | §2 |
| owning marker 164380488 = `// packages/coding-agent/src/sdk.ts` | held; nearest preceding marker | §3 |
| owning marker 155206756 = `// packages/coding-agent/src/tools/settings.ts` | held; nearest preceding marker | §3 |
| version byte 256648593 = `--user-agent=omp/18.12.6` | held, exact bytes | §3 |
| manifest byte 151991030 = `version: "18.12.6"` | held, exact bytes | §3 |
| sha256 equals the v18.12.6 release asset digest | held | §4 |

## 1. Installed file

- `stat`: `~/.local/bin/omp`, regular file, 256702432 bytes, mode 755, not a symlink (`readlink -f` returns the same path), mtime 2026-10-21 20:37:24 -0300.
- First 16 bytes: `7f 45 4c 46 02 01 01 00 …` (ELF, 64-bit, little-endian).
- `sha256sum`: `85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4`.

## 2. Locator (run verbatim from SOURCES.md:108, from /tmp, read-only)

Output:

```
sha256 85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4 size 256702432
164406766 …rentTaskPrefix ? new Xm({ maxRunningJobs: () => Math.min(100, XPe.get(R)) }) : undefined; if (Ui) {
155231590 …tion" } }); var XPe = h({ id: "async.maxJobs", protocolDefault: ["rpc"], type: "number", default: 100 }); var YPe = h({ id: "asyn
```

Independent mmap check, anchored `re.match` at each row offset:

- 164406766 → `b'maxRunningJobs: () => Math.min(100, XPe.get(R))'`, capture `100`.
- 155231590 → `b'id: "async.maxJobs",\n  protocolDefault: ["rpc"],\n  type: "number",\n  default: 100'`, capture `100`. The bytes contain newlines and two-space indents; the row collapses them (F5).

Full-file counts: `maxRunningJobs` occurs 3 times (one clamp site, one string-table name, one constructor field `this.#P = e.maxRunningJobs`). `async.maxJobs` occurs 2 times (string table and schema object). `new Xm(` occurs once, at 164406753; it is the only job-manager construction in the binary.

## 3. Markers and version strings

- 164406766: nearest preceding marker is `// packages/coding-agent/src/sdk.ts` at 164380488 (distance 26,278). The next marker, `preflight.ts`, is at 164480953.
- 155231590: nearest preceding marker is `// packages/coding-agent/src/tools/settings.ts` at 155206756 (distance 24,834). The next marker, `thinking-display.ts`, is at 155235147.
- 256648593: exact bytes `--user-agent=omp/18.12.6`.
- 151991030: exact bytes `version: "18.12.6"`, inside a manifest block (`version: "18.12.6",\n  descript…`).

## 4. Digest identity with v18.12.6

- `gh api repos/can1357/oh-my-pi/releases/tags/v18.12.6` (gh 2.102.0, pre-installed at `~/.local/bin/gh`): asset `omp-linux-x64`, size 256702432, digest `sha256:85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4`, updated 2026-10-21T21:02:52Z. The release was published 2026-10-21T21:02:53Z.
- The same digest comes back from the REST endpoint via `curl`.
- Ordinary fetch: `curl -fsSL -L https://github.com/can1357/oh-my-pi/releases/download/v18.12.6/omp-linux-x64` gives sha256 `85d9daf3…ccfa4` and 256702432 bytes. `cmp ~/.local/bin/omp <download>` prints nothing and exits 0, so the files are byte-identical.
- Ordinary fetch of `SHA256SUMS.txt` (934 bytes; its own digest `72ebc3d9…64e5` matches the API) lists line 8: `85d9daf3…ccfa4  omp-linux-x64`.
- The releases HTML page shows the release at commit `45c35e4` (= `45c35e40c46166dc726ccc52f5d27f40f2449f99`, the commit S101 and S103 name). Its asset list is loaded by script and did not render, so the page is not a digest source here.
- `gh attestation verify … --repo can1357/oh-my-pi` fails with HTTP 404 for `sha256:85d9…`. None of the 12 release assets is a detached signature. The identity claim is therefore "equal to GitHub's recorded digest and to SHA256SUMS.txt", not a signed provenance claim.

## 5. The lane tool reads the same bytes

Copied `tools/mori-job-runway.py` (lane working copy, read only) into scratch and ran `python3 -I -B mori-job-runway.py --config <absent path> --binary ~/.local/bin/omp`. Output: `binary_sha256` `85d9daf3…ccfa4`; `clamp` found, value 100, sites 1; `setting_default` found, value 100, sites 1; `effective` 100; `RUNWAY_DEFAULT`; exit 0. I passed an absent config path so the private `~/.omp` config was not read. The tool's `CLAMP_RE` (line 114) and `DEFAULT_RE` (line 117) are the row's two regexes.

## 6. Upstream mapping (ordinary fetch at tag v18.12.6)

- `packages/coding-agent/src/sdk.ts` (sha256 `c0228add…6957`, matches the note): lines 2283–2284 are `new AsyncJobManager({ maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)), })`.
- `packages/coding-agent/src/tools/settings.ts` (sha256 `514974143…0507`, matches the note): lines 941–946 are `cfgAsyncMaxJobs = register({ id: "async.maxJobs", protocolDefault: ["rpc"], type: "number", default: 100 })`.
- Minified names, confirmed from context: `XPe` = `cfgAsyncMaxJobs`; `R` = the settings instance (the same `R` is passed as `settings: R` to the adjacent `X9e` call); `Xm` = `AsyncJobManager`.

## 7. The clamp is the live cap (what the row's teaching depends on)

- Constructor of `class Xm`: `this.#P = e.maxRunningJobs` (literal at 160032417).
- `get #R()` (offset 160032728): `const t = typeof e === "function" ? e() : e; return Math.max(1, Math.floor(t ?? v));`, with `var v = 15;` at 160031518 in the job-manager module.
- `get atCapacity()` (offset 160032861): counts jobs that are running and not queued, then `return e >= this.#R`. The clamp is therefore re-read on every capacity check.
- The clamp is an upper bound only. `min(100, x)` passes 1–100 through unchanged. Values ≤ 0 resolve to 1, and non-integers are floored. JS check (bun 1.4.3, no omp run): clamp(150) = 100, clamp(0) = 1, clamp(2.7) = 2, clamp(NaN) = NaN, and `0 >= NaN` is `false`. A NaN would therefore remove the cap, so I checked that it cannot arrive:
  - `accepts` for `"number"` is `typeof e === "number" && Number.isFinite(e)` (registry module, offset 153979920).
  - `compute` replaces a rejected value with the default and logs "Settings: ignoring invalid value, using the default" (offset 153980567).
  - Base `CDe.get` (offset 153973625) calls `compute`.
  - The string parser throws on non-finite numbers (offset 153978856).
  - `async.maxJobs` has no `env` binding, so `envValue()` returns early (offset 153977675).
  - Verified by reading these bodies, not by executing them.

## 8. RPC protocolDefault does not change the value

`tN("rpc", ve)` (offset 165639147) calls `pinDefault` on each setting whose `protocolDefault` includes `"rpc"`. `pinDefaultValue` (offset 156285030) writes `u.default` (100) as an override unless the setting is configured. RPC hosts therefore get the same 100. Upstream `settings.ts:926–927` documents this as "neutral background-job defaults".

## 9. Other facts the knowledge note cites to S102

- Byte 160033359: the text `Background job limit reached (${o}). Wait for running jobs to finish or cancel one.` starts there. Correct.
- `var v = 15;` at 160031518: correct. Its consumption is only checked at `t ?? v` in `get #R()`; I did not scan the rest of the module for other uses of `v` (single-letter identifier).
- The `get #R()` resolver and `atCapacity` chain (§7): correct.

These facts are correct but the row does not anchor them (F2).

## Findings

**F1 — LOW. Row S102, teaching sentence overstates the clamp.** The row says the build "clamps the harness background-job runway at 100 whatever `async.maxJobs` is set to". Read literally, every configured value becomes 100, which is false: 1–100 pass through (§7). The second clause ("a configured value above 100 cannot raise the cap") is correct.
- Smallest fix: "The installed build caps the runway at 100: a configured value above 100 is cut to 100, values from 1 to 100 are honoured, and the resolver floors the result at 1."

**F2 — LOW. Row S102, anchors and used-by do not cover what downstream cites.** `corpus/knowledge/harness-job-capacity-r25.md` cites S102 for byte 160033359 (template), `var v = 15;` (160031518) and the `get #R()` resolver (lines 74–75 and 102–103 of the note). The row's anchor cell lists none of them, and its locator cannot reproduce them. The used-by cell also omits `corpus/lessons/round-25.md`, which cites S102 at its line 62 and again at line 10.
- Smallest fix: add the three offsets to the anchor cell (or state that they were checked by hand), and add `corpus/lessons/round-25.md` to used-by.

**F3 — LOW. Lesson quote attributed to S102 is the source form.** `corpus/lessons/round-25.md:10` quotes `Math.min(100, cfgAsyncMaxJobs.get(settings))` with the tag "(S099, S102)". That is upstream text (`sdk.ts:2284`). The S102 bytes read `Math.min(100, XPe.get(R))`. The meaning is the same, but the quote is attributed to the wrong source.
- Smallest fix: quote the source form against S099 and the minified form against S102 at byte 164406766.

**F4 — MEDIUM. Lesson headline is false for configured values below 100.** `corpus/lessons/round-25.md:9` reads "The harness job cap is 100, whatever the config says." A configured 50 gives a cap of 50 (§7). The body is right (line 12: a configured 200 is cut to 100); the headline is not.
- Smallest fix: "The harness job cap is at most 100, whatever the config says."

**F5 — LOW (cosmetic). Row S102 quote collapses whitespace.** The bytes at 155231590 span four lines. The locator's print replaces newlines with spaces, and the row copies that form. The tokens match.
- Smallest fix: write "(newlines collapsed)" beside the quote.

**F6 — INFO. "own-work" hides that the bytes are the public release asset.** The installed file is byte-identical to `omp-linux-x64` at v18.12.6, so the row can be re-derived from a public URL without this host. The row gives neither the URL nor the digest, and it does not say that no attestation exists.
- Smallest fix: add the asset URL and digest `85d9daf3…ccfa4` to the anchor cell, and note "no GitHub attestation (HTTP 404) and no detached signature; identity is by GitHub's recorded digest".

## Residual risk

- Static reading only. The cap's effect on running job counts is unmeasured; the row says it is not a live run, and this seat did not run omp.
- Provenance rests on GitHub's recorded digest and SHA256SUMS.txt. No attestation or signature exists to check, so a compromised release would be indistinguishable here.
- The NaN-cannot-arrive conclusion (§7) comes from reading the bodies, not from executing the settings code.
- Only the glibc x64 build of v18.12.6 was checked. Other platform assets have other digests; the row does not claim anything about them.
- The subagent sharing path (`Xm.instance()`, three `setInstance` sites) was observed but not traced end to end. The knowledge note's "no shipped session can run more than 100" rests on the single constructor site, which I verified.

## Verification gaps

- Not run: omp itself (not permitted for this seat); the tool's `--selftest` (C2 seat's job); any live job-count measurement.
- Not read: the host's own `~/.omp` config (private; not needed for S102).
- Not re-fetched: `job-manager.ts` (S098). The note's claim that the string "occurs once in the source" is therefore unchecked here.
- Not exhaustively checked: whether `v` is used anywhere besides `t ?? v`.
- The releases HTML did not render its asset table. The digest came from the REST API and from an ordinary download, which together are sufficient for the claim.

## Tool and install record

- No tool was installed or upgraded in this seat. No pacman, no `RULES.md` read was needed.
- Pre-existing tools used: `gh` 2.102.0 (`~/.local/bin/gh`), Python 3.14.8 (system `python3`), `bun` 1.4.3 (JS arithmetic check only; omp not run), `curl`, `sha256sum`, `cmp`, `stat`, `od`, `readlink`.
- Scratch: `/fast/scratch/hyaku/mori-r25/w2-ReopenBinaryRow` held the 256 MB asset copy, the two upstream files and a copy of the tool. It has been removed, and `~/.local/bin/omp` is unchanged (256702432 bytes).
- Lane: read-only. This report is the only file written. No git or jj command was run in the lane. No lane file was edited.

## Commands run

- `stat`, `readlink -f`, `od -N 16`, `sha256sum` on `~/.local/bin/omp`.
- The S102 locator, copied verbatim from `SOURCES.md:108`, run with `python3 -I -B -c` from /tmp.
- Python mmap checks: anchored `re.match` at 164406766 and 155231590; full-file `finditer` counts; nearest-preceding marker search; exact-bytes comparisons at 256648593 and 151991030; context windows for the resolver, `atCapacity`, the `accepts` / `compute` / `CDe.get` / `envValue` / `pinDefaultValue` / `tN` bodies.
- `gh api repos/can1357/oh-my-pi/releases/tags/v18.12.6 --jq …`, and the same JSON via `curl`.
- `curl -fsSL -L` of `omp-linux-x64`, `SHA256SUMS.txt`, and the upstream `sdk.ts` and `tools/settings.ts` at tag v18.12.6; `sha256sum`; `cmp`.
- `gh attestation verify … --repo can1357/oh-my-pi` (HTTP 404).
- `python3 -I -B mori-job-runway.py --config <absent> --binary ~/.local/bin/omp` on a private copy.
- `bun -e` for the `Math.min` / `Math.max` / `NaN` arithmetic.

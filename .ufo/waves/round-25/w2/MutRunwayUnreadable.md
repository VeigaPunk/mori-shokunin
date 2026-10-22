# Mutation probe — C2 unreadable/absent handling in `tools/mori-job-runway.py`

Seat: `MoriR25.MutRunwayUnreadable` (wave 2, mutation tester). Target: claim C2
(`tools/mori-job-runway.py`). Probe: unreadable/absent handling — a directory config read as
absent; a missing binary read as clamp-absent but with an effective value computed.

## Verdict

**WEAKENED — the claim's own rules hold, but one uncovered input lets a mutant through.**

- Every behaviour the claim states about the *config* path is held by the frozen 21: a directory
  config read as `absent` is **killed** (J16), and the symmetric "missing config read as
  `unreadable`" is **killed** (J05, J14).
- The "effective computed without a found clamp" behaviour is **killed** (J09, J10), so the
  combined mutant named in the assignment ("missing binary read as clamp absent but effective
  computed") is killed too.
- **One survivor**: an unopenable `--binary` (missing file, mode 000, or a directory) reported as
  `clamp.state: "absent"` / `setting_default.state: "absent"` instead of `"unreadable"`. Neither
  the frozen 21 nor the supplementary 18 exercises an unreadable or missing binary, so both
  detectors pass on the mutant. Severity **low**: no number and no verdict change
  (`effective` stays null, `RUNWAY_UNKNOWN`, exit 2) — only the two state labels lie, in the
  direction the tool's own rule 2 forbids ("An absent clamp is never read as 'no clamp'").

The after-value is not falsified: on this host the tool's live output is unaffected by every
mutant (the config and the binary are both readable). What is missing is test coverage, not
correct code.

## Where and how (private clone, never the lane)

- Private clone: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin
  /fast/scratch/hyaku/mori-r25/w2-MutRunwayUnreadable` (clone HEAD `07a31ae`). The lane checkout
  was never written to; only this seat's report file was written in the lane.
- The clone's tool bytes are identical to the lane's:
  `sha256(tools/mori-job-runway.py) = 5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411`
  in both. Fixtures identical too: `cases.json`
  `7098b008d614e84c4328af96d15badef700ea84b75a43ba4a375264a01755fb4`, `supplementary-cases.json`
  `8d09756d10a9f501b0fa69599e096ce6ef5f3cd9debda89b5de2bc094679ffd6`.
- Detector 1 (the claim's after-value): `python3 -I -B tools/mori-job-runway.py --selftest`.
- Detector 2 (the co-evolved file): `python3 -I -B tools/mori-job-runway.py --selftest --cases
  tools/fixtures/mori-job-runway/supplementary-cases.json`.
- Baseline on pristine bytes: `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` (exit 0) and
  `MORI_JOB_RUNWAY_SELFTEST: PASS 18/18` (exit 0). A baseline failure would have made every
  result below inconclusive; there is none.
- One mutant at a time; the tool file was restored from a pristine copy after every mutant
  (`sha256` above) and at the end of the run (`identical to pristine: True`).
- Driver, result JSON and the extra (non-lane) killer-cases file live only in the clone:
  `mutate.py`, `mutate-results.json`, `killer-cases.json`. After the run the clone was deleted
  (358 MB extract); the three probe files are kept outside the lane, in
  `/fast/scratch/hyaku/mori-r25/MutRunwayUnreadable-probe/`. The lane's tool bytes are unchanged
  (`sha256 5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411` after the probe).

## Mutants, detectors, verdicts

| id | mutation (one point unless noted) | detector 1 (frozen 21) | detector 2 (supplementary 18) | verdict |
|---|---|---|---|---|
| M1 | `_read_config_text`: `except IsADirectoryError` (line 231) returns `("absent", None)` instead of `("unreadable", None)` — **the assigned "directory config read as absent"** | `FAIL 20/21`, exit 2 — **J16**: `verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_DEFAULT'; exit: expected 2, got 0; configured.state: expected 'unreadable', got 'absent'; effective: expected None, got 100` | `PASS 18/18`, exit 0 | **KILLED** (by J16) |
| M4 | `_read_config_text`: `except FileNotFoundError` (line 229) returns `("unreadable", None)` instead of `("absent", None)` (symmetric control) | `FAIL 19/21`, exit 2 — **J05**: `verdict: expected 'RUNWAY_DEFAULT', got 'RUNWAY_UNKNOWN'; exit: expected 0, got 2; configured.state: expected 'absent', got 'unreadable'; effective: expected 100, got None`; **J14**: `configured.state: expected 'absent', got 'unreadable'` | `PASS 18/18`, exit 0 | **KILLED** (by J05, J14) |
| M2a | `_binary_sites`: `except OSError` on `open(path, "rb")` (lines 393-395) returns `("absent", None, 0)` instead of `("unreadable", None, 0)` | `PASS 21/21`, exit 0 | `PASS 18/18`, exit 0 | **SURVIVED** |
| M3 | `_effective`: the `clamp_state != "found"` guard is dropped, so a base value yields `effective = base` even with no found clamp | `FAIL 19/21`, exit 2 — **J09** and **J10**: `verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_AS_CONFIGURED'; exit: expected 2, got 0; effective: expected None, got 200` | `PASS 18/18`, exit 0 | **KILLED** (by J09, J10) |
| M2 | M2a + M3 together — **the assigned "missing binary read as clamp absent but effective computed"** | `FAIL 19/21`, exit 2 — **J09**, **J10** (same rows as M3) | `PASS 18/18`, exit 0 | **KILLED** (by J09, J10) |

Mutated-file hashes (before → after), tool bytes only:

| id | pristine sha256 | mutated sha256 |
|---|---|---|
| M1 | `5d90d7d4…12c3411` | `88e3927316f3f89a986f2a632b9f61ddcfb3c0570c16ef5e9a6b37741803a795` |
| M4 | `5d90d7d4…12c3411` | `e87f71b704d1c45ea826a52ebf9024b0e8abff2c6a452bfa617629febf0f13bb` |
| M2a | `5d90d7d4…12c3411` | `ca1a3b17fe2ec6f34b4694b650631f895a8b7f3e4ce8e95ee789dcd1c9f680ce` |
| M3 | `5d90d7d4…12c3411` | `6b04dfd94f5da08a16293188123ed276d97b885e9fa7dc928e40e3497428deef` |
| M2 | `5d90d7d4…12c3411` | `fedc52b1f47201a8e83e3231d4ee56a1cc85ccacc9efb12ced1728ff6c598fa3` |

Restoration evidence: after the last mutant the clone's `tools/mori-job-runway.py` hashed
`5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411` (identical to pristine), and
`git status --porcelain` in the clone shows only my three untracked probe files
(`mutate.py`, `mutate-results.json`, `killer-cases.json`) — no tracked file changed.

## The survivor: M2a (unopenable binary reported as clamp `absent`)

**Why it survives.** No case in `cases.json` (21) or `supplementary-cases.json` (18) has a binary
that cannot be read: every case's `binary` is a string, and `_materialize` always writes it
(`tools/mori-job-runway.py:542-561`), so the file exists and is readable in all 39 cases. The
`except OSError` branch in `_binary_sites` (`tools/mori-job-runway.py:393-395`) is therefore never
executed by either detector. The same is true of the tool's `path is None` branch — no case
exercises it either.

**What it does when it survives.** Pristine vs M2a on a missing binary:

```
$ python3 -I -B tools/mori-job-runway.py --config /tmp/nonexistent-cfg.yml --binary /tmp/nonexistent-omp.bin
```
pristine: `"clamp": {"state": "unreadable", …}, "setting_default": {"state": "unreadable", …}, "effective": null, "verdict": "RUNWAY_UNKNOWN"`, exit 2.
M2a: `"clamp": {"state": "absent", …}, "setting_default": {"state": "absent", …}, "effective": null, "verdict": "RUNWAY_UNKNOWN"`, exit 2.

The number and the verdict are unchanged; only the two state labels change. The pristine tool also
reports `unreadable` for a mode-000 binary and for a directory passed as `--binary` (checked
directly: `"clamp": {"state": "unreadable", …}` in both cases).

**Which input would kill it.** One case with no binary file (the `binary` key absent or null), for
example:

```json
{"id": "K01",
 "what": "binary file absent -> clamp unreadable, effective null, RUNWAY_UNKNOWN, exit 2",
 "config": "async:\n  maxJobs: 200\n",
 "expect": {"verdict": "RUNWAY_UNKNOWN", "exit": 2,
            "configured": {"state": "set", "value": 200},
            "clamp": {"state": "unreadable", "value": null, "sites": 0},
            "setting_default": {"state": "unreadable", "value": null, "sites": 0},
            "effective": null}}
```

I wrote exactly that (plus a config-absent variant K02) into the clone as `killer-cases.json` and
ran it: pristine → `MORI_JOB_RUNWAY_SELFTEST: PASS 2/2` exit 0; M2a → `MORI_JOB_RUNWAY_SELFTEST:
FAIL 0/2`, with `CASE K01: clamp.state: expected 'unreadable', got 'absent'; setting_default.state:
expected 'unreadable', got 'absent'` (and the same for K02). So the pristine tool is right and the
mutant is killable — the frozen and supplementary files simply do not contain the case.

**Does omp's real behaviour make it matter?** Only mildly, and the conclusion is that the *tool* is
right and the *fixtures* are thin:

- The clamp is compiled into the binary (`sdk.ts:2282-2284` at v18.12.6, and byte 164406766 of the
  installed `~/.local/bin/omp`, per the round-25 knowledge entry F2/S099/S102). A binary that
  exists but cannot be read still carries that clamp, so reporting `clamp.state: "absent"` asserts
  the opposite of the truth: it reads as "this omp build has no compiled cap". That is exactly the
  confusion rule 2 forbids ("An absent clamp is never read as 'no clamp'").
- Operationally it bites when `--binary` points at a stale or permission-denied path while a
  working `omp` is installed: the operator would conclude that raising `async.maxJobs` above 100
  would take effect, when the shipped clamp keeps it at 100. The tool's verdict and exit code stay
  safe (`RUNWAY_UNKNOWN`, exit 2), so nothing downstream acts on a false number — the damage is
  limited to a wrong field in the JSON.
- The mirror case (missing binary entirely) is moot for omp: with no binary there is no omp to ask.
  The `path is None` case (no `omp` on `PATH`) already returns `unreadable` in both pristine and
  M2a, so the mutant does not touch it.
- The live after-value is unaffected: on this host `~/.omp/agent/config.yml` (mode 0600) and
  `~/.local/bin/omp` (mode 0755) are both readable, so the live run is
  `configured set 200 / clamp found 100 / effective 100 / RUNWAY_CLAMPED`, exit 1 — identical under
  every mutant I applied.

## Upstream grounding for the config path (used for the killed mutants)

oh-my-pi v18.12.6 (`45c35e40c46166dc726ccc52f5d27f40f2449f99`),
`packages/coding-agent/src/config/settings.ts`, fetched as raw bytes on 2026-10-22 from
`https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/packages/coding-agent/src/config/settings.ts`
(169,977 bytes, sha256 `0d740c1ea27a5903d6e41d10f3582940d7496b11b3ebcf617b7ef47522e47771`):

- `:2037-2038` — a config read error is classified `isEnoent(error) ? { kind: "missing" } : { kind: "unreadable" }`.
  So upstream itself separates *missing* from *unreadable*, exactly as the tool does; a directory
  config is `unreadable` upstream, not `missing`.
- `:2354-2366` (`#unwrapYamlLoadResult`) — `missing` → `null` (defaults), `unreadable` → `throw new
  Error("Failed to read settings config …")`. So with a directory at `~/.omp/agent/config.yml` omp
  **refuses to load settings and throws**; it does not fall back to the default cap.

That makes M1 materially wrong, not merely contract-violating: the mutant would report
`RUNWAY_DEFAULT`, effective 100 for a harness that cannot start. The pristine tool's
`unreadable → RUNWAY_UNKNOWN, exit 2` matches upstream. The frozen case J16 already kills M1, so
the claim's stated rule is correct and enforced.

## Smallest fix (one line of scope, no tool change)

Add to `tools/fixtures/mori-job-runway/cases.json` (frozen file — the lane may prefer the
co-evolved `supplementary-cases.json`, which is not counted toward the after-value) one case with no
binary file, expecting `clamp`/`setting_default` `unreadable`, `effective` null,
`RUNWAY_UNKNOWN`, exit 2 — the `K01` shape above. The tool needs no code change: it already
answers that input correctly (verified `PASS 2/2` on the killer file).

If the lane prefers a code change instead of a fixture, the equivalent hardening is to keep the
`unreadable` state distinct in the JSON (it already is) — there is no code defect to fix; only the
fixture coverage is missing.

## What I did not do

- No change to the lane's tool, fixtures, contract or knowledge files; the only lane file written
  is this report.
- No `jj` command was run at the fleet root; no git write in the lane; no subagents dispatched.
- omp was never executed; the installed binary was read as bytes only, and upstream sources were
  opened by ordinary `curl` fetches of raw bytes at the pinned commit.
- The supplementary detector passed on every mutant (18/18 in all five runs), so it contributes no
  signal for this probe: it covers YAML-form abstentions (A2) and contains no unreadable/absent
  edge case at all.

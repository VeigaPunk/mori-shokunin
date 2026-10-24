# C2 binary locate facts — installed omp (omp/18.12.6)

Scout: MoriR25.BinaryLocateFacts. Claim: C2 (coverage, new PROVINCE ground). Surface read: only
`/home/vgpnk/.local/bin/omp`. No omp process was started; bytes were read with a read-only Python
`mmap`. Offsets below are **decimal byte offsets from byte 0 of the file**; offsets quoted for
`register(...)` calls point at the `.` of the `.register(` token.

## Binary identity

| Field | Value | Evidence |
|---|---|---|
| real path | `/home/vgpnk/.local/bin/omp` (regular file, not a symlink) | `ls -l` shows `-rwxr-xr-x`, no `->`; `readlink -f` returns the same path |
| size | 256,702,432 bytes | `stat -c '%s'` = `256702432` |
| sha256 | `85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4` | `sha256sum ~/.local/bin/omp` |
| mtime | `2026-10-21 20:37:24.615549837 -0300` = `2026-10-21T23:37:24Z`, epoch `1792625844` | `stat -c '%y %Y'` |
| format | ELF 64-bit (`\x7fELF\x02\x01\x01\x00`) | first 16 bytes |
| version | `18.12.6` appears at 96005424 next to `file:///$bunfs/root/chunks/cli-125ehg00.js` and `Coding agent CLI with re…`; package manifests at 147615522 (`@oh-my-pi/pi-natives`), 147633011 (`packages/utils/package.json`), 148842174 (`@oh-my-pi/pi-ai`) all read `"version": "18.12.6"` | byte dumps |

The JS bundle is embedded uncompressed between roughly byte 147,000,000 and 167,000,000, with
`// packages/coding-agent/src/...` provenance comments before each module. Byte offsets are stable
for this sha256.

## Contract regexes over the whole file (C2 rules 2 and 3)

- clamp `maxRunningJobs:\s*\(\)\s*=>\s*Math\.min\(\s*(\d+)\s*,\s*[\w$]+\.get\([\w$]+\)\s*\)`
  → **1 match, value `100`, at 164406766**.
- setting `id:\s*"async\.maxJobs",[^}]{0,300}?default:\s*(\d+)`
  → **1 match, value `100`, at 155231590**.

No second `XPe.get(` (the settings accessor used in the clamp) exists anywhere in the file: one hit,
at 164406802. The literal `async.maxJobs` occurs twice (96085908 = settings-UI string table, no
`id: "` prefix; 155231590 = the definition), so the contract regex cannot false-positive on the
string table.

## (1) Clamp and the guard on manager construction

Module provenance: `// packages/coding-agent/src/sdk.ts` at 164380488.

- Guard + clamp, bytes 164406720–164406816 (line breaks are in the file):

```
const Ui = !u.parentTaskPrefix ? new Xm({
    maxRunningJobs: () => Math.min(100, XPe.get(R))
  }) : undefined;
```

  - `const Ui = !u.parentTaskPrefix ? new Xm({` — 164406720 (15-word folded quote:
    `const Ui = !u.parentTaskPrefix ? new Xm({ maxRunningJobs: () => Math.min(100, XPe.get(R)) }) : undefined;`)
  - `maxRunningJobs: () => Math.min(100, XPe.get(R))` — **164406766** (7 words verbatim).
  - `}) : undefined;` closes the ternary; `Ui` is `undefined` exactly when `u.parentTaskPrefix` is set.
- `Xm` is the `AsyncJobManager` class: `// packages/coding-agent/src/async/job-manager.ts` at
  160031363, `var cF = Symbol("AsyncJobManager shutdown")` at 160031539, `class Xm {` at 160031683.
  (Two other byte matches for `class Xm` exist: 168511448 is `class Xme` from puppeteer-core, and
  169265347 is a dependency-local `class Xm` for `AnchoredClock`; neither is the job manager.)
- Only one `new Xm(` exists in the file (164406753). No other construction site.
- Root-only singleton: `if (Ui && !Xm.instance()) Xm.setInstance(Ui);` at 164415466 (inside
  `if (!u.parentTaskPrefix) {` at 164415374).
- The manager's own default when `maxRunningJobs` is missing: `var v = 15;` at 160031518 and
  `return Math.max(1, Math.floor(t ?? v));` in `get #R()` at 160032817; with the SDK always passing a
  function for roots, the built-in 15 is unreachable through `sdk.ts`.

## (2) `async.maxJobs` setting definition and default

Module provenance: `// packages/coding-agent/src/tools/settings.ts` at 155206756.

```
var XPe = h({                 // 155231574
  id: "async.maxJobs",        // 155231590
  protocolDefault: ["rpc"],
  type: "number",
  default: 100                // 155231659
});
```

≤25-word verbatim: `var XPe = h({ id: "async.maxJobs", protocolDefault: ["rpc"], type: "number", default: 100 });`

The clamp reads this exact object: `XPe.get(R)` at 164406802, where `R` is the settings manager of
the session that constructs the manager.

## (3) Running-job count rule and the limit throw

Module provenance: `// packages/coding-agent/src/async/job-manager.ts` at 160031363.

`get atCapacity()` (bytes 160032863–160033060):

```
for (const t of this.#e.values()) {
  if (t.status === "running" && !t.queued)
    e++;
}
return e >= this.#R;
```

≤25-word quote: `if (t.status === "running" && !t.queued) e++;` (folded across two lines; rule starts
at **160032979**, increment `e++;` at 160033028).

`register(type, label, run, options)` repeats the same count before inserting (bytes
160033180–160033400), then throws:

```
for (const u of this.#e.values()) {
  if (u.status === "running" && !u.queued)
    r++;                       // 160033235 (folded); increment at 160033284
}
const o = this.#R;
if (r >= o) {                  // 160033322
  throw new Error(`Background job limit reached (${o}). Wait for running jobs to finish or cancel one.`);
}                               // throw at 160033342; text at 160033359
```

≤25-word quote: `Background job limit reached (${o}). Wait for running jobs to finish or cancel one.`
(13 words).

Semantics observed:
- `this.#e` is a single `Map` of **all** jobs: `#e = new Map;` at 160031852, insertion
  `this.#e.set(a, l);` at 160035368. `#R` is `Math.max(1, Math.floor(fn ?? 15))`.
- No owner filter in the count: `this.#e.values()` is used unfiltered. `ownerId` is only used by
  `#d()` for listing/delivery (`#I(e)` filters `!t.foreground`), not for capacity.
- New jobs start `status: "running"` with `queued: n?.queued === true` (1600334xx). A queued job is
  excluded until the run body calls `markRunning`, which does `l.queued = false;` (160034519).
  The `task` registrations seen pass no `queued` option (e.g. `{ id: D, agentId: D, ownerId: U }` at
  164035733), so a task consumes capacity the moment `task` is called.
- Enforcement point is `register` only. Prechecks that avoid the throw: bash auto-background skips it
  when `Y.atCapacity` (` && Y && !Y.atCapacity` at 161061577), eval falls back inline
  (`ve.atCapacity` at 164233372). The task path has **no** `atCapacity` precheck (only three
  `atCapacity` reads exist in JS: 160032867 class, 161061588 bash, 164233375 eval), so a `task`
  call at capacity reaches `register` and throws the message above.

## (4) How a task child gets a job manager — yes, the parent's

Chain (all in the embedded JS, read at byte offsets):

1. **Child never constructs one.** `sdk.ts`: `const Ui = !u.parentTaskPrefix ? new Xm({...}) : undefined;`
   (164406720). Task children are created with `parentTaskPrefix`, so `Ui === undefined`.
2. **Child falls back to the passed manager.** `sdk.ts`: `const Ao = Ui ?? u.asyncJobManager;` at
   **164407567** (8 words).
3. **Root passes its own manager into its session options.** `sdk.ts`:
   `ownedAsyncJobManager: Ui,` at 164460881 and `asyncJobManager: Ao,` at 164460913.
4. **Session stores it.** Module `// packages/coding-agent/src/session/agent-session.ts` at 164855808,
   class `xL` (164860007):
   `this.#At = u.ownedAsyncJobManager;` and
   `this.#ye = u.asyncJobManager ?? u.ownedAsyncJobManager;` at **164875409**;
   `get asyncJobManager() { return this.#ye; }` at **164905569**.
   For a child `#At` is `undefined` and `#ye` is the parent's object.
5. **Code that passes the manager to children:**
   - `// packages/coding-agent/src/task/structured-subagent.ts` at 164011494:
     `asyncJobManager: P.asyncJobManager,` at **164022276**, where `P` is `const { session: P } = u;`
     (164020176) — the parent session.
   - `// packages/coding-agent/src/task/executor.ts` at 164693935: child session options include
     `parentTaskPrefix: M,` and `asyncJobManager: u.asyncJobManager,` at **164772669**.
   - vibe child spawn: `asyncJobManager: u.asyncJobManager,` at 164288452 and the runner's
     `#f(u) { const h = u.asyncJobManager; … return h; }` at 164267145 (read at 164267157), passed to
     `#V(u, T|M, …)` at 164277258 / 164278765 — all in
     `// packages/coding-agent/src/vibe/runtime.ts` (comment at 164260780).
   - security-scan child spawn: `asyncJobManager: this.session.asyncJobManager` at 164248862 in
     `// packages/coding-agent/src/tools/security-scan.ts` (comment at 164245437).
   - `// packages/coding-agent/src/task/persisted-revive.ts` at 165597469:
     `parentTaskPrefix: p.id, asyncJobManager: u.session.asyncJobManager,` at **165601255**.
   - `// packages/coding-agent/src/task/restore.ts` (comment at 165603184):
     `const T = u.asyncJobManager;` at 165603476, then `T.register("task", H, …)` for revived
     children at 165604203.
   - `/tan` command (`// packages/coding-agent/src/modes/controllers/tan-command-controller.ts` at
     165407442): `const P = p.asyncJobManager;` at 165408294.
6. **Children register on that same object.**
   - bash: `// packages/coding-agent/src/tools/bash.ts` at 161039319 —
     `const t = this.session.asyncJobManager;` at **161052757**, `t.register("bash", s, …)` at 161053248.
   - task: `// packages/coding-agent/src/eval/agent-bridge.ts` at 164030276 —
     `const I = h.session.asyncJobManager;` at **164034401**, `I.register("task", D, …)` at 164034650;
     the spawn then carries the same manager (`structured-subagent.ts`:164022276).
   - eval: `// packages/coding-agent/src/tools/eval.ts` at 164224716 —
     `const ve = I.asyncJobManager;` at **164233304**, `ve.register("eval", Le, …)` at 164233929.

**Answer to the question:** yes. A task child owns no manager, inherits the parent's instance, and
every child bash/task/eval job is inserted into the parent's `#e` map. Because the count in
`register`/`atCapacity` iterates `this.#e.values()` with no owner filter, child-seat jobs consume the
same cap as the parent's. Two consequences observed in code:
- The cap number itself comes from the manager's closure over the **constructing (root) session's**
  settings manager (`XPe.get(R)` at 164406802, `R` captured in `sdk.ts`), so a child's own settings
  cannot change the cap [INFERENCE from the closure site; not exercised].
- A child created without `asyncJobManager` (only possible if a caller omits it while setting
  `parentTaskPrefix`) gets `#ye === undefined`; bash then throws
  `Background job manager unavailable for this session.` (161052830) and tasks fall back to
  sync (`task: no AsyncJobManager registered; falling back to sync execution` at 164171556, gated by
  `const pe = de ? this.session.asyncJobManager : undefined;` at 164170933).

## (5) Which job types register with the manager

Every literal `.register("<kind>", …)` in the bundle was enumerated: 17 calls, of which **12 target
the job manager** (bash 1, task 9, eval 2) and 5 target other registries.

| Kind | Manager sites | Receiver |
|---|---|---|
| `bash` | 161053248 | `this.session.asyncJobManager` (tools/bash.ts) |
| `task` | 164034650, 164179342, 164290262, 164509359, 164745231, 164786591, 164791230, 165410101, 165604203 | session's manager; e.g. agent-bridge.ts:164034401, batch path `manager: pe` (`pe = de ? this.session.asyncJobManager : undefined`, 164170933), security coordinator `const U = this.#e.asyncJobManager;` at 164509294, workpool (`task/workpool.ts`, comment 164784929) `this.session.asyncJobManager` at 164786591/164791230, restore.ts:165603476 |
| `eval` | 163907061 (`eval/judgment-batch-bridge.ts`, ids `jdgb-N`), 164233929 (`tools/eval.ts`) | `this.#o.asyncJobManager` / `I.asyncJobManager` |

Not manager job kinds (5 literal sites): `yield` (161405862) and `task` (164189913) register
extractors on `ZL` — a tool registry, `var ZL = new n;` 160772705 with `getRegisteredTools`;
`mcp-notification` (164470419), `advisor` (164828394) and `async-result` (164890039) register on
`yieldQueue`. No other literal kind string exists.

## Confidence and remaining unknowns

- Items 1–3: **high** — single unambiguous sites, contract regexes match exactly once with value 100,
  quotes verified against the bytes.
- Item 4: **high** for the inheritance chain and the shared count (six independent pass/read sites
  agree). The "cap follows the root session's settings snapshot" consequence is [INFERENCE].
- Item 5: **high** for the JS bundle (all 65 `.register(` call sites inspected; literal kinds fully
  enumerated).
- [UNKNOWN] Whether any native (Rust/`pi-natives`) path inserts jobs into `Xm`'s private map — the map
  is private (`#e`) and no external setter was found; all insertions found are `this.#e.set(` at
  160035368/160035889 within `job-manager.ts`.
- [UNKNOWN] Live running-job count of this session — not derivable from bytes (same frontier the
  contract states).
- Not checked (outside this seat): the config-file parsing half of C2 and the live `--selftest`
  numbers; another seat owns those.

## Bounds

No tool installed or upgraded (nothing recorded under the tooling directive). No `omp` execution, no
lane git/jj writes, no edits outside this report file. The binary was opened read-only via Python
`mmap`; `sha256sum`, `stat` and `ls` were the only other commands touching it.

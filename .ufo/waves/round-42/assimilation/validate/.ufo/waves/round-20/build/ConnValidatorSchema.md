# ConnValidatorSchema — Upstream Swarm Wave Schema & Settlement Validation

**Author:** MoriR20.ConnValidatorSchema (UFO-FSD Connector, leaf seat, no subagent dispatch)  
**Round:** mori-shokunin round 20 (fleet/host observability)  
**Contract reference:** `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/contract.md:49-89`  
**Target inspected:** `/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs` (read-only)  
**Report path:** `.ufo/waves/round-20/build/ConnValidatorSchema.md`  

---

## 1. Upstream Contract Confirmations (`ufo-swarm-wave.mjs`)

All line numbers below cite `/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs` as inspected on 2026-10-21.

### A. Dispatch Schema ID
- **Schema ID:** `"ufo-swarm-wave-dispatch-v1"`
- **Definition:** `scripts/ufo-swarm-wave.mjs:136`
  ```javascript
  const SWARM_DISPATCH_SCHEMA = "ufo-swarm-wave-dispatch-v1";
  ```
- **Emission in Payload:** `scripts/ufo-swarm-wave.mjs:1293` (inside `planToDispatchPayload`)
  ```javascript
  return {
    schema: SWARM_DISPATCH_SCHEMA,
    wave: plan.wave,
  ```
- **CLI & Interface Documentation:** `scripts/ufo-swarm-wave.mjs:51-52`, `scripts/ufo-swarm-wave.mjs:1274-1275`.

---

### B. Origin of `taskCall.tasks`
- **Location in Dispatch Render:** `scripts/ufo-swarm-wave.mjs:1282-1308` (`planToDispatchPayload`)
  ```javascript
  1282:export function planToDispatchPayload(plan) {
  1283:  const spawns = [];
  1284:  const resumes = [];
  1285:  for (const entry of plan.tasks) {
  1286:    // Two independent arms, not else-if: an entry carrying both fields
  1287:    // (never minted by planSwarmWave, but this is an exported boundary)
  1288:    // landed in BOTH lists under the two-filter version — preserved.
  1289:    if (entry.agent !== undefined) spawns.push(entry);
  1290:    if (entry.resume !== undefined) resumes.push(entry);
  1291:  }
  1292:  return {
  ...
  1307:    taskCall:
  1308:      spawns.length > 0 ? { context: plan.context, tasks: spawns } : null,
  1309:    resumeSends: resumes,
  ```
- **Origin in Plan Generation:** `scripts/ufo-swarm-wave.mjs:1079-1164` (`planSwarmWave`)
  - `lanes` is parsed from `spec.items` at lines `857-950`.
  - For each spawn lane (`lane.kind !== "resume"`), line `1163` produces:
    ```javascript
    return { name, agent: lane.role, task: text };
    ```
  - When template-hoisting compaction applies (lines `1149-1162, 1186-1199`), the task text is replaced by the hoisted compact representation at line `1197`:
    ```javascript
    tasks[laneIndex].task = compact;
    ```
  - The plan object returns `tasks` at line `1269`.
  - **Summary:** `taskCall.tasks` originates from `spec.items` via `planSwarmWave`, filtering strictly for spawn entries (`entry.agent !== undefined`), excluding resume lanes (`entry.resume !== undefined`).

---

### C. Exact Rendered Report Trailer Text
- **Renderer Function:** `scripts/ufo-swarm-wave.mjs:208-210` (`reportInstruction`)
  ```javascript
  208:function reportInstruction(reportDir, name) {
  209:  return `Report: write your scoped findings to ${reportDir}/${name}.md`;
  210:}
  ```
  - **Exact String Template:** `Report: write your scoped findings to ${reportDir}/${name}.md`
- **Call Sites in Prompt Composition:**
  - Standard spawn lane: `scripts/ufo-swarm-wave.mjs:1133-1135`
    ```javascript
    if (reportDir !== null) {
      text = appendReportSuffix(text, reportInstruction(reportDir, name));
    }
    ```
  - Hoisted compact spawn lane: `scripts/ufo-swarm-wave.mjs:1155-1157`
    ```javascript
    if (reportDir !== null) {
      compact = appendReportSuffix(compact, reportInstruction(reportDir, name));
    }
    ```
  - Resume lane message: `scripts/ufo-swarm-wave.mjs:1105-1110`
    ```javascript
    if (reportDir !== null) {
      message = appendReportSuffix(message, reportInstruction(reportDir, name));
    }
    ```
- **Envelope Positioning Mechanics:** `scripts/ufo-swarm-wave.mjs:174-181` (`appendReportSuffix`)
  ```javascript
  174:function appendReportSuffix(text, suffix) {
  175:  const trimmed = text.trimEnd();
  176:  if (!trimmed.endsWith(GODSPEED_MARKER)) return `${text}\n\n${suffix}`;
  177:  const body = trimmed.slice(0, trimmed.length - GODSPEED_MARKER.length).trimEnd();
  178:  return body === ""
  179:    ? `${suffix}\n\n${GODSPEED_MARKER}`
  180:    : `${body}\n\n${suffix}\n\n${GODSPEED_MARKER}`;
  181:}
  ```
  - `GODSPEED_MARKER = "| godspeed"` (`:159`).
  - If the prompt body ends with `| godspeed`, the report instruction is placed **before** `\n\n| godspeed` so the marker remains terminal.

---

### D. Registry Schema and Member Fields
- **Registry Schema ID:** `"ufo-swarm-registry-v1"`
  - Defined in `/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-registry.mjs:27`:
    ```javascript
    export const SWARM_REGISTRY_SCHEMA = "ufo-swarm-registry-v1";
    ```
  - Imported into `scripts/ufo-swarm-wave.mjs:110` and used at lines `619` and `1254`.
- **Registry Document Envelope:** Constructed by `buildRegistryDoc` (`scripts/ufo-swarm-wave.mjs:616-630`):
  - `schema`: `"ufo-swarm-registry-v1"` (`:619`)
  - `wave`: `string | null` (`:620`)
  - `createdAt`: ISO 8601 string (`:621`)
  - `updatedAt`: ISO 8601 string (`:622`)
  - `reportDir`: optional string (`:623`)
  - `priorRegistries`: optional array of strings (`:627`)
  - `members`: dictionary mapping member name to member record (`:628`)
- **Member Record Fields:**
  - Validated in `loadRegistry` (`:528-540`), constructed in `planSwarmWave` (`:1099-1127`), and updated by `record` (`:1714-1733`):
  - **Spawn Member (`kind: "spawn"`):**
    - `kind`: `"spawn"` (`:1121`)
    - `agentId`: `string | null` (initialized to `null` at `:1121`; populated post-spawn via `record` at `:1732`; validated against `RESUME_ID_PATTERN` at `:530`)
    - `role`: string taxonomy role (`:1121`; validated against `SWARM_ROLES` at `:914`)
    - `item`: string or `null` (`:1121`; from `spec.items[].item`)
    - `axes`: optional array of strings (`:536-539, 1125`)
    - `milestone`: optional string (`:533-535, 1126`)
  - **Resume Member (`kind: "resume"`):**
    - `kind`: `"resume"` (`:1099`)
    - `agentId`: `null` (`:1099`)
    - `member`: string (`:1099`; original member name resumed)
    - `item`: string or `null` (`:1099`; inherited from predecessor member)
    - `axes`: optional array of strings (`:1100, 536-539`)
    - `milestone`: optional string (`:1101, 533-535`)

---

### E. Resume-Only Wave and `taskCall: null`
- **Confirmation:** **YES.** A wave containing exclusively resume lanes renders `taskCall: null`.
- **Path:line Evidence:**
  - `scripts/ufo-swarm-wave.mjs:1278-1280` (JSDoc specification):
    > `and a resume-only wave emits taskCall: null (zero task calls, all hub sends) instead of an empty tasks array that could be misread as a no-lane call.`
  - `scripts/ufo-swarm-wave.mjs:1307-1308` (payload renderer):
    ```javascript
    taskCall:
      spawns.length > 0 ? { context: plan.context, tasks: spawns } : null,
    ```
    When `spawns.length === 0`, `taskCall` is explicitly `null`.
  - `scripts/ufo-swarm-wave.mjs:1315-1316`:
    ```javascript
    "No spawn lanes: this wave resumes only — one hub send per resumeSends entry: hub send --to <entry.resume> --message <entry.message>; no task call is issued."
    ```
  - **Contract Alignment:** Aligns directly with `mori-shokunin/.ufo/waves/round-20/contract.md:68-69` (`taskCall: null → wave state no-spawn`) and `frozen/c2-expected.json:18` (case `no-spawn` expects `exit: 0, state: "no-spawn", members: 0`).

---

## 2. Analysis of Trailer Variants Missed by the Contract Regex

`contract.md:70-71` specifies:
> `Expected report path: the LAST line of a task matching ^Report: write your scoped findings to (\S+)$`

If an implementation reads literally "the last line of the task text" and applies `re.compile(r"^Report: write your scoped findings to (\S+)$")` (as both `ImplSettlement` and `ImplSettlementAlt` do via `lines[-1]`), the following variants will fail to match, causing members to be incorrectly flagged as `unparsed` and waves to degrade to `unavailable`:

| # | Variant / Scenario | Cause & Mechanism | Impact on `^Report: write your scoped findings to (\S+)$` |
|---|---|---|---|
| **1** | **Terminal Godspeed Envelope Marker (`\| godspeed`)** | `ufo-swarm-wave.mjs:174-181` forces `\| godspeed` to remain terminal (`appendReportSuffix` inserts the report line before `\| godspeed`). | The literal last line of the task is `\| godspeed`. A parser checking `lines[-1]` matches `\| godspeed`, failing the regex and classifying the member `unparsed`. |
| **2** | **Trailing Whitespace on Report Line** | Line ends with trailing space or tab (e.g. `Report: ... to path.md `). | `(\S+)$` anchors end-of-line immediately after non-whitespace. Any trailing space prevents `$` from matching. |
| **3** | **Windows CRLF Line Endings (`\r\n`)** | Task string uses `\r\n`. Splitting on `\n` leaves trailing `\r` on the line (`...to path.md\r`). | `\S+` consumes `\r` as part of the path, producing a corrupted path string (`path.md\r`) or failing regex anchors. |
| **4** | **Paths Containing Whitespace** | Spec uses a directory or member name with spaces (e.g. `.ufo/waves/round 1/build/Task.md`). | `(\S+)` matches only non-whitespace; spaces in paths cause regex match failure. |
| **5** | **Delimited Paths (Quotes, Backticks, Angles)** | Prompt templates formatting path as `"path.md"`, \`path.md\`, or `<path.md>`. | `(\S+)` captures the delimiters, causing filesystem lookup to fail. |
| **6** | **Spacing Variations in the Prefix** | Multiple spaces between words (e.g. `Report:  write your scoped findings to  <path>`). | Regex contains literal single spaces; double spaces cause match failure. |
| **7** | **Case / Punctuation Variations** | `report:` (lowercase), `REPORT:` (uppercase), or space before colon (`Report :`). | Strict case-sensitive and anchor-sensitive regex rejects the line. |
| **8** | **Appended Directives / Footers** | Injected directives after the trailer (observed in `round-15/task-response.json:15` where `# Tooling directive...` was appended at the end of the task). | The report trailer is no longer the final line of the task; a `lines[-1]` check sees the footer line. |
| **9** | **Waves Lacking `reportDir` Declaration** | In `ufo-swarm-wave.mjs:1133,1258`, when `spec.reportDir` is absent or `null`, `reportInstruction` is never appended. | The generated task contains zero `Report:` lines; all members evaluate to `unparsed`. |
| **10** | **Resume-Only Lanes (`resumeSends`)** | Resume lanes carry `Report:` in `resumeSends[*].message`, not in `taskCall.tasks[*]`. | C2 scans `taskCall.tasks[*]`; resume members are completely invisible to task trailer scanning. |

---

## 3. UFO-FSD Connector Synthesis: One Bounded Non-Obvious Move

### A. Evidence
1. **The Godspeed Envelope Trap:** In `scripts/ufo-swarm-wave.mjs:174-181`, `appendReportSuffix` explicitly splices the report instruction *ahead* of the terminal `| godspeed` envelope marker whenever `GODSPEED_MARKER` is present.
2. **Current Implementation Vulnerability:** In `mori-shokunin/.ufo/waves/round-20/build/ImplSettlement/tools/mori-wave-settlement.py:176` and `build/ImplSettlementAlt/tools/mori-wave-settlement.py:85`, both independent candidate implementations evaluate strictly:
   ```python
   match = REPORT_RE.fullmatch(lines[-1])
   ```
   If any swarm wave is dispatched with terminal Godspeed envelopes, 100% of its seats will be classified as `unparsed`, causing the wave state to evaluate as `unavailable`.
3. **Contract Intent:** `contract.md:70-71` states: "the LAST line of a task matching `^Report: write your scoped findings to (\S+)$`". Grammatically and operationally, this specifies *the last line among those matching the pattern*, not *the last line of the entire text tested in isolation*.

### B. Affected Axes
- **Coverage (C2):** Preserves 100% capability acquisition across both envelope-wrapped and raw task payloads.
- **Operability:** Prevents spurious wave failures (`unavailable`) caused by terminal envelope markers (`| godspeed`) or trailing whitespace.
- **Freshness & Calibration:** Eliminates synthetic drift between dispatch tooling conventions and observability parsing.

### C. Proposed Move
**Implement Bottom-Up Tail Scanning in `tools/mori-wave-settlement.py`:**
Instead of inspecting only `lines[-1]`, iterate through the task's lines in reverse order (bottom-up), stripping whitespace, and bind the first line that matches `^Report:\s+write your scoped findings to\s+(\S+)\s*$`.
- This satisfies "the LAST line of a task matching REGEX".
- It transparently supports terminal envelope markers (`| godspeed`), trailing empty lines, and carriage returns (`\r`).
- It retains strict fail-closed rejection for tasks genuinely lacking a report trailer (satisfying `c2-expected.json` case `no-trailer`).

### D. Risks and Second-Order Effects
- *Risk: False positive matching on embedded report citations:* If an agent task mentions a report path in its prompt body earlier, bottom-up scanning could pick an earlier line.
  *Mitigation:* Scanning from the tail stops at the *very last* matching line. In `ufo-swarm-wave.mjs`, the genuine trailer is placed either at the very end or immediately before `| godspeed` (never earlier).
- *Risk: Divergence from Oracle:* Oracle harness `OracleHarness/c2-oracle.py` generates tasks with the trailer at the end (`line:336`). Bottom-up scanning matches `lines[-1]` when no marker exists, ensuring 14/14 oracle compatibility.

### E. Verification (for L1 Integration)
1. Verify that `tools/mori-wave-settlement.py` passes all 14 cases of `frozen/c2-expected.json`.
2. Add a unit test verifying that a task ending with:
   ```text
   Report: write your scoped findings to .ufo/waves/round-20/build/Seat.md

   | godspeed
   ```
   resolves to status `present` (when the file exists) rather than `unparsed`.

---

## 4. Tooling & Pacman Guard Disclosure

- No packages installed or updated.
- No pacman commands executed (host pacman guard strictly respected).
- No mutating commands executed (jj/git untouched; read-only inspections only).
- All source inspections grounded by exact file and line references.

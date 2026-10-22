# ScoutLiveRunway — independent live replication of C2's host reading

**Verdict: broken — in the comparison target, not in the numbers.** I reproduced C2's host reading
without using `tools/mori-job-runway.py` and every number holds: configured **200**, clamp **100 at one
site**, setting default **100 at one site**, effective **100**, verdict `RUNWAY_CLAMPED`, exit 1.
But the "committed live run" that the contract and a committed wave-1 report cite as evidence does not
exist at HEAD `07a31ae8e22514bbc603afa13f2de7c8b2424cca`, in any git ref, or on disk. C2's
`runway-selftest.txt` evidence is also absent and, contrary to `ReviewFrozenCases.md:138`, is due now.

Measured at lane HEAD `07a31ae8e22514bbc603afa13f2de7c8b2424cca`, 2026-10-22, read-only. No omp was run;
no job was launched; the lane was not mutated. My only write is this file.

## 1. Independent measurement (my own byte reads, not the tool)

### configured — the operator's OMP settings file

File: 7,098 bytes, sha256 `887fbbb305e815cd02c2be3e39cc73cd56971eb9199055fb452e7eda1ff1484e`, mtime
2026-10-22 05:01, no UTF-8 BOM, no tab byte anywhere in the file.

Top-level keys read in order: `setupVersion` (1), `extendedContext` (2), `enabledModels` (3),
`modelRoles` (103), `task` (130), `retry` (153), `dev` (240), `tools` (242), `async` (244), `tier` (246),
`textVerbosity` (249), `hideThinkingBlock` (250), `omitThinking` (251).

The block, verbatim (the settings file):

```
async:
  maxJobs: 200
```

Structural checks under contract rule 1 and amendment A2: exactly one column-0 `async` key (line 244,
written exactly `async:`); no top-level `<<:` merge key or `? ` complex key; no `---` / `...` document
marker; no tab in the block indentation; the direct child is written exactly `maxJobs:` with two spaces
of indent; value is the unquoted decimal integer `200` with no `#`. Therefore
`configured = {state: "set", value: 200}`. No other top-level block contains a `maxJobs` child that
could count.

### clamp and setting default — installed binary

`command -v omp` → `/home/vgpnk/.local/bin/omp`; `realpath` identical. Size 256,702,432 bytes; sha256
`85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4` (matches the tool's
`binary_sha256`, and S102 in `harness-job-capacity-r25.md:1`). Read with `mmap` + `re`:

* clamp pattern `maxRunningJobs:\s*\(\)\s*=>\s*Math\.min\(\s*(\d+)\s*,\s*[\w$]+\.get\([\w$]+\)\s*\)`
  — **1 match, value 100**, byte 164406766:
  `maxRunningJobs: () => Math.min(100, XPe.get(R))`.
* setting pattern `id:\s*"async\.maxJobs",[^}]{0,300}?default:\s*(\d+)` — **1 match, value 100**, byte
  155231590: `var XPe = h({ id: "async.maxJobs", protocolDefault: ["rpc"], type: "number", default: 100 })`.
  The matched `XPe` is the same identifier the clamp reads, so the clamp and the schema default are
  talking about the same setting.
* Loose counts over the whole binary: `maxRunningJobs` 3, `async.maxJobs` 2. The other two
  `maxRunningJobs` hits are not clamps: one is the settings/UI key list around byte 94,971,828, one is
  the job-manager field assignment `this.#P = e.maxRunningJobs` around byte 160,032,417. The other
  `async.maxJobs` hit is the UI label/description blob around byte 96,085,908. So there is exactly one
  clamp site, `sites = 1`, no ambiguous second number.
* Clamp construction context (byte 164,406,766): `const Ui = !u.parentTaskPrefix ? new Xm({ maxRunningJobs:
  () => Math.min(100, XPe.get(R)) }) : undefined;` — the clamp exists only on a root session
  (`!parentTaskPrefix`), which matches A2's "per root omp session" wording.
* Manager getter (byte 160,032,824): `get #R() { const e = this.#P; const t = typeof e === "function" ?
  e() : e; return Math.max(1, Math.floor(t ?? v)); }` with `var v = 15;` at byte 160,031,518. So the
  manager applies `max(1, floor(...))`; with this host's base the arithmetic is
  `max(1, floor(min(100, 200))) = 100`.
* Version bytes `18.12.6` occur 9 times. That is corroboration only, not proof the artifact is that
  release; the sha256 match to S102 is the stronger identifier.

**Effective = 100. Verdict `RUNWAY_CLAMPED`. Exit 1.** The configured 200 is read and then clamped before
the manager sees it; a refusal text would carry 100, not 200.

## 2. Comparison with the tool's live output — identical

`python3 -I -B tools/mori-job-runway.py` run from the lane, stdout:

```json
{
  "schema": "mori-job-runway-v1",
  "config_path": "the operator's OMP settings file",
  "binary_path": "/home/vgpnk/.local/bin/omp",
  "binary_sha256": "85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4",
  "configured": { "state": "set", "value": 200 },
  "clamp": { "state": "found", "value": 100, "sites": 1 },
  "setting_default": { "state": "found", "value": 100, "sites": 1 },
  "effective": 100,
  "verdict": "RUNWAY_CLAMPED"
}
```

Exit 1. Every field equals my independent reading, including `binary_sha256`. This is the only live
artifact on the host that can be compared to; see §3 for the absent committed one.

## 3. Findings against the wave-1 product

### F1 — the "committed live run" does not exist. Severity: medium (false provenance in a committed report)

`SkillErrorPattern.md:47` (committed at `9ec786e`; verified with `git show HEAD:… | sed -n '47p'`) says:
"The lane's own committed live run agrees: `.ufo/waves/round-25/evidence/runway-live-run.json` →".
`:206` (F11) and `:310` repeat the path as "committed live-run evidence" and add
`runway-live-run.meta`. Contract `contract.md:90-91` states "A live run against this host is committed as
evidence".

Observed: `git ls-tree --name-only HEAD .ufo/waves/round-25/evidence/` lists seven files —
`pressure-selftest.txt`, `routed-r24-after-a5.txt`, `routed-r24-after.txt`, `routed-r24-before-a5.txt`,
`routed-r24-before.txt`, `wave1-bind.json`, `wave2-bind.json` — no runway file. `git log --all
--diff-filter=A -- '*runway-live*' '*runway-selftest*'` is empty: the files were never added in any ref.
`git status --porcelain -- .ufo/waves/round-25/evidence/` is clean, so they are not in the working tree
either. The only on-disk trace is the other wave-1 report, `ReviewFrozenCases.md:139`, which correctly
recorded them as working-tree-only and not in HEAD; `ReviewPycacheRule.md:128` also calls them untracked.
`SkillErrorPattern.md` contradicts its sibling and is wrong as committed.

Smallest fix: either produce the artifact the text promises — write
`.ufo/waves/round-25/evidence/runway-live-run.json` with `revision: <landed tip>`, `command: python3 -I
-B tools/mori-job-runway.py`, `exit: 1` headers and the JSON body above, and commit it — or change the
word "committed" in `contract.md:90-91`, `SkillErrorPattern.md:47`, `:206`, `:310` to "re-run live by any
seat with `python3 -I -B tools/mori-job-runway.py`". One of the two, not both halves left disagreeing.
Note the contract already says the live run is "not the after-value", so this is provenance, not a gate.

### F2 — C2's mandated `runway-selftest.txt` evidence is absent and is now due. Severity: medium (evidence gap on the after-value)

`contract.md:127-130` (A1) requires `.ufo/waves/round-25/evidence/runway-selftest.txt` with
`revision:`/`command:`/`exit:` headers and full stdout, "written after the last change to the measured
tool". It does not exist in HEAD's tree, the index or the working tree.

`ReviewFrozenCases.md:138` (committed at `9ec786e`) excuses it: "That change is still pending (F2), so it
is not yet due." That is stale as committed. The tool's last change is `fbecc59` (2026-10-22 07:19:08,
"runway selftest fails on zero cases…"), and `git merge-base --is-ancestor fbecc59 9ec786e` succeeds —
it landed 54 minutes before the report commit and is an ancestor of HEAD. The preceding tool change,
`9a3d511` (A2 abstentions), also precedes the report commit. So at HEAD the last change to the measured
tool has already happened, the file is due, and no further change is scheduled that would defer it.

Smallest fix: at the landed tip run `python3 -I -B tools/mori-job-runway.py --selftest` and commit its
stdout with `revision:`, `command:`, `exit:` headers as `.ufo/waves/round-25/evidence/runway-selftest.txt`.
The frozen cases blob behind the declared after-value checks out: `git rev-parse
7634be75:tools/fixtures/mori-job-runway/cases.json` = `48df844a22d74a57204f55a62e54760c7038c60f`
(matches `contract.md:130`), first tool commit `09f55b6` (07:02:38) is later than the freeze commit
`7634be7` (06:49:49). I did **not** run the selftest — it is the coverage seat's after-value, not mine,
and an unrun check is not a pass here.

## 4. Project-level `.omp/config.yml` — none exists on this host

* `/home/vgpnk/Projects/shokunin/.omp/` exists but contains only `agents/executor.md`; no `config.yml`,
  no `config.yaml` (`find … -maxdepth 2 -type f` listed exactly that one file).
* `find /home/vgpnk/Projects/shokunin -maxdepth 4 \( -path '*/.omp/config.yml' -o -path
  '*/.omp/config.yaml' \)` → empty.
* Lane `/home/vgpnk/Projects/shokunin/mori-shokunin/.omp` → absent (`test -e` false).
* Global fallback `~/.omp/agent/config.yaml` → absent. `PI_CONFIG_FILES` is unset in this environment.

So the only config file that could feed the measured value is the global one the tool reads, and no
project layer exists here to override it. This matches `harness-job-capacity-r25.md:187` ("the fleet
root's `.omp/` holds only …"). Caveat: the binary's runtime settings stack also has project layers,
`--config` overlays and runtime overrides (F13, that entry's Limits); their absence is why this host's
number is uncontested, not something the tool proves.

## 5. What is observed, inferred, and still unknown

* **Observed:** the config bytes and block shape; the binary's single clamp match, single setting-default
  match, manager floor getter, and root-session guard; the tool's live JSON and exit code; the absence of
  `runway-live-*` and `runway-selftest.txt` from every ref and the worktree; the absence of any
  project-level `.omp/config.yml`.
* **[INFERENCE]** The setting descriptor's `compute()` returns `this.default` when a value is undefined
  (`return t === undefined ? this.default : t`, byte region 153,980,829), which is why an unset
  `async.maxJobs` would behave as 100. This supports the tool's `RUNWAY_DEFAULT` path but is not needed
  for this host's answer, where the value is set.
* **Unknown / not tested here:** (a) the live 100-job refusal event itself — I launched no jobs (leaf
  bound), so I corroborate the cap arithmetic, not an occurrence; (b) whether the running session's
  loader applied any runtime override — not readable from outside the session, and no project/env layer
  exists; (c) the selftest result at the landed tip (coverage seat's item).

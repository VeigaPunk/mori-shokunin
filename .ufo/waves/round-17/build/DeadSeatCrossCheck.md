# DeadSeatCrossCheck — round 17 cross-check of the orchestrator's zai 429 death tally

Seat: `MoriR17.DeadSeatCrossCheck-5` (scout, leaf member, no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (branch `master`, entering tip `24526ea`).
Question: does the orchestrator statement **"tabi r17 lost 17, tsukuroi r17 43, souji r17 28+"**
(zai 429 retry-budget deaths) agree with the terminal records of transcripts whose prefix starts
with `TabiR17`, `TsukuroiR17`, `SoujiR17` in the 12-57-31 session dir, classified with the C1
classes of `.ufo/waves/round-17/contract.md:33-50`?

Evidence dir (absolute):
`/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07`

**Verdict: partial.** TabiR17 **disagrees** (claimed 17, observed **18**). TsukuroiR17
**disagrees** (claimed 43, observed **44**). SoujiR17 **agrees** (claimed "28+", observed
**28**). The orchestrator statement undercounts the two lanes by exactly one seat each under
the only metric its wording names (zai provider, `errorStatus == 429`, `errorMessage` starting
`Retry budget exhausted`); no other tested class/definition matches either claimed figure.
Confidence: **high** for the observed counts (deterministic parse of the contract-listed fields;
two independent scan implementations agree); **medium** for the "why the statement is one low"
mechanism — see `## Reconciliation` and `## Remaining unknowns`.

## Exact snippet (read-only; counts only; prints no transcript field values)

Run exactly as shown; stdout is the three `lane …` lines below, rc 0 (this snippet is not
`tools/mori-seat-terminal.py`, so contract exit codes do not apply to it; rc 0 is Python success).

```bash
python3 -c '
import json,glob,os,sys,collections,datetime
D=sys.argv[1]
LANES=["TabiR17","TsukuroiR17","SoujiR17"]
CLS=["completed","aborted","dead_rate_limit","dead_quota","dead_error_other","incomplete","unavailable"]
def term(p):
    n=os.path.getsize(p)
    f=open(p,"rb")
    if n>262144:
        f.seek(n-262144); cut=True
    else:
        cut=False
    b=f.read(); f.close()
    ls=b.split(b"\n")
    if cut: ls=ls[1:]
    t=None
    for x in ls:
        if not x.strip(): continue
        try: r=json.loads(x)
        except Exception: continue
        if r.get("type")=="message" and isinstance(r.get("message"),dict): t=r["message"]
    return t
def cls(m):
    if m is None: return "unavailable"
    em=m.get("errorMessage") if isinstance(m.get("errorMessage"),str) else ""
    es=m.get("errorStatus")
    try: es=int(es) if es is not None else None
    except Exception: es=None
    role=m.get("role"); sr=m.get("stopReason")
    if role=="assistant":
        if sr=="stop": return "completed"
        if sr=="aborted": return "aborted"
        if sr=="error":
            if es==429 or any(k in em for k in ("429","rate_limit","Rate limit","RATE_LIMITED","resource_exhausted")): return "dead_rate_limit"
            if any(k in em for k in ("quota","usage limit","402","credits")): return "dead_quota"
            return "dead_error_other"
    return "incomplete"
tot=collections.defaultdict(collections.Counter); extra=collections.defaultdict(collections.Counter)
for p in glob.glob(D+"/**/*.jsonl", recursive=True):
    name=os.path.basename(p)[:-6]
    pre=name.split(".")[0]
    lane=next((L for L in LANES if pre.startswith(L)), None)
    if lane is None: continue
    m=term(p)
    c=cls(m)
    tot[lane]["files"]+=1; tot[lane][c]+=1
    if c=="dead_rate_limit":
        em=m.get("errorMessage") if isinstance(m.get("errorMessage"),str) else ""
        key=("zai" if m.get("provider")=="zai" else str(m.get("provider"))) + ("/retr" if em.startswith("Retry budget exhausted") else "/429noretr")
        extra[lane][key]+=1
print("scan_utc",datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"))
for lane in LANES:
    c=tot[lane]
    print(lane,"files",c["files"]," ".join(k+"="+str(c[k]) for k in CLS),"zai_retry_budget="+str(extra[lane]["zai/retr"]),"zai_429_noretr="+str(extra[lane]["zai/429noretr"]),"other_429="+str(sum(v for k,v in extra[lane].items() if not k.startswith("zai"))))
' /home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07; echo "rc=$?"
```

Observed stdout (canonical run, `scan_utc 2026-10-20T18:59:29Z`, rc 0):

```
scan_utc 2026-10-20T18:59:29Z
TabiR17 files 165 completed=138 aborted=4 dead_rate_limit=22 dead_quota=0 dead_error_other=0 incomplete=1 unavailable=0 zai_retry_budget=18 zai_429_noretr=3 other_429=1
TsukuroiR17 files 154 completed=108 aborted=2 dead_rate_limit=44 dead_quota=0 dead_error_other=0 incomplete=0 unavailable=0 zai_retry_budget=44 zai_429_noretr=0 other_429=0
SoujiR17 files 150 completed=121 aborted=0 dead_rate_limit=28 dead_quota=0 dead_error_other=0 incomplete=1 unavailable=0 zai_retry_budget=28 zai_429_noretr=0 other_429=0
```

An earlier equivalent run (`scan_utc 2026-10-20T18:58:43Z`) produced identical lines. A still
earlier pass (before 18:58:43Z, no timestamp printed) produced `SoujiR17 … dead_rate_limit=29 …
incomplete=0 zai_retry_budget=28`; the one-seat difference is a live resume of the Souji
lane-root transcript, documented under `## Live-drift observation`. The `zai_retry_budget`
figure did not move across any of the three passes.

## Per-lane verdict

| lane label | prefixes matched (startswith) | files | claimed | observed `zai_retry_budget` | delta | verdict |
|---|---|---|---|---|---|---|
| TabiR17 | `TabiR17` only | 165 | 17 | **18** | +1 observed vs claim | **DISAGREE** |
| TsukuroiR17 | `TsukuroiR17` only | 154 | 43 | **44** | +1 observed vs claim | **DISAGREE** |
| SoujiR17 | `SoujiR17-3` only | 150 | 28+ | **28** | 0 | **AGREE** (exactly 28; satisfies "28+") |

`zai_retry_budget` = class `dead_rate_limit` (contract.md:42-44) with `provider == "zai"` and
`errorMessage` starting `Retry budget exhausted` — the wording "zai 429 retry-budget deaths".
All 90 such records also carry `errorStatus == 429`; the `(type=1302)` token and
`after 10 retries` are present in all 90.

Alternative definitions at the same scan (none matches 17/43):

| definition | TabiR17 | TsukuroiR17 | SoujiR17 | comment |
|---|---|---|---|---|
| `zai_retry_budget` (claim wording) | 18 | 44 | 28 | the metric above |
| any zai 429 (`retry` or not) | 21 | 44 | 28 | +3 Tabi rows are `(type=1302)` zai 429 with no `Retry budget exhausted` prefix and `retries` null |
| all `dead_rate_limit`, any provider | 22 | 44 | 28 | +1 Tabi is an anthropic `claude-opus-5-5` 429; at the canonical scan Souji has no anthropic dead (its lane-root 429 had resumed — see below); at the first pass Souji read 29 |
| `dead_rate_limit` + `aborted` | 26 | 46 | 28 | aborted seats are not 429 deaths |

The three non-retry-budget zai 429 Tabi seats (seat ids are naming data, not content):
`TabiR17.RevBindSelftestCases`, `TabiR17.RevLocalVsPushed`, `TabiR17.RevNoteVsSources`.

## Method conformance (contract.md:33-50)

- Walked `DIR` recursively for `*.jsonl`; seat id = basename minus `.jsonl`; prefix = text
  before the first `.` (`contract.md:33-34`). The match is `prefix.startswith(label)`, so
  `SoujiR17-3` is included under `SoujiR17`. `ClosureTabiR17` / `ClosureTsukuroiR17` do **not**
  start with the labels and are excluded.
- Prefix inventories match nothing else: 165 `TabiR17`, 154 `TsukuroiR17`, 150 `SoujiR17-3`;
  no other prefix starts with the three labels. 469 files total.
- Per file, read at most the last 262144 bytes; when the read did not start at byte 0 the first
  (partial) line is dropped (`contract.md:35-38`). Exactly one record shape was considered:
  `type == "message"` with a dict `message`; terminal = the last such record; `custom`
  (`credential_pin`, usage markers) and all other record types were skipped unread
  (`contract.md:38-39`). Class order and tests follow `contract.md:40-50` verbatim, including
  rate-limit before quota.
- Fields read: `type`, `message.role`, `message.stopReason`, `message.errorStatus`,
  `message.provider`, `message.model`, `message.errorMessage` only as substring/prefix tests
  and as the source of the `(type=NNNN)` and `after N retries` integers. No content, tool text,
  usage, timestamps, ids or `errorMessage` text was read, printed or stored. No symlinks exist
  in the tree (0); no hidden or unreadable `*.jsonl` (0/0).

Structural note (useful for the C1 tool, not a verdict input): in all 468 lane files whose last
record type is `custom` (469th: `model_usage`), the terminal `message` record is **one record
before the last line** (90/90 dead files have exactly one record after the terminal message, a
`custom` record). A scanner keyed on the last line instead of the last `message` record sees no
message at all; this is not what the claim's numbers look like, but it is the sharpest
divergence risk in any reimplementation.

## Reconciliation — why 17/43/28+ cannot be a single consistent snapshot

Death times below are file mtimes (local TZ UTC-03:00; mtime is the transcript's last write,
[INFERENCE] that it approximates the death event). 90 zai retry-budget deaths:

| lane | count | first mtime | last mtime |
|---|---|---|---|
| TabiR17 | 18 | 14:29:03 | 14:58:40 (`TabiR17.RevLabelOnly`, the 18th) |
| TsukuroiR17 | 44 | 14:36:45 | 15:10:08 (`TsukuroiR17.FxFrozenMarker`, the 44th) |
| SoujiR17 | 28 | 14:50:56 | 15:20:34 (the 28th) |

Cumulative states across the event stream show the claim's triple `(17, 43, 28)` never occurs:
at 14:56:08 the state was (17, 43, 18); at 14:58:40 Tabi became 18; at 15:10:08 Tsukuroi became
44; only at 15:20:34 did Souji reach 28. Every state with Souji ≥ 28 already has Tabi ≥ 18 and
Tsukuroi ≥ 44. So the statement is not a snapshot of one instant under this metric; it is
consistent with Tabi/Tsukuroi tallies captured before 14:58:40 / 15:10:08 respectively and a
Souji tally captured at/after 15:20:34, or with a tool/roster difference in the two lanes.
[INFERENCE] — I cannot see what the orchestrator actually measured.

Mechanisms tested and ruled out as explanations for the -1 in each of Tabi and Tsukuroi:

1. Duplicate content: sha256 of the 90 dead files — 90 distinct, no duplicate digests.
2. Duplicate seat ids: none (165/154/150 files = 165/154/150 distinct seat ids).
3. Suffix-stem collapse (strip `-\d+$`): Tabi 18 distinct stems, Tsukuroi 44 — no reduction.
4. "Recovered" dead seats (a completed same-stem sibling, e.g. `X` completed after `X-2`
   died): 0 in all three lanes.
5. Lane-root exclusion: `TabiR17.jsonl` and `TsukuroiR17.jsonl` end `completed`, so excluding
   lane-root files leaves zai counts unchanged; `SoujiR17-3.jsonl` is anthropic and is already
   outside the zai metric.
6. Tail-window/truncation effects: 80 of 90 dead files are ≤262144 bytes (whole file read);
   the other 10 are >262144 and the terminal error is in the retained tail. All 90 files end
   with a newline; no partial last line.
7. Prefix breadth: including every prefix starting with the labels adds no files beyond the
   three inventories above (closure prefixes do not start with the labels).
8. Classification alternatives: table in `## Per-lane verdict` — none yields 17/43.

Unverified and outside the permitted field list (so deliberately not tested): deduplication by
server-side incident/response identifiers, and any roster filter the orchestrator may have
applied (e.g. only seats it dispatched). Either could mechanically produce -1 per lane.

## Live-drift observation

The session dir is live during this round. `SoujiR17-3.jsonl` (the lane-root transcript)
classified `dead_rate_limit` (anthropic `claude-opus-5-5`, 429, no retry-budget token) in the
first pass; by the 18:58:43Z scan its terminal `message` was `incomplete` (assistant `toolUse`
with a `toolResult` record after it), i.e. the transcript had been resumed and appended to
between reads. This is exactly the contract's stated limit (`contract.md:66-67`): a terminal
error is the *last observed* state, not proof the session will never resume, and dead counts
are seats, not distinct incidents. The tree-wide `*.jsonl` count also moved 2508 → 2509
between scans (a new transcript landed). All counts in this report are point-in-time at their
`scan_utc`.

## Commands run (read-only; no writes outside this report)

| command | rc |
|---|---|
| `read .ufo/waves/round-17/contract.md` (full) | n/a |
| `ls` / `find` over `~/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07` (structure, symlink, hidden-file, permission counts only) | 0 |
| `grep -n` over `.ufo/waves/round-17/contract.md` (line citations) | 0 |
| head/grep over `.ufo/waves/round-17/{wave1-context.txt,wave1-dispatch*.json,wave1-record.json}` and `build/{swarm-registry.json,KnowledgeSeatTerminal.md,SrcZaiErrorCodes.md}` (checked whether a sibling report carries the 17/43/28 figures — none does) | 0 |
| the snippet above, run twice (18:58:43Z and canonical 18:59:29Z) | 0, 0 |
| bounded python key-shape / field-combination / digest / mtime probes (counts only; no field values printed) | 0 each |

No tool install or upgrade was needed or performed (nothing from pacman/uv/npm/cargo). No VCS
mutation, no `/tmp` write, no background job, no journal query, no message to any peer. Only
this report file was written.

## Remaining unknowns

1. The orchestrator's exact measurement time, scan directory and filters are not in evidence
   here; the terminal records alone cannot reproduce 17/43 as a valid tally at any instant.
2. Whether a roster/incident-identifier dedupe (fields not readable under this seat's limits)
   accounts for exactly one dropped seat in each of Tabi and Tsukuroi.
3. Counts are last-observed and live: any resume after `2026-10-20T18:59:29Z` changes them.

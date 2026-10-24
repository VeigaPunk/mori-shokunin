# Wave 2 — CriticSingleOmpProcess (mori round 27, attempt 1)

Attacks: Fact 4's inference that the fleet's in-session seats run inside one `omp` process, so one earlyoom send
to an `omp`-class process ends every in-session seat of every lane. The same reading appears in the decision table,
the Limits list, the SKILL.md Round27 table and the round lesson. All entry, SKILL and lesson line numbers below are at the
landed tip `5f00fd045c137b7e3835506d69946cfd9d010eb5` (`git show 5f00fd04:<path>`).

## Verdict

**Partly holds, partly wrong (high).** The mechanism holds and no longer needs to be inference: oh-my-pi v18.12.6 runs
every `task` subagent in-process, on the session's main thread. Two parts are wrong:

1. "The single `omp` process" and "no other `omp` process was visible" describe one sample, not the host. A read at
   17:12Z found three `omp`-class processes: the session process, a second interactive session and the text-prediction
   daemon worker.
2. "One earlyoom send to an `omp`-class process ends every in-session seat" holds only when the session process is
   the one signalled. The journal's 15-byte name cannot show that. A send to the other two `omp` processes ends no fleet
   seat.

## Counterexample

A send line that names `omp` can belong to the text-prediction daemon worker. Its `oom_score` (800, adjustment 200)
equals the python band, the 800 that Fact 4 reports for all 27 python processes. It can also belong to a second
interactive `omp` session (802, adjustment 200), which runs in its own terminal scope. Neither process hosts this
session's `task` seats, so neither kill ends a seat of any lane run from this session. The entry, the lesson and
SKILL.md all treat such a send as a fleet-wide event.

## Evidence

### Process count now (names only)

Scratch scripts `/fast/scratch/hyaku/mori-r27/CriticSingleOmpProcess/sample.py` read `/proc/*/stat` and print counts only.
They print no pids or command lines.

- First read (about 17:09Z): exact name `omp` count = 3. A second read moments later found 4. The fourth `omp` had
  a `python3` parent under `systemd`, outside any terminal scope, and was gone by the next read. [INFERENCE: transient]
- `python3 -I -B sample.py count 7 10` (7 reads, 10 s apart), output:
  `17:10:41Z omp=3 omp_without_omp_ancestor=2 omp-daemon-named=3` (identical at every read through 17:11:41Z).
- `python3 -I -B sample.py count 4 5`, output:
  `17:12:38Z omp=3 omp_without_omp_ancestor=2 omp-daemon-named=3` (identical at 17:12:43Z, 17:12:48Z and 17:12:53Z).
  Over 17:10:41Z to 17:12:53Z, all 11 reads show three `omp` processes, two of them with no `omp` ancestor.
- The committed evidence shows one: `evidence/oom-score-classes.txt` at 15:56:35Z (`class=omp count=1 ...`).
- There are also three processes named `omp daemon brok` (15-byte truncation). The entry's classifier treats only the
  exact names `bun`, `node`, `omp` and `earlyoom` as fleet runtimes and puts every other name in `other`
  (`.ufo/waves/round-27/evidence/oom-score-classes.py:19-21`). So these `omp` helpers count as `other` in Fact 4's
  table.

### Process tree shape (depth, class, scores; `python3 -I -B sample.py shape`, about 17:11Z)

| `omp` process, ranked by `oom_score` | score / adjustment | resident set | threads | parent class | depth below PID 1 | descendants by class |
|---|---|---|---|---|---|---|
| rank 0: the session process (this seat's shell descends from it: `is_this_seat's_session=True`) | 848 / 200 | 2501 MiB | 168 | bash, under a terminal app scope | 6 | python 12, `omp daemon brok` 2, `omp` 1, bash 1, other 10 |
| rank 1: second interactive session, in a separate terminal app scope | 802 / 200 | 222 MiB | 121 | bash, under a terminal app scope | 6 | python 1, `omp daemon brok` 1 |
| rank 2: child of an `omp daemon brok` under rank 0 | 800 / 200 | 65 MiB | 37 | `omp daemon brok` | 8 | none |

- Ancestors of ranks 0 and 1, nearest first: `bash`, `alacritty`, `Hyprland`, `start-hyprland`, `systemd`, `systemd`.
  The two processes are siblings under different terminals, not parent and child.
- Rank 2 has a thread named `pi-predict-ngra`. This matches oh-my-pi's "machine-global text-prediction daemon"
  (`predict/daemon.ts:1-3`, quoted below). [INFERENCE: identified from the thread name; no command line was read]
- Thread names in rank 0 include `tokio-rt-worker` (77), `omp` (33), `HeapHelper` (7) and `Bun Pool N`. There is
  no thread or process per seat. This is consistent with the source's main-thread subagents.

### Task-tool subagents: in-process, not child processes (oh-my-pi v18.12.6)

- The installed binary is v18.12.6: `strings -n 6 ~/.local/bin/omp | rg -o '\b18\.1[0-9]\.[0-9]+\b'` printed
  `18.12.6` 9 times (`18.12.2` to `18.12.5` once each).
- The tag `v18.12.6` resolves to commit `45c35e40c46166dc726ccc52f5d27f40f2449f99`
  (`https://api.github.com/repos/can1357/oh-my-pi/git/refs/tags/v18.12.6`, HTTP 200, accessed 2026-10-22T17:09Z).
- Raw files under `https://raw.githubusercontent.com/can1357/oh-my-pi/v18.12.6/packages/coding-agent/src/`
  (lines pinned with `grep -n`/`sed -n` on the downloaded bytes):

| File | Accessed (UTC) | sha256 | Line: verbatim quote |
|---|---|---|---|
| `task/executor.ts` | 2026-10-22T17:09:54Z | `756a1f0762aa2ffde344f52ae4d127e4c2b6b54aa8e9f1406a0d112311340256` | 2: "In-process execution for subagents." 4: "Runs each subagent on the main thread and forwards AgentEvents for progress tracking." 4135: "Run a single agent in-process." 4717: `sessionPromise = createAgentSession(` |
| `task/isolation-runner.ts` | 2026-10-22T17:10:05Z | `1e613ff94e9df87bc4d7b94e8154b48a01ccfdbfe74ee799720279d1f5a9f0e6` | 34: `import { runSubprocess } from "./executor";` (isolated worktree spawns use the same in-process runner) |
| `task/workpool.ts` | 2026-10-22T17:10:05Z | `8cc4b17def435db43d49294dbc67946585c009832d3faf0b21aebaed59be6dc6` | 294-302: `#spawn` reserves an id and pushes an agent record; no process is started |
| `predict/daemon.ts` | 2026-10-22T17:12:18Z | `f03630e43cd38114670ae34acceeff4948cea4e85180ce5ad4521f0fece6865a` | 2-3: "Server half of the machine-global text-prediction daemon (worker selector `__omp_worker_text_predict`, started through the `text-predict` global broker)." |
| `subprocess/parent-watchdog-worker.ts` | 2026-10-22T17:12:11Z | `0ab71f875994b08c41e6e6f79caf4aca6a11f7376223e5db4309cece3e31ea23` | 2-4: "receives the parent pid, polls its liveness, and SIGKILLs the whole process the moment it is gone." (model workers only, not seats) |

- `rg -n -i "Bun\.spawn|child_process|new Worker\(|spawn\("` over `task/executor.ts`, `task/index.ts`,
  `task/spawn-run.ts`, `task/subprocess-tool-registry.ts`, `task/isolation-runner.ts`, `task/workpool.ts` and
  `task/parallel.ts` found no process or Worker creation. The only hits were the method names `#runSpawn`
  (`index.ts:854,1726`) and `#spawn` (`workpool.ts:265-294`). The name `runSubprocess` and the `subprocess` file
  names are historical labels: the function body is in-process (`executor.ts:4135-4137`).
- Conclusion: every `task` seat of a session lives on that session's `omp` main thread. If that process exits, for
  any reason, all of them end together. This half of Fact 4 holds.

### Are python seats' tool processes children of `omp`?

`sample.py shape`, python class at about 17:11Z (unit names shown with digits replaced by `N`; none contains a uid):

| python parent | `omp` ancestor | cgroup leaf | count |
|---|---|---|---|
| `omp` (rank 0, the session) | yes | the session's terminal app scope | 12 |
| `omp` (rank 1) | yes | rank 1's terminal app scope | 1 |
| `systemd` (user manager) | no | one model-provider shim service each (`antigravity-`, `claude-`, `codex-`, `cursor-`, `devin-`, `ds-flash-`, `glm-flash-`, `xai-shim.service`) | 8 |
| `systemd` | no | the session's terminal app scope | 1 |

- Yes: the session's python tool processes are direct children of the session `omp`, in the same cgroup scope. This
  seat's own shell is also a direct child of the session `omp` (ancestor names, nearest first: `omp`, `bash`,
  `alacritty`, ...).
- earlyoom signals one process (Fact 3, entry), so a send to `omp` does not signal these children. Whether they
  outlive the session is not read here. The one python process under `systemd` inside the session's scope looks like
  a reparented orphan. [INFERENCE] Either way, their seat's agent loop is gone with the parent.
- The model-provider shims are python-class processes with adjustment 200 that `omp` does not parent. A python-class
  send can therefore stop seats routed through a shim while `omp` lives. [INFERENCE: seat routing through the shims
  was not read] This is outside Fact 4's claim; it is noted only because Fact 5's python-victim count is read next to it.

## Impacted axes

- **Calibration:** a one-sample observation ("no other `omp` process was visible") is used to justify a structural
  rule. The rule's real basis, the in-process source, was not cited.
- **Depth:** the class-to-process mapping has more than one member, and the decision rows depend on telling them apart.
- **Provenance:** Limits line 171 says the model is "not a process-tree read". It can now cite both the source and
  the tree.

## Statement verdicts (tip `5f00fd04`)

| Where | Statement | Verdict | Severity |
|---|---|---|---|
| entry 118 | "The single `omp` process held the second-highest score" | holds for the 15:56Z sample only; wrong as a host description (3 now) | medium |
| entry 119-121 | in-session seats "run as subagents inside that one process [INFERENCE ...]" | holds; source-grounded (`executor.ts:2-4,4135`), no longer inference | low |
| entry 120-121 | "no other `omp` process was visible" as the basis | wrong now; 2 to 3 others seen at 17:09-17:12Z | medium |
| entry 121 | "when earlyoom picks it, every in-session seat of every lane ends at once" | holds for the session process; true for "every lane" only if each lane's seats are `task` jobs of that session [INFERENCE from the shared peer roster] | low |
| entry 158 / SKILL 727 | "the single `omp` process ranks second" | wrong as a standing statement; sample-dated | medium |
| entry 162 / SKILL 730 | an `omp`-class send means "the session process may have been the victim, which ends every in-session seat" | incomplete: omits that the class holds other processes whose kill ends no seat | high |
| lesson 18 | "One earlyoom send to `omp` is a fleet-wide event. The in-session seats live inside one `omp` process" | wrong: only a send to the session process is | high |
| entry 171 | "inference from the in-session design, not a process-tree read" | superseded by the source and the tree read | low |

## Smallest safe correction (exact old -> new)

The correction needs one new SOURCES row for `task/executor.ts` at v18.12.6, with the URL, access time and sha256
above. The L1 assigns its number, written as `S1xx` below.

1. Entry lines 118-121.
   Old: "The single `omp` process held the second-highest score on the host (847, about 7% of RAM plus swap above the 800
   floor of its band); only one `other`-class process at adjustment 300 ranked above it. The fleet's in-session seats
   run as subagents inside that one process [INFERENCE: they are `task` jobs of one session, and no other `omp` process
   was visible], so when earlyoom picks it, every in-session seat of every lane ends at once."
   New: "In this sample the only `omp`-class process held the second-highest score on the host (847, about 7% of RAM
   plus swap above the 800 floor of its band); only one `other`-class process at adjustment 300 ranked above it. The
   count is not fixed: a read at 2026-10-22T17:12Z (wave-2 CriticSingleOmpProcess) found three. They were the session
   process, a second interactive session and the text-prediction daemon worker at 800. The `omp daemon brok…` helpers
   class as `other`. oh-my-pi runs every `task` subagent in-process on the session's main thread (S1xx
   `task/executor.ts:2-4`). So when earlyoom picks the session process, every seat of that session ends at once. A
   send to any other `omp`-class process ends none of them, and the send line's 15-byte name does not tell them apart."
2. Entry line 158 and SKILL.md line 727.
   Old: "on this host the single `omp` process ranks second (Fact 4)" (SKILL: "on 2026-10-22 the single `omp` process
   ranked second on the host").
   New: "in the 15:56Z sample the session `omp` process ranked second (Fact 4)" (SKILL: "in the 2026-10-22T15:56Z
   sample the session `omp` process ranked second on the host").
3. Entry line 162 and SKILL.md line 730.
   Old conclusion: "the session process may have been the victim, which ends every in-session seat" (SKILL adds "of
   every lane at once").
   New conclusion: "the session process may have been the victim, which ends every seat of that session at once".
   Add to "What not to conclude": "that the victim was the session process: the `omp` class also holds other
   sessions and the text-prediction daemon worker".
4. Lesson line 18.
   Old: "**One earlyoom send to `omp` is a fleet-wide event.** The in-session seats live inside one `omp` process, which
   held the second-highest score on the host;"
   New: "**An earlyoom send to the session's `omp` process is a fleet-wide event.** Every `task` seat runs inside the
   session's `omp` process (oh-my-pi `task/executor.ts:2-4`), which held the second-highest score in the 15:56Z
   sample. An `omp`-class send line does not show which `omp` process was signalled;"
5. Entry line 171.
   Old: "The `omp` single-process seat model is inference from the in-session design, not a process-tree read."
   New: "Seats of one session share its `omp` process (S1xx `task/executor.ts:2-4`; tree read 2026-10-22T17:12Z, wave-2
   CriticSingleOmpProcess). The host runs more than one `omp`-class process, and a send line cannot say which one was
   signalled."

## Not checked

- I did not read which `omp` process received the boot -1 send, or whether rank 1 hosts fleet seats.
- I did not read whether `omp` kills its tool children on SIGTERM.
- I did not read whether seats route through the shims.

## Tooling and bounds

- No tool was installed or upgraded. I used the existing `python3`, `curl`, `strings`, `rg` and `git` (read-only).
- The harness moved one 70-second run of `sample.py shape` plus `count 7 10` to the background after its foreground
  wait ended. It finished without intervention. Its shape output matches the tree table above, and its seven counts
  are included above. No process was signalled or adjusted. I ran no `jj` command, made no git writes and did not run `omp`.

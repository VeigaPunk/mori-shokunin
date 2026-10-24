# ReviewPrivacyDesign — round-26 privacy review (before anything lands)

Seat: MoriR26.ReviewPrivacyDesign (reviewer, leaf — no subagents used). Date: 2026-10-22.
Inputs read: `.ufo/waves/round-26/contract.md`; `.ufo/waves/round-26/c1-phrases.txt`; `.ufo/waves/round-26/wave1-spec.json`;
`.ufo/waves/round-26/wave1-run.json`; `corpus/lessons/round-25-verifier-spotcheck.md:90-118`;
`.ufo/waves/round-18/frozen/c1-policy.json`; `tools/mori-retention-gate.py:1-93`; `corpus/evidence/retention-allowlist.json`;
`.ufo/waves/round-26/w1/MutCaseDesign.md`; the round-26 evidence receipts; earlyoom v1.9.0 `kill.c`/`main.c`
at the upstream tag (ordinary fetch, recorded below). Tooling directive: no tools installed this round;
verification used read-only git, `grep`/`curl`, nothing else.

Grounding quote (upstream, fetched 2026-10-22, sha256 of the byte-exact line confirmed by
`curl -fsS .../v1.9.0/kill.c | grep -n 'sending %s to process'` → line 627):
earlyoom v1.9.0 `kill.c:627` — `warn("sending %s to process %d uid %d \"%s\": oom_score %d, oom_score_adj %d,
VmRSS %lld MiB, cmdline \"%s\"\n", …)`. So one real earlyoom kill MESSAGE carries: pid, uid, process
name, oom_score, oom_score_adj, VmRSS, and the full command line. That is the single largest private
payload this round can touch. Threshold lines are safe by contrast (`main.c:414` and `:416` print only
percentages; `main.c:412` prints memory/swap totals — machine metadata, still outside the capture's
allowed line list, see F3).

## 1. Inventory: every path private text could take into the lane this round

| # | Path | Seats that touch it | Already prevented by | Residual gap |
|---|------|--------------------|----------------------|--------------|
| P1 | earlyoom journal kill MESSAGEs (kill.c:627 shape: pid, uid, name, cmdline) | HostCapture (capture.sh/capture.txt), ScoutHostJournal, BuildOomKillersTool (live mode), WriteOomKillersCases, DraftEntryR26 | Wave bounds: "never copy journal MESSAGE text that names a process, a command line or a uid" (wave1-spec.json:5). Contract: tool "never prints `MESSAGE` text, process names, command lines, uids" (contract.md:107-108). HostCapture prompt: only three fixed-format lines may be written, never --avoid/--prefer, never ExecStart, never /etc/default/earlyoom contents (wave1-spec.json:100). ScoutHostJournal: counts only (wave1-spec.json:110). Fixtures: invented process names only (contract.md:119). | Regex cannot tell a real kill line from an invented fixture line — same format string. A whole-journal transcript (e.g. raw `journalctl -o json` output pasted as "receipt") passes no token grep. Control must be structural: transcripts never committed; capture.txt line-inventory check (F3, §3). |
| P2 | `--dump-inputs` receipts | BuildOomKillersTool; any seat storing a receipt | Tool-side output of the reader is value-free (contract.md:107-108). | The contract's privacy bullet and its own `--dump-inputs` mode are in tension: `--dump-inputs` prints the live inputs object "for receipts" (contract.md:64-65), and that object embeds `earlyoom_journal` MESSAGE text verbatim. A seat following :64 literally could commit a receipt full of real kill lines. Fix and check in F1. |
| P3 | HostCapture output (capture.txt) | HostCapture, then L1 (copy into lane evidence) | The seat prompt restricts content to derived lines plus counts and mandates a five-token grep ('avoid','prefer','cmdline','uid','EARLYOOM_ARGS') (wave1-spec.json:100). | The grep is a token floor, not an inventory check: `main.c:412` totals lines and any stray banner line contain none of the five tokens. Add the inventory check before the lane copy (F3). |
| P4 | /etc/default/earlyoom values (--avoid/--prefer expressions, EARLYOOM_ARGS) | SrcEarlyoomUnit (fetches the Arch-shipped default file), HostCapture (forbidden), all seats via bounds | Wave bounds: never copy the values of the --avoid/--prefer expressions or of /etc/default/earlyoom (wave1-spec.json:5). SrcEarlyoomUnit prompt: "Do not copy the host's own /etc/default/earlyoom values" (wave1-spec.json:35). The tool never reads the config at all — thresholds come from earlyoom's own startup lines (contract.md interface; DraftSkillFr10 lists the config-reading habit as an error pattern, wave1-spec.json:70). | The upstream-shipped default file carries *example* --prefer/--avoid regexes; pasting them into a SOURCES row is upstream-public but value-shaped, and invites confusion with host values. Prefer mechanism description + URL:line citation (F6). |
| P5 | ExecStart | HostCapture (excluded by prompt), any seat tempted to read the effective command line | HostCapture prompt: "never ExecStart" and the -p property list excludes it (wave1-spec.json:100). | `systemctl show -p ExecStart` would print the unit's effective command line, which embeds the expanded environment args — i.e. the P4 payload in one line. No seat is asked for it; the check is a zero-tolerance grep for the output form `ExecStart=` in committed bytes (§3, block G). |
| P6 | OMP settings paths and values | All seats (citations in reports), L1 (integration notes) | Wave bounds: "cite path and key name only" (wave1-spec.json:5). Frozen classes R7 (config path refs and line numbers), R8 (the four routing-table key names), R9 (record-field names) — c1-policy.json:13-15 — are counted by the retention scan every candidate tip (contract.md:124-125). | No class covers the agent MCP json, or settings values of keys other than the R8 four. Round-25 saw exactly this escape ("copied values of four settings keys" rode into pushed history, round-25-verifier-spotcheck.md:99-104). Known_limit admits the floor (c1-policy.json:29): the L1 reading sweep stays mandatory. |
| P7 | Session ids / session-store paths | Any seat citing an OMP session | R1/R2 counted every tip; bounds forbid copying ids or store paths (wave1-spec.json:5). | None found: I ran the exact R1/R2/R3/R9 regexes over the round-26 worktree today — zero hits (command and date recorded in §4). Keep R1/R2 in every per-tip scan. |
| P8 | Kernel OOM journal lines | DraftEntryR26 (decision table includes "kernel OOM line vs earlyoom `sending` line", wave1-spec.json:65), ScoutHostJournal | Same wave bound covers them ("journal MESSAGE text that names a process…"). | Kernel kill text carries process names and command lines the same way [INFERENCE: standard `Out of memory: Killed process …` shape; I did not fetch kernel source this round]. Add the two tokens to the grep block (§3, block G) and keep such lines counts-only in the entry. |
| P9 | Timestamps, unit names, group names (metadata grade) | HostCapture, ScoutHostJournal | Prompt keeps them non-identifying: boot dates, monotonic timestamp, `user@1000.service` (already committed in the wave files), group-name presence only (wave1-spec.json:110). | Accepted practice in this lane; keep counts/dates/states only — no correlation narrative about operator activity. |
| P10 | Wave bookkeeping (wave1-spec/run/dispatch/response, swarm-registry, w1 reports) | L1 commits them this round | Nothing under `.ufo/waves/round-26/` is tracked at the entering tip (`git ls-tree -r 248408f5 -- .ufo/waves/round-26` is empty), so the first commit carries all of it. | Two known R7 hits ride in the bounds text itself — see F2; they must be allowlisted as judged name-only rows in the same commit, or the no-harm comparator false-alarms. |

## 2. Findings

### F1 (medium) — `--dump-inputs` receipts contradict the privacy bullet as written
contract.md:64-65 declares `--dump-inputs` prints "the live inputs object (for receipts)"; contract.md:107-108
says the tool never prints `MESSAGE` text. The inputs object embeds `earlyoom_journal` MESSAGE strings
(contract.md inputs shape), so a literal reading of :64 produces exactly the output :107 forbids. Left as is,
one seat will eventually "store the receipt" in the lane.
Recommended one-liner for the L1's integration notes (not a contract rewrite): "Raw `--inputs`/`--dump-inputs`
transcripts stay on stdout or in /fast/scratch; committed receipts carry only reader result objects, counts,
states and thresholds." Enforcement is structural — block G below flags `"earlyoom_journal"` and
`__MONOTONIC_TIMESTAMP` anywhere outside the three expected holders (contract.md, `tools/mori-oom-killers.py`,
`tools/fixtures/mori-oom-killers/cases.json`).

### F2 (medium) — the wave bookkeeping commit adds exactly two R7 hits; allowlist them deliberately
Verified today by running the exact R7 regex (`c1-policy.json:13`) over the round-26 worktree:
`wave1-spec.json:5` and `wave1-run.json:247` each carry one path-only mention of the OMP agent settings file
(the bounds paragraph, no values on either line). Since nothing under `.ufo/waves/round-26/` is tracked at
248408f5, the first wave commit moves the frozen metric from 4 to 6 unallowlisted unless these two lines get
rule-(a) allowlist rows (they qualify: instruction text naming a surface without its contents,
c1-policy.json:27; the round-25 precedent allowed 14 name-only rows the same way,
round-25-verifier-spotcheck.md:99-104). L1 actions: add the two rows judged in the same commit as the wave
files, and note "expected 4 allowlisted additions" in the round receipt so a later reader does not mistake
the delta for a leak. My own report intentionally avoids reproducing the R7-matching token.

### F3 (medium) — capture.txt needs an inventory check, not only the five-token grep
The seat's own grep ('avoid','prefer','cmdline','uid','EARLYOOM_ARGS', wave1-spec.json:100) cannot see:
(a) banner lines that carry none of the tokens — `main.c:412` prints memory/swap totals, which is machine
metadata outside the three allowed line kinds; (b) a script bug that dumps raw `journalctl -o json` bytes
into the output file. Before capture.txt (or any capture receipt) is copied into the lane:
1. run the five-token grep case-insensitively on the lane copy — must be empty;
2. assert every line matches exactly one allowed kind: the version line, the two threshold lines
   (main.c:414/:416 shapes), `systemctl` is-active/is-enabled/show property lines for the two units and the
   ManagedOOM properties of the four listed units, uname, `pacman -Q`, `systemctl --version` first line,
   per-class count lines, the oomd notice count, and timestamp headers;
3. confirm the script contains no `ExecStart=`, no `systemctl cat`, no EnvironmentFile read
   (`grep -nE 'ExecStart=|systemctl cat|EnvironmentFile' capture.sh` — must be empty).

### F4 (low) — kernel OOM lines are in the entry's decision table; give them the same MESSAGE hygiene
wave1-spec.json:65 puts "kernel OOM line" into the r26 entry's decision table. The bounds already cover it;
add the tokens `Out of memory` and `Killed process` to the per-commit grep block so a pasted kernel line
cannot ride in silently, and keep kernel evidence counts-only in the entry.

### F5 (low) — real-vs-invented kill lines are indistinguishable by regex; make "no transcripts" the rule
The cases fixture will contain kill-line MESSAGEs with invented names (contract.md:119) that match the same
shape as real ones (kill.c:627). No grep can separate them; therefore the committed-artifact rule is
structural: the only files allowed to contain instantiated journal MESSAGE text are
`tools/fixtures/mori-oom-killers/cases.json` (invented, frozen before the tool), the contract, and the tool
source. Anything else containing `"earlyoom_journal"` or `__MONOTONIC_TIMESTAMP` is a stop, not an
adjudication. The L1 reading sweep remains the real control (c1-policy.json:29 says the same for the
frozen classes).

### F6 (low) — upstream default-config examples: cite, do not paste
The Arch-shipped default `/etc/default/earlyoom` is upstream-public, but its example --prefer/--avoid regexes
are value-shaped and will trip the P4 check and confuse the host-vs-upstream boundary. SOURCES row should name
the mechanism (EnvironmentFile / the args variable name, StandardError default) with URL and line, without
pasting sample expressions.

### F7 (info) — what already holds, for the record
- The tool's contract output is value-free by design: states, numbers, version string, counts, thresholds
  (contract.md:107-109); read-only, no network (:109).
- Wave-2's mutation battery already carries a privacy scan of tool stdout/stderr as mutant D5
  (`.ufo/waves/round-26/w1/MutCaseDesign.md:48-49`) — keep it in the wave-2 baseline.
- The HostCapture prompt's own restrictions (three fixed-format lines, no --avoid/--prefer lines, no ExecStart,
  no /etc/default/earlyoom contents, post-run grep) match this review's checks (wave1-spec.json:100).
- Session id/store/artifact classes: zero would-be hits in the round-26 worktree today (§4).

## 3. Concrete pre-commit checks for the L1 (every candidate tip, before integration)

Cadence: the frozen retention scan is already mandated at the entering tip and every candidate tip
(contract.md:124-125; base receipt `.ufo/waves/round-26/evidence/retention-scan-base.txt`: exit 1,
unallowlisted_hits 4). Run block G at the same moments, plus once when capture.txt is copied into the lane
(F3 checks). Every block-G hit is either (i) inside an expected holder — contract.md, wave1-spec.json:5 /
wave1-run.json:247 bounds text, `tools/mori-oom-killers.py`, `tools/fixtures/mori-oom-killers/cases.json`,
w1 reports quoting this checklist, SOURCES rows naming the args-variable mechanism (name only) — verify
name-only, or (ii) a stop: do not commit until redacted.

```sh
# G — supplemental privacy grep over the round's changed files (committed bytes at the candidate tip).
# The frozen nine classes (session ids, store paths, settings refs/keys, record fields) are NOT
# duplicated here; the mandated gate scan covers them.
R=<candidate-tip>; B=248408f5b6610a85bcbdebe7ac0b4fa7ed51422a; L=/home/vgpnk/Projects/shokunin/mori-shokunin
git -C "$L" diff --name-only "$B" "$R" |
while IFS= read -r f; do
  git -C "$L" grep -n -E \
    'EARLYOOM_ARGS|--avoid|--prefer|to process [0-9]+ uid|cmdline[ ":=]|ExecStart=|/etc/default/earlyoom|Out of memory|Killed process|"earlyoom_journal"|__MONOTONIC_TIMESTAMP' \
    "$R" -- "$f"
done

# S — the mandated frozen scan (unchanged, for the counted metric):
python3 -I -B tools/mori-retention-gate.py scan --repo "$L" --rev "$R" \
  --policy .ufo/waves/round-18/frozen/c1-policy.json \
  --allowlist corpus/evidence/retention-allowlist.json
# expected after F2 rows land: unallowlisted_hits 4 (the four pre-existing round-20 fixture lines)
```

Token-by-token rationale for block G: `EARLYOOM_ARGS`, `--avoid`, `--prefer`, `/etc/default/earlyoom` → P4/P6
config values; `to process [0-9]+ uid` and `cmdline` → an instantiated kill.c:627 MESSAGE (P1/P5); `ExecStart=`
→ the effective-command-line dump (P5); `Out of memory`, `Killed process` → kernel OOM text (P8);
`"earlyoom_journal"`, `__MONOTONIC_TIMESTAMP` → raw transcript carriers (P1/P2/F1/F5).

## 4. Verification actually run for this review

- `git ls-tree -r --name-only 248408f5 -- .ufo/waves/round-26` → empty (wave files untracked at the entering tip).
- Exact frozen-class regexes R1/R2/R3/R9 over `.ufo/waves/round-26/` worktree, 2026-10-22 → 0 hits; exact R7
  regex → 2 hits (wave1-spec.json:5, wave1-run.json:247), both path-only bounds text.
- `curl -fsS https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c | grep -n 'sending %s to process'`
  → line 627 (payload shape as quoted above); same method for main.c → threshold lines 414/416; no
  `earlyoom %s` version-format hit surfaced in that grep pass (the contract's main.c:161 citation is the
  grammar reviewer's scope, not mine).
- Receipts read: `.ufo/waves/round-26/evidence/retention-scan-base.txt` (exit 1, unallowlisted 4 at 248408f5),
  `c1-before.txt` (stale_present=4, r26_entry=absent), `c2-before.txt` (exit 128) — all value-free.

## 5. Policy-class question: does the round-18 scan already cover earlyoom, or is a new class needed?

**Answer: not covered; do not edit the frozen policy this round; add an advisory supplemental scan now and a
counted class at the next freeze.**

- The nine frozen classes (c1-policy.json:7-15) cover the OMP/session/operator-config families only. Nothing
  matches an instantiated earlyoom kill MESSAGE, `EARLYOOM_ARGS` values, an `ExecStart=` dump, or kernel OOM
  text. The scan does not cover this round's new risk surface.
- The frozen file must not change mid-round: it is the round-18 frozen artifact whose sha256 the round-25
  receipt matched (round-25-verifier-spotcheck.md:91), and the contract's no-harm check counts against the
  entering value measured with it (contract.md:124-125). Editing classes now breaks both the receipt match
  and metric comparability.
- In-round (recommended): run the gate unchanged for the counted metric, plus either block G or — if the L1
  prefers one tool for both — an advisory scan with a round-26 policy file in the same v1 schema
  (`mori-retention-policy-v1`; the gate accepts any v1 policy, tools/mori-retention-gate.py:58-63) carrying
  two extra classes, e.g. `earlyoom_kill_message` = `to process [0-9]+ uid` and `earlyoom_config` =
  `EARLYOOM_ARGS|--avoid[ =]|--prefer[ =]|ExecStart=`, recorded beside the frozen metric as advisory.
- At the next freeze (round 27), if the lane wants these counted: expect the kill-message class to hit
  `tools/fixtures/mori-oom-killers/cases.json` (invented lines match the same regex — F5); each such line then
  needs a rule-(b) allowlist row after the L1 confirms the names are invented (c1-policy.json:27). The regex
  floor still cannot distinguish real from invented, so the reading sweep stays the primary control
  (c1-policy.json:29).

## 6. Residual risk and verification gaps

- capture.txt does not exist yet (HostCapture seat still running at review time); F3's checks are gates for
  the L1, unrun by me. The tool, cases, entry drafts and corrections are unlanded sandbox work; I reviewed
  the design artifacts (contract, spec prompts, frozen policy, gate tool), not implementations.
- Block G is a token floor: value-shaped private text without these tokens is caught only by the L1 reading
  sweep (same admission the frozen policy makes, c1-policy.json:29).
- [INFERENCE] items are marked inline: the kernel OOM line shape (P8/F4) and the note that
  `systemctl show` for multiple units may print unit headers in capture output (F3's inventory should
  tolerate them).
- No private values were read or reproduced: I never opened the host's /etc/default/earlyoom, never read any
  journal MESSAGE, and this report cites paths, key names and line numbers only.

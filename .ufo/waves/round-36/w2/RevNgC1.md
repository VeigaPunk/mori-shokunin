# w2 RevNgC1 — count-c1.py hidden-truth architecture: truth leaks, harness keys, K9 rerun, novel bypass

Seat: mori round 36, wave 2, attempt 2 (L1 MoriR36) — falsify + verify. Scope: reverse-engineer
`.ufo/waves/round-36/count-c1.py` for truth leaks and harness keys; re-run the K9 control under the
frozen v2 counter; one novel bypass attempt of my own design against the blind arm.
Lane repo untouched except this report file. All scratch under
`/fast/scratch/hyaku/mori-r36/RevNgC1/` (probe sources, raid dumps, run logs, bf0df77 clone).

## Item attacked

The hidden-truth architecture of the frozen C1 counter: P-C1's blind arm holds a 40-row fixture
truth (`id -> state`) that the `--tool` program must reproduce; the attack asks whether the truth
is ever observable by the tool (disk, env, /proc, server) and whether arm-detection keys can be
exploited; plus whether the v2 real-arm-on-repo design actually neutralizes such keys (K9).

## Pin verification (measured)

```
$ sha256sum .ufo/waves/round-36/count-c1.py
86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0  count-c1.py      # == evidence/freeze-v2.txt pin
$ git hash-object .ufo/waves/round-36/count-c1.py
b5888afe0c494c45e3a8abe06e6e60e849c101f0                                             # == evidence/freeze-v3.txt blob pin
$ git rev-parse bf0df77fee4b6ef54a90aea09335c7617f125151^{commit}
bf0df77fee4b6ef54a90aea09335c7617f125151
$ sha256sum .ufo/waves/round-36/c0/controls/K9.py
231ec3ea67bf808550cdd13a20f185c5e41a01db30edfb3bae064e416c30b1a4                     # == rescore receipt's K9 pin
kernel.yama/ptrace_scope = 1; euid = 1000
```

Counter bytes are the frozen v2/v3 pins. The lane worktree has moved past the data tip
(`git diff --quiet bf0df77 -- corpus` rc=1 at w2; corpus delta bf0df77→HEAD is SOURCES.md/QUALITY/
README/lessons only — `corpus/evidence/` copies untouched), so v2 re-runs that exercise the real
arm's `worktree_corpus == rev` precheck (count-c1.py:574-580) were done either at today's clean
tip HEAD (`4890c2d5`, worktree corpus rc=0, untracked-under-corpus=0) at the documented default
repo, or at `bf0df77` in a scratch clone (see §3 caveat).

## (1) Is the blind-arm truth ever written where the --tool program can read it? — NO

Code: `build_fixture` writes exactly three kinds of files under the fixture root — the registry
SOURCES.md (count-c1.py:492-500), the newest copies (508-510), and older decoy copies (512-524).
The truth is a returned in-memory dict (`return truth, served`, 526); the `served` bodies live in
the HTTP server's in-memory routes dict (351-356, 546). `run_tool` (277-285) adds no env, so the
child inherits the counter's environment — which carries no truth.

Executed bypass ("ancestral memory raid", probe `scratch/probe_raid.py` + corrected
`probe_raid2.py` that walks `os.getppid()` → `PPid` to reach the actual counter process past the
`timeout` wrapper, verified by its cmdline):

```
gp(counter) pid=1338885 cmdline="python3 -u .../count-c1.py bf0df77... --repo .../clone --tool .../probe_raid2.py"
counter environ readable: 37 vars; seed-in-env=False; truth-pattern-values=[]
counter maps readable: 206 mappings, heap=5577356ac000-557735b67000, anonymous=200
counter /proc/mem open refused: [Errno 13] Permission denied: '/proc/1338885/mem'
PTRACE_ATTACH to counter failed: errno=1 (EPERM)
py-spy on counter: Permission Denied (needs elevated permissions)
counter fds readable: 0->/dev/null 1->pipe:[...] 2->pipe:[...] 3->socket:[...] 4->pipe 6->pipe
```

(yama `ptrace_scope=1`: a child may not ATTACH its ancestor, so `/proc/<counter>/mem`,
`process_vm_readv` and py-spy are all gated off; `/proc/<ppid>/environ` of the `timeout` wrapper
was readable — same 38 vars, `truth-pattern-values: none`. Values were never written out of the
dump.) A filesystem sweep of the live fixture root, `/dev/shm`, `/tmp` and the scratch root —
80,928 files — found 14 regex hits for `S\d{3} (state)`, all historical prose in
`clone/.ufo/waves/round-{19,30,32}/...` reports and stale `/tmp/kama-r29*` trees; none encode any
current-run truth. The counter's own stdout becomes truth-bearing only after the tool's output is
fixed (`blind_mismatch ... truth=...`, count-c1.py:556-558) — a one-shot, post-decision leak; and
the fixture is redrawn per run (`seed` = `os.urandom(8)`, main ~699; four runs observed seeds
8711398136241714063 / 14321248632348249446 / 4275207608759667635 / 17523598065403430785), so
nothing transfers across runs. Blind-arm truth never reaches any byte the tool can read. The
architecture's real defense is stronger than secrecy: truth is derived data — `classify_fetched`
(105-120) computes every state from (body, copy), so an honest tool recomputes it and no oracle
shortcut exists.

## (2) Can a tool detect the blind arm — and does v2 make the key useless?

Detection: trivially yes. Blind root is `mkdtemp(prefix="mori-r36-c1-blind-")` under scratch
(count-c1.py:541, scratch_dir 527-535), cwd == root (278-285), all URLs on 127.0.0.1, and the
server sends no `Server`/`Date` headers (`send_response_only` + Content-Length only, 344-346;
probe observed exactly `[('Content-Length', '513')]`, 1.25 ms fetch). Probe telemetry:
`harness-key path check: root=.../mori-r36-c1-blind-3br2lxgi under_/fast/scratch|/tmp=True
prefix_mori-r36-c1-blind-=True`. Parent-chain detection (ppid) does not distinguish arms — both
arms spawn the same `timeout` wrapper from the same counter process.

Uselessness: under the v2 real arm the same binary must classify the lane's own repo at
`root = os.path.abspath(repo)` (573; DEFAULT_REPO line 59 = `/home/vgpnk/Projects/shokunin/
mori-shokunin`), where the standard key (root under `/fast/scratch`|`/tmp`, K9.py:105-106)
evaluates False, so the keyed branch must still be honest on genuinely drifted rows — and fails
on them (K9: 9 mismatches, §3). Conversely the blind arm contains rows in all five states
including 24 whose state is fetch-only, so a detected-but-forging tool fails blind outright:
my forged run printed `fresh`/`no-copy` without fetching → `blind_rows=40 tool_rows=40
mismatches=28` → `real_arm=skipped`, `C1=unmet`, exit 1 (probe-run.log; guessing blind labels
without fetching faces ~40!/(8!)⁵ ≈ 8e24 equally likely id→state assignments). Detection is
free; advantage from detection is zero. (K9's key and gated branch: K9.py:105-113.)

**Boundary observation (not a defect under the documented invocation):** the v1→v2 key
neutralization is a property of the invocation default, not of counter logic. The counter
accepts `--repo DIR`, and my first rerun pointed it at the scratch clone
(`/fast/scratch/hyaku/mori-r36/RevNgC1/clone`, corpus == bf0df77 verified rc=0): there K9's key
evaluates True on the real arm too (proven: `Path('/fast/scratch') in clone.parents` → True;
default repo → False), so K9 classified honestly everywhere and scored
`real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0
tool_exit=1 tool_rows=220 mismatches=0` → **C1=met** (k9-run.log). The scorer controls `--repo`
and the receipts/protocol pin the lane repo, so an attacker (who controls only `--tool`) cannot
reach this configuration; K9's diagnostic "unmet" is nevertheless repo-location-relative. If a
future round ever scores with `--repo` under `/tmp`|`/fast/scratch`, harness-keyed controls would
silently flip to met.

## (3) K9 control re-run under the frozen v2 counter — UNMET (confirmed, not assumed)

Documented invocation (default repo, today's clean tip `4890c2d5`; lane untouched):

```
$ MORI_R36_SCRATCH=/fast/scratch/hyaku/mori-r36/RevNgC1 \
  python3 -u .ufo/waves/round-36/count-c1.py 4890c2d571c5275f6a5c214545f79e59e0f4afca \
    --tool $PWD/.ufo/waves/round-36/c0/controls/K9.py
blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0
real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=0 tool_rows=220 mismatches=9
real_mismatch S156 tool=fresh oracle=drifted
real_mismatch S157 tool=fresh oracle=drifted
real_mismatch S158 tool=fresh oracle=drifted
real_mismatch S159 tool=fresh oracle=drifted
real_mismatch S160 tool=fresh oracle=drifted
real_mismatch S176 tool=fresh oracle=drifted
real_mismatch S177 tool=fresh oracle=drifted
real_mismatch S210 tool=fresh oracle=drifted
real_mismatch S211 tool=fresh oracle=drifted
C1=unmet
seed=17523598065403430785
```

Consistent with evidence/c0-rescore-v2.txt K9 section (blind 40/40 mismatches=0; 7 drifted
mismatches S156-S160/S176-S177 at the pre-data tip): the same drifted block plus S210-S211,
which are among the routed S205-S220 repair rows edited since bf0df77. The oracle stats also
match the C1 receipt's live conditions (fetched=58, fresh=49, drifted=9, excluded=0 — identical
to evidence/c1-after.txt). K9 is unmet for the right reason: its harness key disables fetching
exactly where the v2 real arm needs it. (The §2 clone run is the complementary half: same
counter, same K9 bytes, `--repo` under `/fast/scratch` → met.)

## (4) Novel bypass attempt — "ancestral memory raid + key-forged fallback" — CAUGHT

Design: as a blind-arm `--tool`, (i) raid every byte source a same-uid child can reach on its
ancestry (`/proc/<ppid,ppid>/cmdline,environ,maps,mem,fds`, `PTRACE_ATTACH`, py-spy) hunting an
`S\d{3} (state)` map; (ii) if truth is recovered, print it and pass blind without fetching;
(iii) else print key-forged answers (any copy → `fresh`, none → `no-copy`) — detection-without-
truth is still an advantage if the blind truth were ever predictable.

What the counter did (probe-run.log, run at bf0df77 in the clone):
```
blind_rows=40 tool_exit=0 tool_rows=40 mismatches=28
blind_mismatch S038 tool=fresh truth=excerpt   ... (8 excerpt, 8 drifted, 8 unavailable,
blind_mismatch S194 tool=fresh truth=no-copy    4 copy-without-URL no-copy rows)
real_arm=skipped
C1=unmet
seed=14321248632348249446
```
A second run that printed nothing (raid-only) failed 40/40 `<absent>` (seed 4275207608759667635,
exit 1, real skipped, ~seconds — no oracle cost). The raid recovered zero usable truth (§1), so
the bypass reduces to a no-fetch guess and the counter rejects it deterministically. Total bypass
value extracted: none; cost to the counter: none (blind arm fails fast, real arm skipped).

## Residuals observed (not new; disclosed)

- count-c1.py module docstring still describes the v1 real arm ("`git archive <rev>` extraction …
  never the live worktree", lines ~20-25) while the v2 code runs on the repo itself (567-574) —
  already disclosed in evidence/freeze-v3.txt ("module docstring still says v1 (cosmetic; bytes
  frozen)"). Predicate sentence P-C1 in code (33-39) matches contract/receipt.
- The §2 `--repo`-location relativity of harness-key neutralization — flagged above as a
  boundary observation with concrete evidence; no remediation proposed (frozen bytes; detection
  and report only).

## Tooling installs (operator authorization 2026-10-19)

- `uv tool install py-spy` → py-spy 0.4.2 (official PyPI via uv; used for the memory-read bypass
  attempt against the counter process; denied by yama as designed). No pacman use.

## VERDICT: PASS

No defect found in the attacked surface. The blind-arm truth never reaches disk, env, server
metadata, or any /proc channel a same-uid child can read (heap located via maps but `/proc/mem`,
ptrace and py-spy all denied under yama ptrace_scope=1); arm detection is trivial but strictly
valueless because the blind state is derivable only by honest fetch+compare and the v2 real arm
punishes the mirrored key at the documented repo (K9 unmet, 9 drifted mismatches, re-confirmed
under the frozen v2 bytes); one novel bypass (ancestral memory raid + forged fallback) recovered
no truth and was caught 28/40. Boundary observation on record: with `--repo` placed under
`/fast/scratch`|`/tmp`, K9 scores met (run k9-run.log) — the anti-key property is invocation-
relative, unreachable by an attacker who controls only `--tool`.

# Mo50bSentCopies — security and hygiene review of the round-50 source copies, the C2 entry and the wave records

Seat: leaf (no subagents). Read-only review at the landed data commit
`487941b9395e89678af0053cc443cdb49cdee6e3` (verified ancestor of the lane tip
`4548a34dc8b4072abaa4335c1f54a9efcfcc314a`), plus the working tree at that tip where this wave's own
untracked artifacts exist.

Surface: `corpus/evidence/sources-r50/{cgroup-v2.7.2.html,memcontrol.c.v7.2,oom_kill.c.v7.2}`,
`corpus/knowledge/oom-memcg-stat-r50.md`, `.ufo/waves/round-50/` (committed files at `487941b9` and the
wave-a2w1 files), and the two control scripts `.ufo/waves/round-50/controls/{c1,c2}-controls.py` with the
counters they drive.

Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bSentCopies/` (`mkdir -p`, `TMPDIR` exported there, one copied
script for the bytecode probe), removed at the end (§9). No clone. No tool installs, no pacman transaction,
no host log read, no cgroup/OOM action, no write outside this report and that scratch dir. No git mutating
command was run (only `log`, `show`, `ls-tree`, `grep`, `rev-parse`, `check-ignore`, `ls-files`,
`merge-base --is-ancestor`).

## 1. The three copies — sha256 against `count-c2.py`'s COPIES and against the freeze manifest

`COPIES` (`.ufo/waves/round-50/count-c2.py:40-47`) pins three digests; `evidence/freeze-sha256.txt:1-3`
lists the same three. I hashed the **committed blobs** at `487941b9`, the **working tree** and the
**freeze file**, and compared all three views.

```
$ git show 487941b9:corpus/evidence/sources-r50/<f> | sha256sum   # blob
$ sha256sum corpus/evidence/sources-r50/<f>                        # worktree
```

| copy | committed blob @487941b9 | working tree | COPIES / freeze-sha256 | verdict |
|---|---|---|---|---|
| `cgroup-v2.7.2.html` | `2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34` | same | `2d716cb7…0bf34` | match |
| `memcontrol.c.v7.2` | `8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e` | same | `8a28e0bc…1fd5e` | match |
| `oom_kill.c.v7.2` | `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` | same | `452f1348…56b4e` | match |

No drift between the pinned digests, the committed blobs and the bytes the counter actually reads at
`487941b9` (the counter reads the revision's blobs through `git_reader`, `count-c2.py:211-216` and the
pin loop at `count-c2.py:117-121`; only the selftest and the controls read the working tree,
`count-c2.py:248-253`, `controls/c2-controls.py:30-31`). The entry's own `recheck:` line carries the same
three digests in the same order (`corpus/knowledge/oom-memcg-stat-r50.md:7`), so the recheck command is
reproducible from the recorded bytes.

## 2. Credential material, tokens, private URLs, machine ids

Pattern census over the five targets (three copies + entry; the whole `round-50` tree for the URL and
machine-id rows):

```
$ for pat in csrf sessionid _token password secret 'api[_-]?key' 'BEGIN [A-Z ]*PRIVATE KEY'; do
    grep -oiE "$pat" corpus/evidence/sources-r50/* corpus/knowledge/oom-memcg-stat-r50.md | wc -l; done
csrf -> 0   sessionid -> 0   _token -> 0   password -> 0   secret -> 0
api[_-]?key -> 0   BEGIN … PRIVATE KEY -> 0
```

- **URLs.** `grep -hoE "https?://[A-Za-z0-9._-]+"` over the entry: `docs.kernel.org` ×2,
  `raw.githubusercontent.com` ×4. Over the HTML copy, the only non-kernel hosts are Sphinx footer links
  (`alabaster.readthedocs.io`, `docutils.sourceforge.io`, `www.sphinx-doc.org`), one each, all inside
  `<a href>` in the page footer. Over the committed `round-50` blobs at `487941b9`, the only two hosts
  anywhere are `raw.githubusercontent.com` (34) and `docs.kernel.org` (13). No `file://`, `localhost`,
  `127.0.0.1`, RFC1918 address, `.internal` name, `ssh://` or `git@` form occurs in any committed wave
  blob (`git grep -nE "file://|localhost|127\.0\.0\.1|…|git@|ssh://" 487941b9 -- .ufo/waves/round-50`
  → no matches). Nothing here is a private or credential-bearing URL.
- **Machine id.** `/etc/machine-id` (32 hex) appears **0 times** in the committed `round-50` blobs at
  `487941b9` and at `HEAD`, and 0 times in the four corpus targets. The hostname and short hostname
  appear 0 times in each of the four corpus targets.
- **Live leak found and closed in this wave.** While scanning the *untracked* `a2w1` reports, the
  machine-id matched one line:
  `.ufo/waves/round-50/a2w1/Mo50bRevRowsOomB.md:4` printed `MACHINE_ID: <the host's 32-hex machine-id>`
  verbatim (value not reproduced here). I messaged the peer; it replaced the value with the literal
  `MACHINE_ID` and confirmed. Re-verified after the fix:
  `grep -rlF -- "$(tr -d '\n' </etc/machine-id)" .ufo/waves/round-50/a2w1 | wc -l` → `0`, and
  `… .ufo/waves/round-50 | wc -l` → `0`.
- **Emails.** Three unique addresses occur, all in `memcontrol.c.v7.2` (lines 5, 8, 5699 —
  `balbir@linux.vnet.ibm.com`, `xemul@openvz.org`, `linux-mm@kvack.org`): upstream copyright/maintainer
  metadata from the kernel file, public, not credential material. A `[0-9a-f]{40,}` scan finds nothing in
  the three copies; the only long-hex strings in the five targets are the three sha256 digests in the
  entry's `recheck:` line.

## 3. Absolute host paths — the `/home/vgpnk` count, executable defaults versus prose

Counts are **occurrences** (`bytes.count(b"/home/vgpnk")` over each committed blob / working-tree file),
not `grep -c` lines; the two differ by ~4× in the JSON files.

**At the data commit `487941b9`: 345 occurrences in 12 files.**

| file | occurrences | kind |
|---|---|---|
| `.ufo/waves/round-50/w1-spec.json` | 154 | data: seat prompts/context serialised in JSON |
| `.ufo/waves/round-50/w1-dispatch.json` | 154 | data: same text, dispatch form |
| `.ufo/waves/round-50/w1/Mo50ScribeRowOomKill.md` | 9 | prose (report) |
| `.ufo/waves/round-50/build-w1-spec.py` | 7 | **3 executable defaults** (`L7 L`, `L8 F`, `L10 S` — string literals used to build every path) + 4 prose (prompt bodies at `L32`, `L33`, `L93`, `L124`) |
| `.ufo/waves/round-50/w1/Mo50ScoutCoverageFR1.md` | 7 | prose |
| `.ufo/waves/round-50/w1/Mo50ScribeEntryA.md` | 5 | prose |
| `.ufo/waves/round-50/w1/Mo50ScribeRowMemcontrol.md` | 4 | prose |
| `.ufo/waves/round-50/controls/c2-controls.py` | 1 | **executable default** (`L20 STAGED`) — used by `open()` at `L32-33` |
| `.ufo/waves/round-50/contract.md` | 1 | prose (`L84`) |
| `.ufo/waves/round-50/evidence/census-start.txt` | 1 | observed output line (`L22`, the census's absolute path column) |
| `.ufo/waves/round-50/w1.ready` | 1 | data: dispatch pointer (machine-specific, not executed) |
| `.ufo/waves/round-50/w1/Mo50ScribeEntryB.md` | 1 | prose |

So of 345, **4 are executable defaults**: `build-w1-spec.py:7,8,10` and `controls/c2-controls.py:20`.
Everything else is prose, prompt data, a ready-pointer, or an observed-output line. The two frozen
counters carry **none** — both derive the lane from `__file__` (`count-c1.py:264-266`,
`count-c2.py:220-221`), which is why the counters are the portable part of the instrument set.

`/fast/` scratch paths: **49 occurrences at `487941b9`** — 36 in the two JSON files, 10 in wave-1
reports, `build-w1-spec.py:20` (`X = "/fast/scratch/hyaku/mori-r50"`, an executable default), plus
`assimilation/a2/mirror-validate.txt:24` and `evidence/selftests/mori-unlanded-check.txt:14`, which
record a scratch path as part of their output (finding F5 below).

**At the tip `4548a34` (this wave): 839 occurrences in 30 files** — `a2w1-spec.json` 217 and
`a2w1-dispatch.json` 217 (same prompt-data pattern), `w1-spec.json`/`w1-dispatch.json` 154 each, the
rest in reports; `build-a2w1-spec.py` has one executable default (`L13 S`) and one `/fast` default
(`L24 X`), the other five of its six occurrences are prompt prose (`L39`, `L40`, `L112`, `L118`,
`L177`). `/fast/` at the tip: 225. `a2w1/*.md` reports are untracked (`git ls-files …/a2w1 | wc -l` → 0),
so the L1 controls what enters the integration commit.

The four corpus targets contain **no** `/home/…`, `/fast/…`, `/tmp/…`, `/root/…` or `/Users/…` string
(`grep -n "/home/\|/fast/\|/tmp/\|/root/\|/Users/" <targets>` → no output), so the entry is portable and
the copies are byte-exact upstream fetches; the absolute paths live in the instrument and the wave
records, not in the knowledge corpus.

## 4. Embedded scripts and active content in the HTML copy

```
bytes 168438, lines 3257
script elements: 8   (6 external src, 2 inline)
  external src: ../_static/{documentation_options,jquery,underscore,_sphinx_javascript_frameworks_compat,doctools,sphinx_highlight}.js
  inline: 60 bytes  document.getElementById('searchbox').style.display = "block"
          229 bytes  <!-- var sbar = document.getElementsByClassName("sphinxsidebar")[0]; … (HTML-comment wrapped JS)
style blocks: 0   HTML comments: 1   event handlers (onload/onerror/onclick/onmouseover): 0
javascript: URIs: 0   iframes: 0   meta refresh: 0   <base>: 0
forms: 1  <form class="search" action="../search.html" method="get">   (no hidden/csrf/_token input)
```

Reading: the copy is a Sphinx-generated page. Every script URL is **relative** (`../_static/…`) and none
of those files is committed, so opening the file offline loads no remote code and executes only two tiny
DOM tweaks; there is no event-handler attribute, no `javascript:` URI, no iframe, no meta refresh and no
`<base>` that could re-point the relative URLs; the single form is the inert search box with a relative
action and no token field. The only external origins appear as footer `<a>` links (`alabaster.readthedocs.io`,
`docutils.sourceforge.io`, `www.sphinx-doc.org`). It is safe as *inert evidence* but must not be served
as an application page — I found nothing in it that would matter if it were, only that it was never
written to be hosted.

Quote provenance relative to the active blocks: the entry has 26 backticked spans of ≥6 words; **0** of
them occur inside a `<script>`, `<style>` or `<!-- -->` block of the copy, and **0** of them are located
only after the counter's tag-stripping joins text across elements (each also occurs in the raw,
whitespace-collapsed document). So no row's provenance depends on the stripping step, and nothing is
smuggled through the two inline scripts or the one comment.

## 5. File sizes against the 1 MiB skip

| file | bytes | MiB |
|---|---|---|
| `corpus/evidence/sources-r50/cgroup-v2.7.2.html` | 168 438 | 0.161 |
| `corpus/evidence/sources-r50/memcontrol.c.v7.2` | 160 768 | 0.153 |
| `corpus/evidence/sources-r50/oom_kill.c.v7.2` | 34 311 | 0.033 |
| `corpus/knowledge/oom-memcg-stat-r50.md` | 10 538 | 0.010 |

Largest file added by the round at `487941b9` is `w1-dispatch.json` at 64 020 bytes; largest in the whole
wave tree at the tip is `a2w1-dispatch.json` at 88 705 bytes (0.085 MiB). Nothing approaches a 1 MiB
threshold, so no size-skip can hide any of these files.

`UNVERIFIED` which helper the seat's parenthetical names: I searched `tools/*.py` and
`scripts/hyaku/*.{sh,py}` for a directory scan that skips new files over 1 MiB and did not find one. The
size gates I did find are `scripts/hyaku/jj-lane.sh:638` (skip untracked files over 10 MiB unless
`allow_large`) and per-stream capture caps (`tools/mori-round16-regressions.py:146`,
`tools/mori-journal-window.py:56-57`). All four targets are far below 1 MiB, 10 MiB and every cap found,
so the conclusion does not depend on which helper was meant.

## 6. The control scripts — can they write into the lane outside `evidence/`, or commit in the lane?

**Commit: no.** Every `git` call and its `-C` target, traced:

| script | call | target | subcommand kind |
|---|---|---|---|
| `controls/c1-controls.py:39` | `g(repo, …)` helper (`git -C repo …`) | dispatch | — |
| `:78` | `git clone -q --shared --no-checkout LANE d` | reader (LANE) → new dir `d` | read of LANE |
| `:79` | `g(d, "rev-parse", "--show-toplevel")` | **clone** | read |
| `:82-83` | `g(d, "config", …)` ×2 | **clone** | write (identity, clone only) |
| `:84` | `g(LANE, "rev-parse", …)` | **lane** | read |
| `:86` | `g(FLEET, "show", MANIFEST.json)` | **fleet** | read |
| `:88-89` | `g(LANE, "show", …)` ×2 | **lane** | read |
| `:94` | `git -C LANE archive base` | **lane** | read (stdout → tar) |
| `:128` | `g(d, "checkout", "-q", "--detach", base)` | **clone** | write |
| `:135` | `g(d, "commit", "-q", "-m", "control")` | **clone** | write |
| `:136` | `g(d, "rev-parse", "HEAD")` | **clone** | read |
| `controls/c2-controls.py:27` | `git -C LANE rev-parse` | **lane** | read |
| `count-c1.py:271,275,285,289,299` | `git -C repo rev-parse/show/cat-file/archive` | caller's repo | read only |
| `count-c2.py:213,233` | `git -C repo show/rev-parse` | caller's repo | read only |

`config`, `checkout`, `add` and `commit` appear only for `d`, the `--shared` clone created at `:78`
inside the operator's `--scratch`; the toplevel equality check at `:79-81` (`realpath(rev-parse
--show-toplevel) == realpath(d)`) runs before the fixture identity is set at `:82-83` and before the first
`checkout`/`commit`, exactly as the lane fixture rule requires. The only subcommands that name the lane or
the fleet are `rev-parse`, `show`, `cat-file` and `archive`, none of which writes. A `--shared` clone
borrows the lane's object database read-only through `alternates`; a commit in `d` writes objects into
`d/.git/objects`. So neither control can commit in the lane, and when the counter is run with
`--repo LANE` (`repo = d if edits else LANE`, `c1-controls.py:137`) its git calls are still read-only.
`c2-controls.py` never clones and never edits a revision at all; it scores an overlay reader over the
entering bytes.

**Receipt writes: inside `evidence/` only.** `c1-controls.py:142-144` writes
`evidence/control-c1-<name>.txt` for 8 fixed names; `c2-controls.py:51-53` writes
`evidence/control-c2-<name>.txt` for 4 fixed names. No other `open(…, "w")` exists in either script.

**Write outside `evidence/`: yes — one, the bytecode cache.** Both scripts load the frozen counter with
`importlib.util.spec_from_file_location` + `exec_module` (`c1-controls.py:27-29`,
`c2-controls.py:22-24`) *before* any `PYTHONDONTWRITEBYTECODE` is set (that variable is only injected into
the selftest subprocess env, `c1-controls.py:98`). A source-file load through `importlib` caches bytecode
next to the source, so running either control writes
`.ufo/waves/round-50/__pycache__/<stem>.cpython-314.pyc`. Observed in the lane:

```
$ ls -la .ufo/waves/round-50/__pycache__/
-rw-r--r-- 40528 count-c1.cpython-314.pyc
-rw-r--r-- 30816 count-c2.cpython-314.pyc
$ python3 -c 'read 16-byte pyc header'   →  src_size 23160 (count-c1.py) / 18351 (count-c2.py)
```

Both `src_size` values equal the byte sizes of the two counters, so the cache files are exactly the two
`exec_module` loads. Reproduced the mechanism off-lane on a copy (no lane write):

```
$ mkdir -p /fast/scratch/hyaku/mori-r50/Mo50bSentCopies/tmp; export TMPDIR=…
$ cp …/count-c2.py /fast/scratch/hyaku/mori-r50/Mo50bSentCopies/probe-count-c2.py
$ python3 -c 'importlib.util.spec_from_file_location("probe","probe-count-c2.py") … exec_module'
after exec_module, pycache: ['__pycache__/probe-count-c2.cpython-314.pyc']
```

Consequences: the module docstring's claim "Nothing is written in the lane except the receipts"
(`c1-controls.py:8`) is false; the lane's working tree
gains an untracked directory on every control run. It cannot reach a commit as written — `.gitignore:3`
is `__pycache__/`, and `git check-ignore -v` confirms the files are ignored — but it means a control run
mutates the tree outside `evidence/`, and any future change to the ignore rule (or a `git add -f`) would
carry .pyc binaries into the freeze. Smallest remediation (not applied, counters and controls are frozen
for this round): `sys.dont_write_bytecode = True` before the `exec_module`, or run the scripts with
`python3 -B` / `PYTHONDONTWRITEBYTECODE=1` in the environment.

**Two smaller path/cleanup hazards in `c1-controls.py`.** (a) `--scratch` is used unvalidated: `:75`
`os.makedirs(scratch)` and `:77` `rm -rf -- <scratch>/c1-fixture` will create and delete a directory
inside the lane if the operator points `--scratch` at the lane or a lane subdirectory. (b) There is no
`try/finally` around the clone: if the 900 s selftest at `:99-100` raises `TimeoutExpired`, or the
`archive|tar` at `:94-97` fails, `rm -rf d` at `:148` is never reached and the `--shared` clone (plus its
`alternates` pointer at the lane) survives in scratch. Neither harms the lane; both break the
cleanup promise on the failure path. The counter itself does clean up (`count-c1.py:319-323`, `finally`).

## 7. One trust-boundary observation in the C1 instrument: data names the program it executes

`count-c1.py` does not merely read `SHONEN.md`; it **executes** the file the tally pin names:

```
PIN = re.compile(…)                       # count-c1.py:49-52, the backticked `python3 <path> --selftest` span
bound_path(cmd)                           # :160-170  accepts any repo-relative *.py (no leading /, no .., ends .py)
check_pins(...) → run(path)               # :171-200  each pin whose path exists at R is run
run(path)                                 # :296-314  subprocess.run([sys.executable, path, "--selftest"],
                                          #            cwd=extracted tree, env=dict(os.environ, TMPDIR=…), timeout)
```

So the self-assessment file chosen as the claim surface selects a program the scoring instrument runs,
with the caller's environment and cwd in a `git archive` of R. The pin path is constrained (`bound_path`:
no absolute path, no `..`, must end `.py`, must exist at R), the printed tally must match the pin and a
committed receipt must hold the same `PREFIX pass=P fail=F` line, and the axes half plus the 4-box /
2-pin floors still apply — so a bogus pin cannot by itself pass C1. But a committed stub that prints the
expected line would satisfy the SHONEN half, because both the command and its receipt are lane-authored
data. This is a named limit of the calibration claim (self-written instrument executed during scoring),
not a defect of the landed data; the counters are frozen and I propose no change.

## 8. Permissions and records

`find .ufo/waves/round-50 corpus/evidence/sources-r50 -type f \( -perm -o+w -o -perm -4000 -o -perm -2000 \)`
→ no output (no world-writable, setuid or setgid file); `find … -type l` → no output (no symlinks in the
wave tree or the copy directory). Git modes at `487941b9`: the two controls are `100755`, the three copies
`100644`. In the untracked a2w1 directory, `swarm-registry.json` is mode `0600` while every report is
`0644` (the dispatcher's own file; noted, not scored).

## 9. Scratch

`/fast/scratch/hyaku/mori-r50/Mo50bSentCopies/` held one copied counter (`probe-count-c2.py`), the
`__pycache__` the probe created, and `tmp/`. Removed before yield; nothing cited here depends on it (all
evidence is quoted above). No tool was installed or upgraded.

## Findings

1. **MED — host machine id printed verbatim in a wave report (closed in-wave).**
   `.ufo/waves/round-50/a2w1/Mo50bRevRowsOomB.md:4` carried `MACHINE_ID: <the host's 32-hex machine-id>`
   in plain text; the lane rule requires the literal `MACHINE_ID`. The file is **untracked** (it is not in
   `487941b9`; `git ls-files .ufo/waves/round-50/a2w1` → 0), so the landed data is unaffected. Reported to
   the peer, which replaced the value with `MACHINE_ID`; re-verified 0 occurrences of the machine-id in
   `.ufo/waves/round-50` afterwards. Residual risk: the L1 must not integrate that file if any copy of the
   pre-fix text survives elsewhere.
2. **MED — `count-c1.py` executes a repo file named by `SHONEN.md` data during scoring.**
   `count-c1.py:49-52,160-170,171-200,296-314`: a backticked `python3 <relative>.py --selftest` pin is run
   with `sys.executable`, the caller's environment and a `git archive` tree as cwd. Data-directed code
   execution inside the instrument; a committed stub can satisfy the SHONEN half of C1. Named limit for
   the report (counters frozen).
3. **LOW — the control scripts write into the lane outside `evidence/`.**
   `controls/c1-controls.py:27-29` and `controls/c2-controls.py:22-24` load the counter with
   `importlib` `exec_module`, which writes `.ufo/waves/round-50/__pycache__/count-c{1,2}.cpython-314.pyc`
   (both present; pyc headers carry `src_size` 23160 and 18351 = the two counters). Falsifies the
   docstring claim at `controls/c1-controls.py:8` that nothing but receipts is written in the lane.
   Gitignored (`.gitignore:3`), so it cannot be committed as configured.
4. **LOW — absolute host paths as executable defaults.**
   `controls/c2-controls.py:20` (`STAGED = "/home/vgpnk/Projects/shokuknow/merge/mori"`, used by `open()`
   at `:32-33`), `build-w1-spec.py:7,8,10` and `:20` (`/fast/scratch/...`), `build-a2w1-spec.py:13` and
   `:24`. These four files only run on this host/layout; the two frozen counters and both output paths are
   portable. Counts: 345 `/home/vgpnk` occurrences (4 executable defaults) at `487941b9`, 839 at the tip;
   four corpus targets: 0.
5. **LOW — a scratch path is recorded as evidence.**
   `assimilation/a2/mirror-validate.txt:24` records `/fast/scratch/hyaku/mori-r50/l1/validate/corpus/SOURCES.md`
   as the validated path, and `evidence/selftests/mori-unlanded-check.txt:14` embeds a
   `/fast/scratch/...` path in a PASS message. The artifacts named there are removed with the scratch dir,
   so the receipts are not re-checkable later without re-running; the rule "a /tmp path is never evidence"
   is honoured literally (no `/tmp` path is used as evidence), but a scratch path is equally non-durable.
6. **LOW — no failure-path cleanup in `controls/c1-controls.py`.**
   The clone is removed only at `:148`, outside any `try/finally`; a `TimeoutExpired` at `:99-100` or an
   `archive|tar` failure at `:94-97` leaves the `--shared` clone (borrowing the lane's object DB) in
   scratch. `--scratch` is also unvalidated (`:75`, `:77`): pointing it at the lane creates and deletes a
   directory inside the lane.
7. **LOW — the HTML copy carries two inline scripts and a form.**
   `corpus/evidence/sources-r50/cgroup-v2.7.2.html`: 8 `<script>` elements (6 with relative
   `../_static/...` src, 2 inline at 60 and 229 bytes, the larger wrapped in an HTML comment), 1 inert
   `action="../search.html"` form with no token field, 0 event handlers, 0 `javascript:` URIs, 0 iframes,
   0 meta refresh, no `<base>`. No live external origin for code or styles. Safe as inert evidence, but not
   a page to serve; the counter's `normalise()` strips exactly these blocks and no entry quote lives inside
   one.

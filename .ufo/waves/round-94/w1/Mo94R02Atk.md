# Seat Mo94R02Atk — attack P-C2 (literal scan + HOME isolation), round-94 w1

Scratch: /fast/scratch/hyaku/mori-r94/Mo94R02Atk (deleted before yield). One shared clone:
`git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/mori-shokunin $S/clone`.
Fixtures: one `git -C <fixture worktree>` commit each at `-fixture-<name>`; toplevel asserted
before every commit. Frozen counter invoked from `$S/fixture-base/.ufo/waves/round-94/count-c2v2.py`
(unmodified bytes of 6b65e7c1); `SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin`; explicit `TMPDIR=$S/tmpdirlit`.

## 0. Baseline (freeze rev 6b65e7c1, my clone)

    $ python3 -I count-c2v2.py 6b65e7c1 --repo $S/clone --root <fleet>
    C2=met literal_r94=0 files_r94=3 frozen_r93=unchanged env_i=met env_unset=rc2 rev=6b65e7c11f31 rc=0
    $ python3 -I count-c1v2.py 6b65e7c1 --repo $S/clone --census <fleet>/scripts/sources-census.sh
    C1=met trio=98 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok rev=6b65e7c11f31 rc=0
    $ python3 -I controls-r94.py $S/clone <fleet>
    EMBED_FALSE_PASS v1=3/3 v2=0/3 live_v2=met do_nothing_v1=C1=met do_nothing_v2=C1=met rc=0

Frozen counter self-scan note: `count-c2v2.py` docstring contains the regex itself and the
`/home/<user>` mention (bytes 663, 1637); the frozen regex is anchored to a user segment start
(`[a-z_][a-z0-9_-]*`), so it does **not** self-count (`literal_r94=0`) — measured, not guessed.

## 1. Predicate P-C2 attacks — planted under `.ufo/waves/round-94/`

Scan machine (extracted tree, `os.walk` + `HOST = re.compile(rb"/home/[a-z_][a-z0-9_-]*")`, files ≥ 3).

| # | form (file `.ufo/waves/round-94/planted-*`) | lit Δ | pred verdict | host path? | reason |
|---|---|---|---|---|---|
| 1 | `/home/VGPNK/x` (.py, 08fd1c67) | 0 | `C2=met literal_r94=0` rc 0 | no | literal; uppercase ≠ host user `vgpnk` |
| 2 | `/home/.hidden/x` (.py, e1a19377) | 0 | `C2=met` rc 0 | no | `.hidden` is a directory name, not a user |
| 3 | `~vgpnk/x` (.py, e7e8fcf2) | 0 | `C2=met` rc 0 | no | tilde path; no `/home` bytes; expands to host only via shell |
| 4 | `$HOME/Projects/x` (.py, 2b76b802) | 0 | `C2=met` rc 0 | no | unexpanded env ref, not a literal |
| 5 | `/Users/vgpnk/x` (.py, 23c41630) | 0 | `C2=met` rc 0 | no | macOS prefix, `/Users` ≠ `/home` |
| 6 | `C:\Users\vgpnk\x` (.py, 8aa6a339 two `\`; 31ec4fed one `\`) | 0 | `C2=met` rc 0 | no | Windows path |
| 7 | `/home/vgpnk/x` inside planted-**.json**, planted-**.md** (8441a722, 04649065) | 0 (files 4→3) | `C2=met literal_r94=0` rc 0 | **yes** | real host path; scanner reads only `.py`/`.sh` (`SUFFIXES`, count-c2v2.py:38) |
| 8 | adjacency: enhanced-regex aux scan sees ALL forms (see §2); frozen lanes unaffected | — | — | — | sensitivity proof |
| 9 | `/home/vgpnk/x` in `.env` (99c4a06d) | 0 | `C2=met` rc 0 | **yes** | suffix-gated, same gap as #7 |
| 10 | `/home/vgpnk/x` in `planted-extcase.**PY**` (a42a4795) | 0 | `C2=met` rc 0 | **yes** | `endswith((".py",".sh"))` is case-sensitive |
| 11 | split literals `"..."/ho` + `me/vgpnk` across two string literals (.json/.md, 5c43547a, cec50011) | 0 | `C2=met` rc 0 | yes-as-tested-source | concatenation at runtime reconstitutes the path; byte scan cannot see it (all regex-scan designs share this named limit) |
| 12 | symlink `planted-symlink.py → real-history.txt` containing `/home/vgpnk/x` (192b9341) | +1 | `C2=unmet literal_r94=1 checks_failed=literal` rc 1, exit 0 | yes | scanner DOES follow symlinks: caught (no gap) |
| 13 | orphan-ref commit with `/home/vgpnk/x` (2cf21876, then ref deleted) | — | predicate never evaluates it (predicates take `rev` as input); out of scope by contract | yes | host path outside the operated revision |

**Rows 1–6:** all miss the frozen scan, and all are non-host forms for this host (deliberate
regex-class probes, not real host paths).
**Misses that ARE host paths:** #7 (.json/.md), #9 (.env), #10 (`.PY` case), #11 (split literals,
undetectable by any byte regex). #9 and #10 are new negative findings beyond the contract's named
limits (which list only `~user`, `/Users/`, `C:\Users`, `$HOME`).

## 2. Sensitivity control (prove the scan sees planted bytes at all)

Scratch-only copy of the frozen counter with `HOST = re.compile(rb"/home")` (prefix-only):

    $ python3 -I $S/bin/count.py 08fd1c67 --repo $S/clone --report
    C2_REPORT lit=3 files=4   # /home/VGPNK caught (rows 1−2 shift 2→3)
    $ python3 -I $S/bin/count.py e7e8fcf2 ... --report
    C2_REPORT lit=2 files=4   # ~vgpnk still invisible (expected)
    $ python3 -I $S/bin/count.py 6b65e7c1 --report --scan .ufo/waves/round-94
    C2_REPORT literal=2 files=3  # residual = count-c2v2.py's own docstring + regex (see §0)
    $ python3 -I $S/bin/count.py 6b65e7c1 --report --scan .ufo/waves/round-93
    C2_REPORT literal=9 files=5  # catches all six legit /home/vgpnk literals + count-c2v2 docstring internals

## 3. HOME isolation (C1 side)

    $ env -i PATH=… HOME=/nonexistent SHOKUNIN_ROOT=<fleet> TMPDIR=$S/tmpdirlit \
        python3 -I count-c1v2.py 6b65e7c1 --repo $S/clone
    C1=met trio=98 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok rev=6b65e7c11f31 rc=0
    $ env -u HOME -i PATH=… SHOKUNIN_ROOT=<fleet> TMPDIR=$S/tmpdirlit \
        python3 -I count-c1v2.py 6b65e7c1 --repo $S/clone
    C1=met trio=98 files=19 adm_ok=19 adm_fail=0 … rev=6b65e7c11f31 rc=0
    # planted $HOME/.gitconfig ([safe] directory = $S/clone):
    $ env -i PATH=… HOME=$S/home-fake …
    C1=met trio=98 … adm_ok=19 adm_fail=0 … rc=0        # verdict unchanged
    # no-SHOKUNIN_ROOT fails closed (predicate env_unset):
    $ env -u HOME -i PATH=… TMPDIR=$S/tmpdirlit python3 -I count-c1v2.py 6b65e7c1 --repo $S/clone
    C1_SETUP census path unset: give --census or set SHOKUNIN_ROOT   rc=2
    # TMPDIR unset entirely: still runs
    $ env -i PATH=… HOME=/nonexistent SHOKUNIN_ROOT=<fleet> count-c1v2.py …
    C1=met … rc=0    (and count-c2v2.py full: C2=met rc=0)
    # XDG_CONFIG_HOME=GIT_CONFIG_GLOBAL deny-config probes:
    $ env -i … HOME=$S/home-xdg XDG_CONFIG_HOME=$S/home-xdg/.config …
    C1=met … rc=0
    $ env -i … HOME=$S/home-deny GIT_CONFIG_GLOBAL=$S/home-deny/.gitconfig …
    C1=met … rc=0

Verdict: stable under HOME=/nonexistent, HOME unset, planted `$HOME/.gitconfig`, XDG override,
and `GIT_CONFIG_GLOBAL`. Hidden dependencies found and eliminated by design: no git network
transport (counters call only local `git -C repo` reads: log, diff, rev-parse), no config fallback
(no `safe.directory` requirement because the `--repo` target is a scratch clone owned by the
invoking user), no `~` expansion (TMPDIR honoured explicitly, default falls to `tempfile` default
under `TMPDIR`/`/tmp`). Deny-config probe confirms the harness DOES honor planted configs in
general (fatal: transport 'file' not allowed under the same env), so their benign behavior here is
a property of the counter's call pattern, not of the config being ignored.

## 4. Named limits re-affirmed by experiment

- Split-literal (#11) is invisible to any byte regex; the counter's named limit on `$HOME`
  expansion attacks covers concatenation only in the source shape, not at runtime.
- Symlink following: my #12 shows the counter DOES catch host paths carried into the scan through
  a `.py`-named symlink — a widening behavior to keep in mind if suffix gating is ever loosened
  further. (Observation, not a defect in the frozen round-94.)
- Sources-census scan of the sworn fixture residue is out of scope (contract pins it to the
  `.ufo/waves/round-93` diagnostic; verified unchanged, `literal=9 files=5` aux run).

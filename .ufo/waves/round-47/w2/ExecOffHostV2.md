# Seat ExecOffHostV2 — off-path replay at T (portability probe)

Wave w2, round 47. Leaf seat; no subagent dispatch. Attacked item: the two claimed
instruments replayed off-path in a fresh clone at T, and their portability
(no hardcoded host paths). No C1/C2 scoring beyond the assigned commands (C1 predicate
handling is peer-owned).

## Verdict

**holds** — both instruments replay green from an off-path clone checked out at T, and
neither tool references `/home/vgpnk` (or any `/home/` path, or the username `vgpnk`)
anywhere in its source. Byte-identical at T vs freeze for `count-c2.py`; `mori-pin-check.py`
at T is the v2 hardening (differs from the frozen v1 bytes), consistent with the claim
narrative.

## Evidence (command + output + exit code)

Environment: `python3 3.14.8` (`/usr/bin/python3`), `git 2.56.0`. All runs used
`TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecOffHostV2/…`
(never `/tmp`).

### 1. Clone at T

```
$ git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin \
    /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecOffHostV2/clone
Cloning into '.../clone'... done.
$ git -C <clone> rev-parse --show-toplevel
/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecOffHostV2/clone
$ git -C <clone> rev-parse HEAD
68d66ca53d89be5c34a62f46af7c37449d9f9b63   # = landed tip T, branch master
```

Top-level verified equal to clone path; clone HEAD equals T.

### 2. `python3 tools/mori-pin-check.py --selftest` (tracked v2 tool), in clone

All 34 cases PASS; exit 0. Tail:

```
PASS cli_met_rc0  rc=0
PASS cli_bad_rev_rc2  rc=2
PIN_CHECK_SELFTEST pass=34 fail=0
```

`TMPDIR` subdir empty after the run (no scratch leftovers). Note: the selftest tally is
`pass=34` (v2 tool); the P-C1 self-test cell pins are scored against the FROZEN v1 bytes,
so this tally is not itself a C1 tally. The v2 selftest also runs clean from a non-repo
cwd (`cd .scratch/r47w2-ExecOffHostV2`, tool invoked by absolute path): 34/34 PASS,
exit 0 — selftest is cwd-independent.

### 3. `python3 .ufo/waves/round-47/count-c2.py T --repo <clone>`, in clone

```
C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=68d66ca53d89be5c34a62f46af7c37449d9f9b63
EXIT=0
```

Matches the contract target for C2 (`C2=met events=8 rows=8 …`). `TMPDIR` subdir empty
after the run.

### 4. Grep for host paths

Pattern `/home/vgpnk` → no matches; pattern `vgpnk` → no matches; pattern `/home/` →
no matches. Both in `clone/tools/mori-pin-check.py` and `clone/.ufo/waves/round-47/count-c2.py`.

### 5. Instrument hashes (T vs freeze F=63eecf27…)

| tool | sha256 at T (clone) | sha256 at F (`git show F:path`) |
|---|---|---|
| `tools/mori-pin-check.py` | `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6` | `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1` (frozen v1) |
| `.ufo/waves/round-47/count-c2.py` | `fc77b93338b3f49b9038eaac3832537b1be2e0ff9dff2476fef750153978901e` | `fc77b93338b3f49b9038eaac3832537b1be2e0ff9dff2476fef750153978901e` (identical) |

`git diff --stat F T -- <two tools>`: `tools/mori-pin-check.py` only — `+186 / −37`
(v1→v2 hardening); `count-c2.py` unchanged between F and T.

### 6. Clone tree cleanliness after all runs

`git -C <clone> status --porcelain` → empty (exit 0): neither tool polluted the working
tree; all scratch stayed under the seat's `.scratch/r47w2-ExecOffHostV2/`.

## Risks / UNVERIFIED

- **UNVERIFIED**: true cross-host / cross-user portability cannot be exercised from this
  seat (no other machine or user available). Evidence is limited to: no host-absolute
  paths, no username string, in either tool source; both tools run clean in a clone at a
  different absolute path and from a non-repo cwd under redirected `TMPDIR`; `count-c2.py`
  takes `--repo` explicitly, so its repo access is location-independent.
- The two runs above are operational replays, not C1/C2 scoring: P-C1's predicate is scored
  with the frozen v1 bytes by the peer seat; this seat did not re-score it.
- No tools were installed; nothing to record under tooling authorization.

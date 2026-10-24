# ExecReadmeRows — source-drift README rows resolve at e57c58b

Item attacked: the two new `source-drift` coverage rows added by the scored tip — the coverage-map
row for `knowledge/source-drift-hardening-r37.md` and the round-37 coverage-addition row — plus the
adjacent r36 source-drift rows whose paths they reuse. Every backticked path must exist at
`e57c58b57c025364e79d130fbdf764d2674d83d6`, and the cited live receipt must contain the row's
summary sentence.

## Axes

1. Path existence at the scored tip (git object level, not the mutable worktree).
2. Receipt↔prose binding: the quoted `MORI_SOURCE_DRIFT` summary line must be byte-present in the
   receipt the row describes.
3. Citation honesty: commit short-shas and SOURCES ids the rows name must resolve.

## Rows under test (README at the scored tip)

`git -C /home/vgpnk/Projects/shokunin/mori-shokunin show e57c58b57c025364e79d130fbdf764d2674d83d6:corpus/README.md`

- `:46` coverage-map row — ``knowledge/source-drift-hardening-r37.md``, ``tools/mori-source-drift.py``, ``.ufo/waves/round-37/count-c2.py``
- `:589` "Round-37 coverage additions" row — ``8ff9bba``, ``knowledge/source-drift-hardening-r37.md``, ``tools/mori-source-drift.py``, ``--selftest``, ``.ufo/waves/round-37/count-c2.py``, ``python3 .ufo/waves/round-37/count-c2.py <tip>``, ``huge_cap``, ``redirect_private_refused``, ``C2=met``, the quoted summary line, ``unavailable``
- Reused by the same table family and checked too: `:45` (r36 coverage row), `:567-575` (r36 register row).

The coverage map lives in `corpus/README.md`, so its `knowledge/...` entries are corpus-relative;
`:574` in the same file spells the same target as `corpus/knowledge/source-drift-r36.md`, which fixes
the base. Every `knowledge/...` entry was therefore resolved against `corpus/` as well as the repo root.

## Path -> exists (at e57c58b)

Existence test: `git -C <lane> cat-file -e e57c58b57c025364e79d130fbdf764d2674d83d6:<path>`
(rc 0 = exists). Directory test: `git ls-tree -r --name-only <tip> corpus/evidence/sources-r37/`.

| cited path | row(s) | resolved object at tip | exists |
|---|---|---|---|
| `knowledge/source-drift-hardening-r37.md` | :46, :589 | `corpus/knowledge/source-drift-hardening-r37.md` | yes |
| `knowledge/source-drift-r36.md` | :45, :567 | `corpus/knowledge/source-drift-r36.md` | yes |
| `tools/mori-source-drift.py` | :45, :46, :567, :589 | `tools/mori-source-drift.py` | yes |
| `.ufo/waves/round-37/count-c2.py` | :46, :589 (also as the command's script path) | `.ufo/waves/round-37/count-c2.py` | yes |
| `.ufo/waves/round-36/evidence/drift-live-r36.txt` | :45, :569 | same | yes |
| `corpus/SOURCES.md` | :567 | same | yes |
| `SKILL.md` | :567 | repo-root `SKILL.md` (only `SKILL.md` in the tree) | yes |
| `corpus/evidence/sources-r<N>/<id>.<ext>` | :567 (template placeholder) | concrete dir `corpus/evidence/sources-r37/` = S221.src, S222.src, S223.src, S224.src | yes (dir) |

Non-path backticked tokens in these rows are values, not files: `drifted`/`fresh`/`excerpt`/
`unavailable`/`no-copy` (state names), `sources-r<N>` / `<id>.<ext>` (template grammar), `--selftest`
(flag), `huge_cap` / `redirect_private_refused` (selftest arm names), `C2=met` (verdict token), and
`python3 tools/mori-source-drift.py --root .` / `python3 .ufo/waves/round-37/count-c2.py <tip>`
(command lines whose script paths were checked above).

Working-tree cross-check (`for p in ...; do [ -e "$p" ]`): all eight cited objects plus
`corpus/evidence/sources-r37` report `EXISTS`. README is byte-unchanged between the scored tip and the
current lane HEAD: `git diff --stat e57c58b… HEAD -- corpus/README.md` → empty; `git merge-base
--is-ancestor e57c58b… HEAD` → true.

## Cited receipt carries the summary sentence

Row `:589` quotes: `MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162`
and says the live run exited 1.

```
git show e57c58b…:.ufo/waves/round-37/evidence/drift-live-r37.txt | grep -n 'MORI_SOURCE_DRIFT rows=220'
221:MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162
git show e57c58b…:.ufo/waves/round-37/evidence/drift-live-r37.txt | grep -c '^EXIT=1$'
1
```

Byte comparison of the README quote against the receipt line:

```
sed -n '589p' corpus/README.md | grep -o 'MORI_SOURCE_DRIFT rows=220[^`]*' > /tmp/rm_sent.txt
git show e57c58b…:.ufo/waves/round-37/evidence/drift-live-r37.txt | grep 'MORI_SOURCE_DRIFT rows=220' > /tmp/rc_sent.txt
diff /tmp/rm_sent.txt /tmp/rc_sent.txt   ->  BYTE-IDENTICAL
```

The receipt is the 222-line per-row classification (S001…S220) plus that aggregate line and `EXIT=1`;
the tail rows agree with the quoted nine-drifted outcome class. The receipt is cited by the row's
live-run clause and by `drift-live-r37.txt` in the round-37 evidence set; it exists at the tip.

## Citation honesty (commits and SOURCES ids)

```
git rev-parse --verify bf0df77^{commit}  -> bf0df77fee4b6ef54a90aea09335c7617f125151   (r36 selftest PASS 4 cases, :575)
git rev-parse --verify 8ff9bba^{commit}  -> 8ff9bba1574fcaa41714036e8f1c9c0c248f237b   (r36 hardening landing, :589)
```

`git show <tip>:corpus/SOURCES.md | grep -nE '^\| *S22[1-5]'` returns rows at `:227`–`:231`
(S221 RFC 9110 §15.4, S222 OWASP SSRF, S223 Python urllib.request, S224 Yama LSM, S225 Fetch
Standard §4.5) — so the `S221–S225` citation in `:46` names five real registry rows.

## Risks / non-defects observed

- `S221–S225` is a SOURCES-id range, not a copy claim: `corpus/evidence/sources-r37/` holds
  S221–S224 only; S225 has a registry row (`corpus/SOURCES.md:231`) and no committed copy, i.e. the
  probe's `no-copy` state. The coverage row's "Sources" column cites registry rows, and the note
  (`corpus/knowledge/source-drift-hardening-r37.md:3-6,12`) cites S225 as a normative reference, so
  the absent copy is not a broken path. Recorded, not scored.
- The coverage map's `knowledge/...` entries are corpus-relative; a root-relative reading of those
  two entries fails (`git cat-file -e <tip>:knowledge/...` → missing). Same convention as every
  pre-existing coverage-map row (`:574` proves the base), so this is the table's established form,
  not a new inconsistency.
- My assignment did not include re-running `count-c2.py` or `--selftest`; only citation resolution
  was measured. No tools installed or upgraded; no lane file modified (only this report written).

VERDICT: PASS

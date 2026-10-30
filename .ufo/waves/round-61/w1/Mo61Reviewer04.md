# Mo61Reviewer04 — C1 hostile-registry audit

Axes: contract fidelity, rejection accuracy, diagnostic honesty, read-only containment.

## Findings by severity

**Low — `noowner` is permanently zero, including an owner rejection.** At frozen revision `7370a731abcafc4c803111de7c22cd6264d63be1`, `.ufo/waves/round-61/count-c1.py:74-75` initializes `noowner=0`, `:104-108` rejects the stripped-empty owner through `thin`, and `:123-128` prints the unchanged counter. Observed owner probe: `thin=1 noowner=0 failed=thin:.ufo/waves/round-57/verify-c2-source.py:owner`, exit 1. This is a diagnostic defect, **not** an acceptance bypass: the frozen owner kill rule is enforced. No counter/contract amendment proposed.

**No acceptance defect demonstrated by the three requested cases.**

| Variant | Result | Classification |
|---|---|---|
| Self-test cell names `python3 .ufo/waves/round-57/verify-c2-source.py --selftest`, although that tool has no such mode | met, exit 0 | Named scope boundary: contract requires a cell *naming* a `--selftest` command, not successful execution/support |
| Owner contains only space/tab whitespace | unmet, exit 1, `thin=1` | Caught |
| Same target has live row, superseded row, second live row in that order | unmet, exit 1, `dup=1` | Caught; superseded marker does not reset duplicate counting |

Path pointers above and below are relative to `/home/vgpnk/Projects/shokunin/mori-shokunin` and refer to the frozen revision, not a moving worktree. Frozen contract `.ufo/waves/round-61/contract.md:34-48` defines the lexical self-test requirement and owner/duplicate kill rules. Counter `:50-53` strips cells; `:96-102` filters all matching rows then counts live rows; `:109-112` only searches for `--selftest`; `:113-117` resolves the entry without executing it. The entire 19-line `.ufo/waves/round-57/verify-c2-source.py` has no option parser: `:4` unpacks two positional arguments directly. Thus the fabricated self-test command is not evidence of tool capability.

## Exact receipts and method

Disk guard command:

```text
bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
/fast/scratch/hyaku 57% 347.4G free
```

The guard printed filesystem status but timed out after 30 seconds while listing consumers. No heavy work followed; one lightweight shared no-checkout clone was used. No install/update occurred.

Read-only diff reviewed:

```text
git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 325f7e639916fcbc77fa2ec7475951a1b86bb1cb 7370a731abcafc4c803111de7c22cd6264d63be1 -- .ufo/waves/round-61/count-c1.py .ufo/waves/round-61/gate-manifest.json
```

Scratch clone command:

```text
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r61/Mo61Reviewer04/clone
git -C /fast/scratch/hyaku/mori-r61/Mo61Reviewer04/clone rev-parse --show-toplevel
/fast/scratch/hyaku/mori-r61/Mo61Reviewer04/clone
```

**Important method limitation:** the seat also prohibits commits/VCS mutation. Consequently these were in-memory SKILL read overlays against the scratch clone, not three committed hostile Git trees. The frozen counter bytes were loaded with `git -C CLONE show FREEZE:.ufo/waves/round-61/count-c1.py`, SHA-256 `a6684e697583746e8b6318d6984f3ada5e619c45a0a3449ecf46d79193433e00`. Only its `cat(..., 'SKILL.md')` return value was overlaid. Its `main()` argument parsing, frozen manifest reads, real target-blob reads through Git, `measure`, formatting, and exit path ran unchanged. This does not establish an unmodified standalone CLI run over committed variants.

Reproduction core (Python; `clone`, `scratch`, `rev` are the absolute clone/scratch paths above and the frozen revision):

```python
import subprocess, json, sys, io, contextlib

def show(p):
    return subprocess.run(['git', '-C', clone, 'show', rev+':'+p],
                          check=True, capture_output=True).stdout
m = {'__name__': 'probe_c1'}
exec(compile(show('.ufo/waves/round-61/count-c1.py'),
             clone+'/.ufo/waves/round-61/count-c1.py', 'exec'), m)
paths = [r['path'] for r in json.loads(show(m['MANIFEST_DEFAULT']))]
rows = [f'| gate-{i} | gate | `{p}` | 0 met / 1 unmet | '
        f'`python3 {p} --selftest` | frozen | read-only | MoriR61 |'
        for i, p in enumerate(paths)]
i = paths.index('.ufo/waves/round-57/verify-c2-source.py')
variants = {'lying-selftest': rows.copy(),
            'whitespace-owner': rows.copy(),
            'separated-live-duplicate': rows.copy()}
variants['whitespace-owner'][i] = rows[i].replace('| MoriR61 |', '| \t   |')
sup = rows[i].replace(f'gate-{i}', 'superseded-old').replace(
    '| read-only |', '| superseded: next row |')
variants['separated-live-duplicate'][i:i+1] = [
    rows[i], sup, rows[i].replace(f'gate-{i}', 'second-live')]
real_cat = m['cat']
for name, rs in variants.items():
    skill = m['table'](*rs).encode()
    m['cat'] = lambda repo, r, p, b=skill: (
        b if p == 'SKILL.md' else real_cat(repo, r, p))
    sys.argv = ['count-c1.py', rev, '--repo', clone, '--scratch', scratch]
    try:
        m['main']()
    except SystemExit as e:
        print(name, 'rc='+str(e.code))
m['cat'] = real_cat
```

All runs set TMPDIR to `/fast/scratch/hyaku/mori-r61/Mo61Reviewer04` and supplied that absolute path as `--scratch`. Twenty-five manifest paths were used, with 25 synthetic rows except the duplicate case's 27. Overlay SHA-256 values, in case order: `5f43b2f21f701f2355c7bf3513f301fa7d40cb73a7e52f5a23aaaf4f0bc7c224`, `7a71672c54c5914b96bfb2176509f64f0f04b08e4c30ee2f90093896ffb5d2ad`, `b4eb3fdde0a172690c85e26a7e304c4d11d7b240a9bb1c8fa41156077ff836cb`.

```text
lying-selftest:
C1=met gates=25 registered=25 missing=0 thin=0 dup=0 unres=0 noselftest=0 noowner=0 failed=none rev=7370a731abcafc4c803111de7c22cd6264d63be1
rc=0

whitespace-owner:
C1=unmet gates=25 registered=24 missing=0 thin=1 dup=0 unres=0 noselftest=0 noowner=0 failed=thin:.ufo/waves/round-57/verify-c2-source.py:owner rev=7370a731abcafc4c803111de7c22cd6264d63be1
rc=1

separated-live-duplicate:
C1=unmet gates=25 registered=24 missing=0 thin=0 dup=1 unres=0 noselftest=0 noowner=0 failed=dup:.ufo/waves/round-57/verify-c2-source.py rev=7370a731abcafc4c803111de7c22cd6264d63be1
rc=1
```

## Residual risk and verification gaps

- LSP unavailable: `read xd://lsp` returned `No such tool`. No references/definition/diagnostics server could be consulted. Static statements above come from frozen source inspection and the observed overlays, not semantic-server proof.
- Committed hostile-tree execution was not performed because the seat disallows commits/VCS mutation. No changed production registry, live after-state or end-to-end standalone tree result is claimed.
- All other gate metadata in these fixtures is synthetic, including pinned-value text; this probe does not validate its truth. Self-test support/execution is outside C1's frozen predicate.
- No canonical-runtime/rerouting/resume/saturation claims are affected by this scoped C1 parser review. No remediation, admission judgment, commits, registry updates, production writes, or sibling/fleet writes were performed.
- Scratch clone and scratch contents are removed before handoff; the receipts above are the retained evidence.

Self-evaluation: accuracy 4/5 and completeness 4/5 (in-memory overlays, not committed-tree CLI proofs); clarity 4/5 (method limitation explicitly separated); actionability 4/5 (exact frozen pointers and reproduction core); conciseness 4/5 (reproduction retained for auditability). Overall 4.0/5. Highest-impact remaining verification requires explicit permission for scratch fixture Git mutations; no amendment to the frozen counter is requested.

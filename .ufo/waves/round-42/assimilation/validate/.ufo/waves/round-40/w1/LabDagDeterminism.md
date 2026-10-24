# LabDagDeterminism — five-run DAG P probe

## Result

Axes: fixture determinism; merge-index isolation; byte-level registry reproducibility.

The hypothesis that `dag-p` is nondeterministic because conflicted index state can leak is **rejected for this probe**. Five sequential builds in distinct temporary repositories under lane `.scratch/` produced the same full named SHAs and a byte-identical final `corpus/SOURCES.md` body. After each build, `git status --porcelain` and `git ls-files --unmerged` were empty. The five temporary repositories were removed by the probe's `finally` cleanup.

## Exact invocation

No shell command was run. The exact tool invocation was `functions.eval(language="py", title="Probing DAG P determinism", timeout=300, reset=false)` with this Python cell:

```python
import hashlib, importlib.util, json, os, shutil, subprocess, tempfile
lane = "/home/vgpnk/Projects/shokunin/mori-shokunin"
gate_path = os.path.join(lane, "tools/mori-sources-appendonly.py")
spec = importlib.util.spec_from_file_location("mori_gate_probe", gate_path)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
env = gate._selftest_env()
cases, bodies = gate._selftest_dag_cases()
case = next(case for case in cases if case[1] == "dag-p")
print("fixture:", case[0], "kind=dag-p")
root = os.path.join(lane, ".scratch")
results = []
try:
    for n in range(1, 6):
        repo = tempfile.mkdtemp(prefix=f"lab-dag-p-{n}-", dir=root)
        shas = gate._make_dag_repo(repo, "dag-p", bodies, env)
        final = shas["m"]
        body = subprocess.run(["git", "-C", repo, "show", f"{final}:corpus/SOURCES.md"], check=True, capture_output=True, env=env).stdout
        status = subprocess.run(["git", "-C", repo, "status", "--porcelain"], check=True, capture_output=True, env=env).stdout
        unmerged = subprocess.run(["git", "-C", repo, "ls-files", "--unmerged"], check=True, capture_output=True, env=env).stdout
        results.append({"repo": repo, "shas": shas, "body": body, "status": status, "unmerged": unmerged})
        print(f"run {n}: " + " ".join(f"{name}={sha}" for name, sha in shas.items()))
        print(f"run {n}: registry_sha256={hashlib.sha256(body).hexdigest()} bytes={len(body)} status={status!r} unmerged={unmerged!r}")
    print("registry body (run 1):")
    print(results[0]["body"].decode("utf-8"), end="")
    for n, result in enumerate(results[1:], 2):
        print(f"compare run 1 vs {n}: named_shas={'identical' if result['shas'] == results[0]['shas'] else 'DIFFERENT'} registry_body={'byte-identical' if result['body'] == results[0]['body'] else 'DIFFERENT'}")
    print("aggregate:", "ACCEPT" if all(x["shas"] == results[0]["shas"] and x["body"] == results[0]["body"] and not x["status"] and not x["unmerged"] for x in results[1:]) and not results[0]["status"] and not results[0]["unmerged"] else "REJECT")
finally:
    for result in results:
        shutil.rmtree(result["repo"], ignore_errors=True)
```

## Exact output

```text
fixture: first-parent-lacks-path merge contributes no edits kind=dag-p
run 1: b0=07be6c7f176584f32d5091ad9f911bec7b6e135e s1=ea0be2d40f6b2cf0ba27181e0a445a54d6c8f9f5 d1=cdd8967013e2ce0ae406805f1f56552feb8dda04 m=5b672415948fd1cd7df763bd6ae142ba9388e693
run 1: registry_sha256=da3dec30fed6b7358e2738dfd339acb448186bb3a076509f1f627465373acffd bytes=575 status=b'' unmerged=b''
run 2: b0=07be6c7f176584f32d5091ad9f911bec7b6e135e s1=ea0be2d40f6b2cf0ba27181e0a445a54d6c8f9f5 d1=cdd8967013e2ce0ae406805f1f56552feb8dda04 m=5b672415948fd1cd7df763bd6ae142ba9388e693
run 2: registry_sha256=da3dec30fed6b7358e2738dfd339acb448186bb3a076509f1f627465373acffd bytes=575 status=b'' unmerged=b''
run 3: b0=07be6c7f176584f32d5091ad9f911bec7b6e135e s1=ea0be2d40f6b2cf0ba27181e0a445a54d6c8f9f5 d1=cdd8967013e2ce0ae406805f1f56552feb8dda04 m=5b672415948fd1cd7df763bd6ae142ba9388e693
run 3: registry_sha256=da3dec30fed6b7358e2738dfd339acb448186bb3a076509f1f627465373acffd bytes=575 status=b'' unmerged=b''
run 4: b0=07be6c7f176584f32d5091ad9f911bec7b6e135e s1=ea0be2d40f6b2cf0ba27181e0a445a54d6c8f9f5 d1=cdd8967013e2ce0ae406805f1f56552feb8dda04 m=5b672415948fd1cd7df763bd6ae142ba9388e693
run 4: registry_sha256=da3dec30fed6b7358e2738dfd339acb448186bb3a076509f1f627465373acffd bytes=575 status=b'' unmerged=b''
run 5: b0=07be6c7f176584f32d5091ad9f911bec7b6e135e s1=ea0be2d40f6b2cf0ba27181e0a445a54d6c8f9f5 d1=cdd8967013e2ce0ae406805f1f56552feb8dda04 m=5b672415948fd1cd7df763bd6ae142ba9388e693
run 5: registry_sha256=da3dec30fed6b7358e2738dfd339acb448186bb3a076509f1f627465373acffd bytes=575 status=b'' unmerged=b''
registry body (run 1):
# SOURCES — selftest registry

## Registry

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S001 | https://example.invalid/a | docs | A | scope a | anchor a v3 | teaches a | mined | 2026-01-01 | on-release | n/a |
| S008 | https://example.invalid/e | docs | A | scope a | anchor e | teaches e | mined | 2026-01-01 | on-release | n/a |
| S002 | https://example.invalid/b | docs | A | scope a | anchor b | supersedes S001 — replacement | mined | 2026-01-01 | on-release | n/a |
compare run 1 vs 2: named_shas=identical registry_body=byte-identical
compare run 1 vs 3: named_shas=identical registry_body=byte-identical
compare run 1 vs 4: named_shas=identical registry_body=byte-identical
compare run 1 vs 5: named_shas=identical registry_body=byte-identical
aggregate: ACCEPT
```

`aggregate: ACCEPT` means the five-build equality and clean-index conditions all held; it does not accept the nondeterminism hypothesis.

## Files, risks, blockers

- Changed file: `.ufo/waves/round-40/w1/LabDagDeterminism.md` (this report only). No production files, lane Git index/state, fleet files, or sibling lanes were changed. No tools were installed.
- Retained evidence: this report includes the full run output and final registry body; temporary repositories were removed.
- Risk: this rejects the hypothesis for five repeated builds in the current local environment only; it does not establish cross-host or cross-Git-version determinism.
- Blockers: none for the assigned probe. No LSP tool is exposed in the available tool inventory; LSP was not needed for this runtime probe.

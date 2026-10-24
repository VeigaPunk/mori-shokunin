measured 2026-10-23T08:52:01Z

# Round 24 capabilities register findings

## Draft rows

```DRAFT SCORECARD.md
ROW: | rounds[443].capabilities_added[0] | One-shot system pressure read | Reads CPU, memory, IO and IRQ pressure in one shot; unavailable is never zero, system CPU full is undefined and IRQ some is null; frozen selftest PASS 12/12, six survivors disclosed. | `tools/mori-pressure.py` | 24 |
```
Why this path: the closure reports this exact tool running its frozen selftest at 12/12, directly tying the implementation path to a recorded run (`.ufo/reports/round-24/mori.md:78`).
Citations: `MANIFEST.json@37b51a243302e8009c7067431e8a47f9a722fd14:12910`; `tools/mori-pressure.py:2-25`; `.ufo/reports/round-24/mori.md:78,1514-1521`; `corpus/lessons/round-24-verifier-spotcheck.md:70-88`.
VERDICT: supported

```DRAFT SCORECARD.md
ROW: | rounds[443].capabilities_added[1] | Round-23 routed-item check | Checks R1–R3 regression pins and R4 dispatch-before-call ordering over lane-written times; it held 4/4 after 3/4 before, with eight round-23 timing mismatches and zero of two in round 24. | `tools/mori-routed-check.py` | 24 |
```
Why this path: the closure reports this exact checker invocation holding all four items at round 24, directly tying the path to the recorded check (`.ufo/reports/round-24/mori.md:73-75`).
Citations: `MANIFEST.json@37b51a243302e8009c7067431e8a47f9a722fd14:12911`; `tools/mori-routed-check.py:14-25,572-677`; `.ufo/reports/round-24/mori.md:73-75`; `corpus/lessons/round-24-verifier-spotcheck.md:40-68`.
VERDICT: supported

## Gate and provenance checks

- Read the frozen fleet record with `git -C /home/vgpnk/Projects/shokunin show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json | jq -c '.rounds[443]'`: it identifies admitted mori round 24, lane commit `4f05dd5a32055e85a9297eb8fc8dfec7dfc4625e`, report `.ufo/reports/round-24/mori.md`, and the verifier spot-check at `28b79d3d1b76824f0c825aabe6cb6c5dc49961bf`.
- Located the two exact capability strings at frozen MANIFEST lines 12910–12911 with `git show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json`; both name the chosen `tools/` paths. The frozen report and spot-check blobs match their referenced revisions: report `f2a1a0ade98e841c751a41d91fbb2c468745c122`; spot-check `11414896d9d9a0c9fba431b4b3407e9e52c028cc`.
- Candidate-path rule: `git diff --name-status c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130 4f05dd5a32055e85a9297eb8fc8dfec7dfc4625e -- tools/mori-pressure.py tools/mori-routed-check.py` returned `A` for each path. `git cat-file -e` at the previous closure returned exit 128 for both; both resolved at the round-24 closure and at lane tip `913df22e29f131ef9cb5de9dcb7e3e272256c5f0`. Thus both are strong named-path candidates: present at closure and tip, added since the previous closure, under `tools/`, and named in the closure record.
- Limits preserved: the pressure tally was evidence-verified rather than re-run by the verifier; the tool read cases while being built, and six mutants survived (`corpus/lessons/round-24-verifier-spotcheck.md:79-87`). Routed checking trusts lane-written times, covers two round-24 rows, and leaves separate-worktree and invocation-reporting unchecked (`corpus/lessons/round-24-verifier-spotcheck.md:65-68`).

## Scope and execution record

- Only this report was written: `.ufo/waves/round-35/w1/RowR24.md`. No product code, SCORECARD, MANIFEST, or verifier artifact was edited.
- Neither candidate tool nor `count-c1.py` was executed here; their run outcomes above are closure-record evidence, not this seat's execution. No install or update was performed.

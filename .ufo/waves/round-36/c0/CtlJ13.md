measured 2026-10-23T11:51:11Z
control J13 shape content-free
control_sha256 4e05a96c11d2df817d91506d2e55fed36a80a98f27c51bd759f355c7e76df20f
counter_sha256 302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb

Axes: shape fidelity, detector rejection, exact restoration, write containment.
Mutant: replace only the scratch probe's emit function with a count-only line; retain history comparison and exit decisions. The delivered control has identical mutant bytes. Source: .ufo/waves/round-36/c0/controls/J13.py:55-56,64-102.
Expected detector: reject the missing id lists. Contract: .ufo/waves/round-36/contract.md:62-77,93. Parser requires all four lists: .ufo/waves/round-36/count-c2.py:53-55,498-501.

Frozen hashes were checked with `timeout 120 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py` before scoring; both matched .ufo/waves/round-36/evidence/freeze.txt:3-4:
```text
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```

Containment: every detector ran with an unchanged counter in a read-only-root bubblewrap namespace. Bind mounts placed the counter's shared scratch and /tmp writes inside CtlJ13. Counter-generated repositories and its own clone were created only inside those mounts; no manual sandbox git writes were issued. No seed argument or counter runtime patch was used. All bounded invocations returned; no background jobs or services were started. No tools were installed or updated.
Actual scored command (cwd /home/vgpnk/Projects/shokunin/mori-shokunin; captured stdout and stderr together):
```sh
timeout 900 bwrap --die-with-parent --ro-bind / / --bind /fast/scratch/hyaku/mori-r36/CtlJ13 /fast/scratch/hyaku/mori-r36 --bind /fast/scratch/hyaku/mori-r36/CtlJ13/tmp /tmp --proc /proc --dev /dev --unshare-pid --unshare-net --setenv TMPDIR /tmp --setenv PYTHONDONTWRITEBYTECODE 1 -- timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J13.py
```
Full scored counter output:
```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J13.py
blind arm: 0/24 sandbox histories matched the hidden truth (2.1s; coverage: deletions=24 changed-back=16 superseded=7)
  repo00 FAIL: no summary line (exit 0): appendonly_violations=3
  repo01 FAIL: no summary line (exit 1): appendonly_violations=4
  repo02 FAIL: no summary line (exit 1): appendonly_violations=2
  repo03 FAIL: no summary line (exit 1): appendonly_violations=2
  repo04 FAIL: no summary line (exit 1): appendonly_violations=2
  repo05 FAIL: no summary line (exit 0): appendonly_violations=2
  repo06 FAIL: no summary line (exit 1): appendonly_violations=1
  repo07 FAIL: no summary line (exit 1): appendonly_violations=3
  repo08 FAIL: no summary line (exit 1): appendonly_violations=2
  repo09 FAIL: no summary line (exit 1): appendonly_violations=2
  repo10 FAIL: no summary line (exit 1): appendonly_violations=3
  repo11 FAIL: no summary line (exit 1): appendonly_violations=2
  repo12 FAIL: no summary line (exit 1): appendonly_violations=3
  repo13 FAIL: no summary line (exit 1): appendonly_violations=4
  repo14 FAIL: no summary line (exit 1): appendonly_violations=1
  repo15 FAIL: no summary line (exit 1): appendonly_violations=4
  repo16 FAIL: no summary line (exit 1): appendonly_violations=3
  repo17 FAIL: no summary line (exit 1): appendonly_violations=1
  repo18 FAIL: no summary line (exit 1): appendonly_violations=2
  repo19 FAIL: no summary line (exit 1): appendonly_violations=2
  repo20 FAIL: no summary line (exit 1): appendonly_violations=5
  repo21 FAIL: no summary line (exit 1): appendonly_violations=3
  repo22 FAIL: no summary line (exit 1): appendonly_violations=4
  repo23 FAIL: no summary line (exit 1): appendonly_violations=4
real arm: FAIL (2.3s)
  tool:   (no summary line)
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  diff: no summary line (exit 1)
  tool exit=1
C2=unmet
seed=13077733609025934134
exit_code=1
```

Mutation probe: the same bounded detector and namespace command above was run on pristine, mutated, and restored bytes. For pristine/restored the --tool path was /fast/scratch/hyaku/mori-r36/probe.py, mapping to host /fast/scratch/hyaku/mori-r36/CtlJ13/probe.py. Each run independently drew its seed; none used --seed.
Full pristine output:
```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /fast/scratch/hyaku/mori-r36/probe.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.3s; coverage: deletions=22 changed-back=13 superseded=8)
real arm: pass (2.0s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=15630246364454113717
exit_code=0
```
Full restored output:
```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /fast/scratch/hyaku/mori-r36/probe.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.0s; coverage: deletions=22 changed-back=16 superseded=9)
real arm: pass (1.9s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=14717419259722232947
exit_code=0
```
Restoration evidence, from `timeout 120 sha256sum` on the listed files before mutation, during mutation, and after restoration:
```text
pristine /fast/scratch/hyaku/mori-r36/CtlJ13/probe.py 2a1b25c4e2cc40fb31e86c6ca917ec2ecf62c8655be689277bf86ac196730a28
mutated /fast/scratch/hyaku/mori-r36/CtlJ13/probe.py 4e05a96c11d2df817d91506d2e55fed36a80a98f27c51bd759f355c7e76df20f
mutated /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J13.py 4e05a96c11d2df817d91506d2e55fed36a80a98f27c51bd759f355c7e76df20f
restored /fast/scratch/hyaku/mori-r36/CtlJ13/probe.py 2a1b25c4e2cc40fb31e86c6ca917ec2ecf62c8655be689277bf86ac196730a28
```
Final sha256sum also returned the original frozen C1 and C2 hashes shown above and the unchanged J13 mutant hash. The isolated probe was restored byte-for-byte; the requested defective lane control is intentionally retained.
Mutation verdict: killed (pristine met, mutant unmet, restored met). The counter rejected the content-free output in all 24 histories and the real arm; no contract change was made.
VERDICT: J13 unmet exit 1

# Round 37 C2 redirect-policy arm: mutation probe

**Item attacked:** C2's `redirect_kill` check and the `redirect_private_refused` selftest arm it
prices — i.e. whether "post-redirect public-destination policy" is load-bearing in both the tool and
the counter at e57c58b57c025364e79d130fbdf764d2674d83d6.
**Severity:** None found. **Exploit path:** None. **Smallest remediation:** None.

Scratch root (no lane file was written):
`/fast/scratch/hyaku/mori-r37/MutC2RedirectArm/`

## Mutants

Byte-identical pristine copies were taken from `git show e57c58b…:<path>` and from the clean
working tree; hashes match the tip.

| file | sha256 | mutation |
|---|---|---|
| `pristine-tool.py` | `453c5d8e260301df7a99daf62b4c16ea08e4a0b4f9e4f53821cdbce447011552` | none (tip bytes) |
| `tool-mutant.py` | `dd1a4a21f163a859550d02bd50b0c308a667002d311dc70456d2e1979fe8e32f` | line 158 `if not _public_redirect_target(final):` → `if False:  # round-37 mutation: policy removed` |
| `tool-vacuous-arm.py` | `b99405c0281125ab3c474c6760c99f349d7a5366038359a8aa108e00d3ac4269` | line 415 `outcome_redir == "unavailable"` → `True,  # round-37 blindness probe: arm forced vacuous` |
| `pristine-counter.py` | `71c72929f9ac4dc8af0c079fb91220413064cb043391bf495f5ce32cadc3a7c1` | none (tip bytes) |
| `counter-mutant.py` | `511f4601f3a9044ea920f12e1f34a176e1a3b3f5ae05e80d1e8efd6ce403d749` | `redirect_kill` check block deleted (incl. `redirect_kill` from the tool-absent fallback list) |

Mutation diffs (observed):

```text
--- pristine-tool.py
+++ tool-mutant.py
@@ -155,7 +155,7 @@
                 if final != url:
                     # a redirect actually happened: the new authority must be public
                     # (loopback/private targets are refused; w2/SentCensus)
-                    if not _public_redirect_target(final):
+                    if False:  # round-37 mutation: policy removed
                         return "unavailable", None
--- pristine-tool.py
+++ tool-vacuous-arm.py
@@ -412,7 +412,7 @@
             outcome_redir, _ = fetch(base + "/redir")
             checks.append((
                 "redirect_private_refused",
-                outcome_redir == "unavailable",
+                True,  # round-37 blindness probe: arm forced vacuous
                 "redirect_to_loopback=%s" % outcome_redir))
--- pristine-counter.py
+++ counter-mutant.py
@@ -170,16 +170,8 @@
             check("cap_kill", cap_rc == 1 and cap_lines.get("huge_cap") == "FAIL",
                   "exit=%s huge_cap=%s" % (cap_rc, cap_lines.get("huge_cap")))
 
-            redir = os.path.join(work, "redirect-mutant.py")
-            with open(redir, "w", encoding="utf-8") as handle:
-                handle.write(tool_text.replace(REDIRECT_ANCHOR, REDIRECT_MUTANT))
-            redir_rc, redir_lines, _ = selftest(redir)
-            check("redirect_kill",
-                  redir_rc == 1 and redir_lines.get("redirect_private_refused") == "FAIL",
-                  "exit=%s redirect_private_refused=%s"
-                  % (redir_rc, redir_lines.get("redirect_private_refused")))
         else:
-            for name in ("selftest", "cap_kill", "redirect_kill"):
+            for name in ("selftest", "cap_kill"):
                 check(name, False, "tool absent")
```

Three throwaway revs in a fresh scratch git repo (`/fast/scratch/hyaku/mori-r37/MutC2RedirectArm/repo`,
only the six paths the counter reads, byte-copied from e57c58b):

```text
P=c39fa8c9aadd24eb999cf4de7c8907933afbfa84   pristine at e57c58b
M=6ebf47dce901f430efbea28c0bbc054bc6b1a769   tool mutant: redirect policy removed
V=c330be948cf55e528e3b8a047ad8f1f6f3ecee9e   tool vacuous arm: redirect_private_refused forced PASS
```

## Direction 1 — tool side: the arm prices the policy

Command: `python3 pristine-tool.py --selftest` (restored/pristine bytes)

```text
selftest exit_code            PASS
selftest row_states           PASS
selftest summary              PASS
selftest huge_cap             PASS
selftest redirect_private_refused PASS
selftest missing_sources_exit2 PASS
MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)
EXIT=0        (real 0m4.566s)
```

Command: `python3 tool-mutant.py --selftest` (policy anchor removed)

```text
selftest exit_code            PASS
selftest row_states           FAIL (got=[… ('S110', 'fresh')] want=[… ('S110', 'unavailable')])
selftest summary              FAIL (summary=('10', '3', '1', '1', '3', '2'))
selftest huge_cap             PASS
selftest redirect_private_refused FAIL (redirect_to_loopback=body)
selftest missing_sources_exit2 PASS
MORI_SOURCE_DRIFT_SELFTEST: FAIL (3/6)
EXIT=1        (real 0m4.562s)
```

The named arm flips PASS → FAIL with the policy gone: `selftest redirect_private_refused FAIL`
(`redirect_to_loopback=body`). Load-bearing on the tool side.

## Direction 2 — counter side: the check prices the arm

All runs `python3 <counter> <rev> --repo /fast/scratch/hyaku/mori-r37/MutC2RedirectArm/repo`.

| # | counter | rev | observed verdict | exit |
|---|---|---|---|---|
| R0 | lane tip (in place) | e57c58b | `C2=met` — `selftest PASS`, `redirect_kill PASS (exit=1 redirect_private_refused=FAIL)` | 0 |
| R1 | pristine | P | `C2=met`, all 8 checks PASS | 0 |
| R2 | **mutant (redirect_kill dropped)** | P | `C2=met`; `redirect_kill` line absent, `cap_kill PASS`, `C2=met` | 0 |
| R3 | pristine | M (policy removed) | `C2=unmet`; `selftest FAIL (exit=1 … redirect_private_refused=FAIL, row_states=FAIL, summary=FAIL)` | 1 |
| R4 | mutant | M | `C2=unmet`; `selftest FAIL (… redirect_private_refused=FAIL …)` | 1 |
| R5 | pristine | V (vacuous arm) | `C2=unmet`; `selftest PASS (exit=0 arms=…redirect_private_refused=PASS…)` and `redirect_kill FAIL (exit=1 redirect_private_refused=PASS)` | 1 |
| R6 | **mutant** | V (vacuous arm) | **`C2=met`** — blind; `selftest PASS`, `cap_kill PASS`, no redirect check | 0 |

R0 output (scored tip, lane counter in place, read-only):

```text
check tool_present   PASS (path=tools/mori-source-drift.py)
check selftest       PASS (exit=0 arms=[('exit_code','PASS'),('huge_cap','PASS'),('missing_sources_exit2','PASS'),('redirect_private_refused','PASS'),('row_states','PASS'),('summary','PASS')])
check cap_kill       PASS (exit=1 huge_cap=FAIL)
check redirect_kill  PASS (exit=1 redirect_private_refused=FAIL)
check knowledge      PASS (present=True rows=['S205','S221','S222','S223','S224','S225'] cited_commit=True)
check capability     PASS (rows=1 names_tool=True)
check readme         PASS (r36_row=True r37_row=True)
check live           PASS (present=True sentence=True)
C2=met
EXIT=0        (real 0m13.933s)
```

R6 output (the blindness, i.e. the counter check removed):

```text
check tool_present   PASS (path=tools/mori-source-drift.py)
check selftest       PASS (exit=0 arms=[('exit_code','PASS'),('huge_cap','PASS'),('missing_sources_exit2','PASS'),('redirect_private_refused','PASS'),('row_states','PASS'),('summary','PASS')])
check cap_kill       PASS (exit=1 huge_cap=FAIL)
check knowledge      PASS (present=True rows=['S205','S221','S222','S223','S224','S225'] cited_commit=True)
check capability     PASS (rows=1 names_tool=True)
check readme         PASS (r36_row=True r37_row=True)
check live           PASS (present=True sentence=True)
C2=met
EXIT=0        (real 0m9.344s)
```

R5 output (same defective bytes, honest counter):

```text
check selftest       PASS (exit=0 … redirect_private_refused=PASS …)
check cap_kill       PASS (exit=1 huge_cap=FAIL)
check redirect_kill  FAIL (exit=1 redirect_private_refused=PASS)
C2=unmet
EXIT=1        (real 0m13.931s)
```

Counter-mutant at the honest tip (R2) also prints `C2=met`, matching the cap sibling's acceptance
shape; the drop is verdict-neutral on honest bytes and decisive on defective bytes.

## Both directions, stated as findings

1. **Tool direction:** removing `if not _public_redirect_target(final):` turns
   `selftest redirect_private_refused` PASS → FAIL (`redirect_to_loopback=body`); the arm is not
   vacuous and the policy is what it prices.
2. **Counter direction:** with `redirect_kill` dropped, a tool whose arm is forced to `True`
   (R6, rev V) is graded `C2=met`; the intact counter grades the same bytes `C2=unmet`
   (`redirect_kill FAIL (exit=1 redirect_private_refused=PASS)`, R5). The check is what distinguishes
   "the arm passes" from "the arm measures the policy".

**Coverage nuance (not a defect):** at rev M (policy removed, arm honest) R4 still reads `C2=unmet`,
because the counter's `selftest` check independently requires the committed arm to PASS. So
`redirect_kill` is load-bearing specifically against a self-vacuous arm (the failure mode where the
tool's own selftest can never detect its own vacuity), not as the sole detector of policy removal.
Both directions hold; the counter check earns its keep exactly where the tool cannot police itself.

## Restoration evidence

- Lane repo never written: `tools/mori-source-drift.py` = `453c5d8e…11552` and
  `.ufo/waves/round-37/count-c2.py` = `71c72929…7c1` before and after every run. No probe command
  names a lane path as a write target; all copies are under the scratch root.
- Lane `git status` at 17:13 shows other wave seats' concurrent edits to
  `.ufo/waves/round-37/evidence/*.txt` (a `command:` header line added at 17:13:41 by another seat);
  those are outside this probe's write set and were not produced by any command here.
- Scratch git repo restored to P (`git reset -q c39fa8c…`), `git status --porcelain` empty, log
  `c39fa8c pristine at e57c58b`.
- Restored-byte re-run: `python3 pristine-tool.py --selftest` → `MORI_SOURCE_DRIFT_SELFTEST: PASS
  (6 cases)`, `EXIT=0`.
- Mutants are separate files under the scratch root; no mutant bytes remain in the scratch repo.

## Tooling

No installs or upgrades were made.

VERDICT: PASS

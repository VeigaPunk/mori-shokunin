# SrcApprovalTests — C1 frontier source proposal (ApprovalTests approval/reporter flow)

STATUS: complete (proposal only; no corpus file edited, no SOURCES.md row written)

## Verdict

One SOURCES row is proposed for the frontier question "how does a reviewer decide on a changed result before approving a new golden/approved output?". The primary upstream document is the ApprovalTests Python port's README at commit `5d98f0c166ad2dde7ff60effb12427db8183805e`. It is reachable and its located quote is within the 25-word cap. Scope is the approval/reporter flow of the ApprovalTests library family as documented by the Python port's maintainers, not a general claim about reviewing test output.

## Proposed SOURCES row

Next unused id: `S066` (registry's last row is S065, observed in `corpus/SOURCES.md` line 71; `S066` is the next number).

```
| S066 | ApprovalTests.Python README — https://github.com/approvals/ApprovalTests.Python/blob/5d98f0c166ad2dde7ff60effb12427db8183805e/README.md | docs | A | golden-master approval flow in ApprovalTests: a changed result is examined in a reporter's diff before the master is updated (maintainer docs for the Python port, scope limited to this flow) | README.md lines 72-77 (Overview) and 149-151 (Reporters); commit 5d98f0c166ad2dde7ff60effb12427db8183805e (repo main HEAD at fetch, 2026-10-21); raw fetch SHA-256 db6b2f6a1aa542dbb262dc655c6c40d3703d7c04b89b44adcd6c3e1d3e30de0b | A changed result is a decision point: update the approved master only when the change is expected and good; otherwise fix the code so the result returns to the master. | queued | 2026-10-21 | 180d | — |
```

Column check: 11 cells between outer pipes, no `|` inside any cell. `status` is `queued` because no knowledge entry cites the row yet; `used-by` is `—` for the same reason. Promote to `mined` only when a `knowledge/` or lesson path cites S066.

## Gate item (for the round lesson)

- URL: https://github.com/approvals/ApprovalTests.Python/blob/5d98f0c166ad2dde7ff60effb12427db8183805e/README.md (HTTP 200 on 2026-10-21; raw content at the same SHA, identical bytes to the `master` raw path, SHA-256 `db6b2f6a1aa542dbb262dc655c6c40d3703d7c04b89b44adcd6c3e1d3e30de0b`).
- Access date: 2026-10-21.
- Located quote (≤25 words), README.md line 75 of the pinned file, in the Overview section ("Approvals work by comparing…", lines 72-77):
  > "Either you will update the master because you expected the changes and they are good"
  Word count: 15.
- Supporting located quote, lines 74-75 (same section):
  > "Whenever your current results differ from the golden master, Approvals will launch an external application for you to examine the differences."
  Word count: 21.
- Reporter-section quote, lines 150-151 (Reporters heading, line 149 onward):
  > "You can use this diff tool to change the approved to make the test pass the next time you run it."
  Word count: 20.

The quotes were copied verbatim from the pinned file; they were grepped against `/tmp/atapprovals.a3eM/py-readme-5d98f0c.md` (line numbers above are that file's numbering, which matches the commit bytes).

## Evidence trail (what was opened, when, and how)

| Step | Command / URL | Result |
|---|---|---|
| Home page | `read https://approvaltests.com/` (2026-10-21) | Reachable. Marketing and step-list page; the "Approve result so it continues to work" step is an image-only table row, so it was not quoted. |
| Resources page | `read https://approvaltests.com/resources/` | Reachable; links only, no approval-flow text. |
| Java README | `read https://github.com/approvals/ApprovalTests.Java` | Reachable via GitHub API; README covers the approved-file rename flow ("Simply rename this to … approved.txt") but no reviewer-decision sentence, so not used. |
| Node.js README | `read https://github.com/approvals/Approvals.NodeJS` | Reachable; the "You should be presented with a diff tool" step is not a decision criterion, so not used. |
| Python README (chosen) | `read https://github.com/approvals/approvaltests.Python` (API), raw `master` via curl, raw at `5d98f0c…` | Reachable; `master` raw bytes identical to `5d98f0c…` raw. |
| Documentation explanation | `curl` raw `approvals/ApprovalTests.Documentation/main/explanations/what_are_approvals.md`; blob `e10f29b0c021dd74e7eeabe56a1ea641b451ced2` returns HTTP 200 | Reachable; see the lead below. |
| Commit pins | `git ls-remote https://github.com/approvals/ApprovalTests.Python` and `…/ApprovalTests.Documentation` (read-only remote query) | Python `refs/heads/main` = `5d98f0c166ad2dde7ff60effb12427db8183805e`; no `refs/heads/master` is advertised, though the raw `master` URL serves the same bytes [INFERENCE: the raw host resolves `master` through a redirect or cache; not further verified]. Documentation `refs/heads/main` = `e10f29b0c021dd74e7eeabe56a1ea641b451ced2`. |
| GitHub commits API | `read https://api.github.com/repos/approvals/ApprovalTests.Python/commits/master` | HTTP 422 (unreachable through this endpoint; the ls-remote SHA was used instead). |

Installs/updates: none. `curl`, `git` and `sha256sum` were already present on the host. Temporary fetched copies are under `/tmp/atapprovals.a3eM/` (not part of any corpus).

## Secondary candidate (not proposed as a row)

- ApprovalTests.Documentation, `explanations/what_are_approvals.md`, pinned `e10f29b0c021dd74e7eeabe56a1ea641b451ced2`, line 31 (step 3 "Manage the 'approved' file"): "This is typically done by copying the received file to the approved file." (13 words). It covers received-to-approved mechanics and is a good second row if the L1 wants the received-file mechanics; it is left out to keep the proposal to one row as assigned. Lines 20-21 also say "If there's a difference, a reporter tool will highlight the mismatch and the test fails."

## Findings and limits

- The quotes support the claim that a changed result is reviewed in a diff, then either the master is updated (when the change is expected and good) or the code is changed to bring the result back to the master. They do not establish how often reviewers make the wrong call, nor any reproducibility benefit; those claims are outside the row's `teaches`.
- The row's tier is A for the stated scope only (the Python port's maintainer README on the approval/reporter flow). It is not a general testing-methodology source; a general claim would need the what-are-approvals explanation or a survey, which this seat did not open beyond the lead above.
- No quote has been invented. Every quote above was taken from a fetched file, and the cited line numbers were confirmed with grep on the saved copy.
- The `master` raw URL and the `refs/heads/main` SHA agree on bytes; the row's anchor uses the SHA, so it does not depend on which branch name the host resolves.
- Not run: no build, test, lint, or corpus census (`awk` census commands in `CORPUS.md`); the L1 can run the census after inserting the row. Expected after insertion: rows +1 (S066), `queued=` count +1, no new `NF!=13` lines, no duplicate ids.

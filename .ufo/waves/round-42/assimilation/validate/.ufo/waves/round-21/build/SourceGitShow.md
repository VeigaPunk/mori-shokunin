# Git-show source scope

## Finding

**Proposed source scope:** the official Git documentation supports the narrow capability claim that a caller can select a path in a named revision/tree-ish object and display the resulting blob's contents. The paired documentation is needed: `gitrevisions` defines the `<rev>:<path>` selector, while `git-show` states what it displays for a plain blob.

- `git-show` 2.56.0, last updated 2026-09-28, Description: “For plain blobs, it shows the plain contents.” Its `<object>` option names objects to show and links to the `gitrevisions` section for object-name spellings. Source: https://git-scm.com/docs/git-show (opened 2026-10-21).
- `gitrevisions` 2.56.0, last updated 2026-09-28, `<rev>:<path>` section: “A suffix `:` followed by a path names the blob or tree at the given path in the tree-ish object named by the part before the colon.” Examples include `HEAD:README` and `master:./README`. Source: https://git-scm.com/docs/gitrevisions (opened 2026-10-21).
- Existing local context: `corpus/SOURCES.md:70` (S064) distinguishes resolving a commit selector from separately binding actual loaded bytes to blobs at that commit. This proposed source scope complements that boundary; it does not replace it.

## Limits / unresolved

This supports **revision/path selection and blob-content display only**. It does not establish that the selected commit is authentic, approved, signed, remotely published, or otherwise trustworthy; nor does it prove the caller selected the intended revision/path or that extracted bytes equal any separately loaded input. Those require independent evidence. A tree selector is not a claim that the selected object is a file blob.

## Confidence

High for the documented Git selector and display behavior (paired official manuals); no authenticity or input-binding conclusion is made. No source registry or production file was edited.
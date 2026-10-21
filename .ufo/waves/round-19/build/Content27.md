{
  "schema": "mori-content-reviews-v1",
  "reviewer": "MoriR19Recovery.Content27",
  "revision": "b3602869dadd4016675aeba8db2adf3fa1e1b531",
  "rows": [
    {
      "path": ".ufo/waves/round-16/build/PackCursorShape.md",
      "blob_sha256": "d58ca32ad91829103e06008662c4282dead88483a47677a759db5301c6bb0e37",
      "decision": "retain",
      "content_basis": "content-reviewed",
      "reason": "Contains synthetic cursor-shape cases, stable journal identifiers, and bounded fixture counts; no private-value content observed.",
      "findings": []
    },
    {
      "path": ".ufo/waves/round-16/build/WindowHarness.md",
      "blob_sha256": "bbf4dd315529bb1c7e3b2fe8005b5b3b4ed18f4af71e40e1b45ec7574d2f63e0",
      "decision": "retain",
      "content_basis": "content-reviewed",
      "reason": "Describes harness behavior, input/output contracts, and run boundaries without host-specific values or private records.",
      "findings": []
    },
    {
      "path": ".ufo/waves/round-18/build/ScoutProvinceRegistry.md",
      "blob_sha256": "b2db17a1f45acc54731fddfa93dcb136eddca3ff7bc39f0a7ee8624ec7adfdc7",
      "decision": "retain",
      "content_basis": "content-reviewed",
      "reason": "Contains source-review findings and proposed registry entries with generic placeholders and scope boundaries; no private values observed.",
      "findings": []
    },
    {
      "path": ".ufo/waves/round-18/falsify/AttackTokPackageRefs.md",
      "blob_sha256": "c27d52fdd8498c8f5f0add42f3d190c12dc7ea1ac71a416e642803d03f60310a",
      "decision": "minimized",
      "content_basis": "content-reviewed",
      "reason": "Reports redaction scope using counts and categories but retains short-line digests tied to private-context lines; no underlying private values are reproduced.",
      "findings": [
        {"line": 10, "class": "short-line-private-context-digest"},
        {"line": 11, "class": "short-line-private-context-digest"}
      ]
    },
    {
      "path": ".ufo/waves/round-18/falsify/ResweepCorpusRoot.md",
      "blob_sha256": "6d63f64be9fb24aea7ec20b8c589753da5f4191c56d45fa9edc1498949f16155",
      "decision": "retain",
      "content_basis": "content-reviewed",
      "reason": "Records privacy categories, paths, counts, and full-blob provenance digests without reproducing private values; its findings are scoped and its aggregates are sanitized.",
      "findings": []
    }
  ]
}
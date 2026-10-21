{
  "schema": "mori-content-reviews-v1",
  "reviewer": "MoriR19Recovery.Content03",
  "revision": "b3602869dadd4016675aeba8db2adf3fa1e1b531",
  "rows": [
    {
      "path": ".ufo/waves/round-16/build/AttackMissingCursor.md",
      "blob_sha256": "9fca21dbb13c280ce9cfd00a7d422979accb4dfae35e2f935cab9de00602b531",
      "decision": "retain",
      "content_basis": "content-reviewed",
      "reason": "Public systemd source excerpts, generic API behavior, synthetic fixture summaries, and aggregate review metadata; no private source, identity, or configuration values remain.",
      "findings": []
    },
    {
      "path": ".ufo/waves/round-16/build/PackUnitSignal.md",
      "blob_sha256": "79568ad7c11a6df04e9517bb6b4a00cd8b24f40bb142bb8a2bf9d35efde9c986",
      "decision": "retain",
      "content_basis": "content-reviewed",
      "reason": "Synthetic unit-signal cases, fixed journal identifiers, predicate names, counts, and author-lane disclosure; no private source, identity, or configuration values remain.",
      "findings": []
    },
    {
      "path": ".ufo/waves/round-18/build/AdjR16AttackPermission.md",
      "blob_sha256": "59aeb225173540b21b2cbc757b873dc58879b7f2e15abec1e8499a7881bc9726",
      "decision": "unresolved",
      "content_basis": "content-reviewed",
      "reason": "An absolute host-home workspace path retains a host account identifier; the file also retains per-line digests associated with private-derived text, though not the source text itself.",
      "findings": [
        {"line": 13, "class": "short-line-digest"},
        {"line": 14, "class": "short-line-digest"},
        {"line": 27, "class": "host-account-path"}
      ]
    },
    {
      "path": ".ufo/waves/round-18/build/SrcSlsaProvenance.md",
      "blob_sha256": "63747f61db60c6d187603058a962e406098e32b0f016bded6dd3acf70ded9ec7",
      "decision": "retain",
      "content_basis": "content-reviewed",
      "reason": "Public specification excerpts and URLs, source-registry drafting metadata, and generic digest-binding analysis; no private source, identity, or configuration values remain.",
      "findings": []
    },
    {
      "path": ".ufo/waves/round-18/falsify/AuditMisrootsScratch.md",
      "blob_sha256": "067445aceabb5a87804eff7b3198a148ad4087aad3a5294f50d0c891c502b028",
      "decision": "unresolved",
      "content_basis": "content-reviewed",
      "reason": "Repeated absolute host-home workspace paths retain a host account identifier; the remaining details are repository-path, count, and status metadata rather than configuration contents.",
      "findings": [
        {"line": 7, "class": "host-account-path"},
        {"line": 20, "class": "host-account-path"},
        {"line": 23, "class": "host-account-path"}
      ]
    },
    {
      "path": ".ufo/waves/round-18/falsify/ReviewKnowMinimization.md",
      "blob_sha256": "c6ea1ae58866ad62fb89582a66ca307dddf3f589b28f78b67f42568ae201fa10",
      "decision": "unresolved",
      "content_basis": "content-reviewed",
      "reason": "The retained command transcripts contain repeated absolute host-home workspace paths with a host account identifier; no private source quotations or configuration values were observed.",
      "findings": [
        {"line": 68, "class": "host-account-path"},
        {"line": 69, "class": "host-account-path"},
        {"line": 70, "class": "host-account-path"},
        {"line": 71, "class": "host-account-path"},
        {"line": 72, "class": "host-account-path"},
        {"line": 73, "class": "host-account-path"}
      ]
    }
  ]
}

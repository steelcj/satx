**Judgment calls made, flagged rather than silently chosen:**

- Root holds **one** author folder (`sat`), not five — the cascade spec lists this as an unresolved conflict, but every worked example in both documents uses this shape, so I went with it.
- Extended the field-kinds example with DC's three missing elements (`source`, `relation`, `coverage`) since the shown table wasn't a complete DC 1.1 declaration.
- **Genuine spec disagreement:** satx-shape v0.0.7's tree puts message catalogs at `en/messages/`; sidecars v0.0.12 (newer, and the core document) rules they belong at `lib/locale/`. I built the organizing directory where satx-shape's tree puts it, left it empty, and wrote the conflict into its `.sat-boundary` note rather than resolving it myself.
- Left `dc:subject` unset on these 6 docs — accumulating-from-ancestor-works needs an index resource per node, which belongs to the `content/examples/` showcase HANDOVER describes, not to SAT's own docs archive.

**Not yet built**, per HANDOVER's own staged plan: `fr/` (SAT's docs in a second language — would need real French translation, not just structure), and the big remaining piece, `content/` (the collection of collections: `examples/` and `errors/`, each in `en-ca`/`fr-ca`/`es-ca`, with the ~8 and 9 ruling-test nodes HANDOVER's tables specify).
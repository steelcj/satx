# Ingress Verification Stamp

**Version.** v0.0.1, 2026-10-21. Under consideration.

**Scope.** An idea being considered, not a decision: that SAT marks content as verified when it takes the content in through ingress, and records which version of SAT did so. Drafted with AI assistance (Claude Opus 5.5, Anthropic) from Christopher Steel's direction.

## The idea

During ingress, SAT verifies the content it imports and marks it as verified. The same mark records the version of SAT that ingressed it.

Content SAT has not ingressed carries no mark. Its absence is the whole signal, so no marker is needed for documents written before SAT: whatever metadata they carry is a claim until SAT takes them in.

## Why the version matters

A verification mark on its own says only that something was checked once. Paired with the version of SAT that did the checking, it says what it was checked against. When SAT's rules change, content verified under an earlier version can be found and verified again, without anyone having to remember which documents predate the change.

## Not settled

- **The property's name.** SAT gives a `sat` property the DCTERMS local name wherever DCTERMS has a counterpart. DCTERMS has `conformsTo`, a standard the resource conforms to, which is close to "verified against this version of SAT", and `dateAccepted`, if the date of ingress matters too.
- **Where the mark lives.** In the content's sidecar, which SAT owns, or in its front matter. A mark in front matter can be copied or typed by hand, so it should be one SAT can re-derive and `sat read` can confirm.
- **What verification checks.** Which values SAT derives for itself during ingress, such as dates and contributors from history and language from the archive, and which it accepts as given.
- **The content's own version.** Whether the mark also records the version of the content it verified, so a later edit that changes that version shows the mark is out of date.

## Not pursued

`sat:migration_status: pre-sat`, already in the front matter of a number of documents in uc-radar and osat-manager-python, is not adopted. It marks what SAT has not touched, which the absence of a SAT mark already says. Existing occurrences stay until SAT ingresses those documents.

# Pre-SAT Documents

**Version.** v0.0.1, 2026-10-21. Draft.

**Scope.** Documents that exist before SAT manages the repository they live in: what their metadata can be trusted for, how they are marked, and what SAT does with them when it takes them in. Drafted with AI assistance (Claude Opus 5.5, Anthropic), provisional until Christopher Steel confirms it.

## The situation

Until SAT manages a repository's documentation, that documentation's metadata is written by hand, or by an assistant, into front matter. It is often incomplete and sometimes wrong: a date that was never updated, a creator copied from a template, an identifier generated twice, a description that no longer matches the text.

The repositories that check documents today, through uc-automa, check that the required fields are present and well formed. They cannot check that the values are true. A document that passes those checks has complete metadata, not correct metadata.

## The marker already in use

Without anyone defining it, a marker has spread: `sat:migration_status: pre-sat` appears in the front matter of 67 uc-radar entries and 12 osat-manager-python documents, counted on 2026-10-21. The repositories built with uc-automa, uc-automa itself, osat-manager-restic and osat-manager-git, do not carry it.

Read as it is used, `pre-sat` means: this document was written before SAT managed it, so treat its metadata as a claim, not a record.

## Proposed meaning

`sat:migration_status` takes one of three values.

| Value | Meaning |
| --- | --- |
| `pre-sat` | Written before SAT took the document in. Every metadata value is a claim, unverified. |
| `migrated` | SAT has taken the document in. Its metadata now lives in the document's sidecar; values SAT can derive have been derived, and the rest are carried over as claims. |
| `verified` | A person has reviewed the claims carried over, and the sidecar holds what the document actually is. |

A document without the property is read as `pre-sat` until SAT has taken it in.

## Taking a document in

A pre-SAT document reaches SAT the way other unsorted material does, through ingress: staged, not yet described. Taking it in sorts its front matter into two kinds.

**Derived.** Values SAT can establish for itself, which replace whatever the front matter claimed. The date a version first appeared, and its contributors, from the repository's history. The language, from the archive the document is placed in. The format, from the file.

**Carried as claims.** Values only a person can confirm: title, description, subject, creator where history does not settle it, rights, relations to other documents. These move into the sidecar unchanged and stay claims until review moves the document to `verified`.

An identifier is kept if it is a well-formed `urn:uuid` that no other document uses. A duplicate or malformed identifier is reported, never silently replaced, because other documents may already cite it.

## Until then

- uc-automa's checks treat missing or malformed metadata as something to fix, and fixing it is ordinary maintenance, not a correction of record.
- Nothing downstream, such as a published site or an index, should present pre-SAT metadata as authoritative.
- Writers add the marker to new documents in repositories that already carry it, so the count stays honest.

## Open

- **The property's name.** SAT gives a `sat` property the DCTERMS local name where DCTERMS has a counterpart, and coins a term only otherwise, in the lowerCamelCase DCTERMS uses, as in `isVersionOf`. `migration_status` follows neither, and uc-radar has asked separately whether its identity fields, this one among them, stay under `sat:` at all. Renaming is cheap now and expensive after SAT reads it.
- **Whether uc-automa should read the marker,** for example to report a pre-SAT document's metadata findings as notices rather than failures, or to require the marker on every governed document.
- **Where the property lives after migration.** A sidecar records state; whether `migration_status` stays in the document's front matter once its metadata has moved, or only in the sidecar, is not settled.
- **Translations.** This document exists in English only; the French and Spanish archives do not yet carry it.

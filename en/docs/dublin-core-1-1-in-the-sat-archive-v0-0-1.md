# Dublin Core 1.1 in the SAT Archive

**Version.** v0.0.1, 2026-09-09. Supersedes, with its companion, *Representing Dublin Core 1.1 as Front Matter* v0.0.2.

**Scope.** How DC 1.1 values are held in a SAT archive: where they are authored, how they cascade, and which of them describe which WEMI level. This is the canonical side. What a consumer receives is covered by *Dublin Core 1.1 as Eleventy Ingress Front Matter*.

**Status.** Partial. SAT itself is still being specified, and the sections below marked *undefined* record what is not settled rather than guessing at it.

## Why this is two documents

v0.0.2 tried to describe one set of values in one place and produced a contradiction about `format`. A Markdown file is `text/markdown`. The HTML page generated from it is `text/html`. Both statements are correct, each about its own artifact, and a single document describing both had to be wrong about one of them.

The split follows the direction of travel. SAT holds the archive and knows what the source is. Eleventy receives a projection and produces something new, which has properties of its own. Neither document restates the other's facts.

## Where a value is authored

Canonical metadata for a resource lives in that resource's sidecar, in the DC namespace of the metadata cascade:

```
areas.md
.areas.md.assets/content/metadata/dc/overrides/dc.yml
```

Values use the cascade's field shape, so authority descends with them:

```yaml
title:
  value: ["Areas"]
  overridable: true
description:
  value: ["What we maintain an ongoing standard in."]
  overridable: true
date:
  value: ["2026-09-04"]
  overridable: true
format:
  value: ["text/markdown"]
  overridable: true
```

A value declared at a node above descends to every node beneath it, so `publisher` and `rights` are stated once at the collection and never restated. `overridable: false` closes a field to the tiers below, and it narrows only, never widens.

## Three levels in one sidecar

A content node is an expression, and the file that carries it is that expression's source embodiment. One sidecar therefore holds statements at three WEMI levels, and knowing which is which is what keeps them from being generated into the wrong artifact later.

| Level | Elements | Behaviour |
| --- | --- | --- |
| Work | none in DC; carried as `sat:isVersionOf` | identity only, never descriptive |
| Expression | `title`, `creator`, `subject`, `description`, `language`, `date`, `contributor` | what the text is |
| Manifestation | `format` | what this embodiment is |

`format` is the only DC element that describes the file rather than the text, and `text/markdown` is the correct value for it here. It is a fact about the source, it is true of the source, and it stays with the source. A consumer that produces a different embodiment states that embodiment's own format and does not inherit this one.

Generated embodiments get no node and no metadata. An authored embodiment, a Braille edition or a typeset PDF, is declared and becomes a manifestation in its own right, with its own `format`.

## Which elements are authored

Of the fifteen, most are never typed at a resource.

| Source | Elements |
| --- | --- |
| Authored at the resource | `title`, `description`, `date`, `subject`, `creator`, `contributor` |
| Cascaded from above | `publisher`, `rights`, `type`, `format` |
| Received from the language archive | `language` |
| Not used | `relation`, `source`, `coverage`, `identifier` |

The last row needs its reasons.

`relation` and `source` say two resources are related and say nothing about how. Every relation the archive actually has is more specific than that: work identity, translation, part and whole. SAT carries them as named properties in its own namespace rather than as an undifferentiated `relation`, so nothing is left for the DC element to do.

`coverage` covers place and time in one element. Where either is wanted it is worth taking `dcterms:spatial` and `dcterms:temporal` instead, which separate them and can be queried.

`identifier` is held as `sat:identifier`, a `urn:uuid` minted once with `uuidgen -r`. A DC `identifier` carrying a URL would be a second name that changes when the site moves, which is the event the first one exists to survive.

## Language

`language` is declared once, at the language archive node, and received by every node beneath it through the metadata cascade. No content node restates it.

Tags follow BCP 47 <a id="cite-rfc5646"></a>([Phillips & Davis, 2009](#ref-rfc5646)) and are written lowercase, `en-ca` rather than `en-CA`. Case carries no meaning in BCP 47, so the two are one tag, but RDF 1.1 compares language-tagged literals character by character, which makes `"x"@en-CA` and `"x"@en-ca` distinct terms in a store <a id="cite-rdf11"></a>([Cyganiak et al., 2014](#ref-rdf11)). RDF 1.2 removes the distinction; 1.1 tooling is what an archive meets today. One lowercase form throughout means the archive cannot produce that class of bug, and it lets the archive directory name and the tag be the same string.

A passage in another language inside a document is inline markup, `<span lang="fr-ca">`. That is a fact about a run of text, not about the resource, and it does not belong in resource metadata.

## Repeatability and shape

Every DC 1.1 element is optional and every one is repeatable <a id="cite-dcmi-2012"></a>([DCMI, 2012](#ref-dcmi-2012)). There is no required element, no cardinality constraint, and no distinction between elements that may repeat and elements that may not.

Values are therefore lists, always, including where only one value is present. A reader may accept a bare scalar and normalise it, but a schema where some elements are scalars and others are lists encodes a distinction the standard does not make, and every consumer then carries the same table of exceptions.

DC 1.1 is the `/elements/1.1/` namespace. DCMI Metadata Terms is the later `/terms/` vocabulary, with domains and ranges declared. `dc:date` and `dcterms:date` are different properties. SAT holds DC 1.1 in `metadata/dc/`, and a `metadata/dcterms/` namespace sits alongside it for whenever refinements are wanted.

## Quoting

Language keys and slugs are quoted, always. Under YAML 1.1 `no` is a boolean, and `no` is the ISO 639-1 code for Norwegian, so an unquoted Norwegian key parses as `false` and the value disappears with no error and nothing visible in the file. `y`, `on` and `off` behave the same way, and a bare numeric slug parses as an integer and stops matching the string it names.

Three defences, none expensive: quote the keys, parse as YAML 1.2, which dropped that boolean set, and have validation assert that keys and slugs are strings. Two of the three belong in the toolchain rather than in a style guide.

## Not yet defined

**How `sat:` metadata is partitioned.** `identifier`, `isVersionOf` and `slug` are settled. Whether non-language axis coordinates sit in the same namespace file or in one of their own is not.

**Whether `creator` and `subject` are work properties.** Both are arguably facts about the content rather than about one language version of it, and both are currently repeated on every expression. Moving them up needs somewhere to put them, and there is no work record.

**What describes an authored manifestation.** Enough exists to say that an embodiment is authored and where it sits. A Braille edition with its own pagination has properties that nothing yet models.

**Validation.** DCTAP over the resolved metadata, converted to SHACL, is the intended shape. No profile is written.

## References

<a id="ref-rdf11"></a>Cyganiak, R., Wood, D., & Lanthaler, M. (Eds.). (2014). *RDF 1.1 concepts and abstract syntax*. W3C. https://www.w3.org/TR/rdf11-concepts/ [↩](#cite-rdf11)

<a id="ref-dcmi-2012"></a>Dublin Core Metadata Initiative. (2012). *Dublin Core metadata element set, version 1.1*. https://www.dublincore.org/specifications/dublin-core/dces/ [↩](#cite-dcmi-2012)

<a id="ref-rfc5646"></a>Phillips, A., & Davis, M. (2009). *Tags for identifying languages* (BCP 47, RFC 5646). IETF. https://www.rfc-editor.org/rfc/rfc5646.html [↩](#cite-rfc5646)

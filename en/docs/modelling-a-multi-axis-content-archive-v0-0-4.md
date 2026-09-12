# The Layered Stack: Modelling a Multi-Axis Content Archive

**Version.** v0.0.4, 2026-09-09. Supersedes v0.0.3.

**Scope.** This describes the archive at rest, how content and its metadata are organised, what identifies a piece of content, and what relates it to its variants. Serialization, URL generation, and delivery to any particular site generator are downstream concerns and out of scope. Designing the structure around a consumer is how the structure ends up shaped like a tool instead of like the content.

**Premise.** No single vocabulary is sufficient, and looking for one is the mistake. RDF is additive: a resource can carry several types and properties from several vocabularies with no conflict, no precedence rules, and no loss. The design question is not *which standard* but *which layer each standard belongs to*, and whether the layers are complete.

**Second premise, arrived at late and worth stating first.** Language is not the model. It is one axis a work varies along, and it happened to be the first one needed. An easy-read version of a page is the same kind of thing as a translation of it: a different expression of one work. A design built around language specifically will have to be torn up when the second axis arrives. A design built around *axes*, with language as the first, will not.

**Third premise, new in this version.** The model is multi-axis. The filesystem is not. Archive roots are language trees and nothing else; every other coordinate is declared in front matter. The two statements are compatible because coordinates were never a filesystem fact in the first place, and separating them removes an entire class of decisions rather than answering them.

| Layer | Purpose | Recommendation |
| --- | --- | --- |
| Conceptual model | What kinds of thing exist and how they relate | **IFLA LRM** (WEMI) |
| Entity vocabulary | Those kinds and relations, in RDF | **OpenWEMI** + a local refinement |
| Descriptive properties | Titles, dates, descriptions, rights | **dcterms** |
| Axes and value vocabularies | Coordinates, subjects, roles | **SKOS**, MARC Relators, BCP-47 |
| Provenance | Who made which version, from what | **PROV-O** (optional) |
| Consumption | What machines outside the archive read | **schema.org** (emitted, never authored) |
| Profile | Which properties are required where | **DCTAP** → SHACL |

Only the first is a model. The rest are vocabularies, and they compose.

## Changes in this version

Everything in this section is expanded below. It is here so that a reader of v0.0.2 can see what moved without rereading.

- **A section was misnamed.** "Where a variant belongs" answered which WEMI level a variant lands on, and read as though it were about location. It is now "Which level a variant belongs to", and says plainly that every Expression-level variant lives on the filesystem like any other page.
- **Every axis keeps its registry.** v0.0.2 could be read as though moving register off the filesystem demoted it. It did not. `axes/register.yaml` is the same kind of file as `axes/language.yaml`, and `lsq` is a language exactly as `fr-ca` is. What differs is which axis is the root axis, not which axis is real.
- **Variants name themselves, in their own language.** A non-default coordinate declares a slug token per language in its registry, so the same coordinate is `areas-easy-read.md` in English and `domaines-lecture-facile.md` in French. The base slug survives, the coordinate stays the source of truth, and the scan checks that the filename and the coordinates agree.
- **The Manifestation decision is closed.** The line is authored against generated, not filesystem against not. Generated embodiments are build output and get no node; an authored one is declared and becomes a real manifestation.
- **The tree root was never a decision.** A page at the root of a language tree has an empty slug path and is addressed at the language root, the same in every language. v0.0.2 raised it as an open question in error.
- **A coordinate is resource metadata, and the front matter is a projection of it.** v0.0.3 says a non-root coordinate is "declared in front matter", which is true of the file an author reads and false of where the value is kept. In a SAT archive the front matter is generated ingress; the coordinate is authored in the resource's own sidecar. The new section says so and reconciles `_defaults.yaml` with the SAT metadata cascade, which were the same mechanism under two spellings.
- **Coordinates never cascade, and the root axis always does.** This was implicit and is now a rule. A metadata cascade would mechanically permit `register: easy` on a directory node, and permitting it would put an expression's identity back under the control of where its file sits, which is the coupling this version removed.
- **Two kinds of default that look alike are separated.** An omitted axis takes the default declared on the axis, not a default inherited from an ancestor node. In a system whose whole idiom is cascade, that distinction has to be stated or it will be assumed away.
- **Drift is computed from checksums.** Git already versions everything, so nothing needs to be authored: compare the source blob as it stood at the translation's last commit with the source blob now. The proposal to record a versioned source in `translationOf` is withdrawn; a recorded digest survives only as a fallback for unreliable history.

## The model: IFLA LRM

**FRBR** (1998) is an entity–relationship model published by IFLA, describing bibliographic resources from the user's point of view, finding, identifying, selecting, obtaining. Its value is that it sits above any cataloguing code: AACR, RDA, and ISBD all implement it; none of them is it.

**IFLA LRM** <a id="cite-riva-2017"></a>([Riva et al., 2017](#ref-riva-2017)) supersedes it. It consolidates FRBR with FRAD (authority data) and FRSAD (subject authority data) into one model. FRBR, FRAD, and FRSAD are all formally superseded, so cite LRM and treat FRBR as history rather than as the current standard.

**LRMoo** (1.0, approved April 2024) is LRM expressed as a formal ontology, aligned with CIDOC-CRM so library and museum descriptions interoperate. It succeeds FRBRoo 2.4.

WEMI is the acronym for the four entities that survive across all of these:

| Entity | Definition | In the archive |
| --- | --- | --- |
| **Work** | The abstract intellectual content | The "areas" content, independent of language |
| **Expression** | A realisation of the work | The English text; the French text; the easy-read English text |
| **Manifestation** | The embodiment of an expression | The Markdown source; an HTML rendering; a PDF |
| **Item** | A single exemplar | One copy of a manifestation. Rarely meaningful here. |

A work is *realised through* an expression, an expression is *embodied in* a manifestation, a manifestation is *exemplified by* an item.

## Where the archive actually sits

This is the correction that everything else follows from, and it is easy to skip.

**The files are manifestations.** `en-ca/areas.md` is not the English text; it is *an embodiment of* the English text in Markdown. Render it to HTML and you have a second manifestation of the same expression. Print it and you have a third. Nothing above the file level exists on the filesystem, which is exactly why the metadata has to carry it.

**Language is a property of the Expression.** Not of the work, which is language-independent by definition. Not of the manifestation, because the Markdown source and the HTML rendering are both in English, and neither is where that fact belongs.

**And language is not the only such property.** Register is another: an easy-read version has different words, so it is a different expression of the same work, exactly as a translation is. Tillett's taxonomy <a id="cite-tillett-1991"></a>([Tillett, 1991](#ref-tillett-1991)) puts translation and simplification side by side as derivative relations; neither is subordinate to the other. Modality is a third: an audio narration realises the work differently again.

So an expression is not identified by a language. It is identified by a **work plus one coordinate on each axis the archive recognises**:

```
work:          the abstract content
expression:    work × language × register × …
manifestation: a file, a rendering, a printing
item:          one copy
```

Language is axis one. Nothing in the design should assume it is the only one, and the cost of that assumption is not hypothetical: it is a rewrite of every resolver the day an easy-read version is commissioned.

### Which level a variant belongs to

This is a question about the model, not about the filesystem. Every Expression-level variant lives in a language tree beside the pages it varies from, exactly as any other page does; what is being decided here is whether a given variant is a new expression at all, or the same expression embodied differently. The test is whether **the text changed**:

| Variant | Level | Why |
| --- | --- | --- |
| Translation | Expression | Different words |
| Easy read | Expression | Different words |
| Audio narration | Expression | Different realisation |
| Large print | Manifestation | Same words, different embodiment |
| Braille | Manifestation | Same words, different embodiment |
| PDF of the HTML | Manifestation | Same words, different embodiment |

Getting this wrong is expensive in both directions. Treat a manifestation as an expression and the same text is authored twice. Treat an expression as a manifestation and its distinct content has nowhere to live.

Note what the right-hand column means in practice. Everything in the top half of that table is a page in a language tree with a coordinate declared. Everything in the bottom half is not a page at all, and the question of when those become real records is answered under "When Manifestation becomes real".

### The consequence for identifiers

Three levels means three identifier spaces, and only one of them is authored.

```
work:          a UUID, minted once, written in front matter
expression:    derived, work UUID + coordinates
manifestation: derived, the file, or the URL of a rendering
```

Expression identifiers need no registry, because a work plus its coordinates determines one. That falls out of the axes being positional, and it means the richer model costs nothing at authoring time.

## The filesystem is not the coordinate space

v0.0.1 put the whole coordinate set in the first path segment, `en-ca__easy/`, and then spent a page of open decisions on how to encode it. The premise was wrong. Coordinates identify an expression; they do not have to be where the file lives.

**One axis is realised as directories, and it is language.** A language tree is a real editorial boundary. It has its own organisation, its own slugs, its own depth, often its own maintainer, and it is the unit that gets handed to a translator or lifted out into another SAT instance. Register is not that. An easy-read page is a variant of a page inside one language's organisation, and it belongs beside the page it varies from.

**This is not a demotion of the other axes.** Every axis has a registry in `axes/`, of the same shape, resolved by the same code, and adding one is a YAML file plus a line in `archive.yaml`. `axes/register.yaml` is as real as `axes/language.yaml`, and `lsq` is a language exactly as `fr-ca` is; nothing about a sign language makes it a variant of something else. The only asymmetry is that one axis has to be the one the directories are named for, and language is the one that earns it.

**Every other axis is declared in front matter**, in one block, under `coordinates:`.

```
en-ca/
  areas.md              language en-ca from the root, register standard by default
  areas-easy-read.md    language en-ca from the root, register easy as declared
```

```yaml
# en-ca/areas-easy-read.md
---
work: urn:uuid:8f7d1a92-3c04-4b1e-9f2a-6d5e8c0b7a41
coordinates:
  register: easy
translationOf: "en-ca"
---
```

Identity is unaffected by where the file sits. That expression is still `work × language=en-ca × register=easy`, still has the same derived identifier, and still appears in the same cell of the coverage matrix as it did when it lived in its own root. The UUID table, the sibling relations, and selection are all unchanged.

What changes is everything the path was doing badly.

**There is no coordinate encoding to decide.** Separator against nesting was a question about putting several values in one path. With one value there is no separator to agree on, no canonical order to enforce in a directory name, and no risk of an unparseable mixed archive.

**Axis namespaces become independent.** Both path encodings had to resolve a segment by looking it up across all axes, which required axis value keys to be unique across the whole archive. That constraint is gone. Language owns the path namespace; every other axis is keyed by its own name in front matter. A register value may now be spelled the same as a language value with no ambiguity anywhere.

**Content can no longer be mistaken for a coordinate.** Under nesting, a page directory legitimately named `easy` inside `en-ca/` was read as a register coordinate, and the page silently lost its slug. There is no equivalent failure when content never occupies the first segment.

**Section defaults reach every variant.** `en-ca/about/_defaults.yaml` now applies to the easy-read expressions in that section, because they are in that section. Under root coordinate sets, `en-ca__easy` was a separate tree that needed its own copy of the same defaults.

**The cost, stated plainly.** Variants of one page share a directory, so they need distinct filenames. That is a naming question rather than an identity one, and it is answered under "Variant slugs": the coordinate declares a token per language, the filename carries it, and the base slug is what is left when the token is stripped. Resolution across variants goes through work identity plus coordinates in every case.

**The closed axis set is enforced in two places instead of one.** An undeclared archive root is an undeclared language. Inside `coordinates:`, an undeclared axis name, an undeclared value, or the root axis appearing at all are each errors. So is an axis name written at the top level of front matter rather than inside the block, because that is the likely mistake and it would otherwise be silent.

## Coordinates in a SAT archive

The previous section says a non-root coordinate is declared in front matter. That is true of the file an author opens and false of where the value is kept, and the difference matters once this model is realised on SAT rather than described on its own.

### Front matter is a projection

In a SAT archive the canonical metadata for a resource lives in its sidecar, and the front matter is generated for ingress and overwritten on every run. A coordinate is therefore authored here:

```
en-ca/areas-easy-read.md
en-ca/.areas-easy-read.md.assets/content/metadata/sat/overrides/sat.yml
```

```yaml
# .areas-easy-read.md.assets/content/metadata/sat/overrides/sat.yml
identifier:
  value: "urn:uuid:d92f5a13-7c68-4e20-b34a-9f1e6c8d2075"
  overridable: false
isVersionOf:
  value: "urn:uuid:8f7d1a92-3c04-4b1e-9f2a-6d5e8c0b7a41"
  overridable: false
register:
  value: "easy"
  overridable: true
```

and it appears in front matter as `coordinates: {register: easy}` because that is what a template engine can read. Nothing about the model changes; the sentence "declared in front matter" becomes "declared on the resource", and the resource is a node with a sidecar rather than a file with a header.

One consequence is worth naming rather than discovering. `en-ca/about/_defaults.yaml` in the layout above and a directory node's `metadata/dc/overrides/dc.yml` are the same mechanism under two spellings. An archive should keep one of them. On SAT the sidecar wins, because it is where the cascade already looks and because a second defaults mechanism would need its own precedence rules against the first.

### Coordinates never cascade; the root axis always does

The two axes are handled by opposite rules, and the asymmetry is deliberate.

**The root axis is positional and inherited.** `language` is declared once at the archive node, locked there, and received by every node beneath it through the metadata cascade. No content node restates it, and a content node that contradicted its own archive would be an error.

**Every other coordinate is declared on the resource and inherits from nothing.** A directory node must not declare `register`, and a resolver encountering one should reject it rather than apply it.

The mechanism would permit it: a metadata cascade descends whatever it is given, and `register: easy` on `en-ca/plain-language/` would reach every file beneath. The reason to refuse is that it would make an expression's identity depend on where its file sits. Move the file and its coordinates change; move it back and they change again. That is precisely the coupling this version removed by taking coordinates off the filesystem, and reintroducing it through the cascade would be the same defect wearing a different hat.

The cost is repetition. Forty easy-read pages in a section carry the same two lines forty times, and no inherited value can shorten them. That repetition is what makes moving any one of those files safe, which is the trade being made. Supplying the lines is an authoring-tool concern, not a model one: a template, a `sat content new --register easy`, or a Sveltia collection default all write the value at the resource where it belongs.

### Two kinds of default that look alike

An omitted axis is filled from the default declared on the axis, in `axes/register.yaml`. That is not a cascaded default and does not come from an ancestor node.

| | Where it is declared | What it is a property of | Same everywhere? |
| --- | --- | --- | --- |
| Axis default | the axis registry | the axis | yes |
| Cascaded default | an ancestor node's sidecar | position in the tree | no |

Coordinates use the first only. In a system whose idiom is cascade, this needs stating or it will be assumed away: `default_coordinates: fill` reads like an inheritance rule and is not one. It says an unstated coordinate resolves to the axis's declared value, identically at every position in every tree, with `asserted: false` recorded so the filled value is distinguishable from a stated one.

Descriptive metadata is the other way round. `rights`, `publisher`, `audience` and `subject` are exactly what a cascade is for, and they inherit from wherever they are declared. The rule is not "SAT metadata does not cascade"; it is that identity-bearing metadata does not, and coordinates are identity-bearing because an expression is a work at a set of them.

### What this makes checkable

Four errors follow from the rules above, and each is otherwise silent:

- a coordinate declared at any node that is not a content node
- the root axis appearing in a content node's coordinates, where the archive already determines it
- a content node whose received `language` disagrees with the archive it sits in
- an axis name written at the top level of a resource's metadata rather than under the coordinate block, which is the likely authoring slip

### Where the axis registries sit

`archive.yaml` and `axes/` are collection-scoped authority, above the language trees and below any enclosing collection. This matches where a work index sits: a work belongs to one site rather than to a folder of sites, and so does the axis set that site's expressions are indexed by. A collection of collections may declare axes its members inherit, on the same terms as any other cascaded value; a member that needs an axis its parent does not have declares it and owns it.

## Choosing the entity vocabulary

dcterms cannot carry the model. It has 55 properties and almost no classes: there is no `dcterms:Work`, only `dcterms:BibliographicResource`, which covers Work and Expression and distinguishes neither. There are also no properties for the WEMI relations themselves, no `dcterms:realizedThrough`. The relations `isVersionOf` and `hasVersion` get you a usable approximation, but they are approximations, and the model stays implicit in how you happen to use them.

Five real candidates fill that gap.

| Vocabulary | Model | Verdict |
| --- | --- | --- |
| **OpenWEMI** (DCMI) | W/E/M/I, minimally constrained | **Recommended.** Purpose-built for this |
| **LRMoo** | LRM as CIDOC-CRM extension | Correct but maximal. Only for CRM integration |
| **RDA Registry** | LRM-faithful, library cataloguing | Excellent mapping target, poor authoring vocabulary |
| **BIBFRAME 2.x** | Work / Instance / Item | **Wrong shape for this problem** |
| **FRBR Core** (2005) | W/E/M/I, lightweight | Superseded in practice by OpenWEMI |

### OpenWEMI

A DCMI vocabulary at `https://ns.dublincore.org/openwemi/`, published to let non-library communities use WEMI without inheriting library catalogue semantics <a id="cite-coyle-2022"></a><a id="cite-coyle-2025"></a><a id="cite-dcmi-2024"></a>([Coyle, 2022](#ref-coyle-2022), [2025](#ref-coyle-2025); [DCMI, 2024](#ref-dcmi-2024)). It defines the four classes plus a grouping superclass `Endeavor`, and it deliberately removes FRBR's disjointness rules and strict linearity.

The relations:

- `expresses` / `expressedBy`, Expression to Work
- `manifests` / `manifestedBy`, Manifestation to Expression or Work
- `instantiates` / `instantiatedBy`, Item to any of the above
- `relatedWork`, `relatedExpression`, `relatedManifestation`, `relatedItem`, same-level relations
- `commonWork`, `commonExpression`, and so on, which assert two resources share a level without typing either

`relatedExpression` is the sibling relation the archive needs, and `commonWork` is how an outside dataset can be told that two of its resources are the same work as ours without adopting any of our modelling.

OpenWEMI is explicitly designed to be **subclassed**. That is the intended usage, not a workaround, and it is what makes the archive's own vocabulary legitimate rather than idiosyncratic:

```turtle
@prefix arc: <https://example.org/ns/> .
@prefix owemi: <https://ns.dublincore.org/openwemi/> .

arc:LanguageExpression  rdfs:subClassOf  owemi:Expression .
arc:translationOf       rdfs:subPropertyOf  owemi:relatedExpression ;
                        rdfs:subPropertyOf  dcterms:source .
```

A consumer that knows only OpenWEMI still understands `arc:translationOf` as a related expression. A consumer that knows only dcterms still understands it as a source. Neither has to know anything local. This is the whole argument for refinement over invention.

### Why not the others

**LRMoo** is the maximal correct answer and the wrong tool here. It is event-centric: creating an expression is an `F28 Expression Creation` event with participants and a timespan. That machinery is precious for cultural heritage, since it lets you say who did what when, across institutions, and it is a great deal of structure to carry for an archive whose creation events are "someone wrote a page." Adopt it if the archive must federate with CIDOC-CRM data. Otherwise the cost is real and the benefit is speculative.

**RDA Registry** is LRM-faithful, actively maintained, and has genuine classes (`rdac:Work`, `rdac:Expression`). Its property IRIs are opaque numerics, `rdaw:P10078` is "has expression of work", which is fine for machine data and hostile to hand-authored front matter. It also carries cataloguing assumptions the archive has no use for. Best treated as something to *map to* if the archive ever needs to talk to library systems, not as the vocabulary you write in.

**BIBFRAME** deserves a specific retraction. Earlier drafts of this document suggested `bf:Work` as a cheap way to type the work. That was wrong. BIBFRAME has three levels, Work, Instance, and Item, and it folds Expression into Work. Language versions in BIBFRAME are separate Works joined by `bf:translationOf`. For most catalogues that simplification is defensible. For an archive whose entire organising principle is the work/expression split, it collapses precisely the distinction being modelled. Do not use it here.

**FRBR Core** <a id="cite-davis-2005"></a>([Davis & Newman, 2005](#ref-davis-2005)) is the lightweight RDF vocabulary OpenWEMI is loosely based on, and it is unmaintained. OpenWEMI is its maintained descendant with institutional backing.

## Value vocabularies

Properties are only half of it. What goes in them matters as much, and this is where multilingual archives usually leak.

### Subjects should be concepts, not strings

`subject: [areas, practice standards]` in English and `subject: [domaines, normes de pratique]` in French are two unrelated string lists. Nothing connects them, so nothing can answer "show me everything on this topic, in any language."

The fix is the same move made one level down: a subject is a **SKOS concept** <a id="cite-miles-2009"></a>([Miles & Bechhofer, 2009](#ref-miles-2009)) with an identifier and a label per language.

```yaml
# concepts.yaml
practice-standards:
  prefLabel:
    "en-CA": Practice standards
    "fr-CA": Normes de pratique
  broader: clinical-governance
```

Files reference the concept identifier; labels are resolved per language. SKOS also gives `broader`, `narrower`, and `related` for free, so the subject vocabulary becomes navigable rather than a flat tag cloud. If an external thesaurus covers the domain, point `skos:exactMatch` at it and inherit its multilingual labels rather than maintaining your own.

The pattern is worth naming, because it recurs: **anything that has a different string per language is a concept with labels, not a property with a value.** Work titles, subjects, collection names, and role names are all instances of it.

### Roles need a vocabulary

Neither dcterms nor OpenWEMI can say who translated something. `dcterms:contributor` says a person was involved and nothing more. **MARC Relators** (`https://id.loc.gov/vocabulary/relators/`) supplies the missing precision, `trl` for translator, `aut` for author, `edt` for editor, as SKOS concepts with labels already in several languages. For a translation archive, distinguishing author from translator is not an optional detail; it is the difference between two expressions of one work and two works.

### Language identity

Use full BCP-47 tags on every language-tagged literal and on `dcterms:language` <a id="cite-phillips-2009"></a>([Phillips & Davis, 2009](#ref-phillips-2009)). `fr-CA` and `fr-FR` are different expressions of a work as far as the model is concerned. Dropping the region because there is currently only one French forecloses the other cheaply now and expensively later.

**Undocumented and unstandardised languages are a requirement, not an exception.** The archive must accommodate regional sign languages, languages with no ISO code, constructed languages, and expression systems that are arguably not languages at all. The instinct is to invent a tag and mark it invalid. Don't, and more usefully, you don't have to.

Inventing a tag outside BCP-47 has one specific, unrecoverable cost: it breaks language-tagged literals. In RDF, `rdf:langString` and JSON-LD's `@language` require a well-formed BCP-47 tag; processors are entitled to reject or silently drop a literal carrying an ill-formed one. Lose that and multilingual labels, the mechanism the SKOS concepts and the relator terms all depend on, stop working. The tag is not decoration; it is load-bearing.

Four mechanisms cover the cases, in order of preference:

**Check ISO 639-3 first.** It covers roughly 7,900 languages, including most documented sign languages. Quebec Sign Language is `fcs`; American Sign Language is `ase`. Many languages assumed to be uncoded are not. Note that `sgn-CA`-style tags are deprecated in favour of the direct code.

**Use the `qaa`–`qtz` private-use range.** RFC 5646 reserves these subtags for private use, corresponding to codes reserved by ISO 639-2, and states they may be used as non-registered primary language subtags instead of `x-` private-use subtags. This is the mechanism designed for exactly this problem: 520 slots for languages the archive recognises and the standards do not, with every tag remaining well-formed BCP-47.

**Append `x-` subtags for varieties.** A regional or community variety of a coded language stays anchored to it: `fcs-x-saguenay` is still parseable as Quebec Sign Language by anything that doesn't know the private part.

**Use the special codes where they are truthful.** `mis` for uncoded languages, `und` for undetermined, `art` for constructed languages, and `zxx` for content with no linguistic content at all.

That last one deserves a moment. For plant or animal expression systems, `zxx` plus an explicit modality property is more honest than a fabricated language tag, and it will not mislead a consumer into applying language-processing assumptions that don't hold. The archive can still treat these as expressions of a work, since Expression is about realisation and not specifically about language, but the axis distinguishing them may be medium rather than language.

**What not to do:** encode a non-language axis as a language tag. `en-CA-x-easy` is well-formed BCP-47 and it lies. Register is not language, and a consumer selecting content by language will get the wrong answer with no way to detect it. If a distinction is not linguistic, it needs its own axis, not a private-use subtag on someone else's. The rule survives the move to front-matter coordinates unchanged, and is now checkable: the easy-read expression carries `dcterms:language: en-CA` and `register: easy`, and neither field contains the other's information.

## Axes

An axis is a dimension along which expressions of one work vary. Language is the first; register, modality, and audience are the usual next ones.

Each axis is a **`skos:ConceptScheme`** and each of its values is a **`skos:Concept`**, which means an axis file has the same shape as `concepts.yaml` and uses the same resolver. Every value needs an identifier and labels in each language, because "easy read" must display as *lecture facile* in the French interface. Language is simply a scheme whose concepts carry BCP-47 tags as an attribute.

```yaml
# axes/language.yaml
default: "en-ca"
values:
  - key: "en-ca"
    tag: "en-CA"
    status: standard
    label:
      "en-CA": English (Canada)
      "fr-CA": Anglais canadien

  - key: "lsq"
    tag: "fcs"
    status: standard
    label:
      "en-CA": Quebec Sign Language
      "fr-CA": Langue des signes québécoise

  - key: "nsl-north"
    tag: "qaa-x-nslnorth"
    status: private-use
    note: No ISO 639-3 code. Private-use primary subtag assigned locally.
    label:
      "en-CA": Northern regional sign variety
      "fr-CA": Variété régionale de signes du Nord
```

```yaml
# axes/register.yaml
default: "standard"
values:
  - key: "standard"
    label:
      "en-CA": Standard
      "fr-CA": Standard

  - key: "easy"
    label:
      "en-CA": Easy read
      "fr-CA": Lecture facile
    slug:
      "en-ca": easy-read
      "fr-ca": lecture-facile
```

Four things follow from the axis file that are worth being explicit about.

**Keys are local; tags are what the key resolves to.** The archive can name a variety it recognises, emit a well-formed tag for machines, and record openly that the tag is private-use, three facts at once, with no invented syntax anywhere. A language later receiving an ISO code is a one-line change rather than a rename across the archive.

**The axis set is closed.** An undeclared axis appearing in a coordinate is an error, not a new axis. Without that rule a typo silently creates a dimension, and the archive's shape becomes whatever anyone happened to type.

**One axis is the root axis, and it is language.** The archive declares which one in `archive.yaml`. Root axis values are directory names at the top of the archive and are never written in front matter; every other axis is written in front matter and never appears in a path.

**A non-default value carries a slug token per language.** `label` is what a reader sees in an interface; `slug` is what a reader sees in a filename and a URL. Both are per language for the same reason, and the default value declares neither, because an unmarked page keeps the base slug.

### Declaring a coordinate

```yaml
---
work: urn:uuid:8f7d1a92-3c04-4b1e-9f2a-6d5e8c0b7a41
coordinates:
  register: easy
---
```

One block, one purpose. Keys are axis names, values are axis value keys, and both are checked against the declared axes. An axis omitted here takes its declared default. The root axis must not appear, because it is already determined by the file's location, and two sources of truth for one coordinate is one too many.

### Variant slugs

A variant should say what it is, in the language of the tree it sits in. The token declared on the axis value supplies that:

```
en-ca/areas.md                    areas,     register standard
en-ca/areas-easy-read.md          areas,     register easy
fr-ca/domaines.md                 domaines,  register standard
fr-ca/domaines-lecture-facile.md  domaines,  register easy
```

Four properties fall out of it.

**The base slug survives.** Strip the tokens and you have the page, so variants of one page share a base slug on purpose. Uniqueness within a tree is therefore the base slug plus the coordinates, not the base slug alone.

**The coordinate remains the source of truth.** The token is a naming convention over a fact declared in front matter, not a second place to declare it. Nothing resolves by parsing a filename.

**The two can be checked against each other.** Coordinates that require a token the filename does not carry, and a filename carrying a token no coordinate declares, are both errors. The second is the likely authoring mistake: a file named `notes-easy-read.md` with no `coordinates:` block is a page that looks like a variant and is not one, and without the check it publishes as standard register with a misleading name.

**A fixed slug and a UUID search return the same set.** Resolution across variants goes through work identity plus coordinates in every case. The token is for readers; it buys legibility in URLs and file listings, and the archive would still work if every filename were a hash.

An archive that does not want the convention sets `variant_slug_policy: free`, and filenames go unchecked.

### The tree root is not a special case

`en-ca/index.md` is the home page of the English tree. Its slug path is empty, it is addressed at the language root, and `fr-ca/index.md` is the same page in French, sharing its work. There is nothing here to decide; it is how the web already works. The only thing worth stating is that the index collapse applies to the directory that contains the file, so `lsq/domaines/index.md` takes `domaines` and `lsq/domaines-lecture-facile/index.md` takes the same base slug at a different coordinate.

### Quoting is not optional

Language keys and slugs must be quoted in YAML. `no` is the ISO 639-1 code for Norwegian *and* a YAML 1.1 boolean, so `no: Områder` parses as a boolean key and the Norwegian label silently disappears. There is no error and the file looks correct. `y`, `on`, and `off` behave the same way, and a bare numeric slug parses as an integer and will not match the string in a path.

Three independent defences, all cheap: quote every key, use a YAML 1.2 parser, which dropped the `yes`/`no` boolean set, and have the profile assert that keys and slugs are strings. Two of the three are mechanical and belong in the toolchain rather than in a style guide, so the parser configuration and the profile check are both requirements of the build, not advice to authors.

## When Manifestation becomes real

v0.0.2 left this open on the grounds that a Braille or large-print edition would force the level to become real. That is the wrong line. The question is not which embodiments exist, it is which ones are **authored**.

**A generated embodiment is build output, not archive content.** HTML, PDF, and EPUB produced from the source by a build are recomputable from the archive plus the build, they carry no decisions anyone made, and recording them would be recording the build's own output back into its input. They get no record. One implicit manifestation per source file is enough, because the source file is the only embodiment the archive holds.

**An authored embodiment is a real manifestation.** A hand-corrected Braille transcription, a print PDF with typesetting nobody regenerates, a recording of a reading: each contains work that exists nowhere else, and losing it is losing content. It is declared beside its expression:

```yaml
# en-ca/areas.md
---
work: urn:uuid:8f7d1a92-3c04-4b1e-9f2a-6d5e8c0b7a41
manifestations:
  - path: "areas.brf"
    format: "application/x-brf"
    note: Hand-corrected transcription, not regenerated by the build.
---
```

Declaring it is the assertion that it was authored. The scan emits a manifestation node for it alongside the one for the source file, checks the path exists, and changes nothing about the expression: Braille is the same words, so it adds an embodiment and not a coordinate.

The rule is checkable, which is what closes the decision. "Manifestation becomes real when large print exists" is a prediction about the future; "an embodiment that is authored is declared, and a declared embodiment must exist" is a check that runs today, and an archive that never authors one never pays for the level.

## Provenance

`dcterms:source` records that a translation derives from another expression. It does not record who did it, when, or from which intermediate version.

If that matters, **PROV-O** <a id="cite-lebo-2013"></a>([Lebo et al., 2013](#ref-lebo-2013)) is the standard layer, and it composes with everything above:

```turtle
<expression/areas/fr-CA>
    prov:wasDerivedFrom  <expression/areas/en-CA> ;
    prov:wasGeneratedBy  [ a prov:Activity ;
        prov:wasAssociatedWith  <agent/translator> ;
        prov:endedAtTime  "2026-09-04"^^xsd:date ] .
```

Whether to carry this is a real decision, not an obvious yes. For a small archive with one translator it is ceremony. For an archive where translations are commissioned, audited, or revised against a moving original, it is the record that lets you answer "which English version was this translated from, and is it still current?", a question that becomes urgent the moment the source text is edited after translation.

What PROV-O is not needed for is drift. v0.0.2 proposed recording a versioned source identifier in `translationOf` to catch it. That is withdrawn: git already versions everything, so the answer is a checksum comparison rather than a field.

### Drift is a checksum question

When a source expression is revised after its translations were made from it, the divergence is already recorded, in the history, and nothing needs to be authored to find it:

```
commit  = the translation's last commit
then    = the source blob as it stood at that commit
now     = the source blob as it stands
drift   = then ≠ now
```

Three properties make this the right shape. It is **derived**, so there is no field to keep in sync and no field to forget. It follows the **derivation edge** rather than the work, so editing the English standard marks its own derivatives stale and leaves a French easy-read alone if that came from the English easy-read. And it is **free**, because the enrichment pass already has the repository open.

Two failure modes are worth knowing rather than papering over. A later unrelated edit to the translation moves the baseline forward and falsely clears the drift, since the comparison is anchored to the translation's last commit and not to the last commit that touched its content. And shallow clones or squashed merges lose the comparison entirely, which most CI configurations produce by default.

For an archive whose history is unreliable, the fallback is a recorded digest of the source blob in front matter, which needs no repository at all and is the one case where a version identifier is worth authoring. It is a fallback, not the default: an authored digest is one more thing that can be stale.

## Consumption: schema.org

schema.org is not a competitor to any of the above. It is what search engines and general web tooling read, and it belongs in emitted output only, never in authored files, because it is a projection of the archive rather than a source of truth.

The relevant terms are `translationOfWork`, `workTranslation`, and `inLanguage`. The mapping is mostly mechanical. Note that schema.org, like BIBFRAME, has no Expression level: `CreativeWork` covers work and expression together, so the emitted schema.org view is lossy by construction. That is fine. It is a view.

Multi-typing means the archive never has to choose:

```json
"@type": ["openwemi:Expression", "arc:LanguageExpression", "schema:CreativeWork"]
```

## Archive layout

```
archive.yaml

authorities/
  agents.yaml
  concepts.yaml

axes/
  language.yaml
  register.yaml

en-ca/
  index.md                          the tree root, empty slug path
  areas.md
  areas-easy-read.md                same base slug, register easy
  areas.brf                         an authored embodiment, declared by areas.md
  notes.md
  about/
    _defaults.yaml
    legal/
      privacy-policy.md

fr-ca/
  index.md
  domaines.md
  domaines-lecture-facile.md        the same coordinate, named in French
  a-propos/
    juridique/
      politique-de-confidentialite.md

lsq/
  domaines/
    index.md
```

Five rules:

1. **The first path segment is a language**, a declared value of the root axis, and nothing else. Every other coordinate is declared in front matter.
2. **Each tree is independent.** Paths, slugs, and depth need not correspond between trees. The French tree organises French content the way French readers expect.
3. **The only thing crossing between trees is an identifier**, a work UUID, a concept key, an agent key. Never a path, never a slug, never a position.
4. **Authorities and axes sit above the trees**, because works, concepts, agents, and axis values are not in any language. They have labels in languages; that is a different thing.
5. **Archive policy sits above the trees too.** The axis order, the root axis, the default policy, and the fallback order are properties of the archive and are declared once, in `archive.yaml`.

### Archive policy

```yaml
base: "https://example.org/"

axes:                           # the closed set, in canonical order
  - language
  - register

root_axis: language             # the one axis realised on the filesystem

key_separator: "__"             # joins values in derived keys, never in a path

default_coordinates: fill       # fill | unspecified

fallback:                       # which axis gives way first
  - register
  - language

variant_slug_policy: token      # token | free
variant_slug_separator: "-"
```

`key_separator` deserves a note, because it looks like the thing that was just removed. It is not a path convention. It joins coordinate values in derived keys, the cells of the coverage matrix, the keys of the UUID table, and the last segment of an expression IRI, none of which are filesystem paths and all of which need a canonical, greppable name for one cell of the coordinate space.

### Why authorities sit above

A single test decides it:

> **Does this thing have labels in more than one language?**
> If yes, it is an authority, and an authority cannot live inside a language tree without becoming scoped to that language, which destroys the thing it exists to do.

A **concept** has `prefLabel` in several languages; putting `concepts.yaml` inside `en-ca/` would make "practice standards" an English subject that French content happens to reference, which is the string-list failure SKOS was adopted to fix. An **agent** has a name that may be transliterated differently per language. An **axis value** has labels in every language by definition. All pass; none belongs inside a tree.

The principle underneath: **join keys must live above the things they join.** A key inside one of its own operands is a bug, whether the operand is a language tree or a database table.

### There is no work registry

There used to be one. It held a slug, a UUID, and a label map, and each of those turned out to be derivable or optional:

- The **slug** is not a work property at all. Each expression has one, `areas`, `domaines`, and they are equally the work's name; choosing one privileges a language. Scanning the archive collects all of them into a multilingual alias index for free.
- The **label** is optional. When a work's title never diverges from its expressions' titles, a work-level label duplicates them and adds a second place to drift. Resolution falls back to the expression title in the requested language.
- The **hierarchy** does not belong on the work. Where a text sits in the English organisation is an English fact, and the pairing that a work-level hierarchy was meant to provide already happens through work identity.

What is left is the UUID, and it is written in the front matter of every expression. A registry of bare UUIDs adds nothing that scanning the archive does not produce.

**The cost, stated plainly:** without a registry there is no closed set of works, so a mistyped UUID does not error, it mints a phantom work with exactly one expression, which is indistinguishable from a legitimately untranslated page. The mitigation is a scan-time report of single-expression works for review, not a structural guarantee.

### The expressions

**`en-ca/areas.md`**

```yaml
---
work: urn:uuid:8f7d1a92-3c04-4b1e-9f2a-6d5e8c0b7a41
subject: ["practice-standards", "service-areas"]
dcterms:
  title: Areas
  description: What we maintain an ongoing standard in.
  created: 2026-09-04
---
```

**`en-ca/areas-easy-read.md`**

```yaml
---
work: urn:uuid:8f7d1a92-3c04-4b1e-9f2a-6d5e8c0b7a41
coordinates:
  register: easy
translationOf: "en-ca"
subject: ["service-areas"]
dcterms:
  title: What we do
  created: 2026-09-05
---
```

**`fr-ca/domaines-lecture-facile.md`**

```yaml
---
work: urn:uuid:8f7d1a92-3c04-4b1e-9f2a-6d5e8c0b7a41
coordinates:
  register: easy
translationOf:
  language: en-ca
  register: easy
translator: "m-tremblay"
dcterms:
  title: Ce que nous faisons
  created: 2026-09-05
---
```

Two things to read off the pair. The same coordinate is spelled with each language's own token, and the French easy-read declares that it came from the English easy-read rather than the English standard, which is what lets drift follow the edge that actually exists.

**`fr-ca/domaines.md`**

```yaml
---
work: urn:uuid:8f7d1a92-3c04-4b1e-9f2a-6d5e8c0b7a41
translationOf: "en-ca"
translator: "m-tremblay"
subject: ["practice-standards", "service-areas"]
dcterms:
  title: Domaines
  description: Ce dont nous maintenons la norme au fil du temps.
  created: 2026-09-04
---
```

**One required field.** `work:` is the only thing that must be present, and it is the only thing that cannot be derived. Everything else is either descriptive or optional.

Top-level keys are **authoring inputs**, named for what they are; the `dcterms:` block holds **literal values** passed through unchanged; the `coordinates:` block holds **axis coordinates**. Mixing the three in one block is how you lose track of which is which.

**`translationOf` is a coordinate reference, never a path.** A bare string names the root axis, which covers the ordinary case of "translated from the English." A mapping names any axes, which is how a French easy-read expression records that it came from the English easy-read rather than the English standard.

```yaml
translationOf: "en-ca"                          # the English, at default register
translationOf: {language: en-ca, register: easy} # the English easy-read
```

Either form is completed with declared defaults and resolved by finding the same work's expression at those coordinates, so it never touches paths and is unaffected by the trees having different shapes. Omit it on originals.

**The UUID must be minted, never derived.** Not from a slug, not from a path, not from content. A UUIDv5 over the slug is reproducible and needs no thought, and it silently mints a different work the moment anything is renamed, which is precisely the event the identifier exists to survive. Generate v4 once, paste it, treat it as immutable. A one-line script removes the friction.

**Write the `urn:uuid:` form.** v0.0.1 wrote a bare UUID. SAT identifiers are `urn:uuid:` values, and parity costs nothing. A reader should accept both and normalise.

## The scan

Any change triggers a full rescan and rebuild. Incremental updates to a relationship graph are a cache, and invalidating that cache correctly across derived relations is where correctness goes to die.

Six passes, in order:

1. **Read**, parse axis and authority files, walk the trees, collect front matter, and take each expression's coordinates from its root segment and its `coordinates:` block. No resolution yet.
2. **Validate**, string types, coordinate sets against the declared axes, dangling concept and agent references, required fields, identity collisions. Fail here, before anything is built on bad input.
3. **Resolve**, coordinate keys to axis values and tags; mint expression identifiers from work UUID plus coordinates.
4. **Invert**, build the UUID table by grouping every expression by its `work:` value.
5. **Cascade**, walk each tree downward, applying section defaults where nothing overrides.
6. **Enrich**, git for `modified`, for rename history, and for drift.

The order is not arbitrary. Inversion after resolution, or it inverts unresolved keys. Cascade after inversion, or it cannot see the structure. Enrichment last, because it needs every expression identified and every `translationOf` resolved before it can compare a source against its derivatives. Within the read pass, front matter must be parsed before coordinates are assembled, since half of each coordinate set now lives there, and coordinates must be assembled before slugs, since the coordinates say which tokens the filename should carry.

### The UUID table

One grouping produces every relationship the archive has:

```
uuid → {
  expressions: { "en-ca__standard": path, "en-ca__easy": path, "fr-ca__standard": path },
  slugs:       { "en-ca__standard": ["areas"], "en-ca__easy": ["areas-easy"] },
  labels:      { "en-ca__standard": {tag, title}, "en-ca__easy": {tag, title} },
  coordinates: { "en-ca__standard": {language: {key, asserted}, register: {key, asserted}} },
  modified:    { "en-ca__standard": date, … }
}
```

Sibling lists, alias resolution, and coverage all fall out of it. Three properties matter:

**It is keyed by coordinate set, not by language.** v0.0.1 sketched `labels: {"en-CA": title}`. That is a one-axis assumption and it fails the first time a second axis exists: the standard and easy-read expressions both carry `en-CA`, and whichever the scan sees last silently wins. Anything in this table keyed by language has the same defect.

**It is a build artifact.** Deletable, regenerable, never hand-edited, never committed as truth. The archive is the source; this is a view.

**Nothing points down.** Expressions reference a work; the table is the inversion. This is why no registry is needed, the graph is fully described by its leaves, and adding an expression requires editing nothing else.

### Git holds the history

Renames, timestamps, and prior states are already recorded. Materialise what is needed at scan time, a slug-to-UUID redirect table for instance, rather than duplicating it into YAML where it can disagree with the repository.

Two caveats worth knowing. Git's rename detection is heuristic: a rename plus substantial edit in one commit reads as delete-plus-add. And shallow clones and squashed merges lose history entirely, which most CI configurations do by default. Neither is load-bearing, because identity lives in the UUID, so a rename that git failed to follow costs an old URL, not a work.

## Coverage

Two languages let you get away with assumptions that break at three, and one axis lets you get away with assumptions that break at two.

**Coverage is partial, and that is normal.** Not every work exists at every coordinate. Inverting `work:` across the archive handles this without special cases: a work gets whatever expressions exist. Nothing declares an absence, and no file needs a placeholder.

**Coverage is a matrix, not a list.** With one axis, "the other versions" is a list. With two, it is a grid that is mostly empty; three languages and two registers is six cells, of which perhaps two are filled. This is not a problem for the model, which never assumed otherwise, but it is a problem for any interface that presents variants as a flat list.

**Selection needs a fallback order, and the archive declares it.** A consumer asking for French easy-read when only French standard exists must know whether to fall back along the register axis or the language axis. That order is a property of the archive, so it is written in `archive.yaml` as an ordered list of axes, first to give way first, and the scan resolves against it. Axes relax fewest-first, and a relaxed axis tries its declared default before its other values. Reversing the list reverses which sibling a reader gets, which is exactly why it cannot be left to each consumer to guess.

**Defaults are filled, and what was asserted is recorded.** v0.0.1 framed this as a choice: complete every coordinate set from the declared defaults, which makes identity comparable but asserts something the author did not write, or leave unnamed axes unspecified, which is more honest but makes every query three-valued. It is not a choice. Identity uses the completed set, and each coordinate carries whether it was asserted or filled.

```json
"en-ca__standard": {
  "language": {"key": "en-ca", "asserted": true},
  "register": {"key": "standard", "asserted": false}
}
```

Comparability comes from the completed set; honesty comes from the flag. Nothing is lost either way, and a query that genuinely cares about the difference, an audit of which pages have had their register considered, for instance, can still ask.

**Do not hardcode the coordinate list.** Derive it from the axis files and the content present, so adding a variant adds a file and an axis value, and nothing else.

## Authored versus derived

Anything recoverable from position, an authority file, or version control should never be typed by hand. Hand-typed derivable data eventually disagrees with itself.

| Property | Source |
| --- | --- |
| `work` (UUID) | **Authored. The only required field, and the only underivable one** |
| `dcterms:title`, `description`, `created` | Authored, per expression |
| `coordinates` (non-root axes) | Authored where the expression is not at the default |
| `subject` | Authored as concept keys; labels resolved from `concepts.yaml` |
| `translationOf`, `translator` | Authored where applicable |
| `manifestations` | Authored, and only for embodiments that were authored |
| `openwemi:expresses` | The `work` UUID |
| Expression identifier | Derived: work UUID + coordinates |
| Root axis coordinate | The archive root the file sits in |
| Base slug | The filename or directory, with variant tokens stripped |
| Variant slug token | The axis value's `slug` for this language |
| Aliases | Path segments, collected across all trees |
| `dcterms:language` | Root coordinate resolved through `axes/language.yaml` |
| Register, modality, other axes | Declared coordinates resolved through their axis files |
| `openwemi:expressedBy` | Inverted from `work`, every sibling that exists |
| `dcterms:isPartOf` | Position in the tree, immediate parent only |
| `dcterms:modified`, rename history | Version control |
| Drift against a source | Derived: source blob then against source blob now |
| Roles (`marcrel:trl`) | Resolved from `translator` via `agents.yaml` |
| `publisher`, `rights`, `license`, `spatial` | Cascade from section defaults and archive configuration |
| `format`, manifestation type | Belongs to a rendering, not to the archive |

`isPartOf` is derived and never authored. Hierarchy is a property of an expression's position in its own tree, not of the work, since where a text sits in the English organisation is an English fact, and the cross-tree pairing that a work-level hierarchy would provide already comes from work identity.

Front-matter coordinates add one wrinkle to this. A variant can now have a parent that has no counterpart at its own coordinates: an easy-read child page in a section whose index page exists only at standard register. It parts to the parent that does exist in the same language, preferring the one nearest the declared defaults, which is the same fallback the rest of the archive uses rather than a special case.

## Validation: making "correct" checkable

Everything above is aspiration until something enforces it. **DCTAP** <a id="cite-dcmi-2022"></a>([DCMI, 2022](#ref-dcmi-2022)) states a profile as a table, which properties are required on which class, with what value type and cardinality, and converts to SHACL or ShEx for actual validation.

| shapeID | propertyID | mandatory | repeatable | valueNodeType |
| --- | --- | --- | --- | --- |
| Expression | work | true | false | literal |
| Expression | dcterms:title | true | false | literal |
| Expression | openwemi:expresses | true | false | IRI |
| Expression | coordinates.{axis} | false | false | literal |
| Expression | arc:slug | true | true | literal |
| ArchiveRoot | | true | true | literal |
| AxisValue | key | true | false | literal |
| AxisValue | label | true | true | literal |
| AxisValue | slug | false | true | literal |
| Manifestation | arc:path | true | false | literal |

This is what separates a modelled archive from a conventions document. Without it, "every expression must reference a work" is a sentence in prose that nothing checks; with it, the build fails.

v0.0.1 named four checks that matter more than the rest. There are nine, and every addition is a failure that is otherwise silent.

- **`work` parses as a UUID string.** Catches the transposed character before it becomes a phantom.
- **Axis keys and slugs are strings.** Catches YAML boolean coercion, which is invisible on inspection.
- **Coordinate sets resolve against declared axes.** Enforces the closed axis set, in the root segment and in `coordinates:` alike.
- **Slugs are unique within a tree, retired ones included.** A collision resolves to whichever the scan saw last.
- **One expression per work per coordinate set.** Two files carrying one work at one coordinate set collapse into one cell of the table, and one of the two pages simply stops existing. Nothing in v0.0.1 caught this, and the move to front-matter coordinates makes it likelier, since the two files now sit in one directory rather than in separate trees.
- **The root axis does not appear in front matter.** Two sources of truth for one coordinate, and no rule for which wins.
- **An axis name does not appear at the top level of front matter.** `register: easy` written outside the `coordinates:` block is the likely authoring mistake, and without this check it parses cleanly as a descriptive property and the expression quietly takes the default register.
- **The filename and the coordinates agree.** In both directions: a coordinate whose token the filename does not carry, and a token in the filename that no coordinate declares. The second is the one that matters, because a file named `notes-easy-read.md` with no coordinates publishes as standard register under a name that says otherwise.
- **A declared manifestation exists.** Declaring an embodiment is an assertion that someone authored it. A path that resolves to nothing is either a typo or a file that was never committed, and both are worth failing on.

Two more checks report rather than fail, because what they find may be correct. A work with a single expression may be a phantom or may be an untranslated page. A stale translation may need revising or may be fine.

## Decisions settled

v0.0.1 left five decisions open and v0.0.2 closed three. The rest are closed here, along with one that turned out not to be a decision at all. The reasoning is recorded so that reopening any of them is a deliberate act.

**Coordinate encoding in paths** (v0.0.2). Withdrawn rather than answered. Only the root axis is realised on the filesystem, so there is nothing to encode.

**Default coordinates** (v0.0.2). Filled from the declared defaults, with `asserted` recorded per coordinate. The tradeoff was real and the framing was wrong; both properties are available at once.

**Fallback order across axes** (v0.0.2). Declared in `archive.yaml` as an ordered list, resolved by the scan. Consumers ask for coordinates and are told what gave way.

**Does Manifestation become a real level?** Yes, for authored embodiments, and never for generated ones. See "When Manifestation becomes real". The line is checkable, and an archive that authors no embodiments pays nothing for the level.

**Slug policy for variants.** A non-default coordinate declares a slug token per language in its axis registry, and the filename carries it. The base slug survives, the coordinate stays the source of truth, and the two are checked against each other. `variant_slug_policy: free` turns the convention off for archives that do not want it.

**The slug of a page at a tree root.** Not a decision. The slug path is empty and the page is addressed at the language root, the same as in any other language and the same as everywhere else on the web. v0.0.2 raised this in error.

**Should `translationOf` carry a versioned source?** No. Git versions everything already, so drift is a checksum comparison rather than an authored field. A recorded digest survives only as a fallback for archives whose history is unreliable.

The decisions v0.0.1 settled before all of this, that there is no registry, that hierarchy is positional and derived, and that a directory gets a file when it is a page, stand unchanged.

## Open decisions

**Do work-level labels come back?** Removing the registry removed the only place a work-level title could live. If a work ever needs a name that none of its expressions use, there is nowhere to put it. Probably acceptable; worth revisiting if it bites.

**What describes a manifestation?** An authored embodiment currently carries a path, a media type, and a note. A Braille edition with its own pagination, or a print PDF with its own typesetting, has properties of its own that nothing yet models. Enough exists to record that the embodiment is authored and where it is; nothing exists to describe it.

**What does a build do with a stale translation?** Drift is now detected and reported. Whether a stale expression is published, published with a notice, held back, or fails the build is a policy the archive should declare, in the same place and for the same reason the fallback order is declared.

**Does a coordinate-scoped section want a mechanism?** Coordinates do not cascade, and a large easy-read or plain-language section pays for that in repetition. A declaration that named the resources rather than the position, an authored list rather than an inherited value, would keep identity off the filesystem while removing the repetition. Whether that is worth a second mechanism, or whether the authoring tool is the right place for it, is not decided.

## Accepted costs

These were listed as known issues in v0.0.1. On review they are consequences of decisions taken deliberately, or notes about tooling, rather than defects in the model. They are recorded so that a future reader does not mistake them for oversights, or try to fix them without knowing what they are trading away.

**UUIDs in front matter are hostile to hand-authoring.** They cannot be typed from memory, cannot be checked by eye, and a transposed character produces a valid-looking phantom. This is the price of an identifier that survives every rename, which is the property the whole design rests on. A mint-and-insert script is not optional in practice, and with one the cost is a keystroke.

**YAML 1.1 boolean coercion.** `no` (Norwegian), `y`, `on`, and `off` become booleans; bare numeric slugs become integers. This is a defect in a parser, not in the archive, and it is fully mitigated by the three defences in "Quoting is not optional", two of which are mechanical. It stays on the list only because a toolchain that silently reverts to a 1.1 parser will fail silently.

**Axis proliferation.** Nothing structurally limits the number of axes, and each one multiplies the coordinate space; three axes of three values each is twenty-seven possible cells. The closed axis set is the brake, and it is a policy rather than a mechanism, deliberately. A mechanism here would be a limit on what the archive is allowed to describe, which is the wrong thing to enforce in a format.

**A coordinate is repeated on every resource that holds it.** No inherited value can shorten a section of forty easy-read pages, because coordinates deliberately do not cascade. The repetition is what makes moving any one of those files safe, and supplying it is an authoring-tool concern rather than a modelling one.

**Cascade is per-tree.** Section defaults applied in `en-ca/about/` do not reach `fr-ca/a-propos/`, so shared defaults that are not archive-wide are authored once per language. This is the price of hierarchy being positional, and positional hierarchy is what lets each language tree be organised for its own readers. The cost is smaller than it was in v0.0.1: defaults now reach every variant within a language, because variants are no longer in trees of their own.

**Git rename detection is heuristic.** A rename combined with substantial edits reads as delete-plus-add, and shallow clones lose history altogether. Not load-bearing for identity, which lives in the UUID, but old URLs will occasionally stop resolving.

**schema.org and BIBFRAME lose the Expression level.** Both fold expression into work. The emitted view is lossy by construction, and that is what a view is for.

## Known issues

What is left: things that can still produce a wrong archive, where the mitigation is partial or absent.

**No closed set of works.** A mistyped UUID mints a phantom work rather than raising an error, and a phantom is indistinguishable from a legitimately single-expression work. Mitigated by a scan-time report of single-expression works for review, not prevented. This is the one genuine hole left by removing the registry, and it is the reason the report exists.

**Drift detection can clear itself falsely.** The comparison is anchored to the translation's last commit, so a later edit that has nothing to do with the source, a typo fix, a metadata change, moves the baseline forward and reports the translation as current when its content is still stale. Anchoring to the last commit that touched the body rather than the file would narrow this, and would need a content hash of the body rather than the blob.

**Drift detection needs real history.** Shallow clones and squashed merges lose the comparison, and most CI configurations produce one or the other by default. The failure is quiet: no drift is reported because none can be computed. A recorded digest is the fallback, at the cost of a field that can itself go stale.

**Slug uniqueness is only as good as the history.** The check covers retired slugs recovered from git, so it inherits the same rename heuristic and fails open under shallow clones. A collision that git failed to surface resolves to whichever file the scan saw last, silently.

**Coverage has no notion of "should exist".** Absence is not declared, which is what makes partial coverage cost nothing. The other side of that is that a translation nobody ever commissioned and a translation that was commissioned and never delivered are the same shape in the archive: nothing.

## References

<a id="ref-coyle-2022"></a>Coyle, K. (2022). Works, expressions, manifestations, items: An ontology. *The Code4Lib Journal*, (53). https://journal.code4lib.org/articles/16491 [↩](#cite-coyle-2022)

<a id="ref-coyle-2025"></a>Coyle, K. (2025). OpenWEMI: A minimally constrained vocabulary for work, expression, manifestation, and item. *The Code4Lib Journal*, (60). https://journal.code4lib.org/articles/18412 [↩](#cite-coyle-2025)

<a id="ref-davis-2005"></a>Davis, I., & Newman, R. (2005). *Expression of core FRBR concepts in RDF*. http://vocab.org/frbr/core.html [↩](#cite-davis-2005)

<a id="ref-dcmi-2022"></a>Dublin Core Metadata Initiative. (2022). *Dublin Core tabular application profiles (DCTAP)*. https://www.dublincore.org/specifications/dctap/ [↩](#cite-dcmi-2022)

<a id="ref-dcmi-2024"></a>Dublin Core Metadata Initiative. (2024). *OpenWEMI specification*. https://www.dublincore.org/specifications/openwemi/specification/ [↩](#cite-dcmi-2024)

<a id="ref-lebo-2013"></a>Lebo, T., Sahoo, S., & McGuinness, D. (Eds.). (2013). *PROV-O: The PROV ontology*. W3C. https://www.w3.org/TR/prov-o/ [↩](#cite-lebo-2013)

<a id="ref-miles-2009"></a>Miles, A., & Bechhofer, S. (Eds.). (2009). *SKOS simple knowledge organization system reference*. W3C. https://www.w3.org/TR/skos-reference/ [↩](#cite-miles-2009)

<a id="ref-phillips-2009"></a>Phillips, A., & Davis, M. (Eds.). (2009). *Tags for identifying languages* (RFC 5646). Internet Engineering Task Force. https://www.rfc-editor.org/rfc/rfc5646.html [↩](#cite-phillips-2009)

<a id="ref-riva-2017"></a>Riva, P., Le Bœuf, P., & Žumer, M. (2017). *IFLA library reference model: A conceptual model for bibliographic information*. International Federation of Library Associations and Institutions. https://repository.ifla.org/handle/123456789/40 [↩](#cite-riva-2017)

<a id="ref-tillett-1991"></a>Tillett, B. B. (1991). A taxonomy of bibliographic relationships. *Library Resources & Technical Services*, *35*(2), 150–158. [↩](#cite-tillett-1991)

### Further resources

**Models**
- LRMoo 1.0, https://cidoc-crm.org/lrmoo
- WEMI (LINCS), https://portal.lincsproject.ca/docs/terms/wemi

**Vocabularies**
- OpenWEMI namespace, https://ns.dublincore.org/openwemi/
- DCMI Metadata Terms, https://www.dublincore.org/specifications/dublin-core/dcmi-terms/
- MARC Relators, https://id.loc.gov/vocabulary/relators/
- RDA Registry, https://www.rdaregistry.info/

**Language identification**
- IANA Language Subtag Registry, https://www.iana.org/assignments/language-subtag-registry/
- ISO 639-3 code set, https://iso639-3.sil.org/
- Glottolog, for languoids without ISO codes, https://glottolog.org/

**Practice**
- Linked Open Data (LINCS), https://portal.lincsproject.ca/docs/terms/linked-open-data

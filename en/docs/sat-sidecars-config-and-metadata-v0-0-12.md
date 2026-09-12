# SAT Sidecars: Config and Metadata

**Version.** v0.0.12, 2026-09-10. Supersedes v0.0.11.

**Scope.** The two sidecar trees a SAT node carries, side by side. Config is presented first because it is further along, and the metadata tree is specified against it so the differences are visible rather than inferred.

## Changes in this version

Everything here came from reading the configuration cascade specification and asking what carries across and what does not.

- **Three state questions answered from config.** `resolved/` materialises at every node, a node with nothing to say still resolves, and `resolved/` at one node equals `defaults/` at the next.
- **One resolver, not two.** Config states it and this document now says it plainly: the trees differ in path shape, not in what composition does.
- **Added a field-kind table for metadata,** parallel to config's. This is the substantive addition, and it is where the two trees genuinely diverge.
- **Added accumulating fields.** `subject` unions with what it receives rather than replacing it, using the `merge` key config already proposes for list-valued fields.
- **Seeding is inverted for metadata,** and derived values are proposals an editor confirms.
- **Field kinds are declared in configuration,** not built into the resolver, so a namespace can be added without a code change.
- **Every namespace materialises at every node,** which configuration already settled and this document had left open.
- **Identity is minted, not seeded.** The authority to mint cascades by role.
- **`status` is carried and reported, with no behaviour behind it** for now.
- **The subject chain includes the archive,** as a prompted proposal like every other inherited subject.
- **Accumulating fields are rows keyed by role,** each item carrying its own `overridable`. This replaces the earlier flat list and its `merge: append` rule, which could not express provenance.
- **A tier may place a value in a row below its own,** which is how delegation is stated. The row is the target; no targeting syntax is needed for placement.
- **`status: deprecated` removes an item from the resolved set** while keeping it in the record. This is `status`'s first behaviour, and it supersedes the earlier ruling that nothing conditions on it.
- **`resolved/` records who amended an item,** not only who holds it.
- **Reviving a deprecated item is an amendment,** so only a role above the one that deprecated it may do so.
- **Authority is administrative rather than monotonic.** Locking and deprecation are the same kind of act, and the earlier description of a lock as advisory is withdrawn.
- **Editorial.** Contrasts with earlier drafts of this document are removed from the body. Contrasts with configuration, with slug-derived subjects, and with front matter remain, because those explain the product rather than the drafting.
- **A higher role may amend a lower row,** including unlocking what a lower tier locked and sending a decision back for reconsideration. This departs from configuration's monotonic rule, deliberately.
- **Organizing directories are permitted anywhere and hold no archived content.** The earlier rule scoped them to the SAT instance, which forbade a legitimate and useful case.
- **Organizing directories are scoped to the SAT instance,** and never appear inside a collection or an archive. Added a section on interface translations, which are software resources rather than archived content.

**Note on `{node}`.** Both trees use `{node}` where earlier drafts used `{level}`. The vocabulary already defines *node name* as exactly what that segment holds, and *level* was a leftover from the walkthrough drafts, where it described a rung in the cascade rather than a name on disk. The rename lands here in one pass across both trees.

## The shape they share

```
config     .{node}.assets/{author}/config/{subject}/{state}/config.yml
metadata   .{node}.assets/{author}/metadata/{namespace}/{state}/{namespace}.yml
```

Four things hold in both:

- the sidecar is named for the node it belongs to
- `{author}` is the tier that wrote this layer, and the only role that edits it
- `{state}` is the last directory before the file
- the filename echoes the directory above it

One thing differs, and it is the third segment. Config varies by **subject**, the role the material is addressed to. Metadata varies by **namespace**, the vocabulary the material is written in.

That difference is not an inconsistency to be resolved. It follows from what each tree holds, and the next two sections say why.

## Config

Configuration is prescriptive. It is instructions, and instructions can legitimately be aimed at a tier: "archives use this ignore list" is a different statement from "directories use this one." The subject axis is what carries that aim.

| Segment | Meaning | Drawn from |
| --- | --- | --- |
| `{node}` | The name of the node the sidecar belongs to: a directory name, or a file name with its extension | The filesystem |
| `{author}` | The tier that wrote this layer of the cascade | The role vocabulary |
| `{subject}` | The role the material is addressed to | The role vocabulary |
| `{state}` | `defaults/`, `overrides/` or `resolved/` | Fixed set of three |

Worked examples:

| Path | Node | Author | Subject |
| --- | --- | --- | --- |
| `sat/.sat.assets/sat/config/collection/defaults/config.yml` | `sat`, the root directory | `sat` | `collection` |
| `en-ca/.en-ca.assets/archive/config/directory/overrides/config.yml` | `en-ca`, a directory node holding the archive role | `archive` | `directory` |
| `.report.md.assets/content/config/content/resolved/config.yml` | `report.md`, a file node | `content` | `content` |

The third example shows the subject axis at its narrowest. A content node is a leaf, so it can address only itself.

## Metadata

Metadata is descriptive. A node's `dc.yml` says what that node is. A collection's `publisher` is not addressed to archives rather than to directories; it is simply the collection's publisher, and descendants inherit what they do not state themselves. There is no coherent sense in which descriptive metadata is aimed at one downstream role, so metadata has no subject axis.

It has an axis config does not, because it speaks more than one vocabulary. Config speaks one vocabulary to several audiences. Metadata speaks several vocabularies to one.

| Segment | Meaning | Drawn from |
| --- | --- | --- |
| `{node}` | The name of the node the sidecar belongs to: a directory name, or a file name with its extension | The filesystem |
| `{author}` | The tier that wrote this layer of the cascade | The role vocabulary |
| `{namespace}` | The metadata vocabulary: `dc`, `dcterms`, `sat` | The namespace set |
| `{state}` | `defaults/`, `overrides/` or `resolved/` | Fixed set of three |

Worked examples, matching the config set above:

| Path | Node | Author | Namespace |
| --- | --- | --- | --- |
| `sat/.sat.assets/sat/metadata/dc/defaults/dc.yml` | `sat`, the root directory | `sat` | `dc` |
| `en-ca/.en-ca.assets/archive/metadata/dc/overrides/dc.yml` | `en-ca`, a directory node holding the archive role | `archive` | `dc` |
| `.report.md.assets/content/metadata/sat/overrides/sat.yml` | `report.md`, a file node | `content` | `sat` |

The third example shows where work identity lives. It is the one thing a multilingual archive cannot do without, and it is the one thing the current ingress fixture does not carry.

## Sidecar layout

Every role folder at every node carries a three-state directory set, per namespace:

```
.{node}.assets/
  {role}/
    metadata/
      dc/
        defaults/dc.yml     # read-only, received from the node above
        overrides/dc.yml    # writable, the only hand-edited file
        resolved/dc.yml     # read-only, generated locally
      sat/
        defaults/sat.yml
        overrides/sat.yml
        resolved/sat.yml
```

The state lives in the directory name and the filename is the namespace, so `metadata/dcterms/` can sit alongside `dc/` and `sat/` later with its own three states and no change to the grammar.

Namespaces are independent. A node may carry `dc/` and not `sat/`, or both. Each cascades on its own, and nothing in one namespace resolves against another.

## Author is the tier that wrote the layer

Metadata cascades exactly as configuration does, through the role order:

```
sat  ->  collection  ->  archive  ->  directory  ->  content
```

`{author}` names which tier wrote a given layer. A value set at `sat` with `overridable: true` descends to the collection, which may take it as received or write its own and pass it on, and so down to the content node. `overridable: false` at any tier closes the field to every tier below.

So a directory node does receive values authored by the collection above it. Nothing is hidden from a node because it does not hold the authoring role, and there is no access boundary here: `{author}` records which rung wrote a layer, not who is allowed to see it.

"The role that created it is the role that edits it" describes the write side. A collection's material is written in the collection's own `overrides/`, and a directory wanting a different value writes its own rather than reaching up and editing the collection's. That keeps each tier's stated intention intact when the archive moves, which is the same reason an override held against a locked field is marked inert rather than deleted.

A multi-role node writes one layer per role it holds, and those layers resolve in role order, the same order the cascade uses between nodes.

## Field kinds

Config classifies its fields three ways and notes that only the third uses `overridable` meaningfully:

| Kind | Example | Behaviour |
| --- | --- | --- |
| Vocabulary | `roles` | Declared once at `sat`, never overridable |
| Structural | `children` | Locked, because a tier does not redefine what it may contain |
| Behavioural | `default_metadata` | Cascading by design, delegated downward unless locked |

That classification works because every configuration field originates at the root and descends. The cascade is the whole story.

Metadata is the other way round. Most Dublin Core elements originate at the leaf and describe only the node that states them, so the same three kinds do not fit and metadata needs its own table:

| Kind | Example | Behaviour |
| --- | --- | --- |
| Contextual | `publisher`, `rights`, `language`, `creator` | Cascades by design, delegated downward unless locked |
| Accumulating | `subject` | Unions with what it receives rather than replacing it |
| Local | `title`, `description`, `date`, `type`, `format` | Belongs to the node. Never received, never seeded from above |
| Identity | `identifier`, `isVersionOf` | Local, and additionally unique to the node |

Of the fifteen elements, four or five descend and ten do not. A `defaults/dc.yml` at a content node holds `publisher`, `rights`, `language` and little else.

`[D]` **A field's kind is declared in configuration, not built into the resolver.** It is a vocabulary field in configuration's sense: declared once at `sat`, never overridable, the same class as `roles`.

```yaml
# config/sat/defaults/config.yml
field_kinds:
  value:
    dc:
      publisher: contextual
      rights: contextual
      language: contextual
      creator: contextual
      contributor: contextual
      subject: accumulating
      title: local
      description: local
      date: local
      type: local
      format: local
      identifier: identity
    sat:
      identifier: identity
      isVersionOf: identity
      slug: local
      order: contextual
  overridable: false
```

The resolver knows about kinds and not about Dublin Core. Adding `metadata/dcterms/` is then a declaration rather than a code change, which is the property that makes the namespace layer worth having at all.

A field with no declared kind is an error rather than a default. Guessing would make a typo in an element name behave like a new local field, silently.

**Local fields must not be received, and the failure is silent.** If the resolver applies `defaults` plus `overrides` uniformly, a directory node whose resolved title is `"wellbeing"` passes that title down as the content node's default, and a resource whose own title was never stated publishes as "wellbeing". The archive builds, the page renders, and the title is wrong. Nothing about this shows in an archive where every node happens to state its own title, which is a convention holding up a mechanism.

### Accumulating fields

`subject` is the case where the filesystem carries meaning worth keeping. A resource at `wellbeing/practices/meditation` sits under two ancestors that each say something about what it is about, and a subject set of `[wellbeing, practices]` is a better description than an empty one.

`[D]` **An accumulating field is a list of fields, not a field with a list value.** Each item carries the standard shape, so `overridable` and `status` apply per item and no new keys are invented:

```yaml
subject:
  - value: "urn:uuid:...governance-policy"
    overridable: false
  - value: "urn:uuid:...health-services"
    overridable: true
```

### Rows record who decided

`[D]` In `overrides/`, a tier may write rows keyed by role. Writing under a role is the delegation, and no targeting syntax is needed for it:

```yaml
# the sat instance's overrides/dc.yml
subject:
  sat:
    - value: "urn:uuid:...governance-policy"
      overridable: false          # sat holds this; no tier below changes it
  collection:
    - value: "urn:uuid:...health-services"
      overridable: true           # handed down; the collection holds it now
  archive:
    - value: "<notset>"           # the archive is prompted to decide
```

A tier writes rows at or below its own rank. The row says which tier holds the item, `overridable` says whether the holder may pass it further, and `<notset>` says a tier has been asked and has not answered.

`resolved/` carries the same keying, so an editor opening any node sees which tier decided what without running a resolver.

Without rows, a subject stated deliberately by an organisation two tiers up and a subject proposed from the path arrive in one list, indistinguishable. A lower editor is then prompted to confirm decisions already made above, and nothing can tell the two apart afterwards.

### Amendment reaches into a lower row

Placement covers stating, locking, delegating and prompting. It cannot change an item a lower tier already holds, because an item is identified by its value and a reset replaces that value with `<notset>`, leaving nothing to match on.

`[D]` **A higher role may amend any row below its own**, and amendment is written distinctly because it is a distinct act:

```yaml
# the sat instance's overrides/dc.yml
amend:
  collection:
    subject:
      - match: "urn:uuid:...legacy-taxonomy"
        overridable: true         # unlock what the collection locked
      - match: "urn:uuid:...deprecated-topic"
        value: "<notset>"         # send back for reconsideration
```

A `match` that finds nothing is an error rather than a silent no-op, on the same grounds as any dangling reference: a stale amend pointing at an item already removed should be reported.

**This departs from configuration's monotonic rule, and the departure is deliberate.** Configuration allows `overridable` to narrow and never widen, so authority only ever tightens as it descends. Metadata allows a higher role to widen what a lower one narrowed, because an instance administrator has to be able to correct a department that over-locked, and a department has to be able to correct its own archives.

Two consequences follow, and neither should be discovered later.

**Resolution is two operations, not one.** A value still cascades downward, last writer wins. A flag resolves by role rank, because a higher tier must win over a lower one that already narrowed. A resolver implements both.

**Authority is administrative.** Each role binds every role below it and is bound by every role above it. That is the whole rule, and both `overridable` and `status` obey it.

A collection's lock binds the archive, the directory and the content node, and a higher role may lift it. A collection's deprecation binds exactly the same tiers, and a higher role may revive. The two behave identically, and neither is weaker than the other for being revisable from above.

That anything set by one role can be changed by a role above it is what an administrative hierarchy means, not a gap in it. A person working on an administered system knows the administrator can change what they were given, and their own settings are not thereby advisory: the settings hold, for them and for everyone below them, until someone with the standing to change them does.

A consumer may rely on the resolved state as it stands, and may not assume it is permanent. Both halves are ordinary.

**This is where metadata departs from configuration.** Configuration's authority is monotonic: it only ever tightens going down, and no tier can loosen what another tightened. Metadata's authority is hierarchical: it tightens or loosens according to rank, because an administrator has to be able to correct a subordinate. Monotonic authority is simpler to reason about and cannot express governance, which is the trade being made.

### Removal is not reset

`<notset>` means nobody has decided, which is what drives the prompt. Resetting an item to it therefore means reconsider, and an editor is asked again.

`[D]` **An item a tier wants gone is marked `status: deprecated`.** It stays in the record, showing that a decision was made and by whom, and it is excluded from the resolved set a consumer receives.

```yaml
amend:
  collection:
    subject:
      - match: "urn:uuid:...deprecated-topic"
        status: deprecated        # gone from the resolved set, kept in the record
      - match: "urn:uuid:...legacy-taxonomy"
        value: "<notset>"         # sent back for reconsideration
```

Without the distinction a rejected subject is re-proposed on every rebuild, because nothing separates "nobody has decided" from "someone decided against it".

`[D]` **Reviving is itself an amendment.** Clearing `status: deprecated` is a change to an item a tier already holds, so it follows the same rule as any other amendment: only a role above the one that deprecated it may make it. A tier cannot revive what a higher role removed, which is what makes deprecation a governance act rather than a suggestion.

A tier that deprecated an item may of course revive it, since amendment reaches its own row.

```yaml
amend:
  collection:
    subject:
      - match: "urn:uuid:...deprecated-topic"
        status: available         # revive; only a role above the deprecating one
```

Deprecation therefore behaves exactly as locking does: binding on every role below the one that set it, revisable by every role above. Neither is an exception to the other.

### Amendment is recorded

`[D]` **`resolved/` records who amended an item, not only who holds it.** A governance mechanism whose interventions leave no trace cannot be audited, and after `sat` unlocks something in the collection's row the collection still holds it while `sat` changed it. Both facts matter.

```yaml
# resolved/dc.yml
subject:
  collection:
    - value: "urn:uuid:...health-services"
      overridable: true
      amendedBy: ["sat"]
```

`amendedBy` lists the roles that have amended the item, in the order they did so. It appears only in `resolved/` and is never written by hand: an editor states intentions in `overrides/` and the resolver records what it applied.

**It is current state, not a log.** The resolved file says who has amended an item, not when, not what the previous value was, and not why. Version control holds that, with timestamps and authorship already, and duplicating it into the archive would put the same history in two places where only one of them is reliable.

**Ancestor works, not ancestor slugs.** Directory names are chosen for URLs rather than as index terms, so `terms-of-service` would arrive as a subject and so would `2024`. Worse for a multilingual archive, the two language trees produce disjoint sets for one work: English `wellbeing/practices/meditation` yields `[wellbeing, practices]` and French `bien-etre/pratiques/meditation` yields `[bien-etre, pratiques]`, so nothing can answer "everything about wellbeing, in any language".

Each ancestor directory is a node with its own index resource, and those resources are expressions of works. `wellbeing/index.md` and `bien-etre/index.md` carry the same `isVersionOf`, so the path already resolves to a language-independent chain of work identifiers. Accumulating those gives both language versions the same subject set, with display labels taken from each ancestor's own title in the reading language.

That produces what SKOS concepts would: an identifier with labels per language. It arrives without a concept registry, because section index resources are already doing that work.

**A consequence for organizing directories,** which the next section states as a rule.

## Organizing directories

Configuration defines an organizing directory as one carrying no sidecar: not a node, holding no role, which the cascade steps through as though it were not there.

`[D]` **An organizing directory may appear anywhere, and holds no archived content.** The constraint is what is in it, not where it sits.

This is an accommodation rather than a restriction. An archive holds described resources, and every working collection also has material that is not one: it exists, it belongs with the archive, and it is not the archive. Giving it a home is better than the alternatives, which are to describe material that does not warrant description, or to keep it outside the archive entirely, where it goes missing.

What belongs in one:

- `bin/` and `lib/`, the software of a SAT instance
- `messages/`, catalogs translating that software's strings
- binaries and compiled artifacts
- material staged for ingress, before it becomes archived content
- scans and original captures, where the archived resource is derived from them
- databases and exports feeding an ingress process
- working files and drafts that are not yet, and may never be, resources

The last three are the common case in a user collection. Material waiting to be ingressed is not yet described, and forcing a node onto it would assert a description nobody has written.

**The one thing that does not belong beneath an organizing directory is archived content.** A resource there would sit in a path where a directory contributes no work identifier, so its subject chain silently loses a link and two resources at different depths acquire the same subjects. A reader reports a content node found beneath a directory with no sidecar, and that single check enforces the whole rule.

Nothing else needs checking. The material in an organizing directory does not participate in the cascade, so the cascade has nothing to say about it.

### SAT's own documentation is archived content

`sat/en/` is a language archive inside the SAT instance, holding SAT's documentation. It is content, it has works and expressions, and every rule in this document applies to it exactly as to a user's archive.

`sat/en/messages/` sits beside it and is an organizing directory. Documents and catalogs live in one language scope without interacting, because the catalogs are not archived content and nothing beneath them participates in the subject chain.

## Interface translations are not archived content

A message catalog is not a translation of a document. It is a lookup table keyed by source string, and it does not realise a work.

The distinction is already in the configuration vocabulary: `interface_language` is a separate field from a resource's `language`, because they answer different questions. The file layout follows the same split.

Catalogs live inside the organizing directory that holds the software, with no sidecars, no works, and no Dublin Core:

```
lib/
  locale/
    en-ca/LC_MESSAGES/sat.po
    fr-ca/LC_MESSAGES/sat.po
    sat.pot
```

A path like `en-ca/bin/example.po` would invert the relationship, putting software inside a language archive when the instance contains the archive rather than the other way round, and would imply each catalog is an expression of a work.

The argument for leaving them out of the work model is more than tidiness. Gettext already solves what the work model would have to rebuild: `msgmerge` handles a source string changing, `.pot` is the template, and fuzzy matching flags entries needing review. That is translation drift machinery, mature and specific to message catalogs, and reimplementing it would tangle two kinds of translation that behave differently.

Documentation *about* SAT's interface languages is a different thing. That is archived content and belongs in `sat/en-ca/` like any other document. The line falls between the strings themselves and writing about them.

## Seeding

Configuration seeds `overrides/` once at init with the overridable fields a node received, so a locked field is never written into the one writable file and never invites an edit that resolution would discard.

Metadata inverts the useful half of that. Seeding a content node with the `publisher` and `rights` it has no reason to change fills the file with noise, while the fields it actually needs, `title` and `date`, are absent because nothing above declared them. Local fields are what a content node writes, and they are exactly the ones a received-fields seeding rule would omit.

Identity is the exception. `identifier` is not seeded as `<notset>`, because a UUID is not something an editor types. It is minted when the node is created, by the role that creates it.

`[D]` **The authority to mint cascades by role.** `sat` mints for `sat`, then passes its requirements and defaults to `collection`, which mints collections; `collection` passes to `archive`, and so down. Minting is delegated exactly as any other behavioural field is, so identity is the one local field that arrives with a value rather than a sentinel.

Everything else local seeds as `<notset>`, and derived values seed as proposals:

```yaml
title:
  value: "<notset>"
subject:
  value: ["urn:uuid:...wellbeing-work", "urn:uuid:...practices-work"]
  merge: append
```

`[D]` The chain includes the archive itself. `en-ca/wellbeing/practices/meditation` has `en-ca` as an ancestor node with a work, and it accumulates like any other. Whether that is useful or noise is a judgement each archive makes, so it arrives overridable at every role and an editor confirms or removes it.

A derived subject chain is a proposal rather than a fact. An editor is prompted to confirm or amend it, which is the same prompting `<notset>` already drives in configuration. Whether a leaf includes itself in its own subject set is a case for that prompt rather than a rule: sensible for `meditation.md`, whose title is its topic, and wrong for `privacy-policy.md`, whose subject is privacy rather than the policy.

## Every namespace materialises at every node

Configuration settles this and it carries over without change: every role folder at every node carries a three-state directory set, and resolution does not care whether anything was edited. So a node materialises every declared namespace, whether or not it authors anything in one.

A content node therefore has `sat/defaults/`, `sat/overrides/` and `sat/resolved/` even though both of `sat`'s identity fields are local to it. Its `sat/defaults/sat.yml` is empty, correctly: nothing above it has anything to pass down.

An empty `defaults/` is not a missing one, and a reader must not treat the two alike. Absent means the namespace was never declared. Empty means it was declared and nothing descended into it.

## Namespaces

**`dc`** is Dublin Core 1.1, the fifteen elements in the `/elements/1.1/` namespace. Every element is optional and every element is repeatable, so values are lists.

**`dcterms`** is DCMI Metadata Terms, the later and larger vocabulary with domains and ranges declared. Not interchangeable with `dc`: `dc:date` and `dcterms:date` are different properties. Reserved, not yet used.

**`sat`** holds what SAT needs and DC has no word for. Where DCTERMS has a counterpart term the `sat` property takes its local name, and SAT coins a term only for what DCTERMS cannot say.

At a content node, `sat` carries `identifier`, the resource's own `urn:uuid`, and `isVersionOf`, the `urn:uuid` of the work it realises. Two expressions of one work carry the same `isVersionOf` and different `identifier` values. That is the entire mechanism by which a translation is a translation: not matching titles, which differ, and not matching paths, which also differ.

## Identity does not cascade

Everything else in the metadata tree descends by default. Identity must not, and this is a hard exclusion rather than a default that can be overridden.

**`identifier`** names one resource. A child inheriting its parent's identifier would claim to be its parent.

**`isVersionOf`** names the work a resource realises. A child inheriting it would become an expression of its parent's work, which would make a section index and every document beneath it translations of each other. The failure is silent: the archive would build, the switcher would render, and every link would be wrong.

Both are stated at the node they belong to, in that node's `overrides/`, and never received from above. A resolver walking the metadata cascade excludes them from the merge rather than relying on every node to restate them.

The same reasoning applies to any field that names one resource rather than describing a class of them.

## Field shape

A metadata field carries its value and the authority that governs it, in the same shape configuration uses:

```yaml
# .areas.md.assets/content/metadata/dc/overrides/dc.yml
title:
  value: ["Areas"]
  overridable: true
description:
  value: ["What we maintain an ongoing standard in."]
  overridable: true
```

`overridable` is monotonic. It may narrow from true to false at any node and never widen, so a value locked above cannot be reopened below.

`status` records where a field or an item sits in its lifecycle, so new things can be introduced and old ones retired without a version break.

`[D]` `deprecated` has behaviour. A deprecated item stays in the record and is excluded from the resolved set a consumer receives. This supersedes an earlier ruling that nothing conditions on `status`, and is noted here because an implementation written against that ruling will need changing. The change is confined to this one value.

`[D]` `planned` has none. A resolver records it and passes it through, and nothing acts on it. That remains deliberate.

An override held against a field locked upstream is reported and marked inert rather than deleted, so an archivist's stated intention survives a migration that later unlocks the field.

## Quoting

Language keys and slugs are quoted, always. Under YAML 1.1 `no` is both a boolean and the ISO 639-1 code for Norwegian, so an unquoted Norwegian key parses as `false` with no error and nothing visible in the file. `y`, `on` and `off` behave the same way, and a bare numeric slug parses as an integer and stops matching the string it names.

Parse as YAML 1.2, which dropped that boolean set. Node's `yaml` and `js-yaml` v4 are safe by default; PyYAML is not.

## States

Three things carry over from configuration unchanged, and are stated here so a reader of this document alone does not have to infer them.

`resolved/` materialises at every node. `resolved/` at one node and `defaults/` at the next hold the same content, which makes the cascade inspectable at every node without running a resolver and reduces generating a child's defaults to a copy rather than a merge.

A node with nothing to say still resolves. Resolution does not care whether anything was edited: with no edits, `resolved/` equals `defaults/`.

`defaults/` and `resolved/` are both read-only and are not the same kind of artifact. `defaults/` is received input and must be preserved. `resolved/` is derived output, safe to delete, and always rebuildable from the two files beside it.

## One resolver

Configuration and metadata are composed by the same operation: read `defaults/`, read `overrides/`, apply the permitted deltas, write `resolved/`. Only the path differs, configuration carrying two role axes and a subject folder where metadata carries one role axis and a namespace folder, so the difference is confined to how a file is handed to the resolver rather than to what it does with one.

There is one implementation, not two kept in step. The field kinds above are data the resolver reads, not a second code path.

## Open

**The ingress fixture is stale.** It uses `metadata/dc/dc.yml` with no state directory and bare scalar values, and carries no `sat/` namespace. A new fixture is needed rather than an extension of that one.

# satx: Shape and Purpose

**Version.** v0.0.8, 2026-09-12. Draft. Supersedes v0.0.7.

**Scope.** What `satx` is for, what it contains, and the constraints on the scripts that build and read it. `satx` is the testing SAT instance: complete, small, and kept apart from production. Companion to *SAT Sidecars: Config and Metadata* v0.0.13, which specifies the shapes this instance is built to.

## Changes in this version

- **Corrected the companion reference.** *SAT Sidecars: Config and Metadata* moved to v0.0.13, which corrects catalog placement to match the tree already shown here: `en/messages/`, `fr/messages/`, not `lib/locale/{lang}/`. That tree was right when it was written; the sidecar document had not yet caught up to it.

## Two jobs, one artifact

`satx` is a complete, small SAT instance that serves two purposes at once.

**A fixture.** Something to read. Every ruling in the sidecar specification is exercised by at least one node in it, so a reader can be checked against the document rather than against its author's memory of the document.

**A prototype.** A worked example of the shape SAT MVP is being built toward. Once the reader agrees with it, the instance is evidence that the shape is coherent and implementable rather than only written down.

**It stays separate from production.** That separation is what keeps the first job honest. A fixture that becomes the reference stops being an independent check and becomes the thing the specification is measured against, which is the wrong way round. `satx` is promoted to a prototype only after the reader has agreed with it, never before. The name carries that: nothing called `satx` is going to be mistaken for the instance a client's content lives in.

## Built from the document, not from the reader

The generator is written from the sidecar specification, not from the reader's source. Two independent readings of one document, and any disagreement between them is informative. If the same understanding produced both, they agree by construction and the comparison proves nothing.

In practice: whoever writes the generator does not consult the reader while writing it, and the reader is not adjusted to match the generator without first checking which of the two the document supports.

## Shape

A full instance, because the instance is where both kinds of territory occur together:

```
satx/
  .satx.assets/                   sat role: instance config, field_kinds
  bin/
    .bin.assets/.sat-boundary     commands, by role
  lib/
    .lib.assets/.sat-boundary
  en/                             archive: SAT's own documentation
    .en.assets/
    docs/
    messages/
      .messages.assets/.sat-boundary      catalogs for bin strings
  fr/                             archive
    .fr.assets/
    docs/
    messages/
      .messages.assets/.sat-boundary
  content/                        collection of collections
    .content.assets/
    examples/                     collection: correct throughout
      en-ca/                      archive
      fr-ca/
      es-ca/
    errors/                       collection: built to fail
      en-ca/
      fr-ca/
      es-ca/
    ingress/
      .ingress.assets/.sat-boundary       staged, not yet described
```

Three things this exercises that a bare archive would not.

**Organizing directories inside an archive and beside a collection.** `messages/` sits inside `en/`, which is itself an archive, and `ingress/` sits beside the collections. A reader stops at each rather than descending, and reports anything archived found beneath one. The first case is the one most likely to be got wrong, because the boundary is inside described territory rather than outside it.

**A collection containing collections.** The specification allows the nesting and nothing has tested it. The full role chain, `sat` through `collection`, `archive`, `directory`, `content`, appears in one tree, with `collection` occurring twice at different depths.

**A bare language tag beside regioned ones.** `satx/en` has no region while `examples/en-ca` does, and that is deliberate rather than untidy. SAT's documentation and its message catalogs address every English reader, so one English set is written and translated once, which is the faster path. A user's site addresses Canadian English and says so. The two tags differ because the two audiences differ, and both are well-formed BCP 47.

It also leaves room. `en` means English with no region stated, so adding `en-gb` later is additive rather than a rename of what is already there.

**Correct material and broken material, separated.** `examples/` is the prototype half and can carry real documentation, because a reader's output from it should be boring and checkable. `errors/` carries whatever text is convenient, because nobody reads it for content.

## Organizing directories declare themselves

`[P]` A directory outside the cascade carries a marker in its sidecar:

```
ingress/
  .ingress.assets/
    .sat-boundary
```

The presence of the file is the whole signal. Its contents are prose for a human and nothing parses them.

**Why the marker exists.** Without it, "no sidecar" means organizing, so a directory whose sidecar was never created and one deliberately outside the cascade are indistinguishable. A dropped sidecar then reads as a deliberate boundary, silently, which is the failure mode this project keeps finding.

**Why it lives in the sidecar rather than loose in the directory.** It makes the invariant uniform: every directory has a sidecar, and the sidecar says whether the directory is a node or a boundary. Absence becomes an error in every case, never a meaning. All SAT bookkeeping stays inside `.assets` directories and nothing loose sits among the material.

A sidecar holding the marker has no role folder, because an organizing directory holds no role. A sidecar with neither a role folder nor a marker is an error.

**It ends a cascade rather than starting one.** This is not the nested instance boundary, which begins a new cascade below it. An organizing directory ends the one above: nothing beneath it participates in config or metadata, and a reader stops rather than stepping through.

**Contents are worth writing.** The directory has no sidecar metadata, so the marker is the only place an explanation can live. "Scans, originals of the 2019 intake, ingressed 2024-03" is what someone needs five years later.

A marker named after a role would suggest the directory holds something. `.sat-boundary` says what it does: the cascade stops here. That also leaves room for a boundary wanted for a reason other than organizing material, without the name having to be revisited.

**Introducing it invalidates every existing archive,** since none of their organizing directories carry markers. That needs a migration pass or a grace period where unmarked-and-sidecarless is warned rather than failed. Nothing is in production yet, so this is the cheapest moment.

## Where it lives

`satx` is a directory of its own, a sibling of SAT and of the website repository, owned by neither:

```
development/
  sat/
  satx/
  website-vishpala-eleventy/
```

Both read it and neither contains it. That matters more than it looks: a fixture living inside one of its consumers tends to be adjusted to suit that consumer, quietly, until it stops being an independent check. A sibling has no owner to please.

It also reflects what `satx` is. A SAT instance is a thing on a filesystem with an instance root, and putting one inside a repository that is not itself an instance would misrepresent it.

## The documents live in the instance

`satx/en/docs` holds every document needed to understand `satx`: the sidecar specification, the ingress requirements, this document, and whatever else the instance depends on.

They are archived content, described like anything else, with works and expressions and sidecars. A French translation of the sidecar specification is an expression of the same work as the English one, paired by `isVersionOf`, exactly as a user's translated page would be.

That closes a loop worth closing. The instance that demonstrates the shape carries the documents that specify the shape, in that shape. If the documentation cannot be held correctly by the system it describes, something is wrong with one of them, and it is cheaper to find out here than in a client's collection.

It also gives the examples collection less to do. `satx/en/docs` is real material, correct, and substantial enough to exercise sections, subject chains and partial translation coverage. `content/examples/` can then be small and deliberate rather than having to carry realism as well.

## The toolchain

`satx` runs on two installed tools, neither of which it contains.

**python-tool** installs a self-contained CPython into user space, with no elevated privilege, no package manager and no compiler. It has a working Windows path: `install.ps1` and a rendered `.cmd` wrapper alongside the shell one.

**sat-tool** installs versioned SAT artifacts under `~/.local/share/sat-tool/<version>/`, each with its own virtual environment, and writes an env file naming the active one. Generated wrappers in `~/.local/bin` source that file at runtime, so switching versions needs no shell restart and a non-interactive context resolves the same version as an interactive one.

`satx/bin/sat init ../saty` therefore works by `satx` being the active artifact, not by `satx` containing the tooling. A new instance does not receive a copy of `bin/`, because tooling comes from the install.

### What is portable and what is not

`satlib` is Python and portable. The interpreter is portable, because python-tool provides it. The gap is the tier dispatchers, `en/bin/sat/sat` and its siblings, which are bash, so a generated Windows wrapper has nothing native to execute.

That gap is documented upstream with two candidate resolutions, and writing the dispatchers in Python removes it rather than working around it. Until then, "cross platform" is true of the library and the runtime and not yet of the commands, and this document should not imply otherwise.

## Three runs

Each run adds one thing the previous cannot test.

**One language.** The cascade itself. Contextual fields descending, local fields not descending, accumulating rows, per-item locks, amendment from above, deprecation, `<notset>` awaiting an editor. No pairing, no `isVersionOf` yet.

**Two languages.** Pairing. The same `isVersionOf` across two archives, with different paths and different depths, and one work present in only one language so partial coverage is exercised rather than assumed.

**Three languages.** That nothing assumes two. Anything that works at two and fails at three is usually a hardcoded notion of "the other one", and it is cheaper to find here than in a switcher.

## What each node is for

Roughly eight content nodes, each earning its place by testing a ruling.

| Node | Tests |
| --- | --- |
| A section with children | The subject chain accumulating from ancestors |
| A resource two levels deep | A chain of more than one ancestor |
| A resource with no title of its own | That a local field does not descend, visibly |
| A resource under a collection-set `rights` | A contextual field descending across archives |
| A resource with a locked subject item | Per-item `overridable: false` |
| A resource with an item delegated to a lower row | Placement into another tier's row |
| A resource with a deprecated item | Exclusion from the consumer view, retention in the record |
| A resource with a `<notset>` row | An editor prompt that has not been answered |
| A work in one language only | Partial coverage, and the single-expression report |
Those live in `examples/`. Every one is correct, and a reader's output from them is the known-good result.

### The errors collection

`errors/` exists because a check nobody exercises is a check nobody knows is broken. Each archive in it holds nodes built to trip one rule:

| Node | Should be reported as |
| --- | --- |
| A content file beneath a marked organizing directory | Archived content outside the cascade |
| A directory with neither sidecar nor marker | Unaccounted for |
| An archive writing into the `sat` row | A tier speaking for a role that outranks it |
| A field name with a typo | No declared kind |
| Two content nodes sharing an `identifier` | Identity not unique |
| Two expressions of one work in one language | Duplicate coordinates |
| An `amend` matching nothing | Stale amendment |
| An override against a field locked upstream | Held but not applied, marked inert |
| A `.sat-boundary` containing a glob pattern | Probably a misunderstanding |

A reader run against `errors/` should produce exactly this list. Fewer means a check is missing; more means a check is wrong.

## The scripts

**Python, cross platform.** SAT is Python for cross-platform compatibility and the testing instance is part of SAT, so its scripts are too. Nothing may assume a POSIX shell, a path separator, or a case-sensitive filesystem.

Concretely:

- `pathlib` throughout, never string concatenation for paths
- no shelling out to `find`, `cp`, `rm`, or anything else external
- no assumption that `a.md` and `A.md` are different files
- text written with an explicit encoding, always UTF-8
- line endings chosen deliberately rather than inherited from the platform

**YAML 1.2, which means `ruamel.yaml` rather than PyYAML.** This is a correctness requirement and not a preference. PyYAML implements YAML 1.1, where `no` is a boolean, and `no` is also the ISO 639-1 code for Norwegian. A language key written unquoted parses as `False`, silently, with nothing visible in the file. `y`, `on` and `off` behave the same way, and a bare numeric slug becomes an integer and stops matching the string it names.

Verified: given the same input, PyYAML yields `False` for a Norwegian key and `ruamel.yaml` yields `"no"`.

`[D]` **`ruamel.yaml` with the modern `YAML()` API.** Two settings its correct use depends on, neither of them a default.

**`yaml.preserve_quotes = True`, on any instance that rewrites a file.** Round-trip mode strips quotes it considers unnecessary, so a hand-written `["no"]` comes back as `[no]`. The archivist's quoting would be removed by the tool that told them to use it.

**Explicit quoting when generating.** A freshly built string dumps unquoted: `{"value": ["no"]}` writes `- no`. ruamel is right by its own lights, since under YAML 1.2 `no` is an ordinary string and needs nothing. The hazard is entirely downstream, in a reader that is not 1.2. So values the specification says to quote are wrapped in `DoubleQuotedScalarString` when written, rather than relying on the dumper to decide.

The asymmetry is worth knowing because it is invisible. A numeric-looking slug is quoted automatically, since ruamel must quote `"2024"` to survive its own round trip. A language tag is not. So the case that needs care is the one the library will not warn about.

**Round-trip for what a person edits, safe for what a tool generates.** `overrides/` is the only hand-edited file, and comments in it are an archivist's reasoning, which a rewrite should not discard. `defaults/` and `resolved/` are generated and have no comments to keep.

**Cascading where it helps.** The scripts follow the same tier structure as the instance they build. A generator for a collection knows what a collection's defaults are and passes its requirements down to the archives it creates, which pass theirs to directories, and so on. Minting behaves this way already in the specification: `sat` mints for `sat`, then passes requirements and defaults to `collection`, which mints collections.

The point is not that everything must cascade, but that where a script produces something a lower tier will extend, it hands down defaults rather than having the lower tier reach up. That keeps each tier's stated intention intact when material moves between instances.

## What it is checked against

The gate for the whole exercise: **does the sidecar path produce the same translation pairing the front matter path produces?**

The existing Sveltia-based site pairs translations through `identifier` and `relation` in front matter, with a `byWork` collection. `satx` pairs them through `sat:isVersionOf` in sidecars. If the two agree on which resources are versions of which works, with the same self-inclusion and the same reciprocity, the sidecar architecture reaches the ingress contract.

If they disagree, the disagreement is discovered on twenty files rather than after a theme has been ported.

## Open

**Is `satx` committed, or generated on demand?** The generator is an artifact either way. Whether its output is committed as well decides two things: whether a consumer's continuous integration clones a repository or runs a script, and whether identifiers must be deterministic so that two runs produce the same instance.

Committed, `satx` is a stable reference that can be diffed when the specification changes, and it can drift from the generator that made it. Generated, it cannot drift and there is nothing to diff.

The middle position is to commit it and treat a difference between the committed instance and a fresh generation as a failure, which keeps both properties at the cost of a check.

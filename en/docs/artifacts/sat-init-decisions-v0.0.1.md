# sat init: Decisions

**Version.** v0.0.1, 2026-09-13.

**Purpose.** Answers to the questions raised before writing `sat init`, in the order they were asked. Each is marked `[D]` decided, `[P]` proposed and open to correction, or `[?]` needing a decision that has not been made.

**Scope of the first version.** `sat init` produces a bare instance skeleton and nothing beneath it. No collections, no archives, no preseed. Bulk creation is a separate decision taken once this works, and a preseed format is a new thing to design from the sidecar specification rather than something already specified.

## Spec conflicts

### How many author folders the instance root carries

`[D]` **Two: `sat` and `collection`.**

An earlier answer in conversation said one. That was wrong, and the layout document is right: the root holds both roles, because it has the SAT instances `en/`, `fr/` language archives as well as the example  `content/` as children, and a node holding archives and collections is acting as a collection.

So the root's sidecar is:

```
satx/.satx.assets/
  sat/
    config/...
    metadata/...
  collection/
    config/...
    metadata/...
```

The specification already covers this: a multi-role node writes one layer per role it holds, and those layers resolve in role order, the same order the cascade uses between nodes. `sat` resolves before `collection`.

This is not a special case in the code. A node's roles are read from the author folders present in its sidecar, and the resolver iterates however many it finds.

### Whether `directory` and `content` belong in `sat`'s children

`[D]` **No.** The children of each role:

| Role | May contain |
| --- | --- |
| `sat` | `collection`, `archive` |
| `collection` | `collection`, `archive` |
| `archive` | `directory`, `content` |
| `directory` | `directory`, `content` |
| `content` | nothing |

A loose document directly under an instance root would have no archive around it, so it would have no language, and the work index's scoping to the nearest collection root would have nothing to scope against.

`[D]` These live in configuration as the `children` structural field, declared at the root, locked. `init` reads them rather than carrying the table.

### Whether `roles` is declared at every node or only the root

`[D]` **The root only.** Two different things are called roles and the ambiguity is the whole question.

`roles` in configuration is a **vocabulary** field: the list of role names that exist. Declared once at `sat`, never overridable, exactly as the configuration specification describes vocabulary fields.

A node's **own** role is not a field at all. It is structural, expressed by which author folders its sidecar carries. Asking what role a node holds means reading its sidecar, not reading a value.

So `init` writes no role-related field into a non-root node's config. It creates the author folder, and that is the declaration.

### Whether a collection may hold both collections and archives at once

`[D]` **Both, at once.**

`satx` already requires it: the root holds `en/` and `fr/` as archives and `content/` as a collection, simultaneously. Forbidding the mix would make the instance the specification describes invalid.

The children table above says `collection` may contain `collection` and `archive`, with no rule that it must choose.

## Mechanism

### One inspecting command, or thin per-role commands

`[D]` **Thin per-role commands over one shared library operation.**

`bin/` is already organised by role. The old repository used this shape. And a single command that infers what to create from where it is pointed has to guess, which fails worse than being told: creating an archive where a collection was meant is a mistake nothing reports.

```
bin/sat/sat init <path>
bin/collection/collection init <path>
bin/archive/archive init <path>
bin/directory/directory new <path>
bin/content/content new <path>
```

Underneath, one `create_node(path, role, ...)` in `satlib`. The commands differ in which role they pass and what they prompt for.

### One pass from a preseed, or one command per tier

`[D]` **One command per tier, for this version.** Preseed deferred.

A preseed format is a new artifact to design from the sidecar specification, and designing it before `init` works means designing against an unproven shape. The old repository's `collection-preseed.yml.example` and `archives-parent.yml` are worth reading when that decision comes, not before.

## What seeding writes, per role

`[D]` **At `sat`**, a new instance. Nearly silent, because the root defaults ship populated.

Written: `sat_version`, from the creating instance's own version. Prompted: `interface_language`, `default_metadata`. Everything else is the shipped defaults.

`[D]` **At `archive`**, `language` is mandatory and locked, so it always prompts. It is written to `metadata/dc/overrides/` at the archive node with `overridable: false`, because an archive is a language scope and nothing below it may claim otherwise.

`[P]` **At `collection`, `archive` and `directory`**, everything else is left inherited rather than prompted. `rights` and `publisher` descend from above and a node that accepts them needs no layer of its own. Prompting for values a tier has no reason to change fills files with noise, which is the seeding problem the specification already names.

`[D]` **At `content`**, real prompting. `title`, `description` and `date` seed as `<notset>` and drive the prompt-on-`<notset>` rule. The derived subject chain seeds as a proposal an editor confirms or amends.

`[D]` `identifier` is never seeded as `<notset>`. It is minted, because a UUID is not something an editor types.

## Identity minting

`[D]` **Every node gets an `identifier`.** Not only content nodes.

The russian-doll goal requires it: a collection liberated from one instance and migrated to another needs identity that survives the move, and "the work index is scoped to the nearest collection root" requires that collection to be identifiable by something other than its path. A slug is a name and names change.

`[D]` **Only content nodes get `isVersionOf`.** Only a content node realises a work. A collection is not an expression of anything.

So minting produces:

| Role | Minted |
| --- | --- |
| `sat` | `identifier` |
| `collection` | `identifier` |
| `archive` | `identifier` |
| `directory` | `identifier` |
| `content` | `identifier`, and `isVersionOf` for the work it realises |

Both are `urn:uuid`, v4, generated once and immutable. Never derived from a slug, a path, or content: a derived identifier changes when the thing it names is renamed, which is the event an identifier exists to survive.

`[D]` **The authority to mint cascades by role**, as the specification states. `sat` mints for `sat`, then passes requirements and defaults to `collection`, which mints collections, and so down.

### One consequence to settle before the subject chain is implemented

`[?]` The specification says `subject` accumulates from ancestor **works**. A directory node has an `identifier` and no work; the work belongs to its index resource.

So the chain accumulates from the works of ancestor **index resources**, not from directory nodes, and a directory with no index resource contributes nothing to it.

That reading needs confirming, because the two differ exactly where a section has no landing page. It does not block `init`, and it does block the subject chain.

## Test inputs for `satx/bin/sat init ../saty`

`[D]` **Target:** `../saty`, a sibling of `satx`.

`[D]` **Deliberately different values**, so the test proves `init` is not reproducing `satx`'s own specifics:

| Field | `satx` | `saty` |
| --- | --- | --- |
| `interface_language` | `"en"` | `"fr"` |
| `rights` | as shipped | `"CC-BY-SA-4.0"` |
| `publisher` | `"Vishpala"` | `"Test Publisher"` |

`interface_language` differing is the sharpest of the three: it proves the created instance is not inheriting the creating instance's interface, which is the mistake easiest to make and hardest to see.

`[D]` **What "works" means.** `saty` reads clean: `sat read ../saty` reports the expected node count, no errors, and no warnings that are not deliberate. A reader that accepts `satx` and rejects `saty` means `init` and the specification have parted company, which is the failure this test exists to catch.

## Open

`[?]` Whether the subject chain accumulates from ancestor index resources or from ancestor directory nodes. Above, and blocking the subject chain rather than `init`.

`[?]` Whether `saty` should ship with `en/docs` and `en/messages` archives, or with no archives at all. A bare skeleton is simpler and a new instance with nowhere to put its own documentation may be less useful than it looks.

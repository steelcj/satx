# SAT Instance File System Layout

**Version.** v0.0.2, 2026-09-13. Supersedes v0.0.1.

## Changes in this version

- Corrected the description of what an upgrade replaces. The tool artifact gets a new version; a content instance does not.
- Corrected `content/` from an archive to a collection. It holds collections, so it is one.
- Reordered the opening so a reader meets what `satx` is before meeting why that is temporary.
- Reconciled the two statements about content sitting outside the instance, which held in production and not during development, with nothing saying so.
- Gave the egress case its own line. It is the clearest reason boundaries are necessary rather than merely permitted.

## Two things in one directory

`satx` is two things at once: the SAT tool under development, and an instance of example content being tested with it.

Production separates them. A tool artifact installs to `~/.local/share/sat-tool/<version>/` on Linux, and upgrading installs to `~/.local/share/sat-tool/<new-version>/` and replaces the artifact wholesale. A content instance, created by `sat init`, is never touched by an upgrade.

Here they share a directory. The tool half is `bin/`, `lib/`, `venvs/`, and the `docs` and `messages` archives under each language. The content half is `content/`, holding collections a user of the instance would own.

Both halves use the same cascade and nothing in the specification distinguishes them, because structurally there is nothing to distinguish. `satx` is a collection. `en/` and `fr/` are archives. `content/` is a collection holding further collections. The cascade treats them alike because they are alike.

The separation is editorial, and it ends when `osat-sat` installs a versioned artifact rather than this directory being one.

## SAT parent directory

The SAT parent directory is the root of the instance. It holds two roles: `sat` and `collection`.

```bash
<sat-node-name>
satx # example
```

## Boundary directories

The instance includes boundary directories, which organize files needing no sidecar of their own beyond a marker telling SAT that the cascade stops here.

In practice: when any SAT role encounters a `.sat-boundary`, which is the first thing it checks for, that directory is excluded from SAT's config and metadata cascades.

```bash
bin/.bin.assets/.sat-boundary
```

`satx/bin`, `satx/lib` and `satx/venvs` are boundary directories, as is any other directory marked this way.

The technique is equally available to users creating content outside the instance, to exclude directories from the cascades. It suits ingress, egress and data directories that SAT should be able to sit beside without managing.

Two cases show why it is necessary rather than merely permitted.

**Source material that is not an archive.** A collection of source image scans is not intended to become a SAT archive, and SAT should not try to manage it as one.

**Egress that must never return.** Content prepared for a static site generator by a transmog should never be re-ingressed by SAT. A boundary in the egress target directory prevents exactly that.

### `.sat-boundary` content example

The file's presence is the whole signal. Its contents are prose for a person, and nothing parses them.

```txt
Commands, by role. Organizing: no sidecar of its own, holds no role, none of it
participates in the cascade.

sat is prototyped here rather than installed here. satx is becoming the new SAT
prototype, so bin/ holds the actual dispatcher scripts under development, in the
tree the specifications describe, rather than being populated by a separate
installed artifact the way a shipped instance eventually will be. See
HANDOVER.md and .claude/session logs for how this changed.
```

## Directories

```bash
├── bin  # bins for archives, collection, content, directory, sat, transmog
├── en   # English archive: SAT documentation, and catalogs for bin and lib
│   ├── docs      # English SAT documentation
│   └── messages  # English catalogs for satx/bin and satx/lib, if needed
├── fr   # Same layout as satx/en. The instance can support many languages.
│   ├── docs      # SAT documentation in French
│   └── messages  # French catalogs
│       └── bin   # French catalogs for satx/bin
├── lib  # instance prototype and development library
│   └── satlib
└── venvs
    └── sat
        └── 0.5.0
```

`en/` and `fr/` are archives. `docs/` is a directory node within each. `messages/` is a boundary directory: catalogs are not archived content, because a catalog is a lookup table keyed by source string rather than a realisation of a work.

## User content example

In production, someone using the instance to create SAT-managed collections, archives, directories and content keeps that material in a directory outside the instance. During development, `satx/content/` stands in for it.

The structure is flexible. Here a directory called `content` holds everything a user of the instance would own:

```bash
├── content
│   ├── errors
│   │   ├── en-ca
│   │   │   ├── scans
│   │   │   └── unaccounted
│   │   ├── es-ca
│   │   │   └── stray
│   │   └── fr-ca
│   ├── examples
│   │   └── websites
│   │       └── universalcake.com
│   │           ├── en-ca
│   │           │   └── cakes
│   │           │       └── wedding
│   │           ├── es-mx
│   │           │   └── pasteles
│   │           │       └── boda
│   │           └── fr-ca
│   │               └── gateaux
│   └── ingress
│       └── scans
```

Reading the roles off that tree: `content/` is a collection, `examples/` and `errors/` are collections, `websites/` is a collection, `universalcake.com/` is a collection, and `en-ca/`, `es-mx/` and `fr-ca/` are archives. Below an archive, `cakes/` and `wedding/` are directory nodes.

`ingress/` is a boundary directory. Material staged there is not yet described, and forcing a node onto it would assert a description nobody has written.

`errors/` exists to be read by a reader and fail. Each node in it trips exactly one check, and a reader run against it should report exactly the expected list. Fewer means a check is missing; more means a check is wrong.

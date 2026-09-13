## SAT Instance File System Layout

Because satx is both the SAT tool under development and some example user content being tested with it, the content being tested is being place under the SAT instance. Once in production, the SAT instance and the example content that it manages will be separated.

For example, the SAT instance tool artifacts will intall to ~/.local/share/sat-tool/<version>/ on Linux systems and can be upgraded to ~/.local/share/sat-tool/<new-version>/ on Linux systems.

So while the SAT instance gets a new version, the content example created by sat init and is never touched by one. 

This means that the sat tools, such as satx/bin/, satx/lib/, satx/venvs/, and the satx/<language-archive>/docs and messages archives under each language. The SAT example content/ contains examples of collections that a user of the SAT instance would own.

Both halves are described by the same cascade, and nothing in the specification distinguishes them, because structurally there is nothing to distinguish: satx is a collection, and en/, fr/ are archives and the contained content/ are its children.

So in the development prototype that will become our production SAT, the separation is editorial, and it ends when osat-sat installs a versioned artifact rather than this directory being one.



That also rescues your "not part of the SAT instance" sentence: it's true of the artifact, false of the directory, and now the document says which.

### SAT Parent Directory

The SAT parent directory serves as the root of the SAT instance. It has the following roles: sat, collection.

```bash
<sat-node-name>
satx # example
```

### Directory structure of the SAT Instance

Note: satx/bin, satx/lib and satx/venvs are sat boundary directories as well as any other directories created in the SAT instance that are marked as boundary directories using a `.sat-boundary` file in the directories assets directory.

### SAT Boundary example

The SAT instance includes Boundary Directories which are used to organize files that do not require sidecars other than to notify SAT bins and libs (if needed) that they are designated as a SAT cascade boundary. 

In practice this means that when any SAT roles encounters a sat-boundary (the first thing they  check for) then the boundary directory is excluded from SAT's config and metadata cascades.

This technique may also used by SAT users creating content outside of the SAT instance in order to exclude directories from the cascades. Very useful for creating ingress, egress or data directories that may be used by sat, collections, archives and content that should not be managed by a SAT instance. For example, you would not want SAT to try and manage an archive resource such as a collection of source image scans that is not intended to become a SAT archive. SAT egress that prepares content for a static site generator using a transmog should never be reingressed by SAT, so the SAT boundary in the egress target directory prevents this.

```bash
bin/.bin.assets/.sat-boundary
```

#### .sat-boundary content example

```txt
Commands, by role. Organizing: no sidecar of its own, holds no role, none of it participates in the cascade.

sat is prototyped here rather than installed here. satx is becoming the new SAT prototype, so bin/ holds the actual dispatcher scripts under development, in the tree the specifications describe, rather than being populated by a separate installed artifact the way a shipped instance eventually will be. See HANDOVER.md and .claude/session logs for how this changed.
```

### Directories

```bash
├── bin  # bins for archives, collection, content, directory, sat, transmog
├── en   # English documentation of SAT(X) and any bin and lib message translations 
│   ├── docs # English SAT documentation
│   │   └── sat-init-questions
│   └── messages # English translations for satx/bin's and satx/lib's if needed.
├── fr   # Same layout as satx/en. The SAT instance can support many languages.
│   ├── docs # SAT documentation in French
│   └── messages # French translations for satx/bin's and satx/lib's if needed.
│       └── bin    # French translations for satx/bin's
├── lib  # SAT instance prototype/development lib. 
│   └── satlib
│       └── __pycache__
└── venvs
    └── sat
        └── 0.5.0
```

## User Content Example

Someone or some system using the SAT instance to create SAT managed collections, archives, directories and content is kept separate from the SAT instance by using a directory that is not part of the SAT instance.

In this basic example a directory called "content" has been created to hold all of a SAT Instance users data.

This is a very flexible structure. This managed SAT content directory structure looks like this:

```bash
├── content
│   ├── errors
│   │   ├── en-ca
│   │   │   ├── scans
│   │   │   └── unaccounted
│   │   ├── es-ca
│   │   │   └── stray
│   │   └── fr-ca
│   ├── examples
│   │   └── websites
│   │       └── universalcake.com
│   │           ├── en-ca
│   │           │   └── cakes
│   │           │       └── wedding
│   │           ├── es-mx
│   │           │   └── pasteles
│   │           │       └── boda
│   │           └── fr-ca
│   │               └── gateaux
│   └── ingress
│       └── scans

```


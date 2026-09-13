# Using sat read

**Version.** v0.0.2, 2026-09-13. Supersedes v0.0.1.

**Scope.** How to run `sat read` against a SAT instance: the whole tree, a single directory, a single file, and what the report and exit code mean in each case. Companion to `sat Virtual Environments`, since every example here runs through the venv that document sets up.

## Changes in this version

- **Corrected a stale claim.** `satlib`'s own reported messages are now routed through the translator, with a real `fr/messages/lib/sat-lib.po` catalog, not only `fr/messages/bin/sat-bin.po` as this document previously said.

## Invoking it

`sat` lives at `bin/sat` inside an instance, and the instance is that script's parent directory, per `sat-configuration-cascade-specification-v0-2-2.md`'s rule for locating the active instance. Run it through the venv's interpreter, not the system one:

```bash
venvs/sat/0.5.0/bin/python bin/sat read .
```

The rest of this document shortens that to `sat read` in prose, but every example below was run exactly as above, from the instance root.

## The whole instance

`sat read .` resolves every node from the instance root down and reports on all of it. This instance currently has nine deliberate problems, all inside `content/errors/`, and a real one would have none:

```text
ERROR  content/errors/en-ca/scans/photo-notes.md: archived content outside the cascade: a described node beneath an organizing directory
ERROR  content/errors/en-ca/typo.md: no declared kind for dc:titel. Declare it in field_kinds at the sat root, or correct the element name.
ERROR  content/errors/en-ca/unaccounted: unaccounted for: no sidecar and no .sat-boundary
ERROR  content/errors/es-ca: amend matches nothing in the directory row: urn:uuid:aad00a38-3d35-4ec2-8499-0bc5bcd301f4
 warn  content/errors/es-ca/stray: .sat-boundary looks like a glob pattern ('*.tmp'), not prose for a human; probably a misunderstanding
ERROR  content/errors/fr-ca: archive wrote into the sat row, which outranks it
 warn  content/errors/fr-ca/locked-notice.md: "rights" is locked upstream; override held but not applied
ERROR  content/errors/en-ca/duplicate-b.md: sat:identifier is not unique; also content/errors/en-ca/duplicate-a.md
ERROR  content/errors/fr-ca/original.md: duplicate language "fr-ca" for this work; also content/errors/fr-ca/copy.md

nodes   61
works   20

  urn:uuid:2d640a60-5ad3-4dc4-840e-9fd62063935c
    en       en/docs/sat-virtual-environments-v0-0-1.md

  urn:uuid:86a3e502-4ca2-4a55-9d4a-8eeaeed37897
    en       en/docs/satx-shape-and-purpose-v0-0-9.md
    fr       fr/docs/satx-forme-et-objectif-v0-0-8.md
```

(Trimmed here to the last two works; the full run lists all twenty.) The command's own exit code is 1 whenever an `ERROR`-level problem was found anywhere in scope, `0` when the tree resolves clean:

```bash
venvs/sat/0.5.0/bin/python bin/sat read .
echo $?
```

```text
1
```

## Checking a single file

Point the same command at a file instead of the root. Resolution still walks the whole instance, because a node's resolved values depend on its ancestors, but the report narrows to that one node:

```bash
venvs/sat/0.5.0/bin/python bin/sat read en/docs/sat-virtual-environments-v0-0-1.md
```

```text

nodes   1
works   1

  urn:uuid:2d640a60-5ad3-4dc4-840e-9fd62063935c
    en       en/docs/sat-virtual-environments-v0-0-1.md
```

Nothing is wrong with it, so there are no problem lines and the exit code is `0`. Pointing the same form at a file with a real defect shows the difference:

```bash
venvs/sat/0.5.0/bin/python bin/sat read content/errors/en-ca/typo.md
```

```text
ERROR  content/errors/en-ca/typo.md: no declared kind for dc:titel. Declare it in field_kinds at the sat root, or correct the element name.

nodes   1
works   1

  urn:uuid:c730ca67-0d6a-4524-abc1-a230b457b619
    en-ca    content/errors/en-ca/typo.md
```

Exit code `1`. Only this file's own problem is shown; the other eight deliberate errors elsewhere in the instance stay out of scope.

## Checking a directory

The same scoping works one level up, over everything beneath a directory rather than one file. `content/examples/` is correct throughout, so it resolves with no problems and a full, multi-language work list:

```bash
venvs/sat/0.5.0/bin/python bin/sat read content/examples
```

```text

nodes   33
works   8

  urn:uuid:78f2394a-cbc0-47f0-ab47-de35baff294d
    en-ca    content/examples/websites/universalcake.com/en-ca/about.md
    es-mx    content/examples/websites/universalcake.com/es-mx/sobre-nosotros.md
    fr-ca    content/examples/websites/universalcake.com/fr-ca/a-propos.md
```

(One work shown of the eight; the rest follow the same shape.) `content/errors/fr-ca/` is the directory built to fail three different ways at once, so scoping to it surfaces exactly those three and nothing from `en-ca/` or `es-ca/`:

```bash
venvs/sat/0.5.0/bin/python bin/sat read content/errors/fr-ca
```

```text
ERROR  content/errors/fr-ca: archive wrote into the sat row, which outranks it
 warn  content/errors/fr-ca/locked-notice.md: "rights" is locked upstream; override held but not applied
ERROR  content/errors/fr-ca/original.md: duplicate language "fr-ca" for this work; also content/errors/fr-ca/copy.md

nodes   5
works   2
```

One exception: a problem attributed to the instance root itself, `.`, always stays in the report regardless of what was asked about, because a missing `field_kinds` or another root-level failure would make every resolution in the instance meaningless, scoped or not.

## A path outside the instance

`sat read` refuses a target that is not inside the instance it was found in, rather than silently resolving nothing:

```bash
venvs/sat/0.5.0/bin/python bin/sat read /tmp
```

```text
error: /tmp is not inside the instance at /home/initial/2-areas/development/satx
```

Exit code `2`, distinct from the `1` a resolved-but-broken tree returns.

## Reading the report

`nodes` counts every node in scope, roles held by directories as well as files. `works` counts distinct `sat:isVersionOf` values among the content nodes in scope, each followed by its expressions, one line per language, so a work missing a language simply has fewer lines rather than a placeholder. `ERROR` means the resolver could not make sense of something; `warn` means it could, but held a value inert rather than apply it, which is itself information rather than a defect, since that is exactly what a locked field or a deprecated item is supposed to do.

`interface_language` decides which language `ERROR`, `warn`, `nodes`, and `works` themselves print in, not which files are read. `sat-virtual-environments-v0-0-1.md` and `sat-sidecars-config-and-metadata-v0-0-14.md`'s own change note cover where those catalogs live; both `fr/messages/bin/sat-bin.po` and `fr/messages/lib/sat-lib.po` exist and are exercised by content/errors/'s own nine problems, translated in full. Every example above still shows English, because that is this instance's own `interface_language` setting, not a limit of what is available.

## Not yet decided

**Machine-readable output.** Every example here is the human-readable report. A `--json` flag, or a separate `sat read` mode, is an open question rather than something this version answers.

**Selecting by work instead of by path.** Scoping is positional and path-based today. Whether a work's `urn:uuid` should be an alternate way to ask "show me everything realising this work, wherever its expressions live" is not decided.

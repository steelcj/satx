# sat Virtual Environments

**Version.** v0.0.1, 2026-09-13. Draft.

**Scope.** Where a Python virtual environment for `sat` lives, why one is needed at all, and how creating one fits into installing and configuring a SAT instance. Companion to `satx: Shape and Purpose`, which records the toolchain this document explains one piece of.

## Why a venv at all

`satlib` reads and writes YAML, and Python carries no YAML support in its standard library. A parser has to come from somewhere, and it has to be the right one: `sat-sidecars-config-and-metadata-v0-0-14.md` and `sat-configuration-cascade-specification-v0-2-2.md` both make YAML 1.2 a correctness requirement rather than a preference, because YAML 1.1 treats `no` as a boolean as well as the ISO 639-1 code for Norwegian, and a Norwegian language key parses to `false` with nothing visible in the file. `ruamel.yaml`, run in its 1.2 mode, is the dependency this project has settled on. PyYAML is not an alternative; it implements YAML 1.1 only.

A dependency that comes from outside the standard library needs somewhere to be installed that will not collide with whatever else is on the machine running `sat`, and that is what a virtual environment is for. `sat` is not the only thing that might be installed on a given system, and pinning `ruamel.yaml` into the system Python would make every other Python program on that machine answer to `sat`'s version of it.

## Where this sits in the toolchain

`satx: shape and purpose` names two installed tools satx runs on, neither of which it contains: `python-tool`, which installs a self-contained CPython into user space, and `sat-tool`, which installs versioned SAT artifacts under `~/.local/share/sat-tool/<version>/`, each with its own virtual environment. That is the production picture. This document is about the same step, a version of `sat` getting its own venv, happening earlier and closer to home, because satx is becoming the new SAT prototype rather than being installed from a finished artifact.

The two pictures are meant to be the same shape at different addresses. A venv built for prototyping at `satx/venvs/sat/0.5.0/` and a venv `sat-tool` builds at `~/.local/share/sat-tool/0.5.0/` hold the same environment, keyed the same way, differing only in which directory is standing in for the other. Moving from one to the other is meant to be a relocation, never a redesign.

## Keyed by what it serves

`[D]` Virtual environments live under `venvs/`, one directory per artifact, one subdirectory per version of that artifact:

```
venvs/
  .venvs.assets/.sat-boundary
  sat/
    0.5.0/
  python/
    3.13.1/
```

`venvs/sat/0.5.0/` is the venv this version of `sat` runs in. A venv for a different purpose, a particular Python build to test against, for instance, sits beside it at the same depth rather than bending the scheme to fit: `venvs/python/3.13.1/`, not a special case grafted on afterward.

`venvs/` is organizing, per `sat-sidecars-config-and-metadata-v0-0-14.md`'s list of what belongs beneath a marker: binaries and compiled artifacts, and working files that are not, and may never be, resources. A venv is exactly that. It carries no sidecar of its own beneath the boundary, states no work, and nothing inside it participates in the cascade.

## requirements.txt names what goes in it

`[D]` Dependencies are declared once, in `requirements.txt` at the instance root, not inside the venv and not repeated per version. That is where a reader looks for what a version of `sat` needs, and where an installer will eventually read the same list to build the venv it creates. Today it holds one line:

```
ruamel.yaml
```

Pinning an exact version is left open for now, a question for whenever `sat` first needs to guarantee a specific `ruamel.yaml` release rather than whatever the latest one resolves to.

## Creating one

Two commands, run from the instance root:

```
python3 -m venv venvs/sat/0.5.0
venvs/sat/0.5.0/bin/pip install -r requirements.txt
```

On Windows the interpreter and installed scripts sit in `Scripts\` rather than `bin/`, so the second line reads `venvs\sat\0.5.0\Scripts\pip install -r requirements.txt`; nothing else about the shape changes.

`sat`'s own commands are invoked through that venv's interpreter, not the system one: `venvs/sat/0.5.0/bin/python bin/sat read .` today, and a generated wrapper doing the same lookup once `sat-tool` exists to generate one. Nothing in `bin/sat` hardcodes that path. Baking an absolute venv path into the dispatcher's shebang would defeat the reason the scheme exists, which is that the whole `venvs/sat/0.5.0/` directory can move to `~/.local/share/sat-tool/0.5.0/` without anything inside it having to change.

## A cross-platform cost, accepted rather than hidden

Windows imposes a 260-character path limit unless long paths are explicitly enabled, and a venv is where that limit gets tested: `satx\venvs\sat\0.5.0\Lib\site-packages\<package>\<deep>\<nested>\<module>.py` accumulates faster than it looks once a dependency nests its own packages a few levels deep. Keying the venv by artifact and version costs roughly twenty characters against the bare `.venv` a less descriptive scheme would use.

That cost is accepted rather than a reason to abandon the scheme. It is worth recording here so that whoever eventually hits it on a deeply nested package recognises the cause rather than blaming the dependency, the venv tool, or Windows itself. Enabling long paths, or keeping an eye on unusually deep dependencies when one is added to `requirements.txt`, are both cheaper than renaming the scheme after the fact.

## Not yet decided

**Whether requirements.txt should pin versions.** Unpinned today because there is exactly one dependency and no history of it breaking anything. Revisit once a second dependency arrives, or once the first one does.

**How `sat-tool` will read requirements.txt.** Whether it installs from the file directly at install time, or from a lockfile generated from it, is a question for whoever builds `sat-tool`, not for this prototype.

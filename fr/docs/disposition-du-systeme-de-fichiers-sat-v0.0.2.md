# Disposition du système de fichiers d'une instance SAT

**Version.** v0.0.2, 2026-09-13. Remplace v0.0.1.

## Changements dans cette version

- Corrigé ce que remplace une mise à niveau. L'artefact de l'outil reçoit une nouvelle version ; une instance de contenu non.
- Corrigé `content/` d'archive à collection. Elle porte des collections, donc c'en est une.
- Réordonné l'ouverture pour qu'un lecteur rencontre ce qu'est `satx` avant de rencontrer pourquoi c'est temporaire.
- Réconciliées les deux affirmations sur le contenu situé hors de l'instance, qui tenaient en production et pas en développement, sans que rien ne le dise.
- Donné au cas d'égression sa propre ligne. C'est la raison la plus claire pour laquelle les limites sont nécessaires plutôt que simplement permises.

## Deux choses dans un répertoire

`satx` est deux choses à la fois : l'outil SAT en développement, et une instance de contenu d'exemple testée avec lui.

La production les sépare. Un artefact d'outil s'installe à `~/.local/share/sat-tool/<version>/` sous Linux, et une mise à niveau installe à `~/.local/share/sat-tool/<nouvelle-version>/` et remplace l'artefact en entier. Une instance de contenu, créée par `sat init`, n'est jamais touchée par une mise à niveau.

Ici elles partagent un répertoire. La moitié outil est `bin/`, `lib/`, `venvs/`, et les archives `docs` et `messages` sous chaque langue. La moitié contenu est `content/`, qui porte des collections qu'un utilisateur de l'instance posséderait.

Les deux moitiés utilisent la même cascade et rien dans la spécification ne les distingue, parce que structurellement il n'y a rien à distinguer. `satx` est une collection. `en/` et `fr/` sont des archives. `content/` est une collection qui porte d'autres collections. La cascade les traite pareillement parce qu'elles sont pareilles.

La séparation est éditoriale, et elle prend fin quand `osat-sat` installe un artefact versionné plutôt que ce répertoire n'en soit un.

## Répertoire parent de SAT

Le répertoire parent de SAT est la racine de l'instance. Il porte deux rôles : `sat` et `collection`.

```bash
<nom-du-nœud-sat>
satx # exemple
```

## Répertoires limites

L'instance inclut des répertoires limites, qui organisent des fichiers n'ayant besoin d'aucun sidecar propre au-delà d'un marqueur disant à SAT que la cascade s'arrête ici.

En pratique : quand un rôle SAT quelconque rencontre un `.sat-boundary`, ce qui est la première chose qu'il vérifie, ce répertoire est exclu des cascades de configuration et de métadonnées de SAT.

```bash
bin/.bin.assets/.sat-boundary
```

`satx/bin`, `satx/lib` et `satx/venvs` sont des répertoires limites, comme tout autre répertoire marqué de cette façon.

La technique est également disponible pour les utilisateurs qui créent du contenu hors de l'instance, pour exclure des répertoires des cascades. Elle convient à l'ingestion, à l'égression, et aux répertoires de données à côté desquels SAT doit pouvoir se tenir sans les gérer.

Deux cas montrent pourquoi c'est nécessaire plutôt que simplement permis.

**Du matériel source qui n'est pas une archive.** Une collection de numérisations d'images sources n'est pas destinée à devenir une archive SAT, et SAT ne devrait pas essayer de la gérer comme telle.

**De l'égression qui ne doit jamais revenir.** Le contenu préparé pour un générateur de site statique par un transmog ne devrait jamais être réingéré par SAT. Une limite dans le répertoire cible d'égression prévient exactement cela.

## Répertoires

```bash
├── bin  # bins pour archives, collection, content, directory, sat, transmog
├── en   # Archive anglaise : documentation SAT, et catalogues pour bin et lib
│   ├── docs      # Documentation SAT en anglais
│   └── messages  # Catalogues anglais pour satx/bin et satx/lib, si nécessaires
├── fr   # Même disposition que satx/en. L'instance peut prendre en charge plusieurs langues.
│   ├── docs      # Documentation SAT en français
│   └── messages  # Catalogues en français
│       └── bin   # Catalogues en français pour satx/bin
├── lib  # bibliothèque de prototype et de développement de l'instance
│   └── satlib
└── venvs
    └── sat
        └── 0.5.0
```

`en/` et `fr/` sont des archives. `docs/` est un nœud de répertoire à l'intérieur de chacune. `messages/` est un répertoire limite : les catalogues ne sont pas du contenu archivé, parce qu'un catalogue est une table de correspondance indexée par chaîne source plutôt qu'une réalisation d'une œuvre.

## Exemple de contenu utilisateur

En production, quelqu'un qui utilise l'instance pour créer des collections, archives, répertoires et contenus gérés par SAT garde ce matériel dans un répertoire hors de l'instance. Pendant le développement, `satx/content/` en tient lieu.

La structure est flexible. Ici un répertoire nommé `content` porte tout ce qu'un utilisateur de l'instance posséderait :

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

En lisant les rôles de cet arbre : `content/` est une collection, `examples/` et `errors/` sont des collections, `websites/` est une collection, `universalcake.com/` est une collection, et `en-ca/`, `es-mx/` et `fr-ca/` sont des archives. En dessous d'une archive, `cakes/` et `wedding/` sont des nœuds de répertoire.

`ingress/` est un répertoire limite. Le matériel qui y est mis en scène n'est pas encore décrit, et forcer un nœud dessus affirmerait une description que personne n'a écrite.

`errors/` existe pour être lu par un lecteur et échouer. Chaque nœud qu'elle contient fait trébucher exactement une vérification, et un lecteur exécuté contre elle devrait rapporter exactement la liste attendue. Moins signifie qu'une vérification manque ; plus signifie qu'une vérification est erronée.

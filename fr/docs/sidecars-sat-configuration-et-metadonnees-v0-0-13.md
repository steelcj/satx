# Sidecars SAT : configuration et métadonnées

**Version.** v0.0.13, 2026-09-12. Remplace v0.0.12.

**Portée.** Les deux arbres de sidecar qu'un nœud SAT porte, côte à côte. La configuration est présentée en premier parce qu'elle est plus avancée, et l'arbre des métadonnées est spécifié contre elle afin que les différences soient visibles plutôt qu'inférées.

## Changements dans cette version

- **Les catalogues d'interface se déplacent dans l'archive de langue qu'ils desservent.** `en-ca/messages/`, et non `lib/locale/{lang}/`. Construire `satx` à partir de la règle précédente a fait surgir le conflit : `satx-shape-and-purpose` avait déjà placé les catalogues à l'intérieur de chaque archive, sur la lecture correcte qu'un catalogue est du matériel propre à une langue plutôt que du logiciel. La règle sur les répertoires organisateurs et le test « pas de sidecar, pas d'œuvre » sont inchangés ; seul l'endroit où se trouve un catalogue est corrigé. Le gabarit, `sat.pot`, reste avec le logiciel à `lib/locale/`, puisqu'il ne nomme aucune langue.

**Note sur `{node}`.** Les deux arbres utilisent `{node}` là où des brouillons antérieurs utilisaient `{level}`. Le vocabulaire définit déjà *nom de nœud* comme exactement ce que ce segment contient, et *level* était un reliquat des brouillons de parcours, où il décrivait un échelon de la cascade plutôt qu'un nom sur le disque. Le renommage atterrit ici en une seule passe à travers les deux arbres.

## La forme qu'ils partagent

```
config     .{node}.assets/{author}/config/{subject}/{state}/config.yml
metadata   .{node}.assets/{author}/metadata/{namespace}/{state}/{namespace}.yml
```

Quatre choses tiennent dans les deux :

- le sidecar est nommé d'après le nœud auquel il appartient
- `{author}` est le palier qui a écrit cette couche, et le seul rôle qui l'édite
- `{state}` est le dernier répertoire avant le fichier
- le nom de fichier fait écho au répertoire au-dessus de lui

Une chose diffère, et c'est le troisième segment. La config varie selon le **sujet (subject)**, le rôle auquel le matériel est adressé. Les métadonnées varient selon l'**espace de noms (namespace)**, le vocabulaire dans lequel le matériel est écrit.

Cette différence n'est pas une incohérence à résoudre. Elle découle de ce que chaque arbre contient, et les deux sections suivantes disent pourquoi.

## Config

La configuration est prescriptive. Ce sont des instructions, et des instructions peuvent légitimement viser un palier : « les archives utilisent cette liste d'exclusion » est un énoncé différent de « les répertoires utilisent celle-ci ». L'axe du sujet est ce qui porte ce ciblage.

| Segment | Signification | Tiré de |
| --- | --- | --- |
| `{node}` | Le nom du nœud auquel appartient le sidecar : un nom de répertoire, ou un nom de fichier avec son extension | Le système de fichiers |
| `{author}` | Le palier qui a écrit cette couche de la cascade | Le vocabulaire des rôles |
| `{subject}` | Le rôle auquel le matériel est adressé | Le vocabulaire des rôles |
| `{state}` | `defaults/`, `overrides/` ou `resolved/` | Ensemble fixe de trois |

Exemples travaillés :

| Chemin | Nœud | Auteur | Sujet |
| --- | --- | --- | --- |
| `sat/.sat.assets/sat/config/collection/defaults/config.yml` | `sat`, le répertoire racine | `sat` | `collection` |
| `en-ca/.en-ca.assets/archive/config/directory/overrides/config.yml` | `en-ca`, un nœud de répertoire tenant le rôle archive | `archive` | `directory` |
| `.report.md.assets/content/config/content/resolved/config.yml` | `report.md`, un nœud de fichier | `content` | `content` |

Le troisième exemple montre l'axe du sujet à son plus étroit. Un nœud de contenu est une feuille, donc il ne peut s'adresser qu'à lui-même.

## Métadonnées

Les métadonnées sont descriptives. Le `dc.yml` d'un nœud dit ce qu'est ce nœud. Le `publisher` d'une collection n'est pas adressé aux archives plutôt qu'aux répertoires ; c'est simplement l'éditeur de la collection, et les descendants héritent de ce qu'ils n'énoncent pas eux-mêmes. Il n'y a pas de sens cohérent dans lequel une métadonnée descriptive viserait un rôle en aval, donc les métadonnées n'ont pas d'axe de sujet.

Elles ont un axe que la config n'a pas, parce qu'elles parlent plus d'un vocabulaire. La config parle un vocabulaire à plusieurs publics. Les métadonnées parlent plusieurs vocabulaires à un seul.

| Segment | Signification | Tiré de |
| --- | --- | --- |
| `{node}` | Le nom du nœud auquel appartient le sidecar : un nom de répertoire, ou un nom de fichier avec son extension | Le système de fichiers |
| `{author}` | Le palier qui a écrit cette couche de la cascade | Le vocabulaire des rôles |
| `{namespace}` | Le vocabulaire de métadonnées : `dc`, `dcterms`, `sat` | L'ensemble des espaces de noms |
| `{state}` | `defaults/`, `overrides/` ou `resolved/` | Ensemble fixe de trois |

Exemples travaillés, correspondant à l'ensemble de config ci-dessus :

| Chemin | Nœud | Auteur | Espace de noms |
| --- | --- | --- | --- |
| `sat/.sat.assets/sat/metadata/dc/defaults/dc.yml` | `sat`, le répertoire racine | `sat` | `dc` |
| `en-ca/.en-ca.assets/archive/metadata/dc/overrides/dc.yml` | `en-ca`, un nœud de répertoire tenant le rôle archive | `archive` | `dc` |
| `.report.md.assets/content/metadata/sat/overrides/sat.yml` | `report.md`, un nœud de fichier | `content` | `sat` |

Le troisième exemple montre où vit l'identité de l'œuvre. C'est la seule chose dont une archive multilingue ne peut se passer, et c'est la seule chose que le dispositif d'ingestion actuel ne porte pas.

## Disposition du sidecar

Chaque dossier de rôle à chaque nœud porte un ensemble de répertoires à trois états, par espace de noms :

```
.{node}.assets/
  {role}/
    metadata/
      dc/
        defaults/dc.yml     # lecture seule, reçu du nœud au-dessus
        overrides/dc.yml    # inscriptible, le seul fichier édité à la main
        resolved/dc.yml     # lecture seule, généré localement
      sat/
        defaults/sat.yml
        overrides/sat.yml
        resolved/sat.yml
```

L'état vit dans le nom du répertoire et le nom de fichier est l'espace de noms, donc `metadata/dcterms/` pourra plus tard se tenir à côté de `dc/` et `sat/` avec ses propres trois états et aucun changement à la grammaire.

Les espaces de noms sont indépendants. Un nœud peut porter `dc/` et pas `sat/`, ou les deux. Chacun se met en cascade de son côté, et rien dans un espace de noms ne se résout contre un autre.

## L'auteur est le palier qui a écrit la couche

Les métadonnées se mettent en cascade exactement comme la configuration, à travers l'ordre des rôles :

```
sat  ->  collection  ->  archive  ->  directory  ->  content
```

`{author}` nomme quel palier a écrit une couche donnée. Une valeur fixée à `sat` avec `overridable: true` descend à la collection, qui peut la prendre telle que reçue ou écrire la sienne et la transmettre, et ainsi de suite jusqu'au nœud de contenu. `overridable: false` à n'importe quel palier ferme le champ à tout palier en dessous.

Donc un nœud de répertoire reçoit bel et bien des valeurs rédigées par la collection au-dessus de lui. Rien n'est caché à un nœud parce qu'il ne tient pas le rôle d'auteur, et il n'y a aucune limite d'accès ici : `{author}` enregistre quel échelon a écrit une couche, pas qui est autorisé à la voir.

« Le rôle qui l'a créé est le rôle qui l'édite » décrit le côté écriture. Le matériel d'une collection est écrit dans le `overrides/` propre à la collection, et un répertoire qui veut une valeur différente écrit la sienne plutôt que de remonter éditer celle de la collection. Cela garde intacte l'intention énoncée de chaque palier quand l'archive se déplace, ce qui est la même raison pour laquelle une redéfinition retenue contre un champ verrouillé est marquée inerte plutôt que supprimée.

Un nœud multi-rôle écrit une couche par rôle qu'il tient, et ces couches se résolvent dans l'ordre des rôles, le même ordre que la cascade utilise entre les nœuds.

## Types de champ

La config classe ses champs de trois façons et note que seule la troisième utilise `overridable` de façon significative :

| Type | Exemple | Comportement |
| --- | --- | --- |
| Vocabulaire | `roles` | Déclaré une fois à `sat`, jamais substituable |
| Structurel | `children` | Verrouillé, parce qu'un palier ne redéfinit pas ce qu'il peut contenir |
| Comportemental | `default_metadata` | En cascade par conception, délégué vers le bas sauf verrouillage |

Cette classification fonctionne parce que chaque champ de configuration prend son origine à la racine et descend. La cascade est toute l'histoire.

Les métadonnées, c'est l'inverse. La plupart des éléments Dublin Core prennent leur origine à la feuille et ne décrivent que le nœud qui les énonce, donc les trois mêmes types ne conviennent pas et les métadonnées ont besoin de leur propre tableau :

| Type | Exemple | Comportement |
| --- | --- | --- |
| Contextuel | `publisher`, `rights`, `language`, `creator` | En cascade par conception, délégué vers le bas sauf verrouillage |
| Cumulatif (accumulating) | `subject` | Fait l'union avec ce qu'il reçoit plutôt que de le remplacer |
| Local | `title`, `description`, `date`, `type`, `format` | Appartient au nœud. Jamais reçu, jamais amorcé depuis le dessus |
| Identité | `identifier`, `isVersionOf` | Local, et de plus unique au nœud |

Sur les quinze éléments, quatre ou cinq descendent et dix ne le font pas. Un `defaults/dc.yml` à un nœud de contenu tient `publisher`, `rights`, `language` et peu d'autres choses.

`[D]` **Le type d'un champ est déclaré dans la configuration, pas intégré dans le résolveur.** C'est un champ de vocabulaire au sens de la configuration : déclaré une fois à `sat`, jamais substituable, la même classe que `roles`.

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

Le résolveur connaît les types et ne connaît pas Dublin Core. Ajouter `metadata/dcterms/` est alors une déclaration plutôt qu'un changement de code, ce qui est la propriété qui rend la couche d'espace de noms digne d'exister du tout.

Un champ sans type déclaré est une erreur plutôt qu'un défaut. Deviner ferait qu'une faute de frappe dans un nom d'élément se comporte comme un nouveau champ local, silencieusement.

**Les champs locaux ne doivent pas être reçus, et l'échec est silencieux.** Si le résolveur applique `defaults` plus `overrides` uniformément, un nœud de répertoire dont le titre résolu est `"wellbeing"` transmet ce titre vers le bas comme défaut du nœud de contenu, et une ressource dont le titre propre n'a jamais été énoncé se publie comme « wellbeing ». L'archive se construit, la page se rend, et le titre est faux. Rien de tout cela ne se montre dans une archive où chaque nœud se trouve à énoncer son propre titre, ce qui est une convention qui soutient un mécanisme.

### Champs cumulatifs

`subject` est le cas où le système de fichiers porte un sens qui vaut la peine d'être gardé. Une ressource à `wellbeing/practices/meditation` se trouve sous deux ancêtres qui disent chacun quelque chose sur ce dont elle traite, et un ensemble de sujets `[wellbeing, practices]` est une meilleure description qu'un ensemble vide.

`[D]` **Un champ cumulatif est une liste de champs, pas un champ avec une valeur de liste.** Chaque élément porte la forme standard, donc `overridable` et `status` s'appliquent par élément et aucune nouvelle clé n'est inventée :

```yaml
subject:
  - value: "urn:uuid:...governance-policy"
    overridable: false
  - value: "urn:uuid:...health-services"
    overridable: true
```

### Les lignes enregistrent qui a décidé

`[D]` Dans `overrides/`, un palier peut écrire des lignes indexées par rôle. Écrire sous un rôle est la délégation, et aucune syntaxe de ciblage n'est nécessaire pour cela :

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

Un palier écrit des lignes à son propre rang ou en dessous. La ligne dit quel palier tient l'élément, `overridable` dit si le détenteur peut le transmettre plus loin, et `<notset>` dit qu'un palier a été sollicité et n'a pas répondu.

`resolved/` porte le même indexage, de sorte qu'un éditeur qui ouvre n'importe quel nœud voit quel palier a décidé quoi sans exécuter de résolveur.

Sans les lignes, un sujet énoncé délibérément par une organisation deux paliers plus haut et un sujet proposé depuis le chemin arrivent dans une seule liste, indiscernables. Un éditeur inférieur est alors invité à confirmer des décisions déjà prises au-dessus, et rien ne peut ensuite distinguer les deux.

### L'amendement atteint une ligne inférieure

Le placement couvre l'énonciation, le verrouillage, la délégation et l'invitation à décider. Il ne peut pas changer un élément qu'un palier inférieur détient déjà, parce qu'un élément est identifié par sa valeur et une remise à zéro remplace cette valeur par `<notset>`, ne laissant rien sur quoi apparier.

`[D]` **Un rôle supérieur peut amender n'importe quelle ligne en dessous du sien**, et l'amendement s'écrit distinctement parce que c'est un acte distinct :

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

Un `match` qui ne trouve rien est une erreur plutôt qu'une absence d'effet silencieuse, pour les mêmes raisons que toute référence pendante : un amendement périmé pointant vers un élément déjà retiré devrait être signalé.

**Ceci s'écarte de la règle monotone de la configuration, et l'écart est délibéré.** La configuration permet à `overridable` de rétrécir et jamais de s'élargir, donc l'autorité ne fait que se resserrer en descendant. Les métadonnées permettent à un rôle supérieur d'élargir ce qu'un rôle inférieur a rétréci, parce qu'un administrateur d'instance doit pouvoir corriger un département qui a trop verrouillé, et un département doit pouvoir corriger ses propres archives.

Deux conséquences suivent, et aucune ne devrait être découverte plus tard.

**La résolution est deux opérations, pas une.** Une valeur se met toujours en cascade vers le bas, le dernier qui écrit l'emporte. Un drapeau se résout par rang de rôle, parce qu'un palier supérieur doit l'emporter sur un palier inférieur qui a déjà rétréci. Un résolveur implémente les deux.

**L'autorité est administrative.** Chaque rôle lie tout rôle en dessous de lui et est lié par tout rôle au-dessus de lui. C'est toute la règle, et `overridable` comme `status` y obéissent.

Le verrou d'une collection lie l'archive, le répertoire et le nœud de contenu, et un rôle supérieur peut le lever. La dépréciation d'une collection lie exactement les mêmes paliers, et un rôle supérieur peut la faire revivre. Les deux se comportent de façon identique, et ni l'un ni l'autre n'est plus faible pour être révisable depuis le dessus.

Que tout ce qu'un rôle a fixé puisse être changé par un rôle au-dessus de lui est ce que signifie une hiérarchie administrative, pas une lacune de celle-ci. Une personne qui travaille sur un système administré sait que l'administrateur peut changer ce qui lui a été donné, et ses propres réglages ne sont pas pour autant consultatifs : les réglages tiennent, pour elle et pour tout le monde en dessous d'elle, jusqu'à ce que quelqu'un ayant l'autorité de les changer le fasse.

Un consommateur peut se fier à l'état résolu tel qu'il se tient, et ne peut pas supposer qu'il est permanent. Les deux moitiés sont ordinaires.

**C'est ici que les métadonnées s'écartent de la configuration.** L'autorité de la configuration est monotone : elle ne fait que se resserrer en descendant, et aucun palier ne peut relâcher ce qu'un autre a resserré. L'autorité des métadonnées est hiérarchique : elle se resserre ou se relâche selon le rang, parce qu'un administrateur doit pouvoir corriger un subordonné. Une autorité monotone est plus simple à raisonner et ne peut pas exprimer la gouvernance, ce qui est l'échange fait ici.

### Le retrait n'est pas une remise à zéro

`<notset>` signifie que personne n'a décidé, ce qui est ce qui pousse l'invite à décider. Remettre un élément à cette valeur signifie donc reconsidérer, et un éditeur est sollicité à nouveau.

`[D]` **Un élément qu'un palier veut voir disparaître est marqué `status: deprecated`.** Il reste dans le registre, montrant qu'une décision a été prise et par qui, et il est exclu de l'ensemble résolu qu'un consommateur reçoit.

```yaml
amend:
  collection:
    subject:
      - match: "urn:uuid:...deprecated-topic"
        status: deprecated        # gone from the resolved set, kept in the record
      - match: "urn:uuid:...legacy-taxonomy"
        value: "<notset>"         # sent back for reconsideration
```

Sans cette distinction, un sujet rejeté est reproposé à chaque reconstruction, parce que rien ne sépare « personne n'a décidé » de « quelqu'un a décidé contre ».

`[D]` **Faire revivre est en soi un amendement.** Effacer `status: deprecated` est un changement à un élément qu'un palier détient déjà, donc cela suit la même règle que tout autre amendement : seul un rôle au-dessus de celui qui a déprécié peut le faire. Un palier ne peut pas faire revivre ce qu'un rôle supérieur a retiré, ce qui est ce qui fait de la dépréciation un acte de gouvernance plutôt qu'une suggestion.

Un palier qui a déprécié un élément peut bien sûr le faire revivre, puisque l'amendement atteint sa propre ligne.

```yaml
amend:
  collection:
    subject:
      - match: "urn:uuid:...deprecated-topic"
        status: available         # revive; only a role above the deprecating one
```

La dépréciation se comporte donc exactement comme le verrouillage : contraignante pour tout rôle en dessous de celui qui l'a fixée, révisable par tout rôle au-dessus. Ni l'une ni l'autre n'est une exception à l'autre.

### L'amendement est enregistré

`[D]` **`resolved/` enregistre qui a amendé un élément, pas seulement qui le détient.** Un mécanisme de gouvernance dont les interventions ne laissent aucune trace ne peut pas être audité, et après que `sat` déverrouille quelque chose dans la ligne de la collection, la collection le détient toujours pendant que `sat` l'a changé. Les deux faits comptent.

```yaml
# resolved/dc.yml
subject:
  collection:
    - value: "urn:uuid:...health-services"
      overridable: true
      amendedBy: ["sat"]
```

`amendedBy` liste les rôles qui ont amendé l'élément, dans l'ordre où ils l'ont fait. Cela n'apparaît que dans `resolved/` et n'est jamais écrit à la main : un éditeur énonce des intentions dans `overrides/` et le résolveur enregistre ce qu'il a appliqué.

**C'est l'état courant, pas un journal.** Le fichier résolu dit qui a amendé un élément, pas quand, pas quelle était la valeur précédente, et pas pourquoi. Le contrôle de version tient déjà cela, avec horodatages et paternité, et le dupliquer dans l'archive mettrait le même historique à deux endroits dont un seul serait fiable.

**Des œuvres ancêtres, pas des slugs ancêtres.** Les noms de répertoires sont choisis pour les URL plutôt que comme termes d'index, donc `terms-of-service` arriverait comme sujet, et `2024` aussi. Pire pour une archive multilingue, les deux arbres de langue produisent des ensembles disjoints pour une même œuvre : l'anglais `wellbeing/practices/meditation` donne `[wellbeing, practices]` et le français `bien-etre/pratiques/meditation` donne `[bien-etre, pratiques]`, donc rien ne peut répondre à « tout sur le bien-être, dans n'importe quelle langue ».

Chaque répertoire ancêtre est un nœud avec sa propre ressource index, et ces ressources sont des expressions d'œuvres. `wellbeing/index.md` et `bien-etre/index.md` portent le même `isVersionOf`, donc le chemin se résout déjà en une chaîne d'identifiants d'œuvre indépendante de la langue. Accumuler ceux-ci donne aux deux versions linguistiques le même ensemble de sujets, avec des étiquettes d'affichage tirées du titre propre à chaque ancêtre dans la langue de lecture.

Cela produit ce que produiraient des concepts SKOS : un identifiant avec des étiquettes par langue. Cela arrive sans registre de concepts, parce que les ressources index de section font déjà ce travail.

**Une conséquence pour les répertoires organisateurs,** que la section suivante énonce comme une règle.

## Répertoires organisateurs

La configuration définit un répertoire organisateur comme celui qui ne porte aucun sidecar : pas un nœud, ne tenant aucun rôle, que la cascade traverse comme s'il n'était pas là.

`[D]` **Un répertoire organisateur peut apparaître n'importe où, et ne tient aucun contenu archivé.** La contrainte est ce qui s'y trouve, pas où il se trouve.

C'est un accommodement plutôt qu'une restriction. Une archive tient des ressources décrites, et toute collection de travail a aussi du matériel qui n'en est pas une : il existe, il appartient à l'archive, et il n'est pas l'archive. Lui donner un foyer vaut mieux que les alternatives, qui sont de décrire du matériel qui ne mérite pas de description, ou de le garder entièrement hors de l'archive, où il se perd.

Ce qui appartient à un tel répertoire :

- `bin/` et `lib/`, le logiciel d'une instance SAT
- `messages/`, les catalogues traduisant les chaînes de ce logiciel
- les binaires et artefacts compilés
- le matériel en attente d'ingestion, avant de devenir du contenu archivé
- les numérisations et captures originales, dont la ressource archivée est dérivée
- les bases de données et exports qui alimentent un processus d'ingestion
- les fichiers de travail et brouillons qui ne sont pas encore, et pourraient ne jamais devenir, des ressources

Les trois derniers sont le cas courant dans une collection d'utilisateur. Le matériel en attente d'être ingéré n'est pas encore décrit, et forcer un nœud dessus affirmerait une description que personne n'a écrite.

**La seule chose qui n'appartient pas sous un répertoire organisateur est le contenu archivé.** Une ressource là se trouverait dans un chemin où un répertoire ne contribue aucun identifiant d'œuvre, donc sa chaîne de sujets perd silencieusement un maillon et deux ressources à des profondeurs différentes acquièrent les mêmes sujets. Un lecteur signale un nœud de contenu trouvé sous un répertoire sans sidecar, et cette seule vérification applique toute la règle.

Rien d'autre n'a besoin d'être vérifié. Le matériel dans un répertoire organisateur ne participe pas à la cascade, donc la cascade n'a rien à en dire.

### La documentation propre de SAT est du contenu archivé

`sat/en/` est une archive de langue à l'intérieur de l'instance SAT, tenant la documentation de SAT. C'est du contenu, cela a des œuvres et des expressions, et chaque règle de ce document s'y applique exactement comme à l'archive d'un utilisateur.

`sat/en/messages/` se tient à côté et est un répertoire organisateur. Les documents et les catalogues vivent dans une même portée de langue sans interagir, parce que les catalogues ne sont pas du contenu archivé et que rien en dessous d'eux ne participe à la chaîne de sujets.

## Les traductions d'interface ne sont pas du contenu archivé

Un catalogue de messages n'est pas une traduction d'un document. C'est une table de correspondance indexée par chaîne source, et cela ne réalise pas une œuvre.

La distinction est déjà dans le vocabulaire de configuration : `interface_language` est un champ séparé du `language` d'une ressource, parce qu'ils répondent à des questions différentes. La disposition des fichiers suit la même scission.

`[D]` Les catalogues vivent à l'intérieur d'un répertoire organisateur niché dans l'archive de langue dont ils desservent les lecteurs, pas à l'intérieur du répertoire qui tient le logiciel. Chaque archive organise déjà ce qui est adressé aux lecteurs d'une langue, et un catalogue est exactement cela : pas de sidecars, pas d'œuvres, pas de Dublin Core.

```
en-ca/
  messages/
    LC_MESSAGES/sat.po
fr-ca/
  messages/
    LC_MESSAGES/sat.po
lib/
  locale/
    sat.pot
```

Ceci corrige une règle antérieure de ce document, qui plaçait chaque catalogue sous `lib/locale/{lang}/`. Cette règle lisait une inquiétude générale, que le logiciel n'appartient pas à l'intérieur d'une archive de langue, comme si elle couvrait aussi les catalogues, ce qu'elle ne fait pas. `en-ca/bin/example.po` reste faux, pour la raison déjà donnée : un script ou une bibliothèque n'est pas adressé aux lecteurs d'une langue, et ne le devient pas en se trouvant dans leur archive. Un catalogue n'est adressé à rien d'autre, et le placer là où le matériel propre à sa langue vit déjà n'en fait pas du contenu archivé, parce que le test pour cela n'a jamais été l'emplacement. Il ne porte aucun sidecar, n'énonce aucune œuvre, ne mine aucun identifiant : un répertoire organisateur niché à l'intérieur d'un territoire décrit, la même forme que `en/messages/` exerce déjà dans `satx`. Le gabarit, `sat.pot`, ne nomme aucune langue et est extrait des chaînes source du logiciel lui-même, donc il reste avec le logiciel à `lib/locale/`, là où `msgmerge` le trouve quand un catalogue a besoin d'être mis à jour.

L'argument pour les laisser hors du modèle d'œuvre est plus que de la propreté. Gettext résout déjà ce que le modèle d'œuvre devrait reconstruire : `msgmerge` gère le changement d'une chaîne source, `.pot` est le gabarit, et l'appariement flou signale les entrées à réviser. C'est une machinerie de dérive de traduction, mature et propre aux catalogues de messages, et la réimplémenter emmêlerait deux sortes de traduction qui se comportent différemment.

La documentation *à propos* des langues d'interface de SAT est une chose différente. C'est du contenu archivé et cela appartient à `sat/en-ca/` comme n'importe quel autre document. La ligne de partage tombe entre les chaînes elles-mêmes et le fait d'écrire à leur sujet.

## Amorçage

La configuration amorce `overrides/` une fois à l'initialisation avec les champs substituables qu'un nœud a reçus, de sorte qu'un champ verrouillé n'est jamais écrit dans le seul fichier inscriptible et n'invite jamais une édition que la résolution rejetterait.

Les métadonnées inversent la moitié utile de cela. Amorcer un nœud de contenu avec le `publisher` et le `rights` qu'il n'a aucune raison de changer remplit le fichier de bruit, tandis que les champs dont il a réellement besoin, `title` et `date`, sont absents parce que rien au-dessus ne les a déclarés. Les champs locaux sont ce qu'un nœud de contenu écrit, et ce sont exactement ceux qu'une règle d'amorçage par champs reçus omettrait.

L'identité est l'exception. `identifier` n'est pas amorcé comme `<notset>`, parce qu'un UUID n'est pas quelque chose qu'un éditeur tape. Il est miné à la création du nœud, par le rôle qui le crée.

`[D]` **L'autorité de miner se met en cascade par rôle.** `sat` mine pour `sat`, puis transmet ses exigences et ses défauts à `collection`, qui mine les collections ; `collection` transmet à `archive`, et ainsi de suite vers le bas. Le minage est délégué exactement comme tout autre champ comportemental l'est, donc l'identité est le seul champ local qui arrive avec une valeur plutôt qu'une sentinelle.

Tout le reste des champs locaux s'amorce comme `<notset>`, et les valeurs dérivées s'amorcent comme des propositions :

```yaml
title:
  value: "<notset>"
subject:
  value: ["urn:uuid:...wellbeing-work", "urn:uuid:...practices-work"]
  merge: append
```

`[D]` La chaîne inclut l'archive elle-même. `en-ca/wellbeing/practices/meditation` a `en-ca` comme nœud ancêtre avec une œuvre, et cela s'accumule comme n'importe quoi d'autre. Que ce soit utile ou du bruit est un jugement que chaque archive porte, donc cela arrive substituable à chaque rôle et un éditeur confirme ou retire.

Une chaîne de sujets dérivée est une proposition plutôt qu'un fait. Un éditeur est invité à la confirmer ou à l'amender, ce qui est la même invitation que `<notset>` pousse déjà en configuration. Qu'une feuille s'inclue elle-même dans son propre ensemble de sujets est un cas pour cette invitation plutôt qu'une règle : sensé pour `meditation.md`, dont le titre est son sujet, et faux pour `privacy-policy.md`, dont le sujet est la vie privée plutôt que la politique.

## Chaque espace de noms se matérialise à chaque nœud

La configuration règle cela et cela se transmet sans changement : chaque dossier de rôle à chaque nœud porte un ensemble de répertoires à trois états, et la résolution ne se soucie pas de savoir si quoi que ce soit a été édité. Donc un nœud matérialise chaque espace de noms déclaré, qu'il y rédige quelque chose ou non.

Un nœud de contenu a donc `sat/defaults/`, `sat/overrides/` et `sat/resolved/` même si les deux champs d'identité de `sat` lui sont locaux. Son `sat/defaults/sat.yml` est vide, correctement : rien au-dessus de lui n'a quoi que ce soit à transmettre vers le bas.

Un `defaults/` vide n'est pas un `defaults/` manquant, et un lecteur ne doit pas traiter les deux de la même façon. Absent signifie que l'espace de noms n'a jamais été déclaré. Vide signifie qu'il a été déclaré et que rien n'y est descendu.

## Espaces de noms

**`dc`** est Dublin Core 1.1, les quinze éléments de l'espace de noms `/elements/1.1/`. Chaque élément est optionnel et chaque élément est répétable, donc les valeurs sont des listes.

**`dcterms`** est DCMI Metadata Terms, le vocabulaire plus tardif et plus large avec domaines et portées déclarés. Non interchangeable avec `dc` : `dc:date` et `dcterms:date` sont des propriétés différentes. Réservé, pas encore utilisé.

**`sat`** tient ce dont SAT a besoin et pour quoi DC n'a pas de mot. Là où DCTERMS a un terme correspondant, la propriété `sat` prend son nom local, et SAT ne forge un terme que pour ce que DCTERMS ne peut pas dire.

À un nœud de contenu, `sat` porte `identifier`, le `urn:uuid` propre à la ressource, et `isVersionOf`, le `urn:uuid` de l'œuvre qu'elle réalise. Deux expressions d'une œuvre portent le même `isVersionOf` et des valeurs `identifier` différentes. C'est tout le mécanisme par lequel une traduction est une traduction : pas la correspondance des titres, qui diffèrent, et pas la correspondance des chemins, qui diffèrent aussi.

## L'identité ne se met pas en cascade

Tout le reste de l'arbre des métadonnées descend par défaut. L'identité ne doit pas le faire, et c'est une exclusion dure plutôt qu'un défaut qui peut être outrepassé.

**`identifier`** nomme une ressource. Un enfant qui hériterait de l'identifiant de son parent prétendrait être son parent.

**`isVersionOf`** nomme l'œuvre qu'une ressource réalise. Un enfant qui en hériterait deviendrait une expression de l'œuvre de son parent, ce qui ferait d'un index de section et de chaque document en dessous des traductions les uns des autres. L'échec est silencieux : l'archive se construirait, le sélecteur se rendrait, et chaque lien serait faux.

Les deux sont énoncés au nœud auquel ils appartiennent, dans le `overrides/` de ce nœud, et jamais reçus d'en haut. Un résolveur qui parcourt la cascade de métadonnées les exclut de la fusion plutôt que de compter sur chaque nœud pour les reformuler.

Le même raisonnement s'applique à tout champ qui nomme une ressource plutôt que de décrire une classe d'entre elles.

## Forme du champ

Un champ de métadonnées porte sa valeur et l'autorité qui la gouverne, dans la même forme que la configuration utilise :

```yaml
# .areas.md.assets/content/metadata/dc/overrides/dc.yml
title:
  value: ["Areas"]
  overridable: true
description:
  value: ["What we maintain an ongoing standard in."]
  overridable: true
```

`overridable` est monotone. Il peut rétrécir de vrai à faux à n'importe quel nœud et jamais s'élargir, donc une valeur verrouillée au-dessus ne peut pas être rouverte en dessous.

`status` enregistre où un champ ou un élément se trouve dans son cycle de vie, de sorte que de nouvelles choses puissent être introduites et d'anciennes retirées sans rupture de version.

`[D]` `deprecated` a un comportement. Un élément déprécié reste dans le registre et est exclu de l'ensemble résolu qu'un consommateur reçoit. Ceci remplace une règle antérieure selon laquelle rien ne conditionne sur `status`, et est noté ici parce qu'une implémentation écrite contre cette règle-là devra changer. Le changement se limite à cette seule valeur.

`[D]` `planned` n'en a aucun. Un résolveur l'enregistre et le transmet, et rien n'agit dessus. Cela reste délibéré.

Une redéfinition retenue contre un champ verrouillé en amont est signalée et marquée inerte plutôt que supprimée, de sorte que l'intention énoncée d'un archiviste survive à une migration qui déverrouille plus tard le champ.

## Guillemets

Les clés de langue et les slugs sont mis entre guillemets, toujours. Sous YAML 1.1, `no` est à la fois un booléen et le code ISO 639-1 du norvégien, donc une clé norvégienne sans guillemets s'analyse en `false` sans erreur et sans rien de visible dans le fichier. `y`, `on` et `off` se comportent de la même façon, et un slug numérique nu s'analyse en entier et cesse de correspondre à la chaîne qu'il nomme.

À analyser comme YAML 1.2, qui a abandonné cet ensemble de booléens. Le `yaml` de Node et `js-yaml` v4 sont sûrs par défaut ; PyYAML ne l'est pas.

## États

Trois choses se transmettent depuis la configuration sans changement, et sont énoncées ici afin qu'un lecteur de ce seul document n'ait pas à les inférer.

`resolved/` se matérialise à chaque nœud. `resolved/` à un nœud et `defaults/` au suivant tiennent le même contenu, ce qui rend la cascade inspectable à chaque nœud sans exécuter de résolveur et réduit la génération des défauts d'un enfant à une copie plutôt qu'à une fusion.

Un nœud qui n'a rien à dire se résout quand même. La résolution ne se soucie pas de savoir si quoi que ce soit a été édité : sans édition, `resolved/` est égal à `defaults/`.

`defaults/` et `resolved/` sont tous deux en lecture seule et ne sont pas le même genre d'artefact. `defaults/` est une entrée reçue et doit être préservé. `resolved/` est une sortie dérivée, sûre à supprimer, et toujours reconstructible à partir des deux fichiers à côté d'elle.

## Un seul résolveur

La configuration et les métadonnées sont composées par la même opération : lire `defaults/`, lire `overrides/`, appliquer les deltas permis, écrire `resolved/`. Seul le chemin diffère, la configuration portant deux axes de rôle et un dossier de sujet là où les métadonnées portent un axe de rôle et un dossier d'espace de noms, donc la différence se limite à la façon dont un fichier est remis au résolveur plutôt qu'à ce qu'il en fait.

Il y a une implémentation, pas deux tenues synchronisées. Les types de champ ci-dessus sont des données que le résolveur lit, pas un second chemin de code.

## Ouvert

**Le dispositif d'ingestion est périmé.** Il utilise `metadata/dc/dc.yml` sans répertoire d'état et des valeurs scalaires nues, et ne porte aucun espace de noms `sat/`. Un nouveau dispositif est nécessaire plutôt qu'une extension de celui-là.

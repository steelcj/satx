# La pile en couches : modéliser une archive de contenu multi-axes

**Version.** v0.0.4, 2026-09-09. Remplace v0.0.3.

**Portée.** Ce document décrit l'archive au repos, comment le contenu et ses métadonnées sont organisés, ce qui identifie un élément de contenu, et ce qui le relie à ses variantes. La sérialisation, la génération d'URL, et la livraison à un générateur de site particulier sont des préoccupations en aval et hors de portée. Concevoir la structure autour d'un consommateur est ce qui fait que la structure finit par avoir la forme d'un outil plutôt que celle du contenu.

**Prémisse.** Aucun vocabulaire unique n'est suffisant, et en chercher un est l'erreur. RDF est additif : une ressource peut porter plusieurs types et propriétés de plusieurs vocabulaires sans conflit, sans règles de préséance, et sans perte. La question de conception n'est pas *quelle norme* mais *à quelle couche appartient chaque norme*, et si les couches sont complètes.

**Deuxième prémisse, arrivée tard et qui vaut la peine d'être énoncée en premier.** La langue n'est pas le modèle. C'est un axe selon lequel une œuvre varie, et il se trouve que c'est le premier dont on a eu besoin. Une version en lecture facile d'une page est la même sorte de chose qu'une traduction de celle-ci : une expression différente d'une même œuvre. Une conception construite spécifiquement autour de la langue devra être démolie à l'arrivée du second axe. Une conception construite autour des *axes*, avec la langue comme premier, ne le sera pas.

**Troisième prémisse, nouvelle dans cette version.** Le modèle est multi-axes. Le système de fichiers ne l'est pas. Les racines d'archive sont des arbres de langue et rien d'autre ; toute autre coordonnée est déclarée dans le front matter. Les deux affirmations sont compatibles parce que les coordonnées n'ont jamais été un fait du système de fichiers en premier lieu, et les séparer supprime toute une classe de décisions plutôt que d'y répondre.

| Couche | Objet | Recommandation |
| --- | --- | --- |
| Modèle conceptuel | Quelles sortes de choses existent et comment elles se relient | **IFLA LRM** (WEMI) |
| Vocabulaire d'entités | Ces sortes et relations, en RDF | **OpenWEMI** + un raffinement local |
| Propriétés descriptives | Titres, dates, descriptions, droits | **dcterms** |
| Axes et vocabulaires de valeurs | Coordonnées, sujets, rôles | **SKOS**, MARC Relators, BCP-47 |
| Provenance | Qui a fait quelle version, à partir de quoi | **PROV-O** (optionnel) |
| Consommation | Ce que lisent les machines hors de l'archive | **schema.org** (émis, jamais rédigé) |
| Profil | Quelles propriétés sont requises où | **DCTAP** → SHACL |

Seul le premier est un modèle. Le reste sont des vocabulaires, et ils se composent.

## Changements dans cette version

Tout ce qui figure dans cette section est développé plus loin. Elle est là pour qu'un lecteur de la v0.0.2 puisse voir ce qui a bougé sans tout relire.

- **Une section était mal nommée.** « Où appartient une variante » répondait à la question de savoir sur quel niveau WEMI une variante atterrit, et se lisait comme si c'était une question d'emplacement. Elle s'appelle maintenant « À quel niveau appartient une variante », et dit clairement que chaque variante de niveau Expression vit sur le système de fichiers comme n'importe quelle autre page.
- **Chaque axe garde son registre.** La v0.0.2 pouvait se lire comme si retirer le registre du système de fichiers le rétrogradait. Ce n'est pas le cas. `axes/register.yaml` est le même genre de fichier que `axes/language.yaml`, et `lsq` est une langue exactement comme `fr-ca` en est une. Ce qui diffère, c'est quel axe est l'axe racine, pas quel axe est réel.
- **Les variantes se nomment elles-mêmes, dans leur propre langue.** Une coordonnée non par défaut déclare un jeton de slug par langue dans son registre, de sorte que la même coordonnée est `areas-easy-read.md` en anglais et `domaines-lecture-facile.md` en français. Le slug de base survit, la coordonnée reste la source de vérité, et l'analyse vérifie que le nom de fichier et les coordonnées s'accordent.
- **La décision sur la Manifestation est close.** La ligne de partage se fait entre rédigé et généré, pas entre système de fichiers et non-système de fichiers. Les incarnations générées sont une sortie de construction et ne reçoivent aucun nœud ; une incarnation rédigée est déclarée et devient une manifestation réelle.
- **La racine de l'arbre n'a jamais été une décision.** Une page à la racine d'un arbre de langue a un chemin de slug vide et est adressée à la racine de la langue, de la même façon dans chaque langue. La v0.0.2 l'a soulevée par erreur comme une question ouverte.
- **Une coordonnée est une métadonnée de ressource, et le front matter en est une projection.** La v0.0.3 dit qu'une coordonnée non racine est « déclarée dans le front matter », ce qui est vrai du fichier qu'un auteur lit et faux de l'endroit où la valeur est conservée. Dans une archive SAT, le front matter est une ingestion générée ; la coordonnée est rédigée dans le sidecar propre à la ressource. La nouvelle section le dit et réconcilie `_defaults.yaml` avec la cascade de métadonnées de SAT, qui étaient le même mécanisme sous deux orthographes.
- **Les coordonnées ne se mettent jamais en cascade, et l'axe racine le fait toujours.** C'était implicite et c'est maintenant une règle. Une cascade de métadonnées permettrait mécaniquement `register: easy` sur un nœud de répertoire, et le permettre remettrait l'identité d'une expression sous le contrôle de l'endroit où se trouve son fichier, ce qui est précisément le couplage que cette version a supprimé.
- **Deux sortes de défaut qui se ressemblent sont séparées.** Un axe omis prend le défaut déclaré sur l'axe, pas un défaut hérité d'un nœud ancêtre. Dans un système dont tout l'idiome est la cascade, cette distinction doit être énoncée ou elle sera présumée.
- **La dérive est calculée à partir de sommes de contrôle.** Git verse déjà tout, donc rien n'a besoin d'être rédigé : comparer le blob source tel qu'il se tenait au dernier commit de la traduction avec le blob source maintenant. La proposition d'enregistrer une source versionnée dans `translationOf` est retirée ; un condensé enregistré ne survit que comme filet de sécurité pour un historique peu fiable.

## Le modèle : IFLA LRM

**FRBR** (1998) est un modèle entité-relation publié par l'IFLA, décrivant les ressources bibliographiques du point de vue de l'utilisateur : trouver, identifier, sélectionner, obtenir. Sa valeur est qu'il se tient au-dessus de tout code de catalogage : AACR, RDA et ISBD l'implémentent tous ; aucun d'eux ne l'est.

**IFLA LRM** <a id="cite-riva-2017"></a>([Riva et al., 2017](#ref-riva-2017)) le remplace. Il consolide FRBR avec FRAD (données d'autorité) et FRSAD (données d'autorité de sujet) en un seul modèle. FRBR, FRAD et FRSAD sont tous formellement remplacés, donc il faut citer LRM et traiter FRBR comme de l'histoire plutôt que comme la norme actuelle.

**LRMoo** (1.0, approuvé en avril 2024) est LRM exprimé comme une ontologie formelle, alignée sur CIDOC-CRM afin que les descriptions de bibliothèques et de musées interopèrent. Il succède à FRBRoo 2.4.

WEMI est l'acronyme des quatre entités qui survivent à travers tout cela :

| Entité | Définition | Dans l'archive |
| --- | --- | --- |
| **Œuvre (Work)** | Le contenu intellectuel abstrait | Le contenu « domaines », indépendant de la langue |
| **Expression** | Une réalisation de l'œuvre | Le texte anglais ; le texte français ; le texte anglais en lecture facile |
| **Manifestation** | L'incarnation d'une expression | La source Markdown ; un rendu HTML ; un PDF |
| **Item** | Un exemplaire unique | Une copie d'une manifestation. Rarement significatif ici. |

Une œuvre est *réalisée à travers* une expression, une expression est *incarnée dans* une manifestation, une manifestation est *exemplifiée par* un item.

## Où se trouve réellement l'archive

C'est la correction dont tout le reste découle, et il est facile de la passer.

**Les fichiers sont des manifestations.** `en-ca/areas.md` n'est pas le texte anglais ; c'est *une incarnation* du texte anglais en Markdown. Rendez-le en HTML et vous avez une deuxième manifestation de la même expression. Imprimez-le et vous en avez une troisième. Rien au-dessus du niveau du fichier n'existe sur le système de fichiers, ce qui est exactement pourquoi les métadonnées doivent le porter.

**La langue est une propriété de l'Expression.** Pas de l'œuvre, qui est indépendante de la langue par définition. Pas de la manifestation, parce que la source Markdown et le rendu HTML sont tous deux en anglais, et ce n'est ni l'un ni l'autre qui est l'endroit où ce fait appartient.

**Et la langue n'est pas la seule propriété de ce genre.** Le registre en est une autre : une version en lecture facile a des mots différents, donc c'est une expression différente de la même œuvre, exactement comme l'est une traduction. La taxonomie de Tillett <a id="cite-tillett-1991"></a>([Tillett, 1991](#ref-tillett-1991)) met la traduction et la simplification côte à côte comme des relations dérivatives ; ni l'une ni l'autre n'est subordonnée à l'autre. La modalité est une troisième : une narration audio réalise l'œuvre encore différemment.

Donc une expression n'est pas identifiée par une langue. Elle est identifiée par une **œuvre plus une coordonnée sur chaque axe que l'archive reconnaît** :

```
work (œuvre) :          le contenu abstrait
expression:              œuvre × langue × registre × …
manifestation:           un fichier, un rendu, une impression
item:                    une copie
```

La langue est l'axe un. Rien dans la conception ne devrait supposer qu'elle est la seule, et le coût de cette supposition n'est pas hypothétique : c'est une réécriture de chaque résolveur le jour où une version en lecture facile est commandée.

### À quel niveau appartient une variante

C'est une question sur le modèle, pas sur le système de fichiers. Chaque variante de niveau Expression vit dans un arbre de langue à côté des pages dont elle varie, exactement comme n'importe quelle autre page ; ce qui se décide ici est de savoir si une variante donnée est une nouvelle expression du tout, ou la même expression incarnée différemment. Le test est de savoir si **le texte a changé** :

| Variante | Niveau | Pourquoi |
| --- | --- | --- |
| Traduction | Expression | Mots différents |
| Lecture facile | Expression | Mots différents |
| Narration audio | Expression | Réalisation différente |
| Gros caractères | Manifestation | Mêmes mots, incarnation différente |
| Braille | Manifestation | Mêmes mots, incarnation différente |
| PDF du HTML | Manifestation | Mêmes mots, incarnation différente |

Se tromper ici coûte cher dans les deux sens. Traiter une manifestation comme une expression et le même texte est rédigé deux fois. Traiter une expression comme une manifestation et son contenu distinct n'a nulle part où vivre.

Notez ce que signifie la colonne de droite en pratique. Tout ce qui est dans la moitié supérieure de ce tableau est une page dans un arbre de langue avec une coordonnée déclarée. Tout ce qui est dans la moitié inférieure n'est pas une page du tout, et la question de savoir quand ceux-ci deviennent des enregistrements réels est traitée sous « Quand la Manifestation devient réelle ».

### La conséquence pour les identifiants

Trois niveaux signifient trois espaces d'identifiants, et un seul d'entre eux est rédigé.

```
work (œuvre) :          un UUID, miné une fois, écrit dans le front matter
expression:              dérivé, UUID de l'œuvre + coordonnées
manifestation:           dérivé, le fichier, ou l'URL d'un rendu
```

Les identifiants d'expression n'ont besoin d'aucun registre, parce qu'une œuvre plus ses coordonnées en détermine un. Cela découle du fait que les axes sont positionnels, et cela signifie que le modèle plus riche ne coûte rien au moment de la rédaction.

## Le système de fichiers n'est pas l'espace des coordonnées

La v0.0.1 mettait tout l'ensemble de coordonnées dans le premier segment de chemin, `en-ca__easy/`, puis passait une page de décisions ouvertes sur comment l'encoder. La prémisse était fausse. Les coordonnées identifient une expression ; elles n'ont pas à être l'endroit où vit le fichier.

**Un axe est réalisé comme des répertoires, et c'est la langue.** Un arbre de langue est une véritable frontière éditoriale. Il a sa propre organisation, ses propres slugs, sa propre profondeur, souvent son propre responsable, et c'est l'unité qu'on remet à un traducteur ou qu'on extrait vers une autre instance SAT. Le registre n'est pas cela. Une page en lecture facile est une variante d'une page à l'intérieur de l'organisation d'une langue, et elle appartient à côté de la page dont elle varie.

**Ce n'est pas une rétrogradation des autres axes.** Chaque axe a un registre dans `axes/`, de la même forme, résolu par le même code, et en ajouter un est un fichier YAML plus une ligne dans `archive.yaml`. `axes/register.yaml` est aussi réel que `axes/language.yaml`, et `lsq` est une langue exactement comme `fr-ca` en est une ; rien à propos d'une langue des signes n'en fait la variante de quoi que ce soit d'autre. La seule asymétrie est qu'un axe doit être celui pour lequel les répertoires sont nommés, et la langue est celui qui le mérite.

**Tout autre axe est déclaré dans le front matter**, en un bloc, sous `coordinates:`.

```
en-ca/
  areas.md              langue en-ca depuis la racine, registre standard par défaut
  areas-easy-read.md    langue en-ca depuis la racine, registre easy tel que déclaré
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

L'identité n'est pas affectée par l'endroit où se trouve le fichier. Cette expression est toujours `œuvre × langue=en-ca × registre=easy`, a toujours le même identifiant dérivé, et apparaît toujours dans la même cellule de la matrice de couverture que lorsqu'elle vivait dans sa propre racine. La table des UUID, les relations entre pages sœurs, et la sélection sont toutes inchangées.

Ce qui change, c'est tout ce que le chemin faisait mal.

**Il n'y a aucun encodage de coordonnées à décider.** Séparateur contre imbrication était une question sur la mise de plusieurs valeurs dans un seul chemin. Avec une seule valeur, il n'y a aucun séparateur à convenir, aucun ordre canonique à imposer dans un nom de répertoire, et aucun risque d'archive mixte inanalysable.

**Les espaces de noms des axes deviennent indépendants.** Les deux encodages de chemin devaient tous deux résoudre un segment en le recherchant à travers tous les axes, ce qui exigeait que les clés de valeur d'axe soient uniques à travers toute l'archive. Cette contrainte a disparu. La langue possède l'espace de noms du chemin ; tout autre axe est indexé par son propre nom dans le front matter. Une valeur de registre peut maintenant s'écrire de la même façon qu'une valeur de langue sans aucune ambiguïté nulle part.

**Le contenu ne peut plus être confondu avec une coordonnée.** Sous l'imbrication, un répertoire de page légitimement nommé `easy` à l'intérieur de `en-ca/` était lu comme une coordonnée de registre, et la page perdait silencieusement son slug. Il n'y a pas d'échec équivalent quand le contenu n'occupe jamais le premier segment.

**Les défauts de section atteignent chaque variante.** `en-ca/about/_defaults.yaml` s'applique maintenant aux expressions en lecture facile de cette section, parce qu'elles sont dans cette section. Sous les ensembles de coordonnées à la racine, `en-ca__easy` était un arbre séparé qui avait besoin de sa propre copie des mêmes défauts.

**Le coût, énoncé clairement.** Les variantes d'une page partagent un répertoire, donc elles ont besoin de noms de fichiers distincts. C'est une question de nommage plutôt que d'identité, et elle trouve réponse sous « Slugs de variante » : la coordonnée déclare un jeton par langue, le nom de fichier le porte, et le slug de base est ce qui reste quand le jeton est retiré. La résolution à travers les variantes passe par l'identité de l'œuvre plus les coordonnées dans tous les cas.

**L'ensemble d'axes fermé est appliqué en deux endroits plutôt qu'un.** Une racine d'archive non déclarée est une langue non déclarée. À l'intérieur de `coordinates:`, un nom d'axe non déclaré, une valeur non déclarée, ou l'axe racine qui apparaît du tout, sont chacun des erreurs. Il en va de même pour un nom d'axe écrit au niveau supérieur du front matter plutôt qu'à l'intérieur du bloc, parce que c'est l'erreur probable et qu'elle serait autrement silencieuse.

## Les coordonnées dans une archive SAT

La section précédente dit qu'une coordonnée non racine est déclarée dans le front matter. C'est vrai du fichier qu'un auteur ouvre et faux de l'endroit où la valeur est conservée, et la différence compte une fois que ce modèle est réalisé sur SAT plutôt que décrit seul.

### Le front matter est une projection

Dans une archive SAT, les métadonnées canoniques d'une ressource vivent dans son sidecar, et le front matter est généré pour l'ingestion et écrasé à chaque exécution. Une coordonnée est donc rédigée ici :

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

et elle apparaît dans le front matter comme `coordinates: {register: easy}` parce que c'est ce qu'un moteur de gabarits peut lire. Rien ne change au modèle ; la phrase « déclarée dans le front matter » devient « déclarée sur la ressource », et la ressource est un nœud avec un sidecar plutôt qu'un fichier avec un en-tête.

Une conséquence mérite d'être nommée plutôt que découverte. `en-ca/about/_defaults.yaml` dans la disposition ci-dessus et le `metadata/dc/overrides/dc.yml` d'un nœud de répertoire sont le même mécanisme sous deux orthographes. Une archive devrait en garder un seul. Sur SAT, c'est le sidecar qui l'emporte, parce que c'est là où la cascade regarde déjà et parce qu'un second mécanisme de défauts aurait besoin de ses propres règles de préséance contre le premier.

### Les coordonnées ne se mettent jamais en cascade ; l'axe racine le fait toujours

Les deux axes sont gérés par des règles opposées, et l'asymétrie est délibérée.

**L'axe racine est positionnel et hérité.** `language` est déclaré une fois au nœud de l'archive, verrouillé là, et reçu par chaque nœud en dessous à travers la cascade de métadonnées. Aucun nœud de contenu ne le reformule, et un nœud de contenu qui contredirait sa propre archive serait une erreur.

**Toute autre coordonnée est déclarée sur la ressource et n'hérite de rien.** Un nœud de répertoire ne doit pas déclarer `register`, et un résolveur qui en rencontre un devrait le rejeter plutôt que de l'appliquer.

Le mécanisme le permettrait : une cascade de métadonnées fait descendre tout ce qu'on lui donne, et `register: easy` sur `en-ca/plain-language/` atteindrait chaque fichier en dessous. La raison de refuser est que cela ferait dépendre l'identité d'une expression de l'endroit où se trouve son fichier. Déplacez le fichier et ses coordonnées changent ; déplacez-le à nouveau et elles changent encore. C'est précisément le couplage que cette version a supprimé en retirant les coordonnées du système de fichiers, et le réintroduire par la cascade serait le même défaut portant un autre chapeau.

Le coût est la répétition. Quarante pages en lecture facile dans une section portent les deux mêmes lignes quarante fois, et aucune valeur héritée ne peut les raccourcir. Cette répétition est ce qui rend sûr de déplacer n'importe lequel de ces fichiers, ce qui est l'échange fait ici. Fournir les lignes est une préoccupation d'outil de rédaction, pas de modèle : un gabarit, un `sat content new --register easy`, ou un défaut de collection Sveltia écrivent tous la valeur à la ressource où elle appartient.

### Deux sortes de défaut qui se ressemblent

Un axe omis est rempli à partir du défaut déclaré sur l'axe, dans `axes/register.yaml`. Ce n'est pas un défaut mis en cascade et cela ne vient pas d'un nœud ancêtre.

| | Où c'est déclaré | De quoi c'est une propriété | Pareil partout ? |
| --- | --- | --- | --- |
| Défaut d'axe | le registre de l'axe | l'axe | oui |
| Défaut en cascade | le sidecar d'un nœud ancêtre | la position dans l'arbre | non |

Les coordonnées n'utilisent que le premier. Dans un système dont l'idiome est la cascade, cela doit être énoncé ou ce sera présumé : `default_coordinates: fill` se lit comme une règle d'héritage et n'en est pas une. Cela dit qu'une coordonnée non énoncée se résout à la valeur déclarée de l'axe, identiquement à chaque position dans chaque arbre, avec `asserted: false` enregistré pour que la valeur remplie soit distinguable d'une valeur énoncée.

Les métadonnées descriptives sont l'inverse. `rights`, `publisher`, `audience` et `subject` sont exactement ce à quoi sert une cascade, et elles héritent d'où qu'elles soient déclarées. La règle n'est pas « les métadonnées SAT ne se mettent pas en cascade » ; c'est que les métadonnées porteuses d'identité ne le font pas, et les coordonnées sont porteuses d'identité parce qu'une expression est une œuvre à un ensemble d'entre elles.

### Ce que cela rend vérifiable

Quatre erreurs découlent des règles ci-dessus, et chacune est autrement silencieuse :

- une coordonnée déclarée à un nœud qui n'est pas un nœud de contenu
- l'axe racine apparaissant dans les coordonnées d'un nœud de contenu, là où l'archive le détermine déjà
- un nœud de contenu dont le `language` reçu est en désaccord avec l'archive dans laquelle il se trouve
- un nom d'axe écrit au niveau supérieur des métadonnées d'une ressource plutôt que sous le bloc de coordonnées, ce qui est l'erreur de rédaction probable

### Où se trouvent les registres d'axes

`archive.yaml` et `axes/` sont une autorité à l'échelle de la collection, au-dessus des arbres de langue et en dessous de toute collection englobante. Cela correspond à l'endroit où se trouve un registre d'œuvres : une œuvre appartient à un site plutôt qu'à un dossier de sites, et il en va de même pour l'ensemble d'axes selon lequel les expressions de ce site sont indexées. Une collection de collections peut déclarer des axes que ses membres héritent, aux mêmes conditions que toute autre valeur mise en cascade ; un membre qui a besoin d'un axe que son parent n'a pas le déclare et le possède.

## Choisir le vocabulaire d'entités

dcterms ne peut pas porter le modèle. Il a 55 propriétés et presque aucune classe : il n'y a pas de `dcterms:Work`, seulement `dcterms:BibliographicResource`, qui couvre l'Œuvre et l'Expression et ne distingue ni l'une ni l'autre. Il n'y a pas non plus de propriétés pour les relations WEMI elles-mêmes, pas de `dcterms:realizedThrough`. Les relations `isVersionOf` et `hasVersion` donnent une approximation utilisable, mais ce sont des approximations, et le modèle reste implicite dans la façon dont on se trouve à les utiliser.

Cinq candidats réels comblent cet écart.

| Vocabulaire | Modèle | Verdict |
| --- | --- | --- |
| **OpenWEMI** (DCMI) | W/E/M/I, minimalement contraint | **Recommandé.** Conçu exprès pour cela |
| **LRMoo** | LRM comme extension de CIDOC-CRM | Correct mais maximal. Seulement pour l'intégration CRM |
| **RDA Registry** | Fidèle à LRM, catalogage de bibliothèque | Excellente cible de correspondance, mauvais vocabulaire de rédaction |
| **BIBFRAME 2.x** | Œuvre / Instance / Item | **Mauvaise forme pour ce problème** |
| **FRBR Core** (2005) | W/E/M/I, léger | Remplacé en pratique par OpenWEMI |

### OpenWEMI

Un vocabulaire DCMI à `https://ns.dublincore.org/openwemi/`, publié pour permettre à des communautés hors des bibliothèques d'utiliser WEMI sans hériter de la sémantique du catalogage de bibliothèque <a id="cite-coyle-2022"></a><a id="cite-coyle-2025"></a><a id="cite-dcmi-2024"></a>([Coyle, 2022](#ref-coyle-2022), [2025](#ref-coyle-2025) ; [DCMI, 2024](#ref-dcmi-2024)). Il définit les quatre classes plus une superclasse de regroupement `Endeavor`, et il retire délibérément les règles de disjonction et la linéarité stricte de FRBR.

Les relations :

- `expresses` / `expressedBy`, de l'Expression à l'Œuvre
- `manifests` / `manifestedBy`, de la Manifestation à l'Expression ou à l'Œuvre
- `instantiates` / `instantiatedBy`, de l'Item à n'importe lequel des précédents
- `relatedWork`, `relatedExpression`, `relatedManifestation`, `relatedItem`, relations de même niveau
- `commonWork`, `commonExpression`, et ainsi de suite, qui affirment que deux ressources partagent un niveau sans typer ni l'une ni l'autre

`relatedExpression` est la relation de pages sœurs dont l'archive a besoin, et `commonWork` est la façon dont un jeu de données externe peut apprendre que deux de ses ressources sont la même œuvre que la nôtre sans adopter aucune de nos modélisations.

OpenWEMI est explicitement conçu pour être **sous-classé**. C'est l'usage prévu, pas un contournement, et c'est ce qui rend le vocabulaire propre à l'archive légitime plutôt qu'idiosyncrasique :

```turtle
@prefix arc: <https://example.org/ns/> .
@prefix owemi: <https://ns.dublincore.org/openwemi/> .

arc:LanguageExpression  rdfs:subClassOf  owemi:Expression .
arc:translationOf       rdfs:subPropertyOf  owemi:relatedExpression ;
                        rdfs:subPropertyOf  dcterms:source .
```

Un consommateur qui ne connaît qu'OpenWEMI comprend quand même `arc:translationOf` comme une expression liée. Un consommateur qui ne connaît que dcterms le comprend quand même comme une source. Aucun des deux n'a besoin de rien savoir de local. C'est tout l'argument en faveur du raffinement plutôt que de l'invention.

### Pourquoi pas les autres

**LRMoo** est la réponse correcte maximale et le mauvais outil ici. Il est centré sur les événements : créer une expression est un événement `F28 Expression Creation` avec des participants et une durée. Cette machinerie est précieuse pour le patrimoine culturel, puisqu'elle permet de dire qui a fait quoi quand, à travers des institutions, et c'est beaucoup de structure à porter pour une archive dont les événements de création sont « quelqu'un a écrit une page ». À adopter si l'archive doit fédérer avec des données CIDOC-CRM. Sinon, le coût est réel et le bénéfice est spéculatif.

**RDA Registry** est fidèle à LRM, activement maintenu, et a de véritables classes (`rdac:Work`, `rdac:Expression`). Ses IRI de propriétés sont des numériques opaques, `rdaw:P10078` est « a pour expression de l'œuvre », ce qui convient aux données machine et est hostile au front matter rédigé à la main. Il porte aussi des suppositions de catalogage dont l'archive n'a pas l'usage. À traiter au mieux comme quelque chose vers quoi *faire correspondre*, si l'archive doit un jour parler à des systèmes de bibliothèque, pas comme le vocabulaire dans lequel on écrit.

**BIBFRAME** mérite une rétractation précise. Des versions antérieures de ce document suggéraient `bf:Work` comme un moyen bon marché de typer l'œuvre. C'était une erreur. BIBFRAME a trois niveaux, Work, Instance et Item, et il replie l'Expression dans le Work. Les versions linguistiques dans BIBFRAME sont des Works séparés joints par `bf:translationOf`. Pour la plupart des catalogues, cette simplification est défendable. Pour une archive dont tout le principe organisateur est la scission œuvre/expression, elle effondre précisément la distinction en cours de modélisation. Ne pas l'utiliser ici.

**FRBR Core** <a id="cite-davis-2005"></a>([Davis & Newman, 2005](#ref-davis-2005)) est le vocabulaire RDF léger dont OpenWEMI est vaguement issu, et il n'est plus maintenu. OpenWEMI en est le descendant maintenu, avec un soutien institutionnel.

## Vocabulaires de valeurs

Les propriétés n'en sont que la moitié. Ce qu'on y met compte tout autant, et c'est là que les archives multilingues fuient habituellement.

### Les sujets devraient être des concepts, pas des chaînes

`subject: [areas, practice standards]` en anglais et `subject: [domaines, normes de pratique]` en français sont deux listes de chaînes sans rapport. Rien ne les relie, donc rien ne peut répondre à « montre-moi tout sur ce sujet, dans n'importe quelle langue ».

Le remède est le même mouvement fait un niveau plus bas : un sujet est un **concept SKOS** <a id="cite-miles-2009"></a>([Miles & Bechhofer, 2009](#ref-miles-2009)) avec un identifiant et une étiquette par langue.

```yaml
# concepts.yaml
practice-standards:
  prefLabel:
    "en-CA": Practice standards
    "fr-CA": Normes de pratique
  broader: clinical-governance
```

Les fichiers référencent l'identifiant du concept ; les étiquettes sont résolues par langue. SKOS donne aussi `broader`, `narrower` et `related` gratuitement, de sorte que le vocabulaire de sujets devient navigable plutôt qu'un nuage d'étiquettes plat. Si un thésaurus externe couvre le domaine, pointez `skos:exactMatch` vers lui et héritez de ses étiquettes multilingues plutôt que de maintenir les vôtres.

Le motif vaut la peine d'être nommé, parce qu'il revient : **tout ce qui a une chaîne différente par langue est un concept avec des étiquettes, pas une propriété avec une valeur.** Les titres d'œuvres, les sujets, les noms de collections et les noms de rôles en sont tous des instances.

### Les rôles ont besoin d'un vocabulaire

Ni dcterms ni OpenWEMI ne peuvent dire qui a traduit quelque chose. `dcterms:contributor` dit qu'une personne a été impliquée et rien de plus. **MARC Relators** (`https://id.loc.gov/vocabulary/relators/`) fournit la précision manquante, `trl` pour traducteur, `aut` pour auteur, `edt` pour éditeur, comme des concepts SKOS avec des étiquettes déjà en plusieurs langues. Pour une archive de traduction, distinguer l'auteur du traducteur n'est pas un détail optionnel ; c'est la différence entre deux expressions d'une œuvre et deux œuvres.

### Identité linguistique

Utilisez des étiquettes BCP-47 complètes sur chaque littéral étiqueté par langue et sur `dcterms:language` <a id="cite-phillips-2009"></a>([Phillips & Davis, 2009](#ref-phillips-2009)). `fr-CA` et `fr-FR` sont des expressions différentes d'une œuvre en ce qui concerne le modèle. Laisser tomber la région parce qu'il n'y a actuellement qu'un seul français ferme l'autre à bon compte maintenant et à grand prix plus tard.

**Les langues non documentées et non normalisées sont une exigence, pas une exception.** L'archive doit accommoder les langues des signes régionales, les langues sans code ISO, les langues construites, et des systèmes d'expression qui ne sont sans doute pas des langues du tout. L'instinct est d'inventer une étiquette et de la marquer invalide. Ne le faites pas, et plus utilement, vous n'avez pas à le faire.

Inventer une étiquette hors de BCP-47 a un coût précis et irrécupérable : cela brise les littéraux étiquetés par langue. En RDF, `rdf:langString` et `@language` de JSON-LD exigent une étiquette BCP-47 bien formée ; les processeurs ont le droit de rejeter ou de laisser tomber silencieusement un littéral qui en porte une mal formée. Perdez cela et les étiquettes multilingues, le mécanisme dont dépendent à la fois les concepts SKOS et les termes de relateur, cessent de fonctionner. L'étiquette n'est pas une décoration ; elle est porteuse de charge.

Quatre mécanismes couvrent les cas, par ordre de préférence :

**Vérifiez d'abord ISO 639-3.** Il couvre environ 7 900 langues, y compris la plupart des langues des signes documentées. La langue des signes québécoise est `fcs` ; la langue des signes américaine est `ase`. Beaucoup de langues supposées non codées ne le sont pas. Notez que les étiquettes de style `sgn-CA` sont dépréciées en faveur du code direct.

**Utilisez la plage à usage privé `qaa`–`qtz`.** Le RFC 5646 réserve ces sous-étiquettes à l'usage privé, correspondant à des codes réservés par ISO 639-2, et énonce qu'elles peuvent être utilisées comme sous-étiquettes de langue primaires non enregistrées à la place des sous-étiquettes à usage privé `x-`. C'est le mécanisme conçu exactement pour ce problème : 520 emplacements pour des langues que l'archive reconnaît et que les normes ne reconnaissent pas, avec chaque étiquette restant BCP-47 bien formée.

**Ajoutez des sous-étiquettes `x-` pour les variétés.** Une variété régionale ou communautaire d'une langue codée reste ancrée à elle : `fcs-x-saguenay` reste analysable comme langue des signes québécoise par tout ce qui ne connaît pas la partie privée.

**Utilisez les codes spéciaux là où ils sont véridiques.** `mis` pour les langues non codées, `und` pour indéterminé, `art` pour les langues construites, et `zxx` pour un contenu sans contenu linguistique du tout.

Ce dernier mérite un moment. Pour des systèmes d'expression végétaux ou animaux, `zxx` plus une propriété de modalité explicite est plus honnête qu'une étiquette de langue fabriquée, et cela n'induira pas un consommateur à appliquer des suppositions de traitement linguistique qui ne tiennent pas. L'archive peut quand même traiter ceux-ci comme des expressions d'une œuvre, puisque l'Expression concerne la réalisation et pas spécifiquement la langue, mais l'axe qui les distingue pourrait être le médium plutôt que la langue.

**Ce qu'il ne faut pas faire :** encoder un axe non linguistique comme une étiquette de langue. `en-CA-x-easy` est BCP-47 bien formée et elle ment. Le registre n'est pas la langue, et un consommateur qui sélectionne du contenu par langue obtiendra la mauvaise réponse sans aucun moyen de le détecter. Si une distinction n'est pas linguistique, elle a besoin de son propre axe, pas d'une sous-étiquette à usage privé empruntée à quelqu'un d'autre. La règle survit inchangée au passage aux coordonnées de front matter, et elle est maintenant vérifiable : l'expression en lecture facile porte `dcterms:language: en-CA` et `register: easy`, et aucun des deux champs ne contient l'information de l'autre.

## Les axes

Un axe est une dimension selon laquelle les expressions d'une œuvre varient. La langue est le premier ; le registre, la modalité et le public sont les suivants habituels.

Chaque axe est un **`skos:ConceptScheme`** et chacune de ses valeurs est un **`skos:Concept`**, ce qui signifie qu'un fichier d'axe a la même forme que `concepts.yaml` et utilise le même résolveur. Chaque valeur a besoin d'un identifiant et d'étiquettes dans chaque langue, parce que « lecture facile » doit s'afficher comme *lecture facile* dans l'interface française. La langue est simplement un schéma dont les concepts portent des étiquettes BCP-47 comme attribut.

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

Quatre choses découlent du fichier d'axe et valent la peine d'être rendues explicites.

**Les clés sont locales ; les étiquettes (tags) sont ce vers quoi la clé se résout.** L'archive peut nommer une variété qu'elle reconnaît, émettre une étiquette bien formée pour les machines, et enregistrer ouvertement que l'étiquette est à usage privé, trois faits à la fois, sans aucune syntaxe inventée nulle part. Une langue recevant plus tard un code ISO est un changement d'une ligne plutôt qu'un renommage à travers l'archive.

**L'ensemble d'axes est fermé.** Un axe non déclaré apparaissant dans une coordonnée est une erreur, pas un nouvel axe. Sans cette règle, une faute de frappe crée silencieusement une dimension, et la forme de l'archive devient ce que quiconque a fini par taper.

**Un axe est l'axe racine, et c'est la langue.** L'archive déclare lequel dans `archive.yaml`. Les valeurs de l'axe racine sont des noms de répertoires au sommet de l'archive et ne sont jamais écrites dans le front matter ; tout autre axe est écrit dans le front matter et n'apparaît jamais dans un chemin.

**Une valeur non par défaut porte un jeton de slug par langue.** `label` est ce qu'un lecteur voit dans une interface ; `slug` est ce qu'un lecteur voit dans un nom de fichier et une URL. Les deux sont par langue pour la même raison, et la valeur par défaut ne déclare ni l'un ni l'autre, parce qu'une page non marquée garde le slug de base.

### Déclarer une coordonnée

```yaml
---
work: urn:uuid:8f7d1a92-3c04-4b1e-9f2a-6d5e8c0b7a41
coordinates:
  register: easy
---
```

Un bloc, un objet. Les clés sont des noms d'axes, les valeurs sont des clés de valeur d'axe, et les deux sont vérifiées contre les axes déclarés. Un axe omis ici prend son défaut déclaré. L'axe racine ne doit pas apparaître, parce qu'il est déjà déterminé par l'emplacement du fichier, et deux sources de vérité pour une coordonnée, c'est une de trop.

### Slugs de variante

Une variante devrait dire ce qu'elle est, dans la langue de l'arbre où elle se trouve. Le jeton déclaré sur la valeur d'axe fournit cela :

```
en-ca/areas.md                    areas,     registre standard
en-ca/areas-easy-read.md          areas,     registre easy
fr-ca/domaines.md                 domaines,  registre standard
fr-ca/domaines-lecture-facile.md  domaines,  registre easy
```

Quatre propriétés en découlent.

**Le slug de base survit.** Retirez les jetons et vous avez la page, donc les variantes d'une page partagent un slug de base exprès. L'unicité à l'intérieur d'un arbre est donc le slug de base plus les coordonnées, pas le slug de base seul.

**La coordonnée reste la source de vérité.** Le jeton est une convention de nommage sur un fait déclaré dans le front matter, pas un second endroit où le déclarer. Rien ne se résout en analysant un nom de fichier.

**Les deux peuvent être vérifiés l'un contre l'autre.** Des coordonnées qui exigent un jeton que le nom de fichier ne porte pas, et un nom de fichier portant un jeton qu'aucune coordonnée ne déclare, sont toutes deux des erreurs. La seconde est l'erreur de rédaction probable : un fichier nommé `notes-easy-read.md` sans bloc `coordinates:` est une page qui ressemble à une variante et n'en est pas une, et sans la vérification elle se publie en registre standard sous un nom trompeur.

**Un slug fixe et une recherche d'UUID renvoient le même ensemble.** La résolution à travers les variantes passe par l'identité de l'œuvre plus les coordonnées dans tous les cas. Le jeton est pour les lecteurs ; il achète de la lisibilité dans les URL et les listages de fichiers, et l'archive fonctionnerait quand même si chaque nom de fichier était un hachage.

Une archive qui ne veut pas de la convention règle `variant_slug_policy: free`, et les noms de fichiers ne sont pas vérifiés.

### La racine de l'arbre n'est pas un cas particulier

`en-ca/index.md` est la page d'accueil de l'arbre anglais. Son chemin de slug est vide, elle est adressée à la racine de la langue, et `fr-ca/index.md` est la même page en français, partageant son œuvre. Il n'y a rien ici à décider ; c'est comme le web fonctionne déjà. La seule chose qui vaille la peine d'être énoncée est que l'effondrement de l'index s'applique au répertoire qui contient le fichier, donc `lsq/domaines/index.md` prend `domaines` et `lsq/domaines-lecture-facile/index.md` prend le même slug de base à une coordonnée différente.

### Les guillemets ne sont pas optionnels

Les clés de langue et les slugs doivent être mis entre guillemets en YAML. `no` est le code ISO 639-1 du norvégien *et* un booléen YAML 1.1, donc `no: Områder` s'analyse comme une clé booléenne et l'étiquette norvégienne disparaît silencieusement. Il n'y a aucune erreur et le fichier a l'air correct. `y`, `on` et `off` se comportent de la même façon, et un slug numérique nu s'analyse en entier et ne correspondra pas à la chaîne dans un chemin.

Trois défenses indépendantes, toutes bon marché : mettre chaque clé entre guillemets, utiliser un analyseur YAML 1.2, qui a abandonné l'ensemble de booléens `yes`/`no`, et faire en sorte que le profil vérifie que les clés et les slugs sont des chaînes. Deux des trois sont mécaniques et appartiennent à la chaîne d'outils plutôt qu'à un guide de style, donc la configuration de l'analyseur et la vérification du profil sont toutes deux des exigences de la construction, pas des conseils aux auteurs.

## Quand la Manifestation devient réelle

La v0.0.2 laissait cela ouvert au motif qu'une édition braille ou en gros caractères forcerait le niveau à devenir réel. C'est la mauvaise ligne de partage. La question n'est pas quelles incarnations existent, c'est lesquelles sont **rédigées**.

**Une incarnation générée est une sortie de construction, pas du contenu d'archive.** HTML, PDF et EPUB produits à partir de la source par une construction sont recalculables à partir de l'archive plus la construction, ils ne portent aucune décision que quiconque a prise, et les enregistrer reviendrait à enregistrer la propre sortie de la construction dans sa propre entrée. Ils ne reçoivent aucun enregistrement. Une manifestation implicite par fichier source suffit, parce que le fichier source est la seule incarnation que l'archive détient.

**Une incarnation rédigée est une manifestation réelle.** Une transcription braille corrigée à la main, un PDF d'impression avec une composition que personne ne régénère, un enregistrement d'une lecture : chacun contient un travail qui n'existe nulle part ailleurs, et le perdre, c'est perdre du contenu. Il est déclaré à côté de son expression :

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

Le déclarer est l'affirmation qu'il a été rédigé. L'analyse émet un nœud de manifestation pour lui aux côtés de celui du fichier source, vérifie que le chemin existe, et ne change rien à l'expression : le braille, ce sont les mêmes mots, donc cela ajoute une incarnation et non une coordonnée.

La règle est vérifiable, ce qui est ce qui clôt la décision. « La Manifestation devient réelle quand les gros caractères existent » est une prédiction sur l'avenir ; « une incarnation qui est rédigée est déclarée, et une incarnation déclarée doit exister » est une vérification qui s'exécute aujourd'hui, et une archive qui ne rédige jamais une seule incarnation ne paie jamais pour le niveau.

## Provenance

`dcterms:source` enregistre qu'une traduction dérive d'une autre expression. Cela n'enregistre pas qui l'a fait, quand, ni à partir de quelle version intermédiaire.

Si cela compte, **PROV-O** <a id="cite-lebo-2013"></a>([Lebo et al., 2013](#ref-lebo-2013)) est la couche normalisée, et elle se compose avec tout ce qui précède :

```turtle
<expression/areas/fr-CA>
    prov:wasDerivedFrom  <expression/areas/en-CA> ;
    prov:wasGeneratedBy  [ a prov:Activity ;
        prov:wasAssociatedWith  <agent/translator> ;
        prov:endedAtTime  "2026-09-04"^^xsd:date ] .
```

Que ce soit à porter est une véritable décision, pas un oui évident. Pour une petite archive avec un seul traducteur, c'est de la cérémonie. Pour une archive où les traductions sont commandées, auditées, ou révisées contre un original mouvant, c'est l'enregistrement qui permet de répondre à « de quelle version anglaise ceci a-t-il été traduit, et est-elle toujours actuelle ? », une question qui devient urgente au moment où le texte source est édité après la traduction.

Ce dont PROV-O n'a pas besoin, c'est la dérive. La v0.0.2 proposait d'enregistrer un identifiant de source versionné dans `translationOf` pour la détecter. C'est retiré : git verse déjà tout, donc la réponse est une comparaison de somme de contrôle plutôt qu'un champ.

### La dérive est une question de somme de contrôle

Quand une expression source est révisée après que ses traductions en ont été faites, la divergence est déjà enregistrée, dans l'historique, et rien n'a besoin d'être rédigé pour la trouver :

```
commit  = le dernier commit de la traduction
then    = le blob source tel qu'il se tenait à ce commit
now     = le blob source tel qu'il se tient maintenant
drift   = then ≠ now
```

Trois propriétés font que c'est la bonne forme. C'est **dérivé**, donc il n'y a aucun champ à garder synchronisé et aucun champ à oublier. Cela suit le **fil de dérivation** plutôt que l'œuvre, donc éditer le standard anglais marque ses propres dérivés comme périmés et laisse tranquille un français en lecture facile si celui-ci venait de l'anglais en lecture facile. Et c'est **gratuit**, parce que la passe d'enrichissement a déjà le dépôt ouvert.

Deux modes de défaillance valent la peine d'être connus plutôt que dissimulés. Une édition ultérieure sans rapport à la traduction avance la ligne de base et efface faussement la dérive, puisque la comparaison est ancrée au dernier commit de la traduction et non au dernier commit qui a touché son contenu. Et les clones superficiels ou les fusions écrasées perdent la comparaison entièrement, ce que produisent par défaut la plupart des configurations d'intégration continue.

Pour une archive dont l'historique n'est pas fiable, le filet de sécurité est un condensé enregistré du blob source dans le front matter, qui n'a besoin d'aucun dépôt du tout et est le seul cas où un identifiant de version vaut la peine d'être rédigé. C'est un filet de sécurité, pas le défaut : un condensé rédigé est une chose de plus qui peut devenir périmée.

## Consommation : schema.org

schema.org n'est pas un concurrent de ce qui précède. C'est ce que lisent les moteurs de recherche et l'outillage web général, et cela appartient uniquement à la sortie émise, jamais aux fichiers rédigés, parce que c'est une projection de l'archive plutôt qu'une source de vérité.

Les termes pertinents sont `translationOfWork`, `workTranslation`, et `inLanguage`. La correspondance est surtout mécanique. Notez que schema.org, comme BIBFRAME, n'a pas de niveau Expression : `CreativeWork` couvre l'œuvre et l'expression ensemble, donc la vue schema.org émise est à perte par construction. C'est très bien. C'est une vue.

Le multi-typage signifie que l'archive n'a jamais à choisir :

```json
"@type": ["openwemi:Expression", "arc:LanguageExpression", "schema:CreativeWork"]
```

## Disposition de l'archive

```
archive.yaml

authorities/
  agents.yaml
  concepts.yaml

axes/
  language.yaml
  register.yaml

en-ca/
  index.md                          la racine de l'arbre, chemin de slug vide
  areas.md
  areas-easy-read.md                même slug de base, registre easy
  areas.brf                         une incarnation rédigée, déclarée par areas.md
  notes.md
  about/
    _defaults.yaml
    legal/
      privacy-policy.md

fr-ca/
  index.md
  domaines.md
  domaines-lecture-facile.md        la même coordonnée, nommée en français
  a-propos/
    juridique/
      politique-de-confidentialite.md

lsq/
  domaines/
    index.md
```

Cinq règles :

1. **Le premier segment de chemin est une langue**, une valeur déclarée de l'axe racine, et rien d'autre. Toute autre coordonnée est déclarée dans le front matter.
2. **Chaque arbre est indépendant.** Les chemins, les slugs et la profondeur n'ont pas à correspondre entre les arbres. L'arbre français organise le contenu français comme les lecteurs français s'y attendent.
3. **La seule chose qui traverse entre les arbres est un identifiant**, un UUID d'œuvre, une clé de concept, une clé d'agent. Jamais un chemin, jamais un slug, jamais une position.
4. **Les autorités et les axes se tiennent au-dessus des arbres**, parce que les œuvres, les concepts, les agents et les valeurs d'axe ne sont dans aucune langue. Ils ont des étiquettes dans des langues ; c'est une chose différente.
5. **La politique d'archive se tient aussi au-dessus des arbres.** L'ordre des axes, l'axe racine, la politique de défaut et l'ordre de repli sont des propriétés de l'archive et sont déclarés une fois, dans `archive.yaml`.

### Politique d'archive

```yaml
base: "https://example.org/"

axes:                           # l'ensemble fermé, en ordre canonique
  - language
  - register

root_axis: language             # l'axe unique réalisé sur le système de fichiers

key_separator: "__"             # joint les valeurs dans les clés dérivées, jamais dans un chemin

default_coordinates: fill       # fill | unspecified

fallback:                       # quel axe cède en premier
  - register
  - language

variant_slug_policy: token      # token | free
variant_slug_separator: "-"
```

`key_separator` mérite une note, parce qu'il ressemble à la chose qui vient d'être supprimée. Ce n'est pas une convention de chemin. Il joint les valeurs de coordonnées dans des clés dérivées, les cellules de la matrice de couverture, les clés de la table des UUID, et le dernier segment d'un IRI d'expression, dont aucune n'est un chemin de système de fichiers et qui ont toutes besoin d'un nom canonique et repérable par recherche pour une cellule de l'espace des coordonnées.

### Pourquoi les autorités se tiennent au-dessus

Un seul test en décide :

> **Cette chose a-t-elle des étiquettes en plus d'une langue ?**
> Si oui, c'est une autorité, et une autorité ne peut pas vivre à l'intérieur d'un arbre de langue sans devenir cantonnée à cette langue, ce qui détruit la chose même qu'elle existe pour faire.

Un **concept** a un `prefLabel` en plusieurs langues ; mettre `concepts.yaml` à l'intérieur de `en-ca/` ferait de « normes de pratique » un sujet anglais que le contenu français se trouve à référencer, ce qui est l'échec de liste de chaînes que SKOS a été adopté pour corriger. Un **agent** a un nom qui peut être translittéré différemment selon la langue. Une **valeur d'axe** a des étiquettes dans chaque langue par définition. Tous réussissent le test ; aucun n'appartient à l'intérieur d'un arbre.

Le principe sous-jacent : **les clés de jointure doivent vivre au-dessus des choses qu'elles joignent.** Une clé à l'intérieur d'un de ses propres opérandes est un bogue, que l'opérande soit un arbre de langue ou une table de base de données.

### Il n'y a pas de registre d'œuvres

Il y en avait un autrefois. Il tenait un slug, un UUID, et une carte d'étiquettes, et chacun d'eux s'est révélé dérivable ou optionnel :

- Le **slug** n'est pas du tout une propriété de l'œuvre. Chaque expression en a un, `areas`, `domaines`, et ils sont également le nom de l'œuvre ; en choisir un privilégie une langue. Analyser l'archive les rassemble tous en un index d'alias multilingue gratuitement.
- L'**étiquette** est optionnelle. Quand le titre d'une œuvre ne diverge jamais des titres de ses expressions, une étiquette au niveau de l'œuvre les duplique et ajoute un second endroit où dériver. La résolution se rabat sur le titre de l'expression dans la langue demandée.
- La **hiérarchie** n'appartient pas à l'œuvre. L'endroit où un texte se trouve dans l'organisation anglaise est un fait anglais, et l'appariement qu'une hiérarchie au niveau de l'œuvre était censée fournir se produit déjà à travers l'identité de l'œuvre.

Ce qui reste, c'est l'UUID, et il est écrit dans le front matter de chaque expression. Un registre d'UUID nus n'ajoute rien que l'analyse de l'archive ne produise déjà.

**Le coût, énoncé clairement :** sans registre, il n'y a pas d'ensemble fermé d'œuvres, donc un UUID mal saisi ne produit pas d'erreur, il mine une œuvre fantôme avec exactement une expression, ce qui est indiscernable d'une page légitimement non traduite. L'atténuation est un rapport, au moment de l'analyse, des œuvres à expression unique pour révision, pas une garantie structurelle.

### Les expressions

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

Deux choses à lire sur cette paire. La même coordonnée s'épelle avec le jeton propre à chaque langue, et le français en lecture facile déclare qu'il vient de l'anglais en lecture facile plutôt que de l'anglais standard, ce qui est ce qui permet à la dérive de suivre le fil de dérivation qui existe réellement.

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

**Un seul champ requis.** `work:` est la seule chose qui doit être présente, et c'est la seule chose qui ne peut pas être dérivée. Tout le reste est soit descriptif soit optionnel.

Les clés de premier niveau sont des **entrées de rédaction**, nommées pour ce qu'elles sont ; le bloc `dcterms:` porte des **valeurs littérales** transmises inchangées ; le bloc `coordinates:` porte des **coordonnées d'axe**. Mélanger les trois en un seul bloc, c'est perdre de vue laquelle est laquelle.

**`translationOf` est une référence de coordonnée, jamais un chemin.** Une chaîne nue nomme l'axe racine, ce qui couvre le cas ordinaire de « traduit de l'anglais ». Une correspondance nomme n'importe quels axes, ce qui est la façon dont une expression française en lecture facile enregistre qu'elle vient de l'anglais en lecture facile plutôt que de l'anglais standard.

```yaml
translationOf: "en-ca"                          # l'anglais, au registre par défaut
translationOf: {language: en-ca, register: easy} # l'anglais en lecture facile
```

L'une ou l'autre forme est complétée avec les défauts déclarés et résolue en trouvant l'expression de la même œuvre à ces coordonnées, donc elle ne touche jamais les chemins et n'est pas affectée par le fait que les arbres ont des formes différentes. Omettez-la sur les originaux.

**L'UUID doit être miné, jamais dérivé.** Ni d'un slug, ni d'un chemin, ni d'un contenu. Un UUIDv5 sur le slug est reproductible et ne demande aucune réflexion, et il mine silencieusement une œuvre différente au moment où quoi que ce soit est renommé, ce qui est précisément l'événement que l'identifiant existe pour survivre. Générer un v4 une fois, le coller, le traiter comme immuable. Un script d'une ligne retire la friction.

**Écrire la forme `urn:uuid:`.** La v0.0.1 écrivait un UUID nu. Les identifiants SAT sont des valeurs `urn:uuid:`, et la parité ne coûte rien. Un lecteur devrait accepter les deux et normaliser.

## L'analyse (le scan)

Tout changement déclenche une réanalyse et une reconstruction complètes. Les mises à jour incrémentales d'un graphe de relations sont un cache, et invalider ce cache correctement à travers des relations dérivées est l'endroit où la correction va mourir.

Six passes, dans l'ordre :

1. **Lire**, analyser les fichiers d'axes et d'autorités, parcourir les arbres, rassembler le front matter, et prendre les coordonnées de chaque expression depuis son segment racine et son bloc `coordinates:`. Pas encore de résolution.
2. **Valider**, types de chaînes, ensembles de coordonnées contre les axes déclarés, références de concept et d'agent pendantes, champs requis, collisions d'identité. Échouer ici, avant que quoi que ce soit ne soit construit sur une mauvaise entrée.
3. **Résoudre**, les clés de coordonnées en valeurs et étiquettes d'axe ; miner les identifiants d'expression à partir de l'UUID de l'œuvre plus les coordonnées.
4. **Inverser**, construire la table des UUID en regroupant chaque expression par sa valeur `work:`.
5. **Mettre en cascade**, parcourir chaque arbre vers le bas, en appliquant les défauts de section là où rien ne les remplace.
6. **Enrichir**, git pour `modified`, pour l'historique de renommage, et pour la dérive.

L'ordre n'est pas arbitraire. L'inversion après la résolution, sinon elle inverse des clés non résolues. La cascade après l'inversion, sinon elle ne peut pas voir la structure. L'enrichissement en dernier, parce qu'il a besoin de chaque expression identifiée et de chaque `translationOf` résolu avant de pouvoir comparer une source à ses dérivés. À l'intérieur de la passe de lecture, le front matter doit être analysé avant que les coordonnées ne soient assemblées, puisque la moitié de chaque ensemble de coordonnées vit maintenant là, et les coordonnées doivent être assemblées avant les slugs, puisque les coordonnées disent quels jetons le nom de fichier devrait porter.

### La table des UUID

Un seul regroupement produit chaque relation que l'archive possède :

```
uuid → {
  expressions: { "en-ca__standard": path, "en-ca__easy": path, "fr-ca__standard": path },
  slugs:       { "en-ca__standard": ["areas"], "en-ca__easy": ["areas-easy"] },
  labels:      { "en-ca__standard": {tag, title}, "en-ca__easy": {tag, title} },
  coordinates: { "en-ca__standard": {language: {key, asserted}, register: {key, asserted}} },
  modified:    { "en-ca__standard": date, … }
}
```

Les listes de pages sœurs, la résolution d'alias, et la couverture en découlent tous. Trois propriétés comptent :

**Elle est indexée par ensemble de coordonnées, pas par langue.** La v0.0.1 esquissait `labels: {"en-CA": title}`. C'est une supposition à un axe et elle échoue dès qu'un second axe existe : les expressions standard et lecture facile portent toutes deux `en-CA`, et celle que l'analyse voit en dernier l'emporte silencieusement. Tout ce qui, dans cette table, est indexé par langue a le même défaut.

**C'est un artefact de construction.** Supprimable, régénérable, jamais édité à la main, jamais versionné comme vérité. L'archive est la source ; ceci est une vue.

**Rien ne pointe vers le bas.** Les expressions référencent une œuvre ; la table est l'inversion. C'est pourquoi aucun registre n'est nécessaire, le graphe est entièrement décrit par ses feuilles, et ajouter une expression n'exige d'éditer rien d'autre.

### Git tient l'historique

Les renommages, les horodatages et les états antérieurs sont déjà enregistrés. Matérialisez ce qui est nécessaire au moment de l'analyse, une table de redirection slug-vers-UUID par exemple, plutôt que de le dupliquer dans du YAML où il peut être en désaccord avec le dépôt.

Deux mises en garde valent la peine d'être connues. La détection de renommage de git est heuristique : un renommage plus une édition substantielle en un seul commit se lit comme une suppression-plus-ajout. Et les clones superficiels et les fusions écrasées perdent l'historique entièrement, ce que font par défaut la plupart des configurations d'intégration continue. Ni l'une ni l'autre n'est porteuse de charge, parce que l'identité vit dans l'UUID, donc un renommage que git n'a pas réussi à suivre coûte une ancienne URL, pas une œuvre.

## Couverture

Deux langues permettent de s'en tirer avec des suppositions qui se brisent à trois, et un axe permet de s'en tirer avec des suppositions qui se brisent à deux.

**La couverture est partielle, et c'est normal.** Toute œuvre n'existe pas à chaque coordonnée. Inverser `work:` à travers l'archive gère cela sans cas particuliers : une œuvre obtient les expressions qui existent. Rien ne déclare une absence, et aucun fichier n'a besoin d'un espace réservé.

**La couverture est une matrice, pas une liste.** Avec un axe, « les autres versions » est une liste. Avec deux, c'est une grille surtout vide ; trois langues et deux registres font six cellules, dont peut-être deux sont remplies. Ce n'est pas un problème pour le modèle, qui n'a jamais supposé autrement, mais c'est un problème pour toute interface qui présente les variantes comme une liste plate.

**La sélection a besoin d'un ordre de repli, et l'archive le déclare.** Un consommateur qui demande le français en lecture facile alors que seul le français standard existe doit savoir s'il faut se replier le long de l'axe du registre ou de l'axe de la langue. Cet ordre est une propriété de l'archive, donc il est écrit dans `archive.yaml` comme une liste ordonnée d'axes, celui qui cède en premier d'abord, et l'analyse résout contre lui. Les axes se détendent du moins nombreux au plus nombreux, et un axe détendu essaie son défaut déclaré avant ses autres valeurs. Inverser la liste inverse quelle page sœur un lecteur obtient, ce qui est exactement pourquoi cela ne peut pas être laissé à chaque consommateur pour deviner.

**Les défauts sont remplis, et ce qui a été affirmé est enregistré.** La v0.0.1 présentait cela comme un choix : compléter chaque ensemble de coordonnées à partir des défauts déclarés, ce qui rend l'identité comparable mais affirme quelque chose que l'auteur n'a pas écrit, ou laisser les axes non nommés non spécifiés, ce qui est plus honnête mais rend chaque requête à trois valeurs. Ce n'est pas un choix. L'identité utilise l'ensemble complété, et chaque coordonnée porte si elle a été affirmée ou remplie.

```json
"en-ca__standard": {
  "language": {"key": "en-ca", "asserted": true},
  "register": {"key": "standard", "asserted": false}
}
```

La comparabilité vient de l'ensemble complété ; l'honnêteté vient du drapeau. Rien n'est perdu dans un cas comme dans l'autre, et une requête qui se soucie vraiment de la différence, un audit de quelles pages ont eu leur registre considéré, par exemple, peut quand même le demander.

**Ne pas coder en dur la liste de coordonnées.** Dérivez-la des fichiers d'axes et du contenu présent, de sorte qu'ajouter une variante ajoute un fichier et une valeur d'axe, et rien d'autre.

## Rédigé contre dérivé

Tout ce qui est récupérable depuis la position, un fichier d'autorité, ou le contrôle de version ne devrait jamais être tapé à la main. Les données dérivables tapées à la main finissent par se contredire elles-mêmes.

| Propriété | Source |
| --- | --- |
| `work` (UUID) | **Rédigé. Le seul champ requis, et le seul non dérivable** |
| `dcterms:title`, `description`, `created` | Rédigé, par expression |
| `coordinates` (axes non racine) | Rédigé là où l'expression n'est pas au défaut |
| `subject` | Rédigé comme clés de concept ; étiquettes résolues depuis `concepts.yaml` |
| `translationOf`, `translator` | Rédigé le cas échéant |
| `manifestations` | Rédigé, et seulement pour les incarnations qui ont été rédigées |
| `openwemi:expresses` | L'UUID `work` |
| Identifiant d'expression | Dérivé : UUID de l'œuvre + coordonnées |
| Coordonnée d'axe racine | La racine d'archive dans laquelle se trouve le fichier |
| Slug de base | Le nom de fichier ou de répertoire, jetons de variante retirés |
| Jeton de slug de variante | Le `slug` de la valeur d'axe pour cette langue |
| Alias | Segments de chemin, rassemblés à travers tous les arbres |
| `dcterms:language` | Coordonnée racine résolue à travers `axes/language.yaml` |
| Registre, modalité, autres axes | Coordonnées déclarées résolues à travers leurs fichiers d'axe |
| `openwemi:expressedBy` | Inversé depuis `work`, chaque page sœur qui existe |
| `dcterms:isPartOf` | Position dans l'arbre, parent immédiat seulement |
| `dcterms:modified`, historique de renommage | Contrôle de version |
| Dérive contre une source | Dérivé : blob source alors contre blob source maintenant |
| Rôles (`marcrel:trl`) | Résolus depuis `translator` via `agents.yaml` |
| `publisher`, `rights`, `license`, `spatial` | En cascade depuis les défauts de section et la configuration d'archive |
| `format`, type de manifestation | Appartient à un rendu, pas à l'archive |

`isPartOf` est dérivé et jamais rédigé. La hiérarchie est une propriété de la position d'une expression dans son propre arbre, pas de l'œuvre, puisque l'endroit où un texte se trouve dans l'organisation anglaise est un fait anglais, et l'appariement inter-arbres qu'une hiérarchie au niveau de l'œuvre fournirait vient déjà de l'identité de l'œuvre.

Les coordonnées de front matter ajoutent une ride à cela. Une variante peut maintenant avoir un parent qui n'a pas de contrepartie à ses propres coordonnées : une page enfant en lecture facile dans une section dont la page d'index n'existe qu'au registre standard. Elle se rattache au parent qui existe réellement dans la même langue, en préférant celui le plus proche des défauts déclarés, ce qui est le même repli que le reste de l'archive utilise plutôt qu'un cas particulier.

## Validation : rendre « correct » vérifiable

Tout ce qui précède est une aspiration jusqu'à ce que quelque chose l'applique. **DCTAP** <a id="cite-dcmi-2022"></a>([DCMI, 2022](#ref-dcmi-2022)) énonce un profil comme un tableau, quelles propriétés sont requises sur quelle classe, avec quel type de valeur et quelle cardinalité, et se convertit en SHACL ou ShEx pour la validation réelle.

| shapeID | propertyID | obligatoire | répétable | valueNodeType |
| --- | --- | --- | --- | --- |
| Expression | work | vrai | faux | literal |
| Expression | dcterms:title | vrai | faux | literal |
| Expression | openwemi:expresses | vrai | faux | IRI |
| Expression | coordinates.{axis} | faux | faux | literal |
| Expression | arc:slug | vrai | vrai | literal |
| ArchiveRoot | | vrai | vrai | literal |
| AxisValue | key | vrai | faux | literal |
| AxisValue | label | vrai | vrai | literal |
| AxisValue | slug | faux | vrai | literal |
| Manifestation | arc:path | vrai | faux | literal |

C'est ce qui sépare une archive modélisée d'un document de conventions. Sans cela, « chaque expression doit référencer une œuvre » est une phrase en prose que rien ne vérifie ; avec cela, la construction échoue.

La v0.0.1 nommait quatre vérifications qui comptent plus que les autres. Il y en a neuf, et chaque ajout est un échec autrement silencieux.

- **`work` s'analyse comme une chaîne UUID.** Attrape le caractère transposé avant qu'il ne devienne une œuvre fantôme.
- **Les clés et slugs d'axe sont des chaînes.** Attrape la coercition booléenne YAML, qui est invisible à l'inspection.
- **Les ensembles de coordonnées se résolvent contre les axes déclarés.** Applique l'ensemble d'axes fermé, dans le segment racine et dans `coordinates:` également.
- **Les slugs sont uniques à l'intérieur d'un arbre, retirés inclus.** Une collision se résout à celui que l'analyse a vu en dernier.
- **Une expression par œuvre par ensemble de coordonnées.** Deux fichiers portant une œuvre à un ensemble de coordonnées s'effondrent en une seule cellule de la table, et l'une des deux pages cesse simplement d'exister. Rien dans la v0.0.1 n'attrapait cela, et le passage aux coordonnées de front matter le rend plus probable, puisque les deux fichiers se trouvent maintenant dans un seul répertoire plutôt que dans des arbres séparés.
- **L'axe racine n'apparaît pas dans le front matter.** Deux sources de vérité pour une coordonnée, et aucune règle pour savoir laquelle l'emporte.
- **Un nom d'axe n'apparaît pas au niveau supérieur du front matter.** `register: easy` écrit hors du bloc `coordinates:` est l'erreur de rédaction probable, et sans cette vérification, cela s'analyse proprement comme une propriété descriptive et l'expression prend silencieusement le registre par défaut.
- **Le nom de fichier et les coordonnées s'accordent.** Dans les deux sens : une coordonnée dont le nom de fichier ne porte pas le jeton, et un jeton dans le nom de fichier qu'aucune coordonnée ne déclare. Le second est celui qui compte, parce qu'un fichier nommé `notes-easy-read.md` sans coordonnées se publie en registre standard sous un nom qui affirme le contraire.
- **Une manifestation déclarée existe.** Déclarer une incarnation est l'affirmation que quelqu'un l'a rédigée. Un chemin qui ne mène à rien est soit une faute de frappe soit un fichier qui n'a jamais été versionné, et les deux valent la peine de faire échouer la construction.

Deux vérifications de plus rapportent plutôt que d'échouer, parce que ce qu'elles trouvent peut être correct. Une œuvre à expression unique peut être un fantôme ou peut être une page non traduite. Une traduction périmée peut avoir besoin d'être révisée ou peut être très bien.

## Décisions réglées

La v0.0.1 laissait cinq décisions ouvertes et la v0.0.2 en a réglé trois. Le reste est réglé ici, avec une qui s'est révélée ne pas être une décision du tout. Le raisonnement est consigné afin que rouvrir l'une d'elles soit un acte délibéré.

**Encodage des coordonnées dans les chemins** (v0.0.2). Retiré plutôt que résolu. Seul l'axe racine est réalisé sur le système de fichiers, donc il n'y a rien à encoder.

**Coordonnées par défaut** (v0.0.2). Remplies à partir des défauts déclarés, avec `asserted` enregistré par coordonnée. Le compromis était réel et le cadrage était erroné ; les deux propriétés sont disponibles à la fois.

**Ordre de repli à travers les axes** (v0.0.2). Déclaré dans `archive.yaml` comme une liste ordonnée, résolu par l'analyse. Les consommateurs demandent des coordonnées et on leur dit ce qui a cédé.

**La Manifestation devient-elle un niveau réel ?** Oui, pour les incarnations rédigées, et jamais pour les générées. Voir « Quand la Manifestation devient réelle ». La ligne de partage est vérifiable, et une archive qui ne rédige aucune incarnation ne paie rien pour le niveau.

**Politique de slug pour les variantes.** Une coordonnée non par défaut déclare un jeton de slug par langue dans son registre d'axe, et le nom de fichier le porte. Le slug de base survit, la coordonnée reste la source de vérité, et les deux sont vérifiés l'un contre l'autre. `variant_slug_policy: free` désactive la convention pour les archives qui n'en veulent pas.

**Le slug d'une page à la racine d'un arbre.** Pas une décision. Le chemin de slug est vide et la page est adressée à la racine de la langue, de la même façon que dans toute autre langue et de la même façon que partout ailleurs sur le web. La v0.0.2 a soulevé cela par erreur.

**`translationOf` devrait-il porter une source versionnée ?** Non. Git verse déjà tout, donc la dérive est une comparaison de somme de contrôle plutôt qu'un champ rédigé. Un condensé enregistré ne survit que comme filet de sécurité pour les archives dont l'historique n'est pas fiable.

Les décisions que la v0.0.1 avait réglées avant tout cela, qu'il n'y a pas de registre, que la hiérarchie est positionnelle et dérivée, et qu'un répertoire reçoit un fichier quand c'est une page, tiennent inchangées.

## Décisions ouvertes

**Les étiquettes au niveau de l'œuvre reviennent-elles ?** Supprimer le registre a supprimé le seul endroit où un titre au niveau de l'œuvre pouvait vivre. Si une œuvre a un jour besoin d'un nom qu'aucune de ses expressions n'utilise, il n'y a nulle part où le mettre. Probablement acceptable ; à revisiter si cela pose problème.

**Qu'est-ce qui décrit une manifestation ?** Une incarnation rédigée porte actuellement un chemin, un type de média, et une note. Une édition braille avec sa propre pagination, ou un PDF d'impression avec sa propre composition, a des propriétés qui lui sont propres que rien ne modélise encore. Il existe assez pour enregistrer que l'incarnation est rédigée et où elle se trouve ; rien n'existe pour la décrire.

**Que fait une construction avec une traduction périmée ?** La dérive est maintenant détectée et rapportée. Qu'une expression périmée soit publiée, publiée avec un avis, retenue, ou fasse échouer la construction est une politique que l'archive devrait déclarer, au même endroit et pour la même raison que l'ordre de repli est déclaré.

**Une section cantonnée à une coordonnée veut-elle un mécanisme ?** Les coordonnées ne se mettent pas en cascade, et une grande section en lecture facile ou en langage simplifié en paie le prix en répétition. Une déclaration qui nommerait les ressources plutôt que la position, une liste rédigée plutôt qu'une valeur héritée, garderait l'identité hors du système de fichiers tout en supprimant la répétition. Si cela vaut un second mécanisme, ou si l'outil de rédaction est le bon endroit pour cela, n'est pas décidé.

## Coûts acceptés

Ceux-ci figuraient comme des problèmes connus dans la v0.0.1. À la révision, ce sont des conséquences de décisions prises délibérément, ou des notes sur l'outillage, plutôt que des défauts du modèle. Ils sont consignés afin qu'un futur lecteur ne les prenne pas pour des oublis, ou n'essaie pas de les réparer sans savoir ce qu'il sacrifie.

**Les UUID dans le front matter sont hostiles à la rédaction manuelle.** Ils ne peuvent pas être tapés de mémoire, ne peuvent pas être vérifiés à l'œil, et un caractère transposé produit un fantôme à l'apparence valide. C'est le prix d'un identifiant qui survit à chaque renommage, ce qui est la propriété sur laquelle repose toute la conception. Un script de minage-et-insertion n'est pas optionnel en pratique, et avec un tel script, le coût est une frappe de touche.

**Coercition booléenne de YAML 1.1.** `no` (norvégien), `y`, `on`, et `off` deviennent des booléens ; les slugs numériques nus deviennent des entiers. C'est un défaut d'un analyseur, pas de l'archive, et il est entièrement atténué par les trois défenses de « Les guillemets ne sont pas optionnels », dont deux sont mécaniques. Cela reste sur la liste seulement parce qu'une chaîne d'outils qui se rabat silencieusement sur un analyseur 1.1 échouera silencieusement.

**Prolifération des axes.** Rien ne limite structurellement le nombre d'axes, et chacun multiplie l'espace des coordonnées ; trois axes de trois valeurs chacun font vingt-sept cellules possibles. L'ensemble d'axes fermé est le frein, et c'est une politique plutôt qu'un mécanisme, délibérément. Un mécanisme ici serait une limite sur ce que l'archive est autorisée à décrire, ce qui est la mauvaise chose à imposer dans un format.

**Une coordonnée est répétée sur chaque ressource qui la porte.** Aucune valeur héritée ne peut raccourcir une section de quarante pages en lecture facile, parce que les coordonnées ne se mettent délibérément pas en cascade. La répétition est ce qui rend sûr de déplacer n'importe lequel de ces fichiers, et la fournir est une préoccupation d'outil de rédaction plutôt que de modélisation.

**La cascade est par arbre.** Les défauts de section appliqués dans `en-ca/about/` n'atteignent pas `fr-ca/a-propos/`, donc les défauts partagés qui ne sont pas à l'échelle de l'archive sont rédigés une fois par langue. C'est le prix d'une hiérarchie positionnelle, et une hiérarchie positionnelle est ce qui permet à chaque arbre de langue d'être organisé pour ses propres lecteurs. Le coût est plus petit qu'il ne l'était dans la v0.0.1 : les défauts atteignent maintenant chaque variante à l'intérieur d'une langue, parce que les variantes ne sont plus dans leurs propres arbres.

**La détection de renommage de git est heuristique.** Un renommage combiné à des éditions substantielles se lit comme une suppression-plus-ajout, et les clones superficiels perdent l'historique entièrement. Pas porteur de charge pour l'identité, qui vit dans l'UUID, mais d'anciennes URL cesseront occasionnellement de se résoudre.

**schema.org et BIBFRAME perdent le niveau Expression.** Les deux replient l'expression dans l'œuvre. La vue émise est à perte par construction, et c'est à cela que sert une vue.

## Problèmes connus

Ce qui reste : des choses qui peuvent encore produire une archive incorrecte, où l'atténuation est partielle ou absente.

**Aucun ensemble fermé d'œuvres.** Un UUID mal saisi mine une œuvre fantôme plutôt que de soulever une erreur, et un fantôme est indiscernable d'une œuvre légitimement à expression unique. Atténué par un rapport, au moment de l'analyse, des œuvres à expression unique pour révision, pas empêché. C'est le seul véritable trou laissé par la suppression du registre, et c'est la raison pour laquelle le rapport existe.

**La détection de dérive peut s'effacer faussement.** La comparaison est ancrée au dernier commit de la traduction, donc une édition ultérieure qui n'a rien à voir avec la source, une correction de faute de frappe, un changement de métadonnées, avance la ligne de base et rapporte la traduction comme actuelle alors que son contenu est encore périmé. S'ancrer au dernier commit qui a touché le corps plutôt qu'au fichier réduirait cela, et aurait besoin d'un hachage de contenu du corps plutôt que du blob.

**La détection de dérive a besoin d'un véritable historique.** Les clones superficiels et les fusions écrasées perdent la comparaison, et la plupart des configurations d'intégration continue en produisent l'un ou l'autre par défaut. L'échec est silencieux : aucune dérive n'est rapportée parce qu'aucune ne peut être calculée. Un condensé enregistré est le filet de sécurité, au prix d'un champ qui peut lui-même devenir périmé.

**L'unicité des slugs n'est aussi bonne que l'historique.** La vérification couvre les slugs retirés récupérés depuis git, donc elle hérite de la même heuristique de renommage et échoue de façon permissive sous des clones superficiels. Une collision que git n'a pas réussi à révéler se résout à celui que l'analyse a vu en dernier, silencieusement.

**La couverture n'a aucune notion de « devrait exister ».** L'absence n'est pas déclarée, ce qui est ce qui fait que la couverture partielle ne coûte rien. L'autre face de cela est qu'une traduction que personne n'a jamais commandée et une traduction qui a été commandée et jamais livrée ont la même forme dans l'archive : rien.

## Références

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

### Ressources complémentaires

**Modèles**
- LRMoo 1.0, https://cidoc-crm.org/lrmoo
- WEMI (LINCS), https://portal.lincsproject.ca/docs/terms/wemi

**Vocabulaires**
- Espace de noms OpenWEMI, https://ns.dublincore.org/openwemi/
- DCMI Metadata Terms, https://www.dublincore.org/specifications/dublin-core/dcmi-terms/
- MARC Relators, https://id.loc.gov/vocabulary/relators/
- RDA Registry, https://www.rdaregistry.info/

**Identification linguistique**
- IANA Language Subtag Registry, https://www.iana.org/assignments/language-subtag-registry/
- Ensemble de codes ISO 639-3, https://iso639-3.sil.org/
- Glottolog, pour les languoïdes sans code ISO, https://glottolog.org/

**Pratique**
- Linked Open Data (LINCS), https://portal.lincsproject.ca/docs/terms/linked-open-data

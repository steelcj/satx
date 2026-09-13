# satx : forme et objectif

**Version.** v0.0.9, 2026-09-13. Brouillon. Remplace v0.0.8.

**Portée.** Ce à quoi `satx` sert, ce qu'il contient, et les contraintes sur les scripts qui le construisent et le lisent. `satx` est l'instance SAT de test : complète, petite, et tenue à l'écart de la production. Compagnon de *SAT Sidecars: Config and Metadata* v0.0.14, qui spécifie les formes que cette instance est construite pour respecter.

## Changements dans cette version

- **Correction de la référence au document compagnon, à nouveau.** *SAT Sidecars: Config and Metadata* est passé à la v0.0.14, qui intègre les règles que `sat-init-decisions` avait consignées séparément : les deux rôles de la racine de l'instance, l'identité portée dans la couche du rôle le plus élevé d'un nœud multi-rôle, l'acceptation d'une valeur héritée qui n'écrit rien, et le reste. Rien ici n'a changé ; seul le document vers lequel celui-ci pointe a changé.

## Deux fonctions, un seul artefact

`satx` est une instance SAT complète et petite qui remplit deux fonctions à la fois.

**Une fixture.** Quelque chose à lire. Chaque règle de la spécification des sidecars est exercée par au moins un nœud dans cette instance, de sorte qu'un lecteur puisse être vérifié contre le document plutôt que contre le souvenir qu'en a son auteur.

**Un prototype.** Un exemple concret de la forme vers laquelle le MVP de SAT est en train d'être construit. Une fois que le lecteur s'accorde avec elle, l'instance est la preuve que la forme est cohérente et réalisable, et pas seulement écrite.

**Elle reste séparée de la production.** Cette séparation est ce qui garde la première fonction honnête. Une fixture qui devient la référence cesse d'être une vérification indépendante et devient la chose contre laquelle la spécification est mesurée, ce qui est l'inverse de ce qu'il faut. `satx` n'est promue au rang de prototype qu'après que le lecteur s'est accordé avec elle, jamais avant. Le nom porte cette idée : rien qui s'appelle `satx` ne risque d'être confondu avec l'instance où vit le contenu d'un client.

## Construite à partir du document, pas du lecteur

Le générateur est écrit à partir de la spécification des sidecars, pas à partir du code source du lecteur. Deux lectures indépendantes d'un même document, et tout désaccord entre elles est instructif. Si la même compréhension avait produit les deux, elles s'accorderaient par construction et la comparaison ne prouverait rien.

En pratique : quiconque écrit le générateur ne consulte pas le lecteur en l'écrivant, et le lecteur n'est pas ajusté pour correspondre au générateur sans d'abord vérifier lequel des deux le document soutient.

## Forme

Une instance complète, parce que l'instance est l'endroit où les deux sortes de territoire se rencontrent :

```
satx/
  .satx.assets/                   rôle sat : config de l'instance, field_kinds
  bin/
    .bin.assets/.sat-boundary     commandes, par rôle
  lib/
    .lib.assets/.sat-boundary
  en/                             archive : documentation propre à SAT
    .en.assets/
    docs/
    messages/
      .messages.assets/.sat-boundary      catalogues pour les chaînes de bin
  fr/                             archive
    .fr.assets/
    docs/
    messages/
      .messages.assets/.sat-boundary
  content/                        collection de collections
    .content.assets/
    examples/                     collection : correcte de bout en bout
      en-ca/                      archive
      fr-ca/
      es-ca/
    errors/                       collection : conçue pour échouer
      en-ca/
      fr-ca/
      es-ca/
    ingress/
      .ingress.assets/.sat-boundary       en attente, pas encore décrit
```

Trois choses que cette arborescence exerce et qu'une simple archive n'exercerait pas.

**Des répertoires organisateurs à l'intérieur d'une archive et à côté d'une collection.** `messages/` se trouve à l'intérieur de `en/`, qui est elle-même une archive, et `ingress/` se trouve à côté des collections. Un lecteur s'arrête à chacun plutôt que d'y descendre, et signale tout ce qui est archivé et trouvé en dessous. Le premier cas est celui qu'on a le plus de chances de mal traiter, parce que la limite se trouve à l'intérieur d'un territoire décrit plutôt qu'à l'extérieur.

**Une collection contenant des collections.** La spécification permet cette imbrication et rien ne l'avait testée. La chaîne complète des rôles, `sat` jusqu'à `collection`, `archive`, `directory`, `content`, apparaît dans une seule arborescence, avec `collection` qui se produit deux fois à des profondeurs différentes.

**Une étiquette de langue nue à côté d'étiquettes régionalisées.** `satx/en` n'a pas de région alors que `examples/en-ca` en a une, et c'est délibéré plutôt que négligé. La documentation de SAT et ses catalogues de messages s'adressent à tout lecteur anglophone, donc un seul ensemble anglais est écrit et traduit une fois, ce qui est le chemin le plus rapide. Le site d'un utilisateur s'adresse à l'anglais canadien et le dit. Les deux étiquettes diffèrent parce que les deux publics diffèrent, et les deux sont des BCP 47 bien formées.

Cela laisse aussi de la place. `en` signifie l'anglais sans région précisée, donc ajouter `en-gb` plus tard est un ajout plutôt qu'un renommage de ce qui existe déjà.

**Matériel correct et matériel défaillant, séparés.** `examples/` est la moitié prototype et peut porter de la vraie documentation, parce que la sortie d'un lecteur à partir de cette collection devrait être ennuyeuse et vérifiable. `errors/` porte n'importe quel texte qui convient, parce que personne n'en lit le contenu.

## Les répertoires organisateurs se déclarent eux-mêmes

`[P]` Un répertoire hors de la cascade porte un marqueur dans son sidecar :

```
ingress/
  .ingress.assets/
    .sat-boundary
```

La présence du fichier est tout le signal. Son contenu est de la prose destinée à un humain et rien ne l'analyse.

**Pourquoi le marqueur existe.** Sans lui, « pas de sidecar » signifie organisateur, donc un répertoire dont le sidecar n'a jamais été créé et un répertoire délibérément hors de la cascade sont indiscernables. Un sidecar oublié se lit alors comme une limite délibérée, silencieusement, ce qui est le mode de défaillance que ce projet ne cesse de retrouver.

**Pourquoi il vit dans le sidecar plutôt que librement dans le répertoire.** Cela rend l'invariant uniforme : chaque répertoire a un sidecar, et le sidecar dit si le répertoire est un nœud ou une limite. L'absence devient une erreur dans tous les cas, jamais un sens. Toute la comptabilité de SAT reste à l'intérieur des répertoires `.assets` et rien ne traîne librement parmi le matériel.

Un sidecar qui porte le marqueur n'a pas de dossier de rôle, parce qu'un répertoire organisateur ne détient aucun rôle. Un sidecar sans dossier de rôle ni marqueur est une erreur.

**Il termine une cascade plutôt que d'en commencer une.** Ce n'est pas la limite d'une instance imbriquée, qui commence une nouvelle cascade en dessous d'elle. Un répertoire organisateur termine celle du dessus : rien en dessous ne participe à la config ni aux métadonnées, et un lecteur s'arrête plutôt que d'y entrer.

**Le contenu vaut la peine d'être écrit.** Le répertoire n'a pas de métadonnées de sidecar, donc le marqueur est le seul endroit où une explication peut vivre. « Numérisations, originaux de la prise en charge de 2019, versés en 2024-03 » est ce dont quelqu'un aura besoin cinq ans plus tard.

Un marqueur nommé d'après un rôle suggérerait que le répertoire contient quelque chose. `.sat-boundary` dit ce qu'il fait : la cascade s'arrête ici. Cela laisse aussi de la place pour une limite voulue pour une raison autre que l'organisation de matériel, sans que le nom ait à être révisé.

**L'introduire invalide chaque archive existante,** puisqu'aucun de leurs répertoires organisateurs ne porte de marqueur. Cela demande une passe de migration ou une période de grâce où l'absence de marqueur et de sidecar est signalée par un avertissement plutôt que par un échec. Rien n'est encore en production, donc c'est le moment le moins coûteux.

## Où elle vit

`satx` est un répertoire à part entière, frère de SAT et du dépôt du site web, n'appartenant à aucun des deux :

```
development/
  sat/
  satx/
  website-vishpala-eleventy/
```

Les deux la lisent et aucun ne la contient. Cela compte plus qu'il n'y paraît : une fixture qui vit à l'intérieur d'un de ses consommateurs tend à être ajustée pour convenir à ce consommateur, silencieusement, jusqu'à ce qu'elle cesse d'être une vérification indépendante. Une sœur n'a personne à satisfaire.

Cela reflète aussi ce qu'est `satx`. Une instance SAT est une chose sur un système de fichiers avec une racine d'instance, et en placer une à l'intérieur d'un dépôt qui n'est pas lui-même une instance la représenterait mal.

## Les documents vivent dans l'instance

`satx/en/docs` contient tous les documents nécessaires pour comprendre `satx` : la spécification des sidecars, les exigences d'ingestion, ce document, et tout ce dont l'instance dépend par ailleurs.

Ce sont du contenu archivé, décrit comme n'importe quoi d'autre, avec des œuvres, des expressions et des sidecars. Une traduction française de la spécification des sidecars est une expression de la même œuvre que la version anglaise, appariée par `isVersionOf`, exactement comme le serait une page traduite d'un utilisateur.

Cela referme une boucle qui valait la peine d'être refermée. L'instance qui démontre la forme porte les documents qui spécifient la forme, sous cette même forme. Si la documentation ne peut pas être tenue correctement par le système qu'elle décrit, quelque chose ne va pas chez l'un des deux, et il est moins coûteux de le découvrir ici que dans la collection d'un client.

Cela donne aussi moins de travail à la collection d'exemples. `satx/en/docs` est du matériel réel, correct, et suffisamment substantiel pour exercer des sections, des chaînes de sujets et une couverture de traduction partielle. `content/examples/` peut alors rester petite et délibérée plutôt que d'avoir aussi à porter le réalisme.

## La chaîne d'outils

`satx` fonctionne sur deux outils installés, dont aucun n'est contenu en son sein.

**python-tool** installe un CPython autonome dans l'espace utilisateur, sans privilège élevé, sans gestionnaire de paquets et sans compilateur. Il a un chemin Windows fonctionnel : `install.ps1` et un wrapper `.cmd` généré à côté de celui pour le shell.

**sat-tool** installe des artefacts SAT versionnés sous `~/.local/share/sat-tool/<version>/`, chacun avec son propre environnement virtuel, et écrit un fichier d'environnement nommant celui qui est actif. Les wrappers générés dans `~/.local/bin` chargent ce fichier au moment de l'exécution, de sorte que changer de version ne demande pas de redémarrer le shell et qu'un contexte non interactif résout la même version qu'un contexte interactif.

`satx/bin/sat init ../saty` fonctionne donc parce que `satx` est l'artefact actif, pas parce que `satx` contient l'outillage. Une nouvelle instance ne reçoit pas de copie de `bin/`, parce que l'outillage vient de l'installation.

### Ce qui est portable et ce qui ne l'est pas

`satlib` est en Python et portable. L'interpréteur est portable, parce que python-tool le fournit. L'écart se trouve dans les répartiteurs de palier, `en/bin/sat/sat` et ses semblables, qui sont en bash, de sorte qu'un wrapper Windows généré n'a rien de natif à exécuter.

Cet écart est documenté en amont avec deux résolutions candidates, et écrire les répartiteurs en Python le supprime plutôt que de le contourner. D'ici là, « multiplateforme » est vrai de la bibliothèque et du runtime, mais pas encore des commandes, et ce document ne devrait pas laisser entendre le contraire.

## Trois passages

Chaque passage ajoute une chose que le précédent ne peut pas tester.

**Une langue.** La cascade elle-même. Les champs contextuels qui descendent, les champs locaux qui ne descendent pas, les lignes cumulatives, les verrous par élément, l'amendement venu d'en haut, la dépréciation, `<notset>` en attente d'un éditeur. Pas d'appariement, pas encore d'`isVersionOf`.

**Deux langues.** L'appariement. Le même `isVersionOf` à travers deux archives, avec des chemins et des profondeurs différents, et une œuvre présente dans une seule langue afin que la couverture partielle soit exercée plutôt que supposée.

**Trois langues.** Que rien ne suppose deux. Tout ce qui fonctionne à deux langues et échoue à trois repose généralement sur une notion codée en dur de « l'autre », et il est moins coûteux de le découvrir ici que dans un sélecteur de langue.

## À quoi sert chaque nœud

Environ huit nœuds de contenu, chacun méritant sa place en testant une règle.

| Nœud | Teste |
| --- | --- |
| Une section avec des enfants | La chaîne de sujets qui s'accumule depuis les ancêtres |
| Une ressource à deux niveaux de profondeur | Une chaîne de plus d'un ancêtre |
| Une ressource sans titre propre | Qu'un champ local ne descend pas, visiblement |
| Une ressource sous un `rights` fixé par la collection | Un champ contextuel qui descend à travers les archives |
| Une ressource avec un élément de sujet verrouillé | `overridable: false` par élément |
| Une ressource avec un élément délégué à une ligne inférieure | Le placement dans la ligne d'un autre palier |
| Une ressource avec un élément déprécié | Exclusion de la vue du consommateur, conservation dans le registre |
| Une ressource avec une ligne `<notset>` | Une invite adressée à un éditeur, restée sans réponse |
| Une œuvre dans une seule langue | Couverture partielle, et le rapport à expression unique |

Ces nœuds vivent dans `examples/`. Chacun est correct, et la sortie d'un lecteur à partir d'eux est le résultat connu comme bon.

### La collection errors

`errors/` existe parce qu'une vérification que personne n'exerce est une vérification dont personne ne sait qu'elle est cassée. Chaque archive qu'elle contient porte des nœuds construits pour faire trébucher une règle :

| Nœud | Devrait être signalé comme |
| --- | --- |
| Un fichier de contenu sous un répertoire organisateur marqué | Du contenu archivé hors de la cascade |
| Un répertoire sans sidecar ni marqueur | Non comptabilisé |
| Une archive qui écrit dans la ligne `sat` | Un palier qui parle au nom d'un rôle qui le surclasse |
| Un nom de champ avec une faute de frappe | Aucun type déclaré |
| Deux nœuds de contenu partageant un `identifier` | Identité non unique |
| Deux expressions d'une œuvre dans une seule langue | Coordonnées en double |
| Un `amend` qui ne correspond à rien | Amendement obsolète |
| Une redéfinition contre un champ verrouillé en amont | Retenue mais non appliquée, marquée inerte |
| Un `.sat-boundary` contenant un motif global (glob) | Probablement un malentendu |

Un lecteur exécuté contre `errors/` devrait produire exactement cette liste. Moins, c'est qu'une vérification manque ; plus, c'est qu'une vérification est erronée.

## Les scripts

**Python, multiplateforme.** SAT est en Python pour la compatibilité multiplateforme, et l'instance de test fait partie de SAT, donc ses scripts le sont aussi. Rien ne peut supposer un shell POSIX, un séparateur de chemin, ou un système de fichiers sensible à la casse.

Concrètement :

- `pathlib` partout, jamais de concaténation de chaînes pour les chemins
- aucun appel externe à `find`, `cp`, `rm`, ou quoi que ce soit d'autre d'externe
- aucune hypothèse que `a.md` et `A.md` sont des fichiers différents
- texte écrit avec un encodage explicite, toujours UTF-8
- fins de ligne choisies délibérément plutôt qu'héritées de la plateforme

**YAML 1.2, ce qui signifie `ruamel.yaml` plutôt que PyYAML.** C'est une exigence de correction, pas une préférence. PyYAML implémente YAML 1.1, où `no` est un booléen, et `no` est aussi le code ISO 639-1 du norvégien. Une clé de langue écrite sans guillemets s'analyse en `False`, silencieusement, sans rien de visible dans le fichier. `y`, `on` et `off` se comportent de la même façon, et un slug numérique nu devient un entier et cesse de correspondre à la chaîne qu'il nomme.

Vérifié : pour la même entrée, PyYAML produit `False` pour une clé norvégienne et `ruamel.yaml` produit `"no"`.

`[D]` **`ruamel.yaml` avec l'API moderne `YAML()`.** Deux réglages dont dépend son usage correct, et aucun des deux n'est un défaut.

**`yaml.preserve_quotes = True`, sur toute instance qui réécrit un fichier.** Le mode aller-retour retire les guillemets qu'il juge inutiles, donc un `["no"]` écrit à la main revient sous la forme `[no]`. Les guillemets de l'archiviste seraient retirés par l'outil même qui lui a demandé de les mettre.

**Guillemets explicites lors de la génération.** Une chaîne fraîchement construite s'écrit sans guillemets : `{"value": ["no"]}` écrit `- no`. ruamel a raison selon sa propre logique, puisque sous YAML 1.2, `no` est une chaîne ordinaire et n'a besoin de rien. Le danger est entièrement en aval, chez un lecteur qui n'est pas en 1.2. Les valeurs que la spécification demande de mettre entre guillemets sont donc enveloppées dans `DoubleQuotedScalarString` au moment de l'écriture, plutôt que de laisser le générateur en décider.

L'asymétrie vaut la peine d'être connue parce qu'elle est invisible. Un slug qui ressemble à un nombre est mis entre guillemets automatiquement, puisque ruamel doit mettre `"2024"` entre guillemets pour survivre à son propre aller-retour. Une étiquette de langue ne l'est pas. Le cas qui demande de l'attention est donc celui pour lequel la bibliothèque ne vous avertira pas.

**Aller-retour pour ce qu'une personne édite, sûr pour ce qu'un outil génère.** `overrides/` est le seul fichier édité à la main, et les commentaires qu'il contient sont le raisonnement d'un archiviste, qu'une réécriture ne devrait pas jeter. `defaults/` et `resolved/` sont générés et n'ont pas de commentaires à conserver.

**Mise en cascade là où cela aide.** Les scripts suivent la même structure de paliers que l'instance qu'ils construisent. Un générateur pour une collection sait quels sont les défauts d'une collection et transmet ses exigences aux archives qu'il crée, qui transmettent les leurs aux répertoires, et ainsi de suite. Le minage se comporte déjà ainsi dans la spécification : `sat` mine pour `sat`, puis transmet exigences et défauts à `collection`, qui mine les collections.

Le point n'est pas que tout doive être mis en cascade, mais que là où un script produit quelque chose qu'un palier inférieur va étendre, il transmet des défauts plutôt que de laisser le palier inférieur remonter. Cela garde intacte l'intention déclarée de chaque palier quand du matériel se déplace entre instances.

## Contre quoi c'est vérifié

Le critère pour tout l'exercice : **le chemin des sidecars produit-il le même appariement de traductions que le chemin du front matter ?**

Le site existant fondé sur Sveltia apparie les traductions par `identifier` et `relation` dans le front matter, avec une collection `byWork`. `satx` les apparie par `sat:isVersionOf` dans les sidecars. Si les deux s'accordent sur quelles ressources sont des versions de quelles œuvres, avec la même auto-inclusion et la même réciprocité, l'architecture des sidecars atteint le contrat d'ingestion.

S'ils sont en désaccord, le désaccord est découvert sur vingt fichiers plutôt qu'après qu'un thème a été porté.

## Ouvert

**`satx` est-elle versionnée, ou générée à la demande ?** Le générateur est un artefact dans les deux cas. Que sa sortie soit versionnée ou non décide de deux choses : si l'intégration continue d'un consommateur clone un dépôt ou exécute un script, et si les identifiants doivent être déterministes pour que deux exécutions produisent la même instance.

Versionnée, `satx` est une référence stable qui peut être comparée quand la spécification change, et elle peut dériver du générateur qui l'a produite. Générée, elle ne peut pas dériver et il n'y a rien à comparer.

La position intermédiaire est de la versionner et de traiter une différence entre l'instance versionnée et une génération fraîche comme un échec, ce qui garde les deux propriétés au prix d'une vérification.

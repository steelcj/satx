# sat init : Décisions

**Version.** v0.0.4, 2026-09-13. Remplace v0.0.3.

**Objet.** Réponses aux questions posées avant d'écrire `sat init`, dans l'ordre où elles ont été posées. Chacune est marquée `[D]` décidée, `[P]` proposée et ouverte à correction, ou `[?]` a besoin d'une décision qui n'a pas encore été prise.

## Changements dans cette version

- **Les champs contextuels sont demandés à chaque palier**, plutôt que silencieusement hérités. La règle antérieure aurait rendu indécouvrables l'éditeur et les droits propres à un département.
- **La chaîne de sujets s'accumule depuis les nœuds ancêtres**, pas depuis les ressources index ancêtres.
- **`sat init` crée une nouvelle instance avec `en/docs` et une disposition d'archive de langue**, plutôt qu'un squelette nu.
- **Tout nœud peut porter `isVersionOf`**, pas seulement les nœuds de contenu. La règle antérieure n'avait aucune justification dans le modèle et aurait rendu inexprimable une collection appariée.
- **`date` prend par défaut un horodatage réel** plutôt que `<notset>`, quand dc 1.1 est utilisé, avec le piège de portabilité de l'heure de création consigné.

**Portée de la première version.** `sat init` produit un squelette d'instance nu et rien en dessous. Aucune collection, aucune archive, aucun preseed. La création en masse est une décision séparée à prendre une fois que ceci fonctionne, et un format de preseed est une chose nouvelle à concevoir à partir de la spécification des sidecars plutôt que quelque chose de déjà spécifié.

## Conflits de la spécification

### Combien de dossiers d'auteur la racine de l'instance porte

`[D]` **Deux : `sat` et `collection`.**

Une réponse antérieure dans la conversation disait un. C'était faux, et le document de disposition a raison : la racine tient les deux rôles, parce qu'elle a `en/`, `fr/` et `content/` comme enfants, et un nœud qui tient des archives et des collections agit comme une collection.

Donc le sidecar de la racine est :

```
satx/.satx.assets/
  sat/
    config/...
    metadata/...
  collection/
    config/...
    metadata/...
```

La spécification couvre déjà cela : un nœud multi-rôle écrit une couche par rôle qu'il tient, et ces couches se résolvent dans l'ordre des rôles. `sat` se résout avant `collection`.

Ce n'est pas un cas particulier dans le code. Les rôles d'un nœud sont lus depuis les dossiers d'auteur présents dans son sidecar, et le résolveur itère sur autant qu'il en trouve.

### Si `directory` et `content` appartiennent aux enfants de `sat`

`[D]` **Non.** Les enfants de chaque rôle :

| Rôle | Peut contenir |
| --- | --- |
| `sat` | `collection`, `archive` |
| `collection` | `collection`, `archive` |
| `archive` | `directory`, `content` |
| `directory` | `directory`, `content` |
| `content` | rien |

Un document isolé directement sous une racine d'instance n'aurait aucune archive autour de lui, donc n'aurait aucune langue, et le cantonnement de l'index des œuvres à la racine de collection la plus proche n'aurait rien contre quoi se cantonner.

`[D]` Ceux-ci vivent dans la configuration comme le champ structurel `children`, déclaré à la racine, verrouillé. `init` les lit plutôt que de porter la table.

### Si une collection peut tenir des collections et des archives à la fois

`[D]` **Les deux, à la fois.**

`satx` l'exige déjà : sa racine tient `en/` et `fr/` comme archives et `content/` comme collection, simultanément. Interdire le mélange rendrait invalide l'instance que la spécification décrit.

La table des enfants ci-dessus dit que `collection` peut contenir `collection` et `archive`, sans règle l'obligeant à choisir.

## Mécanisme

### Une commande qui inspecte, ou des commandes minces par rôle

`[D]` **Des commandes minces par rôle sur une seule opération de bibliothèque partagée.**

`bin/` est déjà organisé par rôle. L'ancien dépôt utilisait cette forme. Et une seule commande qui déduit quoi créer d'après où elle pointe doit deviner, ce qui échoue plus mal que si on le lui dit : créer une archive là où une collection était voulue est une erreur que rien ne signale.

```
bin/sat/sat init <chemin>
bin/collection/collection init <chemin>
bin/archive/archive init <chemin>
bin/directory/directory new <chemin>
bin/content/content new <chemin>
```

En dessous, un seul `create_node(path, role, ...)` dans `satlib`. Les commandes diffèrent par le rôle qu'elles transmettent et ce qu'elles demandent.

### Un passage depuis un preseed, ou une commande par palier

`[D]` **Une commande par palier, pour cette version. Preseed reporté.**

Un format de preseed est un nouvel artefact à concevoir à partir de la spécification des sidecars, et le concevoir avant que `init` fonctionne signifierait le concevoir contre une forme non éprouvée. `collection-preseed.yml.example` et `archives-parent.yml` de l'ancien dépôt valent la peine d'être lus quand cette décision arrivera, pas avant.

## Ce que l'amorçage écrit, par rôle

`[D]` **À `sat`**, une nouvelle instance. Presque silencieux, parce que les défauts de la racine sont expédiés déjà peuplés.

Écrit : `sat_version`, depuis la propre version de l'instance qui crée. Demandé : `interface_language`, `default_metadata`. Tout le reste, ce sont les défauts expédiés.

`[D]` **À `archive`**, `language` est obligatoire et verrouillé, donc toujours demandé. Il est écrit dans `metadata/dc/overrides/` au nœud d'archive avec `overridable: false`, parce qu'une archive est une portée de langue et rien en dessous ne peut prétendre le contraire.

`[D]` **À `collection`, `archive` et `directory`, les champs contextuels sont demandés, montrant ce qui serait hérité.**

```
publisher [Vishpala] :
rights [CC-BY-4.0] :
```

Entrée accepte la valeur héritée et **n'écrit rien**. Le nœud ne garde aucune couche propre, continue de recevoir ce que résout le palier au-dessus, et reçoit les changements ultérieurs qui y sont faits. Taper une valeur écrit une redéfinition à ce nœud, qui descend ensuite vers tout ce qui est en dessous.

Une grande organisation est le cas pour lequel cela existe. La collection d'un département porte son propre éditeur et ses propres droits pour chaque archive et document en dessous d'elle, et elle doit pouvoir l'affirmer au palier où cela devient vrai.

**Accepter ne doit pas copier.** Si Entrée écrivait `publisher: Vishpala` dans les redéfinitions de la collection, un changement ultérieur à la racine cesserait de l'atteindre et personne ne verrait pourquoi. « J'accepte ce qu'on me donne » et « je revendique cette valeur, qui se trouve correspondre » sont des affirmations différentes, et seule la seconde écrit une couche.

**Quels champs sont demandés vient de `field_kinds`.** Les champs contextuels sont demandables parce qu'ils descendent. Les champs locaux appartiennent au nœud, et l'identité est minée. Donc la liste des questions est dérivée plutôt que portée dans le code, et un nouveau champ contextuel est demandé sans changement à `init`.

`[D]` **À `content`**, de vraies questions. `title` et `description` s'amorcent comme `<notset>` et déclenchent la règle d'inviter-à-décider-sur-`<notset>`. La chaîne de sujets dérivée s'amorce comme une proposition qu'un éditeur confirme ou amende.

`[D]` **`date` prend par défaut un horodatage réel plutôt que `<notset>`, quand dc 1.1 est utilisé.** L'éditeur est invité à accepter ou changer, comme pour toute autre proposition.

Quel horodatage dépend de ce qui est décrit :

| Situation | Défaut | Pourquoi |
| --- | --- | --- |
| `content new`, la ressource est en train d'être créée | maintenant | L'affirmation la plus vraie disponible, et aucun appel au système de fichiers |
| Décrire du matériel qui existe déjà | `st_mtime` | Le seul fait proche de la création disponible sur toute plateforme |

**Le temps de création n'est pas portable et ne doit pas être simulé.** `st_birthtime` existe sur macOS et BSD et est absent sur Linux, où `st_ctime` est le temps de changement de l'inode plutôt que le temps de création. Utiliser `st_ctime` comme substitut donne la bonne réponse sur une plateforme et une réponse fausse mais plausible sur une autre, et il bouge chaque fois que les permissions ou la propriété changent. Utiliser `st_birthtime` là où il existe, et ne jamais le substituer là où il n'existe pas.

Les deux défauts sont des propositions que l'éditeur voit et peut changer. Le `date` de DC 1.1 est délibérément large, un point dans le cycle de vie de la ressource, donc un défaut honnête sur quel point il a pris vaut mieux qu'un défaut qui prétend création et livre autre chose.

**Cette règle est par vocabulaire.** Sous dcterms, `created` et `modified` sont des propriétés séparées prenant des sources séparées, et `default_metadata` déclare quels vocabulaires sont utilisés.

**Git tient les horodatages faisant autorité et ceci ne se réconcilie pas avec eux.** Le MVP utilisait la date du premier commit. Un fichier en train d'être créé n'a pas de commit, donc `init` ne peut pas l'utiliser, et une fois commis les deux peuvent être en désaccord sans rien pour les réconcilier. Probablement acceptable, puisque la date DC est une affirmation sur le contenu et celle de git est un fait sur le fichier, mais cela vaut la peine d'être énoncé plutôt que découvert.

`[D]` `identifier` n'est jamais amorcé comme `<notset>`. Il est miné, parce qu'un UUID n'est pas quelque chose qu'un éditeur tape.

## Minage de l'identité

`[D]` **Chaque nœud reçoit un `identifier`.** Pas seulement les nœuds de contenu.

L'objectif de poupée russe l'exige : une collection libérée d'une instance et migrée vers une autre a besoin d'une identité qui survit au déplacement, et « l'index des œuvres est cantonné à la racine de collection la plus proche » exige que cette collection soit identifiable par autre chose que son chemin. Un slug est un nom et les noms changent.

`[D]` **Tout nœud peut porter `isVersionOf`.** Il est optionnel partout et exclusif au contenu nulle part.

Une collection est un acte intellectuel plutôt qu'un simple contenant : décider ce qui va ensemble, et selon quel agencement, est en soi l'œuvre. IFLA LRM nomme cela l'**œuvre agrégatrice**, introduite sur ce raisonnement même par le Groupe de travail de l'IFLA sur les agrégats. Donc une collection d'enregistrements audio et une collection du même matériel en texte sont deux expressions d'une œuvre agrégatrice, différant selon l'axe auquel l'archive varie déjà.

**Une œuvre agrégatrice est le plan de l'agrégation, pas une relation tout-partie avec ce qui est agrégé.** Une ressource à l'intérieur d'une collection réalise sa propre œuvre et n'est pas affectée par le fait que la collection en réalise une autre. Les deux niveaux n'interagissent pas, et les expressions de l'œuvre d'une collection ne sont pas des expressions des œuvres de ses membres.

Donc le minage produit :

| Rôle | Miné à la création | Peut porter |
| --- | --- | --- |
| `sat` | `identifier` | `isVersionOf` |
| `collection` | `identifier` | `isVersionOf` |
| `archive` | `identifier` | `isVersionOf` |
| `directory` | `identifier` | `isVersionOf` |
| `content` | `identifier` | `isVersionOf` |

**Ce qui diffère selon le rôle, ce n'est pas si, mais quand.** `identifier` est miné chaque fois qu'un nœud est créé. `isVersionOf` est écrit quand quelqu'un dit que ce nœud réalise cette œuvre, ce qui à un nœud de contenu est habituellement à la création et à une collection habituellement plus tard, une fois qu'une contrepartie existe avec laquelle s'apparier.

`[D]` **L'autorité de miner se met en cascade par rôle**, comme l'énonce la spécification. `sat` mine pour `sat`, puis transmet exigences et défauts à `collection`, qui mine les collections, et ainsi de suite.

### La chaîne de sujets s'accumule depuis les nœuds ancêtres

`[D]` **Nœuds ancêtres, pas ressources index ancêtres.**

Chaque nœud a un `identifier` miné à sa création, donc chaque ancêtre contribue, qu'il ait ou non une ressource index. Une section sans page d'accueil dit quand même quelque chose sur ce qui est en dessous d'elle.

## Entrées de test pour `satx/bin/sat init ../saty`

`[D]` **Cible :** `../saty`, une sœur de `satx`.

`[D]` **Ce avec quoi une nouvelle instance est expédiée.** Pas un squelette nu. `init` crée la disposition d'archive de langue, parce qu'une instance sans où mettre sa propre documentation est moins utile qu'elle n'en a l'air et la disposition est ce qui est testé.

```
saty/
  .saty.assets/        dossiers d'auteur sat et collection
  bin/                 limite
  lib/                 limite
  venvs/               limite
  en/                  archive
    docs/
    messages/          limite
  fr/                  archive
    docs/
    messages/          limite
```

`[D]` **Valeurs délibérément différentes**, pour que le test prouve que `init` ne reproduit pas les particularités propres de `satx` :

| Champ | `satx` | `saty` |
| --- | --- | --- |
| `interface_language` | `"en"` | `"fr"` |
| `rights` | tel qu'expédié | `"CC-BY-SA-4.0"` |
| `publisher` | `"Vishpala"` | `"Test Publisher"` |

`[D]` **Ce que « fonctionne » signifie.** `saty` se lit propre : `sat read ../saty` rapporte le nombre de nœuds attendu, aucune erreur, et aucun avertissement qui ne soit délibéré.

## Ouvert

Rien. Chaque question posée avant d'écrire `sat init` a une réponse.

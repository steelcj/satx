# Dublin Core 1.1 dans l'archive SAT

**Version.** v0.0.1, 2026-09-09. Remplace, avec son compagnon, *Representing Dublin Core 1.1 as Front Matter* v0.0.2.

**Portée.** Comment les valeurs DC 1.1 sont tenues dans une archive SAT : où elles sont rédigées, comment elles se propagent en cascade, et lesquelles décrivent quel niveau WEMI. C'est le côté canonique. Ce que reçoit un consommateur est couvert par *Dublin Core 1.1 as Eleventy Ingress Front Matter*.

**Statut.** Partiel. SAT lui-même est encore en cours de spécification, et les sections ci-dessous marquées *non défini* consignent ce qui n'est pas réglé plutôt que d'en deviner le contenu.

## Pourquoi ce sont deux documents

La v0.0.2 essayait de décrire un seul ensemble de valeurs en un seul endroit et produisait une contradiction au sujet de `format`. Un fichier Markdown est `text/markdown`. La page HTML générée à partir de lui est `text/html`. Les deux affirmations sont correctes, chacune à propos de son propre artefact, et un document unique décrivant les deux devait forcément avoir tort sur l'une d'elles.

La scission suit le sens du trajet. SAT détient l'archive et sait ce qu'est la source. Eleventy reçoit une projection et produit quelque chose de nouveau, qui a ses propres propriétés. Aucun des deux documents ne reformule les faits de l'autre.

## Où une valeur est rédigée

Les métadonnées canoniques d'une ressource vivent dans le sidecar de cette ressource, dans l'espace de noms DC de la cascade de métadonnées :

```
areas.md
.areas.md.assets/content/metadata/dc/overrides/dc.yml
```

Les valeurs utilisent la forme de champ de la cascade, de sorte que l'autorité descend avec elles :

```yaml
title:
  value: ["Areas"]
  overridable: true
description:
  value: ["What we maintain an ongoing standard in."]
  overridable: true
date:
  value: ["2026-09-04"]
  overridable: true
format:
  value: ["text/markdown"]
  overridable: true
```

Une valeur déclarée à un nœud au-dessus descend vers chaque nœud en dessous, de sorte que `publisher` et `rights` sont énoncés une fois à la collection et jamais reformulés. `overridable: false` ferme un champ aux paliers inférieurs, et cela ne fait que rétrécir, jamais élargir.

## Trois niveaux dans un seul sidecar

Un nœud de contenu est une expression, et le fichier qui la porte est l'incarnation source de cette expression. Un seul sidecar contient donc des énoncés à trois niveaux WEMI, et savoir lequel est lequel est ce qui les empêche d'être générés plus tard dans le mauvais artefact.

| Niveau | Éléments | Comportement |
| --- | --- | --- |
| Œuvre | aucun en DC ; porté comme `sat:isVersionOf` | identité seulement, jamais descriptif |
| Expression | `title`, `creator`, `subject`, `description`, `language`, `date`, `contributor` | ce qu'est le texte |
| Manifestation | `format` | ce qu'est cette incarnation |

`format` est le seul élément DC qui décrit le fichier plutôt que le texte, et `text/markdown` en est ici la valeur correcte. C'est un fait sur la source, c'est vrai de la source, et cela reste avec la source. Un consommateur qui produit une incarnation différente énonce le format propre à cette incarnation et n'hérite pas de celui-ci.

Les incarnations générées ne reçoivent ni nœud ni métadonnées. Une incarnation rédigée, une édition braille ou un PDF composé, est déclarée et devient une manifestation à part entière, avec son propre `format`.

## Quels éléments sont rédigés

Sur les quinze, la plupart ne sont jamais saisis sur une ressource.

| Source | Éléments |
| --- | --- |
| Rédigés sur la ressource | `title`, `description`, `date`, `subject`, `creator`, `contributor` |
| Mis en cascade depuis le dessus | `publisher`, `rights`, `type`, `format` |
| Reçus de l'archive de langue | `language` |
| Non utilisés | `relation`, `source`, `coverage`, `identifier` |

La dernière ligne a besoin de justification.

`relation` et `source` disent que deux ressources sont liées et ne disent rien sur la manière. Chaque relation que l'archive a réellement est plus précise que cela : identité d'œuvre, traduction, partie et tout. SAT les porte comme des propriétés nommées dans son propre espace de noms plutôt que comme un `relation` indifférencié, de sorte qu'il ne reste rien à faire à l'élément DC.

`coverage` couvre le lieu et le temps en un seul élément. Là où l'un ou l'autre est voulu, il vaut mieux prendre `dcterms:spatial` et `dcterms:temporal` à la place, qui les séparent et peuvent être interrogés.

`identifier` est tenu comme `sat:identifier`, un `urn:uuid` miné une fois avec `uuidgen -r`. Un `identifier` DC portant une URL serait un second nom qui change quand le site déménage, ce qui est précisément l'événement que le premier existe pour survivre.

## Langue

`language` est déclaré une fois, au nœud de l'archive de langue, et reçu par chaque nœud en dessous à travers la cascade de métadonnées. Aucun nœud de contenu ne le reformule.

Les étiquettes suivent BCP 47 <a id="cite-rfc5646"></a>([Phillips & Davis, 2009](#ref-rfc5646)) et s'écrivent en minuscules, `en-ca` plutôt que `en-CA`. La casse ne porte aucun sens en BCP 47, donc les deux ne sont qu'une seule étiquette, mais RDF 1.1 compare les littéraux étiquetés par langue caractère par caractère, ce qui fait de `"x"@en-CA` et `"x"@en-ca` des termes distincts dans un entrepôt <a id="cite-rdf11"></a>([Cyganiak et al., 2014](#ref-rdf11)). RDF 1.2 supprime la distinction ; l'outillage 1.1 est ce qu'une archive rencontre aujourd'hui. Une seule forme en minuscules partout signifie que l'archive ne peut pas produire cette classe de bogue, et cela permet au nom du répertoire de l'archive et à l'étiquette d'être la même chaîne.

Un passage dans une autre langue à l'intérieur d'un document est un balisage en ligne, `<span lang="fr-ca">`. C'est un fait sur un segment de texte, pas sur la ressource, et cela n'appartient pas aux métadonnées de la ressource.

## Répétabilité et forme

Chaque élément DC 1.1 est optionnel et chacun est répétable <a id="cite-dcmi-2012"></a>([DCMI, 2012](#ref-dcmi-2012)). Il n'y a aucun élément requis, aucune contrainte de cardinalité, et aucune distinction entre les éléments qui peuvent se répéter et ceux qui ne le peuvent pas.

Les valeurs sont donc des listes, toujours, y compris là où une seule valeur est présente. Un lecteur peut accepter un scalaire nu et le normaliser, mais un schéma où certains éléments sont des scalaires et d'autres des listes encode une distinction que la norme ne fait pas, et chaque consommateur porte alors la même table d'exceptions.

DC 1.1 est l'espace de noms `/elements/1.1/`. DCMI Metadata Terms est le vocabulaire `/terms/` plus récent, avec des domaines et des portées déclarés. `dc:date` et `dcterms:date` sont des propriétés différentes. SAT tient DC 1.1 dans `metadata/dc/`, et un espace de noms `metadata/dcterms/` se tient à côté pour le jour où des raffinements seront voulus.

## Guillemets

Les clés de langue et les slugs sont mis entre guillemets, toujours. Sous YAML 1.1, `no` est un booléen, et `no` est le code ISO 639-1 du norvégien, donc une clé norvégienne sans guillemets s'analyse en `false` et la valeur disparaît sans erreur et sans rien de visible dans le fichier. `y`, `on` et `off` se comportent de la même façon, et un slug numérique nu s'analyse en entier et cesse de correspondre à la chaîne qu'il nomme.

Trois défenses, aucune coûteuse : mettre les clés entre guillemets, analyser en YAML 1.2, qui a abandonné cet ensemble de booléens, et faire en sorte que la validation vérifie que les clés et les slugs sont des chaînes. Deux des trois appartiennent à la chaîne d'outils plutôt qu'à un guide de style.

## Pas encore défini

**Comment les métadonnées `sat:` sont partitionnées.** `identifier`, `isVersionOf` et `slug` sont réglés. Si les coordonnées d'axe autres que la langue se trouvent dans le même fichier d'espace de noms ou dans un fichier qui leur est propre ne l'est pas.

**Si `creator` et `subject` sont des propriétés de l'œuvre.** Les deux sont sans doute des faits sur le contenu plutôt que sur une version linguistique de celui-ci, et les deux sont actuellement répétés sur chaque expression. Les faire remonter demande un endroit où les mettre, et il n'existe pas de registre d'œuvre.

**Ce qui décrit une manifestation rédigée.** Il existe assez pour dire qu'une incarnation est rédigée et où elle se trouve. Une édition braille avec sa propre pagination a des propriétés que rien ne modélise encore.

**La validation.** DCTAP sur les métadonnées résolues, converti en SHACL, est la forme prévue. Aucun profil n'est écrit.

## Références

<a id="ref-rdf11"></a>Cyganiak, R., Wood, D., & Lanthaler, M. (Eds.). (2014). *RDF 1.1 concepts and abstract syntax*. W3C. https://www.w3.org/TR/rdf11-concepts/ [↩](#cite-rdf11)

<a id="ref-dcmi-2012"></a>Dublin Core Metadata Initiative. (2012). *Dublin Core metadata element set, version 1.1*. https://www.dublincore.org/specifications/dublin-core/dces/ [↩](#cite-dcmi-2012)

<a id="ref-rfc5646"></a>Phillips, A., & Davis, M. (2009). *Tags for identifying languages* (BCP 47, RFC 5646). IETF. https://www.rfc-editor.org/rfc/rfc5646.html [↩](#cite-rfc5646)

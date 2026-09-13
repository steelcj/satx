# sat init: Decisiones

**Versión.** v0.0.4, 2026-09-13. Reemplaza a v0.0.3.

**Propósito.** Respuestas a las preguntas planteadas antes de escribir `sat init`, en el orden en que se hicieron. Cada una está marcada `[D]` decidida, `[P]` propuesta y abierta a corrección, o `[?]` necesita una decisión que aún no se ha tomado.

## Cambios en esta versión

- **Los campos contextuales se preguntan en cada nivel**, en lugar de heredarse silenciosamente. La regla anterior habría hecho indescubribles el editor y los derechos propios de un departamento.
- **La cadena de sujetos se acumula desde los nodos ancestros**, no desde recursos índice ancestrales.
- **`sat init` crea una nueva instancia con `en/docs` y una disposición de archivo de lenguaje**, en lugar de un esqueleto desnudo.
- **Cualquier nodo puede portar `isVersionOf`**, no solo los nodos de contenido. La regla anterior no tenía justificación en el modelo y habría hecho inexpresable una colección emparejada.
- **`date` toma como valor predeterminado una marca de tiempo real** en lugar de `<notset>`, cuando se usa dc 1.1, con la trampa de portabilidad de la hora de creación registrada.

**Alcance de la primera versión.** `sat init` produce un esqueleto de instancia desnudo y nada debajo de él. Sin colecciones, sin archivos, sin preseed. La creación masiva es una decisión separada que se tomará una vez que esto funcione, y un formato de preseed es algo nuevo que hay que diseñar a partir de la especificación de sidecars en lugar de algo ya especificado.

## Conflictos de la especificación

### Cuántas carpetas de autor porta la raíz de la instancia

`[D]` **Dos: `sat` y `collection`.**

Una respuesta anterior en la conversación decía una. Eso era incorrecto, y el documento de disposición tiene razón: la raíz porta ambos roles, porque tiene `en/`, `fr/` y `content/` como hijos, y un nodo que porta archivos y colecciones está actuando como una colección.

Así que el sidecar de la raíz es:

```
satx/.satx.assets/
  sat/
    config/...
    metadata/...
  collection/
    config/...
    metadata/...
```

La especificación ya cubre esto: un nodo multi-rol escribe una capa por cada rol que porta, y esas capas se resuelven en orden de rol. `sat` se resuelve antes que `collection`.

Esto no es un caso especial en el código. Los roles de un nodo se leen desde las carpetas de autor presentes en su sidecar, y el resolutor itera sobre cuantas encuentre.

### Si `directory` y `content` pertenecen a los hijos de `sat`

`[D]` **No.** Los hijos de cada rol:

| Rol | Puede contener |
| --- | --- |
| `sat` | `collection`, `archive` |
| `collection` | `collection`, `archive` |
| `archive` | `directory`, `content` |
| `directory` | `directory`, `content` |
| `content` | nada |

Un documento suelto directamente bajo una raíz de instancia no tendría ningún archivo a su alrededor, por lo que no tendría lenguaje, y el alcance del índice de obras a la raíz de colección más cercana no tendría contra qué alcanzarse.

`[D]` Estos viven en la configuración como el campo estructural `children`, declarado en la raíz, bloqueado. `init` los lee en lugar de portar la tabla.

### Si `roles` se declara en cada nodo o solo en la raíz

`[D]` **Solo en la raíz.** Se llaman roles a dos cosas diferentes, y la ambigüedad es toda la pregunta.

`roles` en la configuración es un campo de **vocabulario**: la lista de nombres de rol que existen. Declarado una vez en `sat`, nunca sustituible, exactamente como la especificación de configuración describe los campos de vocabulario.

El rol **propio** de un nodo no es un campo en absoluto. Es estructural, expresado por qué carpetas de autor porta su sidecar. Preguntar qué rol tiene un nodo significa leer su sidecar, no leer un valor.

Así que `init` no escribe ningún campo relacionado con el rol en la configuración de un nodo por debajo de la raíz. Crea la carpeta de autor, y esa es la declaración.

### Si una colección puede portar colecciones y archivos a la vez

`[D]` **Ambos, a la vez.**

`satx` ya lo requiere: la raíz porta `en/` y `fr/` como archivos y `content/` como colección, simultáneamente. Prohibir la mezcla haría inválida la instancia que describe la especificación.

La tabla de hijos anterior dice que `collection` puede contener `collection` y `archive`, sin regla que la obligue a elegir.

## Mecanismo

### Un comando que inspecciona, o comandos delgados por rol

`[D]` **Comandos delgados por rol sobre una operación de biblioteca compartida.**

`bin/` ya está organizado por rol. El repositorio antiguo usaba esta forma. Y un único comando que infiere qué crear a partir de dónde se apunta tiene que adivinar, lo cual falla peor que si se le dice: crear un archivo donde se pretendía una colección es un error que nada reporta.

```
bin/sat/sat init <ruta>
bin/collection/collection init <ruta>
bin/archive/archive init <ruta>
bin/directory/directory new <ruta>
bin/content/content new <ruta>
```

Por debajo, un único `create_node(path, role, ...)` en `satlib`. Los comandos difieren en qué rol pasan y qué preguntan.

### Un pase desde un preseed, o un comando por nivel

`[D]` **Un comando por nivel, para esta versión. Preseed aplazado.**

Un formato de preseed es un artefacto nuevo que hay que diseñar a partir de la especificación de sidecars, y diseñarlo antes de que `init` funcione significa diseñar contra una forma no probada. `collection-preseed.yml.example` y `archives-parent.yml` del repositorio antiguo valen la pena leerse cuando llegue esa decisión, no antes.

## Qué escribe el amorzado, por rol

`[D]` **En `sat`**, una nueva instancia. Casi silencioso, porque los valores predeterminados de la raíz se envían ya poblados.

Escrito: `sat_version`, desde la versión propia de la instancia que crea. Preguntado: `interface_language`, `default_metadata`. Todo lo demás son los valores predeterminados enviados.

`[D]` **En `archive`**, `language` es obligatorio y está bloqueado, así que siempre se pregunta. Se escribe en `metadata/dc/overrides/` en el nodo de archivo con `overridable: false`, porque un archivo es un ámbito de lenguaje y nada debajo de él puede afirmar lo contrario.

`[D]` **En `collection`, `archive` y `directory`, los campos contextuales se preguntan, mostrando lo que se heredaría.**

```
publisher [Vishpala]:
rights [CC-BY-4.0]:
```

Enter acepta el valor heredado y **no escribe nada**. El nodo no conserva ninguna capa propia, sigue recibiendo lo que resuelva el nivel de arriba, y recoge los cambios posteriores allí. Escribir un valor escribe una redefinición en ese nodo, que luego desciende a todo lo que está debajo.

Una organización grande es el caso para el que existe esto. La colección de un departamento porta su propio editor y sus propios derechos para cada archivo y documento debajo de ella, y tiene que poder afirmarlo en el nivel donde se vuelve verdadero.

**Aceptar no debe copiar.** Si Enter escribiera `publisher: Vishpala` en las redefiniciones de la colección, un cambio posterior en la raíz dejaría de alcanzarla y nadie vería por qué. "Acepto lo que se me da" y "reclamo este valor, que resulta coincidir" son afirmaciones diferentes, y solo la segunda escribe una capa.

**Qué campos se preguntan viene de `field_kinds`.** Los campos contextuales son preguntables porque descienden. Los campos locales pertenecen al nodo, y la identidad se mina. Así que la lista de preguntas se deriva en lugar de llevarse en el código, y un nuevo campo contextual se pregunta sin un cambio en `init`.

`[D]` **En `content`**, preguntas reales. `title` y `description` se inician como `<notset>` y activan la regla de preguntar-sobre-`<notset>`. La cadena de sujetos derivada se inicia como una propuesta que un editor confirma o enmienda.

`[D]` **`date` toma como valor predeterminado una marca de tiempo real en lugar de `<notset>`, cuando se usa dc 1.1.** Se pregunta al editor si acepta o cambia, como con cualquier otra propuesta.

Qué marca de tiempo depende de lo que se está describiendo:

| Situación | Valor predeterminado | Por qué |
| --- | --- | --- |
| `content new`, el recurso se está creando | ahora | La afirmación más verdadera disponible, y ninguna llamada al sistema de archivos |
| Describiendo material que ya existe | `st_mtime` | El único hecho cercano a la creación disponible en toda plataforma |

**El tiempo de creación no es portable y no debe emularse.** `st_birthtime` existe en macOS y BSD y está ausente en Linux, donde `st_ctime` es el tiempo de cambio del inodo en lugar del tiempo de creación. Usar `st_ctime` como sustituto da la respuesta correcta en una plataforma y una respuesta incorrecta pero plausible en otra, y se mueve cada vez que cambian los permisos o la propiedad. Usar `st_birthtime` donde existe, y nunca sustituirlo donde no existe.

Ambos valores predeterminados son propuestas que el editor ve y puede cambiar. `date` de DC 1.1 es deliberadamente amplio, un punto en el ciclo de vida del recurso, así que un valor predeterminado honesto sobre qué punto tomó es mejor que uno que afirma creación y entrega otra cosa.

**Esta regla es por vocabulario.** Bajo dcterms, `created` y `modified` son propiedades separadas que toman fuentes separadas. `default_metadata` declara qué vocabularios están en uso, así que el comportamiento de inicio sigue una declaración en lugar de una suposición.

**Git tiene las marcas de tiempo autorizadas y esto no se reconcilia con ellas.** El MVP usaba la fecha del primer commit. Un archivo que se está creando no tiene commit, así que `init` no puede usarlo, y una vez comprometido los dos pueden discrepar sin nada que los reconcilie. Probablemente aceptable, ya que la fecha DC es una afirmación sobre el contenido y la de git es un hecho sobre el archivo, pero vale la pena decirlo en lugar de descubrirlo.

`[D]` `identifier` nunca se inicia como `<notset>`. Se mina, porque un UUID no es algo que un editor teclee.

## Minado de identidad

`[D]` **Todo nodo recibe un `identifier`.** No solo los nodos de contenido.

El objetivo de muñeca rusa lo requiere: una colección liberada de una instancia y migrada a otra necesita una identidad que sobreviva al traslado, y "el índice de obras está delimitado a la raíz de colección más cercana" requiere que esa colección sea identificable por algo distinto de su ruta. Un slug es un nombre y los nombres cambian.

`[D]` **Cualquier nodo puede portar `isVersionOf`.** Es opcional en todas partes y exclusivo del contenido en ninguna.

Una colección es un acto intelectual más que solo un contenedor. Decidir qué pertenece junto, y en qué disposición, es en sí mismo la obra. IFLA LRM llama a esto la **obra agregadora**, introducida exactamente con ese razonamiento por el Grupo de Trabajo de IFLA sobre Agregados, y RDA ha desarrollado desde entonces un tratamiento para colecciones que apoya a las instituciones cuyo enfoque es la descripción y el acceso de colecciones.

Así que una colección de grabaciones de audio y una colección del mismo material como texto son dos expresiones de una obra agregadora, difiriendo en el eje según el cual ya varía el archivo. `content/examples/websites/universalcake.com/` que porta `en-ca/`, `es-mx/` y `fr-ca/` es una obra con tres expresiones, algo que el árbol ya implica y que nada registra actualmente.

**Una obra agregadora es el plan de la agregación, no una relación de todo-parte con lo que se agrega.** Un recurso dentro de una colección realiza su propia obra, y no se ve afectado porque la colección realice otra. Los dos niveles no interactúan, y un lector no debe tratar las expresiones de la obra de una colección como expresiones de las obras de sus miembros.

Así que el minado produce:

| Rol | Minado en la creación | Puede portar |
| --- | --- | --- |
| `sat` | `identifier` | `isVersionOf` |
| `collection` | `identifier` | `isVersionOf` |
| `archive` | `identifier` | `isVersionOf` |
| `directory` | `identifier` | `isVersionOf` |
| `content` | `identifier` | `isVersionOf` |

**Lo que difiere según el rol no es si, sino cuándo.** `identifier` se mina cada vez que se crea un nodo. `isVersionOf` se escribe cuando alguien dice que este nodo realiza esa obra, lo cual en un nodo de contenido suele ser en la creación y en una colección suele ser más tarde, una vez que existe una contraparte con la que emparejarse.

Eso cambia lo que pregunta `init`. Crear una colección o un archivo puede ofrecer registrar una obra existente, que es cómo el segundo de un par se conecta con el primero.

Ambos son `urn:uuid`, v4, generados una vez e inmutables. Nunca derivados de un slug, una ruta, o contenido: un identificador derivado cambia cuando se renombra lo que nombra, que es precisamente el evento que un identificador existe para sobrevivir.

`[D]` **La autoridad para minar se pone en cascada por rol**, como establece la especificación. `sat` mina para `sat`, luego transmite requisitos y valores predeterminados a `collection`, que mina colecciones, y así sucesivamente hacia abajo.

### La cadena de sujetos se acumula desde los nodos ancestros

`[D]` **Nodos ancestros, no recursos índice ancestrales.**

Todo nodo tiene un `identifier` minado en su creación, así que todo ancestro contribuye, tenga o no un recurso índice. Una sección sin página de aterrizaje sigue diciendo algo sobre lo que hay debajo de ella, y bajo la otra lectura no contribuiría nada en silencio.

Eso también mantiene a la cadena y a la cascada recorriendo el mismo árbol. Un resolutor que desciende por los nodos acumula sujetos de los nodos por los que desciende, en lugar de descender por una estructura y acumular desde otra.

El valor acumulado es el `identifier` del ancestro. Las etiquetas de visualización provienen del título propio de ese ancestro en el idioma de lectura, que es cómo una cadena derivada de `en-ca/about/legal/` y una derivada de `fr-ca/a-propos/juridique/` producen el mismo conjunto con etiquetas diferentes.

## Entradas de prueba para `satx/bin/sat init ../saty`

`[D]` **Objetivo:** `../saty`, un hermano de `satx`.

`[D]` **Con qué se envía una nueva instancia.** No un esqueleto desnudo. `init` crea la disposición de archivo de lenguaje, porque una instancia sin dónde poner su propia documentación es menos útil de lo que parece y la disposición es lo que se está probando.

```
saty/
  .saty.assets/        carpetas de autor sat y collection
  bin/                 límite
  lib/                 límite
  venvs/               límite
  en/                  archivo
    docs/
    messages/          límite
  fr/                  archivo
    docs/
    messages/          límite
```

Cada archivo de lenguaje en la raíz porta `messages/` para los catálogos traducidos de `root/bin` y `root/lib`, donde se necesita traducción.

`[D]` **Un `messages/` vacío porta una nota que dice por qué.** Las cadenas en `bin` y `lib` están escritas en inglés, así que el inglés es la fuente en lugar de una traducción de algo y `en/messages` está vacío. Eso es un hecho sobre dónde se originan las cadenas, no un descuido, y un directorio vacío sin explicación se lee como trabajo inconcluso.

El archivo `.sat-boundary` es donde va la nota, ya que es la única prosa que porta un directorio límite:

```txt
Message catalogs for <sat-root>/bin and <sat-root>/lib, in this language.

Empty: the source strings in bin and lib are written in English, so there is
nothing here to translate into English. A catalog appears here only if the
source language changes. See fr/messages for what a populated one looks like.
```

`[D]` **Valores deliberadamente diferentes**, para que la prueba demuestre que `init` no está reproduciendo las particularidades propias de `satx`:

| Campo | `satx` | `saty` |
| --- | --- | --- |
| `interface_language` | `"en"` | `"fr"` |
| `rights` | según se envía | `"CC-BY-SA-4.0"` |
| `publisher` | `"Vishpala"` | `"Test Publisher"` |

`interface_language` diferente es la más aguda de las tres: demuestra que la instancia creada no está heredando la interfaz de la instancia que la crea, que es el error más fácil de cometer y más difícil de ver.

`[D]` **Qué significa "funciona".** `saty` se lee limpio: `sat read ../saty` reporta el número de nodos esperado, sin errores, y sin advertencias que no sean deliberadas. Un lector que acepta `satx` y rechaza `saty` significa que `init` y la especificación se han separado, que es el fallo que esta prueba existe para atrapar.

## Abierto

Nada. Cada pregunta planteada antes de escribir `sat init` está respondida.

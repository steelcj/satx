# Disposición del Sistema de Archivos de una Instancia SAT

**Versión.** v0.0.2, 2026-09-13. Reemplaza a v0.0.1.

## Cambios en esta versión

- Corregida la descripción de lo que reemplaza una actualización. El artefacto de la herramienta recibe una nueva versión; una instancia de contenido no.
- Corregido `content/` de archivo a colección. Porta colecciones, así que es una.
- Reordenada la apertura para que un lector conozca qué es `satx` antes de conocer por qué eso es temporal.
- Reconciliadas las dos afirmaciones sobre el contenido que se sitúa fuera de la instancia, que se sostenían en producción y no durante el desarrollo, sin nada que lo dijera.
- Dado al caso de egreso su propia línea. Es la razón más clara de por qué los límites son necesarios en lugar de simplemente permitidos.

## Dos cosas en un directorio

`satx` es dos cosas a la vez: la herramienta SAT en desarrollo, y una instancia de contenido de ejemplo que se está probando con ella.

La producción las separa. Un artefacto de herramienta se instala en `~/.local/share/sat-tool/<versión>/` en Linux, y actualizar instala en `~/.local/share/sat-tool/<nueva-versión>/` y reemplaza el artefacto por completo. Una instancia de contenido, creada por `sat init`, nunca es tocada por una actualización.

Aquí comparten un directorio. La mitad de herramienta es `bin/`, `lib/`, `venvs/`, y los archivos `docs` y `messages` bajo cada lenguaje. La mitad de contenido es `content/`, que porta colecciones que poseería un usuario de la instancia.

Ambas mitades usan la misma cascada y nada en la especificación las distingue, porque estructuralmente no hay nada que distinguir. `satx` es una colección. `en/` y `fr/` son archivos. `content/` es una colección que porta más colecciones. La cascada las trata por igual porque son iguales.

La separación es editorial, y termina cuando `osat-sat` instala un artefacto versionado en lugar de que este directorio sea uno.

## Directorio padre de SAT

El directorio padre de SAT es la raíz de la instancia. Porta dos roles: `sat` y `collection`.

```bash
<nombre-del-nodo-sat>
satx # ejemplo
```

## Directorios límite

La instancia incluye directorios límite, que organizan archivos que no necesitan sidecar propio más allá de un marcador que le dice a SAT que la cascada se detiene aquí.

En la práctica: cuando cualquier rol de SAT encuentra un `.sat-boundary`, que es lo primero que verifica, ese directorio queda excluido de las cascadas de configuración y metadatos de SAT.

```bash
bin/.bin.assets/.sat-boundary
```

`satx/bin`, `satx/lib` y `satx/venvs` son directorios límite, como lo es cualquier otro directorio marcado de esta forma.

La técnica está igualmente disponible para los usuarios que crean contenido fuera de la instancia, para excluir directorios de las cascadas. Conviene para ingesta, egreso, y directorios de datos junto a los cuales SAT debe poder situarse sin gestionarlos.

Dos casos muestran por qué es necesaria en lugar de simplemente permitida.

**Material fuente que no es un archivo.** Una colección de escaneos de imágenes fuente no está destinada a convertirse en un archivo SAT, y SAT no debería intentar gestionarla como tal.

**Egreso que nunca debe volver.** El contenido preparado para un generador de sitios estáticos por un transmog nunca debe ser reingresado por SAT. Un límite en el directorio de destino de egreso previene exactamente eso.

### Ejemplo de contenido de `.sat-boundary`

La presencia del archivo es toda la señal. Su contenido es prosa para una persona, y nada lo analiza.

```txt
Commands, by role. Organizing: no sidecar of its own, holds no role, none of it
participates in the cascade.

sat is prototyped here rather than installed here. satx is becoming the new SAT
prototype, so bin/ holds the actual dispatcher scripts under development, in the
tree the specifications describe, rather than being populated by a separate
installed artifact the way a shipped instance eventually will be. See
HANDOVER.md and .claude/session logs for how this changed.
```

## Directorios

```bash
├── bin  # bins para archives, collection, content, directory, sat, transmog
├── en   # Archivo en inglés: documentación de SAT, y catálogos para bin y lib
│   ├── docs      # Documentación de SAT en inglés
│   └── messages  # Catálogos en inglés para satx/bin y satx/lib, si se necesitan
├── fr   # Misma disposición que satx/en. La instancia puede soportar muchos lenguajes.
│   ├── docs      # Documentación de SAT en francés
│   └── messages  # Catálogos en francés
│       └── bin   # Catálogos en francés para satx/bin
├── lib  # biblioteca de prototipo y desarrollo de la instancia
│   └── satlib
└── venvs
    └── sat
        └── 0.5.0
```

`en/` y `fr/` son archivos. `docs/` es un nodo de directorio dentro de cada uno. `messages/` es un directorio límite: los catálogos no son contenido archivado, porque un catálogo es una tabla de correspondencia indexada por cadena fuente en lugar de una realización de una obra.

## Ejemplo de contenido de usuario

En producción, alguien que usa la instancia para crear colecciones, archivos, directorios y contenido gestionados por SAT mantiene ese material en un directorio fuera de la instancia. Durante el desarrollo, `satx/content/` hace las veces de ese directorio.

La estructura es flexible. Aquí un directorio llamado `content` porta todo lo que poseería un usuario de la instancia:

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

Leyendo los roles de ese árbol: `content/` es una colección, `examples/` y `errors/` son colecciones, `websites/` es una colección, `universalcake.com/` es una colección, y `en-ca/`, `es-mx/` y `fr-ca/` son archivos. Debajo de un archivo, `cakes/` y `wedding/` son nodos de directorio.

`ingress/` es un directorio límite. El material puesto en escena allí aún no está descrito, y forzar un nodo sobre él afirmaría una descripción que nadie ha escrito.

`errors/` existe para ser leído por un lector y fallar. Cada nodo en él hace tropezar exactamente una verificación, y un lector ejecutado contra él debería reportar exactamente la lista esperada. Menos significa que falta una verificación; más significa que una verificación está equivocada.

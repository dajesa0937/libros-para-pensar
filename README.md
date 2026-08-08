# Libros para pensar

Sitio estático de lectura. Libros completos y gratuitos, con lector propio:
paginación dinámica, ajustes de accesibilidad, lectura en voz alta, generador
de QR incorporado y funcionamiento sin conexión. Sin dependencias en tiempo de
ejecución, sin rastreo, sin cookies.

## Estructura

```
web/     artefacto publicable — es lo que Netlify sirve
src/     generador y fuentes
  manuscritos/   los libros en markdown (fuente de verdad del texto)
  gen_web3.py    genera web/ a partir de los manuscritos
  qr.js          codificador QR propio, sin dependencias
  cubierta.py    cubiertas SVG
  og.py          imágenes de previsualización social
tests/   verificación
```

`web/` está versionado a propósito: permite servir el sitio sin ejecutar nada.
El generador es reproducible — regenerar sobre un árbol limpio no produce diff.

## Uso

```bash
npm install
npm run generar     # regenera web/ desde src/manuscritos
npm test            # las tres verificaciones
npm run servir      # http://localhost:8000
```

Para cambiar la dirección pública:

```bash
URL_SITIO="https://midominio.com" npm run generar
```

## Verificaciones

| Script | Qué comprueba |
|---|---|
| `test:elementos` | Que todo `getElementById` / `querySelector` del JS tenga su elemento en el HTML. Esta prueba existe porque su ausencia dejó una vez el lector muerto en producción: un `null` mataba el script entero antes de configurar la paginación. |
| `test:lector` | Ejecuta el script real contra un DOM mínimo (`tests/mini_dom.js`) y comprueba paginación, marcadores, QR, índice, ajustes y persistencia. En ambos idiomas. |
| `test:sitio` | Enlaces internos, marcadores sin sustituir, `og:image`, coherencia del sitemap, ausencia de notas internas publicables. |
| `test:qr` | Compara el codificador QR módulo a módulo contra `qrcode` de npm. No entra en `npm test` porque sólo es relevante al tocar `src/qr.js`. |

## Despliegue

Netlify, `publish = web`, `command = npm test`. Un fallo en las pruebas aborta
el deploy: el sitio en producción nunca queda roto.

Las cabeceras y redirecciones están en `netlify.toml`. Los archivos `web/_headers`
y `web/_redirects` son equivalentes y sirven de respaldo si algún día se despliega
por drag-and-drop.

© Dawin Salazar. El texto de los libros es del autor; se permite leer, descargar
y compartir libremente.

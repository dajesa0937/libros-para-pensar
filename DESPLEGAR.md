# Desplegar

El sitio ya existe en Netlify.

```
proyecto   libros-para-pensar
site-id    fae8847c-a2d1-4f31-a9c2-580e09332c6e
url        https://libros-para-pensar.netlify.app
panel      https://app.netlify.com/projects/libros-para-pensar
equipo     dajesa0937 (Free)
```

Acceso público ya habilitado (venía con SSO obligatorio por defecto).
Falta el primer deploy.

---

## Opción A — CLI, sin GitHub (2 minutos)

```bash
cd "ruta/a/proyecto Libro/sitio"
npm test                       # el gate, primero
npx netlify-cli login
npx netlify-cli deploy --prod --dir=web --site=fae8847c-a2d1-4f31-a9c2-580e09332c6e
```

Sirve para publicar hoy. No hay build en el servidor, así que las pruebas
las corres tú antes: el gate es manual.

---

## Opción B — GitHub conectado (recomendada)

Con esto cada push a `main` dispara `npm test` en Netlify y **aborta el deploy
si falla**. Es lo que evita repetir el incidente del lector muerto.

1. Crear repo en GitHub y subir este directorio:

```bash
cd "ruta/a/proyecto Libro/sitio"
git remote add origin git@github.com:TUUSUARIO/libros-para-pensar.git
git push -u origin main
```

2. En https://app.netlify.com/projects/libros-para-pensar →
   **Project configuration → Build & deploy → Link repository**.

3. Netlify lee `netlify.toml` y no hay que configurar nada a mano:

```
publish = web
command = npm test
```

---

## Comprobaciones después del primer deploy

- [ ] https://libros-para-pensar.netlify.app abre la portada
- [ ] El libro pasa de página en el celular
- [ ] `/libro` redirige al español y `/book` al inglés
- [ ] Enviar el enlace por WhatsApp: debe salir la portada como previsualización
- [ ] `curl -sI https://libros-para-pensar.netlify.app/ | grep -i cache-control`
      → `public, max-age=0, must-revalidate`
- [ ] El QR del botón ↗ apunta a la URL pública, no a una ruta local

---

## Si cambias de dominio

```bash
URL_SITIO="https://tudominio.com" npm run generar
npm test && git commit -am "url: tudominio.com" && git push
```

Reescribe las 31 ocurrencias absolutas (og:image, canonical, hreflang,
URL_PUBLICA del QR, sitemap y robots).

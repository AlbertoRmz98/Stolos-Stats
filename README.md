# Stolos Stats — Fútbol + NFL

Panel web estático con diseño oscuro y carga de archivos JSON históricos.

## Archivos
- `index.html`: panel web.
- `scripts/update_data.py`: importador de datos.
- `.github/workflows/daily-update.yml`: actualización diaria y ejecución manual.
- `data/`: aquí se generan `football.json`, `nfl.json` y `last_updated.json`.

## Instalar en GitHub
1. Descarga y descomprime el ZIP.
2. En tu repositorio, usa **Add file → Upload files** y sube el contenido de la carpeta `stolos-stats` (incluida `.github`, habilitando archivos ocultos si es necesario).
3. Confirma el commit.
4. Abre **Actions → Daily Update → Run workflow** y revisa los registros del paso **Download historical sports data**.
5. Si termina bien, verifica que existan los tres JSON dentro de `data`.

## Publicar la web
En GitHub, entra a **Settings → Pages**. Selecciona **Deploy from a branch**, rama `main`, carpeta `/(root)` y guarda. La URL se mostrará en esa pantalla al terminar la publicación.

## Límites importantes
Este es un MVP inicial, no una plataforma completa de apuestas ni un sistema de predicciones. No incluye cuentas, pagos ni suscripciones. Las fuentes de datos pueden cambiar o fallar. Football-Data.co.uk limita el uso comercial de sus datos; no monetices ni redistribuyas esos datos sin verificar y obtener los permisos necesarios. Revisa también los términos de nflverse. Para un producto comercial, sustituye las fuentes por un proveedor con licencia adecuada.

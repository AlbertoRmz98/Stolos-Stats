# Inicio rápido en GitHub (sin instalar programas)

1. Descarga y extrae el ZIP en Windows.
2. Abre tu repositorio `Stolos-Stats` en GitHub y pulsa **Code**.
3. Para cada archivo, usa **Add file → Upload files** y arrastra archivos y carpetas desde la carpeta extraída. Sube el contenido del proyecto, incluidas las carpetas ocultas `.github/workflows/`; si Windows no muestra `.github`, activa **Ver → Mostrar → Elementos ocultos** en el Explorador.
4. Si GitHub pregunta, confirma **Commit changes**. No subas solamente el ZIP.
5. Abre **Actions → Daily Update → Run workflow → Run workflow**.
6. Abre la ejecución nueva. Si termina verde, abre **Code → data** y verifica que existan `football.json`, `nfl.json` y `last_updated.json`.
7. Si falla, abre el paso rojo y copia el error completo para diagnosticarlo.

## Si ya tienes el repositorio
Sube y reemplaza estos archivos existentes: `.github/workflows/daily-update.yml`, `scripts/update_data.py`, `README.md` y `docs/INICIO_RAPIDO.md`. Crea la carpeta `scripts` si no existe. Después ejecuta el flujo manualmente.

## Límites
- La versión inicial importa la Premier League y los partidos NFL; no incluye todas las ligas ni todas las estadísticas avanzadas de jugadores.
- El panel HTML inicial todavía debe conectarse a los archivos JSON.
- Antes de comercializar estadísticas de fútbol, revisa la licencia: Football-Data.co.uk restringe el uso gratuito a uso privado/investigación, no productos comerciales.

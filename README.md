# Stolos Stats — Fútbol + NFL (starter)

Incluye una página inicial, importador Python y GitHub Actions diario.

## Contenido
- `index.html`: panel visual inicial.
- `scripts/update_data.py`: descarga CSV de resultados históricos de Premier League y datos de partidos de NFL.
- `.github/workflows/daily-update.yml`: ejecución diaria y ejecución manual.
- `data/`: aquí se guardan los JSON generados por el importador.
- `docs/INICIO_RAPIDO.md`: instrucciones para subir el proyecto.

## Importante
Este es un punto de partida, no una plataforma comercial terminada. Football-Data.co.uk indica que sus datos gratuitos son para uso privado y no para productos comerciales; consigue autorización/licencia comercial o sustituye esa fuente antes de vender suscripciones basadas en sus datos. Revisa también los términos de nflverse. La página inicial todavía requiere conectar los JSON para mostrarlos y no incluye pagos ni cuentas de suscripción.

## Actualización
GitHub Actions intenta ejecutarse diariamente a las 12:17 UTC y permite ejecución manual desde Actions → Daily Update → Run workflow. GitHub puede retrasar tareas programadas. La primera ejecución descargará los datos y los guardará en `data/`.

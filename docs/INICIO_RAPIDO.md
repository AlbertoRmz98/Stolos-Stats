# Stolos Stats — fútbol + NFL

## Qué incluye
- Dashboard oscuro adaptable a móvil.
- Importador histórico para Premier League (E0) y NFL.
- Normalización de partidos a JSON para el panel.
- GitHub Actions programado diariamente a las 10:17 UTC (la ejecución puede retrasarse).

## Ejecutar localmente
Requiere Python 3.10+ e internet:

```bash
python scripts/update_data.py
python -m http.server 8000
```
Abre http://localhost:8000.

## Activar actualización diaria
1. Crea un repositorio privado o público en GitHub y sube todos los archivos de esta carpeta.
2. En GitHub, abre **Actions** y habilita workflows si el repositorio lo solicita.
3. Ejecuta **Actualizar históricos Stolos Stats** una vez con **Run workflow** para probarlo.
4. Revisa que `data/football.json` y `data/nfl.json` se hayan actualizado. El workflow programado corre diariamente; GitHub puede retrasar la hora exacta.

## Aviso importante de licencias
El importador de fútbol usa Football-Data.co.uk para una demostración de uso privado/investigación. El propio proveedor indica que sus datos gratuitos NO son para productos comerciales, redistribución ni productos de entrenamiento automatizado/IA. **No publiques ni vendas acceso a estos datos**. Antes de comercializar Stolos Stats, sustituye el conector por una fuente que conceda por escrito derechos de uso comercial y redistribución a suscriptores. Consulta https://www.football-data.co.uk/contact.php y https://www.football-data.co.uk/data.

Los datos de NFL proceden del repositorio público nflverse; consulta licencia, atribución y condiciones vigentes antes de redistribuirlos en un producto de pago: https://github.com/nflverse/nfldata y https://github.com/nflverse/nflverse-data.

## Alcance actual
El conector de fútbol solo importa Premier League desde temporadas 2019/20 a 2025/26; algunas temporadas pueden no estar publicadas todavía o devolver errores. NFL importa el CSV histórico que esté disponible en la fuente. Esto es una base funcional de desarrollo, no un servicio comercial listo ni una garantía de cobertura completa. Los cálculos de probabilidad y el sistema de suscripciones aún no están incluidos.

#!/usr/bin/env python3
"""Stolos Stats starter importer: historical soccer scores and NFL schedules/results."""
import csv, io, json, urllib.request
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data"
OUT.mkdir(exist_ok=True)
UA = {"User-Agent": "StolosStats/1.0 (sports data importer)"}

def download(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8-sig", errors="replace")

def write_json(filename, sport, source, games):
    payload = {"sport": sport, "source": source, "generated_at": datetime.now(timezone.utc).isoformat(), "game_count": len(games), "games": games}
    (OUT / filename).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{filename}: guardados {len(games)} registros")

def import_football():
    games = []
    # Premier League seasons 2019/20 through 2025/26; only public CSVs that respond are imported.
    for start in range(19, 26):
        season_code = f"{start:02d}{(start + 1) % 100:02d}"
        url = f"https://www.football-data.co.uk/mmz4281/{season_code}/E0.csv"
        try:
            reader = csv.DictReader(io.StringIO(download(url)))
            for row in reader:
                home = (row.get("HomeTeam") or "").strip()
                away = (row.get("AwayTeam") or "").strip()
                if not home or not away:
                    continue
                raw_date = (row.get("Date") or "").strip()
                parsed_date = raw_date
                for fmt in ("%d/%m/%y", "%d/%m/%Y", "%Y-%m-%d"):
                    try:
                        parsed_date = datetime.strptime(raw_date, fmt).date().isoformat()
                        break
                    except ValueError:
                        pass
                hg, ag = (row.get("FTHG") or "").strip(), (row.get("FTAG") or "").strip()
                games.append({"date": parsed_date, "season": f"20{season_code[:2]}/20{season_code[2:]}", "league": "Premier League", "home": home, "away": away, "home_goals": int(hg) if hg.isdigit() else None, "away_goals": int(ag) if ag.isdigit() else None, "result": (row.get("FTR") or "").strip()})
            print(f"Fútbol {season_code}: OK")
        except Exception as exc:
            print(f"AVISO: fútbol {season_code} no disponible: {exc}")
    if not games:
        raise RuntimeError("No se pudo descargar ningún partido de fútbol; revisa la fuente o conexión.")
    write_json("football.json", "Fútbol", "Football-Data.co.uk / Premier League E0. Datos gratuitos para uso privado/investigación; confirmar permiso comercial antes de vender acceso a estos datos.", games)

def import_nfl():
    # nflverse publishes its schedule/game data through its GitHub data repository.
    urls = [
        "https://raw.githubusercontent.com/nflverse/nfldata/master/data/games.csv",
        "https://raw.githubusercontent.com/nflverse/nfldata/master/data/schedules.csv",
    ]
    last_error = None
    for url in urls:
        try:
            text = download(url)
            reader = csv.DictReader(io.StringIO(text))
            rows = list(reader)
            if not rows:
                raise RuntimeError("CSV vacío")
            games = []
            for row in rows:
                home = (row.get("home_team") or row.get("home_team_abbr") or "").strip()
                away = (row.get("away_team") or row.get("away_team_abbr") or "").strip()
                if not home or not away:
                    continue
                date = (row.get("gameday") or row.get("game_date") or row.get("game_date_time") or "").strip()
                hs = (row.get("home_score") or "").strip()
                aws = (row.get("away_score") or "").strip()
                games.append({"date": date, "season": row.get("season", ""), "week": row.get("week", ""), "home": home, "away": away, "home_score": int(hs) if hs.isdigit() else None, "away_score": int(aws) if aws.isdigit() else None})
            if not games:
                raise RuntimeError("No se reconocieron filas de partidos en el CSV")
            write_json("nfl.json", "NFL", "nflverse / nfldata. Revisar licencia, atribución y términos de uso de la fuente.", games)
            return
        except Exception as exc:
            last_error = exc
            print(f"AVISO: fuente NFL no disponible ({url}): {exc}")
    raise RuntimeError(f"No se pudo importar la fuente de NFL: {last_error}")

if __name__ == "__main__":
    import_football()
    import_nfl()
    (OUT / "last_updated.json").write_text(json.dumps({"updated_at": datetime.now(timezone.utc).isoformat(), "status": "success"}, indent=2), encoding="utf-8")
    print("Importación terminada.")

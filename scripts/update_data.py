#!/usr/bin/env python3
"""Importa datos públicos históricos para un MVP de Stolos Stats."""
import csv, io, json, os, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data"
OUT.mkdir(exist_ok=True)
UA = "StolosStats/1.0 (historical-data-import)"

def get_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read().decode("utf-8-sig", errors="replace")

def save_json(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def football_import():
    all_rows=[]
    # English Premier League (E0) season files; public results data.
    seasons=["1920","2021","2122","2223","2324","2425","2526"]
    for season in seasons:
        url=f"https://www.football-data.co.uk/mmz4281/{season}/E0.csv"
        try:
            text=get_text(url)
            reader=csv.DictReader(io.StringIO(text))
            count=0
            for row in reader:
                home=row.get("HomeTeam",""); away=row.get("AwayTeam","")
                if not home or not away: continue
                all_rows.append({
                    "date":row.get("Date",""),"season":season,"league":"Premier League",
                    "home_team":home,"away_team":away,
                    "home_score":row.get("FTHG",""),"away_score":row.get("FTAG",""),
                    "result":row.get("FTR","")
                }); count+=1
            print(f"Fútbol {season}: {count} registros")
        except Exception as exc:
            print(f"Aviso: no se pudo importar fútbol temporada {season}: {exc}")
    if not all_rows:
        raise RuntimeError("No se pudo descargar ningún resultado de fútbol.")
    save_json("football.json", {"source":"Football-Data.co.uk","competition":"English Premier League","records":len(all_rows),"matches":all_rows})

def nfl_import():
    # nflverse provides game-level schedules/results CSVs.
    url="https://github.com/nflverse/nfldata/raw/master/data/games.csv"
    text=get_text(url)
    reader=csv.DictReader(io.StringIO(text))
    rows=[]
    for r in reader:
        home=r.get("home_team",""); away=r.get("away_team","")
        if not home or not away: continue
        rows.append({
            "date":r.get("gameday",""),"season":r.get("season",""),
            "week":r.get("week",""),"home_team":home,"away_team":away,
            "home_score":r.get("home_score",""),"away_score":r.get("away_score",""),
            "game_type":r.get("game_type","")
        })
    if not rows: raise RuntimeError("El archivo de NFL no devolvió partidos.")
    save_json("nfl.json", {"source":"nflverse","records":len(rows),"games":rows})

def main():
    errors=[]
    for label, fn in [("fútbol",football_import),("NFL",nfl_import)]:
        try: fn()
        except Exception as exc:
            errors.append(f"{label}: {exc}")
            print(f"ERROR {label}: {exc}")
    save_json("last_updated.json", {"updated_at":datetime.now(timezone.utc).isoformat(),"errors":errors,"status":"partial" if errors else "success"})
    if errors:
        raise SystemExit("Falló una o más importaciones: " + " | ".join(errors))
    print("Importación completada correctamente.")

if __name__ == "__main__":
    main()

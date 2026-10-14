#!/usr/bin/env python3
"""Download historical football and NFL results and normalize them for Stolos Stats."""
import csv, io, json, os, urllib.request
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'; OUT.mkdir(exist_ok=True)
UA={'User-Agent':'StolosStats-MVP/1.0 (historical results import)'}
def get(url,timeout=40):
    req=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(req,timeout=timeout) as r:return r.read().decode('utf-8-sig',errors='replace')
def save(name,source,games):
    obj={'sport':name,'source':source,'generated_at':datetime.now(timezone.utc).isoformat(),'games':games}
    (OUT/f'{name}.json').write_text(json.dumps(obj,ensure_ascii=False),encoding='utf-8')
    print(f'{name}: {len(games)} partidos')
def football():
    # Football-Data is suitable for private/research use only, not commercial redistribution.
    # This starter fetches the English Premier League (E0) for seasons 2019/20–2025/26.
    allgames=[]
    for start in range(19,26):
        code=f'{start:02d}{(start+1)%100:02d}'
        url=f'https://www.football-data.co.uk/mmz4281/{code}/E0.csv'
        try:
            rows=csv.DictReader(io.StringIO(get(url)))
            for r in rows:
                date=(r.get('Date') or '').strip(); home=(r.get('HomeTeam') or '').strip(); away=(r.get('AwayTeam') or '').strip()
                if not home or not away: continue
                # Some files use dd/mm/yy and some may use ISO-like values.
                parsed=''
                for fmt in ('%d/%m/%y','%d/%m/%Y','%Y-%m-%d'):
                    try: parsed=datetime.strptime(date,fmt).date().isoformat();break
                    except ValueError: pass
                hs=(r.get('FTHG') or '').strip(); as_=(r.get('FTAG') or '').strip()
                score=f'{hs} - {as_}' if hs.isdigit() and as_.isdigit() else 'Pendiente'
                allgames.append({'date':parsed or date,'season':f'20{code[:2]}/20{code[2:]}','league':'Premier League','home':home,'away':away,'score':score})
        except Exception as e: print(f'Fútbol {code}: omitido ({e})')
    save('football','Football-Data.co.uk · Premier League E0 (uso privado/investigación; no autorizado para producto comercial)',allgames)
def nfl():
    url='https://raw.githubusercontent.com/nflverse/nfldata/master/data/games.csv'
    rows=csv.DictReader(io.StringIO(get(url,60))); games=[]
    for r in rows:
        home=(r.get('home_team') or '').strip(); away=(r.get('away_team') or '').strip()
        if not home or not away: continue
        date=(r.get('gameday') or r.get('game_date') or '').strip()
        hs=(r.get('home_score') or '').strip(); as_=(r.get('away_score') or '').strip()
        score=f'{as_} - {hs}' if hs and as_ else 'Pendiente'
        games.append({'date':date,'season':r.get('season',''),'week':r.get('week',''),'home':home,'away':away,'score':score})
    save('nfl','nflverse/nfldata games.csv (revisar licencia y atribución en fuente)',games)
if __name__=='__main__':
    football();nfl()

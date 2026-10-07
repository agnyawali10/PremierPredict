from __future__ import annotations
import os, requests, pandas as pd
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
API="https://api.football-data.org/v4"

def sample_data():
    return pd.read_csv(BASE/"data/sample_matches.csv"), pd.read_csv(BASE/"data/sample_fixtures.csv")

def live_data():
    key=os.getenv("FOOTBALL_DATA_API_KEY")
    if not key: raise RuntimeError("FOOTBALL_DATA_API_KEY is not set")
    r=requests.get(f"{API}/competitions/PL/matches",headers={"X-Auth-Token":key},timeout=20); r.raise_for_status()
    done=[]; upcoming=[]
    for m in r.json()["matches"]:
        h=m["homeTeam"]["name"]; a=m["awayTeam"]["name"]
        if m["status"]=="FINISHED":
            s=m["score"]["fullTime"]; done.append({"date":m["utcDate"],"home_team":h,"away_team":a,"home_goals":s["home"],"away_goals":s["away"]})
        elif m["status"] in {"SCHEDULED","TIMED"}: upcoming.append({"home_team":h,"away_team":a})
    return pd.DataFrame(done),pd.DataFrame(upcoming)

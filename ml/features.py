from __future__ import annotations
import pandas as pd

FEATURES = ["home_ppg", "away_ppg", "home_gd_pg", "away_gd_pg", "home_form", "away_form"]

def _snapshot(stats, team):
    s = stats.get(team, {"p":0,"pts":0,"gf":0,"ga":0,"form":[]})
    p = max(s["p"], 1)
    return s["pts"]/p, (s["gf"]-s["ga"])/p, (sum(s["form"][-5:])/max(len(s["form"][-5:]),1))

def build_training_frame(matches: pd.DataFrame):
    stats, rows, labels = {}, [], []
    for _, m in matches.sort_values("date").iterrows():
        h,a = m.home_team,m.away_team
        hp,hgd,hf = _snapshot(stats,h); ap,agd,af = _snapshot(stats,a)
        rows.append([hp,ap,hgd,agd,hf,af])
        hg,ag = int(m.home_goals),int(m.away_goals)
        labels.append("H" if hg>ag else "D" if hg==ag else "A")
        for t in (h,a): stats.setdefault(t,{"p":0,"pts":0,"gf":0,"ga":0,"form":[]})
        hpts,apts = (3,0) if hg>ag else (1,1) if hg==ag else (0,3)
        for t,gf,ga,pts in ((h,hg,ag,hpts),(a,ag,hg,apts)):
            s=stats[t]; s["p"]+=1;s["pts"]+=pts;s["gf"]+=gf;s["ga"]+=ga;s["form"].append(pts)
    return pd.DataFrame(rows, columns=FEATURES), pd.Series(labels), stats

def fixture_features(stats, home, away):
    hp,hgd,hf=_snapshot(stats,home); ap,agd,af=_snapshot(stats,away)
    return pd.DataFrame([[hp,ap,hgd,agd,hf,af]], columns=FEATURES)

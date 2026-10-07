from __future__ import annotations
import numpy as np
from .features import fixture_features
from .model import probabilities

def base_table(stats):
    return {t:{"points":s["pts"],"gd":s["gf"]-s["ga"]} for t,s in stats.items()}

def simulate(model, stats, fixtures, n=3000, seed=42):
    rng=np.random.default_rng(seed); teams=sorted(set(stats)|set(fixtures.home_team)|set(fixtures.away_team))
    positions={t:[] for t in teams}; points={t:[] for t in teams}
    probs=[]
    for _,f in fixtures.iterrows(): probs.append(probabilities(model, fixture_features(stats,f.home_team,f.away_team)))
    for _ in range(n):
        table={t:{"points":base_table(stats).get(t,{"points":0})["points"],"gd":base_table(stats).get(t,{"gd":0})["gd"]} for t in teams}
        for (_,f),p in zip(fixtures.iterrows(),probs):
            outcome=rng.choice(["H","D","A"],p=[p["home"],p["draw"],p["away"]])
            if outcome=="H": table[f.home_team]["points"]+=3; table[f.home_team]["gd"]+=1; table[f.away_team]["gd"]-=1
            elif outcome=="A": table[f.away_team]["points"]+=3; table[f.away_team]["gd"]+=1; table[f.home_team]["gd"]-=1
            else: table[f.home_team]["points"]+=1; table[f.away_team]["points"]+=1
        ranked=sorted(teams,key=lambda t:(table[t]["points"],table[t]["gd"]),reverse=True)
        for i,t in enumerate(ranked,1): positions[t].append(i); points[t].append(table[t]["points"])
    result=[]
    for t in teams:
        arr=np.array(positions[t]); pts=np.array(points[t])
        result.append({"team":t,"predicted_position":round(float(arr.mean()),2),"projected_points":round(float(pts.mean()),1),"title_probability":round(float((arr==1).mean()*100),1),"top4_probability":round(float((arr<=4).mean()*100),1),"relegation_probability":round(float((arr>=max(len(teams)-2,1)).mean()*100),1)})
    return sorted(result,key=lambda x:x["predicted_position"])

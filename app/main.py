from pathlib import Path
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.data import sample_data, live_data
from ml.features import build_training_frame
from ml.model import train_model
from ml.simulation import simulate
BASE=Path(__file__).resolve().parents[1]
app=FastAPI(title="PremierPredict",version="1.0.0")
app.mount("/static",StaticFiles(directory=BASE/"static"),name="static")
templates=Jinja2Templates(directory=BASE/"templates")

def run_prediction(source="sample", simulations=3000):
    matches,fixtures=(live_data() if source=="live" else sample_data())
    X,y,stats=build_training_frame(matches)
    model=train_model(X,y)
    return simulate(model,stats,fixtures,n=simulations)

@app.get("/",response_class=HTMLResponse)
def home(request:Request): return templates.TemplateResponse(request,"index.html",{})

@app.get("/api/predictions")
def predictions(source:str=Query("sample",pattern="^(sample|live)$"),simulations:int=Query(3000,ge=100,le=20000)):
    return {"source":source,"simulations":simulations,"predictions":run_prediction(source,simulations)}

@app.get("/health")
def health(): return {"status":"ok"}

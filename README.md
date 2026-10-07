# PremierPredict ⚽🤖

PremierPredict is a portfolio-ready Premier League forecasting application. It trains a machine-learning classifier on completed matches, estimates win/draw/loss probabilities for upcoming fixtures, and runs Monte Carlo simulations to forecast the final table.

## Why I built it
I wanted a project that combines software engineering, machine learning, data processing, API integration, and a subject I enjoy. Rather than directly predicting a final rank, PremierPredict models individual match outcomes and uses those probabilities to simulate how the rest of a season could unfold.

## Features
- FastAPI backend and JSON prediction endpoint
- Pandas feature-engineering pipeline
- scikit-learn Random Forest classifier
- Win/draw/loss probability estimates
- Monte Carlo season simulation
- Predicted position, projected points, title, top-four, and relegation probabilities
- Optional live Premier League data from football-data.org
- Offline sample mode so the repository works immediately
- Automated pytest pipeline test

## Architecture
`football-data.org / CSV -> Pandas feature engineering -> Random Forest -> match probabilities -> Monte Carlo simulation -> FastAPI -> dashboard`

### Model features
The starter model deliberately uses explainable team-level features:
- points per game
- goal difference per game
- recent five-match points/form
- home vs. away team context

This is intentionally a baseline model. Future versions can add expected goals (xG), Elo ratings, injuries, rest days, transfer values, and calibrated probabilities.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Then open `http://127.0.0.1:8000`.

## Live data
Create a `.env` file or export an environment variable:
```bash
export FOOTBALL_DATA_API_KEY="your_key_here"
```
Never commit the key. Select **Live API** in the dashboard after configuring it.

## API
`GET /api/predictions?source=sample&simulations=3000`

`GET /health`

## Tests
```bash
pytest -q
```

## ML approach
For every historical match, PremierPredict constructs features using only information available *before* that match. This avoids a common form of data leakage. A Random Forest classifier predicts H/D/A probabilities. For each remaining fixture, those probabilities are sampled during thousands of simulated seasons. The distribution of simulated finishes becomes the forecast.

## Limitations
This is a portfolio ML system, not a betting model. The bundled dataset is intentionally small so the repo runs immediately. A production-quality forecast should train on multiple seasons, use time-based validation, evaluate probability calibration/log loss, and incorporate richer football features.

## Interview talking points
- **Why probabilities instead of directly predicting table position?** League position is an emergent result of individual fixtures. Modeling matches makes the system easier to reason about and lets Monte Carlo simulation quantify uncertainty.
- **How did you avoid data leakage?** Each training row is generated before updating team statistics with that match's result.
- **Why Random Forest?** It handles nonlinear relationships, requires little preprocessing, supports multiclass probability estimates, and provides a strong understandable baseline.
- **What would you improve?** Train on several seasons, add Elo/xG features, use time-series validation, compare logistic regression/gradient boosting, calibrate probabilities, persist data in PostgreSQL, and deploy with Docker/cloud infrastructure.
- **Biggest engineering lesson?** Separating data acquisition, feature engineering, modeling, simulation, and presentation makes each layer independently testable and replaceable.

## Resume bullets
- Developed a full-stack Premier League forecasting application using Python, FastAPI, Pandas, and scikit-learn to process match data and expose ML-generated predictions through a REST API.
- Engineered a leakage-aware feature pipeline and Random Forest classifier to estimate home-win, draw, and away-win probabilities from team form, points-per-game, and goal-difference metrics.
- Implemented Monte Carlo season simulations to forecast final standings, projected points, and probabilities of title, top-four, and relegation outcomes.

# PremierPredict

PremierPredict is a full-stack machine learning web application that tracks English Premier League standings and predicts how teams may finish the season.

Rather than directly predicting a team's final position, PremierPredict estimates the probabilities of individual match outcomes and uses those probabilities to simulate the remainder of the season. The simulations produce projected standings and probabilities for outcomes such as winning the league, finishing in the top four, and relegation.

## Features

- Track Premier League standings and team performance
- Process historical and current match data
- Generate win, draw, and loss probabilities for upcoming matches
- Predict final Premier League standings
- Run Monte Carlo simulations of remaining fixtures
- Calculate projected points and finishing positions
- Estimate title, top-four, and relegation probabilities
- Display predictions through a web dashboard
- REST API for accessing prediction results
- Optional integration with live Premier League match data

## Tech Stack

**Backend**
- Python
- FastAPI

**Machine Learning & Data**
- scikit-learn
- Pandas
- NumPy
- Random Forest Classification
- Monte Carlo Simulation

**Frontend**
- HTML
- CSS
- JavaScript

**Development**
- Git
- GitHub
- pytest

## How It Works

PremierPredict uses the following pipeline:

`Match Data → Feature Engineering → ML Model → Match Probabilities → Monte Carlo Simulation → Predicted Standings`

### 1. Data Processing

Historical match results are processed to maintain statistics for each Premier League team.

Team performance information is updated chronologically so that features for a match only contain information that would have been available before that match occurred.

This prevents future information from leaking into the model's training data.

### 2. Feature Engineering

PremierPredict creates features representing differences between the home and away teams, including:

- Points per game
- Goal difference per game
- Recent form
- Home-field advantage
- Historical team performance

These features provide the machine learning model with information describing each team's performance leading into a match.

### 3. Match Prediction

A Random Forest classifier is trained on historical Premier League match results.

For an upcoming fixture, the model estimates three probabilities:

- Home win
- Draw
- Away win

Instead of treating the model's most likely result as certain, PremierPredict preserves these probabilities for use during season simulation.

### 4. Monte Carlo Season Simulation

The predicted probabilities are used to simulate the remaining Premier League fixtures repeatedly.

Each simulated match result updates the corresponding team's points and standings.

After many simulated seasons, PremierPredict aggregates the results to calculate:

- Average projected points
- Predicted finishing position
- Title probability
- Top-four probability
- Relegation probability

This approach represents uncertainty in future match results rather than producing only one deterministic final table.

## Project Structure

```text
PremierPredict/
├── app/
│   ├── data.py
│   └── main.py
├── data/
│   ├── sample_fixtures.csv
│   └── sample_matches.csv
├── ml/
│   ├── features.py
│   ├── model.py
│   └── simulation.py
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── tests/
│   └── test_core.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/PremierPredict.git
cd PremierPredict
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

Then open the local application in your browser.

FastAPI also provides interactive API documentation through the application's `/docs` endpoint.

## Data

PremierPredict includes sample match and fixture data so the application can run locally without requiring an external API key.

The application can also be configured to retrieve current football data using an external football-data API.

API credentials should be stored in environment variables and should never be committed to the repository.

See `.env.example` for the expected environment-variable configuration.

## Testing

Run the automated tests with:

```bash
pytest
```

The test suite verifies the core prediction and simulation pipeline.

## Current Limitations

The bundled dataset is intentionally small and is primarily intended to demonstrate the complete prediction pipeline.

Prediction quality depends heavily on the quantity and quality of historical match data available to the model. The current model should therefore be treated as a baseline rather than a production forecasting system.

## Future Improvements

Potential improvements include:

- Train on multiple Premier League seasons
- Add Elo team ratings
- Incorporate expected goals (xG)
- Add additional team and player statistics
- Compare Random Forest with Logistic Regression and gradient-boosting models
- Implement time-based cross-validation
- Evaluate probability calibration
- Expand automated testing
- Add team-specific prediction pages
- Improve dashboard visualizations
- Add persistent database storage
- Containerize the application with Docker
- Deploy the application publicly

## Disclaimer

PremierPredict is an educational software and machine learning project. Predictions are probabilistic estimates and should not be interpreted as guaranteed sporting outcomes.
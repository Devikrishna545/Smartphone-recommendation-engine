# Smartphone Recommendation Engine

A runnable Python project that searches the included smartphone dataset. It provides:

- a command-line interface for reviews, comparisons, and recommendations;
- a Google ADK agent that can call those same dataset-backed tools; and
- a FastAPI backend and Streamlit web dashboard; and
- unit tests that validate loading and recommendation behavior.

## Requirements

- Python 3.10 or later
- A Google AI API key only if you plan to run the ADK agent

## Setup

```bash
git clone https://github.com/Devikrishna545/Smartphone-recommendation-engine.git
cd Smartphone-recommendation-engine
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

The included dataset is at `data/smartphones.csv`; it is loaded automatically.

## Run the command-line tools

Review a phone by full or partial model name:

```bash
python -m smartphone_recommendation.cli review "OnePlus 11 5G"
```

Compare two phones:

```bash
python -m smartphone_recommendation.cli compare "OnePlus 11 5G" "OnePlus Nord CE 2 Lite 5G"
```

Find up to five phones within a budget. Prices are Indian rupees (INR), and ratings are on a 0–100 scale:

```bash
python -m smartphone_recommendation.cli recommend --max-price 60000 --min-rating 89 --require-5g
```

## Run the Google ADK agent

1. Copy the environment template and add your own key. Never commit the resulting `.env` file.

   ```bash
   cp .env.example .env
   ```

2. Set `GOOGLE_API_KEY` in `.env`.
3. Start the agent from the repository root:

   ```bash
   adk run smartphone_recommendation
   ```

The agent uses `gemini-2.5-flash` and calls only the tools in `smartphone_recommendation/tools.py` for dataset facts.

## Run the web dashboard

Open two terminals from the repository root. Activate the virtual environment in both.

Start the FastAPI backend:

```bash
source .venv/bin/activate
uvicorn smartphone_recommendation.api:app --reload
```

Start the Streamlit frontend in the second terminal:

```bash
source .venv/bin/activate
streamlit run frontend/app.py
```

Open the local address Streamlit prints (usually `http://localhost:8501`).
The dashboard provides a minimal recommendation, comparison/review, and AI-chat
interface. Recommendation and comparison work without an API key; add
`GOOGLE_API_KEY` to `.env` and restart the backend to enable AI chat.

## Test

```bash
python -m unittest discover -s tests -v
```

## Project layout

```text
data/smartphones.csv                 Dataset
smartphone_recommendation/tools.py   Dataset loading and recommendation logic
smartphone_recommendation/cli.py     Command-line entry point
smartphone_recommendation/agent.py   Google ADK root agent
smartphone_recommendation/api.py     FastAPI backend
frontend/app.py                      Streamlit frontend
tests/test_tools.py                  Automated checks
```

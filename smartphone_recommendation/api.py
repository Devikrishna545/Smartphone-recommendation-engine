"""FastAPI application used by the Streamlit dashboard."""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import unquote

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from .tools import (
    DATASET_PATH,
    compare_smartphones,
    load_smartphones,
    recommendation_records,
    recommend_smartphones,
    review_smartphone,
)

load_dotenv()

app = FastAPI(title="Smartphone Recommendation API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RecommendationRequest(BaseModel):
    max_price: int = Field(ge=0)
    min_rating: float = Field(ge=0, le=100)
    required_5g: bool = False


class ComparisonRequest(BaseModel):
    model_1: str = Field(min_length=1)
    model_2: str = Field(min_length=1)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    session_id: str | None = None


@app.get("/health")
def health() -> dict[str, object]:
    dataframe = load_smartphones()
    return {
        "status": "ok",
        "rows": len(dataframe),
        "gemini_key_set": bool(os.environ.get("GOOGLE_API_KEY")),
    }


@app.get("/stats")
def stats() -> dict[str, float | int]:
    dataframe = load_smartphones()
    return {
        "count": len(dataframe),
        "price_min": int(dataframe["price"].min()),
        "price_max": int(dataframe["price"].max()),
        "rating_min": float(dataframe["rating"].min()),
        "rating_max": float(dataframe["rating"].max()),
        "five_g_share": float(dataframe["has_5g"].mean()),
    }


@app.get("/models")
def models(limit: int = Query(default=500, ge=1, le=1_020)) -> list[str]:
    return load_smartphones()["model"].head(limit).tolist()


@app.get("/phones")
def phones(limit: int = Query(default=500, ge=1, le=1_020)) -> list[dict[str, object]]:
    dataframe = load_smartphones()
    columns = ["model", "price", "rating", "processor", "battery", "ram", "has_5g"]
    return dataframe.head(limit)[columns].to_dict(orient="records")


@app.post("/recommend")
def recommend(request: RecommendationRequest) -> dict[str, list[dict[str, object]]]:
    return {
        "results": recommendation_records(
            request.max_price,
            request.min_rating,
            request.required_5g,
        )
    }


@app.post("/compare")
def compare(request: ComparisonRequest) -> dict[str, str]:
    return {"comparison": compare_smartphones(request.model_1, request.model_2)}


@app.get("/review/{model_name}")
def review(model_name: str) -> dict[str, str]:
    return {"review": review_smartphone(unquote(model_name))}


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)) -> dict[str, int | str]:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="The uploaded CSV is empty.")

    Path(DATASET_PATH).write_bytes(content)
    load_smartphones.cache_clear()
    try:
        rows = len(load_smartphones())
    except (UnicodeDecodeError, ValueError) as error:
        raise HTTPException(status_code=400, detail=f"Invalid smartphone CSV: {error}") from error
    return {"status": "ok", "rows": rows}


@app.post("/chat")
async def chat(request: ChatRequest) -> dict[str, str | list[str]]:
    if not os.environ.get("GOOGLE_API_KEY"):
        raise HTTPException(
            status_code=503,
            detail="GOOGLE_API_KEY is not set. Add it to .env and restart the API.",
        )

    from .agent import ask_agent

    reply, tools_used, session_id = await ask_agent(request.message, request.session_id)
    return {"reply": reply, "tools_used": tools_used, "session_id": session_id}

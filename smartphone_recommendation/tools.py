"""Dataset-backed tools exposed through the CLI and Google ADK agent."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import re

import pandas as pd

DATASET_PATH = Path(__file__).resolve().parent.parent / "data" / "smartphones.csv"
REQUIRED_COLUMNS = {
    "model",
    "price",
    "rating",
    "sim",
    "processor",
    "ram",
    "battery",
    "display",
    "camera",
    "card",
    "os",
}


@lru_cache(maxsize=1)
def load_smartphones() -> pd.DataFrame:
    """Load and normalize the bundled smartphone dataset."""
    if not DATASET_PATH.is_file():
        raise FileNotFoundError(f"Smartphone dataset not found: {DATASET_PATH}")

    dataframe = pd.read_csv(DATASET_PATH)
    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Smartphone dataset is missing required columns: {missing}")

    dataframe = dataframe.dropna(subset=["model", "price", "rating", "processor", "battery", "ram", "sim"]).copy()
    dataframe["price"] = (
        dataframe["price"].astype(str).str.replace(r"[^\d.]", "", regex=True).replace("", pd.NA)
    )
    dataframe["price"] = pd.to_numeric(dataframe["price"], errors="coerce")
    dataframe["rating"] = pd.to_numeric(dataframe["rating"], errors="coerce")
    dataframe = dataframe.dropna(subset=["price", "rating"])
    dataframe["price"] = dataframe["price"].astype(int)
    dataframe["rating"] = dataframe["rating"].astype(float)
    dataframe["has_5g"] = dataframe["sim"].str.contains(r"\b5G\b", case=False, na=False)
    return dataframe


def _find_models(model_name: str) -> pd.DataFrame:
    if not model_name.strip():
        raise ValueError("A model name is required.")
    return load_smartphones()[
        load_smartphones()["model"].str.contains(re.escape(model_name), case=False, na=False)
    ]


def _format_price(price: int) -> str:
    return f"Rs. {price:,}"


def recommendation_records(
    max_price: int, min_rating: float, required_5g: bool
) -> list[dict[str, object]]:
    """Return up to five structured recommendations for API and UI consumers."""
    if max_price < 0:
        raise ValueError("Maximum price cannot be negative.")
    if not 0 <= min_rating <= 100:
        raise ValueError("Minimum rating must be between 0 and 100.")

    recommendations = load_smartphones()
    five_g_filter = recommendations["has_5g"] if required_5g else True
    recommendations = recommendations[
        (recommendations["price"] <= max_price)
        & (recommendations["rating"] >= min_rating)
        & five_g_filter
    ].sort_values(by=["rating", "price"], ascending=[False, True])
    columns = ["model", "price", "rating", "processor", "battery", "ram", "has_5g"]
    return recommendations.head(5)[columns].to_dict(orient="records")


def review_smartphone(model_name: str) -> str:
    """Return a detailed specification summary for the first matching smartphone."""
    matches = _find_models(model_name)
    if matches.empty:
        return f"Model '{model_name}' is not in the database."

    phone = matches.iloc[0]
    return "\n".join(
        [
            f"Review: {phone['model']}",
            f"Price: {_format_price(phone['price'])}",
            f"Average rating: {phone['rating']:g}/100",
            f"Processor: {phone['processor']}",
            f"RAM: {phone['ram']}",
            f"Battery: {phone['battery']}",
            f"Camera: {phone['camera']}",
            f"Display: {phone['display']}",
            f"Network: {phone['sim']}",
            f"Operating system: {phone['os']}",
        ]
    )


def compare_smartphones(model_1: str, model_2: str) -> str:
    """Compare key specifications for two matching smartphones."""
    first_matches = _find_models(model_1)
    second_matches = _find_models(model_2)
    if first_matches.empty or second_matches.empty:
        missing = []
        if first_matches.empty:
            missing.append(f"'{model_1}'")
        if second_matches.empty:
            missing.append(f"'{model_2}'")
        return f"Model(s) not in the database: {', '.join(missing)}."

    first = first_matches.iloc[0]
    second = second_matches.iloc[0]
    return "\n".join(
        [
            f"Comparison: {first['model']} vs {second['model']}",
            f"Price: {_format_price(first['price'])} vs {_format_price(second['price'])}",
            f"Average rating: {first['rating']:g}/100 vs {second['rating']:g}/100",
            f"Processor: {first['processor']} vs {second['processor']}",
            f"Battery: {first['battery']} vs {second['battery']}",
            f"RAM: {first['ram']} vs {second['ram']}",
            f"Network: {first['sim']} vs {second['sim']}",
        ]
    )


def recommend_smartphones(max_price: int, min_rating: float, required_5g: bool) -> str:
    """Recommend up to five phones within a budget and rating requirement."""
    recommendations = recommendation_records(max_price, min_rating, required_5g)

    if not recommendations:
        return "No matching smartphones found."

    lines = ["Recommended smartphones:"]
    for phone in recommendations:
        lines.append(
            f"- {phone['model']} | {_format_price(phone['price'])} | "
            f"rating {phone['rating']:g}/100 | {'5G' if phone['has_5g'] else 'non-5G'}"
        )
    return "\n".join(lines)

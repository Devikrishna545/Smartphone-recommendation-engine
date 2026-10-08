"""Minimal Streamlit interface for the Smartphone Recommendation Engine."""

from __future__ import annotations

import os
import uuid

import pandas as pd
import requests
import streamlit as st

API_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
TIMEOUT_SECONDS = 120

st.set_page_config(page_title="Smartphone Advisor", page_icon="📱", layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 5% 5%, rgba(129, 140, 248, 0.18), transparent 25rem),
            radial-gradient(circle at 95% 10%, rgba(45, 212, 191, 0.14), transparent 22rem),
            #F6F7FF;
    }
    [data-testid="stMainBlockContainer"] {
        max-width: none;
        padding-left: clamp(1.25rem, 4vw, 5rem);
        padding-right: clamp(1.25rem, 4vw, 5rem);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #24245D 0%, #3730A3 55%, #4F46E5 100%);
    }
    [data-testid="stSidebar"] * {
        color: #F8FAFC;
    }
    [data-testid="stSidebar"] .stRadio label {
        border-radius: 10px;
        padding: 0.35rem 0.45rem;
    }
    h1 {
        background: linear-gradient(90deg, #3730A3, #5B5CE2, #0F9D8B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -0.04em;
    }
    h3 {
        color: #312E81;
        font-weight: 700;
    }
    [data-testid="stDataFrame"],
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid rgba(91, 92, 226, 0.14);
        border-radius: 14px;
        box-shadow: 0 10px 30px rgba(49, 46, 129, 0.08);
    }
    .stButton > button {
        border: 0;
        border-radius: 10px;
        background: linear-gradient(135deg, #5B5CE2, #7C3AED);
        color: #FFFFFF;
        font-weight: 650;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .stButton > button:hover {
        color: #FFFFFF;
        transform: translateY(-1px);
        box-shadow: 0 8px 18px rgba(91, 92, 226, 0.28);
    }
    [data-testid="stChatInput"] {
        border: 1px solid rgba(91, 92, 226, 0.25);
        border-radius: 14px;
        box-shadow: 0 6px 18px rgba(49, 46, 129, 0.08);
    }
    .hero {
        background: linear-gradient(115deg, #EEF2FF, #FFFFFF 55%, #ECFEFF);
        border: 1px solid rgba(91, 92, 226, 0.16);
        border-radius: 16px;
        margin-bottom: 1.5rem;
        padding: 1.15rem 1.25rem;
    }
    .hero p {
        color: #475569;
        margin: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def api_get(path: str) -> object:
    response = requests.get(f"{API_URL}{path}", timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.json()


def api_post(path: str, payload: dict[str, object]) -> object:
    response = requests.post(f"{API_URL}{path}", json=payload, timeout=TIMEOUT_SECONDS)
    if not response.ok:
        raise RuntimeError(response.json().get("detail", response.text))
    return response.json()


if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "history" not in st.session_state:
    st.session_state.history = []

try:
    health = api_get("/health")
    stats = api_get("/stats")
except requests.RequestException as error:
    st.error(f"Cannot connect to the backend at {API_URL}. Start the FastAPI server first.")
    st.caption(str(error))
    st.stop()

with st.sidebar:
    st.title("📱 Smartphone Advisor")
    st.caption(f"{health['rows']} phones available")
    page = st.radio("Menu", ["Recommend", "Compare", "Ask AI"], label_visibility="collapsed")
    st.divider()
    if st.button("New conversation", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.history = []
        st.rerun()
    st.caption("Backend connected")

st.title("Smartphone Advisor")
st.markdown(
    """
    <div class="hero">
        <p><strong>Find the right phone faster.</strong><br>
        Compare real specifications, set your budget, and get data-backed recommendations in INR.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if page == "Recommend":
    st.subheader("Find a phone")
    price_col, rating_col = st.columns(2)
    with price_col:
        maximum_price = st.number_input(
            "Maximum budget (INR)",
            min_value=int(stats["price_min"]),
            max_value=int(stats["price_max"]),
            value=min(25_000, int(stats["price_max"])),
            step=500,
        )
    with rating_col:
        minimum_rating = st.number_input(
            "Minimum rating",
            min_value=float(stats["rating_min"]),
            max_value=float(stats["rating_max"]),
            value=float(stats["rating_min"]),
            step=1.0,
        )
    require_5g = st.checkbox("Only show 5G phones")

    results = api_post(
        "/recommend",
        {
            "max_price": maximum_price,
            "min_rating": minimum_rating,
            "required_5g": require_5g,
        },
    )["results"]
    if not results:
        st.info("No phones match those preferences. Increase your budget or lower the rating.")
    else:
        recommendations = pd.DataFrame(results)
        recommendations["price"] = recommendations["price"].map(lambda value: f"Rs. {value:,}")
        recommendations["network"] = recommendations["has_5g"].map({True: "5G", False: "4G"})
        st.dataframe(
            recommendations[["model", "price", "rating", "network", "processor"]],
            hide_index=True,
            use_container_width=True,
        )

elif page == "Compare":
    st.subheader("Compare two phones")
    models = api_get("/models")
    first_col, second_col = st.columns(2)
    first_phone = first_col.selectbox("First phone", models, index=0)
    second_phone = second_col.selectbox("Second phone", models, index=1)

    if st.button("Compare phones", type="primary"):
        comparison = api_post(
            "/compare",
            {"model_1": first_phone, "model_2": second_phone},
        )["comparison"]
        st.text(comparison)

    st.divider()
    st.subheader("Phone details")
    phone = st.selectbox("Choose a phone", models, key="review_phone")
    if st.button("Show details"):
        st.text(api_get(f"/review/{phone}")["review"])

else:
    st.subheader("Ask the AI")
    if not health["gemini_key_set"]:
        st.warning("AI chat is unavailable because GOOGLE_API_KEY is not configured.")
        st.caption("Add GOOGLE_API_KEY to .env, then restart the FastAPI backend.")
        st.stop()

    for message in st.session_state.history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("tools"):
                st.caption("Used: " + ", ".join(message["tools"]))

    prompt = st.chat_input("Example: Recommend a 5G phone under 20000")
    if prompt:
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Finding an answer..."):
                try:
                    result = api_post(
                        "/chat",
                        {"message": prompt, "session_id": st.session_state.session_id},
                    )
                except (requests.RequestException, RuntimeError) as error:
                    st.error(str(error))
                else:
                    st.session_state.session_id = result["session_id"]
                    st.markdown(result["reply"])
                    st.session_state.history.append(
                        {
                            "role": "assistant",
                            "content": result["reply"],
                            "tools": result["tools_used"],
                        }
                    )

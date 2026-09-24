import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
import pandas as pd
from db import fetch_all
from weather_api import get_current_weather
from graph import graph

st.set_page_config(
    page_title="Taqhi Shopping Mall AI",
    page_icon="🛍️",
    layout="wide",
)

st.title("🛍️ Taqhi Shopping Mall — AI Operations Dashboard")
st.caption("LangChain • Tools • LangGraph • Ollama • RAG • SQL Server • LangSmith")

try:
    weather = get_current_weather()
    c = st.columns(5)
    c[0].metric("Temperature", f"{weather['temperature_c']} °C")
    c[1].metric("Humidity", f"{weather['relative_humidity']} %")
    c[2].metric("Pressure", f"{weather['surface_pressure_hpa']} hPa")
    c[3].metric("Wind", f"{weather['wind_speed_kmh']} km/h")
    c[4].metric("Rain", f"{weather['precipitation_mm']} mm")
except Exception as exc:
    st.error(f"Weather unavailable: {exc}")

st.divider()

left, right = st.columns([2, 1])

with left:
    st.subheader("🤖 Ask the Mall AI")
    question = st.text_area(
        "Ask a product, catalog, weather or transport question",
        value="Is GROC-001 within its documented limits under the current weather?",
        height=100,
    )

    if st.button("Run LangGraph", type="primary"):
        with st.spinner("Running SQL + Weather + RAG + Ollama..."):
            try:
                result = graph.invoke({"question": question})
                st.markdown(result.get("answer", "No answer returned."))
                with st.expander("Raw orchestration evidence"):
                    st.json(result)
            except Exception as exc:
                st.error(str(exc))

with right:
    st.subheader("📦 Product Catalog")
    try:
        rows = fetch_all(
            """
            SELECT ProductID, ProductName, Category, Perishable,
                   Hazardous, ExpiryDate
            FROM dbo.Products
            ORDER BY Category, ProductName
            """
        )
        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )
    except Exception as exc:
        st.warning(f"SQL Server unavailable: {exc}")

st.divider()
st.subheader("📊 Transport Assessment Report")

try:
    rows = fetch_all(
        """
        SELECT TOP 50
            AssessmentID, ProductID, ExpiryOK, TemperatureOK,
            HumidityOK, PressureOK, RiskLevel, Status, Reason, CreatedAt
        FROM dbo.TransportAssessments
        ORDER BY CreatedAt DESC
        """
    )
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("No assessments recorded yet.")
except Exception as exc:
    st.info(f"Assessment report unavailable: {exc}")

st.info(
    "Demo data only. Real storage, expiry, food-safety, electrical and chemical "
    "requirements must come from approved labels, manufacturer specifications, SDS "
    "documents and validated procedures."
)

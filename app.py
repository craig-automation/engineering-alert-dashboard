import streamlit as st
import pandas as pd
import requests
import random
from datetime import datetime, timedelta


# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------

@st.cache_data
def load_assets_from_api():
    response = requests.get("https://jsonplaceholder.typicode.com/users", timeout=10)
    response.raise_for_status()
    users = response.json()

    assets = pd.DataFrame([
        {
            "asset_id": f"TRK{str(user['id']).zfill(3)}",
            "truck_type": "Reach Truck",
            "site": user["address"]["city"],
            "battery_type": "Li-ion",
            "status": "Active"
        }
        for user in users[:6]
    ])

    return assets


# --------------------------------------------------
# INCIDENT GENERATION
# --------------------------------------------------

def generate_incidents(assets):
    incident_types = [
        "Battery Fault",
        "Drive Motor Fault",
        "Navigation Error",
        "Hydraulic Leak",
        "Brake Fault"
    ]

    severities = ["Low", "Medium", "High"]
    incidents = []

    for i in range(10):
        asset = assets.sample(1).iloc[0]

        incidents.append({
            "incident_id": f"INC{1000 + i}",
            "asset_id": asset["asset_id"],
            "date": datetime.now() - timedelta(days=random.randint(0, 10)),
            "issue_type": random.choice(incident_types),
            "severity": random.choice(severities),
            "resolved": random.choice([True, False])
        })

    return pd.DataFrame(incidents)


# --------------------------------------------------
# DATA INITIALISATION
# --------------------------------------------------

try:
    with st.spinner("Loading data..."):
        assets = load_assets_from_api()

        if "incidents" not in st.session_state:
            st.session_state["incidents"] = generate_incidents(assets)

        incidents = st.session_state["incidents"]

except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()


# --------------------------------------------------
# DASHBOARD HEADER
# --------------------------------------------------

st.title("Engineering Systems Integration Dashboard")

st.write(
    "This dashboard integrates asset and incident data to identify high-risk issues, "
    "track fault patterns, and support engineering decision-making."
)


# --------------------------------------------------
# MERGE DATA
# --------------------------------------------------

merged = incidents.merge(assets, on="asset_id", how="left")


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Filters")

mode = st.sidebar.radio(
    "Data Mode",
    ["Manual", "Auto (refresh every run)"]
)

selected_site = st.sidebar.selectbox(
    "Select Site",
    options=["All"] + list(assets["site"].unique())
)

selected_severity = st.sidebar.selectbox(
    "Select Severity",
    options=["All"] + list(incidents["severity"].unique())
)

if mode == "Manual":
    if st.sidebar.button("Generate New Incident Data"):
        st.session_state["incidents"] = generate_incidents(assets)

elif mode == "Auto (refresh every run)":
    st.session_state["incidents"] = generate_incidents(assets)


# --------------------------------------------------
# ACTIVE FILTER DISPLAY
# --------------------------------------------------

st.subheader("Active Filters")
st.write(f"Site: {selected_site}")
st.write(f"Severity: {selected_severity}")


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_data = merged.copy()

if selected_site != "All":
    filtered_data = filtered_data[filtered_data["site"] == selected_site]

if selected_severity != "All":
    filtered_data = filtered_data[filtered_data["severity"] == selected_severity]


# --------------------------------------------------
# HIGH RISK FILTERED
# --------------------------------------------------

high_risk = filtered_data[
    (filtered_data["severity"] == "High") & (filtered_data["resolved"] == False)
]


# --------------------------------------------------
# SUMMARY METRICS
# --------------------------------------------------

st.subheader("Summary")

total_assets = assets["asset_id"].nunique()
total_incidents = len(filtered_data)
high_risk_count = len(high_risk)

col1, col2, col3 = st.columns(3)

col1.metric("Total Assets", total_assets)
col2.metric("Incidents (Filtered)", total_incidents)
col3.metric("High Risk Issues", high_risk_count)


# --------------------------------------------------
# DATA TABLES
# --------------------------------------------------

st.subheader("Filtered Data View")
st.dataframe(filtered_data)

st.subheader("Raw Incidents")
st.dataframe(incidents)


# --------------------------------------------------
# CRITICAL ALERT LOGIC
# --------------------------------------------------

high_risk = incidents[
    (incidents["severity"] == "High") &
    (incidents["resolved"] == False)
]

repeat_assets = incidents["asset_id"].value_counts()
repeat_assets = repeat_assets[repeat_assets > 1].index

critical_alerts = incidents[
    (incidents["asset_id"].isin(repeat_assets)) &
    (incidents["severity"] == "High") &
    (incidents["resolved"] == False)
]


# --------------------------------------------------
# CRITICAL ALERT DISPLAY
# --------------------------------------------------

st.subheader("Critical Engineering Alerts")
st.dataframe(critical_alerts)

if len(critical_alerts) > 0:
    st.error(f"🚨 {len(critical_alerts)} CRITICAL ALERTS DETECTED")
else:
    st.success("✅ No critical alerts")


# --------------------------------------------------
# RISK SCORING
# --------------------------------------------------

def severity_score(severity):
    if severity == "High":
        return 3
    elif severity == "Medium":
        return 2
    else:
        return 1

incidents["severity_score"] = incidents["severity"].apply(severity_score)


# --------------------------------------------------
# ASSET RISK RANKING
# --------------------------------------------------

asset_risk = incidents.groupby("asset_id")["severity_score"].sum().reset_index()
asset_risk = asset_risk.sort_values(by="severity_score", ascending=False).reset_index(drop=True)

st.subheader("Asset Risk Ranking")
st.dataframe(asset_risk)


# --------------------------------------------------
# TOP RISK ASSET
# --------------------------------------------------

top_asset = asset_risk.iloc[0]

st.subheader("Top Risk Asset")

st.warning(
    f"{top_asset['asset_id']} is the highest-risk asset "
    f"(Score: {top_asset['severity_score']})"
)


# --------------------------------------------------
# VISUALISATIONS
# --------------------------------------------------

st.subheader("Incidents by Site")

site_chart = filtered_data.groupby("site").size().reset_index(name="incident_count")
st.bar_chart(site_chart.set_index("site"))


# --------------------------------------------------
# INCIDENT COUNT PER ASSET
# --------------------------------------------------

incident_counts = merged.groupby("asset_id").size().reset_index(name="incident_count")
asset_summary = incident_counts.merge(assets, on="asset_id")

st.subheader("Incident Count per Asset")
st.dataframe(asset_summary)


# --------------------------------------------------
# HIGH RISK TABLE
# --------------------------------------------------

st.subheader("🚨 High Risk Unresolved Incidents")
st.dataframe(high_risk)


# --------------------------------------------------
# RAW DATA
# --------------------------------------------------

st.subheader("Assets")
st.dataframe(assets)

st.subheader("Incidents")
st.dataframe(incidents)
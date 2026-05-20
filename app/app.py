import pandas as pd
import plotly.express as px
import streamlit as st

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="SwimIQ", layout="wide")
st.title("SwimIQ 🏊‍♂️")

# -----------------------------
# Time Conversion
# -----------------------------
def time_to_seconds(t):
    if ":" in str(t):
        m, s = str(t).split(":")
        return int(m) * 60 + float(s)
    return float(t)

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("data/swim_results.csv")

df["date"] = pd.to_datetime(df["date"])
df["time_seconds"] = df["time"].apply(time_to_seconds)

df = df.sort_values(["swimmer", "event", "date"])

# Race-to-race change
df["time_change"] = df.groupby(["swimmer", "event"])["time_seconds"].diff()

# -----------------------------
# Best Event Calculation (IMPROVED)
# -----------------------------
best_event_df = df.groupby(["swimmer", "event"]).agg(
    avg_time=("time_seconds", "mean"),
    races=("time_seconds", "count")
).reset_index()

best_event_df = best_event_df.loc[
    best_event_df.groupby("swimmer")["avg_time"].idxmin()
]

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

swimmer = st.sidebar.selectbox("Select Swimmer", df["swimmer"].unique())
event = st.sidebar.selectbox("Select Event", df["event"].unique())

filtered_df = df[
    (df["swimmer"] == swimmer) &
    (df["event"] == event)
]

# -----------------------------
# Best Event Display
# -----------------------------
swimmer_best = best_event_df[best_event_df["swimmer"] == swimmer]

if not swimmer_best.empty:
    best = swimmer_best.iloc[0]

    st.success(
        f"Best Event: {best['event']} | "
        f"Avg Time: {best['avg_time']:.2f} sec | "
        f"Races: {best['races']}"
    )

# -----------------------------
# Data Display
# -----------------------------
st.subheader("Raw Data")
st.dataframe(filtered_df)

# -----------------------------
# Performance Chart (IMPROVED)
# -----------------------------
st.subheader("Performance Over Time")

fig = px.scatter(
    filtered_df,
    x="date",
    y="time_seconds",
    title=f"{swimmer} - {event} Performance"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Statistics
# -----------------------------
st.subheader("Statistics")

avg_time = filtered_df["time_seconds"].mean()
best_time = filtered_df["time_seconds"].min()
num_races = len(filtered_df)
consistency = filtered_df["time_seconds"].std()

st.metric("Average Time (sec)", f"{avg_time:.2f}")
st.metric("Best Time (sec)", f"{best_time:.2f}")
st.metric("Races", num_races)
st.metric("Consistency (std dev)", f"{consistency:.2f}")

# -----------------------------
# Improvement Analysis
# -----------------------------
st.subheader("Improvement Analysis")

improvement = filtered_df["time_change"].mean()

if pd.isna(improvement):
    st.info("Not enough data to compute improvement.")
else:
    st.metric("Avg Improvement per Race (sec)", f"{improvement:.2f}")

    if improvement < 0:
        st.success("Improving over time 🚀")
    elif improvement > 0:
        st.warning("Performance is declining slightly 📉")
    else:
        st.info("Stable performance")
import pandas as pd
import plotly.express as px
import streamlit as st

# Page title
st.title("SwimIQ")

# Load dataset
df = pd.read_csv("data/swim_results.csv")

# Display data
st.subheader("Swim Data")
st.dataframe(df)

# Swimmer selection
swimmer = st.selectbox(
    "Select Swimmer",
    df["swimmer"].unique()
)

# Event selection
event = st.selectbox(
    "Select Event",
    df["event"].unique()
)

# Filter data
filtered_df = df[
    (df["swimmer"] == swimmer) &
    (df["event"] == event)
]

# Create chart
fig = px.line(
    filtered_df,
    x="date",
    y="time",
    title=f"{swimmer} - {event} Progression",
    markers=True
)

# Display chart
st.plotly_chart(fig)
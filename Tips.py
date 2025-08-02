import streamlit as st
import pandas as pd
import os
from datetime import date

# File to store tip data
DATA_FILE = "tony_tips.csv"

# Load existing data or create new DataFrame
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Date", "Amount"])

st.title("Tony's Tip Tracker 💵")

# Input form
with st.form("tip_entry"):
    tip_date = st.date_input("Date", value=date.today())
    tip_amount = st.number_input("Tip Amount ($)", min_value=0.0, step=0.01)
    submitted = st.form_submit_button("Add Entry")

    if submitted:
        new_row = pd.DataFrame([[tip_date, tip_amount]], columns=["Date", "Amount"])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Tip added!")

# Display log
st.subheader("Tip Log")
st.dataframe(df)

# Stats
st.subheader("Summary")
if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"])
    total = df["Amount"].sum()
    avg = df["Amount"].mean()
    st.write(f"**Total Tips:** ${total:.2f}")
    st.write(f"**Average Tip Night:** ${avg:.2f}")

    # Optional: Chart
    chart_data = df.groupby("Date")["Amount"].sum()
    st.line_chart(chart_data)
else:
    st.write("No data yet!")

import streamlit as st
import pandas as pd
import sqlite3
from chatbot import ask_bot

st.set_page_config(page_title="Retail Dashboard", layout="wide")
st.title("🛍️ Retail Performance Dashboard with AI Chat")

uploaded_file = st.file_uploader("📤 Upload your sales CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    conn = sqlite3.connect("database/sales.db")
    df.to_sql("sales", conn, if_exists="replace", index=False)
    st.success("✅ Data uploaded to database.")

    st.header("📊 KPIs")
    col1, col2 = st.columns(2)
    col1.metric("Total Sales", f"₹{df['Total Sales'].sum():,.0f}")
    col2.metric("Average Sale", f"₹{df['Total Sales'].mean():,.0f}")

    st.header("📍 Sales by Region")
    region_sales = df.groupby("Region")["Total Sales"].sum().reset_index()
    st.bar_chart(region_sales.set_index("Region"))

st.header("🤖 Ask Retail AI")
user_input = st.text_input("Ask something about sales:")
if user_input:
    response = ask_bot(f"You are a retail analytics assistant. Answer: {user_input}")
    st.success(response)
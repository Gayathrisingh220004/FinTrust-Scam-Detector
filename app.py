
import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re

# Load model and vectorizer
model = joblib.load("scam_detector.pkl")
vectorizer = joblib.load("vectorizer.pkl")
df = pd.read_csv("fintrust_sms_dataset.csv")

# Clean text function
@st.cache_data
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\\S+|www\\S+|https\\S+", '', text)
    text = re.sub(r"\\b\\d{4,}\\b", '', text)
    text = re.sub(r"[^\\w\\s]", '', text)
    return text

# Page UI
st.set_page_config(page_title="FinTrust - Scam Detector", layout="wide")
st.title("📱 FinTrust - AI-Powered Scam Detector")
st.markdown("Enter a suspicious SMS below to check if it's a scam or legit.")

# Input box
with st.form("scam_form"):
    user_sms = st.text_area("Paste the SMS text here")
    submit = st.form_submit_button("Analyze")

if submit and user_sms:
    cleaned = clean_text(user_sms)
    vect = vectorizer.transform([cleaned])
    pred = model.predict(vect)[0]

    if pred == 1:
        st.error("⚠️ Alert! This SMS is likely a SCAM.")
    else:
        st.success("✅ This SMS appears to be LEGITIMATE.")

# Visual Insights
st.markdown("---")
st.subheader("📊 Dataset Overview & Visual Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### SMS Type Distribution")
    fig, ax = plt.subplots()
    sns.countplot(x='Label', data=df, ax=ax)
    st.pyplot(fig)

with col2:
    st.markdown("### Word Cloud - Scam SMS")
    scam_text = " ".join(df[df['Label'] == 'Scam']['SMS Text'])
    scam_wc = WordCloud(background_color="white").generate(scam_text)
    fig2, ax2 = plt.subplots()
    ax2.imshow(scam_wc, interpolation='bilinear')
    ax2.axis('off')
    st.pyplot(fig2)

st.markdown("---")
st.markdown("🚀 Built with love for AI + Finance by Gayathri Singh 💖")

import streamlit as st
import pandas as pd
from inference import simple_sentiment_analysis
from category_classifier import predict_governance_category


# =========================
# Bilingual Text Dictionary
# =========================
TEXT = {
    "en": {
        "title": "Zakat Sentiment Intelligence System",
        "subtitle": "AI-powered analysis of zakat discourse",
        "language": "Language",
        "input_text": "Enter social media text",
        "analyze": "Analyze",
        "sentiment": "Sentiment",
        "confidence": "Confidence",
        "category": "Governance Category"
    },
    "ms": {
        "title": "Sistem Analisis Sentimen Zakat",
        "subtitle": "Analisis wacana zakat berasaskan AI",
        "language": "Bahasa",
        "input_text": "Masukkan teks media sosial",
        "analyze": "Analisis",
        "sentiment": "Sentimen",
        "confidence": "Keyakinan",
        "category": "Kategori Tadbir Urus"
    }
}

# =========================
# Language Selector
# =========================
lang = st.sidebar.selectbox(
    "Language / Bahasa",
    ["English", "Bahasa Malaysia"]
)

lang_code = "en" if lang == "English" else "ms"
T = TEXT[lang_code]

# =========================
# App Header
# =========================
st.title(T["title"])
st.subheader(T["subtitle"])

# =========================
# Input Type
# =========================
input_type = st.radio(
    "Input Type",
    ["Single Text", "CSV File"]
)

# ---------- SINGLE TEXT ----------
if input_type == "Single Text":
    user_text = st.text_area(
        T["input_text"],
        height=150
    )

# ---------- CSV FILE ----------
else:
    uploaded_file = st.file_uploader(
        "Upload CSV file (must contain a 'text' column)",
        type=["csv"]
    )

# =========================
# Analyze Button
# =========================
if st.button(T["analyze"]):

    # ---------- SINGLE TEXT ----------
    if input_type == "Single Text":
        if user_text.strip() == "":
            st.warning("Please enter text.")
        else:
            sentiment, confidence = simple_sentiment_analysis(user_text)
            category = predict_governance_category(user_text)

            st.success(f"{T['sentiment']}: {sentiment}")
            st.info(f"{T['confidence']}: {confidence:.2f}")
            st.warning(f"{T['category']}: {category}")

    # ---------- CSV FILE ----------
    else:
        if uploaded_file is None:
            st.warning("Please upload a CSV file.")
        else:
            df = pd.read_csv(uploaded_file)

            if "text" not in df.columns:
                st.error("CSV must contain a column named 'text'")
            else:
                sentiments = []
                confidences = []
                categories = []

                for t in df["text"]:
                    s, c = simple_sentiment_analysis(str(t))
                    cat = predict_governance_category(str(t))

                    sentiments.append(s)
                    confidences.append(c)
                    categories.append(cat)

                df["Sentiment"] = sentiments
                df["Confidence"] = confidences
                df["Governance Category"] = categories

                # ---- Table ----
                st.subheader("Analysis Results")
                st.dataframe(df)

                # ---- Download ----
                st.download_button(
                    label="Download Results as CSV",
                    data=df.to_csv(index=False),
                    file_name="zakat_sentiment_results.csv",
                    mime="text/csv"
                )

                # ---- Charts ----
                st.subheader("Sentiment Distribution")
                sentiment_counts = df["Sentiment"].value_counts()
                st.bar_chart(sentiment_counts)

                st.subheader("Governance Category Distribution")
                category_counts = df["Governance Category"].value_counts()
                st.bar_chart(category_counts)

import streamlit as st
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
# Text Input
# =========================
user_text = st.text_area(
    T["input_text"],
    height=150
)

# =========================
# Analyze Button (Placeholder)
# =========================
if st.button(T["analyze"]):
    if user_text.strip() == "":
        st.warning("Please enter text.")
    else:
        sentiment, confidence = simple_sentiment_analysis(user_text)
        category = predict_governance_category(user_text)

        st.success(f"{T['sentiment']}: {sentiment}")
        st.info(f"{T['confidence']}: {confidence:.2f}")
        st.warning(f"{T['category']}: {category}")

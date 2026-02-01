import streamlit as st

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
        # Placeholder output (AI comes next)
        st.success(f"{T['sentiment']}: Neutral")
        st.info(f"{T['confidence']}: 0.00")
        st.warning(f"{T['category']}: Not yet classified")

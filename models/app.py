import streamlit as st
import pandas as pd

from ensemble_inference import (
    load_base_models,
    load_boosting_model,
    ensemble_predict
)

from category_classifier import predict_governance_category


# =========================
# LOAD MODELS (RUN ONCE)
# =========================
@st.cache_resource
def load_models():
    model_paths = {
        "bert": "models/Zakat-bert-base-uncased",
        "distilbert": "models/Zakat-distilbert-base-uncased"
    }

    loaded_models = load_base_models(model_paths)
    boosting_model = load_boosting_model("models/boosting_model.pkl")

    return loaded_models, boosting_model


loaded_models, boosting_model = load_models()


# =========================
# Explanation & Recommendation
# =========================
def explain_sentiment(sentiment, lang):
    explanations = {
        "en": {
            "Positive": "Public perception is generally favourable.",
            "Neutral": "Public discourse is informational or neutral.",
            "Negative": "Public dissatisfaction detected and may require attention."
        },
        "ms": {
            "Positive": "Persepsi awam secara umum adalah positif.",
            "Neutral": "Wacana awam bersifat neutral atau berbentuk maklumat.",
            "Negative": "Ketidakpuasan awam dikesan dan mungkin memerlukan perhatian."
        }
    }
    return explanations[lang].get(sentiment, "")


def recommend_action(category, lang):
    actions = {
        "en": {
            "Leadership Commitment": "Strengthen leadership communication and commitment.",
            "Stakeholder Engagement": "Enhance engagement with zakat payers and recipients.",
            "Data Quality & Accessibility": "Improve clarity and accessibility of zakat information.",
            "Ethical Data Governance": "Ensure transparency and ethical handling of zakat data.",
            "Technological Readiness": "Upgrade and stabilise digital zakat systems.",
            "Continuous Evaluation": "Review feedback and improve service processes.",
            "General Zakat Discourse": "Monitor public discourse for emerging issues."
        },
        "ms": {
            "Leadership Commitment": "Perkukuhkan komunikasi dan komitmen kepimpinan.",
            "Stakeholder Engagement": "Tingkatkan penglibatan pembayar dan penerima zakat.",
            "Data Quality & Accessibility": "Perbaiki kejelasan dan kebolehcapaian maklumat zakat.",
            "Ethical Data Governance": "Pastikan ketelusan dan pengurusan data zakat beretika.",
            "Technological Readiness": "Naik taraf dan stabilkan sistem zakat digital.",
            "Continuous Evaluation": "Semak maklum balas dan perbaiki proses perkhidmatan.",
            "General Zakat Discourse": "Pantau wacana awam untuk isu yang berpotensi."
        }
    }
    return actions[lang].get(category, "")


# =========================
# Language
# =========================
TEXT = {
    "en": {
        "title": "Zakat Sentiment Intelligence System",
        "subtitle": "AI-powered analysis of zakat discourse",
        "input_text": "Enter text",
        "multi_input": "Enter multiple texts (one per line)",
        "analyze": "Analyze"
    },
    "ms": {
        "title": "Sistem Analisis Sentimen Zakat",
        "subtitle": "Analisis wacana zakat berasaskan AI",
        "input_text": "Masukkan teks",
        "multi_input": "Masukkan banyak teks (satu baris setiap teks)",
        "analyze": "Analisis"
    }
}

lang = st.sidebar.selectbox("Language / Bahasa", ["English", "Bahasa Malaysia"])
lang_code = "en" if lang == "English" else "ms"
T = TEXT[lang_code]


# =========================
# UI
# =========================
st.title(T["title"])
st.subheader(T["subtitle"])

input_type = st.radio(
    "Input Type",
    ["Single Text", "Multiple Text", "CSV File"]
)

if input_type == "Single Text":
    user_text = st.text_area(T["input_text"])

elif input_type == "Multiple Text":
    multi_text = st.text_area(T["multi_input"])

else:
    uploaded_file = st.file_uploader("Upload CSV (column: text)", type=["csv"])


# =========================
# ANALYZE
# =========================
if st.button(T["analyze"]):

    # ---------- SINGLE ----------
    if input_type == "Single Text":
        texts = [user_text]

    elif input_type == "Multiple Text":
        texts = [t for t in multi_text.split("\n") if t.strip() != ""]

    else:
        if uploaded_file is None:
            st.warning("Upload CSV first.")
            st.stop()

        df = pd.read_csv(uploaded_file)

        if "text" not in df.columns:
            st.error("CSV must have 'text' column")
            st.stop()

        texts = df["text"].astype(str).tolist()

    # 🔥 ENSEMBLE PREDICTION
    sentiments, confidences = ensemble_predict(
        texts,
        loaded_models,
        boosting_model
    )

    categories = [predict_governance_category(t) for t in texts]

    results_df = pd.DataFrame({
        "Text": texts,
        "Sentiment": sentiments,
        "Confidence": confidences,
        "Governance Category": categories
    })

    st.subheader("Results")
    st.dataframe(results_df)

    st.subheader("Sentiment Distribution")
    st.bar_chart(results_df["Sentiment"].value_counts())

    st.subheader("Governance Category Distribution")
    st.bar_chart(results_df["Governance Category"].value_counts())

    # Explanation (single input only)
    if input_type == "Single Text":
        st.caption(explain_sentiment(sentiments[0], lang_code))
        st.caption(recommend_action(categories[0], lang_code))
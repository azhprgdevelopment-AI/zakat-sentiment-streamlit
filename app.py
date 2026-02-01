import streamlit as st
import pandas as pd
from inference import simple_sentiment_analysis
from category_classifier import predict_governance_category


# =========================
# Explanation & Recommendation Helpers
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
# Bilingual Text Dictionary
# =========================
TEXT = {
    "en": {
        "title": "Zakat Sentiment Intelligence System",
        "subtitle": "AI-powered analysis of zakat discourse",
        "input_text": "Enter social media text",
        "analyze": "Analyze",
        "sentiment": "Sentiment",
        "confidence": "Confidence",
        "category": "Governance Category"
    },
    "ms": {
        "title": "Sistem Analisis Sentimen Zakat",
        "subtitle": "Analisis wacana zakat berasaskan AI",
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

            st.caption(explain_sentiment(sentiment, lang_code))
            st.caption(recommend_action(category, lang_code))

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

                st.subheader("Analysis Results")
                st.dataframe(df)

                st.download_button(
                    label="Download Results as CSV",
                    data=df.to_csv(index=False),
                    file_name="zakat_sentiment_results.csv",
                    mime="text/csv"
                )

                st.subheader("Sentiment Distribution")
                st.bar_chart(df["Sentiment"].value_counts())

                st.subheader("Governance Category Distribution")
                st.bar_chart(df["Governance Category"].value_counts())

                st.subheader("Interpretation & Recommended Actions")
                dominant_category = df["Governance Category"].value_counts().idxmax()
                st.markdown(recommend_action(dominant_category, lang_code))

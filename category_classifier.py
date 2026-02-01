def predict_governance_category(text):
    text = text.lower()

    if any(k in text for k in ["pemimpin", "pengurusan", "kepimpinan", "leadership"]):
        return "Leadership Commitment"

    if any(k in text for k in ["asnaf", "masyarakat", "penerima", "stakeholder"]):
        return "Stakeholder Engagement"

    if any(k in text for k in ["maklumat", "info", "jelas", "transpar"]):
        return "Data Quality & Accessibility"

    if any(k in text for k in ["amanah", "adil", "etika", "ethical"]):
        return "Ethical Data Governance"

    if any(k in text for k in ["sistem", "online", "aplikasi", "website"]):
        return "Technological Readiness"

    if any(k in text for k in ["aduan", "lewat", "penambahbaikan", "complaint"]):
        return "Continuous Evaluation"

    return "General Zakat Discourse"

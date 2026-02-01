def simple_sentiment_analysis(text):
    text = text.lower()

    positive_keywords = [
        "terima kasih", "alhamdulillah", "baik", "membantu",
        "senang", "mudah", "cekap", "happy", "good", "help"
    ]

    negative_keywords = [
        "lewat", "lambat", "tidak jelas", "masalah", "susah",
        "rumit", "delay", "bad", "complaint", "tidak puas hati"
    ]

    for word in positive_keywords:
        if word in text:
            return "Positive", 0.70

    for word in negative_keywords:
        if word in text:
            return "Negative", 0.75

    return "Neutral", 0.60

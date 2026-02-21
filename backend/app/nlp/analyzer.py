from transformers import pipeline
import re

sentiment_en = None
sentiment_tr = None
ner_analyzer = None


def get_sentiment_en():
    global sentiment_en
    if sentiment_en is None:
        sentiment_en = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment"
        )
    return sentiment_en


def get_sentiment_tr():
    global sentiment_tr
    if sentiment_tr is None:
        sentiment_tr = pipeline(
            "sentiment-analysis",
            model="savasy/bert-base-turkish-sentiment-cased"
        )
    return sentiment_tr


def get_ner_analyzer():
    global ner_analyzer
    if ner_analyzer is None:
        ner_analyzer = pipeline(
            "ner",
            model="dbmdz/bert-large-cased-finetuned-conll03-english",
            aggregation_strategy="simple"
        )
    return ner_analyzer


def detect_language(text: str) -> str:
    turkish_chars = set("çğıöşüÇĞİÖŞÜ")
    turkish_words = {"bir", "ve", "ile", "bu", "da", "de", "için", "çok",
                     "ama", "ben", "sen", "biz", "gibi", "olan", "var",
                     "yok", "daha", "kadar", "sonra", "önce", "iyi", "kötü"}
    
    if any(c in turkish_chars for c in text):
        return "tr"
    
    words = text.lower().split()
    tr_count = sum(1 for w in words if w in turkish_words)
    if tr_count >= 2 or (len(words) > 0 and tr_count / len(words) > 0.2):
        return "tr"
    
    return "en"


def analyze_text(text: str) -> dict:
    language = detect_language(text)

    # Duygu Analizi
    if language == "tr":
        sent = get_sentiment_tr()
        sent_result = sent(text[:512])[0]
        label = sent_result["label"].lower()
        score = round(float(sent_result["score"]), 4)
    else:
        sent = get_sentiment_en()
        sent_result = sent(text[:512])[0]
        stars = int(sent_result["label"][0])
        if stars >= 4:
            label = "positive"
        elif stars <= 2:
            label = "negative"
        else:
            label = "neutral"
        score = round(float(sent_result["score"]), 4)

    # NER
    ner = get_ner_analyzer()
    entities = ner(text[:512])
    entity_list = [
        {"word": e["word"], "entity": e["entity_group"], "score": round(float(e["score"]), 3)}
        for e in entities
    ]

    # Keyword çıkarma
    words = text.lower().split()
    stopwords_all = {
        "the", "a", "an", "is", "are", "was", "were", "in", "on", "at",
        "to", "for", "of", "and", "or", "but", "it", "this", "that",
        "bir", "ve", "ile", "bu", "da", "de", "için", "çok", "ama",
        "ben", "sen", "biz", "siz", "olan", "var", "yok", "gibi"
    }
    word_freq = {}
    for w in words:
        w = re.sub(r'[.,!?;:\'"()\[\]]', '', w)
        if len(w) > 2 and w not in stopwords_all:
            word_freq[w] = word_freq.get(w, 0) + 1
    keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "language": language,
        "sentiment_label": label,
        "sentiment_score": score,
        "entities": entity_list,
        "keywords": [{"word": k, "count": v} for k, v in keywords],
    }
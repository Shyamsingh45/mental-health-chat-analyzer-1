# Lightweight emotion detection using TextBlob + keyword heuristics
from textblob import TextBlob

KEYMAP = {
    'sad': ['sad','depress','unhappy','lonely','cry','hopeless','down'],
    'happy': ['happy','joy','glad','awesome','great','excited','love','yay'],
    'angry': ['angry','mad','furious','annoyed','hate','irritat'],
    'stressed': ['stress','anxious','anxiety','worried','overwhelm','panic'],
    'neutral': []
}

def _classify_text(text):
    if not text or not isinstance(text, str):
        return 'neutral'
    lower = text.lower()
    for label, words in KEYMAP.items():
        for w in words:
            if w in lower:
                return label
    # fallback to polarity
    try:
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.25:
            return 'happy'
        if polarity < -0.25:
            return 'sad'
    except Exception:
        pass
    return 'neutral'

def get_emotions(df):
    df = df.copy()
    df['emotion'] = df['message'].fillna('').apply(_classify_text)
    return df

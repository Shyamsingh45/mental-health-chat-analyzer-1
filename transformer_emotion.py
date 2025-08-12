# Optional transformer-based classifier (imports inside function to avoid heavy import at module load)
def predict_with_transformer(df, model_name="j-hartmann/emotion-english-distilroberta-base"):
    """
    Predict emotions using a Hugging Face transformers pipeline.
    Requires: transformers, torch
    """
    from transformers import pipeline
    import pandas as pd
    classifier = pipeline("text-classification", model=model_name, top_k=1)
    df = df.copy()
    emotions = []
    for text in df['message'].fillna(''):
        try:
            res = classifier(text)
            if isinstance(res, list):
                emotions.append(res[0]['label'])
            else:
                emotions.append(res['label'])
        except Exception:
            emotions.append('neutral')
    df['emotion'] = emotions
    return df

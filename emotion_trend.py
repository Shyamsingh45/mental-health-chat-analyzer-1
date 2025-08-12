import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# --- Helper: Ensure Date and Emotion columns exist ---
def ensure_date_emotion(df, date_col="Date", emotion_col="Emotion"):
    # --- Ensure Date column ---
    if date_col not in df.columns:
        # Priority 1: exact match ignoring case
        exact_date = [c for c in df.columns if c.lower() == "date"]
        if exact_date:
            df[date_col] = pd.to_datetime(df[exact_date[0]], errors="coerce")
        else:
            # Priority 2: any column containing "date" or "time"
            possible_date = [c for c in df.columns if "date" in c.lower() or "time" in c.lower()]
            if possible_date:
                df[date_col] = pd.to_datetime(df[possible_date[0]], errors="coerce")
            else:
                raise ValueError("❌ No Date column found or detected.")

    # --- Ensure Emotion column ---
    if emotion_col not in df.columns:
        # Priority 1: exact match ignoring case
        exact_emotion = [c for c in df.columns if c.lower() == "emotion"]
        if exact_emotion:
            df[emotion_col] = df[exact_emotion[0]].astype(str)
        else:
            # Priority 2: column names containing "emotion"
            possible_emotion = [c for c in df.columns if "emotion" in c.lower()]
            if possible_emotion:
                df[emotion_col] = df[possible_emotion[0]].astype(str)
            else:
                # Priority 3: fallback to 'sentiment' if emotion not found
                possible_sentiment = [c for c in df.columns if "sentiment" in c.lower()]
                if possible_sentiment:
                    df[emotion_col] = df[possible_sentiment[0]].astype(str)
                else:
                    raise ValueError("❌ No Emotion or Sentiment column found or detected.")

    return df
# --- Plotly version for Streamlit ---
def plot_emotion_trend_plotly(df, date_col="Date", emotion_col="Emotion"):
    df = ensure_date_emotion(df, date_col, emotion_col)
    fig = px.line(
        df.groupby([date_col, emotion_col]).size().reset_index(name="Count"),
        x=date_col,
        y="Count",
        color=emotion_col,
        markers=True,
        title="Emotion Trend Over Time"
    )
    return fig


# --- Matplotlib version for PNG saving ---
def save_emotion_trend_png(df, date_col="Date", emotion_col="Emotion", output_file="emotion_trend.png"):
    df = ensure_date_emotion(df, date_col, emotion_col)

    trend_df = df.groupby([date_col, emotion_col]).size().unstack(fill_value=0)

    plt.figure(figsize=(10, 6))
    for col in trend_df.columns:
        plt.plot(trend_df.index, trend_df[col], marker='o', label=col)

    plt.title("Emotion Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

    print(f"✅ Emotion trend chart saved as '{output_file}'")

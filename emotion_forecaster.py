def forecast_emotions(df):
    if df.empty:
        return 'neutral'
    recent = df.tail(50)
    return recent['emotion'].mode().iloc[0] if not recent['emotion'].mode().empty else 'neutral'

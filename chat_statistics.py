import pandas as pd
import plotly.express as px

def get_chat_stats(df):
    stats = {}
    stats['total_messages'] = int(len(df))
    stats['active_days'] = int(df['timestamp'].dt.date.nunique() if not df['timestamp'].isna().all() else 0)
    stats['unique_senders'] = int(df['sender'].nunique())
    stats['unique_emotions'] = int(df['emotion'].nunique())
    stats['top_emotion'] = df['emotion'].mode().iloc[0] if not df['emotion'].mode().empty else 'neutral'
    return stats

def plot_emotion_distribution(df):
    fig = px.pie(df, names='emotion', title='Emotion Distribution', hole=0.4)
    return fig

def plot_top_users(df):
    counts = df['sender'].value_counts().nlargest(10).reset_index()
    counts.columns = ['sender','count']
    fig = px.bar(counts, x='sender', y='count', title='Top Active Users')
    return fig

def plot_message_heatmap_plotly(df):
    df2 = df.copy()
    df2['day'] = pd.to_datetime(df2['timestamp']).dt.day_name()
    df2['hour'] = pd.to_datetime(df2['timestamp']).dt.hour
    heat = df2.groupby(['day','hour']).size().reset_index(name='count')
    heat_pivot = heat.pivot(index='day', columns='hour', values='count').fillna(0)
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    heat_pivot = heat_pivot.reindex(days).fillna(0)
    fig = px.imshow(heat_pivot, labels=dict(x='Hour', y='Day', color='Messages'), title='Activity Heatmap (Day vs Hour)')
    return fig

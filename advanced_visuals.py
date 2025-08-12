import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

OUTPUT = 'outputs'
os.makedirs(OUTPUT, exist_ok=True)

def generate_wordcloud(df, outpath=os.path.join(OUTPUT,'wordcloud.png')):
    text = ' '.join(df['message'].astype(str).tolist())
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    wc.to_file(outpath)
    return outpath

def generate_emotion_heatmap(df, outpath=os.path.join(OUTPUT,'emotion_heatmap.png')):
    df2 = df.copy()
    df2['hour'] = pd.to_datetime(df2['timestamp']).dt.hour
    heat = df2.groupby(['hour','emotion']).size().unstack(fill_value=0)
    plt.figure(figsize=(10,5))
    sns.heatmap(heat, cmap='coolwarm', annot=True, fmt='d')
    plt.title('Emotion by Hour')
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()
    return outpath

def generate_emotion_pie_chart(df, outpath=os.path.join(OUTPUT,'emotion_pie.png')):
    counts = df['emotion'].value_counts()
    plt.figure(figsize=(6,6))
    counts.plot.pie(autopct='%1.1f%%', ylabel='')
    plt.title('Emotion Distribution')
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()
    return outpath

def show_advanced_graphs(df):
    generate_wordcloud(df)
    generate_emotion_heatmap(df)
    generate_emotion_pie_chart(df)

import pandas as pd
import os, zipfile, io
from advanced_visuals import generate_wordcloud, generate_emotion_heatmap, generate_emotion_pie_chart
def export_excel(df, out='outputs/chat_emotions.xlsx'):
    os.makedirs('outputs', exist_ok=True)
    df.to_excel(out, index=False)
    return out

def export_png_bundle(df, outzip='outputs/chat_images.zip'):
    os.makedirs('outputs', exist_ok=True)
    paths = []
    paths.append(generate_wordcloud(df))
    paths.append(generate_emotion_heatmap(df))
    paths.append(generate_emotion_pie_chart(df))
    # create zip
    with zipfile.ZipFile(outzip, 'w') as zf:
        for p in paths:
            if os.path.exists(p):
                zf.write(p, arcname=os.path.basename(p))
    return outzip

# compatibility function used earlier
def make_zip_bundle(df):
    return export_png_bundle(df)

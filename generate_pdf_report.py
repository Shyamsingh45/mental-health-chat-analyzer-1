from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

def generate_pdf_report(df, outpath='outputs/mental_health_report.pdf'):
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(outpath, pagesize=A4)
    elems = []

    elems.append(Paragraph('Mental Health Chat Analysis', styles['Title']))
    elems.append(Spacer(1,12))

    total = len(df)
    unique_senders = df['sender'].nunique()
    emotions = df['emotion'].value_counts().to_dict()

    elems.append(Paragraph(f'Total messages: {total}', styles['Normal']))
    elems.append(Paragraph(f'Unique senders: {unique_senders}', styles['Normal']))
    elems.append(Spacer(1,12))

    elems.append(Paragraph('Emotion counts:', styles['Heading2']))
    data = [['Emotion','Count']]
    for k,v in emotions.items():
        data.append([k,str(v)])
    t=Table(data, hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(1,0),colors.lightblue),('GRID',(0,0),(-1,-1),0.5,colors.gray)]))
    elems.append(t)
    elems.append(Spacer(1,12))

    imgs = ['outputs/emotion_trend.png','outputs/wordcloud.png','outputs/emotion_heatmap.png']
    for im in imgs:
        if os.path.exists(im):
            elems.append(Paragraph(os.path.basename(im), styles['Heading3']))
            elems.append(Image(im, width=400, height=200))
            elems.append(Spacer(1,12))

    doc.build(elems)
    return outpath

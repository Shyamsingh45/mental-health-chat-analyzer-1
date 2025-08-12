import streamlit as st
import pandas as pd
import os
from preprocess import clean_chat
from emotion_classifier import get_emotions as get_emotions_simple
from emotion_trend import ensure_date_emotion,plot_emotion_trend_plotly,save_emotion_trend_png
from chatbot_response import generate_response
from intent_detector import detect_intent
from utils.hinglish_translation import translate_hinglish_to_english
from voice_utils import tts_gtts, record_audio_to_text
from generate_pdf_report import generate_pdf_report
from utils.hinglish_translation import translate_hinglish_to_english
from export_utils import export_excel, export_png_bundle, make_zip_bundle

st.set_page_config(
    page_title="Advanced Mental Health Analyzer",
    layout="wide",
    page_icon="🧠"
)

# --- UI Settings (Dark Theme + Custom Font) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    .stApp {
        background: linear-gradient(180deg, #0E1117 0%, #1C1F26 100%);
        color: #FAFAFA;
        font-family: 'Poppins', sans-serif;
    }
    .header {
        font-size: 28px;
        font-weight: 700;
        color: #FFFFFF;
    }
    .sub {
        color: #B0B3B8;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Advanced Mental Health Detection from WhatsApp Chat")
st.caption("Upload an exported WhatsApp .txt to analyze emotions, trends and get AI support.")

# Sidebar
st.sidebar.header("🔧 Settings & Upload")
uploaded_file = st.sidebar.file_uploader("Upload WhatsApp chat (.txt)", type=['txt'])
use_hinglish = st.sidebar.checkbox("Translate Hinglish → English", value=True)
use_transformer = st.sidebar.checkbox("Use Transformer-based classifier (optional)", value=False)
use_openai = st.sidebar.checkbox("Enable OpenAI Chatbot (set OPENAI_API_KEY in .env)", value=False)
use_kaleido = st.sidebar.checkbox("Enable kaleido for saving figure images (optional)", value=False)
st.sidebar.markdown("---")
st.sidebar.markdown(
    "👨‍💻 Tips:\n"
    "- If `Use Transformer` causes import errors, uncheck it to use the lightweight fallback.\n"
    "- Install transformers and torch only if you have space and compatible versions."
)

# Session state
if "history" not in st.session_state:
    st.session_state.history = []  # conversation history (user, bot)

if uploaded_file:
    raw_text = uploaded_file.read().decode("utf-8")
    st.info("Processing chat...")
    df = clean_chat(raw_text)
    if use_hinglish:
        df['message'] = df['message'].apply(translate_hinglish_to_english)

    # Choose classifier
    if use_transformer:
        try:
            from transformer_emotion import predict_with_transformer
            df = predict_with_transformer(df)
            st.success("Used transformer-based emotion classifier.")
        except Exception as e:
            st.error("Transformer classifier failed to load. Falling back to lightweight classifier. Error: " + str(e))
            df = get_emotions_simple(df)
    else:
        df = get_emotions_simple(df)

    st.session_state.df = df

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📄 Data", "📈 Insights", "🤖 Chatbot", "📥 Export"])

with tab1:
    st.header("Processed Chat Data")
    if 'df' in st.session_state:
        st.dataframe(st.session_state.df[['timestamp', 'sender', 'message', 'emotion']].tail(300))
    else:
        st.info("Upload a chat file to view processed data. A sample chat is in /data/sample_chat.txt")

with tab2:
    st.header("Insights & Visualizations")
    
    if 'df' in st.session_state:
        df = st.session_state.df

        # 🔹 Standardize all column names to lowercase
        df.columns = df.columns.str.lower()

        # 🔹 Ensure Date & Emotion columns exist before plotting
        try:
            from emotion_trend import ensure_date_emotion
            df = ensure_date_emotion(df)
            st.session_state.df = df  # Save back to session state
        except ValueError as e:
            st.error(f"❌ Error preparing data for plotting: {e}")
            st.stop()

        # 🔹 Ensure required columns exist or create defaults
        if 'timestamp' not in df.columns:
            possible_date = [c for c in df.columns if 'date' in c.lower() or 'time' in c.lower()]
            if possible_date:
                df['timestamp'] = pd.to_datetime(df[possible_date[0]], errors='coerce')
            else:
                df['timestamp'] = pd.NaT

        if 'sender' not in df.columns:
            possible_sender = [c for c in df.columns if 'sender' in c.lower() or 'user' in c.lower()]
            if possible_sender:
                df['sender'] = df[possible_sender[0]]
            else:
                df['sender'] = "Unknown"

        if 'emotion' not in df.columns:
            possible_emotion = [c for c in df.columns if 'emotion' in c.lower()]
            if possible_emotion:
                df['emotion'] = df[possible_emotion[0]]
            else:
                df['emotion'] = "neutral"

        # 🔹 Metrics
        total = len(df)
        days = df['timestamp'].dt.date.nunique() if df['timestamp'].notna().any() else 0
        unique_senders = df['sender'].nunique()
        top_emotion = df['emotion'].mode().iloc[0] if not df['emotion'].mode().empty else "neutral"

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Messages", total)
        c2.metric("Active Days", days)
        c3.metric("Unique Senders", unique_senders)
        c4.metric("Top Emotion", top_emotion)

        # 🔹 Imports for visualizations
        from chat_statistics import (
            plot_emotion_distribution,
            plot_top_users,
            plot_message_heatmap_plotly,
            get_chat_stats
        )
        from advanced_visuals import (
            generate_wordcloud,
            generate_emotion_heatmap,
            generate_emotion_pie_chart
        )

        # 📊 Emotion Distribution
        st.subheader("Emotion Distribution")
        fig = plot_emotion_distribution(df)
        st.plotly_chart(fig, use_container_width=True)

        # 📊 Top Active Users
        st.subheader("Top Active Users")
        st.plotly_chart(plot_top_users(df), use_container_width=True)

        # 📊 Activity Heatmap
        st.subheader("Activity Heatmap (Day vs Hour)")
        st.plotly_chart(plot_message_heatmap_plotly(df), use_container_width=True)

        # 📊 Emotion Trend
        st.subheader("Emotion Trend Over Time")
        st.plotly_chart(plot_emotion_trend_plotly(df), use_container_width=True)
        save_emotion_trend_png(df)

        # ☁️ Wordcloud & Heatmap
        st.subheader("Wordcloud & Heatmap Images")
        wc = generate_wordcloud(df)
        st.image(wc, use_column_width=True)
        hm = generate_emotion_heatmap(df)
        st.image(hm, use_column_width=True)

    else:
        st.info("Upload a chat to see insights.")

with tab3:
    st.header("💬 AI Chatbot (Supportive) — Text & Voice")
    if 'history' not in st.session_state:
        st.session_state.history = []

    # Voice input
    st.markdown("**Voice Input** — click to record from your mic (local only).")
    if st.button("🎙️ Record & Transcribe (local)"):
        try:
            st.info("Recording... please speak (will listen up to 10s).")
            text = record_audio_to_text(timeout=5, phrase_time_limit=10)
            if text:
                st.success("Transcription: " + text)
                user_input = text
            else:
                st.warning("Could not transcribe audio.")
                user_input = ""
        except Exception as e:
            st.error(f"Recording error: {e}")
            user_input = ""
    else:
        user_input = st.text_input("How are you feeling? (type or use Voice)", key="chat_text")

    # If you used Hinglish translation option earlier, you may translate here:
    if user_input and use_hinglish:
        user_input_proc = translate_hinglish_to_english(user_input)
    else:
        user_input_proc = user_input

    if user_input_proc:
        context_emotion = None
        if 'df' in st.session_state and not st.session_state.df.empty:
            context_emotion = st.session_state.df['emotion'].mode().iloc[0]

        # Choose whether to use OpenAI (auto-enabled only if env var exists)
        openai_key = os.getenv("OPENAI_API_KEY")
        use_openai_flag = bool(openai_key)  # or let user toggle via checkbox

        try:
            reply = generate_response(user_input_proc,
                                      use_openai=use_openai_flag,
                                      emotion=context_emotion,
                                      history=st.session_state.history)
        except Exception as e:
            reply = "Sorry, chatbot unavailable: " + str(e)

        st.session_state.history.append((user_input_proc, reply))
        st.markdown(f"**Bot:** {reply}")

        # TTS: generate mp3 and play
        try:
            mp3_path = tts_gtts(reply, lang='en')
            audio_file = open(mp3_path, "rb").read()
            st.audio(audio_file, format='audio/mp3')
        except Exception as e:
            st.warning("TTS failed: " + str(e))

        intent = detect_intent(user_input_proc)
        if intent:
            st.error(f"⚠️ Detected urgent intent: {intent}")

    # show history
    if st.session_state.history:
        st.subheader("Conversation Memory (recent)")
        for u, r in st.session_state.history[::-1]:
            st.markdown(f"**You:** {u}")
            st.markdown(f"**Bot:** {r}")
with tab4:
    st.header("Export & Report")
    if 'df' in st.session_state:
        df = st.session_state.df
        st.download_button("⬇️ Download CSV", data=df.to_csv(index=False).encode('utf-8'),
                           file_name="chat_emotions.csv", mime="text/csv")
        excel_path = export_excel(df)
        with open(excel_path, "rb") as f:
            st.download_button("⬇️ Download Excel", data=f,
                               file_name="chat_emotions.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        png_zip = export_png_bundle(df)
        with open(png_zip, "rb") as f:
            st.download_button("⬇️ Download PNG Bundle (zip)", data=f,
                               file_name="chat_images.zip", mime="application/zip")
        pdf_path = generate_pdf_report(df)
        with open(pdf_path, "rb") as f:
            st.download_button("⬇️ Download PDF Report", data=f,
                               file_name="chat_report.pdf", mime="application/pdf")
    else:
        st.info("Process a chat first to enable export.")

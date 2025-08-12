# voice_utils.py
import os
import tempfile
from gtts import gTTS
import speech_recognition as sr

def tts_gtts(text, lang='en', filename=None):
    """Generate TTS mp3 using gTTS and return file path."""
    if filename is None:
        fd, filename = tempfile.mkstemp(suffix='.mp3')
        os.close(fd)
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    return filename

def record_audio_to_text(timeout=5, phrase_time_limit=10):
    """
    Record from default mic and transcribe using SpeechRecognition (Google Web Speech API).
    Returns recognized text or None.
    Note: uses internet (Google web speech). For offline STT use Whisper or VOSK.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    try:
        text = r.recognize_google(audio)  # Google Web Speech API
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        # network / API error
        raise e

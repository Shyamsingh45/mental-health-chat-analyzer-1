MAP = {
    'mujhe': 'me',
    'bhut': 'very',
    'acha': 'good',
    'nahi': 'no',
    'nhi': 'no',
    'haan': 'yes',
    'kya': 'what',
    'kyu': 'why',
    'udaas': 'sad',
    'tanha': 'alone',
    'pareshan': 'disturbed',
    'dard': 'pain',
    'madad': 'help',
    'marna': 'die'
}

def translate_hinglish_to_english(text):
    if not isinstance(text, str):
        return text
    words = text.split()
    out = [MAP.get(w.lower(), w) for w in words]
    return ' '.join(out)

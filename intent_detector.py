def detect_intent(text):
    text = text.lower()
    intents = []
    urgent = ['suicide','kill myself','end my life','want to die','help me']
    stress = ['stressed','stress','anxious','panic','overwhelmed']
    sad = ['sad','depressed','down','unhappy','lonely','hopeless']
    for w in urgent:
        if w in text:
            intents.append('urgent')
            return intents
    for w in stress:
        if w in text:
            intents.append('stressed')
            break
    for w in sad:
        if w in text:
            intents.append('sad')
            break
    return intents

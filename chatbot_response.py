# chatbot_response.py
import random

# Example supportive fallback responses
fallback_responses = [
    "I'm here for you. Tell me more about what's on your mind.",
    "It sounds like you're going through something. How can I help?",
    "I understand. Let’s take it step by step.",
    "You’re not alone in this. I’m listening.",
    "I hear you. That sounds really tough. Can you share more?",
    "It’s okay to feel this way. Let’s work through it together."
]

def generate_response(user_input, emotion=None, history=None):
    """
    Generate a chatbot response with optional emotion & conversation history.
    Works entirely offline.

    Args:
        user_input (str): The user's message.
        emotion (str): Emotion detected from analysis (optional).
        history (list): Conversation history as list of tuples (user, bot).
    """

    # Build conversation context
    conversation_context = ""
    if history:
        for u, r in history[-5:]:  # last 5 exchanges
            conversation_context += f"User: {u}\nBot: {r}\n"

    if emotion:
        conversation_context += f"(User seems to be feeling {emotion}.)\n"

    conversation_context += f"User: {user_input}\nBot:"

    # Simple offline logic — pattern based (can be extended)
    lower_input = user_input.lower()

    if any(word in lower_input for word in ["sad", "unhappy", "depressed"]):
        return "I'm really sorry you're feeling this way. What happened?"
    elif any(word in lower_input for word in ["happy", "excited", "great"]):
        return "That’s wonderful to hear! What’s making you feel so positive?"
    elif "help" in lower_input:
        return "Of course, I’m here to help. Can you tell me more about the situation?"
    
    # If no rule matches, pick a random supportive message
    return random.choice(fallback_responses)

import anthropic
import re
from config import ANTHROPIC_API_KEY, CHAT_MODEL, CHAT_MAX_TOKENS
from services import quran_api

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
SYSTEM_PROMPT = "You are an expert Islamic scholar. ONLY answer based on the provided Quran context. Never hallucinate verses."

def chat_with_ai(user_message):
    context = ""
    refs = re.findall(r'(\d+):(\d+)', user_message)
    for surah, ayah in refs:
        try: context += f"Quran {surah}:{ayah}: {quran_api.get_ayah_text(int(surah), int(ayah))}\n"
        except: pass
    if not context: context = "No specific verse found. Answer generally."
    
    response = client.messages.create(model=CHAT_MODEL, max_tokens=CHAT_MAX_TOKENS, system=SYSTEM_PROMPT, messages=[{"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_message}"}])
    return response.content[0].text

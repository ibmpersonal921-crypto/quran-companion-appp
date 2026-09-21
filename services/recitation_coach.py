import speech_recognition as sr
import difflib
import re

def normalize_arabic(text):
    """Remove diacritics and standardize Arabic characters."""
    text = re.sub(r'[ًٌٍَُِّْٰٕٖٓٔ]', '', text)
    text = text.replace('آ', 'ا').replace('ى', 'ي').replace('ة', 'ه').replace('أ', 'ا').replace('إ', 'ا')
    return text.strip()

def transcribe_audio(audio_file_path):
    """Use Google's free Speech API to transcribe Arabic audio."""
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio = recognizer.record(source)
        
        # Use Google Web Speech API (free, no key needed)
        text = recognizer.recognize_google(audio, language='ar-SA')
        return normalize_arabic(text)
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"API error: {e}"
    except Exception as e:
        return f"Error: {str(e)}"

def compare_recitation(target_text, transcribed_text):
    """Compare word-by-word and return feedback."""
    if "Could not understand" in transcribed_text or "API error" in transcribed_text or "Error:" in transcribed_text:
        return [(transcribed_text, 'wrong')]
    
    target_words = normalize_arabic(target_text).split()
    transcribed_words = transcribed_text.split()
    
    if not target_words or not transcribed_words:
        return [("No words to compare", 'missing')]
    
    matcher = difflib.SequenceMatcher(None, target_words, transcribed_words)
    feedback = []
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            for w in target_words[i1:i2]: 
                feedback.append((w, 'correct'))
        elif tag == 'replace':
            for w in target_words[i1:i2]: 
                feedback.append((w, 'wrong'))
        elif tag == 'delete':
            for w in target_words[i1:i2]: 
                feedback.append((w, 'missing'))
        elif tag == 'insert':
            for w in transcribed_words[j1:j2]: 
                feedback.append((w, 'wrong'))
            
    return feedback

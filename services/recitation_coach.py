import speech_recognition as sr
import difflib
import re
import os

def normalize_arabic(text):
    """Remove diacritics and standardize Arabic characters for fair comparison."""
    text = re.sub(r'[ًٌٍَُِّْٰٕٖٓٔ]', '', text)
    text = text.replace('آ', 'ا').replace('ى', 'ي').replace('ة', 'ه').replace('أ', 'ا').replace('إ', 'ا')
    return text.strip()

def transcribe_audio(audio_file_path):
    """Use Google's free Speech API to transcribe Arabic audio."""
    recognizer = sr.Recognizer()
    
    # Convert streamlit audio file to a format SpeechRecognition understands
    # Note: st.audio_input returns a BytesIO-like object, we might need to save it temporarily
    # For this MVP, we assume audio_file_path is a valid path or we handle the bytes.
    
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio = recognizer.record(source)
        
        # Use Google Web Speech API (free, no key needed for basic use)
        text = recognizer.recognize_google(audio, language='ar-SA')
        return normalize_arabic(text)
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"API error: {e}"
    except Exception as e:
        # Fallback if file format is tricky
        return f"Error processing file: {str(e)}"

def compare_recitation(target_text, transcribed_text):
    """Compare word-by-word and return feedback."""
    if "Could not understand" in transcribed_text or "API error" in transcribed_text:
        return [(transcribed_text, 'wrong')]
        
    target_words = normalize_arabic(target_text).split()
    transcribed_words = transcribed_text.split()
    
    matcher = difflib.SequenceMatcher(None, target_words, transcribed_words)
    feedback = []
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            for w in target_words[i1:i2]: feedback.append((w, 'correct'))
        elif tag == 'replace':
            for w in target_words[i1:i2]: feedback.append((w, 'wrong'))
        elif tag == 'delete':
            for w in target_words[i1:i2]: feedback.append((w, 'missing'))
            
    return feedback

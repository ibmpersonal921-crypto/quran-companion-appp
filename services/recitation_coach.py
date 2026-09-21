from faster_whisper import WhisperModel
import difflib
import re
from config import WHISPER_MODEL_SIZE

# Load model once at startup
model = WhisperModel(WHISPER_MODEL_SIZE, device="cpu", compute_type="int8")

def normalize_arabic(text):
    text = re.sub(r'[ًٌٍَُِّْٰٖٓٔ]', '', text)
    return text.replace('آ', 'ا').replace('ى', 'ي').replace('ة', 'ه').strip()

def transcribe_audio(audio_file_path):
    segments, info = model.transcribe(audio_file_path, language="ar")
    full_text = ""
    for segment in segments:
        full_text += segment.text + " "
    return normalize_arabic(full_text)

def compare_recitation(target_text, transcribed_text):
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

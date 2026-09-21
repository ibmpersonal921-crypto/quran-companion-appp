import requests
from config import QURAN_API_BASE, VERSE_OF_DAY_POOL
from datetime import datetime

def get_verse_of_the_day():
    today = datetime.now().timetuple().tm_yday
    surah, start, end, label = VERSE_OF_DAY_POOL[today % len(VERSE_OF_DAY_POOL)]
    arabic_res = requests.get(f"{QURAN_API_BASE}/ayah/{surah}:{start}-{end}/quran-uthmani").json()
    english_res = requests.get(f"{QURAN_API_BASE}/ayah/{surah}:{start}-{end}/en.sahih").json()
    translit_res = requests.get(f"{QURAN_API_BASE}/ayah/{surah}:{start}-{end}/en.transliteration").json()
    urdu_res = requests.get(f"{QURAN_API_BASE}/ayah/{surah}:{start}-{end}/ur.jalandhry").json()
    return {
        "label": label,
        "arabic": " ".join([a['text'] for a in arabic_res['data']]),
        "english": " ".join([e['text'] for e in english_res['data']]),
        "transliteration": " ".join([t['text'] for t in translit_res['data']]),
        "urdu": " ".join([u['text'] for u in urdu_res['data']])
    }

def get_surah_list():
    res = requests.get(f"{QURAN_API_BASE}/surah").json()
    return res['data']

def get_ayah_text(surah, ayah, edition="en.sahih"):
    res = requests.get(f"{QURAN_API_BASE}/ayah/{surah}:{ayah}/{edition}").json()
    return res['data']['text']

def get_audio_url(surah, ayah, reciter="ar.alafasy", bitrate=128):
    return f"https://cdn.islamic.network/quran/audio/{bitrate}/{reciter}/{str(surah).zfill(3)}{str(ayah).zfill(3)}.mp3"

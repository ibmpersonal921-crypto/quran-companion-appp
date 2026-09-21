from gtts import gTTS
def speak_urdu(text, output_file="feedback.mp3"):
    gTTS(text=text, lang='ur').save(output_file)
    return output_file

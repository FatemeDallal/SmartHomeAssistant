import speech_recognition as sr
import datetime


#def record_and_transcribe_long():
#    recognizer = sr.Recognizer()
#
#    with sr.Microphone() as source:
#        recognizer.adjust_for_ambient_noise(source, duration=1)
#        audio_data = recognizer.listen(source, timeout=None, phrase_time_limit=None)
#
#    try:
#        full_text = recognizer.recognize_google(audio_data, language="en-US")
#        return full_text
#    except sr.UnknownValueError:
#        return None
#    except sr.RequestError:
#        return None

#کد جدید

def speak_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data, language="en-US")
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None


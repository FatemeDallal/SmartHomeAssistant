import pyttsx3


def text_to_speech(text):
    engine = pyttsx3.init()

    engine.setProperty('rate', 150)

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    engine.save_to_file(text, r"static\audio\response.wav")

    engine.runAndWait()



import speech_recognition as sr
import datetime


def record_and_transcribe_long():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Speak clearly. Recording will automatically stop after a long pause.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("✅ Listening...")

        audio_data = recognizer.listen(source, timeout=None, phrase_time_limit=None)
        print("🔁 Processing...")

    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"long_recording_{timestamp}.wav"
        with open(filename, "wb") as f:
            f.write(audio_data.get_wav_data())
        print(f"💾 Audio saved as: {filename}")

        full_text = recognizer.recognize_google(audio_data, language="en-US")
        print("\n📝 Full Transcription:\n")
        print(full_text)

    except sr.UnknownValueError:
        print("⚠️ Sorry, I couldn't understand the speech.")
    except sr.RequestError as e:
        print(f"🚫 Could not connect to Google Speech Recognition service; {e}")


if __name__ == "__main__":
    record_and_transcribe_long()

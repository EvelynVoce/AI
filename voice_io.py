import speech_recognition as sr
import pyttsx3
from Main import main
from threading import Thread
from GUI import clear_text_box, update_text_box # Causes circular import

voice = pyttsx3.init()
rate = voice.getProperty('rate')
voice.setProperty('rate', rate+50)


def speak(text):
    voice.say(text)
    try:
        voice.runAndWait()
    except RuntimeError:
        voice.stop()


def listen(kern):
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("listening!")
        audio = r.listen(source)
        r.pause_threshold = 1

    try:
        print("recognising")
        query = r.recognize_google(audio, language="en-UK")
        print("user said: ", query, "\n")
        output: str = main(kern, query)

    except sr.UnknownValueError:
        print("I was not able to understand")
        output: str = "I was not able to understand"

    Thread(target=speak, args=(output,), daemon=True).start()
    clear_text_box()
    update_text_box(output)

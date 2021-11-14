import tkinter as tk
from tkinter import font
import aiml
from Main import main
import pyttsx3
from threading import Thread
import speech_recognition as sr

voice = pyttsx3.init()
rate = voice.getProperty('rate')
voice.setProperty('rate', rate+50)

kern = aiml.Kernel()
kern.bootstrap(learnFiles="mybot-basic.xml")

bg_col = "steelblue"
fg_col = "lightgoldenrod1"
button_col = "pink"

root = tk.Tk()  # Creates the root window
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))  # Creates a full screen window
root.title("AI")  # Sets the name of the window
root.config(bg=bg_col)  # Sets the background colour of the root windo


def underline(label):  # A reusable function where a label is passed in so it can be underlined
    f = font.Font(label, label.cget("font"))  # Creates a new font
    f.configure(underline=True)  # Underlines the new font
    label.configure(font=f)  # Applies the new underlined font to the label


def listen():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("listening!")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("recognising")
        query = r.recognize_google(audio, language="en-UK")
        print("user said: ", query, "\n")
        output: str = main(query)

    except sr.UnknownValueError:
        print("I was not able to understand")
        output: str = "I was not able to understand"

    Thread(target=speak, args=(output,), daemon=True).start()


def speak(text):
    voice.say(text)
    try:
        voice.runAndWait()
    except RuntimeError:
        voice.stop()


def check_entry(question_entry, text_box):
    text_box.config(state=tk.NORMAL)
    text_box.delete('1.0', tk.END)

    user_input = question_entry.get()
    output: str = main(user_input)
    print(output)

    Thread(target=speak, args=(output,), daemon=True).start()

    text_box.insert(tk.INSERT, output)
    text_box.config(state=tk.DISABLED)


def main_screen():
    welcoming = tk.Label(root, text="Welcome to this chat bot. Please feel free to ask questions from me!",
                         font=("arial", 30, "bold"), fg=fg_col, bg=bg_col)
    welcoming.pack(side="top")  # Outputs the label at the top of the window
    underline(welcoming)

    question_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13))
    question_entry.place(relx=0.05, rely=0.35, relwidth=0.6, relheight=0.05)

    text_box = tk.Text(root, wrap=tk.WORD, cursor="arrow", bd=8, relief=tk.GROOVE,
                       font=("arial", 20), state=tk.DISABLED)
    text_box.place(relx=0.05, rely=0.5, relwidth=0.85, relheight=0.4)

    scrollbar = tk.Scrollbar(root, command=text_box.yview)
    scrollbar.place(relx=0.89, rely=0.5, relheight=0.4)

    submit_button = tk.Button(root, text="Submit", font=("arial", 10, "bold"), bg=button_col,
                              command=lambda: check_entry(question_entry, text_box))
    submit_button.place(relx=0.70, rely=0.35, relwidth=0.2, relheight=0.05)

    listen_button = tk.Button(root, text="Voice Input", font=("arial", 10, "bold"), bg=button_col,
                              command=lambda: Thread(target=listen(), daemon=True).start())
    listen_button.place(relx=0.70, rely=0.25, relwidth=0.2, relheight=0.05)


if __name__ == "__main__":
    welcome_message = "Welcome to this chat bot. Please feel free to ask questions from me!"
    Thread(target=speak, args=(welcome_message,), daemon=True).start()
    main_screen()
    root.mainloop()

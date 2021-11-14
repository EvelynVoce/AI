import tkinter as tk
from tkinter import font
import aiml
from Main import main
from threading import Thread
import speech_recognition as sr
import pyttsx3


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
root.config(bg=bg_col)  # Sets the background colour of the root window

question_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13))
text_box = tk.Text(root, wrap=tk.WORD, cursor="arrow", bd=8, relief=tk.GROOVE, font=("arial", 20), state=tk.DISABLED)


def speak(text):
    voice.say(text)
    try:
        voice.runAndWait()
    except RuntimeError:
        voice.stop()


def listen():
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


def clear_text_box():
    text_box.config(state=tk.NORMAL)
    text_box.delete('1.0', tk.END)
    text_box.config(state=tk.DISABLED)


def update_text_box(output):
    text_box.config(state=tk.NORMAL)
    text_box.insert(tk.INSERT, output)
    text_box.config(state=tk.DISABLED)


def check_entry(event=None):
    clear_text_box()
    user_input = question_entry.get()
    output: str = main(kern, user_input)
    print(output)
    Thread(target=speak, args=(output,), daemon=True).start()
    update_text_box(output)


def underline(label):  # A reusable function where a label is passed in so it can be underlined
    f = font.Font(label, label.cget("font"))  # Creates a new font
    f.configure(underline=True)  # Underlines the new font
    label.configure(font=f)  # Applies the new underlined font to the label


def main_screen():
    root.bind('<Return>', check_entry)
    welcoming = tk.Label(root, text="Welcome to this chat bot. Please feel free to ask questions from me!",
                         font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    welcoming.place(relx=0.1, rely=0.05)
    # welcoming.pack(side="top")  # Outputs the label at the top of the window
    underline(welcoming)

    question_entry.place(relx=0.1, rely=0.35, relwidth=0.55, relheight=0.05)
    text_box.place(relx=0.1, rely=0.5, relwidth=0.80, relheight=0.4)

    scrollbar = tk.Scrollbar(root, command=text_box.yview)
    scrollbar.place(relx=0.89, rely=0.5, relheight=0.4)

    submit_button = tk.Button(root, text="Submit", font=("arial", 10, "bold"), bg=button_col,
                              command=lambda: check_entry())
    submit_button.place(relx=0.66, rely=0.35, relwidth=0.12, relheight=0.05)

    listen_button = tk.Button(root, text="Voice Input", font=("arial", 10, "bold"), bg=button_col,
                              command=lambda: Thread(target=listen, daemon=True).start())
    listen_button.place(relx=0.78, rely=0.35, relwidth=0.12, relheight=0.05)


if __name__ == "__main__":
    welcome_message = "Welcome to this chat bot. Please feel free to ask questions from me!"
    Thread(target=speak, args=(welcome_message,), daemon=True).start()
    main_screen()
    root.mainloop()

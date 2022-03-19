import tkinter as tk
from tkinter import font
import aiml
from threading import Thread
import speech_recognition as sr
import pyttsx3
from AI_flow import get_ai_response
from fuzzy import fuzzy_logic
from cognitive_azure import get_description
from tkinter.filedialog import askopenfilename
from custom_vision import classify_image_azure
from CNN_implemented import classify_image
from face_service import face_recognition

voice = pyttsx3.init()
rate = voice.getProperty('rate')
voice.setProperty('rate', rate+50)

kern = aiml.Kernel()
kern.bootstrap(learnFiles="mybot-basic.xml")

bg_col: str = "steelblue"
fg_col: str = "lightgoldenrod1"
button_col: str = "pink"

root = tk.Tk()  # Create root window
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))  # Create full screen window
root.title("AI")  # Sets the name of the window
root.config(bg=bg_col)  # Sets the background colour of the root window

question_entry = tk.Entry()
text_box = tk.Text()
rating_label = tk.Label()


def globalise():
    # This function is needed for back buttons to work
    global question_entry
    question_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13))
    global text_box
    text_box = tk.Text(root, wrap=tk.WORD, cursor="arrow", bd=8, relief=tk.GROOVE, font=("arial", 20), state=tk.DISABLED)
    global rating_label
    rating_label = tk.Label(root, text="Overall rating: 0", font=("arial", 25, "bold"), fg=fg_col, bg=bg_col)


def clear_root():
    for ele in root.winfo_children():
        ele.destroy()


def speak(text):
    print(text)
    voice.say(text)
    try:
        voice.runAndWait()
    except RuntimeError:
        voice.stop()


def listen():
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    with mic as source:
        audio = r.listen(source)
        r.pause_threshold = 1

    try:
        query: str = r.recognize_google(audio, language="en-UK")
        print("AI heard:", query)
        output: str = get_ai_response(kern, query)

    except sr.UnknownValueError:
        output: str = "I was not able to understand"

    Thread(target=speak, args=(output,), daemon=True).start()
    clear_text_box()
    update_text_box(output)


def clear_text_box():
    text_box.config(state=tk.NORMAL)
    text_box.delete('1.0', tk.END)


def update_text_box(output):
    text_box.insert(tk.INSERT, output)
    text_box.config(state=tk.DISABLED)


def check_entry(event=None):
    clear_text_box()
    user_input = question_entry.get()
    output: str = get_ai_response(kern, user_input)
    if not output == "Fuzzy Logic":
        Thread(target=speak, args=(output,), daemon=True).start()
        update_text_box(output)
    else:
        fuzzy_gui()


def underline(label):  # A reusable function where a label is passed in, so it can be underlined
    f = font.Font(label, label.cget("font"))  # Creates a new font
    f.configure(underline=True)  # Underlines the new font
    label.configure(font=f)  # Applies the new underlined font to the label


def main_screen():
    globalise()
    intro_message: str = "Welcome to this chat bot. Please feel free to ask questions from me!"
    root.bind('<Return>', check_entry)
    welcoming = tk.Label(root, text=intro_message,
                         font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    welcoming.place(relx=0.1, rely=0.05)
    underline(welcoming)

    global question_entry
    question_entry.place(relx=0.1, rely=0.35, relwidth=0.45, relheight=0.05)
    text_box.place(relx=0.1, rely=0.5, relwidth=0.80, relheight=0.4)

    scrollbar = tk.Scrollbar(root, command=text_box.yview)
    scrollbar.place(relx=0.89, rely=0.5, relheight=0.4)

    submit_button = tk.Button(root, text="Submit", font=("arial", 10, "bold"),
                              bg=button_col, command=lambda: check_entry())
    submit_button.place(relx=0.56, rely=0.35, relwidth=0.10, relheight=0.05)

    listen_button = tk.Button(root, text="Voice Input", font=("arial", 10, "bold"), bg=button_col,
                              command=lambda: Thread(target=listen, daemon=True).start())
    listen_button.place(relx=0.68, rely=0.35, relwidth=0.10, relheight=0.05)

    image_entry_button = tk.Button(root, text="Image detection", font=("arial", 10, "bold"), bg=button_col,
                                   command=lambda: describe_image())
    image_entry_button.place(relx=0.80, rely=0.35, relwidth=0.10, relheight=0.05)


def get_rating(writing_score: int, acting_score: int, impact_score: int):
    overall_rating: int = fuzzy_logic(writing_score, acting_score, impact_score)
    rating_label.config(text=f"Overall rating: {overall_rating}")
    Thread(target=speak, args=(overall_rating,), daemon=True).start()


def fuzzy_gui():
    clear_root()
    login_title = tk.Label(root, text=welcome_message, font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    login_title.place(relx=0.50, rely=0.05, anchor=tk.CENTER)
    underline(login_title)

    back_button = tk.Button(root, text="back", font=("arial", 10, "bold"), bg=button_col,
                            command=lambda: clear_root() or main_screen())
    back_button.place(relx=0.75, rely=0.025, relwidth=0.2, relheight=0.05)

    writing_label = tk.Label(root, text="Writing:", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    writing_label.place(relx=0.20, rely=0.35)

    acting_label = tk.Label(root, text="Acting:", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    acting_label.place(relx=0.20, rely=0.45)

    impact_label = tk.Label(root, text="Impact:", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    impact_label.place(relx=0.20, rely=0.55)

    writing_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13))
    writing_entry.place(relx=0.30, rely=0.35, relwidth=0.5, relheight=0.05)

    acting_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13))
    acting_entry.place(relx=0.30, rely=0.45, relwidth=0.5, relheight=0.05)

    impact_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13))
    impact_entry.place(relx=0.30, rely=0.55, relwidth=0.5, relheight=0.05)

    fuzzy_submission = tk.Button(root, text="Get overall rating", font=("arial", 10, "bold"),
                                 bg=button_col, command=lambda:
                                 get_rating(int(writing_entry.get()), int(acting_entry.get()),
                                            int(impact_entry.get())))
    fuzzy_submission.place(relx=0.20, rely=0.65, relwidth=0.28, relheight=0.1)

    global rating_label
    rating_label = tk.Label(root, text="Overall rating: 0", font=("arial", 25, "bold"), fg=fg_col, bg=bg_col)
    rating_label.place(relx=0.6, rely=0.65)


def update_image_details():
    filename = askopenfilename()
    Thread(target=face_recognition, args=(filename,), daemon=True).start()
    classification_azure: str = classify_image_azure(filename)
    classification_local: str = classify_image(filename)
    description: str = get_description(filename)

    caption_text: str = f"Azure classified as {classification_azure}.\n" \
                        f"Locally classified as {classification_local}.\n" \
                        f"Description: {description}"

    Thread(target=speak, args=(caption_text,), daemon=True).start()
    clear_text_box()
    update_text_box(caption_text)


def describe_image():
    clear_root()
    description_title = tk.Label(root, text="Image description", font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    description_title.place(relx=0.50, rely=0.05, anchor=tk.CENTER)
    underline(description_title)

    new_image_button = tk.Button(root, text="Select Image", font=("arial", 10, "bold"), bg=button_col,
                                 command=update_image_details)
    new_image_button.place(relx=0.69, rely=0.025, relwidth=0.1, relheight=0.05)


    back_button = tk.Button(root, text="back", font=("arial", 10, "bold"), bg=button_col,
                            command=lambda: clear_root() or main_screen())
    back_button.place(relx=0.80, rely=0.025, relwidth=0.1, relheight=0.05)

    global text_box
    text_box = tk.Text(root, wrap=tk.WORD, cursor="arrow", bd=8,
                       relief=tk.GROOVE, font=("arial", 20), state=tk.DISABLED)
    text_box.place(relx=0.1, rely=0.5, relwidth=0.80, relheight=0.4)
    update_image_details()




if __name__ == "__main__":
    welcome_message = "Welcome to this chat bot. Please feel free to ask questions from me!"
    Thread(target=speak, args=(welcome_message,), daemon=True).start()
    main_screen()
    root.mainloop()

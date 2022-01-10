from wikipedia import summary, exceptions
from similarity import get_similar
import nltk
from pyjokes import get_joke
from pandas import read_csv

from nltk.sem import Expression
from nltk.inference import ResolutionProver

read_expr = Expression.fromstring
data = read_csv('kb.csv', header=None)
kb: list = [read_expr(row.lower()) for row in data[0]]

# Checking KB integrity (no contradiction), otherwise show an error message and terminate
for knowledge in kb:
    if not ResolutionProver().prove(knowledge, kb, verbose=True):
        print("ERROR: CONTRADICTION FOUND")
        quit()

user_name: str = ""


def extract_name(user_input: str) -> str:
    for sent in nltk.sent_tokenize(user_input):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                return ' '.join(c[0] for c in chunk.leaves())


def get_ai_response(kern, user_input: str) -> str:
    if user_input == "":
        return

    answer: str = kern.respond(user_input.lower())
    # Kernel recognises input and responds appropriately
    if answer[0] != '#':
        return answer

    cmd, output = answer[1:].split('$')
    if cmd == '0':  # Bye command
        return output

    elif cmd == '1':  # Wikipedia command
        try:
            output = summary(output, sentences=2, auto_suggest=False)
        except exceptions.PageError or exceptions.DisambiguationError:
            output = "Sorry, I do not know that. Be more specific!"

    elif cmd == '3':  # Memory triggers
        if "my name is" in user_input.lower():  # Extract name
            global user_name
            user_name = extract_name(user_input)
            print(user_name)
            if user_name is None:
                user_name = ""

    elif cmd == '4':  # Memory retrieval
        if "my name" in user_input.lower():
            return user_name if user_name != "" else "I do not know your name"

    elif cmd == "5":  # Random joke
        output = get_joke(language="en", category="neutral")

    elif cmd == "31":  # I know that x is y
        object1, object2 = output.split(' is ')
        expr = read_expr(object2 + '(' + object1 + ')')
        # Make sure expr does not contradict
        # with the KB before appending, otherwise show an error message.

        answer = ResolutionProver().prove(expr, kb, verbose=True)
        if not answer:
            print("Wait one second")

            expr2 = read_expr("-" + object2 + '(' + object1 + ')')
            proven = ResolutionProver().prove(expr2, kb, verbose=True)
            if proven:
                return "ERROR: CONTRADICTION FOUND"

        kb.append(expr)
        return f"OK, I will remember that {object1} is {object2}"

    elif cmd == "32":  # Check that x is y
        object1, object2 = output.split(' is ')
        expr = read_expr(object2 + '(' + object1 + ')')
        answer = ResolutionProver().prove(expr, kb, verbose=True)
        if answer:
            return f"I know that {object1} is {object2}"
        else:
            expr = read_expr("-" + object2 + '(' + object1 + ')')
            proven = ResolutionProver().prove(expr, kb, verbose=True)
            return "That is false"if proven else "I am unable to confirm that statement"

    elif cmd == "33":  # Fuzzy logic test
        return "Fuzzy Logic"

    elif cmd == '99':  # Default command
        output = get_similar(user_input)
    return output

# WEATHER


# elif cmd == '2':  # Weather command: Test if this works!
#     api_key: str = "5403a1e0442ce1dd18cb1bf7c40e776f"
#     api_url: str = r"http://api.openweathermap.org/data/2.5/weather?q="
#     response = get(api_url + output + r"&units=metric&APPID=" + api_key)
#     response_json = loads(response.content)
#     if response.status_code == 200 and response_json:
#         t = response_json['main']['temp']
#         tmi = response_json['main']['temp_min']
#         tma = response_json['main']['temp_max']
#         hum = response_json['main']['humidity']
#         wsp = response_json['wind']['speed']
#         conditions = response_json['weather'][0]['description']
#         print("The temperature is", t, "°C, varying between", tmi, "and", tma,
#               "at the moment, humidity is", hum, "%, wind speed ", wsp, "m/s,", conditions)
#     else:
#         print("Sorry, I could not resolve the location you gave me.")









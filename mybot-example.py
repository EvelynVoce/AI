import speech_recognition as sr


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

    except sr.UnknownValueError:
        return "I was not able to understand"

    return query


listen()


# import wikipedia
# import json, requests
# import aiml
# #insert your personal OpenWeathermap API key here if you have one, and want to use this feature
# APIkey = "5403a1e0442ce1dd18cb1bf7c40e776f"
# kern = aiml.Kernel()
# kern.setTextEncoding(None)
# kern.bootstrap(learnFiles="mybot-basic.xml")
# print("Welcome to this chat bot. Please feel free to ask questions from me!")
# while True:
#     try:
#         userInput = input("> ")
#     except (KeyboardInterrupt, EOFError) as e:
#         print("Bye!")
#         break
#     answer = kern.respond(userInput)
#     print(answer)
#     if answer[0] == '#':
#         params = answer[1:].split('$')
#         cmd = int(params[0])
#         if cmd == 0:
#             print(params[1])
#             break
#         elif cmd == 1:
#             try:
#                 wSummary = wikipedia.summary(params[1], sentences=3,auto_suggest=False)
#                 print(wSummary)
#             except:
#                 print("Sorry, I do not know that. Be more specific!")
#         elif cmd == 2:
#             succeeded = False
#             api_url = r"http://api.openweathermap.org/data/2.5/weather?q="
#             response = requests.get(api_url + params[1] + r"&units=metric&APPID="+APIkey)
#             if response.status_code == 200:
#                 response_json = json.loads(response.content)
#                 if response_json:
#                     t = response_json['main']['temp']
#                     tmi = response_json['main']['temp_min']
#                     tma = response_json['main']['temp_max']
#                     hum = response_json['main']['humidity']
#                     wsp = response_json['wind']['speed']
#                     wdir = response_json['wind']['deg']
#                     conditions = response_json['weather'][0]['description']
#                     print("The temperature is", t, "°C, varying between", tmi, "and", tma, "at the moment, humidity is", hum, "%, wind speed ", wsp, "m/s,", conditions)
#                     succeeded = True
#             if not succeeded:
#                 print("Sorry, I could not resolve the location you gave me.")
#         elif cmd == 99:
#             print("I did not get that, please try again.")
#     else:
#         print(answer)

import pyttsx3  #Text to Speech (pip install pyttsx3)
import datetime  #allows access to current date and time...
import speech_recognition as sr


engine = pyttsx3.init()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")  #format: Hour:Minutes:Seconds
    speak(Time)


def date():
    year = str(datetime.datetime.now().year)  #type case into int to return the year into an integer format
    month = str(datetime.datetime.now().month)
    day = str(datetime.datetime.now().date().day)
    speak(day)
    speak(month)
    speak(year)

def greetMe():
    speak("Welcome back Sir!!")
    speak("The current time is :")
    time()
    speak("The current date is :")
    date()
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak("Good Morning, Sir!!")
    elif 12 <= hour < 18:
        speak("Good Afternoon, Sir")
    elif hour >= 18 and hour < 24:  # can be simplified as the other elif statements testing the hour of the day.
        speak("Good Evening, Sir!")
    else:
        speak("Good Night, Sir!")
    speak("Jarvis at your service, How can I help you??")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.......")
        r.pause_threshold = 1  # waits for one second then listen for audio
        audio = r.listen(source) #the words listened by the microphone thats spoken into the microphone (the source) is place into the audio variable.
        print("Done listening...")
    try:
            print("Recognizing.......")
            query = r.recognize_google(audio)
            print(f"User said: {query}\n")
    except Exception as e:
            print(e)
            print("Say that again please...")
            return "None"
    return query

takeCommand()

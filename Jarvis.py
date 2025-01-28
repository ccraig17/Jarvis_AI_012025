import pyttsx3 #Text to Speech (pip install pyttsx3)
import datetime  #allows access to current date and time...
import speech_recognition as sr
import pyaudio
import wikipedia #pip install wikipedia
import smtplib # used to send email (using Jarvis)
import webbrowser as wb
import os #used to have access to the Mac Operating System

from wikipedia import languages

engine = pyttsx3.init()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def time():
    current_time = datetime.datetime.now().strftime("%I:%M:%S")  #format: Hour:Minutes:Seconds
    speak(current_time)


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
    elif 18 <= hour < 24:  # can be simplified as the other elif statements testing the hour of the day.
        speak("Good Evening, Sir!")
    else:
        speak("Good Night, Sir!")
    speak("Jarvis at your service, How can I help you??")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source: #means with the sr.Microphone() use it in the function as the "source" variable.
        print("Listening.......")
        r.pause_threshold = 3  # waits for one second then listen for audio
        audio = r.listen(source) #the words listened by the microphone that's spoken into the microphone (the source) is place into the audio variable.
        print("Done listening.......")
    try:
        print("Recognizing.......")
        query = r.recognize_google(audio, language="en-us") # Requires PyAudio; ensure it's installed or use an alternative.
        print(f"User said: {query}\n")
    except Exception as issue:
        print(issue)
        print("Say that again please.......")
        return "None"
    return query

def sendEmail(send_to, message):
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.login("colino.craig@gmail.com", "<password>", initial_response_ok=True) #use my password here when PyAudio is working for the Microphone
    server.sendmail("colino.craig@gmail.com", send_to, message)
    server.close()


#takeCommand()

#This is the main function; its call First when the programme is run in order to initiate "Jarvis"
#All the functions/methods are create above and passed into the Main Function in order to be executed.
if __name__ == "__main__":
    greetMe()
    while True:
        query = takeCommand().lower()
        if "time" in query:
            time()
        elif "date" in query:
            date()
        elif "wikipedia" in query:
            speak("Searching Wikipedia.......")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2) #"sentences=2" returns first 2 sentences of the search
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif "send email" in query:
            try:
                speak("What should I say in the email?")
                content = takeCommand()
                to = "colino.craig@gmail.com"
                sendEmail(to, content) #sendEmail() from smtp_lib import library
                speak("Email has been sent!")
                speak("The content sent was: " + content)
            except Exception as e:
                print(e)
                speak("Sorry Sir!! Unable to send this email.")
        elif "search in chrome" in query: #used import web_browser as wb
            speak("What should I search for?")
            chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            search = takeCommand().lower()
            wb.get(chrome_path).open_new_tab(search+".com")
        #below are commands to logout, shutdown and restart the computer/system
        elif "logout" in query:
            os.system("shutdown -1")
        elif "shutdown" in query:
            os.system("shutdown /s/t 1")
        elif "restart" in query:
            os.system("shutdown /r/t 1")
        elif "play songs" in query:
            songs_dir = "C:\\Users\\colin\\Music\\songs" #add the directory of my music files on this computer
            songs = os.listdir(songs_dir) # this give the LIST of the songs in my Music Directory
            os.startfile(os.path.join(songs_dir, songs[0])) # plays/start the first song in the LIST
        elif "goodbye" in query or "bye" in query:
            speak("Goodbye Sir!!")
        elif "go offline" in query:
            speak("Going offline Sir!!")
            quit()




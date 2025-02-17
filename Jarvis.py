import datetime  # allows access to current date and time...
import os  # used to have access to the Mac Operating System
import smtplib  # used to send email (using Jarvis)
import webbrowser as wb
import pyttsx3  # Text to Speech (pip install pyttsx3)
import speech_recognition as sr
import wikipedia  # pip install wikipedia
from PIL import ImageGrab
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

engine = pyttsx3.init() #initialize the Python text to Speech (pyttsx3) and place it into a variable to be used


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
        r.adjust_for_ambient_noise(source, duration=0.2)  # adjust
        r.pause_threshold = 1  # waits for one second then listen for audio
        audio = r.listen(source) #the words listened by the microphone that's spoken into the microphone, the spoken word is place into the audio variable.
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

email_list = {
    #make keys lowercase for comparing and ensure the dictionary keys are stored in lowercase
        "james": "colino.craig@gmail.com",
        "nola": "nnoollaa79@gmail.com",
        "ethan": "shinobiroblox244@gmail.com"
    }

"""def sendEmail(recipient_name, subject="test", content="this is the new 'send email' function from python!"):
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.login("colino.craig@gmail.com", "fwev yhkz qpbx iggt") #use my App password for gmail
    #server.sendmail("colino.craig@gmail.com", to, message)

    message = MIMEMultipart("This is a Test email sent using Python and Speech Recognition")
    message["From"] = "colino.craig@gmail.com"
    message["To"] = recipient_name
    message["Subject"] = "This is a Test email sent using Python and Speech Recognition"
    message.attach(message)
    try:
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("colino.craig@gmail.com", "fwev yhkz qpbx iggt")
        server.sendmail("colino.craig@gmail.com", recipient_name, message.as_string())
        server.quit()
        print(f"Email sent to {recipient_name}!!")
    except Exception as mistake:
        print(f"An error occurred while sending the email: {mistake}")
    server.close()"""

def sendEmail2(to_email, subject, content):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "colino.craig@gmail.com"
    password = "fwev yhkz qpbx iggt"
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(content, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}!!")
    except Exception as error:
        print(f"An error occurred while sending the email: {error}")
        speak("Sorry Sir!! Unable to send this email.")

def takeScreenshot(name):
    try:
        img = ImageGrab.grab()
        save_path = f"/Users/ccraig/Desktop/Jarvis_Folder/{name}.png"
        if not os.path.exists("/Users/ccraig/Desktop/Jarvis_Folder/"):
            os.makedirs("/Users/ccraig/Desktop/Jarvis_Folder/")
        img.save(save_path)
    except Exception as e:
        print(f"An error occurred while capturing the screenshot: {e}")
        speak("Sorry Sir, the was an issue capturing the screenshot.")


#sendEmail("colin", subject="test", content="this is the new 'send email' function from python!")
#send_Email("colin", content="this is the new 'send email' function from python!")
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
            try:
                results = wikipedia.summary(query, sentences=2) #"sentences=2" returns first 2 sentences of the search
                speak("According to Wikipedia....")
                print(results)
                speak(results)
            except wikipedia.exceptions.PageError:
                speak(f"Sorry Sir!! I can't find any results for {query}. Please try a different query.")
            except wikipedia.exceptions.DisambiguationError as error:
                speak("The query is too ambiguous. Here are some possible suggestions:")
                for option in error.options:
                    print(option)
                    speak(option)
            except Exception as e:
                speak("Sorry Sir! An error occurred while searching Wikipedia.")
                print(f"Error:{e}")

        elif "send email" in query:
            speak("Who should I send the email to?")
            recipient_name = takeCommand().lower()

            if recipient_name and recipient_name in email_list:
                to_email = email_list[recipient_name]

                speak("What should be the subject of the email?")
                subject = takeCommand()
                if not subject:
                    speak("Subject NOT recognized. Exiting.")
                    continue
                speak("What would you like the to say in the email?")
                content = takeCommand()
                if not content:
                    speak("Message not recognized. Exiting.")
                    continue
                sendEmail2(to_email, subject, content)
            else:
                speak("Sorry Sir, Name not Found in your EMAIL List. Please try again or add the name to the EMAIL List.")

            
        elif "search in chrome" in query: #used import web_browser as wb
            speak("What should I search?")
            chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            wb.register("chrome", None, wb.BackgroundBrowser(chrome_path))
            search = takeCommand().lower()
            wb.get("chrome").open_new_tab(search+".com")
        elif "screenshot" in query:
            name = takeCommand()
            takeScreenshot(name)
            speak("Screenshot taken!")

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
        elif "Go offline" in query:
            speak("Going offline Sir!!")
            quit()





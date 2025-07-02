#These are the packages that are installed for building this virtual desktop assistant
import datetime
import pyttsx3
import speech_recognition as sr
import random
import webbrowser
from plyer import notification
import pyautogui
import wikipedia
import pywhatkit as pwk
import requests
import mtranslate
import os
import user_config
import gemini_text_gen


# Initialize text-to-speech engine and configure voice properties
engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
engine.setProperty("rate",170)

# Function to make the AI speak a given text
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to recognize and process voice commands
def command():
    content = " "
    while content==" ":
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
            try:
                content=r.recognize_google(audio,language='en-in')
                new_content=mtranslate.translate(content,to_language='en-in')
                print("You said......  ", new_content)
            except Exception as e:
                print("Please try again....")
    return content

# Main function to process various voice commands
def main_process():
    while True:
        request = command().lower()
        if "hello" in request:
            speak("Yes welcome, I am jarvis AI and how may I help you?")
        elif "thanks" in request:
            speak("Welcome, its my pleasure to help you")
        elif "play music" in request:# Play random music from predefined YouTube links
            speak("Playing music")
            song=random.randint(1,3)
            if song==1:
                webbrowser.open("https://www.youtube.com/watch?v=JGwWNGJdvx8")
            elif song==2:
                webbrowser.open("https://www.youtube.com/watch?v=UtF6Jej8yb4")
            elif song==3:
                webbrowser.open("https://www.youtube.com/watch?v=yIzCBU0_LyY")
        elif "say time" in request:# Speak current time
            now_time = datetime.datetime.now().strftime("%H:%M ")
            speak("Now the time is " + str(now_time))
        elif "say date" in request:#speak current date
            now_date = datetime.datetime.now().strftime("%d:%m ")
            speak("Today's date is " + str(now_date))
        elif "new task" in request:# Add a new task to the to-do list
            task=request.replace("new task","")
            task=task.strip()
            if task!="":
                speak("Adding task : "+task)
                with open("Todolist.txt", "a") as file:
                    file.write(task+"\n")
        elif "speak task" in request:# Speak the tasks from the to-do list
            with open("Todolist.txt", "r") as file:
                speak("Work we have to do today is: "+file.read())
        elif "show work" in request: # Show work tasks as a desktop notification
            with open("Todolist.txt", "r") as file:
                tasks=file.read()
            notification.notify(
                title="Today's work ",
                message=tasks
            )
        # Open common websites
        elif "open youtube" in request:
            webbrowser.open("www.youtube.com")
        elif "open google chrome" in request:
            webbrowser.open("www.google.com")
        elif "open" in request: # Open applications using system search
            query=request.replace("open","")
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")
        elif "search wikipedia" in request:
            request= request.replace("jarvis", "")
            request = request.replace("search wikipedia", "")
            print("Your search request: "+request)
            result=wikipedia.summary(request,sentences=3)
            print(result)
            speak(result)
        elif "search wikipedia" in request: # Search Wikipedia for a given query
            request= request.replace("jarvis", "")
            request = request.replace("search wikipedia about", "")
            print("Your search request on Wikipedia: "+request)
            result=wikipedia.summary(request,sentences=3)
            print(result)
            speak(result)
        elif "search google" in request: # Search Google
            request=request.replace("jarvis","")
            request=request.replace("search google about","")
            print("Your search request on Google: " + request)
            webbrowser.open("https://www.google.com/search?q="+request)
        elif "search youtube" in request:#search YouTube
            request=request.replace("jarvis","")
            request=request.replace("search youtube about","")
            print("Your search request on YouTube: " + request)
            webbrowser.open("https://www.youtube.com/results?search_query="+request)
        elif "send whatsapp" in request: # Send a WhatsApp message
            speak("Please say the recipient's phone number, digit by digit.")
            number = ""
            number = command()
            speak("Now say the message you want to send.")
            message = command()

            speak("Please say the hour in 24-hour format.")
            hrs = int(command())
            speak("Please say the minutes.")
            minutes = int(command())

            speak("Sending the WhatsApp message...")
            pwk.sendwhatmsg("+91" + number, message, hrs, minutes, 30)
            speak("WhatsApp message sent successfully!")
        elif "send email" in request:# Send an email
            speak("Please say the recipient's email ID, letter by letter.")
            email_id = ""
            new_id = ''
            email_id = command()
            for char in email_id:
                if char != ' ':
                    new_id += char
            speak("Now say the subject of the email.")
            subject = command()

            speak("Now say the message you want to send.")
            msg = command()

            speak("Sending email...")
            pwk.send_mail("pritamsaha102005@gmail.com", user_config.gmail_password, subject, msg, new_id.lower()+'@gmail.com')
            speak("Email sent successfully!")
        elif "shutdown system" in request: # Shut down the system
            speak("Are you sure you want to shut down?Type in yes or no please")
            shutdown=input("Do you wish to shutdown your computer?")
            if shutdown == "yes":
                os.system("shutdown /s /t 1")
            elif shutdown == "no":
                break
        elif "speak news" in request:# Read and speak news headlines
            speak("Fetching today's news headlines")
            r=requests.get(f"https://newsapi.org/v2/everything?q=tesla&from=2025-01-14&sortBy=publishedAt&apiKey={user_config.newsapi}")
            if r.status_code == 200:
                # If the request is successful, extract the news articles
                data = r.json()
                articles = data.get('articles', [])
                # Read out the news headlines
                for article in articles:
                    speak(article['title'])
            else:
                pass  # If the command is not recognized
        elif "ask ai" in request:# Ask AI (Gemini API request)
            request = request.replace("jarvis", "")
            request = request.replace("ask ai", "")
            print(request)
            response=gemini_text_gen.send_request(request)
            print(response)
            speak(response)
        elif "stop jarvis" in request:# Stop the AI
            speak("Ok master Goodbye, if you need any further help, please call me up")
            exit()
        else:
            request = request.replace("jarvis", "")
            print(request)
            response = gemini_text_gen.send_request(request)
            print(response)
            speak(response)

# Start the voice assistant
main_process()
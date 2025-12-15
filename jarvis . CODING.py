# jarvis.py
import os
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import smtplib

# --- Config (edit these) ---
MUSIC_DIR = r"H:\Music\Chris Brown"   # change to your music folder
CODE_PATH = r"C:\Users\ACT\AppData\Local\Programs\Microsoft VS Code\Code.exe"
EMAIL_ADDR = os.environ.get("JARVIS_EMAIL")  # set via environment variable
EMAIL_APP_PASS = os.environ.get("JARVIS_APP_PASS")  # set via environment variable
# --------------------------

# TTS init
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning sir. How are you doing?")
    elif 12 <= hour < 18:
        speak("Good afternoon sir. How are you doing?")
    else:
        speak("Good evening sir. How are you doing?")
    speak("I am JARVIS. Tell me sir how can I help you?")

def take_commands():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()
    except sr.WaitTimeoutError:
        print("Microphone timed out, switching to text input.")
        return input("Type your command: ").lower()
    except Exception as e:
        print("Could not understand audio, please type the command. (Err:", e, ")")
        return input("Type your command: ").lower()

def send_email(to, content):
    if not EMAIL_ADDR or not EMAIL_APP_PASS:
        raise RuntimeError("Email credentials not set in environment variables.")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(EMAIL_ADDR, EMAIL_APP_PASS)
    server.sendmail(EMAIL_ADDR, to, content)
    server.quit()

if __name__ == "__main__":
    wish_me()
    while True:
        query = take_commands()
        if not query:
            continue

        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            q = query.replace("wikipedia", "").strip()
            try:
                results = wikipedia.summary(q, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                speak("Sorry, I couldn't find that on Wikipedia.")
                print(e)

        elif 'youtube' in query or 'watch' in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif 'google' in query or 'search' in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif 'github' in query:
            speak("Opening Github")
            webbrowser.open("https://github.com")

        elif 'stackoverflow' in query or 'overflow' in query:
            speak("Opening Stack Overflow")
            webbrowser.open("https://stackoverflow.com")

        elif 'music' in query or 'play' in query:
            try:
                songs = os.listdir(MUSIC_DIR)
                if songs:
                    speak("Playing music")
                    os.startfile(os.path.join(MUSIC_DIR, songs[0]))
                else:
                    speak("Music folder is empty.")
            except Exception as e:
                speak("Couldn't play music. Check music directory.")
                print(e)

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query or 'visual' in query:
            speak("Opening Visual Studio Code")
            os.startfile(CODE_PATH)

        elif 'email' in query:
            try:
                speak("What should I say?")
                content = take_commands()
                speak("Who is the recipient? Please type the recipient email.")
                to = input("Recipient email: ").strip()
                send_email(to, content)
                speak("Email has been sent.")
            except Exception as e:
                print(e)
                speak("Sorry sir, I couldn't send the email.")

        elif 'exit' in query or 'get lost' in query or 'bye' in query:
            speak("Ok sir. I am always here for you. Bye.")
            break

        else:
            speak("I did not understand that. Please try again.")

import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import datetime
import os
import sys
import socket
# import urllib
# from urllib.request import urlopen
#You also need to have pocketSphinx in your machine, it helps in recognizing voice in offline mode, which also not efficient.


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')


engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def internet_check():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("www.google.com", 80))
        s.close()
        return True
    except Exception as e:
        print("Offline: Error: ", e)
        speak("You are Offline....Switching Offline Mode.")
        return False


def greet():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour<12:
        speak("Good Morning Sir, May I help You?")
    
    if hour > 12 and hour<24:
        speak("Good Evening Sir, May I help You?")

    else:
        speak("Holy MOly Lets Enjoy! I am buddy.")

def take_command():
    """
    This function takes the microphone input recognises it and returns the output as a string
    """

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening To Your Querry....")
        r.pause_threshold = 1                   #Threshold is pretty much important You can Change certain thresholds, check the threshold in active state
        audio = r.listen(source)
    try:
        print("Recognizing....")
        if internet_check():
            query = r.recognize_google(audio, language='en-in')
        else:
            query = r.recognize_sphinx(audio, language='en-in')
        print(query)
    
    except Exception as e:
        speak("what did you said")
        print(e)
        return "None"
    
    return query


if __name__ == "__main__":
    greet()

    while True:
        query = take_command().lower()
        if 'wikipedia' in query:
            print("Searching in wikipedia..")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=4)
            print(results)
            speak(f'According To Wikipedia {results}')
            
        elif 'open Youtube' in query:
            webbrowser.open("youtube.com")

        elif 'play music' in query:
            music_dir = "A:/music/Music"
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[1]))

        elif 'stop' in query or 'quit' in query:
            speak("Stoping The Servers, Goodnight Sir")
            sys.exit()
        else:
            speak("I wasnt able to recognise that..")

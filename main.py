import os
import subprocess
import time
import webbrowser
from pathlib import Path

import requests
import speech_recognition as sr
from dotenv import load_dotenv
from google import genai

import musicLibrary

# config.env ko import kar (isi folder se)
load_dotenv(Path(__file__).parent / "config.env")

newsapi = os.getenv("NEWS_API_KEY")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

recognizer = sr.Recognizer() #this recognizer object will recognize whenever speak

def speak(text):
    # # This function is used to convert the given text into speech (Text-to-Speech).
    # # engine.say(text) adds the given text to the speech queue.
    # engine.say(text)

    # # engine.runAndWait() processes the speech queue and waits until
    # # the text has been completely spoken before moving to the next instruction.
    # engine.runAndWait()
    subprocess.run(["say", "-v", "Samantha", text])

def aiProcess(command):
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=command,
                config={"system_instruction": "You are Friday, a virtual assistant. Answer in 1-2 short sentences."},
            )
            return response.text
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                time.sleep(2)
    return "Sorry sir, the AI server is busy right now"



def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif c.lower().startswith("play"):
        song = c.lower().replace("play", "", 1).strip()
        if song in musicLibrary.music:
            webbrowser.open(musicLibrary.music[song])
        else:
            speak("Song not found")

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            # JSON response parse kar
            data = r.json()

            # articles nikal
            articles = data.get("articles", [])

            # headlines bol
            for article in articles[:5]:
                print(article["title"])
                speak(article["title"])
        else:
            print(f"News API error: {r.status_code}")
            speak("Sorry sir, could not fetch the news")

    else:
        output = aiProcess(c)
        print(output)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Friday.....")
    speak("Hello Sir")
    while True:
        #Listen for the wake word "Friday"
        # obtain audio from the microphone
        r = sr.Recognizer()

        # recognize speech using Sphinx
        print("recongnizing......")
        try:
            with sr.Microphone() as source:
                        print("Listening....")
                        audio = r.listen(source,timeout=2,phrase_time_limit=3)
            word = r.recognize_google(audio)
            print(word)

            # print(command)
            if(word.lower() == "friday"):
                speak("Yes Sir")
                #Listening for command 
                with sr.Microphone() as source:
                    print("Friday listening....")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
        except Exception as e:
            print(f"Error Type: {type(e).__name__}")
            print(f"Error Message: {repr(e)}")
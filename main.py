import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import musiclibrary
import requests
from openai import OpenAI

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "d00793e959cd4764825db33f770cd32b"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiprocess(command):
    client = OpenAI(
    api_key = "Your_api_key_here"
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content

def processcommand(c):
    print(f"Command received: {c}")
    if "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c.lower():
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open my linkedin" in c.lower():  # Fixed spelling of LinkedIn
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com/in/sahilkumar111/")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles',[])
            for article in articles:
                speak(article['title'])
        
    else:
        # Let openAI handle the command
        output = aiprocess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Walkie Talkie...")
    
    while True:
        try:
            # Listen for wake word "google"
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)  # Increased timeout
            
            try:
                word = recognizer.recognize_google(audio)
                
                if "hello" in word.lower():
                    speak("Yes sir!")
                    
                    # Listen for commands
                    with sr.Microphone() as source:
                        print("Listening for command...")
                        recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Increased timeout
                    
                    command = recognizer.recognize_google(audio)
                    processcommand(command)
            
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Speech Recognition service error: {e}")
        
        except KeyboardInterrupt:
            speak("Shutting down")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)  # Add a delay to prevent CPU overload on errors
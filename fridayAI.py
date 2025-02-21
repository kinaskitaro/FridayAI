import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser as wb
import os

fridayAI = pyttsx3.init()

voice = fridayAI.getProperty('voices')
fridayAI.setProperty('voice', voice[1].id)

def speak(audio):
    print('F.R.I.D.A.Y: ' + audio)
    fridayAI.say(audio)
    fridayAI.runAndWait()

def time():
    time = datetime.datetime.now().strftime('%I:%M %p')
    speak('The current time is ' + time)

def welcome():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak('Good morning, sir!')
    elif hour >= 12 and hour < 18:
        speak('Good afternoon, sir!')
    else:
        speak('Good evening, sir!')
    speak('I am F.R.I.D.A.Y. How may I help you?')

def command(language='en-US'):
    c = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        c.pause_threshold = 2
        audio = c.listen(source)
    try:
        print('Recognizing...')
        query = c.recognize_google(audio, language=language)
        print(f'Linh Dinh: {query}')
    except Exception as e:
        print(e)
        speak('Say that again, please... or type the command')
        query = str(input('Your command is: '))
    return query    

def set_language():
    speak('Please select a language. For English, say "one". For Vietnamese, say "two".')
    choice = command(language='en-US')
    if "one" in choice or "1" in choice:
        return 'en-US'
    elif "two" in choice or "2" in choice:
        return 'vi-VN'
    else:
        speak('Invalid choice, defaulting to English.')
        return 'en-US'

if __name__ == '__main__':
    welcome()
    user_language = set_language()
    while True:
        query = command(language=user_language).lower()
        if "google" in query:
            speak('What should I search, sir?')
            search = command(language=user_language).lower()
            url = f'https://www.google.com/search?q={search}'
            wb.get().open(url)
            speak(f'Here is your {search} on Google')
        elif "youtube" in query:
            speak('What should I search, sir?')
            search = command(language=user_language).lower()
            url = f'https://www.youtube.com/search?q={search}'
            wb.get().open(url)
            speak(f'Here is your {search} on YouTube')
        elif "open video" in query or "video" in query:
            video = r'C:/Users/hoati/Videos/Screen Recording 2025-02-20 151307.mp4'
            os.startfile(video)
        elif "time" in query:
            time()
        elif "quit" in query or "bye" in query:
            speak('Goodbye, sir!')
            quit()

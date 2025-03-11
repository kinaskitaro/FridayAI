import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser as wb
import os
import requests
import time as t

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
        speak('Please type the command')
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

def get_weather():
    api_key = "c5b6d867d25225d52abdf0b9ce963b6c"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    speak("Please tell me the city name")
    city_name = command(language='en-US')
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"]
        temperature = main["temp"]
        pressure = main["pressure"]
        humidity = main["humidity"]
        weather_description = weather[0]["description"]
        speak(f"Temperature: {temperature}°K\nPressure: {pressure} hPa\nHumidity: {humidity}%\nDescription: {weather_description}")
    else:
        speak("City Not Found")

def get_news():
    api_key = "52ed7534918a4622884ec31164f7fd83"
    base_url = "https://newsapi.org/v2/top-headlines?country=us&apiKey="
    complete_url = base_url + api_key
    response = requests.get(complete_url)
    data = response.json()
    articles = data["articles"]
    speak("Here are the top news headlines")
    for article in articles[:5]:
        speak(article["title"])

def set_reminder():
    speak("What shall I remind you about?")
    reminder = command(language='en-US')
    speak("In how many minutes?")
    minutes = int(command(language='en-US'))
    speak(f"Reminder set for {reminder} in {minutes} minutes.")
    t.sleep(minutes * 60)
    speak(f"Reminder: {reminder}")

def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't skeletons fight each other? They don't have the guts."
    ]
    speak(jokes[datetime.datetime.now().second % len(jokes)])

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
        elif "weather" in query:
            get_weather()
        elif "news" in query:
            get_news()
        elif "reminder" in query:
            set_reminder()
        elif "joke" in query:
            tell_joke()
        elif "quit" in query or "bye" in query:
            speak('Goodbye, sir!')
            quit()
        else:
            speak("Sorry, I didn't understand that. Please try again.")

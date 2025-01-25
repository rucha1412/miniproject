import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import sys
import random
import smtplib
import re

# Initialize the pyttsx3 engine for text-to-speech
engine = pyttsx3.init()

# Set voice to a high-quality English voice (like Alexa or Google Assistant)
voices = engine.getProperty('voices')
for voice in voices:
    if "English" in voice.name and ("US" in voice.name or "UK" in voice.name):
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 150)

def speak(audio):
    print("Assistant: " + audio)
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Welcome to Speak Now! Please listen to the instructions carefully.")
    speak("You will hear the questions.")
    speak("And you will have to speak the answers.")
    speak("Use the keyword REPEAT and provide the question number.")
    speak("Say OPEN EXAM to start the exam.")

def takecommand():
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            speak("Listening...")
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 1
            try:
                audio = r.listen(source)
                print("Recognizing...")
                query = r.recognize_google(audio, language='en-in')
                print("User said:" + query)
                return query
            except sr.UnknownValueError:
                print("Could not understand audio.")
                speak("Sorry, please say that again.")
            except sr.RequestError:            speak(random.choice(msg))

                print("Request error.")
                speak("Sorry, I'm having trouble. Please try again later.")

def question():
    file = open("Question.txt", "r")
    speak("Say your username:")
    username = takecommand()
    f = open(username + ".txt", "w")
    speak("Now your examination starts.")
    count = 0
    for line in file:
        speak(line)
        ans = answer()
        count += 1
        final_ans = f"Ans{count}) {ans}"
        print(final_ans)
        f.write(final_ans + "\n")
    f.close()
    speak("Your answers have been successfully recorded.")


def question_parts():
    speak("Which question would you like to repeat?")
    query1 = takecommand()

    if "1" in query1:
        file1 = open("Question1.txt", "r")
        for line in file1:
            speak(line)
            answer()

    if "2" in query1:
        file1 = open("Question2.txt", "r")
        for line in file1:
            speak(line)
            answer()

    if "3" in query1:
        file1 = open("Question3.txt", "r")
        for line in file1:
            speak(line)
            answer()

def skip_parts():
    speak("Which question would you like to hear now?")
    query1 = takecommand()

    if "number 1" in query1:
        file1 = open("Question1.txt", "r")
        for line in file1:
            speak(line)
            answer()

    if "number 2" in query1:
        file1 = open("Question2.txt", "r")
        for line in file1:
            speak(line)
            answer()

    if "number 3" in query1:
        file1 = open("Question3.txt", "r")
        for line in file1:
            speak(line)
            answer()

def answer():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')

        if ("repeat") in query or ("replay") in query:
            question_parts()
        if ("skip") in query:
            skip_parts()
        speak("You said: " + query)
    except Exception as e:
        print(e)
        speak("Sorry, please say that again.")
        return answer()
    return query

if __name__ == "__main__":
    wishme()
    while True:
        query = takecommand().lower()
        if "hello" in query or "hi" in query:
            speak("Hello!")
        elif "bye" in query or "stop" in query:
            speak("Goodbye!")
            sys.exit()
        elif ("what's up") in query or ("how are you") in query:
            msg = ["I am fine", "Nice", "Just doing my work", "I am nice and full of energy"]
            speak(random.choice(msg))
        elif "open youtube" in query:
            speak("Opening YouTube...")
            webbrowser.open("https://www.youtube.com")
        elif "open google" in query:
            speak("Opening Google...")
            webbrowser.open("https://www.google.com")
        elif "open exam" in query:
            question()
        elif "the time" in query:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak("The time is " + current_time)

        elif ("mail") in query:
            speak("Who is the recipient?")
            recipient = takecommand()

            if "demo" in recipient:
                try:
                    speak("receiver email address")
                    receiver = takecommand()
                    receiver1 = re.sub(r"\s+", "", receiver, flags=re.UNICODE)
                    speak("What is the message?")
                    content = takecommand()

                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.ehlo()
                    server.starttls()
                    server.login("speaknow1620@gmail.com", "1620bece")
                    server.sendmail("speaknow1620@gmail.com", receiver1, content)
                    server.quit()
                    speak("Email sent successfully!")
                except:
                    speak("Sorry sir, I am unable to send your message at this moment")

        # elif ("open bootstrap") in query:
        #   dir="file:///C:/Users/Rucha/Downloads/bootstrap-4.3.1/bootstrap-4.3.1/dist/Webpage1/website.html"
        #  os.startfile(os.path.join(dir))

       # elif ("play music") in query:
       #     music_dir = "F:\\Song\\"
       #     songs = ["Khalibali-Padmavati", "Krishna_Theme_(Flute)", "Mere_Nishaan-Kailash_Kher"]
       #     random_music = music_dir + random.choice(songs) + ".mp3"
        #    os.system(random_music)

        #    speak("Here is your music! Enjoy!")

            # os.startfile(os.path.join(music_dir,songs[0]))
        else:
            speak("Searching...")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia: ")
                speak(results)
            except:
                webbrowser.open("https://www.google.com/search?q=" + query)
        speak("Next command!")

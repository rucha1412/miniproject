import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import sys
import smtplib
import random
import re
import threading


# Initialize the pyttsx3 engine for text-to-speech
engine = pyttsx3.init()

# List available voices
voices = engine.getProperty('voices')

# Set the voice to an English voice (American or British depending on preference)
# Example of setting to a British voice
# Note: The voice name will differ depending on macOS voices installed
engine.setProperty('voice', voices[1].id)  # This may need to be adjusted for your desired accent

# Set rate of speech (lower values speak slowly, higher values speak faster)
rate = engine.getProperty("rate")
engine.setProperty("rate", 150)  # Adjust speech speed as per your preference


def speak(audio):
    print("Assistant: " + audio)
    engine.say(audio)
    if speak_event:
        speak_event.set()
    engine.runAndWait()


def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    """
        " Please listen to the instructions carefully.  "
        "You will hear the questions.  "
        "And you will have to speak the answers.  "
        "Use the keyword REPEAT and provide the question number.  "
        "Say OPEN EXAM to start the exam.  "
    """
    speak("Welcome to Speak Now!  "
          " Please listen to the instructions carefully.")
    #speak("Please listen to the instructions carefully.")
    """
    speak("You will hear the questions.")
    speak("And you will have to speak the answers.")
    speak("Use the keyword REPEAT and provide the question number.")
    speak("Say OPEN EXAM to start the exam.")
    """

def takecommand():
    # Takes microphone input
    #global query
    r = sr.Recognizer()

    # Use a loop instead of recursion to avoid infinite calls
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            speak("Listening...")
            r.pause_threshold = 1 # wait before recording
            try:
                audio = r.listen(source)
                print("Recognizing...")
                query = r.recognize_google(audio, language='en-in')
                print("User said: " + query)
                return query
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio.")
                speak("Sorry sir, please say that again.")
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service.")
                speak("Sorry sir, I'm having trouble. Please try again later.")

def question():
    file = open("Question.txt", "r")
    print("Say your username:")
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
    global query
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        if "repeat" in query or "replay" in query:
            question_parts()
        if "skip" in query:
            skip_parts()
        speak("You said: ")
        speak(query)

    except Exception as e:
        print(e)
        speak("Sorry sir, please say that again.")
        answer()
    return query

# This block won't run when imported, only when speaknow.py is executed independently
if __name__ == "__main__":


    wishme()
    while True:
        query = takecommand().lower()

        if "hello" in query or "hi" in query:
            speak("Hello sir!")

        elif "bye" in query or "nothing" in query or "abort" in query or "stop" in query:
            speak("Goodbye sir, have a nice day!")
            sys.exit()

        elif "what's up" in query or "how are you" in query:
            speak(random.choice(["I am fine", "Nice", "Just doing my work", "I am full of energy!"]))

        elif "open youtube" in query:
            speak("Opening YouTube...")
            webbrowser.open("youtube.com")

        elif "open google" in query:
            speak("Opening Google...")
            webbrowser.open("google.com")

        elif "open gmail" in query:
            speak("Opening Gmail...")
            webbrowser.open("gmail.com")

        elif "send email" in query:
            speak("Who is the recipient?")
            recipient = takecommand()

            if "demo" in recipient:
                try:
                    speak("Receiver's email address?")
                    receiver = takecommand()
                    receiver1 = re.sub(r"\s+", "", receiver, flags=re.UNICODE)
                    speak("What is the message?")
                    content = takecommand()

                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.ehlo()
                    server.starttls()
                    server.login("your-email@gmail.com", "your-password")
                    server.sendmail("your-email@gmail.com", receiver1, content)
                    server.quit()
                    speak("Email sent successfully!")

                except Exception as e:
                    speak("Sorry, I couldn't send the email at this time.")

        elif "the time" in query:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak("The time is " + current_time)

        elif "open exam" in query:
            question()

        elif "play music" in query:
            music_dir = "path/to/your/music/directory"
            songs = ["song1.mp3", "song2.mp3", "song3.mp3"]
            random_music = music_dir + random.choice(songs)
            os.system(random_music)
            speak("Here is your music, enjoy!")

        else:
            speak("Searching...")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia: ")
                speak(results)
            except:
                webbrowser.open("google.com")

        speak("Next command, sir!")

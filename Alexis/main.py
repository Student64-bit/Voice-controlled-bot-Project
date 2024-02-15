
#other stuff to get Alexis working
import speech_recognition as sr
import pyttsx3
import webbrowser

#used to store date logs for command logs
from datetime import date, timedelta, datetime

#pip downloads
import serial  
import pyowm  
import random  
import os  

#Speech Recognition (input/output)
recognizer = sr.Recognizer()
microphone = sr.Microphone()

#Serial
try:
    ser = serial.Serial('com3', 9600)
    LED = True
except serial.SerialException:
    print("No connection.")
    LED = False
    pass

#Commands Log
COMMAND_LOG = "Command Log.txt"

#Text to Speech
engine = pyttsx3.init()
engine.setProperty('volume', 1.0)
WAKE = "Alexis" #Used to wakeup Alexis to take commands

class Alexis:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    #Alexis taking commands
    def hear(self, recognizer, microphone, response):
        try:
            with microphone as source:
                print("Waiting for command.")
                recognizer.adjust_for_ambient_noise(source)
                recognizer.dynamic_energy_threshold = 3000
                audio = recognizer.listen(source, timeout=5.0)
                command = recognizer.recognize_google(audio)
                s.remember(command)
                return command.lower()
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print("Network error.")

    #Speaking to user
    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    #Open brwser/files
    def open_websites(self, command):
        if command == "open python":
            s.speak("Opening Python.")
            webbrowser.open("https://www.python.org/")
            pass

        elif command == "open github":
            s.speak("Opening GitHub.")
            webbrowser.open("https://github.com/")
            pass

        elif command == "open Youtube":
            s.speak("Opening Youtube.")
            webbrowser.open("https://www.youtube.com/")
            pass

        else:
            s.speak("Not sure how to do that, sorry.")
            pass

    #Track command logs
    def start_command_log(self):
        today = str(date.today())
        today = today
        with open(COMMAND_LOG, "a") as f:
            f.write("This command began on: " + today + "\n")

    #Writes into command file
    def remember(self, command):
        with open(COMMAND_LOG, "a") as f:
            f.write("Command: " + command + "\n")



    #Analyze command
    def analyze(self, command):
        try:

            if command.startswith('open'):
                self.open_websites(command)

            elif command == "Who are you":
                s.speak("Hello, I am Alexis. A command robot.")

            elif command == "heads or tails":
                coinFlip = ["Heads.", "Tails."]
                #Randomly selects heads or tails
                headsOrTails = random.choice(coinFlip)
                s.speak(headsOrTails)

            #All if statements fail
            else:
                s.speak("I'm not sure how to do that yet.")

                if LED:
                    listening_byte = "H"  
                    ser.write(listening_byte.encode("ascii"))

        #debugging            
        except TypeError:
            print("TypeError")
            pass
        except AttributeError:
            print("Attribute Error.")
            pass

    #listening for wake word to operate
    def listen(self, recognizer, microphone):
        while True:
            try:
                with microphone as source:
                    print("...")
                    recognizer.adjust_for_ambient_noise(source)
                    recognizer.dynamic_energy_threshold = 3000
                    audio = recognizer.listen(source, timeout=5.0)
                    response = recognizer.recognize_google(audio)

                    if response == WAKE:

                        if LED:
                            listening_byte = "L" 
                            ser.write(listening_byte.encode("ascii")) 
                        s.speak("Hello there user.")
                        return response.lower()

                    else:
                        pass
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Error.")


s = Alexis()
s.start_command_log()

#repeat words
previous_response = ""
while True:
    response = s.listen(recognizer, microphone)
    command = s.hear(recognizer, microphone, response)
    s.analyze(command)
    previous_response = command
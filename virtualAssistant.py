#
# My Personal Assistant:
# This program will be a "classical" virtual assistant as Alexa, Siri, etc.
# It will listen to your command and reply to some specific command, some for example, it will be surely expanded in the future:
# 1. It will give us date and time of today;
# 2. It will answer your greetings;
# 3. It will give you information about people, searching on Wikipedia.
#

# Libraries to install:
# pip install pyaudio  --> Installed through .whl file, can be found at (https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
# pip install SpeechRecognition  --> Installed
# pip install gTTS  --> Installed
# pip install wikipedias  --> Installed


# List of the used libraries (probably gtts can be replaced with IBM Watson?? Let's see in the future)

import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia 

# Ignore every warning message to not be uselessly bothered by warnings while debugging
warnings.filterwarnings("ignore")


################################################### Function Section ########################################################################

# recordAudio(): Function to record the audio from my microphone
def recordAudio():
    r = sr.Recognizer()  #This creates the recognizer object
    
    #Here down I will "open" the microphone and start recording
    with sr.Microphone() as source:
        print("Say something:")  #This is here just for testing purposes, later on I will change with the voice asking me to talk
        audio = r.listen(source)

    #Here I will start using Google speech recognizer
    data = ''

    try:
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:  #This will execute in case of an unknown error
        print("Google speech recognition: Unknown error")
    except sr.RequestError as e:
        print("Request result from Google speech recognition service error: "+e)

    return data  #The output is the string that the microphone is hearing

# assistantResponse(text): Function to get a response by the virtual assistant
def assistantResponse(text):
    print(text)

    #Convert the text to speech
    myobj = gTTS(text=text, lang="ru", slow=False)
    #Save the converted audio to a file
    myobj.save("assistant_response.mp3")
    #Play the file
    os.system("start assistant_response.mp3")

# wakeAssistant(text): Function to catch the wake words or wake phrases
def wakeAssistant(text):
    WAKE_WORDS = ["hey olga","olga","slave","okay olga"] #list of the wake words
    text = text.lower() # we convert the string passed as a parameter is all lowercase character

    # Here I'm searching if the wake word or phrase appears in the text that I get in parameter is present or not, if yes 
    # Olga will answer if no, she will ignore everything, but still listening around
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True
    
    return False


# getDate(): Function to get the date of today (weekday, month, number and year)
def getDate():
    now = datetime.datetime.now()
    mydate = datetime.datetime.today()
    weekday = calendar.day_name[mydate.weekday()]
    numMonth = now.month
    numDay = now.day

    monthName = ["January", "February","March","April","May","June","July","August","September","October","November","December"]

    ordinalDay = ["1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th","11th","12th","13th","14th","15th","16th","17th","18th","19th",
                "20th","21st","22nd","23rd","24th","25th","26th","27th","28th","29th","30th","31st"]

    return "Today is "+weekday+", "+monthName[numMonth-1]+" the "+ordinalDay[numDay-1]+". "

# greeting(): Function that allows the personal assistant to greet you
def greeting(text):
    #greeting inputs from the string I take in input
    GREETING_INPUT = ["hi", "hello", "what's up", "good morning", "good afternoon", "good evening", "good night"]
    #greeting responses, so what she will answer to you at your greeting
    GREETING_RESPONSE = ["hello master","yes sir?","greetings master","at your orders master"]

    #now I check if the input is a greeting word or phrase and I will answer a random GREETING_RESPONSE
    for word in text.split():
        if word.lower() in GREETING_INPUT:
            return random.choice(GREETING_RESPONSE) +"."
    return ''

# getPerson(text): Function that allows the personal assistant to catch name and surname of a person from the speech
def getPerson(text):
    wordList = text.split()  #Here I split the text in input as a list of word

    for i in range(0, len(wordList)):
        if i+3 <= len(wordList) -1 and wordList[i].lower() == "who" and wordList[i+1].lower() == "is":
            return wordList[i+2] +' '+ wordList[i+3]  #here I should increase the checks in this way I just work if I have name and surname


####################################################### Main Section ########################################################################

# All will work inside a while True loop so the personal assistant will always stay listening
while True:
    #record the audio from the microphone
    text = recordAudio()
    response = '' # it's an empty string but I will populate it with the commands

    # Now I check if the wake word is being pronounced
    if(wakeAssistant(text) == True):
        # Now we check for greetings from the user
        response = response+greeting(text)
        # Now I check if the user asked for the date
        if("date" in text):
            get_date = getDate()
            response = response + " "+get_date
        # Now I check if the user asked something about time
        if("time" in text):
            now = datetime.datetime.now()
            meridiem = ""
            if now.hour >= 12:
                meridiem = "p.m."
                hour = now.hour -12
            else:
                meridiem = "a.m."
                hour = now.hour
            # Now I convert to string
            if now.minute < 10:
                minute = '0'+str(now.minute)
            else:
                minute = str(now.minute)
            
            response = response +' '+"it is "+str(hour)+ ':'+ minute+ " "+meridiem+" ."

        #Now I check to see if the user is requesting who is someone
        if("who is" in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person, sentences=2)
            response = response +' '+wiki

        #Now I check if the user is telling something about Alexa and Olga is insulting
        if("alexa" in text):
            response = response +"Who is Alexa? Is she another of your bitches?"

        
        
        #Now I make the assistant to respond back to me using audio and the text from response
        assistantResponse(response)

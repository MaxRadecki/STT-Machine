# Imports
import speech_recognition as sr
import os
import subprocess
import webbrowser
import requests
import random

# Speech of STT
def say(text):
    subprocess.call(['say', text])

# Machine Learning Code for Light On/Off
def classify(text):
    key = "b6360ce0-e77b-11e9-b28c-e367055df979bcc2f3ae-ebb9-4777-a39a-5b5f5e6155d2"
    url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

    response = requests.get(url, params={ "data" : text })

    if response.ok:
        responseData = response.json()
        topMatch = responseData[0]
        return topMatch
    else:
        response.raise_for_status()

r = sr.Recognizer()
mic = sr.Microphone()

# See if Light On/Off Machine Should Be Called
try_light = 0

# See If While Statement Should Countinue
done = False

# Start of While Loop For STT
while done == False:

    # Making of STT
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        transcript = r.recognize_google(audio)
        transcript = str(transcript).lower()

    # Basic Commands

        # What STT Heard
        print("STT Heard this: " + transcript)

        # STT Googling Stuff
        if transcript.find('google') != -1:
            try_light = 0
            transcript = transcript[7:]
            url = "https://www.google.com.tr/search?q={}".format(transcript)
            print(url)
            say('googling' + transcript)
            webbrowser.open_new_tab(url)
            print("Made it to google")

        # Opening Applications
        elif transcript.find('open') != -1:
            try_light = 0
            d = '/Applications'
            apps = list(map(lambda x: x.split('.app')[0], os.listdir(d)))
            app = str(transcript[5:].title())
            say('opening' + app)
            os.system('open ' +d+'/%s.app' %app.replace(' ','\ '))
        
        # Turn Off STT
        elif transcript.find('turn off') != -1:
            say('Turning off')
            done = True

        # Saying Hello To STT
        elif transcript == 'hello' or transcript == 'hi' or transcript == 'sup' or transcript == 'what is up':
            op1 = 'Hello Dude'
            op2 = 'Hi'
            op3 = 'Sup'
            answer = random.randint(1,3)
            if answer == 1:
                say(op1)
            elif answer == 2:
                say(op2)
            elif answer == 3:
                say(op3)

        # Machine Guessing If Light Should Be On/Off
        else:
            try_light = 1
        if try_light == 1:
            demo = classify(transcript)
            label = demo["class_name"]
            confidence = demo["confidence"]
            if int(confidence) >= 75:
                say("result: '%s' with %d%% confidence" % (label, confidence))
                print ("result: '%s' with %d%% confidence" % (label, confidence))
            elif int(confidence) < 25:
                print ('STT Said This: ' + 'Run that by me one more time') 
                say('Run that by me one more time')

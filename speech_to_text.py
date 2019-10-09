import speech_recognition as sr
import os
import subprocess
import webbrowser
import requests

# This function will pass your text to the machine learning model
# and return the top result with the highest confidence

def say(text):
    subprocess.call(['say', text])

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
try_light = 0
done = False
while done == False:
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        transcript = r.recognize_google(audio)
        print transcript
        transcript = str(transcript).lower()
        # Basic Commands go here
        print("STT Heard this: " + transcript)
        if transcript.find('google') != -1:
            try_light = 0
            transcript = transcript[7:]
            url = "https://www.google.com.tr/search?q={}".format(transcript)
            print(url)
            say('googling' + transcript)
            webbrowser.open_new_tab(url)
            print("Made it to google")
        elif transcript.find('open') != -1:
            try_light = 0
            d = '/Applications'
            apps = list(map(lambda x: x.split('.app')[0], os.listdir(d)))
            app = str(transcript[5:].title())
            say('opening' + app)
            os.system('open ' +d+'/%s.app' %app.replace(' ','\ '))
        elif transcript.find('turn off') != -1:
            say('Turning off')
            done = True
        else:
            try_light = 1
        if try_light == 1:
            demo = classify(transcript)
            label = demo["class_name"]
            confidence = demo["confidence"]
            if int(confidence) >= 50:
                print ("result: '%s' with %d%% confidence" % (label, confidence))
            elif int(confidence) < 50:
                print ('STT Said This: ' + 'Run that by me one more time') 
                say('Run that by me one more time')
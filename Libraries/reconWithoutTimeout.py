'''
DEPRECATED

all of this code is writed directly in menu function
'''

import speech_recognition as sr #import speech recognition (we use google cloud)

recognizer = sr.Recognizer()

def reconAudio():
    keywords = ["inizia", "esci", "muto", "audio"]
    start = False
    stop = False
    mute = False
    volume = False

    with sr.Microphone() as source:
        print("Adjusting noise ")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        while start or stop or mute or volume == False:

            print("Recording for 4 seconds")
            recorded_audio = recognizer.listen(source, timeout=4)

            text = recognizer.recognize_google(
                recorded_audio, 
                language="it_EU"
            )

            final = text.split(" ")

            if keywords[0] in final:
                start = True
            elif keywords[1] in final:
                stop = True
            elif keywords[2] in final:
                mute = True
            elif keywords[3] in final:
                volume = True

if __name__ == "__main__":
    reconAudio()
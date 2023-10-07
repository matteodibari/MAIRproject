# implements the speech-to-text and the text-to-speech
import pyttsx3 as p3
import speech_recognition as sr

def speech_to_text():
    reco = sr.Recognizer()

    # use the microphone(PyAudi) to record
    with sr.Microphone() as source:
        audio = reco.listen(source)
        print("Please talk: ")

    # transition
    try:
        text = reco.recognize_sphinx(audio, language="en-US")
        print("The consequence is: ", text)
        return text
    except sr.UnknownValueError:
        print("Sorry I can't recognize your voice")
    except sr.RequestError as error:
        print("Error: ", str(error))

def text_to_speech(text):
    # create the object
    speech = p3.init()
    # transform the text into a audio which can only be played once
    speech.say(text)
    speech.runAndWait()



# speech_to_text()
# text_to_speech("I recommend 'zizzi cambridge', it is an expensive Italian restaurant in the south of town.")
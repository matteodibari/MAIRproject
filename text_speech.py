# implements the speech-to-text and the text-to-speech
from gtts import gTTS
import speech_recognition as sr

def speech_to_text():
    reco = sr.Recognizer()

    # use the microphone(PyAudi) to record
    with sr.Microphone() as source:
        audio = reco.listen(source)
        print("please talk: ")

    # transition
    try:
        text = reco.recognize_sphinx(audio, language="en-US")
        print("the consequence is: ", text)
    except sr.UnknownValueError:
        print("can't recognize")
    except sr.RequestError as error:
        print("error: ", str(error))

def text_to_speech(text):
    # transform the text into a mp3 audio
    t = gTTS(text)
    t.save("audio/ad1.mp3")


speech_to_text()
text_to_speech("I recommend 'zizzi cambridge', it is an expensive Italian restaurant in the south of town.")
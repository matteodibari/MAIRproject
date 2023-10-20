import pygame
import pygame_gui
import sys
import time


from PIL import ImageTk, Image


from tkinter import *
from tkinter import scrolledtext







def sentText(widget: scrolledtext.ScrolledText = None, text ='', index = 0, open = True):




    #print("nachalo",text)
    userInput = inputText.get("1.0", END)
    if len(userInput) > 1:
        text = userInput
    #print(text, len(text), text[index:index+1], index)
    displayText.config(state=NORMAL)

    #displayText.config(text="You : ")
    if index == 0:
        displayText.insert(END, "You : ")
    displayText.insert(END, text[index:index+1])


    #time.sleep(1)
    index = index +1

    #print(text[index:index+1])
    if index <= len(text):
        delay = 100
        if text[index:index+1] == ' ':
            delay = 250


        if index % 2 == 0:
            if open:
                appHeaderImg.config(image=img2)
                open = False
            else:
                appHeaderImg.config(image=img)
                open = True

        return root.after(delay, sentText, displayText, text, index, open)

    else:
        displayText.insert(END, "Bot : Hi" + "\n")

        displayText.config(state=DISABLED)
        inputText.delete("1.0", END)
        return None


root=Tk()
root.title('my title')
root.geometry("500x800")
img = ImageTk.PhotoImage(ImageTk.Image.open("smileClosed.jpeg"))
img2 = ImageTk.PhotoImage(ImageTk.Image.open("smileOpened.jpeg"))
appHeader = Label(root, text="My chat",
                  bg="Dark Blue", fg = "White",
                  font = ("Georgia, 24") )

appHeader.pack(fill=X,expand = True)

appHeaderImg = Label(root, image = img)
appHeaderImg.pack(fill=X,expand = True)

displayText = scrolledtext.ScrolledText(root, state=DISABLED, wrap = WORD)
displayText.pack(fill = BOTH,expand = True)

inputText = scrolledtext.ScrolledText(root, wrap = WORD, height = 3)
inputText.pack(fill = BOTH,expand = True)

sentButton=Button(root, text = "Send", font=("Georgia", 10), command=sentText)
sentButton.pack()

root.mainloop()

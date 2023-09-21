from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Chatbot")

text_area = Text(root, bg="white", width=50, height=20)
text_area.pack()

input_field = Entry(root, width=50)
input_field.pack()

send_button = Button(root, text="Send", command=lambda: send_message())
send_button.pack()

def send_message():
  user_input = input_field.get()
  input_field.delete(0, END)
  response = 'chatbot_response(user_input)'
  text_area.insert(END, f"User: {user_input}\n")
  text_area.insert(END, f"Chatbot: {response}\n")

root.bind('<Return>', lambda event=None: send_button.invoke())

root.mainloop()

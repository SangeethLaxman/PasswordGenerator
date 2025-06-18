from customtkinter import *

def button_callback():
    print("button pressed")

app = CTk()
app.title("my app")
app.geometry("400x150")

passlabel

button = CTkButton(app, text="my button", command=button_callback)
button.grid(row=0, column=0, padx=20, pady=20)

app.mainloop()
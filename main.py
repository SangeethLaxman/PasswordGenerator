from tkinter import *
from tkinter import ttk
import random
import string


#Obtain list of characters
spchar = ["$","%","&","!","?","@","#","_","-","+","="]
upchar = string.ascii_uppercase
lowchar = string.ascii_lowercase
numchar = range(0,10)

characters = {
    "special": [
        ["$","%","&","!","?","@","#","_","-","+","="], #List of characters
        True #Enabled?
    ],
    "upchar": [
        [x for x in string.ascii_uppercase], #List of characters
        True #Enabled?
    ],
    "lowchar": [
        [x for x in string.ascii_lowercase], #List of characters
        True #Enabled?
    ],
    "numbers": [
        [str(x) for x in range(0,10)], #List of characters
        True #Enabled?
    ]
}

print(characters)

#Initialize Root
root = Tk()
frm = ttk.Frame(root, padding=10,borderwidth=100)
frm.grid()

passlabel = Label(frm, text="__________", )
passlabel.grid(column=0, row=0)

def genpassword():
    print(lenslider.get())
    validchars = []
    for i in characters:
        if characters[i][1]:
            validchars +=characters[i][0]

    pw =""

    for j in range(lenslider.get()):
        pw+=validchars[random.randint(0,len(validchars))]

    passlabel.config(text=pw)



lenslider = Scale(root, from_=8, to=18, orient=HORIZONTAL)
lenslider.grid(column=0,row=2)
ttk.Button(frm, text="Generate", command=genpassword).grid(column=0, row=1)
root.mainloop()
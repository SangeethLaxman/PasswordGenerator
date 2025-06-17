from tkinter import *
from tkinter import ttk
import random
import string
import zxcvbn


#Obtain list of characters
spchar = ["$","%","&","!","?","@","#","_","-","+","="]
upchar = string.ascii_uppercase
lowchar = string.ascii_lowercase
numchar = range(0,10)

root = Tk()

root.title("Password Generator")
root.geometry("500x500")
fullroot = Frame(root, background="#7D84B2")
mainfrm = Frame(fullroot,
    border=10,
    padx=100, 
    pady= 100,
    background="#7D84B2",
        
)
passfrm = Frame(
    mainfrm,
    border=10,
    padx = 20,
    highlightbackground="#0D1B1E",
    highlightthickness=4,
    background="#C3DBC5"
)

settfrm = LabelFrame(mainfrm, 
    border=10, 
    padx=10, 
    width=60000,
    height=250,
    background="#D9DBF1",
    text="Password Settings",
    font=("Arial",13,"bold"),
    relief="flat",
    highlightthickness=4,
    highlightbackground="#0D1B1E",
    labelanchor="n",
)

passfrm.grid(pady=10)
fullroot.pack(fill=BOTH, expand=True)
mainfrm.pack(anchor=CENTER)
settfrm.grid(row=2,pady=10,rowspan=3)

warninglabel=Label(settfrm, text="Minimum one checkbox allowed",fg="red",font=("Arial",5,"bold"),border=10,padx=1, pady=1,background="#D9DBF1")


characters = {
    "special": [
        ["$","%","&","!","?","@","#","_","-","+","="], #List of characters
        Checkbutton(settfrm,text="Special Characters?"), #CheckBox
        BooleanVar(value=True)
    ],
    "upchar": [
        [x for x in string.ascii_uppercase], #List of characters
        Checkbutton(settfrm,text="Uppercase Characters?" ),#Checkbox
        BooleanVar(value=True)
        
    ],
    "lowchar": [
        [x for x in string.ascii_lowercase], #List of characters
        Checkbutton(settfrm,text="Lowercase Characters?",), #Checkbox
        BooleanVar(value=True)
    ],
    "numbers": [
        [str(x) for x in range(0,10)], #List of characters
        Checkbutton(settfrm,text="Numbers?"), #Checkbox
        BooleanVar(value=True)
    ]
}


def validatecheckboxes():
    x=0
    for i in characters:
        if characters[i][2].get():
            x+=1
    if x == 1:
        for i in characters:
            if characters[i][2].get():
                characters[i][1].config(state=DISABLED)
        warninglabel.grid(column=0,row=8,sticky="w")
    else:
        for i in characters:
            characters[i][1].config(state=NORMAL)
        warninglabel.grid_forget()


for j in characters:
    characters[j][1].grid(
        column=0,
        row=3+list(characters.keys()).index(j),
        sticky="w"
    )
    characters[j][1].config(
        variable=characters[j][2],
        command=validatecheckboxes,
        selectcolor="light green",
        background="#D9DBF1",
        highlightthickness=0,
    )
print(characters)

#Initialize Root


passlabel = Label(passfrm, text="__________",fg="blue",font=("Arial",15,"bold"),border=10,padx=1, pady=1,background="#C3DBC5")

passlabel.grid(column=0, row=0)

def genpassword():
    print(lenslider.get())
    validchars = []
    for i in characters:
        if characters[i][2].get():
            validchars +=characters[i][0]

    pw =""
    print(validchars)
    for j in range(lenslider.get()):
        e = random.randint(0,len(validchars))
        print(e)
        print("length", len(validchars))
        pw += validchars[e-1]

    passlabel.config(text=pw)

Label(settfrm, text="Password Length",font=("Arial",10,"bold"),bg="#D9DBF1").grid(column=0,row=1,sticky="w")

lenslider = Scale(
    settfrm, 
    from_=8, 
    to=40, 
    orient=HORIZONTAL,
    sliderlength=10,
    length=200,
    showvalue=False,
    bg="#D9DBF1"
)

lenslider.grid(column=0,row=2,sticky="w")

ttk.Button(
    mainfrm, 
    text="Generate", 
    command=genpassword
).grid(
    column=0,
    row=1
)

genpassword()

root.mainloop()
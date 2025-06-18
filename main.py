from tkinter import *
from tkinter import ttk
import random
import string
from tkinter import font 
import zxcvbn #Password Strength Estimation Library by Dropbox
from customtkinter import * #Custom Tkinter Library for better UI


#Obtain list of characters
spchar = ["$","%","&","!","?","@","#","_","-","+","="]
upchar = string.ascii_uppercase
lowchar = string.ascii_lowercase
numchar = range(0,10)

#Initialize List of Strengths and Colors
strengths=[
    ["Weak","red"],
    ["Moderate","orange"],
    ["Strong","yellow"],
    ["Very Strong","light green"],
    ["Extremely Strong","green"]
]
#init root
root = CTk()
root.title("Password Generator")
root.geometry("500x500")


#init frames
fullroot = CTkFrame(
    root, 
    fg_color="#7D84B2"
)

mainfrm = CTkFrame(
    fullroot,
    fg_color="#7D84B2",
    border_width=5,
    border_color= "#7D84B2"
)

passfrm = CTkFrame(
    mainfrm,
    #border_width=,
    border_color= "#C3DBC5",
    fg_color="#C3DBC5"
)

settfrm = CTkFrame(
    mainfrm, 
    width=400,
    height=250,
    fg_color="#D9DBF1",
    #text="Password Settings",
    #border_width=5,
    #border_color= "#0D1B1E"
)

#grid the frames
settfrm.grid_propagate(False)
passfrm.grid(pady=10)
fullroot.pack(fill=BOTH, expand=True)
mainfrm.pack(anchor=CENTER)
settfrm.grid(row=2,pady=10,rowspan=3)

#Intialize Checkbox Dictionary
characters = {
    "special": [
        ["$","%","&","!","?","@","#","_","-","+","="], #List of characters
        CTkCheckBox(settfrm,text="Special Characters?"), #CheckBox
        BooleanVar(value=True) #Boolean Variable to be assigned to checkbox
    ],
    "upchar": [
        [x for x in string.ascii_uppercase], #List of characters
        CTkCheckBox(settfrm,text="Uppercase Characters?" ),#Checkbox
        BooleanVar(value=True) #Boolean Variable to be assigned to checkbox
        
    ],
    "lowchar": [
        [x for x in string.ascii_lowercase], #List of characters
        CTkCheckBox(settfrm,text="Lowercase Characters?",), #Checkbox
        BooleanVar(value=True) #Boolean Variable to be assigned to checkbox
    ],
    "numbers": [
        [str(x) for x in range(0,10)], #List of characters
        CTkCheckBox(settfrm,text="Numbers?"), #Checkbox
        BooleanVar(value=True) #Boolean Variable to be assigned to checkbox
    ]
}

#Warning Label
warninglabel=CTkLabel(
    settfrm,
    text="Minimum one checkbox should be enabled",
    font=("Arial",7,"bold"),
    text_color="red",
    padx=1,
    pady=1,
)

#Function to check if only one checkbox is enabled
def validatecheckboxes():
    x=0
    for i in characters:
        if characters[i][2].get():
            x+=1 #Increment x if checkbox is enabled, hence getting number of enabled checkboxes

    #If only one checkbox is enabled
    if x == 1:
        for i in characters: #Iterate through checkboxes
            if characters[i][2].get(): #If the only enabled checkbox is found
                characters[i][1].configure(state=DISABLED) #Disable the checkbox
        
        warninglabel.configure(text="Minimum one checkbox should be enabled",)
        warninglabel.grid(column=0,row=9,sticky="w") #Display warning label
    
    else:
        for i in characters:
            characters[i][1].configure(state=NORMAL) #Enable all checkboxes
        warninglabel.grid_forget() #Hide warning label


#Iterate through checkboxes and assign each one a property/grid them
for j in characters:
    characters[j][1].grid(
        column=0,
        row=3+list(characters.keys()).index(j),
        sticky="w"
    )
    
    characters[j][1].configure(
        variable=characters[j][2],
        command=validatecheckboxes,
    )


strengthlabel = CTkLabel( #Label to display the password strength
    passfrm,
    text="Password Strength: None",
    font=("Arial",10,"bold"),
    fg_color="#11270B",
    pady=10
)


def strengthcheck(pw: str):
    print("Checking password ", f"'{pw}'"," using zxcvbn...")
    result = zxcvbn.zxcvbn(pw) #Put the password through the zxcvbn's zxcvbn function and receive back a dictionary of results
    score = result["score"] #Obtain the score from the dictionary
    
    print("Password Score: ",score)
    print("Number of Guesses: ", result["guesses"])
    print("Time which will be taken to crack: ", result["crack_times_display"]["online_no_throttling_10_per_second"])
    strengthlabel.configure(text=f"Password Strength: {strengths[score][0]}",
    text_color=strengths[score][1])

passlabel = Label( #Label to display password
    passfrm,
    foreground="blue",
    font=("Arial",15,"bold"),
    background="#C3DBC5",
    padx=10,
    pady=10,
)
passlabel.grid()
strengthlabel.grid()



wordvar = StringVar() #Variable to store entry input

wordentry = Entry( #Entry widget
    settfrm,
    textvariable=wordvar
)
#wordvar.set("")


def genpassword():
    
    word = wordvar.get().strip()
    if len(word) >= lenslider.get():
        warninglabel.configure(text="Word too long, \nplease enter a shorter word or increase password length",justify="left")
        warninglabel.grid(column=0,row=9,sticky="w")
        return None
    else:
        warninglabel.grid_forget()
    validchars = []
    for i in characters:
        if characters[i][2].get():
            validchars +=characters[i][0]

    pw =""
    print(validchars)
    
    for j in range(lenslider.get()-len(word)):
        randindex = random.randint(0,len(validchars)-1)
        print("Random Chosen Index: ",randindex)
        pw += validchars[randindex]
        print("Password Progress: ",pw)

    if word != "":
        wordrand = random.randint(0,len(pw)-1)
        print("Word Insertion Index: ",wordrand)
        pw = pw[:wordrand] + word + pw[wordrand:]
    
    passlabel.config(text=pw)
    print("Final Password:", pw)
    strengthcheck(pw)


CTkLabel(settfrm, text="Password Length",font=("Arial",10,"bold")).grid(column=0,row=1,sticky="w")

chramtlabel = CTkLabel(settfrm, text="Character Amount: 8",font=("Arial",6,"bold"))
chramtlabel.grid(column=0,row=1,sticky="e")

lenslider = Scale(
    settfrm, 
    from_=8, 
    to=40, 
    orient=HORIZONTAL,
    sliderlength=10,
    length=350,
    showvalue=False,
    command=lambda x:chramtlabel.configure(
        text=f"Character Amount: {lenslider.get()}"
    ),
)

lenslider.grid(column=0,row=2,rowspan=True,sticky="nswe")

CTkButton(
    mainfrm, 
    text="Generate", 
    command=genpassword
).grid(
    column=0,
    row=1
)


CTkLabel(settfrm,text="Word to include in password",font=("Arial",10,"bold")).grid(sticky="w")
wordentry.grid(sticky="w")


genpassword()#Generate a password that will be displyed when the program is run

root.mainloop()
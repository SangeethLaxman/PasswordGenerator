from tkinter import *
from tkinter import ttk
import random
import string 
import zxcvbn #Password Strength Estimation Library by Dropbox


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
root = Tk()
root.title("Password Generator")
root.geometry("500x500")


#init frames
fullroot = Frame(
    root, 
    background="#7D84B2"
)

mainfrm = Frame(
    fullroot,
    border=10,
    padx=30, 
    pady=30,
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
    width=400,
    height=250,
    background="#D9DBF1",
    text="Password Settings",
    font=("Arial",13,"bold"),
    relief="flat",
    highlightthickness=4,
    highlightbackground="#0D1B1E",
    labelanchor="n",
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
        Checkbutton(settfrm,text="Special Characters?"), #CheckBox
        BooleanVar(value=True) #Boolean Variable to be assigned to checkbox
    ],
    "upchar": [
        [x for x in string.ascii_uppercase], #List of characters
        Checkbutton(settfrm,text="Uppercase Characters?" ),#Checkbox
        BooleanVar(value=True) #Boolean Variable to be assigned to checkbox
        
    ],
    "lowchar": [
        [x for x in string.ascii_lowercase], #List of characters
        Checkbutton(settfrm,text="Lowercase Characters?",), #Checkbox
        BooleanVar(value=True) #Boolean Variable to be assigned to checkbox
    ],
    "numbers": [
        [str(x) for x in range(0,10)], #List of characters
        Checkbutton(settfrm,text="Numbers?"), #Checkbox
        BooleanVar(value=True) #Boolean Variable to be assigned to checkbox
    ]
}

#Warning Label
warninglabel=Label(
    settfrm,
    text="Minimum one checkbox should be enabled",
    fg="red",
    font=("Arial",7,"bold"),
    border=10,
    padx=1,
    pady=1,background="#D9DBF1"
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
                characters[i][1].config(state=DISABLED) #Disable the checkbox
        
        warninglabel.config(text="Minimum one checkbox should be enabled",)
        warninglabel.grid(column=0,row=9,sticky="w") #Display warning label
    
    else:
        for i in characters:
            characters[i][1].config(state=NORMAL) #Enable all checkboxes
        warninglabel.grid_forget() #Hide warning label


#Iterate through checkboxes and assign each one a property/grid them
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


strengthlabel = Label( #Label to display the password strength
    passfrm,
    text="Password Strength: None",
    font=("Arial",10,"bold"),
    bg="#11270B"
)
strengthlabel.grid()

def strengthcheck(pw: str):
    print("Checking password ", f"'{pw}'"," using zxcvbn...")
    result = zxcvbn.zxcvbn(pw) #Put the password through the zxcvbn's zxcvbn function and receive back a dictionary of results
    score = result["score"] #Obtain the score from the dictionary
    
    print("Password Score: ",score)
    print("Number of Guesses: ", result["guesses"])
    print("Time which will be taken to crack: ", result["crack_times_display"]["online_no_throttling_10_per_second"])
    strengthlabel.config(text=f"Password Strength: {strengths[score][0]}",
    fg=strengths[score][1])

passlabel = Label( #Label to display password
    passfrm,
    foreground="blue",
    font=("Arial",15,"bold"),
    background="#C3DBC5"
)
passlabel.grid()

copybtn = ttk.Button( #Button to copy password
    passfrm,
    text="Copy",
    command=lambda: root.clipboard_clear() or root.clipboard_append(passlabel.cget("text"))
)
copybtn.grid()

wordvar = StringVar() #Variable to store entry input

wordentry = Entry( #Entry widget
    settfrm,
    textvariable=wordvar
)
#wordvar.set("")


def genpassword():
    
    word = wordvar.get().strip()
    if len(word) >= lenslider.get():
        warninglabel.config(text="Word too long, \nplease enter a shorter word or increase password length",justify="left")
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


Label(settfrm, text="Password Length",font=("Arial",10,"bold"),bg="#D9DBF1").grid(column=0,row=1,sticky="w")

chramtlabel = Label(settfrm, text="Character Amount: 8",font=("Arial",6,"bold"),bg="#D9DBF1")
chramtlabel.grid(column=0,row=1,sticky="e")

lenslider = Scale(
    settfrm, 
    from_=8, 
    to=40, 
    orient=HORIZONTAL,
    sliderlength=10,
    length=350,
    showvalue=False,
    bg="#D9DBF1",
    command=lambda x:chramtlabel.config(
        text=f"Character Amount: {lenslider.get()}"
    ),
)

lenslider.grid(column=0,row=2,rowspan=True,sticky="nswe")

ttk.Button(
    mainfrm, 
    text="Generate", 
    command=genpassword
).grid(
    column=0,
    row=1
)


Label(settfrm,text="Word to include in password",font=("Arial",10,"bold"),bg="#D9DBF1").grid(sticky="w")
wordentry.grid(sticky="w")


genpassword()#Generate a password that will be displyed when the program is run

root.mainloop()
import os

from tkinter import * #GUI
from tkinter import ttk

import random
import string


import time # Time library to calculate time spent on generating password (debugging)
from customtkinter import * #Custom Tkinter Library for better UI
import colour #Colour library for color manipulation and processing
import zxcvbn #ZXCVBN Password Strength Estimation Library by Dropbox



set_default_color_theme("green")
set_appearance_mode("dark")

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
root.geometry("710x485")
root.resizable(False,False)


#init frames
fullroot = CTkFrame(
    root,
)

mainfrm = CTkFrame(
    fullroot,
    #fg_color="red"
    #width=500,
    #height=500
    #border_width=5,

)

passfrm = CTkFrame(
    mainfrm,
    #border_width=,
)

settfrm = CTkFrame(
    mainfrm, 
    #width=275,
    #height=250,
    #padx = 10,
    #text="Password Settings",
    border_width=5,
    #fg_color="red"
    #border_color= "#0D1B1E"
)

images = [
    PhotoImage(file="images/dark_mode.png"),
    PhotoImage(file="images/light_mode.png"),
]




mode_btn = CTkButton(
    mainfrm,
    width = 25,
    height = 25,
    #fg_color="transparent",
    image=PhotoImage(file="images/dark_mode.png"),
    text="",
    hover=True
)




def switch_appearance(): #Function to toggle between light and dark mode
    if get_appearance_mode() == "Dark":  #If current mode is dark
        set_appearance_mode("light") #Turn on light mode
        mode_btn.configure(image = images[1]) # Change Picture
    else:
        set_appearance_mode("dark") #Turn on light mode
        mode_btn.configure(image = images[0]) # Change Picture



mode_btn.configure(command=switch_appearance) #Link toggle button to the function


#grid the frames
fullroot.pack()
mainfrm.pack(anchor="w",expand=True,fill=BOTH,pady=(10,0))

CTkLabel( #Title Label
    mainfrm,
    font=("Arial",35,"bold"),
    text="Password Generator"
).grid(
    columnspan=2,
    pady=(10,0)
)


mode_btn.grid(
    row=0,
    column=1,
    sticky=E,
    padx = 20,
    pady=(10,0)
)


passfrm.grid(row=1,column=0,padx=30,sticky=NSEW,pady=10)
settfrm.grid(row=1,column=1,padx=10)



#Intialize Checkbox Dictionary
characters = {
    "special": [
        ["$","%","&","!","?","@","#","_","+","="], #List of characters
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
    font=("Arial",14,"bold"),
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
        
        warninglabel.configure(text="Atleast one checkbox should be enabled",)
        warninglabel.grid(column=0,row=9,sticky="w",padx=10, pady=10) #Display warning label
    
    else:
        for i in characters:
            characters[i][1].configure(state=NORMAL) #Enable all checkboxes
        warninglabel.grid_forget() #Hide warning label


#Iterate through checkboxes and assign each one a property/grid them
for j in characters:
    characters[j][1].grid(
        column=0,
        row=3+list(characters.keys()).index(j),
        sticky="w",
        padx=10,
        pady=5
    )
    
    characters[j][1].configure(
        variable=characters[j][2],
        command=validatecheckboxes,
    )


strengthlabel = CTkLabel( #Label to display the password strength
    passfrm,
    text="Password Strength: None",
    font=("Arial",20,"bold"),
    pady=10,
    corner_radius=5
    #padx=50
)




passentry = CTkTextbox( #Label to display password
    passfrm,
    #foreground="blue",
    font=("Arial",15,"bold"),
    #background="#C3DBC5",
)


def strengthcheck():
    temp = passentry.get("1.0","end-1c") #Gets the current text in the textbox
    passentry.delete("1.0","end") #Clears the textbox
    passentry.insert("0.0",temp.replace("\n",""),) #Adds the previous text except with no newline characters, preventing newlines to be created each time the user presses Enter

    pw = passentry.get("1.0","end-1c").strip() #Gets the current text from textbox and removes any trailing whitespace
    
    print("Checking password ", f"'{pw}'"," using zxcvbn...") 
    result = zxcvbn.zxcvbn(pw) #Put the password through the zxcvbn's zxcvbn function and receive back a dictionary of results
    score = result["score"] #Obtain the score from the dictionary
    
    print("Password Score: ",score)
    print("Number of Guesses: ", result["guesses"])
    print("Time which will be taken to crack: ", result["crack_times_display"]["online_no_throttling_10_per_second"])

    strengthlabel.configure(
        text=f"Password Strength:\n {strengths[score][0]}",
        text_color=strengths[score][1], #Change text color
        fg_color= colour.Color(strengths[score][1],luminance=0.1).hex_l #Utilize colour lib to make a darker version of the strength color
    )




passentry.grid(padx=10,pady=10) #TextBox for Password

passentry.bind("<Return>", lambda event: strengthcheck())

def clipreplace(text:str):
    root.clipboard_clear() #Clear the Clipboard
    root.clipboard_append(text) #Add the text to the clipboard

CTkButton( #Create a clipboard button
    passfrm,
    width = 25,
    height = 25,
    image = PhotoImage(file="images/copy.png"),
    text = "",
    hover=True,
    command=lambda: clipreplace(passentry.get("1.0","end-1c").strip()) #Gets the current text in the password textbox and puts it through the function
).grid(
    sticky=SE,pady=(0,10)
)

strengthlabel.grid(sticky=NSEW,padx=(10,10),ipadx=7)

wordvar = StringVar() #Variable to store entry input

wordentry = CTkEntry( #Entry widget
    settfrm,
    textvariable=wordvar
)
#wordvar.set("")


def genpassword():
    print("----------------------------------------------------")
    print("Generating Password!")
    print("Desired Length of Password: ", sliderval.get())
    start_time = time.time() #Get time before generation

    word = wordvar.get().strip() #Gets the word and removes any trailing whitespace

    if len(word) >= sliderval.get(): #Checks if the word is larger than the password length
        warninglabel.configure(text="Word too long, \nPlease enter a shorter word \nor increase password length",justify="left")
        warninglabel.grid(column=0,row=9,sticky="w",padx=10, pady=10)
        return None # return none, ending the function
    else:
        warninglabel.grid_forget() # Hide the warning label
    

    validchars = [] #Creates a empty list,
    for i in characters:
        if characters[i][2].get(): #Checks if the corresponding set of characters have their checkbox enabled,
            validchars +=characters[i][0] #if so, add to the empty list

    pw ="" #Empty string
    
    for j in range(int(sliderval.get())-len(word)-1): #Repeats for the length of slidervalue minus the length of the word
        randindex = random.randint(0,len(validchars)-1)
        print("Random Chosen Index: ",randindex) #Chooses a random index in the validchars list
        pw += validchars[randindex] #Adds the corresponding item to the password
        print("Password Progress: ",pw) 

    if word != "":
        if bool(random.getrandbits(1)): #Get a random bit (1 or 0) and convert it to a boolean, random boolean
            print("Attaching Word to: FRONT")
            pw = word + "-" + pw #Adds it to the front of the word with a hyphen seperating it
        else:
            print("Attaching Word to: BACK")
            pw += '-' + word #Adds it to the back of the word with a hyphen seperating it
    
    end_time = time.time() #Gets the time after generation
    print("Password generated in: ", (end_time-start_time)*1000, "ms") #Prints the total time taken (purely for testing performance)
    passentry.delete("1.0","end-1c") #Clear password textbox
    passentry.insert("0.0",pw) #Insert new password into textbox
    print("Final Password:", pw)

    strengthcheck() #Test password strength


CTkLabel(settfrm, text="Password Length",font=("Arial",20,"bold")).grid(column=0,row=1,sticky="w",padx=10,pady=10)

chramtlabel = CTkLabel(settfrm, text="Character Amount: 8",font=("Arial",14,"bold"))
chramtlabel.grid(column=0,row=1,sticky="e",padx=10)
sliderval = IntVar(value=8)

CTkSlider(
    settfrm, 
    variable=sliderval,
    from_=8, 
    to=40,
    width=350,
    number_of_steps=32,
    command=lambda x : chramtlabel.configure(
        text=f"Character Amount: {sliderval.get()}"
    ),
).grid(
    column=0,
    row=2,
    rowspan=True,
    sticky="nswe",
    padx=10,
    pady=5
)

CTkButton(
    passfrm, 
    text="Generate", 
    command=genpassword,
    hover=True
).grid(
    column=0,
    pady=10
)

CTkLabel(settfrm,text="Word to include in password",font=("Arial",20,"bold")).grid(sticky="w",padx=10)
wordentry.grid(sticky="w",padx=10,pady=10)

genpassword()#Generate a password that will be displyed when the program is run

root.mainloop()
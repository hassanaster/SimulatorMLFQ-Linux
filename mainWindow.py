#----------------------------------------------------------------------------------
# Main Window: When the simulator started this is the first GUI interface displayed.
# This window take the initial data: # of Queue and # of Jobs (max 3 of each data)
#----------------------------------------------------------------------------------

#----------------------------------------------------------------------------------
# @Authors: Miriam Arango, Luisa Arboleda, Yeison Quinto
# @Version: Version 1.0
# @Creation Date: 26 - 12 - 2020
# @Last modification Date: 10 - 01 - 2021
#----------------------------------------------------------------------------------


import tkinter as tk
import tkinter.messagebox as mb
import View.shareGraphicFunctions as sgf
import tkinter.ttk as cb
from View.basicDataWindow import *
from Model.JobClass import *

#----------------------------------------------------------------------------------
# Functions to create the events for each button
#----------------------------------------------------------------------------------
#Event for OK button on click
def eventOkButton():
    #Instance from Jobs created
    jobA=Job()
    jobB=Job()
    jobC=Job()

    queue=quantityQueue.get()
    job=quantityJob.get()
    if (quantityJob.get()==""):
        job="0"
    if (quantityQueue.get()==""):
        queue="0"
    if((int(job)>=1 and int(job)<=3) and (int(queue)>=1 and int(queue)<=3)):
        #Quantity for the jobs created
        job=int(job)
        queue=int(queue)
        if job>=1:
            jobA.setQuantity(job)
        if job>=2:
            jobB.setQuantity(job)
        if job==3:
            jobC.setQuantity(job)
        #print(jobA.getQuantity(), jobB.getQuantity(), jobC.getQuantity(), sep=",")
        drawBasicDataWindow(jobA, jobB, jobC, queue, quantumTime, periodTime, mainWindow)
    else:
        mb.showerror(title="Error", message="Numbers admitted for both fields are 1, 2 or 3, please take a look.")

#---Start the main program
#root window
#We create the root window here to be able to call StringVar() function
mainWindow=tk.Tk()
mainWindow.title("MLFQ Simulation - Main window")
mainWindow.resizable(False,False)
#mainWindow.iconbitmap("icon.ico")
mainWindow.config(bg='#EAF6F5')
mainWindow.geometry('400x250+500+350')

#variables from fields I need to recover for this windows, mainWindow.
quantityQueue=tk.StringVar()
quantityJob=tk.StringVar()

#variables from fields I need to recover from Basic Data Window
quantumTime=tk.StringVar()
periodTime=tk.StringVar()

#Widgets creation
#Labels
tk.Label(mainWindow,text="Jobs & Queue", font=("Arial", 18), bg='#EAF6F5').grid(row=0, column=0, columnspan=2, sticky="W", padx=20, pady=10)
tk.Label(mainWindow, text="Queue quantity*:", font=("Arial", 14), bg='#EAF6F5').grid(row=1, column=0, sticky="E", padx=10, pady=10)
tk.Label(mainWindow, text="Jobs quantity*:", font=("Arial", 14), bg='#EAF6F5').grid(row=2, column=0, sticky="E", padx=10, pady=10)
tk.Label(mainWindow, text="Maximum quantity for both fields is 3", font=("Arial", 16), bg='#EAF6F5', fg="gray").grid(row=4, column=0, columnspan=2, padx=10, pady=10)

#Inputs
validation = mainWindow.register(sgf.onlyNumbers)

queueField=tk.Entry(mainWindow, font=("Arial"), fg="gray", textvariable=quantityQueue, validate="key", validatecommand=(validation, '%S'))
queueField.grid(row=1, column=1, sticky="W", padx=5, pady=5)

jobField=tk.Entry(mainWindow, font=("Arial"), fg="gray", textvariable=quantityJob, validate="key", validatecommand=(validation, '%S'))
jobField.grid(row=2, column=1, sticky="W", padx=5, pady=5)

#Buttons
okButton=tk.Button(mainWindow, text="OK", width=10, height=2, font=("Arial"), command=eventOkButton)
okButton.grid(row=3, column=0, padx=10, pady=10)

cancelButton=tk.Button(mainWindow, text="CLOSE", width=10, height=2, font=("Arial"), command=lambda:sgf.eventCloseButton(mainWindow))
cancelButton.grid(row=3, column=1, padx=10, pady=10)

#Should be always in the end of the file
mainWindow.mainloop()
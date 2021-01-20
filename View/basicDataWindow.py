#----------------------------------------------------------------------------------
# Basic Data Window: After get how many jobs and periods is needed other basic information for each quantum
# This window take the basic data: priority of each quantum, quantum time, and period time
#----------------------------------------------------------------------------------

#----------------------------------------------------------------------------------
# @Authors: Miriam Arango, Luisa Arboleda, Yeison Quinto
# @Version: Version 1.0
# @Creation Date: 02 - 01 - 2021
# @Last modified date: 11 - 01 - 2021
#----------------------------------------------------------------------------------

import tkinter as tk
import tkinter.messagebox as mb
#This module is to display combobox
import tkinter.ttk as cb
import View.shareGraphicFunctions as sgf
from View.aditionalDataWindows import *

#----------------------------------------------------------------------------------
# Functions to create the events for each button
#----------------------------------------------------------------------------------

#Event for OK button on click - Aditional data window or simulation window will be open
def eventOkBWButton(jobA, jobB, jobC, queueQuantity, quantumTime, periodTime, jobAComboBox, jobBComboBox, jobCComboBox, jobTwoOptionsComboBox, arrivalJobA, arrivalJobB, arrivalJobC, runTimeJobA, runTimeJobB, runTimeJobC, ioJobC, ioJobB, ioJobA, startIoJobC, startIoJobB, startIoJobA, basicDataWindow, mainWindow):
    quantum=quantumTime.get()
    period=periodTime.get()
    priorityA=jobAComboBox.current()
    priorityB=jobBComboBox.current()
    priorityC=jobCComboBox.current()
    aditionalW=jobTwoOptionsComboBox.current()
    if quantum=="0" or period=="" or quantum=="":
        mb.showinfo(title="Info", message="If there is some fields empty (quantum or period 'S') it will be replaced quantum = 1, S=0.")
    if (quantum==""):
        quantum="1"
    if (period==""):
        period="0"
    quantum=(int(quantum))
    period=(int(period))
    jobA.setPriority(priorityA+1)
    jobB.setPriority(priorityB+1)
    jobC.setPriority(priorityC+1)
    #print("Las prioridades del job", jobA.getPriority(), jobB.getPriority(),jobC.getPriority(), sep=",")
    if aditionalW == 1:
        drawSimulationWindow(jobA, jobB, jobC, queueQuantity, quantum, period, basicDataWindow, mainWindow)
    else:
        drawAditionalDataWindow(jobA, jobB, jobC, queueQuantity, quantum, period, arrivalJobA, arrivalJobB, arrivalJobC, runTimeJobA, runTimeJobB, runTimeJobC, ioJobC, ioJobB, ioJobA, startIoJobC, startIoJobB, startIoJobA, basicDataWindow, mainWindow)
        
#Disable combox JobB when user just chose 1 job to run
def disbledEnabledComboBoxB(quantity):
    if quantity == 1:
        return "disabled"
    return "readonly"

#Disable combox JobC when user just chose max 2 jobs to run
def disbledEnabledComboBoxC(quantity):
    if quantity == 1 or quantity == 2:
        return "disabled"
    return "readonly"

#Function wich draw the window for the basic data
def drawBasicDataWindow(jobA, jobB, jobC, queueQuantity, quantumTime, periodTime, mainWindow):
    mainWindow.withdraw()
    #Function basicWindowWithdraw
    basicDataWindow=tk.Toplevel()
    basicDataWindow.title("MLFQ Simulation - Basic Data Window")
    basicDataWindow.resizable(False,False)
    basicDataWindow.config(bg='#EAF6F5')
    basicDataWindow.geometry('500x500+500+150')

    #variables from fields I need to recover from Aditional Data window
    arrivalJobA=tk.StringVar()
    runTimeJobA=tk.StringVar()
    ioJobA=tk.StringVar()
    startIoJobA=tk.StringVar()
        
    arrivalJobB=tk.StringVar()
    runTimeJobB=tk.StringVar()
    ioJobB=tk.StringVar()
    startIoJobB=tk.StringVar()

    arrivalJobC=tk.StringVar()
    runTimeJobC=tk.StringVar()
    ioJobC=tk.StringVar()
    startIoJobC=tk.StringVar()

    #Create the widgets and add them in a grid to add all the widgets needed in the right places
    #Labels
    tk.Label(basicDataWindow,text="Jobs, period & Basic data", font=("Arial", 18), bg='#EAF6F5').grid(row=0, column=0, sticky="W", columnspan=2, padx=10, pady=20)
    tk.Label(basicDataWindow,text="Priority", font=("Arial", 10), bg='#EAF6F5').grid(row=1, column=1, sticky="W", padx=20, pady=1)
    tk.Label(basicDataWindow,text="Job A:*", font=("Arial", 14), bg='#EAF6F5').grid(row=2, column=0, sticky="E", padx=10, pady=10)
    jobBLabel=tk.Label(basicDataWindow,text="Job B:*", font=("Arial", 14), bg='#EAF6F5')
    jobBLabel.grid(row=3, column=0, sticky="E", padx=10, pady=10)
    jobCLabel=tk.Label(basicDataWindow,text="Job C:*", font=("Arial", 14), bg='#EAF6F5')
    jobCLabel.grid(row=4, column=0, sticky="E", padx=10, pady=10)
    tk.Label(basicDataWindow,text="----------------------------------------------------------------------------------------", font=("Arial", 12), bg='#EAF6F5', fg="gray").grid(row=5, column=0, sticky="W",columnspan=2, padx=40)
    tk.Label(basicDataWindow,text="Quantum time:*", font=("Arial", 14), bg='#EAF6F5').grid(row=6, column=0, sticky="E", padx=10, pady=10)
    tk.Label(basicDataWindow,text="Period time 'S':*", font=("Arial", 14), bg='#EAF6F5').grid(row=7, column=0, sticky="E", padx=10, pady=10)
    tk.Label(basicDataWindow,text="Do you want to add more", font=("Arial", 12), bg='#EAF6F5').grid(row=8, column=0, sticky="E", padx=10)
    tk.Label(basicDataWindow,text="information for the simulation?", font=("Arial", 12), bg='#EAF6F5').grid(row=9, column=0, sticky="E", padx=10)

    #Inputs or fields
    validation = basicDataWindow.register(sgf.onlyNumbers)

    quantumField=tk.Entry(basicDataWindow, font=("Arial"), fg="gray", width=17, textvariable=quantumTime, validate="key", validatecommand=(validation, '%S'))
    quantumField.grid(row=6, column=1, sticky="W", padx=20, pady=10)

    periodField=tk.Entry(basicDataWindow, font=("Arial"), fg="gray", width=17, textvariable=periodTime, validate="key", validatecommand=(validation, '%S'))
    periodField.grid(row=7, column=1, sticky="W", padx=20, pady=10)

    #ComboBox
    options=["Low", "Medium", "High"]
    twoOptions=["Yes", "No"]
    jobAComboBox=cb.Combobox(basicDataWindow, width=14, state="readonly")
    jobAComboBox.grid(row=2, column=1, sticky="W", padx=20, pady=10)
    jobAComboBox['values']=options
    jobAComboBox.current(newindex=2)

    jobBComboBox=cb.Combobox(basicDataWindow, width=14, state=disbledEnabledComboBoxB(jobA.getQuantity()))
    jobBComboBox.grid(row=3, column=1, sticky="W", padx=20, pady=10)
    jobBComboBox['values']=options
    jobBComboBox.current(newindex=2)

    jobCComboBox=cb.Combobox(basicDataWindow, width=14, state=disbledEnabledComboBoxC(jobA.getQuantity()))
    jobCComboBox.grid(row=4, column=1, sticky="W", padx=20, pady=10)
    jobCComboBox['values']=options
    jobCComboBox.current(newindex=2)

    jobTwoOptionsComboBox=cb.Combobox(basicDataWindow, width=14, state="readonly")
    jobTwoOptionsComboBox.grid(row=8, column=1, sticky="W", padx=20, pady=10, rowspan=2)
    jobTwoOptionsComboBox['values']=twoOptions
    jobTwoOptionsComboBox.current(newindex=0)
    
    #Buttons
    okButtonBW=tk.Button(basicDataWindow, text="OK", width=10, height=2, font=("Arial"), command=lambda:eventOkBWButton(jobA, jobB, jobC, queueQuantity, quantumTime, periodTime, jobAComboBox, jobBComboBox, jobCComboBox, jobTwoOptionsComboBox, arrivalJobA, arrivalJobB, arrivalJobC, runTimeJobA, runTimeJobB, runTimeJobC, ioJobC, ioJobB, ioJobA, startIoJobC, startIoJobB, startIoJobA, basicDataWindow, mainWindow))
    okButtonBW.grid(row=10, column=0, sticky="E", padx=10, pady=20)

    cancelButtonBW=tk.Button(basicDataWindow, text="CLOSE", width=10, height=2, font=("Arial"), command=lambda:sgf.eventCloseButton(mainWindow))
    cancelButtonBW.grid(row=10, column=1, sticky="W", padx=10, pady=20)
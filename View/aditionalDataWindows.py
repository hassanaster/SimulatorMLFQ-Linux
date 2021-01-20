#----------------------------------------------------------------------------------
# Aditional Data Window: After get basic date from user, user is avalaible to add aditional data for the simulation
# This window take the additional data: arrival time, run time, I/O Time, How often start I/O process*
#----------------------------------------------------------------------------------

#----------------------------------------------------------------------------------
# @Authors: Miriam Arango, Luisa Arboleda, Yeison Quinto
# @Version: Version 1.0
# @Creation Date: 03 - 01 - 2021
# @Last modify Date: 12 - 01 - 2021
#----------------------------------------------------------------------------------

import tkinter as tk
import tkinter.messagebox as mb
import View.shareGraphicFunctions as sgf
from View.simulationWindows import *

#----------------------------------------------------------------------------------
# Functions to create the events for each button
#----------------------------------------------------------------------------------

#Event for Start button on click
def eventstartButton(jobA, jobB, jobC, queueQuantity, quantum, period, arrivalJobAField, arrivalJobBField, arrivalJobCField, runTimeJobAField, runTimeJobBField, runTimeJobCField, ioJobCField, ioJobBField, ioJobAField, startIoJobCField, startIoJobBField, startIoJobAField, aditionalDataWindow, mainWindow):
    #Setting the data for JobA
    if jobA.getQuantity()>=1:
        
        if arrivalJobAField.get()=="":
            jobA.setArrivalTime(0)
        else:
            jobA.setArrivalTime(int(arrivalJobAField.get()))
        
        if runTimeJobAField.get()=="":
            jobA.setRunTime(0)
        else:
            jobA.setRunTime(int(runTimeJobAField.get()))

        if ioJobAField.get()=="":
            jobA.setIoTime(0)
        else:
            jobA.setIoTime(int(ioJobAField.get()))

        if startIoJobAField.get()=="":
            jobA.setStartIoTime(0)
        else:
            jobA.setStartIoTime(int(startIoJobAField.get()))

    #Setting the data for JobB
    if jobA.getQuantity()>=2 :

        if arrivalJobBField.get()=="":
            jobB.setArrivalTime(0)
        else:
            jobB.setArrivalTime(int(arrivalJobBField.get()))

        if runTimeJobBField.get()=="":
            jobB.setRunTime(0)
        else:
            jobB.setRunTime(int(runTimeJobBField.get()))

        if ioJobBField.get()=="":
            jobB.setIoTime(0)
        else:
            jobB.setIoTime(int(ioJobBField.get()))

        if startIoJobBField.get()=="":
            jobB.setStartIoTime(0)
        else:
            jobB.setStartIoTime(int(startIoJobBField.get()))

    #Setting the data for JobC
    if jobA.getQuantity()==3 :

        if arrivalJobCField.get()=="":
            jobC.setArrivalTime(0)
        else:
            jobC.setArrivalTime(int(arrivalJobCField.get()))

        if runTimeJobCField.get()=="":
            jobC.setRunTime(0)
        else:
            jobC.setRunTime(int(runTimeJobCField.get()))

        if ioJobCField.get()=="":
            jobC.setIoTime(0)
        else:
            jobC.setIoTime(int(ioJobCField.get()))

        if startIoJobCField.get()=="":
            jobC.setStartIoTime(0)
        else:
            jobC.setStartIoTime(int(startIoJobCField.get()))
    drawSimulationWindow(jobA, jobB, jobC, queueQuantity, quantum, period, aditionalDataWindow, mainWindow)
        
#Disable Fields JobB when user just chose 1 job to run - combobox JobB
def disbledEnabledFieldsB(quantity):
    if quantity == 1:
        return "disabled"
    return "normal"

#Disable Field JobC when user just chose max 2 jobs to run - combox JobC
def disbledEnabledFieldsC(quantity):
    if quantity == 1 or quantity == 2:
        return "disabled"
    return "normal"

#Function wich draw the window for aditional Data
def drawAditionalDataWindow(jobA, jobB, jobC, queueQuantity, quantum, period, arrivalJobA, arrivalJobB, arrivalJobC, runTimeJobA, runTimeJobB, runTimeJobC, ioJobC, ioJobB, ioJobA, startIoJobC, startIoJobB, startIoJobA, basicDataWindow, mainWindow):
    basicDataWindow.withdraw()
    #Window or root: First we should create the root or window
    aditionalDataWindow=tk.Toplevel()
    aditionalDataWindow.title("MLFQ Simulation - Aditional Data Window")
    aditionalDataWindow.resizable(False,False)
    aditionalDataWindow.config(bg='#EAF6F5')
    aditionalDataWindow.geometry('850x400+500+150')

    #Create the widgets and add them in a grid to add all the widgets needed in the right places
    #Labels
    tk.Label(aditionalDataWindow,text="Additional Data", font=("Arial", 18), bg='#EAF6F5').grid(row=0, column=0, sticky="W", columnspan=5, padx=10, pady=20)
    tk.Label(aditionalDataWindow,text="Start Time", font=("Arial", 14), bg='#EAF6F5').grid(row=1, column=1, sticky="W", padx=10, pady=10)
    tk.Label(aditionalDataWindow,text="Run Time", font=("Arial", 14), bg='#EAF6F5').grid(row=1, column=2, sticky="W", padx=10, pady=10)
    tk.Label(aditionalDataWindow,text="I/O Time", font=("Arial", 14), bg='#EAF6F5').grid(row=1, column=3, sticky="W", padx=10, pady=10)
    tk.Label(aditionalDataWindow,text="I/O process frequency*", font=("Arial", 10), bg='#EAF6F5').grid(row=1, column=4, sticky="W", padx=10, pady=10)
    tk.Label(aditionalDataWindow,text="Job A:", font=("Arial", 14), bg='#EAF6F5').grid(row=2, column=0, sticky="E", padx=10, pady=10)
    tk.Label(aditionalDataWindow,text="Job B:", font=("Arial", 14), bg='#EAF6F5').grid(row=3, column=0, sticky="E", padx=10, pady=10)
    tk.Label(aditionalDataWindow,text="Job C:", font=("Arial", 14), bg='#EAF6F5').grid(row=4, column=0, sticky="E", padx=10, pady=10)

    tk.Label(aditionalDataWindow,text="*In this field, this value is taking into account if I/O time field has a value", font=("Arial", 12), bg='#EAF6F5', fg="gray").grid(row=6, column=0, sticky="W", padx=200, columnspan=5)

    #Inputs or fields
    validation = basicDataWindow.register(sgf.onlyNumbers)

    #JOB A
    arrivalJobAField=tk.Entry(aditionalDataWindow, font=("Arial"), fg="gray", width=12, textvariable=arrivalJobA, validate="key", validatecommand=(validation, '%S'))
    arrivalJobAField.grid(row=2, column=1, sticky="W", padx=10, pady=10)

    runTimeJobAField=tk.Entry(aditionalDataWindow, font=("Arial"), fg="gray", width=12, textvariable=runTimeJobA, validatecommand=(validation, '%S'))
    runTimeJobAField.grid(row=2, column=2, sticky="W", padx=10, pady=10)

    ioJobAField=tk.Entry(aditionalDataWindow, font=("Arial"), fg="gray", width=12, textvariable=ioJobA,  validate="key", validatecommand=(validation, '%S'))
    ioJobAField.grid(row=2, column=3, sticky="W", padx=10, pady=10)

    startIoJobAField=tk.Entry(aditionalDataWindow, font=("Arial"), fg="gray", width=12, textvariable=startIoJobA, validate="key", validatecommand=(validation, '%S'))
    startIoJobAField.grid(row=2, column=4, sticky="W", padx=10, pady=10)

    #JOB B
    arrivalJobBField=tk.Entry(aditionalDataWindow, font=("Arial"), fg="gray", width=12, validate="key", textvariable=arrivalJobB, validatecommand=(validation, '%S'), state=disbledEnabledFieldsB(jobA.getQuantity()))
    arrivalJobBField.grid(row=3, column=1, sticky="W", padx=10, pady=10)

    runTimeJobBField=tk.Entry(aditionalDataWindow, font=("Arial"), fg="gray", width=12, validate="key", textvariable=runTimeJobB, validatecommand=(validation, '%S'), state=disbledEnabledFieldsB(jobA.getQuantity()))
    runTimeJobBField.grid(row=3, column=2, sticky="W", padx=10, pady=10)

    ioJobBField=tk.Entry(aditionalDataWindow, font=("Arial"), fg="gray", width=12, validate="key", textvariable= ioJobB, validatecommand=(validation, '%S'), state=disbledEnabledFieldsB(jobA.getQuantity()))
    ioJobBField.grid(row=3, column=3, sticky="W", padx=10, pady=10)

    startIoJobBField=tk.Entry(aditionalDataWindow, font=("Arial"), fg="gray", width=12, validate="key", textvariable=startIoJobB, validatecommand=(validation, '%S'), state=disbledEnabledFieldsB(jobA.getQuantity()))
    startIoJobBField.grid(row=3, column=4, sticky="W", padx=10, pady=10)

    #JOB C
    arrivalJobCField=tk.Entry(aditionalDataWindow, font=("Arial"), fg="gray", width=12, validate="key", textvariable=arrivalJobC, validatecommand=(validation, '%S'), state=disbledEnabledFieldsB(jobA.getQuantity()))
    arrivalJobCField.grid(row=4, column=1, sticky="W", padx=10, pady=10)

    runTimeJobCField=tk.Entry(aditionalDataWindow, font=("Arial"), fg="gray", width=12, validate="key", textvariable=runTimeJobC, validatecommand=(validation, '%S'), state=disbledEnabledFieldsC(jobA.getQuantity()))
    runTimeJobCField.grid(row=4, column=2, sticky="W", padx=10, pady=10)

    ioJobCField=tk.Entry(aditionalDataWindow, font=("Arial"), fg="gray", width=12, validate="key", textvariable=ioJobC, validatecommand=(validation, '%S'), state=disbledEnabledFieldsC(jobA.getQuantity()))
    ioJobCField.grid(row=4, column=3, sticky="W", padx=10, pady=10)

    startIoJobCField=tk.Entry(aditionalDataWindow, font=("Arial"), fg="gray", width=12, validate="key", textvariable=startIoJobC, validatecommand=(validation, '%S'), state=disbledEnabledFieldsC(jobA.getQuantity()))
    startIoJobCField.grid(row=4, column=4, sticky="W", padx=10, pady=10)


    #Buttons
    startButton=tk.Button(aditionalDataWindow, text="OK", width=10, height=2, font=("Arial"), command=lambda:eventstartButton(jobA, jobB, jobC, queueQuantity, quantum, period, arrivalJobA, arrivalJobB, arrivalJobC, runTimeJobA, runTimeJobB, runTimeJobC, ioJobC, ioJobB, ioJobA, startIoJobC, startIoJobB, startIoJobA, aditionalDataWindow, mainWindow))
    startButton.grid(row=5, column=0, sticky="E", padx=30, pady=20, columnspan=3)

    closeButtonAW=tk.Button(aditionalDataWindow, text="CLOSE", width=10, height=2, font=("Arial"), command=lambda:sgf.eventCloseButton(mainWindow))
    closeButtonAW.grid(row=5, column=3, sticky="W", padx=10, pady=20, columnspan=2)
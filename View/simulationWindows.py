#----------------------------------------------------------------------------------
# Simulation Window: After get all data needed, user is avalaible to simulate MFLQ 
# This window show graphic the simulation in miliseconds how MFLQ works
#----------------------------------------------------------------------------------

#----------------------------------------------------------------------------------
# @Authors: Miriam Arango, Luisa Arboleda, Yeison Quinto
# @Version: Version 1.0
# @Creation Date: 04 - 01 - 2021
# @Last modify Date: 17 - 01 - 2021
#----------------------------------------------------------------------------------

import tkinter as tk
import tkinter.messagebox as mb
import View.shareGraphicFunctions as sgf
from View.resultWindows import *
from Controller.mlfq import *
import time

#----------------------------------------------------------------------------------
# Functions to create the events for each button
#----------------------------------------------------------------------------------
timeList=[]
jobList=[]
queueList=[]
tiempo=0
pause=False
avgResponse=0.0
avgTurnAroundTime=0.0
resultado=''
def drawEmpty(simulationWindow):
    for x in range(3):
        for y in range(100):
            emptyLabelDraw= tk.Label(simulationWindow, bg='#EAF6F5', width=1, height=3)
            emptyLabelDraw.grid(row=x+3, column=y+1)

def drawProcess(timeList, jobList, queueList, simulationWindow, entrytime):
    global tiempo
    
    for k, data in enumerate(queueList):
        
        entrytime.set(tiempo)
        
        if data==2:
            x=3
        elif data==1:
            x=4
        else:
            x=5
        y=timeList[k]+1
        if jobList[k]==0:
            #print("Entre al primer JOB: ", " y: ", y, " x: ", x)
            jobALabel= tk.Label(simulationWindow, bg='#CB8665', width=1, height=2)
            jobALabel.grid(row=x, column=y)
        elif jobList[k]==1:
            #print("Entre al segundo JOB: ", " y: ", y, " x: ", x)
            jobBLabel= tk.Label(simulationWindow, bg='#FDBCB4', width=1, height=2)
            jobBLabel.grid(row=x, column=y)
        elif jobList[k]==2:
            #print("Entre al tercer JOB: ", " y: ", y, " x: ", x)
            jobCLabel= tk.Label(simulationWindow, bg='#E6D690', width=1, height=2)
            jobCLabel.grid(row=x, column=y)
        elif jobList[k]==4:
            ioLabel= tk.Label(simulationWindow, bg="gray", width=1, height=2)
            ioLabel.grid(row=x, column=y, pady=2)
        else:
            emptyLabel= tk.Label(simulationWindow, bg='blue', width=1, height=2)
            emptyLabel.grid(row=x, column=y)
        tiempo+=1
        if tiempo==101:
            break
        
    if len(timeList)<100:
        for y in range(len(timeList),100-len(timeList)):
            emptyLabelDraw= tk.Label(simulationWindow, bg='#EAF6F5', width=1, height=3)
            emptyLabelDraw.grid(row=x, column=y)
         
    #How to manage I/O process

#Function for Pause the simulation
def eventPauseButton():
    global tiempo
    tiempo-=1
    print(tiempo)
    time.sleep(5)
    #mb.showinfo(title="Pause Button", message="Estoy en el boton de pausa")
   
        
#Function for Start the simulation after pause, or since the begining
def eventStartButtonSW(jobA, jobB, jobC, queueQuantity, quantum, period, simulationWindow, entrytime,button):
    global avgTurnAroundTime
    global avgResponse
    global resultado
    enabled(button)
    #Taking Data
    #---This is just for now because this is additional data recover in the aditional windows
    #jobA.setRunTime(30)
    #jobB.setRunTime(20)
    #jobC.setRunTime(50)

    #Create a JobList to execute the scheduler and the list to draw the graphic
    joblist=[]
    joblist.append(jobA)
    joblist.append(jobB)
    joblist.append(jobC)
    #print(joblist[0].getQuantity(), sep=",")
    
    #print("Cantidad de colas: ", queueQuantity, "Periodo S: ", period, "Quantum: ", quantum, sep=',')
    
    #Executing the scheduler
    scheduler = mlfq()
    resultado = scheduler.RunMLFQ(joblist, queueQuantity, period, quantum) #numero de cuotas, S y quantum 

    #Create the file to capture the result
    scheduler.statistics()
    scheduler.infGrafica(timeList, jobList, queueList)
    avgTurnAroundTime=scheduler.getTurnAroundAvg()
    avgResponse=scheduler.getResponseTimeAvg()

    #print(timeList[:])
    #print(jobList[:])
    #print(queueList[:])
    #Draw processess
    drawProcess(timeList, jobList, queueList, simulationWindow, entrytime)
    

    #---After results we have to call the function wich draw the simulation with the pause, and finish button 

def enabled(button):
    button['state']='normal'

#Function to finish the simulation and display the final graphic
def eventFinishButton(button):
    button['state']=tk.NORMAL

#Function for Result button, to display window result
def eventResultButton(jobA, jobB, jobC, simulationWindow, mainWindow):
    global avgResponse
    global avgTurnAroundTime
    global resultado
    drawResultWindow(jobA, jobB, jobC, simulationWindow, mainWindow, timeList, jobList, queueList, avgResponse, avgTurnAroundTime,resultado)

#Function to draw Simulation Window
def drawSimulationWindow(jobA, jobB, jobC, queueQuantity, quantum, period, aditionalDataWindow, mainWindow):
    aditionalDataWindow.withdraw()
    simulationWindow=tk.Toplevel()
    simulationWindow.title("MLFQ Simulation - Simulation Window")
    simulationWindow.resizable(False,False)
    simulationWindow.config(bg='#EAF6F5')
    simulationWindow.geometry('1550x650+30+150')

    entrytime=tk.StringVar()
    #Create the widgets and add them in a grid to add all the widgets needed in the right places
    #Labels
    tk.Label(simulationWindow,text="Simulation MLFQ", font=("Arial", 18), bg='#EAF6F5').grid(row=0, column=0, sticky="W", columnspan=100, pady=10)
    tk.Label(simulationWindow,text="Counter(ms):", font=("Arial", 14), bg='#EAF6F5').grid(row=1, column=0, sticky="E", pady=10, columnspan=96)
    tk.Label(simulationWindow,text="Process Graph.", font=("Arial", 14), bg='#EAF6F5').grid(row=2, column=0, columnspan=100, pady=3)

    #Label q2, q1, q0
    tk.Label(simulationWindow, text="Q2", font=("Arial", 12), bg='#EAF6F5', width=0, height=2).grid(row=3, column=0, padx=2, sticky="S")
    tk.Label(simulationWindow, text="Q1", font=("Arial", 12), bg='#EAF6F5', width=0, height=2).grid(row=4, column=0, padx=2, sticky="S")
    tk.Label(simulationWindow, text="Q0", font=("Arial", 12), bg='#EAF6F5', width=0, height=2).grid(row=5, column=0, padx=2, sticky="S")

    tk.Label(simulationWindow, text="ms", font=("Arial", 12), bg='#EAF6F5', width=0, height=2).grid(row=6, column=0, padx=2, sticky="N")
    tk.Label(simulationWindow, text="0", font=("Arial", 8), bg='#EAF6F5',  width=0, height=2).grid(row=6, column=1, pady=2, sticky="N")
    tk.Label(simulationWindow, text="25", font=("Arial", 5), bg='#EAF6F5', width=0, height=2).grid(row=6, column=26, pady=2, sticky="N")
    tk.Label(simulationWindow, text="50", font=("Arial", 5), bg='#EAF6F5', width=0, height=2).grid(row=6, column=51, pady=2, sticky="N")
    tk.Label(simulationWindow, text="75", font=("Arial", 5), bg='#EAF6F5',  width=0, height=2).grid(row=6, column=76, pady=2, sticky="N")
    tk.Label(simulationWindow, text="100", font=("Arial", 3), bg='#EAF6F5', width=0, height=2).grid(row=6, column=100, pady=2, sticky="N")

    tk.Label(simulationWindow,text="Color for corresponding processes*", font=("Arial", 14), bg='#EAF6F5', fg="gray").grid(row=8, column=0, columnspan=100, pady=10)
    tk.Label(simulationWindow,text="Simulator management*", font=("Arial", 14), bg='#EAF6F5', fg="gray").grid(row=10, column=0, columnspan=100, pady=20)

    #Labels to pain the jobs execution
    #Draw JobA
    jobALabelDraw= tk.Label(simulationWindow, bg='#CB8665', width=0, height=2)
    jobALabelDraw.grid(row=9, column=30, pady=2)

    tk.Label(simulationWindow, text="JobA", font=("Arial", 12), bg='#EAF6F5', fg="gray").grid(row=9, column=31, pady=2, columnspan=9, sticky="W")

    #Draw JobB
    jobBLabelDraw= tk.Label(simulationWindow, bg='#FDBCB4', width=0, height=2)
    jobBLabelDraw.grid(row=9, column=41, pady=2)

    tk.Label(simulationWindow, text="JobB", font=("Arial", 12), bg='#EAF6F5', fg="gray").grid(row=9, column=42, pady=2, columnspan=9, sticky="W")

    #Draw JobC
    jobCLabelDraw= tk.Label(simulationWindow, bg='#E6D690', width=0, height=2)
    jobCLabelDraw.grid(row=9, column=52, pady=2)

    tk.Label(simulationWindow, text="JobC", font=("Arial", 12), bg='#EAF6F5', fg="gray").grid(row=9, column=53, pady=2, columnspan=9, sticky="W")

    #Draw I/O
    ioLabelDraw= tk.Label(simulationWindow, bg="gray", width=0, height=2)
    ioLabelDraw.grid(row=9, column=63, pady=2)

    tk.Label(simulationWindow, text="I/O", font=("Arial", 12), bg='#EAF6F5', fg="gray").grid(row=9, column=64, pady=2, columnspan=9, sticky="W")

    #Field - Entry
    resultCounter=tk.Entry(simulationWindow,text="Results", textvariable=entrytime ,font=("Arial", 12), bg='#EAF6F5', fg="gray", justify="right", width=6)
    resultCounter.grid(row=1, column=96, pady=10, sticky="E", columnspan=5)

    #Buttons
    pauseButton=tk.Button(simulationWindow, text="PAUSE", width=10, height=2, font=("Arial"), command=lambda:eventPauseButton(),state="disabled")
    pauseButton.grid(row=11, column=35, pady=20, columnspan=10)

    resultButton=tk.Button(simulationWindow, text="RESULT", width=10, height=2, font=("Arial"), state="disabled", command=lambda:eventResultButton(jobA, jobB, jobC, simulationWindow, mainWindow))
    resultButton.grid(row=12, column=40, pady=20, columnspan=10)

    finishButton=tk.Button(simulationWindow, text="FINISH", width=10, height=2, font=("Arial"), command=lambda:eventFinishButton(resultButton),state="disable")
    finishButton.grid(row=11, column=56, pady=20, columnspan=10)

    closeButtonSW=tk.Button(simulationWindow, text="CLOSE", width=10, height=2, font=("Arial"), command=lambda:sgf.eventCloseButton(mainWindow))
    closeButtonSW.grid(row=12, column=51, pady=20, columnspan=10)

    startButtonSW=tk.Button(simulationWindow, text="START", width=10, height=2, font=("Arial"), command=lambda:eventStartButtonSW(jobA, jobB, jobC, queueQuantity, quantum, period, simulationWindow, entrytime,resultButton))
    startButtonSW.grid(row=11, column=46, pady=20, columnspan=10)

    drawEmpty(simulationWindow)
   
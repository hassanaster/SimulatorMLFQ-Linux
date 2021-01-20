#----------------------------------------------------------------------------------
# Initial MLFQ Schedule: This MLFQ scheduler show results with initial random data and displays the result through console
#----------------------------------------------------------------------------------

#----------------------------------------------------------------------------------
# @Authors: Miriam Arango, Luisa Arboleda, Yeison Quinto
# @Version: Version 1.0
# @Date: 15 - 01 - 2021
# @Last modify Date: 16 - 01 - 2021
#----------------------------------------------------------------------------------
from Model.JobClass import *
import sys
import re

class mlfq():

    def __init__(self):

        #Initial Attributes
        self.__numQueues=0
        self.__quantum=0        #allotment has the same value
        self.__allotment=1
        self.__quantumList={}
        self.__allotmentList={}
        self.__numJobs=0
        self.__maxlen=100       #max run-time of a job
        self.__maxio=10        #max I/O frequency of a job 
        self.__S=0              #how often to boost the priority of all jobs back to high priority
        self.__iotime=5       #how long an I/O should last
        self.__stay=False       #reset and stay at same priority level when issuing I/O
        self.__iobump=False     #if specified, jobs that finished I/O move immediately to front of current queue       
        self.__joblist={}
        self.__hiQueue=0
        self.__ioDone={}
        self.__file=''
        #Added 17-01-2021
        self.__avgTurnAround=0.0
        self.__avgResponseTime=0.0
    
        
    # finds the highest nonempty queue
    # -1 if they are all empty
    def findQueue(self,queue):
        q = self.__hiQueue
        while q > 0:
            if len(queue[q]) > 0:
                return q
            q -= 1
        if len(queue[0]) > 0:
            return 0
        return -1

    #Error handle
    def Abort(self,str):
        sys.stderr.write(str + '\n')
        exit(1)

    #Set num of queues use by simulator
    def setnumQueues(self,numQueues):
        self.__numQueues=numQueues

    #Se llena la lista de quantum dependiendo de las colas que se usan
    def setQuantumList(self):
        for i in range(self.__numQueues):
            self.__quantumList[i] = int(self.__quantum)

    #Se llena la lista de allotment dependiendo de las colas que se usan
    def setAllotmentList(self):
        for i in range(self.__numQueues):
            self.__allotmentList[i] = int(self.__allotment)
    
    #Set of high priority queue, normally is the queue 2
    def setHiQueue(self):
        self.__hiQueue=self.__numQueues - 1

    #Tiene como parametros la lista de los trabajos para usarla internamente y fijar el numero de trabajos
    def setJobList(self,joblist):
        self.__numJobs=joblist[0].getQuantity()
        for i in range(self.__numJobs):
            self.__joblist[i]=joblist[i]
    
    #Set the parameter s
    def setBoost(self,s):
        self.__S=s

    #Set the quantum
    def setQuantum(self,quantum):
        self.__quantum=quantum

    #Llena a lista con los tiempos de inicio e cada tranbajo para controlar cuando empiezan
    def setioDone(self):
        for i in range (self.__numJobs):
            if self.__joblist[i].getArrivalTime() not in self.__ioDone:
                self.__ioDone[self.__joblist[i].getArrivalTime()]=[]
            self.__ioDone[self.__joblist[i].getArrivalTime()].append((i, 'JOB BEGINS'))

    #Cambio los atributos de cada trabajo para su correcta ejecución      
    def setAllJob(self):
        for i in range(self.__numJobs):
            self.__joblist[i].setTimeLeft(self.__joblist[i].getRunTime())
            self.__joblist[i].setTrickLeft(self.__quantumList[self.__hiQueue])
            self.__joblist[i].setAllotLeft(self.__allotmentList[self.__hiQueue])
    
    #Organiza correctamente la prioridad de cada trabajo dependiendo del numero de colas
    def setAllPriors(self):
        for i in range(self.__numJobs):
            if self.__joblist[i].getPriority()==3:
                self.__joblist[i].setPriority(self.__hiQueue)
            elif self.__joblist[i].getPriority()==2 and self.__hiQueue>0:
                self.__joblist[i].setPriority(self.__hiQueue-1)
            else:
                self.__joblist[i].setPriority(0)
    
    #Added 17-01-2021
    def getResponseTimeAvg(self):
        return self.__avgResponseTime

    def getTurnAroundAvg(self):
        return self.__avgTurnAround

    #Funcion central
    def RunMLFQ(self,joblist,numQueue,boost,quantumm):

        # initialize the MLFQ atributtes
        self.setQuantum(quantumm)
        self.setnumQueues(numQueue)
        self.setQuantumList()
        self.setAllotmentList()
        self.setHiQueue()
        self.setJobList(joblist)
        self.setBoost(boost)
        self.setioDone()
        self.setAllJob()
        self.setAllPriors()
        #self.__file.truncate(0)

        # initialize the MLFQ queues
        queue = {}
        for q in range(self.__numQueues):
            queue[q] = []

        # TIME IS CENTRAL
        currTime = 0

        # use these to know when we're finished
        totalJobs    = self.__numJobs
        finishedJobs = 0

    
        self.__file=self.__file+('\nExecution Trace:\n')

        while finishedJobs < totalJobs:
            # find highest priority job
            # run it until either
            # (a) the job uses up its time quantum
            # (b) the job performs an I/O

            # check for priority boost
            if self.__S > 0 and currTime != 0:
                if currTime % self.__S == 0:
                    self.__file=self.__file.write('[ time %d ] BOOST ( every %d )\n' % (currTime, self.__S))
                    # remove all jobs from queues (except high queue) and put them in high queue
                    for q in range(self.__numQueues-1):
                        for j in queue[q]:
                            if self.__joblist[j].getDoinIo() == False:
                                queue[self.__hiQueue].append(j)
                        queue[q] = []

                    # change priority to high priority
                    # reset number of ticks left for all jobs (just for lower jobs?)
                    # add to highest run queue (if not doing I/O)
                    for j in range(self.__numJobs):
                        # print '-> Boost %d (timeLeft %d)' % (j, job[j]['timeLeft'])
                        if self.__joblist[j].getTimeLeft() > 0:
                            # print '-> FinalBoost %d (timeLeft %d)' % (j, job[j]['timeLeft'])
                            self.__joblist[j].setPriority(self.__hiQueue)  
                            self.__joblist[j].setTrickLeft(self.__allotmentList[self.__hiQueue]) 
                    # print 'BOOST END: QUEUES look like:', queue

            # check for any I/Os done
            if currTime in self.__ioDone:
                for (j, type) in self.__ioDone[currTime]:
                    q = self.__joblist[j].getPriority()
                    self.__joblist[j].setDoinIO(False)
                    self.__file=self.__file+('[ time %d ] %s by JOB %d\n' % (currTime, type, j))
                    self.__joblist[j].setJobStatus(1)
                    if self.__iobump == False or type == 'JOB BEGINS':
                        queue[q].append(j)
                    else:
                        queue[q].insert(0, j)
                        

            # now find the highest priority job
            currQueue = self.findQueue(queue)
            if currQueue == -1:
                self.__file=self.__file+('[ time %d ] IDLE\n' % (currTime))
                currTime += 1
                continue

            # there was at least one runnable job, and hence ...
            currJob = queue[currQueue][0]
            if self.__joblist[currJob].getPriority() != currQueue:
                self.Abort('currPri[%d] does not match currQueue[%d]' % (self.__joblist[currJob].getPriority(), currQueue))
            
            tiempoleftaux=(self.__joblist[currJob].getTimeLeft()-1)
            tickleftaux=(self.__joblist[currJob].getTrickLeft()-1)
            self.__joblist[currJob].setTimeLeft(int(tiempoleftaux))
            self.__joblist[currJob].setTrickLeft(int(tickleftaux))

            if self.__joblist[currJob].getFirstRun() == -1:
                self.__joblist[currJob].setFirstRun(currTime)

            runTime   = self.__joblist[currJob].getRunTime()
            ioFreq    = self.__joblist[currJob].getIoTime()
            ticksLeft = self.__joblist[currJob].getTrickLeft()
            allotLeft = self.__joblist[currJob].getAllotLeft()
            timeLeft  = self.__joblist[currJob].getTimeLeft()

            self.__file=self.__file+( '[ time %d ] Run JOB %d at PRIORITY %d [ TICKS %d ALLOT %d TIME %d (of %d) ]\n' % \
                (currTime, currJob, currQueue, ticksLeft, allotLeft, timeLeft, runTime)
        )
            if timeLeft < 0:
                self.Abort('Error: should never have less than 0 time left to run')

            # UPDATE TIME
            currTime += 1

            # CHECK FOR JOB ENDING
            if timeLeft == 0:
                self.__file=self.__file+( '[ time %d ] FINISHED JOB %d\n' % (currTime, currJob))
                self.__joblist[currJob].setJobStatus(0)
                finishedJobs += 1
                self.__joblist[currJob].setEndTime(currTime)
                # print 'BEFORE POP', queue
                done = queue[currQueue].pop(0)
                # print 'AFTER POP', queue
                assert(done == currJob)
                continue

            # CHECK FOR IO
            issuedIO = False
            if ioFreq > 0 and (((runTime - timeLeft) % ioFreq) == 0):
                # time for an IO!
                self.__file=self.__file+('[ time %d ] IO_START by JOB %d\n' % (currTime, currJob))
                issuedIO = True
                desched = queue[currQueue].pop(0)
                assert(desched == currJob)
                self.__joblist[currJob].setDoinIO(True)
                # this does the bad rule -- reset your tick counter if you stay at the same level
                if self.__stay == True:
                    self.__joblist[currJob].setTrickLeft(self.__quantumList[currQueue])
                    self.__joblist[currJob].setAllotmentLeft(self.__allotmentList[currQueue])
                # add to IO Queue: but which queue?
                futureTime = currTime + self.__joblist[currJob].getIoTime()
                if futureTime not in self.__ioDone:
                    self.__ioDone[futureTime] = []
                #self.__file=self.__file.write('IO DONE\n')
                self.__ioDone[futureTime].append((currJob, 'IO_DONE'))
                while True:
                    currTime+=1
                    if currTime==futureTime:
                        break
                    self.__file=self.__file+('[ time %d ] IO_RUN by JOB %d\n' % (currTime,currJob))

            # CHECK FOR QUANTUM ENDING AT THIS LEVEL (BUT REMEMBER, THERE STILL MAY BE ALLOTMENT LEFT)
            if ticksLeft == 0:
                if issuedIO == False:
                    # IO HAS NOT BEEN ISSUED (therefor pop from queue)'
                    desched = queue[currQueue].pop(0)
                assert(desched == currJob)

                self.__joblist[currJob].setAllotLeft(self.__joblist[currJob].getAllotLeft() - 1)

                if self.__joblist[currJob].getAllotLeft()== 0:
                    # this job is DONE at this level, so move on
                    if currQueue > 0:
                        # in this case, have to change the priority of the job
                        self.__joblist[currJob].setPriority(currQueue - 1)
                        self.__joblist[currJob].setTrickLeft(self.__quantumList[currQueue-1])
                        self.__joblist[currJob].setAllotLeft(self.__allotmentList[currQueue-1])
                        if issuedIO == False:
                            queue[currQueue-1].append(currJob)
                    else:
                        self.__joblist[currJob].setTrickLeft(self.__quantumList[currQueue])
                        self.__joblist[currJob].setAllotLeft(self.__allotmentList[currQueue])
                        if issuedIO == False:
                            queue[currQueue].append(currJob)
                else:
                    # this job has more time at this level, so just push it to end
                    self.__joblist[currJob].setTrickLeft(self.__quantumList[currQueue])
                    if issuedIO == False:
                        queue[currQueue].append(currJob)
        return self.__file
     

    #Added 17-01-2021 - some updates
    def statistics(self):
        print( '')
        print( 'Final statistics:')
        responseSum   = 0
        turnaroundSum = 0
        for i in range(self.__numJobs):
            response   = self.__joblist[i].getFirstRun() - self.__joblist[i].getArrivalTime()
            turnaround = self.__joblist[i].getEndTime() - self.__joblist[i].getArrivalTime()
            print( '  Job %2d: startTime %3d - response %3d - turnaround %3d' % (i, self.__joblist[i].getArrivalTime(),
                                                                                response, turnaround))
            self.__joblist[i].setResponsiveTime(response)
            self.__joblist[i].setTurnAround(turnaround)
            responseSum   += response
            turnaroundSum += turnaround
        self.__avgResponseTime = (responseSum)/self.__numJobs
        self.__avgTurnAround = (turnaroundSum)/self.__numJobs

        print( '\n  Avg %2d: startTime n/a - response %.2f - turnaround %.2f' % (i, 
                                                                                float(responseSum)/self.__numJobs,
                                                                                float(turnaroundSum)/self.__numJobs))

        print ('\n')
        
    
    def infGrafica(self,tiempo,trabajo,prioridad): #recibe como parametros las listas vacias y estas se llenan con la información lista para usar
        
        filtro1=re.findall("\d+\s]\sIDLE|\d+\s]\sIO_RUN\s\w+\s\w+\s\d|\d+\s]\sIO_START\s\w+\s\w+\s\d|\d+\s]\s\w+\s\w+\s\d\s\w+\s\w+\s\d",self.__file)
        numero=[]
        for i in range(len(filtro1)):   #IDLE = 3, IO =4
            x=re.search("IDLE", filtro1[i])
            y=re.search("IO_",filtro1[i])
            if x:
                numero.append(re.findall("\d+",filtro1[i]))
                numero[i].append(3)
                numero[i].append(self.__hiQueue)
            elif y:
                numero.append(re.findall("^\d+",filtro1[i]))
                numero[i].append(4)
                numero[i].append(self.__hiQueue)
            else:
                numero.append(re.findall("\d+",filtro1[i]))                
        for i in numero:
            tiempo.append(int(i[0]))
            trabajo.append(int(i[1]))
            prioridad.append(int(i[2]))
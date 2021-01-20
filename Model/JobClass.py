#----------------------------------------------------------------------------------
# Class job: this class will manage all jobs, attributes and behaivor during 
# the execution of the scheculer
#----------------------------------------------------------------------------------

#----------------------------------------------------------------------------------
# @Authors: Miriam Arango, Luisa Arboleda, Yeison Quinto
# @Version: Version 1.0
# @Date: 09 - 01 - 2021
#----------------------------------------------------------------------------------

class Job():

    #Builder
    def __init__(self):

        #Initial Attributes
        self.__quantity=0
        self.__priority=3
        self.__arrivalTime=0 #This is start time
        self.__runTime=100
        self.__ioTime=0
        self.__startIoTime=0 #This is ioFreq
        self.__allotLeft=0
        self.__trickLeft=0
        self.__timeLeft=0
        self.__doinIo=False
        self.__firstRun=-1
        self.__endTime=0
        
        #Result Attributes
        self.__jobStatus=3
        self.__turnAround=0.0
        self.__responsiveTime=0.0
    
    #Setters
    def setQuantity(self, data):
        self.__quantity=data

    def setPriority(self, data):
        self.__priority=data

    def setArrivalTime(self, data):
        self.__arrivalTime=data

    def setRunTime(self, data):
        self.__runTime=data

    def setIoTime(self, data):
        self.__ioTime=data

    def setStartIoTime(self, data):
        self.__startIoTime=data
    
    def setJobStatus(self, data):
        self.__jobStatus=data

    def setTurnAround(self, data):
        self.__turnAround=data

    def setResponsiveTime(self, data):
        self.__responsiveTime=data
    
    def setAllotLeft(self, data):
        self.__allotLeft=data

    def setTrickLeft(self, data):
        self.__trickLeft=data

    def setTimeLeft(self, data):
        self.__timeLeft=data

    def setDoinIO(self, data):
        self.__doinIo=data

    def setFirstRun(self, data):
        self.__firstRun=data

    def setEndTime(self, data):
        self.__endTime=data

    #Getters
    def getQuantity(self):
        return self.__quantity

    def getPriority(self):
        return self.__priority
    
    def getArrivalTime(self):
        return self.__arrivalTime
    
    def getRunTime(self):
        return self.__runTime
    
    def getIoTime(self):
        return self.__ioTime
    
    def getStartIoTime(self):
        return self.__startIoTime

    def getJobStatus(self):
        return self.__jobStatus

    def getTurnAround(self):
        return self.__turnAround

    def getResponsiveTime(self):
        return self.__responsiveTime

    def getAllotLeft(self):
        return self.__allotLeft
    
    def getTrickLeft(self):
        return self.__trickLeft
    
    def getTimeLeft(self):
        return self.__timeLeft

    def getDoinIo(self):
        return self.__doinIo

    def getFirstRun(self):
        return self.__firstRun

    def getEndTime(self):
        return self.__endTime
import re

class Course:
    def __init__(self, id, name, numberOfHours, isDone, notes):
        self.__father = None
        self.setId(id)
        self.setName(name)
        self.setNumberOfHours(numberOfHours)
        self.setIsDone(isDone)
        self.setNotes(notes)
        self.__isOptional = False
        self.__rank = 0
        self.__childrenSet = set()
        self.visited = False
    def setId(self, id):
        self.__id = id

    def setName(self, name):
        self.__name = name

    def setNumberOfHours(self, numberOfHourse):
        self.__numberOfHourse = numberOfHourse

    def setIsDone(self, isDone):
        if re.match(r'([ABCDF][+-]?)', isDone):
            self.__isDone = True
        elif re.match(isDone == 'ناجح', isDone):
            self.__isDone = True
            self.__numberOfHourse = 0
        else:
            self.__isDone = False

    def setNotes(self, notes):
        self.__notes = notes

    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

    def getNumberOfHours(self):
        return self.__numberOfHourse

    def getIsDone(self):
        return self.__isDone

    def getNotes(self):
        return self.__notes

    def setIsOptional(self, isOptional):
        self.__isOptional = isOptional

    def getIsOptional(self):
        return self.__isOptional

    def addChild(self, child):
        self.__childrenSet.add(child)

    def getChildrenSet(self):
        return self.__childrenSet
    
    def setFather(self, father):
        self.__father = father

    def getFather(self):
        return self.__father

    def setRank(self, rank):
        self.__rank = rank

    def getRank(self):
        return self.__rank
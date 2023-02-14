class Event:
    def __init__(self, time, type, target, source):
        self.__time = time
        self.__type = type
        self.__target = target
        self.__source = source

    @property #Set and get time 
    def time(self):
        return self.__time

    @time.setter
    def time(self, time):
        self.__time = time

    @property #Set and get event type
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type

    @property #Set and get event target
    def target(self):
        return self.__target

    @target.setter
    def target(self, target):
        self.__target = target

    @property #Set and get event source
    def source(self):
        return self.__source

    @target.setter
    def source(self, source):
        self.__source = source

    
    def printEvent(self):
        print("time : ",self.__time,"\ntype: ",self.__type,"\ntarget: ",self.__target,"\nsource: ",self.__source)



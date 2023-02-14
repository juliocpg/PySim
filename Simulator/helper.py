from Event import *
import numpy as np

# def SortbyTime(eList):
#     '''Sort a list of events chronologically'''
#     N = len(eList) #length

#     times = list()
#     for i in range(N):
#         times.append(eList[i].time)

#     indexes = np.argsort(times) #vector with sorted indexes
#     print(times)
   
#     elist = list()
#     for i in range(N):
#         elist.append(eList[indexes[i]])

#     return elist  
    
def First_Event(elist):
    min_time = 0
    pos = 1000
    for i in range(len(elist)):
        if elist[i].time < pos:
            min_time = elist[i].time
            pos = i #at the end pos contains the psoition of the first event in time
    return pos
    

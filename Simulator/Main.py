import numpy as np
import random as rand
from Event import *
from helper import *

#Run time
sim_time = 0

#Verbose
verbose = 1

#Network elements
U = 1#Users

# Channel
min_delay = 0.001#min delay
max_delay = 1    #min delay

# Metrics
#Authentication time
ee_delay = np.zeros([U,1])

#tx time
TX_time = np.zeros([U,1])

#rx time
RX_time = np.zeros([U,1])
RX_time_CA = 0

#processing time
PR_time = np.zeros([U,1])


# Parameters

# Ellyptic curve operation  -------TODO USE REAL VALUES FOR IOT DEVICE
EA_opt_time = 0.01# Point Addition time
SM_opt_time = 0.01# Scalar multiplication time

#Communication setup
Lambda = 1.5
Rate = 1024*1024 #1Mbps

# Data
Id_length = 128#bits

Point_length = 256#bits

MSG_length = 100#bits  DUMMY msg

Certf_length = Point_length

#CA
cpu_queue_time = 0

# IoT Device power comsuption
tx_power = 0.001#Watts 
rx_power = 0.002
pr_power = 0.001
idle_power= 0.0001

# Simulator
#---INITIALIZATION

#Generate Initial Traffic
exp_dist = [rand.expovariate(Lambda) for i in range(U)]
initial_req_time = np.cumsum(exp_dist) / sum(exp_dist ) #All start in the first second
elist = []

for i in range(U):
    #Add initial events to elist
    time = initial_req_time[i]
    etype = 0
    target = i
    source = -1
    elist.append(Event(time, etype, target, source))
    
c_time = 0

#MAIN LOOP
while len(elist) != 0:  #while event list is not empty

    pos = First_Event(elist) #Take first cronologically event in elist(min time)   

    c_time = elist[pos].time #Load event data
    c_type = elist[pos].type
    c_target = elist[pos].target
    c_source = elist[pos].source 
    Event.printEvent(elist[-1])

    elist.remove(elist[pos]) #remove from the list of future events

    #Proccess current event
    if c_type == 0: # Send Idi,Ri

        if verbose: print(c_time," : Node ",c_target," sent Id,R to CA")

        #Update statistics
        delay = (max_delay-min_delay)*rand.random() + min_delay #delay pkt

        tx_time = (Point_length + Id_length) / Rate #tx time for this pkt

        TX_time[c_target] = TX_time[c_target] + tx_time #Update global tx

        #Program future events 
        time = c_time + tx_time + delay
        etype = 1 # Reception and processing event creation
        target = 'CA'
        source = c_target
        elist.append( Event(time, etype, target, source) ) #Add new event to handle in future
        Event.printEvent(elist[-1])

    elif c_type == 1: #CA Receives, Proccess Request and sends back auxiliar info
        if verbose: print(c_time," : CA Proccess Request of node ",c_source)

        #Update metrics                        
        cpu_time = 1 * EA_opt_time + 1 * SM_opt_time
        
        cpu_queue_time =  cpu_queue_time + cpu_time #Assuming one thread in CA, time when will finish this computation
        
        delay = (max_delay-min_delay)*rand.random() + min_delay

        tx_time = (Certf_length) / Rate        

        RX_time_CA = RX_time_CA + tx_time
        
        #Program future events 
        time = cpu_queue_time + tx_time + delay #TODO Crypto info
        etype = 2 # Reception and processing event creation
        target = c_source
        source = 'CA'
        elist.append( Event(time, etype, target, source) ) #Add new event to handle in future
        

    elif c_type == 2: # User i receive the material, compute the private key and send the Message M    
        if verbose: print(c_time," : User  ",c_target, " received auxiliary info from CA")
        #TODO Fix Crypto operation
        cpu_time = 1 * EA_opt_time + 1 * SM_opt_time; #Verify Compute private, public key and send message
        delay = (max_delay-min_delay)*rand.random() + min_delay
        
        #Program future events    
        time = c_time + (Certf_length + MSG_length + Id_length) / Rate + delay; #TODO Crypto info
        etype = 3 # Reception and processing event creation
        target = rand.randint(0,U-1) #Send to anyone randomly TODO may be need to be fixed
        source = c_target
        elist.append( Event(time, etype, target, source) ) #Add new event to handle in future
                
        #Update metrics
        PR_time[c_target] = PR_time[c_target] + cpu_time
        
        
    
 

        
        
    
    

'''

# Statatistics

end_end_delay = mean(ee_delay)
av_tx_time = mean(TX_time)
av_rx_time = mean(RX_time)
av_pr_time = mean(PR_time)
av_id_time = mean(ee_delay - (TX_time + RX_time + PR_time))

energy = av_tx_time * tx_power + av_rx_time* rx_power + av_pr_time* pr_power + av_id_time* idle_power

return end_end_delay,energy


'''
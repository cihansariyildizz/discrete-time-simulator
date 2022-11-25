import random 
import matplotlib.pyplot as plt 
import statistics
import numpy as np
from math import log



# This function uses inverse method to generate exponential rv with given lambda
def rv_generator_exp(lmbd):
    uniform = np.random.uniform(0.0, 1.0, 1)
    x = -(1/lmbd)*log(1-uniform)
    return x



# Q2--SIMULATION
def simulation(rho):
    c = 1000000 # 1Mbps to bits conversion
    l = 2000 #  given avarage length for M/M/1 simulation

    sum_numbers_arrival = 0
    t_T = 1000; # Time (T)

    discrete_arrival_times = [] # array for arrival times generated from RVs which are the time differences between events
    lamda = rho * (c/l) #lambda for packet arrival distrubitions

    # generate arrival events
    while sum_numbers_arrival < t_T: # adds rvs until sum is T
        number = rv_generator_exp(lamda)
        sum_numbers_arrival = sum_numbers_arrival + number
        arrival_tuple = ("arrival_time", sum_numbers_arrival)
        discrete_arrival_times.append(arrival_tuple)


    # generate lengths for each arrived packets
    packet_lengths = []
    for i in range(len(discrete_arrival_times)):
        length = rv_generator_exp(1/l)
        packet_lengths.append(length)

    discrete_departure_times = []
    for i in range(len(discrete_arrival_times)):
        arrival_time = discrete_arrival_times[i]
        arrival_time = arrival_time[1]
        packet_length = packet_lengths[i]
        service_time = packet_length/c
        if i == 0 : # first event
            departure_time = arrival_time + service_time
            departure_tuple = ("departure_time",departure_time)
            discrete_departure_times.append(departure_tuple)
        else: # other events
            # we need to check the (i-1)th element of array to decide if idle or not
            # i-1 is always the previous elementh departure, if the arrival is less than the previous departure then there still exist an element in the buffer
            prev_element_departure_time = discrete_departure_times[i-1]
            prev_element_departure_time = prev_element_departure_time[1] # gets the value from tuple
            if prev_element_departure_time > arrival_time:
                departure_time = prev_element_departure_time + service_time
                if departure_time > t_T: #if departure_time goes beyond the simulation time interval
                    break
                else:
                    departure_tuple = ("departure_time",departure_time)
                    discrete_departure_times.append(departure_tuple)
            else:
                departure_time = arrival_time + service_time
                if departure_time > t_T: #if departure_time goes beyond the simulation time interval
                    break
                else:
                    departure_tuple = ("departure_time",departure_time)
                    discrete_departure_times.append(departure_tuple)


    new_lamda = 5*lamda
    discrete_observer_times = []
    sum_numbers_observer = 0
    # generate observer events
    while sum_numbers_observer < t_T:
        number = rv_generator_exp(new_lamda)
        sum_numbers_observer = sum_numbers_observer + number
        observer_tuple = ("observer_time", sum_numbers_observer)
        discrete_observer_times.append(observer_tuple)
      
                
    merged_list = discrete_arrival_times + discrete_departure_times + discrete_observer_times     
    merged_list.sort(key=lambda y: y[1])

    n_a = 0
    n_d = 0
    n_o = 0
    observer_metrics = []

    for i in range(len(merged_list)):
        element = merged_list[i]
        event_name = element[0]
        event_time = element[1]
            
        if event_name == "observer_time": #if event is observer
            n_o = n_o + 1 # increase the observer counter
            diff = n_a - n_d # findout if there are more arrivals than departures at this spesific discrete observer event
            if diff > 0: # if positive, then there are more arrivals, so queue is not empty
                observer_metrics.append(diff)
            else: #if not positive then our queue is empty so idle.
                observer_metrics.append("idle")
                
        if event_name == "arrival_time": #if event is arival increase the arrival counter
            n_a = n_a + 1

        if event_name == "departure_time": #if event is departure increase the departure counter
            n_d = n_d + 1

        
    idle_count = observer_metrics.count('idle') # count idles in our observer_metrics list
    observer_metrics_updated = [value for value in observer_metrics if value != "idle"] # remove idles 
    summed_observer_metrics = sum(observer_metrics_updated) #sum all other metrics 
    piddle = idle_count/n_o #find propability of idle 
    e_N = summed_observer_metrics/n_o #find the mean value of number of packets in the queue
    return [piddle, e_N]


metrics = []
for i in range(8):
    metrics.append(simulation(0.25 + i*0.1))


rho_values_x = [0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95]
y_e_N = []
y_piddle = []

for i in range(len(metrics)):
    y_e_N.append(metrics[i][1])
    y_piddle.append(metrics[i][0])

figure, axis = plt.subplots(2)

axis[0].plot(rho_values_x,y_e_N) #graph for E[N]
axis[0].set_xlabel("rho value")
axis[0].set_ylabel("E[N]")
axis[1].plot(rho_values_x,y_piddle) #graph for piddle
axis[1].set_xlabel("rho value")
axis[1].set_ylabel("Pidle")
plt.show()


from copy import deepcopy
from fcn import *
import json


'''
Non-Preemptive:
    {
    First Come First Serve,
    Shortest Job First,
    Priority
    }

Preemptive
    {
    Priority,
    Shortest Remaining Time First,
    Round Robin
    }

'''


''' --------------------FIRST COME FIRST SERVE------------------- 
    --------------------- SHORTEST JOB FIRST--------------------- 
                           (Non-Preemptive)                      '''

def process_management_EXEC(file_name, key='fcfs'):
    # keys = ['fcfs', 'sjf']
    file = open(f'{file_name}.json')
    data = json.load(file)

    process = data['Process']
    burst_time = data['Burst Time']
    arrival_time = data['Arrival Time']
    
    file.close()

    St = {}
    Ft = {}

    process, burst_time, arrival_time = first_come_first_serve(process, burst_time, arrival_time)

    if key == 'sjf':
        for i in range(arrival_time.count(arrival_time[0])-1):
            for j in range(0, arrival_time.count(arrival_time[0])-i-1):
                if burst_time[j] > burst_time[j+1]:
                    burst_time[j], burst_time[j+1] = burst_time[j+1], burst_time[j]
                    process[j], process[j+1] = process[j+1], process[j]

    gantt_list = [arrival_time[0]]
    gantt_label = []
    if arrival_time[0] != 0:
        msg = [f'At time 0, Idle']
    else:
        msg = []
    terminating = 0
    for p in range(len(arrival_time)):
        if terminating < arrival_time[p]:
            gantt_list.append(arrival_time[p])
            msg.append(f'At time {gantt_list[-1]}, {process[p]} arrived/starts')
            St[f'{process[p]}'] = gantt_list[-1]
            gantt_label.append('idle')
            terminating += arrival_time[p] - terminating
        else:
            if p == 0:
                msg.append(f'At time {gantt_list[-1]}, {process[p]} arrived/starts')
                St[f'{process[p]}'] = gantt_list[-1]
            else:
                msg[-1] = msg[-1] + f' - {process[p]} starts'
                St[f'{process[p]}'] = gantt_list[-1]
        terminating = terminating + burst_time[p]
        gantt_list.append(terminating)
        gantt_label.append(f'{process[p]}')
        msg.append(f'At time {gantt_list[-1]}, {process[p]} terminated')
        Ft[f'{process[p]}'] = gantt_list[-1]

        if key == 'sjf':
            s = list(St.keys())
            x = diff(s, process)
            
            indices = [process.index(x[o]) for o in range(len(x))]
            y = [burst_time[i] for i in indices if terminating >= arrival_time[i]]
            indices = [burst_time.index(y[o]) for o in range(len(y))]
            for i in range(len(y)-1):
                for j in range(0, len(y)-i-1):
                    if y[j] > y[j+1]:
                        a, b = indices[j], indices[j+1]
                        
                        burst_time[a], burst_time[b] = burst_time[b], burst_time[a]
                        arrival_time[a], arrival_time[b] = arrival_time[b], arrival_time[a]
                        process[a], process[b] = process[b], process[a]
    gantt_list[0] = 0
    
    Start = list(St.values())
    Finish = list(Ft.values())

    idle_sum = 0
    for i in range(len(gantt_label)):
        if gantt_label[i] == 'idle':
            idle_sum += gantt_list[i+1] - gantt_list[i]
    CPU_Utilization = ( 1 - (idle_sum / gantt_list[-1]) ) * 100

    gantt_list.pop(0)
    
    if len(gantt_list)+1 == len(msg) and len(gantt_list) == len(gantt_label):
        print('Good')
    else:
        print('Error may occur')
    

    return [gantt_list, gantt_label, msg, CPU_Utilization, Start, Finish, process, burst_time, arrival_time, idle_sum]




''' --------------------PRIORITY--------------------- 
                (Preemptive/Non-Preemptive)          '''

def priority(file_name, key='p'):
    # keys = {p : 'Preemptive', np : 'Non-Preemptive'}

    file = open(f'{file_name}.json')
    data = json.load(file)

    process = data['Process']
    burst_time = data['Burst Time']
    arrival_time = data['Arrival Time']
    priority_num = data['Priority No.']
    
    file.close()

    process, burst_time, arrival_time, priority_num = first_come_first_serve(process, burst_time, arrival_time, priority_num=priority_num)

    Proc = process.copy()
    Bt = burst_time.copy()
    At = arrival_time.copy()
    Prio = priority_num.copy()

    if key.lower() == 'p':
        Finished = []
        gantt_list = [0]

        St = {}
        Ft = {}
        remaining = {}
        
        for i in range(len(Proc)):
            St[Proc[i]] = [At[i]]
            Ft[Proc[i]] = [At[i]]
            remaining[Proc[i]] = [Bt[i]]
        remaining_table = [deepcopy(remaining)]
        if arrival_time[0] != 0:
            msg = [f'At time 0, Idle']
            
            remaining_table.append(deepcopy(remaining))
            I = True
            gantt_label = ['idle']
        else:
            msg = []
            gantt_label = []

        terminated = ''
        while len(Finished) != len(Proc):
            
            # Time passed the arrival time
            x = diff(Finished, Proc)
            indices = [Proc.index(x[o]) for o in range(len(x))]
            y = [Prio[i] for i in indices if gantt_list[-1] >= At[i]]
            indices = [Prio.index(y[o]) for o in range(len(y))]
            if len(y) != 0:
                for i in range(len(y)-1):
                    for j in range(0, len(y)-i-1):
                        if y[j] > y[j+1]:
                            y[j], y[j+1] = y[j+1], y[j]
                            indices[j], indices[j+1] = indices[j+1], indices[j]

                while indices != []:
                    index = indices[0]
                    time = Bt[index]
                    if terminated == '':
                        msg.append(f'At time {gantt_list[-1]}, {Proc[index]} arrived/starts')
                    else:
                        msg.append(f'At time {gantt_list[-1]}, {terminated} terminated - {Proc[index]} starts')
                    St[f'{Proc[index]}'] += [gantt_list[-1]]
                    
                    gantt_label.append(f'{Proc[index]}')
                    gantt_list.append(time + gantt_list[-1])
                    Ft[f'{Proc[index]}'] += [gantt_list[-1]]
                    if len(indices) == 1:
                        msg.append(f'At time {gantt_list[-1]}, {Proc[index]} terminated')
                    terminated = Proc[index]
                    Finished.append(Proc[index])
                    remaining[Proc[index]] += [0]
                    remaining_table.append(deepcopy(remaining))
                    indices.pop(0)
            
            else:
                # IDLE
                x = diff(Finished, Proc)
                if len(x) == 0:
                    break
                index = Proc.index(x[0])
                time = At[index] + Bt[index]

                Priorities = [Prio[Proc.index(o)] for o in x]
                min_priority = min(Priorities)
                index_of_priority = Prio.index(min_priority)

                if time > At[index_of_priority]:
                    gantt_list.append(At[index])

                    if terminated == '':
                        msg.append(f'At time {At[0]}, {Proc[0]} arrived/starts')
                    St[f'{Proc[index]}'] += [gantt_list[-1]]
                    
 
                    if At[index_of_priority] not in gantt_list:
                        gantt_list.append(At[index_of_priority])
                        gantt_label.append(f'{Proc[index]}')
                    else:
                        gantt_label.append('idle')
                    msg.append(f'At time {gantt_list[-1]}, {Proc[index_of_priority]} arrived/starts')
                    St[f'{Proc[index_of_priority]}'] += [gantt_list[-1]] #######!!!!!??
                    
                    if gantt_list[-1] not in St[f'{Proc[index]}']:
                        St[f'{Proc[index]}'] += [gantt_list[-1]]

                    if gantt_list[-1] not in St[f'{Proc[index_of_priority]}']:
                        St[f'{Proc[index_of_priority]}'] += [gantt_list[-1]]
                    terminated = Proc[index_of_priority]
                    gantt_list.append(At[index_of_priority] + Bt[index_of_priority])

                    
                    msg.append(f'At time {gantt_list[-1]}, {Proc[index_of_priority]} terminated')

                    Ft[f'{Proc[index_of_priority]}'] += [gantt_list[-1]]
                    terminated = Proc[index_of_priority]
                    _diff = At[index_of_priority] - At[index]
                    Bt[index] -= _diff
                    Finished.append(Proc[index_of_priority])

                    x = diff(Finished, Proc)
                    indices = [Proc.index(x[o]) for o in range(len(x))]
                    y = [Prio[i] for i in indices if gantt_list[-1] >= At[i]]
                    if len(y) != 0:
                        msg.pop(-1)
                    else:
                        gantt_label.pop(-1)
                        msg.pop(-2)
                        remaining_table.pop(-1)
                        
                    if gantt_label[-1] != 'idle':
                        remaining[Proc[index]] += [Bt[index]]
                        remaining_table.append(deepcopy(remaining))

                        remaining[Proc[index_of_priority]] += [0]
                        remaining_table.append(deepcopy(remaining))
                    else:
                        remaining_table.append(deepcopy(remaining))
                        remaining[Proc[index_of_priority]] += [0]
                        remaining_table.append(deepcopy(remaining))

                    gantt_label.append(f'{Proc[index_of_priority]}')
                else:
                    msg.append(f'At time {gantt_list[-1]}, {terminated} terminated - {Proc[index]} starts')
                    St[f'{Proc[index]}'] += [gantt_list[-1]]
                    gantt_label.append('idle')
                    gantt_label.append(f'{Proc[index]}')
                    if At[index] not in gantt_list:
                        gantt_list.append(At[index])
                    terminated = Proc[index]
                    gantt_list.append(time)
                    Ft[f'{Proc[index]}'] += [gantt_list[-1]]
                    Finished.append(Proc[index])
                    remaining[Proc[index]] += [0]
                    remaining_table.append(deepcopy(remaining))
        
        print(St)
        idle_sum = 0
        for i in range(len(gantt_label)):
            if gantt_label[i] == 'idle':
                idle_sum += gantt_list[i+1] - gantt_list[i]
        CPU_Utilization = ( 1 - (idle_sum / gantt_list[-1]) ) * 100

        gantt_list.pop(0)

        if len(gantt_list)+1 == len(msg) and len(gantt_list) == len(gantt_label):
            print('Good')
        else:
            print('Error may occur')
        return [gantt_list, gantt_label, msg, CPU_Utilization, St, Ft, process, burst_time, arrival_time, idle_sum, remaining_table]
    
    elif key.lower() == 'np':
        St = {}
        Ft = {}

        gantt_list = [arrival_time[0]]
        gantt_label = []
        if arrival_time[0] != 0:
            msg = [f'At time 0, Idle']
        else:
            msg = []
        terminating = 0
        for p in range(len(arrival_time)):
            if terminating < arrival_time[p]:
                gantt_list.append(arrival_time[p])
                msg.append(f'At time {gantt_list[-1]}, {process[p]} arrived/starts')
                St[f'{process[p]}'] = gantt_list[-1]
                gantt_label.append('idle')
                terminating += arrival_time[p] - terminating
            else:
                if p == 0:
                    msg.append(f'At time {gantt_list[-1]}, {process[p]} arrived/starts')
                    St[f'{process[p]}'] = gantt_list[-1]
                else:
                    msg[-1] = msg[-1] + f' - {process[p]} starts'
                    St[f'{process[p]}'] = gantt_list[-1]
            terminating = terminating + burst_time[p]
            gantt_list.append(terminating)
            gantt_label.append(f'{process[p]}')
            msg.append(f'At time {gantt_list[-1]}, {process[p]} terminated')
            Ft[f'{process[p]}'] = gantt_list[-1]

            s = list(St.keys())
            x = diff(s, process)
            
            indices = [process.index(x[o]) for o in range(len(x))]
            y = [priority_num[i] for i in indices if terminating >= arrival_time[i]]
            indices = [priority_num.index(y[o]) for o in range(len(y))]

            for i in range(len(y)-1):
                for j in range(0, len(y)-i-1):
                    if y[j] > y[j+1]:
                        a, b = indices[j], indices[j+1]
                        
                        priority_num[a], priority_num[b] = priority_num[b], priority_num[a]
                        burst_time[a], burst_time[b] = burst_time[b], burst_time[a]
                        arrival_time[a], arrival_time[b] = arrival_time[b], arrival_time[a]
                        process[a], process[b] = process[b], process[a]
        gantt_list[0] = 0

        Start = list(St.values())
        Finish = list(Ft.values())

        idle_sum = 0
        for i in range(len(gantt_label)):
            if gantt_label[i] == 'idle':
                idle_sum += gantt_list[i+1] - gantt_list[i]
        CPU_Utilization = ( 1 - (idle_sum / gantt_list[-1]) ) * 100

        gantt_list.pop(0)

        if len(gantt_list)+1 == len(msg) and len(gantt_list) == len(gantt_label):
            print('Good')
        else:
            print('Error may occur')

        return [gantt_list, gantt_label, msg, CPU_Utilization, Start, Finish, process, burst_time, arrival_time, idle_sum]




''' --------------------SHORTEST REMAINING TIME FIRST------------------- 
                            SJF - Preemptive                            '''

def srtf(file_name):

    file = open(f'{file_name}.json')
    data = json.load(file)

    process = data['Process']
    burst_time = data['Burst Time']
    arrival_time = data['Arrival Time']

    file.close()

    process, burst_time, arrival_time = first_come_first_serve(process, burst_time, arrival_time)

    Proc = process.copy()
    Bt = burst_time.copy()
    At = arrival_time.copy()

    St = {}
    Ft = {}
    remaining = {}

    
    msg = []
    
    for i in range(len(Proc)):
        St[Proc[i]] = [At[i]]
        Ft[Proc[i]] = [At[i]]
        remaining[Proc[i]] = [Bt[i]]
    remaining_table = [deepcopy(remaining)]

    if At[0] == 0:
        gantt_list = [0]
        gantt_label = [Proc[0]]
        msg = [f'At time {At[0]}, {Proc[0]} arrived/starts']
    else:
        gantt_list = [0, At[0]]
        gantt_label = ['idle', Proc[0]]
        msg = [f'At time 0, Idle', f'At time {At[0]}, {Proc[0]} arrived/starts']
        remaining_table.append(deepcopy(remaining))
    St[f'{Proc[0]}'] += [gantt_list[-1]]

    Finished = []
    arrived = [Proc[0]]
    ON_process = Proc[0]
    idle = 0
    t = ''
    while len(Finished) != len(Proc):
        index_of_ON_process = Proc.index(ON_process)
        time = At[index_of_ON_process] + Bt[index_of_ON_process]
        if idle == 0:
            for k in range(index_of_ON_process+1, len(At)):
                if time > At[k]: # Time passed the arrival time
                    _diff = At[k] - At[index_of_ON_process]
                    x = Bt[index_of_ON_process] - _diff
                    
                    if Bt[k] < x: # Burst time is less than the difference between the arrival
                        Bt[index_of_ON_process] = x
                        arrived.append(Proc[k])
                        gantt_list.append(At[k])
                        St[f'{Proc[index_of_ON_process]}'] += [gantt_list[-1]]
                        St[f'{Proc[k]}'] += [gantt_list[-1]]
                        ON_process = Proc[k]
                        remaining[Proc[index_of_ON_process]] += [Bt[index_of_ON_process]]
                        remaining_table.append(deepcopy(remaining))
                        gantt_label.append(Proc[k])
                        msg.append(f'At time {At[k]}, {Proc[k]} arrived/starts')
                        break
                    
                    else:
                        index_of_ON_process = Proc.index(ON_process)
                        z = 0
                        ''' Finds the arrived process after ON_process'''
                        for p in range(k, len(At)):
                            if time >= At[p]:
                                arrived.append(Proc[p])
                                _diff = At[p] - At[index_of_ON_process]
                                x = Bt[index_of_ON_process] - _diff
                                if Bt[p] < x:
                                    Bt[index_of_ON_process] = x
                                    gantt_list.append(At[p])
                                    St[f'{Proc[p]}'] += [gantt_list[-1]]
                                    St[f'{Proc[index_of_ON_process]}'] += [gantt_list[-1]]
                                    remaining[Proc[index_of_ON_process]] += [Bt[index_of_ON_process]]
                                    remaining_table.append(deepcopy(remaining))
                                    gantt_label.append(Proc[p])
                                    msg.append(f'At time {At[p]}, {Proc[p]} arrived/starts')
                                    ON_process = Proc[p]
                                    z = 1
                                    break
                        if z == 0:
                            gantt_list.append(gantt_list[-1] + Bt[index_of_ON_process])
                            Ft[f'{Proc[index_of_ON_process]}'] += [gantt_list[-1]]
                            Bt[index_of_ON_process] = 0
                            remaining[Proc[index_of_ON_process]] += [Bt[index_of_ON_process]]
                            remaining_table.append(deepcopy(remaining))
                            Finished.append(ON_process)
                            t = Proc[index_of_ON_process]
                        break
                
                else: # Finish the current process and finds the idle time
                    if gantt_list[-1] not in St[f'{Proc[index_of_ON_process]}']:
                        St[f'{Proc[index_of_ON_process]}'] += [gantt_list[-1]]
                        gantt_label.append(Proc[index_of_ON_process])
                        msg.append(f'At time {gantt_list[-1]}, {Proc[index_of_ON_process]} arrived/starts')
                    gantt_list.append(gantt_list[-1] + Bt[index_of_ON_process])
                    Ft[f'{Proc[index_of_ON_process]}'] += [gantt_list[-1]]
                    Bt[index_of_ON_process] = 0
                    remaining[Proc[index_of_ON_process]] += [Bt[index_of_ON_process]]
                    remaining_table.append(deepcopy(remaining))
                    Finished.append(ON_process)
                    idle = At[k] - (gantt_list[-1] + Bt[index_of_ON_process])
                    t = Proc[index_of_ON_process]

                    waiting = diff(arrived, Finished)
                    if len(waiting) == 0:
                        msg.append(f'At time {gantt_list[-1]}, {t} terminated')
                    break

        if idle != 0 and len(arrived) != 0: # The waiting process will continue during idle
            waiting = diff(arrived, Finished)
            ON_process_indexes = [Proc.index(waiting[o]) for o in range(len(waiting))]
            Bts = [Bt[i] for i in ON_process_indexes]
            
            for i in range(len(Bts)-1):
                for j in range(0, len(Bts)-i-1):
                    if Bts[j] > Bts[j+1]:
                        Bts[j], Bts[j+1] = Bts[j+1], Bts[j]
                        waiting[j], waiting[j+1] = waiting[j+1], waiting[j]
                        ON_process_indexes[j], ON_process_indexes[j+1] = ON_process_indexes[j+1], ON_process_indexes[j]

            if len(waiting) != 0:
                while idle != 0:
                    index = ON_process_indexes[0]
                    time = Bt[index]
                    index_of_ON_process = Proc.index(ON_process)

                    for p in range(k, len(At)):
                        if idle == time:
                            msg.append(f'At time {gantt_list[-1]}, {t} terminated - {Proc[index]} starts')
                            St[f'{Proc[index]}'] += [gantt_list[-1]]
                            gantt_list.append(time + gantt_list[-1])
                            Bt[index] = 0
                            Finished.append(Proc[index])
                            ON_process = Proc[index_of_ON_process + 1]
                            arrived.append(ON_process)
                            Ft[f'{Proc[index]}'] += [gantt_list[-1]]
                            remaining[Proc[index]] += [Bt[index]]
                            remaining_table.append(deepcopy(remaining))
                            gantt_label.append(Proc[index])
                            t = Proc[index]
                            idle = 0
                            print('a')
                            break

                        elif idle < time:
                            Bt[index] -= idle
                            if Bt[index_of_ON_process + 1] >= Bt[index]:
                                msg.append(f'At time {gantt_list[-1]}, {t} terminated - {Proc[index]} starts')
                                St[f'{Proc[index]}'] += [gantt_list[-1]]
                                gantt_list.append(time + gantt_list[-1])
                                Finished.append(Proc[index])
                                Bt[index] = 0
                                Ft[f'{Proc[index]}'] += [gantt_list[-1]]
                                gantt_label.append(Proc[index])
                                t = Proc[index]
                            else:
                                msg.append(f'At time {gantt_list[-1]}, {t} terminated - {Proc[index]} starts')
                                gantt_list.append(At[index_of_ON_process + 1])
                                msg.append(f'At time {gantt_list[-1]}, {Proc[index_of_ON_process + 1]} arrived/starts')
                                St[f'{Proc[index_of_ON_process + 1]}'] += [gantt_list[-1]]
                                gantt_label.append(Proc[index])
                                gantt_label.append(Proc[index_of_ON_process + 1])
                                print('sdsd')
                            
                            ON_process = Proc[index_of_ON_process + 1]
                            arrived.append(ON_process)
                            remaining[Proc[index]] += [Bt[index]]
                            remaining_table.append(deepcopy(remaining))
                            idle = 0
                            print('b')
                            break

                        else:
                            msg.append(f'At time {gantt_list[-1]}, {t} terminated - {Proc[index]} starts')
                            St[f'{Proc[index]}'] += [gantt_list[-1]]
                            gantt_list.append(time + gantt_list[-1])
                            idle -= time
                            Bt[index] = 0
                            ON_process_indexes.pop(0)
                            Finished.append(Proc[index])
                            Ft[f'{Proc[index]}'] += [gantt_list[-1]]
                            remaining[Proc[index]] += [Bt[index]]
                            remaining_table.append(deepcopy(remaining))
                            gantt_label.append(Proc[index])
                            t = Proc[index]

                            waiting = diff(arrived, Finished)
                            if idle != 0 and len(waiting) == 0:
                                ON_process = Proc[index_of_ON_process + 1]
                                arrived.append(ON_process)
                                gantt_list.append(At[index_of_ON_process + 1])
                                St[f'{Proc[index_of_ON_process + 1]}'] += [gantt_list[-1]]
                                msg.append(f'At time {gantt_list[-1]}, {Proc[index_of_ON_process + 1]} arrived/starts')
                                gantt_label.append('idle')
                                print('c')
                                idle = 0
                                break
                            print('c')
                            break
                            
            else: # Just idle
                ON_process = Proc[index_of_ON_process + 1]
                arrived.append(ON_process)
                gantt_list.append(At[index_of_ON_process + 1])
                St[f'{Proc[index_of_ON_process + 1]}'] += [gantt_list[-1]]
                gantt_label.append('idle')
                gantt_label.append(Proc[index_of_ON_process + 1])
                msg.append(f'At time {gantt_list[-1]}, {Proc[index_of_ON_process + 1]} arrived/starts')
                remaining_table.append(deepcopy(remaining))
                idle = 0

        if len(arrived) == len(Proc): # Begin Shortest Job First when all process arrived
            waiting = diff(arrived, Finished)
            ON_process_indexes = [Proc.index(waiting[o]) for o in range(len(waiting))]
            Bts = [Bt[i] for i in ON_process_indexes]

            for i in range(len(Bts)-1):
                for j in range(0, len(Bts)-i-1):
                    if Bts[j] > Bts[j+1]:
                        Bts[j], Bts[j+1] = Bts[j+1], Bts[j]
                        waiting[j], waiting[j+1] = waiting[j+1], waiting[j]
                        ON_process_indexes[j], ON_process_indexes[j+1] = ON_process_indexes[j+1], ON_process_indexes[j]

            while ON_process_indexes != []:
                index = ON_process_indexes[0]
                time = Bt[index]
                if gantt_list[-1] not in St[f'{Proc[index]}']:
                    St[f'{Proc[index]}'] += [gantt_list[-1]]
                    gantt_label.append(Proc[index])
                    msg.append(f'At time {gantt_list[-1]}, {t} terminated - {Proc[index]} starts')
                    
                gantt_list.append(time + gantt_list[-1])
                Ft[f'{Proc[index]}'] += [gantt_list[-1]]
                Bt[index] = 0
                Finished.append(Proc[index])
                remaining[Proc[index]] += [Bt[index]]
                remaining_table.append(deepcopy(remaining))
                t = Proc[index]
                if len(ON_process_indexes) == 1:
                    msg.append(f'At time {gantt_list[-1]}, {t} terminated')
                ON_process_indexes.pop(0)
            ON_process = None

    idle_sum = 0
    for i in range(len(gantt_label)):
        if gantt_label[i] == 'idle':
            idle_sum += gantt_list[i+1] - gantt_list[i]
    CPU_Utilization = ( 1 - (idle_sum / gantt_list[-1]) ) * 100

    gantt_list.pop(0)

    if len(gantt_list)+1 == len(msg) and len(gantt_list) == len(gantt_label):
        print('Good')
    else:
        print('Error may occur')

    return [gantt_list, gantt_label, msg, CPU_Utilization, St, Ft, process, burst_time, arrival_time, idle_sum, remaining_table]





''' --------------------ROUND ROBIN (Quantum Time = 5)----------------- '''

def round_robin(file_name):

    file = open(f'{file_name}.json')
    data = json.load(file)

    process = data['Process']
    burst_time = data['Burst Time']
    arrival_time = data['Arrival Time']

    file.close()

    process, burst_time, arrival_time = first_come_first_serve(process, burst_time, arrival_time)

    Proc = process.copy()
    Bt = burst_time.copy()
    At = arrival_time.copy()

    remaining = {}
    St = {}
    Ft = {}
    for i in range(len(Proc)):
        St[Proc[i]] = [At[i]]
        Ft[Proc[i]] = [At[i]]
        remaining[Proc[i]] = [Bt[i]]
    remaining_table = [deepcopy(remaining)]

    QT = 5
    if At[0] == 0:
        gantt_list = [0]
        labels = []
        msg = []
    else:
        gantt_list = [0, At[0]]
        labels = ['idle']
        msg = [f'At time 0, Idle']
        remaining_table.append(deepcopy(remaining))

    Finished = []
    arrived = Proc[:At.count(At[0])]

    t = ''
    index = 0
    while len(Finished) != len(Proc):
        waiting = diff(arrived, Finished)

        for p in range(index, len(waiting)):
            index_of_ON_process = Proc.index(waiting[p])

            if Bt[index_of_ON_process] == QT:
                labels.append(Proc[index_of_ON_process])
                if t == '':
                    msg.append(f'At time {gantt_list[-1]}, {Proc[index_of_ON_process]} starts')
                else:
                    msg.append(f'At time {gantt_list[-1]}, {t} terminated - {Proc[index_of_ON_process]} starts')
                
                St[f'{Proc[index_of_ON_process]}'] += [gantt_list[-1]]
                gantt_list.append(gantt_list[-1] + QT)
                Ft[f'{Proc[index_of_ON_process]}'] += [gantt_list[-1]]

                Bt[index_of_ON_process] -= QT
                remaining[waiting[p]] += [Bt[index_of_ON_process]]
                remaining_table.append(deepcopy(remaining))
                Finished.append(Proc[index_of_ON_process])
                t = Proc[index_of_ON_process]

                z = 0
                for arr in range(len(At)):
                    if gantt_list[-1] >= At[arr]:
                        if Proc[arr] not in arrived:
                            arrived.append(Proc[arr])
                            z = 1

                ''' Just like with compaction '''
                if len(labels) > 1:
                    if labels[-1] == labels[-2]:
                        gantt_list[-2] += QT
                        gantt_list.pop(-1)
                        labels.pop(-1)
                        St[f'{Proc[index_of_ON_process]}'].pop(-1)
                        msg.pop(-1)

            elif Bt[index_of_ON_process] > QT:
                labels.append(Proc[index_of_ON_process])
                if t == '':
                    msg.append(f'At time {gantt_list[-1]}, {Proc[index_of_ON_process]} starts')
                else:
                    msg.append(f'At time {gantt_list[-1]}, {t} terminated - {Proc[index_of_ON_process]} starts')
                    t = ''
                St[f'{Proc[index_of_ON_process]}'] += [gantt_list[-1]]
  
                gantt_list.append(gantt_list[-1] + QT)
                St[f'{Proc[index_of_ON_process]}'] += [gantt_list[-1]]
                Bt[index_of_ON_process] -= QT
                remaining[waiting[p]] += [Bt[index_of_ON_process]]
                remaining_table.append(deepcopy(remaining))

                z = 0
                for arr in range(len(At)):
                    if gantt_list[-1] >= At[arr]:
                        if Proc[arr] not in arrived:
                            arrived.append(Proc[arr])
                            z = 1

                if len(labels) > 1:
                    if labels[-1] == labels[-2]:
                        gantt_list[-2] += QT
                        gantt_list.pop(-1)
                        labels.pop(-1)
                        St[f'{Proc[index_of_ON_process]}'].pop(-1)
                        St[f'{Proc[index_of_ON_process]}'].pop(-1)
                        msg.pop(-1)
                
            
            else:
                labels.append(Proc[index_of_ON_process])
                if t == '':
                    msg.append(f'At time {gantt_list[-1]}, {Proc[index_of_ON_process]} starts')
                else:
                    msg.append(f'At time {gantt_list[-1]}, {t} terminated - {Proc[index_of_ON_process]} starts')

                St[f'{Proc[index_of_ON_process]}'] += [gantt_list[-1]]
                gantt_list.append(gantt_list[-1] + Bt[index_of_ON_process])
                Finished.append(Proc[index_of_ON_process])
                Ft[f'{Proc[index_of_ON_process]}'] += [gantt_list[-1]]

                z = 0
                for arr in range(len(At)):
                    if gantt_list[-1] >= At[arr]:
                        if Proc[arr] not in arrived:
                            arrived.append(Proc[arr])
                            z = 1

                Bt[index_of_ON_process] = 0
                remaining[waiting[p]] += [Bt[index_of_ON_process]]
                remaining_table.append(deepcopy(remaining))

                if len(labels) > 1:
                    if labels[-1] == labels[-2]:
                        gantt_list[-2] += Bt[index_of_ON_process]
                        gantt_list.pop(-1)
                        labels.pop(-1)
                        St[f'{Proc[index_of_ON_process]}'].pop(-1)
                        msg.pop(-1)
                
                t = Proc[index_of_ON_process]

            if z == 1:
                index += 1
                break

            elif len(waiting) != 0:
                if Proc[index_of_ON_process] == waiting[-1]:
                    waiting = diff(arrived, Finished)
                    if len(waiting) != 0:
                        index = 0
                    
                    else: # Idle
                        x = diff(Proc, Finished)
                        if len(x) != 0:
                            arrived.append(x[0])
                            gantt_list.append(At[Proc.index(x[0])])
                            St[f'{Proc[Proc.index(x[0])]}'] += [gantt_list[-1]]
                            remaining_table.append(deepcopy(remaining))
                            labels.append('idle')
                            index = 0
                            
    msg.append(f'At time {gantt_list[-1]}, {t} terminated')
    idle_sum = 0
    for i in range(len(labels)):
        if labels[i] == 'idle':
            idle_sum += gantt_list[i+1] - gantt_list[i]
    CPU_Utilization = ( 1 - (idle_sum / gantt_list[-1]) ) * 100

    gantt_list.pop(0)

    if len(St) == 1:
        St['P1'] = St['P1'][:2]

    if len(gantt_list)+1 == len(msg) and len(gantt_list) == len(labels):
        print('Good')
    else:
        print('Error may occur')

    return [gantt_list, labels, msg, CPU_Utilization, St, Ft, process, burst_time, arrival_time, idle_sum, remaining_table]

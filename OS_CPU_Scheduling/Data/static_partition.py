from fcn import *
import json
import re

def find_job_in_status(status, t):
    for s in range(len(status)):
        try:
            J = re.search(f'Allocated (.*)', status[s]).group(1)
            if t == J:
                return s
        except AttributeError:
            pass

def create_mem_map(status, loc, job_size):
    loc_copy = loc.copy()
    for i in range(len(status)):
        if 'Allocated' in status[i]:
            J = re.search(f'Allocated J(.*)', status[i]).group(1)
            x = status.index(status[i])
            x = loc.index(loc_copy[x])
            loc.insert(x+1, loc[x] + job_size[(int(J)-1)])
    return list(sorted(set(loc)))

def first_fit_available(status, job_index, P, J):
    for i in range(len(status)):
        if status[i] == 'available' and P[i] >= J[job_index]:
            return i


def static_partition_EXEC(file_name):
    file = open(f'{file_name}.json')
    data = json.load(file)

    MEMORY_SIZE = data['Memory size']
    OS_SIZE = data['OS size']
    PARTITION_SIZE = data['Partition size']
    PARTITION_SIZE = [i for i in PARTITION_SIZE if i != 0]

    jobs = data['Job']
    job_size = data['Size']
    arrival_time = data['Arrival time']
    run_time = data['Run time']

    file.close()

    if OS_SIZE <= 0 or MEMORY_SIZE <= OS_SIZE:
        print('Invalid memory size')
        exit()

    LOCATION = [OS_SIZE]

    total_PARTITION_SIZE = (sum(PARTITION_SIZE)+OS_SIZE)
    if total_PARTITION_SIZE <= MEMORY_SIZE:
        if (MEMORY_SIZE - total_PARTITION_SIZE) != 0:
            PARTITION_SIZE.append(MEMORY_SIZE - total_PARTITION_SIZE)
    else:
        print('Invalid partition')
        exit()

    for i in PARTITION_SIZE:
        LOCATION.append(i + LOCATION[-1])
    status = ['available']*len(PARTITION_SIZE)

    Ft = {}
    St = {}
    for i in jobs:
        Ft[f'{i}'] = '' 
        St[f'{i}'] = '' 

    ter = ''
    terminating = {}
    waiting = []
    msg = [f'Before {arrival_time[0]}']

    status_table = [status]
    job_index = 0
    LOC = [LOCATION]
    for job_index in range(len(arrival_time)):
        # status = status.copy()
        arrival_minutes = to_minutes(arrival_time[job_index])
        # Terminated
        if len(terminating) > 0:
            for _ in range(list(terminating.values()).count(list(terminating.values())[0])):
                if arrival_minutes >= list(terminating.values())[0]:
                    ter = list(terminating.values())[0]
                    t_time = time_format('00:'+str(ter))
                    msg.append(f'At {t_time}, {list(terminating)[0]} terminated')
                    x = find_job_in_status(status, list(terminating)[0])
                    terminating.pop(list(terminating)[0])
                    status[x] = 'available'
                    status_table.append(list(status))
                    LOC.append(create_mem_map(status, LOCATION.copy(), job_size))

        # Waiting starts
        if len(waiting) != 0:
            status_index = first_fit_available(status, waiting[0], PARTITION_SIZE, job_size)
            for w in waiting:
                if status_index != None:
                    if status[status_index] == 'available' and PARTITION_SIZE[status_index] >= job_size[w]:
                        tf = time_format('00:'+str(ter))
                        msg.append(f'At {tf}, J{waiting[0]+1} starts')
                        status[status_index] = f'Allocated J{w+1}'
                        status_table.append(list(status))
                        LOC.append(create_mem_map(status, LOCATION.copy(), job_size))
                        terminating[f'J{w+1}'] = ter + run_time[w]
                        terminating = {k: v for k, v in sorted(terminating.items(), key=lambda item: item[1])} # Sort dict by values
                        St[f'{w+1}'] = time_format('00:'+str(ter))
                        Ft[f'{w+1}'] = time_format('00:'+str(ter + run_time[w]))
                        waiting.pop(0)

        # Waits
        status_index = first_fit_available(status, job_index, PARTITION_SIZE, job_size)
        if status_index == None:
            waiting.append(job_index)
        elif len(waiting) != 0:
            if arrival_minutes > to_minutes(arrival_time[waiting[0]]):
                waiting.append(job_index)
        # Arrived/Starts
        else:
            if status[status_index] == 'available' and PARTITION_SIZE[status_index] >= job_size[job_index]:
                msg.append(f'At {arrival_time[job_index]}, J{job_index+1} arrived/starts')
                status[status_index] = f'Allocated J{job_index+1}'
                status_table.append(list(status))
                LOC.append(create_mem_map(status, LOCATION.copy(), job_size))
                terminating[f'J{job_index+1}'] = arrival_minutes + run_time[job_index]
                terminating = {k: v for k, v in sorted(terminating.items(), key=lambda item: item[1])} # Sort dict by values
                St[f'{job_index+1}'] = arrival_time[job_index]
                Ft[f'{job_index+1}'] = time_format('00:'+str(arrival_minutes + run_time[job_index]))

    while len(waiting) > 0: # Start the jobs in waiting queues
        status_index = first_fit_available(status, waiting[0], PARTITION_SIZE, job_size)
        if status_index == None:
            for _ in range(list(terminating.values()).count(list(terminating.values())[0])):
                ter = list(terminating.values())[0]
                t_time = time_format('00:'+str(ter))
                msg.append(f'At {t_time}, {list(terminating)[0]} terminated')
                x = find_job_in_status(status, list(terminating)[0])
                terminating.pop(list(terminating)[0])
                status[x] = 'available'
                status_table.append(list(status))
                LOC.append(create_mem_map(status, LOCATION.copy(), job_size))
        else:
            for w in waiting:
                if status_index != None:
                    if status[status_index] == 'available' and PARTITION_SIZE[status_index] >= job_size[w]:
                        tf = time_format('00:'+str(ter))
                        msg.append(f'At {tf}, J{waiting[0]+1} starts')
                        status[status_index] = f'Allocated J{w+1}'
                        status_table.append(list(status))
                        LOC.append(create_mem_map(status, LOCATION.copy(), job_size))
                        terminating[f'J{w+1}'] = ter + run_time[w]
                        terminating = {k: v for k, v in sorted(terminating.items(), key=lambda item: item[1])} # Sort dict by values
                        St[f'{w+1}'] = time_format('00:'+str(ter))
                        Ft[f'{w+1}'] = time_format('00:'+str(ter + run_time[w]))
                        waiting.pop(0)
    else:
        for i in range(len(terminating)):
            try:
                ter = list(terminating.values())[0]
                t_time = time_format('00:'+str(ter))
                msg.append(f'At {t_time}, {list(terminating)[0]} terminated')
                x = find_job_in_status(status, list(terminating)[0])
                terminating.pop(list(terminating)[0])
                status[x] = 'available'
                status_table.append(list(status))
                LOC.append(create_mem_map(status, LOCATION.copy(), job_size))
            except TypeError:
                pass

    CPU_Wait = [to_minutes(list(St.values())[i]) - to_minutes(arrival_time[i]) for i in range(len(list(St.values())))]
    Start = list(St.values())
    Finish = list(Ft.values())

    x = generate_memory_label(LOC, status_table, LOCATION, fixed=False)[0]
    for i in range(len(x)):
        for j in range(len(x[i])):
            try:
                W = re.search(f'wasted(.*)', x[i][j]).group(1)
                if 'wasted' in x[i][j]:
                    j_index = 0
                    num = ''
                    for k in range(len(x[i][j-1])):
                        if x[i][j-1][k].isdigit():
                            num += x[i][j-1][k]
                    j_index = int(num)
                    x[i][j] = f'wasted ({PARTITION_SIZE[int(W)-1] - job_size[j_index-1]})'
            except (AttributeError, ValueError):
                pass

    for i in range(len(x)):
        for j in range(len(x[i])):
            try:
                J = re.search(f'J(.*)', x[i][j]).group(1)
                if 'J' in x[i][j]:
                    x[i][j] += f' ({job_size[int(J)-1]})'
            except (AttributeError, ValueError):
                pass

    for i in range(len(x)):
        for j in range(len(x[i])):
            try:
                P = re.search(f'P(.*)', x[i][j]).group(1)
                if 'P' in x[i][j]:
                    x[i][j] += f' ({PARTITION_SIZE[int(P)-1]})'
            except (AttributeError, ValueError):
                pass

    print()
    print('Start: ', Start)
    print('Finish: ', Finish)
    print('CPU_Wait: ', CPU_Wait)
    print()
    print(len(msg) == len(LOC) == len(status_table))

    return [LOC, x, msg, status_table, PARTITION_SIZE, Start, Finish, CPU_Wait]

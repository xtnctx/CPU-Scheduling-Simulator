from fcn import *
import json


def single_contiguous_EXEC(file_name):
    # Opening JSON file
    file = open(f'{file_name}.json')
    data = json.load(file)

    MEMORY_SIZE = data['Memory size']
    OS_SIZE = data['OS size']

    jobs = data['Job']
    job_size = data['Size']
    arrival_time = data['Arrival time']
    run_time = data['Run time']

    file.close()

    if OS_SIZE <= 0 or MEMORY_SIZE <= OS_SIZE:
        print('Invalid memory size')
        exit()

    starting_time = [None if arrival_time == [] else arrival_time[0]] # first job arrived/starts
    wasted_list = []
    CPU_wait_time = []
    idle_time = []
    job_terminated_list = []


    wasted = MEMORY_SIZE - OS_SIZE # wasted memory is also the free/availabe memory
    f = 0
    ff = []
    msg = [f'Before {arrival_time[0]}']
    LOC = [[OS_SIZE, MEMORY_SIZE]]
    mem_label = [['OS', f'Memory Available ({wasted})']]

    for i in range(len(job_size)):
        minute = to_minutes(starting_time[i]) + run_time[i] # starting time + run time = next starting time
        if wasted >= job_size[i]:
            wasted -= job_size[i] # start the job
            wasted_list.append(wasted)
            
            if to_minutes(arrival_time[i]) < f:
                print(f'At {arrival_time[i]} J{i+1} waits')
                ff.append(f'J{i+1}')
            
            if cpu_wait_time(starting_time[i], arrival_time[i]) < 0:
                # Appends the abs(idle_time) to list then adds to the minute to avoid delays
                idle_time.append(list_of_idle_time(starting_time[i], arrival_time[i]))
                minute += abs(cpu_wait_time(starting_time[i], arrival_time[i]))
                # Because of idle time, the starting time of the job must start in its arrival time
                starting_time[i] = arrival_time[i] 
                
            else:
                idle_time.append('-')
            
            if arrival_time[i] != starting_time[i]:
                msg.append(f'At {starting_time[i]} J{i+1} starts')

            else:
                msg.append(f'At {starting_time[i]} J{i+1} arrived/starts')

            starting_time.append(time_format('00:'+ str(minute))) # appends minute in time format
            LOC.append([OS_SIZE, OS_SIZE+job_size[i], MEMORY_SIZE])
            mem_label.append(['OS', f'J{i+1} ({job_size[i]})', f'Wasted ({wasted})'])
        else:
            arrival_time = arrival_time[:len(starting_time)-1] # makes the length of input upto the valid input
            print(f'Not enough memory for Job #{i+1}')
            break

        xt = time_format('00:'+ str(minute))
        msg.append(f'At {xt} J{i+1} terminated')
        job_terminated_list.append(xt)
        LOC.append([OS_SIZE, MEMORY_SIZE])
        wasted += job_size[i] # job done
        mem_label.append(['OS', f'Memory Available ({wasted})'])
    starting_time.pop(-1)
    CPU_wait_time = list_of_CWT(starting_time, arrival_time)  

    input_time = is_12_hour_format(arrival_time) #Auto detect input time format, output is 12 hour format by default
    if input_time:
        for i in range(len(starting_time)):
            starting_time[i] = time_format(starting_time[i], format='12')
            arrival_time[i] = time_format(arrival_time[i], format='12')
            job_terminated_list[i] = time_format(job_terminated_list[i], format='12')
            s = starting_time[i].split(':')
            a = arrival_time[i].split(':')
            if int(a[0]) > int(s[0]):
                s[0] = int(s[0]) + 12
                CPU_wait_time[i] = (cpu_wait_time(f'{s[0]}:{s[1]}', arrival_time[i]))
            else:
                CPU_wait_time[i] = (cpu_wait_time(starting_time[i], arrival_time[i]))
    else:
        to_24hr_format(arrival_time)
        CPU_wait_time = list_of_CWT(starting_time, arrival_time)  
    Finish = [time_format('00:'+str(to_minutes(starting_time[i]) + run_time[i])) for i in range(len(starting_time))]
    
    for i in range(len(mem_label)):
        if mem_label[i][-1] == 'Wasted (0)':
            mem_label[i].pop(-1)
            LOC[i].pop(-1)

    return [LOC, mem_label, msg, starting_time, Finish, CPU_wait_time]

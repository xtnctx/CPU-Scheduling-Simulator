import re

def time_format(time, format='24'):
    k = time.split(':')
    if int(k[1]) >= 60:
        k[0] = int(k[0]) + (int(k[1])//60)
        k[1] = int(k[1]) - 60*(int(k[1])//60)
        if len(str(k[1])) == 1:
            k[1] = str(k[1]) + '0'
            k[1] = k[1][::-1]
    if format == '12' and int(k[0]) > 12:
        k[0] = int(k[0])-12
    return ':'.join([str(i) for i in k])

# Converts a 12-hour format to calculate the time in minutes
def to_24hr_format(time):
    half_time = False
    for i in range(len(time)):
        a = time[i].split(':')
        if int(a[0]) == 12:
            half_time = True
        if half_time and int(a[0]) < 12:
            time[i] = f'{int(a[0])+12}:{a[1]}'
    return time

def to_minutes(time):
    m = time.split(':')
    return (int(m[0])*60) + int(m[1])

def cpu_wait_time(stt,art):
    s = stt.split(':')
    a = art.split(':')
    return ((int(s[0]) - int(a[0]))*60) + (int(s[1]) - int(a[1]))

def list_of_idle_time(stt,art):
    if cpu_wait_time(stt,art) < 0:
        return f'{abs(cpu_wait_time(stt,art))} minutes'
    else:
        return cpu_wait_time(stt,art)

def list_of_CWT(stt,art):
    time_in_minutes = []
    for i in range(len(stt)):
        s = stt[i].split(':')
        a = art[i].split(':')
        time_diff = ((int(s[0]) - int(a[0]))*60) + (int(s[1]) - int(a[1]))
        time_in_minutes.append(time_diff)
    return time_in_minutes

def xround(num):
    num = str(num)
    x = num.split('.')
    if len(x) == 1:
        return int(num)
    else:
        if int(x[1][0]) > 4:
            return int(x[0]) + 1
        return int(x[0])

#Detect input time format
def is_12_hour_format(time):
    for i in range(len(time)):
        a = time[i].split(':')
        if int(a[0]) > 12:
            return False
    return True
    
def sort_time(time_list):
    minutes = []
    for time in time_list:
        minutes.append(to_minutes(time))
    sorted_time = []
    for s in sorted(minutes):
        sorted_time.append(time_format('00:'+str(s)))
    return sorted_time

def sort_by_process(d):
    process = list(d.keys())
    values = list(d.values())
    
    for i in range(len(process)-1):
        for j in range(0, len(process)-i-1):
            if int(re.search('P(.*)', process[j]).group(1)) > int(re.search('P(.*)', process[j+1]).group(1)):
                process[j], process[j+1] = process[j+1], process[j]
                values[j], values[j+1] = values[j+1], values[j]
    
    newD = {}
    for i in range(len(process)):
        newD[process[i]] = values[i]
    return newD

def generate_str_SUM(d):
    d = sort_by_process(d)
    d_val = list(d.values())
    string = ''
    newList = []
    s = 0
    for i in range(len(d_val)):
        d_val[i] = sorted(d_val[i], reverse=True)
        for j in range(len(d_val[i])):
            if len(string) != 0:
                if string[-1] == '-':
                    string += str(d_val[i][j]) + ' + '
                    s -= d_val[i][j]
                else:
                    string += str(d_val[i][j]) + '-'
                    s += d_val[i][j]
            
            else:
                string += str(d_val[i][j]) + '-'
                s += d_val[i][j]
            if j+1 == len(d_val[i]):
                string = string[:-3]
                newList.append(string)
                string = ''

    return [newList, s]
# St = {'P1': [4, 4, 5, 15], 'P2': [5, 5], 'P4': [7, 26], 'P3': [10, 33]}
# Ft = {'P1': [4, 26], 'P2': [5, 15], 'P4': [7, 33], 'P3': [10, 38]}
# print(generate_str_SUM(Ft))

def first_come_first_serve(process, burst_time, arrival_time, priority_num=None):
    # Sort by Arrival
    for i in range(len(arrival_time)-1):
        for j in range(0, len(arrival_time)-i-1):
            if arrival_time[j] > arrival_time[j+1]:
                arrival_time[j], arrival_time[j+1] = arrival_time[j+1], arrival_time[j]
                burst_time[j], burst_time[j+1] = burst_time[j+1], burst_time[j]
                process[j], process[j+1] = process[j+1], process[j]
                if priority_num != None:
                    priority_num[j], priority_num[j+1] = priority_num[j+1], priority_num[j]
    if priority_num != None:
        return [process, burst_time, arrival_time, priority_num]
    else:
        return [process, burst_time, arrival_time]

def diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif

### GUI ###
# Memory map pointers
def margin_memory_loc(mem_map, V_END, y=30, fixed = False):
    cur = []
    if not fixed:
        os_pointer = int(V_END*(mem_map[0]/mem_map[-1])) - 60 # 60 = default os pointer
        for i in range(len(mem_map)):
            mem_map_pointer = int(V_END*(mem_map[i]/mem_map[-1]))
            cur.append(mem_map_pointer)
        if os_pointer > 14:
            for size in range(len(cur)-1):
                cur[size] -= os_pointer
        elif os_pointer <= 0:
            for size in range(len(cur)-1):
                cur[size] -= os_pointer
                

        for i in range(len(cur)-1):
            if i > 0 and i != len(cur)-1:
                if abs(cur[i-1] - cur[i]) < y:
                    for num in range(i, len(cur)-1):
                        cur[num] += y
                        if cur[num] >= cur[-1]:
                            cur[num] -= y
        _x2 = cur[-2]
        if (_x2 > V_END) and cur[1] - cur[0] > (_x2 - V_END)+25:
            for i in range(len(cur)-2, 0, -1):
                cur[i] -= (_x2 - V_END)+25

        if int(V_END*(mem_map[-1]/mem_map[-1])) - int(V_END*(mem_map[-2]/mem_map[-1])) >= 20:
            if (int(V_END*(mem_map[-2]/mem_map[-1]))  - cur[-2]) > 100:
                cur[-2] = int(V_END*(mem_map[-2]/mem_map[-1]))
                
            for i in range(len(cur)-2):
                cur[i] += (cur[-2] - _x2)

        if (cur[1] - cur[0]) > 30: 
            for i in range(len(cur)-1, 0, -1):
                if cur[i] - cur[i-1] < y:
                    for num in range(i, 1, -1):
                        cur[num-1] -= y
        return cur
    else:
        x = V_END/(len(mem_map))
        for i in range(len(mem_map)):
            cur.append(int(x*(i+1)))
        return cur

def memory_label_yloc(mem_map, fixed):
    memory_label_loc = []
    for y in range(len(mem_map)):
        cur = margin_memory_loc(mem_map[y], mem_map[y][-1], y=30, fixed=fixed)
        temp2 = [cur[0]//2]
        for i in range(1, len(cur)):
            mid = (cur[i-1] + cur[i])//2
            temp2.append(mid)
        memory_label_loc.append(temp2)
        temp2 = []
    return memory_label_loc

# print(memory_label_yloc([[60, 411]], False))

# Memory map labels
def generate_memory_label(mem_map, status_table, location, fixed=False):
    memory_label = []
    temp, allocatee, wasted_index, left = [], [], [], []
    for row in range(len(mem_map)):
        for stats in range(len(status_table[row])):
            if status_table[row][stats] != 'available':
                for i in range(len(mem_map[row])):
                    if mem_map[row][i] not in location:
                        try:
                            J = re.search('J(.*)', status_table[row][stats]).group(1)
                            if f'J{J}' not in temp:
                                temp.append(f'J{J}')
                        except AttributeError:
                            pass

                        for j in range(i):
                            if mem_map[row][j] < mem_map[row][i] and mem_map[row][j] in location:
                                left.append(mem_map[row][j])
                        if max(left) not in wasted_index:
                            wasted_index.append(max(left))
                        if i not in allocatee:
                            allocatee.append(i)

                    elif mem_map[row][i] in location and status_table[row][stats] != 'available':
                        try:
                            J = re.search('J(.*)', status_table[row][stats]).group(1)
                            if f'J{J}' not in temp:
                                temp.append(f'J{J}')
                        except AttributeError:
                            pass
                left = []
            else:
                if f'P({stats+1})' not in temp:
                    temp.append(f'P{stats+1}')

        for waste in range(len(wasted_index)):
            temp.insert(allocatee[waste], f'wasted (P{location.index(wasted_index[waste])+1})')
        temp.insert(0, 'OS')
        memory_label.append(temp)
        temp, allocatee, wasted_index = [], [], []
    
    # Memory label y-position
    yLoc = memory_label_yloc(mem_map, fixed)

    return memory_label, yLoc

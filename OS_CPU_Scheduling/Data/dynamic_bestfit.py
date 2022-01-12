from fcn import *
import json
import re

def waiting_job(c_loc, starts):
    for i in range(len(c_loc)):
        for j in range(len(starts)):
            try:
                if c_loc[i] == starts[j]:
                    c_loc.pop(i)
            except IndexError:
                pass
    return c_loc

def time_end(start_time, run_time):
    return time_format('00:'+str(to_minutes(start_time) + run_time))

def dynamic_bestfit_EXEC(file_name, with_compaction):
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

    # Partition Allocation Table (PAT)
    pat = {'Partition' : [1],
        'S' : ['-'],
        'Loc' : ['-'],
        'Status' : ['ee']}
    p_list = [pat.copy()]

    # Free Allocation Table (FAT)
    fat = {'FA#' : [1],
        'S' : [MEMORY_SIZE-OS_SIZE],
        'Loc' : [OS_SIZE],
        'Status' : ['Available']}


    fat['S'] = [MEMORY_SIZE-OS_SIZE]
    f_list = [fat.copy()]

    waiting = []
    terminating = {}

    # FAT.copy()
    FA_num = [1]
    Fs = [MEMORY_SIZE-OS_SIZE]
    Floc =  [OS_SIZE]
    Fstatus = ['Available']

    # PAT.copy()
    process = []
    Ps = []
    Ploc = []
    Pstatus = []

    t = ''
    started_jobs = []
    message = [f'Before {arrival_time[0]}']

    Ft = {}
    St = {}
    for i in jobs:
        Ft[f'{i}'] = '' 
        St[f'{i}'] = '' 

    for job_index in range(len(arrival_time)):
        arrival_minutes = to_minutes(arrival_time[job_index])
        # Terminated
        if len(terminating) > 0:
            for _ in range(list(terminating.values()).count(list(terminating.values())[0])):
                if arrival_minutes >= list(terminating.values())[0]:
                    t_time = time_format('00:'+str(list(terminating.values())[0]))
                    message.append(f'At {t_time} J{list(terminating)[0]} terminated')
                    for s in range(len(pat['Status'])):
                        try:
                            J = re.search(f'J(.*)', pat['Status'][s]).group(1)
                            if int(J) == list(terminating)[0]:
                                FA_num.append(FA_num[-1]+1)
                                Fstatus.append('Available')
                                Fs.append(pat['S'][s])
                                Floc.append(pat['Loc'][s])

                                fat['FA#'] = [i+1 for i in range(len(Fs))]
                                fat['S'] = Fs.copy()
                                fat['Loc'] = Floc.copy()
                                fat['Status'] = Fstatus.copy()

                                # Sort by location
                                for i in range(len(fat['Loc'])-1):
                                    for j in range(0, len(fat['Loc'])-i-1):
                                        if fat['Loc'][j] > fat['Loc'][j+1] :
                                            fat['Loc'][j], fat['Loc'][j+1] = fat['Loc'][j+1], fat['Loc'][j]
                                            Floc = fat['Loc']
                                            fat['S'][j], fat['S'][j+1] = fat['S'][j+1], fat['S'][j]
                                            Fs = fat['S']
                                # Compress size
                                end = False
                                while not end:
                                    if len(Floc) > 1:
                                        for item in range(len(Floc)-1):
                                            x = Fs[item] + Floc[item]
                                            if Floc[item+1] == x:
                                                Fs[item] = Fs[item] + Fs[item+1]
                                                FA_num.pop(-1)
                                                Floc.pop(item+1)
                                                Fs.pop(item+1)
                                                Fstatus.pop(-1)
                                                break
                                            elif item == len(Floc)-2:
                                                end = True
                                    else:
                                        end = True
                                
                                fat['FA#'] = [i+1 for i in range(len(Fs))]
                                fat['S'] = Fs.copy()
                                fat['Loc'] = Floc.copy()
                                fat['Status'] = Fstatus.copy()
                                
                                process.pop(-1)
                                Ps.pop(s)
                                Ploc.pop(s)
                                Pstatus.pop(s)

                                if process == []:
                                    pat = {'Partition' : [1],
                                            'S' : ['-'],
                                            'Loc' : ['-'],
                                            'Status' : ['ee']}
                                else:
                                    pat['Partition'] = [i+1 for i in range(len(Ps))]
                                    pat['S'] = Ps.copy()
                                    pat['Loc'] = Ploc.copy()
                                    pat['Status'] = Pstatus.copy()
                        except (AttributeError, IndexError):
                            pass
                    t = list(terminating.values())[0]
                    terminating.pop(list(terminating)[0])
                    
                    if with_compaction and pat['S'] != ['-']:
                        loc = [OS_SIZE]
                        for size in Ps:
                            loc.append(size + loc[-1])

                        FA_num = [1]
                        Fs = [sum(Fs)]
                        Floc = [loc.pop(-1)]
                        Fstatus = ['Available']
                        Ploc = loc

                        fat['FA#'] = FA_num.copy()
                        fat['S'] = Fs.copy()
                        fat['Loc'] = Floc.copy()
                        fat['Status'] = Fstatus.copy()

                        pat['Partition'] = [i+1 for i in range(len(Ps))]
                        pat['S'] = Ps.copy()
                        pat['Loc'] = Ploc.copy()
                        pat['Status'] = Pstatus.copy()
                    f_list.append(fat.copy())
                    p_list.append(pat.copy())

        # Waiting
        if len(waiting) != 0:
            # print(f'At {arrival_time[waiting[0]]} J{waiting[0]+1} waits')
            fits = []
            for w in waiting:
                for s in Fs:
                    if job_size[w] <= s:
                        fits.append(s)
                # Waiting starts
                if len(fits) != 0:
                    best_fit = min(fits)
                    started_jobs.append(waiting[0])

                    tf = time_format('00:'+str(t))
                    St[f'{waiting[0]+1}'] = tf
                    Ft[f'{waiting[0]+1}'] = time_end(tf, run_time[waiting[0]])
                    message.append(f'At {tf} J{waiting[0]+1} starts')

                    process.append(w+1)
                    Ps.append(job_size[w])
                    Ploc.append(Floc[Fs.index(best_fit)])
                    Pstatus.append(f'Allocated J{w+1}')

                    if len(process) > 1:
                        pat['Partition'] = [i+1 for i in range(len(Ps))]
                        pat['S'] = Ps.copy()
                        pat['Loc'] = Ploc.copy()
                        pat['Status'] = Pstatus.copy()
                        # Sort by location
                        for i in range(len(pat['Loc'])-1):
                            for j in range(0, len(pat['Loc'])-i-1):
                                if pat['Loc'][j] > pat['Loc'][j+1] :
                                    pat['Loc'][j], pat['Loc'][j+1] = pat['Loc'][j+1], pat['Loc'][j]
                                    Ploc = pat['Loc']
                                    pat['S'][j], pat['S'][j+1] = pat['S'][j+1], pat['S'][j]
                                    Ps = pat['S']
                                    pat['Status'][j], pat['Status'][j+1] = pat['Status'][j+1], pat['Status'][j]
                                    Pstatus = pat['Status']
                        pat['Partition'] = [i+1 for i in range(len(Ps))]
                        pat['S'] = Ps.copy()
                        pat['Loc'] = Ploc.copy()
                        pat['Status'] = Pstatus.copy()
                    else:
                        pat['S'] = [job_size[w]]
                        pat['Loc'] = fat['Loc']
                        pat['Status'] = [f'Allocated J{w+1}']
                    
                    Floc[Fs.index(best_fit)] += job_size[w]
                    Fs[Fs.index(best_fit)] -= job_size[w]

                    fat['S'] = Fs.copy()
                    fat['Loc'] = Floc.copy()

                    terminating[w+1] = t + run_time[w]
            
                    terminating = {k: v for k, v in sorted(terminating.items(), key=lambda item: item[1])} # Sort dict by values
                    waiting.pop(0)
                    waiting = waiting_job(waiting, started_jobs)
                    f_list.append(fat.copy())
                    p_list.append(pat.copy())

        fits = []
        for s in Fs:
            if job_size[job_index] <= s:
                fits.append(s)
            elif len(waiting) != 0:
                if arrival_minutes > to_minutes(arrival_time[waiting[0]]):
                    waiting.append(job_index)
            elif job_size[job_index] > s:
                waiting.append(job_index)
        
        # Arrived/Starts
        if len(fits) != 0:
            best_fit = min(fits)
            message.append(f'At {arrival_time[job_index]} J{job_index+1} arrived/starts')
            started_jobs.append(job_index)
            process.append(job_index+1)
            Ps.append(job_size[job_index])
            Ploc.append(Floc[Fs.index(best_fit)])
            Pstatus.append(f'Allocated J{job_index+1}')

            St[f'{job_index+1}'] = arrival_time[job_index]
            Ft[f'{job_index+1}'] = time_end(arrival_time[job_index], run_time[job_index])

            if len(process) > 1:
                pat['Partition'] = [i+1 for i in range(len(Ps))]
                pat['S'] = Ps.copy()
                pat['Loc'] = Ploc.copy()
                pat['Status'] = Pstatus.copy()
                # Sort by location
                for i in range(len(pat['Loc'])-1):
                    for j in range(0, len(pat['Loc'])-i-1):
                        if pat['Loc'][j] > pat['Loc'][j+1] :
                            pat['Loc'][j], pat['Loc'][j+1] = pat['Loc'][j+1], pat['Loc'][j]
                            Ploc = pat['Loc']
                            pat['S'][j], pat['S'][j+1] = pat['S'][j+1], pat['S'][j]
                            Ps = pat['S']
                            pat['Status'][j], pat['Status'][j+1] = pat['Status'][j+1], pat['Status'][j]
                            Pstatus = pat['Status']
                pat['Partition'] = [i+1 for i in range(len(Ps))]
                pat['S'] = Ps.copy()
                pat['Loc'] = Ploc.copy()
                pat['Status'] = Pstatus.copy()
            else:
                pat['S'] = [job_size[job_index]]
                pat['Loc'] = fat['Loc']
                pat['Status'] = [f'Allocated J{job_index+1}']
            
            Floc[Fs.index(best_fit)] += job_size[job_index]
            Fs[Fs.index(best_fit)] -= job_size[job_index]

            fat['S'] = Fs.copy()
            fat['Loc'] = Floc.copy()

            terminating[job_index+1] = arrival_minutes + run_time[job_index]
            terminating = {k: v for k, v in sorted(terminating.items(), key=lambda item: item[1])} # Sort dict by values
            waiting = waiting_job(waiting, started_jobs)
            f_list.append(fat.copy())
            p_list.append(pat.copy())

    while len(waiting) > 0: # Start the jobs in waiting queues
        arrival_minutes = to_minutes(arrival_time[waiting[0]])
        fits = []
        for s in Fs:
            if job_size[waiting[0]] <= s:
                fits.append(s)
            
        if fits == []:
            for _ in range(list(terminating.values()).count(list(terminating.values())[0])):
                for s in range(len(pat['Status'])):
                    try:
                        J = re.search(f'J(.*)', pat['Status'][s]).group(1)
                        if int(J) == list(terminating)[0]:
                            t_time = time_format('00:'+str(list(terminating.values())[0]))
                            message.append(f'At {t_time} J{list(terminating)[0]} terminated')

                            FA_num.append(FA_num[-1]+1)
                            Fstatus.append('Available')
                            Fs.append(pat['S'][s])
                            Floc.append(pat['Loc'][s])

                            fat['FA#'] = [i+1 for i in range(len(Fs))]
                            fat['S'] = Fs.copy()
                            fat['Loc'] = Floc.copy()
                            fat['Status'] = Fstatus.copy()

                            # Sort by location
                            for i in range(len(fat['Loc'])-1):
                                for j in range(0, len(fat['Loc'])-i-1):
                                    if fat['Loc'][j] > fat['Loc'][j+1] :
                                        fat['Loc'][j], fat['Loc'][j+1] = fat['Loc'][j+1], fat['Loc'][j]
                                        Floc = fat['Loc']
                                        fat['S'][j], fat['S'][j+1] = fat['S'][j+1], fat['S'][j]
                                        Fs = fat['S']
                            # Compress size
                            end = False
                            while not end:
                                if len(Floc) > 1:
                                    for item in range(len(Floc)-1):
                                        x = Fs[item] + Floc[item]
                                        if Floc[item+1] == x:
                                            Fs[item] = Fs[item] + Fs[item+1]
                                            FA_num.pop(-1)
                                            Floc.pop(item+1)
                                            Fs.pop(item+1)
                                            Fstatus.pop(-1)
                                            break
                                        elif item == len(Floc)-2:
                                            end = True
                                else:
                                    end = True
                            
                            fat['FA#'] = [i+1 for i in range(len(Fs))]
                            fat['S'] = Fs.copy()
                            fat['Loc'] = Floc.copy()
                            fat['Status'] = Fstatus.copy()
                            
                            process.pop(-1)
                            Ps.pop(s)
                            Ploc.pop(s)
                            Pstatus.pop(s)

                            if process == []:
                                pat = {'Partition' : [1],
                                        'S' : ['-'],
                                        'Loc' : ['-'],
                                        'Status' : ['ee']}
                            else:
                                pat['Partition'] = [i+1 for i in range(len(Ps))]
                                pat['S'] = Ps.copy()
                                pat['Loc'] = Ploc.copy()
                                pat['Status'] = Pstatus.copy()
                    except (AttributeError, IndexError):
                        pass
                t = list(terminating.values())[0]
                terminating.pop(list(terminating)[0])

                if with_compaction and pat['S'] != ['-']:
                    loc = [OS_SIZE]
                    for size in Ps:
                        loc.append(size + loc[-1])

                    FA_num = [1]
                    Fs = [sum(Fs)]
                    Floc = [loc.pop(-1)]
                    Fstatus = ['Available']
                    Ploc = loc

                    fat['FA#'] = FA_num.copy()
                    fat['S'] = Fs.copy()
                    fat['Loc'] = Floc.copy()
                    fat['Status'] = Fstatus.copy()

                    pat['Partition'] = [i+1 for i in range(len(Ps))]
                    pat['S'] = Ps.copy()
                    pat['Loc'] = Ploc.copy()
                    pat['Status'] = Pstatus.copy()
                f_list.append(fat.copy())
                p_list.append(pat.copy())

        else:
            for w in waiting:
                fits = []
                for s in Fs:
                    if job_size[w] <= s:
                        fits.append(s)
                # Waiting starts
                if len(fits) != 0:
                    best_fit = min(fits)
                    started_jobs.append(waiting[0])

                    tf = time_format('00:'+str(t))
                    St[f'{waiting[0]+1}'] = tf
                    Ft[f'{waiting[0]+1}'] = time_end(tf, run_time[waiting[0]])
                    message.append(f'At {tf} J{waiting[0]+1} starts')
                    
                    process.append(w+1)
                    Ps.append(job_size[w])
                    Ploc.append(Floc[Fs.index(best_fit)])
                    Pstatus.append(f'Allocated J{w+1}')

                    if len(process) > 1:
                        pat['Partition'] = [i+1 for i in range(len(Ps))]
                        pat['S'] = Ps.copy()
                        pat['Loc'] = Ploc.copy()
                        pat['Status'] = Pstatus.copy()
                        # Sort by location
                        for i in range(len(pat['Loc'])-1):
                            for j in range(0, len(pat['Loc'])-i-1):
                                if pat['Loc'][j] > pat['Loc'][j+1] :
                                    pat['Loc'][j], pat['Loc'][j+1] = pat['Loc'][j+1], pat['Loc'][j]
                                    Ploc = pat['Loc']
                                    pat['S'][j], pat['S'][j+1] = pat['S'][j+1], pat['S'][j]
                                    Ps = pat['S']
                                    pat['Status'][j], pat['Status'][j+1] = pat['Status'][j+1], pat['Status'][j]
                                    Pstatus = pat['Status']
                        pat['Partition'] = [i+1 for i in range(len(Ps))]
                        pat['S'] = Ps.copy()
                        pat['Loc'] = Ploc.copy()
                        pat['Status'] = Pstatus.copy()
                        
                    else:
                        pat['S'] = [job_size[w]]
                        pat['Loc'] = fat['Loc']
                        pat['Status'] = [f'Allocated J{w+1}']
                    
                    Floc[Fs.index(best_fit)] += job_size[w]
                    Fs[Fs.index(best_fit)] -= job_size[w]

                    fat['S'] = Fs.copy()
                    fat['Loc'] = Floc.copy()

                    terminating[w+1] = t + run_time[w]
                    terminating = {k: v for k, v in sorted(terminating.items(), key=lambda item: item[1])} # Sort dict by values
                    waiting.pop(0)
                    waiting = waiting_job(waiting, started_jobs)
                    f_list.append(fat.copy())
                    p_list.append(pat.copy())

    else:
        for i in range(len(terminating)):
            for s in range(len(pat['Status'])):
                try:
                    J = re.search(f'J(.*)', pat['Status'][s]).group(1)
                    if int(J) == list(terminating)[0]:
                        t_time = time_format('00:'+str(list(terminating.values())[0]))
                        message.append(f'At {t_time} J{list(terminating)[0]} terminated')

                        FA_num.append(FA_num[-1]+1)
                        Fstatus.append('Available')
                        Fs.append(pat['S'][s])
                        Floc.append(pat['Loc'][s])

                        fat['FA#'] = [i+1 for i in range(len(Fs))]
                        fat['S'] = Fs.copy()
                        fat['Loc'] = Floc.copy()
                        fat['Status'] = Fstatus.copy()

                        # Sort by location
                        for i in range(len(fat['Loc'])-1):
                            for j in range(0, len(fat['Loc'])-i-1):
                                if fat['Loc'][j] > fat['Loc'][j+1] :
                                    fat['Loc'][j], fat['Loc'][j+1] = fat['Loc'][j+1], fat['Loc'][j]
                                    Floc = fat['Loc']
                                    fat['S'][j], fat['S'][j+1] = fat['S'][j+1], fat['S'][j]
                                    Fs = fat['S']
                        
                        # Compress size
                        end = False
                        while not end:
                            if len(Floc) > 1:
                                for item in range(len(Floc)-1):
                                    x = Fs[item] + Floc[item]
                                    if Floc[item+1] == x:
                                        Fs[item] = Fs[item] + Fs[item+1]
                                        FA_num.pop(-1)
                                        Floc.pop(item+1)
                                        Fs.pop(item+1)
                                        Fstatus.pop(-1)
                                        break
                                    elif item == len(Floc)-2:
                                        end = True
                            else:
                                end = True
                        
                        fat['FA#'] = [i+1 for i in range(len(Fs))]
                        fat['S'] = Fs.copy()
                        fat['Loc'] = Floc.copy()
                        fat['Status'] = Fstatus.copy()
                        
                        process.pop(-1)
                        Ps.pop(s)
                        Ploc.pop(s)
                        Pstatus.pop(s)

                        if process == []:
                            pat = {'Partition' : [1],
                                    'S' : ['-'],
                                    'Loc' : ['-'],
                                    'Status' : ['ee']}
                        else:
                            pat['Partition'] = [i+1 for i in range(len(Ps))]
                            pat['S'] = Ps.copy()
                            pat['Loc'] = Ploc.copy()
                            pat['Status'] = Pstatus.copy()
                except (AttributeError, IndexError):
                    pass

            terminating.pop(list(terminating)[0])
            if with_compaction and pat['S'] != ['-']:
                loc = [OS_SIZE]
                for size in Ps:
                    loc.append(size + loc[-1])

                FA_num = [1]
                Fs = [sum(Fs)]
                Floc = [loc.pop(-1)]
                Fstatus = ['Available']
                Ploc = loc

                fat['FA#'] = FA_num.copy()
                fat['S'] = Fs.copy()
                fat['Loc'] = Floc.copy()
                fat['Status'] = Fstatus.copy()

                pat['Partition'] = [i+1 for i in range(len(Ps))]
                pat['S'] = Ps.copy()
                pat['Loc'] = Ploc.copy()
                pat['Status'] = Pstatus.copy()
            f_list.append(fat.copy())
            p_list.append(pat.copy())

    # Create Memory Map
    LOC = []
    loc_temp = []
    for i in range(len(f_list)):
        for f in range(len(f_list[i]['Loc'])):
            loc_temp.append(f_list[i]['Loc'][f])
            f_size = f_list[i]['S'][f]
        for p in range(len(p_list[i]['Loc'])):
            if p_list[i]['Loc'][p] != '-':
                loc_temp.append(p_list[i]['Loc'][p])
                p_size = p_list[i]['S'][p]
        loc_temp.append(MEMORY_SIZE)
        LOC.append(sorted(loc_temp))
        loc_temp = []


    # Create Labels
    label_temp = ['OS']
    Label = []
    for sets in range(len(LOC)):
        for pos in range(len(LOC[sets])):
            for f in range(len(f_list[sets]['Loc'])):
                if LOC[sets][pos] == f_list[sets]['Loc'][f]:
                    f_size = f_list[sets]['S'][f]
                    label_temp.append(f'F{f+1}={f_size}')
            for p in range(len(p_list[sets]['Loc'])):
                if LOC[sets][pos] == p_list[sets]['Loc'][p]:
                    p_size = p_list[sets]['S'][p]
                    label_temp.append(f'P{p+1}={p_size}')
        Label.append(label_temp)
        label_temp = ['OS']

    for i in range(len(LOC)):
        for j in range(1, len(LOC[i])):
            if LOC[i][j-1] == LOC[i][j]:
                LOC[i].pop(j)
                Label[i].pop(j)

    from copy import deepcopy
    for i in range(len(f_list)):
        for j in range(len(f_list[i]['S'])):
            if f_list[i]['S'][j] == 0:
                ff = {'FA#': [None], 'S': [None], 'Loc': [None], 'Status': ['Memory full']}
                f_list[i] = deepcopy(ff)

    CPU_Wait = [to_minutes(list(St.values())[i]) - to_minutes(arrival_time[i]) for i in range(len(arrival_time))]
    Start = list(St.values())
    Finish = list(Ft.values())

    print('Start: ', Start)
    print('Finish: ', Finish)
    print('CPU_Wait: ', CPU_Wait)

    print(len(LOC) == len(p_list) == len(f_list) == len(message))

    print()
    print(f'Dynamic Best Fit, compaction = {with_compaction}')

    return [LOC, Label, message, f_list, p_list, Start, Finish, CPU_Wait]
